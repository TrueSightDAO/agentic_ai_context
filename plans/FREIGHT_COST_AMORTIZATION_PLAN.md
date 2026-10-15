# Freight Cost Amortization Plan — 5 Continent Invoice #1026-08 (AWB 047-3175-3223)

**Status:** DRAFT — awaiting governor go. **No ledger writes made.**
**Owner:** Sophia Truesight (admin+sophia@truesight.me)
**Governor:** Gary Teh
**Related:** `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`; pinned Black King landed-cost thread.
**Supersedes:** the *original* plan merged as PR **#1629** ($4,866.33; AGL15 funded both legs in full).
The base and the cash-waterfall were refined by **#1630–#1635** — read THIS file, not #1629.

---

## 1. What this books

The Brazil→SF air-freight invoice must be allocated across the ledgers whose inventory the
cargo lands on — the freight is a cost of bringing *their* inventory to SF, so it belongs on
the ledger that holds the goods, not all on the Main Ledger.

- **Invoice:** 5 Continent Logistics LLC **#1026-08**
- **Paid:** **USD 4,866.33** — **confirmed by the Wells Fargo wire confirmation**
  (`c02a149627d74a37a74fff3ac654bfdd.pdf`, the receipt the governor shared): *"Wire submitted
  $4,866.33 … To Sea Coast Logistics … From EVERYDAY CHECKING …3099 … For Invoice Number 1026 08"*,
  Confirmation **OW00007548893768**, submitted **2026-10-12 10:54 PT**, deliver-by 2026-10-13.
  (**SUPERSEDES** the earlier $4,987.39 figure — see §3-A, now closed.)
- **Wire fee:** **USD 30.00** — **folded into the amortized pool** (governor ruling, 2026-10-15) ⇒
  **amortized base = USD 4,896.33** (invoice 4,866.33 + fee 30.00), the total debited. **§3-G CLOSED.**
