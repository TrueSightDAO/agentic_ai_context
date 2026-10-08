# 5 Continent - Why $3,510.60 becomes $4,866.33 (variance bridge, 2026-10-08)

> **Question:** why is the quote $3,510.60 and the invoice $4,866.33, and what caused the difference?
>
> **Raw sources:** quote `brazil/sources/2026-08-26_5continent_rate_quote.pdf` (rate table = embedded image, p.2);
> invoice `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf`. Supersedes n/a - this is a new bridge view.

## The headline: the two numbers are not the same kind of figure

- **$3,510.60** = 5 Continent's **freight rate table only** (7 logistics lines).
- **$4,866.33** = the **all-in landed cost** (freight + customs + duties + fees), 15 lines.

The quote contained a **separate** "Customs clearance charges" section (US clearance, FDA, duties, bond, MPF,
line-item fees) that is **not** part of the $3,510.60. So $3,510.60 is a **freight subtotal**, not a landed-cost
quote - which is why the gap resists a one-line "they overcharged" explanation.

## Side-by-side: what each number contains

| Quote freight table (7) | USD | Invoice 1026-08 (15) | USD |
|---|---|---|---|
| Inland in Brazil | 837.00 | Inland Freight in Brazil | 1,012.17 |
| Airport charges BRA | 250.00 | Airline Terminal Fee - Brazil SSA | 345.00 |
| Airline charges BRA | 95.00 | Palletizing | 65.00 |
| Air Freight (+300 kgs) | 1,118.60 | Storage - SSA + Saturday | 112.19 |
| Airline charges USA | 200.00 | Clearance - Export Customs BRA + SDA | 414.59 |
| Handling Fee USA | 125.00 | Air Freight Charges | 1,241.00 |
| Delivery to the door (3 pallets) | 885.00 | Airline Terminal Fee USA | 200.00 |
| | | Air Freight Handling | 125.00 |
| | | Inland Freight (US) | 885.00 |
| | | Customs Clearance USA | 150.00 |
| | | Additional Invoice Lines | 40.00 |
| | | FDA Filing | 100.00 |
| | | Customs Duties | 128.53 |
| | | Duty Advance Fee | 12.85 |
| | | Bank Fees | 35.00 |
| **QUOTED (freight only)** | **3,510.60** | **INVOICED (all-in)** | **4,866.33** |

## The variance bridge: $3,510.60 -> $4,866.33

| Step | Delta | Running total |
|---|---|---|
| Quote - freight rate table | | **3,510.60** |
| 1. Freight overages (2 quoted lines billed above rate) | +297.57 | 3,808.17 |
| 2. Quoted customs/duty/fee items, now billed | +418.53 | 4,226.70 |
| 3. Wholly unquoted charges (5 items, no rate) | +639.63 | 4,866.33 |
| **Invoice total** | | **4,866.33** |
| **Total difference** | **+1,355.73** | |

## The three causes, clearly indicated

### Cause 1 - $297.57: OVERCHARGES on freight lines that WERE quoted
| Line | Quoted | Billed | Over |
|---|---|---|---|
| Inland Freight Brazil | 837.00 | 1,012.17 | +175.17 |
| Air Freight | 1,118.60 | 1,241.00 | +122.40 |
| **Subtotal** | | | **+297.57** |

-> **DISPUTE.** Billed *above the forwarder's own quoted rates.* Air freight is worst: invoice 365 kg @ 3.40 vs
the carrier's own HAWB 349 kg @ 2.30 (= 802.70) and the quote's flat 1,118.60.

### Cause 2 - $418.53: quoted items simply NOT in the freight table
| Item | Amount | Quoted? |
|---|---|---|
| US Customs Clearance | 150.00 | yes (customs section) |
| FDA Processing | 100.00 | yes (customs section) |
| Customs Duties | 128.53 | yes ("at cost") |
| Additional Invoice Lines | 40.00 | yes ($5/line policy) |
| **Subtotal** | **418.53** | |

-> **NOT an overcharge** - billed exactly as quoted. Looks like part of the increase only because the comparator
($3,510.60) excluded customs. Check: "Duties at cost" (128.53) needs a breakdown.

### Cause 3 - $639.63: WHOLLY UNQUOTED charges
| Item | Amount | Note |
|---|---|---|
| Palletizing | 65.00 | no quote rate |
| Storage - SSA + Saturday | 112.19 | no quote rate |
| Export Customs BRA + SDA | 414.59 | quote said "agreed directly with Omega" -> possible DUPLICATE |
| Duty Advance Fee | 12.85 | no quote rate |
| Bank Fees | 35.00 | no quote rate |
| **Subtotal** | **639.63** | |

-> **DISPUTE** - no quoted rate for any of these; the 414.59 export clearance may already have been paid to Omega.

## One-line answer

| Cause | Amount | Share of gap | Verdict |
|---|---|---|---|
| Quoted customs items (not in freight table) | 418.53 | 31% | Legitimate - comparison artifact |
| Freight overages on quoted lines | 297.57 | 22% | **Dispute** |
| Wholly unquoted charges | 639.63 | 47% | **Dispute** (esp. 414.59 duplicate risk) |
| **Total gap** | **1,355.73** | 100% | **~937.20 (69%) genuinely contestable** |

## Caveats
- Quote priced for **3 pallets / 329 kg**; as-shipped **2 pallets / 349 kg**. Air freight is a flat "+300 kgs" bucket
  (weight change does not move it) - but "Delivery to the door" (885) was quoted for 3 pallets and billed in full for 2.
- $4,866.33 excludes any trading-company fee (quote premise: none).
- Air freight has three figures: quote 1,118.60 - carrier HAWB 802.70 - invoice 1,241.00.

## Money rule

Pay-to routing (TD Bank NA, acct 9246418811) is a money move - no payment without an explicit governor command.
