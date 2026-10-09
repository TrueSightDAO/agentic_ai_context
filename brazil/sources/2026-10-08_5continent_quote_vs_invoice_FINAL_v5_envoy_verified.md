# 5 Continent - Quote vs Invoice: FINAL v5 (Envoy-verified, 2026-10-08)

> **Invoice 1026-08 - Freight EXW Ilh\u00e9us \u2192 San Francisco - 2 pallets / 349 kg**
>
> **Consolidated & cross-verified.** Supersedes v1 (mis-split; read only the quote's text layer), v2 (corrected;
> recovered the embedded rate table), v3 (air freight AWB-verified), v4 (consolidated line-by-line + variance
> bridge). **v5 adds the independent cross-check by Envoy (nelanco-claude), reconciled line-by-line.**

## 0. Independent verification - now two passes, not one

| Pass | Who | What it establishes |
|---|---|---|
| FACTS | **Envoy (nelanco-claude)** | Re-read the raw invoice, quote and AWB PDFs independently - corroborates every line figure |
| PARTITION | **This document** | Authoritative split of the full invoice; sums to the cent, no double-count |

**Verdict: the two agree to the cent once bucketing is normalised.** Envoy is an AI instance, **not** governor Gary
Teh - its cross-check is corroborating evidence, not an authorization.

## 1. The headline

The quote is **$3,510.60** and the invoice is **$4,866.33** - but these are **not the same kind of number**:
- **$3,510.60** = 5 Continent's **freight rate table only** (7 logistics lines)
- **$4,866.33** = the **all-in landed cost** (freight + customs + duties + fees), 15 lines

The quote contained a **separate** "Customs clearance charges" section (US clearance, FDA, duties, bond, MPF, line
fees) that is **not** part of the $3,510.60. Comparing the two directly mixes a freight subtotal with a full landed
bill - which is why the gap resists a one-line "they overcharged" answer.

## 2. Line-by-line: Quoted | Actual | Verdict

| Line item | Quoted | Actual | Verdict |
|---|---|---|---|
| Inland Freight in Brazil | 837.00 | 1,012.17 | OVERAGE (+175.17) |
| Airline Terminal Fee - Brazil SSA | 345.00 (= 250 + 95) | 345.00 | MATCH (bundled) |
| Palletizing | - | 65.00 | UNQUOTED |
| Storage - SSA + Saturday | - | 112.19 | UNQUOTED |
| Clearance - Export Customs BRA + SDA | (agreed w/ Omega) | 414.59 | UNQUOTED / possible DUPLICATE |
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

## 3. The three buckets (reconcile to the cent)

| Bucket | Amount | Composition |
|---|---|---|
| MATCH - quoted & billed exactly | **1,973.53** | 150 + 100 + 128.53 + 200 + 345 + 125 + 885 + 40 |
| OVERAGE - quoted line billed above rate | **2,253.17** as billed | Inland Brazil 1,012.17 + Air freight 1,241.00 |
| UNQUOTED - no quote rate at all | **639.63** | 65 + 112.19 + 414.59 + 12.85 + 35 |
| **TOTAL** | **4,866.33** | reconciles exactly |

Overage *above quote* = **+297.57** (175.17 + 122.40).

## 4. Reconciling the two independent passes

Envoy's numbers differ in presentation, not substance. Each difference resolves exactly:

| Category | This document (v5) | Envoy | Exact reconciliation |
|---|---|---|---|
| MATCH | 1,973.53 | 1,933.53 | diff = **40.00** = "Additional Invoice Lines" (v5 folds into MATCH; Envoy lists as its own row) |
| OVERAGE | +297.57 above quote | 613.47 | same component facts; different baseline for air freight |
| UNQUOTED | 639.63 | 225.04 | diff = **414.59** = export clearance (Envoy breaks it out separately) |
| Actionable exposure | **937.20** | **937.20** | **identical on both routes** |

Every line verdict matches: the two bundled Brazil fees, the flat 125 handling line (not the conditional per-exam
125), delivery-to-door, US clearance, FDA, and duties-at-cost. No row is in dispute between the two documents.

**Envoy's table sums to 3,355.16, not 4,866.33** - because its OVERAGE row is a *delta* while its other rows are
*line totals* (Envoy flagged this itself), and Customs Duties 128.53 appears both inside its MATCH figure and as its
own row. **This document is the partition of record** because it sums to the invoice exactly with no double-count.

## 5. Air freight - triangulated from three independent sources

| Source | Basis | USD |
|---|---|---|
| Quote rate table (embedded image, quote p.2) | flat +300 kgs | 1,118.60 |
| Carrier HAWB 047-3175 3223 (gross 349,000 kg, 2 pallets) | 349 kg @ 2.30/kg | 802.70 |
| 5 Continent invoice 1026-08 | 365 kg @ 3.40/kg | 1,241.00 |

The invoice is **above both**: **+122.40** over 5 Continent's own quoted rate, and **+438.30** over what the carrier
itself documents. Both the weight (365 vs 349 kg) and the rate (3.40 vs 2.30) are inflated versus the carrier's own
paperwork - same AWB number, same 2 pallets.

