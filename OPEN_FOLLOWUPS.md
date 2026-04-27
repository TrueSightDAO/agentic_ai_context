# Open follow-ups (cross-session backlog)

Short list of **scoped follow-up tasks** future AI agents (Claude / Cursor /
Codex / Kimi / etc.) and humans can pick up between sessions. The bar is:

- One thing that didn't ship in the original PR but logically belongs after it.
- Small enough to fit in a single session (rough cap: ~60 min of focused work).
- Self-contained — the entry has enough context that someone who didn't write
  the original code can act on it without reverse-engineering history.

This file is **not** a replacement for `CONTEXT_UPDATES.md` (which is the
append-only event log) or for project-specific TODOs that live next to the
code (e.g. `# TODO:` comments, `dapp/UX_CONVENTIONS.md`, repo READMEs, or the
"Q5 parked" pattern inside individual proposal docs like
`PARTNER_VELOCITY_PROPOSAL.md`). It is the place for **cross-repo /
cross-session** items that would otherwise rot in chat transcripts.

## Workflow for agents picking up an entry

1. Read the entry. If the **Blocker** still applies, leave it alone.
2. If you're going to ship it, claim it informally by appending a line to
   `CONTEXT_UPDATES.md` (`<agent-id> | starting OPEN_FOLLOWUPS#…`) so parallel
   sessions don't duplicate work.
3. Open a PR. When merged, **move** the entry to the bottom of this file
   under `## Recently shipped` with the PR link, and append a one-line entry
   to `CONTEXT_UPDATES.md`. Keep the **Pending** list short.
4. If the entry is no longer relevant (priorities shifted, blocker permanent,
   etc.), move it to `## Closed without shipping` with a one-line reason.
   Don't silently delete history.

---

## Pending

### Eyeball-check `partners-velocity.json` numbers after 4 weekly refreshes

