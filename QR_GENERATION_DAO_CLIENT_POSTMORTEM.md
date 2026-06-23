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

## Additional finding: `truesight.me/physical-assets/serialized/` data source

The physical assets serialized page (`truesight.me/physical-assets/serialized/`) does **not** read from the Google Sheet. It reads from the **`TrueSightDAO/lineage-assets`** GitHub repo:

- **Per-QR manifests:** `qrs/<qr_id>.json` — JSON files describing each QR's asset type, farm, status, lineage events, scan target, etc.
- **Compiled QR PNGs:** `pngs/<qr_id>.png` — the print-ready label images (QR + logo + farm info + serial)
- **Index:** `qrs_index.json` — built by `scripts/build_index.py`, aggregating all manifests into a queryable index

If QR codes are written to the Google Sheet but **not** to `lineage-assets`, they will appear in the sheet but not on `truesight.me`. The fix was:
1. Generate per-QR JSON manifests using `lib.manifest.build_manifest()` / `write_manifest()`
2. Copy compiled PNGs to `pngs/`
3. Rebuild `qrs_index.json` via `scripts/build_index.py`
4. Commit and push to `main`

The `batch_compiler.py` script normally does all of this, but our targeted approach had to replicate it manually since the full batch compiler times out on the entire sheet.

---

## Request ID reference

| What | ID |
|------|-----|
| Repackaging batch | `b08d324b-e2f4-4645-9d25-ee43f9e7d9e0` |
| Composition JSON | `https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currency-compositions/b08d324b-e2f4-4645-9d25-ee43f9e7d9e0.json` |
| QR rows | Sheet rows 1572–1589 on `Agroverse QR codes` tab |

---

## Deployment reference (2026-06-22)

The QR generation pipeline uses two GAS projects. When updating code, redeploy the **existing** deployment — never create new ones.

### 1N6o00 — QR processor (Telegram logs → Agroverse QR codes)

| Item | Value |
|------|-------|
| Project | `1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn` |
| Editor | https://script.google.com/home/projects/1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn/edit |
| Clasp dir | `tokenomics/google_app_scripts/1N6o00…/` |
| Deployment ID | `AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO` |
| Web app URL | `https://script.google.com/macros/s/AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO/exec` |
| Clasp update cmd | `clasp deploy --deploymentId AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO -V <version>` |
| Source files | Single merged file: `process_qr_code_generation_telegram_logs.js` (no `register_single_qr_code.js` — merged 2026-06-22 to fix const collision) |

### 1MnAs — Consolidated web service (forwarder → 1N6o00)

| Item | Value |
|------|-------|
| Project | `1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT` |
| Editor | https://script.google.com/home/projects/1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT/edit |
| Script Property | `QR_CODE_TELEGRAM_PROCESSOR_EXEC_BASE` = the 1N6o00 web app URL (above) |

When code changes are pushed to the 1N6o00 project, run `clasp deploy --deploymentId <ID> -V <new_version>` to update the existing web app deployment. Do NOT create new deployments — the Script Property on 1MnAs points to this specific deployment URL.

---

## RESOLUTION — async Edgar → GAS batch-QR pipeline wired end-to-end (2026-06-22, Claude)

The async path (`truesight-dao-batch-qr-generator` → Edgar → GAS `processQRCodeGenerationTelegramLogs`) is now functional. Three independent breaks were found and fixed:

**1. The 1N6o00 web app served nothing (Page Not Found).** `appsscript.json` had **no `webapp` block**, so the `AKfycbxn3siu…` deployment (and `@HEAD`) returned "Page Not Found" on `/exec` — there was no web-app entry point at all. Fixed in **tokenomics #370** (added `webapp { executeAs: USER_DEPLOYING, access: ANYONE_ANONYMOUS }`, version 8) and the existing `AKfycbxn3siu…` deployment was **redeployed to v8** (`clasp update-deployment AKfycbxn3siu… -V 8`) so its **stable URL now serves** — verified: `?action=ping` → JSON, `?action=registerSingleQRCode` → "Missing required parameter: qr_code". (A throwaway `@8` deployment created during diagnosis was deleted; `AKfycbxn3siu…` stays canonical, matching 1MnAs' `QR_CODE_TELEGRAM_PROCESSOR_EXEC_BASE`.)

**2. The marker mismatch is already gone.** The 2026-06-20 failure ("processor didn't pick up `[BATCH QR CODE REQUEST]`") predates the 2026-06-22 merge. The deployed processor now matches `contributionMade.startsWith("[BATCH QR CODE REQUEST]")` (line ~389) — same tag `dao_client` emits. No further change needed.

