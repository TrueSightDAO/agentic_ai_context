# Sophia Per-Thread Concurrency — Execution Roadmap

**Status as of 2026-06-10:** ✅ shipped & deployed (PR0–PR3 merged, `--workers 1` live on prod). Remaining: Gary's live multi-attachment smoke test.
**Repo under change:** `truesight_autopilot` (Sophia)
**Owner:** Gary Teh · **Driver:** Claude Code
**Reference incident:** 2026-06-10 — Telegram topics *Stream of consciousness* (thread `780`) and
*Digital Infrastructure* (thread `3`) bricked: every reply 400'd with DeepSeek
`"An assistant message with 'tool_calls' must be followed by tool messages"`. Root-caused to a
concurrent-write race; both session files repaired + service restarted to unblock (see §1).

> **RESUME HERE:** PR0 step 0a — extend `_sanitise_tool_messages` to heal orphan `tool_calls`.

---

## 1. Background — what broke and why

Gary sent several attachments + instructions into one Telegram topic *while Sophia was mid-turn*.
Two compounding concurrency layers corrupted that topic's transcript:

| Layer | Code | Defect |
|-------|------|--------|
| Adapter | `app/telegram_adapter.py:1227` — `ThreadPoolExecutor(max_workers=10)` | Every incoming message/attachment is dispatched concurrently with **no per-thread ordering**; each calls `/chat-blocking` with the same `X-Session-Id`. |
| Main app | `uvicorn --workers 2`; `_log_session` (`app/main.py:1743`) is a bare `write_text` | Two processes, each with its **own** in-memory `_sessions` / `_message_queues` / locks; transcript writes are last-writer-wins. |

