# Agroverse Invoice PDF Convention

Use this document when generating **customer invoices** as PDFs for Agroverse partners (retailers, wholesale buyers).

---

## Color scheme

Use the **truesight.me** color palette (not the old green `#2d5a27`):

| Role | Hex | Usage |
|------|-----|-------|
| Accent (gold) | `#d38900` | Header row background, horizontal rules, total amount, signature |
| Text | `#2b1d14` | Body text, labels |
| Muted | `#6f5a44` | Subtitle, secondary descriptions, footer |
| Table alt row | `#f7f1e8` | Alternating row background |
| Grid lines | `#d4c5a8` | Table borders |

---

## Layout (ReportLab)

- **Page size:** `letter`
- **Margins:** `0.75\"` all sides
- **Font:** Helvetica (default ReportLab)

### Header

- **Title:** `AGROVERSE CACAO` in bold, 22pt, gold (`#d38900`)
- **Subtitle:** `Invoice` in 9pt, muted
- **Invoice # and Date** in a two-column table below

### Bill To section

- Partner name, attention line, email address

### Line items table

Five columns:

| # | Description | Qty | Unit Price | Amount |
|---|---|:---:|:----------:|-------:|

- Header row: gold background (`#d38900`), white text
- Alternating row colors: `#f7f1e8` / white
- Grid lines: `#d4c5a8`
- Description column can include a second line in 8pt muted for subtext (e.g. "Previous batch" or "Each bag plants a tree")
- **Total Due** row: bold label right-aligned, amount in gold bold

### Payment Instructions section

- "Please make cheque payable to: **Name**"
- "Mail to:" followed by address lines in bold

### Footer

- Thin horizontal rule
- Italic "Thank you for your continued support!" centered
- Name centered in gold

---

## Upload location

- **Repo:** `TrueSightDAO/store_interaction_attachments`
- **Path:** `invoices/<partner-slug>-invoice-<YYYYMMDD>.pdf`
- **Commit message:** `Add <partner> invoice for <description>`

---

## How to generate

Use a Python script with `reportlab` on the `dao_protocol` host (where reportlab is installed):

```bash
ssh dao_protocol 'python3 << \'PYEOF\''
# ... ReportLab script ...
PYEOF
```

Then upload the base64-encoded PDF to GitHub via `upload_file_to_github` with `content_base64`.

---

## Example

See the Green Gulch invoice at:
`store_interaction_attachments/invoices/green-gulch-invoice-20260606.pdf`

---

## Related

- `PURCHASE_AGREEMENT_PDFS.md` — for purchase agreements (different format, for import/wholesale contracts)
- `WORKSPACE_CONTEXT.md` §4 — Agroverse shop context