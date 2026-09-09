# Two Cacao Varieties of Pará — Field Dossier (CCN-51 "Ponta Verde" vs common/traditional)

> Field-video verification + research dossier. Distilled 2026-09-09 from
> `Cacau_Para_Two_Varieties_Report_v6.pdf` (7 pp, on the autopilot box at
> `~/to_analyze/pdf/`) + `BRAZIL_FARMERS_ANALYSIS.md` (transcript).
> Source footage: 4 clips from Rancho Maranta plot 2, Pará
> (**IMG_7654 / IMG_7669 / IMG_7672 / IMG_7673**, ~101 s total) — a farmer-led walkthrough.

## Provenance & attestation (read first)

- Variety labels here are **farmer-attested verbatim**, not vision-model guesses. Pod
  morphology is **not** reliably diagnostic across varieties; an AI labeling "this is
  Criollo" from a photo would be fabricated provenance.
- "**Ponta Verde**" is the name the farmers use — **not** an official registry denomination.
  Most plausibly a local/biotype naming of grafted CCN-51 in Pará (green-tipped pods).
- The farmers contrast the grafted clone against "**essas outras cabaças**" / "cacau comum"
  (common cacao) with a seasonal cycle.
- Genetics note: CCN-51 is ~45.4% IMC, 22.2% Criollo, 21.5% Amelonado, 1.1% Nacional, …
  — essentially a **forastero-dominant hybrid**; the industry classes it as bulk cacao.

## Farmer verbatim (PT + EN, from the clips)

| Clip | PT | EN |
|---|---|---|
| IMG_7654 — naming the variety | "Diferente, é. É esse aí. CCN-51 Ponta Verde." | "Different, yeah. That's the one. CCN-51 Ponta Verde." |
| IMG_7669 — year-round fruiting | "…essas outras cabaças lá tá encerrando, mas esse aqui… é o ano todo… sempre tem fruto, tá madurando, tá colhendo." | "…those other pods are finishing, but this one… all year… always has fruit, ripening, harvesting." |
| IMG_7672 — pest vs disease | "Dois tipos de problemas… praga (inseto: suga/deixa toxina)… lá geralmente são fungos. É inseto e fungos." | "Two problem types — pest (insect: sucks/toxin)… over there usually fungi." |
| IMG_7673 — grafting | "…ela foi enxertada, não foi plantada de semente… não tem um ciclo que finaliza igual o cacau comum, que tem um período que não tem fruto nenhum… sempre vai ter frutos… todo o ano." | "…it was grafted, not seed-planted… no cycle that ends like common cacao (fruitless period)… always fruits all year." |

## Colour-key — how to read the photos

- **Variety A — CCN-51 "Ponta Verde" (grafted):** smooth pods, shallow ribbing, blunt tip,
  yellow when ripe, fruits all year.
- **Variety B — common / traditional cacao:** deeply furrowed (8–10 ridges), pointed tip,
  red-purple when ripe, seasonal.

## Verified field comparison (from the v6 guide)

| Trait | A — CCN-51 "Ponta Verde" (grafted) | B — common / traditional |
|---|---|---|
| Pod surface | Smooth, very shallow ribbing | Deeply furrowed, 8–10 pronounced ridges |
| Pod tip | Blunt / rounded | Distinctly pointed |
| Ripe colour | Bright yellow (occ. black basal patch) | Orange-red → crimson-purple |
| Pod size | Large (~15–18 cm) | Slightly smaller, more elongate |
| Fruiting rhythm | Year-round — pods at every stage any visit | Strongly seasonal — waves, fruitless period |
| Propagation | Grafted clone (enxertia de duas plantas) | Seed-planted (traditional / forastero-type) |
| Farmer's words | "sempre vai ter frutos… durante todo o ano" | "um período que não tem fruto nenhum" |

## Where the media lives (MAP) + roadmap status (2026-09-09)

| Asset | Location | Indexed? |
|---|---|---|
| Source MOVs IMG_7654/7669/7672/7673 | Rancho Maranta plot 2 (`rancho_maranta_plot_2.zip`); S3 `raw/`; in `rancho-maranta-para.json` plot2 entries, GPS ≈ -3.294/-52.578 | ✅ in-place + **variety-labelled** (commit 8927a2b) |
| Same clips (" 2" dups) | `to analyze.zip` → S3 `raw/to-analyze/` | dup set, flagged |
| Audio (16 kHz WAV ×4) | `~/to_analyze/audio/` | ❌ local only |
| Frames (lo + hi-res) | `~/to_analyze/frames/`, `~/to_analyze/hi_frames/` | ❌ local only |
| Farmer transcript | `~/to_analyze/BRAZIL_FARMERS_ANALYSIS.md` | ❌ local only |
| **Guide assets (badges, annotated frames, montage, hero, v6 PDF)** | **`farm-media-raw/rancho-maranta-para/photos/`** (2026-09-09) | ✅ **archived** |
| Dossier PDF v1–v5 | `~/to_analyze/pdf/` | superseded by v6 |

## Manifest-build roadmap (thread 23018) — RESUME HERE

1. **Durable archive**: dossier + MAP namespace note → `agentic_ai_context`. ✅ (PR #970)
2. **Blob archive**: guide assets (annotated frames, badges, montage, hero, v6 PDF) →
   `farm-media-raw/rancho-maranta-para/photos/`. ✅ (2026-09-09, 10 files)
3. **Variety manifest**: `rancho-maranta-para.json` cacao_varieties block + per-item
   variety labels on the 4 plot-2 clips (farmer-verbatim). ✅ (commit 8927a2b)
4. **CEPOTX-office-area (Altamira) cluster**: `cacao_variety_parap.zip` IMG_7830–7848 +
   `sorting.zip` IMG_7807–7829 (S3 `raw/cacao-variety-parap/`, `raw/sorting/`) — unindexed
   orphans; frame-captioned already (process stage, not variety); propose a
   `cepotx-office-altamira` manifest. ← NEXT
5. **Loose end**: `IMG_7830 2` (sorting) is byte-identical to `IMG_7830` (variety) — flag,
   don't double-index.
6. **Optional**: yt_id backfill for the 4 labelled plot-2 clips (no yt_id yet).
