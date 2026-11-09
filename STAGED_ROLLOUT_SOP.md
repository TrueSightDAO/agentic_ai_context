# Staged Rollout SOP — curated subset → visual UAT → full rollout

> **Status:** active default pattern (codified 2026-11-07, from the SGX rollout in `sentiment_importer`).
> **Applies to:** any change that introduces a *new class of data* or a *new surface* into a live
> product — a new exchange, a new country, a new partner tier, a new product line, a new feed.
> **Governor's instruction that produced this:** *"Do A and then visual UAT and then B … perhaps
> write this down as an SOP and follow this pattern in the future."*

---

## 1. The pattern

Never bulk-enable a new data class. Ship it in three gates, in this order:

| Gate | What happens | Exit criterion |
|---|---|---|
| **A — Curated subset** | Ingest/flag a *small, high-quality* slice (tens, chosen by a real signal such as liquidity or revenue — never the first N rows by id). | Subset is in the DB, indicators/derived fields compute, non-destructive to existing data. |
| **UAT — Visual acceptance** | Execute the **actual render path** a user hits, and confirm the new data appears with correct values. | New rows are visibly present in the live surface, values spot-check against an independent source. |
| **B — Full rollout** | Enable the remainder. | Full set enabled; blast radius verified (existing classes unchanged). |

Only after UAT passes does B run. **A failing UAT blocks B** — it is not a formality to click past.

---

## 2. Non-negotiable rules learned the hard way

These are not theoretical. Each one cost real time in the SGX rollout.

### 2.1 Never say "it will appear automatically" without timing the render path

I reported *"SGX tickers are live ✅ — the feed reads the DB, so no further change needed"* while the
cache happened to be empty. The feed's query was a `ROW_NUMBER() OVER (PARTITION BY company_id)`
window function over a **111 GB / 24M-row** table that **could not complete in 120 seconds**.

> **Rule:** before claiming data is visible, execute the exact code path the user hits and record
> the wall-clock time. "The table has the rows" is not evidence that the page renders.

### 2.2 `EXPLAIN` hot read paths against *production* row counts first

A query that is instant on a dev subset can be unusable at production scale. Get the plan and the
row estimate before you touch the data that activates it.

> **Rule:** for any read path your change newly activates, run `EXPLAIN` on production (or a
> production-sized replica) and confirm no `Seq Scan` over a table you just made larger.

### 2.3 Fresh `ANALYZE` cannot rescue a bad algorithm

`daily_trades` had **never** been analyzed. I ran `ANALYZE` (32s) expecting the 9-minute query to
speed up. It did not — the plan was already correct; sorting 24M rows is the algorithm.

> **Rule:** if the plan is a full sort/window over the whole table, statistics are irrelevant.
> Rewrite the query. `DISTINCT ON` does **not** help either — Postgres has no skip-scan.
> `JOIN LATERAL … ORDER BY … LIMIT 1` per parent row is the escape hatch when a suitable index exists.

### 2.4 Know WHICH cache store you are invalidating

Development used `localhost:6379`; production used `mem_cache_store` on a different Redis host.
My "successful" cache warm in development changed **nothing** — the production key stayed absent,
so every production render started a rebuild that could never finish.

> **Rule:** before warming or clearing a cache, print the store class and address **in the target
> environment**, and confirm the key state (`EXISTS`) on that exact instance.

### 2.5 Cron jobs must never invalidate an expensive cache

`SgxPriceRefresher#perform` ended with an unconditional `Rails.cache.delete("daily_trades/latest")`.
Fine when rebuild is milliseconds; catastrophic when it is minutes, because the *next user request*
pays the cost and the pool saturates.

> **Rule:** a scheduled job may only invalidate keys whose rebuild is cheap. For expensive keys,
> let the TTL expire on its own (bounded, gradual) and add the key to a `NEVER_CLEAR_KEYS` guard.

### 2.6 Verify the blast radius explicitly, not implicitly

Bulk `UPDATE … WHERE exchange = 'sgx'` is only safe if you prove the other classes did not move.
After flagging 535 SGX rows I checked `us_white_listed=566` and `all=1139` and reconciled the
arithmetic, rather than assuming the WHERE clause held.

> **Rule:** after a bulk write, re-count each *unaffected* class and show the arithmetic reconciles.

### 2.7 "UAT failed" must be diagnosed before it is reported as a product defect

My first `visual_uat` call returned `verdict: fail` because **my expectation was wrong** — I asserted
on a `<table>` in a page that serves raw XML. The product was fine. Equally, an early `401` looked
like an auth problem but was bot-manager UA banning (`curl` is a banned UA; a browser UA passes).

> **Rule:** when a check fails, separate *the assertion* from *the system*. Read the DOM facts / the
> response body before concluding the feature is broken — and say which one you verified.

---

## 3. Checklist

### Gate A — curated subset
- [ ] Choose the subset by a **real quality signal** (liquidity, revenue, recency), not `LIMIT n`.
- [ ] Ingest with the **idempotent update path**, so re-running fixes rather than duplicates.
- [ ] Confirm derived fields compute (indicators, rollups) on the subset.
- [ ] Confirm no other data class changed (counts before/after).

### Gate UAT — visual acceptance
- [ ] Resolve auth **and** bot-UA gating; know which one you hit.
- [ ] Execute the real render path; measure wall-clock time.
- [ ] Confirm new rows present *and* spot-check values against an independent source.
- [ ] Reconcile the count: total = existing + new.
- [ ] Diagnose any `fail` before reporting it as a defect (§2.7).

### Gate B — full rollout
- [ ] Only after UAT passes.
- [ ] Bulk-enable via one scoped `WHERE`, in a transaction.
- [ ] Verify unaffected classes unchanged (§2.6).
- [ ] Confirm the render path still performs at the new cardinality.

---

## 4. When NOT to use this

- **Pure read-only/derived** changes (a new column on an existing dashboard) — no new class, no gate.
- **Pure code fixes** — ship via PR + tests.
- **Anything reversible and cheap** — the gates exist to bound blast radius; if there is none, skip.

---

## 5. Reference case: SGX rollout (`sentiment_importer`, 2026-11-06/07)

| Item | Outcome |
|---|---|
| Ingest | PR #1144 — SGX board snapshot + Yahoo `.SI` backfill; `D05.SI` keying avoids US-ticker collision; 565 companies, 563 priced |
| Currency bug | Migration defaulted every SGX row to `USD`; the code was right but the rows predated the column — re-running ingest fixed it → 565/565 SGD |
| Gate A | 30 liquid names by traded value, 365 days of history, `white_listed = true` |
| Gate UAT | 563 `.SI` tickers rendered; DBS 69.72, UOB 36.88, OCBC 27.73, Singtel 4.09 |
| Regression I caused | `SgxPriceRefresher` cleared an expensive cache → fixed in PR #1146 (`NEVER_CLEAR_KEYS` guard) |
| Performance | `latest_closes` window fn (>120s) → `JOIN LATERAL` (0.6s warm / 18s cold) in PR #1147 |
| Gate B | Remaining 535 flagged; 565/565, US unchanged at 566 |
| Still open | Durable summary table so `latest_closes` is never computed on request — filed in `OPEN_FOLLOWUPS.md` |
