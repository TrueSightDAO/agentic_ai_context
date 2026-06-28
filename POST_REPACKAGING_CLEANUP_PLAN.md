# Post-Repackaging Cleanup — Implementation Plan

**Status:** Draft — awaiting governor review (§10)
**Handoff target:** Sophia (truesight_autopilot)
**Repo:** `TrueSightDAO/dao_client`
**Date:** 2026-06-28

---

## §1 — Context

### What
A new `dao_client` module that closes the known gap between `[REPACKAGING BATCH EVENT]` submission and a fully populated Main Ledger. Today the repackaging GAS (`agroverse-inventory/gas/repackaging-currency-ingest/Code.gs`) writes only `Currencies` columns **A, B, N, O**. Everything else requires manual gspread ad-hoc edits (documented in `QR_GENERATION_DAO_CLIENT_POSTMORTEM.md:49-56`).

### Why
Every repackaging batch leaves four manual cleanup steps:
1. **Deplete** consumed inputs from `offchain asset location`
2. **Add** output rows (bars/ceremonial/etc.) to `offchain asset location`
3. **Set** `Currencies` columns C (`isSerializable`), D (product image), E–J (farm info), M (SKU Product ID)
4. **Rebuild** `store-inventory.json` so the website reflects reality

This module automates all four from a composition JSON + CLI/YAML input.

### Who
- **Governor:** Gary Teh
- **Builder:** Sophia (truesight_autopilot)
- **QA:** Local LLM (post-UAT)

---

## §2 — Current State

| Item | Status |
|------|--------|
| `[REPACKAGING BATCH EVENT]` submission | Exists: DApp `repackaging_planner.html` + CLI `repackaging_planner.py` |
| GAS writes `Currencies` A, B, N, O | Working |
| GAS writes `offchain asset location` | **Not implemented** — gap |
| GAS writes `Currencies` C, D, E–J, M | **Not implemented** — gap |
| gspread helpers in `dao_client` | Exists: `onboard_partner.py` lines 287-315 (`_gspread_client`, `_find_google_credentials`, `_retry`) |
| Sheets v4 API helpers in `dao_client` | Exists: `server/sheets/base.py` (`update_cell`, `find_row_by_col_a`, `batch_update`, `append_row`) |
| Composition JSON schema | Stable (v2), example: `b08d324b-e2f4-4645-9d25-ee43f9e7d9e0.json` |
| Test framework | pytest, monkeypatch, TestClient |
| Console script entry pattern | `pyproject.toml` `[project.scripts]` |

---

## §3 — Composition JSON Reference (input format)

The module's primary input is a composition JSON file (same format the repackaging GAS already consumes). Key fields:

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

