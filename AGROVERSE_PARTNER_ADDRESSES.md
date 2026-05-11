# Agroverse Partner Addresses — Column J Population Guide

Purpose: Document how we populate and maintain the canonical ship‑to address for each partner so future AIs/operators know where to start.

## Canonical Field

- Sheet: Main Ledger & Operations (ID `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`)
- Tab: `Agroverse Partners`
- Column J: `address` (free‑form)
  - Recommended format: `street1, city, STATE ZIP, country`
  - Used by Shipping Planner API (`get_partner_address`) and the DApp Restock Recommender.
  - Parser tolerates partial/region‑only entries (e.g., city/state only), but USPS quotes are best with full street + ZIP.

See also: `tokenomics/SCHEMA.md` → Sheet: Agroverse Partners (Column J).

## Preferred Population Method (Local Repo → Sheet)

Use local partner pages in `agroverse_shop/partners/<partner_id>/index.html` as source of truth. The helper script extracts the address block and writes it to Column J (matches rows by `partner_id` in Column A):

- Script: `market_research/scripts/extract_partner_addresses_from_repo.py`
- Extraction strategies:
  - `.partner-hero-content > p` (often a one‑line address directly under the heading)
  - `.info-row` where `.info-label == 'Location'` → sibling `.info-value`
- Behavior:
  - Skips rows where J already has a value (does NOT overwrite manual entries)
  - Overwrites only if `--refresh-existing` is passed

Run (dry‑run first):

```
GOOGLE_APPLICATION_CREDENTIALS=agroverse_shop/google-service-account.json \
  python3 market_research/scripts/extract_partner_addresses_from_repo.py \
  --sheet 1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU \
  --partners-tab "Agroverse Partners" \
  --dry-run
```

Write updates (all partners, skip manual J):

```
GOOGLE_APPLICATION_CREDENTIALS=agroverse_shop/google-service-account.json \
  python3 market_research/scripts/extract_partner_addresses_from_repo.py \
  --sheet 1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU \
  --partners-tab "Agroverse Partners"
```

Limit to a subset:

```
... extract_partner_addresses_from_repo.py --only the-way-home-shop,go-ask-alice
```

Overwrite where the repo has improved formatting (use sparingly):

```
... extract_partner_addresses_from_repo.py --refresh-existing
```

## Verification

- Direct API: `get_partner_address`

```
curl -sSL \
  'https://script.google.com/macros/s/AKfycbz5Tt_vz1X26i82yqlGUSI_OtCUEO31jImZH2tXfNaxMbfmJ01dkwUIEZDjsnd10xMbcg/exec?action=get_partner_address&partner_id=the-way-home-shop'
```

Expect `{status: 'success', data: { address: { street1, city, state, zip, country }}}`.

- DApp page: `https://dapp.truesight.me/restock_recommender.html`  
“Shipping to” block should display the formatted address after selecting the partner.

## Fallbacks & Notes

- Manual: You can always paste a one‑line address into Agroverse Partners!J. The API will use it immediately.
- Legacy sheet: If J is blank, API falls back to the older `Partner addresses` tab (A: partner_id, B–F address fields).
- Data quality: USPS quotes are better with full street + ZIP. Region‑only entries work for display but may yield fewer/equivocal USPS options.

## Alternative (Network Scrape) — Usually Not Needed

`market_research/scripts/scrape_partner_addresses.py` can attempt extraction from live pages (heavier, network‑dependent). Prefer the local‑repo method above for reliability and speed.

