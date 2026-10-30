# Loop daemon — background work-state reconciler

**Status:** P0, U1, U2, U3, U4 **SHIPPED and live**. U5 **PARTIAL** (unit installed + enabled on the box, never committed to `deploy/`). U6 **IN PROGRESS** (heartbeat + classification verified; 24h soak still running).
**Corrected 2026-10-30:** this file previously listed P0 as unshipped and described the chat-turn
heartbeat as "never called". Both were stale and cost real time — see §1a for the verified state of
every unit.
**Owner:** Gary Teh (+ Sophia)
**Created:** 2026-10-28
**Goal:** a daemon that runs every 60s, reads the state of every active task, and
answers two questions per Telegram thread / Discord channel:

1. Is Sophia **still busy working** on the task?
2. Is she **idle awaiting a decision**, or just has **nothing to do**?

---

## 1. Verification findings (why this shape, not the obvious one)

Everything below was checked against the live box, not assumed.

| Claim | Verdict |
|---|---|
| Redis is available | ✅ `redis-server` + `redis-cli` on the autopilot box, localhost:6379, password in vault. `app/redis_claim.py` already ships `mark` / `try_claim` / `release` / `owner_of` / `claim_ttl_remaining`, Lua-guarded. |
| Redis tracks live work today | ❌ **No.** `dbsize = 1` — a single `marks` zset with 2 stale entries from Oct 28. `try_claim`/`release`/`owner_of` have **zero production callers**; only `telegram_adapter.py:210` calls `mark()`. The dispatch layer is inert, as its own docstring admits. |
| `mark()` is safe as a liveness signal | ❌ **No.** Plain `zadd`, **no TTL**. A crashed turn looks busy forever. |
| Work state exists somewhere | ✅ In **files**: `data/active_tracks.json`, `sessions/_resume_awaiting.json`, `sessions/_discord_resume_awaiting.json`, `data/thread_goals.jsonl`. |
| Chat turns publish a lease | ✅ **Fixed in P0** (`#561` / `422c92e`). `_register_chat_turn_track()` (`main.py:242`) mirrors in-memory `_active_streams` into `active_tracks.json`, and `_turn_heartbeat.start()` (`main.py:276`) now ticks `last_heartbeat` for the life of the turn, with `_dw_heartbeat()` on unregister (`main.py:292`). |

### The consequence of that missing heartbeat — historical, fixed by P0

Kept for the reasoning trail; **this is no longer a live condition.** Without a heartbeat,
`deploy_watcher.can_deploy()` — which treats `started_at + expected_max_duration_s` as a
lease — would read any turn longer than the lease as expired. That both (a) let
`can_deploy` authorise a restart mid-turn and (b) would have made this daemon report a
perfectly healthy long turn as STALLED.

The second half is now **observed rather than assumed**: this very file was edited inside a
long chat turn while `/loop/status` reported that session as `busy | heartbeat 0s ago` —
no false STALLED.

### 1a. Verified state of each unit (2026-10-30)

Checked on the live box in the session that corrected this file. Nothing below is carried
over from an earlier report.

| Unit | Deliverable | State | Evidence |
|---|---|---|---|
| **P0** | chat-turn lease heartbeat | ✅ **shipped** `#561` / `422c92e` | `main.py:276` `_turn_heartbeat.start()`, `main.py:292` `_dw_heartbeat()`, `tests/test_turn_heartbeat.py` |
| **U1** | pure classifier + parsers | ✅ shipped `#559` | `app/loop_status.py`, `tests/test_loop_status.py` |
| **U2** | daemon loop + Redis publish | ✅ shipped, **running** | `app/loop_daemon.py`, `tests/test_loop_daemon.py`, `truesight-loop-daemon: active` |
| **U3** | read surface `GET /loop/status` | ✅ shipped `#592` / `1f4b85e` | `app/loop_surface.py`, `tests/test_loop_status_route.py` |
| **U4** | alerting, dedupe, flag-gated | ✅ shipped, **delivering** | `app/loop_alerts.py`; live `read=5 planned=1 posted=1 deduped=2` |
| **U5** | systemd unit + deploy wiring | ⚠️ **partial** — installed + enabled, **not committed** | `deploy/` absent from the repo; unit exists only in `/etc/systemd/system` |
| **U6** | live verification | ⏳ **in progress** | ✅ heartbeat 51s (<180s) · ✅ 6 sessions classified · ✅ no false STALLED · ⏳ 24h soak (7.0h elapsed) |

