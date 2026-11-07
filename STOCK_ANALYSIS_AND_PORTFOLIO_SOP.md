# Stock Market Analysis & Portfolio Management SOP

> **Purpose:** The standard method for analysing stock screens, reviewing a portfolio, and
> forming position recommendations. Codified 2026-11-07 from the `perch.truesight.me/large_dips`
> deep-dive, after the governor caught two avoidable errors in the first pass:
> (1) treating a macro-wide selloff as 75 individual "dips", and
> (2) recommending a portfolio-fit name (LMT) without checking its Bollinger position.
>
> **Scope:** Gary's personal portfolio work and Perch analysis. This is analytical support,
> NOT investment advice, and NOT a mandate to trade.
>
> **Applies to:** Sophia (autopilot), Envoy (tmux Claude on `nelanco-claude`), and any agent
> asked to "look at the dips", "review my positions", or "what should I buy".

---

## 1. When this SOP fires

| Trigger | Path |
|---|---|
| "Examine the companies on `<perch screen>`" | Full pipeline §3 → §8 |
| "Here are my positions — what should I add?" | Skip to §6 (portfolio-fit layer first) |
| "Is X a buy?" | §4 metrics + §5 filter, single name |
| "How is my portfolio doing?" | §6 only |
| Morning/periodic review | §3 + §4 |

**Hard rule:** run §6 (portfolio-fit) BEFORE §5 (shortlist ranking) whenever the governor has
positions. A stock can be the best name on a screen and still be the wrong *addition*.

---

## 2. Data acquisition — never scrape the dashboard

Perch subpages are **login-gated** (`https://perch.truesight.me/large_dips` redirects to
`/users/sign_in`). Do not scrape. Pull from the production database using the application's own
query helpers so the population is **identical to what the dashboard renders**.

**Host:** `sing `ssh_run` (host='seni_ror', ...)` — the Rails box for `sentiment_importer` (Nelanco).
`seni_ror` is the **trading platform only**, not the DAO API.

**Canonical pattern:**

```bash
cd /home/ubuntu/sentiment_importer && \
export PATH="$HOME/.rbenv/bin:$HOME/.rbenv/shims:$PATH" && \
cat > /tmp/q.rb <<'EOF'
require File.expand_path("config/environment", "/home/ubuntu/sentiment_importer")
d  = DailyTrade.most_recent_us_market_trading_date(true)
q  = ApplicationController.helpers.interesting_stock_symbols_query(d)
rows = ActiveRecord::Base.connection.execute(q).to_a
puts rows.to_json
EOF
timeout 240 bundle exec ruby /tmp/q.rb 2>&1 | tail -5
```

Ruby here is **2.6.5** — no `filter_map`, no endless methods, no `Hash#except`.

### `daily_trades` — real column names (do not guess)

`close`, `high`, `low`, `volume`, `date_published`, `rsi` (**not** `latest_rsi`), `macd`,
`macd_signal`, `sma_5`, `sma_20`, `sma_30`, `sma_100`, `sma_200`, `price_stddev`,
`volume_sma_90`, `over_sold`, `over_bought`, `large_dip`, `large_spike`, `is_surge`,
`gain_loss`, `buy_now`, `sell_now`.

There is **no** `bollinger_*` column — compute %B yourself from `sma_20` + `price_stddev`,
but verify against a fresh rolling window (see §4).

### Other useful entry points

- `app/models/concerns/etf_helper.rb` → `interesting_stock_symbols_query`, `general_filter_condition`,
  `LARGE_DIP_CACHE_EXPIRY` (24 h).
- `config.dip_cut_off_perc = 10` — the screen's dip threshold.
- `app/views/api/large_dips/index.json.jbuilder` — the JSON shape the dashboard consumes.

**Always persist the raw pull to a file on the host** (e.g. `/tmp/large_dips.json`). A chat turn is
bounded; an unpinned result is lost at the turn boundary and the whole pull has to be redone.

---

## 3. Step 1 — Universe and macro context

1. Pull the screen population (§2) with its trading date.
2. **Establish the macro backdrop for that date before analysing any single name.** Search the
   market wrap for the session(s) the screen covers.
3. Compute the **median move across the whole screen**. This is the single most important number
   in the exercise — see §5.

> **Rule:** a dip screen fired on the day of a market-wide shock produces almost no signal.
> The value is in the **dispersion**, never the raw list.

---

## 4. Step 2 — The five mandatory metrics per symbol

Never report a name without all five. Order matters: momentum alone is misleading.

