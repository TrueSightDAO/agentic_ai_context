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

**Effects:** QR status → **`Reserved`** · cash recognised under `Payment Collected By` ·
**revenue deferred** (not a sale).

### Event 2 — `RESERVATION SETTLEMENT EVENT` (goods collected)

| Field | Meaning |
|---|---|
| `QR Code` | the reserved item being collected |
| `Buyer Email` | recipient of the confirmation email |

**Effects:** QR status → **`SOLD`** · inventory count **reduced** · **sale revenue books here** · buyer emailed.

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

## Open decisions (not yet ruled)

1. **Inventory relief timing** — does the count drop at Event 1 (reserve) or Event 2 (settle), and off **whose** manager row?
   (holder stays +1 with a `Reserved` flag · vs buyer goes −1 [Model C] · vs a liability line [Model B].)
   — **the one mechanic still open.**
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
