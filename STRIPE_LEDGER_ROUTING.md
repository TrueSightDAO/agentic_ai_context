# Stripe Transaction Routing — Flow Map

> **Insertion point:** `MetaCheckoutOrderSync#sync!` (Edgar, `app/services/meta_checkout_order_sync.rb`)
> — after `append_checkout_log`, checks `metadata.ledger` and routes to managed ledger.
> **Registry:** Shipment Ledger Listing (Main Ledger, Col A = Ledger ID, Col AB = Resolved URL)

## Current flow (what exists today)

```
Stripe checkout.session.completed webhook
                    │
                    ▼
           webhook_controller.rb#stripe
                    │
                    ▼
           MetaCheckoutOrderSyncWorker (Sidekiq)
                    │
                    ▼
           MetaCheckoutOrderSync#sync!
           │
           ├── eligible_session? → metadata.channel == 'meta' ??
           │
           ├── Parse products, fetch Wix, create order
           │
           └── append_checkout_log → Gdrive::StripeCheckoutLog
               │
               ▼
               Stripe Social Media Checkout ID tab
               (Main Ledger, gid=1787371190)
               │
               ▼
          [NO FURTHER ROUTING — ends here]
```

## Proposed: metadata.ledger routing

Add to `MetaCheckoutOrderSync#sync!`, after `append_checkout_log`:

```ruby
# After: log_entry = append_checkout_log(...)
if (ledger_id = metadata['ledger']).present?
  ManagedLedgerRouter.route!(
    ledger_id: ledger_id,
    session: @session,
    items: summarize_items(order_items, wix_products),
    log_entry: log_entry
  )
end
```

New service `ManagedLedgerRouter`:
1. Looks up `ledger_id` in Shipment Ledger Listing (Col A)
2. Opens the ledger's spreadsheet via Resolved URL (Col AB)
3. Writes to Transactions tab: Date, Description, Amount, Currency, Type="Sale"
4. No-op if ledger not found or not Active

```
┌─────────────────────────────────────────────────────────────────┐
│  capoeira.agroverse.shop Stripe Checkout                        │
│  metadata: { ledger: "TBM", channel: "web" }                    │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
           Stripe webhook → Edgar
                    │
                    ▼
           MetaCheckoutOrderSync#sync!
                    │
                    ├── eligible_session? → channel='web' ≠ 'meta' → SKIP Wix
                    │
                    ├── metadata.ledger = 'TBM' → ManagedLedgerRouter
                    │       │
                    │       ├── Shipment Ledger Listing lookup
                    │       ├── TBM Transactions tab (write row)
                    │       └── Stripe Checkout Log (append for audit trail)
                    │
                    └── snapshot_managed_ledgers.py → TBM.json → explorer
```

## Ledger routing rule

| Stripe metadata | eligible_session? | Routes to |
|---|---|---|
| `channel: meta, wix_products: ...` | Yes → Wix order created | Existing flow: Stripe Checkout Log |
| `ledger: TBM` | No (no `channel: meta`) | TBM Transactions tab + Stripe Checkout Log |
| `ledger: AGL15` | No | AGL15 Transactions tab + Stripe Checkout Log |
| (none) | No | Stripe Checkout Log only |

Any Stripe Checkout can route to any managed ledger just by setting `metadata.ledger`.

## How the Stripe Social Media Checkout ID tab fits

Populated by `Gdrive::StripeCheckoutLog.append_record` (called from `MetaCheckoutOrderSync`). It's the source of truth for all Stripe checkout orders. It serves as:
- Duplicate-detection source for `stripe_sales_sync.gs` and `process_sales_telegram_logs.gs`
- Audit trail for all Stripe transactions, regardless of routing
