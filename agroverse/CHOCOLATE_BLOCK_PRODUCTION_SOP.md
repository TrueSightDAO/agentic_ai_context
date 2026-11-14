# Chocolate Block Production & Ledger Booking — SOP

**Scope:** producing a bulk tempered cacao block (e.g. 2.5 kg) and booking it correctly in the DAO ledger.
**Status:** v1.2 (amended 2026-11-14). v1.1 recorded the governor ruling; **v1.2 reconciles the document with the live ledger** — §5 currency naming and registry location, §6 sugar-price caveat, §7 append/row-placement guard, and the §4 MAIN mirror `Section` rule. Every figure below is sourced from the live ledger, except where explicitly flagged as provisional.
**Search terms:** chocolate block, slab, 2.5kg, bulk block, melanger, tempering, formulation, yield, sugar, block currency, interim inventory.

> ### Ruling (governor, 2026-11-14): blocks are interim inventory
>
> **"Blocks are interim inventory which Kirsten creates. These are not for sale."**
>
> A block is a **production-stage asset**, never a product. Consequences, which run through this whole document:
>
> - **No QR codes. No serialization. Not a sale unit.**
> - **`Sale Type = Bulk`** — classified like nibs and butter, not like bars.
> - A block leaves inventory only via a later **conversion** (cut into 50 g bars) or a bulk disposal on explicit governor instruction. Never via a retail sale.
> - The `%` in the block's name is an **internal label**, not a consumer claim. The bars cut from it *are* sold, so *their* label must follow the block's actual composition.

> **Why this document exists.** Block #1 was booked across 9 ledger rows and took three rounds of correction. The sugar quantity had to be *back-solved* because nobody recorded what was actually put in. This SOP exists so the next block is booked once, correctly, with the physical numbers captured rather than derived.

---

## 1. Block vs bar — do not conflate

| | Bar | Block |
|---|---|---|
| Unit | 50 g, retail-finished | 2.5 kg bulk, post-production |
| Packaging | Joyberg kraft envelope + Sticker Mule label | none / wrap |
| QR codes | **Yes** — batch-generated per bar | **None** — interim inventory, never serialized |
| Sale Type | `Retail Ready` | **`Bulk`** |
| Purpose | sale unit | **production-stage asset**; consumed by a later conversion |
| Currency example | `... Chocolate Bar 50g \| Vivi Cacao Nibs \| Kirsten 20261025 \| San Francisco - AGL13` | `... Chocolate Block (Kilograms) #1 \| Vivi Cacao Nibs \| Kirsten 20261114 \| San Francisco - AGL13` |

A block and a bar batch consume the **same inputs** but are **different currencies** with different unit costs. Booking a block as bars (or vice versa) breaks the conversion chain.

---

## 2. The formulation model

Craft chocolate has exactly two components:

```
cacao mass = cacao nibs + added cacao butter
finished weight = cacao mass + sugar
% cacao = (nibs + butter) / finished weight
```

Inverting, for a target weight and target %:

```
sugar   = finished_weight - nibs - butter
nibs    = finished_weight * (pct / 100) - butter
```

The `81%` figure refers to **cacao mass as a share of finished weight**, not to nib purity. Butter counts as cacao; sugar does not.

### Reference formulations (Vivi / Jesus do Deus, Bahia)

| Target | Nibs | Butter | Sugar | Finished | % cacao |
|---|---|---|---|---|---|
| 50 g bars, 40 units (AGL13 r42/r43) | 2.00 kg | 0.10 kg | *not booked* | 2.00 kg | **105% — impossible** (see §8) |
| Block #1 2.5 kg (AGL13 r59–r67) | 2.00 kg | 0.10 kg | 0.40 kg | 2.50 kg | **84%** (labelled 81%) |
| Block 2.5 kg at true 81%, zero loss | 1.925 kg | 0.10 kg | 0.475 kg | 2.50 kg | 81% |
| Block 2.5 kg at true 81%, ~5% loss | 1.93 kg | 0.10 kg | 0.475 kg | ~2.38 kg | ~81% |

