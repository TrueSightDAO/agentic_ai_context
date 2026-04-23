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

- Generated (UTC): `2026-04-23T19:50:34Z`
- Look-back: **7** calendar days (`2026-04-16` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | — | — | `2026-12-31` | 252 | — |
| USA Agroverse Partners | 100 | — | — | `2026-12-31` | 252 | — |

_Notes: (live fetch skipped: missing `google_credentials.json`)_

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-04-23T10:59:15.591Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **521**
- Partnered (north-star): **13**
- Meeting Scheduled: **1**
- Shortlisted: **4**

## Funnel by status (curated order)

- AI: Enrich — manual: 68  (#3)
- AI: Contact Form found: 77  (#4)
- AI: Photo rejected: 107  (#7)
- AI: Photo needs review: 41  (#8)
- AI: Warm up prospect: 66  (#9)
- Not Appropriate: 71  (#11)
- Contacted: 4  (#12)
- Shortlisted: 4  (#13)
- Manager Follow-up: 26  (#14)
- Meeting Scheduled: 1  (#16)
- Instagram Followed: 11  (#17)
- On Hold: 17  (#18)
- **Partnered: 13**  (#19)
- Rejected: 14  (#20)
- Followed Up: 1  (#21)

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-04-19 | claude | **iOS Reminders → oracle pipeline:** New Rails endpoint **`POST https://edgar.truesight.me/oracle/reminders_sync`** in **`sentiment_importer`** (`app/controllers/oracle/reminders_sync_controller.rb`). Bearer-auth'd, accepts any POST body (any content-type — iOS Shortcuts sends iCalendar VTODO despite JSON header) and archives verbatim to **`ecosystem_change_logs/reminders_raws/<UTC-timestamp>.json`** via GitHub Contents API. Credentials (`oracle_sync_token`, `github_pat`) in `config/application.rb` (not env). The oracle GAS at `oracle.truesight.me` still reads `ecosystem_change_logs/reminders/current.json` — downstream parser from raw archive to current.json is TODO.

_All dated lines on/after 2026-04-16_ (4):

- 2026-04-16 | cursor | **Tokenomics GAS headers:** Every **`tokenomics/google_app_scripts/**/*.gs`** now documents **`Apps Script editor:`** `https://script.google.com/home/projects/<scriptId>/edit` (or N/A for deprecated stubs) per **`clasp_mirrors/PROJECT_INDEX.md`**. **`NOTES_tokenomics.md`** — index link + SeaCoast ingest row (`1gi4YKh2…`). SeaCoast **`Code.gs`** header order normalized.
- 2026-04-19 | claude | **Beer Hall + advisory snapshot automation:** WhatsApp posting via OpenClaw **retired**; digest is now archive-only. Added **`market_research/.github/workflows/advisory-snapshot-refresh.yml`** (every 6 h) and **`beer-hall-digest-daily.yml`** (00:00 UTC daily, auto-merges PRs). New **`market_research/scripts/draft_beer_hall_digest.py`** calls Claude Sonnet 4.6 via the anthropic SDK to draft Message 1 + Message 2 from the preview + latest 2 archives as few-shot examples. New repo secret: **`ORACLE_ADVISORY_PUSH_TOKEN`** (fine-grained PAT, Contents+PR Read/Write on `ecosystem_change_logs` and `agentic_ai_context`). `ANTHROPIC_API_KEY` also added. **`WORKSPACE_CONTEXT.md` §3d** rewritten; **`OPENCLAW_WHATSAPP.md`** Beer Hall section marked legacy.
- 2026-04-19 | claude | **iOS Reminders → oracle pipeline:** New Rails endpoint **`POST https://edgar.truesight.me/oracle/reminders_sync`** in **`sentiment_importer`** (`app/controllers/oracle/reminders_sync_controller.rb`). Bearer-auth'd, accepts any POST body (any content-type — iOS Shortcuts sends iCalendar VTODO despite JSON header) and archives verbatim to **`ecosystem_change_logs/reminders_raws/<UTC-timestamp>.json`** via GitHub Contents API. Credentials (`oracle_sync_token`, `github_pat`) in `config/application.rb` (not env). The oracle GAS at `oracle.truesight.me` still reads `ecosystem_change_logs/reminders/current.json` — downstream parser from raw archive to current.json is TODO.
- 2026-04-21 | cursor | **DAO client AI contributions:** **`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`** — convention for AI **`[CONTRIBUTION EVENT]`** via **`dao_client`** (TrueSightDAO PR URLs + explicit body). **`dao_client`:** **`modules/report_ai_agent_contribution.py`**. README + **`PROJECT_INDEX.md`** (dao_client row) + **`WORKSPACE_CONTEXT.md`** pointers.

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
d8db274 | 2026-04-21 15:47:21 -0700 | Merge pull request #45 from TrueSightDAO/docs/blog-oracle-feedback-loop
d066d57 | 2026-04-21 15:46:39 -0700 | blog: oracle feedback loop — offline activity to daily advisory
986bcbc | 2026-04-21 13:55:51 -0700 | docs(blog): retarget signature-onboarding demo links to TrueSightDAO/dao_client (#44)
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
```

### `market_research` → `go_to_market`

```
c28d5ef | 2026-04-21 13:45:46 -0700 | Merge pull request #63 from TrueSightDAO/feat/advisory-metrics-from-eco
```

### `agentic_ai_context` → `agentic_ai_context`

```
f2919bc | 2026-04-23 07:19:49 -0700 | chore(previews): refresh Beer Hall preview (2026-04-23 UTC)
5dbde21 | 2026-04-23 07:19:48 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
a43e204 | 2026-04-23 01:19:38 -0700 | chore(previews): refresh Beer Hall preview (2026-04-23 UTC)
85d091e | 2026-04-23 01:19:37 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
5c301b9 | 2026-04-22 20:54:28 -0700 | chore(previews): refresh Beer Hall preview (2026-04-23 UTC)
4acfa00 | 2026-04-22 20:54:27 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
65e7610 | 2026-04-22 19:25:03 -0700 | Merge pull request #42 from TrueSightDAO/auto/advisory-refresh-2026-04-23
c572e23 | 2026-04-23 02:24:54 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
7be31ee | 2026-04-22 12:47:15 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
6b06117 | 2026-04-22 12:47:14 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
48ece2f | 2026-04-22 07:16:26 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
685f1a4 | 2026-04-22 07:16:24 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
0fcc9c1 | 2026-04-22 01:15:27 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
2480a43 | 2026-04-22 01:15:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
7523efd | 2026-04-22 00:46:44 -0700 | docs: correct TrueChain status — designed, NOT running (v0.3) (#41)
cc8d63a | 2026-04-22 00:41:17 -0700 | docs(blockchain-anchoring): v0.2 — TrueChain's value is conditional, not assumed (#40)
7313b77 | 2026-04-22 00:22:34 -0700 | docs(blockchain-anchoring): add two mermaid diagrams for non-technical readers (#39)
cff1715 | 2026-04-22 00:12:54 -0700 | docs: internal proposal for blockchain-anchoring DAO caches + Telegram logs (#38)
a9f220c | 2026-04-21 20:47:34 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
76536c7 | 2026-04-21 20:47:33 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
03d730f | 2026-04-21 19:13:21 -0700 | Merge pull request #37 from TrueSightDAO/auto/advisory-refresh-2026-04-22
8c141a6 | 2026-04-22 02:13:11 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
79ed534 | 2026-04-21 16:09:07 -0700 | docs: AI agent [CONTRIBUTION EVENT] convention (dao_client + context) (#36)
c492992 | 2026-04-21 14:39:30 -0700 | docs: dao_client — mark auth flow validated, document modules/ (#35)
dc30dee | 2026-04-21 14:24:40 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
971b86a | 2026-04-21 14:24:39 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
11d92a4 | 2026-04-21 14:09:00 -0700 | docs: index TrueSightDAO/dao_client (Python Edgar CLI + loopback auth) (#34)
d87deac | 2026-04-21 13:45:50 -0700 | chore: drop CONSTRAINTS.md + METRICS_WEEKLY.md stubs (#33)
980e24b | 2026-04-21 12:45:29 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
e80aed1 | 2026-04-21 12:45:28 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
6546ad7 | 2026-04-21 12:33:29 -0700 | docs: add Retailer Onboarding Playbook v0.1 (#32)
ecb0668 | 2026-04-21 07:15:43 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
0370c50 | 2026-04-21 07:15:42 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
1a02479 | 2026-04-21 01:17:12 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
d155f33 | 2026-04-21 01:17:11 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
97aee49 | 2026-04-20 23:09:31 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
dabdd20 | 2026-04-20 23:09:30 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
26d8542 | 2026-04-20 20:51:14 -0700 | chore(previews): refresh Beer Hall preview (2026-04-21 UTC)
c9cff6a | 2026-04-20 20:51:13 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-21 UTC)
82488a0 | 2026-04-20 19:14:55 -0700 | Merge pull request #31 from TrueSightDAO/auto/advisory-refresh-2026-04-21
… (truncated)
```

### `tokenomics` → `tokenomics`

```
7ae14f8 | 2026-04-22 19:33:51 -0700 | Merge pull request #239 from TrueSightDAO/qr-code-sales-webhook-script-lock
1d6b110 | 2026-04-22 19:33:32 -0700 | Serialize QR Code Sales webhooks with LockService script locks
874827a | 2026-04-22 19:14:57 -0700 | Merge pull request #238 from TrueSightDAO/inventory-webhook-script-lock
6caa170 | 2026-04-22 19:14:40 -0700 | Serialize inventory webhook GETs with LockService script lock
e6abd2d | 2026-04-21 23:42:19 -0700 | feat(dao_members_cache): emit dao_totals at snapshot root (schema_version 2) (#237)
1de4b60 | 2026-04-21 23:25:53 -0700 | feat(tdg_identity_management): dao_members.json cache publisher + doGet action (#236)
1b28994 | 2026-04-21 15:46:30 -0700 | Merge pull request #235 from TrueSightDAO/feature/gas-inventory-expense-authorization
fef3c29 | 2026-04-21 15:46:08 -0700 | feat(gas): unauthorized movement + scored expense Processing Status
539bf43 | 2026-04-21 15:25:03 -0700 | Merge pull request #234 from TrueSightDAO/docs/schema-telegram-chat-logs-governor-s
1b30c34 | 2026-04-21 15:24:40 -0700 | docs(schema): Telegram Chat Logs column S Governor + Edgar semantics
1d65efb | 2026-04-21 14:45:48 -0700 | feat(gas): notify treasury-cache-publisher on 5 additional write-paths (#233)
af8fc00 | 2026-04-21 14:10:38 -0700 | Merge pull request #232 from TrueSightDAO/feat/pipeline-metrics-highlights
f240a25 | 2026-04-21 14:10:03 -0700 | feat(metrics): highlight Meeting Scheduled + Shortlisted in summary
be3e43a | 2026-04-21 13:50:12 -0700 | chore: relocate signature onboarding demo to TrueSightDAO/dao_client (#231)
9b7aea5 | 2026-04-21 13:45:43 -0700 | Merge pull request #229 from TrueSightDAO/feat/pipeline-metrics-snapshot
3683188 | 2026-04-21 13:37:16 -0700 | feat(tdg-inventory): notify treasury-cache-publisher after inventory movements (#230)
9491b1d | 2026-04-21 13:36:39 -0700 | feat(metrics): reuse ORACLE_ADVISORY_PUSH_TOKEN; add clasp mirror
8b9d2d7 | 2026-04-21 12:56:50 -0700 | feat(metrics): GAS to mirror Pipeline Dashboard → ecosystem_change_logs
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
44c4008 | 2026-04-22 20:07:15 -0700 | Merge pull request #173 from TrueSightDAO/fix/store-history-popout-links
9fa52d4 | 2026-04-22 20:06:47 -0700 | Open Store Interaction History in a new tab from nav and links
854324e | 2026-04-22 20:04:08 -0700 | Merge pull request #172 from TrueSightDAO/fix/stores-gas-cache-footer-links
9453d6b | 2026-04-22 20:03:46 -0700 | Stores: fresh GAS fetches, SW v4, interaction history footer links
752b74e | 2026-04-21 23:50:50 -0700 | perf(dapp): shared DaoMembersCache + cache-first signature check on create_signature (#171)
039d937 | 2026-04-21 23:37:39 -0700 | perf(tdg_balance): cache-first fetch against dao_members.json, GAS fallback (#170)
77bf22c | 2026-04-21 15:55:22 -0700 | Merge pull request #169 from TrueSightDAO/fix/stores-nearby-history-link-new-tab
00900b5 | 2026-04-21 15:55:04 -0700 | fix(dapp): open interaction history link in new tab after store update.
2bdae6d | 2026-04-21 15:46:38 -0700 | Store interaction history: simplify help text; no image uploads planned.
ec236f6 | 2026-04-21 15:44:33 -0700 | Stores Nearby: after status update, link to interaction history for calmer review; clarify photo/Edgar scope in history page help.
6e114f3 | 2026-04-21 15:34:52 -0700 | Store interaction history: document update API scope (no photo upload; not Edgar).
3f67262 | 2026-04-21 15:34:36 -0700 | Stores Nearby: link map and details to interaction history; skip full list refresh after update.
fa2d43b | 2026-04-21 14:58:32 -0700 | feat(dapp): extend treasury-cache reads to report_dao_expenses + shipping_planner (#168)
238c3cf | 2026-04-21 14:49:18 -0700 | test(routes): playwright smoke suite for routes.js direct + proxy modes (#167)
56606dd | 2026-04-21 14:20:01 -0700 | feat(report-inventory-movement): read managers + items from treasury-cache JSON (#166)
c8be32f | 2026-04-21 13:24:39 -0700 | feat(routes): probe-and-flip fallback to Edgar proxy for GFW-blocked users (#165)
9208e61 | 2026-04-21 12:52:09 -0700 | feat(routes): migrate remaining pages + tdg_balance.js to Routes (#164)
64dd953 | 2026-04-21 12:44:40 -0700 | feat(routes): migrate Sunmint module to Routes (#163)
6b337ee | 2026-04-21 12:43:10 -0700 | feat(routes): migrate Inventory & Sales module to Routes (#162)
c539745 | 2026-04-21 12:32:47 -0700 | feat(routes): migrate Identity & Governance module to Routes (#161)
d6ca6a5 | 2026-04-21 12:26:18 -0700 | feat(routes): migrate report_contribution.html to Routes (Contributions module) (#160)
1439821 | 2026-04-21 12:24:58 -0700 | feat(routes): centralize endpoints in routes.js + migrate submit_feedback POC (#159)
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
87ffff1 | 2026-04-23 08:13:33 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
0a3a25f | 2026-04-22 19:28:51 -0700 | chore: refresh Agroverse store inventory snapshot
c318a22 | 2026-04-22 16:28:35 -0700 | chore: refresh Agroverse store inventory snapshot
a24746d | 2026-04-22 14:28:40 -0700 | chore: refresh Agroverse store inventory snapshot
08584bc | 2026-04-22 08:08:49 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
9224db7 | 2026-04-21 14:52:31 -0700 | feat(repackaging-ingest): notify treasury-cache-publisher on successful currency commits (#4)
5909bc7 | 2026-04-21 12:28:38 -0700 | chore: refresh Agroverse store inventory snapshot
0da1893 | 2026-04-20 08:30:22 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
ac9568e | 2026-04-19 21:32:47 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
89d4c64 | 2026-04-19 14:03:03 -0700 | feat(gas): add editor-runnable wrappers for repackaging-currency-ingest (#3)
0f5ccf7 | 2026-04-19 13:37:30 -0700 | chore(inventory): repackaging composition 67c88267-b41c-4eab-8ef5-d5be48854d65
9353975 | 2026-04-19 13:37:29 -0700 | chore(inventory): refresh currencies.json (repackaging ingest)
1f830fc | 2026-04-18 21:40:40 -0700 | Merge pull request #2 from TrueSightDAO/feat/repackaging-currency-ingest-gas
d6f5f90 | 2026-04-18 21:40:31 -0700 | feat(gas): add repackaging-currency-ingest Apps Script + doGet processor
c30b32f | 2026-04-17 11:28:50 -0700 | chore: refresh Agroverse store inventory snapshot
```

### `agroverse_shop` → `agroverse_shop_beta`

```
c5d8696 | 2026-04-20 11:28:06 -0700 | Merge pull request #75 from TrueSightDAO/feature/rename-start-script
0ce62b7 | 2026-04-20 11:27:55 -0700 | Rename start-local-server.sh to start_local.sh (standardize across repos)
6090cab | 2026-04-19 15:57:44 -0700 | chore(agl6): live YouTube embed for São Jorge hot chocolate (gw2vIxPCcyQ)
567db30 | 2026-04-19 15:41:11 -0700 | publish sao jorge fazenda (#73)
fe81a3b | 2026-04-16 13:08:13 -0700 | feat(taste-profile): add AGL2 chart and document implementation framework (#72)
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
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-04-23T022449Z_dao-client-read-layer-members-cache-store-restocks.md`

- **posted_at_utc:** `2026-04-23T02:24:49Z`  
- **slug:** `dao-client-read-layer-members-cache-store-restocks`  
- **Message 1 excerpt (first two non-empty lines):**

  Big week for the read side of the stack: the dao_client got a full cache layer so Python scripts and the browser DApp can pull DAO data from GitHub without hitting GAS every time; a DAO members cache went live so signature checks are fast; and Lumin Earth Apothecary restocked with five Oscar 2024 kraft pouches via on-chain inventory movements.
  - dao_client cache layer shipped: GitHub Raw and GitHub Contents backends mean Python consumers now read treasury data from cached snapshots rather than live GAS calls on every request.

### `beer-hall_2026-04-22T021304Z_dao-client-treasury-cache-retailer-playbook-live.md`

- **posted_at_utc:** `2026-04-22T02:13:04Z`  
- **slug:** `dao-client-treasury-cache-retailer-playbook-live`  
- **Message 1 excerpt (first two non-empty lines):**

  Heavy infrastructure week: the DApp got a treasury-cache speed layer, a China GFW workaround, and a full routes centralisation; the dao_client Python CLI shipped with 15 signed-event wrappers; and the Retailer Onboarding Playbook v0.1 landed from 332 real Hit List rows.
  - Treasury-cache framework live: DApp pages now pull a pre-computed JSON snapshot of all off-chain inventory (items, managers, unit cost, weight) from GitHub instead of making slow per-page GAS calls on load.

### `beer-hall_2026-04-21T061005Z_whitepaper-oracle-claude-email-marketing-live.md`

- **posted_at_utc:** `2026-04-21T06:10:05Z`  
- **slug:** `whitepaper-oracle-claude-email-marketing-live`  
- **Message 1 excerpt (first two non-empty lines):**

  Busy week across the stack — whitepaper accuracy, Oracle upgrades, email marketing scaffolding, São Jorge farm page, and ongoing AWS security follow-through.
  - Whitepapers updated to be agentic-AI-friendly: Gas Fee section dropped, Edgar/TrueChain/Oracle terms defined, TrueTech Inc correctly distinguished from Brazilian suppliers, Beer Hall described as archive-only, and 31 broken partnership-agreement links fixed with direct Google Doc URLs.

---

## Recent agent notes (`agentic_ai_context/notes/`)

_No `.md` / `.txt` under `notes/` modified in this window._

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
