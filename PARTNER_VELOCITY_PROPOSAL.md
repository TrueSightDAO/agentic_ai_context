# Partner Velocity Proposal — `partners-velocity.json`

**Status:** Draft for review (Gary). Created 2026-04-27 in response to "can we compute average expected monthly cacao demand per store from historical ledger data?"

**Sibling docs:**
- **`RESTOCK_RECOMMENDER_ON_THE_FLY.md`** — the consumer of this JSON; describes a phone-friendly recommender that reads per-(partner, product) velocity to suggest "send N bags."
- **`CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md`** — earlier framework that treats `sell_through_rate` as an assumed input (0.5–0.8 default). This proposal replaces that assumption with measured velocity.
- **`SUPPLY_CHAIN_AND_FREIGHTING.md`** — documents the multi-ledger structure (Main Ledger + each AGL ledger linked from `Shipment Ledger Listing` column AB).
- **`NOTES_tokenomics.md`** — Main Ledger tab list (`Sales`, `Inventory Movement`, `off chain asset balance`, etc.).

---

## 1. The question

> "Based on historical sales across all ledgers associated with each retailer, can we determine the average expected amount of cacao per store per month?"

Yes. The data exists, the join chain exists, and the script that already produces `partners-inventory.json` (current snapshot) covers most of the plumbing. What's missing is the aggregation over a time window and a few nuances that affect accuracy.

---

## 2. The join chain (verified against existing code)

Confirmed from **`market_research/scripts/sync_agroverse_store_inventory.py`**:

1. **Partner key** in `agroverse-inventory/partners-inventory.json` (e.g. `edge-and-node-house-of-web3`)
2. → **`Agroverse Partners`** tab on Main Ledger (`1GE7PUq-…`), column **A** = `partner_id`
3. → same row's column **E** = `contributor_contact_id` (the store-manager / location name)
4. → that name appears in **`Contributors contact information`** with column **T** flagging it as a store manager
5. → that same name is the **Manager** / **Location** field on:
   - Main Ledger `off chain asset balance` (current stock)
   - Main Ledger `Sales` (sell-through events)
   - Main Ledger `Inventory Movement` (transfers TO the store)
   - **Per-AGL managed ledgers** linked from **`Shipment Ledger Listing`** column **AB** — each has its own `Sales` and `Balance` sheets that need to be summed

The existing inventory snapshot script already iterates every managed ledger from `Shipment Ledger Listing` AB. A velocity script clones that iteration; the only swap is what it reads inside each ledger.

---

## 3. The two velocities (don't conflate them)

For any (partner, product), there are two distinct rates that mean different things:

### 3a. Sales-record velocity (sell-through)

- **Source:** `Sales` rows on Main Ledger and per-AGL ledgers, filtered by recipient/store-manager = the partner's contributor name.
- **What it measures:** how fast the store sells to end customers.
- **Trustworthy when:** the partner is on **consignment** — we still own the inventory, so the store reports sales back to us via `[SALES EVENT]` Telegram logs (processed by `tokenomics/google_app_scripts/tdg_inventory_management/process_sales_telegram_logs.gs`).
- **Unreliable when:** the partner is on **wholesale-bought-outright** — they never report sales to us; we only see what they reorder.

### 3b. Inventory-movement velocity (restock cadence)

- **Source:** `Inventory Movement` rows where the *recipient* / destination = the partner's manager name.
- **What it measures:** how often we ship to them, which is a lagged proxy for sell-through.
- **Trustworthy when:** every partner type — restocks happen for both consignment and wholesale-bought.
- **Caveat:** lagged — restock cadence reflects sell-through *plus* the partner's stock-on-hand decisions and our shipment batching.

**Recommendation:** the JSON should carry **both** fields per (partner, product). Consumers pick the right one based on the partner's path:

```json
{
  "edge-and-node-house-of-web3": {
    "8-ounce-organic-cacao-nibs": {
      "sales_30d": 3,
      "sales_90d": 12,
      "sales_12m_monthly_avg": 4.2,
      "restocks_90d_units": 10,
      "restocks_12m_monthly_avg_units": 3.8,
      "last_sale_date": "2026-04-15",
      "last_restock_date": "2026-04-02",
      "sample_size_sales": 27,
      "sample_size_restocks": 6,
      "partner_type": "consignment"
    }
  }
}
```

The `partner_type` field comes from **`Agroverse Partners`** sheet (need to confirm a column exists for this; if not, add one). Consumer logic:

- `partner_type = consignment` → trust `sales_*` for velocity.
- `partner_type = wholesale-bought` → use `restocks_*` (sales rows for them are sparse / non-canonical).
- `sample_size < N` → flag low confidence; fall back to category default.

---

## 4. Output: `agroverse-inventory/partners-velocity.json`

Sibling to `partners-inventory.json` in the **`agroverse-inventory`** repo. Same generation pattern: a Python script run on a schedule (or via GAS webhook) that reads Main Ledger + every AGL ledger, aggregates, and commits the JSON to GitHub for downstream consumers.

**Generation cadence:** weekly (sales velocity changes slowly; daily is overkill and burns ledger reads). Restock cadence is similarly slow.

**Time windows to emit per (partner, product):**
- `sales_30d` (units in last 30 days)
- `sales_90d` (units in last 90 days)
- `sales_12m_monthly_avg` (units per month over last 365 days, for partners with ≥ 12 months of history)
- Same three for `restocks_*`
- `last_sale_date`, `last_restock_date` (so consumers can flag dormant partners)
- `sample_size_sales`, `sample_size_restocks` (count of contributing rows — confidence signal)

---

## 5. Consumer 1: Restock Recommender (`RESTOCK_RECOMMENDER_ON_THE_FLY.md`)

