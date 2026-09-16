# SOPHIA Subscription Sales Reconciliation Plan

**Purpose:** The standard SOP for recording **Stripe subscription renewal** sales of
QR-coded chocolate bars as DAO `[SALES EVENT]`s — so every monthly renewal follows one
recipe instead of a bespoke script.

**Status:** LIVE — 2026-09-16
**Origin:** Linda Ford's September 2026 renewal (Telegram thread 30870).
**Sibling SOPs:** `SOPHIA_BATCH_SALES_PLAN.md` (one-off bulk / cash sales) ·
`notes/claude_serialized_qr_sales_2026-04-29.md` (the one-event-per-QR-code pattern +
fee amortization) · `plans/CHOCOLATE_SUBSCRIPTION_PLAN.md` (Phase-2 automation; **this
SOP is the interim manual bridge** until that ships).

---

## 0. When this SOP applies

Use it when the sale is a **recurring Stripe charge**, i.e. the Stripe invoice has
`billing_reason = "subscription_cycle"` (ID prefix `in_…`, associated subscription
`sub_…`).

| Sale kind | Stripe marker | SOP |
|-----------|---------------|-----|
| One-off online checkout | `cs_live_…` session | `SOPHIA_BATCH_SALES_PLAN.md` |
| Recurring subscription renewal | `in_…` + `subscription_cycle` | **this SOP** |
| Cash / local pickup | none | `SOPHIA_BATCH_SALES_PLAN.md` |

> Subscriptions are **6 chocolate bars / month** by default (preset chips 3 / 6 / 12,
> hard cap ~24 — see `CHOCOLATE_SUBSCRIPTION_PLAN.md` → *Decisions → Quantity*). Do not
> assume the count; read it off the invoice line items.

---

## 1. Preflight — is it ALREADY accounted for?

**Given a set of QR codes, always check first — never assume.** A renewal that has been
recorded once must not be recorded again.

1. `lookup_qr_batch(<the QR codes>)`.
2. Read `qr_status` per code:

| `qr_status` | Meaning | Action |
|-------------|---------|--------|
| `SOLD` | Already recorded | **Skip** that code. Do not re-submit — a repeat is a duplicate sale. |
| `MINTED` | Not yet recorded | **Reconcile** it (continue below). |
| `SCANNED` / other | Ambiguous | Stop and ask the governor. |

3. Mixed results are normal mid-reconciliation: the downstream GAS flips `MINTED → SOLD`
   **asynchronously** (a few seconds to ~a minute after each submission). Re-`lookup`
   before concluding a submission failed.

---

## 2. Pull the transaction details from Stripe

### 2a. The credential

The **live** Stripe secret key for `acct_1JTNhzHrrz4344ls` ("TrueSight DAO" / Agroverse
Shop) is stored in the autopilot **vault** as:

```
name: stripe_live_key     scopes: ['stripe:read']     created_by: Sophia Truesight
```

Read it **server-side only** and **never print the value**:

```python
# on the autopilot box
import sys; sys.path.insert(0, "/opt/truesight_autopilot")
from app.vault import get_vault
key = get_vault().get_value("stripe_live_key")   # do NOT echo this
```

> Fallback / legacy location: Perch (`sentiment_importer`) sources its key from
> `config/environments/production.rb`. Prefer the vault.

### 2b. Finding the invoice

- **Known invoice ID** (e.g. from the sheet's *Stripe Social Media Checkout ID* tab or a
  prior record): `GET https://api.stripe.com/v1/invoices/{in_…}` — this returns the line
  items, `amount_paid`, `billing_reason`, `charge`, and `customer`.
- **Unknown ID** — start from the charge or the customer:
  - `GET /v1/charges/{ch_…}` → `.invoice`
  - `GET /v1/invoices?customer={cus_…}&status=paid&limit=100` → pick the row whose
    `created` matches the renewal month and whose `billing_reason=subscription_cycle`.
  - `GET /v1/subscriptions/{sub_…}` → the plan/quantity.

Auth header: `Authorization: Bearer <key>` (server-side only).

### 2c. The fee (net-of-fees is the point)

Stripe's processing fee is **not** on the invoice. Get it from the charge's balance
transaction:

```
GET /v1/charges/{ch_…}                     -> .balance_transaction  (txn_…)
GET /v1/balance_transactions/{txn_…}       -> .fee  and .net
```

---

## 3. Compute the per-bar net

**The governor's rule (authoritative):**

```
number_of_bars = sum(qty of chocolate-bar line items on the invoice)
amount_charged = invoice.amount_paid          # total billed to the customer
gross_per_bar  = amount_charged / number_of_bars
stripe_fee     = balance_transaction.fee      # e.g. 2.35
net_per_bar    = (amount_charged - stripe_fee) / number_of_bars
```

Carry the fee through as explicit attributes so the ledger shows the split:

```
"Stripe fee per bar"      = fee / number_of_bars      (e.g. 0.3917)
"Net after fees per bar"  = net_per_bar               (e.g. 11.4083)
```

> ⚠️ **Do NOT divide by (bars + shipping line).** The recurring plan bills
> `N × unit_price` **plus a locked recurring shipping line**; the shipping line is a
> recharge, not a bar. Divide the total by the **number of bars only**.
> (Thread 30870 first pass used ÷7 — wrong. Correct is ÷6.)

---

## 4. Resolve the exact QR codes — never pre-assign

Per `CHOCOLATE_SUBSCRIPTION_PLAN.md`: a subscription is a *recurring charge + a monthly
fulfillment obligation*. The specific QR codes are bound **at pack time** by whoever
ships (Kirsten): she grabs any N in-stock bars and records **what actually shipped**.

