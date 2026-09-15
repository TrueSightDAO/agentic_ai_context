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
| `executing` | Sophia is running a turn | **Wait** (poll; do not re-ping) — but see §2a if the wait is prolonged |
| `paused_at_gate` | Sophia stopped at a gate | Clear it (if autonomous) or escalate (§5) |
| `sophia_uat` | R1 — Sophia verifying her own work on beta | Drive to pass (§4) |
| `envoy_uat` | R2 — Envoy independently verifying on beta | Ask Envoy, drive to pass (§4) |
| `human_uat_ready` | R1+R2 green; request human UAT | **Request human UAT** (§4) |
| `prod_merge` | Human gave thumbs-up; execute the prod merge | Merge to prod (§4/§5) |
| `blocked_on_human` | Needs a human-only action (money/secret/org) | **Escalate** |
| `failed` | Turn errored / no PR opened | Diagnose → retry once → escalate |
| `done` | All units genuinely merged (independently verified — §6) + contribution reported | Confirm closure (§6) |
| `stale` | No activity in N hours (default 24) | Flag; do **not** auto-ping |

### 2a. Long `executing` stalls — verify the process is actually alive (governor directive, 2026-09-15)

A thread reading `executing` for far longer than a turn should reasonably take is **not
automatically "just slow."** Per `WORKSPACE_CONTEXT.md` §"When a flow appears stuck," most of
this workspace's async chains are legitimately slow at some leg — but a *prolonged* `executing`
read, well past the 45-second evidence-based check cadence (`supervision_requires_reading_not_pinging`
pattern — chat + logs, not a blind timer), earns a deeper check than "wait some more":

1. **Check whether Sophia's process is actually running**, not just whether the manifest/log
   still *says* `executing`: `systemctl status truesight-autopilot` (the brain — turns run here)
   and the relevant adapter unit (`truesight-autopilot-telegram` / `truesight-autopilot-discord`).
   Look at `journalctl -u truesight-autopilot --since <turn start time>` for whether rounds/tool
   calls are still landing, or whether the process **restarted** since this turn began.
2. **The specific failure mode to check for: deploy self-disruption.** Any `deploy_autopilot`
   call — from *any* thread, not just this one — restarts the single shared brain process and
   **silently kills every in-flight turn, including this thread's.** The tell: `NRestarts`
   incremented, or the unit's start time is *newer* than this turn's dispatch time, or a
   `Tool ... cancelled by user`-shaped line in the log around the restart. If confirmed, this
   thread will **never resume on its own** — its turn is dead, not slow.
3. **If the process is alive and producing rounds/tool calls for this session**, this is not a
   stall — leave it alone exactly as §3 says: do not re-ping a turn that's actually running.
4. **If a restart killed this thread's turn, the supervisor SHOULD nudge again** — this is a
   deliberate, evidence-backed exception to §3's "do not re-ping a running turn" rule, justified
   specifically because there's concrete proof the original turn is dead, not because time merely
   passed. Nudge with the **grounded context of what was interrupted** (which unit/step, what the
   last completed action was), not a generic "are you stuck?" — and check every other thread you
   or a co-supervisor were tracking for the same restart-shaped gap before assuming only this one
   thread was hit (a shared-process restart interrupts everyone at once).

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
  own loop.** The **primary check is structural, not inferred** — read `handoffs/active_supervision.json` (shown as the 👀 badge on `sprint.truesight.me`), where every supervisor records a live claim the moment it starts driving a thread. If another supervisor holds a **fresh** claim on it, the thread is already being driven — **do not re-ping**. Only fall back to the weaker inference below when there is no claim. Before prompting, check the thread's last message: if Sophia already has an
  unanswered `go` or is mid-turn (from *any* supervisor — another Envoy tmux session, DeepSeek
  Local, or a prior iteration of your own loop), **do not re-ping** — re-pinging a running turn
  stalls or duplicates work. Multiple Envoy tmux sessions on `nelanco-claude` commonly run this
  loop at once (see `ENVOY.md` point 7); read live state before selecting a thread rather than
  assuming you're the only supervisor watching it. **Exception:** §2a — a prolonged `executing`
  read backed by process-level evidence that the turn actually died (a deploy restart, most
  commonly) is not "a running turn," and re-pinging it is the correct action, not a violation of
  this rule.
