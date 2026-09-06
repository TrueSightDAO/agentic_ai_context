# Santa Ana (Bahia) Media + Plot Task — execution plan (thread 19965)

**Created:** 2026-09-02 (Sophia) at Gary's request · **Handoff:** 👍 GO on resume-awaiting (thread 19965)
**Status:** executing

## Goal
1. Establish/refresh the farm page for https://agroverse.shop/farms/fazenda-santa-ana-bahia/index.html — media gallery from the new zip + SunMint plot.
2. SunMint presence on truesight.me/sunmint.html — cross-link BOTH ways (farm page ↔ sunmint).
3. See if anything interesting — add to the media gallery for the farm's page.
4. Add the farm's media to the media archive pipeline (farm-media inbox) with manifest updated for future reference: latitude/longitude, creation date, and transcription info.

## Source media (verified)
- `~/santa_anna_farzenda_bahia.zip` (3.6 GB) = **151 MOV + 91 HEIC + 1 JPG**, all shot **2023-09-18** at Fazenda Santa Ana (Bahia) — Morbeck / Chocolate Morbeck / Coopercabruca estate, Uruçuca region (~14.3227°S, 39.10°W). GPS on all MOVs + HEICs (to be confirmed by sweep).
- Extracted at `/home/ubuntu/santa_ana_bahia_work/` (verified counts 151/91/1; source zip removed after extraction for disk).
- NOTE: distinct from Pará "Santa Anna Fazenda" (Ana Lucia, santa-anna-fazenda-para) — do not conflate.

## Targets & state (verified 2026-09-02)
| Target | Repo | State |
|---|---|---|
| `farms/fazenda-santa-ana-bahia/` | agroverse_shop_beta | index.html + media.json (schemaVersion 1, 3 YT videos, no image entries). No SunMint cross-link. Map pin -14.3225976, -39.1061207. |
| `sunmint.html` | truesight_me_beta | Loads `sunmint/plots/index.geojson`; farms registry section. |
| `sunmint/plots/index.geojson` | sunmint | 9 features — all Pará/test; NO Bahia plot (oscar-bahia OB-P1 also still missing). |
| `farm_media_manifests` | farm_media_manifests | v2 schema EXISTS (oscar-bahia.json: lat/lon + creation_date + transcription_status/transcription). 10 manifests incl. oscar-bahia. |
| `farm-media-raw/` | farm-media-raw | cleide, la-do-sitio, rancho-maranta, santa-anna-fazenda-para — no fazenda-santa-ana-bahia yet. |
| Media daemon | running (pid live) | inbox `/home/ubuntu/media_archive_inbox/farm-media/{cleide,fazenda-dona-rosa,fazenda-santa-rosa,jedielcio,paulo-la-do-sitio,raimundo-geniza-para,santa-anna-fazenda}`. |

## Execution order (ONE PR PER TURN)
- **PR1** (this plan, agentic_ai_context) → **PR2** farm_media_manifests: `fazenda-santa-ana-bahia.json` manifest (v2 schema) + index.json entry → **PR3** agroverse_shop_beta: farm page media gallery + SunMint cross-link + plot overlay → **PR4** truesight_me_beta: sunmint.html ↔ farm page cross-link (both ways) → **PR5** sunmint: FSA-P1 plot proposal in plots/index.geojson → **UAT gate** (Gary reviews beta, then prod sync on explicit GO).

## Media pipeline (long pole — started first)
1. ✅ Free disk (removed source zip; 91%→free). ✅ Kick background sweeps: exiftool GPS/date CSV, sha256, HEIC→JPG.
2. Compute GPS cluster → convex hull → **FSA-P1** polygon (status proposed, boundary_authority approx, mirror RM-P2 schema).
3. Photos (91 JPG) → `farm-media-raw/fazenda-santa-ana-bahia/photos/` (GitHub).
4. MOV→MP4 (H.264) transcode CURATED subset (~15–25 best) + full set if quota/disk allows; GPS re-inject via exiftool + verify.
5. Transcribe (faster-whisper) → polish → titles/descriptions.
6. Build sidecars per farm-media-daemon schema: farm_id=fazenda-santa-ana-bahia, sha256, gps, duration_s, creation_date, title/description, transcription.
7. Place in `/home/ubuntu/media_archive_inbox/farm-media/fazenda-santa-ana-bahia/` → daemon uploads at ~6/day budget (151 vids ≈ weeks — stage curated subset first for gallery).
8. Manifest commit after first yt_ids land (repo farm_media_manifests).

## Gates
- NEVER deploy prod without Gary GO. Beta preview first (beta.agroverse.shop, beta.truesight.me).
- v2 schema already exists (oscar-bahia) — reuse, don't extend further unless needed.
- Daemon sidecar writes only; GitHub commit is deliberate (manifest-commit CLI).
- YouTube quota ~6/day unverified → pace expectations; do NOT hammer.
- Disk is tight (91% after cleanup) — transcode in waves, delete mp4s post-upload.

## RESUME HERE
Next turn: PR2 (farm_media_manifests fazenda-santa-ana-bahia.json skeleton from sweep results) + stage media inbox (curated transcode + sidecars). Then PR3 farm page, PR4 sunmint cross-links, PR5 FSA-P1 plot. UAT gate before any prod sync.
