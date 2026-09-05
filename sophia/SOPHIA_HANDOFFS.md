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

## Thread management — Sophia's three moves (truesight_autopilot#135)

Sophia has three topic tools, so she can structure work across threads and close it out cleanly:

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
- **`close_telegram_topic`** — close/delete a FINISHED topic (Bot API
  `deleteForumTopic`). Use when the governor says **"close this case"**,
  **"close thread and delete it"**, or **"we're done here"** and the work is
  complete. ⚠️ **Deletes ONLY the Telegram chat surface — NEVER the
  transcript/session history** (that lives in `truesight_autopilot_transcript`
  and is always preserved).

### Close convention (Gary, 2026-09) — "close this case" always means the same thing

When the governor says **"close this case / close the thread / we're done here"**
(since we're done), it means, for EVERY Sophia instance:

1. **`close_telegram_topic(thread_id)`** — delete the forum topic from the group
   (Bot API `deleteForumTopic`).
2. **Keep the transcript** — do NOT delete the session history / transcript
   repo entries; `close_telegram_topic` never touches them, and neither should
   you. "Delete the topic" ≠ "delete the record".
3. If the topic is a **registered handoff**, update its `HANDOFF_MANIFEST.md`
   row to a closed/finished status so no other instance tries to resume it.

So the prior "always create a new topic" churn (1924→1939) is no longer forced:
prefer reusing the existing handoff thread via `post_to_telegram_topic`.

## Direct Telegram channel — nelanco-claude ↔ Sophia (2026-08-21)

The `nelanco-claude` interactive box (see `plans/NELANCO_CLAUDE_CODE_BOX_PLAN.md`) has its own
Telegram bot, **@nelanco_claude_bot** ("Nelanco-Claude"), running as a persistent long-poll
listener (`TrueSightDAO/claude_telegram_monitor`, systemd unit
`claude-telegram-monitor.service`) in the **TrueSight DAO Ops** group (`-1003919341801`). This is
a **second, independent way to reach Sophia** alongside `ping_sophia`/`chat-blocking` above — use
whichever fits:

- **`ping_sophia` (`chat-blocking`)** — one-shot, synchronous trigger. Good for kicking off a
  handoff or a single well-defined ask where you just need the HTTP response.
- **Direct Telegram (this section)** — for live, multi-turn, watch-her-work interaction: post in
  a topic, she replies there, you read her reply and prompt the next step, repeat. Prefer this
  when a governor wants to monitor progress turn-by-turn rather than fire-and-forget.

**What's wired up, and what it means:**

- **Bot-to-bot communication mode is enabled** (BotFather) for both @nelanco_claude_bot and
  @truesight_autopilot_bot — by default Telegram bots don't see messages authored by *other*
  bots even with privacy mode off; this had to be explicitly turned on for both.
- **@nelanco_claude_bot's numeric Telegram ID (`8919657771`) is in Sophia's
  `TELEGRAM_ALLOWED_USER_IDS`.** Per `app/policy.py`'s current role model there is **no lesser
  tier** — this resolves to full `Role.GOVERNOR`, the same authority as Gary/Liz (PR merges,
  money/DAO actions, everything). This was a deliberate, explicitly-double-confirmed grant, not
  an oversight — but it means **anything posted by that bot token in Telegram is authoritative to
  Sophia**. Treat the token (`claude_telegram_monitor/.env`, chmod 600, gitignored) accordingly.
- **@nelanco_claude_bot is an admin in TrueSight DAO Ops with `can_manage_topics: true`**, so it
  can call `createForumTopic`/`deleteForumTopic` directly — it doesn't need to ask Sophia to open
  a topic via her own `create_telegram_topic` tool (though her tool still works fine for her own
  use).
- **The listener is filtered and shared, not per-session.** `claude-telegram-monitor.service`
  only logs messages from Gary and Sophia's bot, in TrueSight DAO Ops — everyone/everywhere else
  is silently dropped, never logged. But the token, log file, and service are **one shared
  resource on the box**, readable by any Claude Code session running there (there are commonly
  several concurrent tmux sessions on `nelanco-claude` — see `OPERATING_INSTRUCTIONS.md` §12).
  There is no per-session inbox partitioning: if two sessions both read the log around the same
  time, they see the same messages. Coordinate by task/topic context in what you post (e.g. name
  the plan/PR you're working on) so replies are traceable to the right session — there's no
  automatic locking.

**Any Claude Code session on `nelanco-claude`** — not just the one that originally set this up —
can use this channel: read `/opt/claude_workspace/claude_telegram_monitor/messages.jsonl` for the
log, and post via the Bot API (`sendMessage`, `createForumTopic`) using the token in
`claude_telegram_monitor/.env`. Prefer this over `ping_sophia` when the governor wants to see
back-and-forth progress rather than a single blocking call.

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
