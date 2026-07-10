# SOPHIA Expense Reporting Plan

**Purpose:** SOP for Sophia (and any AI agent) to correctly interpret and submit DAO operational expenses — especially shipping receipts from Pirate Ship, Etsy, UPS, etc.

**Status:** LIVE — 2026-06-29  
**Incident:** Shipping expense submitted with `Target Ledger: USD` (wrong). Correct value is `offchain`. This SOP prevents that class of mistake.

---

## 0. SOP — Submitting a shipping expense (READ FIRST)

When a governor sends a message like "process this shipping receipt" with a PDF attachment, or an AI agent discovers a shipping expense that needs to be recorded:

### Rule 1: Event type = `[DAO Inventory Expense Event]`

Browser equivalent: `dapp.truesight.me/report_dao_expenses.html`

### Rule 2: Target Ledger = `offchain` (the main ledger)

Shipping expenses, supplies, and other operational costs are drawn from the operator's **offchain USD balance** on the main ledger. The correct value is:

```
Target Ledger: offchain
```

**Do NOT use `USD`, `AGL4`, or any other value** — those are either wrong or refer to managed product ledgers. The `offchain` ledger is the offchain transactions tab on the main ledger workbook (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`).

### Rule 3: Item = what was purchased

For shipping labels, include the carrier, service level, and tracking number:
```
Inventory Type: UPS Ground Saver shipping label (tracking 1ZXG9979YN25983449)
```

### Rule 4: Cost = exact dollar amount from the receipt

Read the receipt PDF. Use the exact amount charged, not an estimate.

### Rule 5: Attach the receipt PDF

Always use `--attachment` to upload the receipt as proof. The attachment gets uploaded to GitHub via the `Destination Expense File Location` URL.

### Quick field-reference card

| Field | Source | Example |
|-------|--------|---------|
| `DAO Member Name` | Who paid | `Gary Teh` |
| `Target Ledger` | **Always `offchain`** | `offchain` |
| `Latitude` | Geolocation (optional, use `NA` if unknown) | `NA` |
| `Longitude` | Geolocation (optional, use `NA` if unknown) | `NA` |
| `Inventory Type` | What was purchased — carrier + tracking for shipping | `UPS Ground Saver shipping label (tracking 1ZXG9979YN25983449)` |
| `Inventory Quantity` | Dollar amount from receipt | `6.94` |
| `Description` | Context — what order/person is this for | `Pirate Ship shipping label for Etsy order #4088615882 (Raven Runyan)` |
| `Submission Source` | Where the receipt came from | `pirate_ship_receipt` |
| Attachment | Receipt PDF | `Pirate Ship.pdf` |

**Critical: field names MUST match the GAS parser exactly.** The GAS regex expects `Inventory Type` (not `Item`) and `Inventory Quantity` (not `Cost`). The field order is strict — `DAO Member Name` must come first, then `Target Ledger`.

---

## 2. CLI invocation

```bash
python3 -m truesight_dao_client.modules.report_dao_expenses \
  --dao-member-name "Gary Teh" \
  --target-ledger "offchain" \
  --inventory-type "UPS Ground Saver shipping label (tracking 1ZXG9979YN25983449)" \
  --inventory-quantity "6.94" \
  --description "Pirate Ship shipping label for Etsy order #4088615882 (Raven Runyan)" \
  --submission-source "pirate_ship_receipt" \
  --latitude "NA" \
  --longitude "NA" \
  --attachment "/path/to/Pirate Ship.pdf"
```

Note: Use the dedicated flags (`--inventory-type`, `--inventory-quantity`), NOT `--attr "Item=..."` or `--attr "Cost=..."`. The GAS parser expects the exact field names `Inventory Type` and `Inventory Quantity`.

Path to the .env credentials file: `/Users/garyjob/Applications/dao_client/.env`

---

## 3. Post-submission — triggering GAS processing

After submission, the GAS webhook `parseAndProcessTelegramLogs` processes the expense and deducts the cost from the offchain USD balance. The dispatch runs automatically via the dao_protocol server's background task. If it hasn't fired (check the sheet after a minute), trigger manually from the dao_protocol box:

```bash
python3 -c "
import requests
resp = requests.get(
    'https://script.google.com/macros/s/AKfycbwYBlFigSSPJKkI-F2T3dSsdLnvvBi2SCGF1z2y1k95YzA5HBrJVyMo6InTA9Fud2bOEw/exec',
    params={'action': 'parseAndProcessTelegramLogs'},
    timeout=60
)
print(f'HTTP {resp.status_code} — {resp.text[:200]}')
"
```

The `[DAO Inventory Expense Event]` dispatches:
- `parseAndProcessTelegramLogs` (expense processing)
- Inventory snapshot enqueue (publishes updated offchain balances)

---

## 4. Reversing a wrong expense entry

If the wrong `Target Ledger` was submitted:
1. Delete the row from the **Telegram Chat Logs** sheet
2. Correct and re-submit with `Target Ledger: offchain`
3. The new submission will have a different signature (different payload), so no duplicate guard blocks it

---

## 5. RESUME HERE

Sophia's first turn for an expense report:
1. Read this plan via `read_context_file` or `read_repo_file`
2. Extract details from the receipt PDF (Carrier, tracking, cost)
3. Submit with `Target Ledger: offchain`
4. Attach the PDF receipt
5. Report results to governor
