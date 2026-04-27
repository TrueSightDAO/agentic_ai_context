# Retailer Funnel Proposal — agroverse.shop

**Status:** **Implemented 2026-04-27** (see §9 below for shipped PRs). Originally drafted in response to retailer feedback from Davi (Jupiter Row), 2026-04-27.
**Sibling docs:** `LEAD_LIST_EXTRACTION.md` (how we *find* retailers), `RETAILER_ONBOARDING_PLAYBOOK.md` (what happens after they say yes), `PARTNER_OUTREACH_PROTOCOL.md`. This document covers what happens **on the website** between "they heard of us" and "they're ready to talk".

> **Decisions Gary made on §6 open questions** (encoded in shipped code):
> 1. Container: **C** (full `/wholesale/` page + thin PDP banner).
> 2. Audience: **retailer primary**, with a one-line corporate-gifting capture at the bottom of the page.
> 3. Pricing: **published openly** — no form gate.
> 4. Sample-pack SKU: **mailto only** for now (limited inventory makes a self-serve listing oversell-prone).
> 5. Stockist list: **USA partners only** (27 shops linked).
> 6. CTA email: **`community@agroverse.shop`** (no new alias).
> 7. MOQ: **split by path** — consignment 5 bags, wholesale-bought 10 bags.

---

## 1. The gap Davi exposed

> "I went to your website and did not see any packaging to explore what your product looks like. In your search for retailers may I suggest having some images of your products on shelves as this is the best way to see if it's a fit." — Davi, Jupiter Row

Davi passed before reaching out. The signal:

