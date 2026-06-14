# Sophia Context-Management Plan — Stop the Context-Poisoning Bricks

**Status:** DRAFT — design approved by Gary 2026-06-13; pending execution
**Owner:** TBD (Sophia handoff candidate)
**Scope:** `truesight_autopilot` (the brain — `app/main.py`, tool loop, session store)
**Precursors this replaces / augments:** #181 (8K tool-result truncation), #189 (token-aware
history trim). Those are *lossy-but-dumb* stopgaps; this plan makes them *lossy-but-smart* with
nothing irretrievable.

---

## 1. Problem

DeepSeek `deepseek-chat` has a **131,072-token input window**. Sophia's content (JSON tool
results, RSA keys, signatures, repeated `[Telegram context…]` prefixes) tokenizes at **~2
chars/token**, so a tool-heavy thread crosses the window fast and the LLM call **overflows →
empty response → brick** (measured: thread 780 reached 275,083 chars = **135,123 tokens = 103%**
of the window). Current mitigations:

- **#181** truncates each tool result to 8K chars — but *drops the tail* (unrecoverable).
- **#189** trims oldest messages to a 90K-token budget — but *deletes whole turns* (unrecoverable),
  and deletion is blind to what's still relevant.

Both stop the brick; neither **conserves** information. This plan does.

## 2. Goal & non-goals

**Goal:** keep the live LLM context safely under the model window **while preserving recoverable
detail and the working set**, so (a) overflow bricks stop, (b) nothing is permanently lost, and
(c) Sophia stays coherent on long threads.

**Non-goals (this phase):** changing the model; embeddings/semantic RAG (keyword recall first,
embeddings are a phase-2 option); multi-tenant; cross-thread memory.

## 3. Design principles

1. **Tool results vs conversation have different lifecycles.** Tool results are *acute,
   disposable, and dense* → externalize them. Conversation (your messages + decisions) is
   *durable and low-volume* → keep it, recall on demand.
2. **Completed sub-tasks: keep the conclusion, not the steps.** A finished 11-tool-call bug-fix
   becomes one line: "Fixed X → PR #N." That's what a human keeps.
3. **Lossy-but-smart > lossy-but-dumb.** Anything dropped from context must be **retrievable**.
4. **Security first.** Externalized detail routinely contains secrets / sheet data / PII →
   **private local store, NOT a git repo.** (Per Gary's original idea #1, but git is the wrong
   substrate here — leak risk + commit-per-tool-call overhead.)
