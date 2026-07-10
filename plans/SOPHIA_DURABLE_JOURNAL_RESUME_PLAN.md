# Sophia Durable Journal + Checkpoint-Resume Loop — Execution Plan

**Handoff:** local LLM (Claude) → Sophia (autopilot) — **own-repo** (`truesight_autopilot`)
**Created:** 2026-06-23
**Status:** DRAFT (awaiting governor review; not yet parked)
**Repo:** `truesight_autopilot` (Sophia's own codebase). **Own-repo gate: opens PRs only, NEVER self-merges.**
**Scope discipline:** §5a ONE PR PER TURN — on GO run PR1 ONLY then STOP; each PR self-contained + flag-gated.

---

## 1. Problem & goal

Sophia's agent loop dies at `CHAT_MAX_TOOL_ROUNDS` (default **30**, `app/main.py:2558`). The real binding
constraint isn't the round count — it's **context-window growth**: tool results accumulate in-context (~90K
tok by the time the loop has run, per the 2026-06-16 diagnosis), so raising the cap alone just trades
round-cap-empty for context overflow. The cap is *also* why every handoff plan is bite-sized to one PR per
turn.

**Goal:** make long work **resumable in bounded chunks** by adding a durable **journal + checkpoint/resume**,
so a turn that approaches the cap **checkpoints and ends cleanly**, and the next turn **rehydrates from the
journal** (cheap) instead of dragging the full raw history back into context. Decouples *work length* from
*context window*; survives restarts (the redeploy-loop class of failure, #201). Then a modest cap raise is
safe gravy.

**What already exists (build ON, don't reinvent):**
- **Compaction:** `_compact_old_tool_chains` (`main.py:2860/4175`), `_externalize_tool_result` (`2739`),
  `_summarise_tool_result` (`2398`) — raw tool output is already summarised/externalised.
- **Cap + empty-guard:** `MAX_TOOL_ROUNDS` (`2558`); forced-completion + DSML-strip + non-empty fallback
  (`1164-1196`, `2798-2820`) shipped via #227/#229.
- **Cross-process durable state:** `deploy_watcher` `active_tracks.json` (`STATE_PATH`, `register_track`).
- **Auto-continue without human prompt:** `app/auto_advance.py` (AUTO_ADVANCE).
- **Chunked/heartbeat sends:** `telegram_adapter.py:990`.

The **missing** piece is a durable per-session **journal** + **checkpoint-and-resume-across-turns**. This plan
adds exactly that and wires it to the existing compaction + auto-advance.

## 2. Pre-flight checklist (cross-PR decisions — settle BEFORE PR1)

- [ ] **Build-incremental vs adopt-a-harness.** `OPEN_FOLLOWUPS` has a parked item to swap the hand-rolled
      loop for a mature harness (which ships journaling/compaction/resume for free). **Decision gate:** if the
      governor intends to adopt a harness soon, DO NOT hand-build this — it would be thrown away. This plan
      assumes **build-incremental** (lowest disruption; keeps the DAO tool set + service intact). Confirm.
- [ ] **Journal store:** per-session append-only JSONL under the `deploy_watcher` `STATE_DIR`
      (`journals/<session_id>.jsonl`) — durable across process restarts, same pattern as `active_tracks.json`.
      Confirm path + retention (rotate/expire old journals).
- [ ] **Session key:** `session_id = tg:{chat_id}:{thread_id}` (already the handoff label) — confirm it is
      available at every point the loop writes a record.
- [ ] **Resume trigger decision:** when a checkpoint is open, resume via (a) **AUTO_ADVANCE self-spawn**
      (hands-free) or (b) a one-tap **"continue"** the governor taps. Recommend (b) first (safer), graduate to
      (a) behind a flag once trusted. Confirm.
- [ ] **Hard ceilings:** pick `CHAT_MAX_TOTAL_ROUNDS` (across resumes, e.g. 200) + a per-task token budget so
      "keep going" can't run away. Confirm values.
- [ ] **Anchors confirmed:** `MAX_TOOL_ROUNDS` (2558), forced-completion path (2798-2820), compaction fns
      (2398/2739/2860), `deploy_watcher` STATE_DIR, `auto_advance.py`. (All verified present 2026-06-23.)

## 3. Design

**Journal record (one per tool round + checkpoints):** `{ts, session_id, round, phase, intent,
tool, args_digest, result_summary, status}` where `result_summary` reuses `_summarise_tool_result`. A
**checkpoint** record additionally carries `{goal, resume_pointer, verified:<bool>, next_intent}` — the compact
state a fresh turn needs to continue.

**Loop integration (flag-gated, default OFF → zero behaviour change until enabled):**
1. Each tool round appends a journal record.
2. When `round >= MAX_TOOL_ROUNDS - K` (K≈3): write a **checkpoint** record + emit a clean
   *"checkpointed at round N — {resume_pointer}; continuing"* message **instead of** running to the forced
   completion. (The existing empty-guard remains as the backstop.)
3. A **new turn for the same `session_id`** detects an open checkpoint, loads the **journal head** (goal +
   last checkpoint + resume_pointer) into the system context — NOT the full raw history — and continues.
4. **Compaction tie-in:** once a tool result is journaled, `_compact_old_tool_chains` may drop its raw body
   from context (the journal is the durable copy), bounding net per-round context growth.
5. **Re-grounding:** every N rounds, re-read the journal head into context to fight drift (the governor's
   "check the transcript at a cadence").
6. **Verification checkpoints:** for code tasks, only mark a checkpoint `verified:true` after a green signal
   (tests / `node --check`); a resume must not build on unverified state.

## 4. Sequenced plan (each unit = ONE PR, self-contained, flag-gated, own-repo gate)

| PR | Repo/area | What | Acceptance |
|----|-----------|------|-----------|
| **PR1** | `app/journal.py` (new) | Append-only per-session JSONL journal primitive + record schema + read-head helper. Pure module. Unit tests. No loop wiring. | `pytest` green; journal write/read round-trips; no behaviour change. |
| **PR2** | `app/main.py` | Write a journal record each tool round, behind `JOURNAL_ENABLED` (default OFF), using `_summarise_tool_result`. | Flag OFF = byte-identical behaviour; flag ON = records appended. Tests for both. |
| **PR3** | `app/main.py` | Checkpoint-near-cap + rehydrate-on-new-turn (flag-gated). Replace the run-to-forced-completion at `round>=CAP-K` with checkpoint + clean message; new turn loads journal head. | A turn that would hit the cap instead emits a checkpoint message + leaves a resumable journal; a follow-up turn continues from it. |
| **PR4** | `app/auto_advance.py` + `main.py` | Resume trigger (per pre-flight: one-tap "continue" first; AUTO_ADVANCE self-spawn behind a flag) + **hard ceilings** (`CHAT_MAX_TOTAL_ROUNDS` + token budget) + re-grounding re-read every N rounds. | Long task resumes across turns; ceiling halts a runaway; re-ground read fires. |
| **PR5** | config / `main.py` | Raise default `CHAT_MAX_TOOL_ROUNDS` (e.g. 30→45) now that checkpoint/resume + empty-guard exist; document the cap vs total-ceiling relationship. | Cap raised; ceilings enforced; no empty-response regression on the 2026-06-16 cases. |
| **PR6** | vault panel / introspection | Surface journal/checkpoint state in the "where am I" introspection (ties to `SOPHIA_LIVE_PROGRESS_PLAN`, thread 2799). | Governor can see current round, last checkpoint, resume_pointer mid-task. |

## 5. Resume tracker (§5c Advance markers)

**RESUME HERE → PR1**

| Unit | Advance | PR opened | Merged (human) | Deployed | Contribution reported |
|------|---------|-----------|----------------|----------|----------------------|
| PR1 — journal primitive | `auto` | ☐ | ☐ | n/a | ☐ |
| PR2 — loop writes journal (flag off) | `auto` | ☐ | ☐ | ☐ | ☐ |
| PR3 — checkpoint + rehydrate | `gate: deploy + observe before enabling` | ☐ | ☐ | ☐ | ☐ |
| PR4 — resume trigger + ceilings | `gate: deploy + UAT` | ☐ | ☐ | ☐ | ☐ |
| PR5 — cap raise + ceilings config | `gate: deploy + regression check` | ☐ | ☐ | ☐ | ☐ |
| PR6 — observability | `auto` | ☐ | ☐ | ☐ | ☐ |
| UAT — long-task resume | `gate: human-run completion gate` | ☐ | ☐ | ☐ | ☐ |

Own-repo gate: **opens PRs only, never self-merges**; human merges + deploys each. Each PR is flag-gated so it
lands dark and is enabled deliberately. Report the DAO contribution after each merge.

## 6. UAT (human-run; completion gate — on Sophia's box, observed)

- **U1 — journal writes.** Enable `JOURNAL_ENABLED`; run a normal multi-tool turn. **Expect:** a
  `journals/<session>.jsonl` with one record per round; flag-off behaviour unchanged.
- **U2 — checkpoint at cap.** Force a long task (or lower the cap for the test). **Expect:** at `CAP-K` Sophia
  emits a clean *"checkpointed at round N…"* message (NOT empty, NOT DSML leak) + an open checkpoint in the journal.
- **U3 — resume.** Trigger continuation (tap "continue" / auto-advance). **Expect:** the new turn rehydrates from
  the journal head and continues coherently from `resume_pointer`, without re-loading the full raw history.
- **U4 — restart survival.** Kill/redeploy mid-task. **Expect:** the next turn still resumes from the journal
  (durable across process restart).
- **U5 — runaway ceiling.** Drive past `CHAT_MAX_TOTAL_ROUNDS`. **Expect:** Sophia halts with a clear ceiling
  message, not an infinite resume loop.
- **U6 — no regression.** Re-run the 2026-06-16 empty-response cases. **Expect:** clean final answers, no banner.
- **Acceptance:** a task longer than one round budget completes across ≥2 checkpointed turns, stays coherent,
  survives a restart, and respects the hard ceiling. PASS closes the handoff.

## 7. Risks & notes

- **Don't reinvent compaction** — wire PR4 into the existing `_compact_old_tool_chains` / `_externalize_tool_result`.
- **Drift over long runs** — mitigated by the periodic re-grounding read (U3/U-design); keep checkpoints small + factual.
- **Runaway cost** — the hard total-rounds + token budget (PR4) is mandatory, not optional.
- **Build-vs-adopt** — if the governor adopts a mature harness, this plan is superseded; settle the pre-flight gate first.
- **Flag-gated rollout** — every behavioural PR lands dark; enable on Sophia's box only after the prior soak.
- **Reference shape:** `SCORING_REVIEW_QUEUE_PLAN.md`, `EDGAR_DAO_EXTRACTION_PLAN.md`; related live work:
  `SOPHIA_CONTEXT_MANAGEMENT_PLAN.md` (compaction), `SOPHIA_AUTO_ADVANCE_PLAN.md`, `SOPHIA_LIVE_PROGRESS_PLAN.md`.
