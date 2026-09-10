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

- Generated (UTC): `2026-09-10T03:36:38Z`
- Look-back: **7** calendar days (`2026-09-03` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-09-09T10:59:14.445Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **885**, follow_up **71**, bulk **0**, unknown **2** (data rows: **958**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **62** stores — sum logged **warmup** sends (AU): **809**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **61**; follow-up depth (none / once / ≥2): **62** / **0** / **0**
- **Manager Follow-up**: **34** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **71**; warmup depth (none / once / ≥2): **31** / **1** / **2**; follow-up depth (none / once / ≥2): **11** / **5** / **18**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: **2** stores — sum logged **warmup** sends (AU): **17**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **0** / **0** / **2**; follow-up depth (none / once / ≥2): **2** / **0** / **0**
- **Follow-up pipeline (combined)**: **36** stores — sum logged **warmup** sends (AU): **24**, sum logged **follow-up** sends (AV): **71**; warmup depth (none / once / ≥2): **31** / **1** / **4**; follow-up depth (none / once / ≥2): **13** / **5** / **18**

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
- Manager record: `Kirsten Ritschel` · 16 SKU lines · 1,335 total units · $1,467.21

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 11 | 393 | $815.77 |
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
- Manager record: `Gary Teh` · 28 SKU lines · 13,980.02 total units · $12,389.63

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 26 | 13,903.84 | $12,339.65 |
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

_(+29 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_No lines matched name/keyword heuristics in this window._

_(No `YYYY-MM-DD |` lines on/after 2026-09-03 in CONTEXT_UPDATES.md.)_

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
8e8054d | 2026-09-09 23:34:43 -0300 | fix(ci): stage the whole stats/ dir so new indexes can't be dropped (#370)
e2d6ccd | 2026-09-09 23:30:58 -0300 | Expose SunMint trees/plots/farms + MAP media archive to LLM discovery (#368)
c270bc6 | 2026-09-09 23:21:39 -0300 | SunMint impact map: show Plot Type in the plot popup (#369)
cd8af38 | 2026-09-09 21:07:07 +0000 | chore(stats): refresh stats/current.json [skip ci]
22bc114 | 2026-09-09 16:51:32 +0000 | chore(stats): refresh stats/current.json [skip ci]
9018e0c | 2026-09-09 11:46:10 +0000 | chore(stats): refresh stats/current.json [skip ci]
e37b0bd | 2026-09-09 05:05:24 +0000 | chore(stats): refresh stats/current.json [skip ci]
ce5624c | 2026-09-08 22:54:18 -0300 | SunMint map: Plots type-to-filter combobox + ?plot= opens popup (parity with Tree box) (#367)
46f211b | 2026-09-08 22:42:58 -0300 | test: add SunMint impact-map runtime smoke spec (#365)
77fa0fc | 2026-09-08 22:37:41 -0300 | fix: hoist esc() to IIFE scope (kills the silent map-render regression class) (#366)
0a86c8a | 2026-09-08 21:44:45 -0300 | Show tree photo in SunMint impact-map tree popup (#363)
f52ee46 | 2026-09-08 21:21:19 +0000 | chore(stats): refresh stats/current.json [skip ci]
a50e683 | 2026-09-08 16:48:57 +0000 | chore(stats): refresh stats/current.json [skip ci]
3236758 | 2026-09-08 11:40:00 +0000 | chore(stats): refresh stats/current.json [skip ci]
93aea68 | 2026-09-08 05:06:33 +0000 | chore(stats): refresh stats/current.json [skip ci]
5648f14 | 2026-09-07 22:26:01 -0300 | SunMint map: m.removeLayer -> map.removeLayer (fixes plot/farm select crashing handler before flyToBounds) (#362)
c9ebe7a | 2026-09-07 22:17:28 -0300 | SunMint map: unwrap nested Polygon rings before flyToBounds (fixes plot/farm dropdown not moving map) (#361)
f124247 | 2026-09-07 22:10:37 -0300 | SunMint map: View chips fly to their actual trees, not a hardcoded center (fixes empty ?view=altamira) (#360)
ebfd282 | 2026-09-07 22:01:42 -0300 | SunMint map: Tree/QR control is now a click-to-open dropdown with type-to-filter (#359)
adf89f2 | 2026-09-07 21:54:07 -0300 | SunMint impact map: grouped Plots dropdown (kills Farm select) + Tree/QR lookup box (#358)
0fa87db | 2026-09-07 21:44:39 +0000 | chore(stats): refresh stats/current.json [skip ci]
9b01cf7 | 2026-09-07 12:57:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
a2dae19 | 2026-09-07 05:08:18 +0000 | chore(stats): refresh stats/current.json [skip ci]
b8a3dc2 | 2026-09-06 20:45:16 +0000 | chore(stats): refresh stats/current.json [skip ci]
59b1e5f | 2026-09-06 15:42:23 +0000 | chore(stats): refresh stats/current.json [skip ci]
06f8bbf | 2026-09-06 11:16:59 +0000 | chore(stats): refresh stats/current.json [skip ci]
84db22e | 2026-09-06 05:00:22 +0000 | chore(stats): refresh stats/current.json [skip ci]
52fa3fc | 2026-09-05 22:23:11 -0300 | AGL6 pledge page ↔ Fazenda São Jorge farm profile cross-links (#356)
621891e | 2026-09-05 21:43:14 -0300 | AGL14 pledge page ↔ Oscar farm profile cross-links (#354)
5c8853d | 2026-09-05 21:29:11 -0300 | AGL16 — public ledger detail page (Wholesale Purchase Agreement, terms TBD) (#353)
26cb016 | 2026-09-05 20:40:03 +0000 | chore(stats): refresh stats/current.json [skip ci]
0de4969 | 2026-09-05 15:29:01 +0000 | chore(stats): refresh stats/current.json [skip ci]
acc2098 | 2026-09-05 10:52:15 +0000 | chore(stats): refresh stats/current.json [skip ci]
acdfb4e | 2026-09-05 04:52:46 +0000 | chore(stats): refresh stats/current.json [skip ci]
576b5c0 | 2026-09-04 20:58:57 +0000 | chore(stats): refresh stats/current.json [skip ci]
694a25a | 2026-09-04 14:23:32 -0300 | feat: deep-link a specific tree on the SunMint map, and link to it from the QR profile page (#352)
44f6c0a | 2026-09-04 16:33:36 +0000 | chore(stats): refresh stats/current.json [skip ci]
f0b0dd6 | 2026-09-04 11:50:58 -0300 | fix: plot pills silently vanished — two use-before-declare bugs in render() (#351)
f0baf95 | 2026-09-04 11:39:35 +0000 | chore(stats): refresh stats/current.json [skip ci]
b47113c | 2026-09-04 05:00:48 +0000 | chore(stats): refresh stats/current.json [skip ci]
… (truncated)
```

### `market_research` → `go_to_market`

```
445a5d7 | 2026-09-04 11:47:18 -0300 | Add bilingual EN-PT SunMint CEPOTX agreement (v2: Laguna Beach address, supported species, ISO-7810 card detail)
```

### `agentic_ai_context` → `agentic_ai_context`

```
75fae46 | 2026-09-10 00:30:58 -0300 | Add Cacau na Veia (Pacaje) media task plan — N-06-37 (#984)
cba635e | 2026-09-10 00:30:57 -0300 | docs(followups): file AGL 19Wag9x Credentials.js existence-guard gap (#985)
3c0c9de | 2026-09-09 23:37:08 -0300 | docs: register sunmint_index.json in LLM discovery surface table (#981)
d0e41e9 | 2026-09-09 23:35:42 -0300 | SUNMINT_TREE_PHOTO_PROCESSING §6: Plot Type required (#983)
e2e6a9a | 2026-09-09 23:16:50 -0300 | SUNMINT_PLOTS_REGISTRY §4b: single Plot Type column (7 values), maturing, sheet dropdown (#982)
dceeb7d | 2026-09-09 22:28:10 -0300 | docs(OPEN_FOLLOWUPS): add workflow-dispatch 403 gap; fix stale refresh advice (#980)
91bc6e9 | 2026-09-09 22:25:42 -0300 | docs(OPEN_FOLLOWUPS): plot_type live in index; file workflow-dispatch 403 gap (#979)
5562872 | 2026-09-09 22:21:32 -0300 | docs(OPEN_FOLLOWUPS): Plot Type header landed at col G — verified end-to-end, backfill is the remainder (#978)
b0f8bc0 | 2026-09-09 22:13:12 -0300 | SUNMINT_PLOTS_REGISTRY: document the plot_type (plot role) column + file the sheet backfill follow-up (#977)
fa1648a | 2026-09-09 18:05:01 -0300 | chore(previews): refresh Beer Hall preview (2026-09-09 UTC)
dea0220 | 2026-09-09 18:05:00 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-09 UTC)
f3d7dc2 | 2026-09-09 15:16:02 -0300 | plan: add mandatory security policy to email-inbox-watch plan (#976)
bd6e5eb | 2026-09-09 15:08:51 -0300 | plan: hourly admin+sophia@truesight.me inbox watch (#975)
a3a6205 | 2026-09-09 13:50:33 -0300 | chore(previews): refresh Beer Hall preview (2026-09-09 UTC)
d8dfc19 | 2026-09-09 13:50:31 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-09 UTC)
a0ee3d8 | 2026-09-09 08:43:28 -0300 | chore(previews): refresh Beer Hall preview (2026-09-09 UTC)
f7e162d | 2026-09-09 08:43:26 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-09 UTC)
711b638 | 2026-09-09 05:47:05 -0300 | docs: record SunMint map runtime smoke gate (sunmint-map.spec.ts) — mandatory green before beta→prod promote (#974)
e99ed6b | 2026-09-09 04:54:32 -0300 | docs: krake_ror recycled to v5 instance 98.81.159.70 + consolidated fleet df-alert (#973)
2ca9967 | 2026-09-09 04:41:20 -0300 | docs: mandatory machine self-UAT before any human UAT handoff (all Sophia instances) (#972)
d922245 | 2026-09-09 02:00:03 -0300 | chore(previews): refresh Beer Hall preview (2026-09-09 UTC)
379e136 | 2026-09-09 02:00:02 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-09 UTC)
6fd786f | 2026-09-08 22:40:27 -0300 | docs: mark cacao-varieties roadmap units 2–3 done (blob archive + manifest label layer) (#971)
7dcf21d | 2026-09-08 22:29:26 -0300 | docs: cacao-varieties namespace + attested field dossier (CCN-51 Ponta Verde vs common, Pará) (#970)
77c5c73 | 2026-09-08 21:49:43 -0300 | Sourcing network: Pará/CEPOTX lane gains in-network bean-to-bar conversion (#969)
6c70f02 | 2026-09-08 21:45:07 -0300 | docs: codify equipment-media MAP namespace decision (thread 23018) (#968)
4f08dde | 2026-09-08 18:19:56 -0300 | chore(previews): refresh Beer Hall preview (2026-09-08 UTC)
b0f31a9 | 2026-09-08 18:19:54 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-08 UTC)
c012b60 | 2026-09-08 15:46:59 -0300 | docs: sweep forward-facing /home/ubuntu + ~/media_archive_inbox media refs to /media (#967)
36de8f1 | 2026-09-08 14:41:48 -0300 | docs: document autopilot box /media disk layout (250GB EBS migration) in MEDIA_ARCHIVE_PIPELINE (#966)
b3fb292 | 2026-09-08 13:48:12 -0300 | chore(previews): refresh Beer Hall preview (2026-09-08 UTC)
3874085 | 2026-09-08 13:48:11 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-08 UTC)
bc49737 | 2026-09-08 09:26:17 -0300 | docs(handoff): mark São Jorge media long-pole complete (PR6) — UAT gate open (#955)
b8df1ac | 2026-09-08 08:35:16 -0300 | chore(previews): refresh Beer Hall preview (2026-09-08 UTC)
4a45f24 | 2026-09-08 08:35:14 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-08 UTC)
bf62d9d | 2026-09-08 02:00:20 -0300 | chore(previews): refresh Beer Hall preview (2026-09-08 UTC)
2c85886 | 2026-09-08 02:00:19 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-08 UTC)
249697a | 2026-09-07 22:23:17 -0300 | FSVP guide runbook: record 2026-09-08 delivery to Jedielcio (cepotx.organicos) (#965)
ab04c1a | 2026-09-07 22:11:35 -0300 | FSVP guide runbook: retrieval header + fix stale 10c placeholder note (#964)
d395fd2 | 2026-09-07 22:11:15 -0300 | Archive Gary-supplied melanger photo (used as 10c example in FSVP guide v5+)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
45b1acf | 2026-09-10 00:31:35 -0300 | Serialize plot-invalidation processor with LockService to stop duplicate tracking rows (#469)
aaab424 | 2026-09-09 23:37:29 -0300 | FBE GAS: harden .claspignore against Credentials deletion (#468)
2387315 | 2026-09-09 23:35:29 -0300 | FBE GAS: warn on missing required Plot Type (#467)
38167d9 | 2026-09-09 23:14:41 -0300 | FBE: add maturing to Plot Type vocab + warn on off-vocab plot_type (#466)
00a7616 | 2026-09-09 22:13:07 -0300 | FBE handler: capture Plot Type + stop dropping submitted Boundary Type on farmer plots (#465)
ca9ce8f | 2026-09-09 21:44:24 -0300 | SunMint ingestion: rows without lat/lng/photo start INVALID, never NEW (#464)
fed9cac | 2026-09-09 21:44:20 -0300 | SunMint reject: invalidate ALL rows matching the tree id, not just first match (#463)
67dd81a | 2026-09-09 18:05:19 -0300 | fix(expenses): serialize + re-verify hash before scoring to stop double-booking (#462)
27aea41 | 2026-09-09 05:47:54 -0300 | fix(gas): authorize expenses by registry Sentinel role, not hardcoded name (#461)
5416bf5 | 2026-09-06 12:18:09 -0300 | fix(gas): guard AGL expense processor (19Wag9x) credentials from clasp push deletion (#460)
08f8060 | 2026-09-06 01:01:11 -0300 | fix(gas): authorize DAO-agent (autopilot) expense filings for governors (#459)
7f767af | 2026-09-02 23:55:32 -0300 | fix(fbe): stop empty-field line-bleed in boundary evidence parser (#458)
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
04a91e9 | 2026-09-09 11:50:32 +0000 | chore: refresh currencies.json [skip ci]
91875ca | 2026-09-09 11:27:51 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b670bdc | 2026-09-09 07:29:12 -0300 | chore: refresh Agroverse store inventory snapshot
62fe5ed | 2026-09-08 11:44:02 +0000 | chore: refresh currencies.json [skip ci]
44d8995 | 2026-09-08 11:23:39 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
4cfaac0 | 2026-09-07 13:02:24 +0000 | chore: refresh partners-velocity snapshot [skip ci]
8af7d0c | 2026-09-07 13:00:40 +0000 | chore: refresh currencies.json [skip ci]
be4578f | 2026-09-07 12:38:54 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
ab627df | 2026-09-06 11:20:30 +0000 | chore: refresh currencies.json [skip ci]
0175b1c | 2026-09-06 11:01:33 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b74cebf | 2026-09-04 11:44:22 +0000 | chore: refresh currencies.json [skip ci]
1d3a534 | 2026-09-04 11:22:16 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
f597a45 | 2026-09-03 11:42:51 +0000 | chore: refresh currencies.json [skip ci]
546abfc | 2026-09-03 11:19:06 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
290b6e7 | 2026-09-09 05:30:39 -0300 | Add /agl15 + /agl16 legacy redirects to Google Sheets (#307)
a3931db | 2026-09-06 15:10:56 -0300 | fix(fazenda-bom-sucesso): point .farm-hero CSS at real sunmint hero, drop stale rancho-maranta template token (#306)
513b935 | 2026-09-06 12:16:19 -0300 | Add Fazenda Bom Sucesso to Brazilian Drift journey (#305)
d9aca71 | 2026-09-05 23:15:53 -0300 | Re-apply Fix JS SyntaxError breaking Santa Ana farm map (was reverted by Track A rollout) (#304)
d89bf9d | 2026-09-05 22:51:41 -0300 | Fazenda Clara: make SunMint plot highlight a real two-way link (FC-P1) (#303)
2457f94 | 2026-09-05 22:18:27 -0300 | Track A rollout: add Verified & Traceable FSVP blocks to 12 farm pages (#302)
0ad286a | 2026-09-05 22:12:09 -0300 | Add Fazenda Clara farm profile (Itacaré, Bahia) — Fernando & Clara, Black King supplier (#301)
ad9c54e | 2026-09-05 22:05:18 -0300 | Fix JS SyntaxError breaking Santa Ana farm map (stray semicolon before .openPopup) (#300)
7348115 | 2026-09-05 21:48:31 -0300 | Fazenda São Jorge: farm-visit photo gallery + SunMint plot SJ-P1 cross-link (#297)
5422ee6 | 2026-09-05 21:43:52 -0300 | Fazenda Santa Ana (Bahia): add farm-visit photo gallery + SunMint FSA-P1 cross-link (#299)
cbe8af5 | 2026-09-05 21:43:15 -0300 | Update paulo prose plot id LD-P1 to canonical V-06-29 (#298)
723f30d | 2026-09-05 21:42:39 -0300 | Add Fazenda Santa Ana family photo IMG_8261 (18 Sep 2023 farm visit)
3018c61 | 2026-09-05 21:42:38 -0300 | Add Fazenda Santa Ana drying check photo IMG_8247 (18 Sep 2023 farm visit)
ad73887 | 2026-09-05 21:42:37 -0300 | Add Fazenda Santa Ana drying terrace photo IMG_8224 (18 Sep 2023 farm visit)
4fd4a6e | 2026-09-05 21:42:36 -0300 | Add Fazenda Santa Ana harvest crew photo IMG_8181 (18 Sep 2023 farm visit)
96c45bf | 2026-09-05 21:42:34 -0300 | Add Fazenda Santa Ana fermentation room photo IMG_8117 (18 Sep 2023 farm visit)
96dad84 | 2026-09-05 21:42:33 -0300 | Add Fazenda Santa Ana fermentation photo IMG_8103 (18 Sep 2023 farm visit)
d2d21b8 | 2026-09-05 21:42:32 -0300 | Add Fazenda Santa Ana cacao pod photo IMG_8137 (18 Sep 2023 farm visit)
505abb9 | 2026-09-05 21:42:31 -0300 | Add Fazenda Santa Ana harvest photo IMG_8135 (18 Sep 2023 farm visit)
39e454a | 2026-09-05 21:35:02 -0300 | Oscar Bahia: add farm-visit photo gallery + SunMint AGL14 cross-link (#296)
c32c223 | 2026-09-05 21:27:08 -0300 | Swap legacy plot-id deep links (SA-P1/CL-P1/LD-P1/RG-P1) to canonical CEPOTX codes (#295)
f0dc50d | 2026-09-05 21:00:56 -0300 | Add Verified & Traceable FSVP block to Santa Anna + Cleide farm pages (#294)
c22ecae | 2026-09-05 21:00:54 -0300 | Add CEPOTX/COPOPS member farms as journey stops + hub stats update (#293)
0e00d84 | 2026-09-05 18:23:25 -0300 | Add Fazenda Santa Rosa IMG_8322 fruit harvesting photo (video frame) to gallery (#292)
4af08f9 | 2026-09-05 18:18:16 -0300 | Add Fazenda Santa Rosa IMG_8328 fermentation station photo to gallery (#291)
58f4784 | 2026-09-05 18:16:17 -0300 | Add Fazenda Santa Rosa IMG_8327 drying station photo to gallery (#290)
b66639c | 2026-09-05 17:32:34 -0300 | Fix IMG_8316 video ID (stale lVHN5OZ9HCY → GURyK-f94xA) (#289)
493eda2 | 2026-09-05 17:18:58 -0300 | Add Fazenda Santa Rosa YouTube video gallery (31 clips) (#288)
1056c45 | 2026-09-05 16:52:53 -0300 | Add Fazenda Santa Rosa farm profile (Antônio & Graça, U-06-06, Uruará) (#287)
a84e8b0 | 2026-09-05 16:42:15 -0300 | Sítio Raimundo & Geniza: IMG_8277 is drying station + fermentation station (#286)
8c5b608 | 2026-09-05 16:16:26 -0300 | Sítio Raimundo & Geniza: plot id RG-P1 -> CEPOTX site code U-06-07 (#285)
3e75bff | 2026-09-05 15:30:33 -0300 | Swap Fazenda Dona Rosa hero to governor-supplied photo (3 people)
7f712be | 2026-09-05 15:19:57 -0300 | Add Fazenda Dona Rosa (Pará) farm profile page — Rosa Wronscki, Medicilândia (#284)
c197e20 | 2026-09-05 10:54:35 -0300 | feat: embed Paulo's curated interview videos in fazenda-bom-sucesso media gallery (#283)
200bea4 | 2026-09-04 16:09:38 -0300 | Add COPOPS affiliation to Sítio Raimundo & Geniza profile; fix canonical URL + stale highlight (#282)
5045b47 | 2026-09-04 14:23:29 -0300 | feat: farm profile SunMint links deep-link to the farms specific plot (#278)
59d4007 | 2026-09-04 12:19:02 -0300 | feat(farms): add media.json gallery for fazenda-bom-sucesso (10 planting-day photos) (#281)
47006c7 | 2026-09-04 12:11:00 -0300 | fix(js): add missing comma after raimundo-geniza-para entry in brazilian-path-data.js (#280)
98379b7 | 2026-09-04 12:10:17 -0300 | Swap Sítio Raimundo & Geniza hero to Gary's new plot photo (#279)
cf15416 | 2026-09-04 12:09:48 -0300 | Add Sítio Raimundo & Geniza hero image (1280x960 landscape)
… (truncated)
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

### `beer-hall_2026-09-10T033637Z_sunmint-map-upgrades-plot-validation.md`

- **posted_at_utc:** `2026-09-10T03:36:37Z`  
- **slug:** `sunmint-map-upgrades-plot-validation`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **SunMint Map** — Added plot type filters and clickable dropdowns for Trees and Plots to improve map navigation; popups now display Plot Type and tree photos.

### `beer-hall_2026-09-07T032714Z_fsvp-blocks-fazenda-clara-ledger.md`

- **posted_at_utc:** `2026-09-07T03:27:14Z`  
- **slug:** `fsvp-blocks-fazenda-clara-ledger`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Compliance** — Added "Verified & Traceable" FSVP compliance blocks to 12 farm profiles, including Santa Ana, Cleide, and Oscar.

### `beer-hall_2026-09-05T032747Z_sunmint-deep-links-farms-cepotx-deal.md`

- **posted_at_utc:** `2026-09-05T03:27:47Z`  
- **slug:** `sunmint-deep-links-farms-cepotx-deal`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **New Farms** — Published profiles for Sítio Raimundo & Geniza and Fazenda Bom Sucesso (Pará), complete with planting-day galleries, YouTube embeds, and updated hero imagery.

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
