# Why is the shipment on CBP agriculture hold? — ranked hypotheses

**Question:** governor (Gary Teh), thread 10800 — *"Why would it be on agricultural hold"*
**Date:** 2026-10-09 · **Author:** Sophia Truesight (autopilot)

> ⚠️ **We do NOT have CBP's stated reason.** Nothing below is a fact about CBP's decision — these are **ranked hypotheses** built from our own lane records, each paired with the check that would confirm or kill it. Treat as a diagnostic plan, not a conclusion.

---

## The trigger event (verbatim)

From `imports@5cl.rs`, 09/10 15:41 −0300 (Gmail `1a121f92a07014d8`), cc Matheus:

> "The shipment is currently on **agriculture hold**, and **CBP (U.S. Customs and Border Protection) may decide to inspect it** before releasing it. We cannot pick up the shipment until it has been released. **Airport storage charges may apply** if we are unable to pick it up today."

**Two things to hold onto:** (a) APHIS's own guidance says such a hold **often just means "CBP hasn't gotten to it yet"** — it may be procedural and temporary; (b) but a **plant-product** consignment with an open documentation question is exactly the profile that gets selected. So: don't panic, do respond.

---

## H1 — Plant-product classification; the phytosanitary certificate was never obtained 🔴 STRONGEST

**The smoking gun.** On **29/09** Omega asked whether the importer requires a **phytosanitary certificate** and, if so, an **Import Licence**. **It was never answered** — it is still open item #1 in §5.9.

Cocoa is **Chapter 18** (cocoa and cocoa preparations). US rules for commercial plant-product imports require, for regulated articles, an **APHIS import permit (PPQ 587)** plus a **phytosanitary certificate issued by the exporting NPPO (MAPA in Brazil)**. If CBP's targeting treats this consignment as a regulated plant product, a **missing phyto certificate is by itself sufficient reason to hold** pending inspection.

The unanswered question is now the single best explanation for why the hold appeared.

- **Check that confirms/kills it:** ask Omega/Matheus for the **phyto certificate** (or written confirmation that none is required). Ask the US broker which HTS/entry line triggered.

## H2 — FDA Prior Notice not confirmed filed 🟠 STRONG

The Prior Notice is **mandatory** for this food import, not optional (§5.6). **Last recorded status was `unfiled` — as of 05/10.** The cargo was **received at SFO on 08/10** (Isis).

So either it was filed **off our records**, or **it was never filed** — and either way we cannot currently *show* the confirmation number. An FDA hold and an ag hold are different, but they co-occur, and CBP verifies the PN confirmation at entry.

- **Check:** obtain the **PN confirmation number** and the PNSI receipt. Confirm it **matches the entry** on port, arrival date, importer of record, and product description.

## H3 — Pallet material contradiction (wood vs plastic HDPE) 🔴 HIGH IMPACT

Our own records **contradict each other**:

| Source | Says |
|---|---|
| Quote premise (`2026-10-08_5continent_quote_vs_invoice.md`) | *"Matheus having the **heat treated pallets**"* |
| Rev 14, `2026-10-02_airport_weighing_weight_divergence.md` | 2 × 10 kg **plastic HDPE** pallets — *non-wood, ISPM#15 N/A* |
| NF-e nº 16 | *"2 paletes **plásticos HDPE**"* |
| Airport re-palletizing (02/10, cintagem **R$300**, "03 styrofoam boxes tied together on a plastic pallet + loose boxes") | final pallets may differ from anything described |

**Why this matters:** **solid wood packaging material (WPM) must meet ISPM#15** — treated and **IPPC-stamped**. Unstamped/untreated wood packaging is a **textbook CBP agriculture hold** and is frequently treated or refused. If the cargo ended up on **wood** pallets at re-palletizing, this alone explains the hold — and our "no fumigation needed" conclusion would be **wrong**.

- **Check:** photograph the **actual pallets** now (both sides) and look for an **IPPC stamp**. Get the re-palletizing vendor to state the material. Cheap, fast, decisive.
- ⚠️ **Do not buy a wood-pallet fumigation cert reflexively** — but equally, do not keep asserting "plastic, exempt" until the physical pallet is confirmed.

## H4 — HS code mismatch: AWB `1810.00.00` vs invoice `1801.00.00` 🟠 MEDIUM-HIGH

Flagged on 02/10 and **never closed**. The AWB (and MAWB) carry **`1810.00.00`** (cocoa powder); the commercial invoice/NF-e declares **`1801.00.00`** (**raw cocoa beans**). The **email subject line itself says `NCM 1801.00.00`**.

