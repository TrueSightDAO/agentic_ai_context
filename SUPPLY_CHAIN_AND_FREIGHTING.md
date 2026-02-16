# Supply Chain, Freighting & Unit Cost Economics

> **Purpose:** Single reference for AI assistants (and future workspaces) to answer supply chain, production, and logistics questions—including inventory by location, freighting options, and unit-cost/cacao economics.  
> **Schema detail:** See **tokenomics** repo `SCHEMA.md` for full sheet/column definitions. This doc summarizes logic, data sources, and how to replicate behavior for prompts like the use case below.  
> **Repos:** Logic lives in **tokenomics**. Clone if needed: `git clone https://github.com/TrueSightDAO/tokenomics`. See also **WORKSPACE_CONTEXT.md** §6 and **PROJECT_INDEX.md** (GitHub column).

---

## 1. Where the logic lives

| Concern | Location | Entry points |
|--------|----------|--------------|
| **Inventory by location/manager** | tokenomics | `google_app_scripts/tdg_inventory_management/web_app.gs`; sheet **offchain asset location** (Main Ledger spreadsheet) |
| **Freight & local shipping** | tokenomics | `google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`, `README.md` |
| **Per-shipment/AGL ledger balances** | tokenomics | **Shipment Ledger Listing** → per-ledger **Balance** sheets (see SCHEMA.md) |
| **Unit costs, cacao pricing, processing** | tokenomics | Main Ledger spreadsheet sheets (see §4); **SCHEMA.md** for columns |

**Main spreadsheet (Main Ledger & Operations):**  
`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`  
https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit

### Key locations (canonical)

- **Matheus warehouse:** Ilhéus, Brazil.  
- **Kirsten warehouse:** San Francisco, US.  
- **Matheus ↔ Kirsten:** Always **freighting** (international). They are in different countries; do not use local/USPS for this lane. Use the Brazil → US freight logic (§3).

---

## 2. Inventory: “How many units of X, Y, Z at [location]?”

### 2.1 Data sources

- **offchain asset location** (Main Ledger spreadsheet)  
  - **Columns (see SCHEMA.md):** A = Currency, B = Location, C = Amount Managed, D = Unit Cost, E = Total Value  
  - In code, column B is often referred to as **“manager”** (e.g. Shipping Planner / Inventory API). So “location” = the value in column B (e.g. a person name or a warehouse label like “Matheus warehouse”).
- **AGL / shipment ledgers**  
  - Ledger list: **Shipment Ledger Listing** (Column A = ledger/shipment name, Column L = Ledger URL, Column AB = Resolved URL).  
  - Each ledger has a **Balance** sheet: Manager Names (col H), Asset Quantity (col I), Asset Name (col J); data from row 6.

### 2.2 How to answer “How many units of X, Y, Z in Brazil in Matheus warehouse?”

1. **Main inventory:** Filter **offchain asset location** by:
   - Column B (Location) = value that corresponds to “Matheus warehouse” (or the exact string used, e.g. “Matheus” or “Matheus warehouse, Brazil”).
   - Column A (Currency) in {X, Y, Z} if you want specific products.
   Sum Column C (Amount Managed) per Currency.
2. **AGL ledgers:** If that location also appears as a manager in AGL Balance sheets, open each ledger from **Shipment Ledger Listing**, read **Balance** sheet (Manager Names col H, Asset Quantity col I, Asset Name col J), filter by manager/location and by asset name in {X, Y, Z}, sum quantities.

### 2.3 APIs (optional)

- **List “managers” (locations):**  
  `GET ...?list=true` → Inventory Management API (see tokenomics `API.md`).  
- **Inventory for one location:**  
  `GET ...?manager=<URL-encoded Location value>` → returns assets (currency, amount) for that location.  
- **Shipping Planner** also uses `list_managers` and `get_inventory&manager=<key>` (same “manager” = column B Location).

---

## 3. Freighting: “Options for freighting these to Kirsten warehouse in San Francisco”

### 3.1 Matheus (Ilhéus, Brazil) → Kirsten (San Francisco): always freight

Movement **between Matheus warehouse (Ilhéus, Brazil) and Kirsten warehouse (San Francisco)** is always **international freighting**—different countries. Do **not** use local/USPS for this lane. Use the Brazil → US freight logic below.

**Two modes in the system (for other lanes):**

