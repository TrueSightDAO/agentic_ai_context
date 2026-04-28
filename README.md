# Agentic AI Context

This repository holds **workspace context** for AI coding assistants (Claude Code, OpenAI Codex, Gemini CLI, Cursor, etc.). Read the files here to get up to speed on what the entire workspace is about before making changes.

## Onboarding (new to the DAO or Agroverse?)

Clone this repo and give your LLM access to it so it can get up to speed quickly:

```bash
git clone git@github.com:TrueSightDAO/agentic_ai_context.git
cd agentic_ai_context
```

Then point your editor or LLM at this folder (or at least `OPERATING_INSTRUCTIONS.md` → `WORKSPACE_CONTEXT.md` → `PROJECT_INDEX.md`). **Main Ledger repackaging / conversion questions:** read **`LEDGER_CONVERSION_AND_REPACKAGING.md`** when relevant (also linked from `WORKSPACE_CONTEXT.md` §3b). Your AI will have context on the TrueSight DAO, Agroverse (ceremonial cacao, agroverse.shop, reseller partners), Krake, and the rest of the workspace — conventions, credentials reference, and CMO playbook included.

## Contents

| File | Purpose |
|------|---------|
| **OPERATING_INSTRUCTIONS.md** | **Read this first.** Rules for reading and contributing; canonical vs. append-only vs. per-agent. |
| **DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md** | **AI → Edgar `[CONTRIBUTION EVENT]`** — convention: use **`dao_client`** CLI, include **TrueSightDAO GitHub PR URLs**, explicit “what changed” body; credentials in **`dao_client/.env`**. |
| **WORKSPACE_CONTEXT.md** | High-level overview of the workspace: projects, tech stack, relationships, and conventions. |
| **PROJECT_INDEX.md** | Per-project summary: purpose, stack, entry points, and links to credentials/docs. |
| **CONTEXT_UPDATES.md** | Append-only log for agent notes; do not remove or rewrite lines. |
| **notes/** | Per-agent / per-session notes; create files like `cursor_2025-01-29.md`, `claude_session.md`. |
| **AI_SETUP.md** | How to check/install Claude Code, OpenAI Codex, and Gemini CLI on this machine. |
| **GOOGLE_API_CREDENTIALS.md** | Google API credentials, service accounts, OAuth clients, and ledger spreadsheet IDs (workspace-wide). |
| **LEDGER_CONVERSION_AND_REPACKAGING.md** | **Main Ledger** — repackaging / conversion: input & output `Currency`, cost per unit, standard naming template, SCHEMA/API workflow. **Read when the task involves ledger conversion** (see `WORKSPACE_CONTEXT.md` §3b). |
| **CMO_SETH_GODIN.md** | **Agentic AI CMO** — Seth Godin persona and principles; read when doing marketing (copy, positioning, campaigns, growth). Consult this for CMO perspective. |
| **DR_MANHATTAN.md** | **Agentic AI — Dr Manhattan** — Strategic advisor for Agroverse + TrueSight DAO growth; read when doing strategy, priorities, or onboarding. Future use: chatbot for newcomers. |
| **GOVERNANCE_SOURCES.md** | **Governance** — Whitepaper (truesight.me/whitepaper → Google Doc), proposals (GitHub TrueSightDAO/proposals, Realms). Pull whitepaper via `scripts/fetch_whitepaper.py`; browser for Realms. |
| **SYNDICATE_AGREEMENTS.md** | **Syndicate drafting** — Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee. Template and drafts in `notarizations/`. **Read before drafting any AGL agreement.** |
| **scripts/fetch_whitepaper.py** | **API to pull whitepaper** — Fetches whitepaper content (export URL or Google Docs API). Run from `scripts/` with `-o ../WHITEPAPER_SNAPSHOT.md` to write snapshot. |
| **WHITEPAPER_SNAPSHOT.md** | **Main whitepaper** — Snapshot of truesight.me/whitepaper. Refresh with `scripts/fetch_whitepaper.py -o ../WHITEPAPER_SNAPSHOT.md` or `--all -o ../` for all four. |
| **EDGAR_WHITEPAPER_SNAPSHOT.md** | **Edgar whitepaper** — Snapshot of truesight.me/edgar/whitepaper. Refresh with `--which edgar -o ../EDGAR_WHITEPAPER_SNAPSHOT.md` or `--all -o ../`. |
| **AGROVERSE_WHITEPAPER_SNAPSHOT.md** | **Agroverse whitepaper** — Snapshot of truesight.me/agroverse/whitepaper. Refresh with `--which agroverse -o ../` or `--all -o ../`. |
| **SUNMINT_WHITEPAPER_SNAPSHOT.md** | **Sunmint whitepaper** — Snapshot of truesight.me/sunmint/whitepaper. Refresh with `--which sunmint -o ../` or `--all -o ../`. |
| **DAPP_PAGE_CONVENTIONS.md** | **DApp page structure** — Meta tags, Open Graph, Twitter Card, favicon, nav, body/container layout, and UX pointers. **Follow this when creating or editing pages in the dapp repo** so all pages match existing conventions. See also `dapp/UX_CONVENTIONS.md` for loading/error/combobox patterns. |
| **LEAD_LIST_EXTRACTION.md** | **Lead list / Hit List extraction** — How we discover retailer contacts (Playwright → Google Maps/Yelp), extract Instagram, and append to the Hit List Google Sheet. Read when extending or re-running the apothecary discovery workflow. |
| **LAB_REPORT_TRANSLATION.md** | **Lab report translation** — Portuguese lab reports (ANVISA) for Agroverse shipments. Extract PDF text, translate via Grok API, add English summary to shipment page, link to original Portuguese PDF. Read when translating lab reports or adding English summaries to AGL shipment pages. |
| **DOWNLOADS_MEDIA_TO_AGROVERSE.md** | **`~/Downloads` → agroverse.shop** — Videos: analyze/transcribe/dedupe, optional YouTube upload, blog posts + optional Grok transcript polish, thumbnails. Images: copy into `agroverse_shop/assets/images/…`, wire in HTML, **`sync_blog_listing_thumbnails.py`** (no dedicated Downloads watcher). Read when the user drops media in Downloads for the blog. |
| **PRODUCT_DEVELOPMENT_SPECS.md** | **Agroverse physical product specs** — Packaging / copacker / retail checklists in **Google Sheets** (tabs per section); script `market_research/scripts/populate_chocolate_bar_spec_sheet.py` populates rows and applies readable formatting. **Default Drive folder** for new generated Sheets: folder ID `1esYnlwChRmv9-M3ymWYhWMPHRowhOluw`. Read when starting a **new SKU, bar, pouch, or RDB** spec; align suggestions with agroverse.shop + repo. |
| **TRUECHAIN.md** | **TrueChain** — Private blockchain for contributions, transactions, invoices, QR codes, tree plantings, sales. Setup, integration, block explorer (GAS), technical proposal. Includes "For AI Assistants" section. Repo: [TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain). |
| **HIT_LIST_CONTACT_ENRICHMENT.md** | **Hit List — contact enrichment** — `AI: Enrich with contact` queue (`hit_list_enrich_contact.py`), **DApp Remarks** logging (not Hit List **Notes**), shared `hit_list_dapp_remarks_sheet.py`, hourly GitHub Action. Read when extending web/email/form discovery or Hit List automation; **`market_research/HIT_LIST_CREDENTIALS.md`** for CLI and secrets. |
| **AGROVERSE_QR_CODE_BATCH_GENERATION.md** | **Agroverse serialized QR codes** — Main Ledger tab **`Agroverse QR codes`**: naming (**`LA`**, **`CC`**, **`CT`**), columns **A–V**, **`Currencies`!A** linkage for column **I**, **`batch_compiler.py`** + **`to_print/`**, optional Sheets append + column **K** formula. Read before bulk-creating rows or compiling label PNGs. |
| **AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md** | **agroverse.shop new SKU / PDP** — After launching a product page, update **`farms/*/index.html`** and **`shipments/agl*/index.html`** “Products from …” **`item-card`** grids so SKUs are not PDP-only; pointers to **`PRODUCT_CREATION_CHECKLIST.md`** for feeds/Merchant Center. Also documents the **PDP image layout convention** — one hero shot at full container width, supplementary shots in a `.gallery` grid directly below it (never above the hero, no `<figcaption>` — alt text is the caption). |
| **RETAILER_ONBOARDING_PLAYBOOK.md** | **Retail partner — field-visit / sales** flow that ends at `Status = Partnered`. Use when running an in-person visit or first cold-email cycle for a holistic / apothecary / ceremonial-cacao retailer. Stage gates (Research → Shortlisted → Contacted → Manager Follow-up → Meeting Scheduled → Followed Up → Partnered), shortlisting heuristics, sample-drop protocol, what lands in conversion, recurring decision-maker dynamics, disqualification patterns, and the small-vs-large pitch. |
| **RETAILER_TECHNICAL_ONBOARDING.md** | **Retail partner — technical onboarding** flow that picks up at `Status = Partnered`. Use when an AI / operator needs to wire a new retailer into the ledger + website + inventory pipeline. End-to-end sequence (Contributors row, Agroverse Partners row, partner page, discovery surfaces, photos, opening-order `[INVENTORY MOVEMENT]` events, sync runs), verification checklist, recurring failure modes (Edgar auto-rename + col T semantics), worked example (The Way Home Shop, 2026-04-28). **§10 documents the `dao_client onboard_retail_partner` CLI** that automates the deterministic ledger + inventory steps from a YAML manifest. |
| **DAPP_PERMISSION_CHANGE_FLOW.md** | **DApp permission edits** — `[DAPP PERMISSION CHANGE EVENT]` flow: governor signs in `governor_permissions.html` (edit mode) → Edgar dispatches → GAS handler verifies governor independently, applies the change to `permissions.json` on `treasury-cache`, and logs to the `Dapp Permission Changes` tab on the Telegram-compilation spreadsheet (`1qbZZhf-…`, gid 1054656840). RSA signature is the gate (no PR-review step). Optimistic-concurrency check on roles-before; idempotent on Telegram Update ID. Read when editing the dispatch / handler / DApp UI. |

## How to use (for AIs)

1. **First:** Read `OPERATING_INSTRUCTIONS.md` for rules on reading and contributing.
1b. **AI agent ledger submissions (software/docs work):** Read **`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`** — use **`dao_client/modules/report_ai_agent_contribution.py`** with mandatory **`https://github.com/TrueSightDAO/.../pull/...`** links and an explicit description.
2. **Before editing any project:** Read `WORKSPACE_CONTEXT.md` to understand the workspace as a whole.
3. **Before touching a specific repo:** Check `PROJECT_INDEX.md` for that project’s purpose, stack, and where credentials/docs live.
4. **Main Ledger repackaging / conversion** (inputs, cost per output, new `Currency` names): Read **`LEDGER_CONVERSION_AND_REPACKAGING.md`** in full when the task involves it (`WORKSPACE_CONTEXT.md` §3b points here).
5. **Marketing / CMO consultation:** When the task involves marketing (copy, positioning, campaigns, content, growth), read `CMO_SETH_GODIN.md` to consult the Agentic AI CMO (Seth Godin) and operate based on that context.
6. **Strategy / onboarding (Dr Manhattan):** When the task involves strategy, growth, priorities, or onboarding for the DAO/Agroverse network, read `DR_MANHATTAN.md` to consult Dr Manhattan and operate based on that context.
7. **DApp pages (dapp repo):** When creating or editing HTML pages in the **dapp** repository, read **`DAPP_PAGE_CONVENTIONS.md`** and follow its structure (meta tags, Open Graph, favicon, nav, body/container, status/loading). For UX patterns (loading states, errors, comboboxes), also follow **`dapp/UX_CONVENTIONS.md`**.
8. **Syndicate agreements (AGL contracts):** When drafting Export Trade Financing Syndicate Agreements, read **`SYNDICATE_AGREEMENTS.md`** first. **Precedence:** Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee (avoid double-charging). Template in `notarizations/syndicate_agreement_template.md`.
9. **Lead list / Hit List extraction:** When discovering retailer contacts or updating the Hit List (apothecaries, metaphysical shops), read **`LEAD_LIST_EXTRACTION.md`** for the Playwright → CSV → append workflow, schema, and credentials.
10. **Lab report translation (Agroverse shipments):** When translating Portuguese lab reports to English, adding English summaries to shipment pages (AGL4, AGL8, etc.), or extracting/translating PDF lab reports, read **`LAB_REPORT_TRANSLATION.md`** for the workflow (pdfplumber → Grok API → HTML summary), script location, and Grok key (video_editor/.env).
11. **Downloads media → Agroverse blog/YouTube:** When the user places **videos** or **images** in **`~/Downloads`** (or similar) for **agroverse.shop**, read **`DOWNLOADS_MEDIA_TO_AGROVERSE.md`** for the video pipeline scripts, dedupe rules, and the manual image ingest + blog listing thumbnail rules.
12. **Product development specs (new packaging / SKUs):** When building **checklists for physical products** (chocolate bars, pouches, retail display boxes, labels, GTINs), read **`PRODUCT_DEVELOPMENT_SPECS.md`**. Prefer **Google Sheets** with one tab per section; use **`market_research/scripts/populate_chocolate_bar_spec_sheet.py`** as the template for populate + cell styling (or copy the pattern for a new spreadsheet ID).
13. **TrueChain integration:** When working on TrueChain (blockchain, mirror service, block explorer, provenance), read **`TRUECHAIN.md`** (includes "For AI Assistants" section, setup, technical proposal). Repo: [TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain).
14. **API keys and env vars:** See the sibling repo **agentic_ai_api_credentials** for `env.template` and `API_CREDENTIALS_DOCUMENTATION.md`; no secrets are stored there.
15. **GitHub / Agentic AI SSH:** When pushing to GitHub on behalf of the user with automation, read **`GITHUB_AGENTIC_AI_SSH.md`** — key directory **`~/.ssh/agentic_ai_github/`**, host alias or `GIT_SSH_COMMAND`. **Branch + PR** by default; **`gh pr merge`** to default branch **only when the user explicitly asks** to complete the release (see that doc § “When the user requests the full release loop”).
16. **Hit List contact enrichment (`AI: Enrich with contact`):** When changing website scrape / email / contact-form automation for the holistic wellness Hit List, read **`HIT_LIST_CONTACT_ENRICHMENT.md`** (design decisions, DApp Remarks parity, shared sheet module). Operational details: **`market_research/HIT_LIST_CREDENTIALS.md`**.
17. **Agroverse QR batch (sheet + `batch_compiler.py`):** When adding serialized **`Agroverse QR codes`** rows or generating **`compiled_*.png`** labels locally, read **`AGROVERSE_QR_CODE_BATCH_GENERATION.md`** (naming, columns **A–V**, **`Currencies`!A**, venv + compile command).
18. **agroverse.shop new SKU (farm + shipment grids):** When adding a **`product-page/`** PDP for a farm- or shipment-backed SKU, read **`AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md`** so **“Products from This Farm”** and **“Products from This Shipment”** include **`item-card`** links (with **`PRODUCT_CREATION_CHECKLIST.md`** for feeds/schema).
19. **Onboarding a new retail partner (post-`Partnered`):** When wiring a new shop into the ledger + website + inventory pipeline (Agroverse Partners row, partner page, opening-order `[INVENTORY MOVEMENT]` events, etc.), read **`RETAILER_TECHNICAL_ONBOARDING.md`**. **§10 documents the `dao_client onboard_retail_partner` CLI** — preferred path: draft a YAML manifest (template in `dao_client/examples/onboarding/the-way-home-shop.yaml`), `--dry-run` for review, `--execute`, then handle the website-surface manual steps the script prints. Field-visit / sales work that produces the "yes" lives in the sister doc **`RETAILER_ONBOARDING_PLAYBOOK.md`**.

## Location

- **Context (this repo):** Clone from `git@github.com:TrueSightDAO/agentic_ai_context.git` (or your local path, e.g. `/Users/garyjob/Applications/agentic_ai_context`).
- **Credentials reference:** `/Users/garyjob/Applications/agentic_ai_api_credentials` (or see PROJECT_INDEX for credential docs; no secrets in this repo).
- **Workspace root (multi-root):** Typically `/Users/garyjob/Applications` — contains many project directories; adjust for your machine.

Keep `WORKSPACE_CONTEXT.md` and `PROJECT_INDEX.md` updated when you add repos or change architecture so all AIs stay in sync.
