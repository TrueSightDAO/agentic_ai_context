# Scoring Review Queue — Implementation Plan

**Status:** In progress · **Created:** 2026-06-18
**Last updated:** 2026-06-22 (v17: UAT attempt found a **page↔Edgar integration gap** — `review_queue.html` calls `/api/v1/...` + `/dao/verify_identity` + `/dao/contributors` that 404 on Edgar; `verify_identity` 404 means no Approve buttons render. **RESUME HERE = PR-INTEGRATION** (close the gap), then PR7. See §12.3)
**Last updated:** 2026-06-22 (v16: PR4 DEPLOYED + WIRED — Edgar webhook env set + service restarted; automated write-back path live end-to-end)
**Last updated:** 2026-06-22 (v15: PR4 DEPLOYED — `clasp push` 1BHAGZd + anonymous versioned deployment `@2`; `?exec=processApprovalRejections` verified live)
**Last updated:** 2026-06-22 (v14: PR4 code merged + made deployable — handler #367, dup-`doGet` deploy-blocker fixed #368)
**Last updated:** 2026-06-21 (v13: code-verified state — PR4 GAS write-back was NOT deployed; corrected the manifest's "PR7 done" claim; added §12 resume tracker with `Advance` column)
**Handoff thread:** [Telegram topic 7191](https://t.me/c/3919341801/7191)

> ⚠️ **2026-06-21 verification (Claude):** A live probe + source/git audit found the review
> loop **broken at the write-back step** — **PR4 (`processApprovalRejections` in the `1BHAGZd`
> Grok project) is not deployed.** The earlier *"PR7 done — UAT passed end-to-end"* status was
> **not credible**: without PR4 nothing writes a governor's approval back into Scored Chatlogs
> as `Reviewed`, so the transfer batch never sees it and nothing reaches Ledger history.
> **The next execution turn is PR4, not PR8.** Full evidence + resume tracker in **§12**.

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

1. **GitHub Actions cache generator** (Python, scheduled cron) reads Scored Chatlogs, finds rows with `Status = "Pending Review"` AND `Column N` empty, generates one JSON cache file per row in `treasury-cache/review-queue/`, and marks a `Cache Generated` column on the sheet.
2. **DApp review page** (new HTML page) reads the cache files via Edgar, surfaces the oldest 10 with infinite scroll. Anyone can view the queue.
3. **Governor/Sentinel** sees a three-action panel per row: **Approve** (accepts Grok's provisioned TDG or an adjusted amount), **Skip** (leaves for later), or **Reject** (with required reason).
4. **Contributor resolution** — The cache includes the `found_in_contributors` flag (Column I). If TRUE, the contributor dropdown is pre-selected. If FALSE or "RESOLVE FAILED", the governor must pick the right contributor from a dropdown before approving.
5. **On Approve/Reject**, the browser signs a `[CONTRIBUTION REVIEW EVENT]` to Edgar. The event payload is minimal — only the hash key, action, and TDG amount/rejection reason. **No reviewer email** — Edgar resolves the reviewer's identity from the RSA signature.
6. **Edgar verifies** the signer is a governor or Sentinel (via RSA signature → `Contributors Digital Signatures` sheet). On success, Edgar resolves the reviewer's email and appends the approved event to the **Telegram Chat Logs** sheet (same sheet where `[CONTRIBUTION EVENT]` records land). Edgar includes its internal **transaction ID** in the appended record so the GAS script can track which events it has processed.
7. **Edgar then calls** `GET <GAS_webhook_url>?exec=processApprovalRejections` — this triggers the GAS script to scan Telegram Chat Logs for unprocessed `[CONTRIBUTION REVIEW EVENT]` records and process them in batch.
8. **The GAS script** checks a new **"Review Processed"** column (boolean) on the Telegram Chat Logs sheet. It only processes rows where this column is empty/FALSE. After successfully updating Scored Chatlogs, it sets this column to TRUE and records the Edgar transaction ID in a **"Review Transaction ID"** column. This prevents re-processing the same event on subsequent calls.
9. **On approval**, Edgar deletes the cache file from `treasury-cache/review-queue/`.
10. **On rejection**, Edgar deletes the cache file.
11. **On Skip**, the cache file stays — it will be re-surfaced on the next page load.

---

## 3. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GOOGLE SHEETS                                │
│                                                                     │
│  ┌─────────────────────────────────────────┐                       │
│  │ Telegram Chat Logs (1qbZZ…)             │                       │
│  │                                         │                       │
│  │ Contains BOTH:                          │                       │
│  │  - [CONTRIBUTION EVENT] records         │                       │
│  │  - [CONTRIBUTION REVIEW EVENT] records  │                       │
│  │    (NEW — appended by Edgar)            │                       │
│  │                                         │                       │
│  │ NEW Columns:                            │                       │
│  │  - Col X: "Review Processed" (boolean)  │                       │
│  │  - Col Y: "Review Transaction ID" (str) │                       │
│  └──────────────────┬──────────────────────┘                       │
│                     │                                              │
│                     │ Grok scoring reads [CONTRIBUTION EVENT]      │
│                     │ GAS processApprovalRejections reads          │
│                     │   [CONTRIBUTION REVIEW EVENT] where          │
│                     │   "Review Processed" is empty/FALSE          │
│                     ▼                                              │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ Grok Scoring GAS Project (1BHAGZd…)                     │       │
│  │                                                         │       │
│  │ Existing: Code.js (Grok scoring + write to Scored       │       │
│  │   Chatlogs)                                             │       │
│  │ Existing: telegram_webhook_listener.js (doPost for      │       │
│  │   Telegram webhooks + orchestrator calls)               │       │
│  │ NEW: telegram_webhook_listener.js — add doGet(e) that   │       │
│  │   accepts ?exec=processApprovalRejections, scans        │       │
│  │   Telegram Chat Logs for unprocessed review events      │       │
│  │   (where "Review Processed" is empty/FALSE), updates    │       │
│  │   Scored Chatlogs, marks "Review Processed" = TRUE      │       │
│  │ Existing doPost stays untouched for Telegram webhooks   │       │
│  └─────────────────────────────────────────────────────────┘       │
│         │                                                          │
│         │ (writes scored results)                                  │
│         ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ Scored Chatlogs (1Tbj7H5ur…)                            │       │
│  │                                                         │       │
│  │  Col F = Status (see §7)                                │       │
│  │  Col K = Scoring Hash Key                               │       │
│  │  Col M = Reviewer Email (NEW)                           │       │
│  │  Col N = Cache Generated (NEW)                          │       │
│  │  Col O = Rejection Reason (NEW)                         │       │
│  └─────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (reads via Google Sheets API)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GITHUB ACTIONS (scheduled cron)                                    │
│                                                                     │
│  .github/workflows/generate_review_cache.yml                        │
│  scripts/generate_review_cache.py                                   │
│  - Reads Scored Chatlogs via Google Sheets API                      │
│  - Finds rows with Status = "Pending Review" AND Col N empty                    │
│                                                                                             │
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
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (reads directory listing + individual files)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  EDGAR (dao_protocol)                                               │
│                                                                     │
│  GET /dao/review_queue?limit=10&after_filename=XzQ2EhAMD7MN8X0zFhvw│
│  - Lists treasury-cache/review-queue/ directory (sorted by name)    │
│  - If after_filename is NOT provided: return the first `limit` files│
│  - If after_filename IS provided but file was deleted: skip to next │
│  - Returns next `limit` files + their JSON content                  │
│  - Includes `next_filename` (cursor) and `has_more` (boolean)       │
│                                                                     │
│  POST /dao/submit_contribution  (CONTRIBUTION REVIEW EVENT)         │
│  - Verifies signer is governor or Sentinel (via RSA signature)      │
│  - Resolves reviewer email from the RSA signature                   │
│  - Appends the approved event to Telegram Chat Logs sheet           │
│    INCLUDING Edgar's internal transaction ID                        │
│  - Deletes the cache file from treasury-cache/review-queue/         │
│  - Calls GAS via doGet:                                             │
│    GET <webhook_url>?exec=processApprovalRejections                 │
└─────────────────────────────────────────────────────────────────────┘
         │                    ▲
         │ (serves queue)     │ (signed event — minimal payload)
         ▼                    │
┌─────────────────────────────────────────────────────────────────────┐
│  DAPP (dapp_beta / dapp_prod)                                       │
│                                                                     │
│  review_queue.html (new page)                                       │
│  - Anyone can view the queue (read-only)                            │
│  - Infinite scroll using cursor-based pagination                     │
│  - Contributor resolution badge: ✓ Resolved / ⚠ Resolve Failed     │
│  - Three-action panel per row:                                      │
│    ✓ Approve (with optional TDG override field)                     │
│    → Skip (leaves cache file, re-surfaces later)                    │
│    ✕ Reject (requires reason text field)                            │
│  - On Approve: signs [CONTRIBUTION REVIEW EVENT] with Action=Approve│
│  - On Reject: signs [CONTRIBUTION REVIEW EVENT] with Action=Reject  │
│  - On Skip: no event, just advances to next row                     │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (Edgar calls GAS via doGet with exec=processApprovalRejections)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GAS WRITE-BACK (in Grok Scoring GAS Project — 1BHAGZd…)           │
│                                                                     │
│  NEW: telegram_webhook_listener.js — function doGet(e)              │
│                                                                     │
│  - Reads query parameter: exec                                      │
│  - If exec === "processApprovalRejections":                         │
│    1. Reads Telegram Chat Logs sheet for rows containing            │
│       "[CONTRIBUTION REVIEW EVENT]"                                  │
│    2. Filters to only rows where "Review Processed" column         │
│       (Col X) is empty or FALSE — skips already-processed rows     │
│    3. Parses each unprocessed event: action, scoringHashKey,        │
│       tdgIssued, rejectionReason, reviewerEmail, transactionId      │
│    4. For each event, looks up the row in Scored Chatlogs by        │
│       scoringHashKey (Col K)                                        │
│    5. Double-counting guard: checks if Status is already            │
│       "Reviewed" / "Transferred" / "Rejected" / "Ignored"         │
│    6. On Approve: sets Col F = "Reviewed", Col G = tdgIssued,      │
│       Col M = reviewerEmail                                         │
│    7. On Reject: sets Col F = "Rejected", Col O = rejectionReason, │
│       Col M = reviewerEmail                                         │
│    8. After successful update: sets Col X = TRUE,                   │
│       Col Y = transactionId (from the event)                        │
│  - Returns JSON: { status: "ok", processed: N, errors: M }         │
│                                                                     │
│  Existing doPost(e) stays untouched — still handles Telegram        │
│  webhooks and orchestrator calls                                    │
│                                                                     │
│  Deployment: clasp push from tokenomics/google_app_scripts/         │
│  1BHAGZd…/ (same project as Grok scoring)                           │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (scheduled trigger picks up "Reviewed" rows)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TRANSFER SCRIPT (separate GAS project — 1-ts0WTM8…)               │
│                                                                     │
│  transfer_scored_contributions_to_main_ledger.js                    │
│  - Runs on scheduled trigger (unchanged)                            │
│  - Reads Scored Chatlogs for Status = "Reviewed" or                │
│    "Pending Review"                                           │
│  - Transfers to Ledger history in main ledger                       │
│  - Sets Status = "Transferred to Main Ledger"                       │
│  - No changes needed                                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Schema

### 4.1 Telegram Chat Logs Sheet (Google Sheets — 1qbZZ…)

| Col | Label | Type | Description |
|-----|-------|------|-------------|
| ... | (existing columns) | | |
| X | Review Processed | boolean | **NEW** — TRUE after GAS has processed this review event |
| Y | Review Transaction ID | string | **NEW** — Edgar's internal transaction ID for this review event |

### 4.2 Scored Chatlogs Sheet (Google Sheets — 1Tbj7H5ur…)

| Col | Label | Type | Description |
|-----|-------|------|-------------|
| A | Contributor Name | string | Name of the contributor |
| B | Contribution Description | string | What was done |
| C | Rubric | string | Scoring rubric category |
| D | Contribution Type | string | Time (Minutes) / USD / etc. |
| E | TDGs Provisioned | decimal | Grok's AI-provisioned TDG amount |
| F | Status | string | Current state (see §7) |
| G | TDGs Issued | decimal | Final TDG amount (set by governor) |
| H | Contribution Date | date | When the work was done |
| I | Found in Contributors | string | TRUE / FALSE / RESOLVE FAILED |
| J | Contributor Email | string | Email from contributor lookup |
| K | Scoring Hash Key | string | Unique hash identifying this row |
| L | (reserved) | | |
| M | Reviewer Email | string | **NEW** — Email of the approving governor |
| N | Cache Generated | timestamp | **NEW** — Set by cache generator when JSON is pushed |
| O | Rejection Reason | string | **NEW** — Reason if Status = Rejected |

### 4.3 Cache File Schema (treasury-cache/review-queue/<hash_key>.json)

```json
{
  "scoringHashKey": "XzQ2EhAMD7MN8X0zFhvw",
  "contributorName": "Alice",
  "contributionDescription": "Ledger reconciliation for Q1",
  "rubric": "Operations",
  "contributionType": "Time (Minutes)",
  "tdgsProvisioned": "45.00",
  "tdgsIssued": "0.00",
  "contributionDate": "2026-06-15",
  "foundInContributors": true,
  "contributorEmail": "alice@example.com",
  "scoredChatlogsRow": 142
}
```

### 4.4 CONTRIBUTION REVIEW EVENT Payload

**Approve:**
```
[CONTRIBUTION REVIEW EVENT]
- Action: Approve
- Scoring Hash Key: XzQ2EhAMD7MN8X0zFhvw
- TDGs Issued: 45.00
- Contributor Name: Alice
--------
```

**Reject:**
```
[CONTRIBUTION REVIEW EVENT]
- Action: Reject
- Scoring Hash Key: XzQ2EhAMD7MN8X0zFhvw
- Rejection Reason: Duplicate entry — already recorded in Q1 batch
--------
```

**Note:** `Reviewer Email` is NOT in the signed payload. Edgar resolves it server-side from the RSA signature and appends it to the Telegram Chat Logs record along with Edgar's transaction ID.

### 4.5 Edgar → GAS Callback (doGet with exec parameter)

```
GET <webhook_url>?exec=processApprovalRejections
```

No per-action parameters. Edgar just triggers the GAS script, which scans Telegram Chat Logs for unprocessed `[CONTRIBUTION REVIEW EVENT]` records (where "Review Processed" is empty/FALSE) and processes them in batch.

---

## 5. PR Breakdown

### PR 1 — GitHub Actions Cache Generator

**Repo:** `treasury-cache` (or `dao_protocol` if scripts live there)
**Files:**
- `.github/workflows/generate_review_cache.yml` — scheduled cron (every 5 min)
- `scripts/generate_review_cache.py` — Python script

**What it does:**
- Reads Scored Chatlogs via Google Sheets API (service account: `tdg_scoring`)
- Finds rows where `Status = "Pending Review"` AND `Column N` is empty
- For each row, generates a JSON file at `review-queue/<hash_key>.json`
- Pushes all new files to `treasury-cache` repo in one commit
- Writes timestamp to Column N (`Cache Generated`) via Sheets API

**Edge cases:**
- If the sheet is unreachable (API error), the Action fails with a clear error message
- If a row's hash key already exists as a cache file (from a previous run), skip it
- If the Sheets API returns partial data (rate limited), retry with exponential backoff
- If the push to GitHub fails, don't mark Column N (so next run retries)

**Testing:**
- Dry-run mode: `--dry-run` flag that prints what it would do without writing
- Unit tests for the row-filtering logic (mock Sheets API)

---

### PR 2 — Edgar GET /dao/review_queue Endpoint

**Repo:** `dao_protocol` (Python/FastAPI)
**Files:**
- `app/routers/review_queue.py` — new router

**What it does:**
- `GET /dao/review_queue?limit=10&after_filename=XzQ2EhAMD7MN8X0zFhvw`
- Lists `treasury-cache/review-queue/` directory via GitHub Contents API
- Sorts files alphabetically (by filename = hash key = chronological order)
- **Boundary condition — no cursor (first load):** If `after_filename` is NOT provided, return the first `limit` files from the directory (earliest = first alphabetically). This is the initial page load.
- **Boundary condition — cursor file deleted:** If `after_filename` IS provided but the file no longer exists (already approved/deleted by another governor), skip to the next available file after where it would have been. Do NOT fail, do NOT return empty — just advance the cursor.
- Returns next `limit` files with their JSON content
- Response includes `next_filename` (for cursor) and `has_more` (boolean)

**Edge cases:**
- Empty directory → returns `{ items: [], has_more: false }`
- `after_filename` not found (deleted) → starts from the next available file
- GitHub API rate limit → cache the directory listing for 30 seconds

---

### PR 3 — Edgar CONTRIBUTION REVIEW EVENT Handler

**Repo:** `dao_protocol` (Python/FastAPI)
**Files:**
- `app/event_handlers/contribution_review.py` — new handler

**What it does:**
- Handles `[CONTRIBUTION REVIEW EVENT]` submissions
- Verifies the signer is a governor or Sentinel (lookup in `Contributors Digital Signatures` sheet or Edgar's identity registry)
- Resolves the reviewer's email from the RSA signature
- Appends the approved/rejected event to the **Telegram Chat Logs** sheet, INCLUDING:
  - The full event text (same format as the signed payload)
  - `Reviewer Email` (resolved from RSA signature)
  - Edgar's internal **transaction ID** (for tracking in the GAS script)
- Deletes the cache file from `treasury-cache/review-queue/<hash_key>.json`
- Calls GAS via doGet: `GET <webhook_url>?exec=processApprovalRejections`

**Authorization:**
- Non-governor/non-Sentinel signatures → HTTP 403
- Missing `Action` field → HTTP 400
- Approve without `TDGs Issued` → HTTP 400
- Reject without `Rejection Reason` → HTTP 400

**GAS callback retry:**
- If GAS doGet returns non-200, retry up to 3 times with exponential backoff
- After 3 failures, log the error (the event is still in Telegram Chat Logs with "Review Processed" = FALSE, so it will be picked up on the next successful trigger)

---

### PR 4 — Add doGet to Grok Scoring GAS Project for Review Processing

**GAS Project:** `1BHAGZd…` (same project as Grok scoring script)
**Repo:** `tokenomics` → `google_app_scripts/1BHAGZd…/`
**Files:**
- `telegram_webhook_listener.js` — **add** new `doGet(e)` function

**Why doGet instead of doPost:** Edgar calls the GAS web app via a simple GET request with a single query parameter (`exec=processApprovalRejections`). This avoids CORS issues, content-type restrictions, and the complexity of POST webhook handling. The existing `doPost(e)` stays untouched — it still handles Telegram webhooks and orchestrator calls.

> ⚠️ **PR4 implementation caveats (verified 2026-06-21):**
> 1. **The `1BHAGZd` project ALREADY defines a `doGet(e)`** (it reads `e.parameter.action`
>    and handles `action === 'processTelegramChatLogs'`). GAS does **not** allow two
>    functions of the same name in one project — **do NOT add a second `doGet`.** Instead
>    **merge** an `exec` branch into the existing `doGet` (keep the `action` branch intact),
>    e.g. `const exec = e.parameter.exec; if (exec === 'processApprovalRejections') return processApprovalRejections();`
>    placed alongside the existing `action` check.
> 2. **Duplicate-file hazard:** `doGet` currently appears **identically in both `Code.js` and
>    `grok_scoring_for_telegram_and_whatsapp_logs.js`** (byte-identical 70997-byte files,
>    same `doGet` at line 279). Two definitions in one clasp project collide — **reconcile to a
>    single source file before `clasp push`** (delete/rename the orphan; confirm which file the
>    deployment actually loads).
> 3. **Edgar trigger is NOT wired:** `gas_review_webhook_url` defaults to `""`
>    (`dao_protocol/.../server/config.py:115`); `dao.py:203` then falls back to *"GAS cron will
>    process"* — but **no such cron is deployed.** PR4 must therefore ALSO add a **time-based
>    trigger** on `processApprovalRejections` (safety net) **and** the operator must set
>    `DAO_PROTOCOL_GAS_REVIEW_WEBHOOK_URL` on the Edgar box to the `1BHAGZd` `/exec` URL for
>    immediate processing. Without one of these, approvals sit unprocessed in Telegram Chat Logs.

**NEW — `doGet(e)` — merge a Review-processing branch into the EXISTING `doGet` (illustrative; do not duplicate the function):**
```javascript
// EXISTING doGet already handles e.parameter.action — ADD this branch, don't redefine doGet:
function doGet(e) {
  try {
    const action = e.parameter && e.parameter.action;
    const exec = e.parameter && e.parameter.exec;

    if (action === 'processTelegramChatLogs') {   // existing behavior — keep
      processTelegramChatLogs();
      return ContentService.createTextOutput("✅ Telegram logs processed");
    }
    if (exec === 'processApprovalRejections') {    // NEW — review write-back
      return processApprovalRejections();
    }

    return ContentService.createTextOutput("ℹ️ No valid action specified");
  } catch (err) {
    Logger.log('doGet error: ' + err.message);
    return createJsonResponse({ status: 'error', reason: err.message }, 500);
  }
}

function processApprovalRejections() {
  // 1. Read Telegram Chat Logs sheet
  const chatLogs = getTelegramChatLogs();

  // 2. Find rows containing [CONTRIBUTION REVIEW EVENT] that haven't been processed
  //    Check "Review Processed" column (Col X) — only process if empty or FALSE
  const unprocessed = chatLogs.filter(row =>
    row.text && row.text.includes('[CONTRIBUTION REVIEW EVENT]') &&
    !row.reviewProcessed  // Col X — empty or FALSE
  );

  let processed = 0;
  let errors = 0;

  // 3. Process each event
  for (const event of unprocessed) {
    try {
      const parsed = parseReviewEvent(event.text);
      const result = applyReviewToScoredChatlogs(parsed);

      if (result.status === 'updated' || result.status === 'skipped') {
        // Mark as processed: set Col X = TRUE, Col Y = transactionId
        markEventAsProcessed(event.rowNumber, parsed.transactionId);
        processed++;
      } else {
        errors++;
      }
    } catch (err) {
      Logger.log('Error processing event at row ' + event.rowNumber + ': ' + err.message);
      errors++;
    }
  }

  return createJsonResponse({
    status: 'ok',
    processed: processed,
    errors: errors
  });
}

function parseReviewEvent(text) {
  // Parse the [CONTRIBUTION REVIEW EVENT] text format
  const lines = text.split('\n');
  const result = {};
  for (const line of lines) {
    if (line.startsWith('- Action:')) result.action = line.split(':')[1].trim();
    if (line.startsWith('- Scoring Hash Key:')) result.scoringHashKey = line.split(':')[1].trim();
    if (line.startsWith('- TDGs Issued:')) result.tdgIssued = line.split(':')[1].trim();
    if (line.startsWith('- Rejection Reason:')) result.rejectionReason = line.split(':')[1].trim();
    if (line.startsWith('- Reviewer Email:')) result.reviewerEmail = line.split(':')[1].trim();
    if (line.startsWith('- Transaction ID:')) result.transactionId = line.split(':')[1].trim();
  }
  return result;
}

function applyReviewToScoredChatlogs(parsed) {
  const row = findRowByHashKey(parsed.scoringHashKey);
  if (!row) {
    return { status: 'error', reason: 'Row not found' };
  }

  const currentStatus = row[5]; // Col F

  // Double-counting guard
  if (currentStatus === 'Reviewed' ||
      currentStatus === 'Transferred to Main Ledger' ||
      currentStatus === 'Rejected' ||
      currentStatus === 'Ignored') {
    return { status: 'skipped', reason: 'already processed' };
  }

  if (parsed.action === 'Approve') {
    row[5] = 'Reviewed';           // Col F
    row[6] = parsed.tdgIssued;     // Col G
    row[12] = parsed.reviewerEmail; // Col M
  } else if (parsed.action === 'Reject') {
    row[5] = 'Rejected';            // Col F
    row[14] = parsed.rejectionReason; // Col O
    row[12] = parsed.reviewerEmail;   // Col M
  }

  updateRow(row);
  return { status: 'updated' };
}

function markEventAsProcessed(rowNumber, transactionId) {
  // Set Col X = TRUE, Col Y = transactionId
  const sheet = SpreadsheetApp.openById(TELEGRAM_CHAT_LOG_SHEET_ID).getSheetByName('Telegram Chat Logs');
  sheet.getRange(rowNumber, 24).setValue(true);   // Col X = Review Processed
  sheet.getRange(rowNumber, 25).setValue(transactionId); // Col Y = Review Transaction ID
}

function createJsonResponse(data, statusCode = 200) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
```

**Deployment:**
- `clasp push` from `tokenomics/google_app_scripts/1BHAGZd…/`
- Same web app URL — no new deployment needed
- The web app URL is configured in Edgar's environment as `GAS_REVIEW_WEBHOOK_URL`

**Edge cases:**
- No unprocessed events found → returns `{ processed: 0, errors: 0 }`
- Row not found (hash key doesn't match) → logged as error, continues to next event
- Row already processed (double-counting guard) → still marked as processed in Telegram Chat Logs
- Invalid event format → logged as error, continues to next event
- Sheets API write failure for marking processed → event NOT marked as processed (retry on next trigger)
- **Same event triggered multiple times** → "Review Processed" column check prevents re-processing

---

### PR 5 — DApp Review Queue Page

**Repo:** `dapp_beta`
**Files:**
- `review_queue.html` — new page
- `scripts/review_queue.js` — new JS module
- `styles/review_queue.css` — new stylesheet

**What it does:**
- Fetches queue from Edgar via `GET /dao/review_queue?limit=10&after_filename=...`
- On first load, no `after_filename` is sent — Edgar returns the earliest files
- Infinite scroll: tracks `last_filename` instead of numeric offset
- Each row displays:
  - Contributor name + resolution badge (✓ green / ⚠ yellow)
  - Contribution description
  - Rubric category
  - Grok-provisioned TDG amount
  - Contribution date
- **Contributor resolution:**
  - If `foundInContributors = true`: dropdown pre-selected to matched contributor, green badge
  - If `foundInContributors = false` or `"RESOLVE FAILED"`: dropdown empty, yellow badge, governor must pick from a dropdown of all known contributors before approving
- **Three-action panel per row:**
  - **✓ Approve** — accepts Grok's provisioned TDG or an adjusted amount (text input field)
  - **→ Skip** — leaves cache file, row re-appears on next load
  - **✕ Reject** — requires reason text field (button disabled until reason entered)
- On Approve: signs `[CONTRIBUTION REVIEW EVENT]` with browser's RSA keypair, submits to Edgar
- On Reject: signs `[CONTRIBUTION REVIEW EVENT]` with Action=Reject + reason
- On Skip: no event, just advances to next row
- States: loading spinner, empty state ("No pending reviews"), error state (with retry button), submitting state (with spinner), success confirmation toast

**Authorization:**
- Anyone can view the queue (read-only)
- Only governors/Sentinels see the action buttons (checked via Edgar's `GET /dao/identity/me`)
- Non-governors see a read-only view with a "Request review access" note

---

### PR 6 — dao_client Module for CONTRIBUTION REVIEW EVENT

**Repo:** `dao_protocol` (the repo that IS dao_client)
**Files:**
- `truesight_dao_client/modules/report_contribution_review.py` — new module
- `pyproject.toml` — add console_scripts entry point

**What it does:**
- Thin CLI wrapper using `build_event_cli` (same pattern as `report_contribution.py`)
- Canonical labels: `Action`, `Scoring Hash Key`, `TDGs Issued`, `Contributor Name`, `Rejection Reason`
- Validators:
  - `Action`: must be one of `Approve`, `Reject`, `Skip`
  - `TDGs Issued`: positive number (required for Approve)
  - `Rejection Reason`: non-empty (required for Reject)
- Console script: `truesight-dao-report-contribution-review`

**Usage:**
```bash
# Approve with Grok's provisioned amount
truesight-dao-report-contribution-review \
    --action Approve \
    --scoring-hash-key XzQ2EhAMD7MN8X0zFhvw \
    --tdgs-issued 45.00 \
    --contributor-name Alice

# Reject
truesight-dao-report-contribution-review \
    --action Reject \
    --scoring-hash-key XzQ2EhAMD7MN8X0zFhvw \
    --rejection-reason "Duplicate entry"

# Dry-run
truesight-dao-report-contribution-review \
    --action Approve \
    --scoring-hash-key XzQ2EhAMD7MN8X0zFhvw \
    --tdgs-issued 45.00 \
    --dry-run
```

**Possible states for Action:**
| Action | Required Fields | Effect |
|--------|----------------|--------|
| `Approve` | Scoring Hash Key, TDGs Issued, Contributor Name | Sets Status = "Reviewed", Col G = TDGs Issued |
| `Reject` | Scoring Hash Key, Rejection Reason | Sets Status = "Rejected", Col O = Rejection Reason |
| `Skip` | Scoring Hash Key | No-op (cache file stays) |

---

### PR 7 — Beta Deploy + UAT

**Steps:**
1. Deploy PR 1 (GitHub Action) — test with a dry-run first
2. Deploy PR 2 (Edgar endpoint) — test with curl against staging
3. Deploy PR 3 (Edgar handler) — test with signed event from DApp
4. Deploy PR 4 (GAS webhook) — `clasp push` to Grok scoring project, test with curl
5. Deploy PR 5 (DApp page) — push to `dapp_beta`, test on beta site
6. Deploy PR 6 (dao_client) — test CLI with dry-run
7. End-to-end test: submit contribution → Grok scores → cache generated → DApp shows it → governor approves → GAS updates sheet → transfer script picks it up → appears in Ledger history

---

### PR 8 — Promote to Production

- `sync_beta_to_prod` for `dapp_prod`
- Update Edgar production environment with GAS webhook URL
- Monitor first 24 hours for any issues

---

## 6. Column Reference (Scored Chatlogs)

| Col | Label | Set by | Description |
|-----|-------|--------|-------------|
| A | Contributor Name | Grok scoring script | Name of the contributor |
| B | Contribution Description | Grok scoring script | What was done |
| C | Rubric | Grok scoring script | Scoring rubric category |
| D | Contribution Type | Grok scoring script | Time (Minutes) / USD / etc. |
| E | TDGs Provisioned | Grok scoring script | Grok's AI-provisioned TDG amount |
| F | Status | Multiple (see §7) | Current state of the row |
| G | TDGs Issued | GAS write-back (on Approve) | Final TDG amount |
| H | Contribution Date | Grok scoring script | When the work was done |
| I | Found in Contributors | Grok scoring script | TRUE / FALSE / RESOLVE FAILED |
| J | Contributor Email | Grok scoring script | Email from contributor lookup |
| K | Scoring Hash Key | Grok scoring script | Unique hash identifying this row |
| L | (reserved) | — | — |
| M | Reviewer Email | GAS write-back | **NEW** — Email of the approving governor |
| N | Cache Generated | GitHub Action cache generator | **NEW** — Timestamp when JSON was pushed |
| O | Rejection Reason | GAS write-back (on Reject) | **NEW** — Reason if Status = Rejected |

---

## 7. Status State Machine

### 7.1 All Possible Status Values

| Status | Set by | Terminal? | Description |
|--------|--------|-----------|-------------|
| `Pending Review` | Grok scoring script (initial write) | Scored Chatlogs Col F (source) | No | Row has been scored by Grok, awaiting review |
| `Reviewed` | GAS write-back (on Approve) | No | Governor has approved, ready for transfer |
| `Rejected` | GAS write-back (on Reject) | **Yes** | Governor has rejected with a reason |
| `Successfully Completed / Full Provision Awarded` | Transfer script (on transfer) | **Ledger history** Col F (destination) | No | TDGs Issued was 0, skipped by transfer |
| `Transferred to Main Ledger` | Transfer script (after transfer) | Scored Chatlogs Col F (source) | **Yes** | Successfully moved to Ledger history |
| `Ignored` | Transfer script (TDG=0) | Scored Chatlogs Col F (source) | **Yes** | Error during transfer |
| `Entry Error` | Transfer script | Scored Chatlogs Col F (source) | **Yes** | Contributor lookup failed during transfer |

### 7.2 State Transitions

```
[Grok scores]                    [Governor approves]          [Transfer script]
     │                                │                            │
     ▼                                ▼                            ▼
Pending Review ─────────► Reviewed ──────► Transferred to Main Ledger
 / Full Provision Awarded           │                            ▲
     │                              │ (TDG=0)                    │
     │                              ▼                            │
     │                          Ignored ──────────────────────────┘
     │
     │ [Governor rejects]
     ▼
  Rejected (terminal)
```

### 7.3 Double-Counting Guard Logic

The GAS doGet handler MUST check the current Status before updating:

```javascript
function applyReviewToScoredChatlogs(parsed) {
  const row = findRowByHashKey(parsed.scoringHashKey);
  const currentStatus = row[5]; // Col F (0-indexed)

  // Double-counting guard: skip if already processed
  if (currentStatus === 'Reviewed' ||
      currentStatus === 'Transferred to Main Ledger' ||
      currentStatus === 'Rejected' ||
      currentStatus === 'Ignored') {
    return { status: 'skipped', reason: 'already processed' };
  }

  // Proceed with update
  if (parsed.action === 'Approve') {
    row[5] = 'Reviewed';           // Col F
    row[6] = parsed.tdgIssued;     // Col G
    row[12] = parsed.reviewerEmail; // Col M
  } else if (parsed.action === 'Reject') {
    row[5] = 'Rejected';            // Col F
    row[14] = parsed.rejectionReason; // Col O
    row[12] = parsed.reviewerEmail;   // Col M
  }

  updateRow(row);
  return { status: 'updated' };
}
```

### 7.4 Transfer Script Compatibility

The existing transfer script (`transfer_scored_contributions_to_main_ledger.js`) checks for:
- `Status = "Reviewed"` → transfers to Ledger history
- `Status = "Pending Review"` → does NOT transfer (must be reviewed first)

No changes needed to the transfer script — it already works with the new flow.

---

## 8. Authorization Model

| Role | View Queue | Approve/Reject | Submit via dao_client |
|------|-----------|----------------|----------------------|
| Anyone (unauthenticated) | ✓ (read-only) | ✕ | ✕ |
| Contributor | ✓ (read-only) | ✕ | ✕ |
| Governor | ✓ | ✓ | ✓ |
| Sentinel (Sophia) | ✓ | ✓ | ✓ |

Enforcement:
- **DApp side:** The review page checks `GET /dao/identity/me` to determine if the user is a governor/Sentinel. If not, action buttons are hidden.
- **Edgar side:** The `[CONTRIBUTION REVIEW EVENT]` handler verifies the RSA signature against the `Contributors Digital Signatures` sheet. Non-governor/non-Sentinel signatures get HTTP 403.
- **dao_client side:** Same RSA signature verification — the CLI uses the user's own keypair. Edgar rejects non-governor keys.

---

## 9. Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Cache generator runs but sheet is unreachable | Action fails with clear error, retries next cycle |
| Cache generator finds 0 new rows | No-op (empty commit skipped) |
| GitHub push fails after Sheets write | Column N already marked, next run skips this row — manual recovery needed |
| Edgar receives Approve but cache file was already deleted | No-op (idempotent — file gone = already processed) |
| Edgar receives Approve but GAS doGet fails | Retry 3x with backoff, then log error (event still in Telegram Chat Logs with Review Processed=FALSE, picked up on next trigger) |
| GAS doGet receives duplicate callback | "Review Processed" column check prevents re-processing |
| Transfer script and GAS doGet race | Transfer script checks Status before moving — if GAS hasn't written yet, it sees "Pending Review" and skips the row (no transfer) |
| Governor approves with TDG=0 | Transfer script sets Status = "Ignored" (existing behavior) |
| Governor rejects but cache file was already deleted by another governor | No-op (idempotent) |
| DApp page loads but Edgar is down | Shows error state with retry button |
| DApp page loads but treasury-cache repo is empty | Shows "No pending reviews" empty state |
| Infinite scroll reaches end of queue | `has_more: false` stops loading |
| Contributor resolution fails (RESOLVE FAILED) | Governor must pick from dropdown before approving |
| Reviewer's RSA key is rotated between viewing and approving | Edgar verifies the current key — if rotated, the old signature is rejected (governor re-logs in) |
| **after_filename not provided (first load)** | Edgar returns the first `limit` files from the directory (earliest = first alphabetically) |
| **after_filename provided but file was already deleted** | Edgar skips to the next available file — does NOT fail or return empty |
| **GAS script called repeatedly** | "Review Processed" column (Col X) prevents re-processing the same event |
| **GAS script times out mid-batch** | Already-processed rows are marked (Col X = TRUE). Unprocessed rows remain FALSE and will be picked up on next call |

---

## 10. UAT Testing Environments

Each component deploys to a beta environment for isolated testing before production promotion.

| Component | Production | Beta (UAT) | Notes |
|-----------|-----------|------------|-------|
| **Edgar API** | `edgar.truesight.me` (Rails + FastAPI) | `beta.edgar.truesight.me` (EC2 `dao-protocol-beta`, `i-0b8c6d989594fb229`, t3.small) | Beta box already provisioned. Deploy new endpoints (`GET /dao/review_queue`, `POST /dao/submit_contribution_review`) to beta first. |
| **DApp review page** | `dapp.truesight.me` → `truesightdao.github.io` (GitHub Pages) | `beta.dapp.truesight.me` → `truesightdao.github.io` (same CNAME) | Both point to the same GitHub Pages site. Beta testing uses a separate page path (e.g. `beta.dapp.truesight.me/dapp/review_queue.html`). The page checks `window.location.hostname` to switch between beta/prod Edgar URLs. |
| **GAS webhook** | Grok scoring GAS project (`1BHAGZd…`) — deployed via `clasp push` | Same GAS project, separate **deployment** (GAS supports multiple deployments per project) | Create a new deployment version for beta. The `doGet(e)` handler checks a `?env=beta` query param or a config variable to switch between beta/prod sheet IDs. |
| **GitHub Action cache generator** | `treasury-cache/review-queue/` | `treasury-cache/review-queue-test/` | Same Action, different folder. The Action checks a `BETA_MODE` repo variable or branch name to decide which folder to write to. |
| **Scored Chatlogs sheet** | `1Tbj7H5ur_egQLRugdXUaSIhEYIKp0vvVv2IZ7WTLCUo` | Same sheet, or a **SANDBOX copy** for isolated testing | For full isolation, create a copy of the Scored Chatlogs sheet and configure the beta GAS deployment + cache generator to use the SANDBOX sheet ID. |

### UAT Flow

1. Deploy Edgar changes to `beta.edgar.truesight.me` first
2. Deploy GAS changes as a new deployment version on the Grok scoring project
3. Configure the GitHub Action to write to `review-queue-test/` folder
4. Point the DApp review page at `beta.dapp.truesight.me` → uses `beta.edgar.truesight.me` API
5. Run end-to-end test: submit a test contribution → Grok scores it → cache generated → DApp surfaces it → governor approves → GAS writes back → transfer script picks it up
6. Only after UAT passes, promote to production (update DNS, deploy to prod Edgar, push GAS to default deployment)

### DNS Records (already exist)

| Record | Type | Value |
|--------|------|-------|
| `beta.edgar.truesight.me` | A | `54.162.175.189` (beta EC2 box) |
| `beta.dapp.truesight.me` | CNAME | `truesightdao.github.io` |

---

## 11. Rollback Plan

If the new system has issues:
1. **Disable the GitHub Action** — cache generation stops, no new files appear
2. **Revert the DApp page** — governors go back to manual sheet editing
3. **Delete remaining cache files** — `treasury-cache/review-queue/` can be cleared
4. **Revert Edgar changes** — roll back the FastAPI deployment
5. **Revert GAS webhook** — `clasp push` the previous version

The Scored Chatlogs sheet is never modified by the new system in a way that breaks the existing transfer script — the transfer script already handles "Reviewed" status (and "Pending Review" for backward compatibility).

---

## 12. Verification & Resume Tracker (2026-06-21, Claude)

A code-level audit (live GAS probe + source + `git log` across `tokenomics`, `dao_protocol`,
`dapp_beta`) found the pipeline **broken at the write-back step**. This section is the source of
truth for resume state — it supersedes the manifest's prior *"PR7 done"* line.

### 12.1 What was verified

| Unit | Verdict | Evidence |
|------|---------|----------|
| **PR2** — Edgar `GET /dao/review_queue` | ✅ **in place** | `dao_protocol/truesight_dao_client/server/routes/dao.py` (review-queue cache read) |
| **PR3** — Edgar `POST /dao/submit_contribution_review` | ✅ **in place** | `dao.py:315` — verifies governor/Sentinel, appends `[CONTRIBUTION REVIEW EVENT]` to Telegram Chat Logs, deletes cache, calls `_call_gas_review_webhook()` (`dao.py:195`) |
| **PR5** — DApp `review_queue.html` | ✅ **in place** | committed to `dapp_beta` `main` (`git ls-files` → `review_queue.html`) |
| **PR4** — GAS `processApprovalRejections` write-back (`1BHAGZd` Grok project) | ❌ **NOT deployed** | Live probe `…AKfycbwnCn80es…/exec?exec=processApprovalRejections` → `ℹ️ No valid action specified`; deployed `doGet` only knows `?action=processTelegramChatLogs` (April code); `grep -c processApprovalRejections` = 0 across all project files; no review commit in `git log` |
| **Edgar trigger config** | ❌ **not wired** | `config.py:115` `gas_review_webhook_url: str = ""`; `dao.py:203` falls back to a "GAS cron" that does not exist |
| **PR1** — GitHub Action cache generator | ⚠️ **unverified** | manifest claims deployed; **operator gate** still open: `GH_PAT_TOKEN` + `GOOGLE_SERVICE_ACCOUNT_JSON` secrets in `treasury-cache` |
| **PR6** — `dao_client` review module | ⚠️ **unverified** | not audited this pass |
| Transfer script (`1-ts0WTM8…`) | ✅ **already batch-capable** | `processAllReviewedRows()` (line 256) scans all `Reviewed` rows → `transferRowByIndex()`; **no per-row manual call needed**, **no changes needed** (plan §7.4 confirmed) |

**Net effect of the PR4 gap:** DApp approve ✅ → Edgar appends `[CONTRIBUTION REVIEW EVENT]` ✅
→ **❌ nothing writes it back to Scored Chatlogs as `Reviewed`** → transfer batch never sees it
→ never reaches Ledger history. The loop cannot complete end-to-end until PR4 lands.

> 🛑 **Myth-buster (supersedes an earlier "add a cron to the transfer script" analysis):** the
> transfer step is **not** the bottleneck and is **not** per-hash-key-manual — `processAllReviewedRows()`
> already batches. `"Successfully Completed / Full Provision Awarded"` is the **destination**
> status in Ledger history, not a transfer trigger. The genuinely missing automation is **PR4**.

### 12.2 Resume tracker — `Advance` markers per OPERATING_INSTRUCTIONS §5c

> **2026-06-22 update (Claude):** PR4 **code is now merged** — handler in
> tokenomics #367, and the deploy-blocker it left (duplicate `doGet`) fixed in #368.
> The 1BHAGZd project is now `clasp`-pushable (one `doGet`, no duplicate functions,
> `node --check` clean). **RESUME HERE moved from "write PR4" to the PR4 DEPLOY GATE**
> (operator: `clasp push` + run `installReviewProcessingTrigger()` + set the Edgar env).
> §12.1's "PR4 NOT deployed" row reflected the pre-#367/#368 state and is now historical.

**RESUME HERE → PR4-DEPLOY (operator gate), then PR7 (real E2E UAT), then PR8.** One PR per turn (§5a).

| Unit | Advance | PR opened | Merged (human) | Deployed | State |
|------|---------|-----------|----------------|----------|-------|
| PR1 — cache generator | `gate: confirm treasury-cache secrets (GH_PAT_TOKEN, GOOGLE_SERVICE_ACCOUNT_JSON)` | ☑ (claimed) | ☑ | ⚠️ operator gate | unverified — confirm before relying on it |
| PR2 — Edgar review_queue | — | ☑ | ☑ | ☑ | ✅ verified |
| PR3 — Edgar submit_contribution_review | — | ☑ | ☑ | ☑ | ✅ verified |
| PR4 — GAS write-back **code** (`1BHAGZd`) | — | ☑ #367 + #368 | ☑ | ☑ | ✅ **code merged + deployable** (dup-`doGet` collision fixed #368; `installReviewProcessingTrigger()` added) |
| PR4-DEPLOY — clasp push + versioned deployment | — | n/a | n/a | ☑ **DONE 2026-06-22** | ✅ `clasp push` @HEAD (gary acct — owns project; also repaired @HEAD: removed orphan Code.js, restored Credentials.js, single doGet). New **anonymous versioned deployment @2** `AKfycbzati5N6aT1slb5C8SAIfs11avrAg_8Wf_ecXXMmoUp0K6I3-TnDwIlv1Cth4IHOQMq` — **verified live:** `?exec=processApprovalRejections` → `{"status":"ok","processed":0,"skipped":0}`. Telegram `@1` deployment left untouched. |
| PR4-WIRE — close the loop (Edgar webhook) | — | n/a | n/a | ☑ **DONE 2026-06-22** | ✅ `DAO_PROTOCOL_GAS_REVIEW_WEBHOOK_URL` = @2 `/exec` URL set in `/home/ubuntu/dao_protocol/.env` on `dao_protocol_nelanco` (backup `.env.bak.20260622`); service restarted, `/ping`→200, var confirmed in `/proc/<pid>/environ`. **Automated path now live:** approve → Edgar calls webhook → `processApprovalRejections` writes back. **Optional backup (not required):** run `installReviewProcessingTrigger()` in the GAS editor for the 15-min safety-net cron. |
| PR5 — DApp review_queue.html | — | ☑ | ☑ | ☑ (beta) | ✅ verified |
| PR6 — dao_client module | `auto` | ☐ | ☐ | ☐ | unverified — audit, then ship if missing |
| **PR-INTEGRATION — close review_queue.html ↔ Edgar gap** ← **RESUME HERE** | `gate: review fix; multi-PR` | ☐ | ☐ | ☐ | 🛑 **UAT BLOCKED (found 2026-06-22).** The page↔Edgar contract is broken — never integration-tested. See §12.3. Must fix before any UAT. |
| PR7 — real E2E UAT on beta/prod | `gate: human-run, after integration fixed` | ☐ | ☐ | ☐ | blocked on PR-INTEGRATION. Note: **no beta backend** — `beta.edgar` lacks the review routes; only prod Edgar is wired, and all sheets/cache are prod (no true staging for this feature) |
| PR8 — Promote to prod | `gate: UAT pass + prod Edgar webhook env set` | ☐ | ☐ | ☐ | blocked on PR4-DEPLOY + PR7 |

**PR4-DEPLOY — DONE 2026-06-22 (Claude):**
- `clasp push` from `tokenomics/google_app_scripts/1BHAGZd…/` with the **gary** account (`garyjob@agroverse.shop`, owns the project). This also repaired an inconsistent live `@HEAD` (it had drifted: orphan `Code.js`, a missing `Credentials.js`, and 3 `doGet`s). Push reconciled it to 5 files / single `doGet`. **Pinned production deployments are unaffected by a `@HEAD` push.**
- ⚠️ GAS gotcha confirmed: the **`@HEAD` test deployment is login-walled** despite `ANYONE_ANONYMOUS`. Anonymous access only applies to **versioned** deployments — so created a **new versioned deployment @2**.
- **Review webhook URL (anonymous, serves the new code):**
  `https://script.google.com/macros/s/AKfycbzati5N6aT1slb5C8SAIfs11avrAg_8Wf_ecXXMmoUp0K6I3-TnDwIlv1Cth4IHOQMq/exec`
  Verified: `?exec=processApprovalRejections` → `{"status":"ok","processed":0,"skipped":0}`; health check lists `["processApprovalRejections","processTelegramChatLogs"]`.

**PR4-WIRE — DONE 2026-06-22 (Claude):**
- **(a) Edgar env (primary path) ✅:** appended `DAO_PROTOCOL_GAS_REVIEW_WEBHOOK_URL=<@2 /exec URL>` to `/home/ubuntu/dao_protocol/.env` on `dao_protocol_nelanco` (host 98.93.94.86; backup `.env.bak.20260622`), restarted `truesight-dao-protocol.service` — `/ping`→200, startup clean, var confirmed in the running process env. Edgar now calls the write-back immediately after each approval/rejection.
- **(b) Safety-net cron (optional backup, NOT done):** run `installReviewProcessingTrigger()` once in the `1BHAGZd` Apps Script editor for a 15-min trigger. Only needed as a fallback if an Edgar→GAS callback fails; not required for the primary path.

**RESUME HERE → PR-INTEGRATION (close the page↔Edgar gap), THEN PR7.**

### 12.3 review_queue.html ↔ Edgar integration gap (found 2026-06-22 during UAT attempt)

PR5 (the DApp page) was written against an Edgar API that PR2/PR3 only partially implement.
Verified live against prod `edgar.truesight.me`:

| Page call (review_queue.html) | Live result | Problem |
|-------------------------------|-------------|---------|
| `DAO_PROTOCOL_BASE = EDGAR_BASE + '/api/v1'` then `/dao/review_queue` (L334/426) | `/api/v1/dao/review_queue` → **404**; `/dao/review_queue` → **200** | bogus `/api/v1` prefix |
| `/api/v1/dao/contributors` (L400) | **404** (even `/dao/contributors` → 404) | **no contributors endpoint on Edgar** |
| `POST /dao/verify_identity` (L370) | **404** | **no identity endpoint on Edgar** → `checkAuth` can't set `isGovernor` → **Approve/Reject buttons never render for anyone** |
| `POST /dao/submit_contribution_review` (L586) | **405** (POST works) | ✅ OK |

Actual Edgar routes: `query.py` serves the review queue (reachable at `/dao/review_queue`),
`dao.py` serves `POST /dao/submit_contribution` + `POST /dao/submit_contribution_review`.
**There is no `verify_identity` or `contributors` route anywhere in the server.**

Additional UAT blockers:
- **Empty queue:** `/dao/review_queue` → `{"items":[],"has_more":false}`. No `review-queue/*.json` cache files exist — PR1 (GitHub Action cache generator) is operator-gated on `treasury-cache` secrets and hasn't produced any.
- **No beta backend:** `beta.edgar.truesight.me/dao/review_queue` → 404 (review routes never deployed to the beta box). Only prod Edgar is wired. All data (Scored Chatlogs, Ledger history, treasury-cache) is prod — there is no real staging for this feature.

**PR-INTEGRATION scope (needs design decision + likely 2–3 PRs, one per turn):**
1. **Page PR (dapp_beta):** set `DAO_PROTOCOL_BASE = EDGAR_BASE` (drop `/api/v1`); repoint governor-auth + contributor-list to real sources.
2. **Decide the auth + contributor sources** — implement Edgar `POST /dao/verify_identity` + `GET /dao/contributors`, **or** repoint the page at the existing governor registry / contributor cache (treasury-cache JSON / GAS) the rest of the DApp already uses. (The `truesight-dao-cache-contributors` CLI + the public-key/governor registry already exist — prefer reusing them over new Edgar endpoints.)
3. **Seed the queue:** run/operator-gate PR1 so ≥1 real `Pending Review` row produces a cache file (note: approving it mutates **prod** Scored Chatlogs + Ledger history / real TDG — treat the first UAT as a controlled prod test with a disposable row).

**Then PR7:** real E2E UAT (against prod, since no beta backend). **Then PR8:** promote page to prod.
