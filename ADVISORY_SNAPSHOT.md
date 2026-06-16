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

- Generated (UTC): `2026-06-16T04:26:18Z`
- Look-back: **7** calendar days (`2026-06-09` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | $3,388 | 8% | `2026-12-31` | 198 | **behind** |
| USA Agroverse Partners | 100 | — | — | `2026-12-31` | 198 | — |

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-06-15T10:59:14.270Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **670**
- Partnered (north-star): **14**

## Funnel by status (curated order)

- Reclassified — D2C only: 1  (#1)
- AI: Contact Form found: 118  (#3)
- Research: 59  (#8)
- AI: No fit signal: 158  (#9)
- AI: Enrich — manual: 94  (#10)
- Manager Follow-up: 32  (#13)
- Followed Up: 1  (#15)
- Instagram Followed: 11  (#18)
- Rejected: 14  (#19)
- On Hold: 18  (#20)
- Deferred / Revisit later: 7  (#21)
- **Partnered: 14**  (#22)
- AI: Warm up prospect: 69  (#9999)
- Not Appropriate: 74  (#9999)
- Reclassified — D2C only: 0  (#9999)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **251**, follow_up **70**, bulk **0**, unknown **2** (data rows: **323**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **69** stores — sum logged **warmup** sends (AU): **204**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **3** / **0** / **66**; follow-up depth (none / once / ≥2): **69** / **0** / **0**
- **Manager Follow-up**: **32** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **66**; warmup depth (none / once / ≥2): **29** / **1** / **2**; follow-up depth (none / once / ≥2): **10** / **5** / **17**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: _(no rows in this status)_
- **Follow-up pipeline (combined)**: **32** stores — sum logged **warmup** sends (AU): **7**, sum logged **follow-up** sends (AV): **66**; warmup depth (none / once / ≥2): **29** / **1** / **2**; follow-up depth (none / once / ≥2): **10** / **5** / **17**

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
- Manager record: `Kirsten Ritschel` · 16 SKU lines · 1,421 total units · $1,527.39

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | Packaging Material | Bulk | 4 | 895 | $652.10 |
  | (uncategorized) | (unspecified) | 8 | 458 | $769.54 |
  | Cacao Mass | Bulk | 1 | 50 | $1.55 |
  | Cacao Mass | Retail Ready | 3 | 18 | $104.20 |

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
- Manager record: `Gary Teh` · 31 SKU lines · 13,833.15 total units · $12,280.95

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 27 | 13,745.97 | $12,143.62 |
  | Packaging Material | Bulk | 1 | 74 | $49.98 |
  | Cacao Mass | Retail Ready | 2 | 11 | $87.34 |
  | Cacao Tea | Bulk | 1 | 2.18 | $0.00 |

### Other managers (top 8 by USD value)

| Manager | Items | Units | Value (USD) |
|---------|-------|-------|-------------|
| TrueSight DAO | 1 | 9,036.35 | $9,036.35 |
| Sacred Earth Farms | 3 | 316 | $2,241.33 |
| Val Lapidus | 11 | 1,270 | $1,475.95 |
| Coopercabruca | 1 | 1,706 | $1,199.87 |
| Aga Marecka | 1 | 20 | $537.46 |
| Andrea Catalina Falcon Rios De Pabst | 3 | 223 | $328.62 |
| Shuar Design Boutique | 3 | 37 | $284.34 |
| Go Ask Alice - Niccolina Ammerman | 2 | 14 | $115.81 |

_(+27 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-06-09 | claude (subscriptions session) | GTIN MODEL (canonical, confirmed by Gary): the retail GTIN identifies the PRODUCT TYPE, not the unit/vintage — ALL chocolate bars share one chocolate-bar GTIN; ALL ceremonial cacao share one cacao GTIN. The serialized QR code (Agroverse QR codes tab, column A) is the per-unit identity that differentiates farm+vintage and resolves provenance. A vintage-independent "generic" SKU REUSES the existing shared GTIN (never mint a new GTIN per vintage); per-vintage agroverse.shop product pages are presentation sub-views of one GTIN (expect Merchant Center duplicate-GTIN across them). Provenance is always via QR, never GTIN. Documented in AGROVERSE_QR_CODE_BATCH_GENERATION.md §0 + NOTES_tokenomics.md (Agroverse QR codes tab) + CHOCOLATE_SUBSCRIPTION_PLAN.md (Decisions → GTIN model).
- 2026-06-09 | claude (subscriptions session) | CREDENTIAL HAND-OFF PROTOCOL (new canonical doc CREDENTIAL_HANDOFF_PROTOCOL.md): to get a secret onto a locked-down box an LLM can't SSH (SG blocks 22; box trusts only its own keypair, which lives on the autopilot box), the autopilot box (`sophia`) is the staging hub and Sophia propagates. Rules: never put secrets in chat/Telegram/PRs/commits; move via stdin (mask to prefix+len); chmod 600; stage under /home/ubuntu/ NOT /opt/truesight_autopilot (deploy.sh git-cleans it); prefer sourcing an existing secret (e.g. Stripe test key in sentiment_importer config/environments/development.rb). Then hand off in the Sophia thread (LLM can't post into an existing TG topic — operator drops the line; adapter auto-loads the plan). Pointer added to SOPHIA_HANDOFFS.md. Worked example: beta sandbox Stripe test key staged at ~/stripe_test_key → thread 1955.

_All dated lines on/after 2026-06-09_ (7):

- 2026-06-10 | claude-code | UAT (User Acceptance Testing) — end-to-end validation by the governor before signing off on a feature. The beta sandbox endpoint (thread 1955, `beta.edgar.truesight.me`) is the canonical UAT surface for Stripe-touching flows: standalone EC2 in NELANCO, Stripe TEST mode, isolated fulfillment queue. UAT is distinct from CI/E2E tests — it's the human governor running through the real user journey. Future LLMs and Sophia: when a plan says "UAT," it means the governor (Gary) tests end-to-end on the beta staging environment, not in CI.
- 2026-06-09 | claude (subscriptions session) | GTIN MODEL (canonical, confirmed by Gary): the retail GTIN identifies the PRODUCT TYPE, not the unit/vintage — ALL chocolate bars share one chocolate-bar GTIN; ALL ceremonial cacao share one cacao GTIN. The serialized QR code (Agroverse QR codes tab, column A) is the per-unit identity that differentiates farm+vintage and resolves provenance. A vintage-independent "generic" SKU REUSES the existing shared GTIN (never mint a new GTIN per vintage); per-vintage agroverse.shop product pages are presentation sub-views of one GTIN (expect Merchant Center duplicate-GTIN across them). Provenance is always via QR, never GTIN. Documented in AGROVERSE_QR_CODE_BATCH_GENERATION.md §0 + NOTES_tokenomics.md (Agroverse QR codes tab) + CHOCOLATE_SUBSCRIPTION_PLAN.md (Decisions → GTIN model).
- 2026-06-09 | claude (subscriptions session) | CREDENTIAL HAND-OFF PROTOCOL (new canonical doc CREDENTIAL_HANDOFF_PROTOCOL.md): to get a secret onto a locked-down box an LLM can't SSH (SG blocks 22; box trusts only its own keypair, which lives on the autopilot box), the autopilot box (`sophia`) is the staging hub and Sophia propagates. Rules: never put secrets in chat/Telegram/PRs/commits; move via stdin (mask to prefix+len); chmod 600; stage under /home/ubuntu/ NOT /opt/truesight_autopilot (deploy.sh git-cleans it); prefer sourcing an existing secret (e.g. Stripe test key in sentiment_importer config/environments/development.rb). Then hand off in the Sophia thread (LLM can't post into an existing TG topic — operator drops the line; adapter auto-loads the plan). Pointer added to SOPHIA_HANDOFFS.md. Worked example: beta sandbox Stripe test key staged at ~/stripe_test_key → thread 1955.
- 2026-06-10 | claude (subscriptions session) | TERM: UAT = User Acceptance Testing — a human walks the real end-to-end flow before go-live (NOT more automated tests). Convention: UAT runs on the BETA staging stack (beta.agroverse.shop + beta.edgar.truesight.me beta dao_protocol in Stripe TEST mode, SANDBOX rows), never prod, with Stripe test cards (4242…) — checkout must show TEST MODE. Prefer beta staging over local for UAT (that's what the beta sandbox is for). New doc GLOSSARY.md. Active: chocolate-bar subscription UAT = thread 1955. Live as of 2026-06-10: beta.agroverse.shop/subscribe/chocolate-bar/=200, beta.edgar webhook=400-on-unsigned (verifying).
- 2026-06-14 | claude (sophia prod-incident session) | Sophia prod stall cascade on the Kopi Bay onboarding thread (tg 3926) — root-caused + fixed 3 distinct bugs (all deployed to box 958e8cc). (1) truesight_autopilot#195: submit_contribution crashed when DeepSeek double-encoded `attributes` as a JSON string → AttributeError in _normalize_submission_labels → turn died mid tool-loop, orphan tool_call, silent stall. (2) #200: _externalize_tool_result (CM1, from #193/#194) returned non-str tool results raw — recall_context/search_code/sheet tools return dicts → `result_text[:300]` raised `TypeError: unhashable type: 'slice'` → streaming turn crashed → adapter showed "incomplete chunked read". HEADS-UP to whoever owns the CM work: #200 patched _externalize_tool_result in your subsystem (coerce non-str → json.dumps before the length check) — don't re-fix/revert. (3) #201: deploy_autopilot had no already-on-latest check → always reset --hard + restarted, severing in-flight turns → adapter resubmits → REDEPLOY LOOP (hit the vault commit-hash thread 3981); added a phase-one hash precheck returning status=noop when HEAD==origin/main.
- 2026-06-14 | claude (sophia prod-incident session) | OPEN BUG (diagnosed, NOT yet fixed) — vault panel sophia.truesight.me/vault/ shows "Active tracks: 0" during live chat. Two disconnected active-turn registries: main._active_streams (in-memory; what deploy_autopilot idle-drain reads) vs deploy_watcher active_tracks.json (file; what the vault panel get_system_status + can_deploy read). register_track/unregister_track are called ONLY by aws_monitor.py + email_poller.py — the chat path (main.py) never registers a track. Consequence: panel under-reports live conversations AND its Deploy button (can_deploy) would greenlight a deploy while turns run. Fix options: (a) chat loop calls deploy_watcher.register_track/unregister around each turn, or (b) get_system_status/can_deploy also union main._active_streams. Likely belongs with the thread-3981 vault-panel feature work.
- 2026-06-14 | claude (sophia prod-incident session) | RESOLVED the Active-tracks bug above via truesight_autopilot#203 (deployed, box 969f170): chose option (a) — the chat turn lifecycle now register_track/unregister_track into deploy_watcher's file registry (track_type "telegram_chat", which already existed unused). Option (b) was wrong: the vault panel runs in the standalone vault_app process (port 8002) and can't see main._active_streams — the FILE registry is the cross-process bridge. Verified live: a thread-3966 turn appeared as a telegram_chat track and cleared on completion. This also makes can_deploy block deploys during live turns (a second guard alongside #201). All four incident PRs (#195/#200/#201/#203) merged + deployed.

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
2bf3d30 | 2026-06-15 20:19:40 -0700 | Center Sophia avatar image in blog post (#240)
da253ef | 2026-06-15 18:10:30 -0700 | Add link to Self-Replication SOP in blog post (#239)
9732e85 | 2026-06-15 21:34:48 +0000 | chore(stats): refresh stats/current.json [skip ci]
f28f13d | 2026-06-15 11:26:02 -0700 | Add all 46 blog posts to index (restore missing older entries) (#238)
ac11f45 | 2026-06-15 12:51:05 +0000 | chore(stats): refresh stats/current.json [skip ci]
0ed1f14 | 2026-06-15 05:41:30 +0000 | chore(stats): refresh stats/current.json [skip ci]
ddee7f4 | 2026-06-14 20:08:52 +0000 | chore(stats): refresh stats/current.json [skip ci]
208d4a2 | 2026-06-14 13:00:59 -0700 | [autopilot] Fix index.html (#237)
638172d | 2026-06-14 12:56:39 -0700 | [autopilot] Re-order the landing page (index.html) sections to follow a  (#236)
5c00607 | 2026-06-14 14:56:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
ebef91d | 2026-06-14 10:05:19 +0000 | chore(stats): refresh stats/current.json [skip ci]
6a1a97e | 2026-06-13 23:59:07 -0700 | Add RLHF/weights leakage nuance to context separation (#234)
bbfeb4d | 2026-06-13 23:57:43 -0700 | Add civil law vs common law epistemological framing (#233)
f833765 | 2026-06-13 23:57:23 -0700 | Add weights lineage, stare decisis, and practical challenges nuance (#232)
c53cd52 | 2026-06-13 23:21:39 -0700 | Restructure post flow and add Christensen disruptive innovation section (#231)
9d73221 | 2026-06-13 22:41:18 -0700 | fix: steps grid to 2x2 layout with min-width:0 guard (#230)
391a48d | 2026-06-13 22:39:34 -0700 | fix: card-grid 2+1 layout — restrict media-top a to first-child, add min-width:0 (#229)
e254eb0 | 2026-06-13 22:33:57 -0700 | [autopilot] Fix index.html (#228)
a366168 | 2026-06-14 05:26:40 +0000 | trigger: rebuild GitHub Pages
0f904f3 | 2026-06-14 05:17:57 +0000 | chore(stats): refresh stats/current.json [skip ci]
6df8a34 | 2026-06-14 00:33:50 +0000 | Fix Chat with Sophia link: beerhall → sophia.truesight.me
e72d4bf | 2026-06-14 00:33:09 +0000 | Reorder Platform Services: Sophia → Edgar → Perch
5a18f58 | 2026-06-13 17:23:52 -0700 | Add Platform Services section with Perch and Sophia (#227)
c622d33 | 2026-06-13 20:05:32 +0000 | chore(stats): refresh stats/current.json [skip ci]
995531e | 2026-06-13 11:12:55 -0700 | Add Anatman section: LLM behavior mirrors no-self doctrine (#226)
b0e3afa | 2026-06-13 11:07:03 -0700 | Add hyperscaler monetization collapse argument (#224)
76a2f0a | 2026-06-13 11:07:00 -0700 | Correct model reference: Sophia runs on DeepSeek, not Claude/GPT (#225)
10eb75b | 2026-06-13 10:49:55 -0700 | Add Taoist reversal closing section with data sovereignty (#223)
82fd794 | 2026-06-13 10:33:45 -0700 | Add self-hosted LLM sovereignty section and Sophia profile image (#221)
280ccbb | 2026-06-13 10:20:56 -0700 | Add LKY self-imposed constraint parallel to blog post (#220)
e45cd9b | 2026-06-13 10:19:11 -0700 | Add new post to blog index with LKY image (#219)
8103bfb | 2026-06-13 10:19:06 -0700 | New post: Agentic AI and the Common Law Tradition (with LKY image) (#218)
bd0bb81 | 2026-06-13 10:19:00 -0700 | Add Lee Kuan Yew public domain photo for blog post
96ea59c | 2026-06-13 14:39:57 +0000 | chore(stats): refresh stats/current.json [skip ci]
3f1820d | 2026-06-13 09:43:57 +0000 | chore(stats): refresh stats/current.json [skip ci]
204e271 | 2026-06-13 05:07:43 +0000 | chore(stats): refresh stats/current.json [skip ci]
0a6b4aa | 2026-06-12 21:54:13 -0700 | Add detail about people coming back for seconds of cacao (#213)
8ab6d9c | 2026-06-12 21:43:59 -0700 | Add Alina, students, and group hug ending to blog post (#212)
a53ccf0 | 2026-06-12 21:40:49 -0700 | Add Sophia's name, voice, and profile photo story to blog post (#211)
25cdc00 | 2026-06-12 20:46:32 -0700 | Add Gary's honest reflection — felt like building a toy watching Microsoft demo (#210)
… (truncated)
```

### `market_research` → `go_to_market`

```
_(no commits on origin/main in window)_
```

### `agentic_ai_context` → `agentic_ai_context`

```
e48dabe | 2026-06-15 18:02:41 -0700 | Add Self-Replication SOP as PDF
602e508 | 2026-06-15 17:57:13 -0700 | Merge Clone/Fork SOP: add Fork path for new ecosystems (#519)
79c08e5 | 2026-06-15 17:56:44 -0700 | Add SOP for spawning a new autopilot instance (#517)
b99699b | 2026-06-15 14:32:03 -0700 | chore(previews): refresh Beer Hall preview (2026-06-15 UTC)
f5dafad | 2026-06-15 14:32:02 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-15 UTC)
2a997fb | 2026-06-15 11:06:46 -0700 | Fix V2: sentiment importer already has subscribers + subscription revenue flowing to NAV (#516)
e83c167 | 2026-06-15 09:22:11 -0700 | Fix V2: remove unnecessary lockup guardrail, clarify licensing surplus boosts NAV directly (#515)
58bc9ae | 2026-06-15 09:08:38 -0700 | Add V2 PDF: full capital channels map
c2857b1 | 2026-06-15 09:08:04 -0700 | Add V2: full capital channels map, ecosystem diagram, revenue model
f04aaff | 2026-06-15 09:04:06 -0700 | Fix V1 doc: strip capital channels, keep lean. Add licensing revenue suggestion. (#514)
d8972a1 | 2026-06-15 05:49:15 -0700 | chore(previews): refresh Beer Hall preview (2026-06-15 UTC)
07b6acc | 2026-06-15 05:49:14 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-15 UTC)
43d0bfd | 2026-06-14 23:25:16 -0700 | Split into lean SVH doc + internal strategy memo. Fix carbon credits, AGL securities question, capital-injected TDG. (#513)
2a4ac89 | 2026-06-14 23:12:27 -0700 | Add ecosystem mermaid diagram, revenue distribution model, fix names (Bilal/Liz) (#512)
5a1324d | 2026-06-14 22:58:07 -0700 | Add capital channels map: how partners inject resources, what they get, how they exit (#511)
c8b9041 | 2026-06-14 22:36:56 -0700 | chore(previews): refresh Beer Hall preview (2026-06-15 UTC)
d4f1402 | 2026-06-14 22:36:55 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-15 UTC)
836e259 | 2026-06-14 21:29:43 -0700 | Merge pull request #510 from TrueSightDAO/auto/advisory-refresh-2026-06-15
28d935d | 2026-06-15 04:29:34 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-15 UTC)
f4a4f08 | 2026-06-14 20:14:03 -0700 | Fix Howey question (include buyback) and impact fund contradiction (#509)
07e70b3 | 2026-06-14 19:54:15 -0700 | Fix Wise cost: $0 to open, no minimum deposit. Not $500. (#508)
124a806 | 2026-06-14 19:51:23 -0700 | Strip further: UNA doesn't need its own bank account, TrueTech Inc handles all money flows (#507)
5180376 | 2026-06-14 19:48:48 -0700 | Strip to lean version: one-page proposal, one SVH question, $50 UNA path (#506)
bc2ab0e | 2026-06-14 19:43:14 -0700 | Final revisions: withdrawal methods clarified, reserve formula on truesight.me, SVH approach reset, Howey question (#505)
ec2b1c8 | 2026-06-14 19:41:35 -0700 | Major revision: CTA moot, DUNA conversion corrected, TrueTech Inc independent entity, buyback reserve clarified (#504)
d93f469 | 2026-06-14 17:11:41 -0700 | Fix buyback automation: budget and price are already fully automated (#503)
655c170 | 2026-06-14 17:08:18 -0700 | Fix transparency row: Wise API automates payout, not manual (#502)
a0bfae3 | 2026-06-14 17:03:37 -0700 | Update buyback section: Withdrawal Method dropdown, not cash receipt channel (#501)
2c4476c | 2026-06-14 17:02:35 -0700 | Update buyback section: DApp withdraw page, not Raydium (#500)
d40fd13 | 2026-06-14 16:58:48 -0700 | Update PDF with parallel Wise accounts + buyback infra
59bee80 | 2026-06-14 16:57:51 -0700 | Add parallel Wise accounts timeline + existing buyback infra documentation (#499)
0e16a5c | 2026-06-14 16:42:21 -0700 | Final structure: TrueTech Inc as facility, TDG buyback→burn, impact fund pathways (#498)
93f5599 | 2026-06-14 15:21:17 -0700 | Update PDF with service provider links (OtoCo, Wise)
55d3542 | 2026-06-14 15:20:51 -0700 | v7: Add service provider links (OtoCo, Wise) (#496)
6e5622c | 2026-06-14 15:08:58 -0700 | v6: CTA clarification — only Gary reports as beneficial owner (#495)
0d0b1fd | 2026-06-14 14:44:11 -0700 | Legal Entity Structuring Proposal v5 — Corrected Treasury, DUNA-Owned CNPJ (#494)
9003547 | 2026-06-14 14:26:38 -0700 | Legal Entity Structuring Proposal v4 — UNA Bank Account, No TrueTech Inc Custodian (#493)
ca393bb | 2026-06-14 13:29:31 -0700 | context: Active-tracks vault bug resolved (truesight_autopilot#203)
2f03fb3 | 2026-06-14 13:06:27 -0700 | chore(previews): refresh Beer Hall preview (2026-06-14 UTC)
3bfd4fa | 2026-06-14 13:06:27 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-14 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
15298bf | 2026-06-14 14:59:28 -0700 | fix: align [PARTNER ADD EVENT] handler with existing DAO Partners column format (#349)
74cc56e | 2026-06-14 14:49:04 -0700 | fix: add process_partner_add_telegram_logs.gs to find_nearby_stores manifest (#348)
dae9818 | 2026-06-14 14:48:40 -0700 | feat: add processPartnerAddsFromTelegramChatLogs GAS handler (#347)
f45cf14 | 2026-06-13 16:49:05 -0700 | fix(qr-batch): retry the column-M stamp verification (kill false re-sends) (#346)
1f17941 | 2026-06-11 16:38:11 -0700 | Fix target-path quoting in workflow (#345)
289ca71 | 2026-06-11 23:32:48 +0000 | Use default GITHUB_TOKEN, commit PNGs to tokenomics/generated_qr_codes
617894e | 2026-06-11 23:27:28 +0000 | Use base64-encoded token from webhook payload for lineage-assets upload
80d2311 | 2026-06-11 23:25:56 +0000 | Revert to using secrets.QR_CODE_REPOSITORY_TOKEN for lineage-assets
c306c4d | 2026-06-11 23:21:09 +0000 | Use github_token from webhook payload instead of repo secret
d120a8a | 2026-06-11 23:19:30 +0000 | Fix: pass target_path through handle_webhook_request properly
d601430 | 2026-06-11 23:17:29 +0000 | Switch QR PNG upload target from qr_codes to lineage-assets/pngs
e328c6f | 2026-06-11 23:06:52 +0000 | Fix: use product_name from client_payload (GitHub 10-property limit)
72bfd55 | 2026-06-11 16:05:39 -0700 | Update QR webhook workflow to use client_payload data instead of reading sheet (#344)
25e568d | 2026-06-11 16:05:33 -0700 | [autopilot] Fix github_webhook_handler.py to use production sheet and qr (#343)
f7a52ac | 2026-06-10 18:19:56 -0700 | Sync Code.js from agroverse_shop_beta PR #141
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
b04a540 | 2026-06-11 16:14:09 -0700 | Add QR code for Ceremonial Cacao: E2E_TEST_002 [skip ci]
3411548 | 2026-06-11 16:13:31 -0700 | cleanup test file
2a7e7c4 | 2026-06-11 16:13:25 -0700 | test write after unarchive
```

### `proposals` → `proposals`

```
_(no commits on origin/main in window)_
```

### `agroverse-inventory` → `agroverse-inventory`

```
b476a9f | 2026-06-15 12:54:19 +0000 | chore: refresh partners-velocity snapshot [skip ci]
9fd9e3b | 2026-06-15 12:44:32 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
14867ca | 2026-06-14 09:58:00 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
c90a0d4 | 2026-06-13 17:28:35 -0700 | chore: refresh Agroverse store inventory snapshot
912e060 | 2026-06-13 13:28:38 -0700 | chore: refresh Agroverse store inventory snapshot
75c15d2 | 2026-06-13 09:36:17 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
706b159 | 2026-06-12 10:41:39 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8cba6bb | 2026-06-11 10:59:43 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
a68906a | 2026-06-10 10:35:20 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
5ce8b7a | 2026-06-09 10:04:56 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
3ea8d84 | 2026-06-14 17:07:07 -0700 | Swap Kopi Bar hero to interior photo, demote exterior to gallery (#177)
eaa7c15 | 2026-06-14 17:02:32 -0700 | Add Kopi Bar interior hero image
8061d48 | 2026-06-14 16:18:41 -0700 | Replace Kopi Bar logo with storefront signage photo
c46760a | 2026-06-14 16:17:59 -0700 | [autopilot] Fix cacao-journeys/pacific-west-coast-path/index.html (#176)
2b9fa7c | 2026-06-14 16:13:23 -0700 | [autopilot] Fix cacao-journeys/pacific-west-coast-path/index.html (#175)
064466d | 2026-06-14 16:06:26 -0700 | [autopilot] Update the Kopi Bar & Bakery partner detail page (partners/k (#174)
80720a6 | 2026-06-14 16:05:35 -0700 | Add Kopi Bar tasting session photo
cd70374 | 2026-06-14 16:05:34 -0700 | Add BAMPFA entrance with free entry sign
e32e588 | 2026-06-14 16:05:33 -0700 | Add Kopi Bar signage with hours
eeeb501 | 2026-06-14 16:05:32 -0700 | Add Kopi Bar exterior photo
0ed8e49 | 2026-06-14 16:05:31 -0700 | Add Nora holding cacao bag photo
36c8ddb | 2026-06-14 15:56:23 -0700 | [autopilot] Fix three issues on the Agroverse shop beta site:
e20cd08 | 2026-06-14 15:54:04 -0700 | Add Kopi Bar & Bakery logo
6ba8abb | 2026-06-14 15:09:18 -0700 | Add Kopi Bar & Bakery to wholesale stockist list and partners index (#170)
a9157a3 | 2026-06-14 15:09:14 -0700 | Onboard Kopi Bar & Bakery (Kopi Bay) as wholesale partner (#169)
30e9f9e | 2026-06-11 14:32:39 -0700 | Add subscription CTA to Friends of the Rainforest page to offset event CAC (#167)
fc17fad | 2026-06-11 14:29:40 -0700 | Use shipment-style QR-linked email signup on Friends of the Rainforest page (#166)
67e51df | 2026-06-11 14:18:08 -0700 | Rebuild Friends of the Rainforest page with rich farm content, videos, maps, and product cards (#165)
aead514 | 2026-06-11 14:11:34 -0700 | Add Friends of the Rainforest landing page for event sampling QR code (#164)
c896c25 | 2026-06-11 13:39:20 -0700 | Remove Buy One Bar button from generic PDP (#163)
51949fb | 2026-06-11 13:36:53 -0700 | Restructure generic PDP: hero two-column, content full-width below (#162)
394808d | 2026-06-11 13:33:23 -0700 | Revert generic PDP to two-column layout (#161)
4112de7 | 2026-06-11 13:30:14 -0700 | Switch generic PDP to full-width single-column layout (#160)
0b4cea3 | 2026-06-11 13:29:19 -0700 | Add playful tagline to generic PDP hero (#159)
75262c8 | 2026-06-11 13:13:41 -0700 | Add Premium Dark Chocolate Bar card to homepage product gallery (#158)
67e2d05 | 2026-06-11 13:12:13 -0700 | Add Subscribe CTA to Oscar + Santa Ana PDPs, create generic PDP (#157)
e718c15 | 2026-06-11 12:47:28 -0700 | Add Manage Subscription button to order status page for subscriptions (#156)
443efbb | 2026-06-11 12:41:35 -0700 | Add order-history.js to subscribe page so subscription saves to localStorage (#155)
9e1414d | 2026-06-10 19:39:47 -0700 | Save subscription to order history on success page (#154)
9fa0ab4 | 2026-06-10 19:26:49 -0700 | Fix redirect script stripping success/cancel params (#153)
792cf71 | 2026-06-10 19:11:02 -0700 | Fix subscription success/cancel URLs to match subscribe.js expectations (#152)
6c8c67b | 2026-06-10 19:07:57 -0700 | Add createSubscriptionPortalSession to Code.js + doGet route (#151)
33f319e | 2026-06-10 19:07:51 -0700 | Add subscription management cue to success page + portal endpoint (#149)
98b8fbc | 2026-06-10 19:05:10 -0700 | Add success/cancel state to subscribe page after Stripe redirect (#148)
e724b38 | 2026-06-10 18:57:27 -0700 | Fix subscription shipping amount being $0 due to wrong rate property (#147)
ada1e3e | 2026-06-10 18:53:15 -0700 | Add form autofill to subscribe page using existing CheckoutFormStorage (#146)
fde2451 | 2026-06-10 18:50:53 -0700 | Fix subscription: add product image to Stripe, fix shipping calc args (#145)
240710e | 2026-06-10 18:45:11 -0700 | Fix subscription GAS: duplicate function, + sign decoding, commit missing file (#144)
7cba891 | 2026-06-10 18:27:36 -0700 | Add createSubscriptionCheckoutSession route to doGet (#142)
6904d2d | 2026-06-10 18:20:22 -0700 | Fix success/cancel URLs for development mode on beta (#141)
… (truncated)
```

### `iching_oracle` → `oracle`

```
4f22eee | 2026-06-09 11:51:48 -0700 | fix: add .hero-glass[hidden] CSS rule to override display:grid
55251c5 | 2026-06-09 11:47:20 -0700 | fix: prevent initDaoIdentityState from racing with verification flow
e3877c0 | 2026-06-09 11:32:03 -0700 | feat: collapsible verified-identity panel with Unlink Identity
d89a94b | 2026-06-09 11:14:23 -0700 | fix: use DaoClient.verifyEmail() for EMAIL VERIFICATION flow
87d0e74 | 2026-06-09 10:50:23 -0700 | refactor: use DaoClient 1.1.0-rc.4 with explicit key names
6568fba | 2026-06-09 10:43:27 -0700 | fix: sync DaoClient truesight_dao_* keys to bare publicKey/privateKey
c46fe61 | 2026-06-09 10:41:13 -0700 | fix: call ensureKeys before checking keypair in DAO identity flows
936fa93 | 2026-06-09 09:13:22 -0700 | fix: ensureKeypair and submitSession must reuse existing keys — was overwriting on every page load (#61)
c23c573 | 2026-06-09 09:13:18 -0700 | fix: add missing arrayBufferToBase64 function and puppeteer dep — verification was crashing (#59)
0017b56 | 2026-06-09 07:21:25 -0700 | fix: add missing base64ToArrayBuffer helper + E2E registration test (#58)
1729307 | 2026-06-09 07:00:13 -0700 | test: add DAO Identity UI and full casting flow integration tests (#52)
690e0f8 | 2026-06-09 06:54:37 -0700 | test: add headless browser integration test — loads pages and checks console for errors (#51)
9de9c02 | 2026-06-09 06:46:03 -0700 | fix: bump dao-client from 1.1.0-rc.1 to 1.1.0-rc.3 (fixes constructor crash) (#50)
677aff7 | 2026-06-09 06:27:21 -0700 | fix: show credentials link after DAO identity verification + add JSDom test suite (#49)
63fed34 | 2026-06-08 17:10:30 -0700 | [autopilot] PR2 — Oracle migration to @truesight_dao/dao-client high-lev (#47)
```

### `Cypher-Defense` → `Cypher-Defense`

```
_(no commits on origin/master in window)_
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-06-16T042618Z_self-replication-sop-and-v2.md`

- **posted_at_utc:** `2026-06-16T04:26:18Z`  
- **slug:** `self-replication-sop-and-v2`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Governance (Process)** — Self-Replication SOP published: guides for spawning new autopilot instances and forking into new ecosystems.

### `beer-hall_2026-06-15T042930Z_kopi-bar-onboarding-legal-v7.md`

- **posted_at_utc:** `2026-06-15T04:29:30Z`  
- **slug:** `kopi-bar-onboarding-legal-v7`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Partners (Agroverse)** — Kopi Bar & Bakery (Berkeley) onboarded: partner page live with interior/hero photos and listed as wholesale stockist.

### `beer-hall_2026-06-14T041819Z_narrative-update-sophia-context-plan.md`

- **posted_at_utc:** `2026-06-14T04:18:19Z`  
- **slug:** `narrative-update-sophia-context-plan`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Web (Narrative)** — "Agentic AI and the Common Law Tradition" essay published with Lee Kuan Yew reflection and data sovereignty arguments.

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

- `notes/claude_donation_mint_2026-04-30.md`
- `notes/claude_serialized_qr_sales_2026-04-29.md`
- `notes/sophia_development_workflow.md`

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
