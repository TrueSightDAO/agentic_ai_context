# Sítio Torres (Pacajá, loc3) Media Task Plan — execution

> Instantiated from `handoffs/FARM_MEDIA_TASK_PLAN_TEMPLATE.md` per the
> `AGROVERSE_SUNMINT_FARM_LISTING.md` end-to-end SOP. Same pattern as loc1
> (`handoffs/CACAU_NA_VEIA_MEDIA_TASK_PLAN.md`). This is the **loc3 "Sítio 2"** visit (2026-09-09).

**Created:** 2026-09-10 (Sophia) at Gary's/envoy's request · **Handoff:** 👍 GO (thread 24442)
**Status:** executing — PR1 this plan; **PR2 + PR6 are the real remaining work**

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
5. **⚠️ Site code `N-06-66` — OUTSTANDING GATE.** Read as **N-06-66** from a phone-translator
   screenshot (`loc3/IMG_9694.PNG`: *"O código dele é N0666"*), but
   `CEPOTX_SITE_CODE_REGISTRY.md` lists the **COOPCAO** family beginning **N-06-02**, i.e.
   **N-06-66 sits outside the observed roster range**. The plot row *exists* in the registry;
   whether `N-06-66` is the **correct issued** code needs **CEPOTX registry confirmation**.
   If disconfirmed: `[PLOT INVALIDATION EVENT]` + re-register (not re-derive).
6. **⚠️ Provenance mismatch — OUTSTANDING GATE.** Work dir `/media/pacaje_work/loc3/` holds
   `IMG_9622–IMG_9705`. The zip `20260909_pacaje_location_2_nursery.zip` holds
   `IMG_9562–IMG_9620` — a **disjoint** set (59 files, 118 entries incl. `__MACOSX/`).
   **So that zip is NOT loc3's source.** Whether `loc3` ≡ "location 2", and where loc3's files
   actually came from, needs governor confirmation before archiving (wrong provenance = wrong
   media attached to a farm).
7. **Claimed vs walked extent (flag):** claimed **4.5 ha**; walk hull **19.14 ha** (walk covered
   nursery + mature blocks, not just the plotted area). Boundary authority stays **approx** —
   needs CAR/INCRA or a boundary walk.

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
| `SunMint Plots` tab | sheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` | **verify** the durable sheet row exists for `N-06-66` (daily geojson rebuild source) |
| `farm_media_manifests/sitio-torres-pacaja-para.json` | farm_media_manifests | **404 — MISSING** → **PR2** (peer layout: root-level `<farm_id>.json` + `index.json` entry) |
| `farm-media-raw/sitio-torres-pacaja-para/photos/` | farm-media-raw (api-only) | **MISSING** (10 peer dirs, not this one) → **PR6** |
| `/media/media_archive_inbox/farm-media/sitio-torres-pacaja-para/` | box | **no dir, no daemon config entry** → **PR6** |
| `raw/sitio-torres-*/` in `media.agroverse.shop` | S3 | **absent** → PR6 (daemon upload leg) |
| FSVP / entity | fda_fsvp | already covered by CEPOTX `N-06-66` anchor; no new entity |

## Execution order (ONE PR PER TURN)
- **PR1** this plan (agentic_ai_context) ✅
- **PR2** farm_media_manifests: `sitio-torres-pacaja-para.json` (v2 schema: sha256/GPS/duration/
  objects[]/creation_date/transcription{,_status}/yt_id) + `index.json` entry
- **PR3** SunMint Plots **sheet row** verify for `N-06-66` (+ regenerate `sunmint/plots/index.geojson`
  only if sheet drift implies it) — **expected NO-OP on the geojson**
- **PR4** agroverse_shop_beta — **expected NO-OP**: page + `media.json` gallery already live
- **PR5** truesight_me_beta wiring — **NO-OP expected**: `farm_id` == page slug
  (`sitio-torres-pacaja-para`)
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
