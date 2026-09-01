# SunMint Plot-First Model — farmer submissions create plots, farm link is governor backfill

> **Status:** governor-confirmed 2026-09-01 (thread 11074). Supersedes the farm-first
> interpretation of `SUNMINT_BOUNDARY_SUBMISSION_PLAN.md` rule 4 for NEW submissions.
> The 5 existing governance-defined plots (RM-P1, RM-P2, SA-P1, CL-P1, LD-P1) keep their
> farm associations; only NEW farmer submissions flow plot-first.

## 1. The model

```
Farmer captures → Farm Boundary Evidence tab (raw, immutable)
                    │  auto (GAS handler)
                    ▼
               SunMint Plots tab (plot row: Plot ID auto, Plot Name = farmer text, Farm ID EMPTY)
                    │  governor backfill — only when the farm story is earned
                    │  (site visit, FSVP verification, hectares reconcile, boundary authority upgrade)
                    ▼
               Farm story: owner / region / hectares / authority / verified_at
                    ▼
               farms/index.json + plots/index.geojson (regenerated) → map + dropdown + farm profile link
```

## 2. Why plot-first (governor rationale)

1. **Farmers produce plots, not farms.** The capture flow is "this is MY land, the area I walked" —
   a plot. Forcing farm-entity creation (slug, owner, region, farms index) into the farmer flow is
   DAO governance machinery misplaced in the capture step.
