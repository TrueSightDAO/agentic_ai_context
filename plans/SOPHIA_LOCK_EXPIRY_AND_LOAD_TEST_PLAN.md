# Sophia — lock expiry + single-process load test

**Status:** draft, awaiting governor go. **Owner:** Sophia (execution), Envoy (planner/author).
**Origin:** Gary, 2026-10-27, `nelanco-claude` planner session — follow-up to the Sophia
multi-instance/Sidekiq architecture discussion and the mk3.py / PID 2174824 hung-process hunt
earlier the same day.

---

## 0. Why this plan exists, and why it stops where it does

Gary asked for three things, refined in a follow-up message once PR1/PR2's original scope
(staleness-expiry only) was already drafted: (1) give the per-thread/channel lock an **expiry**,
so a dead process can't hold a thread hostage forever; (1b) when a thread genuinely finishes and
has nothing queued, the lock should **release** so a future process could pick up the *next*
message fresh ("this then starts functioning like Sidekiq") — but while a thread has an
in-flight turn, queued messages, or an active auto-advance chain, the **same** process must keep
owning it until truly idle, and this must **not disrupt auto-advance**; and (2) **load-test** the
current single-process Sophia to find how many concurrent turns it can actually sustain before
anything about multi-instance architecture gets built.

This plan does **only those two things**. It deliberately does **not** build the Sidekiq-style
multi-process/multi-instance architecture itself — see
`agentic_ai_context/plans/` (no such plan exists yet) and the prior conversation's own
conclusion: that's only justified once the load test in PR3 shows the current single process is
actually the bottleneck, which is not yet established. Building Phase C (real multi-instance
coordination) before that evidence exists would be the same mistake flagged earlier — solving a
capacity problem that hasn't been shown to exist.

**The lease precedent this plan generalizes, corrected (2026-10-27, Gary caught this):** Envoy's
own `handoffs/active_supervision.json` is **not** a naive flat file under this plan's original
framing — `truesight_autopilot/app/supervision.py` writes it exclusively via
`GitHubClient.commit_file()` → `update_file(sha=existing.sha)`, so GitHub's Contents API itself
enforces compare-and-swap: a conflicting concurrent write is rejected (409), not silently
corrupted or clobbered. **But it has no retry on that rejection** (`claim()`/`release()` just
`logger.debug` and `return False` on failure) — so under real concurrent writers the *loser's*
claim is cleanly lost, not corrupted. That's acceptable today only because writes are
human-paced (a few an hour across Envoy sessions), not because the pattern is safe under load.
**Do not reuse this write path verbatim for Phase C.** A per-turn/per-thread claim under real
concurrency needs either SQLite (WAL mode, if everything stays on one box) or Redis (if it goes
multi-host) — both give atomic compare-and-swap *with* a retry-friendly contract and no
HTTP-round-trip-plus-permanent-git-commit cost per acquire/release. The git-API-backed file is
fine for occasional supervisor bookkeeping; it is the wrong primitive for a hot-path lock.

Gary's point about expiry stands independent of this correction: a lock with no expiry is
exactly the failure mode the mk3.py/PID 2174824 hunt (2026-10-26/27) just found twice in
unrelated code — a process that dies (or hangs) mid-work holds its claim forever, and nothing
ever notices. The fix here is narrower than full lease/heartbeat (no renewal protocol, no
distributed store yet — that's Phase C's job with the SQLite/Redis choice above) — a **staleness
timeout with loud logging on forced release** — because today everything is still one process,
so correctness only needs "don't let a hung turn block its thread forever," not "survive this
process disappearing while another one is alive to take over." That harder problem is Phase C's,
not this plan's.

---

## 1. Pre-flight (§5d — capture everything a PR turn needs to read, here)

**Four existing lock sites in two layers, all in-process, none with any timeout today** (outer
= per-thread chain lock spanning auto-advance; inner = per-turn session lock, nested inside
each iteration of the outer chain):

