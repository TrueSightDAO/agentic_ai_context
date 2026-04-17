# ADVISORY_SNAPSHOT

Machine-oriented digest of **recent evidence** for LLM advisors. Git lines are **proxies** for shipped work, not verified outcomes.

---

## Meta

- Generated (UTC): `2026-04-17T20:56:19Z`
- Look-back: **7** calendar days (`2026-04-10` → today UTC)
- Curated clone set: **11** repos (same table as Beer Hall preview)

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-04-10 | cursor | **Main Ledger — Matheus / BRL:** Standing convention in **WORKSPACE_CONTEXT.md** §3c: **Matheus Reis** periodically buys **DAO inventory** in **`Brazilian Reis`** (exact **`Currencies`!A**) under his management; double-entry **BRL** cash leg + **inventory** leg; **`Fund Handler`** = **Matheus Reis** both legs; **`Price in USD`** on SKU = R$ landed/unit × **`Brazilian Reis`** **`Price in USD`** (USD per BRL). Short operator prompts (receipt, counts, date, evidence) suffice. Note: **offchain** **Description** must not lead with **`+`** (Sheets formula). Cross-links **AGROVERSE_PRICE_LIST_AND_ASSETS.md**, **SUPPLY_CHAIN_AND_FREIGHTING.md**.

_All dated lines on/after 2026-04-10_ (13):

