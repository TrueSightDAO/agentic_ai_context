# Manual Email Registration SOP

**Purpose:** Register email addresses collected in-person (events, booths, verbal interactions) into the DAO's newsletter subscriber system, tied to a QR code batch.

**Last updated:** 2026-06-12

---

## 1. When to use this

When a governor provides email addresses from people who interacted at an event but didn't scan the QR code themselves. This simulates the same flow as if they had scanned the QR and opted in.

## 2. Registration endpoint

Use the GAS web app at:

```
GET /exec?email_address=<EMAIL>&subscribe=true&source=<SOURCE>&qr_code=<QR_CODE>
```

**Parameters:**

| Parameter | Value | Example |
|-----------|-------|--------|
| `email_address` | The person's email | `k.johnsoki@gmail.com` |
| `subscribe` | `true` | `true` |
| `source` | Event + QR code reference | `SF+Tech+Fest+2026` |
| `qr_code` | The event's QR code batch | `SFTF_FR_20260612_2` |

**Full URL example:**
```
https://script.google.com/macros/s/AKfycbxigq4-J0izShubqIC5k6Z7fgNRyVJLakfQ34HPuENiSpxuCG-wSq0g-wOAedZzzgaL/exec?email_address=k.johnsoki@gmail.com&subscribe=true&source=SF+Tech+Fest+2026&qr_code=SFTF_FR_20260612_2
```

## 3. Verification

After registering, check the subscriber was added in the Main Ledger:
- Sheet: `Agroverse News Letter Subscribers`
- Columns: Email, Status (should be CONFIRMED), Created Date, Imported Date, Source (should be `qr:<QR_CODE>`)

## 4. Context for future AI incarnations

When a governor says "register these emails" or "add these people who gave their emails":

1. Use the GAS web app endpoint above — one request per email
2. Set `subscribe=true` and `source` to the event name
3. Tie to the event's QR code via `qr_code` parameter
4. Verify they appear in the sheet as CONFIRMED
5. The emails will be picked up by the Email360 retention loop automatically

**Key lesson:** The web app's `subscribe` parameter handles both updating the QR code row with the email AND adding the person to the newsletter subscribers sheet in one call.