**Why U5 is left partial rather than ticked.** The unit runs and restarts, but its
definition is not in version control — it exists only on one box. Marking that "done"
would hide a service definition with no backup, which is exactly the kind of quiet gap
this document exists to prevent.

---

## 2. State model — five states, one source of truth each

Classification is **per session** (a session == one Telegram thread or Discord channel).
Precedence is top-down; the first match wins.

| # | State | Rule | Authority | Day-one behaviour |
|---|---|---|---|---|
| 1 | **BUSY** | track `status=running` **and** `now − last_heartbeat < expected_max_duration_s` | `active_tracks.json` | silently OK |
| 2 | **STALLED** | track `status=running` **but** lease expired | `active_tracks.json` | **log only** (silent) |
| 3 | **AWAITING** | not busy **and** the thread's last message is in a resume registry | `_resume_awaiting.json` / `_discord_resume_awaiting.json` | silently OK — this is *correct* waiting |
| 4 | **OPEN-GOAL-LOST** | not busy, not awaiting, **but** an open goal exists and `AUTO_ADVANCE=true` | `thread_goals.jsonl` | **LOUD** — the loop dropped it |
| 5 | **IDLE** | none of the above | — | silently OK |

**Only states 2 and 4 are defects.** 3 and 5 are healthy — the daemon must not nag on them.

### Why OPEN-GOAL-LOST is the payoff

The goal loop (A1–A3 merged, deployed dark) writes a per-thread goal and clears it on
completion. If a goal is open and `AUTO_ADVANCE=true` and **nothing is running and nothing
is waiting on a human**, then the auto-advance loop silently lost the thread. That failure
is currently **unfalsifiable** — it looks identical to IDLE. This daemon makes it visible.

Live check at design time: 41 sessions ever seen, **0 open goals** → the daemon starts quiet,
which is the correct day-one baseline.

Live check 2026-10-30 (daemon running): **6 sessions classified** — 3 `awaiting`, 2
`lost_goal`, 1 `busy`. The two `lost_goal` sessions are genuinely dropped threads, and each
has had an hourly nudge posted into its own channel. The payoff described below is
consequence is therefore now **observed on live data**, not merely designed for.

---

## 3. Decisions taken (documented defaults — reversible)

| Decision | Default | Reversible via |
|---|---|---|
| STALLED loudness | **log only** (no chat post) | `LOOP_DAEMON_ALERT_STALLED=true` |
| OPEN-GOAL-LOST loudness | **loud** (post into the thread) | `LOOP_DAEMON_ALERT_LOST_GOAL=false` |
| Poll interval | **60s** | `LOOP_DAEMON_INTERVAL_S` |
| Redis key TTL | **3 × interval** (180s) | derived |
| Daemon on day one | **dark-ish**: publishes to Redis, alerts off | `LOOP_DAEMON_ALERTS` |
| Channel-less alerts (no chat surface) | **report only** — listed under `unmapped`, posted nowhere | set `LOOP_ALERTS_FALLBACK_TARGET` (e.g. `tg:-1003919341801` or `dc:<channel_id>`) ⇒ routed there instead, and counted as `fallback=` |

**On the fallback (why opt-in, not on by default).** Sessions like `…:envoy-go-media-and-wire-20261028`
or handoff keys have no channel of their own, so `target_for_session()` returns `None`. Silently
dumping those into a shared channel the moment the code shipped would have swapped one unclear
situation ("alert went nowhere") for another ("someone else's channel suddenly got noisier"). The
value of the fallback is a **governor choice about where the noise lands**, so it defaults to off and
is set deliberately. Two behaviours worth knowing when reading it:

- A **bare**, unprefixed id is **rejected** — it is exactly the "silently undeliverable" class this
  module's own docstring names as a bug class. A transport prefix (`tg:` / `dc:`) is required.
- A fallback-routed alert keeps its **own** dedupe key (`<session_id>:<state>`), so it dedupes
  per-session as before — not against the shared channel, which would let one session's alert
  silence a different session's.

Rationale for STALLED-silent: with the pre-P0 heartbeat bug, STALLED would have fired on long
healthy turns. P0 is now deployed and **observed clean** (a long real turn reading `busy` with
a live heartbeat, §1a), so the condition to flip `LOOP_DAEMON_ALERT_STALLED=true` is met. The
flag is intentionally still off until the 24h soak completes — flipped deliberately, not
because the original blocker remains.

---

## 4. Architecture — reader, not a new source of truth

