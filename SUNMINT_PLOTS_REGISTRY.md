# SunMint Plots Registry — defining & extending plots

> **Purpose:** the one place future Sophias / other LLM agents learn how to define
> a new SunMint plot and how to extend an existing one. Mirrors the proven
> `trees/index.geojson` treasury-cache pattern, extended to polygons.

## 1. Concept

- **Plot** = a parcel of land in the SunMint program (a farm's planting area).
  It is the unit the impact map displays as a **polygon** on the satellite
  basemap (currently markers per-tree; plots add the parcel outline).
- **Registry** = `sunmint/plots/index.geojson` — a FeatureCollection of
  `Polygon` features, generated the same way `trees/index.geojson` is.
- **Farm** = the owner entity (e.g. Rancho Maranta, family of Jedielcio). A farm
  can own multiple plots.

## 2. Where things live

| Thing | Location |
|---|---|
| Plot registry | `sunmint/plots/index.geojson` (data repo) |
| Generator | `sunmint/scripts/build_plots_geojson.py` (mirrors `build_tree_geojson.py`) |
| Workflow | `.github/workflows/rebuild-plots-index.yml` (mirrors `rebuild-tree-index.yml`) |
| Source of truth | SunMint Plots sheet tab (SunMint ledger `1qbZZhf-…`) — **write access: `agroverse_qr_code_manager` + `edgar_dapp_listener` SAs** (`cypher_defense` / `tdg_scoring` verified read-only; `edgar_dapp_listener` 403 on write was 2026-08-31 only — write confirmed working 2026-09-06 for FSA-P1 row via that SA) |
| Impact map | `truesight_me_beta/sunmint.html` — draws polygons + clusters tree markers |
| Satellite | `sunmint/satellite/manifest.json` — grid cells derived from plot centroids |
| Ledger | geo-located events (TREE PLANTING EVENT at -3.29609,-52.58318 precedent) |
| Runbook | this file + `SUNMINT_E2E_RUNBOOK.md` |

## 3. Defining a NEW plot (step-by-step)

1. **Capture raw media** — photos + short videos at the plot. iPhone HEIC/MOV
   embed GPS in container metadata; **never decode video frames** to locate a
   plot (wasteful). `exiftool` reads it instantly. Note: **WhatsApp and Telegram
   strip EXIF/GPS on photo upload** — for boundary shots from a farmer, have
   them **email the photos** (attachments preserve EXIF) or send as WhatsApp
   "Document", or scp/Drive the original files.
2. **Extract GPS** — one pass over all files:
   ```bash
   exiftool -GPSLatitude -GPSLongitude <files...>
   ```
   Convert DMS→decimal (S/W negative): `3 deg 17' 45.96" S` → `-3.29610`,
   `52 deg 34' 59.39" W` → `-52.58316`.
3. **Build the boundary** — three tiers of authority:
   - `gps_walk` — walk the perimeter with any GPS-track app (~10 min); this is
     the **recommended default** and yields a real polygon.
   - `car` / `incra` — farmer's CAR (Cadastro Ambiental Rural) or INCRA
     registration gives the authoritative polygon; best if available.
   - `approx` — hull of photo/video GPS points only (quick sketch; label clearly).
4. **Add the farm** to the SunMint Farms sheet tab (farm name, family/owner,
   hectares, region). Add the plot row: plot_id, farm_id, centroid, boundary
   points, hectares, status, **plot_type** (see §4b); name the
   `plot_id` per §4c (`<SITE_CODE>_<YYYYMMDD>_<purpose>_<N>` for sub-plots).
5. **Regenerate** `plots/index.geojson` (local script or the workflow) and
   commit — same flow as the trees index.
6. **Render** — the impact map reads the new polygon automatically after the
   repo push (fallback CDN URL included).
7. **Anchor on-chain** — record a geo-located event (e.g. TREE PLANTING EVENT)
   so the parcel has a ledger identity, not just a map entry.
8. **Media** — upload photos (compressed) to `sunmint/images/...`; keep raw
   videos OUT of git (huge) — reference by Drive/URL or store thumbnails only.

## 4. Extending an EXISTING plot

- **Boundary correction** — replace the polygon with the CAR/INCRA or a proper
  walk; bump `boundary_authority` and add `verified_at`.
- **Status transitions** — `proposed → planted → verified`:
  - `planted`: tree planting events recorded at plot centroid (TREE PLANTING EVENT).
  - `verified`: satellite scene (Sentinel-2, low cloud) confirms canopy + a
    ground photo set with calibration card.
- **New media** — add photos to `sunmint/images/<plot_id>/`; update the plot's
  `media` array; never commit MOV/MP4 into the repo.
- **Hectares reconciliation** — if a walk/registry shows area < claimed (e.g.
  Plot 2 walk ≈ 2.9 ha vs 5 ha claimed), flag it; ask the farmer for the CAR
  polygon before trusting the number.

## 4b. Plot type (`plot_type`) — controlled vocabulary

`plot_type` records a plot's **role in the program** (governor decision
2026-09, thread 24326). It is the axis the impact map filters on and the axis
the tree-count estimator keys on (mature / enrichment / research plots are
**never** auto-estimated). It is **orthogonal** to `status` (lifecycle:
proposed → planted → verified) and to `boundary_authority` (evidence grade:
approx → gps_walk → car → incra) — a separate column, not an overload of either.

