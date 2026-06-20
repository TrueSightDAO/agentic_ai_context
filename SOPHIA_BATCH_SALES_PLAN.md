# SOPHIA Batch Sales Execution Plan

**Purpose:** Teach Sophia how to autonomously handle bulk QR code sales (cash or Stripe)
without the operator having to manually loop through 40 QR codes or debug Edgar errors.

**Status:** DRAFT — 2026-06-20
**Context:** From SOHA 40-bag cash sale experience — 40 submissions attempted, all failed
with HTTP 500 due to Edgar server-side issue. This plan codifies the pattern so Sophia
can self-serve next time.

---

## 1. The pattern

Every batch sale follows the same structure:

1. Receive QR code list + sale metadata from the governor
2. Validate QR codes exist in GAS (lookup, confirm status = MINTED)
3. Health-check Edgar (`GET /events-catalog` should return 200)
4. Submit one `[SALES EVENT]` per QR code (each must have a unique payload — different
   `Bulk order index` or unique `Submission Source` timestamp so signatures don't collide)
5. Report results

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
