# Site visit / inspection log — FSVP process

## Purpose

FSVP requires the importer (TrueTech Inc) to verify that foreign suppliers produce food meeting US safety standards. The site visit log is the primary physical-verification record — a dated, geo-located inspection of a supplier facility (farm / fermentation / drying / packing) with observations mapped to the standard FSVP hazard set.

## When to file one

- First visit to a **new supplier** (initial verification, before first purchase)
- First visit to a **new farm / facility** under an existing supplier (e.g. a CEPOTX member farm)
- Periodic re-verification (refresh interval is per the recurring-verification declaration; keep site visits current)
- A facility materially changes (new processing line, new site)

## Output + location

- **PDF** committed to `fda_fsvp/suppliers/<supplier>/YYYYMMDD_<Supplier>_site_visit_to_<farm>.pdf`
- Update `suppliers/<supplier>/entity.json` `source_farms` (new farm) and `source_documents` (new PDF)
- PR to `fda_fsvp` (never push to main directly)

## The 7-page CEPOTX template (canonical structure)

Page 1 — title `{Supplier} site visit {date}` + statement *"This document established record for FSVP compliance requirements of our site visit to {supplier} facility"*:
- Supplier and visit dates: Supplier name visited · Site name (farmer/farm) · Site code · Date
- Facilities visited: counts of cacao farms / fermentation facilities / drying facilities
- Facility A — Cacao farm: Geo location (Latitude, Longitude, Google Map link) + Observations table header

Pages 2–6 — observation tables (Visual Observation | Remarks), one block per facility:

| Facility | Observations (exact rows used in prior CEPOTX PDFs) |
|----------|-----------------------------------------------------|
| A — Farm | Microbial Contamination (salmonella) · Insect Infestation · Foreign objects like rocks, dirt, or debris from the field |
| B — Fermentation | Inclusion of non-cacao materials in fermentation containers · Contamination from pesticides or chemicals used in cacao plantations |
| C — Drying | Mold growth due to improper drying practices · Inclusion of foreign objects during drying and sorting process · Residues from cleaning agents or pesticides |

Remarks should describe the actual observed practice (harvesting method, fermentation regime, drying schedule — e.g. turnover every 30 min first 2 days, then 1 hr, then 4–5×/day).

Page 7 — signature: *Sincerely, Zhiwen Teh, President, TrueTech Inc (EIN: 88-3411514), admin@truesight.me, +1 415 300 0019*.

## Photo / video evidence workflow

1. **Photos**: run OCR first (`ocr_image`) — usually no text on farm photos; if none, use Grok vision (`app/grok_client.py grok_analyze_images`) to get a per-photo scene description (crops, buildings, people, equipment).
2. **Video**: extract frames with `ffmpeg` (installed on the autopilot box). Pick the sharpest, most informative frames (drying shed, fermentation box, pods on tree) and attach them as evidence pages in the PDF with captions.
3. If EXIF GPS is present, use it for the geo fields. If not (Telegram uploads strip EXIF), get coordinates from the governor / Google Maps — **never invent coordinates on a compliance document**.

## Required fields that must be confirmed by the governor (never guessed)

- Date of visit (drives the filename + page-1 header)
- Site code (if any)
- Geo coordinates (lat/long) + Google Map link
- Farm owner / site contact name
- Confirmation of the practice remarks (or corrected remarks from the visit notes)

## Checklist before PR

- [ ] Filename matches `YYYYMMDD_<Supplier>_site_visit_to_<farm>.pdf` with the **event** date
- [ ] All 8 standard observation rows present across the 3 facilities
- [ ] Geo location fields filled (not placeholder)
- [ ] Photos / frames embedded or referenced with captions
- [ ] Signed with the TrueTech block
- [ ] `entity.json` `source_farms` + `source_documents` updated
- [ ] No PIN/CPF/private identifiers in the PDF
