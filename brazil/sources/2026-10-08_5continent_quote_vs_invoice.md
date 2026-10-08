# 5 Continent - Quote vs Invoice line-by-line analysis

> **Source docs:** quote email `brazil/sources/2026-08-26_5continent_rate_quote.pdf` (Graziela Vedana, 26 Aug 2026);
> invoice `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf` (n 1026-08, 07 Oct 2026).
> **PDFs:** original line-by-line `brazil/sources/2026-10-08_5continent_quote_vs_invoice_analysis.pdf`;
> 3-column comparison `brazil/sources/2026-10-08_5continent_quote_vs_invoice_3col.pdf`.

## Quote (26 Aug 2026)

- "per our WhatsApp conversation, below are the updated rates."
- Premise: *"Matheus having the heat treated pallets and not needing a trading company, he will issue the Nota Fiscal."*
- **Export customs clearance was agreed directly with Omega.** Alternate broker ~ USD 714.00.
- Trading-company fee (if needed): **16.00% over invoice value + local taxes, est. ~4.20% from value.**
- Route: EX Ilheus-BA 45653-310 -> San Francisco CA 94117. **03 pallets @ 100x120x100 cm - 329 kgs.**
- US Customs Clearance **$150.00**.
- Invoice line items: **1st 3 free, $5.00/line thereafter**.
- FDA Processing **$100.00**.
- Bond if applicable: **$6.00 / $1,000 of value plus duty / $100.00 min.**
- Duties: **At Cost**.
- MPF: **0.3464% - $33.58 min // $651.50 max.**
- Exam charges at cost + **$125.00 handling per exam**.

## Spec drift

| | Quote | As shipped |
|---|---|---|
| Pallets | **03** @ 100x120x100 cm | **02** (5.3b/5.7) |
| Weight | **329 kgs** | **349 kg** (5.5/5.7) |

## Three-column comparison

Verdicts: **MATCH** = billed as quoted; **EXTRA** = no quote rate, or contrary to a quote term; **VERIFY** = conditional quote term; **NOT BILLED** = quoted but absent. "n/q" = not quoted.

| Line item | Quoted cost | Actual cost | Match or Extra |
|---|---|---|---|
| US Customs Clearance | 150.00 | 150.00 | MATCH |
| FDA Processing / Filing | 100.00 | 100.00 | MATCH |
| Customs Duties | At Cost | 128.53 | MATCH (at cost) |
| Additional invoice lines (8 x 5) | 1st 3 free, 5.00/line | 40.00 | MATCH (8 chargeable) |
| Air Freight Handling | 125.00 **per exam** | 125.00 | VERIFY (exam or standard?) |
| Air Freight Charges | n/q (AWB: 349 kg @ 2.30 = 802.70) | 1,241.00 | **EXTRA** - 365 kg @ 3.40 |
| Inland Freight in Brazil | n/q | 1,012.17 | **EXTRA** |
| Inland Freight (US) | n/q | 885.00 | **EXTRA** |
| Clearance - Export Customs BRA + SDA | "agreed with Omega" | 414.59 | **EXTRA** (billed anyway) |
| Airline Terminal Fee - Brazil SSA | n/q | 345.00 | **EXTRA** |
| Airline Terminal Fee - USA | n/q | 200.00 | **EXTRA** |
| Storage - SSA + Saturday Airport Fee | n/q | 112.19 | **EXTRA** |
| Palletizing | premise: heat-treated pallets | 65.00 | **EXTRA** |
| Bank Fees | n/q | 35.00 | **EXTRA** |
| Duty Advance Fee (10% of duty) | n/q | 12.85 | **EXTRA** |
| Bond (single-entry, if applicable) | 6.00/1,000 + duty, 100 min | - | NOT BILLED |
| MPF | 0.3464%, 33.58 min | - | NOT BILLED / hidden in Duties? |
| Trading-company fee (if needed) | 16% + ~4.2% taxes | - | NOT BILLED (good) |
| **TOTAL** | (rate card only) | **4,866.33** | - |

## Bucket subtotals

| Bucket | Lines | USD | Share |
|---|---|---|---|
| **MATCH** - quoted and billed as quoted | 4 | **418.53** | 8.6% |
| **VERIFY** - conditional quote term | 1 | **125.00** | 2.6% |
| **EXTRA** - unquoted / contrary to quote | 10 | **4,322.80** | 88.8% |
| **TOTAL invoiced** | 15 | **4,866.33** | 100% |

Only **8.6%** of this bill ($418.53) was actually priced in the quote.

## Key issues

1. **Air freight on a superseded weight** - 365 kg @ $3.40 = $1,241.00 vs AWB 349 kg @ $2.30 = $802.70; 365 ~ superseded Rev 12 gross 364,06. Delta **+$438.30**.
2. **Export clearance $414.59** billed though quote said it was agreed with Omega.
3. **Trading-company fee (16% + ~4.2%) must NOT apply** - confirm none embedded.
4. **MPF missing** (quote $33.58 min) - embedded or omitted?
5. **Bond not invoiced** - confirm continuous bond.
6. **$125 handling is the per-exam rate** - confirm exam vs standard.
7. **Palletizing charged** vs heat-treated-pallet premise; cargo was on a plastic pallet (5.9).
8. **~$3,082 across 9 lines** absent from the quote + request the rate card.
9. **Spec drift** - quote 3 pallets/329 kg vs shipped 2 pallets/349 kg.
10. **Currency basis** - Brazil-side lines billed in USD vs modeled in BRL.

## Money rule

Payment routing (TD Bank, acct `9246418811`) is a money move. No payment without an explicit governor command (sec 0.3).