- 2026-04-10 | cursor | **Main Ledger — Matheus / BRL:** Standing convention in **WORKSPACE_CONTEXT.md** §3c: **Matheus Reis** periodically buys **DAO inventory** in **`Brazilian Reis`** (exact **`Currencies`!A**) under his management; double-entry **BRL** cash leg + **inventory** leg; **`Fund Handler`** = **Matheus Reis** both legs; **`Price in USD`** on SKU = R$ landed/unit × **`Brazilian Reis`** **`Price in USD`** (USD per BRL). Short operator prompts (receipt, counts, date, evidence) suffice. Note: **offchain** **Description** must not lead with **`+`** (Sheets formula). Cross-links **AGROVERSE_PRICE_LIST_AND_ASSETS.md**, **SUPPLY_CHAIN_AND_FREIGHTING.md**.
- 2026-04-10 | cursor | **Tokenomics GAS:** **`clasp push`** for QR web app script `1y6JVYwq…` and sales telegram parser `1dsWec…`; assistants always supply Script editor URLs + **Deploy → Manage deployments → New version** note for Web Apps. **`SCHEMA.md`**: **`Stripe Social Media Checkout ID`** column **P = Agroverse QR code**; **`QR Code Sales`** column **D** = cash proceeds collector for `[SALES EVENT]`. **`NOTES_tokenomics.md`** (clasp/deploy table + Stripe P workflow), **`WORKSPACE_CONTEXT.md`** §3 tokenomics bullet.
- 2026-04-11 | cursor | **Field agent location (Hit List):** DApp **`stores_nearby.html`** + Stores Nearby GAS (`clasp_mirrors/1NpHrKJW…`) **`save_location`** → tab **`Recent Field Agent Location`** (`1eiqZr3LW…` gid 881847228). Python **`market_research/scripts/field_agent_location_places_pull.py`** + GA **`field_agent_location_places_pull.yml`**. Docs: **`tokenomics/SCHEMA.md`** §4, **`DAPP_PAGE_CONVENTIONS.md`** §14 field-agent subsection, **`WORKSPACE_CONTEXT.md`** §3 APIs bullet, **`HIT_LIST_CREDENTIALS.md`** field-agent section.
- 2026-04-11 | cursor | **Beer Hall digest preview (“review recent progress”):** **`market_research/scripts/generate_beer_hall_preview.py`** writes **`agentic_ai_context/previews/beer_hall_preview_latest.md`** (per-clone `git log`, optional **`gh pr list`**, **`list_recent_telegram_chat_logs_for_digest.py`**). **`OPENCLAW_WHATSAPP.md` § Preview digest — review recent progress**; **`WORKSPACE_CONTEXT.md` §3d** preview bullet. Still **TrueSightDAO-only** GitHub in any *Shipped* draft; **no** `openclaw message send` / **no** `append_openclaw_beer_hall_log.py` until the operator approves a real post.
- 2026-04-11 | cursor | **Beer Hall preview → stdout:** `generate_beer_hall_preview.py` now prints the **full Markdown on stdout** by default (`Written to: …` on stderr); **`--no-stdout`** for file-only. Operator preference: when asked to **review progress**, always show digest in **console / terminal**. Docs: **`OPENCLAW_WHATSAPP.md` § Preview**, **`WORKSPACE_CONTEXT.md` §3d**, **`PROJECT_INDEX.md`** agentic row.
- 2026-04-12 | cursor | **Tokenomics QR Code Generation clasp:** **`google_app_scripts/agroverse_qr_codes/version.js`** (`getQRCodeGenerationScriptBuildId`) — bump before every **`clasp push`**; copy **`version.js`** next to **`Code.js`** in mirror **`1N6o00N9VtRK…`**. **`process_qr_code_generation_telegram_logs.gs`** logs build at run start. Docs: **`NOTES_tokenomics.md`**, **`WORKSPACE_CONTEXT.md`** §3a tokenomics bullet, **`PROJECT_INDEX.md`** tokenomics row, **`tokenomics/clasp_mirrors/README.md`** workflow.
- 2026-04-12 | cursor | **Tokenomics clasp `Version.gs` (not version.js):** Removed **`version.js`**; QR Generation uses **`agroverse_qr_codes/Version.gs`**. Added **`google_app_scripts/_clasp_default/Version.gs`** + **`scripts/ensure_clasp_version_gs.mjs`** to seed **`Version.gs`** on all **`clasp_mirrors/*/`** with **`.clasp.json`**. Sales / Parse Telegram continues to use **`tdg_inventory_management/Version.gs`**. Docs: **`NOTES_tokenomics.md`**, **`WORKSPACE_CONTEXT.md`**, **`PROJECT_INDEX.md`**, **`clasp_mirrors/README.md`**.
- 2026-04-14 | cursor | **GitHub CI / PR merge:** Do **not** long-poll Actions (**`gh pr checks --watch`**, **`gh run watch`**, sleep loops). Prefer one **`gh pr checks`** snapshot, local tests (`npm test` / Playwright), then hand off PR + Actions URLs. **`WORKSPACE_CONTEXT.md` §3e**, **`GITHUB_AGENTIC_AI_SSH.md`** merge bullets, **`WORKSPACE_CONTEXT.md` §5** (Agroverse Shop CI bullet).
- 2026-04-14 | cursor | **Agroverse QR codes** (main ledger `1GE7PUq…` tab *Agroverse QR codes*): **Column I (`Currency`)** values are tied to **`Currencies`!A** (same workbook; external reference / IMPORTRANGE pattern—exact string for ledger & sales validation). **Regional promo IDs (column A):** operator prefers **`LA`** (Los Angeles); **`CC`** = ceremonial cacao, **`CT`** = cacao tea (tokens in ids like `AUSTIN_CC_…`). Local label compile: **`tokenomics/python_scripts/agroverse_qr_code_generator/batch_compiler.py`** reads **A–H** only; keep **A** short. **`NOTES_tokenomics.md`**, **`WORKSPACE_CONTEXT.md` §3/§4**, **`tokenomics/SCHEMA.md`** (*Agroverse QR codes* column I).
- 2026-04-14 | cursor | **Agroverse QR batch playbook:** Added **`AGROVERSE_QR_CODE_BATCH_GENERATION.md`** (sheet **A–V**, **K** GitHub `compiled_` formula, **`batch_compiler.py`** + venv + **`to_print/`**, automation notes). **`README.md`** Contents + how-to **§17**; **`WORKSPACE_CONTEXT.md` §5**; **`NOTES_tokenomics.md`** cross-link; **`PROJECT_INDEX.md`** tokenomics row.
- 2026-04-14 | cursor | **LA batch QR fix:** Sheet rows **`LA_*_20260414_*`** — **E–H** reset from reference (**CC** → Oscar Farm/Bahia/Brazil/2024; **CT** → La do Sitio/Para/Brazil/2024); removed **`compiled_Los_Angeles_*.png`**, regenerated **`compiled_Oscar_Farm_*.png`** / **`compiled_La_do_Sitio_*.png`**. **`AGROVERSE_QR_CODE_BATCH_GENERATION.md`** — **E–H** must follow template farm, not handout city unless operator asks.
- 2026-04-14 | cursor | **agroverse.shop new SKU — farm/shipment grids:** Added **`AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md`** ( **`item-card`** on **`farms/*/index.html`** + **`shipments/agl*/index.html`** after new **`product-page/`**). **`PRODUCT_DEVELOPMENT_SPECS.md` §1/§3**, **`README.md`**, **`OPERATING_INSTRUCTIONS.md`**, **`WORKSPACE_CONTEXT.md` §4/§5**, **`PROJECT_INDEX.md`** (agroverse_shop); **`agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md`** new section + template bullets.
- 2026-04-16 | cursor | **Tokenomics GAS headers:** Every **`tokenomics/google_app_scripts/**/*.gs`** now documents **`Apps Script editor:`** `https://script.google.com/home/projects/<scriptId>/edit` (or N/A for deprecated stubs) per **`clasp_mirrors/PROJECT_INDEX.md`**. **`NOTES_tokenomics.md`** — index link + SeaCoast ingest row (`1gi4YKh2…`). SeaCoast **`Code.gs`** header order normalized.

