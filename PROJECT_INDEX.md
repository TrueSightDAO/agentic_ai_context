# Project Index — Per-Project Summary for AI Assistants

Quick reference for each project in the workspace. For credential names and usage, see **agentic_ai_api_credentials**.  
**GitHub:** Clone URLs so future AIs can pull repos (`git clone <URL>`). See also **WORKSPACE_CONTEXT.md** §6 (production domains) and §7 (repo locations).

---

## DAO / Agroverse

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref | GitHub |
|---------|------|---------|--------|-------------------|------------------|--------|
| **dapp** | `dapp/` | TrueSight DAO DApp: signatures, voting rights, scanner, expenses, feedback | Static HTML/JS, GitHub Pages, Node (tests) | `create_signature.html`, `scanner.html`, `report_dao_expenses.html`, `expense-form-utils.js`, `UX_CONVENTIONS.md`, `tests/README.md`, `.github/workflows/ci.yml` | — | [TrueSightDAO/dapp](https://github.com/TrueSightDAO/dapp) |
| **truesight_me** | `truesight_me/` | TrueSight DAO static site (Wix migration): DAO stats, blog, shipments, Sunmint. **truesight.me** deployed from **truesight_me_prod** | HTML/CSS/JS, Google Sheets | `index.html`, `scripts/`, `google_app_scripts/` | WIX_*, google-service-account.json | [TrueSightDAO/truesight_me](https://github.com/TrueSightDAO/truesight_me) · Prod: [truesight_me_prod](https://github.com/TrueSightDAO/truesight_me_prod) |
| **tokenomics** | `tokenomics/` | DAO tokenomics: Apps Scripts, Python scripts, Raydium market making, schema/API. **Note:** LATOKEN market making on hold (disabled in code). Wix integration deprecated. | GAS, Python, TypeScript | `google_app_scripts/`, `python_scripts/`, `API.md`, `SCHEMA.md` | QR_CODE_REPOSITORY_TOKEN, GDRIVE_KEY, WIX_* (deprecated), GITHUB_* | [TrueSightDAO/tokenomics](https://github.com/TrueSightDAO/tokenomics) |
| **agroverse_shop** | `agroverse_shop/` | Agroverse e‑commerce (Wix migration): cart, Stripe, blog, farm/shipment pages. `agl15/` redirects to AGL15 Google Sheet ledger. **agroverse.shop** deployed from **agroverse_shop_prod**. **Important:** See `docs/PRODUCT_CREATION_CHECKLIST.md` when creating new products to prevent Merchant Center URL mismatches. **⚠️ SETUP REQUIRED:** See `docs/SECURITY.md` — requires credential files: `google-service-account.json`, `scripts/youtube_credentials.json`, `scripts/youtube_token.json` (NEVER commit these; prompt user during setup). | Static HTML/JS, Google Apps Scripts, Node (tests) | `scripts/`, blog in `post/`, `shipments/`, `agl15/`, `tests/README.md`, `playwright.config.ts`, `.github/workflows/visual-consistency.yml`, `docs/PRODUCT_CREATION_CHECKLIST.md`, `docs/SECURITY.md` | NAMECHEAP_*, GOOGLE_API_KEY, AWS_* | [TrueSightDAO/agroverse_shop_beta](https://github.com/TrueSightDAO/agroverse_shop_beta) · Prod: [agroverse_shop_prod](https://github.com/TrueSightDAO/agroverse_shop_prod) |
| **qr_codes** | `qr_codes/` | QR code assets / generation (linked to tokenomics/agroverse) | — | — | — | — |
| **proposals** | `proposals/` | DAO proposals (minimal content in workspace) | — | `README.md` | — | — |

---

## Krake / Data Harvesting

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref | GitHub |
|---------|------|---------|--------|-------------------|------------------|--------|
| **krake_ror** | `krake_ror/` | Krake Rails backend (data harvesting engine) | Ruby 2.6, Rails, PostgreSQL, Redis, Elasticsearch | `rails s`, `lib/tasks/` | SENDGRID_API_KEY | [KrakeIO/krake_ror](https://github.com/KrakeIO/krake_ror) |
| **krake_sinatra** | `krake_sinatra/` | Krake Sinatra services | Ruby, Sinatra | — | — | [KrakeIO/krake_sinatra](https://github.com/KrakeIO/krake_sinatra) |
| **krake_local** | `krake_local/` | Local Krake tools (commander, listener, Chrome listener) | Node/TypeScript | `krake_commander/`, `krake_chrome_listener/` | — | — |
| **krake_chrome** | `krake_chrome/` | Krake Chrome extension (data harvesting UI) | JS, CoffeeScript, Jasmine | `manifest.json`, `js/`, `spec_j/` | — | [KrakeIO/Chrome](https://github.com/KrakeIO/Chrome) |

---

## Content & Research

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref | GitHub |
|---------|------|---------|--------|-------------------|------------------|--------|
| **market_research** | `market_research/` | Content calendars, physical stores, blog/social sync for Agroverse & TrueSight | Python, venv | `physical_stores/`, `online_content/` | GOOGLE_CALENDAR_ID, DEFAULT_TIMEZONE | [TrueSightDAO/content_schedule](https://github.com/TrueSightDAO/content_schedule) |
| **video_editor** | `video_editor/` | AI video editor: Whisper, YOLO, Grok, YouTube Shorts upload | Python, Flask | `app.py`, `video_queue.py`, `grok_client.py` | GROK_API_KEY, PORT | — |
| **sentiment_importer** (Edgar) | `sentiment_importer/` | **Edgar** (edgar.truesight.me): DAO API (submit_contribution, proposals, votes); news/stock import | Rails, PostgreSQL, Redis, Elasticsearch, Sidekiq | `rails s`, workers, `dao_controller.rb` | ALPHA_VANTAGE_*, FMP_*, POLYGON_*, IEX_*, WIX_*, HELLOCASH_* | — |
| **garyteh_blog** | `garyteh_blog/` | Personal blog (static or generated) | HTML/JS | — | — | — |

---

## Infra & Tools

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref | GitHub |
|---------|------|---------|--------|-------------------|------------------|--------|
| **jarvis** | `jarvis/` | Local LLM web service (e.g. Qwen), FastAPI | Python, FastAPI, Hugging Face | `app.py`, `start.sh` | SYSTEM_PROMPT, MODEL_NAME, USE_4BIT, etc. (config) | — |
| **read_page** | `read_page/` | Browser extension (read page / content) | JS, manifest | `manifest.json`, `content.js` | — | — |
| **iching_oracle** | `iching_oracle/` | I Ching oracle app | Node/TypeScript | — | — | — |
| **point-of-sales-integrations** | `point-of-sales-integrations/` | POS integrations | — | — | — | — |
| **heierling-pos** | `heierling-pos/` | Heierling POS (small codebase) | HTML/JS | — | — | — |

---

## Compliance / Biz

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref | GitHub |
|---------|------|---------|--------|-------------------|------------------|--------|
| **fda_fsvp** | `fda_fsvp/` | FDA FSVP docs, supplier verification, declarations | PDFs, docs | `public_declarations/`, `suppliers/`, `regulations reference documents/` | — | — |

---

## Context & Credentials (no code)

| Project | Path | Purpose | GitHub |
|---------|------|---------|--------|
| **agentic_ai_context** | `agentic_ai_context/` | This repo: workspace context for AIs (`WORKSPACE_CONTEXT.md`, `PROJECT_INDEX.md`, `SUPPLY_CHAIN_AND_FREIGHTING.md` for supply chain/freighting/unit-cost). | [TrueSightDAO/agentic_ai_context](https://github.com/TrueSightDAO/agentic_ai_context) |
| **agentic_ai_api_credentials** | `agentic_ai_api_credentials/` | Credential **reference** only: `env.template`, `API_CREDENTIALS_DOCUMENTATION.md`. No secrets. | — |

---

*When adding or removing projects, update both WORKSPACE_CONTEXT.md and this PROJECT_INDEX.md.*
