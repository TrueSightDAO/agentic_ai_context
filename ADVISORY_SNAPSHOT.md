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

- Generated (UTC): `2026-04-20T08:33:51Z`
- Look-back: **7** calendar days (`2026-04-13` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | — | — | `2026-12-31` | 255 | — |
| USA Agroverse Partners | 100 | — | — | `2026-12-31` | 255 | — |

_Notes: (live fetch skipped: missing `google_credentials.json`)_

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

_Lines in window matching configured names or status keywords:_

- 2026-04-19 | claude | **iOS Reminders → oracle pipeline:** New Rails endpoint **`POST https://edgar.truesight.me/oracle/reminders_sync`** in **`sentiment_importer`** (`app/controllers/oracle/reminders_sync_controller.rb`). Bearer-auth'd, accepts any POST body (any content-type — iOS Shortcuts sends iCalendar VTODO despite JSON header) and archives verbatim to **`ecosystem_change_logs/reminders_raws/<UTC-timestamp>.json`** via GitHub Contents API. Credentials (`oracle_sync_token`, `github_pat`) in `config/application.rb` (not env). The oracle GAS at `oracle.truesight.me` still reads `ecosystem_change_logs/reminders/current.json` — downstream parser from raw archive to current.json is TODO.

_All dated lines on/after 2026-04-13_ (8):

- 2026-04-14 | cursor | **GitHub CI / PR merge:** Do **not** long-poll Actions (**`gh pr checks --watch`**, **`gh run watch`**, sleep loops). Prefer one **`gh pr checks`** snapshot, local tests (`npm test` / Playwright), then hand off PR + Actions URLs. **`WORKSPACE_CONTEXT.md` §3e**, **`GITHUB_AGENTIC_AI_SSH.md`** merge bullets, **`WORKSPACE_CONTEXT.md` §5** (Agroverse Shop CI bullet).
- 2026-04-14 | cursor | **Agroverse QR codes** (main ledger `1GE7PUq…` tab *Agroverse QR codes*): **Column I (`Currency`)** values are tied to **`Currencies`!A** (same workbook; external reference / IMPORTRANGE pattern—exact string for ledger & sales validation). **Regional promo IDs (column A):** operator prefers **`LA`** (Los Angeles); **`CC`** = ceremonial cacao, **`CT`** = cacao tea (tokens in ids like `AUSTIN_CC_…`). Local label compile: **`tokenomics/python_scripts/agroverse_qr_code_generator/batch_compiler.py`** reads **A–H** only; keep **A** short. **`NOTES_tokenomics.md`**, **`WORKSPACE_CONTEXT.md` §3/§4**, **`tokenomics/SCHEMA.md`** (*Agroverse QR codes* column I).
- 2026-04-14 | cursor | **Agroverse QR batch playbook:** Added **`AGROVERSE_QR_CODE_BATCH_GENERATION.md`** (sheet **A–V**, **K** GitHub `compiled_` formula, **`batch_compiler.py`** + venv + **`to_print/`**, automation notes). **`README.md`** Contents + how-to **§17**; **`WORKSPACE_CONTEXT.md` §5**; **`NOTES_tokenomics.md`** cross-link; **`PROJECT_INDEX.md`** tokenomics row.
- 2026-04-14 | cursor | **LA batch QR fix:** Sheet rows **`LA_*_20260414_*`** — **E–H** reset from reference (**CC** → Oscar Farm/Bahia/Brazil/2024; **CT** → La do Sitio/Para/Brazil/2024); removed **`compiled_Los_Angeles_*.png`**, regenerated **`compiled_Oscar_Farm_*.png`** / **`compiled_La_do_Sitio_*.png`**. **`AGROVERSE_QR_CODE_BATCH_GENERATION.md`** — **E–H** must follow template farm, not handout city unless operator asks.
- 2026-04-14 | cursor | **agroverse.shop new SKU — farm/shipment grids:** Added **`AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md`** ( **`item-card`** on **`farms/*/index.html`** + **`shipments/agl*/index.html`** after new **`product-page/`**). **`PRODUCT_DEVELOPMENT_SPECS.md` §1/§3**, **`README.md`**, **`OPERATING_INSTRUCTIONS.md`**, **`WORKSPACE_CONTEXT.md` §4/§5**, **`PROJECT_INDEX.md`** (agroverse_shop); **`agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md`** new section + template bullets.
- 2026-04-16 | cursor | **Tokenomics GAS headers:** Every **`tokenomics/google_app_scripts/**/*.gs`** now documents **`Apps Script editor:`** `https://script.google.com/home/projects/<scriptId>/edit` (or N/A for deprecated stubs) per **`clasp_mirrors/PROJECT_INDEX.md`**. **`NOTES_tokenomics.md`** — index link + SeaCoast ingest row (`1gi4YKh2…`). SeaCoast **`Code.gs`** header order normalized.
- 2026-04-19 | claude | **Beer Hall + advisory snapshot automation:** WhatsApp posting via OpenClaw **retired**; digest is now archive-only. Added **`market_research/.github/workflows/advisory-snapshot-refresh.yml`** (every 6 h) and **`beer-hall-digest-daily.yml`** (00:00 UTC daily, auto-merges PRs). New **`market_research/scripts/draft_beer_hall_digest.py`** calls Claude Sonnet 4.6 via the anthropic SDK to draft Message 1 + Message 2 from the preview + latest 2 archives as few-shot examples. New repo secret: **`ORACLE_ADVISORY_PUSH_TOKEN`** (fine-grained PAT, Contents+PR Read/Write on `ecosystem_change_logs` and `agentic_ai_context`). `ANTHROPIC_API_KEY` also added. **`WORKSPACE_CONTEXT.md` §3d** rewritten; **`OPENCLAW_WHATSAPP.md`** Beer Hall section marked legacy.
- 2026-04-19 | claude | **iOS Reminders → oracle pipeline:** New Rails endpoint **`POST https://edgar.truesight.me/oracle/reminders_sync`** in **`sentiment_importer`** (`app/controllers/oracle/reminders_sync_controller.rb`). Bearer-auth'd, accepts any POST body (any content-type — iOS Shortcuts sends iCalendar VTODO despite JSON header) and archives verbatim to **`ecosystem_change_logs/reminders_raws/<UTC-timestamp>.json`** via GitHub Contents API. Credentials (`oracle_sync_token`, `github_pat`) in `config/application.rb` (not env). The oracle GAS at `oracle.truesight.me` still reads `ecosystem_change_logs/reminders/current.json` — downstream parser from raw archive to current.json is TODO.

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
179d390 | 2026-04-19 15:27:38 -0700 | Merge pull request #59 from TrueSightDAO/chore/drop-whatsapp-retirement-header
```

### `agentic_ai_context` → `agentic_ai_context`

```
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
94d6326 | 2026-04-12 17:29:58 -0700 | feat(agroverse-qr): Consolidate batch web Apps Script into qr_code_web_service.gs (#218)
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
0f53cfc | 2026-04-13 15:28:38 -0700 | chore: refresh Agroverse store inventory snapshot
```

### `agroverse_shop` → `agroverse_shop_beta`

```
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

### `Cypher-Defense` → `Cypher-Defense`

```
921648e | 2026-04-18 12:49:41 -0700 | Merge pull request #14 from TrueSightDAO/feature/apr18-reply-location
a5134de | 2026-04-18 12:49:30 -0700 | Fill in operator location in AWS case reply draft
22176d4 | 2026-04-18 12:45:12 -0700 | Merge pull request #13 from TrueSightDAO/feature/apr18-security-followup
0fbbc08 | 2026-04-18 12:44:51 -0700 | Add Apr 18 draft reply for AWS case 177613748700177 follow-up
f87fb87 | 2026-04-18 12:38:58 -0700 | Merge pull request #12 from TrueSightDAO/feature/apr18-security-followup
bfc3933 | 2026-04-18 12:38:31 -0700 | Add Apr 18 follow-up sweep report and complete AWS security group remediation
f79ab95 | 2026-04-17 16:16:12 -0700 | Merge pull request #11 from TrueSightDAO/feature/monthly-ebs-snapshot
7c225b7 | 2026-04-17 16:15:53 -0700 | Add monthly EBS snapshot workflow for krake and seni_sql databases
3771146 | 2026-04-15 14:15:12 -0700 | Add final AWS account sweep report for 767697632458 (#10)
ebfe278 | 2026-04-14 12:12:38 -0700 | Member briefing + AWS notice PDF attachment
a2df6e4 | 2026-04-14 12:08:04 -0700 | AWS case 177613748700177: shareable account security response report
8476636 | 2026-04-14 12:02:50 -0700 | Add terminate_ec2_by_launch_keypair.py to scripts/aws
f4dc413 | 2026-04-14 11:57:02 -0700 | AWS incident hygiene: scripts, docs, and .env.example
```

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
