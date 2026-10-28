# Sophia — multi-process worker pool (Sidekiq-style dispatch)

**Status:** Plan-of-record. Not started. Created 2026-10-28 at Gary's request.
**Owner:** Sophia (execution), Gary (gates).
**Repo:** `TrueSightDAO/truesight_autopilot` (Sophia's own codebase — opens PRs).
**Relationship to prior work:** consumes `SOPHIA_REDIS_MARK_AND_CLAIM_DISPATCH_PLAN.md` (Envoy, #1735);
sequenced **after** its PR4–PR5. See §3.

> ## ▶ RESUME HERE: PR0

---

## 1. The ask, restated precisely

> *"Sophia with multiple processes running much like Sidekiq, where each process attends to a
> task in either a Discord channel or a Telegram thread."*

Decomposed into testable requirements:

1. **N worker processes** run concurrently, each executing at most one *turn* at a time.
2. **Work is addressed by conversation** — one Telegram thread or one Discord channel is a unit
   of serialization (two turns in the same thread must never overlap).
3. **A turn is a job**: enqueued by a front-end, claimed by exactly one worker, acknowledged on
   completion, retried or dead-lettered on failure.
4. **Queue state is durable** across worker restart — a worker killed mid-turn must not silently
   swallow the work.
5. **Observable**: pending / in-flight / retrying / dead, per worker, on a dashboard.

Not required by the ask, and explicitly **out of scope**: horizontal multi-host scaling, per-tenant
isolation, worker autoscaling, priority queues, scheduled/cron jobs beyond what already exists.

---

## 2. What already exists (verified 2026-10-28, not assumed)

This is deliberately generous to the status quo: **a large part of the target architecture is
already built**, which is why the plan is 11 units and not 30.

| Piece | State | Evidence |
|---|---|---|
| Mark/claim primitives | **Merged, live** | `app/redis_claim.py`; wired at `telegram_adapter.py:210` |
| Redis server | **Running, authenticated** | `redis-server.service`, `127.0.0.1:6379`, v6.0.16, `PHASE_C_REDIS_PASSWORD` from vault |
| Producer/consumer seam | **Exists** | adapters POST `/chat-blocking` + `/chat` (SSE) over HTTP (`telegram_adapter.py:11,18`) |
| Telegram front-end | **Single-instance poller, own systemd unit** | `truesight-autopilot-telegram.service`; `telegram_adapter.py:1-5` |
| Discord front-end | **Single-instance gateway, own systemd unit** | `truesight-autopilot-discord.service`; `discord_adapter.py:1-7` |
| Process supervision | **systemd** | 5 units: autopilot, telegram, discord, watchdog, vault |
| Bounded concurrency | **Merged** | `app/github_throttle.py` (#553) |
| Bounded lock registries | **Merged, deployed** | `app/lock_registry.py` (#558) |
| Fail-fast on exhausted budget | **Merged, deployed** | #557 |
| Session persistence | **On disk** | `sessions/<hash>_sessions.json` (~812 entries) |

**What does not exist:** any consumer of the marks, work-queue semantics, retry/dead-letter,
heartbeats, shared state across processes, or a queue dashboard.

---

## 3. Why this is a separate plan

`SOPHIA_REDIS_MARK_AND_CLAIM_DISPATCH_PLAN.md` builds mark and claim, then stops. Its §4 says:

> *"Gated: PR6 (design-direction decision) and, separately and **not yet scoped by this plan at
> all, any future work that actually runs a second Sophia process — that is a new plan, not an
> extension of this one**."*

And `redis_claim.py`'s own docstring:

> *"HONEST LIMITATION: Sophia runs as exactly ONE process today … Do not read the presence of
> this module as 'multi-instance Sophia is live'."*

So: this plan is the "new plan" that #1735 hands off to. It **depends on** #1735 PR4 (discovery +
claim attempt) and PR5 (mark TTL), which are **unmerged**. Starting before them would mean
re-implementing their primitives.

### 3a. Plans are invisible — fix that first

All four sibling plans live in **open, unmerged PRs**:
`#1734` lock-expiry, `#1735` mark-and-claim, `#1736` handoff registration, `#1739` rate-limit burner.
GitHub code search indexes **default branches only**, so `search_context` and `search_code` cannot
see any of them. That is why this session repeatedly believed no plan existed.

**PR0 step 1 is therefore: register this plan in `HANDOFF_MANIFEST.md` and regenerate
`handoffs/index.json`** — so the next session (or the sprint board) can actually find it.

---

## 4. Architecture decision

### Option A — scale the HTTP app (`uvicorn --workers N`)
**Rejected.** `app/main.py` holds conversation state in **module-level dicts** that fork-diverge:
`_sessions:179`, `_pending_submissions:180`, `_active_streams:183`, `_cancel_flags:184`,
`_message_queues:187`, `_session_locks:188`, `_session_lock_holders:198`,
`_session_lock_acquired_at:199`, `_live_progress:275`, `_oracle_rate_limit:751`.
Serialization would silently break: two workers could hold the same session with separate
`_session_locks` objects and interleave turns. Also loses `--workers 1`'s restart simplicity.

### Option B — producer/consumer with standalone worker processes  ✅ **CHOSEN**

```
Telegram poller (1)  ─┐
                     ├─► Redis queue ─► worker-1 ─┐
Discord gateway (1) ─┘                  worker-2 ─┼─► shared Redis state
                                        worker-N ─┘   (claims, sessions, budget)
                                                 │
                                                 └─► sophia.truesight.me dashboard
```

- **Producers stay single-instance** (a second `getUpdates` poller races on offset; a second
gateway connection is rejected by Discord). Both facts are already documented in the adapters'
docstrings — this plan *preserves* that constraint instead of fighting it.
- **Only workers scale.** Each is `python -m app.worker`, its own systemd template unit.
- **One thread = one claim.** Reuses the `tg:<chat>:<thread>` / `dc:<guild>:<channel>` key shape
already emitted by `redis_claim.mark()`.
- **Zero new infrastructure.** Redis is already provisioned and authenticated.

### Option B′ — hand-rolled queue (chosen implementation) vs. a framework (RQ / Dramatiq / Celery)

Honest framing, because "don't hand-roll a job queue" is normally sound advice:

| | Hand-rolled (B′) | Dramatiq / RQ |
|---|---|---|
| Reuses `redis_claim.py` + its tests | **yes** | no (re-implemented) |
| Retries, dead-letter, scheduling, web UI | **build** (PR1, PR8) | free |
| Fit for 30–180 s LLM-bound jobs | fine | fine |
| Dependency weight | none new | new runtime dep |
| Debuggability by a future Sophia | **high** (own code) | medium |

**Recommendation: B′**, because the primitives and their tests already exist and the queue is
really *thread-affinity dispatch* with a small feature set (claim, ack, retry, dead, heartbeat).
**Revisit trigger:** if PR1 needs more than ~3 of {priorities, cron, rate-limit groups,
batch callbacks}, stop hand-rolling and switch to Dramatiq before PR3.

### Option C — multi-host
**Explicitly out of scope.** Single box; `t3.medium`. Would require shared session storage AND
cross-host Redis before it means anything. Not planned here.

---

## 5. The seven hard blockers

Each is a thing that *silently breaks* if we add workers without addressing it. **This section is
the reason the plan exists** — the queue is the easy part.

### 5.1 Per-session serialization is in-memory → two workers can interleave one thread
`app/main.py:188 _session_locks`, `:198 _session_lock_holders`, `:199 _session_lock_acquired_at`.
All process-local. **Fix (PR4):** per-session claim in Redis (`SET lock:session:<id> <worker> NX EX 240`).
Test the invariant directly: two workers racing one session ⇒ exactly one wins.

### 5.2 Conversation state is in-memory → a turn on worker-2 cannot see worker-1's history
`_sessions` (`:179`) is the live conversation buffer; disk files (`sessions/*_sessions.json`) are
written on some paths but **read-into-memory at process start**. A turn routed to a worker with a
cold `_sessions` would answer with amnesia. **Fix (PR4):** rehydrate per-session from disk/Redis at
claim time, or pin a session to a worker with a TTL and route to the claim holder. Decide in PR0.

### 5.3 Redis will silently drop jobs at 64 MB
Measured: `used_memory 852.84K`, **`maxmemory 64.00M`**, **`maxmemory_policy noeviction`**, v6.0.16.
With `noeviction`, writes **error** at the limit — and `mark()` swallows errors by design
(`telegram_adapter.py:211-213`: *"a mark is advisory; never break dispatch"*). For a real queue
that is **silent job loss**. **Fix (PR1):** keep `noeviction` (correct for a queue — you must not
evict work), raise `maxmemory` to 512 MB, and invert the swallow: **enqueue failure must raise and
be visible**, while `mark()` stays advisory.

### 5.4 The GitHub budget is shared but the semaphore is per-process
`app/github_throttle.py:85 _semaphore = threading.BoundedSemaphore(...)` — **per process**.
N workers ⇒ 4N concurrent permits against **one** 5,000 req/h PAT. This session already saw a
single process burn **~8,000/hr** and hit 403s that blocked a merge. **Multi-process multiplies
exactly the failure we spent today fixing.** **Fix (PR6):** move the budget to Redis (token bucket,
key `sophia:gh:budget`), so all workers share one allowance. **PR6 is a prerequisite for >1 worker.
It is not optional and not deferrable.**

### 5.5 Caches assume one reader
`github_tools._read_cache:23` (per-process), `telegram_adapter._member_count_cache:590`,
`_pending_verifications:2055`, `discord_adapter._binding_cache:184`, `main._oracle_rate_limit:751`.
None are shared, so N workers = N cache copies and N× API calls — feeding 5.4 directly.
**Fix (PR4):** classify each as *share via Redis* / *acceptable per-process* / *must be singleton*,
and record the classification in code comments. Do not blanket-migrate.

### 5.6 In-flight turns are lost on restart
Today a restart kills the turn (acceptable: systemd restarts, governor re-sends). With a queue we
want at-least-once: claim → execute → **ack**, and unacked claims expire back to `ready`.
**Fix (PR1):** `BRPOPLPUSH`-equivalent (`LMOVE` in ≥6.2; this box is **6.0.16**, so use Lua
`RPOPLPUSH` semantics or `RPOP` + `ZADD`), plus a reaper for expired claims.

### 5.7 Single-poller invariants must be enforced, not just documented
`telegram_adapter.py:1-5` and `discord_adapter.py:1-7` both say single-instance and explain why.
Once systemd template units exist, someone will start `telegram@2`. **Fix (PR9):** a startup
guard (Redis `SET NX` singleton lock per front-end) that **refuses to start** a second poller or
gateway, with an explicit error. Prevent the footgun; don't rely on a comment.

---

## 6. Sequenced plan

One PR per turn. Gates named per §5e. Deploy is human-run and out of band.

| # | Scope | Files (expected) | Gate |
|---|---|---|---|
| **PR0** | **Decision writeup + registration.** Resolve 5.2 (rehydrate vs. pin), 5.5 (per-cache classification), and B′ vs Dramatiq. Register plan in `HANDOFF_MANIFEST.md` + regenerate `handoffs/index.json`. **No code.** | docs only | auto (merge) |
| **PR1** | **Queue substrate.** `sophia:queue:{ready,inflight,retry,dead}`; atomic claim; ack/nack; expired-claim reaper; loud enqueue errors (5.3); tests vs real Redis. | `app/work_queue.py` (new), tests | auto |
| **PR2** | **Job envelope + idempotency.** `{job_id, conversation_key, session_id, platform, payload, attempt, enqueued_at}`; dedupe on `job_id`; replay-safe. | `app/work_queue.py`, tests | auto |
| **PR3** | **Worker process.** `python -m app.worker` — claim loop, graceful SIGTERM drain (finish current turn, don't ack mid-turn), heartbeat `sophia:worker:<id>` TTL 30 s, structured logging with `worker_id`. | `app/worker.py` (new), tests | auto |
| **PR4** | **Shared-state migration.** The 10 dicts from §5.1/5.2/5.5 → Redis or explicit per-process. **The largest and riskiest unit.** Ships with a cross-process test. | `app/main.py`, `app/state.py` (new) | auto, review-heavy |
| **PR5** | **Producers enqueue.** Adapters stop blocking on `/chat-blocking`; enqueue instead; keep an inline fallback behind `DISPATCH_MODE=inline|queue` so rollback is a config flip. | `telegram_adapter.py`, `discord_adapter.py` | auto |
| **PR6** | **Shared GitHub budget (Redis token bucket).** Prerequisite for >1 worker. | `app/github_throttle.py`, tests | **merge-gated** |
| **PR7** | **Front-end singleton guard** (5.7) — refuse a second poller/gateway at startup. | both adapters | auto |
| **PR8** | **Queue dashboard** on `sophia.truesight.me`, **governor-JWT-gated** (same pattern as `media_archive_pipeline.py`), read-only: queues, in-flight claims w/ TTL, per-worker heartbeat, dead set. **No action buttons** (retry/kill is a later, separate unit). | new route + template | auto |
| **PR9** | **systemd template units** `sophia-worker@.service` + documented capacity/env for N. | deploy docs | **merge-gated** |
| **PR10** | **Load test + cutover.** 2 workers → measure → 4. Kill-switch back to `DISPATCH_MODE=inline`. | scripts + runbook | **gate: human** |

**Ordering is load-bearing:** PR6 before PR5 (otherwise enqueued work burns the PAT from N
processes), and PR9 after PR7 (otherwise duplicate pollers are one `systemctl start` away).

---

## 7. Roadmap

**Phase 0 — Decide (PR0).** ~1 turn. Writeup only. Cheap; prevents building the wrong thing.

**Phase 1 — Queue exists, nothing uses it (PR1–PR2).** ~2 turns. Real Redis, real tests,
zero behaviour change. At the end, a job can be enqueued and claimed by hand.

**Phase 2 — A worker exists, still not the path (PR3).** ~1 turn. `app.worker` runs, idles,
heartbeats. Still single-process behaviour.

**Phase 3 — Make state shareable (PR4).** ~2–3 turns. **Go/no-go checkpoint.** If shared state
proves too invasive, **stop here** — the honest fallback is staying single-process with the
existing thread pool (which already gives non-blocking turns), and the plan is a writeoff of
docs + a queue module. That is a legitimate, non-shameful outcome.

**Phase 4 — Move the traffic (PR5–PR7).** ~3 turns. Producers enqueue; budget shared; singleton
guards. Rollback = `DISPATCH_MODE=inline`.

**Phase 5 — Observe (PR8).** ~1 turn. Dashboard so the distributed system is debuggable.

**Phase 6 — Scale & prove (PR9–PR10).** 2 workers, measure, 4 workers. **Human gate.**

**Realistic total: 12–15 turns**, with a designed exit ramp at Phase 3.

---

## 8. Checklist

### Before PR1 — preconditions
- [ ] #1735 PR4 (discovery + claim attempt) merged
- [ ] #1735 PR5 (mark TTL) merged — today `marks` has **TTL -1** and nothing drains it
- [ ] PR0 writeup merged (5.2 / 5.5 / B′ decisions recorded)
- [ ] Redis `maxmemory` raised 64 MB → 512 MB, policy stays `noeviction`, **documented**
- [ ] Redis auth confirmed for every worker path (vault `PHASE_C_REDIS_PASSWORD`)
- [ ] This plan registered in `HANDOFF_MANIFEST.md`; `index.json` regenerated
- [ ] Backup of `sessions/` taken before any PR4 work

### Per-PR (every unit)
- [ ] `python3 -m compileall -q app scripts tests`
- [ ] `python3 -m ruff check app scripts tests`
- [ ] `python3 -m ruff format --check app scripts tests`
- [ ] `python3 -m pytest -q` — all green
- [ ] New test proves the *invariant*, not just the happy path
- [ ] Rollback described in the PR body
- [ ] No change to Telegram/Discord receipt path without proving existing behaviour unchanged

### Correctness invariants to test explicitly
- [ ] **One session, two workers ⇒ exactly one wins** (5.1)
- [ ] **Crash mid-turn ⇒ job returns to `ready`, not lost** (5.6)
- [ ] **Redis at `maxmemory` ⇒ enqueue raises, is visible, job not silently dropped** (5.3)
- [ ] **N workers ⇒ total GitHub rate stays within one budget** (5.4)
- [ ] **Second Telegram poller refuses to start** (5.7)
- [ ] **Worker SIGTERM mid-turn ⇒ finishes, acks, exits clean** (PR3)

### Before declaring done
- [ ] Dashboard shows a real in-flight claim during a live turn (not just 0)
- [ ] Kill-switch `DISPATCH_MODE=inline` verified to actually work
- [ ] Queue depth, retry count, dead-set size visible and alertable
- [ ] Runbook: how to drain, how to kill a stuck claim, how to get back to one worker

---

## 9. Capacity — what this box can actually do

Say this plainly, because "Sidekiq-style" suggests elastic scale and this is not that:

| Resource | Measured | Implication |
|---|---|---|
| vCPU | **2** (t3.medium, burstable) | CPU is the ceiling, and **credits are finite** |
| RAM | 3 GB total, ~1 GB used | 378 MB/worker ⇒ ~4–5 workers max |
| Disk | 66 G / 155 G (43%) | fine |
| Redis | 64 MB (→512 MB) | fine for queue state, **not** for payloads |

**Realistic target: 2–4 workers**, each bound by LLM latency (30–180 s/turn), not CPU.
That is genuine headroom for several governors/messages at once — which is the actual user problem —
but it will **not** be a 25-thread pool, and the plan should never be pitched as one.

If sustained concurrency beyond ~4 is genuinely needed, the answer is a bigger instance type
**first**, and multi-host **much** later.

---

## 10. Risks and anti-patterns

- **Making today's 403 problem worse.** The single biggest risk. N workers ⇒ N× GitHub burn against
  one PAT. PR6 before PR5, no exceptions.
- **Silent job loss** via `noeviction` + swallowed writes (5.3). A queue that drops work under
  pressure is worse than no queue, because it fails invisibly.
- **Distributed-state debugging tax.** Every future incident now needs `worker_id` + correlation
  IDs. PR3 must ship structured logging *before* PR5 moves traffic.
- **Deploy cost rises.** Restarts affect N units. PR3's graceful drain is what makes deploys safe.
- **Don't blanket-migrate caches to Redis (5.5).** Shared state is a cost. Classify, then migrate
  only what genuinely must be shared.
- **Don't let a comment enforce a singleton (5.7).** Two docstrings already warn about it; that
  did not stop this session from asking whether Redis was already a per-message ledger.
- **Don't confuse this with the rate-limit work.** `SOPHIA_GITHUB_RATE_LIMIT_GOVERNOR_PLAN.md`
  (#553/#556/#557/#558) bounds concurrency *within* one process and is **done and deployed**.
  This plan is orthogonal and must not be used to re-open it.

---

## 11. Authorization envelope (§5e)

- **Pre-authorized (autonomous, PR-per-turn):** PR0–PR5, PR7, PR8. Sophia opens each PR, merges
  its own feature PRs when CI is green.
- **Merge-gated:**
  - **PR6** — changes the shared GitHub budget for all workers; a mistake stalls every Sophia
    action at once.
  - **PR9** — introduces N systemd units on the live box.
- **Human gate:** PR10 (cutover to multiple live workers) — irreversible-ish in the sense that a
  badly-chosen N degrades every governor's experience at once.
- **Never autonomous:** production deploy (human-run per §5c), raising Redis `maxmemory` on the
  live instance (infrastructure change — state it, get a go), and any money/TDG action.

---

## 12. Resume tracker

**RESUME HERE → PR0.**

| Unit | PR opened | Merged | Deployed | Notes |
|---|---|---|---|---|
| PR0 — decisions + registration | ☐ | ☐ | n/a | docs only; unblocks the rest |
| PR1 — queue substrate | ☐ | ☐ | ☐ | + raise Redis maxmemory, loud enqueue |
| PR2 — job envelope / idempotency | ☐ | ☐ | ☐ | |
| PR3 — worker process + drain + heartbeat | ☐ | ☐ | ☐ | |
| PR4 — shared-state migration | ☐ | ☐ | ☐ | **go/no-go checkpoint** |
| PR5 — producers enqueue | ☐ | ☐ | ☐ | `DISPATCH_MODE` kill-switch |
| PR6 — shared GitHub budget | ☐ | ☐ | ☐ | **merge-gated; prerequisite for >1 worker** |
| PR7 — front-end singleton guard | ☐ | ☐ | ☐ | |
| PR8 — queue dashboard | ☐ | ☐ | ☐ | governor-JWT-gated, read-only |
| PR9 — systemd template units | ☐ | ☐ | ☐ | **merge-gated** |
| PR10 — load test + cutover | ☐ | ☐ | n/a | **gate: human** |

---

## 13. UAT

- **PR1–PR4:** automated, against the **real local Redis** (not mocked), asserting the §8
  invariants. No human surface.
- **PR5:** regression — a Telegram message and a Discord message each produce exactly one turn,
  with `DISPATCH_MODE=inline` and `=queue` producing identical user-visible behaviour.
- **PR8:** Sophia UAT — dashboard shows a real in-flight claim during a live turn.
- **PR10:** **human UAT** — Gary sends concurrent messages to ≥2 threads and confirms both are
  answered concurrently, then confirms the kill-switch returns to single-worker behaviour.

---

## 14. Pre-flight completeness (§5d)

Every file, symbol, and measurement this plan's units depend on is captured in §2 and §5 with
`file:line` or a measured value. A future session can execute PR0–PR10 **without re-discovering
the system**, which is the point of §5d. If a unit finds a fact contradicting §5, that is a signal
this plan was written against stale code — stop and correct the plan before continuing.
