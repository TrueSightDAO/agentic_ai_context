# Shipment documentation — FSVP process

## Purpose

For every shipment crossing the border under TrueTech Inc's importer-of-record, assemble the FSVP + customs + food-safety record set in `fda_fsvp/suppliers/<name>/`.

## Per-shipment pack

| # | Document | Example |
|---|----------|---------|
| 1 | Purchase order | `suppliers/cepotx/20240704_Purchase_Order_cepotx_100kg.pdf` |
| 2 | Lab test results (pathogens, adulterants) | `suppliers/cepotx/20250402_lab_test_330_kg_cacao_almonds.pdf` |
| 3 | Nota fiscal (BR) / commercial invoice | `suppliers/cepotx/20250402_nota_fiscal_330_kg_cacao_almonds.pdf`, `suppliers/black_king/20241003_30kg_commercial_invoice.xlsx` |
| 4 | FDA prior notice | `suppliers/black_king/20240924_fda_prior_notice_30_bottles_cacao_molasses.pdf` — filed per FDA PNSI before arrival |
| 5 | FDA web entry / ACE entry | `suppliers/black_king/20241003_30kg_cacao_nibs_webentry_prior_notice.pdf` |
| 6 | Shipping / transport receipts | `suppliers/coopercabruca/20231109_100KG_transport_from_Coopercabruca_to_Salvador_invoice.pdf`, Correios `CP…BR` tracking screenshots |
| 7 | CIC report (conversion/quality) where applicable | `suppliers/black_king/20240925_cic_report_fernando.pdf` |
| 8 | Certificates (organic, etc.) | `suppliers/coopercabruca/20241224_Fazenda_Santa_Ana_usda_organic_certificate.pdf` |

## Steps

1. Confirm the supplier's FSVP file is current (site visit + evaluation + written assurance on file; FFR valid). If not, pause shipment until it is.
2. Collect the pack above as PDFs (convert photos/screenshots where needed).
3. Name per convention: `YYYYMMDD_<supplier>_<doc-type>_<description>.pdf` (event date).
4. Commit to `suppliers/<name>/`, update `entity.json` `source_documents`, PR to `fda_fsvp`.
5. Keep the pack linked to the shipment in the shipment ledger / agroverse.shop shipment page.

## Notes

- FDA prior notice must be filed **before** the shipment arrives — no exceptions.
- US lane does **not** need MAPA (only the China/GACC lane does) — see `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md`.
