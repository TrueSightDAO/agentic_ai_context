# TikTok Shop — listing copy drafts (KAN-113)

**Status:** drafted 2026-11-28 (Sophia Truesight), pending category qualification + governor sign-off.
**Governor:** Gary Teh · **Parent:** [KAN-113](https://truesightdao.atlassian.net/browse/KAN-113) · **Blocks:** nothing — ready to paste once qualification clears.

> **Nothing in this document has been submitted to TikTok.** No products created, no sheet cells written.
> Source of truth for prices/stock/GTIN: Main Ledger `Agroverse SKUs` tab, read 2026-11-28.

---

## 0. Why this exists before the decisions are made

Three open questions gate the *listing* (which SKUs, what price, and whether category qualification passes). None of them gate the *copy*. Titles, descriptions, specs and compliance fields are identical regardless of the final SKU mix, so this work is reusable and does not need to wait.

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

> Ceremonial Cacao 200g — Single-Farm Pará Brazil 2024, Stone-Ground, Sugar-Free

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

## 5. `organic-81-dark-chocolate-bar-50g-vivi-jesus-do-deus-bahia-2025` — HOLD (see §7)

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
| 2 | **GTIN missing on all three bar variants** | MEDIUM | Ceremonial (`860010660232`) and nibs (`860010660218`) have GTINs; the bars do not. TikTok has a GTIN-exemption path, but a listing *with* an identifier is smoother. This is a further argument for leading with ceremonial + nibs. |
| 3 | Pack & label photography | **HIGH** | Required by policy. Needs back-of-pack shots with the nutrition panel legible — a lifestyle photo will not do. |
| 4 | Ingredients + nutrition panel | **HIGH** | Must be transcribed from the physical packs. Not inferable from the ledger. |
| 5 | FDA facility registration | **BLOCKER** | Governor-side. See §7a of the ops doc — FSVP records are not this instrument. |
| 6 | Return policy, shipping lead time | LOW | Needed to complete the listing form. |

**Net effect on the recommendation.** §7 items 1 and 2 make the **$10 Vivi bar the weakest of the three recommended SKUs**, despite being the best impulse price point. If the bar's label photography and GTIN cannot be produced quickly, the pragmatic first batch is **ceremonial 200g + 8oz nibs** (both GTIN'd, both deep stock, two price points), with the bar following once per-variant images exist. A 2-SKU start is fine — KAN-113 asked for 1–3.

---

## 8. Open decisions (governor)

1. **Category qualification** — run Seller Center → Qualification Center → Category Qualification, screenshot the document list. Decides the timeline for everything above.
2. **FDA facility registration** — held, or only FSVP/prior-notice records?
3. **SKU count** — 3 as drafted, or the 2-SKU start in §7?
4. **Price parity** — listing at agroverse.shop prices ($30 / $25 / $10). Recommended: yes, match. A higher TikTok price than our own site is screenshot bait.
