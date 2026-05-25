# Edgar → `dao_protocol` extraction — pre-flight + execution roadmap

**Goal:** Pull the DAO/Agroverse integration surface out of the Rails `sentiment_importer`
(Edgar) app into a Python FastAPI service (`dao_protocol`), leaving Edgar as a pure
stock/crypto trading platform. Migrate **one endpoint at a time** behind `edgar.truesight.me`
so clients never change and each step has instant rollback.

> ## ▶ RESUME HERE
> **Current step:** PR1 **code scaffold merged** (dao_protocol#33: `server/` package, `[server]`
> extra, `/ping` + `/healthz`, deploy.sh + systemd unit; validated locally — both health routes
> 200, OpenAPI builds). **Remaining = PR1b, the live deploy:** install/run on `seni_ror_new:8010`
> (systemd unit shipped in `truesight_dao_client/server/deploy/`) + add the nginx `location` flip
> on the **shared** `krake_ng` proxy. That step touches prod infra (SSH + sudo + shared nginx) and
> needs explicit operator go-ahead — do NOT rush it.
> Check the **Execution roadmap** table below for live status. Each PR is independently
> mergeable; stop after any row and continue later from the first unchecked box.
>
> _Note: only the **GitHub repo + local git remote** were renamed. The local working dir is
> still `/Users/garyjob/Applications/dao_client/` and the importable package is still
> `truesight_dao_client` (both intentionally unchanged — path/import stability). Optional
> cosmetic follow-up: rename the local dir. Stale `TrueSightDAO/dao_client` URL references in
> canonical docs still 301-redirect; sweep them when convenient._

**Companion docs:**
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
| Host | Run `dao_protocol` FastAPI on **`seni_ror_new`** (Edgar app box) on **:8010**, own systemd unit. |
| Proxy | Add `location` blocks on **`krake_ng`** (nginx, SSH :2202, SHARED proxy) routing Tenant B paths to `seni_ror_new:8010`; everything else stays at `:3002` (Rails). |
| No clash | tokenomics is GAS on Google's servers — untouched. This replaces Edgar's **Rails** role only. |
| No race | **User-visible writes stay synchronous in-request** to the source of truth (matches today). Async only for downstream propagation the DApp doesn't read back immediately. Each path owned by exactly ONE service at a time (atomic nginx flip) → no dual-write race. |

**Edgar prod topology** (from `~/.ssh/config` + `sentiment_importer/deploy.sh`):
`krake_ng` (54.226.114.186 :2202, nginx) → `seni_ror_new` (3.90.179.151, Rails :3002,
`/home/ubuntu/sentiment_importer`); Sidekiq on `seni_sk_new` (54.163.216.235).
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
- [ ] Snapshot `krake_ng`'s nginx config (the `edgar.truesight.me` server block) before any edit.
- [ ] Python runtime available on `seni_ror_new` (venv strategy; don't collide with system py).

---

## Implementation plan (sequenced PRs)

Each endpoint PR ends with an nginx `location` flip on `krake_ng`; Rails handler stays as
instant rollback until PR7.

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

| Step | Scope | PR | Merged | Contribution reported |
|------|-------|----|--------|-----------------------|
| Planning/docs | This plan + `STRIPE_LEDGER_ROUTING.md` Flow 5 | agentic_ai_context#185 | ✓ | ✓ |
| PR0 | Repo rename `dao_client`→`dao_protocol` (GitHub + remote) | _(settings rename)_ | ✓ | ✓ |
| PR1a (code) | Scaffold `server/` + `[server]` extra + `/ping`/`/healthz` (validated) | dao_protocol#33 | ✓ | ✓ |
| PR1b (deploy) | Deploy to `seni_ror_new:8010` + nginx `location` flip on shared `krake_ng` | — | ☐ | ☐ |  ◀ RESUME HERE (needs go-ahead) |
| PR2 | `/proxy/gas/:name` | — | ☐ | ☐ |
| PR3 | Sheets adapter + newsletter/email-agent tracking | — | ☐ | ☐ |
| PR4 | `/agroverse_shop/shipping_rates` | — | ☐ | ☐ |
| PR5 | `/dao/*` submit_contribution (verify + dispatch) | — | ☐ | ☐ |
| PR6 | Stripe cluster (qr-code-check + meta_checkout + webhook) | — | ☐ | ☐ |
| PR7 | Remove dead Tenant B code from Edgar | — | ☐ | ☐ |

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

## Still open
- [ ] Job durability: BackgroundTasks+APScheduler vs arq/Redis — decide at PR5.
- [ ] Zero-lag inventory: keep `AgroverseInventorySnapshotPublishWorker`-style refresh async
      (matches today) vs synchronous on the sale path — decide at PR6.
