# Setup Requirements — Credential Files Needed Per Project

This document lists credential files and sensitive configuration that must be obtained from the user during project setup. **Never commit these files to Git** — they are excluded via `.gitignore` and should be provided by the user.

**Global check-in rules:** See **WORKSPACE_CONTEXT.md** section **3a** for the full list of what must not be committed to GitHub (credentials, secrets, `node_modules/`, `venv/`, build artifacts, etc.). Always verify before push.

---

## agroverse_shop

**Location:** `/Users/garyjob/Applications/agroverse_shop/`

### Required Credential Files

When setting up `agroverse_shop` for the first time or in a new environment, **prompt the user** to provide these files:

1. **`google-service-account.json`**
   - **Purpose:** Google Cloud service account credentials for QR code management
   - **Location:** Root directory (`agroverse_shop/google-service-account.json`)
   - **Contains:** Service account private key, client email, project ID
   - **Status:** ✅ Protected in `.gitignore`
   - **Action:** Prompt user: "Please provide `google-service-account.json` for Google Cloud service account access"

2. **`scripts/youtube_credentials.json`**
   - **Purpose:** YouTube OAuth credentials for video upload automation
   - **Location:** `agroverse_shop/scripts/youtube_credentials.json`
   - **Contains:** OAuth client ID and client secret
   - **Status:** ✅ Protected in `.gitignore`
   - **Action:** Prompt user: "Please provide `scripts/youtube_credentials.json` for YouTube API access"

3. **`scripts/youtube_token.json`**
   - **Purpose:** YouTube OAuth tokens (access token and refresh token)
   - **Location:** `agroverse_shop/scripts/youtube_token.json`
   - **Contains:** Access token, refresh token, expiry information
   - **Status:** ✅ Protected in `.gitignore`
   - **Action:** Prompt user: "Please provide `scripts/youtube_token.json` for YouTube API authentication"

### API Keys in Tracked Files

**`js/config.js`** is tracked by Git and contains:
- Google Places API key (public key, but should be restricted in Google Cloud Console)
- Facebook Pixel ID (public identifier)

**Note:** These are less sensitive but should ideally be moved to environment variables. For now, ensure the Google Places API key is restricted to specific domains in Google Cloud Console.

### Setup Checklist

When setting up `agroverse_shop`:

- [ ] Verify `.gitignore` includes credential file patterns
- [ ] Prompt user for `google-service-account.json`
- [ ] Prompt user for `scripts/youtube_credentials.json`
- [ ] Prompt user for `scripts/youtube_token.json`
- [ ] Verify files are not tracked: `git ls-files | grep -E '(google-service-account|youtube_credentials|youtube_token)'`
- [ ] Confirm files exist and are readable
- [ ] Review `docs/SECURITY.md` for security best practices

### Verification Commands

```bash
# Check if credential files are tracked (should return nothing)
cd /Users/garyjob/Applications/agroverse_shop
git ls-files | grep -E '(google-service-account|youtube_credentials|youtube_token)'

# Verify files exist locally (should list the files)
ls -la google-service-account.json scripts/youtube_credentials.json scripts/youtube_token.json

# Verify .gitignore protection
git check-ignore google-service-account.json scripts/youtube_credentials.json scripts/youtube_token.json
```

---

## market_research

**Location:** `/Users/garyjob/Applications/market_research/`

### Local `.env` (fresh machine)

Operators and AI agents use **`market_research/.env`** for secrets that must **not** be committed. Tracked template: **`.env.example`**.

| Variable | Required for | Notes |
|----------|----------------|-------|
| **`GITHUB_PAT`** | Uploading invoice PDFs to **`TrueSightDAO/.github`** **`assets/`**, or using **`GH_TOKEN`** with **`gh`** for PRs | Grant **Contents** read/write on that repo. For **`gh pr create` / merge**, also **Pull requests** (fine-grained) or classic **`repo`**. See **`WORKSPACE_CONTEXT.md`** §**3c**. |
| **`google_credentials.json`** (file) | Google Sheets scripts | Service account JSON in repo root; see **`market_research/README.md`**. For tab **OpenClaw Beer Hall updates** on the [Telegram compilation sheet](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit), share that spreadsheet with the service account **client_email** as **Editor**, then run **`market_research/scripts/ensure_beer_hall_log_sheet.py`** (migrates legacy **Beer_Hall_Posts** if it exists). After each Beer Hall digest, append a row with **`market_research/scripts/append_openclaw_beer_hall_log.py`**. |
| Other keys (`DATAFORSEO_*`, `GROK_*`, `WIX_*`, …) | Specific scripts | As documented per script / **`README.md`**. |

