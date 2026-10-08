# 5 Continent - Quote vs Invoice: FINAL v3, AWB-verified (2026-10-08)

> **Supersedes v1** (mis-split; read only the quote's text layer) **and v2** (corrected; recovered the
> embedded rate table). **v3 adds the carrier's own waybill as a third independent check on the air-freight line.**
>
> **Raw sources:** quote `brazil/sources/2026-08-26_5continent_rate_quote.pdf` (rate table = embedded image, p.2);
> invoice `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf`; HAWB
> `brazil/sources/2026-10-02_air_waybill_hawb_issued.md`; MAWB `brazil/sources/2026-10-05_air_waybill_mawb_issued.md`.

## Air freight - now triangulated from three independent sources

| Source | Basis | Amount (USD) |
|---|---|---|
| Quote rate table (embedded image, quote p.2) | flat +300 kgs | 1,118.60 |
| Carrier HAWB 047-3175 3223 (gross 349,000 kg, 2 pallets) | 349 kg @ 2.30/kg | 802.70 |
| 5 Continent invoice 1026-08 | 365 kg @ 3.40/kg | 1,241.00 |

The invoice is **above both**: **+122.40** over 5 Continent's own quoted rate, and **+438.30** over what the
carrier itself documents as the chargeable freight. **Both** the weight (365 vs 349 kg) and the per-kg rate
(3.40 vs 2.30) are inflated versus the carrier's own paperwork - same AWB number, same 2 pallets.

**Which figure is the contractual ask:** the forwarder's own quote (1,118.60) is the price 5 Continent committed
to; the HAWB (802.70) exposes their underlying cost/margin. The clean demand is *"re-bill to your quoted rate."*
The carrier figure is supporting evidence that the invoice rate is inflated, not a separate claim.

**MAWB caveat:** the master waybill bills a nominal minimum (2.30 / total 57.30) - that is consolidator-to-airline
settlement economics, **not** what TrueTech owes. Only the HAWB is the right comparator, because the HAWB consignee
is **TrueTech Inc** (the MAWB consignee is 5 Continent Logistics itself).

## Corrected line-by-line: Quoted | Actual | Verdict

| Line item | Quoted | Actual | Verdict |
|---|---|---|---|
| Inland Freight in Brazil | 837.00 | 1,012.17 | OVERAGE (+175.17) |
| Airline Terminal Fee - Brazil SSA | 345.00 (= 250 + 95) | 345.00 | MATCH (bundled) |
| Palletizing | - | 65.00 | UNQUOTED |
| Storage - SSA + Saturday | - | 112.19 | UNQUOTED |
| Clearance - Export Customs BRA + SDA | - (agreed w/ Omega) | 414.59 | UNQUOTED / possible DUPLICATE |
| Air Freight Charges | 1,118.60 (+300 kgs) | 1,241.00 | OVERAGE (+122.40) |
| Airline Terminal Fee USA | 200.00 | 200.00 | MATCH |
| Air Freight Handling | 125.00 (Handling Fee USA) | 125.00 | MATCH |
| Inland Freight (US) | 885.00 (Delivery to door) | 885.00 | MATCH |
| Customs Clearance USA | 150.00 | 150.00 | MATCH |
| Additional Invoice Lines | 1st 3 free, 5.00/line | 40.00 | MATCH (quoted policy) |
| FDA Filing | 100.00 | 100.00 | MATCH |
| Customs Duties | At cost | 128.53 | MATCH (at cost) |
| Duty Advance Fee | - | 12.85 | UNQUOTED |
| Bank Fees | - | 35.00 | UNQUOTED |
| **TOTAL** | | **4,866.33** | |

## The three buckets (reconcile to the cent)

| Bucket | Amount | Composition |
|---|---|---|
| MATCH - quoted & billed exactly | **1,973.53** | 150 + 100 + 128.53 + 200 + 345 + 125 + 885 + 40 |
| OVERAGE - quoted line billed above rate | **2,253.17** as billed | Inland Brazil 1,012.17 (vs 837) + Air freight 1,241.00 (vs 1,118.60) |
| UNQUOTED - no quote rate at all | **639.63** | Palletizing 65 + Storage 112.19 + Export clearance 414.59 + Duty advance 12.85 + Bank 35 |
| **TOTAL** | **4,866.33** | reconciles |

Overage *above quote* within the as-billed bucket = **+297.57** (175.17 + 122.40).

## Priority: two asks worth a direct reply to Graziela

1. **Air freight - the strongest line item.** Not "unquoted"; it is billed **above 5 Continent's own carrier
   documentation.** Invoice 1,241.00 (365 kg @ 3.40) vs quoted flat 1,118.60 vs carrier HAWB 802.70 (349 kg @ 2.30).
   Ask them to **re-bill to the quoted 1,118.60** and explain the 365 kg / 3.40 basis. **+122.40 minimum; carrier
   delta +438.30.**
2. **Export clearance 414.59 - confirm with Omega BEFORE disputing.** The quote says clearance "was agreed directly
   with Omega," i.e. it was NOT in 5 Continent's quote. If Omega was already paid, this line is a **straight
   duplicate** - the ask becomes *"please remove, already paid,"* not *"please itemize."*

## Lower priority

- **Inland Freight Brazil +175.17** - billed 1,012.17 vs quoted 837.00. Same "re-bill to quote" ask.
- **Bond & MPF** - quoted formulas but no distinct invoice line; possibly bundled into "Customs Duties 128.53."
  Ask 5CL to break them out.
- **Handling Fee USA 125.00** - MATCH, but the quote has a *separate* conditional "125.00 per exam." Confirm no exam
  fee is also embedded.
- **Beneficiary mismatch** - header "5 Continent Logistics LLC" vs pay block "5 Continent Alliance." Verify same entity
  before any wire.
- **Trading-company fee (16% + ~4.2%)** - quote premise was "no trading company." Confirm none embedded.
- **Spec drift** - quote 3 pallets / 329 kgs; as-shipped 2 pallets / 349 kg.

## Money rule

Pay-to routing (TD Bank NA, acct 9246418811) is a money move - no payment without an explicit governor command.
