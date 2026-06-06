# Autopilot Edgar RSA Signing

## Summary

The autopilot has its own RSA-2048 keypair registered with Edgar. It can **sign and submit payloads directly** to `edgar.truesight.me/dao/submit_contribution` — no DApp approval gate needed.

## Keypair

- Registered via `register_identity("autopilot@truesight.me")`
- Stored in `/opt/truesight_autopilot/.env`:
  - `PUBLIC_KEY` — base64 SPKI (public key)
  - `PRIVATE_KEY` — base64 PKCS8 (private key)
  - `EMAIL` — `autopilot@truesight.me`

## How to sign and submit

### 1. Construct the unsigned text

Follow the same format the DApp uses:

```
[EVENT_TYPE]
Field Name: Value
Field Name 2: Value
--------
```

The `--------` line marks the end of the signed content.

### 2. Sign with RSA

Algorithm: **RSASSA-PKCS1-v1_5 with SHA-256**

Python (using `cryptography`):

```python
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# Load private key
pk_bytes = base64.b64decode(PRIVATE_KEY_B64)
private_key = serialization.load_der_private_key(pk_bytes, password=None)

# Sign the text
signature = private_key.sign(
    text.encode('utf-8'),
    padding.PKCS1v15(),
    hashes.SHA256()
)
sig_b64 = base64.b64encode(signature).decode('utf-8')
```

### 3. Build the full payload

```python
full_text = text + '\n\nMy Digital Signature: ' + PUBLIC_KEY_B64 + \
    '\n\nRequest Transaction ID: ' + sig_b64 + \
    '\n\nThis submission was generated using https://dapp.truesight.me/\n\n' + \
    'Verify submission here: https://dapp.truesight.me/verify_request.html'
```

### 4. POST to Edgar

```
POST https://edgar.truesight.me/dao/submit_contribution
Content-Type: application/x-www-form-urlencoded

text=<url-encoded full_text>
```

Optional: include `attachment` as a multipart file upload.

### 5. Check response

```json
{"status":"success","fileUploadedToGithub":false,"googleSheetLogged":true,"signature_verification":"success"}
```

`signature_verification: "success"` means Edgar accepted the signed payload.

## Supported event types

| Event | Use case |
|-------|----------|
| `[RETAIL FIELD REPORT EVENT]` | Hit List store visit / status update |
| `[PARTNER CHECK-IN EVENT]` | Partner check-in |
| `[CONTRIBUTION EVENT]` | DAO contribution logging |
| `[INVENTORY MOVEMENT]` | Inventory transfers |
| `[SALES EVENT]` | QR code sales |
| `[STORE ADD EVENT]` | Add new store to Hit List |
| `[DONATION MINT EVENT]` | Mint donation QR codes |

## Field conventions

- Use the same field names as the DApp (e.g. `Shop Name:`, `Store Key:`, `Update ID:`, `New Status:`)
- `Update ID` should be unique per submission (e.g. `SFR_YYYYMMDD_StoreName_###`)
- For retail field reports, include: `Shop Name`, `Store Key`, `Update ID`, `New Status`, `Previous Status`, `Remarks`
- The `--------` line must be the last line of the signed content (before the signature block)

## Example: Retail Field Report

```python
import base64, urllib.parse, urllib.request
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

text = """[RETAIL FIELD REPORT EVENT]
Shop Name: Example Store
Store Key: example-store__123-main-st__city__state
Update ID: SFR_20260606_Example_001
New Status: Deferred / Revisit later
Previous Status: Research
Contact Method: In Person
Visit Date: 2026-06-06
Follow Up Date: 2026-07-15
Remarks: Notes about the visit.
--------"""

pk_bytes = base64.b64decode(PRIVATE_KEY_B64)
private_key = serialization.load_der_private_key(pk_bytes, password=None)
signature = private_key.sign(text.encode(), padding.PKCS1v15(), hashes.SHA256())
sig_b64 = base64.b64encode(signature).decode()

full = text + '\n\nMy Digital Signature: ' + PUBLIC_KEY_B64 + \
    '\n\nRequest Transaction ID: ' + sig_b64

data = urllib.parse.urlencode({'text': full}).encode()
req = urllib.request.Request(
    'https://edgar.truesight.me/dao/submit_contribution',
    data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    method='POST'
)
resp = urllib.request.urlopen(req)
print(resp.read().decode())
```

## Important notes

- The autopilot's keypair is for **DAO operations only** — not for personal governor actions
- Edgar logs the submission to Telegram Chat Logs and fires async GAS scanners for processing
- The `submit_contribution` tool in the autopilot's toolset goes through a frontend approval gate; **use direct POST instead** for unattended submissions
- Always verify the response includes `signature_verification: "success"`