- **Source of truth = the packer's report / the shipping receipt**, not the subscription.
- If the packer reports only a shipment tracking number, map tracking → order → QR codes
  (the ship confirmation email / GAS order row carries them).
- If the box↔charge mapping cannot be proven, **stop and ask the governor** to confirm —
  do not guess which vintage went in the box.

---

## 5. Submit one `[SALES EVENT]` per QR code

**One event per QR code — never aggregate** (Rule 1 of `SOPHIA_BATCH_SALES_PLAN.md`).
`Item` is the QR code ID; the product description lives in GAS.

Attributes for each bar (per the ratified attribution):

| Field | Value |
|-------|-------|
| `Item` | the QR code, e.g. `2024_20260710_12` |
| `Sales price` | `gross_per_bar` (e.g. `11.80`) |
| `Sold by` | **`Kirsten Ritschel`** (subscription attribution — ratified 2026-06-09) |
| `Cash proceeds collected by` | **`Gary Teh`** |
| `Owner email` | the subscriber's email (e.g. Linda Ford) |
| `Stripe Invoice ID` | `in_…` (the renewal invoice) |
| `Stripe fee per bar` | `fee / bars` |
| `Net after fees per bar` | `net_per_bar` |
| `Shipping Provider` / `Tracking number` | from the ship confirmation |
| `Submission Source` | `dao_client / <subscriber> <Month> subscription renewal / item k of N` |

Notes:

- Use `Stripe Invoice ID` for subscriptions (`in_…`). The `cs_live_…` **`Stripe Session
  ID`** field is for one-off *checkout sessions* — do not put a subscription invoice there.
- Health-check Edgar (`GET https://edgar.truesight.me/events-catalog` → 200) before a
  batch; if any submission returns 500, **abort the batch** (SOPHIA_BATCH_SALES_PLAN.md §5).
- Downstream handles the rest automatically: QR status `MINTED → SOLD`, QR Code Sales tab,
  offchain double-entry, treasury cache. **No separate `[INVENTORY MOVEMENT]`** is needed.

---

## 6. Worked example — Linda Ford, September 2026 (thread 30870)

The six `2024_20260710_12/13/14/37/38/39` bars
("81% Dark Chocolate Bar 50g | Cacao Almonds KG — Fazenda São Jorge", AGL4).

| Step | Value |
|------|-------|
| Preflight | all six `MINTED` → reconcile (not yet accounted for) |
| Invoice | `in_1UEwYMHrrz4344lsRdOATmVB` (2026-09-12, `subscription_cycle`) |
| Charge → fee | `ch_3UExV5Hrrz4344ls0OcT7KUY` → fee **$2.35** |
| Line items | 6 × chocolate bar @ $10.00/mo + 1 × shipping $10.80/mo |
| Bars / charged | **6** / **$70.80** |
| gross_per_bar | 70.80 ÷ 6 = **$11.80** |
| net_per_bar | (70.80 − 2.35) ÷ 6 = **$11.4083** |
| per-bar fee | 2.35 ÷ 6 = **$0.3917** |
| Submit | 6 × `[SALES EVENT]`, `Sold by = Kirsten Ritschel` (×3) / `Gary Teh` (×3), `Owner email = topcoat_cheesy_1h@icloud.com` |
| Verify | all six flipped `MINTED → SOLD` |

---

## 7. Edge cases

| Case | Handling |
|------|----------|
| Renewal **failed / past due**, no `amount_paid` | No sale to record until the payment settles — record only on paid invoices. |
| **Partial/failed** fulfillment (fewer bars shipped than billed) | Record only the bars actually shipped; file a follow-up for the shortfall. |
| Quantity changed (upgrade/downgrade) | Read the **invoice**, not the subscription default. |
| Multiple subscribers same month | Each gets its own invoice + its own set of per-bar events. |
| Currency ≠ USD | Convert at the invoice's rate and note it in `Submission Source`. |
| One invoice, **two** chocolate SKUs | Split: attribute each QR to its own SKU; single invoice ID on all. |
| Duplicate detection | If a QR is already `SOLD` **for the same invoice**, do not resubmit (§1). |

---

## 8. Roadmap — remove the hand-rolling (Phase 2 bridge)

This SOP is the manual bridge. The durable fix (tracked in `OPEN_FOLLOWUPS.md`):

1. **`scripts/reconcile_subscription_sales.py`** in `truesight_autopilot` — takes
   `--invoice in_…` **or** `--qr-codes …`, reads `stripe_live_key` from the vault, computes
   §3, and emits/submits the per-bar events. **Dry-run by default**; `--submit` to fire.
   Idempotent via §1 (skips already-`SOLD` codes).
2. **Monthly detector** — Surface 5 (treasury) / a scheduled probe that flags any
   `subscription_cycle` invoice in the last 30 days with un-recorded QR codes, and
   notifies the operator instead of waiting for a human to notice.

Until those land, follow §1–§6 by hand — but the steps above are copy-paste, not
improvisation.

---

## Cross-references

- `SOPHIA_BATCH_SALES_PLAN.md` — one-off / cash bulk sales (the parent SOP).
- `notes/claude_serialized_qr_sales_2026-04-29.md` — canonical one-event-per-QR + fee amortization.
- `plans/CHOCOLATE_SUBSCRIPTION_PLAN.md` — the subscription product + Phase-2 automation.
- `STRIPE_LEDGER_ROUTING.md` — the Stripe flows + `[LEDGER_ID]` routing + the Stripe Social Media Checkout ID audit tab.
- `OPEN_FOLLOWUPS.md` — where the automation gaps above are filed.
