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

---

## 📊 Google Sheets/Docs IDs (Ledgers)

### Main Ledger (TSD DAO)
- **Spreadsheet ID**: `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`
- **URL**: `https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=0`
- **Outstanding Airdrops Sheet GID**: `1569170936`
- **Service Account**: Cypher Defense (`cypher-defense@get-data-io.iam.gserviceaccount.com`)

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
