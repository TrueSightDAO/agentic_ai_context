# Google API Credentials & Service Account IDs

## Overview
This document lists all Google API credentials, service account IDs, and OAuth client IDs available in the codebase for accessing Google Docs and Google Sheets.

---

## 🔐 Service Account Credentials (For Google Sheets/Docs API)

### 1. **Cypher Defense Service Account** (Primary for Ledgers)
- **File**: `config/cypher_defense_gdrive_key.json`
- **Service Account Email**: `cypher-defense@get-data-io.iam.gserviceaccount.com`
- **Client ID**: `111654637853352905522`
- **Private Key ID**: `01b80356e47755e3b3c0b3233a10945c0e68b157`
- **Project ID**: `get-data-io`
- **Used For**: 
  - TSD DAO Ledger
  - Cypher Defense Ledger
  - Main ledger access

### 2. **Market Research Service Account**
- **File**: `krake_local/google-service-account.json`
- **Service Account Email**: `agroverse-market-research@get-data-io.iam.gserviceaccount.com`
- **Client ID**: `110900631541311492782`
- **Private Key ID**: `6bbaad8e97daaa238d6eef65b80e276fbe7a5df1`
- **Project ID**: `get-data-io`
- **Used For**: Market research Google Sheets

### 3. **UPC Barcode Service Account**
- **File**: `config/upc_barcode_gdrive_key.json`
- **Service Account Email**: `upc-barcode@get-data-io.iam.gserviceaccount.com`
- **Client ID**: `111948237428776722448`
- **Private Key ID**: `23160ba54a6a3fecfd4d9cb43e7774d0330861de`
- **Project ID**: `get-data-io`
- **Used For**: UPC barcode sheets

### 4. **TDG Scoring Service Account**
- **File**: `config/tdg_scoring_gdrive_key.json`
- **Service Account Email**: `tdg-scoring-peer-reviewer@get-data-io.iam.gserviceaccount.com`
- **Client ID**: `103508677348547083951`
- **Private Key ID**: `b8d607602b17153dfdc0a4ad2f24b40928950945`
- **Project ID**: `get-data-io`
- **Used For**: TDG scoring sheets

### 5. **Edgar DApp Listener Service Account**
- **File**: `config/edgar_dapp_listener_key.json`
- **Service Account Email**: `edgar-dapp-listener@get-data-io.iam.gserviceaccount.com`
- **Client ID**: `109837321703136724068`
- **Private Key ID**: `05405eb46a529f4a7beb7051e2c5564005ecf32d`
- **Project ID**: `get-data-io`
- **Used For**: Edgar DApp Telegram logs

### 6. **TrueSight.me whitepaper (Google Docs read) — DEPRECATED**
> ⚠️ **Deprecated (2026-05):** the whitepapers are now static pages in the
> `truesight_me` repo (`truesight_me/<area>/whitepaper/index.html`), not Google
> Docs. This SA and `fetch_whitepaper.py` only read the **retired** Docs. See
> `GOVERNANCE_SOURCES.md` §1. Kept for historical access only.
- **File (local, gitignored):** `truesight_me/credentials/whitepaper-google-sa.json` — key file lives only on developer machines; **never commit** (see `truesight_me/credentials/README.md` and `truesight_me/.gitignore`).
- **Service Account Email**: `truesightme-whitepapers@get-data-io.iam.gserviceaccount.com`
- **Client ID**: `111924219696923655238`
- **Private Key ID**: `91745a4ba4c748eebae3f0b5b6901a81ec0239ec`
- **Project ID**: `get-data-io`
- **Used For**: Reading TrueSight whitepaper Google Docs via the Docs API (e.g. `agentic_ai_context/scripts/fetch_whitepaper.py` with `GOOGLE_APPLICATION_CREDENTIALS` or `--credentials`). Grant **Viewer** on each whitepaper doc to this service account.

---

## 📁 Google Drive folders (Agroverse artifacts)

