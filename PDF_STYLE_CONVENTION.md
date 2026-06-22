# PDF Style Convention — Saffron Monk

> **Canonical reference for PDF generation across all TrueSight DAO projects.**
> Every `.md` document in the DAO's digital infrastructure should have a corresponding `.pdf` generated using this style.

---

## 1. Why This Convention

TrueSight DAO produces many documents — implementation plans, proposals, reports, agreements, runbooks. A consistent visual identity builds trust, professionalism, and brand recognition. The **Saffron Monk** style is the DAO's house style for all generated PDFs.

**Brand name:** Saffron Monk
**Design principle:** Warm, grounded, readable — like a cacao ceremony in document form.

---

## 2. Brand Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Saffron | `#C98A2D` | Primary accent — header band, decorative elements |
| Clay | `#8A5A1D` | Secondary accent — links, secondary headers |
| Cacao Dark | `#3D2B1F` | Titles, strong headings |
| Cacao Mid | `#5A4632` | Subheadings |
| Body | `#222222` | Body text |
| Muted | `#888888` | Captions, footer text, page numbers |
| Rule | `#DDDDDD` | Table header fill, separators, grid lines |
| Zebra | `#FBF7EF` | Light cream — alternating table row background |
| White | `#FFFFFF` | Page background, table row background |

---

## 3. Typography

| Element | Font | Size | Leading | Color |
|---------|------|------|---------|-------|
| Document title (header band) | Helvetica Bold | 14 pt | — | White |
| H1 heading | Helvetica Bold | 15 pt | 19 pt | Cacao Dark |
| H2 heading | Helvetica Bold | 12.5 pt | 16 pt | Cacao Dark |
| H3 heading | Helvetica Bold | 11 pt | 14 pt | Cacao Mid |
| Body text | Helvetica | 10 pt | 14.5 pt | Body |
| Bullet text | Helvetica | 10 pt | 14.5 pt | Body |
| Table header | Helvetica Bold | 9 pt | 12 pt | Cacao Dark |
| Table cell | Helvetica | 9 pt | 12 pt | Body |
| Footer | Helvetica | 8 pt | — | Muted |
| Code/monospace | Courier | 9 pt | — | Body |

**Notes:**
- Helvetica is used instead of Helvetica Neue because it's built into reportlab and available on all deployment targets without TTF files.
- Bold is `Helvetica-Bold`, italic is `Helvetica-Oblique`.

---

## 4. Page Furniture

### Header Band
- **Height:** 42 pt from the top of the page
- **Fill:** Saffron (`#C98A2D`), full page width
- **Content:** Document title in white Helvetica Bold 14 pt, left-aligned at page margin
- **Every page** gets the header band (first page and later pages)

### Footer
- **Position:** 28 pt from the bottom of the page
- **Left:** "TrueSight DAO" in Muted Helvetica 8 pt
- **Right:** "Page N" in Muted Helvetica 8 pt
- **Every page** gets the footer

### Margins
- **Left/Right:** 60 pt
- **Top:** Header band height (42 pt) + 24 pt clearance
- **Bottom:** 48 pt

---

## 5. Tables

All Markdown pipe tables (`| a | b |` + `|---|---|`) must render as **real tables**, never as raw pipe text.

| Property | Value |
|----------|-------|
| Header row fill | Rule (`#DDDDDD`) |
| Row backgrounds | Alternating White / Zebra (`#FBF7EF`) |
| Grid lines | 0.5 pt, Rule (`#DDDDDD`) |
| Cell padding | 5 pt left/right, 4 pt top/bottom |
| Vertical alignment | Top |
| Column widths | Equal distribution across content width |
| Header row | Repeated on page breaks |

---

## 6. Supported Markdown Subset

PDF generators must support at minimum:

| Syntax | Renders As |
|--------|-----------|
| `# Heading` | H1 (Cacao Dark, 15 pt) |
| `## Heading` | H2 (Cacao Dark, 12.5 pt) |
| `### Heading` | H3 (Cacao Mid, 11 pt) |
| Blank line | Paragraph break (6 pt spacer) |
| `- item` or `* item` | Bullet (•) with 14 pt left indent |
| `**bold**` | Bold |
| `*italic*` | Italic |
| `| a \| b |` + `|---|---|` | Real table (gray header, zebra rows) |
| `---`, `***`, `___` | Horizontal rule → vertical spacing |

---

## 7. PDF Generation Workflow

For every significant `.md` document in the DAO's infrastructure:

1. Write the `.md` file with full content
2. Generate a corresponding `.pdf` using the Saffron Monk style
3. Commit both files together (same PR, same branch)
4. The `.pdf` filename matches the `.md` filename, e.g.:
   - `IMPLEMENTATION_PLAN.md` → `IMPLEMENTATION_PLAN.pdf`
   - `FEATURE_IMPLEMENTATION_CONVENTION.md` → `FEATURE_IMPLEMENTATION_CONVENTION.pdf`

**Generation tool:** Use the `generate_pdf` tool (available in truesight_autopilot) with:
- `content`: The full markdown content
- `title`: The document title (shown in the saffron header band)
- `output_path`: Path to save the PDF

---

## 8. Implementation Reference

The reference implementation is in `truesight_autopilot/app/tools/pdf_tools.py` — the `generate_pdf` function. All PDF generators across the DAO should match this style.

---

*Last updated: 2026-06-07*