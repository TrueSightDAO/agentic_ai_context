# Google Maps / Places — project, daily quota cap, and what burns it

_Source: live reverse-engineering on 2026-10-26 after the DApp hit a quota error.
Companion doc: `PLACES_API_CACHING.md` (cache architecture). That doc covers **how**
Places calls are cached; **this** doc covers **which GCP project pays**, **where the
cap lives**, and **what calls it every day**._

## TL;DR

| Question | Answer |
|---|---|
| Which GCP project owns the DApp's browser Maps key? | **`get-data-io`** (project number `667737028020`) |
| Where is the daily request cap? | Quotas & System Limits → metric `places-backend.googleapis.com/billable_default` |
| What was it / what is it now? | **100/day → 200/day** (raised by Gary 2026-10-26) |
| What burns ~100 calls/day? | **`scripts/hit_list_enrich_contact.py`** (hourly cron `:35`) |
| Is it the map tiles? | **No** — `maps-backend` has had **zero** traffic; the dynamic map never loads |

---

## 1. The project: `get-data-io`

```
project_id       get-data-io
project_number   667737028020
service account  agroverse-market-research@get-data-io.iam.gserviceaccount.com
SA creds on box  /home/ubuntu/creds/google_credentials.json   (autopilot EC2)
```

The service account is Owner on the project for project resources (per
`PLACES_API_CACHING.md`), with Cloud Monitoring + Cloud Billing APIs enabled.

### Proof the browser key belongs to this project

Not inferred — read from Cloud Monitoring `serviceruntime.googleapis.com/api/request_count`
for `projects/get-data-io`, 7-day window:

| Service | Method | Calls / 7d |
|---|---|---|
| `places-backend` | `google.places.Autocomplete.Javascript` | **61** |
| `places-backend` | `google.places.Details.Http` | 702 |
| `places-backend` | `google.places.NearbySearch.Http` | 15 |
| `places-backend` | `google.places.Details.Javascript` | 2 |
| `places-backend` | `google.places.FindPlaceFromText.Http` | 2 |
| `places-backend` | `google.places.Autocomplete.Http` | 1 |
| `static-maps-backend` | `google.maps.BaseMap.Http` | 3 |
| `maps-backend` | *(everything)* | **0** |

The **`.Javascript`** suffix only appears for **browser** SDK calls. Only
`stores_nearby.html` uses `libraries=places` in a browser, so those 61 calls are
definitively that page's key.

### Enabled APIs in the project

```
maps-backend.googleapis.com
places-backend.googleapis.com
places.googleapis.com
maps-android-backend.googleapis.com
monitoring.googleapis.com
cloudbilling.googleapis.com
```

---

## 2. Where the daily cap lives (the page that was hard to find)

There are **two different quota pages**, and the one that matters for the
"daily request quota" error is the **Quotas & System Limits** page, **not** the
Maps Platform "Quotas" page:

**The one you want:**

```
https://console.cloud.google.com/iam-admin/quotas/list
  ?location=global
  &metric=places-backend.googleapis.com%2Fbillable_default
  &service=places-backend.googleapis.com
  &project=get-data-io
```

On that page, the row is:

| Quota | Value | Notes |
|---|---|---|
| **Places API Requests per day** | **200** (was 100) | Adjustable — this is the one that throws the error |
| Places API Requests per minute | 6,000 | Non-issue |
| Places API Requests per minute per user | Unlimited | Non-issue |

Also reachable by browsing Quotas & System Limits and typing
`places-backend.googleapis.com` in the filter box.

### Related console pages

| Page | URL suffix (append to `console.cloud.google.com`) |
|---|---|
| Billing linkage (**check this first** on any quota error) | `/billing/linkedaccount?project=get-data-io` |
| API keys + restrictions | `/apis/credentials?project=get-data-io` |
| Budgets + alert thresholds | `/billing/budgets` |
| Maps Platform metrics (live) | `/google/maps-apis/metrics?project=get-data-io` |
| API error breakdown by type | `/apis/dashboard?project=get-data-io` |

---

## 3. Reading the error message correctly

```
You have exceeded your daily request quota for this API. If you did not set a custom
 daily request quota, verify your project has an active billing account: g.co/dev/maps-no-account
```

Google uses **one error string for two different causes**:

