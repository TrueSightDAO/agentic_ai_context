# Google Places API caching — architecture, history, gotchas

_Last updated 2026-05-03 by Claude (Anthropic). PR series #97, #99, #100,
#101, #102, #103 in `TrueSightDAO/go_to_market`._

## TL;DR for future LLMs

Google Places Details / Find Place / Nearby Search calls in this codebase
are **cached permanently in [`TrueSightDAO/places-cache`](https://github.com/TrueSightDAO/places-cache)** via the GitHub Contents API. **Always go through `scripts/places_cache.py`** — never call `https://maps.googleapis.com/maps/api/place/...` directly.

```python
from places_cache import (
    cached_place_details_full,   # Basic + Contact tier — phone/website/hours
    cached_place_details_lite,   # Basic tier only — photos/types/business_status
    cached_nearby_search,        # Nearby Search with per-(centroid,radius,keyword) cache
    is_rate_limited,             # process-level circuit breaker — long sweeps should bail when True
)
```

Repeat lookups for the same `place_id` cost **$0** after the first call.
Definitive negatives (`NOT_FOUND` / `ZERO_RESULTS` / `INVALID_REQUEST`)
are also cached, so bad place_ids don't re-pay either.

If Cloud Monitoring shows Place Details > ~5 calls/day in steady state,
**something is bypassing the cache** — see "Investigating spikes" below.

## Cache repo schema

`TrueSightDAO/places-cache` is the materialized-view repo. One file per
place_id:

```
places/<2-char-prefix>/<place_id>.json
coverage/nearby/<sanitized_combo>.json    # for cached_nearby_search
```

```json
{
  "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
  "name": "Google Sydney - Pirrama Road",
  "fetched_at": "2026-05-03T05:30:00Z",
  "fields_requested": ["place_id", "name", "formatted_address", ...],
  "google_status": "OK",
  "result": { /* the Place Details `result` block, verbatim */ }
}
```

Fields:
- `google_status` — added by PR #102. `"OK"` = positive cache, `"NOT_FOUND"` /
  `"ZERO_RESULTS"` / `"INVALID_REQUEST"` = definitive negative (caller gets
  `{}` without a live call). Old records without this field default to `"OK"`
  via `dict.get(..., "OK")`.
- `fields_requested` — superset check for cache hit. A `lite` cache record
  cannot satisfy a `full` request; the cache module re-fetches the union
  and overwrites.

## Token / secret requirements

| Variable | Where | Purpose |
|---|---|---|
| `PLACES_CACHE_PAT` | `market_research/.env` + `TrueSightDAO/go_to_market` repo secret | Fine-grained PAT, `Contents: Read and write`, scoped only to `TrueSightDAO/places-cache`. **Required** in every workflow that runs a script using `places_cache`. |
| `GOOGLE_MAPS_API_KEY` (or `GOOGLE_PLACES_API_KEY`) | `.env` + repo secret | API key for live Places calls. Issued from the `get-data-io` GCP project. |

**Every cron workflow that runs a script using `places_cache` MUST inject
`PLACES_CACHE_PAT` into the Python step's `env:` block.** This is the bug
PR #99 fixed — the secret existed but wasn't propagated, so the cache
silently no-op'd in production for ~2 days, generating ~11k/day live
Place Details calls and a $200+ daily spend until detected.

```yaml
- name: Run my script
  env:
    GOOGLE_MAPS_API_KEY: ${{ secrets.GOOGLE_MAPS_API_KEY }}
    PLACES_CACHE_PAT: ${{ secrets.PLACES_CACHE_PAT }}      # MUST INCLUDE
  run: python3 scripts/my_script.py
```

## Process-level circuit breaker

When any live call returns `OVER_QUERY_LIMIT` / `REQUEST_DENIED` /
`RESOURCE_EXHAUSTED`, `places_cache._RATE_LIMITED` flips to True for
the rest of the process. Subsequent `cached_place_details*()` calls
return `{}` without hitting the API. Long-running sweeps should check
`places_cache.is_rate_limited()` between iterations and bail.

Rationale: a script with N gappy rows would otherwise make N failed
live calls, each adding to GCP request counts even when status != OK.
The breaker bounds waste at ~1 call per process. Reset by restarting
the process; until then, cached values still serve normally.

## Field tiers (Legacy Places pricing — what we use)

| Tier | Fields | Price |
|---|---|---|
| Basic | place_id, name, formatted_address, geometry, types, address_component, business_status, vicinity, photos, url, plus_code, icon | $17/1k |
| Contact | formatted_phone_number, website, opening_hours | +$3/1k |
| Atmosphere | rating, user_ratings_total, reviews, price_level | +$5/1k |

**Atmosphere fields are NEVER requested.** A 2026-05-01 audit confirmed no
caller reads `rating` / `user_ratings_total` etc. from any response;
requesting them was pure waste (~25% of every Details call). Don't add
them back without first auditing whether they're actually consumed.

## Why we stayed on Legacy, not the New Places API

Looked at Places API (New) per-SKU pricing in PR #98. For our typical
field combo (Basic + Contact: address, phone, website, hours), the
New API splits across Pro + Enterprise SKUs at ~$45/1k, vs $20/1k on
Legacy combined-tier billing. New API only wins for narrow Essentials
slices (~$5/1k for photos+types+place_id), which isn't how we query.

Decision: stay on Legacy. Revisit if a narrow-slice use case appears.

## Hit List qualification pipeline (post-PR #101)

The photo+Grok rubric in `hit_list_research_photo_review.py` was
**retired from cron** on 2026-05-03. The site-keyword crawl in
`detect_circle_hosting_retailers.py` is now the canonical qualifier:

```
Research (with website)
   │
   ▼  (free site crawl — keyword set defined in detect_circle_hosting)
   ├─ Hosts Circles=Yes + email present  →  AI: Warm up prospect   (skip Enrich)
   ├─ Hosts Circles=Yes + email missing  →  AI: Enrich with contact (Enrich harvests email)
   └─ site crawled OK + zero matches     →  AI: No fit signal       (renamed 2026-05-03 from
                                              legacy "AI: Photo rejected"; new name reflects
                                              evidence — site shows no qualifying signals)
```

Legacy `AI: Photo rejected` rows from the OLD photo+Grok pipeline are
re-evaluated by `detect_circle_hosting`'s default-on rescue path (which
reads BOTH the new and legacy names) — if a re-crawl finds keywords,
they get promoted to Enrich. Otherwise they can be bulk-renamed via
`scripts/rename_legacy_photo_rejected_status.py` to the new canonical
name. See `HIT_LIST_STATE_MACHINE.md` for the full state machine.

