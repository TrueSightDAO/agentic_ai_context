# Proposal: Optimal Number of Bags of Ceremonial Cacao to Ship to a Partner on Consignment

## 1. Where Shipping Cost (San Francisco → Various Locations) Is Calculated

Shipping cost from **San Francisco** to various locations is implemented in two places:

### 1.1 Shipping Planner API (tokenomics)

- **Location:** `tokenomics/google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`
- **Origin:** San Francisco (configurable via Script Properties; default `1423 Hayes St`, `94117`, CA).
- **Capabilities:**
  - **Local (US) shipping:** EasyPost API → USPS rates from SF to any US destination address (weight + origin + destination).
  - **Freight:** Cost from a Google Sheet (ID `10Ps8BYcTa3sIqtoLwlQ13upuxIG_DgJIpfzchLjm9og`), weight tiers 200–1000 kg, with full breakdown (air freight, export doc, Brazil inland, airport charges, US terminal/handling/customs, FDA, bond, MPF, etc.).
- **Weight:** Product weights from main spreadsheet “Currencies” sheet (Column K grams / L ounces); box (base 11.5 oz) or pallet (35 kg).
- **API:** `list_managers`, `get_inventory`, `calculate_shipping` (POST body: `selected_items`, `packaging_type`, `shipping_type`, `destination_address`).
- **Deployment URL:** See `tokenomics/google_app_scripts/tdg_shipping_planner/README.md`.

### 1.2 Agroverse Shop Checkout (agroverse_shop)

- **Location:** `agroverse_shop/google-app-script/agroverse_shop_checkout.gs` (and doc `agroverse_shop/docs/archive/SHIPPING_COSTS.md`).
- **Origin:** Warehouse/store address (configurable: `ORIGIN_ADDRESS_*`).
- **Capability:** EasyPost → USPS rates for checkout (package weight from cart + base box + per-item packaging).
- **Use case:** Per-order checkout shipping, not bulk consignment planning.

### 1.3 Partner locations (for destination input)

- **Location:** `agroverse_shop/partner_locations.json`.
- **Content:** Partner keys, display names, and **location strings** (e.g. `"Santa Cruz, California"`, `"Dayton, Ohio"`, `"Denver, Colorado"`, `"Portland, Oregon"`, international e.g. Brazil, Switzerland).
- **Use:** Can drive “destination” for the Shipping Planner (once geocoded to a full address or ZIP for EasyPost).

**Conclusion:** The **Shipping Planner API** is the right place to plug in “cost to ship N bags of ceremonial cacao from SF to partner location.” Use EasyPost for domestic US partners; use the freight sheet for international or very large consignments.

---

## 2. Consignment Context

- **Consignment:** You ship product to a partner; they pay (or share revenue) when they sell it. Unsold units may be returned or written off.
- **Goal:** Choose **how many bags to send** so that expected margin (or another objective) is best, given:
  - Shipping cost (increasing with quantity, but not linear per bag due to tiering),
  - Holding/opportunity cost at partner,
  - Sell-through rate,
  - Consignment terms (e.g. rev share, minimum commitment),
  - Product and shipping cost structure.

---

## 3. Proposal: Framework for Optimal Consignment Quantity

### 3.1 Inputs to Collect (per partner, per product)

| Input | Description | Source / note |
|-------|-------------|----------------|
| **Partner location** | Full address or at least city, state, ZIP (US) for EasyPost | `partner_locations.json` + geocoding or manual fill |
| **Product** | e.g. “Ceremonial Cacao 200g” (or SKU) | Currencies sheet / products config |
| **Weight per bag** | Ounces or grams | Currencies sheet (Column K or L) |
| **Wholesale/consignment price per bag** | Price you receive when partner sells | Internal pricing |
| **Your cost per bag** | COGS | Internal |
| **Sell-through rate** | Expected fraction of shipped units that sell (e.g. 0.7 in 90 days) | Historical by partner or default (e.g. 0.5–0.8) |
| **Consignment terms** | Rev share %, minimum order, return policy | Contract |
| **Planning horizon** | e.g. 90 days | Policy |

### 3.2 Shipping Cost from SF to Partner

- **Domestic US:** Call Shipping Planner API `calculate_shipping` with:
  - `shipping_type`: `"local"`
  - `packaging_type`: `"box"` (or `"pallet"` for large quantities)
  - `selected_items`: one item = ceremonial cacao, `quantity` = N bags, `weight_grams`/`weight_grams` from Currencies
  - `destination_address`: from partner (street, city, state, zip, country).
