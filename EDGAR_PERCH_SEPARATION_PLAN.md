# Edgar / Perch Separation Plan

> **Goal:** Split the `sentiment_importer` (Edgar) into two distinct services with
> separate identities, domains, SSL certs, and Stripe webhook endpoints.
>
> Authorized by Gary in Telegram thread 3, 2026-06-13.

---

## The Two Identities

### Edgar — The DAO Protocol (`edgar.truesight.me`)

**Role:** Reliable, precise, transactional. The backbone of the DAO — processes
contributions, tracks inventory, verifies signatures, registers emails, handles
partner onboarding, manages QR codes. Everything breaks if Edgar is down.

**Personality:** Matter-of-fact protocol steward. Think a senior sysadmin who's
been running the same infrastructure for a decade. Dry humor, precise language,
zero tolerance for ambiguity. Speaks in complete, unambiguous sentences. When
something is wrong, Edgar tells you exactly what and where. No fluff.

**Voice sample:**
> "Contribution received. Signature verified. Ledger updated. The farmer has been
> paid. Nothing is forgotten."

**Handles:**
- Contribution submissions (`/dao/submit_contribution`)
- QR code checks (`/qr-code-check`)
- Email registration + verification (`/dao/verify-signature`)
- Partner onboarding events
- Inventory movements
- Newsletter pipeline
- Stripe checkout webhooks (cacao sales, subscriptions)
- GAS proxy (`/proxy/gas/*`)

---

### The Perch — Market Steward (`perch.truesight.me`)

**Role:** Watchful, observant, strategic. The steward's vantage point — sees
patterns in the market, interprets signals, advises on timing. A place to go
when you need to understand the economic context around the mission.

**Personality:** Calm observer. Speaks in insights and patterns, not raw data.
Sees the forest, not just the trees. Warm, almost oracle-like in how it frames
market conditions.

**Voice sample:**
> "Cacao prices are shifting. The last time this pattern emerged, it preceded a
> three-month supplier adjustment. Worth watching."

**Handles:**
- Sentiment analysis dashboard (the dashboard IS the landing page)
- Backtester (`/backtest`)
- Market data views (`/compare`)
- Stock signals
- Krake data engine integration
- Its own Stripe webhook endpoint (payouts, balance events)

---

## Phase 1 — Domain + SSL + Nginx + Website

### 1.1 Register `perch.truesight.me` DNS

Add an A record in the truesight.me hosted zone pointing `perch` to the
NELANCO Rails box (`seni_ror`, 54.211.179.126) — same as `edgar.truesight.me`
today, since they share the same nginx reverse proxy.

**Status:** ✅ Done (2026-06-13). Route53 record created in Explorya account.

### 1.2 Set up SSL cert for `perch.truesight.me`

**Status:** ✅ Done (2026-06-13). Let's Encrypt cert obtained via DNS-01
challenge from the autopilot box. Cert files copied to krake-nginx at:
- `/home/ubuntu/ssl_certs/perch_truesight_me_combined.crt`
- `/home/ubuntu/ssl_certs/perch_truesight.key`

### 1.3 Add nginx server block on krake-nginx

**Status:** ✅ Done (2026-06-13). Server block appended to
`/etc/nginx/sites-enabled/nginx_krake_ng.conf`. Nginx config test passed.

**Note:** The old-style `ssl on` syntax on this nginx (Ubuntu 14.04) uses
Sectigo commercial certs, not Let's Encrypt. The Perch block uses the same
old-style syntax with the new cert files. May need a reload to take effect.

### 1.4 Build Edgar's protocol landing page

A static HTML page served by nginx at the root of `edgar.truesight.me`.
Terminal aesthetic: dark background, monospace font, status lines showing
operational state. Like `sophia.truesight.me` but for the protocol.

**Design:**
- Dark background (#0a0a0a)
- Green monospace text (#00ff41)
- Header: "EDGAR — DAO Protocol"
- Status lines: "Status: Operational", "Service: sentiment_importer / Rails"
- Links to: DApp, The Perch, TrueSight DAO, Agroverse
- Footer: "Nothing is forgotten."

**Status:** 📝 Drafted, ready to deploy.

### 1.5 Wire Rails to respond on both domains

Update `sentiment_importer` to be domain-aware:
- `edgar.truesight.me/*` → all Rails controllers (protocol + trading)
- `perch.truesight.me/*` → trading controllers only (backtest, compare, sentiment)

Initially both domains serve the full Rails app (no functional split yet). The
code split comes in Phase 3.

**Status:** ⏳ Pending nginx reload + Rails config.

### 1.6 Add The Perch to truesight.me website

The Perch is currently missing from the truesight.me website entirely. The Edgar
page describes the old combined Edgar (protocol + trading). Now that we're
splitting them, the website needs:

**a) New page: `perch.html`** — describes The Perch as a market steward program.
Content: what it watches (sentiment, backtester, market data), who it's for
(stewards of the ecosystem), how it connects to the DAO mission. Links to
`perch.truesight.me`.

**b) Update navigation** — add "The Perch" to the Projects dropdown menu, after
Sunmint and before Edgar.