5. **Backstops stay.** The token-trim (#189) and self-heal sanitiser remain as last-resort
   guards behind everything below.

## 4. Architecture — three pillars

### Pillar A — Tool-result externalization (Gary's idea #1, refined)

- **Artifact store:** per-session dir on the box, e.g.
  `/opt/truesight_autopilot/artifacts/<session_md5>/<tool_call_id>.txt`. **Local filesystem, not
  git.** Optional later: periodic sync to private S3 for durability/audit.
- **On every tool result:** write the **full** result to the artifact file; what stays **inline**
  in the transcript is a **compact summary** = `head (≤8K) + extracted key fields (status, rc,
  url, counts) + a retrieval handle (artifact id)`. (Extends today's `_truncate_tool_result` —
  same 8K, but "+ pointer to full" instead of "+ lost tail".)
- **New tool `read_tool_result(artifact_id, offset?, limit?)`** — fetches the full result (or a
  slice) only when the rare case needs the tail.
- **Net:** the densest, most-disposable content stops accumulating, but is never lost.

### Pillar B — Sub-task compaction (the highest-leverage piece)

- When a sub-task **completes** (the model returns a final text answer after a run of tool
  rounds), replace that whole `assistant.tool_calls → tool results` chain with a single
  **compact summary** message: the assistant's own final text for that sub-task + a marker
  `[compacted N tool calls — details in artifacts <ids>]`.
- This **replaces the dumb "drop oldest" trim** with **"compact oldest *completed* sub-task"**.
  Detail is already externalized (Pillar A) → recoverable.
- **Trigger heuristic (v1):** a final-text turn following ≥1 tool round closes a sub-task; compact
  everything from that sub-task's first tool call through its last tool result. Never compact the
  *active* (most-recent) sub-task.

### Pillar C — Recency window + pinned working-set + recall (Gary's idea #2, refined)

- **Default context** = `pinned working-set + recent token-budgeted window`.
- **Pinned working-set** (always in context regardless of age): role tag, system prompt, and a
  small **scratchpad** of the active goal + key decisions (updated per turn). Prevents a decision
  made 60 messages ago from silently falling out of the window.
- **"Really look back" → `search_transcript(query)` tool:** keyword **grep** over the session's
  full on-disk history (`sessions/*.json`) + artifact files; inject only the matched spans.
  Embeddings deferred to phase 2 (only if grep proves too literal).
- Short threads: behavior unchanged (window covers everything).

## 5. Pre-flight (before writing code)

- [ ] Confirm artifact store path + **retention/cleanup** policy (cron to GC files older than N
      days; cap per-session dir size).
- [ ] Confirm token budgets: model window 131,072; history target ≤ 90K (already live via #189);
      reserve for system+tools+8K response.
- [ ] Lock the **compaction trigger** heuristic + the "never compact the active sub-task" rule.
- [ ] Define the **pinned working-set schema** (what fields; how updated — heuristic vs cheap LLM
      pass).
- [ ] Capture **baseline metrics**: log current avg/max session tokens across active threads for a
      day, so we can measure the win.
- [ ] Confirm artifacts dir is **git-ignored** and not world-readable (chmod 700).

## 6. Execution roadmap (sequenced PRs)

Ordered by dependency + risk. Each is an independent, mergeable PR with tests.

| PR  | Title | Depends | Risk | Deploy |
|-----|-------|---------|------|--------|
| **CM0** | Pre-flight: artifacts dir + retention cron + baseline token metrics + `git-ignore` | — | low | none (infra) |
| **CM1** | Tool-result externalization: artifact store + summary-inline + `read_tool_result` tool | CM0 | low | brain restart |
| **CM2** | Sub-task compaction (smart trim replaces blind drop-oldest) | CM1 | **med** | brain restart |
| **CM3** | `search_transcript` tool + pinned working-set scratchpad + recency default | CM0 | low-med | brain restart |
| **CM4** | Observability + tuning: token/compaction metrics, `/chat/context` introspection endpoint, knob defaults | CM1–3 | low | brain restart |

**Rationale for order:** CM1 makes detail recoverable, which is the precondition for CM2 to drop
detail safely. CM3 is independent (recall). CM4 closes the loop with measurement so we can tune
budgets from real data instead of guessing.

### Per-PR detail

- **CM1** — `app/main.py`: extend `_truncate_tool_result` → `_externalize_tool_result(result,
  tool_call_id, session_id)` (writes file, returns summary+handle); add `app/tools/artifact_tools.py`
  with `read_tool_result`. Artifact write is best-effort (failure → fall back to plain 8K
  truncation, never blocks the turn).
- **CM2** — `app/main.py`: `_compact_completed_subtasks(history)` called in the trim path
  *before* the blind token-trim; only fires when over a soft budget; preserves the active
  sub-task; emits a `[compacted …]` user/system note. The #189 token-trim stays as the final
  backstop if compaction isn't enough.
- **CM3** — `app/tools/transcript_tools.py` `search_transcript(query, max_spans)`; a
  `_working_set` scratchpad persisted alongside the session; the context builder pins it +
  applies the recent window.
- **CM4** — log `history_tokens` per turn (already partially there), `compaction_ratio`, artifact
  counts; `/chat/context?session_id=` returns the pinned set + window size + token estimate (also
  surfaces on the vault status panel).

## 7. Checklist

**Global gates (every PR):**
- [ ] Open a PR — **never self-merge** `truesight_autopilot` (human reviews + merges).
- [ ] `python -m py_compile app/main.py` + the full `pytest` green; `ruff check` + `ruff format`
      clean on touched files.
- [ ] Deploy **only when idle** (idle-drain guard #181 + `ssh_run` block #182 are live — use
      `deploy_autopilot`, never a raw restart).
- [ ] Every new behavior behind an **env flag** defaulting to current behavior until soak-verified.
- [ ] No secrets/PII committed — artifacts live on the box's local FS, `chmod 700`, git-ignored.

**Per-pillar:**
- [ ] CM1: artifact write is best-effort; summary carries status + key fields; `read_tool_result`
      round-trips; falls back to plain truncation on store failure.
- [ ] CM2: active sub-task never compacted; compaction is reversible via `read_tool_result`;
      token-trim still fires as backstop; tool-protocol stays valid (`_sanitise` runs after).
- [ ] CM3: short threads unchanged; `search_transcript` returns spans not whole transcript;
      working-set survives a restart.
- [ ] CM4: metrics logged; introspection endpoint authed (governor-only).

## 8. UAT (acceptance — Gary-runnable)

| # | Scenario | Steps | Expected |
|---|----------|-------|----------|
| U1 | Heavy thread no longer bricks | Run a long tool-heavy session (the kind that bricked 780) past ~150K raw chars | Sophia keeps responding; no "empty response"; logged history stays ≤ budget |
| U2 | Tool detail recoverable | After a big `ssh_run`/sheet dump, ask "show me the full output of that last command" | She calls `read_tool_result` and returns the full content from the artifact |
| U3 | Completed work compacts | Finish a multi-step task, then continue chatting | Older tool-chains collapse to one-line outcomes; token count drops; she still knows the outcome |
| U4 | Default = recent only | In a long thread, ask a question answerable from the last few messages | Fast, correct, low token usage — she did not load the whole history |
| U5 | "Really look back" works | Ask "really look back — what did we decide about perch?" | She runs `search_transcript`, surfaces the perch decision, and uses it |
| U6 | Pinned set holds | Make a decision early, fill the thread with unrelated tool work, then act on the early decision | She still honors it (it was pinned, not dropped) |
| U7 | Security | Inspect the artifacts dir | Local only, `chmod 700`, not in any git repo; no tool output in a pushed repo |
| U8 | Graceful degradation | Simulate artifact-store failure (e.g., dir unwritable) | Falls back to plain 8K truncation; turn still completes; warning logged |

## 9. Rollback

Each pillar is behind an env flag (`CONTEXT_EXTERNALIZE`, `CONTEXT_COMPACT`,
`CONTEXT_RECENCY_RECALL`). Flip any off → that pillar reverts to current behavior. The **#189
token-trim and the self-heal sanitiser remain unconditionally** as last-resort backstops, so even
with all flags off the brain cannot overflow.

## 10. Resume tracker

| PR | Status | Notes |
|----|--------|-------|
| CM0 | ☐ not started | |
| CM1 | ☐ not started | |
| CM2 | ☐ not started | |
| CM3 | ☐ not started | |
| CM4 | ☐ not started | |

_Update this table as PRs land (link the PR, flip the box). Keep the active sub-task uncompacted
while iterating._