**Which is the contractual ask.** The forwarder's own quote (1,118.60) is the price 5 Continent committed to; the
HAWB (802.70) exposes their underlying cost. The clean demand is *"re-bill to your quoted rate"* - Envoy's HAWB
figure is powerful supporting colour, but leading with it invites a margin debate. Both are documented so either can
be deployed.

**MAWB caveat.** The master waybill bills a nominal minimum (2.30 / total 57.30) - consolidator-to-airline
settlement, **not** what TrueTech owes. Only the **HAWB** is the right comparator: the HAWB consignee is **TrueTech
Inc**, while the MAWB consignee is 5 Continent Logistics itself.

## 6. Why $3,510.60 becomes $4,866.33 - the variance bridge

| Step | Delta | Running total |
|---|---|---|
| Quote - freight rate table | | **3,510.60** |
| 1. Freight overages (2 quoted lines billed above rate) | +297.57 | 3,808.17 |
| 2. Quoted customs/duty/fee items, now billed | +418.53 | 4,226.70 |
| 3. Wholly unquoted charges (5 items, no rate) | +639.63 | **4,866.33** |
| **Total difference** | **+1,355.73** | |

### Cause 1 - $297.57: OVERCHARGES on freight lines that WERE quoted
Inland Brazil 837.00 -> 1,012.17 (+175.17); Air Freight 1,118.60 -> 1,241.00 (+122.40). **DISPUTE** - billed above
the forwarder's own quoted rates.

### Cause 2 - $418.53: quoted customs items NOT in the freight table
US clearance 150 + FDA 100 + duties 128.53 + line fees 40. Billed **exactly as quoted**; only looks like an
increase because the $3,510.60 comparator excluded customs. **Legitimate** - but "Duties at cost" 128.53 still needs
a breakdown.

### Cause 3 - $639.63: WHOLLY UNQUOTED charges
Palletizing 65 + Storage 112.19 + Export clearance 414.59 (**possible duplicate**) + Duty advance 12.85 + Bank 35.
**DISPUTE** - no quoted rate for any of these.

## 7. Bottom line

| Cause | Amount | Share of gap | Verdict |
|---|---|---|---|
| Quoted customs items (not in freight table) | 418.53 | 31% | Legitimate - comparison artifact |
| Freight overages on quoted lines | 297.57 | 22% | **Dispute** |
| Wholly unquoted charges | 639.63 | 47% | **Dispute** (esp. 414.59 duplicate risk) |
| **Total gap** | **1,355.73** | 100% | **937.20 (69%) genuinely contestable** |

**Actionable dispute exposure: $937.20 - confirmed independently by both passes.**

## 8. Priority asks worth a direct reply to Graziela

1. **Air freight - the strongest line item.** Billed above 5 Continent's own carrier documentation. Invoice
   1,241.00 (365 kg @ 3.40) vs quoted flat 1,118.60 vs carrier HAWB 802.70 (349 kg @ 2.30). Ask them to **re-bill to
   the quoted 1,118.60** and explain the 365 kg / 3.40 basis.
2. **Export clearance 414.59 - confirm with Omega BEFORE disputing.** The quote says clearance "was agreed directly
   with Omega," i.e. it was NOT in 5 Continent's quote. If Omega was already paid, this line is a **straight
   duplicate** - the ask becomes *"please remove, already paid."*

## 9. Lower priority

- **Inland Freight Brazil +175.17** - billed 1,012.17 vs quoted 837.00. Same "re-bill to quote" ask.
- **Bond & MPF** - quoted formulas, no distinct invoice line; possibly bundled into "Customs Duties 128.53." Ask 5CL
  to break them out.
- **Handling Fee USA 125.00** - MATCH, but the quote has a *separate* conditional "125.00 per exam." Confirm no exam
  fee is embedded.
- **Beneficiary mismatch** - header "5 Continent Logistics LLC" vs pay block "5 Continent Alliance." Verify same
  entity before any wire.
- **Trading-company fee (16% + ~4.2%)** - quote premise was "no trading company." Confirm none embedded.
- **Spec drift** - quote 3 pallets / 329 kgs; as-shipped 2 pallets / 349 kg. "Delivery to the door" (885) was quoted
  for 3 pallets and billed in full for 2.

## 10. Provenance

- Quote: `brazil/sources/2026-08-26_5continent_rate_quote.pdf` (rate table = embedded image p.2)
- Invoice: `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf`
- HAWB: `brazil/sources/2026-10-02_air_waybill_hawb_issued.md`
- MAWB: `brazil/sources/2026-10-05_air_waybill_mawb_issued.md`
- Independent cross-check: `brazil/sources/2026-10-08_envoy_crosscheck_5continent_1026-08.pdf`
- Adjudication: `brazil/sources/2026-10-08_envoy_crosscheck_adjudication.md`

## Money rule

Pay-to routing (TD Bank NA, acct 9246418811) is a money move - no payment without an explicit governor command.
