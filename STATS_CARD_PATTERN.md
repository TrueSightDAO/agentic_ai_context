# TrueSight Stats Card Pattern

A reusable architecture for exposing DAO statistics on the truesight.me landing page, with a detail page backed by a JSON cache.

## The Pattern (5 Layers)

```
GAS Endpoint → Python Script → JSON Cache → Detail Page → Stat Card
```

### 1. GAS Endpoint (Google Apps Script)

**Location:** `tokenomics/google_app_scripts/tdg_asset_management/`

The GAS script exposes a `doGet()` web service that returns Performance Statistics as JSON. Every new stat key added to `syncAllPerformanceStatistics()` is automatically served.

**Key requirements:**
- Add the stat key to `syncAllPerformanceStatistics()` so it writes to the Performance Statistics sheet
- Expose a `?action=triggerSync` handler in `doGet()` so the cache can be refreshed remotely

**Example:** `BUY_BACK_RESERVE` reads from the "off chain asset balance" sheet row "USD - provisions for voting rights cash out".

### 2. Python Script (Cache Builder)

**Location:** `tokenomics/python_scripts/tdg_asset_management/`

A Python script that reads data (from the GAS endpoint or directly from Google Sheets via a service account) and writes a structured JSON file to the `treasury-cache` repo.

**Key requirements:**
- Uses the Cypher Defense service account (`GOOGLE_SERVICE_ACCOUNT_JSON`) for sheet access
- Writes output to the current working directory (the GitHub Actions runner's checkout)
- Does NOT handle git commit/push — that's the workflow's job
- Handles negative amounts (ledger debits) by converting to positive display values

**Example:** `update_buy_back_reserve_cache.py` reads the offchain transactions sheet, aggregates daily buy-back provisions, and writes `buy-back-reserve.json`.

### 3. JSON Cache (GitHub Repo)

**Location:** `treasury-cache/`

An API-only data repo that stores the generated JSON files. Each stat gets its own file.

**GitHub Action workflow:** `treasury-cache/.github/workflows/`
- Runs on a daily cron schedule (e.g. 06:00 UTC)
- Can also be triggered manually from the Actions tab
- Checks out `tokenomics` repo, runs the Python script, then commits the output to `treasury-cache`
- Uses `GH_PAT_TOKEN` for the git push (not the default `GITHUB_TOKEN`)

**Example:** `update-buy-back-reserve-cache.yml` runs `update_buy_back_reserve_cache.py` daily.

### 4. Detail Page (truesight.me)

**Location:** `truesight_me_beta/` (synced to `truesight_me_prod`)

A standalone HTML page at `/stat-name/` that loads data from the JSON cache (fast, from GitHub CDN) with a fallback to the GAS endpoint.

**Key requirements:**
- Loads from `https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/<file>.json` first
- Falls back to the GAS Performance Statistics endpoint if cache is unavailable
- Shows current value, last updated timestamp, and methodology explanation
- Links back to the homepage stats section

**Example:** `buy-back-reserve/index.html`

### 5. Stat Card (Homepage)

**Location:** `truesight_me_beta/index.html`

A stat card in the stats grid on the truesight.me homepage. Links to the detail page.

**Key requirements:**
- Uses `data-key="STAT_KEY"` attribute for the JavaScript to populate the value
- Links to `/stat-name/` for the detail page
- Add a `case 'STAT_KEY':` in the `formatStatValue()` JavaScript function
- If it's the 7th+ card, add `stat-card-hidden` class (hidden behind "Show More Stats")

**Example:**
```html
<div class="stat-card stat-card-hidden" id="stat-card-7">
  <a href="buy-back-reserve/" class="stat-link">
    <h3>Accumulated Buy-Back Reserve</h3>
    <p class="stat-value" data-key="BUY_BACK_RESERVE">&mdash;</p>
  </a>
</div>
```

## Adding a New Stat Card (Checklist)

1. **GAS:** Add the key to `syncAllPerformanceStatistics()` in the GAS script
2. **Python:** Create a cache builder script in `tokenomics/python_scripts/tdg_asset_management/`
3. **Workflow:** Add a GitHub Action workflow in `treasury-cache/.github/workflows/`
4. **Detail page:** Create `/stat-name/index.html` in `truesight_me_beta/`
5. **Stat card:** Add the card to `truesight_me_beta/index.html` + `formatStatValue()` case
6. **Deploy:** Merge to beta, sync to prod, trigger the GAS sync and GitHub Action

## Secrets Required

| Secret | Repo | Purpose |
|--------|------|---------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | `treasury-cache` | Cypher Defense SA key for sheet access |
| `GH_PAT_TOKEN` | `treasury-cache` | GitHub PAT for committing cache files |

## Deployment Flow

1. Merge PRs to `truesight_me_beta` (beta site auto-deploys via GitHub Pages)
2. Run `sync_beta_to_prod()` to promote to `truesight_me_prod` (may hit CNAME conflict)
3. Trigger `?action=triggerSync` on the GAS endpoint to refresh Performance Statistics
4. Trigger the GitHub Action workflow to regenerate the JSON cache

## Example: Buy-Back Reserve

| Layer | File/Location |
|-------|---------------|
| GAS | `syncAllPerformanceStatistics()` reads "USD - provisions for voting rights cash out" |
| Python | `tokenomics/python_scripts/tdg_asset_management/update_buy_back_reserve_cache.py` |
| Workflow | `treasury-cache/.github/workflows/update-buy-back-reserve-cache.yml` |
| Cache | `treasury-cache/buy-back-reserve.json` |
| Detail | `truesight_me_beta/buy-back-reserve/index.html` |
| Card | `truesight_me_beta/index.html` (stat-card #7, hidden behind "Show More Stats") |
