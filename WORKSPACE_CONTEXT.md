# Workspace Context — Overview for AI Assistants

This document describes the **entire workspace** under `/Users/garyjob/Applications`. Read it to understand what the workspace is about before editing any project.

---

## 1. What This Workspace Is

The workspace is a **multi-root** set of applications and repositories. It centers on:

1. **TrueSight DAO / Agroverse ecosystem** — DAO tools, tokenomics, DApp, static sites, e‑commerce, QR/inventory, market making.
2. **Krake / GetData.io** — Data harvesting: Rails app, Sinatra services, local Node tools, Chrome extension.
3. **Supporting projects** — Market research, video editor, sentiment/news import, FDA FSVP, POS integrations, personal blog, I Ching oracle, Jarvis LLM, read_page extension, **Cypher-Defense** (scam/phishing tooling + AWS account hygiene scripts and incident notes).

Credentials and env vars are **not** stored in this context repo; they are documented in the sibling repo **agentic_ai_api_credentials** (env.template, API_CREDENTIALS_DOCUMENTATION.md).

---

## 2. High-Level Grouping

| Group | Repos | Purpose |
|-------|--------|---------|
| **DAO / Agroverse** | dapp, **dao_client**, truesight_me, tokenomics, agroverse_shop, qr_codes, proposals | DAO DApp, **Python Edgar CLI** (signed contributions; AI agent submissions per **`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`**), static site, tokenomics automation, e‑commerce, QR codes, proposals |
| **Krake / Data** | krake_ror, krake_sinatra, krake_local, krake_chrome | Rails backend, Sinatra services, local commander/listener, Chrome extension for data harvesting |
| **Content & Research** | market_research, video_editor, sentiment_importer, garyteh_blog | Content calendars, physical stores, video Shorts, news/sentiment import, blog |
| **Infra & Tools** | jarvis, read_page, iching_oracle, point-of-sales-integrations, heierling-pos, **Cypher-Defense** | Local LLM, browser extension, oracle app, POS integrations; **Cypher-Defense** — Web3 scam/phishing extension **and** AWS incident-response scripts + `docs/incidents/` (local `.env` for AWS keys; never commit) |
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
- **Holistic wellness Hit List — field agent pipeline:** **`dapp/stores_nearby.html`** (signed user) may send **`save_location=true`** on the Stores Nearby **`doGet`** so GAS appends a **`pending`** row on tab **`Recent Field Agent Location`** (`1eiqZr3LW…`, `gid=881847228`). **`market_research/scripts/field_agent_location_places_pull.py`** + GitHub Action **`field_agent_location_places_pull.yml`** process **`pending`** → Google Places Nearby → append **Hit List** / **DApp Remarks** / status **`pulled`** or **`ignored because already pulled`**. **`tokenomics/SCHEMA.md`** §4; **`HIT_LIST_CREDENTIALS.md`**; **DAPP_PAGE_CONVENTIONS.md §14** (subsection *Field agent location*).
- **Tokenomics `clasp push` / “clasp deploy”:** When the user says **clasp deploy** without separate steps, assistants **run `clasp push` then `clasp deploy`** from the correct `tokenomics/clasp_mirrors/<scriptId>/` after syncing `google_app_scripts/**` into the mirror (see **`agentic_ai_context/NOTES_tokenomics.md`**). For existing **Web App** URLs, use **`clasp deploy --deploymentId …`** so **`/exec`** stays stable. After pushing, still give the **Script editor link**; if deploy was not done via clasp, remind that **Manage deployments → New version** may be needed in the UI. **Every mirror must ship `Version.gs`:** sales / Parse Telegram uses **`google_app_scripts/tdg_inventory_management/Version.gs`**; **QR Code Generation** (`1N6o00N9VtRK…`) uses **`google_app_scripts/agroverse_qr_codes/Version.gs`**; other mirrors use **`google_app_scripts/_clasp_default/Version.gs`** (or run **`node tokenomics/scripts/ensure_clasp_version_gs.mjs`** after clone). Bump UTC + changelog in the canonical file before copy + push (**`NOTES_tokenomics.md`**). Mirror IDs, copy/paste sync commands, and Stripe sheet **column P (Agroverse QR code)** workflow are documented in **`agentic_ai_context/NOTES_tokenomics.md`** and **`tokenomics/SCHEMA.md`**. **Agroverse QR codes** tab: **column I (`Currency`)** must match a **`Currencies`!A** value (same workbook; often via **`IMPORTRANGE`** / cross-sheet reference); **column A** promo tokens: **`LA`** = Los Angeles region, **`CC`** = ceremonial cacao, **`CT`** = cacao tea — see **`NOTES_tokenomics.md`** § *Agroverse QR codes tab*.

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
| **Cash / funding (Brazil)** | **`Brazilian Reis`** | **Negative** (e.g. `-180`) | Same as USD leg, but amount is **BRL**; **`Currency`** must **exactly match** the **`Currencies`!A** label for the real (**`Brazilian Reis`** in the ledger today). Inventory **`Price in USD`** still lands in USD using that row’s **`Price in USD`** as **USD per 1 BRL** (see §3c bullets below). |
| **Inventory** | **Custom line** matching **`Currencies`!A** | **Positive** (e.g. `50` for fifty units) | Units received; **no second cash outflow** on a second row. |

