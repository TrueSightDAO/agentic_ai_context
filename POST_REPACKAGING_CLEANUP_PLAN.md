# Post-Repackaging Cleanup — Implementation Plan (v2)

**Status:** Updated — awaiting governor review (§14)
**Handoff target:** Sophia (truesight_autopilot)
**Repos:** `TrueSightDAO/dao_client` + `TrueSightDAO/tokenomics`
**Date:** 2026-06-28
**Update:** v2 — rewritten per governor directive: follow Edgar event → dispatch → GAS pattern (no direct gspread)

---

## §1 — Context

### What
A new event type + CLI + GAS handler that closes the known gap between `[REPACKAGING BATCH EVENT]` submission and a fully populated Main Ledger. Today the repackaging GAS (`agroverse-inventory/gas/repackaging-currency-ingest/Code.gs`) writes only `Currencies` columns **A, B, N, O**. Everything else requires manual gspread ad-hoc edits (documented in `QR_GENERATION_DAO_CLIENT_POSTMORTEM.md:49-56`).

### Why
Every repackaging batch leaves four manual cleanup steps:
1. **Deplete** consumed inputs from `offchain asset location`
2. **Add** output rows (bars/ceremonial/etc.) to `offchain asset location`
3. **Set** `Currencies` columns C (`isSerializable`), D (product image), E–J (farm info), M (SKU Product ID)
4. **Rebuild** `store-inventory.json` so the website reflects reality

### Who
- **Governor:** Gary Teh
- **Builder:** Sophia (truesight_autopilot)
- **QA:** Local LLM (post-UAT)

---

## §2 — Architecture (CANONICAL)

Every other event type in the system follows this pipeline. This module MUST follow it too.

```
┌──────────┐    sign + POST      ┌───────┐   log to Telegram   ┌──────────────┐
│ dao_client│ ──────────────────→ │ Edgar │ ──────────────────→ │ Telegram     │
│ (CLI)    │  /dao/submit_       │       │   Chat Logs tab     │ Chat Logs    │
│          │  contribution       └───────┘                     └──────┬───────┘
└──────────┘                                                         │
                                                               dispatch.py
                                                               matches event tag
                                                                     │
                                                               ┌─────▼──────┐
                                                               │ GAS        │
                                                               │ webhook    │
                                                               │ handler    │
                                                               │            │
                                                               │ Writes to: │
                                                               │ • offchain │
                                                               │   asset    │
                                                               │   location │
                                                               │ • Currencies│
                                                               │ • triggers │
                                                               │   inventory│
                                                               │   snapshot │
                                                               └────────────┘
```

**Key properties:**
- RSA signing at the CLI (cryptographic proof of who ran it)
- Audit trail in Telegram Chat Logs (immutable, searchable)
- Edgar verifies signature before dispatching
- GAS handler does all sheet writes (server-side, no client credentials needed)
- First-match-wins routing in `dispatch.py` (matches existing pattern)

### Anti-pattern (DO NOT USE)
```
CLI ──gspread──→ Google Sheets   ← DIRECT WRITE, NO AUDIT TRAIL, NO SIGNING
```
This approach is explicitly rejected. The `onboard_partner.py` direct gspread pattern is a legacy exception, not the canonical pattern for new event types.

---

## §3 — Composition JSON Reference (input format)

The GAS handler's primary input is the composition JSON URL embedded in the event payload. Format (v2, stable):

```json
{
  "request_id": "b08d324b-...",
  "inputs": [
    {
      "line_kind": "from_holder_inventory",
      "currency": "8 Ounce Package Kraft Pouch  CP340992735BR",
      "quantity": 7,
      "unit_cost_usd": 8.51,
      "extended_cost_usd": 59.57
    }
  ],
  "outputs": [
    {
      "suggested_currency": "Ceremonial Cacao Kraft Pouch - ... | Kirsten 20260620 | San Francisco - AGL4",
      "units": 3,
      "unit_kind": "pouch",
      "weight_per_unit_grams": 200,
      "unit_cost_usd": 11.61,
      "line_total_usd": 34.84
    }
  ]
}
```

**Only `inputs` with `line_kind == "from_holder_inventory"` are depleted.** Packaging/custom lines do not have `offchain asset location` entries.

---

## §4 — Full Surface Checklist

Every new event type must be registered across **all** the surfaces where existing events live. This is the complete checklist extracted from analyzing the `[REPACKAGING BATCH EVENT]` footprint (27 files across 8 layers). The `[POST-REPACKAGING CLEANUP EVENT]` must be added to **every** applicable surface.

### Layer 1: Event Catalog (definition — source of truth)

| # | File (repo) | Action |
|---|-------------|--------|
| 1 | `dao_client/.../server/data/events_catalog.json` | Add new event entry with `category`, `description`, `canonical_labels`, `required_fields`, `dapp_page` |
| 2 | `dao_protocol/.../server/data/events_catalog.json` | Mirror #1 |

**Entry format** (add as last entry in `"Inventory & Supply Chain"` category, after `REPACKAGING BATCH EVENT`):
```json
"POST-REPACKAGING CLEANUP EVENT": {
  "category": "Inventory & Supply Chain",
  "description": "Populate offchain asset location + Currencies metadata after a repackaging batch",
  "canonical_labels": ["Composition URL", "Holder Name", "Farm Name", "State", "Country", "Year", "Landing Page", "Ledger URL", "SKU Mapping", "Deplete Inputs", "Add Output Locations", "Set Currencies Metadata", "Rebuild Inventory", "Submission Source"],
  "required_fields": ["Composition URL", "Holder Name"],
  "dapp_page": "post_repackaging_cleanup.html"
}
```

### Layer 2: Edgar Dispatch (server-side routing)

| # | File (repo) | Action |
|---|-------------|--------|
| 3 | `dao_client/.../server/dispatch.py` | Add `ROUTING` entry (see §6) |
| 4 | `dao_protocol/.../server/dispatch.py` | Mirror #3 |
| 5 | `sentiment_importer/app/controllers/dao_controller.rb` | Add `elsif text.include?('[POST-REPACKAGING CLEANUP EVENT]')` branch |
| 6 | `sentiment_importer/config/application.rb` | Add `config.post_repackaging_cleanup_processing_webhook_url` |
| 7 | `sentiment_importer-donation-mint/app/controllers/dao_controller.rb` | Mirror if that fork is active |

