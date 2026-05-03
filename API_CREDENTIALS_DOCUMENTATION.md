# API Credentials Documentation

This document describes every API credential (and credential-like config) found across the workspace: **what it is used for**, **how** (use case), **where** (scenario), and **which codebase** uses it. Credentials are **not** moved here; they remain in each project. This repo holds a **reference template** (`env.template`) and this documentation only.

---

## 1. sentiment_importer

**Deployment:** Production Rails app (“Edgar”) is **`https://edgar.truesight.me`**. **`https://getdata.io`** is a **different** codebase — **krake_ror** ([KrakeIO/krake_ror](https://github.com/KrakeIO/krake_ror)); do not conflate hosts or credentials.

| Variable | What it is | Use case | Where / scenario | Code location |
|----------|------------|----------|------------------|----------------|
| **ALPHA_VANTAGE_API_KEY** | Alpha Vantage API key | Fetch company overview/fundamentals by stock symbol | Background worker refreshing company data; fallback when FMP/Polygon/IEX fail | `app/workers/company_fundamentals_refresher.rb` |
| **FMP_API_KEY** | Financial Modeling Prep API key | Fetch company profile by symbol | Same worker; primary or fallback source for company fundamentals | `app/workers/company_fundamentals_refresher.rb` |
| **POLYGON_API_KEY** | Polygon.io API key | Fetch company metadata by symbol | Same worker; company data refresh (config fallback: `config.polygon_api_key`) | `app/workers/company_fundamentals_refresher.rb` |
| **IEX_API_KEY** | IEX Cloud API key | Fetch company info by symbol | Same worker; company fundamentals (config fallback: `config.iex_api_key`) | `app/workers/company_fundamentals_refresher.rb` |
| **WIX_API_ACCESS_TOKEN** | Wix API access token | Wix CMS / API access in tests | Test environment only; Wix integration tests | `config/environments/test.rb` |
| **HELLOCASH_PROXY_ENABLED** | Boolean flag | Enable HelloCash API via proxy | Development; when calling HelloCash through an AWS proxy | `config/environments/development.rb` |
| **HELLOCASH_PROXY_HOST** | Proxy host (e.g. AWS IP) | Host for HelloCash proxy | Development; optional override for proxy server | `config/environments/development.rb` |

### sentiment_importer — production URL and Agroverse-facing HTTP (not secrets)

| Item | Detail |
|------|--------|
| **Production base URL** | **`https://edgar.truesight.me`** — deployed **sentiment_importer** (“Edgar”). |
| **Agroverse Shop checkout shipping** | **`GET /agroverse_shop/shipping_rates`** — query: **`weightOz`**, **`shippingAddress`** (JSON string), optional **`environment`**. Returns USPS options via EasyPost (mirrors GAS `calculateShippingRates`). Browser **`fetch`** from **agroverse.shop** / beta; **rack-cors** on Edgar allows cross-origin access. Shop sets origin in **`agroverse_shop/js/config.js`** → **`shippingRatesApiOrigin`**. |
| **Agroverse inventory snapshot (Sidekiq → GAS → GitHub JSON)** | Env on Edgar: **`AGROVERSE_INVENTORY_GAS_WEBAPP_URL`**, **`AGROVERSE_INVENTORY_PUBLISH_SECRET`**, optional **`AGROVERSE_INVENTORY_GAS_ACTION`**. Worker: **`AgroverseInventorySnapshotPublishWorker`**. |

EasyPost for rate quotes uses **`EASYPOST_API_KEY`** (or `config.easypost_api` in environment files); same code path as **`ShippingCalculatorService`**.

---

## 2. krake_ror

**Deployment:** Production Rails app is **`https://getdata.io`**. **Not** **sentiment_importer** / Edgar (**`edgar.truesight.me`** — [TrueSightDAO/sentiment_importer](https://github.com/TrueSightDAO/sentiment_importer)).

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
| **sentiment_importer** | ALPHA_VANTAGE_API_KEY, FMP_API_KEY, POLYGON_API_KEY, IEX_API_KEY, WIX_API_ACCESS_TOKEN, HELLOCASH_PROXY_*, EASYPOST_API_KEY, **AGROVERSE_INVENTORY_*** (production on **`https://edgar.truesight.me`**) |
| **krake_ror** | SENDGRID_API_KEY |
| **video_editor** | GROK_API_KEY, MAX_CONCURRENT_ANALYSIS, PORT |
| **market_research** | GOOGLE_CALENDAR_ID, DEFAULT_TIMEZONE (plus Google OAuth/service account if used) |
| **truesight_me** | WIX_API_KEY, WIX_SITE_ID, WIX_ACCOUNT_ID, google-service-account.json |
| **tokenomics** | QR_CODE_REPOSITORY_TOKEN, GDRIVE_KEY, WIX_ACCESS_TOKEN, GITHUB_TOKEN, GITHUB_ACTIONS |
| **agroverse_shop** | NAMECHEAP_*, GOOGLE_API_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION |
| **jarvis** | SYSTEM_PROMPT, USE_4BIT, USE_8BIT_CPU, MODEL_NAME (config only) |

---

## 10. Credential Permission Audit (2026-05-03)

Live probe results for credentials used by automation. **Future AIs:** consult this before assuming a credential can read/write/create.

### 10.1 Gmail OAuth (`market_research/credentials/gmail/token.json`)

| Attribute | Value |
|---|---|
| **Account** | `garyjob@agroverse.shop` |
| **Client ID** | `667737028020-2ihjpbnq119st9v9b9f4kh6vvkrc4hco.apps.googleusercontent.com` (GCP project `get-data-io`) |
| **Scopes** | `https://www.googleapis.com/auth/gmail.modify` |
| **Refresh token** | ✅ Present (len 103) |
| **Access token expiry** | Short-lived; library auto-refreshes via `token_uri` |
| **Capabilities** | Read/search mail, send mail, create drafts, manage labels |
| **CI usage** | Paste full JSON into `GMAIL_TOKEN_JSON` secret; refresh token persists until revoked |
| **Limitations** | Cannot access other Google Workspace accounts; app in Testing mode requires `garyjob@agroverse.shop` as test user |

**Verdict:** ✅ **Ready for autopilot email monitoring.** The refresh token is active and `gmail.modify` covers reading failure emails + sending replies.

### 10.2 GitHub PAT (`market_research/.env` → `GITHUB_PAT`)

| Attribute | Value |
|---|---|
| **Type** | Fine-grained personal access token |
| **Owner** | `garyjob` (user account, not a bot) |
| **Rate limit** | 5,000/hour (personal tier) |
| **Read access** | ✅ All 25+ `TrueSightDAO/*` repos visible |
| **Write access — `TrueSightDAO/.github`** | ✅ Confirmed (PUT file + DELETE probe succeeded) |
| **Write access — `TrueSightDAO/go_to_market`** | ❌ **DENIED** — "Resource not accessible by personal access token" |
| **Write access — `TrueSightDAO/ecosystem_change_logs`** | ❌ **DENIED** — same error |
| **Write access — branch create / PR open** | ❌ **DENIED** on `go_to_market` (and likely any repo not explicitly granted) |

**Verdict:** ⚠️ **Partially ready.** The PAT can write to `.github` but **cannot open PRs on `go_to_market`** (the repo with the most Actions/workflows). For `truesight_autopilot` to open code-fix PRs, you must either:

1. **Regenerate the fine-grained PAT** and add `Contents: Read + Write` + `Pull requests: Read + Write` on `TrueSightDAO/go_to_market` (and any other repo the autopilot should edit), or
2. **Create a dedicated bot account** (`truesight-autopilot` or similar), invite it as a collaborator to the repos, and issue a PAT from that account.

### 10.3 AWS Credentials

| Source | Status | Details |
|---|---|---|
| `~/.aws/credentials` (default profile) | ❌ **INVALID** | `InvalidClientTokenId` — credentials rotated or belong to a deactivated user |
| `~/.aws/credentials` (`[nelan]` profile) | Unknown | Not probed |
| Environment vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) | ❌ **INVALID** | Same error; may conflict with ~/.aws credentials |
| `agroverse_shop` scripts | ❌ **INVALID** | Same keys, same error |

**Verdict:** ❌ **Not ready for autopilot.** All AWS credentials in the workspace are invalid. To monitor EC2 health and costs, you must:

1. **Rotate AWS credentials** in `~/.aws/credentials` and `.env` files, or
2. **Attach an IAM role** to the EC2 instance running `governor_chatbot_service` so the autopilot can use instance-profile credentials (no long-lived keys needed).

Recommended IAM policy for EC2 monitoring: `CloudWatchReadOnlyAccess` + `CostExplorerReadOnlyAccess` + `AWSHealthFullAccess`.

### 10.4 dao_client Edgar Signing Keys (`dao_client/.env`)

| Attribute | Value |
|---|---|
| **Identity** | Personal (`Gary Teh`) |
| **Keys** | RSA-2048 SPKI/PKCS#8 in `.env` |
| **Usage** | `truesight-dao-report-contribution`, all `truesight-dao-*` CLI tools |

**Verdict:** ⚠️ **Do NOT use for autopilot.** These are personal DAO identity keys. The autopilot should have its own keypair:

1. Generate new RSA keypair (`truesight-dao-auth login` with a new `.env` path)
2. Register with Edgar as `autopilot@agroverse.shop` (or similar)
3. Store only the autopilot `.env` on the EC2

### 10.5 GCP Service Accounts

| Service Account | File location(s) | Project | Verified access |
|---|---|---|---|
| `agroverse-market-research@get-data-io.iam.gserviceaccount.com` | `market_research/google_credentials.json`, `krake_local/google-service-account.json` | `get-data-io` | Assumed (used daily by scripts) |
| `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com` | `agroverse_shop/google-service-account.json`, `truesight_me/google-service-account.json` | `get-data-io` | Assumed |
| `cypher-defense@get-data-io.iam.gserviceaccount.com` | `sentiment_importer/config/cypher_defense_gdrive_key.json` | `get-data-io` | Assumed |
| `edgar-dapp-listener@get-data-io.iam.gserviceaccount.com` | `sentiment_importer/config/edgar_dapp_listener_key.json` | `get-data-io` | ✅ Confirmed Editor on Hit List |
| `tdg-scoring-peer-reviewer@get-data-io.iam.gserviceaccount.com` | `sentiment_importer/config/tdg_scoring_gdrive_key.json` | `get-data-io` | Assumed |
| `upc-barcode@get-data-io.iam.gserviceaccount.com` | `sentiment_importer/config/upc_barcode_gdrive_key.json` | `get-data-io` | Assumed |
| `truesightme-whitepapers@get-data-io.iam.gserviceaccount.com` | `truesight_me/credentials/whitepaper-google-sa.json` | `get-data-io` | Assumed (Viewer on whitepaper docs) |

**Verdict:** ✅ **Ready for sheet access.** No live probe performed (would require API calls), but all are actively used. For GCP billing/monitoring, you need a separate service account with `monitoring.viewer` + `billing.accounts.getSpendingInformation` on the `get-data-io` billing account.

### 10.6 Governor Chatbot Service EC2

| Attribute | Value |
|---|---|
| **Region** | `us-east-1` |
| **Instance type** | t3.small (recommended) or t3.micro |
| **IAM role** | Unknown — IMDS not accessible from this machine |
| **Current services** | `governor-chatbot.service` (systemd) |
| **Proposed addition** | `truesight-autopilot.service` (same EC2, second systemd unit) |

**Verdict:** ⚠️ **Needs IAM role check.** SSH into the EC2 and run `curl http://169.254.169.254/latest/meta-data/iam/info` to verify the instance profile. If none exists, attach one with `CloudWatchReadOnlyAccess` + `CostExplorerReadOnlyAccess`.

---

*Last updated from workspace scan. Credentials were not moved; only variable names and documentation were collected here.*
