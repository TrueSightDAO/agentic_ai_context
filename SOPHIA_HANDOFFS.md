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
replying in that topic with a short go-signal —
…

## Registry

| Plan file | Handoff title | Telegram topic | message_thread_id | Handoff date | Status |
|-----------|---------------|----------------|-------------------|--------------|--------|
| `sentiment_importer/LARGE_SPIKE_INDEX_EXECUTION_ROADMAP.md` (repo: TrueSightDAO/sentiment_importer) | Large Spike Index (`/large_spikes`) — bullish/momentum mirror of the sell-off index | [Large Spike Index](https://t.me/c/3919341801/8297) | 8297 | 2026-07-02 | parked GO-ready — roadmap merged to sentiment_importer `master` (PR #1098); §5a one PR per turn; RESUME HERE = **PR1** (migration `add large_spike` + `mark_large_spikes`, `gate: eyeball predicate`); own-repo — opens PRs only, never self-merges |
| `MEMBERS_PAGE_SINGLE_SOURCE_PLAN.md` | Members page reliability + single-source consolidation | [Members page single-source](https://t.me/c/3919341801/8185) | 8185 | 2026-07-01 | parked GO-ready — §5a one PR per turn; RESUME HERE = **PR1** (lineage-credentials cron 6h→2h); PR2 gate = `LINEAGE_DISPATCH_PAT` secret; PR4 gate = beta→prod human promotion; cross-repo — opens PRs only, never self-merges |
| `POST_REPACKAGING_CLEANUP_PLAN.md` | Post-Repackaging Cleanup: Auto-populate Currencies + offchain after repackaging GAS | [Post-Repackaging Cleanup](https://t.me/c/3919341801/7987) | 7987 | 2026-06-28 | parked GO-ready — RESUME HERE = **PR1** (`modules/post_repackaging_cleanup.py`); own-repo gate |
| `SOPHIA_DURABLE_JOURNAL_RESUME_PLAN.md` | Sophia Durable Journal + Checkpoint-Resume Loop | _draft — not parked_ | _TBD_ | 2026-06-23 | draft — awaiting governor review; RESUME HERE = **PR1** (`app/journal.py`); own-repo gate |
| `QR_SELF_SERVE_CURRENCY_PLAN.md` | Self-Serve QR-Ready Currency Definition via Edgar | [QR Self-Serve Currency](https://t.me/c/3919341801/7611) | 7611 | 2026-06-23 | parked GO-ready — RESUME HERE = **PR1** (`dao_protocol`: define-currency CLI + dispatch route); §5a one PR per turn; opens PRs only, never self-merges |
| `SOPHIA_CONTRIBUTION_SCORING_PLAN.md` | Score contribution review backlog | _(register on GO)_ | — | 2026-06-23 | draft — awaiting governor §10 + GO |
| `SCORING_REVIEW_QUEUE_PLAN.md` | Scoring Review Queue (DApp review → GAS write-back → main ledger) | [Scoring Review Queue](https://t.me/c/3919341801/7191) | 7191 | 2026-06-28 | completed — PR-INTEGRATION fixed, queue processed (~475 approvals), SENTINEL section on members.html live, review SOP at REVIEW_QUEUE_SOP.md |
| `SOPHIA_DAPP_EVENT_ALIGNMENT_PLAN.md` | DApp Event Alignment (all event types) | [DApp Event Alignment](https://t.me/c/3919341801/6416) | 6416 | 2026-06-18 | parked GO-ready |
| `CLI_SALES_EVENT_ALIGNMENT_PLAN.md` | CLI Sales Event Audit & Alignment with DApp | [CLI Sales Event Alignment](https://t.me/c/3919341801/6311) | 6311 | 2026-06-17 | in progress |
| `PUBLIC_KEY_LOOKUP_CACHE_PLAN.md` | Public-Key Lookup Cache | [Public-Key Lookup Cache](https://t.me/c/3919341801/5712) | 5712 | 2026-06-16 | blocked |
| `SOPHIA_VAULT_CREDENTIAL_MIGRATION_PLAN.md` | Vault Initialization & Credential Migration | [Vault Init & Credential Migration](https://t.me/c/3919341801/3981) | 3981 | 2026-06-14 | blocked |
| `SOPHIA_LIVE_PROGRESS_PLAN.md` | Live Progress Introspection | [Live Progress Introspection](https://t.me/c/3919341801/2799) | 2799 | 2026-06-11 | blocked |
| `SOPHIA_MULTI_TENANT_GOVERNANCE_PLAN.md` | Multi-Tenant Governance & Vault — Phase 0 | [Multi-Tenant Governance — Phase 0](https://t.me/c/3919341801/2744) | 2744 | 2026-06-11 | blocked |
| `SOPHIA_FOLLOWUP_MONITOR_PLAN.md` | Durable Follow-up Monitor | [Follow-up Monitor](https://t.me/c/3919341801/2622) | 2622 | 2026-06-11 | in progress |
| `AUTOPILOT_HARDENING_PLAN.md` | Autopilot Hardening | [Autopilot Hardening](https://t.me/c/3919341801/2317) | 2317 | 2026-06-10 | blocked |
| `BETA_SANDBOX_ENDPOINT_PLAN.md` | Beta Sandbox Endpoint | [Beta Sandbox Endpoint](https://t.me/c/3919341801/1955) | 1955 | 2026-06-09 | blocked |
| `CHOCOLATE_SUBSCRIPTION_PLAN.md` | Agroverse Chocolate Subscriptions — Phase 1 | [Chocolate Subscriptions — Phase 1](https://t.me/c/3919341801/1939) | 1939 | 2026-06-09 | blocked |
| `RESEND_VERIFICATION_PLAN.md` | Resend verification email | [Resend Verification](https://t.me/c/3919341801/2622) | 2622 | 2026-06-08 | in progress |
| `SANDBOX_THEOBROMA_1_HANDOFF_DEMO.md` | THEOBROMA-1 (cacao brew demo) | [THEOBROMA-1 Demo](https://t.me/c/3919341801/2622) | 2622 | 2026-06-07 | demo · live |
