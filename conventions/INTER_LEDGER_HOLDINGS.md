# Inter-ledger holdings — naming, valuation, and the equity-tracker blind spot

**Status:** PROPOSED — held for reviewer. **§8 records a governor ruling (2026-10-27) — read it before booking any DAO-owned consumable into an AGL.**
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

1. **AGL15 roll-up:** option (1), (2), or (3)? (recommend **(3)** for auditability, **(2)** as the pragmatic minimum) — **PARTIALLY ANSWERED for consumables: see §8.**
2. **`/aum` basis:** gross (current) or externally-eliminated? (recommend reporting **both**)
3. **AGL15's own Balance:** give the DAO a `"TrueSight DAO"` equity row, or normalise the `Annie Teo` row's currency?

---

## 8. GOVERNOR RULING (2026-10-27) — DAO-owned consumables: financier = `"TrueSight DAO"`

**Governor:** Gary Teh. **Recorded by:** Sophia Truesight (autopilot). **Status:** RULED —
not yet booked (see §8.3 blockers).

### 8.1 The ruling

When a **DAO-owned consumable/material** (envelopes, stickers, packaging, labels) is
**expensed on the Main Ledger** and the physical stock is **transferred into an AGL** for that
ledger's use, the **financier on the AGL's Equity leg is `"TrueSight DAO"`** —
**not `"Main Ledger"`**, and **not** the sourcing ledger.

Worked case: **40 envelopes + stickers, Main → AGL13.**

### 8.2 The three legs (and where each is actually written)

Per `plans/FREIGHT_COST_AMORTIZATION_PLAN.md` §4 — **`Balance` is a derived `query()` view;
writes go to the `Transactions` substrate only.** Writing any `Balance` cell reproduces the
2026-10-14 `#REF!` incident.

| Leg | Substrate tab | Row shape | Primitive |
|---|---|---|---|
| ① **Expensed on Main** | Main `offchain transactions` (cols A–G) | negative amount at cost | `truesight-dao-report-dao-expenses` (Target Ledger = `offchain`) |
| ② **Asset debited on AGL13** | AGL13 `Transactions` (cols A–F) | `+qty` / `+value`, `Transaction Type` = `Assets` | `truesight-dao-report-capital-injection` |
| ③ **Equity credited on AGL13** | AGL13 `Transactions` (cols A–F) | `+value`, `Entity` = `TrueSight DAO`, `Transaction Type` = `Equity` | **same event as ②** — the handler appends **both rows** |

> **Legs ② and ③ are ONE event, not two bookings.** `capital_injection_processing.js`
> appends exactly two rows (`+amount USD / Assets`, then `+amount USD / Equity`) and stamps
> `PROCESSED`, idempotent on Telegram update/message ID.
>
> ⚠️ **Do not hand-write either row.** A hand-rolled append is how the AGL14 QR-side / GL-side
> mismatch arose (`OPEN_FOLLOWUPS.md`); the CLI keeps `investor.Asset == investee.Equity`
> (§3.5 of `LEDGER_CONVERSION_AND_REPACKAGING.md`) true by construction.
>
> ⚠️ **Entity labeling (§3.4): never the same name on both legs.** The `Equity` row's
> `Entity` = the **financier** (`TrueSight DAO`); the `Assets` row's `Entity` = the **human
> custodian**. This ruling fixes the *former* only.

### 8.3 Why `"TrueSight DAO"` is the right string here — and what it buys

`/treasury`'s AGL-equity leg keys on the **literal** `colA === "TrueSight DAO" && colC === "USD"`
(§1, §3). Booking with this exact string makes the stake **visible** to the equity tracker.
Contrast the §3 blind spot: the AGL15 freight stakes booked as `"AGL15"` remain **invisible**.

**Effect on the two surfaces:**

- **`/aum`** — unchanged in aggregate. Main's off-chain treasury drops by the cost (leg ①);
  AGL13's asset section rises by the same amount (leg ②). The two legs **net to zero**, so no
  double count is introduced (unlike the §6-S1 `AGL15 equity holdings` case).
- **`/treasury`** — the DAO's stake in AGL13 **becomes visible** where it previously would not.
  This is the intended benefit of the ruling.

⚠️ **Still required:** the `Assets` row's `Currency` (the envelope/sticker name) **must** have a
`Currencies` row with a real `Price in USD`, or `/aum` silently values it at **$0** (§2).
**As of this ruling no envelope line exists in `Currencies`** — the catalog has
`QR Code Sticker 4x3cm (Kraft Pouch) - Brazil` at **$0.0581/pc**, but no confirmed **envelope**
key. **That `Currencies` row is a hard precondition for booking.**

### 8.4 Unresolved — the mixed-key state (governor's call, do NOT silently normalize)

This ruling makes the key depend on **what kind of thing** moved:

| Transfer | Financier key | Visible to `/treasury`? |
|---|---|---|
| AGL15 → AGL8/AGL13 (freight) | `AGL15` — freight plan §3-D ruling | ❌ no |
| Main → AGL13 (consumables) | **`TrueSight DAO`** — this ruling | ✅ yes |

Both are governor rulings; they were made about different transactions and are **not**
necessarily inconsistent — but the resulting books carry **two conventions**, and only one of
them is tracker-visible.

**Open for the governor:** re-key the AGL15 freight stakes to `"TrueSight DAO"` too (a
**governor-gated, append-only** migration per §4 — add new rows, deprecate the old name via a
status/zero, never delete), or preserve the distinction and instead pursue §7 Q1 **option (3)**
(an explicit `Is DAO vehicle` flag the tracker honours)? **Recommendation: (3)** — it keeps the
entity name honest *and* removes the invisible-key class, instead of overloading one string
with two meanings.

> Per §3 named-template: `<investor> equity in <investee>`. This ruling uses the **legacy
> bare form** `TrueSight DAO` because the tracker's literal match requires it. A future
> tracker change to `TrueSight DAO equity in AGL13` would need the tracker updated **first**.

---

*Docs-only convention. No code path changed; no ledger write made. Migration and any tracker
change are governor-gated follow-ups.*
