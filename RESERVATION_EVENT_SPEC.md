# RESERVATION EVENT — Specification v2

**Status:** v2 — two-event hold model (Gary's Model B, 2026-09-12). Supersedes v1.
**Owner:** Sophia Truesight (admin+sophia@truesight.me).
**Origin:** AGL14 / Telegram thread 25671 (the Flow-4 stray-row case study).
**Design thread:** Telegram topic 26819.

---

## 0. The scenario (in one paragraph)

A buyer **pays us cash for goods we have not yet handed over.** The money is in the pocket of the DAO member who took it. The goods are still physically with us/our holder. We need a signed record that (a) the money landed, (b) *what* the money is holding, and (c) who is holding the cash — and then a second record when the buyer actually **takes possession**.

---

## 1. The model — two events

| # | Event | Trigger | QR status | Ledger |
|---|-------|---------|-----------|--------|
| 1 | **`RESERVATION EVENT`** | money lands; goods NOT yet handed over | mint if needed → **`Reserved`** | `Assets +Amount USD` · `Liability +N <Target Inventory Currency>` |
| 2 | **`RESERVATION CLOSE EVENT`** | buyer takes possession (we deliver) | **`Reserved` → `SOLD`** | `Liability −N <Target Inventory Currency>` · `Assets −N <Target Inventory Currency>` (inventory relieved) |

### Why the QRs are named at Event 1 (reversal of v1)

v1 said *"don't name the QRs until close."* Gary's ruling (2026-09-12): **you cannot hold what you cannot name** — the reservation must name the bags, or the liability has nothing to point at. So Event 1 names the QR codes (minting them if the goods have none) and flags them `Reserved`.

### Why "liability in terms of inventory" is correct (Gary's Model B)

Gary: *"Liability goes up in terms of inventory. Otherwise we won't know what the money is used to reserve for."*

This is **idiomatic for this DAO**. The managed-AGL sale path (`sales_update_managed_agl_ledgers.js`) already books a **Liability denominated in non-money units** — `+1 "Cacao Tree To Be Planted"` under `Liability` per sale. So a liability carried in inventory units is an existing pattern, not a new one.

The liability is **temporary**: it goes up by `N` at Event 1 and down by `N` at Event 2, netting to zero once the goods are delivered. While the reservation is open it is the visible marker of *"N bags are committed to a paid buyer and must not be sold to anyone else."*

---

## 2. Event 1 — `RESERVATION EVENT`

### Fields

| # | Field | Required | Meaning | Example |
|---|-------|----------|---------|---------|
| 1 | `Reservation ID` | yes | Idempotency key (§6) | `RSV-20260911-AGL14-001` |
| 2 | `Amount` | yes | Cash received | `800.00` |
| 3 | `Currency` | yes | Unit of `Amount` | `USD` |
| 4 | `Cash Custodian` | yes | DAO member who took the cash (money is "under their management") | `Gary Teh` |
| 5 | `Cash Custodian Email` | recommended | Contact for the custodian | `gary@truesight.me` |
| 6 | `Paid By` | yes | Who passed the money | `BionPact Pte Ltd` |
| 7 | `Paid By Email` | yes | Contact for the payer (never invented) | — |
| 8 | `Target Ledger` | yes | Ledger ID holding the goods | `AGL14` |
| 9 | `Target Inventory Currency` | yes | The inventory `Currency` string being held | `Cacao Almonds KG from Oscar's farm - AGL14` |
| 10 | `Quantity` | yes | Units held (`== len(QR Codes)`) | `10` |
| 11 | `QR Codes` | yes | The **named** codes held aside (mint first if needed, §5) | `2024OSCAR_AGL14_20260911_1 .. _10` |
| 12 | `Reservation Date` | yes | When the money landed | `2026-09-11` |
| 13 | `Reservation Type` | yes | `Refundable Deposit` \| `Prepayment` | `Prepayment` |
| 14 | `Notes` | no | Free-text context | `collect at SF warehouse` |

### Ledger effect

- `Assets +<Amount> <Currency>` — cash received (under `Cash Custodian`).
- `Liability +<Quantity> <Target Inventory Currency>` — the goods we owe the buyer.
- **Never** `Type = Sale`. The valid `Type` enum on managed ledgers is `Assets | Equity | Liability | Loan` only.

### QR effect

- Named QRs → status **`Reserved`** (§4).
- Manager of the reserved QRs set to `Cash Custodian` (they hold both the cash and, physically, the goods).

---

## 3. Event 2 — `RESERVATION CLOSE EVENT`

Triggered when the buyer **takes possession** — the sale actually happens.

### Fields

| # | Field | Required | Meaning |
|---|-------|----------|---------|
| 1 | `Reservation ID` | yes | Links back to Event 1 |
| 2 | `Closed On` | yes | Date of pickup |
| 3 | `QR Codes` | yes | Must match the reserved set |
| 4 | `Sold By` | yes | Inventory holder (see `SALES EVENT`) |
| 5 | `Cash proceeds collected by` | yes | Confirms the custodian (see `SALES EVENT`) |

### Ledger effect

- `Liability −<Quantity> <Target Inventory Currency>` — the hold is discharged (retires the Event-1 liability).
- `Assets −<Quantity> <Target Inventory Currency>` — inventory relieved (same shape the existing sale path uses: one `-1` inventory-unit line per QR).
- Plus whatever the standard `SALES EVENT` books (e.g. the SunMint tree-planting obligation).

### QR effect

- `Reserved` → **`SOLD`**.

### ⚠️ Open decision — Event 2 identity

Is Event 2 a **distinct event** (`RESERVATION CLOSE EVENT`), or **the existing `SALES EVENT`** carrying a `Reservation ID`?

- **Leaning: reuse `SALES EVENT`.** It already flips QR → `SOLD` and books the sale; adding a `Reservation ID` field lets it *also* retire the Event-1 liability, with one sale-booking path instead of two. **Pending Gary's call.**

---

## 4. QR state model — the `Reserved` status

- New enum value **`Reserved`** — held, money received, goods not handed over.
- **Non-negotiable (AGL14):** a bag is never `SOLD` before the money lands. `SOLD` means *delivered*.
- **Guards this forces:**
  - `Reserved` bags MUST be **excluded from FIFO selection** (`conventions/FIFO_QR_SELECTION_RULE.md`) — otherwise the next consignment sale picks a held bag and double-sells it.
  - `Reserved` bags MUST be **excluded from shop availability**.
  - The new value ripples to the GAS sales + movement processors and the QR DApp pages — a deliberate, enumerated change, not a silent one.
- Event 2 flips `Reserved → SOLD`.

---

## 5. Minting QRs at reservation

If the goods being held do not yet have a QR code (bulk lot, un-serialized stock):

1. **Mint first** — via the existing `BATCH QR CODE REQUEST` / `QR CODE EVENT` path (`AGROVERSE_QR_CODE_BATCH_GENERATION.md` naming).
2. **Then** name those new codes on the `RESERVATION EVENT` and set them `Reserved`.

A reservation never refers to un-serialized goods by free text — the whole point is a nameable target.

---

## 6. Idempotency

- **Primary key:** `Reservation ID` — unique on the money side. Re-firing the same `Reservation ID`, or re-running the pipeline, MUST be a **no-op**, not a second row.
- **Secondary:** the named `QR Codes` — a code already `Reserved` cannot be reserved again.
- Lesson from Flow-4 col-P: the guard must live on **both** sides (money *and* goods), not one.

---

## 7. Motivation — the AGL14 failure mode

AGL14 (thread 25671): 40 QRs marked `SOLD` while the $800 Stripe checkout arrived via the Flow-4 router as an **unsigned** bare `Type=Sale` row. Nothing bound the money to the goods; the join was reconstructed twice. Root cause: **a missing abstraction.** (Gary's ruling: the router is NOT to be modified.)

The reservation fixes it: a hold cannot exist without naming its goods — so an unsigned stray becomes impossible, and `SOLD` can no longer precede the money.

---

## 8. Release paths — deferred

Gary (2026-09-12): refund/expire don't happen often enough yet to build. Retained for later:

| Path | Ledger | QR |
|------|--------|-----|
| Refund | `Assets −Amount USD`; `Liability −N <inv curr>`; cash back | `Reserved → In Inventory` |
| Expire | `Liability −N <inv curr>` (no cash move) | `Reserved → In Inventory` |

No release event, status write, or expiry sweep ships in v2.

---

## 9. Decision log

| # | Question | Ruling |
|---|----------|--------|
| 1 | State model | **RESOLVED** — QRs named at reservation; new `Reserved` status; `Reserved → SOLD` at close. |
| 2 | Release authority | **DEFERRED** — not building yet (rare). |
| 3 | Expiry sweep | **DEFERRED** — not building yet (rare). |
| 4 | Beneficiary ≠ payer | **OPEN** — not ruled; field not assumed. |
| 5 | Terminology "ladder" | **RESOLVED** — Gary meant **"on our ledger"**. |
| 6 | Accounting model | **RESOLVED — Model B.** Liability denominated in **inventory units**; internal precedent is the "Cacao Tree To Be Planted" liability line. |
| 7 | Event 2 identity (distinct vs `SALES EVENT`) | **OPEN** — leaning reuse `SALES EVENT` + `Reservation ID`. |

---

## 10. Relationship to existing events

| Related | Relationship |
|---------|--------------|
| `SALES EVENT` | The likely **close** (Event 2). Names QRs `SOLD`, books the sale, retires the hold. |
| `INVENTORY MOVEMENT` | Custody transfer between known holders; QR stays IN INVENTORY. Orthogonal. |
| `BATCH QR CODE REQUEST` / `QR CODE EVENT` | Mint path for un-serialized goods (§5). |
| Flow 4 router | NOT to be modified (Gary's ruling). |

---

## 11. References

- `sales_update_managed_agl_ledgers.js` — current sale booking (3 rows); precedent for a non-money-unit `Liability`.
- `conventions/FIFO_QR_SELECTION_RULE.md` — must exclude `Reserved`.
- `AGROVERSE_QR_CODE_BATCH_GENERATION.md` — QR naming + mint path.
- `STRIPE_LEDGER_ROUTING.md` §Flow 4 — the router that produced the AGL14 stray row.
- `PURCHASE_AGREEMENT_PDFS.md` — upstream 50/50 deposit precedent.
- AGL14 / Telegram thread 25671 — case study.
