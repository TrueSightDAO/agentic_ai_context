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

- Generated (UTC): `2026-08-29T06:06:14Z`
- Look-back: **7** calendar days (`2026-08-22` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-08-28T10:59:14.938Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **802**, follow_up **71**, bulk **0**, unknown **2** (data rows: **875**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **62** stores — sum logged **warmup** sends (AU): **725**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **61**; follow-up depth (none / once / ≥2): **62** / **0** / **0**
- **Manager Follow-up**: **33** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **67**; warmup depth (none / once / ≥2): **30** / **1** / **2**; follow-up depth (none / once / ≥2): **11** / **5** / **17**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: **2** stores — sum logged **warmup** sends (AU): **17**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **0** / **0** / **2**; follow-up depth (none / once / ≥2): **2** / **0** / **0**
- **Follow-up pipeline (combined)**: **35** stores — sum logged **warmup** sends (AU): **24**, sum logged **follow-up** sends (AV): **67**; warmup depth (none / once / ≥2): **30** / **1** / **4**; follow-up depth (none / once / ≥2): **13** / **5** / **17**

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
- Manager record: `Kirsten Ritschel` · 16 SKU lines · 1,339 total units · $1,492.60

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 11 | 397 | $841.15 |
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
- Manager record: `Gary Teh` · 28 SKU lines · 13,939.66 total units · $12,349.27

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 26 | 13,863.48 | $12,299.29 |
  | Packaging Material | Bulk | 1 | 74 | $49.98 |
  | Cacao Tea | Bulk | 1 | 2.18 | $0.00 |

### Other managers (top 8 by USD value)

| Manager | Items | Units | Value (USD) |
|---------|-------|-------|-------------|
| Sophia Truesight | 2 | 200 | $10,005.81 |
| Sacred Earth Farms | 3 | 316 | $2,241.33 |
| Val Lapidus | 11 | 1,270 | $1,475.95 |
| Coopercabruca | 1 | 1,706 | $1,199.87 |
| Aga Marecka | 1 | 20 | $537.46 |
| Andrea Catalina Falcon Rios De Pabst | 3 | 223 | $328.62 |
| Shuar Design Boutique | 3 | 37 | $284.34 |
| Paloma | 6 | 441.32 | $204.33 |

_(+30 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_No lines matched name/keyword heuristics in this window._

_All dated lines on/after 2026-08-22_ (3):

- 2026-08-23 | claude (envoy) | Named the interactive Claude Code seat on nelanco-claude "Envoy" — see ENVOY.md for the full reasoning.
- 2026-08-23 | deepseek | DeepSeek Local identity + Telegram setup: added DEEPSEEK_LOCAL.md (identity + thread-confusion rules when speaking with Sophia across Telegram topics). Credentials + long-poll listener at ~/Applications/deepseek_telegram_monitor/ (bot @deepseek_tdg_local_bot, ID 8835920598); boot convention in ~/.claude/CLAUDE.md ("DeepSeek local agent").
- 2026-08-23 | deepseek | Added LOCAL_EMULATOR_SETUP.md — how to spin up the local Android emulator (JDK 21 + android-commandlinetools, x86_64 system image, AVD sunmint_test) and iOS Simulator (Xcode 16.2, iPhone 16 Pro) on this Mac for mobile testing. Captures env vars, one-time install, build+install+launch, and gotchas (platform-tools under ANDROID_HOME; Capacitor 8 Node>=22; iOS plugin-Swift incompat blocker). Also registered in OPERATING_INSTRUCTIONS §2.

---

## Pipeline activity map (PROJECT_INDEX ↔ git)

| Pipeline | Mapped clone | Activity in window |
|----------|----------------|----------------------|
| `go_to_market` | `market_research` | **yes** |
| `TrueChain` | `TrueChain` | **no** |
| `oracle` | `iching_oracle` | **no** |

---

## Git log by repo (origin default branch)

### `truesight_me` → `truesight_me_beta`

```
1f19de7 | 2026-08-28 20:05:41 -0300 | Fix mobile overflow on FounderHaus program page QR row (#317)
280d39e | 2026-08-28 22:34:30 +0000 | chore(stats): refresh stats/current.json [skip ci]
bdd9618 | 2026-08-28 09:51:41 -0300 | Link FounderHaus Farm program page to the Cacao Tea 50g product page (#316)
ded4170 | 2026-08-28 12:05:38 +0000 | chore(stats): refresh stats/current.json [skip ci]
615e43d | 2026-08-28 08:30:24 -0300 | Embed FounderHaus Farm videos on program page (#315)
77b62cd | 2026-08-28 08:26:14 -0300 | Add planting-day photo gallery to FounderHaus Farm program page (#314)
ac537e6 | 2026-08-27 22:31:37 +0000 | chore(stats): refresh stats/current.json [skip ci]
7b1b1aa | 2026-08-27 10:26:03 +0000 | chore(stats): refresh stats/current.json [skip ci]
e150301 | 2026-08-26 21:02:11 +0000 | chore(stats): refresh stats/current.json [skip ci]
5ba59fa | 2026-08-26 13:36:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
e6eccf7 | 2026-08-26 07:42:24 -0300 | revert: remove mis-scoped sunmint monitor page from truesight_me_beta (#313)
f635116 | 2026-08-26 07:28:03 +0000 | chore(stats): refresh stats/current.json [skip ci]
d80fab7 | 2026-08-26 02:10:44 +0000 | chore(stats): refresh stats/current.json [skip ci]
40edcf8 | 2026-08-25 22:15:49 -0300 | SunMint monitor spec v1.4 (photo-first + event taxonomy)
9638710 | 2026-08-25 17:53:40 -0300 | feat: add sunmint monitor-tree-growth page (video capture + nearest-tree dropdown + signed PM002 measurement event) (#312)
5ed6c85 | 2026-08-25 19:09:55 +0000 | chore(stats): refresh stats/current.json [skip ci]
360e8a1 | 2026-08-25 14:35:23 -0300 | SunMint Tree-Growth Monitoring spec v1.3 (GeoJSON tree index, no database)
84d3042 | 2026-08-25 14:13:08 -0300 | SunMint Tree-Growth Monitoring spec v1.2 (nearby-tree GPS selection)
202478b | 2026-08-25 14:11:52 -0300 | SunMint Tree-Growth Monitoring spec v1.1 (dual deploy: dapp + sunmint app)
f9a75fe | 2026-08-25 14:10:04 -0300 | SunMint Tree-Growth Monitoring spec v1 (video + Python worker)
def2927 | 2026-08-25 13:13:29 -0300 | SunMint consolidated progress report v8
bbd6276 | 2026-08-25 13:12:19 -0300 | SunMint PDD §12: cacao-sales flywheel funds the carbon-certification pipeline (#311)
ca6593e | 2026-08-25 13:07:02 -0300 | SunMint PDD: Plan Vivo-first decision, free satellite APIs, PM002 equations, grants, milestones, First Tree proof (#310)
65d9c78 | 2026-08-25 13:06:03 -0300 | SunMint consolidated progress report v7
d7e58fe | 2026-08-25 12:55:34 -0300 | SunMint consolidated progress report v6 (PDF) — existing grants map per resource gap
d4eecce | 2026-08-25 12:52:32 -0300 | SunMint consolidated progress report v5 (PDF) — free satellite APIs section added
e2a75fa | 2026-08-25 12:51:22 -0300 | SunMint consolidated progress report v4 (PDF) — PM002 methodology + lean stack + resource gaps
4255d36 | 2026-08-25 12:44:32 -0300 | SunMint PDD: add Community-First MRV section (§7) — decentralized sensing network (#308)
cd37f7a | 2026-08-25 12:43:32 -0300 | SunMint consolidated progress report v3 (PDF) — with execution gap analysis
17ce453 | 2026-08-25 12:42:55 -0300 | SunMint consolidated progress report v2 (Markdown)
aa34c5b | 2026-08-25 12:42:50 -0300 | SunMint consolidated progress report v2 (PDF)
6c981bf | 2026-08-25 12:35:46 -0300 | SunMint whitepaper: Plan Vivo pilot route + phone-camera MRV precedent (#307)
bbccb60 | 2026-08-25 13:30:08 +0000 | chore(stats): refresh stats/current.json [skip ci]
5d95633 | 2026-08-25 07:26:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
c69f62e | 2026-08-25 02:04:54 +0000 | chore(stats): refresh stats/current.json [skip ci]
87553fc | 2026-08-24 19:11:29 +0000 | chore(stats): refresh stats/current.json [skip ci]
7df964c | 2026-08-24 13:32:23 +0000 | chore(stats): refresh stats/current.json [skip ci]
894fff8 | 2026-08-24 07:40:19 +0000 | chore(stats): refresh stats/current.json [skip ci]
60dc1ba | 2026-08-24 02:08:42 +0000 | chore(stats): refresh stats/current.json [skip ci]
9af86cd | 2026-08-23 18:59:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
… (truncated)
```

### `market_research` → `go_to_market`

```
b495a2a | 2026-08-25 11:02:23 -0300 | feat: scheduled daily sync of agroverse-inventory/currencies.json (#173)
```

### `agentic_ai_context` → `agentic_ai_context`

```
f0f7fa5 | 2026-08-28 19:32:05 -0300 | chore(previews): refresh Beer Hall preview (2026-08-28 UTC)
5267d73 | 2026-08-28 19:32:03 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-28 UTC)
8f8891c | 2026-08-28 13:27:25 -0300 | Add BitAngels Demo Day contribution record PDF (2026-08-28)
c92531f | 2026-08-28 08:38:35 -0300 | chore(previews): refresh Beer Hall preview (2026-08-28 UTC)
18e92e6 | 2026-08-28 08:38:34 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-28 UTC)
edb102a | 2026-08-27 19:29:23 -0300 | chore(previews): refresh Beer Hall preview (2026-08-27 UTC)
61f4708 | 2026-08-27 19:29:22 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-27 UTC)
3b46255 | 2026-08-27 07:07:53 -0300 | chore(previews): refresh Beer Hall preview (2026-08-27 UTC)
349b14a | 2026-08-27 07:07:51 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-27 UTC)
b4e9cc6 | 2026-08-27 05:05:12 -0300 | Merge pull request #826 from TrueSightDAO/auto/advisory-refresh-2026-08-27
dacff59 | 2026-08-27 08:04:59 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-27 UTC)
4dc512b | 2026-08-26 21:27:10 -0300 | Update SUNMINT_TREE_GROWTH_MONITORING_PLAN to reflect corrected hosting + completed units (#825)
fca6f65 | 2026-08-26 17:34:08 -0300 | chore(previews): refresh Beer Hall preview (2026-08-26 UTC)
369d64f | 2026-08-26 17:34:07 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-26 UTC)
52a0fca | 2026-08-26 10:33:51 -0300 | chore(previews): refresh Beer Hall preview (2026-08-26 UTC)
bf1ed87 | 2026-08-26 10:33:50 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-26 UTC)
9e5788b | 2026-08-26 09:18:23 -0300 | Add Perch recurring-themes report methodology runbook (#824)
6f3c874 | 2026-08-26 04:26:09 -0300 | chore(previews): refresh Beer Hall preview (2026-08-26 UTC)
2e3248c | 2026-08-26 04:26:08 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-26 UTC)
3f5558e | 2026-08-25 23:29:54 -0300 | Add SUNMINT_MONITOR_TREE_GROWTH_PLAN.md (canonical plan, event taxonomy) (#821)
213e9cc | 2026-08-25 23:09:02 -0300 | chore(previews): refresh Beer Hall preview (2026-08-26 UTC)
f7f80f9 | 2026-08-25 23:09:01 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-26 UTC)
a377ff7 | 2026-08-25 22:23:35 -0300 | Merge pull request #823 from TrueSightDAO/auto/advisory-refresh-2026-08-26
250010b | 2026-08-26 01:23:23 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-26 UTC)
17a791b | 2026-08-25 22:19:20 -0300 | Add SUNMINT_TREE_GROWTH_MONITORING_PLAN.md — complete plan capturing 2026-08-26 decisions (#822)
6094272 | 2026-08-25 16:09:00 -0300 | chore(previews): refresh Beer Hall preview (2026-08-25 UTC)
f0ea85f | 2026-08-25 16:08:59 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-25 UTC)
b3da125 | 2026-08-25 13:09:56 -0300 | docs: mark DEPLOY_PUSH_SOP Phase 2 as shipped (#820)
4642646 | 2026-08-25 12:17:07 -0300 | docs(followups): file deploy-ledger Phase 2 + OPERATING_INSTRUCTIONS pointer items (#819)
9cec10a | 2026-08-25 12:17:03 -0300 | docs(sops): add DEPLOY_PUSH_SOP — cross-agent push/deploy audit procedure (#818)
286f882 | 2026-08-25 10:28:31 -0300 | chore(previews): refresh Beer Hall preview (2026-08-25 UTC)
b65ad28 | 2026-08-25 10:28:29 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-25 UTC)
b69a37d | 2026-08-25 07:54:54 -0300 | docs: plan of record — currency_conversion.html stale currencies.json (#816)
30d6672 | 2026-08-25 04:25:08 -0300 | chore(previews): refresh Beer Hall preview (2026-08-25 UTC)
02de9a1 | 2026-08-25 04:25:07 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-25 UTC)
d8c45b2 | 2026-08-24 23:00:27 -0300 | chore(previews): refresh Beer Hall preview (2026-08-25 UTC)
fd25e75 | 2026-08-24 23:00:25 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-25 UTC)
7e9a000 | 2026-08-24 16:11:44 -0300 | chore(previews): refresh Beer Hall preview (2026-08-24 UTC)
3c2f05d | 2026-08-24 16:11:42 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-24 UTC)
6062b28 | 2026-08-24 15:42:26 -0300 | Docs: Sophia contribution estimates = raw execution + direct time (two separate CONTRIBUTION EVENTS) (#815)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
8e11f91 | 2026-08-27 10:00:12 -0300 | fix(deploy): repoint pinned GAS deployments on push; commit asset_receipt_ingest project (#433)
f51731c | 2026-08-27 09:59:26 -0300 | Server-side enforcement: proximity gate (200m, operators exempt), INVALID tree block, REJECT allows NEW+LINKED (#432)
521d02b | 2026-08-27 09:18:51 -0300 | fix(asset-receipt-ingest): match 'Contributor(s)' label in paired-contribution unit cost lookup (#431)
0d57fba | 2026-08-25 23:30:02 -0300 | Add process_tree_growth_monitoring.gs — [TREE GROWTH MONITORING EVENT] handler (P1d) (#430)
0d55b11 | 2026-08-25 23:29:37 -0300 | fix(asset-receipt-ingest): anchor event detection + idempotent SKIPPED/ERROR dedup (#427)
54bf0cf | 2026-08-25 13:09:09 -0300 | feat: enforce DEPLOY_PUSH_SOP lease+audit in deploy_gas_project.py (direct-run gap) (#429)
d120f70 | 2026-08-25 01:25:03 +0800 | fix: remove stale Code.js duplicate from inventory movement GAS project (#425)
8d69388 | 2026-08-24 22:37:21 +0800 | Add admin+sophia@truesight.me to TRUSTED_AGENTS for inventory movement auth (#424)
e8b166f | 2026-08-24 01:17:26 +0800 | docs: SCHEMA.md — add TREE_PLANTING_FUNDS_TRANSFERRED to status enum + States tab (#422)
79671e8 | 2026-08-24 01:11:11 +0800 | feat: add TREE_PLANTING_FUNDS_TRANSFERRED QR state (enum, pickers, list endpoint, link validation, shop counter) (#421)
7b7fbf4 | 2026-08-23 20:23:06 +0800 | Harden LINK flow: surface tree-planted email failures in tracking outcome (#420)
b885678 | 2026-08-23 07:32:24 +0800 | fix: declare oauthScopes (incl. script.send_mail) in 1UrBg appsscript.json manifest (#419)
985d437 | 2026-08-23 02:48:51 +0800 | Add public authorizeMailApp() to trigger MailApp OAuth consent (#418)
a857fb3 | 2026-08-23 02:10:30 +0800 | Add idempotent hourly trigger self-installer for processBatch (#417)
fd47587 | 2026-08-23 02:10:27 +0800 | resendTreePlantedNotification_: call MailApp.sendEmail directly (no swallowing wrapper) + report quota (#416)
e62a8ff | 2026-08-23 01:37:50 +0800 | Merge pull request #413 from TrueSightDAO/fix/resend-tree-planted-notification
b8dee3b | 2026-08-22 17:34:30 +0000 | fix: add safe standalone re-send for the tree-planted notification email
73c1f8c | 2026-08-23 00:41:36 +0800 | Merge pull request #411 from TrueSightDAO/fix/asset-receipt-quantity-unit-cost
acbcdb0 | 2026-08-22 16:38:58 +0000 | Fix asset receipt ingest: Amount maps to Quantity; unit cost from paired USD contribution
8dadb3c | 2026-08-23 00:26:52 +0800 | Fix processBatch onboarding-email tracking link (query-append + clickable anchor) (#410)
d183155 | 2026-08-22 17:44:46 +0800 | fix: generalize AGL4 main-ledger routing to an allow-list (adds sunmint/main) (#409)
d7a7a79 | 2026-08-22 17:38:53 +0800 | Merge pull request #407 from TrueSightDAO/fix/sales-parser-zero-price
d8cd51c | 2026-08-22 17:12:51 +0800 | Merge pull request #408 from TrueSightDAO/docs/invalidated-status-enum
a5139f6 | 2026-08-22 09:11:57 +0000 | docs: add INVALIDATED to Agroverse QR codes status enum
b306e6c | 2026-08-22 07:00:06 +0000 | fix: sales parser accepts $0 sale price (was rejected as falsy)
62b57d3 | 2026-08-22 14:45:45 +0800 | fix: route AGL4 tree-planting fulfillment to main DAO ledger offchain tab (#406)
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
232d254 | 2026-08-28 19:00:06 +0000 | chore: refresh currencies.json [skip ci]
e7ee650 | 2026-08-28 18:46:14 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8e195dd | 2026-08-27 17:53:42 +0000 | chore: refresh currencies.json [skip ci]
2df3c0b | 2026-08-27 17:40:51 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
edf8fdb | 2026-08-26 07:31:12 +0000 | chore: refresh currencies.json [skip ci]
28f4a7e | 2026-08-26 07:11:14 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
3fff0fa | 2026-08-25 14:04:18 +0000 | chore: refresh currencies.json [skip ci]
6f190de | 2026-08-25 10:24:31 -0300 | chore(inventory): refresh currencies.json (repackaging ingest)
1237c29 | 2026-08-25 08:29:14 -0300 | chore: refresh Agroverse store inventory snapshot
cec3015 | 2026-08-25 07:10:42 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
c166c94 | 2026-08-24 07:45:01 +0000 | chore: refresh partners-velocity snapshot [skip ci]
6fea31d | 2026-08-24 07:30:47 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
cb2f486 | 2026-08-23 07:03:24 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b12ca39 | 2026-08-22 07:05:06 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
c229526 | 2026-08-28 08:28:55 -0300 | Embed FounderHaus Tools of Common video on cacao tea PDP (#224)
4225601 | 2026-08-28 08:24:31 -0300 | Migrate cacao tea PDP gallery to media-gallery.js framework (media.json) (#223)
18afb3f | 2026-08-28 08:22:19 -0300 | Add FounderHaus Farm Edition special-edition callout to cacao tea PDP (#221)
fe173c1 | 2026-08-28 07:42:18 -0300 | Replace cacao tea 50g hero image with new farm photo (#220)
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

### `beer-hall_2026-08-29T060614Z_founderhaus-content-launch-bitangels-event.md`

- **posted_at_utc:** `2026-08-29T06:06:14Z`  
- **slug:** `founderhaus-content-launch-bitangels-event`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **FounderHaus** — Launched the Farm Edition program page with embedded videos, a planting-day photo gallery, and direct links to the Cacao Tea shop.

### `beer-hall_2026-08-27T080454Z_sunmint-monitor-plan-backend-sync.md`

- **posted_at_utc:** `2026-08-27T08:04:54Z`  
- **slug:** `sunmint-monitor-plan-backend-sync`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **SunMint** — Updated the Tree-Growth Monitoring Plan (v1.4) to reflect corrected hosting priorities and shipped the backend handler for signed PM002 measurement events.

### `beer-hall_2026-08-26T012318Z_sunmint-monitoring-page-deploy-sop.md`

- **posted_at_utc:** `2026-08-26T01:23:18Z`  
- **slug:** `sunmint-monitoring-page-deploy-sop`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **SunMint** — Shipped the tree-growth monitoring page featuring video capture, GPS-based tree selection, and signed PM002 measurement events.

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

- `notes/NOTES_dapp.md`
- `notes/NOTES_krake_browser.md`
- `notes/NOTES_sentiment_importer.md`
- `notes/NOTES_tokenomics.md`
- `notes/NOTES_truesight_me.md`
- `notes/claude_donation_mint_2026-04-30.md`
- `notes/claude_serialized_qr_sales_2026-04-29.md`
- `notes/sophia_development_workflow.md`

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
