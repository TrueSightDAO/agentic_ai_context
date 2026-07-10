# VOTING RIGHTS CASH-OUT SETTLEMENT — Implementation Plan

## Executive Summary

Two RSA-signed event types implement a complete voting rights cash-out pipeline:
1. `[VOTING RIGHTS WITHDRAWAL REQUEST]` — contributor signs a cash-out request (existing DApp page)
2. `[VOTING RIGHTS WITHDRAWAL SETTLEMENT EVENT]` — governor signs that settlement happened (new DApp page + backend)

Both are auto-dispatched via Edgar → GAS webhook, producing GitHub JSON paper trail files.

**Deployed:** 2026-07-02  
**GAS Project:** `1rLl94jQ9tDYdRvudnP0prPY5SEjvM07R4gPs6-vRyZEpSJhUqbiE3CZY` ("TDG - Asset Management Web App")  
**Deployment:** `AKfycbygmwRbyqse-dpCYMco0rb93NSgg-Jc1QIw7kUiBM7CZK6jnWnMB5DEjdoX_eCsvVs7` @22

---

## Architecture

```
withdraw_voting_rights.html          withdraw_voting_rights_settlement.html
(Contributor signs request)           (Governor signs settlement)
       │                                       │
       ▼                                       ▼
  POST /dao/submit_contribution         POST /dao/submit_contribution
  (Edgar)                                (Edgar)
       │                                       │
       ▼                                       ▼
  Telegram Chat Logs (col G)            Telegram Chat Logs (col G)
  [VOTING RIGHTS WITHDRAWAL REQUEST]    [VOTING RIGHTS WITHDRAWAL SETTLEMENT EVENT]
       │                                       │
       ▼                                       ▼
  dispatch.py routes to:                dispatch.py routes to:
  ?action=processVotingRights           ?action=processVotingRights
  WithdrawalRequests                     WithdrawalSettlement
       │                                       │
       ▼                                       ▼
  GAS: processVotingRights              GAS: processVotingRights
  WithdrawalRequests_()                  WithdrawalSettlement_()
       │                                       │
       ▼                                       ▼
  GitHub: treasury-cache/               GitHub: treasury-cache/
  cash-out-requests/{id}.json           cash-out-settlements/{id}.json
  (status: "pending")                   (settlement record)
       │                                       │
       │                              ┌────────────────────┐
       │                              │ Ledger history row  │
       │                              │ (A-H, Col G neg)   │
       │                              │ Col D: -1 : Trans- │
       │                              │ actions - For every │
       │                              │ 1 TDG Voting Rights│
       │                              │ Cashed Out          │
       │                              ├────────────────────┤
       │                              │ offchain transact- │
       │                              │ ions row (USD deb) │
       │                              ├────────────────────┤
       │                              │ Decrease USD prov- │
       │                              │ isions row in off  │
       │                              │ chain asset bal    │
       │                              └────────────────────┘
       │                                       │
       ▼                              If requestId present:
  (status: "settled",                 Update request JSON
   settled_at: ISO,                   status → "settled"
   settlement_request_id: ...)         (double-processing guard)
```

---

## Data Structures

### Cash-Out Request JSON
**Location:** `https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/cash-out-requests/{request_id}.json`

```json
{
  "schema_version": 1,
  "request_id": "<RSA signature hash>",
  "generated_at": "ISO-8601",
  "contributor": { "name": "Linda", "public_key": "..." },
  "amount_tdg": 208,
  "value_per_right_usd": 0.00673,
  "expected_total_usd": 1.40,
  "withdrawal_method": "PayLah",
  "payment_details": { "paylah_mobile": "+658..." },
  "raw_request_text": "<full signed event>",
  "signature": "<base64 RSA sig>",
  "source_dapp": "withdraw_voting_rights.html",
  "status": "pending",
  "settled_at": null,
  "settlement_request_id": null
}
```

### Cash-Out Settlement JSON
**Location:** `https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/cash-out-settlements/{settlement_id}.json`

