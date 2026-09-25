# Sophia — goal-anchored thread loop + durable resume + Claude brain (3-track program)

**Status:** PLANNING — Unit A0 (this roadmap) committed; implementation not started.
**Owner:** Gary Teh (+ Sophia). **Created:** 2026-09-25. **Thread:** telegram 36801.
**Repos touched:** `agentic_ai_context` (docs), `truesight_autopilot` (code).
**Convention:** tracked roadmap required by `OPERATING_INSTRUCTIONS.md` §5 before any implementation.
Keep the **Resume tracker** (§6) current as each unit lands. §5a: **one PR per execution turn.**

---

## 1. Goal (why this exists)

Gary, 2026-09-25:

> *"What I want is for Sophia to be able to reason for herself and then keep looping until the task
> in a telegram thread is all completed. Right now we are utilizing Envoy for this part but Envoy
> runs out of quota a lot and then it just becomes manual supervision on my part."*

**End state:** a governor states a task in a Telegram thread; Sophia reasons, acts, checks her own
work, and **keeps going across turns until that thread's task is finished** — no human in the loop for
the routine steps. She still **stops and asks** at the irreversible gates (deploy / promote / TDG-or-
money / UAT-fail). Envoy the human-driven Claude Code seat stops being the supervisor.

This is three separable tracks, deliberately sequenced A → B → C:

- **A — goal-anchored thread loop:** make the loop follow *"is the governor's ask done?"*, not only a
  plan file's `Advance` markers. Raise/parameterize the 8-turn backstop.
- **B — durable journal + checkpoint/resume:** survive the per-turn round cap and a process restart
  mid-task. Absorbs `SOPHIA_DURABLE_JOURNAL_RESUME_PLAN.md`.
- **C — Claude brain:** route the hard reasoning turns to a strong model so quality stops depending on
  the small model. Absorbs `SOPHIA_ONAYA_LLM_SWAP_PLAN.md`.

---

## 2. What already exists (verified live 2026-09-25 — not guessed)

| Fact | Value | Source |
|---|---|---|
| Auto-advance | **ON** | live `.env`: `AUTO_ADVANCE=true` |
| Run-to-UAT mode | **ON** | live `.env`: `AUTO_ADVANCE_UNTIL_UAT=true` |
| Consecutive-turn backstop | **8** (code default; **not set** on the box) | `app/config.py` `auto_advance_max_turns` |
| Auto-advance scope | **plan-file only** — a thread with no handoff plan file **never** auto-advances | `app/main.py::_compute_advance_signal` (2943) |
| Loop driver | `_run_turn_with_auto_advance` | `app/telegram_adapter.py:1564` |
| Per-turn cap + graceful park | shipped | `ROUND_CAP_RESILIENCE_PLAN.md`, autopilot#275 |
| Provider layer | shipped (LiteLLM, provider-agnostic) | `app/llm/`, `docs/LLM_PROVIDER_ROADMAP.md` |
| Live model | `LLM_PROVIDER=litellm`, `LITELLM_MODEL=deepseek/deepseek-flash` | live `.env` |
| `ANTHROPIC_API_KEY` on Sophia's box | **absent** | live `.env` key scan (names only) |
| Restart of `truesight-autopilot` | raw SSH restart **blocked** by design; sanctioned path is `deploy_autopilot()` | `app/tools/ssh_tools.py::_SELF_RESTART_RE` |

---

## 3. The three gaps

- **G1 — plan-scoped only.** Auto-advance keys on a handoff plan's `RESUME HERE` + `Advance` markers.
  A thread whose task is *not* a tracked roadmap (most governor asks) gets **no** auto-continue at all.
  This is the single biggest reason Gary still hand-drives.
- **G2 — no durable resume.** A turn that approaches `CHAT_MAX_TOOL_ROUNDS` parks; a process restart
  mid-task loses the thread's working state. Nothing rehydrates.
- **G3 — no strong-model routing.** Every turn — routine monitoring *and* hard multi-step reasoning —
  runs on the same cheap model, so quality is capped; Gary compensates by supervising with Envoy,
  which starves on quota.

