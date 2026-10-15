# Inter-ledger holdings — naming, valuation, and the equity-tracker blind spot

**Status:** PROPOSED — held for reviewer.
**§3 directional naming REVIEWED & APPROVED by Envoy (admin+envoy@truesight.me), 2026-10-15** (verified against code + live sheets).
**§1/§2/§6 RE-SCOPED 2026-10-15 after Gary Teh's (reviewer) correction: the primary gap is the literal-key equity tracker; the consolidation elimination rule was the wrong-sized fix.**
**Owner:** Sophia Truesight (admin+sophia@truesight.me). **Governor:** Gary Teh. **Filed:** 2026-10-15 (Black King freight lane).
**Related:** `plans/FREIGHT_COST_AMORTIZATION_PLAN.md` (§5.2 holdings rows, §6 `Currencies` rows); `notes/NOTES_tokenomics.md`; `tokenomics` `google_app_scripts/…/tdg_wix_dashboard.js`.

---

## 1. Two different surfaces — traced in code (correction to the first draft)

My first draft conflated `/aum` with `/treasury`'s equity leg. They are **distinct paths**:

| Surface | Computed by (`tdg_wix_dashboard.js`) | Reads | Live value (2026-10-15) |
|---|---|---|---|
| `/aum` (`?type=aum_breakdown`) | `computeAumBreakdown()` → `getManagedLedgerAssetsFromAssetSection()` | each AGL's Balance **Asset** section (cols A–B), valued by joining the asset **name** to `Currencies!A:B` | off-chain `$15,823.19` + managed ledgers `$16,256.92` = **$32,080.11** |
| `/treasury` (`?type=treasury_breakdown`) | `computeTreasuryBreakdown()` → `getInvestmentHoldingsInAGL()` → `getTrueSightDAOEquityHoldings()` | each AGL's Balance **Equity** section, **literal match `colA === "TrueSight DAO" && colC === "USD"`**, sum colB | **$1,176.42** |

- `/aum` **never touches the equity side** — it is a pure asset summation, and it is the only path that reads `Currencies`. That is why the `Currencies` rows are load-bearing for `/aum`.
- `/treasury`'s AGL-equity leg **never touches `Currencies`** — it is a literal **Entity + Currency string match** on each AGL's Balance sheet.
  Traced: `getTrueSightDAOEquityHoldings` (≈L451) and `getTrueSightDAOEquityHoldingsWithIds` (≈L545):
  `if (data[i][0] === "TrueSight DAO" && data[i][2] === "USD")`.

## 2. What an inter-ledger "holding" row is

When ledger **X** finances ledger **Y** (e.g. AGL15 advanced cash to AGL8/AGL13 to pay the
Brazil→SF freight), **X** books an **asset** row on its `Balance` **Asset** section:

| Asset (col E) | Value USD (col F) |
|---|---|
| `AGL8 equity holdings` | `145.054` |
| `AGL13 equity holdings` | `1953.30` |

This is **not a currency** — it is a **valuation key**. `/aum` values any non-USD asset by
joining the asset **name** to the `Currencies` tab (`name → Price in USD`) × quantity. A name
with **no** `Currencies` row silently values at **$0** — that is why the `Currencies` rows
(MAIN r168–r170, price `1`) are load-bearing.

> **Verified structure** (live sheets, 2026-10-15): `Currencies` is ONE **global** catalog on the
> Main Ledger; each AGL has **no local `Currencies` tab** and imports it via
> `State!A1 = IMPORTRANGE(mainLedgerId, "Currencies!A:B")` (checked AGL15). A `Currencies` name
> is therefore a **global** key — cross-ledger collisions are **structural, not hypothetical**.

## 3. THE BLIND SPOT — the real, bigger gap

`/treasury`'s equity leg keys on the **literal string** `"TrueSight DAO"`. But the DAO's freight
stakes were booked with **Financier = `"AGL15"`**, and AGL15's own Balance has **no
`"TrueSight DAO"` row at all**:

| Ledger | Balance **Equity** rows (colA Financier / colB Amount / colC Currency) | Matches `"TrueSight DAO"` + `"USD"`? |
|---|---|---|
| AGL8 | r6 `AGL15` / 145.054 / USD · r7 `Gary Teh` / 6549.25 / USD · r8 `TrueSight DAO` / 268.0568598 / USD | ✅ **only r8** (the *legacy* bit) |
| AGL13 | r6 `AGL15` / 2165.07 / USD · r7 `Gary Teh` / 1180.45 / USD | ❌ none |
| AGL15 | r6 `Annie Teo` / 10000 / **Singaporean SGD** | ❌ none (wrong entity **and** non-USD) |

