# Sophia: Sidekiq-style multi-process dispatch — implementation plan, roadmap, checklist

> ## ⚠️ SUPERSEDED 2026-10-29 — read `plans/SOPHIA_DISPATCH_RECONCILIATION.md` first
>
> This plan's *direction* was right and much of it **shipped**, but its roadmap numbering is dead
> and must not be executed as written:
>
> - Its PR5/PR6 ("Gary decides N" → "flip the service file, deploy, go live") **already happened
>   out of band**: `--workers 4` has been live since 2026-10-29 (`01bcae5`).
> - Its PR1 (replace the in-process `asyncio.Lock` with Redis claims) shipped as
>   `app/session_claim.py`, now enabled in production (`SESSION_CLAIM_ENABLED=true`).
> - Its PR8 (dashboard) is still unbuilt and is renumbered there.
>
> It also ran **in parallel with** `plans/SOPHIA_MULTI_PROCESS_WORKER_PLAN.md` (PR #1740), which
> proposed a *different* target architecture (dedicated workers off a Redis queue, explicitly
> rejecting `--workers N`). The two were never reconciled. They are now:
> **`plans/SOPHIA_DISPATCH_RECONCILIATION.md` is the single plan-of-record.**
>
> Do not start any unit below without reading that document first.

**Status:** **superseded** 2026-10-29 by `plans/SOPHIA_DISPATCH_RECONCILIATION.md`.
**Owner:** supervisor (Envoy), per Gary's direct request in `#envoy-server` 2026-10-28
**Depends on:** `plans/SOPHIA_REDIS_MARK_AND_CLAIM_DISPATCH_PLAN.md` (PR1/PR2 already merged — see §0)

## 0. Pre-flight (§5d completeness)

Gary's ask: *"Sophia with multiple processes running much like sidekiq, where each process
attends to a task in either a Discord channel or Telegram thread."* Today there is exactly
**one** `truesight-autopilot` process (`--workers 1`), and that `1` is load-bearing, not a
tuning default:

```
systemd/truesight-autopilot.service:11: # --workers 1 is REQUIRED, not a tuning choice: the app keeps per-session state
systemd/truesight-autopilot.service:13: # its own copies, so same-thread requests on different workers race on the shared
app/main.py:182-233: _session_locks: dict[str, asyncio.Lock]  — in-process only, not shared across OS processes
```

So the real blocker to "multiple processes" was never Sidekiq-style queue semantics — it's that
session mutual exclusion is implemented with a Python `asyncio.Lock` that only exists inside one
process's memory. Two processes would each get their own lock for the same session and could
run that session concurrently, corrupting shared state (Edgar identities, in-flight PR context,
etc).

**What's already built, resolving most of this** (`SOPHIA_REDIS_MARK_AND_CLAIM_DISPATCH_PLAN.md`,
confirmed merged on `origin/main` just now, not just proposed):

