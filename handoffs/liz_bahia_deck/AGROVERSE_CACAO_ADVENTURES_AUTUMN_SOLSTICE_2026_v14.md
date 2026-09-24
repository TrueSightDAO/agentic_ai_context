# Agroverse Cacao Adventures — Autumn Solstice 2026 (deck v14, 2026-09-21)

**Canonical product name: "Agroverse Cacao Adventures — Autumn Solstice 2026"**
(PT: **"Aventuras de Cacau Agroverse — Solstício de Outono 2026"**.)

## v14 change — REMOVE THE RECIPIENT NAME (for real)
Governor: *"The image. We should remove Liz."* — the v13 pass removed the two visible "Liz"
greetings but MISSED the actual personalization: a **footer** on three slides per language
reading **"Prepared for Elizabeth Wong · Agroverse / TrueSight DAO"**.

**Why v13 missed it:** v13 verified by searching the PDF text for the string `"Liz"`.
"Elizabeth" does not contain the substring "Liz", so the check passed while the name
remained on pages 2, 3 and 9 (and PT equivalents).

The governor said "the image" — but the name was **not** in any image. It was live text in
the `.foot` footer divs (OCR of an earlier render is what surfaced it). No image asset
(`img/*.jpg`) carries the name.

| Element | v13 | v14 |
|---|---|---|
| Slide footer ×3 (EN) | "Prepared for Elizabeth Wong · Agroverse / TrueSight DAO" | "Agroverse / TrueSight DAO" |
| Slide footer ×3 (PT) | "Preparado para Elizabeth Wong · Agroverse / TrueSight DAO" | "Agroverse / TrueSight DAO" |

## Verification (definitive — text AND pixels)
- Text layer: none of `Liz`, `Elizabeth`, `Wong`, `Prepared for`, `Preparado para` present.
- **Pixel sweep:** rendered all 30 pages at 1.5× and OCR'd each — zero hits for any of the
  five tokens across every page. (`pixel sweep: CLEAN`)
- Cover lines unchanged and fitting (EN line-3 x1=507pt, PT 566pt < 895pt margin).
- 30 pp (15 EN + 15 PT).

## Method note (self-improvement)
The v13 near-miss came from verifying with a **substring search for a nickname** rather than
the recipient's **full canonical identity**. Rule going forward: when de-personalizing a doc,
(b) search for the full name AND (b) OCR the *rendered* pages, not just the text layer —
baked-in/alternate-name occurrences are otherwise invisible.

## Carried (v8–v13)
- Cover title = brand "Agroverse Cacao Adventures"; edition line "Autumn Solstice 2026";
  at-a-glance strip + closing slide branded; no personal greeting.
- Cultura slide hero = Mestre Bico Duro & Tribo Bahia Mirim; Cachoeira do Cleandro photo +
  boat-waterfall bullet; Cacao Ceremony / Itacaré cultural slides.

## Build
`build2.sh` (headless Chrome → out_en/out_pt.pdf → merged). Sources: deck.html / deck_pt.html.
Pre-v14 backups: `deck.html.pre14`, `deck_pt.html.pre14`.

## Open
- Handoff **folder** is still `handoffs/liz_bahia_deck/` — and its `README.md` /
  `build.sh` still say "Liz Bahia Origin Tour". Offered to rename the folder to
  `handoffs/agroverse_cacao_adventures/` and de-personalize the README/build comments.
- Standalone **event registration** (`go_to_market/events/`) for the package still un-filed.
