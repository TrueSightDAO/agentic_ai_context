# Edgar → `dao_protocol` extraction — pre-flight + execution roadmap

**Goal:** Pull the DAO/Agroverse integration surface out of the Rails `sentiment_importer`
(Edgar) app into a Python FastAPI service (`dao_protocol`), leaving Edgar as a pure
stock/crypto trading platform. Migrate **one endpoint at a time** behind `edgar.truesight.me`
so clients never change and each step has instant rollback.

> ## ▶ RESUME HERE
> **Current step:** **ALL endpoint ports + ALL 3 deferred impl gaps DONE & deployed gate-off;
> verified live on `:8010` 2026-05-26.** PR2 `/proxy/gas` RAMPED LIVE (#34); PR3 tracking (#35),
> PR4 shipping_rates (#36, exact parity), PR5 `/dao` verify+intake+dispatch (#37/#38), PR6a
> `/qr-code-check` (#39), PR6b order-sync audit log `POST /stripe/order_sync` (#40); deferred gaps
> — inventory-snapshot enqueue + `/dao` attachment→GitHub (#41), EMAIL REGISTERED/VERIFICATION
> onboarding (#42) — all on `:8010`, **58 unit tests**. **Implementation is 100% complete.** DESCOPED
> per decision A: `/meta_checkout` (deprecated Wix) + the shared `/stripe_webhook` entry stay on
> Rails. **Remaining = operator-driven RAMPs + env provisioning + PR7 cleanup — see "Outstanding".** **Ramp + live testing of all
> gate-off endpoints (esp. /dao, Stripe) are operator-driven** (real ledger/GAS/Stripe) and need the
> `*_webhook_url` + `DAO_PROTOCOL_STRIPE_SECRET_KEY` env values provisioned in the box `.env`.
>
> **Dependency convention (operator choice 2026-05-25):** server deps live in `requirements-server.txt`
> (`-r requirements.txt` + web stack); CLI base in `requirements.txt`. NO pyproject `[server]` extra.
> Deploy installs with `pip install -e . -r requirements-server.txt`.
> Check the **Execution roadmap** table below for live status. Each PR is independently
> mergeable; stop after any row and continue later from the first unchecked box.
>
> ⚠️ **TOPOLOGY CORRECTION (verified 2026-05-25):** `edgar.truesight.me` resolves via **DNS
> directly to `seni_ror_new` (3.90.179.151)**, which runs its **own local nginx**
> (`/etc/nginx/sites-available/edgar.conf`, nginx 1.18) terminating `:443` → `127.0.0.1:3002`.
> **`krake_ng` is NOT the edgar front** — it's a separate shared proxy for *other* domains
> (truesight.me, getdata.io); its edgar block is stale/inert (`include sites-enabled` is even
> commented). Edit edgar routing in `edgar.conf` ON `seni_ror_new`, NOT on krake_ng. (This also
> means `deploy.sh` → `seni_ror_new` deploys ARE live, since DNS points straight there.)
>
> _Note: only the **GitHub repo + local git remote** were renamed. The local working dir is
> still `/Users/garyjob/Applications/dao_client/` and the importable package is still
> `truesight_dao_client` (both intentionally unchanged — path/import stability). Optional
> cosmetic follow-up: rename the local dir. Stale `TrueSightDAO/dao_client` URL references in
> canonical docs still 301-redirect; sweep them when convenient._

**Companion docs:**
- **`EDGAR_DAO_CUTOVER_TEST_PLAN.md`** — per-route cutover test checklist (run a route's block before ramping it). PR2 functional tests passed; documents the live-Rails `/proxy/gas` 401 finding + operator items.
- `STRIPE_LEDGER_ROUTING.md` — all 5 Stripe flows (incl. the consumer-QR Flow 5).
- Local scratch (gitignored, may be richer but not shared): `notes/claude_edgar_dao_extraction_2026-05-24.md`.

---

## Why this is cheap (the key finding)

`sentiment_importer` is two near-disjoint tenants:
- **Tenant A — trading platform** (stays in Rails): ~50 Postgres tables, ~80 market-data
  Sidekiq workers, heavy ActiveRecord. Includes the **`tsd/` prediction-game/betting cluster**
  (welded to `Company`/`DailyTrade`/`User`) and the **trading-SaaS Stripe billing**
  (`stripe_controller` subscriptions).
- **Tenant B — DAO/Agroverse glue** (extract to Python): `dao_controller` (1231 LOC, ~zero
  ActiveRecord), shipping rates, meta checkout, newsletter/email-agent tracking, GAS proxy,
  QR check. Data layer is almost entirely `app/models/gdrive/*` (Sheets) + `signature_verifier.rb`.
  **No DAO controller references any trading model → no shared DB to untangle.**

~60% of the protocol already exists in Python: `dao_client` owns signing (`edgar_client.py`),
read caches (`truesight_dao_client/cache/*`), and a proven `Gdrive::*`→Python port
(`dapp_digital_signature_onboarding/demo_edgar_digital_signature_sheet_flow.py`).

---

## Decisions (ratified with Gary, 2026-05-24)

| # | Decision |
|---|----------|
| Repo | Rename `dao_client` → **`dao_protocol`** (GitHub redirects old URLs). Keep importable package `truesight_dao_client` so imports/CLI don't break. Server lives here behind a `[server]` extra. |
| Host | Run `dao_protocol` FastAPI on **`seni_ror_new`** (Edgar app box) on **:8010**, own systemd unit. Bind reachable only via the box's local nginx (no external SG rule needed — localhost hop). |
| Proxy | Add `location` blocks to the **real edgar nginx** on `seni_ror_new` itself: `/etc/nginx/sites-available/edgar.conf` (nginx 1.18), proxying Tenant B paths to `http://127.0.0.1:8010/`; `location /` stays `127.0.0.1:3002` (Rails). **NOT krake_ng** — see topology correction. |
| No clash | tokenomics is GAS on Google's servers — untouched. This replaces Edgar's **Rails** role only. |
| No race | **User-visible writes stay synchronous in-request** to the source of truth (matches today). Async only for downstream propagation the DApp doesn't read back immediately. Each path owned by exactly ONE service at a time (atomic nginx flip) → no dual-write race. |

**Edgar prod topology (CORRECTED, verified 2026-05-25):** `edgar.truesight.me` → DNS →
**`seni_ror_new` (3.90.179.151) directly**. That box runs its own local nginx 1.18
(`/etc/nginx/sites-available/edgar.conf`) terminating `:443` (Let's Encrypt) → `127.0.0.1:3002`
(Rails, `/home/ubuntu/sentiment_importer`). `dao_protocol` runs on the same box (`:8010`).
Sidekiq on `seni_sk_new` (54.163.216.235). **`krake_ng` (54.226.114.186 :2202) is a SEPARATE
shared proxy for truesight.me / getdata.io etc. — NOT the edgar front** (the `~/.ssh/config`
comment and the old `nginx_krake_ng.conf` edgar block are stale/misleading).
Bare `seni_ror`/`seni_sk` aliases = dead Cypher IPs (forensics only — do NOT deploy there).

---

## Pre-flight checklist (verify BEFORE writing endpoint code)

- [ ] SSH reachable: `seni_ror_new`, `seni_sk_new`, `krake_ng` (port 2202).
- [ ] Confirm a free internal port on `seni_ror_new` (proposed **:8010**) not used by Rails/other.
- [ ] Locate Edgar's service-account JSON for Sheets writes (`config/agroverse_qr_code_gdrive_key.json`
      + any others under `sentiment_importer/config/`) — `dao_protocol` needs equivalents.
- [ ] Inventory Tenant B env/secrets on Edgar: Stripe secret key, EasyPost key, GitHub PAT
      (invoice/asset upload), GAS shared secrets, `AGROVERSE_INVENTORY_*`.
- [ ] Confirm `dao_client` auth is active for contribution reporting (`auth.py status`).
- [ ] Snapshot `seni_ror_new:/etc/nginx/sites-available/edgar.conf` before any edit (this is the real edgar nginx — NOT krake_ng).
- [ ] Python runtime available on `seni_ror_new` (venv strategy; don't collide with system py).

---

## Migration gating strategy (decoupled build vs cutover, 2026-05-25)

**Each Python PR is implementation ONLY** — build the endpoint in `dao_protocol`, test it, ship it
(reachable for testing via the `/dao-protocol/...` prefix). It carries **no production traffic**
until a **separate, reversible "ramp" step** opens a per-route gate. This decouples "is the code
done" from "is traffic cut over," so a half-migrated route is never a half-broken route.

**Two-tier gate, chosen per endpoint type:**
- **Anonymous / pass-through / read** (`proxy/gas`, `shipping_rates`, newsletter+email-agent
  pixels, `qr-code-check` read): gate at **nginx** on `seni_ror_new` (`edgar.conf`, nginx 1.18) via
  **`split_clients`** percentage canary to `:8010`; optionally **`mirror`** to shadow-compare
  responses before ramping. Rails stays out of the path.
- **Identity-bearing / risky writes** (`/dao/submit_contribution`; Stripe where comparison is
  wanted): gate **in Rails** via the already-installed **`split`** gem (`/admin/split`), keyed on
  **contributor identity** so we migrate our own signature first, compare, then ramp the cohort.
  Rails proxies the chosen cohort to `:8010` and keeps its own handler as the control until 100%.

**Safety rule for write endpoints** (`/dao`, `/stripe_webhook`): the gate must route each request
to **exactly one** backend (never both) — rely on identity-stickiness or a hard flip, never a
random per-request split, and lean on existing idempotency (Telegram Update ID, Stripe session id).
`mirror`/shadow is read-only.

## Implementation plan (sequenced PRs — Python impl only; ramp is separate)

Each `PRn` below = **implement endpoint X in Python + tests, gate default OFF**. Cutover is a
distinct **"ramp X"** step (flip the `split_clients` % or the `split`-gem cohort), reversible, with
the Rails handler as instant rollback until PR7.

- **PR0 — Repo rename.** `dao_client` → `dao_protocol` (GitHub Settings → rename). Update local
  remote + hardcoded `TrueSightDAO/dao_client` doc references. Keep package name. No behavior change.
- **PR1 — Scaffold + first slice.** `truesight_dao_client/server/` (`main.py`, `config.py`,
  `routes/health.py`), `[server]` extra in `pyproject.toml`, `server/deploy/` (deploy script +
  systemd unit modeled on Edgar `deploy.sh`). Deploy to `seni_ror_new:8010`; add health
  `location` on `krake_ng`. Proves the pipeline end-to-end.
- **PR2 — `/proxy/gas/:name`.** Port allowlist from Rails `proxy_controller` (lockstep with
  `dapp/routes.js` Routes.gas.*). Pure pass-through. Flip nginx.
- **PR3 — Sheets adapter + tracking.** `server/sheets/base.py` (lift from `demo_edgar_*`) +
  `NewsletterEmails`/`EmailAgentDrafts` ports; `/newsletter/{open.gif,click}` +
  `/email_agent/{open.gif,click}`. Flip nginx.
- **PR4 — `/agroverse_shop/shipping_rates`.** `server/services/easypost.py`. Read-only; parity
  vs Rails; confirm agroverse_shop GAS fallback still covers errors. Flip nginx.
- **PR5 — `/dao/*` (crown jewel).** `server/crypto/verify.py` (port `signature_verifier.rb`),
  `/dao/submit_contribution` + event dispatch, `jobs/webhook_trigger.py`. Decide job durability.
  User-visible Sheet writes SYNCHRONOUS before responding. Heavy parity testing. Flip nginx.
- **PR6 — Stripe cluster (last, payment-critical).** `/qr-code-check` (session create on MINTED
  + `?session_id=` reconcile), `/meta_checkout` + `/meta-success`, `/stripe_webhook` →
  `meta_checkout_order_sync` port. Provision shared Stripe secret key on `seni_ror_new`. Decide
  zero-lag-inventory question. Flip nginx.
- **PR7 — Cleanup.** Remove dead Tenant B controllers/workers from `sentiment_importer`. Suggest
  PROJECT_INDEX/WORKSPACE_CONTEXT updates via CONTEXT_UPDATES (don't edit canonical docs directly).

---

## Execution roadmap / resume tracker

Update this table as work lands. **"Continue from the first row that isn't `merged ✓`."**
Per project convention: after each PR merges, **report the DAO contribution** before starting
the next phase.

**Foundation (done):**

| Step | Scope | PR | Merged | Contrib |
|------|-------|----|--------|---------|
| Planning/docs | This plan + `STRIPE_LEDGER_ROUTING.md` Flow 5 | agentic_ai_context#185 | ✓ | ✓ |
| PR0 | Repo rename `dao_client`→`dao_protocol` | _(settings rename)_ | ✓ | ✓ |
| PR1a | Scaffold `server/` + `[server]` extra + `/ping`,`/healthz` | dao_protocol#33 | ✓ | ✓ |
| PR1b | Deploy `seni_ror_new:8010` (systemd) + `/dao-protocol/*` test route live & verified | _(server deploy)_ | ✓ | ✓ |

**Endpoint ports (Python impl + separate ramp). Continue from first row not `impl ✓`:**

| Step | Endpoint | Impl PR | Impl merged | Contrib | Gate | Ramp→100% |
|------|----------|---------|-------------|---------|------|-----------|
| PR2 | `/proxy/gas/:name` | dao_protocol#34 | ✓ | ✓ | nginx hard-flip (Rails was 401) | ✅ ramped live 2026-05-25 (fixed the latent Rails 401) |
| PR3 | newsletter + email-agent tracking pixels (+ first `server/sheets/` adapter) | dao_protocol#35 | ✓ | ✓ | nginx | ☐ (impl done + deployed; ramp pending) |
| PR4 | `/agroverse_shop/shipping_rates` | dao_protocol#36 | ✓ | ✓ | nginx (+mirror shadow) | ☐ (impl done; **exact parity vs Rails verified**) |
| PR5a | RSA verifier (`crypto/verify.py`) | dao_protocol#37 | ✓ | ✓ | n/a (library) | n/a |
| PR5b | `/dao/submit_contribution` intake (verify + dedup + Telegram Chat Logs append) | dao_protocol#38 | ✓ | ✓ | Rails `split` by contributor | ☐ (impl+deployed; webhook URLs + live test at ramp) |
| PR5c | dispatch (`webhook_trigger` + 17-branch event→webhook routing) | dao_protocol#38 | ✓ | ✓ | (with PR5b) | ☐ |
| PR6a | `/qr-code-check` (consumer QR→Stripe: lookup, MINTED→session, session_id→SOLD, /link-email; folds in old "PR4b" read path) | dao_protocol#39 | ✓ | ✓ | Rails `split` / hard flip | ☐ (impl+deployed; lookup verified live; Stripe key + live sale at ramp) |
| PR6b | order-sync audit log → `POST /stripe/order_sync` (`StripeCheckoutLog`); Rails delegates `checkout.session.completed`. **DESCOPED per decision A: `/meta_checkout` (deprecated Wix) + shared `/stripe_webhook` entry stay on Rails** | dao_protocol#40 | ✓ | ✓ | Rails webhook delegation | ☐ (impl+deployed; wire delegation + Stripe key at ramp) |
| PR7 | Remove dead Tenant B code from Edgar (after all ramped 100%) | — | ☐ | ☐ | n/a | n/a |

---

## Migration order rationale (lowest-risk first)

1. `/ping` → 2. `/proxy/gas` (pass-through) → 3. newsletter/email-agent tracking (append-only,
analytics-only blast radius) → 4. `/agroverse_shop/shipping_rates` (read-only, GAS fallback) →
5. `/dao/*` (RSA crown jewel) → 6. **Stripe cluster last** (payment-critical, shares Stripe key;
`/qr-code-check` is NOT read-only — it creates sessions + writes sales).

## Tenant B endpoint → backing reference

| Endpoint | Backing | Async worker |
|---|---|---|
| `/dao/*` submit_contribution (RSA) | Sheets + GitHub + dispatch | webhook_trigger_worker |
| `/agroverse_shop/shipping_rates` | EasyPost | — |
| `/meta_checkout`, `/meta-success` | Sheets + shipping calc | meta_checkout_order_sync_worker |
| `/newsletter/{open.gif,click}` | Gdrive::NewsletterEmails | — |
| `/email_agent/{open.gif,click}` | Gdrive::EmailAgentDrafts | — |
| `/proxy/gas/:name` | pass-through allowlist | — |
| `/qr-code-check` (+ `/stripe_webhook`) | Gdrive::QrCodeLookup + Stripe | inventory_snapshot_publish |
| `/ping` | health | inventory_snapshot_publish, dao_members_cache_refresh (scheduled) |

## PR5 detail — `/dao/submit_contribution` intake + dispatch (crown jewel)

**PR5a — RSA verifier: DONE** (dao_protocol#37, `server/crypto/verify.py`; validated vs the real example payload).

**PR5b — intake** (`POST /dao/submit_contribution`): 1) verify via `crypto/verify.py` →
`signature_verification` = success|failed|no_signature_format|error; 2) on success: dedup by the
Request-Transaction-ID signature (→ 409 if already processed) + resolve governor authority
(`Gdrive::Governors`); 3) append the signed text to **Telegram Chat Logs**
(`Gdrive::TelegramRawLog.add_record` → new `sheets/telegram_raw_log.py`); 4) `[RETAIL FIELD REPORT
EVENT]` also archived; 5) on success → dispatch (PR5c); respond `{status, signature_verification, …}`.
⚠️ **Writes the REAL Telegram Chat Logs ledger** → build gate-OFF + mocked tests; live testing operator-driven (own key).

**PR5c — dispatch** (port `WebhookTriggerWorker` → `jobs/webhook_trigger.py`: HTTP GET `?action=`,
30s timeout, retry, dup-processing lock — Redis in Rails; in-process lock / `arq` here). Event-tag →
(Rails `config.*_webhook_url`, action):

| Event tag | config key (`*_webhook_url`) | action |
|---|---|---|
| `[SALES EVENT]` | sales_processing, sales_agl4, sales_non_agl4 | parseTelegramChatLogs / processTokenizedTransactions / processNonAgl4Transactions |
| `[INVENTORY MOVEMENT]` | inventory_processing | processTelegramChatLogs |
| `[DAO Inventory Expense Event]` | expense_processing | parseAndProcessTelegramLogs |
| `[QR CODE UPDATE EVENT]` | qr_code_update | processQrCodeUpdatesFromTelegramChatLogs |
| `[DAPP PERMISSION CHANGE EVENT]` | dapp_permission_change | apply_permission_change |
| `[WARMUP SEND EVENT]` | warmup_send | apply_warmup_send |
| `[BATCH QR CODE REQUEST]` | qr_code_generation | processQRCodeGenerationTelegramLogs |
| `[PROPOSAL CREATION]` / `[PROPOSAL VOTE]` | proposal_processing | process_dapp_payloads |
| `[REPACKAGING BATCH EVENT]` | repackaging_processing | processRepackagingBatchesFromTelegramChatLogs |
| `[CURRENCY CONVERSION EVENT]` | currency_conversion_processing | parseAndProcessCurrencyConversionLogs |
| `[RETAIL FIELD REPORT EVENT]` | retail_field_report_processing | processRetailFieldReportsFromTelegramChatLogs |
| `[STORE ADD EVENT]` | store_add_processing | processStoreAddsFromTelegramChatLogs |
| `[DONATION MINT EVENT]` | donation_mint_processing | processDonationMintsFromTelegramChatLogs |
| `[CONTRIBUTOR ADD EVENT]` | contributor_add_processing | processContributorAddsFromTelegramChatLogs |
| `[CREDENTIALING ATTESTATION EVENT]` | credentialing_attestation | process_attestation_events |
| `[PARTNER CHECK-IN EVENT]` | partner_check_in_processing | processPartnerCheckInsFromTelegramChatLogs |
| `[ASSET RECEIPT EVENT]` | asset_receipt_processing | processAssetReceiptsFromTelegramChatLogs (+ enqueue inventory snapshot) |

Webhook URLs live in Rails `config/application.rb`/env (`*_webhook_url`) → provision the equivalents
in the dao_protocol box `.env` server-side (like the EasyPost key). Dispatch is non-user-visible
propagation → may run async; the **intake ledger append stays synchronous** (no-race rule).

## Outstanding (2026-05-26 audit)

**Build phase COMPLETE** — all clean Tenant B endpoints ported + deployed gate-off (PR2–PR6b, dao_protocol#33–#40) **plus all 3 deferred impl gaps closed (#41 + #42)**, 58 unit tests, every route verified live on `:8010`. PR2 `/proxy/gas` ramped. **No implementation work remains — everything below is operator-driven (ramps, env, live testing, PR7 cleanup).** Remaining:

**1. Ramps (operator-driven — flip each gate to 100%, one at a time, Rails as rollback):**
- [ ] PR3 newsletter + email-agent → nginx `location` flip in `seni_ror_new:edgar.conf`
- [ ] PR4 `/agroverse_shop/shipping_rates` → nginx flip (optionally `mirror`-shadow first)
- [ ] PR5 `/dao/submit_contribution` → Rails `split` by contributor (dogfood own key first)
- [ ] PR6a `/qr-code-check` → flip (payment-critical)
- [ ] PR6b → wire Rails `/stripe_webhook` to delegate `checkout.session.completed` → `POST /stripe/order_sync`
- (PR2 `/proxy/gas` already ramped ✓)

**2. Env provisioning in box `.env` (server-side at ramp, like the EasyPost key):**
- [ ] `DAO_PROTOCOL_STRIPE_SECRET_KEY` (from Rails `production.rb config.stripe_secret`) — PR6a/PR6b
- [ ] 15 `DAO_PROTOCOL_WEBHOOK_*` URLs (from Rails `config.*_webhook_url`) — PR5c dispatch
- [ ] `DAO_PROTOCOL_GITHUB_PAT` (contents-write to TrueSightDAO repos) — `/dao` attachment upload
- [ ] `DAO_PROTOCOL_AGROVERSE_INVENTORY_GAS_WEBAPP_URL` + `_PUBLISH_SECRET` — ASSET RECEIPT inventory snapshot
- [ ] `DAO_PROTOCOL_EMAIL_VERIFICATION_GAS_WEBHOOK_URL` + `_GAS_SECRET` — EMAIL onboarding mailer (from Rails `config.email_verification_*`)

**3. Deferred impl gaps — ALL PORTED ✓ (dao_protocol#41 + #42, deployed gate-off 2026-05-26):**
- [x] EMAIL REGISTERED / EMAIL VERIFICATION onboarding (`DaoEmailRegistrationService` + `Gdrive::ContributorsDigitalSignatures`) → `server/email_registration.py` + `server/sheets/contributors_digital_signatures.py`, wired into `routes/dao.py` (422 on failure). Server side is portable (only the *client* loopback was machine-bound). **#42.** Gate-off safe: empty `EMAIL_VERIFICATION_GAS_*` env → clean error (Rails parity). NOT ported: `DaoMembersCacheRefreshWorker` fan-out (best-effort cache warm).
- [x] `/dao` attachment → GitHub upload → `server/services/github_upload.py`, wired into `routes/dao.py` (now returns real `fileUploadedToGithub`). **#41.** Needs `DAO_PROTOCOL_GITHUB_PAT` at ramp.
- [x] ASSET RECEIPT → inventory-snapshot enqueue → `server/jobs/inventory_snapshot.py` (GET `?action=&token=`, corrected shape), wired into `dispatch.py`. **#41.** Needs `AGROVERSE_INVENTORY_*` at ramp.
- intentionally **NOT ported** (stay on Rails): `/meta_checkout` (deprecated Wix); `/stripe_webhook` entry (shared with trading-SaaS subscriptions)

**4. PR7 cleanup (only AFTER all ramped 100%):**
- [ ] Remove dead Tenant B controllers/workers from `sentiment_importer`; suggest PROJECT_INDEX/WORKSPACE_CONTEXT updates via CONTEXT_UPDATES.

**5. Operator live testing (per test-execution policy):**
- [ ] dogfood signed `/dao` events (own key); Stripe test-mode checkout; EMAIL VERIFICATION loopback (own machine); real MINTED QR sale → SOLD.

**6. Minor hardening / open decisions:**
- [ ] rebind service to `127.0.0.1:8010` (still `0.0.0.0`; SG blocks externally)
- [ ] job durability: BackgroundTasks+APScheduler vs arq/Redis — decide at first ramp needing durable retries
- [ ] zero-lag inventory: keep snapshot refresh async vs synchronous on the sale path — decide at PR6a ramp