- **Local shipping:** USPS via EasyPost; use only when **both** origin and destination are in the US (e.g. moving within the US to Kirsten’s address).
- **Freight:** Brazil → US (air + inland + customs). Use for **Matheus → Kirsten** and any other Brazil → US moves.

### 3.2 Where it’s implemented

- **Script:** `tokenomics/google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`  
- **README:** `tokenomics/google_app_scripts/tdg_shipping_planner/README.md`  
- **Freight cost sheet:** Spreadsheet ID `10Ps8BYcTa3sIqtoLwlQ13upuxIG_DgJIpfzchLjm9og`, sheet **“Cost Breakdown”** (or “Totals by Weight”). Weight tiers (kg): 200, 300, 500, 750, 1000.

### 3.3 Freight cost logic (Brazil → US)

Function **getFreightCost(weightKg, cargoValueUsd, options)** builds a full line-item estimate. Replicate or call this logic for “what are the different options for freighting” in the Brazil → US case.

**Weight:**

- Product weight from **Currencies** (Column K = grams, Column L = ounces; K takes precedence).  
- Plus packaging: **box** (base e.g. 11.5 oz + optional per-item) or **pallet** (e.g. 35 kg).  
- Total weight in kg is used for freight tiers and per-kg rates.

**Line items (all USD):**

| # | Item | Type | How it’s calculated |
|---|------|------|---------------------|
| 1 | Air Freight (airport to airport) | Variable | Rate per kg (tiers 200–1000 kg); interpolate between tiers. Example rates: 200→3.50, 300→3.40, 500→3.30, 750→3.30, 1000→3.20 USD/kg. |
| 2 | Export Documentation | Fixed | 95.00 |
| 3 | Inland Transport (Brazil) | Fixed + variable | 695 + 0.15% of cargo value |
| 4 | Brazil Airport Charges | Variable | 0.30/kg, minimum 250 |
| 5 | US Airline Terminal Fee | Fixed | 212.50 |
| 6 | US Import Handling Fee | Fixed | 125.00 |
| 7 | US Customs Clearance | Fixed | 150.00 |
| 8 | Invoice Line Items | Conditional | First 3 lines free, then 5 per extra line |
| 9 | FDA Processing | Conditional | 100 if FDA required (typical for cacao) |
| 10 | Bond (Single-Entry) | Conditional | If required: max(100, 6 per 1000 cargo value + duty) |
| 11 | MPF (Merchandise Processing Fee) | Variable | 0.3464% of cargo value, min 33.58, max 651.50 |
| 12 | US Customs Exam Charges | Conditional | e.g. 250 per exam |
| 13 | Duty | Variable | cargo_value × (duty_percent / 100) if duty percent > 0 |

**Options:** fdaRequired, bondRequired, invoiceLines, customsExams, dutyPercent. Cargo value default can be e.g. weight_kg × 5 if not provided.

**Matheus → Kirsten:** Always use freight (getFreightCost). For any other **US → US** move (e.g. another US warehouse → Kirsten), use EasyPost/USPS.

### 3.4 Replicating the behavior for an AI

1. Resolve **inventory** for origin location (e.g. Matheus warehouse, Ilhéus) and chosen products X, Y, Z.  
2. Get **weights** from **Currencies** (Column K or L) for each product; compute total product weight + packaging (box or pallet).  
3. **Matheus (Ilhéus) → Kirsten (San Francisco):** Always **freight**. Compute **getFreightCost(total_kg, cargo_value_usd, options)** with the line items above; present breakdown as “freight options” (one scenario per packaging type / cargo value if needed).  
4. **US → US (other lanes only):** Use EasyPost/USPS from origin to destination with same total weight.

---

## 4. Unit cost & cacao economics (from SCHEMA.md)

Use **tokenomics/SCHEMA.md** as the source of truth for column names and sheet IDs. Below is a short index of **unit-cost and economic** components.

### 4.1 Sheets and columns (Main Ledger spreadsheet)

- **offchain asset location**  
  - **Unit Cost:** Column D  
  - **Total Value:** Column E  
  - (Currency A, Location B, Amount Managed C already described above.)

- **off chain asset balance**  
  - **Balance:** Column B  
  - **Unit Value:** Column C  
  - **Value (USD):** Column D  
  - Cell D1 = total USD value of offchain assets.