**Butter is an ingredient, not a processing aid.** It is consumed into the block and must be booked as a consumption leg, not left as a rounding adjustment. 0.1 kg per batch is the established convention (one per bar batch per the 20261114 governor ruling).

---

## 3. Physical production steps

> ⚠️ **Capture gap.** The ledger records inputs, output and yield but **no process parameters**. Steps 1–4 are standard craft practice; the parameters in brackets are *what must be recorded* going forward, not what was recorded for Block #1.

1. **Nib preparation** — AGL13 uses pre-roasted, pre-winnowed Santos/Vivi nibs. No roasting in SF.
   *Capture: origin, arrival lot, moisture.*
2. **Refine / conche** — nibs + cacao butter into the melanger, run until particle size is below tongue threshold (typically 24–72 h). Sugar is added partway through, not at the start.
   *Capture: melanger load (kg), duration (h), start/end time, machine ID.*
3. **Temper** — melt to ~45 °C, cool to ~27 °C to form stable beta crystals, bring to working temp ~31–32 °C.
   *Capture: tempering curve actually used, working temp at moulding.*
4. **Mould / cold-hold** — pour into block mould, de-mould, hold ~12–18 °C.
   *Capture: mould ID, cold-hold temp and duration, final piece count and weighed output.*
5. **Weigh and record the finished weight.** This is the single most important number in the whole process — it is the only thing that closes the mass balance. **Weigh it; do not assume it equals the sum of inputs.**
6. **Wrap / label** and hand over to the manager's custody.

---

## 4. Ledger booking — the 6-leg sequence

This is where blocks go wrong. AGL13 Block #1 needed a reversal (r64) because sugar was booked straight into AGL13 instead of being received into MAIN first.

**Rule: inputs are received into MAIN, then injected into the location `in kind`, then consumed. Never book an input directly into the consuming location.**

| # | Leg | Ledger | Sign | Amount | Notes |
|---|---|---|---|---|---|
| 1 | Nibs consumption | consuming loc | − | 2.0 kg | must reference the receipt lot |
| 2 | Butter consumption | consuming loc | − | 0.1 kg | |
| 3 | Input asset receipt (in kind) | **MAIN** | + | 0.4 kg | contributor-valued |
| 4a | Injection out of MAIN | **MAIN** | − | 0.4 kg | |
| 4b | Injection into location | consuming loc | + | 0.4 kg | |
| 5 | Equity increase (in kind) | consuming loc | + | **USD** | = value of contributed input |
| 6 | Block asset created | consuming loc | + | 2.5 kg | new currency |

Also required on MAIN: an **equity holdings** leg mirroring leg 5 (`AGL13 equity holdings`) so the injection nets correctly at both ends.

**Which `Section` does that MAIN mirror row take? `Assets` — not `Equity`.** The instrument is *named* "…equity holdings" but on MAIN it is an **asset-side** row. Confirmed 2026-11-14: MAIN r6047 and r6058 were booked `Assets`; r6066 was wrongly booked `Equity` and was corrected to `Assets`.

Reason: per the §9.1 identity the **origin ledger stays flat** — `Assets −$V +$V = 0`, **Equity unchanged**. An `Equity` row on MAIN therefore double-counts the contribution.

Do not conflate the two sides:

| Row | Ledger | Section |
|---|---|---|
| Leg 5 — equity increase (in kind) | **consuming location** | `Equity` |
| Netting pair (`offchain asset location` + `AGL13 equity holdings`) | **MAIN** | `Assets` |

### Booking order that avoids corrections

1. Receive ALL inputs into MAIN (assets + equity for any in-kind contribution).
2. Inject each input MAIN → location (two legs: −MAIN, +location).
3. Book consumption legs at the location.
4. Book the finished block as a new asset.
5. Verify `Balance` reflects every leg (see §7).

> **Do not book an input directly into the consuming location.** If you already did, reverse it (as r64 did) rather than editing history — the reversal is the audit trail.

### Mandatory description fields

