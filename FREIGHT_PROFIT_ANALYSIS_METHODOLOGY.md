# Freight Profit Analysis — Standard Methodology

**Purpose:** This document defines the standard methodology for analyzing a shipping manifest for profit and loss purposes. All future incarnations of the TrueSight DAO Autopilot and any other LLM performing freight analysis MUST follow this methodology to ensure consistency.

**Author:** Governor Gary Teh
**Last updated:** 2026-06-11

---

## 1. Core Principle

A freight profit analysis answers one question: **"What is the expected return on this shipment across different sales channels?"** It is not a forecast — it is a structured breakdown of revenue potential, costs, and margins that enables decision-making about pricing, channel strategy, and capital deployment.

---

## 2. Data Sources

Before beginning any analysis, gather the following:

| Data | Source |
|------|--------|
| Shipping manifest (line items, weights, quantities) | AORA_EXPERIENCE_PLAN.md or the freight plan document |
| Freight cost breakdown | Email threads with freight broker (Graziela@5cl.rs) + freight audit repo (agroverse-freight-audit) |
| Cacao cost basis (COGS) | Treasury cache (treasury-cache/dao_offchain_treasury.json) — look up each item's unit_cost_usd by ledger |
| Retail prices | agroverse.shop/js/products.js for live shop prices |
| Wholesale prices | Governor's stated pricing (ask if not provided) |
| Packaging material costs | Treasury cache (packaging materials listed as inventory items) |
| Cash position | Treasury cache + AORA_EXPERIENCE_PLAN.md cash section |

---

## 3. Pricing Structure

### 3.1. Ask the Governor First

Always ask the governor for their pricing before assuming. The governor has stated the following pricing structure (as of 2026-06-11):

| Product | Unit Size | Retail Price | Wholesale Price |
|---------|-----------|-------------|----------------|
| Ceremonial Cacao Pouch | 200g (7.05 oz) | $25.00 | $17.00 |
| Cacao Nibs Kraft Pouch | 8 oz (227g) | $25.00 | $17.00 |
| Cacao Mass Bar (500g) | 500g | $50.00 | $34.00 |
| Cacao Nibs (bulk, repacked) | 227g pouch | $25.00 | $17.00 |
| Cacao Almonds (bulk, repacked) | 200g pouch | $25.00 | $17.00 |
| Chocolate Bar (50g) | 50g | $10.00 | $6.00 |
| Cacao Husk / Tea (to apothecaries) | Per lb | $20.00/lb | $20.00/lb (fixed) |

**Rule:** If the governor has not stated pricing for a product, use the live shop price from products.js as the retail price, and assume wholesale is 68% of retail (the $17/$25 ratio). Always note the assumption.

### 3.2. Special Channels

Some items go to specific buyers at fixed prices (e.g., apothecaries at $20/lb for husk and tea). These are NOT discounted at wholesale — they have a single fixed price. Identify these from the governor's instructions.

---

## 4. Revenue Calculation

### 4.1. Per-Item Revenue

For each line item in the manifest:

1. **Identify the product type** (ceremonial pouch, nibs pouch, bulk nibs, mass bar, etc.)
2. **Determine the sellable unit size** — bulk items (KG) must be repacked into retail-sized units:
   - Cacao Nibs (KG): 1 kg = 4.4 × 227g pouches
   - Cacao Almonds (KG): 1 kg = 5 × 200g pouches
   - Cacao Husk / Tea (KG): 1 kg = 2.2046 lbs (sell by the lb to apothecaries)
3. **Calculate revenue at retail:** Qty × Retail Price
4. **Calculate revenue at wholesale:** Qty × Wholesale Price
5. **For fixed-price channels:** Qty × Fixed Price (no retail/wholesale split)

### 4.2. Revenue Scenarios

Always calculate three revenue scenarios:

| Scenario | Description |
|----------|-------------|
| **All Retail** | Every item sold at retail price |
| **All Wholesale** | Every item sold at wholesale price (except fixed-price channels) |
| **Mixed (30/70)** | 30% of retail-value items sell at retail, 70% at wholesale. Fixed-price channels always at their fixed price. |

**Rule:** The Mixed scenario is the most realistic and should be treated as the "expected" case.

---

## 5. Freight Cost

### 5.1. Current Cost

