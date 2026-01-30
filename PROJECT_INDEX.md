# Project Index — Per-Project Summary for AI Assistants

Quick reference for each project in the workspace. For credential names and usage, see **agentic_ai_api_credentials**.

---

## DAO / Agroverse

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref |
|---------|------|---------|--------|-------------------|------------------|
| **dapp** | `dapp/` | TrueSight DAO DApp: signatures, voting rights, scanner, expenses, feedback | Static HTML/JS, GitHub Pages | `create_signature.html`, `scanner.html`, `UX_CONVENTIONS.md` | — |
| **truesight_me** | `truesight_me/` | TrueSight DAO static site (Wix migration): DAO stats, blog, shipments, Sunmint | HTML/CSS/JS, Google Sheets | `index.html`, `scripts/`, `google_app_scripts/` | WIX_*, google-service-account.json |
| **tokenomics** | `tokenomics/` | DAO tokenomics: Apps Scripts, Python scripts, Raydium market making, schema/API | GAS, Python, TypeScript | `google_app_scripts/`, `python_scripts/`, `API.md`, `SCHEMA.md` | QR_CODE_REPOSITORY_TOKEN, GDRIVE_KEY, WIX_*, GITHUB_* |
| **agroverse_shop** | `agroverse_shop/` | Agroverse e‑commerce (Wix migration): cart, Stripe, blog, farm/shipment pages | Static HTML/JS, Google Apps Scripts | `scripts/`, blog in `post/` | NAMECHEAP_*, GOOGLE_API_KEY, AWS_* |
| **qr_codes** | `qr_codes/` | QR code assets / generation (linked to tokenomics/agroverse) | — | — | — |
| **proposals** | `proposals/` | DAO proposals (minimal content in workspace) | — | `README.md` | — |

---

## Krake / Data Harvesting

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref |
|---------|------|---------|--------|-------------------|------------------|
| **krake_ror** | `krake_ror/` | Krake Rails backend (data harvesting engine) | Ruby 2.6, Rails, PostgreSQL, Redis, Elasticsearch | `rails s`, `lib/tasks/` | SENDGRID_API_KEY |
| **krake_sinatra** | `krake_sinatra/` | Krake Sinatra services | Ruby, Sinatra | — | — |
| **krake_local** | `krake_local/` | Local Krake tools (commander, listener, Chrome listener) | Node/TypeScript | `krake_commander/`, `krake_chrome_listener/` | — |
| **krake_chrome** | `krake_chrome/` | Krake Chrome extension (data harvesting UI) | JS, CoffeeScript, Jasmine | `manifest.json`, `js/`, `spec_j/` | — |

---

## Content & Research

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref |
|---------|------|---------|--------|-------------------|------------------|
| **market_research** | `market_research/` | Content calendars, physical stores, blog/social sync for Agroverse & TrueSight | Python, venv | `physical_stores/`, `online_content/` | GOOGLE_CALENDAR_ID, DEFAULT_TIMEZONE |
| **video_editor** | `video_editor/` | AI video editor: Whisper, YOLO, Grok, YouTube Shorts upload | Python, Flask | `app.py`, `video_queue.py`, `grok_client.py` | GROK_API_KEY, PORT |
| **sentiment_importer** | `sentiment_importer/` | News headlines + stock prices import | Rails, PostgreSQL, Redis, Elasticsearch | `rails s`, workers | ALPHA_VANTAGE_*, FMP_*, POLYGON_*, IEX_*, WIX_*, HELLOCASH_* |
| **garyteh_blog** | `garyteh_blog/` | Personal blog (static or generated) | HTML/JS | — | — |

---

## Infra & Tools

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref |
|---------|------|---------|--------|-------------------|------------------|
| **jarvis** | `jarvis/` | Local LLM web service (e.g. Qwen), FastAPI | Python, FastAPI, Hugging Face | `app.py`, `start.sh` | SYSTEM_PROMPT, MODEL_NAME, USE_4BIT, etc. (config) |
| **read_page** | `read_page/` | Browser extension (read page / content) | JS, manifest | `manifest.json`, `content.js` | — |
| **iching_oracle** | `iching_oracle/` | I Ching oracle app | Node/TypeScript | — | — |
| **point-of-sales-integrations** | `point-of-sales-integrations/` | POS integrations | — | — | — |
| **heierling-pos** | `heierling-pos/` | Heierling POS (small codebase) | HTML/JS | — | — |

---

## Compliance / Biz

| Project | Path | Purpose | Stack | Entry / Key files | Credentials ref |
|---------|------|---------|--------|-------------------|------------------|
| **fda_fsvp** | `fda_fsvp/` | FDA FSVP docs, supplier verification, declarations | PDFs, docs | `public_declarations/`, `suppliers/`, `regulations reference documents/` | — |

---

## Context & Credentials (no code)

| Project | Path | Purpose |
|---------|------|---------|
| **agentic_ai_context** | `agentic_ai_context/` | This repo: workspace context for AIs (`WORKSPACE_CONTEXT.md`, `PROJECT_INDEX.md`, `SUPPLY_CHAIN_AND_FREIGHTING.md` for supply chain/freighting/unit-cost). |
| **agentic_ai_api_credentials** | `agentic_ai_api_credentials/` | Credential **reference** only: `env.template`, `API_CREDENTIALS_DOCUMENTATION.md`. No secrets. |

---

*When adding or removing projects, update both WORKSPACE_CONTEXT.md and this PROJECT_INDEX.md.*
