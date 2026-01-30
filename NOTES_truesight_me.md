# TrueSight.me — Working Notes (Shared Context for AIs)

Purpose: Quick, actionable reference for Grok/Claude/Codex to understand, maintain, and extend the TrueSight DAO website repo (`/Users/garyjob/Applications/truesight_me`).

## Overview
- Static site (HTML/CSS/JS) deployed via GitHub Pages with custom domain `truesight.me` (`CNAME` present).
- Primary goals: transparency, shipments/pledges pages, impact registry, educational modules, and blog.
- Authoritative data sources: Google Sheets (master), Wix CMS (historical + stats), local assets.

## Core Structure
- Main pages: `index.html` (landing + stats), `agroverse.html`, `sunmint.html`, `edgar.html`, `about-us.html`, `blog/`.
- Generated detail pages:
  - Agroverse shipments → `agroverse-shipments/{agl}/index.html`
  - Sunmint pledges → `sunmint-tree-planting-pledges/{agl}/index.html`
- Data: `data/` (exchange-rates.{js,json}, blog-posts.json, agroverse-shipments.js, edgar-modules.js…)
- Scripts: `scripts/` (Node automations for Google Sheets + Wix + generation)
- Redirects: HTML-only under `redirects/` and hand-written deep links like `ttl/irs/index.html`
- Google Apps Scripts: `google_app_scripts/` (read-only here; logic moved to tokenomics GAS for runtime)

## Data Flow
1) CSV bootstrap (legacy):
- `assets/raw/shipments_collection.csv` + `assets/raw/Agroverse+Shipments_new.csv`
- Merge → upload into Google Sheets tab “Shipment Ledger Listing”

2) Master source of truth: Google Sheets
- Spreadsheet: 1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU
- Tabs used: “Shipment Ledger Listing”, “Performance Statistics”
- Service account: agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com
- Credentials file in repo root: `google-service-account.json` (present locally; do not commit elsewhere)

3) Static generation
- `scripts/generate-shipment-pages.js` reads “Shipment Ledger Listing” → renders clean URLs for shipments/pledges with OG/Twitter meta, Leaflet maps, footer, and accessible markup.
- `scripts/syncAllWixData.js` fetches Wix collections (AgroverseShipments, ExchangeRate, Statistics, EdgarModules) → writes `data/*.js` and `data/exchange-rates.json`, optionally inlines exchange rates inside `index.html`.
- Blog: `scripts/syncBlogPosts.js` fetches Wix Blog → builds `blog/posts/*.html` and `blog/index.html`.

4) Runtime display
- `index.html` loads stats from `data/exchange-rates.json` (and/or inline) to populate cards and charts; Chart.js is used for visuals.

## Key Scripts (Node)
- generate-shipment-pages.js
  - Reads Google Sheet, maps rows via header names, extracts lat/lng from Google Maps URL using robust patterns (`3d...!4d...`, `@lat,lng`, `ll=lat,lng`).
  - Builds meta tags, sanitizes WYSIWYG fragments (removes broken `<link>`/Google Fonts remnants), escapes output.
  - Outputs directory-per-page with `index.html` and shared footer; supports both cacao shipments (`is_cacao_shipment=true`) and serialized pledges (`serialized=true`).
- merge-and-upload-shipments.js
  - Parses multiline CSVs, merges old/new rows by shipment ID, prefers non-empty values, special-cases Google Maps fields.
  - Ensures headers in “Shipment Ledger Listing”; auto-adds columns via Sheets API if needed; preserves existing non-empty cells.
- syncAllWixData.js
  - Generic Wix Data sync: writes JS modules and JSON; updates inlined `exchangeRatesData` in `index.html` when found.
- syncBlogPosts.js
  - Calls Wix Blog v3 API; fetches IDs then each post with `fieldsets=RICH_CONTENT`; converts Ricos format to HTML; builds listing + previous/next navigation.
- populatePerformanceStatistics.js
  - Fetches ExchangeRate from Wix and writes rows to “Performance Statistics” in the Google Sheet (header formatting optional).
- generate-redirects.js / identify-redirects.js
  - From `wix_redirects.csv` and CSVs, produce HTML redirect pages compatible with GitHub Pages (meta refresh + JS + canonical + fallback link).
- Utilities: update-coordinates-from-urls.js, update-cacao-serialized-values.js, upload-shipments-to-sheets.js, add-google-analytics.js.

## Google Apps Scripts (GAS)
- Local files `google_app_scripts/` are documentation. The live logic is consolidated in tokenomics:
  - tokenomics/google_app_scripts/tdg_asset_management/tdg_wix_dashboard.gs
  - Provides `doGet()` web app, `updatePerformanceStatistic()`, and functions that persist Wix metrics into “Performance Statistics”.
- One-time bootstrap present here: `sync_performance_statistics.gs` can populate the sheet from Wix.

## Credentials & Config
- `.env` in this repo (present):
  - WIX_API_KEY, optional WIX_SITE_ID, WIX_ACCOUNT_ID for Wix APIs.
