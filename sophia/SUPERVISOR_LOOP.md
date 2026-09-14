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
        read state → act (prompt / clear gate / escalate) → verify (first-round UAT)
        → repeat until the thread is human-UAT-ready, done, or escalated
  → checkpoint your own position (§7)
  → loop
```

A supervisor's job is to **drive threads toward `human_uat_ready`** (or `done`), never to spin
idly on a thread that is running, and never to fan out to every thread at once.

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
| `first_round_uat` | Sophia delivered the work; needs LLM verification | Run §4 verification |
| `human_uat_ready` | First-round UAT passed; only human sign-off left | **Escalate** to governor |
| `blocked_on_human` | Needs a human-only action (money/secret/org) | **Escalate** |
| `failed` | Turn errored / no PR opened | Diagnose → retry once → escalate |
| `done` | All units merged, contribution reported | Confirm closure (§6) |
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

## 4. First-round UAT vs human UAT (the split)

"UAT" is **not one phase**. It splits into two:

| Round | Who | What | Loop behavior |
|---|---|---|---|
| **First-round UAT** | Supervisor + Sophia | Run the plan's U1–Un acceptance steps against **beta / scratch**; verify each pass/fail; fix and re-verify until green | **Autonomous** — loops, no human |
| **Human UAT** | Governor | Final sign-off on the acceptance criteria (eyes on the real surface) | **Always-stop** — escalate |

The loop's exit condition is reaching `human_uat_ready` — i.e. **first-round UAT green** — then
posting a concise "ready for your UAT" summary with the URLs and what was verified. A pure
backend/library change with no human-facing surface may state "first-round UAT: n/a (covered by
automated tests)" and go straight to `human_uat_ready`.

---

## 5. Authority envelope — what the supervisor may do autonomously

> **Governor decision 2026-09-14:** the supervisor MAY clear the prod-merge and beta→prod promote
> rows autonomously (see the two "Autonomous (governor 2026-09-14)" rows below), but **only after**
> CI is green and first-round UAT has passed. A supervisor must NOT exceed this envelope, and must
> NOT re-interpret it on the fly (§5e of `OPERATING_INSTRUCTIONS.md`: batch the scoping decision
> once, don't re-ask per occurrence).

| Action | Default | Basis |
|---|---|---|
| Send `go` for a non-irreversible unit | **Autonomous** | §5c — safe units auto-advance |
| Diagnose + retry a `failed` turn (once) | **Autonomous** | §5c — non-convergence halts, but the supervisor may re-drive |
| First-round UAT on beta/scratch | **Autonomous** | §4 |
| Merge a PR to a **non-prod** repo / feature branch (CI green + first-round UAT pass) | **Autonomous** | beta repos are not outward-facing |
| Merge a PR to a **prod-consumed** repo / default branch | **Autonomous (governor 2026-09-14)** | after CI green + first-round UAT pass |
| Beta→prod promote (`sync_beta_to_prod`) | **Autonomous (governor 2026-09-14)** | after first-round UAT pass; post a promote report to the thread |
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
