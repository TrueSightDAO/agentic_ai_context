# My Trees Module — Plan

**Status: planning — recon COMPLETE 2026-09-28 · Owner: Gary Teh · Author: Sophia Truesight (autopilot)**
**Trigger (Gary, thread 35944, 2026-09-28):** *"https://cfr.truesight.me/ And Sunmint.truesight.me Should have a page listing trees planted by the public key of the page if it is on the page and then also indicate the status of the tree. Clicking on the tree id should expand the tree details card. User can then click further to get to the monitor tree module with that tree already selected in the dropdown. This module should be accessible via the dropdown of both these mini sites."*

---

## 1. What Gary asked for (5 requirements)

| # | Requirement | Status today |
|---|---|---|
| R1 | A page listing **trees for the viewer's public key** (read from the page / localStorage) | cfr ✅ / sunmint ❌ |
| R2 | Show each tree's **status** | cfr ✅ / sunmint ❌ |
| R3 | **Clicking the tree id expands the tree details card** | ❌ both |
| R4 | Then **click through to the Monitor Tree module with that tree preselected** | ❌ both (deep-link exists in monitor, not wired from My Trees) |
| R5 | Reachable via the **nav dropdown on both mini sites** | cfr partial (in-page nav only, NOT on cfr root) / sunmint ❌ |

## 2. Recon facts (verified read-only 2026-09-28)

- **cfr.truesight.me ALREADY has** `/my-trees/` + `/my-trees-utils.js` (commit `e0db8e5d`, landed as cfr-anapu #15, **2026-09-26**). It derives the viewer's own `pk_hash` from the localStorage keypair and keeps only matching features from `sunmint/trees/index.geojson`. Renders a card per tree: photo, `tree_id`, status chip (`NEW`/`INVALID`/`LINKED`/`SOLD`), species, qr_code, last_measured, program.
  - **MISSING there:** cards are **not** expandable (R3) and there is **no** click-through to Monitor Tree (R4).
- **`sunmint_beta` has NO `my-trees` page at all** (root: index.html, monitor-tree-growth/, limites-da-fazenda/, instrucoes/, payout_registration.html, service-worker.js).
- **Monitor Tree already supports deep-link** `?tree=<id>` on **both** sites (`monitor-tree-growth/index.html` ~L1264: `URLSearchParams.get('tree')` → select → `onTreeSelectChange(true)`). So R4 is **wiring, not new machinery**: My Trees just needs to link `/monitor-tree-growth/?tree=<tree_id>`.
- **`cfr-anapu` is a VENDOR COPY of `sunmint_beta`** (`vendor.json`: `vendor_source_repo: TrueSightDAO/sunmint_beta`, `vendor_source_ref: main`; `sync_sunmint_app.py`). Its `files[]` currently lists only index.html, monitor-tree-growth/, limites-da-fazenda/, instrucoes/, service-worker.js.
- **⚠️ DRIFT:** `my-trees/index.html`, `my-trees-utils.js`, and `derivePkHash()` (in `payout-registration-utils.js`) exist **only on the vendor target (cfr-anapu)** — not on the vendor source (sunmint_beta), and are **not in `vendor.json`**. `derivePkHash`: cfr pru = 280 lines ✅ / sunmint_beta pru = 191 lines ❌.
- **Data source:** `TrueSightDAO/sunmint/trees/index.geojson` — 152 features; per-feature props: `tree_id, species, last_measured, photo_url, status, qr_code, submission_source, pk_hash, program`.
- **Privacy contract (from `my-trees-utils.js`):** only the derived non-reversible `pk_hash` ever appears; raw public key / name / email / PIX / CPF never enter inputs or outputs.

## 3. Canonical-repo decision (RESOLVED)

**`sunmint_beta` is the single canonical source for BOTH surfaces:**
- `sunmint.truesight.me` ← `sunmint_prod` (fork of `sunmint_beta`) → `sync_beta_to_prod`
- `cfr.truesight.me` ← `cfr-anapu` (vendor of `sunmint_beta`) → `sync_sunmint_app.py`

Therefore the module is built **once, in `sunmint_beta`**, then propagated. Building on `cfr-anapu` directly (as the existing copy did) is the **anti-pattern that created the drift** — do not extend it.

## 4. Build units (ONE PR PER TURN)

- **U1 ⏳** `sunmint_beta`: port the module — `my-trees/index.html` + `my-trees-utils.js`, add `derivePkHash()`/`maskPkHash()` to `payout-registration-utils.js`, i18n keys, existing tests ported. Base = the proven cfr files (verbatim) so the diff is reviewable.
- **U2 ⏳** R3 — **expandable** tree details card (click the tree id → details panel: photo, species, planted, status, QR, measurement, submission source; reuse the monitor page's `.tree-detail` markup).
- **U3 ⏳** R4 — **"Monitor this tree" →** link `/monitor-tree-growth/?tree=<tree_id>` (relative on sunmint, absolute-safe on cfr).
- **U4 ⏳** R5 — nav: add `myTrees` option + `onNavChange()` route to `sunmint_beta/index.html` root (and ensure cfr root gets it via re-vendor).
- **U5 ⏳** `vendor.json`: add `my-trees/index.html`, `my-trees-utils.js`, `payout-registration-utils.js` to `files[]`; run `sync_sunmint_app.py` → cfr-anapu (supersedes the drifted cfr-only copy; single source thereafter).
- **U6 ⏳** UAT on `beta.sunmint.truesight.me` + cfr beta preview.
- **U7 🔒 GATED** `sync_beta_to_prod(sunmint_prod)` — **only after Gary's explicit GO**.

## 5. UAT checklist

- [ ] Signed-in farmer with N trees sees N cards; status chip matches `index.geojson`
- [ ] A key with zero trees shows the honest empty state (not a silent blank)
- [ ] No key in localStorage shows the "link email / no key" state
- [ ] Clicking a tree id expands its details card (R3)
- [ ] "Monitor this tree" opens Monitor Tree with **that** tree preselected in the dropdown (R4)
- [ ] Nav dropdown lists the module on **both** root pages (R5)
- [ ] **Privacy:** no raw public key / PIX / CPF anywhere in the DOM or network

## 6. Risks / notes

- **Drift** (already materialized): without U5 the two sites diverge again. `vendor.json` must list every module file.
- GitHub Pages rebuild lag after merges → verify with a cache-busted fetch.
- `index.geojson` `pk_hash` coverage: `countWithPkHash() === 0` → page shows a "feed not rebuilt" note (by design).
- Product intent: SunMint never links out to the full dApp (complexity the app exists to avoid).

## 7. RESUME HERE

**Next unit = U1** — create the module in `sunmint_beta` (port the proven cfr files). Then U2 (expandable) → U3 (deep-link) → U4 (nav) → U5 (vendor + `vendor.json`) → U6 UAT → U7 prod (gated on Gary).
