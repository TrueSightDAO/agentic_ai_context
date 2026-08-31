# Farm Media Manifests

Searchable index of raw farm media (photos + videos) ingested via FARM_MEDIA_PIPELINE.md. Each manifest is the reference layer: SHA-256, GPS, duration, YOLO objects, YouTube IDs.

| Farm | Farm ID | Manifest | Photos | Videos (YouTube) | Status |
|---|---|---|---|---|---|
| La do Sitio (Paulo) | `la-do-sitio` | [la-do-sitio.json](la-do-sitio.json) | 52/52 in `farm-media-raw/la-do-sitio/photos/` | 53/71 LIVE, 18 pending quota, 1 SOURCE_CORRUPT | v1 filed; updating as re-uploads complete |
| Cleide | `cleide` | — (in flight) | — | — | other instance |
| Santa Anna | `santa-anna-fazenda-para` | — (in flight) | — | — | other instance |
| Rancho Maranta | `rancho-maranta` | — (in flight) | — | — | other instance |

## Schema (v1.0)
- `farm_id`, `region`, `plot_ids`, `pipeline`, `objects_remap` (COCO-80 `banana` → `cacao_pods`)
- `videos[]`: `file`, `size_bytes`, `sha256`, `duration_s`, `latitude`/`longitude`, `objects[]`, `yt_id`, `status` (LIVE / PENDING_QUOTA_REUPLOAD / SOURCE_CORRUPT)
- `storage.photos_repo` — where originals live

## Updating
Manifests are machine-generated; update via Contents-API push (not hand-edit), then bump this index.