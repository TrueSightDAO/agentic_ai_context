# Recurring foreign-supplier verification — FSVP process

## Purpose

FSVP requires *ongoing* verification, not just an initial file. TrueTech maintains periodic written declarations of the recurring verification procedure per product line, and keeps the FDA regulations reference set current.

## The declaration documents

Existing declarations in `fda_fsvp/public_declarations/`:
- `20230827 - Foreign supplier FSVP approval process.pdf`
- `20230827 - small importer fsvp compliance declaration.pdf`
- `20231017 - foreign supplier recurring verification procedure.pdf`
- `20240623_foreign_supplier_recurring_verification_procedure_for_cacao_mass.pdf`
- `20250602_foreign_supplier_recurring_verification_procedure_for_cacao_tea.pdf`

## When to refresh

- New **product line** (e.g. cacao mass → cacao tea → ceremonial cacao): add a new declaration PDF `YYYYMMDD_foreign_supplier_recurring_verification_procedure_for_<product>.pdf`.
- **Annually** (or when the verification approach changes) — refresh the procedure description.
- When the FSVP importer's status changes (FFR renewal, supplier set changes).

## Regulations reference upkeep

Keep `fda_fsvp/regulations reference documents/` current — add new FDA guidance/FSVP publications when they drop (FSVP guidance Jan 2023, UFI guidance Apr 2022, small-entity compliance guide, records-requirements list, CBP 5106). Point future agents at this folder rather than re-downloading.

## Cross-references

- `brazil/BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE_CEPOTX.md` — China lane (GACC) is separate from US FSVP; US lane runs on FDA FFR + FSVP + Prior Notice + per-shipment phytosanitary.
- `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md` — lane-by-lane requirements.
