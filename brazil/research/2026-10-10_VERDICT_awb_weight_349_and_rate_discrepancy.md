# VERDICT — the AWB weight box: 349,000 kg (not 365)

**Date:** 2026-10-10 · **Author:** Sophia Truesight (autopilot) · thread 10800
**Trigger:** governor go-signal on RESUME unit 1 — *"Open the 2026 AWB PDF and read the weight box."*
**Settles:** the reopened §5.5 weight question (365 vs 349)

---

## 0. 🎯 The AWB says 349,000 kg — `365` appears ZERO times

**Air waybill `047-3175-3223`, 12 pages:**

| Field | Value |
|---|---|
| No. of pieces / RCP | **2** / **2** |
| **Gross weight** | **349,000 kg** |
| **Chargeable weight** | **349,000 kg** |
| Rate / charge | **2.30** |
| **Total** | **802,70** |
| Goods description | **`02 PALLETS WITH 27 BOXES WITH BARS OF CHOCOLATE`** |
| Freight | **`FRT PREPAID`** |
| DU-E | `26BR001795400-0` |
| RUC | `6BR50042585200000000000000001987510` |
| Signed | **05/OCT/2026** |
| Agent | **Maritime and Air Transports Ltda**, CNPJ `02.992.800/0001-61`, IATA `57199210014` |

**Automated check:** `349,000` occurs **24×**; `365` occurs **0×**.
Files `5146f8d2893b4d7b97150795f901f12b.pdf` and `e376a900c089431bae2625832e1788f7.pdf`.

> ⚠️ The string `349` also appears in the agent's street address — *"Rua Doutor José Peroba, **349**, SL
> 104/105"*. That is a **false-positive trap**; the weight-box reading above is separate and unambiguous.

## 1. ⇒ Graziela's statement is refuted by the document she cites

> *"Cargo was weighted at the airport, and the final weight, including pallets, was determined to be
> **365 kgs, as shown in the paperwork (AWB)**."*

**The AWB does not show 365 kg.** It shows **349,000 kg gross AND 349,000 kg chargeable.** She cited the
AWB to prove a figure the AWB contradicts — and the AWB is the **carrier's own instrument**, not our
commercial doc.

**⇒ §5.5 is settled definitively at 349 kg.** The checklist already had §5.5 CLOSED at 349; **this
confirms it against an attempt to reopen it.**

## 2. 🔴 The money is in the RATE, not the weight

| Document | Line |
|---|---|
| **Invoice #1026-08** | `Air Freight Charges  365 × $3.40 = $1,241.00` |
| **AWB `047-3175-3223`** | `349 × $2.30 = $802.70` |

**Overcharge = $438.30.** Decomposed:

| Cause | Arithmetic | Amount |
|---|---|---|
| **Weight** inflated | 16 kg × $3.40 | **$54.40** |
| **Rate** inflated | 349 kg × $1.10 | **$383.90** |
| | | **$438.30** ✓ |

**The rate is 87.6% of the overcharge.** Everyone — me included — has been arguing about **16 kg
($54.40)** while the real exposure is the **$3.40-vs-$2.30 rate ($383.90)** on the carrier's own waybill.

**Graziela's defence addresses only the smaller half.** She defended the *weight* and said **nothing about
the rate**, which the same AWB also contradicts. **That asymmetry is our strongest single point** — and
it is now document-backed on both axes.

## 3. Full invoice, line by line — #1026-08

| Item | Qty | Price | Amount |
|---|---|---|---|
| Inland Freight in Brazil | 1 | $1,012.17 | $1,012.17 |
| Brazil SSA (Airline + airport fees) | 1 | $345.00 | $345.00 |
| Palletizing | 1 | $65.00 | $65.00 |
| **Storage — SSA + Saturday Airport Fee** | 1 | $112.19 | **$112.19** |
| **Clearance — Export Customs BRA + SDA** | 1 | $414.59 | **$414.59** |
| **Air Freight Charges** | **365** | **$3.40** | **$1,241.00** |
| Airline Terminal Fee USA | 1 | $200.00 | $200.00 |
| Air Freight Handling | 1 | $125.00 | $125.00 |
| Inland Freight | 1 | $885.00 | $885.00 |
| Customs Clearance USA | 1 | $150.00 | $150.00 |
| Additional Invoice Lines | 8 | $5.00 | $40.00 |
| FDA Filing | 1 | $100.00 | $100.00 |
| Customs Duties | 1 | $128.53 | $128.53 |
| Duty Advance Fee | 0.1 | $128.53 | $12.85 |
| Bank Fees | 1 | $35.00 | $35.00 |
| **TOTAL** | | | **$4,866.33** |

