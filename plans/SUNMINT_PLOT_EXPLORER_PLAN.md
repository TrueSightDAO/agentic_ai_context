# SunMint Plot Explorer — dedicated exploration surface (plan, roadmap & checklist)

> **Purpose:** give the SunMint plot/tree/media data a **dedicated exploration surface** — a
> full-viewport instrument for visualising and exploring plots, trees, boundary evidence and
> media galleries — instead of crowding the `truesight.me/sunmint` marketing page.
> Beta-first; prod promote only after the R3 sign-off — governor, or Envoy's verified go-ahead per `sophia/SUPERVISOR_LOOP.md` §4a.
>
> **Origin:** governor request, thread 33323 (2026-09-19): *"perhaps we should have a
> dedicated surface somewhere that actually allows the visualization, exploration of the
> plots, data and images and gallery."*

## 0. Why a dedicated surface

`truesight.me/sunmint` (file `sunmint.html` in `truesight_me_beta`) is a **narrative** page:
hero, problem statement, six-part "how it works", Impact Registry table, highlights, then an
in-page Leaflet impact map. It is ~68KB of HTML and the map is one section competing with a
whole marketing story.

A plot explorer is a different kind of object — an **instrument**:

- wants the full viewport, not a 480px section;
- wants persistent, composable filters (farm, plot type, status, boundary authority);
- wants a detail pane you can *sit in* (gallery, tree list, provenance links);
- wants deep-links so any plot/farm/tree is shareable.

Bolting that onto the marketing page makes both jobs worse. **Decision: dedicated surface**,
with the marketing page's map reduced to a teaser linking through.

## 1. Surface decision (2026-09-19)

**Route + repo:** a new directory on the **existing site** — `/sunmint/plots/` served from
`truesight_me_beta` (beta: `beta.truesight.me/sunmint/plots/`) — NOT a new repo and NOT a new
domain. Rationale:

- rides the existing `truesight_me_beta` → `truesight_me_prod` `sync_beta_to_prod` promote path
  (no new deploy surface, no new CNAME, no new certificate);
- the impact map already lives in this repo and already reads these data files;
- keeps the QR-profile / farm-page / SunMint cross-link graph on one origin.

**Marketing page change:** the existing in-page impact map section becomes a **teaser** — keep
it lean (it already shows plot polygons, tree markers, a plot selector, and popups with up to 4
boundary thumbnails + a "Trees in this plot" list) and add a prominent **"Explore all plots →"**
link to `/sunmint/plots/`. Do NOT grow the marketing-page popup into a gallery (popups clip on
pan; single-instance; small).

## 2. In scope

1. **Explorer shell** — full-viewport map + left rail (plot list) + right rail (selected-plot
   detail panel). Responsive down to mobile.
2. **Filters** — by farm, plot type, plot status (proposed | planted | verified), boundary
   authority (approx | gps_walk | car | incra). Filters compose; each shows a count.
3. **Per-plot detail panel** — hectares, owner, region, verified_at, boundary authority, plot
   type, status; the **media gallery**; the tree list (joined on `plot_id`); links out to the
   QR profile, the farm profile on Agroverse, and any ledger/credential record.
4. **Per-plot media index** — a single prebuilt `plot_id → media[]` artifact so the explorer
   does ONE fetch, not an N-fetch fan-out across farm galleries.
5. **Deep-links** — `?plot=`, `?farm=`, `?tree=`, `?qr=` reusing the convention the existing map
   already supports (`impactMapGetUrlParam` / `impactMapSetUrlParam`), so any view is shareable.
6. **Marketing-page teaser** — shrink + add the "Explore all plots →" link (see §1).
7. **Data-quality surface** — filters must show explicit **"unclassified / no media / no farm"**
   states rather than silently hiding rows (see §5).

## 3. Out of scope (this plan)