The daemon **does not invent state**. It reconciles state the turn loop already emits.
That is the only version that stays honest.

```
        turn loop (main.py)                     files                      loop_daemon (60s)
  ┌──────────────────────────┐        ┌────────────────────┐        ┌────────────────────────┐
  │ _register_chat_turn_track│──write─▶ active_tracks.json│──read──▶  collect()             │
  │ heartbeat (P0 — DONE)    │──write─▶ (last_heartbeat)  │          │   ↓                    │
  │ resume_registry.mark_…   │──write─▶ _resume_awaiting  │──read──▶  classify() [PURE]      │
  │ thread_goal.open/complete│──write─▶ thread_goals.jsonl│──read──▶    ↓                    │
  └──────────────────────────┘        └────────────────────┘        publish() → Redis       │
                                                                      ↓                      │
                                       GET /loop/status (8001) ◀──reads Redis◀── loop:status:*│
```

### Redis keyspace

| Key | Type | TTL | Content |
|---|---|---|---|
| `loop:daemon:heartbeat` | string | 3×interval | epoch of last successful pass — **absence == daemon dead** |
| `loop:status:<session_id>` | hash | 3×interval | `state`, `reason`, `age_s`, `goal`, `updated_ts`, `label` |
| `loop:alerts` | zset | — | dedupe set for loud alerts (`session:state` → last fired epoch) |

TTL matters: a dead daemon's data **self-expires** rather than lying. That is the fix for
exactly the failure mode `mark()` has today.

---

## 5. Execution roadmap — 6 units

Each unit is its own PR, merged before the next starts. No prod deploy at any point;
this is the autopilot service itself, deployed by `deploy_autopilot`.

| Unit | Deliverable | Files | Test gate |
|---|---|---|---|
| **P0** ✅ | Chat turns heartbeat their lease (bug fix) — **shipped `#561` / `422c92e`** | `app/main.py` | `tests/test_turn_heartbeat.py`; verified live: session reads `busy`, heartbeat 0s ago |
| **U1** ✅ | Pure classifier + parsers — **shipped `#559`** | `app/loop_status.py`, `tests/test_loop_status.py` | all 5 states + precedence + malformed input → fail-closed |
| **U2** ✅ | Daemon loop + Redis publish — **shipped, running** | `app/loop_daemon.py`, `tests/test_loop_daemon.py` | fake client: keys + TTL written; dead-source → IDLE not crash |
| **U3** ✅ | Read surface — **shipped #592 / `1f4b85e`** | `app/loop_surface.py`, `app/main.py` (`GET /loop/status`) | endpoint 200 + shape; Redis down → **200 + `degraded`** (deliberate deviation from 503 — see U3 note) |
| **U4** ✅ | Alerting (dedupe, flag-gated) — **shipped and delivering** | `app/loop_alerts.py`, `tests/test_loop_alerts.py`, `tests/test_loop_alerts_quarantine.py` | live counters `read=5 planned=1 posted=1 deduped=2` — one hourly nudge per defect, dedupe honoured |
| **U5** ⚠️ | systemd unit — **installed + enabled, NOT committed** | `deploy/` does not exist; unit lives in `/etc/systemd/system` only | `truesight-loop-daemon` active; `tests/test_loop_daemon_unit.py` covers the write-heartbeat path |
| **U6** ⏳ | Live verification + UAT note | — | ✅ heartbeat 51s (<180s) · ✅ 6 sessions classified · ✅ no false STALLED in a real long turn · ⏳ 24h soak (7.0h elapsed) |

---

## 6. Checklist

### P0 — chat-turn heartbeat — ✅ SHIPPED (`truesight_autopilot#561`, `422c92e`)
- [x] `_dw_heartbeat` imported and called from the turn loop (`main.py:292`)
- [x] heartbeat ticks for the turn's life, not just turn start (`main.py:276`)
- [x] regression test: long turn keeps lease alive (`tests/test_turn_heartbeat.py`)
- [x] regression test: finished turn releases lease
- [x] PR opened + merged
- [x] **verified live 2026-10-30:** long real turn reads `busy`, heartbeat ages from 0s

### U1 — classifier — ✅ SHIPPED (`truesight_autopilot#559`)
- [x] `app/loop_status.py`: `Lease`, `SessionState`, `classify_session`, `summarize`
- [x] parsers: `parse_iso_ts`, `parse_tracks`, `lease_expired`
- [x] tests: BUSY / STALLED / AWAITING / OPEN-GOAL-LOST / IDLE
- [x] tests: precedence (awaiting beats lost-goal; busy beats everything)
- [x] tests: malformed / missing input → fail-closed, never raises
- [x] compileall + ruff + ruff format + pytest green
- [x] PR opened + merged

