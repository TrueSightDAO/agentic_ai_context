# Partner Inventory Turnaround Deep-Dive Methodology

> **Purpose:** Replicable playbook for tracing the complete inventory journey of a single retail partner — from receipt through all exit paths — to verify sell-through rate accuracy and identify data pipeline gaps.

---

## When to Use This

Run this deep dive when a partner's velocity metrics (from `partners-velocity.json`) show suspicious patterns:
- Zero sales despite high restock frequency
- "0" sales in `sales_12m_monthly_avg` but partner appears active
- Gap between restocks received and inventory-on-hand + reported sales
- Any partner where the numbers "don't add up"

---

## Step 1: Establish Total Inventory Inflow

**Data source:** `Inventory Movement` sheet (Telegram & Submissions spreadsheet `1qbZZhf-…`, gid `83682662`)

Query all rows where `RECIPIENT NAME` (column I) matches the partner's name(s). Sum the `AMOUNT` for all cacao product rows (exclude USD rows).

Partner name variations to check:
- Exact name from `contributor_contact_id` in `Agroverse Partners`
- Display name from `partner_name`
- Common variations (Kelly vs Kelley, full names, abbreviations)

```sql
-- Pseudocode
SELECT SUM(AMOUNT) 
FROM InventoryMovement 
WHERE RECIPIENT_NAME ILIKE ANY(%variations%) 
  AND CURRENCY NOT LIKE '%USD%'
  AND STATUS IN ('NEW', 'PROCESSED')
```

**Record:** Total bags received, by product and date.

---

## Step 2: Find All Outflow Transactions

### 2a. Check QR Code Sales sheet

**Data source:** `QR Code Sales` sheet (Telegram & Submissions spreadsheet, index/detect by header or gid)

**CRITICAL:** The velocity script (`sync_partners_velocity.py`) uses `Sold By` (column P, index 15). Many sales rows have populated `Reporter Name` (column D, index 3) but **empty** `Sold By` — these sales are silently dropped. Always check BOTH columns.

Query all rows where either `Sold By` or `Reporter Name` matches the partner:

```python
# The buggy check (what the script does):
sold_by = row[15]  # Sold By column
if not sold_by:
    continue  # DROPS sales even if Reporter Name has the partner

# What the deep dive should do:
reporter = row[3]  # Reporter Name column  
sold_by = row[15]  # Sold By column
if partner_name in (sold_by or '').lower() or partner_name in (reporter or '').lower():
    # This is a legitimate sale
```

**Record:** All QR codes sold, sale prices, dates, and whether Sold By was populated.

### 2b. Check Inventory Movement for returns

Query Inventory Movement where `SENDER NAME` (column H) matches the partner and `CURRENCY` is a cacao product (not USD).

**Record:** Bags returned to Gary Teh/Kirsten.

### 2c. Check for USD payments/settlements

Query Inventory Movement where `SENDER NAME` matches partner and `CURRENCY` is "USD". These are cash settlements for sales.

**Record:** All USD payments with dates and amounts.

---

## Step 3: Check QR Code Status

**Data source:** `Agroverse QR codes` sheet (Main Ledger `1GE7PUq-…`, gid `472328231`)

Cross-reference each QR code sent to the partner against its current status (`SOLD`, `MINTED`, etc.) and `Manager Name`. This reveals:
- Which QRs were actually sold
- Which QRs were assigned to other managers (cross-batch sales)
- Discrepancies between assigned and actual sale QRs

**Note:** Partners may sell QRs from batches NOT assigned to them in the Inventory Movement sheet (e.g., Kelly sold QRs from batch `2024OSCAR_20250805` that had `Manager Name: Kirsten Ritschel`). These still count as legitimate sales.

---

## Step 4: Cross-Reference with Telegram Chat Logs

**Data source:** `Telegram Chat Logs` sheet (Telegram & Submissions spreadsheet)

Search for partner name variations across all columns. Look for:
- `[SALES EVENT]` submissions
- `[CONTRIBUTION EVENT]` entries related to the partner
- Shipping/tracking discussions
- Inventory management conversations

