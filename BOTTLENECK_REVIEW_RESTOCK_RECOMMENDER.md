# Supply Chain Bottleneck — On‑the‑Fly Restock Recommender

Status: implemented (frontend + API live). UI: dapp/restock_recommender.html → https://dapp.truesight.me/restock_recommender.html. Backend action: `restock_recommend` in tokenomics `google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`.

Purpose: capture the highest‑leverage operational bottleneck and the thin solution to unlock speed, lower shipping cost per unit, and better capital allocation across the partner network.

## Summary

The current supply chain lacks a single‑tap flow to size partner restocks using live shipping rates from Kirsten (SF) and recent sell‑through. This slows replies to partners, raises shipping $/bag through too‑frequent small parcels, and ties up capital in over‑sent inventory. A thin “Restock Recommender” layer unblocks this in under 30 seconds from a phone.

See also: `RESTOCK_RECOMMENDER_ON_THE_FLY.md` (implementation outline).

## Impact (why this first)

- Cost: Fewer, larger parcels lower shipping cost per bag from SF.
- Speed: Partners get confident answers in <30 seconds.
- Capital efficiency: Ship ~4–8 weeks of stock based on actual velocity.
- Network ops: Fewer back‑and‑forths; fewer stockouts; smoother cadence.

## Solution (thin slice)

- API: `restock_recommend` in Shipping Planner (tokenomics `google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`).
  - Inputs: `partner_id`, optional `product` (default: Ceremonial Cacao 200g).
  - For N in [6, 12, 18, 24, 36, 48], compute USPS cost SF→partner and weeks‑of‑stock from recent velocity; pick N in target range minimizing $/bag.
  - Output: `{ recommended_N, shipping_cost_usd, weeks_of_stock, alternatives[] }`.
- Data plumbing:
  - Partner addresses sheet in Main Ledger: `partner_id, street, city, state, zip, country`.
  - Partner sales/velocity sheet: `partner_id, product, units_last_90_days` (or monthly rate) derived from existing sales/ledger.
- UI: Minimal mobile page in `dapp` (`restock_recommender.html`).
  - Select partner → “Get recommendation” → “Send 24 bags (~6 weeks), ~$11 ship.” + copyable reply text.

## Success Metrics

- Time‑to‑reply < 30 seconds from message to number.
- Shipping $/bag reduced (baseline vs post‑launch).
- Partner stockouts reduced; “weeks of stock at partner” within target.

## Prerequisites

- Currencies: Ensure unit weights populated (K grams/L ounces) for shipped SKUs.
- Shipping Planner: Script Properties set to Kirsten’s SF origin; EasyPost creds valid.
- Inventory fidelity: “offchain asset location” current for available‑to‑ship view.

## Risks & Mitigations

- Stale velocity data → refresh weekly (or backfill via POS/QR where available).
- Address quality → maintain Partner addresses sheet; basic validation on write.
- USPS rating variance → show ranges; cache last known good quote per lane/N.

## Next Steps Checklist

1. Add “Partner addresses” sheet to Main Ledger (columns A–F as above).
2. Add “Partner sales/velocity” sheet (A: partner_id, B: product, C: units_90d).
3. Verify API deployment URL in `dapp/restock_recommender.html` (fallback matches live GAS URL) and that Script Properties are set (EasyPost + SF origin).
4. Pilot with 1–2 partners; compare recommendations vs actual sell‑through.

## Related Docs

- `RESTOCK_RECOMMENDER_ON_THE_FLY.md` — detailed implementation outline.
- `SUPPLY_CHAIN_AND_FREIGHTING.md` — inventory locations, USPS vs freight logic.
- `PROJECT_INDEX.md` → tokenomics, dapp — stack, entry points.

## Notes

- Brazil→US lanes (Matheus→Kirsten) are freight‑only; separate UI/CLI can expose `getFreightCost(...)` later. Not required for the MVP above.
- I‑Ching/QMDJ work is orthogonal to this supply‑chain bottleneck and can proceed in parallel without blocking restock decisioning.
