# GetData.IO MCP agent-marketplace bridge — pre-flight + execution roadmap

**Goal:** Expose GetData.IO's existing 47,000+ community data-source marketplace to AI agents via
an MCP server, monetized per-call via agent-native payments (x402), distributed entirely through
channels an LLM agent can reach without a human doing sales/outreach. This is **not** a rebuild —
`getdata.io` already has a documented REST API (`Data Source Management API`, `Semantic Query
Language`, export/webhook APIs); the work here is wrapping that API as MCP tools, adding
agent-native billing, and listing it where agents already look.

**Architecture pivot (2026-07-23, governor decision):** the MCP server is now built **directly into
`krake_ror`** (the existing, already-deployed Rails app) using Ruby's official `mcp` gem (or
`FastMCP` — decide in 2c), **not** as a separate `getdata-mcp-bridge` Node/TypeScript repo. See
"Why the pivot" below — the separate-repo path hit five distinct blockers in a row (wrong-org repo
creation, PAT scope gaps, round-cap failures on multi-file Node scaffolding) that a Rails-native
build sidesteps entirely, since `krake_ror` already exists, is already deployed, already has
Doorkeeper OAuth wired (Unit 2b), and Sophia already has confirmed working push access to it.
`KrakeIO/getdata-mcp-bridge` was never successfully created and this plan no longer targets it —
don't resume work there.

