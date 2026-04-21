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

- Generated (UTC): `2026-04-21T06:12:29Z`
- Look-back: **7** calendar days (`2026-04-14` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | $1,646 | 4% | `2026-12-31` | 254 | **behind** |
| USA Agroverse Partners | 100 | 26 | 26% | `2026-12-31` | 254 | on track |

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

_All dated lines on/after 2026-04-14_ (6):

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
| `oracle` | `iching_oracle` | **yes** |

---

## Git log by repo (origin default branch)

### `truesight_me` → `truesight_me_beta`

```
f9cfed7 | 2026-04-20 12:15:29 -0700 | Merge pull request #43 from TrueSightDAO/docs/add-markdown-mirror-alt-links
5a99cf4 | 2026-04-20 12:15:11 -0700 | Add (md) alt link next to each agreement: point LLMs at Markdown mirror
1182ede | 2026-04-20 11:54:03 -0700 | Merge pull request #42 from TrueSightDAO/docs/agreement-anchor-titles
d96c0b8 | 2026-04-20 11:53:47 -0700 | Agreement anchor text: use formal doc titles for clarity
f29f70e | 2026-04-20 11:51:09 -0700 | Merge pull request #41 from TrueSightDAO/docs/clarify-truetech-vs-brazilian-suppliers
35ad693 | 2026-04-20 11:50:50 -0700 | Agroverse whitepaper: clarify TrueTech Inc (US importer) ≠ Brazilian suppliers
1e0f787 | 2026-04-20 11:45:39 -0700 | Merge pull request #40 from TrueSightDAO/fix/broken-partnership-agreement-links
c8a6394 | 2026-04-20 11:45:16 -0700 | Fix 31 partnership-agreement links: redirect → direct Google Doc URLs
7a1f435 | 2026-04-20 11:29:07 -0700 | Merge pull request #39 from TrueSightDAO/feature/rename-start-script
efb177d | 2026-04-20 11:28:56 -0700 | Rename start_server.sh to start_local.sh (standardize across repos)
f507df8 | 2026-04-20 11:18:26 -0700 | Merge pull request #38 from TrueSightDAO/docs/drop-vault-standard-rate-add-review-proposal-nav
6489dce | 2026-04-20 11:18:07 -0700 | Whitepaper: drop Vault + Standard Rate; nav "Proposals" → "Review & vote"
b5b546f | 2026-04-20 11:11:54 -0700 | Merge pull request #37 from TrueSightDAO/docs/whitepaper-accuracy-and-drop-gas-fee
dc0bbc2 | 2026-04-20 11:11:29 -0700 | Whitepapers: drop Gas Fee; define Edgar/TrueChain/Oracle; Beer Hall archive-only
bcbf5e6 | 2026-04-20 10:50:25 -0700 | Merge pull request #36 from TrueSightDAO/feat/agroverse-partnership-economics
7c376d0 | 2026-04-20 10:45:24 -0700 | docs: communications architecture; drop prisoner-dilemma framing (#35)
544ce84 | 2026-04-20 10:43:36 -0700 | agroverse: add unit economics + partnership shapes; fix 2.65% fee
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
5c7a127 | 2026-04-20 23:08:27 -0700 | Merge pull request #62 from TrueSightDAO/fix/beer-hall-workflow-commit-beer-hall-files
d163ffc | 2026-04-20 23:08:07 -0700 | beer-hall-digest-daily: commit beer_hall/ files before advisory step
e4d046e | 2026-04-20 12:11:18 -0700 | Merge pull request #61 from TrueSightDAO/feat/export-google-docs-workflow
95adadc | 2026-04-20 12:10:54 -0700 | Add export-google-docs workflow — daily Markdown mirror of partnership Docs
4465255 | 2026-04-20 11:28:13 -0700 | feat(newsletter): reusable Gmail send/draft flow with sheet logging + opt-in open tracking (#60)
179d390 | 2026-04-19 15:27:38 -0700 | Merge pull request #59 from TrueSightDAO/chore/drop-whatsapp-retirement-header
9e6d351 | 2026-04-19 15:27:22 -0700 | draft_beer_hall_digest: drop redundant WhatsApp-retired header
dbee4af | 2026-04-19 15:10:29 -0700 | Merge pull request #58 from TrueSightDAO/chore/beer-hall-daily-cadence
1641850 | 2026-04-19 15:10:14 -0700 | Beer Hall digest: daily cadence + auto-merge PRs
9c68b19 | 2026-04-19 15:00:16 -0700 | Merge pull request #57 from TrueSightDAO/feat/advisory-beer-hall-automation
e2bce7d | 2026-04-19 14:59:31 -0700 | Automate advisory snapshot refresh + weekly Beer Hall digest
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
```

### `agentic_ai_context` → `agentic_ai_context`

```
97aee49 | 2026-04-20 23:09:31 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
dabdd20 | 2026-04-20 23:09:30 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
26d8542 | 2026-04-20 20:51:14 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
c9cff6a | 2026-04-20 20:51:13 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
82488a0 | 2026-04-20 19:14:55 -0700 | Merge pull request #31 from TrueSightDAO/auto/advisory-refresh-2026-04-21
8b5e128 | 2026-04-21 02:14:46 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
b53bf56 | 2026-04-20 12:40:52 -0700 | chore(previews): refresh Beer Hall preview (2026-04-20 UTC)
581cdbc | 2026-04-20 12:40:50 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-20 UTC)
6cc2d49 | 2026-04-20 11:29:36 -0700 | docs: add Agroverse newsletter workflow for AI assistants (#30)
3151d62 | 2026-04-20 07:19:32 -0700 | chore(previews): refresh Beer Hall preview (2026-04-20 UTC)
335a465 | 2026-04-20 07:19:31 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-20 UTC)
046269f | 2026-04-20 01:34:05 -0700 | chore(previews): refresh Beer Hall preview (2026-04-20 UTC)
6af2189 | 2026-04-20 01:34:04 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-20 UTC)
fd23b73 | 2026-04-19 20:58:00 -0700 | chore(previews): refresh Beer Hall preview (2026-04-20 UTC)
16bd6f7 | 2026-04-19 20:57:59 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-20 UTC)
fead069 | 2026-04-19 19:27:52 -0700 | Merge pull request #29 from TrueSightDAO/auto/advisory-refresh-2026-04-20
7bf1e1a | 2026-04-20 02:27:43 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-20 UTC)
39f25f9 | 2026-04-19 15:14:18 -0700 | Merge pull request #28 from TrueSightDAO/docs/automate-beer-hall-and-reminders-pipeline
3dec1d1 | 2026-04-19 15:13:56 -0700 | docs: Beer Hall WhatsApp retired; daily automation + Reminders pipeline
5c5c21c | 2026-04-19 15:13:49 -0700 | Merge pull request #27 from TrueSightDAO/auto/advisory-refresh-2026-04-19
c3e2490 | 2026-04-19 22:13:40 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-19 UTC)
5ee7330 | 2026-04-19 15:09:51 -0700 | Merge pull request #25 from TrueSightDAO/auto/advisory-refresh-2026-04-19
cb87804 | 2026-04-19 15:09:11 -0700 | Merge pull request #26 from TrueSightDAO/feat/purpose-mission-and-beer-hall-audience-filter
80d0550 | 2026-04-19 22:06:13 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-19 UTC)
2769e45 | 2026-04-19 14:43:21 -0700 | Merge pull request #24 from TrueSightDAO/chore/advisory-snapshot-beer-hall-2026-04-19
504af42 | 2026-04-19 14:42:59 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT + Beer Hall preview (2026-04-19)
e29461a | 2026-04-19 14:17:42 -0700 | Merge main (advisory snapshot + beer hall preview PR #23)
b511a84 | 2026-04-19 14:17:35 -0700 | Merge pull request #23 from TrueSightDAO/chore/advisory-snapshot-beer-hall-preview-2026-04-19
b91cb0c | 2026-04-19 14:17:21 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT and Beer Hall preview
4c2e91b | 2026-04-19 14:01:29 -0700 | Merge main into feat branch (pick up WORKSPACE_CONTEXT §3c column D)
959035d | 2026-04-19 14:01:11 -0700 | Merge pull request #22 from TrueSightDAO/docs/offchain-column-d-numeric
739e2a3 | 2026-04-19 14:00:41 -0700 | docs(ledger): require numeric amounts in offchain transactions column D
9d24cbe | 2026-04-19 13:30:24 -0700 | feat(advisory/comms): add PURPOSE_AND_MISSION north star; filter Beer Hall (#21)
5e6585e | 2026-04-19 13:27:14 -0700 | feat(advisory/comms): add PURPOSE_AND_MISSION north star; filter Beer Hall
1d31eb3 | 2026-04-19 13:12:47 -0700 | Merge pull request #20 from TrueSightDAO/docs/repackaging-edgar-route
33421ff | 2026-04-19 13:12:37 -0700 | docs(ledger): document Edgar-routed repackaging planner flow
9f3e138 | 2026-04-18 15:08:56 -0700 | fix(advisory): goal is 2026 YTD sales, not cumulative since inception (#19)
4450a6e | 2026-04-18 14:18:29 -0700 | feat(advisory): add operator-curated stubs for ADVISORY_SNAPSHOT strategic frame (#18)
a299443 | 2026-04-17 16:30:35 -0700 | chore(advisory): refresh snapshot + Beer Hall preview (2026-04-17 UTC)
91cb5bd | 2026-04-17 13:56:35 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-17 UTC)
… (truncated)
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
```

### `dapp` → `dapp`

```
ec3cb4a | 2026-04-20 11:30:11 -0700 | Merge pull request #158 from TrueSightDAO/feature/rename-start-script
ef8bb26 | 2026-04-20 11:30:00 -0700 | Rename serve_local.sh to start_local.sh, default port 8081
e0f868c | 2026-04-18 21:39:36 -0700 | Merge pull request #157 from TrueSightDAO/feat/repackaging-planner-edgar-route
ba2ccea | 2026-04-18 21:39:05 -0700 | feat(repackaging_planner): route through Edgar with signed payload + UX rewrite
f89e75e | 2026-04-17 16:03:20 -0700 | feat(batch-qr): update GAS URL to new admin@truesight.me project (#156)
a4b7565 | 2026-04-16 16:16:24 -0700 | feat(report_contribution): paste file in description switches proof to upload (#155)
e148b58 | 2026-04-16 15:25:10 -0700 | feat(create_signature): auto-submit email verification when em+vk present (#154)
4779157 | 2026-04-16 12:42:20 -0700 | Parse freight lane JSON even when served as text/plain.
4ffd47e | 2026-04-16 12:39:55 -0700 | Improve freight lane loading UX and error messages.
a44fc61 | 2026-04-16 12:36:23 -0700 | Load freight lanes from audit JSON and estimate client-side.
844959f | 2026-04-15 17:33:55 -0700 | Polish create_signature onboarding layout and status placement (#153)
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
0da1893 | 2026-04-20 08:30:22 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
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
```

### `agroverse_shop` → `agroverse_shop_beta`

```
c5d8696 | 2026-04-20 11:28:06 -0700 | Merge pull request #75 from TrueSightDAO/feature/rename-start-script
0ce62b7 | 2026-04-20 11:27:55 -0700 | Rename start-local-server.sh to start_local.sh (standardize across repos)
6090cab | 2026-04-19 15:57:44 -0700 | chore(agl6): live YouTube embed for São Jorge hot chocolate (gw2vIxPCcyQ)
567db30 | 2026-04-19 15:41:11 -0700 | publish sao jorge fazenda (#73)
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
546dbd9 | 2026-04-19 20:59:22 -0700 | fix(oracle): wrap long tokens in advisory panel; prevent overflow (#7)
9ca7ab8 | 2026-04-19 20:57:54 -0700 | feat(oracle): switch advisor to Claude with prompt caching; revised prompt (#6)
3ae6cfa | 2026-04-19 20:44:13 -0700 | feat(oracle): surface iPhone reminder intents pending since last Mac sync (#5)
67bd3bc | 2026-04-17 15:32:00 -0700 | Merge pull request #4 from TrueSightDAO/feature/oracle-gas-version-control
6ed09fb | 2026-04-17 15:25:57 -0700 | feat(gas): version-control oracle advisory bridge GAS source
70ee47d | 2026-04-16 23:40:56 -0700 | Merge pull request #3 from TrueSightDAO/fix/oracle-advisory-initial-visibility
490fbbf | 2026-04-16 23:40:48 -0700 | fix(oracle): keep advisory controls hidden until response
4a5635e | 2026-04-16 23:35:09 -0700 | Merge pull request #2 from TrueSightDAO/feature/oracle-advisory-loading-and-context-links
78d71fe | 2026-04-16 23:35:00 -0700 | feat(oracle): refine advisory actions visibility and context links
b2cf048 | 2026-04-16 23:28:02 -0700 | Merge pull request #1 from TrueSightDAO/feature/oracle-dao-advisory-ux
8059c9e | 2026-04-16 23:27:31 -0700 | feat(oracle): add DAO advisory panel and contribution CTA
```

### `Cypher-Defense` _(no clone)_

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-04-21T061005Z_whitepaper-oracle-claude-email-marketing-live.md`

- **posted_at_utc:** `2026-04-21T06:10:05Z`  
- **slug:** `whitepaper-oracle-claude-email-marketing-live`  
- **Message 1 excerpt (first two non-empty lines):**

  Busy week across the stack — whitepaper accuracy, Oracle upgrades, email marketing scaffolding, São Jorge farm page, and ongoing AWS security follow-through.
  - Whitepapers updated to be agentic-AI-friendly: Gas Fee section dropped, Edgar/TrueChain/Oracle terms defined, TrueTech Inc correctly distinguished from Brazilian suppliers, Beer Hall described as archive-only, and 31 broken partnership-agreement links fixed with direct Google Doc URLs.

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

---

## Open reminders (macOS `rem` — action items)

_Open (not done) items from Reminders.app (`rem list --incomplete -o json`). When the user asks for **oracle response options**, propose **1–3** concrete next steps that honestly connect the hexagram reading to these **actionable** items where it fits; do **not** invent due dates or claim items are done._
_Showing **60** of **108** open reminders (cap `--rem-limit`)._

| Title | List | Due (date) | Flagged | Notes (trunc.) |
|-------|------|------------|---------|------------------|
| Follow up with USPS claims | Reminders | `2025-04-07` | — | — |
| Send Matthew the Dizajn | Reminders | `2025-09-11` | — | — |
| Get cursor to look into the AWS charges still coming to my account | Reminders | `2026-01-29` | — | — |
| Look at the influencer platform that a surface and a beer hall | Reminders | `2026-01-29` | — | — |
| Spinner an instance for the RAG architecture | Reminders | `2026-01-29` | — | — |
| Look to order photos of the storage shop listed by AI | Reminders | `2026-04-21` | — | — |
| Review my Clock subscription package | Reminders | `2026-05-09` | — | — |
| [FEATURE] Allow the module where people can add their own photo for the… | Reminders | `—` | — | — |
| [priority] Look through AI generated emails, edit and send them out | Reminders | `—` | — | — |
| Additional consideration: one DAO member has flagged that having inform… | Reminders | `—` | — | — |
| Allow remark to be expendable when retractable in mobile | Reminders | `—` | — | — |
| Allow upload of MH for the store nearby status submission | Reminders | `—` | — | — |
| Allow upload of MH to the stores nearby status submission | Reminders | `—` | — | — |
| Also have a conversation with multiple items are combine together to be… | Reminders | `—` | — | — |
| Also record a composition | Reminders | `—` | — | — |
| Andrew is pretty impressed by the fact that it is a community project | Reminders | `—` | — | — |
| Build up a dashboard for all the trees belong to the same email address | Reminders | `—` | — | — |
| Buy the battery back up tomorrow on amazon.com | Reminders | `—` | — | — |
| Check the time and Spam packaging to cut out as well as expenses | Reminders | `—` | — | — |
| Choclate has an API block post | Reminders | `—` | — | — |
| Communication architecture of TrueSight DAO | Reminders | `—` | — | — |
| Create a donation receipt | Reminders | `—` | — | — |
| Create a mobile app that venue owners can use to set the price | Reminders | `—` | — | — |
| Create a mod for registering new members | Reminders | `—` | — | — |
| Create a route for the wine Kenosha | Reminders | `—` | — | — |
| Create an expected physical pop-up expansion | Reminders | `—` | — | — |
| Create an instance of the iOS native app using cursor AI | Reminders | `—` | — | — |
| Create the volunteer estimator for the different places that are sellin… | Reminders | `—` | — | — |
| Create tutorial for Deckers | Reminders | `—` | — | — |
| Download Prince of tights | Reminders | `—` | — | — |
| Easy post calculate Sweet spot for postal rate across all the different… | Reminders | `—` | — | — |
| Extend debt with the transforming of inventory from one | Reminders | `—` | — | — |
| Figure out how to be a reasonable schedule by another four weeks from $… | Reminders | `—` | — | — |
| Figure out how to social proof like the Michelin star list | Reminders | `—` | — | — |
| Follow up with all the Desert resell us on April 16 after our Cacao com… | Reminders | `—` | — | — |
| Follow up with Fatima on Wednesday regarding the quotation from Santa A… | Reminders | `—` | — | — |
| Follow up with Liz Wong on Monday regarding the proposal that she menti… | Reminders | `—` | — | — |
| Follow up with Matthews on Monday regarding the follow up with the Omeg… | Reminders | `—` | — | — |
| Follow up with the dude that dust incense from Nathan's fire | Reminders | `—` | — | — |
| Follow up with the people on our email list | Reminders | `—` | — | — |
| Garfield Street and box Canyon Road | Reminders | `—` | — | — |
| Generate the auto follower feature | Reminders | `—` | — | — |
| Get Hwang to send over the USDANOP certification for the new part | Reminders | `—` | — | — |
| Get Ken a shirt | Reminders | `—` | — | — |
| Go visit the board stores to see and figure out why the seller rate is … | Reminders | `—` | — | — |
| https://a.co/d/0jhwOqgO | Reminders | `—` | — | U Organic Dark Chocolate 10 Bars x 1.58 Ounce 85% Cacao - Kosher Gluten & Allergen Free Vegan -… |
| I'm at Pov 169 | Reminders | `—` | — | — |
| Include the CEPOTX fund video | Reminders | `—` | — | — |
| Include the inventory level as well as Kirsten and Matheus special posi… | Reminders | `—` | — | — |
| Include Western Union for withdrawal | Reminders | `—` | — | — |
| Indicating where the venues the banks are available | Reminders | `—` | — | — |
| Integrate the identity protocol to reverse.shop | Reminders | `—` | — | — |
| Interesting reference | Reminders | `—` | — | Book: Let this radicalize you  Documentary: No fun city |
| John Oliver carbon credit black hole | Reminders | `—` | — | — |
| Just maybe follow up before the email addresses harvested | Reminders | `—` | — | — |
| Larger more established retailers Symphony telling them that I am the d… | Reminders | `—` | — | — |
| Let the Oracle know that Kirsten and Matheus are the main warehouses | Reminders | `—` | — | — |
| List on etsy amazon.com and google search | Reminders | `—` | — | — |
| Liz is having issues because she was never selling directly to consumers | Reminders | `—` | — | — |
| Look at cat.io website | Reminders | `—` | — | — |

### Suggestion seeds (titles only)

- Follow up with USPS claims
- Send Matthew the Dizajn
- Get cursor to look into the AWS charges still coming to my account
- Look at the influencer platform that a surface and a beer hall
- Spinner an instance for the RAG architecture
- Look to order photos of the storage shop listed by AI
- Review my Clock subscription package
- [FEATURE] Allow the module where people can add their own photo for the front page cover of the chocolate bar
- [priority] Look through AI generated emails, edit and send them out
- Additional consideration: one DAO member has flagged that having information split across the blog, landing page, potential chatbot, and WhatsApp creates UX fragmentation — she doesn’t want to click multiple links to piece together context. Consider whether the recommendation should include a consolidated hub page (possibly on the landing page itself) that surfaces the latest blog posts, the daily ops compilation, and the chatbot input field in one place, so the underlying infrastructure separation doesn’t burden the end user.
- Allow remark to be expendable when retractable in mobile
- Allow upload of MH for the store nearby status submission
- Allow upload of MH to the stores nearby status submission
- Also have a conversation with multiple items are combine together to become a new item
- Also record a composition
- Andrew is pretty impressed by the fact that it is a community project
- Build up a dashboard for all the trees belong to the same email address
- Buy the battery back up tomorrow on amazon.com
- Check the time and Spam packaging to cut out as well as expenses
- Choclate has an API block post
- Communication architecture of TrueSight DAO
- Create a donation receipt
- Create a mobile app that venue owners can use to set the price
- Create a mod for registering new members

_… **48** more open reminders not shown (raise `--rem-limit`)._

---

## Recent agent notes (`agentic_ai_context/notes/`)

_No `.md` / `.txt` under `notes/` modified in this window._

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
