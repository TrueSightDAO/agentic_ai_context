# `/large_spikes` — Disappearing Cards Fix + Breakout-Gauge Legibility — Execution Roadmap

**Author:** Claude Anthropic (Opus 4.8) — 2026-07-05
**Target repo:** **TrueSightDAO/sentiment_importer** (Perch — Rails; deploys to **perch.truesight.me**)
**Handoff to:** Sophia (autopilot)
**Follow-up to:** `LARGE_SPIKE_INDEX_EXECUTION_ROADMAP.md` (the original `/large_spikes` build, thread 8297) and
`LARGE_SPIKE_INDEX_REVIEW_AND_RECTIFICATION.md` (F2 — the breakout chart — is now built; this plan hardens it).

> **Repo gate:** `sentiment_importer` is an own-repo for Sophia — **open PRs only, NEVER self-merge.** A human merges.
> **Deploy gate:** Perch has **no auto-deploy on merge**. Going live requires `./deploy.sh --skip-migrate` on the prod
> box (no schema change in this plan). The deploy is an always-stop gate (§5c).

---

## 0. TL;DR — what we are fixing and why

Two problems the governor reported on **https://perch.truesight.me/large_spikes**:

1. **All company cards vanish on some views.** Root cause is a **period-keyed cache mismatch**: the "Lookback Period"
   selector offers `1080` (3yr), `3600` (10yr), `7200` (20yr), `10800` (30yr), but the refresher worker only
   pre-generates the per-card S3 cache for `[7, 30, 90, 180, 360, 720, 1800]`. The card list fetch-only helper misses
   → returns `[]` → **no cards**. The chart keeps rendering because it reads the DB directly (period-independent), so
   the symptom is exactly "chart fine, cards gone." (The sector pie also survives — it uses the always-present 7-day
   cache — so on a broken view you even see the pie populated while the grid below it is empty. That inconsistency is
   the tell.)

2. **The "Market Breakout Participation" gauge is hard to interpret.** Two concrete gaps: (a) the read-box promises a
   **"shaded over-extended zone"** but the orange band dataset is set to `fill: false`, so nothing is actually shaded —
   just a thin dashed line; (b) there is **no "you are here" numeric readout**, so the user has to eyeball whether the
   green line sits above/below a dashed grey line with no anchor number.

**Fix shape:** 2 small, view-only PRs. No migration, no model changes, no data mutation, no money.

---

## 1. Pre-flight checklist (§5d — Pre-flight Completeness gate)

> ✅ **Pre-flight Completeness:** no execution unit requires reading a file/state not already captured in this
> pre-flight. Both PRs edit exactly one view file each in `sentiment_importer`; all current-state snapshots, the
> Chart.js version, the helper return-shapes, and the existing spec are captured below.

### 1a. Access / prerequisites
- Sophia has push access to `TrueSightDAO/sentiment_importer` (via the agent SSH key). Branch + PR; do not self-merge.
- No credentials, no env vars, no external services touched. Pure Rails view logic.
- Ruby/RSpec toolchain already present (`spec/requests/large_spikes_spec.rb` exists and passes today).

### 1b. Confirmed facts (root-cause evidence)

**The period selector's values** — `app/helpers/application_helper.rb#period_nav_class` returns these `:value`s:
```
7 (week), 30 (month), 90 (quarter), 180 (six months), 360 (year), 720 (2 years),
1080 (3 years), 1800 (5 years), 3600 (10 years), 7200 (20 years), 10800 (30 years)
```

**The refresher only generates card caches for a subset** — `app/workers/large_spike_index_refresher.rb:101`:
```ruby
look_back_periods = [7, 30, 90, 180, 360, 720, 1800]
```
→ Missing card caches: **1080, 3600, 7200, 10800**. Selecting those four buttons ⇒ empty grid.