- **`Amount` (column D) — numeric only:** Put **real numbers** in **D** (e.g. `-27.70`, `-180`, `50`). **Do not** store amounts as **text** (no currency symbols or thousands separators typed into the cell, no leading apostrophe to force text, no `"$…"` / `"R$…"` strings). **Text in D breaks downstream formulas** (`ARRAYFORMULA`, `SUM`, references from other tabs) that assume **D** is numeric. When using the **Sheets API** or CSV import, send **number** values for **D**, not quoted strings.
- **Standing convention — Matheus (Brazil):** **`Matheus Reis`** (exact **Contributors contact information** **Name**) **periodically purchases inventory for the DAO in Brazilian reais**, under **his fund custody** in Brazil (Ilhéus area). For these events **do not** require a long operator brief: receipt (or amount + date + what was bought + unit count), evidence paths, and transaction date are enough. Apply **both** legs with **`Fund Handler` = `Matheus Reis`**. **Inventory `Price in USD`** = **(R$ landed per unit) × (`Brazilian Reis` row `Price in USD`)**, with **R$ landed per unit** = receipt grand total ÷ units (tax-included unless policy says otherwise). **Do not** invent FX; use the **established** **`Brazilian Reis`** row unless treasury is updating it.
- **If the user has not already recorded the negative cash row** (**`USD`** or **`Brazilian Reis`**) for that purchase, **insert it**: parse the invoice/receipt for **grand total**, date, **`Fund Handler`** (ship-to rule **or** Matheus convention above), and links. **Do not** only add the positive inventory leg and assume the cash row exists.
- **Pairing:** The **positive inventory** row’s **Description** should cite the **sheet row number** of the **cash** leg (e.g. “pairs offchain row N…”), plus **order id**, **location**, and a **GitHub** link to archived evidence (see below). The **`Currency`** string on the inventory row must **exactly match** the **inventory** **`Currencies`** row’s column **A**. **Google Sheets:** do **not** start **Description** with **`+`** or **`=`** (formula interpretation); lead with words (e.g. “Received 4 units…”).

### **`Currencies` tab (unit “price” for the inventory leg)**

- **`Price in USD`:** Use **tax-included “landed”** unit cost in **USD**: **landed USD per unit = (invoice grand total ÷ unit count in local currency) × FX to USD** when the receipt is **not** in USD. For **BRL** receipts, use **`Brazilian Reis`** **`Price in USD`** (**USD per 1 BRL**). Example: R$180 for 4 units → R$45/unit → if **`Brazilian Reis`** is `0.2323`, **landed USD per unit** = `45 × 0.2323`.
- **New SKU / packaging:** Append a row (**A** = canonical name; **`Price in USD` = landed USD per unit**). Then **sort** the tab: **row 2 through last data row**, **all sheet columns in the grid** (e.g. **A through AC**), **A→Z by column A**, so **`VLOOKUP`** / **`ARRAYFORMULA`** on other tabs stay aligned and **no column is orphaned**.

### **Fund Handler (manager) from ship-to**

