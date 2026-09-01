# MEDIA_ARCHIVE_PIPELINE.md — Raw media intake, dedupe & distribution (Media Archives Pipeline / MAP)

> **Renamed from `FARM_MEDIA_PIPELINE.md`** (2026-09-01) to match MAP terminology. Older docs/links may still say FARM_MEDIA_PIPELINE.md — same file.

## Terminology — Media Archives Pipeline (MAP)

> **Media Archives Pipeline (MAP)** is the umbrella term for this whole system — the
> capture → process → archive → manifest → query flow for **any** DAO media (farm visits,
> community events, partner trips…). Farm media is the **first source namespace** under it.
>
> - **MAP** — the umbrella: intake → processing → upload/archive → manifest → query
> - **Source namespace** — which bucket the media came from: `farm-media` (this runbook, formerly FARM_MEDIA_PIPELINE.md),
>   `event-media` (community events, future)…
> - **The queue** — the inbox + sidecars (what's waiting; pending = no `yt_id`)
> - **The daemon** — the shared uploader (`farm-media-daemon` repo), dumb-on-purpose
> - **The manifests** — `farm_media_manifests/` (repo TrueSightDAO/farm_media_manifests), the committed, queryable source of truth
> - **Distribution ≠ archive** — Instagram/TikTok/shop-page posting are consumers of the
>   archive, not the pipeline itself
>
> Legacy filenames keep the `farm-media` prefix (this file, the repo, the manifests dir)
> as the first namespace; new sources add their own namespace (e.g. `EVENT_MEDIA_MANIFESTS/`).

Standardized pipeline for ingesting raw farm media (HEIC photos + MOV videos zips) from TrueSightDAO partner farms: GPS extraction, plot registration, SHA-256 dedupe, object detection, MOV→MP4 (GPS-preserving), **public** YouTube upload, photo storage in `farm-media-raw` (Contents-API only), farm-page wiring, and a searchable manifest index.

Written so **any Sophia instance** can process a farm end-to-end or pick up a farm handed off by a governor. Governors: hand off a zip + this file's checklist; the receiving instance follows this doc.

## Where things land (end state)

| Artifact | Destination | Notes |
|---|---|---|
| Videos (MP4) | **YouTube public** (admin@truesight.me channel) | free, unlimited, durable; embed via media-gallery.js `youtube` entries |
| Photos (HEIC/JPG originals) | GitHub repo **`farm-media-raw`**, `<farm-id>/photos/` | individual files, **Content-API only** (repo can get large; never clone/branch-edit) |
| Manifest / index | `farm_media_manifests/<farm-id>.json` (repo TrueSightDAO/farm_media_manifests) | the reference layer: sha256, GPS, duration, objects[], yt_id — keyword-searchable via GitHub code search |
| Farm page gallery | `agroverse_shop_beta/farms/<farm-id>/media.json` | curated youtube + image entries |
| Plot polygon | `sunmint/plots/index.geojson` (+ `SunMint Plots` sheet tab) | only if new farm plot |

## Farm IDs (keyed everywhere by these slugs)

| Farm | farm_id slug | SunMint plot | media repo subfolder |
|---|---|---|---|
| La do Sitio (Paulo) | `paulo-la-do-sitio-para` | LD-P1 | `la-do-sitio/` |
| Santa Anna Fazenda | `santa-anna-fazenda-para` | SA-P1 | `santa-anna-fazenda-para/` |
| Rancho Maranta | `rancho-maranta-para` | RM-P1 / RM-P2 | `rancho-maranta/` |
| Cleide | `cleide` | CL-P1 | `cleide/` |

## Pipeline (per farm)

### 1. Intake
- Unzip to `/home/ubuntu/<farm>_work/` (La do Sitio pattern: `/home/ubuntu/la_do_sitio_work/la do sitio/`).
- Count: `ls *.HEIC | wc -l; ls *.MOV | wc -l` (La do Sitio: 52 HEIC + 72 MOV).

### 2. GPS sweep
- `exiftool -s -s -GPSCoordinates -GPSLatitude -GPSLongitude <file>` on every file.
- MOV stores GPS under QuickTime key **`GPSCoordinates`** as `3°23'10.68"S, 51°51'5.04"W, 134.4m` — parse DMS; **S/W = negative**.
- Coverage ~115/124; interior shots often lack GPS.
- **New farm?** convex-hull the unique points → plot polygon → add row to `SunMint Plots` sheet tab (plot_id, farm_id, status `proposed`/`planted`, `boundary_authority: approx`, media, notes) → run `build_plots_geojson.py` (needs `sunmint_work` checkout + `agroverse_qr_code_manager` SA key at `/opt/truesight_autopilot/config/google/`) → push `plots/index.geojson` via `upload_file_to_github` (sunmint is api-only).

### 3. SHA-256 dedupe (mandatory)
- `sha256sum` every media object. **Same sha = already uploaded = skip** — the anti-duplicate gate for both YouTube and the repo.

### 4. Manifest build
- JSON per video: `file, size_bytes, sha256, duration_s, latitude, longitude, objects[]`.
- Pilot (La do Sitio, 72 videos): `/tmp/la_do_manifest_full.json`.

### 5. Object detection (local, governor-approved if accurate)
- **Ultralytics YOLOv8n** (CPU). 3 frames/video (10/50/90%).
- COCO-80 lacks cacao → remap `banana` → **`cacao_pods`** (header note; raw label kept in `raw_objects`).
- Install: `/opt/truesight_autopilot/.venv/bin/pip install ultralytics` (pulls torch-cpu).

### 6. MOV→MP4 (**CRITICAL: GPS**)
```bash
ffmpeg -y -v error -i in.MOV -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k -movflags +faststart out.mp4
exiftool -overwrite_original -api QuickTimeUTC=1 "-GPSCoordinates=<from source>" out.mp4
exiftool -s -s -GPSCoordinates out.mp4   # VERIFY before upload
```
- **ffmpeg DROPS Apple QuickTime GPS.** `-map_metadata 0` does NOT carry it. Always re-inject via exiftool, then verify.
- Batch: `nohup` loop with progress file (`/tmp/mp4_progress.txt`), ~35–60 s/video on t3.medium.

### 7. YouTube upload (public)
- `/opt/truesight_autopilot/config/youtube/upload_video_to_youtube.py --file --title --description --tags --privacy public`
- **SHARED QUOTA**: all instances share ONE Google project (`project_number:323153649224`). 'Video Uploads per day' is a hard daily cap (~50-60/day). Batch uploads WILL hit 429 mid-run. **Always** run uploads behind a retry loop: on 429, wait 30 min and retry (quota resets ~midnight PT); skip entries that already have a LIVE yt_id. Never re-upload blindly.
- **VERIFY LIVE, not just captured**: after upload, the returned ID must be confirmed with `videos().list(part='id')`. A title->ID recovery map against the shared channel's uploads playlist (which can contain deleted/lingering entries) WILL capture stale IDs. Live-sweep every manifest ID before trusting it; dead ID = re-upload.
- **Corrupt source**: if ffmpeg fails with 'moov atom not found' on the ORIGINAL MOV (zip corruption), mark `error: SOURCE_CORRUPT` in the manifest — do not loop retries.
- Token: `config/youtube/youtube_token.json` (admin@truesight.me channel); refresh if expired.
- Title pattern: `"<Farm name> — <basename> (cacao pods, <lat>, <lng>)"`. Description: GPS, objects, date, farm link.
- Write returned `videoId` back into manifest as `yt_id`.

### 8. Photos → farm-media-raw
- `upload_file_to_github(repo='farm-media-raw', path='<farm-id>/photos/<basename>', content_base64=...)` — one call per file (Content API, 25 MB cap; HEICs fine).
- **Never** `git_push_changes` to `farm-media-raw` (api-only repo).

### 9. Farm page wiring (beta-first)
- `agroverse_shop_beta/farms/<farm-id>/media.json`: gallery entries `{type: youtube, id: yt_id}` + `{type: image, src: /assets/images/farms/IMG_x.jpg}`.
- Upload web-optimized JPEGs to `agroverse_shop_beta/assets/images/farms/` (**repo-root** path — site serves from root; og:image + rancho-maranta precedent).
- `index.html` Farm Location: Leaflet pin → GPS centroid, add `L.polygon` overlay (plot ring), add SunMint impact-map link.
- PR → merge → beta verify → `sync_beta_to_prod` **only on explicit governor go**.

### 10. Manifest PR to agentic_ai_context
- `farm_media_manifests/<farm-id>.json` (+ update index). `git_push_changes` on the data repo (TrueSightDAO/farm_media_manifests).

## Handoff checklist (governor → another Sophia instance)
Include in the handoff message:
- [ ] zip path on box (`/home/ubuntu/<farm>.zip`) or new upload
- [ ] farm_id slug + SunMint plot id (or "new plot needed")
- [ ] privacy (Gary default: **public**)
- [ ] plot status decision (proposed vs planted)
- [ ] region/municipality if known
- [ ] READ THIS FILE first (MEDIA_ARCHIVE_PIPELINE.md)

## Anti-patterns / lessons learned
- ❌ Plain ffmpeg convert → **GPS lost** (pilot video `jM4Y6Wq5fMc` went up without GPS before catch).
- ❌ Raw MOV/HEIC in git repos (2 files > 100 MB hard cap; repo bloat).
- ❌ `-map_metadata 0` does NOT carry QuickTime GPS.
- ❌ Duplicate uploads (sha-dedupe before EVERY upload).
- ✅ exiftool inject `GPSCoordinates` AFTER convert; verify before upload.
- ✅ YouTube = videos, GitHub = photos; S3 not needed (governor choice).
