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

- Generated (UTC): `2026-10-08T05:02:57Z`
- Look-back: **7** calendar days (`2026-10-01` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-10-05T10:59:14.227Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **1064**, follow_up **71**, bulk **0**, unknown **2** (data rows: **1137**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **62** stores — sum logged **warmup** sends (AU): **991**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **61**; follow-up depth (none / once / ≥2): **62** / **0** / **0**
- **Manager Follow-up**: **37** stores — sum logged **warmup** sends (AU): **15**, sum logged **follow-up** sends (AV): **71**; warmup depth (none / once / ≥2): **31** / **1** / **5**; follow-up depth (none / once / ≥2): **14** / **5** / **18**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: **2** stores — sum logged **warmup** sends (AU): **17**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **0** / **0** / **2**; follow-up depth (none / once / ≥2): **2** / **0** / **0**
- **Follow-up pipeline (combined)**: **39** stores — sum logged **warmup** sends (AU): **32**, sum logged **follow-up** sends (AV): **71**; warmup depth (none / once / ≥2): **31** / **1** / **7**; follow-up depth (none / once / ≥2): **16** / **5** / **18**

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
- Manager record: `Kirsten Ritschel` · 16 SKU lines · 1,332 total units · $1,450.34

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 11 | 390 | $798.89 |
  | Cacao Mass | Bulk | 1 | 50 | $1.55 |

**Matheus Reis** _( Ilhéus, Brazil — bulk warehouse + freight to SF )_
- Manager record: `Matheus Reis` · 33 SKU lines · 2,360.22 total units · $9,876.98

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 2 | 1,038 | $722.13 |
  | (uncategorized) | (unspecified) | 20 | 454.13 | $2,380.58 |
  | Cacao Bean | Bulk | 3 | 328.59 | $574.54 |
  | Cacao Mass | Retail Ready | 1 | 170 | $1,762.90 |
  | Cacao Tea | Bulk | 5 | 155.50 | $1,577.59 |
  | Cacao Nib | Retail Ready | 1 | 134 | $889.76 |
  | Cacao Nib | Bulk | 1 | 80 | $1,969.48 |

**Gary Teh** _( Operational cash + assorted retail inventory )_
- Manager record: `Gary Teh` · 29 SKU lines · 12,929.72 total units · $12,629.41

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 27 | 12,853.54 | $12,579.42 |
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
| Paloma | 7 | 661.32 | $247.02 |
| Go Ask Alice - Niccolina Ammerman | 2 | 14 | $115.81 |

_(+31 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_No lines matched name/keyword heuristics in this window._

_(No `YYYY-MM-DD |` lines on/after 2026-10-01 in CONTEXT_UPDATES.md.)_

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
de46cc3 | 2026-10-07 23:16:12 +0000 | chore(stats): refresh stats indexes [skip ci]
d8953e0 | 2026-10-07 13:47:51 +0000 | chore(stats): refresh stats indexes [skip ci]
81d402d | 2026-10-07 06:22:20 +0000 | chore(stats): refresh stats indexes [skip ci]
1cd9948 | 2026-10-06 22:45:44 +0000 | chore(stats): refresh stats indexes [skip ci]
53a513c | 2026-10-06 18:34:05 +0000 | chore(stats): refresh stats indexes [skip ci]
c9e0ff3 | 2026-10-06 06:47:19 +0000 | chore(stats): refresh stats indexes [skip ci]
71178a8 | 2026-10-06 00:16:25 +0000 | chore(stats): refresh stats indexes [skip ci]
1f39db3 | 2026-10-05 19:49:44 -0300 | AGL4 shipment page: status SALES IN PROGRESS → COMPLETED (#412)
29562a7 | 2026-10-05 19:47:44 -0300 | AGL8 + AGL14 shipment pages: status MANUFACTURING → SALES IN PROGRESS (#411)
03caeea | 2026-10-05 19:43:56 -0300 | AGL7 shipment page: status FREIGHTING IN PROGRESS → COMPLETED (#410)
f716984 | 2026-10-05 15:11:59 +0000 | chore(stats): refresh stats indexes [skip ci]
ad8b7f4 | 2026-10-05 06:07:14 +0000 | chore(stats): refresh stats indexes [skip ci]
2e29164 | 2026-10-04 21:51:47 +0000 | chore(stats): refresh stats indexes [skip ci]
20d8b6c | 2026-10-04 12:48:19 +0000 | chore(stats): refresh stats indexes [skip ci]
963a975 | 2026-10-04 06:14:55 +0000 | chore(stats): refresh stats indexes [skip ci]
0157846 | 2026-10-03 21:42:28 +0000 | chore(stats): refresh stats indexes [skip ci]
d7ec531 | 2026-10-03 16:37:56 +0000 | chore(stats): refresh stats indexes [skip ci]
ef44a3d | 2026-10-03 11:57:14 +0000 | chore(stats): refresh stats indexes [skip ci]
52816bb | 2026-10-03 05:39:38 +0000 | chore(stats): refresh stats indexes [skip ci]
1ceabe6 | 2026-10-02 22:29:34 +0000 | chore(stats): refresh stats indexes [skip ci]
438c973 | 2026-10-02 13:04:43 +0000 | chore(stats): refresh stats indexes [skip ci]
d5eaaa5 | 2026-10-02 06:05:13 +0000 | chore(stats): refresh stats indexes [skip ci]
6979798 | 2026-10-01 22:51:53 +0000 | chore(stats): refresh stats indexes [skip ci]
fba68ad | 2026-10-01 13:48:57 +0000 | chore(stats): refresh stats indexes [skip ci]
7d79dfa | 2026-10-01 06:27:02 +0000 | chore(stats): refresh stats indexes [skip ci]
```

### `market_research` → `go_to_market`

```
0c6a49d | 2026-10-05 22:49:03 -0300 | report: CN clearance batch 2 — Cabruca/Catongo/Itacare clear; Bahia REGISTERED (cl30+cl35) (#181)
```

### `agentic_ai_context` → `agentic_ai_context`

```
ce69546 | 2026-10-07 20:15:19 -0300 | chore(previews): refresh Beer Hall preview (2026-10-07 UTC)
b1488d3 | 2026-10-07 20:15:18 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-07 UTC)
a3c4c08 | 2026-10-07 03:18:13 -0300 | chore(previews): refresh Beer Hall preview (2026-10-07 UTC)
7f76863 | 2026-10-07 03:18:11 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-07 UTC)
78a3276 | 2026-10-06 15:32:48 -0300 | chore(previews): refresh Beer Hall preview (2026-10-06 UTC)
bb81fe6 | 2026-10-06 15:32:46 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-06 UTC)
c1b9bf3 | 2026-10-05 22:39:41 -0300 | docs(black-king): §5.10 col R — Ilheus trio AGL4->MAIN (AGL4 is COMPLETED) (#1513)
cd8ef51 | 2026-10-05 22:29:44 -0300 | docs(black-king): §5.10 add col R 'Ledger Name' + confirm AGL4 != MAIN (#1512)
fdbc32b | 2026-10-05 21:14:45 -0300 | chore(previews): refresh Beer Hall preview (2026-10-06 UTC)
86d8c58 | 2026-10-05 21:14:44 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-06 UTC)
8c58554 | 2026-10-05 19:59:00 -0300 | followups: record CN trademark tooling gaps (Chinese-mark images, TMview unreachable) (#1511)
6042d39 | 2026-10-05 19:50:36 -0300 | OPEN_FOLLOWUPS: file AGL9 broken ledger (status sweep, thread 40471) (#1510)
147ae0e | 2026-10-05 19:42:35 -0300 | Rev 5.10: col C = uCom unit counts (129/37/169 for pouch/bar/ceremonial lines) per PL Qty(uCom) (#1509)
c110a9d | 2026-10-05 19:41:43 -0300 | Rev aisle 5.10: in-transit rows v3 - drop Para, almonds->Cacao Almonds (KG) per AGL8 managed ledger, ceremonial confirmed (8 rows) (#1508)
f20bb47 | 2026-10-05 19:29:48 -0300 | docs(brazil): key in-transit register col B to currencies.json (Gary) (#1507)
14fd812 | 2026-10-05 19:16:17 -0300 | §5.10 In-transit register rows written (NF-e nº 18 lot → offchain assets in transit) (#1506)
e595d01 | 2026-10-05 19:03:35 -0300 | docs: queue manifest now writes Redis (primary) + GitHub (fallback) (#1505)
5e16da9 | 2026-10-05 12:46:48 -0300 | NF-e nº 18 confirmed FINAL (md5-identical to archived copy) (#1504)
1ca9de6 | 2026-10-05 12:39:58 -0300 | §5.9 Origin ops email thread: flight rescheduled depart 06/10 ETA 08/10 (#1503)
f1692d5 | 2026-10-05 12:37:50 -0300 | §5.8 MAWB issued: consolidated master AWB 047-3175-3223, executed 05/OCT/2026 (#1502)
412eb4a | 2026-10-05 12:36:23 -0300 | §5.7 Air waybill (HAWB) issued — 349 kg confirmed, DU-E registered (#1501)
d247f82 | 2026-10-05 12:07:20 -0300 | chore(previews): refresh Beer Hall preview (2026-10-05 UTC)
ac42754 | 2026-10-05 12:07:19 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-05 UTC)
0048827 | 2026-10-05 09:59:41 -0300 | §5.6 FDA Prior Notice gate: Iolanda needs the AWB (US import) (#1500)
8abbc03 | 2026-10-05 09:58:17 -0300 | §5.5: TAP (047) airline, flight-status HAWB gate, Caer storage, Iolanda-vs-Isis roles (#1499)
b966d24 | 2026-10-05 09:54:23 -0300 | Fix stale §8 row: gross divergence is carton tare, not pallet mass (#1498)
9528c49 | 2026-10-05 03:03:02 -0300 | chore(previews): refresh Beer Hall preview (2026-10-05 UTC)
67a4506 | 2026-10-05 03:03:01 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-05 UTC)
3d5a859 | 2026-10-04 18:46:38 -0300 | chore(previews): refresh Beer Hall preview (2026-10-04 UTC)
b14cd0c | 2026-10-04 18:46:36 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-04 UTC)
c119a63 | 2026-10-04 09:44:39 -0300 | chore(previews): refresh Beer Hall preview (2026-10-04 UTC)
280877a | 2026-10-04 09:44:38 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-04 UTC)
7c7db77 | 2026-10-04 03:11:55 -0300 | chore(previews): refresh Beer Hall preview (2026-10-04 UTC)
9ace75d | 2026-10-04 03:11:53 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-04 UTC)
5740e90 | 2026-10-03 20:58:15 -0300 | MAP §0: wire CIC (both zips) -> facility-cic-cacao-innovation-center; update §4.3 coverage (#1497)
b5930ff | 2026-10-03 20:56:39 -0300 | MAP: record courier queue manifest as machine-readable zip identity + oscar_fazenda_2026 register row (#1496)
39f49b4 | 2026-10-03 20:54:49 -0300 | docs: document queue manifest (media_upload_queue.json) + publisher timer in TRUESIGHT_MEDIA_COURIER.md
c0744f8 | 2026-10-03 20:49:07 -0300 | docs: rename COURIER.md → TRUESIGHT_MEDIA_COURIER.md (truesight_media_* naming) (#1495)
4d5614e | 2026-10-03 20:11:14 -0300 | MAP: file #36 backfill scope+divergence gap (thread 30550); record ilheus cards (#1494)
860f7d8 | 2026-10-03 19:24:30 -0300 | MAP plan: document stills source_zip as accepted gap (§4.2) (#1493)
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
f01b53c | 2026-10-07 13:29:35 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
22f9054 | 2026-10-06 13:37:16 +0000 | chore: refresh currencies.json [skip ci]
30fbdd4 | 2026-10-06 13:22:37 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
61f1230 | 2026-10-05 15:17:55 +0000 | chore: refresh partners-velocity snapshot [skip ci]
e1e2e82 | 2026-10-05 15:16:09 +0000 | chore: refresh currencies.json [skip ci]
51e7a2a | 2026-10-05 14:46:25 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
4d55c46 | 2026-10-04 12:51:04 +0000 | chore: refresh currencies.json [skip ci]
8c77900 | 2026-10-04 12:26:18 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
31f27dc | 2026-10-03 12:01:28 +0000 | chore: refresh currencies.json [skip ci]
bdd4651 | 2026-10-03 11:43:45 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
762d8cb | 2026-10-02 13:10:22 +0000 | chore: refresh currencies.json [skip ci]
10cb1a7 | 2026-10-02 12:40:50 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
d9705f2 | 2026-10-01 13:53:44 +0000 | chore: refresh currencies.json [skip ci]
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

### `beer-hall_2026-10-08T050257Z_agl-shipments-complete-hawb-issued-oscar-loaded.md`

- **posted_at_utc:** `2026-10-08T05:02:57Z`  
- **slug:** `agl-shipments-complete-hawb-issued-oscar-loaded`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Shipments Completed** — AGL4 and AGL7 moved to COMPLETED; AGL8 + AGL14 advanced to SALES IN PROGRESS on site.

### `beer-hall_2026-09-29T044723Z_ledger-explorer-shipped-payout-filter-prod-gate.md`

- **posted_at_utc:** `2026-09-29T04:47:23Z`  
- **slug:** `ledger-explorer-shipped-payout-filter-prod-gate`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Ledger Explorer** — Shipped to prod: deep links per transaction, infinite scroll, inline expand, and SunMint tree-planting cross-links. Fixed dead hamburger on ~17 pages and a site-wide mobile horizontal-scroll breakage.

### `beer-hall_2026-09-20T035637Z_sunmint-explorer-and-santos-ops.md`

- **posted_at_utc:** `2026-09-20T03:56:37Z`  
- **slug:** `sunmint-explorer-and-santos-ops`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **SunMint** — Plot Explorer shell and supervision claim registered; production handoff delegated to Envoy.

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
