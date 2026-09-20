# Schwab Portfolio Integration Plan — read-only positions in `sentiment_importer` (Perch)

**Owner / requester:** Gary Teh, via the `analyst` Claude Code seat (nelanco-claude), 2026-09-20.
**Goal:** Let Gary link his real Charles Schwab brokerage account into Perch
(`sentiment_importer`) so his live positions/account value can be pulled programmatically —
feeding "in-depth discussions" about his personal portfolio (the same kind of session that
already reviewed his APLD/INTU/LRCX/ORCL/PLAY holdings against Perch's own RSI/MACD/dip
signals on 2026-09-17). **This is a READ-ONLY integration — see the hard scope boundary below.**

**RESUME HERE → PR1.**

---

## 0. Hard scope boundary — READ-ONLY, no trading (do not relax without an explicit governor decision)

Perch already has a working live-trading brokerage abstraction
(`Brokerages::BrokerageInterface`) wired into an algorithmic trading system
(`PortfolioSignaler`, `PortfolioIncluder`/`PortfolioExcluder`, `PortfolioAllocationAutoEntry`,
`place_order_market`/`place_order_limit`). That system currently targets a `amtd` (Ameritrade)
brokerage class that is effectively dead (TD Ameritrade's API was retired in the Schwab
migration; `PortfolioSignaler#perform` already has a `rescue Faraday::ConnectionFailed` dead-API
warning for it).

**Decision (made in this plan, flag to Gary if he wants it revisited):** the new `Schwab`
brokerage class implements **only the read methods** — `account_positions`,
`current_cash_balance`, `current_portfolio_value`, `brokerage_account_id`, market-hours checks.
It **does not override** `place_order_market`, `place_order_limit`, `cancel_all_orders`, or
`cancel_order` — those stay inherited from `Brokerages::BrokerageInterface` where they
`raise NotImplementedError`. **No Schwab-linked user is ever added to `auto_buy: true`**, and no
code in this plan touches `PortfolioSignaler`, `PortfolioIncluder`, `PortfolioExcluder`, or the
order-placement path. This is enforced by a unit test in PR1 (assert the trading methods raise),
not just by omission — see PR1.

**Why this matters:** this is Gary's real personal brokerage account with real money, not a DAO
system. The existing algo-trading workers were built for a paper-adjacent/managed-allocation
model; wiring a live personal account into `send_buy_now_signals_for_auto_buy_enabled_users` or
`PortfolioIncluder` would mean Perch's existing signal logic could place real trades on Gary's
account without a human clicking "buy." **Nothing in this plan enables that path.** If future
work wants Schwab order placement, that is a separate, explicitly-scoped follow-up plan with its
own governor sign-off — do not fold it into this one.

---

## 1. Pre-flight (§5d completeness — read once here, not re-discovered per PR)

### 1a. Existing brokerage abstraction to mirror (`sentiment_importer` repo, path relative to repo root)

- **`app/models/brokerages/brokerage_interface.rb`** — abstract base class. Declares
  `can_trade?`, `brokerage_name`, `brokerage_account_id`, `account_positions`,
  `current_cash_balance`, `current_portfolio_value`, `place_order_market`,
  `place_order_limit`, `cancel_all_orders`, `fetch_market_price`, `opening_hour?`,
  `closing_hour?`, `trading_time?`, `market_open?`, `pre_market_open?`, `post_market_open?` —
  all `raise NotImplementedError` by default. Class method `self.brokerage(user_id,
  desired_brokerage_name=nil)` looks up `user.default_brokerage`, falls back to
  `paper_trade_brokerage` if not linked.
