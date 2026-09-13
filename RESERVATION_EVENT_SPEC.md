# RESERVATION EVENT — Design Spec (v3)

**Status:** design only — no implementation yet. Supersedes v2 (2026-09-12).
**Owner:** Gary Teh · **Drafted by:** Sophia Truesight

## Scenario

A buyer pays cash for a **specific, QR-coded item** but has **not yet collected it**.
Money has changed hands; the goods have not. This is neither a sale (no possession
change) nor a plain inventory movement (money moved). It is a **reservation**.

Because money changed hands *before* the goods, revenue must **not** be recognised at
reservation — it books when the buyer collects.

## Two events

### Event 1 — `RESERVATION EVENT` (money in, goods held)

| Field | Meaning |
|---|---|
| `Buyer` | the person reserving (is owed the item) |
| `Buyer Email` | captured so the buyer can be notified at settlement |
| `QR Code` | the specific reserved item |
| `Payment Collected By` | DAO member who took the cash (cash custodian) |
| `Sale Price` (+ currency) | amount paid |
| `Proof` (image/PDF) | evidence money actually changed hands |

**Effects:** QR status → **`Reserved`** · cash booked under `Payment Collected By` (this is **leg 2**
of a normal sale — see mapping below). **No inventory row moves. No liability line books.**

### Event 2 — `RESERVATION SETTLEMENT EVENT` (goods collected)

| Field | Meaning |
|---|---|
| `QR Code` | the reserved item being collected |
| `Buyer Email` | recipient of the confirmation email |

**Effects:** QR status → **`SOLD`** · inventory count **reduced** (this is **leg 1** of a normal sale) ·
**the `Cacao Tree To Be Planted` liability books here (leg 3)** · buyer emailed.

### How this maps onto the existing sale booking (verified)

`sales_update_managed_agl_ledgers.js` books a sale as **three `Transactions` rows at one instant**:

| # | Contributor | Amount | Inventory Type | Category |
|---|---|---|---|---|
| 1 | Sold By | −1 | `<inventory type>` | Assets |
| 2 | Cash Proceeds Collector | +sale price | USD | Assets |
| 3 | `SunMint Tree Planting Contract - <agl>` | +1 | Cacao Tree To Be Planted | Liability |

A retail sale books **legs 1 + 2 together** (money and goods move at once). A reservation simply
**splits those legs across two events**:

- **Event 1** books **leg 2 only** (+USD to `Payment Collected By`) + sets QR `Reserved`. **No inventory row, no liability row.**
- **Event 2** books **legs 1 + 3** (−1 `<inventory type>` off the QR's **current holder**; +1 `Cacao Tree To Be Planted` Liability), sets QR `SOLD`, emails the buyer.

So the **tree-planting liability rides with the goods, not the cash** — it accrues only once the buyer
actually takes possession (settlement), matching the real-world trigger (a tree is planted per delivered bag).

No new booking machinery — the reservation flow reuses the same row shape, **one leg at a time**.

## Naming

- **Event 1:** `RESERVATION EVENT`
- **Event 2:** `RESERVATION SETTLEMENT EVENT`  (runners-up: `RESERVATION FULFILLMENT EVENT`, `RESERVATION REDEMPTION EVENT`)
- **Module 1:** "Reservation Reporter" → `report_reservation.html` (section: Retail & field activity)
- **Module 2:** "Reservation Settlement Reporter" → `report_reservation_settlement.html`

DAO convention: **module names ≠ event names** — "Sales Reporter" emits a `SALES EVENT`;
"Inventory Movement Reporter" emits an `INVENTORY MOVEMENT`. And "Settlement" already means
"close out a pending state" (`Repackaging Settlement`, `Voting Rights Settlement`).

## Prerequisites

1. **QR must exist at reservation** → if un-serialised, mint first (`BATCH QR CODE REQUEST` / `QR CODE EVENT`).
2. New QR **status enum `Reserved`** — add to GAS sales/movement processors + QR DApp pages.
3. **Exclude `Reserved` from FIFO selection** and shop availability (else the held bag is double-sold).
4. Adding the menu entries → bump `menu.js?v=` in every HTML page **and** `service-worker.js`.

## Ruled

1. **Inventory relief timing (RULED):** the physical inventory drop happens at
   **`RESERVATION SETTLEMENT EVENT` only** — never at reservation. During the reservation the goods are
   marked **solely by the QR status `Reserved`**; no inventory position moves. The drop lands on the
   QR's **current holder**. (This retires the earlier Model B / Model C "negative position" ideas.)

2. **Tree-to-be-planted liability timing (RULED):** the `+1 Cacao Tree To Be Planted` Liability line
   (leg 3) fires at **`RESERVATION SETTLEMENT EVENT` only** — never at reservation. Event 1 books **no**
   liability line; the reservation hold is marked solely by the QR `Reserved` status. Rationale: a tree
   is planted per **delivered** bag, so the obligation accrues when the buyer takes possession.

## Open decisions (not yet ruled)

1. **Residual (partly resolved):** leg-3 liability timing is now **RULED** (fires at settlement —
   Ruled #2), so Event 1 carries **no** liability line and the QR `Reserved` status is the sole marker of a
   hold. Remaining question: whether the **treasury-cache / P&L aggregation** splits the legs correctly
   (leg 2 at T1; legs 1+3 at T2) across two reporting periods, or double-counts. Needs a tokenomics schema
   check before asserting.
2. **Refund / expiry** — what happens if the buyer never collects? (deferred)
3. **Beneficiary ≠ payer** — unruled.
4. **Email path** — confirm/reuse the existing sale-confirmation sender.

## Evidence / grounding

- `offchain asset location` already carries **negative** manager rows (e.g. `… Gary Teh … → −2`),
  so "short on inventory" is native to the ledger.
- `sales_update_managed_agl_ledgers.js` already has a **currency/ledger-targeted** booking branch
  (non-AGL4), booking `−1 <currency>`.
- `SALES EVENT` already supports `Attached Filename` (proof attachments).
- Menu convention verified in `menu.js`.
