# AGROVERSE Cacao Adventures — Autumn Solstice 2026 — deck v22

**EN+PT, 34 pages.** Delivered to Telegram thread 34157 (PDF msg 39050; slide previews 39051, 39057), 2026-09-29.

## What changed in v22 — 30 September itinerary

Governor's instruction: *"30th September, we update the itinerary to: Visit warehouse;
help load freight bound for San Francisco USA to truck; visit Santos factory; Visit
Coopercabruca."*

The Ilhéus / Itabuna circuit already carried three of the four stops. **v22 adds the
freight-load step** and makes the full sequence explicit, in **EN and PT**:

- **Cover:** Day-2 line → `… Ilhéus / Itabuna (30 Sep) · load SF freight`.
- **At-a-glance table:** *"Black King Warehouse (Matheus Reis) — help load freight bound
  for **San Francisco, USA** onto the truck · Santos Chocolate Factory — bean-to-bar ·
  Coopercabruca co-op."*
- **Stop 2 Warehouse slide:** new bullet — *"Help load the freight bound for San Francisco,
  USA onto the truck — the hands-on hand-off as your cacao starts its journey to the States."*
- **Day-by-day row:** *"… Black King Warehouse (load freight for San Francisco, USA),
  Santos Factory, Coopercabruca …"*

PT mirrors all four (warehouse bullet localises to "São Francisco, EUA").

## Verification

- Rebuilt 34 pp (EN 17 + PT 17) via `build2.sh`.
- PyMuPDF text check: all four occurrences present on both EN and PT pages
  (cover, at-a-glance, warehouse, day-by-day).
- **Overflow check (OCR, warehouse slide):** all 5 bullets + the "Why it matters"
  highlight render — no clipping.

## Files

- `AGROVERSE_CACAO_ADVENTURES_AUTUMN_SOLSTICE_2026_EN_PT.pdf` — v22, 34 pp (this folder)
- `deck.html`, `deck_pt.html` — source
- `mkmap_final.py`, `build2.sh` — map + build tooling

## Still parked (governor-gated)

- **@tbcitacare outreach** — drafted, held unsent (draft_id `r-3762151385599414737`).
- **Website Itacaré page** — PR #327 on beta; prod untouched.