Live consequence — `/treasury` AGL-equity `per_ledger` = `[AGL14 456.49, AGL8 268.056, AGL7 242.86, AGL10 193.91, AGL6 15.10, AGL2 ~0]`, total **$1,176.42**. **AGL15 and AGL13 are absent.** AGL15 *is* polled (it appears in `ledger_urls`); it simply has nothing under the literal key.

⇒ The DAO's freight stake (AGL15's advance into AGL8/AGL13) is **invisible** to the equity tracker — and there is **no concept of a "DAO-controlled vehicle"** in the tracker at all. This is a **semantic** gap, not a naming one.

## 4. Decision — directional naming (APPROVED by Envoy)

**Canonical key:** `<investor> equity in <investee>`

| Booking | Key |
|---|---|
| AGL15 → AGL8 | `AGL15 equity in AGL8` |
| AGL15 → AGL13 | `AGL15 equity in AGL13` |
| AGL15 → Main Ledger | `AGL15 equity in Main Ledger` |

- One distinct key per **(investor, investee)** pair ⇒ N investors × M targets ⇒ **N×M unique, non-colliding** keys.
- **ASCII-only** (safe as a sheet key — no arrow glyphs).
- `Price in USD` stays **`1`** (§5).
- Swap `equity` → `debt` when instruments multiply; keep the `<investor> … <investee>` shape.

**Migration of the 3 existing keys** (`AGL8 equity holdings`, `AGL13 equity holdings`,
`Main Ledger equity holdings`) is a **separate, governor-gated, live-ledger write**: rename in
**both** `Currencies` **AND** the AGL15 `Balance` asset rows atomically, **append-only** (add new
rows; deprecate the old name via a status/zero — never delete).

## 5. Decision — static price, NOT a dynamic equation in `Currencies`

Keep `Currencies!B` a **literal `1`**. Do **not** make it `=IMPORTRANGE(other_ledger, …)`.

- The **Quantity column already stores the USD value at booking**; `price = 1` is the identity
  `value = quantity`. A *dynamic* live price would **re-mark an already-marked quantity**.
- A dynamic formula makes AUM depend on a **cell address in another spreadsheet**: it breaks
  silently on a row insert, is async-blank on first open, and inverts the dependency
  (X's asset ← Y's balance sheet) — a cycle waiting to happen.
- A booked transfer is **point-in-time**; **audit stability beats live re-marking**.

If a *dynamic* derivation is ever wanted, put it in the **`Balance` view** as a computed cell —
not in the price catalog.

## 6. Re-scoped: what actually needs fixing

The consolidation **elimination rule** (my first draft's §5) is real but **secondary** — it only
bears on `/aum`'s asset summation. The **primary** issue is the equity-tracker blind spot (§3).

**Primary — the literal-key equity tracker**
`/treasury`'s equity leg has no concept of a **DAO-controlled vehicle**. Options (governor's call):
1. Book the DAO's stake in AGL15 with Financier = `"TrueSight DAO"` — smallest, but conflates an
   *external investor* with a *DAO-owned vehicle* in one string.
2. Give `/treasury` a **recognised set of DAO-controlled ledger ids** (e.g. `AGL15`) whose equity
   the DAO owns, and roll them in — a "DAO-controlled vehicle roll-up".
3. Add an explicit **`Is DAO vehicle`** flag column to the Balance sheet the tracker honours —
   most buttoned-down; keeps the entity name honest.

**Secondary**
- **(S1) Elimination on `/aum`.** AGL15's `AGLx equity holdings` **asset** (+ the `Currencies`
  rows) is summed by `/aum` *on top of* AGL13/AGL8's own assets → the financed amount is counted
  twice. Real, but downstream of the §3 decision.
- **(S2) AGL13 asset understatement.** AGL15 claims 1953.30 from AGL13, yet AGL13's `/aum` asset
  total is only 1221.88 — freight/inventory not yet on AGL13's asset side (consistent with the
  arrival gate; noted for completeness).

## 7. Open questions for the governor

1. **AGL15 roll-up:** option (1), (2), or (3)? (recommend **(3)** for auditability, **(2)** as the pragmatic minimum)
2. **`/aum` basis:** gross (current) or externally-eliminated? (recommend reporting **both**)
3. **AGL15's own Balance:** give the DAO a `"TrueSight DAO"` equity row, or normalise the `Annie Teo` row's currency?

---

*Docs-only convention. No code path changed; no ledger write made. Migration and any tracker
change are governor-gated follow-ups.*
