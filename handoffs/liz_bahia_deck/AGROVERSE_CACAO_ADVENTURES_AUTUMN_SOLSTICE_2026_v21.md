# AGROVERSE Cacao Adventures — Autumn Solstice 2026 — deck v21

**EN+PT, 34 pages.** Delivered to Telegram thread 34157 (msgs 37889–37891), 2026-09-26.

## What changed in v21

- **Culture slide (EN+PT):** new bullet *"Quilombos & the Feira Quilombola"* —
  eight certified quilombola communities, the historic root of both cacao and
  capoeira; the monthly *Feira Quilombola* at **Porto de Trás** opens with
  **Capoeira Angola** (the slow, berimbau-led lineage); the year-round
  **Roteiro Quilombola** can be arranged for the trip dates.
- **Map (EN+PT):** **Porto de Trás** added as pin **#10** with a new **QUILOMBO**
  legend group — in both the rendered map PNG and the slide's inline HTML legend
  (EN line 289 / PT line 274).
- **Layout fix:** the new bullet pushed the harvest note off the Culture slide
  (`overflow:hidden` clipped it). Fixed with a scoped `.cul` list rule
  (11.6pt / 1.42 line-height) + a tighter bullet. Verified both the bullet and the
  harvest note render — EN p12, PT p29 — via PyMuPDF text extraction + OCR.
- **Source sync:** `deck.html` / `deck_pt.html` in this folder replaced the stale
  v11 originals (26 KB → 35 KB); this also removes the older guest-name content.

## Also in this revision line (v19/v20, delivered earlier same-day)

- "Lively, on its own terms" culture bullet (EN+PT).
- Harvest-season note: visits are organised in **September**, when the Bahia cacao
  *safra* begins.
- Full-page map slides (town + region) with HTML legends, EN+PT.

## Files

- `AGROVERSE_CACAO_ADVENTURES_AUTUMN_SOLSTICE_2026_EN_PT.pdf` — v21, 34 pp (this folder)
- `deck.html`, `deck_pt.html` — source (headless-Chrome → PDF)
- `mkmap_final.py`, `build2.sh` — map + build tooling

## Open / next

- **@tbcitacare outreach** — drafted, held for governor go. Contact:
  *Turismo Comunitário – Quilombos de Itacaré*, tbcquilombosdeitacare@gmail.com
  (ask: confirm the October Feira date + book a Roteiro Quilombola visit within
  29 Sep–8 Oct 2026).
