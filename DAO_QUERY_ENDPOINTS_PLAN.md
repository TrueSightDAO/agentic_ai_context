# DAO Query Endpoints — Implementation Plan

**Status:** Draft · **Author:** Sophia Truesight (admin+sophia@truesight.me)
**Thread:** Telegram #6045 · **Date:** 2026-06-17

---

## 1. Problem Statement

Sophia (the autopilot) currently has no efficient way to answer queries like:
- "How many bags did SOHA buy last time?"
- "Which QR codes are managed by Kirsten?"
- "What inventory has passed through David Campbell's hands?"
- "Which QR codes match SKU X?"

Today she must either:
1. Read raw Google Sheets directly (multiple round-trips, schema guessing, truncation)
2. Search stale cached JSON files (partners-velocity.json, sell-through report)
3. Ask the governor for pointers

None of these scale. The data lives in Google Sheets (Main Ledger, Telegram & Submissions workbook), and Edgar (dao_protocol FastAPI on `172.31.23.207:8010`) already has the service accounts and Sheets client code to read them. What's missing are **read/query endpoints**.

---

## 2. Architecture Decision

**Extend Edgar (dao_protocol), don't build a separate tool.**

Edgar already:
- Has Google Sheets service accounts with access to all relevant ledgers
- Has a Sheets v4 client (`truesight_dao_client/server/sheets/base.py`)
- Has nginx routing, auth, and FastAPI framework
- Is the single source of truth for DAO operations

New query endpoints follow the same pattern as existing read endpoints (`GET /qr-code-check`, `GET /dao/check_digital_signature`).

---

## 3. The Four Query Scenarios

| # | Scenario | Source sheet(s) | Key filter columns |
|---|---|---|---|
| 1 | Historical sales by partner | `QR Code Sales` (gid=1003674539) in Telegram & Submissions workbook | Partner name (substring), date range, SKU |
| 2 | QR codes by store/owner/manager | `Agroverse QR codes` in Main Ledger | Manager Name (col U), Owner, Status, Currency/SKU |
| 3 | QR codes through a person's hands | `Inventory Movement` in Telegram & Submissions | SENDER NAME (col H), RECIPIENT NAME (col I), date range |
| 4 | QR codes by SKU | `Agroverse QR codes` in Main Ledger | Currency (col I, maps to SKU via Currencies tab) |

---

## 4. PR1 — Query Endpoints (live Sheets reads)

### 4.1 New Endpoints

All endpoints are `GET`, return JSON, and support **substring matching** on name/partner fields (as requested by Gary).

#### `GET /dao/transactions`

Query historical sales records.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `partner` | string | no | Substring match on buyer/partner name (e.g. `SOHA`, `soha`, `Campbell`) |
| `sku` | string | no | Filter by product/SKU (e.g. `ceremonial-cacao-fazenda-santa-ana-2023-200g`) |
| `from` | string (YYYYMMDD) | no | Start date (inclusive) |
| `to` | string (YYYYMMDD) | no | End date (inclusive) |
| `limit` | int | no | Max rows (default 100, max 1000) |

**Response:**
```json
[
  {
    "date": "20260115",
    "partner": "SOHA",
    "sku": "ceremonial-cacao-fazenda-santa-ana-2023-200g",
    "qty": 10,
    "qr_code": "",
    "value": 0,
    "status": "",
    "source_sheet": "QR Code Sales",
    "source_row": 142
  }
]
```

**Source:** `QR Code Sales` tab (gid=1003674539) in workbook `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`. Columns A–R per SCHEMA.md.

#### `GET /dao/qr-codes`

List QR codes by any attribute.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `manager` | string | no | Substring match on Manager Name (col U, header has line break) |
| `owner` | string | no | Substring match on Owner |
| `sku` | string | no | Substring match on Currency (col I) |
| `status` | string | no | Exact match on Status (MINTED, SOLD, SAMPLE, GIFT, etc.) |
| `limit` | int | no | Max rows (default 100, max 1000) |

**Response:**
```json
[
  {
    "qr_code": "2024OSCAR_20260121_12",
    "sku": "oscar-bahia-ceremonial-cacao-200g",
    "status": "MINTED",
    "manager": "Kirsten",
    "owner": "",
    "location": "",
    "ledger_name": "AGL#25",
    "source_row": 45
  }
]
```

