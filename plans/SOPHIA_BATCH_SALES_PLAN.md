# SOPHIA Batch Sales Execution Plan

**Purpose:** SOP for Sophia to correctly interpret and execute bulk QR code sales
from a governor's Telegram message. Covers intent parsing, field mapping, and execution.

**Status:** LIVE — 2026-06-20
**Incident:** SOHA 40-bag cash sale. Sophia misinterpreted the governor's message and
submitted 2 erroneous aggregate entries (total $680, Sold by Gary Teh, Item as
description instead of QR codes). This SOP prevents that class of mistake.

---

## 0. SOP — Interpreting the governor's batch sale message (READ FIRST)

When a governor sends a message in a batch-sale Telegram topic like:

> "David just transferred $680 to me for the purchase of all 40 bags of cacao"

or:

> "Here's the receipt for 40 bags sold to SOHA at $17 each. QR codes below:"

**Sophia MUST apply these rules BEFORE calling any tool:**

### Rule 1: ONE SALES EVENT PER QR CODE — never aggregate

A batch of N bags with N distinct QR codes = **N separate `[SALES EVENT]` submissions**.
NEVER submit a single `[SALES EVENT]` with `Item: "Ceremonial Cacao (40 bags)"` or
`Item: "QR1, QR2, QR3, ..."`. Each QR code gets its own submission.

### Rule 2: Extract per-unit price, never use the total

- Governor says "$680 for 40 bags" → `Sales price` = `17.00` (680 ÷ 40)
- Governor says "$17 each" → `Sales price` = `17.00`
- Never set `Sales price` to the total payment amount.

### Rule 3: "Sold by" = the person/entity SELLING the bags — NOT the governor

- Governor says "David from SOHA bought 40 bags" → `Sold by` = `SOHA - David Campbell`
- Governor says "I (Gary) collected the cash" → `Cash proceeds collected by` = `Gary Teh`
- The governor is often the cash collector, rarely the seller. Do NOT copy the
  governor's name into `Sold by`.

### Rule 4: "Item" = the QR code ID — never a product description

- `Item` MUST be a QR code like `2024OSCAR_20260330_1`
- NEVER use `Item: "Ceremonial Cacao"`, `Item: "Cacao Kraft Pouch"`, etc.
- The QR code IS the item identifier. The product name lives in GAS.

### Rule 5: The governor provides the QR code list — do not invent one

- Wait for the governor to post the QR code list. Do not guess, fabricate, or derive
  QR codes from context.
- If a list is provided, parse it. If not, ask: "Please paste the list of QR codes."

### Rule 6: Validate before submitting

- Run `lookup_qr_code` on at least one QR code to confirm it exists and is MINTED.
- Health-check Edgar with `GET /events-catalog` (must return 200).
- If either check fails, stop and report to the governor.

### Quick field-reference card

| Field | Source | Example from SOHA incident |
|-------|--------|---------------------------|
| `Item` | QR code from governor's list | `2024OSCAR_20260330_1` |
| `Sales price` | Per-unit price (total ÷ count) | `17.00` |
| `Sold by` | Named seller in governor's message | `SOHA - David Campbell` |
| `Cash proceeds collected by` | Person who received the money | `Gary Teh` |
| `Owner email` | Buyer's email from governor | `david@soha.center` |
| `Submission Source` | Descriptive string | `dao_client / bulk cash sale, local pickup` |

---

## 1. The pattern

Every batch sale follows the same structure:

1. Parse the governor's message using the SOP rules in §0 above.
2. Receive the QR code list from the governor.
3. Validate QR codes exist in GAS (lookup, confirm status = MINTED).
4. Health-check Edgar (`GET /events-catalog` should return 200).
5. Submit one `[SALES EVENT]` per QR code (each with a unique payload).
6. Report results.

Key rule: **ONE SALES EVENT PER QR CODE.** Do NOT submit an INVENTORY MOVEMENT to
deplete — that event type transfers custody person-to-person, NOT inventory-to-sale.
Inventory depletion happens automatically downstream from the SALES EVENT.

## 2. Required metadata per sale

| Field | Cash sale | Stripe sale |
|-------|-----------|-------------|
| Item | QR code ID | QR code ID |
| Sales price | e.g. "17.00" | e.g. "10.00" |
| Sold by | Manager name | Manager name |
| Cash proceeds collected by | Person who received cash | N/A (use same as Sold by) |
| Owner email | customer@domain | customer@domain |
| Stripe Session ID | **(omit entirely)** | cs_live_... |
| Shipping Provider | N/A | N/A or actual |
| Tracking number | N/A | N/A or actual |
| Submission Source | Descriptive string | Descriptive string |

**For cash sales, NEVER include `Stripe Session ID` at all** — do not use "N/A" or
"(none)". Omit the field.

## 3. CLI invocation (preferred for single sales)

```bash
truesight-dao-report-sales \
  --qr-code "2024OSCAR_20260330_1" \
  --sales-price "17.00" \
  --sold-by "SOHA - David Campbell" \
  --cash-proceeds-collected-by "Gary Teh" \
  --owner-email "david@soha.center" \
  --submission-source "dao_client / bulk cash sale, local pickup"
```

For batch (Python SDK — preferred for 3+ QR codes):