Extract the freight cost breakdown from the freight audit repo or email threads. Typical components:

| Component | Source |
|-----------|--------|
| Air Freight (airport to airport) | Per-kg rate from broker quote × total weight |
| Export Documentation | Per-shipment fee |
| Inland Transport (Brazil) | $695 + 0.15% ad valorem (or updated quote) |
| Brazil Airport Charges | Max($0.30/kg, $250 minimum) |
| US Airline Terminal Fee | Per-shipment (varies by airline) |
| US Import Handling Fee | Per-shipment |
| US Customs Clearance | Per-shipment |
| MPF (Merchandise Processing Fee) | 0.3464% of cargo value, min $33.58, max $651.50 |

### 5.2. Potential Increases

Always note risks that could increase freight cost:
- **Inland transport increase** — Isis from Omega quoted R$7,290 (vs original $695) on 28 May 2026
- **Pallet + fumigation** — New cost of BRL 695 (~$139)
- **War risk surcharge** — Iran/USA conflict driving up air freight rates (amount TBD)

Include a **Worst Case** scenario that uses the highest known estimates.

### 5.3. Freight Metrics

Always calculate:
- Freight cost per kg shipped
- Freight cost as % of retail value
- Freight cost per item

---

## 6. Cost of Goods Sold (COGS)

### 6.1. Cacao Cost Basis

Look up each item's unit cost from the treasury cache (`dao_offchain_treasury.json`):

1. Find the item in the `items[]` array by matching currency name
2. Use `unit_cost_usd` as the per-unit cost
3. Multiply by quantity to get total COGS for that item
4. If an item has no cost basis (unit_cost_usd = null or 0), note it as $0

### 6.2. Packaging Costs

For bulk items that need repacking, calculate packaging costs:

1. Count how many retail pouches each bulk item will produce
2. Look up pouch cost from treasury cache (e.g., "Cacao Nibs Kraft Pouch - V2" at $0.70 each)
3. Add label costs (Sticker Mule labels at $0.55 each)
4. Add shipping box costs

### 6.3. Total COGS

Total COGS = Cacao Cost Basis + Packaging Materials

---

## 7. Profit & Loss Statements

For each scenario, produce a full P&L:

| Line | Description |
|------|-------------|
| **Revenue** | From Section 4 |
| Less: Freight Cost | From Section 5 |
| Less: Cacao COGS | From Section 6.1 |
| Less: Packaging Materials | From Section 6.2 |
| Less: Payment Processing | ~3% of revenue (Stripe: 2.9% + $0.30) |
| Less: Platform Fees | ~$100 (shopify/domain) |
| **Gross Profit** | Revenue minus all costs |
| **Gross Margin** | Gross Profit ÷ Revenue |
| **Return on Freight Investment** | Gross Profit ÷ Freight Cost |

Always include these four scenarios:
1. **All Retail**
2. **All Wholesale**
3. **Mixed (30/70)** — the expected case
4. **Worst Case** — increased freight + wholesale pricing

---

## 8. Unit Economics

### 8.1. Per-Kilogram

| Metric | Formula |
|--------|---------|
| Revenue per kg | Total Revenue ÷ Total Weight (375 kg) |
| Freight cost per kg | Total Freight ÷ Total Weight |
| COGS per kg | Total COGS ÷ Total Weight |
| Profit per kg | (Revenue - Freight - COGS) ÷ Total Weight |

### 8.2. Per-Item

| Metric | Formula |
|--------|---------|
| Avg revenue per item | Total Revenue ÷ Total Sellable Units |
| Avg cost per item | (Freight + COGS) ÷ Total Sellable Units |
| Avg profit per item | (Revenue - Freight - COGS) ÷ Total Sellable Units |

### 8.3. Break-Even

| Metric | Formula |
|--------|---------|
| Break-even revenue | Freight + COGS + Packaging + Fees |
| Break-even as % of retail value | Break-even Revenue ÷ Total Retail Value |
| Units to break even (retail) | Break-even Revenue ÷ Avg Retail Price |
| Units to break even (wholesale) | Break-even Revenue ÷ Avg Wholesale Price |

---

## 9. Cash Flow & Capital Position

### 9.1. Available Cash

From the treasury cache, sum the ledgers the governor controls (typically Main Ledger + AGL15). Subtract the freight cost to get remaining cash.