**Why this and not a broader pivot:** see conversation history 2026-07-18 through 2026-07-21 for
the full research trail. Short version: gray-area social scraping is a losing cat-and-mouse fight;
"agentic browser automation" is an even more brutal, fast-moving, well-funded battlefield
(Browserbase, Hyperbrowser, Steel, Anchor, Deck already fighting over the exact "authenticate into
real accounts" angle); FDA/compliance data isn't a market GetData.IO has a real product in; and
licensing the scraped corpus as AI training data inherits the same rights-clearance problem as
scraping generally (industry trend is explicitly *away* from unlicensed scraped data). The one
real, differentiated asset found: a live, currently-growing, 47,475-source community marketplace
(comparable in raw count to Apify's ~30-31K Actor Store) that nobody outside this workspace knows
exists. Apify's own answer to the AI-agent wave was `apify-mcp-server`; this plan is the same move,
scoped to GetData.IO's existing marketplace rather than a new one.

**Why the Rails-native pivot (2026-07-23):** the original Unit 2c (scaffold a new
`KrakeIO/getdata-mcp-bridge` Node/TS repo) hit five distinct blockers across several turns:
(1) `git_tools.py` hardcoded the TrueSightDAO org, so pushing to a KrakeIO repo would have gone to
the wrong org even once created; (2) Sophia had no tool capable of creating a brand-new repo at
all; (3) once that tool was built and deployed, `KRAKE_IO_PAT` turned out to lack org-repo-creation
scope (404, despite being documented as "full" Krake access); (4) `KrakeIO` turned out to be a
personal GitHub **user** account, not a true Organization, so `POST /orgs/KrakeIO/repos` was never
going to work regardless of credential — the correct endpoint is `POST /user/repos` authenticated
*as* that account; (5) even with the repo problem fixed, Sophia hit the round-cap three separate
times trying to construct-and-push a 7-file Node scaffold in one turn, and in one of those attempts
manually bypassed the (at-the-time-broken) tooling and created the repo under the wrong org by
hand. None of this is a reason the *product* idea is wrong — it's all friction specific to standing
up brand-new cross-org infrastructure. Building the MCP endpoint directly into `krake_ror` (already
deployed, already has confirmed working push access, already has Doorkeeper OAuth live) sidesteps
every one of these five problems at once. Ruby has first-class MCP tooling for this: an **official
`mcp` gem** (`bundle add mcp`) and **`FastMCP`**, a popular Rails-specific wrapper gem — this is not
an awkward off-path choice, it's well-supported, current (2026), production-used tooling (see e.g.
Fleetio's engineering blog on securing an MCP server in Rails).

> ## ▶ RESUME HERE
>
> **Units 1, 2a, 2b done (2026-07-21) — all three needed zero backend code changes, just
> verification (see Findings 1-2 below, still accurate).** Unit 2c is **being redone** per the
> 2026-07-23 architecture pivot above: instead of a separate `getdata-mcp-bridge` repo, add MCP
> routes directly to `krake_ror` using the `mcp` gem (or `FastMCP` — pick one and document why in
> the PR). **This is the current RESUME HERE unit — nothing has been built for it yet.**
>
> **Finding 1 — public marketplace search already returns JSON, live, today, with zero code
> changes.** `https://getdata.io/data-for-everyone.json` works right now — a `public.json.jbuilder`
> view already existed in the codebase (Rails' implicit responder serves it automatically), nobody
> had tried the `.json` suffix before. Confirmed live: bare request returns `{total: 47475,
> pagination: {...}, results: [{id, name, description, ...}]}` instantly. **Caveat**: `?search=` on
> the `.json` route timed out in testing (15s) where the bare request is fast — likely an uncached
> search path. Since the new MCP routes live in the same Rails app now, prefer calling
> `Krake.public(...)` (the model method) directly from the MCP tool handler rather than making an
> HTTP round-trip to the app's own JSON endpoint — faster, and sidesteps the caching question until
> it's addressed separately.
>
> **Finding 2 — token issuance uses Doorkeeper.** `Member` has
> `has_many :oauth_access_tokens, foreign_key: "resource_owner_id", class_name: "Doorkeeper::AccessToken"`
> — this is the standard Ruby OAuth2 provider gem. Doorkeeper supports fully programmatic token
> issuance via standard OAuth2 grant flows (`client_credentials` and `password` are both already
> enabled — see Unit 2b below), which is what makes "no human in the loop" token provisioning for
> MCP-server tenants realistic. The new MCP routes should sit behind this existing auth, not a new
> auth mechanism.

---

## Pre-flight (§5d Pre-flight Completeness)

### The existing API surface (already live, confirmed via rendered `getdata.io/docs/*` pages)

- **Auth**: personal access token (Bearer), obtained from a user's developer-settings page.
  MCP-server auth will need a way to provision/rotate these programmatically or per-tenant — not
  yet confirmed whether there's a token-issuance API distinct from the web dashboard; **Unit 1
  must confirm this** (if token issuance is web-dashboard-only today, that's the one piece that
  isn't yet "no human in the loop" and may need a small backend addition).
- **Run a data source**: `POST https://getdata.io/data-sources/:DATA_SOURCE_UNIQUE_ID/run`,
  body `{origin_urls, data, format}`.
- **List data sources / batches**: documented, exact call shapes not yet captured — **Unit 1
  pre-flight task**, render `/docs/data-source-management/api` in full (only the "Run" section was
  captured in this pass; "List your data sources" / "List your data source batches" sections exist
  per the page's own nav but weren't read in full).
- **Export results**: `GET http://cache.getdata.io/:DATA_SOURCE_UNIQUE_ID/:TIMESTAMP_page_:PAGE.json`
  (also CSV), 100 records/page, `latest` or a Unix timestamp for `:TIMESTAMP`.
- **Webhooks**: register a callback URL when creating/updating a data source; fires on data
  completion with `data_url_json` / `data_url_csv`.
- **Semantic Query Language**: a JSON recipe format (`engine`, `origin_url`, `headers`, `method`,
  `cookies`, `post_data`, `actions`, `columns`, `next_page`, `groupings`, `order_by`, `data`,
  dynamic variables, nested page queries) for **declaring new** data sources — this is the
  mechanism an agent would use to create a data source that doesn't already exist among the 47K.
- **Discovery**: `getdata.io/data-for-everyone` — client-rendered (Backbone.js), 47,475 sources,
  sortable by Most Popular / Created Most Recently / Ran Most Recently, filterable by 20+
  categories. No public search/list *API* was found in the docs pages read so far — **Unit 1 must
  check whether "List your data sources" (mentioned in the nav but not yet read) covers searching
  the public marketplace, or only a user's own private sources.** If there's no public search API,
  the MCP server's `search_data_sources` tool will need to either scrape `/data-for-everyone`
  itself (fragile, ironic) or this becomes a small backend addition to expose one.

### Existing monetization (do not touch — this plan adds a new channel, doesn't replace it)

- Stripe-integrated tiered SaaS: `COMMUNITY / SOLO / STARTUP / BUSINESS / RETAILER / ENTERPRISE`
  plans (`krake_ror/app/models/subscription.rb`, `stripe_plan.rb`). This is the human/dashboard
  signup path — unaffected by this plan.

### Proposed new monetization layer: x402 (agent-native, per-call, no human in the loop)

- **x402**: an open protocol (Coinbase-backed) that lets an AI agent autonomously pay for an API/
  MCP tool call with stablecoins, settled per-request — no credit card form, no dashboard signup.
  Market reference range: **$0.002–$0.44 per call, $0.028 median** (per-call API market data cited
  in `systemprompt.io`'s x402 monetization guide, 2026).
- **Validated in-category precedent**: Bright Data — the market leader I found in earlier research
  — has an **open RFC** (`brightdata/brightdata-mcp#126`, opened 2026-03-31) proposing exactly this:
  "pay-per-scrape via x402/MPP" for their own MCP server. This is not a speculative pattern; a
  direct competitor is actively building toward it.
- **Why x402 over extending Stripe subscriptions to agents**: an agent mid-conversation cannot fill
  out a web signup form or hold a saved credit card the way a human does. x402 requires only that
  *whoever deployed the agent* funded a wallet once, in advance — after that, every tool call
  settles autonomously. This is the actual mechanism that makes "GTM to other LLM agents, no human
  in the loop" *possible*, not just a nice framing.
- **Proposed pricing** (starting point, revisit after Unit 1's real cost data): price per
  `run_data_source` call by the underlying recipe's crawl cost/complexity — a simple static-page
  source near the low end (~$0.01), a JS-rendered/interactive recipe near the median (~$0.03), a
  multi-page/paginated crawl toward the top of the range (~$0.10–$0.30). `search_data_sources`
  (read-only, hits the existing catalog, cheap to serve) should be **free** — the catalog is the
  discovery surface; paywalling discovery kills adoption before an agent ever finds a reason to pay.
- **Fallback / alternative**: `SettleGrid` (`@settlegrid/mcp` SDK, `sg.wrap()`) brokers payment
  across 9 agent payment protocols via a hosted proxy — lower integration effort than wiring x402
  directly, worth evaluating in Unit 3 as a build-vs-buy call instead of a hard requirement to
  hand-roll x402.

### GTM: autonomous distribution channels (no human sales required)

All of the following accept programmatic/CLI-based or PR-based submission:

1. **Official MCP Registry** (`registry.modelcontextprotocol.io`) — the ecosystem's canonical
   directory as of 2026. Publishing is a CLI push of a `server.json`; namespace ownership proven by
   a domain/repo check (exact mechanism to confirm in Unit 5, likely a DNS TXT record or GitHub
   repo ownership proof for the `getdata.io` or `krake` namespace).
2. **PulseMCP** (`pulsemcp.com`) — 22,310+ servers indexed, updated daily; has a submission flow.
3. **MCP.so** — directory with a `Submit` flow.
4. **Glama** — 22,775+ servers indexed as of mid-2026.
5. **`awesome-mcp-servers`-style GitHub lists** — plain PR submissions (multiple such lists exist;
   Unit 5 should target the 2-3 highest-traffic ones, not all of them).
6. **Agent-onboarding doc on getdata.io itself** — mirror Firecrawl's `/agent-onboarding/SKILL.md`
   pattern (a machine-readable "how an AI agent should use this" doc, distinct from human-facing
   marketing copy) so agents that land on the site directly (or via web search) can self-serve
   setup instructions without a human explaining it to them.

None of these require a phone call, a demo, or a human reviewer approving a business relationship
— all are either CLI/API-driven or a standard open-source-style PR. This is what makes the GTM
"executable without human in the loop": the *channel* itself doesn't gate on a human on the
receiving end, only on the work of actually submitting correctly-formed listings.

### ✅ Pre-flight Completeness (§5d self-cert)
**Not fully satisfiable yet** — two facts are explicitly deferred to Unit 1 (token-issuance
mechanism; whether a public search/list API exists for the marketplace) because getting them right
requires reading pages this pass didn't fully render. Flagging honestly rather than guessing: Unit
1 is scoped as a pre-flight-completion unit, not a code-writing unit, specifically to close this
gap before Unit 2 starts building.

---

## Sequenced plan

| Unit | What | Advance | Status |
|------|------|---------|--------|
| 1 | **Pre-flight completion (read-only).** ✅ Done — see RESUME HERE. | _(auto — read-only)_ | ✅ |
| 2a | ~~`krake_ror` PR: add `format.json`~~ **NOT NEEDED — already live.** Verified 2026-07-21: `https://getdata.io/data-for-everyone.json` already returns real structured JSON in production (`{total, pagination, results: [{id, name, description, ...}]}`) — a `public.json.jbuilder` view + `_krake_summary.json.jbuilder` partial already exist in the codebase, Rails' implicit responder serves them, nobody had ever tried the `.json` suffix. **Zero code change required for basic listing.** Caveat found during verification: `?search=` query param on the `.json` route timed out (15s) where the bare unfiltered request is fast — likely an uncached/slow DB path for search specifically. **Unit 2c must verify search-param performance before relying on it**; may need a small caching fix as a follow-up, but doesn't block starting 2c. | _(auto — read-only verification, done)_ | ✅ |
| 2b | ~~Confirm/enable Doorkeeper `client_credentials`~~ **NOT NEEDED — already enabled.** Verified 2026-07-21: `config/initializers/doorkeeper.rb` line 8 has `grant_flows ["authorization_code", "client_credentials", "password"]`. Both `client_credentials` (service-to-service, no member credentials needed) and `password` (exchange a member's email+password directly for a token via `POST /oauth/token`) are already live. Zero config change needed. Client app registration uses Doorkeeper's standard built-in `Doorkeeper::Application` model — no custom model found, which is normal/expected for a stock Doorkeeper setup. | _(auto — verification only, done)_ | ✅ |
| 2c | **[REDONE 2026-07-23] Add MCP server to `krake_ror`** via a `krake_ror` PR (branch + PR, same convention as any other change to this repo — not a fresh empty-repo push). `bundle add mcp` (or `FastMCP` — pick one, document the choice in the PR description). New route (e.g. `POST /mcp`, Streamable HTTP transport) behind Doorkeeper OAuth (Finding 2). Three tools: `search_data_sources(query, category?)` [free — calls `Krake.public(...)` directly, not an HTTP round-trip to the app's own JSON endpoint], `run_data_source(handle, origin_urls?, data?)` [paid — calls the existing run logic], `get_results(handle, timestamp?, page?)` [free — reads from the existing cache path]. Dropped `create_data_source` (recipe creation via Semantic Query Language) from this first cut — smaller v1, add it as a follow-up unit once the three read/run tools are proven live. Include a request spec per §9 (this workspace's HTML/JS/Rails test-before-merge convention). | _(auto — additive PR to an already-deployed, already-working app; standard branch+PR review, not a prod-infra gate)_ | ☐ |
| 3 | **Payment integration.** Build-vs-buy decision: hand-rolled x402 (Ruby: check for an x402 gem/middleware first, otherwise implement the HTTP 402 + payment-header exchange directly — it's a fairly small spec) vs. `SettleGrid`'s hosted proxy (its docs reference `@settlegrid/mcp`, a Node package — check for a language-agnostic/HTTP-proxy mode before ruling it out for a Ruby app). Wire `run_data_source` behind per-call settlement at the pricing in the pre-flight. `search_data_sources` and `get_results` stay free/ungated. | _(auto — additive to krake_ror, no real money moves until Unit 6 UAT)_ | ☐ |
| 4 | **Deploy.** No new infrastructure needed — this ships as part of `krake_ror`'s normal deploy process to its existing EC2 instance. Still worth a quick governor confirmation before the route goes live on production traffic, since `krake_ror` is a real, currently-used app (see the traffic-surge findings from 2026-07-18/19). | `gate: prod deploy confirmation` (§5c — lower-stakes than standing up new infra, but still touches live prod) | ☐ |
| 5 | **GTM submissions.** Submit to the official MCP Registry, PulseMCP, MCP.so, Glama, and 2-3 top `awesome-mcp-servers` lists per the pre-flight's channel list — these list the live endpoint URL (e.g. `https://getdata.io/mcp`), not a GitHub repo, so the earlier repo-creation problems don't even apply here. Write and publish an agent-onboarding doc (SKILL.md-style) linked from `getdata.io`. | _(auto — all channels are PR/CLI-driven, reversible, no spend)_ | ☐ |
| 6 | **UAT (§5c always-stop).** A human (governor) — or an agent under the governor's supervision — actually discovers the MCP server through one of the Unit 5 channels (not by being told the URL directly), calls `search_data_sources`, runs a real `run_data_source` call, and confirms a real x402 (or SettleGrid) payment settles correctly end-to-end. This is the first point real money moves — hard stop regardless of how Units 1-5 went. | `gate: UAT + first real payment` | ☐ |

**Note on scope**: this plan deliberately stops at "live, discoverable, and provably working
end-to-end for one real transaction." Pricing tuning, category-specific rate limiting, and broader
marketing are explicitly out of scope for v1 — revisit after Unit 6 with real usage data, the same
way the SSL-recovery plan's Unit 7 cleanup items were left as low-priority follow-ups rather than
bundled in.

---

## Rollback

- Units 1-3 touch nothing but a brand-new repo — zero blast radius, trivially abandoned if wrong.
- Unit 4 (deploy) is new infrastructure, not a modification of anything existing — can be torn down
  without affecting `getdata.io`'s current live traffic or Stripe billing at all.
- Unit 5 (GTM submissions) are all reversible (delist/close the PR) if something's wrong post-launch.
- The existing Stripe/dashboard monetization and the existing 47K-source marketplace are **never
  modified** by this plan — this is strictly additive.
