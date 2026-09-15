# Supervisor Loop — directive for LLMs supervising Sophia

**Audience:** any LLM acting as a *supervisor* over Sophia (DeepSeek Local, Envoy, or a fresh
local LLM). A supervisor is a **human-driven LLM** (not the autonomous autopilot) that keeps
Sophia moving through a handoff until the work is **ready for human UAT** — so the governor only
has to appear at the truly human-only gates, not prompt every step.

**Read this once before supervising.** For the trigger mechanics (ping template, GO convention,
thread rules) see `sophia/SOPHIA_HANDOFFS.md`; for the big-picture actor map see
`handoffs/HANDOFF_PROTOCOL_OVERVIEW.md`; for the live registry see `handoffs/HANDOFF_MANIFEST.md`.

---

## 1. The loop (core)

```
refresh context (git pull agentic_ai_context) → read the unfinished-work index (§2)
  → select the next thread(s) within the WIP limit (§3)
  → for each selected thread, supervise to a stop (§4/§5):
        read state → act (prompt / clear gate / escalate) → verify (R1/R2 UAT)
        → repeat until the thread is human-UAT-thumbs-up → prod merged → done, or escalated
  → checkpoint your own position (§7)
  → loop
```

A supervisor's job is to **drive threads through R1/R2 UAT to `human_uat_ready`**, then through the
human thumbs-up to `prod_merge` and `done` — never to spin idly on a thread that is running, and
never to fan out to every thread at once.

---

## 2. Reading state — the unfinished-work index

