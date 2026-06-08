# Sophia handoffs — registry

Index of execution handoffs from a local LLM to **Sophia** (the autopilot).
**Each handoff opens its own Telegram topic** in `TrueSight DAO Ops`
(`-1003919341801`). This file is the durable, LLM-readable record so a future
local session can find, reference, and **rejoin** any handoff conversation.

## How to reference a handoff from a fresh local LLM

The magic field is **`session_id`** = `tg:{chat_id}:{thread_id}`. Because the
autopilot keys a chat session as `{governor_pubkey[:20]}:{X-Session-Id}`, a
local LLM that pings with that same `session_id` (and the same governor's
`./.env` keys) lands in **the exact same conversation thread as the Telegram
topic** — so it can pick up where Sophia left off:

```
truesight-dao-ping-sophia \
  --session-id tg:-1003919341801:<thread_id> \
  --message "Where are we on THEOBROMA-1? Summarize progress + blockers."
```

To start a **new** handoff: commit the plan to `agentic_ai_context`, then
`truesight-dao-ping-sophia` telling Sophia to open a topic named for it and
post a kickoff. Add a row below (newest first).

## Convention for the trigger message

> Open a new Telegram topic named `<short title>` and post a kickoff. You've
> taken over execution of `<plan file>` in agentic_ai_context — read its resume
> tracker and start at RESUME HERE. Report progress in this topic.

---

## Registry (newest first)

| Date | Handoff | Plan file | Topic | thread_id | session_id (to rejoin) | Status |
|------|---------|-----------|-------|-----------|------------------------|--------|
| 2026-06-08 | Resend verification email | `RESEND_VERIFICATION_PLAN.md` | [topic](https://t.me/c/3919341801/1504) | 1504 | `tg:-1003919341801:1504` | active |
| 2026-06-07 | THEOBROMA-1 (cacao brew, demo) | `SANDBOX_THEOBROMA_1_HANDOFF_DEMO.md` | [THEOBROMA-1](https://t.me/c/3919341801/1401) | 1401 | `tg:-1003919341801:1401` | demo · live |
