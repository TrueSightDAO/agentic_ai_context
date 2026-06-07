# Edgar → `dao_protocol` extraction — pre-flight + execution roadmap

**Goal:** Pull the DAO/Agroverse integration surface out of the Rails `sentiment_importer`
(Edgar) app into a Python FastAPI service (`dao_protocol`), leaving Edgar as a pure
stock/crypto trading platform. Migrate **one endpoint at a time** behind `edgar.truesight.me`
so clients never change and each step has instant rollback.

> ## ▶ RESUME HERE
>
> **▶ ACTIVE WORK (2026-06-07): PR8 — finish the `/dao/*` cutover (4 remaining endpoints).**
> Gary chose "finish cutover, then delete." The original extraction intentionally left
> 4 `/dao/*` routes on Rails (exact-match nginx only moved `submit_contribution`).
> Audit confirms **all 4 are in active use** (POS integrations + DApp + CLI) → each must
> be **ported**, not just deleted. Sequenced easy→hard in the **PR8 section at the bottom
> of this doc**; that section owns the live resume tracker for this phase. Prior phases
> (PR2–PR6b) remain DONE as described below.
>
> **Current step (prior phases):** **ALL endpoint ports + ALL 3 deferred impl gaps DONE & deployed gate-off;
> verified live on `:8010` 2026-05-26.** PR2 `/proxy/gas` + PR3 newsletter/email-agent tracking RAMPED LIVE (#34, #35),
> PR4 shipping_rates (#36, exact parity), PR5 `/dao` verify+intake+dispatch (#37/#38), PR6a
> `/qr-code-check` (#39), PR6b order-sync audit log `POST /stripe/order_sync` (#40); deferred gaps
> — inventory-snapshot enqueue + `/dao` attachment→GitHub (#41), EMAIL REGISTERED/VERIFICATION
> onboarding (#42) — all on `:8010`, **58 unit tests**. **Implementation is 100% complete.** DESCOPED
> per decision A: `/meta_checkout` (deprecated Wix) + the shared `/stripe_webhook` entry stay on
> Rails. Env provisioning DONE (23 keys, 2026-05-26). **PR2–PR6a RAMPED LIVE + PR6b ACTIVATED (Rails restarted 2026-05-26; delegation wiring verified) — all 6 routes cut over.** PR6a MINTED→Stripe-checkout redirect verified via a Stripe **test-mode sandbox** (2nd instance, sk_test). **Remaining = optional real-payment reconcile test + PR7 cleanup — see "Outstanding".** **Ramp + live testing of all
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
| PR3 | newsletter + email-agent tracking pixels (+ first `server/sheets/` adapter) | dao_protocol#35 | ✓ | ✓ | nginx | ✅ ramped live 2026-05-26 (302 parity vs Rails + journal-confirmed; live conf mirrored sentiment_importer#1066) |
| PR4 | `/agroverse_shop/shipping_rates` | dao_protocol#36 | ✓ | ✓ | nginx | ✅ ramped live 2026-05-26 (exact JSON parity vs Rails + CORS ACAO `*` + journal-confirmed; needed global CORS dao_protocol#44; conf mirrored #1067) |
| PR5a | RSA verifier (`crypto/verify.py`) | dao_protocol#37 | ✓ | ✓ | n/a (library) | n/a |
| PR5b | `/dao/submit_contribution` intake (verify + dedup + Telegram Chat Logs append) | dao_protocol#38 | ✓ | ✓ | **exact-match nginx flip** (operator chose full flip over Rails `split`) | ✅ ramped live 2026-05-26 (dogfood: real signed `[CONTRIBUTION]` POST → 200, sig verified, sheet-logged, journal-confirmed; exact-match so other `/dao/*` stay on Rails; conf mirrored #1068) |
| PR5c | dispatch (`webhook_trigger` + 17-branch event→webhook routing) | dao_protocol#38 | ✓ | ✓ | (with PR5b) | ☐ |
| PR6a | `/qr-code-check` (consumer QR→Stripe: lookup, MINTED→session, session_id→SOLD, /link-email; folds in old "PR4b" read path) | dao_protocol#39 | ✓ | ✓ | exact-match nginx flip | ✅ ramped live 2026-05-26 (read lookup verified on Python + journal; conf mirrored #1069). **Operator-test the payment paths**: MINTED→Stripe session, session_id→SOLD reconcile, /link-email write (real Stripe/sheets) |
| PR6b | order-sync audit log → `POST /stripe/order_sync` (`StripeCheckoutLog`); Rails delegates `checkout.session.completed`. **DESCOPED per decision A: `/meta_checkout` (deprecated Wix) + shared `/stripe_webhook` entry stay on Rails** | dao_protocol#40 | ✓ | ✓ | Rails webhook delegation | ✅ **ACTIVATED 2026-05-26** (sentiment_importer#1070 deployed; `systemctl restart seni_ror` done, Edgar healthy). Wiring verified: a synthetic `checkout.session.completed` → Rails delegated to Python (`POST /stripe/order_sync` from 127.0.0.1, journal-confirmed; webhook still acked 200 via the rescue). Real paid-session StripeCheckoutLog write = optional operator test |
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

**Build phase COMPLETE** — all clean Tenant B endpoints ported + deployed gate-off (PR2–PR6b, dao_protocol#33–#40) **plus all 3 deferred impl gaps closed (#41 + #42)**, 58 unit tests, every route verified live on `:8010`. **PR2–PR6a RAMPED LIVE + PR6b ACTIVATED (Rails restarted 2026-05-26) — all 6 routes cut over.** PR6a MINTED→Stripe-checkout redirect verified via a Stripe **test-mode sandbox** (2nd dao_protocol instance on `:8011` with the `sk_test` key from `development.rb`; MINTED code → 302 to `checkout.stripe.com/c/pay/cs_test_…`, no SOLD write). PR6b wiring verified (synthetic event → Rails→Python journal-confirmed). **No implementation work remains; env provisioning DONE. Remaining is operator-driven: optional real-payment reconcile→SOLD test, PR7 cleanup.** Remaining:

**1. Ramps (operator-driven — flip each gate to 100%, one at a time, Rails as rollback):**
- [x] PR3 newsletter + email-agent → nginx `location` flip in `seni_ror_new:edgar.conf` — ✅ **ramped live 2026-05-26** (302 parity vs Rails + dao_protocol journal-confirmed; live conf mirrored to repo #1066; rollback = drop the two `location` blocks + reload)
- [x] PR4 `/agroverse_shop/shipping_rates` → nginx exact-match flip — ✅ **ramped live 2026-05-26** (exact JSON parity vs Rails + CORS `ACAO: *` on GET/preflight + journal-confirmed; required adding global CORS to the app first, dao_protocol#44, mirroring Edgar rack-cors; conf mirrored #1067)
- [x] PR5 `/dao/submit_contribution` → ✅ **ramped live 2026-05-26** via **exact-match nginx flip** (operator chose full flip over Rails `split`). Dogfood: a real signed `[CONTRIBUTION]` POST returned 200 + sig verified + Telegram-logged + journal-confirmed (no ledger webhook for that event type). Exact-match `location` so the other `/dao/*` routes (cypher/canvas/check_digital_signature) stay on Rails. Webhook URLs already provisioned in `.env`; conf mirrored #1068. ⚠️ Other event types (SALES/MINT/etc.) now also flow through Python's dispatch → real GAS webhooks — operator should watch the first few of each in production
- [ ] PR6a `/qr-code-check` → flip (payment-critical)
- [x] PR6a `/qr-code-check` + `/link-email` → exact-match nginx flip ✅ **ramped live 2026-05-26** (read lookup verified on Python + journal; conf mirrored #1069). Payment paths (MINTED→Stripe session, session_id→SOLD, /link-email write) are operator-tested with real Stripe.
- [x] PR6b → ✅ delegation **merged** (sentiment_importer#1070): `webhook_controller#stripe` does a synchronous rescued localhost POST to `:8010/stripe/order_sync` for `checkout.session.completed`. ⏳ **Activates on next Rails web restart** (`systemctl restart seni_ror` on `seni_ror_new`) — until then `perform_async` (Sidekiq) still runs (current behavior). `/stripe_webhook` entry + subscription events stay on Rails.
- (PR2 `/proxy/gas` ✓, PR3 newsletter/email-agent ✓, PR4 shipping_rates ✓, PR5 `/dao/submit_contribution` ✓ already ramped)

**2. Env provisioning in box `.env` — DONE ✓ (2026-05-26).** Extracted the canonical runtime values from the live Rails process (loaded `/proc/<pid>/environ` for `SECRET_KEY_BASE` etc., then a `rails runner` read `Rails.application.config.*`) and merged into `/home/ubuntu/dao_protocol/.env` (chmod 600) — values never echoed. Service restarted; **23 keys** verified loaded (pydantic Settings for the 4 secrets; systemd `EnvironmentFile` puts the 19 webhooks into the process env for `dispatch.py`'s `os.environ` lookups). **Still gate-off** (env-only; no traffic moved).
- [x] `DAO_PROTOCOL_STRIPE_SECRET_KEY` (from `production.rb config.stripe_secret`, literal)
- [x] 19 `DAO_PROTOCOL_WEBHOOK_*` URLs (from `config.*_webhook_url` in `application.rb`; mix of literal + ENV-driven — all resolved non-empty)
- [x] `DAO_PROTOCOL_GITHUB_PAT` (literal in `application.rb`)
- [x] `DAO_PROTOCOL_EMAIL_VERIFICATION_GAS_WEBHOOK_URL` + `_GAS_SECRET` (ENV-driven via `config.email_verification_*`; resolved non-empty)
- [ ] `DAO_PROTOCOL_AGROVERSE_INVENTORY_GAS_WEBAPP_URL` + `_PUBLISH_SECRET` — **left empty: the HTTP publish path is dormant end-to-end, by omission not breakage** (verified 2026-05-26). (1) GAS project `1P0Mg33i…` (`update_store_inventory`) has only `AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT` in Script Properties — **no `AGROVERSE_INVENTORY_PUBLISH_SECRET`**, so `verifyPublishToken_` returns false and the HTTP actions `publishInventorySnapshot`/`recalculateAndPublishInventory` reject every call as Unauthorized. (2) the worker's `AGROVERSE_INVENTORY_*` env is unset on the **`seni_sk_new`** worker host (Sidekiq **is** running there — verified; the worker just hits its own "missing env" skip branch). [corrected 2026-05-26: an earlier note wrongly said Sidekiq was inactive — that was the vestigial unit on the *web* box; see NOTES_sentiment_importer.md topology warning]. (3) Inventory freshness comes from the GAS **time-driven hourly `updateStoreInventory` trigger** (pushes via the GIT_REPO_UPDATE_PAT), which needs no HTTP secret. dao_protocol `inventory_snapshot.publish()` no-ops, matching reality. **Enabling the immediate-after-sale refresh = net-new setup** (mint a secret → set GAS `AGROVERSE_INVENTORY_PUBLISH_SECRET` script property → set it + `/exec` URL in dao_protocol `.env` → optionally re-enable `seni_sk`), not a copy-existing-value task.
- ⚠️ **Blast-radius note:** with webhooks now populated, a *validly-signed* event POSTed to the `/dao-protocol/*` test prefix will fire **real** production GAS webhooks (propagate to real ledgers) — same as Rails. Agent never fires ledger-mutating events; operator dogfooding should use throwaway/own-key events.

**3. Deferred impl gaps — ALL PORTED ✓ (dao_protocol#41 + #42, deployed gate-off 2026-05-26):**
- [x] EMAIL REGISTERED / EMAIL VERIFICATION onboarding (`DaoEmailRegistrationService` + `Gdrive::ContributorsDigitalSignatures`) → `server/email_registration.py` + `server/sheets/contributors_digital_signatures.py`, wired into `routes/dao.py` (422 on failure). Server side is portable (only the *client* loopback was machine-bound). **#42.** Gate-off safe: empty `EMAIL_VERIFICATION_GAS_*` env → clean error (Rails parity). Also ported (post-soak bugfix 2026-05-28, **#45**): `DaoMembersCacheRefreshWorker` fan-out — `_trigger_dao_members_cache_refresh()` fires the GAS `refresh_dao_members_cache` action against the same publisher after a successful activation, best-effort. Was originally flagged "NOT ported (best-effort cache warm)" — that was wrong: without it the dapp's "is registered" check (reads `dao_members.json` cache) shows stale after a fresh verification, even though the sheet flipped to ACTIVE.
- [x] `/dao` attachment → GitHub upload → `server/services/github_upload.py`, wired into `routes/dao.py` (now returns real `fileUploadedToGithub`). **#41.** Needs `DAO_PROTOCOL_GITHUB_PAT` at ramp.
- [x] ASSET RECEIPT → inventory-snapshot enqueue → `server/jobs/inventory_snapshot.py` (GET `?action=&token=`, corrected shape), wired into `dispatch.py`. **#41.** Needs `AGROVERSE_INVENTORY_*` at ramp.
- intentionally **NOT ported** (stay on Rails): `/meta_checkout` (deprecated Wix); `/stripe_webhook` entry (shared with trading-SaaS subscriptions)

**Tenant B Sidekiq worker audit (2026-05-28, post-#45):** the entire Tenant B surface in `sentiment_importer` consists of just **4 Sidekiq workers**, and all 4 are now ported or bypassed — confirmed by sweeping `app/workers/` for HTTP-callers and cross-referencing DAO/Agroverse keywords. `AgroverseInventorySnapshotPublishWorker` → `jobs/inventory_snapshot.py` (#41); `WebhookTriggerWorker` → `jobs/webhook_trigger.py` + `dispatch.py` (#38); `MetaCheckoutOrderSyncWorker` → bypassed via the PR6b Rails-web delegation to `/stripe/order_sync`; `DaoMembersCacheRefreshWorker` → `email_registration._trigger_dao_members_cache_refresh` (#45). The ~96 other workers are Tenant A (trading: crypto, EODHD, intraday, market_cap, modelling, news, fundamentals, …) and stay on Rails. `HelloCashService` (POS-API client called from one of the non-ported `dao_controller` actions) is not a GAS caller and not in scope.

**4. PR7 cleanup + doc updates — DEFERRED ~30 days for ramp soak (revisit ~2026-06-25).** Captured as an OPEN_FOLLOWUPS entry ("Edgar → dao_protocol: post-soak cleanup"). Decision 2026-05-26: let the live ramps soak before removing the Rails controllers (they're the instant nginx-flip rollback net). When revisited:
- [ ] PR7: remove dead Tenant B controllers/workers from `sentiment_importer` — **phased + merge-not-deploy** (safe first: `MetaCheckoutOrderSyncWorker` + newsletter/email_agent/shipping_rates controllers; hold qr_code_check/proxy/dao#submit_contribution until reconcile soak-tested). Suggest PROJECT_INDEX/WORKSPACE_CONTEXT updates via CONTEXT_UPDATES.
- [ ] dao_protocol `README.md` — reframe "Edgar (source: sentiment_importer)" to reflect this repo now hosts the server (keep historical PR refs).
- [ ] truesight.me blog post — update its `sentiment_importer` reference to dao_protocol.

**5. Operator live testing (per test-execution policy):**
- [x] signed `/dao` submission → Python (dogfooded via `report_ai_agent_contribution`, 200 + sig verified + journal). [x] PR6b delegation wiring (synthetic event → Rails→Python). [x] PR6a MINTED→Stripe-checkout redirect via **test-mode sandbox** (`:8011` + `sk_test`; 302 → `cs_test_…`).
- [ ] **optional, operator:** complete a test/real Stripe checkout to exercise reconcile→SOLD + the real StripeCheckoutLog write (needs a publicly-reachable `success_url`; the sandbox `success_url` was localhost). EMAIL VERIFICATION loopback (own machine) if/when used.

**6. Minor hardening / open decisions:**
- [ ] rebind service to `127.0.0.1:8010` (still `0.0.0.0`; SG blocks externally)
- [ ] job durability: BackgroundTasks+APScheduler vs arq/Redis — decide at first ramp needing durable retries
- [ ] zero-lag inventory: keep snapshot refresh async vs synchronous on the sale path — decide at PR6a ramp

---

## PR8 — Finish the `/dao/*` cutover (the 4 routes intentionally left on Rails)

**Why now:** Gary (2026-06-07) wants the Rails DAO submit/dispatch surface retired to stop
LLMs (and humans) being confused by "two backends both accept `/dao/*`." PR5 only moved
`POST /dao/submit_contribution` (exact-match nginx). These 4 stayed on Rails by design — but
all 4 are **still live and still called**, so the cutover = *port → nginx flip → delete*, not
just delete.

**Usage audit (2026-06-07) — who calls each (so none is wrongly deleted as "dead"):**

| Rails route → action | Real callers | Backing | Port complexity |
|---|---|---|---|
| `POST /dao/verify-signature` → `dao#verify_signature` | dao_client CLI (`edgar_client.py`), heierling-pos, point-of-sales-integrations | `SignatureVerifier` only | **Trivial** — Python `crypto/verify.py` already exists; just map `{valid, message/error}` |
| `GET /dao/check_digital_signature` → `dao#check_digital_signature` | `dapp/create_signature.html`, butterfly_effects_club, dao_client CLI | `Gdrive::ContributorsDigitalSignatures.find_row_by_public_key` (+ Name/Email/Status) | **Low** — extend `sheets/contributors_digital_signatures.find_by_public_key` to also return Contributor Name; 3 response shapes + `ACAO:*` |
| `POST /dao/link_upc` → `dao#link_upc` | heierling-pos, point-of-sales-integrations (`create_invoice.html`) | `Gdrive::UpcBarcodeSheet.update_upc_code(product_id, upc_code)` | **Medium** — new `sheets/upc_barcode_sheet.py` adapter (single update) |
| `POST /dao/express_submit_contribution` → `dao#express_submit_contribution` | heierling-pos, point-of-sales-integrations (invoice flow) | `HelloCashService` (POS API) + `Gdrive::InvoicesSheet` + `UpcBarcodeSheet` + sig verify + Telegram log + GAS dispatch | **High** — new `services/hellocash.py` + `sheets/invoices_sheet.py`; reuses verify/dispatch/telegram_raw_log |

**Convention (same as every prior PR here):** build in `dao_protocol` **gate-off** (reachable via
the `/dao-protocol/*` test prefix, no traffic moved) with unit tests + exact-JSON parity vs live
Rails; ramp later via an **exact-match nginx `location =`** flip in `seni_ror:edgar.conf` (Rails stays
as instant rollback); only delete the Rails action in the final PR after soak. Each row is
independently shippable — stop after any unchecked box.

**Sequenced sub-PRs (easy→hard, lowest risk first):**

| Step | Scope | Impl PR | Merged | Deployed gate-off | nginx ramp | Rails delete |
|---|---|---|---|---|---|---|
| PR8a | `POST /dao/verify-signature` + `GET /dao/check_digital_signature` (read/verify only; reuse `crypto/verify` + sig-sheet adapter) | dao_protocol#62 | ✅ | ✅ 2026-06-07 (restart clean; 80 tests; **parity verified**: `check_digital_signature` exact-match vs live Rails for an ACTIVE key) | ☐ `location = /dao/verify-signature` + `location = /dao/check_digital_signature` | ☐ |
| PR8b | `POST /dao/link_upc` (+ `sheets/upc_barcode_sheet.py`) | dao_protocol#TBD | ☐ | ☐ | ☐ `location = /dao/link_upc` | ☐ |
| PR8c | `POST /dao/express_submit_contribution` (+ `services/hellocash.py` + `sheets/invoices_sheet.py`; [INVOICE CONTRIBUTION] + [UPC LINKING CONTRIBUTION]) | dao_protocol#TBD | ☐ | ☐ | ☐ `location = /dao/express_submit_contribution` | ☐ |
| PR8d | **Delete** the 4 Rails actions + routes + now-orphaned helpers/services (`HelloCashService`, `Gdrive::{UpcBarcodeSheet,InvoicesSheet}` if unused elsewhere) from `sentiment_importer`; **also** delete the already-ramped `submit_contribution` action (PR5, soaked since 2026-05-26). Merge-not-deploy first; this is the original **PR7 cleanup** for the `/dao/*` surface. | sentiment_importer#TBD | ☐ | n/a | n/a | ☐ |

**Keep on Rails (NOT in scope — Edgar-specific, no Python equivalent):** `dao#index`,
`dao#chrome_installed`, `dao#review_contribution` (human review UI + TDG award), `dao#cypher`,
`dao#canvas`, and the email-onboarding *that the DApp drives through Rails* — note `submit_contribution`'s
email-registration path was already ported (#42), so PR8d's delete of `submit_contribution` is safe, but
confirm `DaoEmailRegistrationService` has no *other* Rails caller before removing it.

**Pre-flight before PR8c (express):** confirm whether `HelloCashService` POS-invoice creation should
stay synchronous in-request (it returns invoice data the POS client reads back → yes, keep sync, matches
the "user-visible writes stay synchronous" decision). Confirm HelloCash API creds exist in the box `.env`
(`DAO_PROTOCOL_HELLOCASH_*` — likely NOT yet provisioned; net-new, like the inventory secret).

**Parity test harness:** for each, POST/GET the same payload to live Rails (`/dao/<route>`) and to the
gate-off Python (`http://127.0.0.1:8010/dao/<route>` on the box, or `/dao-protocol/...` prefix) and diff
the JSON (the POS/DApp clients depend on exact shape — `verify-signature` returns `{valid, message}`,
`check_digital_signature` returns `{registered, contributor_name, contributor_email}` /
`{registered:false, pending_verification:true,…}`).

> ⚠️ **Parity gotcha (found 2026-06-07):** live Rails applies a global `rate_limit_bot_calls`
> before_action that **401s curl/bot requests** (empty body) even on the skip-listed `/dao/*` actions —
> real browsers pass. So a naked `curl` to Rails returns 401, not the real payload. Send a browser
> `User-Agent` + `Origin: https://dapp.truesight.me` to get the true Rails response. The Python port
> intentionally does NOT replicate the bot-throttle (a Tenant-A/global concern), so it answers curl
> directly — confirmed identical JSON to browser-Rails for `check_digital_signature`. (Same class of
> latent Rails 401 that PR2 `/proxy/gas` fixed.)
