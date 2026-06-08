# Sophia handoffs — registry

Index of execution handoffs from a local LLM to **Sophia** (the autopilot).
**Each handoff opens its own Telegram topic** in `TrueSight DAO Ops`
(`-1003919341801`). This file is the durable, LLM-readable record so a future
local session can find, reference, and **rejoin** any handoff conversation.

## ⚠️ Pull-first rule (critical)

Before acting on ANY handoff mentioned in this file, **always `git pull` the
agentic_ai_context remote `main` branch first.** Plans are committed to the
remote by the handing-off LLM (Claude, Cursor, etc.) and may not be in your
local clone. Searching your local cache without pulling first will miss new
or updated plan files.

**Workflow:**
1. `cd agentic_ai_context && git pull origin main`
2. Check `HANDOFF_MANIFEST.md` for the active handoff list
3. Read the plan file referenced in the manifest
4. Read `SOPHIA_HANDOFFS.md` for Telegram topic context

## Before you start ANY handoff — refresh your repo view

Sophia/agents read a **synced clone** of this repo, which can be **stale**. A handoff doc may have been committed after your clone was last pulled. So the FIRST step of picking up any handoff is to refresh:

- Read the plan via **`read_repo_file`** (GitHub `main` — always current), **or**
- `ssh_run(host='autopilot', "cd /opt/truesight_autopilot/context/agentic_ai_context && git fetch origin main && git reset --hard origin/main")` then read.

Do **not** act on a possibly-stale local copy (this caused confusion on 2026-06-08).

## How to reference a handoff from a fresh local LLM

**How handoffs actually reach Sophia (the earlier claim here was WRONG).**
`ping_sophia` POSTs to the HTTP endpoint `https://sophia.truesight.me/chat-blocking`
with an `X-Session-Id` header. That endpoint returns Sophia's reply **in the HTTP
response to the caller** — it does **NOT** post into a Telegram topic on its own,
and its session does **not** automatically share memory with the Telegram-facing
Sophia the governor chats with. (Proven 2026-06-08: a handoff to thread 3 was
answered over HTTP but never appeared in Telegram, so the governor saw "no
handoff from Claude.") `session_id = tg:{chat_id}:{thread_id}` is just a **label**
tying a handoff to its topic in this registry — it is **not** a guaranteed bridge.

Therefore:
- **The durable handoff is the committed plan file + this registry** (always on
  GitHub `main`). That is the source of truth Sophia reads — every time.
- **The ping is only a *trigger*.** It MUST explicitly instruct Sophia to **post
  the context into a Telegram topic and wait there** (protocol below), so the
  governor finds her ready when they open Telegram.

To **rejoin** an existing handoff, ping with its `session_id` AND tell Sophia
which `message_thread_id` to post in:

```
truesight-dao-ping-sophia \
  --session-id tg:-1003919341801:<thread_id> \
  --message "Post in thread <thread_id>: where are we on <plan>? Summarize progress + blockers."
```

## Handoff trigger protocol (REQUIRED)

Every handoff must end with **Sophia waiting in a Telegram topic, the full
context already posted there** — so the governor finds her ready, not a cold
thread. The ping message MUST instruct Sophia to:

1. **Refresh** — read the plan via `read_repo_file` (GitHub `main`).
2. **Ensure a topic exists** — if none exists for this handoff, **create one**
   with `create_telegram_topic` named `<short title>`; otherwise use the given
   `message_thread_id`.
3. **Post the kickoff + context INTO that Telegram topic** (not just the HTTP
   reply): confirm she's read the plan, restate the RESUME-HERE step + key gates,
   state she's ready/parked.
4. **Reply with the `message_thread_id` + `t.me` link** (the handing-off LLM
   records it in the registry).
5. **Wait in that topic** for the governor.

Trigger-message template:

> Refresh first (read `<plan file>` via read_repo_file on GitHub `main`). If no
> Telegram topic exists for this handoff, create one named `<short title>` with
> create_telegram_topic; otherwise post in thread `<id>`. **Post your kickoff +
> context summary INTO that Telegram topic** — confirm you've read the plan,
> restate RESUME HERE + the gates, state you're ready/parked — then reply with
> the thread_id + link and wait there for the governor.

---

## Registry (newest first)

| Date | Handoff | Plan file | Topic | thread_id | session_id (to rejoin) | Status |
|------|---------|-----------|-------|-----------|------------------------|--------|
| 2026-06-08 | DAO client integration fixes (consolidated: oracle + capoeira) | `DAO_CLIENT_INTEGRATION_FIXES.md` | [topic](https://t.me/c/3919341801/3) | 3 | `tg:-1003919341801:3` | active |
| 2026-06-08 | Capoeira dao-client swap (PR2) | `CAPOEIRA_DAO_CLIENT_SWAP_PLAN.md` | [topic](https://t.me/c/3919341801/1658) | 1658 | `tg:-1003919341801:1658` | active |
| 2026-06-08 | Oracle CDN re-wire (@truesight_dao/dao-client) | `ORACLE_CDN_REWIRE_PLAN.md` | [topic](https://t.me/c/3919341801/1638) | 1638 | `tg:-1003919341801:1638` | active |
| 2026-06-08 | Resend verification email | `RESEND_VERIFICATION_PLAN.md` | [topic](https://t.me/c/3919341801/1504) | 1504 | `tg:-1003919341801:1504` | active |
| 2026-06-07 | THEOBROMA-1 (cacao brew, demo) | `SANDBOX_THEOBROMA_1_HANDOFF_DEMO.md` | [THEOBROMA-1](https://t.me/c/3919341801/1401) | 1401 | `tg:-1003919341801:1401` | demo · live |