**Only `inputs` with `line_kind == "from_holder_inventory"` are depleted** (custom/packaging lines are consumed in the batch but don't have an `offchain asset location` entry to deplete).

---

## §4 — Target Sheets & Columns

### `offchain asset location` (Main Ledger, gid=1883963235)
| Col | Name | Action |
|-----|------|--------|
| A | Currency | Match against `inputs[].currency` for depletion; write `outputs[].suggested_currency` for addition |
| B | Location | Match/filter by `--holder-name` |
| C | Amount Managed | **Decrement** by `inputs[].quantity` for depletion; **write** `outputs[].units` for addition |
| D | Unit Cost | Write `outputs[].unit_cost_usd` for addition |
| E | Total Value | Write `outputs[].line_total_usd` for addition |

### `Currencies` (Main Ledger, gid=1552160318)
| Col | Name | Action |
|-----|------|--------|
| A | Currencies | Match against `outputs[].suggested_currency` |
| C | Serializable | Set to `"TRUE"` (always for QR-ready output) |
| E | landing_page | From `--landing-page` flag |
| F | ledger | From `--ledger` flag |
| G | farm name | From `--farm-name` flag |
| H | state | From `--state` flag |
| I | country | From `--country` flag |
| J | Year | From `--year` flag |
| M | SKU Product ID | From `--sku-mapping` (keyed by output label substring match) |

---

## §5 — PR Breakdown

### PR1: Core module — `modules/post_repackaging_cleanup.py` (NEW FILE)

**What it does:**
1. Parse CLI args (argparse, no `build_event_cli` — this is NOT an Edgar event, it's direct sheet writes)
2. Fetch composition JSON from `--composition-url` (HTTP GET)
3. Validate composition against expected schema (check for `inputs`, `outputs`, `request_id`)
4. If `--deplete-inputs` (default true):
   - For each input with `line_kind == "from_holder_inventory"`:
     - Find row in `offchain asset location` where col A = `currency` AND col B = `--holder-name`
     - If row found: read current amount (col C), compute new amount = current - quantity
     - If new amount ≤ 0: set amount to 0 (or delete row? decision below)
     - If new amount > 0: write new amount to col C
     - If row NOT found: warn and skip (the input may not have been in offchain asset location)
5. If `--add-output-locations` (default true):
   - For each output:
     - Append row to `offchain asset location`: col A = `suggested_currency`, col B = `--holder-name`, col C = `units`, col D = `unit_cost_usd`, col E = `line_total_usd`
6. If `--set-currencies-metadata` (default true):
   - For each output:
     - Find row in `Currencies` where col A = `suggested_currency`
     - If found: batch-update columns C, E, F, G, H, I, J, M with provided values
     - If NOT found: warn and skip (the repackaging GAS may not have run yet)
7. If `--rebuild-inventory` (default false, opt-in):
   - Invoke `sync_agroverse_store_inventory.py` as subprocess
8. Print summary table of what was done / skipped / warned

**Pattern:** Follow `onboard_partner.py` — custom argparse, gspread for sheet writes, `_find_google_credentials` / `_gspread_client` / `_retry` copied from that module.

**Dependencies:**
- `gspread` (already in the repo's transitive deps via `onboard_partner.py`)
- `google-auth` (same)
- `requests` or `urllib` (stdlib — for fetching composition JSON)

**CLI arguments:**
```
Required:
  --composition-url URL       URL to composition JSON (GitHub raw or any HTTP)

Optional:
  --holder-name NAME          Who physically holds the inventory (required if depleting/adding locations)
  --sku-mapping JSON          {"<substring>": "<sku-id>", ...} — matches output label substrings
  --landing-page URL          Landing page for Currencies!E
  --ledger URL                Ledger URL for Currencies!F
  --farm-name NAME            Farm name for Currencies!G
  --state STATE               State for Currencies!H
  --country COUNTRY           Country for Currencies!I
  --year YEAR                 Year for Currencies!J

  --deplete-inputs / --no-deplete-inputs         (default: true)
  --add-output-locations / --no-add-output-locations  (default: true)
  --set-currencies-metadata / --no-set-currencies-metadata  (default: true)
  --rebuild-inventory / --no-rebuild-inventory   (default: false)

  --spreadsheet-id ID         Override Main Ledger spreadsheet ID (default: 1GE7PUq-...)
  --dry-run                   Validate, resolve, print what WOULD be written — don't write
  --verbose                   Print per-row detail
```

**SKU mapping logic:**
The `--sku-mapping` flag accepts a JSON object where each key is a substring to match against `outputs[].suggested_currency` and each value is the SKU Product ID to write to Currencies!M. Example:
```json
{
  "Ceremonial Cacao Kraft Pouch": "ceremonial-cacao-kraft-pouch-200g",
  "Agroverse 81% Cacao Chocolate Bar 50g": "agroverse-81-cacao-chocolate-bar-50g"
}
```
First match wins. If no key matches, Currencies!M is left empty (warn).

**Design decisions:**
- **Delete vs. zero for depletion:** Write amount to 0 rather than deleting the row (preserves audit trail; the GAS ignores zero-amount rows for inventory snapshots).
- **Idempotency:** The module checks existing values before writing. If `offchain asset location` already has a row for an output, it skips (warns). If Currencies!C is already `TRUE`, it skips that column. This makes the module safe to re-run.
- **No Edgar integration:** This module writes directly to Google Sheets (like `onboard_partner.py`'s Steps 2 & 3). It does NOT submit events to Edgar — no cryptographic signing, no Telegram Chat Log audit trail. This matches the postmortem workaround pattern.

---

### PR2: Console script + pyproject.toml entry

**File:** `pyproject.toml` — add one line under `[project.scripts]`:
```toml
truesight-dao-post-repackaging-cleanup = "truesight_dao_client.modules.post_repackaging_cleanup:main"
```

**No other changes.** The module's `main()` follows standard argparse conventions.

---

### PR3: Unit tests — `test_post_repackaging_cleanup.py` (NEW FILE)

**Test file location:** `dao_client/tests/test_post_repackaging_cleanup.py`

**Framework:** pytest + monkeypatch (matching repo conventions — no unittest.mock, no test classes)

**Test cases:**

| # | Test | What it verifies |
|---|------|-----------------|
| 1 | `test_parse_composition_json` | Valid composition JSON parses correctly; missing fields raise clear errors |
| 2 | `test_filter_holder_inventory_inputs` | Only `line_kind == "from_holder_inventory"` inputs are depleted; packaging/custom lines are skipped |
| 3 | `test_deplete_input_partial` | Input with quantity 7 and existing amount 10 → writes 3 to col C |
| 4 | `test_deplete_input_full` | Input with quantity 7 and existing amount 7 → writes 0 to col C |
| 5 | `test_deplete_input_more_than_available` | Input with quantity 7 and existing amount 3 → writes 0, warns |
| 6 | `test_deplete_input_not_found` | Input currency not in offchain asset location → warns, skips |
| 7 | `test_deplete_input_wrong_holder` | Input currency exists but under different holder → skips (row not matched) |
| 8 | `test_add_output_location_new` | Output not yet in offchain asset location → appends row |
| 9 | `test_add_output_location_idempotent` | Output already in offchain asset location → skips, warns |
| 10 | `test_set_currencies_metadata` | Currencies row found → batch-updates C, E-J, M |
| 11 | `test_set_currencies_metadata_not_found` | Currencies row not found → warns, skips |
| 12 | `test_sku_mapping_substring_match` | `--sku-mapping '{"Ceremonial Cacao": "sku-cc"}'` matches `"... Ceremonial Cacao Kraft Pouch ..."` |
| 13 | `test_sku_mapping_first_match_wins` | Multiple keys could match → first wins |
| 14 | `test_sku_mapping_no_match` | No key matches → Currencies!M left empty, warns |
| 15 | `test_dry_run_no_writes` | `--dry-run` prints what WOULD happen, no gspread calls |
| 16 | `test_empty_composition` | Composition with no inputs/outputs → graceful message, exit 0 |
| 17 | `test_fetch_composition_http_error` | URL returns 404 → clear error message |
| 18 | `test_all_flags_disabled` | `--no-deplete-inputs --no-add-output-locations --no-set-currencies-metadata` → prints "nothing to do" |

**Mocking strategy:**
- `monkeypatch.setattr` on `_gspread_client` to return a mock gspread client
- `monkeypatch.setattr` on `_retry` to be a pass-through
- Mock `worksheet.get_all_values()`, `worksheet.update_cell()`, `worksheet.append_row()`
- Mock `urllib.request.urlopen` for composition URL fetch
- Use `tmp_path` fixture for local JSON file testing

---

### PR4: Integration test — real dry-run against b08d324b

**Script:** `tests/test_post_repackaging_cleanup_integration.py`

**What it does:**
1. Run `--dry-run` against the actual `b08d324b` composition JSON
2. Verify it correctly identifies:
   - 4 inputs (1 holder-inventory nibs + 3 packaging lines)
   - 2 outputs (ceremonial + bars)
3. Verify SKU mapping resolution
4. Verify it does NOT write to any sheet (dry-run)
5. Verify output is parseable and human-readable

**Run:** `pytest tests/test_post_repackaging_cleanup_integration.py -v`

---

## §6 — Gates

| Gate | What | Who |
|------|------|-----|
| **G1** | PR1, PR2, PR3 merged to `main` | Sophia |
| **G2** | `pytest tests/test_post_repackaging_cleanup.py -v` — all pass | Sophia |
| **G3** | `pytest tests/test_post_repackaging_cleanup_integration.py -v` — pass | Sophia |
| **G4** | `python -m truesight_dao_client.modules.post_repackaging_cleanup --help` prints clean help | Sophia |
| **G5** | Dry-run against b08d324b produces expected output (UAT §9) | Governor / QA |
| **G6** | Real run against a test composition (UAT §9) — verify sheet changes | Governor / QA |
| **G7** | Post-UAT sign-off | Governor |

---

## §7 — RESUME HERE

**After the plan is committed + Sophia pinged:** Sophia reads this file via `read_repo_file` on GitHub `main`, opens a Telegram topic, posts kickoff, and awaits the GO signal.

**RESUME HERE = PR1** (core module `post_repackaging_cleanup.py`).

Execution order: PR1 → PR2 (trivial, can be same PR) → PR3 → G2/G3 → hand off for G5/G6 UAT.

---

## §8 — Roadmap

```
Week 1: PR1+PR2 → PR3 → G2/G3 → ping QA for G5/G6
Week 1-2: UAT (manual dry-run + real run against a test batch)
Week 2: G7 sign-off → merge → Sophia pings "governor, cleanup module is live"
```

---

## §9 — User Acceptance Testing (UAT)

### UAT-1: CLI help
```bash
cd /Users/garyjob/Applications/dao_client
python -m truesight_dao_client.modules.post_repackaging_cleanup --help
```
**Expected:** Clean help text listing all flags, defaults, and examples.

### UAT-2: Dry-run against b08d324b (no sheet writes)
```bash
python -m truesight_dao_client.modules.post_repackaging_cleanup \
    --composition-url "https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/b08d324b-e2f4-4645-9d25-ee43f9e7d9e0.json" \
    --holder-name "Kirsten Ritschel" \
    --farm-name "Oscar's Farm, Bahia" \
    --state "Bahia" \
    --country "Brazil" \
    --year "2024" \
    --landing-page "https://agroverse.shop/shipments/agl4" \
    --ledger "https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=1762218634" \
    --sku-mapping '{"Ceremonial Cacao Kraft Pouch": "ceremonial-cacao-kraft-pouch-200g", "Agroverse 81% Cacao Chocolate Bar 50g": "agroverse-81-cacao-chocolate-bar-50g"}' \
    --dry-run \
    --verbose
```

**Expected output:**
```
Composition: b08d324b-e2f4-4645-9d25-ee43f9e7d9e0
DRY RUN — no changes will be written

[1/4] DEPLETE INPUTS (offchain asset location)
  SKIP  "Ceremonial Cacao Kraft Pouch - Alibaba:..." (qty 3) — packaging line, not holder inventory
  SKIP  "Sticker Mule 4x2in custom rectangle label..." (qty 15) — packaging line
  SKIP  "RLAVBL 7x5x4 corrugated ship box..." (qty 15) — packaging line
  WOULD deplete "8 Ounce Package Kraft Pouch  CP340992735BR" by 7 (Kirsten Ritschel)

[2/4] ADD OUTPUT LOCATIONS (offchain asset location)
  WOULD add "Ceremonial Cacao Kraft Pouch - ... | Kirsten 20260620 | San Francisco - AGL4" x3  @ $11.61 ($34.84 total)
  WOULD add "Agroverse 81% Cacao Chocolate Bar 50g | ... | Kirsten 20260620 | San Francisco - AGL4" x15 @ $2.90 ($43.55 total)

[3/4] SET CURRENCIES METADATA
  WOULD set cols C,E,F,G,H,I,J,M on "Ceremonial Cacao Kraft Pouch - ..."
    C = TRUE
    E = https://agroverse.shop/shipments/agl4
    F = https://docs.google.com/spreadsheets/d/...
    G = Oscar's Farm, Bahia
    H = Bahia
    I = Brazil
    J = 2024
    M = ceremonial-cacao-kraft-pouch-200g
  WOULD set cols C,E,F,G,H,I,J,M on "Agroverse 81% Cacao Chocolate Bar 50g | ..."
    ... (same farm info)
    M = agroverse-81-cacao-chocolate-bar-50g

[4/4] REBUILD INVENTORY SNAPSHOT
  SKIP — --rebuild-inventory not set

Done (dry run). 0 writes, 0 errors.
```

### UAT-3: Real run against b08d324b
```bash
# SAME COMMAND AS UAT-2 but without --dry-run
python -m truesight_dao_client.modules.post_repackaging_cleanup \
    --composition-url "https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/b08d324b-e2f4-4645-9d25-ee43f9e7d9e0.json" \
    --holder-name "Kirsten Ritschel" \
    --farm-name "Oscar's Farm, Bahia" \
    --state "Bahia" \
    --country "Brazil" \
    --year "2024" \
    --landing-page "https://agroverse.shop/shipments/agl4" \
    --ledger "https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit#gid=1762218634" \
    --sku-mapping '{"Ceremonial Cacao Kraft Pouch": "ceremonial-cacao-kraft-pouch-200g", "Agroverse 81% Cacao Chocolate Bar 50g": "agroverse-81-cacao-chocolate-bar-50g"}' \
    --verbose
```

**Post-run verification checklist:**
- [ ] `offchain asset location`: "8 Ounce Package Kraft Pouch CP340992735BR" under "Kirsten Ritschel" is now 0
- [ ] `offchain asset location`: 2 new rows for ceremonial + bars under Kirsten Ritschel
- [ ] `Currencies`: `isSerializable` = TRUE on both CC and CB output rows
- [ ] `Currencies`: farm info (E-J) populated on both rows
- [ ] `Currencies`: SKU Product ID (M) populated on both rows
- [ ] Re-run the same command → all steps report "already done, skipping" (idempotency)

### UAT-4: Rebuild inventory snapshot
```bash
python -m truesight_dao_client.modules.post_repackaging_cleanup \
    --composition-url "..." \
    --holder-name "Kirsten Ritschel" \
    --deplete-inputs --no-add-output-locations --no-set-currencies-metadata \
    --rebuild-inventory \
    --verbose
```

**Post-run verification:**
- [ ] `store-inventory.json` updated on GitHub
- [ ] agroverse.shop shows correct stock for the new SKUs

### UAT-5: Error handling
```bash
# Invalid URL
python -m ... --composition-url "https://example.com/nonexistent.json"
# Expected: clear error "Failed to fetch composition: HTTP 404"

# Composition without matching Currencies rows (GAS hasn't run yet)
# Expected: warns "Currency row not found, skipping metadata for: ..."

# Duplicate run (idempotency)
# Run the same command twice → second run reports all skips
```

---

## §10 — Unit Test Specifications (for PR3)

```python
# tests/test_post_repackaging_cleanup.py

import pytest
from types import SimpleNamespace

# ---------- fixtures ----------

@pytest.fixture
def sample_composition():
    return {
        "request_id": "b08d324b-...",
        "inputs": [
            {"line_kind": "from_holder_inventory", "currency": "8 Ounce Nibs CP340992735BR", "quantity": 7, "unit_cost_usd": 8.51},
            {"line_kind": "from_holder_inventory", "currency": "Ceremonial Cacao Kraft Pouch - Alibaba:...", "quantity": 3, "unit_cost_usd": 0.74},
            {"line_kind": "from_holder_inventory", "currency": "Sticker Mule 4x2in label...", "quantity": 15, "unit_cost_usd": 0.55},
            {"line_kind": "from_holder_inventory", "currency": "RLAVBL 7x5x4 box...", "quantity": 15, "unit_cost_usd": 0.55},
        ],
        "outputs": [
            {"suggested_currency": "Ceremonial Cacao Kraft Pouch - ... | Kirsten 20260620 | SF - AGL4", "units": 3, "unit_cost_usd": 11.61, "line_total_usd": 34.84, "unit_kind": "pouch", "weight_per_unit_grams": 200},
            {"suggested_currency": "Agroverse 81% Cacao Chocolate Bar 50g | ... | Kirsten 20260620 | SF - AGL4", "units": 15, "unit_cost_usd": 2.90, "line_total_usd": 43.55, "unit_kind": "each", "weight_per_unit_grams": 50},
        ],
        "totals": {"inputs_subtotal_usd": 78.39, "grand_total_usd": 78.39, "total_output_weight_grams": 1350, "cost_per_gram_usd": 0.058}
    }

@pytest.fixture
def sample_offchain_data():
    """Mock offchain asset location sheet data (header at row 1)."""
    return [
        ["Currency", "Location", "Amount", "Unit Cost", "Total Value"],  # header
        ["8 Ounce Nibs CP340992735BR", "Kirsten Ritschel", "7", "8.51", "59.57"],
        ["Ceremonial Cacao Kraft Pouch - Alibaba:...", "Kirsten Ritschel", "10", "0.74", "7.40"],
        ["Sticker Mule 4x2in label...", "Kirsten Ritschel", "100", "0.55", "55.00"],
        ["8 Ounce Nibs CP340992735BR", "Gary Teh", "5", "8.51", "42.55"],  # different holder
    ]

@pytest.fixture
def sample_currencies_data():
    """Mock Currencies tab data (header at row 1)."""
    return [
        ["Currencies", "Price", "Serializable", "Image", "Landing", "Ledger", "Farm", "State", "Country", "Year", "Wt(g)", "Wt(oz)", "SKU", "Raw", "Composition"],
        ["Ceremonial Cacao Kraft Pouch - ... | Kirsten 20260620 | SF - AGL4", "11.61", "", "", "", "", "", "", "", "", "", "", "", "...", "..."],
        ["Agroverse 81% Cacao Chocolate Bar 50g | ... | Kirsten 20260620 | SF - AGL4", "2.90", "", "", "", "", "", "", "", "", "", "", "", "...", "..."],
    ]


# ---------- unit tests ----------

def test_filter_holder_inventory_inputs(sample_composition):
    """Only inputs with line_kind 'from_holder_inventory' are depleted."""
    from truesight_dao_client.modules.post_repackaging_cleanup import _holder_inventory_inputs
    result = _holder_inventory_inputs(sample_composition["inputs"])
    assert len(result) == 4
    # (all sample inputs are holder inventory; custom lines would be skipped)

def test_deplete_input_partial(monkeypatch, sample_composition, sample_offchain_data):
    """Deplete: amount 7 → 0 (was exactly 7)."""
    # ... mock gspread, verify update_cell called with "0"
    pass

def test_deplete_input_not_found(monkeypatch, sample_composition):
    """Deplete: currency not in sheet → warn."""
    pass

def test_deplete_input_wrong_holder(monkeypatch, sample_composition, sample_offchain_data):
    """Deplete: currency exists but under different holder → skip."""
    pass

def test_add_output_location_new(monkeypatch, sample_composition):
    """Add: output not yet in offchain → append row."""
    pass

def test_add_output_location_idempotent(monkeypatch, sample_composition, sample_offchain_data):
    """Add: output already in offchain → skip."""
    pass

def test_set_currencies_metadata(monkeypatch, sample_composition, sample_currencies_data):
    """Set: Currencies row found → batch-update C,E-J,M."""
    pass

def test_set_currencies_metadata_not_found(monkeypatch, sample_composition):
    """Set: Currencies row not found → warn."""
    pass

def test_sku_mapping_substring_match():
    """Substring 'Ceremonial Cacao' matches 'Ceremonial Cacao Kraft Pouch - ...'."""
    from truesight_dao_client.modules.post_repackaging_cleanup import _resolve_sku
    mapping = {"Ceremonial Cacao Kraft Pouch": "sku-cc"}
    result = _resolve_sku("Ceremonial Cacao Kraft Pouch - Alibaba:... | 200g", mapping)
    assert result == "sku-cc"

def test_sku_mapping_first_match_wins():
    """First matching key wins."""
    from truesight_dao_client.modules.post_repackaging_cleanup import _resolve_sku
    mapping = {"Ceremonial": "sku-first", "Ceremonial Cacao": "sku-second"}
    result = _resolve_sku("Ceremonial Cacao Kraft Pouch", mapping)
    assert result == "sku-first"  # Order depends on dict insertion order (Python 3.7+)

def test_sku_mapping_no_match():
    """No key matches → return None."""
    from truesight_dao_client.modules.post_repackaging_cleanup import _resolve_sku
    mapping = {"Chocolate Bar": "sku-cb"}
    result = _resolve_sku("Ceremonial Cacao Kraft Pouch", mapping)
    assert result is None

def test_dry_run_no_writes(monkeypatch, sample_composition, capsys):
    """--dry-run prints but does not call gspread write methods."""
    pass

def test_empty_composition(capsys):
    """Composition with no inputs/outputs → graceful."""
    pass
```

---

## §11 — Integration Test Specifications (for PR4)

```python
# tests/test_post_repackaging_cleanup_integration.py

import json
import subprocess
import sys

def test_dry_run_against_b08d324b():
    """Dry-run the module against the real b08d324b composition."""
    result = subprocess.run(
        [sys.executable, "-m", "truesight_dao_client.modules.post_repackaging_cleanup",
         "--composition-url", "https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/b08d324b-e2f4-4645-9d25-ee43f9e7d9e0.json",
         "--holder-name", "Kirsten Ritschel",
         "--dry-run", "--verbose"],
        capture_output=True, text=True, cwd="/Users/garyjob/Applications/dao_client"
    )
    assert result.returncode == 0
    output = result.stdout + result.stderr
    assert "DRY RUN" in output
    assert "b08d324b" in output
    # 4 inputs total, but only 1 is holder inventory (nibs) — 3 are packaging
    assert "deplete" in output.lower()
    # 2 outputs
    assert "Ceremonial Cacao" in output
    assert "81% Cacao Chocolate Bar" in output
    assert "Done" in output


def test_help():
    """--help prints and exits 0."""
    result = subprocess.run(
        [sys.executable, "-m", "truesight_dao_client.modules.post_repackaging_cleanup", "--help"],
        capture_output=True, text=True, cwd="/Users/garyjob/Applications/dao_client"
    )
    assert result.returncode == 0
    assert "--composition-url" in result.stdout
    assert "--dry-run" in result.stdout


def test_invalid_url():
    """Invalid URL → nonzero exit, clear error."""
    result = subprocess.run(
        [sys.executable, "-m", "truesight_dao_client.modules.post_repackaging_cleanup",
         "--composition-url", "https://httpbin.org/status/404",
         "--dry-run"],
        capture_output=True, text=True, cwd="/Users/garyjob/Applications/dao_client"
    )
    assert result.returncode != 0
```

---

## §12 — Acceptance Criteria

- [ ] `truesight-dao-post-repackaging-cleanup --help` prints clean help
- [ ] All unit tests pass (`pytest tests/test_post_repackaging_cleanup.py -v`)
- [ ] All integration tests pass (`pytest tests/test_post_repackaging_cleanup_integration.py -v`)
- [ ] Dry-run against b08d324b prints expected depletion + addition + metadata plan
- [ ] Real run successfully writes to `offchain asset location` and `Currencies`
- [ ] Real run is idempotent — second run reports all skips
- [ ] No errors or unexpected warnings in verbose output
- [ ] `--rebuild-inventory` triggers `sync_agroverse_store_inventory.py` successfully
- [ ] Module follows existing code conventions (argparse, gspread helpers, no new dependencies beyond gspread/google-auth)
- [ ] Console script registered in `pyproject.toml`