### U2 — daemon — ✅ SHIPPED and running (`truesight-loop-daemon: active`, 60s cycles)
- [x] `app/loop_daemon.py`: `collect`, `publish_states`, `loop_once`, `main`
- [x] TTL = 3× interval on heartbeat + every status hash (heartbeat observed 51s fresh)
- [x] dedupe zset present (`loop:alerts`)
- [x] tests with fake Redis client (`tests/test_loop_daemon.py`)
- [x] tests: missing file → empty, not exception
- [x] PR opened + merged

### U3 — read surface — ✅ SHIPPED (`truesight_autopilot#592`, `1f4b85e`, live 2026-10-30)
- [x] `GET /loop/status` returns daemon freshness + per-session states
- [x] stale/absent heartbeat → `degraded: true`
- [x] Redis unavailable → **`200` + `degraded: true`** (deviation from the spec's 503 — see note)
- [x] PR opened + merged

**Deviation, documented deliberately.** The roadmap row and the checklist above both specified
`Redis down → 503`. The shipped route returns **200 with `degraded: true` / `healthy: false`**, and
reserves `503` for a route that genuinely cannot answer. Rationale: this surface exists to expose
that the loop is *unhealthy*. Failing closed precisely when Redis is down would hide the one
condition it was built to report, and would page as "endpoint broken" rather than "loop down".
Live-verified shape: `{generated_at, total, counts, defects, daemon, healthy, degraded, error}`;
`tests/test_loop_status_route.py` covers 400 anonymous / 403 non-governor / 200 governor plus the
degraded path.

### U4 — alerts — ✅ SHIPPED and delivering (`app/loop_alerts.py`)
- [x] OPEN-GOAL-LOST posts to thread (flag on by default) — live: `posted=1` per run
- [x] STALLED log-only (flag off by default) — still off, pending 24h soak (see §3)
- [x] dedupe: one alert per (session, state) per hour — live: `deduped=2` of `read=5`
- [x] **channel-less sessions routed to a fallback target** — `LOOP_ALERTS_FALLBACK_TARGET`
      (`truesight_autopilot#608`). Unset by default ⇒ byte-identical to before (reported under
      `unmapped`, still undelivered). Opt-in lever, not a change in default behaviour.
- [ ] PR opened + merged

### U5 — service — ⚠️ PARTIAL: installed and running, **not committed**
- [ ] systemd unit committed — **still open**: `deploy/` does not exist in the repo; the unit
      definition lives only in `/etc/systemd/system` on one box, with no backup
- [x] installed + enabled on box (`truesight-loop-daemon`, `truesight-loop-alerts`,
      `loop-daemon-wake.timer`)
- [x] survives restart, no duplicate instances
- [ ] PR opened + merged (for the unit files)

**Left deliberately unticked.** The gap is the un-versioned service definition, not the
running process. Committing `deploy/truesight-autopilot-loop-daemon.service` is separate work.

### U6 — verification — ⏳ IN PROGRESS (3 of 5 gates met)
- [x] `loop:daemon:heartbeat` age < 180s — **51s** measured 2026-10-30
- [x] ≥1 real session classified — **6** sessions: 3 `awaiting`, 2 `lost_goal`, 1 `busy`
- [x] no false STALLED during a real long turn — this document was edited inside a long
      turn while its session read `busy`, heartbeat 0s ago
- [ ] 24h soak with no exceptions in journal — **7.0h elapsed**, soak still running
- [ ] UAT note written

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| `_discord_resume_awaiting.json` has **2430 entries, no GC** → almost every Discord channel classifies AWAITING, drowning the signal | U2 classifies awaiting by *freshest* entry only, and a GC sweep (age > 7d) is filed as a follow-up in `OPEN_FOLLOWUPS.md` |
| Classifier becomes a second source of truth | It reads files only; it never writes them |
| Daemon dies silently | `loop:daemon:heartbeat` with TTL → absence is visible; `/loop/status` reports `degraded` |
| 60s polling cost | Four small file reads + a handful of Redis writes per minute — negligible on t3.medium |

## 8. Explicitly out of scope

- No production / beta site deploy — this is the autopilot service only.
- No TDG, no money movement.
- No auto-*action* on STALLED (the daemon reports; it does not kill or retry turns).
