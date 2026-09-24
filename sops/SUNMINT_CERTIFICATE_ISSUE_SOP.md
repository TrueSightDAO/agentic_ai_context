# SOP — Issuing a SunMint “Certificate of Tree Guardianship”

**Owner:** Sophia Truesight (autopilot). **Governor:** Gary.
**Origin:** thread 35189, 2026-09-24 — *“Make sure we have an SOP in place for future
issues of SunMint certificate… You can always find it in our registry.”*
**Revision:** rev2 (2026-09-24) — corrects the QR-embedding method (§3, §11).

---

## 1. The one rule

**Never invent, generate, or re-encode a QR. Always embed the registry's OWN image.**

The registry is the single source of truth for the QR image. If you find yourself
constructing a QR (qrcode lib, PIL, an online generator, a re-draw), **stop** — you
are doing it wrong.

## 2. Where the QR lives (the lookup — do not search per-issue)

For any Agroverse/SunMint QR id (e.g. `2024OSCAR_CB_20260620_1`):

| Artifact | Path |
|---|---|
| Canonical **image** | `TrueSightDAO/lineage-assets` → `pngs/<qr_id>.png` |
| **Manifest** (metadata) | `TrueSightDAO/lineage-assets` → `qrs/<qr_id>.json` |
| Derived web view | `https://truesight.me/qr/?id=<qr_id>` |

Raw URL to embed / fetch:

```
https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/pngs/<qr_id>.png
```

This is generic — the repo holds ~1,000 `qrs/` + ~1,000 `pngs/` entries keyed by id, so
the image can be derived for **any** id without a search.

**Do NOT use `qr_codes/*.png`** — that is a stale path and 404s.

## 3. How to embed it (the method that works)

**Verified empirically (60+ variants tested) — use THIS:**

1. Fetch the registry PNG.
2. Decode it (`pyzbar`) and confirm the payload contains the expected `qr_id`. **Abort if not.**
3. Crop the **detector's own bounding rect**, **unchanged**. Do **not** pad or nudge it —
   a 1-px shift changes the module phase and breaks decoding.
4. Add a synthetic **quiet zone** ≥ 4 modules (white border) around the crop.
5. Re-confirm the quiet-zoned crop decodes.
6. Resize that crop to the tile size the layout needs, trying resamplers in order
   `LANCZOS → BOX → NEAREST`, and **accept the first tile that decodes**.

> **Why not reconstruct a module grid?** Sampling the registry image to its true
> 49×49 module grid (~4.92 px/module) mis-samples a handful of modules (≈99.5%
> match) — and that is **enough to make barcode decoding fail outright**. It also
> looks “more correct” while being more fragile. Resampling the registry's **own
> pixels** is both simpler and robust.

## 4. Acceptance gate (do not skip)

A certificate is **not done** until all of these pass on the **rendered output**:

- [ ] The cert's QR **decodes** (`pyzbar`) and its payload **exactly equals** the
      registry PNG's payload. (Payload equality — stronger and simpler than a
      %-module comparison.)
- [ ] The in-place PNG **and** the exported PDF both carry the image.
- [ ] No overlap / clipping of text, photo, signature, or QR.

Automate the QR check — never eyeball a QR.

## 5. The tree photo

- **Source of truth:** the `Photo URL:` line inside the **RSA-signed**
  `[TREE PLANTING EVENT]` payload
  (`verify_public_signatures/tree_planting/<tree_id>.json` → `signed_payload`).
  Use exactly that URL — it is the attested, provenance-linked image.
- **Placement (governor spec):** centred, **below the works/description block and
  above the “TrueSight DAO” byline**.
- ⚠️ **Supersession caveat:** a signed attestation covers the **URL string, not the
  image bytes**. A photo can be overwritten in place (see
  `OPEN_FOLLOWUPS.md` → “Tree-planting photo supersession…”), which leaves the
  signature green while the bytes changed. If the governor says the photo is wrong,
  **do not assume the URL is right** — enumerate candidates and confirm which frame.

## 6. Signature

- **Printed name:** `Sophia Truesight` (exact — no cert change needed).
- **Mark:** the gestural ink mark stored privately in `signature_assets`
  (`sophia_truesight_signature_mark.png`). Pass it to the renderer via `--mark`;
  it is deliberately **never committed alongside the template**.
- The mark is illegible by design; **legibility is delegated to the printed name.**

## 7. Data precedence on conflicts

When a field disagrees across surfaces, prefer:

1. **Edgar live resolve** (`/agroverse/qr-code-check`) — current state.
2. **`SunMint Tree Planting` sheet** — the operational record.
3. **`lineage-assets` manifest** — metadata.

Known open conflict for `2024OSCAR_CB_20260620_1`: manifest says `SOLD`; sheet + live
QR say `ASSIGNED_TO_TREE`. **Ask the governor** which framing the cert should carry;
do not silently pick one.

### Date
Derive the planted date from the ledger event; flag to the governor if the sheet
column disagrees (observed 2026-09-02 vs 2026-09-03).

## 8. Template

A config-driven renderer (this SOP's rules encoded as executable checks) lives at:

```
agentic_ai_context/templates/sunmint_certificate/render_sunmint_certificate.py
```

Usage:

```
python3 render_sunmint_certificate.py \
    --config example.config.json \
    --mark /path/to/sophia_truesight_signature_mark.png \
    --outdir /tmp/cert_out
```

It emits, per variant, `<outdir>/certificate_<variant>.png` and `.pdf` (300 dpi) and
**refuses to finish unless the QR payload-equality gate passes**.

## 9. Do NOT

- Do **not** generate or re-encode a QR.
- Do **not** use the stale `qr_codes/*.png` path.
- Do **not** reconstruct a module grid (see §3).
- Do **not** pad/nudge the detector rect.
- Do **not** trust the sheet over a live registry resolve without asking.
- Do **not** commit the signature mark with the template.

## 10. Checklist (per issue)

1. Identify `qr_id`, `tree_id`, awardee, variant(s).
2. Fetch registry PNG; verify payload.
3. Fetch the attested photo URL from the signed payload.
4. Render personal (+ institutional) via the template.
5. Run the acceptance gate (§4).
6. Deliver PNG + PDF; record the issue.

## 11. Revision history

- **rev1 (2026-09-24, PR #1347 as opened):** prescribed reconstructing the 49×49
  module grid and rendering at an integer scale. **This was WRONG** — it is lossy
  (≈99.5% module match) and was observed to break decoding entirely. Corrected in rev2.
- **rev2 (2026-09-24):** replaced with the registry-pixel-crop method (§3); acceptance
  gate changed from %-module-match to **payload equality** (§4); added §5 photo
  supersession caveat, §8 template pointer. The rev1 error is retained here on purpose
  — it is exactly the failure mode this SOP exists to prevent.