This matters beyond tidiness: **`1801` = raw cocoa beans = plainly a plant product**; `1810` = a processed powder. A disagreement across entry documents about **product identity** is a standard mismatch flag — and one of the two declared identities is raw agricultural produce.

- **Check:** reconcile HS/NCM across **NF-e ↔ AWB ↔ entry ↔ PN**; have the broker state what was actually entered.

## H5 — The AWB still declares `2106.90.00` (cacao tea) removed from the cargo 🟡 MEDIUM — sharp finding

**Rev 13 removed the cacao-tea line** (Paulo's AGL8, 12 kg, 2 boxes) from the physical consignment — cargo went **31 → 27 boxes**. **27 boxes matches the AWB.** ✅

**But the AWB's HS list still includes `2106.90.00`** — the code we ourselves use for **cacao tea** (NF-e 16 lines #6/#10). So the face of the air waybill declares a **dried-plant-material** product code for goods **no longer in the shipment**.

Dried plant material / tea is **far more APHIS-sensitive than cocoa powder**. If CBP targeting reads `2106.90.00` + `1801.00.00`, it sees **two plant products** — a strong inspection trigger.

- **Check:** confirm whether the AWB HS list was corrected after the Rev 13 removal; determine what the **entry/PN** declared.

## H6 — Entry ↔ Prior Notice field mismatches 🟡 MEDIUM

FDA guidance is explicit that the PN must **match the CBP entry exactly** (port, arrival date, importer of record, product description) and that **mismatches alone are enough to trigger a hold**. Documented divergences to check:

- **Weight:** NF-e 18 bruto **322.06** · Rev 15 gross **349.00** · forwarder charged **365 kg** — three numbers.
- **Description:** AWB says *"27 boxes with **bars of chocolate**"*; the invoice covers beans/nibs/butter/powder.
- PPQ 587 processing is **5–15 business days** — a permit that *should* have been obtained weeks ago cannot be obtained retroactively in time.

---

## Ranked view

| # | Hypothesis | Evidence strength | Cost to check |
|---|---|---|---|
| **H1** | Phyto cert missing (question never answered) | 🔴🔴 strongest | low |
| **H2** | FDA PN not confirmed filed | 🔴🔴 strong | low |
| **H3** | Pallet wood vs plastic; no IPPC stamp | 🔴 high impact | **lowest — just photograph** |
| **H4** | HS `1810` vs `1801` mismatch | 🟠 | low |
| **H5** | Stale `2106.90.00` tea code on AWB | 🟡 | low |
| **H6** | PN/entry field divergence | 🟡 | medium |

**Note the pattern:** every one of these is a **documentation/verification gap we already knew about and had not closed**, not a new external surprise. The hold is the bill for the open items — most logged in §5.9 days ago.

---

## Who to ask what

| Ask | Owner |
|---|---|
| **Phyto certificate — does it exist? Ever requested/issued?** | Omega (Iolanda / Isis) + Matheus |
| **What HTS/entry line triggered the hold? Any CBP notice of action?** | US broker (Iolanda) |
| **PN confirmation number + receipt; does it match the entry?** | Iolanda (Omega) |
| **Photograph the pallets; wood vs HDPE; IPPC stamp present?** | Matheus (Ilhéus) / Kirsten at delivery |
| **The corrected 5 Continent invoice** (also requested) | Graziela |

---

## Cost & risk notes

1. **Storage is accruing** while held — a live exposure **not in any cost model**, and arguably not ours to bear given the shared delay fault (adjudication §8).
2. **Do NOT** reflexively purchase a wood-pallet fumigation certificate — but **do** stop asserting the pallets are plastic until verified. Both errors are expensive.
3. If H1 is correct, the fix may require a **phyto certificate issued in Brazil (MAPA)** — potentially not solvable at SFO. Escalate early.
4. If a **PPQ 587 permit** was required and never obtained, that is a **5–15 business-day** problem — start now.

---

## Bottom line

The most likely answer, on our own evidence: **the consignment was treated as a regulated plant product and the paperwork that would answer that — a phytosanitary certificate, and a confirmed FDA Prior Notice — was never demonstrated.** The unanswered 29/09 phyto question is the clearest single cause. The **pallet material** is the fastest and cheapest thing to settle: photograph the pallets.

*Analysis only. Nothing sent, nothing purchased, no money moved.*