**Context.** First version of `sync_partners_velocity.py` shipped via
[go_to_market#80][velocity-pr] and the first JSON snapshot via
[agroverse-inventory#5][velocity-snap]. Refresh cadence is weekly. Per
Gary's §9 Q5 decision in `PARTNER_VELOCITY_PROPOSAL.md` ("wait till
settle"), no downstream consumer should *trust* the numbers until at
least **4 successful weekly refreshes** have run and a manual sanity
check has confirmed the values track operator intuition for 3–5 known
partners (Go Ask Alice, Lumin Earth, Edge & Node, Kiki's Cocoa).

**Outcome.** Either flip the green-light (wire dormant / high-velocity
signals into warm-up generator — see next entry), or file a defect on
the script if the numbers feel wrong.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read the latest committed snapshot.
- `market_research/scripts/sync_partners_velocity.py` — re-run locally if needed.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §9 Q5 (acceptance criterion).

**Blocker / signal to revisit.** Wait for ≥4 entries on the GitHub
Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible
acceptance check: **2026-05-25** (~4 weeks after first snapshot).

**Owner.** Gary (manual sanity check), then any agent for downstream wiring.

[velocity-pr]: https://github.com/TrueSightDAO/go_to_market/pull/80
[velocity-snap]: https://github.com/TrueSightDAO/agroverse-inventory/pull/5

---

### Wire dormant / high-velocity signals into warm-up draft generator

**Context.** Once `partners-velocity.json` numbers are trusted (see
previous entry), the warm-up draft generator
(`market_research/scripts/suggest_warmup_prospect_drafts.py`) and any
sibling check-in flow can read per-partner activity to:

- **Dormant retailer** (`last_sale_date > 90 days ago` and
  `last_restock_date > 90 days ago`) → trigger a check-in email
  instead of a generic warmup, or de-prioritize warmups for them.
- **High-velocity retailer** (per-SKU `*_12m_monthly_avg >
  category_medians[sku].monthly × N`) → flag as a candidate for
  case-study / testimonial / shelf-photo capture for `/wholesale/`.
- **Cold-start / newly-onboarded retailer**
  (`max(sample_size_*) < 3`) → no recommendation; default to
  category baseline.

**Outcome.** Tighter outreach prioritization without manual triage; a
small CSV-style "this week's flags" surface (sheet or Markdown) for
operator review.

**Files.**
- `market_research/scripts/suggest_warmup_prospect_drafts.py` —
  primary integration point.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic.
- `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` — tighten the
  status-transition rules once the signals exist.

**Blocker.** Previous entry (eyeball-check) must complete green.

**Owner.** Unclaimed.

---

### Advisory ops-health v2: burn rate + days-of-cover at SF

**Context.** Ops-health v1 ([TrueSightDAO/go_to_market#77][pr77] +
[follow-up #78][pr78]) ships per-shipper stock from
`treasury-cache/dao_offchain_treasury.json`, cash float from `off chain asset
balance`, and in-transit freight from `Shipment Ledger Listing`. Burn rate /
days-of-cover at SF (Kirsten) was deliberately deferred — the structured
snapshot at `ecosystem_change_logs/ops_health/current.json` already reserves
two `null` slots: **`sales_velocity_30d`** and **`days_of_cover_at_sf`**.

**Outcome.** When v2 lands, the daily oracle / a future
`dapp/supply_health.html` page can flag a SKU with **🟢 ≥4 weeks cover · 🟡
2–4 weeks · 🔴 <2 weeks** at Kirsten — exactly the signal Gary is missing
today (*"Kirsten goes low before Matheus's freight inbound has arrived"*).

**Files / shape.**
- `market_research/scripts/generate_advisory_snapshot.py` →
  `_compute_ops_health(...)` returns the structured dict; add a peer
  `_compute_burn_rate_and_cover(treasury, qr_sales_rows)` that populates the
  two reserved slots and surface a few `🟢/🟡/🔴` lines in
  `_render_ops_health_markdown`.
- `QR Code Sales` window already loaded by `_fetch_sheet_sales_markdown` when
  `--with-sheet-sales` is on — pass the parsed rows through instead of
  re-reading.

**Join key.** Today the join between sales (per Currency string) and stock
(per `inventory_type` × `unit_format`) is brittle because **`inventory_type`
is only populated on ~28% of `dao_offchain_treasury.json` items as of
2026-04-27** (column added 2026-04-26; backfill in progress). Two paths:

1. **Conservative:** join on the raw `Currency` string (works today, exact
   match per batch — granular but noisy).
2. **Cleaner (preferred when ready):** join on `inventory_type` × `unit_format`
   once the backfill is meaningful (~>80% populated). Surface the same flag
   one level higher.

**Blocker / signal to revisit.** Check `inventory_type` sparseness on
`dao_offchain_treasury.json` before starting:

```bash
curl -sL https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/dao_offchain_treasury.json \
  | python3 -c '
import json, sys
d = json.load(sys.stdin)
items = [it for m in d.get("managers", []) for it in m.get("items", [])]
populated = sum(1 for it in items if (it.get("inventory_type") or "").strip())
print(f"{populated}/{len(items)} = {100*populated/len(items):.0f}% populated")
'
```

If <40%, do path (1) only. If >80%, go straight to path (2). In between, ship
path (1) and re-roll-up by `inventory_type` for the markdown summary.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks after v1
shipped, gives the backfill room).

[pr77]: https://github.com/TrueSightDAO/go_to_market/pull/77
[pr78]: https://github.com/TrueSightDAO/go_to_market/pull/78

---

### `two_bahia_bars` newsletter — post-send open / click / reply read-out

**Context.** First Agroverse newsletter to ship with the full pipeline ([buyer
exclusion][n-pr79], [JPG fallback + tighter image margins][n-pr84],
[side-by-side comparison row][n-pr85]) sent 2026-04-27 to **38 recipients**
(2 past-buyers excluded via `--exclude-buyers-of-substring` against
`Agroverse QR codes`). Tracking on by default — opens land in cols H–K and
clicks in L–P on the **`Agroverse News Letter Emails`** tab of the dedicated
newsletter workbook (`1ed3q3SJ8ztGwfWit6Wxz_S72Cn5jKQFkNrHpeOVXP8s`),
filtered by `campaign='two_bahia_bars'`.

**Why a follow-up reads the data.** The v5 layout (compact 280px images,
side-by-side comparison row at top) was a deliberate design call. Without a
read-out, the data sits in the sheet and the comparison-row decision can't
be validated for future sends. iOS Mail Privacy Protection inflates opens
in the first hour — the read-out should land **after a 7–10 day soak** so
real engagement (repeat opens, clicks, replies) dominates the noise.

**Outcome.** A short summary covering:
- Open rate (recipients with `open_count > 0`) and median `open_count`.
- Click rate (recipients with `click_count > 0`) and which CTA each clicker
  hit (`last_clicked_url` — Oscar's Farm, Fazenda Santa Ana, or both via the
  comparison row's separate "Check this bar" links).
- Reply rate (search Gmail `to:garyjob@agroverse.shop` against the
  recipient list; count distinct addresses that replied).
- **Did the comparison row's "Check this bar" CTA get clicked at a
  meaningfully different rate than the in-section "Check Oscar's Farm
  2024" / "Check Fazenda Santa Ana 2023" CTAs?** (Same destination URLs,
  different anchor text + position. Real design signal for whether the
  comparison row earns its keep on future two-SKU sends.)

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:two_bahia_bars'`,
   description includes the headline numbers).
2. A DAO contribution submission via **`dao_client`** with the analysis as
   the body and a link to the DApp Remarks row.

**Files / shape.**
- Recipient list keyed off `campaign='two_bahia_bars'` from
  `Agroverse News Letter Emails`.
- Open / click columns already populated by Edgar's
  `/newsletter/open.gif` and `/newsletter/click` endpoints.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<recipient> after:2026-04-27`.
- Sheet write: append to `DApp Remarks` on the Hit List spreadsheet
  (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); see
  `market_research/scripts/hit_list_dapp_remarks_sheet.py` for the helper.

**Owner.** Unclaimed. Earliest sensible: **2026-05-07** (10 days after the
send — opens / clicks have stabilized, replies have had a week to land).

**Optional adjacent work.** While reading the data, also note whether
either of the two excluded buyers (`pamelacotton7@msn.com`,
`toffees_fibrils.0l@icloud.com`) ever asked "why didn't I get the
newsletter about the bars I bought?" — would update the buyer-exclusion
copy in `AGROVERSE_NEWSLETTER_WORKFLOW.md` §4.3a if so.

[n-pr79]: https://github.com/TrueSightDAO/go_to_market/pull/79
[n-pr84]: https://github.com/TrueSightDAO/go_to_market/pull/84
[n-pr85]: https://github.com/TrueSightDAO/go_to_market/pull/85

---

## Recently shipped

_(empty — move entries here with their merged PR link when they ship)_

---

## Closed without shipping

_(empty — move entries here with a one-line reason when they're no longer
relevant)_
