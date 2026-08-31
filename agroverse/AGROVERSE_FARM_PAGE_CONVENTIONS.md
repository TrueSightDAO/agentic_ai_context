# Agroverse Farm Page Conventions

**Read this** whenever building or updating a farm page on agroverse.shop (or beta.agroverse.shop), or when documenting a farm site visit for the web. Established from the Santa Anna Fazenda build (2026-08-31).

---

## 1. Hero image — humans over scenery

**The farm page hero should show PEOPLE — farmers at the farm — not just groves/scenery.**

- A wide, welcoming photo of the farmers (e.g. the farmer + cooperative contact, on the farm) is the preferred hero.
- A grove/pod/scenery shot is acceptable as a *fallback* or gallery item, but NOT the default hero.
- Why: visitors connect with faces; the current Santa Anna hero is the farmers-with-Jedielcio photo (teal-shirt farmer, woman in red, Jedielcio in cacao-print shirt) — see `assets/images/farms/santa_anna_farmers_hero.jpg`.
- When building a new farm page, check the site-visit media for a usable people photo FIRST. If none exists, ask the governor whether one can be supplied before defaulting to scenery.

## 2. Real GPS from EXIF — never guess coordinates

- Extract lat/lon from the **original media** (HEIC/IPhone photos carry EXIF GPS; phone .MOV files carry creation time but usually not location).
- **Telegram strips EXIF on upload** — attachments received via Telegram have zero GPS. Use scp'd originals (e.g. `~/santa_anna_fazenda.zip`) for GPS extraction.
- Conversion: `convert IMG_7732.HEIC out.jpg` (ImageMagick) preserves EXIF.
- Santa Anna reference: **-3.292475, -52.572250** (all 9 HEICs consistent).
- If coordinates can't be extracted, ASK the governor — never fabricate from web search (ambiguous farm names produce wrong results).
- Put the real coords in: Leaflet map init, `Google Maps` links, and (for FSVP docs) the facility geo-location fields.

## 3. Page anatomy (files)

| File | Purpose |
|---|---|
| `farms/<slug>/index.html` | Farm page: hero (CSS bg + inline section), story, highlights, gallery container, Leaflet map, farm nav, footer. Clone a working farm (e.g. `paulo-la-do-sitio-para`) as template. |
| `farms/<slug>/media.json` | `{"schemaVersion":1, "hero": {...}, "gallery": [{"type":"image"|"youtube", ...}]}` — note literal UTF-8 (e.g. `Pará`, NOT `\u00e1`) |
| `assets/images/farms/<slug>-*.jpg` | Web-optimized images (longest side ~1600, quality ~82, progressive) |
| `js/farms-data.js` | Farm coordinates for drift navigation |
| `cacao-journeys/brazilian-path/index.html` | Journey stop in `BRAZILIAN_PATH_DATA` + `journeyOrder` + **explicit image-path mapping** |
| `cacao-journeys/brazilian-path-data.js` | Journey stop data (if used) |
| `cooperatives/<name>/index.html` | Member-farm card on the cooperative page |

### Slug conventions
- Farm slug: `<farm>-<region>` e.g. `santa-anna-fazenda-para` — always disambiguate region if another farm shares the name (existing `fazenda-santa-ana-bahia` is a DIFFERENT farm).
- Journey stops: add BEFORE the cooperative stop, AFTER the neighboring farm.

## 4. Video evidence

- Original phone videos (.MOV, HEVC) are fine as-is for editing; upload to **admin@truesight.me YouTube** (public by default; unlisted if requested).
- Titles: descriptive (`Cacao Pods on Trunks at Santa Anna Fazenda`). Descriptions: Grok-polished transcription (faster-whisper → polish) — coherent + interesting, not raw fragments.
- Embed in `media.json` gallery as `{"type": "youtube", "videoId": "...", "title": "..."}` — rendered as iframe by `media-gallery.js`.
- Record uploads in `scripts/youtube_videos.json` (source of truth).
- Full pipeline: `fsvp/VIDEO_EVIDENCE_PROCESS.md`.

## 5. Gotchas (learned the hard way)

1. **JS string escaping**: Leaflet `bindPopup()` URLs are single-quoted; DMS coords contain apostrophes (`3%C2%B017'32.9%22S`) — MUST escape as `\'` or the map script throws SyntaxError and the map never renders. (HTML href attributes keep plain apostrophes — correct for HTML.)
2. **GitHub Pages deploy lag**: after merge, live site can 404 / serve stale JSON for ~90s. Verify via `curl` retry; check `last-modified` header + `x-cache`.
3. **Journey image-path fallback**: journey renderer builds `../../assets/images/farms/${slug}.jpg` unless an explicit `else if (stop.slug === '...')` mapping exists — add the mapping for every new farm, pointing at the ACTUAL asset filename.
4. **og:image dims**: must match the actual hero image dimensions (e.g. 1280x960 → og 1200x900), or social previews crop oddly.
5. **Media.json uses literal UTF-8** — search/replace must use the literal accented char, not `\u00e1` escape.
6. **Telegram attachment filenames are UUIDs** — original names are lost; scp originals preserve names + EXIF.
7. **Same-named farms**: always include region in slug + page copy to avoid collision (Santa Ana Bahia vs Santa Anna Pará).

## 6. Related runbooks

- `fsvp/SITE_VISIT_PROCESS.md` — site-visit documentation + PDF template
- `fsvp/VIDEO_EVIDENCE_PROCESS.md` — .MOV frame extraction + YouTube pipeline
- `fsvp/SUPPLIER_ONBOARDING_PROCESS.md` — supplier/coop records
- `AGROVERSE_QR_CODE_BATCH_GENERATION.md` — QR codes for cacao bags

---

*Last updated: 2026-08-31 (Santa Anna Fazenda build — beta #225/#226/#228/#230/#231, prod sync 2026-08-31)*
