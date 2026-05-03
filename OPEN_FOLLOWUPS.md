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

### `dao_client onboard_retail_partner` CLI — v1: website + PR automation

**Context.** MVP shipped via [`dao_client#11`][onboard-mvp] on
2026-04-28 — automates the deterministic ledger + inventory steps
(§3.1 / §3.2 / §3.3 / §3.13 / §3.14 of
`RETAILER_TECHNICAL_ONBOARDING.md`) idempotently, with a YAML manifest
input. Dry-run by default. Operator still has to do the website surface
work + photo upload + PR creation manually after running it.

v1 fills in the remaining steps:

- §3.4 Partner page generation (clone `partners/lumin-earth-apothecary/`,
  named-replacement on slug + name + address + lat/lon + about-blurb;
  about-blurb either operator-supplied in manifest or Grok-extracted
  from `website` URL).
- §3.5 Discovery surface updates (`partners-data.js` append,
  `partner_locations.json` append, `wholesale/index.html` and
  `partners/index.html` alphabetical inserts,
  `cacao-journeys/pacific-west-coast-path/index.html` jpeg-extension
  conditional).
- §3.6 Photo download + resize (operator URLs in manifest, or fall back
  to scraping `og:image` / favicon).
- §3.12 + §3.15 Branch + commit + `gh pr create` in `agroverse_shop_beta`
  and `agroverse-inventory`. Push branch only — operator merges manually
  for the first 5–10 onboardings before flipping to auto-merge.
- §3.4 lat/lon geocoding via Nominatim (free, no key) when manifest
  doesn't include them.

**Acceptance criterion.** Next retail-partner onboarding takes ≤ 5
minutes of operator time end-to-end, including PR review + merge.

**Blocker.** None — every required piece exists. MVP must run cleanly
on a real onboarding before v1 layers on the more invasive automation
(template clone, multi-repo PR creation).

**Owner.** Unclaimed.

[onboard-mvp]: https://github.com/TrueSightDAO/dao_client/pull/11

---

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

### Warm-up email A/B read-out — PDF-only vs PDF+packaging-photos cohort comparison

**Context.** [`go_to_market#74`][wp-pr74] (merged 2026-04-27) flipped the
default warm-up email payload from "PDF wholesale catalog only" to "PDF +
2 packaging photos" for every send via the partner-outreach pipeline. The
hypothesis: visual product proof in the first touch lifts open / click /
reply rates over a PDF-only ask. Without a read-out, the change sits as
an untested intuition.

**Why a follow-up reads the data.** The cleanest natural experiment we'll
get — the cutover is sharp (one PR), the population is otherwise
homogeneous (same Hit List rows, same template, same operator), and the
volume on either side of 2026-04-27 should be enough for a directional
signal even if not statistically rigorous. Earliest sensible read:
**2026-05-11** (~2 weeks of post-cutover sends + replies have had time
to land — Gmail reply soak window matches the newsletter read-out
above).

**Outcome.** A short comparison covering, for each cohort:
- **Cohort split.** Read the `Email Agent Follow Up` tab of the Hit List
  workbook (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); split
  rows where status indicates a warm-up was sent into:
  - **Pre-2026-04-27** (PDF only) — sent before the cutover.
  - **On/after 2026-04-27** (PDF + 2 packaging photos) — the new default.
- **Metrics per cohort.** Count, open rate (`Open` column > 0), click
  rate (`Click through` column > 0), reply rate (cross-reference Gmail
  for inbound replies to each `to_email` after `sent_at`).
- **Time-controlled comparison.** Repeat the metrics restricted to the
  **2 weeks immediately before** vs **2 weeks immediately after**
  2026-04-27 to neuter time-of-year / list-quality drift.
- **Verdict.** Did packaging-photo warm-ups beat PDF-only on any of
  open / click / reply by a margin that would survive doubling the
  sample size? If yes — keep the new default. If no — flag whether to
  revert or keep as the cleaner UX call regardless of metrics.

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:warmup_packaging_photos_ab'`,
   description includes headline numbers + PR URL).
2. A DAO contribution submission via **`dao_client`** with the analysis
   as the body and a link back to the DApp Remarks row + PR #74.

