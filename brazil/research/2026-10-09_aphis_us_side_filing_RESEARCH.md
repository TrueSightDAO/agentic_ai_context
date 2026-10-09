# RESEARCH — Do we need to file APHIS on the US side?

**Date:** 2026-10-09 · **Author:** Sophia Truesight (autopilot) · thread 10800
**Question (governor):** *"Do we need to file Aphis on the USA side?"*

---

## 0. Short answer — two filings, two owners

| # | Artefact | Who files it | Where | Ours? |
|---|---|---|---|---|
| 1 | **APHIS import permit (PPQ 587)** | **US importer of record — TrueTech Inc** | **APHIS eFile** | ✅ **yes — genuinely USA-side** |
| 2 | Phytosanitary certificate (CF) | Brazil NPPO — **MAPA / VIGIAGRO** | Brazil, before export | ❌ **not ours** — Brazil's |

**The governor's instinct is correct.** #1 is a **US-side** filing in **our** name, and it is a
**different artefact** from the Brazil-side phyto certificate we have been chasing.

## 1. The legal chain

Three APHIS sources chain into a specific answer for cocoa:

1. **Plants for Planting Manual** — regulated propagative list reads:
   > *"**Theobroma spp.** cacao montaras — **All propagules except seeds** — All countries."*

   ⇒ Cocoa **seeds are expressly carved OUT** of the Plants-for-Planting regime.

2. Carved out of one manual routes it into the other. APHIS's **Generally Authorized Non-Propagative
   Plant Products** page states the governing rule:
   > *"Products **not listed** in the **Miscellaneous Processed Products Manual** or the **Seeds Not for
   > Planting Manual** are **unrestricted** unless covered under CITES, a Federal Noxious Weed, or part of
   > the Federal Seed Act."*

3. Cocoa beans are, in USDA's framing, *"technically considered **seeds**"* → **Plants and Plant
   Products Not for Propagation** → the **Seeds Not for Planting Manual** — a **regulated** manual.

**Being listed in a regulated manual is what creates the permit question.** That is the entire mechanism.

## 2. The exposure splits by article — only ~15 kg

| Article | Product | Form | APHIS risk |
|---|---|---|---|
| **0004** | Cacao Almonds | **WHOLE BEANS** 10 kg | 🔴 **seeds → permit question** |
| **0009** | Cacao Almonds, Pará | **WHOLE BEANS** 5 kg | 🔴 **seeds → permit question** |
| 0002 | Mass bar | processed | 🟢 likely unrestricted |
| 0001/0003/0006 | Nibs | processed | 🟢 likely unrestricted |
| 0005 | Ceremonial pouch | processed | 🟢 likely unrestricted |
| 0007 | Cacao tea | dried plant material | 🟡 borderline — see §3.2 |
| 0008 | Cacao butter | rendered fat | 🟢 likely unrestricted |

⇒ **15 kg of 302 kg carries the APHIS question; ~287 kg plausibly carries none of it.**
The same 15 kg flagged in PR #1559 and #1560 — it remains the concentrated risk in this consignment.

## 3. Two "false friends" that could mislead us

1. **"Dried beans and peas may be imported without a permit."** The generally-authorized list says this —
   and it does **not** refer to cocoa. In USDA usage that line covers **leguminous pulses** (*Phaseolus*,
   *Pisum*). Cocoa "beans" are the **seeds of a Malvaceae tree**. Treating our product's common name as
   a vegetable is a trap.
2. **"Dried teas, herbal teas… of *Camellia sinensis*."** Our **cacao tea (0007)** is *Theobroma*,
   **not** *Camellia* — so that allowance likely does not cover it, and it may sit in a regulated manual too.

## 4. 🔴 The material fact

A repo-wide search of **`fda_fsvp`** for any permit number (`P-########`), `PPQ 587`, or `eFile` returns
**nothing — across every shipment and every supplier.** **We have never obtained an APHIS import permit.**

