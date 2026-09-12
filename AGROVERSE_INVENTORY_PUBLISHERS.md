# Agroverse Inventory JSON Publishers — caches, crons, and how to force a refresh

**Status:** compiled 2026-09-12 (Sophia, thread 27015). Facts read from live state — see §7.
**Audience:** AI assistants (Claude / Cursor / Codex / Kimi) and human operators.
**Siblings:** `WORKSPACE_CONTEXT.md` §cross-repo flow · `partner/RETAILER_TECHNICAL_ONBOARDING.md` §3.8 · `GAS_SCRIPT_PROPERTIES.md`.

---

## 1. What this doc is

`TrueSightDAO/agroverse-inventory` is a **machine-generated public data mirror** for
[agroverse.shop](https://agroverse.shop) and the DApp. **Nothing in it is hand-edited** — every file is
derived from the **Main Ledger** (Google Sheets) by an automated publisher. Because the files are consumed
by live pages, "which publisher, on what cadence, and how do I make it refresh now" is a recurring question.
This doc answers it.

If a cache looks stale, do **not** hand-edit the JSON — the next run overwrites it. Fix the source sheet or
force a run of the publisher (§6).

---

## 2. The published caches (branch `main`)

| File | Content | Consumer | Raw URL |
|---|---|---|---|
| `store-inventory.json` | product ID → online-fulfillable stock count | agroverse_shop, Restock Recommender, Merchant feed | `https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/store-inventory.json` |
| `partners-inventory.json` | per-partner venue + online inventory, keyed by `partner_id` | partner PDPs, Restock Recommender | `…/main/partners-inventory.json` |
| `currencies.json` | alphabetized Main-Ledger `Currencies` col A strings | repackaging planner, DApp pickers | `…/main/currencies.json` |
| **`skus.json`** | the public **SKU catalog** (see §4) | DApp `define_currency.html` | `…/main/skus.json` |
| `partners-velocity.json` | weekly partner sales-velocity snapshot | Restock Recommender, partner deep-dives | `…/main/partners-velocity.json` |
| `currency-compositions/{request_id}.json` | one per repackaging batch (inputs/outputs/totals) | repackaging audit trail | `…/main/currency-compositions/<id>.json` |

---

## 3. The publishers

All publisher code lives in **`TrueSightDAO/go_to_market`** — *formerly named `market_research` (renamed; same
repo id `1064108315`). Git history and the workflow header comments still say `market_research`, which is why
both names appear in the wild.* Treat `go_to_market` as canonical.

| Cache | Publisher (repo path) | Workflow | Cadence (cron, UTC) |
|---|---|---|---|
| `store-inventory.json`, `partners-inventory.json`, **`skus.json`** | `scripts/sync_agroverse_store_inventory.py` | `publish-agroverse-inventory-snapshot.yml` | `15 6 * * *` (daily 06:15) |
| `currencies.json` | `scripts/sync_agroverse_currencies.py` | `publish-agroverse-currencies.yml` | `45 6 * * *` (daily 06:45) |
| `partners-velocity.json` | (velocity script) | `publish-partners-velocity.yml` | `45 6 * * 1` (Mondays 06:45) |

Each workflow: checkouts `agroverse-inventory` into a subdir with the push token, installs Python 3.11 +
`gspread`/`google-auth`, writes the service-account JSON, runs the script with `--execute`, then commits as
**`github-actions[bot]`** and pushes to `main` — **only if a file actually changed** (no useless churn).
`workflow_dispatch` is enabled on all three, so a governor/agent can force a run (§6).

### Required repo secrets (in `go_to_market`)

| Secret | Purpose |
|---|---|
| `GOOGLE_CREDENTIALS_JSON` | service-account JSON with Sheets + Drive **read** on the Main Ledger |
| `AGROVERSE_INVENTORY_PUSH_TOKEN` | fine-grained PAT with **Contents: Read and write** on `TrueSightDAO/agroverse-inventory` (a classic PAT with `repo` scope also works). Needed because the default `GITHUB_TOKEN` cannot push to a different repo. |

---

## 4. `skus.json` — the SKU catalog (added 2026-09-12)

Shape (drop-in compatible with the retired GAS publisher and the DApp parser):

```json
{
  "generatedAt": "2026-09-12T23:56:31.000Z",
  "source": "sync_agroverse_store_inventory",
  "skus": [
    {
      "productId": "ceremonial-cacao-paulo-s-la-do-sitio-farm-200g",
      "productName": "Ceremonial Cacao – La do Sitio Farm, Pará Brazil, 2024 (200g)",
      "priceUsd": "25",
      "weightOz": 7.05,
      "category": "retail",
      "shipment": "AGL8",
      "farm": "Paulo",
      "imagePath": "https://www.agroverse.shop/assets/images/products/la-do-sitio-farm.jpg",
      "storeInventory": 0
    }
  ]
}
```

**Source columns** — the **`Agroverse SKUs`** tab of the Main Ledger, columns **A–I**:

| Col | Field |
|---|---|
| A | `productId` (**rows with a blank A are skipped**) |
| B | `productName` |
| C | `priceUsd` (USD list price) |
| D | `weightOz` (numeric or `null`) |
| E | `category` |
| F | `shipment` |
| G | `farm` |
| H | `imagePath` |
| I | `storeInventory` |

**Two contract details that have already caused a bug — do not "simplify" them away:**

1. **Cells are read UNFORMATTED.** The publisher uses `valueRenderOption=UNFORMATTED_VALUE`, mirroring GAS
   `getValues()`. So `priceUsd` is `"25"`, **not** `"$25.00"`. The DApp drops `priceUsd` straight into
   `<input type="number" id="priceInput">`, so the formatted `"$25.00"` renders the field **blank**.
   (go_to_market #175 fixed exactly this.) Likewise a zero price serializes as `""`, not `"0.00"`.
2. **`weightOz` and `storeInventory` are numbers** (`parseFloat` semantics), `null`/`0` when absent — not strings.

**Consumer:** DApp `define_currency.html` fetches
`https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/skus.json` into its SKU picker.

---

## 5. Secrets are never in source

Credentials live **only** in GitHub Actions repo secrets (§3) and GAS **Script Properties** —
never in the repo. The GAS side uses **`AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`**
(see `GAS_SCRIPT_PROPERTIES.md`). Do not commit any token.

---

## 6. How to force a refresh now

**Option A — GitHub UI (no token needed):** repo **Actions** → pick the workflow → **Run workflow** → `main`.
E.g. `https://github.com/TrueSightDAO/go_to_market/actions/workflows/publish-agroverse-inventory-snapshot.yml`.

**Option B — API (`workflow_dispatch`)** — needs a PAT with **Actions: write** on `go_to_market`:

```bash
curl -X POST \
  -H "Authorization: token $PAT" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/TrueSightDAO/go_to_market/actions/workflows/publish-agroverse-inventory-snapshot.yml/dispatches \
  -d '{"ref":"main"}'
# HTTP 204 = accepted
```

**Option C — run the script directly** (local dry-run writes nothing; `--execute` writes the JSON):

```bash
python3 scripts/sync_agroverse_store_inventory.py --execute \
  --json-out agroverse-inventory/store-inventory.json \
  --partner-json-out agroverse-inventory/partners-inventory.json \
  --skus-json-out agroverse-inventory/skus.json
```

Only `--execute` writes files. Without it, the script reports row counts and exits (safe dry-run against the
live sheet).

---

## 7. How to verify a publish actually happened

A raw.githubusercontent.com read can be served from **CDN cache for a few minutes** after a push — if
`source`/`generatedAt` look stale right after a run, check the **commit** instead:

```bash
# newest commit + author + message in the mirror
gh api repos/TrueSightDAO/agroverse-inventory/commits?per_page=3 \
  --jq '.[] | "\(.commit.author.date) | \(.commit.author.name) | \(.commit.message)"'

# byte-true content at a pinned sha (bypasses the CDN)
gh api repos/TrueSightDAO/agroverse-inventory/contents/skus.json?ref=<sha> --jq .content | base64 -d | head
```

- **Scheduled/forced Python publish** → author **`github-actions[bot]`**, message
  `chore: refresh store, partner inventory, and SKU catalog snapshots [skip ci]`, `source` = the script's value.
- **Manual GAS publish** → author **the human**, `source: "update_store_inventory"` (§8).

---

## 8. Known duality — two writers to the same files

The GAS project **`update_store_inventory`** (script id `1P0Mg33i_dD9x9IeoHYvtKrf0xFcmUznpqAswyC_KXR3VJZu-0C-UOP0v`,
clasp mirror under `tokenomics/google_app_scripts/`) can **also** push to this repo via the GitHub Contents API
using `AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`. It stamps `source: "update_store_inventory"`, whereas the
Python/GHA job stamps `source: "sync_agroverse_store_inventory"`; the two emit otherwise-identical content, so
if both run they **flap the `source` field** on every pass. Tracked in `OPEN_FOLLOWUPS.md` — the recommendation
is to retire one writer per file.
