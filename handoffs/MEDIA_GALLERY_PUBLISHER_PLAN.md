# Media Gallery Publisher — execution plan

**Created:** 2026-09-11 (Sophia) at Gary's request · **Handoff:** thread 26438 · **Status:** PR1 filed — executing
**Origin:** spun out of the Cacau na Veia (N-06-37) PR6 near-miss — 33 site-visit videos were fully transcoded + uploaded to YouTube (sidecars carried `yt_id`), yet `farms/cacau-na-veia-pacaje/media.json` stayed photos-only. Nothing reconciled "uploaded" against "published". See `handoffs/CACAU_NA_VEIA_MEDIA_TASK_PLAN.md`.

## Goal
Make a farm/program media gallery a **derived artifact the page fetches**, written into the machine-owned `farm_media_manifests` repo — so "uploaded but not published" is impossible by construction, not merely audited.

## Problem (measured)
Three homes, no reconciliation:

| Asset | Home | Owner |
|---|---|---|
| `yt_id`/sha256/GPS per clip | daemon sidecars | automation |
| farm manifest | `farm_media_manifests` (Contents-API) | automation |
| the web gallery `farms/<slug>/media.json` | site repo | **hand-authored** |

The site gallery is the only hand-authored link → it silently lags the pipeline.

## Design (verified)
- **Publisher** = the manifest/commit stage (NOT the daemon, which is YouTube/S3-credentialed; publishing is a deliberate act). Idempotent, re-runnable.
- **Write target** = `farm_media_manifests` (reuse the existing dedicated, machine-owned repo; already Contents-API owned). No site-repo writes → no PR gate, no drift.
- **Read path** = `js/media-gallery.js` fetches `./media.json` today; change to **fetch the manifest repo first, fall back to `./media.json`**. Zero-breakage migration.
- **Generality** = key on a generic `collection_id` (farm / program / partner), aligning with the CRF-Anapu `entity_type` work (OPEN_FOLLOWUPS).
- **Cadence** = **systemd timer** running an idempotent reconcile (cheaper + crash-safe vs. a long-running poll loop). "Done" primitive already exists: sidecar `yt_id` / `farm-media-queue list`.

## Data flow
```
MAP daemon (unchanged):  transcode -> sidecars(yt_id) -> manifest
Publisher (NEW, timer):  read sidecars -> emit ordered gallery JSON
                         -> write galleries/<collection>.json in farm_media_manifests
                            (+ backfill yt_id into the manifest)
site media-gallery.js:   fetch that JSON  (fallback ./media.json)
```

## PR sequence (ONE PR PER TURN)
- **PR1** ✅ this plan + HANDOFF_MANIFEST row (thread 26438).
- **PR2 ⛔ BLOCKER** — fix the box's GitHub write path so it can **UPDATE an existing file**. Today `upload_file_to_github` / `upload_local_file_to_github` both fail on updates: GitHub `422 "sha wasn't supplied"` (they never fetch the current blob sha). Any publisher that rewrites `index.json`/the gallery breaks on run 2. (PR6 workaround: the box SSH deploy key — `garyjob` — did a direct `git push`; fine for a one-shot, but a *publisher* needs a supported path.) Decide: fix the tool to fetch+pass `sha`, or standardise an SSH-key push helper.
- **PR3** — `farm_media_gallery.py`: sidecars/manifest → gallery block. Idempotent, stable order (capture time), `aspect` from ffprobe, captions from transcript/VTT + **QA guard** (drop Whisper hallucinations e.g. "Legendas pela comunidade de Amara.org"; boilerplate fallback on empty transcripts).
- **PR4** — `farm-media-manifest commit --with-gallery <collection>`; backfill `yt_id` (replaces the hand-authoring PR6 needed). Parity check: `sidecars-with-yt_id == media.json youtube count == manifest yt_id`.
- **PR5** — publisher + systemd timer wired as an idempotent reconcile.
- **PR6** — site `media-gallery.js` fetch-first (fallback `./media.json`) → beta → **UAT gate**.
- **PR7** — promote beta→prod on explicit GO.

## Gates / cautions
- Never write the site repo from the daemon. The publisher may write the data repo without a PR (machine-owned); the *site* change (PR6) is PR-reviewed and beta-first.
- Hosting the fetched JSON: prefer **GitHub Pages on `farm_media_manifests`** (controlled origin, proper CORS + caching). `raw.githubusercontent.com` works (`ACAO: *`) but is a third-party origin, uncached, rate-limited. NOTE: the S3 bucket `media.agroverse.shop` is **not** a viable JSON origin until its TLS is fixed (separate OPEN_FOLLOWUPS entry).
- No prod sync without governor GO.

## RESUME HERE
PR2 (the update-existing-file write-path blocker) — without it the publisher cannot run twice. Then PR3→PR7.
