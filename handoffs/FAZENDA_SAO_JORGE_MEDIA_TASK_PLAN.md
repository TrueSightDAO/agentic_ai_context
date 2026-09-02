# Fazenda São Jorge Media Task — execution plan (thread 19930)

**Created:** 2026-09-02 (Sophia) at Gary's request · **Handoff:** 👍 GO on resume-awaiting (thread 19930)
**Status:** executing

## Goal
1. Establish the plot for https://agroverse.shop/farms/fazenda-sao-jorge-bahia/index.html on truesight.me's SunMint page (impact map) — cross-link BOTH ways (farm page ↔ sunmint).
2. See if anything interesting in the new media — add to the media gallery for São Jorge's page.
3. Add to the media archive pipeline (MAP) with manifest updated for future reference: latitude/longitude, creation date, and transcription info.

## Source media
- `~/sao_jorge_fazenda.zip` (1.5 GB) = **36 HEIC + 67 MOV = 103 files**, **100% GPS coverage**, 0 duplicates (52 unique geotagged points).
- **Two visits:** 2023-06-06 (31 HEIC + 31 MOV) and 2023-09-21 (5 HEIC + 36 MOV).
- Location: **Itajuípe / Itabuna, Bahia** (cabruca region, Coopercabruca cooperative) — NOT Pará. São Jorge is the source farm for shipment **AGL6**.
- Extent: lat −14.6544…−14.6288, lon −39.4029…−39.3921 → convex hull ~64.7 ha, centroid −14.6361, −39.3992.
- Extract at `/home/ubuntu/sao_jorge_work/extracted/`; metadata at `/tmp/sao_jorge_rows.json`; analysis complete.

## Targets & state (verified 2026-09-02)
| Target | Repo | State |
|---|---|---|
| `farms/fazenda-sao-jorge-bahia/` | agroverse_shop_beta | index.html + media.json (schemaVersion 1: 2 YT videos sLNS9pZUBVw/33nwH67UIag + 2 images). Leaflet map pin at −14.6289989,−39.4028297. No SunMint cross-link yet. |
| `sunmint.html` | truesight_me_beta | Impact map loads `sunmint/plots/index.geojson`; popup shows "View farm profile on Agroverse ↗" when feature has farm_id (`FARM_SLUG` map: santa-anna-fazenda, rancho-maranta; fallback = raw farm_id). |
| `sunmint-tree-planting-pledges/agl6/` | truesight_me_beta | AGL6 pledge page exists (São Jorge is AGL6's source farm). |
| `sunmint/plots/index.geojson` | sunmint (api-only) | 5 real plots (RM-P1/P2, SA-P1, CL-P1, LD-P1) + test rows. No SJ plot. Machine-regenerated daily from SunMint Plots sheet → **sheet row is the durable write**. |
| `SunMint Plots` tab | sheet 1qbZZhf-… | Headers: Plot ID/Farm ID/Plot Name/Hectares/Status/Boundary Authority/Owner/Region/Verified At/Media/Notes/Coordinates/Lat/Long/… Write OK via agroverse_qr_code_manager SA. |
| `farm_media_manifests` | farm_media_manifests | oscar-bahia.json already extended schema to **v2** (creation_date, transcription_status, transcription present). Add fazenda-sao-jorge-bahia.json + index entry — **no schema change needed**. |
| `farm-media-raw/` | farm-media-raw | cleide, la-do-sitio, rancho-maranta, santa-anna — no sao-jorge yet. |
| `~/media_archive_inbox/farm-media/` | box | cleide, jedielcio, paulo-la-do-sitio, santa-anna — add fazenda-sao-jorge-bahia/ |

## Execution order (ONE PR PER TURN)
- **PR1** (this plan, agentic_ai_context + handoff row) → **PR2** farm_media_manifests: `fazenda-sao-jorge-bahia.json` manifest (v2 schema, 103 items, transcription_status=pending) + index.json entry → **PR3** SunMint Plots sheet row SJ-P1 + regenerate `plots/index.geojson` + `farms/index.json` (sunmint, Contents-API) → **PR4** agroverse_shop_beta: media.json gallery additions (3 web JPEGs: sao-jorge-img_1616/1671/8532 from visits) + SunMint impact-map cross-link → **PR5** truesight_me_beta: AGL6 pledge page ↔ farm page + sunmint.html farm_id wiring → **PR6** photos → farm-media-raw + inbox sidecars + MOV→MP4 transcode → daemon upload (long pole, ~6/day quota) → **UAT gate** (Gary reviews beta, then prod sync on explicit GO).

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

Farm_id == agroverse slug → popup farm link works without FARM_SLUG edit (fallback uses farm_id as-is).

## Gates
- NEVER deploy prod without Gary GO. Beta preview first (beta.agroverse.shop, beta.truesight.me).
- sunmint repo is api-only → upload_file_to_github, never branch-edit. farm-media-raw also api-only.
- SunMint Plots sheet is the durable plot source (daily rebuild) — geojson direct edit alone gets overwritten.
- YouTube quota ~6/day unverified → pace expectations; do NOT hammer.

## RESUME HERE
PR2: farm_media_manifests — commit `fazenda-sao-jorge-bahia.json` (v2, 103 items) + index.json entry (git_push_changes, deliberate commit). Then PR3 sheet row + geojson, PR4 farm page, PR5 sunmint cross-links, PR6 raw photos + inbox + transcode/daemon. UAT gate before any prod sync.