---

## 4. Track A — goal-anchored thread loop (the ask)

**Idea:** give each thread a lightweight, persisted **goal** — `{goal_text, done_criteria, status,
opened_ts, turns, last_progress_ts}` — written by Sophia when a governor states a task, and cleared
when she judges it done. The turn driver continues while a goal is **open** and the last turn **made
progress**; it stops on completion, a stall, an always-stop, or the hard ceiling.

**Design rules (non-negotiable):**

1. **Cheap.** No extra LLM call per turn just to ask "are we done?". Completion is *declared* by
   Sophia through a `complete_thread_goal` tool call, plus the existing made-progress/stall signal —
   not inferred by a second model pass.
2. **Fail-closed.** Any error / missing state ⇒ no auto-continue (identical to today).
3. **Flag-gated, lands dark.** `GOAL_LOOP_ENABLED=false` default ⇒ byte-identical behavior until the
   governor enables it after a soak.
4. **Always-stop preserved.** deploy / promote / TDG-or-money still gate by rule, reusing
   `app/auto_advance._ALWAYS_STOP_RE` — one source of truth, not a second regex.
5. **No cross-thread bleed.** The goal is keyed to `session_id` (`tg:{chat}:{thread}`), exactly the
   existing handoff label; a goal in one thread can never advance work in another.
6. **Hard ceiling.** A per-goal total-turn ceiling + a stall detector so "keep going" cannot run away.

### Units

| Unit | Repo | Scope | Advance |
|---|---|---|---|
| **A0** | `agentic_ai_context` | This roadmap. | `auto` |
| **A1** | `truesight_autopilot` | `app/thread_goal.py` — pure, I/O-light goal store (append-only JSONL under `DEPLOY_WATCHER_STATE_DIR`) + `should_continue()` decision (reuses `_ALWAYS_STOP_RE`). No wiring. Unit tests. | `auto` |
| **A2** | `truesight_autopilot` | Expose `set_thread_goal` / `complete_thread_goal` tools (manifest `TOOL_SPEC` + role). Wire the adapter loop: continue while goal open + progress + under ceiling, behind `GOAL_LOOP_ENABLED` (default OFF). Tests for both flag states. | `gate: deploy + observe before enabling` |
| **A3** | `truesight_autopilot` | Raise/parameterize the consecutive-turn backstop (document `AUTO_ADVANCE_MAX_TURNS` default) + add `CHAT_MAX_GOAL_TURNS` hard ceiling + stall detector. | `gate: deploy + UAT` |

**Exit:** a plain Telegram thread with a stated task runs to completion across turns without a governor
prompt, parks cleanly at a real gate, and cannot run away.

---

## 5. Track B / Track C — absorb the two drafted plans

Track B and Track C are **already drafted**; this roadmap does not re-derive them, it sequences them
behind Track A and records the dependency.

- **Track B — durable journal + checkpoint/resume.** Plan: `SOPHIA_DURABLE_JOURNAL_RESUME_PLAN.md`.
  Its own §2 pre-flight carries the **build-vs-adopt gate** (build incremental vs adopt a model-agnostic
  harness). **Decision recorded 2026-09-25: build incremental** — the provider layer already exists, so
  the gap is loop quality, and a harness swap is not required to deliver Gary's ask. Do **not** start
  B's PR1 until A3 is deployed and soaked (A makes the loop *reach* the cap far more often; B makes the
  cap survivable).
- **Track C — Claude brain.** Plan: `SOPHIA_ONAYA_LLM_SWAP_PLAN.md` (config-only: `LLM_PROVIDER=litellm`,
  `LITELLM_MODEL=anthropic/claude-haiku-4-5`, shared `ANTHROPIC_API_KEY`). **Always-stop gate:** the
  restart that makes it live is a production deploy. See §8 for the volume risk that must be resolved
  before triggering.

Tiered routing (cheap model for monitoring + simple chat, strong model on hard turns) is the durable
end state for Track C; the single-model swap is the bounded first step toward it.

---

## 6. Resume tracker

**RESUME HERE → A1**