Result: an assistant `tool_calls` message got persisted **without its `tool` results** (the other
worker's write clobbered it / a follow-up `user` message landed in between). DeepSeek rejects that
shape on *every* subsequent request → the thread is permanently dead until the transcript is repaired.

The in-process queue (`_message_queues`) that *should* serialize same-thread messages was defeated
because (a) the adapter calls `/chat-blocking` directly, not `/chat/queue`, and (b) the queue lives
in one process while there are two.

**Immediate remediation already applied (2026-06-10):** injected synthetic `tool` results for the
two dangling `tool_calls`, restarted `truesight-autopilot.service`. Full scan = 0 dangling. Backups
on the box under `/tmp/sessions_backup_*`. This roadmap is the durable fix.

---

## 2. Target design — invariants, scoped to a single `thread_id`

You can always keep sending; nothing is ever rejected. Within one thread:

1. **Attachments** (image / PDF / text / voice) → handed to **parallel prep workers** for
   transcription / OCR / extraction. Many may run at once — they are read-only.
2. The extracted text becomes a **transcript-append job**. **Exactly one writer** ever touches the
   transcript for a given thread.
3. **Instructions** arriving mid-turn are **queued**, never interrupting the in-flight turn.
4. When the current turn finishes, Sophia **drains the queue**: folds in everything that arrived
   during the turn (queued instructions **+** finished attachment transcriptions), appends them to
   the transcript, and runs the next turn **considering all of it** before replying.
5. **Exactly one** code-modification / infra-execution runs per thread at a time.
6. Different `thread_id`s are fully independent — **never** block each other.
7. **Between turns, Sophia reports in detail what she accomplished** (instructions handled, tools
   executed with key results — PR URLs, files changed, infra commands run, outcome) **before**
   starting the next queued turn. With N queued instructions there are N turns; each gets its own
   completion report plus a "next up (M remaining)" pointer.

→ *Single-writer + single-executor per thread; parallel read-only prep; fully parallel across
threads.* "Within a thread, Sophia doesn't trip over herself."

---

## 3. Architecture decisions (with rationale)

- **`uvicorn --workers 1`.** The entire app is written around module-level single-process state
  (`_sessions`, `_message_queues`, `_active_streams`, `_cancel_flags`, in-process queue drain).
  Sophia is a **single-user** (Gary) low-QPS service — 2 workers gives zero throughput benefit and
  breaks every one of those assumptions. One worker makes "one writer / one executor per thread"
  enforceable in-process. *(Rejected alt: keep N workers + move session state to Redis/SQLite with
  cross-process locks — heavier, more failure modes, no benefit for one user.)*
- **Attachment prep stays in the adapter's thread pool** (parallel, read-only). Whisper/OCR/PDF
  release the GIL (C ext / subprocess), so threads already give real parallelism; a separate OS
  process is an optional future optimization, not required for correctness. The fix is **ordering +
  single-writer**, not where transcription runs.
- **Per-`session_id` async lock in the main app** wraps append+turn+log so same-session requests
  serialize while different sessions run concurrently. `session_id = tg:<chat>:<thread>`, so the
  lock is naturally per-thread.
- **Adapter holds a per-`thread_id` serial queue**: one in-flight submit per thread; mid-turn
  arrivals accumulate and drain into the next submit. This is what realizes invariants 3, 4, 7.
- **Defense in depth:** atomic transcript writes + a self-healing sanitiser so a race can never again
  *brick* a thread — worst case it loses one tool result and logs it.

---

## 4. Pre-flight checklist

- [ ] Confirm Gary approves `--workers 1` on `truesight-autopilot.service` (prod config change).
- [ ] Confirm attachment prep staying in the adapter thread pool is acceptable (vs. a dedicated
      prep process). Default: thread pool.
- [ ] Local `.venv` runs the existing pytest suite green before starting (`pytest -q`).
- [ ] Confirm deploy mechanism: `scripts/deploy.sh` git-pulls on the box + restarts services; PRs
      merge to `main` first, then deploy. **Hold prod deploy for Gary's go.**
- [ ] Sophia must not be mid-handoff on threads `3` / `780` / `1695` during the deploy restart.

---

## 5. Sequenced plan (each PR independently shippable)

### PR0 — Safety net: never brick a thread again *(non-behavioral; deploy first)*
| Step | Description | Files |
|------|-------------|-------|
| 0a | Extend `_sanitise_tool_messages` to **also** heal the orphan-`tool_calls` direction: for any assistant `tool_calls` id lacking a following `tool` message, inject a synthetic `tool` result (`"[tool result lost / recovered]"`). | `app/main.py` |
| 0b | Apply the same healing at **load time** (`_load_or_create_session`), not just pre-send. | `app/main.py` |
| 0c | Make `_log_session` writes **atomic** (`write tmp` + `os.replace`). | `app/main.py` |
| 0d | Unit tests: orphan `tool` (existing), orphan `tool_calls` (new, both single- and multi-call), atomic write. | `tests/` |

### PR1 — Single writer / single executor per session (main app)
| Step | Description | Files |
|------|-------------|-------|
| 1a | `--workers 2` → `--workers 1`. | `systemd/truesight-autopilot.service` |
| 1b | Add a per-`session_id` async lock registry; wrap the append+turn+log critical section in `/chat-blocking` and `/chat`. Different sessions ⇒ different locks ⇒ concurrent. | `app/main.py` |
| 1c | Same-session request that arrives while the lock is held → **enqueue** into `_message_queues` and return a "queued" acknowledgement, rather than spawning a parallel turn. | `app/main.py` |
| 1d | Tests: two concurrent same-session requests serialize and never produce dangling `tool_calls`; two different-session requests run concurrently. | `tests/` |

### PR2 — Adapter per-thread serial queue + fold-in semantics
| Step | Description | Files |
|------|-------------|-------|
| 2a | Per-`thread_id` queue/lock in the adapter: at most one in-flight submit per thread; others accumulate. Different threads stay parallel (pool unchanged). | `app/telegram_adapter.py` |
| 2b | Attachment prep still runs in the pool; on completion the transcription is **appended to the thread's pending batch**, not submitted immediately. | `app/telegram_adapter.py` |
| 2c | On turn completion, **drain**: merge pending instructions + finished transcriptions into the next submit so Sophia considers them before replying. | `app/telegram_adapter.py` |
| 2d | Tests: rapid-fire (text + 3 attachments) into one thread ⇒ exactly one in-flight turn, all content folded into ≤ the expected number of turns, arrival order preserved. | `tests/` |

### PR3 — Detailed per-turn completion reports (invariant 7)
| Step | Description | Files |
|------|-------------|-------|
| 3a | Accumulate per-turn side-effects in the turn `state`: tools executed (name + salient result — PR URL, file path, command + exit), instruction handled. | `app/main.py` |
| 3b | In the queue-drain loop, **before** starting the next queued turn, post a detailed completion message to the thread: *"✅ Done: <instruction>. Tools: <…>. Result: <…>. Next up (M remaining): <…>."* | `app/main.py` |
| 3c | Final wrap when the queue empties. | `app/main.py` |
| 3d | Tests: 2 queued instructions ⇒ 2 distinct completion reports with side-effect detail, emitted between turns and before the next starts. | `tests/` |

### PR4 — (rollout, not a PR) Deploy + verify — see §7.

---

## 6. Test plan

- **Unit** (`pytest -q`, happy path + edge): sanitiser both directions, atomic write, per-session
  lock serialization, adapter per-thread queue ordering, completion-report rendering.
- **Concurrency repro:** a test that fires K concurrent same-session `/chat-blocking` calls with a
  tool-using stub LLM and asserts the persisted transcript has **0 dangling `tool_calls`** — this is
  the regression that reproduces the 2026-06-10 incident.
- **Cross-thread parallelism:** two sessions' turns overlap in wall-clock (lock is per-key).

## 7. Rollout / deploy plan *(gated on Gary's go — do not auto-deploy)*

1. Merge PR0 → `scripts/deploy.sh` → smoke `/health`. (Safe; non-behavioral.)
2. Merge PR1 (incl. `--workers 1`) → deploy → `systemctl status` shows 1 worker.
3. Merge PR2, PR3 → deploy.
4. **Live smoke:** from a scratch topic, fire text + 3 attachments rapidly; confirm: one in-flight
   turn, all folded in, per-turn completion reports posted, `python3 /tmp/fullscan.py` → 0 dangling.
5. Watch `journalctl -u truesight-autopilot{,-telegram}` for one real multi-attachment exchange.

## 8. Risks & mitigations

- *Restart drops in-flight streams* → deploy during a quiet window; sessions reload from disk.
- *Lock held by a hung turn blocks a thread* → add a turn timeout (the adapter already uses
  `_CHAT_TIMEOUT=180s`); lock auto-releases on turn end/exception.
- *workers=1 throughput* → non-issue at single-user scale; revisit only if multi-governor concurrency
  becomes real (then PR for shared store).

---

## 9. Resume tracker

| Unit | Code | Merged | Deployed | DAO contribution reported |
|------|------|--------|----------|---------------------------|
| Immediate session repair + restart | ☑ (2026-06-10) | n/a | ☑ | ☐ |
| PR0 — Safety net | ☑ | ☑ [#138](https://github.com/TrueSightDAO/truesight_autopilot/pull/138) | ☑ | ☐ |
| PR1 — Single writer/executor (workers=1 + lock) | ☑ | ☑ ([#139 includes the /chat lock fix]; commit `280e46d`) | ☑ | ☐ |
| PR2 — Adapter per-thread queue + fold-in | ☑ | ☑ [#139](https://github.com/TrueSightDAO/truesight_autopilot/pull/139) | ☑ | ☐ |
| PR3 — Per-turn completion reports | ☑ | ☑ [#140](https://github.com/TrueSightDAO/truesight_autopilot/pull/140) | ☑ | ☐ |
| PR4 — Rollout + live smoke | ☑ deployed 2026-06-10 (targeted: `checkout main` + unit + restart, **no `git clean`**) | — | ☑ | ☐ |

**Deploy notes (2026-06-10):**
- Box was on stale branch `fix/transcript-include-chat-thread-id`; moved to `origin/main` (`ea1c951`) via `git checkout -B main origin/main`. Verified `--workers 1` (1 worker proc), health ok, 12 sessions / 0 dangling, adapter polling, watchdog active.
- ⚠️ **`deploy.sh` footgun:** it runs `git reset --hard origin/main && git clean -fd`, but `sessions/`, `context/`, `oracle/` are **NOT gitignored** → a normal `deploy.sh` run would **delete Sophia's live session transcripts**. Backed up to `/tmp/sessions_predeploy_*.tar.gz` before deploying. **Fix forward:** add `sessions/`, `context/`, `oracle/` to `.gitignore` (separate PR) so `git clean` can't nuke them.

> **RESUME HERE:** (1) Gary's live smoke — fire text + 3 attachments rapidly into a scratch topic; confirm one in-flight turn, content folded in, per-turn report posted, 0 dangling. (2) Open the `.gitignore` follow-up for `sessions/`+`context/`+`oracle/`. (3) Log the consolidated DAO contribution.