**Files / shape.**
- Sheet read: `Email Agent Follow Up` tab on
  `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc` via
  `google_credentials.json` + gspread.
- Status / cohort inference: `market_research/HIT_LIST_CREDENTIALS.md`
  documents the Status column conventions.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<to_email> after:<sent_at>` per recipient.
- DApp Remarks append: `market_research/scripts/hit_list_dapp_remarks_sheet.py`.
- Contribution log: dao_client CLI per
  `agentic_ai_context/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`.
- Label / status convention: `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` §9.7.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks post-cutover).

**Why not `/schedule`.** Tried — remote agent can't access the private
sheet, Gmail OAuth, or Edgar tokens (no MCP connectors connected, no
`google_credentials.json` in cloud sandbox). Belongs on the local
backlog.

[wp-pr74]: https://github.com/TrueSightDAO/go_to_market/pull/74

### Migrate `dapp/stores_nearby.html` Add Store form onto the `[STORE ADD EVENT]` Edgar path

**Context.** The dao_client / Edgar / GAS slice of `[STORE ADD EVENT]`
shipped 2026-04-28 (see *Recently shipped* below). The DApp's
`stores_nearby.html` Add Store form still talks directly to GAS
`add_store` — small GET payload that doesn't have the cross-origin
failure mode the retail field report flow had, so it works, but the
DAO has decided that **all signed Hit List writes go through the same
canonical pattern**: DApp → Edgar → Telegram Chat Logs → async GAS
scanner. This entry is the remaining migration to that posture.

**What's needed.**
- Replace the direct `fetch(GAS, {action: 'add_store', …})` call in
  `dapp/stores_nearby.html` with a signed `[STORE ADD EVENT]` POST to
  Edgar (mirror today's `submitRetailFieldReportToEdgar` shape in
  `dapp/store_interaction_history.html`).
- Drop or repurpose the `add_store` action in
  `clasp_mirrors/1NpHrKJW…/Code.js` once no callers remain. The
  `addNewStore()` helper stays — it's the GAS scanner's own
  dependency.
- Verify the DApp form's "duplicate detected" UX still works
  (today the GAS direct call returned `{success: false, duplicate:
  true, existing_store: …}` synchronously; with the async path the
  duplicate detection lands on **Store Adds** col K
  `existing_store_shop_name`, so the form needs a polling /
  back-channel UX or a "submitted — check Hit List in a minute"
  message).

**Cost estimate:** ~30 min including the form's status / duplicate UX.

**Blocker.** None — purely additive once started. Don't bundle with
unrelated `stores_nearby.html` work.

**Owner.** Unclaimed.

### Deprecate `backfill_hit_list_opening_hours.py` + `backfill_hit_list_google_listing.py` after 2 cron cycles

**Context.** 2026-04-28 the two responsibilities — opening-hours grid (Mon
Open … Sun Close) and `Google listing` column — were folded into the routine
hourly cron at `.github/workflows/hit_list_enrich_contact.yml` (`35 * * * *`)
via [TrueSightDAO/go_to_market#88][pr88]. The enriched
`scripts/hit_list_enrich_contact.py` now also fills empty `Address / City /
State / Latitude / Longitude` from the same Places Details call. The two
standalone backfills still exist as manual one-shots but should no longer
need to be invoked routinely.

**Outcome.** Either delete the two standalone scripts, or shrink them to
thin documented wrappers that call into `hit_list_enrich_contact.py`'s
`apply_place_result_to_row_gaps()` helper for one-shot full-table sweeps.

**Files.**
- `market_research/scripts/backfill_hit_list_opening_hours.py`
- `market_research/scripts/backfill_hit_list_google_listing.py`
- `market_research/scripts/hit_list_enrich_contact.py` (already imports both
  via `bl` / `dl` for `resolve_place_id` + `append_place_id_to_notes` —
  if either backfill is deleted, inline the helpers it depends on or move
  them into a shared module).

**Verification before deleting.** On the Hit List, confirm:

1. New rows landing in the past 2 weeks have non-empty `Address`, `City`,
   `State`, `Latitude`, `Longitude`, `Monday Open`, `Google listing` (where
   Places returns those fields) within ~24h of arrival.
2. The `cron`-scheduled action's last 24 runs each show `filled>0` or a
   clean `skipped` count (i.e. the cron is closing gaps, not silently
   no-op'ing).

**Blocker / signal to revisit.** Earliest sensible: **2026-05-12** (~2
weeks of cron cycles after #88 lands).

**Owner.** Unclaimed.

[pr88]: https://github.com/TrueSightDAO/go_to_market/pull/88

---

### Validate the circle-hosting → cacao-velocity hypothesis after 4 partners-velocity refreshes

**Context.** 2026-04-28 observation: two recent / candidate retail partners
mention **women's circles** prominently — [The Way Home Shop in SE
Portland][way-home] (just onboarded) and Lumin Earth (existing partner).
Ceremonial cacao genuinely lives in that ecosystem (women's circles, sound
baths, breathwork, new-moon gatherings), so "hosts circles" is plausibly
a leading indicator of cacao sell-through.

The cheap detection step shipped immediately as
`market_research/scripts/detect_circle_hosting_retailers.py`
(see [go_to_market#XX][circle-pr] when filed) — it crawls each Hit List
retailer's `Website` for high-precision keywords (women's circle, moon
circle, cacao ceremony, sound bath, breathwork, sister/sacred circle,
ecstatic dance) and writes **Yes / Not detected** to a new
**Hosts Circles** Hit List column. *That* part is data-only; this entry
covers the deferred *correlation* check.

**Outcome.** Once `partners-velocity.json` has ≥4 weekly refreshes, cross-
reference per-SKU velocity against the **Hosts Circles** flag for
already-onboarded partners. Two questions:

1. Do circle-hosting partners outsell non-circle peers per-SKU at
   statistically meaningful margins? If yes, **green-light**:
   - Add `Hosts Circles=Yes` as a positive signal on the warm-up draft
     generator (next to the dormant / high-velocity logic in the existing
     entry above).
   - Open a separate research entry on whether to build a **circle
     facilitator** outreach motion (different ICP than retailers — direct
     to circle-leaders who buy in bulk for their gatherings).
2. If the correlation is weak or negative, rule it out and close.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read latest snapshot.
- Hit List **Hosts Circles** column (col after `Google listing`) — read.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic + sample-size guards.

**Blocker / signal to revisit.** Same as the **Eyeball-check
`partners-velocity.json`** entry above — wait for ≥4 entries on the
GitHub Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible:
**2026-05-25**. Combine with that entry's manual sanity check so
both reads happen in one sitting.

**Owner.** Unclaimed.

[way-home]: https://thewayhomeshop.com/
[circle-pr]: https://github.com/TrueSightDAO/go_to_market/pulls?q=is%3Apr+circle+hosting

---

### Fix `addNewStore()` GAS — `setValues`-dimension mismatch on tail-end step

**Context.** `[STORE ADD EVENT]` end-to-end test 2026-04-28 (see *Recently
shipped*) added 3 referrals for Psychic Sister (Clary Sage / Casa de Ritual
/ La Sirena Botanica) — all three landed on Hit List rows 526–528 with the
correct shop name / status / city / state / shop type / Notes / Sales
Process Notes / Status Updated By / Status Updated Date / Store Key.

But every single submission also recorded `status: error` on the **Store
Adds** dedup log with this error message:

```
The number of rows in the data does not match the number of rows in the
range. The data has 1 but the range has 526.
```

That's an Apps Script `setValues(values)` dimensional error from inside
`addNewStore()` (likely the trailing `logDappSubmission_(...)` call or a
sales-notes write). It throws **after** the new Hit List row has been
fully written (since the row is correct), so the data is fine — but the
exception escapes addNewStore's try/catch boundary and lands in the new
GAS scanner's error handler.

**Symptoms.**
- Hit List rows land correctly (operator-visible).
- Store Adds dedup log says `error` with this message (audit-trail-misleading).
- A re-fired Telegram Chat Logs row would NOT re-add (idempotent on
  Telegram Update ID), so no double-row risk.

**Fix targets.**
1. **Root cause** in `clasp_mirrors/1NpHrKJW…/Code.js` `addNewStore()` /
   `logDappSubmission_()`. The `526` figure is "all data rows on the Hit
   List sheet"; somewhere a `range.setValues(arr)` is being called with
   `arr.length === 1` against a range covering all data rows. Likely
   pattern: `sheet.getDataRange().setValues([row])` instead of
   `sheet.appendRow(row)` / `sheet.getRange(targetRow, 1, 1, n).setValues([row])`.
2. **Defensive workaround** in
   `google_app_scripts/find_nearby_stores/process_store_adds_telegram_logs.gs`:
   when `addNewStore` throws, fall back to a Hit List lookup by
   `store_key` (the same key `createStoreKey_` builds). If found,
   record `status: added_with_warning` + the exception text in
   `error_message` instead of `status: error`. That way the audit log
   correctly reports the row was added even when addNewStore's tail
   step fails.

**Cost.** ~20 min for (1) once the offending line is found; ~10 min
for (2). Both are independent — do (2) first if you want clean audit
trails fast; do (1) if you want addNewStore stable for the existing
DApp form callers.

**Owner.** Unclaimed.

---

## Recently shipped

### `dao_client onboard_retail_partner` MVP — 2026-04-28

Manifest-driven CLI that automates the deterministic ledger + inventory
steps from `RETAILER_TECHNICAL_ONBOARDING.md` §3:

- Step 1 `[CONTRIBUTOR ADD EVENT]` (with name pre-formatted as
  `<First> - <Store>` to dodge Edgar's auto-rename).
- Step 2 `Contributors!U` (Mailing Address). Explicitly does **not**
  toggle col T — that flag is reserved for online-fulfillment managers
  (Gary + Kirsten only).
- Step 3 `Agroverse Partners` row append.
- Step 13 `[INVENTORY MOVEMENT]` loop for opening-order QR codes.
- Step 14 subprocess `sync_agroverse_store_inventory.py` and
  `sync_partners_velocity.py` so JSON snapshots refresh.

Idempotent at every step. `--dry-run` is the default. Worked-example
manifest in `examples/onboarding/the-way-home-shop.yaml` replays the
2026-04-28 onboarding as a no-op.

Steps still operator-manual in MVP: partner page, discovery surfaces,
photo download, PR creation (steps 4 / 5–10 / 11 / 12 / 15). Script
prints copy-paste instructions at the end. v1 covers those — see the
remaining Pending entry above.

PR: https://github.com/TrueSightDAO/dao_client/pull/11

---

### `[STORE ADD EVENT]` canonical pattern (additive slice) — 2026-04-28

Signed Hit List adds now route through the same Edgar pattern as retail
field reports: dao_client / DApp signs `[STORE ADD EVENT]` → Edgar
`/dao/submit_contribution` → Telegram Chat Logs → `WebhookTriggerWorker`
fires `processStoreAddsFromTelegramChatLogs` GAS scanner → `addNewStore`
on Hit List + audit row on **Store Adds** dedup log
(`1qbZZhf-…`, gid 1208101506; col B `telegram_update_id` is the dedup
key). Verified end-to-end: 3 Psychic Sister referrals (Clary Sage,
Casa de Ritual, La Sirena Botanica) added as Research rows on Hit List
rows 526–528 with referral provenance in Notes + Sales Process Notes;
scanner replay = 0/0/0/0 (perfectly idempotent).

Two follow-ups split out into Pending above:
1. Migrate `dapp/stores_nearby.html` Add Store form off the legacy
   direct GAS GET onto the same Edgar path.
2. Fix the pre-existing `addNewStore()` GAS `setValues` dimensional
   bug so audit logs say `added` instead of `error` even though the
   actual Hit List rows write correctly.

PRs:
- TrueSightDAO/dao_client#9 — `add_hit_list_store.py` module.
- TrueSightDAO/sentiment_importer#1042 — Edgar `[STORE ADD EVENT]` branch.
- TrueSightDAO/tokenomics#250 — `processStoreAddsFromTelegramChatLogs`
  GAS scanner + Store Adds tab schema.

---

## Closed without shipping

_(empty — move entries here with a one-line reason when they're no longer
relevant)_
