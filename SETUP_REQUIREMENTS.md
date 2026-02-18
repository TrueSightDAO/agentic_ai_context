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

## Other Projects

### sentiment_importer (Edgar)

**Location:** `/Users/garyjob/Applications/sentiment_importer/`

- Environment variables (see `agentic_ai_api_credentials` for variable names)
- No credential files required (uses `.env`)

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
- `agentic_ai_api_credentials/API_CREDENTIALS_DOCUMENTATION.md` — Environment variable reference
- `agentic_ai_api_credentials/env.template` — Template for environment variables
