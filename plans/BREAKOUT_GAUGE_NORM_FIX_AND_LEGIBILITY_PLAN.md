# `/large_spikes` regime gauge — Norm/Bollinger window fix + legibility simplification

**Author:** Envoy (Claude Code, interactive seat) — 2026-08-24
**Target repo:** **TrueSightDAO/sentiment_importer** (Perch — Rails; deploys to **perch.truesight.me**)
**Handoff to:** Sophia (autopilot)
**Follow-up to:** `LARGE_SPIKES_CARD_FIX_AND_CHART_LEGIBILITY_PLAN.md` (2026-07-05, superseded/implemented —
built the current regime-gauge chart this plan is now correcting) and the 2026-08-24 empirical backtest
of `/large_spikes` signals (logged in `garyjob/perch-market-analysis`, personal repo).

> **Repo gate:** `sentiment_importer` is an own-repo for Sophia — **open PRs only, NEVER self-merge.** A
> human merges.
> **Deploy gate:** Perch has **no auto-deploy on merge**. Going live requires `./deploy.sh --skip-migrate`
> on the prod box (no schema change in this plan — no migration needed, everything below is app code
> only). Deploy is an always-stop gate (§5c) — see Authorization envelope below for how it's pre-scoped
> for this specific arc.

---

## 0. TL;DR — what we're fixing and why

The governor flagged (screenshot, 2026-08-24) that the "Market Breakout Participation" regime gauge on
`/large_spikes` is hard to read. Root-caused to a real bug, not just a design problem:

**The "Norm (typical breadth)" line and the "Over-extended — stop chasing" line are computed over two
different, statistically incompatible lookback windows** — Norm uses a hardcoded 180-day plain SMA
(`spike_sma_over_period`), while Over-extended uses a 30-day Bollinger band (`bollinger_period_days`
config). A coherent Bollinger-style band needs the SAME window for its center line and its boundary. The
mismatch means Norm barely moves for months after any regime change (a 180-day average needs ~9 months
of new data to meaningfully shift), making "today vs. Norm" a near-useless comparison for most of any
given regime — exactly the confusion the governor reported. The design doc for this chart even describes
Norm as a **20-day** SMA — never matching what's actually shipped (180-day) either.

The fix isn't "pick a new number" — `app/helpers/companies_helper.rb`'s `plot_bollinger_values` already
computes a `"middle"` variant (`plot_bollinger_middle`) that IS the exact SMA the Over-extended band is
built around. Wiring Norm to that, instead of the separate 180-day method, makes Norm and the band a
genuinely coherent pair for free — no config guessing.

Separately, the governor asked for visual simplification: less dead flat-zero space, less visually
dominant "danger" shading, more prominence for the plain-English verdict sentence that's already correct
and already there.

---

## 1. Pre-flight (§5d — everything below is captured so no PR turn needs to re-discover it)

### 1.1 The buggy code (what Norm currently does)

`app/models/macro_indicator.rb` (~line 112-116):
```ruby
def spike_sma_over_period period=180, current_date=Time.now
  spike_index = Company.fetch_sym SentimentImporter::Application.config.market_spike_symbol
  plot_sma_values(spike_index, current_date, 180, period, 4).map {|sma_value|
     (sma_value * 100).round(2)
  }
end
```
Note the method's own parameter is named `period=180` (the chart's overall display window, e.g. the 90
calendar days a user has selected) — but it hardcodes the SMA lookback (`plot_sma_values`'s third
positional arg) to `180` regardless of what `period` is passed. This is a **plain SMA of `daily_trades.close`**
on the synthetic `LARGE_SPIKE_INDEX` company row — nothing to do with the Bollinger machinery used for
the sibling line.

### 1.2 The correct machinery that already exists (don't touch — reuse)