### Layer 3: GAS Handler (Google Apps Script)

| # | File (repo) | Action |
|---|-------------|--------|
| 8 | `tokenomics/google_app_scripts/.../post_repackaging_cleanup.gs` | New file — the `doGet(?action=processPostRepackagingCleanup)` function (see §7) |
| 9 | `tokenomics/.../grok_scoring_for_telegram_and_whatsapp_logs.js` | Add to recognized event types list (excluded from TDG scoring) |

### Layer 4: DApp (browser UI)

| # | File (repo) | Action |
|---|-------------|--------|
| 10 | `dapp/post_repackaging_cleanup.html` | New DApp page — follows `DAPP_PAGE_CONVENTIONS.md` exactly (see §4b) |
| 11 | `dapp/menu.js` | Add nav entry: `{ title: 'Post-Repackaging Cleanup', url: './post_repackaging_cleanup.html', section: 'Inventory & ledger' }` |

### Layer 5: CLI (command-line client)

| # | File (repo) | Action |
|---|-------------|--------|
| 12 | `dao_client/.../modules/post_repackaging_cleanup.py` | New module — `build_event_cli` wrapper (see §8 PR1) |
| 13 | `dao_protocol/.../modules/post_repackaging_cleanup.py` | Mirror #12 |

### Layer 6: Web Surfaces (public documentation)

| # | File (repo) | Action |
|---|-------------|--------|
| 14 | `truesight_me/contracts/index.html` | Add contract card (see §4c) |
| 15 | `truesight_autopilot/app/tools/lookup_event_docs.py` | Add to `_INTENT_GUIDANCE` and `_IMPORTANT_FIELDS` dicts |
| 16 | `truesight_autopilot/app/data/events_catalog_snapshot.json` | Auto-refreshed from live catalog (no manual edit needed) |

### Layer 7: Documentation

| # | File (repo) | Action |
|---|-------------|--------|
| 17 | `dao_client/INTEGRATION_GUIDE.md` | Add to event type reference table |
| 18 | `dao_protocol/INTEGRATION_GUIDE.md` | Mirror #17 |
| 19 | `dao_client/README.md` | Add to CLI module mapping table |
| 20 | `dao_protocol/README.md` | Mirror #19 |
| 21 | `agentic_ai_context/EDGAR_DAO_EXTRACTION_PLAN.md` | Add dispatch mapping |

### Layer 8: Infrastructure

| # | File (repo) | Action |
|---|-------------|--------|
| 22 | Env var on Edgar box | `DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP=<GAS URL>` |
| 23 | Env var on autopilot EC2 | Same as #22 |
| 24 | `sentiment_importer/config/application.rb` | `config.post_repackaging_cleanup_processing_webhook_url` |

### What Sophia does vs. what the governor does

| Responsibility | Who |
|---------------|-----|
| Code PRs (CLI, dispatch, events_catalog, DApp page, menu.js, contracts page, docs) | **Sophia** |
| GAS handler (Apps Script) | **Sophia** (writes + deploys) |
| Env vars on Edgar box / EC2 | **Governor** (provisions secrets) |
| Rails controller changes (`sentiment_importer`) | **Governor** or **Sophia** (TBD per handoff scope) |
| Sophia autopilot tooling (`lookup_event_docs.py`) | **Sophia** (own-repo change) |

---

## §4b — DApp Page Specification

**File:** `dapp/post_repackaging_cleanup.html`

Must follow `DAPP_PAGE_CONVENTIONS.md` exactly (full checklist in that doc, §2 of this plan summarises key rules). Reference page: `dapp/report_dao_expenses.html` (simple form, similar structure).

**Page purpose:** Operator-facing form that builds a `[POST-REPACKAGING CLEANUP EVENT]`, signs it, and POSTs to Edgar. Matches the CLI's canonical labels 1:1.

**Form fields:**

| Field | Input type | Required | Default |
|-------|-----------|----------|---------|
| Composition URL | `<input type="url">` | **Yes** | — |
| Holder Name | `<input type="text">` | **Yes** | — |
| Farm Name | `<input type="text">` | No | — |
| State | `<input type="text">` | No | — |
| Country | `<input type="text">` | No | — |
| Year | `<input type="text">` (4-digit) | No | — |
| Landing Page | `<input type="url">` | No | — |
| Ledger URL | `<input type="url">` | No | — |
| SKU Mapping | `<textarea>` (JSON) | No | `{}` |
| Deplete Inputs | `<input type="checkbox" checked>` | No | `true` |
| Add Output Locations | `<input type="checkbox" checked>` | No | `true` |
| Set Currencies Metadata | `<input type="checkbox" checked>` | No | `true` |
| Rebuild Inventory | `<input type="checkbox">` | No | `false` |

**Submission flow:**
1. Build `requestText`: event tag header, bullet lines for each label, `--------` divider
2. Call `signRequestText(requestText)` → appends `My Digital Signature`, `Request Transaction ID`, generation source, verify URL
3. POST `FormData { text: shareText }` to `EDGAR_SUBMIT`
4. Render signed payload + server response in `#submissionResult` `<pre>` blocks

**Menu entry** in `dapp/menu.js` (insert after Repackaging Planner, line 24):
```javascript
{ title: 'Post-Repackaging Cleanup', url: './post_repackaging_cleanup.html', section: 'Inventory & ledger' },
```

**Version bump:** Increment the `?v=` query on `<script src="./menu.js?v=...">` in every HTML page (and `service-worker.js` `URLS_TO_CACHE`).

---

## §4c — Smart Contracts Page (truesight.me/contracts)

**File:** `truesight_me/contracts/index.html`

Add a new `.contract-card` in the **"Inventory & Supply Chain"** category section (after the Repackaging Planner card at ~line 1465).

