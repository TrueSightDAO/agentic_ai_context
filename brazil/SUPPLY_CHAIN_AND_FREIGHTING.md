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

### 2.4 Warehouse floor map (Ilhéus)

Reference map for the **Matheus warehouse (Ilhéus, Brazil)**. Companion docs: **`ILHEUS_WAREHOUSE_MANAGEMENT.md`** (action register) and **`ILHEUS_WAREHOUSE_FLOOR_MAP.md`** (canonical transcription).

**Source:** whiteboard photograph, 2026-10-09 (thread 41062), transcribed verbatim. **Unaudited working reference** — the Main Ledger + **offchain asset location** (§2.1) remain authoritative for quantities. Photo: `images/ilheus_warehouse_whiteboard_20261009.jpg`.

```
MAP

[ Door ]                          [   Table   ]

  +---------------+--------------+--------------+
  | FUMIGATION    | Oscar.       |              |
  |    29th Sept  | 2026.        |   [BLANK]    |
  | Paulo         | AGL 16       |              |
  | Beans 2024.   | 108 kg       |              |
  | 263.58 kg.    |              |              |
  | AGL 8         |              |              |
  +---------------+--------------+--------------+
```

**Shelving (right column):** F5 packet · trolley · plastic bags · kraft pouch (nibs) · kraft pouch (caramel) · 6× 80-mesh nibs · **20× chocolate mold** · label maker · weighing machine · tape.

**Ledger cross-check:**

- `FUMIGATION · 29 Sept · Paulo Beans 2024 · 263.58 kg · AGL 8` — matches AGL8 ledger lines (note: the 2026-10-08/09 Matheus write-off touches AGL8).
- `Oscar 2026 · AGL 16 · 108 kg` — matches the 2026-10-07 load into AGL16.
- `20× chocolate mold` — reconciles with ledger holding `Chocolate Mold MHC-CL082` (Matheus = 21 units; ~20 shelved, one in use).

## 2.5 Measured dimensions register (Ilhéus)

Tape-measure dimensions captured **on site at the Ilhéus (Black King / Matheus Reis) warehouse** (thread **41062**, 2026-10-09/10) and resolved from the tape photos via vision models (**Gemini 3.8-flash + Grok 4.5** — tesseract OCR could not resolve the tape digits). **Working, unaudited measurements**; the Main Ledger stays authoritative for quantities.

**Provenance:** tape photos in the thread-41062 transcript (`truesight_autopilot_transcript`, session `6414080bc772`).

| # | Element | Dimension | Measured | Notes / confidence |
|---|---|---|---|---|
| M1 | Main window | width | **~53–54 cm** (≈21 in) | upper ~53 cm; lower ~53.5–54 cm; hook off-frame → ±1–2 cm |
| M2 | Main window | upper-pane clear height | **~14.5–15 cm** | louver/pane clear opening; attribution to re-confirm against the lower-pane reading |
| M3 | Main window | **lower-pane height** (vertical) | **~90 cm** (35 in) | **CORRECTED 2026-10-10:** this is the **lower pane**, **not** the full window; frame's full height still unmeasured |
| M4 | Toilet/bathroom window (louvered) | width | **53 cm** (21 in) | **governor-confirmed 2026-10-10** (Gary); matches M1 |
| M5 | Toilet/bathroom window (louvered) | **openable height** | **35 cm** (~14 in) | **governor-confirmed 2026-10-10** (Gary) — **supersedes** the ~39.5–40 cm tape reading, which likely spanned the **surrounding frame**, not just the openable sash |
| M6 | Plastic (HDPE) pallet | one edge | **~110–112 cm** (~44 in) | other edge, height, and qty still unmeasured |
| M7 | Warehouse wall span | wall length | **~4.30 m** | single span, one wall only (see A1) |

**Opening areas (for fixtures/fans):** toilet/bathroom window opening = 53 × 35 = **~1,855 cm²**; main window = 53–54 cm W × (upper ~15 + lower ~90) **≈ 5,500 cm²**. A 100 mm axial fan's 13.5 × 13.5 cm square plate (~182 cm²) therefore covers only **~10%** of the bathroom opening — a filler panel is required around it (see thread 41062 fan analysis).

**Reading rules / caveats:**

- Most shots are **close-ups**; the tape's hook/zero is **off-frame**, so each value is the reading where the tape meets the far frame — treat as **±1–2 cm**.
- Values are **vision-derived** (Gemini + Grok converged on every item); **not** OCR-verified.
- Emerging spec: **main window ≈ 53–54 cm W, lower pane ~90 cm H** (upper pane clear ~14.5–15 cm; **full frame height still unmeasured**); **louvered toilet/bathroom window = 53 cm W × 35 cm openable H** (governor-confirmed) — both share a ~53 cm sash module.
- Still open: warehouse **footprint** (L×W), **full wall heights**, the **main window's full frame height** (only the lower pane ~90 cm + upper pane ~15 cm are measured so far), and any **other openings/windows**.

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