Every production row must carry, in its description:
- Quantity in **kg** to at least 2 dp.
- The **recipe** — nibs / butter / sugar, so the % cacao is recoverable.
- The **batch identifier** linking to the block currency.
- Evidence link (photo/weight slip) archived to `TrueSightDAO/.github`.
- If any figure was derived rather than weighed, **say so explicitly**. Block #1's sugar row did this correctly ("Sugar qty derived by mass balance").

---

## 5. Currency registration (`Currencies`)

A block needs its own row in `Currencies`. Naming convention:

```
Agroverse <pct>% Cacao Chocolate Block (Kilograms) #<n> | <nib origin> | <maker> <YYYYMMDD> | <location>
```

**`(Kilograms)` is literal and required.** It states the unit that `Price in USD` is quoted in. Without it a reader must guess whether `24.160143536` is the cost of *one kilogram* or of *one whole 2.5 kg block* — a **2.5× error** on every deduction and on the price of every bar later cut from it. (Renamed from the older `<weight>kg` form, e.g. `2.5kg`, on 2026-11-14; the ledger was renamed but this document was not.)

**Do not put the weight in the name.** It is already carried as a number in `Unit Weight (grams)` (col 10). Duplicating it in the name invites the two drifting apart, and a block is a **per-kg asset**: `Amount` is in kilograms, and `Amount × Price in USD = total USD`.

### 5.1 `Price in USD` is the cost of one *unit of account* — and `Unit Weight` declares that unit

Two fields together define what one "unit" is. They **must** agree, and checking only one of them is how a 2.5× error slips through:

| Field | Means |
|---|---|
| `Price in USD` (col 1) | cost of **ONE** unit |
| `Unit Weight (grams)` (col 10) | mass of **ONE** unit, in grams |
| `Amount` (ledger) | **number of units** |

Cross-checked against the live `Currencies` catalog:

| Currency | `Unit Weight` | `Price in USD` | One unit is | `Amount` booked |
|---|---|---|---|---|
| 81% bar (r26/r28) | `50` | 2.709 | one 50 g bar | 40 bars |
| Cacao Nibs Santos + SF (r83) | `1000` | 27.25 | one kilogram | 95.5 kg |
| Cacao Tea (r90) | `1000` | 10.18234711 | one kilogram | 21 kg |
| **Block #1 (r180)** | **`1000`** | **24.160143536** | **one kilogram** | **2.5 kg** |

The rule that ties them together: **for a per-kg commodity, `Unit Weight = 1000` and `Amount` is in kilograms.** `Amount × Price in USD = total USD` then holds on every row above.

**Why the block is `1000`, not `2500`.** The block is a **per-kg asset** — its `Amount` is 2.5 *kilograms*, not 1 block. Setting `Unit Weight = 2500` while `Amount = 2.5` **mixes units**: it declares "one unit weighs 2.5 kg" and then books 2.5 of those units — **6.25 kg of asset for a 2.5 kg block**. `2500` is correct only if the whole block is sold as one indivisible SKU priced `$60.40035884`, which is neither how it is booked nor how it will be consumed by a later conversion.

> **Corrected 2026-11-14 (governor instruction, Gary).** Block #1 `Unit Weight (grams)` changed **`2500` → `1000`**, and the currency was renamed from the old `<weight>kg` form to `(Kilograms)`. **No quantity or value changed** — `Balance` still reads 2.5 / 2.5 and `$60.40035884`; `2.5 × 24.160143536 = 60.40035884` exactly. The earlier "`2500` ✅" in this document was tracking the **physical size** of the block rather than the **unit of account** — the exact conflation this section now exists to prevent.

> ⚠️ **Live consumer — do not give a per-kg currency a retail SKU.** `go_to_market/scripts/check_retail_margins.py` reads `Currencies` col B as the **per-unit cost** and compares it directly to a SKU's retail price **without** multiplying by `Unit Weight`. That is correct for 50 g bars (col B already *is* the bar cost), but a per-kg currency attached to a whole-block SKU would understate cost **2.5×** and let a sub-cost price pass the margin guard silently. Blocks are `Sale Type = Bulk` and so are skipped today; if a bulk currency ever gains a retail SKU, divide by the unit mass first.

