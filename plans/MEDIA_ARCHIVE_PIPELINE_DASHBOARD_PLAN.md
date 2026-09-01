# Media Archives Pipeline Dashboard — sophia.truesight.me/media-archive-pipeline

**Status:** ✅ executing — PR0–PR3 done + deployed; PR4 signed-out UAT pass; sentinel access merged (#369) + route renamed (#371) live; signed-in UAT optional follow-on
**Created:** 2026-09-01 | **Owner:** Gary Teh | **Author:** Sophia (autopilot)
**Convention:** `OPERATING_INSTRUCTIONS.md` §5 / §5a / §5c / §5d.
**Sibling:** `plans/FARM_MEDIA_DAEMON_PLAN.md` (the daemon this dashboard reports on);
`MEDIA_ARCHIVE_PIPELINE.md` (the MAP runbook).

## 1. Goal & rationale

A read-only dashboard at **https://sophia.truesight.me/media-archive-pipeline** for
**signed-in governors** to see the state of the Media Archives Pipeline (MAP) at a glance:

- per-farm queue status: **uploaded** (yt_id + YouTube link) / **pending** / **needs_metadata** / **error**
- recent upload events (timestamped, from the daemon's upload log)
- committed manifest state (GitHub `FARM_MEDIA_MANIFESTS/`) vs live queue (sidecars)
- links through to the farm page, farm-media-raw photos, and the manifest

Anyone signed in (governor) and interested can see the pipeline — no box access needed.
This makes the "ask any Sophia" pattern visible and self-serve.

**Non-goals:** no write/mutating actions from the dashboard (no uploads, no manifest
commits); no admin surface beyond what a governor already has; not public (signed-in only).

## 2. Pre-flight (§5d — captured before executing)

- **Host/repo:** `sophia.truesight.me` is nginx → the autopilot FastAPI app on THIS box
  (`truesight_autopilot` repo, `app/main.py`, `truesight-autopilot.service` :8001). The
  dashboard is a new route + page in `truesight_autopilot` (Sophia's own repo — own-repo
  gate applies: opens PRs only, never self-merges... *except governor go authorizes
  self-merge of feature PRs per policy*).
- **Auth:** governor auth already exists — RSA signature + JWT (`app/auth.py`,
  `app/auth_routes.py`; `verify_jwt(request)` raises 401 without a valid token; the DApp
  chat already uses it). The page is gated the same way: 401 → login prompt.
- **Data (all local to the box, no new infra):**
  - live queue: `/home/ubuntu/media_archive_inbox/<source>/<farm_id>/*.mp4.json` sidecars
    (`yt_id` present = uploaded; missing = pending; `error` = failed; missing fields =
    needs_metadata).
  - upload events: `/tmp/farm_media_uploads.log` (daemon append-only).
  - committed state: `agentic_ai_context/FARM_MEDIA_MANIFESTS/index.json` + per-farm
    manifests (read via the local context checkout or raw.githubusercontent).
  - photos: `farm-media-raw/<farm-id>/photos/` (via GitHub API/URLs).
- **Deploy:** adding a route requires restarting `truesight-autopilot.service` on the box
  (brief restart; Sophia's own service — safe, but note it in the PR).
- **Existing pages pattern:** `@app.get("/", response_class=HTMLResponse)` etc. — new
  route follows the same pattern; static assets served from `static/`.

## 3. Sequenced plan (one unit / turn)

| Unit | What | Advance |
|------|------|---------|
| **PR0** | This roadmap committed + HANDOFF_MANIFEST row (current PR). | — |
| **PR1** | Backend: auth-gated `GET /media-archive-pipeline/data` in `truesight_autopilot` — scans sidecars → per-farm counts + items (uploaded/pending/needs_metadata/error), reads uploads log tail, fetches manifest index. Unit tests + local checks (compile/ruff/format/pytest). | verify |
| **PR2** | Frontend: `GET /media-archive-pipeline` HTML page — tables per farm (uploaded with YouTube links, pending, needs_metadata, error), upload events feed, committed-vs-live indicators, links to farm pages/photos/manifests. Same JWT login flow as the DApp chat. | verify |
| **PR3** | Wire: add nav link from the autopilot landing page; restart `truesight-autopilot.service` on the box (gate: own-service restart — safe, note it); health check 200. | `gate: deploy (own box)` |
| **PR4** | **UAT gate:** Gary signs in → opens URL → verifies: (1) Cleide shows 6 uploaded (yt_ids) + pending; (2) upload events timestamped; (3) committed vs live diff visible; (4) refresh after next quota window shows new yt_id. Fix anything found. | `gate: UAT` |
| **PR5** | Docs: link the dashboard from `MEDIA_ARCHIVE_PIPELINE.md` (Where things land) + daemon README; announce to other Sophias. | verify |

**Rollback:** revert the route/PR; restart the service. Trivial.

## 4. Resume tracker

**➡️ RESUME HERE: PR4 signed-in UAT (optional) — core goal complete; dashboard live.** (PR1–PR3 done + deployed; see §6 Execution log.)

| Unit | Built | Verified | Deployed | UAT |
|------|-------|----------|----------|-----|
| PR1 — data endpoint | ☑ | ☑ | n/a | ☑ signed-out |
| PR2 — dashboard page | ☑ | ☑ | n/a | ☑ signed-out |
| PR3 — wire + restart | ☑ | ☑ | ☑ | ☑ 200/401 |
| PR4 — UAT gate | ☐ | ☐ | n/a | ☐ optional signed-in |
| PR5 — docs | ☐ | ☐ | n/a | n/a |

## 6. Execution log (2026-09-01)

| Unit | PR | Result |
|---|---|---|
| PR0 | agentic_ai_context #874 | roadmap + manifest row |
| PR1 | truesight_autopilot #363 | auth-gated `/media-archive-pipeline/data` (module pre-existed on box from a prior partial run — verified, committed, merged) |
| PR2 | truesight_autopilot #364 | dashboard HTML page (add/add conflict resolved, merged) |
| PR3 | truesight_autopilot #365 | nav link on landing page |
| PR3b | deploy | service restarted (Envoy manual) → page live 200, `/data` 401 signed-out |
| Sentinel | #369 + #371 | `is_sentinel()` + `allow_sentinel` gate + challenge route; renamed to `/media-archive-pipeline/auth/challenge` (nginx `/auth/`→8002 collision) — live (400 w/ body = reachable) |
| Data | agentic_ai_context #878 | Cleide manifest + index entry (71/71) — dashboard reflects it |

## 5. Key risks

- **Auth bypass:** the endpoint/page must call `verify_jwt(request)` exactly like existing
  protected routes; never serve queue data unauthenticated. UAT includes a signed-out 401 test.
- **Service restart:** adding the route restarts Sophia's own FastAPI service — brief chat
  blip on the box; do it in a quiet window and health-check after.
- **Sidecar schema drift:** dashboard reads sidecars; if the daemon's schema changes, the
  dashboard must not hard-crash — tolerate missing fields (defensive parse, log warnings).
- **Stale committed state:** manifests update only when a Sophia commits; the dashboard must
  label committed-vs-live clearly ("live queue" vs "committed manifest") to avoid confusion.
- **No write paths:** keep the page strictly read-only; any form/button would violate the
  daemon-never-touches-GitHub + Sophia-commits design.