### 9.2. Cash Required

List all costs that must be paid in cash:
- Freight (already allocated)
- Packaging materials
- Production labor (e.g., Kirsten's bar production ~$200)

### 9.3. ROI on Cash Deployed

| Metric | Formula |
|--------|---------|
| Cash-on-cash return | Expected Profit ÷ Total Cash Deployed |
| Net profit on cash | Expected Profit - Total Cash Deployed |

---

## 10. Risk & Sensitivity

### 10.1. Risk Factors Table

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Air freight rate increase | +$200–$500 | Medium | Lock rate ASAP |
| Inland transport increase | +$760 | High | Already quoted |
| Customs exam fee | +$250–$500 | Low | Proper docs |
| Damage/loss in transit | Full loss | Very Low | Insurance |
| Slow sell-through | Delayed ROI | Medium | Wholesale channels |
| Production delay | Delayed bars | Medium | Parallel production |

### 10.2. Sensitivity Table

Show profit at different sell-through rates (25%, 50%, 75%, 100%) for the Mixed scenario.

### 10.3. Time to Profitability

Estimate months to break even based on current retail run rate (~$1,000/month). Note that a wholesale bulk sale makes this immediate.

---

## 11. Summary Table

End with a summary table showing all scenarios side by side:

| Scenario | Revenue | Total Costs | Net Profit | Margin | ROI |
|----------|---------|-------------|------------|--------|-----|
| All Retail | $X | $X | $X | X% | X× |
| All Wholesale | $X | $X | $X | X% | X× |
| Mixed (30/70) | $X | $X | $X | X% | X× |
| Worst Case | $X | $X | $X | X% | X× |
| Aora 100 bars | $X | $X | $X | X% | X× |
| La do Sitio (2K bars) | $X | $X | $X | X% | X× |

---

## 12. Output Format

### 12.1. Verbal Summary

Provide a concise spoken summary (for Telegram voice) covering:
- The pricing structure used
- The top-line numbers for each scenario
- What changed from the previous version (if applicable)
- Key takeaways (3-5 bullet points)

### 12.2. PDF Report

Generate a full PDF report using `generate_pdf()` with these sections:
1. Payload & Pricing
2. Freight Cost
3. Cost of Goods Sold
4. Revenue Scenarios
5. Profit & Loss Statements
6. Unit Economics
7. La do Sitio Full Conversion (future potential)
8. Cash Flow & Capital Position
9. Risk & Sensitivity
10. Summary

Upload the PDF to `agentic_ai_context/reports/` with a versioned filename (e.g., `freight_profit_analysis_2026-06-11_v4.pdf`).

### 12.3. PDF Styling

Use the Saffron Monk brand styling:
- Saffron header band with the title
- Helvetica text
- Pipe tables rendered as REAL tables (gray header + zebra rows)
- Clear section headings

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| v1 | 2026-06-11 | Initial analysis with shop prices ($25 retail, $10/kg tea) |
| v2 | 2026-06-11 | Updated: tea to Upper Taekri at $20/lb, wholesale $17/bag, bars $6 wholesale |
| v3 | 2026-06-11 | Updated: 500g mass bars at $50 retail / $34 wholesale |
| v4 | 2026-06-11 | Corrected: apothecaries (not Upper Taekri) at $20/lb |

---

## 14. Related Documents

- [AORA_EXPERIENCE_PLAN.md](./AORA_EXPERIENCE_PLAN.md) — Master execution roadmap with freight context
- [agroverse-freight-audit/pointers/freight_partners.json](https://github.com/TrueSightDAO/agroverse-freight-audit/blob/main/pointers/freight_partners.json) — Freight partner contacts
- [agroverse-freight-audit/pointers/freight_lanes.json](https://github.com/TrueSightDAO/agroverse-freight-audit/blob/main/pointers/freight_lanes.json) — Freight pricing snapshots
- [treasury-cache/dao_offchain_treasury.json](https://github.com/TrueSightDAO/treasury-cache/blob/main/dao_offchain_treasury.json) — Treasury ledger with cost basis
- [agroverse.shop/js/products.js](https://agroverse.shop/js/products.js) — Live retail prices
- [reports/freight_profit_analysis_2026-06-11_v4.pdf](./reports/freight_profit_analysis_2026-06-11_v4.pdf) — Latest example report