**The card fetch is fetch-only in production** — `app/helpers/daily_trades_helper.rb:133`:
```ruby
def large_spikes the_date_str, look_back_days=7, refresh_cache=false
  if refresh_cache || !Rails.env.production?
    begin
      generate_large_spikes_cache the_date_str, look_back_days
    rescue => e
      Rails.logger.error "[large_spikes] Cache generation failed for #{the_date_str}/#{look_back_days}: #{e.message}"
      return []
    end
  end
  fetch_large_spikes_cache the_date_str, look_back_days      # ← prod: miss ⇒ rescue ⇒ []
rescue => e
  Rails.logger.warn "[large_spikes] Cache not ready for #{the_date_str}/#{look_back_days}: #{e.message}"
  []
end
```
S3 key = `LARGE_SPIKES/#{Rails.env}/#{the_date_str}_#{look_back_days}` (`daily_trades_helper.rb:148`).

**The controller already sets a decoupled card lookback that the view never uses** —
`app/controllers/daily_trades_controller.rb#large_spikes` (lines 170–172):
```ruby
@the_period = params["period"] || 90
@the_period = @the_period.to_i
@the_company_period = 180        # ← set, but the view passes @the_period to the card list, not this
```
`@the_company_period = 180` is **currently dead** (grep confirms zero uses in the view/partials). `180` is always in
the generated cache set, so wiring the card list to it fixes every period selection at once. This is the intended
(but unwired) design.

**The set of card symbols is period-independent.** `generate_large_spikes_cache` derives symbols from
`interesting_spike_symbols(the_date_str)` (no `look_back_days` arg) and only varies the *fluctuation columns* by
`look_back_days` via `component_flucations_query`. So switching the card list from `@the_period` → `@the_company_period`
changes the per-card fluctuation window (to a consistent 180 days) but **not which companies appear** — and the count
will now match the sector pie (which uses the 7-day cache; same symbol set).

**Chart.js version (critical for PR2).** The app loads **Chart.js 2.9.3** globally in
`app/views/layouts/application.html.erb:42`:
```erb
<script src='https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js'></script>
```
The spike chart's inline script (`_spike_chart.html.erb`) runs at parse time on v2.9.3 and uses v2 API
(`scales.xAxes`, `tooltips`, `Chart.pluginService.register`). The bare `cdn.jsdelivr.net/npm/chart.js` (v4) include at
the bottom of `large_spikes.html.erb` loads *after* and is only consumed by the sector-pie script (v4 syntax, inside
`DOMContentLoaded`). **PR2 must use Chart.js v2.9.3 fill syntax** (`fill: 'end'`), not v3/v4 `fill` objects.

**Current over-extended dataset** — `app/views/daily_trades/_spike_chart.html.erb` (dataset 3, ~lines 125–136):
```js
    },{
      label: 'Over-extended — stop chasing',
      data: <%= raw(chartjs_spike_upper_bollinger(@current_date, @the_period)) %>,
      backgroundColor: 'rgba(249, 115, 22, 0.10)',
      borderColor: '#f97316',
      borderWidth: 1.5,
      borderDash: [3, 3],
      fill: false,               // ← nothing is shaded; read-box promises a shaded zone
      pointRadius: 0,
      pointHoverRadius: 0,
      tension: 0.4
    }]
```

**Helpers available for the PR2 headline (no new model code needed)** —
`app/helpers/daily_trades_helper.rb`:
- `chartjs_spike_values(current_date, the_period)` → array of participation %, ascending by date; `.last` = today.
- `chartjs_spike_sma_values(current_date, the_period)` → array (the "Norm" line); `.last` = today's norm.
- `chartjs_spike_upper_bollinger(current_date, the_period)` → array; `.last` = today's over-extended threshold.
All three already back the chart datasets, so reusing them for a server-rendered headline is zero-risk. Guard `nil`
(`plot_sma_values` can return a shorter/empty array early in history).

**Existing spec** — `spec/requests/large_spikes_spec.rb` (70 lines) already covers `GET /large_spikes` → 200,
`GET /large_spikes/:period/:the_date` → 200, and the non-trading-day redirect. It stubs page helpers via a
`shared_examples "stub spike page helpers"` block (stubs `large_spikes` → `[]`, `sector_distribution_for_large_spikes`
→ `nil`, and the three `MacroIndicator.spike_*` methods). New tests extend this file and reuse its patterns.