```python
from truesight_dao_client.edgar_client import EdgarClient
import time

client = EdgarClient.from_env(
    path="/Users/garyjob/Applications/dao_client/.env"
)
client.generation_source = "dao_client / bulk cash sale"

QR_CODES = [...]  # from governor's list
SALES_PRICE = "17.00"
SOLD_BY = "SOHA - David Campbell"
CASH_COLLECTED_BY = "Gary Teh"
OWNER_EMAIL = "david@soha.center"

for i, qr in enumerate(QR_CODES, start=1):
    attrs = [
        ("Item", qr),
        ("Sales price", SALES_PRICE),
        ("Sold by", SOLD_BY),
        ("Cash proceeds collected by", CASH_COLLECTED_BY),
        ("Owner email", OWNER_EMAIL),
        ("Submission Source", f"dao_client / bulk cash sale / item {i} of {len(QR_CODES)}"),
    ]
    resp = client.submit("SALES EVENT", attrs)
    # handle response (see §5)
    time.sleep(1.0)
```

Path to the .env credentials file: `/Users/garyjob/Applications/dao_client/.env`

## 4. Before submitting — health check

Always check Edgar is healthy before attempting batch submissions:

```bash
curl -s -o /dev/null -w "%{http_code}" https://edgar.truesight.me/events-catalog
# Must return 200
```

If this returns non-200, **stop and report to governor** — do not attempt submissions.

## 5. Error handling — response codes

| HTTP | Meaning | Action |
|------|---------|--------|
| 200 | Success | Record + continue |
| 409 | Duplicate (txn ID already processed) | This submission went through previously. The QR code should already be SOLD. Verify with lookup. |
| 500 | Edgar server error | **Stop immediately.** All submissions will fail. Report to governor. Check `/events-catalog` endpoint. The txn IDs are likely recorded server-side, meaning retries with the same payload will get 409. DO NOT mass-retry. |
| 4xx (other) | Client error (bad payload) | Log the error, skip this QR code, continue to next. |

**Critical: if ANY submission gets HTTP 500, ABORT the entire batch.** Do NOT continue
through the remaining codes — every one will also 500, and all txn IDs will be "burned"
(409 on retry with same payload).

## 6. Verifying after submission

After each submission (or batch), verify QR codes flipped to SOLD:

```bash
python3 -m truesight_dao_client.modules.lookup_qr_code --qr <code>
# Status should now be "SOLD", not "MINTED"
```

## 7. Handling a "stuck" batch (Edgar 500 mid-batch)

If Edgar returns 500 for some codes:
1. Note which QR codes were submitted (txn IDs burned server-side)
2. Wait for Edgar to recover
3. Re-submit with **modified payloads** (add retry timestamp to Submission Source
   so signatures differ) — otherwise the burned txn IDs will cause 409
4. Example modified payload:

```python
attrs = [
    ("Item", qr),
    ("Sales price", SALES_PRICE),
    ("Sold by", SOLD_BY),
    ("Cash proceeds collected by", CASH_COLLECTED_BY),
    ("Owner email", OWNER_EMAIL),
    ("Submission Source", f"dao_client / bulk cash sale / retry-{int(time.time())}"),
]
```

## 8. Example — full SOHA batch (canonical reference)

```python
QR_CODES = [
    "2024OSCAR_20260330_1",  "2024OSCAR_20260330_2",  "2024OSCAR_20260330_3",
    "2024OSCAR_20260330_4",  "2024OSCAR_20260330_5",  "2024OSCAR_20260330_6",
    "2024OSCAR_20260330_7",  "2024OSCAR_20260330_8",  "2024OSCAR_20260330_9",
    "2024OSCAR_20260330_10", "2024OSCAR_20260330_11", "2024OSCAR_20260330_12",
    "2024OSCAR_20260330_13", "2024OSCAR_20260330_14", "2024OSCAR_20260330_15",
    "2024OSCAR_20260330_17", "2024OSCAR_20260330_19", "2024OSCAR_20260330_20",
    "2024OSCAR_20260330_21", "2024OSCAR_20260330_22", "2024OSCAR_20260330_30",
    "2024OSCAR_20260330_34", "2024OSCAR_20260330_35", "2024OSCAR_20260330_36",
    "2024OSCAR_20260121_22", "2024OSCAR_20260121_24", "2024OSCAR_20260121_25",
    "2024OSCAR_20260121_26", "2024OSCAR_20260121_27", "2024OSCAR_20260121_28",
    "2024OSCAR_20260121_29", "2024OSCAR_20260121_30", "2024OSCAR_20260121_31",
    "2024SA_20251227_35",    "2024SA_20251227_36",    "2024SA_20251227_37",
    "2024SA_20251227_38",    "2024SA_20251227_39",    "2024SA_20251227_40",
    "2024SA_20251227_42",
]
```

Batch execution script template: `~/Applications/dao_client/submit_soha_david_campbell_sales.py`

## 9. RESUME HERE

Sophia's first turn for a batch sale:
1. Read this plan from `read_repo_file` on GitHub `main`
2. Health-check Edgar
3. Validate QR codes via `lookup_qr_code`
4. Build and run the batch submission script (or CLI loop)
5. Report results to governor

## 10. Acceptance

- [ ] Sophia can receive a batch sale request and autonomously submit all QR codes
- [ ] Sophia health-checks Edgar before starting
- [ ] Sophia stops on first HTTP 500 (doesn't burn remaining txn IDs)
- [ ] Sophia verifies at least one QR code flipped to SOLD after submission