| value | meaning |
|---|---|
| `restoration` | net-new planting on a prior **non-forest** baseline (pasture / cleared land). Carries the additionality case. |
| `mature` | established cacao/agroforest the farmer already had (incl. cabruca, century-old groves). |
| `maturing` | an established-but-still-growing stand — canopy filling in / bearing, not yet a closed old grove (the walk-observed **middle stage**). |
| `enrichment` | **additional** trees planted into an existing stand. |
| `research` | research / trial plot — excluded from headline sequestration & 10,000-ha counts. |
| `nursery` | seedling production. |
| `infrastructure` | non-crop built area (processing yard, drying terrace, fermentary, house/compound). |
| *(blank)* | **not yet classified.** Never auto-defaulted by the generator or any writer. |

Rules:

- **Never auto-default.** A blank cell stays blank — guessing a plot's role is
  how you end up claiming a baseline you never established (the "nothing
  asserted until evidenced" credentialing-lineage principle).
- **ONE column, seven values — never split stage into a second column.** A
  walk-observed growth *stage* (`establishing`/`maturing`/`established`) was
  prototyped as a sibling `plot_stage` column and **dropped** (2026-09, thread
  24326): the authoritative `SunMint Plots` sheet uses a **single** `Plot Type`
  column and `maturing` is already typed there. Conform code to the sheet, not
  the reverse. In particular **do not** re-introduce a `plot_stage` axis — the
  test `TestSingleColumnVocabulary.test_no_separate_stage_axis` guards this.
- **`plot_type` is current-state and mutable** — a `restoration` plot becomes
  `mature` in ~15 yr. Update it when the ground truth changes.
- The *immutable* "was this land forest before?" fact (additionality baseline)
  does **not** live here. A sibling `baseline_land_use` axis was considered and
  **dropped** (2026-09): it is not walk-observable (the walk pass could not
  distinguish prior pasture from cleared forest), and `restoration` already
  encodes the non-forest-baseline claim. If formal additionality is needed later
  it belongs to a **CAR / satellite-fed credit annex**, not a plot-walk field.
- **Single canonical enum in code:** `VALID_PLOT_TYPES` in
  `sunmint/scripts/build_plots_geojson.py`. The generator **warns** (does not
  reject) on an unrecognized token and on any schema field whose sheet header is
  missing — so a tag cannot silently vanish from the registry.
- **The sheet column is a dropdown.** `SunMint Plots!G` carries a strict
  `ONE_OF_LIST` data-validation rule listing the seven values above (added
  2026-09, thread 24326), so a hand-edit in the sheet cannot introduce an
  off-vocabulary token. Programmatic writes (GAS `setValue`, DApp submissions)
  are **not** blocked by validation — the GAS off-vocab warning is the guard on
  that path.
- **Live on the sheet (2026-09-10):** the `SunMint Plots` `Plot Type` header sits
  at column **G** with its `ONE_OF_LIST` dropdown intact (rows 2+), and values are
  populated for every plot. The first `research`-typed sub-plot is
  `B-06-108_20260908_research_1` (thread 24321).
- **Write paths:** the sheet column **`Plot Type`** (header named to avoid a
  `farm`/`plot` prefix collision with `farm_id`/`plot_id` in the generator's
  column matcher), the FBE GAS handler
  (`tokenomics` `process_farm_boundary_evidence.gs`, `- Plot Type:` line, plus a
  non-fatal warning on an off-vocabulary value), the `extract_plot_gps.py
  --plot-type` CLI, and the farmer DApp
  (`sunmint_beta/limites-da-fazenda/`, `Plot Type` selector). Registries:
  `sunmint/SCHEMA.md` §Plot-type conventions (keep in sync).

## 4c. Sub-plot naming (`plot_id`) — sibling plots on one property

`plot_id` is **not** free text: §3 step 4 derives it from the **CEPOTX site
code** (see `CEPOTX_SITE_CODE_REGISTRY.md`), and a site code is issued **per
property, not per parcel**. So when a property hosts more than one plot, the site
code alone is ambiguous and the sub-plot needs a suffix.

**Canonical sub-plot rule (governor decision 2026-09-10, thread 24321):**

```
<SITE_CODE>_<YYYYMMDD>_<purpose>_<N>
```

- `<SITE_CODE>` — the real CEPOTX code; never invented or re-derived.
- `<YYYYMMDD>` — the date the **evidence was captured** (the photo/visit date),
  not the date the row was filed.
- `<purpose>` — short lowercase token for the plot's role, chosen from the §4b
  `plot_type` vocabulary (`restoration` / `research` / `enrichment` / `nursery` /
  `infrastructure`), so the id reads as its own type.
- `<N>` — 1-based sequence among same-day, same-purpose plots.

Live examples in the registry: `B-06-108_20260908_research_1` (the first
`research`-typed sub-plot), `B-06-108_20260908_1`, and
`N-06-37_20260909_restoration_1`.

Gotchas:

- **Include `<purpose>` whenever the property already has a same-day row** —
  otherwise a research plot collides with e.g. `B-06-108_20260908_1`.
- The site code stays the **prefix**, so the sub-plot still groups with its
  parent property in the sheet, the impact map, and `farms/index.json`.
- **Pre-existing ids are not retro-renamed.** Two older styles remain on purpose:
  `B-06-108_20260908_1` (bare `_N`) and
  `V-06-29-reforestation_20260907_plot_1` (`-purpose_…_plot_N`). New rows follow
  the canonical rule above; **do not invent a third style.**
- `plot_type` (column) remains the **source of truth** for role — the `<purpose>`
  token in `plot_id` is a human-readable convenience, not a substitute.

## 5. Registry schema (`plots/index.geojson`)

> Canonical schema also lives repo-side: **`sunmint/SCHEMA.md`** (plots + trees registries). Keep both in sync when columns change.

```jsonc
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {
      "plot_id": "RM-P1",
      "farm_id": "rancho-maranta",
      "name": "Rancho Maranta Plot 1 (house)",
      "hectares": 0.5,
      "status": "planted",          // proposed | planted | verified
      "plot_type": "infrastructure", // restoration | mature | maturing | enrichment | research | nursery | infrastructure (blank = unclassified; see §4b)
      "boundary_authority": "gps_walk", // approx | gps_walk | car | incra
      "verified_at": null,
      "media": ["images/RM-P1/img_7624.jpg"],
      "owner": "Jedielcio family"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[-52.583164,-3.296100], [-52.583164,-3.296053], ...]]
    }
  }]
}
```

Note: GeoJSON is `[lng, lat]` order. Polygon rings must close (first == last).

## 6. Seed data — Rancho Maranta (2026-08-30 visit)

| Plot | Location | Media | Status | Boundary |
|---|---|---|---|---|
| RM-P1 (house) | -3.29610, -52.58316 | 4 HEIC + 3 MOV | planted (TREE PLANTING EVENT at -3.29609,-52.58318) | approx (tight cluster ~35 m) |
| RM-P2 (family) | walk track -3.2934..-3.2947, -52.5768..-52.5789 | 6 HEIC + 23 MOV | proposed | approx — walk covers ~2.9 ha < 5 ha claimed → get CAR polygon |
| B-06-58 (compound; legacy SA-P1) | hull -3.291769..-3.292514, -52.571500..-52.572400, centroid -3.292243,-52.572044 | 44 HEIC/MOV | proposed | approx — photo-hull ~0.31 ha < 3 ha claimed → get Jedielcio boundary photos / CAR polygon |

## 5b. Plot popup → farm profile link (impact map)

- `sunmint.html` plot popups show **"View farm profile on Agroverse ↗"** when the
  feature carries `farm_id`, linking to `https://agroverse.shop/farms/<slug>/`.
- **Gotcha:** registry `farm_id` is the logical id (e.g. `santa-anna-fazenda`),
  NOT the agroverse page slug (e.g. `santa-anna-fazenda-para`). The popup keeps a
  `FARM_SLUG` map (`truesight_me_beta/sunmint.html`) — add new farms there or
  the link 404s. Fallback: unmapped farm_id is used as-is.

## 5c. Promoting sunmint.html to production (beta → prod)

- `truesight_me_beta` and `truesight_me_prod` **intentionally diverge on `CNAME`**
  (`beta.truesight.me` vs `truesight.me`). `sync_beta_to_prod` will refuse with a
  **merge conflict** — this is expected, NOT an error. Do NOT force.
- Resolution: GitHub UI → prod repo → fork page → **Sync fork** → merge upstream,
  resolving the CNAME conflict by **keeping `truesight.me`** (prod's value).
  Then verify the live page serves the new code (Pages deploy lag ~1-5 min).

## 7. Do / Don't

- **Do** read GPS from container metadata (exiftool), never frame-decode videos.
- **Do** keep the plot registry machine-generated from the sheet (treasury-cache pattern).
- **Do** name sub-plots `<SITE_CODE>_<YYYYMMDD>_<purpose>_<N>` (§4c) — never invent a new suffix style.
- **Do** store raw videos outside git; commit only compressed photos / thumbnails.
- **Don't** invent a polygon from a photo cluster and label it authoritative.
- **Don't** create variant backlog files — use OPEN_FOLLOWUPS.md for gaps.
- **Don't** edit PRODUCTION repos; beta-first (truesight_me_beta), promote only with approval.

## 8. Related

- `SUNMINT_E2E_RUNBOOK.md` — end-to-end SunMint flow
- `OPEN_FOLLOWUPS.md` — "SunMint satellite cache" (CDSE creds pending, Gary) — plots will feed this grid
- `truesight_me_beta/sunmint.html` — impact map implementation (#319, #320, #321, #322)
- `sunmint/scripts/build_tree_geojson.py` — the generator to mirror for plots