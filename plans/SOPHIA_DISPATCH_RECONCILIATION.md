# Sophia dispatch — reconciliation of the two multi-process plans (PLAN OF RECORD)

**Status:** **plan-of-record.** Decided 2026-10-29.
**Governor:** Gary. **Executor:** Sophia.
**Supersedes:** `plans/SOPHIA_SIDEKIQ_MULTIPROCESS_PLAN.md` (roadmap numbering) and
`plans/SOPHIA_MULTI_PROCESS_WORKER_PLAN.md` (PR #1740 — target architecture).

---

## 0. Why this document exists

Two plans were written in parallel and described **two different target architectures**:

| | Plan | Assumed substrate |
|---|---|---|
| **Plan 1** | `SOPHIA_SIDEKIQ_MULTIPROCESS_PLAN.md` (on `main`) | Scale `uvicorn --workers N` directly; solve session affinity with Redis claims. |
| **Plan 2** | `SOPHIA_MULTI_PROCESS_WORKER_PLAN.md` (PR #1740) | **Reject** `--workers N`; run N dedicated `python -m app.worker` processes consuming a Redis queue. |

Neither built the dashboard. Neither was reconciled with the other. Gary flagged it
2026-10-29: *"don't build toward two different target architectures."*

Then reality decided part of it: **Option A went live on its own.** The service has run
`--workers 4` since 2026-10-29, and a large amount of Plan 2's "prerequisite" work had
already shipped as part of making that safe. This document records what is actually true,
and re-scopes both plans against it.

---

## 1. Verified live state (evidence, not inference)

Checked against the running box on 2026-10-29, after Gary's direction.

| # | Fact | Evidence |
|---|---|---|
| 1 | **`--workers 4` is live** | `ExecStart=/opt/…/uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4`; master PID 4180377, children 4180381–84, **283–341 MB RSS each** |
| 2 | Deployed HEAD | `01bcae5` — *"fix(lifespan): singleton-guard the 9 background loops for --workers 4 (#583)"* |
| 3 | Second app on the same box | `vault_app` :8002 `--workers 2` (PIDs 4179599/600) — 6 python children total vs 2 vCPU |
| 4 | **Cross-process session exclusion is live** | `app/session_claim.py` (Lua check-owner-then-act over `redis_claim`), wired at `app/main.py:363-372`; **`SESSION_CLAIM_ENABLED=true`** in `.env:94` |
| 5 | **Queue / cancel / live-progress are shared** | `app/session_state.py` — `queue_push/pop/snapshot`, `set_cancel/is_cancelled`, `progress_set/get/clear`, read cross-process at `main.py:1592, 3503, 4000s, 4760s` |
| 6 | **Background-loop singletons are live** | `app/singleton_guard.py` at 9 sites (`main.py:712–816`). Live keys prove it works: `_catalog_refresh_loop` on PID 4180381, `aws_monitor`/`calendar_watchdog_loop`/`email_poller` on 4180382, `followup_loop`/`email_watch`/`_context_sync_loop` on 4180384 |
| 7 | **GitHub budget is still per-process** | `app/github_throttle.py`: `_semaphore = threading.BoundedSemaphore(max_concurrency())` **at import**, default 4 ⇒ **16 concurrent permits against one 5,000 req/h PAT** |
| 8 | Redis ceiling unchanged | 6.0.16, `used_memory 963.41K`, **`maxmemory 64 MB`**, policy `noeviction`, `dbsize 38` — families `lock:`×10, `loop*`×27, `marks`×1 |
| 9 | **Nothing drains `marks`** | ~31 live members (`tg:*`, `dc:923008087315587072:*`). `mark()` is advisory and no reaper consumes it |
| 10 | Front-end pollers are separate units | `telegram_adapter.py:4` / `discord_adapter.py:3` say "run it as its own systemd unit"; **no `run_as_singleton` in `telegram_adapter.py`** ⇒ #1740 PR7 (front-end singleton guard) is genuinely still open |

### The consequence for Plan 2

Plan 2's §5 "seven hard blockers" was the stated reason to reject Option A. Most of them are
**already fixed by code that is running right now**:

| Plan 2 blocker | Status today |
|---|---|
| §5.1 per-session serialization is in-memory | **CLOSED** — `session_claim`, enabled in prod |
| §5.2 conversation state is in-memory | **Materially addressed** — `session_state` holds queue, cancel, live progress cross-process |
| §5.7 single-poller footgun | **CLOSED for the 9 loops** (`singleton_guard`); **still open for the adapters** |
| §5.6 in-flight turn lost on restart | Open, and *accepted* under Option A (systemd restarts; governor re-sends) |
| §5.4 shared PAT, per-process semaphore | **OPEN and live** — the most important item on this page |
| §5.3 Redis drops work at 64 MB | **OPEN** |

The premise for rejecting Option A — *"in-process state diverges across workers"* — is no longer
true for locks, cancel flags, live progress, or loop singletons. Plan 2's Phase-3 go/no-go on
shareable state has, in practice, **already been answered yes**. So the architecture question
is settled empirically, not by preference.

---

## 2. Decision

> **Option A — `uvicorn --workers N` — is the dispatch substrate.**
> Plan 2 is demoted from *target architecture* to **gap register + dashboard specification**.

What this cancels in Plan 2 (`SOPHIA_MULTI_PROCESS_WORKER_PLAN.md`):

| Plan 2 unit | Disposition |
|---|---|
| PR0 decision writeup | **Superseded by this document** |
| PR1 `app/work_queue.py` (queue substrate) | **CANCELLED** — `session_state` already provides the queue |
| PR2 job envelope + idempotency | **CANCELLED** — no job envelope needed without a job queue |
| PR3 `app/worker.py` | **CANCELLED** — uvicorn children *are* the workers |
| PR4 shared-state migration | **LARGELY SHIPPED** (see §1 rows 4–6); residual = §1 row 9 (marks reaper) |
| PR5 producers enqueue | **CANCELLED** — no `DISPATCH_MODE`, no queue to roll back to |
| PR6 shared GitHub budget | **SURVIVES, promoted to first** (PR-C) |
| PR7 front-end singleton guard | **SURVIVES** (PR-E) — see §1 row 10 |
| PR8 dashboard | **SURVIVES** (PR-B), split 8a/8b as already specified in #1740 §4a |
| PR9 systemd `sophia-worker@.service` | **CANCELLED** — template units exist only for dedicated workers |
| PR10 load test + cutover | **DEGRADED** to "watch CPU/mem under real load" — the cutover already happened |

---

## 3. The constraint that defines "deliberate dispatch"

Gary's goal 2 is *"real deliberate task dispatch — assign this task to this worker."* Under
Option A there is a hard structural limit that must be stated plainly, because it changes what
the feature can be:

**With `--workers N`, uvicorn shares one listening socket and the OS kernel chooses which child
`accept()`s each connection.** The application cannot pin an inbound request to a worker before
it is accepted. Therefore:

> **Deliberate dispatch cannot mean "route the TCP connection." It must mean affinity routing
after accept** — every child registers identity + heartbeat in Redis
(`sophia:worker:<id>`, TTL 30 s), and a request that arrives on the *wrong* child for its session
is handed off / enqueued for the designated worker instead of executed inline, reusing the
existing `session_state` queue.

This is a genuinely smaller feature than Plan 2's, and it is the only version that is true under
the substrate we actually run.

**Ordering consequence:** the registry (PR-A) is a **prerequisite for the dashboard (PR-B)**, not
a sibling. "Per-worker heartbeat" is something the dashboard *reads*; today there is no worker
identity or heartbeat anywhere in Redis to read. A dashboard built first would render an empty page.

---

## 4. Unit order (governor-directed 2026-10-29)

Because `--workers 4` is **already live**, the per-process GitHub budget is a *present-tense*
production risk, not a sequencing preference. Hence PR-C first.

| # | Unit | Scope | Gate |
|---|---|---|---|
| **PR-C** | **Shared GitHub token bucket (Redis)** | Replace the import-time per-process `BoundedSemaphore(4)` with a Redis token bucket (`sophia:gh:budget`) so all workers share **one** 4-permit / 5,000-h budget. Keep fail-open-on-timeout semantics. Cross-process test. | auto (merge) |
| **PR-D** | **Redis `maxmemory` 64 MB → 512 MB** | Config + documented; `noeviction` stays (correct for a queue). Also decide the `marks` reaper (§1 row 9). | auto + documented |
| **PR-A** | **Dispatch registry** | `app/dispatch_registry.py`: worker id, 30 s heartbeat `sophia:worker:<id>` (TTL 30 s), session→worker affinity key, TTL'd. Read-only observable surface first; no routing change. | auto |
| **PR-B** | **Governor-JWT dashboard** | Read-only view on `sophia.truesight.me`: live workers, heartbeat age, in-flight claims + TTL remaining, queue depth, marks backlog, dead/lost count. **No action buttons.** Reuses existing auth gate (#379). | auto |
| **PR-E** | **Front-end singleton guard** | Startup `SET NX` guard so a second telegram poller / discord gateway refuses to start (Plan 2 PR7). | auto |
| **PR-F** | **Affinity routing** | Actually use the registry: wrong-child handoff via `session_state`. This is Gary's goal 2 proper. | **gate: human** |

### Dashboard placement (carried over from #1740 §4a, still correct)

- `sprint.truesight.me` (GitHub Pages) **cannot hold a secret** ⇒ public **aggregate counters only**, if built at all (8a).
- `sophia.truesight.me` is the **governor-JWT** surface ⇒ per-thread/per-worker forensics (8b). **PR-B = 8b**, which is what Gary asked for.
- CORS is already permitted from the sprint origin (`main.py` `CORSMiddleware`), so 8a adds no auth work if it is ever wanted.
- Any such view must render a visible `snapshot_at` and fetch with `cache: "no-store"`.

---

## 5. Open items

- **Filed in `OPEN_FOLLOWUPS.md`:** §1 row 7 (16 permits / 1 PAT) and row 8 (64 MB + swallowing `mark()`).
- **Still open, not yet scoped:** adapters have no singleton guard (row 10) — tracked as PR-E.
- **Now measurable, previously not:** whether 4 workers on 2 vCPU is right. `--workers 4` was set by
go-ahead, not by measurement. PR-B's dashboard is what makes that question answerable.
- **Plan 2 (#1740)** is rescoped in place; its remaining value is §4a (dashboard split), §5 (gap
register) and §9 (capacity math).

---

## 6. Resume

**RESUME HERE → PR-C (shared GitHub token bucket).**
