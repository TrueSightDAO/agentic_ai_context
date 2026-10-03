# MAP intake go-live — front door + back door (farm / event zip funnel)

**Thread 30550** · Governor: Gary Teh · Filed: 2026-09-29 · Runbook: `MEDIA_ARCHIVE_PIPELINE.md` (MAP)
Config: `/opt/truesight_autopilot/media_archive_daemon_config.yaml` · Box: autopilot `i-05276b8ae82d6b88c`

## Goal

Make the Media Archives Pipeline (MAP) intake funnel **go live end-to-end** for arbitrary
dropped farm/event zips: a governor drops `*.zip` in `/media/to_process/`; the pipeline
claims it, archives every media object to the correct S3 `raw/<farm_id>/` prefix, and
promotes the zip to `/media/processed/` — **without anyone hand-typing a path**, and
**never** mis-filing a zip under the wrong `farm_id`.

Two halves, one funnel:

| | Front door | Back door (FORM 3) |
|---|---|---|
| Unit | `farm-media-intake.timer` → `farm_media_intake.py` | `farm-media-archive.service` → archive worker |
| Does | claims a **settled** `*.zip` (`/media/to_process` → `/media/processing`) | resolves each zip → its own `farm_id`, streams media **per file** to S3 `raw/<farm_id>/`, promotes zip + `.archive.json` sidecar → `/media/processed/` |
| Identity source | none (transport only) | `archive.roots[].zip_farm_ids` map in the config — **hand-edited** |
| Status | **LIVE** | **LIVE** (8 mappings wired 2026-09-30) |

## §0 — The `farm_id` register (the durable output of this thread)

The whole point of the thread was the `<zip → farm_id>` map. Mappings wired + verified
(threat: several farms **share a name across regions** — the "do not conflate" trap):

| Zip | `farm_id` | Region | Owner / coop | Plot | Evidence |
|---|---|---|---|---|---|
| `fazenda_santa_rosa.zip` | `fazenda-santa-rosa` | Uruará, **PA** | Antônio & Graça · CEPOTX **COPOPS** | `U-06-06` | zip GPS mean −3.634/−53.670; manifest `region: Uruara, Para` |
| `fazenda_dona_rosa.zip` | `fazenda-dona-rosa` | Medicilândia, **PA** | Rosa Wronscki / Dona Rosa Chocolates · **COOPOXIN** | `DR-P1` | sidecar GPS −3.4894/−52.9667; IMG 8501–8561 |
| `sao_jorge_fazenda_complete.zip` | `fazenda-sao-jorge-bahia` | **BA** | — | `SJ-P1` | — |
| `vivi_fazenda_2025.zip` | `vivi-jesus-do-deus-itacare` | Itacaré, **BA** | — | — | — |
| `santa_anna_fazenda_bahia_complete.zip` | `fazenda-santa-ana-bahia` | Uruçuca, **BA** | Chocolate Morbeck · Coopercabruca | `FSA-P1` | **mapping KEPT**, corrected prefix (see §2) |
| `itacare_pituba_samba_festival_2024.zip` | `event-media` | Itacaré, BA | (event namespace) | — | — |
| `tribo_mirim_roda_2024.zip` | `event-media` | (event namespace) | — | — | — |
| `oscar_complete.zip` | `oscar-bahia` | **BA** (Óscar/Osca) | — | — | wired 2026-09-30: 77 media (62 size-skip + 15 new), IMG 2133–2225; farm_id pre-existing in config |
| `oscar_fazenda_2026.zip` | `oscar-bahia` | **BA** (Óscar/Osca) | — | — | wired 2026-10-03 on governor word (relayed via DeepSeek Local); same farm as `oscar_complete.zip`; 12.9 GB, in flight (courier manifest) — auto-archives on arrival |

### ⚠️ Same-name traps resolved this thread (do NOT re-litigate)

- **Santa Rosa:** Gary's first label "Bahia" was **wrong**; corrected to **Pará / CEPOTX**.
  `fazenda-santa-rosa` already **is** the Pará farm (U-06-06). The zip was a **byte-identical
  duplicate** (sha256 `b6060158…`) of the `upload_zips/` copy → archive was a **size-dedupe
  no-op** (31/31 "already in S3; skip") + promote. Zero risk.
- **Dona Rosa:** confirmed a **distinct Pará farm** (Medicilândia, ~80 km from Santa Rosa) —
  an earlier "possible santa-rosa variant" flag was **retracted**.
- **Santa Anna:** **TWO farms share the name** — (A) **Pará** `santa-anna-fazenda`
  (B-06-58, Ana Lucia, CEPOTX COOPOXIN; page slug `santa-anna-fazenda-para`, S3 44 objs) and
  (B) **Bahia** `fazenda-santa-ana-bahia` (FSA-P1, Morbeck; 244 objs). `santa-anna-fazenda`
  is **NOT** a Bahia variant.

