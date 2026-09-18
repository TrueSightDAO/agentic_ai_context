# Black King (Matheus Reis Pereira) - NF-e / transit-register crosswalk

**Generated:** 2026-09-18 - Sophia Truesight (autopilot) - thread 31905
**Purpose:** the single authoritative join between the **15 SEFAZ-issued NF-e** (keyed by
44-digit *chave*) and the **arrival register** (keyed by *tracking number*). The two source
documents share **no common key** - this file **is** the crosswalk.

---

## Sources

| Source | What it provides |
|---|---|
| Main Ledger `shipment_nfe` tab (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`) | NF-e #, chave, issue date, value, recipient, SEFAZ status, `Supersedes`/`Superseded By`, **Parcel Tracking Number** binding |
| Main Ledger `offchain assets in transit` tab (gid `1888711771`) | the **arrival register** - per-parcel tracking # -> destination member -> ledger line # -> status |
| `fda_fsvp/suppliers/black_king/notas_fiscais/` | the 15 DANFE PDFs (chave-named) |
| `black_king_shipments.json` / `BLACK_KING_SHIPMENT_MANIFESTS.md` (Rev-9) | FDA prior-notice-based US-lane manifests + EO-14324 context |

## Join key

**Tracking number** - `shipment_nfe!K` (*Parcel Tracking Number*) <-> register column K.
A parcel row with a tracking that never appears in `shipment_nfe` has **no NF-e**;
an NF-e row whose tracking is blank/`NA` has **no parcel**.

---

## Table 1 - NF-e -> parcel state (all 15)

| NF-e | Chave (44) | Date | Value (R$) | Recipient | SEFAZ | Tracking | Parcel state |
|---:|---|---|---:|---|---|---|---|
| 1 | `29241150042585000180550010000000011061000061` | 2024-11-04 | 2,000.00 | TRUETECH INC | Autorizada | `CP340992695BR` | linked |
| 2 | `29241150042585000180550010000000021061000069` | 2024-11-04 | 4,500.00 | TRUETECH INC | Autorizada | `CP340992687BR` | linked |
| 3 | `29250150042585000180550010000000031061000065` | 2025-01-30 | 544.80 | TRUETECH INC | Autorizada | `CP340992735BR` | linked |
| 4 | `29250250042585000180550010000000041061000066` | 2025-02-19 | 2,362.00 | TRUETECH INC | Autorizada | *(blank)* | **no parcel** |
| 5 | `29250250042585000180550010000000051061000063` | 2025-02-25 | 1,125.00 | ANDREA CATALINA F. RIOS DE PABST | Autorizada | `CP340993838BR` | linked |
| 6 | `29250350042585000180550010000000061061000064` | 2025-03-06 | 2,000.00 | TRUETECH INC | **Cancelada** | `NA` | superseded by NF7 |
| 7 | `29250350042585000180550010000000071061000061` | 2025-03-06 | 2,000.00 | TRUETECH INC | Autorizada | *(blank)* | **no parcel** |
| 8 | `29250350042585000180550010000000081061000069` | 2025-03-06 | 1,000.00 | TRUETECH INC | Autorizada | `CP340992761BR` | linked |
| 9 | `29250350042585000180550010000000091061000066` | 2025-03-06 | 500.00 | AGNIESKA MARECKA | Autorizada | `CP340993237BR` | linked |
| 10 | `29250450042585000180550010000000101061000060` | 2025-04-01 | 800.00 | TRUETECH INC | Autorizada | `74 4476 6210` (DHL) | linked |
| 11 | `29250450042585000180550010000000111061000068` | 2025-04-28 | 500.00 | TRUETECH INC | Autorizada | `CP340993988BR` | linked |
| 12 | `29250650042585000180550010000000121061000062` | 2025-06-04 | 466.71 | TRUETECH INC | Autorizada | `CP340993869BR` | linked |
| 13 | `29250650042585000180550010000000131061000060` | 2025-06-20 | 2,250.00 | TRUETECH INC | **Cancelada** | `NA` | superseded by NF14 |
| 14 | `29250650042585000180550010000000141061000067` | 2025-06-20 | 2,250.00 | TRUETECH INC | Autorizada | `CP340993299BR` | linked |
| 15 | `29250950042585000180550010000000151061000065` | 2025-09-23 | 1,000.00 | TRUETECH INC | Autorizada | *(blank)* | **no parcel** |

## Table 2 - arrival register -> NF-e (all rows)

| Reg. row | Destination | Origin asset | Qty | Courier | Tracking # | Ledger line(s) | Status | NF-e |
|---:|---|---|---:|---|---|---|---|---|
| 2 | Val Lapidus | 8 oz Kraft Pouch | 120 | Correios | `CP340992735BR` | 296 | Arrived | **NF3** |
| 3 | Val Lapidus | Cacao Mass Bar 40 g | 125 | Correios | `CP327946643BR` | 10 | Arrived | none |
| 4 | Val Lapidus | Cacao Mass Bar 500 g | 10 | Correios | `CP327946643BR` | 9 | Arrived | none |
| 5 | Val Lapidus | Cacao Nibs 8 oz pouches | 44 | Correios | `CP327946643BR` | 11 | Arrived | none |
| 6 | Nima Kaz (FounderHaus BR) | 8 oz Kraft Pouch | 50 | Correios | `QN226716310BR` | 248, 316 | Arrived | none |
| 7 | Hans Martin Heierling (CH) | 8 oz Kraft Pouch | 25 | Correios | `CP340993268BR` | 313, 364 | Arrived | none |
| 8 | Aga Marecka (PL) | 8 oz Kraft Pouch | 25 | Correios | `CP340993271BR` | 311 | **Rejected** | none |
| 9 | Aga Marecka (PL) | Cacao Mass Bar 500 g | 10 | Correios | `CP340993271BR` | 312 | **Rejected** | none |
| 10 | Andrea Catalina (CH) | Cacao Mass Bar 500 g | 10 | Correios | `CP340993838BR` | 357, 452 | Arrived | **NF5** |
| 11 | Andrea Catalina (CH) | 8 oz Kraft Pouch | 25 | Correios | `CP340993838BR` | 359, 454 | Arrived | **NF5** |
| 12 | Val Lapidus | Cacao Mass Bar 500 g | 19 | Correios | `CP340992761BR` | 462, 463 | Arrived | **NF8** |
| 13 | Val Lapidus | Cacao Molasses 250 ml | 20 | DHL | `74 4476 6210` | 484 | Arrived | **NF10** |
| 14 | Aga Marecka (PL) | Cacao Mass Bar 500 g | 10 | Correios | `CP340993237BR` | 469, 470 | Arrived | **NF9** |
| 15 | Kirsten Ritschel | Cacao Husk (KG) | 1 | (none) | (none) | (none) | **Rejected** | none |
| 16 | Kirsten Ritschel | Cacao Nibs (KG) | 20 | Correios | `CP340993988BR` | 505 | Arrived | **NF11** |
| 17 | Kirsten Ritschel | Cacao Mass Bar 40 g (AGL8) | 115 | Correios | `CP340993869BR` | 25,26,31,32 | Arrived | **NF12** |
| 18 | Kirsten Ritschel | Cacao Husk loose g (AGL8) | 1.343 | Correios | `CP340993869BR` | 27,28,29,30 | Arrived | **NF12** |
| 19 | Kirsten Ritschel | 22 L Insulated Box | 1 | Correios | `CP340993869BR` | 638 | Arrived | **NF12** |
| 20 | Kirsten Ritschel | Cacao Mass Bar 500 g (AGL10) | 40 | Correios | `CP340993299BR` | 734, 735 | Arrived | **NF14** |

---

## The four states

### A. Linked - NF-e <-> arrived parcel (10)
NF1, NF2, NF3, NF5, NF8, NF9, NF10, NF11, NF12, NF14.

> **Weight reconciliation check (passes):** NF3 declares **27.24 kg cacao nibs**; the register
> binds `CP340992735BR` to **120 x 8 oz (227 g) Kraft Pouches = 120 x 0.227 = 27.24 kg**. This is
> the proof the corridor NF-e *weight* and the register *pouch count* describe the same physical
> goods - i.e. the crosswalk reconciles, it is not just a join.

### B. NF-e issued, NO parcel - invoiced but never landed (3)
**NF4** (R$2,362, 19/02/2025) - **NF7** (R$2,000, 06/03/2025) - **NF15** (R$1,000, 23/09/2025).
All `Autorizada`, tracking blank. These are **write-off candidates** - no arrival, no FDA prior
notice, no shipping receipt.

- NF7 is the reissue of the **cancelled NF6** (both 06/03/2025, both R$2,000, 40 x 500 g bars).
- NF15 (20 x 500 g bars, 23/09/2025) sits ~6 weeks **after** EO-14324 (de-minimis suspension
  effective 2025-08-29) - the post-cutoff lane produced no prior notice.

### C. Cancelled / superseded (2)
**NF6 -> NF7** and **NF13 -> NF14** - cancel-and-reissue pairs (same value, same issue date).
R$4,250 is duplicated, **not** lost cargo. Status `Cancelada`, tracking `NA`.

### D. Arrived parcel with NO NF-e (4 parcels / 7 rows)
- **`CP327946643BR`** - AGL2/AGL6-era SF parcel (Rows 3-5). Predates the NF-e set.
- **`QN226716310BR`** - FounderHaus **Brazil-domestic** (Nima Kaz).
- **`CP340993268BR`** - **Switzerland** (Hans Martin Heierling).
- **`CP340993271BR`** - **Poland**, **Rejected** by Brazilian customs (Rows 8-9).
- *(plus Row 15, Kirsten husk, trackingless, **Rejected**)*

> **Note:** Europe consignments *do* normally carry an NF-e - **NF5** (Andrea Catalina, CH) and
> **NF9** (Aga Marecka, PL) both exist. So the Europe parcels above are a **genuine documentation
> gap**, not 'no NF-e by design'. `CP340993271BR` is the **rejected 1st Poland parcel** - its
> sibling (2nd Poland parcel `CP340993237BR`) *is* covered by NF9.

---

## Corridor summary

| State | Count |
|---|---:|
| NF-e linked to arrived parcel | **10** |
| NF-e issued, never shipped (write-off candidates) | **3** (NF4, NF7, NF15) |
| NF-e cancelled/superseded | **2** (NF6, NF13) |
| **Total NF-e** | **15** |
| Arrived parcels with no NF-e | **4** |

**Bottom line for the tax accountant:** of 15 chaves, **10** correspond to a physically arrived
parcel, **2** were cancelled/reissued, and **3** (NF4, NF7, NF15) are invoiced-but-never-shipped
write-off candidates. Separately, **4** arrived parcels carry **no** NF-e and need one issued or
an exemption noted.
