# Scoring Review Queue — Implementation Plan

**Status:** Draft · **Created:** 2026-06-18
**Last updated:** 2026-06-18 (v5: explicit status state machine, corrected initial status)
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
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (reads via Google Sheets API)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GITHUB ACTIONS (scheduled cron)                                    │
│                                                                     │
│  generate_review_cache.py                                           │
│  - Reads Scored Chatlogs via Google Sheets API                      │
│  - Finds rows with Status = "Successfully Completed / Full Provision
│    Awarded" AND Col N empty                                          │
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
│  - Skips files up to and including after_filename (if provided)     │
│  - Returns next `limit` files + their content                       │
│  - Includes `next_filename` for the DApp to use as cursor           │
│  - No numeric offset — cursor is the filename itself                │
│                                                                     │
│  POST /dao/submit_contribution  (CONTRIBUTION REVIEW EVENT)         │
│  - Verifies signer is governor or Sentinel (via RSA signature)      │
│  - Resolves reviewer email from the RSA signature                   │
│  - On Approve: deletes cache file, fires webhook with TDG amount    │
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
│  - Governor/Sentinel sees three-action panel:                       │
│    • **Approve** — accepts Grok's provisioned TDG or adjusted amt   │
│    • **Skip** — leaves for later (cache file stays)                 │
│    • **Reject** — requires reason text field                        │
│  - If contributor resolve failed: dropdown to pick correct person   │
│  - On Approve/Reject: browser signs minimal event → Edgar           │
│    (no reviewer email in the signed payload)                         │
│  - Non-governors see queue but no action buttons                    │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ (Edgar webhook on approval/rejection — includes reviewer_email)
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GAS WRITE-BACK SCRIPT                                              │
│                                                                     │
│  process_review_approval.gs                                         │
│  - Receives webhook from Edgar with:                                │
│    • hash_key, action (approve/reject), tdgs_issued (if approve),   │
│      reviewer_email (resolved by Edgar from signature),             │
│      rejection_reason (if reject), contributor_name                 │
│  - Opens Scored Chatlogs sheet                                      │
│  - Finds row by hash_key (Column K)                                 │
│  - Double-counting guard: skip if Status is terminal (see §7)       │
│  - On Approve: sets Status = "Reviewed", TDGs Issued, Reviewer,    │
│    and Contributor Name (if corrected)                               │
│  - On Reject: sets Status = "Rejected", Rejection Reason (Col O),   │
│    Reviewer Email                                                    │
│  - Returns JSON status                                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow (Step by Step)

### 4.1 Cache Generation (GitHub Action)

1. **Trigger:** GitHub Actions scheduled cron (every 5 minutes, or on-demand via workflow_dispatch)
2. **Read:** Google Sheets API → `Scored Chatlogs` tab, columns A–N
3. **Filter:** Rows where `Column F (Status) = "Successfully Completed / Full Provision Awarded"` AND `Column N (Cache Generated)` is empty
4. **For each matching row:**
   - Read `Column K (Scoring Hash Key)` → this is the filename
   - Read `Column I (Found in Contributors)` → TRUE / FALSE / "RESOLVE FAILED"
   - Build JSON object (see §6 for schema)
   - Write to `treasury-cache/review-queue/<hash_key>.json`
5. **After all files written:**
   - Git commit + push to `main`
   - For each processed row, write current timestamp to `Column N` (via Sheets API batch update)
