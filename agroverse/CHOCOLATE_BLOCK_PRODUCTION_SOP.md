# Chocolate Block Production & Ledger Booking — SOP

**Scope:** producing a bulk tempered cacao block (e.g. 2.5 kg) and booking it correctly in the DAO ledger.
**Status:** v1.1 (amended 2026-11-14 per governor ruling). Every figure below is sourced from the live ledger.
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
| Currency example | `... Chocolate Bar 50g \| Vivi Cacao Nibs \| Kirsten 20261025 \| San Francisco - AGL13` | `... Chocolate Block 2.5kg #1 \| Vivi Cacao Nibs \| Kirsten 20261114 \| San Francisco - AGL13` |

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
Agroverse <pct>% Cacao Chocolate Block <weight>kg #<n> | <nib origin> | <maker> <YYYYMMDD> | <location>
```

### Required fields (col index)

| Col | Field | Block #1 value | Status |
|---|---|---|---|
| 0 | Currencies (name) | `...Chocolate Block 2.5kg #1 \| Vivi Cacao Nibs \| Kirsten 20261114 \| San Francisco - AGL13` | ✅ |
| 1 | Price in USD | `24.160143536` | ✅ per-kg |
| 2 | Serializable | `TRUE` | ⚠️ leftover — see §9 |
| 4 | landing_page | `https://agroverse.shop/shipments/agl13/index.html` | ✅ |
| 5 | ledger | MAIN spreadsheet URL | ✅ |
| 6/7/8 | farm / state / country | Jesus do Deus / Bahia / Brazil | ✅ |
| 9 | Year | — | ❌ missing |
| 10 | Unit Weight (grams) | `2500` | ✅ |
| 12 | SKU Product ID | — | n/a — not sold, so no SKU |
| 15 | Inventory Type | — | ❌ should identify it as a block |
| 16 | Sale Type | — | ❌ **must be `Bulk`** |

**Unit Weight (grams) is not optional** — bars carry it (col 10 = `50`) and it is what a later conversion divides by. A block without it cannot be cut correctly. (It is now populated on Block #1.)

**`Sale Type` must be `Bulk`, never `Retail Ready`** — see the ruling at the top. The ledger already follows this convention: bars r21/r22 and ceremonial r123 are `Retail Ready`; nibs r83 and butter r131 are `Bulk`. Misclassifying a block as `Retail Ready` would push interim inventory into retail-facing channels.

### `#1` suffix = new currency per batch

A trailing `#1` means **block #2 gets its own currency row**, because its unit cost will differ. Decide explicitly before #2 exists; retrofitting a stable key later is expensive, because conversions and price components key off the currency name.

Since blocks are **not sold and carry no QR codes**, they do *not* need the stable consumer-facing identity a bar SKU does — which makes per-batch keys (`#1`, `#2`, …) the natural choice.

---

## 6. Unit cost formula

```
unit_cost_per_kg = (nibs_kg × nibs_price + butter_kg × butter_price + sugar_kg × sugar_price) / finished_kg
```

**Use the landed cost at the consuming location**, i.e. the currency whose name includes the freight leg.

### Worked example — AGL13 Block #1, verified to the cent

| Input | kg | $/kg | USD | Source |
|---|---|---|---|---|
| Cacao nibs | 2.00 | 27.25 | 54.50 | `Currencies` r83 — *Santos 20260213 - AGL13 + SF* (landed SF) |
| Cacao butter | 0.10 | 34.40 | 3.44 | `Currencies` Coopercabruca butter |
| Cane sugar | 0.40 | 6.1508971 | 2.46035884 | `Currencies` r178 — wholesale per-lb (the **more expensive** of the two sugar links) |
| **Total** | | | **60.40035884** | ÷ 2.5 kg |
| **Unit cost** | | | **24.160143536 /kg** | ✅ matches ledger exactly |

> **Landing-page trap.** Two sugar rows were registered: r178 wholesale @ $6.1508971/kg and r179 retail 2 lb box @ $6.0516891/kg. **Use the more expensive one** — it reflects actual acquisition cost. Getting this wrong understates the block and every bar cut from it.

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

Block currency was missing `Unit Weight (grams)` (col 10) — **now populated as 2500**. Still missing `Year` (col 9); `SKU Product ID` (col 12) is not applicable since the block is not sold. `Sale Type` / `Inventory Type` (cols 15/16) unset and should be `Bulk`. Note `Serializable = TRUE` (col 2) is a creation leftover and is **not** a serialization instruction — see §9.

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
- [ ] Block registered in `Currencies` — **including Unit Weight = grams**.
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
