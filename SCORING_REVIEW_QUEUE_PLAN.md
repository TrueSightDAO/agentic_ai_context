# Scoring Review Queue — Implementation Plan

**Status:** Draft · **Created:** 2026-06-18
**Handoff thread:** [Telegram topic 7191](https://t.me/c/3919341801/7191)

---

## 1. Problem Statement

Today, after Grok scores a `[CONTRIBUTION EVENT]` and writes it to the **Scored Chatlogs** sheet (spreadsheet `1Tbj7H5ur_egQLRugdXUaSIhEYIKp0vvVv2IZ7WTLCUo`), the row sits with `Status = "Pending Review"` and `TDGs Issued = "0.00"`. A governor must:

1. Open the Google Sheet
2. Find the row
3. Review the contribution and Grok's provisioned TDG
4. Manually set `Status` to `"Reviewed"`
5. Manually enter the corrected `TDGs Issued` amount

Only then does the scheduled transfer script (`transfer_scored_contributions_to_main_ledger.js`) pick it up and move it to the main Ledger history.

This is slow, error-prone, and has no audit trail for who approved what.

---

## 2. Solution Overview

Replace the manual sheet-editing step with a **DApp-based review queue**:

1. **GitHub Actions cache generator** (Python, scheduled cron) reads Scored Chatlogs, finds rows with `Status = "Pending Review"` that haven't been cached yet, generates one JSON cache file per row in `treasury-cache/review-queue/`, and marks a `Cache Generated` column on the sheet.
2. **DApp review page** (new HTML page, or tab on the existing DApp) reads the cache files via Edgar, surfaces the oldest 10 with infinite scroll. Anyone can view the queue.
3. **Governor/Sentinel approves** by clicking Approve (or entering a corrected TDG amount) → browser signs a `[CONTRIBUTION REVIEW EVENT]` to Edgar. Edgar verifies the signer is a governor or Sentinel, rejects otherwise.
4. **On approval**, Edgar deletes the corresponding cache file from `treasury-cache/review-queue/` (via GitHub API).
5. **GAS write-back listener** (triggered by Edgar webhook) updates the Scored Chatlogs row: sets `Status = "Reviewed"` and `TDGs Issued` to the approved amount — but **only if the row isn't already reviewed/transferred**, preventing double-counting.

---

## 3. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GOOGLE SHEETS                                │
│                                                                     │
│  ┌──────────────────────┐    ┌──────────────────────────────┐      │
│  │ Telegram Chat Logs   │    │  Scored Chatlogs             │      │
│  │ (1qbZZ…)             │───→│  (1Tbj7H5ur…)                │      │
│  │                      │    │                              │      │
│  │ Column J = "Pending"  │    │  Col F = "Pending Review"    │      │
│  └──────────────────────┘    │  Col E = TDGs Provisioned    │      │
│         │                    │  Col G = TDGs Issued (0.00)  │      │
│         │ Grok scoring       │  Col K = Scoring Hash Key    │      │
│         ▼                    │  Col N = Cache Generated (NEW)│      │
│  ┌──────────────────────┐    └──────────┬───────────────────┘      │
│  │ Grok Scoring Script  │               │                          │
│  │ (1BHAGZd…)           │───────────────┘                          │
│  │ Scheduled GAS        │                                          │
│  └──────────────────────┘                                          │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (reads via Google Sheets API)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GITHUB ACTIONS (scheduled cron)                                    │
│                                                                     │
│  generate_review_cache.py                                           │
│  - Reads Scored Chatlogs via Google Sheets API                      │
│  - Finds rows with Status = "Pending Review" AND Col N empty        │
│  - Generates one JSON file per row                                  │
│  - Pushes to treasury-cache/review-queue/<hash_key>.json            │
│  - Writes timestamp to Col N ("Cache Generated")                    │
│  - Commits + pushes to main                                         │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (writes JSON cache files)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GITHUB REPO: treasury-cache                                        │
│                                                                     │
│  review-queue/                                                      │
│  ├── XzQ2EhAMD7MN8X0zFhvw.json    ← one file per pending review    │
│  ├── M52VB3RP2VLzU3UxLIf.json                                       │
│  └── ...                                                             │
│                                                                     │
│  Each file contains:                                                │
│  {                                                                  │
│    "hash_key": "XzQ2EhAMD7MN8X0zFhvw",                              │
│    "contributor": "gotothe_peak",                                   │
│    "contribution": "Who's looking for...",                          │
│    "rubric": "100TDG For every 1 hour...",                          │
│    "tdgs_provisioned": 8.33,                                        │
│    "status_date": "20241214",                                       │
│    "reporter": "gotothe_peak",                                      │
│    "generated_at": "2026-06-18T12:00:00Z"                           │
│  }                                                                  │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (reads directory listing + individual files)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  EDGAR (sentiment_importer / dao_protocol)                          │
│                                                                     │
│  GET /dao/review_queue?limit=10&offset=0                            │
│  - Reads treasury-cache/review-queue/ directory                     │
│  - Returns oldest 10 files (sorted by filename = hash_key age)      │
│  - Includes total count for infinite scroll                         │
│                                                                     │
│  POST /dao/submit_contribution  (CONTRIBUTION REVIEW EVENT)         │
│  - Verifies signer is governor or Sentinel (via RSA signature)      │
│  - On success: deletes cache file from treasury-cache/review-queue/ │
│  - Fires webhook to GAS write-back script                           │
└─────────────────────────────────────────────────────────────────────┘
         │                    ▲
         │ (serves queue)     │ (signed event)
         ▼                    │
┌─────────────────────────────────────────────────────────────────────┐
│  DAPP (dapp_beta / dapp_prod)                                       │
│                                                                     │
│  review_queue.html (new page)                                       │
│  - Anyone can view the queue                                        │
│  - Infinite scroll (calls Edgar for next 10)                        │
│  - Each row shows: contributor, contribution, rubric, provisioned   │
│  - Governor/Sentinel sees Approve button + TDG adjust field         │
│  - On Approve: browser signs CONTRIBUTION REVIEW EVENT → Edgar      │
│  - Non-governors see the queue but no action buttons                │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (Edgar webhook on approval)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GAS WRITE-BACK SCRIPT                                              │
│                                                                     │
│  process_review_approval.gs                                         │
│  - Receives webhook from Edgar with hash_key + approved TDG         │
│  - Opens Scored Chatlogs sheet                                      │
│  - Finds row by hash_key (Column K)                                 │
│  - Checks: if Status is already "Reviewed" or "Transferred...", SKIP│
│  - Sets Status = "Reviewed", TDGs Issued = approved amount          │
│  - Logs reviewer email from the event                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow (Step by Step)

### 4.1 Cache Generation (GitHub Action)

1. **Trigger:** GitHub Actions scheduled cron (every 5 minutes, or on-demand via workflow_dispatch)
2. **Read:** Google Sheets API → `Scored Chatlogs` tab, columns A–N
3. **Filter:** Rows where `Column F (Status) = "Pending Review"` AND `Column N (Cache Generated)` is empty
4. **For each matching row:**
   - Read `Column K (Scoring Hash Key)` → this is the filename
   - Build JSON object with fields: `hash_key`, `contributor`, `project`, `contribution`, `rubric`, `tdgs_provisioned`, `status_date`, `reporter`, `generated_at`
   - Write to `treasury-cache/review-queue/<hash_key>.json`
5. **After all files written:**
   - Git commit + push to `main`
   - For each processed row, write current timestamp to `Column N` (via Sheets API batch update)
6. **Idempotency:** If a file already exists in the repo, skip it (don't overwrite). If `Column N` already has a timestamp, skip the row.

### 4.2 Queue Serving (Edgar)

1. **Endpoint:** `GET /dao/review_queue?limit=10&offset=0`
2. **Read:** GitHub API → list `treasury-cache/review-queue/` directory, sorted by filename (oldest first)
3. **Paginate:** Return `limit` files starting at `offset`. Include `total_count` for the DApp to know how many pages exist.
4. **Read each file's content** and return as JSON array:
   ```json
   {
     "items": [
       {
         "hash_key": "XzQ2EhAMD7MN8X0zFhvw",
         "contributor": "gotothe_peak",
         "contribution": "Who's looking for...",
         "rubric": "100TDG For every 1 hour of human effort",
         "tdgs_provisioned": 8.33,
         "status_date": "20241214",
         "reporter": "gotothe_peak",
         "generated_at": "2026-06-18T12:00:00Z"
       }
     ],
     "total_count": 42,
     "offset": 0,
     "limit": 10
   }
   ```
5. **Auth:** Anyone can call this endpoint (read-only). No signature required.

### 4.3 Approval (DApp → Edgar)

1. **DApp page** loads the queue from Edgar, renders each row
2. **Governor/Sentinel** sees an Approve button + a TDG amount field (pre-filled with Grok's provisioned value)
3. **On click:**
   - Browser builds `[CONTRIBUTION REVIEW EVENT]` payload:
     ```
     [CONTRIBUTION REVIEW EVENT]
     - Scoring Hash Key: XzQ2EhAMD7MN8X0zFhvw
     - TDGs Issued: 8.33
     - Reviewer Email: garyjob@agroverse.shop
     - Status: Reviewed
     ```
   - Browser signs with RSA private key (same as existing DApp keypair)
   - Submits to `POST /dao/submit_contribution`
4. **Edgar receives and validates:**
   - Verifies RSA signature
   - Looks up signer's email in `Contributors Digital Signatures`
   - Checks if signer is a governor (in `Governors` tab) OR Sentinel (`Is Sentinel = TRUE`)
   - If not authorized → return 403
   - If authorized:
     a. Logs the event to Telegram Chat Logs (same as other events)
     b. Deletes `treasury-cache/review-queue/<hash_key>.json` via GitHub API
     c. Fires webhook to GAS write-back script
     d. Returns success

### 4.4 Write-Back (GAS webhook)

1. **Trigger:** Edgar sends POST to GAS web app URL with payload:
   ```json
   {
     "action": "process_review_approval",
     "hash_key": "XzQ2EhAMD7MN8X0zFhvw",
     "tdgs_issued": 8.33,
     "reviewer_email": "garyjob@agroverse.shop"
   }
   ```
2. **GAS script:**
   - Opens `Scored Chatlogs` sheet
   - Finds row by `Column K = hash_key`
   - **Double-counting guard:** Checks if `Column F (Status)` is already `"Reviewed"` or `"Transferred to Main Ledger"` or `"Successfully Completed / Full Provision Awarded"` → if so, SKIP (return 200 with `"already_processed"`)
   - Sets `Column F = "Reviewed"`
   - Sets `Column G (TDGs Issued)` = approved amount
   - Optionally sets `Column M (Reviewer Email)` = reviewer_email
   - Returns 200

---

## 5. Event Schema

### CONTRIBUTION REVIEW EVENT

| Field | Required | Description |
|-------|----------|-------------|
| `Scoring Hash Key` | Yes | The hash key from Scored Chatlogs Column K |
| `TDGs Issued` | Yes | Final TDG amount awarded (number) |
| `Reviewer Email` | Yes | Email of the governor/Sentinel who approved |
| `Status` | Yes | Always `"Reviewed"` |

---

## 6. Cache File Schema

Each file in `treasury-cache/review-queue/<hash_key>.json`:

```json
{
  "hash_key": "XzQ2EhAMD7MN8X0zFhvw",
  "contributor": "gotothe_peak",
  "project": "telegram_chatlog",
  "contribution": "Who's looking for a dev for your DeFi or Tg miniapp project?",
  "rubric": "100TDG For every 1 hour of human effort",
  "tdgs_provisioned": 8.33,
  "status_date": "20241214",
  "reporter": "gotothe_peak",
  "generated_at": "2026-06-18T12:00:00Z"
}
```

---

## 7. Scored Chatlogs Column Reference

| Col | Header | Role |
|-----|--------|------|
| A | Contributor Name | Contributor display name |
| B | Project Name | Source platform (e.g. `telegram_chatlog`) |
| C | Contribution Made | The contribution text |
| D | Rubric classification | Grok's classification |
| E | TDGs Provisioned | Grok's suggested TDG amount |
| F | Status | `"Pending Review"` → `"Reviewed"` → `"Transferred to Main Ledger"` |
| G | TDGs Issued | Final awarded TDG (set by governor) |
| H | Status date | Date of the original contribution |
| I | Existing Contributor | Whether contributor exists in ledger |
| J | Reporter Name | Who reported the contribution |
| K | Scoring Hash Key | Unique hash for deduplication |
| L | Main Ledger Row Number | Row in Ledger history after transfer |
| M | Reviewer Email | (NEW) Email of the approving governor |
| N | Cache Generated | (NEW) Timestamp when cache file was created |

---

## 8. PR Breakdown (Sequenced)

Each PR is standalone, small, and independently reviewable. Do NOT chain multiple PRs in one turn.

### PR 1: GitHub Action — Cache Generator

**Repo:** `treasury-cache` (API-only DATA repo — single-file write via `upload_file_to_github`)

**Scope:**
- Create `.github/workflows/generate_review_cache.yml` — scheduled cron (every 5 min) + `workflow_dispatch`
- Create `scripts/generate_review_cache.py` — Python script that:
  - Reads Scored Chatlogs via Google Sheets API (service account from GitHub Secrets)
  - Filters for `Status = "Pending Review"` AND `Column N` empty
  - Generates JSON files in `review-queue/<hash_key>.json`
  - Writes timestamp to Column N via Sheets API batch update
  - Commits + pushes new files to `main`
- Add `google_credentials.json` to GitHub Secrets (or use existing SA)
- Add `requirements.txt` with `google-auth`, `google-api-python-client`, `pygithub`

**Files created:**
- `.github/workflows/generate_review_cache.yml`
- `scripts/generate_review_cache.py`
- `scripts/requirements.txt`

**Acceptance:**
- Manual `workflow_dispatch` run creates JSON files in `review-queue/`
- Column N populated with timestamps for processed rows
- Re-run skips already-cached rows

---

### PR 2: Edgar — Review Queue Endpoint

**Repo:** `sentiment_importer` (Rails) or `dao_protocol` (Python FastAPI)

**Scope:**
- Add `GET /dao/review_queue` endpoint
- Reads `treasury-cache/review-queue/` directory via GitHub API
- Returns paginated results (limit, offset, total_count)
- Reads each JSON file's content and returns as array

**Files created/modified:**
- `app/controllers/dao_controller.rb` (Rails) or `app/routes/review_queue.py` (FastAPI)
- Tests for pagination, empty queue, file-not-found

**Acceptance:**
- `GET /dao/review_queue?limit=10&offset=0` returns 10 items + total_count
- `GET /dao/review_queue?limit=10&offset=100` returns next page
- Returns empty array when queue is empty

---

### PR 3: Edgar — CONTRIBUTION REVIEW EVENT Handler + Cache File Deletion

**Repo:** `sentiment_importer` or `dao_protocol`

**Scope:**
- Register `[CONTRIBUTION REVIEW EVENT]` in Edgar's event catalog
- On receipt:
  1. Verify signer is governor or Sentinel (reuse existing check from `dao_controller.rb`)
  2. Delete `treasury-cache/review-queue/<hash_key>.json` via GitHub API
  3. Fire webhook to GAS write-back URL
  4. Log to Telegram Chat Logs
- Return 403 for non-governor/non-Sentinel signers

**Files created/modified:**
- Event handler in `app/services/` or `app/controllers/dao_controller.rb`
- GitHub API client for file deletion
- Webhook dispatch to GAS URL

**Acceptance:**
- Governor's signed event deletes cache file + fires webhook
- Non-governor's signed event returns 403
- Missing hash_key returns 400

---

### PR 4: GAS Write-Back Script

**Repo:** `tokenomics` (GAS script)

**Scope:**
- Create new GAS project (or add to existing scoring script) with web-app endpoint
- `doPost(e)` handler:
  - Parses JSON payload: `hash_key`, `tdgs_issued`, `reviewer_email`
  - Opens Scored Chatlogs sheet
  - Finds row by Column K
  - **Double-counting guard:** Skip if Status is already Reviewed/Transferred/Completed
  - Sets Status = "Reviewed", TDGs Issued = approved amount, Reviewer Email
  - Returns JSON `{"status": "ok"}` or `{"status": "already_processed"}`
- Deploy as web app ("Anyone" access for Edgar to POST)

**Files created/modified:**
- `google_app_scripts/<scriptId>/process_review_approval.gs`
- `google_app_scripts/<scriptId>/Code.js` (if needed for doPost routing)
- Update `SCHEDULE_TRIGGERS.md` if needed

**Acceptance:**
- POST with valid hash_key updates the row
- POST with already-reviewed hash_key returns `already_processed`
- POST with invalid hash_key returns 404

---

### PR 5: DApp — Review Queue Page

**Repo:** `dapp_beta`

**Scope:**
- Create `review_queue.html` (new page)
- Fetches queue from `GET /dao/review_queue` with infinite scroll
- Renders table: contributor, contribution (truncated), rubric, provisioned TDG, date
- For governors/Sentinels (checked via Edgar identity lookup):
  - Approve button (accepts Grok's provisioned amount)
  - TDG adjust field (override the amount)
  - On click: builds `[CONTRIBUTION REVIEW EVENT]`, signs with RSA keypair, submits to Edgar
- For non-governors: read-only view of the queue
- Loading states, error states, empty queue message
- Link from DApp navigation

**Files created/modified:**
- `review_queue.html`
- `scripts/edgar_payload_helper.js` (may need update for new event type)
- Navigation menu update

**Acceptance:**
- Anyone can view the queue with infinite scroll
- Governor sees Approve button + TDG adjust field
- Non-governor sees read-only queue
- Successful approval removes item from queue (after refresh)
- Error states handled gracefully

---

### PR 6: Beta Deploy + UAT

**Scope:**
- Deploy PR 5 to `dapp_beta` (GitHub Pages)
- Deploy PR 4 GAS script (clasp push + deploy)
- Verify end-to-end:
  - U1: Cache generator creates files for pending rows
  - U2: Edgar serves queue with pagination
  - U3: Governor approves a row → cache file deleted → sheet updated
  - U4: Non-governor sees queue but cannot approve
  - U5: Double-counting guard prevents re-approval
  - U6: Infinite scroll loads more items
- Fix any issues found

**Acceptance:**
- All UAT tests pass
- Governor signs off

---

### PR 7: Promote to Production

**Scope:**
- Sync `dapp_prod` from `dapp_beta`
- Deploy GAS script to production deployment
- Enable GitHub Action cron (set to 5-minute schedule)
- Update `OPEN_FOLLOWUPS.md` with any known gaps

**Acceptance:**
- Live on production
- Governor can review and approve from the DApp

---

## 9. Double-Counting Guard (Critical)

**Problem:** If the GAS write-back script runs after the row is already "Transferred to Main Ledger", it could set Status back to "Reviewed", causing the transfer script to re-process it and award TDGs twice.

**Solution (three layers):**

1. **Cache file deletion:** Once a cache file is deleted from `treasury-cache/review-queue/`, the DApp can no longer surface it. The GitHub Action won't re-generate it because Column N is already populated.

2. **GAS write-back guard:** Before writing, check `Column F (Status)`. If it's already `"Reviewed"`, `"Transferred to Main Ledger"`, `"Successfully Completed / Full Provision Awarded"`, or `"Ignored"` → skip. Return `"already_processed"`.

3. **Transfer script guard:** The existing `transfer_scored_contributions_to_main_ledger.js` already checks for `"Transferred to Main Ledger"` status and skips those rows. It also checks for existing records in Ledger history by matching contributor + contribution + TDG + date.

---

## 10. Authorization Model

| Action | Who can do it | How enforced |
|--------|---------------|-------------|
| View the queue | Anyone (no auth) | No check needed — read-only data |
| Approve a review | Governor or Sentinel | Edgar verifies RSA signature → checks `Governors` tab + `Is Sentinel` column |
| Generate cache files | GitHub Action (service account) | GitHub Secrets + Google Sheets API scope |
| Write back to sheet | GAS web app (called by Edgar) | Edgar authenticates via shared secret or IP allowlist |

---

## 11. Edge Cases

| Case | Handling |
|------|----------|
| Grok scores a row as "Unknown" | Status is still "Pending Review" with TDGs Provisioned = 0. Governor can review and set to 0 or ignore. |
| Cache file exists but row is already reviewed | GitHub Action skips because Column N is populated. If manually deleted, next run re-generates. |
| Edgar goes down | DApp shows error state. Cache files remain in repo — no data loss. |
| GAS write-back fails | Edgar logs the failure. Cache file is already deleted (approval already processed). Manual retry via admin endpoint. |
| Governor approves with 0 TDG | Valid — some contributions may be worth 0. Row becomes "Reviewed" with 0. Transfer script will mark as "Ignored". |
| Two governors approve the same row simultaneously | First one deletes the cache file. Second one gets 404 from Edgar (file not found) → DApp shows "already approved". |
| GitHub Action timeout (6 hours) | Unlikely for this workload. Each run processes at most a few hundred rows. |

---

## 12. Files to Create / Modify Summary

| PR | Repo | Files | Type |
|----|------|-------|------|
| 1 | `treasury-cache` | `.github/workflows/generate_review_cache.yml`, `scripts/generate_review_cache.py`, `scripts/requirements.txt` | New |
| 2 | `sentiment_importer` or `dao_protocol` | Review queue controller/route + tests | New |
| 3 | `sentiment_importer` or `dao_protocol` | Event handler + GitHub API client + webhook dispatch | New/Modify |
| 4 | `tokenomics` | `google_app_scripts/<id>/process_review_approval.gs` | New |
| 5 | `dapp_beta` | `review_queue.html`, `scripts/edgar_payload_helper.js` (maybe) | New/Modify |
| 6 | — | UAT testing (no code changes) | — |
| 7 | `dapp_prod` | Sync from beta | Sync |

---

## 13. RESUME HERE

**Next action:** PR 1 — GitHub Action cache generator for `treasury-cache`.

**Gate:** Governor says "go for it" or "proceed" in this thread.

**One PR per turn rule:** On GO, execute PR 1 ONLY, then stop and report the PR URL. Do NOT chain PRs.
