# SKU naming — component vs finished good

**Status:** canonical · **Created:** 2026-11-26 · **Owner:** Sophia Truesight

How to tell what a `Currencies` row actually *is*, without trusting its name.

> **The rule in one line:** the noun phrase in a SKU name is a **noun class, not a product**. Read `Serializable`, the **unit price**, and **whether a delivery suffix is present** — never the name alone.

---

## 1. The trap

`Currencies` names collide on purpose-built vocabulary. "Kraft Pouch" appears in both
an **empty disposable** and a **finished sellable product**:

| Row | Name string | Price | Serializable | What it actually is |
|---|---|---|---|---|
| r113 | `Ceremonial Cacao Kraft Pouch - 20250219006` | **$0.6754468485** | blank | **empty pouch** — component, consumed in packing |
| r92 | `Cacao Nibs Kraft Pouch - 20250219006` | **$0.6754468485** | blank | **empty pouch** — component |
| r91 | `Cacao Nibs Kraft Pouch` | **$0.34** | blank | **empty pouch** — component |
| r13 | `8 Ounce Package Kraft Pouch - Ilheus, Brazil 2024` | **$6.64** | TRUE | **finished, sellable** nibs pouch |
| r122 | `Ceremonial Cacao Kraft Pouch - 20250219006 \| Cacao Mass \| 200 grams \| Paulo 2024 \| Santos 018-2025 016-2025 \|\| Ilheus - AGL8 + 047-3175-3223 - San Francisco` | **$13.85857** | TRUE | **finished, sellable** ceremonial cacao, arrived SF |

Three rows share the head noun `Kraft Pouch` at **$0.34–$0.675**; two share it at
**$6.64–$13.86**. The words are identical. **Only the price and the qualifiers differ.**

---

## 2. The three-axis rule

Evaluate in this order. Never classify from the name alone.

### Axis 1 — unit price magnitude (strongest, most reliable)

| Price band | Reads as |
|---|---|
| **< ~$1.00** | almost certainly a **component / consumable** (pouch, sticker, seal, empty bag) |
| **$2 – $5** | small finished good (bar, tea) **or** an unusually pricey component — check Axis 2 |
| **> ~$5** | **finished good**, staged or arrived — even when `Serializable` is blank |

This is the axis that most directly catches the failure mode: a $0.675 empty pouch
can never be cacao, and a $13.86 line can never be an empty pouch.

### Axis 2 — name qualifiers

A **finished** line practically always carries at least one of:

- a **fill/farm/origin** qualifier — `Cacao Mass`, `Cacao Nibs`, `Cacao Almonds`, `Oscar 2024`, `Paulo 2024`
- a **date or batch** marker — `20250219006`, `Santos 018-2025 016-2025`
- a **delivery suffix** — `+ 047-3175-3223 - San Francisco`, `+ CP340993838BR - Zurich`
- a **holder + date** tail — `| Kirsten 20251124 | San Francisco - AGL4`

A **component** is a bare noun plus at most a spec code: `Cacao Nibs Kraft Pouch`,
`Ceremonial Cacao Kraft Pouch - 20250219006`, `Heat Sealer for Kraft Pouch`,
`QR Sticker`.

### Axis 3 — `Serializable` (`Currencies` col C)

- **`TRUE`** ⇒ a **serializable / QR-target** row. Reliable as a *positive* marker.
- **blank** ⇒ **NOT a serialization target.** This does **not** mean component. See §3.
- **`FALSE`** ⇒ explicitly not serializable; treat as component. (Caveat: r47
  `Cacao Almonds (KG) + … - San Francisco` is `FALSE` on a deprecated renamed
  line — read the `[DEPRECATED …]` note in the name.)

> **Caveat on `TRUE`:** per `CHOCOLATE_BLOCK_PRODUCTION_SOP.md` §9, `TRUE` is sometimes a
> *creation leftover* on chocolate-block currency and **is not by itself an instruction to
> serialize**. `TRUE` proves a row *can* be serialized — not that it *must* be. The flag is
> reliable in the **negative** (blank/FALSE ⇒ do not QR-target it) and advisory in the positive.

---

## 3. `Serializable = blank` is NOT "component"

This is the subtle part, and getting it wrong is how a **component** gets read as cacao:

| Row | Serializable | Price | What it actually is |
|---|---|---|---|
| r113 | blank | $0.675 | empty pouch — **component** |
| r15 | blank | $9.45 | `8 Ounce … + CP340993838BR - Zurich` — **finished, staged** |
| r119 | blank | $8.315 | Oscar ceremonial, `+ … San Francisco - AGL8` — **finished, staged** |
| r121 | blank | $10.37 | Paulo ceremonial, `\|\| Ilheus - AGL8` **origin** — finished cacao, still in Brazil |

