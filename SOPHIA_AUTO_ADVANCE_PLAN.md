# Sophia Auto-Advance — Execution Roadmap (handoff to Sophia)

**Status as of 2026-06-17:** DRAFT — design approved by Gary 2026-06-17; pending execution.
**Repo under change:** `truesight_autopilot` (Sophia's OWN codebase — adapter + brain).
**Designed by:** Gary Teh + Claude · **Implemented by:** Sophia (or Claude), human-merged.

> ⛔ **Own-repo gate:** open PRs only, **NEVER self-merge** `truesight_autopilot` PRs (a human
> reviews + merges). Every new behavior ships behind an env flag defaulting to *current behavior*
> until soak-verified.

> **RESUME HERE:** PR1 — the `Advance`-column convention + pure marker parser (no runtime change).

---

## 1. Why

§5a (`OPERATING_INSTRUCTIONS.md`) enforces **one PR per execution turn** because a turn has a hard
`CHAT_MAX_TOOL_ROUNDS` cap (~30): a turn that tries to do a whole roadmap calls a tool every round,
never converges, exhausts the cap, and the forced completion comes back as **"⚠️ Autopilot produced
an empty response."** Keeping each turn to one PR keeps it *converging* inside the budget.

That rule fixed the brick — but introduced a **slowdown**: after each PR turn Sophia **stops and
waits for the governor to prompt her again** for the next PR. On a 5-PR plan that's 5 round-trips of
"…ok, next" from Gary, who is otherwise left wondering whether anything is happening.

The original *reason* one-PR-per-turn also protected the context window
(`SOPHIA_CONTEXT_MANAGEMENT_PLAN.md`: DeepSeek's 131K window overflowing on a tool-heavy thread →
empty response). **That protection now exists independently** — externalization + sub-task
compaction + recall shipped + deployed 2026-06-14 (CM0–CM4). A completed PR turn now **compacts to a
one-line outcome** ("PR3 → URL") before the next turn starts, so a long multi-PR thread stays
bounded. The window is no longer the reason to stop after each PR.

**Goal:** keep the per-turn round-cap discipline (one PR = one turn, fresh round budget, fresh
compaction), but **auto-advance to the next PR turn without waiting for a human prompt** — pausing
only at explicitly-marked gates, on failure, on completion, or at a runaway cap. The governor gets a
**progress report between every PR** so the thread is never silent.

## 2. Design

### 2a. The `Advance` marker (the explicit gate convention)

The roadmap's **resume tracker** grows one column, `Advance`, per unit:

| Value | Meaning |
|-------|---------|
| `auto` | On successful completion of this unit, **immediately continue** to the next unit. |
| `gate: <reason>` | After this unit, **STOP** and post a pause report carrying `<reason>` + open-PR links + "reply `go` to continue." |

Sophia obeys the column **literally** — she does not infer gates. Anything she cannot parse
unambiguously is treated as `gate` (**safe default: stop, never auto-advance blindly**). UAT and any
prod-touching / human-merge-dependent unit are always marked `gate:`.

Example tracker:

| Unit | Advance | PR opened | Merged (human) | Deployed | UAT |
|------|---------|-----------|----------------|----------|-----|
| PR1 | `auto` | ☐ | ☐ | ☐ | — |
| PR2 | `auto` | ☐ | ☐ | ☐ | — |
| PR3 | `gate: PR2 must merge first (depends on its schema)` | ☐ | ☐ | ☐ | — |
| PR4 | `gate: prod deploy — eyeball before go` | ☐ | ☐ | ☐ | — |
| UAT | `gate: UAT` | ☐ | ☐ | ☐ | U1–U5 |

### 2b. The loop

```
turn = one PR  (do the RESUME-HERE unit: make change → open PR → report contribution → tick tracker)
  → brain posts the per-turn completion report  (existing _build_turn_report)
  → brain computes the ADVANCE SIGNAL for the unit it just finished:
        decision ∈ { auto | gate | done | failed }
  → adapter obeys the signal:
        auto  AND under the consecutive-turn cap  → dispatch the next "continue" turn (loop)
        gate                                      → post pause report (reason + PR links + "reply go") and STOP
        done  (no more units)                     → post final summary and STOP
        failed (turn errored / no PR opened)      → post halt report and STOP
```

### 2c. Reporting (so the governor is never in the dark)

- **Between PRs (heartbeat):** the existing per-turn report (`_build_turn_report`, `app/main.py`)
  already enumerates the turn's side-effects (PR URL, files, commands). Auto-advance **reuses it
  verbatim** and appends a one-liner: `▶️ Continuing to <next unit> (<N> remaining).`
- **At a gate:** `⏸️ Paused before <unit>. Gate: <reason>. PRs so far: <links>. Reply "go" to continue.`
- **On completion:** `✅ Plan complete — <N> PRs opened: <links>. <M> gated for your review.`
- **On failure:** `🛑 Halted at <unit>: <error>. <K> PRs opened before this: <links>. Nothing auto-advanced past the failure.`
- **Mid-PR ("what's happening right now"):** covered by the companion `SOPHIA_LIVE_PROGRESS_PLAN.md`
  (pull-side `/chat/progress`). Auto-advance covers the *gaps between* PRs; live-progress covers
  *inside* a long PR. (Note: live-progress had two cross-process bugs found 2026-06-17 — see that
  plan's tracker; fix `fix/live-progress-cross-process`.)

## 3. Architecture decisions (with rationale)

- **Adapter-driven loop; one `/chat` call per PR.** Each PR is a separate brain turn (≤ the
  adapter's `_CHAT_TIMEOUT = 180s`, ≤ the round cap, with its own compaction pass). The adapter
  re-invokes for the next PR. *Rejected alt: the brain self-enqueues into `_message_queues` and the
  existing drain loop runs the whole chain in ONE SSE stream — clean, but a multi-PR chain blows past
  the 180s per-call timeout and loses clean per-PR messages. The per-call loop is robust to per-turn
  timeouts and gives one tidy report per PR.*
- **Brain emits the advance decision, deterministically.** The brain just finished the PR and (per
  §5) just ticked the tracker, so it holds the freshest plan state — it parses the `Advance` column
  and emits `{decision, gate_reason, next_unit}` in the `done` event. *This avoids the adapter
  re-reading a stale synced clone of the tracker (≤5-min lag) — the source of truth is the process
  that just wrote it.*
- **Gate decision is deterministic; PR *work* stays LLM-driven.** The LLM does the PR inside the
  turn; whether to continue is a literal read of the `Advance` column, not the LLM's judgment.
- **Failure = halt.** A turn that errors, or completes **without opening a PR** (the success
  signal), never auto-advances. Halt and report.
- **Ambiguity = gate.** Unparseable tracker, missing `Advance` column, can't identify the next unit
  → treat as gate (stop), never auto-advance. Mirrors live-progress's "bias toward safe."
- **Runaway cap + human interrupt.** A consecutive-auto-turn cap (`AUTO_ADVANCE_MAX_TURNS`, default
  **8**) backstops a mis-marked all-`auto` plan. A real governor message arriving mid-chain folds
  into the per-thread queue (existing concurrency machinery) and can halt the loop ("stop").
- **Off by default.** Behind `AUTO_ADVANCE` env flag; until on, behavior is exactly today's
  one-PR-then-wait.

## 4. Pre-flight checklist

- [ ] Confirm `CHAT_MAX_TOOL_ROUNDS` value on prod and that a typical single PR converges within it.
- [ ] Confirm context-management flags are **on** in prod (`CONTEXT_COMPACT`, `CONTEXT_EXTERNALIZE`,
      `CONTEXT_COMPACT_KEEP_RECENT`) so a multi-turn auto-advanced thread stays under the window.
- [ ] Confirm the brain can resolve the active plan file per thread at turn-end — it already gets the
      handoff prefix (`_handoff_prefix` → `_handoff_plan_for_thread`, `app/telegram_adapter.py`); the
      brain side needs the same resolution (via thread_id in the dispatch text, or pass the plan file
      through the request).
- [ ] Decide `AUTO_ADVANCE_MAX_TURNS` default (proposed **8**).
- [ ] Confirm the **success signal** for "a PR turn completed": a PR-opening tool fired this turn
      (`open_fix_pr` in `tool_trace` returning a PR URL). Lock this — it gates auto-advance.
- [ ] Add the `Advance`-column convention to `OPERATING_INSTRUCTIONS.md` §5a + the roadmap template
      (this is PR1's doc step; it is a canonical-file edit → call it out for human approval in the PR).
- [ ] Own-repo gate confirmed: open PRs only, never self-merge.

## 5. Sequenced plan (each PR independently shippable — §5a)

### PR1 — `Advance`-marker convention + pure parser *(no runtime behavior change)*
| Step | Description | Files |
|------|-------------|-------|
| 1a | Document the `Advance` column in `OPERATING_INSTRUCTIONS.md` §5a + add it to the roadmap template; safe-default = `gate`. *(canonical edit — flag for human approval.)* | `agentic_ai_context/OPERATING_INSTRUCTIONS.md` |
| 1b | Pure helpers: `parse_resume_tracker(plan_text) -> [(unit, advance_marker, done?)]` and `advance_after(plan_text, completed_unit) -> {decision, gate_reason, next_unit}`. Unparseable/missing → `decision="gate"`. | `app/auto_advance.py` (new) |
| 1c | Unit tests: auto→auto, auto→gate, last-unit→done, missing column→gate, malformed→gate, gate-reason extraction. | `tests/test_auto_advance.py` |

### PR2 — Brain emits the advance signal *(flagged off)*
| Step | Description | Files |
|------|-------------|-------|
| 2a | At turn-end on a handoff thread, resolve the active plan, read the (just-ticked) tracker, call `advance_after(...)`, and include `advance: {decision, gate_reason, next_unit}` in the `done` SSE event + the `/chat-blocking` response. Gated on `AUTO_ADVANCE`. | `app/main.py` |
| 2b | Success signal: only emit `decision="auto"` when this turn actually opened a PR (`open_fix_pr` in `tool_trace`); else `failed`/`gate`. | `app/main.py` |
| 2c | Tests: stub plan + stub tool_trace → correct `advance` payload for each decision; flag off → no `advance` field (today's behavior). | `tests/` |

### PR3 — Adapter self-advance loop + reports *(flagged off)*
| Step | Description | Files |
|------|-------------|-------|
| 3a | On `done` with `advance.decision=="auto"` and consecutive-turn count `< AUTO_ADVANCE_MAX_TURNS`: dispatch the next turn (`"[AUTO-ADVANCE] Execute the next PR (RESUME HERE) in <plan>; stop at any gate."`) reusing `call_chat_with_progress`. | `app/telegram_adapter.py` |
| 3b | `gate` → pause report (reason + open-PR links + "reply `go`"); `done` → final summary; `failed` → halt report. | `app/telegram_adapter.py` |
| 3c | Honor the per-thread queue: a governor message arriving mid-chain halts/interrupts the loop. Reset the consecutive counter when the governor re-issues `go`. | `app/telegram_adapter.py` |
| 3d | Tests: 3 auto units → 3 turns + 2 heartbeats + final; auto→gate stops with pause report; failure stops; cap stops; governor "stop" interrupts. | `tests/` |

### PR4 — (rollout, not a PR) Deploy + UAT — see §7–8.

## 6. Test plan

- **Unit (`pytest -q`):** the parser (all decisions + safe defaults), the brain signal payload, the
  adapter loop (mocked brain returning scripted `advance` decisions), report rendering.
- **Loop correctness:** N auto units ⇒ exactly N turns, N−1 heartbeats, one terminal report;
  arrival order preserved; failure at unit k ⇒ stops at k, k−1 PRs reported.
- **Safety:** missing/malformed tracker ⇒ gate (stop); cap ⇒ stop; flag off ⇒ identical to today.

## 7. Rollout *(gated on Gary's go — do not auto-deploy)*

1. Merge PR1 (pure + docs) → no deploy needed.
2. Merge PR2, PR3 with `AUTO_ADVANCE` **off** → deploy via the targeted path
   (`git checkout -B main origin/main` on the box, **no `git clean`** — `deploy.sh` footgun nukes
   `sessions/`; use `deploy_autopilot`), restart, confirm behavior unchanged (flag off).
3. Flip `AUTO_ADVANCE=true` → run UAT on a scratch handoff thread with a throwaway 3-PR plan.

## 8. UAT — operator acceptance (run in Telegram)

| # | Scenario | Expected |
|---|----------|----------|
| U1 | Hand off a 3-PR plan, all `auto`; say `go` | 3 PRs opened across 3 turns with **no further prompting**; a heartbeat report after PR1 and PR2; final summary with 3 links |
| U2 | Plan with PR1 `auto`, PR2 `gate: eyeball` | Stops after PR1 with a pause report carrying the reason + PR1 link; `go` resumes to PR2 |
| U3 | A PR turn fails (e.g. tests red) | Loop **halts** at that PR, reports the error + prior PR links; does **not** roll into the next PR |
| U4 | All-`auto` plan longer than the cap | Stops at `AUTO_ADVANCE_MAX_TURNS` with a "hit the auto cap — reply `go` to continue" report |
| U5 | Governor sends "stop" mid-chain | Loop halts after the current PR; no further auto-advance |
| U6 | `AUTO_ADVANCE` off | Behavior is exactly today's: one PR, then wait |

**Completion gate:** PRs human-merged (Sophia opens, never self-merges); U1–U6 pass.

## 9. Risks & mitigations

- *LLM fails to tick the tracker* → brain can't find the next unit → **gate (stop)**, safe default.
- *Mis-marked all-`auto` plan runs away* → `AUTO_ADVANCE_MAX_TURNS` cap + governor interrupt.
- *A PR "succeeds" without really opening a PR* → success signal requires `open_fix_pr` in
  `tool_trace`; otherwise `failed` → halt.
- *Context still grows across many turns* → compaction (CM2) runs per turn; cap bounds the chain;
  the #189 token-trim + self-heal sanitiser remain unconditional backstops.
- *Two governors / cross-thread* → loop state is per-thread (per `session_id`); different threads are
  independent (existing concurrency invariants).

## 10. Resume tracker

| Unit | Advance | PR opened | Merged (human) | Deployed | UAT | DAO contribution reported |
|------|---------|-----------|----------------|----------|-----|---------------------------|
| PR1 — convention + parser | `auto` | ☐ | ☐ | n/a | — | ☐ |
| PR2 — brain advance signal | `auto` | ☐ | ☐ | ☐ | — | ☐ |
| PR3 — adapter self-advance loop | `gate: deploy + UAT before go-live` | ☐ | ☐ | ☐ | U1–U6 | ☐ |
| PR4 — rollout + UAT | `gate: UAT` | ☐ | ☐ | ☐ | U1–U6 | ☐ |

> **RESUME HERE:** PR1 — add the `Advance`-column convention to `OPERATING_INSTRUCTIONS.md` §5a +
> roadmap template, and ship the pure `app/auto_advance.py` parser with tests. Open a PR; **do not
> self-merge** (human reviews). This unit is itself `auto` → on success continue to PR2.

## 11. Dependency notes

Builds on the shipped per-thread concurrency work (`SOPHIA_THREAD_CONCURRENCY_PLAN.md`: dispatch
lock, `_message_queues` drain, `_build_turn_report`) and the context-management stack
(`SOPHIA_CONTEXT_MANAGEMENT_PLAN.md`: compaction keeps the multi-turn thread bounded — the
precondition that makes auto-advance safe now). Pairs with `SOPHIA_LIVE_PROGRESS_PLAN.md` for the
inside-a-PR "what's happening now" view.
