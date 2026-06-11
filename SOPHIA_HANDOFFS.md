# Sophia handoffs — registry

Index of execution handoffs from a local LLM to **Sophia** (the autopilot).

> 🗺️ **New here? Read [`HANDOFF_PROTOCOL_OVERVIEW.md`](HANDOFF_PROTOCOL_OVERVIEW.md)** for the big-picture map (actors, interfaces, mermaid flow diagrams, and the three human touchpoints). This file is the operational registry + conventions.
>
> 🔐 **Handing a secret (API key / token / webhook secret) to a box Sophia owns?** Follow [`CREDENTIAL_HANDOFF_PROTOCOL.md`](CREDENTIAL_HANDOFF_PROTOCOL.md): never put it in chat/Telegram/PRs — stage it on the autopilot box under `/home/ubuntu/` (`chmod 600`, value via stdin, outside the git repo), then hand off to Sophia (she holds the target-box keys) to propagate. The autopilot box is the credential-staging hub.
**Each handoff opens its own Telegram topic** in `TrueSight DAO Ops`
(`-1003919341801`). This file is the durable, LLM-readable record so a future
local session can find, reference, and **rejoin** any handoff conversation.

## ⚠️ Pull-first rule (critical)

Before acting on ANY handoff mentioned in this file, **always `git pull` the
agentic_ai_context remote `main` branch first.** Plans are committed to the
remote by the handing-off LLM (Claude, Cursor, etc.) and may not be in your
local clone. Searching your local cache without pulling first will miss new
or updated plan files.