| # | Metric | Definition | Why it's mandatory |
|---|---|---|---|
| 1 | **1-year return** | last close vs. close on/after D−365 | Separates "dip in an uptrend" from "staircase down" |
| 2 | **% off 52-week high** | last / max(adj close, 52w) − 1 | Drawdown magnitude, split-adjusted |
| 3 | **vs 200-day MA** | last / SMA200 − 1 | Primary trend. Above = uptrend intact |
| 4 | **7-day move** | the screen's own trigger | Compare against the median (§5) |
| 5 | **Bollinger %B** | `(P − lower) / (upper − lower)`, 20d, 2σ | **Where in the channel** it sits today |

**%B interpretation:** `<0` = below lower band (washout) · `0–0.2` = lower fifth ·
`0.5` = mid-channel · `>0.5` = upper half. RSI alone is NOT a dip measure — a name can have
RSI 55 and sit mid-channel while a name with RSI 50 sits on its lower band.

**Compute %B from a rolling window, not only from stored `sma_20`/`price_stddev`.** Populate
`date_published, close, rsi` and compute SMA20 + population σ in Ruby; that field takes no
parameters, but recompute so the window is explicit and split-repaired:

```ruby
w   = adj.last(20).map { |x| x[:cl] }
sma = w.sum / w.size
sd  = Math.sqrt(w.map { |v| (v - sma)**2 }.sum / w.size)
lb  = sma - 2*sd ; ub = sma + 2*sd
pb  = (ub - lb) > 0 ? (last - lb) / (ub - lb) : 0.5
```

### Split repair (unavoidable — see §9)

Walk the series forward; if a single-session absolute move exceeds **28%**, treat it as a split
factor and rescale all prior closes. Mark any row where this fired with `*` and say so — a genuine
+30% earnings gap is indistinguishable from a split without a split calendar.

---

## 5. Step 3 — The beta-vs-signal test (do not skip)

This is the correction that matters most. Compute the median 7-day move across the screen, then:

- **|name's 7d move − median| < 5pp** → **beta**. The name fell because the market fell. Not a dip.
  Do not write a paragraph about it. Do not put it in a shortlist.
- **|name's 7d move − median| ≥ 5pp** → **candidate idiosyncratic event**. Research the cause.

Also flag any sector that is a net **beneficiary** of the rotation — a name up 60% on the year and
down 12% in a week is a *victim of rotation into it*, not a dip.

> **The 2026-11-06 example:** 75 names, median 7d ≈ −13%, because the S&P fell −4.36% and the
> Nasdaq −5.52% in one session on the midterm result. ~60 of 75 were pure beta. Only ~10 carried
> company-specific information. Writing up 75 names individually would have been 87% noise.

---

## 6. Step 4 — Portfolio-fit layer (run this before ranking anything)

**Never recommend an addition on single-name merit alone.** Sequence:

1. **Get the actual positions.** If the governor attaches a screenshot, OCR it and confirm the
tickers back before analysing (`ocr_image` → read the text → sanity-check against the DB).
2. **Pull each holding's metrics** from the same pipeline (§4) — 1y, off-high, vs200, RSI, %B.
3. **Factor-cluster them.** Group holdings by the *driver*, not the sector label. Ask: how many
   distinct macro factors does this book actually express?
4. **Test the candidate against the book:** does it add a factor the book lacks, or a fourth slice
   of the same bet? Check beta and end-market exposure explicitly.
5. **Only then** consult the screen ranking.

> **The 2026-11-06 example:** the book was APLD (−50%), ORCL (−52.8%), INTU (−47.7%), PLAY (−40.9%).
> All four down 41–53% in 12 months; three of four were the **same AI-capex factor** — APLD and ORCL
> as leveraged beneficiaries, INTU as the AI-disruption victim. The top-ranked name on the screen
> (MU) was a memory-cycle play on that identical factor. Recommending it would have been a
> four-position bet on one variable. The screen ranking and the portfolio answer **diverged**, and the
> portfolio answer wins.

**Position sizing vocabulary:**
- *Upside engine* — highest expected return, accepts full factor correlation.
- *Hedge / insurance* — low beta, negatively-correlated regime exposure, accepts lower return
  (e.g. LMT, beta 0.10, pays a dividend while it waits).
- Say explicitly which role the recommendation plays. "Add X" without a role is not a recommendation.

**Honesty requirement:** if the correct answer is "don't add a fifth — deploy into what I already
hold," say that. A fifth ticker often buys the *illusion* of diversification.

---

## 7. Step 5 — The three-question filter per candidate

For each name that survives §5, answer all three in writing:

1. **Is the business broken, or is the price broken?** Revenue growth, margin trend, guidance
   revisions. A −45% drawdown with revenue +8% and EPS +57% is a price event. A −56% drawdown with
   two consecutive revenue misses and a CEO+CFO exit is a business event. (Real examples: LMT vs. TRIP.)
2. **Is the fall idiosyncratic or structural?** Reference the trigger: guidance cut, earnings miss,
   C-suite exit, litigation, rate shock, sector rotation.