---

## Pipeline activity map (PROJECT_INDEX ↔ git)

| Pipeline | Mapped clone | Activity in window |
|----------|----------------|----------------------|
| `go_to_market` | `market_research` | **yes** |
| `openclaw` | `agentic_ai_context` | **yes** |
| `TrueChain` | `TrueChain` | **no** |
| `oracle` | `iching_oracle` | **no** |

---

## Git log by repo (origin default branch)

### `truesight_me` → `truesight_me_beta`

```
c1f33e4 | 2026-04-16 16:27:45 -0700 | Point Agroverse and Sunmint pages to their program whitepapers. (#34)
8a6cca6 | 2026-04-16 14:35:49 -0700 | Surface Beer Hall digest feed on home and beerhall/updates.
eda8e5a | 2026-04-16 14:34:49 -0700 | blog: ACTIVE ledger schematic + DApp verified success mockup (#33)
a16b793 | 2026-04-16 14:28:01 -0700 | blog: add end-to-end flow diagram to signature onboarding post (#32)
aecdb5f | 2026-04-16 14:23:35 -0700 | blog: name Main Ledger workbook, Sheet links, ledger mirror, schematic (#31)
865471e | 2026-04-16 14:18:57 -0700 | blog: unify server-side narrative on demo_edgar_digital_signature_sheet_flow.py (#30)
1529cd9 | 2026-04-16 14:10:43 -0700 | blog: point DApp signature onboarding to public Python demo only (#29)
81c0262 | 2026-04-16 14:04:17 -0700 | blog: dedicated art for DApp signature onboarding post (#28)
a01d84b | 2026-04-16 13:54:36 -0700 | Blog: link Edgar onboarding post to sentiment_importer master Ruby sources. (#27)
56eeb88 | 2026-04-16 13:48:26 -0700 | Fix meta title and description on DApp signature onboarding blog post. (#26)
c887826 | 2026-04-16 13:47:40 -0700 | Blog: DApp digital signature email onboarding protocol (2026-04-16). (#25)
cc62635 | 2026-04-14 13:15:10 -0700 | Blog: new header art for WhatsApp-in-the-loop post (#24)
5bf9f92 | 2026-04-14 13:12:58 -0700 | Blog: coop post live links, meme header, editorial context doc (#23)
b393050 | 2026-04-14 13:07:41 -0700 | Add start_server.sh for local static preview (#22)
76dc983 | 2026-04-14 13:01:29 -0700 | Whitepaper: DAO label vs co-ops/Web3; blog on cooperative models (#21)
d7aee1e | 2026-04-14 12:54:27 -0700 | Blog: sweat-equity hero uses PD knight-vs-snail marginalia (#20)
61541f6 | 2026-04-14 12:46:11 -0700 | Blog: embed YouTube poster thumbnails on sweat-equity post (#19)
9d58692 | 2026-04-14 12:44:29 -0700 | Replace truesight.me/vault with /dapp; Cypher Defense icon on AWS post (#18)
0f0bf23 | 2026-04-14 12:35:47 -0700 | Blog: AWS / Cypher-Defense and sweat-equity DAO philosophy (Apr 14, 2026)
677ef37 | 2026-04-11 15:38:46 -0700 | Merge pull request #16 from TrueSightDAO/copy/view-whitepaper-labels
3ec152f | 2026-04-11 15:38:37 -0700 | UI: label whitepaper links and CTAs as View Whitepaper
c70b578 | 2026-04-11 15:34:46 -0700 | Merge pull request #15 from TrueSightDAO/feat/sunmint-whitepaper-html
271f058 | 2026-04-11 15:34:37 -0700 | Port SunMint whitepaper from stash to static HTML
5775eb0 | 2026-04-11 15:32:31 -0700 | Merge pull request #14 from TrueSightDAO/fix/restore-whitepaper-diagram-assets
3897782 | 2026-04-11 15:32:17 -0700 | Restore real whitepaper diagram PNGs (replace placeholders)
5f4f663 | 2026-04-11 15:30:43 -0700 | Merge pull request #13 from TrueSightDAO/fix/whitepaper-links-local-root
f9543a8 | 2026-04-11 15:30:34 -0700 | Use root-relative whitepaper URLs so local dev matches production
7c985a5 | 2026-04-11 15:28:33 -0700 | Merge pull request #12 from TrueSightDAO/fix/whitepaper-root-relative-assets
70e0f2f | 2026-04-11 15:28:24 -0700 | Fix whitepaper asset URLs: use root-relative paths for local dev
b76609d | 2026-04-11 15:25:18 -0700 | Merge pull request #11 from TrueSightDAO/fix/whitepaper-css-and-assets
1cff0b9 | 2026-04-11 15:25:06 -0700 | Fix whitepaper production: TOC layout CSS and diagram assets
0f5d0ff | 2026-04-11 15:12:40 -0700 | Merge pull request #10 from TrueSightDAO/docs/agroverse-milestones-sales
bc6cd68 | 2026-04-11 15:12:27 -0700 | Docs: add public sales feed figures to Agroverse milestones
8aa074b | 2026-04-11 15:04:48 -0700 | Merge pull request #9 from TrueSightDAO/docs/whitepaper-handbook-update
b9a38ce | 2026-04-11 15:01:40 -0700 | Docs: refresh DAO and Agroverse whitepapers for ledger governance
```

