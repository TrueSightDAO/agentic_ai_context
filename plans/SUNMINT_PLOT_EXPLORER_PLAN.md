# SunMint Plot Explorer — dedicated exploration surface (plan, roadmap & checklist)

> **Purpose:** give the SunMint plot/tree/media data a **dedicated exploration surface** — a
> full-viewport instrument for visualising and exploring plots, trees, boundary evidence and
> media galleries — instead of crowding the `truesight.me/sunmint` marketing page.
> Beta-first; prod promote only with explicit governor approval.
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
  only, on governor GO).

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

- **Beta-first:** all changes to `truesight_me_beta`; prod promote only after governor approval
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
