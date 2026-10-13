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

- Generated (UTC): `2026-10-13T05:56:06Z`
- Look-back: **7** calendar days (`2026-10-06` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-10-12T10:59:13.697Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **1112**, follow_up **71**, bulk **0**, unknown **2** (data rows: **1185**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **63** stores — sum logged **warmup** sends (AU): **1040**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **2** / **0** / **61**; follow-up depth (none / once / ≥2): **63** / **0** / **0**
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
- Manager record: `Matheus Reis` · 31 SKU lines · 2,135.59 total units · $14,064.89

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 2 | 942 | $654.61 |
  | (uncategorized) | (unspecified) | 24 | 689.59 | $7,566.26 |
  | Cacao Nib | Bulk | 2 | 179 | $2,977.53 |
  | Cacao Mass | Retail Ready | 1 | 170 | $1,762.90 |
  | Cacao Nib | Retail Ready | 1 | 134 | $889.76 |
  | Cacao Tea | Bulk | 1 | 21 | $213.83 |

**Gary Teh** _( Operational cash + assorted retail inventory )_
- Manager record: `Gary Teh` · 29 SKU lines · 12,874.96 total units · $12,574.65

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 27 | 12,798.78 | $12,524.66 |
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

_(No `YYYY-MM-DD |` lines on/after 2026-10-06 in CONTEXT_UPDATES.md.)_

---

## Pipeline activity map (PROJECT_INDEX ↔ git)

| Pipeline | Mapped clone | Activity in window |
|----------|----------------|----------------------|
| `go_to_market` | `market_research` | **yes** |
| `TrueChain` | `TrueChain` | **no** |
| `oracle` | `iching_oracle` | **yes** |

---

## Git log by repo (origin default branch)

### `truesight_me` → `truesight_me_beta`

```
60cc5a7 | 2026-10-13 00:56:04 +0000 | chore(stats): refresh stats indexes [skip ci]
d6401b8 | 2026-10-12 15:59:18 +0000 | chore(stats): refresh stats indexes [skip ci]
d5c6e4b | 2026-10-12 06:25:16 +0000 | chore(stats): refresh stats indexes [skip ci]
fb4f883 | 2026-10-11 22:22:57 +0000 | chore(stats): refresh stats indexes [skip ci]
7789df1 | 2026-10-11 13:24:08 +0000 | chore(stats): refresh stats indexes [skip ci]
fe5b0ab | 2026-10-11 06:19:27 +0000 | chore(stats): refresh stats indexes [skip ci]
42c94ed | 2026-10-10 21:57:29 +0000 | chore(stats): refresh stats indexes [skip ci]
69d8a81 | 2026-10-10 12:58:44 +0000 | chore(stats): refresh stats indexes [skip ci]
cda7801 | 2026-10-10 06:18:58 +0000 | chore(stats): refresh stats indexes [skip ci]
5f5efdd | 2026-10-09 22:50:28 +0000 | chore(stats): refresh stats indexes [skip ci]
e93e270 | 2026-10-09 13:41:38 +0000 | chore(stats): refresh stats indexes [skip ci]
8d2306d | 2026-10-09 06:35:34 +0000 | chore(stats): refresh stats indexes [skip ci]
c0cab46 | 2026-10-08 23:31:20 +0000 | chore(stats): refresh stats indexes [skip ci]
402e023 | 2026-10-08 13:56:57 +0000 | chore(stats): refresh stats indexes [skip ci]
efbe9ea | 2026-10-08 06:33:57 +0000 | chore(stats): refresh stats indexes [skip ci]
de46cc3 | 2026-10-07 23:16:12 +0000 | chore(stats): refresh stats indexes [skip ci]
d8953e0 | 2026-10-07 13:47:51 +0000 | chore(stats): refresh stats indexes [skip ci]
81d402d | 2026-10-07 06:22:20 +0000 | chore(stats): refresh stats indexes [skip ci]
1cd9948 | 2026-10-06 22:45:44 +0000 | chore(stats): refresh stats indexes [skip ci]
53a513c | 2026-10-06 18:34:05 +0000 | chore(stats): refresh stats indexes [skip ci]
c9e0ff3 | 2026-10-06 06:47:19 +0000 | chore(stats): refresh stats indexes [skip ci]
71178a8 | 2026-10-06 00:16:25 +0000 | chore(stats): refresh stats indexes [skip ci]
```

### `market_research` → `go_to_market`

```
0bfa795 | 2026-10-10 20:19:35 -0300 | Add B2B email outreach funnel report (2026-09-29 PDF)
```

### `agentic_ai_context` → `agentic_ai_context`

```
9adafeb | 2026-10-12 23:47:10 -0300 | plan(discord-gateway-resume): tick Deployed row + mark tracker COMPLETE (#1593)
4a14619 | 2026-10-12 23:44:46 -0300 | handoffs: close Discord gateway RESUME fix -- PLAN COMPLETE (#1592)
8ad9c2f | 2026-10-12 21:55:13 -0300 | chore(previews): refresh Beer Hall preview (2026-10-13 UTC)
83b3e26 | 2026-10-12 21:55:11 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-13 UTC)
5f4f256 | 2026-10-12 21:49:34 -0300 | OPEN_FOLLOWUPS: close AGL8 landed-clone rename; file GAS silent-success gap (#1591)
57a5902 | 2026-10-12 20:32:13 -0300 | OPEN_FOLLOWUPS: currency-naming hygiene (bare generic names) + AWB landed-clone convention (#1590)
6ff250e | 2026-10-12 12:54:11 -0300 | chore(previews): refresh Beer Hall preview (2026-10-12 UTC)
d42058e | 2026-10-12 12:54:09 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-12 UTC)
0fcebd6 | 2026-10-12 03:18:54 -0300 | chore(previews): refresh Beer Hall preview (2026-10-12 UTC)
f18adda | 2026-10-12 03:18:52 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-12 UTC)
23fec1b | 2026-10-11 21:45:47 -0300 | docs: file Julio enrichment sample-audit as a Sophia standing duty (#1589)
b12e167 | 2026-10-11 16:16:17 -0300 | docs: add task-design appendix to Julio's enrichment guide (#1588)
5fb6ec5 | 2026-10-11 14:58:59 -0300 | docs: add Julio store-enrichment guide (clean) (#1587)
838837a | 2026-10-11 14:52:55 -0300 | plans: file DAPP_ACCESS_RIGHTS_PLAN (UI-slice scope) + update OPEN_FOLLOWUPS entry (#1585)
0ddc827 | 2026-10-11 14:13:50 -0300 | handoffs: register DApp access-rights thread; update Discord gateway fix status (#1584)
3fa7ed1 | 2026-10-11 01:37:50 -0300 | Merge pull request #1583 from TrueSightDAO/auto/advisory-refresh-2026-10-11
aa0e839 | 2026-10-11 04:37:38 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-11 UTC)
6f1e742 | 2026-10-10 20:31:54 -0300 | plan(discord-gateway-resume): tick PR0 tracker — PR opened + merged (1ca1dcc) (#1582)
6493861 | 2026-10-10 19:59:41 -0300 | handoffs: release plans/DISCORD_GATEWAY_RESUME_BACKOFF_FIX_PLAN.md (Sophia (autopilot, self))
f2e4c74 | 2026-10-10 19:56:39 -0300 | handoffs: claim Discord gateway RESUME fix (thread 41950) (#1581)
f8ab2c7 | 2026-10-10 19:51:10 -0300 | handoffs: claim plans/DISCORD_GATEWAY_RESUME_BACKOFF_FIX_PLAN.md (Sophia (autopilot, self))
41eb375 | 2026-10-10 19:50:06 -0300 | Plan: Discord gateway RESUME + backoff reset fix (#1580)
47260d5 | 2026-10-10 18:55:47 -0300 | chore(previews): refresh Beer Hall preview (2026-10-10 UTC)
28b2c27 | 2026-10-10 18:55:46 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-10 UTC)
67c9a6a | 2026-10-10 17:34:33 -0300 | docs(calendar): the watchdog is the runner — fold in Gary's correction (#1579)
ada29f1 | 2026-10-10 17:31:03 -0300 | docs(followups): move Discord member-replies from Pending to Recently shipped (tier-aware replies live) (#1577)
716f9c8 | 2026-10-10 11:30:57 -0300 | VERDICT: AWB says 349,000 kg — Graziela's 365 kg claim refuted by the document she cites (#1576)
5058a98 | 2026-10-10 09:53:31 -0300 | chore(previews): refresh Beer Hall preview (2026-10-10 UTC)
6c72106 | 2026-10-10 09:53:30 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-10 UTC)
261b844 | 2026-10-10 09:30:55 -0300 | Status: USDA RELEASED shipment Fri 09/10 — no inspection, no surcharge; Graziela answers invoice questions (#1575)
f0bdcf6 | 2026-10-10 01:02:12 -0300 | Merge pull request #1573 from TrueSightDAO/handoffs/matheus-followup-complete-20261010
b905d8b | 2026-10-10 04:01:33 +0000 | handoffs: Matheus follow up items (thread 41588) COMPLETE — verified independently
5b22536 | 2026-10-10 00:59:57 -0300 | handoffs: release brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md (Sophia (autopilot, self))
b57ee52 | 2026-10-10 00:58:22 -0300 | handoffs: claim brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md (Sophia (autopilot, self))
ffecd10 | 2026-10-10 00:57:56 -0300 | handoffs: release brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md (Sophia (autopilot, self))
801db4b | 2026-10-10 00:57:46 -0300 | codify Ilhéus register (C2/C5/B2/B3/E1) + file calendar tooling note (#1572)
334cc6e | 2026-10-10 00:56:14 -0300 | handoffs: claim brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md (Sophia (autopilot, self))
2fc08f7 | 2026-10-10 00:51:09 -0300 | Merge pull request #1571 from TrueSightDAO/handoffs/matheus-pr524-merged-20261010
ad2278d | 2026-10-10 03:50:34 +0000 | handoffs: truesight_autopilot#524 merged (calendar watchdog, thread 41588)
75ee51b | 2026-10-10 00:44:44 -0300 | Merge pull request #1570 from TrueSightDAO/handoffs/matheus-followup-items-register-20261010
… (truncated)
```

### `tokenomics` → `tokenomics`

```
04d7acd | 2026-10-12 23:37:46 -0300 | Currency-definition ingest: write Currencies cols N-V + FDA Product Code (#581)
41848ed | 2026-10-09 11:26:16 -0300 | PR4: automate managed-ledger snapshot (Contents-API publisher + daily GHA) (#580)
465db28 | 2026-10-08 19:38:10 -0300 | Allow Sentinels to file inventory-expense events for ALL members (#579)
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
a31a3db | 2026-10-12 22:20:19 -0300 | Add landed-cost composition for AWB 047-3175-3223 (8 clones)
f5d9baa | 2026-10-12 16:06:31 +0000 | chore: refresh currencies.json [skip ci]
aaaf54d | 2026-10-11 13:31:26 +0000 | chore: refresh currencies.json [skip ci]
f29de07 | 2026-10-11 12:55:27 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
1e973d5 | 2026-10-10 13:02:52 +0000 | chore: refresh currencies.json [skip ci]
d548ac7 | 2026-10-10 12:36:59 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
904093f | 2026-10-09 13:45:46 +0000 | chore: refresh currencies.json [skip ci]
55cb5bd | 2026-10-09 13:22:42 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
7ce92a2 | 2026-10-08 13:35:15 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
f01b53c | 2026-10-07 13:29:35 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
22f9054 | 2026-10-06 13:37:16 +0000 | chore: refresh currencies.json [skip ci]
30fbdd4 | 2026-10-06 13:22:37 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
_(no commits on origin/main in window)_
```

### `iching_oracle` → `oracle`

```
ccda3c5 | 2026-10-09 10:51:12 -0300 | Stop padding stacked hexagram cards on mobile (#74)
063c5c9 | 2026-10-09 09:20:01 -0300 | Remove excess vertical whitespace in printed readings (#73)
```

### `Cypher-Defense` → `Cypher-Defense`

```
_(no commits on origin/master in window)_
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-10-13T055606Z_black-king-landed-cost-wire-sent.md`

- **posted_at_utc:** `2026-10-13T05:56:06Z`  
- **slug:** `black-king-landed-cost-wire-sent`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Wire Transfer to 5 Continent Logistics** — Invoice #1026-08 paid for Brazil→SF cacao consignment; disputed lines clarified with Graziela (export-customs scope, FDA AMS $100 filing, 365 vs 349 kg weight).

### `beer-hall_2026-10-11T043733Z_usda-released-gateway-fix-warehouse-codified.md`

- **posted_at_utc:** `2026-10-11T04:37:33Z`  
- **slug:** `usda-released-gateway-fix-warehouse-codified`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **USDA Released Shipment** — No inspection required, no surcharge; Graziela now answering invoice questions.

### `beer-hall_2026-10-09T050607Z_cooperative-first-sourcing-ilheus-wind-down.md`

- **posted_at_utc:** `2026-10-09T05:06:07Z`  
- **slug:** `cooperative-first-sourcing-ilheus-wind-down`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Cooperative-First Sourcing** — Documented strategic decision to prioritize cooperative sourcing and wind down Ilhéus warehouse operations.

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
