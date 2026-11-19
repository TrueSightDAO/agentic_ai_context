## Manifest-build roadmap (thread 23018) — RESUME HERE

1. **Durable archive**: dossier + MAP namespace note → `agentic_ai_context`. ✅ (PR #970)
2. **Blob archive**: guide assets (annotated frames, badges, montage, hero, v6 PDF) →
   `farm-media-raw/rancho-maranta-para/photos/`. ✅ (10 files, 2026-09-09)
3. **Variety manifest**: `rancho-maranta-para.json` cacao_varieties block + per-item
   variety labels on the 4 plot-2 clips (farmer-verbatim). ✅ (commit 8927a2b)
4. **CEPOTX-office-area (Altamira) cluster**: new **`cepotx-office-altamira.json`**
   manifest in `farm_media_manifests` — 30 MOV + 2 HEIC (variety zip IMG_7830–7848 +
   sorting zip IMG_7807–7829), GPS centroid **-3.2124/-52.2328**, process-stage labels,
   S3 refs (`raw/cacao-variety-parap/`, `raw/sorting/`), registered in `index.json`
   (`entity_type: site` — first non-farm MAP manifest). ✅ (commits a0cb54d + dc47795)
5. **Dup + stray flagged**: `IMG_7830 2.MOV` (sorting) = byte-identical to `IMG_7830.MOV`
   (variety) — sha256 match, indexed once; `IMG_7654.MOV` (variety zip) cross-referenced
   to `rancho-maranta-para` (was misfiled). ✅
6. **Optional**: yt_id backfill for the 4 labelled plot-2 clips (no yt_id yet). ← remaining

### Status print (2026-09-13)

- **Rancho Maranta variety layer**: dossier ✅ · guide assets archived ✅ · manifest labelled ✅
- **CEPOTX-area cluster**: previously orphaned on S3 → now manifested as a site ✅
- **Open**: optional yt_id backfill (unit 6); audio/frames/transcript still local-only under `~/to_analyze/`
  (low priority — transcript text is captured in this dossier).
