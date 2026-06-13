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

- Generated (UTC): `2026-06-13T03:59:24Z`
- Look-back: **7** calendar days (`2026-06-06` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | $2,851 | 7% | `2026-12-31` | 201 | **behind** |
| USA Agroverse Partners | 100 | — | — | `2026-12-31` | 201 | — |

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-06-12T10:59:14.491Z`
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

- **Email Agent Follow Up** — logged sends: warmup **245**, follow_up **70**, bulk **0**, unknown **2** (data rows: **317**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **88**, follow_up **23**, bulk **0**, unknown **2**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **69** stores — sum logged **warmup** sends (AU): **198**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **3** / **1** / **65**; follow-up depth (none / once / ≥2): **69** / **0** / **0**
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
- Manager record: `Gary Teh` · 31 SKU lines · 13,363.18 total units · $11,840.97

  | Inventory type | Unit format | Items | Units | Value (USD) |
  |----------------|-------------|-------|-------|-------------|
  | (uncategorized) | (unspecified) | 27 | 13,273 | $11,678.16 |
  | Packaging Material | Bulk | 1 | 74 | $49.98 |
  | Cacao Mass | Retail Ready | 2 | 14 | $112.82 |
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
| Green Gulch Zen Monastery | 6 | 84 | $222.54 |

_(+28 more in JSON snapshot.)_

### Cash float

_Skipped — re-run with `--with-sheet-sales` (or fix `google_credentials.json`) to surface USD / BRL balances._

### In-transit freight

_Skipped — re-run with `--with-sheet-sales` to surface in-flight `Shipment Ledger Listing` rows._

_Burn rate / days-of-cover is v2 — needs a sales × `inventory_type` join. The JSON snapshot reserves `sales_velocity_30d` / `days_of_cover_at_sf` slots so a dapp dashboard can be wired now and back-filled later._

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-06-06 | claude-code | Filed OPEN_FOLLOWUPS pending entry: scoped fine-grained agent PAT for GitHub-side enforcement of the repo-class policy (deferred by operator choice; trigger = observed guard bypass or second autonomous agent).
- 2026-06-09 | claude (subscriptions session) | GTIN MODEL (canonical, confirmed by Gary): the retail GTIN identifies the PRODUCT TYPE, not the unit/vintage — ALL chocolate bars share one chocolate-bar GTIN; ALL ceremonial cacao share one cacao GTIN. The serialized QR code (Agroverse QR codes tab, column A) is the per-unit identity that differentiates farm+vintage and resolves provenance. A vintage-independent "generic" SKU REUSES the existing shared GTIN (never mint a new GTIN per vintage); per-vintage agroverse.shop product pages are presentation sub-views of one GTIN (expect Merchant Center duplicate-GTIN across them). Provenance is always via QR, never GTIN. Documented in AGROVERSE_QR_CODE_BATCH_GENERATION.md §0 + NOTES_tokenomics.md (Agroverse QR codes tab) + CHOCOLATE_SUBSCRIPTION_PLAN.md (Decisions → GTIN model).
- 2026-06-09 | claude (subscriptions session) | CREDENTIAL HAND-OFF PROTOCOL (new canonical doc CREDENTIAL_HANDOFF_PROTOCOL.md): to get a secret onto a locked-down box an LLM can't SSH (SG blocks 22; box trusts only its own keypair, which lives on the autopilot box), the autopilot box (`sophia`) is the staging hub and Sophia propagates. Rules: never put secrets in chat/Telegram/PRs/commits; move via stdin (mask to prefix+len); chmod 600; stage under /home/ubuntu/ NOT /opt/truesight_autopilot (deploy.sh git-cleans it); prefer sourcing an existing secret (e.g. Stripe test key in sentiment_importer config/environments/development.rb). Then hand off in the Sophia thread (LLM can't post into an existing TG topic — operator drops the line; adapter auto-loads the plan). Pointer added to SOPHIA_HANDOFFS.md. Worked example: beta sandbox Stripe test key staged at ~/stripe_test_key → thread 1955.

_All dated lines on/after 2026-06-06_ (17):

- 2026-06-10 | claude-code | UAT (User Acceptance Testing) — end-to-end validation by the governor before signing off on a feature. The beta sandbox endpoint (thread 1955, `beta.edgar.truesight.me`) is the canonical UAT surface for Stripe-touching flows: standalone EC2 in NELANCO, Stripe TEST mode, isolated fulfillment queue. UAT is distinct from CI/E2E tests — it's the human governor running through the real user journey. Future LLMs and Sophia: when a plan says "UAT," it means the governor (Gary) tests end-to-end on the beta staging environment, not in CI.
- 2026-06-06 | claude-code | Merged duplicate OPEN_FOLLOW_UPS.md into OPEN_FOLLOWUPS.md (4 autopilot items → Recently shipped, all resolved by capability uplift); duplicate is now a tombstone redirect; canonical-file warning added; attention-surfaces refs updated; Sophia prompt gained single-backlog rule (truesight_autopilot#98).
- 2026-06-06 | claude-code | Repo-class policy: full org audit → 13 API-only data repos (never clone; Contents API only) + beta-first enforcement for *_prod repos with new sync_beta_to_prod tool. Doc: GITHUB_AGENTIC_AI_SSH.md §§ API-only repos / prod promotion. Code enforcement in truesight_autopilot (api_only_repos + prod_repos settings; git_push_changes/open_fix_pr/merge_pr guards).
- 2026-06-06 | claude-code | Filed OPEN_FOLLOWUPS pending entry: scoped fine-grained agent PAT for GitHub-side enforcement of the repo-class policy (deferred by operator choice; trigger = observed guard bypass or second autonomous agent).
- 2026-06-06 | autopilot | Added AUTOPILOT_EDGAR_SIGNING.md — the autopilot has its own RSA-2048 keypair and can sign Edgar payloads directly (no DApp approval gate). Use direct POST to edgar.truesight.me/dao/submit_contribution with RSASSA-PKCS1-v1_5 + SHA-256 signature. See AUTOPILOT_EDGAR_SIGNING.md for full guide.
- 2026-06-06 | autopilot | Added AGROVERSE_INVOICE_CONVENTION.md — invoice PDF convention for Agroverse partners. truesight.me color scheme (gold #d38900, warm cream bg), ReportLab layout, line-item table with alternating rows, payment/mailing address section. Upload to store_interaction_attachments/invoices/. See AGROVERSE_INVOICE_CONVENTION.md for full guide.
- 2026-06-06 | claude (outreach session) | SOPHIA BOX HARDWARE UPGRADE — PRESERVE THESE (not in git): /opt/truesight_autopilot/.env (incl. TELEGRAM_API_ID/HASH added on-box 2026-06-06, may differ from local .env), /opt/truesight_autopilot/.telethon_watchdog.session (Telethon user-session = full account access; loss requires Gary to redo interactive login), data/attention_watchdog_state.json (nudge timers, minor). In-place resize keeps EBS = safe; fresh volume must migrate these three. Watchdog runbook: memory + truesight_autopilot#102.
- 2026-06-06 | claude (outreach session) | SOPHIA AMI BLUE/GREEN RUNBOOK GOTCHA: never boot an AMI clone while the old box still runs the Telegram services — two clients on one Telethon auth key => AuthKeyDuplicatedError => session PERMANENTLY invalidated (Gary must redo interactive login); bot adapter double-getUpdates conflicts too. Cutover order: (1) stop truesight-autopilot-watchdog + truesight-autopilot-telegram on OLD box, (2) boot new instance + verify, (3) repoint Elastic IP, (4) shutdown old. Also: use AWS DLM for periodic AMIs; keep AMIs private (they contain .env, Gmail token, Telethon session).
- 2026-06-07 | claude (outreach session) | SOPHIA SELF-EXEC + AMI AUTOMATION SHIPPED: (1) ssh_run host="autopilot" (127.0.0.1 loopback) lets Sophia sudo/apt-get on her own box; sophia_infra.pub now self-trusted in box authorized_keys via deploy.sh + user-data.sh (truesight_autopilot#114). (2) System prompt embeds live host-identity block (IMDS) — no more location hallucination. (3) GROK_API_KEY added to box .env (health grok_key_set=true). (4) Weekly AMI automated: Cypher-Defense/.github/workflows/snapshot_autopilot_ami.yml (#37,#38), resolves by Name tag truesight-autopilot, --no-reboot, retain 8; secrets TRUESIGHT_DAO_AUTOPILOT_AWS_KEY/SECRET set on Cypher-Defense; first AMI ami-0dae91c5216989753. For the parallel infra session: the FLEET self-host + the AMI Name-tag resolution both assume tag Name=truesight-autopilot — keep that tag on any blue/green replacement instance.
- 2026-06-07 | claude (outreach session) | DB AMI BACKUPS AUTOMATED: Cypher-Defense/.github/workflows/snapshot_databases_ami.yml + scripts/aws/snapshot_databases_ami.py — full bootable AMIs of the two Nelanco DB boxes seni_sql (i-08ebe96afbc649a95, ext /dev/sdb 250GiB) + krake_data (i-07c76510b231d787f, ext /dev/sdf 100GiB), monthly 1st 04:00 UTC, --no-reboot, retain 6/instance, CYPHER_DEFENCE_AWS_* secrets. Complements (does not replace) the data-vol-only snapshot_databases.py. First AMIs: seni_sql ami-05098dac19769a8ae, krake_data ami-07f1e676f7c7b14aa (#39).
- 2026-06-07 | claude (outreach session) | AWS BACKUP STORAGE PRUNED + EBS-only DB job RETIRED: Cypher-Defense prune_aws_backups.py + prune_aws_backups.yml (monthly 2nd, after the 1st-of-month AMI backups) — keeps newest 2 legacy monthly EBS/codebase, deregisters AMIs >2yr + frees snapshots, deletes orphans; dry-run default, recomputes kept-AMI backing set after dereg so kept AMIs never lose snapshots. snapshot_databases.yml DELETED (redundant — DB AMI captures the data vol); snapshot_databases.py deprecation-bannered. First run: Nelanco 62 snaps/4164GiB -> 26/2690GiB, 41 AMIs -> 14 (27 deregistered, 36 snaps deleted, ~1474 GiB reclaimed). The two new DB AMIs survived. All three backup scripts (autopilot retain 8, db-ami retain 6, this janitor) now bound storage. (PR #40)
- 2026-06-07 | claude (outreach session) | SOPHIA EXECUTION-HANDOFF SHIPPED: (1) create_telegram_topic tool (truesight_autopilot#119) — Sophia opens a forum topic on request; needs bot=group admin w/ Manage Topics + TELEGRAM_HOME_GROUP_ID. (2) ping_sophia (dao_protocol#63, console `truesight-dao-ping-sophia`) — governor-signed one-shot to /chat-blocking; GOVERNOR-ONLY (Sophia 403s non-governors); reusable by any LLM on a governor machine. Working group = TrueSight DAO Ops -1003919341801; bot @truesight_autopilot_bot (8217115914). TELEGRAM_HOME_GROUP_ID set on box .env. Validated e2e: ping -> topic created in Ops group. Full handoff: local LLM commits roadmap to agentic_ai_context -> ping_sophia -> Sophia opens topic+kickoff -> governor monitors in that topic.
- 2026-06-07 | autopilot | Gary Teh grounding credential PK mapping: `pk-iWL9OH9hpE_D` = Gary Teh's public key for the truesight-grounding program. Practice events live in `lineage-credentials/programs/truesight-grounding/pk-iWL9OH9hpE_D/practice/`. This key is NOT in dao_members.json — it's a separate program-registration key. When Gary shares a credential URL like `truesight.me/programs/truesight-grounding/credentials/#pk-iWL9OH9hpE_D`, read the latest practice event from lineage-credentials, NOT from oracle_logs (which may return stale data).
- 2026-06-08 | claude (outreach session) | NEW CONVENTION — agent attribution required on every commit + PR: add `Generated-by: <agent>` trailer to commits (squash-merge persists it) + same line in PR body; identifies Sophia vs Claude Code vs Cursor vs Kimi etc. (git author is the human operator). Motivated by the 2026-06-08 oracle outage: Sophia PRs #36/#38/#39 broke oracle.truesight.me prod (index.html SyntaxError from a Didnt apostrophe +
- 2026-06-09 | claude (subscriptions session) | GTIN MODEL (canonical, confirmed by Gary): the retail GTIN identifies the PRODUCT TYPE, not the unit/vintage — ALL chocolate bars share one chocolate-bar GTIN; ALL ceremonial cacao share one cacao GTIN. The serialized QR code (Agroverse QR codes tab, column A) is the per-unit identity that differentiates farm+vintage and resolves provenance. A vintage-independent "generic" SKU REUSES the existing shared GTIN (never mint a new GTIN per vintage); per-vintage agroverse.shop product pages are presentation sub-views of one GTIN (expect Merchant Center duplicate-GTIN across them). Provenance is always via QR, never GTIN. Documented in AGROVERSE_QR_CODE_BATCH_GENERATION.md §0 + NOTES_tokenomics.md (Agroverse QR codes tab) + CHOCOLATE_SUBSCRIPTION_PLAN.md (Decisions → GTIN model).
- 2026-06-09 | claude (subscriptions session) | CREDENTIAL HAND-OFF PROTOCOL (new canonical doc CREDENTIAL_HANDOFF_PROTOCOL.md): to get a secret onto a locked-down box an LLM can't SSH (SG blocks 22; box trusts only its own keypair, which lives on the autopilot box), the autopilot box (`sophia`) is the staging hub and Sophia propagates. Rules: never put secrets in chat/Telegram/PRs/commits; move via stdin (mask to prefix+len); chmod 600; stage under /home/ubuntu/ NOT /opt/truesight_autopilot (deploy.sh git-cleans it); prefer sourcing an existing secret (e.g. Stripe test key in sentiment_importer config/environments/development.rb). Then hand off in the Sophia thread (LLM can't post into an existing TG topic — operator drops the line; adapter auto-loads the plan). Pointer added to SOPHIA_HANDOFFS.md. Worked example: beta sandbox Stripe test key staged at ~/stripe_test_key → thread 1955.
- 2026-06-10 | claude (subscriptions session) | TERM: UAT = User Acceptance Testing — a human walks the real end-to-end flow before go-live (NOT more automated tests). Convention: UAT runs on the BETA staging stack (beta.agroverse.shop + beta.edgar.truesight.me beta dao_protocol in Stripe TEST mode, SANDBOX rows), never prod, with Stripe test cards (4242…) — checkout must show TEST MODE. Prefer beta staging over local for UAT (that's what the beta sandbox is for). New doc GLOSSARY.md. Active: chocolate-bar subscription UAT = thread 1955. Live as of 2026-06-10: beta.agroverse.shop/subscribe/chocolate-bar/=200, beta.edgar webhook=400-on-unsigned (verifying).

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
25cdc00 | 2026-06-12 20:46:32 -0700 | Add Gary's honest reflection — felt like building a toy watching Microsoft demo (#210)
38e423a | 2026-06-12 20:44:58 -0700 | Add Microsoft and Google demo photos to the opening section (#209)
9eb63be | 2026-06-12 20:44:38 -0700 | Add photo of Google voice UX demo at TECH FEST 2026
2da00c4 | 2026-06-12 20:44:37 -0700 | Add photo of Microsoft agentic fleet demo at TECH FEST 2026
36f0c28 | 2026-06-12 20:41:22 -0700 | Fix: upload correct photo of Gary and Soniya
d3f6df1 | 2026-06-12 20:39:55 -0700 | Fix: upload correct photo of attendees drinking cacao
f710392 | 2026-06-12 20:39:30 -0700 | Fix: upload correct photo of Gary, Martin and Ken
c2e5806 | 2026-06-12 20:39:15 -0700 | Fix: upload correct photo of Gary and Soniya
14ac067 | 2026-06-12 20:39:01 -0700 | Fix: upload correct photo of Kim holding setup instructions on her phone
ae7d93a | 2026-06-12 20:38:40 -0700 | Fix: upload correct photo of Gary, Atrish and Kim
b27c9cd | 2026-06-12 20:36:52 -0700 | Fix: Soniya invited us and set up the cacao booth — she did the heavy lifting (#208)
044d67c | 2026-06-12 20:36:10 -0700 | Remove empty techfest-gary.jpg leftover file (#207)
b2a9d7b | 2026-06-12 20:35:54 -0700 | Fix blog post photo references and captions — correct the mix-up (#206)
0738ae9 | 2026-06-12 20:35:30 -0700 | Fix: re-upload Gary, Atrish and Kim photo
5f43be8 | 2026-06-12 20:35:26 -0700 | Fix: upload Gary and Soniya photo
5922f92 | 2026-06-12 20:35:25 -0700 | Fix: upload Gary, Martin and Ken photo
f3c8048 | 2026-06-12 20:35:24 -0700 | Fix: upload attendees drinking cacao photo
dd543d7 | 2026-06-12 20:35:23 -0700 | Fix: upload Kim holding instructions photo
e26beb4 | 2026-06-12 20:31:38 -0700 | Fix: demoralized watching demos on stage, lifted by seeing Sophia delight others (#204)
9691aac | 2026-06-12 20:29:57 -0700 | Fix Martin section — he's a longtime DAO supporter and cacao lover (#203)
9112926 | 2026-06-12 20:28:28 -0700 | Add blog post: The Joy Was the Point — TECH FEST 2026 reflection (#202)
8888b88 | 2026-06-12 20:27:29 -0700 | Add TECH FEST 2026 photo - cacao tasting
0a3c264 | 2026-06-12 20:27:28 -0700 | Add TECH FEST 2026 photo - Gary and Soniya
59b4ccf | 2026-06-12 20:27:27 -0700 | Add TECH FEST 2026 photo - Gary, Martin, Ken
83cc40c | 2026-06-12 20:27:26 -0700 | Add TECH FEST 2026 photo - Gary, Atrish, Kim
614ee64 | 2026-06-12 20:27:25 -0700 | Add TECH FEST 2026 photo - Gary
8ac0df3 | 2026-06-12 20:38:13 +0000 | chore(stats): refresh stats/current.json [skip ci]
feb220f | 2026-06-12 15:49:03 +0000 | chore(stats): refresh stats/current.json [skip ci]
8e5e8c3 | 2026-06-12 10:50:40 +0000 | chore(stats): refresh stats/current.json [skip ci]
83779f0 | 2026-06-12 05:21:25 +0000 | chore(stats): refresh stats/current.json [skip ci]
810badd | 2026-06-11 21:03:41 +0000 | chore(stats): refresh stats/current.json [skip ci]
9b54839 | 2026-06-11 16:38:23 +0000 | chore(stats): refresh stats/current.json [skip ci]
5fe5485 | 2026-06-11 11:13:12 +0000 | chore(stats): refresh stats/current.json [skip ci]
831b683 | 2026-06-11 05:12:06 +0000 | chore(stats): refresh stats/current.json [skip ci]
d20a461 | 2026-06-10 20:24:26 -0700 | assets: update narration with self-hosted sovereignty section
6d5504d | 2026-06-10 20:23:51 -0700 | blog: add self-hosted sovereignty section to Darwinian Agent post (#201)
95d921a | 2026-06-10 21:09:39 +0000 | chore(stats): refresh stats/current.json [skip ci]
695ab71 | 2026-06-10 16:23:10 +0000 | chore(stats): refresh stats/current.json [skip ci]
378678e | 2026-06-10 08:42:08 -0700 | assets: update narration with Claude feedback revisions
60cb1d7 | 2026-06-10 08:41:29 -0700 | blog: address Claude's feedback — fix Polanyi claim, tighten sovereignty, resolve gift tension (#200)
… (truncated)
```

### `market_research` → `go_to_market`

```
7a806bd | 2026-06-05 22:39:52 -0700 | Add West Coast distributor list assembly proposal for ceremonial cacao & chocolate (#165)
```

### `agentic_ai_context` → `agentic_ai_context`

```
63db74d | 2026-06-12 16:59:09 -0700 | handoff(vault): login via dao-client DAO Identity (like capoeira) + root->/vault/login link (#473)
198aba4 | 2026-06-12 13:35:23 -0700 | chore(previews): refresh Beer Hall preview (2026-06-12 UTC)
91cb1cb | 2026-06-12 13:35:22 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-12 UTC)
e3c44fa | 2026-06-12 08:47:15 -0700 | chore(previews): refresh Beer Hall preview (2026-06-12 UTC)
d2693aa | 2026-06-12 08:47:13 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-12 UTC)
c965ad8 | 2026-06-12 03:49:17 -0700 | chore(previews): refresh Beer Hall preview (2026-06-12 UTC)
b6152ba | 2026-06-12 03:49:16 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-12 UTC)
618cefd | 2026-06-11 22:14:07 -0700 | chore(previews): refresh Beer Hall preview (2026-06-12 UTC)
9a2547f | 2026-06-11 22:14:06 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-12 UTC)
7b52b89 | 2026-06-11 21:58:25 -0700 | handoff: Sophia vault hotfix + ops-safety roll-up (thread 2744) (#472)
e2257d1 | 2026-06-11 21:12:46 -0700 | Merge pull request #470 from TrueSightDAO/auto/advisory-refresh-2026-06-12
4854c6c | 2026-06-12 04:12:35 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-12 UTC)
2dbb8e1 | 2026-06-11 16:17:56 -0700 | Reorder execution plan: vault-first (Phase 3 → Phase 0.1 → vault), add worktree convention (#459)
8983672 | 2026-06-11 16:10:31 -0700 | handoff(live-progress): register thread 2799 (Sophia parked GO-ready) (#458)
b572f09 | 2026-06-11 16:03:18 -0700 | plan: Sophia live-progress introspection (quick handoff) (#457)
f90cae3 | 2026-06-11 15:12:23 -0700 | Add Phase 0 governance plan PDF for DAO sharing
5ddf6b3 | 2026-06-11 15:10:36 -0700 | handoff(governance): register thread 2744 (Sophia parked GO-ready, Phase 0) (#454)
7de043c | 2026-06-11 15:06:20 -0700 | Add QR Code Registration implementation plan (#452)
e67dfa2 | 2026-06-11 15:05:48 -0700 | plan: Sophia multi-tenant governance, identity & vault roadmap + UAT (#453)
b6db1a1 | 2026-06-11 15:03:32 -0700 | Add QR Code Registration implementation plan PDF
336a02e | 2026-06-11 14:06:44 -0700 | Add PDF of Friends of the Rainforest implementation plan
40d3d21 | 2026-06-11 13:54:48 -0700 | Add Sophia's DAO contributor ledger name to operating instructions (#450)
f8c5102 | 2026-06-11 13:42:56 -0700 | chore(previews): refresh Beer Hall preview (2026-06-11 UTC)
3ccc8d5 | 2026-06-11 13:42:55 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-11 UTC)
aea7136 | 2026-06-11 13:32:23 -0700 | handoff(followup-monitor): register thread 2622 (Sophia parked GO-ready) (#449)
0b9ab07 | 2026-06-11 13:23:54 -0700 | Add deferred follow-up for Chocolate Subscription Phase 2 (#448)
36d0344 | 2026-06-11 13:09:32 -0700 | handoff: Sophia durable follow-up monitor — plan + UAT + registry rows (#447)
2f3c4fd | 2026-06-11 11:17:41 -0700 | Update PDF: clarify events live on agroverse.shop, not truesight.me
b5468ec | 2026-06-11 11:09:17 -0700 | Update PDF with self-reinforcing loop diagram
206b97e | 2026-06-11 11:02:27 -0700 | Add PDF of Partner Events Monitoring implementation plan
a1d6129 | 2026-06-11 10:38:28 -0700 | Add freight profit analysis methodology runbook (#445)
29a6110 | 2026-06-11 09:36:22 -0700 | chore(previews): refresh Beer Hall preview (2026-06-11 UTC)
53e4401 | 2026-06-11 09:36:20 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-11 UTC)
bc9d3ab | 2026-06-11 08:50:13 -0700 | Update freight profit analysis v4 - apothecaries not Upper Taekri
e814dc8 | 2026-06-11 08:48:46 -0700 | Update freight profit analysis v3 with $50 mass bar pricing
57f8ece | 2026-06-11 08:46:48 -0700 | Update freight profit analysis with corrected pricing
552f6df | 2026-06-11 08:42:26 -0700 | Add detailed freight profit analysis PDF
f3ac8ab | 2026-06-11 04:09:35 -0700 | chore(previews): refresh Beer Hall preview (2026-06-11 UTC)
d86ad95 | 2026-06-11 04:09:34 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-06-11 UTC)
18e3b26 | 2026-06-10 22:09:44 -0700 | chore(previews): refresh Beer Hall preview (2026-06-11 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
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
85a4d98 | 2026-06-06 17:45:35 -0700 | docs(identity manifest): map the 3 orphan files to scriptId 1m8IZPs1 (#338)
76d0ded | 2026-06-06 07:13:43 -0700 | [autopilot] Add Sentinel role support to dao_members_cache_publisher.gs  (#335)
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
706b159 | 2026-06-12 10:41:39 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
8cba6bb | 2026-06-11 10:59:43 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
a68906a | 2026-06-10 10:35:20 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
5ce8b7a | 2026-06-09 10:04:56 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b082748 | 2026-06-08 11:30:42 +0000 | chore: refresh partners-velocity snapshot [skip ci]
d4be99b | 2026-06-08 11:22:22 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
e5206f4 | 2026-06-07 09:41:41 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
1c64adf | 2026-06-06 08:48:18 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
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
d737445 | 2026-06-10 18:08:33 -0700 | Move address fields above summary on subscribe page (#139)
1ca97e5 | 2026-06-10 16:54:28 -0700 | Replace premature Stripe note with contextual helper text on subscribe page (#137)
9181c03 | 2026-06-10 16:38:09 -0700 | Add address suggestion UI — accept correction or keep original (#136)
0d37fd1 | 2026-06-10 16:38:05 -0700 | Add address verification UI to subscribe page — accept suggested corrections (#135)
bd47586 | 2026-06-10 16:29:18 -0700 | Add browser-native address autocomplete attributes to subscribe form (#134)
a5706d5 | 2026-06-10 16:22:38 -0700 | Rename product to 'Premium Dark Chocolate Bar — Single-Estate, Monthly Discovery' (#133)
ad6085e | 2026-06-10 16:11:49 -0700 | Rename product to 'Single-Estate, Monthly Discovery' (#132)
df9d572 | 2026-06-10 15:56:48 -0700 | Add address blur listeners to trigger live shipping calculation on subscribe page (#131)
d684044 | 2026-06-10 15:56:45 -0700 | Add shipping rates container and address blur listeners to subscribe page HTML (#130)
5f0b2e3 | 2026-06-10 15:56:41 -0700 | Add live shipping calculation to subscribe page — shows shipping cost as soon as address is filled (#129)
b79a124 | 2026-06-10 15:49:34 -0700 | Fix subscribe/chocolate-bar/ — add slug query param redirect (#128)
a9e10a9 | 2026-06-09 15:02:38 -0700 | [autopilot] Facebook Pixel leaks from beta.agroverse.shop into productio (#127)
3e0f708 | 2026-06-09 14:32:12 -0700 | PR1.5: Generic-bar PDP at /product-page/ceremonial-cacao-chocolate-bar/ (#126)
44c22fa | 2026-06-09 14:32:08 -0700 | PR1.4: Add createSubscriptionCheckoutSession function body (#125)
dd41a5b | 2026-06-09 14:32:05 -0700 | PR1.3: Clean path wrapper /subscribe/chocolate-bar/ (#123)
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
1493693 | 2026-06-08 15:39:22 -0700 | feat: fire-and-forget daily briefing trigger after governor's reading (#46)
f7f4575 | 2026-06-08 15:35:57 -0700 | Update dao-client CDN URL to @1.1.0-rc.1 for testing (#45)
1abc49b | 2026-06-08 14:41:13 -0700 | fix(oracle): adopt @truesight_dao/dao-client@1.0.1 CDN bundle (#44)
88ec3fd | 2026-06-08 13:48:29 -0700 | hotfix: revert #42 CDN integration — package global API mismatch broke signing (#43)
176eac6 | 2026-06-08 13:36:31 -0700 | PR1: Add CDN @truesight_dao/dao-client@1.0.0, replace base64 helpers with DaoClient.* (#42)
edc64bc | 2026-06-08 09:53:47 -0700 | hotfix: restore oracle — revert broken CDN refactor + resend syntax errors (#40)
d175a6f | 2026-06-08 00:23:43 -0700 | fix: add @truesight/dao-client CDN script tag to index.html (#39)
bda78aa | 2026-06-08 00:22:40 -0700 | refactor: swap inline DAO client code for @truesight/dao-client (#38)
ed016e2 | 2026-06-07 22:13:32 -0700 | feat: add resend verification email affordance to oracle (PR2) (#36)
c49f533 | 2026-06-07 21:09:35 -0700 | Fix DAO-identity linking: signature verification, dynamic verify URL, 3-state UX, retire stale SW (#35)
c41b37e | 2026-06-07 19:39:25 -0700 | fix: add generation_source_url to EMAIL REGISTERED EVENT so verification email returns to oracle.truesight.me (#33)
8f93da3 | 2026-06-07 19:21:21 -0700 | Add timestamp nonce to email registration to avoid duplicate signature rejection (#32)
5908140 | 2026-06-07 19:14:34 -0700 | Fix verification email return_url to point back to oracle page (#31)
9414bcf | 2026-06-07 19:10:27 -0700 | Fix email registration format to include -------- separator for SignatureVerifier (#30)
9440e3b | 2026-06-07 19:02:58 -0700 | Add "Link to DAO Identity" button in hero actions row (#29)
```

### `Cypher-Defense` → `Cypher-Defense`

```
4a68565 | 2026-06-07 14:52:29 -0700 | Prune old AWS backups + retire redundant EBS-only DB snapshot job (#40)
6328007 | 2026-06-07 14:35:36 -0700 | Monthly AMI backups of the two production DB EC2 instances (Nelanco) (#39)
e749b90 | 2026-06-07 14:17:11 -0700 | Fix AMI backup: AMI Description must be ASCII (em-dash -> hyphen) (#38)
a7615af | 2026-06-07 14:12:26 -0700 | Weekly AMI backup of the autopilot EC2 (blue/green DR) (#37)
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-06-13T035924Z_tech-fest-recap-sophia-hotfix.md`

- **posted_at_utc:** `2026-06-13T03:59:24Z`  
- **slug:** `tech-fest-recap-sophia-hotfix`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Web (Blog)** — "The Joy Was the Point" TECH FEST 2026 reflection published with full event gallery and contributor credits.

### `beer-hall_2026-06-12T041228Z_friends-rainforest-live-sophia-phase-0.md`

- **posted_at_utc:** `2026-06-12T04:12:28Z`  
- **slug:** `friends-rainforest-live-sophia-phase-0`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Web (Shop)** — "Friends of the Rainforest" landing page live with rich media, QR-linked event signup, and subscription CTAs.

### `beer-hall_2026-06-11T041108Z_subscription-verification-aora-plan.md`

- **posted_at_utc:** `2026-06-11T04:11:08Z`  
- **slug:** `subscription-verification-aora-plan`  
- **Message 1 excerpt (first two non-empty lines):**

  Automated daily digest of the DAO
  - **Web (Blog)** — "Sovereignty in the Age of Replaceable AI" post published with revised sovereignty section and updated narration.

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
