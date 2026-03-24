# Lead List Extraction — Contact Discovery for Hit List

**Read this** when the task involves discovering retailer/lead contacts and updating the **Hit List** (Holistic Wellness retailer lead list for Agroverse.shop ceremonial cacao distribution).

---

## Overview

The Hit List is a Google Sheet of qualified retail stores (apothecaries, metaphysical shops, wellness centers) to visit or contact for Agroverse.shop distribution. We extract contact information via:

1. **Playwright** — Scrape Google Maps and Yelp for business listings
2. **CSV output** — `apothecary_discovery.csv` with normalized fields
3. **Append script** — Push rows to the Hit List Google Sheet

---

## Hit List Location

- **Spreadsheet:** https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit
- **Tab:** Hit List
- **Credentials:** `market_research/google_credentials.json` (service account `agroverse-market-research@get-data-io.iam.gserviceaccount.com`)
- **Schema:** See `market_research/HIT_LIST_CREDENTIALS.md`

---

## Extraction Flow

```
Playwright (research_apothecaries.ts)
    → Google Maps + Yelp scraping
    → apothecary_discovery.json / apothecary_discovery.csv
    → append_to_hit_list.py
    → Hit List Google Sheet
```

---

## Key Files (market_research repo)

| File | Purpose |
|------|---------|
| `ceremonial_cacao_seo/playwright/research_apothecaries.ts` | Playwright script: Google Maps + Yelp discovery |
| `ceremonial_cacao_seo/apothecary_discovery.csv` | Output CSV (input for append) |
| `ceremonial_cacao_seo/apothecary_discovery.json` | Output JSON (full data) |
| `append_to_hit_list.py` | Appends CSV rows to Hit List via gspread |
| `HIT_LIST_CREDENTIALS.md` | Schema, Store Key format, credentials |
| `physical_stores/pull_hit_list.py` | Pull Hit List to `data/hit_list.csv` (backup/sync) |
| `physical_stores/generate_shop_list.py` | Replace Hit List with hardcoded SHOPS (legacy) |
| `physical_stores/process_dapp_remarks.py` | Apply DApp remarks to Hit List |

---

## Run Order

### 1. Discovery (Playwright)

```bash
cd market_research/ceremonial_cacao_seo/playwright
npx ts-node research_apothecaries.ts
```

**Env vars:**
- `HEADLESS=0` — Visible browser (debug)
- `YELP_MAX_PAGES=1` or `2` — Limit Yelp pages (throttling)
- `REGIONS=TX,NY` — Run only specified states (e.g. Austin TX + Rochester NY). Omit to run all (CA, AZ, OR, WA, TX, NY).

**Output:** `../apothecary_discovery.json` and `../apothecary_discovery.csv`

### 2. Append to Hit List

```bash
cd market_research
python3 append_to_hit_list.py
```

**Requires:** `google_credentials.json` in `market_research/`, sheet shared with service account.

### 3. (Optional) Pull latest Hit List before/after

```bash
cd market_research/physical_stores
python3 pull_hit_list.py
```

Writes `data/hit_list.csv` for local backup or downstream scripts.

---

## What the Playwright Script Does

1. **Google Maps** — Searches "apothecary metaphysical" in CA, AZ, OR, WA (2 cities per state)
2. **Yelp** — Same regions, with 4–8 s delays and `YELP_MAX_PAGES` limit
3. **Filters:**
   - Junk names: `Results`, `Sponsored`, `Suggest an edit`, etc.
   - Valid address: ≥10 chars, contains a number
   - Clean address: remove leading Unicode chars from Google Maps
4. **Instagram extraction:**
   - From Maps/Yelp panel: `a[href*="instagram"]` links
   - Fallback: visit store website, scrape for Instagram links
5. **Instagram follower count:** Visit `instagram.com/{handle}` for stores with Instagram; extract count from page source or body text
6. **Store Key:** `{shop-name}__{address}__{city}__{state}` (lowercase, hyphens)

---

## Hit List Column Schema (aligned with append)

| Col | Name | Notes |
|-----|------|-------|
| A | Shop Name | |
| B | Status | Research, Partnered, etc. |
| C | Priority | Medium |
| D | Address | Required |
| E | City | |
| F | State | CA, AZ, OR, WA |
| G | Shop Type | Metaphysical/Spiritual |
| H | Phone | |
| I | Cell Phone | |
| J | Website | |
| K | Email | |
| L | Instagram | @handle format; important for qualified leads |
| M–AB | Notes, Contact Date, etc. | |
| AC | Instagram Follow Count | From Instagram profile scrape |
| AD | Store Key | Deduplication key |

---

## Extending for New Sources or Regions

- **New regions:** Edit `STATES` and `cities` in `research_apothecaries.ts`. Current: CA, AZ, OR, WA, TX (Austin area), NY (Rochester area). Use `REGIONS=TX,NY` to run only specific states.
- **New sources:** Add search function (e.g. another directory site), output `DiscoveredStore[]`, merge into `allStores` with `seenKeys` dedup
- **New fields:** Add to `DiscoveredStore`, `toCsvRow()`, CSV header, and `append_to_hit_list.py` `cols` list
- **Different store types:** Change search term (e.g. "wellness center", "herb shop") and `shopType`

---

## Credentials Checklist

- [ ] `market_research/google_credentials.json` exists (service account)
- [ ] Hit List sheet shared with `agroverse-market-research@get-data-io.iam.gserviceaccount.com` as Editor
- [ ] Google Sheets API enabled in project `get-data-io`

---

## Related

- **Ceremonial cacao competitors:** `market_research/ceremonial_cacao_seo/` — brand research, sales drivers
- **Physical stores Hit List:** `market_research/physical_stores/` — pull, generate, DApp remarks
- **Cursor rule:** `market_research/.cursor/rules/ceremonial-cacao-competitors.mdc` — competitor context
