# Self-Serve QR-Ready Currency Definition via Edgar — Execution Plan

**Handoff:** local LLM (Claude) → Sophia (autopilot)
**Created:** 2026-06-23
**Status:** GO-ready (parked in Telegram topic — see HANDOFF_MANIFEST.md / SOPHIA_HANDOFFS.md)
**Repos touched:** `dao_protocol` (CLI + Edgar dispatch), `tokenomics` (GAS 1N6o00 + deploy), `agentic_ai_context` (docs)
**Scope discipline:** §5a ONE PR PER TURN — on GO run **PR1 ONLY then STOP**; next turn resumes the next unit. Cross-repo PRs: **open PRs only, a human merges** (no self-merge). Advance markers in §5.

---

## 1. Context & goal

Today an LLM/operator can mint QR codes for an **existing, QR-ready** currency in one Edgar call
(`truesight-dao-batch-qr-generator`), verified working end-to-end 2026-06-22 (see
`QR_GENERATION_DAO_CLIENT_POSTMORTEM.md`). But a **brand-new SKU** cannot be QR'd via Edgar alone: the
`Currencies` tab row must first exist **and** carry the QR-required fields, and **no Edgar event sets
them**:

- The QR generator (`findCurrencyInAgroverse`) hard-requires **col C `Serializable = TRUE`** and reads
  **cols E–J** (landing_page, ledger, farm, state, country, year) onto the label.
- The repackaging ingest (`agroverse-inventory/gas/repackaging-currency-ingest/Code.gs`) writes only
  cols A/B/N/O; the asset-receipt ingest similarly skips C + E–J. So a currency created via Edgar lands
  **not QR-ready**, requiring a manual gspread fill before generation works.

**Goal:** add an Edgar event that **defines a QR-ready serializable currency** end-to-end, so a new SKU
goes from zero → QR-ready row → minted QR using **Edgar calls only**, no gspread.

**Non-goal (separate follow-up, unchanged):** the render workflow still emits only the PNG, not
`qrs/<id>.json` + `qrs_index.json`, so workflow-generated QRs don't yet appear on
`truesight.me/physical-assets/serialized`. Out of scope here.

## 2. Design

**New event:** `[CURRENCY DEFINITION EVENT]` (a reusable primitive — currencies get defined for reasons
beyond QR; keep it separate from QR minting).

**`Currencies` tab schema (confirmed):** A=name, B=Price in USD, C=Serializable, D=Product Image,
E=landing_page, F=ledger, G=farm name, H=state, I=country, J=Year, K=Unit Weight (grams),
L=Unit Weight (ounces).

**Payload fields** (named flags + `--attr` escape hatch, mirroring `batch_qr_generator`):
`Currency` (A, required), `Price in USD` (B), `Serializable` (C, default `TRUE`), `Product Image` (D),
`Landing Page` (E), `Ledger` (F), `Farm Name` (G), `State` (H), `Country` (I), `Year` (J),
`Unit Weight Grams` (K), `Unit Weight Ounces` (L).
**Required for QR-ready:** A, C=`TRUE`, E, F, G, H, I, J. (B/D/K/L recommended but optional.)

**Dispatch route:** `("[CURRENCY DEFINITION EVENT]", [("CURRENCY_DEFINITION",
"processCurrencyDefinitionsFromTelegramChatLogs")], False)` in `dispatch.py`. Webhook URL from
`DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION`.

**Handler home:** the **1N6o00** QR project (`process_qr_code_generation_telegram_logs.js`) — it already
reads `Currencies`, has signature-verification helpers (`isTelegramSignatureVerificationSuccess_`,
`getContributorEmailFromSignature`), and its deployment (`AKfycbxn3siu…`) is already wired to Edgar.
Reuse that same deployment URL for the new webhook (doGet routes by `action`). *(Pre-flight decision:
confirm 1N6o00 vs a dedicated currency-management GAS.)*

**Handler behavior:** scan `Telegram Chat Logs` for `[CURRENCY DEFINITION EVENT]` from the watermark,
verify signature, parse fields, **append** a row writing A–L, then **sort the tab A→Z full-width**
(cols A→L, row 2→last — same discipline as the repackaging ingest, so VLOOKUP/ARRAYFORMULA stay aligned).
**Idempotent:** skip if a row with col A == name already exists (report `skipped`); dedup on Telegram
Update ID like the other processors. `Serializable` written as boolean `TRUE`.

**Why GAS can write the protected `Currencies` tab:** the script executes as the owner (garyjob), which
already appends to `Currencies` elsewhere; service-account range-protection does not apply to owner-run
GAS. *(Pre-flight: confirm on the live sheet.)*

