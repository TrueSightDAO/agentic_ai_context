# Chocolate bar production accounting (81% bars from cacao in managed AGLs)

**Status:** CONFIRMED by Governor Gary Teh, 2026-10-27. Worked case: AGL13 / Kirsten, 40 bars.
**Canonical for:** producing finished chocolate bars at an operator's location from cacao already
sitting in a managed AGL.
**Reads with:** `LEDGER_CONVERSION_AND_REPACKAGING.md` (general playbook) ·
`brazil/FREIGHT_PROFIT_ANALYSIS_METHODOLOGY.md` §6 (COGS) ·
`conventions/INTER_LEDGER_HOLDINGS.md` (cross-ledger rules).

---

## 1. The one-line rule

A bar-production run is a **REPACKAGING batch** — **not** a capital injection, **not** a sale.

Consumables (pouches, envelopes, QR labels/stickers) are **production inputs whose cost is COGS**.
They do **not** create an equity stake for whoever paid for them.

---

## 2. Why this is a repackaging batch

`LEDGER_CONVERSION_AND_REPACKAGING.md` defines ledger conversion as: at a specific place/operator,
inventory **consumes input `Currency` lines and creates output units**.

`FREIGHT_PROFIT_ANALYSIS_METHODOLOGY.md`:

> §6.2 *"…Add label costs (Sticker Mule labels at $0.55 each)"*
> §6.3 *"Total COGS = Cacao Cost Basis + Packaging Materials"*

⇒ Envelopes and stickers are **packaging materials** → COGS → they flow into the **output bar's
unit cost**. No equity leg, no capital injection.

---

## 3. Cost per bar (the formula)

```
cost per bar = [ Σ (input qty × input unit cost)  +  labour/overhead if allocated ] / bars produced
```

### 3.1 Input catalog lines (verified live, Main `Currencies`)

| Input | Currency key | Unit cost |
|---|---|---|
| Cacao nibs | `Cacao Nibs (KG)` | $27.25 / kg |
| Kraft pouch | (the AGL13 pouch line) | $0.6754468485 / pc |
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
> Booking on the $0.0581 lookalike understates the expense by **$19.84 on 40 units** and permanently
> mislabels provenance (the ledger is append-only). **Check dimensions + vendor + order ref**, never
> name similarity. Corroborated independently by
> `brazil/FREIGHT_PROFIT_ANALYSIS_METHODOLOGY.md:137` *"Sticker Mule labels at $0.55 each"*.

### 3.2 Worked example — 40 bars

| Component | Per bar | × 40 |
|---|---|---|
| Nibs (50 g @ $27.25/kg) | $1.3625 | $54.5000 |
| Pouch | $0.6754468485 | $27.0179 |
| Envelope | $0.0705 | $2.8200 |
| Sticker | $0.554 | $22.1600 |
| **Materials subtotal** | **$2.6624468485** | **$106.4979** |

Note the sticker is **7.9× the envelope** — packaging cost is dominated by the label, not the bag.
The earlier pinned figure of **$2.038/bar** covered nibs + pouch only; it is **incomplete** for a
finished, QR-sealed bar.

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

Playbook rule: add labour/overhead **only if it is a separate allocated ledger line**. But on a
small batch a *fixed* labour charge dominates everything else:

| Bars | Labour ($200 fixed) per bar | Materials | **Unit cost** | vs wholesale $6 | vs retail $10 |
|---|---|---|---|---|---|
| 40 | $5.0000 | $2.6624 | **$7.6624** | **−$1.66 → LOSS** | +$2.34 |
| 90 | $2.2222 | $2.6624 | **$4.8847** | +$1.12 | +$5.12 |

⇒ At **40 bars, a $200 labour charge makes the batch loss-making at the $6 wholesale price.**
Buying ~50 more envelopes costs ≈$3.53 and repairs the unit economics.

**Before booking a batch, surface to the governor:** (a) whether the labour figure is per-batch or
per-bar, (b) what it covers, (c) the resulting unit cost vs both price points.

---

## 6. Pipeline — four units, in order