| Unit | Advance | PR opened | Merged | Deployed | Contribution reported |
|---|---|---|---|---|---|
| A0 — roadmap (this file) | `auto` | ✅ [#1411](https://github.com/TrueSightDAO/agentic_ai_context/pull/1411) | ✅ | n/a (docs) | ☐ |
| A1 — `app/thread_goal.py` primitive + tests | `auto` | ☐ | ☐ | n/a | ☐ |
| A2 — goal tools + adapter loop (`GOAL_LOOP_ENABLED`, default OFF) | `gate: deploy + observe before enabling` | ☐ | ☐ | ☐ | ☐ |
| A3 — backstop raise + hard ceiling + stall detector | `gate: deploy + UAT` | ☐ | ☐ | ☐ | ☐ |
| B — durable journal + checkpoint/resume | `gate: A3 deployed + soaked` | ☐ | ☐ | ☐ | ☐ |
| C — Claude brain (Onaya key, bounded trial) | `gate: governor go + key copy` | ☐ | ☐ | ☐ | ☐ |
| UAT — long thread task runs to completion | `gate: human-run completion gate` | ☐ | ☐ | ☐ | ☐ |

**Repo merge policy (current practice, 2026-09-25):** Sophia merges her own feature PRs (including on
`truesight_autopilot`, her own control loop) — merging carries **no** auto-deploy, so a merged PR is
inert until a deliberate restart. The **deploy** is the always-stop gate, and production repos
(`*_prod`) and API-only data repos remain off-limits for writes. The older "opens PRs only, never
self-merges" line in `SOPHIA_DURABLE_JOURNAL_RESUME_PLAN.md` / `ROUND_CAP_RESILIENCE_PLAN.md` is stale.

---

## 7. Definition of Done

- A governor states a non-roadmap task in a Telegram thread; Sophia works it across **≥2** turns
  **without** a governor prompt, declaring completion herself.
- She **stops** at deploy / promote / TDG-or-money and asks — verified, not assumed.
- The hard ceiling halts a runaway with a clear message (no infinite loop).
- Flag OFF ⇒ behavior byte-identical to today (regression-tested).
- No cross-thread advancement (a goal in thread X never advances thread Y).

---

## 8. Risks & gates

1. **Runaway cost / loops.** Mitigated by the stall detector + `CHAT_MAX_GOAL_TURNS` hard ceiling (A3),
   which are mandatory, not optional.
2. **A2 widens auto-continuation beyond plan files** — the exact class the 2026-08-21 cross-thread-bleed
   fix narrowed. Mitigation: goal is `session_id`-keyed; flag lands dark; soak before enabling.
3. **Track C volume mismatch (the real one).** Sophia's overnight load was measured at **~84.7M
   tokens/night**; Onaya's Claude key is described as "underutilized" on a *human-paced, low-traffic*
   basis. Pointing Sophia's volume at a **shared** key risks exhausting its rate/spend cap and degrading
   **Onaya's own service**, plus a surprise bill. Also: litellm pass-through of a Claude model on a
   shared key has no per-consumer spend guard. **Therefore Track C is a bounded, monitored trial with a
   one-line rollback to DeepSeek**, and it does **not** start until (a) the governor explicitly says go
   and (b) tiered routing is decided (do we really want *all* turns on Claude?).
4. **Never force.** Deploy/critical-gate paths stay manual (`deploy_autopilot`, no raw restart).

---

## 9. Supersession

- Absorbs and sequences: `SOPHIA_DURABLE_JOURNAL_RESUME_PLAN.md` (Track B) and
  `SOPHIA_ONAYA_LLM_SWAP_PLAN.md` (Track C).
- Relates to the parked follow-up in `OPEN_FOLLOWUPS.md` (*"Swap autopilot's hand-rolled agent loop for
  a model-agnostic harness"*) — this roadmap **explicitly chooses build-incremental** and closes that
  build-vs-adopt gate.
- Relates to: `SOPHIA_AUTO_ADVANCE_PLAN.md`, `ROUND_CAP_RESILIENCE_PLAN.md`, `MULTI_LLM_ORCHESTRATION.md`.