## 3. Pre-flight checklist (do BEFORE PR1 — cross-PR reads live here per §5a)

- [ ] **Repo map confirmed:** `dao_protocol` hosts BOTH the CLI (`truesight_dao_client/modules/`) and
      Edgar (`truesight_dao_client/server/dispatch.py`) — local checkout dir is `dao_client/`, remote is
      `github.com/TrueSightDAO/dao_protocol`. So PR1 (CLI + dispatch) is one repo.
- [ ] **§8 version-bump rule N/A:** it applies to `packages/dao-client/` (TS npm). This work touches
      `truesight_dao_client` (python) — no version bump required.
- [ ] **Confirm handler home** = 1N6o00 (reuse deployment `AKfycbxn3siu…`) vs a dedicated GAS. Default: 1N6o00.
- [ ] **Confirm `Currencies` owner-write** works (GAS runs as garyjob; appends already happen elsewhere).
- [ ] **Confirm the exact `Serializable` truthiness** the QR generator accepts — `findCurrencyInAgroverse`
      treats `row[2] === true || 'TRUE' || 'True'` as serializable. Write boolean `true` (renders as `TRUE`).
- [ ] **Decide UAT sheet:** `Currencies` is **prod-only** (no beta copy). Either (a) UAT on prod with a
      clearly-labeled `TEST …` currency then delete it, or (b) use the 1N6o00 **SANDBOX**
      `AGROVERSE_QR_SPREADSHEET_URL` (commented in the script) for the whole UAT. **Recommend (b)** if the
      sandbox sheet has a `Currencies` tab; else (a) with cleanup. **Operator confirms before UAT.**
- [ ] **Edgar box access** for PR3: `dao_protocol_nelanco` (`98.93.94.86`, ssh alias `dao_protocol_nelanco`),
      env `/home/ubuntu/dao_protocol/.env`, service `truesight-dao-protocol.service`. (Operator/Sophia gate.)
- [ ] **clasp deploy path** for PR2/PR3: 1N6o00 mirror is
      `tokenomics/google_app_scripts/1N6o00N9VtRK_…/`; redeploy the EXISTING deployment
      `AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO` (`clasp update-deployment <id> -V <new>`);
      do NOT create new deployments (Edgar + 1MnAs reference this URL). `appsscript.json` MUST keep its
      `webapp` block.

## 4. Sequenced plan (each unit = exactly ONE PR, self-contained)

### PR1 — `dao_protocol`: define-currency CLI + Edgar dispatch route
- **Add** `truesight_dao_client/modules/define_currency.py` → console script
  `truesight-dao-define-currency`, emitting `[CURRENCY DEFINITION EVENT]` with the §2 fields (named flags
  + `--attr LABEL=VALUE` + `--dry-run`). Mirror `modules/batch_qr_generator.py`.
- **Register** the console script in `pyproject.toml` `[project.scripts]`.
- **Add** the ROUTING entry to `truesight_dao_client/server/dispatch.py` (§2).
- **Test:** unit test asserting the dry-run payload renders the required labels; dispatch test (if the
  repo has them) that the new tag routes to `CURRENCY_DEFINITION`.
- **Acceptance:** `truesight-dao-define-currency --currency 'X' --serializable TRUE --farm … --dry-run`
  prints a well-formed signed `[CURRENCY DEFINITION EVENT]`; tests pass. No deploy.

### PR2 — `tokenomics`: GAS handler in 1N6o00
- **Add** `processCurrencyDefinitionsFromTelegramChatLogs()` to
  `google_app_scripts/1N6o00…/process_qr_code_generation_telegram_logs.js`: watermark scan, sig-verify
  (reuse `isTelegramSignatureVerificationSuccess_`), parse fields, append A–L QR-ready row, **sort A→Z
  full-width**, idempotent on col-A name + Update ID.
- **Add** a `doGet` action branch `action === 'processCurrencyDefinitionsFromTelegramChatLogs'`.
- **Test:** `node --check`; a small pure-function test for the field parser if practical.
- **Acceptance:** code merged; `node --check` clean. No deploy (PR3).

### PR3 — DEPLOY + WIRE (operator/prod gate)
- `clasp push` 1N6o00 from the mirror; `clasp update-deployment AKfycbxn3siu… -V <new>` (reuse existing).
- On `dao_protocol_nelanco`: back up `.env`, set
  `DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION=https://script.google.com/macros/s/AKfycbxn3siu…/exec`,
  restart `truesight-dao-protocol.service`, verify the var in `/proc/<pid>/environ` + `/ping` 200.