- **Ship-to** is **TrueTech Inc, 1423 Hayes St, San Francisco, CA 94117-1425, United States** (normalize minor formatting): **Fund Handler** = **`Kirsten Ritschel`** (exact **Name** in tab **Contributors contact information**).
- **Brazil — Matheus-managed BRL purchases (DAO inventory):** **Fund Handler** = **`Matheus Reis`** on **both** the **`Brazilian Reis`** cash leg and the **inventory** leg. This is **periodic** operational reality, not a one-off; see **standing convention** under **Double-entry** above. (Ilhéus / Brazil warehouse context: **`AGROVERSE_PRICE_LIST_AND_ASSETS.md`**, **`SUPPLY_CHAIN_AND_FREIGHTING.md`**.)
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
2. **Ensure negative cash row exists** on **`offchain transactions`** (**`USD`** or **`Brazilian Reis`**); if not, **add it** (amount = **-grand total** in that currency as a **numeric** **D** — see **Column D** bullet under **Double-entry** above). If the user points at an **existing** cash row, **skip** creating a duplicate cash line.
3. **GitHub `assets/`:** **Upload** only when there is **no** file yet (local invoice only, or missing link). If **`Destination Expense File Location`** already references **`TrueSightDAO/.github`**, use that **`blob`** URL in the inventory **Description**.
4. **Add or update `Currencies`** row (landed unit **= grand total ÷ qty**); **full-width sort** by column **A**.
5. **Add positive inventory row** on **`offchain transactions`**: **`Currency`** = **`Currencies`!A** exact string; **column D** = unit count (or agreed quantity) as a **number**, not text; **Description** links **cash row**, PDF **blob** URL, order id; **Fund Handler** per **ship-to**.

### **Sheet protection**

**`Currencies`** is often **range-protected**. Service accounts (e.g. **`agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com`**) may edit **`offchain transactions`** but still be blocked on **`Currencies`**. Remedies: editor **unprotect** / **exception** for that account, or human completes **`Currencies`** + **sort** in the UI.

---

## 3d. Beer Hall digest + oracle advisory snapshot

**Beer Hall WhatsApp posting via OpenClaw is RETIRED (2026-04-19).** The Beer Hall digest is now an **archive-only** artifact that feeds (a) the static Beer Hall feed at `ecosystem_change_logs/beer_hall/feed/` (read by truesight.me) and (b) `ADVISORY_SNAPSHOT.md` (read by the Grok advisor at `oracle.truesight.me`). It is **not** broadcast to WhatsApp. Community feedback (Kirsten, Fatima, Garis via Telegram log) flagged the WhatsApp firehose as too noisy; Fatima proposed a newsletter shape — this archive-only flow is the newsletter.

**Automation (no agent involvement required):**

- **`market_research/.github/workflows/advisory-snapshot-refresh.yml`** — runs every 6 h. Shallow-clones all 11 DAO sibling repos and publishes a fresh `ADVISORY_SNAPSHOT.md` to both `agentic_ai_context` and `ecosystem_change_logs` via the GitHub Contents API. Keeps the oracle's DAO context fresh between digests.
- **`market_research/.github/workflows/beer-hall-digest-daily.yml`** — runs daily at **00:00 UTC**. Generates the preview, drafts Message 1 + Message 2 via **Claude Sonnet 4.6** (`market_research/scripts/draft_beer_hall_digest.py`, which uses the latest 2 archives as few-shot style examples), runs `archive_beer_hall_changelog.py` on `ecosystem_change_logs`, refreshes the advisory snapshot, opens PRs on both target repos, and **auto-merges** them.

Both workflows need these repo secrets on `TrueSightDAO/go_to_market`: `ANTHROPIC_API_KEY`, `GOOGLE_CREDENTIALS_JSON`, `ORACLE_ADVISORY_PUSH_TOKEN` (fine-grained PAT with Contents + Pull-requests Read/Write on `ecosystem_change_logs` and `agentic_ai_context`).

**Local preview — "review recent progress":** Operators can still run `market_research/scripts/generate_beer_hall_preview.py` from a local `market_research/` clone (writes `agentic_ai_context/previews/beer_hall_preview_latest.md`). It emits the full Markdown on stdout — when the user asks to review recent progress, surface that output in the terminal transcript. The preview script no longer prints an OpenClaw `send` checklist; the operator checklist now points to `archive_beer_hall_changelog.py` + advisory snapshot refresh (both of which the daily workflow does automatically).

