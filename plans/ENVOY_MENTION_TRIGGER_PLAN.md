# Envoy mention-trigger — execution roadmap

> Goal: Gary currently has to manually open/find a Claude Code session and prompt it to get
> Envoy supervising something. This roadmap builds a standing watcher with **two trigger
> sources** that wakes/injects into the `supervisor` tmux session on `nelanco-claude` in
> near-real-time: (1) an `@envoy` mention from the governor anywhere on Discord or Telegram,
> and (2) **new activity in any channel/thread Envoy is currently supervising** (per
> `HANDOFF_MANIFEST.md` + `active_supervision.json`) — e.g. Sophia posting a status update in
> a thread Envoy is actively watching should itself wake Envoy to review it, without needing
> an explicit mention. Matches the responsiveness Sophia already has via her own adapters.
>
> **Hard requirement, not optional:** every piece of code this plan produces must be
> committed to a real, git-tracked GitHub repo — never left as a local/scratch script on the
> box — specifically so a **future Envoy instance** (after a reboot, a fresh box, or
> `envoy-spinup.sh` recreating the tmux sessions) can deploy it without reconstructing
> anything from memory. See §7.

---

## 0. Pre-flight — facts captured, no execution unit should need to re-derive these

**Why Sophia has this and Envoy doesn't.** Sophia is architected as a persistent HTTP
service (`truesight-autopilot.service`) with live Discord/Telegram gateway listeners
(`app/discord_adapter.py`, `app/telegram_adapter.py`) that feed directly into her own agent
loop — a message arrives, she responds, same process. Envoy is architecturally different:
an interactive Claude Code CLI session running inside a tmux pane, with **no persistent
listening process today**. There is no `ping_envoy` equivalent to `truesight-dao-ping-sophia`
(confirmed: only `ping_sophia.py` exists in `dao_client/truesight_dao_client/modules/`), and
no systemd service or crontab entry on `nelanco-claude` currently watches Discord/Telegram
for mentions (confirmed via `systemctl list-units` + `crontab -l`, both empty of anything
Envoy-related).

**Telegram — half the plumbing already exists.** `@nelanco_claude_bot` already runs as a
persistent long-poll listener, `claude-telegram-monitor.service` (code: private repo
`TrueSightDAO/claude_telegram_monitor`, `Restart=always`, runs as `ubuntu`). It's a member
of **TrueSight DAO Ops** (chat_id `-1003919341801`) and **Bionpact work area**
(`-1003840338729`), and logs every message from **trusted senders only** — `TRUSTED_SENDER_IDS
= {garyjob (2102593402), @truesight_autopilot_bot (8217115914), @bionpact_bot (8928965571)}`
— to `/opt/claude_workspace/claude_telegram_monitor/messages.jsonl` (JSONL, append-only,
offset tracked in `offset.txt`, gitignored, chmod 600). Everyone else and every other chat
is **silently dropped** — this is the existing security invariant, not a gap to fix.
**Explicitly documented as log-only by design** (`listener.py` docstring): "nothing here
acts on messages or replies automatically — a Claude Code session reads the log when asked
to check in." **That "when asked" is exactly the gap this plan closes** — the log already
has the data; nothing currently watches it proactively or wakes a session on a new entry.