- `google-service-account.json` at repo root for Google Sheets access; client email must match CONFIG and sheet must grant access.
- See `agentic_ai_context/API_CREDENTIALS_DOCUMENTATION.md` for variable roles; no secrets live in context.

## Dependencies
- Node: `dotenv`, `google-auth-library`, `google-spreadsheet`, `googleapis`; dev: `jsdom`, `playwright`.
- Frontend: Chart.js (CDN), Google Fonts, vanilla HTML/CSS.

## Deployment
- GitHub Pages from `main`; `CNAME` ensures custom domain.
- Redirects are HTML files only (no `_redirects`, `.htaccess`, or `vercel.json`). See `docs/GITHUB_PAGES_DEPLOYMENT.md`.
- Pre-deploy checklist in README: regenerate pages, verify redirects, images, mobile responsiveness, and Sheets access.

## Cross-Repo Links
- Tokenomics
  - SCHEMA.md: authoritative sheet structures and names (notably “Shipment Ledger Listing”, “Performance Statistics”).
  - API.md: GAS endpoints for signature/asset APIs powering the DApp and metrics pipeline.
- DApp
  - UX_CONVENTIONS.md: patterns for loading/verification UX mirrored by site interactions.

## Operational Runbooks
- Add/Update shipment
  1) Edit Google Sheet row (set `Is Cacao Shipment` / `Serialized`, add Maps URL & image URL).
  2) `node scripts/generate-shipment-pages.js` to (re)build pages.
  3) Ensure `assets/shipments/{id}.avif` (or gif for AGL7) and URL set to public GitHub raw.
- Sync Wix data/stats
  - `node scripts/syncAllWixData.js` to refresh `data/*` and inline stats.
  - or `node scripts/populatePerformanceStatistics.js` to populate the sheet from Wix.
- Blog import
  - `node scripts/syncBlogPosts.js` with WIX_* in `.env`.
- Redirects
  - Edit `wix_redirects.csv` → `node scripts/generate-redirects.js` (or hand-craft `path/index.html`).
- Local preview
  - `python3 -m http.server 8080` and browse `http://localhost:8080`.

## SEO/Content Notes
- Meta tags generated for shipment/pledge pages include OG/Twitter with fallback image `assets/truesight-logo.png`.
- `stripHtmlAndClean()` aggressively removes broken font/link fragments from WYSIWYG content before meta descriptions.

## Pitfalls & Edge Cases
- Header drift in Sheets: tokenomics/SCHEMA.md notes header line breaks and name changes; scripts here match by exact header text. If headers change, update mapping functions.
- Coordinates: Some Google Maps URLs center the viewport; prefer `3d…!4d…` match; script already prioritizes this.
- Column auto-add: If `google-spreadsheet` cannot expand columns, script attempts a raw `googleapis` batchUpdate; installs `googleapis` on the fly if missing.
- Base URL assumptions: Meta tags assume `https://www.truesight.me` in `generateMetaTags()`.
- Service account mismatch: Script warns if `client_email` != expected; still attempts use.

## Next Improvements (optional)
- Harden header mapping by normalizing whitespace/case (align with SCHEMA.md recommendations).
- Move shared UI fragments (header/footer) to partials and inject at build to avoid duplication.
- Add a small JS health check to surface when exchange-rates JSON is stale versus inline.
- Wire a `npm run build` script that sequences: Wix sync → inline stats → generate pages → redirect generation → validation.

References
- Repo: `/Users/garyjob/Applications/truesight_me`
- Docs in repo: `README.md`, `docs/GITHUB_PAGES_DEPLOYMENT.md`
- Related: `/Users/garyjob/Applications/tokenomics/{API.md, SCHEMA.md}`; `/Users/garyjob/Applications/dapp/UX_CONVENTIONS.md`

## Quick Commands
- Install Node deps
  - `cd /Users/garyjob/Applications/truesight_me && npm install`

- Generate shipment/pledge pages from Google Sheets
  - `node scripts/generate-shipment-pages.js`

- Merge legacy CSVs and upload to Google Sheets
  - `node scripts/merge-and-upload-shipments.js`

- Sync all Wix collections to `data/` (+ inline rates in `index.html`)
  - `node scripts/syncAllWixData.js`

- Populate “Performance Statistics” (Wix → Google Sheet)
  - `node scripts/populatePerformanceStatistics.js`

- Import Wix Blog posts
  - Ensure `.env` has `WIX_API_KEY` (and optionally `WIX_SITE_ID`, `WIX_ACCOUNT_ID`)
  - `node scripts/syncBlogPosts.js`

- Generate redirects from CSV
  - `node scripts/identify-redirects.js`
  - `node scripts/generate-redirects.js`

- Local preview (choose one)
  - `python3 -m http.server 8080`
  - `npx serve .`

- Required local files
  - `google-service-account.json` in repo root (service account must have access to spreadsheet `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`)
  - `.env` with `WIX_API_KEY` for Wix-powered scripts