`app/helpers/companies_helper.rb`:
```ruby
BOLLINGER_LOOKBACK_PERIOD = SentimentImporter::Application.config.bollinger_period_days  # = 30
                                                                          # (config/application.rb:207)

def plot_bollinger_values range_type, company, current_date=Time.now.to_date.to_s, period=DEFAULT_PERIOD
  # ... computes, per point, sma_val over the trailing BOLLINGER_LOOKBACK_PERIOD (30) days, then:
  #   "upper"  -> sma_val + stddev * STD_DEV_MULTIPLE
  #   "middle" -> sma_val                              <-- this is what Norm SHOULD be
  #   "lower"  -> sma_val - stddev * STD_DEV_MULTIPLE
end

def plot_bollinger_upper  company, current_date=..., period=DEFAULT_PERIOD
  plot_bollinger_values "upper", company, current_date, period
end
# plot_bollinger_middle already exists too (same pattern, range_type="middle") — confirmed present.
```

`app/models/macro_indicator.rb` (~line 119-123) already has the pattern to mirror:
```ruby
def spike_upper_bollinger_over_period period=180, current_date=Time.now
  spike_index = Company.fetch_sym SentimentImporter::Application.config.market_spike_symbol
  plot_bollinger_upper(spike_index, current_date, period).map {|bollinger_value|
     (bollinger_value * 100).round(2)
  }
end
```
This is the exact pattern PR1 replicates for `plot_bollinger_middle`.

### 1.3 The chart view

`app/views/daily_trades/_spike_chart.html.erb`:
- Line 6: `<% _norm_series = chartjs_spike_sma_values(@current_date, @the_period) %>` — feeds the header
  stat block's `_norm` value (line 9, `_norm_series.last`) — this is the buggy 180-day value the governor
  saw as "Norm 2.04%".
- Line 11-18: regime classification logic — `_today >= _band` → "Over-extended"; `_today > _norm` →
  "Risk-on"; else → "Narrow — stand aside". This logic itself is fine and needn't change; it just needs
  `_norm` to be the corrected value.
- Line 149: the "Norm (typical breadth)" Chart.js dataset's `data:` also calls `chartjs_spike_sma_values`
  — same substitution needed here as line 6.
