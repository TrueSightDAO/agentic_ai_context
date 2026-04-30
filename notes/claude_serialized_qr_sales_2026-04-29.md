# Serialized QR Code Sales Pattern — DAO Client

**Date:** 2026-04-29
**Agent:** Claude
**Context:** Elizabeth Wong purchased all 37 remaining dark chocolate bars (20 Oscar 2024 + 17 Santa Ana 2023) via Stripe checkout link.

---

## The Pattern

When a customer buys **multiple serialized QR-coded products** in one transaction:

### 1. Discover the exact QR codes

Use the same GAS endpoint the DApp (`report_sales.html`) uses:

```
https://script.google.com/macros/s/AKfycbxigq4-J0izShubqIC5k6Z7fgNRyVJLakfQ34HPuENiSpxuCG-wSq0g-wOAedZzzgaL/exec?list_with_members=true
```

Filter by:
- `contributor_name` (e.g. `Kirsten Ritschel`)
- `currency` (exact match from `currencies.json`)
- `status` = `MINTED` (available for sale)

### 2. One [SALES EVENT] per QR code

The DApp's `report_sales.html` sets `Item` to the **QR code ID**, not a human description. Example payload:

```
[SALES EVENT]
- Item: 2024OSR_81PB_20260412_3
- Sales price: $10.00
- Sold by: Kirsten Ritschel
- Cash proceeds collected by: Gary Teh
- Owner email: ewong@gogreatop.com
- Stripe Session ID: cs_live_...
- Shipping Provider: (none)
- Tracking number: (none)
- Attached Filename: New Order_ Elizabeth Wong - $370.00.pdf
- Submission Source: dao_client / bulk Stripe checkout
--------
```

**This is the canonical pattern whether using DApp or dao_client.**

### 3. Amortize transaction fees

For bulk Stripe orders, split the fee evenly:

```
Stripe fee per bar = $11.03 / 37 = $0.2981
```

Include via `--attr`:
```bash
--attr "Stripe fee per bar=0.2981" \
--attr "Stripe fee total=11.03" \
--attr "Net after fees per bar=9.7019"
```

### 4. The canonical labels mismatch

`dao_client/modules/report_sales.py` canonical labels:
```python
['Item', 'Sales price', 'Sold by', 'Cash proceeds collected by',
 'Owner email', 'Stripe Session ID', 'Shipping Provider',
 'Tracking number', 'Attached Filename', 'Submission Source']
```

There is **no `QR Code` field** — the QR code goes in `Item`. This is by design (matches DApp).

### 5. Cash sales (no Stripe)

When the customer pays cash (not Stripe checkout):

| Field | Value | Why |
|-------|-------|-----|
| Stripe Session ID | **`(none)`** | GAS `normalizeSalesEventOptionalField()` strips `(none)` to empty, skipping the Stripe checkout lookup. **Do NOT use "N/A"** — it passes through as a literal string and triggers a "No Stripe row found" log line (even after the 2026-04-30 GAS fix that validates `cs_(live\|test)_` prefixes). |
| Shipping Provider | `N/A` | Local pickup or hand delivery |
| Tracking number | `N/A` | No shipping label |

### 6. Ledger assignment ≠ physical possession

A QR code's `ledger_shortcut` (e.g. `agl4`, `agl6`) and `manager_name` indicate which **ledger tracks the item** and who **manages the record**. It does **not** mean the item is physically at that location or in that person's hands.

**Example:** `2024SJ_20250515_NIBS_27` is tracked under AGL6 ledger but was physically carried by Gary Teh to Stanford Farm for sale. The `[SALES EVENT]` submission is sufficient — the downstream chain (QR Code Sales tab → offchain transactions → treasury cache) handles inventory depletion automatically.

### 7. What downstream handles automatically

| System | Handled? | Notes |
|--------|----------|-------|
| Telegram Chat Logs | ✅ Yes | One row per `[SALES EVENT]` |
| QR Code Sales tab | ✅ Yes | Parser reads `Item` as QR code |
| Agroverse QR codes status | ✅ Yes | `process_sales_telegram_logs.gs` flips `MINTED` → `SOLD` |
| offchain transactions | ✅ Yes | `sales_update_main_dao_offchain_ledger.gs` creates double-entry rows |
| Inventory JSON / treasury cache | ✅ Yes | Rebuilt asynchronously by treasury-cache-publisher |
| **Separate [INVENTORY MOVEMENT]** | ❌ **Not needed** | For serialized QR products, the QR lifecycle (MINTED → SOLD) IS the inventory movement. Only needed for bulk/non-serialized inventory tracked by weight/count. |

---

## Cross-references (discoverability)

- **Canonical context files now point here:**
  - `OPERATING_INSTRUCTIONS.md` §2 — row in "What to read" table
  - `WORKSPACE_CONTEXT.md` §5 — bullet under "Where to Look Next"
  - `PROJECT_INDEX.md` — `dao_client` row mentions serialized QR bulk sales
- **Reusable template:** `dao_client/examples/bulk_qr_sales_template.py` — copy, set CONFIG section, uncomment the submission calls.

## Open enhancement: dao_client read-side

The DApp has authenticated proxy reads (`edgar.truesight.me/proxy/gas/qrCodes`).
The CLI has no equivalent. A `cache/qr_codes.py` module should be added
so future bulk sales don't require manual `curl` + JSON parsing.

---

## Worked example: Elizabeth Wong, 37 bars

**QR codes discovered:**
- Oscar 2024 (20): `2024OSR_81PB_20260412_3` through `_23` (skipping already-sold `_1`, `_2`, `_11`)
- Santa Ana 2023 (17): `2023SA_81PB_20260412_1`, `_5` through `_20` (skipping already-sold `_2`, `_3`, `_4`)

**Script approach:** Python loop using `EdgarClient.submit()` with 1-second delays between calls.