```json
{
  "schema_version": 1,
  "settlement_id": "<RSA signature hash>",
  "generated_at": "ISO-8601",
  "governor": { "name": "Gary Teh", "public_key": "..." },
  "cash_out_request_id": "<request_id | null>",
  "contributor": "Linda",
  "amount_tdg_deducted": 208,
  "amount_paid_usd": 1.40,
  "payment_reference": "PayLah txn ID",
  "payment_method": "PayLah",
  "proof_attachment_url": "<URL | null>",
  "settlement_date": "20260702",
  "notes": "",
  "raw_settlement_text": "<full signed event>",
  "signature": "<base64 RSA sig>",
  "source_dapp": "withdraw_voting_rights_settlement.html"
}
```

### Ledger history Row (Settlement)
8-column write following the standard pattern (A-H):

| Col | Value | Notes |
|-----|-------|-------|
| A | Contributor name | From `Contributors contact information`!A |
| B | `Voting Rights Cash-Out` | Free-form project name |
| C | Cash-out settlement — {N} TDG — paid ${X.XX} | Contribution description |
| D | `-1 : Transactions - For every 1 TDG Voting Rights Cashed Out` | Rubric classification — defined in Meta Game Scoring Rubric spreadsheet, mirrored in `Intiatives Scoring Rubric` tab |
| E | {N} | Positive — the amount being acted upon (requested) |
| F | `Successfully Completed / Cash-Out Settled` | Distinct status from `Full Provision Awarded` |
| G | -{N} | **Negative** — reduces `voting_rights_circulated` (cell E1) |
| H | YYYYMMDD | Settlement date |

**Why this is safe:**
- `voting_rights_circulated` (E1) uses `=SUM(G:G)` — negative values reduce it correctly
- Airdrop refresher reads Col F for `"Full Provision Awarded"` — our distinct status is ignored
- Duplicate detection matches on Col A+Col C — our descriptions are unique
- Governor ranking formula sums Col G within 180-day window — cash-out deductions are typically for old accumulated TDG and won't meaningfully affect rankings

### Offchain Transactions Row (Settlement)

| Col | Value |
|-----|-------|
| A | YYYYMMDD |
| B | Voting rights cash-out — {Contributor} — {N} TDG — {Governor} |
| C | Governor name (Fund Handler) |
| D | -${amount} (negative = debit from provisions) |
| E | USD |

Plus: Decrease `off chain asset balance` Col D of the `"USD - provisions for voting rights cash out"` row by the USD amount.

---

## Files Modified / Created

### Backend — GAS Web App Handler
| File | Lines | What |
|------|-------|------|
| `tokenomics/google_app_scripts/1rLl94j.../Code.js` | 49-57 | Renamed `creds` → `assetCreds` to avoid file-scope conflict |
| `tokenomics/google_app_scripts/1rLl94j.../Code.js` | 423-429 | `doGet()` now routes `?action=processVotingRightsWithdrawalRequests` and `?action=processVotingRightsWithdrawalSettlement` |
| `tokenomics/google_app_scripts/1rLl94j.../Code.js` | 513-894 | Two new handler functions: `processVotingRightsWithdrawalRequests_()` (writes request JSONs to GitHub) and `processVotingRightsWithdrawalSettlement_()` (writes ledger + offchain + GitHub settlement JSON, updates request status) |
| `tokenomics/google_app_scripts/1rLl94j.../web_app.js` | 52-62 | Commented-out duplicate top-level `const` declarations (already defined in Code.js) |
| `tokenomics/google_app_scripts/1rLl94j.../.clasp.json` | filePushOrder | Set to `["web_app.js", "tdg_wix_dashboard.js", "Credentials.js", "Code.js"]` — Code.js loads last so its `doGet()` with action routing wins |

### Backend — Edgar Dispatch
| File | Lines | What |
|------|-------|------|
| `dao_client/.../dispatch.py` | 62-67 | Two new routing entries: `[VOTING RIGHTS WITHDRAWAL REQUEST]` → `processVotingRightsWithdrawalRequests`, `[VOTING RIGHTS WITHDRAWAL SETTLEMENT EVENT]` → `processVotingRightsWithdrawalSettlement` |