This is not a lapse on this shipment alone; it is a **standing gap** in how US entries have been done.

**Consistent, not contradictory:** the 2023 Coopercabruca precedent cleared with no APHIS document on
file — and it shipped **processed** (nibs). **Processed cocoa may not need one. Whole beans may.**
**The product mix is what changed** — not the lane.

## 5. Timing — this cannot be fixed today

**PPQ 587 processing: ~5–15 business days.**

Unlike a phone call, a permit **cannot be retrofitted on a Friday**. ⇒ **If the hold turns out to be
APHIS, phoning the cargo desk will not release it.** That materially reshapes the weekend plan in
`2026-10-09_weekend_inspection_vs_hold_RESEARCH.md`.

## 6. Honest gap — not overclaiming

**ACIR is login-gated** (SAML/SSO; 401s and redirects on every attempt). **I could not read the
authoritative requirement for cocoa beans from Brazil, and I will not assert a definitive yes/no on the
permit.** The evidence above is **strongly indicative** — one commercial broker states *"most cocoa bean
imports should have a permit"* — but indicative is not authoritative.

**The exact lookup, for whoever has credentials:**

| Resource | Detail |
|---|---|
| **ACIR** (Plants & Plant Products Not for Propagation) | `acir.aphis.usda.gov/s/acir-global-search?category=Plants-and-Plant-Products-Not-for-Propagation` |
| **PPQ Plant Permits Team** | `plantproducts.permits@usda.gov` · **(877) 770-5990** |
| **Apply** | `efile.aphis.usda.gov` |
| **Search terms** | **"cacao"** *and* **"Theobroma"** separately — and run **per article form** (beans vs processed) |

**This is distinct from the AQI-vs-FDA question.** Both remain open and they have different fixes:
the agency determines ***which*** fix; this determines ***whether a permit was ever possible in time***.

## 7. Consequence for the process doc

`fsvp/SHIPMENT_DOCUMENTATION_PROCESS.md` says *"US lane does **not** need MAPA (only the China/GACC
lane does)."* That sentence now looks **half-right**: MAPA may indeed be unnecessary for **processed**
cocoa while still being required for **whole beans**. **That distinction is the likely root of the
omission** and deserves its own PR — not a drive-by edit here.

## Sources

- APHIS **Generally Authorized Non-Propagative Plant Products** — https://www.aphis.usda.gov/ace/generally-authorized-non-propagative-plant-products
- APHIS **Plants for Planting Manual** (Theobroma: all propagules *except seeds*) — https://www.betterseed.org/wp-content/uploads/USDA-APHIS-Plants-for-Planting-Seed-Manual.pdf
- APHIS **eFile / PPQ-587** — https://www.aphis.usda.gov/efile · https://www.aphis.usda.gov/sites/default/files/apply-fruits-vegetables-import-permits-ppq.pdf
- APHIS **Commodity Import and Export Manuals** — https://www.aphis.usda.gov/trade-management-manuals
- APHIS **"Seeds Not for Planting" manual update** — https://content.govdelivery.com/accounts/USDAAPHIS/bulletins/1cdad29
- APHIS **ACE PGA Message Set** (document codes: PPQ 587, phyto cert, treatment cert) — https://www.aphis.usda.gov/sites/default/files/trade_itds_ver_4.6.pdf
- APHIS **ACIR** (login-gated) — https://acir.aphis.usda.gov/s/
- CBP **APHIS Supplemental Trade Guide, Appendix APH-A** (AP0700 Miscellaneous & Processed Products → A01 phyto / AE1 e-phyto / A05 treatment cert) — https://www.cbp.gov/sites/default/files/2024-10/APHIS%20Supplemental%20Trade%20Guide%20-%20Appendix%20APH-A%20%28ver.%204.1%29%28508%20Compliant%29%20%282%29_508_0.pdf

*Analysis only. Nothing sent, nothing purchased, no money moved.*
