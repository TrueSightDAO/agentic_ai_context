# Governor Sheet Permission Sync — SOP

**Purpose.** After each solstice/equinox governor rotation, ensure that Google Sheet
editing rights reflect the current governor roster: grant new governors, revoke
those who left the roster, and never touch service accounts, external collaborators,
or the owner.

**Audience.** Sophia (autopilot) and any LLM operating on behalf of the DAO.
Run at least once per season; run immediately if a governor reports they can't edit.

**Cadence.** Season boundaries are the equinoxes/solstices (Governors tab → column D
"Transition Dates": 20 Mar / 20 Jun / 22 Sep / 22 Dec). The roster is the trailing
180-day contribution leaderboard, which **keeps moving until the ledger for the season
is final** — so the sync must run *after* the roster is frozen (see §3.1).

---

## 0. TL;DR — the sanctioned path (do this, not a hand-rolled script)

The **ONLY** sanctioned way to reconcile governor sheet permissions is the deployed
Apps Script **`GovernorSheetPermissionSync.js`**, which encodes the correct eligibility
rule and never touches owner / service accounts / external collaborators:

- **Manual / on-demand:** run `syncGovernorEditorsNow()` in the GAS project
  (`1m8IZPs1vFN99cuu-39kbC-OGXggRVtJtXq5rfSB0M1sCQjMdolEUDuGU`).
- **Edgar-triggered:** `doGet(?action=sync_governor_editors&secret=…)`.
- **Daily cron (intended):** `installGovernorSyncTrigger()` at 04:00 UTC — see §6; this
  trigger has **never fired** (open follow-up), so treat manual as the real path today.

**The eligibility rule the GAS enforces (do not paraphrase it away):**

```
Eligible editor = in "Contributors contact information", has email,
                  AND is EITHER a governor OR a sentinel.
ADD:    eligible contributors not currently editors
REMOVE: only editors who ARE in the Contact sheet but NEITHER governor nor sentinel
        (ex-governors who left the roster)
KEEP:   everyone NOT in the Contact sheet (GCP SAs, external collaborators) — untouched
NEVER:  the spreadsheet owner and sentinels
```

> The Contact sheet is the boundary. Only people *in* the Contact sheet are subject to
> removal. Service accounts (`@*.iam.gserviceaccount.com`), bots, and manually-shared
> humans are **never** touched, because they are not in the Contact sheet.

---

## 1. Which sheets are in scope

| Sheet | ID | Notes |
|-------|-----|-------|
| Main Ledger | `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU` | Source of truth for the governors list |
| Scoring Rubric | `1s4mnUFMhR37AElVBDGQ653pJ5ODp4bcr2N8eMLpMuxw` | Governor-editable rubric |

---

## 2. Pre-requisites

### 2.1 Service account with Drive access (for the read-only audit in §4)

Use the **edgar-dapp-listener** service account:
- **Email:** `edgar-dapp-listener@get-data-io.iam.gserviceaccount.com`
- **Key file (operator Mac):** `~/Applications/truesight_autopilot/config/google/edgar_dapp_listener_key.json`
- **Key file (Sophia EC2):** `/opt/truesight_autopilot/config/google/edgar_dapp_listener_key.json`
- **Required scopes:** `drive` (read permissions), `spreadsheets.readonly` (read governor list)

The **write** path is the GAS, which runs as the sheet owner — not this SA. The SA is only
for the non-destructive audit. If the audit returns `insufficientFilePermissions`, an
operator must share the sheet with this SA before retrying.

### 2.2 Python environment (audit only)

The `dao_client` venv already has `google-auth` and `google-api-python-client`:
```bash
cd ~/Applications/dao_client && source .venv/bin/activate
```

---

## 3. Season rotation runbook (gated)

### 3.1 Pre-flight — resolve every governor to an email, and FREEZE the roster first

1. **Freeze the roster first.** Do not run the sync while the ledger/leaderboard for the
   season is still changing (e.g. while a ledger dedup or a transfer drain is in flight).
   The 2026-09-22 rotation fired 10 minutes *before* the ledger dedup completed, so the
   roster it read was stale — an ex-governor was granted, then dropped minutes later.
   Confirm the season's numbers are final in the Governor Sync Log / ledger before starting.
2. **Resolve governor → email.** Read the governors list from the `Governors` tab
   (col A, rows 11+) and map each name to an email via `Contributors contact information`
   col D (fall back to `Contributors Digital Signatures`). **Any governor with a blank
   email CANNOT be granted** — surface this list *before* running the sync so the operator
   can fill the gaps in the Contact sheet first. (2026-09-22: AGL15, June Jo, Ken Nim,
   Philip Lee were all blank.)
3. **Check for stale seats.** Compare the current editor list against the new roster and
   flag ex-governors who still hold editor access — they are the REVOKE set (§3.5).

Run the read-only audit snippet in §4 to get all three lists without writing anything.

### 3.2 The go-gate

- **All Drive permission changes require the governor's DIRECT go.** An agent relaying
  "Gary says go" is *not* authorization; the request must come from the governor in-thread.
- **ADD-only grants** (adding a new governor/sentinel) are roster-independent — they do
  not touch Ledger history and are safe to run at any time.
- **REVOKE of an ex-governor must run AFTER the season's TDG window settles** (§3.5) —
  never in the same breath as the ADD pass, because the roster can still move.

