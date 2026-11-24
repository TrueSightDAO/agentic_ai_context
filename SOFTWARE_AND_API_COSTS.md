# Software & API Costs — receipt registry

> **Purpose:** one canonical place to record third-party software / API / subscription costs paid
> by DAO members on the DAO's behalf, with the receipt evidence cited, so each one can be filed
> to the ledger once and never double-filed.
>
> **Why this file exists.** Governors pay for vendor subscriptions and API credits out of pocket
> and file them as USD contributions after the fact. Those receipts live in email and chat
> attachments, which is exactly where they get lost. (2026-11-23: **13 Anthropic receipts** were
> found unfiled in a single inbox sweep.) This registry is the index; the PDFs live in
> `store_interaction_attachments/asset_receipts/`.
>
> **Filing convention.** `CONTRIBUTION EVENT`, `Type = USD`, `Amount` = **amount actually paid**
> (i.e. inclusive of tax), `Contributor` = the governor's **ledger name** (never an inferred email).

---

## Filed

| Date paid | Vendor | Description | Amount | Evidence | Ledger status |
|---|---|---|---|---|---|
| 2026-11-24 | **DeepSeek** | DeepSeek API tokens (1 × $20.00 + 6% China VAT $1.20) | **USD 21.20** | `asset_receipts/2026-11-24_deepseek_api_credits_usd21.20_paypal_VFN458TBKS9EU.pdf` | filed 2026-11-24 |

### DeepSeek — 2026-11-24 receipt detail

| Field | Value |
|---|---|
| Vendor | DeepSeek, 12F Galaxy International Building, Gongshu Dist, Hangzhou 310003, Zhejiang, China — `api-service@deepseek.com` |
| Bill to | Zhiwen Teh, US — `billing@getdata.io` |
| Payment number | `7PB95166B6013154G` |
| Receipt number | `772877866fe946e1bf67d25fa7ddcecf` |
| Payment method | PayPal — `VFN458TBKS9EU` |
| Date paid | November 24, 2026 |
| Line item | DeepSeek API tokens — Qty 1 — Unit $20.00 — Tax 6% |
| Subtotal / excl. tax | $20.00 |
| VAT-China 6% | $1.20 |
| **Total paid** | **$21.20** |

**Note on the tax line.** The 6% is **China VAT**, applied because the vendor is a Chinese entity.
The contribution is recorded at **$21.20** (cash actually out of pocket), not the $20.00 pre-tax
subtotal — the VAT is a real cost of the purchase, not a recoverable item.

---

## Unfiled backlog — awaiting governor decision

### Anthropic, PBC — Claude Pro, 13 monthly receipts

All from `invoice+statements@mail.anthropic.com` to `garyjob@agroverse.shop`.
**Discovered 2026-11-23, still unfiled.** Amounts are **$20.00** each ⇒ **≈$260 total**.

| Receipt # | Date | Amount |
|---|---|---|
| 2893-9096-8721 | 22 Nov 2026 | $20.00 |
| 2890-6235-8370 | 22 Oct 2026 | $20.00 |
| 2128-4828-6836 | 22 Sep 2026 | $20.00 |
| 2909-9495-4792 | 22 Aug 2026 | $20.00 |
| 2690-1065-0974 | 22 Jul 2026 | $20.00 |
| 2999-5545-1246 | 22 Jun 2026 | $20.00 |
| 2914-5219-1159 | 22 May 2026 | $20.00 |
| 2300-8242-2302 | 21 May 2026 | $20.00 |
| 2724-0095-9425 | 15 May 2026 | $20.00 |
| 2529-3686-6324 | 21 Apr 2026 | $20.00 |
| 2354-4725-3095 | Apr 2026 | $20.00 |
| (2 further, IDs not yet captured) | ~Mar 2026 | $20.00 |

**Three things must be resolved before filing these:**

1. **No PDF attachments.** Those emails carry **Stripe links**, not files — `Download receipt`
   (`dashboard.stripe.com/...`, likely auth-walled) and `Download invoice`
   (`pay.stripe.com/invoice/...`, usually public). Receipts must be *fetched*, not read from the mail.
2. **May 2026 looks anomalous** — receipts on **21 May** and **22 May**, plus an off-cycle **15 May**.
   That pattern suggests a duplicate/retry charge or a plan change. Verify against the Stripe
   billing history **before** filing all of them as clean monthly subscriptions.
3. **Expense vs contribution.** These are vendor costs, not value-add. Filing a cost as a
   contribution inflates contribution totals. Governor must pick one convention and it should be
   applied consistently to DeepSeek too.

**Procedure when approved:** file **one** receipt -> read back to confirm it actually persisted
(see `OPEN_FOLLOWUPS.md` — HTTP 200 from `submit_contribution` does **not** prove the event
landed) -> only then file the remainder.