### 5.2 Never write into a derived tab's spill range

`Balance` is **entirely derived** in every managed location ledger (AGL8 / AGL13 / AGL15): `A6`, `E6`, `H6` and `L6` are `QUERY()` array formulas that spill down the whole tab, and each location's `State!A1` is an `IMPORTRANGE("1GE7PUq-…", "Currencies!A:B")` spill. MAIN's `offchain asset location` behaves the same way (`sops/REPACKAGING_SETTLEMENT_SOP.md`).

A **literal write into any cell inside a spill range blocks the formula** and cascades. On 2026-11-14, a literal placed in AGL13 `Balance!E7` and `!J7` produced `#REF!` at row 6 and blanked `E:J` on rows 7–10 — including a real bar balance — and a literal at `State!A180` turned `State!A1` itself into `#REF!`.

**Pre-write guard — the check that is NOT sufficient.** Asking *"does any formula reference this currency name?"* is **not** a guard: it returned `0` before that write, the write was judged safe, and it still broke the sheet.

1. Read the target tab in **FORMULA** view — `get_all_values(value_render_option="FORMULA")`.
2. Find every array formula (`QUERY`, `IMPORTRANGE`, `FILTER`, `SORT`, `UNIQUE`, `ARRAYFORMULA`) and treat **every cell below and to the right of it** as spill-owned.
3. Change the **substrate** (`Transactions`, or MAIN `Currencies`) — never the derived view. Derived tabs repair themselves; hand-written cells do not.
4. If a literal already landed, `batch_clear` the cell and let the formula re-spill, then re-read and confirm **zero** `#REF!` / `#NAME?` remain across the tab.

### Required fields (col index)

| Col | Field | Block #1 value | Status |
|---|---|---|---|
| 0 | Currencies (name) | `...Chocolate Block (Kilograms) #1 \| Vivi Cacao Nibs \| Kirsten 20261114 \| San Francisco - AGL13` | ✅ |
| 1 | Price in USD | `24.160143536` | ✅ per-kg |
| 2 | Serializable | `TRUE` | ⚠️ leftover — see §9 |
| 4 | landing_page | `https://agroverse.shop/shipments/agl13/index.html` | ✅ |
| 5 | ledger | MAIN spreadsheet URL | ✅ |
| 6/7/8 | farm / state / country | Jesus do Deus / Bahia / Brazil | ✅ |
| 9 | Year | — | ❌ missing |
| 10 | Unit Weight (grams) | `1000` | ✅ per-kg unit of account — see §5.1 |
| 12 | SKU Product ID | — | n/a — not sold, so no SKU |
| 15 | Inventory Type | — | ❌ should identify it as a block |
| 16 | Sale Type | — | ❌ **must be `Bulk`** |

**Unit Weight (grams) is not optional** — bars carry it (col 10 = `50`) and it is what a later conversion divides by. A block without it cannot be cut correctly. Block #1 carries **`1000`**, because it is booked as a **per-kg asset** (`Amount` = 2.5 kg). The value states the *unit of account*, **not** the physical size of the block — see §5.1.

**`Sale Type` must be `Bulk`, never `Retail Ready`** — see the ruling at the top. The ledger already follows this convention: bars r21/r22 and ceremonial r123 are `Retail Ready`; nibs r83 and butter r131 are `Bulk`. Misclassifying a block as `Retail Ready` would push interim inventory into retail-facing channels.

### `#1` suffix = new currency per batch

A trailing `#1` means **block #2 gets its own currency row**, because its unit cost will differ. Decide explicitly before #2 exists; retrofitting a stable key later is expensive, because conversions and price components key off the currency name.

Since blocks are **not sold and carry no QR codes**, they do *not* need the stable consumer-facing identity a bar SKU does — which makes per-batch keys (`#1`, `#2`, …) the natural choice.

### Which spreadsheet? `Currencies` lives on MAIN only

**Create and edit block currencies in MAIN `Currencies` — never in a location ledger.**

Each location ledger's `State` tab is a live **read-only mirror**:

```
=IMPORTRANGE("1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU", "Currencies!A:B")
```

Block #1 appears at AGL13 `State` **r180** only because MAIN `Currencies` r180 exists. Writing a currency into the imported block is futile — IMPORTRANGE owns those cells and will overwrite or reject the edit. `Balance` reads through the mirror, so a currency created there is invisible to it.

---

## 6. Unit cost formula

```
unit_cost_per_kg = (nibs_kg × nibs_price + butter_kg × butter_price + sugar_kg × sugar_price) / finished_kg
```

**Use the landed cost at the consuming location**, i.e. the currency whose name includes the freight leg.

### Worked example — AGL13 Block #1 (arithmetic exact; sugar unit price provisional)

| Input | kg | $/kg | USD | Source |
|---|---|---|---|---|
| Cacao nibs | 2.00 | 27.25 | 54.50 | `Currencies` r83 — *Santos 20260213 - AGL13 + SF* (landed SF) |
| Cacao butter | 0.10 | 34.40 | 3.44 | `Currencies` Coopercabruca butter |
| Cane sugar | 0.40 | 6.1508971 ⚠️ | 2.46035884 ⚠️ | `Currencies` r178 — **unit price in dispute, see the warning below** |
| **Total** | | | **60.40035884** | ÷ 2.5 kg |
| **Unit cost** | | | **24.160143536 /kg** | ✅ matches ledger exactly |

> ⚠️ **Sugar price is unresolved — do not treat r178 as settled.** v1.1 instructed *"use the more expensive one — it reflects actual acquisition cost."* **That premise does not hold:**
>
> - `$6.1508971/kg` is **$2.79/lb**, which traces to an **Instacart aggregator snippet**, not a Rainbow Grocery shelf price.
> - Rainbow's own product pages show **brown sugar $2.49/lb ($5.48951/kg)** and **white cane sugar $1.79/lb ($3.946274/kg)**.
> - Neither registered row is confirmed to be the SKU actually bought, and the lb→kg conversion is our arithmetic, not a shelf quote.
>
> **Standing rule:** a currency `Price in USD` must trace to a **first-party shelf price for an identified SKU**. An aggregator snippet is **not** sufficient, and "more expensive" is not a proxy for "accurate".
>
> Until brown-vs-white is confirmed, Block #1's `$60.40035884` total and `$24.160143536/kg` are **provisional**. The exposure is small (~$0.011 per 50 g bar, i.e. immaterial to retail price) but the figures must not be quoted as verified.
>
> **To close it:** confirm with Kirsten whether the sugar is brown or white, re-point the currency at the verified shelf price, then re-cost the block. Recorded as defect §8.7.

> **Nibs price trap.** The nibs currency exists in three forms: base ($10.18/kg), and + SF ($27.25/kg landed). Use the **landed** figure for the location. Do not use $7.56/kg — that is beans, not nibs.

---

## 7. Verification — do not skip

After booking, confirm on the location's `Balance` tab:

- [ ] Asset quantity appears in the **amount** column. `Balance` is `QUERY(... sum(D) ...)` driven, so **amounts must be written as numbers, not text** — `sum()` silently ignores strings and the cell stays blank.
- [ ] Location column attributes custody to the right person.
- [ ] Equity total increased by the in-kind value.
- [ ] Both the consuming location and MAIN reconcile to zero for every injected input.

```python
# amounts must land as numeric
check = ws.get(f"D{row}:D{row}", value_render_option='UNFORMATTED_VALUE')[0]
assert isinstance(check[0], (int, float)), "written as TEXT — Balance will show 0"
```

### Row placement — the append trap

Both ledgers have a **title row above the header**, so an `append` with `INSERT_ROWS` lands *at row 2 and shifts the header down*:

| Ledger | Tab | Layout |
|---|---|---|
| AGL13 | `Transactions` | title **r1**, blank r2, header **r3**, data r4+ |
| MAIN | `offchain transactions` | header **r1**, data r2+ |

This silently corrupts the sheet while looking like a successful write — and it happened twice in one session on 2026-11-14.