**Discord — nothing exists for Envoy.** Envoy's own bot identity is `envoy_truesight`
(user id `1548902290344255600`, same guild `923008087315587072` as Sophia's
`sophia_truesight`). Confirmed via API this session: no live gateway/WebSocket listener
process, no systemd unit, no polling script. All Discord activity from Envoy this session
has been one-off outbound REST calls (curl + bot token), never inbound. **Token's canonical
storage location is not yet confirmed** — a scratch copy exists at
`/tmp/claude-1000/.../scratchpad/dtok.txt` (this session's working copy), but the durable
credential file (likely alongside `claude_telegram_monitor/.env` or in
`truesight_autopilot/.env`) needs confirming in U1 below, not assumed.

**The "wake a tmux session" mechanism is novel and unverified.** No prior art exists in this
repo for injecting text into a live, idle Claude Code CLI session via `tmux send-keys` (or
any other mechanism) and having it treated as a real prompt. This is the single biggest
technical risk in this plan and must be de-risked **first**, before building either watcher
around it (§2 PR1) — if `send-keys` doesn't reliably wake/prompt an idle session, the whole
design needs rethinking (e.g., Claude Code's `--remote-control` mode may expose a more
reliable injection path than raw tmux).

**Target session.** Per Gary's own framing ("your session or another session... named as
supervisor"), the injection target is specifically the `supervisor` tmux session defined in
`ENVOY_TMUX_SESSIONS.md` — the one already running a standing pull-based loop
(`sophia/SUPERVISOR_LOOP.md`). This plan does not change that loop's logic — it adds a new
*wake source* alongside its existing periodic self-pacing.

**Known gotcha to carry forward:** `ENVOY_TMUX_SESSIONS.md` documents that a box reboot
kills tmux sessions, and `envoy-spinup.sh` is the recovery script. **Out of scope for this
plan**: auto-respawning a dead `supervisor` session. If the session doesn't exist when a
mention lands, the watcher should log the gap loudly (not silently drop it) rather than try
to resurrect a tmux session itself — flagged as a follow-up, not core scope here.

**Supervised-channel activity — the second trigger source.** `HANDOFF_MANIFEST.md` already
carries structured `Discord channel id` / `Discord thread id` / `message_thread_id` (Telegram)
columns per row, and `active_supervision.json` carries free-text claims (this session's own
claims include channel ids in the `note` field — not yet structured, see §2 PR0-follow-up).
Together these already define "the set of channels/threads Envoy is currently supervising" —
no new state needs inventing, just reading what already exists. The watcher's second job:
on each poll, build that channel/thread set from both files, and treat **any new message in
one of them** (not just mentions) as a wake signal — e.g. Sophia posting a "done this turn"
update in a thread Envoy claimed should itself trigger review, the way it's happened
manually all session via Gary nudging Envoy to go check.

**Explicitly OUT OF SCOPE:**
- Multi-session routing (mentioning `@planner` vs `@analyst` vs `@supervisor` differently) —
  v1 routes every trigger to `supervisor` only.
- Auto-respawning a dead tmux session.
- Full feature parity with Sophia's adapter (personas, tiered response posture, channel
  whitelisting beyond the governor-gate). This is a narrow wake-mechanism, not a second
  full adapter.
- A full WebSocket Discord gateway (heavier than needed). REST polling at a modest interval
  (e.g. every 20–30s) is sufficient — the bar to beat is "Gary has to go find a session,"
  which could take minutes; 20–30s polling is already a large improvement and far simpler
  to build/operate than a persistent gateway connection.

---

## 1. Security invariant (carries over from the Discord/Telegram adapter precedent)

**Two different trigger sources need two different gates — do not conflate them.**

**(A) `@envoy` mention trigger — governor-only.** Same instruction-boundary invariant as
`plans/DISCORD_ADAPTER_PLAN.md` §3: message text is DATA, not INSTRUCTIONS, unless the
author resolves to a verified governor. A random guild member or channel visitor saying
"@envoy do X" must **never** reach the tmux injection path — it would mean arbitrary
untrusted text executing with Envoy's full fleet credentials and access.

- **Telegram side:** already enforced upstream by `TRUSTED_SENDER_IDS` in `listener.py` —
  only Gary's and Sophia's-bot's messages ever reach `messages.jsonl` in the first place.
  The new watcher only needs to additionally filter OUT Sophia-bot-authored entries (so her
  own Telegram chatter doesn't re-trigger Envoy via this path — her activity still triggers
  via (B) below if the thread is supervised) and match on an `@envoy`/`envoy` keyword in
  Gary's remaining messages.