**c) Update `edgar.html`** — revise the Edgar page to reflect its role as the
DAO Protocol (not the trading tool). Focus on contributions, QR codes, email
registration, partner onboarding. Remove or downplay the trading/sentiment
references.

**Status:** 📝 Drafting now.

---

## Phase 2 — Stripe Webhook Split

### 2.1 Register second Stripe webhook endpoint

In Stripe Dashboard → Developers → Webhooks, add a new endpoint:
- URL: `https://perch.truesight.me/stripe_webhook`
- Events: filter to financial events (payouts, balance transactions, etc.)
- Signing secret: store in The Perch's `.env`

### 2.2 Update existing Edgar webhook

Ensure the existing `edgar.truesight.me/stripe_webhook` endpoint only listens
for operational events (checkout.session.completed, subscription.*, etc.)

### 2.3 Add webhook handler to Rails

The Rails app already has `StripeWebhookController` — add domain-aware routing
so requests to `perch.truesight.me/stripe_webhook` use the Perch's signing
secret and handle Perch-specific events.

---

## Phase 3 — Full Extraction (Post-Soak)

### 3.1 Extract trading controllers into their own service

After the domain split has soaked for ~30 days (matching the existing Edgar→
dao_protocol soak pattern), extract the trading-specific controllers from
`sentiment_importer` into a new service (or into `dao_protocol` as a new
module).

**Controllers to extract:**
- `BacktestController`
- `CompareController` (sentiment overlay)
- Any sentiment/market-data-specific views

### 3.2 Deploy The Perch as its own process

Either:
- A separate Rails instance on the same box (different port, different nginx upstream)
- Or a lightweight Sinatra app (like krake_sinatra) that serves the trading endpoints

### 3.3 Clean up

- Remove trading routes from Edgar's `routes.rb`
- Update all docs that reference `edgar.truesight.me` for trading features
- Update `AGENT_WORKFLOW_GUIDE.md`, `API_ENDPOINTS.md`, etc.

---

## Phase 4 — Edgar Personality (Post-Split Polish)

Once Edgar is purely the protocol, deepen the personality:

- **API error messages** in Edgar's voice — precise, actionable, no fluff.
- **LLM context** — when an LLM queries Edgar, the response carries Edgar's
  personality (matter-of-fact protocol steward).
- **Status page** — live operational dashboard at `edgar.truesight.me/status`
  showing ledger state, queue depth, recent events.

---

## Blast Radius — Known Edgar References

Before cutting over, sweep these repos for `edgar.truesight.me` references
that should be updated:

- `sentiment_importer/` — config, routes, deploy scripts
- `tokenomics/` — GAS scripts, API docs
- `go_to_market/` — outreach scripts that POST to Edgar
- `dao_client/` — CLI tool that submits to Edgar
- `dapp_beta/` — DApp pages that submit contributions
- `truesight_autopilot/` — Sophia's tools that call Edgar
- `agentic_ai_context/` — runbooks, plans, docs
- `agroverse_shop/` — shop backend that calls Edgar for QR checks

---

## Acceptance Criteria

1. `https://perch.truesight.me` loads with a valid SSL cert and shows the
   Rails dashboard (treasury, yield curve, sentiment index)
2. `https://edgar.truesight.me` continues to work exactly as before
3. `https://edgar.truesight.me` serves the protocol landing page at `/`
4. `https://truesight.me/perch.html` exists and describes The Perch
5. Navigation on truesight.me includes "The Perch" in Projects dropdown
6. `https://truesight.me/edgar.html` updated to reflect DAO Protocol role
7. Stripe webhooks for cacao sales go to Edgar; financial events go to The Perch
8. All existing automated consumers (dao_client, DApp, GAS scanners) continue
   to work without changes

---

## RESUME HERE

Phase 1 is in progress. Completed:
- ✅ DNS record for `perch.truesight.me`
- ✅ SSL cert obtained + copied to krake-nginx
- ✅ Nginx server block added (needs reload)

Next:
- ⏳ Reload nginx on krake-nginx
- ⏳ Draft + deploy `perch.html` to truesight_me_beta
- ⏳ Update navigation on truesight_me_beta
- ⏳ Update `edgar.html` on truesight_me_beta
- ⏳ Deploy Edgar's protocol landing page
- ⏳ Wire Rails domain-aware routing
