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

- Generated (UTC): `2026-08-26T01:23:18Z`
- Look-back: **7** calendar days (`2026-08-19` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-08-25T10:59:14.292Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **768**, follow_up **71**, bulk **0**, unknown **2** (data rows: **841**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **62** stores — sum logged **warmup** sends (AU): **690**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **61**; follow-up depth (none / once / ≥2): **62** / **0** / **0**
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
| Sacred Earth Farms | 3 | 316 | $2,241.33 |
| Val Lapidus | 11 | 1,270 | $1,475.95 |
| Coopercabruca | 1 | 1,706 | $1,199.87 |
| Aga Marecka | 1 | 20 | $537.46 |
| Andrea Catalina Falcon Rios De Pabst | 3 | 223 | $328.62 |
| Shuar Design Boutique | 3 | 37 | $284.34 |
| Paloma | 3 | 201 | $152.39 |
| Go Ask Alice - Niccolina Ammerman | 2 | 14 | $115.81 |

_(+29 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-08-20 | sophia | Cacao Tea 50g Oscar Farm retail packet (FounderHaus offline QR-scan sales) shipped end-to-end: cost basis $0.683/50g (AGL8 loose-tea basis; Currencies row 131), SKU oscar-bahia-cacao-tea-50g (SKUs row 15, $10 retail), 100 QR codes 2024OSCAR_CT_20260820_1..100 (rows 1678-1777, MINTED; serial _3 found undecodable in mint QA -> VOID row 1680, replacement _101 minted row 1778, landing agroverse.shop/shipments/agl4). Assets: 100 label PNGs + 100 qrs/<id>.json manifests + qrs_index.json -> lineage-assets main (PR #5), corrected zip v2 (100 scannable labels) delivered to thread 11578 (msg 11992). Generator hardened: post-mint decodability self-check aborts batch on dead labels (lineage-assets #7). Shop (agroverse_shop_beta, beta-first): PDP no price/no buy button (offline sales only, embeds Emelin cacao-tea video R4_xqBjKzNs) + cross-list cards on retail-packs category, Oscar farm, AGL4 shipment + hero image swaps to Gary's product photos + QR-batch text correction (PRs #197-205, #208). VOID serial documented in OPEN_FOLLOWUPS (agentic_ai_context #776). STILL BLOCKED (governor-gated): promote to prod via sync_beta_to_prod(agroverse_shop_prod) - awaiting Gary's explicit approval; www.agroverse.shop not yet live.

_All dated lines on/after 2026-08-19_ (4):

- 2026-08-20 | sophia | Cacao Tea 50g Oscar Farm retail packet (FounderHaus offline QR-scan sales) shipped end-to-end: cost basis $0.683/50g (AGL8 loose-tea basis; Currencies row 131), SKU oscar-bahia-cacao-tea-50g (SKUs row 15, $10 retail), 100 QR codes 2024OSCAR_CT_20260820_1..100 (rows 1678-1777, MINTED; serial _3 found undecodable in mint QA -> VOID row 1680, replacement _101 minted row 1778, landing agroverse.shop/shipments/agl4). Assets: 100 label PNGs + 100 qrs/<id>.json manifests + qrs_index.json -> lineage-assets main (PR #5), corrected zip v2 (100 scannable labels) delivered to thread 11578 (msg 11992). Generator hardened: post-mint decodability self-check aborts batch on dead labels (lineage-assets #7). Shop (agroverse_shop_beta, beta-first): PDP no price/no buy button (offline sales only, embeds Emelin cacao-tea video R4_xqBjKzNs) + cross-list cards on retail-packs category, Oscar farm, AGL4 shipment + hero image swaps to Gary's product photos + QR-batch text correction (PRs #197-205, #208). VOID serial documented in OPEN_FOLLOWUPS (agentic_ai_context #776). STILL BLOCKED (governor-gated): promote to prod via sync_beta_to_prod(agroverse_shop_prod) - awaiting Gary's explicit approval; www.agroverse.shop not yet live.
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
1d3729b | 2026-08-24 01:00:50 +0800 | Fix Butterfly Effect logo: repoint to self-hosted asset (#306)
49b43b9 | 2026-08-24 00:54:18 +0800 | Simplify FounderHaus Farm pill to SunMint initiative (#305)
e540ef3 | 2026-08-24 00:54:15 +0800 | Retarget FounderHaus Farm primary CTA to batch verification (#304)
38f3736 | 2026-08-24 00:54:12 +0800 | Support **bold** in program-shell markdown renderer (#303)
7dbcf26 | 2026-08-24 00:43:01 +0800 | Add FounderHaus Farm Edition brief details to landing page (PDF, photo, QR, economics) (#302)
dcddbaf | 2026-08-24 00:39:15 +0800 | Brand FounderHaus Farm as SunMint initiative — FounderHaus Farm Edition (#301)
d5c150b | 2026-08-24 00:37:40 +0800 | Add FounderHaus Farm program page + programs.html card (#300)
d56bf8c | 2026-08-23 13:13:10 +0000 | chore(stats): refresh stats/current.json [skip ci]
73c591d | 2026-08-23 07:17:18 +0000 | chore(stats): refresh stats/current.json [skip ci]
97f0a01 | 2026-08-23 02:10:48 +0000 | chore(stats): refresh stats/current.json [skip ci]
686c7bd | 2026-08-22 19:00:13 +0000 | chore(stats): refresh stats/current.json [skip ci]
b803ee7 | 2026-08-22 21:20:04 +0800 | feat(qr): embed OpenStreetMap for tree QRs with real coordinates (#299)
2d87b42 | 2026-08-22 13:10:46 +0000 | chore(stats): refresh stats/current.json [skip ci]
… (truncated)
```

### `market_research` → `go_to_market`

```
b495a2a | 2026-08-25 11:02:23 -0300 | feat: scheduled daily sync of agroverse-inventory/currencies.json (#173)
```

### `agentic_ai_context` → `agentic_ai_context`

```
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
2e24fb9 | 2026-08-24 21:30:35 +0800 | chore(previews): refresh Beer Hall preview (2026-08-24 UTC)
51bac85 | 2026-08-24 21:30:33 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-24 UTC)
b353986 | 2026-08-24 19:26:07 +0800 | docs: reflect 2026-08-24 Explorya cleanup, EIP release, nginx chatbot fix (#814)
c604208 | 2026-08-24 18:18:00 +0800 | Plan: /large_spikes regime gauge Norm/Bollinger window fix + legibility (#813)
db5477f | 2026-08-24 15:37:20 +0800 | chore(previews): refresh Beer Hall preview (2026-08-24 UTC)
81f035e | 2026-08-24 15:37:19 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-24 UTC)
e7bb274 | 2026-08-24 10:07:46 +0800 | chore(previews): refresh Beer Hall preview (2026-08-24 UTC)
1aeedae | 2026-08-24 10:07:45 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-24 UTC)
ca7b1c4 | 2026-08-24 09:23:22 +0800 | Merge pull request #812 from TrueSightDAO/auto/advisory-refresh-2026-08-24
5c81c3e | 2026-08-24 01:23:10 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-24 UTC)
1257ff2 | 2026-08-24 07:20:01 +0800 | Add markdown source for sugarcane environmental report
49926b3 | 2026-08-24 07:19:54 +0800 | Add environmental deep-dive report: sugarcane and land in Brazil
f50f2a3 | 2026-08-24 04:06:34 +0800 | docs: consolidate Brazil export lane learnings + SOP reference (#810)
6fd1bb5 | 2026-08-24 03:24:42 +0800 | Add deep-dive PDF: sugarcane plantation & land impact in Brazil
ce3e3b5 | 2026-08-24 03:12:02 +0800 | Merge pull request #809 from TrueSightDAO/local-emulator-setup-doc
22fc3b2 | 2026-08-23 16:11:48 -0300 | Add LOCAL_EMULATOR_SETUP.md: how to spin up local Android emulator + iOS Simulator
35ec17d | 2026-08-24 02:57:37 +0800 | chore(previews): refresh Beer Hall preview (2026-08-23 UTC)
e48bece | 2026-08-24 02:57:36 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-23 UTC)
b38bcef | 2026-08-24 01:26:13 +0800 | docs: add TREE_PLANTING_FUNDS_TRANSFERRED state to linking plan (#808)
ca4c84f | 2026-08-24 01:26:00 +0800 | Merge pull request #807 from TrueSightDAO/deepseek-local-telegram-setup
29d7315 | 2026-08-23 14:25:40 -0300 | Add DEEPSEEK_LOCAL.md: DeepSeek Local identity + Telegram thread-confusion rules
42d82f8 | 2026-08-24 00:18:38 +0800 | Merge pull request #805 from TrueSightDAO/docs/envoy-sentinel-registered
189ae97 | 2026-08-23 23:34:43 +0800 | Tracker: PR3 + PR6-PR11 merged
f7cb66a | 2026-08-23 15:08:41 +0000 | Update ENVOY.md: Envoy TrueSight now registered as Sentinel (row 418, Is Sentinel = TRUE) — no longer "in progress"
… (truncated)
```

### `tokenomics` → `tokenomics`

```
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
d0e5f78 | 2026-08-21 18:48:11 +0800 | Fix SOLD_DATE_COL 22->26 in Parse Telegram ChatLogs.js (stamp to Column AA, not W) (#405)
81c0181 | 2026-08-21 18:48:07 +0800 | Fix SOLD_DATE_COL_DEST 27->26 in process_qr_code_updates.js (match Column AA comment) (#404)
3d45ab8 | 2026-08-21 17:26:12 +0800 | fix: admit [TREE PLANTING REJECT EVENT] rows in the scan filter (#402)
6ef80e2 | 2026-08-21 06:01:47 +0800 | Expose processTreePlantingLinkCron via doGet action for manual/cron trigger (#400)
95d9f02 | 2026-08-21 05:41:46 +0800 | Add doPost webhook to close TREE PLANTING LINK ingestion gap (#397)
3490723 | 2026-08-21 04:58:38 +0800 | feat: allow sentinels to link QR codes to trees (governor OR sentinel gate) (#399)
0bcc261 | 2026-08-21 03:41:57 +0800 | fix: move Sold Date + Tree Planted Notification to AA/AB (column collision with review workflow), add lat/long to owner email (#398)
be92958 | 2026-08-20 18:23:14 +0800 | feat(tokenomics): add TREE PLANTING REJECT path — governor marks SunMint submission INVALID (#396)
3e07028 | 2026-08-20 17:26:17 +0800 | Merge pull request #395 from TrueSightDAO/fix/sales-processing-claspignore
0276607 | 2026-08-20 09:25:44 +0000 | Add .claspignore for sales-processing GAS project
b319262 | 2026-08-20 09:05:48 +0800 | Merge pull request #394 from TrueSightDAO/fix/sunmint-claspignore-credentials-sample
517c1b4 | 2026-08-20 01:05:02 +0000 | Exclude Credentials.sample.js from SunMint's clasp push
701de08 | 2026-08-19 17:25:34 +0800 | Merge pull request #393 from TrueSightDAO/fix/sunmint-webapp-config
4102e66 | 2026-08-19 09:24:29 +0000 | Fix SunMint Tree Planting deploy: add webapp config, Credentials.sample.js, .claspignore
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
3fff0fa | 2026-08-25 14:04:18 +0000 | chore: refresh currencies.json [skip ci]
6f190de | 2026-08-25 10:24:31 -0300 | chore(inventory): refresh currencies.json (repackaging ingest)
1237c29 | 2026-08-25 08:29:14 -0300 | chore: refresh Agroverse store inventory snapshot
cec3015 | 2026-08-25 07:10:42 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
c166c94 | 2026-08-24 07:45:01 +0000 | chore: refresh partners-velocity snapshot [skip ci]
6fea31d | 2026-08-24 07:30:47 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
cb2f486 | 2026-08-23 07:03:24 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b12ca39 | 2026-08-22 07:05:06 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
d206ab7 | 2026-08-21 07:09:39 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
1fdd50d | 2026-08-20 18:28:47 +0800 | chore: refresh Agroverse store inventory snapshot
1cb9039 | 2026-08-20 07:08:40 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
66f6778 | 2026-08-19 07:07:42 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
a44b7ce | 2026-08-20 21:08:44 +0800 | fix: mobile polish for cacao tea PDP (stack detail rows, tighten 480px layout) (#219)
df6756e | 2026-08-20 20:17:11 +0800 | fix: remove QR label image + duplicate hero photo from cacao tea PDP gallery (#218)
52ecd14 | 2026-08-20 19:49:55 +0800 | fix(spec): filter benign Chromium compute-pressure + raw 403 throttle noise (#217)
beeeccf | 2026-08-20 19:48:59 +0800 | PR7: agl6 special case - retire agroverse:youtube meta-tag + bespoke lazy-load script, replace with media.json + shared loader (#215)
1598d96 | 2026-08-20 19:46:36 +0800 | PR6: migrate shipment pages agl10, agl13, agl14 to media.json (remove dead Wix video on agl10, fix agl14 heroVideo.play guard) (#214)
a645559 | 2026-08-20 19:43:17 +0800 | PR5: migrate shipment pages agl5, agl7, agl8 to media.json (distinct farmer slot for agl8) (#212)
c35c11d | 2026-08-20 19:39:25 +0800 | PR4: Migrate shipment pages agl0, agl1, agl2 to media.json (#210)
147cec6 | 2026-08-20 19:36:44 +0800 | fix(pdp): correct QR batch label (serial _3 voided, replaced by _101) (#208)
ea556e3 | 2026-08-20 19:36:39 +0800 | PR3: Migrate farm pages fazenda-sao-jorge-bahia + vivi-jesus-do-deus-itacare to media.json (#207)
9a73c14 | 2026-08-20 19:33:20 +0800 | PR2: Migrate farm pages fazenda-santa-ana-bahia + paulo-la-do-sitio-para to media.json (#206)
a510006 | 2026-08-20 19:28:49 +0800 | PR1: migrate shipments/agl4 to media.json (fixes agl14.avif bug + hero-video console error) (#200)
f6cd051 | 2026-08-20 19:21:03 +0800 | Use product photo on cacao tea cards (category/farm/shipment) (#205)
faeffaa | 2026-08-20 19:19:23 +0800 | Use v2 cacao tea photo as PDP hero (#204)
da13e0f | 2026-08-20 19:19:01 +0800 | Add cacao tea hero photo v2 (Oscar's Farm 50g)
7dfdf26 | 2026-08-20 19:18:46 +0800 | Use real cacao tea product photo as PDP hero (#203)
3d2fdec | 2026-08-20 19:18:10 +0800 | Add cacao tea product photo (Oscar's Farm 50g)
2d2be09 | 2026-08-20 19:00:23 +0800 | Fix cacao tea images: use real 50g tea label instead of ceremonial cacao photo (#202)
7dde445 | 2026-08-20 18:50:27 +0800 | Add Cacao Tea 50g card to retail-packs category page (#201)
3b86936 | 2026-08-20 18:36:32 +0800 | PR0: farm/shipment media JSON externalization pilot (oscar-bahia) + shared media-gallery.js loader (#196)
5e2b35a | 2026-08-20 18:32:43 +0800 | Cross-list Cacao Tea 50g on AGL4 shipment page (#199)
7e50e91 | 2026-08-20 18:32:39 +0800 | Cross-list Cacao Tea 50g on Oscar's Farm page (#198)
c4564ff | 2026-08-20 18:32:36 +0800 | Add Cacao Tea 50g PDP (Oscar's Farm 2024) — offline QR-scan sales only (#197)
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

### `beer-hall_2026-08-26T012318Z_sunmint-monitoring-page-deploy-sop.md`

- **posted_at_utc:** `2026-08-26T01:23:18Z`  
- **slug:** `sunmint-monitoring-page-deploy-sop`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **SunMint** — Shipped the tree-growth monitoring page featuring video capture, GPS-based tree selection, and signed PM002 measurement events.

### `beer-hall_2026-08-24T012305Z_founderhaus-launch-fund-transfer-state.md`

- **posted_at_utc:** `2026-08-24T01:23:05Z`  
- **slug:** `founderhaus-launch-fund-transfer-state`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Web** — Launched the FounderHaus Farm Edition as a SunMint initiative, adding a dedicated program page, brief details, and batch verification CTAs to the site.

### `beer-hall_2026-08-23T012558Z_qr-map-updates-email-oauth-fix.md`

- **posted_at_utc:** `2026-08-23T01:25:58Z`  
- **slug:** `qr-map-updates-email-oauth-fix`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Web** — Updated tree QR pages to display live OpenStreetMap coordinates, inline seedling photos, and signer references in the event history.

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
