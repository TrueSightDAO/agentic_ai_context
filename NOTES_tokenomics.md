# Tokenomics — Working Notes (Shared Context for AIs)

Purpose: One-stop reference for the TrueSight DAO tokenomics stack at `/Users/garyjob/Applications/tokenomics` — APIs, Google Apps Scripts, sheet schema, and supporting automation used by the DApp and truesight.me.

## Overview
- Central repo powering DAO tokenomics, data automations, and integrations.
- Surfaces APIs for the DApp (Edgar + Google Apps Script web apps).
- Owns the Google Sheets schema and consolidation of GAS logic (including Performance Statistics web service consumed by truesight.me).

Key docs
- `API.md` — DApp-facing API usage and signing model.
- `API_ENDPOINTS.md` — Consolidated endpoints, webhooks, cron, and module mapping.
- `SCHEMA.md` — Authoritative Google Sheets schema (recent header changes, new sheets, naming conventions).
- `SCHEDULE_TRIGGERS.md` — Time-driven automations and their roles.

## Main Areas
- Google Apps Scripts (`google_app_scripts/`) grouped by domain:
  - tdg_asset_management: expenses, capital injection, recurring tokenization, wallet checks, Stripe, Wix dashboard + web service
  - tdg_inventory_management: sales & movement parsing + web app
  - tdg_identity_management: member signature registration (email/telegram)
  - tdg_scoring: Grok scoring for Telegram/WhatsApp logs and transfer to main ledger
  - tdg_proposal: proposal manager
  - agroverse_qr_codes: QR code web app + generation/update processing + notifications
  - tdg_shipping_planner, sunmint_tree_planting, agroverse_products, wix_workflows, agroverse_site_statistics
- Web services consumed by the DApp: various deployed `doGet` web apps (see Endpoints).
- Python/TS tooling: Raydium market making (TypeScript), LAToken scripts (Python), IRS tax compilation scripts, QR code GitHub webhook utility.

## Google Apps Scripts — Highlights
- tdg_asset_management/tdg_wix_dashboard.gs
  - Consolidates Performance Statistics logic and exposes a `doGet` JSON web service for the website.
  - Updates/syncs: USD_TREASURY_BALANCE, TDG_ISSUED, ASSET_PER_TDG_ISSUED, 30-day sales, etc.
  - AUM calculation including main ledger and all managed ledgers (via Currencies sheet for non-USD asset valuation).
  - Web app URL documented in file header; deploy as Web App with "Anyone" access for public reads.
- tdg_inventory_management/process_*.gs
  - Parse sales and inventory movements from "Telegram Chat Logs" → update respective sheets and ledgers.
- agroverse_qr_codes/web_app.gs
  - List/lookup QR codes; update QR code email/status/member; used by DApp modules.
- Webhook approach
  - Edgar logs to "Telegram Chat Logs", then Sidekiq triggers GAS webhooks to process records.
  - Cron triggers (time-driven) serve as fallback; see SCHEDULE_TRIGGERS.md and API_ENDPOINTS.md.

## APIs and Endpoints
- Edgar (production): `https://edgar.truesight.me`
  - `POST /dao/submit_contribution` (multipart: `text`, optional `attachment`) — primary submission endpoint
  - `HEAD /ping` — health check
  - Optionally: `/dao/verify_signature`, `/dao/link_upc`, `/dao/express_submit_contribution` (see API_ENDPOINTS.md)
- Google Apps Script web apps (examples seen in code)
  - Signature & asset verification: `AKfycbygmwRbyqse-.../exec`
  - QR code API (list/list_all/list_with_members/lookup/update): `AKfycbxigq4-.../exec`
  - DAO form data for lists (members/recipients/ledgers/currencies): `AKfycbztpV3T-.../exec`
  - Proposals web app: `AKfycbzgNstwR-.../exec`
  - Feedback web app: `AKfycbz3FQgXL-.../exec`
  - Performance Statistics JSON (served by tdg_wix_dashboard.gs) — URL referenced in that file header
- All endpoints and deployment notes mapped in `API_ENDPOINTS.md`.

## Schema — SCHEMA.md Snapshot
- Authoritative reference for sheet structures; recent changes include headers with line breaks and new/renamed columns.
- Key tabs used cross-repo:
  - Main ledger: `Ledger history`, `offchain transactions`, `off chain asset balance`, `Performance Statistics`, `Currencies`, `Shipment Ledger Listing`, `Monthly Statistics`, etc.
  - Telegram & Submissions: `Telegram Chat Logs`, `Scored Expense Submissions`, `Capital Injection`, `QR Code Sales`, `Inventory Movement`, `QR Code Generation`, `Proposal Submissions`, `SunMint Tree Planting`, `Document Notarizations`, `States`.
  - Managed AGL Ledgers: dynamic list of ledgers and their URLs.
