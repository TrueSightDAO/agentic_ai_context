# Fazenda São Jorge Media Task — execution plan (thread 19930)

**Created:** 2026-09-06 (Sophia) at Gary's request · **Handoff:** 👍 GO on resume-awaiting (thread 19930)
**Status:** executing — PR1–PR6 delivered; **UAT gate open** (beta review → prod sync on Gary GO)

## Goal
1. Establish the plot for https://agroverse.shop/farms/fazenda-sao-jorge-bahia/index.html on truesight.me's SunMint page (impact map) — cross-link BOTH ways (farm page ↔ sunmint).
2. See if anything interesting in the new media — add to the media gallery for São Jorge's page.
3. Add to the media archive pipeline (MAP) with manifest updated for future reference: latitude/longitude, creation date, and transcription info.

## Source media
- `~/sao_jorge_fazenda.zip` (1.5 GB) = **36 HEIC + 67 MOV = 103 files**, **100% GPS coverage**, 0 duplicates (52 unique geotagged points).
- **Two visits:** 2023-06-06 (31 HEIC + 31 MOV) and 2023-09-21 (5 HEIC + 36 MOV).
- Location: **Itajuípe / Itabuna, Bahia** (cabruca region, Coopercabruca cooperative) — NOT Pará. São Jorge is the source farm for shipment **AGL6**.
- Extent: lat −14.6544…−14.6288, lon −39.4029…−39.3921 → convex hull ~64.7 ha, centroid −14.6361, −39.3992.
- Extract at `/media/sao_jorge_work/extracted/`; metadata rows `/tmp/sao_jorge_rows.json`; analysis complete (2026-09-02).

