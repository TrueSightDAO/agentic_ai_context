# QR Code Registration: dao_client + GAS Implementation Plan

**Date:** 2026-06-12
**Author:** Sophia (TrueSight Autopilot)
**Status:** Draft — awaiting governor approval

---

## 1. Problem Statement

There is no way to register a single Agroverse QR code from the autopilot or dao_client. The existing flow requires:
- Adding a row to the "Agroverse QR codes" Google Sheet manually
- Running the batch compiler from a macOS machine with the right fonts and templates

This means the autopilot cannot mint a QR code for an event (like SF Tech Fest) without manual sheet editing. The gap is: **no GAS endpoint for single QR registration** and **no dao_client command to call it**.

---

## 2. Solution Architecture

```
dao_client register_qr_code
  |
  |  HTTP POST (signed params)
  v
GAS Web App (qr_code_web_service.gs on 1MnAsIQAxcSf...)
  |  Validates fields, checks duplicates
  |  Creates row in "Agroverse QR codes" sheet
  |  Triggers GitHub Actions webhook
  v
GitHub Actions (lineage-assets)
  |  Runs batch_compiler.py
  |  Generates branded QR PNG
  |  Commits PNG + JSON manifest
  v
QR code live at truesight.me/qr/?id=<code>
```

### Component Breakdown

| Component | Repo | What it does |
|-----------|------|-------------|
| **dao_client command** | `dao_client` | New `register_qr_code` CLI command. Signs params, POSTs directly to GAS web app URL. |
| **GAS web app** | `tokenomics` (GAS script `1MnAsIQAxcSf...`) | `handleRegisterSingleQRCode()` in `qr_code_web_service.gs`. Validates, deduplicates, appends row, triggers GitHub Actions. |
| **GitHub Actions** | `lineage-assets` | Existing `generate_qr_batch.sh` workflow. Triggered by GAS webhook. Generates branded QR PNG + manifest. |

---

## 3. Implementation Phases

### Phase 1: GAS Endpoint (Single QR Registration)

**PR1 — `tokenomics` — Add `register_single_qr_code.gs`**

New GAS file that adds a `doGet(e)` handler for `?action=registerSingleQRCode` with parameters:
- `qr_code` (string) — the QR code ID (e.g. `SFTF_FR_20260612_1`)
- `landing_page` (string) — the URL the QR points to
- `farm_name` (string) — display name
- `state` (string)
- `country` (string)
- `year` (string) — harvest year
- `currency` (string) — product name
- `status` (string) — defaults to `SAMPLE`
- `manager` (string) — who minted it
- `creation_date` (string) — YYYYMMDD

**Logic:**
1. Validate required fields
2. Check for duplicate `qr_code` in sheet
3. Append row to "Agroverse QR codes" tab
4. Trigger GitHub Actions webhook for single QR generation
5. Return success/error JSON

**Deployment:** clasp mirror `1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn`

---

### ~~Phase 2: Edgar Endpoint~~ (REMOVED)

No Edgar hop needed. dao_client POSTs directly to the GAS web app URL.

Nginx can optionally proxy `POST /dao/qr-code-register` to the GAS `/exec` URL for a cleaner API surface, but this is a deployment concern, not a code change.

---

### Phase 3: dao_client Command

**PR3 — `dao_client` — Add `register_qr_code` CLI command**

```bash
truesight-dao-register-qr-code \
  --qr-code "SFTF_FR_20260612_1" \
  --landing-page "https://agroverse.shop/friends-of-the-rainforest" \
  --farm-name "SF Tech Fest" \
  --state "CA" \
  --country "USA" \
  --year "2026" \
  --currency "Friends of the Rainforest" \
  --status "SAMPLE" \
  --manager "Gary Teh"
```

**Logic:**
1. Build query params from CLI args
2. POST directly to GAS web app URL: `https://script.google.com/macros/s/AKfycbzMJom6MSHfbBL2RWOPrHg62iau8lgDbuAjxFbd3eBQ9L7SIXMBvh8tkdko4k1J_PMf/exec?action=registerSingleQRCode&...`
3. Print result + QR code URL

**No Edgar dependency.** The GAS web app handles validation, deduplication, sheet write, and webhook trigger.

---

### Phase 4: Autopilot Integration

**PR4 — `truesight_autopilot` — Wire autopilot to use new command**

Update the autopilot's QR code workflow so that when a governor asks to mint a QR code:
1. Call `dao_client register_qr_code` with the parameters
2. Wait for the GAS + GitHub Actions pipeline
3. Report the QR code URL back