- **`app/models/brokerages/ameritrade.rb`** — the concrete class to mirror (Schwab's Trader API
  is the direct successor of TD Ameritrade's, endpoint/JSON shapes are documented as
  near-identical: `/accounts?fields=positions,orders` → `securitiesAccount.positions[].
  instrument.symbol` / `.marketValue` / `.longQuantity`; `currentBalances.equity`;
  `currentBalances.cashBalance` + `marginBalance`). `Brokerages::ActivePosition` (referenced,
  not yet re-read in this pre-flight — trivial value object, confirm shape when writing PR1:
  `grep -n "class ActivePosition" -A10 app/models/brokerages/active_position.rb` if it's a
  separate file, else it's defined inline near `Ameritrade#account_positions`) is what
  `account_positions` returns a list of (`symbol`, `market_value`, `long_quantity`).
- **`app/models/brokerages/brokerage_manager.rb`** — `SUPPORTED_BROKERAGES` hash
  (`"amtd" => Brokerages::Ameritrade`, `"coinbase_pro"`, `"paper_trade_brokerage"`,
  `"tsd_game"`). PR1 adds `"schwab" => Brokerages::Schwab`. `supported_brokerages` /
  `linked_brokerages` / `live_linked_brokerages` all read this hash + `brk_class::
  BROKERAGE_DISPLAY_NAME` — no separate registration needed beyond the hash entry.
- **`app/models/oauth2_credential.rb`** — generic OAuth2 token store, already provider-agnostic
  at the DB layer (see schema below). `self.fetch_client(provider)` is a `case` statement,
  currently only handles `"amtd"` (`amtd_client`, built with
  `OAuth2::Client.new(config.td_ameritrade_client_id, nil, site:, authorize_url:, token_url:)`
  — **note the `nil` client_secret**: TDA's flow didn't require one). PR1 adds a `"schwab"` branch
  + `schwab_client` class method. **Schwab's OAuth DOES require a client_secret** (confidential
  client) — this is a material difference from the Ameritrade pattern; do not copy the `nil`.
  `#refresh_token!` / `#token` / `#client` instance methods are fully generic and need **no
  changes** — they'll work for Schwab once `fetch_client("schwab")` is wired.
- **`db/schema.rb` `oauth2_credentials` table** (line ~451) — already generic:
  `user_id, provider, access_token, refresh_token, expires_at, created_at, updated_at, api_key,
  api_secret`, unique index on `(user_id, provider)`. **No migration needed** for PR1/PR2.
- **`config/application.rb`** (~line 110-112) — existing amtd URL constants:
  `config.amtd_site_url = "https://api.tdameritrade.com"`,
  `config.amtd_authorize_url = "https://auth.tdameritrade.com/auth"`,
  `config.amtd_token_url = "https://api.tdameritrade.com/v1/oauth2/token?access_type=offline"`.
  PR1 adds the Schwab equivalents (public Schwab Trader API base URLs, confirm exact paths at
  implementation time against Schwab's published API docs — as of the 2026 Trader API these are
  `https://api.schwabapi.com` / `https://api.schwabapi.com/v1/oauth/authorize` /
  `https://api.schwabapi.com/v1/oauth/token`; sanity-check against Schwab's developer docs when
  writing PR1 in case the path has moved).
- **⚠️ Known anti-pattern to NOT repeat:** `config/environments/production.rb` (~line 124) and
  `config/environments/development.rb` (~line 77) currently **hardcode the TD Ameritrade
  `client_id` in plaintext, committed to the repo** (`config.td_ameritrade_client_id =
  "UNXGPLUZAIT7KJDLV82KN2ZOF0OZTAOT"`). **Do not do this for Schwab.** Schwab's client_id AND
  client_secret must come from `ENV["SCHWAB_CLIENT_ID"]` / `ENV["SCHWAB_CLIENT_SECRET"]`,
  unset/nil in dev+test (tests stub the `OAuth2::Client`), and set only on the production hosts
  via the existing systemd-env-file pattern (`NOTES_sentiment_importer.md` — `SECRET_KEY_BASE`-
  from-systemd is the precedent to follow), never committed. This is a repo-wide "never commit
  secrets" rule (`WORKSPACE_CONTEXT.md` §3a) that the existing amtd code already violates — don't
  extend the violation.