2. **FSVP is the farm gate.** A farm becomes a *listable profile* only after FDA FSVP verification
   (supplier verification, site visit, video evidence — see `fda_fsvp/` + `AGROVERSE_FARM_PAGE_CONVENTIONS.md`;
   e.g. Paulo's La do Sitio has FSVP site code V-06-29). Empty Farm ID = "not yet verified/listable"
   is the honest state, not a bug.
3. **The map already implements it.** `truesight_me_beta/sunmint.html` lines 670-673: the
   "View farm profile on Agroverse ↗" link renders only `if (fid)` — empty Farm ID → no link, no error.
   Zero map changes needed.
4. **Credentialing-lineage principle** (GROWTH_MODEL.md): nothing is asserted until evidenced.
   The farm story is built only when the evidence (walk/CAR/INCRA, FSVP docs) justifies it.

## 3. The 3-table association (as it works now)

| Tab | Role | Key | Written by |
|---|---|---|---|
| **Farm Boundary Evidence** | Raw submission log (immutable) | Telegram/Edgar Update ID | FBE GAS handler (append-only) |
| **SunMint Plots** | Plot registry | **Plot ID** (auto-generated for new farmer submissions) | FBE GAS handler (`fbeUpsertFarm_`) |
| **SunMint Registered Farms** | (dead tab today — wrong schema, 0 rows) | Farm ID | nothing — park or repurpose for governor-mapped farms |

Join path: **Evidence.PlotID → Plots.PlotID**; **Plots.FarmID → (backfill) → Farm story → farms/index.json**.

> Note: the old `SunMint Registered Farms` tab has a copy-paste schema from another system
> (Telegram Update/Chatroom/File IDs) and zero rows — it is NOT part of the pipeline. Either park it
> or repurpose it as the governor-mapped farm registry (recommended).

## 4. GAS changes needed (process_farm_boundary_evidence.gs)

Current `fbeUpsertFarm_` (lines 163-225) keys rows by **Plot ID then Farm ID slug**, and on create
writes **Farm ID = farmSlug** + Plot Name = farmName. Plot-first changes:

1. **Auto-generate Plot ID when none supplied** — `PL-<seq>` (e.g. `PL-001`, `PL-002`) or
   contributor-scoped (`<initials>-P<n>`). Keep existing governance IDs (RM-P1…) untouched.
2. **Farm ID left EMPTY on create** — do NOT write farmSlug into the Farm ID column for new farmer
   submissions. (Keep slug derivation only as a *dedup hint* for matching, not as a stored value.)
3. **Plot Name = farmer's typed text** (already the behavior — `newRow[nameCol] = farmName`).
4. **Status = `proposed`, Boundary Authority = `approx`** (already the behavior).
5. Keep Evidence-tab append + tracking-tab append as-is (immutable trail).

## 5. Python builder changes (sunmint/scripts/)

- **`build_plots_geojson.py`** — already tolerant: `farm_id: cell(...) or None` (line 155).
  New plots with empty Farm ID produce `"farm_id": null` features. **No change required** — verify
  the impact map handles `null` farm_id (it does: `props.farm_id || ''` → `if (fid)` fails → no link).
- **`build_farms_index.py`** — **must skip rows with empty Farm ID** (today it would emit
  `farm_id: ''` entries, polluting the dropdown seed). Change: in `load_farms()`, `if not fid: continue`.
  (Line ~94: `fid = cell(row, cols["farm_id"])` → add empty-skip.)

## 6. GitHub Actions changes (sunmint/.github/workflows/)

`rebuild-plots-index.yml` **already exists** and runs BOTH builders (`build_plots_geojson.py` +
`build_farms_index.py`) on a daily cron + `repository_dispatch: types: [plots-index-rebuild]` +
manual trigger. Findings:

1. **The repository_dispatch hook is declared but NEVER wired** — neither GAS handler
   (`process_farm_boundary_evidence.gs`, `process_media_retraction.gs`) pings it. So after a farmer
   submission processes, the indexes DON'T rebuild until the daily cron. **Fix: add a dispatch ping**
   (UrlFetchApp → `POST repos/TrueSightDAO/sunmint/dispatches` with `event_type: plots-index-rebuild`,
   `Accept: application/vnd.github+json`, using a stored GH PAT in Script Properties) at the end of
   both handlers' processing loop (only when something changed).
2. **Farms index skip** — after the builder change (§5), the workflow needs no extra step; the builder
   handles it. The commit step already only commits when `git diff --cached` is non-empty.
3. **Permissions** — workflow uses `GH_PAT_TOKEN` + `GOOGLE_SERVICE_ACCOUNT_JSON` secrets (both set).
   The GAS-side dispatch needs its own GH PAT secret in Script Properties (different scope than the
   workflow's).

## 7. Governor backfill workflow (association, later)

When enough evidence exists to construct the farm story (FSVP verification, site visit, hectares
reconcile, boundary authority upgrade):

1. **Edit the Plots tab**: set the plot's **Farm ID** to the farm slug (e.g. `rancho-maranta`).
2. **Add the farm story** (owner/region/etc.) — either in the Plots row or a governor-mapped
   `SunMint Registered Farms` tab (if repurposed).
3. **Update `FARM_SLUG` map** in `truesight_me_beta/sunmint.html` (line 671) if the pretty
   agroverse.shop URL differs from the farm_id — else the link falls back to raw farm_id (may 404).
4. **Regenerate** — daily cron picks it up, or trigger `plots-index-rebuild` manually.
5. The impact map farm-profile link appears organically (`if (fid)` now true).

## 8. Open decisions

- Plot ID scheme: `PL-<seq>` vs contributor-scoped. Default proposal: `PL-<seq>` (globally unique,
  simple).
- Duplicate-plot handling: same farmer walks twice → two rows (accept for now; consolidate in the
  farm story later) vs GPS-cluster dedup (defer).
- `SunMint Registered Farms` tab: park vs repurpose as governor-mapped registry (recommend repurpose).
- UI label: rename `Farm:` → `Plot:` (or "Área") in the limits app (sunmint_beta).

## 9. Related

- `SUNMINT_BOUNDARY_SUBMISSION_PLAN.md` — the roadmap this model refines (rule 4)
- `SUNMINT_PLOTS_REGISTRY.md` — runbook (schema, boundary tiers, seed data)
- `SUNMINT_MEDIA_INVALIDATION_DESIGN.md` — retraction/soft-invalidate design
- `truesight_me_beta/sunmint.html` — impact map (`if (fid)` farm-link guard)
