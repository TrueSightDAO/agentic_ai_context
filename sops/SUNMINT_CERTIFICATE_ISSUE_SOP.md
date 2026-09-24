# SunMint Certificate — Issue SOP

**Audience:** Sophia Truesight and any autopilot agent issuing a certificate for a cacao
bag, a planted tree, or a sponsored planting.
**Purpose:** Teach-once procedure. The QR image source, the build rules, and the acceptance
gate are fixed here so no governor has to re-explain them per issue.
**Status:** Draft · **Last updated:** 2026-09-24 · **Author:** Sophia Truesight
(admin+sophia@truesight.me)

> Governor directive (Gary Teh, 2026-09-24): *"Make sure we have an SOP in place for future
> issues of SunMint certificate. I don't want to have to teach you every time where to find the
> right QR code to embed in the certificate. You can always find it in our registry."*

---

## 1. The one rule

**Never invent, generate, or re-encode a QR code. Always embed the registry's own image.**

The QR on a certificate is not decorative — it is the asset's pointer into the DAO registry. It
must be *the registry's image*, so that the printed artifact and the digital record cannot diverge.

---

## 2. Where the QR lives (the registry)

Canonical asset registry: **`TrueSightDAO/lineage-assets`** (public).

| What | Path / URL |
|---|---|
| Per-asset provenance manifest | `qrs/<qr-id>.json` |
| **Canonical QR image** | `pngs/<qr-id>.png` — 450×350, QR + "scan to verify" caption |
| Registry index | `qrs_index.json` |
| Schema | `SCHEMA.md` |

For **any** `qr_id`, the image is derivable without a lookup:

```
https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/pngs/<qr-id>.png
https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/qrs/<qr-id>.json
```

The same asset is also reachable by humans at `https://truesight.me/qr/?id=<qr-id>` (the
registry profile page renders the PNG above) and resolves via
`https://edgar.truesight.me/agroverse/qr-code-check?qr_code=<qr-id>` (302 → landing page).

**The manifest is the source of truth for:** `status`, `lineage` (farm/state/country/harvest/sku),
`current_holder`, `current_landing_page`, `qr_image_url`, `scan_target`, `edgar_resolve_url`.

---

## 3. Do NOT

1. **Do not generate a new QR** with the `qrcode` library or any encoder — even if the payload
   would be identical. Use the registry pixels.
