# 5 Continent invoice 1026-08 — Adjudication of Graziela's reply (09 Oct 2026, 23:46 +0800)

**Adjudicated by:** Sophia Truesight (autopilot) · **Thread:** 10800 · **Date:** 2026-10-09
**Base under review:** `brazil/sources/2026-10-09_5continent_v6_bucket_derivation.md`
**Reply:** Gmail `1a1215a7694cfe1a` (thread `1a11b3c9cfbbdb95`)

Purpose: separate what the counterparty **conceded**, what she **corrected on us**, what she **left unanswered**, and the **new operational fact**. The dispute position must be rebuilt on this, not on v6 alone.

---

## 1. SELF-CORRECTION — our v6 air-freight finding was wrong

Graziela: *"The original quotation clearly stated 329 kg … billed at the quoted rate of $3.40/kg based on the final chargeable weight."*

**Arithmetic check:**

```
$1,118.60 / $3.40 = 329.0 kg   ← exact
329 kg x $3.40    = $1,118.60  ← exact
```

**So the quoted line `Air Freight +300 kgs = 1,118.60` was NOT a flat rate.** It was a **329 kg × $3.40/kg** figure — the "+300 kgs" was the *tier label*, not a flat charge.

**Consequence — this must be removed from the dispute.** v6 (Cause 1) labelled this line *"365 kg @ $3.40 vs quoted flat 1,118.60"* and carried **+$122.40** as a rate overage. That characterisation is **incorrect**. Charged weight × the quoted rate = a **contractually correct** weight-driven adjustment. **+$122.40 is legitimate and must come out of the disputable set.**

> **Revised actionable dispute:** $937.20 − $122.40 = **$814.80** (before resolving the items below).

### 1b. But the weight itself is still unexplained — 16 kg / $54.40

She asserts chargeable weight **365 kg**. Our documented gross is **349 kg** (Rev 15: net 302.06 + carton 26.94 + pallet 20.00; corroborated by the airport scale).

```
365 - 349 = 16 kg  x $3.40 = $54.40 unexplained
```

**Volumetric-weight check (rules out the obvious explanation):** AWB dims 110×77×90 + 110×104×100 cm = **1,906,300 cm³ ÷ 6000 = 317.7 kg** — *below* 349, so volumetric weight does **not** explain 365. **Request the AWB's chargeable-weight calculation sheet.**

---

## 2. CONCESSION — she validates our derivation

> *"This fee is 10% of the duties paid on your behalf."*

**Our v6 (Cause 3, item 4):** $12.85 = 10% × $128.53. **Confirmed independently by the counterparty.** The duty-advance derivation stands.

---

## 3. EVASION — the inland freight discrepancy is unanswered

**v6 Cause 1, other half:** Inland in Brazil billed **$1,012.17** against her own quoted **$837.00** = **+$175.17**.

Her reply addresses air freight (weight) in detail — but **says nothing about inland freight being billed $175.17 above her own quoted rate.** That is a billed-above-own-quote delta with no stated basis.

**This survives as the surviving freight dispute.** Ask directly: what changed between the quoted BRL basis and the billed figure for inland transport?

---

## 4. $414.59 — "agreed with Omega" / pass-through question still open

Her position: *"You agreed to pay Omega for its Brazilian export customs services, and Omega provided its quotation directly to you by email. I am billing you for the charges previously advised."*

That is an assertion that the charge was **pre-advised**, not evidence of **who paid Omega**. The duplicate test is not "was it quoted" but **"was it paid twice?"**

