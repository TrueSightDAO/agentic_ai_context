# 5 Continent - Quote vs Invoice: RE-VERIFIED + consistency check (2026-10-08)

> **Purpose:** independent re-check of the autopilot's filed reconciliation (Graziela's 26-Aug rate quote vs
> invoice n 1026-08, USD 4,866.33). Every figure was re-added from the raw invoice so this artifact can be
> diffed against any other agent's output.
>
> **Raw sources:** quote `brazil/sources/2026-08-26_5continent_rate_quote.pdf`;
> invoice `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf`.

## Quote terms (benchmark)

- Premise: heat-treated pallets + **no trading company**; Matheus issues the Nota Fiscal.
- **Export customs clearance agreed directly with Omega** (alternate broker ~USD 714.00).
- Trading-company fee if used: **16.00% over invoice value + ~4.20% local taxes**.
- Route: EX Ilheus-BA 45653-310 -> San Francisco CA 94117. **03 pallets @ 100x120x100 cm - 329 kgs.**
- US Customs Clearance **$150.00** | FDA Processing **$100.00** | Duties **At Cost** | MPF **0.3464% ($33.58 min / $651.50 max)** | Bond **$6.00/$1,000 + duty ($100 min)** | invoice lines **1st 3 free, $5.00/line after** | exam handling **$125.00/exam**.

## Line-by-line - Quoted | Actual | Match or Extra

| Line item | Quoted cost | Actual cost | Match or Extra |
|---|---|---|---|
| US Customs Clearance | 150.00 | 150.00 | MATCH |
| FDA Processing / Filing | 100.00 | 100.00 | MATCH |
| Customs Duties | At cost | 128.53 | MATCH |
| Add'l invoice lines (8 x 5.00) | 1st 3 free, then 5.00/line | 40.00 | MATCH |
| Air Freight Handling | 125.00 (per exam) | 125.00 | VERIFY - exam, or standard? |
| Air Freight Charges | n/q (AWB 349 kg x 2.30 = 802.70) | 1,241.00 | **EXTRA** - 365 kg x 3.40 |
| Inland Freight in Brazil | n/q | 1,012.17 | **EXTRA** |
| Inland Freight (US) | n/q | 885.00 | **EXTRA** |
| Clearance - Export Customs BRA + SDA | "agreed with Omega" | 414.59 | **EXTRA** |
| Airline Terminal Fee - Brazil SSA | n/q | 345.00 | **EXTRA** |
| Airline Terminal Fee - USA | n/q | 200.00 | **EXTRA** |
| Storage - SSA + Saturday fee | n/q | 112.19 | **EXTRA** |
| Palletizing | premise: heat-treated pallets | 65.00 | **EXTRA** |
| Bank Fees | n/q | 35.00 | **EXTRA** |
| Duty Advance Fee | n/q | 12.85 | **EXTRA** |
| **TOTAL INVOICED** | - | **4,866.33** | - |
| **- of which MATCH** | 418.53 | **418.53** | quoted & billed as quoted |
| **- of which VERIFY** | 125.00 | **125.00** | conditional term |
| **- CHARGED AS EXTRA** | **0.00 quoted** | **4,322.80** | **88.8% of the bill is extra** |

\* "n/q" = no rate for that line was in the quote email.

## Consistency check - all figures re-added

- Sum of the 15 invoice lines = **4,866.33** -> equals invoice total OK
- MATCH 418.53 + VERIFY 125.00 + EXTRA 4,322.80 = **4,866.33** OK
- Air freight 365 x 3.40 = **1,241.00** OK | AWB 349 x 2.30 = **802.70** OK | delta **438.30** OK
- Extra share 4,322.80 / 4,866.33 = **88.8%** OK

## Spec drift - quote vs as-shipped

| | Quote | As shipped |
|---|---|---|
| Pallets | 03 | 02 |
| Weight | 329 kgs | 349 kg |

## Quoted, but NOT billed

| Item | Quote term | Invoice |
|---|---|---|
| Bond (single-entry) | 6.00/1,000 + duty, 100 min | not billed |
| MPF | 0.3464%, 33.58 min | not billed (inside Duties?) |
| Trading-company fee | 16% + ~4.2% | not billed (good) |

## Key issues to raise with 5 Continent

1. **Air freight keyed to a superseded weight** - invoice bills 365 kg; AWB/scale is 349 kg. Rate also differs (3.40 vs 2.30/kg). **+438.30.**
2. **Export clearance 414.59 billed** although the quote said Omega did it directly.
3. **Trading-company fee (16% + ~4.2%) must NOT appear** - confirm none is embedded.
4. **MPF** (33.58 min) not shown - is it inside "Customs Duties 128.53"?
5. **Bond** not invoiced - confirm a continuous bond is on file.
6. **"Air Freight Handling 125.00"** - the quote's $125 is a *per-exam* charge; confirm whether an exam occurred.
7. **~3,082 across 9 lines has no quote rate** - request the underlying rate card.
8. **Beneficiary name mismatch** - header "5 Continent Logistics LLC" vs payment block "5 Continent Alliance"; verify same legal entity before wiring.
9. **Currency basis** - the five "in Brazil" lines are billed in USD though modelled in BRL; confirm FX basis/date.

## Cross-agent reconciliation status

- This artifact re-derives every figure from the raw invoice and states the arithmetic explicitly.
- **No handoff from the nelanco agent was present in the autopilot mailbox at the time of writing** (checked). If another agent's line items are posted, diff them against the table above - all rows are stated to 2 decimals and their sum is exact, so any discrepancy will localise to a single line.

## Money rule

Pay-to routing (TD Bank NA, acct `9246418811`) is a money move - no payment without an explicit governor command.