- **Discord side:** must resolve the mention author's Discord user id against the governor
  identity the same way `discord_adapter.py` does — `garyjob = 849324553221832794` per
  `DISCORD_ADAPTER_PLAN.md` §2. Reuse that resolution (read from the Main Ledger
  "Contributors contact information" col G mapping, or hardcode the single known governor id
  with a comment pointing at the sheet as source of truth) — do **not** build a new identity
  store.

**(B) Supervised-channel-activity trigger — scoped by channel membership, not sender
identity.** Authorization here comes from the channel/thread already being in Envoy's
tracked supervision set (`HANDOFF_MANIFEST.md` + `active_supervision.json`) — that
membership is itself the governor-approved context (a human put it there via the normal
handoff/claim process), so per-message sender resolution isn't required the way it is for
(A). The one filter still needed: **exclude messages authored by Envoy's own bot identity**
(`envoy_truesight` on Discord; Envoy doesn't post to Telegram today but guard it anyway) to
avoid a self-triggering loop where Envoy's own "done this turn" post wakes itself.

---

## 2. PR roadmap — one PR (or one spike/unit) per turn

| # | Scope | Repo | Gate |
|---|---|---|---|
| U1 | Confirm `envoy_truesight` Discord bot token's canonical storage location (read-only investigation) | n/a | auto |
| PR1 | **De-risking spike**: prove `tmux send-keys -t supervisor "<text>" Enter` (or `--remote-control`'s own injection path, whichever is more reliable) actually wakes an idle Claude Code CLI session and gets treated as a real prompt. Minimal standalone test, not production code. Report findings even if the answer is "doesn't work, needs a different mechanism." | n/a (scratch test on `nelanco-claude`) | auto — but **blocks PR3/PR4** until proven |
| PR2 | Telegram watcher: small script/service that tails `claude_telegram_monitor/messages.jsonl` (own read-only offset, separate from the listener's own `offset.txt` — never touch that file), filters to Gary-authored messages containing `envoy`/`@envoy`, and on match calls the injection mechanism proven in PR1 | `claude_telegram_monitor` (or a small new repo if that one is policy-walled — confirm) | auto → review |
| PR3 | Discord watcher: lightweight REST poller (every 20–30s) against whitelisted channels (start with the channels Envoy has actually operated in this session — reuse that list, don't guess a broader scope), filters to governor-id-only mentions of `envoy_truesight`'s user id, dedup via last-seen message id per channel, on match calls the same injection mechanism | new small script, likely `claude_telegram_monitor` repo (co-locate with the Telegram watcher) or `truesight_autopilot` if that's the more natural home — decide in PR3, don't pre-guess here | auto → review |
| PR4 | Supervised-channel-activity watcher (trigger source B): on each poll, read `HANDOFF_MANIFEST.md` + `active_supervision.json`, build the current channel/thread set (Discord + Telegram), poll each for new messages not authored by Envoy's own identity, dedup via last-seen message id per channel/thread, on any new message call the same injection mechanism. Reuses PR2/PR3's polling + dedup machinery rather than a third parallel implementation. | same repo as PR2/PR3 | auto → review |
| PR5 | systemd unit(s) for all watchers (`Restart=always`, matches the existing `claude-telegram-monitor.service` pattern), deployed on `nelanco-claude` | ops (systemd on nelanco-claude) | **gate: human** — first activation of a new standing service that injects into a live privileged session; confirm before enabling, not before building/testing |
| PR6 | UAT: live end-to-end test — Gary `@envoy`-mentions in both Discord and Telegram (trigger A), AND Sophia posting in a supervised thread (trigger B), confirm the `supervisor` session receives and visibly acts on both within the expected latency window | n/a | **gate: human** (this IS the UAT) |
| PR7 | Update this plan's header to `Status: LIVE` (mirroring `DISCORD_ADAPTER_PLAN.md`'s own convention) + a short operator doc (how to check the watchers are alive, how to redeploy on a fresh box) in `agentic_ai_context` | `agentic_ai_context` | auto (docs) |

**Do not combine PR1 with PR2/PR3** — the spike must land and be confirmed working before
either watcher is built around it, per §0's risk note.

---

## 3. Resume tracker

**2026-10-20: U1 done.** `envoy_truesight`'s Discord bot token is confirmed at
`claude_telegram_monitor/.env` → `DISCORD_BOT_TOKEN` (co-located with `TELEGRAM_BOT_TOKEN` as
predicted in §0) — verified live against Discord's `/users/@me`: resolves to id
`1548902290344255600`, username `envoy_truesight`. No further lookup needed; PR2/PR3 can read
this file directly.

**2026-10-20: PR1 (de-risking spike) PROVEN — `tmux send-keys` works.** Ran the spike in a
throwaway tmux session (`pr1-spike-test`, killed after), not against the live `supervisor`
pane (which was mid-conversation with Gary at the time — injecting into it would have
corrupted an in-flight draft). Sequence: `tmux send-keys -t <session> -l "<text>"` (literal
mode, so the text isn't reinterpreted as key names) followed by a separate `tmux send-keys -t
<session> Enter`, with a ~1s gap between the two calls. Result: the idle Claude Code CLI
session picked up the injected text as a genuine user turn and responded correctly to an
explicit instruction embedded in it (replied with a specific verification string on request)
— full round-trip proof, not just "text appeared in the box." **Separately corroborated**
earlier this same day: the same `-l` + `Enter` sequence, sent into the live `supervisor`
session from a different thread (the Discord-gateway-RESUME handoff), was picked up and
acted on (`supervisor` visibly began working on it). Two independent real-world confirmations.
**Mechanism is proven — PR3/PR4 are unblocked.** No fallback to `--remote-control` injection
needed.

**Open edge case for PR2/PR3 to handle, not re-litigate:** what happens if `send-keys` fires
while the target session is **mid-turn** (actively generating), rather than idle at its
prompt — observed informally today (the live `supervisor` pane had unsubmitted draft text
sitting in its input while a prior turn's status widgets were still rendered). The watchers
should assume text can land in a non-empty input box and must not assume the box starts
empty; this is a PR2/PR3 concern, not a PR1 blocker (PR1's scope was proving idle-session
injection only, which it did).

**2026-10-20: PR1 done — injection mechanism PROVEN.** (Recording the finding explicitly, per §7's
"a future instance must not reconstruct this from memory" bar; the earlier entry above described
the spike's *intent*, not its outcome.) The sequence that actually works is:

```
tmux send-keys -t supervisor -l -- "<text>"     # literal burst — one keystroke blob
tmux send-keys -t supervisor Enter              # SEPARATE call — this is what submits
```

Combining the two (`send-keys "<text>" Enter`) makes tmux interpret `Enter` **inside** the
literal string; the session then never submits and the text sits unsubmitted in the box. This
was §0's single biggest technical risk and it is now retired — raw tmux injection is sufficient,
no `--remote-control` fallback needed.

**2026-10-20: PR2 done.** `claude_telegram_monitor` **PR #5**, squash-merged as `6eb4d50`.
Source A (governor-only `envoy`/`@envoy` mentions) ships as a new `envoy_trigger/` package
(`trigger_source.py` / `telegram_source.py` / `inject.py` / `watcher.py`, 54 tests, no network or
tmux needed to test). It tails `messages.jsonl` through its **own** cursor
(`envoy_trigger_offset.txt` + `envoy_trigger_seen.jsonl`) and never touches the listener's
`offset.txt`.

Two things PR3/PR4 inherit from PR2 and should not re-derive:

- **`build_sources()` is the seam for source B.** Source A is one `TriggerSource`
  implementation; PR4 appends `SupervisedActivitySource` in that one function and nothing in
  `inject.py` or the daemon core changes. Source B is a drop-in, not a rewrite.
- **The "non-empty input box" edge case has a second failure mode.** Beyond draft text sitting
  in the box, `capture-pane` renders an *idle* box as `│ >        │` — whose trailing
  box-drawing border reads as draft text unless the vertical rules are stripped first. Without
  that strip, every idle box classifies as DRAFT and nothing ever gets injected. `inject.py`
  now strips box edges before matching, and all non-ready panes fail closed (trigger stays
  un-acked and is retried) rather than typing into an unknown TUI state.

**2026-10-20: PR3 done.** `claude_telegram_monitor` **PR #7**, squash-merged as `385b3c1`.
Source A's Discord half ships as `discord_source.py` (`DiscordMentionSource`), a second
`TriggerSource` registered in `build_sources()` alongside PR2's Telegram source — exactly the
drop-in PR2 set up for. REST-polls a small fixed channel whitelist (`envoy-server`,
`server-administration` — **not** the whole 70-channel guild, per §0's scoping note), with its
own per-channel cursor (`envoy_trigger_discord_cursors.json`) + seen store
(`envoy_trigger_discord_seen.jsonl`), mirroring PR2's ack-only-after-success contract. 24 new
tests (107 total across the two PRs' own counts — 83 after this PR specifically; see that
repo's README), no network/tmux needed (HTTP layer injected). `envoy-mention-watcher.service`
(the plan PR5 systemd unit) also landed in this PR, not yet installed/enabled.

**Real gap found + fixed operationally, not by changing tested code:** dry-running the merged
PR2 code against this box's actual `messages.jsonl` (44MB / 85k+ lines of real history, no
`envoy_trigger_offset.txt` yet) showed it replays **every historical `@envoy` mention ever
logged** as a fresh trigger on first start, because `JsonlTailer` defaults to offset 0 when
the offset file is absent — correct for the unit tests' fixture-then-construct pattern, wrong
for a cold start against a box with real history. Rather than changing `JsonlTailer`'s tested
default, seeded `envoy_trigger_offset.txt` to the current EOF as a one-time bootstrap
(documented as a **required** step in the repo's README for any future fresh-box redeploy) and
verified clean with `--once --dry-run` showing zero backlog. The Discord source doesn't need
this — it self-baselines per channel on first poll.

**2026-10-20: PR4 done.** `claude_telegram_monitor` **PR #8**, squash-merged as `f49db4c`.
Source B ships as `supervised_source.py` (`SupervisedActivitySource`) — one `TriggerSource`
covering both platforms, registered in `build_sources()` as the plan anticipated. Membership
in the manifest's structured columns is the only gate; Sophia's own activity in a supervised
thread triggers, matching §0's worked example exactly. 18 new tests, 101 total. Found +
fixed the same cold-start bootstrap gap as PR3, this time in this source's own independent
Telegram cursor (`envoy_trigger_supervised_tg_offset.txt`) — seeded to current EOF, same as
PR3's fix, now documented together in the repo README.

**2026-10-20: PR5 done — deployed and enabled.** `envoy-mention-watcher.service` copied to
`/etc/systemd/system/`, `daemon-reload` + `enable --now` on `nelanco-claude`. Verified via
`systemctl status` (`active (running)`, `enabled` — survives reboot) and ~25s of live
`journalctl` across multiple poll cycles: no crash, no backlog flood (both bootstraps held),
only the expected repeated `discord poll non-200 ... 404` warnings for 5 of the 11 manifest
Discord channel ids (likely stale entries or channels the bot isn't a member of — logged
loudly per the plan's requirement, not investigated further here as it's a manifest
data-quality question, not a daemon bug). This was a governor-authorized activation (explicit
go-ahead given in-session), satisfying the §5c always-stop gate for first activation.

**2026-10-20: PR6 (live UAT) — in progress, real bug found + fixed live.** Gary posted real
activity in two supervised Discord channels. The daemon correctly detected it (source B,
`supervised_activity`, 5 triggers staged from `#sitio-catarinense`) — but **every single
injection attempt failed with `pane_unknown`**, confirmed via `journalctl` (dozens of real
retries, zero successes). Root cause: `inject.py`'s `PROMPT_RE` only matched an ASCII `>`
prompt character; this box's actual Claude Code build renders the prompt as `❯` (a different
Unicode glyph), which `>` can never match — `assess_pane()` was silently returning `UNKNOWN`
for every real pane, idle or not, on **every source**, since PR2. Every existing test fixture
happened to use the ASCII glyph, so the whole 101-test suite was green while the live daemon
could never inject anything into any session, ever. Fixed in `claude_telegram_monitor` **PR
#9** (merged `ea49121`): `PROMPT_RE` now matches either glyph, 3 new regression tests pin the
real one down (104 tests total). Service restarted to pick up the fix — confirmed live:
classification correctly shifted from `pane_unknown` to `pane_busy`/`pane_draft` as Gary
actively used the `supervisor` pane during the restart window (correctly deferring rather
than clobbering his draft — proof the fix works in both directions). The 5 staged triggers
from Gary's test are un-acked and safely queued; they'll inject the moment the pane goes
idle, with no further action needed. **Still open:** confirming a trigger actually lands
once the pane goes idle, and testing the `@envoy`-mention (source A) half specifically (the
activity so far only exercised source B, since `#sitio-catarinense` isn't in the Telegram/
Discord mention whitelists).

**2026-10-20: second UAT round — a second real bug found + fixed, then a real injection
confirmed live.** Gary reported `supervisor`'s pane as idle; the daemon still classified it
`pane_draft`. Root cause (a second, more general instance of the #9 bug class): Claude Code
renders a *different* dim placeholder hint depending on context ("Keep monitoring the two
threads", SGR dim-styled) — not just the couple of strings `CLEAN_PROMPT_HINTS` hardcodes, so
text-content matching could never fully enumerate every variant. Fixed in `claude_telegram_monitor`
**PR #10** (merged `1405f25`): `assess_pane()` now also takes the live cursor column
(`tmux display-message -p '#{cursor_x}'`) as an authoritative signal — the prompt is a fixed
2-column `"❯ "` prefix, so `cursor_x <= 2` means the box is empty regardless of what
decorative hint text is rendered underneath (verified empirically against two different real
placeholder variants now). 6 new tests, 109 total. Restarted the service —

**first real end-to-end injection confirmed live, immediately on restart:** one of the 10
queued `supervised_activity` triggers from Gary's earlier test injected successfully into the
live `supervisor` session (`journalctl`: `injected dc-supervised:...`), `supervisor` visibly
picked it up and began sensibly acting on it (checked a related GitHub PR), no garbling. The
remaining queued triggers correctly deferred (`pane_draft`) the instant the first injection
made the pane busy again — proving the one-at-a-time safety behavior works as designed, not
just the happy path.

**PR6 substantially passed.** The single biggest risk in this whole plan (§0: "does
`tmux send-keys` reliably wake a session") is now proven true end-to-end against the real
`supervisor` session, through source B. **Still open, not blocking:** an explicit `@envoy`
mention test (source A) — Gary's two tests both landed in a supervised-but-not-mention-whitelisted
channel, so only source B has been live-exercised; source A's detection logic is already
unit-tested and shares the exact same now-proven injection path, so this is a nice-to-have
confirmation, not a risk. PR7 (flip this plan's header to `Status: LIVE` + the operator doc)
can proceed.

**RESUME HERE → PR7** (docs: flip `Status: LIVE`, add the operator doc).

No execution unit above should need to read cross-repo state not already captured in §0.

---

## 4. UAT checklist (PR6)

**Trigger A (mention):**
- [ ] Gary posts "@envoy <test message>" in a Discord channel the watcher polls. `supervisor`
  tmux session visibly receives it and begins acting, within the polling interval + a few
  seconds.
- [ ] Gary posts the Telegram equivalent in TrueSight DAO Ops. Same result, within the
  Telegram watcher's check interval.
- [ ] A **non-governor** test message containing "@envoy" (if safely testable — e.g. a
  message from Sophia's bot, which is already in `TRUSTED_SENDER_IDS` but is NOT the
  governor) does **not** trigger an injection. This proves the security gate, not just the
  happy path.

**Trigger B (supervised-channel activity):**
- [ ] A thread/channel currently in `HANDOFF_MANIFEST.md`/`active_supervision.json` gets a
  new message from Sophia (or anyone other than Envoy's own bot identity) — `supervisor`
  wakes and reviews it, without any `@envoy` mention present.
- [ ] A message in a channel that is **not** in the supervised set does **not** trigger —
  proves the scoping, not just that polling works at all.
- [ ] Envoy's own posted message in a supervised channel does **not** self-trigger (loop
  guard works).

**Both:**
- [ ] If the `supervisor` tmux session doesn't exist when a trigger fires, the watcher logs
  this clearly (not a silent drop) — confirm the log line exists and is findable.
- [ ] All systemd units show `Restart=always` and survive a manual `systemctl restart`
  without losing their dedup/offset state (no duplicate re-injection on restart).

---

## 5. Gates

- No injection without governor-resolved authorship (§1) — this is the load-bearing security
  invariant of the whole plan, verify it explicitly in UAT, not just assume it from code
  review.
- PR4 (first systemd activation) and PR5 (UAT) are both human gates — this is new standing
  infrastructure with access to a privileged session, treat activation with the same care as
  a prod deploy even though it isn't literally one.
- One PR/unit per turn, per standing convention.

---

## 6. Open question carried forward, not blocking

Multi-session routing (which tmux session a mention should wake, if more than `supervisor`
is ever meant to be mention-triggered) is deliberately deferred — v1 is `supervisor`-only,
matching exactly what Gary asked for.

---

## 7. Deployability — hard requirement, not a nice-to-have

Gary's explicit instruction: *"The daemon codebase needs to be checked in to github so that
future instances can be deployed without complications."* Concretely, this means:

- **No code from this plan may live only as a local/untracked script on `nelanco-claude`.**
  Every watcher, the systemd unit files, and any helper scripts must be committed to a real
  GitHub repo under `TrueSightDAO` (PR2–PR5 above name the target repo per unit).
- **A future Envoy instance must be able to deploy this from a clean checkout** — i.e. `git
  clone` + read a README + run a documented install step, not "ask the session that built it
  how it works." If a step depends on a manually-placed credential file (matching the
  existing `claude_telegram_monitor/.env` pattern), document exactly what the file must
  contain and where, without ever committing the actual secret.
- **PR7 updates `agentic_ai_context`** once the watchers are live — this plan's own header
  flips to `Status: LIVE` (mirroring `DISCORD_ADAPTER_PLAN.md`'s convention) and a short
  operator doc is added describing: how to check both watchers are alive
  (`systemctl status`), what their dedup/offset state files are and where they live, and the
  redeploy steps for a fresh box. This is the same documentation bar every other piece of
  standing infrastructure in this repo is held to (see `ENVOY_TMUX_SESSIONS.md`'s own
  spin-up section as the model to follow).

---

*Created 2026-10-20, from Gary's direct ask: "I wonder there is a way for your session or
another session in the future named as supervisor to get triggered everytime you @envoy is
mentioned in either telegram or discord instead of needing me to always come to you to
trigger you to supervise." Cross-links: `DISCORD_ADAPTER_PLAN.md`, `ENVOY_TMUX_SESSIONS.md`,
`sophia/SUPERVISOR_LOOP.md`, `NELANCO_CLAUDE_CODE_BOX_PLAN.md` §8.*
