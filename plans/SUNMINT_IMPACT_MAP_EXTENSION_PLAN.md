# SunMint Impact Map Extension — implementation plan, roadmap & checklist

> **Purpose:** extend `beta.truesight.me/sunmint.html` (the SunMint impact map page)
> so plots/farms are first-class, auditable objects: farms selectable/filterable,
> plot popups enriched with boundary authority + status + media evidence, and a
> Farms Registry section aggregating plot data. Beta-first; prod promote only with
> explicit governor approval (plan §3f rule).

## 1. Scope

### In scope
1. **Farms selector/filter** — a dropdown of farms (derived from `plots/index.geojson`
   `farm_id`s + a future `farms/index.json` when it exists) that filters visible
   plot polygons + tree markers to that farm.
2. **Enriched plot popups** — show `boundary_authority` (approx | gps_walk | car |
   incra), `status` (proposed | planted | verified), `hectares`, `owner`, `region`,
   `verified_at`, and media thumbnails (from `media` array) in the plot popup.
3. **Farms Registry section** — a compact table/cards listing farms: farm name,
   plots count, total hectares, latest status, region (aggregated from plots).
4. **Legends + status styling** — a legend for boundary authority tiers and plot
   status; visual distinction (color/opacity) between proposed vs planted vs verified.

### Out of scope (this plan)
- Farmer-app boundary capture UI (`sunmint_beta` farmer app — separate plan/thread).
- `extract_plot_gps.py` GPS→polygon automation (`sunmint` repo — separate PR).
- Farms registry source-of-truth changes (SunMint Plots sheet stays canonical).
- Any PRODUCTION repo edits (`truesight_me_prod` untouched; promote via sync only).

## 2. Current state (pre-flight facts, 2026-08-31)

### Page
- `truesight_me_beta/sunmint.html` (40,784 bytes) — sections: problem, solution,
  impact registry, highlights, impact-map.
- Impact map: Leaflet, `#impactMap` (480px), trees markers (`trees/index.geojson`),
  plot polygons (`plots/index.geojson`), `#plotSelector` chips, `#viewSelector`,
  satellite overlay toggle (`#satOverlayToggle`), layer buttons (Satellite/Map),
  PILOT_CENTER fallback, CDN fallback URLs, `?cb=` cache-busters.
- Plot chips: colored pills (PLOT_COLORS), click → `flyToBounds`, exclusive selection
  vs view chips. Popup currently: name + hectares + status only.

### Data sources (all live, verified 200)
| Source | URL | Contents |
|---|---|---|
| Trees | `sunmint/trees/index.geojson` | 1 tree (GPS point, species, status) |
| Plots | `sunmint/plots/index.geojson` | 2 plots: RM-P1 (planted, walk-approx), RM-P2 (proposed, approx) |
| Satellite | `sunmint/satellite/manifest.json` | Sentinel-2 scenes per grid cell (date, cloud, asset) |
| Source of truth | SunMint Plots sheet (1qbZZhf…) | Plot ID, Farm ID, Plot Name, Hectares, Status, Boundary Authority, Owner, Region, Verified At, Media, Notes, Coordinates |

### Plot schema (plots/index.geojson feature properties)
`plot_id`, `farm_id`, `name`, `hectares`, `status` (proposed|planted|verified),
`boundary_authority` (approx|gps_walk|car|incra), `owner`, `region`, `verified_at`,
`media` (array of `images/<plot_id>/…` paths), `notes`. Geometry: Polygon, [lng, lat].

## 3. Constraints (rules)
- **Beta-first (§3f):** all changes to `truesight_me_beta`; prod promote only after
  governor approval via `sync_beta_to_prod`.
- **ONE PR PER TURN** — execute one PR, report, stop; next unit in a fresh turn.
- **Local test suite** before pushing (compile, ruff lint, ruff format, pytest).
  Static HTML/JS changes: verify tags balanced + JS `node --check` where feasible.
- Data stays machine-generated from the sheet (no hand-edits to geojson).
- No new backlog files; gaps → OPEN_FOLLOWUPS.md.

## 4. Roadmap (ONE PR PER TURN)

| # | Deliverable | Repo | Depends on |
|---|---|---|---|
| **PR0** | This roadmap + manifest row | agentic_ai_context | — |
| **PR1** | Enriched plot popups (boundary authority, status, hectares, owner, region, verified_at) + legend chips | truesight_me_beta | PR0 |
| **PR2** | Farms selector/filter dropdown (farm → filter plots + trees) | truesight_me_beta | PR1 |
| **PR3** | Farms Registry section (table/cards aggregated from plots) | truesight_me_beta | PR2 |
| **PR4** | Status styling + boundary-authority legend + media thumbnails in popups | truesight_me_beta | PR3 |
| **PR5** | **`gate: UAT`** — 7-step check on beta.truesight.me/sunmint.html | truesight_me_beta | PR4 |
| *(post-UAT)* | Promote to prod (`sync_beta_to_prod truesight_me_prod`) **only with governor approval** | — | UAT pass |

## 5. Checklist

### PR1 — Enriched plot popups
- [ ] Read current popup builder in `sunmint.html` (`bindPopup` in `loadPlots`)
- [ ] Add boundary_authority label (approx|gps_walk|car|incra) with friendly text
- [ ] Add status, hectares, owner, region, verified_at lines
- [ ] Add legend chip(s) in `#plotSelector` area or controls
- [ ] Verify tags balanced + JS syntax; run local suite (compile/lint/format)
- [ ] Open PR, report URL

### PR2 — Farms selector/filter
- [ ] Derive unique farms from plots `farm_id` (+ fallback to owner)
- [ ] Add `#farmSelector` dropdown (All farms + each farm)
- [ ] Filter polygons + tree markers on selection; clear on All
- [ ] Keep plot-chip/view-chip interplay working
- [ ] Open PR, report URL

### PR3 — Farms Registry section
- [ ] Add `#farms` section (cards/table) fed from same plots data
- [ ] Aggregate: farm name, plots count, total ha, status mix, region
- [ ] Link/scroll from farms dropdown or nav
- [ ] Open PR, report URL

### PR4 — Status styling + legend + media
- [ ] Color/opacity by status (proposed dashed/light, planted solid, verified filled)
- [ ] Boundary-authority legend (approx/gps_walk/car/incra)
- [ ] Media thumbnails in popups (from `media` array; CDN fallback for images)
- [ ] Open PR, report URL

### PR5 — UAT gate (7 steps on beta.truesight.me/sunmint.html)
- [ ] Page loads, map renders, trees + plots visible
- [ ] Plot popups show full detail (boundary authority, status, ha, owner, region, verified_at)
- [ ] Farms dropdown filters plots/trees correctly; All restores
- [ ] Farms Registry section shows aggregated farms
- [ ] Legend renders; status styling distinct
- [ ] Media thumbnails load (fallback OK)
- [ ] No console errors; offline still renders (SW/service already live on sunmint site)

## 6. Do / Don't
- **Do** keep data machine-generated; never hand-edit `plots/index.geojson`.
- **Do** preserve existing behaviour (plot chips, view chips, satellite toggle, CDN fallbacks).
- **Do** keep changes additive and small (one improvement per PR).
- **Don't** touch `truesight_me_prod`; don't self-promote without governor approval.
- **Don't** create variant plan/backlog files.

## 7. Related
- `SUNMINT_PLOTS_REGISTRY.md` — plots registry runbook (schema, boundary tiers, seed data)
- `sunmint/plots/index.geojson` + `scripts/build_plots_geojson.py` — data + generator
- `HANDOFF_MANIFEST.md` — this plan's row (thread 11074)
