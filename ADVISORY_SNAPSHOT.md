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

- Generated (UTC): `2026-07-30T02:32:25Z`
- Look-back: **7** calendar days (`2026-07-23` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-07-29T10:59:13.680Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **670**
- Partnered (north-star): **14**

## Funnel by status (curated order)

- Reclassified — D2C only: 1  (#1)
- AI: Contact Form found: 119  (#3)
- Research: 53  (#8)
- AI: No fit signal: 164  (#9)
- AI: Enrich — manual: 95  (#10)
- Manager Follow-up: 33  (#13)
- Followed Up: 1  (#15)
- Instagram Followed: 11  (#18)
- Rejected: 16  (#19)
- On Hold: 19  (#20)
- Deferred / Revisit later: 6  (#21)
- **Partnered: 14**  (#22)
- AI: Warm up prospect: 64  (#9999)
- Not Appropriate: 74  (#9999)
- Reclassified — D2C only: 0  (#9999)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **585**, follow_up **70**, bulk **0**, unknown **2** (data rows: **657**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **64** stores — sum logged **warmup** sends (AU): **521**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **63**; follow-up depth (none / once / ≥2): **64** / **0** / **0**
- **Manager Follow-up**: **33** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **66**; warmup depth (none / once / ≥2): **30** / **1** / **2**; follow-up depth (none / once / ≥2): **11** / **5** / **17**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: _(no rows in this status)_
- **Follow-up pipeline (combined)**: **33** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **66**; warmup depth (none / once / ≥2): **30** / **1** / **2**; follow-up depth (none / once / ≥2): **11** / **5** / **17**

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
- Manager record: `Kirsten Ritschel` · 15 SKU lines · 1,345 total units · $1,569.88

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 10 | 403 | $918.43 |
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
- Manager record: `Gary Teh` · 27 SKU lines · 13,512.54 total units · $11,919.45

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 25 | 13,436.36 | $11,869.47 |
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

_No lines matched name/keyword heuristics in this window._

_(No `YYYY-MM-DD |` lines on/after 2026-07-23 in CONTEXT_UPDATES.md.)_

---

## Pipeline activity map (PROJECT_INDEX ↔ git)

| Pipeline | Mapped clone | Activity in window |
|----------|----------------|----------------------|
| `go_to_market` | `market_research` | **no** |
| `TrueChain` | `TrueChain` | **no** |
| `oracle` | `iching_oracle` | **yes** |

---

## Git log by repo (origin default branch)

### `truesight_me` → `truesight_me_beta`

```
caf27df | 2026-07-29 19:54:08 +0000 | chore(stats): refresh stats/current.json [skip ci]
67367c2 | 2026-07-29 14:54:05 +0000 | chore(stats): refresh stats/current.json [skip ci]
a7795f1 | 2026-07-29 09:23:14 +0000 | chore(stats): refresh stats/current.json [skip ci]
dd67901 | 2026-07-29 03:52:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
21eb1ca | 2026-07-28 20:03:24 +0000 | chore(stats): refresh stats/current.json [skip ci]
254a23b | 2026-07-28 15:02:00 +0000 | chore(stats): refresh stats/current.json [skip ci]
cc4874c | 2026-07-28 09:19:19 +0000 | chore(stats): refresh stats/current.json [skip ci]
6131fc5 | 2026-07-28 03:48:10 +0000 | chore(stats): refresh stats/current.json [skip ci]
fcabaca | 2026-07-27 20:06:41 +0000 | chore(stats): refresh stats/current.json [skip ci]
a65c861 | 2026-07-27 15:25:38 +0000 | chore(stats): refresh stats/current.json [skip ci]
d81df71 | 2026-07-27 10:27:23 +0000 | chore(stats): refresh stats/current.json [skip ci]
b287932 | 2026-07-27 04:24:50 +0000 | chore(stats): refresh stats/current.json [skip ci]
4b98174 | 2026-07-26 19:45:47 +0000 | chore(stats): refresh stats/current.json [skip ci]
76917e9 | 2026-07-26 14:11:00 +0000 | chore(stats): refresh stats/current.json [skip ci]
71d1c73 | 2026-07-26 08:58:44 +0000 | chore(stats): refresh stats/current.json [skip ci]
4e700fc | 2026-07-26 04:08:18 +0000 | chore(stats): refresh stats/current.json [skip ci]
9e8a677 | 2026-07-25 19:46:50 +0000 | chore(stats): refresh stats/current.json [skip ci]
6f084c2 | 2026-07-25 14:12:09 +0000 | chore(stats): refresh stats/current.json [skip ci]
10b5566 | 2026-07-25 08:32:58 +0000 | chore(stats): refresh stats/current.json [skip ci]
9416215 | 2026-07-25 03:51:11 +0000 | chore(stats): refresh stats/current.json [skip ci]
9162711 | 2026-07-24 19:57:29 +0000 | chore(stats): refresh stats/current.json [skip ci]
c56f0cf | 2026-07-24 14:22:18 +0000 | chore(stats): refresh stats/current.json [skip ci]
88517b2 | 2026-07-24 09:05:06 +0000 | chore(stats): refresh stats/current.json [skip ci]
ffa1c3a | 2026-07-24 03:55:55 +0000 | chore(stats): refresh stats/current.json [skip ci]
7d3eb6e | 2026-07-23 19:56:54 +0000 | chore(stats): refresh stats/current.json [skip ci]
92efb9d | 2026-07-23 14:51:36 +0000 | chore(stats): refresh stats/current.json [skip ci]
688c31f | 2026-07-23 09:11:09 +0000 | chore(stats): refresh stats/current.json [skip ci]
851f5bd | 2026-07-23 03:56:50 +0000 | chore(stats): refresh stats/current.json [skip ci]
```

### `market_research` → `go_to_market`

```
_(no commits on origin/main in window)_
```

### `agentic_ai_context` → `agentic_ai_context`

```
213e8d4 | 2026-07-30 03:52:32 +0800 | chore(previews): refresh Beer Hall preview (2026-07-29 UTC)
b5689fd | 2026-07-30 03:52:31 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-29 UTC)
24c6885 | 2026-07-29 22:41:30 +0800 | chore(previews): refresh Beer Hall preview (2026-07-29 UTC)
04f9e9d | 2026-07-29 22:41:29 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-29 UTC)
50406c7 | 2026-07-29 17:21:36 +0800 | chore(previews): refresh Beer Hall preview (2026-07-29 UTC)
c1bc336 | 2026-07-29 17:21:34 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-29 UTC)
2f2cb9a | 2026-07-29 11:49:59 +0800 | chore(previews): refresh Beer Hall preview (2026-07-29 UTC)
e9d8c94 | 2026-07-29 11:49:58 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-29 UTC)
c9a1d23 | 2026-07-29 04:01:05 +0800 | chore(previews): refresh Beer Hall preview (2026-07-28 UTC)
7117843 | 2026-07-29 04:01:04 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-28 UTC)
96956ad | 2026-07-28 22:59:06 +0800 | chore(previews): refresh Beer Hall preview (2026-07-28 UTC)
64da0f6 | 2026-07-28 22:59:03 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-28 UTC)
60497f1 | 2026-07-28 17:18:21 +0800 | chore(previews): refresh Beer Hall preview (2026-07-28 UTC)
fd94d9e | 2026-07-28 17:18:19 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-28 UTC)
251a89d | 2026-07-28 11:46:45 +0800 | chore(previews): refresh Beer Hall preview (2026-07-28 UTC)
03b2ca1 | 2026-07-28 11:46:44 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-28 UTC)
ecd1e06 | 2026-07-28 04:04:50 +0800 | chore(previews): refresh Beer Hall preview (2026-07-27 UTC)
0d12491 | 2026-07-28 04:04:48 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-27 UTC)
02a307e | 2026-07-27 23:23:52 +0800 | chore(previews): refresh Beer Hall preview (2026-07-27 UTC)
2ed895b | 2026-07-27 23:23:50 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-27 UTC)
6ab8f71 | 2026-07-27 18:26:42 +0800 | chore(previews): refresh Beer Hall preview (2026-07-27 UTC)
bd0b6c7 | 2026-07-27 18:26:41 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-27 UTC)
b8d2ec0 | 2026-07-27 15:03:27 +0800 | Add Cacao Club membership model proposal PDF
22a6336 | 2026-07-27 12:13:32 +0800 | chore(previews): refresh Beer Hall preview (2026-07-27 UTC)
ef120a9 | 2026-07-27 12:13:31 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-27 UTC)
79415f3 | 2026-07-27 10:31:09 +0800 | pdf(en): updated with 4 demographics, epicatechin, P&L
534bdec | 2026-07-27 10:31:04 +0800 | ppt(cn): compressed version 23MB→793KB
54a8e1a | 2026-07-27 10:31:00 +0800 | ppt(en): compressed version 23MB→794KB
db2fad5 | 2026-07-27 03:44:11 +0800 | chore(previews): refresh Beer Hall preview (2026-07-26 UTC)
fd54e5d | 2026-07-27 03:44:10 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-26 UTC)
a41e5a6 | 2026-07-26 22:08:12 +0800 | chore(previews): refresh Beer Hall preview (2026-07-26 UTC)
4af87e0 | 2026-07-26 22:08:11 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-26 UTC)
2a0fe49 | 2026-07-26 16:56:09 +0800 | chore(previews): refresh Beer Hall preview (2026-07-26 UTC)
3a7a882 | 2026-07-26 16:56:08 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-26 UTC)
567a2c9 | 2026-07-26 14:39:50 +0800 | Replace with full Mandarin CN PowerPoint - 13 slides, all content in Chinese
e18d328 | 2026-07-26 14:31:50 +0800 | Add slide mockdowns for easy reference and future modifications
07ef71b | 2026-07-26 14:31:35 +0800 | Add Chinese PowerPoint deck - 13 slides
239baea | 2026-07-26 14:31:28 +0800 | Add English PowerPoint deck - 13 slides cacao tea China opportunity
ab18d32 | 2026-07-26 14:22:53 +0800 | Update married couples tagline to 昨天的我们青春正好
b752522 | 2026-07-26 14:22:52 +0800 | Update married couples tagline to Yesterday We Were Young
… (truncated)
```

### `tokenomics` → `tokenomics`

```
1a7da01 | 2026-07-23 18:58:56 +0800 | Add Claude Pro subscription to Recurring Transactions sheet (#383)
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
a2580e9 | 2026-07-29 09:11:37 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8690717 | 2026-07-28 09:08:10 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
a3a04be | 2026-07-27 10:29:07 +0000 | chore: refresh partners-velocity snapshot [skip ci]
40f9d80 | 2026-07-27 10:11:01 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
01a0461 | 2026-07-26 08:40:51 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
f31d38f | 2026-07-25 08:25:53 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
a14d554 | 2026-07-24 08:45:05 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8dffed9 | 2026-07-23 08:46:14 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
_(no commits on origin/main in window)_
```

### `iching_oracle` → `oracle`

```
0bd1a09 | 2026-07-29 15:25:55 +0800 | Fix hexagram lines rendering blank in printed/exported PDFs (#64)
40c0070 | 2026-07-28 08:23:07 +0800 | Frame oracle readings as the operator's personal practice, not a DAO-wide directive (#63)
```

### `Cypher-Defense` → `Cypher-Defense`

```
_(no commits on origin/master in window)_
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-07-30T023225Z_cacao-club-and-oracle-updates.md`

- **posted_at_utc:** `2026-07-30T02:32:25Z`  
- **slug:** `cacao-club-and-oracle-updates`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Product (Oracle)** — Fixed blank lines in exported PDFs and reframed readings as personal practice rather than DAO directives.

### `beer-hall_2026-07-21T025013Z_dao-infrastructure-inventory-report.md`

- **posted_at_utc:** `2026-07-21T02:50:13Z`  
- **slug:** `dao-infrastructure-inventory-report`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Ops (Transparency)** — Published DAO asset, infrastructure, and agent inventory report to improve system visibility and tracking.

### `beer-hall_2026-07-20T032156Z_warmup-conversion-ssl-recovery-plan.md`

- **posted_at_utc:** `2026-07-20T03:21:56Z`  
- **slug:** `warmup-conversion-ssl-recovery-plan`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Sales (Conversion)** — Launched "WARMUP" conversion improvement plan to eliminate waste in sales onboarding.

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
