# Managed Ledger Explorer — Reusable Pattern

**For future projects** that need a public donation / disbursement audit trail riding on TrueSight DAO infrastructure.

## The pattern in one sentence

A static `treasury-cache/managed-ledgers/<ledger_name>.json` file published by a data producer (Apps Script, Claude agent, cron job) is rendered as a public transparency explorer by a GitHub Pages site that reads from it via `raw.githubusercontent.com`.

## Components

| Layer | What | Example |
|-------|------|---------|
| **Data source** | Stripe, TransferWise, Pix, bank feed, manual entry | Stripe Checkout on `capoeira.agroverse.shop` |
| **Producer** | Apps Script (Google Sheets → git), Claude agent (direct commit), or cron Python script | GAS reconciles Stripe CSV → JSON |
| **Canonical JSON** | `treasury-cache/managed-ledgers/<ledger_name>.json` | `treasury-cache/managed-ledgers/tribomirimbahia.json` |
| **Explorer UI** | Dark-theme GitHub Pages site, fetches from `raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/managed-ledgers/<ledger_name>.json` | `tribomirimbahia/index.html` |
| **Domain** | Custom domain via CNAME in the explorer repo | `mirim-bahia.truesight.me` (tribomirimbahia repo) |

## How to set up a new ledger

### 1. Choose a `ledger_name`

Lowercase, snake_case, matches the program. Examples:
- `tribomirimbahia` — Tribo Bahia Mirim Capoeira
- `sunmint_reforestation` — Sunmint tree-planting donations
- `agroverse_coop_fund` — Cooperative investment fund

### 2. Create the initial JSON file

```bash
mkdir -p treasury-cache/managed-ledgers
```

Minimal bootstrap file at `treasury-cache/managed-ledgers/<ledger_name>.json`:

```json
{
  "ledger_name": "<ledger_name>",
  "program_name": "Human-readable program name",
  "description": "One-line description of what this ledger tracks.",
  "schema_version": 1,
  "generated_at": "<ISO timestamp>",
  "source": "manual-init",
  "summary": {
    "total_donations_usd": 0,
    "total_fees_usd": 0,
    "total_net_to_program": 0,
    "transaction_count": 0
  },
  "transactions": []
}
```

### 3. Transaction schema (recommended)

The explorer normalizes flexibly, but producers **should** use these canonical fields:

```json
{
  "id": "unique_transaction_id",
  "date": "2026-05-10T14:30:00Z",
  "type": "stripe_donation | transferwise_fx | pix_outbound | other",
  "description": "Human-readable summary",
  "amount": 50.00,
  "fees": 1.75,
  "net": 48.25,
  "currency": "USD | BRL",
  "reference": "stripe_ch_xxx | tw_ref_xxx | pix_e2e_id_xxx",
  "status": "completed | pending | failed",
  "recipient": "Destination name (for outbound transfers)"
}
```

**Type conventions:**
- `stripe_donation` — incoming donation via Stripe Checkout
- `transferwise_fx` — currency conversion (e.g. USD → BRL)
- `pix_outbound` — final disbursement to program recipient

**Field conventions:**
- `amount` / `fees` / `net` are in the `currency` unit
- `reference` is the external payment ID (Stripe charge, TransferWise transfer, Pix end-to-end ID)
- `recipient` is required for `pix_outbound` transactions

### 4. Create the managed ledger in Google Sheets

**Template:** `1WoGS2_IPFmwM8VI0G-nU9mJ05wwwacDn7QypJKYnxq4` — "AGL MANAGED LEDGER TEMPLATE"

1. Open the template → **File → Make a copy** → save to your account
2. Rename: `"<LEDGER_NAME> — <Program Name>"`
3. Update contract URLs on Balance (B1) and Transactions (B1) tabs
4. Register in Shipment Ledger Listing (see below)
5. Share with `cypher-defense@get-data-io.iam.gserviceaccount.com` (writer)

The template has 7 tabs with all formulas, formatting, and AGL-standard structure:
- `README` — setup instructions
- `Unit Costing Economics` — per-unit cost breakdowns
- `Balance` — Equity, Asset, Resource Location, Liabilities
- `Transactions` — Date, Description, Entity, Amount, Currency, Type, Line #
- `State` — Currencies catalog with Price in USD
- `Entities` — Ledger Entities (TrueSight DAO, Smart Contract, Customer)
- `Pricing Tiers` — cost/pricing models

**Register in Shipment Ledger Listing:**

Add a row to `Shipment Ledger Listing` (Main Ledger sheet `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, gid `483234653`):

| Col | Value |
|-----|-------|
| Shipment Date | Current date |
| Status | Active |
| Description | One-line description of the ledger's purpose |
| Transaction Type | `Donation` or `DAO financed` or `Defi Pre-Purchase` or `Merchant Green Pledge` |
| Ledger URL | Public-facing URL (e.g. `https://truesight.me/<program>`) |
| Resolved URL | The Google Sheets URL from step 1 |

Use the `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com` service account (has write access to Main Ledger) via `agroverse_shop/google-service-account.json`.

**Result:** The GAS scripts (`capital_injection_processing.gs`, `currency_conversion_processing.gs`, `web_app.gs`) read Shipment Ledger Listing dynamically — the new ledger is immediately discoverable. The DApp `currency_conversion.html` dropdown is also dynamic; no DApp code changes needed.

### 6. Build the explorer page

Copy `tribomirimbahia/index.html` as a template. Update three things:
1. `LEDGER_NAME` constant → your ledger name
2. `program_name` in `<title>` and meta tags
3. Domain-specific links in header and footer

The explorer auto-adapts to whatever shape the JSON has — it normalizes field names, handles missing entries gracefully, and shows a friendly empty state when the ledger isn't initialized.

### 7. Wire up the producer

The producer (App Script, Claude, or cron script) writes to `treasury-cache/managed-ledgers/<ledger_name>.json`. Two common patterns:

**A. Apps Script (mirrors existing tokenomics pipeline):**
1. Google Sheet → JSON export
2. GitHub Contents API PUT to `TrueSightDAO/treasury-cache/main/managed-ledgers/<ledger_name>.json`
3. Commit message: `chore: update <ledger_name> ledger snapshot`

**B. Direct commit (Claude agent or Python script):**
1. Clone/pull `treasury-cache` repo
2. Read existing JSON, append/replace transactions
3. Update `generated_at` and `summary` fields
4. Commit + push to main

### 8. Deploy the explorer

Enable GitHub Pages on the explorer repo (Settings → Pages → main branch → / (root)). Add CNAME for custom domain if desired.

## Existing ledgers

| Ledger name | Program | JSON file | Explorer |
|-------------|---------|-----------|----------|
| `tribomirimbahia` | Tribo Bahia Mirim Capoeira | `managed-ledgers/tribomirimbahia.json` | `tribomirimbahia/index.html` → `mirim-bahia.truesight.me` |

## Derivation rule

From a `ledger_name`, derive all paths:

```
JSON:   treasury-cache/managed-ledgers/<ledger_name>.json
URL:    https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/managed-ledgers/<ledger_name>.json
GitHub: https://github.com/TrueSightDAO/treasury-cache/blob/main/managed-ledgers/<ledger_name>.json
```
