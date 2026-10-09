# CORRECTION — We DO have a US customs broker (5 Continent) + the hold is USDA/APHIS

**Date:** 2026-10-09 · **Author:** Sophia Truesight (autopilot) · thread 10800
**Trigger:** governor — *"We do have a customs broker check the email thread"*
**Corrects:** PR #1563 (`2026-10-09_who_files_aphis_broker_vs_importer_RESEARCH.md`)

---

## 0. ⚠️ The correction — the governor is right

PR #1563 concluded *"there is no US customs broker named anywhere in our context."* **That is WRONG.**

`imports@5cl.rs` (5 Continent), **Fri 2026-10-09 16:29 −0300**:

> *"**Our broker is handling this.** We are monitoring the situation to ensure the shipment can be
> picked up as soon as the **Department of Agriculture** releases it."*

**We do have a broker — 5 Continent's** — and they are actively working the release.

### Why I got it wrong (method failure, worth recording)

- I searched the **`fda_fsvp` repo**, **`agentic_ai_context`**, and the **`admin`** mailbox — and found
  every broker reference to be Brazil-side. I then wrote *"no US broker named anywhere in our context."*
- **But "our context" meant repos — not the live mailbox.** The decisive evidence was in **Gary's
  `garyjob@agroverse.shop` thread** with `imports@5cl.rs`, which I had not searched.
- **Absence of evidence in one store is not absence.** I answered a *"who is our broker?"* question by
  searching *documents about cacao*, then stated the negative too confidently. **`gmail_search` on the
  `gary` account was the obvious first move, and I made it last, under correction.**

## 1. 🎉 The thread also ANSWERS the open agency question — it is USDA, not FDA

Same email: *"the shipment is currently on **agriculture hold**, and **CBP** … may decide to inspect it
before releasing it"* — and *"as soon as the **Department of Agriculture** releases it."*

| | Hypothesis (PR #1560) | Now confirmed |
|---|---|---|
| Agency | *"AQI/USDA, not FDA — unresolved"* | ✅ **Department of Agriculture (USDA/APHIS)** |
| Enforcement arm | CBP/AQI | ✅ **CBP** |

**⇒ The AQI-vs-FDA fork I called "the single highest-value question" is CLOSED — in favour of
USDA/APHIS.** **Import Alert 34-01 (FDA) is therefore likely the WRONG frame**; the APHIS line reopens —
and with it the **PPQ 587 permit** question from PR #1562.

**⚠️ But a broker handling the release does NOT resolve the permit question.** If a PPQ 587 is required
for the whole beans and none exists, **no broker can conjure one.** Still open; now the critical path.

## 2. 🔴 NEW — the storage clock is now the biggest number in the file

Gary asked for the rates; 5 Continent supplied them (Fri 2026-10-09 16:08 −0300):

> *"**Storage: $1 per kilo per day** on **chargeable weight** and (**30% surcharge applied to freight
> after 72hrs**). **Minimum STG Per Day: $200**"*

### Arithmetic

| Component | Value | Basis |
|---|---|---|
| Chargeable weight | **365 kg** | 5 Continent's figure |
| Storage | **$365/day** | $1/kg/day — exceeds the $200/day floor |
| Freight | **$1,241.00** | $3.40/kg × 365 kg |
| **30% surcharge** | **$372.30** | per the 72-hr rule |
| Arrival | **08/10 14:30** | PN `F26X30142399` |
| **72 hrs expires** | **11/10 14:30 (Sunday)** | ⇒ surcharge lands **inside the dead zone** |

**Estimate to a Tuesday 13/10 release, storage running from Fri 09/10:**
**4 days × $365 = $1,460 + $372.30 = ~$1,832**, and climbing.
(Five days ⇒ **~$2,197**.)

### ⇒ This reframes the thread

- The 5 Continent invoice dispute is **~$1,355.73**. The delay cost could be **~$1,800+ and growing**.
- **The hold is regulatory, so the storage may be nobody's fault** — but it means **litigating the invoice
  is now the smaller prize.**
- **Strategic shift: getting released Tuesday morning outweighs re-litigating the invoice.**
  *Every day is ~$365.*

## 3. REOPENED — the 365 vs 349 kg divergence

- **5 Continent:** *"quotation clearly stated **329 kg**. The final **chargeable weight was 365 kg**,
  which is **36 kg above** the quoted weight."* And: *"final gross weight is the cargo weight +
  pallet weight."*
- **Gary:** *"my record shows that cargo weight **including pallets was 349kg**."*
- **Our AWB:** gross **349.000 kg** (§5.5, previously marked **CLOSED**).

**349 (AWB gross, incl. pallets) vs 365 (billed chargeable) = 16 kg unexplained.**
§5.5's "CLOSED" status should be **reopened** — the invoice now depends on that number, **and so does
 every storage day.**

## 4. Also clarified in the thread (invoice adjudication inputs)

1. **The $100 FDA filing is a real, separate service.** *"The FDA Prior Notice you completed and the FDA
   filing service performed by our team are separate services… It is not a charge for completing the
   Prior Notice on your behalf."* ⇒ **5 Continent does perform US-side regulatory filing** — consistent
   with the broker claim, and it partly rebuts our "double-charge" reading.
2. **$65 palletizing** — securing cargo for international transport; *"Proper export packing and securing
   of the cargo is the shipper's responsibility."* ⇒ **Our obligation; weak ground to dispute.**
3. **Storage + a Saturday airport fee** — 5 Continent attributes these to export paperwork not being ready
   inside Friday's Brazilian clearance window. ⇒ **Attribution dispute between us, Omega and 5 Continent**
   (see `2026-10-09_5continent_graziela_reply_adjudication.md`).
4. **Brazilian export customs** is **separate**, quoted by **Omega directly**; *"Brazilian export customs
   and US import customs involve different requirements and costs."*

## 5. Revised ownership table (supersedes PR #1563 §0)

| # | File | Who | Status |
|---|---|---|---|
| 1 | **APHIS PPQ 587 permit** (if required) | 🔴 **Unresolved — must be settled** | **open, critical path** |
| 2 | **APHIS Core message set** transmission in ACE | ✅ **5 Continent's broker** | **covered** |
| 3 | **FDA Prior Notice** | ✅ Us — 5C additionally bills a filing service | **done** |

## 6. Honest gaps

- **Is 5 Continent's broker *our* broker, or the forwarder's broker acting on the entry?** The email says
  *"our broker"* — ambiguous. **Whose name is on the entry as importer of record and broker of record?**
  Not established from documents.
- **Whether a PPQ 587 permit exists / is required for the 15 kg of whole beans** — unverified
  (ACIR login-gated).
- **Whether CBP has inspected, or merely *may* inspect** — nothing new since 16:29 −0300.
  **No emergency action notice seen** ⇒ still a **hold, not a finding.**
- **Whether the 30% surcharge applies to the full $1,241 or only the increment** — assumed full;
  needs confirmation.

## Source

Thread: `garyjob@agroverse.shop` ↔ `imports@5cl.rs` / `graziela@5cl.rs`,
subject *"Quote Gary / Exportação = NCM 1801.00.00 / Docs / Averbação"*, messages
`1a121f92a07014d8`, `1a12211c4453c7d1`, `1a12224b80108220`, `1a1215a7694cfe1a` (08–09 Oct 2026).

*Analysis only. Nothing sent, nothing purchased, no money moved.*