- **Respect Sophia's own guards** — she already has per-thread `_thread_dispatch_locks`
  (Telegram) / `_channel_dispatch_lock` (Discord, #456) and `AUTO_ADVANCE_MAX_TURNS=8`. The WIP
  limit is *on top of* those: it caps Sophia's **total concurrent load** (and the GitHub write PAT,
  see `plans/SOPHIA_GITHUB_RATE_LIMIT_GOVERNOR_PLAN.md`), not just per-thread.

---

### 3a. Board priority signals are advisory — never an automatic override (Gary, 2026-09-15)

`sprint.truesight.me` — the public Kanban board over `handoffs/index.json` — is a **read-only view**:
no write action, and no priority data structure of any kind. A visitor who thinks a ticket deserves
attention clicks through to its live Telegram/Discord thread and says so *in the conversation*, the same
way every other instruction reaches Sophia/Envoy today.

That chat message is **context to weigh** alongside everything §3 already considers when selecting the
next thread — it is **not** a queue reorder, a state change, or an override of the priority order above.
Clicking "this matters" on the board changes nothing mechanically; it just gives the supervisor one more
input for its own judgment. Recorded here as canonical (per `plans/SPRINT_TRUESIGHT_ME_BOARD_PROPOSAL.md`
§2.4) so "a chat message isn't an automatic override" is a documented rule, not just remembered from the
conversation that produced the board.

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

### 5.0 The standing principle (Gary, 2026-09-15 — this should be read as general, not a one-off)

*"Since Sophia now has a supervisor, [merging] shouldn't be human gated... this should be global."*
Gary confirmed this is a **principle**, not a scope expansion to more repos — the table below's
prod-repo merge behavior is unchanged (still gated on human UAT thumbs-up, not on a separate merge
ask) — write it once, apply it consistently to future cases, rather than re-litigating "does
supervision cover this?" from scratch each time:

- **Supervision substitutes for a human gate on actions that are reversible and verifiable after
  the fact.** A bad merge can be reverted, re-diagnosed, and fixed in a later turn — a supervisor
  (Envoy, DeepSeek Local, or Sophia's own R1 self-check) catching a mistake days or minutes later
  still fully closes the loop. That's why merging — to `truesight_autopilot` or any non-prod
  repo — no longer needs a human specifically: the supervisor *is* the check.
- **Supervision does NOT substitute for a human gate on actions that are irreversible, carry
  external/financial/legal weight, or require a judgment only a human can make.** A supervisor
  catching a mistake *after* a TDG issuance, a domain/DNS change, a GAS deploy that broke a live
  spreadsheet integration, or a prod website merge that shipped a broken checkout to real
  customers — doesn't undo the mistake, and in the prod-website case specifically, human UAT isn't
  really a check on *Sophia's code quality* (which supervision does cover) so much as it's a human
  confirming the actual *customer-facing outcome* is right, a class of judgment supervision cannot
  stand in for. That's why GAS deployment, human UAT, TDG/money movement, account-only actions,
  and (per §5e below) prod-website merge/promote (which is gated *by* UAT, not separately) all stay
  human-always regardless of how good supervision gets.
- **Apply this test to any future case, not just the ones already enumerated below**: is the
  action reversible and will a supervisor's after-the-fact review genuinely catch and fix a
  mistake? Then it can be autonomous. Does getting it wrong cause external/irreversible harm, or
  require a judgment call only a human is positioned to make? Then it stays gated, no matter how
  much supervision exists.

> **Governor decision 2026-09-14 (3-round UAT):** prod merge/promote is **not** autonomous on its
> own — it is **authorized by the human UAT thumbs-up** (§4 R3). The supervisor executes the merge
> only after that thumbs-up. A supervisor must NOT exceed this envelope, and must NOT re-interpret
> it on the fly (§5e of `OPERATING_INSTRUCTIONS.md`: batch the scoping decision once, don't re-ask
> per occurrence).

> **Governor decision 2026-09-15 (merge is not a gate):** *"I don't think merging should be human
> gated. Only deployment of GAS and human UAT. Merge should just be handled by Sophia."* This
> **retires the `truesight_autopilot` own-repo "never self-merge" rule** that had been carried as
> convention text in individual plan-doc headers (`SOPHIA_AUTO_ADVANCE_PLAN.md`,
> `SOPHIA_AUTO_ADVANCE_PR_LESS_UNITS_PLAN.md`, and others) rather than centralized here — Sophia may
> now self-merge PRs to her own codebase, same as any other non-prod repo. **Scoped narrowly, not a
> blanket loosening:** only the git-level *merge* action moves to autonomous.
> - **GAS deployment** (`clasp push`/`deploy`) — still an always-stop, unchanged (§5c).
> - **Human UAT (R3)** — still an always-stop, unchanged (§4).
> - **TDG/money, account-only actions** — untouched; this decision was about merging, not those.
> - **Restarting/deploying `truesight_autopilot`'s own live service** (as opposed to merely merging
>   code to its default branch) is treated here as **still gated**, matching the general
>   deploy/promote always-stop category GAS deploy is one instance of — merging and deploying are
>   different actions, and Gary's statement named deployment (GAS) as a thing that stays gated. This
>   is Envoy's conservative reading of an otherwise-unstated case, not something Gary said
>   explicitly either way — correct it if you intended autopilot's own deploy to be freed too.

