# Restock Recommender — On the Fly (When a Partner Texts)

**Goal:** When you’re out and get a text from a partner asking to restock, get the **optimal number of bags** in seconds from your phone — using **shipping cost from Kirsten’s (SF)** and **their prior sales** so you don’t over-send and tie up capital.

---

## 1. Best Way to Get the Number On the Fly

**Recommended: single mobile-friendly Restock Recommender page** (one URL, open on your phone, 3 taps).

| Option | Pros | Cons |
|--------|-----|------|
| **Restock Recommender web page** (new page in dapp or standalone) | Works in browser, no install; can save to home screen (PWA); reuses Shipping Planner API; fast | Needs one new HTML page + one new API action |
| **Google Sheet “Restock” tab** | No deploy; you already use Sheets; works on phone | Slower to open; button runs script (may need auth); less polished |
| **SMS/WhatsApp bot** | Reply in-thread | Needs backend + messaging setup; more work |
| **Pre-computed table (e.g. weekly email)** | No device needed when text arrives | Stale if sales or rates change; no “right now” shipping quote |

**Recommendation:** Add a **Restock Recommender** page that:

1. You open from your phone (bookmark or home screen).
2. You select the **partner** (dropdown or search — matches who just texted).
3. Optionally select **product** (default: Ceremonial Cacao 200g).
4. Tap **“Get recommendation”**.
5. You see: **“Send 24 bags. Shipping ~$11. That’s ~6 weeks of stock at their current rate.”** plus a short reply suggestion you can copy-paste into the text.

Total time: **under 30 seconds** so you can reply to the partner immediately.

---

## 2. Using Prior Sales Data (Ledger)

You already have **prior sales in the ledger**. To use it for “on the fly”:

- **Option A – Dedicated “Partner sales” sheet (recommended for speed)**  
  - In the main spreadsheet (or a linked one), add a sheet **“Partner sales”** (or **“Partner velocity”**).  
  - Columns: **Partner** (name or key matching `partner_locations`), **Product** (e.g. Ceremonial Cacao 200g), **Units sold (last 90 days)** or **Monthly average**.  
  - Populate from your existing ledger/sales data (manual update, or a script that aggregates from ledger/sales reports).  
  - The Restock API reads this sheet to get “units per month” (or per 90 days) for that partner + product.

- **Option B – Derive from existing ledger(s)**  
  - If sales are already in a sheet (e.g. “Sales” or “report_sales” output), the API can sum by partner + product for the last 90 days and compute rate.  
  - If sales are only in ledger *movements* (e.g. outflows from “offchain asset location” or shipment ledgers), add a small script or formula that aggregates “sold by partner” into a single table the API can read.

**For the recommender:** We only need **one number per (partner, product)**: e.g. **“units sold per month”** or **“units in last 90 days”**. The API then uses it to compute “weeks of stock” for a given N.

---

## 3. What We Optimize For

- **Shipping cost from Kirsten’s (SF):** Use the existing **Shipping Planner API** (origin = Kirsten’s address in SF) to get USPS cost for N bags to the partner’s address. Prefer **fewer, larger shipments** to lower cost per bag.
- **Don’t send too much:** Use **prior sales** to estimate “weeks of stock” for a given N. Cap N so you don’t deploy more capital than you want (e.g. **max 8–12 weeks of stock** at their current rate).

**Simple rule:**

- **Target:** Send enough for **about 4–8 weeks** of stock at their recent sales rate (configurable).
- **Constraint:** Don’t exceed **max weeks of stock** (e.g. 12) so inventory at partner doesn’t tie up too much capital.
- **Discrete options:** Only recommend **sensible N** (e.g. 6, 12, 18, 24, 36, 48 bags) so it’s easy to pack and communicate.

**Formula (conceptually):**

- `weeks_of_stock(N) = N / (partner_monthly_sales_rate * (4.33 weeks/month))`  
  (or use “last 90 days” and divide by 13 for weeks).
- **Ideal N:** Smallest N in your list such that `weeks_of_stock(N)` is in the target range (e.g. 4–8), and `weeks_of_stock(N) ≤ max_weeks` (e.g. 12).
- If their rate is **zero** (new partner), fall back to a **default N** (e.g. 12 or 24) and show “No prior sales; default recommendation.”

---

## 4. Data Needed

| Data | Where it lives / where to add it |
|------|----------------------------------|
| **Partner list** | Already in `agroverse_shop/partner_locations.json` (and can be synced to a sheet). |
| **Partner address** | Add a **“Partner addresses”** sheet (or extend partner_locations): one row per partner with **street, city, state, zip, country** so EasyPost can rate SF → partner. |
| **Product weight** | Already in main spreadsheet **Currencies** (Column K or L) for Ceremonial Cacao. |
| **Partner sales rate** | New **“Partner sales”** (or “Partner velocity”) sheet: Partner, Product, Units (e.g. last 90 days) or Monthly average; filled from ledger/sales. |
| **Origin (Kirsten’s)** | Already in Shipping Planner Script Properties (SF address). Ensure it’s set to Kirsten’s place. |