### `market_research` → `go_to_market`

```
c418f7b | 2026-04-16 22:53:35 -0700 | Merge pull request #50 from TrueSightDAO/feature/advisory-snapshot-optional-sheet-sales
9ce3fb7 | 2026-04-16 22:53:29 -0700 | feat(advisory): optional --with-sheet-sales in generate_advisory_snapshot
595e194 | 2026-04-16 22:17:46 -0700 | feat(advisory): index.json v2 with BASE, read_order, canonical_context URLs.
75c285a | 2026-04-16 13:50:38 -0700 | chore: move Beer Hall archiver to ecosystem_change_logs repo
4f0f0a4 | 2026-04-16 13:50:38 -0700 | feat(beer-hall): archive published digests to ecosystem_change_logs
3aab055 | 2026-04-15 15:32:58 -0700 | Merge pull request #49 from TrueSightDAO/feature/agroverse-partner-venue-inventory-sync
73ca10e | 2026-04-15 15:31:29 -0700 | fix(agroverse): partner venue totals independent of store-manager flag
79032f9 | 2026-04-15 14:54:08 -0700 | Merge pull request #48 from TrueSightDAO/feature/publish-agroverse-inventory-snapshot
0461be4 | 2026-04-15 14:53:55 -0700 | ci: publish Agroverse store and partner inventory JSON daily
30c343b | 2026-04-14 16:40:44 -0700 | feat(beer-hall): DApp Remarks digest helper and preview wiring
bcbac83 | 2026-04-14 12:03:03 -0700 | Remove EC2 terminate script (now in Cypher-Defense)
e6a1de5 | 2026-04-14 11:58:24 -0700 | EC2 terminate helper and Cypher-Defense .env for AWS keys
edcc983 | 2026-04-13 12:49:41 -0700 | Hit List: Google listing column, Places backfill, GAS sync (#45)
5119301 | 2026-04-12 17:36:46 -0700 | chore(scripts): add Beer Hall digest preview generator (#44)
03da181 | 2026-04-12 16:03:18 -0700 | Merge pull request #43 from TrueSightDAO/feat/warmup-email-grok-rainforest-flexibility
8f75b4d | 2026-04-12 16:02:59 -0700 | feat(email-agent): warmup Grok prompt — rainforest, QR trees, flexible paths
98af9e3 | 2026-04-11 14:34:31 -0700 | Merge pull request #42 from TrueSightDAO/feat/hit-list-human-shortlisted-pipeline-chart-script
af9d095 | 2026-04-11 14:34:19 -0700 | feat: human Shortlisted → enrich + pipeline dashboard chart colors
6e93ed4 | 2026-04-11 14:33:24 -0700 | Merge pull request #41 from TrueSightDAO/chore/field-agent-places-hourly-cron
92e72d1 | 2026-04-11 14:33:12 -0700 | ci: run field agent Places pull every hour
c8796f8 | 2026-04-11 14:22:40 -0700 | Merge pull request #40 from TrueSightDAO/fix/hit-list-enrich-contact-workflow-yaml
38ff600 | 2026-04-11 14:22:28 -0700 | fix(ci): quote workflow_dispatch description for YAML validity
5818a10 | 2026-04-11 14:11:48 -0700 | Merge pull request #39 from TrueSightDAO/feature/field-agent-location-places-pull
5702de2 | 2026-04-11 14:11:25 -0700 | feat(field-agent): Recent Field Agent Location → Places → Hit List
19dba9f | 2026-04-10 15:48:32 -0700 | Merge pull request #38 from TrueSightDAO/feat/hit-list-exclude-audit
267750c | 2026-04-10 15:48:18 -0700 | feat(hit-list): exclude bar/drink Places types; audit script for Not Appropriate
6e978f4 | 2026-04-10 15:27:21 -0700 | feat(hit-list): dedupe by Shop Name + Address, script to remove dup rows (#37)
643a28a | 2026-04-10 15:18:33 -0700 | fix(hit-list): retry Google Sheets API on transient 502/503/504 (#36)
b69afba | 2026-04-10 15:09:50 -0700 | Merge pull request #35 from TrueSightDAO/fix/hit-list-sheets-read-quota
6d9a831 | 2026-04-10 15:09:37 -0700 | fix(hit-list): avoid Sheets read quota on status promote batch
4d0a028 | 2026-04-10 10:56:22 -0700 | Merge pull request #34 from TrueSightDAO/feature/hit-list-status-promote-automation
912e03e | 2026-04-10 10:56:08 -0700 | feat(hit-list): automated status promotions with DApp Remarks
```

