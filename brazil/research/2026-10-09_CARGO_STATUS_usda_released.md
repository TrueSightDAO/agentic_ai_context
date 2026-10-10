# CARGO STATUS — USDA RELEASED the shipment (2026-10-09)

**Date:** 2026-10-09 (late) · **Author:** Sophia Truesight (autopilot) · thread 10800
**Trigger:** governor — *"Cargo status update / Check the email thread"*
**Supersedes:** the storage-cost projections in PR #1565

---

## 0. 🎉 RELEASED

`imports@5cl.rs`, **Fri 2026-10-09 18:01:36 −0300**:

> *"The **Department of Agriculture has just released the shipment.** We have already requested the
> carrier to pick it up."*

**No inspection reported** — released the same day, ~3 hrs after the hold was first flagged to us
(15:41 −0300).

## 1. ⚠️ Retraction — my storage estimate in PR #1565 was wrong

I warned of **~$1,832–$2,197**. **That was wrong**, and here is the arithmetic showing why:

| Event | Time (PT) | |
|---|---|---|
| Arrival | Wed 08/10 14:30 | |
| Hold flagged | Fri 09/10 ~11:41 | *(`15:41 −0300`)* |
| **Released** | **Fri 09/10 ~14:01** | *(`18:01 −0300`)* |
| 72-hr surcharge clock | Sat 11/10 14:30 | |

**Release beat the 72-hour clock ⇒ the 30% freight surcharge ($372.30) is likely VOID.**
Storage ran **~2 days**, not 4–5: **≈ $730** (2 × $365).

**The error:** I computed *"to a Tuesday release"* as though the dead zone were certain — **before the
Friday-evening release window had even closed.** I extrapolated a worst case and presented its arithmetic
as the expected cost. **The rate card was real; the duration was speculative, and I did not label it as
such.** Lesson: state the assumption a number rests on, in the same breath as the number.

**⇒ The invoice dispute is the main event again** — ~$1,355.73 now exceeds the delay cost, and there is
no surcharge to argue about.

## 2. 🔑 The APHIS permit question resolved EMPIRICALLY

**The shipment released with no permit scenario materialising.** The **15 kg of whole beans**
(articles 0004 + 0009) — the concentrated exposure flagged in PRs #1559/#1560/#1562 — **did not block
release.**

**⇒ For this shipment, no PPQ 587 was required.** That does not prove the manual's text is favourable;
it proves **practice didn't bite.** The ACIR lookup is still worth doing **for future shipments**, but it
is **no longer a live blocker on 10800.** Down-graded: *critical path* → *standing-process follow-up.*

## 3. 🔑 Graziela's answers — one materially changes our position

### 3.1 "Why no Brazilian export customs in 2023, but a line item in 2026?"

> *"**You had hired that service separately.** You also hired the **air freight services separately**
> last time — **we only handled clearance for you back in 2023.**"*

**A legitimate answer — and it defeats our own 2023-comparison argument.** In 2023, 5 Continent
**only did clearance**; export-customs and air-freight sat with other parties (Omega et al.). In 2026
they do **export customs + air freight + clearance** — **a different scope of engagement.**
Comparing 2023 to 2026 line-by-line (**PR #1544**) **presupposes the same scope. It wasn't.**

### 3.2 The $100 FDA filing

> *"FDA Filing with US customs is the **integration of your prior notice with the actual customs
> clearance in the AMS system**."*

**That is the ACE/AMS transmission — the broker-side filing** in PR #1563/#1565's ownership table.
**A real, distinct service.** Our "we already filed the Prior Notice ⇒ double charge" reading
**does not hold.** *($100 conceded.)*

### 3.3 The weight — a direct contradiction, AWB is the authority

> *"Cargo was weighed at the airport, and the final weight, **including pallets, was determined to be
> 365 kgs, as shown in the paperwork (AWB)**."*

| Source | Figure |
|---|---|
| Graziela (cites AWB) | **365 kg** incl. pallets |
| Gary's record | **349 kg** incl. pallets |
| Our checklist §5.5 | **349.000 kg** gross |

**Both claim "incl. pallets" and they differ by 16 kg ⇒ one reading of the AWB is wrong.**
**Unresolved:** the 2026 AWB is **not** in `fda_fsvp` (only the **2023** TAP AWB is:
`047-04136716`, **8 volumes, 104.0 kg**). The 2026 AWB was an **email attachment I cannot read.**
⇒ **Action: open the AWB PDF, read the weight box.** Worth **both $54.40 in freight and every storage
 day.**

## 4. Gary's open questions — still UNANSWERED

1. *"Will the freight be shipped only when the invoice amount has landed in the bank account, or proof
   of the transfer is sent?"*
2. *"Will freighting to destination warehouse only happen during weekday, or weekend is possible?"*

**These are now the live questions** — the hold no longer gates anything; **payment terms do.**
And Q2 matters because the **72-hr surcharge clock runs against the *freight*, not the customs hold**:
if the shipment sits awaiting payment past **Sat 11/10 14:30**, the **$372.30 may re-attach for a
different reason.**

## 5. Scoreboard

| Item | Before | Now |
|---|---|---|
| USDA hold | 🔴 open | ✅ **released Fri 18:01 −0300** |
| Inspection | possible | ✅ **none reported** |
| Storage exposure | ~$1,832–2,197 | ✅ **~$730** |
| 30% surcharge | expected | ✅ **likely void (beat clock)** |
| APHIS PPQ 587 | 🔴 critical path | ⚪ **empirically not required** |
| Brazilian export customs line | disputed | 🟡 **legitimate — different 2026 scope** |
| $100 FDA filing | disputed | 🟡 **legitimate (AMS integration)** |
| $65 palletizing | disputed | 🟡 shipper's responsibility — weak ground |
| Weight 365 vs 349 | reopened | 🔴 **open — read the AWB** |
| Invoice ~$1,355.73 | secondary | 🔴 **main event again** |

## 6. Honest gaps

- **No carrier pickup confirmation yet** — 5 Continent *requested* it; no proof of collection, no
  delivery ETA to the destination warehouse.
- **AWB weight unverified** (§3.3).
- **Whether "released" means *no inspection* or *inspected and passed*** — not stated. Materially
  different for the process doc.
- **Payment-terms answer outstanding** — gates the freight (§4).
- **30% surcharge**: *likely* void because release beat 72 hrs; **if pickup/delivery slips past
  Sat 14:30 it may re-attach.**

## Source

Thread `garyjob@agroverse.shop` ↔ `imports@5cl.rs` / `graziela@5cl.rs`, subj.
*"Quote Gary / Exportação = NCM 1801.00.00 / Docs / Averbação"*:
`1a1227900962d661` (release, 09/10 18:01 −0300) · `1a124c0825a04d6d` (Graziela's answers,
10/10 15:38 +0800) · `1a12289de491523b` (Gary's open questions, 09/10 18:20 −0300).

*Analysis only. Nothing sent, nothing purchased, no money moved.*