- Validation utility: `python_scripts/schema_validation/test_schema_validation.py` checks IDs, sheet names, headers, and (optionally) Wix collection items.

## Supporting Tools
- IRS tax compilation (`irs_tax_compilation/`)
  - Extracts USD sales/expenses from main + managed ledgers for a target tax year and writes to a dedicated spreadsheet.
  - Service account: `irs-tax-filing@get-data-io.iam.gserviceaccount.com`; local `credentials.json` required.
- QR code GitHub webhook service (`agroverse_qr_code_web_service/`)
  - Generates QR images, uploads to `TrueSightDAO/qr_codes` via PAT (`QR_CODE_REPOSITORY_TOKEN`), and ties back to Sheets.
  - Can read Google Sheets via `GDRIVE_KEY` (JSON in env) or local credentials file.
- Market making
  - `raydium_market_making/raydium_type_script` (TypeScript, Node >=18) for Raydium buyback scripts.
  - `la_token_market_making_python` for LAToken; includes `requirements.txt` and helper modules.
- Python scoring notebooks (`python_scripts/`)
  - Jupyter notebooks for TDG awards and AGL sales scoring; `requirements.txt` under python_scripts.

## Credentials & Env
- See `agentic_ai_context/API_CREDENTIALS_DOCUMENTATION.md` for variable names and usage.
- Common:
  - `QR_CODE_REPOSITORY_TOKEN` — PAT for qr_codes repo uploads (QR code web service)
  - `GDRIVE_KEY` — Google service account JSON (string) for Sheets access in GitHub Actions
  - Wix: `WIX_ACCESS_TOKEN` / `WIX_API_KEY` (GAS properties or local .env for scripts consuming Wix)
- Never commit secrets. GAS script properties store Wix tokens; local scripts use `.env` or environment variables.

## Quick Commands
- Run schema validation (service account or OAuth creds required)
  - `cd /Users/garyjob/Applications/tokenomics/python_scripts`
  - `pip install -r requirements.txt`
  - Optional: `export WIX_ACCESS_TOKEN=...`
  - `python python_scripts/schema_validation/test_schema_validation.py`

- IRS tax compilation
  - `cd /Users/garyjob/Applications/tokenomics/irs_tax_compilation`
  - `python3 -m venv venv && source venv/bin/activate`
  - `pip install -r requirements.txt`
  - Place `credentials.json` here (service account) and run `python3 irs_tax_compiler.py`

- QR code webhook utility (local test)
  - `cd /Users/garyjob/Applications/tokenomics/agroverse_qr_code_web_service`
  - `python3 -m venv venv && source venv/bin/activate`
  - `pip install -r requirements.txt`
  - Set `QR_CODE_REPOSITORY_TOKEN` and optionally `GDRIVE_KEY` in environment or `.env`
  - Run tests: `pytest -q` or scripts in repo (see README.md)

- Raydium TS scripts
  - `cd /Users/garyjob/Applications/tokenomics/raydium_market_making/raydium_type_script`
  - `npm install`
  - `npx ts-node buyback_sol_to_tdg.ts` (configure `config.ts` as needed)

## Pitfalls & Tips
- SCHEMA drift: Scripts often match headers by exact text; line breaks and renames can break mappings. Normalize headers where possible or update mappings promptly.
- Endpoints are hardcoded in multiple DApp files; when changing a GAS URL, update DApp pages and `API_ENDPOINTS.md`.
- GAS web apps should read from Sheets (not URL params) to avoid injection; this pattern is already followed.
- For AUM: non-USD assets depend on `Currencies` sheet; ensure entries exist and are priced in USD.

## Next Improvements (optional)
- Centralize endpoint configuration into a small JSON/JS consumed by both DApp and docs to avoid drift.
- Add a smoke test script that pings all deployed GAS web apps and verifies JSON shape.
- Harden header handling utilities to tolerate whitespace/casing/line breaks across all scripts.

References
- Repo: `/Users/garyjob/Applications/tokenomics`
- Primary docs: `API.md`, `API_ENDPOINTS.md`, `SCHEMA.md`, `SCHEDULE_TRIGGERS.md`
- Related repos: `/Users/garyjob/Applications/dapp`, `/Users/garyjob/Applications/truesight_me`