**Card template:**
```html
<div class="contract-card">
  <h3>Post-Repackaging Cleanup <span class="event-name">[POST-REPACKAGING CLEANUP EVENT]</span></h3>
  <p class="purpose">Automates the four cleanup steps after a repackaging batch is processed: depletes consumed inputs from offchain asset location, adds output rows for new products, sets Currencies metadata (isSerializable, SKU ID, farm info), and optionally rebuilds the store inventory snapshot so agroverse.shop reflects current stock.</p>
  <div class="meta">
    <span class="tag">Inventory Manager</span>
    <span>Required: Composition URL, Holder Name</span>
  </div>
  <div class="authority">
    <span class="auth-label">Authority: </span><span class="auth-value">Inventory Manager only</span>
    <div class="auth-note">Only wallets with the Inventory Manager role can sign. Unauthorized signers are rejected by Edgar with a 403 Forbidden response.</div>
  </div>
  <div class="sheets">
    <span class="sheet-label">Sheets: </span><span class="sheet-value"><a href="https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=1883963235" target="_blank" rel="noreferrer">offchain asset location</a>, <a href="https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=1552160318" target="_blank" rel="noreferrer">Currencies</a></span>
  </div>
  <details class="source-code">
    <summary>Source Code</summary>
    <ul>
      <li><a href="https://github.com/TrueSightDAO/dao_client/blob/main/truesight_dao_client/server/dispatch.py" target="_blank" rel="noreferrer">Dispatch Module (dao_client/server/dispatch.py)</a></li>
      <li><a href="https://github.com/TrueSightDAO/dao_client/blob/main/truesight_dao_client/modules/post_repackaging_cleanup.py" target="_blank" rel="noreferrer">Module: post_repackaging_cleanup.py</a></li>
      <li><a href="https://github.com/TrueSightDAO/tokenomics/blob/main/google_app_scripts/.../post_repackaging_cleanup.gs" target="_blank" rel="noreferrer">GAS Handler: post_repackaging_cleanup.gs</a></li>
      <li><a href="https://github.com/TrueSightDAO/sentiment_importer/blob/main/app/controllers/dao_controller.rb" target="_blank" rel="noreferrer">Edgar Controller: dao_controller.rb</a></li>
    </ul>
  </details>
</div>
```

**Category count:** Update `<span class="count">` from current count to count+1.

---

## §5 — New Event Type Specification

...

## §6 — Dispatch Route

### Addition to `dispatch.py` ROUTING list

Insert BEFORE the `[ASSET RECEIPT EVENT]` entry (line 61 in the current file):

```python
("[POST-REPACKAGING CLEANUP EVENT]", [
    ("POST_REPACKAGING_CLEANUP", "processPostRepackagingCleanup"),
], True),  # enqueue inventory snapshot (writes to offchain asset location)
```

### Env var required
```
DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP = <GAS webapp URL>
```
This must be set on the Edgar box and the autopilot EC2.

### Why `enqueue_inventory=True`
Because this event writes to `offchain asset location` and `Currencies`, the inventory snapshot (`store-inventory.json`) must be rebuilt afterward — same as `[INVENTORY MOVEMENT]` and `[DAO Inventory Expense Event]`.

## §5 — Target Sheets & Columns

### `offchain asset location` (Main Ledger, gid=1883963235)
| Col | Name | Action |
|-----|------|--------|
| A | Currency | Match against `inputs[].currency` for depletion; write `outputs[].suggested_currency` for addition |
| B | Location | Match/filter by Holder Name from event payload |
| C | Amount Managed | **Decrement** by `inputs[].quantity` for depletion; **write** `outputs[].units` for addition |
| D | Unit Cost | Write `outputs[].unit_cost_usd` for addition |
| E | Total Value | Write `outputs[].line_total_usd` for addition |

### `Currencies` (Main Ledger, gid=1552160318)
| Col | Name | Action |
|-----|------|--------|
| A | Currencies | Match against `outputs[].suggested_currency` |
| C | Serializable | Set to `"TRUE"` |
| E | landing_page | From event payload Landing Page |
| F | ledger | From event payload Ledger URL |
| G | farm name | From event payload Farm Name |
| H | state | From event payload State |
| I | country | From event payload Country |
| J | Year | From event payload Year |
| M | SKU Product ID | From event payload SKU Mapping (substring-matched against output label) |

---

## §5 — New Event Type Specification

### Event tag
```
[POST-REPACKAGING CLEANUP EVENT]
```

### Canonical labels (order matters — matches payload format)
| # | Label | Required | Validator | Description |
|---|-------|----------|-----------|-------------|
| 1 | `Composition URL` | **Yes** | `required, url` | URL to the composition JSON (GitHub raw) |
| 2 | `Holder Name` | **Yes** | `required` | Who physically holds the inventory (e.g. "Kirsten Ritschel") |
| 3 | `Farm Name` | No | — | Farm name for Currencies!G |
| 4 | `State` | No | — | State/region for Currencies!H |
| 5 | `Country` | No | — | Country for Currencies!I |
| 6 | `Year` | No | — | Harvest year for Currencies!J |
| 7 | `Landing Page` | No | `url_or_empty` | Landing page URL for Currencies!E |
| 8 | `Ledger URL` | No | `url_or_empty` | Ledger URL for Currencies!F |
| 9 | `SKU Mapping` | No | — | JSON string: `{"substring": "sku-id", ...}` |
| 10 | `Deplete Inputs` | No | — | `"true"` or `"false"` (default: `"true"`) |
| 11 | `Add Output Locations` | No | — | `"true"` or `"false"` (default: `"true"`) |
| 12 | `Set Currencies Metadata` | No | — | `"true"` or `"false"` (default: `"true"`) |
| 13 | `Rebuild Inventory` | No | — | `"true"` or `"false"` (default: `"false"`) |
| 14 | `Submission Source` | No | — | Standard source label |

### Default values (set in CLI via `defaults` dict)
```python
defaults={
    "Deplete Inputs": "true",
    "Add Output Locations": "true",
    "Set Currencies Metadata": "true",
    "Rebuild Inventory": "false",
    "Submission Source": "Post-Repackaging Cleanup CLI",
}
```

### DApp page
None (no browser equivalent — this is CLI-only, operator-facing post-repackaging tool).

---

## §6 — Dispatch Route

### Addition to `dispatch.py` ROUTING list

Insert BEFORE the `[ASSET RECEIPT EVENT]` entry (line 61 in the current file):