**Always write to an explicit cell range, then assert the header is still where it belongs:**

```python
row = len(existing_values) + 1          # explicit, computed
ws.update(f"A{row}:F{row}", [row_values], value_input_option='RAW')

# header integrity — run AFTER every write
hdr = ws.get("A3:F3", value_render_option='UNFORMATTED_VALUE')[0]
assert hdr[0] == 'Date', f"HEADER MOVED — found {hdr[0]!r}, expected 'Date'"
title = ws.get("A1:A1")[0]
assert 'Contract URL' in str(title[0]), "TITLE ROW DAMAGED"
```

If the grid is full, `append` fails with *"exceeds grid limits"* — expand it with `update_sheet_properties(gridProperties={'rowCount': n})` rather than reaching for `append`.

If you do corrupt the layout, delete the inserted row via `deleteDimension` and rewrite at an explicit range. **Do not leave the shifted header in place** — `Balance` is `QUERY`-driven and will read garbage.

---

## 8. Known defects & open questions

Documented, **not** silently corrected — unbacked reversals need a physical count.

### 8.1 The block is 84% cacao by weight, labelled 81%

`(2.0 nibs + 0.1 butter) / 2.5 = 84%`; sugar is 16%.

The block's composition JSON (`agroverse-inventory/currency-compositions/2abac3bb-...json`) records `cacao_mass_fraction: 0.84` / `sugar_mass_fraction: 0.16`.

> ⚠️ **Do not treat that file as independent corroboration.** Its `source` is `sophia_autopilot_backfill` and its `raw_request_text` opens *"BACKFILL NOTES (Sophia Truesight...)"* — it is **my own reconstruction from the same ledger rows**. Citing it back as proof is circular. The 84% is arithmetically certain from the inputs; it is *not* independently measured.

**Because blocks are interim inventory and never sold, this is a naming issue, not a product-recall issue** — lower stakes than it first appears. It is still not ignorable: the 50 g bars cut from this block **are** sold, and their label must reflect the block's true composition rather than the block's name. Options: relabel the block `84%`, or reformulate to a true 81% going forward (nibs 1.925 + butter 0.1 + sugar 0.475 → 2.5 kg).

### 8.2 Block sugar was a plug, not a measurement

0.4 kg = `2.5 − 2.0 − 0.1`, which **assumes zero yield loss**. The bar batch on the same equipment by the same operator lost **4.8%**. At 4.8% loss the real sugar figure is ≈ 0.52 kg. The ledger legs are arithmetically self-consistent; the *physical* number is unverified.

**Action:** weigh sugar at the next batch. Record the weighed value in the row description, not a derivation.

### 8.3 Bar batch r42/r43 has no sugar and cannot be 81%

2.1 kg in, 2.0 kg out → cacao = **105% of finished weight**, physically impossible. Either sugar was used and never booked, or the `81%` label is wrong. This affects unit cost and therefore the price of every one of those 40 bars — **and unlike blocks, these bars are sold**.

**Action:** count/confirm what actually went into the 20261025 batch before those bars are priced or sold.

### 8.4 Zero-loss assumption

Block #1 books exactly zero yield loss (2.5 in → 2.5 out). Loss is certain in practice (melanger retention, mould scrapings). Treat 0% as **unknown, not as truth** — the finished weight should be weighed, and any loss booked explicitly.

### 8.5 Process parameters not captured

Roast profile, melanger duration, tempering curve, equipment ID, cold-hold time — all absent. Without them a batch cannot be reproduced or a defect diagnosed. This matters more, not less, because Kirsten is currently the sole block maker: her method is an unrecorded single point of failure. Requires a decision on where these live (ledger description vs a separate production sheet).

### 8.6 Currency fields incomplete

Block currency was missing `Unit Weight (grams)` (col 10) — **now populated as `1000`** (per-kg unit of account; see §5.1). Still missing `Year` (col 9); `SKU Product ID` (col 12) is not applicable since the block is not sold. `Sale Type` / `Inventory Type` (cols 15/16) unset and should be `Bulk`. Note `Serializable = TRUE` (col 2) is a creation leftover and is **not** a serialization instruction — see §9.