## Targets & state (verified 2026-09-02/06)
| Target | Repo | State |
|---|---|---|
| `farms/fazenda-sao-jorge-bahia/` | agroverse_shop_beta | index.html + media.json (schemaVersion 1: 2 YT videos sLNS9pZUBVw/33nwH67UIag + 2 images). Leaflet map pin −14.6289989,−39.4028297. No SunMint cross-link yet. |
| `sunmint.html` | truesight_me_beta | Impact map loads `sunmint/plots/index.geojson`; popup shows "View farm profile on Agroverse ↗" when feature has farm_id (FARM_SLUG map: santa-anna-fazenda, rancho-maranta; fallback = raw farm_id). |
| `sunmint-tree-planting-pledges/agl6/` | truesight_me_beta | AGL6 pledge page exists (São Jorge is AGL6's source farm). |
| `sunmint/plots/index.geojson` | sunmint (api-only) | 5 real plots (RM-P1/P2, SA-P1, CL-P1, LD-P1) + test rows. No SJ plot. Machine-regenerated daily from SunMint Plots sheet → **sheet row is the durable write**. |
| `SunMint Plots` tab | sheet 1qbZZhf-… | Headers include Plot ID/Farm ID/Plot Name/Hectares/Status/Boundary Authority/Owner/Region/Verified At/Media/Notes/Coordinates/Lat/Long. Write OK via agroverse_qr_code_manager SA (verified 2026-09-02). |
| `farm_media_manifests` | farm_media_manifests | oscar-bahia.json extended schema to **v2** (creation_date, transcription_status) — commit fazenda-sao-jorge-bahia.json v2 + index entry, **no schema change needed**. |
| `farm-media-raw/` | farm-media-raw (api-only) | cleide, la-do-sitio, rancho-maranta, santa-anna — add fazenda-sao-jorge-bahia/ later (Contents-API only). |
| `/media/media_archive_inbox/farm-media/` | box | cleide, jedielcio, paulo-la-do-sitio, santa-anna — inbox dir fazenda-sao-jorge-bahia/ created. |

## Execution order (ONE PR PER TURN)
- **PR1** (this plan, agentic_ai_context) → **PR2** farm_media_manifests: `fazenda-sao-jorge-bahia.json` manifest (v2 schema, 103 items, transcription_status=pending) + index.json entry → **PR3** SunMint Plots sheet row SJ-P1 + regenerate `sunmint/plots/index.geojson` + `farms/index.json` (sunmint, Contents-API) → **PR4** agroverse_shop_beta: media.json gallery additions (3 web JPEGs from visits) + SunMint impact-map cross-link → **PR5** truesight_me_beta: AGL6 pledge page ↔ farm page + sunmint.html farm_id wiring → **PR6** photos → farm-media-raw + inbox sidecars + MOV→MP4 transcode → daemon upload (long pole, ~6/day quota) → **UAT gate** (Gary reviews beta, then prod sync on explicit GO).

## Media pipeline notes
1. Photos (36 HEIC) → web JPEGs for gallery + full-res originals → farm-media-raw/fazenda-sao-jorge-bahia/photos/ (Contents-API only).
2. Videos (67 MOV) → MOV→MP4 transcode (ffmpeg, GPS re-inject via exiftool — verify) → inbox sidecars (farm-media-daemon schema + creation_date) → daemon uploads ~6/day → yt_ids backfilled.
3. Manifest commit after first yt_ids land (v2 schema already includes lat/long + creation_date + transcription fields).
4. Transcription (faster-whisper) is a future MAP step — transcription_status=pending for all items now.

## Plot feature (SJ-P1, for PR3)
```json
{"plot_id":"SJ-P1","farm_id":"fazenda-sao-jorge-bahia","name":"Fazenda Sao Jorge Plot 1 (cabruca groves)","hectares":64.7,"status":"proposed","boundary_authority":"approx","owner":"Matheus & Mailan (Coopercabruca)","region":"Itajuibe, Bahia","notes":"Hull of 103 geotagged media (36 HEIC + 67 MOV, visits 2023-06-06 + 2023-09-21): lat -14.6544..-14.6288, lng -39.4029..-39.3921. Cabruca cacao groves; AGL6 source farm. Approx 64.7 ha hull; boundary authority approx - needs walk/CAR."}
```
GeoJSON polygon (lng,lat, closed): [[-39.3925,-14.6544],[-39.402517,-14.630406],[-39.4027,-14.6299],[-39.4029,-14.6288],[-39.4023,-14.6291],[-39.4002,-14.6312],[-39.3983,-14.6333],[-39.3921,-14.6516],[-39.3925,-14.6544]]

farm_id == agroverse slug → popup farm link works without FARM_SLUG edit (fallback uses farm_id as-is).

## Gates
- NEVER deploy prod without Gary GO. Beta preview first (beta.agroverse.shop, beta.truesight.me).
- sunmint repo is api-only → upload_file_to_github, never branch-edit. farm-media-raw also api-only.
- SunMint Plots sheet is the durable plot source (daily rebuild) — geojson direct edit alone gets overwritten.
- YouTube quota ~6/day unverified → pace expectations; do NOT hammer.

## RESUME HERE
**PR1–PR6 all delivered (2026-09-07/08).** Manifest v2 + index ✓ (PR2); SJ-P1 plot in source sheet + geojson ✓ (PR3); farm page gallery + cross-link ✓ (PR4); AGL6 ↔ sunmint wiring ✓ (PR5); media long pole complete ✓ (PR6): 67/67 MP4 uploaded w/ yt_ids merged to main (farm_media_manifests#2, sha 5ae619a9), 36 HEIC archived to farm-media-raw/photos (36), inbox sidecars in place. Manifest on main = 103 items (67 PUBLISHED w/ yt_id, 36 PENDING photos).

**UAT GATE OPEN — next action is Gary:** review beta surfaces (beta.agroverse.shop farms/fazenda-sao-jorge-bahia gallery incl. 36 photos + Leaflet map; beta.truesight.me AGL6 pledge page ↔ farm page cross-links; sunmint SJ-P1 plot on impact map), then explicit GO → sync_beta_to_prod.