- **International or large bulk:** Use `shipping_type`: `"freight"` and same weight; API returns freight estimate from the existing freight sheet (SF/origin can be implied by your process).

So: **shipping_cost(N)** = result of one (or a few) API calls for N bags. Optionally cache by (partner_id, N) for a planning session.

### 3.3 Objective: Maximize Expected Contribution (or Minimize Cost per Expected Sale)

A simple formulation:

- **Revenue (expected):**  
  `E[revenue] = N * sell_through_rate * consignment_price_per_bag`
- **Costs:**  
  - Your COGS: `N * cost_per_bag`  
  - Shipping: `shipping_cost(N)` (from API)  
  - (Optional) Holding/opportunity cost: e.g. `(1 - sell_through_rate) * N * cost_per_bag * discount_factor`
- **Contribution:**  
  `contribution(N) = E[revenue] - N * cost_per_bag - shipping_cost(N) - optional_holding_cost`

**Optimal N:** Choose N that maximizes `contribution(N)` over a reasonable range (e.g. 1 to 50 or 100 bags, or up to a pallet).

- **Alternative:** Minimize “cost per expected sale”:  
  `[N * cost_per_bag + shipping_cost(N)] / (N * sell_through_rate)`  
  and then pick N above a minimum volume that is operationally acceptable.

### 3.4 Practical Algorithm (Step-by-Step)

1. **List partners** from `partner_locations.json` (and optionally from your CMS/sheet).
2. **Resolve address** for each partner (city/state/ZIP or full address). Store in a small “partner addresses” sheet or JSON (one row per partner: id, name, street, city, state, zip, country).
3. **For a given partner and product:**
   - Get weight per bag from Currencies (or products config).
   - Set consignment price, cost per bag, sell-through rate, terms.
4. **Loop over candidate quantities** (e.g. N = 6, 12, 24, 48, … or 1..50):
   - Call Shipping Planner `calculate_shipping` for that N (and packaging type).
   - Compute `shipping_cost(N)` from the response (e.g. cheapest USPS option for local, or freight total for freight).
   - Compute `contribution(N)` (and optionally cost per expected sale).
5. **Choose N** that maximizes contribution (or meets a “min margin” or “max cost per sale” rule).
6. **Optional:** Enforce min/max (e.g. min 6 bags, max 100) or step sizes (e.g. multiples of 6).

### 3.5 Where to Implement

- **Option A – Script (e.g. Python or Node):**  
  - Reads partners (and addresses), product weights, and pricing defaults.  
  - Calls Shipping Planner API for each (partner, N).  
  - Computes contribution; outputs recommended N per partner (and optionally a small report).
- **Option B – Google Apps Script:**  
  - New function in the tokenomics project (or agroverse_shop) that:  
    - Reads partner list and addresses from a sheet;  
    - Uses existing `calculateEasyPostRates` / `getFreightCost` internally (no external HTTP to yourself);  
    - Writes recommended N and shipping cost to a “Consignment planning” sheet.
- **Option C – Sheet-only:**  
  - “Consignment planner” sheet: columns Partner, Address, N (dropdown or list), Weight, Shipping Cost (formula or script that calls the API once per row).  
  - You manually or with a script sweep N and take the best.

Recommendation: **Option A** for clarity and testability; reuse the existing **Shipping Planner API** so all SF→destination logic stays in one place.

### 3.6 Data to Add (One-Time / Ongoing)

- **Partner addresses:** Extend `partner_locations.json` (or a Google Sheet) with full address or at least city, state, ZIP, country so EasyPost can rate it.
- **Product weight:** Ensure “Ceremonial Cacao” (and any SKU) has weight in the Currencies sheet (Column K or L) so the API returns correct shipping cost.
- **Sell-through and terms:** A small table (partner × product or default) for sell-through rate and consignment price; can live in a sheet or config.

---

## 4. Summary

- **Where shipping is calculated:**  
  **San Francisco → various locations** is implemented in the **Shipping Planner API** (`tokenomics/google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`), with origin SF (configurable), EasyPost for US domestic, and a freight Google Sheet for heavier/international. Agroverse shop checkout uses EasyPost from the same origin pattern for single orders.
- **Consignment optimal quantity:**  
  Use the Shipping Planner to get **shipping_cost(N)** from SF to each partner; then maximize **expected contribution** (or minimize cost per expected sale) over N, using sell-through rate, consignment price, and COGS. Implement as a small script or sheet that calls the existing API and optionally reads partner list from `partner_locations.json` and a partner-address store.

This keeps all “cost from SF to location” logic in the existing codebase and only adds a thin “consignment quantity” layer on top.
