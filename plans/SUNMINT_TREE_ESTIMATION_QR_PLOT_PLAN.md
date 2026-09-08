# SunMint: Plot-Estimation + QR↔Plot Association (evolution beyond per-tree photography)

> **Status:** active — governor decisions filed 2026-09-08 (density rule, D1=88 trees, plot
> association rule); W1 tree-batch registration in progress. Raised by Governor Gary 2026-09-07
> (thread 23226) after the La do Sitio field batch exposed that per-tree photography doesn't
> scale (phone overheated mid-run; 103 photos → ~88 unique trees = hours of walking for ONE
> plot). Builds on the **governor-confirmed SUNMINT_PLOT_FIRST_MODEL.md (2026-09-01)**. This doc
> extends it; it does not replace it.

## 1. The problem (field evidence)

- 2026-09-07 La do Sitio batch: 103 iPhone HEIC photos geotagged at the site (~-3.3899, -51.8514,
  Pará). Kinematic analysis (GPS + timestamps, 0.43 m/s median walk speed) confirms **~15 same-tree
  re-take groups → 88 unique trees** (strict 1.5 m/<10 s); conservative 73 (2.5 m/<20 s).
- Field reality: walking tree-by-tree, framing, and shooting took hours; Gary's phone **overheated
  and stopped mid-batch**. Asking every farmer to individually photograph every tree is not feasible.
- Farmers CAN walk a boundary / provide CAR-INCRA polygons / send geo-tagged media of their land.

## 2. The model (plot-first estimation)

```
Farmer surfaces plot (boundary walk / CAR / INCRA / geo-tagged media)
        │
        ▼
Plot polygon (boundary_authority tier: approx | gps_walk | car | incra)  [already in plot-first model]
        │
        ▼
Tree-count ESTIMATE per plot:
   • density sampling — farmer (or agent) counts trees on 1-2 representative transects × area
   • farmer-reported total (their count) as cross-check
   • estimator: count = density_sample × hectares; label tier: estimated | sampled | farmer-reported
        │
        ▼
QR association:
   • NEW cacao-bag QRs ↔ PLOT (not tree)
   • LEGACY tree-bound QRs: keep tree anchor, link tree → nearest plot polygon (spatial join)
        │
        ▼
Farmers submit videos/photos of the plot with GPS → auto-classified to plot
   → QR owners get updates on 'their' plot
```

## 3. Why this is sound (ties to existing context)

- `SUNMINT_PLOT_FIRST_MODEL.md` already makes **plots the capture unit** and Farm ID a later
  governor backfill. Estimation + QR-to-plot is the natural completion of that model.
- QR lineage already runs at **farm/batch level** (TRUECHAIN.md — e.g. La do Sitio = AGL8 batch),
  so plot-level association is strictly finer-grained than today, not a new liability.
- Media classification uses **container GPS** (exiftool) — no video frame decoding needed
  (SUNMINT_PLOTS_REGISTRY.md).
- Credentialing-lineage principle (GROWTH_MODEL.md): estimates are labeled `estimated`, only
  counted/verified stands claim precision. Honest state > false precision.

## 4. Evidence from this batch (seeds the estimator)

| Metric | Value | Source |
|---|---|---|
| Photos taken | 103 (102 w/ GPS) | batch EXIF |
| Unique trees (strict) | **88** | GPS+time dedup (1.5 m/<10 s) |
| Unique trees (conservative) | 73 | dedup 2.5 m/<20 s |
| Distinct spatial stands | 6 (3 dense: 64, 14, 6 trees) | eps=30 m single-linkage |
| Median nearest-neighbor spacing | **2.4-2.9 m** | tree coords |
| Stand density (walked area) | ~60-110 trees/ha | bbox division |

> Caveat: this batch is **planted agroforestry rows** (tight spacing). Reforestation density may
> differ — the estimator needs per-context calibration, never a single hardcoded constant.

## 4b. Tree-density estimation rule (governor decision, 2026-09-08)

Governor Gary set the estimation convention for NEW plots (filed 2026-09-08, thread 23226):

> **Default tree-count for a new plot = plot_hectares × 1,100 (~3 m spacing), used ONLY when
> the polygon represents planted extent and the stand is young/planted rows.** Otherwise the
> farmer-reported count is primary and the spacing model is a cross-check; when
> |farmer_report ÷ spacing_model| is outside ~0.5–2× the plot is flagged for a transect sample.
> Mature / cabruca / native / explicitly-numbered plots are never auto-estimated.
> Label tier: `spacing-estimate` | `farmer-reported` | `sampled` | `counted`.