| PR | Commit | Status |
|---|---|---|
| PR1 — Redis claim primitives (mark/try_claim/release) | `1664e99` (#552) | merged |
| PR1 — GitHub concurrency governor + thread-safe read cache | `7b8e45e` (#553) | merged |
| fix — redis made a runtime dep (was broken in prod) | `6a9e407` (#554) | merged |
| PR2 — Telegram adapter writes an advisory Redis mark per inbound message | `ed56348` (#555) | merged |
| PR1 — staleness expiry on the *inner* per-turn session lock | `62ecabb` (#551) | merged |
| PR0 (this plan) — Discord adapter writes an advisory Redis mark per inbound message | `c8ed47f` (#565) | merged |

The dispatch plan's own resume tracker (as committed) still shows all boxes unchecked — that
doc is stale, not the code; this table supersedes it. **Not yet built**: the discovery/claim-attempt loop (PR4), mark TTL/cleanup
(PR5), the
`active_supervision.json` relationship decision (PR6, human gate), the dashboard (PR7) — and,
critically, **the one thing that actually turns these marks into safe multi-process dispatch**:
replacing `_session_lock()`'s in-process `asyncio.Lock` with the cross-process `try_claim`/
`release` primitives PR1 already shipped. The marks today are *advisory telemetry* ("something
is happening with this session"), not yet a claim that a second process would respect.

**Resource headroom — re-verified today, not assumed from the 2026-10-26/27 note**
([[project_sophia_box_resource_pressure]]):
- The previously-open second hung process (PID 2174824, 30 days/72% CPU) **no longer exists** —
  resolved since that note was written. One fewer blocker than the memory recorded.
- `free -h`: 3.7Gi total, 2.4Gi *available* (2.6Gi buff/cache is reclaimable), swap 5Gi total
  (2Gi `/swapfile` + 3Gi ad-hoc `/tmp/gaia.swap`) with only 526Mi in use.
- The single running autopilot process uses **~350MB RSS** (`systemctl show ... MemoryCurrent`).
- `nproc` = **2** (t3.medium). CPU, not RAM, is the more likely first ceiling for multiple
  concurrent async-Python processes doing real LLM-round work — this must be load-tested
  (Unit 3 below), not assumed either way.
- Still open, **not** a gate for this plan but worth closing separately: `/tmp/oscar2026` (13GB
  real farm-media bytes, disposition undecided) and `/tmp/gaia.swap` being unregistered in
  `/etc/fstab` (works today, won't survive a reboot without re-creation).

**Why Sidekiq-the-metaphor is directionally right but not literally what to build**: Sidekiq
workers are stateless and pull arbitrary jobs off one shared queue. Sophia's "jobs" are
long-lived *conversations* (a Discord thread, a Telegram chat) with multi-turn context that
must stay affinitized to whichever process is handling it — you cannot load-balance individual
turns across workers mid-conversation. So the right shape is **one worker claims one
session-stream for its duration**, not Sidekiq's "any worker takes any job." The Redis
mark-and-claim primitives already model this correctly (claim = ownership of a session, not a
job pop) — this plan finishes wiring that model into something that actually dispatches across
*more than one OS process*, rather than one process privately bookkeeping its own marks.

## 1. Design

**Phase A (this plan): scale workers on the existing box.** Run N `uvicorn` worker processes
behind the same `truesight-autopilot` service, coordinating session ownership through Redis
(already running, already the mark store) instead of the in-process dict. This is the cheapest
way to get real multi-process behavior and to find out whether the box's CPU is actually the
constraint, before touching infrastructure.

**Phase B (out of scope here, revisit only if Phase A proves CPU-bound): multiple EC2
instances.** Each instance runs its own autopilot process, all pointed at the same Redis for
cross-host claims. Bigger blast radius (health checks, per-host deploys, DNS/LB), so only take
this on if Phase A's load test (Unit 3) shows the single t3.medium genuinely can't hold the
concurrency Gary wants. Not sequenced below; flag back to Gary if we get there.

## 2. Sequenced plan (one PR per turn, §5a)

| Unit | What | Why this order |
|---|---|---|
| **PR0** | Finish the mechanism layer: Discord adapter marks (dispatch plan's PR3) | Needed before cross-process claiming has two symmetric adapters to protect |
| **PR1** | Replace `_session_lock()`'s `asyncio.Lock` with Redis `try_claim`/`release` (check-owner-then-release via Lua `EVAL`, same pattern as PR1's primitives) | **The actual architectural change.** Everything after this is safe only because of this |
| **PR2** | Discovery + claim-attempt loop (dispatch plan's PR4): idle worker scans unclaimed marks, attempts claim, routes that session's subsequent turns to itself | Without this, a 2nd process never picks anything up — it just sits idle |
| **PR3** | Mark TTL + cleanup (dispatch plan's PR5) | Needed once marks are load-bearing for real dispatch, not just telemetry |
| **PR4** | Load test: run `--workers 2` in a scratch/staging config on the real box, drive concurrent sessions, watch `free -h` / `MemoryCurrent` / CPU under load | Validates or refutes the "CPU is the ceiling" hypothesis in §0 with data, before enabling for real |
| **PR5** (gate: human) | Based on PR4's numbers, Gary decides N (likely 2, maybe stays at 1 if CPU-bound) and approves flipping `systemd/truesight-autopilot.service` to `--workers N` | A live-service deploy/restart — always-stop per §5.0/§5c |
| **PR6** | Flip the service file, deploy, verify no regressions over 24h | The actual go-live |
| **PR7** | `active_supervision.json` relationship decision (dispatch plan's PR6, still pending) | Needs revisiting now that there may be >1 live process each capable of picking up claims |
| **PR8** | Admin dashboard (dispatch plan's PR7): which process holds which session, claim age, mark backlog | Only useful once there's something to observe beyond 0/1 workers |

Separately, not sequenced into the roadmap: resolve `/tmp/oscar2026` disposition and register
`/tmp/gaia.swap` in `/etc/fstab` (or replace with a properly-provisioned swapfile) — both
pre-existing, neither blocks this plan, but PR4's load test will be more trustworthy if swap
state is stable and intentional rather than ad-hoc.

## 3. Resume tracker

**RESUME HERE → PR2 (discovery + claim-attempt loop).**

| Unit | PR opened | Merged (human) | Notes |
|---|---|---|---|
| PR0 — Discord adapter marks | ✅ #565 | ✅ `c8ed47f` (2026-10-28) | merged; mirrors #555's Telegram pattern |
| PR1 — cross-process session lock via Redis claim | ✅ #567 | ✅ `1a7d923` (2026-10-28) | merged; #566 closed as a less-complete duplicate (no renewal) |
| PR2 — discovery + claim-attempt loop | ☐ | ☐ | |
| PR3 — mark TTL/cleanup | ☐ | ☐ | |
| PR4 — load test `--workers 2` | ☐ (data, not code) | n/a | produces the numbers PR5 decides on |
| PR5 — N + go-ahead | ☐ (writeup) | n/a | **gate: human (Gary)** — live-service restart |
| PR6 — flip service file + deploy + 24h verify | ☐ | ☐ | **gate: human sign-off before/after**, per §5.0 deploy rule |
| PR7 — active_supervision.json relationship decision | ☐ (writeup) | n/a | **gate: human** (carried over from dispatch plan's PR6) |
| PR8 — dashboard | ☐ | ☐ | |

### PR1 handoff note — cross-process session lock via Redis claim

**Goal:** replace `app/main.py`'s in-process `_session_lock()` `asyncio.Lock`
(`app/main.py:182-233`) with the cross-process `try_claim` / `release` primitives already
shipped in `app/redis_claim.py` (PR1, `1664e99` / #552). This is **the actual architectural
change** — everything after it in §2 is only safe because of it.

**Why it matters:** `_session_locks: dict[str, asyncio.Lock]` lives inside one process's
memory. With `--workers 2` each process would get its own lock for the *same* session, so two
processes could execute one conversation concurrently and race on shared state (Edgar
identities, in-flight PR context, session transcript writes). The marks shipped in #555
(Telegram) and #565 (Discord) are currently *advisory telemetry* — a second process does not
respect them yet.

**Approach for the next turn:**
1. Read `_session_lock()` and every call site in `app/main.py`; record current semantics
   (acquisition, per-turn staleness expiry, release in `finally`, behaviour on timeout).
2. Confirm the `try_claim` / `release` contract in `app/redis_claim.py`: TTL, owner token, and
   the Lua `EVAL` check-owner-then-release, so a process cannot release a claim it does not
   hold.
3. Preserve existing behaviour as the default: single-process (`--workers 1`) must behave
   identically; the Redis path only becomes load-bearing when a second process exists.
4. Degrade safely like the marks do — a Redis outage must not wedge every session forever.
   Whether that means fail-open or bounded-wait must be decided explicitly, not by accident.
5. Tests must prove: two independent claimers cannot both hold one session · a stale claim
   expires · release is owner-checked · the Redis-down behaviour is the documented one.

**Gate:** the four local gates (compileall / ruff on touched files / ruff format / pytest)
before any push. **No production restart in PR1** — flipping
`systemd/truesight-autopilot.service` stays PR5/PR6 and remains a human gate.

## 4. Always-stop gates (§5.0/§5c)

- PR5: choosing to increase live worker count is a production-capacity decision, not an
  implementation detail — Gary decides N from PR4's data.
- PR6: restarting/redeploying the live `truesight-autopilot` service is always-gated regardless
  of what triggered it.
- PR7: whether `active_supervision.json` (human-facing claim ledger) and Redis marks (machine
  dispatch state) merge, stay parallel, or one subsumes the other is a workflow decision for
  Gary, carried over unresolved from the original dispatch plan.