- **Funded from:** the **USD balance under Gary Teh's management** — the managed USD held on
  **Main Ledger** and **AGL15** (the wire drew on Wells Fargo Everyday Checking …3099, the
  operating account that holds that managed USD). ⇒ **direct debit against the managed USD**,
  **not** a third-party payable (**item #1 CLOSED**). **Cash-waterfall allocation (§2.1):** each
  landed ledger **self-funds from its own USD first**; AGL15 finances only the shortfall.
- **Basis:** shipped weight (kg) = `Currencies` unit weight × arrival quantity

## 2. Allocation (weight basis)

| Ledger | Currency lines shipped | kg | Share | Amortized |
|---|---|---|---|---|
| **Main Ledger** | 8oz Kraft Pouch ×129 · Mass Bar ×37 · Nibs ×80 · Butter ×5 · **Pará samples 5.00 kg** | 137.757 | 45.6063% | **$2,233.03** |
| **AGL8** | Almonds ×10 · Ceremonial Kraft ×169 | 43.800 | 14.5006% | **$710.00** |
| **AGL13** | Nibs Santos ×99.5 · Tea Santos ×21 | 120.500 | 39.8931% | **$1,953.30** |
| | | **302.057** | 100% | **$4,896.33** |

- **Main Ledger composition (audit):** 129 Kraft Pouch + 37 Mass Bar + 80 Nibs + 5 Butter =
  **132.757 kg**, **+ Pará samples 5.00 kg** (not part of any AGL ledger) = **137.757 kg**.
- **Portion 1 (Main Ledger)** = **$2,233.03** → **expensed** on the Main Ledger (the inventory
  unit cost already carries the freight, so no second capitalization).
- **Portion 2 (AGL8 + AGL13)** = **$2,663.30** → **cash waterfall**: each ledger **self-funds
  its share from its own USD cash first**, and **AGL15 finances only the shortfall**.

### 2.1 Cash waterfall — self-fund first, AGL15 covers the shortfall

> **Governor ruling (2026-10-15):** *"if AGL13 and AGL8 have USD balance those should be
> depleted first to account for the shipment cost before they borrow against AGL15 for
> financing."*

| Ledger | Freight share | Own USD cash | Self-funded | **Borrows from AGL15** |
|---|---|---|---|---|
| **Main** | 2,233.03 | 4,590.91 | 2,233.03 | — |
| **AGL8** | 710.00 | **564.946** | 564.946 | **145.054** |
| **AGL13** | 1,953.30 | **0.00** | 0.00 | **1,953.30** |
| | **4,896.33** | | | **AGL15 outlay: 2,098.354** |

*(USD cash read live from each ledger's `Balance` Asset section, 2026-10-15: AGL8 USD 564.946,
AGL13 none, AGL15 USD 4,240.75.)*

- **AGL8** drains its own **$564.946**, then borrows the **$145.054** remainder.
- **AGL13** holds **no USD**, so it borrows its **full $1,953.30**.
- **AGL15** outlay = **$2,098.354**; its USD after = 4,240.75 − 2,098.354 = **$2,142.396**.

Funding check: Main/Gary USD 4,590.91 ≥ P1 2,233.03 OK · AGL15 USD 4,240.75 ≥ P2 **2,098.354** OK

> **⏳ Placeholders pending NF-e derivation.** `w_MAIN = 137.757` · `w_8 = 43.800` ·
> `w_13 = 120.500` kg — derived from `Currencies` unit weight × arrival qty, **not yet
> cross-checked against NF-e nº 18 line items** (§3-C). The **shares** are robust to small kg
> corrections; the exact `$` are not. Treat the four amortized figures as **provisional**
> until §3-C closes (B is now CLOSED).

> **📌 Booked at AS-BILLED; disputed delta tracked separately.** The booking uses the
> **as-billed $4,866.33** (what was actually wired). The **$438.30 air-freight overcharge
> dispute** — the invoice bills `365 kg × $3.40 = $1,241.00` while the carrier's own AWB
> documents `349 kg × $2.30 = $802.70` → **+$438.30** — is a **separate recovery item**, tracked
> in `brazil/research/2026-10-10_VERDICT_awb_weight_349_and_rate_discrepancy.md`. **Do NOT blend
> it into the amortized base.** If 5 Continent issues a credit note for it later, that is a
> **credit event** booked then — not now.

## 3. Open items (MUST close before booking)

- **A. ~~$121.06 delta~~ — CLOSED (2026-10-15).** The Wave overdue-notice figure ($4,987.39)
  was **not** the paid amount. The **Wells Fargo wire confirmation** shows **$4,866.33** was
  actually submitted (OW00007548893768, 2026-10-12). The invoice total is $4,866.33; the **amortized base** is then raised to
  **$4,896.33** by folding in the $30 wire fee (§3-G) — a fee add, not a re-scaling. *(Lesson: an auto overdue-notice is not proof of payment; the
  bank confirmation is.)*
- **B. ~~5.00 kg gap~~ — CLOSED (2026-10-15).** Governor ruled the **5.00 kg are the Pará
  samples**, their portion **charged to the Main Ledger**. Main 132.757 → **137.757 kg**; total
  **302.057 kg** (matches the documented 302.06 net). Shares + $ re-scaled (§2).
- **C. Weight source.** Unit weights read from the `Currencies` catalog. Cross-check against
  **NF-e nº 18** per-line net kg before locking (NF-e 18 is not in the `shipment_nfe` tab,
  which holds NF-e 1–15).
- **D. Entity naming** for the three new holdings rows (see 5.2) — "AGL15" (self) vs
  "TrueSight DAO".
- **E. Event type (vehicle CONFIRMED; one question left).** The receive legs use
  **`[CAPITAL INJECTION EVENT]`** via `truesight-dao-report-capital-injection` — **verified
  managed-AGL-only** (the GAS `validateManagedLedger` rejects offchain submission), which is
  exactly what AGL8/AGL13 need. Canonical labels: `Ledger · Ledger URL · Amount · Description ·
  Attached Filename · Destination Capital Injection File Location`. **Still open:** whether an
  **internal** AGL15→AGL8/AGL13 move should use Capital Injection (documented as *external*
  investment) or `[MANAGED LEDGER TRANSACTION EVENT]`. Governor call.
- **E2. AGL15 source leg has no vehicle yet.** Debiting AGL15's USD (−$2,098.354 under the
  cash-waterfall model, §2.1) is **neither**
  a Capital Injection **nor** a `DAO Inventory Expense Event` (the latter targets *inventory*,
  not cash). Name the vehicle before the AGL15 cash-out row can be booked.
