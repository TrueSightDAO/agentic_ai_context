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

- Generated (UTC): `2026-09-16T03:53:13Z`
- Look-back: **7** calendar days (`2026-09-09` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-09-15T10:59:13.658Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **0**

## Funnel by status (curated order)

- Reclassified — D2C only: 0  (—)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **921**, follow_up **71**, bulk **0**, unknown **2** (data rows: **994**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **62** stores — sum logged **warmup** sends (AU): **846**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **61**; follow-up depth (none / once / ≥2): **62** / **0** / **0**
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
- Manager record: `Matheus Reis` · 32 SKU lines · 2,255.22 total units · $8,558.35

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 2 | 1,038 | $722.13 |
  | (uncategorized) | (unspecified) | 19 | 348.13 | $1,055.31 |
  | Cacao Bean | Bulk | 3 | 328.59 | $574.54 |
  | Cacao Mass | Retail Ready | 1 | 170 | $1,762.90 |
  | Cacao Tea | Bulk | 5 | 155.50 | $1,577.59 |
  | Cacao Nib | Retail Ready | 1 | 135 | $896.40 |
  | Cacao Nib | Bulk | 1 | 80 | $1,969.48 |

**Gary Teh** _( Operational cash + assorted retail inventory )_
- Manager record: `Gary Teh` · 29 SKU lines · 14,193.52 total units · $12,911.41

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 27 | 14,117.34 | $12,861.43 |
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

_(+30 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_No lines matched name/keyword heuristics in this window._

_All dated lines on/after 2026-09-09_ (2):

- 2026-09-12 | sophia | `skus.json` SKU catalog now published by the `go_to_market` Python/GHA job (`sync_agroverse_store_inventory.py` + `publish-agroverse-inventory-snapshot.yml`, daily `15 6 * * *`) — PRs go_to_market #174 (emit A–I of the Agroverse SKUs tab) + #175 (`UNFORMATTED_VALUE` read so `priceUsd` is `25`, not `$25.00`; the DApp `define_currency.html` inputs `priceUsd` into a `type="number"` field). Verified live: commit `cf5d0c6` by `github-actions[bot]` 2026-09-12T23:56:32Z, `source = sync_agroverse_store_inventory`, 14 rows, `priceUsd = "25"`. New runbook `AGROVERSE_INVENTORY_PUBLISHERS.md` maps all four caches → publishers → crons → force-a-run; `OPEN_FOLLOWUPS.md` files the GAS-vs-Python two-writer hazard.
- 2026-09-14 | deepseek | Added `sophia/SUPERVISOR_LOOP.md` — directive for LLMs supervising Sophia: a bounded-WIP supervise loop (read the unfinished-work index → drive ≤2 threads at a time → first-round UAT → escalate only human gates), plus a first-round-UAT-vs-human-UAT split and a DEFAULT authority envelope (autonomous: go/retry/first-round-UAT/beta merges; human-only: TDG/money, account-only, final human UAT). **Governor decision 2026-09-14:** UAT is THREE rounds — R1 Sophia on beta → R2 Envoy on beta → R3 human UAT — and prod merge/promote executes ONLY after the human UAT thumbs-up (supervisor executes the merge, human authorizes via thumbs-up). SUGGESTED (canonical, not edited): add SUPERVIOR_LOOP.md to OPERATING_INSTRUCTIONS §2 read-order; add a machine-readable `handoffs/index.json` mirror (state enum + Telegram thread_id + Discord channel/thread id + last_updated).

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
c64b3ae | 2026-09-15 21:41:49 +0000 | chore(stats): refresh stats indexes [skip ci]
dab6722 | 2026-09-15 14:17:43 -0300 | PR6: repoint quests/ Trello redirects to sprint.truesight.me (4 layers x 2 files) (#380)
f1f3a9d | 2026-09-15 17:13:42 +0000 | chore(stats): refresh stats indexes [skip ci]
4d1bef9 | 2026-09-15 12:02:35 +0000 | chore(stats): refresh stats indexes [skip ci]
5719914 | 2026-09-15 05:13:09 +0000 | chore(stats): refresh stats indexes [skip ci]
edcd99b | 2026-09-14 21:37:26 -0300 | perf(media-gallery): lazy-load YouTube iframes to fix perceived-missing videos on load (#379)
55f1371 | 2026-09-14 21:27:55 -0300 | fix(crf-anapu): responsive 16:9 video/image boxes, fix squished YouTube embeds (#378)
5cf632f | 2026-09-14 21:58:47 +0000 | chore(stats): refresh stats indexes [skip ci]
d9f30e0 | 2026-09-14 13:15:42 +0000 | chore(stats): refresh stats indexes [skip ci]
159e9bd | 2026-09-14 05:21:26 +0000 | chore(stats): refresh stats indexes [skip ci]
f9f4f2c | 2026-09-13 21:05:17 +0000 | chore(stats): refresh stats indexes [skip ci]
1809777 | 2026-09-13 16:35:16 +0000 | chore(stats): refresh stats indexes [skip ci]
7c2d1d3 | 2026-09-13 12:14:24 +0000 | chore(stats): refresh stats indexes [skip ci]
b80534f | 2026-09-13 05:17:47 +0000 | chore(stats): refresh stats indexes [skip ci]
eae16a7 | 2026-09-12 20:52:19 +0000 | chore(stats): refresh stats indexes [skip ci]
e5edb34 | 2026-09-12 15:46:15 +0000 | chore(stats): refresh stats indexes [skip ci]
1a22e76 | 2026-09-12 08:22:56 -0300 | crf-anapu: add 14 site-visit videos to program gallery (#377)
3c2897a | 2026-09-12 11:11:35 +0000 | chore(stats): refresh stats indexes [skip ci]
6bee84b | 2026-09-12 04:55:43 +0000 | chore(stats): refresh stats indexes [skip ci]
ccaed47 | 2026-09-11 21:12:38 +0000 | chore(stats): refresh stats indexes [skip ci]
80355de | 2026-09-11 16:43:03 +0000 | chore(stats): refresh stats indexes [skip ci]
b64dd83 | 2026-09-11 11:47:05 -0300 | Fix blank-basemap zoom wall: upscale z17 imagery instead of requesting missing z18 tiles (#376)
14272f6 | 2026-09-11 10:43:28 -0300 | Add CRF Anapu program media gallery (program-page gallery convention) (#375)
f74382b | 2026-09-11 11:44:21 +0000 | chore(stats): refresh stats indexes [skip ci]
0523fbe | 2026-09-11 06:24:46 -0300 | Fix literal unicode escapes in crf-anapu pages (#374)
e5237ea | 2026-09-11 05:06:11 +0000 | chore(stats): refresh stats indexes [skip ci]
cd13355 | 2026-09-10 23:44:14 -0300 | Add CRF Anapu program credentialing surface (#373)
3b19b0f | 2026-09-10 22:54:19 -0300 | sunmint.html: show newest trees first in the Tree/QR dropdown (was capped at 20 rows) (#372)
010d259 | 2026-09-10 19:35:51 -0300 | sunmint.html: list plot's trees in the plot popup (join on plot_id) (#371)
b9d4e16 | 2026-09-10 21:07:52 +0000 | chore(stats): refresh stats indexes [skip ci]
a01b33a | 2026-09-10 16:38:38 +0000 | chore(stats): refresh stats indexes [skip ci]
5335493 | 2026-09-10 11:44:20 +0000 | chore(stats): refresh stats indexes [skip ci]
163418c | 2026-09-10 05:08:04 +0000 | chore(stats): refresh stats indexes [skip ci]
8e8054d | 2026-09-09 23:34:43 -0300 | fix(ci): stage the whole stats/ dir so new indexes can't be dropped (#370)
e2d6ccd | 2026-09-09 23:30:58 -0300 | Expose SunMint trees/plots/farms + MAP media archive to LLM discovery (#368)
c270bc6 | 2026-09-09 23:21:39 -0300 | SunMint impact map: show Plot Type in the plot popup (#369)
cd8af38 | 2026-09-09 21:07:07 +0000 | chore(stats): refresh stats/current.json [skip ci]
22bc114 | 2026-09-09 16:51:32 +0000 | chore(stats): refresh stats/current.json [skip ci]
9018e0c | 2026-09-09 11:46:10 +0000 | chore(stats): refresh stats/current.json [skip ci]
e37b0bd | 2026-09-09 05:05:24 +0000 | chore(stats): refresh stats/current.json [skip ci]
… (truncated)
```

### `market_research` → `go_to_market`

```
bed242c | 2026-09-12 20:47:55 -0300 | fix(go_to_market): read skus.json cells unformatted so priceUsd matches the GAS/dapp contract (#175)
```

### `agentic_ai_context` → `agentic_ai_context`

```
24ff59c | 2026-09-15 19:18:02 -0300 | handoffs: 30473 UAT passed, krake_nginx fix merged, held for Gary (#1219)
b475e55 | 2026-09-15 19:16:58 -0300 | docs(vault): record UAT results (U1-U7) on deployed 1254da2 (#1217)
96676b2 | 2026-09-15 19:16:00 -0300 | handoffs: 30471 self-fixed a real stale-auto-advance-directive bug (#1218)
bf4c549 | 2026-09-15 19:05:00 -0300 | handoffs: 30471 all 4 authorized items complete, held open pending Gary (#1216)
bb922d0 | 2026-09-15 19:03:51 -0300 | handoffs: 30471 tokenomics fix reviewed, merge classifier-blocked (#1215)
8901726 | 2026-09-15 19:00:24 -0300 | docs(uat): record UAT U1-U5 results + U5 per-key-emitter regression (frozen since 2026-06-18) (#1214)
5362c79 | 2026-09-15 18:38:12 -0300 | chore(previews): refresh Beer Hall preview (2026-09-15 UTC)
3b38ff2 | 2026-09-15 18:38:10 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-15 UTC)
a8a296c | 2026-09-15 18:31:06 -0300 | handoffs: 30471 finds 3-month per-key-generator regression; 30279 closed (#1213)
a20698d | 2026-09-15 18:28:26 -0300 | auto-advance close-out: mark plan COMPLETE (PR0–PR5); manifest row completed + index regen (#1211)
36f69b1 | 2026-09-15 18:26:40 -0300 | handoffs: 30475 U3 regression found + fixed, close-out retracted (#1212)
2d5e1c1 | 2026-09-15 18:24:28 -0300 | handoffs: 30279/30475 wrapping up, activate 30471/30473 (#1210)
767948c | 2026-09-15 18:21:29 -0300 | docs(auto-advance): PR5 — verified outcome, stale label fixes, tracker close-out (#1209)
71d1aed | 2026-09-15 18:20:19 -0300 | handoffs: SOPHIA_LIVE_PROGRESS_PLAN complete — UAT U1-U5 passed on deployed 1254da2 (#1208)
2a0d6f7 | 2026-09-15 18:00:40 -0300 | handoffs: deploy landed (1254da2) — activate 30279/30475, queue 30471/30473 (#1205)
7871229 | 2026-09-15 17:55:12 -0300 | handoffs: release plans/WARMUP_CONVERSION_IMPROVEMENT_PLAN.md (Sophia (autopilot, self))
8a46697 | 2026-09-15 17:54:12 -0300 | handoffs: claim plans/WARMUP_CONVERSION_IMPROVEMENT_PLAN.md (Sophia (autopilot, self))
ea7e673 | 2026-09-15 17:39:40 -0300 | handoffs: thread 30279 status corrected — blocked_on_human (#1204)
c2724de | 2026-09-15 17:29:14 -0300 | handoffs: thread 30279 PR2 merged (#474) — auto-advance marker drift fix (#1202)
21b6ef6 | 2026-09-15 16:32:59 -0300 | docs(auto-advance): PR0 pre-flight complete — capture incident #2 repro, correct root cause, rebase RESUME HERE (#1201)
c356142 | 2026-09-15 16:29:00 -0300 | handoffs: claim 30279, mark 30477 blocked_on_human (#1200)
8aa156d | 2026-09-15 16:11:28 -0300 | handoffs: claim 30477, refresh all active claims to current state (#1199)
f0bbf59 | 2026-09-15 16:10:26 -0300 | docs(vault): SSH credentials are vault-native; update plan RESUME + file 3 remaining gaps (#1198)
8a968ac | 2026-09-15 15:41:13 -0300 | PR5 step2 tracker: mark merged (#99) + step3 verdict (not needed) + Elizabeth Wong blocker + stale-directive meta-bug (#1197)
8281ef1 | 2026-09-15 15:27:01 -0300 | PR5 step1 tracker: mark merged (#470), RESUME HERE = PR5 step 2 (#1196)
e8612dd | 2026-09-15 15:18:16 -0300 | handoffs: claim 30473, refresh 30471 to PR5/blocked (#1195)
4672a1c | 2026-09-15 15:14:33 -0300 | chore(handoff): PR4 merged — tick tracker, RESUME HERE=PR5, regen index (#1194)
c1eefcb | 2026-09-15 14:49:10 -0300 | fix(plans+handoffs): tracker un-desync — RESUME=PR4, manifest in progress, regen index.json (#1193)
9fc1cb2 | 2026-09-15 14:45:30 -0300 | fix(plans): un-desync PUBLIC_KEY_LOOKUP_CACHE tracker (PR1–PR3 done; RESUME=PR4) (#1191)
a89d0ac | 2026-09-15 14:27:04 -0300 | handoffs: claim 30471, mark 30083/30475 blocked_on_human (#1190)
3d6fd74 | 2026-09-15 14:14:26 -0300 | PR5 close-out: UAT U1-U6 done (U3 bug fixed #1187), U7 blocked on deploy; RESUME\u2192PR6; +4 follow-ups (#1189)
cf66430 | 2026-09-15 14:12:26 -0300 | chore(previews): refresh Beer Hall preview (2026-09-15 UTC)
5fc3a8c | 2026-09-15 14:12:25 -0300 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-09-15 UTC)
a3030fa | 2026-09-15 14:06:22 -0300 | fix(auto-advance): reword prose 'RESUME HERE' mention so the parser stops latching onto it (#1188)
18d7fbf | 2026-09-15 14:01:01 -0300 | fix(board): strip backticks from Discord id cells so deep links aren't broken (#1187)
b51a0c7 | 2026-09-15 13:57:56 -0300 | PR4c close-out: mark DONE (#1181+#167+#466), advance RESUME markers to PR5 (#1186)
7cb5f8d | 2026-09-15 13:42:38 -0300 | register: Discord voice-attachment follow-up on the parity-gaps row (#1185)
af829a5 | 2026-09-15 13:23:14 -0300 | handoffs: refresh active supervision claims with current status (#1183)
ed18097 | 2026-09-15 13:23:13 -0300 | sophia: state the supervision-substitutes-for-gating principle generally (#1184)
30a8146 | 2026-09-15 13:16:53 -0300 | sophia: retire own-repo "never self-merge" rule for truesight_autopilot (#1182)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
9f2a248 | 2026-09-15 12:19:40 -0300 | docs(schema): document Currencies cols P-S + add T Source Documents (#493)
cd2648f | 2026-09-14 20:19:49 -0300 | fix(expenses): strip [ledger] prefix from Inventory Type before Column E write (#492)
bd12393 | 2026-09-13 15:21:13 -0300 | asset_receipt_ingest: fill empty Currencies D/E from Product Image / Landing Page labels (#491)
df418a0 | 2026-09-13 15:08:24 -0300 | docs(schema): add CNPJ + Physical Address cols to Agroverse Cacao Processing Cost (#490)
d9af5b9 | 2026-09-13 14:58:42 -0300 | feat(qr-gen): PR4 auto-define QR-ready currency from a batch QR request (thread 27015) (#489)
8e05cc3 | 2026-09-13 14:45:55 -0300 | feat(gas): RESERVATION + RESERVATION SETTLEMENT processors (unit 3) (#488)
3eb0156 | 2026-09-13 13:19:20 -0300 | fix(gas): repair sales project 1dsWecVwb HEAD drift (rename parser to live name, sync SOLD_DATE_COL, un-ignore) (#487)
a58b256 | 2026-09-13 09:46:32 -0300 | chore(gas): track secret-free Credentials.js for sales project + bump Version (#486)
d9f620b | 2026-09-13 01:22:18 -0300 | fix(1N6o00): currency-def parser must not leak next line on empty fields (#485)
5c6e948 | 2026-09-13 01:19:16 -0300 | fix(1N6o00): define missing findContributorByDigitalSignature() in currency-def handler (#484)
dc9ef29 | 2026-09-13 01:12:08 -0300 | fix(1N6o00): currency-def handler accepts Pending + writes terminal status (#483)
71dcfd2 | 2026-09-13 01:05:06 -0300 | fix(1N6o00): merge currency-definition action into the single doGet (duplicate doGet shadowed it) (#482)
18050d1 | 2026-09-13 00:21:37 -0300 | Add RESERVED QR status enum + exclude from availability pickers (#481)
3c92587 | 2026-09-12 22:40:05 -0300 | fix(scoring): stop grok scorer falsely stamping non-[CONTRIBUTION EVENT] rows as Successfully Completed (#479)
53f3075 | 2026-09-12 22:02:07 -0300 | dao_forms: add ?currency_fields action (farm/state/country distinct values) (#478)
afeaf42 | 2026-09-12 19:20:47 -0300 | update_store_inventory: emit agroverse-inventory/skus.json (SKU catalog cache) (#477)
2f411a0 | 2026-09-12 19:16:46 -0300 | currency definition GAS: write SKU Product ID (col M) + infer Serializable from SKU stock; fix A:L sort (#476)
054f700 | 2026-09-12 14:32:10 -0300 | fix(expense): disable proc script lock (contention stalled all runs) + stop false success (#475)
0100cd4 | 2026-09-10 16:30:37 -0300 | feat(tree-planting): optional Plot ID column (T) on SunMint Tree Planting (#474)
c9e7d18 | 2026-09-10 07:48:34 -0300 | Add regression guard: Telegram-log processors must take the script lock (#473)
765ae53 | 2026-09-10 00:48:00 -0300 | Serialize media-retraction + tree-growth processors with LockService (completes #469/#471 family) (#472)
33965af | 2026-09-10 00:45:06 -0300 | Serialize farm-boundary-evidence processor with LockService (same race as #469) (#471)
4946fd9 | 2026-09-10 00:40:03 -0300 | fix(gas): pre-push guard against missing live Credentials accessor (#470)
45b1acf | 2026-09-10 00:31:35 -0300 | Serialize plot-invalidation processor with LockService to stop duplicate tracking rows (#469)
aaab424 | 2026-09-09 23:37:29 -0300 | FBE GAS: harden .claspignore against Credentials deletion (#468)
2387315 | 2026-09-09 23:35:29 -0300 | FBE GAS: warn on missing required Plot Type (#467)
38167d9 | 2026-09-09 23:14:41 -0300 | FBE: add maturing to Plot Type vocab + warn on off-vocab plot_type (#466)
00a7616 | 2026-09-09 22:13:07 -0300 | FBE handler: capture Plot Type + stop dropping submitted Boundary Type on farmer plots (#465)
ca9ce8f | 2026-09-09 21:44:24 -0300 | SunMint ingestion: rows without lat/lng/photo start INVALID, never NEW (#464)
fed9cac | 2026-09-09 21:44:20 -0300 | SunMint reject: invalidate ALL rows matching the tree id, not just first match (#463)
67dd81a | 2026-09-09 18:05:19 -0300 | fix(expenses): serialize + re-verify hash before scoring to stop double-booking (#462)
27aea41 | 2026-09-09 05:47:54 -0300 | fix(gas): authorize expenses by registry Sentinel role, not hardcoded name (#461)
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
dcfef2e | 2026-09-15 12:07:30 +0000 | chore: refresh currencies.json [skip ci]
c5e911c | 2026-09-15 11:48:24 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
f6f2108 | 2026-09-14 13:22:27 +0000 | chore: refresh partners-velocity snapshot [skip ci]
75f6c32 | 2026-09-14 13:21:04 +0000 | chore: refresh currencies.json [skip ci]
f273dbc | 2026-09-13 12:16:38 +0000 | chore: refresh currencies.json [skip ci]
d5451d4 | 2026-09-13 11:57:01 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
cf5d0c6 | 2026-09-12 23:56:32 +0000 | chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]
de8a58b | 2026-09-12 20:28:34 -0300 | chore: refresh Agroverse SKU catalog snapshot
f9425a2 | 2026-09-12 14:21:54 -0300 | chore: refresh currencies.json [skip ci]
8ef82e7 | 2026-09-12 13:13:59 -0300 | chore(currencies): sync Currencies tab @ 2026-09-12T16:13:10.000Z (141)
0220cc5 | 2026-09-12 11:14:55 +0000 | chore: refresh currencies.json [skip ci]
bc1bb68 | 2026-09-12 10:51:36 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
bc37849 | 2026-09-11 11:48:14 +0000 | chore: refresh currencies.json [skip ci]
1112f40 | 2026-09-11 11:26:20 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
bea3cc9 | 2026-09-10 11:49:07 +0000 | chore: refresh currencies.json [skip ci]
fdb2e9f | 2026-09-10 11:24:18 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
04a91e9 | 2026-09-09 11:50:32 +0000 | chore: refresh currencies.json [skip ci]
91875ca | 2026-09-09 11:27:51 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b670bdc | 2026-09-09 07:29:12 -0300 | chore: refresh Agroverse store inventory snapshot
```

### `agroverse_shop` → `agroverse_shop_beta`

```
1390844 | 2026-09-12 22:33:13 -0300 | media-gallery: fetch-first published gallery with local fallback + curation merge (PR6) (#322)
2cdd03f | 2026-09-11 11:48:47 -0300 | brazilian-path: smooth south→north→west route, no backtracking (#321)
931df0a | 2026-09-11 11:31:34 -0300 | cacau-na-veia-pacaje: publish 33 site-visit videos in the farm page gallery (PR6) (#320)
604c4e5 | 2026-09-10 16:52:25 -0300 | farm(sitio-torres-pacaja-para): surface 35 site-visit videos in gallery (#319)
7c0b0cd | 2026-09-10 11:40:22 -0300 | Cristo Rei: deep-link SunMint highlight to plot CR-PA-P2 (reciprocity) (#318)
fa0586a | 2026-09-10 11:18:02 -0300 | fix(brazilian-path): list Sítio Cristo Rei in journeyOrder (#317)
9120e3d | 2026-09-10 10:47:03 -0300 | fix(farms): Cristo Rei hero → humans-first shot (IMG_9563) + map marker image (#316)
83445a6 | 2026-09-10 07:56:55 -0300 | Add Sítio Cacau na Veia (Pacajá) to cacao-journeys (#315)
5911c34 | 2026-09-10 07:50:35 -0300 | Align Sítio Torres CEPOTX card wording with peer farm pages (#314)
0703929 | 2026-09-10 07:50:30 -0300 | feat(farms): add Sítio Cristo Rei (Pacajá) farm page + nav card (#313)
af0bd9e | 2026-09-10 07:49:22 -0300 | Add dedicated CEPOTX highlight card to Sítio Torres farm page (#312)
328949e | 2026-09-10 07:48:09 -0300 | Add Sítio Torres (Pacajá) as a stop on the Brazilian cacao journey (#311)
4662efc | 2026-09-10 07:28:16 -0300 | Add Sítio Cacau na Veia (Pacajá) farm page — plots N-06-37 + restoration_1 (#310)
869c38a | 2026-09-10 07:19:29 -0300 | Rename Sitio Dois -> Sitio Torres (Pacaja, Para); plot N-06-66 (#309)
424b4d8 | 2026-09-10 00:47:26 -0300 | Add Sítio Dois (Pacajá) farm profile — plot N-06-66 (#308)
7843b36 | 2026-09-10 00:46:08 -0300 | Add sitio-2-pacaja-para photo IMG_9692
b83ba40 | 2026-09-10 00:46:07 -0300 | Add sitio-2-pacaja-para photo IMG_9689
96086b8 | 2026-09-10 00:46:06 -0300 | Add sitio-2-pacaja-para photo IMG_9688
cd95983 | 2026-09-10 00:46:04 -0300 | Add sitio-2-pacaja-para photo IMG_9687
a51dd95 | 2026-09-10 00:46:03 -0300 | Add sitio-2-pacaja-para photo IMG_9682
b21f763 | 2026-09-10 00:46:02 -0300 | Add sitio-2-pacaja-para photo IMG_9676
57f903f | 2026-09-10 00:46:01 -0300 | Add sitio-2-pacaja-para photo IMG_9673
84ace90 | 2026-09-10 00:45:59 -0300 | Add sitio-2-pacaja-para photo IMG_9666
81e86fb | 2026-09-10 00:45:58 -0300 | Add sitio-2-pacaja-para photo IMG_9662
6bcb851 | 2026-09-10 00:45:56 -0300 | Add sitio-2-pacaja-para photo IMG_9659
4a9070a | 2026-09-10 00:45:55 -0300 | Add sitio-2-pacaja-para photo IMG_9642
fe967cc | 2026-09-10 00:45:53 -0300 | Add sitio-2-pacaja-para photo IMG_9622
290b6e7 | 2026-09-09 05:30:39 -0300 | Add /agl15 + /agl16 legacy redirects to Google Sheets (#307)
```

### `iching_oracle` → `oracle`

```
_(no commits on origin/main in window)_
```

### `Cypher-Defense` → `Cypher-Defense`

```
0659ac2 | 2026-09-14 20:08:35 -0300 | Add weekly AMI backup for the nelanco-claude interactive Claude Code box (#42)
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-09-16T035312Z_reservation-settlement-and-cacau-na-veia.md`

- **posted_at_utc:** `2026-09-16T03:53:12Z`  
- **slug:** `reservation-settlement-and-cacau-na-veia`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Sales Logic** — Shipped RESERVATION + RESERVATION SETTLEMENT GAS processors (Unit 3) to support two-event sales models.

### `beer-hall_2026-09-15T035424Z_youtube-fix-repo-access-denylist-complete.md`

- **posted_at_utc:** `2026-09-15T03:54:24Z`  
- **slug:** `youtube-fix-repo-access-denylist-complete`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Media Performance** — Fixed squished YouTube embeds and implemented lazy-loading to resolve missing-video glitches on load.

### `beer-hall_2026-09-14T035447Z_sunmint-ux-reservation-logic-and-logistics.md`

- **posted_at_utc:** `2026-09-14T03:54:47Z`  
- **slug:** `sunmint-ux-reservation-logic-and-logistics`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **SunMint UX** — Added plot-specific tree lists to popups and sorted tree dropdowns by newest first.

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