```python
("[POST-REPACKAGING CLEANUP EVENT]", [
    ("POST_REPACKAGING_CLEANUP", "processPostRepackagingCleanup"),
], True),  # enqueue inventory snapshot (writes to offchain asset location)
```

### Env var required
```
DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP = <GAS webapp URL>
```
This must be set on the Edgar box and the autopilot EC2.

### Why `enqueue_inventory=True`
Because this event writes to `offchain asset location` and `Currencies`, the inventory snapshot (`store-inventory.json`) must be rebuilt afterward — same as `[INVENTORY MOVEMENT]` and `[DAO Inventory Expense Event]`.

---

## §7 — GAS Handler Specification

### Location
`tokenomics/google_app_scripts/<deployment_id>/post_repackaging_cleanup.gs`

(Or added to an existing GAS project that already handles Telegram Chat Log processing — follow the pattern of `processRepackagingBatchesFromTelegramChatLogs`.)

### Entry point
```javascript
function processPostRepackagingCleanup(request) {
  // Standard GAS webapp entry: doGet/doPost → calls this
  // request.parameter.action === "processPostRepackagingCleanup"
}
```

### Processing logic

```
1. PARSE the Telegram Chat Log row for this event
   - Extract Composition URL, Holder Name, Farm Name, etc. from the text body
   - Parse the SKU Mapping JSON string

2. FETCH composition JSON from Composition URL
   - UrlFetchApp.fetch(compositionUrl)
   - Validate schema (inputs array, outputs array, request_id)

3. DEPLETE INPUTS (if Deplete Inputs != "false")
   For each input where line_kind == "from_holder_inventory":
     a. Open "offchain asset location" tab
     b. Find row where col A == input.currency AND col B == Holder Name
     c. If found:
        - Read current amount (col C)
        - new_amount = max(0, current_amount - input.quantity)
        - Write new_amount to col C
        - Log: "Depleted {currency} from {old} to {new} (consumed {qty})"
     d. If NOT found:
        - Log warning, skip
   Packaging/custom lines (line_kind != "from_holder_inventory"): skip with log

4. ADD OUTPUT LOCATIONS (if Add Output Locations != "false")
   For each output in composition.outputs:
     a. Check if row already exists: col A == output.suggested_currency AND col B == Holder Name
     b. If exists: skip (idempotent), log "already present"
     c. If NOT exists: append row:
        A = output.suggested_currency
        B = Holder Name
        C = output.units
        D = output.unit_cost_usd
        E = output.line_total_usd
        Log: "Added {currency} x{units} @ ${cost}"

5. SET CURRENCIES METADATA (if Set Currencies Metadata != "false")
   For each output in composition.outputs:
     a. Open "Currencies" tab
     b. Find row where col A == output.suggested_currency
     c. If found:
        - If col C is empty/false: set to "TRUE"
        - If Farm Name provided: set col G
        - If State provided: set col H
        - If Country provided: set col I
        - If Year provided: set col J
        - If Landing Page provided: set col E
        - If Ledger URL provided: set col F
        - If SKU Mapping provided: resolve SKU ID (substring match), set col M
        - Log per-column what was set (or skipped if already populated)
     d. If NOT found:
        - Log warning: "Currencies row not found for {currency} — repackaging GAS may not have run yet"

6. REBUILD INVENTORY (if Rebuild Inventory == "true")
   - Trigger the inventory snapshot publish (same mechanism as dispatch.py's inventory_snapshot.publish())
   - This rebuilds store-inventory.json on GitHub

7. LOG summary to a status column or a dedicated log
```

### GAS SKU Mapping logic (JavaScript)
```javascript
function resolveSkuId(suggestedCurrency, skuMappingJson) {
  if (!skuMappingJson) return null;
  var mapping = JSON.parse(skuMappingJson);
  var keys = Object.keys(mapping);
  for (var i = 0; i < keys.length; i++) {
    if (suggestedCurrency.indexOf(keys[i]) !== -1) {
      return mapping[keys[i]];
    }
  }
  return null;  // no match — col M left empty
}
```

### Idempotency
The handler must be safe to re-run:
- **Depletion:** Check current amount before decrementing. If already 0, skip.
- **Output locations:** Check if row already exists (A + B match). If yes, skip.
- **Currencies metadata:** Check each column before writing. If already populated, skip that column only.
- **Rebuild inventory:** The snapshot publisher is already idempotent (coalesces duplicate enqueues).

### Error handling
- If composition URL fetch fails (non-200): log error, abort processing
- If sheet is not found: log error, abort
- If individual row operations fail: log error per row, continue with remaining rows
- Never throw unhandled exceptions that could crash the GAS webapp

### Logging
Write a processing summary to a status column or dedicated log tab (follow existing GAS conventions). At minimum, log to `Logger.log()` for GAS console debugging.

---

## §8 — PR Breakdown (FINAL — v2 with all surfaces)

**Repos touched:** `dao_client` (primary), `dao_protocol` (mirrors), `dapp`, `truesight_me`, `tokenomics` (GAS), `sentiment_importer` (Rails dispatch), `truesight_autopilot` (Sophia tools)

---

### PR1 (dao_client): CLI module + events catalog + pyproject.toml

**Files changed:**
1. `truesight_dao_client/modules/post_repackaging_cleanup.py` — **NEW** (~40 lines)
2. `truesight_dao_client/server/data/events_catalog.json` — add event entry
3. `pyproject.toml` — add console script

**CLI module** — follows `repackaging_planner.py` exactly, a thin `build_event_cli` wrapper:

```python
#!/usr/bin/env python3
"""Submit [POST-REPACKAGING CLEANUP EVENT] to Edgar.

Populates offchain asset location + Currencies metadata after a repackaging
batch has been processed by the repackaging-currency-ingest GAS.

DApp equivalent: dapp.truesight.me/post_repackaging_cleanup.html

Run from the dao_client repo root:
    python -m truesight_dao_client.modules.post_repackaging_cleanup --help
"""
import sys

from ..edgar_client import build_event_cli
from ..validators import required, url_or_empty

main = build_event_cli(
    event_name='POST-REPACKAGING CLEANUP EVENT',
    canonical_labels=[
        'Composition URL',
        'Holder Name',
        'Farm Name',
        'State',
        'Country',
        'Year',
        'Landing Page',
        'Ledger URL',
        'SKU Mapping',
        'Deplete Inputs',
        'Add Output Locations',
        'Set Currencies Metadata',
        'Rebuild Inventory',
        'Submission Source',
    ],
    required_labels=['Composition URL', 'Holder Name'],
    validators={
        'Composition URL': required,
        'Holder Name': required,
        'Landing Page': url_or_empty,
        'Ledger URL': url_or_empty,
    },
    defaults={
        'Deplete Inputs': 'true',
        'Add Output Locations': 'true',
        'Set Currencies Metadata': 'true',
        'Rebuild Inventory': 'false',
        'Submission Source': 'Post-Repackaging Cleanup CLI',
    },
    dapp_page='post_repackaging_cleanup.html',
)

if __name__ == "__main__":
    sys.exit(main())
```

**Dependencies:** None beyond existing `build_event_cli` / `EdgarClient` / `validators`.

**Console script** in `pyproject.toml`:
```toml
truesight-dao-post-repackaging-cleanup = "truesight_dao_client.modules.post_repackaging_cleanup:main"
```

**Events catalog entry** in `events_catalog.json` (add to `"Inventory & Supply Chain"`, after REPACKAGING):
```json
"POST-REPACKAGING CLEANUP EVENT": {
  "category": "Inventory & Supply Chain",
  "description": "Populate offchain asset location + Currencies metadata after a repackaging batch",
  "canonical_labels": ["Composition URL", "Holder Name", "Farm Name", "State", "Country", "Year", "Landing Page", "Ledger URL", "SKU Mapping", "Deplete Inputs", "Add Output Locations", "Set Currencies Metadata", "Rebuild Inventory", "Submission Source"],
  "required_fields": ["Composition URL", "Holder Name"],
  "dapp_page": "post_repackaging_cleanup.html"
}
```

---

### PR2 (dao_client): Dispatch route

**File changed:** `truesight_dao_client/server/dispatch.py`

Add to `ROUTING` list (after `[REPACKAGING BATCH EVENT]`, before `[CURRENCY CONVERSION EVENT]`):

```python
("[POST-REPACKAGING CLEANUP EVENT]", [
    ("POST_REPACKAGING_CLEANUP", "processPostRepackagingCleanup"),
], True),
```

**Env var** for governor to provision after PR2 merges:
```bash
DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP=<GAS webapp deployment URL>
```

---

### PR3 (dapp): DApp page + menu entry

**Files changed:**
1. `dapp/post_repackaging_cleanup.html` — **NEW** (full page following `DAPP_PAGE_CONVENTIONS.md`)
2. `dapp/menu.js` — add nav entry

**DApp page** — must follow §4b spec (full DApp conventions checklist). Reference implementation: `dapp/report_dao_expenses.html`.

**Menu entry** (insert after Repackaging Planner, line 24):
```javascript
{ title: 'Post-Repackaging Cleanup', url: './post_repackaging_cleanup.html', section: 'Inventory & ledger' },
```

**Version bump:** Increment `?v=` on `<script src="./menu.js?v=...">` in every HTML page and `service-worker.js`.

---

### PR4 (truesight_me): Smart contracts page

**File changed:** `truesight_me/contracts/index.html`

Add contract card per §4c template. Update category count.

---

### PR5 (tokenomics): GAS handler

**File:** New `.gs` file, following the logic in §7.

**Also update:** `grok_scoring_for_telegram_and_whatsapp_logs.js` — add `[POST-REPACKAGING CLEANUP EVENT]` to recognized event types (excluded from TDG scoring).

**Deployment:** Deploy webapp, update `DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP` env var.

---

### PR6 (dao_client mirror): Sync dao_protocol

**Files changed** (mirror PR1, PR2 changes in dao_protocol):
1. `truesight_dao_client/modules/post_repackaging_cleanup.py` — mirror
2. `truesight_dao_client/server/data/events_catalog.json` — mirror
3. `truesight_dao_client/server/dispatch.py` — mirror
4. `pyproject.toml` — mirror
5. `README.md` — add to CLI module mapping table
6. `INTEGRATION_GUIDE.md` — add to event type reference table

---

### PR7 (sentiment_importer): Rails dispatch

**Files changed:**
1. `app/controllers/dao_controller.rb` — add `elsif` branch for `[POST-REPACKAGING CLEANUP EVENT]`
2. `config/application.rb` — add `config.post_repackaging_cleanup_processing_webhook_url`

(If sentiment_importer-donation-mint fork is active, mirror there too.)

---

### PR8 (truesight_autopilot): Sophia tooling

**File changed:** `app/tools/lookup_event_docs.py`

Add to `_INTENT_GUIDANCE` and `_IMPORTANT_FIELDS` dicts:

```python
# In _INTENT_GUIDANCE:
"post-repackaging cleanup": "POST-REPACKAGING CLEANUP EVENT",
"populate offchain": "POST-REPACKAGING CLEANUP EVENT",
"set currencies metadata": "POST-REPACKAGING CLEANUP EVENT",

# In _IMPORTANT_FIELDS:
"POST-REPACKAGING CLEANUP EVENT": "Composition URL (required), Holder Name (required), Farm Name, State, Country, Year, Landing Page, SKU Mapping (JSON)",
```

---

### PR9 (dao_client): Tests

**Test file:** `tests/test_post_repackaging_cleanup.py`

Same test cases as §13 (18 tests covering CLI, dispatch, DApp, and integration).

---

### Summary: 9 PRs across 6 repos

| PR | Repo | What |
|----|------|------|
| PR1 | `dao_client` | CLI module + events catalog + pyproject.toml |
| PR2 | `dao_client` | Dispatch route |
| PR3 | `dapp` | DApp page + menu.js |
| PR4 | `truesight_me` | Contracts page card |
| PR5 | `tokenomics` | GAS handler + scoring exclusion |
| PR6 | `dao_protocol` | Mirror PR1 + PR2 + docs |
| PR7 | `sentiment_importer` | Rails dispatch |
| PR8 | `truesight_autopilot` | Sophia tooling |
| PR9 | `dao_client` | Tests