- **F. Canonical AGL15 `State` `#REF!` — CLOSED (2026-10-15); residual TBM-mirror `#REF!` remains open (non-blocking).** Governor's desktop **browser click** accepted the one-time IMPORTRANGE grant on canonical AGL15 (`1tXgDss…`, *"20260216 - Agroverse Shipment 15 Financing Ledger"* — the URL `/aum` reads via SLL col AB): `State!A1` now **spills live** (`Currencies · Price in USD`) — re-verified 2026-10-15 via the Sheets API ⇒ **§7.2 step 2 DONE.** The remaining `#REF!`s are in the **TBM donation ledger** — the "AGL15-mirrored"
  workbook (`1rNwXIp…`, registered at SLL row 18; a duplicate copy `1_MjYZ…` is orphaned):
  - `State!A1` **and** `Entities!A19` → `#REF!` *"Please use a desktop web browser to connect
    this sheet"* — an **un-approved** `IMPORTRANGE` from Main Ledger `Currencies!A:B`;
  - `Balance!A6/E6/H6/L6` → `#REF!` *"Unresolved sheet name 'Transactions'"* (`1_MjYZ`) /
    `#VALUE!` *"Unable to parse query"* (`1rNwXIp`).
  **The IMPORTRANGE fix needs a HUMAN** — open the TBM sheet in a browser, click `State!A1`,
  accept the one-time "Allow access" dialog (no service account/script can click it); the 4
  Balance QUERY clauses are then repairable via API.
  **Impact on THIS plan: none** — `/aum` reads each ledger's **`Balance`** (not `State`), and
  canonical AGL15's Balance is clean, so the new holdings value once the §6 `Currencies` rows
  exist. **F does not block the freight booking.**
- **G. ~~$30 wire fee~~ — CLOSED (2026-10-15).** Governor folded it into the amortized pool ⇒
  base = **$4,896.33**. Booked as a **pooled landed cost** (weight-allocated), not a
  separate Main-Ledger expense.
- **H. ~~Beneficiary name~~ — CLOSED (2026-10-15).** The wire reads **"To Sea Coast
  Logistics"**; the invoice/quote are from **"5 Continent Logistics LLC."** **Governor ruling:**
  these are the **SAME entity** — the receiving bank's rendering of our **forwarder**, **not** a
  mis-payee and **not** a discrepancy. Corroborated: `PURCHASE_AGREEMENT_PDFS.md` already uses
  **"Sea Coast Logistics"** as our canonical example *forwarder* name, and the wire narrative
  itself names the invoice (*"For Invoice Number 1026 08"*). **No further action.**
- **I. Who paid — CLOSED (2026-10-15).** Governor confirmed the **$4,866.33 was wired from the
  USD balance under his management** (Wells Fargo Everyday Checking …3099 — the operating account
  holding the DAO-managed USD). ⇒ a **direct debit against the DAO-managed USD** (Main Ledger +
  AGL15 USD), **not** a reimbursement or payable to Gary/TrueTech. Portion 1 books as a
  Main-Ledger **expense** that reduces managed USD; **no offsetting liability arises**.

## 4. Write primitive — never write `Balance`

All three managed `Balance` tabs (AGL8/AGL13/AGL15) are **derived array formulas** that spill
from their own `Transactions` tab, e.g.:

```
Balance!A6 (Equity) = query(Transactions!$A$4:F1012, "select C, sum(D), E where F='Equity' group by C, E ...")
Balance!E6 (Asset)  = Query(query(Transactions!$A$4:G1011, "select E, sum(D) where F='Assets' group by E, F ..."))
Balance!H6 (Resource) = query(query(Transactions!$A$4:G1011, ...))
Balance!L6 (Liab.)  = ifna(query(Transactions!$A$4:F1012, ...))
```

> ### 🔒 Writes go to `Transactions` ONLY — never `Balance`
>
> **Writing any `Balance` cell reproduces the 2026-10-14 `#REF!` incident ×3.** All three
> managed `Balance` tabs are formula-derived views of their own `Transactions` tab. The only
> safe primitive is to **append rows to the `Transactions` substrate**; the `Balance` view
> re-spills. This applies to **every leg** of this plan, without exception.

- Main Ledger substrate: `offchain transactions` — cols A–G:
  `Transaction Date · Description · Fund Handler · Amount · Currency · Ledger Line · Is Revenue`
- Managed-ledger substrate: `Transactions` — cols A–F:
  `Date · Description · Entity · Amount · Currency · Transaction Type`

