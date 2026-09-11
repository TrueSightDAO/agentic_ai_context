# Black King (Matheus Reis Pereira) — shipment manifests & origin unit costs

Per-shipment breakdown of the **Ilhéus, BA → US** export corridor operated through
**Black King** (Matheus Reis Pereira, CNPJ 50.042.585/0001-80).

For each shipment: **what was shipped** (from the FDA FSVP prior notices — the record of
what actually crossed the border) and **each line item's origin unit cost prior to shipping,
in USD** (from the Main Ledger `Currencies`/`offchain asset location` tabs, joined by product).

Machine-readable mirror: `black_king_shipments.json`. Tracking-number index: `CORREIOS_SHIPMENTS.md`.

> **Revision 4 (2026-09-11, governor-corrected, thread 26215):** **Reverted the Revision-3
> error** — **Shipment 9 (AGL7 molasses) DID pass through**; restored to the totals. **Shipment 14**
> (2025-10-09 hand-carried) remains excluded per governor instruction. Weight columns retained.
> Totals (per Rev-4; superseded by Rev-6): **212.67 kg · USD 5,669.35** origin value (excl. #12 [no qty], #14). **Open:** a
> governor note that *a ceremonial-cacao shipment from AGL8 did not pass through* is **pending
> confirmation of the exact manifest line** before any row is flagged.

> **Revision 5 (2026-09-11, thread 26215): post-EO (de-minimis) import-gate context.**
> **Executive Order 14324** ("Suspending Duty-Free De Minimis Treatment for All Countries") was
> **signed 2025-07-30** and **effective 2025-08-29** — from that date CBP rejected all de-minimis
> entries and every commercial import required formal entry. On this corridor the **only FDA prior
> notice filed on/after 2025-08-29 is Shipment 14** (2025-10-08/09, hand-carried, Avianca AV560) —
> the cargo the governor carried across the border himself. **Every other post-cutoff consignment
> has no prior notice on file** — the documentary signature of **blocked / never-shipped** cargo
> (nothing was filed to clear it). Per the governor (thread 26215), the large blocked lot is
> **DAO inventory carried on the Main Ledger** (`offchain asset location` tab) rather than a line in
> this Black King manifest; candidate lots still held in Brazil include the **AGL8 ceremonial cacao**
> (Santos/Martinus-produced; ledger line *"Ceremonial Cacao Kraft Pouch - 20250219006"*, held by
> *Matheus Reis*) and the **Poland package** (500 g bars, rejected). **Row-level flagging remains
> pending governor confirmation of the exact ledger line.**

---

> **Revision 6 (2026-09-11, thread 26215): governor-confirmed exclusions.** Per the governor,
> **Shipment 8 (2025-02-28, 10 × 500 g ceremonial bars) and Shipment 13 (2025-06-27, ceremonial
> bars + caramelized) NEVER SHIPPED** — Black King (Matheus) repeatedly missed the export
> deadlines — so both are **struck from this manifest and excluded from all totals** (origin
> **-USD 784.75**, weight **-30 kg**). An earlier broader rule ("all 2025 Correios lanes out") was
> **withdrawn by the governor as too broad**; **Shipment 9 (AGL7, Correios) is retained**
> (pass-through). **Updated totals: 182.67 kg · USD 4,884.60** origin value.

> **Revision 7 (2026-09-11, thread 26215): arrival-register cross-check.** The Main Ledger
> **`offchain assets in transit`** tab (gid `1888711771`) is the **arrival register** — every
> delivered parcel, with its tracking number joined to a ledger line and a status. Cross-checked
> against this manifest: **Shipments 8 and 13 have no row in the arrival register** (no tracking
> number was ever assigned) — independent corroboration of the Rev-6 *never-shipped* finding.
> The landed caramelized unit cost cited under Shipment 13 is **re-homed to the AGL10
> consignment** (`CP340993299BR`), which *did* arrive (governor-confirmed; no caramelized line) — see the note on the cost-reference table.
> Index: `CORREIOS_SHIPMENTS.md` §*Arrival register*; machine mirror `in_transit_register.json`.

> **Revision 8 (2026-09-11, thread 26215): AGL10 caramelized question resolved (governor-confirmed).**
> The governor confirmed the AGL10 parcel **`CP340993299BR` arrived** (booked to Kirsten Ritschel;
> ledger lines 734/735) and carried **no caramelized line** — the arrival register lists 40 × 500 g
> mass bars only. The ledger currency line `Caramelized Cacao Beans (KG) + CP340993299BR San Francisco
> AGL10` is therefore a **costing reference only** for the *landed* caramelized unit cost: **no
> caramelized stock physically moved on that parcel**, and none belongs to Shipment 13. The Rev-7
> open question is **closed** — the Shipment-13 caramelized lot (5 kg) **never shipped as physical
> stock**. No totals change (Shipment 13 remains excluded): **182.67 kg · USD 4,884.60**.

---

## Origin unit-cost reference (USD, pre-export / ex-works Ilhéus)

These are the **origin cost basis** values used throughout — the value of the goods while
still in Brazil, before export freight/duty. All pulled from the Main Ledger; BRL rows
converted at the ledger rate **1 BRL = 0.19405 USD**.

| Item (origin form) | Unit cost (USD) | Unit | Source |
|---|---|---|---|
| Cacao Nibs (bulk) | 24.61847089 | per kg | Ledger: `Cacao Nibs (KG) - Ilheus, Brazil 2024` |
| Cacao Mass Bar 500 g | 15.6951006 | per bar | Ledger: `Cacao Mass Bar (500grams) - Ilheus, Brazil 2024` |
| 8 oz Nibs Kraft Pouch (finished) | 6.64 | per pouch | Ledger: `8 Ounce Package Kraft Pouch - Ilheus, Brazil 2024` |
| Cacao Husk | 17.7854853 | per kg | Ledger: `Cacao Husk (KG) - Ilheus, Brazil` |
| Cacao Tea (loose) | 13.6601548 | per kg | Derived: `Cacao Tea (loose grams) … AGL8` = 0.0136601548/g |
| Cacao Molasses (raw, from Luana Pinto Leite) | 2.911 | per litre | Nota fiscal R$15.00/L (2024-09-24 & 2025-03-15) |
| Cacao Almonds (raw, from Oscar) | 19.405 | per kg | Nota fiscal R$100.00/kg, 100 kg / R$10 000 (2025-02-18) |
| Caramelized Cacao Beans | 36.7492 **(landed)** | per kg | Ledger: `Caramelized Cacao Beans (KG) + CP340993299BR San Francisco AGL10` — *includes US freight* |

> ⚠️ **Re-homed (Rev-7):** this landed unit cost is drawn from the **AGL10** ledger line
> (`CP340993299BR`, San Francisco AGL10). It therefore belongs to the **AGL10 consignment**
> (40 × 500 g mass bars, ledger lines 734/735 — **arrived**; governor-confirmed — register lists mass bars only, no caramelized line), **not** to
> Shipment 13. The manifest had used it to value the Shipment-13 caramelized lot — a mis-join.

> ⚠️ **`landed` = not a pre-export cost.** Only the caramelized-beans line carries a
> freight-inclusive figure in the ledger; treated separately below.

---

## Shipment 1 — 2024-09-30 · Cacao Molasses, 30 × 250 g bottles

- **Carrier:** **FedEx** (NOT Correios) — AGL5 lane, "commercial import via air freight"
- **FDA prior notice:** Envelope `F24X24688706`, PN `240517670551`, submitted 2024-09-24, anticipated 2024-09-30, Entry Type *Mail (Commercial)*
- **Evidence:** `fda_fsvp/.../20240924_fda_prior_notice_30_bottles_cacao_molasses.pdf`, `20240924_invoice_for_30_bottles_cacao_molasses.pdf`, `20240925_fedex_shipping.jpeg`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Molasses 250 ml bottle | 30 | 12.143 *(ledger, landed SF)* | 364.29 |
| — | *origin molasses only (raw)* | 30 L | 2.911 /L (→ 0.728 /250 ml) | 87.32 *(R$450 nota fiscal)* |

**Shipment total (ledger unit costs): USD 364.29.** Origin raw-material value: USD 87.32.

---

## Shipment 2 — 2024-10-04 · Cacao Nibs, 30 kg

- **Carrier:** **Correios** — receipt `20241004_emelin_30kg_carreois_transport_receipt.jpeg`
- **FDA PN:** confirmation `240519102235`, submitted 2024-10-03, anticipated 2024-10-04, Entry Type *Mail (Commercial)*; 3 bags × 10 kg
- **Evidence:** `20241003_30kg_cacao_nibs_webentry_prior_notice.pdf`, `20241003_30kg_commercial_invoice.xlsx`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Nibs (bulk) | 30 kg | 24.61847089 /kg | 738.55 |

**Shipment total: USD 738.55.**

---

## Shipment 3 — 2024-11-01 · Cacao Nibs, 20 kg

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** confirmation `240523261506`, submitted 2024-10-31, anticipated 2024-11-01; 2 bags × 10 kg
- **Evidence:** `20241031_fda_fsvp_20kg_cacao_nibs_prior_notice.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Nibs (bulk) | 20 kg | 24.61847089 /kg | 492.37 |

**Shipment total: USD 492.37.**

---

## Shipment 4 — 2024-11-01 · Cacao Liquor (mass), 23 kg = 46 × 500 g

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** confirmation `240523265813`, submitted 2024-10-31, anticipated 2024-11-01; 46 packages × 0.5 kg
- **Evidence:** `20241031_fda_fsvp_23kg_cacao_liquor_prior_notice.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Mass Bar 500 g | 46 | 15.6951006 /bar | 721.97 |

**Shipment total: USD 721.97.**

---

## Shipment 5 — 2024-11-01 · Cacao Nibs, 88 bags (8 oz pouches)

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** confirmation `240523268263`, submitted 2024-10-31, anticipated 2024-11-01
- **Evidence:** `20241031_fda_fsvp_88bags_cacao_nibs_prior_notice.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | 8 oz Nibs Kraft Pouch | 88 | 6.64 /pouch | 584.32 |

**Shipment total: USD 584.32.**

---

## Shipment 6 — 2025-01-24 · Cacao Nibs, 120 bags

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** confirmation `250534805511`, submitted 2025-01-18, anticipated 2025-01-24
- **Evidence:** `20250118_black_king_120_bags_cacao_nibs.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | 8 oz Nibs Kraft Pouch | 120 | 6.64 /pouch | 796.80 |

**Shipment total: USD 796.80.**

---

## Shipment 7 — 2025-01-24 · Cacao Tea, 20 kg

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** confirmation `250534834955`, submitted 2025-01-19, anticipated 2025-01-24
- **Evidence:** `20250119_black_king_20_kg_cacao_tea.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Tea (loose) | 20 kg | 13.6601548 /kg | 273.20 |

**Shipment total: USD 273.20.**

---

## Shipment 8 — 2025-02-28 · Ceremonial Cacao 500 g, 10 bars — ⛔ **NEVER SHIPPED (excluded)**

> **Excluded per governor (thread 26215, 2026-09-11):** Black King (Matheus) missed the export
> deadlines — this lot **never shipped**. Retained as a documentary record; **struck from totals.**
> **Corroborated (Rev-7):** this lot has **no row in the `offchain assets in transit` arrival
> register** — no tracking number was ever assigned, consistent with never-shipped.

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** confirmation `250540041942`, submitted 2025-02-28; product *Amazonian Regenerative Ceremonial Cacao 500 grams*
- **Evidence:** `20250228_fda_prior_notice_10_bars_ceremonial_cacao_500grams.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Ceremonial Cacao 500 g bar | 10 | 15.6951006 /bar | 156.95 |

**Shipment total: USD 156.95 — ⛔ EXCLUDED (never shipped).**

---

## Shipment 9 — 2025-03-14 · Cacao Molasses, 20 × 250 g bottles

- **Carrier:** Correios (Entry Type *Mail (Commercial)*) — AGL7 lane. **Passed through** (governor-corrected 2026-09-11).
- **FDA PN:** confirmation `250541039416`, Envelope `F25X25832010`, submitted 2025-03-09, anticipated 2025-03-14; product *250 grams cacao molasses*
- **Evidence:** `20250309_fda_prior_notice_20_bottles_of_cacao_molasses.pdf`, `20250315_20x_cacao_molasses.pdf` (NF-e: 20 L melaço de cacau, R$300)

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Molasses 250 ml bottle | 20 | 250 g | 5.00 kg | 12.143 *(landed)* | 242.86 |
| — | *origin molasses only (raw)* | 20 L | — | — | 2.911 /L | 58.22 *(R$300 nota fiscal)* |

**Shipment total: 5.00 kg · USD 242.86.** Origin raw-material value: USD 58.22.

---

## Shipment 10 — 2025-04-14 · Cacao Husk, 10 kg

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** confirmation `250545517902`, Envelope `F25X26036043`, submitted 2025-04-09, anticipated 2025-04-14
- **Evidence:** `20250419_10kg_cacao_husk.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Husk | 10 kg | 17.7854853 /kg | 177.85 |

**Shipment total: USD 177.85.**

---

## Shipment 11 — 2025-04-14 · Cacao Nibs, 20 kg

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** Envelope `F25X26036004`, submitted 2025-04-09, anticipated 2025-04-14
- **Evidence:** `20250419_20kg_cacao_nibs.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Cacao Nibs (bulk) | 20 kg | 24.61847089 /kg | 492.37 |

**Shipment total: USD 492.37.**

---

## Shipment 12 — 2025-06-06 · Ceremonial Cacao + Cacao Husk/Tea

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** Envelope `F25X26344037`, confirmations `250552273893` (Agroverse Organic Ceremonial Cacao) and `250552273904` (Agroverse Cacao Husk/Tea), submitted 2025-06-02, anticipated 2025-06-06
- **Evidence:** `20250602_fda_prior_notice_cacao_husk_and_ceremonial_bars.pdf`

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | Agroverse Organic Ceremonial Cacao | (n/a — weight not on PN) | — | — |
| 2 | Agroverse Cacao Husk/Tea | (n/a — weight not on PN) | — | — |

**Note:** this PN lists two article names but no weights/counts — unit costs cannot be
multiplied to a total without the manifest quantities (which are not on the PN). Flagged
as a data gap.

---

## Shipment 13 — 2025-06-27 · Ceremonial Cacao Bars + Caramelized Cacao — ⛔ **NEVER SHIPPED (excluded)**

> **Excluded per governor (thread 26215, 2026-09-11):** Black King (Matheus) missed the export
> deadlines — this lot **never shipped**. Retained as a documentary record; **struck from totals.**
> **Corroborated (Rev-7):** this lot has **no row in the `offchain assets in transit` arrival
> register** — no tracking number was ever assigned, consistent with never-shipped.

- **Carrier:** Correios (Entry Type *Mail (Commercial)*)
- **FDA PN:** Envelope `F25X26465487`, confirmations `250554762813` (500 g ceremonial cacao bar) and `250554762824` (Caramelized Cacao Almond Beans), submitted 2025-06-23, anticipated 2025-06-27
- **Evidence:** `20250623_fda_prior_notice_20kg_ceremonial_cacao_5kg_caramelized_cacao.pdf`, `20250617_payment_for_5kg_caramelized_cacao.pdf` (R$725 paid)

| # | Item | Qty | Origin unit cost (USD) | Extended (USD) |
|---|---|---|---|---|
| 1 | 500 g ceremonial cacao bar | 40 (20 kg ÷ 0.5 kg) | 15.6951006 /bar | 627.80 |
| 2 | Caramelized Cacao Almond Beans | 5 kg | 36.7492 /kg **(landed)** ⚠️ *mis-joined — this unit cost is the **AGL10** ledger line, not a Shipment-13 cost (see Rev-7/8 note)* | 183.75 |

**Shipment total: USD 811.55 — ⛔ EXCLUDED (never shipped).** (USD 183.75 of this was a *landed*
figure, not pre-export; origin caramelized value ≈ R$725 = USD 140.69.)

> ⚠️ **Rev-7 re-home:** the `36.7492/kg` landed figure is the **AGL10** value
> (`CP340993299BR`), which **arrived** — it does not belong to this never-shipped lot and is
> **excluded** along with the rest of Shipment 13. **Open question — RESOLVED (Rev-8, governor-confirmed 2026-09-11; answer: NO):** the 5 kg
> caramelized lot did **NOT** physically move on the AGL10 parcel. The arrival register lists mass
> bars only (no caramelized line), so the AGL10 ledger line is a *costing reference only*; the
> Shipment-13 caramelized stock never shipped.

---

## Shipment 14 — 2025-10-09 · Ceremonial Cacao 200 g (+ husk + bean sample)

- **Carrier:** **hand-carried** (Avianca AV560, SF Airport) — Entry Type *Baggage*, NOT Correios
- **FDA PN:** Envelope `F25X27194819`, arrival 2025-10-09 20:45
- **Evidence:** `20251008_fda_prior_notice.pdf`, `20251008_commercial_invoice_cacao.pdf`

Commercial invoice (declared values, USD):

| # | Item | Qty | Declared unit price (USD) | Total (USD) |
|---|---|---|---|---|
| 1 | Ceremonial Cacao 200 g | 10 bags | 5.00 | 50.00 |
| 2 | Cacao Husk (waste) | — | 0.00 | 0.00 |
| 3 | Cacao Beans (sample) | — | 0.00 | 0.00 |

**Declared total: USD 50.00** (husk = waste, beans = sample; FOB Brazil).

---

## Summary — pre-export origin value by shipment

| # | Date | Carrier | Contents | Origin value (USD) |
|---|---|---|---|---|
| 1 | 2024-09-30 | FedEx | 30 × 250 g molasses | 364.29 |
| 2 | 2024-10-04 | Correios | 30 kg nibs | 738.55 |
| 3 | 2024-11-01 | Correios | 20 kg nibs | 492.37 |
| 4 | 2024-11-01 | Correios | 46 × 500 g mass bars | 721.97 |
| 5 | 2024-11-01 | Correios | 88 × 8 oz nibs pouches | 584.32 |
| 6 | 2025-01-24 | Correios | 120 × 8 oz nibs pouches | 796.80 |
| 7 | 2025-01-24 | Correios | 20 kg cacao tea | 273.20 |
| ~~8~~ | ~~2025-02-28~~ | ~~Correios~~ | ~~10 × 500 g ceremonial bars~~ — **never shipped, excluded per governor** | ~~156.95~~ |
| 9 | 2025-03-14 | Correios | 20 × 250 g molasses | 242.86 |
| 10 | 2025-04-14 | Correios | 10 kg cacao husk | 177.85 |
| 11 | 2025-04-14 | Correios | 20 kg nibs | 492.37 |
| 12 | 2025-06-06 | Correios | ceremonial cacao + husk/tea | *(no qty on PN)* |
| ~~13~~ | ~~2025-06-27~~ | ~~Correios~~ | ~~ceremonial bars + caramelized~~ — **never shipped, excluded per governor** | ~~627.80~~ |
| ~~14~~ | ~~2025-10-09~~ | ~~hand-carried~~ | ~~10 × 200 g ceremonial~~ — **excluded per governor** | ~~50.00~~ |

**Total measurable origin value: ≈ USD 4,884.60** across the shipments with quantifiable line items
(excluding #12 [no qty], **#14 hand-carried**, and **#8 / #13 [never shipped]**). Total weight
≈ **182.67 kg**. **Open:** a
governor note that *a ceremonial-cacao shipment from AGL8 did not pass through* is pending
confirmation of the exact manifest line before a row is flagged.

---

## Known gaps

1. **No unit prices on the FDA prior notices.** The prior notices give product + weight/count
   only; unit costs are **joined from the ledger by product name** — the CP-number → prior-notice
   → cost link is inferred, not explicit. Fix: record the Correios tracking number *inside*
   each shipment/prior-notice record.
2. **Shipment 12** lists article names but no weights — no total can be computed.
3. **Molasses & caramelized beans** are only available in the ledger as **landed** (freight-inclusive)
   figures; the true origin (pre-export) cost is shown separately from the Brazilian notas fiscais.
4. Prior notices for shipments 3–5 (all 2024-10-31) were filed as three separate PNs against a
   single 2024-11-01 ship date; treat them as one physical mailing.
5. **Shipments 8 and 13 (2025-02-28, 2025-06-27) never shipped** — Black King (Matheus) missed the
   export deadlines; retained as documentary records but **excluded from every total** (governor,
   thread 26215, 2026-09-11).

## Provenance

- FDA FSVP records: `TrueSightDAO/fda_fsvp/suppliers/black_king/` (11 prior notices + invoices/notas fiscais, read 2026-09-11).
- Ledger: Main Ledger `1GE7PUq-…` — `Currencies` col B, `offchain asset location` col D (read 2026-09-11).
- FX: ledger rate **1 BRL = 0.19405 USD** (`Currencies` row `BRL`).
