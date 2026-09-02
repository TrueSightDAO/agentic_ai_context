# Oscar Bahia Media Task — execution plan (thread 19891)

**Created:** 2026-09-02 (Sophia) at Gary's request · **Handoff:** 👍 GO on resume-awaiting (thread 19891)
**Status:** executing

## Goal
1. Establish/polish the plot page for https://agroverse.shop/farms/oscar-bahia/index.html — hero, story, media gallery from the new zip.
2. SunMint presence on truesight.me/sunmint.html — cross-link BOTH ways (farm page ↔ sunmint/AGL14 pages).
3. See if anything interesting — add to the media gallery for Oscar's page.
4. Add Oscar's media to the media archive pipeline (farm-media inbox) with manifest updated for future reference: latitude/longitude, creation date, and transcription info.

## Source media
- `~/oscar.zip` (1.4 GB) = **45 MOV + 5 HEIC**, all shot **2025-09-20** at Oscar Fazenda, Bahia (~14°02–03'S, 39°26'W, Uruçuca region). GPS on all 45 MOVs + all 5 HEICs. Extract at `/tmp/oscar_extract/`. (iPhone .MOV = HEVC; .HEIC stills.)

## Targets & state (verified 2026-09-02)
| Target | Repo | State |
|---|---|---|
| `farms/oscar-bahia/` | agroverse_shop_beta | index.html + media.json with 2 YT videos (`lh_dAXhE7xQ`, `BI55aQ6B73U`). No SunMint cross-link. Map pin -14.052624,-39.438206. |
| `sunmint.html` | truesight_me_beta | Loads `sunmint/plots/index.geojson`; AGL14 shipment block exists (Oscar Fazenda). |
| `sunmint-tree-planting-pledges/agl14/` | truesight_me_beta | Pledge page exists; links to agroverse.shop/agl14 but NOT to the farm page. |
| `sunmint/plots/index.geojson` | sunmint | NO Oscar/OB plot yet — 9 features (RM-P1/P2, SA-P1, CL-P1, LD-P1…). |
| `farm_media_manifests` | farm_media_manifests | 4 farm manifests; schema has lat/lon but NOT creation_date/transcription → EXTEND schema. |
| `farm-media-raw/` | farm-media-raw | cleide, la-do-sitio, rancho-maranta, santa-anna — no oscar. |

## Execution order (ONE PR PER TURN)
- **PR1** (this plan, agentic_ai_context) → **PR2** farm_media_manifests: schema v2 (add `creation_date`, `transcription`, keep lat/lon) + `oscar-bahia.json` manifest + index.json entry → **PR3** agroverse_shop_beta: farm page gallery + hero + SunMint cross-link → **PR4** truesight_me_beta: AGL14 pledge page ↔ farm page cross-link + sunmint.html touch → **PR5** sunmint: OB plot proposal → **UAT gate** (Gary reviews beta, then prod sync on explicit GO).

## Media pipeline (long pole — start first)
1. MOV→MP4 (H.264) transcode ~45 files (15 min total video ≈ 30–45 min CPU on t3.medium).
2. Stills: convert the 5 HEICs → JPEG; frame-extract a few key scenes from MOVs for the gallery.
3. Build sidecars per farm-media-daemon schema: farm_id=oscar-bahia, sha256, gps, duration_s, creation_date, title/description (faster-whisper transcription → polish).
4. Place in `/home/ubuntu/media_archive_inbox/farm-media/oscar-bahia/` → daemon uploads at ~6/day budget (≈7–8 days for 45 vids).
5. Manifest commit after first yt_ids land (repo farm_media_manifests).
6. photos → `farm-media-raw/oscar-bahia/` (GitHub) for durable photo storage.

## Gates
- NEVER deploy prod without Gary GO. Beta preview first (beta.agroverse.shop, beta.truesight.me).
- Schema extension must stay backward-compatible with existing 4 manifests (bump schemaVersion, don't rewrite old ones).
- Daemon sidecar writes only; GitHub commit is deliberate (manifest-commit CLI).
- YouTube quota ~6/day unverified → pace expectations; do NOT hammer.

## RESUME HERE
Next turn: PR2 (farm_media_manifests schema v2 + oscar-bahia.json manifest skeleton) and stage media inbox (transcode + sidecars). Then PR3 farm page, PR4 sunmint cross-links, PR5 OB plot. UAT gate before any prod sync.