The tokenomics handler `capital_injection_processing.js` opens the target ledger via
`Shipment Ledger Listing` and appends exactly two rows (`+amount USD / Assets`, then
`+amount USD / Equity`), stamping `PROCESSED` — idempotent on Telegram update/message ID.

**Use the two existing CLI primitives for every leg — do NOT hand-write any Balance cell and
DO NOT hand-roll the append** (verified to exist in `dao_protocol`, package
`truesight_dao_client`, `pyproject.toml` `[project.scripts]`):

| Leg | Module | Console entry point |
|---|---|---|
| Capital injection (AGL15→AGL8, AGL15→AGL13) | `report_capital_injection.py` | `truesight-dao-report-capital-injection` |
| Expense (Main Ledger P1; AGL8/AGL13 shares) | `report_dao_expenses.py` | `truesight-dao-report-dao-expenses` |

These produced the AGL15→AGL13 precedent row, so the path is battle-tested and matches the
handler's append semantics exactly.

## 4b. Traps A–C — structural, do NOT repeat

- **Trap A — double-counting the freight.** The inventory `Unit Cost` **already embeds** the
  landed freight. Booking the same freight *again* as a ledger **expense** counts it twice
  (once via unit cost → COGS, once as an expense line). **Rule:** our choice is
  **ledger-level expense**, and we do **not** additionally re-load the unit cost. Pick ONE
  treatment per ledger and state it in the booking note. (Cross-ref: this is the same failure
  class the `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` freight handling warns about.)
- **Trap B — writing a derived `Balance` cell.** All three `Balance` tabs are `query()` array
  formulas spilling off their own `Transactions` tab (§4). A single write reproduces the
  **2026-10-14 `#REF!` incident ×3**. **Rule:** writes go to the **`Transactions` substrate
  only, never `Balance`** — verify with the API's `formulaValue`, then re-check the spill after
  every append.
- **Trap C — blending settled vs disputed.** Book at the **$4,896.33 actually debited**
  (invoice 4,866.33 + fee 30.00). Keep the **$438.30 overcharge delta** and the superseded **$4,987.39** Wave figure
  **out of the amortized base** — they are separate tracking/recovery items, not booking inputs.
  Mixing them re-scales every leg.

## 5. Dry-run entries

### 5.1 Main Ledger — Portion 1 (expense)

Event: **`DAO Inventory Expense Event`** (console `truesight-dao-report-dao-expenses`) —
appends to the `offchain transactions` substrate:

| Canonical field | Value |
|---|---|
| DAO Member Name | Gary Teh |
| Target Ledger | `offchain` *(literal — the GAS dispatches Main Ledger by this name)* |
| Latitude / Longitude | *(empty)* |
| Inventory Type | USD |
| Inventory Quantity | 2233.03 |
| Description | `5 Continent #1026-08 air freight, AWB 047-3175-3223 — Main Ledger share (45.6063% of $4,896.33 by shipped kg, incl Pará samples)` |
| Attached Filename | *(invoice PDF)* |
| Destination Expense File Location | *(Main Ledger)* |
| Submission Source | autopilot |

### 5.2 AGL15 — finances the shortfall only (cash → holdings)

Append to AGL15 `Transactions`:

| Date | Description | Entity | Amount | Currency | Type |
|---|---|---|---|---|---|
| 20261014 | 5 Continent #1026-08 freight — AGL15-financed shortfall (AGL8 $145.054 + AGL13 $1,953.30) | Gary Teh | -2098.354 | USD | Assets |
| 20261014 | Investment in AGL8 (freight shortfall financed) | AGL8 | 145.054 | AGL8 equity holdings | Assets |
| 20261014 | Investment in AGL13 (freight share financed) | AGL13 | 1953.30 | AGL13 equity holdings | Assets |

Net: AGL15 assets unchanged (cash → holdings); equity unchanged. Outlay **$2,098.354** —
AGL8 self-funds its own $564.946.

### 5.3 AGL8 — receive + expense

Append to AGL8 `Transactions`:

| Date | Description | Entity | Amount | Currency | Type |
|---|---|---|---|---|---|
| 20261014 | Capital injection from AGL15 (freight shortfall financed) | AGL15 | 145.054 | USD | Assets |
| 20261014 | Capital injection from AGL15 (freight shortfall financed) | AGL15 | 145.054 | USD | Equity |
| 20261014 | 5 Continent #1026-08 freight — AGL8 share | AGL8 | -710.00 | USD | Assets |

