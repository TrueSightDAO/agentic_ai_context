# Sophia auto-advance — stop gating on PR-less units (follow-on to SOPHIA_AUTO_ADVANCE_PLAN.md)

**Filed:** 2026-09-15, by Claude Anthropic (Envoy), at Gary's request. **Repo under change:**
`truesight_autopilot` (Sophia's own codebase). **Status: proposal, ready for review.**

> ✅ **Updated 2026-09-15 — own-repo merge gate retired.** Gary: *"I don't think merging should be
> human gated. Only deployment of GAS and human UAT. Merge should just be handled by Sophia."*
> (`sophia/SUPERVISOR_LOOP.md` §5, governor decision 2026-09-15.) PRs to `truesight_autopilot` may
> now be self-merged (CI green + tests pass), same as any other non-prod repo — the line below is
> kept only as historical record of what PR3 originally assumed.
>
> ~~⛔ Own-repo gate carries over from the parent plan: open PRs only, never self-merge
> `truesight_autopilot` PRs — a human reviews + merges (unlike the docs-only self-merge convention
> used elsewhere in `agentic_ai_context`).~~ **Superseded.** PR3 (deploy) below is still gated —
> restarting the live service is a separate action from merging code, per the same governor decision.

---

## 0. The problem, stated plainly

Gary, 2026-09-15, watching the sprint-board handoff execute live: *"I am thinking right now Sophia
does auto advance conditionally. My sense is if her thread is in the handoff JSON she should just
auto advance by default until a gated stage. Right now the interim wait where she pauses and
supervisor wakes up from the loop to check on her is too long."*

**This isn't a hypothetical — it reproduced twice in the same live thread while this doc was being
written**, against the sprint-board plan (`SPRINT_TRUESIGHT_ME_BOARD_PROPOSAL.md`, thread 30083):

1. After **PR3** ("Route53 CNAME `sprint.truesight.me`; verify live, 200, valid cert") — a unit that,
   *by design*, never produces a GitHub PR (it's a DNS/Pages config-and-verify step) — Sophia's own
   turn correctly finished the work (`sprint.truesight.me` confirmed live over HTTP) and then halted:
   `⏸️ Paused before the next unit. Gate: turn did not open a PR — halting auto-advance. Reply 'go' to
   continue.` Work was done; nothing was wrong; it stopped anyway.
2. A separate halt in the same thread: `Gate: unit '(§4) = PR1a.' not found in resume tracker`.
   **Root cause confirmed by Sophia herself, live, while this doc was being written:** the plan carried
   **two** `RESUME HERE` markers (a top-of-file hint + the authoritative one in the resume tracker —
   `find_resume_here()`'s own design, by its docstring: *"plans repeat the pointer... the last
   occurrence wins"*). An earlier edit updated only one of the two occurrences; the stale, unedited one
   was the one actually read. Not a regex/parsing bug — an **authoring-discipline gap** with no
   automated check catching the drift. See the corrected §2.3.
3. **A third instance of the same root shape, also surfaced live, in the merge step:** `merge_pr`
   refused to merge a docs-only PR because CI read as "pending," when the workflow triggering that
   check is `paths:`-filtered to `handoffs/**` + `scripts/**` and the PR touched neither — no check was
   ever going to run. Filed separately (§2.4) since it's a different tool/code path, but it's the same
   pattern: a correct, converged outcome misread as an unfinished one.

All three are real, all happened without any human editing error beyond the ordinary act of writing a
plan, and each required a human (or Envoy, standing in) to notice and intervene before work continued
— exactly the latency Gary is describing.

---

## 1. Current-state audit — the exact mechanism (read directly, 2026-09-15)

### 1.1 How "did this turn converge" is decided

`app/auto_advance.py::next_action(plan_text, opened_pr, ...)`:

```python
def next_action(plan_text: str, opened_pr: bool, *, run_to_uat: bool = False) -> AdvanceDecision:
    if not opened_pr:
        return AdvanceDecision(
            decision="gate",
            gate_reason="turn did not open a PR — halting auto-advance",
        )
    ...
```

`opened_pr` is computed in `app/main.py::_compute_advance_signal()`:

```python
progress_tools = {"open_fix_pr", "open_pr", "merge_pr"}
opened_pr = any((t or {}).get("name") in progress_tools for t in (tool_trace or []))
```

**"Progress" is defined as literally calling one of three specific tools this turn.** Any unit whose
correct completion doesn't involve those tools — a DNS/Pages verification step, a pure research/
pre-flight turn, an SSH-based infra check, a `git_push_changes` direct-to-main commit (the docs-only
self-merge pattern used everywhere in `agentic_ai_context` this session) — **can never satisfy this
condition**, regardless of how much real, correct work the turn did. The gate function has no signal
for "this turn succeeded and simply wasn't a PR-shaped unit."

### 1.2 Why this exists (worth preserving, not just deleting)

The docstring is explicit: *"Never auto-advance on a broken turn."* This condition was added
specifically to stop a genuinely stuck/erroring turn from silently chaining into "the next unit,"
compounding a failure invisibly. `app/turn_convergence.py`'s `soft_budget` mechanism (nudges the model
to wrap up before the hard `CHAT_MAX_TOOL_ROUNDS` cap) exists for the adjacent, related problem — a
turn that's taking too long gets pushed toward a clean stopping point rather than crashing into the
cap mid-thought. **The fix below must keep catching real non-convergence** (errors, zero-progress
turns, hitting the hard cap with nothing to show) — it must not simply flip the default to "always
continue," which would reopen the exact failure mode this code was built to close.

### 1.3 The duplicate-`RESUME HERE`-marker drift (incident #2 — root cause confirmed)

`find_resume_here()`'s own docstring: *"plans repeat the pointer (a top-of-file hint plus the
authoritative one in the resume tracker)... the last occurrence wins."* This duplication is
intentional design, not an accident — a reader scanning the top of a long plan gets a quick hint
without scrolling to the tracker. **The bug is that nothing keeps the two occurrences in sync.** In the
live incident, an editing turn updated the tracker's `RESUME HERE` but not the top-of-file hint (or
vice versa — order in the file determines which one `find_resume_here()` treats as authoritative); the
stale one was read, its leftover text (`'(§4) = PR1a.'`) didn't key-match any tracker row, and the turn
gated on "unit not found." This is an **authoring-discipline gap with no automated check**, not a
regex/parsing defect — §2.3 below fixes the actual cause.

