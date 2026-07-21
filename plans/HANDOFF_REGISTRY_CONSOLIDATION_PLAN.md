# Handoff registry consolidation — plan

**Status:** executing (single interactive session, no Sophia handoff needed — this is a
same-turn fix, not a multi-turn parking).

## Problem

`handoffs/HANDOFF_MANIFEST.md` and `sophia/SOPHIA_HANDOFFS.md` both hand-maintain an
overlapping registry table (Plan file / Handoff title / Status / date). They have already
drifted, confirmed by inspection on 2026-07-18:

- **`LARGE_SPIKES_CARD_FIX_AND_CHART_LEGIBILITY_PLAN`** — Manifest: `SUPERSEDED — already
  implemented`. SOPHIA_HANDOFFS: `DRAFTED — awaiting thread + governor GO`. Verified via
  `sentiment_importer` git log: PR #1124 (`bf97824f`) and #1125 (`898db920`) are both merged
  to `master`. **Manifest is correct; SOPHIA_HANDOFFS is stale.**
- **`SOPHIA_CONTRIBUTION_SCORING_PLAN`** — Manifest: `in progress` (detailed narrative: bulk
  of 906-row backlog processed, ~475 approved). SOPHIA_HANDOFFS: `draft — awaiting governor
  §10 + GO`. Same drift pattern; Manifest's narrative is more recent/detailed, trusted.
- **`message_thread_id` 2622 reused across three different plans** —
  `RESEND_VERIFICATION_PLAN` (2026-06-08), `SOPHIA_FOLLOWUP_MONITOR_PLAN` (2026-06-11), and
  `SANDBOX_THEOBROMA_1_HANDOFF_DEMO` (2026-06-07) all cite thread 2622 in SOPHIA_HANDOFFS.
  Almost certainly a copy-paste error in the source registry — silent until someone clicks
  through to the wrong topic.

Root cause: two files, one conceptual record, no mechanical check — drift is only caught by
a human noticing disagreement.

## Fix

Make `HANDOFF_MANIFEST.md` the **single source of truth**. Add `Telegram topic` +
`message_thread_id` columns to it (pulled from SOPHIA_HANDOFFS). Strip the duplicate table
out of `SOPHIA_HANDOFFS.md`, keeping only the Sophia-specific trigger protocol (GO
convention, trigger template, thread management rules) — content that has no other home.
Add a validator script + tests so schema/consistency drift is caught by CI, not eyeballing.

## Sequenced units (single PR — no handoff, executing directly)

1. Merge tables into `handoffs/HANDOFF_MANIFEST.md`:
   - Add `Telegram topic` / `message_thread_id` columns.
   - Conflicts resolved per "Problem" above; ambiguous thread_id reuse marked
     `NEEDS VERIFICATION (see PR)` rather than guessed.
2. Slim `sophia/SOPHIA_HANDOFFS.md`: drop the `## Registry` table, replace with a pointer
   to `HANDOFF_MANIFEST.md`; keep runbook (trigger template, GO convention, thread rules).
3. Update `handoffs/HANDOFF_PROTOCOL_OVERVIEW.md` pointers to match.
4. Update `OPERATING_INSTRUCTIONS.md` — the two "what to read" table rows for
   `HANDOFF_MANIFEST.md` and `SOPHIA_HANDOFFS.md` (protected canonical file per §3; called
   out explicitly here and in the PR description since this is a direct, small consequence
   of the approved fix, not a scope-creep edit).
5. `scripts/validate_handoff_manifest.py` — stdlib-only markdown table parser + rules:
   required columns present; no duplicate `Plan file` rows; `Status` is a documented enum
   value (cross-checked against the `## Status values` legend); `Telegram topic` /
   `message_thread_id` are both-or-neither per row; no `message_thread_id` reused across
   distinct `Plan file` rows.
6. `scripts/tests/test_validate_handoff_manifest.py` — unit tests, one fixture per rule
   (valid + broken case each).
7. `scripts/tests/test_validate_handoff_manifest_integration.py` — runs the validator
   against the real committed Manifest end-to-end.
8. `.github/workflows/validate-handoff-manifest.yml` — CI gate on PRs touching
   `handoffs/HANDOFF_MANIFEST.md`.

## Pre-flight completeness

✅ No execution unit requires reading a file/state not already captured above: the two
source tables were read in full in-session, the drift was verified against real git history
(`sentiment_importer` PRs #1124/#1125), and no other repo's state is needed to execute any
of units 1–8.

## Resume tracker

Single session, single PR — no resume tracking needed across turns. If interrupted, resume
at the first unchecked unit below.

- [ ] 1. Merge Manifest table
- [ ] 2. Slim SOPHIA_HANDOFFS.md
- [ ] 3. Update HANDOFF_PROTOCOL_OVERVIEW.md
- [ ] 4. Update OPERATING_INSTRUCTIONS.md rows
- [ ] 5. Validator script
- [ ] 6. Unit tests
- [ ] 7. Integration test
- [ ] 8. CI workflow
- [ ] 9. Local test run green, commit, push, open PR (no merge — human reviews)

## UAT

n/a — this is a documentation/tooling change with no human-facing product surface. Covered
by: unit tests (validator logic) + integration test (validator against real file) + CI gate
(future PRs). Human acceptance = Gary reviewing the merged table for the reconciled/flagged
rows above and confirming the `NEEDS VERIFICATION` thread_id calls before relying on them.