6. **Idempotency:** If a file already exists in the repo, skip it (don't overwrite). If `Column N` already has a timestamp, skip the row.

### 4.2 Queue Serving (Edgar) — Cursor-Based Pagination

1. **Endpoint:** `GET /dao/review_queue?limit=10&after_filename=XzQ2EhAMD7MN8X0zFhvw`
   - `limit` (optional, default 10, max 50): how many items to return
   - `after_filename` (optional): the filename of the last item from the previous page. If omitted, start from the beginning.
2. **Read:** GitHub API → list `treasury-cache/review-queue/` directory, sorted alphabetically by filename (ascending)
3. **Skip:** If `after_filename` is provided, skip all files up to and including that filename
4. **Slice:** Take the next `limit` files from the remaining list
5. **Read each file's content** and return as JSON array
6. **Response:**
   ```json
   {
     "items": [ /* cache file objects */ ],
     "total_count": 42,
     "next_filename": "M52VB3RP2VLzU3UxLIf",
     "has_more": true
   }
   ```
   - `next_filename` is the filename of the last item in this page. The DApp passes this as `after_filename` on the next request.
   - `has_more` is `false` when there are no more files after this page.
7. **Why cursor-based instead of offset:** Files are deleted from the directory as approvals happen. A numeric offset would shift — the file at offset 10 today might be a different file tomorrow. The filename is stable; even if files before it are deleted, the cursor still points to the right place.
8. **Auth:** Anyone can call this endpoint (read-only). No signature required.

### 4.3 Approval / Rejection (DApp → Edgar)

1. **DApp page** loads the queue from Edgar, renders each row
2. **Governor/Sentinel** sees:
   - Contributor name with resolution badge (✓ Resolved / ⚠ Resolve Failed)
   - If resolve failed: a dropdown of all known contributors to pick the correct one
   - Three buttons: **Approve**, **Skip**, **Reject**
   - TDG amount field (pre-filled with Grok's provisioned value, editable)
   - Rejection reason text field (shown when Reject is selected)
3. **On Approve click:**
   - Browser builds `[CONTRIBUTION REVIEW EVENT]` payload — **minimal, no reviewer email**:
     ```
     [CONTRIBUTION REVIEW EVENT]
     - Action: Approve
     - Scoring Hash Key: XzQ2EhAMD7MN8X0zFhvw
     - TDGs Issued: 8.33
     - Contributor Name: Gary Teh (if corrected from resolve-failed)
     ```
   - Browser signs with RSA private key
   - Submits to `POST /dao/submit_contribution`
4. **On Reject click:**
   - Browser builds payload — **no reviewer email**:
     ```
     [CONTRIBUTION REVIEW EVENT]
     - Action: Reject
     - Scoring Hash Key: XzQ2EhAMD7MN8X0zFhvw
     - Rejection Reason: Duplicate contribution, already recorded in ledger
     ```
   - Browser signs and submits
5. **On Skip click:** No event sent. Cache file stays. UI simply removes the row from the current view (it will re-appear on next page load).
6. **Edgar receives and validates:**
   - Verifies RSA signature
   - Looks up signer's email in `Contributors Digital Signatures` sheet → this is the `reviewer_email`
   - Checks if signer is a governor (in `Governors` tab) OR Sentinel (`Is Sentinel = TRUE`)
   - If not authorized → return 403
   - If authorized:
     a. Logs the event to Telegram Chat Logs
     b. Deletes `treasury-cache/review-queue/<hash_key>.json` via GitHub API
     c. Fires webhook to GAS write-back script with action + payload + `reviewer_email` (resolved from signature)
     d. Returns success

### 4.4 Write-Back (GAS webhook)

1. **Trigger:** Edgar sends POST to GAS web app URL with payload:
   ```json
   {
     "action": "process_review_result",
     "hash_key": "XzQ2EhAMD7MN8X0zFhvw",
     "review_action": "approve",
     "tdgs_issued": 8.33,
     "reviewer_email": "garyjob@agroverse.shop",  ← resolved by Edgar from RSA signature
     "contributor_name": "Gary Teh",
     "rejection_reason": null
   }
   ```
   Or for rejection:
   ```json
   {
     "action": "process_review_result",
     "hash_key": "XzQ2EhAMD7MN8X0zFhvw",
     "review_action": "reject",
     "tdgs_issued": 0,
     "reviewer_email": "garyjob@agroverse.shop",  ← resolved by Edgar from RSA signature
     "contributor_name": null,
     "rejection_reason": "Duplicate contribution, already recorded in ledger"
   }
   ```
2. **GAS script:**
   - Opens `Scored Chatlogs` sheet
   - Finds row by `Column K = hash_key`
   - **Double-counting guard:** Checks if `Column F (Status)` is a terminal status (see §7) → if so, SKIP (return 200 with `"already_processed"`)
   - **On Approve:**
     - Sets `Column F = "Reviewed"`
     - Sets `Column G (TDGs Issued)` = approved amount
     - Sets `Column M (Reviewer Email)` = reviewer_email
     - If `contributor_name` provided and differs from current `Column A`, update it
   - **On Reject:**
     - Sets `Column F = "Rejected"`
     - Sets `Column O (Rejection Reason)` = rejection_reason
     - Sets `Column M (Reviewer Email)` = reviewer_email
   - Returns 200

---

## 5. Event Schema

### CONTRIBUTION REVIEW EVENT (signed by browser → Edgar)

| Field | Required | Description |
|-------|----------|-------------|
| `Action` | Yes | `"Approve"` or `"Reject"` |
| `Scoring Hash Key` | Yes | The hash key from Scored Chatlogs Column K |
| `TDGs Issued` | On Approve | Final TDG amount awarded (number) |
| `Contributor Name` | On Approve | Corrected contributor name (if different from cache) |
| `Rejection Reason` | On Reject | Free-text reason for rejection |

**Note:** `Reviewer Email` is NOT in the signed event. Edgar resolves it from the RSA signature server-side.

### Edgar → GAS Webhook Payload

| Field | Source | Description |
|-------|--------|-------------|
| `action` | Fixed | Always `"process_review_result"` |
| `hash_key` | From sign event | The hash key |
| `review_action` | From sign event | `"approve"` or `"reject"` |
| `tdgs_issued` | From sign event | Final TDG amount (0 for reject) |
| `reviewer_email` | Resolved by Edgar | Email of the governor/Sentinel who signed |
| `contributor_name` | From sign event | Corrected contributor name (if provided) |
| `rejection_reason` | From sign event | Reason for rejection (null if approve) |

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
  "found_in_contributors": false,
  "generated_at": "2026-06-18T12:00:00Z"
}
```

---

## 7. Status State Machine (Column F)

This is the definitive reference for every possible status value in Column F of the Scored Chatlogs sheet, who sets it, when, and what transitions are valid.

### Status Values and Transitions

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
                    ▼                                              │
  ┌─────────────────────────────────────────────────────┐         │
  │ Successfully Completed / Full Provision Awarded     │         │
  │ (Initial — set by Grok scoring script)              │         │
  │ TDGs Issued = 0.00 (placeholder)                    │         │
  └─────────────────────┬───────────────────────────────┘         │
                        │                                         │
          ┌─────────────┼─────────────┐                           │
          ▼             ▼             ▼                           │
  ┌──────────┐  ┌──────────────┐  ┌──────────┐                   │
  │ Reviewed │  │   Rejected   │  │ (stays)  │  ← Skip (no       │
  │          │  │              │  │          │    status change)  │
  │ TDGs > 0 │  │ TDGs = 0    │  │          │                   │
  └─────┬────┘  └──────┬───────┘  └──────────┘                   │
        │              │                                          │
        │              │  (terminal — no further transitions)     │
        ▼              │                                          │
  ┌──────────┐         │                                          │
  │Ignored   │         │                                          │
  │(TDG=0)   │         │                                          │
  └─────┬────┘         │                                          │
        │              │                                          │
        ▼              │                                          │
  ┌────────────────┐   │                                          │
  │ Transferred to │   │                                          │
  │ Main Ledger    │   │                                          │
  │ (terminal)     │   │                                          │
  └────────────────┘   │                                          │
                        │                                          │
  ┌────────────────┐    │                                          │
  │ Entry Error    │◄───┘  (set by transfer script if contributor │
  │                │        not found in Contributors sheet)       │
  │ Entry Error -  │                                               │
  │ Contributor    │                                               │
  │ Not Found      │                                               │
  └────────────────┘                                               │
```

### Detailed Status Table

| # | Status Value | Set By | When | Column G (TDGs Issued) | Terminal? | Next Valid Statuses |
|---|-------------|--------|------|----------------------|-----------|-------------------|
| 1 | `Successfully Completed / Full Provision Awarded` | Grok scoring script | After AI scoring completes | `0.00` (placeholder) | No | Reviewed, Rejected, (stays same on Skip) |
| 2 | `Reviewed` | GAS write-back script | Governor approves via DApp | Governor's approved amount (> 0) | No | Ignored (if TDG=0), Transferred to Main Ledger |
| 3 | `Reviewed` | GAS write-back script | Governor approves via DApp | `0` (zero TDG) | No | Ignored (transfer script auto-converts) |
| 4 | `Rejected` | GAS write-back script | Governor rejects via DApp | `0` | **Yes** | (none) |
| 5 | `Ignored` | Transfer script | Auto-set when Reviewed row has TDGs Issued = 0 | `0` | **Yes** | (none) |
| 6 | `Transferred to Main Ledger` | Transfer script | After successful transfer to Ledger history | Governor's approved amount | **Yes** | (none) |
| 7 | `Entry Error` | Transfer script | Contributor not found in Contributors sheet | `0` | **Yes** | (none) |
| 8 | `Entry Error - Contributor Not Found` | Transfer script | Contributor not found (variant) | `0` | **Yes** | (none) |

### Double-Counting Guard Logic

The GAS write-back script MUST check Column F before writing. If the current status is any of the **terminal** statuses (Rejected, Ignored, Transferred to Main Ledger, Entry Error, Entry Error - Contributor Not Found), the script MUST skip the write and return `"already_processed"`. This prevents:

- A row that was already transferred from being set back to "Reviewed" (which would cause the transfer script to re-process it)
- A row that was already rejected from being approved later

### Transfer Script Behavior

The existing `transfer_scored_contributions_to_main_ledger.js` checks for these statuses:
- `"Reviewed"` → proceeds with transfer (if TDGs Issued > 0)
- `"Reviewed"` with TDGs Issued = 0 → sets to `"Ignored"` immediately
- `"Successfully Completed / Full Provision Awarded"` → also proceeds (legacy support)
- `"Transferred to Main Ledger"` → skips
- Any other status → skips

**Important:** The transfer script does NOT check for `"Rejected"` explicitly — it will skip it because it doesn't match `"Reviewed"` or `"Successfully Completed / Full Provision Awarded"`. This is correct behavior.

---

## 8. Scored Chatlogs Column Reference

| Col | Header | Role |
|-----|--------|------|
| A | Contributor Name | Contributor display name |
| B | Project Name | Source platform (e.g. `telegram_chatlog`) |
| C | Contribution Made | The contribution text |
| D | Rubric classification | Grok's classification |
| E | TDGs Provisioned | Grok's suggested TDG amount |
| F | Status | See §7 for full state machine |
| G | TDGs Issued | Final awarded TDG (set by governor) |
| H | Status date | Date of the original contribution |
| I | Existing Contributor | TRUE / FALSE / "RESOLVE FAILED" — whether contributor resolved |
| J | Reporter Name | Who reported the contribution |
| K | Scoring Hash Key | Unique hash for deduplication |
| L | Main Ledger Row Number | Row in Ledger history after transfer |
| M | Reviewer Email | (NEW) Email of the approving/rejecting governor (set by GAS write-back) |
| N | Cache Generated | (NEW) Timestamp when cache file was created |
| O | Rejection Reason | (NEW) Free-text reason if rejected |

---

## 9. UI Specification (DApp review_queue.html)

### Layout

- **Header:** "Contribution Review Queue" with count badge (e.g., "42 pending")
- **Filter bar:** Optional — filter by contributor name or date range
- **Card list** (infinite scroll using cursor-based pagination):
  - DApp tracks `last_filename` (not `offset`) for the next page request
  - On scroll to bottom, calls `GET /dao/review_queue?limit=10&after_filename=<last_filename>`
  - Each card shows:
    - **Contributor name** with resolution badge:
      - ✓ Green badge = `found_in_contributors: true`
      - ⚠ Yellow badge = `found_in_contributors: false` or `"RESOLVE FAILED"`
    - **Contribution text** (truncated to 3 lines, expandable)
    - **Rubric** (classification)
    - **TDGs Provisioned** (Grok's amount)
    - **Date** (status_date)
    - **Reporter** name

### Governor/Sentinel Actions (only visible to authorized users)

- **Contributor dropdown** — If `found_in_contributors` is FALSE or "RESOLVE FAILED", show a dropdown of all known contributors (loaded from `dao_members.json` or Edgar). Pre-selected to current value if resolved.
- **TDG amount field** — Pre-filled with Grok's provisioned value. Editable.
- **Three buttons:**
  - **✓ Approve** — Green button. Submits approval with current TDG amount and selected contributor.
  - **→ Skip** — Gray button. Removes card from view (no event sent).
  - **✕ Reject** — Red button. When clicked, reveals a text area for rejection reason (required). Submits rejection.

### Non-Governor View

- Same card list, but no action buttons, no dropdown, no TDG field.
- Text at top: "You are viewing the review queue as a read-only observer."

### States

| State | UI |
|-------|-----|
| Loading | Skeleton cards with pulse animation |
| Empty queue | "🎉 All contributions have been reviewed!" with illustration |
| Error (Edgar down) | "Unable to load review queue. Retry" button |
| Submitting approval | Button shows spinner, disabled state |
| Approval success | Card fades out with green checkmark animation |
| Approval error | Toast: "Approval failed. Please try again." |
| Rejection (no reason) | Reject button disabled, red border on reason field |

---

## 10. PR Breakdown (Sequenced)

Each PR is standalone, small, and independently reviewable. Do NOT chain multiple PRs in one turn.

### PR 1: GitHub Action — Cache Generator

**Repo:** `treasury-cache` (API-only DATA repo — single-file write via `upload_file_to_github`)

**Scope:**
- Create `.github/workflows/generate_review_cache.yml` — scheduled cron (every 5 min) + `workflow_dispatch`
- Create `scripts/generate_review_cache.py` — Python script that:
  - Reads Scored Chatlogs via Google Sheets API (service account from GitHub Secrets)
  - Filters for `Status = "Successfully Completed / Full Provision Awarded"` AND `Column N` empty
  - Generates JSON files in `review-queue/<hash_key>.json` (includes `found_in_contributors` field)
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
- `found_in_contributors` field correctly reflects Column I

---

### PR 2: Edgar — Review Queue Endpoint (Cursor-Based Pagination)

**Repo:** `sentiment_importer` (Rails) or `dao_protocol` (Python FastAPI)

**Scope:**
- Add `GET /dao/review_queue` endpoint with cursor-based pagination
- Parameters: `limit` (default 10, max 50), `after_filename` (optional cursor)
- Reads `treasury-cache/review-queue/` directory via GitHub API
- Lists files sorted alphabetically by filename (ascending)
- Skips files up to and including `after_filename` (if provided)
- Returns next `limit` files with their content
- Response includes `next_filename` and `has_more` for the DApp cursor
- Also add `GET /dao/contributors` (or reuse existing) to return contributor list for the dropdown

**Files created/modified:**
- `app/controllers/dao_controller.rb` (Rails) or `app/routes/review_queue.py` (FastAPI)
- Tests for pagination, empty queue, file-not-found, cursor stability after deletion

**Acceptance:**
- `GET /dao/review_queue?limit=10` returns first 10 items + `next_filename` + `has_more: true`
- `GET /dao/review_queue?limit=10&after_filename=...` returns next 10 items
- Returns empty array + `has_more: false` when queue is empty
- Cursor still works correctly even if files before it were deleted

---

### PR 3: Edgar — CONTRIBUTION REVIEW EVENT Handler + Cache File Deletion

**Repo:** `sentiment_importer` or `dao_protocol`

**Scope:**
- Register `[CONTRIBUTION REVIEW EVENT]` in Edgar's event catalog
- On receipt:
  1. Parse action field: `"Approve"` or `"Reject"`
  2. Verify RSA signature
  3. **Resolve reviewer email** from the RSA signature via `Contributors Digital Signatures` sheet
  4. Check if signer is governor or Sentinel (reuse existing check)
  5. Delete `treasury-cache/review-queue/<hash_key>.json` via GitHub API
  6. Fire webhook to GAS write-back URL with full payload including `reviewer_email`
  7. Log to Telegram Chat Logs
- Return 403 for non-governor/non-Sentinel signers
- Return 400 if Reject without rejection_reason

**Files created/modified:**
- Event handler in `app/services/` or `app/controllers/dao_controller.rb`
- GitHub API client for file deletion
- Webhook dispatch to GAS URL

**Acceptance:**
- Governor's signed Approve event deletes cache file + fires webhook with tdgs_issued + reviewer_email
- Governor's signed Reject event deletes cache file + fires webhook with rejection_reason + reviewer_email
- Non-governor's signed event returns 403
- Reject without reason returns 400
- Missing hash_key returns 400

---

### PR 4: GAS Write-Back Script

**Repo:** `tokenomics` (GAS script)

**Scope:**
- Create new GAS project (or add to existing scoring script) with web-app endpoint
- `doPost(e)` handler:
  - Parses JSON payload: `hash_key`, `review_action`, `tdgs_issued`, `reviewer_email`, `contributor_name`, `rejection_reason`
  - Opens Scored Chatlogs sheet
  - Finds row by Column K
  - **Double-counting guard:** Check Column F — if terminal status (Rejected, Ignored, Transferred to Main Ledger, Entry Error, Entry Error - Contributor Not Found), skip and return `"already_processed"`
  - **On Approve:**
    - Sets `Column F = "Reviewed"`
    - Sets `Column G (TDGs Issued)` = approved amount
    - Sets `Column M (Reviewer Email)` = reviewer_email
    - Updates `Column A (Contributor Name)` if `contributor_name` provided and differs
  - **On Reject:**
    - Sets `Column F = "Rejected"`
    - Sets `Column O (Rejection Reason)` = rejection_reason
    - Sets `Column M (Reviewer Email)` = reviewer_email
  - Returns JSON `{"status": "ok"}` or `{"status": "already_processed"}`
- Deploy as web app ("Anyone" access for Edgar to POST)

**Files created/modified:**
- `google_app_scripts/<scriptId>/process_review_approval.gs`
- `google_app_scripts/<scriptId>/Code.js` (if needed for doPost routing)

**Acceptance:**
- POST with valid hash_key + approve updates the row
- POST with valid hash_key + reject sets Status = "Rejected" + reason
- POST with already-processed hash_key returns `already_processed`
- POST with invalid hash_key returns 404

---

### PR 5: DApp — Review Queue Page

**Repo:** `dapp_beta`

**Scope:**
- Create `review_queue.html` (new page)
- Fetches queue from `GET /dao/review_queue` with cursor-based infinite scroll
  (tracks `last_filename` instead of `offset`)
- Fetches contributor list from `GET /dao/contributors` (for resolve-failed dropdown)
- Renders card list: contributor (with resolution badge), contribution, rubric, provisioned TDG, date, reporter
- For governors/Sentinels (checked via Edgar identity lookup):
  - Contributor dropdown (if resolve failed)
  - TDG adjust field (pre-filled with Grok's provisioned)
  - Three-action panel: Approve (green), Skip (gray), Reject (red)
  - Rejection reason text area (shown when Reject selected, required)
  - On Approve/Reject: builds `[CONTRIBUTION REVIEW EVENT]` with **minimal payload** (no reviewer email), signs with RSA keypair, submits to Edgar
  - On Skip: removes card from view (no event)
- For non-governors: read-only view with observer notice
- Loading, empty, error states as specified in §9
- Link from DApp navigation

**Files created/modified:**
- `review_queue.html`
- `scripts/edgar_payload_helper.js` (update for new event type)
- Navigation menu update

**Acceptance:**
- Anyone can view the queue with cursor-based infinite scroll
- Governor sees three-action panel + contributor dropdown + TDG field
- Non-governor sees read-only queue with observer notice
- Successful approval removes item from queue (after refresh)
- Successful rejection removes item and sets status to Rejected
- Skip removes item from current view only
- Error states handled gracefully

---

### PR 6: Beta Deploy + UAT

**Scope:**
- Deploy PR 5 to `dapp_beta` (GitHub Pages)
- Deploy PR 4 GAS script (clasp push + deploy)
- Verify end-to-end:
  - U1: Cache generator creates files for pending rows (includes found_in_contributors)
  - U2: Edgar serves queue with cursor-based pagination
  - U3: Governor approves a row → cache file deleted → sheet updated to "Reviewed"
  - U4: Governor rejects a row → cache file deleted → sheet updated to "Rejected" + reason
  - U5: Governor skips a row → cache file stays, row re-appears on reload
  - U6: Non-governor sees queue but cannot approve/reject
  - U7: Resolve-failed row shows dropdown, governor picks correct contributor
  - U8: Double-counting guard prevents re-approval of already-processed row
  - U9: Infinite scroll loads more items with cursor stability
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
- Governor can review, approve, reject, and skip from the DApp

---

## 11. Double-Counting Guard (Critical)

**Problem:** If the GAS write-back script runs after the row is already "Transferred to Main Ledger", it could set Status back to "Reviewed", causing the transfer script to re-process it and award TDGs twice.

**Solution (three layers):**

1. **Cache file deletion:** Once a cache file is deleted from `treasury-cache/review-queue/`, the DApp can no longer surface it. The GitHub Action won't re-generate it because Column N is already populated.

2. **GAS write-back guard:** Before writing, check `Column F (Status)`. If it's a terminal status (Rejected, Ignored, Transferred to Main Ledger, Entry Error, Entry Error - Contributor Not Found), skip. Return `"already_processed"`. See §7 for the full state machine.

3. **Transfer script guard:** The existing `transfer_scored_contributions_to_main_ledger.js` already checks for `"Transferred to Main Ledger"` status and skips those rows. It also checks for existing records in Ledger history by matching contributor + contribution + TDG + date.

---

## 12. Authorization Model

| Action | Who can do it | How enforced |
|--------|---------------|-------------|
| View the queue | Anyone (no auth) | No check needed — read-only data |
| Approve a review | Governor or Sentinel | Edgar verifies RSA signature → resolves email → checks `Governors` tab + `Is Sentinel` column |
| Reject a review | Governor or Sentinel | Same as above |
| Skip a review | Governor or Sentinel | Client-side only (no event sent) |
| Generate cache files | GitHub Action (service account) | GitHub Secrets + Google Sheets API scope |
| Write back to sheet | GAS web app (called by Edgar) | Edgar authenticates via shared secret or IP allowlist |

---

## 13. Edge Cases

| Case | Handling |
|------|----------|
| Grok scores a row as "Unknown" | Status is still "Successfully Completed / Full Provision Awarded" with TDGs Provisioned = 0. Governor can approve (0 TDG), reject, or skip. |
| Cache file exists but row is already reviewed | GitHub Action skips because Column N is populated. If manually deleted, next run re-generates. |
| Edgar goes down | DApp shows error state. Cache files remain in repo — no data loss. |
| GAS write-back fails | Edgar logs the failure. Cache file is already deleted (approval already processed). Manual retry via admin endpoint. |
| Governor approves with 0 TDG | Valid — some contributions may be worth 0. Row becomes "Reviewed" with 0. Transfer script will mark as "Ignored". |
| Two governors approve the same row simultaneously | First one deletes the cache file. Second one gets 404 from Edgar (file not found) → DApp shows "already approved". |
| Governor rejects without reason | Edgar returns 400. DApp shows validation error on the reason field. |
| Resolve-failed contributor — governor picks wrong name | Governor can correct on re-review if caught. Otherwise, the transfer script uses whatever name is in Column A. |
| GitHub Action timeout (6 hours) | Unlikely for this workload. Each run processes at most a few hundred rows. |
| Cursor points to a file that was deleted | Edgar skips missing files silently and continues to the next one. The cursor is just a starting point — if the file is gone, it moves to the next alphabetical file. |

---

## 14. Files to Create / Modify Summary

| PR | Repo | Files | Type |
|----|------|-------|------|
| 1 | `treasury-cache` | `.github/workflows/generate_review_cache.yml`, `scripts/generate_review_cache.py`, `scripts/requirements.txt` | New |
| 2 | `sentiment_importer` or `dao_protocol` | Review queue controller/route + tests + contributors endpoint | New |
| 3 | `sentiment_importer` or `dao_protocol` | Event handler + GitHub API client + webhook dispatch | New/Modify |
| 4 | `tokenomics` | `google_app_scripts/<id>/process_review_approval.gs` | New |
| 5 | `dapp_beta` | `review_queue.html`, `scripts/edgar_payload_helper.js` (maybe), nav update | New/Modify |
| 6 | — | UAT testing (no code changes) | — |
| 7 | `dapp_prod` | Sync from beta | Sync |

---

## 15. RESUME HERE

**Next action:** PR 1 — GitHub Action cache generator for `treasury-cache`.

**Gate:** Governor says "go for it" or "proceed" in this thread.

**One PR per turn rule:** On GO, execute PR 1 ONLY, then stop and report the PR URL. Do NOT chain PRs.
