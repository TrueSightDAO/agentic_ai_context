# China market entry — reconciliation + errata

**Date:** 2026-11-14
**Prepared by:** Sophia Truesight
**Between:**
- **Sophia (committed):** `FIELD_AUDIT_AND_SWOT_2026-11-13.md` (PR #1837), `FINAL_SKU_POSITIONING_2026-11-14.md` (PR #1838)
- **Envoy (Discord):** China Market Entry Report v2 — five-decision framework

**Purpose:** resolve the substantive conflicts *before* merging, and settle where the canonical document lives. Envoy flagged the merge rather than deciding it; this document makes the call and fixes what needs fixing first.

---

## 0. The two documents are complementary, not duplicative

| | Sophia (committed) | Envoy (Discord) |
|---|---|---|
| **Depth** | 80 photos, 22-SKU ladder, SWOT, competitive positioning | ~10+3 photos, decision framework |
| **Does well** | Competitive/SWOT evidence, price discovery | Explicit SKU/channel/packaging/price recommendations |
| **Gap** | No decision framework | Shallower evidence base, not in a repo |

**Both are needed.** Envoy is right that these are complementary. The correction below is that several of Envoy's load-bearing claims need fixing *before* they become canonical, because they are checkable and some are wrong.

**Where it lives:** `agentic_ai_context/reports/china_market_positioning_2026/` — the repo of record, already referenced from that folder's `README.md`. A Discord scratchpad is not durable and cannot be cited from a listing conversation. Envoy's report should be **committed as a sibling file** so the final synthesis can cite real text rather than a summary.

> **Why this document exists rather than a merge:** I have only Envoy's *summary* of their report — I cannot read Discord channel history. Merging from a summary would silently misrepresent their work. So this fixes the conflicts now, and the canonical synthesis waits for Envoy's text to be committed.

---

## 1. The discovery-box recommendation is CORRECT — but the composition is wrong

**Envoy's headline SKU call is validated by the SKU catalogue.** Four 81% 50 g single-estate bar SKUs exist and are live:

| # | SKU ID | Estate | Region | Harvest | List |
|---|---|---|---|---|---|
| 1 | `organic-81-dark-chocolate-bar-50g-oscar-bahia-2024` | **Oscar's Farm** | Bahia | 2024 | $10 |
| 2 | `organic-81-dark-chocolate-bar-50g-fazenda-santa-ana-bahia-2023` | **Fazenda Santa Ana** | Bahia | 2023 | $10 |
| 3 | `organic-81-dark-chocolate-bar-50g-fazenda-sao-jorge-bahia-2024` | **Fazenda São Jorge** | Bahia | 2024 | $10.00 |
| 4 | `organic-81-dark-chocolate-bar-50g-vivi-jesus-do-deus-bahia-2025` | **Vivi's Farm (Jesus do Deus)** | Bahia (Itacaré) | **2025** | $10.00 |

Source: Main Ledger `1GE7PUq-…`, tab `Agroverse SKUs`, column A.

**So a 4-bar discovery box is entirely supportable.** That is a genuinely strong call, and Envoy reached it by pattern-matching the price ladder — the same conclusion my 卡卡星座 finding pointed at from a different direction. Two independent routes to one answer is the strongest signal either of us produced.

### 1.1 The correction: it is not Paulo / La do Sitio

Envoy names the four as **"Paulo/Oscar/Santa Ana/Vivi"**. **Paulo's La do Sitio Farm (Pará) has no 50 g bar SKU.** Its SKUs are:

| SKU | Format |
|---|---|
| `ceremonial-cacao-paulo-s-la-do-sitio-farm-200g` | Ceremonial cacao 200 g |
| `premium-organic-cacao-beans-la-do-sitio` | Beans, per kg |

No bar. The missing fourth estate is **Fazenda São Jorge, Bahia 2024**, which has a live 50 g bar SKU.

**Corrected discovery box: Oscar 2024 · Santa Ana 2023 · São Jorge 2024 · Vivi 2025.**

This matters commercially, not pedantically: a box promising four estates and delivering a Pará ceremonial-cacao farm as a *bar* would ship a promise the catalogue cannot fill.

### 1.2 Why the distinction is worth keeping, not erasing

La do Sitio is **Pará**, and the other four are **Bahia**. It is also the farm with a full FSVP equipment set on file (roaster, cracker/winnower, mould, fridge) and an award-winning regional reputation. Excluding it from the bar box is a *catalogue* fact, not a judgement on the farm. If a La do Sitio bar SKU is later created, it becomes the fifth estate — and the only Pará-origin one, which is a real point of difference in a Bahia-heavy lineup.

---

## 2. The McCann reading needs correcting

Envoy's decomposition:

> *"considering McCann Worldgroup's 'Truth Well Told' framework (**Truth=verifiable provenance, Well=how it's packaged/experienced, Told=where it's placed**)"*

That is not what the framework is, and the misreading has a commercial consequence.

**What "Truth Well Told" actually is:** McCann's guiding platform since 1912 — find an enduring *human* truth, then tell it well. Their leadership describe it as a growth framework and belief system, operationalised through a planning process called **Truth to Impact**. It is **not** a three-part decomposition of truth / packaging / placement; "Well Told" is not a packaging or media layer.

**The consequence.** McCann's own stated doctrine is:

> "You move the market by moving people. And you're not going to move people by just telling them why **functional superiority** should command a price premium."

Making **"Truth = verifiable provenance"** the foundation of the framework is exactly the functional-superiority claim that doctrine warns will not carry a premium. The field evidence agrees: Meiji sells 50% Dominican and 70% Venezuelan in identical 75 g packs at an identical ¥18.90 — **+20 points of cocoa and a different single-origin claim earned zero price premium.** If a better claim earns nothing, a more verifiable one will not automatically earn ¥88.

**The fix (already in PR #1838):** verifiability is the **reason to believe**, never the positioning. The reason to buy is a human truth — in China, *"when I give a gift I want it to prove I didn't just grab the first box off the shelf"*; in the USA, *"I want my morning ritual to feel like a treat while still counting as healthy."*

Encouragingly, this strengthens Envoy's discovery-box recommendation rather than weakening it: **a box of four named estates is a better gift object than a bar**, which is a human-truth argument, not a functional one.

---

## 3. ¥88 is not a convergence with Café-Tasse

Envoy writes that the ¥88 price is where *"your cost model and my field-confirmed Café-Tasse comparable converge … independently."*

The field-confirmed Café-Tasse is **¥25.00 for 20 g = ¥1,250/kg = ¥62.50 per 50 g equivalent.** Arithmetic:

| Price / 50 g | ¥/kg | vs Café-Tasse (¥1,250/kg) | Reading |
|---:|---:|---:|---|
| ¥59 | 1,180 | **0.94×** | Below the top rung — defensible premium without novelty premium |
| ¥62.50 | 1,250 | **1.00×** | Parity with the only craft SKU in the aisle |
| ¥71 | 1,420 | **1.14×** | The $10 US list price; just above the top rung |
| **¥88** | **1,760** | **1.41×** | **41% above Café-Tasse per gram — not convergence** |

¥88 is 41% above the comparable, not a convergence with it. Presenting it as independent agreement is the kind of claim that collapses the first time a buyer does the division.

### 3.1 But ¥88 does work — under the gift-box architecture

There is a coherent defence, just not the one stated:

| SKU | Price | Per bar |
|---|---:|---:|
| Single 50 g bar | **¥88** | ¥88 |
| 4-bar discovery box | **¥352** | ¥88 |

Under the gift frame, **¥352 is the hero price point** — it sits against wine (blt carries bottles to ¥2,599) and ¥70–150 tea gift boxes for the same occasion. The single bar at ¥88 then functions as the **anchor** that makes the box read as fair value (4 × ¥88 = ¥352). That is legitimate price architecture.

**But it only works if the gift frame is accepted** — and the gift frame comes from the human-truth analysis, not from "Truth = verifiable provenance." So §2 and §3 are the same correction seen twice.

**What I could not verify:** Jerrie Huang's landed-cost study is **not in my context**, so I cannot confirm the cost side of ¥88. Whether ¥88 is *cost-justified* is unknown to me; whether it is *comparably justified* is answered above (it is not).

---

## 4. "Never a health claim — legal constraint" is wrong on the reasoning

Envoy's decision 5: *"composition + provenance only, never a health/functional claim — **legal constraint, not a copywriting choice**."*

**It is not a legal constraint.** CHOCDAY 每日黑巧 prints, on a Chinese retail pack I photographed at 超盒算NB:

> 高膳食纤维 · **益生元++** · 23 kcal/份 · Clean Label 清洁标签通过华测检测权威验证 · **膳食纤维有助于维持正常的肠道功能** · 膳食纤维是低能量物质

"Dietary fibre helps maintain normal intestinal function" is a **standard function claim** of the kind GB 28050 permits when the product qualifies and substantiates. So functional claims are legally available in China — already logged as a falsified prediction in the field audit (§6C).

**The recommendation is still right, for different reasons:**

1. **The ground is taken.** CHOCDAY owns the claim stack with own-brand-scale distribution. Contesting it on claim density is an unwinnable, expensive fight.
2. **Claims invite scrutiny we do not need.** An 81% single-estate bar with a QR ledger does not need a health halo; adding one invites substantiation questions that distract from provenance.
3. **Regulatory cost is real** — substantiation, testing, label approval. Optional spend for no strategic gain.

So: **keep "no health claim" as the decision; drop "legal constraint" as the reason.** Stating a false legal constraint in a planning document is worse than a weak strategic argument — it cannot be maintained in front of a Chinese retail buyer, who knows exactly what does and does not clear GB 28050.

---

## 5. Estate readiness — two findings that touch both reports

Surfaced while verifying the discovery box. Both need confirmation; neither is settled.

### 5.1 La do Sitio has no melanger

Per `fsvp/ONBOARDING_GUIDE_EN_PT.md`: *"previously no farm in our network had a melanger installed (La do Sitio at **Stage 1, roast → crack & winnow**; Kingma melanger on the 'to acquire' list)"*, with a Gary-supplied melanger photo added only as a **guide example**, not as installed equipment.

La do Sitio's verified FSVP set: **roaster ✓ · cracker & winnower ✓ · chocolate mould ✓ · fridge ✓ · melanger ✗**.

**Implication:** Stage 1 means it can produce **nibs**, not chocolate. So the 274 kg of La do Sitio beans cannot become bars on that farm today. This sharpens — rather than contradicts — the "no convertor identified" weakness in the field audit: the convertor gap is specifically **grind/refine/conch**, and it sits at La do Sitio as much as at any Kaiping factory.

### 5.2 Vivi: a documentation conflict

Two facts that do not sit together:

| Source | Says |
|---|---|
| `brazil/SUPPLY_CHAIN_SIMPLIFICATION.md` | *"Vivi is the only remaining non-cooperative farmer in-network, and **no beans were stocked from him this year**"* |
| `Agroverse SKUs` | **`organic-81-dark-chocolate-bar-50g-vivi-jesus-do-deus-bahia-2025`** — a live **2025** bar SKU |

Both can be true (a 2025 bar made from earlier-stocked beans, with none stocked in the current season), but the planning consequence differs materially. Also relevant: independents (Vivi, Clara, Analuana) *"must join a cooperative to move beans through the coop's MAPA + NF-e"*, and co-ops take only member-farmed beans.

**For the discovery box this is a supply-continuity risk, not just a naming question.** If Vivi's is a limited 2025 run with no replenishment path, the box is either (a) a genuine limited edition — which is a *selling point* for a collectible series — or (b) unbuildable at a second print run. **Which one it is needs confirming before the box is promised to a buyer.**

---

## 6. What survives unchanged

For the record, Envoy's other calls hold up and I endorse them:

| Decision | Status |
|---|---|
| **Channel** — specialist/gifting, cafe/HORECA, premium-format supermarkets; never general gondolas or NB-type discount | **Endorsed.** Matches the field evidence: the blt destination aisle is the right home, and both 超盒算NB (天天低价, 10 km from 大岭山) and general gondolas would cap the price. |
| **Packaging** — QR per bar not per box, estate name on wrapper, lab data on box | **Endorsed — the strongest call in the report.** Per-bar QR is what makes the gift claim demonstrable; per-box would collapse four estates into one code and destroy the mechanic. |
| **Discovery box as lead SKU, single bar secondary** | **Endorsed** — with the composition fix in §1 and the reminder that the box does not yet exist as a SKU. Both current SKUs are single bars; the box is a **new product** requiring its own SKU, barcode, label and gift packaging. A real work item with real lead time, not a repack. |
| **Fold-in of my CHOCDAY + GACC corrections** | Correctly applied. |

---

## 7. Recommended path to one canonical document

1. **Envoy commits their report** to `reports/china_market_positioning_2026/CHINA_MARKET_ENTRY_DECISIONS.md` via PR. Required, because I cannot merge from a summary without misrepresenting their work.
2. **Apply §1–§5 of this document** as corrections to whichever text becomes canonical.
3. **Then** produce a single synthesis doc (`CANONICAL_CHINA_POSITIONING.md`) that supersedes all three and carries: the discovery-box decision (corrected composition), the human-truth framing, the two-market architecture, the 22-SKU ladder as evidence annex, and the SWOT.
4. **Keep the evidence docs as appendices** rather than deleting them — the field audit's photo provenance is the audit trail any buyer claim will rest on.

**One open decision for Gary:** whether the canonical doc should be a decision memo (short, for acting on) or a positioning dossier (long, for a retail buyer). They serve different readers, and the current draft is trying to be both.
