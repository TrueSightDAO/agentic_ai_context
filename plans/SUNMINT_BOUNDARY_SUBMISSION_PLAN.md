# SunMint Boundary Submission Pipeline — implementation plan, roadmap & checklist

> **Purpose:** build the farmer-facing boundary-capture pipeline: a farmer uploads geo-tagged
> photos of the farm plot boundary (the pillar-and-log walk Jedielcio did at Santa Anna
> Fazenda), the lat/lng embedded in those images is extracted, and a Python script creates or
> updates the plot record — which then renders on the impact map automatically. This is the
> **upstream data-capture** pipeline; the impact map (SUNMINT_IMPACT_MAP_EXTENSION_PLAN) is
> **downstream display** and is parked until this lands.

## 1. Governor design rules (confirmed 2026-09-01, thread 11074)

1. **Farm available in dropdown before the record exists in the main repo** — when a farmer
   registers a new farm, the farm must be selectable in the dropdown immediately, even if the
   farm record doesn't yet exist in `sunmint/plots/index.geojson` / the Farms sheet due to time
   lag or no internet.
2. **Boundary photo → farm dropdown; free-text fallback** — when the farmer takes a boundary
   photo, the farm is selectable; if it's not there yet, the farmer can simply type the name.
3. **Next event sees the name** — the typed/registered farm name is already an option at the
   next boundary event (device-local persistence).
4. **Backend auto-creates the farm record** — when a boundary event arrives with a new farm
   name, the backend creates the farm record and associates the boundary submission with it.
5. **Boundary = lat/lng embedded in the uploaded images** — extract GPS from the photos
   themselves (exiftool, container metadata), build the boundary polygon as the **convex hull**
   of those points, labeled `approx` until a walk/CAR/INCRA polygon upgrades it. No walk-track
   apps, no CAR dependency, no video frame decoding.

## 2. Current state (pre-flight facts, 2026-09-01)

| Fact | Value |
|---|---|---|
| Plots registry | `sunmint/plots/index.geojson` — **5 features live**: RM-P1 (planted, walk-approx, 0.4 ha), RM-P2 (proposed, approx, 5 ha), SA-P1 (proposed, approx, 3 ha), CL-P1 (proposed, approx, 114 ha), LD-P1 (proposed, approx, 5.56 ha, **8 media items**) |
| Generator | `sunmint/scripts/build_plots_geojson.py` + `.github/workflows/rebuild-plots-index.yml` (sheet → geojson) |
| Source of truth | SunMint Farms sheet tab (write: `agroverse_qr_code_manager` SA) — cols: Plot ID, Farm ID, Plot Name, Hectares, Status, Boundary Authority, Owner, Region, Verified At, Media, Notes, Coordinates |
| GPS tooling | `exiftool` installed on autopilot box (`/usr/bin/exiftool`); runbook `SUNMINT_PLOTS_REGISTRY.md` §3 documents extraction + DMS→decimal + the **WhatsApp/Telegram strip EXIF** caveat (use email attachment, WhatsApp "Document", or Drive/scp to preserve) |
| Boundary UI | **None** — `sunmint_beta` has only `index.html` + `monitor-tree-growth/index.html`; `dapp_beta` has `register_farm.html` |
| Extract script | **None** — `sunmint/scripts/` has `build_plots_geojson.py`, `build_tree_geojson.py`, `cache_satellite_scenes.py` only |
| Event catalog | No `FARM BOUNDARY EVIDENCE EVENT` in Edgar (only `FARM REGISTRATION EVENT`) |
| Offline queue | `sunmint_beta/index.html` already has IndexedDB queue + service worker (network-first, offline fallback) — the capture module rides on this |
| Media store | `sunmint/images/<plot_id>/` pattern (existing); raw videos stay OUT of git |

## 3. Constraints (rules)
- **Beta-first (§3f):** all changes to `sunmint_beta` / `sunmint`; prod promote only after governor approval.
- **ONE PR PER TURN** — execute one PR, report, stop; next unit in a fresh turn.
- **Local test suite** before pushing (compile, ruff lint, ruff format, pytest). Static HTML/JS: verify tags balanced + JS `node --check`. Python: run the suite.
- Data stays machine-generated from the sheet (no hand-edits to geojson).
- No new backlog files; gaps → OPEN_FOLLOWUPS.md.
- Media uploads: compressed photos into the repo; raw videos referenced by URL, never committed.

## 4. Roadmap (ONE PR PER TURN)

