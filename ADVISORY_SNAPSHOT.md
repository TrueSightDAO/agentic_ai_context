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

- Generated (UTC): `2026-08-22T01:19:25Z`
- Look-back: **7** calendar days (`2026-08-15` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-08-21T10:59:14.626Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **753**, follow_up **71**, bulk **0**, unknown **2** (data rows: **826**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **62** stores — sum logged **warmup** sends (AU): **675**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **61**; follow-up depth (none / once / ≥2): **62** / **0** / **0**
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
- Manager record: `Kirsten Ritschel` · 15 SKU lines · 1,339 total units · $1,536.14

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 10 | 397 | $884.69 |
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
- Manager record: `Gary Teh` · 27 SKU lines · 13,929.66 total units · $12,336.57

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 25 | 13,853.48 | $12,286.59 |
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

_(+26 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-08-18 | claude | Sunmint tree-planting -> QR linking (plans/SUNMINT_TREE_QR_LINKING_PLAN.md) shipped PR2-PR8: Agroverse QR codes gained columns W (Sold Date) and X (Tree Planted Notification Sent Date); SunMint Tree Planting gained columns R/S (Linked QR Code/Linked At); new GAS handler process_tree_planting_link.gs (tokenomics, same project as process_qr_code_updates.js) processes governor-only [TREE PLANTING LINK EVENT], the first handler in this codebase with real server-side governor enforcement (existing gates elsewhere are client-side only); new DApp page dapp_beta/link_tree_planting.html + treasury-cache permissions.json action tree_planting.link; dao_client and dao_protocol confirmed to be the same git repository (one local checkout is a legacy-named second clone), not separate forks. RESUME HERE is now the clasp deploy + GOVERNOR_READ_KEY provisioning step, then RUN/UAT (both always-stop gates, not yet done).
- 2026-08-20 | sophia | Cacao Tea 50g Oscar Farm retail packet (FounderHaus offline QR-scan sales) shipped end-to-end: cost basis $0.683/50g (AGL8 loose-tea basis; Currencies row 131), SKU oscar-bahia-cacao-tea-50g (SKUs row 15, $10 retail), 100 QR codes 2024OSCAR_CT_20260820_1..100 (rows 1678-1777, MINTED; serial _3 found undecodable in mint QA -> VOID row 1680, replacement _101 minted row 1778, landing agroverse.shop/shipments/agl4). Assets: 100 label PNGs + 100 qrs/<id>.json manifests + qrs_index.json -> lineage-assets main (PR #5), corrected zip v2 (100 scannable labels) delivered to thread 11578 (msg 11992). Generator hardened: post-mint decodability self-check aborts batch on dead labels (lineage-assets #7). Shop (agroverse_shop_beta, beta-first): PDP no price/no buy button (offline sales only, embeds Emelin cacao-tea video R4_xqBjKzNs) + cross-list cards on retail-packs category, Oscar farm, AGL4 shipment + hero image swaps to Gary's product photos + QR-batch text correction (PRs #197-205, #208). VOID serial documented in OPEN_FOLLOWUPS (agentic_ai_context #776). STILL BLOCKED (governor-gated): promote to prod via sync_beta_to_prod(agroverse_shop_prod) - awaiting Gary's explicit approval; www.agroverse.shop not yet live.

_All dated lines on/after 2026-08-15_ (2):

- 2026-08-18 | claude | Sunmint tree-planting -> QR linking (plans/SUNMINT_TREE_QR_LINKING_PLAN.md) shipped PR2-PR8: Agroverse QR codes gained columns W (Sold Date) and X (Tree Planted Notification Sent Date); SunMint Tree Planting gained columns R/S (Linked QR Code/Linked At); new GAS handler process_tree_planting_link.gs (tokenomics, same project as process_qr_code_updates.js) processes governor-only [TREE PLANTING LINK EVENT], the first handler in this codebase with real server-side governor enforcement (existing gates elsewhere are client-side only); new DApp page dapp_beta/link_tree_planting.html + treasury-cache permissions.json action tree_planting.link; dao_client and dao_protocol confirmed to be the same git repository (one local checkout is a legacy-named second clone), not separate forks. RESUME HERE is now the clasp deploy + GOVERNOR_READ_KEY provisioning step, then RUN/UAT (both always-stop gates, not yet done).
- 2026-08-20 | sophia | Cacao Tea 50g Oscar Farm retail packet (FounderHaus offline QR-scan sales) shipped end-to-end: cost basis $0.683/50g (AGL8 loose-tea basis; Currencies row 131), SKU oscar-bahia-cacao-tea-50g (SKUs row 15, $10 retail), 100 QR codes 2024OSCAR_CT_20260820_1..100 (rows 1678-1777, MINTED; serial _3 found undecodable in mint QA -> VOID row 1680, replacement _101 minted row 1778, landing agroverse.shop/shipments/agl4). Assets: 100 label PNGs + 100 qrs/<id>.json manifests + qrs_index.json -> lineage-assets main (PR #5), corrected zip v2 (100 scannable labels) delivered to thread 11578 (msg 11992). Generator hardened: post-mint decodability self-check aborts batch on dead labels (lineage-assets #7). Shop (agroverse_shop_beta, beta-first): PDP no price/no buy button (offline sales only, embeds Emelin cacao-tea video R4_xqBjKzNs) + cross-list cards on retail-packs category, Oscar farm, AGL4 shipment + hero image swaps to Gary's product photos + QR-batch text correction (PRs #197-205, #208). VOID serial documented in OPEN_FOLLOWUPS (agentic_ai_context #776). STILL BLOCKED (governor-gated): promote to prod via sync_beta_to_prod(agroverse_shop_prod) - awaiting Gary's explicit approval; www.agroverse.shop not yet live.

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
fdfe771 | 2026-08-21 19:07:44 +0000 | chore(stats): refresh stats/current.json [skip ci]
952544a | 2026-08-21 13:28:07 +0000 | chore(stats): refresh stats/current.json [skip ci]
22a18af | 2026-08-21 07:25:38 +0000 | chore(stats): refresh stats/current.json [skip ci]
1dfa2b6 | 2026-08-21 02:09:43 +0000 | chore(stats): refresh stats/current.json [skip ci]
d721f0d | 2026-08-20 19:11:55 +0000 | chore(stats): refresh stats/current.json [skip ci]
152633b | 2026-08-21 02:05:44 +0800 | SunMint PDD: update methodology to Verra VM0047 (ARR) + Andean Cacao precedent (#294)
f5a3624 | 2026-08-20 13:28:34 +0000 | chore(stats): refresh stats/current.json [skip ci]
710a8d7 | 2026-08-20 07:24:09 +0000 | chore(stats): refresh stats/current.json [skip ci]
229e051 | 2026-08-20 02:03:27 +0000 | chore(stats): refresh stats/current.json [skip ci]
82ffc2b | 2026-08-19 19:04:04 +0000 | chore(stats): refresh stats/current.json [skip ci]
bf4507c | 2026-08-19 13:26:36 +0000 | chore(stats): refresh stats/current.json [skip ci]
92fb673 | 2026-08-19 07:22:27 +0000 | chore(stats): refresh stats/current.json [skip ci]
186f92b | 2026-08-19 02:04:07 +0000 | chore(stats): refresh stats/current.json [skip ci]
214293a | 2026-08-19 03:58:23 +0800 | feat: add IVY (Liv for Yoga) program page (#293)
1fa6f07 | 2026-08-18 19:08:12 +0000 | chore(stats): refresh stats/current.json [skip ci]
31dfabc | 2026-08-18 13:24:53 +0000 | chore(stats): refresh stats/current.json [skip ci]
08c1a5a | 2026-08-18 07:20:59 +0000 | chore(stats): refresh stats/current.json [skip ci]
31daf4d | 2026-08-18 02:01:24 +0000 | chore(stats): refresh stats/current.json [skip ci]
edc8f26 | 2026-08-17 19:08:42 +0000 | chore(stats): refresh stats/current.json [skip ci]
4293736 | 2026-08-17 13:22:45 +0000 | chore(stats): refresh stats/current.json [skip ci]
72d70d8 | 2026-08-17 07:35:02 +0000 | chore(stats): refresh stats/current.json [skip ci]
c909c9e | 2026-08-17 02:05:51 +0000 | chore(stats): refresh stats/current.json [skip ci]
96a5919 | 2026-08-16 18:58:05 +0000 | chore(stats): refresh stats/current.json [skip ci]
0de21d3 | 2026-08-16 13:11:02 +0000 | chore(stats): refresh stats/current.json [skip ci]
e56ceeb | 2026-08-16 07:10:10 +0000 | chore(stats): refresh stats/current.json [skip ci]
f2b5dde | 2026-08-16 02:07:43 +0000 | chore(stats): refresh stats/current.json [skip ci]
62bd300 | 2026-08-15 18:58:03 +0000 | chore(stats): refresh stats/current.json [skip ci]
d6421f7 | 2026-08-15 13:09:44 +0000 | chore(stats): refresh stats/current.json [skip ci]
bda77b3 | 2026-08-15 07:07:53 +0000 | chore(stats): refresh stats/current.json [skip ci]
fd8c1b4 | 2026-08-15 01:59:52 +0000 | chore(stats): refresh stats/current.json [skip ci]
```

### `market_research` → `go_to_market`

```
0655d78 | 2026-08-18 17:34:59 +0800 | Fix photo orientations (EXIF transpose + portrait-aware layouts) in Evan Bahia deck
```

### `agentic_ai_context` → `agentic_ai_context`

```
e41ceb1 | 2026-08-22 03:07:05 +0800 | chore(previews): refresh Beer Hall preview (2026-08-21 UTC)
4f55d2c | 2026-08-22 03:07:04 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-21 UTC)
69614a3 | 2026-08-21 21:26:57 +0800 | chore(previews): refresh Beer Hall preview (2026-08-21 UTC)
0d2ecbb | 2026-08-21 21:26:55 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-21 UTC)
6990c17 | 2026-08-21 20:09:15 +0800 | Merge pull request #784 from TrueSightDAO/worktree-sunmint-prod-incident-and-pr-closure
0f1ca35 | 2026-08-21 11:16:31 +0000 | Mark PR-FIX1/PR-FIX2 merged+deployed+verified; document prod Credentials.js incident; close #403/dao_protocol#145
31c1f8c | 2026-08-21 19:02:35 +0800 | Document nelanco-claude's Telegram bot + direct Sophia channel (#783)
429f499 | 2026-08-21 18:37:23 +0800 | Merge pull request #782 from TrueSightDAO/worktree-sunmint-architecture-note
a0dc3f1 | 2026-08-21 10:36:49 +0000 | Merge: resolve conflict, keep both §8 audit findings and §9 architecture pattern
5f6b79b | 2026-08-21 10:34:15 +0000 | Document required request pattern (Sheet write + doGet trigger); flag #403's doPost may be solving a non-problem
0285b05 | 2026-08-21 18:10:10 +0800 | Merge pull request #781 from TrueSightDAO/worktree-sunmint-audit-findings
ae029a2 | 2026-08-21 10:09:36 +0000 | Audit Sophia's post-deploy work: 2 live data-corruption bugs found, must fix before RUN
5cd5c80 | 2026-08-21 15:24:16 +0800 | chore(previews): refresh Beer Hall preview (2026-08-21 UTC)
81cfba1 | 2026-08-21 15:24:14 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-21 UTC)
5c50772 | 2026-08-21 10:08:19 +0800 | chore(previews): refresh Beer Hall preview (2026-08-21 UTC)
a332fc1 | 2026-08-21 10:08:17 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-21 UTC)
77314ed | 2026-08-21 04:40:57 +0800 | docs(credentialing): add end-to-end cohort validation runbook (IVY E2E) (#780)
71e0025 | 2026-08-21 03:10:58 +0800 | chore(previews): refresh Beer Hall preview (2026-08-20 UTC)
60dc3d3 | 2026-08-21 03:10:57 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-20 UTC)
fc84a07 | 2026-08-21 02:05:48 +0800 | SunMint snapshot: note VM0047 supersedes VM0017 methodology reference (#779)
a92cbe7 | 2026-08-20 21:27:32 +0800 | chore(previews): refresh Beer Hall preview (2026-08-20 UTC)
c1f7f39 | 2026-08-20 21:27:30 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-20 UTC)
e9a185f | 2026-08-20 19:39:34 +0800 | docs: log cacao tea 50g Oscar Farm QR batch delivery to CONTEXT_UPDATES (#777)
7edfcc7 | 2026-08-20 19:37:26 +0800 | docs: note cacao tea 50g QR serial _3 VOID (replaced by _101) (#776)
8291504 | 2026-08-20 19:24:37 +0800 | docs: IVY plan — infra fully live, UAT narrowed to human-only steps (#761)
4a0d8f3 | 2026-08-20 19:22:39 +0800 | fix(ivy-plan): refresh §4 tracker — all units merged + E2E verified, PR3 gated on Gary (#774)
6a3ecb7 | 2026-08-20 18:58:29 +0800 | docs(handoffs): add SUNMINT_TREE_QR_LINKING row for thread 11596 (Sophia-owned) (#772)
6e9e985 | 2026-08-20 17:50:25 +0800 | future-proof credentialing onboarding: internal lineage-credentials manifest step + backlog entry (#770)
7ae5ef9 | 2026-08-20 17:28:50 +0800 | Merge pull request #769 from TrueSightDAO/worktree-sunmint-deploy-complete
4dc3950 | 2026-08-20 09:28:12 +0000 | Mark all 4 GAS deploy targets complete; RESUME HERE -> RUN
40abbf8 | 2026-08-20 09:07:41 +0000 | Record Sophia's Telegram topic for Farm/Shipment Media JSON handoff
aceaaaa | 2026-08-20 09:05:44 +0000 | Add Farm & Shipment Media JSON plan — hand off to Sophia
7e9d78a | 2026-08-20 16:47:19 +0800 | docs: SOP — verify root cause before assuming an async flow is just slow (#768)
852cbd3 | 2026-08-20 15:23:11 +0800 | chore(previews): refresh Beer Hall preview (2026-08-20 UTC)
c499091 | 2026-08-20 15:23:10 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-20 UTC)
379b864 | 2026-08-20 09:59:06 +0800 | chore(previews): refresh Beer Hall preview (2026-08-20 UTC)
ca6a690 | 2026-08-20 09:59:04 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-20 UTC)
0c54787 | 2026-08-20 06:24:11 +0800 | Mandate agent registry entry for new sibling instances
983ab02 | 2026-08-20 03:03:57 +0800 | chore(previews): refresh Beer Hall preview (2026-08-19 UTC)
e28c586 | 2026-08-20 03:03:56 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-19 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
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
2d85e9b | 2026-08-19 05:06:10 +0800 | Merge pull request #392 from TrueSightDAO/docs/tree-planting-link-schema
9ee6e94 | 2026-08-18 21:05:27 +0000 | Document [TREE PLANTING LINK EVENT], its new columns, and its endpoints
11de876 | 2026-08-19 04:44:48 +0800 | Merge pull request #391 from TrueSightDAO/feature/tree-planting-link-handler
d532ef3 | 2026-08-18 20:44:26 +0000 | Add [TREE PLANTING LINK EVENT] handler: link Sunmint submissions to sold QR codes
124c0c2 | 2026-08-19 04:36:38 +0800 | Merge pull request #390 from TrueSightDAO/feature/tree-planting-read-endpoints
e79c9b6 | 2026-08-18 20:36:10 +0000 | Add governor-gated read endpoints for the tree-planting linking picker
47c2dc1 | 2026-08-19 04:31:16 +0800 | Merge pull request #389 from TrueSightDAO/feature/qr-sold-date-column
63c5072 | 2026-08-18 20:30:39 +0000 | Add Sold Date column (W) to Agroverse QR codes; exclude ASSIGNED_TO_TREE from availability pickers
67373a9 | 2026-08-16 19:28:35 +0800 | feat(1ovx): email notification for subscription renewal payments on ledger (#387)
29c4898 | 2026-08-16 19:23:17 +0800 | sync(1ovx): commit live agroverse_shop_checkout.js from production clasp pull (#386)
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
d206ab7 | 2026-08-21 07:09:39 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
1fdd50d | 2026-08-20 18:28:47 +0800 | chore: refresh Agroverse store inventory snapshot
1cb9039 | 2026-08-20 07:08:40 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
66f6778 | 2026-08-19 07:07:42 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
efbaec2 | 2026-08-18 07:06:39 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
2649f45 | 2026-08-17 07:38:57 +0000 | chore: refresh partners-velocity snapshot [skip ci]
af2a122 | 2026-08-17 07:18:29 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
06232e8 | 2026-08-17 03:28:41 +0800 | chore: refresh Agroverse store inventory snapshot
70e69b1 | 2026-08-16 07:01:45 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b1d29ce | 2026-08-15 06:59:28 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
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

### `beer-hall_2026-08-22T011925Z_cacao-tea-launch-media-refactor.md`

- **posted_at_utc:** `2026-08-22T01:19:25Z`  
- **slug:** `cacao-tea-launch-media-refactor`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Retail** — Launched Cacao Tea 50g (Oscar's Farm) for offline QR-scan sales and added product cards to category and farm pages.

### `beer-hall_2026-08-19T012020Z_tree-planting-links-ivy-page.md`

- **posted_at_utc:** `2026-08-19T01:20:20Z`  
- **slug:** `tree-planting-links-ivy-page`  
- **Message 1 excerpt (first two non-empty lines):**

  - **Sunmint** — Activated the link between sold QR codes and tree-planting submissions, enabling direct traceability from purchased bar to specific farm trees.
  - **Web** — Published the IVY (Liv for Yoga) program page to the main site to support partner visibility.

### `beer-hall_2026-08-18T011823Z_ledger-notifications-advisor-update.md`

- **posted_at_utc:** `2026-08-18T01:18:23Z`  
- **slug:** `ledger-notifications-advisor-update`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Payments** — Enabled automated email notifications for subscription renewal payments directly on the ledger.

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