**Invoice dated Oct 7 2026 · Payment due Oct 8 2026.**
Bank: **TD Bank NA** · Beneficiary **5 Continent Alliance** · ABA `011400071`.

> **Terms:** *"If not paid within credit terms, **5% fee** will be added automatically."*
> ⇒ **a 5% late fee (~$243.32) is live.**

### Buckets reconcile exactly

| Bucket | Amount |
|---|---|
| Inland Brazil overage | $175.17 |
| Air Freight overage | $438.30 |
| **OVERAGE on quoted services** | **$613.47** ✓ |

**$175.17 + $438.30 = $613.47** exactly — matching the Envoy cross-check's OVERAGE row.

## 4. ⚠️ Third correction — my storage estimate was wrong again

I estimated storage at **~$730**. **The invoice already carries Storage = $112.19.**
My figure was **~6.5× too high** and double-counted what was already billed.

**But the storage line was set Oct 7, before the Oct 8–9 hold** — so **additional storage for the delay
may still be billed separately.** The residual risk is not zero; it is **unquantified and not yet
invoiced.** No number is asserted here.

## 5. Also settled / newly surfaced

1. **The $414.59 "Export Customs BRA + SDA" is invoiced** — previously listed as *UNQUOTED / needs an
   Omega direct answer*. It is on the invoice as a clearance line, and Graziela's scope answer (*"we only
   handled clearance for you back in 2023"*) explains why it is new. **Tracked: legitimate-new, not fraud.**
2. **New discrepancy — pallet count.** The quote's delivery line reads *"Delivery to the door $885
   (**3 pallets**)"*; **the AWB says `02 PALLETS`.** Worth a question — delivery was quoted on 3.
3. **Destination is Kirsten's warehouse.** Gary (10/10 09:49) cc'd **Kirsten Ritschel
   <kirsten@kikiscocoa.com>** and asked 5 Continent to *"make arrangements with Kirsten on the drop off
   at her warehouse."* ⇒ the delivery leg ends at **Kiki's Cocoa**, not an Agroverse site. First naming of
   the destination in the thread.
4. **Gary has committed to payment** (*"Will make arrangements for the wire transfer"*) and asked whether
   the **Brazilian export customs service is one-off or a recurring fixed cost.**

## 6. Honest gaps

- **Rate basis unexplained.** AWB shows **$2.30**; we were quoted **$3.40**. Nothing in the thread addresses
  why. **Now the central question.**
  *(Plausible benign reading: $2.30 is the **airline's** IATA rate and $3.40 is 5 Continent's **all-in**
  rate incl. agent margin — but this is **unstated**. Do not assume bad faith without asking.)*
- **Chargeable = gross = 349** on the AWB ⇒ on the carrier's own instrument the shipment was **not**
  volume-charged up to 365.
- **Additional storage for Oct 8–9 not yet invoiced.**
- **Whether the $112.19 storage predates the hold** — inferred from the Oct 7 invoice date; not stated.
- **No pickup/delivery confirmation**; no ETA to Kirsten's warehouse.
- **PN attribution conflict:** checklist §5.6 says **Iolanda (Omega)** files the PN; `fda_fsvp` evidence
  shows **TrueTech self-filed** (`F26X30142399`, 06/10). **Unresolved.**

## Source

Thread `garyjob@agroverse.shop` ↔ `imports@5cl.rs` / `graziela@5cl.rs`, subj.
*"Quote Gary / Exportação = NCM 1801.00.00 / Docs / Averbação"*: msgs `1a124c0825a04d6d`,
`1a125dcc123b1044`.
PDFs: **AWB** `5146f8d2893b4d7b97150795f901f12b.pdf` / `e376a900c089431bae2625832e1788f7.pdf` (12 pp.,
`047-3175-3223`) · **Invoice #1026-08** `955a5ce4451e494ab432672ee5a04576.pdf` /
`d4f1d171cea94fa48cd38bd1e0d3a8ba.pdf` (`/tmp/tg_attachments/`).

*Analysis only. Nothing sent, nothing purchased, no money moved. The wire transfer has NOT been initiated
 — the governor said he would make arrangements; that is a governor action.*