Blank spans **both** classes. It means *"this row is not a serialization target"* — which is
true of an empty pouch **and** of an unsuffixed origin/staging line whose arrived
counterpart is the serializable one.

**Therefore:** blank + price **< ~$1** ⇒ component. Blank + price **> ~$5** ⇒ a **staged/
unsuffixed finished good**, not a component. Never classify on blank alone.

### Staged-vs-arrived pairs

Freight arrival is modelled as **two rows**, not one:

```
origin  (unsuffixed, often blank Serializable, priced ≈ production cost)
   ↓  [+ AWB + destination city]        ← the arrival leg naming convention
arrived (AWB suffix, Serializable=TRUE, priced ≈ landed cost)
```

Worked pair: **r121** `… || Ilheus - AGL8` **$10.37** (blank) → **r122** `… + 047-3175-3223 - San Francisco` **$13.85857** (TRUE).
Same physical pouches, two stages. Per `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` col M,
`Destination Asset Name = Origin Asset Name + AWB + destination city`.

**Consequence:** a QR code must point at the **arrived** row. Pointing it at the origin row
puts the bag on a non-serializable line — see §4.

---

## 4. Worked failure case (2026-11-26)

The error this doc exists to prevent.

**Claimed:** *"AGL8 still holds 169 ceremonial cacao with Matheus Reis; and MAIN shows
Matheus 115 + Gary 74 = 189, which doesn't reconcile with 170."*

**Both halves were wrong, for two different reasons.**

1. **Wrong columns.** The AGL8 tab's `Asset`/`Amount`/`Resource Location` block (cols E/F/H)
   was read as "the balance." The actual pouches were in the **`Liabilities`** block
   (cols I/J) at **Kirsten Ritschel — 170**. The governor caught this.
2. **Wrong asset entirely.** The *115 at Matheus* on MAIN is **empty pouches** —
   `Ceremonial Cacao Kraft Pouch - 20250219006` @ $0.675 — not cacao. Comparing
   **189 empty pouches** against **170 finished cacao** is meaningless: different asset,
   different unit cost, no reconciliation owed.

**The tell that was missed:** AGL8 `Transactions` r196 already stated it plainly —
*"169 empty … pouches consumed from Matheus Reis's Main-held packaging stock to produce the
169 finished units"* → 284 − 169 = **115 remaining empties**. The sentence was in hand.

**Correct reconciliation:** Kirsten **170 finished** = the 169 filled + 1 previously on the
origin SKU. Nothing was orphaned. Empty pouches remaining in Brazil: **115** (+74 Gary) —
both are packaging stock, neither is cacao.

**Second-order error worth noting:** the conclusion "r121 is `Serializable=''`, therefore a
component, therefore the QR repoint was correct" was **right answer, wrong reason**. r121 is
**finished cacao at $10.37**, not a component. The repoint was correct because the QRs
belonged on the **arrived** row (r122, `TRUE`) per §3, and because the manager was wrong —
not because the origin line was a component.

---

## 5. Before you reason about any `Currencies` row

1. Read **`Price in USD`** and **`Serializable`** *first* — before forming any opinion.
2. Classify with **all three axes** (§2). Name alone is never sufficient.
3. If `Serializable` is **blank**, use price to split component (< ~$1) from staged finished (> ~$5).
4. If the SKU has **no delivery suffix**, expect a **staged** row — go find its arrived
   counterpart before reasoning about quantity or location.
5. Run `python3 scripts/describe_sku.py "<sku string>"` in `truesight_autopilot` for a
   machine-read of all three axes plus live balances.

> **Do not** infer product-vs-component from the name. **Do not** compare a component's
> quantity against a finished good's quantity. **Do not** treat `Serializable=''` as proof
> of *either* class on its own.

---

## 6. Related

- `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` — bags, quantities, inventory
- `LEDGER_CONVERSION_AND_REPACKAGING.md` — repackaging consumes components, creates finished lots
- `SUPPLY_CHAIN_AND_FREIGHTING.md` — cost build-up across the staging → arrived legs
- `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` — the AWB naming convention (col M)
- `CHOCOLATE_BLOCK_PRODUCTION_SOP.md` §9 — `Serializable=TRUE` as creation leftover
- `truesight_autopilot` `app/tools/sku_lookup.py` + `scripts/describe_sku.py`