## §1 — Front door (Unit A) — LIVE

`farm_media_intake.timer` runs `farm_media_intake.py`: claims a `*.zip` from
`/media/to_process` once **`settle_seconds: 300`** has elapsed since last modification, into
`/media/processing`, guarded by **`min_free_gb: 20`**; ledger at
`farm_media_intake_ledger.json`; enumerates `*.zip` only.

## §2 — Back door (FORM 3, Units D/E) — LIVE

`archive.roots[].zip_farm_ids` (config lines ~320–346) maps each claimed zip → its own
`farm_id`. **A zip ABSENT from the map is SKIPPED with a warning — never mis-filed**
(fail-closed is deliberate: the destination prefix is irreversible). Videos archive to
`raw/<farm_id>/`; **stills are never sent to S3** (video-only extensions on this root);
once every media entry is recorded, the zip **and** its `.archive.json` sidecar move to
`/media/processed/`.

**Bahia consolidation (2026-09-29, Option A — governor GO):** the Bahia farm's 244 raw
objects (+151 previews) lived under a **non-canonical** S3 prefix
`raw/santa-ana-fazenda-bahia/` while the manifest/page/`farm_id` said
`fazenda-santa-ana-bahia`. Fixed by **server-side `copy_object`** (0 re-download):
`244/244` raw + `151/151` previews copied, **content sha256 verified** (120 apparent ETag
diffs were a multipart-vs-single-part artifact, **not** content), then the **one**
archive-root `farm_id` was flipped forward. The **old prefix was retained** as a rollback,
then **pruned** (244 + 151 deleted) on a separate governor GO after a pre-prune parity
check (canonical complete, 0 missing). Bucket is **unversioned** — the prune was a real,
non-recoverable delete, done only after verification.

**Truncated zip quarantined:** `/media/processing/santa_anna_fazenda_bahia_complete.zip`
(2.25 GB) was **truncated** (`BadZipFile`; DEFLATE + data-descriptor, unrecoverable past
the cut) and looped a harmless `bad zip` warning every 30 s. Its content was **already
fully archived** (the 244 Bahia objs), so it was **moved** (not deleted) to
`/media/quarantine/` + a `README.md` (hash, reason, restore cmd). The map entry was
**kept** (annotated) so a future good re-upload auto-archives idempotently.

## §3 — State (verified 2026-09-29)

- Services: `farm-media-intake.timer`, `farm-media-archive.service`,
  `farm-media-publisher.timer`, `farm-media-daemon.service` — **all active**.
- `/media/processed/`: **7 zips + 7 sidecars** (as of 2026-09-30). `/media/to_process/`,
  `/media/processing/`: **empty**. `/media/quarantine/`: the bad zip + README.
- Disk: `/` 62 % (96 G/155 G), `/media` 37 % (86 G/246 G).

## §4 — Remaining / RESUME HERE

1. **Intake context card** — the one real product gap (filed in `OPEN_FOLLOWUPS.md`,
   "MAP intake has no per-zip context channel"): identity arrives out-of-band in chat and a
   zip that never gets context **stalls invisibly**. Design = a sibling
   `foo.zip.context.json` dropped with the zip (inert to the claimer; travels the funnel)
   + a **fail-visible** hold. **Not yet built.**
2. **Never wire `/media/quarantine/` as an intake/archive root** — it would re-loop the bad
   zip. Parking lot, not a source.

### §4.1 — source_zip provenance (landed 2026-10-03, supersedes the dated snapshot above)

- **PR #35 (farm-media-daemon, merged a381d815)** — the archive worker now records the
  origin zip filename on every media item going forward, so a single archived file is
  traceable/retrievable by name (zip), not just by S3 path.
- **PR #36 (farm-media-daemon, merged f5812905)** — the retroactive-stamp tool: backfills
  `source_zip` onto everything archived **before** #35 landed, so old and new data share
  the same schema.
- **In progress (Envoy supervising, per governor's "supervise this to completion"):**
  Sophia is running the #36 backfill tool against the live box (refreshed to merged
  `main` first). Verify once done: every archived item (old + new) carries `source_zip`;
  spot-check a pre-#35 farm (e.g. `fazenda-dona-rosa`) and a post-#35 one for the field.

### §4.2 — stills have no `source_zip` (accepted scope gap, 2026-10-03)

**Question answered (Gary, thread 30550): do stills get `source_zip` via whatever separate
path commits them to `farm-media-raw`, or is it an accepted gap?** — **No separate path
exists. It is an accepted, by-design gap: do NOT read a photo item's missing `source_zip`
as a backfill regression.**

