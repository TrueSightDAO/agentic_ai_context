# Context updates (append-only)

Agents: append one line per entry. Do not remove or rewrite existing lines.

Format: `YYYY-MM-DD | <agent-id> | <short note>`

---
2025-02-16 | cursor | agroverse_shop/agl15: added redirect page at agl15/index.html → Google Sheet ledger (1tXgDss-AAdAFgBWVcW4ESRzRTodRmXyp7JxwBb0A-fE gid=2133986329). agroverse.shop/agl15 now points to AGL15 transparency ledger.
2025-02-16 | cursor | Deployment mapping: truesight.me → truesight_me_prod; agroverse.shop → agroverse_shop_prod. Updated WORKSPACE_CONTEXT.md §6 and PROJECT_INDEX.md.
2026-02-16 | cursor | Syndicate agreements: Added syndicate_agreement_template.md (20% DAO fee), AGL14 and AGL15 drafts in notarizations/, SYNDICATE_AGREEMENTS.md, and GOVERNANCE_SOURCES.md §5. Template + Markdown-first workflow for future agreements.
2026-02-16 | cursor | Syndicate precedence: Shipment financing = 20% fee; operational fund (invests in other AGLs) = no fee (avoid double-charging). AGL14 = USD 456.49. Updated WORKSPACE_CONTEXT, SYNDICATE_AGREEMENTS (quick reference), GOVERNANCE_SOURCES. Future AIs: read SYNDICATE_AGREEMENTS.md before drafting.
2026-02-16 | cursor | PDF generation: notarizations/scripts/generate_syndicate_pdf.mjs — always use TrueSight DAO logo as header. Logo: .github/assets/20221219 - Gary logo white background squarish.jpeg (fallback: 20240612_truesight_dao_logo.png). npm run generate-pdf in notarizations/.
2026-02-16 | cursor | Syndicate agreements: (1) Profit split: 20% retained by DAO, 80% distributed to financiers. (2) Remove redundant "Ledger spreadsheet" line — Location of AGLnn already resolves to it. (3) Logo header: max-height 100px, max-width 320px.
2026-02-16 | cursor | LATOKEN API disabled: getTdgUsdtPriceLaToken() in tdg_wix_dashboard.gs now returns null (on hold). Prevents 503 errors. Wix integration deprecated. Updated file header and PROJECT_INDEX.md.
2026-02-16 | cursor | Deprecated Wix gas fee script archived: tokenomics/google_app_scripts/deprecated/tdg_wix_gas_fees_deprecated.gs — contains setEcosystemGasFees() that calls LATOKEN API (causes 503). Do not execute. Archived for reference only.