# Stripe Transaction Routing — Flow Map

> **Where:** `tokenomics/google_app_scripts/tdg_asset_management/stripe_sales_sync.gs` (runs hourly)
> **Registry:** Shipment Ledger Listing (Main Ledger, Col A = Ledger ID, Col AB = Resolved URL)

## Current flows

```
┌─────────────────────────────────────────────────────────────────┐
│                        STRIPE CHARGES                           │
└─────────────────────────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┬──────────────────┐
        ▼           ▼           ▼                  ▼
   Agroverse QR  Meta/IG     Edgar SaaS       capoeira.agroverse
   Code Checkout Checkout   Subscription        .shop donations
        │           │           │                  │
        ▼           ▼           ▼                  │
   QR Code      Stripe      stripe_sales_         │ (NO ROUTE YET)
   Sales tab    Social       sync.gs              │
   (Telegram    Media        │                    │
   sheet)       Checkout     │                    │
   │            ID tab       ▼                    │
   │            │        offchain                 │
   ▼            │       transactions              │
  Edgar ────────┘       (Main Ledger)             │
   │                                              │
   ▼                                              │
process_sales_telegram_logs.gs                     │
   │                                              │
   ▼                                              │
AGL Managed Ledgers (AGL4, AGL6, etc.)             │
   │                                              │
   ▼                                              │
snapshot_managed_ledgers.py                        │
   │                                              │
   ▼                                              │
treasury-cache/managed-ledgers/<LedgerID>.json     │
```

## Proposed: metadata.ledger routing

Add to `stripe_sales_sync.gs`, after the existing product-ID check:

```
For each Stripe charge:
  1. Existing: check QR Code Sales → skip if found
  2. Existing: check Stripe Social Media Checkout ID → skip if found
  3. Existing: check Stripe product ID (Edgar SaaS) → write to offchain transactions
  4. NEW: check charge.metadata.ledger → if set, route to that ledger:
     a. Look up Ledger ID in Shipment Ledger Listing
     b. Open the ledger's spreadsheet via Resolved URL
     c. Write to its Transactions tab:
        Date, Description, Amount, Currency, Type="Sale"
```

```
┌─────────────────────────────────────────────────────────────────┐
│  NEW: capoeira.agroverse.shop Stripe Checkout                   │
│  metadata: { ledger: "TBM" }                                    │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
           stripe_sales_sync.gs
           (hourly run)
                    │
                    ▼
           detects metadata.ledger = "TBM"
                    │
                    ▼
           Shipment Ledger Listing lookup
            TBM → 1rNwXIpARVb06Opn5gYuiNTG6ZSdA...
                    │
                    ▼
           TBM Transactions tab
           (Date, Description="Stripe: Donation", Amount, Currency, Type="Sale")
                    │
                    ▼
           snapshot_managed_ledgers.py
                    │
                    ▼
           treasury-cache/managed-ledgers/TBM.json
                    │
                    ▼
           tribomirimbahia.truesight.me (explorer)
```

## Ledger routing rule

| Stripe metadata | Routes to |
|---|---|
| `ledger: TBM` | TBM (Tribo Bahia Mirim — Donation ledger) |
| `ledger: AGL4` | AGL4 (Oscar Fazenda inventory) |
| `ledger: SEF1` | SEF1 (Sunmint tree planting) |
| (no metadata) | Existing flow (QR Code / Meta / Edgar SaaS) |

Any Stripe Checkout can route to any managed ledger just by setting `metadata.ledger`.

## How the Stripe Social Media Checkout ID tab fits

It's populated automatically by Stripe's Meta/Instagram integration — no GAS writes to it. It serves as a duplicate-detection source for `stripe_sales_sync.gs` and `process_sales_telegram_logs.gs`. It does NOT pipe into Telegram & Submissions. The tab is the source of truth for Meta/Instagram orders; the GAS scripts read from it, never write to it.
