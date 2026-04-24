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

- Generated (UTC): `2026-04-24T16:51:11Z`
- Look-back: **7** calendar days (`2026-04-17` → today UTC)
- Curated clone set: **12** repos (same table as Beer Hall preview)

---

## Growth goals (year / quarter)

| Goal | Target | Actual | % | Deadline | Days left | Pace |
|------|--------|--------|---|----------|-----------|------|
| 2026 QR Code Sales | $40,000 | — | — | `2026-12-31` | 251 | — |
| USA Agroverse Partners | 100 | — | — | `2026-12-31` | 251 | — |

_Notes: (live fetch skipped: `No module named 'gspread'`)_

---

## Operator metrics (pipeline funnel, auto-synced)

_Auto-synced from the Pipeline Dashboard tab of the Holistic Hit List workbook._
_Do not edit by hand — see `google_app_scripts/pipeline_metrics_snapshot/` in tokenomics._

- Generated (UTC): `2026-04-21T21:15:55.298Z`
- Source: [Pipeline Dashboard](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=1606881029)
- Total stores tracked: **516**
- Partnered (north-star): **13**
- Meeting Scheduled: **1**
- Shortlisted: **3**

## Funnel by status (curated order)

- AI: Enrich — manual: 68  (#3)
- AI: Contact Form found: 76  (#4)
- AI: Photo rejected: 107  (#7)
- AI: Photo needs review: 39  (#8)
- AI: Warm up prospect: 65  (#9)
- Not Appropriate: 71  (#11)
- Contacted: 4  (#12)
- Shortlisted: 3  (#13)
- Manager Follow-up: 26  (#14)
- Meeting Scheduled: 1  (#16)
- Instagram Followed: 11  (#17)
- On Hold: 17  (#18)
- **Partnered: 13**  (#19)
- Rejected: 14  (#20)
- Followed Up: 1  (#21)

---

## CONTEXT_UPDATES (append-only, heuristic highlights)

_Lines in window matching configured names or status keywords:_

- 2026-04-19 | claude | **iOS Reminders → oracle pipeline:** New Rails endpoint **`POST https://edgar.truesight.me/oracle/reminders_sync`** in **`sentiment_importer`** (`app/controllers/oracle/reminders_sync_controller.rb`). Bearer-auth'd, accepts any POST body (any content-type — iOS Shortcuts sends iCalendar VTODO despite JSON header) and archives verbatim to **`ecosystem_change_logs/reminders_raws/<UTC-timestamp>.json`** via GitHub Contents API. Credentials (`oracle_sync_token`, `github_pat`) in `config/application.rb` (not env). The oracle GAS at `oracle.truesight.me` still reads `ecosystem_change_logs/reminders/current.json` — downstream parser from raw archive to current.json is TODO.
- 2026-04-22 | cursor | **Newsletter workbook `1ed3q3…`:** IMPORTRANGE mirrors (Subscribers, QR codes, SKUs, Currencies) + **Email 360** (lookup email → sends, QR, SKUs via ledger slug→Shipment, subscriber row, campaigns) + **Workbook context** tab. Script **`market_research/scripts/setup_newsletter_workbook_mirrors.py`**. **`AGROVERSE_NEWSLETTER_WORKFLOW.md`** + **`send_newsletter.py`** (`NEWSLETTER_LOG_SPREADSHEET_ID`) + **`sentiment_importer`** `Gdrive::NewsletterEmails` same ID; removed stray **`binding.pry`** in **`newsletter_controller#click`**.
- 2026-04-24 | cursor | **Hit List retailer pipeline — email tracking + reconcile:** **sentiment_importer (Edgar)** — `GET /email_agent/open.gif` + `/email_agent/click` + `Gdrive::EmailAgentDrafts` (merged PR **#1031**). **go_to_market** — `--track-clicks` / **Open** & **Click through** on **Email Agent Drafts**; **`regenerate_pending_email_agent_draft_tracking.py`** for MIME refresh; **`reconcile_email_agent_drafts_stale_sent.py`** when Gmail is **SENT** but the sheet still says **`pending_review`**. **`HIT_LIST_CREDENTIALS.md`**; **`WORKSPACE_CONTEXT.md`** §4 Hit List bullet.

_All dated lines on/after 2026-04-17_ (8):

- 2026-04-19 | claude | **Beer Hall + advisory snapshot automation:** WhatsApp posting via OpenClaw **retired**; digest is now archive-only. Added **`market_research/.github/workflows/advisory-snapshot-refresh.yml`** (every 6 h) and **`beer-hall-digest-daily.yml`** (00:00 UTC daily, auto-merges PRs). New **`market_research/scripts/draft_beer_hall_digest.py`** calls Claude Sonnet 4.6 via the anthropic SDK to draft Message 1 + Message 2 from the preview + latest 2 archives as few-shot examples. New repo secret: **`ORACLE_ADVISORY_PUSH_TOKEN`** (fine-grained PAT, Contents+PR Read/Write on `ecosystem_change_logs` and `agentic_ai_context`). `ANTHROPIC_API_KEY` also added. **`WORKSPACE_CONTEXT.md` §3d** rewritten; **`OPENCLAW_WHATSAPP.md`** Beer Hall section marked legacy.
- 2026-04-19 | claude | **iOS Reminders → oracle pipeline:** New Rails endpoint **`POST https://edgar.truesight.me/oracle/reminders_sync`** in **`sentiment_importer`** (`app/controllers/oracle/reminders_sync_controller.rb`). Bearer-auth'd, accepts any POST body (any content-type — iOS Shortcuts sends iCalendar VTODO despite JSON header) and archives verbatim to **`ecosystem_change_logs/reminders_raws/<UTC-timestamp>.json`** via GitHub Contents API. Credentials (`oracle_sync_token`, `github_pat`) in `config/application.rb` (not env). The oracle GAS at `oracle.truesight.me` still reads `ecosystem_change_logs/reminders/current.json` — downstream parser from raw archive to current.json is TODO.
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
d3fcf05 | 2026-04-23 18:28:22 -0700 | feat(newsletter): workbook mirrors, Email 360, and Workbook context tab. (#70)
3fc50d9 | 2026-04-23 18:17:43 -0700 | Merge pull request #69 from TrueSightDAO/feat/email-agent-reconcile-stale-sent-sheet
492a734 | 2026-04-23 18:16:35 -0700 | feat(email-agent): reconcile Email Agent Drafts when Gmail already SENT
eb33521 | 2026-04-23 18:04:31 -0700 | Newsletter send log: use dedicated workbook ID (match Edgar).
dd2d1c4 | 2026-04-23 18:04:25 -0700 | Merge pull request #68 from TrueSightDAO/feat/regenerate-email-agent-draft-tracking
ae01938 | 2026-04-23 18:04:00 -0700 | feat(email-agent): regenerate pending drafts with tracking MIME
c8dc570 | 2026-04-23 17:44:51 -0700 | Merge pull request #67 from TrueSightDAO/feat/email-agent-track-clicks-and-sheet-columns
60aeb26 | 2026-04-23 17:44:38 -0700 | feat(email-agent): --track-clicks, HTML helper, Drafts Open/Click columns on append
7224724 | 2026-04-23 17:43:54 -0700 | migrate_newsletter_emails_sheet: use gspread update(values=, range_name=) to silence deprecation.
9f9d94d | 2026-04-23 17:41:08 -0700 | Add script to migrate Agroverse News Letter Emails tab to new workbook.
a9388ce | 2026-04-23 17:30:45 -0700 | Merge pull request #66 from TrueSightDAO/feat/email-agent-drafts-engagement-followup-suggestion-id
791f424 | 2026-04-23 17:30:09 -0700 | feat(email-agent): Drafts Open/Click, Follow Up suggestion_id and sync port
8224b8d | 2026-04-23 16:18:21 -0700 | feat(hit-list): email follow-up tracking, AU/AV on new rows, discard cadence bypass (#65)
c28d5ef | 2026-04-21 13:45:46 -0700 | Merge pull request #63 from TrueSightDAO/feat/advisory-metrics-from-eco
111a192 | 2026-04-21 13:30:00 -0700 | feat(newsletter): add --track-clicks link rewriting through Edgar (#64)
2afe693 | 2026-04-21 12:56:55 -0700 | fix(advisory): read metrics from ecosystem_change_logs; drop CONSTRAINTS
5c7a127 | 2026-04-20 23:08:27 -0700 | Merge pull request #62 from TrueSightDAO/fix/beer-hall-workflow-commit-beer-hall-files
d163ffc | 2026-04-20 23:08:07 -0700 | beer-hall-digest-daily: commit beer_hall/ files before advisory step
e4d046e | 2026-04-20 12:11:18 -0700 | Merge pull request #61 from TrueSightDAO/feat/export-google-docs-workflow
95adadc | 2026-04-20 12:10:54 -0700 | Add export-google-docs workflow — daily Markdown mirror of partnership Docs
4465255 | 2026-04-20 11:28:13 -0700 | feat(newsletter): reusable Gmail send/draft flow with sheet logging + opt-in open tracking (#60)
179d390 | 2026-04-19 15:27:38 -0700 | Merge pull request #59 from TrueSightDAO/chore/drop-whatsapp-retirement-header
9e6d351 | 2026-04-19 15:27:22 -0700 | draft_beer_hall_digest: drop redundant WhatsApp-retired header
dbee4af | 2026-04-19 15:10:29 -0700 | Merge pull request #58 from TrueSightDAO/chore/beer-hall-daily-cadence
1641850 | 2026-04-19 15:10:14 -0700 | Beer Hall digest: daily cadence + auto-merge PRs
9c68b19 | 2026-04-19 15:00:16 -0700 | Merge pull request #57 from TrueSightDAO/feat/advisory-beer-hall-automation
e2bce7d | 2026-04-19 14:59:31 -0700 | Automate advisory snapshot refresh + weekly Beer Hall digest
b9c368d | 2026-04-19 14:38:29 -0700 | Merge pull request #56 from TrueSightDAO/chore/beer-hall-retire-openclaw-send
b5124bb | 2026-04-19 14:38:03 -0700 | Beer Hall: retire OpenClaw WhatsApp send; archive + advisory-snapshot only
2ce3e97 | 2026-04-19 13:30:21 -0700 | feat(advisory): render Purpose & Mission north-star block at top of snapshot (#55)
dabd348 | 2026-04-18 14:59:32 -0700 | fix(advisory): read filter from source, add starts_with predicate (#54)
e607577 | 2026-04-18 14:18:25 -0700 | feat(advisory): add operator-curated strategic blocks to ADVISORY_SNAPSHOT (#53)
5440b17 | 2026-04-18 11:53:45 -0700 | Merge pull request #52 from TrueSightDAO/add-oracle-cypher-defense-repos
bea9b7b | 2026-04-18 11:53:15 -0700 | Add oracle and Cypher-Defense repos to REPOS poll lists
8b4e413 | 2026-04-17 16:16:10 -0700 | Merge pull request #51 from TrueSightDAO/fix/telegram-digest-edgar-parser
b50b0f2 | 2026-04-17 16:15:50 -0700 | fix(digest): parse Edgar event fields in Telegram log helper
```

### `agentic_ai_context` → `agentic_ai_context`

```
6eaae20 | 2026-04-24 07:14:28 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
fe3780d | 2026-04-24 07:14:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
4a726fd | 2026-04-24 01:31:30 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
a49b6e0 | 2026-04-24 01:31:29 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
518f860 | 2026-04-23 20:58:05 -0700 | chore(previews): refresh Beer Hall preview (2026-04-24 UTC)
a61c04e | 2026-04-23 20:58:03 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
34905e7 | 2026-04-23 19:25:50 -0700 | Merge pull request #47 from TrueSightDAO/auto/advisory-refresh-2026-04-24
4711fff | 2026-04-24 02:25:41 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-24 UTC)
c8f8124 | 2026-04-23 18:33:59 -0700 | docs(newsletter): Email 360 purpose, limits, and regeneration (§1b). (#46)
ef734c6 | 2026-04-23 18:29:08 -0700 | docs(newsletter): dedicated workbook, Email 360, mirrors (#45)
e5d3620 | 2026-04-23 18:17:46 -0700 | Merge pull request #44 from TrueSightDAO/feat/context-email-agent-reconcile-2026-04-24
786bcb2 | 2026-04-23 18:16:34 -0700 | docs: Hit List email-agent Edgar tracking and reconcile scripts
432962d | 2026-04-23 17:21:17 -0700 | Merge pull request #43 from TrueSightDAO/docs/clasp-deploy-push-then-deploy-convention
3dbc605 | 2026-04-23 17:20:56 -0700 | docs(tokenomics): treat 'clasp deploy' as push then deploy
5e8a79b | 2026-04-23 12:50:46 -0700 | chore(previews): refresh Beer Hall preview (2026-04-23 UTC)
70f4416 | 2026-04-23 12:50:45 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
f2919bc | 2026-04-23 07:19:49 -0700 | chore(previews): refresh Beer Hall preview (2026-04-23 UTC)
5dbde21 | 2026-04-23 07:19:48 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
a43e204 | 2026-04-23 01:19:38 -0700 | chore(previews): refresh Beer Hall preview (2026-04-23 UTC)
85d091e | 2026-04-23 01:19:37 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
5c301b9 | 2026-04-22 20:54:28 -0700 | chore(previews): refresh Beer Hall preview (2026-04-23 UTC)
4acfa00 | 2026-04-22 20:54:27 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
65e7610 | 2026-04-22 19:25:03 -0700 | Merge pull request #42 from TrueSightDAO/auto/advisory-refresh-2026-04-23
c572e23 | 2026-04-23 02:24:54 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-23 UTC)
7be31ee | 2026-04-22 12:47:15 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
6b06117 | 2026-04-22 12:47:14 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
48ece2f | 2026-04-22 07:16:26 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
685f1a4 | 2026-04-22 07:16:24 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
0fcc9c1 | 2026-04-22 01:15:27 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
2480a43 | 2026-04-22 01:15:26 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
7523efd | 2026-04-22 00:46:44 -0700 | docs: correct TrueChain status — designed, NOT running (v0.3) (#41)
cc8d63a | 2026-04-22 00:41:17 -0700 | docs(blockchain-anchoring): v0.2 — TrueChain's value is conditional, not assumed (#40)
7313b77 | 2026-04-22 00:22:34 -0700 | docs(blockchain-anchoring): add two mermaid diagrams for non-technical readers (#39)
cff1715 | 2026-04-22 00:12:54 -0700 | docs: internal proposal for blockchain-anchoring DAO caches + Telegram logs (#38)
a9f220c | 2026-04-21 20:47:34 -0700 | chore(previews): refresh Beer Hall preview (2026-04-22 UTC)
76536c7 | 2026-04-21 20:47:33 -0700 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
03d730f | 2026-04-21 19:13:21 -0700 | Merge pull request #37 from TrueSightDAO/auto/advisory-refresh-2026-04-22
8c141a6 | 2026-04-22 02:13:11 +0000 | chore(advisory): refresh ADVISORY_SNAPSHOT (2026-04-22 UTC)
79ed534 | 2026-04-21 16:09:07 -0700 | docs: AI agent [CONTRIBUTION EVENT] convention (dao_client + context) (#36)
c492992 | 2026-04-21 14:39:30 -0700 | docs: dao_client — mark auth flow validated, document modules/ (#35)
… (truncated)
```

### `tokenomics` → `tokenomics`

```
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
20bf43c | 2026-04-19 13:11:19 -0700 | Merge pull request #228 from TrueSightDAO/feat/inventory-api-agl-unit-cost-lookup
b9103e5 | 2026-04-19 13:10:51 -0700 | feat(inventory-api): resolve AGL Balance unit_cost from main Currencies tab
cfd760f | 2026-04-18 14:17:53 -0700 | perf(gas): fix 30-min trigger timeouts on telegram log processors (#227)
c421451 | 2026-04-18 13:21:19 -0700 | feat(agroverse-qr): multi-item Stripe session link via column Z on QR codes (#226)
4fc9491 | 2026-04-17 16:03:18 -0700 | feat(agroverse-qr): migrate qr_code_web_service to admin@truesight.me and consolidate owner emails (#225)
```

### `dapp` → `dapp`

```
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
6b337ee | 2026-04-21 12:43:10 -0700 | feat(routes): migrate Inventory & Sales module to Routes (#162)
c539745 | 2026-04-21 12:32:47 -0700 | feat(routes): migrate Identity & Governance module to Routes (#161)
d6ca6a5 | 2026-04-21 12:26:18 -0700 | feat(routes): migrate report_contribution.html to Routes (Contributions module) (#160)
1439821 | 2026-04-21 12:24:58 -0700 | feat(routes): centralize endpoints in routes.js + migrate submit_feedback POC (#159)
ec3cb4a | 2026-04-20 11:30:11 -0700 | Merge pull request #158 from TrueSightDAO/feature/rename-start-script
ef8bb26 | 2026-04-20 11:30:00 -0700 | Rename serve_local.sh to start_local.sh, default port 8081
e0f868c | 2026-04-18 21:39:36 -0700 | Merge pull request #157 from TrueSightDAO/feat/repackaging-planner-edgar-route
ba2ccea | 2026-04-18 21:39:05 -0700 | feat(repackaging_planner): route through Edgar with signed payload + UX rewrite
f89e75e | 2026-04-17 16:03:20 -0700 | feat(batch-qr): update GAS URL to new admin@truesight.me project (#156)
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
b8d12d4 | 2026-04-24 08:25:24 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
87ffff1 | 2026-04-23 08:13:33 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
0a3a25f | 2026-04-22 19:28:51 -0700 | chore: refresh Agroverse store inventory snapshot
c318a22 | 2026-04-22 16:28:35 -0700 | chore: refresh Agroverse store inventory snapshot
a24746d | 2026-04-22 14:28:40 -0700 | chore: refresh Agroverse store inventory snapshot
08584bc | 2026-04-22 08:08:49 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
9224db7 | 2026-04-21 14:52:31 -0700 | feat(repackaging-ingest): notify treasury-cache-publisher on successful currency commits (#4)
5909bc7 | 2026-04-21 12:28:38 -0700 | chore: refresh Agroverse store inventory snapshot
0da1893 | 2026-04-20 08:30:22 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
ac9568e | 2026-04-19 21:32:47 +0000 | chore: refresh store and partner inventory snapshots [skip ci]
89d4c64 | 2026-04-19 14:03:03 -0700 | feat(gas): add editor-runnable wrappers for repackaging-currency-ingest (#3)
0f5ccf7 | 2026-04-19 13:37:30 -0700 | chore(inventory): repackaging composition 67c88267-b41c-4eab-8ef5-d5be48854d65
9353975 | 2026-04-19 13:37:29 -0700 | chore(inventory): refresh currencies.json (repackaging ingest)
1f830fc | 2026-04-18 21:40:40 -0700 | Merge pull request #2 from TrueSightDAO/feat/repackaging-currency-ingest-gas
d6f5f90 | 2026-04-18 21:40:31 -0700 | feat(gas): add repackaging-currency-ingest Apps Script + doGet processor
c30b32f | 2026-04-17 11:28:50 -0700 | chore: refresh Agroverse store inventory snapshot
```

### `agroverse_shop` → `agroverse_shop_beta`

```
c5d8696 | 2026-04-20 11:28:06 -0700 | Merge pull request #75 from TrueSightDAO/feature/rename-start-script
0ce62b7 | 2026-04-20 11:27:55 -0700 | Rename start-local-server.sh to start_local.sh (standardize across repos)
6090cab | 2026-04-19 15:57:44 -0700 | chore(agl6): live YouTube embed for São Jorge hot chocolate (gw2vIxPCcyQ)
567db30 | 2026-04-19 15:41:11 -0700 | publish sao jorge fazenda (#73)
```

### `iching_oracle` → `oracle`

```
546dbd9 | 2026-04-19 20:59:22 -0700 | fix(oracle): wrap long tokens in advisory panel; prevent overflow (#7)
9ca7ab8 | 2026-04-19 20:57:54 -0700 | feat(oracle): switch advisor to Claude with prompt caching; revised prompt (#6)
3ae6cfa | 2026-04-19 20:44:13 -0700 | feat(oracle): surface iPhone reminder intents pending since last Mac sync (#5)
67bd3bc | 2026-04-17 15:32:00 -0700 | Merge pull request #4 from TrueSightDAO/feature/oracle-gas-version-control
6ed09fb | 2026-04-17 15:25:57 -0700 | feat(gas): version-control oracle advisory bridge GAS source
```

### `Cypher-Defense` _(no clone)_

---

## Recent Beer Hall archives (newest entries)

### `beer-hall_2026-04-21T061005Z_whitepaper-oracle-claude-email-marketing-live.md`

- **posted_at_utc:** `2026-04-21T06:10:05Z`  
- **slug:** `whitepaper-oracle-claude-email-marketing-live`  
- **Message 1 excerpt (first two non-empty lines):**

  Busy week across the stack — whitepaper accuracy, Oracle upgrades, email marketing scaffolding, São Jorge farm page, and ongoing AWS security follow-through.
  - Whitepapers updated to be agentic-AI-friendly: Gas Fee section dropped, Edgar/TrueChain/Oracle terms defined, TrueTech Inc correctly distinguished from Brazilian suppliers, Beer Hall described as archive-only, and 31 broken partnership-agreement links fixed with direct Google Doc URLs.

### `beer-hall_2026-04-19T213956Z_retire-whatsapp-oracle-and-reminders-live.md`

- **posted_at_utc:** `2026-04-19T21:39:56Z`  
- **slug:** `retire-whatsapp-oracle-and-reminders-live`  
- **Message 1 excerpt (first two non-empty lines):**

  OpenClaw × Cursor digest — retired from WhatsApp posting; archive-only for oracle / feed context (not a manual post from Gary)
  - Cybernetic Oracle is live. oracle.truesight.me now draws a hexagram and passes DAO state (advisory snapshot, strategic blocks, open reminders) to Grok for a grounded reading. GAS backend version-controlled.

### `beer-hall_2026-04-18T223617Z_qr-email-migration-admin-truesight-advisory-goals.md`

- **posted_at_utc:** `2026-04-18T22:36:17Z`  
- **slug:** `qr-email-migration-admin-truesight-advisory-goals`  
- **Message 1 excerpt (first two non-empty lines):**

  *OpenClaw × Cursor — daily state of the DAO (not a manual post from Gary)*
  - Owners buying multiple QR-coded items in a single Stripe checkout now get ONE onboarding email listing all their tracking links, instead of one email per item

---

## Open reminders (macOS `rem` — action items)

_Open (not done) items from Reminders.app (`rem list --incomplete -o json`). When the user asks for **oracle response options**, propose **1–3** concrete next steps that honestly connect the hexagram reading to these **actionable** items where it fits; do **not** invent due dates or claim items are done._
_Showing **60** of **120** open reminders (cap `--rem-limit`)._

| Title | List | Due (date) | Flagged | Notes (trunc.) |
|-------|------|------------|---------|------------------|
| Follow up with USPS claims | Reminders | `2025-04-07` | — | — |
| Send Matthew the Dizajn | Reminders | `2025-09-11` | — | — |
| Get cursor to look into the AWS charges still coming to my account | Reminders | `2026-01-29` | — | — |
| Look at the influencer platform that a surface and a beer hall | Reminders | `2026-01-29` | — | — |
| Spinner an instance for the RAG architecture | Reminders | `2026-01-29` | — | — |
| Look to order photos of the storage shop listed by AI | Reminders | `2026-04-21` | — | — |
| Review my Clock subscription package | Reminders | `2026-05-09` | — | — |
| [FEATURE] Allow the module where people can add their own photo for the… | Reminders | `—` | — | — |
| [priority] Look through AI generated emails, edit and send them out | Reminders | `—` | — | — |
| [priority] Post Instagram gratitude to Raven | Reminders | `—` | — | — |
| [Priority] Research on Santa Fe Fazenda In International Airport | Reminders | `—` | — | — |
| [priority] review Fatima suggestion and then revert to Fatima | Reminders | `—` | — | — |
| [priority] The store interaction history is missing some status that's … | Reminders | `—` | — | — |
| [priority] Write a blocked post about heavy metals | Reminders | `—` | — | — |
| Allow remark to be expendable when retractable in mobile | Reminders | `—` | — | — |
| Allow to name the tree | Reminders | `—` | — | — |
| Allow upload of MH for the store nearby status submission | Reminders | `—` | — | — |
| Allow upload of MH to the stores nearby status submission | Reminders | `—` | — | — |
| Andrew is pretty impressed by the fact that it is a community project | Reminders | `—` | — | — |
| Build up a dashboard for all the trees belong to the same email address | Reminders | `—` | — | — |
| Buy the battery back up tomorrow on amazon.com | Reminders | `—` | — | — |
| Check the time and Spam packaging to cut out as well as expenses | Reminders | `—` | — | — |
| Check when the last day they bought | Reminders | `—` | — | — |
| Check when was the last time they bought and then sent a pull-up email … | Reminders | `—` | — | — |
| Choclate has an API block post | Reminders | `—` | — | — |
| Consult external source for SWOT analysis in advisory | Reminders | `—` | — | — |
| Create a donation receipt | Reminders | `—` | — | — |
| Create a mobile app that venue owners can use to set the price | Reminders | `—` | — | — |
| Create a mod for registering new members | Reminders | `—` | — | — |
| Create a route for the wine Kenosha | Reminders | `—` | — | — |
| Create an expected physical pop-up expansion | Reminders | `—` | — | — |
| Create an instance of the iOS native app using cursor AI | Reminders | `—` | — | — |
| Create the volunteer estimator for the different places that are sellin… | Reminders | `—` | — | — |
| Create tutorial for Deckers | Reminders | `—` | — | — |
| Do engine rate to see what's up with the engine lights | Reminders | `—` | — | — |
| Do the 2 x 2 matrix for the users and the products that they were intro… | Reminders | `—` | — | — |
| Download Prince of tights | Reminders | `—` | — | — |
| Drop Jennifer as well as Founder Haus from the past | Reminders | `—` | — | — |
| Easy post calculate Sweet spot for postal rate across all the different… | Reminders | `—` | — | — |
| Explore this https://www.linkedin.com/posts/%7Efinn_today-were-proud-to… | Reminders | `—` | — | — |
| Extend debt with the transforming of inventory from one | Reminders | `—` | — | — |
| Figure out how to be a reasonable schedule by another four weeks from $… | Reminders | `—` | — | — |
| Figure out how to social proof like the Michelin star list | Reminders | `—` | — | — |
| Follow up with all the Desert resell us on April 16 after our Cacao com… | Reminders | `—` | — | — |
| Follow up with andrea | Reminders | `—` | — | — |
| Follow up with Fatima on Wednesday regarding the quotation from Santa A… | Reminders | `—` | — | — |
| Follow up with Matthews on Monday regarding the follow up with the Omeg… | Reminders | `—` | — | — |
| Follow up with the dude that dust incense from Nathan's fire | Reminders | `—` | — | — |
| Follow up with the people on our email list | Reminders | `—` | — | — |
| Garfield Street and box Canyon Road | Reminders | `—` | — | — |
| Get Claude look into for the gate up action for visual consistency test… | Reminders | `—` | — | — |
| Get Hwang to send over the USDANOP certification for the new part | Reminders | `—` | — | — |
| Get Ken a shirt | Reminders | `—` | — | — |
| Go visit the board stores to see and figure out why the seller rate is … | Reminders | `—` | — | — |
| Have the cloth maybe extend cipher defense to do a radar detection of t… | Reminders | `—` | — | — |
| Hey the right thing to do is different than every single compact so the… | Reminders | `—` | — | — |
| https://a.co/d/0jhwOqgO | Reminders | `—` | — | U Organic Dark Chocolate 10 Bars x 1.58 Ounce 85% Cacao - Kosher Gluten & Allergen Free Vegan -… |
| I collect $100 for the two bath soap | Reminders | `—` | — | — |
| Include the CEPOTX fund video | Reminders | `—` | — | — |
| Include the inventory level as well as Kirsten and Matheus special posi… | Reminders | `—` | — | — |

### Suggestion seeds (titles only)

- Follow up with USPS claims
- Send Matthew the Dizajn
- Get cursor to look into the AWS charges still coming to my account
- Look at the influencer platform that a surface and a beer hall
- Spinner an instance for the RAG architecture
- Look to order photos of the storage shop listed by AI
- Review my Clock subscription package
- [FEATURE] Allow the module where people can add their own photo for the front page cover of the chocolate bar
- [priority] Look through AI generated emails, edit and send them out
- [priority] Post Instagram gratitude to Raven
- [Priority] Research on Santa Fe Fazenda In International Airport
- [priority] review Fatima suggestion and then revert to Fatima
- [priority] The store interaction history is missing some status that's why it's not getting populated
- [priority] Write a blocked post about heavy metals
- Allow remark to be expendable when retractable in mobile
- Allow to name the tree
- Allow upload of MH for the store nearby status submission
- Allow upload of MH to the stores nearby status submission
- Andrew is pretty impressed by the fact that it is a community project
- Build up a dashboard for all the trees belong to the same email address
- Buy the battery back up tomorrow on amazon.com
- Check the time and Spam packaging to cut out as well as expenses
- Check when the last day they bought
- Check when was the last time they bought and then sent a pull-up email to get feedback and introduced new product

_… **60** more open reminders not shown (raise `--rem-limit`)._

---

## Recent agent notes (`agentic_ai_context/notes/`)

_No `.md` / `.txt` under `notes/` modified in this window._

---

## Pointers

- **Stable orientation:** `ecosystem_change_logs/advisory/BASE.md` (also linked from `advisory/index.json`).
- Dated snapshots + manifest: [`TrueSightDAO/ecosystem_change_logs`](https://github.com/TrueSightDAO/ecosystem_change_logs) `advisory/`
- Human / WhatsApp evidence pack: `market_research/scripts/generate_beer_hall_preview.py`
- Sheet layouts / tabs: `tokenomics/SCHEMA.md`
