# Perch Recurring-Themes Report — Methodology Runbook

> **Purpose:** Generate the 6-month recurring-themes report across the two Perch dashboards (large-spike breakout cards and large-dip cards), cross-referenced against market regime, with sector-level breakdown and a researched macro narrative. A governor should only need to say: *"Run the Perch recurring-themes report"* (optionally with a date range) and this runbook tells the instance exactly what to do.
> **Last validated:** 2026-08-26 (sector deep-dive edition)

---

## 1. Goal & inputs

Produce a PDF (and optionally Markdown) covering:
1. Both dashboard charts **as displayed** (spike chart + sell-off chart), reconstructed from the DB.
2. Top-30 lists: **large dips** (severity-filtered) and **large spikes** (frequency), over the requested window.
3. **Regime cross-reference:** large spikes surfaced during the **risk-on zone**; large dips surfaced during **macro-above-average** periods.
4. **Sector charts + sector totals** (spike-days and dip-days by sector, top symbols per sector).
5. **Web deep-dive** explaining *why* each leading sector behaved as it did (real macro/geopolitical events).

Default window: **2026-02-26 → last trading day before today** (6 months). Charts show the dashboard's 180-day lookback window ending at the last trading day.

## 2. Infrastructure & access (critical)

- **App:** `sentiment_importer` (Rails) = **Perch**, production at `perch.truesight.me`, deployed on host **`seni_ror`** (Rails) — SSH fleet label `seni_ror`.
- **DB:** PostgreSQL. Connection details in `/home/ubuntu/sentiment_importer/config/database.yml` under `production:` (host `44.193.55.205`, db `sentiment`, user `prod`). **Never print the password** — read it in-process from the yml (see §7).
- **DB auth is host-restricted:** the DB only accepts connections from the app host (`seni_ror`). The autopilot box cannot connect directly. → **All DB/query work runs on `seni_ror`** via `ruby -rpg -ryaml -rjson`.
- **Transfer:** the autopilot box has an SSH alias `seni-ror` (`~/.ssh/config`) — use `scp seni-ror:/tmp/<file> /tmp/<file>` to move computed payloads to the autopilot box for chart/PDF rendering.
- **Rails runner is unreliable on the box** (initializer boot failure) → use direct `PG.connect` from ruby, never `bundle exec rails runner`.

## 3. Universe (must match dashboards)

Qualified stocks = `companies` where:
- `sell_off_index = true`
- AND (`market_cap > 20000000000` OR `white_listed = true`)  — config `minimum_market_cap` = $20B
- AND `daily_price_std_dev != 0` (quality filter)
- AND `close >= 5` (price filter added by governor for this report)

## 4. Event definitions

**Large spike** (breakout card): close at/above the trailing high over the spike cutoff period — config `spike_cut_off_period = 20` (20 sessions). Matches `interesting_spike_symbols_query` in `app/models/concerns/etf_helper.rb`.

**Large dip** (dip card): close ≥ `dip_cut_off_perc = 10`% below the trailing 7-day high:
```sql
(close - max_close_7d) / max_close_7d * 100 < -10
-- where max_close_7d = MAX(close) OVER (PARTITION BY company_id ORDER BY date_published
--                                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```
> This is STRICTER than the live dashboard's 'any decline' predicate — the live `/large_dips` card is loose; the report uses the −10% severity filter to get meaningful names. (Governor's explicit spec; keep it.)

## 5. Regime definitions (from the code)

- **Spike index** = `LARGE_SPIKE_INDEX` company close ×100 (config `market_spike_symbol`). **Norm** on the spike chart = **30-day Bollinger middle** (`MacroIndicator.spike_bollinger_middle_over_period`). **Over-extended** = 30-day/3σ upper.
- **Sell-off index** = `LARGE_DIP_INDEX` close ×100 (config `market_sell_off_symbol`). **Average Level** on the sell-off chart = **180-day SMA** (`plot_sma_values(…, 180, …)`). Bands = 30-day/3σ Bollinger (green Over-Corrected / orange Over-Extended).
- **Risk-on day** = spike index **above its Norm** (30-day Bollinger middle) → the regime-gauge's "broad leadership, take the breakout cards" zone.
- **Macro-above-average day** = sell-off index **above its 180-day average**.
- **Bollinger deviation metric** = close-to-close delta (`price_deviation`), `standard_deviation` is the **sample** stddev (n−1) — see `config/initializers/enumerable.rb`; multiply ×3. Periods: `bollinger_period_days = 30`, `std_dev_exit_threshold_multiple = 3`.

## 6. Query plan (SQL shapes)

```sql
WITH qualified AS (
  SELECT c.id FROM companies c
  WHERE c.sell_off_index = true
    AND (c.market_cap > 20000000000 OR c.white_listed = true)
    AND c.daily_price_std_dev != 0
),
base AS (   -- PERFORMANCE: restrict to window start − 7 days, NOT full history
  SELECT dt.company_id, c.stock_symbol,
         dt.date_published::date AS trade_date, dt.close,
         MAX(dt.close) OVER (PARTITION BY dt.company_id ORDER BY dt.date_published
                             ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS max_close_7d
  FROM daily_trades dt
  JOIN qualified q ON q.id = dt.company_id
  JOIN companies c ON c.id = dt.company_id
  WHERE dt.close >= 5
    AND dt.date_published >= '<window_start> - 7 days'
)
SELECT stock_symbol, COUNT(*) AS dip_day_count,
       MIN(trade_date)::text AS first_seen, MAX(trade_date)::text AS last_seen,
       ROUND(AVG(pct_drop_7d)::numeric, 2) AS avg_pct_drop_7d
FROM (
  SELECT *, (close - max_close_7d) / max_close_7d * 100 AS pct_drop_7d
  FROM base
  WHERE max_close_7d > 0 AND (close - max_close_7d) / max_close_7d * 100 < -10
    AND trade_date BETWEEN '<window_start>' AND '<window_end>'
) dip_days
GROUP BY stock_symbol ORDER BY dip_day_count DESC, stock_symbol LIMIT 30;
```

