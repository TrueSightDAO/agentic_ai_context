# RESERVATION EVENT — Design Spec (v3)

**Status:** design **fully ruled** (v3.1) — implementation starting. Supersedes v2 (2026-09-12).
**Owner:** Gary Teh · **Drafted by:** Sophia Truesight

## Scenario

A buyer pays cash for a **specific, QR-coded item** but has **not yet collected it**.
Money has changed hands; the goods have not. This is neither a sale (no possession
change) nor a plain inventory movement (money moved). It is a **reservation**.

**Correction (verified 2026-09-12):** the DAO's ledgers are **cash-basis** — revenue is
recognised wherever the **positive-USD cash leg** lands, which is **Event 1 (reservation)**, not
settlement. See Ruled #3. Settlement books only the *non-revenue* legs (inventory −1, tree liability +1).

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

3. **Revenue-recognition timing (RULED, verified against the aggregators):** the DAO ledger is
   **cash-basis** — every revenue aggregator keys off the **positive-USD cash leg**, so revenue is
   recognised at **`RESERVATION EVENT` (T1)**, the moment cash is booked.
   `RESERVATION SETTLEMENT EVENT` (T2) books **only the non-revenue legs** (inventory −1 = leg 1;
   `Cacao Tree To Be Planted` liability +1 = leg 3), which are **not** USD-positive and are therefore
   **never** counted as revenue.
   - **No double-count (verified).** `treasury-cache` `snapshot_managed_ledgers.py` writes **per-ledger**
     JSON summing only **positive** rows (`total_amount = sum(amount for amount if amount > 0)`) — no
     cross-ledger netting, no period logic. `backfill_monthly_statistics.py` and
     `irs_tax_compilation/irs_tax_compiler.py` both select revenue as **row-level**
     `currency == 'USD' AND amount > 0` (plus an `Is Revenue` flag / sale-keyword fallback). Splitting the
     cash leg (T1) from the goods legs (T2) still yields **exactly one** positive-USD revenue row per sale.
   - **Implementation guard (important):** the settlement rows (legs 1 + 3) must **not** set
     `Is Revenue = TRUE` and must **not** carry a sale keyword (`sale` / `sales` / `sold` / `purchase` /
     `payment`) in their description — otherwise a future positive-USD settlement adjustment could be
     double-counted. The **reservation cash row is the one that carries revenue**; settlement rows do not.

4. **Refund / expiry (RULED 2026-09-12):** if the buyer never collects, the QR **stays `Reserved`
   indefinitely**. **No** reversal, **no** cancellation event, **no** auto-expiry. Consistent with
   cash-basis revenue (Ruled #3): the cash is booked, the goods simply remain held. `Reserved` is a
   *terminal-until-collected* state, **not** a timeout state — nothing sweeps it.

5. **Beneficiary ≠ payer (RULED 2026-09-12):** a **free-text note** on the reservation event is
   sufficient to record who the item is for when that differs from the payer. **No** distinct
   beneficiary field is added to the ledger schema.

6. **Email path (RULED 2026-09-12):** the settlement confirmation email **reuses the existing
   sale-confirmation sender** — GAS `sendTransactionCompletionNotification(qrCode, contributorName)`
   (already called by the `sales_update_*` processors at sale completion). **No** new mail transport.

## Open decisions

**None — the design is fully ruled.** The three former open items (#2–#4) were ruled by the governor on
2026-09-12 and are recorded below as **Ruled #4–#6**. Two residual *verification nits* (not decisions)
remain on Ruled #3: (a) confirm the ongoing treasury-cache publisher (`dao_offchain_treasury.json` /
`SNAPSHOT.md`) adds no *second* revenue surface; (b) confirm whether `Monthly Statistics` is refreshed by
an ongoing job (`backfill_monthly_statistics.py` is labelled one-time).

## Definition of Done (completion checklist)

Nothing in this feature counts as **done** until **all** of these ship. The last item is the one
easiest to forget — it lives in a *different repo* from the DApp and the ledger.

1. **DApp** — `report_reservation.html` + `report_reservation_settlement.html`, menu entries
   (section: *Retail & field activity*), and the `menu.js?v=` cache-buster bumped **in every HTML page
   and `service-worker.js`**.
2. **Ledger** — Edgar handlers for `RESERVATION EVENT` + `RESERVATION SETTLEMENT EVENT`; new QR status
   enum **`Reserved`**; `Reserved` excluded from FIFO selection and shop availability.
3. **Event-lookup tool updated** — `truesight_autopilot/app/tools/lookup_event_docs.py`.
   The tool fetches the *catalog* live from `edgar.truesight.me/events-catalog` (SSOT — no hardcoded
   event list), **but it does carry three hardcoded side-structures that must be extended**:
   - register both events in **Edgar's live events catalog** (`dao_protocol`);
   - add both to **`_INTENT_GUIDANCE`**, e.g. *"reserve item" / "buyer paid, not collected" →
     `RESERVATION EVENT`*, and *"collect reserved item" / "settle reservation" / "redeem reservation"
     → `RESERVATION SETTLEMENT EVENT`*;
   - add both to **`_IMPORTANT_FIELDS`** — Event 1: `Buyer`, `Buyer Email`, `QR Code`,
     `Payment Collected By`, `Sale Price`, `Proof`; Event 2: `QR Code`, `Buyer Email`;
   - add **`_FALLBACK_DOCS`** entries so the tool still resolves them when Edgar is unreachable.
   - Note the existing guard: `submit_contribution` requires a prior **in-session `lookup_event_docs`**
     (`SOPHIA_DAPP_EVENT_ALIGNMENT_PLAN.md`), so the two events must resolve *before* they can be submitted.

## Evidence / grounding

- `offchain asset location` already carries **negative** manager rows (e.g. `… Gary Teh … → −2`),
  so "short on inventory" is native to the ledger.
- `sales_update_managed_agl_ledgers.js` already has a **currency/ledger-targeted** booking branch
  (non-AGL4), booking `−1 <currency>`.
- `SALES EVENT` already supports `Attached Filename` (proof attachments).
- Menu convention verified in `menu.js`.
