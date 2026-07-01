# Governor Sheet Permission Sync — SOP

**Purpose.** After each solstice/equinox governor rotation, ensure that Google Sheet
editing rights reflect the current governor roster: revoke non-governors, grant
new governors, and never touch service accounts or the owner.

**Audience.** Sophia (autopilot) and any LLM operating on behalf of the DAO.
Run at least once per season; run immediately if a governor reports they can't edit.

---

## 1. Which sheets are in scope

| Sheet | ID | Notes |
|-------|-----|-------|
| Main Ledger | `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU` | Source of truth for governors list |
| Scoring Rubric | `1s4mnUFMhR37AElVBDGQ653pJ5ODp4bcr2N8eMLpMuxw` | Governor-editable rubric |

To add a sheet: append its ID to the `FILES` dict in the audit script below.

---

## 2. Pre-requisites

### 2.1 Service account with Drive admin access

Use the **edgar-dapp-listener** service account:
- **Email:** `edgar-dapp-listener@get-data-io.iam.gserviceaccount.com`
- **Key file (operator Mac):** `~/Applications/truesight_autopilot/config/google/edgar_dapp_listener_key.json`
- **Key file (Sophia EC2):** `/opt/truesight_autopilot/config/google/edgar_dapp_listener_key.json`
- **Required scopes:** `drive` (read-write on permissions), `spreadsheets.readonly` (read governor list)

This SA must have **writer or owner** access on every sheet in scope.
If the audit script returns `insufficientFilePermissions`, an operator must
share the sheet with this SA before retrying.

### 2.2 Python environment

The `dao_client` venv already has `google-auth` and `google-api-python-client`:
```bash
cd ~/Applications/dao_client && source .venv/bin/activate
```

---

## 3. Audit + remediation (one script)

Run this Python script. It does three things: (a) reads current governors,
(b) lists each sheet's permissions, (c) revokes non-governor writers and
grants missing governors.

