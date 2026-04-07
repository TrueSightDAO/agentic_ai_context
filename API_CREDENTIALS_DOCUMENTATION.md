# API Credentials Documentation

This document describes every API credential (and credential-like config) found across the workspace: **what it is used for**, **how** (use case), **where** (scenario), and **which codebase** uses it. Credentials are **not** moved here; they remain in each project. This repo holds a **reference template** (`env.template`) and this documentation only.

---

## 1. sentiment_importer

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **ALPHA_VANTAGE_API_KEY** | Alpha Vantage API key | Fetch company overview/fundamentals by stock symbol | Background worker refreshing company data; fallback when FMP/Polygon/IEX fail | `app/workers/company_fundamentals_refresher.rb` |
| **FMP_API_KEY** | Financial Modeling Prep API key | Fetch company profile by symbol | Same worker; primary or fallback source for company fundamentals | `app/workers/company_fundamentals_refresher.rb` |
| **POLYGON_API_KEY** | Polygon.io API key | Fetch company metadata by symbol | Same worker; company data refresh (config fallback: `config.polygon_api_key`) | `app/workers/company_fundamentals_refresher.rb` |
| **IEX_API_KEY** | IEX Cloud API key | Fetch company info by symbol | Same worker; company fundamentals (config fallback: `config.iex_api_key`) | `app/workers/company_fundamentals_refresher.rb` |
| **WIX_API_ACCESS_TOKEN** | Wix API access token | Wix CMS / API access in tests | Test environment only; Wix integration tests | `config/environments/test.rb` |
| **HELLOCASH_PROXY_ENABLED** | Boolean flag | Enable HelloCash API via proxy | Development; when calling HelloCash through an AWS proxy | `config/environments/development.rb` |
| **HELLOCASH_PROXY_HOST** | Proxy host (e.g. AWS IP) | Host for HelloCash proxy | Development; optional override for proxy server | `config/environments/development.rb` |
| **AGROVERSE_INVENTORY_GAS_WEBAPP_URL** | Google Apps Script **web app** URL (no query string) | **`GET`** after **`meta`** Wix order **`:created`** (`MetaCheckoutOrderSyncWorker` / success page), after **QR + Stripe** sale rows are saved (`QrCodeCheckController`), and after successful **ledger** `WebhookTriggerWorker` runs when **`enqueue_agroverse_inventory_snapshot`** is true (`dao_controller#trigger_immediate_processing`) | Production **Sidekiq** `AgroverseInventorySnapshotPublishWorker`; must match **`update_store_inventory`** deployment **exec** URL | `app/workers/agroverse_inventory_snapshot_publish_worker.rb`, `webhook_trigger_worker.rb`, `meta_checkout_order_sync_worker.rb`, `meta_checkout_controller.rb`, `qr_code_check_controller.rb`, `dao_controller.rb` |
| **AGROVERSE_INVENTORY_PUBLISH_SECRET** | Same value as GAS Script property **`AGROVERSE_INVENTORY_PUBLISH_SECRET`** | Query param **`token`** for **`publishInventorySnapshot`** / **`recalculateAndPublishInventory`** | **Never** commit; set in Edgar/sentiment_importer `.env` / host env | Same worker |
| **AGROVERSE_INVENTORY_GAS_ACTION** | Optional; default **`recalculateAndPublishInventory`** | **`publishInventorySnapshot`** = sheet → GitHub only (faster); **`recalculateAndPublishInventory`** = full ledger recalc + publish (slower, safer after sales) | When unset, worker uses **`recalculateAndPublishInventory`** | Same worker |

---

## 2. krake_ror

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **SENDGRID_API_KEY** | SendGrid API key | Send transactional email via SendGrid | Email engagement analyzer task; fetching/sending email-related data | `lib/tasks/email_engagement_analyzer.rb` |

*Note: `config/application.rb` also references `config.bugsnag_api_key` and auth tokens; those are app config, not env-based credentials in the scanned code.*

---

## 3. video_editor

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **GROK_API_KEY** | xAI Grok API key | Call Grok API for video analysis / AI features | Video analysis pipeline; Grok client for AI summarization or analysis | `grok_client.py` |
| **MAX_CONCURRENT_ANALYSIS** | Integer (concurrency limit) | Limit parallel video analysis jobs | Video queue processing | `video_queue.py` |
| **PORT** | Server port | HTTP server port | Running the Flask app | `app.py` |

---

## 4. market_research

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **GOOGLE_CALENDAR_ID** | Google Calendar ID | Target calendar for creating events | Physical-store scripts: creating follow-up events, Staples reminders, etc. | `physical_stores/create_*.py` |
| **DEFAULT_TIMEZONE** | Timezone string (e.g. America/Los_Angeles) | Default timezone for calendar events | Same scripts; event times | `physical_stores/create_*.py` |