- Harmless probe: `…/exec?action=processCurrencyDefinitionsFromTelegramChatLogs` returns JSON (0 processed).
- **Acceptance:** service healthy; var live; probe returns clean JSON.

### PR4 — (optional convenience) auto-define in the batch-QR flow
- Extend `truesight-dao-batch-qr-generator` (and/or the 1N6o00 processor): when the currency is missing
  AND the batch request carries define-fields, define the QR-ready row before minting — so a new SKU is
  one call. **Optional; defer if PR1–PR3 + UAT already satisfy the operator.**
- **Acceptance:** one `batch_qr_generator` call with define-fields for a never-seen SKU mints a QR.

### PR5 — docs
- Update `AGROVERSE_QR_CODE_BATCH_GENERATION.md` (new define event + QR-ready field list),
  `LEDGER_CONVERSION_AND_REPACKAGING.md` (point new-currency creation at the define event),
  `QR_GENERATION_DAO_CLIENT_POSTMORTEM.md` (note the gap is now closeable via Edgar).
- **Acceptance:** docs describe the zero→QR-ready→minted flow via Edgar only.

## 5. Resume tracker (§5c Advance markers)

**RESUME HERE → PR1**

| Unit | Advance | PR opened | Merged (human) | Deployed | Contribution reported |
|------|---------|-----------|----------------|----------|----------------------|
| PR1 — CLI + dispatch (`dao_protocol`) | `auto` | ☐ | ☐ | n/a | ☐ |
| PR2 — GAS handler (`tokenomics`) | `auto` | ☐ | ☐ | n/a | ☐ |
| PR3 — deploy + wire env (**OPERATOR-run**: clasp + prod ssh; Sophia writes the runbook only — see §8) | `gate: operator runs clasp + Edgar env change` | ☐ | ☐ | ☐ | ☐ |
| PR4 — auto-define (optional) | `gate: confirm operator wants it` | ☐ | ☐ | ☐ | ☐ |
| PR5 — docs | `auto` | ☐ | ☐ | n/a | ☐ |
| UAT — human, beta/sandbox | `gate: human-run completion gate` | ☐ | ☐ | ☐ | ☐ |

**Gate rules:** Sophia opens PRs only and **never self-merges** (cross-repo); each PR turn STOPS after
opening the PR. After each unit merges, **report the DAO contribution before the next** (see
`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`). Fail-closed: anything ambiguous = gate.

## 6. UAT phase (human-run; completion gate — never prod money, sandbox or labeled-test + cleanup)

- **U1 — define via Edgar.** Run `truesight-dao-define-currency --currency 'TEST QR Currency <date>'
  --serializable TRUE --price-usd 25 --landing-page <url> --ledger <url> --farm 'Oscar Farm' --state Bahia
  --country Brazil --year 2024`. **Expect:** Edgar HTTP 200, `signature_verification: success`.
- **U2 — row is QR-ready.** Open the `Currencies` tab (sandbox or prod). **Expect:** a new row with
  A=name, **C=TRUE**, E–J populated; tab still sorted A→Z; no duplicate.
- **U3 — generate a QR for it.** `truesight-dao-batch-qr-generator --currency 'TEST QR Currency <date>'
  --quantity 1`. **Expect:** QR row mints (`MINTED`), PNG lands in `lineage-assets/pngs/…` (HTTP 200).
- **U4 — idempotency.** Re-submit the same define event. **Expect:** `skipped` (no duplicate Currencies row).
- **U5 — cleanup.** Delete the TEST currency row + the test QR row (and PNG if generated).
- **Acceptance criterion:** a brand-new SKU went zero → QR-ready → minted QR via **Edgar calls only**,
  no gspread, with idempotency holding. PASS closes the handoff.

## 7. Risks & notes

- **Currencies is prod-only & range-protected** — owner-run GAS writes fine; UAT must use sandbox or a
  labeled TEST row with cleanup (pre-flight decision).
- **Substring dispatch** — never put the literal `[CURRENCY DEFINITION EVENT]` (or any `[… EVENT]`) inside
  a *field value*; the dao-client guard rejects it and Edgar dispatches by substring
  (`reference_edgar_event_dispatch_substring`).
- **Sort-after-append is mandatory** — skipping it misaligns downstream VLOOKUP/ARRAYFORMULA on other tabs.
- **Token coupling (orthogonal)** — QR PNG upload currently uses `ORACLE_ADVISORY_PUSH_TOKEN`; unrelated to
  this plan but see the OPEN_FOLLOWUPS hardening note.
