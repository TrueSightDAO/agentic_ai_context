# Prod Sales Reconciliation Plan - 20260710 Sao Jorge Bar Batch

**Status:** blocked - awaiting governor confirmation of the UPS 6-bar order
**Thread:** Telegram #30870 - **Date:** 2026-09-15 - **Author:** Sophia Truesight (admin+sophia@truesight.me)

---

## 1. Goal

Reconcile the six "81% Dark Chocolate Bar 50g - Cacao Almonds KG, Fazenda Sao Jorge" units
(QR `2024_20260710_12` / `_13` / `_14` / `_37` / `_38` / `_39`, ledger AGL4) that shipped under
UPS tracking `1Z0C39140337625102`: confirm the net sale price per unit and record the sale so the
QR codes flip MINTED to SOLD and the off-chain ledger depletes.

## 2. Findings (2026-09-15)

- **Consignment origin:** all six bars are consigned to **Kirsten Ritschel** (manager); every
  aggregate sell-through partner ("Acme Bread", "Rainbow Grocery", "Good Eggs", ...) is
  **Kirsten's store**: `sold_by = Kirsten Ritschel`, `cash_collected_by = Gary Teh`.
- **The matching September sale is a subscription renewal**, not a one-off retail order:
  - Customer **Linda Ford** - the `toffees_fibrils.0l@icloud.com` / `topcoat_cheesy_1h@icloud.com`
    Apple-relay alias (confirmed: the June order for the same relay email shipped in Linda Ford's name).
  - Stripe row `2026-09-12T21:06:43.367Z`, item "6 x Premium Dark Chocolate Bar - Single-Estate,
    Monthly Discovery" + shipping, **$70.80 gross**, **$2.35 Stripe fee**, invoice `in_1UEwYMHrrz4344lsRdOATmVB`.
- **Economics per bar:** gross **$10.114/bar**; net after fees **$9.78/bar** (shipping is a
  pass-through recharged inside the $70.80, so the Stripe fee amortizes across the bars).

## 3. Open question (blocker)

The UPS consignment box (6 bars, label dated ~2026-09-13) and Linda Ford's **direct-to-home**
subscription (shipped 2026-08-16) may be two different movements of the same SKU. Confirm whether
the six `2024_20260710_*` codes are the units in Linda's September renewal - if so, record the
`[SALES EVENT]`(s) at the gross figures above.

## 4. RESUME HERE

1. Governor confirms the mapping between UPS `1Z0C39140337625102` and Linda Ford's September charge.
2. Record six `[SALES EVENT]`s (or one bulk) at sales price $10.1143/bar, net $9.78/bar.
3. Verify the QR codes flip MINTED to SOLD and AGL4 depletes.