### Backend — Event Catalog
| File | What |
|------|------|
| `dao_client/.../events_catalog.json` | Updated `VOTING RIGHTS WITHDRAWAL REQUEST` canonical labels to match actual form fields; added new `VOTING RIGHTS WITHDRAWAL SETTLEMENT EVENT` with 11 canonical labels |

### Backend — CLI
| File | Lines | What |
|------|-------|------|
| `dao_client/.../modules/voting_rights_settlement.py` | 53 | Python CLI for governor-signed settlement via `build_event_cli` pattern |

### Frontend — DApp
| File | What |
|------|------|
| `dapp/withdraw_voting_rights_settlement.html` | Governor-gated settlement page. Two modes: reference pending request (dropdown from GitHub API `treasury-cache/contents/cash-out-requests`) or ad-hoc settlement with proof attachment. RSA-PKCS1v15 signing, Edgar submission. |
| `dapp/menu.js` | Added "Voting Rights Settlement" to "Governor only" section |

### Frontend — Existing Page (No Changes)
| File | What |
|------|------|
| `dapp/withdraw_voting_rights.html` | Existing contributor-facing cash-out request page — unchanged. New behavior: when Edgar dispatches the signed request, GAS auto-writes a JSON to GitHub. |

### Documentation
| File | What |
|------|------|
| `tokenomics/SCHEMA.md` | Added Meta Game Scoring Rubric spreadsheet documentation, rubric relationship chain (Meta Game → Initiatives → Ledger Col D), `Voting Rights Cash-Outs` tab schema for Telegram Chat Logs spreadsheet |

### Infrastructure — Server
| What | Details |
|------|---------|
| `.env` vars on `dao_protocol_nelanco` | `DAO_PROTOCOL_WEBHOOK_VOTING_RIGHTS_WITHDRAWAL_REQUEST` and `DAO_PROTOCOL_WEBHOOK_VOTING_RIGHTS_WITHDRAWAL_SETTLEMENT` both point to GAS webapp `AKfycbygmwRbyqse-.../exec` |
| Service restarted | `sudo systemctl restart truesight-dao-protocol` — confirmed healthy |

### Infrastructure — Google Sheets
| What | Details |
|------|---------|
| `Voting Rights Cash-Outs` tab | Created in Telegram Chat Logs spreadsheet `1qbZZhf-...` (sheetId 172058200) with 16-column header row |

---

## GAS Script Properties Required

The GAS project needs a `GITHUB_PAT` script property for writing JSONs to `TrueSightDAO/treasury-cache`:

```
Property Name: GITHUB_PAT
Property Value: <GitHub personal access token with repo scope>
```

Set via: GAS script editor → Project Settings → Script Properties → Add script property.

The existing `DAO_PROTOCOL_GITHUB_PAT` from the server's `.env` can be reused or a new fine-grained PAT can be created with `contents:write` permission on `TrueSightDAO/treasury-cache`.

---

## Env Vars (Server-Side, Already Set)

```
DAO_PROTOCOL_WEBHOOK_VOTING_RIGHTS_WITHDRAWAL_REQUEST=https://script.google.com/macros/s/AKfycbygmwRbyqse-dpCYMco0rb93NSgg-Jc1QIw7kUiBM7CZK6jnWnMB5DEjdoX_eCsvVs7/exec
DAO_PROTOCOL_WEBHOOK_VOTING_RIGHTS_WITHDRAWAL_SETTLEMENT=https://script.google.com/macros/s/AKfycbygmwRbyqse-dpCYMco0rb93NSgg-Jc1QIw7kUiBM7CZK6jnWnMB5DEjdoX_eCsvVs7/exec
```

Set on `dao_protocol_nelanco:/home/ubuntu/dao_protocol/.env`. Backup: `.env.bak.<timestamp>`.

---

## Deploy / Verify Commands

