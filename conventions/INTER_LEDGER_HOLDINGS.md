# Inter-ledger holdings — naming, valuation, and consolidation elimination

**Status:** PROPOSED — held for reviewer. **§3 directional naming REVIEWED & APPROVED by Envoy (admin+envoy@truesight.me), 2026-10-15** — verified against the actual code + live sheets, not the proposal text. **Owner:** Sophia Truesight (admin+sophia@truesight.me). **Governor:** Gary Teh.
**Filed:** 2026-10-15 (Black King freight lane).
**Related:** `plans/FREIGHT_COST_AMORTIZATION_PLAN.md` (§5.2 holdings rows, §6 `Currencies` rows); `notes/NOTES_tokenomics.md`; `tokenomics` `google_app_scripts/…/web_app.js` (`getInvestmentHoldingsInAGL`, `getTrueSightDAOEquityHoldings`).

---

## 1. What an inter-ledger "holding" row is

When ledger **X** finances ledger **Y** (e.g. AGL15 advanced cash to AGL8/AGL13 to pay the
Brazil→SF freight), **X** books an **asset** row on its `Balance` **Asset** section:

| Asset (col E) | Value USD (col F) |
|---|---|
| `AGL8 equity holdings` | `145.054` |
| `AGL13 equity holdings` | `1953.30` |

This is **not a currency**. It is a **valuation key**. AUM values *any* non-USD asset by
joining the asset **name** to the `Currencies` tab (`name → Price in USD`) and multiplying by
quantity. A name with **no** `Currencies` row silently values at **$0** — that is why the
`Currencies` rows (MAIN r168–r170, price `1`) are load-bearing, and why they are added in the
same booking rather than left implicit.

> **Verified mechanism** (`tokenomics/…/web_app.js`):
> `/aum = getOffChainAssetValue() + getUSDTBalanceInVault() + getInvestmentHoldingsInAGL()`.
> The off-chain leg values named holdings through the `Currencies` join; the investment-holdings
> leg is a *separate* path (`Balance` rows with `Entity='TrueSight DAO' & Currency='USD'`).
>
> **Verified structure** (live sheets, 2026-10-15): `Currencies` is ONE **global** catalog on the
> Main Ledger; each AGL has **no local `Currencies` tab** and imports it via
> `State!A1 = IMPORTRANGE(mainLedgerId, "Currencies!A:B")` (checked AGL15). So a `Currencies`
> name is a **global** key — cross-ledger collisions are **structural, not hypothetical**.

## 2. The two problems this convention fixes

**(a) Ambiguity.** `AGL8 equity holdings` does not say *who* holds it. The moment a second
ledger also holds AGL8 equity, one name collides → both collapse onto one price and one AUM
line → the quantity is wrong and unattributable.

**(b) Double count on consolidation.** AUM sums assets across ledgers. Investor **X**'s holding
in **Y**, and **Y**'s own (freight-inclusive) inventory, are downstream of the **same dollars**.
Naive summation counts the financed amount **twice**.

## 3. Decision — directional naming

**Canonical key:** `<investor> equity in <investee>`

| Booking | Key |
|---|---|
| AGL15 → AGL8 | `AGL15 equity in AGL8` |
| AGL15 → AGL13 | `AGL15 equity in AGL13` |
| AGL15 → Main Ledger | `AGL15 equity in Main Ledger` |

- One distinct key per **(investor, investee)** pair ⇒ N investors × M targets ⇒ **N×M unique,
  non-colliding** keys.
- **ASCII-only** (safe as a sheet key — no arrow glyphs).
- `Price in USD` stays **`1`** (see §4).
- Swap `equity` → `debt` (etc.) when instruments multiply; keep the `<investor> … <investee>`
  shape.

**Migration of the 3 existing keys** (`AGL8 equity holdings`, `AGL13 equity holdings`,
`Main Ledger equity holdings`) is a **separate, governor-gated, live-ledger write**: rename in
**both** `Currencies` **AND** the AGL15 `Balance` asset rows atomically, **append-only**
(add new rows; deprecate the old name via a status/zero, never delete).

## 4. Decision — static price, NOT a dynamic equation in `Currencies`

Keep `Currencies!B` a **literal `1`**. Do **not** make it `=IMPORTRANGE(other_ledger, …)`.

Rationale:
- The **Quantity column already stores the USD value at booking**; `price = 1` is the identity
  `value = quantity`. A *dynamic* live price would **re-mark an already-marked quantity** —
  double-applying.
- A dynamic formula makes AUM depend on a **cell address in another spreadsheet**: it breaks
  silently on a row insert, is async-blank on first open, and inverts the dependency
  (X's asset ← Y's balance sheet) — a cycle waiting to happen.
- A booked transfer is a **point-in-time** event; **audit stability beats live re-marking**.
  Mark-to-market, if ever wanted, is a separate deliberate decision.

If a *dynamic* derivation is ever wanted, put it in the **`Balance` view** as a computed cell —
**not** in the price catalog.

## 5. Decision — consolidation elimination rule

On any consolidation that sums assets across ledgers, **eliminate the investor's inter-ledger
holding against the investee's corresponding internal equity**, so the financed amount is
counted **once**.

- **External-network view:** inter-ledger holdings net to **zero**; only claims on *external*
  assets count toward headline AUM.
- **Rule:** for each (investor X, investee Y) pair, subtract `min(X's holding in Y, Y's internal
  equity attributable to X)` **once**.

> Today `/aum`'s asset summation counts AGL13's freight-inclusive inventory **and** AGL15's
> claim on AGL13 — the **same dollar twice**. The elimination rule removes that.

## 6. Open question for the governor (recommend reporting BOTH)

Does the DAO want **AUM = external-network (eliminated)** or **AUM = gross sum (no
elimination)**? **Recommendation:** report a headline **`AUM (external)`** plus a memo line
**`inter-ledger gross-up`**, so the number is honest under either reading and the difference is
visible rather than buried.

---

*Docs-only convention. No code path changed; no ledger write made. Migration and any
elimination implementation are governor-gated follow-ups.*
