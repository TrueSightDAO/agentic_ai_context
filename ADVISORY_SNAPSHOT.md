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

- Generated (UTC): `2026-07-05T03:38:50Z`
- Look-back: **7** calendar days (`2026-06-28` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | $4,361 | 11% | `2026-12-31` | 179 | **behind** |
| USA Agroverse Partners | 100 | — | — | `2026-12-31` | 179 | — |

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-07-04T10:59:14.243Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **670**
- Partnered (north-star): **14**

## Funnel by status (curated order)

- Reclassified — D2C only: 1  (#1)
- AI: Contact Form found: 119  (#3)
- Research: 59  (#8)
- AI: No fit signal: 158  (#9)
- AI: Enrich — manual: 95  (#10)
- Manager Follow-up: 32  (#13)
- Followed Up: 1  (#15)
- Instagram Followed: 11  (#18)
- Rejected: 15  (#19)
- On Hold: 18  (#20)
- Deferred / Revisit later: 7  (#21)
- **Partnered: 14**  (#22)
- AI: Warm up prospect: 66  (#9999)
- Not Appropriate: 74  (#9999)
- Reclassified — D2C only: 0  (#9999)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **418**, follow_up **70**, bulk **0**, unknown **2** (data rows: **490**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **66** stores — sum logged **warmup** sends (AU): **368**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **65**; follow-up depth (none / once / ≥2): **66** / **0** / **0**
- **Manager Follow-up**: **32** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **66**; warmup depth (none / once / ≥2): **29** / **1** / **2**; follow-up depth (none / once / ≥2): **10** / **5** / **17**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: _(no rows in this status)_
- **Follow-up pipeline (combined)**: **32** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **66**; warmup depth (none / once / ≥2): **29** / **1** / **2**; follow-up depth (none / once / ≥2): **10** / **5** / **17**

---

## Attention surfaces (catalog for draw-time direction)

_Operator-curated catalog read by Sophia (truesight_autopilot) and the oracle
advisory during daily grounding readings. Machine form:
[`attention_surfaces.json`](attention_surfaces.json). Shareable PDF:
[`ATTENTION_SURFACES.pdf`](ATTENTION_SURFACES.pdf) — regenerate with
`python3 scripts/build_attention_surfaces_pdf.py` after editing this file.
Roadmap: `ATTENTION_SURFACES_PLAN.md`._

The daily oracle draw gives the **quality of the moment** (I-Ching; QMDJ adds
its strategic structure once the extension ships). This catalog gives the
**space of surfaces** — the stable map of where attention can go across the
TrueSight DAO / Agroverse ecosystem. The advisor's job at reading time is
matchmaking: **quality × staleness × mission-weight → direct attention to 1–3
surfaces.**

## Reading-time protocol (Sophia / oracle advisor)

1. **Read the draw** — hexagram(s), changing lines, advisory summary the
   practitioner recorded.
2. **Shortlist 1–3 surfaces** that resonate. The trigram affinities below are
   hints, not rules — staleness and mission-weight outrank resonance.
3. **Check each surface's named signal before recommending.** Recommend from
   evidence, not vibes. If the tracker is missing or stale, the recommendation
   is *build/refresh the tracker* — never *do more activity* on an unmeasured
   surface.
4. **Output per surface:** surface → signal checked + what it showed → ONE
   concrete next action → one-line tie-back to the mission (10,000 hectares of
   Amazon rainforest restored).

A reading is a **compass, not a dashboard review** — never more than 3 surfaces.

## The ten surfaces (soil → governance)

| # | Surface | What lives here | Observable signals | Levers | Staleness hint |
|---|---------|-----------------|--------------------|--------|----------------|
| 1 | **Origin & Restoration** | Trees, farms, Matheus/Brazil ops, ERA/BEC tree issuance — *the mission itself* | tree-planting ledger events in Telegram pulse; `treasury-cache/managed-ledgers/*.json` (BEC); `SUPPLY_CHAIN_AND_FREIGHTING.md` | plantings, farmer relations, BRL purchases | no origin/tree event in 14 days |
| 2 | **Supply Line** | AGL shipments, freight, customs, FSVP, Próspera export entity | Shipment Ledger Listing (Main Ledger); `CP…BR` Correios tracking; agroverse.shop/shipments/ pages; ops-health block in snapshot | financing syndicates, booking freight, compliance docs | shipment in transit with no status change in 14 days |
| 3 | **Inventory & Ledger Integrity** | Main Ledger, conversions/repackaging, QR serialization, double-entry health | `treasury-cache/dao_offchain_treasury.json`; `offchain transactions` tab; `Agroverse QR codes` tab | repackaging runs, reconciliation, serialization batches | snapshot age; unpaired double-entry legs |
| 4 | **Commerce (online)** | agroverse.shop, Stripe, Merchant Center, restock recommender | `agroverse-inventory/store-inventory.json`; `[SALES EVENT]` stream in pulse; Stripe sheet | SKU launches, pricing, feed fixes | days since last online sale event |
| 5 | **Retail Partner Network** | Hit List funnel, partner check-ins, velocity, restocks | Hit List statuses + pipeline-metrics block in snapshot; `Partner Check-in` tab; `partners-inventory.json` | outreach, sample drops, restock pokes | partners without a check-in in 30 days |
| 6 | **Community & Programs** | capoeira, BEC, grounding, Aora, credentialing pipeline, cohorts | `[PRACTICE EVENT]`/attestation stream in pulse; `lineage-credentials` commits; truesight.me/stats/programs_index.json | new programs, sessions, attestations | programs with zero practice events in 14 days |
| 7 | **Treasury & Governance** | TDG, managed ledgers, proposals/amendments, trading-dashboard runway | `dao_offchain_treasury.json`; goal-progress block in snapshot; proposals repo / Realms | conversions, amendments, runway moves | goals pacing behind in goal-progress block |
| 8 | **Content & Reach** | blog, YouTube, newsletter, LLM discovery surface | truesight.me/stats/*.json; `Agroverse News Letter Emails` opens; blog/repo commit activity | posts, newsletter sends, llms.txt extensions | days since last post/send |
| 9 | **Infra & Agent Health** | Edgar, GAS fleet, Sophia herself, AWS costs, credential vault | monit :2812 endpoints; CloudWatch/Cost Explorer via `aws_query`; GH Action failure emails (already polled); `OPEN_FOLLOWUPS.md` infra items | fix PRs, deploys, key rotation, cost trims | any red monit check; failure email unactioned 48h |
| 10 | **Frontier** | China/Aora launch, Kosovo GO, Krake browser, new bets — open loops not yet in any pipeline | `OPEN_FOLLOWUPS.md` (the single backlog); `*_PLAN.md` resume trackers (e.g. `AORA_EXPERIENCE_PLAN.md`) | the next irreversible step on each open loop | a tracker whose RESUME pointer hasn't moved in 14 days |

**Mission traceability:** Surface 1 *is* the mission. 2–5 fund it (cacao
revenue → restoration). 6 grows the human lineage that sustains it. 7 stewards
what's been gathered. 8 widens the circle. 9 keeps everything else standing.
10 is where the next 1–8 comes from.

## Resonance layer — trigram affinities

_A modern synthesis, not classical practice: the mapping is a prompt scaffold
for the advisor, in the same honest-disclaimer convention as
`ICHING_QMDJ_EXTENSION.md`. The affinity **suggests**; staleness and
mission-weight **decide**._

| Trigram | Quality | Natural surfaces |
|---------|---------|------------------|
| ☷ Earth | receptivity, stores | 3 Inventory & Ledger |
| ☵ Water | flow, danger, cash | 7 Treasury, 2 Supply Line |
| ☴ Wind | gradual penetration | 5 Partner Network, 8 Reach |
| ☲ Fire | visibility, clarity | 8 Content, 4 Commerce |
| ☳ Thunder | initiative, launch | 10 Frontier |
| ☶ Mountain | stillness, maintenance | 9 Infra |
| ☱ Lake | joy, exchange | 6 Community & Programs |
| ☰ Heaven | creative order | 7 Governance, 1 Mission |

When QMDJ ships (`ICHING_QMDJ_EXTENSION.md`), doors/directions gain their own
affinity column — e.g. 開門 Open Door → launches (10), 休門 Rest Door →
maintenance (9), 生門 Life Door → origin (1).

## Maintenance

- Catalog changes are **operator decisions** — edit this file + `attention_surfaces.json` together, regenerate the PDF, same PR.
- Surfaces should stay ~10 and stable; if a surface splits or merges, update Sophia's prompt examples only if the protocol itself changes.
- The advisory snapshot embeds this file automatically (6-hourly refresh); Sophia's box re-syncs it on every deploy and can always `read_repo_file` the live copy.

---

## Operations health (supply pipeline + cash float)

_Live snapshot for the oracle / advisor: per-shipper stock from the public **`treasury-cache/dao_offchain_treasury.json`**, cash float from `off chain asset balance`, and in-transit freight from **`Shipment Ledger Listing`**. Days-of-cover / burn-rate is v2 — the JSON snapshot at `ecosystem_change_logs/ops_health/current.json` has the full per-SKU detail._

### Stock at production shippers

**Kirsten Ritschel** _( San Francisco — retail / online fulfilment / partner restock )_
- Manager record: `Kirsten Ritschel` · 15 SKU lines · 1,374 total units · $1,432.80

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 10 | 432 | $781.35 |
  | Cacao Mass | Bulk | 1 | 50 | $1.55 |

**Matheus Reis** _( Ilhéus, Brazil — bulk warehouse + freight to SF )_
- Manager record: `Matheus Reis` · 22 SKU lines · 2,012.72 total units · $8,345.85

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 2 | 1,038 | $722.13 |
  | Cacao Bean | Bulk | 3 | 329.09 | $574.54 |
  | Cacao Mass | Retail Ready | 1 | 170 | $1,762.90 |
  | Cacao Tea | Bulk | 5 | 156.50 | $1,587.77 |
  | Cacao Nib | Retail Ready | 1 | 137 | $909.68 |
  | (uncategorized) | (unspecified) | 9 | 102.13 | $819.35 |
  | Cacao Nib | Bulk | 1 | 80 | $1,969.48 |

**Gary Teh** _( Operational cash + assorted retail inventory )_
- Manager record: `Gary Teh` · 26 SKU lines · 14,678.99 total units · $12,852.84

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 24 | 14,602.81 | $12,802.86 |
  | Packaging Material | Bulk | 1 | 74 | $49.98 |
  | Cacao Tea | Bulk | 1 | 2.18 | $0.00 |

### Other managers (top 8 by USD value)

| Manager | Items | Units | Value (USD) |
|---------|-------|-------|-------------|
| Sacred Earth Farms | 3 | 316 | $2,241.33 |
| Val Lapidus | 11 | 1,270 | $1,475.95 |
| Coopercabruca | 1 | 1,706 | $1,199.87 |
| Aga Marecka | 1 | 20 | $537.46 |
| Andrea Catalina Falcon Rios De Pabst | 3 | 223 | $328.62 |
| Shuar Design Boutique | 3 | 37 | $284.34 |
| Go Ask Alice - Niccolina Ammerman | 2 | 14 | $115.81 |
| Tess Walkowski | 2 | 13 | $108.75 |

_(+28 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-06-28 | deepseek | dao_members.json expanded to 406 contributors (was 18): DaoMembersCache.js now seeds byName from ALL Contributors contact information sheet entries, not just signature-holders. Enables sentinel section on truesight.me/members.html (6 sentinels: Sophia Truesight, Claude Anthropic, Kimi Moon, Deep Seek, truesight-autopilot, Open Ai).
- 2026-06-28 | deepseek | Governor Sheet-Permission Sync: Created GAS script (GovernorSheetPermissionSync.js) that syncs Main Ledger editor list to governor roster + sentinels. Rule: ADD governors/sentinels from Contact sheet not yet editors; REMOVE only editors IN Contact sheet who aren't governor/sentinel; KEEP everyone not in Contact sheet (GCP SAs, externals). Wired via doGet(?action=sync_governor_editors) + daily 04:00 UTC cron. See GOVERNOR_SHEET_PERMISSION_SYNC_PLAN.md.
- 2026-06-28 | claude | Disassociated sentiment_importer from dao_protocol in current-state docs: Edgar = standalone Python dao_protocol (own host); Perch = sentiment_importer (Rails). Fixed WORKSPACE_CONTEXT §6 prose+table (incl. dao_protocol link that pointed at dao_client repo), TRUECHAIN AI-docs table, and EDGAR(...) diagram labels in SCORING_REVIEW_QUEUE_PLAN + TRUESIGHT_GROUNDING. Historical migration plans (EDGAR_DAO_EXTRACTION_PLAN etc.) left intact as accurate record.

_All dated lines on/after 2026-06-28_ (5):

- 2026-06-28 | deepseek | Review Queue SOP + auto-review: Created REVIEW_QUEUE_SOP.md with automatable rules (Scenario A: name matching against dao_members.json then lineage-credentials; Scenario B: compute TDG from event Amount, not Grok's estimate; Scenario C: Edgar should enforce TDG server-side). Reviewed ~500 scored chatlogs — 475 approved via Deep Seek RSA key signing [CONTRIBUTION REVIEW EVENT]s to Edgar. 5 remaining edge cases (unrecognized names: X, Gergana, openai, Nora, Edgar-no-contributor).
- 2026-06-28 | deepseek | dao_members.json expanded to 406 contributors (was 18): DaoMembersCache.js now seeds byName from ALL Contributors contact information sheet entries, not just signature-holders. Enables sentinel section on truesight.me/members.html (6 sentinels: Sophia Truesight, Claude Anthropic, Kimi Moon, Deep Seek, truesight-autopilot, Open Ai).
- 2026-06-28 | deepseek | Governor Sheet-Permission Sync: Created GAS script (GovernorSheetPermissionSync.js) that syncs Main Ledger editor list to governor roster + sentinels. Rule: ADD governors/sentinels from Contact sheet not yet editors; REMOVE only editors IN Contact sheet who aren't governor/sentinel; KEEP everyone not in Contact sheet (GCP SAs, externals). Wired via doGet(?action=sync_governor_editors) + daily 04:00 UTC cron. See GOVERNOR_SHEET_PERMISSION_SYNC_PLAN.md.
- 2026-06-28 | deepseek | DApp menu: Added Review Queue to nav dropdown (menu.js) — Governor only section. Bumped cache version to v=20260628a across all 39 files.
- 2026-06-28 | claude | Disassociated sentiment_importer from dao_protocol in current-state docs: Edgar = standalone Python dao_protocol (own host); Perch = sentiment_importer (Rails). Fixed WORKSPACE_CONTEXT §6 prose+table (incl. dao_protocol link that pointed at dao_client repo), TRUECHAIN AI-docs table, and EDGAR(...) diagram labels in SCORING_REVIEW_QUEUE_PLAN + TRUESIGHT_GROUNDING. Historical migration plans (EDGAR_DAO_EXTRACTION_PLAN etc.) left intact as accurate record.

---

## Pipeline activity map (PROJECT_INDEX ↔ git)

| Pipeline | Mapped clone | Activity in window |
|----------|----------------|----------------------|
| `go_to_market` | `market_research` | **no** |
| `TrueChain` | `TrueChain` | **no** |
| `oracle` | `iching_oracle` | **no** |

---

## Git log by repo (origin default branch)

### `truesight_me` → `truesight_me_beta`

```
7a07075 | 2026-07-04 19:47:19 +0000 | chore(stats): refresh stats/current.json [skip ci]
223f17b | 2026-07-04 14:10:45 +0000 | chore(stats): refresh stats/current.json [skip ci]
1ddc9d1 | 2026-07-04 09:06:08 +0000 | chore(stats): refresh stats/current.json [skip ci]
14ec4f5 | 2026-07-04 04:22:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
b570f8d | 2026-07-03 19:59:35 +0000 | chore(stats): refresh stats/current.json [skip ci]
5f956ef | 2026-07-03 14:54:47 +0000 | chore(stats): refresh stats/current.json [skip ci]
55ac7c3 | 2026-07-03 09:43:46 +0000 | chore(stats): refresh stats/current.json [skip ci]
4e46e77 | 2026-07-03 04:28:08 +0000 | chore(stats): refresh stats/current.json [skip ci]
65bbe5d | 2026-07-02 23:09:05 -0400 | trigger redeploy [skip ci]
eaca091 | 2026-07-02 23:09:05 -0400 | Merge branch 'main' of https://github.com/TrueSightDAO/truesight_me_beta
8fd48ff | 2026-07-02 23:08:24 -0400 | Merge pull request #266 from TrueSightDAO/feat/update-voting-rights-contracts
d5a19ca | 2026-07-02 23:07:56 -0400 | docs: update voting rights contracts with corrected event names and settlement flow
592168d | 2026-07-02 23:07:34 -0400 | fix(ci): replace deprecated sync_top_nav.py check with placeholder verification (#265)
213a34e | 2026-07-02 23:06:34 -0400 | fix(ci): replace deprecated sync_top_nav.py check with placeholder verification
66d3e47 | 2026-07-02 23:03:21 -0400 | feat: shared nav + footer via JS injection with root-relative paths (#264)
bfbe0b0 | 2026-07-02 20:04:20 +0000 | chore(stats): refresh stats/current.json [skip ci]
07cc1a7 | 2026-07-02 14:54:11 +0000 | chore(stats): refresh stats/current.json [skip ci]
ae5caaf | 2026-07-02 09:45:02 +0000 | chore(stats): refresh stats/current.json [skip ci]
533f8b4 | 2026-07-02 04:43:26 +0000 | chore(stats): refresh stats/current.json [skip ci]
04a6207 | 2026-07-01 20:26:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
89672ca | 2026-07-01 15:21:44 +0000 | chore(stats): refresh stats/current.json [skip ci]
835a1b0 | 2026-07-01 10:31:13 +0000 | chore(stats): refresh stats/current.json [skip ci]
7b25ecc | 2026-07-01 01:18:40 -0400 | refactor(members): single-source from index.json, drop separate dao_members fetch (#263)
aab6284 | 2026-07-01 05:08:19 +0000 | chore(stats): refresh stats/current.json [skip ci]
a7e7857 | 2026-06-30 20:31:30 +0000 | chore(stats): refresh stats/current.json [skip ci]
7694e25 | 2026-06-30 15:14:45 +0000 | chore(stats): refresh stats/current.json [skip ci]
db5c084 | 2026-06-30 10:09:29 +0000 | chore(stats): refresh stats/current.json [skip ci]
6734b67 | 2026-06-30 04:47:43 +0000 | chore(stats): refresh stats/current.json [skip ci]
d3ff19a | 2026-06-29 20:27:49 +0000 | chore(stats): refresh stats/current.json [skip ci]
14f767f | 2026-06-29 16:25:20 +0000 | chore(stats): refresh stats/current.json [skip ci]
673bf6c | 2026-06-29 11:33:26 +0000 | chore(stats): refresh stats/current.json [skip ci]
2ef4628 | 2026-06-29 05:15:28 +0000 | chore(stats): refresh stats/current.json [skip ci]
86857c7 | 2026-06-28 15:51:17 -0700 | rename: Post-Repackaging Cleanup → Repackaging Settlement on contracts page
d68b67a | 2026-06-28 15:35:34 -0700 | PR4: Add Post-Repackaging Cleanup contract card to contracts page (#262)
2fdbfde | 2026-06-28 19:55:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
11fc1d0 | 2026-06-28 14:25:11 +0000 | chore(stats): refresh stats/current.json [skip ci]
3cf5799 | 2026-06-28 09:44:03 +0000 | chore(stats): refresh stats/current.json [skip ci]
41b618e | 2026-06-28 05:05:35 +0000 | chore(stats): refresh stats/current.json [skip ci]
```

### `market_research` → `go_to_market`

```
_(no commits on origin/main in window)_
```

### `agentic_ai_context` → `agentic_ai_context`

```
ad2d59f | 2026-07-04 15:45:31 -0400 | chore(previews): refresh Beer Hall preview (2026-07-04 UTC)
b2f69b1 | 2026-07-04 15:45:30 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-04 UTC)
03fb362 | 2026-07-04 10:09:29 -0400 | chore(previews): refresh Beer Hall preview (2026-07-04 UTC)
76fb0bd | 2026-07-04 10:09:27 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-04 UTC)
2f93a85 | 2026-07-04 05:05:22 -0400 | chore(previews): refresh Beer Hall preview (2026-07-04 UTC)
e142908 | 2026-07-04 05:05:20 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-04 UTC)
f5d5c16 | 2026-07-04 00:11:24 -0400 | chore(previews): refresh Beer Hall preview (2026-07-04 UTC)
97f52d0 | 2026-07-04 00:11:23 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-04 UTC)
83ee950 | 2026-07-03 23:22:24 -0400 | Merge pull request #642 from TrueSightDAO/auto/advisory-refresh-2026-07-04
312a596 | 2026-07-04 03:22:16 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-04 UTC)
9fdc0e7 | 2026-07-03 15:57:50 -0400 | chore(previews): refresh Beer Hall preview (2026-07-03 UTC)
924181d | 2026-07-03 15:57:49 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-03 UTC)
5c6c262 | 2026-07-03 10:41:39 -0400 | chore(previews): refresh Beer Hall preview (2026-07-03 UTC)
9c3f74b | 2026-07-03 10:41:38 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-03 UTC)
26bf54d | 2026-07-03 05:43:13 -0400 | chore(previews): refresh Beer Hall preview (2026-07-03 UTC)
65e9911 | 2026-07-03 05:43:11 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-03 UTC)
d784612 | 2026-07-03 00:26:09 -0400 | chore(previews): refresh Beer Hall preview (2026-07-03 UTC)
6faf0e9 | 2026-07-03 00:26:08 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-03 UTC)
bf39827 | 2026-07-02 23:28:48 -0400 | Merge pull request #641 from TrueSightDAO/auto/advisory-refresh-2026-07-03
0c47b47 | 2026-07-03 03:28:36 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-03 UTC)
0819ee3 | 2026-07-02 16:01:55 -0400 | chore(previews): refresh Beer Hall preview (2026-07-02 UTC)
2bf31ef | 2026-07-02 16:01:54 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-02 UTC)
8c267cb | 2026-07-02 10:38:53 -0400 | chore(previews): refresh Beer Hall preview (2026-07-02 UTC)
d092c97 | 2026-07-02 10:38:52 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-02 UTC)
6d5b970 | 2026-07-02 05:43:12 -0400 | chore(previews): refresh Beer Hall preview (2026-07-02 UTC)
cc196c0 | 2026-07-02 05:43:12 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-02 UTC)
2f1f2fe | 2026-07-02 03:58:19 -0400 | handoff: Large Spike Index parked GO-ready in thread 8297 (#640)
552350a | 2026-07-02 03:55:55 -0400 | handoff: register Large Spike Index (/large_spikes) draft (awaiting trigger+GO) (#639)
0e98016 | 2026-07-02 00:39:56 -0400 | chore(previews): refresh Beer Hall preview (2026-07-02 UTC)
50f65fc | 2026-07-02 00:39:55 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-02 UTC)
b382e21 | 2026-07-01 23:47:21 -0400 | Merge pull request #638 from TrueSightDAO/auto/advisory-refresh-2026-07-02
525cb89 | 2026-07-02 03:47:12 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-02 UTC)
66d8a6f | 2026-07-01 16:25:16 -0400 | chore(previews): refresh Beer Hall preview (2026-07-01 UTC)
21c7037 | 2026-07-01 16:25:14 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-01 UTC)
fded38f | 2026-07-01 11:19:00 -0400 | chore(previews): refresh Beer Hall preview (2026-07-01 UTC)
e4663ca | 2026-07-01 11:18:59 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-01 UTC)
db3dda5 | 2026-07-01 06:30:22 -0400 | chore(previews): refresh Beer Hall preview (2026-07-01 UTC)
0d48cd6 | 2026-07-01 06:30:21 -0400 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-01 UTC)
9500aa9 | 2026-07-01 03:10:44 -0400 | docs: SOP for seasonal governor sheet permission rotation
a1d4532 | 2026-07-01 01:06:21 -0400 | chore(previews): refresh Beer Hall preview (2026-07-01 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
761dc08 | 2026-06-29 23:17:50 -0700 | fix(gas): make extractExpenseDetails order-independent with detailed diagnostics (#377)
b95d84a | 2026-06-28 16:01:22 -0700 | Transfer script: O(n) refactoring, batch trigger, data validation fix
154fa0f | 2026-06-28 15:33:26 -0700 | GovernorSheetPermissionSync v5: only remove editors IN Contact sheet who aren't governor/sentinel
926af1d | 2026-06-28 15:31:23 -0700 | GovernorSheetPermissionSync v4: sentinels always keep editing rights
3e3cb29 | 2026-06-28 15:29:58 -0700 | GovernorSheetPermissionSync v3: eligible = non-sentinel governors with email in Contact sheet
33991a9 | 2026-06-28 15:28:55 -0700 | GovernorSheetPermissionSync v2: log-based safelist — only remove editors we added
43f63f8 | 2026-06-28 15:25:45 -0700 | Add GovernorSheetPermissionSync: auto-sync Main Ledger editors from governor roster
8be8c7c | 2026-06-28 13:14:33 -0700 | DaoMembersCache: seed byName from all Contact sheet names, not just signature-holders
256d247 | 2026-06-28 13:06:54 -0700 | feat: add update_tabulation endpoint for retroactive vote dedup (#376)
2350874 | 2026-06-28 12:43:13 -0700 | fix: dedup proposal votes by contributor identity, not just by key (#376)
```

### `dapp` → `dapp`

```
_(no commits on origin/main in window)_
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
b1b1eaa | 2026-06-30 20:31:56 -0700 | Merge proposal: 18
```

### `agroverse-inventory` → `agroverse-inventory`

```
9c625f7 | 2026-07-04 09:02:44 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
a1f26f7 | 2026-07-03 09:37:22 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
27e8083 | 2026-07-02 20:28:41 -0400 | chore: refresh Agroverse store inventory snapshot
00cb449 | 2026-07-02 09:34:45 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8c46e5f | 2026-07-02 03:59:01 -0400 | sync inventory snapshots via sync_agroverse_store_inventory.py (#16)
32f1f3a | 2026-07-02 02:28:54 -0400 | chore: refresh Agroverse store inventory snapshot
8fc82a0 | 2026-07-01 10:16:44 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
455bc76 | 2026-06-30 15:28:41 -0700 | chore: refresh Agroverse store inventory snapshot
102677d | 2026-06-30 10:03:09 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
4095414 | 2026-06-29 18:28:39 -0700 | chore: refresh Agroverse store inventory snapshot
681953f | 2026-06-29 11:35:18 +0000 | chore: refresh partners-velocity snapshot [skip ci]
6789db8 | 2026-06-29 11:25:21 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
6e1d053 | 2026-06-28 16:53:22 -0700 | inventory: expense 4 tasting bars — Oscar 81% now 10
8ac3abc | 2026-06-28 16:40:52 -0700 | inventory: settlement b08d324b — Oscar 81% bars (14) + ceremonial cacao (2)
e2a4ece | 2026-06-28 15:39:48 -0700 | feat: add processPostRepackagingCleanup GAS handler
e3a0775 | 2026-06-28 09:34:31 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
9d8f70e | 2026-07-02 23:09:05 -0400 | trigger redeploy [skip ci]
40d70fe | 2026-07-02 23:03:21 -0400 | feat: shared nav + footer via JS injection with root-relative paths (#179)
28ab8fb | 2026-07-02 03:09:05 -0400 | chore: remove .clasp.json from tracking, add to .gitignore
7074c49 | 2026-07-02 03:08:54 -0400 | fix: prevent double-encoding of Etsy OAuth scopes
e8eec32 | 2026-07-02 03:04:11 -0400 | fix: correct Etsy OAuth URLs in GAS script
624ea22 | 2026-07-02 02:53:08 -0400 | feat: add Etsy order monitoring to agroverse shop checkout
```

### `iching_oracle` → `oracle`

```
_(no commits on origin/main in window)_
```

### `Cypher-Defense` → `Cypher-Defense`

```
_(no commits on origin/master in window)_
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-07-05T033850Z_vote-dedup-fix-proposal-18-partnership-outreach.md`

- **posted_at_utc:** `2026-07-05T03:38:50Z`  
- **slug:** `vote-dedup-fix-proposal-18-partnership-outreach`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Governance (Mechanics)** — Fixed retroactive vote deduplication logic to rely on contributor identity rather than cryptographic key.

### `beer-hall_2026-07-04T032211Z_settlement-pipeline-tdg-hardening-members-fix.md`

- **posted_at_utc:** `2026-07-04T03:22:11Z`  
- **slug:** `settlement-pipeline-tdg-hardening-members-fix`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Governance (Settlement)** — Implemented full voting rights cash-out settlement pipeline across tokenomics and inventory scripts.

### `beer-hall_2026-07-03T032828Z_etsy-integration-shared-nav-large-spike-go-ready.md`

- **posted_at_utc:** `2026-07-03T03:28:28Z`  
- **slug:** `etsy-integration-shared-nav-large-spike-go-ready`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Engineering (Web/Shop)** — Consolidated navigation and footer across the main site and Agroverse Shop using shared JS injection.

---

## Recent retail field reports (DApp store status updates)

- **`20260511T210201Z.json`** — `2026-05-11T21:02:02Z`  
  **Apotheca** → `Rejected` (was `Rejected`) | type: Metaphysical/Spiritual | method: Social Media | sig: success
  _Noticing this which we visited that was not carrying ceremonial cacao or mentioned they were carrying their own earlier in the year ended up stocking Ora’s ceremonial cacao… I wonder why… I wonder if there is something wrong with_

- **`20260509T001510Z.json`** — `2026-05-09T00:15:10Z`  
  **Care Rituals, LLC** → `Deferred / Revisit later` (was `AI: Prospect replied`) | type: Metaphysical/Spiritual | sig: success

- **`20260509T001234Z.json`** — `2026-05-09T00:12:34Z`  
  **Seagrape Apothecary** → `Deferred / Revisit later` (was `AI: Prospect replied`) | type: Metaphysical/Spiritual | sig: success

- **`20260509T000800Z.json`** — `2026-05-09T00:08:00Z`  
  **Elliott's Natural Foods** → `Manager Follow-up` (was `AI: Prospect replied`) | type: Metaphysical/Spiritual | sig: success

- **`20260509T000735Z.json`** — `2026-05-09T00:07:35Z`  
  **Esalen Institute Gift Shop** → `AI: Warm up prospect` (was `AI: Prospect replied`) | type: Wellness Center | sig: success

---

## Recent agent notes (`agentic_ai_context/notes/`)

- `notes/claude_donation_mint_2026-04-30.md`
- `notes/claude_serialized_qr_sales_2026-04-29.md`
- `notes/sophia_development_workflow.md`

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