1. **An actual custom daily cap was hit** (was the case here: 100/day, 108 used → 54%).
2. **The project has no linked billing account** — hence the `g.co/dev/maps-no-account` hint.

So: check **billing linkage first**, then the daily cap. Don't assume overage from
the wording alone — the previous month's usage here was ~100/day against a 100 cap,
which is why it tripped daily at an arbitrary point in the day.

**A billing *budget* is not a cap.** A budget only sends alert emails; it never blocks
traffic. If someone remembers "setting a limit on the budget", that is not what stops
requests — the **Quotas & System Limits** daily cap is.

---

## 4. What actually burns the quota (~100/day)

### The driver: `hit_list_enrich_contact.py`

```
workflow   .github/workflows/hit_list_enrich_contact.yml
schedule   cron: "35 * * * *"   (hourly at :35 UTC)
script     scripts/hit_list_enrich_contact.py
cache PAT  PLACES_CACHE_PAT is present in the workflow env: block  (good — see PR #99)
invocation python3 scripts/hit_list_enrich_contact.py --limit "$LIMIT"
           ($LIMIT = 10 on cron; --fill-gaps-limit is NOT passed)
budget     --limit 10, and --fill-gaps-limit falls back to its argparse DEFAULT of 20
```

**The fingerprint that proves it.** Hourly `Details.Http` over a 3-day window showed
isolated bursts, not 24 even ticks:

```
2026-10-23T14:00   60   ############################################################
2026-10-23T19:00   29
2026-10-24T13:00    8
2026-10-24T15:00   60   ############################################################
2026-10-25T07:00   30
2026-10-25T13:00   62   ############################################################
2026-10-25T20:00   30
2026-10-25T23:00    2
```

**30 = `--limit 10` + fill-gaps `20` (the default).** The hourly cron runs 24×/day but
only spends calls when rows are queued to enrich, so cost arrives in 30–60 bursts, 2–3
per day. The **60** bursts are the other branch of the same loop — see below.

### The attempt cap is the real ceiling (and the real gotcha)

```python
fill_cap         = args.fill_gaps_limit      # default 20
fill_attempt_cap = max(fill_cap * 3, 50)     # <-- the max(..., 50) FLOOR
```

`fill_attempt_cap` bounds how many rows the sweep will *scan* looking for fillable ones.
Because of the `max(..., 50)` floor, **lowering `--fill-gaps-limit` changes very little**:

| `--fill-gaps-limit` | `fill_cap` | `fill_attempt_cap` | worst-case live calls/run |
|---|---|---|---|
| 50 | 50 | 150 | ~160 |
| **20 (current default)** | **20** | **50** | **~60** |
| 10 | 10 | 50 (floor) | ~60 |
| 5 | 5 | 50 (floor) | ~60 |
| 0 (`--no-fill-gaps`) | 0 | sweep disabled | ~10 |

So the two observed burst sizes are the two branches of one loop: **30** = 10 contact rows
+ 20 fills (clean run); **60** = 10 contact rows + 50 attempts (many rows scanned).
**To actually bound spend you must change the `max(..., 50)` floor**, not just the flag.

### What the cache does and does not absorb

The cache **is** working — `TrueSightDAO/places-cache` received 23 commits in the two weeks
to 2026-10-25, latest push `2026-10-25T12:58Z`.

Crucially, `--resolve-missing-place-id` is **OFF by default**, so the fill sweep **skips**
rows with no `place_id` (`fill_skipped += 1; continue`) instead of resolving them. The sweep
therefore only touches rows that **already** have a `place_id` — and those **are**
cache-absorbable. So the cache does help here.

Residual live spend is the ~10 contact-enrich rows (website/contact work, not always
cacheable) plus the attempt-cap scan overhead. This is **not** a structural cache-miss
problem — the cache design is sound.

---

## 5. The two browser API keys in the DApp

Both are embedded in HTML (normal and unavoidable for the Maps JS SDK) and both are
**HTTP-referrer restricted** — server-side use is rejected with
`API keys with referer restrictions cannot be used with this API`.

| Key (prefix) | File | Purpose |
|---|---|---|
| `AIzaSyBWmnvj…zWe4` | `stores_nearby.html:46` | Maps JS + `libraries=places` (Autocomplete) |
| `AIzaSyCS5tz9…` | `shipping_planner.html:54` | Maps JS (shipping planner) |