Spike-side equivalent: same universe, predicate = close >= trailing 20-day high (`spike_cut_off_period = 20`), count qualifying days, top 30.

**Performance warning:** `daily_trades` is ~23.8M rows / 111 GB spanning 1971→today. NEVER window over full history — a full-history run takes 7+ min and must be killed. The trailing-7d/20d window only needs ~7 (or 20) days of lookback before the window start, so restrict `base` to `date_published >= '<window_start>' - INTERVAL '7 days'` (or 20 days for spikes).

## 7. How to execute on seni_ror (paste-ready pattern)

```bash
cd /home/ubuntu/sentiment_importer && ruby -rpg -ryaml -rjson -e '
cfg = YAML.load_file("config/database.yml")["production"]
conn = PG.connect(host: cfg["host"], port: cfg["port"], dbname: cfg["database"], user: cfg["username"], password: cfg["password"])
# ... run queries, write results to /tmp/*.json (JSON.generate) ...
'
```

Read config in-process so the password never appears in tool output/logs.

## 8. Sector mapping

- `companies.sector_id` → `sectors.name` (LEFT JOIN; `COALESCE(s.name,'Unknown')`).
- Sector table has noise: blank names (id 4, 8), duplicates (Healthcare vs Health Care, Finance vs Financial Services), one junk name (id 25 = pillar-score text). Normalize to the canonical GICS-ish buckets for the report: Technology, Financial Services, Consumer Cyclical, Industrials, Healthcare, Consumer Defensive, Energy, Communication Services, Utilities, Real Estate, Basic Materials, Services.
- **"Unknown" bucket** = synthetic indices/ETFs without a sector tag (e.g. FIG, SQQQ, TQQQ, CRWV, DOCN, APLD, NET). Flag this in the report rather than dropping them.
- Compute sector spike/dip **day counts** by joining event lists (from §6 queries) to the symbol→sector map, filtered to regime days (§5). Also emit per-sector daily time series for the sector panel charts.

## 9. Chart reconstruction (faithful to live dashboards)

Live pages are behind login — reconstruct the charts from the same series the Chart.js renders:
- **Spike chart** (dark line on white): index ×100; Norm = 30-day Bollinger middle (dashed grey); green "GO zone" fill between index and Norm when above; orange "Over-extended" upper band. Title: "Market Breakout Participation".
- **Sell-off chart** (blue line): index ×100; "Average Level" = 180-day SMA (grey dashed); green lower band ("Over-Corrected") and orange upper band ("Over-Extended") = 30-day 3σ Bollinger. Title: "US Stock Market Correction Level".
- Shade the **risk-on** days (spike index > Norm) and **macro-above-average** days (sell-off index > 180-day SMA) on the respective charts.
- 180-day window (`DEFAULT_PERIOD = 180`), x-axis = trading days.
- **Tooling:** on the autopilot box — `matplotlib` (Agg backend), `reportlab`, `psycopg2`. Render charts as PNGs with matplotlib; assemble PDF with reportlab (Saffron-Monk-ish brand: header #7a4a1d, zebra tables #faf5ee/#d8c3a5).

## 10. Sector charts

- Two 3×2 subplot grids (matplotlib): (a) daily spike-day counts by sector during risk-on days — top 6 sectors; (b) daily dip-day counts by sector during macro-above days — top 6 sectors. Per-sector colored line + light fill, dates on x-axis.

## 11. Web deep-dive

After computing sector totals, run web searches for each leading sector to explain the moves (e.g. `web_search` on: semiconductor selloff AI infrastructure 2026; bank stocks breakout 2026; refiner crack spread rally; consumer discretionary weakness travel; hawkish Fed rotation). Synthesize into short per-sector narratives tied to the observed numbers (e.g. "MU 22 dip-days ← SK Hynix HBM slowdown + AI-capex digestion"). Always pair the researched 'why' with the DB 'what'.

## 12. PDF structure (reportlab)

1. Cover: title + window + regime summary (risk-on day count /180, macro-above-avg day count /180).
2. Both dashboard charts (reconstructed).
3. Sector chart panels (spike + dip).
4. Sector totals tables (Sector | Days | First | Last | Top symbols).
5. Deep-dive narratives per sector + macro backdrop.
6. Reference tables: top-30 dips (Symbol | Dip days | First | Last | Avg drop 7d %) and top-30 spikes during risk-on (Symbol | Spike days | First | Last).
7. Send via `send_telegram_attachment`.

## 13. Known gotchas

- Rails runner on seni_ror fails to boot → always direct `PG.connect`.
- DB password never printed — read from yml in-process.
- Full-history window scans time out → always date-restrict (§6).
- `max_close_7d` window includes the current row (`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`) — a qualifying day is close >10% below the best close of the trailing 7 sessions.
- `avg_pct_drop_7d` should be the mean of per-day pct drops, rounded 2dp.
- Last trading day may be < requested end date (weekend/holiday) — report actual max date.
- Sector table noise (duplicates/junk names) → normalize (§8).
- No credentials or secrets in this runbook — DB access is via config/database.yml on the host.

## 14. Deliverables & handoff

- PDF via `send_telegram_attachment` into the requesting thread.
- Optionally upload the PDF to a reports folder (e.g. `market_research` or Gary's personal `garyjob/perch-market-analysis` — only if the governor explicitly asks; see `PERSONAL_CONTRIBUTOR_BACKLOGS.md`).
- Report is read-only against the DB — no writes, no ledger events.
