# Email thread: "RE: Quote Gary / Exportação = NCM 1801.00.00 / Docs" — MAWB revised (rev2)

Source: Gmail thread (Gary's inbox), latest message **Isis Ribeiro (Omega), Tue 6 Oct 2026 16:21 UTC**.
Doc: `exports/2026-10-06_air_waybill_black_king_mawb_047-3175-3223_rev2.pdf` (12 pp, text PDF).
Supersedes the 05/OCT master at `exports/2026-10-05_air_waybill_black_king_mawb_047-3175-3223.pdf`.

## Latest message (Isis, 06/10 16:21) — verbatim + translation

> PT: "Gentileza notar que fizemos uma atualização no MAWB, pois o sistema estava fazendo o cálculo
>  pelo valor mínimo, quando na verdade é por peso, conforme acerto de venda. Segue anexo nova
>  documentação, e já fizemos a troca da documentação com a companhia aérea. E, a previsão de embarque
>  está mantida para hoje à noite."

EN: **"We updated the MAWB, because the system was calculating on the MINIMUM value, when in fact it is
by WEIGHT, per the sale agreement. New documentation attached, and we have already swapped the
documentation with the airline. And the shipment forecast is maintained for TONIGHT."**

⇒ **This is the ORIGIN of the charge discrepancy §5.8 flagged.** It is resolved, not an error:
the first MAWB billed the **2,30 minimum**; the corrected MAWB bills the **full weight charge
(349 kg @ USD 2,30 = USD 802,70)** — matching the HAWB exactly.

## What changed (05/OCT master → 06/OCT rev2)

| Field | OLD (05/OCT file, generated 02/10 17:31) | **NEW rev2 (06/10 13:13)** |
|---|---|---|
| AWB no. | `047-3175-3223` | `047-3175-3223` (unchanged) |
| Consignee | 5 Continent Logistics LLC (EIN 82-4285211) | **unchanged** |
| Flight / route | `TP028` · SSA→SFO | **unchanged** |
| Gross weight | 349,000 kg | **unchanged** |
| HS codes | 1810.00.00 / 1803.10.00 / 2106.90.00 / 1804.00.00 | **unchanged** (⚠ 1810 still there — see §5.7) |
| Rate class | **`MINIMUM`** | **none (weight-rated)** |
| Rate / charge | 2,30 (minimum) | **2.30 /kg** |
| Weight charge | — (minimum applied) | **USD 802,70** |
| **Total prepaid** | **USD 57,30** | **USD 857,70** ✅ == HAWB |
| CC charges (BRL) | 296,87 | **4.443,66** |
| Generated | 02/10/2026 17:31 | **06/10/2026 13:13** |

**Net:** master now mirrors the house **exactly** — `total prepaid USD 857,70` on both. The ~USD 800
"double-count" risk in §5.8 is **cleared**: it was a single charge, once mis-stated at the minimum.

## Still open (unchanged by this revision)

1. **Arrival TIME** for the FDA Prior Notice — still not on the waybill (§5.6 hard blocker).
2. **Final SFO-leg flight no.** — `TP028` is the transatlantic leg (SSA→LIS); historically `TP237` LIS→SFO (§5.6).
3. **HS `1810.00.00`** — persists on the master (§5.7 discrepancy, unfixed).
4. **Consignee note:** master consignee is the **forwarder's US agent** (5 Continent, Manchester NH) —
   expected for a consolidation. The **US importer of record for FDA purposes is still TrueTech Inc.**

## Significance

- Removes the §5.8 charge-reconciliation flag; HAWB and MAWB now agree to the cent.
- Departure forecast **maintained for the night of 06/10** (ETA destination 08/10 per §5.9).
