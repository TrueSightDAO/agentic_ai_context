# Chocolate bar production accounting (81% bars from cacao in managed AGLs)

**Status:** CONFIRMED by Governor Gary Teh, 2026-10-27. Worked case: AGL13 / Kirsten, 40 bars.
**Canonical for:** producing finished chocolate bars at an operator's location from cacao already
sitting in a managed AGL.
**Reads with:** `LEDGER_CONVERSION_AND_REPACKAGING.md` · `brazil/FREIGHT_PROFIT_ANALYSIS_METHODOLOGY.md`
§6 (COGS) · `conventions/INTER_LEDGER_HOLDINGS.md` (cross-ledger rules).

---

## 1. The one-line rule

A bar-production run is a **REPACKAGING batch** — **not** a sale.

- Cacao on **Main** → nothing crosses a ledger. **No expense, no injection. Just repackaging.**
- Cacao in an **AGL** → the consumables must first be **capital-injected** into that AGL (§9),
  *then* repackaging consumes inputs and creates finished units.

Consumables (pouches, envelopes, QR labels/stickers) are **production inputs whose cost is COGS**.
At the bar level they are absorbed into unit cost; at the ledger level the DAO's funding of them is a
**retained claim** (§9), not a P&L expense at purchase.

---

## 2. Why this is a repackaging batch

`LEDGER_CONVERSION_AND_REPACKAGING.md` defines ledger conversion as: at a specific place/operator,
inventory **consumes input `Currency` lines and creates output units**.

`FREIGHT_PROFIT_ANALYSIS_METHODOLOGY.md`:

> §6.2 *"…Add label costs (Sticker Mule labels at $0.55 each)"*
> §6.3 *"Total COGS = Cacao Cost Basis + Packaging Materials"*

⇒ Envelopes and stickers are **packaging materials** → they flow into the **output bar's unit cost**.

---

## 3. Cost per bar (the formula)

```
cost per bar = [ Σ (input qty × input unit cost)  +  labour/overhead if allocated ] / bars produced
```

### 3.1 Input catalog lines (verified live, Main `Currencies!A1:B400`)

| Input | Currency key | Unit cost |
|---|---|---|
| Cacao nibs | `Cacao Nibs (Kilograms) Santos 20260213 - AGL13 + 047-3175-3223 - San Francisco` | $27.25 / kg |
| Envelope | `Joyberg kraft cash envelope 6.5x3.2in (per piece, Amazon 111-2611520-6121033)` | $0.0705 / pc |
| QR label / sticker | `Sticker Mule 4x2in custom rectangle label (per piece, order R384751187)` | $0.554 / pc |

> ### ⚠️ Sticker disambiguation — do not pick by name shape
>
> **Wrong** (both $0.0581, both **4×3 cm kraft**):
> `QR Code Sticker 4x3cm (Kraft Pouch) - Brazil` · `Agroverse Sticker 4x3cm (Founder Haus) - Brazil`
>
> **Right:** `Sticker Mule 4x2in custom rectangle label (per piece, order R384751187)` — $0.554.
>
> Sticker Mule is **4×2 inch** (~10×5 cm) — different product, vendor and order, **9.5× the price**.
> Booking the $0.0581 lookalike understates the expense by **$19.84 on 40 units** and permanently
> mislabels provenance (append-only ledger). **Check dimensions + vendor + order ref**, never name
> similarity. Corroborated independently by
> `brazil/FREIGHT_PROFIT_ANALYSIS_METHODOLOGY.md:137` *"Sticker Mule labels at $0.55 each"*.

### 3.2 The three candidate cost bases — and which one is live

Three bases circulate for a 50 g bar. They disagree, and **the ledger already encodes one of them**:

| Basis | Composition | Value | Status |
|---|---|---|---|
| nibs + pouch | legacy/pinned figure | $2.0379 | ❌ wrong for this product |
| **nibs + envelope + sticker** | **live `Currencies` row** | **$1.987** | ✅ **matches the catalogue to the digit** |
| nibs + pouch + envelope + sticker | over-inclusive | $2.6624 | ❌ adds a pouch that isn't used |

**The existing `Currencies` row decomposes exactly:**

```
Agroverse 81% Cacao Chocolate Bar 50g | Vivi Cacao Nibs | Kirsten 20261025 | San Francisco - AGL13
  nibs      1.3625   (50 g @ $27.25/kg)
  envelope  0.0705
  sticker   0.5540
  ─────────────────
            1.9870   ← matches the sheet to the digit
```

