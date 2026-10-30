# Loop daemon — background work-state reconciler

**Status:** U1/U2/U3 SHIPPED — U3 (`GET /loop/status`) live on :8001 since 2026-10-30. P0, U4, U5, U6 still open.
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
| Chat turns publish a lease | ⚠️ **Partially — buggy.** `_register_chat_turn_track()` (`main.py:242`) mirrors in-memory `_active_streams` into `active_tracks.json` precisely so another process can see it. But `deploy_watcher.heartbeat()` is **never called** for chat turns → `last_heartbeat` frozen at `started_at`. |

### The consequence of that missing heartbeat

`deploy_watcher.can_deploy()` treats `started_at + expected_max_duration_s` as a lease.
With no heartbeat, **any chat turn longer than the lease reads as expired** — which both
(a) lets `can_deploy` authorise a restart mid-turn, and (b) would make this daemon report
a perfectly healthy long turn as STALLED. **This is prerequisite P0.**

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

---

## 3. Decisions taken (documented defaults — reversible)

| Decision | Default | Reversible via |
|---|---|---|
| STALLED loudness | **log only** (no chat post) | `LOOP_DAEMON_ALERT_STALLED=true` |
| OPEN-GOAL-LOST loudness | **loud** (post into the thread) | `LOOP_DAEMON_ALERT_LOST_GOAL=false` |
| Poll interval | **60s** | `LOOP_DAEMON_INTERVAL_S` |
| Redis key TTL | **3 × interval** (180s) | derived |
| Daemon on day one | **dark-ish**: publishes to Redis, alerts off | `LOOP_DAEMON_ALERTS` |

Rationale for STALLED-silent: the heartbeat bug (P0) means STALLED would otherwise fire on
long healthy turns. Silence until P0 is deployed + observed clean, then flip.

---

## 4. Architecture — reader, not a new source of truth

The daemon **does not invent state**. It reconciles state the turn loop already emits.
That is the only version that stays honest.

```
        turn loop (main.py)                     files                      loop_daemon (60s)
  ┌──────────────────────────┐        ┌────────────────────┐        ┌────────────────────────┐
  │ _register_chat_turn_track│──write─▶ active_tracks.json│──read──▶  collect()             │
  │ heartbeat (P0 — ADD)     │──write─▶ (last_heartbeat)  │          │   ↓                    │
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
| **P0** | Chat turns heartbeat their lease (bug fix) | `app/main.py` | unit test asserting `heartbeat()` called during a turn; `can_deploy` respects a live long turn |
| **U1** | Pure classifier + parsers | `app/loop_status.py`, `tests/test_loop_status.py` | all 5 states + precedence + malformed input → fail-closed |
| **U2** | Daemon loop + Redis publish | `app/loop_daemon.py`, `tests/test_loop_daemon.py` | fake client: keys + TTL written; dead-source → IDLE not crash |
| **U3** ✅ | Read surface — **shipped #592 / `1f4b85e`** | `app/loop_surface.py`, `app/main.py` (`GET /loop/status`) | endpoint 200 + shape; Redis down → **200 + `degraded`** (deliberate deviation from 503 — see U3 note) |
| **U4** | Alerting (dedupe, flag-gated, off) | `app/loop_daemon.py` | dedupe test: same defect twice in a row → one alert |
| **U5** | systemd unit + deploy wiring | `deploy/truesight-autopilot-loop-daemon.service`, docs | unit starts, writes heartbeat, restarts clean |
| **U6** | Live verification + UAT note | — | heartbeat < 180s old, states present, 24h soak |

---

## 6. Checklist

### P0 — chat-turn heartbeat
- [ ] `_dw_heartbeat` imported and called from the turn loop
- [ ] heartbeat on *every* tool round, not just turn start
- [ ] regression test: long turn keeps lease alive
- [ ] regression test: finished turn releases lease
- [ ] PR opened + merged

### U1 — classifier
- [ ] `app/loop_status.py`: `Lease`, `SessionState`, `classify_session`, `summarize`
- [ ] parsers: `parse_iso_ts`, `parse_tracks`, `lease_expired`
- [ ] tests: BUSY / STALLED / AWAITING / OPEN-GOAL-LOST / IDLE
- [ ] tests: precedence (awaiting beats lost-goal; busy beats everything)
- [ ] tests: malformed / missing input → fail-closed, never raises
- [ ] compileall + ruff + ruff format + pytest green
- [ ] PR opened + merged

### U2 — daemon
- [ ] `app/loop_daemon.py`: `collect`, `publish_states`, `loop_once`, `main`
- [ ] TTL = 3× interval on heartbeat + every status hash
- [ ] dedupe zset present
- [ ] tests with fake Redis client
- [ ] tests: missing file → empty, not exception
- [ ] PR opened + merged

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

### U4 — alerts
- [ ] OPEN-GOAL-LOST posts to thread (flag on by default)
- [ ] STALLED log-only (flag off by default)
- [ ] dedupe: one alert per (session, state) per hour
- [ ] PR opened + merged

### U5 — service
- [ ] systemd unit committed
- [ ] installed + enabled on box
- [ ] survives restart, no duplicate instances
- [ ] PR opened + merged

### U6 — verification
- [ ] `loop:daemon:heartbeat` age < 180s
- [ ] ≥1 real session classified
- [ ] no false STALLED during a real long turn
- [ ] 24h soak with no exceptions in journal
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
