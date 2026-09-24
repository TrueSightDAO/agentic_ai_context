# Plan A — SunMint index loud-failure fix

**Handoff:** thread 36213 (split out of 35189 at Gary's request, 2026-09-24).
**Source of truth for scope:** `OPEN_FOLLOWUPS.md` → `## Pending` → the *"SunMint index freeze"* entry.
No prior plan file existed for this work (404-checked `plans/SUNMINT_LOUD_FAILURE_*.md`).

## Problem (silent-green defect)

`sunmint/scripts/build_plots_geojson.py` and `sunmint/scripts/build_farms_index.py`
catch a sheet-read failure, log `WARN: could not read '<tab>' … preserving existing
registry`, rewrite the *previous* file, commit nothing, and **exit 0**. A transient
credential / permission failure therefore reads as **success**, and the public
indexes freeze with **no signal**. This is exactly what masked the 2026-09-17 → 09-24
outage (all three rebuilds frozen by a shared CI SA 403).

## Already resolved (do NOT re-do)

The credential half is DONE: the CI SA access was restored and the indexes were
re-dispatched / refreshed (see agentic_ai_context #1386 / #1387). Only the
loud-failure half remains.

## RESUME HERE = PR1 (repo `TrueSightDAO/sunmint`)

1. In `build_plots_geojson.py` (~L21-22, L80, L305) and `build_farms_index.py`,
   replace the swallow-and-preserve branch with a **loud failure**: `sys.exit(1)`
   (or raise) on sheet open/read error, with a message naming the tab + the SA
   credential that failed.
2. Add a **regression test** that stubs the sheet read to raise and asserts a
   non-zero exit (it must fail on `main` first).
3. Run the local suite green (`compileall` → `ruff check` → `ruff format --check`
   → `pytest -q`), then push → merge.
4. Tick the `OPEN_FOLLOWUPS.md` entry to `## Recently shipped`; report the
   contribution.

## Scope boundary

The two plots/farms generators ONLY. `cache-satellite-scenes` and
`rebuild-plot-media-index` read no sheet and are **out of scope**.
