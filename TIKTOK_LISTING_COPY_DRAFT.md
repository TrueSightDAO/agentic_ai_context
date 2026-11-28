# TikTok Shop — listing copy drafts (KAN-113)

**Status:** drafted 2026-11-28 (Sophia Truesight); **revised 2026-11-28** to a single-SKU slate per governor decisions (§0a). Pending category qualification + GTIN exemption + pack data.
**Governor:** Gary Teh · **Parent:** [KAN-113](https://truesightdao.atlassian.net/browse/KAN-113) · **Blocks:** nothing — ready to paste once qualification clears.

> **Nothing in this document has been submitted to TikTok.** No products created, no sheet cells written.
> Source of truth for prices/stock/GTIN: Main Ledger `Agroverse SKUs` tab, read 2026-11-28.

---

## 0. Why this exists before the decisions are made

The *listing* is gated by category qualification, a GTIN route, and pack data. None of those gate the *copy*. Titles, descriptions, specs and compliance fields are reusable regardless of the final SKU mix, which is why this was drafted before the slate was settled.

---

## 0a. Governor decisions (2026-11-28) — slate collapsed to ONE SKU

| Decision | Governor's call | Effect on this doc |
|---|---|---|
| **Brand** | **Agroverse** | §2 brand field resolved. Needs Agroverse selectable in the brand dropdown, or added via "Add a brand" first — and it must match the brand the GTIN (if any) is licensed to. "Unbranded" is no longer used. |
| **Slate size** | **One single-estate SKU at launch**, not a 3-variant spread | §3 is the **only** live listing. §4, §5, §6 are parked drafts, kept because the copy is reusable. |
| **Estate naming** | **RESOLVED — Oscar's** (2026-11-28) | §0a.1–0a.3 below. Two consequences the decision surfaces: the launch SKU changes (§0a.1), and the naming advice **inverts for bars** (§0a.3). |

**Why one SKU is the better call, independent of preference.** One estate = one lot = one packaging-photo review, one ingredient/nutrition transcription, one qualification submission. A four-variant launch multiplies the review surface while returning the same learning — all four would screenshot the same buyer behaviour. This is the same reasoning that settled the China SKU format (one estate = one lot = one GACC/CIFER filing). Ship one, iterate.

**What it deliberately gives up.** `TIKTOK_SHOP_AGENTIC_OPS.md` §7a argued for three SKUs across three price points ($10 / $25 / $30) so attribution could learn *which product type* converts. With one SKU the experiment measures one product's conversion rate, not product-type fit. That is an acceptable trade now: KAN-113 asked for 1–3, and KAN-115 / KAN-117 supply the content-side learning.

### 0a.1 Estate = Oscar's — and it moves the launch SKU

Governor decision 2026-11-28: **the estate is Oscar's.** Verified against `skus.json` (`generatedAt` 2026-11-28T09:28:46Z): the `farm` field confirms four distinct estates — **Paulo**, **Oscar**, **Vivi**, **Fazenda Santa Ana** — so "Oscar's" is unambiguous.

**⚠️ But Oscar's + ceremonial cacao has nothing to ship.**

| SKU | Farm | Price | Stock |
|---|---|---|---|
| `oscar-bahia-ceremonial-cacao-200g` | **Oscar** | $25 | **0** |
| `ceremonial-cacao-paulo-s-la-do-sitio-farm-200g` | Paulo | $30 | **170** |

This section previously assumed the Paulo's 200g bag (170 units) was the launch SKU. Naming **Oscar's** makes that impossible: the 170-unit bag is a different farm, and Oscar's ceremonial bag is at zero. Listing it would generate refunds, not data.

**Oscar's in-stock products — the real launch candidates:**

| SKU | Price | Stock | Form |
|---|---|---|---|
| `8-ounce-organic-cacao-nibs` | $25 | **131** | nibs |
| `cacao-mass-bar-500g-ilheus-2024` | $60 | **37** | cacao mass |
| `organic-81-dark-chocolate-bar-50g-oscar-bahia-2024` | $10 | **34** | finished bar |

**Recommended: the 81% bar.** It is the named estate (`Oscar's Farm, Bahia` in `productName`), it is literally "the chocolate bar" from the original GTIN question, and 34 units is a real first batch. The 8oz nibs carry more stock, but Oscar's farm there is a *sourcing* attribution rather than a branded estate claim.

> ⚠️ **§3 below still contains the Paulo's ceremonial listing and is NO LONGER the launch listing.** It is retained as the reusable template. Rewriting §3 around the Oscar's bar is the next unit.

### 0a.2 The launch-SKU question, and whether to switch estates instead

Two coherent resolutions; this doc recommends the first:

- **(i) Keep Oscar's, change product → the 81% bar.** Estate decision honoured, deepest in-stock Oscar's finished good, and the bar is the stronger TikTok visual anyway.
- **(ii) Keep ceremonial cacao, change estate → Paulo's.** Keeps the 170-unit bag and the $30 AOV, but *contradicts* the governor's estate decision.

This doc cannot choose between a governor's decision and a stock constraint — **(i) is recorded as the recommendation, (ii) as the alternative.** Flag which is intended and §3 is rewritten accordingly.

### 0a.3 The pack is anonymous — which inverts the naming advice for bars

§7 treated the single shared packaging photo across four bar variants as a defect. OCR of that image (`81-dark-chocolate-bar-50g-packaging.jpg`, 1597×900) shows otherwise:

> *"81% Brazil Single Estate Chocolate — Saving our Amazon Rainforest, one cacao at a time…"*

**The wrapper names no farm.** "Single Estate" is the claim; the estate is withheld on the pack itself. That explains why one photo legitimately serves all four variants — the pack genuinely is generic — and it **downgrades §7's shared-photo finding** from a blocker to a cosmetic gap. Per-variant photos would be nice; they are not required by the pack.

**But it reverses the naming advice for bars.** §9.5 of the ops doc argued for naming the estate in the listing, on the grounds that an unnamed estate is an unverifiable label claim. That logic holds for a **farm-specific ceremonial bag** (where the bag itself is the farm's). It does *not* hold for a **bar whose own packaging says "Brazil Single Estate" and names nothing**: a TikTok listing titling itself "Oscar's Farm" while the pack in the review photos says only "Brazil" reads as a listing-vs-pack mismatch, which is precisely what qualification review checks.

**Revised guidance:**

| Product form | Title should say | Why |
|---|---|---|
| Farm-specific ceremonial bag (Paulo's 200g) | **Name the farm** | The bag wrapper *is* the farm's; the name matches the pack and is the differentiator |
| 81% bar | **"Single Estate, Brazil"** — estate named in description/QR, not the title | Matches the anonymous pack; naming it in the title creates the mismatch |

The estate decision still does real work either way: it determines **which SKU** is listed and **which lot the QR resolves to**. It just should not be printed on a title whose packaging prints something else.

---

### The estate-name question, stated properly

"Single estate without specifically naming the estate" has two possible readings, and they are not the same decision:

- **Reading A — humanise, don't anonymise.** The listing leads with the **Agroverse** brand, and the farm appears as a named place (`Paulo's farm, Pará`). The *brand* is the headline; the estate is the substantiation underneath it.
- **Reading B — anonymise.** The listing says "single estate, Brazil" and never names the farm. The name lives only in the QR / batch record.

**Recommendation: A.** The documented positioning puts a **named single estate** as the *first* of four pillars — *"no shelf found … combines a named single estate, vintage/lot, third-party lab testing, and per-unit QR traceability."* Drop the name and three of four survive, but the one a shopper grasps in two seconds without scanning anything is gone. "Single estate" *unnamed* is indistinguishable from a label claim; every craft chocolate brand already says "single origin." The name is what makes the claim checkable rather than asserted.

Three practical objections to B:

1. **It contradicts the QR.** Our differentiator is a per-unit code resolving to farm and harvest. If the QR page names the farm — and it should, that is the entire point — the listing withholding it is a speed bump, not a protection. The name is one scan away.
2. **Qualification compares listing against pack.** The packaging/label images submitted are reviewed against what the listing says. If the wrapper or back label prints the farm, a listing that omits it reads as a mismatch.
3. **The category's own convention is named origin.** Ceremonial cacao buyers actively ask where a cacao is from; named-origin competitors name theirs. An unnamed estate reads as commodity to precisely the smallest viable audience we want.

**The one legitimate reason to withhold — disintermediation.** If the concern is a buyer going direct to the farm and cutting us out, that is real and it is not answered by Reading A or B, because the name is in the QR record either way. The correct fix is the **QR landing page**: show batch, lot, region, harvest, assay and the traceability chain *without* the farm's contact identity. Which of the two is the actual worry changes the recommendation — flag it and this section gets rewritten.

---

## 1. Non-negotiable copy constraints

Cacao sits in TikTok's **restricted Packaged Food & Beverage** category (§7a of `TIKTOK_SHOP_AGENTIC_OPS.md`). Restricted status raises the bar on what copy may claim, because the label images submitted for qualification must match what the listing says.

**Prohibited in all copy — no exceptions:**

| Never write | Why |
|---|---|
| "superfood", "ancient superfood" | implied health claim |
| "anti-inflammatory", "antioxidant", "detox", "boosts immunity" | disease/health claims absent FDA-authorised wording |
| "lowers blood pressure", "improves mood", "better than coffee" | drug-adjacent claims |
| "cures", "treats", "prevents" | outright drug claims |
| "100% organic" unless certified | organic claims need certification on file |

**Safe territory:** provenance (farm, region, harvest year), process (fermented, sun-dried, stone-ground), sensory description (tasting notes), use-case (how to prepare), culture and craft, farmer relationship. Provenance is both compliant *and* our actual differentiator — no need to reach for a health claim.

**Marked `CONFIRM FROM PACK`:** every ingredient list, nutrition panel, net-weight statement and allergen line below. These must be transcribed from the physical packaging, not inferred. An invented ingredient line is a compliance misrepresentation and it is exactly what qualification checks against.

---

## 2. Shared fields (all products)

| Field | Value |
|---|---|
| Brand | Agroverse |
| Category | Food & Beverages → Pantry Food (ceremonial, nibs) / Snacks (bars) |
| Country of origin | Brazil |
| Region | Bahia (Oscar, Vivi, Santa Ana, São Jorge) · Pará (La do Sitio) |
| Seller / warehouse location | CONFIRM — must match the FDA-registered facility |
| Shipping | CONFIRM carrier + lead time |
| Return policy | CONFIRM |

---

## 3. `ceremonial-cacao-paulo-s-la-do-sitio-farm-200g` — RECOMMENDED, lead listing

**Ledger record:** $30.00 · 200g (7.05 oz) · **stock 170** · shipment AGL8 · farm Paulo · **GTIN 860010660232**

**Title** (≤ 120 chars; front-loads what a buyer searches):

> **Variant A (recommended — brand-lead, estate substantiates):**
>
> Agroverse Single Estate Ceremonial Cacao 200g — Paulo's Farm, Pará Brazil 2024, Stone-Ground
>
> **Variant B (if §0a Reading B applies):**
>
> Agroverse Single Estate Ceremonial Cacao 200g — Pará Brazil 2024, Stone-Ground, Sugar-Free
>
> Both are under the 120-character limit. Variant B requires the farm name stripped from the long description below as well — otherwise the title and body contradict each other, which is a review flag.

**Short description:**

> Single-farm ceremonial cacao from Paulo's farm in Pará, Brazil — the 2024 harvest, stone-ground and packed at origin. Rich, unsweetened drinking cacao for traditional preparation.

**Long description:**

> **One farm, one harvest, one ingredient list.**
>
> This ceremonial cacao comes from a single grower — Paulo, in Pará, Brazil — and a single harvest year, 2024. It is not a blend. Every 200g block can be traced to the farm that grew it, which is why each bag carries its own QR code linking to that batch's record.
>
> **How it is made.** The beans are fermented and sun-dried on the farm, then stone-ground into a smooth paste. Nothing is added to soften the flavour: what you taste is the 2024 Pará harvest.
>
> **How to prepare.** Traditional ceremonial preparation is roughly 30–40g of cacao per cup, whisked into hot water or milk. Many people add a little cinnamon or chilli. It is unsweetened — sweeten to taste.
>
> **Why single-origin matters here.** Blended cacao hides its origins. Ours names the farm, the region and the year on the pack, and the QR code takes you to the batch record on the Agroverse ledger — the same record the farm and the importer see.
>
> **Ingredients:** `CONFIRM FROM PACK`
> **Net weight:** 200g (7.05 oz) · **Storage:** cool, dry, away from direct sunlight · **Shelf life:** `CONFIRM FROM PACK` · **Allergens:** `CONFIRM FROM PACK`

**Attributes:** form = block/paste · preparation = drinking cacao · sweetened = no · organic = `CONFIRM — only claim if certified`

**Photography needed:** front pack · back pack (label + nutrition panel legible) · cacao block out of pack · prepared cup · **QR code close-up**. The last one is the hook for video content and doubles as traceability proof.

---

## 4. `8-ounce-organic-cacao-nibs` — RECOMMENDED

**Ledger record:** $25.00 · 8 oz · **stock 131** · shipment AGL4 · farm Oscar · **GTIN 860010660218**

**Title:**

> Amazon Rainforest Cacao Nibs 8oz — Regenerative Single-Farm, Raw & Unsweetened

**Short description:**

> Raw cacao nibs from Oscar's regenerative farm in Bahia, Brazil. Crunchy, deeply chocolatey, unsweetened — for smoothies, porridge, baking or straight from the bag.

**Long description:**

> **Cacao in its simplest form.** These are cacao beans that have been fermented, sun-dried, roasted and cracked — nothing else. No sugar, no oil, no coating.
>
> **Grown regeneratively.** Oscar's farm in Bahia grows cacao under rainforest canopy rather than on cleared land. That is what "regenerative" means here, concretely: shade-grown cacao intermixed with native trees, which is how cacao grew in the Amazon long before it was a commodity. It is also why the flavour is complex rather than flat.
>
> **How to use it.** A spoonful in a smoothie or porridge; scattered over yoghurt; folded into bakes for texture; or eaten as-is. Nibs are the least fussy way to get cacao into a day.
>
> **Traceable to the farm.** The bag's QR code resolves to this batch's record on the Agroverse ledger — farm, harvest, and the shipment that carried it.
>
> **Ingredients:** `CONFIRM FROM PACK`
> **Net weight:** 8 oz · **Storage:** cool, dry, sealed · **Shelf life:** `CONFIRM FROM PACK` · **Allergens:** `CONFIRM FROM PACK` (note: cacao is processed in facilities that may also handle nuts — verify before stating)

**Photography needed:** front pack · back pack (nutrition panel legible) · nibs poured out, shallow depth of field · **QR code close-up**.

---

## 5. `organic-81-dark-chocolate-bar-50g-vivi-jesus-do-deus-bahia-2025` — PARKED (not in launch slate, §0a)

**Ledger record:** $10.00 · 50g (1.76 oz) · **stock 35** · shipment AGL13 · farm Vivi · **GTIN blank**

**Title:**

> 81% Dark Chocolate Bar 50g — Single-Farm Bahia Brazil 2025, Bean-to-Bar

**Short description:**

> A 50g 81% dark chocolate bar, made bean-to-bar from Vivi's 2025 harvest in Bahia, Brazil. Intense, low-sugar, single-farm.

**Long description:**

> **81%, from one farm.** Vivi's farm in Bahia, 2025 harvest — made bean-to-bar rather than from industrially blended couverture. At 81% cacao there is very little between you and the bean, which is the point.
>
> **What "bean-to-bar" buys you.** When a maker buys blended chocolate, the origin disappears. Making it from the beans means the farm, the year and the fermentation are all still legible in the finished bar.
>
> **Ingredients:** `CONFIRM FROM PACK` — this will list cacao mass, cocoa butter, sugar and any emulsifier; do not paraphrase it
> **Net weight:** 50g (1.76 oz) · **Storage:** cool, dry, below ~20°C to avoid bloom · **Shelf life:** `CONFIRM FROM PACK` · **Allergens:** `CONFIRM FROM PACK` — **must state "may contain milk/soy/nuts" per the actual pack**, since this is the field most likely to trigger a compliance rejection

---

## 6. `cacao-mass-bar-500g-ilheus-2024` — alternate (high AOV)

**Ledger record:** $60.00 · **stock 37** · shipment/farm details `CONFIRM` — not yet pulled

Not drafted: it is a 500g unsweetened cacao mass block, a fundamentally different use-case (kitchen/bulk ingredient, not a $10 impulse buy), and its ledger row has not been read in full. Draft it only if the governor prefers margin over volume.

---

## 7. Asset gaps that must close before submission

These are the actual blockers, and two of them are new findings rather than restatements:

| # | Gap | Severity | Detail |
|---|---|---|---|
| 1 | **All four 81% bar variants share ONE image file** | **HIGH** | `81-dark-chocolate-bar-50g-packaging.jpg` is referenced by Oscar 2024, Santa Ana 2023, São Jorge 2024 **and** Vivi 2025. Qualification requires *"a complete set of images of the product's packaging and labeling"* **per listing**. One shared stock photo across four vintages cannot satisfy that — and if the packs genuinely differ (farm, year), the photo is wrong for at least three of them. |
| 2 | **GTIN: bars have none — and the two we DO have are questionable on TikTok** | **Resolved on approach** | Correction to an earlier reading: GTIN is **not a hard prerequisite** for Food & Beverage. TikTok documents a **GTIN-exemption** route for private-label / own-brand / brands without UPCs, applied per category + product type (see ops doc §9). So the bars are not blocked by GTIN. **But our existing codes carry risk:** `860010660232` and `860010660218` both begin `860` = **GS1 Serbia**, and share one company prefix (`860010660`) — the signature of a bought-in barcode block, not a prefix licensed to Agroverse. Check digits verify, but TikTok validates prefix *ownership* via GEPIR / GTIN.cloud, so a prefix we do not own is worse than no identifier. **Decision: take the exemption route; do not buy more barcodes; verify `860010660` in GEPIR before using it anywhere.** |
| 3 | Pack & label photography | **HIGH** | Required by policy. Needs back-of-pack shots with the nutrition panel legible — a lifestyle photo will not do. |
| 4 | Ingredients + nutrition panel | **HIGH** | Must be transcribed from the physical packs. Not inferable from the ledger. |
| 5 | FDA facility registration | **BLOCKER** | Governor-side. See §7a of the ops doc — FSVP records are not this instrument. |
| 6 | Return policy, shipping lead time | LOW | Needed to complete the listing form. |

**Net effect on the recommendation.** Per §0a the launch slate is a **single SKU: `ceremonial-cacao-paulo-s-la-do-sitio-farm-200g`**. It is the only product that clears all three gates at once — exemption-eligible on GTIN, deepest stock (170 units, so no refunds-as-data), and one farm / one harvest / one lot, which means a single packaging-photo set and a single ingredient transcription.

Items 1 and 2 therefore stop mattering at launch: the shared-barise photograph (item 1) is irrelevant to a ceremonial-cacao listing, and the bars' missing GTIN (item 2) is moot once the exemption covers the launch SKU. Both return to relevance only when the bars are added later — at which point item 1 becomes the hard blocker, not item 2.

---

## 8. Decision status

### Resolved (2026-11-28)

| Decision | Call |
|---|---|
| Brand | **Agroverse** |
| SKU count | **One** — ceremonial 200g only |
| GTIN approach | **Exemption route**, not new/existing barcodes |

### Still open (governor)

| # | Decision | Why it blocks |
|---|---|---|
| 1 | **Category qualification** — run Seller Center → Qualification Center → Category Qualification, screenshot the document list | Decides the timeline for every listing. Five minutes. Highest information per minute of anything on this list. |
| 2 | **FDA facility registration** — held, or only FSVP / prior-notice records? | §7a of the ops doc rates this a **hard blocker**: restricted categories cannot be listed until qualification is approved, and the registration is a required document. FSVP records are a different instrument. |
| 3 | **Estate naming** | ✅ **RESOLVED — Oscar's** (§0a.1). Note §0a.3: resolved estate ≠ estate printed in the title — for the 81% bar the pack is anonymous, so the title stays "Single Estate, Brazil". |
| 4 | **Price parity** — list at $30 (agroverse.shop parity) or at an uplift? | Recommended: **match $30**. A higher TikTok price than our own site is screenshot bait. |
| 5 | **GEPIR check on `860010660`** — is that prefix licensed to Agroverse? | Only matters if we ever list *with* a GTIN. Moot while we take the exemption, but it is the cheapest way to retire the question. |
