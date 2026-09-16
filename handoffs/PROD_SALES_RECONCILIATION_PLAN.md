# Prod Sales Reconciliation Plan - 20260710 Sao Jorge Bar Batch

**Status:** COMPLETE - 2026-09-16. Six SALES EVENTs recorded; all six QR codes SOLD.
**Thread:** Telegram #30870 - **Date:** 2026-09-15 (updated 2026-09-16) - **Author:** Sophia Truesight (admin+sophia@truesight.me)

---

## 1. Goal

Reconcile the six "81% Dark Chocolate Bar 50g - Cacao Almonds KG, Fazenda Sao Jorge" units
(QR `2024_20260710_12` / `_13` / `_14` / `_37` / `_38` / `_39`, ledger AGL4) that shipped under
UPS tracking `1Z0C39140337625102`: confirm the net sale price per unit and record the sale so the
QR codes flip MINTED to SOLD and the off-chain ledger depletes.

## 2. Findings

### 2.1 Stripe API verification (2026-09-16)

- Live key sourced from the **Perch** codebase (`sentiment_importer`, `config/environments/production.rb`);
  account `acct_1JTNhzHrrz4344ls` ("TrueSight DAO"). (Key value never printed/stored.)
- Subscription `sub_1ThahUHrrz4344lszxTsvLeR` - **Linda Ford**, status **active**, started 2026-06-12,
  next renewal **2026-10-12**:
  - `price_1Thag4Hrrz4344lsxkuev1so` - "Premium Dark Chocolate Bar - Single-Estate, Monthly Discovery" - qty **6 @ $10.00/mo**
  - `price_1Thag4Hrrz4344lsmnIbNNqX` - Shipping - qty 1 @ $10.80/mo
- September renewal invoice `in_1UEwYMHrrz4344lsRdOATmVB`, created **2026-09-12 19:25 UTC**,
  period 2026-08-12 -> 2026-09-12, `billing_reason=subscription_cycle`:
  - lines: 6 x $10.00 = **$60.00** (bars) + 1 x $10.80 (shipping) = **$70.80**
  - charge `ch_3UExV5Hrrz4344ls0OcT7KUY` - amount $70.80, Stripe fee **$2.35**, **net $68.45**

### 2.2 Economics per bar

| Basis | Gross/bar | Net/bar |
|---|---|---|
| Order total / 6 bags (incl. shipping recharge) | $11.80 | **$11.41** |
| Bars line only (excl. shipping pass-through) | $10.00 | $9.61 |

- Gross per bag = $70.80 / 6 = **$11.80**; net per bag = $68.45 / 6 = **$11.41**.
- If the $10.80 shipping is treated as a pass-through not attributable to the bars:
  bars gross $10.00, product net = ($60.00 - $2.35) / 6 = **$9.61**.

> Supersedes the earlier (wrong) "net $9.78/bar" figure in the first draft of this plan.

### 2.3 Consignment origin

- All six bars are consigned to **Kirsten Ritschel** (manager); aggregate sell-through partners
  ("Acme Bread", "Rainbow Grocery", "Good Eggs", ...) are **Kirsten's stores**:
  `sold_by = Kirsten Ritschel`, `cash_collected_by = Gary Teh`.
- The matching September sale is a **subscription renewal**, not a one-off retail order.
  Customer **Linda Ford** = the `topcoat_cheesy_1h@icloud.com` Apple-relay alias.

## 3. Resolution (2026-09-16)

Governor confirmed the six `2024_20260710_*` codes are Linda Ford's September renewal units. Six
`[SALES EVENT]`s submitted (one per QR, per SOPHIA_BATCH_SALES_PLAN.md sec.0): Item = QR code,
Sales price $11.80/bar gross, Sold by = manager (Kirsten Ritschel x3 / Gary Teh x3), Owner email
topcoat_cheesy_1h@icloud.com, plus attrs Stripe fee per bar $0.3917 / Net after fees per bar $11.4083.
All six verified SOLD. Live Stripe key vaulted as `stripe_live_key`.

## 4. RESUME (historical)

1. Governor confirms UPS `1Z0C39140337625102` = the six `2024_20260710_*` bags in Linda's Sept renewal.
2. Record six `[SALES EVENT]`s (one per QR code, per SOPHIA_BATCH_SALES_PLAN.md sec.0) at the chosen
   price - recommend **$11.41 net/bar** (or $11.80 gross/bar).
3. Verify the QR codes flip MINTED -> SOLD and AGL4 depletes.