### 1c. Decision already made (no gate)
- **Card lookback = `@the_company_period` (180), not the URL period.** Chosen over "add the 4 missing periods to the
  worker" because the worker approach generates 4 extra large S3 caches every day and leaves the conceptual
  conflation (`@the_period` meaning both "chart window" and "card fluctuation window") in place. Wiring the already-set
  `@the_company_period` is smaller, cheaper, and matches the original intent.

---

## 2. Sequenced plan (§5a — ONE PR per execution turn, then STOP)

### PR1 — Card list keys off the fixed 180-day company lookback (functional fix) 🔴

**Branch:** `fix/large-spikes-cards-fixed-lookback`
**File:** `app/views/daily_trades/large_spikes.html.erb` (only)

**Change:** replace every card-list call `large_spikes(@current_date, @the_period)` with
`large_spikes(@current_date, @the_company_period)`. There are **7 occurrences**, all in the card section
(current lines **90, 96, 111, 114, 119, 123, 135**). This exact substring appears only in the card section of this
one file — a scoped `replace_all` of `large_spikes(@current_date, @the_period)` →
`large_spikes(@current_date, @the_company_period)` in this file is complete and safe.

**Do NOT touch:**
- `chartjs_spike_*(@current_date, @the_period)` in `_spike_chart.html.erb` — the chart window stays user-selectable.
- `period_nav_class(@the_period)` / `large_spikes_with_period_n_date_path(@the_period, ...)` in the nav/period
  partials — the selected-period button must still reflect the chart window.
- `sector_distribution_for_large_spikes(@current_date.to_s)` (line 45) — already period-independent (7-day cache).

**Tests (extend `spec/requests/large_spikes_spec.rb`):** add a context that proves the card list no longer keys off
the URL period. Drop this in (standalone before-block, not the shared stub, so the `with(anything, 180)` expectation
is meaningful):
```ruby
  describe "card list lookback decoupling (regression: cards vanished on long periods)" do
    before do
      allow(DailyTrade).to receive(:most_recent_us_market_trading_date).and_return(trade_date)
      allow(DailyTrade).to receive(:count_qualified_trades).and_return(2000)
      allow_any_instance_of(DailyTradesHelper).to receive(:sector_distribution_for_large_spikes).and_return(nil)
      allow(MacroIndicator).to receive(:spike_over_period).and_return({})
      allow(MacroIndicator).to receive(:spike_sma_over_period).and_return([])
      allow(MacroIndicator).to receive(:spike_upper_bollinger_over_period).and_return([])
    end

    it "fetches the card list with the fixed 180-day company lookback regardless of the 30-year URL period" do
      expect_any_instance_of(DailyTradesHelper).to receive(:large_spikes)
        .with(anything, 180).at_least(:once).and_return([])
      get large_spikes_with_period_n_date_path(period: 10800, the_date: trade_date.to_s),
          headers: BROWSER_HEADERS
      expect(response).to have_http_status(:ok)
    end
  end
```
Run `bundle exec rspec spec/requests/large_spikes_spec.rb` — all green before opening the PR (§9 test-before-merge).

**PR body must state:** goal (cards vanished on 3/10/20/30-year lookbacks — period-keyed cache miss), the fix
(wire the dead `@the_company_period`), why not the worker-list approach, the regression test, and the deploy note
(`./deploy.sh --skip-migrate`, no schema change).

**Advance:** auto (code unit, own-repo → opens PR only). Stops at human merge (own-repo gate).

---

### PR2 — Breakout-gauge legibility: shaded over-extended band + "today vs norm" headline (UX) 🟡

**Branch:** `feat/breakout-gauge-legibility`
**File:** `app/views/daily_trades/_spike_chart.html.erb` (only)
**Do PR2 only after PR1 is merged** (both would touch this page; keeping them one-file-each avoids conflicts).

**Change A — shade the over-extended zone (Chart.js v2.9.3 syntax).** In dataset 3 (`'Over-extended — stop chasing'`),
change `fill: false` → `fill: 'end'`. In v2.9.3, `fill: 'end'` fills from the line to the top of the scale, so the
existing `backgroundColor: 'rgba(249, 115, 22, 0.10)'` becomes a faint orange wash over the whole region **above** the
threshold — i.e. the "over-extended zone" the read-box already describes. No other dataset changes (green stays
`fill: true` to origin; grey Norm stays `fill: false`).