2. **Do not point at `qr_codes/*.png`** — that path is stale and **404s**. (Known gap: at least
   Main Ledger row 1575's `QR code location` cell points there. File/see `OPEN_FOLLOWUPS.md`.)
3. **Do not resize with NEAREST at a non-integer ratio.** A registry module is ~4.918 px wide
   (49 modules across 241 px). Downscaling 261→129 px smears every module and the QR **stops
   decoding entirely**. This is a real failure hit on 2026-09-24 — see §6.
4. **Do not trust the sheet over the registry** (or vice versa) without reconciling — see §7.

---

## 4. Procedure (deterministic)

1. **Resolve the manifest.** Fetch `qrs/<qr-id>.json`. Read `status`, `lineage`,
   `current_landing_page`, `edgar_resolve_url`. Confirm the asset is what you think it is.
2. **Fetch the image.** `pngs/<qr-id>.png`; assert **HTTP 200**.
3. **Decode it.** Assert the decoded payload **== the manifest's `edgar_resolve_url`** for that
   `qr_id`. If it does not match, STOP — do not build.
4. **Find the module grid `N`.** Probe N in 21..58: sample N×N module centres, re-render, decode;
   the N that decodes is the true grid (**49** for this family).
5. **Render at an INTEGER scale.** Expand the N×N grid by an integer factor; keep a quiet zone
   of **≥4 modules**.
6. **Paste onto the certificate.**
7. **Verify the FINAL artifact.** Re-decode the finished certificate (PNG and the 300 dpi PDF
   render). It MUST decode to the exact `edgar_resolve_url`.
8. **Prove provenance, not just payload.** Sample the cert's QR back to N×N and diff against the
   registry modules. Require **100% module match**.

---

## 5. Acceptance checklist (all required before sending)

- [ ] QR image fetched from `lineage-assets/pngs/<qr-id>.png` (not generated, not `qr_codes/`)
- [ ] Registry PNG decodes to the manifest's `edgar_resolve_url`
- [ ] Module grid determined; rendered at integer scale with a ≥4-module quiet zone
- [ ] **Final certificate decodes** to the exact registry URL
- [ ] **100% module-for-module match** vs the registry PNG
- [ ] Printed issuer name = **`Sophia Truesight`** (registered identity; only the org byline is `TrueSight DAO`)
- [ ] Signature mark appended from `signature_assets/sophia_truesight/`
- [ ] Lineage / status language on the cert matches the registry once §7 conflicts are resolved

---

## 6. Copy-paste: fetch + extract + verify

```python
from PIL import Image
from pyzbar.pyzbar import decode
import numpy as np, urllib.request

QR = "2024OSCAR_CB_20260620_1"           # <- the qr_id
BASE = "https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main"
url = f"{BASE}/pngs/{QR}.png"

urllib.request.urlretrieve(url, "/tmp/reg.png")
im = Image.open("/tmp/reg.png").convert("RGB")
d  = decode(im)[0]
assert QR in d.data.decode(), "registry PNG payload mismatch"

# true module grid (49 for this family) -> exact module bitmap
r = d.rect
qr = im.crop((r.left, r.top, r.left + r.width, r.top + r.height)).convert("L")
N, a = 49, np.array(qr).astype(float)
sy, sx = a.shape[0] / N, a.shape[1] / N
grid = np.array([[a[int((j+.5)*sy), int((i+.5)*sx)] < 128 for i in range(N)]
                 for j in range(N)], bool)

# render at INTEGER scale + quiet zone, paste, then re-decode the FINAL cert
# scale = px // (N + 2*quiet); NEAREST only, never a fractional ratio
```

**Verification of the finished certificate:**

```python
cert = Image.open("/tmp/certificate.png").convert("RGB")
rc   = decode(cert)[0]                    # MUST decode
assert QR in rc.data.decode()
cq = cert.crop((rc.left, rc.top, rc.left + rc.width, rc.top + rc.height)).convert("L")
b  = np.array(cq).astype(float)
sy, sx = b.shape[0] / N, b.shape[1] / N
g2 = np.array([[b[int((j+.5)*sy), int((i+.5)*sx)] < 128 for i in range(N)]
               for j in range(N)], bool)
assert (g2 == grid).mean() == 1.0          # 100% module match
```

---

## 7. Reconciling registry vs. other sinks

Data can disagree between the registry manifest, the Main Ledger sheet, and Edgar's live resolve.

**Ground-truth precedence:**

1. **Edgar live resolve** (`/agroverse/qr-code-check?qr_code=<id>` → final URL + `status=`) — what a
   scanner actually sees.
2. **Main Ledger / SunMint sheet** — the operational state.
3. **`lineage-assets` manifest** — the provenance record.

**Known open conflict (2026-09-24):** for `2024OSCAR_CB_20260620_1` the manifest says
`status: SOLD` while the sheet + live resolve say `ASSIGNED_TO_TREE`. **Resolve before framing a
certificate as "guardian" vs "sold".** Do not silently pick one.

---

## 8. Signature block

- **Printed name:** `Sophia Truesight` — the registered DAO identity. Never `TrueSight` in the
  personal name (only the org byline reads `TrueSight DAO`).
- **Mark:** `signature_assets` (private) → `sophia_truesight/sophia_truesight_signature_mark.png`,
  a *gestural* mark (deliberately not legible as text; the printed name carries legibility).
- The signature is a **graphic mark**, **not** a cryptographic attestation.

---

## 9. Related

- `SUNMINT_E2E_RUNBOOK.md` — the full tree pipeline (email link → planting → monitoring → attestation)
- `AGROVERSE_QR_CODE_BATCH_GENERATION.md` — QR id naming convention
- `LEDGER_CONVERSION_AND_REPACKAGING.md` — ledger/repackaging mechanics
- `OPEN_FOLLOWUPS.md` — the `qr_codes/*.png` stale-path gap