```python
"""Governor sheet permission sync — audit + remediate in one pass."""
import os, sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = (
    os.path.expanduser(
        '~/Applications/truesight_autopilot/config/google/edgar_dapp_listener_key.json'
    )
)

from google.oauth2 import service_account
from googleapiclient.discovery import build

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MAIN_LEDGER_ID = '1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU'
GOVERNORS_RANGE = "'Governors'!A11:A25"
CONTACT_RANGE = "'Contributors contact information'!A4:D200"
SIGS_RANGE = "'Contributors Digital Signatures'!A2:F2000"

FILES = {
    'Main Ledger': MAIN_LEDGER_ID,
    'Scoring Rubric': '1s4mnUFMhR37AElVBDGQ653pJ5ODp4bcr2N8eMLpMuxw',
}

# Known email mappings for governors whose sheet display names don't match.
# Keep this updated when a governor's email changes.
KNOWN_EMAILS = {
    'jacob nelan': 'jakenelan@gmail.com',
    'kirsten ritschel': 'kirsten@kikiscocoa.com',
    'gary teh': 'garyjob@agroverse.shop',
}

# ---------------------------------------------------------------------------
# Step 1 — Fetch current governor names
# ---------------------------------------------------------------------------
drive_creds = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/drive'],
)
sheets_creds = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'],
)
drive = build('drive', 'v3', credentials=drive_creds)
sheets = build('sheets', 'v4', credentials=sheets_creds)

gov_result = sheets.spreadsheets().values().get(
    spreadsheetId=MAIN_LEDGER_ID, range=GOVERNORS_RANGE,
).execute()

governor_names_lower = set()
for row in gov_result.get('values', []):
    name = row[0].strip().lower() if row else ''
    if name and name != 'governor':
        governor_names_lower.add(name)

print(f'Governors ({len(governor_names_lower)}): {sorted(governor_names_lower)}')

# ---------------------------------------------------------------------------
# Step 2 — Resolve governor emails
# ---------------------------------------------------------------------------
def resolve_emails():
    """Merge emails from contact info, signatures, and KNOWN_EMAILS."""
    emails = dict(KNOWN_EMAILS)

    # Contributors contact information (col A=name, col D=email)
    contact = sheets.spreadsheets().values().get(
        spreadsheetId=MAIN_LEDGER_ID, range=CONTACT_RANGE,
    ).execute()
    for row in contact.get('values', []):
        name = row[0].strip().lower() if len(row) > 0 and row[0] else ''
        email = row[3].strip().lower() if len(row) > 3 and row[3] else ''
        if name and email:
            emails[name] = email

    # Contributors Digital Signatures (col A=name, col F=email)
    sigs = sheets.spreadsheets().values().get(
        spreadsheetId=MAIN_LEDGER_ID, range=SIGS_RANGE,
    ).execute()
    for row in sigs.get('values', []):
        name = row[0].strip().lower() if len(row) > 0 and row[0] else ''
        email = row[5].strip().lower() if len(row) > 5 and row[5] else ''
        if name and email:
            emails[name] = email

    return emails

governor_emails = resolve_emails()

missing_emails = [n for n in sorted(governor_names_lower) if n not in governor_emails]
if missing_emails:
    print(f'\n⚠ Governors with NO known email — cannot grant access:')
    for n in missing_emails:
        print(f'  - {n}')

# ---------------------------------------------------------------------------
# Step 3 — Audit + remediate each file
# ---------------------------------------------------------------------------
for label, file_id in FILES.items():
    print(f'\n=== {label} ===')

    perms = drive.permissions().list(
        fileId=file_id,
        fields='permissions(id,emailAddress,displayName,role,type)',
    ).execute()

    existing_emails = {}  # email → role
    for p in perms.get('permissions', []):
        email = p.get('emailAddress', '').lower()
        existing_emails[email] = {
            'id': p['id'],
            'role': p.get('role', ''),
            'type': p.get('type', ''),
            'name': p.get('displayName', ''),
        }

    # --- Revoke non-governor writers ---
    for email, info in existing_emails.items():
        role = info['role']
        ptype = info['type']
        is_sa = 'gserviceaccount.com' in email
        is_owner = role == 'owner'

        if role not in ('writer', 'owner'):
            continue
        if is_owner or is_sa:
            continue

        # Check if this email belongs to a current governor
        name_match = info['name'].lower()
        is_gov = (
            name_match in governor_names_lower
            or any(ge == email for ge in governor_emails.values())
        )
        if not is_gov:
            print(f'  REVOKE: {info["name"]} ({email})')
            drive.permissions().delete(
                fileId=file_id, permissionId=info['id']
            ).execute()
            print(f'    ✓ Revoked')

    # --- Grant missing governors ---
    for gov_name in sorted(governor_names_lower):
        email = governor_emails.get(gov_name, '')
        if not email or '@' not in email:
            continue
        if email.lower() in existing_emails:
            continue  # already has access

        print(f'  GRANT: {gov_name} ({email})')
        body = {
            'role': 'writer',
            'type': 'user',
            'emailAddress': email,
        }
        drive.permissions().create(
            fileId=file_id, body=body, sendNotificationEmail=False,
        ).execute()
        print(f'    ✓ Granted')

    # --- Final summary ---
    perms = drive.permissions().list(
        fileId=file_id,
        fields='permissions(emailAddress,displayName,role,type)',
    ).execute()
    writers = [
        p for p in perms.get('permissions', [])
        if p['role'] in ('writer', 'owner')
        and not ('gserviceaccount.com' in p.get('emailAddress', ''))
        and p['role'] != 'owner'
    ]
    print(f'  Remaining non-SA writers: {len(writers)}')

print('\n✅ Sync complete.')
```

---

## 4. Edge cases

| Situation | Handling |
|-----------|----------|
| Governor has no email on file | Printed as ⚠ warning; operator must add email to `Contributors contact information` col D, then re-run |
| Governor's Google display name differs from sheet name | `KNOWN_EMAILS` dict bridges the gap; update it when a new mismatch appears |
| AGL15 or other ledger code appears as governor | Skip — not a person; no email to grant |
| Service account missing from a sheet | Script fails with `insufficientFilePermissions`; operator shares the sheet with the SA email listed above |
| Sophia calls the script | She sources her venv: `source .venv/bin/activate` from `~/Applications/dao_client`, adjusts the creds path to `/opt/truesight_autopilot/config/google/edgar_dapp_listener_key.json`, and runs |

---

## 5. Trigger

- **On schedule:** within 48 hours of each solstice/equinox (governor rotation dates)
- **On demand:** when a governor reports they can't edit a sheet
- **Sophia/fix-agent:** `fix_agent.py` can invoke this as a tool using `ssh_run` with the python command above