**Note what is absent: the pouch.** The 50 g bar goes **straight into the kraft envelope** — there is
no pouch in this SKU. A four-decimal exact match is deliberate, not coincidence: **do not contradict
a live `Currencies` row without a governor ruling.**

### 3.3 Worked example — 40 bars

| Component | Per bar | × 40 |
|---|---|---|
| Nibs (50 g @ $27.25/kg) | $1.3625 | $54.5000 |
| Envelope | $0.0705 | $2.8200 |
| Sticker | $0.554 | $22.1600 |
| **Materials subtotal** | **$1.987** | **$79.4800** |

The sticker is **7.9× the envelope** — packaging cost is dominated by the label, not the bag.

> The earlier pinned figure of **$2.038/bar** (nibs + pouch) is the **wrong basis** for this product —
it includes a pouch the SKU does not use. See §3.2.

---

## 4. Bar count is set by the SCARCEST input — not by nibs weight

```
bars = min over all inputs of ( available qty / qty consumed per bar )
```

In the worked case the binding constraint was **envelopes: 40** ⇒ **40 bars = 2.0 kg** of nibs
(40 × 50 g). A "90 bars / 4.5 kg" figure assumed nibs were the limit and would have needed
**90 envelopes**.

**Always compute the binding constraint before quoting a batch size.** Nibs weight is usually
*not* binding — packaging stock almost always is.

---

## 5. ⚠️ Labour makes or breaks a small batch

Playbook rule: add labour/overhead **only if it is a separate allocated ledger line**. But on a small
batch a *fixed* labour charge dominates everything else (at the live $1.987 basis):

| Bars | Labour ($200 fixed) per bar | Materials | **Unit cost** | vs wholesale $6 | vs retail $10 |
|---|---|---|---|---|---|
| 40 | $5.0000 | $1.9870 | **$6.9870** | **−$0.99 → LOSS** | +$3.01 |
| 90 | $2.2222 | $1.9870 | **$4.2092** | +$1.79 | +$5.79 |

⇒ At **40 bars a $200 labour charge still makes the batch loss-making at the $6 wholesale price**
(narrower than under the $2.6624 basis, but the conclusion is unchanged). Buying ~50 more envelopes
costs ≈$3.53 and repairs the unit economics.

**Before booking a batch, surface to the governor:** (a) whether the labour figure is per-batch or
per-bar, (b) what it covers, (c) the resulting unit cost vs both price points.

---

## 6. Pipeline — four units, in order

1. **Main expense** — consumables bought with Main cash.
   `truesight-dao-report-dao-expenses`, Target Ledger `offchain`.
2. **Capital injection** — consumables Main → the AGL holding the cacao (§9, **four rows**).
   **Only needed when the cacao sits in an AGL**; if the nibs are on Main, skip to step 3.
3. **REPACKAGING BATCH** — inputs consumed → a **new output `Currency`** for the finished bar with
   **col B `Price in USD` = computed cost per bar** ($1.987 at the live basis). Register it with
   `truesight-dao-define-currency` (`[CURRENCY DEFINITION EVENT]`) so it is QR-ready — see
   `agroverse/AGROVERSE_QR_CODE_BATCH_GENERATION.md` §2b.
4. **QR generation** — one QR per physical bar.
   Runbook: **`agroverse/AGROVERSE_QR_CODE_BATCH_GENERATION.md`** — note the `agroverse/` **subpath**
   (a root-level lookup 404s; this is why it was previously reported "missing").

Then **`[REPACKAGING SETTLEMENT EVENT]`** (`post_repackaging_cleanup`) once
`currency-compositions/<request_id>.json` is live.

---

## 7. Custody vs ownership — do NOT move bars to MAIN by default

An AGL ledger **already models both halves**: **Assets** row `Entity` = the **human custodian** (who
physically holds the goods); **Equity** row `Entity` = the **DAO / financier** (who owns them).

So *"DAO-owned bars in Kirsten's hands"* is **exactly** what an AGL13 row pair already expresses.
Nothing is lost by keeping them there.

**Putting the bars on MAIN loses custody fidelity.** Main is a book — not a place, not a person. A
Main asset row saying *"DAO holds 40 bars"* is silent on whether they are physically in SF with
Kirsten or elsewhere. You would have to invent a holder name to recover information the AGL row
already carried.