### 8.7 Sugar unit price is unverified (affects every block cost)

`Currencies` r178 carries **$6.1508971/kg**, which equals **$2.79/lb** — a figure traceable to an **Instacart aggregator snippet**, not to a Rainbow Grocery shelf price. Verified first-party prices are **brown $2.49/lb ($5.48951/kg)** and **white cane $1.79/lb ($3.946274/kg)**.

Consequences:

- Block #1's `$60.40035884` and `$24.160143536/kg` are **provisional**, though the arithmetic on top of the sugar price is exact.
- Every block and every bar cut from a block inherits the error.
- Materiality is low (~$0.011 per 50 g bar) — this is a **documentation-integrity** defect, not a pricing crisis. Fix it before it becomes the default input to a bigger batch.

**Action:** confirm brown vs white with Kirsten; re-point the currency at the verified shelf price; re-cost Block #1. Also confirm *which* SKU she actually buys — neither registered row is verified as the product purchased.

---

## 9. Blocks get no QR codes (settled)

**Ruling 2026-11-14: blocks are interim inventory, not for sale → never serialized.** No QR batch is generated for a block, and a block never enters the QR manifest pipeline.

The block currency still carries `Serializable = TRUE` (col 2). That flag is a leftover from creation — **it is not an instruction to serialize**, and it is not evidence a block needs a QR. Leave the batch generator (which is bar-shaped, one label per unit) pointed at bars only.

**What does need QR codes: the 50 g bars cut from a block.** Each bar is a serialized sale unit and gets a QR per `AGROVERSE_QR_CODE_BATCH_GENERATION.md`. That conversion must also:

- decrement the block by the mass actually consumed;
- yield-check: `bars × 50 g` reconciled against block weight minus loss;
- register the resulting bar currency with its **actual** composition taken from the block, not from the block's name.

---

## 10. Checklist

**Before production**
- [ ] Target weight and target % cacao agreed.
- [ ] Nibs lot identified; landed $/kg confirmed.
- [ ] Butter and sugar sourced; the **more expensive** sugar link registered.

**During production**
- [ ] Weigh every input actually used (nibs, butter, sugar) — not a calculation.
- [ ] Record melanger duration, tempering working temp, mould.
- [ ] **Weigh the finished block.**
- [ ] Photograph the block and the scale reading; archive to `TrueSightDAO/.github`.

**Ledger**
- [ ] Classified as interim inventory: `Sale Type = Bulk`; **no QR codes requested** for the block itself.
- [ ] Inputs received into MAIN (asset + equity if in kind).
- [ ] Injected MAIN → location (two legs each).
- [ ] Consumption legs booked at the location.
- [ ] Block registered in `Currencies` — **`Unit Weight (grams) = 1000`** for a per-kg block (§5.1). Do **not** enter the block's physical size (`2500`).
- [ ] Unit cost computed from landed prices; block asset + quantity booked.
- [ ] `Balance` verified — quantities numeric, equity increased, nets reconcile.
- [ ] Any derived (not weighed) figure flagged as such in the description.

---

## References

- `LEDGER_CONVERSION_AND_REPACKAGING.md` — conversion conventions; equity/asset imbalance = accrued net profit
- `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` — bag quantities
- `agroverse/BEAN_TO_BAR_EQUIPMENT_INVENTORY.md` — melanger/mould/temperer acquisition
- `agroverse/AGROVERSE_QR_CODE_BATCH_GENERATION.md` — bar QR conventions

### Ledger evidence for this SOP (AGL13 Block #1)

| Row | Leg |
|---|---|
| AGL13 `Transactions` r59 | nibs −2.0 kg |
| r60 | butter −0.1 kg |
| r61 / r64 | sugar received in kind / reversed |
| r65 / r67 | sugar injected / consumed |
| r62 | block +2.5 kg |
| r66 | equity +$2.46035884 |
| MAIN `offchain transactions` r6064–r6066 | receipt, injection out, equity holdings |
| `Currencies` r178 / r180 | sugar, block |