- Our **packaging story** lived in our outbound replies, not on the site.
- Our **shelf-presence proof** (Go Ask Alice, Lumin Earth, Green Gulch, Edge & Node, Heierling, Kiki's, Queen Hippie Gypsy, Whole Body Repair Clinic, etc.) was scattered across partner pages, not bundled.
- Our **differentiator** (QR traceability → farm provenance → Amazon reforestation) lived in Gary's Jupiter Row reply, nowhere else.

**Already shipped (PR #76):** Front + back packaging on 3 PDPs; on-shelf photos on 3 partner pages. That closes the literal gap Davi raised.

**This proposal addresses the next layer:** how a future Davi self-serves to "yes" without an email round-trip.

---

## 2. Goal

A retailer (or premium gift-buyer) who lands on agroverse.shop should be able to answer the following without emailing us:

1. What does the product look like? *(closed by PR #76 on PDPs)*
2. What does it look like on someone's shelf? *(closed by PR #76 on partner pages)*
3. Why is this different from any other ceremonial cacao? *(QR traceability, single-estate, tree planting)*
4. What's the wholesale economics? *(price, MOQ, margin, lead time)*
5. Who else is selling it? *(social proof — list of stockists)*
6. What are the lab / safety credentials? *(heavy metals, FDA, organic)*
7. How do I move forward? *(one clear CTA)*

PR #76 closes 1 and 2. This proposal is about 3–7.

---

## 3. Container options (pick one — these are the strategic forks)

### Option A — Dedicated `/wholesale/` page

A single canonical destination linkable from PDP footers, partner pages, the site footer, and outreach emails.

**Pros**

- Clean information architecture; doesn't dilute the consumer-facing PDP experience.
- Can grow over time (FAQs, downloads, regional logistics) without polluting other pages.
- Linkable URL we can include in every Hit List email, Instagram bio, and partner referral.
- SEO surface for "wholesale ceremonial cacao" / "white-label cacao supplier" queries.

**Cons**

- Only as good as the inbound traffic to it — must be deliberately linked from PDPs, partner pages, footer, homepage hero.
- Builds a second mental model on the site (consumer site + B2B site).

### Option B — Shared "Why retailers stock us" block, embedded across PDPs and homepage

Inline section on every PDP and the homepage that bundles QR traceability + shelf photos + stockist list + a "wholesale inquiry" CTA.

**Pros**

- Highest reach — every product page reaches both consumers and retailers.
- Reuses the visitor's existing scroll path; nothing new to discover.

**Cons**

- Adds clutter for direct-to-consumer shoppers who don't care about wholesale.
- Harder to evolve — every change ships to N pages.
- Mixes two audiences with very different intents on the same scroll.

### Option C — Both: dedicated `/wholesale/` page + a thin banner on PDPs

A full wholesale page (Option A) plus a small "Selling Agroverse in your store? See wholesale info →" banner on each PDP that deep-links there.

**Pros**

- Best of both: depth where it's wanted, discoverability where buyers actually land.
- Banner is cheap to add and easy to remove if it underperforms.
- Lets the wholesale page evolve independently.

**Cons**

- Two surfaces to maintain.
- Banner placement is a UX call (above-the-fold steals attention from consumer CTA; below-the-fold may not get seen).

### Option D — Lightweight downloadable one-pager (PDF)

A `/wholesale-overview.pdf` we attach to outreach emails, no website page.

**Pros**

- Zero website change. Fast to produce.
- Solves the "Davi-style" buyer who wants to see specs after we email them.

**Cons**

- Doesn't help inbound discovery (Davi found us via search/site, not email).
- PDFs go stale; not SEO-discoverable; harder to update.
- Doesn't serve the next Davi who lands cold.

---

## 4. Recommended content bundle (modular — same regardless of container)

Whichever container we pick, the content is roughly:

1. **Hero** — front + back packaging (already produced); short pitch line: "Single-estate, QR-traced ceremonial cacao from Brazilian smallholder farms. Every bag plants a tree in the Amazon."
2. **Shelf-proof gallery** — 6-9 photos pulled from existing partner pages (Go Ask Alice, Lumin Earth, Green Gulch, Edge & Node, Heierling, Kiki's, Queen Hippie Gypsy, etc.) with retailer names as captions.
3. **Why it sells** — Gary's Jupiter Row reply, restructured as 5 bullets:
   - The farm this bag came from + named farmer
   - The farm's location (interactive map, like AGL pages)
   - The story behind the farm
   - Lab reports (heavy-metals absence, FDA / ANVISA)
   - Each bag plants a tree → customer gets satellite imagery of *their* tree
4. **The QR code, in 30 seconds** — embed the Instagram reel (`https://www.instagram.com/p/DJqW8TRtJK3/`) or a short hosted clip; show a mock QR scan flow.
5. **Stockist list** — text list of all current retailers, linking to existing partner pages.
6. **Wholesale economics** — price tier, MOQ, suggested retail markup, lead time, freight.
7. **Lab + safety** — link to the heavy-metals lab reports already published with shipments (AGL4, AGL8, etc.).
8. **CTA** — see §5.

---

## 5. CTA options (pick one or two)

| CTA | Friction | What it gets us | Best for |
|---|---|---|---|
| **Wholesale inquiry form** (Google Form / Tally) | Low | Structured leads with shop name, location, current stockists, est. volume | Inbound from cold visitors |
| **`mailto:wholesale@agroverse.shop`** | Lowest | Free-form email; current default | Already-warm leads who'd email anyway |
| **"Book a 15-min intro call"** (Calendly) | Medium | Real conversation; shorter sales cycle | Buyers like Davi who'd value a human |
| **Sample pack purchase** ($X for 1 bag of each origin) | High | Self-qualifying — buyer has skin in the game | Buyers who want to taste before deciding |

**Recommendation:** form **+** sample-pack purchase. The form captures everyone; the sample pack converts the curious into committed without our time.

---

## 6. Open questions for Gary

1. **Which container option** (A / B / C / D)? Default recommendation: **C** (full `/wholesale/` page + thin PDP banner) — bundles depth with discoverability.
2. **Audience emphasis:** retailer-only, or retailer + premium-gift-consumer (the latter buys cases, gives as gifts, would value the same story)?
3. **Wholesale economics** — are price tiers / MOQ / margins ready to publish, or do we keep that gated behind the form?
4. **Sample pack** — is the SKU fulfillment ready (existing inventory + ledger / QR codes) to support a "$X for 3-bag sampler" listing, or is that out of scope?
5. **Stockist list** — publish the full list, or curate (some stockists may prefer not to be advertised)?
6. **CTA email** — `wholesale@agroverse.shop` or reuse `community@agroverse.shop`? If the former, who owns triage?

---

## 7. Effort estimate (if we pick Option C)

| Task | Estimate |
|---|---|
| Wholesale page (`/wholesale/index.html`) — DApp page conventions, mobile, OG/Twitter cards | 0.5 day |
| Pull existing partner shelf photos into a unified gallery | 0.5 day |
| Wholesale inquiry form (Google Form embed) | 1 hour |
| Thin PDP banner + footer link | 1 hour |
| Stockist list — auto-generate from partners directory | 1 hour |
| Lab-report links wired to existing AGL pages | 30 min |

Total: ~1 working day after decisions are made on §6.

---

## 8. What this proposal is *not*

- Not a redesign of the consumer-facing site.
- Not a separate B2B subdomain (`wholesale.agroverse.shop`) — same site, dedicated path.
- Not a CRM / pipeline tool — out of scope here; current Hit List + DApp Remarks workflow is adequate.
- Not a price-list overhaul — see `AGROVERSE_PRICE_LIST_AND_ASSETS.md`.

---

## 9. Implementation (shipped 2026-04-27)

| Layer | What landed | PR |
|---|---|---|
| Packaging on PDPs + on-shelf photos on partner pages | Front/back of bag on 3 ceremonial-cacao PDPs; "Agroverse Cacao on the Shelves" gallery on Green Gulch, Go Ask Alice, Lumin Earth | [agroverse_shop_beta#76](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/76) |
| `/wholesale/` page + PDP banners + footer | Full retailer page (packaging hero, why-it-sells, shelf-proof gallery, pricing, stockist list, lab links, CTAs); thin banner on all 11 PDPs; footer link on home + 33 partner pages | [agroverse_shop_beta#77](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/77) |
| Section + CTA alignment fix | Alt-background section H2s and hero CTAs aligned across all viewports | [agroverse_shop_beta#78](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/78) |
| Lab-reports bullet alignment | `<ul>` left edge aligned with section content | [agroverse_shop_beta#79](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/79) |
| Pricing split: consignment (5) + wholesale-bought (10) | Two-card pricing block; same product/price, different opening-order MOQ + ownership semantics | [agroverse_shop_beta#80](https://github.com/TrueSightDAO/agroverse_shop_beta/pull/80) |
| Warm-up draft cites `/wholesale/` as visual companion | Static template + Grok system prompt + style guide updated | [go_to_market#76](https://github.com/TrueSightDAO/go_to_market/pull/76) |

**Live page:** https://agroverse.shop/wholesale

**Where the canonical pricing lives now:** `AGROVERSE_PRICE_LIST_AND_ASSETS.md` (post-rollout: documents both consignment and wholesale-bought paths and links to the page).

**Follow-ups not done in this rollout:**

- Sample-pack SKU as a real e-commerce listing (deferred — limited inventory makes oversell risk real; mailto stays the gate).
- Footer Wholesale link on shipment pages, blog posts, cacao-journeys (deferred — wait on inbound traffic data before sweeping).
- Founderhaus partner page footer (Brazil-based; outside USA stockist scope).
- Corporate-gifting `/gifts/` sibling page (wait for signal — captured today as a one-line CTA).
