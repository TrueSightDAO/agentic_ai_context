# GetData.IO MCP agent-marketplace bridge — pre-flight + execution roadmap

**Goal:** Expose GetData.IO's existing 47,000+ community data-source marketplace to AI agents via
an MCP server, monetized per-call via agent-native payments (x402), distributed entirely through
channels an LLM agent can reach without a human doing sales/outreach. This is **not** a rebuild —
`getdata.io` already has a documented REST API (`Data Source Management API`, `Semantic Query
Language`, export/webhook APIs); the work here is wrapping that API as MCP tools, adding
agent-native billing, and listing it where agents already look.

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

> ## ▶ RESUME HERE
>
> **Unit 1 — not started.** This plan was drafted 2026-07-21 by Claude (interactive session); no
> code has been written yet.

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
| 1 | **Pre-flight completion (read-only).** Render (Playwright) the full `/docs/data-source-management/api` page (List data sources, List batches sections) and check for a public marketplace search endpoint. Confirm token-issuance mechanism (dashboard-only vs. API). Read `krake_ror`'s `app/controllers` for the actual Rails routes backing these docs (ground-truth beats docs that may be stale). Output: an updated pre-flight section in this file with the gaps closed, or an explicit note if a small backend addition is needed before Unit 2 can proceed. | _(auto — read-only)_ | ☐ |
| 2 | **Scaffold new MCP server repo** (`KrakeIO/getdata-mcp` or similar — new repo, not touching `krake_ror`). Node/TypeScript MCP server (matches the ecosystem's dominant tooling). Tools: `search_data_sources(query, category?)` [free], `run_data_source(id, params)` [paid], `get_results(id, timestamp?, page?)` [free — result retrieval shouldn't be double-charged after the run already was], `create_data_source(recipe: SemanticQueryLanguage)` [paid, priced higher — this is the "extend the marketplace" action]. Wraps the existing REST API from Unit 1 — no new backend logic unless Unit 1 found a gap. | _(auto — new repo, no prod impact)_ | ☐ |
| 3 | **Payment integration.** Build-vs-buy decision: hand-rolled x402 vs. `SettleGrid`'s `@settlegrid/mcp` SDK. Wire the paid tools (`run_data_source`, `create_data_source`) behind per-call settlement at the pricing in the pre-flight. Free tools (`search_data_sources`, `get_results`) stay ungated. | _(auto — new repo, no prod impact, no real money moves until Unit 6 UAT)_ | ☐ |
| 4 | **Deploy.** Needs a hosting decision — could piggyback on existing Nelanco/Explorya AWS (consistent with the rest of the Krake fleet) or a simple serverless deploy (Cloudflare Workers has first-class x402/paid-MCP-tool support per pre-flight research, worth considering to avoid touching the fragile EC2/ALB fleet at all). | `gate: infra/deploy decision` (§5c — this is standing up new infrastructure, even if low-risk; worth a quick governor confirmation on where it lives before it's live) | ☐ |
| 5 | **GTM submissions.** Submit to the official MCP Registry, PulseMCP, MCP.so, Glama, and 2-3 top `awesome-mcp-servers` lists per the pre-flight's channel list. Write and publish an agent-onboarding doc (SKILL.md-style) linked from `getdata.io`. | _(auto — all channels are PR/CLI-driven, reversible, no spend)_ | ☐ |
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
