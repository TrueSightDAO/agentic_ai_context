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
- **Static sites**: truesight_me, agroverse_shop, dapp — often deployed to GitHub Pages or similar; design uses “Saffron Monk” / earthen palette where noted.
- **Ruby**: krake_ror, sentiment_importer use Rails; krake_sinatra uses Sinatra. Check README for Ruby/RVM version (e.g. 2.6.x).
- **Python**: market_research, video_editor, tokenomics scripts, jarvis — use venv and `requirements.txt` per project.
- **Node/TS**: krake_local, tokenomics (Raydium), iching_oracle — check for Node 18+ or 20+ and npm/pnpm.
- **APIs**: DApp and automation often talk to tokenomics backend/Google Apps Scripts; see tokenomics API.md and dapp UX_CONVENTIONS.md.

---

## 4. Cross-Repo Relationships

- **dapp** ↔ **tokenomics**: DApp calls tokenomics APIs; see tokenomics API.md.
- **Edgar** = **sentiment_importer** (edgar.truesight.me): DAO submission API; receives DApp contributions and triggers webhooks via Sidekiq (e.g. proposal → GitHub PR without waiting for cron).
- **truesight_me** ↔ **tokenomics**: Static site data (e.g. shipments) can come from Google Sheets / tokenomics scripts.
- **agroverse_shop** ↔ **market_research**: Content and physical store scripts in market_research feed or sync with agroverse.
- **krake_local** ↔ **krake_ror** / **krake_chrome**: Local tools and extension interact with Krake backend/services.
- **agentic_ai_api_credentials**: Reference only for env var names and which project uses them; no secrets.

---

## 5. Where to Look Next

- **Per-project details**: `PROJECT_INDEX.md` in this repo (purpose, stack, entry points, credentials reference).
- **Setup requirements**: `SETUP_REQUIREMENTS.md` in this repo — credential files needed per project (prompt user during setup).
- **Git / GitHub check-in**: Section **3a** above — never commit credentials or unnecessary library/build files; keep `.gitignore` updated and verify before push.
- **Env vars and API keys**: `agentic_ai_api_credentials/API_CREDENTIALS_DOCUMENTATION.md` and `env.template`.
- **DAO schema/API**: tokenomics `SCHEMA.md`, `API.md`.
- **Supply chain, freighting & unit-cost economics**: this repo `SUPPLY_CHAIN_AND_FREIGHTING.md` (inventory by location, freight options Brazil→US, cacao processing/cost; references SCHEMA.md).
- **DApp UX**: dapp `UX_CONVENTIONS.md`.
- **DApp CI/testing**: dapp has unit tests (Node) and Playwright integration tests. Run `npm test` in `dapp/`. See dapp `tests/README.md`. CI: `.github/workflows/ci.yml` on push/PR to main. Pure logic in `expense-form-utils.js`; integration tests mock Google Apps Script and Edgar APIs (no real network calls).
- **Agroverse Shop CI/testing**: agroverse_shop has Playwright visual consistency tests. Run `npm test` in `agroverse_shop/`. See agroverse_shop `tests/README.md`. **Local runs hit `localhost:8000`** — Playwright auto-starts Python `http.server` on port 8000; ensure nothing else uses that port. CI (GitHub Actions) runs against live site (beta or prod). Workflow: `.github/workflows/visual-consistency.yml`. Smart runner: `npm run test:resume` to resume from failures.
- **Marketing / CMO consultation**: this repo `CMO_SETH_GODIN.md` — Agentic AI CMO (Seth Godin). Read when doing marketing activities to consult the CMO and operate based on his principles.
- **Strategy / onboarding**: this repo `DR_MANHATTAN.md` — Dr Manhattan. Read when doing strategy, growth, priorities, or onboarding for the DAO/Agroverse network. Future use: chatbot for newcomers.
- **Governance**: this repo `GOVERNANCE_SOURCES.md` — Whitepaper (truesight.me/whitepaper), proposals (GitHub TrueSightDAO/proposals, Realms). Pull whitepaper via `scripts/fetch_whitepaper.py`; browser for Realms.
- **Syndicate agreements**: this repo `SYNDICATE_AGREEMENTS.md` — Template and drafts in `notarizations/`. **Precedence:** Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee (avoid double-charging). Shipment Ledger as source. **PDF generation:** Use `notarizations/scripts/generate_syndicate_pdf.mjs` with TrueSight DAO logo header (`.github/assets/20221219 - Gary logo white background squarish.jpeg`).

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
| `krake_ror/` | https://github.com/KrakeIO/krake_ror |
| `krake_sinatra/` | https://github.com/KrakeIO/krake_sinatra |
| `krake_chrome/` | https://github.com/KrakeIO/Chrome |

Other projects (qr_codes, proposals, krake_local, sentiment_importer, fda_fsvp, jarvis, etc.) may be local-only or under different orgs; check `PROJECT_INDEX.md` GitHub column when added.

---

Keep this file and PROJECT_INDEX.md updated when adding or retiring repos so all AI assistants stay in sync.
