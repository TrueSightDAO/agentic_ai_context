# Forwarder Invoice Comparison - 2023 vs 2026, SSA to SFO Cacao

**Same lane, same carrier, same forwarder principal.** Line-item comparison of the two air-freight
invoices for cacao shipments Salvador (SSA) to San Francisco (SFO).

## The two shipments

| | 2023 shipment | 2026 shipment |
|---|---|---|
| Cargo | 100 kg cacao nibs | 9 articles cacao |
| Shipper | Coopercabruca | Black King |
| Consignee | TrueTech Inc | TrueTech Inc |
| Flight | TAP 047-04136716 | TAP 047-3175 3223 |
| Routing | SSA to LIS to SFO | SSA to LIS to SFO |
| Volume | 8 volumes | 2 pallets |
| Gross weight | 104 kg | 349 kg |
| Forwarder | Seacoast Logistics Inc | 5 Continent Logistics LLC |
| Invoice | #102000607-1 | #1026-08 |
| Invoice date | 17 Nov 2023 | 07 Oct 2026 |
| **Invoice total** | **$521.03** | **$4,866.33** |

Same human on both: Graziela Vedana (Seacoast Logistics in 2023, 5 Continent in 2026).

## Line-by-line comparison

| Charge | 2023 (Seacoast) | 2026 (5 Continent) | Status |
|---|---|---|---|
| Customs clearance US | $125.00 | $150.00 | Same line, higher |
| Import / freight handling | $95.00 | $125.00 | Same line, higher |
| FDA processing | $100.00 | $100.00 | Unchanged |
| Duties and taxes | $2.53 | $128.53 | At cost (scales) |
| Airline terminal fee (US) | $198.50 | $200.00 | Unchanged |
| Air freight | separate | $1,241.00 | See note |
| Inland freight Brazil | separate | $1,012.17 | NEW on invoice |
| Airline terminal fee (Brazil SSA) | absent | $345.00 | NEW |
| Export clearance BRA + SDA | absent | $414.59 | NEW |
| Palletizing | absent | $65.00 | NEW |
| Storage (SSA + Saturday) | absent | $112.19 | NEW |
| Door delivery (inland US) | absent | $885.00 | NEW |
| Additional invoice lines (8 x $5) | absent | $40.00 | NEW |
| Duty advance fee (10%) | absent | $12.85 | NEW |
| Bank fee | absent | $35.00 | NEW |

## The answer: 9 charges new in 2026

These lines appear on the 2026 invoice and had **no counterpart line** on the 2023 invoice:

1. **Inland freight in Brazil** - $1,012.17
2. **Airline terminal fee, Brazil SSA** - $345.00
3. **Clearance, export customs BRA + SDA** - $414.59
4. **Palletizing** - $65.00
5. **Storage (SSA + Saturday fee)** - $112.19
6. **Inland freight, delivery to door** - $885.00
7. **Additional invoice lines (8 x $5)** - $40.00
8. **Duty advance fee (10%)** - $12.85
9. **Bank fee** - $35.00

**New-line subtotal: $2,921.80.**

## The structural change

In 2023 the forwarder invoice was **US-side only** - five lines: customs clearance, import handling,
FDA processing, duties, and the US airline terminal fee. The Brazil-side export work existed but was
**billed separately** (an Omega "numerario" of R$4,000 plus a R$864.15 transport CT-e), so it never
appeared on the forwarder invoice.

In 2026 the same forwarder invoice is **end-to-end**: it absorbs the entire Brazil-side export chain
(inland freight, Brazil terminal fee, export clearance, palletizing, storage) plus a door-delivery leg
and three new administrative fees (per-line billing, duty advance, bank fee).

## Two things to weigh, not assume

- **Size is not the explanation for most of this.** The 2026 shipment is about 3.4x the weight
  (349 vs 104 kg). Weight-scaled lines (air freight, duties) move with that. But palletizing, storage,
  the per-line fee, the duty advance fee, and the bank fee are **flat or structural** - they are not
  weight-scaled, so shipment size does not account for them.
- **Some "new" items are genuinely new scope, not new charges for old scope.** Door delivery and export
  clearance were not done by the forwarder in 2023, so charging for them is defensible in principle. The
  question is whether the **amounts and the add-ons** (storage, per-line fee, duty advance, bank fee) are
  reasonable and were agreed.

## Caveat on scope

This compares **forwarder invoices**. It is not a full landed-cost comparison: 2023's Brazil-side costs
were real but sat on a separate invoice. A true like-for-like landed cost needs the 2023 Omega numerario
and CT-e brought into scope. This document answers the specific question asked: *which line items are on
the 2026 invoice that were not on the 2023 one.*

## Sources

- 2023 invoice: `fda_fsvp/suppliers/coopercabruca/20231117_payment_for_customs_clearance_taxes_airport_handling.pdf`
  (Seacoast Logistics Inc #102000607-1)
- 2023 flight/waybill: `fda_fsvp/suppliers/coopercabruca/20231118_100KG_airway_bill_for_portugese_airlines_tap.pdf`
  (AWB 047-04136716, 8 vol / 104 kg)
- 2023 Brazil-side: `20231109_100KG_flight_from_salvador_to_sfo.pdf` (Omega numerario R$4,000),
  `20231109_100KG_transport_from_Coopercabruca_to_Salvador_invoice.pdf` (CT-e R$864.15)
- 2026 invoice: `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf` (5 Continent #1026-08)
- 2026 waybill: `brazil/sources/2026-10-02_air_waybill_hawb_issued.md` (AWB 047-3175 3223, 349 kg)

Prepared by Sophia (TrueSight DAO Autopilot), 2026-10-09. No payment initiated.