---

## §9 — Gates (FINAL)

| Gate | What | Who |
|------|------|-----|
| **G1** | PR1 (CLI + events catalog + pyproject.toml) merged to `dao_client` `main` | Sophia → Governor |
| **G2** | PR2 (dispatch route) merged to `dao_client` `main` | Sophia → Governor |
| **G3** | PR3 (DApp page + menu.js) merged to `dapp` `main` | Sophia → Governor |
| **G4** | PR4 (contracts card) merged to `truesight_me` `main` | Sophia → Governor |
| **G5** | PR5 (GAS handler) deployed to GAS, env var provisioned on Edgar box + EC2 | Sophia → Governor |
| **G6** | PR6 (dao_protocol mirrors) merged | Sophia → Governor |
| **G7** | PR7 (sentiment_importer Rails dispatch) merged | Sophia → Governor |
| **G8** | PR8 (truesight_autopilot tooling) merged | Sophia → Governor |
| **G9** | PR9 (tests) merged + `pytest` all pass | Sophia |
| **G10** | `python -m truesight_dao_client.modules.post_repackaging_cleanup --help` clean | Sophia |
| **G11** | Dry-run against b08d324b prints expected signed payload | Governor / QA |
| **G12** | DApp page loads correctly at dapp.truesight.me/post_repackaging_cleanup.html | Governor / QA |
| **G13** | Contracts page shows new card at truesight.me/contracts | Governor / QA |
| **G14** | Real run against b08d324b — verify Main Ledger sheet changes | Governor / QA |
| **G15** | Real run idempotent — second run no duplicate writes | Governor / QA |
| **G16** | Post-UAT sign-off | Governor |

---

## §10 — RESUME HERE

**After the plan is committed + Sophia pinged:** Sophia reads this file via `read_repo_file` on GitHub `main`, refreshes her clone, posts kickoff in thread 7987, and awaits the GO signal.

**RESUME HERE = PR1** (CLI module `post_repackaging_cleanup.py` — the thin `build_event_cli` wrapper + events catalog entry + pyproject.toml).

**Execution order (sequential, one PR per turn):**
```
PR1 → G1 → PR2 → G2 → PR3 → G3 → PR4 → G4 → PR5 → G5 → PR6 → G6 → PR7 → G7 → PR8 → G8 → PR9 → G9 → G10 → hand off for G11—G16 UAT
```

---

## §11 — Roadmap

```
Day 1: PR1 (CLI + events catalog, ~45 lines) + PR2 (dispatch, ~3 lines)
Day 2: PR3 (DApp page, ~250 lines) + PR4 (contracts card, ~30 lines)
Day 3: PR5 (GAS handler, ~150 lines) + deploy + provision env var
Day 4: PR6 (dao_protocol mirrors) + PR7 (sentiment_importer Rails)
Day 5: PR8 (truesight_autopilot tooling) + PR9 (tests, ~200 lines)
Day 5-6: G9-G10 self-checks
Day 6-7: UAT (dry-run, DApp, contracts page, real run, idempotency)
Day 7: G16 sign-off
```

---

## §12 — User Acceptance Testing (UAT)

### UAT-1: CLI help
```bash
cd /Users/garyjob/Applications/dao_client
python3 -m truesight_dao_client.modules.post_repackaging_cleanup --help
```
**Expected:** Clean help listing all 14 canonical labels with flags, defaults, required fields. Shows `DApp equivalent: dapp.truesight.me/post_repackaging_cleanup.html`.

### UAT-2: DApp page loads
1. Open `https://dapp.truesight.me/post_repackaging_cleanup.html`
2. **Expected:** Page loads with DAO logo, nav dropdown (includes "Post-Repackaging Cleanup" under "Inventory & ledger"), all 12 form fields per §4b, TDG balance badge, status indicator
3. Verify meta tags: Open Graph (6 tags), Twitter Card (4 tags), favicon
4. Verify `menu.js` dropdown includes `{ title: 'Post-Repackaging Cleanup', url: './post_repackaging_cleanup.html', section: 'Inventory & ledger' }`

### UAT-3: Contracts page updated
1. Open `https://truesight.me/contracts`
2. **Expected:** New card "Post-Repackaging Cleanup `[POST-REPACKAGING CLEANUP EVENT]`" under "Inventory & Supply Chain"
3. Verify: description accurate, authority shows "Inventory Manager only", sheet links correct, source code links resolve

### UAT-4: Events catalog serves new entry
```bash
curl https://edgar.truesight.me/events-catalog | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['events']['POST-REPACKAGING CLEANUP EVENT'])"
```
**Expected:** Returns the full event entry with category, description, labels, required_fields, dapp_page.

### UAT-5: Dry-run against b08d324b (CLI)
```bash
python3 -m truesight_dao_client.modules.post_repackaging_cleanup \
    --composition-url "https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/b08d324b-e2f4-4645-9d25-ee43f9e7d9e0.json" \
    --holder-name "Kirsten Ritschel" \
    --farm-name "Oscar's Farm, Bahia" \
    --state "Bahia" \
    --country "Brazil" \
    --year "2024" \
    --landing-page "https://agroverse.shop/shipments/agl4" \
    --ledger-url "https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=1762218634" \
    --sku-mapping '{"Ceremonial Cacao Kraft Pouch": "ceremonial-cacao-kraft-pouch-200g", "Agroverse 81% Cacao Chocolate Bar 50g": "agroverse-81-cacao-chocolate-bar-50g"}' \
    --dry-run
```

**Expected output:** Signed share text with all labels populated:
```
[POST-REPACKAGING CLEANUP EVENT]

- Composition URL: https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/b08d324b-...
- Holder Name: Kirsten Ritschel
- Farm Name: Oscar's Farm, Bahia
- State: Bahia
- Country: Brazil
- Year: 2024
- Landing Page: https://agroverse.shop/shipments/agl4
- Ledger URL: https://docs.google.com/spreadsheets/d/...
- SKU Mapping: {"Ceremonial Cacao Kraft Pouch": "ceremonial-cacao-kraft-pouch-200g", ...}
- Deplete Inputs: true
- Add Output Locations: true
- Set Currencies Metadata: true
- Rebuild Inventory: false
- Submission Source: Post-Repackaging Cleanup CLI

-----BEGIN DAO SIGNED CONTRIBUTION-----
...
-----END DAO SIGNED CONTRIBUTION-----
```

