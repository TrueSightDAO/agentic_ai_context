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

## §4 — Target Sheets & Columns

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

## §8 — PR Breakdown (REVISED)

### PR1 (dao_client): CLI module — `modules/post_repackaging_cleanup.py` (NEW FILE)

**Pattern:** Follow `repackaging_planner.py` — a ~25-line wrapper using `build_event_cli()`.

```python
#!/usr/bin/env python3
"""Submit [POST-REPACKAGING CLEANUP EVENT] to Edgar.

Populates offchain asset location + Currencies metadata after a repackaging
batch has been processed by the repackaging-currency-ingest GAS.

CLI-only (no DApp equivalent).

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
)

if __name__ == "__main__":
    sys.exit(main())
```

**Dependencies:** None beyond existing `build_event_cli` / `EdgarClient` / `validators`.

**Console script entry** in `pyproject.toml`:
```toml
truesight-dao-post-repackaging-cleanup = "truesight_dao_client.modules.post_repackaging_cleanup:main"
```

**IMPORTANT:** The SKU Mapping label value is a JSON string. The operator passes it as:
```
--sku-mapping '{"Ceremonial Cacao Kraft Pouch": "ceremonial-cacao-kraft-pouch-200g", "Agroverse 81% Cacao Chocolate Bar 50g": "agroverse-81-cacao-chocolate-bar-50g"}'
```
This gets embedded as `- SKU Mapping: {"Ceremonial Cacao...": ...}` in the signed payload. The GAS handler parses it with `JSON.parse()`.

---

### PR2 (dao_client): Dispatch route — `server/dispatch.py`

**Change:** Add one entry to the `ROUTING` list.

Insert after the `[REPACKAGING BATCH EVENT]` entry (line 49) and before `[CURRENCY CONVERSION EVENT]` (line 50):

```python
("[POST-REPACKAGING CLEANUP EVENT]", [
    ("POST_REPACKAGING_CLEANUP", "processPostRepackagingCleanup"),
], True),
```

**Env var** to provision on the Edgar box + autopilot EC2:
```bash
DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP=<GAS webapp deployment URL>
```

---

### PR3 (tokenomics): GAS handler — Google Apps Script

**File:** New `.gs` file in the appropriate GAS project (the one that hosts the existing Telegram Chat Log processing handlers — e.g., the project containing `processRepackagingBatchesFromTelegramChatLogs`).

**Function signature:**
```javascript
function processPostRepackagingCleanup(request) { ... }
```

**Implementation:** Follows the logic in §7 above.

**Deployment:** Deploy as a new webapp version (or add to existing deployment if the GAS project already serves multiple handlers via the `?action=` query parameter). Update the `DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP` env var with the new deployment URL.