Per that proposal, the recommender wants **one number** per (partner, product) — "units per month." With `partners-velocity.json`:

```
let v = velocity[partner_key][product_id];
let monthly_rate = v.partner_type === "consignment"
  ? v.sales_12m_monthly_avg ?? v.sales_90d / 3
  : v.restocks_12m_monthly_avg_units ?? v.restocks_90d_units / 3;

if (v.sample_size_sales < 6 && v.sample_size_restocks < 3) {
  // low confidence — fall back to category default
}
```

Then it computes "weeks of stock at rate" exactly as the existing `RESTOCK_RECOMMENDER_ON_THE_FLY.md` describes.

---

## 6. Consumer 2: Wholesale conversation / outreach prioritization

Velocity data lets the warm-up draft generator (`market_research/scripts/suggest_warmup_prospect_drafts.py`) and the manager-follow-up generator make smarter calls:

- **Dormant retailer** (`last_sale_date > 90 days ago`) → trigger a check-in email instead of a generic warmup.
- **High-velocity retailer** (`sales_90d / 3 > category median`) → flag as a candidate for case-study / testimonial / shelf-photo capture for `/wholesale/`.
- **Newly-onboarded retailer** (`sample_size < 3`) → no recommendation; default to category baseline.

---

## 7. Caveats and known unknowns

- **Sample size is unevenly distributed.** Long-tenured stores (Go Ask Alice, Kiki's, Lumin Earth, Edge & Node) have ≥ 12 months of data. Most of the 27 USA stockists are tail with < 6 months.
- **Seasonality breaks flat averages** for pop-up vendors (Raye Workz, Llama Bus, Okanogan Family Barter Faire) and Q4-heavy retailers. A 12-month average is more honest than a 30-day for those, *but* the JSON should expose both so the consumer can pick.
- **Cold-start.** Partners with zero history → recommender falls back to a category default (e.g. "median monthly velocity for ceremonial cacao among 12-month+ partners").
- **Restock ≠ sell-through.** Documented in §3 — caller must use the right field.
- **Partner-type field may not exist yet.** If `Agroverse Partners` has no column distinguishing consignment vs wholesale-bought, the script either has to infer it (presence of sales rows = consignment) or we need to add it.
- **Timezone / date parsing.** Sales rows use Pacific time on the Main Ledger; per-AGL ledgers may differ. Normalize to UTC during aggregation.
- **Refunds / returns.** If a sale row is a refund (negative quantity or reversal), it should net out, not double-count.
- **Multiple managers per partner.** A few partners are run by two contributors (rare but exists); the script must `OR` across all `contributor_contact_id` values listed in the `Agroverse Partners` row.

---

## 8. Implementation (proposed)

### Step 1 — Aggregation script

**Path:** `market_research/scripts/sync_partners_velocity.py` (sibling to `sync_agroverse_store_inventory.py`).

Reuses these helpers from the existing inventory script:
- `get_store_managers(sh)` — Contributors col T flag
- `read_partners_by_contributor(sh)` — `Agroverse Partners` col A ↔ col E
- `Shipment Ledger Listing` AB iteration

Adds:
- `aggregate_sales_for_managers(sh, managers, *, windows=(30, 90, 365))` — reads Main Ledger `Sales` tab, filters by recipient/manager, buckets by window.
- `aggregate_movements_for_managers(sh, managers, *, windows=(30, 90, 365))` — same shape from `Inventory Movement`.
- For each managed AGL ledger from `Shipment Ledger Listing` AB: open it, read its `Sales` and `Inventory Movement` sheets, aggregate, sum into the same totals.
- Emit `partners-velocity.json` to `~/Applications/agroverse-inventory/partners-velocity.json`.

### Step 2 — Schedule + commit

Run weekly via the same mechanism that updates `partners-inventory.json` (likely a CI workflow in `agroverse-inventory` calling out to the market_research script with credentials, or a manual invocation pinned to Monday).

### Step 3 — Consumers

- Update `RESTOCK_RECOMMENDER_ON_THE_FLY.md` to point at `partners-velocity.json` as the canonical velocity source (replaces "add a Partner sales sheet" Option A).
- Update `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` §3.1 to source `sell_through_rate` from `partners-velocity.json` instead of the 0.5–0.8 default.
- (Future) Restock Recommender web page reads the JSON; ships in a follow-up PR.

---

## 9. Open questions for Gary

1. **Partner-type field.** Does `Agroverse Partners` already have a column distinguishing consignment vs wholesale-bought? If not, OK to add one and backfill?
2. **Refresh cadence.** Weekly OK, or do you want daily?
3. **Where the aggregation runs.** Python script invoked from your machine on a schedule (same as inventory sync today), or move it to GAS so it runs server-side without local credentials?
4. **Cold-start default.** What's a reasonable category-median fallback for ceremonial-cacao monthly velocity? (Suggest: pull from existing 12-month+ partners and use their median; recompute every refresh.)
5. **Surface in the wholesale conversation?** Should the dormant-retailer / high-velocity retailer signal feed back into the warm-up draft generator now, or wait until velocity numbers settle in?

---

## 10. What this proposal is *not*

- Not the Restock Recommender UI itself — that's a separate proposal (`RESTOCK_RECOMMENDER_ON_THE_FLY.md`); this one just produces the data it needs.
- Not a replacement for `partners-inventory.json` — the two are complementary (current stock + historical rate).
- Not a forecasting model — flat moving averages with explicit sample-size + last-active flags. ARIMA / exponential smoothing can come later if the simple version proves valuable.
- Not a CRM — partner relationship state still lives in the Hit List / DApp Remarks workflow.