`hit_list_research_photo_review.yml` workflow keeps `workflow_dispatch`
for manual debugging but the schedule cron is gone.

## Direct callers of the cache (reference)

All Place Details routed through `places_cache`:

| Script | Helper used | Tier |
|---|---|---|
| `google_places_lookup.py:place_details` (canonical shim) | `cached_place_details_full` | full |
| `discover_apothecaries_la_hit_list.py:place_details` + `collect_nearby_for_center` | `cached_place_details_full`, `cached_nearby_search` | full + Nearby coverage |
| `hit_list_research_photo_review.py:place_details` (manual-only now) | `cached_place_details_lite` | lite |
| `hit_list_enrich_contact.py:place_details_full` | `dl.place_details` (→ shim → cache) | full |
| `backfill_instagram_la_discovery.py:place_details_website` | `cached_place_details_full` | full |
| `hit_list_extract_email_gemini.py:place_details_website` | `cached_place_details_full` | full |
| `backfill_hit_list_google_listing.py` | `dl.place_details` (→ shim → cache) | full |
| `backfill_hit_list_opening_hours.py` | `dl.place_details` (→ shim → cache) | full |
| `field_agent_location_places_pull.py` | `dl.place_details` (→ shim → cache) | full |
| `refresh_places_cache_status.py` | direct (intentional — Basic-only refresh sweep, free SKU) | basic |
| `bootstrap_places_cache_from_hit_list.py` | direct write (no live call — synthesizes from sheet) | n/a |

## Bootstrapping the cache from sheet data

`scripts/bootstrap_places_cache_from_hit_list.py` (PR #103) walks the
Hit List, extracts `place_id` from the Notes column, and synthesizes a
Place Details cache record from the sheet's columns (Shop Name → name,
Address+City+State → formatted_address, Phone → formatted_phone_number,
Website → website, Lat/Lng → geometry.location, per-day Open/Close →
opening_hours.weekday_text). Writes to `places-cache` via Contents API.

Idempotent — skips already-cached `place_id`s. `--force` to overwrite.
`--dry-run` to preview. Run once per noticeable Hit List growth to
keep the cache pre-warm for new rows.

## Investigating Places API cost spikes