This provides qualitative context for transaction patterns.

---

## Step 5: Reconcile the Numbers

Build the reconcilation table:

| Category | Count |
|----------|-------|
| Bags received (inflow) | A |
| Bags returned (outflow) | B |
| Bags sold (QR confirmed) | C |
| Bags remaining (current inventory) | D |
| **Balance: A - B - C - D** | **Must = 0** |

If the balance is non-zero:
1. Missing bags may be in cross-batch QRs not tracked in the partner's assigned batch
2. Sales may be recorded under a slightly different name
3. Inventory may have been damaged/lost without formal write-off
4. The inventory snapshot JSON may be stale

---

## Step 6: Verify Against Velocity JSON

Read `agroverse-inventory/partners-velocity.json` and compare the `sales_*` fields against what you found.

Common causes of inaccurate velocity data:

| Issue | Symptom | Root Cause |
|-------|---------|------------|
| **Empty `Sold By`** | Sales exist but show as 0 in velocity | `sync_partners_velocity.py:264` drops rows with empty `Sold By`, but `Reporter Name` is populated |
| **Cross-batch QRs** | Sales don't match assigned QRs | Partner sold QRs from a batch assigned to another manager; `contributor_to_partners` join fails |
| **Name mismatch** | `Sold By` has name but doesn't match partner | `contributor_contact_id` differs from display name used in `Sold By` |
| **Currency→SKU resolution** | Sales dropped at line 349 | Long-form currency strings don't match the `Currencies` sheet's SKU cross-reference |

---

## Example: Love Wisdom Power (Kelly Springer)

**Step 1:** 30 bags received from Kirsten Ritschel (Aug 2025 - Mar 2026)

**Step 2a:** 12 bags sold via QR Code Sales — all had `Reporter Name: Kelly Springer` but **empty `Sold By`** → dropped by velocity script

**Step 2b:** 2 bags returned to Gary Teh (Aug 2025)

**Step 2c:** $204 USD received in 4 payments ($34 + $85 + $68 + $17), matching 12 sales at $17 each

**Step 3:** QR Status showed 4 Oscar bags SOLD, 4 Santa Ana bags SOLD, 2 QRs (_20, _21) assigned to OTHER managers — cross-batch sales correctly attributed to Kelly via Reporter Name

**Step 4:** Telegram logs confirmed shipping, setup, and sales conversations

**Step 5:** 30 - 2 - 12 - 16 = 0 ✓ Perfect reconciliation

**Step 6:** Velocity JSON showed `sales_12m_monthly_avg: 0` — the primary bug is empty `Sold By` column in QR Code Sales

---

## Fixing the Velocity Pipeline

In `sync_partners_velocity.py`, function `read_qr_code_sales()` (line 249):

**Current code (broken):**
```python
sold_by = (row[QRS_COL_SOLD_BY] if len(row) > QRS_COL_SOLD_BY else "").strip()
if not sold_by:
    continue  # Drops rows where Sold By is empty
```

**Fix (fallback to Reporter Name):**
```python
sold_by = (row[QRS_COL_SOLD_BY] if len(row) > QRS_COL_SOLD_BY else "").strip()
if not sold_by:
    # Fall back to Reporter Name (column D, index 3) when Sold By is empty
    sold_by = (row[3] if len(row) > 3 else "").strip()
if not sold_by:
    continue
```

This single-line fix would recover Kelly's 12 "missing" sales and any other partners affected by the same empty-`Sold By` issue.

---

## When the Deep Dive Is Complete

After reconciling all numbers to zero, you have two outcomes:

1. **Partner IS selling** but velocity data is wrong → Fix the data pipeline
2. **Partner is NOT selling** and inventory is genuinely stuck → Operational action needed (recover stock, convert to wholesale, sunset)

Do NOT rely on `partners-velocity.json` alone for sell-through decisions without first verifying against raw source data.

---

*Created 2026-05-11 | claude | Deep dive methodology for partner inventory turnaround analysis. Companion to `PARTNER_VELOCITY_PROPOSAL.md`. Updated `README.md` and `PROJECT_INDEX.md`.*
