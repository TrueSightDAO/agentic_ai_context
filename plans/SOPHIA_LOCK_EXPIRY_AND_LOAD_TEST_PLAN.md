# Sophia — lock expiry + single-process load test

**Status:** draft, awaiting governor go. **Owner:** Sophia (execution), Envoy (planner/author).
**Origin:** Gary, 2026-10-27, `nelanco-claude` planner session — follow-up to the Sophia
multi-instance/Sidekiq architecture discussion and the mk3.py / PID 2174824 hung-process hunt
earlier the same day.

---

## 0. Why this plan exists, and why it stops where it does

Gary asked for two things: (1) give the per-thread/channel lock an **expiry**, so a dead
process can't hold a thread hostage forever, and (2) **load-test** the current single-process
Sophia to find how many concurrent turns it can actually sustain before anything about
multi-instance architecture gets built.

This plan does **only those two things**. It deliberately does **not** build the Sidekiq-style
multi-process/multi-instance architecture itself — see
`agentic_ai_context/plans/` (no such plan exists yet) and the prior conversation's own
conclusion: that's only justified once the load test in PR3 shows the current single process is
actually the bottleneck, which is not yet established. Building Phase C (real multi-instance
coordination) before that evidence exists would be the same mistake flagged earlier — solving a
capacity problem that hasn't been shown to exist.

**The lease precedent this plan generalizes:** Envoy's own `handoffs/active_supervision.json` is
a claim file with no expiry — it works today because every supervisor is disciplined about
reading it before acting. Gary's point is sharper: a lock with no expiry is exactly the failure
mode the mk3.py/PID 2174824 hunt (2026-10-26/27) just found twice in unrelated code — a process
that dies (or hangs) mid-work holds its claim forever, and nothing ever notices. The fix here is
narrower than full lease/heartbeat (no renewal protocol, no distributed store) — a **staleness
timeout with loud logging on forced release** — because today everything is still one process,
so correctness only needs "don't let a hung turn block its thread forever," not "survive this
process disappearing while another one is alive to take over." That harder problem is Phase C's,
not this plan's.

---

## 1. Pre-flight (§5d — capture everything a PR turn needs to read, here)

**Three existing lock sites, all in-process, none with any timeout today:**

1. `app/main.py` — `_session_lock(session_id) -> asyncio.Lock`, backed by module-level dict
   `_session_locks: dict[str, asyncio.Lock]`. Docstring (as of 2026-10-26): "Per-session async
   lock... serializes one turn at a time *within* a thread... Requires `--workers 1` to be
   effective (the lock lives in one process)." This is the lock that actually gates **turn
   processing** — the one that matters most, since a stuck turn here is exactly what mk3.py /
   PID 2174824 looked like (CPU-spinning, never returning).
2. `app/telegram_adapter.py:65-75` — `_thread_dispatch_locks: dict[str, threading.Lock]`,
   acquired around inbound-message dispatch (not the turn itself) to prevent double-dispatch of
   the same Telegram forum topic.
3. `app/discord_adapter.py:128-139` — `_channel_dispatch_locks: dict[str, threading.Lock]` /
   `_channel_dispatch_lock(channel_id)`, same role as #2 for Discord, acquired at
   `discord_adapter.py:1488`.

**Relevant existing guard, do not duplicate:** `AUTO_ADVANCE_MAX_TURNS=8`
(`sophia/SUPERVISOR_LOOP.md` §3) already bounds how many auto-advance turns run unattended in a
thread — that is a *turn-count* cap, unrelated to *lock duration*. A legitimate single turn can
still run long (tool rounds, `git`/`gh` calls, Playwright). **The staleness timeout in PR1/PR2
must be generous enough that it never fires on a real, slow-but-alive turn** — getting this
number wrong in the unsafe direction (too short) recreates exactly the class of bug this plan is
trying to prevent, just inverted (killing live work instead of freeing dead work). Recommend
basing the timeout on the **longest observed legitimate turn duration**, not a guess — PR1 must
pull that number from existing session transcripts (`truesight_autopilot_transcript` repo,
`sessions/*/transcript.md`, timestamp deltas between a user turn and its final assistant message)
before picking a constant.

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
| **PR1** | Add staleness expiry to `_session_lock()` (`app/main.py`). Wrap the existing `asyncio.Lock` in a small struct carrying `acquired_at` + `holder_session_id` (for logging). On acquire-contention, if the current holder has been held longer than the timeout (derived per pre-flight, not guessed), **force-release with a loud `logger.error`** (include session id, hold duration, and — if available — the stuck turn's last `_live_progress` snapshot, already built for exactly this kind of introspection per `main.py:216-271`), then proceed. Never silently swallow a forced release. Unit test: a lock held past timeout is force-released; a lock held under timeout is NOT. | auto |
| **PR2** | Same staleness treatment for `_thread_dispatch_locks` (telegram_adapter.py) and `_channel_dispatch_locks` (discord_adapter.py). These guard dispatch, not the turn itself, so their timeout should be much shorter than PR1's (dispatch is supposed to be fast; if it isn't, something is already wrong). Can land as one PR covering both adapters since the lock shape is near-identical — split only if the diff gets unwieldy in-turn. | auto |
| **PR3** | **Load test.** A standalone script (not wired into CI) that fires N synthetic concurrent turns against a **non-production** target — do this against `sophia-staging` if one exists, otherwise against production with synthetic session ids that are obviously test data (`loadtest-<uuid>`, per the §5g test-data marking convention) and a cheap no-tool-call prompt so it doesn't burn real GitHub/Sheets writes or DeepSeek spend at scale. Ramp N (e.g. 2, 4, 8, 16...) and record: RSS, CPU, swap, p50/p95 turn latency, error rate at each step, until something degrades. This is the number that answers Gary's actual question — "how many concurrent turns can the *current single process* sustain" — not a multi-process test, since there is no second process yet to test. State that distinction explicitly in the report so the result isn't misread as evidence about multi-instance capacity. | auto |
| **PR4 — gate: human** | Review PR3's results with Gary. Decide: (a) is single-process capacity actually the bottleneck (vs. WIP=2 being a policy choice that was never actually hit), and (b) is Phase C (real multi-process/multi-instance coordination, using the claim-file-plus-discipline precedent from `active_supervision.json` as the starting design per the prior conversation) now justified. This PR produces a decision + short writeup, not code — it is the fork point to either close this plan out or open a new one for Phase C. | **gate: human — always-stop, this is the decision whether to build Phase C at all** |

**UAT:** n/a for PR1/PR2 (backend lock behavior — covered by the unit tests specified in each
row: force-release-when-stale, no-release-when-not-stale). PR3 is itself a test; its own output
*is* the UAT artifact for PR4's review.

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

## 4. Authorization envelope (§5e)

- **Pre-authorized, autonomous, PR-only:** PR1–PR3 — Sophia may open each PR without asking
  mid-arc, per the existing standing rule that she never self-merges (confirmed explicitly after
  she offered to self-merge the unrelated vault-key cleanup PR the same day this plan was
  written — see `handoffs/HANDOFF_MANIFEST.md` "Ops: disk + mk3.py cleanup" thread, 2026-10-27).
- **Gated:** merging any of PR1–PR3 to a default branch (human, standard §5c gate) and PR4 in
  full (human decision, not just a merge click).
- **Not in scope for this plan at all:** any Phase C code. A future plan, opened only after PR4
  says go.
