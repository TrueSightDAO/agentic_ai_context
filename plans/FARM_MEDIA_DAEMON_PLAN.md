# Farm Media Daemon — shared YouTube upload pipeline: implementation plan, roadmap & UAT

> **Purpose:** one shared, dumb-on-purpose background daemon that uploads farm videos to
> YouTube for ALL farms, under one shared daily-quota budget with round-robin fairness, so no
> single farm (or Sophia instance) can starve the others or blow the quota. Metadata travels
> WITH each file (sidecar), the queue is plain files on disk, and **GitHub is the committed
> source of truth** — any Sophia, in any thread, can read the manifests and answer "what's
> uploaded / pending / committed", and can perform the manifest commit. The governor can
> query ANY Sophia for assets across farms.
>
> Origin: Gary, thread 17181 (2026-09-01), after Cleide's upload chain stalled on the YouTube
> daily 429 quota (La do Sitio's 71 uploads consumed the day's cap on project 323153649224).

## 1. Governor design rules (confirmed 2026-09-01, thread 17181)

1. **Metadata travels with the file** — each video lands in the inbox with a `<file>.mp4.json`
   sidecar carrying everything upstream already computed (sha256, GPS, objects, duration,
   title, description, farm_id, produced_by, generated). The daemon never regenerates,
   never looks up, never infers — it reads the sidecar, uploads, writes `yt_id` back, and
   moves on. Incomplete sidecar → mark `needs_metadata`, skip; it never guesses.
2. **Queue = the inbox** — pending files have no `yt_id`; done files have one; failed files
   have an `error` field. Any software can read the queue by listing the inbox.
3. **Daemon never touches GitHub** — it edits only the sidecar it is working on, atomically.
   No shared mutable state, no lock contention, no corruption across multiple Sophias.
4. **GitHub is the committed state** — `FARM_MEDIA_MANIFESTS/<farm_id>.json` (each video's
   `yt_id` → watch URL) + `index.json` (directory across farms). Committing is a deliberate,
   separate step so repo history stays readable and reviewable.
5. **Any Sophia can read state and commit** — a fresh Sophia in a new Telegram thread reads
   GitHub and answers instantly, and can run the manifest commit. Midstream handoff works.
6. **Governor queries any Sophia** — "find me cacao videos from Cleide" / "which farms have
   fermentation footage" → the Sophia reads the manifests (photos in `farm-media-raw` +
   videos in `FARM_MEDIA_MANIFESTS/`) and returns the asset list.
7. **Sidecar records provenance** — `produced_by` (which agent/pipeline) + `generated`
   timestamp, so stale/wrong metadata is traceable to its producer (lineage audit).

## 2. Current state (pre-flight facts, 2026-09-01)