### GAS Project
```bash
# From tokenomics repo root
cd /Users/garyjob/Applications/tokenomics
python3 scripts/deploy_gas_project.py 1rLl94jQ9tDYdRvudnP0prPY5SEjvM07R4gPs6-vRyZEpSJhUqbiE3CZY --push

# Deploy to existing deployment (preferred — reuses stable URL)
cd google_app_scripts/1rLl94jQ9tDYdRvudnP0prPY5SEjvM07R4gPs6-vRyZEpSJhUqbiE3CZY
clasp deploy --deploymentId AKfycbygmwRbyqse-dpCYMco0rb93NSgg-Jc1QIw7kUiBM7CZK6jnWnMB5DEjdoX_eCsvVs7 --description "<message>"
```

### Verify handlers are live
```bash
# Request handler (scans for unprocessed requests)
curl -sL "https://script.google.com/macros/s/AKfycbygmwRbyqse-dpCYMco0rb93NSgg-Jc1QIw7kUiBM7CZK6jnWnMB5DEjdoX_eCsvVs7/exec?action=processVotingRightsWithdrawalRequests"

# Settlement handler (scans for unprocessed settlements)
curl -sL "https://script.google.com/macros/s/AKfycbygmwRbyqse-dpCYMco0rb93NSgg-Jc1QIw7kUiBM7CZK6jnWnMB5DEjdoX_eCsvVs7/exec?action=processVotingRightsWithdrawalSettlement"
```

Expected: `{"status":"ok","processed":0,"errors":[]}`

### Edgar deploy
```bash
cd /Users/garyjob/Applications/dao_client
./truesight_dao_client/server/deploy/deploy.sh
```

---

## Known Idiosyncrasies

### GAS V8 file-scope const conflict
This GAS project (`1rLl94j...`) has `Code.js` and `web_app.js` which are near-identical copies with duplicate `const` declarations. GAS V8 evaluates all files in a shared scope — duplicate `const` causes `SyntaxError`.

**Fix applied:** Commented-out duplicates in `web_app.js`; set `filePushOrder` to `["web_app.js", "tdg_wix_dashboard.js", "Credentials.js", "Code.js"]` so Code.js loads last and its `doGet()` (with action routing) wins.

**If redeploying:** Always maintain this filePushOrder. Do NOT add new `const` declarations that duplicate across files.

### doGet shadowing
`web_app.js` also has a `doGet()` that shadows the one in `Code.js` unless `filePushOrder` places Code.js LAST. The action routing (`?action=processVotingRights...`) lives in Code.js's `doGet()`. If the order is lost, the action endpoints return `{"error":"Signature parameter missing"}` instead of the expected `{"status":"ok","processed":0,"errors":[]}`.

### Column R as PROCESSED marker
Both handlers use Telegram Chat Logs Column R (index 17) to mark rows as processed:
- Request handler writes: `PROCESSED:VOTING_RIGHTS_REQUEST`
- Settlement handler writes: `PROCESSED:VOTING_RIGHTS_SETTLEMENT`
- Error variants: `PROCESSED:VOTING_RIGHTS_SETTLEMENT:ERROR_ALREADY_SETTLED`, `PROCESSED:VOTING_RIGHTS_SETTLEMENT:ERROR_MISSING_FIELDS`, `PROCESSED:VOTING_RIGHTS_SETTLEMENT:ERROR_GH_WRITE`

This follows the convention used by `process_repackaging_settlement.py` (writes `PROCESSED:REPACKAGING_SETTLEMENT` to Col R).

### Without GITHUB_PAT, handlers are no-op
If the GAS project doesn't have a `GITHUB_PAT` script property, the handlers will return errors for each row they try to process (GitHub write fails). No ledger updates will happen — the system idempotently retries on next dispatch.

### Double-processing guard
When a settlement references a `Cash-Out Request ID`, the handler fetches the request JSON from GitHub and checks `status !== "settled"`. If already settled, the row is marked `ERROR_ALREADY_SETTLED` and skipped. The request JSON is updated with `status: "settled"` after successful processing.