- **2023 precedent:** Omega billed **separately** (numerário R$4,000 + CT-e R$864.15, Brazil-side, billed apart from Seacoast's US-side invoice).
- **2026 search:** **no Omega invoice found** in the mailbox for this shipment.

→ Negative evidence, but **not conclusive**. **Confirm with Omega (Isis Ribeiro) whether an invoice was issued and paid for the 2026 export-customs service.** Until then $414.59 stays flagged, not disputed.

---

## 5. 🔴 THE INVOICE HAS MOVED — $4,866.33 is superseded

> *"I also identified that the US bond charge included in the quotation was omitted from the original invoice, so I have corrected the invoice accordingly."*

**A quoted item (US bond) was omitted and is being added back.** So the corrected invoice is **higher** than the $4,866.33 we have been analysing, and the 15-line structure will change.

> ⚠️ **Action: request the corrected invoice before further line-level argument.** Continuing to argue against a superseded document wastes the position — and the duty-advance fee (10%) may itself move, since it tracks the duties line.

She also states the **US terminal charges were billed below her actual cost** (supporting receipt attached) — consistent with the 2023 Menzies SFO **$198.50** pass-through we independently verified.

---

## 6. Palletizing ($65) — her argument is commercially stronger than ours

> *"Proper export packing and securing of the cargo is the shipper's responsibility. The fact that the shipment was collected by a trucking company does not transfer that responsibility to the trucker."*

**Adjudication:** this is a **defensible position** — export-grade packing/securing conventionally sits with the shipper, not the carrier. Our counter ("it was the trucker's job") is weak on the merits.

However it is **not fully clean for her either**: the cargo passed *her* Brazil-side collection and still arrived **improperly strapped** (Brazil-side **cintagem R$300** already charged separately on 02/10). **Reasonable landing: concede $65** and bank the credibility for the inland $175.17 and the 16 kg.

---

## 7. Storage + Saturday airport fee ($112.19) — partly earned, partly ours

Her causal claim: we failed to complete export paperwork within Friday's working hours.

**Partial counter-evidence on our side:** the 30/09–01/10 truck wait and the RADAR/SISCOMEX broker habilitação (30/09) were on the **Brazil-side** critical path too (Omega asked Matheus to add its customs brokers). Responsibility for the delay is **shared, not unilateral**. Negotiable, low priority.

---

## 8. 🔴 NEW OPERATIONAL FACT — CBP agriculture hold

From `imports@5cl.rs` (15:41 −0300), cc Matheus:

> *"The shipment is currently on agriculture hold, and CBP may decide to inspect it before releasing it. We cannot pick up the shipment until it has been released. Airport storage charges may apply."*

**Why this matters beyond logistics:**
1. **It is an APHIS/agriculture matter on a plant-product import** — the exact domain of the **phytosanitary certificate + Import Licence** question that has sat **UNANSWERED** since 29/09 (§5.9 #1). This is plausibly the loose end now surfacing at the border.
2. **Pallet material is now materially relevant.** §7/§5.5 record a contradiction: one row says *heat-treated* pallets; the export-doc generator declares **plastic HDPE (non-wood)** → ISPM#15 N/A. **If the pallets were wood, ISPM#15 treatment/stamp compliance becomes live on an agriculture hold.** Reconcile the material **now**, before CBP asks.
3. ⚠️ **Accruing cost:** airport storage may apply while held — a live cost exposure **not in any current model**, and arguably not ours to bear (see §7 delay apportionment).

**Immediate actions:** (a) resolve pallet material definitively; (b) get the phyto/Import-Licence answer from Omega/Matheus; (c) confirm who bears storage during the hold; (d) obtain the CBP hold reason/HTS line if disclosed.

---

## 9. Rebuilt position

| Item | Amount | Status after her reply |
|---|---|---|
| Air freight weight delta | 122.40 | ❌ **WITHDRAWN** — weight-driven, quoted rate, correct |
| **16 kg unexplained chargeable weight** | **54.40** | 🟡 **NEW ask** — AWB weight calc sheet |
| **Inland billed above her own quote** | **175.17** | ✅ **LIVE — unanswered** |
| Quoted customs items (Cause 2) | 418.53 | ✅ legitimate (as v6 found) |
| Palletizing | 65.00 | 🟠 weak — recommend concede |
| Storage + Saturday fee | 112.19 | 🟠 shared fault — negotiable |
| Export customs BRA + SDA | 414.59 | 🟡 pass-through — confirm Omega paid |
| Duty advance (10%) | 12.85 | ✅ correct (she confirmed) |
| Bank fees | 35.00 | 🟡 "standard" — ask for the schedule |
| **US bond** | ? | 🔴 **now added — invoice revised up** |

**Dispute discipline:** the credible core is now **$175.17 (inland) + $54.40 (weight) + the Omega-payment question** — a tighter, more winnable case than v6's headline $937.20, which **overstated our position by $122.40**.

---

## Note
Analysis of correspondence. Nothing was sent. No payment was made or implied.
