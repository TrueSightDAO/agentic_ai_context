# TikTok Shop — manual-first agentic ops experiment

**Status:** compiled 2026-11-28 (Sophia Truesight). Manual-first in progress; API registration blocked.
**Governor:** Gary Teh · **Track owner:** Envoy (Jira) / Sophia (execution)
**Epic:** [KAN-112](https://truesightdao.atlassian.net/browse/KAN-112) — Agroverse US DTC: TikTok agentic ops experiment
**Audience:** future AI agents and humans picking this up cold.

---

## 1. Why this is manual-first

The obvious architecture is: TikTok Shop API → orders → ledger. That path is **blocked twice over**, and both blocks are TikTok-side, not ours.

| Wall | Detail |
|---|---|
| **AM gate** | Registering as a **seller (in-house) developer** at `partner.us.tiktokshop.com` returns *"Account ineligible for seller developer registration — only sellers with an assigned account manager (AM) can register."* AM assignment is itself a growth-tier reward. |
| **Rate limit** | Falling back to **ISV** registration hit a signup rate limit. |

Root cause of hitting the AM gate at all: an email already tied to a seller account is **routed to the seller-developer path only** — you never get offered the ISV path. Registering under a fresh, non-shop email is the documented way to reach `developer type = ISV`.

**Decision:** don't block the commercial experiment on a TikTok org-chart decision. Run the experiment manually now; keep the API registration running in parallel (KAN-118).

### The API track, so nobody re-runs the same failure

- Register ISV at `partner.us.tiktokshop.com` (US market — `partner.tiktokshop.com` is rest-of-world) using an email that has **never touched a TikTok Shop**.
- Create app type **Custom** (not Public — public means App Store listing + multi-week review).
- Enable scopes: **Shop Authorized Information**, **Order Information**, **Product Basic** (+ Finance optional).
- Capture **App Key / App Secret / Service ID**. Secret goes to the vault — never a repo, never an env file, never chat.
- Authorization: `https://services.us.tiktokshop.com/open/authorize?service_id=<SERVICE_ID>&state=<single-use>` → returns `code` (30 min, single-use) → exchange at `GET https://auth.tiktok-shops.com/api/v2/token/get` (`app_key`, `app_secret`, `auth_code`, `grant_type=authorized_code`).
- Business calls: `https://open-api.tiktokglobalshop.com`, with `app_key`, `timestamp` (10-digit Unix **seconds**), `sign` query params + `x-tts-access-token` header. `sign` = hex HMAC-SHA256 over `app_secret + path + sorted-params + body`, keyed with `app_secret`.
- **Access token lives 7 days.** Any integration needs a scheduled refresh loop or the channel dies weekly. Design this in, don't bolt it on.
- Live shop likely can't authorize a development app; test against a **Development Shop** test account until review clears.

⚠️ Do **not** conflate this with the **TikTok Content Posting API** (`developers.tiktok.com`) — separate product, separate app, separate review. See `MEDIA_ARCHIVE_PIPELINE.md`, which treats TikTok as a media *distribution* consumer.

---

## 2. Where the tracking lives

**Canonical content spreadsheet:** `1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ`

TikTok was added as three tabs **inside the existing content workbook**, beside `Instagram Content Schedule` and friends — not in a new silo. TikTok is a content channel; its ops belong with content ops.

### `TikTok Content Schedule`
Mirrors the Instagram tab's shape so anyone who knows one knows the other.
`primary_key · status · Week · Date Range · Theme Focus · Post Day · Day of Week · Post Type · Theme · Description · Caption · Hashtags · CTA · Sound / Audio · Tool Suggestions · Published Video URL · Posted By · Shop Product Tagged · Experiment Arm · Notes`

### `TikTok Video Metrics`
Leading indicators — explicitly **not** the success metric.
`snapshot_date · primary_key · video_url · views · likes · comments · shares · saves · avg_watch_secs · followers_gained · profile_visits · product_clicks · shop_orders_attributed · notes`

### `TikTok Orders`
The outcome. This tab is what makes the experiment measurable.
`order_date · tiktok_order_id · sku · qty · gross_revenue_usd · status · attributed_primary_key · attributed_video_url · customer_note · ledger_row_ref`

**Why Orders is a separate tab from Metrics:** it structurally prevents the classic error of concluding "the video did well, therefore it sold product." Views live in one place, money in another. You can't accidentally read one as the other.

---

## 3. Experiment arms

Recorded in the spreadsheet's `Configuration` tab alongside the status vocabulary.

| Arm | Setup | What it isolates |
|---|---|---|
| **A** | Listening only — no product tags | Organic discovery baseline |
| **B** | Product tagged on a **new** video | Tag lift on fresh content |
| **C** | Product tagged on an **existing high-performing** video | Retro-tag lift (uses KAN-115's top videos) |

A is the control. Without it, B and C have no denominator and any lift is unattributable.

---

## 4. The success metric (KAN-119)

**Primary:** TikTok Shop attributed **orders and gross revenue** — read off the `TikTok Orders` tab — over a **2–4 week** window.

**Explicitly not a metric:** views, likes, comments, shares, followers. These are recorded in `TikTok Video Metrics` as leading indicators only. Engagement is a hypothesis about the path to revenue, not the goal.

**Attribution rule (must not be fudged):** an order counts toward an arm only if (a) a real `tiktok_order_id` exists in Seller Center, **and** (b) `order_date` falls inside that arm's window. "I think that sale came from TikTok" does not count. This rule exists because it is the single easiest place to accidentally lie to ourselves.

---

## 5. Logging cadence

Deliberately minimal. A cadence that isn't kept is worse than no cadence — it produces a sparse table that looks like data.

| When | Time | What |
|---|---|---|
| **Daily** | ~5 min | New orders → `TikTok Orders`. Snapshot `TikTok Video Metrics` for videos posted in the last 7 days. |
| **Weekly (Mon)** | ~15 min | Full metrics snapshot for **all** live videos. Status sweep on `TikTok Content Schedule`. |

---

## 6. Pre-existing drift found while verifying (NOT fixed — out of scope)

Flagged because it affects whether any comparison is trustworthy:

- **`Published Content Index` holds only 2 data rows** despite the org having far more published assets.
- **`F5 Content Schedule` is header-only** (0 rows) — the forward calendar is effectively empty.
- **Instagram tab status vocabulary is inconsistent:** it uses `PROPOSED` and `SUPERSEDED`, neither of which appears in `Configuration`'s "Instagram Reel Status" list; and **182 of 245 rows have a blank status (74%, measured 2026-11-28)**. This has been loosely described in conversation as "~95% empty" — the measured figure is 74%, and the precise number matters because it is the evidence base for building TikTok tracking cleanly from day one.

**Consequence:** do **not** use the Instagram tab's status counts as a reliable denominator for any TikTok-vs-Instagram comparison. TikTok is being tracked cleanly from day one rather than inheriting this. Worth its own follow-up if comparisons matter.

---

## 7. Task map

| Key | Task | Blocked on |
|---|---|---|
| KAN-113 | List 1–3 existing Agroverse products manually in Seller Center | Gary (manual) |
| KAN-114 | Tracking tab + manual logging cadence | ✅ **Verified live 2026-11-28.** All 3 tabs exist with documented columns; all 3 are header-only pending data. Moved to Done. |
| KAN-115 | Performance data on ~18+ existing @thecacaofanatic videos | 🟨 **In Progress 2026-11-28.** Gary captures views/date/caption (+person-in-frame, content type); Sophia writes rows and does the differentiator analysis. |
| KAN-116 | New content matched to existing account voice | KAN-115 |
| KAN-117 | Tag products in new + existing high-performing videos | KAN-113, KAN-115 |
| KAN-118 | API registration (ISV + AM request) | TikTok rate limit / AM gate |
| KAN-119 | Define + track the real success metric | ✅ defined; needs order data |

---

## 7a. KAN-113 — the manual listing path has its own gate (verified 2026-11-28)

**The assumption this section exists to kill:** that skipping the API (KAN-118) also skips the restrictions. It does not. There are **two independent gates**, and only one of them is about developer access.

| Gate | Applies to | Blocks |
|---|---|---|
| Partner Center / ISV registration | anyone wanting API access | KAN-118 |
| **Category qualification (this one)** | **anyone listing food, API or not** | KAN-113 |

**Packaged Food and Beverage is a RESTRICTED category** per TikTok Seller University §3.3. Chocolate, sweets and snacks fall explicitly inside the covered list. Documentation required at listing time:

1. Proof of a valid **FDA registration**
2. **A complete set of images of the product's packaging and labeling**, including all information printed on the pack

Sellers are additionally responsible for NLEA (nutrition labeling), FD&C Act and FPLA compliance. And the operative sentence: *"Products in restricted categories cannot be listed until qualification is approved."*

**Verified path to the real answer:** Seller Center → Settings → My Account → **Qualification Center → Category Qualification**. TikTok surfaces the exact document list for the account and region there. Do not research this from blogs — the account-specific list is authoritative and takes five minutes to obtain.

**What this doc does NOT assert:** whether TrueSight holds a valid FDA facility registration. The repo contains extensive **FDA FSVP** material (supplier entities, prior notices, import entries), but FSVP supplier records and import prior notices are *different instruments* from a facility registration for the selling entity. Do not conflate them when answering TikTok.

### Referral fee (for unit economics)

Food & Beverages carries a **6% referral fee** — consistent across all sub-categories (Pantry Food, Snacks, Drinks). Calculated on `(customer payment + platform discount − tax)`. Creator commission is seller-set; food open-plan norms run ~10–15%. So a $30 bag nets roughly **$23.70** before shipping and affiliate.

### Listing slate — chosen from live stock, not from preference

From `skus.json` (generated 2026-11-28T02:29:53Z). Every retail SKU except these four sits at **zero stock**, so listing them would generate refunds rather than data.

| SKU | Price | Stock | Role |
|---|---|---|---|
| `ceremonial-cacao-paulo-s-la-do-sitio-farm-200g` | $30 | 170 | hero / flagship |
| `8-ounce-organic-cacao-nibs` | $25 | 131 | shelf-stable snack |
| `cacao-mass-bar-500g-ilheus-2024` | $60 | 37 | high-AOV alternative |
| `organic-81-dark-chocolate-bar-50g-vivi-jesus-do-deus` | $10 | 35 | $10 impulse entry |

**Recommended three:** ceremonial 200g + Vivi 50g bar + 8oz nibs — three price points ($10/$25/$30) across three sub-categories, so attribution learns *which product type* converts rather than measuring one product three ways.

> ⚠️ **Superseded 2026-11-28** by the governor's decision to launch a **single SKU** (`ceremonial-cacao-paulo-s-la-do-sitio-farm-200g`). See **§9.4**. The three-price-point rationale below stands as recorded reasoning; it is not the current plan.

---

## 8. Standing risk: empty tabs are not a build failure

Verified 2026-11-28: `TikTok Content Schedule`, `TikTok Video Metrics` and `TikTok Orders` are all **header-only (0 data rows)**. That is the correct pre-data state, not a defect — KAN-115 supplies metrics, KAN-113 supplies listable products, and order rows only exist once something sells.

The failure mode to avoid is subtler than "the tab is empty". It is reaching week 6 with *nine* filled rows out of forty planned, and then reading a decision off that table as though it were the population. The Instagram tab demonstrates the shape of this: a 245-row schedule where the status column is blank on 182 rows is not a 245-row plan, it is a 63-row plan wearing a 245-row costume.

So the cadence in §5 is the deliverable, not the tab. If the cadence lapses, the honest response is to say the experiment has no data — not to compute a rate off whatever happens to be present.

---

## 9. KAN-113 decision record (2026-11-28) — one SKU, brand Agroverse, exemption route

Governor decisions taken this date, plus two findings that changed the §7a recommendation.

### 9.1 The three gates are independent

§7a established that skipping the API does not skip the restrictions. There are now **three** gates, and they clear separately. Treating any two as one gate is what stalls a launch for weeks.

| Gate | Applies to | How it clears |
|---|---|---|
| **Category qualification** (restricted: Packaged Food & Beverage) | any food listing, API or not | Qualification Center → Category Qualification |
| **FDA facility registration** | the selling entity | document uploaded during qualification |
| **GTIN** | most categories, **exemption available** | Catalog → GTIN Exemptions |

**Brand** is a fourth, lighter step: select an existing brand or "Add a brand". Decided: **Agroverse**. Note the coupling — if a listing carries a GTIN, the brand must match the brand that GTIN is licensed to.

### 9.2 GTIN is not a hard prerequisite (correcting an earlier reading)

An earlier pass treated missing GTINs on the 81% bars as a reason to prefer other SKUs. That was too strong. TikTok's own Seller Academy documents a **GTIN exemption** for private-label, handmade, or brands that do not use UPCs. Per TikTok's walkthrough:

1. Seller Center → **Catalog → GTIN Exemptions → Apply for GTIN exemptions**
2. Store information (up to 3 store URLs — optional, but speeds review)
3. Up to **10 categories**, then up to **100 product types**. The exemption covers **only the types ticked**.
4. Choose brand per line (type "Unbranded" if none — not our case now)
5. Reason, then Submit. Status starts **Processing**.
   - **Needs info** → respond within **5 days** or the request auto-closes
   - **Approved** → wait **≥ 4 hours** before creating items so the system updates

Because the exemption is granted per product type under a category, it is **downstream of** category qualification in practice. Sequence qualification first.

### 9.3 Our existing GTINs carry ownership risk

Both codes we hold check-digit correctly, but the prefix is the problem:

| GTIN | Length | Check digit | Prefix | Prefix owner (GS1) |
|---|---|---|---|---|
| `860010660232` | 12 | ✅ valid | `860` | **GS1 Serbia** |
| `860010660218` | 12 | ✅ valid | `860` | **GS1 Serbia** |

Both share the single company prefix `860010660` — the signature of a **bought-in barcode block**, not a prefix licensed to the brand owner. GS1 prefixes do not indicate country of origin, so a Serbian prefix on Brazilian cacao is not itself an error; the error would be **not owning the prefix**.

TikTok validates GTINs via **GEPIR and GTIN.cloud** to confirm the UPC Company Prefix is licensed to the seller as brand owner. Other marketplaces have delisted sellers for exactly this shared-prefix pattern. **A GTIN that fails ownership validation is worse than no GTIN** — it risks listing rejection or account action, whereas an approved exemption is clean and sanctioned.

**Decision: take the exemption route. Do not buy more barcodes.** Buying a resold block is what created this exposure. Before those codes are used on any marketplace, verify `860010660` in GEPIR.

### 9.4 Launch slate: one SKU

Governor decision: **list one single-estate SKU**, not a variant spread. The launch SKU is `ceremonial-cacao-paulo-s-la-do-sitio-farm-200g` — $30, 170 units, Paulo's farm, Pará, 2024 harvest.

**Why one.** One estate = one lot = one packaging-photo review, one ingredient/nutrition transcription, one qualification submission. Four variants would screenshot the same buyer behaviour while multiplying the review surface. Identical reasoning to the China entry, where one estate resolved the consolidation objection.

**What it costs.** §7a chose three price points so attribution could learn *which product type* converts. One SKU measures one product's conversion rate instead. Accepted: KAN-113 asked for 1–3, and KAN-115 / KAN-117 carry the content-side learning.

**Why this SKU.** It is the only product clearing all three gates at once — exemption-eligible, deepest stock (no refunds-as-data), and one farm / one harvest / one lot so the photography and ingredient transcription happen once.

### 9.5 Estate naming — open, and it is two different questions

Governor's instinct: lead with the brand, don't name the estate. Two readings, not one:

- **Reading A** — brand is the headline, estate is named as substantiation (`Agroverse Single Estate … Paulo's Farm, Pará`).
- **Reading B** — estate never named in the listing; name lives only in the QR / batch record.

**Recommendation: A.** A **named single estate** is the first of four documented positioning pillars. Unnamed, "single estate" is indistinguishable from a label assertion — every craft chocolate brand already claims single origin. The name is what makes it checkable. B also fights the QR (the name is one scan away) and risks a mismatch between the listing and the pack images qualification reviews.

**The one legitimate case for B is disintermediation** — fear of a buyer going direct to the farm. That is not solved by B, since the name is in the QR record either way. The real fix is the **QR landing page**: batch, lot, region, harvest, assay, traceability chain, *without* the farm's contact identity.