> **Automatic safety net (truesight_autopilot#130, 2026-06-09):** Sophia's
> autopilot now hard-refreshes its read-only context mirrors
> (`agentic_ai_context`, `tokenomics`) to `origin/main` every ~5 min via a
> background loop (`_context_sync_loop`), so `read_context_file` /
> `search_context` no longer go stale between deploys (the root cause of the
> 2026-06-09 "plan doesn't exist" handoff miss — clone was 21 commits behind).
> This is a backstop, not a license to skip the rule: **`read_repo_file` on
> GitHub `main` is still the freshest read** and the recommended way to load a
> just-committed plan. Activated on the next deploy after the PR merged.

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

## Thread management — Sophia's two moves (truesight_autopilot#135)

Sophia has two topic tools, so she can structure work across threads:

- **`create_telegram_topic`** — open a NEW topic (+ optional kickoff). Use for a
  new handoff, or to **shard a sub-scope into its own thread**: open a topic, post
  a kickoff that names the plan file + the *specific* units/scope, and cross-link
  it from the parent. ⚠️ Each topic = a **separate autopilot session**, so the new
  thread's kickoff MUST carry its scope (plan + units) — a fresh session has no
  memory of the parent thread.
- **`post_to_telegram_topic`** — post into an EXISTING topic by `message_thread_id`.
  Use to **rejoin** a parked handoff, **report cross-thread** ("sandbox is ready,
  you can test"), or cross-link a sharded sub-thread back to its parent — without
  spawning a duplicate topic.

So the prior "always create a new topic" churn (1924→1939) is no longer forced:
prefer reusing the existing handoff thread via `post_to_telegram_topic`.

## Handoff runbook — for ANY local LLM (Claude, Cursor, Kimi, Codex, …)

The process is **agent-agnostic** — any local LLM on the governor's machine
follows the same five steps:

1. **Write the plan** (`*_PLAN.md` in `agentic_ai_context`, §5 shape: context,
   sequenced PRs, gates, RESUME HERE, acceptance) and commit it to **`main`**
   (PR → merge). **This committed plan is the durable handoff — the source of
   truth Sophia reads.**
2. **Add a registry row** (below, newest first): plan file + intended topic.
3. **Trigger Sophia** with `ping_sophia` using the trigger-message template below.
4. **Record the `message_thread_id`** Sophia replies with, in the registry row.
5. Give the governor the topic link. Done — Sophia is parked there with context.

## What the trigger MUST tell Sophia (REQUIRED)

Every handoff must end with **Sophia parked in a Telegram topic, full context
posted** — so the governor finds her ready, not a cold thread. The ping MUST
instruct Sophia to:

1. **Refresh** — read the plan via `read_repo_file` (GitHub `main`).
2. **Sophia opens (or reuses) the topic.** New handoff → `create_telegram_topic`
   (named `<short title>`), report its `message_thread_id`. **Existing thread**
   (rejoin / cross-link / report into a parked handoff) → **`post_to_telegram_topic`**
   (truesight_autopilot#135, 2026-06-09) — Sophia CAN now post into a thread she
   didn't create (the Bot API + adapter `send_message` always supported
   `message_thread_id`; it was just an unexposed tool). So the old "can only post
   into topics she creates" limitation is **retired**.
3. **Post the kickoff + context INTO the topic** (not just the HTTP reply):
   confirm she read the plan, restate RESUME HERE + the gates, state she's
   ready/parked, and **end with the GO prompt**:
   > ✅ Ready. Reply **"go for it"** and I'll execute from RESUME HERE through the
   > gates, reporting progress here.
4. **Reply with the `message_thread_id` + `t.me` link.**
5. **Wait** in that topic for the governor.

Trigger-message template:

> Refresh first (read `<plan file>` via read_repo_file on GitHub `main`). If no
> Telegram topic exists for this handoff, create one named `<short title>`
> (create_telegram_topic); else post in thread `<id>`. **Post your kickoff +
> context INTO that topic** — confirm you've read the plan, restate RESUME HERE +
> the gates, state you're ready/parked, and end with: 'Reply "go for it" and I'll
> execute from RESUME HERE.' Then reply with the thread_id + link and wait there.

## The GO convention (governor authorization)

Once Sophia is parked in a handoff topic, the governor authorizes execution by
replying in that topic with a short go-signal — **"go for it"**, "go",
"proceed", "ship it", "Sophia go for it". On that signal, Sophia:

- **Executes the plan** referenced in this topic's kickoff, **starting at RESUME
  HERE**, straight through its units.
- **Honors every gate without re-asking** — especially **open the PR, do NOT
  auto-merge** where the plan says so, the verify / runtime-smoke-test gates, and
  the `Generated-by: Sophia (TrueSight Autopilot)` trailer.
- **Reports progress + blockers in the topic**; pauses only at a real blocker or
  a step the plan explicitly marks for review.
- Treats the go-signal as **full authorization for the whole plan** — no per-step
  confirmation.

**The contract: after a handoff, the governor only needs to say "go for it."**

---

## Registry (newest first)

| Date | Handoff | Plan file | Topic | thread_id | session_id (to rejoin) | Status |
|------|---------|-----------|-------|-----------|------------------------|--------|
| 2026-06-11 | Live Progress Introspection (report what the executing turn is doing when Gary asks mid-turn) — **on Sophia's OWN codebase** | `SOPHIA_LIVE_PROGRESS_PLAN.md` | [Live Progress](https://t.me/c/3919341801/2799) | 2799 | `tg:-1003919341801:2799` | **active — Sophia parked GO-ready** (kickoff posted 2026-06-11); on GO executes PR1 (`_live_progress` + richer ack) → PR2 (lock-bypassing progress query); **opens PRs only, NEVER self-merges own-repo PRs** (human merges); UAT U1–U5 = completion gate |
| 2026-06-11 | Sophia Multi-Tenant Governance, Identity & Vault — **PHASE 0 only** (policy layer + tool-layer authorization + data-vs-instruction boundary + guest-default) — **on Sophia's OWN codebase** | `SOPHIA_MULTI_TENANT_GOVERNANCE_PLAN.md` | [Governance and Vault](https://t.me/c/3919341801/2744) | 2744 | `tg:-1003919341801:2744` | **active — Sophia parked GO-ready** (kickoff posted 2026-06-11); on GO executes **Phase 0 only** from RESUME HERE (PR0.1 `app/policy.py`), then STOPS for human merge + Phase 0 UAT P0.1–P0.4 before Phase 1; **opens PRs only, NEVER self-merges own-repo PRs** (human merges) |
| 2026-06-11 | Durable Follow-up Monitor (thread-bound, multi-day follow-ups; `gmail_reply` + `elapsed_days`; on strike spins a Sophia turn in the originating thread) — **on Sophia's OWN codebase** | `SOPHIA_FOLLOWUP_MONITOR_PLAN.md` | [Follow-up Monitor](https://t.me/c/3919341801/2622) | 2622 | `tg:-1003919341801:2622` | **active — Sophia parked GO-ready** (kickoff posted 2026-06-11); on GO executes from RESUME HERE (PR1 `app/followups.py`) through PR4; **opens PRs only, NEVER self-merges own-repo PRs** (human merges); UAT U1–U9 = completion gate |
| 2026-06-09 | Beta Sandbox Endpoint (beta.edgar.truesight.me; standalone NELANCO EC2 + beta dao_protocol in Stripe TEST) | `BETA_SANDBOX_ENDPOINT_PLAN.md` | [topic](https://t.me/c/3919341801/1955) | 1955 | `tg:-1003919341801:1955` | **active — Sophia parked GO-ready**; on GO executes from Unit 1, STOPS at operator gates (launch approval / prod deploy / Stripe dashboard); Unit 8 = mandatory AWS_DIGITAL_INFRASTRUCTURE.md update |
| 2026-06-09 | Agroverse Chocolate Subscriptions — Phase 1 (finalized plan w/ STOP gates) | `CHOCOLATE_SUBSCRIPTION_PLAN.md` | [topic](https://t.me/c/3919341801/1939) | 1939 | `tg:-1003919341801:1939` | **active — Sophia parked GO-ready**; on GO executes Phase 1 PR1.1–1.6, then STOPS at the operator test gate for Gary's local test-mode pass |
| 2026-06-09 | ~~Agroverse Chocolate Subscriptions (initial handoff)~~ | `CHOCOLATE_SUBSCRIPTION_PLAN.md` | [topic](https://t.me/c/3919341801/1924) | 1924 | `tg:-1003919341801:1924` | **SUPERSEDED by 1939** (kickoff predated the STOP-gate finalization) |
| 2026-06-08 | DAO client adoption audit (oracle + capoeira use lib, not hand-rolled) | `DAO_CLIENT_ADOPTION_AUDIT_PLAN.md` | [topic](https://t.me/c/3919341801/1776) | 1776 | `tg:-1003919341801:1776` | active (Sophia parked PR1, GO-ready) |
| 2026-06-08 | Morning Oracle Standup (draw → daily briefing in #General) | `MORNING_ORACLE_STANDUP_PLAN.md` | [topic](https://t.me/c/3919341801/1722) | 1722 | `tg:-1003919341801:1722` | active (Sophia parked PR1, GO-ready) |
| 2026-06-08 | DAO client integration fixes (consolidated: oracle + capoeira) | `DAO_CLIENT_INTEGRATION_FIXES.md` | [topic](https://t.me/c/3919341801/1695) | 1695 | `tg:-1003919341801:1695` | active (Sophia parked, GO-ready; supersedes thread 3) |
| 2026-06-08 | Capoeira dao-client swap (PR2) | `CAPOEIRA_DAO_CLIENT_SWAP_PLAN.md` | [topic](https://t.me/c/3919341801/1658) | 1658 | `tg:-1003919341801:1658` | active |
| 2026-06-08 | Oracle CDN re-wire (@truesight_dao/dao-client) | `ORACLE_CDN_REWIRE_PLAN.md` | [topic](https://t.me/c/3919341801/1638) | 1638 | `tg:-1003919341801:1638` | active |
| 2026-06-08 | Resend verification email | `RESEND_VERIFICATION_PLAN.md` | [topic](https://t.me/c/3919341801/1504) | 1504 | `tg:-1003919341801:1504` | active |
| 2026-06-07 | THEOBROMA-1 (cacao brew, demo) | `SANDBOX_THEOBROMA_1_HANDOFF_DEMO.md` | [THEOBROMA-1](https://t.me/c/3919341801/1401) | 1401 | `tg:-1003919341801:1401` | demo · live |
