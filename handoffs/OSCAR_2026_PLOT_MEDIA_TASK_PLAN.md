# Oscar 2026 — new patch (SunMint plot) task plan (thread 41214)

**Created:** 2026-10-09 (Sophia) at Gary's request, instantiated from
`handoffs/FARM_MEDIA_TASK_PLAN_TEMPLATE.md`.
**Thread:** 41214 (sub-thread of 30550) · **Farm:** `oscar-bahia`
**Status:** 🚧 **blocked — needs a geometry source.** No code unit can unblock it.

---

## Goal

Register the **new patch** visible in the 2026 Oscar site-visit media as a **second SunMint
plot** under the existing farm `oscar-bahia` — plot row in the `SunMint Plots` sheet +
feature in `sunmint/plots/index.geojson` — so the planted area is on the public impact map.

Note this is a **second plot**, not a correction of the existing one: `OB-P1` is already
registered (see *Targets & state*).

---

## Source media

| Property | Value |
|---|---|
| Zip | `/media/processed/oscar_fazenda_2026.zip` |
| Size | 13,289,922,842 bytes (~12.4 GiB) |
| Contents | **52 HEIC + 1 JPG + 18 MOV** (archive manifest: 18 video entries with `captured_at`, `duration_s`, `farm_id`, `preview`, `produced_by`) |
| Capture date | **2026-10-03** (`CreateDate`, uniform across the batch) |
| Sibling state | `/media/processed/oscar_fazenda_2026.zip.archive.json` (11 KB) |
| Destination | `/media/processed/` — archive + YouTube daemon already consumed it; `farm_id` resolved to `oscar-bahia` on governor word (relayed via DeepSeek Local), same farm as `oscar_complete.zip` |

### ⚠️ GPS: absent — verified, not assumed

`exiftool` on samples across both formats:

| Sample | Result |
|---|---|
| `IMG_8401.HEIC`, `IMG_8411.HEIC`, `IMG_8437.HEIC` | `CreateDate` present · **no GPSLatitude / GPSLongitude** |
| `IMG_8447.MOV`, `IMG_8395.MOV` | **no GPS keys at all** (only `CreateDate`) |
| Raw ISO6709 string scan (both formats) | nothing — the coordinates are not in the bytes, it is not a tag-name mismatch |

**Contrast with the 2025 batch** (`oscar.zip`, shot 2025-09-20, same farm, same phone):
**5/5 HEIC + 45/62 MOV carried GPS** (`lat −14.053…−14.0339`, `lng −39.4415…−39.4366`).

**Root cause:** GPS was **stripped in transit** — the media almost certainly reached us via
WhatsApp/Telegram (which strip EXIF/GPS), not as original files. This is precisely the trap
called out in `SUNMINT_PLOTS_REGISTRY.md` §3.

**Why that blocks everything:** the `approx` boundary tier is *defined* as "hull of
photo/video GPS points". With **zero GPS points** there is no hull, so no generator run can
produce a boundary — and a plot row additionally needs field facts (hectares, plot name,
plot type) that no archive field supplies.

---

## Targets & state (verified 2026-10-09)

