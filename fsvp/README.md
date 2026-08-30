# FSVP documentation system (FDA Foreign Supplier Verification Program)

Runbooks for the FDA FSVP record-keeping that TrueTech Inc (the US FSVP + CBP importer of record, EIN 88-3411514) maintains across the Agroverse supplier network.

## Where the records live

The records themselves live in the **`fda_fsvp`** repo (not here). This folder documents *how* those records are produced, named, and filed.

`fda_fsvp` layout:
- `public_declarations/` — TrueTech-level declarations & compliance docs (FDA FFR, foreign supplier approval process, small-importer FSVP compliance declaration, recurring verification procedure declarations, FSPCA cert, proof of inception, net transactions)
- `regulations reference documents/` — FDA guidance, FSVP participant manual, exercise workbook, records-requirements list, UFI guidance, CBP 5106 form, FDA-483a
- `suppliers/<name>/` — per-supplier folders (one per supplier in the network)
- `entities.index.json` — machine-readable index pointing at every `suppliers/<name>/entity.json` profile + `truetech_inc.entity.json`

## Document category taxonomy

| # | Category | Example real file(s) in fda_fsvp | Process runbook |
|---|----------|--------------------------------|-----------------|
| 1 | Site visit / inspection log | `suppliers/cepotx/20240625_CEPOTX_site_visit_to_paulo_farm.pdf` | `SITE_VISIT_PROCESS.md` (video evidence: `VIDEO_EVIDENCE_PROCESS.md`) |
| 2 | Written assurance letter | `suppliers/cepotx/20240626_CEPOT_cacao_Almonds_Written_assurance_letter.pdf` | `SUPPLIER_ONBOARDING_PROCESS.md` |
| 3 | Supplier evaluation / declaration | `suppliers/cepotx/20240701_cepotx_supplier_evaluation.pdf` | `SUPPLIER_ONBOARDING_PROCESS.md` |
| 4 | Identifier records (CNPJ / DUNS / FDA FFR) | `suppliers/cepotx/20240628_cepotx_cpnj_record.pdf`, `20240624_cepotx_duns_number.pdf`, `20250101_fda_registration_cepotx.pdf` | `SUPPLIER_ONBOARDING_PROCESS.md` |
| 5 | Entity profile (`entity.json`) | `suppliers/cepotx/entity.json`, `entities.index.json` | `SUPPLIER_ONBOARDING_PROCESS.md` |
| 6 | Purchase order | `suppliers/cepotx/20240704_Purchase_Order_cepotx_100kg.pdf` | `SHIPMENT_DOCUMENTATION_PROCESS.md` |
| 7 | Lab test results | `suppliers/cepotx/20250402_lab_test_330_kg_cacao_almonds.pdf` | `SHIPMENT_DOCUMENTATION_PROCESS.md` |
| 8 | Nota fiscal / commercial invoice | `suppliers/cepotx/20250402_nota_fiscal_330_kg_cacao_almonds.pdf` | `SHIPMENT_DOCUMENTATION_PROCESS.md` |
| 9 | FDA prior notice + web entry | `suppliers/black_king/20240924_fda_prior_notice_30_bottles_cacao_molasses.pdf` | `SHIPMENT_DOCUMENTATION_PROCESS.md` |
| 10 | Shipping / transport receipts | `suppliers/coopercabruca/20231109_100KG_transport_from_Coopercabruca_to_Salvador_invoice.pdf` | `SHIPMENT_DOCUMENTATION_PROCESS.md` |
| 11 | CIC report / certificates (organic, etc.) | `suppliers/black_king/20240925_cic_report_fernando.pdf`, `suppliers/coopercabruca/20241224_Fazenda_Santa_Ana_usda_organic_certificate.pdf` | `SHIPMENT_DOCUMENTATION_PROCESS.md` |
| 12 | Recurring verification procedure declaration | `public_declarations/20240623_foreign_supplier_recurring_verification_procedure_for_cacao_mass.pdf` | `RECURRING_VERIFICATION_PROCESS.md` |
| 13 | Regulations / guidance references | `regulations reference documents/` | `RECURRING_VERIFICATION_PROCESS.md` |

## Naming conventions

- **Site visits / inspections:** `YYYYMMDD_<Supplier>_site_visit_to_<farm_or_facility>.pdf` (e.g. `20240702_CEPOTX_site_visit_to_cleide_farm.pdf`, `20250908_Black_King_sitevisit_to_jesus_do_deus_Farm.pdf`)
- **Written assurance:** `YYYYMMDD_<Supplier>_<product>_Written_assurance_letter.pdf`
- **Evaluations:** `YYYYMMDD_<Supplier>_<product>_evaluation(_declaration).pdf`
- **FDA entries/prior notice:** `YYYYMMDD_fda_prior_notice_<description>.pdf`, `YYYYMMDD_fda_<product>_web_entry.pdf`
- **Registration renewals:** `YYYYMMDD_fda_registration_<supplier>.pdf`

Date is the event date, not the upload date. If the event date differs from the upload date, confirm before naming.

## Adding a new supplier / farm / shipment — quick path

1. New **supplier**: `SUPPLIER_ONBOARDING_PROCESS.md`
2. New **farm under an existing supplier** (e.g. a CEPOTX member farm): site visit per `SITE_VISIT_PROCESS.md` (incl. `VIDEO_EVIDENCE_PROCESS.md` when a video was recorded), then add the farm to `suppliers/<name>/entity.json` `source_farms`
3. New **shipment**: `SHIPMENT_DOCUMENTATION_PROCESS.md`
4. Periodic **verification declaration**: `RECURRING_VERIFICATION_PROCESS.md`

## Key identity anchors (do not guess these)

- TrueTech Inc — EIN 88-3411514 · CBP importer-of-record 88-341151400 · FDA FFR 12202640780 · DUNS 119035208
- Signature block on all site-visit PDFs: Zhiwen Teh, President, TrueTech Inc, admin@truesight.me, +1 415 300 0019
- See `fda_fsvp/truetech_inc.entity.json` for the full profile (payment details, service providers, addresses).

## Privacy rule

FDA registration PINs and any personal CPF are intentionally **excluded** from the public fda_fsvp repo. Never commit PINs/CPF.