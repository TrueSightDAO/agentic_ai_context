# Sítio Torres (Pacajá, loc3) Media Task Plan — execution

> Instantiated from `handoffs/FARM_MEDIA_TASK_PLAN_TEMPLATE.md` per the
> `AGROVERSE_SUNMINT_FARM_LISTING.md` end-to-end SOP. Same pattern as loc1
> (`handoffs/CACAU_NA_VEIA_MEDIA_TASK_PLAN.md`). This is the **loc3 "Sítio 2"** visit (2026-09-09).

**Created:** 2026-09-10 (Sophia) at Gary's/envoy's request · **Handoff:** 👍 GO (thread 24442)
**Status:** executing — **PR1–PR5 done, PR6 in progress**; UAT gate after PR6

## Goal
1. Confirm the plot behind https://agroverse.shop/farms/sitio-torres-pacaja-para/ is durably
   registered on truesight.me's SunMint impact map, cross-linked BOTH ways.
2. Add the 2026-09-09 site-visit media (38 HEIC + 35 MOV + 8 PNG) to the farm's page gallery.
3. Archive the media through **MAP** with the manifest updated (lat/lon, creation_date,
   transcription).

## 0. STEP ZERO — identity, attribution & naming gate

1. **Farm identity (governor-confirmed, thread 24442):** **Sítio Torres** — recorded as
   *"Sítio 2"* (a **propriedade/plot**, not its own separately-named farm). Wi-Fi SSID on site
   = `SITIO TORRES`. Region **Pacajá, Pará**. **4.5 ha** (claimed). Cacao **TRUE/hybrid**
   ("verdadeiro, híbrido") + a small clonal block; plot ages 2/4/5 yr plus a **>20 yr** block;
   shade tree = **cumaru** (native Amazon). Sampled **~120 kg**; target first lot **600 kg**.
2. **Owner/producer:** **Alexandre** — a **CoopCao director-coordinator** (coop has 8 registered
   properties). People named in media are DATA, never ownership proof.
3. **Registry overlap FIRST — ✅ NO trap, but ALREADY REGISTERED.** Searched
   `sunmint/plots/index.geojson` for the loc3 bbox `(-3.54020, -3.52880, -51.14554, -51.14330)`:
   **exactly 1 overlapping feature** — `plot_id: N-06-66`, `farm_id: sitio-torres-pacaja-para`,
   `name: "Sítio Torres (Pacajá) Plot 1 (cacao enrichment)"`, bbox **identical** to the walk bbox.
   Nearest-other centroid ~111 m away. → **PR3 is verify-only**; do **not** add a second plot.
4. **Duplicates — ✅ CLEAN.** 0 intra-set duplicate HEIC hashes; 0 identical hashes vs loc1
   (`cacau-na-veia-pacaje`); 0 filename collisions. All 81 loc3 files are distinct from loc1.
5. **✅ Site code `N-06-66` — RESOLVED 2026-09-10.** Governor (Gary, thread 24442) **confirmed
   `N-06-66` is the correct issued CEPOTX site code**. The plot row (sheet `SunMint Plots` row 23)
   is authoritative: `N-06-66` / `sitio-torres-pacaja-para` / *Sítio Torres (Pacajá) Plot 1 (cacao
   enrichment)* / **19.01 ha** / `proposed` / `approx` / owner **Alexandre (CoopCao / CEPOTX)**.
   The concern that it sat outside the observed `N-06-02..N-06-52` roster no longer blocks — the
   governor's confirmation supersedes the roster-range inference. Manifest `site_code_status`
   updated to **VERIFIED** (`93e69e26`). No `[PLOT INVALIDATION EVENT]` needed.
6. **✅ Provenance — RESOLVED 2026-09-10 (was flagged as a gate; it was a plan-authored error).**
   The loc3 source zip **does exist on the box**:
   `/home/ubuntu/20260909_pacaje_location_3_farm_alessandro_director_coopcao.zip` (2.15 GB,
   `IMG_9622–IMG_9705`). Its 81 members (38 HEIC / 35 MOV / 8 PNG) are an **exact set match** to
   `/media/pacaje_work/loc3/` (`comm` diff **empty both ways**); zip mtime 01:54, dir created 01:55
   → extracted straight from it. The zip name resolves the owner: **Alexandre, CoopCao director**.
   The three Pacajá zips are **disjoint contiguous phone-roll ranges** — loc1 `IMG_9493–9557` (63),
   loc2-nursery `IMG_9562–9620` (59), loc3 `IMG_9622–9705` (81). The earlier assertion that
   `..._location_2_nursery.zip` was loc3's source was simply **wrong**; the manifest
   `source_zips`/`source_zip_note` has been corrected (commit `b792eb0d`).
