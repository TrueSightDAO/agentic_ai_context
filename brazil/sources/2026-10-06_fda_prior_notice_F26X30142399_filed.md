# FDA Prior Notice **FILED** — envelope `F26X30142399` (Black King → TrueTech)

**Date filed:** 2026-10-06 22:54:52 EDT
**Source artefact:** `fda_fsvp/suppliers/black_king/20261006_fda_prior_notice_cacao_9_articles_sfo_air.pdf`
(+ `…/20261007_fda_product_codes_cacao_9_articles.pdf`, `FDA_PRODUCT_CODES.md`)
**Recorded by:** Sophia Truesight (autopilot) — 2026-10-09, thread 10800
**Why this file exists:** §5.6 of the checklist still said *"unfiled"*. The PN lives **only** in
`fda_fsvp`; a grep for `F26X30142399` across `agentic_ai_context` returned nothing. This closes that
cross-repo record gap so no future agent repeats the error.

---

## Envelope header (as filed)

| Field | Value |
|---|---|
| **PN Envelope / Confirmation** | **`F26X30142399`** |
| Entry Identifier | `###-4317322-5` (masked in the PDF) |
| Port of Arrival | **San Francisco Airport, CA (2801)** |
| Number of Food Articles | **9** |
| Entry Type | **Consumption** |
| Anticipated Arrival | **10/08/2026 14:30** |
| Mode of Transportation | **Air** |
| Submitter / Importer | **Zhiwen Teh / TrueTech Inc**, 3041 Taraval St, San Francisco CA 94116-2106 |
| Carrier | **TAP PORTUGAL** (IATA `TP`), **Flight `TP237`** |
| Airway Bill — Master / House | `04731753223` / `04731753223` |
| PN software version | v15.0.0 (November 14, 2024) |

**Deliverable:** the PN Summary Confirmation must be presented to CBP/FDA at the port of arrival.

## The 9 food articles (net 302.06 kg total)

| # | Product (as filed) | Packaging | Qty | Net kg | FDA Product Code | Confirmation # |
|---|---|---|---|---|---|---|
| 0001 | Cacao Nibs Kraft Pouch 8oz | 129 × 8oz pouch | 129 UN | 29.26 | `34BGN04` | 260636277882 |
| 0002 | Cacao Mass Bar 500g | 37 × 500 g bar | 37 UN | 18.50 | `34BDN05` | 260636277893 |
| 0003 | Cacao Nibs 10KG | 8 × 10 KG bag | 8 bags | 80.00 | `34BGN04` | 260636277860 |
| 0004 | Cacao Almonds | 1 × 10 KG bag | 10 KG | 10.00 | `34AHN99` | 260636277915 |
| 0005 | Ceremonial Cacao Kraft Pouch 200g | 169 × 200 g pouch | 169 UN | 33.80 | `34BHN05` | 260636277926 |
| 0006 | Cacao Nibs (KG) | 10 × 10 KG bag | 100 nominal | 99.50 | `34BGN04` | 260636277871 |
| 0007 | **Cacao Tea KG** | 2 × 10.5 KG bag | 21 KG | 21.00 | `34BHN04` | 260636277904 |
| 0008 | Cacao Butter | 1 × 5 KG block | 5 KG | 5.00 | `34BHN03` | 260636277930 |
| 0009 | **Cacao Almonds samples from Para** | 1 × 5 KG bag | 5 KG | 5.00 | `34AHN99` | 260636277856 |
| | **TOTAL** | | | **302.06** | | |

Manufacturer / Grower / Consolidator on **all 9 articles: `MATHEUS REIS PEREIRA`, Brazil.**
Submission date on all 9: **10/06/2026**.

> ⚠️ **"Cacao Almonds" = cocoa BEANS** (PT *amêndoas de cacau*), **not** tree nuts. Articles 0004 and
> 0009 are cocoa beans. Do **not** file or declare them as allergens/nuts.

## ✅ Consistency win — the PN matches the Rev-15 line table exactly

| Check | PN | Rev 15 (`build_black_king_export_docs.py`) | Match |
|---|---|---|---|
| Article / line count | 9 | 9 | ✅ |
| Net total | **302.06 kg** | **302.06 kg** | ✅ |
| Cacao Tea | 21.00 kg (art. 0007) | line 7, 21 kg, `2106.90.00` | ✅ |
| Cacao Almonds | 10.00 + 5.00 kg (art. 0004/0009) | line 4 (10 kg) + line 9 (5 kg) | ✅ |
| Gross (separately) | — | Rev 15 gross **349.00** = 302.06 + carton 26.94 + pallet 20.00 | ✅ |

The filed Prior Notice and our own commercial-doc SSOT **agree line for line**. Timing was also
compliant: filed **06/10**, arrival **08/10** — inside the ≥4 h-before-arrival and ≤15-day (PNSI)
windows of 21 CFR 1.279.

## ⚠️ Two discrepancies found while verifying

1. **Flight number:** the PN names **`TP237`**; the AWB requests **`TP028`**. If the flight changed after
   filing, the PN should have been amended — an arrival-document mismatch is a known CBP flag.
2. **Importer address:** the PN carries **3041 Taraval St** — the *registered CBP physical address*
   (`truetech_inc.entity.json` → `cbp_physical_on_file`), which is the correct one to use. The AWB
   consignee instead shows **1423 Hayes St**. Same importer, two addresses across the file set.

## What this does **not** prove

- **It is not APHIS clearance.** A Prior Notice satisfies **FDA**; it does not satisfy **APHIS**
  plant-health requirements. Those are different agencies and different gates.
- It does not evidence the **customs entry (ACE)** having been filed or matched.

## Related

- `brazil/sources/2026-10-09_agriculture_hold_CORRECTION_h2_refuted.md` — the retraction this file forced.
- `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` §5.6 — **still carries the stale `unfiled` line; needs flipping to FILED.**
- `fda_fsvp/FDA_PRODUCT_CODES.md` — durable product-code reference incl. these 9 articles.
