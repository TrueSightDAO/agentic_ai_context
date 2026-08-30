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
| Source of truth | SunMint Farms sheet tab (gspread via `GOOGLE_SERVICE_ACCOUNT_JSON`) |
| Impact map | `truesight_me_beta/sunmint.html` — draws polygons + clusters tree markers |
| Satellite | `sunmint/satellite/manifest.json` — grid cells derived from plot centroids |
| Ledger | geo-located events (TREE PLANTING EVENT at -3.29609,-52.58318 precedent) |
| Runbook | this file + `SUNMINT_E2E_RUNBOOK.md` |

## 3. Defining a NEW plot (step-by-step)

1. **Capture raw media** — photos + short videos at the plot. iPhone HEIC/MOV
   embed GPS in container metadata; **never decode video frames** to locate a
   plot (wasteful). `exiftool` reads it instantly.
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
   points, hectares, status.
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

## 5. Registry schema (`plots/index.geojson`)

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

## 7. Do / Don't

- **Do** read GPS from container metadata (exiftool), never frame-decode videos.
- **Do** keep the plot registry machine-generated from the sheet (treasury-cache pattern).
- **Do** store raw videos outside git; commit only compressed photos / thumbnails.
- **Don't** invent a polygon from a photo cluster and label it authoritative.
- **Don't** create variant backlog files — use OPEN_FOLLOWUPS.md for gaps.
- **Don't** edit PRODUCTION repos; beta-first (truesight_me_beta), promote only with approval.

## 8. Related

- `SUNMINT_E2E_RUNBOOK.md` — end-to-end SunMint flow
- `OPEN_FOLLOWUPS.md` — "SunMint satellite cache" (CDSE creds pending, Gary) — plots will feed this grid
- `truesight_me_beta/sunmint.html` — impact map implementation (#319, #320, #321, #322)
- `sunmint/scripts/build_tree_geojson.py` — the generator to mirror for plots