---

## 4. Gates

| Gate | Phase | Description | Who |
|------|-------|-------------|-----|
| G1 | Phase 1 | GAS deploys, manual test with curl | Gary |
| G2 | ~~Phase 2~~ | ~~Edgar endpoint~~ — removed | — |
| G3 | Phase 3 | dao_client command works end-to-end | Gary |
| G4 | Phase 4 | Autopilot successfully mints a QR for SF Tech Fest | Gary |

---

## 5. UAT (User Acceptance Tests)

### U1: GAS Single QR Registration
1. `curl` the GAS web app with `?action=registerSingleQRCode&qr_code=UAT_TEST_001&...`
2. Verify row appears in "Agroverse QR codes" sheet
3. Verify status is `MINTED`

### U2: Duplicate Detection
1. Register the same QR code twice
2. Verify second call returns error "QR code already exists"

### ~~U3: Edgar Endpoint~~ (REMOVED)
No Edgar endpoint to test. dao_client → GAS directly.

### U4: dao_client Command
1. Run `truesight-dao-register-qr-code --dry-run`
2. Verify output shows correct payload and GAS URL
3. Run without `--dry-run`
4. Verify QR code appears in "Agroverse QR codes" sheet

### U5: End-to-End: SF Tech Fest QR
1. Run dao_client to register `SFTF_FR_20260612_1`
2. Wait for GitHub Actions to generate branded PNG
3. Verify PNG at `lineage-assets/pngs/SFTF_FR_20260612_1.png`
4. Verify JSON manifest at `lineage-assets/qrs/SFTF_FR_20260612_1.json`
5. Verify `https://truesight.me/qr/?id=SFTF_FR_20260612_1` resolves

### U6: Error Handling — Missing Fields
1. Call endpoint without required fields
2. Verify descriptive error message

### U7: Error Handling — Invalid Status
1. Call with invalid status value
2. Verify validation error

### U8: Batch Compatibility
1. Verify existing batch QR generation still works
2. Verify no regression in `processQRCodeGenerationTelegramLogs`

### U9: Autopilot Integration
1. Ask autopilot to "mint a QR code for SF Tech Fest"
2. Verify autopilot calls dao_client
3. Verify QR code is generated

---

## 6. Files to Create/Modify

### New Files
| File | Repo | Purpose |
|------|------|--------|
| `google_app_scripts/agroverse_qr_codes/register_single_qr_code.gs` | `tokenomics` | GAS endpoint for single QR registration |
| `dao_client/commands/register_qr_code.py` | `dao_client` | CLI command |
| ~~`sentiment_importer/app/controllers/qr_code_registration_controller.rb`~~ | ~~`sentiment_importer`~~ | ~~Edgar endpoint~~ — removed |

### Modified Files
| File | Repo | Change |
|------|------|--------|
| `dao_client/setup.py` | `dao_client` | Register new command entry point |
| `truesight_autopilot/app/qr_workflow.py` | `truesight_autopilot` | Wire autopilot to use new command |

---

## 7. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| GAS web app quota exceeded | Low | Single QR registration is lightweight |
| GitHub Actions webhook fails | Medium | GAS retries with exponential backoff |
| Duplicate QR code IDs | Low | Sheet-level unique check in GAS |
| Font/Helvetica missing on autopilot | Medium | Install fonts or use fallback in batch_compiler |

---

## 8. Timeline (Estimated)

| Phase | Effort | Dependencies |
|-------|--------|-------------|
| Phase 1: GAS | 2-3 hours | clasp access to `1N6o00N9VtRK...` |
| ~~Phase 2: Edgar~~ | ~~1-2 hours~~ | ~~removed~~ |
| Phase 3: dao_client | 1-2 hours | dao_client release |
| Phase 4: Autopilot | 1 hour | truesight_autopilot deploy |
| **Total** | **4-6 hours** | |

---

## 9. RESUME HERE

When governor says "go for it":
1. ~~PR1~~ ✅ GAS handler deployed (Phase 1 complete — `registerSingleQRCode` action live on `1MnAsIQAxcSf...` project)
2. ~~PR2~~ ❌ Removed — no Edgar endpoint needed
3. Open PR3: Add `register_qr_code` CLI command to `dao_client` that POSTs directly to GAS web app URL
4. Open PR4: Wire autopilot to call dao_client command
5. Run UAT U1, U2, U4-U9 (U3 removed)
6. Report results in this thread

**Gate: PRs are opened only — NEVER self-merge. Governor reviews and merges.**
