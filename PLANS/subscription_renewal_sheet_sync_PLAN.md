# Plan: Sync Subscription Renewal Payments to Social Media Checkout ID Tab

**Author:** Sophia Truesight (admin+sophia@truesight.me)  
**Date:** 2026-07-12  
**Implemented:** 2026-07-13  
**Status:** Implemented  
**Reviewers:** Gary, DeepSeek, Claude

---

## 1. Problem Statement

Linda Ford has an active subscription for Premium Dark Chocolate Bar x6 (Monthly Discovery). On **July 12, 2026**, her subscription auto-renewed and Stripe successfully charged **$70.80** (`pi_3TsTxDHrrz4344ls1nolc2GI`, invoice `in_1TsT0kHrrz4344lsK6MU40Xf`).

This payment exists in Stripe but **never landed in the "Stripe Social Media Checkout ID" tab** of the Main Ledger. The tab only contains her initial checkout session from June 12.

## 2. Root Cause

The GAS script (`1ovx-Hq5L5MgzF32qB_cPV_G5Hc6XshKMAYOmiJY8tZ355gzWUqvFCPvn/Code.js`) handles two flows:

| Flow | Stripe Event | Currently Handled? |
|------|-------------|-------------------|
| One-time checkout | `checkout.session.completed` | ✅ Yes — webhook + poller |
| Subscription initial signup | `checkout.session.completed` | ✅ Yes — same as above |
| **Subscription renewal** | **`invoice.paid`** | **✅ Yes (implemented 2026-07-13)** |

The webhook handler only checked `event.type === 'checkout.session.completed'`. The poller (`syncStripeOrders`) only queried `checkout/sessions?status=complete`. Neither touched subscription invoices.

## 3. Schema Change (Actual — columns adjusted for existing usage)

The sheet already had columns O/P/Q in use (`Tracking Notification Sent`, `Ledger Routed`, `Environment`). New columns use **R/S/T**:

| Col | Header | Description | Existing rows | New renewal rows |
|-----|--------|-------------|---------------|------------------|
| A–Q | *(existing)* | Timestamp, Name, Session ID, Items, Amount, etc. | ✅ Filled | ✅ Filled |
| **R** | **Invoice ID** | `in_xxx` from Stripe invoice | *(blank)* | `in_1TsT0k...` |
| **S** | **Payment Intent ID** | `pi_xxx` from Stripe payment intent | *(blank)* | `pi_3TsTxD...` |
| **T** | **Payment Type** | `one_time` or `subscription_renewal` | *(blank)* | `subscription_renewal` |

**Why this doesn't break existing rows:**
- Existing rows have blanks in R/S/T — no data loss
- Column C (Stripe Session ID) remains the primary identifier for one-time checkouts
- Renewal rows carry the **original `cs_xxx` session ID** in column C (retrieved from subscription metadata), linking them to the parent subscription

## 4. Deduplication Strategy

Three-layer dedup to handle Stripe webhook retries and poller overlap:

```js
// Layer 1: Session ID (col C) — catches initial checkouts
if (findOrderRowBySessionId(sheet, sessionId)) return;

// Layer 2: Invoice ID (col R, index 17) — catches subscription renewals
if (findOrderRowByColumn(sheet, 17, invoiceId)) return;

// Layer 3: Payment Intent ID (col S, index 18) — ultimate dedup
if (findOrderRowByColumn(sheet, 18, paymentIntentId)) return;
```

Stripe webhook retries always carry the **same** `invoice.id` and `payment_intent.id`, so retries will be caught by Layer 2 or 3.

## 5. Implementation Checklist

### 5.1 Webhook Handler — Add `invoice.paid` branch ✅

**File:** `agroverse_shop_checkout.gs` → `handleStripeWebhook()`

Added `else if (event.type === 'invoice.paid')` branch that:
- Filters for `billing_reason === 'subscription_cycle'`
- Retrieves subscription to get `metadata.checkout_session_id`
- Calls `saveSubscriptionPaymentToSheet()`

### 5.2 Poller — Extend `syncStripeOrders` to also query invoices ✅

**File:** `agroverse_shop_checkout.gs` → `syncStripeOrdersForEnvironment()`

Added invoice polling after existing checkout session polling:
- **7-day lookback** (not 24h — catches missed webhooks after weekends, as confirmed by Linda's July 12 case being discovered July 13)
- Dedups by Invoice ID (col R) and Payment Intent ID (col S)
- Auto-creates headers via `ensureSubscriptionColumns_()`

### 5.3 Helper Functions ✅

All added to `agroverse_shop_checkout.gs`:

- `ensureSubscriptionColumns_()` — adds R/S/T headers if missing
- `findOrderRowByColumn(sheet, colIndex, value)` — generic column-value dedup
- `retrievePaidSubscriptionInvoices(stripeSecretKey, createdAfter)` — queries `/v1/invoices?status=paid`
- `retrieveStripeSubscription(subscriptionId, secretKey)` — GET `/v1/subscriptions/{id}`
- `saveSubscriptionPaymentToSheet(invoice, subscription, originalSessionId, CONFIG)` — builds and appends row

### 5.4 Schema Migration ✅

Headers added via GAS auto-migration (`ensureSubscriptionColumns_`). Also added to SCHEMA.md.

## 6. Edge Cases & Risks

| Edge Case | Handling |
|-----------|----------|
| **Stripe webhook retries** (exponential backoff, up to 3 days) | Dedup by invoice ID (col R) — same `in_xxx` every retry |
| **Webhook + poller both fire for same invoice** | Dedup catches it — second write is a no-op |
| **Subscription cancelled mid-cycle** | No `invoice.paid` fires — nothing to write. Correct behavior. |
| **Customer changes shipping address on renewal** | Invoice has `shipping_details` — use it. If absent, fall back to original subscription metadata. |
| **Multiple subscriptions, same customer** | Each renewal is a separate invoice with unique `in_xxx` — no collision |
| **Existing rows (no R/S/T columns)** | `findOrderRowByColumn` returns 0 for blank cells — no false positives |
| **Stripe API rate limits** | Poller runs every 5-15 min, max 100 invoices per call — well within Stripe's limits |

## 7. Backfill — Linda Ford's July 12 Payment

Covered by 7-day poller lookback. The first poller run after deployment will pick up Linda's July 12 invoice (`in_1TsT0kHrrz4344lsK6MU40Xf`) because:
- The 7-day lookback window includes July 12
- The invoice has `billing_reason === 'subscription_cycle'` and `status === 'paid'`
- It's not already in the sheet (no row with this invoice ID)

## 8. Rollback Plan

- Remove columns R, S, T from the sheet (no data loss — they're additive)
- Revert the GAS script to the previous deployed version
- Existing data in A–Q is untouched

## 9. Resolved Questions

1. ✅ **Backfill Linda's July 12 payment?** — Yes, handled by 7-day poller lookback.
2. ✅ **Poller lookback: 24h or 7 days?** — **7 days.** Confirmed by the discovery pattern: payment made July 12, discovered missing July 13.
3. ✅ **Shipping cost on renewal rows?** — Invoice line items handle this; shipping is $0 for subscription renewals (Stripe doesn't charge shipping on renewals).
4. ✅ **`invoice.payment_failed` events?** — Not handled. Deferred for future alerting work.

---

**Files changed:**
- `agroverse_shop/google-app-script/agroverse_shop_checkout/agroverse_shop_checkout.gs`
- `tokenomics/SCHEMA.md`
- `agentic_ai_context/PLANS/subscription_renewal_sheet_sync_PLAN.md`
