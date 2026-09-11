# Correios shipments index

Canonical index of **Correios (Brazil Post)** shipments in the Agroverse / TrueSight DAO
supply chain — primarily the **Matheus Reis / Black King (Ilhéus, BA)** export corridor.

Derived from the three authoritative sources:

1. **`Currencies` tab of the Main Ledger** (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`)
   — Correios tracking numbers (`CP……BR`, `QN……BR`) are embedded in product/currency names.
2. **`fda_fsvp/suppliers/black_king/`** — shipping receipts + FDA prior notices per shipment.
3. **`offchain assets in transit` tab of the Main Ledger** (gid `1888711771`) — the **arrival
   register**: per-parcel tracking # → destination member → ledger line # → **status**. This is
   the join key between a tracking number and its ledger line, and the authoritative record of
   which parcels actually **arrived**. A parcel with no row here never landed.

Machine-readable mirrors: `correios_shipments.json` and `in_transit_register.json`.

Convention references: `WORKSPACE_CONTEXT.md` §4, `LEDGER_CONVERSION_AND_REPACKAGING.md`,
and the FSVP shipment-documentation runbook (Correios `CP…BR` tracking screenshots are
required pack item #6).

## Tracking numbers

| Tracking # | Products on the parcel | Destination (inferred) | Evidence in `fda_fsvp` | Post-arrival holders |
|---|---|---|---|---|
| `CP327946643BR` | Cacao Mass Bar 40g / 500g / loose g; Cacao Nibs 8 oz kraft pouches; ceremonial pouch + mass bar | US (AGL2 / AGL6 era) | — (earliest; predates the FSVP receipt set) | AGL2 / AGL6 |
| `CP340992130BR` | 8 Ounce Package Kraft Pouch | US | — | — |
| `CP340992687BR` | 8 oz kraft pouch; Cacao Mass Bar 500g / 50g / loose g; ceremonial + mass bar | US (San Francisco) | `20241111_shipping_CP340992687BR.jpeg` + `…_payment_receipt.jpeg` | Miss Tomato – Asad (10); Shannon Barlow – Ponderosa (1) |
| `CP340992695BR` | 8 oz kraft pouch + v2 bags; Cacao Nibs (KG) | US | `20241111_shipping_CP340992695BR.jpeg` + `…_payment_receipt.jpeg` | Edge and Node (3); Tess Walkowski (4) |
| `CP340992735BR` | 8 oz kraft pouches; repackaged ceremonial + 81% dark-chocolate-bar lines | US (San Francisco) | tokenized batch `2024OSCAR_20250711_NIBS_21` (see `ADVISORY_SNAPSHOT.md`) | Edge and Node (2); Elinor Janelle (1); Kirsten Ritschel (2); Rune Shields (3); Shannon Barlow – Ponderosa (5) |
| `CP340992761BR` | Cacao Mass Bar 500g; ceremonial pouch + mass bar | San Francisco | — | Val Lapidus (19) **✅ arrived** (register line 462/463) |
| `CP340993237BR` | Cacao Mass Bar 500g | Poland | — | Aga Marecka **✅ arrived** — **2nd Poland parcel** (register line 469/470) |
| `CP340993268BR` | 8 oz kraft pouches | Switzerland | — | Hans Martin Heierling (25) **✅ arrived** (register line 313/364) |
| `CP340993271BR` | 8 oz kraft pouches; Cacao Mass Bar 500g | Poland | — | — **⛔ REJECTED by Brazilian customs (2025-02-28 → 2025-03-01) — never arrived** (1st Poland parcel; no arrival-register row) |
| `CP340993299BR` | Cacao Mass Bar 500g; Caramelized Cacao Beans; ceremonial lines | San Francisco (AGL10) | — | SF retail network (40 × 500 g mass bars) **✅ arrived** (register line 734/735) |
| `CP340993838BR` | 8 oz kraft pouches; Cacao Mass Bar 500g / loose g | Zurich | — | Andrea Catalina Falcon Rios De Pabst (16 + 7 + 200 g); Yasmin (40 g) **✅ arrived** (register line 357/452, 359/454) |
| `CP340993869BR` | Cacao Mass Bar 40g; Cacao Tea loose g; ceremonial pouch + mass bar | San Francisco (AGL8) | — | AGL8 retail; Kirsten Ritschel **✅ arrived** (register line 638) |
| `CP340993988BR` | Cacao Mass / Husk / Nibs (KG); 81% Dark Chocolate Bar 50g; ceremonial Oscar lines | San Francisco (Oscar 2024 batch) | — | SF retail (Kirsten 20251107 / 20251124 / 20251211) — register line 505 **✅ arrived** |
| `QN226716310BR` | 8 Ounce Package Kraft Pouch | FounderHaus Brazil | — | Nima Kaz (50) **✅ arrived** (register line 248/316) |

**14 distinct Correios tracking numbers.** Plus a shipping-supply ledger line:
`Correios packing box to hold cacao nibs 20kg`.

## Arrival register — `offchain assets in transit` tab (gid `1888711771`)

The arrival-side counterpart to the table above. Each row is one parcel-line with the
**tracking number joined to its ledger line number and delivery status**. Read 2026-09-11.
Machine mirror: `in_transit_register.json`. Every row below reads **"Arrived at Destination."**

| Destination member | Origin asset | Qty | Courier | Tracking # | Ledger line(s) | Status |
|---|---|---|---|---|---|---|
| Val Lapidus | 8 Ounce Package Kraft Pouch | 120 | Correios | `CP340992735BR` | 296 | Arrived at Destination |
| Nima Kaz | 8 Ounce Package Kraft Pouch | 50 | Correios | `QN226716310BR` | 248, 316 | Arrived at Destination |
| Hans Martin Heierling | 8 Ounce Package Kraft Pouch | 25 | Correios | `CP340993268BR` | 313, 364 | Arrived at Destination |
| Andrea Catalina Falcon Rios De Pabst | Cacao Mass Bar 500 g | 10 | Correios | `CP340993838BR` | 357, 452 | Arrived at Destination |
| Andrea Catalina Falcon Rios De Pabst | 8 Ounce Package Kraft Pouch | 25 | Correios | `CP340993838BR` | 359, 454 | Arrived at Destination |
| Val Lapidus | Cacao Mass Bar 500 g | 19 | Correios | `CP340992761BR` | 462, 463 | Arrived at Destination |
| Val Lapidus | Cacao Molasses 250 ml | 20 | **DHL** | `74 4476 6210` | 484 | Arrived at Destination |
| Aga Marecka | Cacao Mass Bar 500 g | 10 | Correios | `CP340993237BR` | 469, 470 | Arrived at Destination |
| Kirsten Ritschel | Cacao Nibs (KG) | 20 | Correios | `CP340993988BR` | 505 | Arrived at Destination |
| Kirsten Ritschel | Cacao Mass Bar 40 g (AGL8) | 115 | Correios | `CP340993869BR` | — | Arrived at Destination |
| Kirsten Ritschel | Cacao Husk loose g (AGL8) | 1.343 | Correios | `CP340993869BR` | — | Arrived at Destination |
| Kirsten Ritschel | 22 Litres Insulated Box | 1 | Correios | `CP340993869BR` | 638 | Arrived at Destination |
| Kirsten Ritschel | Cacao Mass Bar 500 g (AGL10) | 40 | Correios | `CP340993299BR` | 734, 735 | Arrived at Destination |

> **Note (2026-09-11):** `CP340993299BR` is the **AGL10** parcel. The ledger currency line
> `Caramelized Cacao Beans (KG) + CP340993299BR San Francisco AGL10` attaches the *landed*
> caramelized unit cost to **this** parcel — not to a Black King manifest shipment.

## FDA FSVP records for Black King (Matheus)

The `suppliers/black_king/` folder holds the shipping receipts and FDA prior notices.
Prior notices represent a US-bound import, but are keyed by **date + weight + product**,
not by Correios tracking number.

### Shipping / transport receipts

| File | What it is |
|---|---|
| `20240925_fedex_shipping.jpeg` | FedEx parcel — **not** Correios |
| `20241004_emelin_30kg_carreois_transport_receipt.jpeg` (+ `_english`) | 30 kg Correios transport receipt |
| `20241111_shipping_CP340992687BR.jpeg` (+ `_payment_receipt`) | Correios receipt + payment |
| `20241111_shipping_CP340992695BR.jpeg` (+ `_payment_receipt`) | Correios receipt + payment |

### FDA prior notices (one per US-bound import batch)

| File | Weight / product |
|---|---|
| `20240924_fda_prior_notice_30_bottles_cacao_molasses.pdf` | 30 bottles cacao molasses (FedEx, AGL5) |
| `20241003_30kg_cacao_nibs_webentry_prior_notice.pdf` | 30 kg cacao nibs |
| `20241031_fda_fsvp_20kg_cacao_nibs_prior_notice.pdf` | 20 kg cacao nibs |
| `20241031_fda_fsvp_23kg_cacao_liquor_prior_notice.pdf` | 23 kg cacao liquor |
| `20241031_fda_fsvp_88bags_cacao_nibs_prior_notice.pdf` | 88 bags cacao nibs |
| `20250228_fda_prior_notice_10_bars_ceremonial_cacao_500grams.pdf` | 10 bars ceremonial cacao 500 g — **never shipped (excluded, manifest Rev-6)** |
| `20250309_fda_prior_notice_20_bottles_of_cacao_molasses.pdf` | 20 bottles cacao molasses |
| `20250602_fda_prior_notice_cacao_husk_and_ceremonial_bars.pdf` | cacao husk + ceremonial bars |
| `20250623_fda_prior_notice_20kg_ceremonial_cacao_5kg_caramelized_cacao.pdf` | 20 kg ceremonial + 5 kg caramelized — **never shipped (excluded, manifest Rev-6)** |
| `20251008_fda_prior_notice.pdf` | cacao (commercial invoice 20251008) — hand-carried, not Correios |

## Known gap

**Closed (2026-09-11):** the **tracking-number ↔ ledger-line join** is now explicit — it is
recorded in the `offchain assets in transit` tab and mirrored in the *Arrival register* section
above + `in_transit_register.json`.

**Still open:** the **prior-notice ↔ tracking-number** join. Neither the ledger nor `fda_fsvp`
stores them together, so linking a specific FDA prior notice to a specific parcel remains
**inferred from date + weight + product**. A future improvement is to record the Correios
tracking number *inside* each prior-notice record (or a shared shipment record) so the link is
explicit. Filed as a follow-up in `OPEN_FOLLOWUPS.md` when raised.

## Not Correios (for the avoidance of doubt)

- **Bulk freight:** AGL4 (300 kg), AGL8 (330 kg), AGL13 (Santos), AGL14 — air/ocean freight (Omega / Mega Services).
- **FedEx:** AGL5 molasses (30 bottles).
- **Hand-carried:** AGL0, AGL1.

## Provenance

- `Currencies` + `offchain asset location` + `offchain assets in transit` tabs, Main Ledger `1GE7PUq-…` (read 2026-09-11).
- `fda_fsvp/suppliers/black_king/entity.json` + folder listing.
- `agroverse-inventory/currencies.json` (machine mirror of the Currencies tab).
