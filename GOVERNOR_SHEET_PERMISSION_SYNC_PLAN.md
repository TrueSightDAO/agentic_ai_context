# Governor Sheet-Permission Sync — Implementation Plan

**Status:** Draft · **Created:** 2026-06-28  
**Goal:** Automatically sync the Main Ledger spreadsheet's editor list to the current governor roster, without touching SA (service account) permissions.

---

## 1. Problem

Today, adding a new governor to the Main Ledger Sheet requires manually sharing the sheet via Google's Share UI. When the governor roster changes (quarterly at equinoxes/solstices, computed from the trailing 180-day contribution leaderboard), the sheet permissions fall out of sync — ex-governors retain edit access they shouldn't have, and new governors can't edit.

---

## 2. Data Sources

| Source | Sheet | Column | Purpose |
|--------|-------|--------|---------|
| Main Ledger | `1GE7PUq-...` | — | Target spreadsheet to manage permissions on |
| "Governors" tab | gid=842148543 | Column A, rows 11+ | Current governor names (leaderboard-derived) |
| "Contributors contact information" | gid=1460794618 | Col A = Name, Col D = Email | Map governor names → email addresses |
| Script properties | — | `GOVERNOR_SYNC_SA_EMAILS` (comma-sep) | SA/agent emails to NEVER remove |

---

## 3. Safety Philosophy

The script **only removes editors it previously added itself**, tracked via the "Governor Sync Log" tab. This avoids the need to catalog every SA, GitHub Actions bot, or GCP service account.

- **ADD:** governor email not currently an editor → `addEditor()`
- **REMOVE:** only editors previously added BY THIS SCRIPT (tracked in Governor Sync Log `ADD` rows) who are no longer governors → `removeEditor()`
- **NEVER remove:** the spreadsheet owner, any `*.iam.gserviceaccount.com` / `*.gserviceaccount.com` address, `admin+*` agent aliases, or any editor we didn't add ourselves — even if they're not governors.

Patterns auto-detected as protected (never removed):
| Pattern | Example |
|---------|---------|
| `@*.iam.gserviceaccount.com` | `butterfly-effect-club@get-data-io.iam.gserviceaccount.com` |
| `@*.gserviceaccount.com` | older GCP service accounts |
| `admin+*` | `admin+sophia@truesight.me` |
| `admin@truesight.me` | master autopilot |
| Spreadsheet owner | detected at runtime via `Spreadsheet.getOwner()` |

---

## 4. Algorithm

```
FOR the Main Ledger spreadsheet:
  1. READ "Governors" tab (col A, rows 11+) → governor names
  2. READ "Contributors contact information" (col A=name, col D=email) → name→email map
  3. RESOLVE governor name → email from contact sheet
     → Names without email are logged (warn) and skipped
  4. GET current editors via Spreadsheet.getEditors()
  5. READ "Governor Sync Log" tab → find emails previously ADD-ed by this script
     → Only these are eligible for removal
  6. DETERMINE
     a. Editors to ADD = governor_emails NOT in current_editors
     b. Editors to REMOVE = previously-added-by-us emails NOT in governor_emails,
        NOT matching SA patterns, NOT owner
  7. APPLY: addEditor() for each ADD, removeEditor() for each REMOVE
  8. LOG changes to "Governor Sync Log" tab and Logger
```

**Key difference from v1:** Step 5 reads the log to build a safelist. Only editors previously added by this script are ever removed. Unknown SAs, bots, and manually shared humans are completely untouched.

---

## 5. GAS Implementation Checklist

### PR1: Governor Sheet-Permission Sync Script

- [ ] Create `GovernorSheetPermissionSync.js` in GAS project `1m8IZPs...`
- [ ] Read "Governors" tab names (col A, rows 11+)
- [ ] Read "Contributors contact information" (col A=name, col D=email)
- [ ] Map governor names → emails (skip names without email, log warnings)
- [ ] Build protected-accounts set from script property `GOVERNOR_SYNC_SA_EMAILS` + runtime owner
- [ ] Compute add/remove diffs
- [ ] Apply changes: `addEditor()`, `removeEditor()`
- [ ] Log to "Governor Sync Log" tab (timestamp, action, email, reason)
- [ ] Create `installGovernorSyncTrigger()` for daily UTC cron
- [ ] Create `syncGovernorEditorsNow()` for manual execution
- [ ] Wire `doGet(?action=sync_governor_editors)` for Edgar-triggered sync

### PR2: Deploy & Test

- [ ] Set `GOVERNOR_SYNC_SA_EMAILS` script property with SA email list
- [ ] Deploy web app version
- [ ] Run `syncGovernorEditorsNow()` manually, verify Log tab
- [ ] Verify editor list in Share dialog matches expectations
- [ ] Verify SA accounts still have edit access

### PR3: Wire Into Governor Rotation Cadence

- [ ] After each equinox/solstice governor recomputation, trigger sync
- [ ] Daily safety-net cron: `installGovernorSyncTrigger()`

---

## 6. Log Tab Schema

The "Governor Sync Log" tab (auto-created if not present):

| Column | Field | Example |
|--------|-------|---------|
| A | Timestamp | `2026-06-28T22:30:00Z` |
| B | Action | `ADD` / `REMOVE` / `SKIP` |
| C | Email | `kirsten@kikiscocoa.com` |
| D | Governor Name | `Kirsten Ritschel` |
| E | Reason | `new governor, not yet editor` / `no longer governor` / `no email in contact sheet` |

---

## 7. Trigger Flow

```
Equinox/Solstice
  ↓
Governors tab leaderboard recalculates (formula-driven)
  ↓
Edgar calls doGet(?action=sync_governor_editors)
  ↓
GAS syncs editor list
  ↓
Governor Sync Log updated
```

Plus daily safety-net cron at 04:00 UTC (runs even if Edgar ping fails).

---

## 8. Edge Cases & Safeguards

- **Governor name with no email in Contact sheet:** Log warning, skip (don't remove, don't add)
- **SA email appears in governor list:** Never remove, even if not currently a governor
- **Spreadsheet owner:** Never remove (detected at runtime)
- **Concurrent sync:** Script lock prevents overlapping runs
- **Empty governors tab:** Abort with log entry (no removals)
- **New governor email already an editor but with different permissions:** No-op for add (don't downgrade viewer→editor until confirmed)
