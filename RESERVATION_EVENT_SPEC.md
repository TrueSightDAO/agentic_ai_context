# RESERVATION EVENT — Specification v1

**Status:** v1 — governor rulings folded in (2026-09-12). Supersedes v0.
**Owner:** Sophia Truesight (admin+sophia@truesight.me).
**Origin:** AGL14 / Telegram thread 25671 (the Flow-4 stray-row case study).
**Design thread:** Telegram topic 26819 — *"Design: reservations & deposits"*.
**Terminology note:** the topic title says "on the ladder" — Gary has confirmed (2026-09-12) that he said **"on our ledger"**; "ladder" was a voice mis-transcription. There is no "ladder" concept. All references corrected.

---

## 1. Purpose

A **RESERVATION EVENT** is a single signed event that lets a governor:

1. **report an amount set aside** (money placed to hold something), and
2. **name the target item on a ledger** (which item, on which ledger, and how many units), and
3. **record who passed the money** (the payer).

It exists so that the join *"this money is for these items"* is written **once**, by a signed event — instead of being reconstructed later by inference.

**What a reservation deliberately does NOT do (Gary, 2026-09-12):** it does **not** name individual **QR codes**, and it does **not** change any QR's status. The money↔bags join is written only when the transaction **closes** — i.e. when the reserver **takes possession** of the inventory — which is the `SALES EVENT`, where the QRs are named and flip to `SOLD`.

---

## 2. Motivation — the AGL14 failure mode

AGL14 (thread 25671) produced a recurring **unsigned** bare ledger row.

- 40 QR codes (`2024OSCAR_AGL14_20260911_1..40`) were marked **SOLD**.
- The $800 Stripe checkout arrived via the **Stripe → managed-ledger router** (Flow 4, `STRIPE_LEDGER_ROUTING.md`), which hand-writes a bare, unsigned row (`Type=Sale`).
- Nothing bound the money to the item. The relationship lived in **two places** and was never joined, so the system reconstructed it twice — slightly differently.

