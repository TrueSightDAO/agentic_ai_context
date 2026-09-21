# Agroverse Cacao Adventures — Autumn Solstice 2026 (deck v13, 2026-09-21)

**Canonical product name: "Agroverse Cacao Adventures — Autumn Solstice 2026"**
(PT mirror: **"Aventuras de Cacau Agroverse — Solstício de Outono 2026"**.)

## v13 change — DEPERSONALIZE (remove "Liz")
Governor instruction: *"Remove the mention of Liz so that anyone reading this feels it is
addressed to them."*

The deck previously greeted Liz by name on two slides. Both are now generic:

| Slide | v12 | v13 |
|---|---|---|
| Cover line 3 | "Welcome to Bahia, **Liz** · Itinerary 2026 · dates" | "**Welcome to Bahia** · Itinerary 2026 · dates" |
| Closing | "See you in Bahia, **Liz** — Agroverse Cacao Adventures…" | "See you in Bahia — Agroverse Cacao Adventures…" |
| Cover line 3 (PT) | "Bem-vinda à Bahia, **Liz** · Roteiro 2026 · dates" | "**Boas-vindas à Bahia** · Roteiro 2026 · dates" |
| Closing (PT) | "Até a Bahia, **Liz** — Aventuras de Cacau Agroverse…" | "Até a Bahia — Aventuras de Cacau Agroverse…" |

PT uses the gender-neutral **"Boas-vindas à Bahia"** (rather than "Bem-vinda/Bem-vindo") so
the greeting fits any reader regardless of gender.

## Verification
- **Zero** occurrences of "Liz" in the rendered 30-page text (`'Liz' in all_text == False`).
- Cover lines fit: EN x1=507pt, PT x1=566pt (< 895pt right margin).
- 30 pp (15 EN + 15 PT), PDF metadata title unchanged.

## Carried (v8–v12)
- Cover title = brand "Agroverse Cacao Adventures"; edition line = "Autumn Solstice 2026".
- At-a-glance strip: AGROVERSE CACAO ADVENTURES · AUTUMN SOLSTICE 2026 · dates.
- Cultura slide hero = Mestre Bico Duro & Tribo Bahia Mirim; Cachoeira do Cleandro photo +
  boat-waterfall bullet; Cacao Ceremony / Itacaré cultural slides.

## Build
`build2.sh` (headless Chrome → out_en/out_pt.pdf → merged). Sources: deck.html / deck_pt.html.
Pre-v13 backups: `deck.html.pre13`, `deck_pt.html.pre13`.

## Open
- Folder still `handoffs/liz_bahia_deck/` (kept to avoid breaking INDEX.json / manifest refs);
  now that the name "Liz" is out of the deck, a folder rename to
  `handoffs/agroverse_cacao_adventures/` makes sense — available on request.
- Standalone **event registration** (`go_to_market/events/`) for the package still un-filed.