Field evidence behind the constant (2026-09-07 La do Sitio batch):
- Farmers interviewed so far space planted trees ~3 m apart (Gary field observation; median
  nearest-neighbor of photographed trees in plot_1 = 2.1 m → 2–3 m rows, i.e. ~1,100–2,300/ha local).
- Gary confirmed the La do Sitio trees are **neatly aligned planted rows** — the 103-photo walk
  captured only ~88 unique trees of a ~0.67 ha pocket that at 3 m spacing holds far more (~700+);
  photography stopped because the **phone camera overheated**, not because the stand ended.

Guardrail (from the batch numbers): polygon area ≠ planted area. Running area × 1,100 on a
boundary-walk hull that includes buffer/gaps over-estimates (La do Sitio plot_1: 0.67 ha × 1,100
≈ 740 vs 63 trees actually walked & photographed — much of the walked hull is unplanted gaps).
Mature cabruca is the opposite failure (50–150 trees/ha real). Hence the rule applies to
**planted extent**, is cross-checked against the farmer report, and mature stands are excluded.

**Decision log 2026-09-08 (thread 23226):**
- D1 → **88** evidenced trees (strict dedup) registered for La do Sitio; each carries its photoset.
- D2 → accepted: new plots carry tiered `estimated` counts; `counted` only via a full walk.
- Tree→plot association rule (Gary): containment plot_1 → plot_2 → parent V-06-29;
  hull-edge stragglers fall back to nearest polygon (CSV `method` column documents this).

## 5. Open decisions (D1-D7)

- **D1** — Registration count for this batch: strict 88 vs conservative 73? (Recommend 88 with
  per-tree photoset kept for audit; 73 as floor.)
- **D2** — Tree-count tiers for plots: accept `estimated` for all new plots, `counted` only when
  a full walk happens? (Recommend yes; matches credentialing-lineage.)
- **D3** — QR↔plot: new bag QRs bind to plot + batch. Do we mint plot-level QR types
  (QR CODE REGISTRATION events gain a `plot_id` field)?
- **D4** — Legacy tree-QR owners: spatial-join each tree to nearest plot automatically, or
  governor-confirmed per farm? (Recommend auto-join + governor review list.)
- **D5** — Farmer field media: enforce **Document/email upload** (WhatsApp/Telegram strip EXIF) —
  already documented in SUNMINT_PLOTS_REGISTRY.md. Confirm farmers can use email/Document.
- **D6** — Where tree-count lives: SunMint Plots sheet new column (`tree_count`, `tree_count_tier`)
  vs separate tab. (Recommend column on Plots tab + regenerate plots/index.geojson props.)
- **D7** — Does 'this is the last individual-tree photo batch' apply to ALL farms, or only
  large/reforestation plots (keep per-tree for small flagship plots like RM-P1 house)?

## 6. Mapped work items (W1-W5)

- **W1** — Register this La do Sitio batch as trees (88) + anchors, per existing tree-registry
  flow (treasury-cache trees/index.geojson pattern; TREE PLANTING EVENT anchors). Requires D1.
- **W2** — Plots sheet + `build_plots_geojson.py`: add `tree_count` / `tree_count_tier` / `est_method`
  columns; emit into plots/index.geojson properties.
- **W3** — Tree→plot spatial join: script trees/index.geojson → nearest polygon in plots/index.geojson;
  write `plot_id` back onto tree features (legacy + new). Requires D4.
- **W4** — Media→plot classification: GPS-bearing farmer media matched to plot polygons; feed QR
  owner updates (parallels FBE pipeline; see SUNMINT_PLOT_FIRST_MODEL.md §4 GAS handler).
- **W5** — QR registry: add plot-level binding to QR CODE REGISTRATION (dao_protocol event schema).
  Requires D3.

## 7. Related

- `plans/SUNMINT_PLOT_FIRST_MODEL.md` (2026-09-01, governor-confirmed) — parent model
- `SUNMINT_PLOTS_REGISTRY.md` — plot schema, boundary tiers, media/EXIF guidance
- `TRUECHAIN.md` / `NOTES_tokenomics.md` — QR/batch lineage
- `SUNMINT_BOUNDARY_SUBMISSION_PLAN.md` — the roadmap plot-first refines
- Batch analysis artifacts (2026-09-07): /tmp/la_do_sitio_unique_trees_{strict,loose}.csv
- `GROWTH_MODEL.md` — credentialing-lineage principle (nothing asserted until evidenced)
