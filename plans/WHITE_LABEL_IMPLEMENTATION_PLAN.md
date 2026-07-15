# Agroverse White-Label Corporate Gifting — Implementation Plan & Checklist

**Date:** July 14, 2026  
**Status:** ⚠️ **Shipped but NOT working — primary path is dead.** Phase 1 (plumbing) complete;
Phase 2 (state repair + visual placement) is the live work. See § Phase 2 below.  
**Author:** AI Agent

> **Status correction (2026-07-14, browser-verified):** the checklist below is ticked end-to-end,
> but a Playwright pass over all 7 states found the **registration path and the post-payment
> confirmation are both broken in production**. Ticking "deploy to production" while the primary
> funnel is dead is exactly the failure `OPERATING_INSTRUCTIONS.md` §9/§10 exist to prevent —
> the UAT spec at `tests/white-label-uat.spec.ts` did not exercise interaction handlers.
> Do not trust Phase 1's ✅ as evidence the flow works.

---

## Architecture (Final)

```
Client (agroverse.shop/white-label/)
  │
  ├─→ Edgar (POST /dao/submit_contribution)    — RSA-signed uploads + orders
  │     ├─ github_upload.py                     — writes PNG + design JSON to agroverse-designs repo
  │     ├─ design_events_log.py                 — dedup via Google Sheet
  │     └─ dispatch.py                          — routes to GAS webhooks
  │
  ├─→ GitHub API (GET .../contents/designs/)    — list designs directly (no server proxy)
  │
  ├─→ raw.githubusercontent.com                 — serve design images directly (no server proxy)
  │
  └─→ GAS checkout (createCheckoutSession)      — Stripe + shipping (same as cart)
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| No `/design/*` endpoints | Uploads go through existing `submit_contribution` with attachment flow; list/image call GitHub directly |
| `agroverse-designs` repo | Versioned, auditable, unified file + metadata per design |
| Flat $10/bar | Simple pricing; volume covers label cost variance |
| Email → sha256 folder | Privacy — email not exposed in public repo URLs |
| DaoClient CDN (unpkg) | Same pattern as oracle + capoeira; zero build system |
| `publicKey` / `privateKey` localStorage | Shares keys with DApp (same as oracle pattern) |
| Gallery loads immediately if keys exist | No network check — design list serves as auth gate |

---

## Checklist

### Infrastructure
- [x] Create `TrueSightDAO/agroverse-designs` GitHub repo
- [x] Add `DESIGN UPLOAD EVENT` to events_catalog.json
- [x] Add `DESIGN ORDER EVENT` to events_catalog.json
- [x] Add `PRODUCT REGISTRATION EVENT` to events_catalog.json
- [x] Add `custom-white-label-chocolate-bar-50g` to products.js

### Backend (dao_protocol — deployed to edgar.truesight.me)
- [x] Extend `github_upload.py` — `write_design_json()`, `append_order_to_design()`, `list_design_directory()`, `get_file_content()`
- [x] Create `design_events_log.py` — Design Events sheet adapter with dedup
- [x] Add DESIGN event handling to `dao.py` submit_contribution (JSON write + dedup log)
- [x] Add dispatch entries for `[DESIGN UPLOAD EVENT]` + `[DESIGN ORDER EVENT]`
- [x] Update SCHEMA.md with Design Events tab schema
- [x] Update npm `dao-client` (edgar.ts) with design methods
- [x] Deploy to production (git pull + systemctl restart)

### Frontend (agroverse.shop)
- [x] Create `/white-label/index.html` — how-it-works, pricing, auth, gallery, order form
- [x] Create `/js/white-label.js` — DaoClient auth, GitHub API gallery, submit_contribution upload/order
- [x] Create `/css/white-label.css` — gallery grid, steps, pricing table, order form
- [x] Add Homepage CTAs ("Corporate Gifting" + "Custom White-Label Bars")
- [x] Add "White Label" to nav (shared-chrome.js)
- [x] Add "White Label" to footer (shared-chrome.js)

### GAS
- [x] Fix image URL handling for absolute URLs (GitHub raw)
- [x] Pass `design_url` and `design_id` through to Stripe metadata
- [x] Recognize white-label productId in cart items

### Docs
- [x] Update `PROJECT_INDEX.md` with agroverse-designs
- [x] Update `WORKSPACE_CONTEXT.md` with agroverse-designs
- [x] Update `SCHEMA.md` with Design Events tab
- [x] Update `truesight_me/contracts/` with 3 new event types
- [x] UAT test spec at `tests/white-label-uat.spec.ts`

---

## Files Changed

| File | Change |
|---|---|
| `dao_protocol/.../server/data/events_catalog.json` | +3 event types |
| `dao_protocol/.../server/services/github_upload.py` | +5 new functions |
| `dao_protocol/.../server/sheets/design_events_log.py` | New — dedup adapter |
| `dao_protocol/.../server/routes/dao.py` | DESIGN event handling |
| `dao_protocol/.../server/dispatch.py` | +2 dispatch entries |
| `dao_protocol/packages/dao-client/src/edgar.ts` | +3 design methods |
| `agroverse_shop/white-label/index.html` | New page |
| `agroverse_shop/js/white-label.js` | New — full client logic |
| `agroverse_shop/css/white-label.css` | New styles |
| `agroverse_shop/js/products.js` | +1 SKU entry |
| `agroverse_shop/js/shared-chrome.js` | +nav + footer links |
| `agroverse_shop/index.html` | +2 CTA buttons |
| `agroverse_shop/google-app-script/.../agroverse_shop_checkout.gs` | URL fix + metadata |
| `agroverse_shop/tests/white-label-uat.spec.ts` | New — UAT tests |
| `agentic_ai_context/PROJECT_INDEX.md` | +agroverse-designs |
| `agentic_ai_context/WORKSPACE_CONTEXT.md` | +agroverse-designs |
| `tokenomics/SCHEMA.md` | +Design Events tab |
| `truesight_me/contracts/index.html` | +3 contract cards |
| New repo: `TrueSightDAO/agroverse-designs` | Design storage |

---

## Production URLs

| Resource | URL |
|---|---|
| White-label page | https://agroverse.shop/white-label/ |
| Design repo | https://github.com/TrueSightDAO/agroverse-designs |
| Edgar (submit) | https://edgar.truesight.me/dao/submit_contribution |
| GAS checkout | GAS script `1ovx-Hq5L5Mg...` |
| npm CDN | https://unpkg.com/@truesight_dao/dao-client@1.1.0-rc.4/dist/dao-client.min.js |

---
---

# Phase 2 — State Repair + Visual Placement Spec

**Added 2026-07-14** after a browser pass (Playwright, Chromium, 1280×900 + 390×844) drove all
seven states with stubbed Edgar/GitHub responses. Evidence: console errors + full-page renders per
state. This section is the **plan of record for Phase 2** and is written to be executed by another
LLM (DeepSeek is active in `agroverse_shop/` — see § Division of labor).

---

## 2.0 🔴 D0 — THE LABEL SPEC IS ROTATED 90°. Resolve this before writing any other code.

**Found 2026-07-14 by Gary, confirmed by measurement.** Colour-isolating the orange label in
`agroverse_shop/assets/images/products/81-dark-chocolate-bar-50g-packaging.jpg` (1597×900):

| | Aspect (W:H) | Real size | Orientation |
|---|---|---|---|
| **Label on the actual product** | **1 : 1.95** (bbox x1190–1457, y221–741 = **267 × 520 px**) | **2.05" W × 4" H** | **Portrait** |
| Spec asserted across the page | 1 : 0.5 (1200 × 600 px) | 4" W × 2" H | Landscape |

**Every design collected under the current spec is unusable.** Customers upload landscape artwork
for a portrait label. Fixing B1/B2 without fixing this just means we collect broken artwork faster
— which is why **D0 outranks PR1**.

**Where the 4"×2" likely came from:** `WORKSPACE_CONTEXT.md:131` cites a real ledger purchase —
*"Sticker Mule 4x2in custom rectangle label (per piece, order R384751187)"*. That is almost
certainly the **QR-code label stock** (see `AGROVERSE_QR_CODE_BATCH_GENERATION.md`), **not** the
chocolate-bar label. The 4"×2" figure appears to have been lifted from that ledger line and adopted
as the artwork spec. **Unverified — Gary must confirm against the actual printer / die.**

**Why the repo can't answer it:** `agroverse_shop/docs/WHITE_LABEL_SUPPLY_CHAIN_HANDOFF.md` points
to **`agentic_ai_context/AGROVERSE_WHITE_LABEL_SUPPLY_CHAIN.md`** — which **does not exist**, on
`main` or locally. The Liz pilot, routing, school pricing, and shipping tiers it references are
unrecorded anywhere. **Someone must write that file**; it is the missing authority for D0.

### ✅ D0 RESOLVED — Gary confirmed 2" W × 4" H (2026-07-14); flipped in [beta#183](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/183)

**No data migration was needed** — audited `TrueSightDAO/agroverse-designs`: `designs/` contained
only `.gitkeep`, so zero artwork had been collected under the wrong spec.

Guarded by `agroverse_shop/tests/white-label-label-spec.spec.ts` (verified fails-first: 5/7 failed
pre-flip, 7/7 pass after). It tests **spec drift** — the bug class that caused D0, the same fact
hard-coded in 7 places with nothing checking they agreed — and the **validator via a real file
drop**, since `validateImageDimensions()` only runs on interaction (§10).

Also fixed an off-by-one in the pre-existing UAT spec (asserted CA at `nth(6)`, TX at `nth(45)`;
index 0 is the placeholder, so those were CO and VT). **That spec had never passed** — further
evidence Phase 1's "UAT test spec ✅" was ticked without being run. Suite is now **26/26 green**.

<details><summary>Original checklist (all applied)</summary>


| File | Line | Now | → |
|---|---|---|---|
| `agroverse_shop/js/white-label.js` | 247–248 | `naturalWidth !== 1200 \|\| naturalHeight !== 600` | `!== 600 \|\| !== 1200` + message |
| `agroverse_shop/js/white-label.js` | 324 | `Dimensions: '4x2in'` | `'2x4in'` |
| `agroverse_shop/css/white-label.css` | 33 | `aspect-ratio: 2/1` | `aspect-ratio: 1/2` |
| `agroverse_shop/white-label/index.html` | 43 | subtitle `4"×2" labels` | `2"×4" labels` |
| `agroverse_shop/white-label/index.html` | 45 | badge `4"×2" labels` | `2"×4" labels` |
| `agroverse_shop/white-label/index.html` | 86 | drop hint `1200×600px (4"×2")` | `600×1200px (2"×4")` |
| `agroverse_shop/white-label/index.html` | 159 | step 1 `1200×600px (4"×2")` | `600×1200px (2"×4")` |
| `agentic_ai_context/PROJECT_INDEX.md` | 75 | agroverse-designs `(4″×2″ PNG)` | `(2″×4″ PNG)` — **still open**: canonical file, §3 says don't edit without an explicit ask. Logged in `CONTEXT_UPDATES.md` for Gary to apply. |
| — | — | **Any designs already uploaded** | ✅ audited — none existed (`.gitkeep` only) |

</details>

✅ **Already done (merged, [agroverse_shop_beta#182](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/182)):**
`white-label-mockup.png` rebuilt from the real photo — portrait 2"×4" placeholder composited onto
the actual kraft pouch at the real label's bbox; auth card shows that single mockup;
`object-fit: contain`; mockup stacks above the email field on narrow viewports (P3).
**The page is internally inconsistent until the table above lands** — the mockup says 2"×4", the
copy still says 4"×2".

---

## 2.1 The core placement diagnosis

**The page is a marketing page with app panels injected into its middle.** The frame — hero
(~600px) + How It Works + Pricing — renders **identically in every state**; only the middle band
swaps. Three consequences, and they compound:

1. **The app is always below the fold.** Every state (`My Designs`, `Place Order`, `Order Placed`)
   begins at y≈610–700px. Every single interaction costs a scroll past a pitch the user has
   already accepted.
2. **The marketing never retires.** A customer placing their 4th reorder still gets *"Step 1:
   Upload artwork"* underneath their order form, and a Pricing table restating the dropdown they
   just used. The frame's value decays to ~0 after first purchase; its pixel cost stays at 600px.
3. **The hero sells the wrong product.** `81-dark-chocolate-bar-50g-packaging.jpg` is the
   **standard Agroverse retail bar with the orange 81% label**. On a page whose entire promise is
   *"your brand on this bar,"* the largest, most persistent, most-repeated visual is
   **Agroverse's own label**. The one image that carries the value proposition —
   `white-label-mockup.png`, captioned *"Your custom label on this bar"* — renders ~220px wide,
   bottom-right of the auth card, at y≈800, with unreadable body text.

**The through-line, and the single most important finding in this document:**

> The page gives its largest pixels to a generic product photo and its smallest to the customer's
> own artwork. **For a white-label product, the customer's artwork _is_ the product.** That
> inversion repeats in all seven states — hero (wrong bar, 320px) vs. mockup (220px), gallery
> (220px cards), order (130px preview in a 260px column with ~200px of dead space beneath it),
> success (design absent entirely).

Everything in §2.3 follows from correcting that one inversion.

### Placement principles (apply to every state)

| # | Principle | Consequence for this page |
|---|---|---|
| P1 | **The product is the customer's artwork.** | Every state's dominant visual is *their* design on a bar — never a stock Agroverse bar. |
| P2 | **Proof before ask.** | The mockup + How It Works + Pricing precede the email capture. Today the ask (y≈630) sits *above* the proof (y≈980–1360). Invert. |
| P3 | **DOM order = mobile priority order.** | The auth grid stacks at ≤640px, dropping the mockup *below* the email field: on mobile you are asked for your email **before you ever see the product**. Fix by DOM order, not CSS. |
| P4 | **Marketing chrome is state-scoped, not global.** | Full frame for anonymous visitors; a one-line strip once authenticated; **nothing** competing with a live order form. |
| P5 | **A state swap preserves the container's position and size.** | Swapping form→verify inside `#wl-auth` currently collapses the card to an empty box. Reserve the height; swap contents in place. |
| P6 | **A visual's size tracks the decision's value.** | A $2,000 decision does not get a 130px preview. Order-state preview is the largest element on screen. |
| P7 | **Never show the raw artboard where the product belongs.** | Gallery/upload/order previews composite the 1200×600 file **onto the bar**. Raw artwork on a grey field answers "here's my file"; the user is asking "here's my product?" |

---

## 2.2 Broken / disjointed flows found (browser-verified)

Ordered by severity. **B1 and B2 are showstoppers — the funnel does not work today.**

| ID | Severity | Flow | Mechanism (verified) |
|----|----------|------|----------------------|
| ~~**B1**~~ ✅ [#184](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/184) | 🔴 **Critical** | **Registration dead-ends into an empty card.** Enter email → click *Get Started* → the form vanishes and **nothing replaces it**. No feedback, ever. | `white-label.js:96` writes to `#wl-auth-loading`, **which does not exist in the HTML** → `TypeError: Cannot set properties of null`. Thrown *after* `hide('wl-auth-form')` (:95) and *before* `show('wl-verify-state')` (:97), so the verify panel never appears. The `catch` (:99) writes the error into `#wl-auth-error` — **which is a child of the form it just hid** (`index.html:60`), so the error is invisible too. Result: heading + intro paragraph + ~250px of void. **This is the exact class of bug in `OPERATING_INSTRUCTIONS.md` §10** (`base64ToArrayBuffer`) — a runtime error in a handler that only fires on interaction, which page-load tests cannot catch. |
| ~~**B2**~~ ✅ [#184](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/184) | 🔴 **Critical** | **After paying, the customer sees "No designs yet. Upload your first one above."** | Two IIFEs race. The success IIFE (:520) shows `#wl-success` on `?session_id=`. Then the init IIFE (:533) runs `initAuth()` → keys+email exist → `showGallery()` → **`hide('wl-success')`** (:154). Verified: at 500ms the success panel is *already gone*. The confirmation is unreachable for every returning customer — i.e. everyone who just paid. A $2,000 Stripe redirect lands on an empty-gallery message. |
| **B3** | 🟠 **Money** | **Shipping is quoted for the wrong weight.** Enter address at qty=200 → rates load → change qty to 1,000 → total updates to $10,000, **rates do not re-fetch**, the old selection stays, button stays enabled → checkout with shipping quoted for 1/5 the weight. | `:369` binds qty `change` → `updateOrderTotal` **only**. `calculateShipping` derives weight from qty (`:396`) but is bound solely to address blur / state change (`:378–381`). Nothing invalidates `selectedShippingRateId`. |
| **B4** | 🟠 | **Gallery never sorts; "newest first" is a no-op.** | Upload signs via legacy **`client.sign()`** (`:320`) which is *"v1.0.x compatible — **no Timestamp injection**"* (`dao-client/src/payload.ts:21`). Backend sets `created_at = _extract_field(text, "Timestamp") or ""` (`dao.py:369`) → **`created_at: ""` on every design** → `(b.created_at||'').localeCompare(...)` (`:192`) always returns 0 → designs render in GitHub API order (alphabetical by UUID) forever. The order path (`:451`) correctly uses `submitEvent()`, which *does* inject Timestamp — **two different signers in one file.** |
| **B5** | 🟠 | **Shipping failures are silent.** Network error → nothing renders, button stays disabled, no reason shown. | `catch (e) {}` — empty (`:435`). |
| **B6** | 🟡 | **Disabled button with no stated blocker.** *Produce → Checkout* ships greyed out with no hint that an address is required to enable it. | `:142` `disabled`; `updateProduceButton` (:438) gates on `selectedShippingRateId` with no adjacent explanation. |
| **B7** | 🟡 | **Empty state points at a button, not the drop zone.** *"No designs yet. Upload your first one above"* renders **below** the collapsed upload panel, orphaned in whitespace, pointing at a toggle the user must first discover. First-run requires a click to reveal the one thing first-run is for. | `#wl-upload-panel` is `display:none` until `#wl-upload-btn` toggles it (`:260–263`). |
| **B8** | 🟡 | **No route from Order back to Upload.** Realise on the order screen that the design is wrong → only *"← Back to Gallery"*. | `:363`. |
| **B9** | 🟡 | **Upload success is unacknowledged.** Panel closes, grid reloads. No "uploaded" confirmation. | `:337–342`. |
| **B10** | 🟡 | **Duplicate hero image.** The same packaging photo renders twice, ~350px apart (`index.html:44` and `:70`), and again on mobile within one scroll. | — |
| **B11** | 🟡 | **State select truncates to "Stat".** | `.wl-ship-row { grid-template-columns: 1fr 80px 100px }` (`white-label.css:52`) — 80px cannot hold a select + arrow. |
| **B12** | 🟡 | **"How It Works" orphans step 5** onto a second row, centered under step 1. | `repeat(auto-fit, minmax(160px, 1fr))` (`:60`) yields 4-up at 960px for a 5-step flow. |
| ~~**B14**~~ ✅ [#184](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/184) | 🟠 | **A TypeError on every page load.** `universal-nav.js:122` injects `cart-ui.js`, which calls `window.Cart.getItemCount()` for the nav badge — but `white-label/index.html` never loaded `cart.js`, so it threw on every load. Every other page loads it explicitly. Found while establishing a no-uncaught-errors invariant; fixed with one script tag. |
| **B13** | 🟡 | **Pricing table is six rows of `$10.00`.** Sets up an expectation of volume discounts, then delivers none, and restates the dropdown verbatim. | `index.html:167–181`. |

### Open questions for Gary (not bugs — decisions)

| ID | Question |
|----|----------|
| **Q1** | **Is world-readable corporate artwork acceptable?** `agroverse-designs` is a **public** repo. The plan's rationale — *"Email → sha256 folder \| Privacy — email not exposed in public repo URLs"* — is true but is **obfuscation, not confidentiality**: anyone who knows a customer's email can hash it and enumerate that folder. We would be storing *unreleased corporate branding* (the whole point of a white-label gift program) in public. A private repo + Edgar-proxied reads closes it, at the cost of the "no server proxy" decision. |
| **Q2** | **Can we actually ship 500 / 1,000 bars?** Weight = `2.41·qty + 11.5` oz (`:397`) → **500 bars ≈ 76 lb, 1,000 bars ≈ 151 lb**, both over the **USPS 70 lb single-parcel limit**. The dropdown sells quantities the shipping call may be unable to quote — and there is no multi-parcel/freight path. |
| **Q3** | **Why is 200 bars ($2,000) the preselected default?** (`:120`) Deliberate anchoring, or an accident? It is the only non-minimum default on the page. |
| **Q4** | **Flat $10/bar at every tier** — confirm no volume break is intended before we redesign the pricing block (B13). |
| **Q5** | **Where is the artwork template?** There is no downloadable 1200×600 artboard / bleed / safe-area guide anywhere. We reject non-conforming files with a hard error and offer no way to produce a conforming one. |

---

## 2.3 Per-state visual placement spec

Seven states. For each: **what it's for**, **where each visual goes**, and **why**. Percentages are
of the container (`.wl-container`, max 960px). "Frame" = hero + How It Works + Pricing.

---

### State A — Anonymous / first visit  *(the pitch)*

**Job:** convince, *then* capture an email. Nothing here is worth gating before the pitch lands.

| Slot | Content | Why |
|------|---------|-----|
| 1 — Hero, full width, ~380px | **The mockup** — customer artwork on the bar. Ideally **3 bars with 3 different custom labels** (holiday / conference / wedding). | P1. Answers "what is this?" in one glance and shows the range. The current hero shows the 81% retail bar — the one product this page is *not* selling. |
| 2 — Fact strip | Existing badge (`50-unit min · $10/bar · 4"×2" · 50g · 1 bar = 1 tree`). | Already good: dense, scannable, sets expectations before the ask. Keep as-is. |
| 3 | **How It Works** (5 steps, 5-up — fix B12) | P2. This is the "can I actually do this?" objection. It must precede the ask. |
| 4 | **Pricing** — replace the 6-row table (B13) with one line: *"$10/bar, any quantity from 50 to 1,000. Shipping at checkout."* + the tree/lead-time note. | P2 + B13. Six identical rows imply a volume break that doesn't exist. One line is the whole truth and reads faster. |
| 5 — **Closing CTA** | Email capture. Headline **not** "Sign In to Get Started" — lead with the outcome: *"Start your design"*. Sub-line states what happens next: *"We'll email you a link to your design workspace."* | P2. **This is the inversion to fix:** the ask currently sits at y≈630, the proof at y≈980–1360 — the user is asked to pay (in email) before being told what they're buying. |
| — | **Delete** the second copy of the packaging photo (B10). | It adds nothing and pushes the mockup further down. |

**Mobile (≤640px):** DOM order *is* priority order (P3). Mockup → badge → How It Works → Pricing →
form. Today the grid stacks the form above the mockup: **the ask lands before the proof.**

---

### State B — Awaiting verification

**Job:** tell them it worked, and keep selling while they check their inbox. *(Currently: B1 — a blank card.)*

| Slot | Content | Why |
|------|---------|-----|
| Same card, same position, **reserved height** | ✉ icon → **"Check your inbox — we sent a link to `brand@acme.com`"** → *Resend* + *Use a different email*. | P5. The transition must not move or collapse the card; a card that empties reads as "it broke" — which is precisely what B1 does today. Echoing the typed address back catches typos, the #1 cause of "it never arrived." |
| Right column (desktop) | **Keep the mockup visible.** | The user is about to leave for their mail client. The last thing on screen should be the product, not a dead form. |
| Below | *"Nothing yet? Check spam, or resend."* | The only self-service exit from the most common failure. Today's *Check Status* button re-registers on every click with no pending feedback. |

---

### State C — Gallery  *(returning, has designs)*

**Job:** this is now an **app**, not a landing page. The marketing has done its work — retire it.

| Slot | Content | Why |
|------|---------|-----|
| 1 — Compact header (~80px) | *"My Designs"* + `Upload New Design`. **Replace the 600px hero** with a one-line strip. | P4. Reclaims ~520px. The app starts **above** the fold instead of at y≈700. A repeat customer should not re-read the pitch to reorder. |
| 2 — Grid | Cards at 2:1 — **each showing the label composited on the bar**, not the raw artboard on a grey field. Name + *"3 past orders · last 2026-06-14"* + `Reorder`. | P1/P7. The card is a **product**, not a file listing. Dates require **B4** fixed first (`created_at` is empty today, so ordering is arbitrary and "last ordered" is unrenderable). |
| 3 — Below fold | How It Works + Pricing → collapse to *"Need a refresher? →"*. | P4. |

**Empty gallery = first-run.** This is the highest-intent moment on the page and it currently
hides behind a toggle (B7). The drop zone should be **open by default, large, centred, in the
grid's place**, with the spec and the **template download** (Q5) inside it. The
*"No designs yet"* line then has no reason to exist.

---

### State D — Upload

**Job:** answer one question — *"will my artwork look right on the product?"*

| Slot | Content | Why |
|------|---------|-----|
| Drop zone | Spec **+ downloadable template** (Q5) **+ "auto-fit my image"** escape hatch. | P7. We demand an exact 1200×600 and offer no artboard and no recovery — just a hard reject (`:247`). That's a wall in front of the exact people we want (corporate designers). |
| Preview — **large, dominant** | The artwork **composited onto the bar**, not the bare file. | P1/P7. The bare 1200×600 preview answers "did my file upload?" The user is asking "does my product look right?" Those are different questions, and only one of them matters here. |
| Error | Attached **to the drop zone**, offering the fix (auto-fit / template), never a bare string. | B7-adjacent: `error()` dumps a raw rejection with no way forward. |
| On success | Explicit confirmation + the new card highlighted in the grid (B9). | Today the panel just closes — indistinguishable from a silent failure. |

---

### State E — Order  *(the $500–$10,000 decision)*

**Job:** confirm exactly what is being bought, for how much, arriving when. **Flip the emphasis.**

| Slot | Content | Why |
|------|---------|-----|
| **No frame above it.** | Order state suppresses the hero entirely. | P4. Today the biggest thing on screen at the moment of purchase is **a photo of a different product** (the 81% retail bar), and the user must scroll past it to buy. |
| Left, **large + sticky** | The **mockup of their design**, the dominant element on screen. | P6. Currently 130px tall in a 260px column with ~200px of dead space beneath — the smallest meaningful element in a $2,000 decision. |
| Right — controls | Qty → address → rates. Fix the state select (B11). Re-fetch rates on qty change (**B3**). Surface shipping errors (**B5**). | B3 is a money bug: it checks out at a shipping rate quoted for the wrong weight. |
| Right — **order summary**, directly above the button | `200 × $10 = $2,000` · `USPS Ground — $47.30` · **`Total $2,047.30`** · `200 trees planted` · `Est. delivery Aug 4`. | **There is no summary today**, and `Total: $2,000.00` (`:374`) **excludes shipping** — the number shown is not the number charged. The tree count is the emotional close and appears nowhere in the order state. |
| Button | Enabled state, or the blocker stated adjacent: *"Enter a shipping address to see rates"* (B6). | A greyed button with no reason is a dead end. |
| Secondary | *"Use a different design"* → back to gallery **and** to upload (B8). | |

---

### State F — Success  *(currently unreachable — B2)*

**Job:** the highest-anxiety moment in the funnel. They just wired $2,000 to a chocolate company.

| Slot | Content | Why |
|------|---------|-----|
| **Whole viewport, top of page, nothing above it.** | | P4/P6. This deserves the top of the page — not a panel that gets destroyed 200ms later by the gallery (**B2**). |
| Centre | **The mockup of what they bought** + `200 bars · $2,047.30 · Est. Aug 4` + order ref + *"Confirmation sent to brand@acme.com"* + **"You planted 200 trees."** | The design is **absent entirely** today. `Session ID: cs_test_a1b2…` (`:527`) is developer output, not a receipt. |
| Below | `View my designs` → gallery. | The exit, chosen — not forced. |

---

### State G — Error / degraded

**Job:** never strand the user. Today three separate paths (B1, B5, B7) end in silence.

| Case | Placement |
|------|-----------|
| Edgar unreachable at registration | Error **inside the form, form still visible** (fix the B1 parent-hiding trap), with retry. |
| GitHub 403 rate-limited (Q1-adjacent) | *"Can't load your designs right now — retry"* in the grid's place. Unauthenticated `api.github.com` = **60 req/hr/IP**, and the gallery costs **1 + N sequential** requests (`:175–190`); a corporate NAT can exhaust it. Batch with `Promise.all` regardless — the N+1 is also just slow. |
| Shipping quote fails | Message **in the rates block**, with the blocker named (B5). |

---

## 2.4 Sequenced plan — ONE PR per execution turn (§5a)

Each PR is self-contained, independently shippable, and lands in **`agroverse_shop_beta`** —
never prod (§3f; note Phase 1 violated this).

| Unit | Scope | Advance |
|------|-------|---------|
| **PR1** | **B1 + B2** — the two showstoppers. Delete the `#wl-auth-loading` write; move `#wl-auth-error` **out** of `#wl-auth-form`; make the `session_id` branch **return early** so `initAuth()` cannot destroy the success panel. **+ happy-dom tests that fail first** (§9). | _(auto)_ |
| **PR2** | **B3 + B4 + B5** — re-fetch rates on qty change + invalidate selection; switch upload to `submitEvent()` so `created_at` populates; surface shipping errors. Tests per §9. | _(auto)_ |
| **PR3** | **State A re-composition** — mockup as hero, kill duplicate photo (B10), invert to proof-before-ask (P2), DOM order for mobile (P3), pricing one-liner (B13), 5-up steps (B12). | _(auto)_ |
| **PR4** | **State C/D** — compact authed header, open-by-default drop zone (B7), template download (Q5 — **needs Gary**), composited previews (P7), upload confirmation (B9). | `gate: needs Q5 asset` |
| **PR5** | **State E/F** — order emphasis flip, order summary incl. shipping, blocker text (B6), state select (B11), route to upload (B8), real success receipt. | _(auto)_ |
| **PR6** | **UAT + promote beta → prod** | `gate: prod deploy` (always-stop, §5c) |

### Resume tracker

| Unit | PR opened | Merged (human) | Deployed | Contribution reported |
|------|-----------|----------------|----------|----------------------|
| **PR0** — commit the implementation + correct the mockup | ☑ [beta#182](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/182) | ☑ | n/a | ☑ |
| **D0** — confirm + flip the label spec | ☑ [beta#183](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/183) | ☑ | n/a | ☑ |
| PR1 — B1 + B2 | ☑ [beta#184](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/184) | ☑ | n/a | ☑ |
| PR2 — B3 + B4 + B5 | ☑ [beta#185](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/185) | ☑ | n/a | ☐ |
| PR3 — State A re-composition | ☑ [beta#187](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/187) | ☑ | n/a | ☐ |
| PR4 — State C/D | ☑ [beta#188](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/188) | ☐ | n/a | ☐ |
| PR5 — State E/F | ☑ [beta#189](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/189) (stacked on #188) | ☐ | n/a | ☐ |
| PR6 | ☐ | ☐ | ☐ | ☐ |

**Also landed this session (infra, outside the PR1-6 sequence):** [beta#186](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/186)
fixed `beta.agroverse.shop`'s CNAME — it was still claiming the apex domain from
before `agroverse_shop_prod` was split out, so GitHub Pages had no repo
registered for the beta subdomain (DNS was already correct). Beta is now
reachable at **https://beta.agroverse.shop/white-label/** — confirmed live,
serving PR2+PR3 (PR4/PR5 not yet merged, see below).

> **▶ RESUME HERE: review + merge PR4** ([beta#188](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/188)),
> **then PR5** ([beta#189](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/189), stacked on
> #188 — GitHub will auto-retarget it to `main` once #188 merges). Both are opened, tested
> (47/47 and 54/54 green respectively), and stopped here per §5c — merging to `main` is a human gate.
> PR4 ships Q5 (template download + auto-fit) as a generated interim rather than blocking on a
> designed asset from Gary; P7 (fully photorealistic composited previews) remains open pending a
> blank base-pouch asset, same gap class as Q5 — flagged in-code, not faked. Once PR4 + PR5 are
> merged, next turn resumes **PR6** (UAT + beta→prod promotion) — an always-stop gate requiring
> Gary's explicit review of the live beta site first.

---

### ▶ START HERE — handoff for the next agent

**Read in this order:** `OPERATING_INSTRUCTIONS.md` → this file top-to-bottom (§2.0 first) →
`agroverse_shop/js/white-label.js` (543 lines, the whole state machine) →
`agroverse_shop/white-label/index.html`.

**Before touching `agroverse_shop`:**
```bash
cd ~/Applications/agroverse_shop && git fetch origin main
git worktree add /tmp/wl-<unit> -b fix/white-label-<unit> origin/main
```
**Use a worktree — not `stash`+branch.** The DeepSeek session has ~20 uncommitted blog-post edits
in that working directory; a `git checkout` will clobber them
(`feedback_use_worktree_for_parallel_sessions`). PR0 already committed the white-label files and
the 4 files it depends on (`products.js`, `shared-chrome.js`, `index.html`, `checkout.gs`), so
`origin/main` has a complete, working copy of the feature — you do not need that dirty tree.

**Repo routing:** work lands in **`agroverse_shop_beta`**, never `agroverse_shop_prod` (§3f).
Phase 1 violated this; don't repeat it.

**How to verify (this is what found B1/B2/B4 — the existing UAT spec did not):**
```bash
cd ~/Applications/agroverse_shop && python3 -m http.server 8000 &
# Playwright drives each state with stubbed Edgar/GitHub routes, asserting
# console errors + which #wl-* sections are visible. Page-load-only tests
# cannot catch these — the bugs live in interaction handlers (§10 postmortem).
```
Per §9, every unit needs happy-dom/JSDom tests that **fail first**, then pass.

**Per unit:** one PR, then **stop** (§5a — the 30-round cap). Tick the tracker above, report the
DAO contribution (`truesight-dao-report-ai-agent-contribution`, contributor **`Claude Anthropic`**
for AI work), then the next turn resumes the next unit.

**Don't re-derive these — they're settled and cited:**
- B1 root cause: `#wl-auth-loading` doesn't exist; error element is trapped inside the hidden form.
- B2 root cause: two IIFEs race; `showGallery()` hides `#wl-success`.
- B4 root cause: `sign()` vs `submitEvent()` — only the latter injects `Timestamp`.
- The label is portrait; the mockup is already fixed; the **copy is not**.

✅ **Pre-flight Completeness (§5d):** no execution unit requires reading a file/state not already
captured here. Every mechanism above cites its file + line (`white-label.js`, `white-label.css`,
`index.html`, `dao.py:369`, `payload.ts:21`). The only external unknowns are **Q1–Q5**, which are
**decisions for Gary, not reads** — and only Q5 blocks a unit (PR4).

### UAT (§5, human-tested, on **beta** — never prod, never real money)

| # | Surface | Interaction | Acceptance |
|---|---------|-------------|------------|
| 1 | `beta` `/white-label/` | Enter a fresh email → *Start your design* | **"Check your inbox"** appears in place, card does not collapse (B1) |
| 2 | Inbox | Click the verification link | Lands in the gallery, verified |
| 3 | Gallery (empty) | — | Drop zone open by default; template downloads (B7/Q5) |
| 4 | Upload | Drop a 1200×600 PNG | Preview shows the label **on the bar**; explicit success (B9) |
| 5 | Upload | Drop an 800×400 PNG | Rejected **with a way forward**, not a bare string |
| 6 | Order | Address at qty 50 → change qty to 500 | Rates **re-fetch**; total = bars **+ shipping** (B3) |
| 7 | Order | Stripe **test card** `4242…` | Redirects to Stripe |
| 8 | Return | — | **"Order Placed"** with design + total + ETA — **not** "No designs yet" (B2) |
| 9 | Gallery | Upload 3 designs | **Newest first** (B4) |
| 10 | 390px | Full flow | Mockup **above** the email field (P3); no h-scroll |

---

## 2.5 Division of labor

**DeepSeek is active in `agroverse_shop/`.** This spec deliberately touches **no** files in that
repo — it is the *what and why*, for DeepSeek to execute as the *how*. Per
`feedback_use_worktree_for_parallel_sessions`, any agent picking up PR1–PR5 must use a **git
worktree**, not `stash`+branch, or it will clobber the other session's unstaged work.

**Verification method for Phase 2** (reusable): Playwright drives each state with stubbed
Edgar/GitHub routes, asserting console errors and which `#wl-*` sections are visible. This is what
found B1/B2/B4; the existing `tests/white-label-uat.spec.ts` did not, because it never fires the
interaction handlers (§10's exact postmortem).