---

## 5. Implementation Outline

### 5.1 New API action: `restock_recommend`

Add to **Shipping Planner API** (or a sibling Apps Script that reuses the same functions):

- **Input:** `partner_id` or `partner_name`, optional `product` (default Ceremonial Cacao).
- **Steps:**
  1. Resolve partner to **full address** (from Partner addresses sheet).
  2. Get **product weight** from Currencies (Column K or L).
  3. Get **partner sales rate** for that product from Partner sales sheet (units per month or last 90 days).
  4. For each **N** in [6, 12, 18, 24, 36, 48] (or a configurable list):
     - Call existing `calculateEasyPostRates(weightOz_for_N_bags, partner_address)` (or the same logic that `calculate_shipping` uses).
     - Compute `weeks_of_stock(N) = N / (monthly_rate * 4.33)` (or equivalent).
     - Store `{ N, shipping_cost, weeks_of_stock, shipping_per_bag }`.
  5. Apply rule: choose **N** where `weeks_of_stock` is in target range (e.g. 4–8) and ≤ max (e.g. 12); if multiple, pick one that minimizes **shipping per bag** (or total cost).
  6. If no N fits (e.g. very high rate), cap at max weeks; if rate is 0, return default N.
- **Output:** `{ recommended_N, shipping_cost_usd, weeks_of_stock, partner_name, product, optional_alternatives: [{ N, shipping_cost_usd, weeks_of_stock }] }`.

### 5.2 Restock Recommender page (HTML)

- **URL:** e.g. `https://truesightdao.github.io/dapp/restock_recommender.html` (or same origin as shipping_planner).
- **Layout (mobile-first):**
  - Dropdown or typeahead: **Partner** (load from API or static list from partner_locations).
  - Dropdown: **Product** (default “Ceremonial Cacao 200g”; optional).
  - Button: **“Get recommendation”**.
  - Result: **“Send **24** bags. Shipping ~$11. That’s ~6 weeks of stock at their rate.”**  
    Optional: “Alternative: 18 bags (~4.5 weeks), shipping ~$10.”  
    Optional: Short reply text: “I’ll send 24 bags; should arrive by [date]. I’ll send tracking.”
- **Flow:** Page calls `restock_recommend?partner_id=go-ask-alice&product=...`; displays result. No login if the API is open; or use a simple token if you want to restrict access.

### 5.3 Optional: Google Sheet “Restock” tab

- Columns: **Partner** (dropdown), **Product** (dropdown), **Get recommendation** (button), **Recommended N**, **Shipping $**, **Weeks of stock**, **Reply text**.
- Button runs Apps Script that calls the same `restock_recommend` logic (or the API), then writes back Recommended N, Shipping $, Weeks of stock and a suggested reply into the row.

---

## 6. Quick Start (Minimal Path)

1. **Partner addresses:** In the **main spreadsheet** (same as Shipping Planner, ID `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`), add a sheet named **“Partner addresses”** with columns: **A** = partner_id (e.g. `go-ask-alice`), **B** = street1, **C** = city, **D** = state, **E** = zip, **F** = country. Fill one row per partner that can restock (use same keys as `agroverse_shop/partner_locations.json`).
2. **Partner sales (optional):** Add a sheet **“Partner sales”** with columns: **A** = partner_id, **B** = product name (e.g. Ceremonial Cacao 200g), **C** = units last 90 days. If missing, the API uses a default rate (4 units/month). Populate from your ledger/sales data.
3. **Script Properties:** Ensure Shipping Planner origin = Kirsten’s SF address (ORIGIN_ADDRESS_* in Script Properties).
4. **API:** The Shipping Planner Apps Script now has action **`restock_recommend`**. Redeploy the web app after pulling the latest `shipping_planner_api.gs`.
5. **Restock page:** Open **Restock Recommender** from the dapp: `https://truesightdao.github.io/dapp/restock_recommender.html` (or your deployment). Select partner → tap “Get recommendation” → see “Send X bags. Shipping ~$Y. That’s Z weeks of stock.”
6. **Bookmark** the Restock Recommender URL on your phone (or “Add to Home Screen”). When a partner texts, open link → select partner → tap “Get recommendation” → reply with the number.

---

## 7. Summary

- **Best way on the fly:** One **Restock Recommender** web page (mobile-friendly), bookmarked on your phone: select partner (and optionally product) → tap “Get recommendation” → see **optimal N**, **shipping cost from Kirsten’s (SF)**, and **weeks of stock** from their prior sales.
- **Prior sales:** Use a **“Partner sales”** (or “Partner velocity”) sheet populated from your ledger; API reads it to get units per month (or last 90 days) per partner + product.
- **Optimization:** Minimize shipping cost per bag by preferring fewer, larger shipments, while **capping weeks of stock** (e.g. max 8–12 weeks) so you don’t deploy too much capital in partner inventory.

This keeps all shipping logic in the existing Shipping Planner (Kirsten’s SF origin) and adds a thin “restock recommend” layer that uses ledger-based sales and your target weeks-of-stock rule.
