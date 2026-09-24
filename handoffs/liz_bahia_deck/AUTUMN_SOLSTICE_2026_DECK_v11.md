# Autumn Solstice 2026 — visitor-package deck (v11, 2026-09-21)

**Canonical name: "Autumn Solstice 2026"** (Gary's product name for the 2026 visit offering;
term coined 2026-09-21 — not previously in agentic_ai_context or repos).

## v11 change — RENAME
Governor instruction (thread 34157): *"Let's rename the deck to autumn solstice 2026."*
The product name is promoted from a subtitle line to the **deck title**:

| Element | v10 | v11 |
|---|---|---|
| Cover **title** (52pt) | "Welcome to Bahia, Liz" | **"Autumn Solstice 2026"** (PT: **"Solstício de Outono 2026"**) |
| Cover **subtitle** (20pt) | "Autumn Solstice 2026" | "Welcome to Bahia, Liz" (PT: "Bem-vinda à Bahia, Liz") |
| Filename | `LIZ_BAHIA_ORIGIN_TOUR_EN_PT.pdf` | **`AUTUMN_SOLSTICE_2026_EN_PT.pdf`** |
| HTML `<title>` | (none) | "Autumn Solstice 2026" / "Solstício de Outono 2026" |
| PDF metadata title | (none) | "Autumn Solstice 2026 — Agroverse Origin Tour (EN/PT)" |

The greeting is **retained** (demoted to subtitle) — Liz still feels personally addressed.
The at-a-glance strip (slide 2) and closing slide already carried the package name since v10.

## Verification
- 30 pp (15 EN + 15 PT), merged cleanly.
- Cover titles fit the frame: EN title x1=605pt, PT x1=686pt, both < 895pt right margin.
- Title band renders as real image data (mean ~75, std ~87 — not blank).

## Still carried (v8–v10)
- Cultura slide hero = **Mestre Bico Duro & the Tribo Bahia Mirim kids**, plus **Cachoeira do
  Cleandro** photo (EXIF −14.275214,−39.036561, 2024-10-29) + boat-waterfall bullet.
- "Itinerary 2026" / "Roteiro 2026" on the cover sub-line.

## Build
`build2.sh` (headless Chrome → out_en/out_pt.pdf → merged). Sources: deck.html / deck_pt.html.
Pre-v11 backups: `deck.html.pre11`, `deck_pt.html.pre11`.

## Open
- Folder is still `handoffs/liz_bahia_deck/` (kept to avoid breaking INDEX.json / manifest
  references). Can rename to `handoffs/autumn_solstice_2026/` on request.