1. **Cloud Monitoring on `get-data-io`** is authoritative for call
   counts per method per day. Service: `places-backend.googleapis.com`,
   metric: `serviceruntime.googleapis.com/api/request_count`. Service
   account `agroverse-market-research@get-data-io.iam.gserviceaccount.com`
   is Owner on the project — has access. Cloud Monitoring + Cloud
   Billing APIs are enabled.

   ```python
   # one-shot example — drop into a script
   from google.oauth2.service_account import Credentials
   from googleapiclient.discovery import build
   from datetime import datetime, timezone
   creds = Credentials.from_service_account_file(
       'google_credentials.json',
       scopes=['https://www.googleapis.com/auth/monitoring.read'],
   )
   mon = build('monitoring', 'v3', credentials=creds, cache_discovery=False)
   now = datetime.now(timezone.utc)
   start = now.replace(hour=0, minute=0, second=0, microsecond=0)
   resp = mon.projects().timeSeries().list(
       name='projects/get-data-io',
       filter=('metric.type="serviceruntime.googleapis.com/api/request_count" AND '
               'resource.labels.service="places-backend.googleapis.com"'),
       interval_startTime=start.isoformat(),
       interval_endTime=now.isoformat(),
       aggregation_alignmentPeriod='86400s',
       aggregation_perSeriesAligner='ALIGN_SUM',
   ).execute()
   for s in resp.get('timeSeries', []) or []:
       method = s.get('resource', {}).get('labels', {}).get('method', '?')
       total = sum(int(p.get('value', {}).get('int64Value') or 0) for p in s.get('points', []))
       print(f'{method}: {total}')
   ```

2. **`TrueSightDAO/places-cache` commit log** shows cache writes per
   day. If the cache is working but call volume is high, cache misses
   are growing — usually means new place_ids surfaced (e.g., a fresh
   `discover_apothecaries` run). If cache writes are zero AND call
   volume is high, the cache is being bypassed — check the `env:`
   block of the running workflow for `PLACES_CACHE_PAT` (PR #99 lesson).

3. **Math sanity check**: total daily Places API calls divided by
   number of unique `place_id`s in the workload. If the ratio is much
   greater than 1, the cache isn't holding (each place is being looked
   up more than once per day). Today's bug surfaced as 11,211 calls /
   600 rows = 18.7 calls/place/day.

## Diagnostic timeline 2026-04-30 → 2026-05-03

| Date | PR | What |
|---|---|---|
| 2026-04-30 | [#97](https://github.com/TrueSightDAO/go_to_market/pull/97) | Persistent cache module + cache repo bootstrap. |
| 2026-04-30 | [#98](https://github.com/TrueSightDAO/go_to_market/pull/98) | Photo gate + Nearby coverage cache + status refresh sweep. |
| 2026-05-03 | [#99](https://github.com/TrueSightDAO/go_to_market/pull/99) | **Critical fix**: workflow `env:` blocks now pass `PLACES_CACHE_PAT`. Without this, the cache from #97/#98 was 100% bypassed in production for ~2 days. Diagnosed via Cloud Monitoring (11,211 Place Details calls in <6 hours). |
| 2026-05-03 | [#100](https://github.com/TrueSightDAO/go_to_market/pull/100) | Process-level circuit breaker + fill-gap attempt cap. Bounds waste on rate-limit days. |
| 2026-05-03 | [#101](https://github.com/TrueSightDAO/go_to_market/pull/101) | Retire photo+Grok qualification, make site crawl canonical. Eliminates the largest Places line item (Place Photos at $7/1k × 5 per shop). |
| 2026-05-03 | [#102](https://github.com/TrueSightDAO/go_to_market/pull/102) | Cache definitive-negative responses. Bad place_ids no longer re-pay. |
| 2026-05-03 | [#103](https://github.com/TrueSightDAO/go_to_market/pull/103) | Bootstrap script — pre-populate cache from existing Hit List sheet data so new cron ticks don't pay first-call cost. |

## Future work / things not yet done

- **Find Place from Text caching.** Used by `hit_list_research_photo_review`
  (manual now), `discover_apothecaries`, `google_places_lookup`. Each call
  is $17/1k. Cacheable on `(text, lat, lng)` key. Same `places-cache` repo,
  different file layout (e.g. `find_place/<sha256(query)>.json`). Not
  shipped yet because the volume is low after photo review went off-cron;
  worth shipping when a noticeable spike appears.
- **Tracking warm-up draft photos.** Photos *as warm-up context* (vs.
  qualification) was discussed but not implemented. A future
  `hit_list_warmup_photo_context.py` could pull photos at draft time
  for personalized warm-ups, but the 2026-05-03 Buck's Spices reply
  case showed site-crawl text was sufficient context.
- **Migrate to Places API (New).** Decided against in PR #98 audit due
  to per-SKU pricing being more expensive for our combo. Revisit if
  Google announces pricing changes.