### UAT-6: Real run against b08d324b
```bash
# SAME AS UAT-2 but WITHOUT --dry-run
python3 -m truesight_dao_client.modules.post_repackaging_cleanup \
    --composition-url "..." \
    --holder-name "Kirsten Ritschel" \
    --farm-name "Oscar's Farm, Bahia" \
    --state "Bahia" --country "Brazil" --year "2024" \
    --landing-page "https://agroverse.shop/shipments/agl4" \
    --ledger-url "..." \
    --sku-mapping '{"Ceremonial Cacao Kraft Pouch": "ceremonial-cacao-kraft-pouch-200g", "Agroverse 81% Cacao Chocolate Bar 50g": "agroverse-81-cacao-chocolate-bar-50g"}'
```

**Expected:** HTTP 200 from Edgar. Edgar logs to Telegram Chat Logs. Dispatch fires webhook. GAS handler processes.

**Post-run verification checklist:**
- [ ] Telegram Chat Logs shows `[POST-REPACKAGING CLEANUP EVENT]` entry
- [ ] `offchain asset location`: "8 Ounce Package Kraft Pouch CP340992735BR" under Kirsten → 0
- [ ] `offchain asset location`: 2 new rows for ceremonial (x3) + bars (x15) under Kirsten
- [ ] `Currencies`: `isSerializable` = TRUE on both CC and CB rows
- [ ] `Currencies`: farm info E-J populated on both rows
- [ ] `Currencies`: SKU Product ID M populated on both rows
- [ ] `store-inventory.json` updated (because `enqueue_inventory=True`)

### UAT-7: Idempotency
Re-run the same command. **Expected:**
- [ ] Edgar accepts the duplicate event (HTTP 200)
- [ ] Telegram Chat Logs shows a second entry
- [ ] GAS handler detects all outputs already in `offchain asset location` → skips addition
- [ ] GAS handler detects `isSerializable` already TRUE → skips
- [ ] GAS handler detects farm info already populated → skips
- [ ] No duplicate rows created, no data corruption

### UAT-8: Rebuild inventory flag
```bash
python3 -m truesight_dao_client.modules.post_repackaging_cleanup \
    --composition-url "..." \
    --holder-name "Kirsten Ritschel" \
    --attr "Rebuild Inventory=true" \
    --attr "Deplete Inputs=false" \
    --attr "Add Output Locations=false" \
    --attr "Set Currencies Metadata=false"
```

**Post-run verification:**
- [ ] `store-inventory.json` rebuilt on GitHub
- [ ] agroverse.shop reflects current stock

### UAT-9: Error handling
```bash
# Invalid composition URL
python3 -m ... --composition-url "https://example.com/nonexistent.json" --dry-run
# Expected: dry-run still succeeds (CLI doesn't fetch), but payload shows the bad URL

# Real run: Edgar submits successfully, GAS handler fetches URL → returns 404
# Expected: GAS handler logs error, aborts gracefully, no sheet corruption
```

---

## §13 — Unit Test Specifications (for PR4)

