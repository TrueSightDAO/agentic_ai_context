# ADVISORY_SNAPSHOT

Machine-oriented digest of **recent evidence** for LLM advisors. Git lines are **proxies** for shipped work, not verified outcomes.

---

## Purpose & Mission (north star)

**Purpose:** Heal the world with love.

**Mission:** Restore 10,000 hectares of Amazon rainforest.

---

_This is the north star. Every advisory suggestion — product, partnerships, fundraising, operations, hiring, or growth — should be traceable back to whether it moves us toward restoring 10,000 hectares of Amazon rainforest, in service of healing the world with love._

_When two paths both appear valid, prefer the one that more directly advances the mission. When the mission is not obviously relevant, default to decisions that preserve trust, community, and long-term optionality rather than short-term metrics alone._

---

## Meta

- Generated (UTC): `2026-04-19T21:40:15Z`
- Look-back: **7** calendar days (`2026-04-12` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | $1,646 | 4% | `2026-12-31` | 256 | **behind** |
| USA Agroverse Partners | 100 | 26 | 26% | `2026-12-31` | 256 | on track |

---

## Constraints / risks this week

_Current bottlenecks for growth. 3–5 bullets, keep under 15 lines._
_Examples of constraint types: capital, inventory, fulfilment, volunteer hours, distribution reach._

<!-- TODO: replace the examples below with real constraints and delete this comment.
Examples:
- Inventory: 2024SJ batch near-exhausted; next shipment ETA 2026-05-15
- Volunteer capacity: only 2 operators available for weekend fulfilment
- Distribution: no warehouse presence outside SF Bay Area
-->

---

## Operator metrics (manual, 7-day)

_Manually-maintained weekly snapshot of key numbers that can't be auto-derived._
_Update once per week. For auto-pulled sheet data, see `--with-sheet-sales`._

<!-- TODO: replace the examples below with real metrics and delete this comment.
Examples:
- Units sold (7-day): 42 (+12% WoW)
- New customer emails: 18
- Treasury: $3,450 USDC + 12M TDG
- Active Telegram members: 187
- Open Stripe checkout sessions without tracking: 4
-->

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_No lines matched name/keyword heuristics in this window._

_All dated lines on/after 2026-04-12_ (8):

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
```

### `market_research` → `go_to_market`

```
b9c368d | 2026-04-19 14:38:29 -0700 | Merge pull request #56 from TrueSightDAO/chore/beer-hall-retire-openclaw-send
b5124bb | 2026-04-19 14:38:03 -0700 | Beer Hall: retire OpenClaw WhatsApp send; archive + advisory-snapshot only
2ce3e97 | 2026-04-19 13:30:21 -0700 | feat(advisory): render Purpose & Mission north-star block at top of snapshot (#55)
dabd348 | 2026-04-18 14:59:32 -0700 | fix(advisory): read filter from source, add starts_with predicate (#54)
e607577 | 2026-04-18 14:18:25 -0700 | feat(advisory): add operator-curated strategic blocks to ADVISORY_SNAPSHOT (#53)
5440b17 | 2026-04-18 11:53:45 -0700 | Merge pull request #52 from TrueSightDAO/add-oracle-cypher-defense-repos
bea9b7b | 2026-04-18 11:53:15 -0700 | Add oracle and Cypher-Defense repos to REPOS poll lists
8b4e413 | 2026-04-17 16:16:10 -0700 | Merge pull request #51 from TrueSightDAO/fix/telegram-digest-edgar-parser
b50b0f2 | 2026-04-17 16:15:50 -0700 | fix(digest): parse Edgar event fields in Telegram log helper
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
```

### `agentic_ai_context` → `agentic_ai_context`

```
b511a84 | 2026-04-19 14:17:35 -0700 | Merge pull request #23 from TrueSightDAO/chore/advisory-snapshot-beer-hall-preview-2026-04-19
b91cb0c | 2026-04-19 14:17:21 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT and Beer Hall preview
959035d | 2026-04-19 14:01:11 -0700 | Merge pull request #22 from TrueSightDAO/docs/offchain-column-d-numeric
739e2a3 | 2026-04-19 14:00:41 -0700 | docs(ledger): require numeric amounts in offchain transactions column D
9d24cbe | 2026-04-19 13:30:24 -0700 | feat(advisory/comms): add PURPOSE_AND_MISSION north star; filter Beer Hall (#21)
1d31eb3 | 2026-04-19 13:12:47 -0700 | Merge pull request #20 from TrueSightDAO/docs/repackaging-edgar-route
33421ff | 2026-04-19 13:12:37 -0700 | docs(ledger): document Edgar-routed repackaging planner flow
9f3e138 | 2026-04-18 15:08:56 -0700 | fix(advisory): goal is 2026 YTD sales, not cumulative since inception (#19)
4450a6e | 2026-04-18 14:18:29 -0700 | feat(advisory): add operator-curated stubs for ADVISORY_SNAPSHOT strategic frame (#18)
a299443 | 2026-04-17 16:30:35 -0700 | chore(advisory): refresh snapshot + Beer Hall preview (2026-04-17 UTC)
91cb5bd | 2026-04-17 13:56:35 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-17 UTC)
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
```

### `tokenomics` → `tokenomics`

```
20bf43c | 2026-04-19 13:11:19 -0700 | Merge pull request #228 from TrueSightDAO/feat/inventory-api-agl-unit-cost-lookup
b9103e5 | 2026-04-19 13:10:51 -0700 | feat(inventory-api): resolve AGL Balance unit_cost from main Currencies tab
cfd760f | 2026-04-18 14:17:53 -0700 | perf(gas): fix 30-min trigger timeouts on telegram log processors (#227)
c421451 | 2026-04-18 13:21:19 -0700 | feat(agroverse-qr): multi-item Stripe session link via column Z on QR codes (#226)
4fc9491 | 2026-04-17 16:03:18 -0700 | feat(agroverse-qr): migrate qr_code_web_service to admin@truesight.me and consolidate owner emails (#225)
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
```

### `dapp` → `dapp`

```
e0f868c | 2026-04-18 21:39:36 -0700 | Merge pull request #157 from TrueSightDAO/feat/repackaging-planner-edgar-route
ba2ccea | 2026-04-18 21:39:05 -0700 | feat(repackaging_planner): route through Edgar with signed payload + UX rewrite
f89e75e | 2026-04-17 16:03:20 -0700 | feat(batch-qr): update GAS URL to new admin@truesight.me project (#156)
a4b7565 | 2026-04-16 16:16:24 -0700 | feat(report_contribution): paste file in description switches proof to upload (#155)
e148b58 | 2026-04-16 15:25:10 -0700 | feat(create_signature): auto-submit email verification when em+vk present (#154)
4779157 | 2026-04-16 12:42:20 -0700 | Parse freight lane JSON even when served as text/plain.
4ffd47e | 2026-04-16 12:39:55 -0700 | Improve freight lane loading UX and error messages.
a44fc61 | 2026-04-16 12:36:23 -0700 | Load freight lanes from audit JSON and estimate client-side.
844959f | 2026-04-15 17:33:55 -0700 | Polish create_signature onboarding layout and status placement (#153)
dda786d | 2026-04-13 12:50:11 -0700 | Stores nearby: hours in listings, expanded Open now, closed styling (#152)
10cb1b6 | 2026-04-12 17:38:50 -0700 | feat(dapp): batch QR manager picker, signed message, and URL state (#151)
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
ac9568e | 2026-04-19 21:32:47 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
89d4c64 | 2026-04-19 14:03:03 -0700 | feat(gas): add editor-runnable wrappers for repackaging-currency-ingest (#3)
0f5ccf7 | 2026-04-19 13:37:30 -0700 | chore(inventory): repackaging composition 67c88267-b41c-4eab-8ef5-d5be48854d65
9353975 | 2026-04-19 13:37:29 -0700 | chore(inventory): refresh currencies.json (repackaging ingest)
1f830fc | 2026-04-18 21:40:40 -0700 | Merge pull request #2 from TrueSightDAO/feat/repackaging-currency-ingest-gas
d6f5f90 | 2026-04-18 21:40:31 -0700 | feat(gas): add repackaging-currency-ingest Apps Script + doGet processor
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

### `iching_oracle` → `oracle`

```
_(no commits on origin/main in window)_
```

### `Cypher-Defense` _(no clone)_

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-04-19T213956Z_retire-whatsapp-oracle-and-reminders-live.md`

- **posted_at_utc:** `2026-04-19T21:39:56Z`  
- **slug:** `retire-whatsapp-oracle-and-reminders-live`  
- **Message 1 excerpt (first two non-empty lines):**

  OpenClaw × Cursor digest — retired from WhatsApp posting; archive-only for oracle / feed context (not a manual post from Gary)
  - Cybernetic Oracle is live. oracle.truesight.me now draws a hexagram and passes DAO state (advisory snapshot, strategic blocks, open reminders) to Grok for a grounded reading. GAS backend version-controlled.

### `beer-hall_2026-04-18T223617Z_qr-email-migration-admin-truesight-advisory-goals.md`

- **posted_at_utc:** `2026-04-18T22:36:17Z`  
- **slug:** `qr-email-migration-admin-truesight-advisory-goals`  
- **Message 1 excerpt (first two non-empty lines):**

  *OpenClaw × Cursor — daily state of the DAO (not a manual post from Gary)*
  - Owners buying multiple QR-coded items in a single Stripe checkout now get ONE onboarding email listing all their tracking links, instead of one email per item

### `beer-hall_2026-04-17T232946Z_partner-inventory-81pct-skus-kirsten-sales.md`

- **posted_at_utc:** `2026-04-17T23:29:46Z`  
- **slug:** `partner-inventory-81pct-skus-kirsten-sales`  
- **Message 1 excerpt (first two non-empty lines):**

  *OpenClaw × Cursor — daily state of the DAO (not a manual post from Gary)*
  - Partners selling our cacao in LA can now see their live stock levels directly on their agroverse.shop page — less back-and-forth on how much inventory they have left

---

## Recent agent notes (`agentic_ai_context/notes/`)

_No `.md` / `.txt` under `notes/` modified in this window._

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
