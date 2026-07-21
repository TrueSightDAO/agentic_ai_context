# Handoff Auto-start — plan

**Status:** executing (single interactive session).

## Problem / goal

Today, every handoff parks Sophia in a Telegram topic with a kickoff message ending
in "Reply 'go for it' and I'll execute" — she then waits for an explicit governor
go-signal before touching RESUME HERE. Gary asked whether a handoff could instead
have her skip that wait for specific plans: post the kickoff, then immediately start
executing and post progress into the thread as she goes, with no human-in-the-loop
prompt needed to *begin*.

## Design decision (discussed with Gary before this plan)

Make it an **opt-in, plan-level marker** (`Auto-start: yes`) rather than removing the
wait globally. Reasoning surfaced in conversation: the initial go-for-it is the one
point where a human confirms a plan is still *current* before Sophia commits real PRs
to it — this session's own `LARGE_SPIKES_CARD_FIX_AND_CHART_LEGIBILITY_PLAN` would
have been redundant work if auto-executed on trigger, since another fix had already
landed by the time anyone looked. Opt-in keeps that safeguard the default while
letting routine/low-risk plans skip the wait.

**Auto-start does NOT relax §5c always-stop gates** (prod deploy, default-branch
merge, TDG/money, UAT) or any per-unit `gate:` marker — it only removes the initial
"wait for a human to say go" step before the *first* unit.

## Pre-flight

- **Registry schema** (`agentic_ai_context/handoffs/HANDOFF_MANIFEST.md`): current
  columns are `Plan file | Handoff title | Handoff date | Status | Telegram topic |
  message_thread_id | Resume tracker state | Last manifest update` (8 columns,
  consolidated 2026-07-20/21, see `HANDOFF_REGISTRY_CONSOLIDATION_PLAN.md`). Adding a
  9th column: `Auto-start` (yes/no), inserted after `message_thread_id`.
- **Resolver code** (`truesight_autopilot/app/telegram_adapter.py`):
  `_parse_handoff_plan(registry_text, thread_id) -> str | None` is a schema-position-
  agnostic scanner (matches thread_id via any cell, excludes terminal-status rows via
  `_TERMINAL_STATUS_MARKERS`) — used by two DIFFERENT test fixtures with two
  DIFFERENT column layouts (`tests/test_handoff_prefix.py`'s 8-column fixture and
  `tests/test_telegram_topic.py`'s older 7-column `_REG` fixture, the latter with no
  header/separator row at all in one test case). Any change must not require a
  specific header shape to keep matching the plan filename — confirmed by re-reading
  both fixtures in full during this pre-flight.
- `_handoff_prefix(thread_id, text)` injects context per-message; this is where the
  auto-start-vs-wait instruction text branches.
- `sophia/SOPHIA_HANDOFFS.md` documents the trigger-message template and the "what
  the trigger MUST tell Sophia" steps (create/reuse topic, post kickoff, end with GO
  prompt, wait) — this is prompt-driven, not code: the very FIRST turn of a NEW
  handoff runs in the `ping_sophia` session, before the Telegram thread/thread_id
  exists, so `_handoff_prefix`'s registry lookup can't apply to it. Auto-start
  behavior for a brand-new handoff must therefore be requested in the trigger
  message itself (reading the plan file's own `Auto-start: yes` marker) — the code
  change in `telegram_adapter.py` only covers *rejoining* an already-registered
  auto-start thread (redeploys, follow-up messages).
- No merge/deploy in this plan — docs + code + tests only, PRs opened for review,
  not merged (matches this session's established pattern of opening PRs and letting
  the governor decide when to merge).

✅ Pre-flight Completeness: no execution unit requires reading a file/state not
already captured above.

## Sequenced units

1. **agentic_ai_context**: add `Auto-start` column to `HANDOFF_MANIFEST.md` (default
   `no` for all 22 existing rows — none are currently opted in); update
   `scripts/validate_handoff_manifest.py` (new required column + yes/no value check)
   with new unit tests; update `sophia/SOPHIA_HANDOFFS.md` (document the marker +
   an auto-start trigger-message template variant) and
   `handoffs/HANDOFF_PROTOCOL_OVERVIEW.md` (note the option in the flow); a short,
   explicitly-flagged addition to `OPERATING_INSTRUCTIONS.md` (§5f) documenting the
   marker's relationship to §5c gates. No merge — PR opened for review.
2. **truesight_autopilot**: add `_parse_handoff_plan_and_flags()` (additive, doesn't
   touch `_parse_handoff_plan`'s existing logic — new function, independent scan) +
   `_handoff_plan_and_auto_start_for_thread()` (refactors `_handoff_plan_for_thread`
   into a thin wrapper, preserving its existing signature/behavior for any other
   caller) + branch in `_handoff_prefix()` for the auto-start instruction text.
   New unit tests covering: auto-start row resolves True, non-auto-start / missing
   column resolves False, old-schema fixtures (no `Auto-start` column, and the
   single-line-no-header fixture) still resolve False without crashing, and
   `_handoff_prefix`'s two message variants. No merge — PR opened for review.

## Resume tracker

- [ ] 1. agentic_ai_context: schema + validator + docs, tests pass, PR opened
- [ ] 2. truesight_autopilot: resolver code + tests pass, PR opened

## UAT

Human-facing (changes Sophia's live Telegram behavior) — **not run by Claude in this
session**, since it requires triggering a real handoff against production Sophia.
When Gary is ready: pick a genuinely low-risk plan, mark it `Auto-start: yes` in both
the plan file and its `HANDOFF_MANIFEST.md` row, trigger via `ping_sophia` with a
message telling her to check the plan's Auto-start marker, and confirm she posts a
kickoff AND begins executing RESUME HERE without a "go for it" — while still stopping
cleanly at any `gate:` marker or §5c always-stop.
