# Governor Sheet-Permission Sync — Implementation Plan

**Status:** Deployed · **Last updated:** 2026-06-28  
**GAS project:** `1m8IZPs1vFN99cuu-39kbC-OGXggRVtJtXq5rfSB0M1sCQjMdolEUDuGU`  
**Script:** `GovernorSheetPermissionSync.js`  
**Goal:** Automatically sync the Main Ledger spreadsheet's editor list to the current governor roster, without touching GCP SAs, external collaborators, or the owner.

**Important (2026-06-30):** The `Governors` tab now has an **`ALLOW SENTINELS`** boolean toggle at `E12` (label at `D12`). When `E12 = FALSE`, the leaderboard formula in A11 **excludes** sentinels from column A. However, this GAS independently reads `Contributors contact information` column W for sentinel editor grants (lines 126-151) — sentinels still get editor access even when excluded from formal governorship. See `tokenomics/SCHEMA.md` § Governors for the full formula documentation.

---

## 1. Problem

Today, adding a new governor to the Main Ledger Sheet requires manually sharing the sheet via Google's Share UI. When the governor roster changes (quarterly at equinoxes/solstices, computed from the trailing 180-day contribution leaderboard), the sheet permissions fall out of sync — ex-governors retain edit access they shouldn't have, and new governors can't edit.

---

## 2. Data Sources

| Source | Sheet | Column | Purpose |
|--------|-------|--------|---------|
| Main Ledger | `1GE7PUq-...` | — | Target spreadsheet |
| "Governors" tab | gid=842148543 | Col A, rows 11+ | Current governor names (leaderboard-derived) |
| "Contributors contact information" | gid=1460794618 | Col A=Name, Col D=Email, Col W=Is Sentinel | Map names → emails + sentinel flag |

---

## 3. Final Rule (v5)

```
Eligible editor = in "Contributors contact information", has email,
                  AND is EITHER a governor OR a sentinel.

ADD:    eligible contributors not currently editors
REMOVE: only editors whose email IS in the Contact sheet but are
        NEITHER governor NOR sentinel (ex-governors who left the roster)
KEEP:   everyone NOT in the Contact sheet (GCP SAs, external
        collaborators, IAM service accounts) — completely untouched
NEVER:  the spreadsheet owner; sentinels
```

**Key insight:** The Contact sheet is the boundary. Only people IN the Contact sheet are subject to removal. Everything outside it — GCP IAM service accounts (`@*.iam.gserviceaccount.com`), GitHub Actions bots, external collaborators, manually-shared humans — is never touched.

---

## 4. Simulation Result (2026-06-28)

With the v5 rule applied to the current editor list (18 editors including GCP SAs, external collaborators, governors):

| | Count | Details |
|---|---|---|
| **Kept** | 18 | All GCP SAs (`butterfly-effect-club@get-data-io.iam.gserviceaccount.com`, etc.), external collaborators (`ed@hackerdojo.com`, `emelinjung@gmail.com`, etc.), governors with email in Contact sheet |
| **Removed** | 0 | No ex-governors currently in the Contact sheet as editors |
| **Added** | 5 | `garyjob@gmail.com` (Gary Teh, governor), `admin+claude@truesight.me`, `admin+deepseek@truesight.me`, `admin+kimi@truesight.me`, `admin+sophia@truesight.me` (sentinel agents) |

---

## 5. GAS Implementation Checklist

- [x] Create `GovernorSheetPermissionSync.js` in GAS project `1m8IZPs...`
- [x] Read "Governors" tab names (col A, rows 11+)
- [x] Read "Contributors contact information" (col A=name, col D=email, col W=Is Sentinel)
- [x] Map governor names → emails; map sentinel names → emails
- [x] Only remove editors whose email IS in the Contact sheet but not eligible
- [x] Never remove: owner, sentinels, anyone not in Contact sheet
- [x] Apply changes: `addEditor()`, `removeEditor()`
- [x] Log to "Governor Sync Log" tab (timestamp, action, email, reason)
- [x] `installGovernorSyncTrigger()` for daily UTC 04:00 cron
- [x] `syncGovernorEditorsNow()` for manual execution
- [x] Wire `doGet(?action=sync_governor_editors)` for Edgar-triggered sync
- [x] Deploy to GAS

---

## 6. Log Tab Schema

The "Governor Sync Log" tab (auto-created if not present):

| Column | Field | Example |
|--------|-------|---------|
| A | Timestamp | `2026-06-28T22:30:00Z` |
| B | Action | `ADD` / `REMOVE` / `SKIP` |
| C | Email | `kirsten@kikiscocoa.com` |
| D | Name | `Kirsten Ritschel` |
| E | Reason | `governor — added as editor` / `in Contact sheet but neither governor nor sentinel` |

---

## 7. Trigger Flow

```
Equinox/Solstice
  ↓
Governors tab leaderboard recalculates (formula-driven)
  ↓
Edgar calls doGet(?action=sync_governor_editors&secret=...)
  ↓
GAS syncs editor list
  ↓
Governor Sync Log updated
```

Plus daily safety-net cron at 04:00 UTC (runs even if Edgar ping fails).

---

## 8. Related Changes (2026-06-28 Session)

- **DaoMembersCache.js** — now includes ALL Contact sheet names (406+ contributors, 6 sentinels), not just signature-holders. Enables sentinel section on `truesight.me/members.html`.
- **REVIEW_QUEUE_SOP.md** — automatable SOP for reviewing scored chatlogs: name resolution (dao_members.json → lineage-credentials), auto-compute TDG from event Amount, auto-approve via Deep Seek RSA key.
- **Review queue** — ~475 items approved, ~15 rejected, ~10 skipped. Deep Seek signed all `[CONTRIBUTION REVIEW EVENT]` submissions via `POST /dao/submit_contribution_review`.
