# Sophia — Redis mark-and-claim dispatch (Phase C)

**Status:** approved to execute, ahead of the original gate. **Owner:** Sophia (execution),
Envoy (planner/author). **Origin:** Gary, 2026-10-28, explicitly overriding
`SOPHIA_LOCK_EXPIRY_AND_LOAD_TEST_PLAN.md`'s PR4 gate (that plan parked this work behind the
PR3 load test; Gary chose to build it now instead). Design content lifted from that plan's §3b,
written there 2026-10-28 before this split-out.

**Cross-reference:** `SOPHIA_LOCK_EXPIRY_AND_LOAD_TEST_PLAN.md` PR1–PR3 (session/dispatch-lock
staleness expiry + load test) continue independently — this plan does not block or get blocked
by that one. The Redis instance this plan uses was already provisioned and hardened
(`PHASE_C_REDIS_PASSWORD` in the vault) per that plan's §3a, 2026-10-27.

---

## 0. What this is, and the one thing it honestly cannot prove yet

Adapters (Telegram, Discord) write a **mark** to Redis on every inbound message: "this thread
has unprocessed work." Any idle Sophia worker can discover marks and **claim** a thread
(`SET lock:<thread_id> <worker_id> NX EX <ttl>` — Redis's standard atomic distributed-lock
primitive) before acting on it. A mark is not a claim; two different operations, two different
owners (§1 below has the full design, unchanged from the original sketch).

**Honest limitation, stated up front:** Sophia runs as exactly **one process** today. Every PR in
this plan is independently correct and testable in isolation (unit/integration tests against the
real local Redis), but **none of it has a second worker to observably change behavior with until
a second Sophia process exists** — which this plan does not build (multi-process deployment,
systemd units or multi-EC2, is a separate, not-yet-scoped piece of work). Building this now is a
deliberate bet that the mechanism is worth having in place before it's needed, not a claim that
it does anything differently in production yet. Say this plainly in every status report so it
isn't mistaken for "multi-instance Sophia is now live."

---

## 1. Pre-flight (§5d)

**Redis, already provisioned (`SOPHIA_LOCK_EXPIRY_AND_LOAD_TEST_PLAN.md` §3a):** local instance
on Sophia's box, `127.0.0.1:6379`, `requirepass` set (vault name `PHASE_C_REDIS_PASSWORD`,
`Vault().get_value("PHASE_C_REDIS_PASSWORD")` — same retrieval pattern as `DISCORD_BOT_TOKEN`),
`maxmemory 64mb` / `maxmemory-policy noeviction`. Currently 0 keys, nothing else using it
(verified 2026-10-28 — no redis client import anywhere in `app/*.py` yet).

**Existing code this plan must not break, same sites as the other plan's pre-flight:**
- `app/telegram_adapter.py` `handle_message` → `_run_turn_with_auto_advance` (holds
  `_thread_dispatch_locks` for the whole auto-advance chain) is the **current, only** dispatch
  path. This plan's mark-write is **additive** — it must not change when/whether a message is
  processed, only add a parallel Redis record of "this happened."
- `app/discord_adapter.py` `handle_message`, same shape, `_channel_dispatch_locks`.
- `app/main.py`'s `while queue:` drain (`main.py:3703`) is the existing same-process mechanism
  for "a message arrived while this worker was already mid-turn on this thread." This plan does
  **not** replace it — the Redis mark is purely a discovery aid for *idle* threads a worker
  doesn't already own.
- `app/supervision.py` `claim_for_turn`/`release` (PR4c(a)) already write
  `handoffs/active_supervision.json` on every turn, at the *inner per-turn* granularity, as a
  human-facing dashboard-freshness signal. This plan's claim is a **different, lower-level**
  primitive (atomic Redis lock for mutual exclusion) — not a replacement for that dashboard
  signal. Do not conflate the two or try to unify them in this plan; that's an explicit open
  question (§4) for whoever scopes multi-process deployment later.

**No cross-repo reads beyond this** — the lock sites, the queue-drain, and the existing
supervision-claim mechanism are the only things a PR turn needs, and they're all captured above.

✅ **Pre-flight Completeness:** no execution unit requires reading a file/state not already
captured in this pre-flight.

---

## 2. Sequenced plan (§5a — one PR per turn)