- **Scope is org-wide, not just the 5 oscar HEICs.** Across all 15 manifests: **347 photo
  items, 347 missing `source_zip` (100%)**, while videos on zip-sourced farms are stamped.
  `oscar-bahia`'s 5 (IMG_2162/2163/2191/2192/2193, all `.HEIC`) are simply its only photos
  on a farm whose videos did get stamped — the same phenomenon as every other farm.
  (Farms with *no* `source_zip` on videos at all — e.g. `cleide`, `cacau-na-veia-pacaje` —
  were never archived from a zip, so #35/#36 correctly skipped them. Four zip-sourced farms
  carry stamped videos: `fazenda-dona-rosa`, `fazenda-santa-rosa`, `fazenda-sao-jorge-bahia`,
  `oscar-bahia`.)
- **Root cause — the archive worker never touches stills.** `farm_media_archive.py`
  `resolve_extensions()` **strips photo extensions** (`.heic/.heif/.jpg/.jpeg/.png`) off every
  root before archiving, per `MEDIA_ARCHIVE_PIPELINE.md` "**No S3 for still photos**". So the
  S3 worker writes **no** `<file>.raw.json` sidecar for a still — and both #35 (worker-side
  emit) and #36 (zip-`<zip>.archive.json` backfill) are keyed on the worker's sidecars, so
  stills are structurally outside the provenance chain. This is a **different destination**
  (`farm-media-raw` on GitHub), not a bug in the S3 worker.
- **No stills path emits it either.** There is **no org tooling** that commits stills or
  writes their provenance: org code-search for `farm-media-raw` → **0 hits**; a box-wide
  `*.HEIC.json` sidecar search → **0 real files** (only pytest temp artifacts);
  `farm-media-raw` has **no `oscar-bahia/` folder** (404). Stills are committed without any
  provenance tooling today.
- **Consequence, and what closing it would take.** A still is currently traceable only by
  farm + filename, **not** by origin zip. Closing the gap means adding a stills-specific
  `source_zip` emitter to whichever tool commits `farm-media-raw` (a stills path exists:
  `<farm-id>/photos/`) — out of scope for #35/#36. Filed here so a future session treats
  "photos missing `source_zip`" as **expected**, not a regression.

### §4.3 — Courier queue manifest = machine-readable zip identity (2026-10-04)

Gary's Mac (**TrueSight Media Courier**, launchd `com.garyjob.truesight-media-courierqueue`)
now publishes a queue manifest to `lineage-assets/media_upload_queue.json` every ~5 min
(`truesight_media_queue_publisher`). Each item carries `filename`, `size_bytes`, `sha256`
(once hashed), `status` (`queued`|`uploading`), `added_at`; the wrapper carries `generated_at`
+ `daemon_running`. Read it with `read_repo_file("lineage-assets", "media_upload_queue.json")`
to confirm a zip's **exact name + size + sha** before wiring — no more guessing from a bare
chat filename. Full pipeline: `TRUESIGHT_MEDIA_COURIER.md`.

**Mapping snapshot (2026-10-04, from that manifest):** of 12 queued zips, only **2 are
mapped** (`oscar_fazenda_2026.zip`→`oscar-bahia`, `santa_anna_fazenda_bahia_complete.zip`→
`fazenda-santa-ana-bahia`); the other **10 fail-closed skip** until wired. Notably **two CIC
zips** (`cic_20260929.zip` 3.88 GB, `cic_complete.zip` 6.07 GB) → need a `facility-cic-*` id
(open question, thread 30550); plus `santos_complete.zip`, `santa_anna_farzenda_bahia.zip`,
and four `la_do_sitio_*` patches. `cic_complete.zip` + `cacao_variety_parap.zip` are already
in `/media/to_process_staging/` (active upload).

## Gates

- NEVER deploy prod without governor GO. Beta preview first.
- S3 objects: **one per original file**, never the zip blob; skip `__MACOSX/` + `._`.
- Deletes/prefix-prunes need an **explicit** governor GO + a pre-delete parity check.
- `sunmint` + `farm-media-raw` are api-only → Contents-API writes, never branch-edit.

## RESUME HERE

**2026-10-03 (Envoy, supervising per governor's "@nelanco_claude_bot supervise this to
completion"):** §4.1's backfill run is the live unit — confirm it completes clean and
`source_zip` is verifiably present org-wide (not just claimed) before calling this done.
After that: the intake context card (§4.1) is the only remaining open item; everything
else (front door, back door, the `farm_id` register, the Bahia consolidation, the
quarantine) is live and verified. Front door + back door are **live**; the `farm_id`
register (§0) is the thread's durable artifact.