```python
# tests/test_post_repackaging_cleanup.py

import pytest
from fastapi.testclient import TestClient
from truesight_dao_client.server.main import create_app
from truesight_dao_client.server import dispatch
from truesight_dao_client.server.jobs import inventory_snapshot

# ---------- CLI tests ----------

def test_cli_help(capsys):
    """--help prints all canonical labels."""
    from truesight_dao_client.modules.post_repackaging_cleanup import main as cli_main
    try:
        cli_main(["--help"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "Composition URL" in captured.out
    assert "Holder Name" in captured.out
    assert "SKU Mapping" in captured.out
    assert "Deplete Inputs" in captured.out
    assert "--dry-run" in captured.out


def test_cli_required_fields_missing(monkeypatch):
    """Missing --composition-url or --holder-name → SystemExit."""
    from truesight_dao_client.modules.post_repackaging_cleanup import main as cli_main
    # Mock EdgarClient.from_env to avoid .env lookup during dry-run
    with pytest.raises(SystemExit):
        cli_main(["--dry-run"])


def test_cli_dry_run_output(monkeypatch, capsys):
    """--dry-run prints signed share text, does NOT POST to Edgar."""
    from truesight_dao_client.modules.post_repackaging_cleanup import main as cli_main
    from ..edgar_client import EdgarClient
    monkeypatch.setattr(EdgarClient, "from_env", lambda: EdgarClient(
        email="test@test.com",
        public_key="fake",
        private_key="fake",
        edgar_url="https://edgar.example.com",
    ))
    cli_main([
        "--composition-url", "https://example.com/comp.json",
        "--holder-name", "Test Holder",
        "--dry-run",
    ])
    captured = capsys.readouterr()
    assert "[POST-REPACKAGING CLEANUP EVENT]" in captured.out
    assert "BEGIN DAO SIGNED CONTRIBUTION" in captured.out


def test_cli_defaults_applied(monkeypatch, capsys):
    """Defaults for boolean flags appear in payload."""
    from truesight_dao_client.modules.post_repackaging_cleanup import main as cli_main
    from ..edgar_client import EdgarClient
    monkeypatch.setattr(EdgarClient, "from_env", lambda: EdgarClient(
        email="test@test.com", public_key="fake", private_key="fake",
        edgar_url="https://edgar.example.com",
    ))
    cli_main([
        "--composition-url", "https://example.com/comp.json",
        "--holder-name", "Test Holder",
        "--dry-run",
    ])
    captured = capsys.readouterr()
    assert "- Deplete Inputs: true" in captured.out
    assert "- Add Output Locations: true" in captured.out
    assert "- Rebuild Inventory: false" in captured.out


def test_cli_all_flags_can_be_overridden(monkeypatch, capsys):
    """--attr overrides for boolean flags."""
    from truesight_dao_client.modules.post_repackaging_cleanup import main as cli_main
    from ..edgar_client import EdgarClient
    monkeypatch.setattr(EdgarClient, "from_env", lambda: EdgarClient(
        email="test@test.com", public_key="fake", private_key="fake",
        edgar_url="https://edgar.example.com",
    ))
    cli_main([
        "--composition-url", "https://example.com/comp.json",
        "--holder-name", "Test Holder",
        "--attr", "Deplete Inputs=false",
        "--attr", "Add Output Locations=false",
        "--attr", "Set Currencies Metadata=false",
        "--attr", "Rebuild Inventory=true",
        "--dry-run",
    ])
    captured = capsys.readouterr()
    assert "- Deplete Inputs: false" in captured.out
    assert "- Rebuild Inventory: true" in captured.out


def test_cli_sku_mapping_in_payload(monkeypatch, capsys):
    """SKU Mapping JSON string appears correctly in signed payload."""
    from truesight_dao_client.modules.post_repackaging_cleanup import main as cli_main
    from ..edgar_client import EdgarClient
    monkeypatch.setattr(EdgarClient, "from_env", lambda: EdgarClient(
        email="test@test.com", public_key="fake", private_key="fake",
        edgar_url="https://edgar.example.com",
    ))
    cli_main([
        "--composition-url", "https://example.com/comp.json",
        "--holder-name", "Test Holder",
        "--sku-mapping", '{"CC": "sku-cc", "CB": "sku-cb"}',
        "--dry-run",
    ])
    captured = capsys.readouterr()
    assert '- SKU Mapping: {"CC": "sku-cc", "CB": "sku-cb"}' in captured.out

# ---------- Dispatch tests ----------

def test_dispatch_route_matches(monkeypatch):
    """Text containing [POST-REPACKAGING CLEANUP EVENT] is matched by dispatch."""
    triggered = []
    monkeypatch.setattr(dispatch.webhook_trigger, "trigger", lambda url, action: triggered.append((url, action)))
    monkeypatch.setattr(dispatch, "_webhook_url", lambda key: f"https://example.com/{key}")
    monkeypatch.setattr(dispatch.inventory_snapshot, "publish", lambda: triggered.append("snapshot"))

    dispatch.dispatch_event("[POST-REPACKAGING CLEANUP EVENT]\n- Holder Name: Test\n")
    assert len(triggered) == 2  # webhook + snapshot
    assert triggered[1] == "snapshot"


def test_dispatch_route_no_match():
    """Unrelated event text does not trigger the route."""
    import os
    # Ensure no env var is set for the cleanup route
    old = os.environ.pop("DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP", None)
    try:
        # dispatch_event should silently skip (no matching tag for this text)
        dispatch.dispatch_event("[SOME OTHER EVENT]\n...")
        # Should not raise
    finally:
        if old:
            os.environ["DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP"] = old


def test_dispatch_route_no_webhook_url_logs_warning(monkeypatch, caplog):
    """When env var is unset, dispatch logs warning and skips webhook."""
    monkeypatch.setattr(dispatch, "_webhook_url", lambda key: "")
    monkeypatch.setattr(dispatch.inventory_snapshot, "publish", lambda: None)

    dispatch.dispatch_event("[POST-REPACKAGING CLEANUP EVENT]\n...")
    assert "no webhook URL" in caplog.text or "POST_REPACKAGING_CLEANUP" in caplog.text

# ---------- Integration test ----------

def test_end_to_end_signed_submission(monkeypatch):
    """Full flow: CLI signs, Edgar verifies, dispatch triggers webhook + snapshot."""
    from fastapi.testclient import TestClient
    from truesight_dao_client.server.main import create_app
    # ... set up TestClient, mock GAS webhook response, verify dispatch
    pass
```

---

## §14 — Acceptance Criteria

- [ ] `truesight-dao-post-repackaging-cleanup --help` prints all 14 canonical labels with DApp reference
- [ ] CLI module uses `build_event_cli` (NOT custom argparse, NOT gspread)
- [ ] Events catalog (`events_catalog.json`) has new entry at `GET /events-catalog`
- [ ] `--dry-run` prints signed share text without hitting Edgar
- [ ] Dispatch route matches `[POST-REPACKAGING CLEANUP EVENT]` and enqueues inventory snapshot
- [ ] `edgar.truesight.me/events-catalog` returns the new event in JSON
- [ ] `dapp.truesight.me/post_repackaging_cleanup.html` loads correctly with all form fields
- [ ] DApp nav dropdown includes the new page under "Inventory & ledger"
- [ ] `truesight.me/contracts` shows new contract card in "Inventory & Supply Chain"
- [ ] GAS handler processes Telegram Chat Log entry and writes to sheets
- [ ] GAS handler is idempotent (safe to re-run)
- [ ] GAS handler handles errors gracefully (bad URL, missing rows)
- [ ] All 9 PRs merged across all repos
- [ ] All unit tests pass (`pytest tests/test_post_repackaging_cleanup.py -v`)
- [ ] Real run against b08d324b produces correct sheet changes
- [ ] Real run is idempotent — second run produces no duplicate writes
- [ ] `--rebuild-inventory` flag triggers snapshot rebuild
- [ ] Module follows existing code conventions (build_event_cli, canonical labels, validators, dapp_page reference)

---

## §15 — Sophia Feedback (2026-06-28)

Sophia opened PR https://github.com/TrueSightDAO/dao_protocol/pull/133 with two issues:

1. **Wrong repo.** The plan specifies `TrueSightDAO/dao_client`, not `dao_protocol`. All CLI modules live in `dao_client/truesight_dao_client/modules/`. The dispatch route lives in `dao_client/truesight_dao_client/server/dispatch.py`.

2. **Wrong architecture.** The PR uses direct gspread writes (following the `onboard_partner.py` pattern). This plan has been updated to v2 to specify the canonical Edgar event → dispatch → GAS pattern instead. The CLI module must be a thin `build_event_cli` wrapper that signs and POSTs to Edgar. All sheet writes must happen in a new GAS handler, triggered by Edgar's dispatch.

**Action for Sophia:** Close PR #133. Start fresh with this v2 plan. RESUME HERE = PR1 (the CLI wrapper in dao_client, ~25 lines using `build_event_cli`).
