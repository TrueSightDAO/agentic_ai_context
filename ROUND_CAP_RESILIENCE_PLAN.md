# Round-Cap Resilience — prevent silent per-turn blowups in future plans

**Status:** in progress · **Owner:** Claude (Opus 4.8) · **Created:** 2026-06-28
**Repos touched:** `agentic_ai_context` (docs), `truesight_autopilot` (code)

---

## §1 — Context (what went wrong)

On 2026-06-28 a Sophia turn executing `POST_REPACKAGING_CLEANUP_PLAN.md` came back as the
empty-response fallback (`_EMPTY_TURN_FALLBACK`, `truesight_autopilot/app/main.py:1166`):

> *"I worked through the maximum number of tool rounds but couldn't land a final answer…"*

Root cause (confirmed against the live box, not guessed):

- The "uncap" the governor applied was **`AUTO_ADVANCE=true`** (`app/config.py:27`) — present in
  `/opt/truesight_autopilot/.env` and the running process env. That removes the *human-GO gate
  between PRs* (the across-turns axis).
- The cap that actually fired is **`CHAT_MAX_TOOL_ROUNDS`** (`app/main.py:2576`, default **30**) —
  the *per-turn* tool-call budget. It is **not set anywhere** on the box, so it runs at the code
  default. The uncap never touched it.
- The turn **merged PR4** (`truesight_me` #262) **and** auto-advanced into **PR5** (`tokenomics`
  GAS handler) in the *same turn*. PR5 required reading the current
  `agroverse-inventory/gas/repackaging-currency-ingest/Code.gs` to extend it, so the turn spent
  8+ `ssh_run` rounds curling that live file. Merge + cross-repo audit + handler edit > 30 rounds
  → forced text-only completion → DeepSeek emitted DSML-as-content → `_strip_dsml` emptied it →
  fallback banner. **Silent and non-resumable.**

This is the `OPERATING_INSTRUCTIONS.md` §5a anti-pattern. The rule already exists; the failure was
that (a) the plan was under-pre-flighted and (b) the harness degraded silently instead of parking
cleanly. This plan fixes both, structurally, so it doesn't depend on the next author being perfect.

## §2 — Goal

Three independent, additive mechanisms (governor selected all three, 2026-06-28):

