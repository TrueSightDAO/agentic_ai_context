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
- Sentiment analysis dashboard
- Backtester (`/backtest`)
- Market data views (`/compare`)
- Stock signals
- Krake data engine integration
- Its own Stripe webhook endpoint (payouts, balance events)

---

## Phase 1 — Domain + SSL + Landing Page

### 1.1 Register `perch.truesight.me` DNS

Add a CNAME record in the truesight.me hosted zone pointing `perch` to the
NELANCO Rails box (`seni_ror`, 54.211.179.126) — same as `edgar.truesight.me`
today, since they share the same nginx reverse proxy.

**Files:** Route53 hosted zone for truesight.me (NELANCO account).

### 1.2 Set up SSL cert for `perch.truesight.me`

Same pattern as `sophia.truesight.me`:

```bash
# On krake-nginx (the NELANCO reverse proxy):
sudo certbot --nginx -d perch.truesight.me
```

This gives The Perch its own HTTPS certificate, independent of Edgar's.

### 1.3 Add nginx server block on krake-nginx

Create `/etc/nginx/sites-available/perch` that proxies `perch.truesight.me` →
the same Rails backend (`127.0.0.1:3002`) but with a different root for the
landing page.

**Key difference from Edgar:** The Perch's nginx block serves a static landing
page at `/` (like `sophia.truesight.me`) instead of redirecting to Rails. The
Rails app handles `/backtest`, `/compare`, `/sentiment` etc. under the same
upstream.

### 1.4 Build The Perch landing page

A static HTML page at `/var/www/perch/index.html` served by nginx, following
the same pattern as `sophia.truesight.me`:

- Clean, warm design
- States its purpose: "The Perch — a steward's view of the markets"
- Links to the trading tools (backtester, sentiment, compare)
- Links to Edgar for protocol operations
- Links to the DAO mission

### 1.5 Wire Rails to respond on both domains

Update `sentiment_importer/config/routes.rb` and nginx to route:
- `edgar.truesight.me/*` → existing Rails controllers (protocol + trading)
- `perch.truesight.me/*` → trading controllers only (backtest, compare, sentiment)

Initially both domains serve the full Rails app (no functional split yet). The
domain separation comes first; the code split comes in Phase 3.

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

## Phase 4 — Edgar Personality (Optional, Post-Split)

Once Edgar is purely the protocol, give it a distinct voice:

- **Landing page** at `edgar.truesight.me` — a clean, minimal page that states
  Edgar's role as the DAO Protocol. Think terminal aesthetic: dark background,
  monospace font, status lines.
- **API error messages** in Edgar's voice — precise, actionable, no fluff.
- **LLM context** — when an LLM queries Edgar, the response carries Edgar's
  personality (matter-of-fact protocol steward).

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
   landing page (no certificate warnings)
2. `https://edgar.truesight.me` continues to work exactly as before
3. Stripe webhooks for cacao sales go to Edgar; financial events go to The Perch
4. The Perch's landing page has its own identity (not just a copy of Edgar's)
5. All existing automated consumers (dao_client, DApp, GAS scanners) continue
   to work without changes

---

## RESUME HERE

Phase 1 is authorized and ready to execute. Start with:
1. DNS: add `perch.truesight.me` CNAME
2. SSL: certbot on krake-nginx
3. Nginx: add perch server block
4. Landing page: build `/var/www/perch/index.html`
5. Rails: domain-aware routing

Gary will test each step before proceeding to Phase 2.