**Change B — add a server-rendered "you are here" headline** in the `.chart-header`, above the `<canvas>`. Insert
after the `<p class="chart-subtitle">…</p>` line:
```erb
  <% _spike_series = chartjs_spike_values(@current_date, @the_period) %>
  <% _norm_series  = chartjs_spike_sma_values(@current_date, @the_period) %>
  <% _band_series  = chartjs_spike_upper_bollinger(@current_date, @the_period) %>
  <% _today = _spike_series.respond_to?(:last) ? _spike_series.last : nil %>
  <% _norm  = _norm_series.respond_to?(:last) ? _norm_series.last : nil %>
  <% _band  = _band_series.respond_to?(:last) ? _band_series.last : nil %>
  <% if _today && _norm %>
    <% if _band && _today >= _band %>
      <% _regime_label = "Over-extended — stop initiating" %><% _regime_class = "regime-hot" %>
    <% elsif _today > _norm %>
      <% _regime_label = "Risk-on — broad leadership" %><% _regime_class = "regime-up" %>
    <% else %>
      <% _regime_label = "Narrow — stand aside" %><% _regime_class = "regime-flat" %>
    <% end %>
    <div class="breakout-now <%= _regime_class %>" id="breakoutNow">
      <span class="breakout-now-metric">Today <strong><%= _today %>%</strong> participation</span>
      <span class="breakout-now-sep">·</span>
      <span class="breakout-now-metric">Norm <strong><%= _norm %>%</strong></span>
      <span class="breakout-now-sep">·</span>
      <span class="breakout-now-regime"><%= _regime_label %></span>
    </div>
  <% end %>
```
Add matching CSS in the partial's `<style>` block (colors mirror the read-box dots: up `#16a34a`, flat `#64748b`,
hot `#f97316`):
```css
.breakout-now { display:flex; flex-wrap:wrap; align-items:center; gap:8px; margin-top:12px;
  padding:10px 14px; border-radius:10px; font-size:14px; background:#f8fafc; border:1px solid #e2e8f0; }
.breakout-now .breakout-now-sep { color:#cbd5e1; }
.breakout-now .breakout-now-regime { font-weight:700; }
.breakout-now.regime-up   { border-left:4px solid #16a34a; }
.breakout-now.regime-up   .breakout-now-regime { color:#16a34a; }
.breakout-now.regime-flat { border-left:4px solid #64748b; }
.breakout-now.regime-flat .breakout-now-regime { color:#475569; }
.breakout-now.regime-hot  { border-left:4px solid #f97316; background:#fff7ed; }
.breakout-now.regime-hot  .breakout-now-regime { color:#c2410c; }
```
(Optional polish, not required: update the read-box copy so "shaded 'over-extended' zone" now literally matches the
newly shaded band.)

**Tests (extend `spec/requests/large_spikes_spec.rb`):** add a context that stubs the three chart helpers with data
and asserts the headline + fill mode render:
```ruby
  describe "breakout gauge legibility" do
    before do
      allow(DailyTrade).to receive(:most_recent_us_market_trading_date).and_return(trade_date)
      allow(DailyTrade).to receive(:count_qualified_trades).and_return(2000)
      allow_any_instance_of(DailyTradesHelper).to receive(:large_spikes).and_return([])
      allow_any_instance_of(DailyTradesHelper).to receive(:sector_distribution_for_large_spikes).and_return(nil)
      # chart datasets + headline read from these:
      allow_any_instance_of(DailyTradesHelper).to receive(:chartjs_spike_dates).and_return(%w[a b c])
      allow_any_instance_of(DailyTradesHelper).to receive(:chartjs_spike_values).and_return([3.0, 4.0, 6.2])
      allow_any_instance_of(DailyTradesHelper).to receive(:chartjs_spike_sma_values).and_return([3.5, 3.8, 4.1])
      allow_any_instance_of(DailyTradesHelper).to receive(:chartjs_spike_upper_bollinger).and_return([7.0, 7.0, 7.0])
    end

    it "renders the today-vs-norm headline with a regime read" do
      get large_spikes_path, headers: BROWSER_HEADERS
      expect(response.body).to include('id="breakoutNow"')
      expect(response.body).to include('6.2%')          # today
      expect(response.body).to include('4.1%')          # norm
      expect(response.body).to include('Risk-on — broad leadership')  # 6.2 > 4.1, below 7.0 band
    end

    it "shades the over-extended band (Chart.js v2 fill mode)" do
      get large_spikes_path, headers: BROWSER_HEADERS
      expect(response.body).to include("fill: 'end'")
    end
  end
```
Run `bundle exec rspec spec/requests/large_spikes_spec.rb` — all green before the PR.

