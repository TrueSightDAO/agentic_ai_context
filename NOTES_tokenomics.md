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

### Google Apps Script — `clasp push` and Web App deploy (assistant convention)

After running **`clasp push`** from any `tokenomics/clasp_mirrors/<scriptId>/` folder, **always** tell the user:

1. **Script editor URL** (open project, then **Deploy → Manage deployments** if the change must go live for a Web App or API):

| Project | Script ID | Editor URL |
|---------|-----------|------------|
| **Agroverse QR web app** (DApp `AKfycbxigq4…/exec`, list/lookup/Stripe sessions) | `1y6JVYwqdrFD4zHT4zyIfU762RRsW7GgZKPVuzorpwUS61mDnFQZ65Qsz` | https://script.google.com/home/projects/1y6JVYwqdrFD4zHT4zyIfU762RRsW7GgZKPVuzorpwUS61mDnFQZ65Qsz/edit |
| **Parse Telegram / QR sales** (`process_sales_telegram_logs`, webhook `parseTelegramChatLogs`) | `1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7` | https://script.google.com/home/projects/1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/edit |
| **QR Code Generation** (`processQRCodeGenerationTelegramLogs`, Telegram → Agroverse → GitHub sync) | `1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn` | https://script.google.com/home/projects/1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn/edit |

2. **`clasp push` updates project code only.** For **Web App** deployments, Google often requires **Manage deployments → Edit (pencil) → New version → Deploy** so the public `/exec` URL serves the latest code. (Same deployment entry keeps the same URL.)

3. **`Version.gs` on every push.** Every clasp mirror under `tokenomics/clasp_mirrors/<scriptId>/` should include **`Version.gs`** (tracked in git) so deploy time and changelog survive in the Apps Script project.
   - **Sales / `[SALES EVENT]` / Parse Telegram + ledgers:** bump and copy **`google_app_scripts/tdg_inventory_management/Version.gs`** into the mirrors that already use it (`1dsWec…`, `1wmgYP…`, `1duQFf…`). Run **`getTdgInventoryDeployInfo()`** in the editor to read it back.
   - **QR Code Generation** (`1N6o00…`): bump and copy **`google_app_scripts/agroverse_qr_codes/Version.gs`** ( **`getAgroverseQRGenerationDeployInfo()`** ).
   - **All other mirrors:** use **`google_app_scripts/_clasp_default/Version.gs`** ( **`getClaspMirrorDeployInfo()`** ), or replace with a domain-specific file when that project deserves its own changelog.
   - After **`clasp clone`** / new mirror folder: run **`node scripts/ensure_clasp_version_gs.mjs`** from `tokenomics/` root to add missing **`Version.gs`** (dry-run: same command with **`--dry-run`**).

4. **Sync before push:** Canonical sources live under `google_app_scripts/`; mirrors are pushed with clasp. From repo root, copy then push, e.g.:

```bash
cp google_app_scripts/agroverse_qr_codes/web_app.gs "clasp_mirrors/1y6JVYwqdrFD4zHT4zyIfU762RRsW7GgZKPVuzorpwUS61mDnFQZ65Qsz/Code.js"
cp google_app_scripts/_clasp_default/Version.gs "clasp_mirrors/1y6JVYwqdrFD4zHT4zyIfU762RRsW7GgZKPVuzorpwUS61mDnFQZ65Qsz/Version.gs"
cp google_app_scripts/tdg_inventory_management/process_sales_telegram_logs.gs "clasp_mirrors/1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/Parse Telegram ChatLogs.js"
cp google_app_scripts/tdg_inventory_management/Version.gs "clasp_mirrors/1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/Version.gs"
cp google_app_scripts/agroverse_qr_codes/process_qr_code_generation_telegram_logs.gs "clasp_mirrors/1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn/Code.js"
cp google_app_scripts/agroverse_qr_codes/Version.gs "clasp_mirrors/1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn/Version.gs"
```

### Stripe checkout ↔ Agroverse QR (column P)

- Spreadsheet **`Stripe Social Media Checkout ID`** (main ledger workbook `1GE7PUq…`): **Column P = Agroverse QR code** links a Stripe session row to the serialized QR (`Agroverse QR codes` column A). **C** = Session ID, **N** = tracking.
- Unassigned sessions (P blank) are listed for the Sales Reporter; successful `[SALES EVENT]` processing can set **N** and **P** via `updateStripeCheckoutMetadata` in `process_sales_telegram_logs.gs`. See **`SCHEMA.md`** (recent changes + Stripe sheet table).

### Agroverse QR codes tab — `Currency` (column I) and regional ids

- **Canonical playbook (agents):** **`AGROVERSE_QR_CODE_BATCH_GENERATION.md`** in this repo — end-to-end **sheet columns A–V**, **K** `compiled_` GitHub URL formula, **`batch_compiler.py`** command, venv path, **`to_print/`** clearing, and Sheets API notes.
- **Workbook:** [TrueSight DAO Contribution Ledger](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit) — tab **`Agroverse QR codes`** ([gid=472328231](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit?gid=472328231)).
- **Column I (`Currency`):** Must stay consistent with **`Currencies` column A** in the **same** spreadsheet (operator uses an **external reference** / **`IMPORTRANGE`**-style link so the displayed value is exactly the canonical **`Currencies`!A** string). Sales and ledger logic treat that as the inventory/currency identity; do not paste freeform marketing copy in **I** unless it already exists as a **`Currencies`** row.
- **Column A (`qr_code`):** Short serialized id embedded in check URLs and printed on compiled labels. **Regional handout convention (operator):** e.g. `AUSTIN_CC_20260317_6` — **`CC`** = **ceremonial cacao**, **`CT`** = **cacao tea**; **Los Angeles** promos use the **`LA`** token (not `LOSANGELES`). Keep **A** compact (see **`batch_compiler.py`** `MAX_RECOMMENDED_QR_LENGTH` in tokenomics).
- **Local batch images:** `tokenomics/python_scripts/agroverse_qr_code_generator/batch_compiler.py` pulls **A–H** from the sheet (not column **I**); **`Currencies`** linkage is still required in the sheet for anything that consumes **I** downstream.

## Main Areas
- **Google Apps Script — canonical on disk for clasp:** `tokenomics/clasp_mirrors/<scriptId>/` (one folder per project). Use `clasp push` / `clasp pull` there after a fresh clone. **Git does not store** mirror `*.js` or `appsscript.json` (secrets / noise); the repo keeps `.clasp.json` + checklist + manifest. Regenerate: `node scripts/clone_clasp_mirrors.mjs` from tokenomics root.
- **Reference layout:** `google_app_scripts/` — same logic grouped by domain for reading and docs; **not** the primary clasp root after 2026-03. Backport from mirrors if thematic folders should reflect production.
- Domains under `google_app_scripts/` (reference paths):
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