| Action | Default | Basis |
|---|---|---|
| Send `go` for a non-irreversible unit | **Autonomous** | §5c — safe units auto-advance |
| Diagnose + retry a `failed` turn (once) | **Autonomous** | §5c — non-convergence halts, but the supervisor may re-drive |
| R1 (Sophia) + R2 (Envoy) UAT on beta | **Autonomous** | §4 |
| Merge a PR to a **non-prod** repo / feature branch (CI green + R1/R2 UAT pass) | **Autonomous** | beta repos are not outward-facing |
| Merge a PR to **`truesight_autopilot`** (Sophia's own codebase) | **Autonomous** (revised 2026-09-15 — previously human-merge-only) | CI green + tests pass; git-level merge only, not a live restart |
| Merge a PR to a **prod-consumed** repo / default branch (e.g. `truesight_me_prod`, `agroverse_shop_prod`, `dapp_prod`) | **Gated on human UAT thumbs-up** | supervisor executes after §4 R3 thumbs-up |
| Beta→prod promote (`sync_beta_to_prod`) | **Gated on human UAT thumbs-up** | supervisor executes after §4 R3 thumbs-up |
| GAS deploy (`clasp push`/`deploy`) | **Human (always)** | §5c — non-negotiable, explicitly reaffirmed 2026-09-15 |
| Restart/deploy `truesight_autopilot`'s own live service | **Gated** (Envoy's conservative default — see callout above) | distinct from merging; verify healthy after, not just that the command ran |
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
- **Verify merge state before accepting "done" / "Plan complete" — a completion claim is not
  evidence (governor directive, 2026-09-15).** Incident: thread 26410 ("Exec: repo-access
  denylist"), 2026-09-14. Sophia's own RESUME HERE named 3 mechanical steps (re-apply a manifest
  edit, merge once CI green, close+delete the topic). One turn correctly reported `merge_pr`
  refused on `agentic_ai_context` PR #1127 (405 — merge conflict) and correctly held off on
  closing the topic. The **next** turn's "actions taken" log showed only a bare link to GitHub's
  REST API reference page for "merge a pull request" — not an actual merge response — yet
  immediately declared **"✅ Plan complete — all units finished."** PR #1127 was never merged
  (confirmed still `OPEN` the next day). The plan was not complete; only the *claim* was made.
  **Rule:** before a supervisor (or Sophia, self-checking) accepts a `done`/"Plan complete"
  declaration, independently verify — for every PR the plan references, not just the
  last-mentioned one — that it is actually merged: `gh pr view <repo> <number> --json
  state,mergedAt` (or the platform-appropriate equivalent) must show `state: "MERGED"` with a
  real `mergedAt` timestamp. Never infer completion from a chat message alone. **A tool result
  that doesn't look like the expected shape — a documentation link instead of a merge response
  body, an empty or malformed payload — is itself evidence the call did NOT execute as claimed;
  treat it exactly like a `failed` turn (diagnose → retry once → escalate), never as silent
  success.** A plan declared "complete" with any unmerged PR is not `done`: correct the manifest's
  Status back to reality, then either finish the merge or escalate — do not proceed to close-out
  (contribution report / topic deletion) until verification actually passes.

---

## 7. Checkpoint & resume (the supervisor's own state)

A supervisor is itself session-scoped and can be interrupted. Between threads, persist your
position so a fresh supervisor session resumes without re-reading every thread:

- **Mechanism of record (PR4b, 2026-09-15): the shared `handoffs/active_supervision.json`.**
  **Claim** a thread by adding an entry (`plan_file`, `supervisor`, `claimed_at`, optional
  `note`) when you start driving it, and **release** it by removing that entry when you stop —
  a small, self-mergeable docs-only PR. It is merged into `handoffs/index.json`'s `supervised_by`
  field and rendered on `sprint.truesight.me`, so a fresh session (or a *different* supervisor)
  sees what's live **before** re-reading any thread. A claim older than ~60 min is surfaced as
  **stale** (`.stale = true`), so an abandoned claim is never silently trusted (mirrors §2a).
- The private notes file is now **optional supplementary context, not the checkpoint of
  record** — keep a short `notes/supervisor_loop_<date>.md` (or the supervisor's own row in the
  index) only for free-text reasoning that doesn't fit the claim's one-line `note` field,
  recording: which thread(s) you're supervising, their state, and your next action.
- Keep it tiny — a line per thread. This is the supervisor's analogue of Sophia's context
  compaction: bound your own context, don't re-derive the world each session.

---

## 8. Enabling work

1. **`handoffs/index.json`** — ✅ **SHIPPED 2026-09-15** (PR #1143 + #1145). A generated,
   machine-readable mirror of the manifest: the §2 state enum, counts by state, both Telegram
   `thread_id` **and** Discord `channel_id`/`thread_id` (columns added to the manifest itself —
   option (a) from the design discussion, not a sidecar file, so the manifest stays the single
   source of truth), and a `last_updated` timestamp. Built by `scripts/build_handoff_index.py`;
   `scripts/validate_handoff_manifest.py --check-index` gates CI so the index can't silently
   drift from the manifest.
2. **A read-order reference** — add this file to the `OPERATING_INSTRUCTIONS.md` §2 table so
   every supervisor LLM finds it (canonical file — raise as a suggested update, don't edit it).
   Still open.

## 9. Keep `handoffs/index.json` current — mandatory, not optional (Gary, 2026-09-15)

Shipping the index once doesn't fix the drift problem — it only fixes it if every supervisor
keeps feeding it. Two standing obligations, both part of the core loop (§1), not a separate task:

1. **Whenever a thread advances to a materially new stage** — whether the supervisor drove it or
   just observed Sophia do it (a PR opens/merges, a deploy lands, a gate clears, UAT starts, a
   thread closes) — update that row's `Status` / `Resume tracker state` / `Last manifest update`
   cells in `HANDOFF_MANIFEST.md` in the same sitting, not as a batched cleanup later. If the
   thread has no row yet (see #2), add one first.
2. **Periodically reconcile the manifest against Sophia's live registry**, not just against what
   a human happened to write a plan for. Sophia's `sessions/_resume_awaiting.json` (Telegram) and
   `_discord_resume_awaiting.json` (Discord) are the ground truth of what she considers open —
   ask her for the current thread/channel IDs directly (a supervisor has no filesystem access to
   her box) and diff against `handoffs/index.json`'s covered set. For each gap: if it's a real,
   still-open unit of work, give it a manifest row (even a minimal one — a `Plan file` cell just
   needs to *contain* `.md` somewhere for `build_handoff_index.py` to count it as handoff-shaped;
   if no real plan doc exists, point it at an existing doc plus an anchor, e.g.
   `OPEN_FOLLOWUPS.md#short-slug`, rather than a bare `—`, which the builder silently excludes);
   if it's already resolved/closed noise, it needs no row. Do not let "no plan file was written"
   be a reason to leave a live, open thread invisible to every other agent.
3. **After any manifest edit, regenerate the index before committing**
   (`python3 scripts/build_handoff_index.py`) — CI's `--check-index` gate will reject a manifest
   change that doesn't, but don't rely on that catching it; run it yourself so the PR is clean on
   the first pass. Also sanity-check the `Status` cell phrasing against the state-rule keywords in
   `build_handoff_index.py` (`STATE_RULES`) — a status like "not yet deployed" can accidentally
   match the `deployed` → `done` rule via substring, so state a still-open gate as
   **"blocked on human — ..."** rather than describing what's *not* done yet.

This closes the loop the rest of this document assumes: §2's "read the unfinished-work index" is
only as good as this upkeep. An index that's accurate once and then drifts is worse than no index
— it tells every future supervisor a confident, wrong story.

---

*Last updated 2026-09-15. If the authority envelope or WIP limit changes, update this file
directly — it is not on the do-not-edit list in `OPERATING_INSTRUCTIONS.md` §3.*
