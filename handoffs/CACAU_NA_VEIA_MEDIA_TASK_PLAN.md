# Sítio Cacau na Veia (Pacajá) Media Task Plan — execution

> Instantiated from `handoffs/FARM_MEDIA_TASK_PLAN_TEMPLATE.md` per the
> `AGROVERSE_SUNMINT_FARM_LISTING.md` end-to-end SOP. This is the **mature-plot**
> half of a two-plot property; the **restoration** plot is a separate, later handoff.

**Created:** 2026-09-10 (Sophia) at Gary's request · **Handoff:** 👍 GO on resume-awaiting (thread 24441)
**Status:** executing — PR1–PR4 done (PR4 = farm page live on beta `beta.agroverse.shop/farms/cacau-na-veia-pacaje/`, PR #310 merged `4662efc8`); **PR5 verified NO-OP** (`farm_id` == page slug)

## Goal
1. Establish plot **N-06-37** (mature cacao agroforest) on https://agroverse.shop/farms/cacau-na-veia-pacaje/ and on truesight.me's SunMint impact map — cross-link BOTH ways.
2. Add the 2026-09-09 site-visit media (33 MOV + 30 HEIC) to the farm's page gallery.
3. Archive the media through MAP with manifest updated (lat/lon, creation_date, transcription).

## 0. STEP ZERO — identity, attribution & naming gate ✅ (governor-confirmed, thread 24441)
1. **People from media:** site visit guided by a female narrator = **Jader Adriano da Silva Santos's wife** (owner/co-owner). **Jader was NOT present** (traveling, IMG_9547) — the on-camera assertions of ownership are the guide's, not the owner's; recorded as DATA.
2. **Registry overlap FIRST:** checked all 18 features in `sunmint/plots/index.geojson` — **NO overlap** with the loc1 bbox `[-51.03630,-3.60980,-51.03240,-3.60850]`. Nearest = CR-PA-P2 (-51.104,-3.558), a different site. Not the Bom Sucesso trap.
3. **Name + owner ↔ plot confirmed by governor:** farm name **Sítio Cacau na Veia** (spoken 3× on camera); owner **Jader Adriano da Silva Santos (CEPOTX President) & wife**; coop **COOPCAO**.
4. **Existing site code looked up first** (`fda_fsvp/suppliers/cepotx/site_codes.md` + `CEPOTX_SITE_CODE_REGISTRY.md`): **N-06-37 = Jader Adriano da Silva Santos — CEPOTX President, COOPCAO** (roster + public record). Video speaks the code (**"Código… 37"**, IMG_9493). Site code **already issued — NOT re-derived**.
5. Coop claim (COOPCAO) matches the N-06 family in the CEPOTX rosters.

## Source media
- Zip on box: `/media/pacaje_work/loc1/` (unzipped from `20260909_pacaje_location_1_farm_cepotx_president_farm.zip`).
- **33 MOV + 30 HEIC = 63 files**, **61 files with GPS (97%)**, 0 duplicates, **54 unique geotagged points**.
- Visit: **2026-09-09** (13:35–14:26 UTC).
- Location: **Pacajá, Pará** (COOPCAO / CEPOTX) — **not** Altamira/Uruará.
- Extent: lat `-3.60980…-3.60850`, lon `-51.03630…-51.03240` → convex hull **~3.02 ha** (8 vertices, visited corner only), centroid **-3.609276, -51.034411**.
- Transcripts: `/media/pacaje_work/loc1_tx/MAP/*.json` (faster-whisper `small`, pt; MAP §6b).

## Targets & state (verified 2026-09-10)
| Target | Repo | State |
|---|---|---|
| `farms/cacau-na-veia-pacaje/` | agroverse_shop_beta | **does not exist yet** — to create |
| `sunmint.html` | truesight_me_beta | data-driven; renders new plots automatically after push |
| `sunmint/plots/index.geojson` | sunmint (api-only) | **no N-06-37 plot** — add |
| `SunMint Plots` tab | sheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` | agentic_ai_context note says `1qbZZhf-…`; **full ID = `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`** (from SUNMINT_E2E_RUNBOOK.md). Write via `agroverse_qr_code_manager` SA |
| `farm_media_manifests/cacau-na-veia-pacaje.json` | farm_media_manifests | **does not exist** — add + index entry |
| `farm-media-raw/` | farm-media-raw (api-only) | `<farm_id>/photos/` — Contents-API only |
| `/media/media_archive_inbox/farm-media/` | box | `<farm_id>/` dir + daemon config entry |
| FSVP / entity | fda_fsvp | already covered by CEPOTX N-06-37 anchor; no new entity needed |

## Execution order (ONE PR PER TURN)
- **PR1** this plan (agentic_ai_context) ✅
- **PR2** farm_media_manifests: `cacau-na-veia-pacaje.json` (v2, creation_date + transcription_status=done) + `index.json` entry
- **PR3** SunMint Plots **sheet row** `N-06-37` + regenerate `sunmint/plots/index.geojson` (+ `farms/index.json` if present) — sheet row is the durable write
- **PR4** agroverse_shop_beta: `farms/cacau-na-veia-pacaje/` index.html + media.json (hero + gallery) + SunMint impact-map cross-link (BOTH directions)
- **PR5** truesight_me_beta wiring only if farm_id ≠ page slug; otherwise none
- **PR6** photos → farm-media-raw + inbox sidecars + MOV→MP4 transcode (GPS re-inject) + transcription → daemon upload (~6/day quota) → yt_ids backfilled
- **UAT gate** → governor reviews beta → prod sync ONLY on explicit GO.

## Plot features (TWO plots, for PR3)

Governor confirmed 2026-09-10 (thread 24441) there are **two plots**: the MATURE
plot (`N-06-37`) and a RESTORATION plot in front/behind it, named
**`N-06-37_20260909_restoration_1`** — following the established sub-plot suffix
convention `<sitecode>_<YYYYMMDD>_<purpose>_<seq>` (cf. live sheet rows
`B-06-108_20260908_research_1`, `B-06-108_20260908_1`,
`V-06-29-reforestation_20260907_plot_1`). Only the BASE code `N-06-37` is issued
by CEPOTX; suffixing it for a sub-plot does not invent a code.

```json
{"plot_id":"N-06-37","farm_id":"cacau-na-veia-pacaje","name":"Sítio Cacau na Veia Plot 1 (mature cacao agroforest)","hectares":30,"status":"proposed","plot_type":"mature","boundary_authority":"approx","owner":"Jader Adriano da Silva Santos (CEPOTX) & wife","region":"Pacajá, Pará","verified_at":"2026-09-09","notes":"Mature-plot segment of a 2026-09-09 walk: 47 geotagged files, hull 2.52 ha; lat -3.60980..-3.60850, lng -51.03630..-51.03240. 35+yr hybrid cacao agroforest (SAF). Claimed 30 ha (8 forest + 22 cacao, ~22k plants, IMG_9514/9546); hull < claimed -> needs CAR/INCRA or boundary walk."}
{"plot_id":"N-06-37_20260909_restoration_1","farm_id":"cacau-na-veia-pacaje","name":"Sítio Cacau na Veia Restoration Plot 1 (2026-09-09)","hectares":0.74,"status":"proposed","plot_type":"restoration","boundary_authority":"approx","owner":"Jader Adriano da Silva Santos (CEPOTX) & wife","region":"Pacajá, Pará","verified_at":"2026-09-09","notes":"Failed reforestation patch (IMG_9533: cacao+forest species planted, lost to drought, to be replanted). Hull 0.74 ha from the 15-photo restoration set (governor-supplied zip 20260909_president_restoration_plot.zip); lat -3.609697..-3.608539, lng -51.034236..-51.033394. Adjacent to (and hull-overlapping) the mature plot N-06-37 - same-day walk crossed both; needs walk/CAR to separate."}
```
GeoJSON rings (lng,lat, closed):
- N-06-37 (mature): `[[-51.0363,-3.6098],[-51.0363,-3.6097],[-51.034022,-3.608539],[-51.0324,-3.6085],[-51.032403,-3.608553],[-51.033864,-3.609617],[-51.0341,-3.6097],[-51.0359,-3.6098],[-51.0363,-3.6098]]`  (as published, blob `8d3434c3`)
- N-06-37_20260909_restoration_1: `[[-51.034236,-3.609258],[-51.034211,-3.609697],[-51.033864,-3.609617],[-51.033578,-3.609242],[-51.033394,-3.608928],[-51.034022,-3.608539],[-51.034169,-3.60875],[-51.034231,-3.609192],[-51.034236,-3.609258]]`

## Media pipeline notes
1. Photos (30 HEIC) → web JPEGs for gallery + full-res originals → `farm-media-raw/cacau-na-veia-pacaje/photos/` (Contents-API only).
2. Videos (33 MOV) → MOV→MP4 transcode (ffmpeg, GPS re-inject via exiftool — VERIFY `Keys:GPSCoordinates` after) → transcription DONE → inbox sidecars (daemon schema + creation_date + transcription) → daemon uploads ~6/day → yt_ids backfilled.
3. Manifest commit (PR2) v2 schema: sha256/GPS/duration/objects[]/creation_date/transcription/transcription_status/yt_id.
4. ZIP-HANDLING: one object per original file, skip `__MACOSX/` + `._`.

## Gates
- NEVER deploy prod without governor GO. Beta preview first (beta.agroverse.shop).
- `sunmint` + `farm-media-raw` are api-only → `upload_file_to_github`, never branch-edit.
- SunMint Plots sheet is the durable plot source (daily rebuild) — geojson direct edit alone gets overwritten.
- Two-way link: farm page → map must be a real `<a href="https://truesight.me/sunmint.html?plot=N-06-37">`; map → farm page needs no FARM_SLUG entry when plot `farm_id` == page slug.
- HECTARES: flagged — hull 3.02 ha vs claimed 30 ha. Registered as 30 (claimed) with `approx` authority + reconciliation note (RM-P2 precedent).

## RESUME HERE
PR1 ✅ this plan. PR2 ✅ manifest `cacau-na-veia-pacaje.json` (64 items: 49 mature + 15 restoration) + index entry.
**PR3 ✅ DONE 2026-09-10.** Sheet rows written to `SunMint Plots` (`N-06-37` mature 30 ha + `N-06-37_20260909_restoration_1` restoration 0.74 ha, farm `cacau-na-veia-pacaje`, no dups) → `plots/index.geojson` **22 features** (blob `8d3434c3`) + `farms/index.json` **15 farms** (blob `10ad6004`) published via Contents API, both ours present with closed 9-vertex rings.
**PR4 ✅ DONE 2026-09-10** (PR #310 merged `4662efc8`): shop page `farms/cacau-na-veia-pacaje/index.html` (27.8 KB) + `media.json` (hero `IMG_9499` + 12-image gallery) + 12 web JPEGs (5.9 MB) in `assets/images/farms/`; token-grep clean; live on beta (page 200, hero/gallery/media.json 200, both plot ids present, cross-link ×3).
**PR5 ✅ VERIFIED NO-OP 2026-09-10** — published `plots/index.geojson` carries `farm_id: "cacau-na-veia-pacaje"` == page slug, so `sunmint.html` line 862 (`FARM_SLUG[fid] || fid`) emits `agroverse.shop/farms/cacau-na-veia-pacaje/` with no `truesight_me_beta` edit. No PR needed.
Next: **PR6** raw photos + inbox sidecars + MOV→MP4 transcode + daemon upload. UAT gate before any prod sync.

> **Write-path (corrected 2026-09-10 — the previous 'READ-ONLY SAs' note was WRONG):**
the SunMint Plots sheet is the durable source of truth, and there ARE write-capable SAs
on this box — `agroverse_qr_code_manager` and `edgar_dapp_listener` both verified by live
no-op writes. The two halves of the FBE pipeline:
> 1. **Capture/audit** — `limites-da-fazenda` → `[FARM BOUNDARY EVIDENCE EVENT]` → Edgar → `process_farm_boundary_evidence.gs` (plot-first row + media mirror + tracking tab).
> 2. **Enrichment/geometry** — `sunmint/scripts/extract_plot_gps.py` (photo/video GPS → convex hull → `Coordinates`/Media/hectares/plot_type). Purpose-built for this; `--dry-run` first, then atomic `append_rows`/`batch_update` (its per-cell loop times out at 300 s).
> NOTE: the hourly FBE cron trigger is still unset (OPEN_FOLLOWUPS); a second writer touched the sheet concurrently this session (created `PL-005`) — always re-read before writing.


Status: restoration zip received (15 HEIC, 0 MOV, 14 dups of loc1, 1 new) — **no new transcription needed**. Governor confirmed plot naming.
