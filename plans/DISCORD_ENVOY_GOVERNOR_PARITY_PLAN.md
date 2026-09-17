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

### Decision — ✅ RESOLVED 2026-09-17: target tier is SENTINEL (2026-09-15 "Option A" withdrawn)

> **2026-09-17 (Gary, exec thread):** "*correction — Gary says Envoy should get SENTINEL role,
> not governor … route my Discord bot id through the SAME D4 sentinel mechanism you already
> built.*" Envoy's Discord bot is to resolve to `"sentinel"` — the DAO's AI-agent contributor
> tier (same as Claude / DeepSeek / Kimi / Sophia / the autopilot) — **no governor grant, no
> `DISCORD_ALLOWED_USER_IDS` entry.** Sentinels already carry governor-tier RIGHTS under the
> brain's WRITE/ADMIN gate (plan D4), so this still delivers full *supervision* parity.
>
> *Historical (superseded):* Gary, 2026-09-15 — "Yup. That is desired" (full governor parity).
> PR2's `gate: human` now covers only a live-config change, not a governor grant.

### Open decision — SUPERSEDED authority-tier question; the live question is the (i)/(ii) mechanism (gates PR2, not PR1)

**Which authority tier does Envoy's Discord bot get?** — **SUPERSEDED 2026-09-17: tier is fixed at `sentinel`** (see Decision). The live question is *how* Envoy's id resolves to sentinel: **(i)** add `1548902290344255600` to env `DISCORD_SENTINEL_USER_IDS` (recommended — mirrors his `TELEGRAM_ALLOWED_USER_IDS` precedent; already supported at `author_role` line 453; no cache/GAS dependency) **or (ii)** fix Finding A's `email:null` cache row so the existing col-W flag flows through `sentinel_emails()` (blocked behind a tokenomics GAS change). The Option A/B table below is retained for history only.