- **Reference example for plan shape:** `EDGAR_DAO_EXTRACTION_PLAN.md`, `SCORING_REVIEW_QUEUE_PLAN.md`.

---

## 8. Turnkey appendix for Sophia (paste-ready — minimise discovery, stay inside the round budget)

> **Read only the cited line ranges, not the whole 1854-line GAS file.** Each PR below is sized to
> finish well inside `CHAT_MAX_TOOL_ROUNDS`. If a turn starts to sprawl, checkpoint and STOP.

### PR1 (`dao_protocol`) — paste-ready

**New file `truesight_dao_client/modules/define_currency.py`** (the CLI is a declarative factory —
`build_event_cli` auto-generates `--kebab-case` flags from `canonical_labels`):

```python
#!/usr/bin/env python3
"""Submit [CURRENCY DEFINITION EVENT] to Edgar — define a QR-ready serializable currency.

Writes a Currencies-tab row carrying the fields the QR generator requires (col C
Serializable=TRUE + landing/ledger/farm/state/country/year), so a brand-new SKU can be
QR'd via Edgar alone. Browser equivalent: none yet (CLI-first).

    python -m truesight_dao_client.modules.define_currency \\
        --currency 'Cacao Tea 1LB - NewFarm 2025' --serializable TRUE \\
        --price-in-usd 25 --landing-page 'https://...' --ledger 'https://...' \\
        --farm-name 'NewFarm' --state Bahia --country Brazil --year 2025 --dry-run
"""
import sys
from ..edgar_client import build_event_cli
from ..validators import (
    currency_code, normalize_currency, normalize_number,
    positive_number, positive_integer, url_or_empty, google_sheets_url_or_empty,
)

main = build_event_cli(
    event_name='CURRENCY DEFINITION EVENT',
    canonical_labels=[
        'Currency', 'Price in USD', 'Serializable', 'Product Image',
        'Landing Page', 'Ledger', 'Farm Name', 'State', 'Country', 'Year',
        'Unit Weight Grams', 'Unit Weight Ounces',
    ],
    required_labels=['Currency', 'Serializable', 'Landing Page', 'Ledger',
                     'Farm Name', 'State', 'Country', 'Year'],
    validators={
        'Currency': currency_code,            # relax to `required` if it rejects a valid new name
        'Price in USD': positive_number,
        'Year': positive_integer,
        'Landing Page': url_or_empty,
        'Ledger': google_sheets_url_or_empty,
    },
    normalizers={'Currency': normalize_currency, 'Price in USD': normalize_number},
)

if __name__ == "__main__":
    sys.exit(main())
```
*(If `build_event_cli` requires a `dapp_page` arg, pass `dapp_page=None`. Template to copy:
`modules/batch_qr_generator.py` — same shape, fewer labels.)*

**`pyproject.toml` `[project.scripts]`** — add:
```
truesight-dao-define-currency = "truesight_dao_client.modules.define_currency:main"
```

**`truesight_dao_client/server/dispatch.py`** — add to the `ROUTING` list (next to the other QR rows):
```python
("[CURRENCY DEFINITION EVENT]", [("CURRENCY_DEFINITION", "processCurrencyDefinitionsFromTelegramChatLogs")], False),
```

**Test:** mirror an existing module test — assert `--currency X --serializable TRUE … --dry-run` renders
`[CURRENCY DEFINITION EVENT]` with the required labels. (§8 dao-client version bump does NOT apply — that's
the `packages/dao-client/` TS package, not `truesight_dao_client`.)

**Acceptance:** dry-run prints a well-formed signed event; `pytest` green. Open PR, STOP.

### PR2 (`tokenomics`) — GAS handler skeleton (read only lines 59-66, 204-236, 304-360, 801-836)

Add a `doGet` branch (next to the existing `action ===` branches, ~line 1670) and this handler. It mirrors
`processQRCodeGenerationTelegramLogs` (watermark scan + dedup + sig-verify) but writes a Currencies row:

