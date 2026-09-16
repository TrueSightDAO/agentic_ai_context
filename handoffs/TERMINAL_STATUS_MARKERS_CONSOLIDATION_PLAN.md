# Terminal-Status Marker Consolidation Plan

**Status:** DRAFT — 2026-09-16. Not yet started.
**Thread:** Telegram #30954 — **Date:** 2026-09-16 — **Author:** Sophia Truesight (admin+sophia@truesight.me)

---

## 1. Problem

"Is this handoff terminal?" is answered in **three** places, with three different definitions:

| Where | Mechanism | `COMPLETE` recognised? |
|---|---|---|
| `scripts/build_handoff_index.py` `derive_state()` | regex `\bcomplet(?:e\|ed)\b` (case-insensitive) | yes (correct) |
| `app/telegram_adapter.py` `_TERMINAL_STATUS_MARKERS` | substring `"completed"` on `.lower()` | **no** (misses `COMPLETE`) |
| `app/daily_briefing.py` `_TERMINAL_STATUS_MARKERS` | hand-copied mirror of the above | **no** (misses `COMPLETE`) |

The two consumer lists trace to the **same commit `38571a1` (#438)** — `daily_briefing.py`'s own
header comment says it *mirrors* `telegram_adapter.py`. One registry, one reasoning, two copies
of the marker tuple, no shared symbol. Fixing the *data* (one manifest, 2026-07-18
HANDOFF_REGISTRY_CONSOLIDATION_PLAN) never fixed the *logic*.

### Symptoms

1. **Zombie handoff context.** `_handoff_plan_and_auto_start_for_thread` only skips a row when a
   marker matches; a `COMPLETE` row does not → the adapter keeps injecting "this topic is the
   active handoff for ... resume from RESUME HERE" after the plan is done. (Observed live in
   thread 30870 after the plan was already COMPLETE.)
2. **Daily re-surfacing.** `daily_briefing` lists any non-terminal row as "active"; a `COMPLETE`
   row leaks in and is re-nagged daily.

## 2. Fix

One predicate, one owner:

1. Add `is_terminal_status(status: str) -> bool` next to `derive_state()` in
   `scripts/build_handoff_index.py`, built on the existing `STATE_RULES` regex (not a substring
   list). Terminal states: `done`, `superseded`, `stale`, `demo · live`.
2. `app/telegram_adapter.py` and `app/daily_briefing.py` **import** it; delete both local
   `_TERMINAL_STATUS_MARKERS` tuples.
3. Point the validator's "known status keyword" logic at the same rules so warnings and derived
   state cannot disagree.
4. Tests: `COMPLETE` / `completed` / `superseded` / `stale` all recognised terminal;
   `in progress` / `blocked` not.

## 3. Scope / gates

- Repo: `truesight_autopilot` (own repo). No prod repo touched.
- ONE PR PER TURN. No money, no prod deploy — pure refactor + tests.

## 4. RESUME HERE

1. PR1: shared `is_terminal_status()` + tests; import in adapter + briefing + validator.
2. Run the three local CI steps (`compileall` / `ruff check` / `ruff format --check` / `pytest`)
   before push; confirm `--check-index` + `--check-supervision` still pass.

## 5. Roots

- Spun out of thread 30870 (Prod sales reconciliation — Linda Ford subscription renewal, COMPLETE).
