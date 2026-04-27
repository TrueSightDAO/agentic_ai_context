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

- Generated (UTC): `2026-04-27T09:04:59Z`
- Look-back: **7** calendar days (`2026-04-20` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | $1,928 | 5% | `2026-12-31` | 248 | **behind** |
| USA Agroverse Partners | 100 | 26 | 26% | `2026-12-31` | 248 | **behind** |

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-04-26T10:59:14.160Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **522**
- Partnered (north-star): **13**
- Meeting Scheduled: **1**
- Shortlisted: **4**

## Funnel by status (curated order)

- AI: Enrich — manual: 69  (#3)
- AI: Contact Form found: 77  (#4)
- AI: Photo rejected: 107  (#7)
- AI: Photo needs review: 41  (#8)
- AI: Prospect replied: 2  (#9)
- AI: Warm up prospect: 64  (#10)
- Not Appropriate: 71  (#11)
- Contacted: 4  (#12)
- Shortlisted: 4  (#13)
- Manager Follow-up: 26  (#14)
- Meeting Scheduled: 1  (#16)
- Instagram Followed: 11  (#17)
- On Hold: 17  (#18)
- **Partnered: 13**  (#19)
- Rejected: 14  (#20)
- Followed Up: 1  (#21)

## Email outreach visibility (logged sends + Hit List AU/AV)

- **Email Agent Follow Up** — logged sends: warmup **64**, follow_up **42**, bulk **0**, unknown **0** (data rows: **106**)
- Distinct recipient addresses (`to_email`, by log `status`): warmup **61**, follow_up **18**, bulk **0**, unknown **0**

### Hit List cohorts (stores in stage × AU/AV send counts)

- **AI: Warm up prospect**: **64** stores — sum logged **warmup** sends (AU): **28**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **38** / **24** / **2**; follow-up depth (none / once / ≥2): **64** / **0** / **0**
- **Manager Follow-up**: **26** stores — sum logged **warmup** sends (AU): **0**, sum logged **follow-up** sends (AV): **16**; warmup depth (none / once / ≥2): **26** / **0** / **0**; follow-up depth (none / once / ≥2): **20** / **1** / **5**
- **Bulk Info Requested**: _(no rows in this status)_
- **AI: Prospect replied**: **2** stores — sum logged **warmup** sends (AU): **0**, sum logged **follow-up** sends (AV): **0**; warmup depth (none / once / ≥2): **2** / **0** / **0**; follow-up depth (none / once / ≥2): **2** / **0** / **0**
- **Follow-up pipeline (combined)**: **28** stores — sum logged **warmup** sends (AU): **0**, sum logged **follow-up** sends (AV): **16**; warmup depth (none / once / ≥2): **28** / **0** / **0**; follow-up depth (none / once / ≥2): **22** / **1** / **5**

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-04-22 | cursor | **Newsletter workbook `1ed3q3…`:** IMPORTRANGE mirrors (Subscribers, QR codes, SKUs, Currencies) + **Email 360** (lookup email → sends, QR, SKUs via ledger slug→Shipment, subscriber row, campaigns) + **Workbook context** tab. Script **`market_research/scripts/setup_newsletter_workbook_mirrors.py`**. **`AGROVERSE_NEWSLETTER_WORKFLOW.md`** + **`send_newsletter.py`** (`NEWSLETTER_LOG_SPREADSHEET_ID`) + **`sentiment_importer`** `Gdrive::NewsletterEmails` same ID; removed stray **`binding.pry`** in **`newsletter_controller#click`**.
- 2026-04-24 | cursor | **Hit List retailer pipeline — email tracking + reconcile:** **sentiment_importer (Edgar)** — `GET /email_agent/open.gif` + `/email_agent/click` + `Gdrive::EmailAgentDrafts` (merged PR **#1031**). **go_to_market** — `--track-clicks` / **Open** & **Click through** on **Email Agent Drafts**; **`regenerate_pending_email_agent_draft_tracking.py`** for MIME refresh; **`reconcile_email_agent_drafts_stale_sent.py`** when Gmail is **SENT** but the sheet still says **`pending_review`**. **`HIT_LIST_CREDENTIALS.md`**; **`WORKSPACE_CONTEXT.md`** §4 Hit List bullet.

_All dated lines on/after 2026-04-20_ (6):

- 2026-04-21 | cursor | **DAO client AI contributions:** **`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`** — convention for AI **`[CONTRIBUTION EVENT]`** via **`dao_client`** (TrueSightDAO PR URLs + explicit body). **`dao_client`:** **`modules/report_ai_agent_contribution.py`**. README + **`PROJECT_INDEX.md`** (dao_client row) + **`WORKSPACE_CONTEXT.md`** pointers.
- 2026-04-23 | cursor | **Hit List draft-registry tab** renamed **Email Agent Suggestions** → **Email Agent Drafts** (live sheet + Python constants + `ensure_email_agent_suggestions_sheet.py` legacy rename). **GAS:** `store_interaction_history_api.gs` tab + **`email_agent_drafts`** JSON; `email_agent_drafts.gs`, `newsletter_subscriber_sync.gs`. **DApp:** `store_interaction_history.html`. Docs: **`HIT_LIST_CREDENTIALS.md`**, **`PARTNER_OUTREACH_PROTOCOL.md`**, **`GMAIL_OAUTH_WORKFLOW.md`**, **`PROJECT_INDEX.md`**, tokenomics `google_app_scripts` READMEs. Redeploy web app after `clasp push`.
- 2026-04-23 | cursor | **Tokenomics — phrase “clasp deploy”:** When the user says **clasp deploy** (or similar) without listing steps, agents **always** run **`clasp push`** from the correct **`tokenomics/clasp_mirrors/<scriptId>/`** (after syncing canonical **`google_app_scripts/**`** into mirror files clasp pushes, e.g. **`Code.js`**, per **`clasp_mirrors/PROJECT_INDEX.md`** / checklist), **then** **`clasp deploy`**. For **existing Web App** URLs use **`clasp deploy --deploymentId <id>`** so **`/exec`** stays stable—avoid bare **`clasp deploy`** unless creating a new deployment on purpose. **`NOTES_tokenomics.md`** § *Google Apps Script*, **`WORKSPACE_CONTEXT.md`** §3a tokenomics bullet, **`tokenomics/clasp_mirrors/README.md`** workflow.
- 2026-04-22 | cursor | **Newsletter workbook `1ed3q3…`:** IMPORTRANGE mirrors (Subscribers, QR codes, SKUs, Currencies) + **Email 360** (lookup email → sends, QR, SKUs via ledger slug→Shipment, subscriber row, campaigns) + **Workbook context** tab. Script **`market_research/scripts/setup_newsletter_workbook_mirrors.py`**. **`AGROVERSE_NEWSLETTER_WORKFLOW.md`** + **`send_newsletter.py`** (`NEWSLETTER_LOG_SPREADSHEET_ID`) + **`sentiment_importer`** `Gdrive::NewsletterEmails` same ID; removed stray **`binding.pry`** in **`newsletter_controller#click`**.
- 2026-04-24 | cursor | **Hit List retailer pipeline — email tracking + reconcile:** **sentiment_importer (Edgar)** — `GET /email_agent/open.gif` + `/email_agent/click` + `Gdrive::EmailAgentDrafts` (merged PR **#1031**). **go_to_market** — `--track-clicks` / **Open** & **Click through** on **Email Agent Drafts**; **`regenerate_pending_email_agent_draft_tracking.py`** for MIME refresh; **`reconcile_email_agent_drafts_stale_sent.py`** when Gmail is **SENT** but the sheet still says **`pending_review`**. **`HIT_LIST_CREDENTIALS.md`**; **`WORKSPACE_CONTEXT.md`** §4 Hit List bullet.
- 2026-04-22 | cursor | **Email 360 — purpose doc:** **`AGROVERSE_NEWSLETTER_WORKFLOW.md`** §**1b** — why the tab exists (email→newsletters/QR/SKU-shipment/subscriber/currencies for de-noise + forensics), what it does **not** infer (no SKU in send log), and that formulas are regenerated by **`setup_newsletter_workbook_mirrors.py`** from detected headers (**B2** lookup).

---

## Pipeline activity map (PROJECT_INDEX ↔ git)

| Pipeline | Mapped clone | Activity in window |
|----------|----------------|----------------------|
| `go_to_market` | `market_research` | **yes** |
| `openclaw` | `agentic_ai_context` | **yes** |
| `TrueChain` | `TrueChain` | **no** |
| `oracle` | `iching_oracle` | **yes** |

---

## Git log by repo (origin default branch)

### `truesight_me` → `truesight_me_beta`

```
b4f96bd | 2026-04-24 13:38:16 -0700 | blog: link interactive artifacts and swap private Edgar repo for public dao_client (#52)
f2473bd | 2026-04-24 13:20:33 -0700 | blog: add Stone Soup folklore analogy to Plug-and-Play architecture post (#51)
ddea086 | 2026-04-24 13:12:53 -0700 | blog: expand Plug-and-Play post with concrete examples, repo links, and accessibility (#50)
221d685 | 2026-04-24 13:04:45 -0700 | blog: unique header images for Do Nothing Society and Plug-and-Play posts (#49)
82be0fc | 2026-04-24 13:00:07 -0700 | blog: Plug-and-play architecture — why every service reads from one sheet (#48)
ee41942 | 2026-04-24 12:48:31 -0700 | blog: The Do Nothing Society — let machines run the chain, let humans hold the soul (#47)
90f50c3 | 2026-04-24 11:52:26 -0700 | Merge pull request #46 from TrueSightDAO/fix/mobile-overflow-beerhall-detail
dfb498c | 2026-04-24 11:52:03 -0700 | fix: prevent mobile overflow on beerhall detail view
d8db274 | 2026-04-21 15:47:21 -0700 | Merge pull request #45 from TrueSightDAO/docs/blog-oracle-feedback-loop
d066d57 | 2026-04-21 15:46:39 -0700 | blog: oracle feedback loop — offline activity to daily advisory
986bcbc | 2026-04-21 13:55:51 -0700 | docs(blog): retarget signature-onboarding demo links to TrueSightDAO/dao_client (#44)
f9cfed7 | 2026-04-20 12:15:29 -0700 | Merge pull request #43 from TrueSightDAO/docs/add-markdown-mirror-alt-links
5a99cf4 | 2026-04-20 12:15:11 -0700 | Add (md) alt link next to each agreement: point LLMs at Markdown mirror
1182ede | 2026-04-20 11:54:03 -0700 | Merge pull request #42 from TrueSightDAO/docs/agreement-anchor-titles
d96c0b8 | 2026-04-20 11:53:47 -0700 | Agreement anchor text: use formal doc titles for clarity
f29f70e | 2026-04-20 11:51:09 -0700 | Merge pull request #41 from TrueSightDAO/docs/clarify-truetech-vs-brazilian-suppliers
35ad693 | 2026-04-20 11:50:50 -0700 | Agroverse whitepaper: clarify TrueTech Inc (US importer) ≠ Brazilian suppliers
1e0f787 | 2026-04-20 11:45:39 -0700 | Merge pull request #40 from TrueSightDAO/fix/broken-partnership-agreement-links
c8a6394 | 2026-04-20 11:45:16 -0700 | Fix 31 partnership-agreement links: redirect → direct Google Doc URLs
7a1f435 | 2026-04-20 11:29:07 -0700 | Merge pull request #39 from TrueSightDAO/feature/rename-start-script
efb177d | 2026-04-20 11:28:56 -0700 | Rename start_server.sh to start_local.sh (standardize across repos)
f507df8 | 2026-04-20 11:18:26 -0700 | Merge pull request #38 from TrueSightDAO/docs/drop-vault-standard-rate-add-review-proposal-nav
6489dce | 2026-04-20 11:18:07 -0700 | Whitepaper: drop Vault + Standard Rate; nav "Proposals" → "Review & vote"
b5b546f | 2026-04-20 11:11:54 -0700 | Merge pull request #37 from TrueSightDAO/docs/whitepaper-accuracy-and-drop-gas-fee
dc0bbc2 | 2026-04-20 11:11:29 -0700 | Whitepapers: drop Gas Fee; define Edgar/TrueChain/Oracle; Beer Hall archive-only
bcbf5e6 | 2026-04-20 10:50:25 -0700 | Merge pull request #36 from TrueSightDAO/feat/agroverse-partnership-economics
7c376d0 | 2026-04-20 10:45:24 -0700 | docs: communications architecture; drop prisoner-dilemma framing (#35)
544ce84 | 2026-04-20 10:43:36 -0700 | agroverse: add unit economics + partnership shapes; fix 2.65% fee
```

### `market_research` → `go_to_market`

```
3904e3d | 2026-04-24 16:30:15 -0700 | ci: install gspread for live Sheets fetch in advisory snapshot
```

### `agentic_ai_context` → `agentic_ai_context`

```
bdd7d1b | 2026-04-26 21:07:44 -0700 | chore(previews): refresh Beer Hall preview (2026-04-27 UTC)
a71c052 | 2026-04-26 21:07:42 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-27 UTC)
9ed4c34 | 2026-04-26 19:32:23 -0700 | Merge pull request #54 from TrueSightDAO/auto/advisory-refresh-2026-04-27
3b1bcc9 | 2026-04-27 02:32:13 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-27 UTC)
3a0ec03 | 2026-04-26 12:28:36 -0700 | chore(previews): refresh Beer Hall preview (2026-04-26 UTC)
599d622 | 2026-04-26 12:28:35 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-26 UTC)
444fd9e | 2026-04-26 06:46:29 -0700 | chore(previews): refresh Beer Hall preview (2026-04-26 UTC)
edef04c | 2026-04-26 06:46:28 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-26 UTC)
8c4d089 | 2026-04-26 01:01:39 -0700 | chore(previews): refresh Beer Hall preview (2026-04-26 UTC)
a64d824 | 2026-04-26 01:01:38 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-26 UTC)
0e57a61 | 2026-04-25 21:02:49 -0700 | chore(previews): refresh Beer Hall preview (2026-04-26 UTC)
8b99690 | 2026-04-25 21:02:48 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-26 UTC)
d95d2ed | 2026-04-25 19:30:25 -0700 | Merge pull request #53 from TrueSightDAO/auto/advisory-refresh-2026-04-26
cef6366 | 2026-04-26 02:30:15 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-26 UTC)
17f7a49 | 2026-04-25 12:26:18 -0700 | chore(previews): refresh Beer Hall preview (2026-04-25 UTC)
c702a12 | 2026-04-25 12:26:17 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-25 UTC)
9aad56b | 2026-04-25 06:43:42 -0700 | chore(previews): refresh Beer Hall preview (2026-04-25 UTC)
0503c1e | 2026-04-25 06:43:41 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-25 UTC)
62fec98 | 2026-04-25 00:52:35 -0700 | chore(previews): refresh Beer Hall preview (2026-04-25 UTC)
7ce2b0a | 2026-04-25 00:52:34 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-25 UTC)
0a3344f | 2026-04-24 20:40:21 -0700 | chore(previews): refresh Beer Hall preview (2026-04-25 UTC)
29a7716 | 2026-04-24 20:40:20 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-25 UTC)
c22c9a1 | 2026-04-24 19:07:19 -0700 | Merge pull request #52 from TrueSightDAO/auto/advisory-refresh-2026-04-25
f56ade3 | 2026-04-25 02:07:10 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-25 UTC)
9f95eef | 2026-04-24 16:33:27 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
d81801f | 2026-04-24 16:33:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
de6aadf | 2026-04-24 16:32:10 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
21b0f7c | 2026-04-24 16:32:09 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
aaa123d | 2026-04-24 16:27:46 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
22a3d36 | 2026-04-24 16:27:45 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
a277910 | 2026-04-24 16:19:59 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
c147647 | 2026-04-24 16:19:58 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
256630c | 2026-04-24 12:29:15 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
d2c27f7 | 2026-04-24 12:29:14 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
c5507aa | 2026-04-24 10:58:00 -0700 | docs(sentiment_importer): add NOTES with deploy flow + systemd env gotcha (#49)
69ed377 | 2026-04-24 10:42:42 -0700 | docs: note sentiment_importer deploy.sh flow (#48)
6eaae20 | 2026-04-24 07:14:28 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
fe3780d | 2026-04-24 07:14:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
4a726fd | 2026-04-24 01:31:30 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
a49b6e0 | 2026-04-24 01:31:29 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
3065561 | 2026-04-26 15:55:58 -0700 | fix(gas): normalize Stores Visits Field Reports rows for GitHub URL keys
ae98ca1 | 2026-04-24 10:12:29 -0700 | feat(gas): include visible Agroverse logo tracker in draft HTML. (#245)
a93030c | 2026-04-23 17:30:46 -0700 | Merge pull request #244 from TrueSightDAO/feat/email-agent-drafts-open-click
b6dfe32 | 2026-04-23 17:30:09 -0700 | feat(apps-script): Email Agent Drafts Open and Click through columns
2f71a03 | 2026-04-23 17:21:59 -0700 | Merge pull request #243 from TrueSightDAO/docs/clasp-mirrors-readme-deploy-note
c7dee85 | 2026-04-23 17:21:37 -0700 | docs(clasp_mirrors): document clasp deploy shorthand
2a9f729 | 2026-04-23 17:01:40 -0700 | Fix listStoresByFilter: pass warmup/followup buckets into listHitListByFilter_. (#242)
a9c940d | 2026-04-23 16:57:39 -0700 | Store History API: eight AU/AV depth buckets and list filters (#241)
d9506f9 | 2026-04-23 16:31:21 -0700 | Document Apps Script editor vs web app Gmail sender identity.
b2c5c5f | 2026-04-23 16:18:25 -0700 | feat(metrics): outreach_visibility in weekly JSON; store history pipeline touches (#240)
99a3d80 | 2026-04-23 16:16:02 -0700 | GAS email verification: editor resend helpers and execution logging.
7ae14f8 | 2026-04-22 19:33:51 -0700 | Merge pull request #239 from TrueSightDAO/qr-code-sales-webhook-script-lock
1d6b110 | 2026-04-22 19:33:32 -0700 | Serialize QR Code Sales webhooks with LockService script locks
874827a | 2026-04-22 19:14:57 -0700 | Merge pull request #238 from TrueSightDAO/inventory-webhook-script-lock
6caa170 | 2026-04-22 19:14:40 -0700 | Serialize inventory webhook GETs with LockService script lock
e6abd2d | 2026-04-21 23:42:19 -0700 | feat(dao_members_cache): emit dao_totals at snapshot root (schema_version 2) (#237)
1de4b60 | 2026-04-21 23:25:53 -0700 | feat(tdg_identity_management): dao_members.json cache publisher + doGet action (#236)
1b28994 | 2026-04-21 15:46:30 -0700 | Merge pull request #235 from TrueSightDAO/feature/gas-inventory-expense-authorization
fef3c29 | 2026-04-21 15:46:08 -0700 | feat(gas): unauthorized movement + scored expense Processing Status
539bf43 | 2026-04-21 15:25:03 -0700 | Merge pull request #234 from TrueSightDAO/docs/schema-telegram-chat-logs-governor-s
1b30c34 | 2026-04-21 15:24:40 -0700 | docs(schema): Telegram Chat Logs column S Governor + Edgar semantics
1d65efb | 2026-04-21 14:45:48 -0700 | feat(gas): notify treasury-cache-publisher on 5 additional write-paths (#233)
af8fc00 | 2026-04-21 14:10:38 -0700 | Merge pull request #232 from TrueSightDAO/feat/pipeline-metrics-highlights
f240a25 | 2026-04-21 14:10:03 -0700 | feat(metrics): highlight Meeting Scheduled + Shortlisted in summary
be3e43a | 2026-04-21 13:50:12 -0700 | chore: relocate signature onboarding demo to TrueSightDAO/dao_client (#231)
9b7aea5 | 2026-04-21 13:45:43 -0700 | Merge pull request #229 from TrueSightDAO/feat/pipeline-metrics-snapshot
3683188 | 2026-04-21 13:37:16 -0700 | feat(tdg-inventory): notify treasury-cache-publisher after inventory movements (#230)
9491b1d | 2026-04-21 13:36:39 -0700 | feat(metrics): reuse ORACLE_ADVISORY_PUSH_TOKEN; add clasp mirror
8b9d2d7 | 2026-04-21 12:56:50 -0700 | feat(metrics): GAS to mirror Pipeline Dashboard → ecosystem_change_logs
```

### `dapp` → `dapp`

```
bd02efd | 2026-04-26 14:30:31 -0700 | feat(store history): field reports timeline and optional Edgar attachments (#181)
4dd3169 | 2026-04-26 14:17:26 -0700 | Make inventory holdings page mobile-friendly.
6ba3469 | 2026-04-26 14:16:04 -0700 | Add shared dapp footer links script for reload and GitHub source.
4ada550 | 2026-04-26 14:09:22 -0700 | Cache-bust menu.js (?v=20260426) and bump SW to v6.
2d321df | 2026-04-26 14:07:21 -0700 | Add Inventory Holdings by Manager view and nav link.
2feb9b0 | 2026-04-26 13:55:10 -0700 | Merge pull request #180 from TrueSightDAO/feature/deferred-revisit-later-status
d00e2aa | 2026-04-26 13:45:00 -0700 | Add Hit List status Deferred / Revisit later across nearby, by-status, and history.
d2aa823 | 2026-04-24 15:41:23 -0700 | chat: reclaim mobile vertical space and fix media query cascade (#179)
074828d | 2026-04-24 15:24:58 -0700 | fix: pin chat input to bottom, fix flex layout for mobile
9649675 | 2026-04-24 14:49:36 -0700 | feat: move Governor Chat to top of nav menu
452ebea | 2026-04-24 14:44:46 -0700 | fix(chat): mobile layout — responsive logo, dvh viewport, touch targets
b2a577b | 2026-04-24 14:14:47 -0700 | deploy: point API_BASE_URL to production chatbot.truesight.me
b4449e4 | 2026-04-24 14:08:26 -0700 | feat(chat): render full Markdown in conversation using marked.js
d5c91d7 | 2026-04-24 14:06:50 -0700 | fix(chat): move nav dropdown and badge inside container, fix viewport sizing
4dc0155 | 2026-04-24 14:04:38 -0700 | fix(chat): prevent conversation overflow from container
dcae305 | 2026-04-24 13:38:14 -0700 | feat(chat): friendly access-denied UI for restricted Governor Chat
b12dd27 | 2026-04-24 12:50:01 -0700 | feat: add Governor Chat page (chat.html) + nav link
49e91bf | 2026-04-24 12:16:19 -0700 | feat(dapp): POST signed [RETAIL FIELD REPORT EVENT] to Edgar (#178)
4b0d779 | 2026-04-23 16:57:40 -0700 | Stores by Status: eight-bucket WU/FU bars and segment drill-down (#177)
4fbbf23 | 2026-04-23 16:48:01 -0700 | Nav dropdown: open Store Interaction History in same tab. (#176)
2f4137d | 2026-04-23 16:18:29 -0700 | feat(stores-by-status): pipeline overview with warmup/follow-up touch metrics (#175)
63a084a | 2026-04-23 15:58:18 -0700 | Store interaction history: quick links above results; align drafts copy. (#174)
44c4008 | 2026-04-22 20:07:15 -0700 | Merge pull request #173 from TrueSightDAO/fix/store-history-popout-links
9fa52d4 | 2026-04-22 20:06:47 -0700 | Open Store Interaction History in a new tab from nav and links
854324e | 2026-04-22 20:04:08 -0700 | Merge pull request #172 from TrueSightDAO/fix/stores-gas-cache-footer-links
9453d6b | 2026-04-22 20:03:46 -0700 | Stores: fresh GAS fetches, SW v4, interaction history footer links
752b74e | 2026-04-21 23:50:50 -0700 | perf(dapp): shared DaoMembersCache + cache-first signature check on create_signature (#171)
039d937 | 2026-04-21 23:37:39 -0700 | perf(tdg_balance): cache-first fetch against dao_members.json, GAS fallback (#170)
77bf22c | 2026-04-21 15:55:22 -0700 | Merge pull request #169 from TrueSightDAO/fix/stores-nearby-history-link-new-tab
00900b5 | 2026-04-21 15:55:04 -0700 | fix(dapp): open interaction history link in new tab after store update.
2bdae6d | 2026-04-21 15:46:38 -0700 | Store interaction history: simplify help text; no image uploads planned.
ec236f6 | 2026-04-21 15:44:33 -0700 | Stores Nearby: after status update, link to interaction history for calmer review; clarify photo/Edgar scope in history page help.
6e114f3 | 2026-04-21 15:34:52 -0700 | Store interaction history: document update API scope (no photo upload; not Edgar).
3f67262 | 2026-04-21 15:34:36 -0700 | Stores Nearby: link map and details to interaction history; skip full list refresh after update.
fa2d43b | 2026-04-21 14:58:32 -0700 | feat(dapp): extend treasury-cache reads to report_dao_expenses + shipping_planner (#168)
238c3cf | 2026-04-21 14:49:18 -0700 | test(routes): playwright smoke suite for routes.js direct + proxy modes (#167)
56606dd | 2026-04-21 14:20:01 -0700 | feat(report-inventory-movement): read managers + items from treasury-cache JSON (#166)
c8be32f | 2026-04-21 13:24:39 -0700 | feat(routes): probe-and-flip fallback to Edgar proxy for GFW-blocked users (#165)
9208e61 | 2026-04-21 12:52:09 -0700 | feat(routes): migrate remaining pages + tdg_balance.js to Routes (#164)
64dd953 | 2026-04-21 12:44:40 -0700 | feat(routes): migrate Sunmint module to Routes (#163)
… (truncated)
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
9330f1a | 2026-04-27 08:43:16 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b963a99 | 2026-04-26 07:56:43 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
20d337d | 2026-04-25 07:47:54 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
b8d12d4 | 2026-04-24 08:25:24 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
87ffff1 | 2026-04-23 08:13:33 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
0a3a25f | 2026-04-22 19:28:51 -0700 | chore: refresh Agroverse store inventory snapshot
c318a22 | 2026-04-22 16:28:35 -0700 | chore: refresh Agroverse store inventory snapshot
a24746d | 2026-04-22 14:28:40 -0700 | chore: refresh Agroverse store inventory snapshot
08584bc | 2026-04-22 08:08:49 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
9224db7 | 2026-04-21 14:52:31 -0700 | feat(repackaging-ingest): notify treasury-cache-publisher on successful currency commits (#4)
5909bc7 | 2026-04-21 12:28:38 -0700 | chore: refresh Agroverse store inventory snapshot
0da1893 | 2026-04-20 08:30:22 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
```

### `agroverse_shop` → `agroverse_shop_beta`

```
c5d8696 | 2026-04-20 11:28:06 -0700 | Merge pull request #75 from TrueSightDAO/feature/rename-start-script
0ce62b7 | 2026-04-20 11:27:55 -0700 | Rename start-local-server.sh to start_local.sh (standardize across repos)
```

### `iching_oracle` → `oracle`

```
546dbd9 | 2026-04-19 20:59:22 -0700 | fix(oracle): wrap long tokens in advisory panel; prevent overflow (#7)
9ca7ab8 | 2026-04-19 20:57:54 -0700 | feat(oracle): switch advisor to Claude with prompt caching; revised prompt (#6)
3ae6cfa | 2026-04-19 20:44:13 -0700 | feat(oracle): surface iPhone reminder intents pending since last Mac sync (#5)
```

### `Cypher-Defense` → `Cypher-Defense`

```
_(no commits on origin/master in window)_
```

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-04-27T023204Z_store-history-timelines-way-home-shop-onboarded.md`

- **posted_at_utc:** `2026-04-27T02:32:04Z`  
- **slug:** `store-history-timelines-way-home-shop-onboarded`  
- **Message 1 excerpt (first two non-empty lines):**

  A productive week on the DApp and outreach front: store interaction history gained field report timelines, a new partner (The Way Home Shop) was onboarded for ceremonial cacao, and several quality-of-life fixes landed across inventory, mobile, and the sales pipeline.
  - Store Interaction History now shows a field reports timeline with optional Edgar attachments — contributors can see the full picture of store touchpoints in one place.

### `beer-hall_2026-04-26T023006Z_governor-chat-live-retail-field-reports-member-cache.md`

- **posted_at_utc:** `2026-04-26T02:30:06Z`  
- **slug:** `governor-chat-live-retail-field-reports-member-cache`  
- **Message 1 excerpt (first two non-empty lines):**

  A busy week across the DApp, sales tooling, and contributor infrastructure: Governor Chat shipped to production, retail field reporting landed, and member identity caching cut load on the signature flow.
  - Governor Chat is live on the DApp (chat.html) — token-gated with a friendly access-denied screen, full Markdown rendering, and pinned mobile input; promoted to the top of the nav menu.

### `beer-hall_2026-04-25T020706Z_governor-chat-blog-blitz-retail-field-reports.md`

- **posted_at_utc:** `2026-04-25T02:07:06Z`  
- **slug:** `governor-chat-blog-blitz-retail-field-reports`  
- **Message 1 excerpt (first two non-empty lines):**

  Big week for contributor-facing tools and narrative: Governor Chat launched on the DApp, two new blog posts shipped, and a Retail Field Report webhook now lets contributors log store visits directly from their phones.
  - Governor Chat is live at dapp.truesight.me/chat.html — token-gated, mobile-optimised, with full Markdown rendering; moved to top of nav.

---

## Recent retail field reports (DApp store status updates)

- **`20260426T224831Z.json`** — `2026-04-26T22:48:31Z`  
  **The Way Home Shop – Metaphysical Store in SE Portland** → `AI: Prospect replied` (was `AI: Prospect replied`) | type: Metaphysical/Spiritual | sig: success
  _Final test_

- **`20260426T224042Z.json`** — `2026-04-26T22:40:43Z`  
  **The Way Home Shop – Metaphysical Store in SE Portland** → `AI: Prospect replied` (was `AI: Prospect replied`) | type: Metaphysical/Spiritual | sig: success
  _teting_

- **`20260424T201819Z.json`** — `2026-04-24T20:18:19Z`  
  **** → `` (was `—`) | sig: success

- **`20260424T201629Z.json`** — `2026-04-24T20:16:29Z`  
  **** → `` (was `—`) | sig: success

- **`20260424T200731Z.json`** — `2026-04-24T20:07:32Z`  
  **** → `` (was `—`) | sig: success

---

## Sheet evidence (sales)

_Canonical layouts: `tokenomics/SCHEMA.md` — **Monthly Statistics** on the main ledger; **QR Code Sales** on Telegram & Submissions. Figures are copied as-is from Sheets; verify before financial decisions._

### `Monthly Statistics` (last **14** non-empty rows)

| Year-Month | Monthly USD | Cumulative USD | Last updated |
|------------|-------------|------------------|---------------|
| 2025-03 | 1010 | 3854.96 | 2025-12-07 19:14:46 |
| 2025-04 | 1393.09 | 5248.05 | 2025-12-07 19:14:46 |
| 2025-05 | 825.37 | 6073.42 | 2025-12-07 19:14:46 |
| 2025-06 | 1552.45386 | 7625.87386 | 2025-12-07 19:14:46 |
| 2025-07 | 731 | 8356.87386 | 2025-12-07 19:14:46 |
| 2025-08 | 1011.96 | 9368.83386 | 2025-12-07 19:14:46 |
| 2025-09 | 734.72 | 10103.55386 | 2025-12-07 19:14:46 |
| 2025-10 | 595.22 | 10698.77386 | 2025-12-07 19:14:46 |
| 2025-11 | 268.97 | 10967.74386 | 2025-12-07 19:14:46 |
| 2025-12 | 1380.88 | 12348.62386 | 12/31/2025 |
| 2026-01 | 1063.94 | 13412.56386 | 1/31/2026 18:52:06 |
| 2026-02 | 144.42 | 13556.98386 | 2/28/2026 18:50:17 |
| 2026-03 | 273.97 | 13830.95386 | 3/31/2026 19:51:02 |
| 2026-04 | 445.65 | 14276.60386 | 4/27/2026 1:51:53 |

### `QR Code Sales` (up to **25** rows; `Sales Date` ≥ `2026-04-20`; scanned last **327** data rows)

| Sales date | Price | Currency / product | Status | QR (trunc.) | Stripe (suffix) | Remarks (trunc.) |
|-------------|-------|--------------------|--------|-------------|-------------------|--------------------|
| 2026-04-21 | 10 | 81% Dark Chocolate Bar 50grams - Oscar … | TOKENIZED | 2024OSR_81PB_20260412_11 | — | — |
| 2026-04-21 | 10 | 81% Dark Chocolate Bar 50grams - Santa … | TOKENIZED | 2023SA_81PB_20260412_4 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_35 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_34 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_33 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_32 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_31 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_30 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_29 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_26 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251124_25 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - Alibaba:… | TOKENIZED | 2024OSCAR_20251124_23 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - Alibaba:… | TOKENIZED | 2024OSCAR_20251124_22 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - Alibaba:… | TOKENIZED | 2024OSCAR_20251124_21 | — | — |
| 2026-04-23 | — | — | IGNORED | — | — | IGNORED: Duplicate QR code already on QR Code Sales when this message w… |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251108_3 | — | — |
| 2026-04-23 | 17 | Ceremonial Cacao Kraft Pouch - 20250219… | TOKENIZED | 2024OSCAR_20251102_9 | — | — |
| 2026-04-24 | 23.97 | Ceremonial Cacao Kraft Pouch - Alibaba:… | TOKENIZED | 2024OSCAR_20260121_13 | zuLBUwzHvpjt | Stripe checkout (online) |

_Source IDs: main ledger `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, submissions `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`._

---

## Recent agent notes (`agentic_ai_context/notes/`)

_No `.md` / `.txt` under `notes/` modified in this window._

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
