# 5 Continent - Quote vs Invoice: CORRECTED v2 (2026-10-08)

> **Correction notice.** The v1 reconciliation mis-split **four** lines, because it read only the *text layer* of the
> quote PDF. The quote's actual rate table is an **embedded image on page 2 (916x628 px)**; that page's text layer
> literally renders as *"Error! Filename not specified."* A second agent's independent cross-check (run from the raw
> quote + invoice PDFs) caught this; it is **confirmed correct**. Every figure below was re-read by OCR of the image.
>
> **Raw sources:** quote `brazil/sources/2026-08-26_5continent_rate_quote.pdf` (rate table = embedded image, page 2);
> invoice `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf`.

## The quote's real rate table (recovered from the embedded image)

| Quote line | Rate (USD) |
|---|---|
| Inland in Brazil | 837.00 |
| Airport charges BRA | 250.00 minimum |
| Airline charges BRA | 95.00 |
| Air Freight (+300 kgs) | 1,118.60 |
| Airline charges USA | 200.00 |
| Handling Fee USA | 125.00 |
| Delivery to the door (3 pallets) | 885.00 |
| **Quoted freight total** | **3,510.60** |

Customs terms: US Customs Clearance 150.00 | FDA 100.00 | Duties At Cost | MPF 0.3464% (33.58 min / 651.50 max) |
Bond 6.00/1,000 (100 min) | invoice lines 1st 3 free, 5.00/line after | exam handling 125.00 per exam.

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

Overage *above quote* within the 2,253.17 as-billed bucket = **+297.57** (175.17 + 122.40).

> The second agent framed it slightly differently: it put the 40.00 additional-invoice-lines in UNQUOTED
> (as "policy-consistent") giving MATCH 1,933.53 and UNQUOTED 679.63. Both reconcile to 4,866.33; the 40.00 is the
> only difference and it is quoted-policy-consistent either way.

## Honest correction: what v1 got WRONG

| Line | v1 said | Correct |
|---|---|---|
| Airline Terminal Fee BRA 345.00 | EXTRA | MATCH (= quote 250 + 95) |
| Airline Terminal Fee USA 200.00 | EXTRA | MATCH (= quote 200) |
| Air Freight Handling 125.00 | VERIFY | MATCH (= Handling Fee USA, the flat one) |
| Inland Freight US 885.00 | EXTRA | MATCH (= Delivery to door 885) |

v1's headline "88.8% charged as extra" was **overstated**. Corrected: **~40%** of the bill (1,973.53) matches the
quote exactly; **~298** is overage on two quoted freight lines; **~640** is wholly unquoted. Root cause: v1 read only
- the quote PDF's *text layer* and missed the embedded rate-table image.

## The three issues to raise with 5 Continent

1. **Export clearance 414.59 - ask Matheus/Omega BEFORE disputing.** The quote says clearance "was agreed directly
   with Omega," so 5CL's quote did NOT include it. If Omega was already paid, this line is a **straight duplicate** -
   which changes the ask from "please itemize" to "please remove, already paid."
2. **Two overages on quoted freight** - Inland Brazil billed 1,012.17 vs quoted 837.00 (+175.17); Air Freight billed
   1,241.00 vs quoted flat +300 kgs rate 1,118.60 (+122.40). Ask them to re-bill at the quoted rates. **+297.57.**
3. **Air freight has a THIRD figure.** Quote table 1,118.60 (flat +300 kgs) vs air waybill ~802.70 (349 kg x 2.30, per
   the runbook) vs invoice 1,241.00 (365 kg x 3.40). Reconcile all three to one chargeable basis. (The AWB figure
   comes from the runbook, not a document re-pulled here - verify against the AWB itself.)

## Still open

- **Bond & MPF** have quoted formulas but no distinct invoice line - possibly bundled into "Customs Duties 128.53."
  Ask 5CL to break them out.
- **Handling Fee USA 125.00** now MATCH - but the quote has a *separate* conditional "125.00 per exam." Confirm no exam
  fee is also embedded.
- **Beneficiary mismatch** - header "5 Continent Logistics LLC" vs pay block "5 Continent Alliance." Verify same entity
  before any wire.
- **Trading-company fee (16% + ~4.2%)** - quote premise was "no trading company." Confirm none embedded.
- **Spec drift** - quote 3 pallets / 329 kgs; as-shipped 2 pallets / 349 kg.

## Money rule

Pay-to routing (TD Bank NA, acct 9246418811) is a money move - no payment without an explicit governor command.