**GitHub URLs in the digest:** only `https://github.com/TrueSightDAO/...` — do not link personal or other-org repos (e.g. `garyjob`, `KrakeIO`).

**Historical / legacy context only:** `OPENCLAW_WHATSAPP.md` — kept for group JID reference, monitoring policy, and the history of the two-message send playbook. Do **not** follow its old closed-loop send instructions for Beer Hall; that path is retired. The `append_openclaw_beer_hall_log.py` sheet logger is also unused for the auto-archive flow.

---

## 3e. GitHub Actions and PR checks — **no long polling**

Assistants should **not** tie up the session waiting for GitHub Actions to finish. Avoid long or repeated waits such as **`gh pr checks --watch`**, **`gh run watch`** for many minutes, or tight loops of **`sleep`** + **`gh api …/actions/jobs/…`** until **`conclusion`** is set.

**Preferred workflow**

- After **`git push`** or updating a PR, optionally take **one** non-blocking snapshot: **`gh pr checks`**, **`gh pr view --json statusCheckRollup`**, **`gh run view <id>`**, or paste the **Actions** URL from **`gh pr view --web`**.
- When possible, **run the same checks locally** (for example in **`agroverse_shop/`**: **`npm run sitemap:check`**, **`npx playwright test …`**) so merge confidence does not depend on watching the remote runner.
- Give the user the **PR** and **workflow run** links; they can watch CI or merge when green. If the user explicitly asked to **merge**, merge only when checks are **already green** from a snapshot (or after the user confirms)—**do not** poll GitHub for extended periods to “babysit” the run.

**Related:** **`GITHUB_AGENTIC_AI_SSH.md` § Pull requests** (merge step: snapshot, not long watch).

---

## 4. Cross-Repo Relationships

