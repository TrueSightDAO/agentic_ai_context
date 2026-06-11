# Sophia — Live Progress Introspection — Execution Roadmap (handoff to Sophia)

**Status as of 2026-06-11:** handed off to Sophia — parked GO-ready (see HANDOFF_MANIFEST.md)
**Repo under change:** `truesight_autopilot` (Sophia's OWN codebase)
**Designed by:** Gary Teh + Claude · **Implemented by:** Sophia, human-merged

> ⛔ **Own-repo gate:** open PRs only, **NEVER self-merge** `truesight_autopilot` PRs (a human
> reviews + merges). `Generated-by: Sophia (TrueSight Autopilot)` trailer on every commit.

> **RESUME HERE:** PR1 — the `_live_progress` record + richer busy-ack.

---

## 1. Why

When Gary sends a message into a thread where Sophia is mid-turn, the per-topic dispatch lock
queues it and she replies with a canned *"📥 Got it — queued, I'll get to it right after."* That
ack is blind to what she's actually doing. The running turn already streams its activity (the
adapter live-edits a status message: 🔄 → 🔧 open fix pr …), but a *second* message can't see
any of it. This makes that in-flight activity **introspectable**, so a "how's progress?" gets a
real answer.

## 2. Design

A per-session **live-progress record** the executing turn updates as it works; the listening
handler reads it (read-only) and reports.

```
_live_progress[session_id] = {
  instruction, started_at, round, elapsed,
  current_tool, current_arg,           # e.g. ssh_run / "git checkout main"
  done: ["read_repo_file", "ssh_run ×2", "open_fix_pr → PR#160"],
  queued_behind,
}
```

**Invariants:**
- **Read-only + race-free.** Under `--workers 1` the read is a plain dict access on the same
  event loop — atomic relative to the turn's writes. The introspection never touches the running
  turn, only observes it.
- **A progress query must NOT take the dispatch lock** — else the question about the busy turn
  blocks *behind* that very turn. It's a read-only side path that bypasses the lock.
- **Intent classification biases toward queuing.** Ambiguous "status vs instruction" → treat as
  an instruction (queue it). Never silently drop real work as a misread status check. Only short,
  clearly status-y phrases get the instant-answer path.
- **Templated, not LLM.** The snapshot is rendered from the structured record — instant + free.
  (An LLM natural-language summary is a possible later add for "give me detail.")

## 3. Sequenced plan (open PR, human merges)

### PR1 — `_live_progress` record + richer busy-ack
| Step | Description |
|------|-------------|
| 1 | `_live_progress: dict[session_id, dict]` in `app/main.py`. `_run_tool_round_loop` updates it at each round + tool-call start/done (current_tool/current_arg, round, append to done); clear it when the turn ends (success or error). |
| 2 | Helper `_render_progress(session_id) -> str | None` — templated one/two-line snapshot (instruction excerpt, round, elapsed, current tool + arg, done-so-far, queued_behind). Returns None if nothing running. |
| 3 | `telegram_adapter._ack_queued_if_busy` folds the snapshot into the ack: *"📥 Queued. Right now I'm ~2m into 'fix the import' — round 3, running `ssh_run` (git checkout main); done: read 3 files, opened PR#160."* |
| 4 | Tests: record populated across a stubbed tool loop; cleared on end; `_render_progress` formats the fields; ack includes the snapshot when busy, plain when idle. |

### PR2 — Progress-query → immediate answer (lock-bypassing)
| Step | Description |
|------|-------------|
| 1 | Read-only progress path on the app (e.g. `GET /chat/progress` keyed by session) returning `_render_progress` — does **not** acquire the per-session lock. |
| 2 | Adapter: a lightweight classifier for short status-y phrases ("how's it going", "progress?", "status", "where are you", "done yet?"). On a busy thread + a match → call the progress path and reply immediately (no queue); else → queue with the PR1 richer ack. |
| 3 | Tests: status phrase on a busy thread → immediate snapshot, not queued, no lock wait; a real instruction (even during a busy turn) → still queued; ambiguous → queued; status query with nothing running → graceful "nothing running right now". |

## 4. UAT — operator acceptance (run in Telegram)
- **U1** While a turn runs, send a new instruction → the ack now carries the live snapshot (current tool, round, elapsed, done-so-far, queue depth).
- **U2** While a turn runs, ask "how's progress?" → **immediate** templated snapshot, **not** queued, no lock wait.
- **U3** A real instruction sent during a busy turn is **still queued** (not misread as a status query).
- **U4** A progress query with nothing running → graceful "nothing running right now."
- **U5** The introspection never slows or interferes with the executing turn (read-only).

**Completion gate:** PRs human-merged (Sophia opens, never self-merges); U1–U5 pass.

## 5. Rollout
Deploy via the targeted path (`git checkout -B main origin/main` on the box, **no `git clean`**),
restart `truesight-autopilot`, run U1–U5.

## 6. Resume tracker
| Unit | PR opened | Merged (human) | Deployed | UAT |
|------|-----------|----------------|----------|-----|
| PR1 — live-progress record + richer ack | ☐ | ☐ | ☐ | U1 |
| PR2 — progress-query immediate answer | ☐ | ☐ | ☐ | U2–U5 |

> **RESUME HERE:** PR1 — `_live_progress` record + `_render_progress` + richer `_ack_queued_if_busy`.
> Open PRs; **do not self-merge** (human reviews). Report progress in the handoff topic.

## 7. Dependency notes
Builds directly on the shipped per-topic concurrency work (the dispatch lock + `_ack_queued_if_busy`
in `app/telegram_adapter.py`) and the per-turn report (`tool_trace` in `_run_tool_round_loop`,
`app/main.py`). Pairs with `list_followups` as a consistent "here's my current state" surface.