1. `app/main.py` — `_session_lock(session_id) -> asyncio.Lock`, backed by module-level dict
   `_session_locks: dict[str, asyncio.Lock]`. Docstring (as of 2026-10-26): "Per-session async
   lock... serializes one turn at a time *within* a thread... Requires `--workers 1` to be
   effective (the lock lives in one process)." This is the lock that actually gates **turn
   processing** — the one that matters most, since a stuck turn here is exactly what mk3.py /
   PID 2174824 looked like (CPU-spinning, never returning).
2. `app/telegram_adapter.py:65-75` — `_thread_dispatch_locks: dict[str, threading.Lock]`.
   **Corrected understanding (verified by reading the code, 2026-10-27 — supersedes the
   original PR2 framing below):** this is not just a dispatch-time guard. `_run_turn_with_auto_advance`
   (`telegram_adapter.py:1590+`) holds this lock for the **entire auto-advance chain** — the
   first turn, every queued message drained via `main.py`'s `while queue:` loop (`main.py:3703`),
   and every auto-advance continuation (loop at `telegram_adapter.py:1631-1690`, capped by
   `AUTO_ADVANCE_MAX_TURNS`) — in one unbroken hold, per the comment at `telegram_adapter.py:2920`
   ("which acquires the dispatch lock itself"). It only releases when the loop actually returns:
   no more `advance` signal, the turn cap hit, or a gate. **This means Gary's point-4 requirement
   (same process keeps chaining through queued + auto-advance work without releasing) is already
   true by construction — nothing to build there.** What's net-new is point 1-3: the release point
   (loop returns) *is* the moment the thread is genuinely awaiting user input, but today that's an
   implicit fact about control flow, not an observable event. Making it an explicit, logged
   "thread released / idle" signal at that exact point is the one real gap — it is the hook a
   future Phase C claim-store would attach to, so a different process could claim the thread fresh
   for its next message. No race window exists at this layer: because the whole chain runs under
   one unbroken lock hold, there is never a moment where the thread looks idle between two
   auto-advance turns.
3. `app/discord_adapter.py:128-139` — `_channel_dispatch_locks: dict[str, threading.Lock]` /
   `_channel_dispatch_lock(channel_id)`, same role and same auto-advance-spanning scope as #2 for
   Discord, acquired at `discord_adapter.py:1488`.
4. `app/main.py` — `_session_lock(session_id) -> asyncio.Lock`, backed by module-level dict
   `_session_locks: dict[str, asyncio.Lock]`, acquired at `main.py:4497/4661/4985` for the
   duration of a single turn's handler body (history load through response + queue-drain, per
   the 2026-07-21 fix noted in that code's own comment). This is the **finer-grained** lock —
   nested *inside* each iteration of #2/#3's outer chain — that prevents a second same-thread
   request's history read/write from interleaving with an in-flight turn. Still worth a staleness
   expiry in its own right (PR1) since a single stuck turn is exactly the mk3.py/PID 2174824
   failure shape, but it is not the layer the idle-release signal belongs on.

**Relevant existing guard, do not duplicate:** `AUTO_ADVANCE_MAX_TURNS=8`
(`sophia/SUPERVISOR_LOOP.md` §3) already bounds how many auto-advance turns run unattended in a
thread — that is a *turn-count* cap, unrelated to *lock duration*. A legitimate single turn can
still run long (tool rounds, `git`/`gh` calls, Playwright), and a legitimate full auto-advance
chain can legitimately run as long as 8× that. **The staleness timeout must be generous enough
that it never fires on a real, slow-but-alive turn or chain** — getting this number wrong in the
unsafe direction (too short) recreates exactly the class of bug this plan is trying to prevent,
just inverted (killing live work instead of freeing dead work). Two different constants are
needed, not one:
- **PR1 (inner, per-turn session lock):** base the timeout on the **longest observed single-turn
  duration** from existing session transcripts (`truesight_autopilot_transcript` repo,
  `sessions/*/transcript.md`, timestamp deltas between one user/assistant turn pair).