The supervisor's queue is **`handoffs/HANDOFF_MANIFEST.md`** (human-facing) backed by a
**machine-readable `handoffs/index.json`** (supervisor-facing; see §8 "enabling work" if it
doesn't exist yet). Every unfinished handoff has a **state** from this enum:

| State | Meaning | Supervisor action |
|---|---|---|
| `awaiting_kickoff` | Plan written + row registered; not yet triggered | Dispatch (§5) |
| `executing` | Sophia is running a turn | **Wait** (poll; do not re-ping) |
| `paused_at_gate` | Sophia stopped at a gate | Clear it (if autonomous) or escalate (§5) |
| `sophia_uat` | R1 — Sophia verifying her own work on beta | Drive to pass (§4) |
| `envoy_uat` | R2 — Envoy independently verifying on beta | Ask Envoy, drive to pass (§4) |
| `human_uat_ready` | R1+R2 green; request human UAT | **Request human UAT** (§4) |
| `prod_merge` | Human gave thumbs-up; execute the prod merge | Merge to prod (§4/§5) |
| `blocked_on_human` | Needs a human-only action (money/secret/org) | **Escalate** |
| `failed` | Turn errored / no PR opened | Diagnose → retry once → escalate |
| `done` | All units merged, contribution reported, channel closed | Confirm closure (§6a) |
| `stale` | No activity in N hours (default 24) | Flag; do **not** auto-ping |

**How to read a thread's live state (Telegram + Discord):**

- **Telegram:** read the topic's latest messages from the supervisor's monitor log —
  DeepSeek Local reads `~/Applications/deepseek_telegram_monitor/messages.jsonl`; Envoy reads
  `/opt/claude_workspace/claude_telegram_monitor/messages.jsonl`. Or ask Sophia directly:
  `truesight-dao-ping-sophia --session-id tg:-1003919341801:<thread_id> --message "where are we on <plan>?"`.
- **Discord:** read the channel/thread state via the Discord adapter; Sophia's own reports land
  in the same channel she was dispatched in.

**Before trusting any local copy, `git pull`** the context repo — a plan or manifest row may have
been committed since your clone was last refreshed (`SOPHIA_HANDOFFS.md` §"Pull-first rule").

---

## 3. Bounded WIP — do not flood Sophia or yourself

- **WIP limit: 2 threads** supervised concurrently (default). Drive each to a human gate or
  completion **before** selecting the next. Never broadcast `go` to every unfinished thread.
- **Priority order** when selecting: `paused_at_gate` (cheap unblock) > `failed` (diagnose) >
  `executing` (monitor) > `awaiting_kickoff` (dispatch). Prefer the most-advanced thread.
- **One outstanding directive per thread, max — across ALL concurrent supervisors, not just your
  own loop.** Before prompting, check the thread's last message: if Sophia already has an
  unanswered `go` or is mid-turn (from *any* supervisor — another Envoy tmux session, DeepSeek
  Local, or a prior iteration of your own loop), **do not re-ping** — re-pinging a running turn
  stalls or duplicates work. Multiple Envoy tmux sessions on `nelanco-claude` commonly run this
  loop at once (see `ENVOY.md` point 7); read live state before selecting a thread rather than
  assuming you're the only supervisor watching it.
- **Respect Sophia's own guards** — she already has per-thread `_thread_dispatch_locks`
  (Telegram) / `_channel_dispatch_lock` (Discord, #456) and `AUTO_ADVANCE_MAX_TURNS=8`. The WIP
  limit is *on top of* those: it caps Sophia's **total concurrent load** (and the GitHub write PAT,
  see `plans/SOPHIA_GITHUB_RATE_LIMIT_GOVERNOR_PLAN.md`), not just per-thread.

---

## 4. UAT — three rounds, then prod merge

UAT is **three rounds**, all in the **beta** environment, then prod:

| Round | Who | What | Loop behavior |
|---|---|---|---|
| **R1 — Sophia UAT** | Sophia (autopilot) | Run the plan's U1–Un acceptance steps on **beta**; verify each pass/fail; fix and re-verify until green | **Autonomous** — supervisor drives |
| **R2 — Envoy UAT** | Envoy (independent Claude seat) | Independently re-run the acceptance steps on **beta**; report pass/fail | **Autonomous** — supervisor asks Envoy |
| **R3 — Human UAT** | Governor | Final sign-off on the acceptance criteria (eyes on the real surface) | **Always-stop** — supervisor requests |
| **Prod merge** | Supervisor / Sophia | After human UAT **thumbs-up**, execute the merge to prod (`sync_beta_to_prod` / default-branch merge) | **Authorized by human thumbs-up** |

The loop's exit is the human **thumbs-up**, then the prod merge. Each round posts a short pass/fail
summary to the thread so the next round starts from a verified baseline. A pure backend/library
change with no human-facing surface may skip R1/R2 (state "covered by automated tests") but **still
waits for human UAT before prod**.

---

## 5. Authority envelope — what the supervisor may do autonomously

> **Governor decision 2026-09-14 (3-round UAT):** prod merge/promote is **not** autonomous on its
> own — it is **authorized by the human UAT thumbs-up** (§4 R3). The supervisor executes the merge
> only after that thumbs-up. A supervisor must NOT exceed this envelope, and must NOT re-interpret
> it on the fly (§5e of `OPERATING_INSTRUCTIONS.md`: batch the scoping decision once, don't re-ask
> per occurrence).

| Action | Default | Basis |
|---|---|---|
| Send `go` for a non-irreversible unit | **Autonomous** | §5c — safe units auto-advance |
| Diagnose + retry a `failed` turn (once) | **Autonomous** | §5c — non-convergence halts, but the supervisor may re-drive |
| R1 (Sophia) + R2 (Envoy) UAT on beta | **Autonomous** | §4 |
| Merge a PR to a **non-prod** repo / feature branch (CI green + R1/R2 UAT pass) | **Autonomous** | beta repos are not outward-facing |
| Merge a PR to a **prod-consumed** repo / default branch | **Gated on human UAT thumbs-up** | supervisor executes after §4 R3 thumbs-up |
| Beta→prod promote (`sync_beta_to_prod`) | **Gated on human UAT thumbs-up** | supervisor executes after §4 R3 thumbs-up |
| TDG / money movement (issuing, payouts, treasury, capital injection, batch contributions) | **Human (always)** | §5c — non-negotiable |
| Account-only actions (secrets, tokens, npm publish, org/SSO, domain/DNS) | **Human (always)** | §5c — non-negotiable |
| Final human UAT sign-off | **Human (always)** | §4 |

**Overrides:** a plan may tighten this (an explicit `gate: human` marker always wins) but may not
loosen it. A plan with an explicit `gate: human` on its prod/deploy/merge unit still stops and
escalates even under this envelope — always-stop markers win over the standing autonomy here.

---

## 6. Failure & safety

- **Never silently drop a thread.** Every stop (gate, failure, human handoff) must end with a
  message in the thread stating state + next step + who owns it.
- **Failed turn:** read the error, fix if it's clearly in scope, retry **once**, then escalate
  with the error and prior PR links (§5c — a broken turn never auto-advances).
- **Ambiguity fails closed.** If you can't tell *where* the thread is, stop and ask the governor —
  don't guess and send `go`.
- **Money/identity gates are never clearable** by a supervisor regardless of any other wording.

---

## 6a. Close-out — deleting a task-scoped channel (governor directive, 2026-09-14)

**A chat surface created for one specific piece of work — a Telegram forum topic or a Discord
channel opened to run a single handoff — gets deleted once that work is truly finished.** A
supervisor's responsibility for a thread does **not** end at "units merged" or even at "human
UAT thumbs-up" — it ends only after this close-out sequence completes, in order:

1. **Prod merge / promote lands** (§4 Prod merge row) and is confirmed healthy.
2. **The DAO contribution report is filed** (`truesight-dao-report-ai-agent-contribution`,
   `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`) — **never skip or defer this step.** It's the durable
   record of the work; the channel is not.
3. **Only then** does Sophia close and delete the channel/topic.

**Never delete before step 2.** If the channel disappears before the contribution is filed, the
supervisor loses the PR links and context needed to file it correctly — don't create that gap.

**Mechanics differ by venue:**

- **Telegram:** Sophia has `close_telegram_topic_checked` (preferred — verifies the handoff's
  registered state first) / `close_telegram_topic` (`app/tools/telegram_topic.py`). This deletes
  **only** the Telegram chat surface — it never deletes the underlying session transcript/history,
  which stays queryable. See `sophia/SOPHIA_HANDOFFS.md`.
- **Discord:** Sophia has `delete_discord_channel` (`app/tools/discord_admin.py`) — governor-only
  (`default_roles={"governor"}`), requires **both** `dry_run=false` **and** `confirm=true` (two
  deliberate flags for an irreversible action). Prefer a dry-run first to confirm the target
  channel id via `list_discord_channels`. The tool's own docstring nudges toward
  `update_discord_channel` (rename + move to an archive category) as the reversible alternative —
  but per this directive, a genuinely finished task-scoped channel gets hard-deleted, not archived,
  once steps 1–2 above are done.

**Mandatory: name the channel before it's gone.** The final closing message — posted in the
parent chat/log, not just the doomed channel itself — must explicitly name the channel/topic
being deleted, so there's a durable record of what existed even after the surface is gone. If
Sophia's close-out message doesn't include the name, the supervisor asks for it before letting
the deletion stand as complete.

**Applies only to task-scoped surfaces** (one handoff, one channel) — not to standing/general
channels (e.g. a team's always-on Discord channel), which are never auto-deleted by this rule.

---

## 7. Checkpoint & resume (the supervisor's own state)

A supervisor is itself session-scoped and can be interrupted. Between threads, persist your
position so a fresh supervisor session resumes without re-reading every thread:

- Write a short `notes/supervisor_loop_<date>.md` (or update the supervisor's own row in the
  index) recording: which thread(s) you're supervising, their state, and your next action.
- Keep it tiny — a line per thread. This is the supervisor's analogue of Sophia's context
  compaction: bound your own context, don't re-derive the world each session.

---

## 8. Enabling work (not yet shipped)

The loop is followable today against `HANDOFF_MANIFEST.md`, but two pieces make it clean:

1. **`handoffs/index.json`** — a generated, machine-readable mirror of the manifest with the §2
   state enum, both Telegram `thread_id` **and** Discord channel/thread id, and a `last_updated`
   timestamp. Emit/validate it by extending `scripts/validate_handoff_manifest.py`.
2. **A read-order reference** — add this file to the `OPERATING_INSTRUCTIONS.md` §2 table so
   every supervisor LLM finds it (canonical file — raise as a suggested update, don't edit it).

These are follow-on work items, not prerequisites to supervising with this directive today.

---

*Last updated 2026-09-14. If the authority envelope or WIP limit changes, update this file
directly — it is not on the do-not-edit list in `OPERATING_INSTRUCTIONS.md` §3.*
