# Freight Cost Amortization Plan — 5 Continent Invoice #1026-08 (AWB 047-3175-3223)

**Status:** DRAFT — awaiting governor go. **No ledger writes made.**
**Owner:** Sophia Truesight (admin+sophia@truesight.me)
**Governor:** Gary Teh
**Related:** `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`; pinned Black King landed-cost thread.

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
- **Wire fee:** **USD 30.00** — total debit from the account **$4,896.33** (see §3-G).
- **Funded from:** the USD holdings **Gary Teh manages** on **Main Ledger** and **AGL15**
  (the wire drew on Wells Fargo Everyday Checking …3099 — the governor's personal account).
- **Basis:** shipped weight (kg) = `Currencies` unit weight × arrival quantity

## 2. Allocation (weight basis)

| Ledger | Currency lines shipped | kg | Share | Amortized |
|---|---|---|---|---|
| **Main Ledger** | 8oz Kraft Pouch ×129 · Mass Bar ×37 · Nibs ×80 · Butter ×5 | 132.757 | 44.69% | **$2,174.80** |
| **AGL8** | Almonds ×10 · Ceremonial Kraft ×169 | 43.800 | 14.74% | **$717.52** |
| **AGL13** | Nibs Santos ×99.5 · Tea Santos ×21 | 120.500 | 40.56% | **$1,974.01** |
| | | **297.057** | 100% | **$4,866.33** |

- **Portion 1 (Main Ledger)** = **$2,174.80** → **expensed** on the Main Ledger (the inventory
  unit cost already carries the freight, so no second capitalization).
- **Portion 2 (AGL15)** = **$2,691.53** → **equity injection** into AGL8 (**$717.52**) +
  AGL13 (**$1,974.01**), each immediately expensed against the invoice.

Funding check: Main/Gary USD 4,590.91 ≥ P1 2,174.80 OK · AGL15 USD 4,240.75 ≥ P2 2,691.53 OK

## 3. Open items (MUST close before booking)

- **A. ~~$121.06 delta~~ — CLOSED (2026-10-15).** The Wave overdue-notice figure ($4,987.39)
  was **not** the paid amount. The **Wells Fargo wire confirmation** shows **$4,866.33** was
  actually submitted (OW00007548893768, 2026-10-12). All four allocation figures stand on
  **$4,866.33** — no re-scaling. *(Lesson: an auto overdue-notice is not proof of payment; the
  bank confirmation is.)*
- **B. 5.00 kg gap.** Our sum = 297.06 kg vs the checklist's documented net **302.06 kg**
  (gross 349 = 302.06 net + 26.94 carton + 20 pallet). Reconcile — `Coopercabruca Butter`
  (rounds to exactly 5.000) is the suspect. Shares are robust to it; exact $ are not.
- **C. Weight source.** Unit weights read from the `Currencies` catalog. Cross-check against
  **NF-e nº 18** per-line net kg before locking (NF-e 18 is not in the `shipment_nfe` tab,
  which holds NF-e 1–15).
- **D. Entity naming** for the three new holdings rows (see 5.2) — "AGL15" (self) vs
  "TrueSight DAO".
- **E. Event type.** `[CAPITAL INJECTION EVENT]` is documented for **external investors**
  wiring into an AGL contract; AGL15→AGL8/AGL13 is **internal** (DAO fund → DAO ledger).
  Confirm `[CAPITAL INJECTION EVENT]` vs `[MANAGED LEDGER TRANSACTION EVENT]`.
- **F. AGL15/State is `#REF!`** — the AGL15 Currencies/price catalog is broken, so `/aum`
  cannot value the new holdings until it is repaired.
- **G. $30 wire fee** — a banking cost of paying, **not** part of invoice #1026-08. Decide:
  add it to the amortized pool (pool becomes **$4,896.33**) or book it separately as a
  Main-Ledger expense. It must not silently vanish.
- **H. Beneficiary name** — the wire reads **"To Sea Coast Logistics"**; the invoice/quote are
  from **"5 Continent Logistics LLC."** Presumed a beneficiary-bank alias — confirm so the
  audit trail ties out.

## 4. Write primitive — never write `Balance`

All three managed `Balance` tabs (AGL8/AGL13/AGL15) are **derived array formulas** that spill
from their own `Transactions` tab, e.g.:

```
Balance!A6 (Equity) = query(Transactions!$A$4:F1012, "select C, sum(D), E where F='Equity' group by C, E ...")
Balance!E6 (Asset)  = Query(query(Transactions!$A$4:G1011, "select E, sum(D) where F='Assets' group by E, F ..."))
Balance!H6 (Resource) = query(query(Transactions!$A$4:G1011, ...))
Balance!L6 (Liab.)  = ifna(query(Transactions!$A$4:F1012, ...))
```

**Writing any `Balance` cell reproduces the 2026-10-14 `#REF!` incident x3.** The only safe
primitive is to **append rows to the substrate**; the `Balance` view re-spills.

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

## 5. Dry-run entries

### 5.1 Main Ledger — Portion 1 (expense)

Append to `offchain transactions` (via `truesight-dao-report-dao-expenses`):

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| 20261014 | `[DAO EXPENSES]` 5 Continent #1026-08 air freight, AWB 047-3175-3223 — Main Ledger share (44.69% of $4,866.33 by shipped kg) | Gary Teh | -2174.80 | USD | | |

### 5.2 AGL15 — Portion 2 (source: cash -> investment)

Append to AGL15 `Transactions`:

| Date | Description | Entity | Amount | Currency | Type |
|---|---|---|---|---|---|
| 20261014 | 5 Continent #1026-08 freight — Portion 2 funded from Gary's USD | Gary Teh | -2691.53 | USD | Assets |
| 20261014 | Investment in AGL8 (freight share) | D | 717.52 | AGL8 equity holdings | Assets |
| 20261014 | Investment in AGL13 (freight share) | D | 1974.01 | AGL13 equity holdings | Assets |

Net: AGL15 assets unchanged (cash -> holdings); equity unchanged.

### 5.3 AGL8 — receive + expense

Append to AGL8 `Transactions`:

| Date | Description | Entity | Amount | Currency | Type |
|---|---|---|---|---|---|
| 20261014 | Capital injection from AGL15 (freight share) | AGL15 | 717.52 | USD | Assets |
| 20261014 | Capital injection from AGL15 (freight share) | AGL15 | 717.52 | USD | Equity |
| 20261014 | 5 Continent #1026-08 freight — AGL8 share | AGL8 | -717.52 | USD | Assets |

Net AGL8: Equity +717.52 (AGL15 now a financier); cash nets to zero.

### 5.4 AGL13 — receive + expense

Append to AGL13 `Transactions`:

| Date | Description | Entity | Amount | Currency | Type |
|---|---|---|---|---|---|
| 20261014 | Capital injection from AGL15 (freight share) | AGL15 | 1974.01 | USD | Assets |
| 20261014 | Capital injection from AGL15 (freight share) | AGL15 | 1974.01 | USD | Equity |
| 20261014 | 5 Continent #1026-08 freight — AGL13 share | AGL13 | -1974.01 | USD | Assets |

**Separate item (do NOT fold in):** AGL13 `Balance` already carries an Equity row
`AGL15 · 211.77 · USD` with **no reciprocal asset on AGL15**. Completing that half-recorded
entry is a **separate reconciliation**; book only the freight share (1974.01) in this batch.

## 6. Currency catalog additions

New asset names, each with **Price in USD = 1.0** (USD-at-par) so `/aum` rollups value them:

- `AGL8 equity holdings`  (on AGL15)
- `AGL13 equity holdings` (on AGL15)
- `Main Ledger equity holdings` — **separate, historical** item (AGL15's prior Main-Ledger
  investment); **not** part of this freight batch. **Do NOT call it "TDG holdings"** — TDG is
  a distinct live token (~2.4M circulating).

Confirmed (governor): **AGL8 already independently holds USD 564.946 as an asset** (small,
pre-existing). Post-booking its cash is 564.946 + 717.52 − 717.52 = **564.946** — the freight
net-zeroes and the pre-existing balance is untouched.

## 7. Sequencing

1. Close open items **A–F**.
2. Repair AGL15 `State` (`#REF!`) + add the `Currencies`/`State` rows.
3. Dry-run each leg -> governor review.
4. **On explicit go:** book Main Ledger -> AGL15 -> AGL8 -> AGL13.
5. Verify each `Balance` re-spill matches the expected figures.

> WARNING — **Gate:** no final ledger settlement until the governor gives an explicit go (ledger
> writes move money). Code/metadata work proceeds without it.
