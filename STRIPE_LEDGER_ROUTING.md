# Stripe Transaction Routing — All Flows

> **Where the code lives:**  
> Webhook handler: `sentiment_importer/app/controllers/webhook_controller.rb`  
> Meta checkout: `sentiment_importer/app/services/meta_checkout_order_sync.rb`  
> Stripe tab writer: `sentiment_importer/app/models/gdrive/stripe_checkout_log.rb`  
> GAS poller: `tokenomics/google_app_scripts/tdg_asset_management/stripe_sales_sync.gs`  
> **Registry:** Shipment Ledger Listing (Main Ledger, Col A = Ledger ID, Col AB = Resolved URL)

---

## Flow 1: Meta/Instagram Checkout (agroverse.shop)

**Trigger:** Stripe `checkout.session.completed` webhook with `metadata.channel == 'meta'`  
**Latency:** Real-time (webhook → Sidekiq worker, seconds)

```
Instagram/Facebook Shop → Stripe Checkout → webhook_controller.rb#stripe
                                                    │
                                          MetaCheckoutOrderSyncWorker
                                                    │
                                          MetaCheckoutOrderSync#sync!
                                          │
                                          ├── eligible_session? → metadata.channel == 'meta' ✓
                                          ├── parse Wix products from metadata.wix_products
                                          ├── create Wix order via WixStoreService
                                          └── append_checkout_log → Gdrive::StripeCheckoutLog
                                              │
                                              ▼
                                         Stripe Social Media Checkout ID tab
                                         (Main Ledger gid=1787371190)
                                              │
                                              ▼
                                         [ENDS — no further routing]
```

**Code:** `met»_checkout_order_sync.rb:20-45` (sync!), `:49-51` (eligible_session?), `:325-336` (append_checkout_log)

---

## Flow 2: QR Code Checkout (DApp scanner)

**Trigger:** User scans QR code on `dapp.truesight.me/scanner.html`, signs `[SALES EVENT]`  
**Latency:** Near real-time (DApp POST → Edgar → GAS processing, seconds to minutes)

```
DApp scanner.html → scan QR code → submit [SALES EVENT]
                    │
                    ▼
              Edgar dao_controller.rb
                    │
                    ▼
              Telegram Chat Logs tab (signed event text)
                    │
                    ▼
              campaign_codes_processor.gs (GAS trigger)
                    │
                    ▼
              QR Code Sales tab (Telegram sheet)
                    │
                    ▼
              process_sales_telegram_logs.gs (GAS trigger)
              │
              ├── reads Shipment Ledger Listing for ledger lookup
              ├── writes to target AGL ledger Transactions tab
              └── fires treasury-cache-publisher notification
                    │
                    ▼
              treasury-cache/dao_offchain_treasury.json (main DAO)
```

**Code:** `process_sales_telegram_logs.gs` (main orchestrator), `qr_code_web_service.gs` (QR lookup), `sales_update_managed_agl_ledgers.gs` (ledger writes)

---

## Flow 3: Edgar SaaS Subscriptions

**Trigger:** Stripe charges with specific product IDs (Edgar market sell-off dashboard)  
**Latency:** Hourly poll (`stripe_sales_sync.gs` timer trigger)

```
stripe_sales_sync.gs (runs every hour)
          │
          ├── fetchStripeTransactions() → Stripe API charges
          ├── isChargeInQrCodeSales() → skip if QR code flow handled
          ├── isChargeInStripeCheckoutLog() → skip if Meta flow handled
          ├── matches TARGET_PRODUCT_IDS? (prod_K9i..., prod_K7d..., prod_JvD...)
          │       │
          │       ▼
          │   write to offchain transactions tab (Main Ledger)
          │   - Date, Description, Amount, Currency, Is Revenue
          │   - Also writes Stripe fee as separate negative row
          │
          ▼
      [ENDS — writes to Main Ledger directly]
```

**Code:** `stripe_sales_sync.gs:161-418` (fetchStripeTransactions), `:31-45` (TARGET_PRODUCT_IDS)

**Real-time option:** Deploy GAS as web app with `doPost`, POST from `webhook_controller.rb` after processing. Current hourly poll is acceptable since SaaS billing isn't time-critical.

---

## Flow 4: capoeira.agroverse.shop Donations → TBM (PROPOSED)

**Trigger:** Stripe `checkout.session.completed` with `metadata.ledger` set  
**Latency:** Real-time (webhook → Sidekiq, same path as Flow 1)

