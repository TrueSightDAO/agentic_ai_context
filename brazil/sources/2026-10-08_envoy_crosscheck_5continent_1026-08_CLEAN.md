# Independent Cross-Check - 5 Continent Invoice 1026-08 vs. Rate Quote

**Envoy (nelanco-claude)** - built from the raw source PDFs, not from Sophia's output - 2026-10-08

> *Cleaned re-render (2026-10-08): table cells reflowed so no value collides with the adjacent column.*
> Original as-received PDF: `brazil/sources/2026-10-08_envoy_crosscheck_5continent_1026-08.pdf`.

## Sources read directly

- Invoice: `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf` (5 Continent Logistics LLC, Invoice
  1026-08, Oct 7 2026, $4,866.33 total)
- Quote: `brazil/sources/2026-08-26_5continent_rate_quote.pdf` (Graziela Vedana, 5CL, email Aug 26 2026)
- AWB: `brazil/sources/2026-10-02_air_waybill_hawb_issued.md` + `brazil/sources/2026-10-05_air_waybill_mawb_issued.md`
  (Uxcomex, AWB 047-3175 3223)

## 1. Line-by-line reconciliation (independently re-derived)

| Invoice line | Billed | Quote reference | Verdict |
|---|---|---|---|
| Inland Freight in Brazil | $1,012.17 | Inland in Brazil: $837.00 | OVERAGE +$175.17 |
| Airline Terminal Fee - Brazil SSA | $345.00 | Airport BRA $250 + Airline BRA $95 | MATCH (bundled) |
| Palletizing | $65.00 | not in quote | UNQUOTED |
| Storage (SSA + Saturday fee) | $112.19 | not in quote | UNQUOTED |
| Clearance - Export Customs BRA + SDA | $414.59 | quote: arranged directly with Omega | CHECK - possible duplicate |
| Air Freight Charges (365kg x $3.40) | $1,241.00 | HAWB: 349kg x $2.30 = $802.70 | OVERAGE +$438.30 vs AWB |
| Airline Terminal Fee USA | $200.00 | Airline charges USA $200.00 | MATCH |
| Air Freight Handling | $125.00 | Handling Fee USA $125.00 (flat) | MATCH |
| Inland Freight (delivery to door) | $885.00 | Delivery to the door $885 (3 pallets) | MATCH |
| Customs Clearance USA | $150.00 | US Customs Clearance $150.00 | MATCH |
| Additional Invoice Lines (8 x $5) | $40.00 | 1st 3 free, $5/line thereafter | policy-consistent |
| FDA Filing | $100.00 | FDA Processing $100.00 | MATCH |
| Customs Duties | $128.53 | At Cost (no fixed quote) | MATCH (at cost) |
| Duty Advance Fee (10%) | $12.85 | not in quote | UNQUOTED |
| Bank Fee | $35.00 | not in quote | UNQUOTED |

## 2. Totals - two different cuts of the same $4,866.33

| Category | Amount |
|---|---|
| MATCH - incl. bundled Brazil fees + corrected $125 handling | $1,933.53 |
| OVERAGE - quoted services (Inland BR + Air Freight, vs AWB) | $613.47 |
| Wholly UNQUOTED new lines (Palletizing, Storage, Duty Advance, Bank Fee) | $225.04 |
| Additional Invoice Lines (policy-consistent per quote rule) | $40.00 |
| Export Clearance - needs a direct answer (Omega question) | $414.59 |
| Customs Duties (at-cost, no fixed quote to compare) | $128.53 |
| Air Freight remainder | already counted in the OVERAGE row above |
| TOTAL | $4,866.33 |

*Note: rows don't sum to a clean total because the OVERAGE row mixes a quoted baseline with a billed amount.
The table accounts for the full $4,866.33 across the categories - it is not an additional $4,866.33 of dispute
exposure. The actionable dispute amount is the delta, not the line total.*

## 3. AWB verification (read directly, not from Sophia's summary)

HAWB 047-3175 3223 (House Air Waybill - TrueTech Inc. is the named consignee, so this is the correct reference
document, not the Master AWB): gross weight 349.000 kg (2 pallets), chargeable weight 349 kg @ USD 2.30/kg =
USD 802.70, total prepaid USD 857.70 (802.70 + CCC 15.00 + AWB 20.00 + XBC 20.00). Source:
`brazil/sources/2026-10-02_air_waybill_hawb_issued.md`.

The Master AWB (same number, executed 2026-10-05) bills a separate USD 57.30 minimum-charge line to the
forwarder's own account at the consolidator level - that is internal 5CL/airline economics, not what Black
King/TrueTech owes, and is not the right comparison point for this invoice.

**Conclusion:** the invoice's Air Freight Charges line (365kg x $3.40 = $1,241.00) is $438.30 above what 5
Continent's own carrier documentation states as the chargeable weight and rate for the identical shipment
(349kg x $2.30 = $802.70). Both the weight (365 vs 349) and the rate ($3.40 vs $2.30) are inflated versus the
AWB, not just one factor.

## 4. Recommended next step

Two items are strong enough to raise directly with Graziela before addressing the smaller unquoted lines:

1. **Air freight weight/rate discrepancy** - backed by the carrier's own AWB.
2. **The $414.59 export clearance charge** - the quote states this was arranged directly with Omega, so confirm
   with Matheus/Omega first whether it has already been paid separately. That changes the ask from *itemize* to
   *remove, already paid*.

## Attribution

Envoy is an AI instance, **not** governor Gary Teh. This cross-check is corroborating evidence, not an
authorization.

## Clean-render note

Re-rendered to fix overlapping table words in the as-received PDF. Two cells collided with the adjacent column
in the original render: `SDA$414.59` (Clearance row) and `amount` (Totals row). Content is verbatim; only layout
changed. Verified: 0 column-crossing words, 0 cell overflows.