- **Currencies**  
  - **Price in USD:** Column B  
  - **Unit Weight (grams):** Column K  
  - **Unit Weight (ounces):** Column L  
  - Product names in Column A; used for pricing and shipping weight.

- **Agroverse Price Components**  
  - **Description,** **Amount** (price component breakdown).

- **Agroverse Cacao Category Pricing**  
  - **Type,** **Multiplier** (category-based pricing multipliers).

- **Agroverse Cacao Processing Cost**  
  - **Facility Name,** **Process name,** **Cost,** **Currency,** **Status Date,** contact/Alibaba columns.  
  - Use for “what would be the next cost” for processing steps (e.g. beans → nibs → mass).  
  - **Sheet URL:** [Agroverse Cacao Processing Cost](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit?gid=603759787#gid=603759787).

### 4.2 Updating Agroverse Cacao Processing Cost from WhatsApp chat

Chat exports (e.g. **Downloads > WhatsApp Chat - Agroverse cacao production.zip**) can be parsed to extract facility, process, cost, currency, and date for new rows:

1. **Extract:** Run `tokenomics/python_scripts/agroverse_cacao_processing/extract_whatsapp_to_processing_cost.py` with the zip or `_chat.txt` path. It parses WhatsApp format `[date] Sender: message`, finds R$ amounts and facility names (Martinus, Santos, Fazenda Capela Velha, etc.), and outputs CSV in the sheet column order.
2. **Review:** Open the CSV; fix Facility/Process names, remove duplicates, add Contact/WhatsApp if known.
3. **Update sheet:** Either paste the new rows below existing data in [Agroverse Cacao Processing Cost](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit?gid=603759787#gid=603759787) (columns A–G), or use Google Sheets API to append (see tokenomics script README). **Exact insert steps, column order, and where to paste:** tokenomics `python_scripts/agroverse_cacao_processing/INSERT_PROCEDURE.md`.

Details: **tokenomics** repo `python_scripts/agroverse_cacao_processing/README.md`.

### 4.3 “How many units of cacao beans convert to what and what would be the next cost?”

- **Conversion / product mix:**  
  - Product and category definitions: **Currencies**, **Agroverse SKUs**, **Agroverse Cacao Category Pricing**.  
  - Conversion ratios (e.g. beans → nibs → mass) may be in business rules, scripts, or the same sheets; if not in SCHEMA, infer from Currencies/Agroverse Cacao Processing Cost or ask.

- **Next cost:**  
  - **Agroverse Cacao Processing Cost:** cost per facility/process (and currency).  
  - **Agroverse Price Components** and **Agroverse Cacao Category Pricing:** apply to get unit or category-level cost.  
  - **offchain asset location** Unit Cost / Total Value for existing inventory at a location.

---

## 5. Use-case summary

| Prompt | Where to look | Action |
|--------|----------------|--------|
| “How many units of X, Y, Z in Brazil in Matheus warehouse?” | offchain asset location (Location B = Matheus warehouse); AGL Balance sheets if used | Filter by Location and Currency; sum Amount Managed (and AGL quantities). |
| “Options for freighting these to Kirsten warehouse in San Francisco” | tdg_shipping_planner | **Matheus (Ilhéus, Brazil) → Kirsten (San Francisco):** always freight—use getFreightCost(weight_kg, cargo_value, options) and document line items. (For US→US only, use EasyPost/USPS.) |
| “How many units of cacao beans convert to what and what would be the next cost?” | SCHEMA.md + Agroverse Cacao Processing Cost, Agroverse Cacao Category Pricing, Agroverse Price Components, Currencies | Map beans → products from Currencies/SKUs/category pricing; use Processing Cost + Price Components + Category Pricing for “next cost.” |

---

## 6. Cross-references

- **Full schema (all sheets/columns):** `tokenomics/SCHEMA.md`  
- **API endpoints (inventory, shipping, etc.):** `tokenomics/API.md`  
- **Shipping Planner deployment and parameters:** `tokenomics/google_app_scripts/tdg_shipping_planner/README.md`  
- **Workspace overview:** This repo `WORKSPACE_CONTEXT.md` and `PROJECT_INDEX.md`  
- **GitHub (clone tokenomics):** https://github.com/TrueSightDAO/tokenomics — see WORKSPACE_CONTEXT.md §6 for all repo URLs.

*When you add or change sheets or cost logic, update tokenomics SCHEMA.md and, if needed, this document.*