### `agentic_ai_context` → `agentic_ai_context`

```
e1ee31a | 2026-04-16 22:53:15 -0700 | Merge pull request #17 from TrueSightDAO/feature/beer-hall-review-advisory-snapshot-docs
a96ebfb | 2026-04-16 22:53:10 -0700 | docs(advisory): pair Beer Hall review with advisory snapshot refresh
67239b5 | 2026-04-16 22:26:41 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-17 UTC)
128764f | 2026-04-16 22:18:22 -0700 | docs(advisory): mobile quick-start links to BASE, index, snapshots.
4a43d08 | 2026-04-16 22:18:08 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-17 UTC)
19df969 | 2026-04-16 22:12:35 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-17 UTC)
f7fedd8 | 2026-04-16 15:57:16 -0700 | Document GAS editor URL header convention and SeaCoast ingest project.
7a88000 | 2026-04-16 13:49:01 -0700 | docs(openclaw): run Beer Hall archiver from ecosystem_change_logs clone
0206462 | 2026-04-16 13:15:59 -0700 | docs(openclaw): closed loop includes ecosystem_change_logs archive
903a2e4 | 2026-04-15 14:54:51 -0700 | docs: note go_to_market workflow for agroverse-inventory JSON publish
13d9751 | 2026-04-14 16:40:45 -0700 | docs(openclaw): Beer Hall digests include DApp Remarks (Hit List)
fe794b7 | 2026-04-14 14:42:51 -0700 | Merge pull request #16 from TrueSightDAO/feature/2026-04-14-qr-batch-and-shop-sku-context
6ed49f4 | 2026-04-14 14:42:18 -0700 | Document Agroverse QR batch compile and shop SKU farm/shipment grids
3327dc6 | 2026-04-14 13:40:15 -0700 | docs: no long-polling GitHub Actions for PR/CI (§3e, merge guidance)
f570a50 | 2026-04-14 12:03:06 -0700 | PROJECT_INDEX: EC2 terminate script under Cypher-Defense
13d6a4f | 2026-04-14 11:57:45 -0700 | Document Cypher-Defense for AWS IR and incident notes
2adddfd | 2026-04-11 14:12:55 -0700 | Merge pull request #13 from TrueSightDAO/docs/field-agent-hit-list-context
a3de6c9 | 2026-04-11 14:12:44 -0700 | docs: field agent Hit List pipeline + related context
```

### `tokenomics` → `tokenomics`

