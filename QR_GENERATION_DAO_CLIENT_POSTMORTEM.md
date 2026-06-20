# QR Code Generation via dao_client / GAS — Failures & Workarounds

**Date:** 2026-06-20
**Context:** Repackaging batch `b08d324b-e2f4-4645-9d25-ee43f9e7d9e0` — 7 nibs → 3 ceremonial (Oscar/AGL4) + 15 chocolate bars (81%, 50g). After currencies were created on the Main Ledger, QR codes needed to be generated and compiled.

---

## What was attempted via dao_client

### 1. Batch QR Code Request via Edgar (`truesight-dao-batch-qr-generator`)

```bash
python -m truesight_dao_client.modules.batch_qr_generator \
    --currency 'Ceremonial Cacao Kraft Pouch ... | Kirsten 20260620 | San Francisco - AGL4' \
    --quantity 3
```

**Result:** HTTP 200, signature verified. Event landed in Telegram Chat Logs.

**Failure:** QR codes were never generated. Triggering `?action=processDonationMintsFromTelegramChatLogs` returned `{"minted":0,"rejected":0}` — the Telegram-based processor didn't pick up the `[BATCH QR CODE REQUEST]` events. Triggering `?action=processQRCodeGenerationTelegramLogs` returned an error requiring a missing Script Property (`QR_CODE_TELEGRAM_PROCESSOR_EXEC_BASE`). The async Edgar→GAS→GitHub pipeline is not end-to-end functional for batch QR generation at this time.

### 2. Direct GAS API (`?action=generate`)

```
GET .../exec?action=generate&product_name=...&quantity=3
```

**Failure chain:**

| # | Error | Root cause | Fix |
|---|-------|-----------|-----|
| 1 | `Currency not found` | New Currency rows only had cols A/B/N/O populated. Col C (`isSerializable`) was empty — the QR generator requires `TRUE`. | Set col C = TRUE via gspread |
| 2 | `Currency not found` (again) | The GAS reads from Google Sheets `Currencies` tab, not from GitHub `currencies.json`. The sheet is the source of truth. | (same fix as above) |
| 3 | `cell U1572 violates data validation rules` | The deployed GAS writes `Manager Name` (not `batch_id`) to column U. The direct API path (`?action=generate`) with no authenticated user produces empty/null values that violate the sheet's data validation on col U. The source code at `qr_code_web_service.js` differs from what's actually deployed — the source pushes `batchId` to col U but the deployed code writes a different schema. | Could not fix — requires GAS code update or operator with sheet edit permissions to bypass validation |

### 3. Repackaging GAS — missing columns

The repackaging currency ingest GAS (`Code.gs` at `agroverse-inventory/gas/repackaging-currency-ingest/`) only writes columns A (Currency), B (unit cost), N (raw request text), O (composition URL) to the `Currencies` tab. It does NOT set:
- Column C (`isSerializable`) — needed for QR generation
- Columns E-J (landing page, ledger, farm name, state, country, year) — needed for QR row data
- Column D (product image) — needed for QR row

This means **every repackaging batch requires manual follow-up** to populate these columns before QR codes can be generated.

---

## Workarounds applied (in order)

1. **`isSerializable` fix:** Used gspread with `market_research/google_credentials.json` to set col C = TRUE for both new Currency rows.

2. **Farm info fix:** Populated columns E (landing page), G (farm name), H (state), I (country), J (year) with Oscar's Farm data via gspread.

3. **QR row creation:** Wrote 18 QR code rows directly to `Agroverse QR codes` sheet via gspread (columns A-V), bypassing the GAS API entirely. Used `2024OSCAR_CC_*` and `2024OSCAR_CB_*` naming convention.

4. **Compiled label generation:** Called `generate_qr_image()` and `compile_image()` from `lineage-assets/scripts/qr_generator/batch_compiler.py` directly for just the 18 rows, producing print-ready labels with Agroverse logo, farm info, and serial numbers.

---

## Recommendations for Sophia / operator

### Immediate (manual)
- [ ] Verify the compiled QR images in `~/Applications/tmp/` look correct (open one and check layout)
- [ ] Column K (QR code location) in the sheet still points to GitHub — the images aren't on GitHub since the webhook wasn't triggered. Either upload them manually or run the full `batch_compiler.py` when the GAS pipeline is fixed.

### Medium-term (code fixes)
- [ ] **Repackaging GAS:** Add col C (`isSerializable = TRUE`) and cols E-J (farm info) to the Currency row writes in `Code.gs:processBatchData_()` so repackaging outputs are immediately QR-ready.
- [ ] **QR generator GAS:** Fix the `?action=generate` endpoint to handle anonymous calls (empty manager name should pass validation, or the endpoint should require auth).
- [ ] **QR generator GAS:** Sync the deployed code with the source at `qr_code_web_service.js` — the column schema mismatch (source says batch_id at col U, deployed has Manager Name) caused confusion.
- [ ] **Edgar → Telegram → GAS pipeline:** Debug why `processDonationMintsFromTelegramChatLogs` returns `minted:0` for valid `[BATCH QR CODE REQUEST]` events. The end-to-end async path should work without requiring direct API calls.

### Process
- [ ] Document that repackaging batches currently need manual `isSerializable` + farm info population before QR codes can be generated.
- [ ] Add a `post_repackaging_checklist` to `LEDGER_CONVERSION_AND_REPACKAGING.md`.

---

## Request ID reference

| What | ID |
|------|-----|
| Repackaging batch | `b08d324b-e2f4-4645-9d25-ee43f9e7d9e0` |
| Composition JSON | `https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/b08d324b-e2f4-4645-9d25-ee43f9e7d9e0.json` |
| QR rows | Sheet rows 1572–1589 on `Agroverse QR codes` tab |
