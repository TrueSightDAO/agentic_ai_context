# truesight_autopilot hardening — implementation plan + execution roadmap

**Goal:** Close the **verification + self-modification-safety + operational-robustness**
gaps surfaced by the 2026-06-10 assessment (and by this session's accidental
chaos-test of the operational seams). The codebase is architecturally sound — this
plan shifts investment from net-new capabilities to **making self-authored change
trustworthy**, since the autopilot writes code to its own repo and deploys to a
critical box.

> ## ▶ RESUME HERE
>
> **▶ ACTIVE: Phase 1, PR-B — add `ruff` (lint + format check) to CI.**
> PR-A merged (PR #146). Next: add ruff to `requirements-dev.txt` + `pyproject.toml`
> config + a CI step in `smoke.yml`. Fix or `# noqa`-justify violations so it passes.
>
> **Order of priority:** Phase 1 (real CI) → Phase 2 (self-modification gate) →
> Phase 3 (operational state) → Phase 4 (stretch). Each PR is independently
> shippable; report the DAO contribution after each merge.

**Why this matters (the binding constraint):** the weakest layer today is
**verification of self-authored change**, not features. "Green CI" was theater
until 2026-06-09 (pytest existed but CI never ran it; 3 tests were red); an LLM
(Sophia) authors much of this code; and a committed merge-conflict marker (#132)
once bricked a deploy. An agent that edits its own repo should be the *most*
rigorously verified thing in the fleet.

**Companion docs:** `OPERATING_INSTRUCTIONS.md` §5 (roadmap + UAT convention),
`GLOSSARY.md` (UAT), `OPEN_FOLLOWUPS.md` (the 3-deselected-tests item this plan absorbs).

---

## Pre-flight checklist (verify BEFORE coding)

- [ ] pytest is wired in CI (done — truesight_autopilot#136) and runs the unit
      suite with 3 `--deselect`s. Confirm current green baseline (`157 passed`).
- [ ] Decide the **lint/type tools**: `ruff` (lint+format, fast) + `mypy`. Confirm
      they install cleanly; expect mypy to need a lenient baseline at first.
- [ ] Decide the **own-repo PR gate** mechanism: a label + branch-protection-style
      check, and whether to add a second-LLM adversarial review in `fix_agent`.
- [ ] Decide **nonce persistence** backend: file-based (simplest, no new infra) vs
      Redis (the `auth.py` TODO). Default: file-based unless Redis already present.
- [ ] All work is on `truesight_autopilot`; PRs only, never self-merge (esp. for
      the own-repo gate work — dogfood it).

---

## Execution roadmap (resume tracker)

Legend: ☐ todo · ⧗ in progress · ☑ merged · 💸 contribution reported

### Phase 1 — Make CI real (verification)

| PR | Scope | Status |
|----|-------|--------|
| **A** | **Fix the 3 deselected unit tests** (mock their network/IO so they're hermetic): `tests/test_ssh_tools.py::test_missing_key_is_a_clear_error`, `tests/test_telegram_adapter.py::test_handle_message_allowed_calls_chat`, `tests/test_telegram_adapter.py::test_send_message_retries_without_thread_on_400`. Then **remove the `--deselect` flags** in `smoke.yml` so the full unit suite gates. (Closes the OPEN_FOLLOWUPS item.) | ☑ |
| **B** | **Add `ruff`** (lint + format check) to `requirements-dev.txt` + `pyproject.toml` config + a CI step in `smoke.yml`. Fix or `# noqa`-justify violations so it passes. Catches style + a class of bugs cheaply. | ☐ |
| **C** | **Add `mypy`** (type check) — start lenient (`ignore_missing_imports`, no `--strict`), establish a passing baseline, wire into CI. Types catch the "wrong attr / half-pasted snippet" failure mode that dominates LLM-authored code (and that `compileall` misses). Tighten incrementally later. | ☐ |

### Phase 2 — Harden the self-modification loop (highest blast radius)

| PR | Scope | Status |
|----|-------|--------|
| **D** | **Own-repo PR gate.** PRs the autopilot opens against **`truesight_autopilot`** must carry a distinct label (e.g. `self-modify`) and **never be self-merged** — require explicit, tracked human approval. Enforce in `github_client.py` / the `merge_pr` tool (`app/main.py`) + `fix_agent.py` (refuse to target own repo without the gate). | ☐ |
| **E** | **Adversarial pre-PR review for own-repo changes** (stretch within Phase 2): before `fix_agent` opens a PR against its own repo, run a second LLM pass prompted to *find reasons NOT to merge* (broken syntax, unsafe edit, scope creep); attach the verdict to the PR body. Cheap insurance beyond the bypassable regex hooks (`fix_agent.py:30–48`). | ☐ |

### Phase 3 — Operational state robustness

| PR | Scope | Status |
|----|-------|--------|
| **F** | **Persist the nonce replay cache** (`app/auth.py` `_seen_nonces` — in-memory, resets on restart → reopens a replay window). File-based store keyed by nonce+expiry (or Redis). Removes the "restart weakens auth" footgun. | ☐ |
| **G** | **flock timeout on the context lock** (`app/context.py` `_context_lock`) — currently no timeout; a hung reader could hold it. Add a bounded wait + fall back to lock-free with a logged warning. (Low severity; quick.) | ☐ |

### Phase 4 — Stretch / debt paydown

| PR | Scope | Status |
|----|-------|--------|
| **H** | Migrate the 4 legacy orchestration tools (`submit_contribution`, `open_fix_pr`, `merge_pr`, `create_dao_submission`) from the inline branches in `app/main.py` `_run_tool` (~260 lines) to the registry handler pattern — removes the dual dispatch path. | ☐ |
| **I** | Add a **troubleshooting runbook** to the README (email not polling, context sync hung, Telegram adapter down, deploy recovery) — the assessment flagged it missing. | ☐ |

---

## UAT phase (human acceptance — mostly automated, but eyeball these)

Most of this is backend/CI, so much of it is "UAT: covered by automated tests."
The **human-observable** acceptance checks:

| # | Surface | Interaction / what to eyeball | Acceptance |
|---|---------|-------------------------------|------------|
| U1 | A PR's **GitHub Actions** tab (after Phase 1) | Open a throwaway PR that deliberately breaks a unit test (or adds a type error / lint violation) | CI turns **red** and blocks it — proves the gate is real, not theater |
| U2 | Same | Revert the break | CI turns **green** |
| U3 | A `truesight_autopilot` PR **opened by the autopilot itself** (after Phase 2) | Eyeball: it carries the `self-modify` label and **cannot be merged** by the agent | Self-merge refused; explicit human approval required; (Phase 2E) adversarial-review verdict present in the PR body |
| U4 | The autopilot service after a **restart** (after Phase 3) | Replay a previously-used signed request (nonce) | Rejected as a replay even across the restart |

Acceptance = U1–U4 behave as stated. U1/U2 are the proof that "green CI" now
means something.

---

## Risks / notes

- **mypy baseline churn** — a large untyped codebase may surface many errors;
  start lenient and ratchet, don't block Phase 1 on a clean `--strict` run.
- **Own-repo gate must be dogfooded** — build PR-D via a normal PR, and confirm the
  gate would have caught the #132 conflict-marker class (CI red) before merge.
- **Don't over-rotate to scaling** — single-worker / in-memory sessions are a real
  ceiling but acceptable at current load; this plan only hardens the *auth-critical*
  state (nonce), not a full distributed-state rewrite.

---

*Plan owner: this doc. Update the resume tracker as each PR lands; report the DAO
contribution before starting the next. Can be handed off to Sophia (per
`SOPHIA_HANDOFFS.md`) — but **dogfood the Phase-2 own-repo gate**: those PRs are
the exact case the gate governs.*