- **`app/controllers/callbacks_controller.rb`** — Devise::OmniauthCallbacksController subclass;
  its `#amtd` action is wired to the `omniauth-td-ameritrade` gem's Devise strategy. **That
  strategy is currently commented out** in `config/initializers/devise.rb` line 302
  (`# config.omniauth :amtd, ...`) — amtd linking is not live today via this path. **Design
  decision for Schwab: do NOT use Devise::OmniauthCallbacksController / an omniauth strategy gem
  at all.** Schwab's OAuth grant isn't an identity/sign-in flow (no email/profile claim to sign
  a user in with, unlike Google/LinkedIn) — it's purely "let an already-logged-in TrueSight user
  authorize account access." PR2 instead adds a small dedicated controller with two plain
  actions built directly on the `oauth2` gem (already a Gemfile dependency, same gem
  `Oauth2Credential` already uses) — simpler, no new gem dependency, no fighting a possibly
  Schwab-incompatible ancient TDA-era omniauth gem.
- **`app/controllers/api_controller.rb`** — `/api/me` already surfaces `portfolio_value` /
  `cash_balance` generically via `Brokerages::BrokerageInterface.has_brokerage?` /
  `brokerage_name` (helper methods `portfolio_balance` / `account_cash_balance`, not yet
  re-read — confirm they call through `Brokerages::BrokerageInterface.brokerage(current_user.id)`
  when writing PR3). **`/api/holdings` is NOT the right endpoint for this** — it queries
  `PortfolioAllocation` (Perch's own *algo-managed* allocations table), not raw brokerage
  positions, and is irrelevant to a personal Schwab account Perch's algo doesn't manage. PR3
  adds a **new** read-only endpoint that calls `brokerage.account_positions` directly.
- **Spec pattern to mirror** (PR1 tests): `spec/models/brokerages/ameritrade_spec.rb` +
  `spec/fixtures/json_responses/ameritrade_account_details.json` (and sibling fixtures:
  `_market_price.json`, `_market_hours_{open,close,weekend}.json`, `_orders.json`,
  `_oauth_token.json`). Also `spec/models/oauth2_credential_spec.rb`,
  `spec/models/brokerages/brokerage_manager_spec.rb`, `spec/models/brokerages/
  brokerage_interface_spec.rb`, `spec/factories/oauth2_credential.rb`. Same fixture/stub style
  for Schwab: `spec/models/brokerages/schwab_spec.rb` +
  `spec/fixtures/json_responses/schwab_*.json`.

### 1b. Operational caveat to document, not solve in code (flag to Gary, not a blocker)

**Schwab refresh tokens expire after 7 days** (a hard Schwab platform limit, unlike a typical
OAuth provider's long-lived refresh token). `Oauth2Credential#refresh_token!` will start failing
~weekly with no code-level fix — the account will need periodic re-linking through the same
`GET /schwab/connect` flow PR2 builds. Document this in the Mobile_API.md addendum (PR3) and in
the handoff to Gary; do not attempt to silently work around it (there is no supported way to).

### 1c. Credentials — nothing to provision yet

Gary has **not yet registered a Schwab developer app** (that's explicitly scoped as the human
step after this plan's code ships — see §4 below). PR1–PR3 need zero live Schwab credentials:
all specs stub `OAuth2::Client`/HTTP calls against the fixtures above. `ENV["SCHWAB_CLIENT_ID"]`
/ `ENV["SCHWAB_CLIENT_SECRET"]` simply won't be set until Gary completes registration — the code
must not error at boot/load time when they're unset (mirror how `td_ameritrade_client_id`
being blank in test env doesn't break anything today).

### 1d. Deploy model (different from the beta/prod fork repos — read before assuming a pattern)

`sentiment_importer` (Perch) is **not** one of the `*_beta`/`*_prod` fork pairs
(`WORKSPACE_CONTEXT.md` §3f only covers `truesight_me`/`agroverse_shop`/`dapp`). Perch ships
`master` directly to `seni_ror` (Rails) + `seni_sk` (Sidekiq) via `./deploy.sh` (README —
pre-compiles assets, `db:migrate` from `seni_sk`, `systemctl restart` both). **Both "merge to
`master`" and "run `./deploy.sh`" are §5c always-stop gates** (default-branch merge; production
deploy) — Sophia opens each PR and stops; a human (Gary or Envoy-with-delegated-authority) merges
and separately authorizes the deploy. No `*_beta` self-merge authority applies here (that's
scoped to `*_beta` repos only) — every PR in this plan needs an explicit human merge.

### ✅ Pre-flight Completeness (§5d)

No execution unit below requires reading a file/state not already captured in §1a–§1d above.

---

## 2. Sequenced plan — ONE PR per execution turn (§5a)

### PR1 — `Brokerages::Schwab` model + registry + OAuth client factory + config + safety spec

Files:
- **New** `app/models/brokerages/schwab.rb` — `Brokerages::Schwab < Brokerages::BrokerageInterface`.
  `BROKERAGE_NAME = "schwab"`, `BROKERAGE_DISPLAY_NAME = "Charles Schwab"`,
  `SUPPORTED_EXCHANGES = ["nyse", "nasdaq"]`. Implement (mirroring `ameritrade.rb`'s shape,
  adjusted for Schwab's Trader API request paths — confirm exact paths against Schwab's docs at
  write time, expected to be `/trader/v1/accounts?fields=positions` and similar under
  `api.schwabapi.com`): `self.is_linked?(user_id)`, `initialize(user_id)`, `display_name`,
  `can_trade?` (return `false` — explicit, not just inherited, so it self-documents as
  read-only), `brokerage_name`, `brokerage_account_id`, `fetch_brokerage_token`,
  `fetch_account_details`, `account_positions`, `current_cash_balance`,
  `current_portfolio_value`, `fetch_market_price`/`fetch_market_quote`, and the market-hours
  methods (`market_hours`, `opening_time`/`opening_hour?`, `closing_time`/`closing_hour?`,
  `trading_time?`, `market_open?`, `pre_market_open?`, `post_market_open?`) — Schwab's Trader
  API exposes a market-hours endpoint with an equivalent shape to TDA's; confirm at write time.
  **Do NOT define** `place_order_market`, `place_order_limit`, `cancel_all_orders`,
  `cancel_order` — leave inherited (`NotImplementedError`).
- **Edit** `app/models/brokerages/brokerage_manager.rb` — add `"schwab" => Brokerages::Schwab`
  to `SUPPORTED_BROKERAGES`.
- **Edit** `app/models/oauth2_credential.rb` — add `when "schwab" then schwab_client` to
  `fetch_client`, and a `schwab_client` class method: `OAuth2::Client.new(
  SentimentImporter::Application.config.schwab_client_id,
  SentimentImporter::Application.config.schwab_client_secret,
  site: config.schwab_site_url, authorize_url: config.schwab_authorize_url,
  token_url: config.schwab_token_url)` — **note the non-nil secret**, unlike `amtd_client`.
- **Edit** `config/application.rb` — add `config.schwab_site_url`, `schwab_authorize_url`,
  `schwab_token_url` (public, non-secret, fine to commit — same pattern as the amtd URL
  constants) and `config.schwab_client_id = ENV["SCHWAB_CLIENT_ID"]`, `config.schwab_client_secret
  = ENV["SCHWAB_CLIENT_SECRET"]` (env-sourced, **not hardcoded** — see the anti-pattern note in
  §1a).
- **New** `spec/models/brokerages/schwab_spec.rb` + `spec/fixtures/json_responses/
  schwab_account_details.json` (+ market price/hours fixtures as needed) — mirror
  `ameritrade_spec.rb`'s structure and stubbing style. **Must include** an explicit safety
  assertion: `expect { schwab.place_order_market(...) }.to raise_error(NotImplementedError)`
  (and same for `place_order_limit`, `cancel_all_orders`) — this is the enforcement mechanism
  for §0's hard scope boundary, not just a design note.
- **Edit** `spec/models/brokerages/brokerage_manager_spec.rb` — extend existing coverage to
  assert `"schwab"` is in `supported_brokerages`.

Self-UAT: `bundle exec rspec spec/models/brokerages/schwab_spec.rb
spec/models/brokerages/brokerage_manager_spec.rb spec/models/oauth2_credential_spec.rb` green,
locally, before opening the PR. No live Schwab credentials needed (all HTTP stubbed).

### PR2 — OAuth link/callback flow (plain controller, not Devise omniauth)

Files:
- **New** `app/controllers/schwab_link_controller.rb` (or similarly named) with two actions:
  - `connect` (`GET /schwab/connect`) — `before_action :authenticate_user!`; builds the Schwab
    authorize URL via `Oauth2Credential.fetch_client("schwab").auth_code.authorize_url(
    redirect_uri: schwab_callback_url, scope: <confirm Schwab's required scope string at write
    time>)`, `redirect_to` it.
  - `callback` (`GET /schwab/callback`) — `before_action :authenticate_user!`; exchanges
    `params[:code]` for tokens (`Oauth2Credential.fetch_client("schwab").auth_code.get_token(
    params[:code], redirect_uri: schwab_callback_url)`), persists via
    `current_user.oauth2_credentials.where(provider: "schwab").first_or_initialize` (mirror the
    field assignment in `CallbacksController#amtd`'s tail: `access_token`, `refresh_token`,
    `expires_at`), sets `current_user.default_brokerage = "schwab"` if the user has none set yet
    (don't clobber an existing default silently — only set if blank), redirects to the account/
    brokerage page with a success notice.
- **Edit** `config/routes.rb` — add the two routes (`get "/schwab/connect"`,
  `get "/schwab/callback"`), near the existing `brokerage`/`linked_brokerages` routes.
- **Edit** `app/views/daily_trades/_link_brokerage.html.erb` — add a "Link Charles Schwab"
  button pointing at `/schwab/connect`, alongside the existing brokerage-linking UI.
- **New** `spec/requests/schwab_link_spec.rb` (or controller spec, matching whatever pattern
  `spec/` uses for other controllers — check one similar existing request/controller spec for
  the house style before writing) — stub `OAuth2::Client#auth_code` (`authorize_url` and
  `get_token`) and assert: unauthenticated `connect` redirects to sign-in; authenticated
  `connect` redirects to a URL containing the configured `schwab_authorize_url`; `callback` with
  a stubbed successful token exchange creates/updates an `Oauth2Credential` row with
  `provider: "schwab"` for `current_user` and sets `default_brokerage` only when previously
  blank.

Self-UAT: `bundle exec rspec spec/requests/schwab_link_spec.rb` green with stubbed OAuth2
responses. **A real end-to-end OAuth round-trip against live Schwab is NOT possible yet** —
Gary has not registered a Schwab developer app (§1c) — so this PR's human UAT is explicitly
**deferred**, not skipped: see §4 below, which happens after PR2 (and PR3) ship, once Gary
completes registration.

### PR3 — Read-only positions/account API + doc

Files:
- **Edit** `app/controllers/api_controller.rb` — new action, e.g. `def positions` (name it to
  avoid colliding with the existing `PortfolioAllocation`-based `holdings` action — see §1a):
  calls `Brokerages::BrokerageInterface.brokerage(current_user.id)`, returns
  `.account_positions` (symbol/market_value/long_quantity per `Brokerages::ActivePosition`) +
  `.current_cash_balance` + `.current_portfolio_value` as JSON. 404/graceful-empty if no
  brokerage linked (mirror the `brokerage_linked` boolean pattern already used in
  `user_brokerage_info`).
- **Edit** `config/routes.rb` — add the route for the new action, under the existing `/api/`
  namespace alongside `holdings`/`watchlist`/`me`.
- **New** `spec/requests/api/positions_spec.rb` (or wherever the existing `/api/holdings`
  spec lives — mirror its structure) — stub a linked Schwab `Oauth2Credential` + stubbed
  `account_positions` response, assert the JSON shape.
- **Edit** `Mobile_API.md` — add a `## Positions (raw brokerage read)` section documenting the
  new endpoint (mirror the existing `## User holdings` doc block's format), **plus a note on
  the 7-day Schwab refresh-token expiry** (§1b) so anyone consuming this endpoint later knows
  why it might start 401ing weekly until re-linked.

Self-UAT: `bundle exec rspec spec/requests/api/positions_spec.rb` green, stubbed.

---

## 3. Resume tracker

| Unit | Advance | PR opened | Merged (human) | Self-UAT | Deployed |
|------|---------|-----------|-----------------|----------|----------|
| PR1 — Schwab brokerage model + registry + safety spec | _(auto)_ | ☐ | ☐ | ☐ | n/a |
| PR2 — OAuth link/callback controller + routes + view | _(auto)_ | ☐ | ☐ | ☐ | n/a |
| PR3 — read-only positions API + doc | _(auto)_ | ☐ | ☐ | ☐ | `gate: prod deploy` (also always-stop) |

**RESUME HERE = PR1.** No `Auto-start` — this plan waits for the governor's explicit "go for
it" in its Telegram topic before touching PR1 (default; this is a first-of-its-kind live
personal-brokerage integration, not a routine follow-up, so the extra confirmation point is
deliberate, not an oversight).

---

## 4. UAT — deferred human step, not skippable, not part of PR1–PR3

Per §5's "Self-UAT before human UAT" rule: PR1–PR3 each carry their own automated self-UAT
(rspec, stubbed) as described above, and Sophia must run+pass those before opening each PR — no
PR opens with a red local spec run. But the **full end-to-end human UAT — actually linking
Gary's real Schwab account and confirming real positions come back correctly — cannot happen
until Gary completes Schwab developer app registration** (a step only he can do; see the prior
session's discussion — Schwab ties app registration to his own login/identity, no API for it).

**Sequence after PR1–PR3 all merge:**
1. Gary registers a Schwab developer app (schwab-tradeapi.schwab.com), gets `client_id` +
   `client_secret`, registers the callback URL Perch's `/schwab/callback` route resolves to on
   `seni_ror`.
2. `SCHWAB_CLIENT_ID` / `SCHWAB_CLIENT_SECRET` are set on the production host's systemd env file
   (never committed — `WORKSPACE_CONTEXT.md` §3a), and PR3's deploy gate is cleared (human GO,
   then `./deploy.sh`).
3. **Gary + the `analyst` Claude Code seat work through the login/linking together** (as Gary
   specified) — visit `/schwab/connect`, complete Schwab's consent screen, confirm the callback
   creates the `Oauth2Credential` row and `GET /api/positions` returns his real live holdings.
   This is the real acceptance test for the whole plan; nothing before this point can fully
   verify it.
4. Acceptance criterion: `/api/positions` (or whatever the final route is named) returns Gary's
   actual Schwab positions with correct symbol/quantity/market value, and no order-placement
   method is reachable (confirmed by PR1's spec, re-confirmed live by attempting nothing —
   there's no UI path to a live order, by construction).

---

## 5. Contribution reporting

Per `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md` — Sophia reports a `[CONTRIBUTION EVENT]` (contributor
"Sophia Truesight") after each PR merges, citing that PR's GitHub URL, before starting the next
PR in this plan.
