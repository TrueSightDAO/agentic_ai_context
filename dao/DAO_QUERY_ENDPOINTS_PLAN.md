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

## 7. Deployment Checklist

When setting up a new autopilot instance or provisioning a new machine, perform these steps:

### 7.1 Disk cleanup cron

Install the disk cleanup script and cron job to prevent the autopilot box from running out of space:

```bash
# Create the cleanup script
sudo tee /usr/local/bin/disk-cleanup.sh > /dev/null << 'SCRIPT'
#!/bin/bash
# Disk cleanup for autopilot box
# Removes stale temp dirs, old logs, and pip cache

# Clean /tmp — remove dirs older than 1 day (not files, those may be in-use)
find /tmp -maxdepth 1 -type d -mtime +1 -exec rm -rf {} + 2>/dev/null || true

# Clean pip cache older than 7 days
find /home/ubuntu/.cache/pip -mtime +7 -type f -delete 2>/dev/null || true

# Clean apt cache
sudo apt-get clean -y 2>/dev/null || true

# Clean old journal logs (keep last 3 days)
sudo journalctl --vacuum-time=3d 2>/dev/null || true

echo "Disk cleanup complete"
df -h / | tail -1
SCRIPT

# Make it executable
sudo chmod +x /usr/local/bin/disk-cleanup.sh

# Add daily cron entry (runs at 3am)
(crontab -l 2>/dev/null | grep -q disk-cleanup) || \
  (crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/disk-cleanup.sh >> /var/log/disk-cleanup.log 2>&1") | crontab -
```

### 7.2 SSH key setup

The dao_protocol box (`172.31.23.207`) is only reachable via jump through `seni_ror`:

```bash
# Copy the NELANCO key to seni_ror for jump access
cat ~/.ssh/nelanco.pub | ssh ubuntu@seni_ror "cat >> ~/.ssh/authorized_keys"

# Test jump access
ssh -J ubuntu@seni_ror ubuntu@172.31.23.207 "hostname"
```

### 7.3 Service accounts

Verify the Google Sheets service accounts have access to the Main Ledger:

- `edgar_dapp_listener_key.json` — used by transactions + inventory movement queries
- `cypher_defense_gdrive_key.json` — used by QR code queries

### 7.4 Git clone + deploy

```bash
ssh -J ubuntu@seni_ror ubuntu@172.31.23.207 "
  cd /home/ubuntu && \
  git clone https://github.com/TrueSightDAO/dao_protocol.git && \
  cd dao_protocol && \
  pip install -e . && \
  sudo systemctl restart dao_protocol
"
```

### 7.5 Verify endpoints

```bash
curl https://edgar.truesight.me/ping
curl https://edgar.truesight.me/dao/qr-codes?manager=test&limit=1
curl https://edgar.truesight.me/dao/transactions?partner=test&limit=1
curl https://edgar.truesight.me/dao/inventory-movements?person=test&limit=1
```

---

## 8. Context Engineering

This plan follows the **context engineering** pattern (see Weaviate blog): instead of trying to make the LLM smarter through fine-tuning or prompt changes, we give it better context at the point of need.

Key design decisions:
1. **`lookup_event_docs` tool** — fetches live docs from the Edgar landing page before calling `submit_contribution`, so the LLM always has the correct format and when-to-use rules
2. **Edgar landing page as single source of truth** — update it once, every instance of the LLM gets the new docs
3. **Pre-flight check before action** — look up docs first, then act, rather than act and check after

This is more robust than hardcoding rules into the system prompt because:
- Docs can evolve without redeploying the LLM
- No false positives — the LLM sees the docs and makes the call
- Works for any future event type — add it to the landing page, and `lookup_event_docs` finds it