3. **Is the cycle at peak or trough?** For cyclicals this is the whole thesis. A refiner at
   $39/bbl crack vs. a $14/bbl mid-cycle assumption is at peak earnings — down 13% is a warning,
   not a discount. Always state where in the cycle you think you are.

---

## 8. Step 6 — Mandatory caveats (non-negotiable)

Every written output must carry:

- **The bear case**, plainly. Not a token "risks include" line — the actual strongest argument
  against the recommendation.
- **What would change the call** — a specific, observable trigger per name (a print, a price level,
  a guidance revision).
- **Where the price sits in its channel** — if recommending a dip entry, state %B and the lower-band
  price. If the name is mid-channel, **say it is not a dip entry** and give a limit level instead.
- **"Not financial advice"** and the open questions the screen cannot answer.
- **No price targets invented by the agent.** Attribute sell-side targets to the firm
  ("Susquehanna $660"); never present your own number as a target.
- **Valuation is not the only axis** — a low multiple at peak cycle is expensive; a full multiple on
  a working uptrend may be fair.

---

## 9. Known data-quality traps in Perch (check every time)

These degrade every screen and must be disclosed, not silently absorbed:

| Trap | How to detect | Handling |
|---|---|---|
| **Corrupted price series** | single-session move >100% (e.g. AMTD **+5,624%** on 2026-10-19; STI **+301%**) | Discard any 1y return for that symbol; flag it |
| **Dead / mismapped tickers** | STI = SunTrust (dead 2019), S labelled "Sprint Corp" (dead 2020), AMTD labelled "TD Ameritrade" (dead 2020), FIG labelled an ETF while being Figma's ticker | Quarantine; they recycle into every screen forever |
| **`sector_name` NULL** | `companies.sector_id → sectors.name` LEFT JOIN with no match (~6 tickers on 2026-11-06) | Breaks sector colour-coding and any rotation read; report the count |
| **`market_cap` NULL/0** | nearly every row on 2026-11-06 | The liquidity filter is NOT actually filtering — do not claim it does |
| **Leveraged ETFs in the set** | `TQQQ` (3×), any inverse product | Its "dip" is arithmetic, not a valuation event — exclude by default |
| **No split calendar** | 18 of 75 names needed heuristic repair | Heuristic only; mark repaired rows `*` and tell the governor |
| **Stale caches** | `LARGE_DIP_CACHE_EXPIRY = 24.hours` | Confirm the trading date; never assume "today" |

**Fix direction (small PRs to `sentiment_importer`):** `stock_splits` reference table + adjust on
ingest; sector backfill + NOT-NULL guard on new `companies` rows; `is_leveraged` flag excluded from
`interesting_stock_symbols_query`; delisted-ticker quarantine; market-cap backfill; a sanity assertion
rejecting single-session moves >100%.

---

## 10. Report structure (PDF)

Use `generate_pdf` (Saffron Monk styling), then deliver the file itself with
`send_telegram_attachment` — governors are often behind firewalls that block GitHub links.

### 10.0 The acceptance test — run it before you send

The report exists to make a decision obvious. Test it as a **reader**, not as its author:

1. **The 1-page test** — can someone who never saw the screen name the 3 best and 3 worst candidates
   from page 1 alone? If not, the report fails, regardless of analysis quality.
2. **The 3-page test** — by page 3, does the reader know their specific next action (which name, what
   price, what event to wait for)? If they are still reading tables, it fails.
3. **The glaze test** — is any page a wall of numbers with no verdict attached? Cut, compress, or move
   it to the appendix.
4. **The "so what" test** — every table is immediately followed by the one sentence saying what it
   means and what to do about it. A table without a verdict line is a data dump.

**Length budget: 4 pages of body + unlimited appendix.** If the body overflows 4 pages, the analysis
is being dumped, not communicated. The full universe table is *always* appendix.

> **Why this section exists.** v1 of the `/large_dips` report was a 13-page analyst's lab notebook:
> the universe table on page 4, the actual verdicts on page 9. Feedback from a trader with 6 years
> and 1,000+ executions: *"I read the PDF and my eyes just glazed over it. I stopped reading 3 pages
> in."* Every structure rule below follows from that correction. The analysis was not wrong — the
> **ordering** was. **A report is not a container for analysis; it is a decision aid.**

### 10.1 Page 1 — the verdict page (all of it)

Page 1 must be self-sufficient. Nothing on it may require page 2.

- **Verdict line** — one sentence: is this screen telling us anything, or is it macro noise? (§5)
- **The call** — at most **5 names**, as ranked *cards*, not rows. Each card carries exactly:
  `TICKER · one-line why · role (upside engine / hedge / avoid) · entry zone · invalidation · %B`.
- **The avoid list** — at most 5 names, one line each, with the *category* of failure: broken business
  vs. peak cycle vs. systematic de-rating vs. beta.