- Farmer-app boundary capture UI (`sunmint_beta` — separate plan).
- Backend event schemas / sheet source-of-truth changes (SunMint Plots sheet stays canonical).
- New repos / new domains / new DNS.
- Any direct PRODUCTION repo edits (`truesight_me_prod` untouched; promote via `sync_beta_to_prod`
  only, on the R3 sign-off — governor, or Envoy's verified go-ahead per `sophia/SUPERVISOR_LOOP.md` §4a).

## 4. Data contract (all sources live)

| Source | Path | Used for |
|---|---|---|
| Plots | `sunmint/plots/index.geojson` | polygons + props (`plot_id`, `farm_id`, `name`, `hectares`, `status`, `boundary_authority`, `owner`, `region`, `verified_at`, `plot_type`, `media`) |
| Trees | `sunmint/trees/index.geojson` | tree markers + point popups (`tree_id`, `qr_code`, `species`, `status`, `plot_id`) |
| Per-plot media index | **NEW** — e.g. `sunmint/plots/media.json` (`plot_id → [{file, kind, nearest_location_id, nearest_distance_m, …}]`) | the detail-panel gallery, ONE fetch |
| Farm media manifests | `farm_media_manifests/*.json` | upstream source for the per-plot index |
| Nearest-location join | shipped in farm-media-daemon #30 | media→plot attribution (`nearest_location_id` / `nearest_distance_m`) |

**New artifact only:** the per-plot media index. Everything else is already generated.
The index is **machine-generated** (no hand-edits) — see §6.

## 5. Data-quality risks (surface them, don't hide them)

The explorer's value is bounded by registry quality. Known offenders that will look "broken"
in a surface that promises exploration:

- **Orphan plots with no `farm_id`** (e.g. `PL-005` duplicating `CR-PA-P2`) — no farm link,
  and no media source. Clean the SunMint Plots sheet row (the durable source).
- **Missing / cleared media** (e.g. `B-06-108_20260908_1`, boundary photos absent everywhere).
- **`locations_cache.json` refresh is manual** — if the explorer keys on nearest-location, a
  stale cache silently mis-attributes media. Fix the cadence or the panel goes stale.

**Rule:** filters must expose "unclassified / no media / no farm" as a *visible state*, and
counts must reconcile (per-filter count vs total). The explorer should embarrass us into
cleaning the registry.

## 6. Constraints (rules)

- **Beta-first:** all changes to `truesight_me_beta`; prod promote only after the R3 sign-off (governor, or Envoy's verified go-ahead per `sophia/SUPERVISOR_LOOP.md` §4a)
  via `sync_beta_to_prod`. UAT gate before promote.
- **ONE PR PER TURN** — execute one PR, report, stop; next unit in a fresh turn.
- **Local test suite** before pushing (compile, ruff lint, ruff format, pytest). Static HTML/JS:
  verify tags balanced + `node --check` on extracted JS where feasible.
- **Data stays machine-generated** — never hand-edit `plots/index.geojson` or the per-plot index.
- **Don't create variant plan/backlog files.**

## 6a. Freshness — the index MUST refresh on ingest (governor directive, 2026-09-19)

> **Governor directive:** *"Make sure that pre-built is updated whenever a new item is
> added to its underlying data source, otherwise it will get outdated."*

A **stale prebuilt index is worse than no index** — it silently under-reports media and makes
"uploaded but not published" (the Cacau na Veia PR6 near-miss) possible again, just one layer
deeper. So freshness is a **hard requirement of PR1**, not a follow-up.

### Mechanism — reuse the PROVEN publisher pattern, do not invent one

The `farm-media-publisher` already solves exactly this shape (verified live on the box
2026-09-19: `farm-media-publisher.timer` **active**, last run 22:32 UTC, every collection
reported `unchanged` → idempotency proven):

```
manifests / sidecars  →  idempotent reconcile (systemd timer, 15 min, Persistent=true)  →  emitted JSON
```

The per-plot index is a **second, derived stage in that same reconcile**: it reads the very
manifests the publisher just reconciled, so it **cannot lag the manifest by construction**.
Concretely, PR1 must ship:

1. **Idempotent reconcile** — regeneration writes only when content actually changes (no empty
   commits; the publisher's `unchanged` output is the reference behaviour).
2. **Timer-swept, not event-plumbed** — a periodic full reconcile is cheaper and crash-safe vs. a
   webhook chain; a missed event can't strand the index. Same 15-min cadence + `Persistent=true`.
3. **Reconcile over the FULL input set, not just manifests.** Attribution depends on plot
   geometry, so a **new/renamed plot changes attribution with no new media at all**. Inputs =
   `farm_media_manifests/*` ∪ `sunmint/plots/index.geojson` ∪ the nearest-location cache.
   A drifted `plots/index.geojson` must therefore also re-trigger the index.
4. **Freshness stamp in the artifact** — `generated_at` at index level, plus per-plot `updated`
   and the source manifest revision (sha). The explorer renders "media as of <timestamp>" so
   staleness is *visible to the user*, not just to us.
5. **Staleness monitor** — a check that alerts when index age exceeds 2× the cadence (same shape
   as the existing `df-alert.sh` / `map_drain_monitor.py` cron entries). Silent-failure is the
   enemy: a dead timer must page, not rot.
6. **CI/UAT assertion** — the PR7 UAT gate asserts index `generated_at` is newer than the newest
   input `updated`; a stale index fails UAT.

### Explicitly rejected alternatives
- **Regenerate on page load** — no: couples page latency to GitHub API, rate-limits, and can't
  be cached. A prebuilt artifact is right; it just has to be *kept* fresh.
- **Hand-refresh** — no: hand-authored link is precisely the failure mode the publisher plan
  killed on farm pages. Don't reintroduce it one layer down.
- **Webhook per daemon completion** — workable but strictly worse here; one cadence-swept
  reconciler covers manifest changes *and* plot-geometry changes that emit no media event.

> **Same argument applies to `sunmint/plots/index.geojson` itself** — if the geojson is stale, the
> explorer is stale regardless of index freshness. Its generator cadence is in scope for PR1.

## 7. Roadmap (ONE PR PER TURN)

| # | Deliverable | Repo | Depends on |
|---|---|---|---|
| **PR0** | This roadmap + handoff-manifest row | agentic_ai_context | — |
| **PR1** | Per-plot media index generator + WARN on un-attributable media + **idempotent systemd-timer reconcile (§6a)** + freshness stamp + staleness monitor | sunmint | PR0 |
| **PR2** | Explorer shell on `/sunmint/plots/` — map + left rail + detail panel, plots only | truesight_me_beta | PR1 |
| **PR3** | Filters (farm / plot type / status / boundary authority) + counts + "unclassified" states | truesight_me_beta | PR2 |
| **PR4** | Detail-panel media gallery + tree list + provenance out-links | truesight_me_beta | PR3 |
| **PR5** | Deep-links (`?plot=/?farm=/?tree=/?qr=`) + share affordance | truesight_me_beta | PR4 |
| **PR6** | Marketing-page teaser: shrink map + "Explore all plots →" link | truesight_me_beta | PR5 |
| **PR7** | **`gate: UAT`** — checklist on `beta.truesight.me/sunmint/plots/` + marketing teaser | truesight_me_beta | PR6 |
| *(post-UAT)* | Promote to prod (`sync_beta_to_prod truesight_me_prod`) **only with governor approval** | — | UAT pass |

## 7b. Phase 2 — per-plot satellite history (PR8–PR9)

> **Origin:** governor scope via Envoy, thread 33323 (2026-09-20). Build-then-cleanup order,
> so the capability is not lost mid-transition.

| # | Deliverable | Repo | Depends on |
|---|---|---|---|
| **PR8** | **Satellite history date-picker** in the plot detail panel — a slider / prev-next date stepper that swaps the displayed image for the selected plot, showing date + cloud cover | truesight_me_beta (+ `sunmint` data) | PR4 |
| **PR9** | Retire the now-redundant satellite-history widget from `sunmint.html` (marketing page) | truesight_me_beta | PR8 |
| *(post-PR9)* | Re-run UAT + promote (`sync_beta_to_prod`) on the R3 sign-off (governor, or Envoy's verified go-ahead per §4a) | — | PR9 |

### Data-source reality check (verified 2026-09-20 — constrains PR8's stated range)

Envoy's brief assumes `sunmint/satellite/manifest.json`'s `plots` key already carries the
**full historical range** per plot. **It does not, today.** Verified on the box:

- `plots` exists and **is plot-keyed** (21 plots), each with its own `bbox` + `scenes[]` —
  so PR8 can drop the marketing page's ~1° cell approximation. ✅
- BUT the generator (`sunmint/scripts/cache_satellite_scenes.py`) hard-codes
  **`DAYS_BACK = 45`** and **`MAX_SCENES_PER_CELL = 4`**, with a STAC query at
  `limit: 20` over a rolling 45-day window (cron: daily 06:30 UTC). Result: **every plot
  carries exactly 4 scenes, spanning ~2026-08-13..2026-09-18** — a rolling recent window,
  *not* the 2017→ archive Envoy measured by querying STAC directly.

**Consequence:** a date-picker built against the current manifest would step through **4
recent dates**, not "years of change". The range Envoy verified (RM-P1 earliest 2017-01-27;
first low-cloud 2017-07-11) is reachable **only by changing the generator** — raise/remove
`DAYS_BACK`, raise/lift `MAX_SCENES_PER_CELL`, and paginate the STAC query. PR8 is therefore
**not purely a UI task**: it takes a small `sunmint` pipeline change as its data dependency.

### Resolved decisions (governor, 2026-09-20 — via Envoy thread 33323)

- **Storage → commit the images into our own repo, low-cloud subset.** The governor's
  rationale is legitimacy/permanence: an external third-party bucket (`sentinel-cogs`) is
  not something we control long-term, and the whole point of pulling maximum historical
  depth is **durable evidence** — so the pixels must live in `sunmint/satellite/plot_<id>/`,
  not just be a live pointer to someone else's infrastructure. We commit the
  **cloud<20% subset**, not every scene (see the size arithmetic below).
- **`asset_url` vs committed `file` → committed local copy wins.** Today the marketing page
  reads `sc.asset_url || (raw.githubusercontent…/satellite/…)` (`sunmint.html:814`) — i.e.
  **external S3 first, local only as fallback**, the *inverse* of what we want. PR8's fetch
  logic must **prefer the committed `raw.githubusercontent.com` copy** (CORS confirmed
  `access-control-allow-origin: *`) and treat `asset_url` as an optional degraded fallback,
  if used at all.
- **Per-plot tiles:** archive start varies by Sentinel-2 tile; Envoy's 2017-01-27 is
  **RM-P1-specific**. Backfill must verify per-plot, not assume one global start date.
- **Backfill execution → a self-driving catch-up daemon, NOT a manually-dispatched one-shot
  (governor, 2026-09-20).** Instead of a human/Envoy-run `workflow_dispatch`, extend the
  **existing** cron script (`scripts/cache_satellite_scenes.py`, run by
  `.github/workflows/cache-satellite-scenes.yml`) so each run detects it has not yet reached
  full history, pulls **one rate-limited batch** toward the archive floor, and **merges** it
  into the committed `satellite/manifest.json` + `satellite/plot_<id>/`; once caught up it
  settles into the **steady-state rolling-window + merge** mode. No human trigger at any
  point — it is the existing daily-cron pattern plus a bounded catch-up phase. (This changes
  *what gets written*, not *who writes it* — initial code authorship is still gated by the
  `sunmint` `api_only_repos` restriction, below.)

### Size arithmetic (measured 2026-09-20 — pins the storage choice)

Direct earth-search STAC query for RM-P1's bbox over the full 2015→now window, projected
across 21 plots at the repo's measured ~41 KB/image:

| scope | scenes/plot | × 21 plots | projected committed size |
|---|---|---|---|
| **cloud < 20%** (the usable set) | **140** | **2,940** | **~125 MB** ✅ |
| **ALL scenes** (incl. cloudy) | 1,881 | 39,501 | ~1.67 GB ❌ |

Committing every scene (~1.7 GB) exceeds GitHub's recommended repo ceiling and is ~96%
cloudy frames nobody would step to. **The low-cloud subset (~125 MB) is the choice** — ~140
usable dates/plot spanning 2017→2026 (≈15/year, dry-season-dominated, as expected for Amazon
cloud cover). Note the *current* `satellite/` tree is already 1305 jpgs / 55 MB for a mere
45-day window, so ~125 MB for the full decade is modest.

### PR8a design — self-driving catch-up daemon (governor, 2026-09-20)

PR8a is the `sunmint` data dependency. **Design (verified against the repo on the box):**

- The workflow that runs the cache is **already** a daily cron `30 6 * * *` that commits with
  `secrets.GH_PAT_TOKEN` (`git add satellite && git commit && git push`) — so a self-driving
  catch-up needs **no new triggering mechanism**, just a changed script body.
- **State/cursor:** `satellite/manifest.json` already carries top-level `generated_at`,
  `source`, `cells`, `plots` — a per-plot (or global) `backfill_cursor` / `archive_floor`
  field can ride there so each run knows where it left off and when it has caught up.
- **Each run:** (1) if not yet at the archive floor, run a **bounded** paginated STAC query
  (`cloud_cover < 20`) reaching **backward** from the current earliest recorded date for up to
  N new scenes / M requests per plot (respect STAC + rate limits); (2) download + commit those
  jpgs into `satellite/plot_<id>/`; (3) **merge** into the manifest by date (accumulate, never
  truncate); (4) advance the cursor. Net effect: it walks back to ~2017 over successive daily
  runs, then switches to steady-state rolling-window + merge.
- **Why merge, not rebuild:** today's script **rebuilds** `manifest.json` from a `DAYS_BACK=45`
  window each run, which is exactly why history never accumulates. The catch-up requires an
  **incremental merge** path (and a `MAX_SCENES_PER_CELL` that can exceed 4).
- **Bounded and self-terminating:** the catch-up phase is finite (reaches the per-plot archive
  floor and sets a `caught_up` marker); mismatched/tile-varying floors are expected, so
  "caught up" is evaluated **per plot**.

### PR8 scope (as specified by the governor)

- Data source: `sunmint/satellite/manifest.json`'s **`plots`** key (plot-keyed, per-plot
  `bbox` + `scenes[{date, cloud_cover, asset_url, file}]`). Do **not** re-derive cell proximity.
- Full available range per plot (see the data caveat above — requires the generator change).
- **Archive the pixels, not just links:** backfill the **cloud<20% subset** of the full range
  into `sunmint/satellite/plot_<id>/` (committed), and make the manifest/PR8 fetch prefer the
  **committed local copy** over the external `sentinel-cogs` `asset_url` (see resolved
  decisions above).
- **Genuine change-over-time mechanism** (explicit requirement): a **slider or prev/next date
  stepper** that swaps the displayed image, with **date + cloud-cover shown**, so a user can
  step through and *see* change. A static thumbnail grid is **not** acceptable.
- Scoped tightly to the single selected plot's own bbox (reuse the marketing page's
  `toggleOverlay` / thumbnail-click logic, but not its cell approximation).

### PR9 scope

- Remove the satellite-history widget from `sunmint.html` once PR8 ships the real per-plot
  version. Traced: it is **not literally broken** (click updates a hidden panel + a map
  overlay), but the overlay is a ~1°-cell tile on an all-plots map — visually imperceptible
  at that zoom, so it reads as non-functional. Retire it rather than maintain two versions.

## 8. Checklist

### PR1 — per-plot media index
- [ ] Read `farm_media_manifests/*` schema + the `nearest_location_id` join fields
- [ ] Generator: join manifest items → plots via nearest-location / plot_id → `sunmint/plots/media.json`
- [ ] WARN loudly on any media item that cannot be attributed to a plot (mirror existing loud-not-silent warnings)
- [ ] **§6a:** emit `generated_at` + per-plot `updated` + source manifest sha (freshness stamp)
- [ ] **§6a:** ship + install the systemd service/timer (idempotent reconcile, 15 min, `Persistent=true`)
- [ ] **§6a:** reconcile over the full input set (manifests ∪ plots geojson ∪ nearest-location cache)
- [ ] **§6a:** prove idempotency (second run reports `unchanged`, no new commit)
- [ ] **§6a:** staleness monitor that alerts when index age > 2× cadence
- [ ] Run local suite; open PR, report URL

### PR2 — explorer shell
- [ ] New `truesight_me_beta/sunmint/plots/index.html` (+ reused Leaflet/CDN conventions)
- [ ] Full-viewport map, left plot rail, right detail panel
- [ ] Reuse `SATELLITE_BASEMAP` + CDN fallback pattern from `sunmint.html`
- [ ] Open PR, report URL

### PR3 — filters
- [ ] Farm / plot type / status / boundary authority filters; compose; show counts
- [ ] "Unclassified / no media / no farm" visible states
- [ ] Open PR, report URL

### PR4 — detail panel
- [ ] Media gallery (from per-plot index) with image/video handling + lazy load
- [ ] Tree list joined on `plot_id` (reuse the `__treesByPlot` join)
- [ ] Provenance out-links (QR profile, Agroverse farm profile)
- [ ] Open PR, report URL

### PR5 — deep-links
- [ ] `?plot=/?farm=/?tree=/?qr=` restore + share
- [ ] Open PR, report URL

### PR6 — marketing teaser
- [ ] Shrink the in-page map; add "Explore all plots →" link
- [ ] Open PR, report URL

### PR7 — UAT gate
- [ ] Explorer loads; map + rails render on desktop + mobile
- [ ] Filters compose correctly; counts reconcile
- [ ] Gallery + tree list populate for a plot with media; empty state is explicit
- [ ] Deep-links restore the right view
- [ ] Marketing teaser links through correctly
- [ ] **§6a freshness:** index `generated_at` is newer than the newest input `updated` (stale index FAILS UAT)
- [ ] **§6a freshness:** explorer displays the "media as of <timestamp>" stamp
- [ ] No console errors

### PR8 — per-plot satellite history date-picker
- [ ] (data) `sunmint` generator: convert to a **self-driving catch-up daemon** — per-run bounded paginated STAC (`cloud<20`) walking back to the per-plot archive floor, **merge** into `manifest.json` (never rebuild), commit jpgs via the existing daily cron + `GH_PAT_TOKEN`; settle into steady-state rolling+merge once caught up; verify per-plot start date
- [ ] (data) PR8a authorship path — `sunmint` is in `api_only_repos` (`config.py:353`): `git_push_changes`/`open_fix_pr` refuse it. Options: (1) governor authorizes a single-file Contents-API write + a dispatch to kick the first run; (2) a cloner (Envoy) opens the `sunmint` PR; (3) governor reclassifies `sunmint`'s code out of `api_only_repos`. **Awaiting governor decision.**
- [ ] (data) **Commit the cloud<20% images into `sunmint/satellite/plot_<id>/`** (not links) — one-time backfill run; keep it to the low-cloud subset (~125 MB, not ~1.7 GB)
- [ ] (data) Manifest + PR8 fetch: **prefer committed `raw.githubusercontent.com` copy**, demote `asset_url` to fallback (fixes the `sunmint.html:814` inversion)
- [ ] Detail-panel control: slider + prev/next date stepper that swaps the image, showing date + cloud cover
- [ ] Scoped to the selected plot's own bbox (no cell approximation)
- [ ] Open PR, report URL

### PR9 — retire marketing-page satellite widget
- [ ] Remove the redundant widget from `sunmint.html` (marketing page otherwise intact)
- [ ] Confirm the explorer's PR8 stepper is the single home for satellite history
- [ ] Open PR, report URL

### PR8/PR9 — post-merge gate
- [ ] Re-run UAT on `beta.truesight.me/sunmint/plots/` (stepper works; retired widget gone)
- [ ] Promote on the R3 sign-off (governor, or Envoy's verified go-ahead per §4a)

## 9. Do / Don't
- **Do** keep data machine-generated; never hand-edit geojson or the per-plot index.
- **Do** preserve the existing marketing page behaviour (plot chips, view chips, satellite toggle, CDN fallbacks).
- **Do** keep changes additive and small (one improvement per PR).
- **Don't** touch `truesight_me_prod`; don't self-promote without governor approval.
- **Don't** create variant plan/backlog files.

## 10. Related
- `plans/SUNMINT_IMPACT_MAP_EXTENSION_PLAN.md` — the in-page map this surface complements (PR0–PR4 merged; parked)
- `SUNMINT_PLOTS_REGISTRY.md` — plots registry runbook (schema, boundary tiers, seed data)
- `MEDIA_ARCHIVE_PIPELINE.md` / `CREDENTIALING_PROGRAM_PAGES.md` §6 — media manifest schema
- `sunmint/plots/index.geojson` + `scripts/build_plots_geojson.py` — data + generator
- `HANDOFF_MANIFEST.md` — this plan's row (thread 33323)
