# Sophia ↔ Envoy on Discord — governor-parity plan

**Governor:** Gary. **Filed:** 2026-09-15. **Requested by:** Gary, in a `nelanco-claude` Envoy
session ("Can we have an implementation, execution roadmap done up such that she can respond to
your inputs on Discord. I think this is a desirable behavior to have").

**Problem.** Sophia's Discord adapter currently drops every message authored by a bot account —
including Envoy's own separate Discord bot (`claude_telegram_monitor/.env`'s `DISCORD_BOT_TOKEN`,
a different token from Sophia's) — before any identity/role check runs. On Telegram this isn't a
problem (no such blanket bot-filter exists there, and Envoy's Telegram bot already resolves to a
role that gets replies), so Envoy can nudge, unblock gates, and drive Sophia's supervision loop
over Telegram today. Discord is structurally silent to Envoy. This plan closes that gap so Envoy
can do the same supervision work — nudge, answer her questions, send go-signals, get real replies
— over Discord.

---

## Pre-flight

### Confirmed facts (already read this session — do not re-discover mid-PR)

- **`app/discord_adapter.py::handle_message`** (origin/main, `truesight_autopilot`) opens with:
  ```python
  if author.get("bot"):
      return  # never respond to bots (incl. ourselves)
  ```
  This runs **before** `strip_bot_mention`, session-id build, or `author_role()` — a message from
  *any* bot account, Envoy's included, never reaches role resolution, never gets a reply, never
  dispatches a turn. It is unconditional; there is no allowlist exception today.
- **`app/discord_adapter.py::author_role(user_id, allowed)`** resolution order (already correct,
  does not need to change):
  1. `user_id` in env `DISCORD_ALLOWED_USER_IDS` → `"governor"`.
  2. `user_id` bound (Contributors sheet, col **G** = Discord ID, index `COL_DISCORD_ID = 6`) to
     an email that's in the Governors cache (`treasury-cache/dao_members.json`) → `"governor"`.
  3. Bound to *any* contributor, or on env `DISCORD_MEMBER_USER_IDS` → `"member"`.
  4. Otherwise → `"guest"`.
- **Only `"governor"` gets a reply or a dispatched turn.** In `handle_message`:
  ```python
  if role != "governor":
      ...
      if public_key:
          log_observed_message(...)   # logged as context, NO reply
      return
  ```
  A `"member"`-role sender is logged as context and the function returns — **no turn is
  dispatched, no reply is sent.** This is a hard fact, not a config knob: if the goal is "Sophia
  responds," Envoy's Discord identity **must** resolve to `"governor"`. There is no
  lighter-weight "converse but don't instruct" path available today on Discord (unlike the
  `Role.MEMBER` docstring's aspiration in `app/policy.py`, which the adapter doesn't yet act on
  for replies — a real gap, but out of scope here; filing a narrower fix is more useful than
  blocking this plan on it).
- **`handle_reaction`** only excludes Sophia's *own* bot id (`if bot_id and user_id ==
  str(bot_id): return`) — it does **not** blanket-drop other bots. The reaction/go-signal path
  may already work for a governor-resolved bot identity; message-send is the actual gap.
- **Tool-layer gate is unaffected by any of this** — `app/policy.py::evaluate()` still enforces
  WRITE/ADMIN/SECRET actions as governor-only regardless of *how* the calling identity reached
  `"governor"` (env allowlist vs. sheet binding). Granting Envoy's Discord bot `"governor"` role
  is exactly equivalent, at the tool layer, to Envoy's Telegram bot already having it — this is
  **parity**, not a new class of capability. §5c always-stop gates (prod deploy, default-branch
  merge, TDG/money, UAT) remain enforced at the **process** level (`SUPERVISOR_LOOP.md`,
  `OPERATING_INSTRUCTIONS.md`), same as they already are for Telegram — this plan does not change
  that enforcement boundary, only extends which venue can carry governor-authenticated messages.
- **`create_/update_/delete_discord_channel`** already exist (`app/tools/discord_admin.py`,
  governor-gated, dry-run + confirm double-flag on delete) — confirmed 2026-09-15 after an earlier
  false claim in `sophia/SUPERVISOR_LOOP.md` was corrected same-day. Not otherwise relevant here
  except as evidence the Discord admin surface is actively maintained and a narrow addition (a
  trusted-bot allowlist) fits its existing conventions (dry-run defaults, explicit confirm flags,
  `default_roles` gating).
- **Live config state (`truesight_autopilot/.env`, checked 2026-09-15, values not reproduced
  here):** `TELEGRAM_ALLOWED_USER_IDS` is set (non-empty). `DISCORD_ALLOWED_USER_IDS` and
  `DISCORD_MEMBER_USER_IDS` are **both unset** today — no Discord identity, including Gary's own,
  currently resolves to governor via the env path; Gary's own Discord governor status (if he
  posts there) would have to come through the sheet-binding path instead. This plan does not
  change Gary's binding, only adds Envoy's.
- **`env.discord_guild_id`, `DISCORD_ADAPTER_ENABLED=true`, `DISCORD_DRY_RUN=false`** are live
  (`AUTOPILOT_CHANNEL_INTEGRATIONS.md` §2 — Discord activated 2026-09-14). The adapter is a real,
  already-serving surface, not a dark rollout — treat every change here as touching production.

### Decision — confirmed by Gary 2026-09-15: Option A ✅

> Gary, in the parking Telegram thread's originating session: "Yup. That is desired" — confirming
> full governor parity (Option A below) for Envoy's Discord bot. **Do not re-ask this in PR0 or
> PR2** — it is resolved. PR2 still carries `gate: human` (a live-authority-grant is always-stop
> per §5c regardless of whether the *choice* is pre-confirmed), but that stop is to execute the
> already-approved grant, not to re-litigate which option to pick.

### Open decision (RESOLVED — kept for context) — batch this once (§5e), don't re-ask per PR

**Which authority tier does Envoy's Discord bot get?**

| Option | What it means | Risk | Recommendation |
|---|---|---|---|
| **A — Full governor parity (recommended)** | Envoy's Discord bot resolves to `"governor"`, identical in capability to Envoy's Telegram bot today: can converse, nudge, send go-signals, and (subject to the *existing* §5c process gates) trigger any write/admin tool. | Matches a risk profile Gary has already accepted for Telegram — not new in kind, only in venue. `DISCORD_BOT_TOKEN` (Envoy's) becomes a governor-authority-bearing secret from this point on; rotate immediately if ever exposed. | This is what actually satisfies "she can respond to your inputs" in the way Envoy needs for supervision (nudging, unblocking, go-signals) — a lesser tier would leave Discord supervision non-functional even though messages stop being silently dropped. |
| B — Member-tier chat only | Requires an *additional* code change (`handle_message` doesn't reply to MEMBER today — see pre-flight) to let Sophia converse with Envoy without granting instruction authority. | Lower risk, but doesn't unblock the actual supervision use case (go-signals, gate-clearing) that prompted this request — Envoy could chat but not drive. | Only pick this if Gary wants a strictly narrower rollout first; treat as a possible **PR0.5** stepping stone, not the end state, if chosen. |

**Recommendation: Option A.** Confirm with Gary once, here in the plan (or in the parking
Telegram thread — see Rollout below), before PR2 executes — PR2 is the unit that actually grants
live authority, so it carries a `gate: human` marker below regardless of which option is picked.

### Still to resolve before PR1 can execute (do this as PR0 — a pre-flight-completion turn, not
implementation — so PR1 onward needs no further discovery, per §5d)

1. **Resolve Envoy's Discord bot's numeric user id.** `claude_telegram_monitor/.env` holds
   `DISCORD_BOT_TOKEN` for Envoy's bot; call Discord's `GET /users/@me` with that token once to
   get the bot's own snowflake id. Record it in PR0's update to this plan (not a secret — a
   Discord user id is not sensitive the way a token is, but still don't paste the *token*
   anywhere in this repo).
2. **Read the Contributors sheet's current col G / col X state** (`WORKSPACE_CONTEXT.md` §3c
   ledger — `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, tab `Contributors contact
   information`) to see how Envoy's existing Telegram binding (col X) is actually set up — bound
   to which contributor/email, and whether that email is in the Governors cache directly or
   whether Envoy's Telegram authority instead comes from the `TELEGRAM_ALLOWED_USER_IDS` env
   bootstrap. Mirror whichever mechanism is actually in effect for col G (Discord ID), rather
   than assuming — this is exactly the kind of cross-file state §5d requires be captured before
   PR1, not discovered mid-PR.