- **dapp** ↔ **tokenomics**: DApp calls tokenomics APIs; see tokenomics API.md. **Apps Script edits:** implement and deploy from **`tokenomics/clasp_mirrors/<scriptId>/`** (clasp); **`tokenomics/google_app_scripts/`** is reference-only unless explicitly backported.
- **dapp** ↔ **holistic wellness Hit List (Sheets)**: `store_interaction_history.html` calls the read-only web app documented under **`tokenomics/google_app_scripts/holistic_hit_list_store_history/`** (Deployment URL in `store_interaction_history_api.gs`; DApp **`API_BASE_URL`** should match after redeploys). **Deploy changes** from the matching **`tokenomics/clasp_mirrors/<scriptId>/`** project (`clasp push`), not from the thematic folder alone. Spreadsheet: `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`. Partner workflow: **`PARTNER_OUTREACH_PROTOCOL.md`**, **`HIT_LIST_CREDENTIALS.md`** (market_research). **Email-agent open/click tracking:** Edgar **`/email_agent/open.gif`** and **`/email_agent/click`** (**TrueSightDAO/sentiment_importer**) update **Email Agent Drafts** columns **Open** / **Click through**; **go_to_market** scripts **`sync_email_agent_followup.py`**, **`regenerate_pending_email_agent_draft_tracking.py`**, and **`reconcile_email_agent_drafts_stale_sent.py`** keep Gmail, drafts tab, and **Email Agent Follow Up** aligned. For LLM subject/content tuning, **Email Agent Drafts** is the canonical engagement source — Follow Up L/M is frozen at send-time. See **`HIT_LIST_CREDENTIALS.md`** §"Performance analysis / LLM tuning — which sheet to use".
- **Hit List — Status = `Research` (automated Google Places photo review):** Treat **`Research`** rows as the queue for the same pipeline used for manual photo vetting: **`market_research/scripts/hit_list_research_photo_review.py`** resolves the store via **Google Places**, downloads public listing photos, runs **Grok** vision (`grok-4-1-fast-non-reasoning` or successor), appends a row on **`DApp Remarks`** (column **Remarks** / D is **multi-paragraph**, human-readable: location block, Places summary, bullet positives/negatives, model rationale), updates **Hit List** column **B** to **`AI: Shortlisted`**, **`AI: Photo rejected`**, or **`AI: Photo needs review`**, and appends **`Sales Process Notes`** using the **`[{Submitted At} | {Submitted By}]`** prefix pattern described in **`physical_stores/process_dapp_remarks.py`**. Use **`--shop "…"`** to target one shop by **substring** even if status is no longer `Research`. **Bulk append of `Research` leads (LA, SF Bay, future metros):** **`market_research/scripts/discover_apothecaries_la_hit_list.py --region la|sf_bay`** — Nearby Search + filters + sheet append; how to add regions and required keys are in **`market_research/HIT_LIST_CREDENTIALS.md`** § *Bulk discovery — append Research rows*. **GitHub Actions:** **`market_research/.github/workflows/hit_list_research_photo_review.yml`** — **`schedule`** hourly (UTC), default **`limit` 20** per run, plus **`workflow_dispatch`**; **`concurrency`** avoids overlapping runs. Secrets: **`GOOGLE_CREDENTIALS_JSON`**, **`GOOGLE_MAPS_API_KEY`**, **`GROK_API_KEY`** (**`GMAIL_TOKEN_JSON`** is unrelated). Local: **`market_research/.env`** plus **`google_credentials.json`**.
- **Hit List — Status = `AI: Enrich with contact` (website email / contact form):** Queue for **`market_research/scripts/hit_list_enrich_contact.py`**: fetch **Website** (or Places **website** using **`place_id`** in **Notes**), scan for emails + contact-form pages, optional **Grok** disambiguation, set **`AI: Email found`** / **`AI: Contact Form found`** / **`AI: Enrich — manual`** and fill **Email** or **Contact Form URL** when applicable. **Does not** append audit lines to **Hit List → Notes** (keep **Notes** for discovery / `place_id`). Each run appends **`DApp Remarks`** with **`[enrich-contact <ISO8601 Z>] outcome=…`** in column **Remarks**, **`Submitted By` = `hit_list_enrich_contact`**, then applies **Status**, **`Sales Process Notes`**, **Status Updated By/Date**, and marks the remark **Processed** via shared **`market_research/scripts/hit_list_dapp_remarks_sheet.py`** (same semantics as photo review / **`process_dapp_remarks.py`**). **Requires** Hit List columns **Sales Process Notes**, **Status Updated By**, **Status Updated Date**. **CI:** **`market_research/.github/workflows/hit_list_enrich_contact.yml`** — hourly **:35** UTC, default **10** rows; same Actions secrets as photo review. **Narrative / design notes:** **`HIT_LIST_CONTACT_ENRICHMENT.md`** in this repo.
- **Edgar** = **sentiment_importer** deployed at **`https://edgar.truesight.me`** (production). **Not** **`getdata.io`** — that host is **krake_ror** (see **§6**). DAO submission API; receives DApp contributions and triggers webhooks via Sidekiq (e.g. proposal → GitHub PR without waiting for cron). **Agroverse Shop checkout** calls **`GET https://edgar.truesight.me/agroverse_shop/shipping_rates`** first for USPS rate quotes (EasyPost; same behavior as Google Apps Script), with GAS fallback in **`agroverse_shop/js/checkout-shipping-calculator.js`**. **Inventory JSON refresh:** Sidekiq **`AgroverseInventorySnapshotPublishWorker`** hits GAS with **`AGROVERSE_INVENTORY_GAS_WEBAPP_URL`** + **`AGROVERSE_INVENTORY_PUBLISH_SECRET`** (host env on Edgar).
- **truesight_me** ↔ **tokenomics**: Static site data (e.g. shipments) can come from Google Sheets / tokenomics scripts.
- **Agroverse main ledger (`Currency` / product strings):** Codes like **`CP`…`BR`** embedded in pouch or ceremonial names are usually **Correios (Brazil Post) international package tracking numbers** for shipments from **Ilheus, Bahia** (often **Matheus’** / Oscar-adjacent origin) **to a destination in the United States**. They disambiguate a specific mailed batch when naming SKUs or composite ceremonial lines (e.g. `… + 8 Ounce Package Kraft Pouch CP340992735BR …`). See **`tokenomics/SCHEMA.md`** for sheet/column layout. For **repackaging and composite SKUs**, read **`LEDGER_CONVERSION_AND_REPACKAGING.md`** and **§3b** above (pointer).
- **agroverse_shop** ↔ **market_research** (GitHub repo **`go_to_market`**): Content and physical store scripts in market_research feed or sync with agroverse. **Automated publish of `agroverse-inventory` JSON:** workflow **`Publish Agroverse inventory snapshots`** (`.github/workflows/publish-agroverse-inventory-snapshot.yml`) runs `scripts/sync_agroverse_store_inventory.py --execute` on a schedule and pushes `store-inventory.json` + `partners-inventory.json` to **`TrueSightDAO/agroverse-inventory`**; requires repo secrets **`GOOGLE_CREDENTIALS_JSON`** and **`AGROVERSE_INVENTORY_PUSH_TOKEN`** on `go_to_market`. **Field media in `~/Downloads` (videos → blog/YouTube, images → assets):** read **`DOWNLOADS_MEDIA_TO_AGROVERSE.md`** in this repo. **Blog listing page (`agroverse_shop/blog/index.html`):** Card images MUST reference **`assets/images/blog/listing-640w/{post-slug}.jpg`** (resized for performance; built by **`agroverse_shop/scripts/sync_blog_listing_thumbnails.py`**). Source selection: prefer each **`post/<slug>/index.html`** first in-body image (skip nav logo; normalize relative `../../assets/` paths); ignore useless generic **`cacao-tasting-wheel.jpg`** as the only OG image for text-only posts. For fallbacks and breaking accidental duplicates (same file/hash or same Wix reuse id), use distinct shots from **`assets/images/blog/bahia-photo-library/`** and elsewhere in-repo. See **`PROJECT_INDEX.md`** (agroverse_shop row) and **`agroverse_shop/.cursor/rules/blog-listing-images.mdc`**. **Product development specs** (packaging, new SKUs): checklists live in **Google Sheets** (tabs per section); `market_research/scripts/populate_chocolate_bar_spec_sheet.py` can populate + style cells; read **`PRODUCT_DEVELOPMENT_SPECS.md`** in agentic_ai_context for the workflow and future AI behavior. **New PDP / SKU (do not skip):** after **`product-page/`** exists, add matching **`item-card`** rows on **`farms/*/index.html`** and **`shipments/agl*/index.html`** — **`AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md`**. **Default Drive folder** for new generated Sheet artifacts: `1esYnlwChRmv9-M3ymWYhWMPHRowhOluw` (link in that doc and in **`GOOGLE_API_CREDENTIALS.md`**). **Wholesale / import purchase agreement PDFs:** `market_research/purchase_agreements/` (ReportLab); read **`PURCHASE_AGREEMENT_PDFS.md`** before generating or extending agreements—farm canonical URLs (e.g. Oscar: `https://agroverse.shop/farms/oscar-bahia/index.html`), table/markup rules, deposit layout, and copy-from-script workflow.
- **Agroverse partner pages ↔ `Agroverse Partners` sheet (new canonical sync):** when adding/removing partner cards in `agroverse_shop/partners/index.html`, run `market_research/scripts/sync_agroverse_partners_sheet.py` (dry-run first, then `--execute`) to upsert rows in ledger tab **`Agroverse Partners`**. **Primary key is `partner_id` slug** (URL slug), and column **`contributor_contact_id`** uses dropdown validation from **`Contributors contact information!A:A`**. **Do not clear/rewrite the whole sheet**: preserve existing rows and manual edits; default behavior should append only missing `partner_id` records (optional `--refresh-existing-listing-fields` can refresh name/url/location only). Inventory pipeline extension: `market_research/scripts/sync_agroverse_store_inventory.py` emits `agroverse-inventory/partners-inventory.json` keyed by `partner_id` (each item includes `venueInventory`, `onlineInventory`, `availableOnline`). Partner PDPs load **`agroverse_shop/js/partner-catalog-snippets.js`** (raw GitHub JSON) to render snippets: **Add to Cart** only when the SKU is **retail**, **in `products.js`**, and **`availableOnline`**; otherwise show **in‑venue / limited release** copy with **no cart** and a PDP link.
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
- **Hit List contact enrichment** (`AI: Enrich with contact`, DApp Remarks parity): this repo **`HIT_LIST_CONTACT_ENRICHMENT.md`** — scripts, hourly CI, Notes vs DApp Remarks, shared `hit_list_dapp_remarks_sheet.py`. **`market_research/HIT_LIST_CREDENTIALS.md`** for CLI and secrets.
- **DApp UX**: dapp `UX_CONVENTIONS.md`.
- **AI agent → contribution ledger (`[CONTRIBUTION EVENT]`):** **`dao_client/`** — `python3 modules/report_ai_agent_contribution.py` with mandatory **`https://github.com/TrueSightDAO/.../pull/N`** URLs and an explicit body; credentials in **`dao_client/.env`**. Convention: this repo **`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`**. **Important:** `[CONTRIBUTION EVENT]` covers time *and* out-of-pocket expenses (Type: USD); `[CAPITAL INJECTION EVENT]` is **only** for external investors wiring funds into AGL-managed contracts.
- **DApp CI/testing**: dapp has unit tests (Node) and Playwright integration tests. Run `npm test` in `dapp/`. See dapp `tests/README.md`. CI: `.github/workflows/ci.yml` on push/PR to main. Pure logic in `expense-form-utils.js`; integration tests mock Google Apps Script and Edgar APIs (no real network calls).
- **Agroverse Shop CI/testing**: agroverse_shop has Playwright visual consistency tests. Run `npm test` in `agroverse_shop/`. See agroverse_shop `tests/README.md`. **Local runs hit `localhost:8000`** — Playwright auto-starts Python `http.server` on port 8000; ensure nothing else uses that port. CI (GitHub Actions) runs against live site (beta or prod). Workflow: `.github/workflows/visual-consistency.yml`. Smart runner: `npm run test:resume` to resume from failures. **Waiting on GitHub:** Section **§3e** — do not long-poll Actions; snapshot once or run tests locally; hand off URLs.
- **Downloads → Agroverse (videos + images):** **`DOWNLOADS_MEDIA_TO_AGROVERSE.md`** — video pipeline: `analyze_incoming_videos.py` → optional `youtube_batch_incoming.py` → `generate_video_transcript_blog_posts.py` (optional Grok polish). **After regen or any `youtube_videos.json` title change**, run **`youtube_update_video_titles.py`** so YouTube matches the manifest; if OAuth **`invalid_scope` / refresh fails**, use **`youtube_oauth_reauthorize.py`** then rerun the updater (details in that doc). **Images:** no dedicated Downloads automation; copy into `agroverse_shop/assets/images/…`, wire in HTML, run `sync_blog_listing_thumbnails.py`; blog card rules remain as in §4 (listing-640w, first in-body image, `bahia-photo-library` fallbacks).
- **Marketing / CMO consultation**: this repo `CMO_SETH_GODIN.md` — Agentic AI CMO (Seth Godin). Read when doing marketing activities to consult the CMO and operate based on his principles.
- **Strategy / onboarding**: this repo `DR_MANHATTAN.md` — Dr Manhattan. Read when doing strategy, growth, priorities, or onboarding for the DAO/Agroverse network. Future use: chatbot for newcomers.
- **Governance**: this repo `GOVERNANCE_SOURCES.md` — Whitepaper (truesight.me/whitepaper), proposals (GitHub TrueSightDAO/proposals, Realms). Pull whitepaper via `scripts/fetch_whitepaper.py`; browser for Realms.
- **Syndicate agreements**: this repo `SYNDICATE_AGREEMENTS.md` — Template and drafts in `notarizations/`. **Precedence:** Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee (avoid double-charging). Shipment Ledger as source. **PDF generation:** Use `notarizations/scripts/generate_syndicate_pdf.mjs` with TrueSight DAO logo header (`.github/assets/20221219 - Gary logo white background squarish.jpeg`).
- **TrueChain integration**: this repo `TRUECHAIN.md` — Private blockchain setup, mirror service, block explorer (GAS), schema evolution, product/shipment/farm, technical proposal. Repo: https://github.com/TrueSightDAO/TrueChain.
- **Agroverse serialized QR codes (sheet rows + local `batch_compiler.py`):** this repo **`AGROVERSE_QR_CODE_BATCH_GENERATION.md`** — tab **`Agroverse QR codes`**, naming (**`LA`**, **`CC`**, **`CT`**), columns **A–V**, column **I** ↔ **`Currencies`!A**, **`to_print/`** workflow. **`NOTES_tokenomics.md`** § *Agroverse QR codes tab* for shorthand.
- **Serialized QR bulk sales (post-minted QR codes):** `notes/claude_serialized_qr_sales_YYYY-MM-DD.md` (or newest matching) — one **`[SALES EVENT]`** per QR code (`Item` = QR code ID), `[INVENTORY MOVEMENT]` to deplete `offchain asset location`, and live GAS endpoint discovery (`?list_with_members=true`). Reusable template: **`dao_client/examples/bulk_qr_sales_template.py`**. See also **PROJECT_INDEX.md** `dao_client` row.
- **agroverse.shop new SKU (farm + shipment discovery grids):** this repo **`AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md`** — **`item-card`** on **`farms/`** and **`shipments/agl*/`** pages when adding **`product-page/`** PDPs; complements **`agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md`**.

