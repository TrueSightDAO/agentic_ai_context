# Supplier onboarding — FSVP documentation process

## Purpose

Build the FSVP record set for a **new foreign supplier** (or add a new product to an existing one) before/at first purchase, so TrueTech Inc's FSVP file is complete and defensible.

## Document set (each gets a real file in `fda_fsvp/suppliers/<name>/`)

1. **Site visit / inspection log** — see `SITE_VISIT_PROCESS.md` (the initial visit is the anchor record).
2. **Written assurance letter** — supplier letterhead, confirms product meets US food-safety requirements. Example: `20240626_CEPOT_cacao_Almonds_Written_assurance_letter.pdf`. File as `YYYYMMDD_<Supplier>_<product>_Written_assurance_letter.pdf`.
3. **Supplier evaluation / declaration** — TrueTech's evaluation of the supplier's food-safety controls. Example: `20240701_cepotx_supplier_evaluation.pdf`. File as `YYYYMMDD_<Supplier>_<product>_evaluation.pdf`.
4. **Identifier records** (one file each):
   - CNPJ (Brazil) — `YYYYMMDD_<supplier>_cnpj_record.pdf` (or `cpnj` typo variants in legacy files)
   - DUNS — `YYYYMMDD_<supplier>_duns_number.pdf` (or `duns.pdf`)
   - FDA Food Facility Registration — `YYYYMMDD_fda_registration_<supplier>.pdf` (annual, renew before 12-31)
5. **Entity profile** — create `suppliers/<name>/entity.json` per the schema in `fda_fsvp/entities.index.json` (legal name, trade name, CNPJ, DUNS, FDA FFR, address, products, FSVP status, contacts, source_documents), then register it in `entities.index.json`.

## Steps

1. Onboard the supplier (partner protocol — see agentic_ai_context `PARTNER_OUTREACH_PROTOCOL.md` / `RETAILER_ONBOARDING_PLAYBOOK.md` analogies).
2. Collect: CNPJ/DUNS/FFR records, written assurance letter, evaluation, site-visit evidence.
3. Build the PDFs (reportlab or the prior templates as base) and commit under `suppliers/<name>/`.
4. Create/update `entity.json` + `entities.index.json`.
5. PR to `fda_fsvp`; merge after governor review.

## Field anchors (from fda_fsvp)

- TrueTech signature block: Zhiwen Teh, President, admin@truesight.me, +1 415 300 0019
- Never commit FDA registration PINs or personal CPF (repo is public).