| # | Deliverable | Repo | Depends on |
|---|---|---|---|
| **PR0** | This roadmap + manifest row (impact-map row parked) | agentic_ai_context | — |
| **PR1** | `scripts/extract_plot_gps.py` — exiftool GPS → DMS→decimal → convex hull → closed polygon ring → upsert/update plot row in Farms sheet (Coordinates, Boundary Authority=approx, Media) | sunmint | PR0 |
| **PR2** | Farmer-app **"Limites da Fazenda"** capture module — farm picker (device-local union + "New farm…" free-text), camera/photo capture, offline queue, upload to `images/<plot_id>/` | sunmint_beta | PR1 |
| **PR3** | Machine-generated **farms seed** (`farms/index.json`) + union with device-local list (rules 1–3 for all devices) | sunmint | PR2 |
| **PR4** | Backend farm upsert + `FARM BOUNDARY EVIDENCE EVENT` catalog entry (rule 4 — new farm name auto-creates record) | dao_protocol / tokenomics | PR3 |
| **PR5** | **`gate: UAT`** — end-to-end: capture boundary photos → extract → plot appears on impact map | sunmint_beta / sunmint | PR4 |
| *(post-UAT)* | Promote to prod (`sync_beta_to_prod` where applicable) **only with governor approval** | — | UAT pass |

## 5. Checklist

### PR1 — `extract_plot_gps.py`
- [ ] Read `exiftool -GPSLatitude -GPSLongitude` output for a directory of images/videos
- [ ] DMS→decimal conversion (S/W negative) per runbook §3
- [ ] Convex hull (monotonic chain, stdlib only) → closed `[lng, lat]` ring
- [ ] Upsert plot row in SunMint Farms sheet (Coordinates, Boundary Authority=approx, Media list); create plot row if missing
- [ ] Regenerate `plots/index.geojson` via existing generator (or invoke workflow)
- [ ] Local suite passes; unit test with fixture media (LD-P1's 8 items as fixture)
- [ ] Open PR, report URL

### PR2 — Farmer-app boundary capture module
- [ ] Add "Limites da Fazenda" to dropdown/nav on `sunmint_beta/index.html`
- [ ] Farm picker: device-local farm names (IndexedDB) + "New farm…" free-text (rules 1–3)
- [ ] Camera/photo capture with geolocation; batch photos at boundary markers
- [ ] Offline queue (existing IndexedDB pattern); upload to `images/<plot_id>/` on reconnect
- [ ] Submit boundary evidence (farm name, media list, extracted GPS, `is_new_farm` flag)
- [ ] Tags balanced + JS `node --check`; Open PR, report URL

### PR3 — Farms seed index
- [ ] Generator `scripts/build_farms_index.py` (mirror plots generator) → `sunmint/farms/index.json`
- [ ] Farmer app fetches seed when online; unions with device-local list
- [ ] Open PR, report URL

### PR4 — Backend farm upsert + event
- [ ] Add `FARM BOUNDARY EVIDENCE EVENT` to catalog (`lookup_event_docs`); canonical labels
- [ ] Receiver: on boundary event with new farm name → create farm row, then append plot/media
- [ ] Open PR, report URL

### PR5 — UAT gate
- [ ] Capture boundary photos on beta device → photos uploaded
- [ ] `extract_plot_gps.py` builds polygon from uploaded GPS
- [ ] Plot row created/updated; `plots/index.geojson` regenerated
- [ ] Impact map shows the new polygon (farm selector picks it up)
- [ ] New farm name typed → record auto-created (rule 4)
- [ ] Offline: capture works without internet, queues, flushes
- [ ] No console errors

## 6. Do / Don't
- **Do** read GPS from image container metadata (exiftool), never decode video frames.
- **Do** label hull-of-photos boundaries `approx`; upgrade path = gps_walk / car / incra + `verified_at`.
- **Do** keep plot registry machine-generated from the sheet.
- **Don't** invent polygons and label them authoritative.
- **Don't** touch production repos; beta-first, promote only with approval.
- **Don't** create variant plan/backlog files.

## 7. Related
- `SUNMINT_PLOTS_REGISTRY.md` — runbook (schema, boundary tiers, extraction, seed data)
- `SUNMINT_IMPACT_MAP_EXTENSION_PLAN.md` — downstream display (parked until this lands)
- `sunmint/plots/index.geojson` + `scripts/build_plots_geojson.py` — data + generator
- `sunmint_beta/index.html` — farmer app (offline queue + SW already live)
- `dapp_beta/register_farm.html` — farm registration entry point
