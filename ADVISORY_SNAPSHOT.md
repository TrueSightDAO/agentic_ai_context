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

- Generated (UTC): `2026-10-16T03:36:51Z`
- Look-back: **7** calendar days (`2026-10-09` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-10-14T10:59:14.625Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **1128**, follow_up **71**, bulk **0**, unknown **2** (data rows: **1201**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **66** stores — sum logged **warmup** sends (AU): **1056**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **5** / **0** / **61**; follow-up depth (none / once / ≥2): **66** / **0** / **0**
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
- Manager record: `Kirsten Ritschel` · 27 SKU lines · 1,888.50 total units · $13,271.19

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 892 | $649.90 |
  | (uncategorized) | (unspecified) | 14 | 396 | $895.00 |
  | Cacao Nib | Bulk | 2 | 179.50 | $6,046.57 |
  | Cacao Mass | Retail Ready | 1 | 169 | $2,328.82 |
  | Cacao Nib | Retail Ready | 1 | 129 | $1,355.79 |
  | Cacao Mass | Bulk | 2 | 87 | $898.06 |
  | Cacao Tea | Bulk | 1 | 21 | $572.25 |
  | Cacao Bean | Bulk | 1 | 10 | $352.80 |
  | Cacao Butter | Bulk | 1 | 5 | $172.00 |

**Matheus Reis** _( Ilhéus, Brazil — bulk warehouse + freight to SF )_
- Manager record: `Matheus Reis` · 27 SKU lines · 1,856.59 total units · $10,430.59

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 2 | 942 | $654.61 |
  | (uncategorized) | (unspecified) | 21 | 619.59 | $6,757.99 |
  | Cacao Mass | Retail Ready | 1 | 170 | $1,762.90 |
  | Cacao Nib | Bulk | 1 | 99 | $1,008.05 |
  | Cacao Tea | Bulk | 1 | 21 | $213.83 |
  | Cacao Nib | Retail Ready | 1 | 5 | $33.20 |

**Gary Teh** _( Operational cash + assorted retail inventory )_
- Manager record: `Gary Teh` · 29 SKU lines · 7,859.61 total units · $7,559.30

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 27 | 7,783.43 | $7,509.31 |
  | Packaging Material | Bulk | 1 | 74 | $49.98 |
  | Cacao Tea | Bulk | 1 | 2.18 | $0.00 |

### Other managers (top 8 by USD value)

| Manager | Items | Units | Value (USD) |
|---------|-------|-------|-------------|
| Sacred Earth Farms | 3 | 316 | $2,241.33 |
| AGL13 | 1 | 2,165.07 | $2,165.07 |
| Val Lapidus | 11 | 1,270 | $1,475.95 |
| Coopercabruca | 1 | 1,706 | $1,199.87 |
| Aga Marecka | 1 | 20 | $537.46 |
| Andrea Catalina Falcon Rios De Pabst | 3 | 223 | $328.62 |
| Shuar Design Boutique | 3 | 37 | $284.34 |
| Paloma | 7 | 661.32 | $255.43 |

_(+33 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_No lines matched name/keyword heuristics in this window._

_(No `YYYY-MM-DD |` lines on/after 2026-10-09 in CONTEXT_UPDATES.md.)_

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
3a0e493 | 2026-10-15 21:41:07 +0000 | chore(stats): refresh stats indexes [skip ci]
58a1889 | 2026-10-15 17:17:43 +0000 | chore(stats): refresh stats indexes [skip ci]
1b1033c | 2026-10-15 11:59:16 +0000 | chore(stats): refresh stats indexes [skip ci]
8b9213f | 2026-10-15 05:04:33 +0000 | chore(stats): refresh stats indexes [skip ci]
9c168fa | 2026-10-14 21:53:56 +0000 | chore(stats): refresh stats indexes [skip ci]
54c49bb | 2026-10-14 17:32:09 +0000 | chore(stats): refresh stats indexes [skip ci]
da65923 | 2026-10-14 12:16:56 +0000 | chore(stats): refresh stats indexes [skip ci]
d5835e6 | 2026-10-14 05:16:59 +0000 | chore(stats): refresh stats indexes [skip ci]
f0008cc | 2026-10-13 23:03:59 +0000 | chore(stats): refresh stats indexes [skip ci]
145cf7c | 2026-10-13 14:30:38 +0000 | chore(stats): refresh stats indexes [skip ci]
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
```

### `market_research` → `go_to_market`

```
0bfa795 | 2026-10-10 20:19:35 -0300 | Add B2B email outreach funnel report (2026-09-29 PDF)
```

### `agentic_ai_context` → `agentic_ai_context`

```
8c98d5f | 2026-10-15 20:03:36 -0300 | Archive CFR Anapu payout PDF v3 (86/86 links resolve)
aeba6e1 | 2026-10-15 20:01:20 -0300 | OPEN_FOLLOWUPS: file CFR Anapu ingest-GPS-drop gap; mark pseudo-tree case resolved (#1657)
3ea8408 | 2026-10-15 19:26:32 -0300 | Add payout-report format SOP + file pseudo-tree index gap follow-up (#1656)
6965b5f | 2026-10-15 19:10:45 -0300 | Add PIX payout schedule with clickable per-tree links (CFR Anapu 2026-10-15)
5e75e31 | 2026-10-15 18:57:51 -0300 | Add PIX payout schedule PDF (86 trees, R$430) - CFR Anapu
150580d | 2026-10-15 18:57:03 -0300 | Merge pull request #1655 from TrueSightDAO/sop/cross-ledger-freight-settlement-phase8-r5-10
40a3c1e | 2026-10-15 18:56:21 -0300 | Merge pull request #1654 from TrueSightDAO/sop/cross-ledger-freight-settlement-phase8
cb98a01 | 2026-10-15 21:50:58 +0000 | §5.16: extend settlement SOP with rules 5-10 (reciprocal, Currencies, landed cost, AUM/treasury, numeric type, independent verification)
e02aeee | 2026-10-15 21:49:28 +0000 | Add §5.16 cross-ledger freight/investment settlement SOP + generic cost-allocation rule
bf717fc | 2026-10-15 18:37:24 -0300 | chore(previews): refresh Beer Hall preview (2026-10-15 UTC)
a20d54a | 2026-10-15 18:37:22 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-15 UTC)
be3641b | 2026-10-15 18:10:08 -0300 | conventions: inter-ledger holdings — directional naming, static price, consolidation elimination (#1653)
08e8461 | 2026-10-15 14:16:07 -0300 | chore(previews): refresh Beer Hall preview (2026-10-15 UTC)
bba799d | 2026-10-15 14:16:05 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-15 UTC)
7c26ce0 | 2026-10-15 11:23:08 -0300 | Plan: end-to-end Brazil->SF freight SOP refresh + machine-readable checklist (#1643)
feef4ae | 2026-10-15 11:17:22 -0300 | OPEN_FOLLOWUPS: E ruled — residual is server half; scope refined (handler is piece 3) (#1652)
5e4482d | 2026-10-15 10:14:44 -0300 | Freight plan §3: record C/D/E rulings (C validated vs NF-e nº 18 · D = AGL15 · E = Managed Ledger Transaction Event) (#1651)
f6255f6 | 2026-10-15 03:35:23 -0300 | followup: [MANAGED LEDGER TRANSACTION EVENT] client CLI shipped (#187); server registration residual (#1650)
241bf47 | 2026-10-15 02:37:57 -0300 | Freight plan §2.1: land AGL13 own-USD=$0.00 clarification (lost when #1638 closed unmerged) (#1649)
89420e0 | 2026-10-15 02:15:28 -0300 | Freight plan: §6 Currencies-catalog rows added to MAIN, §7 step 2 fully done (#1648)
933014a | 2026-10-15 02:13:35 -0300 | Dedupe §3-F in freight plan (fixes duplication left by #1638/#1645) (#1646)
f192af2 | 2026-10-15 02:05:06 -0300 | chore(previews): refresh Beer Hall preview (2026-10-15 UTC)
de998fd | 2026-10-15 02:05:05 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-10-15 UTC)
756d99f | 2026-10-15 01:59:47 -0300 | OPEN_FOLLOWUPS: AGL15 two bugs PARTIALLY OFFSET - true $4,471.77 not $4,644.10 (#1642)
81a06e3 | 2026-10-15 01:56:35 -0300 | Freight plan: close item H (beneficiary name not a discrepancy) (#1641)
ef14acf | 2026-10-15 01:55:21 -0300 | Freight plan 5.5: wire-fee reconciliation (30 USD does not vanish) (#1640)
52b22ae | 2026-10-15 01:53:19 -0300 | OPEN_FOLLOWUPS: AGL15 r66 A+B shell (3rd instance) + new expense double-insert class (11 pairs, -$403.35) (#1639)
59211ad | 2026-10-15 01:36:32 -0300 | OPEN_FOLLOWUPS: quantify treasury-cache negative-drop bug as a live AUM-surface divergence (AGL8 $5, AGL16 $1,868.92) (#1637)
50fbf69 | 2026-10-15 01:28:01 -0300 | Freight plan: correct §3-F (#REF! is in the AGL15-mirrored TBM ledger, not canonical AGL15) + add supersedes-#1629 pointer (#1636)
104b02c | 2026-10-15 01:13:23 -0300 | Freight plan: final — base $4,896.33 (+ $30 fee) + 5kg Para samples on Main; re-scale all legs (#1635)
a5df1c5 | 2026-10-15 01:02:05 -0300 | Freight plan: close item #1 (who paid) — direct debit against managed USD (#1633)
b3b7c59 | 2026-10-15 01:00:59 -0300 | Freight plan: cash-waterfall model — AGL8/AGL13 self-fund first, AGL15 covers shortfall (#1632)
d7986d0 | 2026-10-15 00:18:17 -0300 | Freight plan: add placeholders, exact payloads, Traps A-C, Transactions-only callout (#1631)
99d704e | 2026-10-15 00:14:25 -0300 | Freight plan: confirm $4,866.33 via Wells Fargo wire; close item A; add primitives (#1630)
1a556da | 2026-10-15 00:00:57 -0300 | Add FREIGHT_COST_AMORTIZATION_PLAN (5 Continent #1026-08, $4,866.33) (#1629)
4d9e552 | 2026-10-14 23:34:17 -0300 | Correct §5.15: only 2 of 3 pallets were transferred, not 3 (#1628)
c913c60 | 2026-10-14 23:30:05 -0300 | File OPEN_FOLLOWUPS: missing POST_REPACKAGING_CLEANUP webhook env var (#1627)
a7730f5 | 2026-10-14 23:28:13 -0300 | Release the brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md supervision claim (#1626)
c579285 | 2026-10-14 23:26:35 -0300 | Close out the Black King AGL8 corridor: §5.15 execution log + 2 tooling gaps (#1625)
47a1a36 | 2026-10-14 23:23:37 -0300 | Document the #REF! incident + correct idempotency behavior in the repackaging SOP (#1624)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
7dda371 | 2026-10-14 13:09:21 -0300 | Rename SunMint Plots col T from 'Contributor Name' to 'Farmer' (#582)
04d7acd | 2026-10-12 23:37:46 -0300 | Currency-definition ingest: write Currencies cols N-V + FDA Product Code (#581)
41848ed | 2026-10-09 11:26:16 -0300 | PR4: automate managed-ledger snapshot (Contents-API publisher + daily GHA) (#580)
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
285af84 | 2026-10-15 12:06:58 +0000 | chore: refresh currencies.json [skip ci]
7937880 | 2026-10-15 11:34:35 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
39eea85 | 2026-10-14 23:23:34 -0300 | Fix [REPACKAGING SETTLEMENT EVENT] handler writing directly to a derived tab (#18)
93d2b40 | 2026-10-14 22:16:44 -0300 | fix(inventory): packaging write-off composition — drop plastic pallet line (2 pallets transfer to Kirsten instead)
a5efcb9 | 2026-10-14 22:12:32 -0300 | fix(inventory): packaging write-off composition — plastic pallets consume 2 (was 3), leave 1
2573313 | 2026-10-14 22:09:22 -0300 | chore(inventory): packaging expense write-off composition 3c53976f (Black King)
4690a6a | 2026-10-14 18:28:46 -0300 | chore: refresh Agroverse SKU catalog snapshot
82a8c6c | 2026-10-14 18:28:44 -0300 | chore: refresh Agroverse store inventory snapshot
c98fec2 | 2026-10-14 12:22:09 +0000 | chore: refresh currencies.json [skip ci]
76b18cc | 2026-10-13 21:44:48 -0300 | chore: retire mislabeled currency BRL (currencies.json refresh)
8231b29 | 2026-10-13 14:16:46 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
a31a3db | 2026-10-12 22:20:19 -0300 | Add landed-cost composition for AWB 047-3175-3223 (8 clones)
f5d9baa | 2026-10-12 16:06:31 +0000 | chore: refresh currencies.json [skip ci]
aaaf54d | 2026-10-11 13:31:26 +0000 | chore: refresh currencies.json [skip ci]
f29de07 | 2026-10-11 12:55:27 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
1e973d5 | 2026-10-10 13:02:52 +0000 | chore: refresh currencies.json [skip ci]
d548ac7 | 2026-10-10 12:36:59 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
904093f | 2026-10-09 13:45:46 +0000 | chore: refresh currencies.json [skip ci]
55cb5bd | 2026-10-09 13:22:42 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
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

### `beer-hall_2026-10-16T033651Z_cfr-payout-live-settlement-sop-merged.md`

- **posted_at_utc:** `2026-10-16T03:36:51Z`  
- **slug:** `cfr-payout-live-settlement-sop-merged`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **CFR Anapu PIX Payout Schedule Shipped** — 86 trees, R$430 total, clickable per-tree links in PDF; all 86/86 links verified resolving.

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