*Google Calendar access may also use OAuth or service-account credentials (e.g. from env or a credentials file); the code uses `GOOGLE_CALENDAR_ID` to choose the calendar.*

---

## 5. truesight_me

| Variable / Asset | What it is | Use case | Where / scenario | Code location |
|------------------|------------|----------|------------------|----------------|
| **WIX_API_KEY** | Wix API key | Authenticate to Wix APIs | Syncing blog posts, performance stats, and other Wix data to the static site | `scripts/populatePerformanceStatistics.js`, `scripts/syncBlogPosts.js`, `scripts/syncAllWixData.js` |
| **WIX_SITE_ID** | Wix site ID | Identify Wix site | Same scripts; optional override (defaults in code exist) | Same |
| **WIX_ACCOUNT_ID** | Wix account ID | Identify Wix account | Same scripts; optional override | Same |
| **google-service-account.json** | Google service account JSON (file) | JWT auth to Google Sheets API | Generate shipment and impact registry pages from "Shipment Ledger Listing" sheet | `scripts/generate-shipment-pages.js` (path: `../google-service-account.json`) |

*Expected service account email in that script: `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com`.*

---

## 6. tokenomics

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **QR_CODE_REPOSITORY_TOKEN** | GitHub or repo token | Access QR code repository (e.g. GitHub API) | Webhook handler for QR code repo operations | `agroverse_qr_code_web_service/github_webhook_handler.py` (as `GITHUB_TOKEN`) |
| **GDRIVE_KEY** | Google Drive key / credentials (e.g. JSON) | Drive access in webhook handler | When handling events that need Drive; optional | `agroverse_qr_code_web_service/github_webhook_handler.py` |
| **WIX_ACCESS_TOKEN** | Wix access token | Wix API in tests/scripts | Schema validation tests against Wix | `python_scripts/schema_validation/test_schema_validation.py` |
| **GITHUB_TOKEN** | GitHub token | GitHub API from Apps Script | Apps Script calling GitHub (e.g. repo checks) | `agroverse_qr_code_web_service/qr_code_generator.gs` |
| **GITHUB_ACTIONS** | Env flag | Detect GitHub Actions environment | Conditional behavior in webhook handler | `agroverse_qr_code_web_service/github_webhook_handler.py` |

*Other tokenomics scripts may use AWS (e.g. `AWS_SECRET_ACCESS_KEY_GARYJOB`) for TDG/asset workflows; those are environment-specific and not duplicated here.*

### 6a. Google Apps Script — Agroverse store inventory (`update_store_inventory`)