| Unit | Scope | Advance |
|---|---|---|
| **PR1** | Redis client module (`app/redis_claim.py` or similar — name it sensibly, don't presume) with two primitives: `mark(thread_id)` (idempotent, e.g. `SADD marks <thread_id>` or a sorted-set keyed by timestamp — pick one and justify it in the PR) and `try_claim(thread_id, worker_id, ttl) -> bool` using `SET lock:<thread_id> <worker_id> NX EX <ttl>`, plus `release(thread_id, worker_id)` using a **check-owner-then-delete** pattern (a small Lua script via `EVAL`, so a worker can never release a lock it doesn't currently own — critical if its own TTL already expired and a different worker has since claimed it). Unit tests against the real local Redis (not a mock) for: claim succeeds when free, claim fails when held, release only succeeds for the actual owner, claim becomes available again after TTL expiry. No adapter changes yet. | auto |
| **PR2** | Telegram adapter calls `mark(thread_id)` on every inbound message, additive only — verify via test that existing dispatch behavior (what gets processed, when) is provably unchanged (same test suite that covers `handle_message` today, still green, plus a new assertion that a mark now exists in Redis after the call). | auto |
| **PR3** | Same for Discord adapter (`_channel_dispatch_lock` path). | auto |
| **PR4** | Discovery: a background task that pops marks (prefer `BLPOP` on a list the adapters `LPUSH` onto over polling a set, per the original design note — near-zero latency, no wasted cycles; state in the PR body which was chosen and why if it ends up different) and attempts `try_claim` before doing anything. Explicitly test the **mark-is-not-a-claim** invariant: a mark for a thread currently held by the existing dispatch lock must not result in a second concurrent handler running — this is the one correctness property the whole plan exists to protect, test it directly, not incidentally. | auto |
| **PR5** | Mark TTL/cleanup — marks that are never claimed (no worker ever available) must not grow Redis unbounded. Pick a cleanup horizon and justify it; verify old unclaimed marks expire. | auto |
| **PR6 — gate: human** | Decision writeup (not code): does this supersede `active_supervision.json`'s per-turn claim signal, or do the two coexist permanently serving different audiences (dashboard freshness vs. mutual-exclusion correctness)? §1 deliberately left this open; resolve it here with reasoning, not by default. | **gate: human** — this is a design-direction call, not a mechanical merge |
| **PR7** (added 2026-10-28, Gary) | **Admin dashboard on sophia.truesight.me** — a Sidekiq-Web-style view of live dispatch state: pending marks, active claims (thread, worker, TTL remaining). **Governor-JWT-gated, same pattern as the existing `media_archive_pipeline.py` dashboard route** — not public/no-auth like `sprint.truesight.me` (that board is a deliberate exception Gary chose for business-level handoff status; this one exposes lower-level operational internals and should not default to that precedent). Read-only — no action buttons (retry/kill a claim) in this PR; that's a separate, more consequential unit if ever wanted. Honest caveat to state in the PR: with one Sophia process, "active" will typically show 0-1 entries — value right now is debugging the mechanism itself while PR2-PR6 are still being built, not a production multi-worker view. | auto |

**UAT:** no human-facing surface — covered by the unit/integration tests specified per row,
all run against the real local Redis instance (already provisioned, not mocked). State plainly
in each PR's report that this tests the mechanism in isolation, not multi-process behavior, per
§0's limitation.

---

## 3. Resume tracker

**RESUME HERE → PR1.**

| Unit | PR opened | Merged (human) | Notes |
|---|---|---|---|
| PR1 — Redis claim primitives + tests | ☐ | ☐ | check-owner-then-delete via Lua `EVAL`, not a plain `DEL` |
| PR2 — Telegram adapter marks | ☐ | ☐ | additive only, prove existing dispatch unchanged |
| PR3 — Discord adapter marks | ☐ | ☐ | same |
| PR4 — discovery + claim attempt | ☐ | ☐ | test the mark-is-not-a-claim invariant directly |
| PR5 — mark TTL/cleanup | ☐ | ☐ | |
| PR6 — active_supervision.json relationship decision | ☐ (writeup) | n/a | **gate: human** |
| PR7 — admin dashboard on sophia.truesight.me | ☐ | ☐ | governor-JWT-gated (not public like sprint.truesight.me), read-only, no action buttons |

---

## 4. Authorization envelope (§5e)

- **Pre-authorized, autonomous, PR-only:** PR1–PR5 — Sophia opens each PR, never self-merges
  (standing rule, reconfirmed throughout the sibling plan's execution the same week).
- **Extra caution, not a hard gate, but call it out explicitly in review:** PR2/PR3 touch the
  live adapter message-receipt path — the one thing that must keep working regardless of
  anything else in this plan. A human reviewing those two PRs specifically should confirm the
  "provably unchanged existing behavior" claim against the actual diff, not just trust the PR
  description.
- **Gated:** PR6 (design-direction decision) and, separately and not yet scoped by this plan at
  all, any future work that actually runs a second Sophia process — that is a new plan, not an
  extension of this one.
