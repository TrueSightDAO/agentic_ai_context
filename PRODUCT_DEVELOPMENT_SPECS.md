# Product development specifications (Agroverse physical products)

Read this when creating or updating **packaging, copacker, or retail SKU specs** (chocolate bars, pouches, display boxes, labels, GTINs, etc.) so work stays consistent with **agroverse.shop**, **market_research** scripts, and Google Workspace.

---

## 0. Google Drive location for generated Sheets (artifacts)

**Create and keep** new Google Sheets produced by scripts or AI-assisted workflows (product specs, checklists, packaging matrices, etc.) under this folder unless the user specifies otherwise:

| | |
|--|--|
| **Folder name** | (Use the Drive UI label you set; folder ID is stable below.) |
| **Folder ID** | `1esYnlwChRmv9-M3ymWYhWMPHRowhOluw` |
| **Open** | [Google Drive folder](https://drive.google.com/drive/folders/1esYnlwChRmv9-M3ymWYhWMPHRowhOluw) |

**Practice**

- **New spreadsheet:** Create in Drive **inside this folder** (or create then **Move** here), so artifacts stay discoverable.  
- **Automation:** To create files in this folder via API, use **Google Drive API** with `parents: ['1esYnlwChRmv9-M3ymWYhWMPHRowhOluw']` on `files.create`, or create in My Drive and move. The service account (`agroverse-qr-code-manager@…` or whichever key you use) must have **Editor** on the **folder** (not only on individual files).  
- **Sharing:** Folder-level access is preferred so future sheets inherit visibility rules you set on the folder.

---

## 1. Canonical workflow (preferred)

1. **Google Sheet = source of truth for checklists**  
   - One **tab per section** (e.g. meta, primary front/back, RDB, logistics, artwork, next steps).  
   - Columns: **Topic** | **What to decide / check** | **Suggested (Agroverse.shop + repo)** | **Owner** | **Status**.  
   - Pre-fill **Suggested** using live site copy (`index.html`, product pages, footer), `js/products.js`, `facebook_product_feed.xml` patterns, and repo docs — not generic CPG boilerplate unless labeled as such.

2. **Scripted populate + styling**  
   - `market_research/scripts/populate_chocolate_bar_spec_sheet.py` creates tabs (if missing), writes rows, then applies **readability formatting** (frozen header row, wrap text, column widths, header row background).  
   - Re-running **overwrites cell values** for those ranges; treat as “regenerate template,” not merge.

3. **Optional long-form Google Doc**  
   - Narrative specs or meeting notes can live in a separate Doc.  
   - For **API access**: enable **Google Docs API** on the same GCP project as the service account; share the Doc with **Editor** to `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com` (key: `agroverse_shop/google-service-account.json`) and/or `agroverse-market-research@get-data-io.iam.gserviceaccount.com` (`market_research/google_credentials.json`).

4. **Related repo docs**  
   - New **shop SKUs / PDPs / Merchant Center**: `agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md`, `docs/MERCHANT_CENTER_FIX.md`.  
   - **Feeds**: `scripts/generate_facebook_feed.py`, `productPageSlug` in `js/products.js`, apex `https://agroverse.shop` for feed URLs.

---

## 2. Example spreadsheet (81% bar)

| Item | Value |
|------|--------|
| **Spreadsheet** | [20260324 - 81% premium dark chocolate bar…](https://docs.google.com/spreadsheets/d/13WbBbbC2dgPo8itltfNvMIx2qFCgDI1aS5Ald3JDCBc/edit) |
| **Script** | `market_research/scripts/populate_chocolate_bar_spec_sheet.py` |
| **Doc (optional)** | `1cP5vq7o6QM3Sgkeklixvw4DmJW1kGD4O-qDUPDT_fC4` — long tabulated checklist (may be superseded by Sheet) |

---

## 3. What future AIs should do

- **Prefer the Sheet** for line-item tracking; extend with **new tabs** or rows, keep the five-column pattern.  
- **Pull suggestions** from: homepage title/footer, `LocalBusiness` JSON-LD, `/farms/`, `/shipments/`, existing QR copy on product pages, CSS brand colors (`:root` in site CSS).  
- **Do not commit** `google-service-account.json` or other secrets; user places keys locally.  
- **Put new spec spreadsheets** in the Drive folder in **§0** (or document here if an exception is agreed).  
- After changing the workflow, folder ID, or spreadsheet ID for a **new** product line, update **this file** and a one-line entry in **`CONTEXT_UPDATES.md`**.

---

## 4. Google API checklist

- **Sheets API** enabled for the service account’s GCP project.  
- Spreadsheet shared with **Editor** to the service account email on the key you use.  
- **Docs API** only if automating Google Docs (optional).