- **Generated Google Sheets / spec artifacts (default location)**  
  - **Folder ID:** `1esYnlwChRmv9-M3ymWYhWMPHRowhOluw`  
  - **URL:** [drive.google.com/.../folders/1esYnlwChRmv9-M3ymWYhWMPHRowhOluw](https://drive.google.com/drive/folders/1esYnlwChRmv9-M3ymWYhWMPHRowhOluw)  
  - **Purpose:** New spreadsheets from scripts or AI workflows (e.g. product development checklists) should be created or moved here. See **`PRODUCT_DEVELOPMENT_SPECS.md`**.  
  - **Access:** Grant **Editor** on the folder to service accounts that create files (e.g. `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com`).

---

## 📊 Google Sheets/Docs IDs (Ledgers)

### Main Ledger (TSD DAO)
- **Spreadsheet ID**: `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`
- **URL**: `https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=0`
- **Outstanding Airdrops Sheet GID**: `1569170936`
- **Service Account**: Cypher Defense (`cypher-defense@get-data-io.iam.gserviceaccount.com`)
- **Correios tracking in `Currency` strings:** Product names may include **`CP`…`BR`** — typically the **Correios** tracking reference for parcels shipped from **Ilheus, Brazil** (often **Matheus’** location) **to the U.S.**, used to tie ledger lines to a specific inbound package. See **`WORKSPACE_CONTEXT.md`** §4 (same repo).
- **Ledger conversion / repackaging:** Composite product names (inputs combined into outputs at a location) — **`LEDGER_CONVERSION_AND_REPACKAGING.md`** (canonical); **`WORKSPACE_CONTEXT.md` §3b** points agents there.

### Cypher Defense Ledger
- **Spreadsheet ID**: `1zRDDL9JRzfbQTMo6AmTdDxWTQaDv4aQakbZrm4T2BTU`
- **URL**: `https://docs.google.com/spreadsheets/d/1zRDDL9JRzfbQTMo6AmTdDxWTQaDv4aQakbZrm4T2BTU/edit?resourcekey=undefined#gid=2007931337`
- **Worksheet GID**: `282644568`
- **Service Account**: Cypher Defense (`cypher-defense@get-data-io.iam.gserviceaccount.com`)

---

## 🔑 OAuth Client IDs (For User Authentication)

### Production OAuth Client
- **Client ID**: `667737028020-r81hcrevugbn0h7pv17gubkq4kn373oh.apps.googleusercontent.com`
- **Client Secret**: `g0jGv7YAS02-k3wOWTGeE7vl`
- **Location**: `config/environments/production.rb`
- **Used For**: User OAuth authentication (email, profile)

### Development OAuth Client
- **Client ID**: `667737028020-s5mf5lcr4gsm3ruhfbnd61v8ln28qib7.apps.googleusercontent.com`
- **Client Secret**: `QLD-s447HWJYcB2e4IwFiE6S`
- **Location**: `config/environments/development.rb`
- **Used For**: Development/testing OAuth

### Test OAuth Client (Krake ROR)
- **Client ID**: `667737028020-s5mf5lcr4gsm3ruhfbnd61v8ln28qib7.apps.googleusercontent.com`
- **Client Secret**: `QLD-s447HWJYcB2e4IwFiE6S`
- **Location**: `krake_ror/config/environments/test.rb`

---

## 🧰 clasp OAuth — per-account credentials files

For deploying Google Apps Script projects via `clasp push`. clasp itself reads `~/.clasprc.json` (single active identity). To deploy projects owned by *different* Google accounts without re-running `clasp login` every time, Gary maintains **per-account credentials files** in his home directory and swaps the active one before each push.

| File | Account | Resolved 2026-05-29 |
|---|---|---|
| `~/.clasprc-gary.json`  | `garyjob@agroverse.shop` (daily driver) | ✅ verified via `oauth2/v3/userinfo` |
| `~/.clasprc-admin.json` | `admin@truesight.me` (owner of digital-signature ingestion, QR-code web service, Edgar email verification, and other admin@-pinned GAS projects) | ✅ verified via `oauth2/v3/userinfo` |
| `~/.clasprc.json`       | Whichever one was last copied into place. | (the active identity at any moment) |

### Workflow

The `tokenomics/scripts/deploy_gas_project.py` script (see [`TOKENOMICS_GAS_RESTRUCTURE_PLAN.md`](TOKENOMICS_GAS_RESTRUCTURE_PLAN.md) PR-final-1 + PR-1g) **refuses to push** when the active clasp identity doesn't match the project's `owner_email` in its manifest. So before pushing an admin@-owned project, do:

```bash
cp ~/.clasprc-admin.json ~/.clasprc.json
cd ~/Applications/tokenomics
python3 scripts/deploy_gas_project.py <scriptId> --push          # gates on owner_email match
cp ~/.clasprc-gary.json ~/.clasprc.json                          # restore daily driver
```

The script's `CLASPRC_PATH` env var can also point identity *resolution* at a different file (for the safety check), but clasp itself still reads `~/.clasprc.json` — so the `cp` swap above is the actual deploy gesture.

### Re-minting (when one of these tokens expires / gets revoked)

Each clasprc holds a long-lived OAuth refresh token. If it stops working:

```bash
clasp logout
clasp login                                    # browser flow, sign in as the target account
cp ~/.clasprc.json ~/.clasprc-<account>.json   # save into the per-account slot
```

### Backup considerations

These files contain long-lived refresh tokens. They're **not committed to any repo** (correct), but they're also **not backed up anywhere off-host** as of 2026-05-29 — a wiped laptop loses both, and the only recovery is to re-run `clasp login` for each account (~3 min). Same risk applies to several other workspace credentials (Google service-account JSONs under various `*/config/*.json`, the `dao_client/.env` RSA private key, etc.). See the *Open follow-up* below.

---

## 🗄️ Credential backup / vault — moved to own repo

Disaster recovery for laptop credentials now lives in
**[`TrueSightDAO/credential_vault`](https://github.com/TrueSightDAO/credential_vault)**.
That repo's `ONBOARDING.md` is the LLM-runnable script for new governor
architects; `README.md` is the disaster-recovery / restore runbook.

This document continues to be the source of truth for *what each
credential is for*. The vault repo is the source of truth for *how to
store/restore them*. See [`CREDENTIAL_VAULT.md`](CREDENTIAL_VAULT.md) for
the redirect + LLM routing notes.

**Out of scope for V1** (and intentionally): host-side credential
provisioning for new EC2 instances — that's a separate vault problem
tracked in [`OPEN_FOLLOWUPS.md`](OPEN_FOLLOWUPS.md) § "Credential vault for
service-account keys (AWS Secrets Manager)".

---

## 📝 Usage Examples

### Accessing Main Ledger (Ruby/Rails)
```ruby
require 'google_drive'

# Using Cypher Defense service account
session = GoogleDrive::Session.from_service_account_key("config/cypher_defense_gdrive_key.json")

# Access main ledger
spreadsheet = session.file_by_url("https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=0")

# Or by spreadsheet ID
spreadsheet = session.spreadsheet_by_key("1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU")
```

### Accessing Cypher Defense Ledger
```ruby
session = GoogleDrive::Session.from_service_account_key("config/cypher_defense_gdrive_key.json")
spreadsheet = session.file_by_url("https://docs.google.com/spreadsheets/d/1zRDDL9JRzfbQTMo6AmTdDxWTQaDv4aQakbZrm4T2BTU/edit")
worksheet = spreadsheet.worksheet_by_gid("282644568")
```

### Python Example (Using gspread)
```python
import gspread
from google.oauth2.service_account import Credentials

# Load service account credentials
creds = Credentials.from_service_account_file('config/cypher_defense_gdrive_key.json')
client = gspread.authorize(creds)

# Open spreadsheet
spreadsheet = client.open_by_key('1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU')
worksheet = spreadsheet.sheet1  # or by name: spreadsheet.worksheet('Sheet Name')

# Read data
rows = worksheet.get_all_records()
```

---

## 🎯 Recommended Service Account for Tax Submission

**For reading/writing sales and expenses records from ledgers:**

**Use**: `cypher-defense@get-data-io.iam.gserviceaccount.com`
- **File**: `config/cypher_defense_gdrive_key.json`
- **Client ID**: `111654637853352905522`

This service account already has access to:
- Main TSD DAO Ledger (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`)
- Cypher Defense Ledger (`1zRDDL9JRzfbQTMo6AmTdDxWTQaDv4aQakbZrm4T2BTU`)

---

## ⚠️ Important Notes

1. **Service Account Permissions**: Make sure the service account email has been granted "Editor" or "Viewer" access to the Google Sheets you want to access. Share the spreadsheet with the service account email address.

2. **Scopes Required**: For reading/writing Google Sheets and Docs, ensure these scopes are enabled:
   - `https://www.googleapis.com/auth/spreadsheets`
   - `https://www.googleapis.com/auth/drive`
   - `https://www.googleapis.com/auth/documents` (for Google Docs)

3. **API Enablement**: Ensure these APIs are enabled in Google Cloud Console:
   - Google Sheets API
   - Google Drive API
   - Google Docs API (if needed)

4. **Project**: All service accounts belong to project `get-data-io`

---

## 📚 Related Files

- `sentiment_importer/app/models/gdrive/tsd_dao_ledger.rb` - TSD DAO Ledger access
- `sentiment_importer/app/models/gdrive/cypher_ledger.rb` - Cypher Defense Ledger access
- `sentiment_importer/app/models/gdrive/upc_barcode_sheet.rb` - UPC Barcode sheet access
- `sentiment_importer/app/models/gdrive/scored_chatlog.rb` - Scored chatlog access

---

## 🔍 Finding More Spreadsheet IDs

To find additional spreadsheet IDs from URLs:
- Format: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`
- The ID is the long string between `/d/` and `/edit`

Example: `https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit`
- Spreadsheet ID: `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`
