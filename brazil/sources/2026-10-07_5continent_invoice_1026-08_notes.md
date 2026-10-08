# 5 Continent Logistics - Invoice no 1026-08 (2026-10-07)

> **Source:** invoice PDF supplied by Gary, thread 10800, 2026-10-07. Archived at
> `brazil/sources/2026-10-07_5continent_invoice_1026-08.pdf`. This is the **forwarder's actual freight bill**
> for the Black King -> TrueTech cacao export (HAWB/MAWB `047-3175-3223`).

## Identity

| Field | Value |
|---|---|
| Issuer | **5 Continent Logistics LLC** - 373 South Willow Street, Suite 333, Manchester NH 03103 |
| Role in the lane | **MAWB consignee / consolidation agent** (section 5.8; EIN 82-4285211) |
| Bill to | **TrueTech Inc** / Gary Teh - 1423 Hayes St, San Francisco CA 94117 (US importer of record) OK |
| Invoice no | **1026-08** |
| P.O./S.O. no | **`047-31753223`** - = the AWB number OK |
| Invoice date | 2026-10-07 |
| Payment due | **2026-10-08** |
| Amount due | **USD 4,866.33** |
| Terms | "If not paid within credit terms, 5% fee will be added automatically." |
| Pay-to | TD Bank NA, Portsmouth NH - beneficiary **5 Continent Alliance**, acct `9246418811`, ABA `011400071`, SWIFT `NRTHUS33XXX` (USD) / `TDOMCATTTOR` (FX) |

## Line items

| Item | Qty | Price | Amount (USD) |
|---|---|---|---|
| Inland Freight in Brazil | 1 | 1,012.17 | 1,012.17 |
| Airline Terminal Fee - Brazil SSA (airline + airport fees) | 1 | 345.00 | 345.00 |
| Palletizing | 1 | 65.00 | 65.00 |
| Storage - SSA Storage + Saturday Airport Fee | 1 | 112.19 | 112.19 |
| Clearance - Export Customs BRA + SDA | 1 | 414.59 | 414.59 |
| **Air Freight Charges** | **365** | **3.40** | **1,241.00** |
| Airline Terminal Fee - Airline Terminal Fee USA | 1 | 200.00 | 200.00 |
| Air Freight Handling | 1 | 125.00 | 125.00 |
| Inland Freight (US) | 1 | 885.00 | 885.00 |
| Clearance - Customs Clearance USA | 1 | 150.00 | 150.00 |
| Add Lines - Additional Invoice Lines | 8 | 5.00 | 40.00 |
| FDA - FDA Filing | 1 | 100.00 | 100.00 |
| Duties - Customs Duties | 1 | 128.53 | 128.53 |
| Duty Advance - Duty Advance Fee | 0.1 | 128.53 | 12.85 |
| Bank Fee - Bank Fees | 1 | 35.00 | 35.00 |
| **Total** | | | **4,866.33** |

## Cross-check vs section 7 cost model + the AWB

| Invoice item | Invoice (USD) | Section 7 / AWB expectation | Verdict |
|---|---|---|---|
| Air Freight Charges | **1,241.00** (365 kg @ 3.40) | AWB: 349 kg @ 2.30 = **802.70** (prepaid 857.70) | WARN mismatch |
| Airline Terminal Fee USA | 200.00 | ~212.50 | OK close |
| Air Freight Handling | 125.00 | US handling ~125.00 | OK exact |
| Customs Clearance USA | 150.00 | ~150.00 | OK exact |
| FDA Filing | 100.00 | FDA ~100.00 | OK exact |
| Inland Freight in Brazil | 1,012.17 | road BRL 6,615 (~$1,282 @PTAX) | WARN different basis |
| Palletizing | 65.00 | 3 pallets BRL 195 | WARN qty (physical = 2 pallets) |
| Terminal fee Brazil SSA | 345.00 | BR airport ~$0.30/kg min $250 | WARN close |
| Storage / SSA + Sat. fee | 112.19 | **not in section 7** (ties to 5.9 diaria) | new |
| Clearance - Export Customs BRA + SDA | 414.59 | **not itemized in section 7** | new |
| Customs Duties | 128.53 | "duty if applicable" | new |
| Duty Advance Fee | 12.85 | **not in section 7** | new |
| Bank Fees | 35.00 | **not in section 7** | new |
| Additional Invoice Lines (8 x 5) | 40.00 | **not in section 7** | new |
| **Total** | **4,866.33** | freight-only est. ~ **3,550** | WARN ~ +$1,300 |

## Flags

1. **Air freight keyed to a superseded weight.** The invoice bills **365 kg @ $3.40/kg = $1,241.00**. The air waybill / airport scale gives a **gross of 349,000 kg** (sections 5.5/5.7), billed **349 kg @ USD 2,30 = USD 802,70** (total prepaid **USD 857,70**). **365 is close to the superseded Rev 12 gross (364,06 kg)** - i.e. the invoice appears to have been cut on the stale weight, before the 349 kg re-weigh (Rev 15). **Delta = +$438.30** on the weight charge alone. Ask 5 Continent/Graziela to re-bill on 349 kg and confirm the $3.40 vs $2.30 rate basis.
2. **Three different air-freight figures now exist on one lane:** MAWB **$57,30** (5.8) / HAWB **$857,70** (5.8) / invoice **$1.241,00**. Reconcile to a single chargeable figure before paying - the 5.8 note already flagged the MAWB/HAWB gap.
3. **Beneficiary name mismatch.** The invoice header reads **"5 Continent Logistics LLC"** but the payment block reads **"5 Continent Alliance"**. Confirm the wire beneficiary is the **same legal entity** already verified on the MAWB (EIN 82-4285211) before any payment.
4. **Currency basis of the "in Brazil" lines.** The five Brazil-side lines are billed in **USD** here, whereas section 7 modeled them in **BRL** - confirm the FX basis/date so the pass-through is auditable.
5. **Palletizing qty = 1.** Physical cargo = **2 pallets** (5.3b, 5.7). Minor, but reconcile.
6. **Total vs estimate.** **$4,866.33** vs the June freight-only estimate ~ **$3,550** - roughly **$1,300 over**. Most of the gap is flag #1.
7. **MONEY RULE (section 0.3).** Payment routing (TD Bank, acct `9246418811`) is a **money move**. **No payment is made - and none may be - without an explicit governor command.** This note records the bill; it does not authorize (or initiate) payment.

## Open asks

- [ ] 5 Continent/Graziela -> re-issue/confirm the **air-freight line on 349 kg** (not 365) + confirm the **rate basis**.
- [ ] Confirm the **beneficiary legal entity** (Logistics LLC vs Alliance).
- [ ] Confirm **FX basis** for the Brazil-side USD lines.
- [ ] Reconcile the three air-freight figures (5.8) to one.
- [ ] Governor decision on whether/how to pay (money rule).
