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
| **`ANTHROPIC_API_KEY`** | `scripts/draft_beer_hall_digest.py` (Claude Sonnet 4.6 drafter) — also mirrored as a GH Actions secret on `TrueSightDAO/go_to_market` for the daily Beer Hall workflow. | No scope restrictions at the provider level; rotate if leaked. |
| **`ORACLE_ADVISORY_PUSH_TOKEN`** | GH Actions workflows (`beer-hall-digest-daily.yml`, `advisory-snapshot-refresh.yml`) that push + auto-merge on `ecosystem_change_logs` and `agentic_ai_context`. Local runs of `generate_advisory_snapshot.py --github-api-publish` can also read it. | Fine-grained PAT with **Contents: Read + Write** and **Pull requests: Read + Write** on `TrueSightDAO/ecosystem_change_logs` and `TrueSightDAO/agentic_ai_context`. Add **Contents: Read** on `TrueSightDAO/Cypher-Defense` if that repo is private. |
| **`google_credentials.json`** (file) | Google Sheets scripts | Service account JSON in repo root; see **`market_research/README.md`**. Shared with the service account **client_email** as **Editor** on the [Telegram compilation sheet](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit) so `list_recent_telegram_chat_logs_for_digest.py` can pull recent rows into the Beer Hall preview. Also mirrored as GH Actions secret `GOOGLE_CREDENTIALS_JSON` on `TrueSightDAO/go_to_market`. |
| Other keys (`DATAFORSEO_*`, `GROK_*`, `WIX_*`, …) | Specific scripts | As documented per script / **`README.md`**. |

**Setup:** `cp .env.example .env` then fill in values. Confirm **`git check-ignore .env`**.

### Setup Checklist

- [ ] Copy **`.env.example`** → **`.env`**
- [ ] Add **`GITHUB_PAT`** if automating Contribution Ledger asset uploads or PR tooling from this workspace
- [ ] Add **`ANTHROPIC_API_KEY`** if running `scripts/draft_beer_hall_digest.py` locally (otherwise only needed in repo secrets)
- [ ] Add **`ORACLE_ADVISORY_PUSH_TOKEN`** if running `generate_advisory_snapshot.py --github-api-publish` locally
- [ ] Add **`google_credentials.json`** and share Sheets with the service account
- [ ] Verify **`.env`** is ignored: `git check-ignore -v .env`

---

## Other Projects

### sentiment_importer (Edgar)

**Location:** `/Users/garyjob/Applications/sentiment_importer/`

- **Production deploy:** **`https://edgar.truesight.me`** (Rails app + Sidekiq). **Not** **`getdata.io`** — that is **krake_ror** (see **WORKSPACE_CONTEXT.md** §6).
- **Agroverse Shop** checkout calls **`GET https://edgar.truesight.me/agroverse_shop/shipping_rates`** for USPS quotes (see **`agroverse_shop/js/config.js`** `shippingRatesApiOrigin`); inventory snapshot worker uses **`AGROVERSE_INVENTORY_*`** env vars on the Edgar host.
- Environment variables (see `agentic_ai_api_credentials` / **`API_CREDENTIALS_DOCUMENTATION.md`** for variable names)
- No credential files required (uses `.env`)

### krake_ror

**Location:** `/Users/garyjob/Applications/krake_ror/`

- **Production:** **`https://getdata.io`** — Krake data-harvesting Rails app. **Not** Edgar / **sentiment_importer** (**`edgar.truesight.me`**).

### truesight_me

**Location:** `/Users/garyjob/Applications/truesight_me/`

- May require `google-service-account.json` (check project-specific requirements)
- WIX_* credentials (environment variables)

### tokenomics

**Location:** `/Users/garyjob/Applications/tokenomics/`

- Environment variables (see `agentic_ai_api_credentials`)
- QR_CODE_REPOSITORY_TOKEN, GDRIVE_KEY, WIX_*, GITHUB_*

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