1. **Main expense** — consumables bought with Main cash.
   `truesight-dao-report-dao-expenses`, Target Ledger `offchain`.
2. **INVENTORY MOVEMENT** — consumables Main → the AGL that will hold them (physical custody with
   the operator).
3. **REPACKAGING BATCH** — inputs consumed → a **new output `Currency`** for the finished bar with
   **col B `Price in USD` = computed cost per bar**. Register it with
   `truesight-dao-define-currency` (`[CURRENCY DEFINITION EVENT]`) so it is QR-ready — see
   `agroverse/AGROVERSE_QR_CODE_BATCH_GENERATION.md` §2b.
4. **QR generation** — one QR per physical bar.
   Runbook: **`agroverse/AGROVERSE_QR_CODE_BATCH_GENERATION.md`** — note the `agroverse/` **subpath**
   (a root-level lookup 404s; this is why it was previously reported "missing").

Then **`[REPACKAGING SETTLEMENT EVENT]`** (`post_repackaging_cleanup`) once
`currency-compositions/<request_id>.json` is live.

---

## 7. Custody vs ownership — do NOT move bars to MAIN by default

An AGL ledger **already models both halves**:

- **Assets** row → `Entity` = the **human custodian** (who physically holds the goods)
- **Equity** row → `Entity` = the **DAO / financier** (who economically owns them)

So *"DAO-owned bars in Kirsten's hands"* is **exactly** what an AGL13 row pair already expresses.
Nothing is lost by keeping them there.

**Putting the bars on MAIN loses custody fidelity.** Main is a book — not a place, not a person. A
Main asset row saying *"DAO holds 40 bars"* is silent on whether they are physically in SF with
Kirsten or elsewhere, and in practice the physical holder is still the operator. You would have to
invent a holder name to recover information the AGL row already carried.

Moving bars AGL → Main is also **not free**: it needs a reciprocal pair —
`AGL Assets −` / `AGL Equity −` and `Main Assets +` / `Main Equity +` (four rows, two per ledger) —
for zero informational gain, and it doubles the audit trail.

### 7.1 Decision rule

| Bars should live on… | When |
|---|---|
| **The AGL (default)** | The operator produced them and/or will hold or sell them. Sales booked there; Main consolidates the result. |
| **MAIN** | Only if the bars are **DAO-branded finished goods sold centrally** (online shop / FounderHaus) and the operator's role genuinely **ends at production**. Then do **one** `INVENTORY MOVEMENT` after the batch **with** the reciprocal equity pair, and **name the human physically holding them** on the Assets leg. |

> **Non-negotiable:** whichever ledger holds the bars, the **SALES EVENT must be booked on that same
> ledger**. A sale booked elsewhere produces the *sold-but-never-landed* orphan class (see
> `OPEN_FOLLOWUPS.md`). **Never split holding from selling.**

**OPEN — awaiting governor ruling on MAIN vs AGL for DAO-branded bars.** Record the ruling here
when made.

---

## 8. Traps

- **Do not book consumables as a `CAPITAL INJECTION`.** That handler hardcodes `Currency = 'USD'` on
  both legs and stamps one `Entity` on both — it would record *"AGL received $N of cash"*. Wrong
  shape for in-kind goods. (See `INTER_LEDGER_HOLDINGS.md` §8.3b for the code evidence.)
- **Do not create an equity stake for DAO-paid packaging.** It is absorbed into bar COGS. A future
  session expecting a stake back from the ~$24.98 is misreading §8 of the older doc.
- **Verify a `Currencies` key against the LIVE sheet, not `agroverse-inventory/currencies.json`.**
  That snapshot's **E-section is missing entirely** (it jumps `Digital Kitchen Scale` → `ETH` →
  `Foam container box`), so an E-initial name can *never* appear there. This produced a false
  "no envelope key exists" conclusion in a prior session. Read `Currencies!A1:B400` live.
- **Sticker ≠ sticker.** Check dimensions + vendor + order ref (§3.1).
- **Bar count is the scarcest input**, not the nibs weight (§4).
