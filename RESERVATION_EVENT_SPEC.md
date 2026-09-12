# RESERVATION EVENT — Specification v0 (DRAFT)

**Status:** Draft for governor review.
**Owner:** Sophia Truesight (admin+sophia@truesight.me).
**Origin:** AGL14 / Telegram thread 25671 (the Flow-4 stray-row case study).
**Design thread:** Telegram topic 26819 — "Design: reservations & deposits on the ladder".

---

## 1. Purpose

A **RESERVATION EVENT** is a single signed event that lets a governor:

1. **report an amount set aside** (money placed to hold something), and
2. **name the target item on a ledger** (which item, on which ledger, optionally which specific QR codes), and
3. **record who passed the money** (the payer, and optionally the beneficiary if different).

It exists so that the join "*this money is for these items*" is written **once**, by a signed event — instead of being reconstructed later by inference.

---

## 2. Motivation — the AGL14 failure mode

AGL14 (thread 25671) produced a recurring **unsigned** bare ledger row.

- 40 QR codes (`2024OSCAR_AGL14_20260911_1..40`) were marked **SOLD**.
- The $800 Stripe checkout arrived via the **Stripe → managed-ledger router** (Flow 4, `STRIPE_LEDGER_ROUTING.md`), which hand-writes a bare, unsigned row (`Type=Sale`).
- Nothing bound the money to those specific codes. The relationship lived in **two places** and was never joined, so the system reconstructed it twice — slightly differently.

The root cause was **a missing abstraction, not a bad line of code**. (Gary's ruling: the router is NOT to be modified; the stray stemmed from how that particular Stripe checkout was generated.)

A RESERVATION fixes this structurally: you cannot reserve against bags without **naming** them, so an unsigned stray row becomes impossible.

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
| 6 | `QR Codes` | preferred | Specific bags held aside | `2024OSCAR_AGL14_20260911_1 .. _10` |
| 7 | `Quantity` | yes | Units held (assert `Quantity >= len(QR Codes)`) | `10` |
| 8 | `Paid By` | yes | **Who passed the money** | `BionPact Pte Ltd` |
| 9 | `Paid By Email` | yes | Contact for the payer | (never invented — omit if unknown) |
| 10 | `Beneficiary` | no | Who the reservation is held *for*, if ≠ payer | `—` |
| 11 | `Reservation Type` | yes | `Refundable Deposit` \| `Prepayment` | `Prepayment` |
| 12 | `Expires On` | yes | TTL — when the hold lapses | `2026-12-31` |
| 13 | `Release Path` | yes | What happens at expiry/settlement | `Convert to Sale` \| `Refund` \| `Expire` |

---

## 4. Accounting shape — why it is a Liability, never revenue

Money "placed to keep something aside" is **not** revenue. On reserve:

- `Assets +<Amount> <Currency>` (cash received), **and**
- `Liability +<Amount> <Currency>` (obligation owed back to the payer).

**Never** `Equity`. **Never** `Type = Sale`.

The valid `Type` enum on managed ledgers is **`Assets | Equity | Liability | Loan`** only — there is no `Sale`/`Expenses` type.

Only on **release → Convert to Sale** does the Liability retire and the sale book. Until then the money is *owed back*, not *earned*.

**Upstream precedent:** purchase agreements are **50% due on signing / 50% on arrival** (`PURCHASE_AGREEMENT_PDFS.md`). A customer-side reservation is the retail *mirror* of that existing practice.

---

## 5. QR state model — the AGL14 rule

- Held bags get status **`Reserved`** — **NOT `SOLD`**.
- Reservation **names the QRs**, so the money↔bags join is written *once*, by the event itself.
- On **Convert to Sale** → named QRs flip `Reserved → SOLD`.
- On **Expire / Refund** → named QRs flip `Reserved → In Inventory`.

> Marking a bag `SOLD` before the money lands is the exact AGL14 failure mode. This rule is non-negotiable.

---

## 6. Idempotency — the col-P lesson

The Flow-4 router's only guard lived on **one** side (Stripe-tab col P `LedgerRouted`). A RESERVATION must be keyed on **both** sides:

- the `Reservation ID` unique on the **money** side, and
- the **QR / quantity** side.

Re-firing the event (or re-running the pipeline) must be a **no-op**, not a second row.

---

## 7. Target-item resolution

"Target item on a ledger" must resolve to a **canonical pointer**, not free text — otherwise we rebuild the two-roads problem. Candidate key:

```
(Target Ledger, Target Item, [QR Codes])
  with Quantity >= len(QR Codes)
```

---

## 8. Release paths

| Release Path | Ledger effect | QR effect |
|--------------|---------------|-----------|
| Convert to Sale | Liability retires; sale books | `Reserved → SOLD` |
| Refund | `Assets -Amount`; Liability retires | `Reserved → In Inventory` |
| Expire | Liability retires (no cash movement) | `Reserved → In Inventory` |

---

## 9. Open questions (governor decision needed)

1. **State model** — new `Reserved` QR status, or a reservations table keyed by QR with a derived display status? *(Lean: table + derived status, so we don't disturb the QR manager's enum.)*
2. **Release authority** — who may release, and does release emit its own signed event (`Release` / `Refund` / `Convert`), or is it a status write?
3. **Expiry sweep** — cron job? Dead reservations = stale marks = the mirror of the original bug.
4. **Beneficiary ≠ payer** cases (gift / third-party reservation).
5. **Terminology** — Gary said "on our **ladder**"; no canonical "ladder" term exists in context (`EDITORIAL_TONE.md` has only a passing metaphor). Need Gary to name it before this hardens.

---

## 10. Relationship to existing events

| Related | Relationship |
|---------|--------------|
| `SALES EVENT` | RESERVATION ≠ SALES. QR stays `Reserved`, not `SOLD`, until converted. |
| `INVENTORY MOVEMENT` | Custody transfer between known holders; QR stays IN INVENTORY. Orthogonal — a reservation does not move custody. |
| Flow 4 router | RESERVATION is the signed ingress that a managed-ledger inflow *should* use. **Router itself is NOT to be modified** (Gary's ruling). |

---

## 11. References

- `STRIPE_LEDGER_ROUTING.md` §Flow 4 — the router that produced the stray row.
- `PURCHASE_AGREEMENT_PDFS.md` — upstream 50/50 deposit precedent.
- `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` — inventory/quantity model.
- AGL14 / Telegram thread 25671 — case study.