The root cause was **a missing abstraction, not a bad line of code**. (Gary's ruling: the router is NOT to be modified; the stray stemmed from how that particular Stripe checkout was generated.)

A RESERVATION fixes this structurally, in two parts:

1. **Signed money → item binding.** The reservation writes a *signed* join from the payment to `(Target Ledger, Target Item, Quantity)` — so an unsigned stray row for that money becomes impossible.
2. **QR named only at close.** Bags are named on the **`SALES EVENT`** at possession, never earlier — so a bag can never be marked `SOLD` before the money landed.

---

## 3. Event definition

**Event name:** `RESERVATION EVENT`

| # | Field | Required | Meaning | Example |
|---|-------|----------|---------|---------|
| 1 | `Reservation ID` | yes | Idempotency key (see §6) | `RSV-20260911-AGL14-001` |
| 2 | `Amount` | yes | The amount set aside | `800.00` |
| 3 | `Currency` | yes | Unit of `Amount` | `USD` |
| 4 | `Target Ledger` | yes | Ledger ID holding the item | `AGL14` |
| 5 | `Target Item` | yes | The item being held | `Cacao Almonds KG from Oscar's farm - AGL14` |
| 6 | `Quantity` | yes | Units held | `10` |
| 7 | `Paid By` | yes | **Who passed the money** | `BionPact Pte Ltd` |
| 8 | `Paid By Email` | yes | Contact for the payer | (never invented — omit if unknown) |
| 9 | `Beneficiary` | no | Who the reservation is held *for*, if ≠ payer. **Semantics OPEN** (see §9) | `—` |
| 10 | `Reservation Type` | yes | `Refundable Deposit` \| `Prepayment` | `Prepayment` |
| 11 | `Expires On` | no | TTL hint — when the hold lapses. Informational only; no sweep yet (§9) | `2026-12-31` |
| 12 | `Release Path` | no | Intended settlement. Informational only; release mechanics deferred (§9) | `Convert to Sale` |
| 13 | `Notes` | no | Free-text context | `50% deposit per purchase agreement` |

**Deliberately absent:** no `QR Codes` field. QR codes are named at **close**, on the `SALES EVENT` (see §1, §5).

---

## 4. Accounting shape — why it is a Liability, never revenue

Money "placed to keep something aside" is **not** revenue. On reserve:

- `Assets +<Amount> <Currency>` (cash received), **and**
- `Liability +<Amount> <Currency>` (obligation owed back to the payer).

**Never** `Equity`. **Never** `Type = Sale`.

The valid `Type` enum on managed ledgers is **`Assets | Equity | Liability | Loan`** only — there is no `Sale`/`Expenses` type.

Only at **close** (Convert to Sale) does the Liability retire and the sale book. Until then the money is *owed back*, not *earned*.

**Upstream precedent:** purchase agreements are **50% due on signing / 50% on arrival** (`PURCHASE_AGREEMENT_PDFS.md`). A customer-side reservation is the retail *mirror* of that existing practice. *(The settlement half of that mirror — the release/convert events — is deferred; see §9.)*

---

## 5. QR state model — REVISED (Gary, 2026-09-12)

- A reservation does **not** name and does **not** mark individual QR codes.
- **No `Reserved` QR status is introduced.** The QR-manager status enum is left untouched (this resolves v0 open question #1 in the *simplest* direction: reservations are simply not QR-scoped).
- The QR ↔ bag association is written **only at close**, when the reserver **takes possession** of the inventory — i.e. on the **`SALES EVENT`**, where the QRs are named and flip to `SOLD`.
- **The AGL14 rule is non-negotiable and preserved:** a bag is **never** marked `SOLD` before the money lands. The signed reservation is the evidence the money landed; the sale then names the bags.

---

## 6. Idempotency — the col-P lesson (re-keyed off QR codes)

v0 planned to key idempotency partly on QR codes. With QR association deferred to close (§5), the key is reworked:

- **Primary idempotency key:** `Reservation ID` (unique on the money side). Re-firing the same `Reservation ID` — or re-running the pipeline — must be a **no-op**, not a second row.
- **Resolvable pointer (not a uniqueness constraint):** `(Target Ledger, Target Item, Quantity)`. Multiple reservations may legitimately point at the same item (the quantities sum); only a duplicate `Reservation ID` is rejected.

The Flow-4 router's guard lived on **one** side (Stripe-tab col P `LedgerRouted`); the reservation's key is written on the **money** side and its target is asserted on the **item** side, so both sides carry the check.

---

## 7. Target-item resolution

"Target item on a ledger" must resolve to a **canonical pointer**, not free text — otherwise we rebuild the two-roads problem. Candidate key:

```
(Target Ledger, Target Item)
  asserted with Quantity >= 1
```

No QR codes participate in the pointer (they arrive at close).

---

## 8. Release paths — NOT IMPLEMENTED (deferred)

Gary (2026-09-12): *"Let's not go that far for now, since this scenario doesn't happen very often yet."*

The table below is retained as the **intended design**, for when release is built. No release event, status write, or expiry behaviour ships in v1:

| Release Path | Ledger effect | QR effect (at close) |
|--------------|---------------|----------------------|
| Convert to Sale | Liability retires; sale books | QRs named, `→ SOLD` |
| Refund | `Assets -Amount`; Liability retires | QRs never named; stay `In Inventory` |
| Expire | Liability retires (no cash movement) | QRs never named; stay `In Inventory` |

---

## 9. Decision log (governor, 2026-09-12)

| # | Question (v0) | Ruling |
|---|---------------|--------|
| 1 | State model — new `Reserved` status, or a QR-keyed reservations table with derived status? | **RESOLVED — neither.** A reservation does not associate with QR codes at all; the QR is associated only at **close**. No new QR status, no QR-keyed table. |
| 2 | Release authority — who may release, and is it its own signed event? | **DEFERRED** — not building yet (rare). |
| 3 | Expiry sweep — cron to lapse dead reservations? | **DEFERRED** — not building yet (rare). |
| 4 | Beneficiary ≠ payer (gift / third-party) | **OPEN** — Gary did not rule. Field kept optional (§3 #9); no semantics assumed. |
| 5 | Terminology — "ladder" | **RESOLVED** — Gary meant **"on our ledger"**. Corrected throughout. |

---

## 10. Relationship to existing events

| Related | Relationship |
|---------|--------------|
| `SALES EVENT` | The **close**. Names the QRs and flips them to `SOLD`. A reservation is the signed money-side evidence that precedes it. |
| `INVENTORY MOVEMENT` | Custody transfer between known holders; QR stays IN INVENTORY. Orthogonal — a reservation moves no custody. |
| Flow 4 router | RESERVATION is the signed ingress a managed-ledger inflow *should* use. **Router itself is NOT to be modified** (Gary's ruling). |

---

## 11. References

- `STRIPE_LEDGER_ROUTING.md` §Flow 4 — the router that produced the stray row.
- `PURCHASE_AGREEMENT_PDFS.md` — upstream 50/50 deposit precedent.
- `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` — inventory/quantity model.
- AGL14 / Telegram thread 25671 — case study.