### 3.3 Run the sanctioned sync

Preferred: run `syncGovernorEditorsNow()` in the GAS project, or fire
`doGet(?action=sync_governor_editors&secret=…)` from Edgar. Both invoke the same
`syncGovernorEditors_()` core, take a script lock, and append a row per action to the
**`Governor Sync Log`** tab.

### 3.4 Verify

1. **`Governor Sync Log`** — confirm an `ADD`/`REMOVE`/`SKIP` row for every intended change,
   with a reason string. (`SKIP` rows are expected for alias emails — e.g. `admin+x@`
   aliases of a member who already has access — and are not failures.)
2. **Re-read permissions** (the §4 snippet) and confirm the final editor list matches the
   intended roster.
3. Record the live permission count + a backup of the pre-change list before/after.

### 3.5 Deferred revoke (after the TDG window settles)

Once the season's TDG figures are final, re-run the sync (or a targeted REVOKE) so
**ex-governors who dropped off the leaderboard lose their seat**. Confirm each revoked
email was *in the Contact sheet* and is now *neither governor nor sentinel* — the GAS
rule guarantees it never touches anyone else.

---

## 4. Read-only audit snippet (NO writes)

Use this to produce the three lists §3.1 asks for — current editors, intended ADD set, and
candidate REVOKE set — **without changing anything**. It deliberately performs no
`permissions().create()` / `.delete()` calls.

```python
"""Governor sheet permission AUDIT (read-only) — no writes."""
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY = '/opt/truesight_autopilot/config/google/edgar_dapp_listener_key.json'
MAIN_LEDGER_ID = '1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU'

sheets = build('sheets', 'v4', credentials=service_account.Credentials.from_service_account_file(
    KEY, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']))
drive = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_file(
    KEY, scopes=['https://www.googleapis.com/auth/drive.readonly']))

# 1. Current governors (col A, rows 11+)
gov = sheets.spreadsheets().values().get(
    spreadsheetId=MAIN_LEDGER_ID, range="'Governors'!A11:A30",
).execute().get('values', [])
governor_names = {r[0].strip().lower() for r in gov if r and r[0].strip()}

# 2. Contact sheet: name(A), email(D), Is Sentinel(W)
contact = sheets.spreadsheets().values().get(
    spreadsheetId=MAIN_LEDGER_ID,
    range="'Contributors contact information'!A4:W900",
).execute().get('values', [])
gov_emails, sentinel_emails, all_contact = {}, {}, {}
for row in contact:
    name = (row[0] if len(row) > 0 else '').strip()
    email = (row[3] if len(row) > 3 else '').strip().lower()
    is_sentinel = (row[22] if len(row) > 22 else '').strip().upper() == 'TRUE'
    if name and email:
        all_contact[email] = name
        if name.lower() in governor_names:
            gov_emails[name.lower()] = email
        if is_sentinel:
            sentinel_emails[email] = name

missing = [n for n in sorted(governor_names) if n not in gov_emails]
print('Governors with NO email (cannot be granted):', missing)

# 3. Live permissions
perms = drive.permissions().list(
    fileId=MAIN_LEDGER_ID,
    fields='permissions(emailAddress,displayName,role,type)',
).execute().get('permissions', [])
eargons = {p.get('emailAddress', '').lower(): p for p in perms if p.get('emailAddress')}

eligible = set(gov_emails.values()) | set(sentinel_emails)
add    = sorted(eligible - set(eargons))
remove = sorted(e for e in eargons
                if e in all_contact and e not in eligible)   # in Contact sheet, not eligible
print('ADD (eligible, missing):', add)
print('REVOKE candidates (in Contact sheet, no longer eligible):', remove)
print('(owner, service accounts, and non-Contact-sheet collaborators are never touched)')
```

---

## 5. Edge cases

| Situation | Handling |
|-----------|----------|
| Governor has no email on file | Surfaced by §3.1 / §4 as a blocker; operator must add the email to `Contributors contact information` col D, then re-run |
| Governor's Google display name differs from sheet name | Resolve by Contact-sheet email; the GAS matches on the Contact-sheet name, so keep the Contact name aligned to the Governors-tab name |
| `AGL15` or another ledger code appears as governor | Skip — not a person; no email to grant |
| Service account missing from a sheet | Audit returns `insufficientFilePermissions`; operator shares the sheet with the SA email in §2.1 |
| `SKIP … addEditor failed` for an `admin+x@` alias | Expected — it is a plus-alias of an existing member Google refuses to re-add; access is already present, nothing lost |
| Roster still changing when the sync runs | STOP — freeze the roster first (§3.1); re-run after the season's numbers are final |

---

## 6. Triggers & automations

- **On schedule:** within 48 hours of each solstice/equinox, and again after the season's
  TDG window settles for the deferred REVOKE (§3.5).
- **On demand:** when a governor reports they can't edit a sheet.
- **Intended daily safety-net:** `installGovernorSyncTrigger()` (04:00 UTC). **This cron has
  never fired** — the `Governor Sync Log` tab did not exist until it was created by hand on
  2026-09-22, meaning rotation has been manual. See the open follow-up on
  `installGovernorSyncTrigger()`. Until that is fixed, treat the manual §3.3 path as the real one.