```javascript
// in doGet(e):
if (action === 'processCurrencyDefinitionsFromTelegramChatLogs') {
  return ContentService.createTextOutput(JSON.stringify(processCurrencyDefinitionsFromTelegramChatLogs()))
    .setMimeType(ContentService.MimeType.JSON);
}

function cdef_(text, label) {            // field extractor — same idea as extractCurrencyName (line 204)
  var m = (text || '').match(new RegExp('- ' + label + ':\\s*(.+)$', 'm'));
  return m ? m[1].trim() : '';
}

function processCurrencyDefinitionsFromTelegramChatLogs() {
  var logTab = SpreadsheetApp.openByUrl(QR_GEN_TELEGRAM_MAIN_WORKBOOK_URL).getSheetByName(telegramLogTabName);
  var cur = SpreadsheetApp.openByUrl(AGROVERSE_QR_SPREADSHEET_URL).getSheetByName('Currencies');
  var existing = {}; var nA = cur.getLastRow();
  if (nA >= 2) cur.getRange(2,1,nA-1,1).getValues().forEach(function(r){ existing[String(r[0]).trim().toLowerCase()] = true; });
  var processed = 0, skipped = 0;
  var last = logTab.getLastRow();
  var rows = logTab.getRange(2, 1, last - 1, TELEGRAM_LOG_READ_LAST_COL).getValues();  // see line 370 for col-count const
  rows.forEach(function(row) {
    var contributionMade = row[6];       // col G = contribution text (see line ~377-391)
    if (!contributionMade || String(contributionMade).indexOf('[CURRENCY DEFINITION EVENT]') !== 0) return;
    var sigRaw = row[/* signature-status col index, see line ~391-395 */ 15];
    if (!isTelegramSignatureVerificationSuccess_(sigRaw)) return;                       // reuse helper line 59
    var name = cdef_(contributionMade, 'Currency');
    if (!name || existing[name.toLowerCase()]) { skipped++; return; }                   // idempotent
    var serial = (cdef_(contributionMade,'Serializable').toUpperCase() !== 'FALSE');     // default TRUE
    cur.appendRow([                       // cols A..L (Currencies schema)
      name,                               // A name
      Number(cdef_(contributionMade,'Price in USD')) || '',  // B
      serial,                             // C Serializable (boolean -> TRUE)
      cdef_(contributionMade,'Product Image'),   // D
      cdef_(contributionMade,'Landing Page'),    // E
      cdef_(contributionMade,'Ledger'),          // F
      cdef_(contributionMade,'Farm Name'),       // G
      cdef_(contributionMade,'State'),           // H
      cdef_(contributionMade,'Country'),         // I
      cdef_(contributionMade,'Year'),            // J
      Number(cdef_(contributionMade,'Unit Weight Grams')) || '',   // K
      Number(cdef_(contributionMade,'Unit Weight Ounces')) || '',  // L
    ]);
    existing[name.toLowerCase()] = true; processed++;
  });
  SpreadsheetApp.flush();
  var lr = cur.getLastRow(), lc = cur.getLastColumn();                                  // sort A->Z full-width
  if (lr > 2) cur.getRange(2, 1, lr - 1, lc).sort({ column: 1, ascending: true });      // same as repackaging ingest
  return { status: 'ok', processed: processed, skipped: skipped };
}
```
**Confirm before commit (1 quick read each):** the exact col index of the signature-status cell (the `sigRaw`
`15` above is a guess — verify against the read near line 391-395) and `TELEGRAM_LOG_READ_LAST_COL`. Then
`node --check`. Open PR, STOP.

### PR3 — DEPLOY + WIRE = **operator step, not Sophia** (clasp auth + prod ssh)
Sophia almost certainly lacks clasp auth on the 1N6o00 project and ssh to `dao_protocol_nelanco`. So **PR3 is a
runbook Sophia writes, a human runs.** The exact steps (for Gary / a clasp-authed operator):
```bash
# 1. deploy GAS (from the 1N6o00 mirror dir)
clasp push --force
clasp update-deployment AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO -V <new>
# 2. wire Edgar (on the box)
ssh dao_protocol_nelanco
cp /home/ubuntu/dao_protocol/.env /home/ubuntu/dao_protocol/.env.bak.$(date -u +%Y%m%d%H%M%S)
# add: DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION=https://script.google.com/macros/s/AKfycbxn3siu…/exec
sudo systemctl restart truesight-dao-protocol.service
# 3. verify
curl -s localhost:8010/ping
curl -sL 'https://script.google.com/macros/s/AKfycbxn3siu…/exec?action=processCurrencyDefinitionsFromTelegramChatLogs'
```
**Acceptance:** `/ping` 200; var in `/proc/<pid>/environ`; probe returns `{"status":"ok","processed":0,...}`.

### Sophia execution notes
- **Targeted reads only:** for PR2, read the cited line ranges — do **not** load the whole file.
- **One PR per turn, then STOP.** After each merge, report the DAO contribution before the next unit.
- **You can't do PR3** (clasp/prod-ssh) — produce the runbook and hand it to the operator as a gate.
- If any turn approaches the round cap, **checkpoint your state into the PR/thread and STOP cleanly** rather
  than looping to the cap.
