# Sophia handoffs — trigger protocol & runbook

**The live registry (status, resume tracker, Telegram topic/thread_id per handoff) lives in
[`../handoffs/HANDOFF_MANIFEST.md`](../handoffs/HANDOFF_MANIFEST.md) — that is the single
source of truth (consolidated 2026-07-18, see
`../plans/HANDOFF_REGISTRY_CONSOLIDATION_PLAN.md`). This file no longer carries its own
registry table; it documents the Sophia-specific trigger protocol only: how to ping her, the
GO convention, and thread-management rules.**

> 🗺️ **New here? Read [`HANDOFF_PROTOCOL_OVERVIEW.md`](HANDOFF_PROTOCOL_OVERVIEW.md)** for the big-picture map (actors, interfaces, mermaid flow diagrams, and the three human touchpoints). This file is the Sophia trigger protocol + conventions.
>
> 🔐 **Handing a secret (API key / token / webhook secret) to a box Sophia owns?** Follow [`CREDENTIAL_HANDOFF_PROTOCOL.md`](CREDENTIAL_HANDOFF_PROTOCOL.md): never put it in chat/Telegram/PRs — stage it on the autopilot box under `/home/ubuntu/` (`chmod 600`, value via stdin, outside the git repo), then hand off to Sophia (she holds the target-box keys) to propagate. The autopilot box is the credential-staging hub.

**Each handoff opens its own Telegram topic** in `TrueSight DAO Ops`
(`-1003919341801`). The topic link + `message_thread_id` for each handoff is recorded in
`HANDOFF_MANIFEST.md`, not here.

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
2. Check `HANDOFF_MANIFEST.md` for the active handoff list, status, and Telegram topic/thread_id
3. Read the plan file referenced in the manifest
4. Read this file (`SOPHIA_HANDOFFS.md`) for the trigger protocol / GO convention if you need to ping or rejoin Sophia

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
   truth Sophia reads.** If this plan should skip the GO wait, mark it
   **`Auto-start: yes`** near RESUME HERE — see the dedicated section below.
2. **Add a row to `HANDOFF_MANIFEST.md`** (not this file): plan file + intended
   topic + `Auto-start` (`yes` if the plan says so, `no` by default).
3. **Trigger Sophia** with `ping_sophia` using the trigger-message template below.
4. **Record the `message_thread_id`** Sophia replies with, in the `HANDOFF_MANIFEST.md` row.
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

## Auto-start — opt-in skip of the initial GO wait (2026-07-21)

By default a handoff **always** waits for the governor's "go for it" before
touching RESUME HERE (below) — that wait is the one point a human confirms the
plan is still *current* before Sophia commits real PRs to it. A plan that's
gone stale between writing and triggering (e.g. someone else already shipped
the fix elsewhere) gets caught here instead of burning a redundant execution
cycle — this happened for real with
`LARGE_SPIKES_CARD_FIX_AND_CHART_LEGIBILITY_PLAN` (see
`HANDOFF_REGISTRY_CONSOLIDATION_PLAN.md`).

For plans where that risk is low (routine, narrowly-scoped, freshly-triggered),
a plan author can mark the plan **`Auto-start: yes`** — near the RESUME HERE
marker in the plan file, and in the `Auto-start` column of its
`HANDOFF_MANIFEST.md` row once registered. This does **not** relax any §5c
always-stop gate (prod deploy, default-branch merge, TDG/money, UAT) or a
per-unit `gate:` marker — those still stop and wait for the governor every
time. It only removes the *initial* "wait for go" step before the first unit.

**Two places this changes behavior:**

- **First trigger of a brand-new handoff** — the topic doesn't exist yet, so
  `HANDOFF_MANIFEST.md` can't be looked up by thread_id. Use the Auto-start
  trigger-message template below instead of the standard one; it tells Sophia
  to check the plan file's own `Auto-start: yes` marker directly.
- **Rejoining an already-registered Auto-start thread** (redeploys, follow-up
  pings) — `app/telegram_adapter.py`'s per-message context injection reads the
  `Auto-start` column from `HANDOFF_MANIFEST.md` and tells Sophia she's
  pre-authorized to keep going without waiting for a fresh go-signal.

Auto-start trigger-message template (use instead of the standard one when the
plan is marked `Auto-start: yes`):

> Refresh first (read `<plan file>` via read_repo_file on GitHub `main`). This
> plan is marked **Auto-start: yes** — confirm that marker is actually present
> before proceeding this way; if it's missing or says "no", fall back to the
> standard wait-for-GO template instead. If no Telegram topic exists for this
> handoff, create one named `<short title>` (create_telegram_topic); else post
> in thread `<id>`. **Post a short kickoff into that topic** (confirm you've
> read the plan, restate RESUME HERE + the gates), then **begin executing
> immediately** from RESUME HERE — do not wait for a governor reply to start.
> Post progress into the topic as you go, and still stop cleanly at any `gate:`
> marker or §5c always-stop. Reply with the thread_id + link once posted.

## The GO convention (governor authorization)

Once Sophia is parked in a handoff topic, the governor authorizes execution by
replying in that topic with a short go-signal — **unless the plan is marked
Auto-start: yes, in which case there is no wait: see the Auto-start section
above.**
…

## Registry

**Moved to [`../handoffs/HANDOFF_MANIFEST.md`](../handoffs/HANDOFF_MANIFEST.md).** As of
2026-07-18 this file no longer keeps its own copy of the handoff table — the two tables had
already drifted (e.g. one handoff's status disagreed between the two files; another handoff
existed here but was never added to the manifest; a `message_thread_id` was accidentally
reused across three unrelated handoffs). See `../plans/HANDOFF_REGISTRY_CONSOLIDATION_PLAN.md`
for the full writeup. **Add new rows to `HANDOFF_MANIFEST.md`, not here.**