### 7.1 Decision rule

| Bars should live on… | When |
|---|---|
| **The AGL (default)** | The operator produced them and/or will hold or sell them. Sales booked there; Main consolidates. |
| **MAIN** | Only if the bars are **DAO-branded finished goods sold centrally** (online shop / FounderHaus) and the operator's role genuinely **ends at production**. Then do **one** transfer after the batch, **name the human physically holding them**, and **retire the §9 claim**. |

> **Non-negotiable:** whichever ledger holds the bars, the **SALES EVENT must be booked on that same
> ledger**. A sale booked elsewhere produces the *sold-but-never-landed* orphan class (see
> `OPEN_FOLLOWUPS.md`). **Never split holding from selling.**

**OPEN — awaiting governor ruling on MAIN vs AGL for DAO-branded bars.** Record the ruling here.

---

## 8. Traps

- **Consumables are COGS, not a per-bar equity markup.** The unit cost absorbs them (§3); the DAO's
  funding appears as a *ledger-level* claim (§9), never as a markup on the bar.
- **Verify a `Currencies` key against the LIVE sheet, not `agroverse-inventory/currencies.json`.**
  That snapshot's **E-section is missing entirely** (jumps `Digital Kitchen Scale` → `ETH` →
  `Foam container box`), so an E-initial name can *never* appear there. This produced a false
  "no envelope key exists" conclusion in a prior session. Read `Currencies!A1:B400` live.
- **Sticker ≠ sticker.** Check dimensions + vendor + order ref (§3.1).
- **Bar count is the scarcest input**, not the nibs weight (§4).
- **Do not add a pouch that isn't used.** The 50 g envelope SKU has no pouch (§3.2).

---

## 9. Capital injection of in-kind goods (Main → AGL) — the FOUR-row rule

**Governor ruling, Gary Teh, 2026-10-27:**

> *"Capital injection of an asset from one ledger to another needs to reduce the asset figure on the
> origin ledger while increasing the asset figure at the destination ledger as well as equity figure
> of the original ledger in the destination ledger."*
>
> *"Main is always reflected as TrueSight DAO in the AGLs."*

### 9.1 The four rows

| # | Ledger | Currency | Qty | `Entity` | Section |
|---|---|---|---|---|---|
| ① | Main (origin) | `<commodity key>` | −N | custodian | **Assets** |
| ② | Main (origin) | `<Main's claim key on AGLnn>` | +$V | custodian | **Assets** |
| ③ | AGLnn (dest) | `<commodity key>` | +N | custodian | **Assets** |
| ④ | AGLnn (dest) | `USD` | +$V | **`TrueSight DAO`** | **Equity** |

- Origin: Assets −$V +$V = **0**, Equity unchanged → **balances**.
- Destination: Assets +$V, Equity +$V → **balances**.

**The origin's second leg (②) is mandatory.** Reducing the origin's asset with no counterpart leaves
the origin unbalanced. ②+④ are the two halves of one claim.

### 9.2 `Entity` on row ④ must literally read `TrueSight DAO`

Code-verified (`tokenomics` `tdg_wix_dashboard.js`, `getTrueSightDAOEquityHoldings` ≈L451 and
`…WithIds` ≈L545): `/treasury`'s AGL-equity leg matches

```js
if (data[i][0] === "TrueSight DAO" && data[i][2] === "USD")
```

⇒ **two conditions, not one.** "Reflected as TrueSight DAO" covers the entity; the **currency must
also be exactly `USD`**.

| Row ④ `Entity` | Visible to `/treasury`? |
|---|---|
| `TrueSight DAO` | ✅ |
| `Main` · `Main Ledger` · `TrueSight DAO (Main)` · `AGL13` | ❌ invisible — the `INTER_LEDGER_HOLDINGS.md` §3 blind-spot class |

Also required by `INTER_LEDGER_HOLDINGS.md` §3.4: **Assets** rows (①②③) carry the **human
custodian**; the **Equity** row (④) carries the **financier**. **Never the same name on both legs.**

### 9.3 ⚠️ This creates an `/aum` double count — elimination required