**Source:** `Agroverse QR codes` tab in Main Ledger (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`). Columns A–V per SCHEMA.md.

#### `GET /dao/inventory-movements`

Track inventory through a person's hands.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `person` | string | no | Substring match on SENDER NAME or RECIPIENT NAME |
| `role` | string | no | `sender` or `recipient` — narrows the match to one column |
| `from` | string (YYYYMMDD) | no | Start date (inclusive) |
| `to` | string (YYYYMMDD) | no | End date (inclusive) |
| `limit` | int | no | Max rows (default 100, max 1000) |

**Response:**
```json
[
  {
    "date": "20260315",
    "sender": "Kirsten",
    "recipient": "SOHA",
    "sku": "ceremonial-cacao-fazenda-santa-ana-2023-200g",
    "qty": 10,
    "ledger_name": "AGL#25",
    "status": "PROCESSED",
    "source_row": 88
  }
]
```

**Source:** `Inventory Movement` tab in workbook `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`. Columns A–O per SCHEMA.md.

### 4.2 Implementation Details

**New files:**
- `truesight_dao_client/server/routes/query.py` — new router with the three endpoints
- `truesight_dao_client/server/sheets/transactions.py` — reads `QR Code Sales` tab
- `truesight_dao_client/server/sheets/qr_codes.py` — reads `Agroverse QR codes` tab
- `truesight_dao_client/server/sheets/inventory_movements.py` — reads `Inventory Movement` tab

**Modified files:**
- `truesight_dao_client/server/main.py` — mount the new `query` router

**Key design decisions:**
1. **Substring matching** on name fields (case-insensitive) — so `?partner=soha` matches `SOHA`, `?person=campbell` matches `David Campbell`
2. **Live reads from Sheets** — no caching in PR1. Every call hits the live sheet.
3. **Sheet ID and tab names** come from config/constants, not hardcoded in routes
4. **Error handling** — if a sheet is unreachable, return `{"error": "...", "results": []}` with 200 status (graceful degradation)
5. **Rate limiting** — Sheets API has its own quotas; we add a simple `max_rows` cap per endpoint

### 4.3 Testing

- Unit tests for each sheet reader (mock Sheets API responses)
- Integration tests against the actual sheets (optional, run manually)
- All 58 existing tests must still pass

---

## 5. PR2 — GitHub Flat-File Cache (documented, not implemented)

**Concept:** After PR1 is live and we observe which queries are frequent, add a cache layer.

- Cache files in `treasury-cache/` repo: `transactions/{partner_slug}.json`, `qr-codes/by-manager/{name_slug}.json`
- Read path: check cache → if fresh (TTL configurable) return → else read Sheets → write cache → return
- Cache bust: after `POST /dao/submit_contribution`, delete affected cache files
- No additional infrastructure — GitHub flat files are free, versioned, and readable by both Sophia and dao_protocol

**Filed in:** This document, §5. Not implemented until usage patterns justify it.

---

## 6. Roadmap

| Step | What | Who |
|------|------|-----|
| 1 | Review + approve this plan | Gary |
| 2 | Read SCHEMA.md in detail, map exact column names | Sophia |
| 3 | Build PR1 (query endpoints + tests) | Sophia → PR |
| 4 | Review + merge PR1 | Gary |
| 5 | Deploy to dao_protocol (systemd restart) | Sophia |
| 6 | UAT: test all 4 scenarios live | Gary + Sophia |
| 7 | Write PR2 plan doc, file in agentic_ai_context | Sophia |

---

## 7. Checklist

### PR1 — Query Endpoints

- [ ] Create `truesight_dao_client/server/sheets/transactions.py` — reads `QR Code Sales` tab
- [ ] Create `truesight_dao_client/server/sheets/qr_codes.py` — reads `Agroverse QR codes` tab
- [ ] Create `truesight_dao_client/server/sheets/inventory_movements.py` — reads `Inventory Movement` tab
- [ ] Create `truesight_dao_client/server/routes/query.py` — three GET endpoints
- [ ] Mount query router in `main.py`
- [ ] Add substring matching helper (case-insensitive)
- [ ] Add `max_rows` cap per endpoint
- [ ] Write unit tests for all three sheet readers
- [ ] Write unit tests for the query router
- [ ] Run full test suite (58 existing + new)
- [ ] Open PR on `dao_protocol` repo
- [ ] Merge (after Gary review)
- [ ] Deploy: `ssh` to `dao_protocol_nelanco`, `git pull`, restart systemd service
- [ ] UAT: call each endpoint with known test values

### PR2 — Cache Layer (filed, not implemented)

- [ ] Document cache schema (file paths, TTL, bust strategy)
- [ ] File in `agentic_ai_context/` for future reference

---

## 8. Schema Reference

### Workbook: TrueSight DAO Telegram & Submissions
`1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`

#### Tab: `QR Code Sales` (gid=1003674539)
| Col | Header | Type | Notes |
|-----|--------|------|-------|
| A | Telegram Update ID | Number | |
| B | Telegram Chatroom ID | Number | |
| C | Telegram Chatroom Name | String | |
| D | Telegram Message ID / Reporter | String | Legacy reporter name |
| E | Contributor Name | String | Person reporting sale |
| F | Contribution Made | String | Full sale message |
| G | Status date | Date | YYYYMMDD |
| H | Currency | String | Product/SKU name |
| I | Amount | Number | Quantity |
| J | Status | String | PROCESSING, TOKENIZED, ACCOUNTED, IGNORED |
| K | QR Code | String | QR code identifier |
| L | Owner email | String | Buyer email |
| M | Stripe Session ID | String | Stripe checkout session |
| N | Shipping Provider | String | Carrier name |
| O | Tracking Number | String | Tracking number |
| P | Sold by | String | Seller name |
| Q | Cash Collected By | String | Cash collector |
| R | Remarks | String | Audit notes |

#### Tab: `Inventory Movement` (gid varies)
| Col | Header | Type | Notes |
|-----|--------|------|-------|
| A | Telegram Update ID | Number | |
| B | Telegram Chatroom ID | Number | |
| C | Telegram Chatroom Name | String | |
| D | Telegram Message ID | Number | |
| E | Contributor Name | String | Reporter |
| F | Contribution Made | String | Full message |
| G | Status Date | Date | YYYYMMDD |
| H | SENDER NAME | String | Uppercase header |
| I | RECIPIENT NAME | String | Uppercase header |
| J | CURRENCY | String | SKU/product |
| K | AMOUNT | Number | Quantity |
| L | LEDGER_NAME | String | e.g. AGL#25 |
| M | LEDGER_URL | String | Spreadsheet URL |
| N | STATUS | String | NEW, unauthorized, PROCESSED, ERROR |
| O | RECORD ROWS | String | Destination row numbers |

### Workbook: Main Ledger
`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`

#### Tab: `Agroverse QR codes` (gid varies)
| Col | Header | Type | Notes |
|-----|--------|------|-------|
| A | QR Code | String | QR identifier |
| B | Status | String | MINTED, SOLD, SAMPLE, GIFT, etc. |
| C | Price | Number | Unit price |
| D | Product Image | String | Image URL |
| E | landing_page | String | Product page URL |
| F | farm name | String | Farm of origin |
| G | state | String | State of origin |
| H | country | String | Country of origin |
| I | Currency | String | SKU/product name (maps to Currencies tab) |
| J | Year | String | Harvest year |
| K | Product Name | String | Display name |
| L | Product Description | String | Description |
| M | Onboarding Email \nSent Date | String | Header has line break |
| N | Tree Planting Date\n(YYYYMMDD) | String | Header has line break |
| O | Tree ID | String | Associated tree ID |
| P | Notarization URL | String | Notarization link |
| Q | Notarization Date | String | Notarization date |
| R | Notarized By | String | Notarizer name |
| S | Owner | String | Current owner |
| T | Batch ID | String | Generation batch |
| U | Manager \nName | String | Header has line break; current manager |
| V | Ledger Name | String | NEW column |

---

## 9. Service Account Access

dao_protocol uses multiple service accounts for different sheets:
- `cypher_defense_gdrive_key.json` — Main Ledger access (Agroverse QR codes tab)
- `edgar_dapp_listener_key.json` — Telegram & Submissions workbook (QR Code Sales, Inventory Movement)

The sheet reader modules will accept an optional `key_path` parameter, defaulting to the appropriate key per sheet.

---

## 10. Open Questions

1. **Pagination:** For large result sets, should we add offset-based pagination? (Deferred — start with `limit` cap)
2. **Caching TTL:** What default TTL makes sense for the cache layer? (Deferred to PR2)
3. **Auth:** Should query endpoints require authentication? (Deferred — they're read-only and behind nginx already)
4. **SCHEMA.md updates:** If column headers change, who updates the schema mapping? (Gary or Sophia, as needed)