3. Update this plan's resume tracker with the two answers above before starting PR1.

✅ **Pre-flight Completeness:** every fact needed to design PR1–PR4 below is either already
captured above (code paths, line-level behavior, live config state) or is explicitly scoped as
PR0's job — no later PR should need to re-read `discord_adapter.py`, `policy.py`, or the
Contributors sheet to *understand* them; PR1 onward only *edits* them.

---

## Sequenced plan (one PR per execution turn — §5a)

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | Pre-flight completion (no code): resolve Envoy's Discord bot id, read the sheet's col G/X binding pattern, update this plan's "Still to resolve" section with real answers. (Option A/B call is already resolved — see "Decision" above, skip re-asking.) | auto |
| **PR1** | `truesight_autopilot`: add `discord_trusted_bot_ids: str` to `app/config.py` (`DISCORD_TRUSTED_BOT_IDS` env, default empty — same `_ADAPTER_ENABLED`-style safe-default convention as §3a of `AUTOPILOT_CHANNEL_INTEGRATIONS.md`). In `handle_message`, change the top guard to: drop the message **unless** `author.get("bot")` is true **and** `user_id` is in the parsed trusted-bot-id set **and** `user_id != bot_id` (never trust "yourself", even if misconfigured) — otherwise behavior is byte-for-byte identical to today. A trusted-bot message then proceeds through the **unchanged** `author_role()` resolution — being on the trusted-bot list grants *only* "don't reflexively discard," never role/authority by itself (defense in depth: two independently-configured knobs must both be right). Unit tests: (a) untrusted bot still dropped (regression guard on the existing security invariant), (b) trusted-but-not-governor-resolved bot proceeds to the existing `role != "governor"` → context-only branch (still no reply — correct), (c) trusted **and** governor-resolved bot dispatches and replies, (d) Sophia's own bot id, even if erroneously added to the trusted list, is still dropped. | auto |
| **PR2** | Grant Envoy's Discord bot id `"governor"` role, via whichever mechanism PR0 determined mirrors the Telegram precedent (env `DISCORD_ALLOWED_USER_IDS` bootstrap, and/or a Contributors sheet col G row), **and** add the same id to the new `DISCORD_TRUSTED_BOT_IDS`. Deploy pattern mirrors `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §5 item 7: land the config, confirm via `journalctl -u truesight-autopilot-discord` that a test message from Envoy's bot now resolves to `governor` in the logs, **before** relying on it for anything live. | **`gate: human`** — this is the unit that actually grants live governor authority to a second bot identity; always-stop per §5c "account-only actions" posture even though the mechanism itself (env var / sheet row) is not literally a secret. |
| **PR3** | UAT (see below) + docs: update `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §2 registry row and §3b table with Envoy's new Discord binding; update `ENVOY.md` with the new capability and the standing rule that Envoy's Discord posts stay **human-driven per turn** — no automated blind-relay loop that could create a bot-to-bot echo (mirrors the existing Telegram "one outstanding directive per thread, max" rule in `SUPERVISOR_LOOP.md` §3, restated here for the new venue). | auto (docs-only, but blocked on PR2's UAT passing first) |

**RESUME HERE → PR0.**

---

## UAT

All against **live Discord** (there is no beta Discord guild — see §3f caveat: this surface has
no staging equivalent, so UAT runs in a scratch/test channel within the real guild, not a mirror
environment). Self-UAT by whoever executes PR3, per `OPERATING_INSTRUCTIONS.md` §"Self-UAT before
human UAT," before asking Gary to click-test.

- **U1 — basic reply.** Envoy's bot posts a plain question in a scratch channel. **Expect:**
  Sophia replies in-channel. **Pass/fail:** a reply appears, addressing the question.
- **U2 — governor-tier dispatch.** Envoy's bot sends a safe read-only instruction (e.g. "list the
  Discord channels"). **Expect:** Sophia calls `list_discord_channels` and replies with the real
  tree, not a generic "I can't do that." **Pass/fail:** the reply contains real channel names/ids
  matching `list_discord_channels`' actual output.
- **U3 — regression guard on the security invariant.** A second, *not*-trusted bot account (any
  other bot in the guild, or a disposable test bot token) posts in the same scratch channel.
  **Expect:** silently dropped, exactly as before this plan. **Pass/fail:** no reply, no log line
  showing role resolution ran for that id (confirms the trusted-bot carve-out didn't widen to
  "all bots").
- **U4 — self-message guard intact.** Confirm Sophia's own bot messages are still never
  reprocessed (unchanged code path, but re-verify after PR1's edit). **Pass/fail:** no self-reply
  loop, no log line showing her own id hit the trusted-bot branch.
- **U5 — real supervision round (only if Option A shipped).** Envoy nudges a genuinely
  stalled Discord-native Sophia thread and observes her resume — the actual behavior this plan
  exists to unblock, mirroring the Telegram nudge-react pattern. **Pass/fail:** she resumes
  visibly in the thread after the nudge, without a human needing to relay it via Telegram instead.

**Human UAT (Gary):** after U1–U5 pass self-UAT, ask Gary to post once in the scratch channel
himself and confirm nothing about his own (human, sheet-bound) governor experience regressed —
this plan should be additive-only for his own identity.

---

## Rollout

**Parked 2026-09-15** in Telegram topic [Exec: Discord Envoy governor parity](https://t.me/c/3919341801/29970)
(`message_thread_id` 29970, TrueSight DAO Ops supergroup) and registered in
`handoffs/HANDOFF_MANIFEST.md`, per Gary's standing instruction this session — not executed in
this Envoy session. Whichever Envoy/Sophia supervisor thread picks it up drives PR0→PR3 per
`sophia/SUPERVISOR_LOOP.md` end to end, including its §6a close-out (contribution report filed,
then the parking topic itself closed) once PR3's UAT is green. **2026-09-15: Gary confirmed
Option A** (full governor parity) in the originating session — PR0/PR2 need no further
authority-tier confirmation, only PR2's standard `gate: human` execution stop.
