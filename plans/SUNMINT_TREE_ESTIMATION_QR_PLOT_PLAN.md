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
  (QR CODE REGISTRATION events gain a `plot_id` field)? → **RESOLVED 2026-10-14** (per-**pseudo-tree**
  QRs); see **§8 Addendum** below and `plans/SUNMINT_PSEUDO_TREE_QR_PLAN.md`. `plot_id` is still
  carried on the QR row (SCHEMA.md col AC `Linked Plot ID`), so plot-level association is retained as
  the fallback.
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
- `plans/SUNMINT_PSEUDO_TREE_QR_PLAN.md` — the pseudo-tree design that answers D3 (2026-10-14)
- U3 (live) — `expected_trees` + `expected_trees_source` on the `SunMint Plots` tab (col T), governor-editable

---

## 8. Addendum (2026-10-14) — D3 answered: pseudo-tree slots as the QR binding target

**Why this addendum.** D3 asked whether NEW bag QRs bind to the **plot** or to individual trees. The
2026-09-08 leaning was plot-level, *because per-tree photography doesn't scale* (§1). On 2026-10-14
Governor Gary extended the model: bind a QR to an individual, QR-codable **pseudo tree** — a **third
option** between per-plot and per-real-tree. This closes D3; the full design lives in
`plans/SUNMINT_PSEUDO_TREE_QR_PLAN.md` (v2).

**Resolution of D3 — the QR binding target is a pseudo-tree slot.**

- A **pseudo tree** is a **placeholder slot** for a tree the estimator expects but which has **not been
  photographed or located**. Physically it is a `SunMint Tree Planting`-shaped row with **blank
  Latitude/Longitude** and **no photo**, `plot_id` set, and a stable id.
- **id** `PS-<plot_id>-<seq>`; **discriminator = blank K/L** (a real submission always has a
  GPS-tagged position). **No new column needed** — blank K/L *is* "not yet individually verified," and
  is more honest than a fabricated map point.
- **No geometry is computed.** The plot's density rule (§4b: `plot_hectares × 1,100`, ~3 m spacing)
  now supplies only the **count** `expected_trees` (U3), not positions. Pseudo slots carry no
  coordinates, so their map geometry is `null`. NB: `build_tree_geojson.py` does **not** currently
  drop blank-coordinate rows (it emits `geometry: null`); the builder must be taught to skip
  blank-K/L rows from the tree index (PR2), so placeholders never surface as map features.
- **Link timing (Gary, 2026-10-14): a QR MAY be bound to a pseudo slot BEFORE any real tree exists.**
  The binding does not wait for a `[TREE PLANTING EVENT]`; the slot is minted on demand at link time to
  receive the QR, and a real tree later promotes it **in place** (§6 of the pseudo-tree plan). This is why the slot
  must be a first-class link target with no tree behind it.
- **Link event** = **reuse/extend `[TREE PLANTING LINK EVENT]`** (same atomic pattern: QR row + a row +
  ledger leg), pointed at a pseudo slot — no parallel mechanism.
- **Plot-level association is retained** as the fallback: the QR row still carries `plot_id`
  (SCHEMA.md `Agroverse QR codes` col AC `Linked Plot ID`).
- **Honest state** (`GROWTH_MODEL.md` §"How to extend this model" step 4 + anti-patterns): a
  pseudo-bound bag's QR / landing page must read *"Plot X — estimated slot #N. Position not yet
  verified."*, and must **not** increment any public "trees planted" counter.
- **Promotion** (real K/L arrives) — **IN PLACE, SAME ROW** (Gary, 2026-10-14): *"once it gets assigned
  a lat and long it is no longer a pseudo tree."* Writing the real K/L (+ photo + planter) onto the
  pseudo row **makes that row the real tree** — **no second row, no `[PSEUDO TREE RECONCILE EVENT]`,
  no orphaned pseudo row.** The signed planting event that writes K/L **is** the audit trail. The row's
  **id is unchanged**; live pseudo-vs-real is decided by **blank K/L alone**. (This **supersedes** the
  earlier claim-on-arrival/FIFO idea: with in-place promotion there is **no matching step at all**,
  so no radius and no ambiguity handling.)

**Effect on this plan's open decisions:**

- **D3 → CLOSED** (2026-10-14): per-pseudo-slot QRs; `plot_id` retained as fallback.
- **D6 → RESOLVED by U3 (2026-10-14)**: tree-count now lives on the `SunMint Plots` tab, col **T
  `Expected Trees`** (governor-editable), emitted into `plots/index.geojson` as `expected_trees` +
  `expected_trees_source`. W2 is partly shipped; a separate `tree_count_tier` column remains open.
- **D4 → CLOSED (2026-10-14): ONE registry** — a pseudo tree is a `SunMint Tree Planting` row with
  blank K/L; **no separate tab**. **D7/D8 moot** (no separate row to reconcile). **D13 → resolved**:
  a real submission with no bound slot fills the **first/any open slot in its plot**. All D-decisions
  now settled — pseudo-tree plan §8 (v4).

**Sequencing:** **all D-decisions are now ruled** (Gary 2026-10-14, via Envoy) — see the pseudo-tree
plan §8 (v4). Build units (PR2–PR7) may proceed. U3's simpler editable-count part already shipped
(col T) and proceeds independently.
