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

- Generated (UTC): `2026-08-07T02:44:48Z`
- Look-back: **7** calendar days (`2026-07-31` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-08-06T10:59:14.411Z`
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

- **Email Agent Follow Up** — logged sends: warmup **647**, follow_up **71**, bulk **0**, unknown **2** (data rows: **720**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **64** stores — sum logged **warmup** sends (AU): **584**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **63**; follow-up depth (none / once / ≥2): **64** / **0** / **0**
- **Manager Follow-up**: **33** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **67**; warmup depth (none / once / ≥2): **30** / **1** / **2**; follow-up depth (none / once / ≥2): **11** / **5** / **17**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: _(no rows in this status)_
- **Follow-up pipeline (combined)**: **33** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **67**; warmup depth (none / once / ≥2): **30** / **1** / **2**; follow-up depth (none / once / ≥2): **11** / **5** / **17**

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

_(No `YYYY-MM-DD |` lines on/after 2026-07-31 in CONTEXT_UPDATES.md.)_

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
413ae62 | 2026-08-07 00:25:41 +0000 | chore(stats): refresh stats/current.json [skip ci]
11f03e7 | 2026-08-06 14:56:42 +0000 | chore(stats): refresh stats/current.json [skip ci]
5de2bae | 2026-08-06 09:24:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
d7e0ce6 | 2026-08-06 03:51:47 +0000 | chore(stats): refresh stats/current.json [skip ci]
d3036ce | 2026-08-05 20:11:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
e62ca76 | 2026-08-05 14:57:50 +0000 | chore(stats): refresh stats/current.json [skip ci]
2b82746 | 2026-08-05 09:20:37 +0000 | chore(stats): refresh stats/current.json [skip ci]
16559a7 | 2026-08-05 03:46:20 +0000 | chore(stats): refresh stats/current.json [skip ci]
0f013d8 | 2026-08-04 20:10:26 +0000 | chore(stats): refresh stats/current.json [skip ci]
ed89f8a | 2026-08-04 15:04:50 +0000 | chore(stats): refresh stats/current.json [skip ci]
43a7a00 | 2026-08-04 09:22:43 +0000 | chore(stats): refresh stats/current.json [skip ci]
dd4a6c1 | 2026-08-04 03:51:05 +0000 | chore(stats): refresh stats/current.json [skip ci]
67fd004 | 2026-08-03 20:14:57 +0000 | chore(stats): refresh stats/current.json [skip ci]
cf4c46e | 2026-08-03 15:26:34 +0000 | chore(stats): refresh stats/current.json [skip ci]
aa9d193 | 2026-08-03 10:24:59 +0000 | chore(stats): refresh stats/current.json [skip ci]
a73eeee | 2026-08-03 04:09:05 +0000 | chore(stats): refresh stats/current.json [skip ci]
2a419ac | 2026-08-02 19:45:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
f7a856a | 2026-08-02 14:10:12 +0000 | chore(stats): refresh stats/current.json [skip ci]
f292701 | 2026-08-02 08:56:31 +0000 | chore(stats): refresh stats/current.json [skip ci]
c814abf | 2026-08-02 04:06:29 +0000 | chore(stats): refresh stats/current.json [skip ci]
575470b | 2026-08-01 19:46:31 +0000 | chore(stats): refresh stats/current.json [skip ci]
50edfaf | 2026-08-01 14:08:05 +0000 | chore(stats): refresh stats/current.json [skip ci]
33bd02c | 2026-08-01 08:54:26 +0000 | chore(stats): refresh stats/current.json [skip ci]
fd04396 | 2026-08-01 04:02:37 +0000 | chore(stats): refresh stats/current.json [skip ci]
f47edbe | 2026-07-31 20:05:24 +0000 | chore(stats): refresh stats/current.json [skip ci]
976cfd7 | 2026-07-31 15:02:02 +0000 | chore(stats): refresh stats/current.json [skip ci]
a6c9019 | 2026-07-31 09:25:17 +0000 | chore(stats): refresh stats/current.json [skip ci]
49489fe | 2026-07-31 12:39:21 +0800 | Add photo: sealing the pack
e7f1cfa | 2026-07-31 12:39:19 +0800 | Add photo: the ceremonial cacao pack
783d0ec | 2026-07-31 12:39:18 +0800 | Add photo: where the pack was signed (origin)
054d618 | 2026-07-31 04:03:29 +0000 | chore(stats): refresh stats/current.json [skip ci]
```

### `market_research` → `go_to_market`

```
4e4e9be | 2026-08-01 10:06:49 +0000 | chore: refresh warm-up conversion readout [skip ci]
```

### `agentic_ai_context` → `agentic_ai_context`

```
56caaa2 | 2026-08-07 08:24:13 +0800 | chore(previews): refresh Beer Hall preview (2026-08-07 UTC)
03fa478 | 2026-08-07 08:24:12 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-07 UTC)
15f4a4b | 2026-08-06 22:54:08 +0800 | chore(previews): refresh Beer Hall preview (2026-08-06 UTC)
a86ec0a | 2026-08-06 22:54:06 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-06 UTC)
ed8b7ca | 2026-08-06 17:21:35 +0800 | chore(previews): refresh Beer Hall preview (2026-08-06 UTC)
fb46220 | 2026-08-06 17:21:34 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-06 UTC)
564e507 | 2026-08-06 16:47:03 +0800 | v14: secure supply + price insulation goal (maintenance-cost peg)
a3dfba4 | 2026-08-06 16:46:27 +0800 | v13: machine-maintenance-cost barter anchor (bypass commodity price)
d737649 | 2026-08-06 16:28:15 +0800 | Update robotics-for-cacao barter PDF v12: sequence farmer receptiveness check before Gianluca farm visit
1f86459 | 2026-08-06 16:12:33 +0800 | Update robotics-for-cacao barter PDF v11: automation extends farmer ownership longevity (causal chain)
d4fef6d | 2026-08-06 15:56:26 +0800 | Update robotics-for-cacao barter PDF v10: cut & collect witches broom, no spray (agroforestry)
e89d2fe | 2026-08-06 15:55:13 +0800 | Update robotics-for-cacao barter PDF v9: add Problem 4 farm succession risk
7d2911f | 2026-08-06 15:51:12 +0800 | Update robotics-for-cacao barter PDF v8: restructure around 3 problems (broom, aging farmers, roast consistency)
0331c5d | 2026-08-06 15:46:49 +0800 | Update robotics-for-cacao barter PDF v7: remove DAO references
454154f | 2026-08-06 15:46:19 +0800 | Update robotics-for-cacao barter PDF v6: roast control as reinforcement learning problem
5d15cec | 2026-08-06 15:45:36 +0800 | Update robotics-for-cacao barter PDF v5: add §3 scalable roast control via particle detection
c6d934a | 2026-08-06 15:44:34 +0800 | Update robotics-for-cacao barter PDF v4: anonymize roles (drop Matheus/Sophia/CNPJ)
82798f4 | 2026-08-06 15:43:05 +0800 | Update robotics-for-cacao barter PDF v3: Frasky ref in context, §2, and pilot step 1
ef01339 | 2026-08-06 15:42:37 +0800 | Update robotics-for-cacao barter PDF: add Frasky working-prototype reference (§2)
e7e2b77 | 2026-08-06 15:19:13 +0800 | Add robotics-for-cacao barter action item PDF (2026-08-06)
53326c7 | 2026-08-06 11:48:59 +0800 | chore(previews): refresh Beer Hall preview (2026-08-06 UTC)
537e82b | 2026-08-06 11:48:58 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-06 UTC)
e818a63 | 2026-08-06 04:08:49 +0800 | chore(previews): refresh Beer Hall preview (2026-08-05 UTC)
227e9bb | 2026-08-06 04:08:47 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-05 UTC)
d8cf7eb | 2026-08-05 22:55:12 +0800 | chore(previews): refresh Beer Hall preview (2026-08-05 UTC)
f6bf5a3 | 2026-08-05 22:55:11 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-05 UTC)
9a8bd15 | 2026-08-05 17:19:05 +0800 | chore(previews): refresh Beer Hall preview (2026-08-05 UTC)
60478ac | 2026-08-05 17:19:03 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-05 UTC)
830ee09 | 2026-08-05 11:43:24 +0800 | chore(previews): refresh Beer Hall preview (2026-08-05 UTC)
143a77f | 2026-08-05 11:43:23 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-05 UTC)
ecab6ea | 2026-08-05 04:09:44 +0800 | chore(previews): refresh Beer Hall preview (2026-08-04 UTC)
8dd3948 | 2026-08-05 04:09:42 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-04 UTC)
5ddf304 | 2026-08-04 23:00:55 +0800 | chore(previews): refresh Beer Hall preview (2026-08-04 UTC)
6ceb4e4 | 2026-08-04 23:00:54 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-04 UTC)
d18eeac | 2026-08-04 17:20:28 +0800 | chore(previews): refresh Beer Hall preview (2026-08-04 UTC)
08f6ae2 | 2026-08-04 17:20:27 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-04 UTC)
e21fc64 | 2026-08-04 11:48:10 +0800 | chore(previews): refresh Beer Hall preview (2026-08-04 UTC)
86b6607 | 2026-08-04 11:48:09 +0800 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-04 UTC)
be07074 | 2026-08-04 10:42:35 +0800 | Merge pull request #730 from TrueSightDAO/auto/advisory-refresh-2026-08-04
f41c435 | 2026-08-04 02:42:24 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-08-04 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
_(no commits on origin/main in window)_
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
d1fa08f | 2026-08-06 09:08:36 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
a5787ce | 2026-08-05 09:07:58 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
1c71295 | 2026-08-04 09:10:57 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
16d8cd9 | 2026-08-03 10:26:45 +0000 | chore: refresh partners-velocity snapshot [skip ci]
2e3478f | 2026-08-03 10:07:58 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
da51bf2 | 2026-08-02 08:38:35 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
50493bf | 2026-08-01 08:35:48 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8876d46 | 2026-07-31 09:18:39 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
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

### `beer-hall_2026-08-07T024448Z_robotics-barter-strategy-maintenance-peg.md`

- **posted_at_utc:** `2026-08-07T02:44:48Z`  
- **slug:** `robotics-barter-strategy-maintenance-peg`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Strategy** — Finalized the "Robotics-for-Cacao Barter" action plan, proposing a maintenance-cost peg to bypass commodity price volatility.

### `beer-hall_2026-08-04T024220Z_prospera-operating-agreement-signed-china-market-strategy.md`

- **posted_at_utc:** `2026-08-04T02:42:20Z`  
- **slug:** `prospera-operating-agreement-signed-china-market-strategy`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Legal** — Filed the signed TrueSight DAO LLC Próspera Operating Agreement v1.0, formalizing the entity’s foundational framework.

### `beer-hall_2026-08-01T025616Z_cacao-pack-visuals-sop.md`

- **posted_at_utc:** `2026-08-01T02:56:16Z`  
- **slug:** `cacao-pack-visuals-sop`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Operations** — Updated Brazil-SF freight SOP to document three active NF-e blockers (CNAE, cert expiry, CNPJ Inapto) and added pre-flight checks.

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