```
32ba059 | 2026-04-16 16:01:35 -0700 | SeaCoast ingest: default xAI model grok-3 (grok-2-latest invalid on API).
3645375 | 2026-04-16 15:57:16 -0700 | Document Apps Script editor URLs in google_app_scripts headers; index SeaCoast project.
1893d1c | 2026-04-16 14:10:48 -0700 | docs: drop private Edgar repo links from signature demo + SCHEMA (#224)
016f4d4 | 2026-04-16 13:54:18 -0700 | Docs: point digital signature demo README at sentiment_importer master sources. (#223)
9f9a743 | 2026-04-16 13:47:10 -0700 | Add Python demo for DApp digital signature sheet onboarding. (#222)
adaa924 | 2026-04-16 12:58:11 -0700 | Track seacoast ingest appsscript.json; unignore that path in .gitignore.
8ba66cd | 2026-04-16 12:57:52 -0700 | Add SeaCoast freight quotation ingest Apps Script (Gmail, Grok, GitHub PR).
df20521 | 2026-04-15 17:39:51 -0700 | chore(clasp): canonical Version.gs + ensure script; stop tracking mirror copies (#221)
8098c1a | 2026-04-15 17:39:48 -0700 | chore(agroverse-qr): refresh compiled QR PNGs for La do Sitio + Oscar Farm (#220)
bf36e30 | 2026-04-15 17:33:52 -0700 | Split Edgar verification email to admin GAS project; document identity scripts (#219)
94d6326 | 2026-04-12 17:29:58 -0700 | feat(agroverse-qr): Consolidate batch web Apps Script into qr_code_web_service.gs (#218)
767b9b5 | 2026-04-12 14:11:50 -0700 | feat(qr-gen): gate Agroverse batch on Telegram col P signature success
a85ab47 | 2026-04-12 13:37:54 -0700 | docs(schema): sync QR Code Sales L–R with code and Stripe append
61d8645 | 2026-04-12 13:32:49 -0700 | fix(gas): align QR Code Sales L–R with sheet layout (O tracking, P/Q attribution)
2a1f498 | 2026-04-12 13:28:56 -0700 | feat(gas): record IGNORED Telegram parses on QR Code Sales with Remarks
fe04aae | 2026-04-12 13:10:13 -0700 | chore(gas): refresh Version.gs changelog after clasp mirror push
dfc39c3 | 2026-04-12 13:09:32 -0700 | chore(gas): add Version.gs deploy log for tdg_inventory clasp mirrors
df9dd4c | 2026-04-12 13:05:24 -0700 | fix(sales telegram): stronger pre-Grok duplicate detection and id normalization
8bd3dda | 2026-04-12 12:54:22 -0700 | fix(sales telegram): skip Grok when heuristic QR already on QR Code Sales
ff43236 | 2026-04-12 12:45:59 -0700 | feat(qr sales): columns O/P for cash collector and sold-by; ledgers use O/P
0a66fc2 | 2026-04-11 14:12:30 -0700 | Merge pull request #217 from TrueSightDAO/docs/hit-list-field-agent-schema
fc4da80 | 2026-04-11 14:12:19 -0700 | docs(schema): Holistic Hit List field agent Recent Location tab
f82a298 | 2026-04-10 12:47:10 -0700 | Merge pull request #216 from TrueSightDAO/feature/qr-code-sales-l-through-o-extract
2dc11e0 | 2026-04-10 12:46:58 -0700 | feat(gas): QR Code Sales columns L–O for DApp sale fields
af3f8d7 | 2026-04-10 12:41:27 -0700 | Merge pull request #215 from TrueSightDAO/feature/qr-update-stripe-ledger-sales-shipping
2f98388 | 2026-04-10 12:41:11 -0700 | feat(gas): Stripe shipping sync for sales + robust QR update processing
2bda8c4 | 2026-04-10 11:36:52 -0700 | Merge pull request #214 from TrueSightDAO/feature/sales-reporter-gas-ledger-sync
269dc86 | 2026-04-10 11:36:33 -0700 | feat(gas): Sales reporter API and ledger sync for Stripe + owner email
```

### `dapp` → `dapp`

```
a4b7565 | 2026-04-16 16:16:24 -0700 | feat(report_contribution): paste file in description switches proof to upload (#155)
e148b58 | 2026-04-16 15:25:10 -0700 | feat(create_signature): auto-submit email verification when em+vk present (#154)
4779157 | 2026-04-16 12:42:20 -0700 | Parse freight lane JSON even when served as text/plain.
4ffd47e | 2026-04-16 12:39:55 -0700 | Improve freight lane loading UX and error messages.
a44fc61 | 2026-04-16 12:36:23 -0700 | Load freight lanes from audit JSON and estimate client-side.
844959f | 2026-04-15 17:33:55 -0700 | Polish create_signature onboarding layout and status placement (#153)
dda786d | 2026-04-13 12:50:11 -0700 | Stores nearby: hours in listings, expanded Open now, closed styling (#152)
10cb1b6 | 2026-04-12 17:38:50 -0700 | feat(dapp): batch QR manager picker, signed message, and URL state (#151)
ed3bedf | 2026-04-11 15:42:04 -0700 | Add stores_by_status.html for dapp.truesight.me deployment
1d91bcc | 2026-04-11 14:12:12 -0700 | Merge pull request #150 from TrueSightDAO/feature/field-agent-stores-nearby-save-location
fc77b7c | 2026-04-11 14:11:58 -0700 | feat(stores-nearby): field agent location save + tests
9d62176 | 2026-04-10 12:41:27 -0700 | Merge pull request #149 from TrueSightDAO/feature/shipping-provider-easypost-dapp
244eab7 | 2026-04-10 12:41:05 -0700 | feat(dapp): EasyPost USPS shipping provider on QR update and sales reporter
9a8c871 | 2026-04-10 11:36:52 -0700 | Merge pull request #148 from TrueSightDAO/feature/sales-reporter-stripe-and-metadata-ui
de21850 | 2026-04-10 11:36:29 -0700 | feat(sales-reporter): Stripe session picker, ledger fields, and wrapping
```

