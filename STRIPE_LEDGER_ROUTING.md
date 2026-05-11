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

**Trigger:** Any Stripe checkout whose "Items Purchased" starts with a known Ledger ID  
**Latency:** Hourly poll (`stripe_sales_sync.gs` timer, or immediate via Sidekiq trigger)

**No Stripe metadata changes needed.** The capoeira checkout creates a Stripe product with a bracketed Ledger ID prefix: `[TBM] — Donation to Tribo Bahia Mirim`. When the checkout completes, the webhook writes to the Stripe tab as usual. `stripe_sales_sync.gs` detects the `[LEDGER_ID]` prefix and routes.

**Implementation:** Add to `stripe_sales_sync.gs`, after the existing product-ID check (line ~407):

```javascript
// After existing product-ID routing...
// NEW: Check Stripe Social Media Checkout ID for ledger-routed purchases
routeStripeCheckoutPurchasesToLedgers();
```

New function `routeStripeCheckoutPurchasesToLedgers()`:
1. Read "Stripe Social Media Checkout ID" tab
2. Read Shipment Ledger Listing for all Ledger IDs + Resolved URLs
3. For each row in Stripe tab:
   - Extract `Items Purchased` (col F)
   - Match `/^\[([A-Z0-9]+)\]/` to extract Ledger ID (e.g. `[TBM]`)
   - If matched and not already processed (check new col P "Ledger Routed"):
     - Open the ledger's sheet via Resolved URL
     - Write to Transactions tab: Date, Description=Items Purchased, Amount, Currency, Type="Sale"
     - Mark col P = the Ledger ID (prevents re-processing)
     - Also fire treasury-cache-publisher notification

```
capoeira.agroverse.shop → Stripe Checkout
  product name: "[TBM] — Donation to Tribo Bahia Mirim"
                    │
                    ▼
           Stripe webhook → Edgar
                    │
                    ▼
           MetaCheckoutOrderSync#sync!
           │
           ├── eligible_session? → no 'channel: meta' → skip Wix
           │
           └── append_checkout_log
               │
               ▼
           Stripe Social Media Checkout ID tab
           Items Purchased: "[TBM] — Donation to Tribo Bahia Mirim"
               │
               ▼
           stripe_sales_sync.gs (hourly, or Sidekiq-triggered)
           │
           ├── routeStripeCheckoutPurchasesToLedgers()
           │       │
           │       ├── regex /^\[([A-Z0-9]+)\]/ extracts "TBM"
           │       ├── Shipment Ledger Listing lookup → TBM sheet URL
           │       ├── Writes to TBM Transactions tab
           │       └── Marks col P = "TBM"
           │
           └── snapshot_managed_ledgers.py → TBM.json → explorer
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
| 4. TBM Donations | `[TBM]` prefix in Items Purchased | Hourly (or trigger) | TBM Transactions tab | Shipment Ledger Listing |

---

## `[LEDGER_ID]` routing pattern

Any Stripe product whose name starts with `[LEDGER_ID] — ` is auto-routed. The GAS matches `/^\[([A-Z0-9]+)\]/` and looks up the Ledger ID in Shipment Ledger Listing.

| Stripe product name | Extracts | Routes to |
|---|---|---|
| `[TBM] — Donation to Tribo Bahia Mirim` | TBM | TBM Transactions tab |
| `[AGL15] — Operational fund contribution` | AGL15 | AGL15 Transactions tab |
| `[SEF1] — Tree planting pledge` | SEF1 | SEF1 Transactions tab |
| `Organic Cacao Beans — Bahia` | (no bracket) | No routing (legacy flow) |

This works for any future merchant — just create a Stripe product named `[LEDGER_ID] — <description>`, and the GAS handles the rest. No metadata, no webhook changes, no Edgar code. The Shipment Ledger Listing is the single registry.

---

## Real-time GAS trigger

`stripe_sales_sync.gs` (Flow 3) normally runs hourly. To trigger it immediately after a webhook, call its `doGet` web app endpoint.

**GAS web app URL:** `https://script.google.com/macros/s/AKfycbwauCMu-3Es0s4rB7Cr-fsP2JuEnebyPS8W-ecXG6RUi_zhqpLfG71bramoEwtk54drfg/exec`

**Edgar side** — Sidekiq worker:

```ruby
# app/workers/stripe_sales_sync_trigger_worker.rb
class StripeSalesSyncTriggerWorker
  include Sidekiq::Worker

  STRIPE_SYNC_URL = 'https://script.google.com/macros/s/AKfycbwauCMu-3Es0s4rB7Cr-fsP2JuEnebyPS8W-ecXG6RUi_zhqpLfG71bramoEwtk54drfg/exec'

  def perform
    HTTP.get(STRIPE_SYNC_URL)
  end
end
```

**Trigger from webhook controller:**

```ruby
# app/controllers/webhook_controller.rb
when "checkout.session.completed"
  session_id = event_json.dig("data", "object", "id")
  MetaCheckoutOrderSyncWorker.perform_async(session_id) if session_id.present?
  StripeSalesSyncTriggerWorker.perform_in(30.seconds)
```

---

## Stripe Social Media Checkout ID tab role

Written exclusively by `Gdrive::StripeCheckoutLog.append_record` (called from `MetaCheckoutOrderSync#sync!`). Never written by GAS. Serves as:

- **Audit trail:** Every Stripe checkout lands here regardless of routing
- **Duplicate guard:** `stripe_sales_sync.gs` (Flow 3) and `process_sales_telegram_logs.gs` (Flow 2) read it to skip already-handled charges
- **Shipping updates:** `process_qr_code_updates.gs` writes shipping provider + tracking number back into this tab
