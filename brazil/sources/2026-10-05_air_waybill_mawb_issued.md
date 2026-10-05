# Master Air Waybill (MAWB) issued — consolidated, 2026-10-05

**Source:** Uxcomex PDF, `exports/2026-10-05_air_waybill_black_king_mawb_047-3175-3223.pdf`
(12 pages = original + copies; the URL `.../AirWaybillAWB?idProcesso=50505` marks it the **MAWB**
counterpart of the earlier **HAWB** `.../AirWaybillHAWB?idProcesso=50505`). Shared by Gary, thread 10800.

## Header fields

- AWB no. **`047-3175-3223`** (prefix `047` TAP, SSA) — **the same number as the HAWB**
  (same Uxcomex process 50505). Ref `00093-0926TEA`.
- **Shipper: MARITIME AND AIR TRANSPORTS LTDA** — the carrier's agent *itself* (CNPJ 02.992.800/0001-61),
  **not** Black King. Normal for a master: the airline contracts with the consolidator.
- **Consignee: 5 CONTINENT LOGISTICS LLC**, 373 South Willow Street Suite 333, Manchester, NH 03103,
  EIN **`82-4285211`**, TL +1 603 234 3667, **GRAZIELA@5CL.RS**
  — this is **Graziela's / the forwarder's US arm** (§2: Graziera Vedana, `graziela@5cl.rs`).
- Issuing carrier's agent: same Maritime & Air Transports Ltda. Signed **Helesson Bastos**.
- **Executed on `05/OCT/2026`** at SALVADOR (the HAWB's date box was blank — this fills it).

## Routing & cargo

- Departure **SALVADOR (SSA)** → **SAN FRANCISCO (SFO)**; requested flight **`TP028`** (TAP).
- Handling: **"CONSOLIDATED CARGO AS PER ATTACHED CARGO MANIFEST"**;
  nature of goods: **"CONSOLIDATED CARGO AS PER ATTACHED MANIFEST ON HAWB"**.
- **2 pieces / gross `349,000 kg`** — matches Rev 15 and the HAWB.
- HS on face: `1810.00.00 / 1803.10.00 / 2106.90.00 / 1804.00.00` (same list as the HAWB).
- DU-E `26BR001795400-0`; RUC `6BR50042585200000000000000001987510`.

## Charges (⚠️ differs from the HAWB)

- FX: **USD 1,00 = BRL 5,180900** (the HAWB printed 0,000000).
- Weight charge: **349,00 MINIMUM** rate class @ **USD 2,30** → **USD 2,30**
  (i.e. the minimum-charge rule applied at master level).
- Total prepaid: **USD 57,30** (`2,30` weight + CCC 15,00 + AWB 20,00 + XBC 20,00).
- **vs HAWB total prepaid USD 857,70** (weight `802,70` = 349 kg @ 2,30 + same 3 charges of 35,00).
  → the master bills a nominal minimum; the house bills the full weight charge.
  **Flag for reconciliation** (consolidation economics / account settlement) — see §5.8.

## Significance

1. The shipment is a **CONSOLIDATION** — Black King's cargo rides in 5 Continent Logistics'
   master consignment; the airline delivers to the **forwarder's US agent**, who then delivers
   to the **importer of record (TrueTech)**.
2. **MAWB consignee ≠ HAWB consignee** — MAWB → 5 Continent Logistics LLC; HAWB → TrueTech Inc.
   Expected for a consolidated air shipment.
3. **Both waybills carry AWB `047-3175-3223`** → for the **FDA Prior Notice** cite **`047-3175-3223`**.
4. **Executed 05/OCT/2026** — the doc pair now has a hard date.

## Status

- ✅ HAWB issued (`047-3175 3223`)
- ✅ **MAWB issued** (`047-3175-3223`, consolidated, executed 05/OCT/2026)
- ✅ Gross 349 kg agreed at both levels
- ✅ DU-E registered
- ⬜ Flight **arrival date** (for the FDA PN 4h/15-day window) → ⬜ FDA PN filed (Iolanda)