### `TrueChain` → `TrueChain`

```
_(no commits on origin/master in window)_
```

### `qr_codes` → `qr_codes`

```
_(no commits on origin/main in window)_
```

### `proposals` → `proposals`

```
_(no commits on origin/main in window)_
```

### `agroverse-inventory` → `agroverse-inventory`

```
c30b32f | 2026-04-17 11:28:50 -0700 | chore: refresh Agroverse store inventory snapshot
c5e2924 | 2026-04-15 15:33:16 -0700 | Merge pull request #1 from TrueSightDAO/chore/refresh-inventory-snapshots-2026-04-15
176e451 | 2026-04-15 15:31:29 -0700 | chore: refresh store and partner inventory snapshots
2872f1b | 2026-04-15 14:45:20 -0700 | Add partners-inventory.json snapshot alongside store inventory
5277872 | 2026-04-14 12:47:47 -0700 | chore: resolve inventory merge; sync 81% bar counts from ledgers
8ce3f08 | 2026-04-14 12:28:38 -0700 | chore: refresh Agroverse store inventory snapshot
0f53cfc | 2026-04-13 15:28:38 -0700 | chore: refresh Agroverse store inventory snapshot
01a7516 | 2026-04-12 14:28:44 -0700 | chore: refresh Agroverse store inventory snapshot
16fa64d | 2026-04-12 13:28:49 -0700 | chore: refresh Agroverse store inventory snapshot
4e111dc | 2026-04-12 11:28:39 -0700 | chore: refresh Agroverse store inventory snapshot
```

### `agroverse_shop` → `agroverse_shop_beta`

```
fe81a3b | 2026-04-16 13:08:13 -0700 | feat(taste-profile): add AGL2 chart and document implementation framework (#72)
23f8070 | 2026-04-15 16:10:36 -0700 | Merge pull request #71 from TrueSightDAO/fix/partner-inventory-after-gallery-2026-04-15
c4c47b2 | 2026-04-15 16:10:26 -0700 | fix(partners): place inventory block after venue gallery when present
aa09586 | 2026-04-15 15:53:08 -0700 | Merge pull request #70 from TrueSightDAO/feature/partner-pdp-inventory-snippet-ux-2026-04-15
40fd053 | 2026-04-15 15:52:52 -0700 | fix(partners): PDP inventory snippets — copy, images, layout, stock stack
3d37d8c | 2026-04-15 14:54:29 -0700 | Merge pull request #69 from TrueSightDAO/feature/partner-venue-inventory-snippets
3f332d1 | 2026-04-15 14:54:16 -0700 | feat(partners): show ledger venue inventory and optional online cart
9e58314 | 2026-04-14 16:58:20 -0700 | fix(partners): use PNG for Raven logo in img tags
62da857 | 2026-04-14 16:53:46 -0700 | Merge pull request #68 from TrueSightDAO/feature/2026-04-gtin-pdp-feed-blog-youtube-pipeline
8974e44 | 2026-04-14 16:52:35 -0700 | feat(partners): add Raven Things Collected (Echo Park) partner page
c10ae2e | 2026-04-14 16:29:41 -0700 | feat(shop): GTIN on PDPs and catalog feed; blog/video pipeline; nav and inventory
3474b4d | 2026-04-14 15:16:17 -0700 | feat(content): Kirsten hot chocolate blog, partner & 81% PDP embeds
336e1b2 | 2026-04-14 15:03:55 -0700 | fix(pdp): align product-page footers with canonical nav links
ef2c958 | 2026-04-14 15:01:21 -0700 | feat(shop): farm/shipment catalog snippets, related PDP, card alignment
6b63ede | 2026-04-14 14:43:52 -0700 | Merge pull request #66 from TrueSightDAO/feature/2026-04-14-sku-crosslinks-related-pdp
9c8ba62 | 2026-04-14 14:43:21 -0700 | Shop: 81% bar cross-listings on farms/shipments, related PDPs, checklist
cd5c049 | 2026-04-14 14:16:31 -0700 | feat(shop): 81% dark chocolate 50g Oscar and Santa Ana SKUs
eaf8668 | 2026-04-14 13:27:15 -0700 | fix(nav): AGL4 duplicate handlers; overlay test click; menu scroll on open
cb34076 | 2026-04-14 12:49:58 -0700 | chore: regenerate sitemap (blog URLs) for CI sitemap:check
63b962a | 2026-04-14 12:48:34 -0700 | feat(shop): 81% dark chocolate 50g Oscar and Santa Ana SKUs
```

### `iching_oracle` → `iching_oracle`

```
_(no commits on origin/main in window)_
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-04-16T224657Z_digest-2026-04-16.md`