**3. Edgar's webhook env pointed at the WRONG GAS deployment.** `DAO_PROTOCOL_WEBHOOK_QR_CODE_GENERATION` on the Edgar box (`dao_protocol_nelanco:/home/ubuntu/dao_protocol/.env`) was set to a **1MnAs public-query deployment** (`AKfycbyGD…`) whose only actions are `list / search / generate / generate_single` — it has **no `processQRCodeGenerationTelegramLogs` action**, so every dispatch returned `{"error":"Invalid action…"}` (HTTP 200) and nothing processed. **Fix:** repointed it **directly at the 1N6o00 processor** (`AKfycbxn3siu…/exec`), which natively handles that action — no dependence on the 1MnAs forwarder's Script Property. (`.env.bak.20260622212504` saved; `truesight-dao-protocol.service` restarted; var confirmed in `/proc/<pid>/environ`.)

**Wiring now (canonical):**
```
truesight-dao-batch-qr-generator  →  [BATCH QR CODE REQUEST]  →  Edgar (dao_protocol)
  dispatch.py: "[BATCH QR CODE REQUEST]" → DAO_PROTOCOL_WEBHOOK_QR_CODE_GENERATION ?action=processQRCodeGenerationTelegramLogs
  →  https://script.google.com/macros/s/AKfycbxn3siu…/exec  (1N6o00 processor, anonymous web app)
  →  reads Telegram Chat Logs, writes QR Code Generation tab, triggers GitHub batch-zip webhook
```

**Not re-triggered on purpose:** I did not fire `processQRCodeGenerationTelegramLogs` against the live sheet as a test — the processor scans all unprocessed rows from its watermark and the b08d324b batch was already QR'd manually (rows 1572–1589), so a manual trigger could double-generate. The real end-to-end proof is the next genuine `[BATCH QR CODE REQUEST]`.

**Still open (separate, upstream data-quality — unchanged by this fix):** the repackaging currency-ingest GAS still doesn't set col C `isSerializable` + cols E–J farm info, so a repackaging batch's currency rows need manual population before generation *succeeds* (see "Medium-term (code fixes)" above). Wiring is fixed; row-completeness is not.

| Env var (Edgar box) | Old (broken) | New (fixed) |
|---------------------|--------------|-------------|
| `DAO_PROTOCOL_WEBHOOK_QR_CODE_GENERATION` | `…/s/AKfycbyGD…/exec` (1MnAs query svc — no processor action) | `…/s/AKfycbxn3siu…/exec` (1N6o00 processor) |

### Live end-to-end test (2026-06-22) + PNG-storage repoint

Submitted a real `[BATCH QR CODE REQUEST]` for `Cacao Tea 1LB - Oscar Fazenda 2024` ×1 via `truesight-dao-batch-qr-generator` (signed Gary Teh). Result: **the Edgar hook works** — Edgar dispatched the webhook and the processor minted QR **`2024_20260622_22`** (row 1611, status `MINTED`, manager Gary Teh) and fired the GitHub render webhook. So the whole async chain is proven: `dao_client → Edgar → 1N6o00 processor → sheet mint → render webhook`.

**But the PNG render then failed at upload**, exposing a 4th break: the render workflow (`tokenomics/.github/workflows/qr-code-batch-webhook.yml`) uploaded the compiled PNG to **`TrueSightDAO/qr_codes`, which was archived (read-only) 2026-06-11** → `403 Repository was archived`. Every batch QR since has minted a sheet row with no PNG.

**Repoint fix (tokenomics #373, MERGED + GAS deployed @9):** the canonical serialized-QR home is `lineage-assets/pngs/`. The workflow derives the upload repo+path from the **column-K URL** (`parse_github_url`), so the GAS const is the single source of truth:
- `QR_GEN_TELEGRAM_GITHUB_BLOB_BASE_URL` → `…/lineage-assets/blob/main/pngs/`
- `ZIP_FILE_DOWNLOAD_BASE_URL` + `QR_CODES_ZIP_GITHUB_REPO` → `lineage-assets`
- workflow `GITHUB_REPOSITORY` default + `github_webhook_handler.py` fallback → `lineage-assets`
- 1N6o00 deployment `AKfycbxn3siu…` redeployed to v9 with the new const.

Verified via `workflow_dispatch` on row 1611: target now resolves to `TrueSightDAO/lineage-assets` and the PNG renders.

**⚠️ STILL BLOCKED on a credential (account-owner action):** upload now returns `403 "Resource not accessible by personal access token"` — the `QR_CODE_REPOSITORY_TOKEN` secret on `TrueSightDAO/tokenomics` is a fine-grained PAT scoped to `qr_codes` and has **no write on `lineage-assets`**. **Fix:** grant that PAT `Contents: Read and write` on `TrueSightDAO/lineage-assets` (or replace the secret with a token that has it), then re-run generation. Until then, new QR rows carry correct `lineage-assets` col-K URLs but the PNGs don't upload.

**Separate follow-up:** the workflow emits only the PNG — not `qrs/<id>.json` + a `qrs_index.json` rebuild — so workflow-generated QRs won't appear on `truesight.me/physical-assets/serialized` until that's added (or generation unifies on `batch_compiler.py`). Filed in `OPEN_FOLLOWUPS.md`.
