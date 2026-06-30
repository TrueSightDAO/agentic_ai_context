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

- Generated (UTC): `2026-06-30T03:53:59Z`
- Look-back: **7** calendar days (`2026-06-23` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | $4,361 | 11% | `2026-12-31` | 184 | **behind** |
| USA Agroverse Partners | 100 | — | — | `2026-12-31` | 184 | — |

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-06-29T10:59:13.567Z`
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
- Rejected: 14  (#19)
- On Hold: 18  (#20)
- Deferred / Revisit later: 7  (#21)
- **Partnered: 14**  (#22)
- AI: Warm up prospect: 67  (#9999)
- Not Appropriate: 74  (#9999)
- Reclassified — D2C only: 0  (#9999)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **359**, follow_up **70**, bulk **0**, unknown **2** (data rows: **431**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **67** stores — sum logged **warmup** sends (AU): **313**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **66**; follow-up depth (none / once / ≥2): **67** / **0** / **0**
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
- Manager record: `Kirsten Ritschel` · 16 SKU lines · 1,378 total units · $1,443.91

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 10 | 435 | $790.06 |
  | Cacao Mass | Bulk | 1 | 50 | $1.55 |
  | Cacao Mass | Retail Ready | 1 | 1 | $2.40 |

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
- Manager record: `Gary Teh` · 26 SKU lines · 14,730.39 total units · $12,904.24

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 24 | 14,654.21 | $12,854.26 |
  | Packaging Material | Bulk | 1 | 74 | $49.98 |
  | Cacao Tea | Bulk | 1 | 2.18 | $0.00 |

### Other managers (top 8 by USD value)

| Manager | Items | Units | Value (USD) |
|---------|-------|-------|-------------|
| TrueSight DAO | 1 | 9,036.35 | $9,036.35 |
| Sacred Earth Farms | 3 | 316 | $2,241.33 |
| Val Lapidus | 11 | 1,270 | $1,475.95 |
| Coopercabruca | 1 | 1,706 | $1,199.87 |
| Aga Marecka | 1 | 20 | $537.46 |
| Andrea Catalina Falcon Rios De Pabst | 3 | 223 | $328.62 |
| Shuar Design Boutique | 3 | 37 | $284.34 |
| Go Ask Alice - Niccolina Ammerman | 2 | 14 | $115.81 |

_(+27 more in JSON snapshot.)_

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

_All dated lines on/after 2026-06-23_ (5):

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
e7bbf6a | 2026-06-27 19:54:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
010c83d | 2026-06-27 14:15:07 +0000 | chore(stats): refresh stats/current.json [skip ci]
6bca5c2 | 2026-06-27 09:13:44 +0000 | chore(stats): refresh stats/current.json [skip ci]
3a79893 | 2026-06-27 04:37:17 +0000 | chore(stats): refresh stats/current.json [skip ci]
1aae8a9 | 2026-06-26 20:20:15 +0000 | chore(stats): refresh stats/current.json [skip ci]
ca2c7a4 | 2026-06-26 15:13:42 +0000 | chore(stats): refresh stats/current.json [skip ci]
e8ba753 | 2026-06-26 09:59:21 +0000 | chore(stats): refresh stats/current.json [skip ci]
59c0d80 | 2026-06-26 04:52:24 +0000 | chore(stats): refresh stats/current.json [skip ci]
6892e18 | 2026-06-25 20:32:55 +0000 | chore(stats): refresh stats/current.json [skip ci]
5b2ed63 | 2026-06-25 15:26:17 +0000 | chore(stats): refresh stats/current.json [skip ci]
0db2744 | 2026-06-25 09:54:47 +0000 | chore(stats): refresh stats/current.json [skip ci]
9e694aa | 2026-06-25 04:47:53 +0000 | chore(stats): refresh stats/current.json [skip ci]
bad4b7e | 2026-06-24 20:20:30 +0000 | chore(stats): refresh stats/current.json [skip ci]
ba83e60 | 2026-06-24 15:20:02 +0000 | chore(stats): refresh stats/current.json [skip ci]
9c89006 | 2026-06-24 09:59:17 +0000 | chore(stats): refresh stats/current.json [skip ci]
40870f7 | 2026-06-24 04:48:29 +0000 | chore(stats): refresh stats/current.json [skip ci]
f2c6719 | 2026-06-23 20:35:59 +0000 | chore(stats): refresh stats/current.json [skip ci]
50c54cb | 2026-06-23 15:36:39 +0000 | chore(stats): refresh stats/current.json [skip ci]
6e49f35 | 2026-06-23 10:21:21 +0000 | chore(stats): refresh stats/current.json [skip ci]
a21ddf7 | 2026-06-23 04:43:44 +0000 | chore(stats): refresh stats/current.json [skip ci]
```

### `market_research` → `go_to_market`

```
_(no commits on origin/main in window)_
```

### `agentic_ai_context` → `agentic_ai_context`

```
66ea32e | 2026-06-29 21:35:11 -0400 | fix(sop): correct expense reporting SOP to use GAS-compatible field names
96b0ad4 | 2026-06-29 21:27:35 -0400 | feat: add SOPHIA_EXPENSE_REPORTING_PLAN.md — SOP for shipping expense reporting
cab11b6 | 2026-06-29 21:07:57 -0400 | fix(context): remove stale Edgar/Rails references from canonical context files
a53f829 | 2026-06-29 13:24:33 -0700 | chore(previews): refresh Beer Hall preview (2026-06-29 UTC)
18efd8d | 2026-06-29 13:24:32 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-29 UTC)
20b114d | 2026-06-29 09:23:54 -0700 | chore(previews): refresh Beer Hall preview (2026-06-29 UTC)
7dcf8ea | 2026-06-29 09:23:53 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-29 UTC)
23597d5 | 2026-06-29 04:32:06 -0700 | chore(previews): refresh Beer Hall preview (2026-06-29 UTC)
50ee546 | 2026-06-29 04:32:05 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-29 UTC)
19354dd | 2026-06-28 22:12:27 -0700 | chore(previews): refresh Beer Hall preview (2026-06-29 UTC)
e4ffa4f | 2026-06-28 22:12:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-29 UTC)
d741fd3 | 2026-06-28 21:08:22 -0700 | Merge pull request #635 from TrueSightDAO/auto/advisory-refresh-2026-06-29
1c2d6fc | 2026-06-29 04:08:11 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-29 UTC)
fea6d9d | 2026-06-28 16:53:40 -0700 | docs: repackaging settlement SOP + v3 plan (#634)
fd841ff | 2026-06-28 16:49:23 -0700 | docs: repackaging settlement SOP — full reference for AIs and Sophia
b784c55 | 2026-06-28 16:49:06 -0700 | chore(roadmap): round-cap resilience COMPLETE — #275 merged + deployed (#633)
4fee8cc | 2026-06-28 16:26:55 -0700 | chore(roadmap): round-cap resilience resume tracker — PR1 merged, #275 open (#632)
d6c4dcf | 2026-06-28 16:18:04 -0700 | docs: disassociate sentiment_importer from dao_protocol (now separate standalone codebases) (#631)
0ece68c | 2026-06-28 15:59:21 -0700 | Round-cap resilience: roadmap + §5d Pre-flight Completeness gate (#630)
4325d1f | 2026-06-28 15:51:25 -0700 | rename: POST-REPACKAGING CLEANUP → REPACKAGING SETTLEMENT throughout plan
d1a1f59 | 2026-06-28 15:35:03 -0700 | Update context: review queue complete, governor sync deployed, SOP created
6dfd039 | 2026-06-28 15:28:58 -0700 | Governor sheet sync plan v2: log-based safelist, SA pattern detection
6eed131 | 2026-06-28 15:25:51 -0700 | Add Governor Sheet-Permission Sync implementation plan
0766a4c | 2026-06-28 15:20:37 -0700 | plan(post-repackaging-cleanup): v3 — add full surface checklist
e019a10 | 2026-06-28 15:16:00 -0700 | plan(post-repackaging-cleanup): v2 — switch to Edgar event → dispatch → GAS pattern
71f528b | 2026-06-28 15:11:28 -0700 | docs: post-repackaging cleanup plan + Sophia handoff (#629)
ea9fdba | 2026-06-28 15:04:04 -0700 | registry: record sophia handoff thread_id 7987 for post-repackaging cleanup
a27bc48 | 2026-06-28 15:03:23 -0700 | handoff(sophia): post-repackaging cleanup plan — auto-populate Currencies + offchain location after repackaging GAS
5d59c40 | 2026-06-28 13:32:59 -0700 | SOP: switch primary name match to dao_members.json, lineage-credentials as fallback
73f9fef | 2026-06-28 13:01:03 -0700 | Proposal CLI plan: clean resume pointer + tracker (parseable by auto-advance) (#628)
40f2699 | 2026-06-28 12:54:27 -0700 | chore(previews): refresh Beer Hall preview (2026-06-28 UTC)
63d93ed | 2026-06-28 12:54:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-28 UTC)
67b0a57 | 2026-06-28 07:23:21 -0700 | chore(previews): refresh Beer Hall preview (2026-06-28 UTC)
b4e439d | 2026-06-28 07:23:19 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-28 UTC)
246dfeb | 2026-06-28 02:41:34 -0700 | chore(previews): refresh Beer Hall preview (2026-06-28 UTC)
f3f8846 | 2026-06-28 02:41:33 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-28 UTC)
834e4d5 | 2026-06-27 22:00:21 -0700 | chore(previews): refresh Beer Hall preview (2026-06-28 UTC)
e14b3e4 | 2026-06-27 22:00:20 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-28 UTC)
7573b9f | 2026-06-27 21:03:30 -0700 | Merge pull request #627 from TrueSightDAO/auto/advisory-refresh-2026-06-28
c479e43 | 2026-06-28 04:03:19 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-28 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
b95d84a | 2026-06-28 16:01:22 -0700 | Transfer script: O(n) refactoring, batch trigger, data validation fix
154fa0f | 2026-06-28 15:33:26 -0700 | GovernorSheetPermissionSync v5: only remove editors IN Contact sheet who aren't governor/sentinel
926af1d | 2026-06-28 15:31:23 -0700 | GovernorSheetPermissionSync v4: sentinels always keep editing rights
3e3cb29 | 2026-06-28 15:29:58 -0700 | GovernorSheetPermissionSync v3: eligible = non-sentinel governors with email in Contact sheet
33991a9 | 2026-06-28 15:28:55 -0700 | GovernorSheetPermissionSync v2: log-based safelist — only remove editors we added
43f63f8 | 2026-06-28 15:25:45 -0700 | Add GovernorSheetPermissionSync: auto-sync Main Ledger editors from governor roster
8be8c7c | 2026-06-28 13:14:33 -0700 | DaoMembersCache: seed byName from all Contact sheet names, not just signature-holders
256d247 | 2026-06-28 13:06:54 -0700 | feat: add update_tabulation endpoint for retroactive vote dedup (#376)
2350874 | 2026-06-28 12:43:13 -0700 | fix: dedup proposal votes by contributor identity, not just by key (#376)
f3fdfa4 | 2026-06-23 10:15:21 -0700 | feat: add processCurrencyDefinitionsFromTelegramChatLogs GAS handler (1N6o00) (#376)
ce68b47 | 2026-06-22 18:22:49 -0700 | fix(qr-gen): repoint batch-zip upload off archived qr_codes -> lineage-assets (#375)
029dc6c | 2026-06-22 18:10:03 -0700 | Review approve: write reviewer-selected contributor back to Col A (#374)
4ffe230 | 2026-06-22 18:06:10 -0700 | fix(qr-gen): repoint serialized-QR PNG storage from archived qr_codes -> lineage-assets (#373)
578df97 | 2026-06-22 17:57:43 -0700 | Review write-back: match Scored Chatlogs row by (hash + contributor), not hash alone (#372)
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
_(no commits on origin/main in window)_
```

### `agroverse-inventory` → `agroverse-inventory`

```
4095414 | 2026-06-29 18:28:39 -0700 | chore: refresh Agroverse store inventory snapshot
681953f | 2026-06-29 11:35:18 +0000 | chore: refresh partners-velocity snapshot [skip ci]
6789db8 | 2026-06-29 11:25:21 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
6e1d053 | 2026-06-28 16:53:22 -0700 | inventory: expense 4 tasting bars — Oscar 81% now 10
8ac3abc | 2026-06-28 16:40:52 -0700 | inventory: settlement b08d324b — Oscar 81% bars (14) + ceremonial cacao (2)
e2a4ece | 2026-06-28 15:39:48 -0700 | feat: add processPostRepackagingCleanup GAS handler
e3a0775 | 2026-06-28 09:34:31 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
ddfd787 | 2026-06-27 04:28:35 -0700 | chore: refresh Agroverse store inventory snapshot
5b24715 | 2026-06-27 09:06:58 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
48f8cd7 | 2026-06-26 09:53:33 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
fbe83bb | 2026-06-25 23:28:44 -0700 | chore: refresh Agroverse store inventory snapshot
ee79c37 | 2026-06-25 09:46:53 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
5fe3701 | 2026-06-24 09:52:31 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
1ddcb08 | 2026-06-23 10:05:12 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
_(no commits on origin/main in window)_
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

### `beer-hall_2026-06-30T035358Z_sophia-expense-reporting-plan-live.md`

- **posted_at_utc:** `2026-06-30T03:53:58Z`  
- **slug:** `sophia-expense-reporting-plan-live`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Ops (Tools)** — Sophia Expense Reporting Plan published; SOP updated for GAS-compatible field names.

### `beer-hall_2026-06-29T040807Z_repackaging-settlement-governor-sync.md`

- **posted_at_utc:** `2026-06-29T04:08:07Z`  
- **slug:** `repackaging-settlement-governor-sync`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Ops (Inventory)** — Repackaging settlement executed: 14 Oscar 81% bars and 2 ceremonial cacao units settled; inventory updated.

### `beer-hall_2026-06-28T040310Z_edgar-registration-oscar-sales-qr-flag.md`

- **posted_at_utc:** `2026-06-28T04:03:10Z`  
- **slug:** `edgar-registration-oscar-sales-qr-flag`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Ops (Governance)** — New program registration request submitted by Edgar (XysraBvHfNTSvAraec).

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