**Setup:** `cp .env.example .env` then fill in values. Confirm **`git check-ignore .env`**.

### Setup Checklist

- [ ] Copy **`.env.example`** → **`.env`**
- [ ] Add **`GITHUB_PAT`** if automating Contribution Ledger asset uploads or PR tooling from this workspace
- [ ] Add **`google_credentials.json`** and share Sheets with the service account
- [ ] Verify **`.env`** is ignored: `git check-ignore -v .env`

---

## Other Projects

### sentiment_importer (Edgar)

**Location:** `/Users/garyjob/Applications/sentiment_importer/`

- Environment variables (see **`API_CREDENTIALS_DOCUMENTATION.md`** §1 for variable names)
- **Agroverse store inventory (optional):** **`AGROVERSE_INVENTORY_GAS_WEBAPP_URL`** ( **`update_store_inventory`** web app exec URL, no query string) and **`AGROVERSE_INVENTORY_PUBLISH_SECRET`** (must match the GAS Script property of the same name). **Sidekiq** calls the GAS **`doGet`** (default **`recalculateAndPublishInventory`**) after **Meta** checkout Wix sync **`:created`** and after **QR code + Stripe** success once **`QrCodeCheckController`** saves **Agroverse QR codes** / **QR Code Sales**. If unset, the worker no-ops. See **`app/workers/agroverse_inventory_snapshot_publish_worker.rb`**.
- No credential files required (uses `.env`)

### truesight_me

**Location:** `/Users/garyjob/Applications/truesight_me/`

- May require `google-service-account.json` (check project-specific requirements)
- WIX_* credentials (environment variables)

### tokenomics

**Location:** `/Users/garyjob/Applications/tokenomics/`

- Environment variables (see `agentic_ai_api_credentials`)
- QR_CODE_REPOSITORY_TOKEN, GDRIVE_KEY, WIX_*, GITHUB_*
- **Apps Script `update_store_inventory`** (clasp mirror **`clasp_mirrors/1P0Mg33i_dD9x9IeoHYvtKrf0xFcmUznpqAswyC_KXR3VJZu-0C-UOP0v/`**): in the **Google Cloud / Apps Script** project (not in `tokenomics/.env`), set **Script property** **`AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`** to the fine-grained PAT that can write **`TrueSightDAO/agroverse-inventory`** via the Contents API. See **`API_CREDENTIALS_DOCUMENTATION.md`** §**6a**.

### agroverse-inventory (public snapshot repo)

**Location:** operator clone (e.g. `/Users/garyjob/Applications/agroverse-inventory/`)

- **No** PAT or `.env` is required **in this repository** for normal use; automation commits via GAS using Script properties above.
- Optional: keep a **`README.md`** describing that JSON is generated and that **`AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`** is configured only in **`update_store_inventory`**.

---

## General Principles

1. **Never commit credential files** — Always check `.gitignore` first
2. **Prompt during setup** — When cloning or setting up a project, ask the user for required credential files
3. **Verify protection** — Use `git check-ignore` to confirm files are excluded
4. **Document requirements** — Update this file when new credential requirements are discovered
5. **Use environment variables** — Prefer `.env` files over credential JSON files when possible

---

## Related Documentation

- `agroverse_shop/docs/SECURITY.md` — Security guidelines and credential management
- `market_research/README.md` — **`.env`**, **`.env.example`**, **`GITHUB_PAT`**, Google Sheets setup
- `market_research/SECURITY.md` — Do not commit **`.env`** or **`GITHUB_PAT`**
- `WORKSPACE_CONTEXT.md` §**3c** — Contribution Ledger invoice → GitHub pattern using **`GITHUB_PAT`**
- `agentic_ai_api_credentials/API_CREDENTIALS_DOCUMENTATION.md` — Environment variable reference (sibling repo, if cloned)
- `agentic_ai_api_credentials/env.template` — Template for environment variables (sibling repo, if cloned)