`/aum` = Main off-chain assets **+** Σ(each AGL's asset section). Under the four-row rule:

- Main's asset total is **unchanged** (① −$V, ② +$V).
- AGL13's asset section **rises** by $V (③).
- ⇒ **`/aum` rises by $V for goods the DAO already held.** Nothing was created.

Same **double-count class as `INTER_LEDGER_HOLDINGS.md` §6-S1** (`AGL15 equity holdings`). The
superseded two-row *expense* model netted to zero and needed no elimination; the four-row *claim*
model **does**. Consolidation must **eliminate ② against ④**.

> Dichotomy to resolve: if `/aum`'s off-chain leg **excludes** claim rows there is no double count —
> but then the DAO's claim is **invisible to `/aum`** and its position understated. **Either way
> something needs fixing.** Determine which leg counts ② before trusting `/aum` after an injection.

### 9.4 Direction matrix

| Direction | Primitive |
|---|---|
| **Main → AGL** | **Capital injection**, four rows above |
| **AGL → AGL** | **Capital injection**, four rows above (② names the investee) |
| **AGL → Main** | ⚠️ **NOT a capital injection.** **Expense on the AGL** + **contribution report in Main** under the AGL's name — **and retire ② first**, up to the value returned, or the claim outlives the asset it represents and value is counted twice. |

⚠️ **Caution on the AGL→Main contribution leg:** a `[CONTRIBUTION EVENT]` runs through the **TDG
rubric**, which auto-computes issuance. A return of goods is **not labour**; booking it as a
contribution could **mint TDG for moving inventory**. Needs an explicit governor decision per case —
never submit one unprompted.

### 9.5 No repayment mechanism — state it, don't imply it

In the normal path AGL13 **sells** the bars itself, so the §9 claim is **never repaid**; AGL13's
equity ratchets up by the cost of every consumable the DAO funds. Main→AGL funding of consumables is
therefore, in substance, **permanent equity** — realised only on `/aum` consolidation, never via
repayment. Write it down, or someone will look for the payback and not find it.

### 9.6 OPEN — the claim key's name (governor's call)

Row ② needs a `Currencies` key at **`Price in USD = 1`**, whose quantity therefore stores the USD
value directly (`price = 1` ⇒ `value = quantity`).

| Option | Key | Trade-off |
|---|---|---|
| **A (recommended)** | `TrueSight DAO equity in AGL13` — **new row** | Follows the `INTER_LEDGER_HOLDINGS.md` §4 template `<investor> equity in <investee>`; one key per pair ⇒ non-colliding; honest about *who* financed |
| B | reuse legacy `AGL13 equity holdings` (already price `1`) | No new row — but AGL15's freight claim uses the same key on a different ledger, so an `/aum` reader cannot tell whose claim it is |

⚠️ **Never name a key that collides with the `/treasury` literal match.** `Currencies` is **global**
(one catalog on Main, imported by every AGL via `IMPORTRANGE`), so a collision is **structural, not
hypothetical**.

> Outstanding from `INTER_LEDGER_HOLDINGS.md` §4/§8.4: the 3 legacy keys and the `AGL15`-vs-
> `TrueSight DAO` mixed state are governor-gated migrations. **Do not normalise silently.**

### 9.7 Mechanically blocked today

`capital_injection_processing.js` (`processNewCapitalInjections`) cannot express ①–④:

```js
const assetRow  = [injectionDate, logMessage, reporterName, amount, 'USD', 'Assets'];
const equityRow = [injectionDate, logMessage, reporterName, amount, 'USD', 'Equity'];
```

- **Currency hardcoded `'USD'`** on both rows — no commodity key, no quantity.
- **`reporterName` used as `Entity` on BOTH legs** — the §3.4 violation reproduced *by construction*.
- Parsed inputs: only `ledgerName · amount · ledgerUrl · injectionDate · description
  · attachedFilename · fileLocation` — **no quantity, no asset currency, no origin ledger**.
- Amount regex `/- Amount:\s*\$?([0-9,]*\.?[0-9]+)\s*USD?/i` **hard-requires USD**.
- `getLedgerConfigsFromWix()` returns AGL destinations only (`is_managed_ledger: true`) — there is
  **no origin-side write path at all**.

⇒ A run as-is records *"AGL13 received $40 of cash"* — factually false, plus two structural breaks.
Unblock requires **asset-currency + quantity parameters**, a **`Capital Injection` sheet column** to
hold them, and a **new origin-side write**. Recommended: keep `CAPITAL INJECTION` cash-only and ship
`[MANAGED LEDGER TRANSACTION EVENT]` as the internal-transfer primitive.
