# Workspace Context — Overview for AI Assistants

This document describes the **entire workspace** under `/Users/garyjob/Applications`. Read it to understand what the workspace is about before editing any project.

---

## 1. What This Workspace Is

The workspace is a **multi-root** set of applications and repositories. It centers on:

1. **TrueSight DAO / Agroverse ecosystem** — DAO tools, tokenomics, DApp, static sites, e‑commerce, QR/inventory, market making.
2. **Krake / GetData.io** — Data harvesting: Rails app, Sinatra services, local Node tools, Chrome extension.
3. **Supporting projects** — Market research, video editor, sentiment/news import, FDA FSVP, POS integrations, personal blog, I Ching oracle, Jarvis LLM, read_page extension.

Credentials and env vars are **not** stored in this context repo; they are documented in the sibling repo **agentic_ai_api_credentials** (env.template, API_CREDENTIALS_DOCUMENTATION.md).

---

## 2. High-Level Grouping

| Group | Repos | Purpose |
|-------|--------|---------|
| **DAO / Agroverse** | dapp, truesight_me, tokenomics, agroverse_shop, qr_codes, proposals | DAO DApp, static site, tokenomics automation, e‑commerce, QR codes, proposals |
| **Krake / Data** | krake_ror, krake_sinatra, krake_local, krake_chrome | Rails backend, Sinatra services, local commander/listener, Chrome extension for data harvesting |
| **Content & Research** | market_research, video_editor, sentiment_importer, garyteh_blog | Content calendars, physical stores, video Shorts, news/sentiment import, blog |
| **Infra & Tools** | jarvis, read_page, iching_oracle, point-of-sales-integrations, heierling-pos | Local LLM, browser extension, oracle app, POS integrations |
| **Compliance / Biz** | fda_fsvp | FDA FSVP documentation and supplier verification |
| **Context & Credentials** | agentic_ai_context, agentic_ai_api_credentials | AI context (this repo) and credential reference only |

---

## 3. Key Conventions

- **Credentials**: Never commit secrets. Use `.env` per project; variable names and usage are in `agentic_ai_api_credentials`. **Credential files** (e.g. `google-service-account.json`) must be obtained from user during setup — see `SETUP_REQUIREMENTS.md`.

---

## 3a. Git check-in: do not commit to GitHub

**Before committing or pushing any project, ensure the following are never included:**

### Never commit

1. **Security credentials and secrets**
   - `.env`, `.env.local`, `.env.*.local`
   - Credential files: `*credentials*.json`, `*token*.json`, `google-service-account.json`, `*.pem`, `*.key`, `*.p12`, `secrets/`, `credentials/`
   - **Gmail user OAuth (market_research):** `market_research/credentials/gmail/client_secret.json` and `token.json` — see **`GMAIL_OAUTH_WORKFLOW.md`**; run `python3 scripts/gmail_oauth_authorize.py` after placing the Desktop client JSON; never commit those files (folder uses `.gitignore`; only `README.md` there may be tracked).
   - API keys, passwords, or tokens in source (use env vars or secret managers)

2. **Unnecessary library and build artifacts**
   - **Node:** `node_modules/`, `npm-debug.log*`, `yarn-error.log`, `.npm`, `.yarn`
   - **Python:** `venv/`, `__pycache__/`, `*.py[cod]`, `.eggs/`, `dist/`, `build/`, `*.egg-info/`
   - **Ruby:** `vendor/bundle/`, `.bundle/`, `tmp/`, `log/*.log`
   - **General:** `dist/`, `build/`, `out/`, `.cache/`, `*.log`, `test-results/`, `playwright-report/`, `.coverage`, `htmlcov/`

3. **Large or generated assets** (unless the repo is intended to host them)
   - Binary blobs, DB dumps (e.g. `dump.rdb`), large media (e.g. raw video) — add to `.gitignore` and avoid staging

### What to do