| Fact | Value |
|---|---|---|
| YouTube channel | **admin@truesight.me** (TrueSight DAO channel), OAuth Desktop client, `config/youtube/` on autopilot box (gitignored) |
| Upload script | `/opt/truesight_autopilot/config/youtube/upload_video_to_youtube.py` — **no 429/quota retry** |
| Daily upload quota | Google default for unverified OAuth project (323153649224): **6 uploads/day** (verified apps: up to 100/day); resets ~midnight PT ≈ **07:00 UTC** |
| La do Sitio | 71 yt_ids already committed in `FARM_MEDIA_MANIFESTS/paulo-la-do-sitio-para.json` (consumed today's quota) |
| Cleide | 71 mp4s transcoded + GPS-fixed on box (`/home/ubuntu/cleide_work/mp4/`); throttled ad-hoc uploader PID 105025 (6/day) — **to be superseded by this daemon** |
| Manifest convention | `FARM_MEDIA_MANIFESTS/<farm_id>.json` (dict: farm_id, plots, counts, gps_coverage, items[]) + `index.json` ({"index": [...]}) — rancho/la-do-sitio/santa-anna committed (commit b3580e4) |
| Raw photos | `farm-media-raw/<farm_id>/photos/` — Cleide 14 HEIC committed |
| Current ad-hoc uploaders | Cleide throttled_uploader.py (PID 105025); La do Sitio `reupload_retry.sh` on box — **both to be retired once daemon lands** |

## 3. Constraints (rules)
- **ONE PR PER TURN** — execute one PR, report, stop; next unit in a fresh turn.
- **Local test suite** before pushing (compile, ruff lint, ruff format, pytest); scripts `node --check` where JS.
- **Singleton daemon** — PID lockfile + systemd service; ONE writer to the sidecars at a time.
- **Credentials never in the repo** — `config/youtube/*.json` stay local (gitignored); repo documents the path.
- New repo must be added to `truesight_autopilot` `allowed_repos` before `git_push_changes`/`open_fix_pr` can touch it (governor-approved PR to settings).
- No new backlog files; gaps → OPEN_FOLLOWUPS.md.
- Beta/prod: this daemon is infra on the autopilot box; the farm-page wiring stays beta-first as always.

## 4. Architecture (agreed shape)

```
farm_media_inbox/<farm_id>/
  IMG_4859.mp4
  IMG_4859.mp4.json      <- sidecar: sha256, gps, objects, duration, title, description,
                           farm_id, produced_by, generated, yt_id, error, status
```

- **Daemon** (`uploader_daemon.py`): scan inboxes → sidecar complete? → upload → write
  `yt_id` into sidecar (atomic) → next. Global daily budget (6/day), round-robin across
  farms, 429 → sleep till reset (~07:05 UTC) with retry, corrupt file → `error` + move on.
- **Queue reader** (`farm-media-queue list --farm <id>`): uploaded / pending / error state.
- **Manifest committer** (`farm-media-manifest commit <farm_id>`): aggregate sidecars →
  `FARM_MEDIA_MANIFESTS/<farm>.json` + `index.json` → PR (or direct push on explicit go).
- **systemd unit** `farm-media-daemon.service` on the autopilot box; survives reboots.
- Future: multiple YouTube projects/channels = config entries, no code change.

## 5. Roadmap (ONE PR PER TURN)

| # | Deliverable | Repo | Depends on |
|---|---|---|---|
| **PR0** | This roadmap + manifest row | agentic_ai_context | — |
| **PR1** | Repo scaffold `TrueSightDAO/farm-media-daemon` + `DESIGN.md` (queue contract, sidecar schema, fairness) + README + config.yaml template + allowed_repos entry | new repo + truesight_autopilot | PR0 |
| **PR2** | Daemon core: `uploader_daemon.py` — scan, sidecar read, upload, yt_id write-back (atomic), global daily budget, round-robin, 429 backoff, error marking | farm-media-daemon | PR1 |
| **PR3** | CLIs: `farm-media-queue list` + `farm-media-manifest commit` (+ index.json update) | farm-media-daemon | PR2 |
| **PR4** | systemd service + inbox dirs (`/home/ubuntu/farm_media_inbox/<farm_id>/`) + migrate Cleide mp4s/sidecars + retire throttled_uploader/reupload_retry | farm-media-daemon | PR3 |
| **PR5** | **`gate: UAT`** — Cleide videos upload under budget/fairness; manifest committed; fresh-Sophia query works; governor query works | all | PR4 |
| *(post-UAT)* | Docs + cross-Sophia announcement (HANDOFF/OPEN_FOLLOWUPS note) so every instance uses the daemon, not ad-hoc scripts | — | UAT pass |

## 6. Checklist

### PR1 — Scaffold + DESIGN.md
- [ ] Create `TrueSightDAO/farm-media-daemon` (**public** — Gary 2026-09-01: design is transparent, creds stay local/gitignored), description: shared farm video → YouTube upload daemon
- [ ] `DESIGN.md`: queue contract, sidecar JSON schema, daemon loop, fairness, quota budget, commit model, query patterns
- [ ] `config.yaml` template: farms/inboxes, daily cap, channel/creds path, priorities
- [ ] README: how farms register, how videos land, how manifests commit
- [ ] `allowed_repos` entry in truesight_autopilot settings (PR)

### PR2 — Daemon core
- [ ] PID-lockfile singleton guard
- [ ] Scan inboxes; skip done (`yt_id` set); flag `needs_metadata` / `error`
- [ ] Upload via existing script; write `yt_id` back atomically (temp + rename)
- [ ] Global daily budget 6; round-robin across farms; 429 → sleep to 07:05 UTC + retry
- [ ] Network error backoff; corrupt file → `error`, continue
- [ ] Audit log (`upload.log` lines: ts, farm, file, yt_id/FAILED, rc)
- [ ] Local suite passes

### PR3 — CLIs
- [ ] `farm-media-queue list [--farm X] [--status uploaded|pending|error]`
- [ ] `farm-media-manifest commit <farm_id>` → builds FARM_MEDIA_MANIFESTS/<farm>.json + index.json → PR
- [ ] Dry-run flag default; explicit `--push` to actually open PR

### PR4 — Service + inboxes + migration
- [ ] systemd unit (Restart=always, runs as ubuntu)
- [ ] `/home/ubuntu/farm_media_inbox/cleide/` populated: 71 mp4 + sidecars built from manifest.json (sha256/GPS/objects/title/desc)
- [ ] Retire PID 105025 throttled_uploader + La do Sitio reupload_retry.sh
- [ ] Daemon picks up remaining Cleide uploads under budget/fairness

### PR5 — UAT gate
- [ ] Remaining Cleide videos upload across days under 6/day budget (no 429 blowout, fairness observable)
- [ ] Manifest committed with yt_ids; index.json updated
- [ ] Fresh-Sophia test: read GitHub → correct uploaded/pending/committed answer
- [ ] Governor query test: "find me cacao videos from Cleide" → correct asset list (photos + videos)
- [ ] systemd restart survival; daemon resumes where it left off (sidecar state)
- [ ] Old ad-hoc uploaders confirmed stopped

## 7. Do / Don't
- **Do** keep the daemon dumb: metadata comes from sidecars, never regenerated.
- **Do** keep GitHub commits deliberate (never automatic per-video pushes).
- **Do** log every upload attempt (auditable quota accounting).
- **Don't** let two writers touch sidecars (singleton, lockfile).
- **Don't** put credentials in the repo.
- **Don't** create variant plan/backlog files.

## 8. Related
- `FARM_MEDIA_PIPELINE.md` — the pipeline runbook this daemon serves (PR #858)
- `FARM_MEDIA_MANIFESTS/index.json` + `<farm>.json` — committed state the daemon feeds
- `farm-media-raw` — raw photo blob store (sibling)
- `config/youtube/upload_video_to_youtube.py` — the upload primitive (local, gitignored)