- **PR2 (outer, per-thread chain lock):** base its timeout on the **longest observed full
  auto-advance chain duration** (sum of consecutive auto-turns in one thread, same transcript
  source) — this will legitimately be several times PR1's number, since it covers up to 8 turns,
  not one. Do not reuse PR1's constant here; that would make PR2 fire while a real multi-unit
  chain is still legitimately running.

Both must be pulled from real transcript data before picking a constant — not guessed.

**Resource baseline (post-cleanup, 2026-10-27):** t3.medium, 3.7GB RAM, disk 42% used / 90GB
free on `/`, swap partially in use. This is **healthy**, unlike the 97%-full state the lock-expiry
discussion started from — PR3's load test is not blocked on more disk cleanup.

**No cross-repo reads beyond what's captured above** — all three lock sites, their call sites,
and the one existing turn-count guard are now on the record; a PR turn should not need to
re-discover any of this live.

✅ **Pre-flight Completeness:** no execution unit requires reading a file/state not already
captured in this pre-flight.

---

## 2. Sequenced plan (§5a — one PR per turn)

| Unit | Scope | Advance |
|---|---|---|
| **PR1** | Add staleness expiry to the **inner, per-turn** `_session_lock()` (`app/main.py`). Wrap the existing `asyncio.Lock` in a small struct carrying `acquired_at` + `holder_session_id` (for logging). On acquire-contention, if the current holder has been held longer than the single-turn timeout (derived per pre-flight §1, not guessed), **force-release with a loud `logger.error`** (include session id, hold duration, and — if available — the stuck turn's last `_live_progress` snapshot, already built for exactly this kind of introspection per `main.py:216-271`), then proceed. Never silently swallow a forced release. Unit test: a lock held past timeout is force-released; a lock held under timeout is NOT. | auto |
| **PR2** | **Outer, per-thread chain lock** (`_thread_dispatch_locks` / `_channel_dispatch_locks`) gets three things, not just staleness: (a) a staleness expiry using the **chain-length** timeout from §1 (several× PR1's constant, since this lock legitimately spans up to `AUTO_ADVANCE_MAX_TURNS` consecutive turns) — same force-release-and-log pattern as PR1, scaled to the right duration; (b) an explicit, structured "thread released / idle" log event emitted exactly where `_run_turn_with_auto_advance` (`telegram_adapter.py:1590+`) naturally returns and drops the lock — today that's just a Python context manager exiting with nothing to mark the moment; this makes it an observable signal, which is the one concrete hook Phase C would need to let a different process claim the thread next, without building Phase C itself; (c) a regression test asserting the lock stays held continuously across a *simulated* multi-unit auto-advance sequence (2-3 fake units in a row) with **no idle-release event fired until the chain actually ends** — this is the test that protects Gary's "should not disrupt auto-advance" requirement, since the failure mode to guard against is releasing early mid-chain, not failing to release at all. Covers both adapters (Telegram + Discord) since the lock shape and `_run_turn_with_auto_advance`-equivalent loop are near-identical; split into two PRs only if the diff gets unwieldy in-turn. | auto |
| **PR3** | **Load test.** A standalone script (not wired into CI) that fires N synthetic concurrent turns against a **non-production** target — do this against `sophia-staging` if one exists, otherwise against production with synthetic session ids that are obviously test data (`loadtest-<uuid>`, per the §5g test-data marking convention) and a cheap no-tool-call prompt so it doesn't burn real GitHub/Sheets writes or DeepSeek spend at scale. Ramp N (e.g. 2, 4, 8, 16...) and record: RSS, CPU, swap, p50/p95 turn latency, error rate at each step, until something degrades. This is the number that answers Gary's actual question — "how many concurrent turns can the *current single process* sustain" — not a multi-process test, since there is no second process yet to test. State that distinction explicitly in the report so the result isn't misread as evidence about multi-instance capacity. | auto |
| **PR4 — gate: human** | Review PR3's results with Gary. Decide: (a) is single-process capacity actually the bottleneck (vs. WIP=2 being a policy choice that was never actually hit), and (b) is Phase C (real multi-process/multi-instance coordination, using the claim-file-plus-discipline precedent from `active_supervision.json` as the starting design per the prior conversation) now justified. This PR produces a decision + short writeup, not code — it is the fork point to either close this plan out or open a new one for Phase C. | **gate: human — always-stop, this is the decision whether to build Phase C at all** |

**UAT:** n/a for PR1/PR2 (backend lock behavior — covered by the unit tests specified in each
row: force-release-when-stale, no-release-when-not-stale, and for PR2 specifically, no-idle-event
mid-chain). PR3 is itself a test; its own output *is* the UAT artifact for PR4's review.

---

## 3. Resume tracker

**RESUME HERE → PR1.**

| Unit | PR opened | Merged (human) | Notes |
|---|---|---|---|
| PR1 — session-lock expiry | ☐ | ☐ | timeout constant must be derived from transcript data per §1, not guessed |
| PR2 — dispatch-lock expiry (both adapters) | ☐ | ☐ | |
| PR3 — load test | ☐ | ☐ | synthetic session ids marked per §5g; report the single-process-only caveat explicitly |
| PR4 — human review + Phase C go/no-go | ☐ (no code) | n/a | **always-stop** |

---

## 3a. Phase C infra prep — done ahead of the gate, on Gary's explicit instruction (2026-10-27)

Gary explicitly chose to provision the Phase C claim-store dependency now, ahead of PR4, as prep
work rather than waiting for the load test. Recorded here so this isn't mistaken for scope creep
on PR1-PR3, and so Phase C's eventual pre-flight doesn't have to re-discover it:

- **Decision: local Redis on Sophia's existing box, not a new EC2** ("approach 2" from the
  options discussed — a dedicated new EC2 is the architecturally cleaner choice *if* Phase C ever
  goes multi-host, since a coordination store living on one of the workers it coordinates is a
  single point of failure; but that's only worth the new-infra cost once multi-host is real).
- **Turned out Redis was already installed and running** on the box (6.0.16, systemd-enabled,
  bound to `127.0.0.1`/`::1` only, previously unauthenticated, 0 keys, nothing else using it —
  confirmed no collectd/webdis/ruby-redis-store actually installed). No new package needed.
- **Hardened for this purpose, 2026-10-27:** `requirepass` set (password in the vault, name
  `PHASE_C_REDIS_PASSWORD`, retrievable via `Vault().get_value("PHASE_C_REDIS_PASSWORD")` the same
  way `DISCORD_BOT_TOKEN` already is — never committed, never printed to chat); `maxmemory 64mb` /
  `maxmemory-policy noeviction` (was previously unlimited with no cap — capped small since this
  will only ever hold tiny claim keys, and `noeviction` means a write fails loudly instead of an
  active lock silently getting evicted under memory pressure); bind unchanged at localhost-only.
- **Not wired into any application code.** This is the dependency sitting ready, nothing more —
  Phase C's own future PRs still need to actually write the claim-store client code against it.
  PR4's go/no-go on Phase C itself is unaffected by this prep being done early.

---

## 4. Authorization envelope (§5e)

- **Pre-authorized, autonomous, PR-only:** PR1–PR3 — Sophia may open each PR without asking
  mid-arc, per the existing standing rule that she never self-merges (confirmed explicitly after
  she offered to self-merge the unrelated vault-key cleanup PR the same day this plan was
  written — see `handoffs/HANDOFF_MANIFEST.md` "Ops: disk + mk3.py cleanup" thread, 2026-10-27).
- **Gated:** merging any of PR1–PR3 to a default branch (human, standard §5c gate) and PR4 in
  full (human decision, not just a merge click).
- **Not in scope for this plan at all:** any Phase C code. A future plan, opened only after PR4
  says go.
