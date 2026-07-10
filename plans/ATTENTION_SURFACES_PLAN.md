# Attention Surfaces — execution roadmap

**Owner:** Gary Teh · **Started:** 2026-06-04 · **Status:** ACTIVE

Give the daily oracle reading (oracle.truesight.me → `truesight-grounding`
`[PRACTICE EVENT]`) a stable catalog of WHERE attention can go, so Sophia
(truesight_autopilot) and the draw-time advisory can map each reading's
*quality* onto concrete ecosystem surfaces and direct attention from evidence.

```
Draw (I-Ching quality + QMDJ direction)   ← the moment
        ×
Surface catalog (stable, 10 buckets)       ← the space        } Sophia picks
        ×                                                      } 1–3 surfaces
Freshness signals (snapshot pulse,         ← the urgency      } for today
Telegram events, per-surface staleness)
```

## Decisions locked (Gary, 2026-06-04)

1. **10 surfaces** following the value chain soil → governance (catalog below in `ATTENTION_SURFACES.md`).
2. **Trigram resonance layer included in v1** — Gary explicitly loves it; honest-disclaimer convention (modern synthesis, not classical practice) per `ICHING_QMDJ_EXTENSION.md`.
3. **Canonical home = this repo**: `ATTENTION_SURFACES.md` (human + embedded into snapshot) + `attention_surfaces.json` (machine).
4. **Shareable PDF** generated from the catalog (both tables — the 10-surface walk and the trigram affinities) — `ATTENTION_SURFACES.pdf` at repo root, regenerated on content change via `scripts/build_attention_surfaces_pdf.py`; copy to `~/Downloads` for WhatsApp/Feishu sharing.
5. **Zero new distribution infra**: the existing `advisory-snapshot-refresh` pipeline embeds the catalog into `ADVISORY_SNAPSHOT.md` via the `_read_operator_block` pattern, so the Grok oracle advisor sees it with no new plumbing.
6. **Sophia's prompt** gains a DAILY ORACLE READINGS — ATTENTION DIRECTION section in `truesight_autopilot/app/context.py` (`_SYSTEM_PROMPT_HEADER`): map reading → ≤3 surfaces, check the named signal before recommending, "build the tracker" when unmeasured, one next action per surface, mission tie-back.

## Design principles

- **Every surface names its tracker.** No observable signal → the recommendation is *build/refresh the tracker*, never *do more activity* (generalizes the standing check-tracking-before-recommending rule).
- **Mission traceability per surface** — each carries one line on how it advances the 10,000 hectares.
- **A reading is a compass, not a dashboard review** — at most 3 surfaces per reading.
- **Catalog stays stable; urgency stays live** (snapshot refreshes 6-hourly).

## Pre-flight

- [x] Sophia prompt location confirmed: `truesight_autopilot/app/context.py` `_SYSTEM_PROMPT_HEADER`; context files reach the box via `deploy.sh` hard-reset of `context/agentic_ai_context` (+ `read_repo_file` live-GitHub fallback)
- [x] Snapshot insertion point confirmed: `market_research/scripts/generate_advisory_snapshot.py` `_read_operator_block` pattern (after operator-metrics block)
- [x] PDF tooling: weasyprint + markdown on operator Mac
- [x] Trigram glyphs (☰☱☲☳☴☵☶☷) render via PingFang SC fallback font

## Sequenced plan + RESUME TRACKER

| Unit | Repo | Scope | Status |
|------|------|-------|--------|
| **PR0** | agentic_ai_context | This plan + `ATTENTION_SURFACES.md` + `attention_surfaces.json` + `scripts/build_attention_surfaces_pdf.py` + `ATTENTION_SURFACES.pdf` + CONTEXT_UPDATES line | merged ☑ ([#288](https://github.com/TrueSightDAO/agentic_ai_context/pull/288)) |
| **PR1** | market_research (go_to_market) | Embed catalog in `ADVISORY_SNAPSHOT.md` via `_read_operator_block` in `generate_advisory_snapshot.py` | merged ☑ ([go_to_market#151](https://github.com/TrueSightDAO/go_to_market/pull/151)) |
| **PR2** | truesight_autopilot | DAILY ORACLE READINGS section in `_SYSTEM_PROMPT_HEADER` + `ATTENTION_SURFACES.md` in the CONTEXT FILES key list | merged ☑ ([truesight_autopilot#95](https://github.com/TrueSightDAO/truesight_autopilot/pull/95)) |
| **OPS1** | — | `scripts/deploy.sh` against the box (syncs context + restarts service); verify health + prompt live | done ☑ (2026-06-05: `EC2_HOST=sophia`, service active, /health ok, prompt + catalog confirmed on box) |
| **DAO** | — | Consolidated `[CONTRIBUTION EVENT]` via dao_client | done ☑ |

> **COMPLETE** — this pass shipped end to end. Next iterations live under "Later" below.

## Later (not this pass)

- Per-surface staleness computed automatically (days since last matching event in the Telegram pulse) so "starved of attention" becomes a number.
- QMDJ doors/directions affinity layer once `ICHING_QMDJ_EXTENSION.md` ships.
- Public articulation on truesight.me as part of the `truesight-grounding` program page.
