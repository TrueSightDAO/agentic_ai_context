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
| **sentiment_importer** | ALPHA_VANTAGE_API_KEY, FMP_API_KEY, POLYGON_API_KEY, IEX_API_KEY, WIX_API_ACCESS_TOKEN, HELLOCASH_PROXY_* |
| **krake_ror** | SENDGRID_API_KEY |
| **video_editor** | GROK_API_KEY, MAX_CONCURRENT_ANALYSIS, PORT |
| **market_research** | GOOGLE_CALENDAR_ID, DEFAULT_TIMEZONE (plus Google OAuth/service account if used) |
| **truesight_me** | WIX_API_KEY, WIX_SITE_ID, WIX_ACCOUNT_ID, google-service-account.json |
| **tokenomics** | QR_CODE_REPOSITORY_TOKEN, GDRIVE_KEY, WIX_ACCESS_TOKEN, GITHUB_TOKEN, GITHUB_ACTIONS |
| **agroverse_shop** | NAMECHEAP_*, GOOGLE_API_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION |
| **jarvis** | SYSTEM_PROMPT, USE_4BIT, USE_8BIT_CPU, MODEL_NAME (config only) |

---

*Last updated from workspace scan. Credentials were not moved; only variable names and documentation were collected here.*