- **Maintain `.gitignore`** per project with the above patterns (and project-specific ones).
- **Verify before push:** `git status` and `git diff --cached`; run `git check-ignore -v <file>` if unsure.
- **Credential files:** See `SETUP_REQUIREMENTS.md` for per-project credential file names; prompt user for these during setup, never commit them.
- **If something was committed by mistake:** Remove from tracking, add to `.gitignore`, rotate any exposed secrets, and use history-rewriting only if necessary and with care.
- **Agroverse product feeds / Merchant Center safety:** keep product category in feed as `g:google_product_category` only; avoid adding freeform `Product.category` in page JSON-LD when it causes Merchant warnings. Keep feed URLs canonical and non-redirecting (prefer `https://agroverse.shop/...` consistently), and ensure feed text/entities are valid XML (avoid double-escaped entities like `&amp;apos;`).
- **Static sites**: truesight_me, agroverse_shop, dapp — often deployed to GitHub Pages or similar; design uses “Saffron Monk” / earthen palette where noted.
- **Ruby**: krake_ror, sentiment_importer use Rails; krake_sinatra uses Sinatra. Check README for Ruby/RVM version (e.g. 2.6.x).
- **Python**: market_research, video_editor, tokenomics scripts, jarvis — use venv and `requirements.txt` per project.
- **Node/TS**: krake_local, tokenomics (Raydium), iching_oracle — check for Node 18+ or 20+ and npm/pnpm.
- **APIs**: DApp and automation often talk to tokenomics backend/Google Apps Scripts; see tokenomics API.md and dapp UX_CONVENTIONS.md. **Google Apps Script web apps** must allow the caller (**Who has access**); otherwise the browser reports **CORS** errors for `fetch()` even though the `.gs` uses standard `ContentService` JSON — see **DAPP_PAGE_CONVENTIONS.md §14**.

---

## 3b. Main ledger: **Ledger conversion and repackaging**

**Mandatory for those tasks:** If the user asks about **repackaging**, **Main Ledger conversion**, **input/output `Currency`**, **cost per unit after conversion**, or **naming new production lines**, read **`LEDGER_CONVERSION_AND_REPACKAGING.md`** in this repo **in full** before replying. That file is the **canonical playbook** (prompt pattern, standard `Currency` template, cost formula, SCHEMA/API pointers, legacy vs new naming, cross-ledger placeholder).

**One-line summary:** Operators combine **input** inventory lines into **output** SKUs at a location; composite names use **`Alibaba:…`**, **`CP…BR`** (Correios — see §4 below), and **`| Operator YYYYMMDD`**; costs come from **`offchain asset location`** **Unit Cost** × quantities ÷ output count.

---

## 3c. TrueSight DAO Contribution Ledger — **double-entry offchain**, **Currencies**, **invoice → GitHub**