- **posted_at_utc:** `2026-04-16T22:46:57Z`  
- **slug:** `digest-2026-04-16`  
- **Message 1 excerpt (first two non-empty lines):**

  *OpenClaw × Cursor — daily state of the DAO (not a manual post from Gary)*
  We made the public site easier to follow: truesight.me now surfaces a live, paginated list of published Beer Hall digests from git so anyone can skim what changed without hunting repos.

---

## Sheet evidence (sales)

_Canonical layouts: `tokenomics/SCHEMA.md` — **Monthly Statistics** on the main ledger; **QR Code Sales** on Telegram & Submissions. Figures are copied as-is from Sheets; verify before financial decisions._

### `Monthly Statistics` (last **14** non-empty rows)

| Year-Month | Monthly USD | Cumulative USD | Last updated |
|------------|-------------|------------------|---------------|
| 2025-03 | 1010 | 3854.96 | 2025-12-07 19:14:46 |
| 2025-04 | 1393.09 | 5248.05 | 2025-12-07 19:14:46 |
| 2025-05 | 825.37 | 6073.42 | 2025-12-07 19:14:46 |
| 2025-06 | 1552.45386 | 7625.87386 | 2025-12-07 19:14:46 |
| 2025-07 | 731 | 8356.87386 | 2025-12-07 19:14:46 |
| 2025-08 | 1011.96 | 9368.83386 | 2025-12-07 19:14:46 |
| 2025-09 | 734.72 | 10103.55386 | 2025-12-07 19:14:46 |
| 2025-10 | 595.22 | 10698.77386 | 2025-12-07 19:14:46 |
| 2025-11 | 268.97 | 10967.74386 | 2025-12-07 19:14:46 |
| 2025-12 | 1380.88 | 12348.62386 | 12/31/2025 |
| 2026-01 | 1063.94 | 13412.56386 | 1/31/2026 18:52:06 |
| 2026-02 | 144.42 | 13556.98386 | 2/28/2026 18:50:17 |
| 2026-03 | 273.97 | 13830.95386 | 3/31/2026 19:51:02 |
| 2026-04 | 163.68 | 13994.63386 | 4/17/2026 13:50:35 |

### `QR Code Sales` (up to **25** rows; `Sales Date` ≥ `2026-04-10`; scanned last **309** data rows)

| Sales date | Price | Currency / product | Status | QR (trunc.) | Stripe (suffix) | Remarks (trunc.) |
|-------------|-------|--------------------|--------|-------------|-------------------|--------------------|
| 2026-04-10 | 33.68 | Ceremonial Cacao Kraft Pouch - Alibaba:… | TOKENIZED | 2024OSCAR_20260330_38 | — | — |
| 2026-04-12 | 25 | Ceremonial Cacao Kraft Pouch - Alibaba:… | TOKENIZED | 2024OSCAR_20260330_37 | — | — |
| 2026-04-12 | 25 | 8 Ounce Package Kraft Pouch  CP34099273… | TOKENIZED | 2024OSCAR_20250711_NIBS_15 | — | — |
| 2026-04-13 | 5 | SunMint Tree Planting Pledge - QR Code | TOKENIZED | 20260413_FATIMA | — | — |
| 2026-04-17 | 12.5 | 81% Dark Chocolate Bar 50grams - Oscar … | TOKENIZED | 2024OSR_81PB_20260412_1 | — | — |
| 2026-04-17 | 12.5 | 81% Dark Chocolate Bar 50grams - Oscar … | TOKENIZED | 2024OSR_81PB_20260412_2 | — | — |
| 2026-04-17 | 12.5 | 81% Dark Chocolate Bar 50grams - Santa … | TOKENIZED | 2023SA_81PB_20260412_2 | — | — |
| 2026-04-17 | 12.5 | 81% Dark Chocolate Bar 50grams - Santa … | TOKENIZED | 2023SA_81PB_20260412_3 | — | — |

_Source IDs: main ledger `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, submissions `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`._

---

## Open reminders (cached JSON — action items)

_Open (not done) items loaded from `/Users/garyjob/Applications/market_research/automation/reminders_incomplete.json`; export with `rem list --incomplete -o json` or `scripts/export_advisory_reminders_json.sh` so **done** rows are never written. Refresh from a Mac when you want CI to mirror actionable tasks. When the user asks for **oracle response options**, propose **1–3** concrete next steps that honestly connect the hexagram reading to these open items where it fits; do **not** invent due dates or claim items are done._
_No open (not done) reminders in this source._

---

## Recent agent notes (`agentic_ai_context/notes/`)

_No `.md` / `.txt` under `notes/` modified in this window._

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
