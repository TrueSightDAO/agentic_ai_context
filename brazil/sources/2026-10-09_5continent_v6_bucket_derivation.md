# 5 Continent Invoice 1026-08 - Line-by-Line Derivation of the Three Buckets

**Answering: how is each bucket figure derived?** Every row carries quoted rate, billed amount, delta, and source.

## Establishing the two baselines (do this first)

| Baseline | Amount | What it is | Source |
|---|---|---|---|
| Quote - freight rate table | **$3,510.60** | 7 logistics lines only | Quote 26 Aug 2026, embedded table, quote p.2 |
| Quote - customs section | separate | US clearance, FDA, duties, bond, MPF, line fees | Quote p.2, "Customs clearance charges" |
| Invoice 1026-08 | **$4,866.33** | 15 lines, all-in landed | 5 Continent invoice, 07 Oct 2026 |

The two quote parts are separate. The customs section is deliberately outside the $3,510.60. That single fact
drives Causes 2 and 3.

**Quoted freight rate table, opened up (sums to $3,510.60):**

| Quoted line | Rate |
|---|---|
| Inland in Brazil | 837.00 |
| Airport charges BRA | 250.00 |
| Airline charges BRA | 95.00 |
| Air Freight +300 kgs | 1,118.60 |
| Airline charges USA | 200.00 |
| Handling Fee USA | 125.00 |
| Delivery to the door | 885.00 |
| **Total** | **3,510.60** |

---

## Cause 1 - Freight overages: $297.57
### "2 quoted lines billed above rate"

This is a **delta only** - the two lines were billed higher than the forwarder's own quoted rate.

| Quoted line | Quoted rate | Billed | Delta | Why |
|---|---|---|---|---|
| Inland in Brazil | 837.00 | 1,012.17 | **+175.17** | Billed above 5 Continent's own quote |
| Air Freight +300 kgs | 1,118.60 | 1,241.00 | **+122.40** | 365 kg @ $3.40 vs quoted flat 1,118.60 |
| **Cause 1 delta** | | | **+297.57** | |

**Cross-check - the "as billed" figure (why you may see $2,253.17):**

| Same two lines, as billed | Amount |
|---|---|
| Inland Freight in Brazil | 1,012.17 |
| Air Freight Charges | 1,241.00 |
| **Billed total of the 2 lines** | **2,253.17** |

**So both v5 numbers are correct, they just answer different questions:**
- **$297.57** = how much *above quote* (the bridge input; the dispute)
- **$2,253.17** = what these two lines *total on the invoice* (the bucket as billed)

The $297.57 is the one that belongs in the variance bridge. $2,253.17 minus $297.57 leaves $1,955.60 - the quoted value
of those two lines; the other $1,955.60 of the freight table is inside the MATCH bucket.

---

## Cause 2 - Quoted customs items, now billed: $418.53
### "quoted customs/duty/fee items, now billed"

These lines were **quoted** - just in the *customs* section, not the freight table. Billed **exactly as quoted**, so they
only look like an increase because the $3,510.60 comparator excluded customs.

| Line item | Quote basis | Billed | Delta | Verdict |
|---|---|---|---|---|
| Customs Clearance USA | $150.00 | 150.00 | 0.00 | match |
| FDA Filing | $100.00 | 100.00 | 0.00 | match |
| Customs Duties | At Cost | 128.53 | +128.53 | match (at cost) |
| Additional Invoice Lines | 1st 3 free, $5/line (8 chargeable) | 40.00 | +40.00 | match (quoted policy) |
| **Cause 2 total** | | **418.53** | | |

**Why this is +418.53 and not $0:** "At Cost" duties and the quoted per-line policy had no dollar figure in the quote, so
the *first billing* of them is what moves the number. US clearance and FDA were quoted at exactly $150 and $100 with
zero movement.

**This $418.53 is legitimate** - it is a comparison artifact, not an overcharge. The one item still needing detail is
the $128.53 duties ("At Cost") - it needs a customs breakdown.

---

## Cause 3 - Wholly unquoted charges: $639.63
### "5 items, no rate"

No quoted rate of any kind exists anywhere in the quote for these five lines.

| # | Line item | Quoted rate | Billed | Note |
|---|---|---|---|---|
| 1 | Palletizing | none | 65.00 | Quote premise was heat-treated pallets; billed anyway |
| 2 | Storage - SSA + Saturday Airport Fee | none | 112.19 | Not in quote |
| 3 | Clearance - Export Customs BRA + SDA | "agreed with Omega" | 414.59 | **Possible DUPLICATE** - see below |
| 4 | Duty Advance Fee | none | 12.85 | = 10% of the 128.53 duty |
| 5 | Bank Fees | none | 35.00 | Not in quote |
| | **Cause 3 total** | **0.00** | **639.63** | |

**Duplicate risk on item 3 ($414.59).** The quote states export customs clearance was "agreed directly with Omega" -
i.e. **outside** 5 Continent's scope. If Omega was paid separately, this line is a straight duplicate. This is the single
largest unquoted item and **must be confirmed with Omega before disputing**.

**Arithmetic check on item 4:** the Duty Advance Fee is 10% of the Customs Duties line - 10% x 128.53 = **12.85**.
Confirmed exactly.

---

## The bridge, now fully derived

| Step | This cause | Running total |
|---|---|---|
| Quote - freight rate table | | 3,510.60 |
| 1. Freight overages (2 quoted lines above rate) | +297.57 | 3,808.17 |
| 2. Quoted customs items, now billed | +418.53 | 4,226.70 |
| 3. Wholly unquoted (5 items, no rate) | +639.63 | **4,866.33** |
| **Total difference** | **+1,355.73** | |

| Verdict | Amount | Share |
|---|---|---|
| Legitimate (comparison artifact) | 418.53 | 31% |
| **Dispute - freight overages** | 297.57 | 22% |
| **Dispute - wholly unquoted** | 639.63 | 47% |
| **Total gap** | **1,355.73** | 100% |
| **Actionable dispute exposure** | **937.20** | **69% of gap** |

**Reconciliation proof (all checked to the cent):**
297.57 + 418.53 + 639.63 = 1,355.73 OK - 3,510.60 + 1,355.73 = 4,866.33 OK - 297.57 + 639.63 = 937.20 OK

---

## Sources

- Quote: `brazil/sources/2026-08-26_5continent_rate_quote.pdf` (Graziela Vedana, 26 Aug 2026; freight table is an
  embedded image, quote p.2)
- Invoice: `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf` (no. 1026-08, 07 Oct 2026)
- Supporting: `2026-10-07_5continent_invoice_1026-08_notes.md`,
  `2026-10-08_5continent_quote_vs_invoice_FINAL_v5_envoy_verified.md`

Prepared by Sophia (TrueSight DAO Autopilot), 2026-10-09. All bucket arithmetic verified in-script before render.

**MONEY RULE (sec 0.3):** this is analysis only. No payment made or implied.