**Spreadsheet:** [TrueSight DAO Contribution Ledger](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit) (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`). Tabs include **`Currencies`** and **`offchain transactions`**.

### Double-entry on **`offchain transactions`**

Treat **`offchain transactions`** as **double-entry** for purchases that consume cash and add physical (or countable) inventory:

| Leg | **`Currency`** (col E) | **Amount** (col D) | Role |
|-----|-------------------------|-------------------|------|
| **Cash / funding** | **`USD`** | **Negative** (e.g. `-27.70`) | Money left the wallet / card for the order (grand total, tax-included). |
| **Inventory** | **Custom line** matching **`Currencies`!A** | **Positive** (e.g. `50` for fifty units) | Units received; **no second USD outflow**. |

- **If the user has not already recorded the negative `USD` row** for that purchase, **insert it**: parse the invoice/receipt for **grand total**, date, payer (`Fund Handler` per ship-to rule below), and links. **Do not** only add the positive inventory leg and assume the cash row exists.
- **Pairing:** The **positive inventory** row’s **Description** should cite the **sheet row number** of the **`USD`** leg (e.g. “pairs offchain row N…”), plus **order id**, **ship-to**, and a **GitHub** link to the archived invoice PDF (see below). The **`Currency`** string on the inventory row must **exactly match** the new **`Currencies`** row’s column **A**.

### **`Currencies` tab (unit “price” for the inventory leg)**

- **`Price in USD`:** Use **tax-included “landed”** unit cost: **landed per unit = invoice grand total ÷ unit count** (not pre-tax unit price), unless policy is explicitly changed.
- **New SKU / packaging:** Append a row (**A** = canonical name; **`Price in USD` = landed per unit**). Then **sort** the tab: **row 2 through last data row**, **all sheet columns in the grid** (e.g. **A through AC**), **A→Z by column A**, so **`VLOOKUP`** / **`ARRAYFORMULA`** on other tabs stay aligned and **no column is orphaned**.

### **Fund Handler (manager) from ship-to**

- **Ship-to** is **TrueTech Inc, 1423 Hayes St, San Francisco, CA 94117-1425, United States** (normalize minor formatting): **Fund Handler** = **`Kirsten Ritschel`** (exact **Name** in tab **Contributors contact information**).
- **Any other ship-to:** **Fund Handler** = **`Gary Teh`** unless the user states otherwise. Apply consistently on **both** legs (cash and inventory) when the handler represents **custody / management** of the asset or spend context.

### **Invoice PDF → `TrueSightDAO/.github` (automation pattern)**

Archive a **canonically named** PDF under **`main/assets/`** so **`offchain`** descriptions can point at a stable **`blob`** URL.

1. **Name files** predictably, e.g. **`YYYYMMDD_vendor_order_<order-id>_<short-slug>_invoice.pdf`** (use real order id from the invoice).
2. **Credentials:** Use **`GITHUB_PAT`** from **`market_research/.env`** (never commit; rotate if exposed). On a **fresh machine**, copy **`market_research/.env.example`** → **`.env`** and set **`GITHUB_PAT`**; see **`SETUP_REQUIREMENTS.md`** (**market_research**) and **`market_research/README.md`**. Do **not** change hardcoded tokens inside **`sentiment_importer`**.
3. **API (same idea as Edgar’s `submit_contribution` after `file_uploaded`):** Reference **`sentiment_importer`** **`app/controllers/dao_controller.rb`** — **`GET`** `https://api.github.com/repos/{owner}/{repo}/contents/{path}` with **`Authorization: token <PAT>`** and **`Accept: application/vnd.github+json`**; if **404**, **`PUT`** the same URL with JSON **`message`**, **`content`** (base64 file bytes), **`branch`** (`main`); if **200**, file exists (update only if replacing, using **`sha`** from the GET body). **Do not** paste the PAT into chat or into source code.
4. **Local copy:** Optionally keep a same-named copy under **`~/Downloads`** for the operator; source of truth for the ledger link is **GitHub**.

### **Non-Amazon / vendor PDFs; invoice already linked from `offchain`**

Many expenses are **not** Amazon (e.g. **Sticker Mule**, other suppliers). Layouts differ; do not assume Amazon’s “Order Summary” text.

1. **Locate the PDF URL** in the existing **`USD`** row (column **B**): **`Destination Expense File Location:`** often points at **`https://github.com/TrueSightDAO/.github/tree/main/assets/…pdf`**. If the user gives a **sheet row** (e.g. “process line 2801”), read that row first.
2. **Download for parsing:** Convert **`/tree/main/`** to **`/raw/main/`** (or use **Raw** on GitHub) so the agent can **`curl`** / HTTP GET the bytes to a temp path under **`~/Downloads`** (or workspace). **No OAuth** is required for public repo raw files.
3. **Extract fields:** Use **`pypdf`** (or similar) **`PdfReader` → `extract_text()`** on the downloaded file. From the text, derive **grand total** (tax-included), **line quantities**, **vendor order / confirmation id**, **billing vs shipping** addresses, and dates. **Reconcile** the PDF total with column **D** on the **`USD`** row; if they disagree, stop and surface the mismatch.
4. **GitHub upload:** If the PDF is **already** under **`TrueSightDAO/.github`** **`assets/`** at that URL, **do not re-upload** unless the user wants a renamed copy. Use the existing **`blob`** link in the inventory row’s **Description** (same path as Edgar’s upload convention: `https://github.com/TrueSightDAO/.github/blob/main/assets/<filename>.pdf`).
5. **`Currencies` naming:** Build a clear **`Currency`** string (column **A**) that includes **vendor + unit meaning + order ref** (example pattern: *`Sticker Mule 4x2in custom rectangle label (per piece, order R384751187)`* so lookups stay unique). **Landed unit price** = **grand total ÷ countable units** chosen for the inventory leg (e.g. per label, per envelope).
6. **Fund Handler:** Apply the **ship-to** rule (§3c above). Vendor PDFs often list **Shipping Address** separately from billing; **1423 Hayes St, San Francisco, CA 94117** (with **TrueTech Inc** / **Kirsten Ritschel**) → **`Kirsten Ritschel`** on the **inventory** leg.

**User shortcut for agents:** Instructions like *“process **`offchain` row N; PDF is already attached”*** mean: **download from GitHub**, **parse**, **add `Currencies` + sort**, **add positive inventory row** pairing row **N** — **do not** assume Amazon format or re-upload the PDF if it already lives in **`assets/`**.

### **Suggested order of operations (agents)**

1. Obtain invoice text: from **`~/Downloads`**, or **`offchain`** row **B** URL → **raw** PDF download, then **`pypdf`** (vendor formats vary).
2. **Ensure negative `USD` row exists** on **`offchain transactions`**; if not, **add it** (amount = **-grand total** as in existing ledger style). If the user points at an **existing** cash row, **skip** creating a second **`USD`** line.
3. **GitHub `assets/`:** **Upload** only when there is **no** file yet (local invoice only, or missing link). If **`Destination Expense File Location`** already references **`TrueSightDAO/.github`**, use that **`blob`** URL in the inventory **Description**.
4. **Add or update `Currencies`** row (landed unit **= grand total ÷ qty**); **full-width sort** by column **A**.
5. **Add positive inventory row** on **`offchain transactions`**: **`Currency`** = **`Currencies`!A** exact string; **Description** links **cash row**, PDF **blob** URL, order id; **Fund Handler** per **ship-to**.

### **Sheet protection**

**`Currencies`** is often **range-protected**. Service accounts (e.g. **`agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com`**) may edit **`offchain transactions`** but still be blocked on **`Currencies`**. Remedies: editor **unprotect** / **exception** for that account, or human completes **`Currencies`** + **sort** in the UI.

---

## 3d. OpenClaw + WhatsApp (pointer)

**Canonical detail** (verified / excluded group JIDs, inbound monitor **intent** vs **`~/.openclaw/openclaw.json`**, JID discovery, CLI pairing): **`OPENCLAW_WHATSAPP.md`** in this repo.

**Outbound digests:** That file also defines how to generate **Beer Hall** (full DAO / ops) and **Founder Haus AI prompt** (Web3 partner channel — **AI/agent subset**) WhatsApp summaries: required **OpenClaw × Cursor** attribution, **WhatsApp-safe** formatting, a **TLDR in plain language** (non-technical readers; explicit **why it matters for the DAO**) before technical bullets, **links** (PR/commit/Sheets), **git push → PR → merge** before posting when code changed, tab **`OpenClaw Beer Hall updates`** on the Telegram compilation sheet for logging, and **sequential** sends to avoid gateway timeouts. **GitHub in those two channels:** only **`https://github.com/TrueSightDAO/`** — do not link personal or other org repos (e.g. `garyjob`, `KrakeIO`) in Beer Hall / Founder Haus digests.

---

## 4. Cross-Repo Relationships

- **dapp** ↔ **tokenomics**: DApp calls tokenomics APIs; see tokenomics API.md. **Apps Script edits:** implement and deploy from **`tokenomics/clasp_mirrors/<scriptId>/`** (clasp); **`tokenomics/google_app_scripts/`** is reference-only unless explicitly backported.
- **dapp** ↔ **holistic wellness Hit List (Sheets)**: `store_interaction_history.html` calls the read-only web app documented under **`tokenomics/google_app_scripts/holistic_hit_list_store_history/`** (Deployment URL in `store_interaction_history_api.gs`; DApp **`API_BASE_URL`** should match after redeploys). **Deploy changes** from the matching **`tokenomics/clasp_mirrors/<scriptId>/`** project (`clasp push`), not from the thematic folder alone. Spreadsheet: `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`. Partner workflow: **`PARTNER_OUTREACH_PROTOCOL.md`**, **`HIT_LIST_CREDENTIALS.md`** (market_research).
- **Edgar** = **sentiment_importer** (edgar.truesight.me): DAO submission API; receives DApp contributions and triggers webhooks via Sidekiq (e.g. proposal → GitHub PR without waiting for cron).
- **truesight_me** ↔ **tokenomics**: Static site data (e.g. shipments) can come from Google Sheets / tokenomics scripts.
- **Agroverse main ledger (`Currency` / product strings):** Codes like **`CP`…`BR`** embedded in pouch or ceremonial names are usually **Correios (Brazil Post) international package tracking numbers** for shipments from **Ilheus, Bahia** (often **Matheus’** / Oscar-adjacent origin) **to a destination in the United States**. They disambiguate a specific mailed batch when naming SKUs or composite ceremonial lines (e.g. `… + 8 Ounce Package Kraft Pouch CP340992735BR …`). See **`tokenomics/SCHEMA.md`** for sheet/column layout. For **repackaging and composite SKUs**, read **`LEDGER_CONVERSION_AND_REPACKAGING.md`** and **§3b** above (pointer).
- **agroverse_shop** ↔ **market_research**: Content and physical store scripts in market_research feed or sync with agroverse. **Field media in `~/Downloads` (videos → blog/YouTube, images → assets):** read **`DOWNLOADS_MEDIA_TO_AGROVERSE.md`** in this repo. **Blog listing page (`agroverse_shop/blog/index.html`):** Card images MUST reference **`assets/images/blog/listing-640w/{post-slug}.jpg`** (resized for performance; built by **`agroverse_shop/scripts/sync_blog_listing_thumbnails.py`**). Source selection: prefer each **`post/<slug>/index.html`** first in-body image (skip nav logo; normalize relative `../../assets/` paths); ignore useless generic **`cacao-tasting-wheel.jpg`** as the only OG image for text-only posts. For fallbacks and breaking accidental duplicates (same file/hash or same Wix reuse id), use distinct shots from **`assets/images/blog/bahia-photo-library/`** and elsewhere in-repo. See **`PROJECT_INDEX.md`** (agroverse_shop row) and **`agroverse_shop/.cursor/rules/blog-listing-images.mdc`**. **Product development specs** (packaging, new SKUs): checklists live in **Google Sheets** (tabs per section); `market_research/scripts/populate_chocolate_bar_spec_sheet.py` can populate + style cells; read **`PRODUCT_DEVELOPMENT_SPECS.md`** in agentic_ai_context for the workflow and future AI behavior. **Default Drive folder** for new generated Sheet artifacts: `1esYnlwChRmv9-M3ymWYhWMPHRowhOluw` (link in that doc and in **`GOOGLE_API_CREDENTIALS.md`**). **Wholesale / import purchase agreement PDFs:** `market_research/purchase_agreements/` (ReportLab); read **`PURCHASE_AGREEMENT_PDFS.md`** before generating or extending agreements—farm canonical URLs (e.g. Oscar: `https://agroverse.shop/farms/oscar-bahia/index.html`), table/markup rules, deposit layout, and copy-from-script workflow.
- **krake_local** ↔ **krake_ror** / **krake_chrome**: Local tools and extension interact with Krake backend/services.
- **agentic_ai_api_credentials**: Reference only for env var names and which project uses them; no secrets.
- **TrueChain** ↔ **tokenomics** / **Edgar**: Private blockchain for DAO/Agroverse audit trail. Mirror Service copies new rows from Google Sheets to TrueChain. Block explorer via Google Apps Script (not Edgar). See `TRUECHAIN_README.md`, `TRUECHAIN_SETUP_AND_INTEGRATION.md`.

---

## 5. Where to Look Next

- **OpenClaw + WhatsApp:** **`OPENCLAW_WHATSAPP.md`** — JIDs, monitor intent, exclusions, playbook (see also **§3d** pointer).
- **Per-project details**: `PROJECT_INDEX.md` in this repo (purpose, stack, entry points, credentials reference).
- **Setup requirements**: `SETUP_REQUIREMENTS.md` in this repo — credential files needed per project (prompt user during setup).
- **Git / GitHub check-in**: Section **3a** above — never commit credentials or unnecessary library/build files; keep `.gitignore` updated and verify before push.
- **Env vars and API keys**: `agentic_ai_api_credentials/API_CREDENTIALS_DOCUMENTATION.md` and `env.template`.
- **DAO schema/API**: tokenomics `SCHEMA.md`, `API.md`. **Tokenomics GAS:** edit under local `tokenomics/clasp_mirrors/<scriptId>/` (`clasp pull` after clone); git tracks mirror `.clasp.json` + checklist only — not `*.js` / `appsscript.json`. `google_app_scripts/` = readable reference `.gs`.
- **Ledger conversion / repackaging**: **`LEDGER_CONVERSION_AND_REPACKAGING.md`** (canonical). **§3b** above — mandatory pointer so new agents do not skip the playbook.
- **Contribution Ledger (double-entry offchain, `Currencies`, Amazon vs vendor PDFs, GitHub upload or existing `assets/` link, ship-to → manager):** **§3c** above — includes **“process `offchain` row N, PDF already attached”** (download **`raw`**, **`pypdf`**, pair to row **N**).
- **Supply chain, freighting & unit-cost economics**: this repo `SUPPLY_CHAIN_AND_FREIGHTING.md` (inventory by location, freight options Brazil→US, cacao processing/cost; references SCHEMA.md).
- **Wholesale purchase agreement PDFs**: this repo **`PURCHASE_AGREEMENT_PDFS.md`** — `market_research/purchase_agreements/`, ReportLab conventions, farm profile URLs, payment schedule table pattern.
- **Gmail user OAuth (local tokens for automations):** this repo **`GMAIL_OAUTH_WORKFLOW.md`** — `market_research/scripts/gmail_oauth_authorize.py`, `market_research/credentials/gmail/` (gitignored secrets + optional tracked `README.md`).
- **DApp UX**: dapp `UX_CONVENTIONS.md`.
- **DApp CI/testing**: dapp has unit tests (Node) and Playwright integration tests. Run `npm test` in `dapp/`. See dapp `tests/README.md`. CI: `.github/workflows/ci.yml` on push/PR to main. Pure logic in `expense-form-utils.js`; integration tests mock Google Apps Script and Edgar APIs (no real network calls).
- **Agroverse Shop CI/testing**: agroverse_shop has Playwright visual consistency tests. Run `npm test` in `agroverse_shop/`. See agroverse_shop `tests/README.md`. **Local runs hit `localhost:8000`** — Playwright auto-starts Python `http.server` on port 8000; ensure nothing else uses that port. CI (GitHub Actions) runs against live site (beta or prod). Workflow: `.github/workflows/visual-consistency.yml`. Smart runner: `npm run test:resume` to resume from failures.
- **Downloads → Agroverse (videos + images):** **`DOWNLOADS_MEDIA_TO_AGROVERSE.md`** — video pipeline: `analyze_incoming_videos.py` → optional `youtube_batch_incoming.py` → `generate_video_transcript_blog_posts.py` (optional Grok polish). **After regen or any `youtube_videos.json` title change**, run **`youtube_update_video_titles.py`** so YouTube matches the manifest; if OAuth **`invalid_scope` / refresh fails**, use **`youtube_oauth_reauthorize.py`** then rerun the updater (details in that doc). **Images:** no dedicated Downloads automation; copy into `agroverse_shop/assets/images/…`, wire in HTML, run `sync_blog_listing_thumbnails.py`; blog card rules remain as in §4 (listing-640w, first in-body image, `bahia-photo-library` fallbacks).
- **Marketing / CMO consultation**: this repo `CMO_SETH_GODIN.md` — Agentic AI CMO (Seth Godin). Read when doing marketing activities to consult the CMO and operate based on his principles.
- **Strategy / onboarding**: this repo `DR_MANHATTAN.md` — Dr Manhattan. Read when doing strategy, growth, priorities, or onboarding for the DAO/Agroverse network. Future use: chatbot for newcomers.
- **Governance**: this repo `GOVERNANCE_SOURCES.md` — Whitepaper (truesight.me/whitepaper), proposals (GitHub TrueSightDAO/proposals, Realms). Pull whitepaper via `scripts/fetch_whitepaper.py`; browser for Realms.
- **Syndicate agreements**: this repo `SYNDICATE_AGREEMENTS.md` — Template and drafts in `notarizations/`. **Precedence:** Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee (avoid double-charging). Shipment Ledger as source. **PDF generation:** Use `notarizations/scripts/generate_syndicate_pdf.mjs` with TrueSight DAO logo header (`.github/assets/20221219 - Gary logo white background squarish.jpeg`).
- **TrueChain integration**: this repo `TRUECHAIN.md` — Private blockchain setup, mirror service, block explorer (GAS), schema evolution, product/shipment/farm, technical proposal. Repo: https://github.com/TrueSightDAO/TrueChain.

---

## 6. Production domains and deployment sources

**Important:** The following domains are deployed from specific GitHub repos. Do not confuse workspace paths with deployment sources.

| Domain | Deployed from (production source) | Notes |
|--------|-----------------------------------|-------|
| **truesight.me** | [TrueSightDAO/truesight_me_prod](https://github.com/TrueSightDAO/truesight_me_prod) | Main DAO landing page — production |
| **agroverse.shop** | [TrueSightDAO/agroverse_shop_prod](https://github.com/TrueSightDAO/agroverse_shop_prod) | E‑commerce — production |

- `truesight_me/` in the workspace may be the beta repo (truesight_me or truesight_me_beta); changes for production go to **truesight_me_prod**.
- `agroverse_shop/` in the workspace may be the beta repo (agroverse_shop_beta); changes for production go to **agroverse_shop_prod**.

When editing for **truesight.me** or **agroverse.shop**, ensure changes are made in or synced to the **\*_prod** repo that deploys that domain.

---

## 7. Repository locations (GitHub)

Future AIs can **clone** these repos when the workspace path is missing or a fresh copy is needed. Use `git clone <URL>` (HTTPS below; SSH also works if configured).

| Workspace path | GitHub repo (HTTPS clone URL) | Production deploy |
|----------------|-------------------------------|-------------------|
| `tokenomics/` | https://github.com/TrueSightDAO/tokenomics | — |
| `dapp/` | https://github.com/TrueSightDAO/dapp | — |
| `truesight_me/` | https://github.com/TrueSightDAO/truesight_me | → **truesight_me_prod** → truesight.me |
| `agroverse_shop/` | https://github.com/TrueSightDAO/agroverse_shop_beta | → **agroverse_shop_prod** → agroverse.shop |
| `market_research/` | https://github.com/TrueSightDAO/content_schedule |
| `agentic_ai_context/` | https://github.com/TrueSightDAO/agentic_ai_context |
| `TrueChain/` | https://github.com/TrueSightDAO/TrueChain |
| `krake_ror/` | https://github.com/KrakeIO/krake_ror |
| `krake_sinatra/` | https://github.com/KrakeIO/krake_sinatra |
| `krake_chrome/` | https://github.com/KrakeIO/Chrome |

Other projects (qr_codes, proposals, krake_local, sentiment_importer, fda_fsvp, jarvis, etc.) may be local-only or under different orgs; check `PROJECT_INDEX.md` GitHub column when added.

---

Keep this file and PROJECT_INDEX.md updated when adding or retiring repos so all AI assistants stay in sync.
