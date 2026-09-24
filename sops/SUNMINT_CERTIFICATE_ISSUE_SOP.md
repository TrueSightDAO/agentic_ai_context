# SOP — Issuing a SunMint “Certificate of Tree Guardianship”

**Owner:** Sophia Truesight (autopilot). **Governor:** Gary.
**Origin:** thread 35189, 2026-09-24 — *“Make sure we have an SOP in place for future
issues of SunMint certificate… You can always find it in our registry.”*
**Revision:** rev4 (2026-09-24) — §3 corrected to the method the canonical template ACTUALLY implements (grid + native-resolution centre-overlay re-paste); added the pyzbar-at-native-size gotcha and the canonical-template-path warning. (rev3: §7 conflict framing resolved, canonical tree id = col D, planted date from EXIF.)

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
   - ⚠️ **pyzbar-at-native-size gotcha.** Some registry PNGs embed the QR small enough
     that pyzbar fails at native size even though the image decodes fine at 2–3× (cv2 and
     real scanners read it). This affects **the whole `2023SA…` (Santa Anna) family** —
     every one of them fails pyzbar at native resolution, so **every Santa Anna cert is
     un-renderable** unless you retry on an upscale. Retry on a 2–3× LANCZOS upscale
     before aborting; the §8 template now does this automatically.
3. Crop the **detector's own bounding rect**, **unchanged**. Do **not** pad or nudge it —
   a 1-px shift changes the module phase and breaks decoding.
4. Add a synthetic **quiet zone** ≥ 4 modules (white border) around the crop.
5. Re-confirm the quiet-zoned crop decodes.
6. Render the recovered grid at an **INTEGER scale `k ≥ 4`** via **NEAREST** (a
   non-integer NEAREST resize smears modules and kills scanning; `k ≥ 4` is a hard
   print floor), then **re-composite the registry's own centre overlay (if any) at
   native resolution** on top of the crisp grid (see the note below).

> **What the canonical template actually does (and why reconstruction is now OK).**
> The §8 template **does** reconstruct a module grid — and that is deliberate. rev1
> forbade it because a *naive* grid (no overlay paste, non-integer scale) mis-sampled a
> few modules and failed to decode. The canonical approach **reconciles both facts**:
> recover the true module grid (smallest N that re-decodes), render it at an **integer**
> scale `k ≥ 4` via NEAREST for crispness, and then **re-paste the registry's own
> centre-overlay pixels at native resolution**. Reconstruction is safe *iff* it is
> integer-scaled, overlay-preserving, and decode-gated — which is exactly what §8
> enforces. Skipping the overlay re-paste is the 2026-09-24 thread-35189 defect (the
> Agroverse centre logo gets thresholded into speckle).

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

**Conflict framing — RESOLVED (governor ruling, 2026-09-24).** A bag QR that has been
linked to a planted tree is framed **`ASSIGNED_TO_TREE`**. The `sold` event is *history*
(the bag was sold, financing the tree); the **current state** is tree-linked. The
manifest previously said `SOLD` only because it was seeded before the link existed — the
seeder now joins the link at seed time and history is append-only
(`lineage-assets` #12/#13/#14), so the manifest carries `status: ASSIGNED_TO_TREE`
**and** retains the `sold` event. If a manifest still disagrees with the live resolve,
**re-seed — never hand-edit** (hand-added top-level fields are still dropped on re-seed;
see the `OPEN_FOLLOWUPS.md` entry on `merge_preserve_events`).

### Canonical tree id (the +1 trap)
The canonical `tree_id` is the SunMint sheet **col D** Telegram Message ID
(e.g. `Edgar_20260903083523_003`) and equals the tree's `ledger_ref`. `sunmint/trees/
index.geojson` keys on col A, so its `tree_id` is **+1** (`…_004`). **Canonical = col D
(`…_003`).** Do not "fix" the cert config to match the geojson; the geojson is the wrong
side (tracked at `OPEN_FOLLOWUPS.md` → "tree_id is keyed on the sheet's col A").

### Date
Derive the planted date from the image EXIF / ledger, not the sheet's col G. Resolved for
`2024OSCAR_CB_20260620_1`: the seedling photo's EXIF is `2026:09:02 18:47:11` →
**2026-09-02** (`date_display="2 September 2026"`); the sheet's `20260903` is the *logging*
date. Flag to the governor only on a genuine disagreement.

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

> ⚠️ **Render from the canonical path ONLY — never a `/tmp` copy.** On 2026-09-24 a
> certificate was rendered from a stale untracked `/tmp` WIP snapshot (a pre-#1352 copy,
> **403 lines vs the canonical 540**) that had **no overlay logic** — the Agroverse centre
> logo was silently thresholded away in the delivered PDFs. Always resolve the template via
> `read_repo_file`/raw URL from `agentic_ai_context`, and optionally assert its `md5`
> against `main` before rendering.

## 9. Do NOT

- Do **not** generate or re-encode a QR.
- Do **not** use the stale `qr_codes/*.png` path.
- Do **not** reconstruct a module grid **without re-pasting the centre overlay at native
  resolution** (see §3, step 6 — the Agroverse-logo defect).
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
- **rev3 (2026-09-24):** §7 governor conflict-framing resolved (`ASSIGNED_TO_TREE`, with
  `sold` retained as history); canonical tree id pinned to col D (the `index.geojson` +1
  trap); planted date = EXIF, not sheet col G. Seeder read-path fixed (#12/#13/#14) so the
  manifest no longer needs a hand-edit.
- **rev4 (2026-09-24):** §3 rewritten to the method the canonical template ACTUALLY
  implements — recover the true module grid, integer-scale at k≥4, **and re-composite the
  registry's centre overlay at native resolution** (the missing step that garbled the
  Agroverse logo, thread 35189). Added the **pyzbar-at-native-size gotcha** (`2023SA…`
  family) and the **canonical-template-path warning** (never render from a `/tmp` copy).
  Template now retries pyzbar on a 3× upscale.
