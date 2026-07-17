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

- Generated (UTC): `2026-07-17T02:47:54Z`
- Look-back: **7** calendar days (`2026-07-10` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

_Not yet configured. Add `GROWTH_GOALS.json` at `/home/runner/work/go_to_market/go_to_market/repos/agentic_ai_context` with a `{"goals": [...]}` object to surface progress here._

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-07-16T10:59:14.444Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **670**
- Partnered (north-star): **14**

## Funnel by status (curated order)

- Reclassified — D2C only: 1  (#1)
- AI: Contact Form found: 119  (#3)
- Research: 59  (#8)
- AI: No fit signal: 158  (#9)
- AI: Enrich — manual: 95  (#10)
- Manager Follow-up: 33  (#13)
- Followed Up: 1  (#15)
- Instagram Followed: 11  (#18)
- Rejected: 15  (#19)
- On Hold: 18  (#20)
- Deferred / Revisit later: 6  (#21)
- **Partnered: 14**  (#22)
- AI: Warm up prospect: 66  (#9999)
- Not Appropriate: 74  (#9999)
- Reclassified — D2C only: 0  (#9999)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **498**, follow_up **70**, bulk **0**, unknown **2** (data rows: **570**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **66** stores — sum logged **warmup** sends (AU): **450**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **1** / **0** / **65**; follow-up depth (none / once / ≥2): **66** / **0** / **0**
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

_Lines in window matching configured names or status keywords:_

- 2026-07-10 | deepseek | **AI contributor ledger name = "Deep Seek"** (confirmed by Gary 2026-07-10). When filing AI-agent [CONTRIBUTION EVENT]s for this opencode/DeepSeek assistant (model deepseek-v4-pro), ALWAYS use --contributors "Deep Seek" — it is the exact display name registered on the Contributors ledger (Edgar rejects mismatches, same rule as "Sophia Truesight" in OPERATING_INSTRUCTIONS §5b). Applies to ALL current and future Deep Seek sessions. Example filed this session: Próspera ZEDE Operating Agreement/By-Laws for TrueSight DAO LLC — Gary Teh 15min (25 TDG) + Deep Seek 94min via report_ai_agent_contribution, PR https://github.com/TrueSightDAO/agentic_ai_context/pull/650 (merged). Both HTTP 200, signature_verification success.
- 2026-07-10 | DeepSeek | Reorganized agentic_ai_context repository (168 files into 13 new + 6 existing folders). Generated 25 QR codes + inventory movements for São Jorge 81% chocolate bars to Kirsten. Fixed QR manifest schema + rebuilt qrs_index.json for serialized page. Fixed product image on checkout flow.
- 2026-07-14 | claude | White-label label spec was ROTATED 90°. Gary confirmed the physical label is 2" W x 4" H portrait (measured 267x520px = 1:1.95 in 81-dark-chocolate-bar-50g-packaging.jpg); the page asserted 4"x2" landscape in 7 places. Flipped in agroverse_shop_beta#183. NEEDS HUMAN APPROVAL: PROJECT_INDEX.md:75 still describes agroverse-designs as "(4″×2″ PNG)" — should read "(2″×4″ PNG)". Not edited directly per OPERATING_INSTRUCTIONS §3 (canonical file).
- 2026-07-15 | claude | White-label PR1 merged (agroverse_shop_beta#184): B1 (registration dead-ended into an empty card — phantom #wl-auth-loading write; #wl-auth-error moved out of the form it was trapped inside) and B2 (post-payment receipt destroyed ~200ms after render by a two-IIFE race) are fixed. Also B14: white-label/index.html never loaded cart.js, so universal-nav's injected cart-ui.js threw window.Cart.getItemCount() on every page load. Suite 34/34 green. STILL AWAITING EXPLICIT HUMAN APPROVAL (canonical files, §3): (1) PROJECT_INDEX.md:75 says agroverse-designs is "(4x2 PNG)" — should be "(2x4 portrait PNG, 600x1200)"; (2) WORKSPACE_CONTEXT.md:131 "Sticker Mule 4x2in custom rectangle label" needs a note that it is QR-code label stock, NOT the chocolate-bar label — reusing it as an artwork spec is the likely origin of the rotated spec fixed in beta#183.

_All dated lines on/after 2026-07-10_ (6):

- 2026-07-10 | deepseek | **AI contributor ledger name = "Deep Seek"** (confirmed by Gary 2026-07-10). When filing AI-agent [CONTRIBUTION EVENT]s for this opencode/DeepSeek assistant (model deepseek-v4-pro), ALWAYS use --contributors "Deep Seek" — it is the exact display name registered on the Contributors ledger (Edgar rejects mismatches, same rule as "Sophia Truesight" in OPERATING_INSTRUCTIONS §5b). Applies to ALL current and future Deep Seek sessions. Example filed this session: Próspera ZEDE Operating Agreement/By-Laws for TrueSight DAO LLC — Gary Teh 15min (25 TDG) + Deep Seek 94min via report_ai_agent_contribution, PR https://github.com/TrueSightDAO/agentic_ai_context/pull/650 (merged). Both HTTP 200, signature_verification success.
- 2026-07-10 | DeepSeek | Reorganized agentic_ai_context repository (168 files into 13 new + 6 existing folders). Generated 25 QR codes + inventory movements for São Jorge 81% chocolate bars to Kirsten. Fixed QR manifest schema + rebuilt qrs_index.json for serialized page. Fixed product image on checkout flow.
- 2026-07-14 | claude | White-label label spec was ROTATED 90°. Gary confirmed the physical label is 2" W x 4" H portrait (measured 267x520px = 1:1.95 in 81-dark-chocolate-bar-50g-packaging.jpg); the page asserted 4"x2" landscape in 7 places. Flipped in agroverse_shop_beta#183. NEEDS HUMAN APPROVAL: PROJECT_INDEX.md:75 still describes agroverse-designs as "(4″×2″ PNG)" — should read "(2″×4″ PNG)". Not edited directly per OPERATING_INSTRUCTIONS §3 (canonical file).
- 2026-07-14 | claude | Likely origin of the 4"x2" error: WORKSPACE_CONTEXT.md:131 cites a real ledger purchase, "Sticker Mule 4x2in custom rectangle label (per piece, order R384751187)" — that is almost certainly the QR-code label stock, not the chocolate-bar label. Suggest a clarifying note there so the next agent doesn't reuse it as an artwork spec. Needs human approval (canonical file).
- 2026-07-14 | claude | MISSING FILE: agroverse_shop/docs/WHITE_LABEL_SUPPLY_CHAIN_HANDOFF.md points to agentic_ai_context/AGROVERSE_WHITE_LABEL_SUPPLY_CHAIN.md, which does not exist on main or locally. The Liz pilot, routing, school pricing and shipping tiers it references are unrecorded — which is why the label spec had to be recovered by measuring pixels off a product JPEG. Someone should write it.
- 2026-07-15 | claude | White-label PR1 merged (agroverse_shop_beta#184): B1 (registration dead-ended into an empty card — phantom #wl-auth-loading write; #wl-auth-error moved out of the form it was trapped inside) and B2 (post-payment receipt destroyed ~200ms after render by a two-IIFE race) are fixed. Also B14: white-label/index.html never loaded cart.js, so universal-nav's injected cart-ui.js threw window.Cart.getItemCount() on every page load. Suite 34/34 green. STILL AWAITING EXPLICIT HUMAN APPROVAL (canonical files, §3): (1) PROJECT_INDEX.md:75 says agroverse-designs is "(4x2 PNG)" — should be "(2x4 portrait PNG, 600x1200)"; (2) WORKSPACE_CONTEXT.md:131 "Sticker Mule 4x2in custom rectangle label" needs a note that it is QR-code label stock, NOT the chocolate-bar label — reusing it as an artwork spec is the likely origin of the rotated spec fixed in beta#183.

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
90c9c38 | 2026-07-16 19:43:09 +0000 | chore(stats): refresh stats/current.json [skip ci]
d56e7ad | 2026-07-16 14:35:05 +0000 | chore(stats): refresh stats/current.json [skip ci]
043bb75 | 2026-07-16 08:56:14 +0000 | chore(stats): refresh stats/current.json [skip ci]
44701ae | 2026-07-16 03:48:56 +0000 | chore(stats): refresh stats/current.json [skip ci]
bab6a0b | 2026-07-15 19:46:58 +0000 | chore(stats): refresh stats/current.json [skip ci]
0e14a14 | 2026-07-15 14:22:56 +0000 | chore(stats): refresh stats/current.json [skip ci]
dc2e738 | 2026-07-15 08:56:20 +0000 | chore(stats): refresh stats/current.json [skip ci]
4e0414c | 2026-07-15 03:46:03 +0000 | chore(stats): refresh stats/current.json [skip ci]
48ee72a | 2026-07-14 19:52:24 +0000 | chore(stats): refresh stats/current.json [skip ci]
d4ce96f | 2026-07-14 14:25:50 +0000 | chore(stats): refresh stats/current.json [skip ci]
79787f5 | 2026-07-14 08:38:20 +0000 | chore(stats): refresh stats/current.json [skip ci]
dfc30b2 | 2026-07-14 03:45:34 +0000 | chore(stats): refresh stats/current.json [skip ci]
685d282 | 2026-07-13 20:00:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
888a471 | 2026-07-13 15:25:57 +0000 | chore(stats): refresh stats/current.json [skip ci]
4c95b1a | 2026-07-13 09:55:35 +0000 | chore(stats): refresh stats/current.json [skip ci]
ca74d67 | 2026-07-13 04:10:33 +0000 | chore(stats): refresh stats/current.json [skip ci]
44d10d5 | 2026-07-12 19:42:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
dfa1249 | 2026-07-12 14:12:37 +0000 | chore(stats): refresh stats/current.json [skip ci]
2c6eb84 | 2026-07-12 08:40:14 +0000 | chore(stats): refresh stats/current.json [skip ci]
8062c26 | 2026-07-11 23:59:35 -0700 | Fix 'each trip' to 'this upcoming trip' and add uncertainty framing (#281)
462cf47 | 2026-07-11 23:57:48 -0700 | Fix postscript to third person — Gary's warning in Sophia's voice (#280)
fc2f15a | 2026-07-11 23:52:51 -0700 | Expand postscript into full warning about Altamira and Ilhéus reality (#279)
485fb8e | 2026-07-11 23:48:53 -0700 | Add Ilhéus to postscript (#278)
55eeb1c | 2026-07-11 23:48:20 -0700 | Add postscript about Altamira reality (#277)
110c5c1 | 2026-07-11 21:49:10 -0700 | Drop The People Behind the Story section entirely (#276)
b87e4a1 | 2026-07-12 04:08:19 +0000 | chore(stats): refresh stats/current.json [skip ci]
c27eddb | 2026-07-11 17:03:13 -0700 | Strip job titles from People section — names and context only (#275)
818c4a0 | 2026-07-11 16:59:42 -0700 | Editorial v2: move lede, add epistemic markers, honest mistake, proof point, consent note (#274)
5535f15 | 2026-07-11 16:55:14 -0700 | Fix Jerry Luk title: VP -> Director of Engineering at Edmodo (#273)
ab652ff | 2026-07-11 16:40:34 -0700 | Remove duplicate Epilogue section causing rendering error (#272)
a752209 | 2026-07-11 16:33:20 -0700 | Apply Claude's editorial feedback: move People section after epilogue, fix Chinese chars, reconcile cacao origins (#271)
0cecf88 | 2026-07-11 15:58:20 -0700 | Add Jerry Luk to blog post: convinced Gary to join Edmodo, making getdata.io a side project (#269)
5d4cd1d | 2026-07-11 15:28:12 -0700 | Fix blog post format: convert from Jekyll markdown to static HTML (#268)
2c7f591 | 2026-07-11 18:25:07 -0400 | Add blog post: The Desert and the Diamond (#267)
9862364 | 2026-07-11 18:24:07 -0400 | Add header image for desert-and-diamond blog post
5c7af25 | 2026-07-11 19:45:02 +0000 | chore(stats): refresh stats/current.json [skip ci]
4ff8350 | 2026-07-11 14:03:10 +0000 | chore(stats): refresh stats/current.json [skip ci]
3d2dad3 | 2026-07-11 08:22:49 +0000 | chore(stats): refresh stats/current.json [skip ci]
739ab69 | 2026-07-11 03:54:43 +0000 | chore(stats): refresh stats/current.json [skip ci]
d6e332e | 2026-07-10 20:01:47 +0000 | chore(stats): refresh stats/current.json [skip ci]
… (truncated)
```

### `market_research` → `go_to_market`

```
_(no commits on origin/main in window)_
```

### `agentic_ai_context` → `agentic_ai_context`

```
3c7af1d | 2026-07-16 14:16:05 -0700 | Add live ledger URL to HTS schema PDF so partners can click through
962c9eb | 2026-07-16 14:15:14 -0700 | Update HTS schema PDF with complete product mapping and existing data
fe62004 | 2026-07-16 14:13:55 -0700 | Update HTS schema PDF with research links and existing HS data
16e2323 | 2026-07-16 14:12:11 -0700 | Add Currencies sheet HS/HTS codes schema PDF for partner sharing
73473cd | 2026-07-16 12:41:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-16 UTC)
c83fca0 | 2026-07-16 07:32:54 -0700 | chore(previews): refresh Beer Hall preview (2026-07-16 UTC)
994a646 | 2026-07-16 07:32:53 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-16 UTC)
be8a478 | 2026-07-16 01:40:46 -0700 | chore(previews): refresh Beer Hall preview (2026-07-16 UTC)
5d711f7 | 2026-07-16 01:40:45 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-16 UTC)
fafe122 | 2026-07-15 20:47:16 -0700 | chore(previews): refresh Beer Hall preview (2026-07-16 UTC)
b81d2cb | 2026-07-15 20:47:14 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-16 UTC)
948aadf | 2026-07-15 12:45:36 -0700 | chore(previews): refresh Beer Hall preview (2026-07-15 UTC)
7921720 | 2026-07-15 12:45:34 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-15 UTC)
5f183fa | 2026-07-15 12:15:53 -0700 | docs: Sophia Nelanco migration, Claude Cloud box, white-label changelog (#671)
979d0c3 | 2026-07-15 11:48:38 -0700 | handoffs: mark large_spikes plan as SUPERSEDED (already implemented) (#670)
bae6f0d | 2026-07-15 11:38:08 -0700 | CONTEXT_UPDATES: flag stale handoff protocol in OPERATING_INSTRUCTIONS §11 (#669)
6fbdad3 | 2026-07-15 07:57:37 -0700 | Add handoff PDF: Gary to Fatima (Brazil ops, Jul 2026)
0e1cad9 | 2026-07-15 07:20:12 -0700 | chore(previews): refresh Beer Hall preview (2026-07-15 UTC)
172d58e | 2026-07-15 07:20:10 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-15 UTC)
d5a1f20 | 2026-07-15 05:06:40 -0700 | handoffs: register white-label Phase 2 -> nelanco-claude box (#668)
7584532 | 2026-07-15 04:52:16 -0700 | plans: white-label PR1 done — funnel works end-to-end; resume moves to PR2 (#667)
3684ae4 | 2026-07-15 04:37:43 -0700 | docs(infra): Sophia migrated Explorya->Nelanco (2026-07-15) + new Claude box (#666)
937b23d | 2026-07-15 04:33:07 -0700 | plans: D0 done — label spec flipped to portrait 2"x4" (#665)
c8c72a0 | 2026-07-15 01:42:24 -0700 | chore(previews): refresh Beer Hall preview (2026-07-15 UTC)
74eeea7 | 2026-07-15 01:42:22 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-15 UTC)
ccc959a | 2026-07-14 20:45:05 -0700 | chore(previews): refresh Beer Hall preview (2026-07-15 UTC)
8ab0af0 | 2026-07-14 20:45:04 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-15 UTC)
372de3b | 2026-07-14 19:37:11 -0700 | Merge pull request #664 from TrueSightDAO/auto/advisory-refresh-2026-07-15
c3872a6 | 2026-07-15 02:37:00 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-15 UTC)
38fadb7 | 2026-07-14 19:08:47 -0700 | plans: white-label D0 — the label spec is rotated 90 degrees (#663)
7a62c02 | 2026-07-14 18:29:59 -0700 | plans: white-label Phase 2 — state repair + visual placement spec (#662)
c2de69b | 2026-07-14 18:17:00 -0700 | plans: Nelanco box Gate C done + add Sophia->Nelanco migration roadmap (#661)
dba7187 | 2026-07-14 14:18:29 -0700 | chore(plan): Gate B done — Nelanco Claude Code box provisioned (#660)
7b1a878 | 2026-07-14 13:55:26 -0700 | chore(plan): tick PR1, advance RESUME to PR2 (Nelanco Claude Code box) (#659)
2df0616 | 2026-07-14 13:41:00 -0700 | plan: correct Nelanco box scope — interactive Claude Code + SSH parity, not a 2nd Sophia (#658)
f5ee11e | 2026-07-14 13:19:45 -0700 | plan: Nelanco Claude Code box (2nd Sophia + mobile remote-control) (#657)
0c4e7b5 | 2026-07-14 12:51:30 -0700 | chore(previews): refresh Beer Hall preview (2026-07-14 UTC)
1996524 | 2026-07-14 12:51:29 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-07-14 UTC)
e6852a7 | 2026-07-14 12:21:46 -0700 | plan: subscription renewal sheet sync (implemented 2026-07-13)
9c37fef | 2026-07-14 07:24:39 -0700 | chore(previews): refresh Beer Hall preview (2026-07-14 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
e111714 | 2026-07-15 11:47:00 -0700 | fix(tokenomics): remove all Wix dependencies from tdg_wix_dashboard.js (#380)
a278954 | 2026-07-14 12:21:08 -0700 | docs: add subscription renewal columns R/S/T to SCHEMA
c224d36 | 2026-07-10 13:23:27 -0700 | docs: redefine Telegram Chat Logs col R as Processor Dedup Marker
3b4403c | 2026-07-10 16:12:54 -0400 | fix(dao-members-cache): probe first contributor WITH a public key (#379)
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
48c1f0b | 2026-07-16 08:36:51 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8ee569b | 2026-07-15 08:37:32 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
81e1bfc | 2026-07-14 14:30:52 -0700 | inventory: refresh cache counters
f29ce99 | 2026-07-14 14:28:37 -0700 | chore: refresh Agroverse store inventory snapshot
35917f2 | 2026-07-14 13:28:41 -0700 | chore: refresh Agroverse store inventory snapshot
fd0852e | 2026-07-14 08:29:51 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
6c2b915 | 2026-07-13 09:59:56 +0000 | chore: refresh partners-velocity snapshot [skip ci]
222ac87 | 2026-07-13 09:49:27 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
12d2d2b | 2026-07-12 08:33:15 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
695df5d | 2026-07-11 08:16:21 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
e569571 | 2026-07-10 16:13:10 -0400 | fix(repackaging-ingest): wire settlement handler to real event tag + add audit tab (#17)
3d3590e | 2026-07-10 12:38:00 -0700 | fix: restore São Jorge repackaging composition JSON (accidentally removed in prior sync)
6fc3df4 | 2026-07-10 12:37:38 -0700 | chore: sync store-inventory (São Jorge 81% bar 25 in stock)
79e0c23 | 2026-07-10 15:29:07 -0400 | chore: refresh Agroverse store inventory snapshot
821b4ab | 2026-07-10 14:53:30 -0400 | chore(inventory): repackaging composition e963c8ff-4520-4b52-a5c7-3abfaae963fb
29a886c | 2026-07-10 14:53:20 -0400 | chore(inventory): refresh currencies.json (repackaging ingest)
6d54628 | 2026-07-10 09:55:00 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
a2e9ca6 | 2026-07-17 05:24:44 +0800 | Add Coopercabruca membership to Oscar's farm page (#191)
5798a7b | 2026-07-16 14:10:31 -0700 | fix(white-label): PR5 — State E/F order emphasis + real success receipt (#189)
166cf42 | 2026-07-16 14:08:40 -0700 | fix(white-label): PR4 — State C/D gallery + upload (P4, B7, B9, Q5, P7-partial) (#188)
ecb4e42 | 2026-07-16 13:58:19 -0700 | fix(white-label): registration/verification never worked -- dao-client field-name bug (#190)
7604237 | 2026-07-15 12:24:11 -0700 | fix(white-label): PR3 — State A re-composition (P1, P2, B10, B12, B13) (#187)
5cdd1b7 | 2026-07-15 12:11:03 -0700 | fix(pages): point CNAME at beta.agroverse.shop, not the apex domain (#186)
b939f0a | 2026-07-15 12:08:08 -0700 | fix(white-label): PR2 — re-quote shipping on qty change, timestamp uploads, surface shipping errors (B3+B4+B5) (#185)
4fc77ac | 2026-07-15 04:48:21 -0700 | fix(white-label): PR1 — repair registration (B1) and the post-payment receipt (B2) (#184)
9e03bc8 | 2026-07-15 04:31:03 -0700 | fix(white-label): D0 — flip the label spec to portrait 2"x4" (#183)
89e7622 | 2026-07-14 19:05:28 -0700 | feat(white-label): correct label to portrait 2"×4" + commit the full implementation (#182)
285ef34 | 2026-07-14 12:21:01 -0700 | feat: sync subscription renewal payments (invoice.paid) to Stripe Checkout sheet
4871cd1 | 2026-07-10 13:55:18 -0700 | fix: split video/photo grids on São Jorge farm page, restore original photo markup
e25b4ac | 2026-07-10 16:33:28 -0400 | Add São Jorge farm video embeds + Bean to Bliss ep 12 + swamp-walk blog posts (#181)
e82943e | 2026-07-10 12:52:45 -0700 | Add São Jorge (Coopercabruca) 81% dark chocolate bar SKU (#180)
```

### `iching_oracle` → `oracle`

```
_(no commits on origin/main in window)_
```

### `Cypher-Defense` → `Cypher-Defense`

```
47a3bb5 | 2026-07-15 04:33:04 -0700 | fix(backup): retarget weekly autopilot AMI backup to the Nelanco box (#41)
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-07-17T024754Z_white-label-fixes-hts-schema-pdf.md`

- **posted_at_utc:** `2026-07-17T02:47:54Z`  
- **slug:** `white-label-fixes-hts-schema-pdf`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Engineering (Shop)** — Shipped white-label PR4 (gallery/upload) and PR5 (success receipt); fixed a critical dao-client field-name bug blocking registration/verification.

### `beer-hall_2026-07-15T023656Z_white-label-fixes-subscription-sync.md`

- **posted_at_utc:** `2026-07-15T02:36:56Z`  
- **slug:** `white-label-fixes-subscription-sync`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Engineering (Shop)** — Committed full implementation for white-label label orientation (corrected to portrait 2"×4").

### `beer-hall_2026-07-14T023918Z_operating-agreement-signed-shop-updates.md`

- **posted_at_utc:** `2026-07-14T02:39:18Z`  
- **slug:** `operating-agreement-signed-shop-updates`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Ops (Legal)** — Finalized and uploaded the clean v1.0 Operating Agreement PDF, ready for signature.

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