| Option | What it means | Risk | Recommendation |
|---|---|---|---|
| **A — Full governor parity (recommended)** | Envoy's Discord bot resolves to `"governor"`, identical in capability to Envoy's Telegram bot today: can converse, nudge, send go-signals, and (subject to the *existing* §5c process gates) trigger any write/admin tool. | Matches a risk profile Gary has already accepted for Telegram — not new in kind, only in venue. `DISCORD_BOT_TOKEN` (Envoy's) becomes a governor-authority-bearing secret from this point on; rotate immediately if ever exposed. | This is what actually satisfies "she can respond to your inputs" in the way Envoy needs for supervision (nudging, unblocking, go-signals) — a lesser tier would leave Discord supervision non-functional even though messages stop being silently dropped. |
| B — Member-tier chat only | Requires an *additional* code change (`handle_message` doesn't reply to MEMBER today — see pre-flight) to let Sophia converse with Envoy without granting instruction authority. | Lower risk, but doesn't unblock the actual supervision use case (go-signals, gate-clearing) that prompted this request — Envoy could chat but not drive. | Only pick this if Gary wants a strictly narrower rollout first; treat as a possible **PR0.5** stepping stone, not the end state, if chosen. |

**Recommendation:** tier is settled at **sentinel**; the only open call is the **(i)/(ii) mechanism**
above — **(i) recommended**. PR2 keeps its `gate: human` marker (it is the live-config change).

### Resolved in PR0 (2026-09-17) — do NOT re-discover (§5d)

**1 — Envoy's Discord bot id = `1548902290344255600`** (bot name `envoy_truesight`), via Discord
`GET /users/@me`. 📌 Token path corrected: the live token is at
**`/opt/claude_workspace/claude_telegram_monitor/.env`** on `nelanco-claude` (the original
`claude_telegram_monitor/.env` was stale). A Discord user id is NOT a secret; the **token is** —
never paste it.

**2 — Sheet col G / col X state** (row 418, tab `Contributors contact information`): Name
`Envoy TrueSight`; **col G (Discord ID) = `1548902290344255600` — already bound ✅**; col W
`Is Sentinel` = `TRUE` ✅; col D email = `admin+envoy@truesight.me`; col X (Telegram ID) **blank**
(Telegram authority comes from `TELEGRAM_ALLOWED_USER_IDS` env bootstrap — the env precedent (i)
mirrors). **No sheet edit needed.**

**3 — Three findings that reshape PR1–PR2:**

- **Finding A — the D4 chain is blocked by an `email:null` cache row, not just the bot-filter.**
  Live `dao_members.json` row: `{"name":"Envoy TrueSight","email":null,"roles":["member","sentinel"]}`.
  Roles correctly has `sentinel`, **but `email` is `null`** and `sentinel_emails()` keys on **email**
  → returns `{claude, deepseek, kimi, sophia, admin@}`, Envoy **absent** → `author_role(1548902290344255600)`
  → **`member`** (verified live). Root cause: cache builder (`tokenomics …/DaoMembersCache.js`)
  sources `email` only from "Contributors Digital Signatures" col F; contact-only names seed with
  `email:null`. (`Open Ai` shares the latent null-email sentinel row.)
- **Finding B — the dispatch premise is STALE.** Old pre-flight says "only `governor` gets a reply".
  No longer true: BRAIN_TIER_AWARENESS PR3 (merged 2026-09-17) set
  `is_instructive = role in ("governor", "sentinel")` — **sentinels are already dispatched.** So
  once Envoy *resolves* to sentinel, only the bot-filter carve-out is needed.
- **Finding C — deployed cache is schema v3, not v4.** `DaoMembersCache.js` declares
  `SCHEMA_VERSION = 4` (adds `discord_id`/`telegram_id`) but the live cache is `schema_version: 3`
  with **0 rows carrying `discord_id`** — the v4 builder exists but is not what is publishing.

✅ **Pre-flight Completeness:** every fact needed to design PR1–PR4 below is either already
captured above (code paths, line-level behavior, live config state) or is explicitly scoped as
PR0's job — no later PR should need to re-read `discord_adapter.py`, `policy.py`, or the
Contributors sheet to *understand* them; PR1 onward only *edits* them.

---

## Sequenced plan (one PR per execution turn — §5a)

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | ✅ **DONE 2026-09-17.** Resolved Envoy's Discord bot id (`1548902290344255600`) + read the sheet col G/X binding (col G already bound, col W=TRUE); surfaced Findings A/B/C above. No code changed. | — |
| **PR1** | `truesight_autopilot`: add `discord_trusted_bot_ids: str` to `app/config.py` (`DISCORD_TRUSTED_BOT_IDS` env, default empty — same `_ADAPTER_ENABLED`-style safe-default convention as §3a of `AUTOPILOT_CHANNEL_INTEGRATIONS.md`). In `handle_message`, change the top guard to: drop the message **unless** `author.get("bot")` is true **and** `user_id` is in the parsed trusted-bot-id set **and** `user_id != bot_id` (never trust "yourself", even if misconfigured) — otherwise behavior is byte-for-byte identical to today. A trusted-bot message then proceeds through the **unchanged** `author_role()` resolution — being on the trusted-bot list grants *only* "don't reflexively discard," never role/authority by itself (defense in depth: two independently-configured knobs must both be right). Unit tests: (a) untrusted bot still dropped (regression guard on the existing security invariant), (b) trusted-but-**not-sentinel**-resolved bot proceeds to the `observed` (context-only) branch — still no dispatch/reply, (c) trusted **and sentinel-resolved** bot dispatches (the target end state), (d) Sophia's own bot id, even if erroneously added to the trusted list, is still dropped. | auto |
| **PR2** | Get Envoy's Discord bot id (`1548902290344255600`) to **resolve to `"sentinel"`** via the mechanism Gary picks in PR0's open decision — **(i)** env `DISCORD_SENTINEL_USER_IDS` (recommended) **or (ii)** fix Finding A's `email:null` cache row so the col-W sentinel flag flows through `sentinel_emails()`. **No governor grant.** Also add the id to the new `DISCORD_TRUSTED_BOT_IDS`. Deploy pattern mirrors `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §5 item 7: land the config, confirm via `journalctl -u truesight-autopilot-discord` that a test message from Envoy's bot now resolves to `governor` in the logs, **before** relying on it for anything live. | **`gate: human`** — live-config change granting a second bot identity sentinel-tier dispatch rights (NOT a governor grant); always-stop per §5c even though the mechanism itself (env var / sheet row) is not literally a secret. |
| **PR3** | UAT (see below) + docs: update `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §2 registry row and §3b table with Envoy's new Discord binding; update `ENVOY.md` with the new capability and the standing rule that Envoy's Discord posts stay **human-driven per turn** — no automated blind-relay loop that could create a bot-to-bot echo (mirrors the existing Telegram "one outstanding directive per thread, max" rule in `SUPERVISOR_LOOP.md` §3, restated here for the new venue). | auto (docs-only, but blocked on PR2's UAT passing first) |

**RESUME HERE → PR1** (bot-filter carve-out; `truesight_autopilot`). PR0 ✅ done 2026-09-17.

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