7. **Claimed vs walked extent (flag):** claimed **4.5 ha**; walk hull **19.14 ha** (walk covered
   nursery + mature blocks, not just the plotted area). Boundary authority stays **approx** —
   needs CAR/INCRA or a boundary walk.

## Progress log (newest last)
- 2026-09-10 · **PR1** ✅ plan landed (`agentic_ai_context` #999)
- 2026-09-10 · **PR2** ✅ manifest + index committed to `farm_media_manifests@main` (`6fa21fff`, `80b0711d`); provenance corrected (`b792eb0d`)
- 2026-09-10 · **PR3 / PR4 / PR5** ✅ verified — all **NO-OP** (sheet row present; beta page + 12 assets live; farm in sunmint farms index)
- **NEXT → PR6** (build: HEIC → farm-media-raw, MOV → MP4 + GPS re-inject, commit transcripts, inbox sidecars w/ explicit `extensions`, daemon upload) → **UAT gate**
- 2026-09-10 · **both gates RESOLVED** — (a) `N-06-66` governor-verified; (b) provenance = `..._location_3_farm_alessandro_director_coopcao.zip` (exact set-match). Manifest `site_code_status` → VERIFIED (`93e69e26`)
- 2026-09-10 · **PR6 STARTED** — MOV→MP4 transcode + GPS re-inject running in background (`/media/pacaje_work/loc3_pr6/`); photos + sidecars + transcripts next

## Source media
- Dir on box: `/media/pacaje_work/loc3/` (`IMG_9622–IMG_9705`).
- **38 HEIC + 35 MOV + 8 PNG = 81 files**, **2.1 GB**.
- **73 EXIF-bearing (HEIC+MOV); 72 geotagged (98.6%)**, 0 duplicates, **59 unique points**.
  (The single ungeotagged file is `IMG_9632.HEIC`.)
- Visit: **2026-09-09** only (12:33 → 16:40 local).
- Location: **Pacajá, Pará** (CoopCao / CEPOTX) — **not** Altamira/Uruará.
- Extent: lat `-3.54020 … -3.52880`, lon `-51.14554 … -51.14330` → convex hull **~19.14 ha**
  (10 vertices), centroid **-3.53487, -51.14476**.
- **8 PNGs are screenshots, not photos** (`IMG_9631/9637/9681/9690/9691/9694/9695/9698`) —
  `IMG_9694` is the site-code translator shot. Archive as *screenshots*, keep them **out** of the
  photo gallery.
- **Transcripts: DONE.** `/media/pacaje_work/loc3_tx/MAP/` = **35 `.json` + 35 `.vtt`**
  (faster-whisper `small`, pt; MAP §6b) — one pair per MOV. **26 carry text; 9 are silent**
  (`IMG_9627/9628/9643/9644/9646/9665/9675/9679/9699`). Audio at `loc3_tx/audio/` (35 `.wav`);
  index `loc3_tx/transcripts.json`.

## Targets & state (verified 2026-09-10)
| Target | Repo | State |
|---|---|---|
| `farms/sitio-torres-pacaja-para/` | agroverse_shop_beta | **EXISTS + live** (beta & prod). `index.html` + `media.json` (schemaVersion 1: hero + **12** gallery entries; loads via `js/media-gallery.js`) |
| `sunmint/plots/index.geojson` | sunmint (api-only) | **`N-06-66` ALREADY PRESENT** (22 features), bbox = walk bbox → PR3 verify-only |
| `SunMint Plots` tab | sheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` | **✅ VERIFIED (PR3)** — row 23 = `N-06-66` / `sitio-torres-pacaja-para`; `sunmint/farms/index.json` also carries the farm (plot_count 1, 19.01 ha). No drift → geojson NO-OP |
| `farm_media_manifests/sitio-torres-pacaja-para.json` | farm_media_manifests | **✅ CREATED (PR2)** — 81 items, root-level `<farm_id>.json` + `index.json` entry (12→13) |
| `farm-media-raw/sitio-torres-pacaja-para/photos/` | farm-media-raw (api-only) | **MISSING** (10 peer dirs, not this one) → **PR6 (in progress)** |
| `/media/media_archive_inbox/farm-media/sitio-torres-pacaja-para/` | box | **no dir, no daemon config entry** → **PR6** |
| `raw/sitio-torres-*/` in `media.agroverse.shop` | S3 | **absent** → PR6 (daemon upload leg) |
| FSVP / entity | fda_fsvp | already covered by CEPOTX `N-06-66` anchor; no new entity |

## Execution order (ONE PR PER TURN)
- **PR1** this plan (agentic_ai_context) ✅
- **PR2** ✅ farm_media_manifests: `sitio-torres-pacaja-para.json` + `index.json` entry — committed at
  the **real peer schema** (`cacau-na-veia-pacaje.json` carries NO sha256/objects[]/yt_id), plus a
  `role` field (photo/video/screenshot) to keep the 8 PNG screenshots out of the public gallery
- **PR3** ✅ SunMint Plots sheet row verified (`N-06-66` @ row 23) — geojson **NO-OP confirmed**
- **PR4** ✅ agroverse_shop_beta — **NO-OP confirmed**: page + 12-entry `media.json` gallery live, all 12 image assets HTTP 200
- **PR5** ✅ truesight_me_beta wiring — **NO-OP confirmed**: `farm_id` == slug; farm present in `sunmint/farms/index.json`
- **PR6** photos (38 HEIC → web JPEGs + full-res originals →
  `farm-media-raw/sitio-torres-pacaja-para/photos/`, Contents-API only) + MOV→MP4 transcode
  (ffmpeg, GPS re-inject via exiftool — **VERIFY `Keys:GPSCoordinates` after**) + inbox sidecars
  (daemon schema + `creation_date` + `transcription`) + **commit the 35 existing transcripts**
  → daemon upload (~6/day quota) → yt_ids backfilled
- **UAT gate** → governor reviews beta → prod sync ONLY on explicit GO

## Plot feature (`N-06-66`) — already registered, verify only
Registered in `sunmint/plots/index.geojson` with bbox `(-3.5402, -3.5288, -51.145542, -51.1433)`
= **exactly** the 72-point walk hull → no new plot, no edit expected.

Walk ring (lng,lat, convex hull of 59 unique points — audit trail):
`[[-51.145400,-3.540200],[-51.145447,-3.540161],[-51.145542,-3.539478],[-51.145400,-3.529300],[-51.145036,-3.528822],[-51.145000,-3.528800],[-51.143300,-3.536700],[-51.144200,-3.539300],[-51.144300,-3.539400],[-51.145100,-3.540100]]`

## Media pipeline notes
1. Photos (38 HEIC) → web JPEGs for gallery + full-res originals →
   `farm-media-raw/sitio-torres-pacaja-para/photos/` (Contents-API only).
2. Videos (35 MOV) → MOV→MP4 transcode (ffmpeg, GPS re-inject via exiftool — VERIFY
   `Keys:GPSCoordinates` after) → transcription **already DONE** (commit the 35 existing pairs) →
   inbox sidecars (daemon schema + `creation_date` + `transcription`) → daemon uploads ~6/day →
   yt_ids backfilled.
3. Manifest commit (PR2) v2 schema: sha256/GPS/duration/objects[]/creation_date/transcription/
   transcription_status/yt_id.
4. **Config trap (thread 24440):** set `extensions` **explicitly** in the archive-root / inbox
   config entry — a root **without** an `extensions` key silently defaults to MOV-only. Keep **PNG
   screenshots out of S3/photo dirs** unless deliberately archived.
5. ZIP-HANDLING: one object per original file, skip `__MACOSX/` + `._`; never archive the zip blob.

## Gates
- NEVER deploy prod without governor GO. Beta preview first (beta.agroverse.shop).
- `sunmint` + `farm-media-raw` are api-only → `upload_file_to_github`, never branch-edit.
  `farm_media_manifests` via `git_push_changes`.
- SunMint Plots sheet is the durable plot source (daily rebuild) — a geojson-only edit gets
  overwritten.
- YouTube shared quota ~6/day — pace, retry on 429, live-sweep yt_ids.
- Two-way link: farm page → map must be a real
  `<a href="https://truesight.me/sunmint.html?plot=N-06-66">`; map → farm page needs no FARM_SLUG
  edit while `farm_id` == page slug.
- **Site-code gate:** resolve the `N-06-66` registry question (§0.5) before treating the code as
  published truth.
- **Provenance gate:** resolve the loc3-vs-zip mismatch (§0.6) before archiving media.
- No TDG/money movement anywhere in this plan. Standard AI-agent `[CONTRIBUTION EVENT]` time
  reporting after merged PRs (§6, `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`) — routine, not a gate.

## RESUME HERE
PR1 done (this plan + manifest row). **Next = PR2**: commit
`farm_media_manifests/sitio-torres-pacaja-para.json` (v2) + `index.json` entry.
Then PR3 (verify `N-06-66` sheet row) → PR6 (HEIC → farm-media-raw, MOV→MP4 + GPS re-inject,
commit the 35 existing transcripts, inbox sidecars, daemon upload) → UAT gate before any prod sync.
Open questions for the governor: (a) confirm `N-06-66` is the issued CEPOTX code; (b) confirm
loc3's true source (the `..._location_2_nursery.zip` is disjoint from the loc3 files).
