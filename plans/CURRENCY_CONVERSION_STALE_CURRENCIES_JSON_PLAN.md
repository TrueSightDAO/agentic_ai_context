# currency_conversion.html — stale currencies.json — plan of record

**Status:** plan-of-record, drafted 2026-08-25 by Envoy (Claude, interactive session on `nelanco-claude`,
Gary driving). Full diagnosis complete; **implementation/execution handed to Sophia** — this seat does not
mutate shared repos/services directly (see `agentic_ai_context/ENVOY.md`).

**Trigger:** Gary noticed `https://dapp.truesight.me/currency_conversion.html`'s currency picker doesn't
offer entries that are genuinely recorded in the `Currencies` tab (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`,
gid `1552160318`), citing row 97 as a reference point.

---

## 1. Pre-flight (§5d — everything an execution unit needs, captured here)

### 1.1 Root cause, fully traced and verified

`currency_conversion.html`'s source/target currency comboboxes are populated entirely from a static file:

```js
const CURRENCIES_JSON_URL = 'https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/currencies.json';
```

That file's `generatedAt` is **`2026-06-20T22:59:51.211Z`** — **over two months stale** as of this plan
(2026-08-25). Direct exact-string comparison between the live `Currencies` sheet (135 data rows) and the
published JSON (127 entries) found:

**9 currencies exist in the live sheet but are missing from the JSON** (so they can't be selected on the
form at all):
```
81% Dark Chocolate Bar 50g | Cacao Almonds KG - Organic (Fazenda São Jorge) | Gary Teh 20260710 | San Francisco
Bluetooth Label Printer w/20 Label Rolls - Brazil
Cacao Almonds KG from Vivi's farm - AGL13   [note: trailing space in the live sheet, see 1.1a]
Cacao Tea 1g | Cacao Almonds KG - Organic (Fazenda São Jorge) | Gary Teh 20260710 | San Francisco
Cacao Tea 50g - Oscar's Farm, Bahia Brazil, 2024 (AGL4)
Cacao Tea 50g QR code labels (batch 2024OSCAR_CT_20260820)
Chocolate Mold MHC-CL082 (58 x 125 mm) - Dongguan MHC Industrial Co Ltd
FounderHaus Tree Planting Pledge - QR Code
Stand-Up Pouch Kraft w/Zip 10x15cm (per unit) - Brazil
```

**1.1a — one entry has drifted (trailing-whitespace mismatch):** the JSON has
`Cacao Almonds KG from Vivi's farm - AGL13` (no trailing space); the live sheet row now reads
`Cacao Almonds KG from Vivi's farm - AGL13 ` (trailing space). If a user could select this from a
cache that predates the edit, submission would fail exact-match validation against the live sheet.

**Row 97 itself** (`Ceremonial Cacao Kraft Pouch - Alibaba:269035810001023771 | Cacao Mass | 200 grams |
8 Ounce Nibs CP340992735BR | Kirsten 20260620 | San Francisco - AGL4`) is present and exact-matches in the
JSON — it happened to land right at the last successful publish. It's a good example of the *class* of
entry (repackaging-ingest output) that *does* get synced; the 9 missing ones above are the ones that don't.

### 1.2 Why it stopped syncing — the actual mechanism, not a crash

`currencies.json` is **only** rewritten as a side effect of one specific code path:
`TrueSightDAO/agroverse-inventory` → `gas/repackaging-currency-ingest/Code.gs` →
`appendCurrencyRowsAndSort_()` → `publishCurrenciesJsonToGitHub_(list)` (line ~457, confirmed by reading
the source directly). This only fires when a `[REPACKAGING BATCH...]` event is processed through *this*
GAS project. **There is no time-driven trigger, no cron, no other write path that republishes it.**

Every one of the 9 missing entries was added to the `Currencies` sheet through a **different** pathway
(manual edit, the QR-code batch minting flow for `2024OSCAR_CT_20260820`, etc.) — none of those touch
`publishCurrenciesJsonToGitHub_`, so the JSON silently drifts further out of sync every time. This is not
a bug that throws or logs anything — it's a structural gap (one specific event type publishes; everything
else doesn't), which is why it went unnoticed for two months.

**Contrast:** `agroverse-inventory/store-inventory.json` in the *same repo* refreshes reliably every day
via a scheduled GitHub Actions workflow (`go_to_market` / `market_research` repo,
`publish-agroverse-inventory-snapshot.yml` calling `sync_agroverse_store_inventory.py`) — confirmed via
`gh api repos/TrueSightDAO/agroverse-inventory/commits`, daily `[skip ci]` commits through today. That's
the working pattern to copy for `currencies.json`, which currently has no equivalent.

**Separately confirmed NOT the cause:** the `treasury-cache-publisher` GAS project
(`treasury-cache/gas/treasury-cache-publisher/Code.gs`, script id
`AKfycbyBmjwmFhR8nQ5ZCtdqQwr-OgC5-htdFnMeXOKLD-Z-NWvNpLGvi7nPbMQVvnhrnbSXdQ`) is alive and unrelated — it
publishes `dao_offchain_treasury.json` in the `treasury-cache` repo, a different file entirely. The
`notifyTreasuryCachePublisher_()` call inside `repackaging-currency-ingest/Code.gs` triggers *that*
service as an unrelated side effect; it has nothing to do with `agroverse-inventory/currencies.json`.

### 1.3 Access already confirmed

- Read access to the `Currencies` tab: `tokenomics/python_scripts/schema_validation/gdrive_schema_credentials.json`
  (documented service account, already used elsewhere in this workspace for Main Ledger reads).
- `agroverse-inventory` repo is public-readable via `raw.githubusercontent.com`; write access needs
  whatever GitHub PAT `repackaging-currency-ingest/Code.gs` already uses (`AGROVERSE_INVENTORY_*` script
  properties per its own header comment) — Sophia should confirm which one at execution time rather than
  guess; don't invent a new credential.
- The `store-inventory.json` scheduled-workflow pattern to copy lives in `go_to_market` (aka
  `market_research`) repo, `.github/workflows/publish-agroverse-inventory-snapshot.yml` +
  `scripts/sync_agroverse_store_inventory.py` — read this file for the actual cron cadence + secrets
  pattern (`GOOGLE_CREDENTIALS_JSON`, `AGROVERSE_INVENTORY_PUSH_TOKEN`) before designing PR2 below.

---

## 2. Sequenced plan

| Unit | What | Repo(s) | Advance |
|---|---|---|---|
| **PR1 — immediate catch-up** | One-time manual re-publish of `currencies.json` from the current live `Currencies` sheet state, closing the 9-entry gap + the trailing-space drift now, without waiting for PR2's automation. Simplest path: run `publishCurrenciesJsonToGitHub_` (or an equivalent one-off script) once, by hand or via a temporary `doGet` action, against the live sheet. | `agroverse-inventory` | _(auto)_ |
| **PR2 — structural fix** | Decouple `currencies.json` from the single repackaging-ingest event path. Recommended shape: a scheduled GitHub Actions workflow (mirrors the already-working `publish-agroverse-inventory-snapshot.yml` / `sync_agroverse_store_inventory.py` pattern) that reads the live `Currencies` tab directly and rewrites `currencies.json` on a schedule (hourly or daily — daily matches the sibling snapshot's cadence and is almost certainly sufficient), independent of which GAS project or manual edit added a row. Do **not** just add more call-sites to `publishCurrenciesJsonToGitHub_()` inside individual event handlers — that repeats the same "only syncs from paths someone remembered to wire up" failure mode. | `go_to_market` (workflow) + `agroverse-inventory` (output) | _(auto)_ |
| **PR3 — UI/UX freshness signal** | On `currency_conversion.html`, surface `currencies.json`'s `generatedAt` near the currency pickers (e.g. small "Currency list updated: <date>" caption) so staleness is visible to a user/operator in the future instead of silently failing to offer an option. See §3 for the fuller UX reasoning — this PR is the minimal, low-risk slice of it. | `dapp_beta` (confirmed — `currency_conversion.html` lives there, not `dapp`) | _(auto)_ |

**PR1 detail:** the cleanest one-off approach is to open the Apps Script editor for
`repackaging-currency-ingest` and run `publishCurrenciesJsonToGitHub_(readCurrencyStringsFromSheet_(mainSs,
shCur))` (or whatever the exact call shape is — read the surrounding function bodies, don't guess the
signature) once by hand, OR temporarily add a `doGet(?action=republish_currencies)` branch that calls the
same function, hit it once, then decide whether to keep or remove that branch (PR2 makes it moot either
way once the scheduled job exists). Verify success by re-diffing sheet vs. JSON exactly as done in §1.1 —
the 9-entry gap and the trailing-space drift should both be gone.

**PR2 detail:** don't reinvent the wheel — `sync_agroverse_store_inventory.py` already reads Google Sheets
and writes JSON to this exact repo on a working schedule. A new sibling script (`sync_currencies_json.py`
or similar) doing the equivalent read-`Currencies`-tab → write-`currencies.json` should be a small diff
against that existing pattern, not a from-scratch design.

---

## 3. UI/UX assessment (asked for explicitly, not just the bug)

The deeper issue isn't really the widget — it's that a **static, irregularly-refreshed cache is the source
of truth for a live financial form**, and the UI gives no signal when that cache is stale. Three tiers,
cheapest first:

1. **(This plan, PR3) Surface the cache's own freshness.** `currencies.json` already carries a
   `generatedAt` field — just render it. Turns an invisible failure into a visible one, which is most of
   the value for the least effort.
2. **(Not in this plan — flag for Gary, don't build without a decision)** Consider whether the combobox
   should have a manual "Can't find your currency? Refresh list" affordance that re-fetches
   `currencies.json` with cache-busting, for the gap between PR2's scheduled refreshes and a truly live
   read.
3. **(Bigger, not recommended without real need)** Replace the static-JSON pattern with a live read (a
   lightweight GAS/Edgar endpoint that queries `Currencies` directly on page load). More correct, but a
   heavier lift than the actual problem warrants — PR2's scheduled regeneration should close the gap to
   "stale by at most a few hours," which is almost certainly fine for a form a human fills out
   interactively. Only worth it if staleness turns out to still bite after PR1+PR2 ship.

**Recommendation: ship PR3 (tier 1) as part of this plan; leave tier 2 as an open question for Gary; don't
build tier 3 unless PR1+PR2 turn out not to be enough.**

---

## 4. Resume tracker

**RESUME HERE → PR1.**

| Unit | PR | Opened | Merged | Deployed/live | Reported |
|---|---|---|---|---|---|
| PR1 — immediate catch-up republish | not started | ☐ | ☐ | ☐ | ☐ |
| PR2 — scheduled regeneration workflow | not started | ☐ | ☐ | ☐ | ☐ |
| PR3 — UI freshness caption | not started | ☐ | ☐ | ☐ | ☐ |

✅ **Pre-flight Completeness (§5d):** §1 captures the full root-cause trace, the exact missing/drifted
entries, the working sibling pattern to copy for PR2, and where credentials for `agroverse-inventory`
writes already live. No execution unit should need to re-derive the diagnosis from scratch.

---

## 5. UAT (human-tested, before calling this done)

| # | Surface | What to expect | Interaction | Acceptance criterion |
|---|---|---|---|---|
| 1 | `currencies.json` raw file | Fresh `generatedAt`, all 135 live sheet entries present, no trailing-space drift | `curl` + diff against live sheet (same method as §1.1) | Zero missing/drifted entries |
| 2 | `currency_conversion.html` | Source/Target comboboxes offer the 9 previously-missing currencies (e.g. type "Cacao Tea 50g") | Open the page, type into the currency field | The previously-missing entries now appear and are selectable |
| 3 | (after PR2) `agroverse-inventory` commit history | New scheduled `chore: refresh currencies.json` commits appear on the expected cadence | `gh api repos/TrueSightDAO/agroverse-inventory/commits`, wait one cycle | At least one new scheduled commit, matching `store-inventory.json`'s pattern |
| 4 | (after PR3) `currency_conversion.html` | A visible "Currency list updated: <date>" caption near the pickers | Open the page | Caption renders, date matches `currencies.json`'s `generatedAt` |

---

## 6. References

- `agroverse-inventory/gas/repackaging-currency-ingest/Code.gs` — the incomplete publish path (root cause)
- `treasury-cache/gas/treasury-cache-publisher/Code.gs` — confirmed unrelated, do not confuse the two
- `go_to_market` `.github/workflows/publish-agroverse-inventory-snapshot.yml` +
  `scripts/sync_agroverse_store_inventory.py` — the working pattern PR2 should mirror
- `dapp_beta` `currency_conversion.html` — the form itself, PR3's target
