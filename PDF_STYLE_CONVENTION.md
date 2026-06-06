# TrueSight DAO — PDF / Document House Style

**Binding on every PDF generated within the DAO** — by Sophia (autopilot `app/tools/pdf_tools.py`),
by `market_research/` generators, and by any LLM (Claude / Cursor / Codex / etc.) producing a document
for the DAO. The goal: every PDF we hand to a partner, governor, or the public looks like it came from
**one brand**, not from whichever tool happened to render it.

**Canonical exemplar:** `market_research/briefs/2026-06-05_dtc_paid_ads_brief_hubert_yee.pdf` (the Hubert
Yee DTC brief) and the invoice PDFs Gary prompt-styled on 2026-06-05. Match these. This is the
**"Saffron Monk"** brand palette (same tokens as truesight.me) applied to documents.

## Palette (use these exact hex values)

| Role | Hex | Use |
|---|---|---|
| Body text | `#222222` | all paragraph/body copy (soft near-black, never pure `#000`) |
| **Saffron (primary accent)** | `#C98A2D` | top header band, section accents, key rules |
| Clay / caramel (secondary accent) | `#8A5A1D` | links, emphasis, callouts |
| Cacao brown (dark) | `#3D2B1F` | titles/headings on light bg, strong emphasis |
| Cacao brown (mid) | `#5A4632` | subheads, secondary headings |
| Muted gray | `#888888` | captions, footnotes, metadata labels |
| Rule / table-gray | `#DDDDDD` | table header fill, row separators, light zebra striping |

## Typography

- **Family:** **Helvetica Neue** (Regular / Bold / Italic). Monospace (code, IDs, IPs, commands): **Andale Mono** (fallback: any monospace). Do **not** use Times New Roman or default serif.
- **Type scale:**
  - Document title — Helvetica Neue **Bold ~19pt**
  - Section heading (numbered) — **Bold ~14pt**
  - Subheading — **Bold ~11pt**
  - Body — Regular **10pt** (secondary/dense **9pt**)
  - Caption / footnote — **8pt** (muted gray)
  - Code / mono — **8pt** Andale Mono

## Layout

1. **Saffron header band** (`#C98A2D`, full content width, ~33pt tall) at the top of page 1, with the document title on it.
2. **Metadata block** directly under the title — `For: … / From: … / Date: … / Status: …` (labels in muted gray).
3. **Numbered sections** (`1.`, `2.`, …) with Bold 14pt headings.
4. **Content width ~475pt** on US-Letter (≈1″ margins).
5. **Footer:** small muted-gray line — "TrueSight DAO" + page number.

## Tables — the #1 rule

**Render tables as real tables. Never dump raw Markdown pipes (`| col | col |`) into a PDF.**
(The 2026-06-06 autopilot upgrade proposal violated this — its tables printed as literal `| … |` text because `pdf_tools.py` uses reportlab's default stylesheet.) Table style:
- Header row: `#DDDDDD` fill, Bold text.
- Body rows: light zebra striping (alternate `#FFFFFF` / very light gray), thin `#DDDDDD` separators.
- Cell text 9–10pt Helvetica Neue.

## Implementation notes

- **Sophia's `app/tools/pdf_tools.py` currently uses `getSampleStyleSheet()` (reportlab defaults)** → it does NOT yet emit this style and renders Markdown tables as raw text. It must be updated to: register Helvetica Neue + Andale Mono, define ParagraphStyles per the type scale + palette, draw the saffron header band on the canvas, and convert Markdown tables to reportlab `Table`/`TableStyle`. Until then, Sophia PDFs will look off-brand.
- Prefer a **single shared styling helper** that all generators import, rather than each re-implementing the palette — so the brand only lives in one place.
- HTML→PDF generators (weasyprint/wkhtmltopdf) should use a shared brand CSS encoding the same palette/fonts.

## Quick checklist before shipping any PDF
- [ ] Saffron header band + title on page 1
- [ ] Helvetica Neue throughout (Andale Mono for code/IDs); no serif
- [ ] Body `#222`, accents from the palette above
- [ ] Tables rendered as tables (gray header, zebra) — **no raw `|` pipes**
- [ ] Metadata block under title; muted-gray footer with page number