1. **Authoring gate (#1, doc):** every future plan must pre-flight its cross-repo reads, enforced
   by a checkable Pre-flight Completeness self-cert in the plan SOP (`OPERATING_INSTRUCTIONS.md` §5).
2. **Execution backstop (#2, code):** a turn winds down *gracefully* before the round cap — it
   summarizes, updates the resume tracker, and parks — instead of grinding to 30 and leaking DSML.
   Author-independent: catches every under-pre-flighted plan.
3. **One-PR-boundary (#3, code):** a turn that fires a PR side-effect (`merge_pr`/`open_pr`/
   `open_fix_pr`) converges to its "what I did" report and stops; auto-advance starts the next PR
   in a **fresh** turn. Kills the "merge PRn + start PR(n+1) in one turn" bundling specifically.

## §3 — Pre-flight (CANONICAL — read before any execution turn)

> Modeling the fix: every cross-file read an execution unit needs is captured here so no PR turn
> re-discovers it live.

### Access / prereqs
- `truesight_autopilot` and `agentic_ai_context` both clone clean under `~/Applications`; git ops
  pre-authorized. Push via HTTPS (`gh` cred helper). `pytest` configured (`pyproject.toml`,
  `requirements-dev.txt`); existing `tests/test_auto_advance.py` is the pattern for #3.
- Autopilot is its own deploy (not a beta/prod-split repo). Own-repo gate: **open PRs, governor
  merges** the code PRs (#2/#3). Restart to deploy: `sudo systemctl restart truesight-autopilot`
  (no auto-deploy on merge).

### Code snapshot — the per-turn round loop (`app/main.py`, `_run_chat_turn` generator)
- `MAX_TOOL_ROUNDS = int(os.getenv("CHAT_MAX_TOOL_ROUNDS", "30"))` — line **2576**.
- Loop header `while round_num < MAX_TOOL_ROUNDS:` — line **2608**; `round_num += 1` at top.
- Per-round: builds `chat_task`, extracts `tool_calls`; when there ARE tool calls it executes them
  and appends `{"role":"tool",…}` to `history`, then `_sanitise_tool_messages(history)`
  (lines ~2794–2806). When there are **no** tool calls: `assistant_text = client.extract_text(...)`
  then `break` (line **2809**). **This is the injection point** — after the tool-results append
  (~2803) is where a convergence nudge gets pushed into `history`.
- Cap-exhaustion path (lines **2814–2845**): if `assistant_text` empty → force `tools=None`
  completion → `_strip_dsml` → `_ensure_nonempty_final` → `_EMPTY_TURN_FALLBACK`. This is the
  silent failure #2 replaces with a graceful park.
- `state["tool_trace"]` accumulates `{name,args,result}` per tool — #3 reads it (or tracks a flag)
  to know a PR side-effect fired this turn.

### Code snapshot — side-effect + advance plumbing (already exists, reuse it)
- `_SIDE_EFFECT_TOOLS` set — `app/main.py:2367` — already contains `open_fix_pr`, `merge_pr`,
  `open_pr` (plus deploys, ledger, ssh). #3's trigger = "a `*_pr` tool in this set fired".
- `opened_pr = any(...)` then `next_action(plan_text, opened_pr)` — `app/main.py:2479–2489`.
  `auto_advance.next_action(plan_text, opened_pr)` (`app/auto_advance.py:230`) **already** fails
  closed to `gate` unless a PR opened AND `RESUME HERE` is `auto`. So the *across-turn* boundary is
  handled; #3 only needs to ensure the *brain turn itself* converges right after the PR side-effect
  rather than rolling into the next unit's discovery.
- Auto-advance turn driver: `telegram_adapter._run_turn_with_auto_advance` (`app/telegram_adapter.py:974`),
  backstop `auto_advance_max_turns` default 8 (`app/config.py:29`).

### Design decision (resolve once, here)
- #2 and #3 share one helper: inject a single `{"role":"system"|"user"}` **convergence nudge** into
  `history` (idempotent — once per turn, guarded by a local flag), instructing: *stop calling tools,
  write the "what I did / what's blocking / RESUME-HERE" report, do not start new multi-step work.*
  Triggers: #2 = `round_num >= SOFT_BUDGET` (default `ceil(MAX_TOOL_ROUNDS * 0.75)`, env
  `CHAT_TOOL_ROUNDS_SOFT_FRACTION`); #3 = a `_SIDE_EFFECT_TOOLS` PR tool fired this turn.
- Keep `CHAT_MAX_TOOL_ROUNDS=30` (the hard convergence guarantee). The backstop lands *before* it.

## §4 — Sequenced plan (ONE PR per execution turn — §5a)

| PR | Repo | Scope | Merge |
|----|------|-------|-------|
| **PR1** | `agentic_ai_context` | This roadmap **+** §5 "Pre-flight Completeness" authoring gate (#1) | docs — self-merge OK |
| **PR2** | `truesight_autopilot` | Convergence-nudge helper + **soft-budget** trigger (#2) + unit test | governor merges |
| **PR3** | `truesight_autopilot` | **PR-side-effect** trigger reusing PR2's helper (#3) + unit test | governor merges |

PR2 lands the shared helper; PR3 adds the second trigger on top. Each PR is self-contained with its
own test. No PR turn reads a file not snapshotted in §3.

## §5 — Resume tracker

| Unit | PR opened | Merged | Deployed (restart) | Contribution reported |
|------|-----------|--------|--------------------|-----------------------|
| PR1 — roadmap + authoring gate | ☐ | ☐ | n/a (docs) | ☐ |
| PR2 — soft-budget backstop (#2) | ☐ | ☐ | ☐ | ☐ |
| PR3 — one-PR-boundary (#3) | ☐ | ☐ | ☐ | ☐ |

**RESUME HERE → PR1.**

> ✅ Pre-flight Completeness (§5d): no execution unit requires reading a file/state not already
> captured in §3.

## §6 — UAT (beta/manual; never prod money)

- **U1 (#2):** On a scratch thread, set `CHAT_MAX_TOOL_ROUNDS=6`, give an instruction that needs
  >6 tool rounds. Expect: a clean parked summary with a RESUME-HERE line at ~round 5, **no**
  `_EMPTY_TURN_FALLBACK`, no DSML banner. Acceptance: response is human-readable + resumable.
- **U2 (#3):** Give a one-PR instruction on a handoff thread with `AUTO_ADVANCE=true`. Expect: the
  turn merges/opens exactly one PR, reports, and **stops**; the next unit begins in a new turn.
  Acceptance: no single turn contains both a PR side-effect and the next unit's discovery.
- **U3 (#1):** n/a (doc) — reviewer confirms the self-cert line renders in §5 of OPERATING_INSTRUCTIONS.
