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
| **`GITHUB_PAT`** | Uploading invoice PDFs to **`TrueSightDAO/.github`** **`assets/`**, or using **`GH_TOKEN`** with **`gh`** with PRs | Grant **Contents** read/write on that repo. See **`WORKSPACE_CONTEXT.md`** §**3c**. **Legacy — limited scope.** |
| **`TRUESIGHT_DAO_AUTOPILOT`** | **Autopilot service** — open PRs, create branches, read workflow logs across all `TrueSightDAO/*` repos | Fine-grained PAT with **Contents: Read + Write** + **Pull requests: Read + Write** on all target repos. **✅ Verified live 2026-05-03 — see `API_CREDENTIALS_DOCUMENTATION.md` §10.2.2.** |
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

### sentiment_importer (trading platform)

**Location:** `/Users/garyjob/Applications/sentiment_importer/`

- **Production:** **`https://perch.truesight.me`** (Rails app + Sidekiq). Trading platform (stock/crypto) — DAO operations are in **dao_protocol**. **Not** **`getdata.io`** — that is **krake_ror** (see **WORKSPACE_CONTEXT.md** §6).
- **Agroverse Shop** checkout calls **`GET https://edgar.truesight.me/agroverse_shop/shipping_rates`** for USPS quotes (this route is proxied to dao_protocol via nginx); see **`agroverse_shop/js/config.js`** `shippingRatesApiOrigin`.
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
3. **Verify protection** — Confirm files are gitignored/tracked appropriately
4. **Document locations** — Keep canonical docs (`SETUP_REQUIREMENTS.md`, `credentials/API_CREDENTIALS_DOCUMENTATION.md`) in sync when adding new credentials

---

## truesight_autopilot (deployed)

`TrueSightDAO/truesight_autopilot` is live on a **dedicated EC2 instance** (`us-east-1`, t3.small, IP `100.52.234.163`) — separate from `seni_ror` (Edgar) to protect critical infrastructure.

### Server Layout

| Path | Purpose |
|---|---|
| `/opt/truesight_autopilot` | Application code (rsync'd from local repo via `scripts/deploy.sh`) |
| `/opt/truesight_autopilot/.env` | Live credentials (chmod 600) |
| `/etc/systemd/system/truesight-autopilot.service` | Systemd service definition |
| `~/.ssh/config` → `Host truesight-autopilot` | SSH alias (auto-updated by `launch_ec2.sh`) |

### Prerequisites (all resolved)

| Item | Status | Notes |
|---|---|---|
| Gmail OAuth token | ✅ Ready | `market_research/credentials/gmail/token.json` copied to EC2 `.env` as `GMAIL_TOKEN_JSON`; `gmail.modify` + refresh token active |
| GitHub PAT | ✅ Ready | `TRUESIGHT_DAO_AUTOPILOT` from `market_research/.env`; fine-grained PAT with Contents+PR write on `TrueSightDAO/*` |
| DeepSeek API | ✅ Ready | `DEEPSEEK_SDK` from local `.env`; ~30× cheaper than Claude |
| AWS credentials | ✅ Ready | `TRUESIGHT_DAO_AUTOPILOT_AWS_KEY` / `_SECRET` from `cypher_def/.env` copied to EC2 as `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` |
| Tencent Cloud | ✅ Present | `TENCENT_SECRET_ID` / `TENCENT_SECRET_KEY` in `/opt/truesight_autopilot/.env` (also appended to `/opt/bionpact_autopilot/.env` on the Bionpact host) |
| EC2 host | ✅ Ready | Dedicated t3.small in `us-east-1d`; launched via `scripts/launch_ec2.sh` |

### Remaining blockers

| # | Blocker | Impact | Resolution |
|---|---|---|---|
| 1 | **No dedicated Edgar identity for automation** | Autopilot currently uses no Edgar signing; contributions are not logged to Edgar | Generate new RSA keypair via `truesight-dao-auth login`, register as `autopilot@agroverse.shop`, store in isolated `.env` |

### Suggested `.env` for autopilot

```bash
# Gmail (monitor failure emails)
GMAIL_TOKEN_JSON=<paste full token.json contents>

# GitHub (open PRs, read workflow logs)
TRUESIGHT_DAO_AUTOPILOT=<fine-grained PAT with Contents+PR write on target repos>

# LLM (DeepSeek only — dropped Kimi + Claude)
DEEPSEEK_API_KEY=<or DEEPSEEK_SDK>
DEEPSEEK_BASE_URL=https://api.deepseek.com

# AWS (long-lived keys; IAM instance role also acceptable)
AWS_ACCESS_KEY_ID=<from cypher_def/.env TRUESIGHT_DAO_AUTOPILOT_AWS_KEY>
AWS_SECRET_ACCESS_KEY=<from cypher_def/.env TRUESIGHT_DAO_AUTOPILOT_AWS_SECRET>
AWS_REGION=us-east-1

# Tencent Cloud (COS / SMS / other Tencent services)
# Locations: /opt/truesight_autopilot/.env and /opt/bionpact_autopilot/.env
TENCENT_SECRET_ID=<Tencent Cloud API SecretId>
TENCENT_SECRET_KEY=<Tencent Cloud API SecretKey>

# Edgar (automation identity — NOT personal keys)
EMAIL=autopilot@agroverse.shop
PUBLIC_KEY=<SPKI base64>
PRIVATE_KEY=<PKCS#8 base64>

# Context sync
AGENTIC_CONTEXT_REPO=https://github.com/TrueSightDAO/agentic_ai_context.git
```

---

## Related Documentation