---

## 2. Target design

### 2.1 Distinguish "no progress" from "progress, no PR" — don't just delete the gate

Replace the single boolean `opened_pr` with a richer signal computed in `_compute_advance_signal()`:

- **`pr_opened`** (unchanged) — one of the three PR tools fired. Still triggers the existing
  one-PR-per-turn `pr_boundary` stop in `turn_convergence.py` — untouched.
- **`made_progress`** (new) — the turn's tool trace contains at least one *side-effecting* tool call
  (write/admin action, per `app/policy.py::classify_action` — the same WRITE/ADMIN classification
  already used for the governor gate) **or** a direct commit to a repo (`git_push_changes`,
  `upload_file_to_github`) **or** an explicit self-report of success the turn itself asserts (the
  final-message convergence text, already parsed elsewhere for the "✅ Done this turn" report). A
  turn with `made_progress=True` and no error signal converged, even without a PR.
- **`no_progress`** — neither `pr_opened` nor `made_progress`: this is the actual "broken turn" case
  §1.2 exists to catch, and **keeps gating exactly as today.**

`next_action()`'s signature becomes `next_action(plan_text, *, pr_opened: bool, made_progress: bool,
run_to_uat: bool = False)`. Gate only on `no_progress` (`not pr_opened and not made_progress`); the
existing `pr_boundary`/always-stop/UAT/gate-marker logic downstream is otherwise unchanged.

### 2.2 Gary's stated default: "in the handoff JSON → auto-advance until a gate"

This is already the *intended* design per `SOPHIA_AUTO_ADVANCE_PLAN.md`'s own 2026-06-23 revision
("Default = auto... Sophia STOPS only when [irreversible/outward, explicit gate, non-convergence, or
can't locate the unit]") — §2.1 above is what makes that promise actually true for PR-less units. No
new policy is being invented; this closes the gap between the stated policy and what the code
currently enforces.

### 2.3 Eliminate the duplicate-marker drift class (incident #2, corrected)

Two options, not mutually exclusive — recommend both, cheapest first:

1. **Detect drift automatically (defensive, do this regardless).** `find_resume_here()` already scans
   every line for the marker; instead of silently keeping only the last match, collect **all**
   matches. If more than one exists and they disagree, that's exactly the failure mode that just
   happened — surface it as a `gate` with a clear reason ("multiple RESUME HERE markers disagree:
   '<a>' vs '<b>' — fix the plan before continuing") instead of silently picking one and failing
   key-lookup downstream with an opaque "unit not found." Turns a confusing gate into a
   self-explanatory one; small, isolated, testable with the literal incident string as a repro.
2. **Remove the duplication at the source (bigger, optional).** If the top-of-file hint's only purpose
   is a quick visual pointer, consider dropping it from the convention entirely — one canonical
   `RESUME HERE`, in the tracker, full stop. Removes the bug class rather than detecting it, at the
   cost of losing the "hint at a glance" convenience. Worth a governor opinion (§6) rather than
   deciding unilaterally, since it's a workspace-wide plan-authoring convention change, not just a
   code fix.

### 2.4 Related finding, filed separately: `merge_pr`'s CI-readiness check

Surfaced live in the same thread, same session: `merge_pr` refused a docs-only `agentic_ai_context` PR
touching only `sophia/` + `plans/`, reading CI as "pending," when `validate-handoff-manifest.yml` is
`paths:`-filtered to `handoffs/**` + `scripts/**` — no check was ever going to fire for that PR's
changed files. Same root shape as §2.1 (a correct, converged outcome misread as unfinished) but a
different tool/code path (the merge gate, not the auto-advance gate) — **not folded into this plan's
PR sequence; filed as its own `OPEN_FOLLOWUPS.md` entry** (§7) so this plan stays scoped to
`auto_advance.py`.

### 2.5 What does NOT change

- One-PR-per-turn discipline (`pr_boundary` in `turn_convergence.py`) — untouched. A turn that opens a
  PR still stops there; the fix is only about turns that legitimately complete *without* one.
- All existing always-stop categories (§5c: deploy/promote, TDG/money, UAT, explicit `gate:` markers)
  — untouched, still hard gates regardless of `made_progress`.
- The `no_progress` (genuinely stuck) case — still gates, still gets a human "go" (or the existing
  "retry once, then escalate" handling), exactly as today.

---

## 3. Pre-flight — verify before PR1 (§5d completeness gate)

1. **Capture the exact plan text that produced incident #2** (`'(§4) = PR1a.'`) from
   `SPRINT_TRUESIGHT_ME_BOARD_PROPOSAL.md`'s git history around the time of the halt, so §2.3's fix is
   written against a real repro, not a guess.
2. **Confirm `app/policy.py::classify_action`'s WRITE/ADMIN tool set is the right proxy for
   "made progress"** — read it fully; some WRITE-classified tools (e.g. a failed/no-op write that
   still executed) might need excluding. List any exclusions explicitly rather than assuming the set
   is clean.
3. **Find and read the existing `tests/test_auto_advance.py`** in full (this session confirmed it
   exists, ~30 tests, including `test_next_action_gate_when_no_pr_opened` — a test whose *name and
   assertion* this change directly invalidates and must update deliberately, not break silently).

✅ **Pre-flight Completeness:** all three items are code-only reads any executing agent resolves
directly. No human decisions block PR1.

---

## 4. Sequenced execution roadmap (one PR per turn — §5a)

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | Pre-flight completion: resolve §3 items 1–3. No code. | auto |
| **PR1** | `app/auto_advance.py` + `app/main.py`: implement §2.1's `made_progress` signal and the updated `next_action()` signature. Update `test_next_action_gate_when_no_pr_opened` to reflect the new behavior (keep a `test_next_action_gate_when_no_progress_at_all` case for the still-gated true-failure path) + add tests for the `made_progress`-but-no-PR case. | auto |
| **PR2** | `app/auto_advance.py`: implement §2.3 option 1 (detect + gate-with-clear-reason on disagreeing multiple `RESUME HERE` markers), with a regression test using the literal incident string (§3 item 1). Option 2 (drop the duplicate-marker convention entirely) is deferred to §6 — not this PR unless Gary picks it. | auto |
| **PR3** | Deploy to the box (PR1/PR2 are self-merged directly, no human step — see the 2026-09-15 update above; deploy itself follows the existing "verify healthy after restart, not just that the command ran" discipline). | **`gate: human`** — merging PR1/PR2 no longer needs a human, but **restarting the live service still does**: that's the deploy action, a separate thing from merging, per the same 2026-09-15 decision |
| **PR4** | UAT (§5) on a scratch handoff thread with a throwaway plan containing at least one deliberately PR-less unit. | auto (post-deploy) |
| **PR5** | Docs: note the fix in `SOPHIA_AUTO_ADVANCE_PLAN.md`'s own history (append, don't rewrite its resume tracker) and in `SUPERVISOR_LOOP.md` if the state-reading guidance references the old behavior anywhere. | auto |

**RESUME HERE → PR0.**

---

## 5. UAT

- **U1** — On a scratch plan with a unit whose scope is explicitly "no code, verify only" (mirrors
  real PR3 from the sprint-board plan), confirm Sophia completes it and **auto-advances** to the next
  `auto` unit without a human `go`.
- **U2** — On the same scratch plan, deliberately induce a real failure (a tool call that errors, or a
  unit with no actionable next step) and confirm she **still gates** — §2.1's `no_progress` path must
  remain intact.
- **U3** — Confirm one-PR-per-turn discipline is unaffected: a unit that opens a real PR still stops
  there (`pr_boundary`), does not chain into the next unit in the same turn.
- **U4** — Re-run the exact incident #2 plan text (or the regression test from PR2) and confirm the
  resume-tracker parse now correctly locates the row.
- **U5** — Confirm all existing `tests/test_auto_advance.py` cases pass (updated ones deliberately, all
  others unchanged) — this is a control on Sophia's core safety logic; no accidental behavior change
  outside §2.1/§2.3's explicit scope.

---

## 6. Open decisions

**One.** §2.3 option 2: drop the top-of-file `RESUME HERE` hint entirely (one canonical marker, in the
tracker only) versus keeping the duplication and just detecting drift (§2.3 option 1, in PR2
regardless). This is a workspace-wide plan-authoring convention, not just a code change to
`truesight_autopilot` — affects every plan doc, not only this repo. Recommend deciding once PR2's
drift-detection has been live for a while and it's clear whether the duplication keeps causing
trouble or option 1 alone is enough. Not a blocker for PR0–PR5 below.

Everything else is a bug-fix/gap-closure against `SOPHIA_AUTO_ADVANCE_PLAN.md`'s own already-approved
2026-06-23 design intent (§2.2) — it doesn't introduce new policy, it makes existing policy actually
hold for a class of units (PR-less) the original implementation didn't anticipate.

---

## 7. Rollout

Per the pattern established for every other roadmap this session: **park in a new Telegram topic** for
a supervisor to pick up. **Merging PR1/PR2 no longer needs a human** (2026-09-15 update, top of this
doc) — Sophia self-merges directly, same as a docs-only `agentic_ai_context` PR. **PR3 (deploy —
restarting the live service) remains an explicit always-stop regardless** — that's a separate action
from merging. RESUME HERE (§4) = PR0.