- **"Everything else is beta"** — one line giving the count dismissed and why. This is the single most
  important sentence in the document and it belongs on page 1.
- **Portfolio overlay** (when the governor has positions) — the factor clustering from §6: "your book
  is N bets, not M positions", plus where the recommendation fits against it.

### 10.2 Pages 2–3 — the shortlist in detail

One block per shortlisted name (the first ~5 only). Per name, in this order and no other:

1. **What happened** — 2 sentences: the trigger.
2. **Why it's interesting** — 3 bullets maximum, each a fact carrying a number.
3. **Where the price is** — %B, lower-band price, and an explicit **entry zone** and **invalidation
   level**. Numbers a trader can put straight into an order ticket.
4. **What would change the call** — one specific observable: a print date, a price, a guidance revision.
5. **The bear case** — the strongest argument against, stated plainly.

### 10.3 Page 4 — the decision summary

- **Action table**: `Ticker | Role | Action | Entry zone | Invalidation | Trigger event | Confidence`.
  One row per shortlisted name. This is the page a trader screenshots.
- **Macro backdrop**, compressed to ≤4 dated bullets — context, not a section.
- **What this screen cannot answer** — ≤3 bullets.

### 10.4 Appendix — supporting data (not body)

Everything below the fold, explicitly labelled "Appendix — supporting data".

- **A1. Full universe table** — every name, the five metrics from §4, and the stated composite weights
  (e.g. 40% 1y / 30% off-high / 30% vs200dma — call it a *resilience* rank, never a cheapness rank).
  **Every row also carries a verdict token in the first column:** `WATCH` / `HOLD-OFF` / `AVOID` /
  `BETA-IGNORE`. No row ships without a token — a bare number row is unreadable at a glance.
- **A2. Dispersion table** — only names that beat the median filter, with the excess move.
- **A3. Data-quality findings** — the §9 evidence: corrupted series, dead tickers, NULL sectors.
- **A4. Methodology** — algorithms, windows, split-repair logic, so every number is reproducible.

### 10.5 Formatting rules that prevent glaze

- **No table wider than 6 columns**; no table longer than ~20 rows in the body. Wide or long tables
  are appendix-only.
- **Every table gets a verdict line underneath** — the "so what" sentence.
- **Verdict tokens go in the first column, never the last.** Readers scan left to right and stop.
- **Bold only the number that drives the decision** in a row — not every number.
- **No analyst hedging in the body.** Caveats, uncertainty and data-quality live in the appendix,
  compressed. If a caveat genuinely changes the recommendation, it belongs *inside that name's card*,
  not on a disclaimer page.
- **State the role of every recommendation** (upside engine / hedge). "Add X" without a role is not a
  recommendation.
- **A longer document is not a more thorough one.** Thoroughness lives in the appendix and in the
  per-name research; it must never inflate the body.

---

## 11. Self-improvement hooks

When a governor corrects an analysis, that correction is training data. Convert it into a change:

| Correction pattern | Codify as |
|---|---|
| "Doesn't look like it's at the lower band" | §4 metric #5 — %B is mandatory, not optional |
| "That's not a dip, that's the market" | §5 beta-vs-signal test |
| "But I already own that factor" | §6 portfolio-fit-first sequencing |
| "Why this one over X?" | §7 three-question filter, plus the bear case |
| A tool/field error (`latest_rsi`) | Add the real column name to §2 immediately |
| "My eyes glazed over / I stopped 3 pages in" | §10 restructure: verdict on page 1, data to appendix, verdict token per row, 4-page body cap |
| "Can you even see what to invest or not?" | §10.0 acceptance test — every output must name ≤5 actions and an avoid list explicitly |

**Third-party reader feedback is first-class training data.** A trader who abandoned the document on
page 3 is a stronger signal than a governor who read all 13 pages — the governor knows the context and
will forgive structure a stranger cannot. When feedback arrives from someone other than a governor
(trader, partner, prospective user), relay it through the governor but record it here with the same
weight. The question to ask of any report: **would a busy stranger act on this, or put it down?**

Propose SOP amendments via a PR to `agentic_ai_context`. Keep one improvement per PR.

---

## 12. Related documents

- `PERCH_RECURRING_THEMES_REPORT.md` — methodology runbook for the 6-month recurring-themes report
  (the cross-screen crosstab). This SOP covers single-screen deep dives; that one covers recurrence.
- `plans/SCHWAB_PORTFOLIO_INTEGRATION_PLAN.md` — read-only Schwab account link so live positions can
  be pulled instead of OCR'd from a screenshot.
- `ENVOY_TMUX_SESSIONS.md` — Envoy's seat also works `sentiment_importer` (Perch) and portfolio work.
  Hand off via `send_handoff(target_agent='bionpact')` if the work moves to that box.