Introduced `AIzaSyBWmnvj…zWe4` in commit `bceef5c1` (2025-11-08, Zhiwen Teh).

**Place was compromised/reviewed**: do not paste full key values into context docs;
read them from the repo file if needed.

### Restriction hygiene

Referrer restriction is the only protection on a public browser key. Recommended on
each key:

- **Application restrictions** → Websites → list the exact origins (`dapp.truesight.me`).
- **API restrictions** → Restrict key → only `Maps JavaScript API` + `Places API`.

---

## 6. Diagnostic recipe (copy-paste)

Needs `google-auth` + `google-api-python-client` (both present on the autopilot box).

```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta

creds = Credentials.from_service_account_file(
    '/home/ubuntu/creds/google_credentials.json',
    scopes=['https://www.googleapis.com/auth/monitoring.read'])
mon = build('monitoring', 'v3', credentials=creds, cache_discovery=False)

now = datetime.now(timezone.utc); start = now - timedelta(days=7)
resp = mon.projects().timeSeries().list(
    name='projects/get-data-io',
    filter='metric.type="serviceruntime.googleapis.com/api/request_count"',
    interval_startTime=start.isoformat(),
    interval_endTime=now.isoformat(),
    aggregation_alignmentPeriod='86400s',   # '3600s' to fingerprint a cron
    aggregation_perSeriesAligner='ALIGN_SUM',
).execute()

for s in resp.get('timeSeries', []) or []:
    lbl = s.get('resource', {}).get('labels', {}) or {}
    total = sum(int(p.get('value', {}).get('int64Value') or 0) for p in s.get('points', []))
    print(f"{total:>8}  {lbl.get('service')} :: {lbl.get('method')}")
```

**Interpreting it:** group by `method`;
- `.Javascript` suffixes = browser (SDK) traffic — a human on a page.
- `.Http` suffixes = server-side — a script/cron.
- Use `aggregation_alignmentPeriod='3600s'` and look for **bursts** (a batch size)
  versus **even ticks** (an every-run job) to identify the caller.

### What the service account CANNOT read (don't waste time)

| Attempt | Result | Fix if ever needed |
|---|---|---|
| `apikeys.googleapis.com` (key restrictions) | **403** — API not enabled in project | Enable API Keys API in `get-data-io` |
| `cloudbilling.googleapis.com/v1/billingAccounts` | **200 but empty list** | Grant SA `roles/billing.viewer` **on the billing account** (project IAM is not enough) |
| `serviceusage .../consumerQuotaMetrics` | **404** HTML — wrong host/path | Use the console Quotas page (section 2); the API path is `serviceusage.googleapis.com/v1/...` on the **service**, not the metric |

---

## 7. Known defects worth fixing

1. **`stores_nearby.html` fails hard, not gracefully.** There is no
   `window.gm_authFailure` handler, and store-card rendering is gated behind the Maps
   callback (`onGoogleMapsReady` → `loadStoresForBounds()`, which needs map bounds).
   When the key fails, members get a blank page plus a console error instead of a list.
   Add `gm_authFailure` + a non-map fallback list.
2. **`maps-backend` has zero traffic.** The dynamic map never renders — only the
   Autocomplete widgets work. Worth confirming that's expected (the page may be
   effectively a search list already).
3. **100/day cap was the binding constraint.** With a backfill backlog, the cap will be
   hit again. Either raise it deliberately or bound `--fill-gaps-limit` so daily spend is
   predictable.

---

## 8. Quick reference card

```
PROJECT           get-data-io  (667737028020)
DAILY CAP         Quotas & System Limits -> places-backend.googleapis.com/billable_default
                  2026-10-26: 100 -> 200
DIALOG ERROR      "exceeded your daily request quota" = cap OR unlinked billing
NOT A CAP         Cloud Billing *budget* = email alerts only
DAILY DRIVER      scripts/hit_list_enrich_contact.py  (cron :35 hourly, 10 + 50 gaps)
CACHE REPO        TrueSightDAO/places-cache
BROWSER KEY       stores_nearby.html:46 (referrer-restricted, browser-only)
MAP TILES         maps-backend = 0 requests -> map never renders
```