- Lines 127-169: full three-dataset Chart.js config. Dataset 0 = "Breakout Participation" (green, solid,
  gradient-filled). Dataset 1 = "Norm (typical breadth)" (gray, dashed, `borderWidth: 2`, no fill).
  Dataset 2 = "Over-extended — stop chasing" (orange, dashed, `borderWidth: 1.5`,
  `backgroundColor: 'rgba(249, 115, 22, 0.10)'`, `fill: 'end'` — this `fill:'end'` is what shades the
  entire region from the Over-extended line up to the y-axis max (35% in the governor's screenshot),
  regardless of how far today's reading actually is from that boundary. **Chart.js v2.9.3 is in use here
  — confirmed by the existing PR history (`LARGE_SPIKES_CARD_FIX_AND_CHART_LEGIBILITY_PLAN.md` explicitly
  flags "do NOT use v3/v4 fill objects" — same constraint applies to any new fill-related change in PR2.**
- `app/helpers/daily_trades_helper.rb`:
  - `chartjs_spike_sma_values` (line ~287-289) — thin wrapper, delegates to `MacroIndicator.spike_sma_over_period`.
  - `chartjs_spike_upper_bollinger` (line ~291-293) — same pattern, delegates to
    `MacroIndicator.spike_upper_bollinger_over_period`. PR1 adds a `chartjs_spike_norm_values` wrapper
    following this exact pattern.

### 1.4 Controller / period context

`app/controllers/daily_trades_controller.rb#large_spikes` sets `@the_period = params["period"] || 90` —
default display window is 90 calendar days (matches the governor's screenshot: ~May 11 – Aug 6 range).
The long flat-zero lead-in (mid-May to ~July 1) the governor found confusing is real data (`LARGE_SPIKE_INDEX`
genuinely read 0% for that stretch — independently confirmed via read-only SQL on `seni_sql` during the
2026-08-24 backtest session), not a rendering bug.

### 1.5 Existing test conventions to follow

Per `OPERATING_INSTRUCTIONS.md` §9 (HTML/JS test-before-merge rule), any change to a repo with
`index.html`/frontend JS — sentiment_importer qualifies — needs a local test before merge. Check
`spec/` for existing coverage of `_spike_chart.html.erb` or `macro_indicator.rb` before writing new specs
(don't assume none exists).

### ✅ Pre-flight Completeness (§5d)
No execution unit below requires reading a file/state not already captured above.

---

## 2. Authorization envelope (§5e — batched up front, not per-PR)

Given the governor's explicit ask ("ensure that she fixes and then deploys"), and that `sentiment_importer`'s
own standing rule + §5c mean merge-to-default-branch and prod-deploy are **always-stop gates regardless of
auto-advance settings** — Sophia will still pause and post asking for `go` at each of those points; that's
existing, deliberate safety behavior this plan doesn't (and shouldn't try to) override.

**Pre-authorized for this arc** (both PR1 and PR2, so the governor replies `go` once per gate rather than
re-litigating scope twice):
- Opening PRs, running local tests, iterating on review feedback: fully autonomous, no gate.
- **Merging PR1 and PR2** once tests pass and the diff matches this plan's scope: pre-authorized — post in
  this arc's Telegram thread that it's ready, then merge on the governor's next `go` (or if he's
  unresponsive for a while and the change is exactly in-scope per this doc, a human on the thread may
  merge directly — but Sophia herself still does not self-merge, per the standing repo rule).
- **Deploying after each merge** (`./deploy.sh --skip-migrate` — no migration in either PR): pre-authorized
  same way — post readiness, proceed on `go`.

**Not pre-authorized / still needs a fresh ask:**
- Any change outside this plan's explicit scope (e.g., if Sophia discovers PR1's fix has knock-on effects
  on another chart also using `spike_sma_over_period` — check for other callers before assuming it's
  dead code; if found, that's a **new** decision, flag it rather than silently expanding scope).
- PR2's specific visual choices (lead-in trimming approach, opacity values) are judgment calls flagged
  explicitly in section 3.2 below — Sophia should implement her best judgment per the guidance given, but
  the PR description should call out each visual change as a **discrete, individually revertible** tweak
  so the governor can approve/reject pieces independently rather than all-or-nothing.

---

## 3. Sequenced plan (§5a — ONE PR per execution turn)

### PR1 — Fix Norm to share the Bollinger band's window (bug fix, low risk)

1. In `app/models/macro_indicator.rb`, add (mirroring `spike_upper_bollinger_over_period` exactly):
   ```ruby
   def spike_bollinger_middle_over_period period=180, current_date=Time.now
     spike_index = Company.fetch_sym SentimentImporter::Application.config.market_spike_symbol
     plot_bollinger_middle(spike_index, current_date, period).map {|bollinger_value|
        (bollinger_value * 100).round(2)
     }
   end
   ```
2. In `app/helpers/daily_trades_helper.rb`, add (mirroring `chartjs_spike_upper_bollinger`):
   ```ruby
   def chartjs_spike_norm_values current_date, the_period=180
     MacroIndicator.spike_bollinger_middle_over_period the_period, current_date
   end
   ```
3. In `app/views/daily_trades/_spike_chart.html.erb`: change line 6 and line 149's data source from
   `chartjs_spike_sma_values` to `chartjs_spike_norm_values`. Do not touch the regime-classification
   logic (lines 11-18) — it already reads `_norm_series.last` generically and will pick up the corrected
   value automatically.
4. **Before deleting anything:** grep the whole repo for other callers of `chartjs_spike_sma_values` /
   `spike_sma_over_period` — if genuinely unused after this change, note it as dead code in the PR
   description for a human to decide on removal later; don't delete speculatively in this PR.
5. Add/update a spec asserting `chartjs_spike_norm_values` and `chartjs_spike_upper_bollinger` are
   computed over the same lookback (`bollinger_period_days`) — e.g. stub fixture `daily_trades` rows and
   assert the norm series and the middle-of-the-band value match for a known date.
6. PR description: goal (fix Norm/Band window mismatch — quote the governor's screenshot finding: Norm
   read 2.04% when it should track the 30-day band's center), before/after, testing, note this is a pure
   bug fix with no visual/design judgment calls (contrast with PR2).

### PR2 — Visual legibility simplification (governor-requested polish, more judgment involved)

1. **Trim the dead flat-zero lead-in.** Preferred approach (safer — doesn't change the underlying data
   window, just what's rendered): have the chart auto-scale its visible x-range to start at the first
   non-zero `Breakout Participation` reading within the fetched `@the_period`, rather than always showing
   the full period from day 1. If that proves awkward to implement cleanly in the Chart.js v2.9.3 config,
   the fallback is reducing `@the_period`'s default in `daily_trades_controller.rb#large_spikes` from 90
   to a shorter window (e.g. 45) — flag which approach was taken and why in the PR description, this is a
   judgment call.
2. **Reduce the Over-extended zone's visual dominance.** Current `fill:'end'` shades the entire region
   from the Over-extended line to the chart's y-axis max regardless of how far away today's reading is.
   Reduce `backgroundColor` opacity from `rgba(249, 115, 22, 0.10)` to something lighter (try `0.06`) so
   it reads as a boundary marker, not a dominant "danger zone" filling half the chart. **Chart.js
   v2.9.3 constraint — no v3/v4 fill objects.**
3. **Thin the Norm line slightly relative to the main data series** (`borderWidth` currently 2 — consider
   1.5) now that PR1 makes it move meaningfully and it shouldn't visually compete with the primary green
   line.
4. **Elevate the header verdict block** (`.breakout-now`, lines 19-25 + CSS ~lines 89-98) — it already
   states the plain-English answer correctly ("Today X% · Norm Y% · Risk-on — broad leadership"); increase
   its relative prominence (font-size/weight) versus the chart title, since for a quick-glance read this
   sentence IS the answer, the chart below is supporting detail.
5. Add/update a JSDom or Percy-style test per §9 covering: chart renders with 3 datasets; header verdict
   block renders the correct `regime_class` for stubbed today>norm / today<norm / today>=band fixtures.
6. PR description: goal, changes (list each visual tweak as a **discrete, individually revertible** item),
   testing, explicit note that this is subjective governor-requested polish, not a correctness fix
   (contrast with PR1) — so review can approve pieces independently if some land better than others.

---

## 4. Resume tracker

**RESUME HERE →** PR1 (bug fix) — not started.

| Unit | Status | PR opened | Merged (human, pre-authorized this arc) | Deployed (human, pre-authorized this arc) |
|---|---|---|---|---|
| PR1 — Norm/Bollinger window fix | not started | ☐ | ☐ | ☐ |
| PR2 — Visual legibility simplification | not started | ☐ | ☐ | ☐ |

PR2 does not strictly depend on PR1 being deployed first (the visual changes are independent of the
data-correctness fix), but sequencing PR1 first is still correct: it's lower-risk, and isolating its
deploy-and-verify cycle before layering visual changes on top makes it easy to tell which change caused
which effect if something looks off.

---

## 5. UAT (human-facing surface — required per §5)

For **each** unit, after its deploy:

1. **Surface:** `https://perch.truesight.me/large_spikes` (check `NOTES_sentiment_importer.md` for
   whether a staging/beta target exists for this repo before assuming prod is the only option — if none
   exists, UAT happens on prod immediately post-deploy; low risk since this is read-only display data,
   not a mutation).
2. **What to expect — PR1:** the "Norm" value in the header stat block and the gray dashed line's shape
   should now move meaningfully within the 30-day window's timescale, not sit flat near 0-2% for months
   after a regime change. Cross-check: Norm's current value should closely track (ideally exactly match,
   modulo rounding) the midpoint you'd compute by eye between the Over-extended line and the actual
   participation line's recent baseline.
3. **What to expect — PR2:** less dead space at the start of the visible window; the orange "over-extended"
   region should read as a boundary, not dominate the chart when today's reading is well below it; the
   header verdict sentence should be the first thing your eye lands on.
4. **Interaction:** load the page, no query params needed (default view); optionally try
   `?period=180` to confirm the fix holds across different display windows too.
5. **Acceptance criterion:** Pass = Norm responds on a sensible timescale; regime label
   (`Risk-on`/`Narrow — stand aside`/`Over-extended`) still computes correctly for all three cases; no
   console errors; mobile breakpoints (`max-width: 768px` / `480px`) still render correctly per the
   existing responsive CSS.

✅ Pre-flight Completeness: no execution unit requires reading a file/state not already captured in the
pre-flight above.
