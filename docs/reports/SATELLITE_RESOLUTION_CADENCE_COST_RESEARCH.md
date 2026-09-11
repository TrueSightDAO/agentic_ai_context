# Satellite Resolution &amp; Cadence — Cost Research

**Thread:** 26145 · **Date:** 2026-09-11 · **Author:** Sophia Truesight

Sponsor-ready PDF: [`satellite_resolution_cadence_cost_report_20260911.pdf`](satellite_resolution_cadence_cost_report_20260911.pdf)

## Baseline (what we run today)

| Item | State |
|---|---|
| Source | Sentinel-2 L2A via Earth Search STAC — anonymous, free, no key |
| Refresh | Daily cron 06:30 UTC |
| Cache policy | 4 scenes/cell max, 45-day look-back |
| Grid | 0.01 deg (~1 km) cells |
| Coverage | 5 tree cells + 21 plot dirs, 104 scenes, 4.4 MB |
| Rendered asset | `preview.jpg` at 343x343 px (~10-49 KB) |
| Full tile (not stored) | 241 MB per tile |
| Basemap | Esri World Imagery + previews overlaid |

Script: `sunmint/scripts/cache_satellite_scenes.py`

## Two independent levers

| Lever | Free move | Paid move |
|---|---|---|
| Resolution | Larger render (512-1024 px) from the Copernicus Process API | PlanetScope 3 m; SkySat 50 cm tasking |
| Cadence | Raise scenes/cell (4 to 8-12), shrink grid, relax cloud filter, add Landsat + Sentinel-1 | PlanetScope near-daily; on-demand tasking |

## Pricing

| Option | Resolution / cadence | Cost |
|---|---|---|
| Sentinel-2 (current) | 10 m / ~5 d | $0 |
| Copernicus Data Space (Sentinel Hub) | 10 m / ~5 d | Free tier 10,000 PU/month; commercial by quote |
| Sentinel-1 radar + Landsat 8/9 | 10 m / 30 m | $0 |
| Planet Agriculture | 3 m / near-daily | $1.80 / $0.85 / $0.35 per ha/yr, 500 ha min, annual |
| Planet Monitoring (AUM) | 3 m / near-daily | $9,650/yr (50 km2); $2,700/yr (189 loc); $5,100/yr (49); $9,650/yr (17) |
| Planet Tropical Forest Observatory | 4.77 m / monthly | Quote only (NICFI free program ended Apr 2025) |
| Planet Nonprofit Program | as above | Tiered, quote only |
| SkySat 50 cm tasking | 0.5 m / on demand | ~$1,212/km2, 25 km2 min (~$30k); resellers $15k tasking / $5k archive min |

## Cost at scale

| Footprint | Tier 1 ($1.80/ha) | Tier 2 ($0.85/ha) | Tier 3 ($0.35/ha) |
|---|---|---|---|
| 273 ha (current) | ~$900/yr | ~$425/yr | ~$175/yr |
| 10,000 ha (mission target) | ~$18,000/yr | ~$8,500/yr | ~$3,500/yr |

## Defect found during review

Esri World Imagery returns a **blank tile at zoom 18 and above** over the pilot plots (2,521 bytes vs 17,267 bytes for San Francisco at the same zoom) — the basemap goes empty exactly at the zoom needed to inspect canopies. Worth a follow-up independent of any purchase.

## Recommendation

1. **Free first:** ship a CDSE Sentinel Hub renderer (512-1024 px true-color + NDVI) on the free 10,000 PU/month tier, and fix the z>=18 basemap gap.
2. **Then quote:** Planet Agriculture at the 500 ha minimum + Nonprofit Program; ask about Tropical Forest Observatory.
3. **Exclude 50 cm tasking** from routine budgets — per-collect product, not continuous monitoring.

## Caveat

Planet's pricing page is bot-blocked. Per-ha and AUM figures are search-derived and **indicative, not quoted**. A formal sales quote is required.