**Advance:** auto (code unit, own-repo → opens PR only). Stops at human merge.

---

### DEPLOY + UAT (always-stop gate 🚪 — human runs; Sophia does NOT deploy)

After **both** PRs are merged by a human:
1. On the Perch prod box: `./deploy.sh --skip-migrate` (no schema change — do NOT run migrations).
2. **UAT (human eyeball on https://perch.truesight.me/large_spikes — read-only page, fully revertible):**

| # | Surface / URL | Interaction | Expect | Pass? |
|---|---------------|-------------|--------|-------|
| U1 | `/large_spikes` (default, quarter) | load | Cards grid populated; sector pie count == "Assets Surging" count | ☐ |
| U2 | Lookback Period → **3 years** | click | Cards **still render** (previously empty); chart window widens to 3yr | ☐ |
| U3 | Lookback Period → **10 years / 20 years / 30 years** | click each | Cards render on all three (previously empty) | ☐ |
| U4 | Any view | look at gauge top | Headline "Today X% participation · Norm Y% · <regime>" shows and matches line-vs-dashed position | ☐ |
| U5 | A day where the green line pokes above the orange dashed line | inspect | The region above the orange threshold is visibly **shaded** orange; headline reads "Over-extended" | ☐ |
| U6 | Regression | click week/month/quarter/6mo/year/2yr/5yr | Cards render on every one (no regression) | ☐ |

**Acceptance:** U1–U6 all pass. If U5 can't be observed on the current date, it's satisfied by the unit test
(`fill: 'end'` present) + eyeballing that the band shades when the threshold line is within the visible y-range.

---

## 3. Resume tracker

> ### 👉 RESUME HERE = **PR1**

| Unit | Advance | PR opened | Merged (human) | Deployed | Contribution reported |
|------|---------|-----------|----------------|----------|----------------------|
| **PR1** — cards → `@the_company_period` (180) | _(auto)_ | ☐ | ☐ | n/a (batch at deploy) | ☐ |
| **PR2** — shaded band + today-vs-norm headline | _(auto)_ | ☐ | ☐ | n/a (batch at deploy) | ☐ |
| **DEPLOY + UAT** | `gate: prod deploy + UAT` (always-stop) | n/a | n/a | ☐ | ☐ |

**Per-unit close-out:** after each PR merges, report the DAO contribution before starting the next
(`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`; Sophia files as `"Sophia Truesight"`), and tick the row above.

> ✅ **Pre-flight Completeness self-cert:** no execution unit requires reading a file/state not already captured in §1.
> Both PRs edit one view file each; exact current snippets, Chart.js version, helper shapes, and the existing spec are
> all in the pre-flight.

---

## 4. Notes / non-goals
- **No worker change.** We deliberately do not add `1080/3600/7200/10800` to `large_spike_index_refresher.rb`'s
  `look_back_periods`; the decoupling in PR1 makes that unnecessary and avoids 4 extra daily S3 caches.
- **No model/migration change.** Deploy with `--skip-migrate`.
- **No money, no TDG, no external calls, no data mutation.** Pure view-layer read fixes; fully revertible by reverting
  the PRs and redeploying.
- **F1/F2/F4 from `LARGE_SPIKE_INDEX_REVIEW_AND_RECTIFICATION.md` are already resolved in `master`** (EOD spike
  refresh triggers wired; the breakout chart built; the request spec exists) — do not redo them.