**Implementation:** Add to `MetaCheckoutOrderSync#sync!`, after `append_checkout_log`:

```ruby
metadata = @session.metadata || {}
if (ledger_id = metadata['ledger']).present?
  ManagedLedgerRouter.route!(
    ledger_id: ledger_id,
    session: @session,
    items: summarize_items(order_items, wix_products),
    log_entry: log_entry
  )
end
```

```
capoeira.agroverse.shop → Stripe Checkout
  metadata: { ledger: "TBM", channel: "web" }
                    │
                    ▼
           Stripe webhook → Edgar
                    │
                    ▼
           MetaCheckoutOrderSync#sync!
           │
           ├── eligible_session? → channel='web' ≠ 'meta' → skip Wix
           │
           ├── metadata.ledger = 'TBM' → ManagedLedgerRouter
           │       │
           │       ├── Shipment Ledger Listing lookup (Col A='TBM')
           │       ├── Open TBM sheet via Resolved URL (Col AB)
           │       ├── Write to Transactions tab: Date, Description,
           │       │   Amount, Currency, Type="Sale"
           │       └── Append to Stripe Checkout Log for audit trail
           │
           └── snapshot_managed_ledgers.py (next run) → TBM.json
                    │
                    ▼
           tribomirimbahia.truesight.me (explorer)
```

**New files needed:**
- `app/services/managed_ledger_router.rb` — looks up ledger via Google Sheets, writes transaction
- `app/models/gdrive/managed_ledger_transaction.rb` — writes to managed ledger's Transactions tab

---

## All flows summary

| Flow | Trigger | Latency | Writes to | Ledger routing |
|---|---|---|---|---|
| 1. Meta Checkout | Webhook (channel:meta) | Real-time | Stripe tab + Wix order | None (ends at tab) |
| 2. QR Code | DApp [SALES EVENT] | Near real-time | Telegram + AGL ledger | Shipment Ledger Listing |
| 3. Edgar SaaS | Hourly GAS poll | Hourly | offchain transactions | Hardcoded product IDs |
| 4. TBM Donations | Webhook (metadata.ledger) | Real-time | TBM Transactions + Stripe tab | Shipment Ledger Listing |

---

## Real-time GAS trigger

`stripe_sales_sync.gs` (Flow 3) normally runs hourly. To trigger it immediately after a webhook, deploy the GAS as a web app with a `doGet` entry point, then have Edgar enqueue a Sidekiq worker that GETs the URL.

**GAS side** — add to `stripe_sales_sync.gs`:

```javascript
function doGet(e) {
  var result = fetchStripeTransactions();
  return ContentService.createTextOutput(JSON.stringify({
    status: 'ok',
    processed: result
  })).setMimeType(ContentService.MimeType.JSON);
}
```

Deploy as web app (`Deploy → New deployment → Web app`, execute as "Me", access "Anyone"). Copy the exec URL.

**Edgar side** — new Sidekiq worker:

```ruby
# app/workers/stripe_sales_sync_trigger_worker.rb
class StripeSalesSyncTriggerWorker
  include Sidekiq::Worker

  def perform
    uri = URI(ENV['STRIPE_SALES_SYNC_GAS_URL'])
    uri.query = URI.encode_www_form({})
    HTTP.get(uri.to_s)
  end
end
```

**Trigger from webhook controller:**

```ruby
# app/controllers/webhook_controller.rb
when "checkout.session.completed"
  session_id = event_json.dig("data", "object", "id")
  MetaCheckoutOrderSyncWorker.perform_async(session_id) if session_id.present?
  StripeSalesSyncTriggerWorker.perform_in(30.seconds)  # slight delay to let meta checkout finish
```

This mirrors the existing `doGet` pattern used by `dao_members_cache_publisher.gs`, `dapp_permission_change_handler.gs`, and the treasury-cache-publisher — all triggered via GET from Edgar's Sidekiq workers.

---

## Stripe Social Media Checkout ID tab role

Written exclusively by `Gdrive::StripeCheckoutLog.append_record` (called from `MetaCheckoutOrderSync#sync!`). Never written by GAS. Serves as:

- **Audit trail:** Every Stripe checkout lands here regardless of routing
- **Duplicate guard:** `stripe_sales_sync.gs` (Flow 3) and `process_sales_telegram_logs.gs` (Flow 2) read it to skip already-handled charges
- **Shipping updates:** `process_qr_code_updates.gs` writes shipping provider + tracking number back into this tab
