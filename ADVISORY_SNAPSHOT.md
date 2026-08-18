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

- Generated (UTC): `2026-08-18T01:18:24Z`
- Look-back: **7** calendar days (`2026-08-11` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-08-17T10:59:14.016Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **708**, follow_up **71**, bulk **0**, unknown **2** (data rows: **781**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **62** stores — sum logged **warmup** sends (AU): **629**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **61**; follow-up depth (none / once / ≥2): **62** / **0** / **0**
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

_No lines matched name/keyword heuristics in this window._

_(No `YYYY-MM-DD |` lines on/after 2026-08-11 in CONTEXT_UPDATES.md.)_

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
097c4d3 | 2026-08-14 19:31:11 +0000 | chore(stats): refresh stats/current.json [skip ci]
870fec3 | 2026-08-14 13:56:45 +0000 | chore(stats): refresh stats/current.json [skip ci]
5457e6b | 2026-08-14 07:58:20 +0000 | chore(stats): refresh stats/current.json [skip ci]
dd22aa5 | 2026-08-14 03:08:49 +0000 | chore(stats): refresh stats/current.json [skip ci]
080f7b7 | 2026-08-13 19:36:59 +0000 | chore(stats): refresh stats/current.json [skip ci]
06ca853 | 2026-08-13 14:01:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
8e4dfef | 2026-08-13 08:02:15 +0000 | chore(stats): refresh stats/current.json [skip ci]
cf50f72 | 2026-08-13 03:10:27 +0000 | chore(stats): refresh stats/current.json [skip ci]
0f66057 | 2026-08-12 19:41:11 +0000 | chore(stats): refresh stats/current.json [skip ci]
e820ba1 | 2026-08-12 14:05:14 +0000 | chore(stats): refresh stats/current.json [skip ci]
dded1eb | 2026-08-12 08:00:54 +0000 | chore(stats): refresh stats/current.json [skip ci]
8576ef4 | 2026-08-12 03:06:23 +0000 | chore(stats): refresh stats/current.json [skip ci]
6228897 | 2026-08-11 19:38:37 +0000 | chore(stats): refresh stats/current.json [skip ci]
35d8593 | 2026-08-11 13:59:37 +0000 | chore(stats): refresh stats/current.json [skip ci]
99bc749 | 2026-08-11 16:25:33 +0800 | Add Farmer App link to the Part 4 (Trees Registry) card too (#291)
f040442 | 2026-08-11 07:47:49 +0000 | chore(stats): refresh stats/current.json [skip ci]
48e4551 | 2026-08-11 02:36:29 +0000 | chore(stats): refresh stats/current.json [skip ci]
```

### `market_research` → `go_to_market`

```
_(no commits on origin/main in window)_
```

### `agentic_ai_context` → `agentic_ai_context`

```
7a80680 | 2026-08-18 03:08:14 +0800 | chore(previews): refresh Beer Hall preview (2026-08-17 UTC)
4d8f164 | 2026-08-18 03:08:13 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-17 UTC)
a6368fd | 2026-08-17 21:21:39 +0800 | chore(previews): refresh Beer Hall preview (2026-08-17 UTC)
1727975 | 2026-08-17 21:21:38 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-17 UTC)
dd1aaac | 2026-08-17 15:32:35 +0800 | chore(previews): refresh Beer Hall preview (2026-08-17 UTC)
a273171 | 2026-08-17 15:32:34 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-17 UTC)
3250419 | 2026-08-17 10:03:38 +0800 | chore(previews): refresh Beer Hall preview (2026-08-17 UTC)
7b894db | 2026-08-17 10:03:36 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-17 UTC)
f97f6f3 | 2026-08-17 06:30:45 +0800 | Add 7 followup blocks to OPEN_FOLLOWUPS (Matheus, PODream, Gianluca, Ling, Jerrie x2, Orlantildes) — all ping thread 11042 (#749)
667043c | 2026-08-17 02:56:29 +0800 | chore(previews): refresh Beer Hall preview (2026-08-16 UTC)
24a4818 | 2026-08-17 02:56:27 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-16 UTC)
1a49f22 | 2026-08-16 21:10:11 +0800 | chore(previews): refresh Beer Hall preview (2026-08-16 UTC)
1a089c9 | 2026-08-16 21:10:09 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-16 UTC)
a903ad5 | 2026-08-16 15:09:14 +0800 | chore(previews): refresh Beer Hall preview (2026-08-16 UTC)
54e6450 | 2026-08-16 15:09:13 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-16 UTC)
d51a20a | 2026-08-16 10:06:18 +0800 | chore(previews): refresh Beer Hall preview (2026-08-16 UTC)
c83fbff | 2026-08-16 10:06:17 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-16 UTC)
0723186 | 2026-08-16 02:56:59 +0800 | chore(previews): refresh Beer Hall preview (2026-08-15 UTC)
9e84da9 | 2026-08-16 02:56:58 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-15 UTC)
1fce9ca | 2026-08-15 21:08:25 +0800 | chore(previews): refresh Beer Hall preview (2026-08-15 UTC)
bbe1ef5 | 2026-08-15 21:08:24 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-15 UTC)
425be72 | 2026-08-15 15:13:52 +0800 | chore(previews): refresh Beer Hall preview (2026-08-15 UTC)
6a2411d | 2026-08-15 15:13:51 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-15 UTC)
a5f27ad | 2026-08-15 09:56:46 +0800 | chore(previews): refresh Beer Hall preview (2026-08-15 UTC)
683a100 | 2026-08-15 09:56:45 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-15 UTC)
27bc65a | 2026-08-15 03:29:36 +0800 | chore(previews): refresh Beer Hall preview (2026-08-14 UTC)
8c41eef | 2026-08-15 03:29:34 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-14 UTC)
7d1e65d | 2026-08-14 21:52:43 +0800 | chore(previews): refresh Beer Hall preview (2026-08-14 UTC)
82196eb | 2026-08-14 21:52:41 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-14 UTC)
47610f7 | 2026-08-14 15:57:55 +0800 | chore(previews): refresh Beer Hall preview (2026-08-14 UTC)
6a637ff | 2026-08-14 15:57:53 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-14 UTC)
1a7e3d7 | 2026-08-14 11:07:02 +0800 | chore(previews): refresh Beer Hall preview (2026-08-14 UTC)
7e937eb | 2026-08-14 11:07:00 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-14 UTC)
413c12b | 2026-08-14 03:34:53 +0800 | chore(previews): refresh Beer Hall preview (2026-08-13 UTC)
16fa83c | 2026-08-14 03:34:52 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-13 UTC)
828a3a9 | 2026-08-13 21:56:50 +0800 | chore(previews): refresh Beer Hall preview (2026-08-13 UTC)
3a5ed62 | 2026-08-13 21:56:48 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-13 UTC)
0f55e14 | 2026-08-13 16:01:07 +0800 | chore(previews): refresh Beer Hall preview (2026-08-13 UTC)
17a7f56 | 2026-08-13 16:01:05 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-13 UTC)
e55e83a | 2026-08-13 11:08:04 +0800 | chore(previews): refresh Beer Hall preview (2026-08-13 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
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
2649f45 | 2026-08-17 07:38:57 +0000 | chore: refresh partners-velocity snapshot [skip ci]
af2a122 | 2026-08-17 07:18:29 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
06232e8 | 2026-08-17 03:28:41 +0800 | chore: refresh Agroverse store inventory snapshot
70e69b1 | 2026-08-16 07:01:45 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b1d29ce | 2026-08-15 06:59:28 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
a5214b4 | 2026-08-14 07:53:30 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
3a0f243 | 2026-08-13 07:55:54 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
e7cd591 | 2026-08-12 07:54:38 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
07bec35 | 2026-08-11 07:39:48 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
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

### `beer-hall_2026-08-18T011823Z_ledger-notifications-advisor-update.md`

- **posted_at_utc:** `2026-08-18T01:18:23Z`  
- **slug:** `ledger-notifications-advisor-update`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Payments** — Enabled automated email notifications for subscription renewal payments directly on the ledger.

### `beer-hall_2026-08-12T020437Z_sunmint-ux-refine-freight-redirect.md`

- **posted_at_utc:** `2026-08-12T02:04:37Z`  
- **slug:** `sunmint-ux-refine-freight-redirect`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Product** — Refined Sunmint Farmer App UX following live beta testing, including a shift to tree-first reporting and live camera capture instead of file uploads.

### `beer-hall_2026-08-11T015201Z_oracle-fix-startup-summit-coordination.md`

- **posted_at_utc:** `2026-08-11T01:52:01Z`  
- **slug:** `oracle-fix-startup-summit-coordination`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Oracle** — Fixed a visual rendering bug where broken hexagram lines appeared as solid black blocks instead of transparent gaps.

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