| Target | State |
|---|---|
| `SunMint Plots` sheet (spreadsheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`, SA `agroverse_qr_code_manager`) | 26 data rows. **`OB-P1` present**: `OB-P1` / `oscar-bahia` / `Oscar Fazenda Plot 1 (100-year cacao groves)` / **3.74 ha** / `proposed` / `approx` / `mature` / `Oscar` / `Urucuca, Bahia, Brazil` / verified 2026-09-06 |
| `sunmint/plots/index.geojson` (repo `sunmint`) | 23 features; `OB-P1` present with `auth: approx`, `type: mature`, 3.74 ha |
| `farm_media_manifests/oscar-bahia.json` | `farm_name`: **"Oscar Fazenda (Oscar's 100-Year Farm)"**; `plot_ids`: `["OB-P1"]`; region **Uruçuca, Bahia, Brazil**; `source` = 2025 zip (67 files) |
| `agroverse.shop/farms/oscar-bahia/` | Live farm page, title **"Oscar's Farm"** — Bahia, Brazil · tagline *"Three Generations of Cacao Wisdom"* · map pin `-14.052624, -39.438206` · member of **Coopercabruca** |

**Farm identity on record:** `farm_id` = `oscar-bahia` · display names in use:
*"Oscar's Farm"* (public page), *"Oscar Fazenda (Oscar's 100-Year Farm)"* (manifest),
*"Oscar Bahia"* (`MEDIA_ARCHIVE_PIPELINE.md`). No formal Portuguese estate name exists in
context — the "100-Year" phrasing is a descriptor (trees planted by Oscar's grandfather),
not a registered property name.

---

## Gate — what is actually needed to proceed

Any **one** of the following unblocks the plot work:

1. **`gps_walk`** *(recommended default)* — walk the new patch perimeter with a phone GPS app
   for ~10 min, export GPX/KML. Produces a real boundary, upgrades the authority tier above `approx`.
2. **CAR / INCRA polygon** — the property's official polygon, clipped to the new patch.
3. **Original un-stripped files re-sent** — email attachment / zip / AirDrop / USB, **never**
   WhatsApp or Telegram (both strip EXIF). Then the existing GPS-hull pipeline works as-is.

Plus, from Gary or the field: **hectares**, **plot name**, and **plot type**
(`mature` / `maturing` / `restoration` / `enrichment` / `research`).

> `SUNMINT_PLOTS_REGISTRY.md` §4b: **never auto-default geometry.** If a boundary cannot be
> justified, the plot does not go in.

---

## Execution order (ONE PR PER TURN) — only after the gate clears

- **PR1** — plot row appended to the `SunMint Plots` sheet (write SA; verify the read-back row).
- **PR2** — `sunmint`: add the feature to `plots/index.geojson`, regenerate, verify `feature_count` grew by 1 and `OB-P2` renders on `sunmint.html`.
- **PR3** — `farm_media_manifests`: extend `oscar-bahia.json` to schema v2 for the 2026 batch
  (add the 52 HEIC + 18 MOV with `creation_date`, `transcription_status`, `gps: null` explicitly — **do not invent lat/lon**), add `OB-P2` to `plot_ids`.
- **PR4** — `agroverse_shop_beta` farm page: 2026 gallery additions (stills only; MOVs awaiting
  YouTube publish ids).

Naming convention for the new plot id follows the existing pattern: `OB-P2`.

---

## Media pipeline notes

- Archive + YouTube work for this zip is **already done** by `farm-media-daemon` /
  `farm-media-archive` (18 video entries carry `produced_by`). This plan does not re-run it.
- MOV → MP4 (H.264) transcode and HEIC → JPEG stills follow the 2025 batch path
  (`/media/oscar_work/`, sizes staged under `heic/`, `mp4/`, `raw/`, `src/`).
- Do **not** re-ingest: the zip sits in `/media/processed/`, not an inbox.

---

## Gates

- **GPS/geometry gate** — described above. Blocks PR1/PR2.
- **UAT gate** — after PR2, the plot must be visually confirmed on the beta site before any
  prod promotion (beta-first; never push `*_prod`).
- **No money, no TDG** involved in this plan.

---

## RESUME HERE

1. **Ask Gary** (single message, two questions): (a) which patch is "the new patch" and its
   **hectares / plot name / plot_type**; (b) can Oscar do a **`gps_walk`** of it, or will the
   **original files** be re-sent un-stripped (email/zip, not WhatsApp/Telegram)?
2. On a `gps_walk` GPX/KML → build the FeatureCollection, then **PR1** (sheet row `OB-P2`) → **PR2**
   (geojson) → verify live → **PR4** (gallery).
3. On un-stripped originals → re-run the GPS-hull extraction (2025 procedure), then PR1 → PR2.
4. If neither arrives: **leave the plot unregistered.** Do not fabricate `approx` geometry from
   zero GPS points — the tier's definition forbids it.

**Do not** treat "52 photos, no GPS" as a data-quality mystery to be re-diagnosed: it is
confirmed, and the cause (courier EXIF-stripping) is known.