These are **not** shell `.env` variables. Set them in the **Apps Script editor** for project **`update_store_inventory`**: **Project Settings → Script properties**. **Console:** [script `1P0Mg33i…` (edit)](https://script.google.com/home/projects/1P0Mg33i_dD9x9IeoHYvtKrf0xFcmUznpqAswyC_KXR3VJZu-0C-UOP0v/edit). After `clasp pull`, local mirror: **`tokenomics/clasp_mirrors/1P0Mg33i_dD9x9IeoHYvtKrf0xFcmUznpqAswyC_KXR3VJZu-0C-UOP0v/`**.

| Script property key | What it is | Use case | Where / scenario | Code location |
|---------------------|------------|----------|------------------|----------------|
| **`AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`** | Fine-grained GitHub PAT (**Contents: Read and write** on **`TrueSightDAO/agroverse-inventory`** only) | GitHub **Contents API** (`PUT …/contents/…`) to create or update the public inventory JSON snapshot, including **`sha`** when the file already exists (e.g. after recalculating store inventory or on a time-driven trigger) | Google Apps Script only; **never** commit the value; do not store in the **`agroverse-inventory`** git working tree | **`update_store_inventory`**: after each successful **`updateStoreInventory()`**, and when serving **`?action=publishInventorySnapshot`** |
| **`AGROVERSE_INVENTORY_PUBLISH_SECRET`** | Long random secret (generate locally; not a GitHub token) | **`GET …/exec?action=publishInventorySnapshot&token=…`** and **`…action=recalculateAndPublishInventory&token=…`** so only **sentiment_importer** / trusted callers can trigger a publish or full recalc over the public web app | Set in the same Apps Script project; **never** commit or log | Required for HTTP-triggered publish/recalc; omitting it returns **401 JSON** for those actions |
| **`AGROVERSE_INVENTORY_GITHUB_OWNER`** | Optional override | GitHub repo owner for the snapshot file | Default **`TrueSightDAO`** | — |
| **`AGROVERSE_INVENTORY_GITHUB_REPO`** | Optional override | Repo name | Default **`agroverse-inventory`** | — |
| **`AGROVERSE_INVENTORY_GITHUB_BRANCH`** | Optional override | Branch | Default **`main`** | — |
| **`AGROVERSE_INVENTORY_GITHUB_PATH`** | Optional override | Path to JSON in repo | Default **`store-inventory.json`** | Raw read: `https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/store-inventory.json` |

Snapshot JSON shape: **`{ "generatedAt", "source", "inventory": { "<product-id>": <number>, … } }`**. Consumers should use **`payload.inventory`** for the SKU map. **Publish behavior:** GAS **GET**s the existing file, compares **`inventory`** to the new map, and **skips GitHub PUT** when equal (fewer commits on hourly triggers); **`generatedAt`** is only refreshed when a **PUT** runs.

**`TrueSightDAO/agroverse-inventory`** itself does not require a local `.env` for this PAT—operators configure the secret in Apps Script. If **sentiment_importer** or other Ruby code later pushes to that repo instead, document a separate env var in that codebase; the canonical name proposed for the GAS secret remains **`AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`**.

---

## 7. agroverse_shop

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **NAMECHEAP_API_USER** | Namecheap account username | Namecheap API auth | DNS scripts: testing API, migrating DNS | `scripts/test_namecheap_api.py`, `scripts/migrate_dns_namecheap.py` |
| **NAMECHEAP_API_KEY** | Namecheap API key | Namecheap API auth | Same scripts | Same |
| **NAMECHEAP_CLIENT_IP** | Client IP whitelisted in Namecheap | Required by Namecheap API | Same scripts | `scripts/test_namecheap_api.py` |
| **GOOGLE_API_KEY** / **GOOGLE_API_KEy** | Google API key (typo variant in code) | Google APIs (e.g. Geocoding / Maps) | Finding partner addresses | `scripts/find_partner_addresses.py` |
| **AWS_ACCESS_KEY_ID** | AWS access key | AWS API auth | Listing Route 53 zones | `scripts/list_route53_zones.py` |
| **AWS_SECRET_ACCESS_KEY** | AWS secret key | AWS API auth | Same | Same |
| **AWS_DEFAULT_REGION** / **AWS_REGION** | AWS region | Region for Route 53 / AWS calls | Same; default `us-east-1` if unset | Same |

---

## 8. jarvis

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **SYSTEM_PROMPT** | System prompt text | Override default LLM system prompt | Local LLM chat app | `app.py` |
| **USE_4BIT** | Boolean | Use 4-bit quantization for local model | Model loading | `app.py` |
| **USE_8BIT_CPU** | Boolean | Use 8-bit on CPU | Model loading | `app.py` |
| **MODEL_NAME** | Model name string | Which local model to load | Model selection | `app.py` |

*Jarvis runs a local LLM; no cloud API keys are required for basic use. These are configuration overrides.*

---

## 9. File-based credentials (no env var)

| Asset | Codebase | What it is | Use case | Where / scenario |
|-------|----------|------------|----------|------------------|
| **google-service-account.json** | truesight_me | Google service account JSON (private key, client email, etc.) | Read Google Sheet "Shipment Ledger Listing" and generate static shipment/impact pages | `scripts/generate-shipment-pages.js`; file path: repo root `google-service-account.json` |

*Do not commit this file. Keep it only in the truesight_me project (or a secure secret store) and reference it from the script.*

---

## Summary by codebase

| Codebase | Credentials / config |
|----------|----------------------|
| **sentiment_importer** | ALPHA_VANTAGE_API_KEY, FMP_API_KEY, POLYGON_API_KEY, IEX_API_KEY, WIX_API_ACCESS_TOKEN, HELLOCASH_PROXY_*, **AGROVERSE_INVENTORY_GAS_WEBAPP_URL**, **AGROVERSE_INVENTORY_PUBLISH_SECRET**, **AGROVERSE_INVENTORY_GAS_ACTION** (optional) |
| **krake_ror** | SENDGRID_API_KEY |
| **video_editor** | GROK_API_KEY, MAX_CONCURRENT_ANALYSIS, PORT |
| **market_research** | GOOGLE_CALENDAR_ID, DEFAULT_TIMEZONE (plus Google OAuth/service account if used) |
| **truesight_me** | WIX_API_KEY, WIX_SITE_ID, WIX_ACCOUNT_ID, google-service-account.json |
| **tokenomics** | QR_CODE_REPOSITORY_TOKEN, GDRIVE_KEY, WIX_ACCESS_TOKEN, GITHUB_TOKEN, GITHUB_ACTIONS; GAS **`update_store_inventory`**: Script property **`AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`** (§6a) |
| **agroverse-inventory** | No workspace `.env`; PAT only in GAS Script properties (**`AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`**) |
| **agroverse_shop** | NAMECHEAP_*, GOOGLE_API_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION |
| **jarvis** | SYSTEM_PROMPT, USE_4BIT, USE_8BIT_CPU, MODEL_NAME (config only) |

---

*Last updated from workspace scan. Credentials were not moved; only variable names and documentation were collected here.*
