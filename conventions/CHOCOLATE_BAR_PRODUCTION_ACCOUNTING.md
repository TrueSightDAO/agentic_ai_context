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
cost per bar = 0.05 × P(nibs key) + P(envelope key) + P(sticker key)  [ + labour / bar ]

  where P(key) = that key's live 'Price in USD' in Currencies; 0.05 = 50 g expressed in kg
  (nibs are priced per kilogram).

  THERE IS NO SINGLE BAR PRICE (governor direction, 2026-10-27: "the right price differs
  based on the unit cost of the cacao nibs used"). Every batch derives its own from its own
  inputs. See 3.2a for the sensitivity range.
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

### 3.2a Nibs price drives the bar price — sensitivity across the live catalog

Same formula, same packaging, **five different nibs keys**:

| Nibs currency key | $/kg | nibs/bar (50 g) | + packaging | **cost/bar** |
|---|---|---|---|---|
| `Cacao Nibs (Kilograms) Santos 20260213 - AGL13` | 10.18234711 | 0.5091 | 0.6245 | **$1.1336** |
| `Cacao Nibs (KG) - Ilheus, Brazil 2024` | 24.61847089 | 1.2309 | 0.6245 | **$1.8554** |
| `Cacao Nibs (Kilograms) Santos 20260213 - AGL13 + 047-3175-3223 - San Francisco` | **27.25** | 1.3625 | 0.6245 | **$1.9870** |
| `Cacao Nibs (KG) - AGL2` | 29.9404 | 1.4970 | 0.6245 | **$2.1215** |
| `Cacao Nibs (KG) - Ilheus, Brazil 2024 + 047-3175-3223 - San Francisco` | 41.69 | 2.0845 | 0.6245 | **$2.7090** |

**Spread: $1.1336 → $2.7090 — 2.39×.** The nibs key alone moves the bar price more than everything
else combined. ⇒ **Never quote a bar price without naming the nibs key it came from.**

Packaging subtotal `0.6245` = envelope `0.0705` + sticker `0.5540`.

> **Packaging keys are location-dependent too.** The envelope is an **Amazon US** order
> (`111-2611520-6121033`); the sticker is **Sticker Mule US** (`R384751187`). A batch produced **in
> Brazil** can use neither — it needs its own Brazilian envelope and label keys, hence **another
> different price** on top of the nibs difference. When a batch moves location, re-derive **all
> three** components; never carry packaging constants across borders.

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
| 40 | $5.0000 | see 3.2a | **LOSS across the ENTIRE nibs range** ($6.1336–$7.7090) | — |
| 90 | $2.2222 | see 3.2a | **PROFIT across the entire range** ($3.3558–$4.9312) | ✅ |

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

> **✅ SUPERSEDED 2026-10-27.** Do **not** extend `capital_injection_processing.js`. The recommended
> path was taken instead: `[MANAGED LEDGER TRANSACTION EVENT]` (§11) is now the internal-transfer
> primitive, its GAS handler is **deployed** (PR #599, `457c0e4`), and it expresses ①–④ natively
> because it takes **asset + quantity + source + destination** and derives the rest.
> ⇒ **For any in-kind Main→AGL or AGL↔AGL move, use §11, not `CAPITAL INJECTION`.**
> Keep `CAPITAL INJECTION` **cash-only** external investment, as it is today. See §11.7 for the
> field-name conflict with the shipped client CLI that must be resolved before the first live run.

---

## 10. `[INTER_LEDGER CLAIM RETIREMENT EVENT]` — contract NAMED, derivation IMPLEMENTED, live write GATED

> **Status 2026-10-27:** the contract is no longer *missing* — parameters (§10.2), rows (§10.3),
> guards (§10.4) and a code stub (§10.5) all exist and are **deployed**. What remains gated is the
> **live write**: `processNewClaimRetirements()` throws `NOT_IMPLEMENTED`, and `retirement` is excluded
> from `COMMITTABLE_TRANSACTION_TYPES`. Per the governor ruling, unblock only after a **real**
> claim-retirement has been observed and the **outstanding-claim ceiling** guard is written.

> **Governor ruling, Gary Teh, 2026-10-27:** *"AGL -> Main for retired claim is a missing contract
> which we will need to implement later. ... Indicate in the code clearly that implementation will
> happen later. If this scenario occurs, we then gather enough data and do the implementation at the
> GAS."*

**Specification + placeholder only.** NOT wired into any handler. Do NOT submit this event expecting
ledger writes.

### 10.1 Why a new event, not a reused `CAPITAL INJECTION`

| | Capital injection | Claim retirement |
|---|---|---|
| Effect on claim ② | **creates** | **extinguishes** |
| Guard | total ≥ 0 | **must not exceed the outstanding balance** |
| Meaning | financing **in** | financing **unwound** |
| Partial | allowed | allowed — and is the *normal* case |

`SETTLEMENT` rejected as a name: `[REPACKAGING SETTLEMENT EVENT]` already uses it for post-batch
cleanup.

### 10.2 Parameters

| Parameter | Type | Req | Notes |
|---|---|---|---|
| `Source Ledger` | string | ✅ | ledger **holding the claim** (usually `Main Ledger`) |
| `Source Ledger URL` | url | ✅ | resolved & validated before any write |
| `Destination Ledger` | string | ✅ | ledger whose **equity is reduced** (e.g. `AGL13`) |
| `Destination Ledger URL` | url | ✅ | |
| `Claim Currency Key` | string | ✅ | must exist in `Currencies` at **price 1** |
| `Retirement Amount USD` | number | ✅ | `$V`; **must be ≤ outstanding claim** |
| `Settlement Form` | enum | ✅ | `goods` / `cash` / `write-off` |
| `Asset Currency Key` | string | if `goods` | the commodity returned |
| `Asset Quantity` | number | if `goods` | positive; direction implied by source→dest |
| `Assets Entity` | string | ✅ | **human custodian** (all Assets legs) |
| `Equity Entity` | string | ✅ | **must be `TrueSight DAO`** (§9.2) |
| `Injection Reference` | string | ⭑ | originating injection txn id — makes claim life traceable |
| `Effective Date` | date | ✅ | |
| `Description` | string | ✅ | |
| `Reference` | string | ⭑ | idempotency key |
| `Digital Signature` | string | ✅ | |

### 10.3 The four rows — exact mirror of §9.1

| # | Ledger | Currency | Qty | `Entity` | Section |
|---|---|---|---|---|---|
| ① | Source (Main) | `<claim key>` | **−$V** | custodian | **Assets** |
| ② | Source (Main) | `<asset key>` / `USD` | **+$V** | custodian | **Assets** |
| ③ | Destination (AGL) | `<asset key>` / `USD` | **−$V** | custodian | **Assets** |
| ④ | Destination (AGL) | `USD` | **−$V** | `TrueSight DAO` | **Equity** |

**`write-off` variant:** no ②/③ transfer. ① still reduces the claim; the Source books an **expense**
of `$V` instead of receiving an asset. The one case where retirement *is* a P&L event.

### 10.4 Guards

1. **Outstanding-claim ceiling** — `Retirement Amount USD ≤ Σ(claim-key assets on Source)`. Larger
   than outstanding is an **error**, never a negative asset.
2. **Both-ledger balance assertion** (§9.1 identity) before commit.
3. **`Equity Entity === 'TrueSight DAO'`** (§9.2) — else the reduction is invisible to `/treasury`
   and the claim looks extinguished while the tracker never saw it.
4. **Claim key must exist at price 1** — a mis-priced key would "reconcile" non-matching amounts.
5. **All-or-nothing** — ①②③④ together or not at all.

### 10.5 Placeholder in code — deliberately unimplemented

> **✅ LANDED 2026-10-27** in `tokenomics` →
> `google_app_scripts/1orWgdGckts55owiYOysR_y4sde52T_eUmrtDGAEkb4YV5DlUfJ0JZC5J/managed_ledger_transaction_processing.js`
> (§11.11), **deployed** (PR #599, `457c0e4`). The snippet below is the spec as drafted; the shipped
> stub is stricter — the **derivation for `retirement` is implemented and tested**, only the **live
> write** throws. Two guards are named as still unbuilt: the **outstanding-claim ceiling** and an
> **`Injection Reference`** link. `COMMITTABLE_TRANSACTION_TYPES` is the go-live switch.

```js
// ============================================================================
// [INTER_LEDGER CLAIM RETIREMENT EVENT] -- MISSING CONTRACT, NOT IMPLEMENTED
// ============================================================================
// Governed by conventions/CHOCOLATE_BAR_PRODUCTION_ACCOUNTING.md 10.
// See also conventions/INTER_LEDGER_HOLDINGS.md for the claim/holding rules.
//
// Governor ruling (Gary Teh, 2026-10-27):
//   "AGL -> Main for retired claim is a missing contract which we will need to
//    implement later. ... Indicate in the code clearly that implementation will
//    happen later. If this scenario occurs, we then gather enough data and do
//    the implementation at the GAS."
//
// DO NOT IMPLEMENT ON SPECULATION. This stub exists so the contract is NAMED and
// its shape agreed BEFORE the first real occurrence. When a genuine
// claim-retirement actually arises:
//   1. gather the real submission payload + the actual ledger rows produced,
//   2. reconcile it against 10.2 / 10.3 of the convention,
//   3. only then write processNewClaimRetirements() modelled on
//      processNewCapitalInjections() (the mirror-image handler),
//   4. add the event to Edgar's catalog and to server/dispatch.py ROUTING.
//
// Until then, submitting this event performs NO ledger writes.
// ============================================================================

/**
 * @throws {Error} always -- NOT_IMPLEMENTED by design (see block comment above).
 */
function processNewClaimRetirements() {
  throw new Error(
    'NOT_IMPLEMENTED: [INTER_LEDGER CLAIM RETIREMENT EVENT] is a named but '
    + 'deliberately unimplemented contract. See '
    + 'conventions/CHOCOLATE_BAR_PRODUCTION_ACCOUNTING.md 10.'
  );
}
```

---

## 11. `[MANAGED LEDGER TRANSACTION EVENT]` — the declarative contract

> **Governor direction, Gary Teh, 2026-10-27:** *"load the business logic we have been exploring into
> the Managed Ledger transaction event. So in the future, all I need to do is indicate to you the
> assets and their original ledger and destination ledger and you can just call this event and then
> the ledgers will automatically update."*

⇒ The **caller declares intent**; the **handler derives all rows**, prices and entities. The caller
never hand-builds a row.

### 11.1 Why this must exist

Every defect in this document is a failure to *derive* rows from intent:

| Defect | Root cause |
|---|---|
| `$40 = "AGL13 received $40 cash"` | handler hardcoded `USD` instead of reading the asset key |
| Wrong sticker at **$0.0581** vs **$0.554** | near-identical names, no dimension/vendor check |
| Origin left **unbalanced** (my first two-row model) | handler derived 2 rows for a 4-row shape |
| `Entity` identical on both legs | handler stamped `reporterName` twice |

All four are **derivation** bugs. A declarative event fixes them once, in one place, by construction.

### 11.2 Parameters — the minimal declaration

| Parameter | Type | Req | Notes |
|---|---|---|---|
| `Source Ledger` | string | ✅ | |
| `Source Ledger URL` | url | ✅ | resolved & validated |
| `Destination Ledger` | string | ✅ | |
| `Destination Ledger URL` | url | ✅ | |
| **`Assets`** | list | ✅ | one or more lines: `{ Currency Key, Quantity }` |
| `Assets Entity` | string | ✅ | **human custodian** (all Assets legs) |
| `Equity Entity` | string | ⭑ | default `TrueSight DAO` (§9.2) |
| `Transaction Type` | enum | ✅ | `injection` / `retirement` / `movement` |
| `Effective Date` | date | ✅ | |
| `Description` | string | ✅ | |
| `Reference` | string | ⭑ | idempotency |
| `Digital Signature` | string | ✅ | |

**That is it.** No amounts, no USD figures, no counterparty rows — all **derived**.

### 11.3 Derivation the handler performs

1. **Resolve** every `Currency Key` against live `Currencies!A:B`. **Unknown key ⇒ REFUSE.** Never
   silently value at **$0** — the silent-corruption mode `INTER_LEDGER_HOLDINGS.md` §2 warns of.
2. **Validate units.** kg-priced keys need a kg quantity; piece-priced keys a piece count. Reject
   mixed units on one line.
3. **Value** each line: `$V = Σ (qty × price)`.
4. **Derive `Transaction Type`** if omitted: destination is an AGL and source holds no claim ⇒
   `injection`; source holds a claim on destination ⇒ `retirement`; both AGLs under a common
   financier ⇒ `movement`.
5. **Build rows** per §9.1 (or §10.3), asserting the §9.1 identity on **both** ledgers.
6. **Echo before commit** — return resolved keys, prices, `$V` and the exact row set for confirmation.
7. **Commit atomically.**

### 11.4 The governor's example, shaped as the declaration

> *"all I need to do is indicate to you the assets and their original ledger and destination ledger"*

```
Transaction Type:  injection
Source Ledger:     Main Ledger
Destination:       AGL13
Assets Entity:     Kirsten
Assets:
  - Joyberg kraft cash envelope 6.5x3.2in (per piece, Amazon 111-2611520-6121033)  x 40
  - Sticker Mule 4x2in custom rectangle label (per piece, order R384751187)        x 40
```

Handler derives (§9.1, at live prices): `$V = (40 × 0.0705) + (40 × 0.554) = 2.82 + 22.16 = 24.98`

| # | Ledger | Currency | Qty | Entity | Section |
|---|---|---|---|---|---|
| ① | Main | the 2 keys above | −40 / −40 | Kirsten | Assets |
| ② | Main | `TrueSight DAO equity in AGL13` | +24.98 | Kirsten | Assets |
| ③ | AGL13 | the 2 keys above | +40 / +40 | Kirsten | Assets |
| ④ | AGL13 | `USD` | +24.98 | `TrueSight DAO` | Equity |

⇒ **One declaration in, four correct rows out.** No USD total supplied, no entity argued about, no
chance of the origin going unbalanced.

### 11.5 Design guards that make it safe

- **All-or-nothing.** Build + validate the full row set, *then* commit. The **2-of-4 partial write**
  is precisely the failure this event exists to eliminate — a crash between legs must not be
  representable.
- **Refuse on unknown key** (§11.3.1). A `$0` valuation is worse than a failure.
- **Echo resolved keys, prices and rows before commit.** A bare *"40 stickers"* genuinely cannot
  distinguish **$0.0581** from **$0.554** — the caller must see which key resolved before money moves.
- **Never hand-build rows.** If an operator needs rows this event cannot derive, that is a **new
  `Transaction Type`** — not a manual append.

### 11.6 Status — GAS handler DEPLOYED 2026-10-27; two blockers before a live run

> **✅ SHIPPED 2026-10-27.** `tokenomics` PR **#599** (merged `457c0e4`), deployed to Apps Script
> project `1orWgdGckts55owiYOysR_y4sde52T_eUmrtDGAEkb4YV5DlUfJ0JZC5J` at 09:11:48 (deploy ledger
> `deploy_20261027T091245Z_1orwgdgckts55owiyoysr-y4sde52t-eumrtdgae`).
> File: **`managed_ledger_transaction_processing.js`** (644 lines), added alongside
> `capital_injection_processing.js` — which is **untouched and still live**.

The derivation engine exists and is unit-tested. It is **not yet reachable end-to-end**. Two
concrete blockers, both outside the code that shipped:

| # | Blocker | Consequence | Fix |
|---|---|---|---|
| **B1** | The **`Managed Ledger Transactions`** tab does **not exist** in the Telegram Logs spreadsheet (`1qbZZhf-…`) | `processNewManagedLedgerTransactions()` returns immediately at *"sheet not found"*. Nothing routes. | create the tab with the **17 columns** in §11.8 |
| **B2** | The event is absent from Edgar's catalog and `dispatch.py` `ROUTING` | no event is ever delivered, so nothing is queued as `NEW` | the existing `OPEN_FOLLOWUPS.md` server-half entry |

⚠️ **B1 is the one that bites.** A run today returns silently and looks idle rather than broken —
the exact fail-silent class §8 warns about. Create the tab **before** submitting anything.

### 11.7 ⚠️ Field-name conflict with the SHIPPED client CLI — resolve before submittal

**This is the single most important thing for a future LLM reading this document to understand.**

Two incompatible designs are now published under the **same event name**:

| | **Shipped client CLI** (`dao_protocol` #187, 2026-10-15) | **This contract + the deployed GAS** |
|---|---|---|
| Philosophy | caller **supplies the amount/rows** | caller **declares intent; handler derives everything** |
| `Amount` | ✅ **required** (`positive_number`) | ❌ **forbidden** — derived from live `Currencies` |
| `Currency` | ✅ single field | ❌ replaced by a repeatable `Asset:` list |
| `Sender` / `Recipient` | ✅ required | ❌ `Assets Entity` / `Equity Entity` |
| `Ledger` / `Ledger URL` | ✅ **one** ledger | ✅ **`Source` + `Destination`** (two) |
| `Transaction Type` | ❌ absent | ✅ `injection` / `movement` / `retirement` |

⇒ **A submission built by the shipped CLI will be rejected by the deployed handler** (no source
ledger, no asset quantities, no transaction type) — and a declaration built per this section will be
rejected by the CLI's own validators (no `Amount`, no `Sender`/`Recipient`).

**Resolution required — a governor call, not an autonomous one.** Three options:

- **(a) Align the CLI to this contract** *(recommended)* — the client sends the declaration, the
  handler derives. Preserves the whole point of §11.1: no hand-built rows, no `$0` silent
  valuation, no unbalanced origin. Cost: rewrite `report_managed_ledger_transaction.py`'s labels.
- **(b) Keep the CLI's legacy blob and add a second event name** for the declarative path.
  Cost: two vehicles for one job — exactly the confusion this document exists to prevent.
- **(c) Treat the CLI as dead** and drive the sheet directly. Cost: loses the signed submission
  and the Edgar hash, i.e. the audit trail.

**Do NOT silently implement one side.** Whichever is chosen, update this table and the catalog entry
in the same PR.

### 11.8 The `Managed Ledger Transactions` tab — exact 17-column shape (blocker B1)

Lives in the **Telegram Logs** spreadsheet (`1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`), as a new
tab named **`Managed Ledger Transactions`**. Columns A–Q, header in row 1. `Status` values the code
writes: `NEW` → `PROCESSED` / `FAILED` / `BLOCKED`.

| Col | Field | Notes |
|---|---|---|
| A | Telegram Update ID | dedupe key |
| B | Telegram Message ID | dedupe key |
| C | Log Message | full signed message |
| D | Reporter | who submitted |
| E | Source Ledger | name, e.g. `Main Ledger` |
| F | Source Ledger URL | must resolve to a real spreadsheet |
| G | Destination Ledger | e.g. `AGL13` |
| H | Destination Ledger URL | |
| I | Transaction Type | `injection` / `movement` / `retirement` |
| J | **Assets** | **JSON**: `[{"currency":"<exact Currencies key>","quantity":40}]` |
| K | Assets Entity | **human custodian** (never `TrueSight DAO`) |
| L | Equity Entity | **must be exactly `TrueSight DAO`** |
| M | Value USD | written by the handler on success — leave blank |
| N | Effective Date | |
| O | Description | |
| P | Status | `NEW` to queue — set by the writer, never by hand |
| Q | Ledger Lines | written by the handler, e.g. `source:Main Ledger=1234-1236; …` |

### 11.9 What a future Sophia must do — operating procedure

1. **Never hand-edit a `Transactions` tab** for an inter-ledger move. That is how all four defects
   in §11.1 arose.
2. **Ask the governor only for assets + source + destination** (§11.4). Do not ask for a USD total
   — it is derived, and supplying it re-introduces the drift this event removes.
3. **Resolve every `Currency Key` against the LIVE `Currencies` tab**, never
   `agroverse-inventory/currencies.json` (its E-section is missing, §3.1).
4. **Run `testDeriveTransactionRows()` in the GAS editor** after any edit to the handler. It asserts
   the 4-row shape, both-ledger balance, and all six guards, with **no side effects**.
5. **Read the echo before the commit.** The handler logs every resolved key, its price, `$V` and the
   full row set. A bare *"40 stickers"* cannot distinguish **$0.0581** from **$0.554** — 9.5×
   apart. If the echoed price is not the one you expect, stop.
6. **Retirement is GATED.** `processNewClaimRetirements()` **throws `NOT_IMPLEMENTED`** by design.
   `COMMITTABLE_TRANSACTION_TYPES` is the single go-live switch — flipping that array is the entire
   change, and it needs a governor go-ahead plus the outstanding-claim ceiling guard (§10).

### 11.10 Two bugs the balance guard caught during development — keep the guard

Recorded because the guard is what makes this safe, and because both bugs would have shipped silently:

1. **Mixed units.** The first draft of `assertLedgerBalances_` summed **raw amounts**. An injection's
   origin legitimately holds `−40 envelopes` *and* `+24.98 USD` in the **same** Assets section;
   raw summation gave **−55.02**, which is meaningless — 40 envelopes are not 40 dollars. Fixed by
   **valuing every row in USD** via the price table before asserting.
2. **Float accumulation.** `40 × 0.0705 + 40 × 0.554` produced `24.980000000000004`. Now rounded
   **once to 6 dp** before the value reaches a ledger row.

⇒ **The guard caught both BEFORE any row was written** — and neither was caught by review. Any
future change to the derivation must keep the both-ledger assertion and must run the harness.

### 11.11 Handler API (as deployed)

| Function | Purpose |
|---|---|
| `loadCurrencyPrices_()` | reads live `Currencies!A:B` from the Main ledger |
| `resolvePrice_(key, table)` | fails closed on unknown key — **never** `$0` |
| `deriveTransactionRows_(decl, table)` | **pure**; declaration + prices → rows for both ledgers |
| `assertLedgerBalances_(d, table)` | Σ Assets ≡ Σ Equity **in USD, per ledger** |
| `appendRowsAtomically_(writes)` | append both legs; **delete applied rows in reverse** on failure |
| `parseManagedLedgerTransactionMessage(msg)` | parses the §11.4 declaration |
| `processNewManagedLedgerTransactions()` | the commit loop; `NEW` → `PROCESSED`/`FAILED`/`BLOCKED` |
| `processNewClaimRetirements()` | **throws `NOT_IMPLEMENTED`** (§10) |
| `testDeriveTransactionRows()` | self-test, **no side effects** |