---

## 6. Production domains and deployment sources

**Important:** The following domains are deployed from specific GitHub repos. Do not confuse workspace paths with deployment sources.

**Rails hosts (do not conflate):** **`getdata.io`** is the production deploy for **`krake_ror`** ([KrakeIO/krake_ror](https://github.com/KrakeIO/krake_ror)) — the Krake **data-harvesting** Rails app. **`edgar.truesight.me`** is the production deploy for **`sentiment_importer`** ([TrueSightDAO/sentiment_importer](https://github.com/TrueSightDAO/sentiment_importer)) — **“Edgar”** (DAO API, Sidekiq, Meta checkout, **`/agroverse_shop/shipping_rates`**, inventory snapshot workers, etc.). These are **different codebases** and **different servers**; do not assume APIs or env vars on one apply to the other.

| Domain | Deployed from (production source) | Notes |
|--------|-----------------------------------|-------|
| **truesight.me** | [TrueSightDAO/truesight_me_prod](https://github.com/TrueSightDAO/truesight_me_prod) | Main DAO landing page — production |
| **agroverse.shop** | [TrueSightDAO/agroverse_shop_prod](https://github.com/TrueSightDAO/agroverse_shop_prod) | E‑commerce — production |
| **getdata.io** | [KrakeIO/krake_ror](https://github.com/KrakeIO/krake_ror) | Krake Rails backend — **not** Edgar / sentiment_importer |
| **edgar.truesight.me** | [TrueSightDAO/sentiment_importer](https://github.com/TrueSightDAO/sentiment_importer) | **Edgar** — Rails **sentiment_importer** (DAO API, Sidekiq, Meta checkout helpers). Public: **`/agroverse_shop/shipping_rates`**, **`/meta_checkout`**, **`/ping`**, etc. **Not** krake_ror / getdata.io |

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
| `dao_client/` | https://github.com/TrueSightDAO/dao_client | — |
| `truesight_me/` | https://github.com/TrueSightDAO/truesight_me | → **truesight_me_prod** → truesight.me |
| `agroverse_shop/` | https://github.com/TrueSightDAO/agroverse_shop_beta | → **agroverse_shop_prod** → agroverse.shop |
| `market_research/` | https://github.com/TrueSightDAO/content_schedule |
| `agentic_ai_context/` | https://github.com/TrueSightDAO/agentic_ai_context |
| `TrueChain/` | https://github.com/TrueSightDAO/TrueChain |
| `krake_ror/` | https://github.com/KrakeIO/krake_ror | → **getdata.io** (Krake; not Edgar) |
| `sentiment_importer/` | https://github.com/TrueSightDAO/sentiment_importer | → **edgar.truesight.me** (Edgar; not getdata.io) |
| `krake_sinatra/` | https://github.com/KrakeIO/krake_sinatra |
| `krake_chrome/` | https://github.com/KrakeIO/Chrome |

Other projects (qr_codes, proposals, krake_local, fda_fsvp, jarvis, etc.) may be local-only or under different orgs; check `PROJECT_INDEX.md` GitHub column when added.

---

Keep this file and PROJECT_INDEX.md updated when adding or retiring repos so all AI assistants stay in sync.
