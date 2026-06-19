# Scoring Review Queue — Implementation Plan

**Status:** Draft · **Created:** 2026-06-18
**Last updated:** 2026-06-18 (v9: add doGet health check to telegram_webhook_listener.js)
**Handoff thread:** [Telegram topic 7191](https://t.me/c/3919341801/7191)

---

## 1. Problem Statement

Today, after Grok scores a `[CONTRIBUTION EVENT]` and writes it to the **Scored Chatlogs** sheet (spreadsheet `1Tbj7H5ur_egQLRugdXUaSIhEYIKp0vvVv2IZ7WTLCUo`), the row sits with `Status = "Successfully Completed / Full Provision Awarded"` and `TDGs Issued = "0.00"`. A governor must:

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

1. **GitHub Actions cache generator** (Python, scheduled cron) reads Scored Chatlogs, finds rows with `Status = "Successfully Completed / Full Provision Awarded"` AND `Column N` empty, generates one JSON cache file per row in `treasury-cache/review-queue/`, and marks a `Cache Generated` column on the sheet.
2. **DApp review page** (new HTML page) reads the cache files via Edgar, surfaces the oldest 10 with infinite scroll. Anyone can view the queue.
3. **Governor/Sentinel** sees a three-action panel per row: **Approve** (accepts Grok's provisioned TDG or an adjusted amount), **Skip** (leaves for later), or **Reject** (with required reason).
4. **Contributor resolution** — The cache includes the `found_in_contributors` flag (Column I). If TRUE, the contributor dropdown is pre-selected. If FALSE or "RESOLVE FAILED", the governor must pick the right contributor from a dropdown before approving.
5. **On Approve/Reject**, the browser signs a `[CONTRIBUTION REVIEW EVENT]` to Edgar. The event payload is minimal — only the hash key, action, and TDG amount/rejection reason. **No reviewer email** — Edgar resolves the reviewer's identity from the RSA signature.
6. **Edgar verifies** the signer is a governor or Sentinel (via RSA signature → `Contributors Digital Signatures` sheet). On success, Edgar resolves the reviewer's email and includes it in the webhook to GAS.
7. **On approval**, Edgar deletes the cache file from `treasury-cache/review-queue/` and fires a webhook to the GAS write-back script with the TDG amount and reviewer email.
8. **On rejection**, Edgar deletes the cache file and fires a webhook with the rejection reason and reviewer email. The GAS script sets Status = "Rejected" and records the reason.
9. **On Skip**, the cache file stays — it will be re-surfaced on the next page load.

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
│  │ Column J = "Pending"  │    │  Col A = Contributor Name    │      │
│  └──────────────────────┘    │  Col F = Status (see §7)     │      │
│         │                    │  Col E = TDGs Provisioned    │      │
│         │ Grok scoring       │  Col G = TDGs Issued (0.00)  │      │
│         ▼                    │  Col I = Found in Contribs   │      │
│  ┌──────────────────────┐    │  Col K = Scoring Hash Key    │      │
│  │ Grok Scoring Script  │    │  Col M = Reviewer Email (NEW)│      │
│  │ (1BHAGZd…)           │    │  Col N = Cache Generated(NEW)│      │
│  │ Scheduled GAS        │    │  Col O = Rejection Reason(NEW)│      │
│  └──────────────────────┘    └──────────┬───────────────────┘      │
│         │                               │                          │
│         │ (same GAS project)            │ (same GAS project)       │
│         ▼                               ▼                          │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ Grok Scoring GAS Project (1BHAGZd…)                     │       │
│  │                                                         │       │
│  │ Existing: Code.js (Grok scoring + write to Scored       │       │
│  │   Chatlogs)                                             │       │
│  │ Existing: telegram_webhook_listener.js (doPost for      │       │
│  │   Telegram webhooks + orchestrator calls)               │       │
│  │ Extended: telegram_webhook_listener.js — add doGet for  │       │
│  │   health check/ping + route for Edgar review callbacks  │       │
│  │   in doPost                                              │       │
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
│  - Finds rows with Status = "Successfully Completed / Full          │
│    Provision Awarded" AND Col N empty                               │
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
│  EDGAR (sentiment_importer / dao_protocol)                          │
│                                                                     │
│  GET /dao/review_queue?limit=10&after_filename=XzQ2EhAMD7MN8X0zFhvw│
│  - Lists treasury-cache/review-queue/ directory (sorted by name)    │
│  - If after_filename is NOT provided: return the first `limit` files│
│    from the directory (earliest = first alphabetically)             │
│  - If after_filename IS provided but the file no longer exists      │
│    (already approved/deleted): skip to the next available file      │
│    — do NOT fail or return empty                                    │
│  - Returns next `limit` files + their JSON content                  │
│  - Includes `next_filename` for the DApp to use as cursor           │
│  - No numeric offset — cursor is the filename itself                │
│                                                                     │
│  POST /dao/submit_contribution  (CONTRIBUTION REVIEW EVENT)         │
│  - Verifies signer is governor or Sentinel (via RSA signature)      │
│  - Resolves reviewer email from the RSA signature                   │
│  - On Approve: deletes cache file, fires webhook with TDG amount   │
│    + reviewer email                                                  │
│  - On Reject: deletes cache file, fires webhook with rejection      │
│    reason + reviewer email                                           │
│  - On Skip: no-op (cache file stays)                                │
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
│    (tracks `last_filename` instead of `offset`)                      │
│  - Each row shows: contributor, contribution, rubric, provisioned   │
│  - Contributor resolution badge: ✓ Resolved / ⚠ Resolve Failed     │
│    - If Resolved: dropdown pre-selected to matched contributor      │
│    - If Failed: dropdown empty, governor must pick from list        │
│  - Three-action panel per row:                                      │
│    ✓ Approve (with optional TDG override field)                     │
│    → Skip (leaves cache file, re-surfaces later)                    │
│    ✕ Reject (requires reason text field)                            │
│  - On Approve: signs [CONTRIBUTION REVIEW EVENT] with Action=Approve│
│  - On Reject: signs [CONTRIBUTION REVIEW EVENT] with Action=Reject  │
│  - On Skip: no event, just advances to next row                     │
│  - States: loading, empty (no pending reviews), error, submitting,  │
│    success confirmation                                              │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (Edgar fires webhook to GAS)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GAS WRITE-BACK (in Grok Scoring GAS Project — 1BHAGZd…)           │
│                                                                     │
│  Extended: telegram_webhook_listener.js                             │
│                                                                     │
│  NEW: function doGet(e) — health check / ping endpoint              │
│  - Returns JSON: { status: "ok", project: "tdg_scoring",           │
│    version: "1.0.0" }                                               │
│  - Edgar can GET this URL to verify the webhook is reachable        │
│    before sending POST callbacks                                     │
│  - Avoids CORS/content-type issues that can block POST              │
│                                                                     │
│  EXISTING: function doPost(e) — extended with route check           │
│  - Existing doPost already handles Telegram webhooks                │
│  - Add a route check: if JSON body contains `scoringHashKey`,       │
│    route to review callback handler instead of Telegram handler     │
│  - Parses { scoringHashKey, action, tdgIssued?, rejectionReason?,  │
│      reviewerEmail }                                                │
│  - Looks up the row in Scored Chatlogs by scoringHashKey (Col K)    │
│  - Double-counting guard: checks if Status is already "Reviewed"    │
│    or "Transferred to Main Ledger" — if so, skips (no-op)           │
│  - On Approve: sets Col F = "Reviewed", Col G = tdgIssued,         │
│    Col M = reviewerEmail                                             │
│  - On Reject: sets Col F = "Rejected", Col O = rejectionReason,    │
│    Col M = reviewerEmail                                             │
│  - Returns 200 OK with { status: "updated" }                       │
│                                                                     │
│  Deployment: clasp push from tokenomics/google_app_scripts/         │
│  1BHAGZd…/ (same project as Grok scoring)                           │
│  No new deployment needed — same web app URL, same doPost entry     │
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
│    "Successfully Completed / Full Provision Awarded"                │
│  - Transfers to Ledger history in main ledger                       │
│  - Sets Status = "Transferred to Main Ledger"                       │
│  - No changes needed — it already works with the "Reviewed" status  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Schema

### 4.1 Scored Chatlogs Sheet (Google Sheets — 1Tbj7H5ur…)

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

### 4.2 Cache File Schema (treasury-cache/review-queue/<hash_key>.json)

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

### 4.3 CONTRIBUTION REVIEW EVENT Payload

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

**Note:** `Reviewer Email` is NOT in the signed payload. Edgar resolves it server-side from the RSA signature.

### 4.4 Edgar Webhook to GAS (POST)

```json
{
  "scoringHashKey": "XzQ2EhAMD7MN8X0zFhvw",
  "action": "Approve",
  "tdgIssued": "45.00",
  "contributorName": "Alice",
  "reviewerEmail": "gary@truesight.me",
  "timestamp": "2026-06-18T14:30:00Z"
}
```

---

## 5. PR Breakdown

### PR 1 — GitHub Actions Cache Generator

**Repo:** `treasury-cache` (or `dao_protocol` if scripts live there)
**Files:**
- `.github/workflows/generate_review_cache.yml` — scheduled cron (every 5 min)
- `scripts/generate_review_cache.py` — Python script

**What it does:**
- Reads Scored Chatlogs via Google Sheets API (service account: `tdg_scoring`)
- Finds rows where `Status = "Successfully Completed / Full Provision Awarded"` AND `Column N` is empty
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
- On **Approve**:
  - Deletes the cache file from `treasury-cache/review-queue/<hash_key>.json`
  - Fires webhook to GAS with `{ scoringHashKey, action: "Approve", tdgIssued, contributorName, reviewerEmail }`
- On **Reject**:
  - Deletes the cache file
  - Fires webhook to GAS with `{ scoringHashKey, action: "Reject", rejectionReason, reviewerEmail }`
- On **Skip**: no-op (cache file stays)

**Authorization:**
- Non-governor/non-Sentinel signatures → HTTP 403
- Missing `Action` field → HTTP 400
- Approve without `TDGs Issued` → HTTP 400
- Reject without `Rejection Reason` → HTTP 400

**Webhook retry:**
- If GAS webhook returns non-200, retry up to 3 times with exponential backoff
- After 3 failures, log the error and leave the cache file (manual recovery)

---

### PR 4 — Extend GAS doPost + Add doGet in Grok Scoring Project

**GAS Project:** `1BHAGZd…` (same project as Grok scoring script)
**Repo:** `tokenomics` → `google_app_scripts/1BHAGZd…/`
**Files:**
- `telegram_webhook_listener.js` — **extend** existing doPost(e) + **add** doGet(e)

**Why extend instead of new file:** The Grok scoring project already has a `doPost(e)` deployed as a web app in `telegram_webhook_listener.js`. Rather than creating a new GAS project or a new file with a separate deployment, we add a route check to the existing `doPost(e)` and add a `doGet(e)` for health checks.

**NEW — function doGet(e) — Health check / ping endpoint:**
```javascript
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({
      status: "ok",
      project: "tdg_scoring",
      version: "1.0.0",
      timestamp: new Date().toISOString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
}
```
- Edgar can GET this URL to verify the webhook is reachable before sending POST callbacks
- Avoids CORS/content-type issues that can block POST — GET is universally allowed
- Returns a simple JSON status response

**EXISTING — function doPost(e) — Extended with route check:**
```javascript
function doPost(e) {
  const json = JSON.parse(e.postData.contents);
  // Route: if this is an Edgar review callback, handle it
  if (json.scoringHashKey) {
    return handleReviewCallback(json);
  }
  // Existing Telegram webhook handling...
}
```

**handleReviewCallback(json) function:**
- Parses `{ scoringHashKey, action, tdgIssued?, rejectionReason?, reviewerEmail }`
- Looks up the row in Scored Chatlogs by `scoringHashKey` (Column K)
- **Double-counting guard:** Checks if `Status` is already `"Reviewed"` or `"Transferred to Main Ledger"` — if so, returns 200 with `{ status: "skipped", reason: "already processed" }` (no-op)
- On **Approve**:
  - Sets `Col F` = `"Reviewed"`
  - Sets `Col G` = `tdgIssued`
  - Sets `Col M` = `reviewerEmail`
- On **Reject**:
  - Sets `Col F` = `"Rejected"`
  - Sets `Col O` = `rejectionReason`
  - Sets `Col M` = `reviewerEmail`
- Returns 200 OK with `{ status: "updated" }`

**Deployment:**
- `clasp push` from `tokenomics/google_app_scripts/1BHAGZd…/`
- Same web app URL — no new deployment needed, same `doPost(e)` entry point
- The web app URL is configured in Edgar's environment as `GAS_REVIEW_WEBHOOK_URL`

**Edge cases:**
- Row not found (hash key doesn't match) → return 404
- Row already processed (double-counting guard) → return 200 with skip reason
- Invalid JSON body → return 400
- Sheets API write failure → return 500 (triggers Edgar retry)

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
| `Successfully Completed / Full Provision Awarded` | Grok scoring script (initial) | No | Row has been scored by Grok, awaiting review |
| `Reviewed` | GAS write-back (on Approve) | No | Governor has approved, ready for transfer |
| `Rejected` | GAS write-back (on Reject) | **Yes** | Governor has rejected with a reason |
| `Ignored` | Transfer script (TDG=0) | **Yes** | TDGs Issued was 0, skipped by transfer |
| `Transferred to Main Ledger` | Transfer script | **Yes** | Successfully moved to Ledger history |
| `Entry Error` | Transfer script | **Yes** | Error during transfer |
| `Entry Error - Contributor Not Found` | Transfer script | **Yes** | Contributor lookup failed during transfer |

### 7.2 State Transitions

```
[Grok scores]                    [Governor approves]          [Transfer script]
     │                                │                            │
     ▼                                ▼                            ▼
Successfully Completed ──────► Reviewed ──────► Transferred to Main Ledger
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

The GAS write-back script MUST check the current Status before updating:

```javascript
function handleReviewCallback(json) {
  const row = findRowByHashKey(json.scoringHashKey);
  const currentStatus = row[5]; // Col F (0-indexed)

  // Double-counting guard: skip if already processed
  if (currentStatus === 'Reviewed' ||
      currentStatus === 'Transferred to Main Ledger' ||
      currentStatus === 'Rejected' ||
      currentStatus === 'Ignored') {
    return { status: 'skipped', reason: 'already processed' };
  }

  // Proceed with update
  if (json.action === 'Approve') {
    row[5] = 'Reviewed';  // Col F
    row[6] = json.tdgIssued; // Col G
    row[12] = json.reviewerEmail; // Col M
  } else if (json.action === 'Reject') {
    row[5] = 'Rejected';  // Col F
    row[14] = json.rejectionReason; // Col O
    row[12] = json.reviewerEmail; // Col M
  }

  updateRow(row);
  return { status: 'updated' };
}
```

### 7.4 Transfer Script Compatibility

The existing transfer script (`transfer_scored_contributions_to_main_ledger.js`) checks for:
- `Status = "Reviewed"` → transfers to Ledger history
- `Status = "Successfully Completed / Full Provision Awarded"` → also transfers (backward compatibility for rows that were never reviewed)

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
| Edgar receives Approve but GAS webhook fails | Retry 3x with backoff, then log error for manual recovery |
| GAS webhook receives duplicate callback | Double-counting guard skips if Status is already Reviewed/Transferred |
| Transfer script and GAS webhook race | Transfer script checks Status before moving — if GAS hasn't written yet, it sees "Successfully Completed" and transfers with TDG=0 (existing behavior) |
| Governor approves with TDG=0 | Transfer script sets Status = "Ignored" (existing behavior) |
| Governor rejects but cache file was already deleted by another governor | No-op (idempotent) |
| DApp page loads but Edgar is down | Shows error state with retry button |
| DApp page loads but treasury-cache repo is empty | Shows "No pending reviews" empty state |
| Infinite scroll reaches end of queue | `has_more: false` stops loading |
| Contributor resolution fails (RESOLVE FAILED) | Governor must pick from dropdown before approving |
| Reviewer's RSA key is rotated between viewing and approving | Edgar verifies the current key — if rotated, the old signature is rejected (governor re-logs in) |
| **after_filename not provided (first load)** | Edgar returns the first `limit` files from the directory (earliest = first alphabetically) |
| **after_filename provided but file was already deleted** | Edgar skips to the next available file — does NOT fail or return empty |

---

## 10. Rollback Plan

If the new system has issues:
1. **Disable the GitHub Action** — cache generation stops, no new files appear
2. **Revert the DApp page** — governors go back to manual sheet editing
3. **Delete remaining cache files** — `treasury-cache/review-queue/` can be cleared
4. **Revert Edgar changes** — roll back the FastAPI deployment
5. **Revert GAS webhook** — `clasp push` the previous version

The Scored Chatlogs sheet is never modified by the new system in a way that breaks the existing transfer script — the transfer script already handles "Reviewed" and "Successfully Completed / Full Provision Awarded" statuses.