Net AGL8: cash **564.946 → 0** (drains its own USD; +145.054 in − 710.00 out = −564.946);
Equity **+145.054** (AGL15's stake is only the financed shortfall, not the full share).

### 5.4 AGL13 — receive + expense

Append to AGL13 `Transactions`:

| Date | Description | Entity | Amount | Currency | Type |
|---|---|---|---|---|---|
| 20261014 | Capital injection from AGL15 (freight share financed) | AGL15 | 1953.30 | USD | Assets |
| 20261014 | Capital injection from AGL15 (freight share financed) | AGL15 | 1953.30 | USD | Equity |
| 20261014 | 5 Continent #1026-08 freight — AGL13 share | AGL13 | -1953.30 | USD | Assets |

Net AGL13: holds **no USD cash**, so it borrows its **full $1,953.30**; cash nets to zero,
Equity **+1953.30**.

**Separate item (do NOT fold in):** AGL13 `Balance` already carries an Equity row
`AGL15 · 211.77 · USD` with **no reciprocal asset on AGL15**. Completing that half-recorded
entry is a **separate reconciliation**; book only the freight share ($1,953.30) in this batch.
**After this batch AGL15's total recorded stake in AGL13 = 211.77 + 1953.30 = $2,165.07.**

### 5.5 Booking reconciliation — the $30 wire fee does not silently vanish

Invoice #1026-08 is **$4,866.33**; the Wells Fargo wire debited **$4,896.33** (invoice + **$30.00**
fee, §3-G). Per the governor's ruling (2026-10-15) the fee is **weight-allocated into each
leg's booked amount** (a pooled landed cost), **not** booked as a separate Main-Ledger expense.
So the three booking amounts must sum to the **debited** total, with the fee's weight-share
living *inside* each:

| Leg | Booked amount | of which = $30 fee-share |
|---|---:|---:|
| Main Ledger (§5.1) | 2,233.03 | 13.6819 |
| AGL8 (§5.3) | 710.00 | 4.3502 |
| AGL13 (§5.4) | 1,953.30 | 11.9679 |
| **Total** | **4,896.33** | **30.0000** |

**Invariant (verify post-booking).** Σ booked expense amounts = **$4,896.33** =
$4,866.33 (invoice) + $30.00 (fee). If the booked amounts sum to only **$4,866.33**, the fee
has vanished — re-check the legs. (Weight split = Main 45.6063% · AGL8 14.5006% · AGL13 39.8931%.)

## 6. Currency catalog additions — DONE (2026-10-15)

New asset names, each with **Price in USD = 1.0** (USD-at-par) so `/aum` rollups value them.
**Added live to MAIN `Currencies` (rows 168-170)**, verified by direct read-back:

- `AGL8 equity holdings`  (on AGL15)
- `AGL13 equity holdings` (on AGL15)
- `Main Ledger equity holdings` — **separate, historical** item (AGL15's prior Main-Ledger
  investment); **not** part of this freight batch. **Do NOT call it "TDG holdings"** — TDG is
  a distinct live token (~2.4M circulating).

Confirmed (governor): **AGL8 already independently holds USD 564.946 as an asset** (small,
pre-existing). Under the **cash-waterfall model (§2.1)** AGL8 **spends that 564.946** on its
freight share and borrows only $145.054: post-booking cash = 564.946 + 145.054 − 710.00 = **0**.

## 7. Sequencing

1. Close open items **A–F**.
2. ~~Repair AGL15 `State` (`#REF!`) + add the `Currencies`/`State` rows~~ — **DONE (2026-10-15)**:
   governor's browser click fixed canonical AGL15 `State!A1`; the 3 §6 `Currencies` rows are
   live on MAIN (rows 168-170). *(Residual TBM-mirror `#REF!` is separate + non-blocking — see §3-F.)*
3. Dry-run each leg -> governor review.
4. **On explicit go:** book Main Ledger -> AGL15 -> AGL8 -> AGL13.
5. Verify each `Balance` re-spill matches the expected figures.

> WARNING — **Gate:** no final ledger settlement until the governor gives an explicit go (ledger
> writes move money). Code/metadata work proceeds without it.
