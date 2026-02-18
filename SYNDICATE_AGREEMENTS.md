# Syndicate Agreement Drafting — TrueSight DAO

Reference for drafting new Export Trade Financing Syndicate Agreements. Use when creating agreements for AGL shipments or operational funds.

**Quick reference (read this first):**
- **Shipment financing contract** (e.g. AGL14): 20% DAO fee on proceeds. Direct cacao shipment with physical collateral.
- **Operational fund contract** (e.g. AGL15): **No 20% fee** on proceeds. Fund invests in other AGLs; those AGLs already charge 20% — do not double-charge. Financiers receive proportional share of capital and returns.
- **Source data:** Shipment Ledger Listing (Google Sheets). Capital amounts in USD unless otherwise noted (e.g. AGL14 = USD 456.49).
- **Exhibit:** Use "Location of AGLnn: https://agroverse.shop/aglnn" only — do not add redundant "Ledger spreadsheet" URL (Location already resolves to it).

---

## 1. Source data

**Shipment Ledger Listing** (single source of truth):
- URL: https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit?gid=483234653#gid=483234653
- Key columns: Shipment ID, Shipment Date, Status, Description, Cargo Size, Cacao (kg), Transaction Type, Capital Injection, Ledger URL, Contract URL, TrueSight DAO URL, Ledger spreadsheet URL

---

## 2. Precedence: shipment vs operational fund

| Contract type | DAO fee on proceeds | Rationale |
|---------------|---------------------|-----------|
| **Shipment financing contract** | 20% | Direct cacao shipment; DAO charges 20% for fund management. |
| **Operational fund contract** | None (0%) | Fund invests in other AGLs; those AGLs already charge 20%. No double-charging. |

### Shipment financing contract
- **DAO management fee: 20%** — 20% of net profit is retained by TrueSight DAO; the remaining 80% is distributed to financiers (proportionally). Same 20% applies to offer-to-purchase markup, withdrawal fee, transfer-of-ownership facilitation fee.
- **Shortfall compensation:** 1 USD = 1 TDG.

### Operational fund contract
- **No DAO fee** at the operational fund level when the fund invests in other AGLs (which already charge 20%).
- Financiers receive their proportional share of capital and returns without an additional fee layer.
- **Shortfall compensation:** 1 USD = 1 TDG.

---

## 3. Template and drafts

| File | Purpose |
|------|---------|
| `notarizations/syndicate_agreement_template.md` | Template with placeholders; 20% fee; cacao shipment + operational fund variants |
| `notarizations/20260216_AGL14_export_trade_financing_syndicate_agreement.md` | AGL14: 40 kg Oscar Fazenda, USD 456.49, **shipment** (20% fee) |
| `notarizations/20260216_AGL15_export_trade_financing_syndicate_agreement.md` | AGL15: **operational fund** (no 20% fee—invests in other AGLs) |

**Location:** `notarizations/` (local; may sync to GitHub TrueSightDAO/notarizations or similar).

### PDF generation (with logo header)

When generating PDFs from syndicate agreement `.md` files, **always use the TrueSight DAO logo as the header.**

- **Script:** `notarizations/scripts/generate_syndicate_pdf.mjs`
- **Logo (use as header):** `/Users/garyjob/Applications/.github/assets/20221219 - Gary logo white background squarish.jpeg`  
  Fallback: `/Users/garyjob/Applications/.github/assets/20240612_truesight_dao_logo.png`
- **Commands:**
  ```bash
  cd notarizations
  npm install   # once
  npm run generate-pdf       # both AGL14 and AGL15
  npm run generate-pdf:agl14 # AGL14 only
  npm run generate-pdf:agl15 # AGL15 only
  node scripts/generate_syndicate_pdf.mjs <filename.md>  # any .md file
  ```
- **Output:** PDFs are written next to the source `.md` files (e.g. `20260216_AGL14_export_trade_financing_syndicate_agreement.pdf`).

---

## 4. How to draft a new agreement

1. **Pull shipment data** from Shipment Ledger Listing (or use existing context).
2. **Determine agreement type:**
   - **Shipment financing (cacao shipment):** Specific shipment with physical cacao collateral. **Charge 20%** DAO fee. Use cacao shipment template.
   - **Operational fund:** Mixed-use fund that invests in other AGLs (procurement, freighting, shipping, consignment, etc.). **No 20% fee** — underlying AGLs already charge 20%. Omit cacao-specific clauses (3.6–3.8).
3. **Fill placeholders** from `syndicate_agreement_template.md`:
   - `[AGL_ID]`, `[DATE]`, `[SHIPMENT_DESCRIPTION]`, `[CARGO_SIZE]`, `[CACAO_KG]`, `[FINANCING_AMOUNT]`, `[COST_SCHEDULE]`, `[LEDGER_URL]`, `[LEDGER_SPREADSHEET_URL]`
4. **Save as** `notarizations/YYYYMMDD_AGLnn_export_trade_financing_syndicate_agreement.md`.
5. **Generate PDF** with logo header: `cd notarizations && npm run generate-pdf` (or run script for specific file). See "PDF generation (with logo header)" above.
6. **Copy into Google Doc** (or use generated PDF) for signatures.

---

## 5. Google Docs (stubs / live versions)

Agreements are often drafted in Markdown locally, then pasted into Google Docs for collaboration and PDF export. Direct Google Docs API access is not required if Markdown/PDF files are maintained in `notarizations/`.

- AGL14 stub: https://docs.google.com/document/d/1V2XrHdgJfLmogixzLR3jsUbneLMkwTB7DY-Y3E7eXBQ/edit
- AGL15 stub: https://docs.google.com/document/d/1nEf0amclzTjzuG1QI15sly4lqOO5zGPaoe-79wsGULo/edit

---

## 6. Service accounts for Drive/Sheets access

To read Google Docs or Sheets programmatically, share with:
- `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com`
- `agroverse-market-research@get-data-io.iam.gserviceaccount.com`

Credentials: `truesight_me/google-service-account.json`, `market_research/google_credentials.json`.
