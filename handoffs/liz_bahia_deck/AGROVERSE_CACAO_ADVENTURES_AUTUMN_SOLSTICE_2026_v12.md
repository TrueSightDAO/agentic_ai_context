# Agroverse Cacao Adventures — Autumn Solstice 2026 (deck v12, 2026-09-21)

**Canonical product name: "Agroverse Cacao Adventures — Autumn Solstice 2026"**
(Gary's naming, thread 34157. PT mirror: **"Aventuras de Cacau Agroverse — Solstício de Outono 2026"**.)

## v12 change — RENAME (extend to the brand)
Governor instruction: *"I also think the deck should be renamed Agroverse cacao adventures
autumn solstice 2026."* The **brand** becomes the cover title; the **edition** becomes the
second line.

| Element | v11 | v12 |
|---|---|---|
| Cover **title** (48→46pt) | Autumn Solstice 2026 | **Agroverse Cacao Adventures** (PT: **Aventuras de Cacau Agroverse**) |
| Cover **line 2** (20pt) | Welcome to Bahia, Liz | **Autumn Solstice 2026** (PT: **Solstício de Outono 2026**) |
| Cover **line 3** (13.5pt) | Agroverse Origin Tour — Itinerary 2026 · dates | "Welcome to Bahia, Liz · Itinerary 2026 · dates" (greeting kept) |
| At-a-glance strip (slide 2) | AUTUMN SOLSTICE 2026 · AGROVERSE ORIGIN TOUR · dates | **AGROVERSE CACAO ADVENTURES · AUTUMN SOLSTICE 2026 · dates** |
| Closing slide | …Autumn Solstice 2026 · dates | **…Agroverse Cacao Adventures · Autumn Solstice 2026 · dates** |
| HTML `<title>` | Autumn Solstice 2026 | Agroverse Cacao Adventures — Autumn Solstice 2026 |
| Filename | AUTUMN_SOLSTICE_2026_EN_PT.pdf | **AGROVERSE_CACAO_ADVENTURES_AUTUMN_SOLSTICE_2026_EN_PT.pdf** |
| PDF metadata title | Autumn Solstice 2026 — Agroverse Origin Tour (EN/PT) | Agroverse Cacao Adventures — Autumn Solstice 2026 (EN/PT) |

The greeting ("Welcome to Bahia, Liz") is **retained** on the cover's third line — Liz is still
personally addressed without crowding the brand.

## Verification
- 30 pp (15 EN + 15 PT), merged cleanly.
- Cover text fits: EN xmax=707pt / PT xmax=744pt (< 895pt right margin); text ymax=331pt (< 540pt page height — no overflow).
- Title set to 46pt (from 52pt) so the longer brand line fits on one line on both covers.

## Carried (v8–v11)
- Cultura slide hero = Mestre Bico Duro & the Tribo Bahia Mirim kids; plus **Cachoeira do
  Cleandro** photo + boat-waterfall bullet; Cacao Ceremony / Itacaré cultural slides.

## Build
`build2.sh` (headless Chrome → out_en/out_pt.pdf → merged). Sources: deck.html / deck_pt.html.
Pre-v12 backups: `deck.html.pre12`, `deck_pt.html.pre12`.

## Open
- Folder still `handoffs/liz_bahia_deck/` (kept to avoid breaking INDEX.json / manifest refs).
  Rename to `handoffs/agroverse_cacao_adventures/` available on request.
- Deck carries the product name; the standalone **event registration**
  (`go_to_market/events/`) for "Agroverse Cacao Adventures — Autumn Solstice 2026" is still
  un-filed — offered to Gary.