**Testing the GAS handler (manual):**
1. Submit a `[POST-REPACKAGING CLEANUP EVENT]` from the CLI with `--dry-run` to see the signed payload
2. Copy the payload text and manually POST it to the GAS webapp URL (or use the GAS editor's debugger)
3. Verify sheet changes in the Main Ledger

---

### PR4: Tests

**Test file:** `tests/test_post_repackaging_cleanup.py`

**Framework:** pytest + monkeypatch + TestClient (matching repo conventions)

**Test cases (revised for Edgar event pattern):**

| # | Test | What it verifies |
|---|------|-----------------|
| 1 | `test_cli_help` | `--help` prints all canonical labels, defaults |
| 2 | `test_cli_required_fields` | Missing `--composition-url` or `--holder-name` → error |
| 3 | `test_cli_dry_run_output` | `--dry-run` prints signed share text, does NOT hit Edgar |
| 4 | `test_cli_sku_mapping_flag` | `--sku-mapping '{"key": "val"}'` is accepted and appears in payload |
| 5 | `test_cli_defaults_applied` | `--deplete-inputs`, `--add-output-locations`, etc. default to "true"/"false" |
| 6 | `test_cli_all_flags_disabled` | `--attr "Deplete Inputs=false" --attr "Add Output Locations=false" --attr "Set Currencies Metadata=false"` → payload contains all three |
| 7 | `test_dispatch_route_matches` | Text containing `[POST-REPACKAGING CLEANUP EVENT]` is matched by dispatch |
| 8 | `test_dispatch_route_env_var` | When `DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP` is set, webhook is triggered |
| 9 | `test_dispatch_enqueues_inventory_snapshot` | `enqueue_inventory=True` → `inventory_snapshot.publish()` is called |
| 10 | `test_event_submission_end_to_end` | Full integration: CLI → Edgar → dispatch → mock GAS |

**Mocking strategy:**
- `monkeypatch.setattr` on `EdgarClient.submit` for CLI tests (mock HTTP)
- `monkeypatch.setattr` on `webhook_trigger.trigger` for dispatch tests
- `monkeypatch.setattr` on `inventory_snapshot.publish` for snapshot enqueue test
- `TestClient` against `create_app()` for end-to-end FastAPI tests

---

## §9 — Gates (REVISED)

| Gate | What | Who |
|------|------|-----|
| **G1** | PR1 (CLI module) merged to `dao_client` `main` | Sophia → Governor |
| **G2** | PR2 (dispatch route) merged to `dao_client` `main` | Sophia → Governor |
| **G3** | PR3 (GAS handler) deployed to GAS, env var provisioned | Sophia → Governor |
| **G4** | `pytest tests/test_post_repackaging_cleanup.py -v` — all pass | Sophia |
| **G5** | `python -m truesight_dao_client.modules.post_repackaging_cleanup --help` prints clean help | Sophia |
| **G6** | Dry-run against b08d324b prints expected signed payload | Governor / QA |
| **G7** | Real run against b08d324b — verify sheet changes in Main Ledger | Governor / QA |
| **G8** | Real run is idempotent — second run produces Telegram log but no duplicate sheet writes | Governor / QA |
| **G9** | Post-UAT sign-off | Governor |

---

## §10 — RESUME HERE

**After the plan is committed + Sophia pinged:** Sophia reads this file via `read_repo_file` on GitHub `main`, refreshes her clone, opens a Telegram topic (or reuses existing thread 7987), posts kickoff, and awaits the GO signal.

**RESUME HERE = PR1** (CLI module `post_repackaging_cleanup.py` — the thin `build_event_cli` wrapper).

Execution order: PR1 → PR2 → PR3 → G4/G5 → hand off for G6/G7/G8 UAT.

---

## §11 — Roadmap

```
Day 1: PR1 (CLI module, ~25 lines) + PR2 (dispatch, ~3 lines)
Day 2: PR3 (GAS handler, ~150 lines) + deploy + provision env var
Day 3: PR4 (tests, ~200 lines) → G4/G5
Day 3-4: UAT (dry-run + real run against b08d324b)
Day 4: G9 sign-off
```

---

## §12 — User Acceptance Testing (UAT)

### UAT-1: CLI help
```bash
cd /Users/garyjob/Applications/dao_client
python3 -m truesight_dao_client.modules.post_repackaging_cleanup --help
```
**Expected:** Clean help listing all 14 canonical labels with their flags, defaults shown, required fields marked.

### UAT-2: Dry-run against b08d324b
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

### UAT-3: Real run against b08d324b
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

### UAT-4: Idempotency
Re-run the same command. **Expected:**
- [ ] Edgar accepts the duplicate event (HTTP 200)
- [ ] Telegram Chat Logs shows a second entry
- [ ] GAS handler detects all outputs already in `offchain asset location` → skips addition
- [ ] GAS handler detects `isSerializable` already TRUE → skips
- [ ] GAS handler detects farm info already populated → skips
- [ ] No duplicate rows created, no data corruption

### UAT-5: Rebuild inventory flag
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

### UAT-6: Error handling
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

- [ ] `truesight-dao-post-repackaging-cleanup --help` prints all 14 canonical labels
- [ ] CLI module uses `build_event_cli` (NOT custom argparse, NOT gspread)
- [ ] `--dry-run` prints signed share text without hitting Edgar
- [ ] Dispatch route matches `[POST-REPACKAGING CLEANUP EVENT]`
- [ ] Dispatch enqueues inventory snapshot (`enqueue_inventory=True`)
- [ ] GAS handler processes Telegram Chat Log entry and writes to sheets
- [ ] GAS handler is idempotent (safe to re-run)
- [ ] GAS handler handles errors gracefully (bad URL, missing rows)
- [ ] All unit tests pass (`pytest tests/test_post_repackaging_cleanup.py -v`)
- [ ] Real run against b08d324b produces correct sheet changes
- [ ] Real run is idempotent — second run produces no duplicate writes
- [ ] `--rebuild-inventory` flag triggers snapshot rebuild
- [ ] Module follows existing code conventions (build_event_cli, canonical labels, validators)

---

## §15 — Sophia Feedback (2026-06-28)

Sophia opened PR https://github.com/TrueSightDAO/dao_protocol/pull/133 with two issues:

1. **Wrong repo.** The plan specifies `TrueSightDAO/dao_client`, not `dao_protocol`. All CLI modules live in `dao_client/truesight_dao_client/modules/`. The dispatch route lives in `dao_client/truesight_dao_client/server/dispatch.py`.

2. **Wrong architecture.** The PR uses direct gspread writes (following the `onboard_partner.py` pattern). This plan has been updated to v2 to specify the canonical Edgar event → dispatch → GAS pattern instead. The CLI module must be a thin `build_event_cli` wrapper that signs and POSTs to Edgar. All sheet writes must happen in a new GAS handler, triggered by Edgar's dispatch.

**Action for Sophia:** Close PR #133. Start fresh with this v2 plan. RESUME HERE = PR1 (the CLI wrapper in dao_client, ~25 lines using `build_event_cli`).
