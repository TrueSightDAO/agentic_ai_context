# Tree-planting photo GPS — capture at source (A1 + B)

**Filed:** 2026-10-15, by Sophia Truesight, at Gary's direction.
**Status:** registered 2026-10-15 — A1 PR1 not yet started.
**Workstream channel:** Discord `#tree-planting-photo-gps` (channel `1560808245948588103`, category SunMint).
**Trigger (Gary, 2026-10-15):** *"when the photo is submitted with CFR or Sunmint DApps that
specific detail never gets captured"* → *"go for it"* → *"monitor and supervise that new thread
to completion."*

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**

---

## 0. The bug (verified live, 2026-10-15)

Farmer-facing DApps submit `[TREE PLANTING EVENT]`s to Edgar
(`POST https://edgar.truesight.me/dao/submit_contribution`) but the **burned-in watermark
lat/long is never read** — coordinates only ever come from `navigator.geolocation` or, in the CFR
gallery path, EXIF GPS.

- **CFR DApp** (`cfr.truesight.me` `cfr_main.html`) — live-camera capture → `navigator.geolocation`
  only; gallery file → `readExifGps()`. When both fail it submits **blank** `- Latitude: ` /
  `- Longitude: ` lines (line ~1104).
- **SunMint DApp** (`dapp`/`sunmint` `report_tree_planting.html`) — `navigator.geolocation` only,
  and it **refuses** to submit when missing.
- **GAS parser** (`tokenomics` `process_tree_planting_telegram_logs.js:508/522`) gates on the
  literal `'N/A'`. A **blank** line is `''`, not `'N/A'`, so the row lands **`NEW` with empty
  sheet cols K/L** instead of `INVALID`.

**Observed impact:** 17 of 91 CFR Anapu tree rows (2026-10-15 batch) arrived coordinate-less and
had to be backfilled by hand (15 payable + 2 dropped-dup rows). The 17 in-place backfills are
DONE; this plan fixes the *source* so it stops recurring.

## 1. Root cause — the seam

The coordinate never reaches the signed submission. Two independent reasons:

1. A live camera blob is a **canvas re-encode** → carries **no EXIF**, and if `navigator.geolocation`
   is denied/slow there is no fallback to the watermark that is *visibly printed on the photo*.
2. The DApp never reads the watermark; the adapter's `read_timemark_watermark()` (which *does*
   read it, for the chat summary) is not on the DApp path at all.

## 2. Hard constraint (shapes the design)

The RSA signature is computed **client-side over the exact `requestText`** and verified
server-side. **A server-side append would break verification** — so coordinates can only be folded
into `requestText` **in the browser, before signing**. (Consistent with the 2026-10-14 ruling: the
signed planting event is the audit trail; lat/long is an *attribute* of it, not part of the
signature's meaning.)

## 3. Design — A1 (fix) + B (backstop)

### A1 — DApp reads the watermark before signing (the fix)
When EXIF **and** `navigator.geolocation` both yield nothing, the DApp reads the burned-in
watermark and folds `- Latitude:` / `- Longitude:` into `requestText` **before** `signText()`.
- **A1.1 (server helper, recommended):** new Edgar endpoint
  `POST /dao/read_watermark_gps` that runs the **existing, tested** `read_timemark_watermark`
  (vision-first, tesseract fallback) and returns `{lat, lon, source}`. Reliable; reuses code we
  trust; small prod surface (one route + vision key).
- **A1.2 (client-only fallback):** in-browser `tesseract.js` on a bottom-left crop. Zero server
  change, but the module's own docs say tesseract alone struggles on the light-on-foliage block →
  flaky, risks silently-wrong coords. Use only if a server surface is undesirable.
- Stamp `- GPS Source: watermark` so a vision-read value is auditable vs a device-typed one.

**Repos:** `truesight_dao_client` (endpoint, deploys to `dao_protocol`) + `dapp_beta`
(`cfr_main.html` and `report_tree_planting.html`). Beta-first; prod promote on explicit go.

### B — GAS parser hardening (the backstop)
Treat a **blank** `- Latitude:` as missing → `NEEDS_REVIEW`/`INVALID`, never silently `NEW`, so
this class can never again persist unseen. `tokenomics` is describe-don't-fix (per standing SOP) —
**spec handed to the governor, not self-merged.**

## 4. Units / PR roadmap

| Unit | Scope | Repo | Gate |
|---|---|---|---|
| **PR0** | This plan + manifest row (registration) | `agentic_ai_context` | auto (docs) |
| **PR1** | A1.1 — `POST /dao/read_watermark_gps` + unit tests (reuse `read_timemark_watermark`) | `truesight_dao_client` | auto (own-repo) |
| **PR2** | A1 — wire both DApp pages to call the endpoint when EXIF+geolocation empty, before signing | `dapp_beta` | auto → beta review |
| **PR3** | B — GAS parser blank-latitude guard | `tokenomics` | **spec only → governor go** |
| **PR4** | Beta UAT (Gary / a real farmer capture) → prod promote | `dapp_beta` → `dapp_prod` | **gate: human** |

## 5. Gates / boundaries

- No production deploy without an explicit governor go (beta → review → `sync_beta_to_prod`).
- No money / TDG movement in this plan.
- `tokenomics` (PR3) is spec-only — no self-merge.
- One PR per execution turn.

## 6. Verification / UAT

1. **PR1:** unit tests green; endpoint returns the same lat/long the on-disk reader returns for a
   known CFR Anapu photo (regression fixture).
2. **PR2:** on beta, a capture with geolocation disabled and a photo carrying only the watermark
   yields **non-blank** `- Latitude:`/`- Longitude:` in the signed `requestText`.
3. **PR3:** a synthetic blank-latitude row lands `NEEDS_REVIEW`, not `NEW`.
4. **End-to-end:** a real farmer capture through `cfr.truesight.me` produces sheet cols K/L
   populated with no hand-backfill.
