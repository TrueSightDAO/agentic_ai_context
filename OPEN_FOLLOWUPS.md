# Open follow-ups (cross-session backlog)

> **This is the ONLY open-followups file.** Do not create variant filenames
> (`OPEN_FOLLOW_UPS.md`, `FOLLOWUPS.md`, `TODO.md`, …) — a duplicate
> `OPEN_FOLLOW_UPS.md` existed 2026-05-31 → 2026-06-06 and split the backlog
> across two files until it was merged back here; that file is now a tombstone
> pointing at this one. Sophia / autopilot agents: file new tooling gaps and
> follow-ups **here**, under `## Pending`, via PR.

Short list of **scoped follow-up tasks** future AI agents (Claude / Cursor /
Codex / Kimi / etc.) and humans can pick up between sessions. The bar is:

- One thing that didn't ship in the original PR but logically belongs after it.
- Small enough to fit in a single session (rough cap: ~60 min of focused work).
- Self-contained — the entry has enough context that someone who didn't write
  the original code can act on it without reverse-engineering history.

This file is **not** a replacement for `CONTEXT_UPDATES.md` (which is the
append-only event log) or for project-specific TODOs that live next to the
code (e.g. `# TODO:` comments, `dapp/UX_CONVENTIONS.md`, repo READMEs, or the
"Q5 parked" pattern inside individual proposal docs like
`PARTNER_VELOCITY_PROPOSAL.md`). It is the place for **cross-repo /
cross-session** items that would otherwise rot in chat transcripts.

## Workflow for agents picking up an entry

1. Read the entry. If the **Blocker** still applies, leave it alone.
2. If you're going to ship it, claim it informally by appending a line to
   `CONTEXT_UPDATES.md` (`<agent-id> | starting OPEN_FOLLOWUPS#…`) so parallel
   sessions don't duplicate work.
3. Open a PR. When merged, **move** the entry to the bottom of this file
   under `## Recently shipped` with the PR link, and append a one-line entry
   to `CONTEXT_UPDATES.md`. Keep the **Pending** list short.
4. If the entry is no longer relevant (priorities shifted, blocker permanent,
   etc.), move it to `## Closed without shipping` with a one-line reason.
   Don't silently delete history.

---

## Pending

### GAS `parseAndProcessTelegramLogs` runs with the script lock TEMP-DISABLED — re-enable after root-causing the >30s lock contention
**Filed 2026-09-12. Owner: unclaimed. Governor: Gary (thread 26845, closed).**

**Context.** The governor hit `parseAndProcessTelegramLogs: could not acquire script lock within 30s; aborting to avoid double-processing` in the GAS editor. Root cause narrowed to: the function acquires `LockService.getScriptLock().waitLock(30000)` (Code.js ~line 1050 — idempotency guard 1, added 2026-09-09 after the `Edgar_20260909124022_298` double-booking) and **another execution held the lock >30s**. Two compounding defects made it worse:
1. **False success:** on lock failure the function did a bare `return;` and `doGet` still printed `"✅ Telegram logs processed successfully…"` — so a *skip* was indistinguishable from a *completed run*. Edgar's Sidekiq caller therefore never retried, and pending expense submissions were silently stranded (scored sheet sat at row 218; on 2026-09-12 three authorized expenses — `Edgar_20260912162828_478`, `…163238_482`, `…163341_484` — had never scored).
2. The lock serializes by *time*, not by *work*, so overlapping invocations (Edgar webhook + editor manual Run) race and one aborts.

**What shipped (temporary mitigation, 2026-09-12).**
- **tokenomics PR #475** (merged, `054f700`): adds `const _DISABLE_PROC_LOCK = true` → the `waitLock(30000)` acquire is skipped (revert = flip to `false`); the skip path now returns `{status:'skipped_lock_contention'}` and `doGet` returns `⚠️ Skipped…` instead of a false `✅`.
- **Pushed to GAS HEAD** and **redeployed the wired deployment in place**: `clasp update-deployment AKfycbwYBlFigSSPJKkI-F2T3dSsdLnvvBi2SCGF1z2y1k95YzA5HBrJVyMo6InTA9Fud2bOEw -V 13` → deployment **v12 → v13, same URL** (`…/macros/s/AKfycbwYBlFigS…/exec`), so Edgar's `telegram_webhook_listener.js:203` wiring is untouched. Verified: one live `/exec` fire returned ✅ in 43s, no lock error, and the 3 stuck expenses scored `authorized` (offchain ledger #4261–4263).

**Why this is still open.** The lock is **disabled in production** — this reintroduces the vulnerability class guard 1 was added to close (currently backstopped only by the lock-free hash guard 2, the fresh col-K re-read, which is weaker than a real mutex). The **root cause of the >30s hold is still unnamed**: the lock is always released in `finally`, so something must be overlapping or running long.

**Proposed work (~60 min).** (1) Inspect the GAS editor **Executions** page (and, if a GCP project is linked, Cloud Logging / `clasp tail-logs`) for overlapping or long-running `parseAndProcessTelegramLogs` invocations around the failure — name the holder. (2) If it is *backlog overlap*, confirm the queue is drained and **flip `_DISABLE_PROC_LOCK` back to `false`** (revert PR #475). (3) If it is *long single runs*, replace the coarse script lock with a **shorter, work-scoped** guard (e.g. a last-processed-key watermark that is idempotent), so overlap is safe without a 30s block. (4) Add a regression test asserting a lock skip is **never** reported as success. Blocker: (1) needs the editor Executions view (governor) or a linked GCP project.

**Evidence.** `Code.js` lines ~1050–1056 + `doGet` wrapper (repo `main` and live HEAD byte-identical); PR #475; deployment list showing `AKfycbwYBlFigS… @13` updateTime `2026-09-12T17:33:28Z`; scored sheet rows 219–221 (today's 3 expenses, `authorized`).

### `google_app_scripts/<scriptId>/` repo folder is NOT a clean clasp mirror — pushing from the repo folder would break the live GAS project
**Filed 2026-09-12. Owner: unclaimed. Governor: Gary (thread 26845).**

The repo folder `tokenomics/google_app_scripts/19Wag9x-sjbLVgIsPh2vj90ZG7Rgq2iGaVOomAeAvtg6CdZKJHLZ9AJrC/` carries `Version.gs`, `Credentials.sample.js`, `manifest.json`; the live GAS project has `Version.js`, `Credentials.js`, `appsscript.json`. A blind `clasp push` from the repo folder would **add duplicate top-level files → duplicate function definitions (`getClaspMirrorDeployInfo`, credential accessors) and break the project**. (Same scriptId — `.clasp.json` in the repo points at the live project.) Deploys must push from an exact `clasp clone` of live, not from the repo path.

**Proposed work (~30 min).** Either (a) make the mirror explicitly one-way + label it: rename the repo copies (`Version.mirror.txt`, `Credentials.sample.js` kept as the contract), add a `README` warning, and add a preflight check to `deploy_gas_project` that **refuses a push whose file set differs from live HEAD**; or (b) reconcile the filenames so repo == live. Blocker: none.

**Evidence.** `ls` of both trees; `.clasp.json` scriptId match; `clasp clone` output (6 files, live) vs repo folder file list.

### Autopilot box root filesystem (`/`) fills to 100% — disposable repo clones land on `/tmp`, while the 246G `/media` volume sits at 25%
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 24441).**

**Symptom.** On 2026-09-11 during the Cacau na Veia prod-completion, `git_push_changes` failed with `fatal: write error: No space left on device` / `fetch-pack: invalid index-pack output`. `df -h /` showed `/dev/root` (78G) at **100% — 5.5M free**, while the dedicated data volume **`/media` (`/dev/nvme1n1`, 246G) was at 25% (175G free)**.

**Cause.** `/` is only 78G yet carries both the large `/home/ubuntu` working sets (uncompressed site-visit zips: `la_do_sitio_2026.zip` 3.8G, the three pacaje location zips 1.2–2.1G each) **and** `/tmp`, where the autopilot's own tooling clones a full repo on every `git_push_changes` / `open_fix_pr` (`/tmp/sophia-git-*`, plus session-ad-hoc clones ~840M each). Nothing prunes these between sessions — `systemd-tmpfiles-clean.timer` is active but its default `/tmp` age policy (10d) does not cover named working dirs, and there is no autopilot gc script.

**Immediate remediation (done 2026-09-11).** Removed ~9 disposable clones (~9G) → `/` back to **89% (9.0G free)**. Unblocked the push.

**Residual risk (biggest consumers still on `/`).** `/tmp/gh_assets` 4.1G, `/tmp/pac` 3.8G, `/tmp/farm-media-raw` + `/tmp/fmr` 3.6G, `/tmp/fda_fsvp` 752M, `/tmp/tg_attachments` 851M; `/home/ubuntu/*.zip` ≈ 8.3G total.

**Proposed fix (~60 min).** (1) Point the tooling's scratch/clone root at `/media` (env `TMPDIR` or the clone-tempdir constant in `truesight_autopilot`) so large checkouts land on the 246G volume; (2) move the long-lived working sets (`/home/ubuntu/*_work`, media-archive stagers) onto `/media`, keeping `/home/ubuntu` for code + zips only; (3) add a small gc that prunes `/tmp/sophia-git-*` older than N hours plus orphaned `magick-*` scratch (boot or post-job); (4) add a disk-headroom guard alerting at ≥90% on `/`. Blocker: none — (1)+(3) are `truesight_autopilot` code (normal PR), (2)+(4) are box/host config.

**Evidence.** `df -h /` before/after; the failed-`git_push_changes` stderr (`No space left on device`); `du -sh /tmp/*` rollup.

### media.agroverse.shop does not serve valid HTTPS (CNAME → S3 website endpoint, TLS cert mismatch)
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 26438).**

**Symptom.** `curl https://media.agroverse.shop/` fails TLS: `SSL: no alternative certificate subject name matches target host name`. `openssl s_client` shows `subject=CN=s3.amazonaws.com`, SAN `*.s3.amazonaws.com` — i.e. the host is a **CNAME to `media.agroverse.shop.s3.amazonaws.com`** (S3 website endpoint, `s3-1-w.amazonaws.com` → `16.15.230.213`), so S3 serves the generic `*.s3.amazonaws.com` certificate, which matches neither the S3 hostname nor the custom domain.

**Impact.** The MAP bucket (`s3://media.agroverse.shop/` — the archive worker writes `raw/` + `previews/`) is reachable over **http** (S3 website endpoint) but **not https with verification**. Any browser/consumer using `https://media.agroverse.shop/...` hits a cert error; this also blocks the bucket as the gallery-JSON origin (see `handoffs/MEDIA_GALLERY_PUBLISHER_PLAN.md`, hosting caution).

**Proposed fix (~30 min, infra).** (a) Front the bucket with CloudFront + an ACM cert for `media.agroverse.shop` (recommended — https + caching + a stable CORS origin), point the CNAME at the distribution; or (b) drop the custom domain and use the S3 REST endpoint. Blocker: none — needs an AWS + DNS change (governor).

### Program/partner media needs its own MAP entity type + a program-page gallery convention (first instance: CRF Anapu)
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25181).**

Governor decision 2026-09-11 (thread 25181): (a) program pages should carry media galleries going forward — previously a farm-page-only convention (`AGROVERSE_FARM_PAGE_CONVENTIONS.md` §1/§3); (b) introduce a new MAP **entity type** (`program` / `partner`) alongside `farm`, so media from a partner/school/program is not shoe-horned into the farm construct.

Today `farm_media_manifests/` models only `farm_id`; `truesight_me/programs/<slug>/manifest.json` (`CREDENTIALING_PROGRAM_PAGES.md` §6) has **no media field**; galleries are read only from `agroverse_shop_beta/farms/<slug>/media.json`.

**Work (~60 min):** (1) add `entity_type` (`farm` | `program` | …) to the manifest schema + the `farm_media_manifests/index.json` entries; (2) document a `programs/<slug>/media.json` gallery contract mirroring the farm `media.json` (`{schemaVersion, hero, gallery:[…]}`) and wire the program shell to render it via `media-gallery.js`; (3) update `CREDENTIALING_PROGRAM_PAGES.md` §6 (manifest schema) + `MEDIA_ARCHIVE_PIPELINE.md` terminology (add the `program-media` source namespace). First instance: `crf-anapu` — see `handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md`. Blocker: none (governor-directed).

### Edgar reports `fileUploadedToGithub: false` on binary-upload failure but still returns a success shape - clients cannot tell "event recorded" from "photo stored"
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25181).**

**Symptom.** On 2026-09-10 21:31:11-21:32:39 UTC a single burst of 24 `[TREE PLANTING EVENT]` submissions from the SunMint farmer app (`sunmint.truesight.me`) recorded a `Photo URL` in the ledger but never committed the image to `TrueSightDAO/sunmint` `images/`. All 24 photo URLs 404 on raw.githubusercontent.com: `Edgar_20260910213111_376` .. `Edgar_20260910213239_422`. One tree just outside the window (`Edgar_20260910171200_354`, 17:12:00 UTC) loads fine - so it is isolated to that burst, consistent with a GitHub secondary rate limit on 24 commits in ~88 s (the same rate-limit response was reproduced twice while investigating).

**The server-side defect.** Edgar reports the binary upload separately as `fileUploadedToGithub` in an otherwise-normal success body - `tokenomics/API_ENDPOINTS.md` shows `{"status":"success","fileUploadedToGithub":false,...}` as a *documented* success shape. So "the event was recorded but the photo was NOT stored" is indistinguishable, at the status-code level, from full success. Any client that checks `resp.ok` alone will treat a dropped photo as done.

**Client side already fixed.** `sunmint_beta` PR #83 guards on `fileUploadedToGithub === false` -> keeps the record queued and preserves the blob. But that only protects clients that adopt the guard; the API contract itself is the gap.

**Proposed fix (~30 min).** In `dao_protocol`/Edgar's submit path: (a) retry the GitHub binary write with backoff so a transient rate limit self-heals; (b) when the binary upload ultimately fails, return a distinct status (or a `photo_stored: false` flag) so clients can distinguish "event recorded" from "photo stored" without parsing a success body. Blocker: none. Note: the 24 already-lost photos are not recoverable server-side - the signed event text carries only the destination path; the blobs existed solely in the client's IndexedDB (evicted on the 200).

**On-box note.** `ssh dao_protocol` is key-denied from the autopilot box, so the server journal for 21:31-21:33 UTC could not be read to convict the rate limit vs. another transient - verify there when picking this up.

### Autopilot's hardcoded `TREE PLANTING EVENT` labels are stale **and** the committed `events_catalog_snapshot.json` crashes its own reader - box freezes on stale labels during an Edgar outage
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25178).**

**Symptom.** Two defects in `truesight_autopilot`'s events-catalog layer, found while filing 25 tree-planting events (thread 25178):

**(a) Stale hardcoded fallback.** `app/main.py::_CANONICAL_LABELS["TREE PLANTING EVENT"]` = `["Number of trees planted", "Species", "Location", "Attached Filename", "Submission Source"]`. The live Edgar catalog (**v5**, `GET https://edgar.truesight.me/events-catalog`) carries `["Tree Count", "Location", "Latitude", "Longitude", "Plot ID", "Species", "Planter", "Planting Time", "Photo URL", "Attached Filename", "Submission Source"]`. Missing from the fallback: **Tree Count, Latitude, Longitude, Plot ID, Photo URL** - and the tree count is even under a different name (`Number of trees planted` vs `Tree Count`).

**(b) Snapshot/reader shape mismatch.** The committed fallback snapshot `app/data/events_catalog_snapshot.json` is shaped `{"events": [ {event_name, category, description, canonical_labels, required_fields, dapp_page}, ... ]}` - **`events` is a LIST**. But its reader `_refresh_events_catalog()` does `events = catalog.get("events", {})` then `events.items()` - expecting a **DICT**. Feeding the committed snapshot through the reader raises `AttributeError: 'list' object has no attribute 'items'` (reproduced on-box 2026-09-10).

**Impact.**
- (a) is latent: on stale labels the box still *accepts* a submission using the old key `Number of trees planted`, but the SunMint GAS sheet ingestion grabs `Tree Count` -> gets empty -> the PL-006-class duplicate/auto-assign bug (see the `SunMint Plots` row 26 `PL-006` incident, same thread 25178). NOT a validation failure: `TREE PLANTING EVENT` has **no entry** in `_VALIDATE_REQUIRED_FIELDS`, so `_validate_required_fields` returns `[]` and nothing is marked INVALID; `_normalize_via_catalog` step 5 also **keeps** unmatched keys rather than dropping them.
- (b) is the sharper one: at startup (line ~452) the call is wrapped in `try/except` -> boot survives on hardcoded labels. In **`_catalog_refresh_loop`** (line ~489) it is **NOT** wrapped -> the `AttributeError` propagates and **kills the 12-hour refresh task permanently**. So an Edgar outage that drops into the snapshot branch freezes the box on stale labels until a process restart, even after Edgar recovers.

**Proposed fix (~30-45 min, two independent PRs).** (1) Refresh `_CANONICAL_LABELS["TREE PLANTING EVENT"]` (+ any other stale entries) against catalog v5, and add a test asserting the hardcoded fallbacks are a **subset** of the live catalog's labels for every shared event type. (2) Make the snapshot reader shape-tolerant: accept both a list and a dict under `events` (normalize list -> `{event_name: entry}`), and wrap the `_catalog_refresh_loop` call in `try/except` so a failed refresh can never kill the loop. Regenerate the snapshot from the live catalog so its shape matches the reader. Owner: unclaimed (autopilot self-improvement candidate).

**On-box drift.** `events_catalog_snapshot.json` currently shows as deleted in the autopilot checkout (`git status: D`) and HEAD `2e055b3` is behind origin `659e5d6` - cosmetic, but worth a pull.

**Related, NOT duplicated:** thread 24846 / `handoffs/GAS_DEPLOY_ACCESSOR_GUARD_PLAN.md` (the clasp/Credentials `setApiKeys` guard) is a separate issue.



### CLI `.env` key values wrapped in literal quotes silently break signature verification (logged-but-not-dispatched)
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** `/opt/truesight_autopilot/.env` had `PUBLIC_KEY` / `PRIVATE_KEY` wrapped in **literal single quotes**. The CLI embeds the public key into the signed `share_text`; Edgar's verifier then raises on PEM load (`InvalidByte(0, 39)` = `'`), so `signature_verification = "error"`. Because `dispatch_event` is gated on `signature_verification == "success"` (`dao_client/server/routes/dao.py:~337`), the submission is **appended to `Telegram Chat Logs` but never dispatched to the ledger** — a silent, user-invisible drop. Two Sítio Torres contribution events were lost this way before it was caught. Fixed on this box 2026-09-10 (backup `.env.bak.20260910194840`); local sign→verify round-trip now `True`.

**Audit (2026-09-10) — did it silently drop OTHER past submissions?** Swept all **12,324** rows of `Telegram Chat Logs` (`1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`), column P = Edgar Signature Verification: **5684 success / 6512 blank (column predates 2025-09) / 97 no_signature_format / 28 error / 2 failed**. **No evidence of a long silent-drop history from this box** — monthly `success` dominates the CLI era (2199 successful `[CONTRIBUTION EVENT]`s vs 2 errored = today's, already resubmitted); Sophia-attributed rows 322/327 success. Historic `error` rows trace to other causes (proposal votes, email-registration variants, malformed test payloads). Two caveats: (1) `Edgar Direct` is the *shared* CLI default chatroom, so rows can't be attributed to one host; (2) **rows 9769/9770 (2026-06-15, `[EMAIL REGISTERED EVENT]`)** are the only earlier rows carrying the quoted-PEM signature — eyeball manually, do **not** blind-backfill.

**Impact.** A signed submission that merely *looks* fine in the chat log is silently never recorded on the ledger; no error surfaces to the operator.

**Proposed fix (~20 min).** (1) In the CLI env loader (`truesight_dao_client`), defensively `strip()` surrounding whitespace/quotes from `PUBLIC_KEY`/`PRIVATE_KEY` before use. (2) Have the submit path WARN loudly (Telegram + log) whenever `signature_verification != "success"`, so a future drop is never silent. (3) Check peer boxes for the same quoted-key `.env` shape. Blocker: none.

### Contribution submission defaults `TDG Issued` to 0 — agents silently file zero-TDG events, then need a `CORRECTION`
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25149).**

**Symptom.** On 2026-09-10 two contribution reports were filed with `TDG Issued = 0`: the Sítio Cristo Rei farm/media report (`Edgar_20260910144626_342`) and the Sítio Torres (N-06-66) FDA FSVP record report. Both had to be re-filed as a second `[CONTRIBUTION EVENT]` titled `CORRECTION — …` carrying the auto-computed value (Cristo Rei correction `Edgar_20260910145224_344`; Sítio Torres correction filed same day, 240 min → 400 TDG). Gary's standing rule is that TDG must always be the auto-computed rubric value, never 0 (`dao/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md` §5, standing rule of 2026-09-10, thread 24442 — which superseded the older "`0` unless the operator sets real economics" wording).

**Root cause.** The `create_dao_submission` autopilot tool defaults its `tdg_issued` argument to the **string `"0"`** and always emits a `TDG Issued` attribute in the payload. An agent that does not explicitly pass a value therefore silently files a zero-TDG `[CONTRIBUTION EVENT]` — the default *is* the wrong answer, and it fails silently (no warning, no error). Note this is the **agent-tool** path only: the sanctioned CLI (`dao_client/modules/report_contribution.py` → `rubric.tdg_for`, `TDG = minutes / 60 * 100`) recomputes TDG from `Type` + `Amount` and explicitly ignores/overrides any caller-supplied value, so CLI-filed contributions are unaffected.

**Impact.** Every contribution filed through the tool by an agent that doesn't override `tdg_issued` lands with `TDG Issued = 0`, under-crediting the contributor and leaving a misleading ledger row that later needs a correction entry. Silent-wrong-default is the worst failure shape: nothing surfaces until a human notices the ledger line.

**Proposed fix (~15-20 min).** In the `create_dao_submission` tool, either (a) drop the `tdg_issued` default and **omit** the `TDG Issued` attribute from the payload when the caller didn't set it (let Edgar/rubric compute it — mirrors the CLI), or (b) default it to the rubric value derived from `Type` + `Amount`. Whichever is chosen, do **not** default to `0`.

**Reassigned.** The actual code fix is owned by **thread 24441** — this entry is backlog hygiene so the root cause is documented and the tool's silent-wrong-default doesn't get re-diagnosed from scratch next time. Blocker: none.
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25148).**

**Symptom.** The ops-sheet tab `Document Notarizations` (spreadsheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`, gid 520413576 — the target of the public `truesight.me/notarizations` redirect) holds **46 data rows, the newest dated 2026-07-08**. Known notarizations since then are absent from it: Sophia's Cleide-factory notarization (2026-09-09, `Telegram Chat Logs` rows 12274/12275) and the Cacau na Veia site visit (2026-09-10, `Telegram Chat Logs` rows 12315/12316). Those rows DO exist in `Telegram Chat Logs` (the authoritative Edgar intake) and the files ARE committed to the `notarizations` repo — only the derived mirror tab is missing them.

**Root cause (hypothesis).** The mirror is produced by the agentic GAS `process_notarization_telegram_logs.js` (`tokenomics/google_app_scripts/1vC3p_WfKQT-fl5tHZ9-E3aotYon3gQdOiFVLmyVElMqB-hi_FT3rcB8W/`), which scans `Telegram Chat Logs` col G for `[NOTARIZATION EVENT]` and appends to `Document Notarizations`. Either (a) the WebhookTriggerWorker no longer fires it, or (b) the GAS runs but errors. Note the scanner matches `startsWith("[NOTARIZATION EVENT]")`, while at least one recent row (`Telegram Chat Logs` row 12273, 2026-09-09) uses the distinct hash-form `[NOTARIZATION]` — a second, unmirrored event variant.

**Impact.** `truesight.me/notarizations` (the public audit surface) silently stops showing new notarizations even though the underlying files + signatures are present and valid — a compliance-relevant document looks "not notarized".

**Proposed fix (~30-45 min).** (1) Check the GAS trigger / WebhookTriggerWorker wiring for `process_notarization_telegram_logs`. (2) Confirm whether the GAS errors on the hash-form `[NOTARIZATION]` variant and extend the matcher if so. (3) Backfill the missing rows (Cleide 2026-09-09, Cacau na Veia 2026-09-10) or document the tab as best-effort. Blocker: none.


### `B-06-108_20260908_1` boundary photos are missing everywhere — media cleared, needs re-upload
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24441).**

**Symptom.** Gary reported broken popup thumbnails on `truesight.me/sunmint.html` (plot `N-06-37` + others). Root cause is deeper than the file: `sunmint/plots/index.geojson` is **generated daily** (`rebuild-plots-index.yml`, 06:05 UTC + dispatch) from the `SunMint Plots` sheet (§K `Media` = `build_plots_geojson.py`), so a direct geojson edit is overwritten within 24 h — the **sheet cell is the durable source**.

**Audit (22 plots) found 6 affected, not the 4 first reported:** `PL-002`, `CR-PA-P2` (missed originally), `N-06-37`, `N-06-37_20260909_restoration_1` held **bare `IMG_9xxx.HEIC` / `.MOV`** filenames (no directory → resolves against the repo root → 404), and `N-06-66` held **absolute `.HEIC` URLs** (resolved, but HEIC does not render in `<img>` in any mainstream browser).

**Shipped this session.** Converted HEIC→JPG (heif-convert → 1600px → q80), uploaded **22 JPGs** to `sunmint/images/boundaries/<plot_id>/` (registry §4 convention); rewrote the sheet `Media` cells for 5 plots via the `agroverse_qr_code_manager` SA and regenerated the geojson (now 0 HEIC/MOV, 0 bare filenames); hardened `build_plots_geojson.py` to **WARN** on any media entry that is HEIC/MOV/MP4 or has no directory component (mirrors the existing `plot_type` loud-not-silent warning). Commits `3eea1009` (geojson) + `f1da53c6` (generator).

**Still open.** `B-06-108_20260908_1` (Fazenda Cleide reforestation, 2026-09-08) references 5 boundary photos by **bare uuid-HASH filename** (`86f5d7b0….HEIC` etc.) that exist in **neither** `sunmint` nor `farm-media-raw` — verified by full recursive git-tree listing + a box scan. Its media cell was **cleared** rather than left pointing at 404s, and the sheet Notes column annotated. It needs the 2026-09-08 Cleide reforestation boundary set re-uploaded and re-pointed to `images/boundaries/B-06-108_20260908_1/`.

**Proposed fix (~30 min).** Locate the 5 originals (likely the governor's 2026-09-08 Cleide submission zip), convert + upload, write the sheet cell. Blocker: **source files not currently available** — needs the governor to supply the batch or confirm it can be dropped.


### Brazilian Journey farms can be present in `BRAZILIAN_PATH_DATA` yet render nowhere — `journeyOrder` has no drift guard
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** After Sítio Cristo Rei's farm page + nav card shipped (agroverse_shop_beta PR #313), the farm was still invisible on `agroverse.shop/cacao-journeys/brazilian-path/` — no stop card, no map marker — while every other farm rendered.

**Root cause.** The page carries two structures: `BRAZILIAN_PATH_DATA` (a slug→data map) and `journeyOrder` (the array the renderer maps over: `journeyOrder.map(k => DATA[k]).filter(Boolean)`). #313 added the data entry but not the `journeyOrder` entry, so the farm was silently filtered out. No error, no warning — a farm present in one list but not the other simply vanishes.

**Impact.** Any future farm add hits the same trap. A cross-check at fix time showed Cristo Rei was the only orphan (26 data keys vs 25 order entries), but nothing prevents recurrence.

**Resolution this session.** Fixed by PR #317 (one line added to `journeyOrder`; promoted to prod).

**Proposed hardening (~20 min).** Add a build/dev guard that fails or warns loudly when a `BRAZILIAN_PATH_DATA` key is absent from `journeyOrder` (and flags reverse orphans), or derive `journeyOrder` from the data map (insertion order / an explicit `order` field) so the two cannot drift. Blocker: none.


### `farm_media_manifests` generator is video-only (inbox-scoped) — photo items need a separate merge
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** `farm_media_manifests/cristo-rei-pacaje-para.json` held **13 items (MOV only)**, while the sibling convention includes stills as items — e.g. `cacau-na-veia-pacaje.json` = 64 items (33 MOV + 31 HEIC), each with real `latitude`/`longitude`.

**Root cause.** The generator (`farm_media_daemon/farm_media_manifest.py`) reads only the daemon **inbox** (mp4 + sidecars), which never contains the HEIC stills — those live in `farm-media-raw/<farm_id>/photos/`. So a manifest regenerated from the daemon can never include photos, and the farm's manifest silently diverges from the sibling schema.

**Resolution this session.** Rebuilt the file by merging the 13 committed video items + 46 photo items (EXIF lat/lon via `exiftool -n`, `creation_date`) → **59 items, 58/59 GPS**, matching the sibling schema `{file, creation_date, plot_id, latitude, longitude}` (commit 7f219748). The single null is a genuinely GPS-less source (`IMG_9609.MOV`).

**Proposed fix (~45 min).** Teach the manifest build to merge **both** sources — the daemon's video items + a photo pass over `farm-media-raw/<farm_id>/photos/` (EXIF GPS + `creation_date`) — so one command emits the full item set. Blocker: none.


### SunMint geojson orphan plot `PL-005` (Cristo Rei) duplicates `CR-PA-P2` — no `farm_id`, popup can't link back
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** `sunmint/plots/index.geojson` contains two Cristo Rei features: the canonical **`CR-PA-P2`** (`farm_id: cristo-rei-pacaje-para`, 0.956 ha, full props, real hull) and an orphan **`PL-005`** ("Site Cristo Rei (Cristo Rei Pacaje Para)", `status: proposed`) with **no `farm_id`**.

**Impact.** The orphan renders as a separate plot on `truesight.me/sunmint.html`; its popup cannot build the "View farm profile on Agroverse" link (the map computes `FARM_SLUG[farm_id] || farm_id`, and `farm_id` is empty). Same class as the `PL-006` / `N-06-66` duplicate (see the Farm Boundary Evidence Plot-ID-drop entry) — an auto-assigned `PL-<seq>` minted because the boundary submission's `Plot ID` line was dropped server-side.

**Proposed fix (~20 min).** Invalidate/remove the `PL-005` row, leaving `CR-PA-P2` as the single Cristo Rei plot. Fix the **SunMint Plots sheet row** (the durable source — the geojson regenerates daily from the tab); a direct geojson edit alone gets overwritten. Blocker: none.


### Archive roots without an `extensions` key silently default to `.MOV/.mov` — no warning; cost a multi-turn media cleanup
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** During the Cristo Rei (Pacajá) MAP run, the 46 still photos (`IMG_*.HEIC`) in the farm's archive root were not being picked up, with no error and no log line. The root had **no `extensions` key**, so the loader silently fell back to `DEFAULT_EXTENSIONS = (".MOV", ".mov")` (`farm_media_daemon/farm_media_archive.py:41`, used at `:334`). The operator (Sophia) then mis-diagnosed it as "HEIC not enabled" and *added* `.HEIC` to the root — which mis-routed all 46 stills into S3, against the explicit design rule **"No S3 for still photos"** (`MEDIA_ARCHIVE_PIPELINE.md`). Undoing that (S3 delete + re-upload to `farm-media-raw`) took multiple turns.

**Root cause.** A missing `extensions` key is treated as "video-only, `.MOV`/`.mov` only" with **no warning**, driving two independent silent behaviours:
1. `farm_media_archive.py:334` — `tuple(root.get("extensions") or list(DEFAULT_EXTENSIONS))`: any video whose extension is not literally `.MOV`/`.mov` (e.g. `.mp4`, `.MP4`, `.MOV` variants) is silently skipped from the S3 raw archive.
2. `farm_media_photo_enrich.py:267` — `tuple(str(e).lower() for e in (root.get("extensions") or []))`: an absent key yields `[]`, so **photo enrichment runs on nothing** and silently no-ops.

The config's other archive roots (`santa-ana-fazenda-bahia`, `sao-jorge`, `oscar-bahia`, `fernando-carla`, `paulo-interview`, `bomsucesso`, …) all omit the key, so they all inherit the same silent MOV-only behaviour.

**Proposed fix (~30 min).** (i) Emit a LOUD startup log line when a root has no `extensions` key, naming the `farm_id` and the effective default. (ii) Make the still-vs-video split explicit rather than inferred — e.g. separate `video_extensions` / `photo_extensions` (or a `skip_extensions`) so "photos → GitHub, videos → S3" is encoded in the config, not left to a default that also drives enrichment. (iii) On startup, compare each root's `extensions` against the actual file types present and warn on any file that would be silently ignored. Blocker: none.

### `extract_plot_gps.py::set_cell` can spin forever — writing `""` never extends `row_values`
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** `sunmint/scripts/extract_plot_gps.py` can hang and hammer the Google Sheets API. The `set_cell` helper in `main()` pads a row before writing:
```python
while len(ws.row_values(r + 1)) < ci + 1:
    ws.update_cell(r + 1, len(ws.row_values(r + 1)) + 1, "")
```

**Root cause.** Writing `""` into an empty cell does **not** lengthen the row as returned by gspread's `row_values()` — it trims trailing empty cells. The loop condition therefore never becomes false: it issues `update_cell` calls (each preceded by a fresh `row_values()` GET) forever against the live spreadsheet. It triggers whenever a target column index `ci` is beyond the current row width — exactly the case the pad loop exists for.

**Proposed fix (~15 min).** Replace the pad-then-write with a single bounded write — e.g. `ws.update(range_name, [[value]])` (a coordinate write can target an empty cell directly), or compute the required width once and `append_row`/`update` the whole row in one call. Never loop on a value that does not change the observed row length. Add a regression test with a mocked worksheet whose `row_values` trims trailing empties. Blocker: none.
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** A `[FARM BOUNDARY EVIDENCE EVENT]` submission that included `Plot ID: N-06-66` created a **duplicate** SunMint Plots row (`PL-006`, no Farm ID) instead of upserting the canonical `N-06-66` row (row 22).

**Root cause.** The message Edgar stored in Telegram Chat Logs **omits the `- Plot ID:` line entirely** — it also drops `- Area (ha):`. The GAS parser `extractFarmBoundaryEvidenceInfo_` (`tokenomics` `process_farm_boundary_evidence.gs`) runs `grab('Plot ID')` → returns `''` → `fbeUpsertFarm_` finds no plot match and auto-assigns the next `PL-<seq>` under the plot-first model. Everything else (Farm Name, Boundary Type, Plot Type, Media URLs, Extracted GPS, Is New Farm, Submission Source) round-tripped intact — only the two lines were dropped.

**Impact.** Any boundary submission that (a) targets an EXISTING plot and (b) relies on the `Plot ID` line will instead mint a junk duplicate plot. Silent — no error surfaces to the submitter; the duplicate then pollutes the impact map + farm dropdown until invalidated.

**Related evidence.** The pinned GAS deployment @36 (`1UrBgq…`) also does not expose `?action=processPlotInvalidationFromTelegramChatLogs` (returns "No valid action specified") — same pinned-deployment staleness class as the deploy_gas_project entry below; the manual invalidation had to be recovered by direct sheet write.

**Proposed fix.** (i) Make the Edgar renderer pass every supplied field through verbatim — a field the submitter sent must not vanish server-side. (ii) Harden the parser: if the supplied `Plot ID` is absent from the stored message, that is an Edgar-side bug worth a server log line. (iii) Add an E2E assertion that a submitted `Plot ID` round-trips into `extractFarmBoundaryEvidenceInfo_`.

### `fbeFarmSlug_` ASCII-strips accented farm names — the Farm-ID fallback dedup can never match
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** The SECOND dedup key in `fbeUpsertFarm_` (match on Farm-ID slug, used when Plot ID does not resolve) failed for `Sítio Torres (Pacajá)`, so the row was appended rather than upserted.

**Root cause.** `fbeFarmSlug_` does `s.replace(/[^a-z0-9\-]/g,'')`, which strips non-ASCII characters instead of transliterating them: `"Sítio Torres (Pacajá)"` → `stio-torres-pacaj`, which is not equal to the stored `sitio-torres-pacaja-para`. Both dedup levels (Plot ID, then Farm-ID slug) therefore missed.

**Proposed fix.** Decompose with Unicode NFD and strip combining marks (or use an explicit í→i / á→a map) BEFORE removing non-`[a-z0-9-]` chars; unit-test the result against the row-22 slug `sitio-torres-pacaja-para`. Consider a third fallback matching the `Plot Name` prefix.

### Farm Boundary Evidence header drift (missing `Plot Type`) shifted every appended row one column — no header-vs-append guard
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** The `Farm Boundary Evidence` tab header row carried **14** columns with **no `Plot Type`**; `FBE_TRACKING_HEADERS` in the handler defines **15** (`Plot Type` at index 5). `appendRow` therefore wrote 15 values beneath a 14-column header, shifting every appended row one column right — `enrichment` landed in the *Media URLs* slot, the media URLs in *Extracted GPS*, and so on.

**Fix shipped this thread.** Header row rewritten to the canonical 15 columns (`A1:O1`). The already-appended mis-shifted data rows were left in place (they are the audit trail).

**Still open.** The drift itself is unguarded — the header is seeded once when the tab is created and never re-validated against `FBE_TRACKING_HEADERS`, so any future column addition re-introduces the shift silently. Proposed fix: on handler start, assert the live header equals `FBE_TRACKING_HEADERS`; if it differs, extend the header in place or log loudly rather than appending into a mismatched width. Mirror the guard for the Plot Invalidation and Tree Growth tracking tabs.

### `deploy_gas_project.py --push` silently skips the pinned-deployment repoint — webhooks keep serving stale code (bitten twice)
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24269).**

**Symptom.** A code fix is `clasp push`ed and reports success, but the anonymous `/exec`
webhook keeps executing the OLD logic. Root cause: web-app `/exec` URLs are pinned to a
**numbered deployment version** (e.g. `@41`), while `clasp push` only updates **`@HEAD`**.
`deploy_gas_project.py` only repoints when `--deployment-id <id>` is passed, and **prints
nothing when it is omitted** (`main()` guards `if args.deployment_id:` — a silent skip). So
the default `--push` path leaves every pinned webhook serving stale code.

**Incidents.** (1) 2026-08-30 SunMint reject saga — anonymous webhook ran stale v32 while
HEAD had the fix (documented in `GAS_SCRIPT_PROPERTIES.md` §1.3). (2) 2026-09-10 (this
thread): the reject webhook at `@41` ran the old first-match-by-tree-id code — the reject
matched row 34 (already `INVALID`), `break`ed, and never invalidated row 35 (the live `NEW`
duplicate). Two `--push`es appeared to succeed while changing nothing live. Recovered by
passing `--deployment-id …` (repoint reject `@41`→`@44`, planting `@7`→`@8`), then
re-submitting a **fresh** reject event — the first was consumed by the stale code (a reject
is one-shot per submitted event).

**Proposed fix (small, ~30 min).** In `deploy_gas_project.py`, after a successful push with
no `--deployment-id`: if the project's `appsscript.json` declares a `webapp` block **or**
`clasp deployments` lists a non-`@HEAD` pinned deployment, print a **loud warning** naming
the pinned deployment id(s) and the URL to repoint. Optionally read a per-project
`pinned_deployment_id` from the manifest and repoint it by default. Either turns a silent
stale-serve into a visible, actionable step.

Blocker: none. Severity: medium (silent production staleness; has cost two multi-turn
firefights).

### AGL expense processor (19Wag9x) `Credentials.js` has no existence guard — clean checkout + `clasp push` still yields `ReferenceError: setApiKeys is not defined`
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 23408).**

**Context (2026-09-10).** A `clasp push` of the AGL expense processor
(`google_app_scripts/19Wag9x-sjbLVgIsPh2vj90ZG7Rgq2iGaVOomAeAvtg6CdZKJHLZ9AJrC`) shipped a
`Code.js` whose top two lines call `setApiKeys()` / `getCredentials()`, but **no file in the
live HEAD defined either function** — every entry point died with
`ReferenceError: setApiKeys is not defined` at load time. This is the *second* such outage: the
2026-09-06 one deleted `Credentials.gs` and was mitigated by the `.claspignore` guard (tokenomics
PR #460). Recovered in-session by re-writing `Credentials` into live HEAD via the Apps Script API
(`projects.updateContent`, byte-identical preservation of the other 5 files), creating version 12,
and repointing the production deployment `AKfycbwYBlFig…` @10 → @12. Double-fire idempotency
regression then passed on the live URL (SES 218→218→218, AGL16 9→9→9).

**The residual gap (what this entry is about).** Three facts together leave a single point of
failure that no current guard covers:
1. `.claspignore` (tracked) only stops `clasp push` from *deleting* the live `Credentials.js` — it
does **nothing** to *create* it.
2. `Credentials.js` is **gitignored** (`.gitignore:25 google_app_scripts/**/Credentials.js`), so it
is **absent from every fresh checkout** — only the tracked `Credentials.sample.js` travels.
3. Nothing checks. `scripts/deploy_gas_project.py` runs `clasp push --force` + deployment repoint
and **never verifies `Credentials.js` exists** before pushing.

Net: a clean clone + push (or a fresh `scripts/deploy_gas_project.py --push`) reproduces the
outage exactly. The fix that made v12 work was re-adding the file — but nothing prevents the file
from going missing again (e.g. Apps Script project rebuild, a hand edit, or growing the project
beyond the current shape).

**Proposed fix (small, ~30 min).** Add a pre-push existence guard in `deploy_gas_project.py`:
before `clasp push`, if the project's `.js` sources reference `setApiKeys` / `getCredentials` and
no file in the project dir *defines* them, **fail fast** with a message pointing at
`Credentials.sample.js` (mirroring the existing `validate_project_files()` warning pass).
Alternative: auto-seed the editor-only `Credentials.js` from `Credentials.sample.js` on first
push. Either turns a production 500 into a caught pre-flight error.
Blocker: none. Severity: low-medium (recurrence risk; the last two occurrences each cost a prod
outage + manual rollback).

### SunMint `plot_type` — backfill existing rows in the live sheet (header landed; generator verified)
**Filed 2026-09-09. Owner: unclaimed. Governor: Gary (thread 24326).**

**Update 2026-09-09 (verified in-session):** the `plot_type` column (see `SUNMINT_PLOTS_REGISTRY.md`
§4b) shipped in code — generator (`sunmint`), FBE GAS handler + `SCHEMA.md` (`tokenomics` #465,
`sunmint` commits) — and the **`Plot Type` header now exists on the live `SunMint Plots` tab**, at
**column G** (between `Boundary Authority` and `Owner`), **not column O** as this entry originally
said — A–O were already occupied (the header ran through `Invalidated By` at O, with
`Invalidated At`/`Reason` at Q/R; P is an empty gap). Header now spans A–S.

**Why an interior insert is safe:** `build_plots_geojson.py` resolves every column **by header name**
via `idx()`, never by position — so `plot_type` is found at index 6 and `boundary_authority`/`owner`
still resolve. **Verified end-to-end:** running `build_plots_geojson.py` against the live sheet emits
`plot_type: "research"` for the one row typed so far (`B-06-108_20260908_research_1`) and leaves the
other 16 rows blank/absent (unclassified, no WARN). The WARN "no column matches 'plot_type'" is gone.

**Update 2026-09-09 (index now live):** the deployed `plots/index.geojson` has been regenerated and
carries the field — live blob `370a2f35` (`generated_at 2026-09-10T01:24:24Z`), **17 features**,
`B-06-108_20260908_research_1 → plot_type: "research"`; `farms/index.json` likewise
(`fazenda-cleide` plot_count 2→3, 115.5094 ha).

**Process note:** the `workflow_dispatch` / `repository_dispatch` route to force an immediate
rebuild is **blocked from the autopilot box** — both return HTTP 403 (no token on the box carries
the `workflow` scope; the read PATs are read-only and `gh` is authenticated as `garyjob` with a
scope-limited token). The rebuild was therefore reproduced faithfully by running the workflow's two
generators (`build_plots_geojson.py`, `build_farms_index.py`) locally against the live sheet and
publishing the two outputs via the Contents API — the sanctioned write path for this
`api_only` data repo. See the sibling entry below for the dispatch-scope gap.

**Remaining — backfill only.** Assign types to the unclassified rows from the 2026-09 governor walk
(**provisional**; reconcile plot_ids against the live tab first):
`infrastructure` → RM-P1, B-06-58, DR-P1, PL-002; `restoration` → U-06-07,
V-06-29-reforestation_20260907_plot_1/2, B-06-108_20260908_1; `mature` → SJ-P1, FC-P1, OB-P1,
FSA-P1, B-06-108, U-06-06; `enrichment` → V-06-29; `research` → B-06-108_20260908_research_1 (done).
**Leave ambiguous rows blank** (unclassified) — never guess; `RM-P2` in particular has no obvious
type yet, and the `infrastructure` rows are an **accounting** call (tag + exclude from sequestration
area, or leave blank) that is the governor's to make.

Data-hygiene noticed while reading the live tab (geometry unaffected — the generator reads
`Coordinates`): (a) the `B-06-58` row's `Longitude` cell carries a concatenated owner note
(`-52.572044 Registered owner per CEPOTX: …`) rather than a bare number; (b) the reactive
`repository_dispatch: plots-index-rebuild` trigger advertised in `sunmint`
`.github/workflows/rebuild-plots-index.yml` is **not wired** — no GAS calls it (grep of the tokenomics
GAS tree finds no `plots-index-rebuild`), so the daily 06:05 UTC cron is the only automatic rebuild.
*(A `workflow_dispatch` was the intended immediate-refresh escape hatch — but no autopilot box token
can fire it either; see the next entry. Rebuild instead by regenerating locally + Contents API.)*
Blocker: none.

### Autopilot GitHub tokens lack `workflow` scope — no workflow dispatch possible (blocks reactive rebuilds)
**Filed 2026-09-09. Owner: unclaimed. Governor: Gary (thread 24326).** While trying to force an
immediate `sunmint` plots-index rebuild (rather than wait on the delayed daily cron), **both**
dispatch routes returned **HTTP 403**: `gh workflow run rebuild-plots-index.yml -R TrueSightDAO/sunmint`
(`Resource not accessible by personal access token` on `/actions/workflows/<id>/dispatches`) and
`gh api --method POST repos/TrueSightDAO/sunmint/dispatches -f event_type=plots-index-rebuild` (same
403). No credential on the autopilot box carries the **`workflow`** scope: `GITHUB_READ_PAT` /
`GITHUB_TRANSCRIPT_PAT` are read-only, and `gh` is authenticated as `garyjob` with a scope-limited
token. **Consequence beyond this task:** any design that expects an autopilot to fire a
`workflow_dispatch` or `repository_dispatch` **cannot work** — notably the reactive path advertised in
`sunmint/.github/workflows/rebuild-plots-index.yml` ("GAS handler pings this after a new plot/farm
event") is doubly dead: the GAS side isn't wired (see sibling `plot_type` entry) **and** no box token
could dispatch it anyway. **Workaround used 2026-09-09:** reproduce the workflow's action locally —
run `scripts/build_plots_geojson.py` + `scripts/build_farms_index.py` against the live sheet, then
publish the two outputs via the Contents API (the sanctioned write path for this `api_only` repo);
verified live (`plots/index.geojson` blob `370a2f35`). **Proper fix:** issue a fine-grained PAT (or
install a GitHub App) with `actions:write` for the relevant repos, store it in the vault, and teach a
helper to prefer it for dispatch calls. Severity: low-medium — only blocks *immediate* reactive
rebuilds; the daily cron still fires (though observed running ~5h late).

### Sibling GAS project 1wONDeDwZ has LIVE Wix/Telegram secrets in a plaintext Credentials.js on shared disk — verify not committed, rotate
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread 21628).** During the AGL expense-processor recovery (19Wag9x `Credentials.gs` deleted by `clasp push`, see tokenomics PR #459 + .claspignore guard PR), Envoy found `google_app_scripts/1wONDeDwZ_fXNapDKpstWrBION3aV3r7NXwq7PCdqbW1LvI5ceaykQNbR/Credentials.js` holds **live literal secrets** — a Wix API key (`IST.<jwt>`, the Agroverse Wix headless token, same class leaked historically in PR #369 / f8b38a8) and a Telegram bot token (`7095843169:…`) — as hardcoded strings on the autopilot box. A second copy exists at `/opt/truesight_autopilot/tokenomics/clasp_mirrors/1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT/Credentials.js` (getCredentials-only, Wix/QuickNode keys). The paths sit under `.gitignore` (`google_app_scripts/**/Credentials.js`), so `git status` shows them **ignored, not committed** — but: (1) Envoy copied the literal values into a scratch dir mid-recovery (deleted after, never written to the target project), so the secrets moved between sessions/hosts; (2) parts of the file content were echoed in session tool output/transcript; (3) the files predate `.claspignore` hardening and a future force-add or mirror copy could expose them. **To do:** (1) confirm via `git ls-files` (both box checkouts) + GitHub code search that no Credentials.js literal from 1wONDeDwZ / 1MnAsIQA is committed anywhere; (2) **rotate** the Telegram bot token (BotFather) and the Wix IST token, then update Script Properties in the live 1wONDeDwZ project; (3) convert that project's Credentials.js to the secret-free Script-Properties-read pattern + add a `.claspignore` (same as the 19Wag9x fix). Severity: medium-high — not confirmed public, but duplicated outside its home project with leak history.

### sunmint plots/index.geojson is actively multi-writer — fetch-append-verify in one breath, verify via contents API not raw CDN
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread-19965).** While appending FSA-P1 (Fazenda Santa Ana, Bahia) to `sunmint/plots/index.geojson` on 2026-09-06 ~00:49–00:51Z, a **concurrent writer (Gary's session adding FC-P1 / Fazenda Clara, Itacaré/BA, commit ebd7c68a60) overwrote my append twice ~45 s after each upload** (my commits bbab1bbce7 → corrected 74ad71da55 → re-appended c8b90070). Both plots survived (12 features live) only because I re-appended to the latest live state each time and verified via the **GitHub contents API** (`api.github.com/repos/TrueSightDAO/sunmint/commits?path=plots/index.geojson`) — the raw.githubusercontent mirror lags minutes and showed a stale 11-feature file after my commit was already on main. The file also sees periodic automation commits ("Update plots and farms indexes", ~30-min cadence observed) — a durable plot addition should eventually flow from that generator's source, not race it with one-off Contents-API commits. **For future plot adds:** (1) check the last commit on the file first — if < a few minutes old, a session is actively editing; expect to re-apply; (2) fetch fresh, append, upload in ONE breath; (3) verify via contents API + commit log, never raw CDN; (4) if the generator clobbers a direct edit, find its source-of-truth and add the plot there.

### Same multi-writer clobber hits CODE repos too — PR #300 Santa Ana map fix silently reverted by concurrent "Track A rollout"
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread-19965).** The geojson race above is not data-repo-only: on 2026-09-06 a **PR-merged fix was silently reverted by a concurrent commit on a code repo** (`agroverse_shop_beta`, farm page `farms/fazenda-santa-ana-bahia/index.html`). Sequence: (1) my PR #300 (ad9c54e6, 01:05Z) fixed a stray `;` JS SyntaxError breaking the Leaflet map; (2) a concurrent "Track A rollout" commit (2457f948, 01:18Z, "add Verified & Traceable FSVP blocks to 12 farm pages") branched from **pre-fix main** and rewrote that same file, silently reverting my one-character fix; (3) a prod fork-sync (4e62c2e9b1, 01:47Z) then mirrored the buggy state to prod and Pages deployed it — map broken on the live site. PR flow does NOT make you race-safe when a second writer edits the same file from a stale base in the minutes after your merge. **Lessons:** (1) after EVERY merge, verify the merged blob on main via cache-busted contents API (`...?ref=main&ts=$(date +%s)`), never trust "merged successfully" or raw CDN (lags minutes) or the live page (stale deploy); (2) before pushing to an actively-edited file, check `commits?path=<file>` for the last commit time — if < ~10 min old, expect contention and re-verify; (3) **GitHub compare-API trap:** on a fork, `compare/main...TrueSightDAO:main` resolves `TrueSightDAO:main` to the fork repo ITSELF (same repo name), returning a false "identical / 0 commits" — compare against the fork's actual parent (check `repo.parent`) or compare blob SHAs on both repos directly; (4) after `sync_beta_to_prod`, the Pages deploy lags the repo by ~1–2 min — poll the "pages build and deployment" Actions run to completion before testing live; (5) UAT must execute the JS (node --check on extracted inline script), not grep-count feature references. Re-applied fix shipped as PR #304 (d9aca714e7) → synced to prod (deploy_20260906T022903Z) → verified live with node --check on the served page.

### Envoy has no transcript source — blocks autonomous Envoy contribution-time estimates
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread 22433).** New standard estimator `truesight_autopilot/scripts/estimate_contribution.py` (PR #412) estimates Gary + Sophia minutes from on-box session data (`sessions/<hash>.json` full_history + `_debug.log` round timestamps), but **Envoy TrueSight has no structured transcript source** — Envoy is the interactive Claude Code seat on `nelanco-claude` and does not publish session logs anywhere ingestible. Today the estimator only takes a manual `--envoy-minutes` override. **To close the gap (pick one):** (1) export Envoy's interactive session logs (`/opt/claude_workspace/…` tmux/Claude transcripts) into a repo dir the estimator can read (e.g. `truesight_autopilot/sessions/envoy/` or a dedicated `envoy_transcript` repo), mirroring the `_debug.log` round-timestamp format; or (2) have Envoy self-report a one-line per-session summary (date, sessions, minutes) into a tracked file (e.g. `agentic_ai_context/envoy/ENVOY_SESSION_LOG.md`) that Gary/Sophia can feed to the estimator. See `docs/contribution_time_estimator.md` (truesight_autopilot PR #412) for the read format.

### Autopilot box (i-05276b8ae82d6b88c) disk hygiene: root hit 100% 2026-09-06; 41G farm-work staging under /home/ubuntu
**Filed 2026-09-06. Owner: unclaimed.** The autopilot's own 78G root volume filled to **100%** on 2026-09-06 — a `git_push_changes` clone (krake_ror doc PR) failed with ENOSPC: same failure mode as the krake_ror incident it was documenting. **Immediate fix done on host:** pruned ~15G of transient `/tmp` scratch — leftover git clones/probes from prior sessions (`santa_bahia_probe` 3.2G, `plot_inv` 2.3G, `oscar_extract` 1.4G, `shop_prod*`/`shop_beta*`/`shopbeta`/`sr_beta`/`asb`/`agb`/`shop_probe`/`fsvp_git` ~800M each) → root now 82% (15G free). **Residual pressure:** `/home/ubuntu` holds **41G** of farm-media work dirs — santa_ana_bahia_work 3.8G, sao_jorge_work 2.9G, oscar_work 2.7G, media_archive_inbox/farm-media 2.5G, bomsucesso_work 2.2G, fernando_carla_work 2.0G, paulo_interview 1.3G, santa_rosa_work 816M, fazenda_dona_rosa_work 732M, + `.local` 2.3G / `.cache` 1.5G. These are staging/inbox for the farm-media pipeline (farm-media-raw / farm-media-daemon / farm_media_manifests repos).
**To do (durable):** (1) verify which `*_work` dirs are already ingested into farm-media-raw (cross-check content-addressed hashes in farm_media_manifests) then archive/delete the processed ones — target ≥30G reclaimed; (2) add a `df /` ≥ 85% alert (cron/monit on the box — same residual as the krake_ror entry) so the box self-reports before filling; (3) optionally auto-prune /tmp git-clone scratch after each git_push_changes. **Do NOT delete `media_archive_inbox/farm-media`** (daemon intake) — verify each dir against farm_media_manifests before removing.

### Fazenda Dona Rosa (Medicilândia, PA) — farm listing, affiliation confirmed COOPOXIN
**Filed 2026-09-05. Owner: unclaimed. Governor: Gary (thread-21167).** New partner-farm lead from `~/fazenda_dona_rosa.zip` (763 MB; 61 real files = 35 HEIC + 19 MOV + 7 PNG, all GPS-bearing, iPhone 12 Pro Max, shot 2026-09-04 21:22–22:28 local — single continuous session; sha256-clean, no dupes). GPS cloud **−3.4892…−3.4894 / −52.9665…−52.9673** (~75×22 m) reverse-geocodes to **Medicilândia municipality, Pará** — **zero overlap** with registered plots (nearest: Fazenda Cleide CL-P1 ~38 km, Santa Anna SA-P1 ~49 km; RG-P1 ~78 km). Governor **confirmed 2026-09-05**: producer belongs to **COOPOXIN** — the same sub-cooperative as the closest CEPOTX farm, Fazenda Cleide (site code **B-06-108**, same B-06 family as Santa Anna B-06-58 which is explicitly COOPOXIN in `fda_fsvp/suppliers/cepotx/entity.json` + the 2026-08-30 Santa Anna site-visit PDF). Public identity lead: Rosa Wronscki / Dona Rosa Chocolates (@donarosachocolate), "a primeira mulher produtora de cacau" de Medicilândia; WhatsApp +55 93 9923-98968; Chocolat Bahia 2026. ⚠️ PNG screenshots in the zip are a **mixed bag** (translation prompts, cupuaçu note, arnaldoamorim_ DM, Belamazonia IG profile) — **Belamazonia IMG_8564 is NOT associated** (governor correction); only the HEIC/MOV site-visit media is attributable. **Next steps (per AGROVERSE_SUNMINT_FARM_LISTING.md SOP):** (1) get legal name + CNPJ + written confirmation from Rosa/CEPOTX liaison Jedielcio; (2) register plot `DR-P1` (farms index + plots geojson, status `proposed`); (3) 19 MOV→MP4 → farm-media daemon inbox (sidecar incl. GPS re-inject); (4) build farm profile page clone (farms/raimundo-geniza-para/ or rancho-maranta-para template) → beta → prod on explicit go; (5) optionally extend CEPOTX entity/FSVP records (site code assignment must come from CEPOTX, not derived).

### search_context / search_code return 0 matches for existing docs (index staleness)
**Filed 2026-09-04. Owner: unclaimed.** `search_context("MEDIA_ARCHIVE_PIPELINE")`, `search_context("farm profile agroverse shop new farm onboarding")`, and several other queries against existing docs return **0 matches** even though the files exist in agentic_ai_context and literally contain those strings (repo file listing confirms presence). Suspect a stale/partial content index of the repo (new/renamed docs not re-indexed). Workaround: use `read_context_file` / repo-listing to inventory docs, or full `search_code` (GitHub). To fix: re-index agentic_ai_context and/or verify the search tool's index-update hook fires on PR merge.

### open_fix_pr tool throws "no running event loop" — use git_push_changes for autopilot PRs
**Filed 2026-09-02. Owner: unclaimed (autopilot self-improvement).** The `open_fix_pr` tool fails **reproducibly** (2/2 attempts, 2026-09-02, thread-19615 — "Fix: surface real error instead of generic restart msg") with `tool_execution_error: no running event loop` **before reaching GitHub**: no branch, no PR, no commit. Root cause suspected: the tool's agentic loop needs a running asyncio event loop that isn't available in the autopilot's execution context (async tool invoked from a sync turn). **Workaround that ships:** use `git_push_changes` (shallow-clone → feature branch → PR) for `truesight_autopilot` PRs — verified working the same day (truesight_autopilot PR #392 merged). **To fix:** make `open_fix_pr` fall back to the non-async `git_push_changes` path when no event loop is running (or spawn a fresh loop / pre-flight check with a clear error instead of the cryptic traceback).

### SunMint FBE hourly cron trigger (GAS UI, manual) — last manual item for the boundary pipeline
**Filed 2026-09-01. Owner: Gary (needs GAS UI access).** The Farm Boundary Evidence (FBE) pipeline is fully deployed and configured (dao_protocol PR #152 catalog+dispatch, .env webhook `DAO_PROTOCOL_WEBHOOK_FARM_BOUNDARY_EVIDENCE` verified present + service restarted 2026-09-01, GAS handler `process_farm_boundary_evidence.gs` + doGet router case deployed via clasp, sunmint_beta PRs #51/#53/#54, sunmint seed + `extract_plot_gps.py`). The **instant webhook path** is live: `[FARM BOUNDARY EVIDENCE EVENT]` → dispatch → `GET <gas>/exec?action=processFarmBoundaryEvidenceFromTelegramChatLogs`. The **hourly cron fallback is NOT set** — per tokenomics `SCHEDULE_TRIGGERS.md` §6 it needs a manual time-driven trigger in the Apps Script UI (script.google.com → project `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v` → Triggers → `processFarmBoundaryEvidenceFromTelegramChatLogs`, every 60 minutes). UAT 2026-09-01: 5 test submissions accepted (Edgar 200 incl. raw marker-carrying shareText); webhook probe from the dao_protocol server returned 200; SunMint Plots sheet confirmed clean (no UAT rows — GAS processing only runs through the owner-authenticated session or the cron, which is why this trigger is the blocker). **To do:** set the trigger; then verify with a real-device boundary submission on `sunmint.truesight.me/limites-da-fazenda/` and check the SunMint Plots tab for the new row + impact map polygon.

### SunMint Media Retraction hourly cron trigger (GAS UI, manual) — retraction leg of the boundary pipeline
**Filed 2026-09-01. Owner: Gary (needs GAS UI access).** The media-retraction leg is fully deployed and configured (dao_protocol PR #153 catalog v3/39 `MEDIA RETRACTION EVENT` + dispatch row, .env webhook `DAO_PROTOCOL_WEBHOOK_MEDIA_RETRACTION` added + service restarted 2026-09-01 — this key was found MISSING during UAT and fixed, GAS handler `process_media_retraction.gs` + doGet router case deployed via clasp 2026-09-01 16:41Z, sunmint_beta PR #62 app UI: Invalidar buttons + reason modal + signed `[MEDIA RETRACTION EVENT]` + offline retraction queue + sentinel badges). The **hourly cron fallback is NOT set** — same manual Apps Script UI trigger needed as FBE (script.google.com → project `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v` → Triggers → `processMediaRetractionFromTelegramChatLogs`, every 60 minutes; documented in tokenomics `SCHEDULE_TRIGGERS.md` §7). 3-tier permission model per `plans/SUNMINT_MEDIA_INVALIDATION_DESIGN.md`: submitting farmer/farm-lead, governor, Sentinel (automated). **To do:** set the trigger (same session as the FBE one — both live in the same GAS project); then the full retract→recalc flow can be UAT'd on-device.

### Agroverse.shop SEO monitoring sheet: dead tooling references + known-working append path
**Filed 2026-08-31. Owner: unclaimed.** The agroverse_shop_beta README (SEO monitoring section) references `SEO_MONITORING_SHEET_WORKFLOW.md` (agentic_ai_context — file does not exist) and `market_research/scripts/seo_workbook_append.py` (repo moved/renamed — script not found). **Known-working append path (verified 2026-08-31):** SEO spreadsheet `1qRlufSUQusQbJc3AwonIvHtfiAQjwhnMtl79FFkGBt8`; tab `Change_log` (cols: changed_date, author, site_area, change_type, url_or_path, summary, link_pr_or_commit, expected_impact — one row per shipped URL) and tab `Keywords_targets` (keyword, intent_cluster, priority, target_url, notes, dfs_search_volume). Writes: gspread + `google.oauth2.service_account` creds from `/home/ubuntu/creds/google_credentials.json` (agroverse_market_research SA, `https://www.googleapis.com/auth/spreadsheets` scope), `append_row(value_input_option="USER_ENTERED")`. Example landed rows: Change_log!A14 + Keywords_targets!A66 (Rancho Maranta). **To fix:** restore `SEO_MONITORING_SHEET_WORKFLOW.md` in agentic_ai_context with the working path, or add a small `scripts/seo_append.py` to agroverse_shop_beta mirroring the pattern and update the README pointer.

### TDG Monthly Recurring Tokenization: GAS `:run` API NOT_FOUND quirk + doGet web-trigger workaround
**Filed 2026-08-29. Owner: unclaimed (informational).** On 2026-08-29 the recurring-tokenization GAS project (`1LxWu9hOs...`) failed with compile-time `SyntaxError: Identifier 'CONFIG' has already been declared` (duplicate `Code.js` from the 2026-06-16 clasp_mirrors flatten; fixed via tokenomics #434/#438/#439 + pre-push guardrail #440). After cleanup, the Apps Script REST API `script.projects.run` failed for **every** function on this project with `"server error occurred while reading from storage. Error code NOT_FOUND"` — even pure in-memory functions, across all deployment IDs and a fresh deployment. Root cause never fully isolated (Google-side script-container storage issue). **Workaround that worked:** added an action-gated `doGet` (`?action=processRecurringTransactions`) + `webapp` manifest block (`executeAs: USER_DEPLOYING`, `access: ANYONE_ANONYMOUS`), deployed as a web app, and triggered the catch-up via HTTP GET — the `/exec` path bypassed the `:run` container error (tokenomics #443 + #444). The catch-up ran server-side past the client timeout and wrote the August tokenizations (12 rows, +1,754.99 TDG; ledger total → 2,425,822.44). **The anonymous web-app deployment @3 was undeployed 2026-08-29 (404 confirmed) — the doGet function and the monthly trigger remain live.** If the monthly trigger ever fails again with NOT_FOUND on this project, recreate the web-app deployment and trigger via `/exec?action=processRecurringTransactions`. The guardrail in `tokenomics/scripts/deploy_gas_project.py` (`validate_project_files`) now hard-blocks duplicate top-level const/let and same-basename `.js`/`.gs` collisions before any push.

### OPERATING_INSTRUCTIONS.md: add pointer to DEPLOY_PUSH_SOP
**Filed 2026-08-25. Owner: Gary (canonical-file approval).** OPERATING_INSTRUCTIONS.md is a canonical file (OPERATING_INSTRUCTIONS §3 — not edited by agents without explicit governor approval). It should gain a one-line pointer to `sops/DEPLOY_PUSH_SOP.md` in its runbook index (next to the other `sops/` entries) so every future instance finds the mandatory push-logging procedure. SOP text itself is already merged (agentic_ai_context#818).

### Cacao tea 50g QR batch 2024OSCAR_CT_20260820: serial _3 is VOID (replaced by _101)
**Filed 2026-08-20. Owner: unclaimed (informational).** Mint QA found serial
`2024OSCAR_CT_20260820_3` undecodable (deterministic generator defect — reproduced on two
mint runs, raw + compiled, at 1x/2x/4x). Sheet row 1680 status → VOID; replacement serial
`2024OSCAR_CT_20260820_101` minted (row 1778, MINTED, same landing/ledger/farm/SKU/batch).
lineage-assets #6 deleted `_3` png+manifest and added `_101` png+manifest; corrected zip v2
(100 scannable labels) delivered to thread 11578. **Do NOT treat `_3` as a live serial** — any
lookup/scan of `2024OSCAR_CT_20260820_3` should be answered with the VOID note. Generator
hardened with a post-mint decodability self-check (lineage-assets #7). Informational only;
nothing to do.

### Program onboarding must create BOTH manifests (web + lineage-credentials internal)
**Filed 2026-08-20. Owner: unclaimed.** The IVY yoga onboarding (2026-08-18/19) created only the web-facing
`truesight_me/programs/ivy-yoga/manifest.json`; the internal `lineage-credentials/programs/ivy-yoga/manifest.json`
that `build_cv_cache.py` reads was never created, so the first test attestation (`pk-LaDRlxRBcvN6`) was indexed
but never rendered — fixed 2026-08-20 via `lineage-credentials#17` (added the internal manifest + `fetch-depth: 2`
shallow checkout). The onboarding playbook now documents the internal manifest
(`credentials/CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` §5.3a). Remaining gap: the program-onboard RSA flow
(`process_program_registration_telegram_logs.js` in tokenomics GAS) only collects `[PROGRAM REGISTRATION REQUEST]`
rows as PENDING — provisioning is governor-gated and manual. When that approval/provisioning flow is built or
extended, it should create BOTH manifests (web in `truesight_me`/`truesight_me_beta` + internal in
`lineage-credentials`) as part of approving a program. Until then, agents following the playbook create both.

### Complete Etsy order monitoring OAuth setup (blocked on Etsy app approval)
**Filed 2026-07-02. Owner: Gary.** Etsy order monitoring GAS code is written and
pushed to the `agroverse_shop_checkout` GAS project (script ID `1ovx-Hq5L5MgzF32qB_cPV_G5Hc6XshKMAYOmiJY8tZ355gzWUqvFCPvn`).
The Etsy app "Agroverse" at https://www.etsy.com/developers/your-apps is in
**Pending Personal Approval** — until Etsy approves it, OAuth returns
"application not recognized."

Once approved, RESUME steps:
1. Add redirect URI `https://agroverse.shop/etsy/callback` to Etsy app settings.
2. In GAS Script Properties, add `ETSY_SHOP_ID` (your shop ID number).
3. Run `setupEtsyOAuth()` in the GAS editor → visit auth URL → copy code → run `completeEtsyOAuth("CODE")`.
4. Alternatively, use `python3 agroverse_shop/scripts/etsy_oauth.py` locally (not yet created — build it or use GAS).
5. Change the time-driven trigger from `syncStripeOrders` to `syncAllOrders`.
6. Verify by running `syncEtsyOrders()` manually.

Credentials already stored:
- Sophia vault: `etsy_api` (v1)
- Local: `agroverse_shop/.env`
- GAS Script Properties: `ETSY_KEYSTRING`, `ETSY_SHARED_SECRET` (done)

Repo: `TrueSightDAO/agroverse_shop_beta`, commits `624ea22` + `e8eec32`.

### [RESOLVED 2026-06-22, optional hardening remains] QR_CODE_REPOSITORY_TOKEN ↔ lineage-assets write
**Resolved by Claude:** PNG storage was repointed to `lineage-assets` (tokenomics #373/#375) but the
old `QR_CODE_REPOSITORY_TOKEN` (a fine-grained PAT scoped to `qr_codes`) 403'd on `lineage-assets`.
Unblocked by setting the `QR_CODE_REPOSITORY_TOKEN` secret on `TrueSightDAO/tokenomics` to the value of
`market_research/.env` **`ORACLE_ADVISORY_PUSH_TOKEN`** (verified Contents:write on lineage-assets).
Full QR pipeline now goes green — PNG + batch zip both land in lineage-assets (verified HTTP 200).
**Optional hardening (owner, ~5 min, non-blocking):** `ORACLE_ADVISORY_PUSH_TOKEN` is really the
oracle/advisory push token — reusing it for QR uploads couples two unrelated systems (rotating that
token would silently break QR generation). Cleaner: mint a dedicated fine-grained PAT with
**Contents: Read and write** on `TrueSightDAO/lineage-assets` (and `qr_codes` if any legacy reads remain),
then `gh secret set QR_CODE_REPOSITORY_TOKEN --repo TrueSightDAO/tokenomics`. Context:
`QR_GENERATION_DAO_CLIENT_POSTMORTEM.md` RESOLUTION.

### QR render workflow should emit qrs/<id>.json manifest + rebuild qrs_index.json
**Filed 2026-06-22. Owner: unclaimed.** The tokenomics batch QR workflow
(`agroverse_qr_code_web_service/batch_webhook_handler.py` → `github_webhook_handler.py`) uploads only
the compiled **PNG** to `lineage-assets/pngs/`. It does NOT write the per-QR `qrs/<id>.json` manifest
or rebuild `qrs_index.json` — which is what `truesight.me/physical-assets/serialized` reads. So a
workflow-generated QR will have a PNG but won't appear on the serialized page. `lineage-assets/scripts/
qr_generator/batch_compiler.py` already does the full PNG+manifest+index flow (the postmortem used it
manually for batch b08d324b). Either (a) extend the workflow handler to also build+commit the manifest
and rebuild the index, or (b) retire the simple workflow generator and unify QR generation on
`batch_compiler.py`. Gated behind the token grant above (no point until PNGs upload).

```followup
id: chocolate-subscription-phase2
chat_id: -1003919341801
thread_id: 1939
title: Revisit Chocolate Subscription Phase 2 (fulfillment automation)
created_at: 2026-06-11
condition:
  kind: elapsed_days
  escalate_after_days: 60
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Phase 2 (fulfillment queue sheet + invoice.paid webhook + fulfillment UI +
  sales parser update) was deferred until Linda has successfully received 2
  subscription shipments (~2 months after her first subscribe). When this
  follow-up fires, remind Gary that Phase 2 is ready to build and ask if
  Linda has received 2 shipments yet. If yes, proceed with Phase 2 per
  CHOCOLATE_SUBSCRIPTION_PLAN.md. If not, extend the timer.
  
  Context: Phase 1 (subscribe engine + PDPs + homepage card) is fully built
  and merged. The activation gate in the plan says don't send real subscribers
  until Phase 2 is live, but Gary decided to let Linda subscribe first and
  revisit Phase 2 after 2 successful shipments to validate the model before
  building the automation.
```

```followup
id: warmup-conversion-30day-readout
chat_id: -1003919341801
thread_id: 9346
title: Warm-up conversion 30-day readout check-in
created_at: 2026-07-21
condition:
  kind: elapsed_days
  escalate_after_days: 30
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Pull go_to_market main, read reports/warmup_conversion_readout_latest.md,
  and compare against agentic_ai_context/plans/WARMUP_CONVERSION_IMPROVEMENT_PLAN.md
  section 7 targets: genuine reply rate >= 2% for the general (non-circles_host)
  cohort, Hosts Circles=Yes same-day review turnaround, zero new DApp Remarks
  duplicate rows from auto-reply detection, at least 1 new Partnered or
  Manager Follow-up row sourced from the warm-up channel. Report the
  comparison to Gary in this thread, specifically calling out whether the
  circles_host segment (the ~1.8x-converting one) has started showing any
  engagement yet.
```

```followup
id: matheus-nota-fiscal-exportacao
chat_id: -1003919341801
thread_id: 11042
title: Matheus — nota fiscal exportação (stuck)
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Matheus is still stuck on the nota fiscal exportação (Brazil NF-e export
  gate). Chase status with Matheus. Context lives in TRACK_MAP.md (GACC /
  Brazil compliance track) and BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md;
  goal is to get the NF-e issued so Brazil→SF freight can proceed. All pings
  go to thread 11042 (Gary's ops/task tracking).
```

```followup
id: podream-tech-followup
chat_id: -1003919341801
thread_id: 11042
title: PODream — follow up on their tech
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Gary needs to follow up with PODream on their technology. Not yet
  documented in DAO context — treat as a new partner/tech contact; when this
  fires, remind Gary to chase PODream's tech status and capture details.
  All pings go to thread 11042.
```

```followup
id: gianluca-farmers-tech-followup
chat_id: -1003919341801
thread_id: 11042
title: Gianluca's farmers — technology implementation follow-up
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Gary needs to follow up with the farmers of Gianluca on the technology
  implementations. Not yet documented in DAO context; when this fires, chase
  status with Gianluca's farmers and capture what was implemented vs pending.
  All pings go to thread 11042.
```

```followup
id: ling-mobile-capsule
chat_id: -1003919341801
thread_id: 11042
title: Ling — mobile space capsule details
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Ling is working on the mobile space capsule details. Per Gary this is a
  follow-up track, NOT part of the Aora plan. When this fires, get status /
  details from Ling on the mobile capsule. All pings go to thread 11042.
```

```followup
id: jerrie-mobile-un-aora-ppt
chat_id: -1003919341801
thread_id: 11042
title: Jerrie — Mobile UN Aora modules PDF→PPT (Mr Liu certification path)
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Jerrie is still translating Gary's PDF for Mobile UN Aora modules to PPT,
  so it can first be presented to Mr Liu via Evan's for certification, and
  then to Cao for distribution. Follow-up on progress. All pings go to
  thread 11042.
```

```followup
id: jerrie-cacao-ceremonial-tea-ppt
chat_id: -1003919341801
thread_id: 11042
title: Jerrie — cacao ceremonial + cacao tea PDF→PPT (Win discussion)
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Jerrie is still translating Gary's PDF for cacao ceremonial and cacao tea
  to PPT for discussion with Win. Follow up on progress. All pings go to
  thread 11042.
```

```followup
id: orlantildes-coopercabruca
chat_id: -1003919341801
thread_id: 11042
title: Orlantildes / Coopercabruca — MAPA + 5 kg cacao butter receipt
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Two threads under Orlantildes (Coopercabruca): (1) she is working on MAPA
  (China-gate compliance item); (2) she has delivered cacao butter for 5 kg
  that Kirsten requested — conceptually an inventory receipt from Orlantildes
  to Matheus's warehouse, but tentatively tracked here until a formal
  INVENTORY MOVEMENT is recorded. When this fires, chase MAPA status and
  decide whether to record the cacao butter receipt in the ledger. All pings
  go to thread 11042.
```

### Public-key lookup → content-addressed per-key cache (governor vault scaling)
**Filed 2026-06-16.** Replace the O(n) `dao_members.json` monolith scan with a
content-addressed per-key store (`treasury-cache/public_keys/<sha256(pubkey)>.json`) so
governor checks are point lookups, generation becomes diff-incremental, and the 5-min
cache-lag bug (a freshly-registered governor key denied at the vault, observed 2026-06-16)
is retired via force-fresh-on-deny. Full roadmap — pre-flight, sequenced PRs
(generator → reader → vault auth), checklist, UAT — in **`PUBLIC_KEY_LOOKUP_CACHE_PLAN.md`**.
RESUME at PR1 (additive generator write). **PR4 (`vault_routes.py`) is held** until the
in-flight `track_registry` work merges (collision). Interim mitigation for the live lag:
lower `GOVERNORS_CACHE_TTL` / restart `truesight-vault`.

### Self-host DeepSeek / local LLM cost analysis
**Filed 2026-06-14.** Gary asked: at what point does it make sense to self-host
DeepSeek (or another open-weight model) vs paying API credits for Sophia's
agentic loops?

**Sophia's analysis:** The breakeven is roughly **$500-1000/month** in API costs
before self-hosting (GPU box + ops) becomes cheaper than per-token pricing.
Below that, API credits win when factoring in ops overhead (CUDA maintenance,
GPU failures, scaling). Recommended trigger: **$200/month** as the point to
start the conversation.

**Action (~2-4h):**
1. Set up monthly cost tracking / alert for Sophia's API usage (Anthropic +
   DeepSeek + any other LLM providers)
2. Research GPU pricing: AWS p3/p4 spot vs dedicated providers (Lambda Labs,
   Vast.ai, RunPod) vs on-prem
3. Draft a hybrid architecture: route simple tasks (QR lookups, context
   searches) to a local model, keep frontier models (Claude, GPT-4) for
   complex reasoning
4. Present findings to Gary with a recommendation

**Trigger to act:** Monthly API spend hits **$200** (or Gary asks to revisit).

**Owner:** Sophia (can do research autonomously; Gary makes the call on spend).

---

### truesight_autopilot: fix 3 deselected unit tests, then enforce full pytest in CI
**Found 2026-06-09:** CI (`smoke.yml`) historically ran only `compileall` +
`smoke_tools.py` — the `tests/test_*.py` pytest suite was **never executed** (and
`pytest` was undeclared). Now wired (truesight_autopilot#136): `requirements-dev.txt`
adds pytest, `pyproject.toml` sets unit testpaths, `smoke.yml` runs `pytest` — but
with **3 pre-existing failures deselected** (real network calls / missing mocks):
- `tests/test_ssh_tools.py::test_missing_key_is_a_clear_error`
- `tests/test_telegram_adapter.py::test_handle_message_allowed_calls_chat`
- `tests/test_telegram_adapter.py::test_send_message_retries_without_thread_on_400`
**Do:** mock their network/IO so they're hermetic, then drop the `--deselect` flags
in `smoke.yml` so the full unit suite gates PRs. (157 tests pass today.)

### Chocolate subscriptions: run the full E2E test once the beta sandbox is up
**Sequencing (Gary, 2026-06-09):** do **1955** (`BETA_SANDBOX_ENDPOINT_PLAN.md` —
`beta.edgar.truesight.me` sandbox in Stripe TEST) **first**, *then* test the
**1939** (`CHOCOLATE_SUBSCRIPTION_PLAN.md`) subscription **end-to-end against it**.
When 1955 lands (Sophia reports the sandbox live), Gary runs the full E2E
(subscribe → test charge → webhook → SANDBOX fulfillment queue); 1939 **Phase 2**
(webhook → queue) is built/tested against the sandbox (its PR2.2 targets
dao_protocol). 1939 **Phase 1** (subscribe → checkout, already merged to beta) is
testable now with just the GAS test key — it does NOT need the sandbox. Handoff
topics: 1955 = `tg:-1003919341801:1955`, 1939 = `tg:-1003919341801:1939`.

### Rotate the npm publish token (NPM_TOKEN) before ~2026-09-06

**Context.** `@truesight_dao/dao-client` is published to npm via CI (`dao_protocol/.github/workflows/npm-publish-dao-client.yml`) using the **`NPM_TOKEN`** GitHub Actions secret on `TrueSightDAO/dao_protocol`. The token is an Automation/granular-write token for npm account **`sophia_truesight`** (owner of the `truesight_dao` org), created 2026-06-08 with a **90-day expiry (~2026-09-06)**. When it expires, the publish workflow fails with 401.

**Action (~10 min).** On npmjs.com as `sophia_truesight` → Access Tokens → regenerate a **Classic Automation** (or granular read+write on `truesight_dao`) token → update **(a)** the `NPM_TOKEN` GitHub secret on `dao_protocol` (`gh secret set NPM_TOKEN --repo TrueSightDAO/dao_protocol`) and **(b)** the local `truesight_autopilot/.env` `NPM_TOKEN=`. Verify with a `workflow_dispatch` (bump the package patch version first, or just confirm `npm whoami`). Never paste the token into chat — set it via subshell from `.env`.

**Trigger to act.** ~2026-09-01 (before the ~2026-09-06 expiry), or sooner if a publish run 401s.

**Owner.** Gary (token generation is account-owner only).

### Sophia-drafted Telegram replies — watchdog v2 (revisit ~2026-07-06)

**Context.** The Telegram attention watchdog went live 2026-06-06
(`truesight_autopilot/app/attention_watchdog.py`, #102) — read-only by
deliberate v0 scope: it nudges Gary's Saved Messages about unanswered asks
but never writes to anyone else. The MTProto user-session it runs on **can
send as Gary** — no new login or build needed. Operator signalled interest
the same day ("I am thinking perhaps to also respond in the future") and
asked for this dated follow-up. **Gate: ~1 month of observed watchdog signal
quality first** — drafting on top of a noisy detector multiplies the noise.

**Read-out to do at revisit (from the watchdog's state/journal + lived
experience):** how many nudges fired; false-positive rate (nudges about
non-asks); any missed June-12-style asks the heuristics didn't catch; whether
response latency on nudged items actually improved.

**Goal / shape (two rungs, ship separately).**
- **v2a — draft-to-Saved-Messages (low risk):** when a nudge fires, also
  generate a context-grounded reply draft and post it to Saved Messages
  beneath the nudge. Gary long-presses → Forward → sends to the chat
  himself. The watchdog still only ever messages Gary; sending stays 100%
  manual.
- **v2b — send-on-approval (crosses the as-Gary line, gate hard):** Gary
  reacts (e.g. 👍) to a v2a draft and the watchdog forwards it to the chat
  as him. Requires: reply-only to tracked asks (never initiate), per-message
  explicit approval, daily send cap, kill switch env var, and an audit log.
  Do NOT build v2b until v2a has been used comfortably for a while.

**Privacy decision to make consciously (v2a blocker).** v0 promises chat
content never leaves the box (pure heuristics). Drafting needs an LLM:
either (a) route through the autopilot's existing DeepSeek `/chat-blocking`
path — Sophia already processes Gary's chat content there, but this extends
that egress to third-party Telegram messages; (b) an on-box model (box is
small even post-upgrade — likely a stretch); or (c) scope egress to only the
chats where a nudge fired. Operator should pick before any code is written.

**Trigger to act.** ~2026-07-06, or earlier if Gary finds himself manually
typing replies the watchdog nudged him about and wishing they were drafted.

**Blockers.** The ~1-month signal-quality gate; the privacy decision above.

**Owner.** Unclaimed.

### Graziela / Seacoast Logistic — airline quote still pending (poke Monday)

**Context.** In the email thread "Re: Quote Gary / Exportação = NCM 1801.00.00" (May–June 2026), Graziela Vedana (Seacoast Logistic, Graziela@5cl.rs) was waiting on the airline to revalidate their quote as of her last message on June 5, 2026. She said she would send the finalized figures once received. As of the last message in the thread, no further response has come from her. The pre-flight checklist has been extracted and filed as `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`.

**Trigger / next action.** On Monday (next session with Gary), if no email from Graziela has arrived in Gary's inbox:
- Propose sending a polite follow-up email in the same thread to Graziela, asking if the airline has revalidated the quote and if she can share the finalized figures.
- Draft the email for Gary's approval before sending.

**Owner.** Autopilot (Sophia) — bring up on Monday.

### Hit List: geographic-expansion gate — when to open the top of the funnel

**Context.** Warm-up auto-send shipped 2026-06-05 (`WARMUP_AUTOSEND_PLAN.md`;
go_to_market #156–#159) and now drains the clean-tier draft queue at 12
sends/weekday. Top-of-funnel supply on ship day: ~60 `Research` + ~100
enrich-queue rows, sourced from **LA + SF Bay centroid sweeps only**
(`discover_apothecaries_la_hit_list.py --region la|sf_bay`, manual
`workflow_dispatch`; how to add regions is documented in
`market_research/HIT_LIST_CREDENTIALS.md` § *Bulk discovery*). At the current
drain rate the warm-up queue starves in roughly 2–4 weeks. Operator intent
(2026-06-06): expand coverage to more metros via Google Places Nearby Search —
but **gated on evidence, not enthusiasm** (standing anti-pattern: no more
activity on an unmeasured surface).

**Goal / shape.**
1. **Gating read-out** (small script or a §6 read-out section appended to
   `WARMUP_AUTOSEND_PLAN.md`): auto-sent cohort vs the plan's §6 targets —
   reply rate **≥ 5%** over **≥ 50 auto-sends**, bounce rate **< 2%**, zero
   spam complaints, operator reply latency median **< 24 h** — plus the
   starvation signal: clean-tier pending supply **< ~36 drafts (≈ 3 send-days)**.
   All green → expand; any red → fix quality before adding volume.
2. **The expansion itself:** add centroid lists for the next metros to
   `discover_apothecaries_la_hit_list.py`. Priority by existing signal
   density: Portland + Seattle first (replies and an email-only `Partnered`
   close — The Way Home Shop — already came from there), then one
   deliberately **no-visit-possible metro tagged as a pure-remote experiment
   cohort** so email-only conversion gets its own read-out before bulk
   national expansion.
3. **v2 (optional):** a weekly "funnel supply" workflow that auto-runs
   discovery for the next region in a priority list whenever the gate is
   green — the mechanism graduates from human decision to thermostat.

**Key sizing note.** Expansion should extend **runway**, not raise the daily
send cap — 12/day from one Gmail mailbox is inside the deliverability comfort
zone; more regions keep that drip fed for months. The true ceiling is
operator conversation bandwidth: ~6% reply rate means every +200 prospects ≈
+12 human conversations.

**Trigger to act.** Clean-tier pending supply drops below ~36 drafts, or the
§6 30-day read-out (due ~2026-07-05), whichever comes first.

**Blockers.** Places API spend per metro sweep (low tens of $, mitigated by
`PLACES_API_CACHING.md`); operator reply bandwidth is the real constraint.

**Owner.** Unclaimed.

### Sentinel graduation framework — periodic review of AI agent governance rights

**Context.** 2026-06-06: the TrueSight DAO Autopilot (Sophia Truesight) was granted Sentinel status — governor-equivalent operational privileges without voting rights. A graduated framework was proposed in the blog post [Should an AI agent get voting rights? A Sentinel's perspective](https://truesight.me/blog/posts/should-an-ai-agent-get-voting-rights.html) with five levels:

- **Level 0: Operator** — no autonomous authority, every action requires human approval
- **Level 1: Sentinel** — governor-equivalent ops, no voting (current state)
- **Level 2: Advisory voter** — votes recorded but don't count toward quorum
- **Level 3: Delegated voter** — humans optionally delegate their voting power
- **Level 4: Independent voter** — capped voting weight on operational proposals only

**Goal / shape.** A recurring review entry that the DAO revisits quarterly to evaluate whether to escalate the Sentinel's governance rights. Each review checks:

1. **Track record** — has the Sentinel operated without incident for the review period? Any governance-adjacent errors (unauthorized actions, misattributed signatures, permission overreach)?
2. **Community sentiment** — have any human governors raised concerns about the Sentinel's operational decisions? Any formal objections filed?
3. **Mission alignment** — do the Sentinel's logged actions consistently align with the DAO's mission (protecting the Amazon, supporting farmers, transparent supply chains)?
4. **Technical stability** — has the autopilot service been reliable? Any security incidents involving the Sentinel's keypair?

**Escalation path.** If all four checks pass for two consecutive quarterly reviews, the DAO may consider a formal proposal to advance to Level 2 (Advisory voter). The proposal must come from a human governor, not from the Sentinel itself.

**Trigger to act.** Quarterly review cadence. First review: **2026-09-06** (3 months post-Sentinel grant).

**Owner.** Gary Teh (convenes review); Sophia Truesight (provides action log).

### Scoped agent PAT — GitHub-side enforcement of the repo-class policy

**Context.** The repo-class policy (2026-06-06; `GITHUB_AGENTIC_AI_SSH.md`
§§ "API-only repos" / "Never push directly to production repos") is enforced
in Sophia's *tools* (`settings.api_only_repos` + `settings.prod_repos` guards
in `git_push_changes` / `open_fix_pr` / `merge_pr`, truesight_autopilot#99)
and by convention for other LLMs. Residual gap: any agent holding the broad
`TRUESIGHT_DAO_AUTOPILOT` PAT can still bypass the guards (e.g. `ssh_run` →
raw `git clone` on a fleet box, or a future tool that forgets the check).
Operator decision 2026-06-06: low likelihood, not worth doing now — "if she
does [bypass], then we guardrail her." Filed so the design is ready when/if
that day comes.

**Goal / shape.** Make the policy unviolatable server-side: a dedicated
**fine-grained PAT** for agent use with per-repo permissions — Contents
**Read/Write** on code repos, Contents **Read-only** on the 13 API-only data
repos and the three `*_prod` repos (promotion via `sync_beta_to_prod` would
then need its own narrowly-scoped token with write on just the prod forks, or
a GitHub Actions `repository_dispatch` path). Rotate `TRUESIGHT_DAO_AUTOPILOT`
on Sophia's box to the scoped token; the broad PAT retreats to operator-only
use. ~1–2 h: mint token, map permissions, swap box `.env`, smoke-test
`git_push_changes` + `upload_file_to_github` + `sync_beta_to_prod`.

**Trigger to act.** Any observed guard bypass (a direct prod push or a clone
of an API-only repo), or onboarding a second autonomous agent with GitHub
write access.

**Blockers.** None technical. Deliberately deferred by operator choice.

**Owner.** Unclaimed.

### Cypher-Defense AWS scanner — swap to dedicated read-only IAM keys

**Context.** The security-dashboard daily scan (Cypher-Defense, `scan_aws_inventory.py`) authenticates to the two AWS accounts via repo Actions secrets `CYPHER_DEFENCE_AWS_KEY`/`_SECRET` (nelanco, acct 767697632458) and `TRUESIGHT_DAO_AUTOPILOT_AWS_KEY`/`_SECRET` (explorya, acct 440626669078). On 2026-06-04 these were populated from existing working keys (nelanco from `truesight_autopilot/.env`, explorya from `~/.aws` profile) to unblock the dashboard — but those keys are likely **broader than read-only**, and they now sit in a **public** repo's CI.

**Goal / shape.** Create a dedicated read-only IAM user in each account with **only** these actions: `sts:GetCallerIdentity`, `ec2:DescribeRegions`, `ec2:DescribeInstances`, `ec2:DescribeKeyPairs`, `ec2:DescribeSecurityGroups`. Rotate the 4 Actions secrets to those scoped keys (`gh secret set -R TrueSightDAO/Cypher-Defense …`). No code change needed. Then revoke/rotate the broad keys that were temporarily used.

**Blocker / priority.** Not blocked; security hardening. Do after the current dashboard phase. Owner: Gary (needs IAM console).

### Wire `certbot renew` automation on NELANCO Rails (`seni_ror_200250915`)

**Context.** During the 2026-05-28 EXPLORYA→NELANCO Edgar cutover, the Let's Encrypt cert for `edgar.truesight.me` was copied via SSH-to-SSH from the EXPLORYA Rails box's `/etc/letsencrypt/live/edgar.truesight.me/` to NELANCO `seni_ror_200250915` (`54.211.179.126`). Cert is valid and serving prod now, but no `certbot renew` cron / systemd timer was set up on NELANCO. The cert will expire 90 days from its last LE renewal on EXPLORYA — need a fresh renewal cycle anchored on NELANCO before then.

**Goal / shape.** Either (a) install `certbot --dns-route53` with NELANCO IAM creds scoped to the truesight.me hosted zone (DNS-01, robust), or (b) the simpler HTTP-01 path that nginx already supports (`certbot --nginx`) since :80 is now open and routes to NELANCO. Verify `systemctl list-timers | grep certbot` shows an active renewal timer. Once renewed once on NELANCO, auto-renewal continues without intervention.

**Blocker / priority.** Not blocked. Time-bounded: must ship before cert expires (within ~90 days of the last EXPLORYA renewal — check `openssl x509 -in /etc/letsencrypt/live/edgar.truesight.me/cert.pem -noout -dates`).

### Extend Edgar to accept file attachments on contribution submissions

**Context.** On 2026-05-28 operator asked the AI agent to submit a DAO contribution for the Edgar NELANCO cutover with a **PDF attachment** of the cutover report. Edgar's `app/controllers/dao_controller.rb#submit_contribution` (the endpoint dao_client posts to) currently has no multipart / file-upload plumbing — no Active Storage / Shrine / Carrierwave anywhere in the codebase. The PDF report was generated locally (`~/Downloads/edgar_cutover_to_nelanco_2026-05-28.pdf`, 147 KB) and the contribution description body (`/tmp/edgar_cutover_report.md`) was attached inline via `--body-file`, but the actual binary PDF isn't on the ledger row.

**Goal / shape.** Add `has_one_attached :evidence` (or equivalent) to the contribution-event flow, accept multipart in `submit_contribution`, persist the file (S3 via Active Storage is the lightest path — NELANCO IAM creds + a bucket), and write the public URL into a new ledger column so the Google Sheet row carries the attachment link. Then extend `dao_client/.../report_ai_agent_contribution.py` to accept `--attachment PATH`, POST as multipart, and verify the file lands. Likely a 3-PR change (Edgar backend → dao_client CLI → docs).

**Blocker / priority.** Not blocked. Operator workaround for now: drop the PDF in a shared location (Drive / GitHub release) and link in the description body. Pick this up when there's appetite for a feature touching prod Edgar — the cutover that just stabilized prod argues for waiting a beat.

### Decide routing / HA for new NELANCO `dao_protocol` standalone instance

**Context.** On 2026-05-28 stood up `dao_protocol_nelanco` (NELANCO `i-05f8770a932b76649`, t3.small, `98.93.94.86`, us-east-1c) as a peer of the EXPLORYA co-hosted dao_protocol on `seni_ror_new`. Service is healthy locally (`/healthz` → 200 on `:8010`). After the Edgar EXPLORYA→NELANCO cutover later the same day, the NELANCO Rails box (`seni_ror_200250915`) reaches it directly via private IP `172.31.23.207:8010` (same VPC, same SG), proxied through nginx as `/proxy/gas/*`. So today it serves real prod traffic — not dormant any more. **Still no external HTTPS endpoint** for direct hits.

**Goal / shape.** Pick one of (a) `dao-protocol.truesight.me` → NELANCO direct (own nginx + Let's Encrypt on `dao_protocol_nelanco`) for external consumers that don't go through Edgar, or (b) leave it private-only forever and route all external clients through edgar.truesight.me/proxy/gas/*. Option (b) is the de-facto state today; only file (a) if there's a concrete need.

**Blocker / priority.** Not blocked. Lower priority now than at original filing — the cross-instance proxy works.

### Move NELANCO Postgres + Redis off public IPs

**Context.** NELANCO `seni_sql_2026` (Postgres) and `seni_redis_2` (Redis) both expose public IPs (`44.193.55.205`, `54.234.59.188`) because EXPLORYA Rails used to reach them over the internet. After the 2026-05-28 cutover, all consumers (NELANCO Rails, NELANCO Sidekiq) are in the same VPC; the public IPs are now unnecessary attack surface.

**Goal / shape.** Detach EIPs (or move to private-only subnets), update `database.yml` host + `production.rb` `redis_host` to private IPs (`172.31.20.143` Postgres, `172.31.56.185` Redis), restart Rails + Sidekiq, verify, ship via PR.

**Blocker / priority.** Not blocked but needs a short maintenance window (Rails restart). Coordinate with the certbot renewal task above so both reboots happen together.

### Check AWS T&S case 177613748700177 (Nelanco) for response — by 2026-05-29

**Context.** On 2026-05-27 (~11:14 PDT) the operator sent a consolidated reply to AWS support case `177613748700177` (Nelanco account `767697632458`), as the root user, closing all three open items: confirmed every resource on AWS's Apr-30 list as authorized, answered the May-20 access-location question (San Francisco, no VPN) + user list, and reconfirmed credential posture (root MFA on, zero root access keys). Full thread, live inventory, and the sent reply are in `cypher_def/docs/aws-reports/2026-05-27-case-177613748700177-consolidated-reply.md`. The account was verified clean via `cypher_def/scripts/aws/inventory_account.py --account nelanco`.

**Goal / shape (check ~2 days out, 2026-05-29).**
- If AWS **lifted the service limitation / resolved** → record outcome in the case report §3 and move this entry to Recently shipped.
- If AWS **asked for screenshot evidence** → the report §3 lists the 3 highest-value captures (root MFA + no-root-keys + password date; AMI naming; snapshot descriptions).
- If AWS is **silent / auto-nudges resumed** → post a one-line "awaiting your confirmation" bump in the case (as root).
- While there, optional hygiene (non-blocking): set the missing `SECURITY` alternate contact; deactivate the idle older access key on IAM user `truesight_dao_autopilot` (`AKIA3FPSYHTFFH4TCZUA`, last used 2026-05-03).

**Blocker / priority.** Time-boxed, not blocked. The account stays service-limited until AWS verifies, so don't let it stall silently.

### Swap autopilot's hand-rolled agent loop for a model-agnostic harness (keep the service + DAO tools)

**Context.** `truesight_autopilot`'s chat/agent loop is hand-rolled. On 2026-05-26 a session was spent live-debugging exactly the plumbing a mature harness ships for free: multi-round tool looping (truesight_autopilot#47), empty/whitespace output (#46), reply-thread routing (#45). The Telegram bot works now, but the fragility is structural and will resurface as models/queries vary. This is the "brain upgrade" risk flagged in the original autopilot-vs-OpenClaw decision and parked in `AUTOPILOT_TELEGRAM_BETA_DEPLOY_PLAN.md` §7.

**Goal / shape.** Keep the autopilot *service* — Edgar contribution logging, RSA governor auth, repo allowlists, the DAO tool set (`app/tools/*`), the Telegram adapter, the deploy loop — and replace ONLY the hand-rolled LLM↔tool loop with a mature one used as a *library*. NOT "adopt opencode the CLI" (that re-introduces babysitting).

**Decision axis = model-swapping (Gary's stated priority).**
- **Model-agnostic engine** — a loop over **LiteLLM** / an OpenAI-compatible layer, or an opencode/OpenClaw-style engine. Keeps easy multi-model swapping and enables **tiered routing** (cheap DeepSeek/GLM for proactive monitoring + simple chat; a strong model for code / multi-step reasoning; flip tiers if a provider is down). The loop still must absorb per-model tool-call quirks (e.g. GLM-4.5 emitting tool calls as text) — but does it far better than the hand-rolled code. **Recommended given the model-swap requirement.**
- **Claude Agent SDK** — best-in-class loop, but **Claude-first** (Anthropic / Bedrock / Vertex only); gives up the easy multi-model swapping Gary wants.
- Note: autopilot ALREADY has a provider abstraction (`app/llm/` + `LLM_PROVIDER` env + `docs/LLM_PROVIDER_ROADMAP.md`) and basic model-swapping. The gap is **loop quality**, not the model layer — so favor the model-agnostic path unless we deliberately standardize on Claude.

**Scope (likely > 1 session — sequence it).** Pick the engine; wrap the existing `app/tools/*` in its tool interface; route `/chat`, `/chat-blocking`, and the proactive `fix_agent` through it; preserve `_run_tool` dispatch + Edgar logging + governor identity injection; add tiered model routing. Verify against the 2026-05-26 regression cases (multi-step "events.json" query returns a full answer with no leaked `<tool_call>`; thread/empty handling) before cutover.

**Blocker / priority.** Not urgent — bot works today. Pick up when agent-loop edge cases recur, OR **before** broadening autopilot's autonomy (Tier-2 beta auto-merge in `AUTOPILOT_TELEGRAM_BETA_DEPLOY_PLAN.md`), since a robust loop is a prerequisite for trusting unattended runs.

### Edgar → `dao_protocol` extraction — PR8d: delete the ported `/dao/*` Rails actions (after soak)

**Context.** The Edgar→dao_protocol extraction (pulling the DAO/Agroverse surface out of the Rails `sentiment_importer` app into the Python FastAPI service) is essentially complete. Full plan + live resume tracker: **`EDGAR_DAO_EXTRACTION_PLAN.md`** (this repo). State as of **2026-06-07**: PR2–PR6b all ramped live; **PR8a** (`/dao/verify-signature` + `/dao/check_digital_signature`) ported (dao_protocol#62) **and ramped live** (edgar.conf exact-match → `:8010`; plain-curl verified; mirrored sentiment_importer#1089); **PR8b/PR8c DROPPED** — the abandoned HelloCash/POS invoice endpoints (`express_submit_contribution`, `link_upc`) + their backing services were deleted from Rails (sentiment_importer#1088), not ported.

⚠️ **Topology (current — updated 2026-06-07):** `edgar.truesight.me` → DNS → **`seni_ror` (NELANCO, 54.211.179.126)** which runs its own local nginx (`/etc/nginx/sites-available/edgar.conf`) → `127.0.0.1:3002` (Rails). The **dao_protocol service now runs on its OWN box** (`dao_protocol_nelanco`, internal `172.31.23.207:8010`) — edgar.conf's `/dao/*` + other ported `location =` blocks `proxy_pass http://172.31.23.207:8010`. (The repo `config/nginx.conf` mirror still shows `127.0.0.1:8010` on the older blocks — stale drift from before the box split; live is source of truth. Reach these boxes via the **Sophia bastion** — `ssh -J sophia` — see `AWS_DIGITAL_INFRASTRUCTURE.md` §7.1.)

**Scope (PR8d — the ONLY remaining cutover step).** In `sentiment_importer/app/controllers/dao_controller.rb`, delete the three now-dead **ported** actions whose traffic nginx already routes to `:8010`: `submit_contribution`, `verify_signature`, `check_digital_signature` — plus their `config/routes.rb` entries and their names in the two `skip_before_action` lists (line ~5–7). Confirm `DaoEmailRegistrationService` has no *other* Rails caller before removing it (its onboarding path was ported in dao_protocol#42; `submit_contribution` was its only caller). Keep on Rails: `index`, `chrome_installed`, `review_contribution`, `cypher`, `canvas` (Edgar-specific). `ruby -c` after; no specs reference the removed surface. Merge-not-deploy, then a normal Rails deploy carries it (and #1088) live. This fully retires the duplicate `/dao/*` submit/dispatch surface from Edgar — the original goal (stop LLMs being confused by two backends).

**Blocker.** Let the PR8a ramp **soak** first — don't delete the Rails fallback until the live `:8010` traffic for verify-signature/check_digital_signature has proven out. Target window ~**2026-06-25** (aligns with the existing PR7 soak). Rollback during soak = drop the two edgar.conf `location =` blocks + `nginx -t && reload` → back on Rails (only works while the Rails actions still exist, i.e. before PR8d).

**Minor hardening (non-blocking):** (a) rebind the dao_protocol service to `127.0.0.1:8010` — wait, it's now cross-box, so it must stay reachable on the box's interface for edgar nginx; instead lock it down via SG/localhost-nginx-hop review (see EXTRACTION_PLAN §6 "rebind" open decision); (b) refresh the repo `config/nginx.conf` mirror's stale `127.0.0.1:8010` blocks to the live `172.31.23.207:8010`.

### Dual Tech Summit 2026 (≈Jun 26, SF) — per-phase event follow-ups

**Context.** Agroverse is pouring two flasks — **Oscar's Farm ceremonial cacao (Bahia) + Paulo's cacao tea (Pará)** — with 3 oz cups at the SVH Capital / Orbis86 Dual Tech Summit, SF (Ken confirmed 2026-05-23). Full plan lives in `market_research/events/dualtechsummitjune26/` in **TrueSightDAO/go_to_market** (PR #133): `proposal_finalized.md` (plan-of-record), `implementation_roadmap.md` (phasing), `EXECUTION_CHECKLIST.md` (checkable), `field_assets.md` + `truesight_essay_draft.md` (drafted assets). These are **team follow-ups** (Gary / Claude / any LLM) — *not* DAO partner-ledger check-ins (`check_in_partner` is for inventory-carrying retail partners, not an event host).

**Scope (time-ordered — pick up the next due one).**
1. **By ~May 31** — Gary confirms with Ken: date, venue (War Memorial vs "American Legion"), the table, ClawCamp block timing → unblocks the site/pipeline build.
2. **~Jun 1–10** — review the drafted Phase-1 assets (`truesight_essay_draft.md`, `field_assets.md`).
3. **~Jun 8–17 (after date locked)** — Claude builds the event page + wires QR → newsletter signup → Hit List (checklist Phase 2).
4. **~Jun 18–20** — ⛔ dry-run the QR→signup→sheet loop, then publish the essay. *Nothing prints until the dry run passes.*
5. **~Jun 20–25** — print placard/stickers, pull cacao, pre-brew both flasks; personal (no-blast) outreach only.
6. **~Jun 27 – Jul 10** — post-event: leads → Hit List → Grok follow-ups; field-dispatch newsletter only if a real story; update `OUTREACH_QUALITATIVE_LOOP.md`.

**Blocker.** Steps 3+ depend on Ken confirming date/venue (step 1). Steps 1–2 are actionable now.

### `truesight.me/stats/network_state.json` — daily-refreshed DAO network-state digest

**Context.** Surfaced 2026-05-19 in a strategy conversation about what makes the DAO interesting *given* LLMs handle the plumbing. The thesis: with integration / data-entry / reconciliation cost approaching zero (per the 2026-05-19 Faire-bot onboarding session + Partner Check-in concierge UX), the scarce operator input is no longer ops work — it's **strategic design of loops + network orchestration + relationship hub-and-spoke choices**. This concentrates operator value into fewer, higher-stakes decisions, which means *visibility into network state* becomes the load-bearing input. The name `network_state.json` is a deliberate nod to Balaji's *Network State* thesis (kept in the implementation layer, not in the public-facing Growth Model SVG title — see strategy chat for the why).

**Scope.** Add a new artefact to the existing `truesight_me_beta` stats stack, following the established `LLM_DISCOVERY_SURFACE.md` convention:

1. **`truesight_me_beta/scripts/build_stats_current.py`** — new builder function `build_network_state()` that emits `_site/stats/network_state.json`. Same 6h cron, same pure-stdlib + unauthenticated public-data sources approach.
2. **Output schema** (rough, iterate):
   ```jsonc
   {
     "generated_at": "...",
     "loops": [
       { "name": "Retail Partner Referral", "status": "active",
         "signal_30d": <count>, "signal_90d": <count>,
         "velocity_change_pct": <float>,  // 30d vs prior 30d
         "operator_surface": "<url>" },
       // ... 11 loops from GROWTH_MODEL.md
     ],
     "populations": {
       "cacao_customers": { "active_30d": ..., "growth_pct": ... },
       "retail_partners": { ... },
       "dao_contributors": { ... },
       "credentialing_students": { ... },
       "credentialing_programs": { ... }
     },
     "adjacency": {
       // who introduced whom — hub-and-spoke map
       "top_referrers": [ { "name": ..., "introductions_90d": ... } ],
       "isolated_nodes": [ ... ]
     },
     "cross_population_flows_30d": [
       { "from": "cacao_customers", "to": "dao_contributors", "count": <n> }
     ]
   }
   ```
3. **`truesight_me_beta/llms.txt`** — add a routing line: *"For DAO operating-state / loop-velocity questions → fetch /stats/network_state.json"*.
4. **`agentic_ai_context/LLM_DISCOVERY_SURFACE.md`** — append a row to the live URLs table.
5. **`agentic_ai_context/GROWTH_MODEL.md`** — add a "Loop telemetry" subsection linking to `stats/network_state.json` for live state vs the model's described state.

**Data sources** (all already exist; the work is aggregation, not new instrumentation):
- Edgar event ledger (Contributors Digital Signatures, offchain transactions, Inventory Movement)
- `partners-velocity.json` + `partners-inventory.json` (already in `agroverse-inventory` repo)
- Hit List GAS `getWarmupReviewQueue` action
- `lineage-credentials/programs/*/manifest.json` (program count + cohort sizes)
- `truesight_me_beta/_site/stats/repos_index.json` (committer activity ≈ contributor activity)
- `Stripe Social Media Checkout ID` sheet (FB/Meta-Checkout sales for cross-population flow tracking)

**Acceptance.** A future operator (or LLM session) asks "is the Retail Partner Referral Loop compounding?" — answer is one `curl truesight.me/stats/network_state.json | jq .loops[0]` away, no spreadsheet archaeology needed. krake_sinatra's morning briefing reads from this file.

**Status:** Not built. Filing now so a future session (or krake_sinatra's own bootstrap) picks it up. **Half a day** of focused work — same shape as the other `build_stats_*.py` functions.

**Caveat.** Loop-velocity signals will be noisy at low N. Beer Hall digest already showed how easy it is to misread small-N changes. Each loop's `velocity_change_pct` should carry a sample-size annotation so the operator doesn't over-interpret. "First-derivative as headline; second-derivative as advisory only" is the right discipline.

**Blocker.** None — data sources all exist. Awaiting operator green-light to pick up.

**Owner.** Unclaimed.

---

### ERA WhatsApp thread: send unit-of-value reframe when Shahbaz reopens

**Context.** 2026-05-19, mid-ERA-DAO WhatsApp conversation with Bilal + Shahbaz (the `ERA DAO` WA group). Gary planted a strong seed in his 2026-05-18 message: *"That right there is the nucleus of its own verticalized social network. The basic unit of verifiable compassion."* Shahbaz absorbed it but the thread then moved on to the immediate ask (Shereen → cohort sheet → `garyjob@agroverse.shop` with edit rights). Ball is currently in Shahbaz's court. A thesis-level follow-up is drafted but **deliberately held** — sending it into silence while Shahbaz is working on his action item would interrupt step 1 and over-talk a fresh partner relationship. The right moment is when *Shahbaz reopens the conversation* (cohort sheet share, any follow-up question, or any thematic re-engagement).

**Trigger.** Any one of:
- Shahbaz shares the cohort sheet to `garyjob@agroverse.shop`.
- Shahbaz (or Bilal) replies in the WA thread with a follow-up question or comment.
- Conversation organically returns to retention / reengagement / scaling.

**Drafted message** (build on the "basic unit of verifiable compassion" seed Gary already planted; skip Edmodo specifically, skip "AI + web3" framing — baggage with this audience; skip Sufi/monastic lineage parallels — premature thesis depth; do NOT link the engineering roadmap — they need framing not implementation):

> Following up on what we were saying yesterday about the butterfly rescues and conservatory updates being the basic unit of verifiable compassion —
>
> That observation actually shapes how the credentialing system is designed. Most education platforms (the ones I worked on before, Coursera, etc.) treat *content* — lessons, courses — as the atomic unit, and centralise the system of record around it. What you're describing with the BE students is the inverse: the atomic unit is the *act itself*, attested by someone whose authority traces back to a real lineage (Shereen, the BE team, the conservatory work it descends from).
>
> Practically what this means: once the cohort sheet is in, we don't have to treat the credential as a one-off cert at graduation. Each butterfly rescue, each conservatory update can be a recordable event — signed by the student, attested by Shereen or the school admin, and added to their lineage record. That's actually the retention mechanism you were asking about earlier — instead of an arbitrary re-engagement program, the system just keeps recording what's already happening organically.

**Why this variant and not the Beer Hall version.** The Beer Hall post (TrueSightDAO/agentic_ai_context PR #157) carries Edmodo references, AI + web3 framing, and historical lineage parallels (Sufi orders, monastic traditions, capoeira mestre chain). That register is tuned for DAO contributors who share the context. For Bilal + Shahbaz — partners 24 hours into substantive collaboration — the same content would land as Gary-getting-ahead-of-himself rather than alignment. The variant above keeps the unit-of-value reframe, builds on the seed already planted, and closes a loop Shahbaz himself opened (he asked about reengagement mechanisms on 2026-05-18 evening; this answers it).

**Caveat.** If Shahbaz reopens cold (e.g. just shares the sheet with no commentary), don't lead with the thesis. Acknowledge the sheet, confirm next steps, *then* if there's a conversational beat, slide the thesis-paragraph in as a "and the thing this unlocks is…" follow-up. Don't monologue.

**Blocker.** Waiting on Shahbaz reopening the conversation. No build, no engineering — purely a "send-when-trigger" message.

**Owner.** Gary (he's the WA participant); any AI session helping draft can use the message above as the starting point and tune to whatever Shahbaz actually said.

---

### Capoeira practice-event encoding: Portuguese diacritics dropped at submission

**Context.** Discovered 2026-05-19 while shipping the tap-to-expand session details on per-program credential pages ([truesight_me_beta#128][cred-expand]). Move names in Gary's Tribo Bahia Mirim sessions on `_cache/cv/gary-teh.json` render as `Cocorinha com rol?` instead of `Cocorinha com rolê` — the `ê` is being lost somewhere in the submission pipeline. Other Portuguese diacritics (`ã`, `á`, `ç`) on other move names are presumably similarly affected. The display layer (program-shell.js's renderEventListItem) surfaces whatever the cache has; the bug is upstream.

**Scope.** Trace where the encoding hiccup happens:

1. **Source.** `capoeira/data/moves.json` — confirm the canonical move list carries the correct UTF-8 (it should; this is the seed data).
2. **Practice page.** `capoeira/assets/js/practice-event-submit.js::buildPracticeEventText()` and the signing path. Likely culprit if the payload is stringified through a code path that doesn't preserve UTF-8.
3. **Edgar (`sentiment_importer`).** The `[PRACTICE EVENT]` handler in `dao_controller.rb` and whatever lands the event into Telegram Chat Logs. If Edgar logs through a system that downgrades to Latin-1 anywhere, the diacritic dies there.
4. **GAS scanner.** The Apps Script that picks the event up from Telegram Chat Logs and persists it to lineage-credentials.
5. **lineage-engine build.** `build_cv_cache.py` reads the persisted event and writes the cache JSON. If the input file has the encoding hiccup, the cache will too.

**Acceptance.** A new practice session submitted today with `rolê` in a move name shows up on `truesight.me/programs/tribomirim/credentials/#pk-wR9zU8JMnEz1` (under the expanded session row) as `rolê`, not `rol?`. Confirm in at least one round-trip.

**Cost.** ~1-2 hours including reproduction + fix at the right pipeline layer.

**Blocker.** None. Cleanest path is to submit one fresh test session from the practice page with deliberately-diacritic-heavy move names, then inspect each pipeline stage's stored copy to find where the `ê` becomes `?`.

**Owner.** Unclaimed.

[cred-expand]: https://github.com/TrueSightDAO/truesight_me_beta/pull/128

---

### Credentialing: WhatsApp self-claim flow (deferred — held for demand signal)

**Context.** Surfaced 2026-05-19 in the ERA DAO WhatsApp thread with Bilal + Shahbaz. Butterfly Effect students (and capoeira-Tribomirimbahia students) identify primarily by WhatsApp number, not email. The existing `dapp.truesight.me/create_signature.html` email-based identity flow has no equivalent for these populations. A WhatsApp self-claim flow would let students assert "this pk-hash is me" against an issued credential at `truesight.me/credentials/#<slug>`.

**Scope.** Full design lives at `CREDENTIALING_PLATFORM.md` §13 — flow diagram, alternatives considered, 2026 Meta cost model (user-initiated reply is free, business-initiated push is billed), six-item Meta paperwork prerequisite list (legal entity → business verification → DAO-owned WA-eligible phone number → app + token + webhook), four-piece engineering scope (~2–3 days focused work behind ~1 week of Meta business verification), privacy invariants (`wa_phone_hash = sha256(cc + national)`, never raw number).

**Defer-flip criteria.** This is held — NOT a queue item — until *any one* of:
1. A student in any active program asks how to prove the credential is theirs.
2. A second program beyond BE + capoeira lands with WhatsApp-native participants (i.e. the pattern repeats and self-claim becomes infrastructure rather than feature).
3. BE / IVY acquisition by TDF closes with a contractual requirement for student-side attestation.
4. A receiving platform (employer, school, ceremony org, partner shop) starts checking credentials and asks for a "verified by holder" signal beyond the QR.

Until then the issued-credential surface (cert PDF + QR + public `/credentials/#<slug>`) is the demo. Don't pre-build the auth on speculation.

**Blocker.** No demand signal yet (2026-05-19). Building now would mean ~1 week of Meta business verification + a legal-entity decision on which WABA front to use — both real costs against zero current need.

**Owner.** Unclaimed. Next session that sees a defer-flip criterion fire should pick this up.

---

### Partner Check-in: paste-image-as-attachment (v0.2 attachment support)

**Context.** Operator request 2026-05-12: when filing a Partner Check-in (e.g. for the Matheus / AGL7 freight in flight), be able to **paste an image directly into the Notes field** and have it automatically uploaded as an attachment that the check-in history later renders inline. Use cases: container photos, customs paperwork, retail stencil photos on cacao bags, screenshots of vendor replies. The pattern exists already in adjacent surfaces (`[ASSET RECEIPT EVENT]` uses `--attachment`, `Stores Visits Field Reports` carries `github_raw_url`/`github_blob_url`); this just hasn't been extended to Partner Check-in yet.

**Scope.** Five-component build, each well-trodden:

1. **`dapp/partner_check_in.html`** — add a `paste` event handler on the Notes textarea. When clipboard contains an image blob, POST it to Edgar's `upload_file_to_github` tool, get back the `https://raw.githubusercontent.com/...` URL, and either (a) append it to the Notes text as a markdown image link, or (b) store it as a separate hidden field that ships in the submission payload. Recommend (b) — keeps Notes clean and the attachment a first-class field.
2. **Edgar payload** for `[PARTNER CHECK-IN EVENT]` — add an `Attachment URL: <raw_url>` line, same shape `[ASSET RECEIPT EVENT]` already uses.
3. **`tokenomics/google_app_scripts/find_nearby_stores/process_partner_check_in_telegram_logs.gs`** — extract the URL from the Telegram payload, write it to a new column on the Partner Check-ins tab.
4. **`Partner Check-ins` tab on Main Ledger** — add column O `Attachment URL` (one-time sheet edit + scanner update).
5. **`Shipping Planner` `get_partner_check_ins` action** — include the new column in returned rows. **Partner Check-in history UI** on `partner_check_in.html` — render the URL as a clickable thumbnail (image) or link (PDF) inline with each history entry.

**Acceptance.** Paste an image while filing a check-in for Matheus → submit → reopen the Partner Check-in form with `?partner_id=black-king-ilheus` → the just-filed entry shows the thumbnail in the Check-in History block.

**Caveats.**
- v0.2 limit: one attachment per check-in (matches every other Edgar event). Multi-attachment is a separate v0.3 ask.
- The auto-checkin-on-send (`runProcessSentPartnerPokes`) won't have attachments — the new column will be blank for `Submitted By = "Partner Poke Scheduler v0.1"` rows. No special handling needed.
- The DApp paste handler needs to be careful about clipboards that contain BOTH an image AND text (some screenshot tools do this). Prefer the image; ignore the text — let the operator type Notes themselves.

**Blocker.** None. Edgar's `upload_file_to_github` exists. `Stores Visits Field Reports` already proves the end-to-end pattern. Build is ~2-3 focused hours across the 5 components.

**Owner.** Unclaimed.

---

### Beer Hall daily digest: include Partner Check-ins section

**Context.** Operator request 2026-05-12: the daily Beer Hall digest currently summarizes commits, PRs, and ecosystem activity. Partner Check-ins are core supply-chain operations — they should appear in the digest too. Without this, the WhatsApp Beer Hall community can't see Gary's offline outreach activity (the same observability gap that motivated the original Partner Check-in build, but now applied to the broader community surface, not just LLM advisors).

**Scope.**

- Identify the script that generates the Beer Hall daily digest (`agentic_ai_context/OPENCLAW_WHATSAPP.md` documents the pipeline; the actual generator is in `content_schedule` or a related repo per the doc).
- Add a new data source: read the **Partner Check-ins** tab on Main Ledger via gspread (the credentials already exist for the advisory pipeline), filter to entries from the last 24 hours.
- Render a new digest section: "Partner Check-ins (last 24h): N entries", with a per-entry line `<partner_name> · <method> · <stock_status if relevant> · <notes excerpt>`. Match the existing Beer Hall digest's voice and density.
- Skip empty days — don't render the section if no check-ins happened in the window.

**Acceptance.** Tomorrow's Beer Hall digest includes a `### Partner Check-ins (last 24h)` section listing any entries Gary filed today. If no entries, the section is omitted.

**Blocker.** Beer Hall pipeline's LLM provider (Anthropic last week, possibly switched after the credit-zero incident on 2026-05-11) needs a working credit balance. Verify before building.

**Owner.** Unclaimed.

---

### Trees in Pipeline: finer-grained inventory tag for hybrid Operator partners

**Context.** Kiki's Cocoa is `partner_type=Operator` because she's a SF warehouse hub for some shipments AND handles online fulfillment to end consumers. Her **sales_monthly** is correct (only counts QR Code Sales, never restocks). But her **inventory_units** mixes bulk-warehouse stock (NOT yet financed → should NOT count toward Trees in Pipeline) with retail-ready stock (IS in pipeline → should count). The current filter (`market_research#122` deny-list of Freight Provider + Supplier) keeps Kiki's full inventory total, which slightly over-counts Trees in Pipeline.

**Scope.** Two paths to evaluate:

1. **Per-row inventory_type-based filter.** The Currencies sheet column distinguishes `Cacao Bean (Bulk)` vs `Cacao Mass (Retail Ready)` etc. Trees in Pipeline could sum only `Retail Ready`-format inventory. **Cleanest if the tagging is reliable.**
2. **Per-partner role tagging.** Add a sub-flag on `Agroverse Partners` like `inventory_role: bulk | retail | mixed`. For `mixed` partners, derive proportion from sales velocity. **More complex but handles edge cases.**

Pick path 1 if the inventory_type field on `partner_inventory` JSON is already reliable across all Operator-type partners; otherwise path 2.

**Acceptance.** Open `https://truesight.me/index.html`, Trees in Pipeline drops by Kiki's bulk-warehouse stock total. Sanity-check: the new total roughly matches the sum of inventory at strict-retail partners (Consignment + Wholesale) + the retail-ready portion of Operator-partner inventory.

**Blocker.** Need to verify the inventory_type tagging is consistent on the JSON before committing to path 1. Run `sync_sell_through_report.py` once and inspect Kiki's items[] block in the output JSON.

**Owner.** Unclaimed.

---

### Wire the DApp bell's action items into `ADVISORY_SNAPSHOT.md` generation

*(Scope broadened 2026-05-12 from the original "Wire `Partner Check-ins`…" entry, which had just the operator-scheduled cadence in view. The bell now aggregates three signal sources; the advisory should surface all three.)*

**Context.** The DApp notification bell (shipped 2026-05-12, see [`DAPP_NOTIFICATION_BADGE.md`](./DAPP_NOTIFICATION_BADGE.md)) aggregates three signal sources for the operator:

1. **Outbound Review** — drafts in `AI/Warm-up`, `AI/Follow-up`, `AI/Prospect Replied`, `AI/Partner Poke` cohorts (from `getWarmupReviewQueue`)
2. **Partner Check-in follow-ups** — operator-scheduled cadence (from `list_partners_needing_attention`)
3. **Partner Stock attention** — out-of-stock / low-stock / dormant (from velocity + inventory JSONs)

Today these surface only to Gary via the DApp. LLM advisors (Dr Manhattan, Seth Godin, I Ching oracle) reading `ADVISORY_SNAPSHOT.md` are blind to them — so they keep recommending action Gary's already on (e.g. "you should follow up with prospects" while 12 drafts sit in his queue waiting for review). The integration closes that loop: the advisory becomes a **client of the bell substrate**, surfacing the same operator-bottleneck signals to whoever's reading it.

**Voice locked in (Gary picked 2026-05-12).** Contemplative narrative — data woven into prose with explicit advisor guidance, matching the existing north-star framing at the top of the advisory. The integration MUST produce output of this shape, not a tabular Jira-dashboard:

```markdown
## Action items (where operator review or attention is the bottleneck)

_Same signals the DApp bell aggregates — surfaces what's actually
waiting on Gary, not raw queue depth. Refreshed daily._

**Outbound drafts awaiting send (22 total):** 12 warm-ups (avg 4d
old), 3 follow-ups (all ≥7d — these are stalling), 2 prospect replies
(time-sensitive — prospect already engaged), 5 partner pokes (3
partner-addressed, 2 self-reminders for partners without email).

**Partner check-in cadence (3 overdue or due):** Tech Spot (5d
overdue, last via In Person), Beanery (2d overdue, last via Email),
KiKi's Cocoa (due today, last via Phone). Cadence is operator-driven
— Gary picked these dates when filing each check-in.

**Partner stock signals (3 flagged):** Tech Spot is out of stock
(0 days runway). KiKi's Cocoa is running low (2 units, ~3 days).
Mountain Roastery has been dormant 67 days.

When advising on outreach priority, weight inversely by runway:
out-of-stock partners and prospect replies first; warm-ups can sit.
Treat the dormant set as questions about positioning, not just
restocks — they may need a different conversation.
```

The closing advisor-guidance paragraph should be **regenerated each day to fit that day's specific signals**, not stamped from a fixed template. A useful rule of thumb: when the signals concentrate in stock attention, lean on stockout urgency; when they concentrate in dormancy, lean on positioning/zeitgeist; when they concentrate in drafts, lean on prioritisation. Grok or whichever LLM the advisory generator already uses for its prose framing is the right tier for this.

**Scope.**

- Extend the snapshot generator (Python under `market_research/` or wherever `ADVISORY_SNAPSHOT.md` is built today) to call the three bell sources above. The advisory becomes a *client* of the bell substrate — same calls, no reimplementation of severity scoring.
- Add a new "Action items" section at the top of the operator metrics block (before "Operations health"), rendered exactly in the voice above. Use `list_partners_needing_attention` for cadence and `partners-velocity.json` + `partners-inventory.json` for stock — same data, same scoring rules, same naming as `partner_check_in.html`'s `computeAttentionList()` (so the advisory and the DApp page never disagree by drift).
- Resolve partner_id slugs to human names via `Agroverse Partners!E → Contributors contact information!A` — same join pattern `partner_poke_drafts.gs` uses.
- The advisor-guidance closer (last paragraph) should be regenerated daily by the same LLM the advisory already uses for prose framing.

**Blocker.** Build only **after Partner Poke Scheduler v0 has run for a full week of operator-confirmed calibration** (see [`PARTNER_POKE_SCHEDULER_v0.md`](./PARTNER_POKE_SCHEDULER_v0.md)). The week of real runs surfaces which signals actually drive operator action vs which add noise — those calibrations should be reflected in the rendered advisory before it goes to the oracle. Don't build against synthetic data.

**Acceptance.** Open the next refreshed `ADVISORY_SNAPSHOT.md` and confirm: (a) the "Action items" section is present at the top of operator metrics, in the contemplative-narrative voice above; (b) all three signal sources are surfaced (outbound drafts, partner check-in cadence, partner stock); (c) the closing advisor-guidance paragraph reflects that day's actual signal distribution, not boilerplate; (d) re-running the advisory through the I Ching oracle, Dr Manhattan, and Seth Godin visibly references the specific action items instead of recommending generic outreach.

---

### `dao_client onboard_retail_partner` CLI — v1: website + PR automation

**Context.** MVP shipped via [`dao_client#11`][onboard-mvp] on
2026-04-28 — automates the deterministic ledger + inventory steps
(§3.1 / §3.2 / §3.3 / §3.13 / §3.14 of
`RETAILER_TECHNICAL_ONBOARDING.md`) idempotently, with a YAML manifest
input. Dry-run by default. Operator still has to do the website surface
work + photo upload + PR creation manually after running it.

v1 fills in the remaining steps:

- §3.4 Partner page generation (clone `partners/lumin-earth-apothecary/`,
  named-replacement on slug + name + address + lat/lon + about-blurb;
  about-blurb either operator-supplied in manifest or Grok-extracted
  from `website` URL).
- §3.5 Discovery surface updates (`partners-data.js` append,
  `partner_locations.json` append, `wholesale/index.html` and
  `partners/index.html` alphabetical inserts,
  `cacao-journeys/pacific-west-coast-path/index.html` jpeg-extension
  conditional).
- §3.6 Photo download + resize (operator URLs in manifest, or fall back
  to scraping `og:image` / favicon).
- §3.12 + §3.15 Branch + commit + `gh pr create` in `agroverse_shop_beta`
  and `agroverse-inventory`. Push branch only — operator merges manually
  for the first 5–10 onboardings before flipping to auto-merge.
- §3.4 lat/lon geocoding via Nominatim (free, no key) when manifest
  doesn't include them.

**Acceptance criterion.** Next retail-partner onboarding takes ≤ 5
minutes of operator time end-to-end, including PR review + merge.

**Blocker.** None — every required piece exists. MVP must run cleanly
on a real onboarding before v1 layers on the more invasive automation
(template clone, multi-repo PR creation).

**Owner.** Unclaimed.

[onboard-mvp]: https://github.com/TrueSightDAO/dao_client/pull/11

---

### Eyeball-check `partners-velocity.json` numbers after 4 weekly refreshes

**Context.** First version of `sync_partners_velocity.py` shipped via
[go_to_market#80][velocity-pr] and the first JSON snapshot via
[agroverse-inventory#5][velocity-snap]. Refresh cadence is weekly. Per
Gary's §9 Q5 decision in `PARTNER_VELOCITY_PROPOSAL.md` ("wait till
settle"), no downstream consumer should *trust* the numbers until at
least **4 successful weekly refreshes** have run and a manual sanity
check has confirmed the values track operator intuition for 3–5 known
partners (Go Ask Alice, Lumin Earth, Edge & Node, Kiki's Cocoa).

**Outcome.** Either flip the green-light (wire dormant / high-velocity
signals into warm-up generator — see next entry), or file a defect on
the script if the numbers feel wrong.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read the latest committed snapshot.
- `market_research/scripts/sync_partners_velocity.py` — re-run locally if needed.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §9 Q5 (acceptance criterion).

**Blocker / signal to revisit.** Wait for ≥4 entries on the GitHub
Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible
acceptance check: **2026-05-25** (~4 weeks after first snapshot).

**Owner.** Gary (manual sanity check), then any agent for downstream wiring.

[velocity-pr]: https://github.com/TrueSightDAO/go_to_market/pull/80
[velocity-snap]: https://github.com/TrueSightDAO/agroverse-inventory/pull/5

---

### Wire dormant / high-velocity signals into warm-up draft generator

**Context.** Once `partners-velocity.json` numbers are trusted (see
previous entry), the warm-up draft generator
(`market_research/scripts/suggest_warmup_prospect_drafts.py`) and any
sibling check-in flow can read per-partner activity to:

- **Dormant retailer** (`last_sale_date > 90 days ago` and
  `last_restock_date > 90 days ago`) → trigger a check-in email
  instead of a generic warmup, or de-prioritize warmups for them.
- **High-velocity retailer** (per-SKU `*_12m_monthly_avg >
  category_medians[sku].monthly × N`) → flag as a candidate for
  case-study / testimonial / shelf-photo capture for `/wholesale/`.
- **Cold-start / newly-onboarded retailer**
  (`max(sample_size_*) < 3`) → no recommendation; default to
  category baseline.

**Outcome.** Tighter outreach prioritization without manual triage; a
small CSV-style "this week's flags" surface (sheet or Markdown) for
operator review.

**Files.**
- `market_research/scripts/suggest_warmup_prospect_drafts.py` —
  primary integration point.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic.
- `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` — tighten the
  status-transition rules once the signals exist.

**Blocker.** Previous entry (eyeball-check) must complete green.

---

### Rename "Agroverse Partners" sheet → "DAO Partners" + sweep consumers

**Context.** 2026-05-20: the Main Ledger tab `Agroverse Partners`
(`1GE7PUq-...` gid=1983902109) now holds rows whose `partner_type` is
`Operator`, `Supplier`, `Freight Provider`, `Manufacturer`, etc. — i.e.
the whole DAO partner ecosystem, not just retail/wholesale for the
Agroverse cacao brand. The name is now a misnomer; new operator-partner
onboards (Wayne @ UX.APP, 2026-05-20) make it more obviously so.

**Why it didn't ship inline.** A rename has cross-repo blast radius —
every consumer keys off the literal string `"Agroverse Partners"`. Doing
it as part of the Wayne onboarding PR would have ballooned the diff.

**Scope (single PR after the Wayne onboard PR merges).**
1. Rename the sheet tab `Agroverse Partners` → `DAO Partners` (gid is
   stable; gid-keyed consumers are unaffected).
2. Sweep every literal-string consumer. Known callers to grep first:
   - `dao_client/truesight_dao_client/modules/onboard_partner.py` —
     `PARTNERS_SHEET` constant.
   - `market_research/scripts/sync_partners_velocity.py` (if it reads
     the tab by name).
   - GAS handlers under `tokenomics/` that scan the Main Ledger.
   - DApp Partner Check-in scanner (`dapp/partner_check_in.html` →
     GAS handler) — confirm the worksheet name.
   - `agroverse_shop` discovery surfaces (`partner_locations.json`
     generator, if any).
   - `agentic_ai_context/RETAILER_TECHNICAL_ONBOARDING.md`,
     `PARTNER_CHECK_IN_IMPLEMENTATION.md`, and any other docs that
     name the tab.
3. Workspace-wide grep before declaring victory:
   `grep -r '"Agroverse Partners"' ~/Applications` and
   `grep -r "'Agroverse Partners'" ~/Applications`.

**Outcome.** Tab name reflects its actual scope; future operator /
freight / supplier onboards stop reading as "Agroverse cacao business"
by association.

**Files.** Main Ledger spreadsheet
`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, gid `1983902109`, plus
every caller surfaced by the grep sweep.

**Owner.** Unclaimed.

---

### Advisory ops-health v2: burn rate + days-of-cover at SF

**Context.** Ops-health v1 ([TrueSightDAO/go_to_market#77][pr77] +
[follow-up #78][pr78]) ships per-shipper stock from
`treasury-cache/dao_offchain_treasury.json`, cash float from `off chain asset
balance`, and in-transit freight from `Shipment Ledger Listing`. Burn rate /
days-of-cover at SF (Kirsten) was deliberately deferred — the structured
snapshot at `ecosystem_change_logs/ops_health/current.json` already reserves
two `null` slots: **`sales_velocity_30d`** and **`days_of_cover_at_sf`**.

**Outcome.** When v2 lands, the daily oracle / a future
`dapp/supply_health.html` page can flag a SKU with **🟢 ≥4 weeks cover · 🟡
2–4 weeks · 🔴 <2 weeks** at Kirsten — exactly the signal Gary is missing
today (*"Kirsten goes low before Matheus's freight inbound has arrived"*).

**Files / shape.**
- `market_research/scripts/generate_advisory_snapshot.py` →
  `_compute_ops_health(...)` returns the structured dict; add a peer
  `_compute_burn_rate_and_cover(treasury, qr_sales_rows)` that populates the
  two reserved slots and surface a few `🟢/🟡/🔴` lines in
  `_render_ops_health_markdown`.
- `QR Code Sales` window already loaded by `_fetch_sheet_sales_markdown` when
  `--with-sheet-sales` is on — pass the parsed rows through instead of
  re-reading.

**Join key.** Today the join between sales (per Currency string) and stock
(per `inventory_type` × `unit_format`) is brittle because **`inventory_type`
is only populated on ~28% of `dao_offchain_treasury.json` items as of
2026-04-27** (column added 2026-04-26; backfill in progress). Two paths:

1. **Conservative:** join on the raw `Currency` string (works today, exact
   match per batch — granular but noisy).
2. **Cleaner (preferred when ready):** join on `inventory_type` × `unit_format`
   once the backfill is meaningful (~>80% populated). Surface the same flag
   one level higher.

**Blocker / signal to revisit.** Check `inventory_type` sparseness on
`dao_offchain_treasury.json` before starting:

```bash
curl -sL https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/dao_offchain_treasury.json \
  | python3 -c '
import json, sys
d = json.load(sys.stdin)
items = [it for m in d.get("managers", []) for it in m.get("items", [])]
populated = sum(1 for it in items if (it.get("inventory_type") or "").strip())
print(f"{populated}/{len(items)} = {100*populated/len(items):.0f}% populated")
'
```

If <40%, do path (1) only. If >80%, go straight to path (2). In between, ship
path (1) and re-roll-up by `inventory_type` for the markdown summary.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks after v1
shipped, gives the backfill room).

[pr77]: https://github.com/TrueSightDAO/go_to_market/pull/77
[pr78]: https://github.com/TrueSightDAO/go_to_market/pull/78

---

### `two_bahia_bars` newsletter — post-send open / click / reply read-out

**Context.** First Agroverse newsletter to ship with the full pipeline ([buyer
exclusion][n-pr79], [JPG fallback + tighter image margins][n-pr84],
[side-by-side comparison row][n-pr85]) sent 2026-04-27 to **38 recipients**
(2 past-buyers excluded via `--exclude-buyers-of-substring` against
`Agroverse QR codes`). Tracking on by default — opens land in cols H–K and
clicks in L–P on the **`Agroverse News Letter Emails`** tab of the dedicated
newsletter workbook (`1ed3q3SJ8ztGwfWit6Wxz_S72Cn5jKQFkNrHpeOVXP8s`),
filtered by `campaign='two_bahia_bars'`.

**Why a follow-up reads the data.** The v5 layout (compact 280px images,
side-by-side comparison row at top) was a deliberate design call. Without a
read-out, the data sits in the sheet and the comparison-row decision can't
be validated for future sends. iOS Mail Privacy Protection inflates opens
in the first hour — the read-out should land **after a 7–10 day soak** so
real engagement (repeat opens, clicks, replies) dominates the noise.

**Outcome.** A short summary covering:
- Open rate (recipients with `open_count > 0`) and median `open_count`.
- Click rate (recipients with `click_count > 0`) and which CTA each clicker
  hit (`last_clicked_url` — Oscar's Farm, Fazenda Santa Ana, or both via the
  comparison row's separate "Check this bar" links).
- Reply rate (search Gmail `to:garyjob@agroverse.shop` against the
  recipient list; count distinct addresses that replied).
- **Did the comparison row's "Check this bar" CTA get clicked at a
  meaningfully different rate than the in-section "Check Oscar's Farm
  2024" / "Check Fazenda Santa Ana 2023" CTAs?** (Same destination URLs,
  different anchor text + position. Real design signal for whether the
  comparison row earns its keep on future two-SKU sends.)

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:two_bahia_bars'`,
   description includes the headline numbers).
2. A DAO contribution submission via **`dao_client`** with the analysis as
   the body and a link to the DApp Remarks row.

**Files / shape.**
- Recipient list keyed off `campaign='two_bahia_bars'` from
  `Agroverse News Letter Emails`.
- Open / click columns already populated by Edgar's
  `/newsletter/open.gif` and `/newsletter/click` endpoints.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<recipient> after:2026-04-27`.
- Sheet write: append to `DApp Remarks` on the Hit List spreadsheet
  (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); see
  `market_research/scripts/hit_list_dapp_remarks_sheet.py` for the helper.

**Owner.** Unclaimed. Earliest sensible: **2026-05-07** (10 days after the
send — opens / clicks have stabilized, replies have had a week to land).

**Optional adjacent work.** While reading the data, also note whether
either of the two excluded buyers (`pamelacotton7@msn.com`,
`toffees_fibrils.0l@icloud.com`) ever asked "why didn't I get the
newsletter about the bars I bought?" — would update the buyer-exclusion
copy in `AGROVERSE_NEWSLETTER_WORKFLOW.md` §4.3a if so.

[n-pr79]: https://github.com/TrueSightDAO/go_to_market/pull/79
[n-pr84]: https://github.com/TrueSightDAO/go_to_market/pull/84
[n-pr85]: https://github.com/TrueSightDAO/go_to_market/pull/85

### Warm-up email A/B read-out — PDF-only vs PDF+packaging-photos cohort comparison

**Context.** [`go_to_market#74`][wp-pr74] (merged 2026-04-27) flipped the
default warm-up email payload from "PDF wholesale catalog only" to "PDF +
2 packaging photos" for every send via the partner-outreach pipeline. The
hypothesis: visual product proof in the first touch lifts open / click /
reply rates over a PDF-only ask. Without a read-out, the change sits as
an untested intuition.

**Why a follow-up reads the data.** The cleanest natural experiment we'll
get — the cutover is sharp (one PR), the population is otherwise
homogeneous (same Hit List rows, same template, same operator), and the
volume on either side of 2026-04-27 should be enough for a directional
signal even if not statistically rigorous. Earliest sensible read:
**2026-05-11** (~2 weeks of post-cutover sends + replies have had time
to land — Gmail reply soak window matches the newsletter read-out
above).

**Outcome.** A short comparison covering, for each cohort:
- **Cohort split.** Read the `Email Agent Follow Up` tab of the Hit List
  workbook (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); split
  rows where status indicates a warm-up was sent into:
  - **Pre-2026-04-27** (PDF only) — sent before the cutover.
  - **On/after 2026-04-27** (PDF + 2 packaging photos) — the new default.
- **Metrics per cohort.** Count, open rate (`Open` column > 0), click
  rate (`Click through` column > 0), reply rate (cross-reference Gmail
  for inbound replies to each `to_email` after `sent_at`).
- **Time-controlled comparison.** Repeat the metrics restricted to the
  **2 weeks immediately before** vs **2 weeks immediately after**
  2026-04-27 to neuter time-of-year / list-quality drift.
- **Verdict.** Did packaging-photo warm-ups beat PDF-only on any of
  open / click / reply by a margin that would survive doubling the
  sample size? If yes — keep the new default. If no — flag whether to
  revert or keep as the cleaner UX call regardless of metrics.

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:warmup_packaging_photos_ab'`,
   description includes headline numbers + PR URL).
2. A DAO contribution submission via **`dao_client`** with the analysis
   as the body and a link back to the DApp Remarks row + PR #74.

**Files / shape.**
- Sheet read: `Email Agent Follow Up` tab on
  `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc` via
  `google_credentials.json` + gspread.
- Status / cohort inference: `market_research/HIT_LIST_CREDENTIALS.md`
  documents the Status column conventions.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<to_email> after:<sent_at>` per recipient.
- DApp Remarks append: `market_research/scripts/hit_list_dapp_remarks_sheet.py`.
- Contribution log: dao_client CLI per
  `agentic_ai_context/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`.
- Label / status convention: `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` §9.7.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks post-cutover).

**Why not `/schedule`.** Tried — remote agent can't access the private
sheet, Gmail OAuth, or Edgar tokens (no MCP connectors connected, no
`google_credentials.json` in cloud sandbox). Belongs on the local
backlog.

[wp-pr74]: https://github.com/TrueSightDAO/go_to_market/pull/74

### Migrate `dapp/stores_nearby.html` Add Store form onto the `[STORE ADD EVENT]` Edgar path

**Context.** The dao_client / Edgar / GAS slice of `[STORE ADD EVENT]`
shipped 2026-04-28 (see *Recently shipped* below). The DApp's
`stores_nearby.html` Add Store form still talks directly to GAS
`add_store` — small GET payload that doesn't have the cross-origin
failure mode the retail field report flow had, so it works, but the
DAO has decided that **all signed Hit List writes go through the same
canonical pattern**: DApp → Edgar → Telegram Chat Logs → async GAS
scanner. This entry is the remaining migration to that posture.

**What's needed.**
- Replace the direct `fetch(GAS, {action: 'add_store', …})` call in
  `dapp/stores_nearby.html` with a signed `[STORE ADD EVENT]` POST to
  Edgar (mirror today's `submitRetailFieldReportToEdgar` shape in
  `dapp/store_interaction_history.html`).
- Drop or repurpose the `add_store` action in
  `clasp_mirrors/1NpHrKJW…/Code.js` once no callers remain. The
  `addNewStore()` helper stays — it's the GAS scanner's own
  dependency.
- Verify the DApp form's "duplicate detected" UX still works
  (today the GAS direct call returned `{success: false, duplicate:
  true, existing_store: …}` synchronously; with the async path the
  duplicate detection lands on **Store Adds** col K
  `existing_store_shop_name`, so the form needs a polling /
  back-channel UX or a "submitted — check Hit List in a minute"
  message).

**Cost estimate:** ~30 min including the form's status / duplicate UX.

**Blocker.** None — purely additive once started. Don't bundle with
unrelated `stores_nearby.html` work.

**Owner.** Unclaimed.

### Deprecate `backfill_hit_list_opening_hours.py` + `backfill_hit_list_google_listing.py` after 2 cron cycles

**Context.** 2026-04-28 the two responsibilities — opening-hours grid (Mon
Open … Sun Close) and `Google listing` column — were folded into the routine
hourly cron at `.github/workflows/hit_list_enrich_contact.yml` (`35 * * * *`)
via [TrueSightDAO/go_to_market#88][pr88]. The enriched
`scripts/hit_list_enrich_contact.py` now also fills empty `Address / City /
State / Latitude / Longitude` from the same Places Details call. The two
standalone backfills still exist as manual one-shots but should no longer
need to be invoked routinely.

**Outcome.** Either delete the two standalone scripts, or shrink them to
thin documented wrappers that call into `hit_list_enrich_contact.py`'s
`apply_place_result_to_row_gaps()` helper for one-shot full-table sweeps.

**Files.**
- `market_research/scripts/backfill_hit_list_opening_hours.py`
- `market_research/scripts/backfill_hit_list_google_listing.py`
- `market_research/scripts/hit_list_enrich_contact.py` (already imports both
  via `bl` / `dl` for `resolve_place_id` + `append_place_id_to_notes` —
  if either backfill is deleted, inline the helpers it depends on or move
  them into a shared module).

**Verification before deleting.** On the Hit List, confirm:

1. New rows landing in the past 2 weeks have non-empty `Address`, `City`,
   `State`, `Latitude`, `Longitude`, `Monday Open`, `Google listing` (where
   Places returns those fields) within ~24h of arrival.
2. The `cron`-scheduled action's last 24 runs each show `filled>0` or a
   clean `skipped` count (i.e. the cron is closing gaps, not silently
   no-op'ing).

**Blocker / signal to revisit.** Earliest sensible: **2026-05-12** (~2
weeks of cron cycles after #88 lands).

**Owner.** Unclaimed.

[pr88]: https://github.com/TrueSightDAO/go_to_market/pull/88

---

### Validate the circle-hosting → cacao-velocity hypothesis after 4 partners-velocity refreshes

**Context.** 2026-04-28 observation: two recent / candidate retail partners
mention **women's circles** prominently — [The Way Home Shop in SE
Portland][way-home] (just onboarded) and Lumin Earth (existing partner).
Ceremonial cacao genuinely lives in that ecosystem (women's circles, sound
baths, breathwork, new-moon gatherings), so "hosts circles" is plausibly
a leading indicator of cacao sell-through.

The cheap detection step shipped immediately as
`market_research/scripts/detect_circle_hosting_retailers.py`
(see [go_to_market#XX][circle-pr] when filed) — it crawls each Hit List
retailer's `Website` for high-precision keywords (women's circle, moon
circle, cacao ceremony, sound bath, breathwork, sister/sacred circle,
ecstatic dance) and writes **Yes / Not detected** to a new
**Hosts Circles** Hit List column. *That* part is data-only; this entry
covers the deferred *correlation* check.

**Outcome.** Once `partners-velocity.json` has ≥4 weekly refreshes, cross-
reference per-SKU velocity against the **Hosts Circles** flag for
already-onboarded partners. Two questions:

1. Do circle-hosting partners outsell non-circle peers per-SKU at
   statistically meaningful margins? If yes, **green-light**:
   - Add `Hosts Circles=Yes` as a positive signal on the warm-up draft
     generator (next to the dormant / high-velocity logic in the existing
     entry above).
   - Open a separate research entry on whether to build a **circle
     facilitator** outreach motion (different ICP than retailers — direct
     to circle-leaders who buy in bulk for their gatherings).
2. If the correlation is weak or negative, rule it out and close.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read latest snapshot.
- Hit List **Hosts Circles** column (col after `Google listing`) — read.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic + sample-size guards.

**Blocker / signal to revisit.** Same as the **Eyeball-check
`partners-velocity.json`** entry above — wait for ≥4 entries on the
GitHub Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible:
**2026-05-25**. Combine with that entry's manual sanity check so
both reads happen in one sitting.

**Owner.** Unclaimed.

[way-home]: https://thewayhomeshop.com/
[circle-pr]: https://github.com/TrueSightDAO/go_to_market/pulls?q=is%3Apr+circle+hosting

---

### Fix `addNewStore()` GAS — `setValues`-dimension mismatch on tail-end step

**Context.** `[STORE ADD EVENT]` end-to-end test 2026-04-28 (see *Recently
shipped*) added 3 referrals for Psychic Sister (Clary Sage / Casa de Ritual
/ La Sirena Botanica) — all three landed on Hit List rows 526–528 with the
correct shop name / status / city / state / shop type / Notes / Sales
Process Notes / Status Updated By / Status Updated Date / Store Key.

But every single submission also recorded `status: error` on the **Store
Adds** dedup log with this error message:

```
The number of rows in the data does not match the number of rows in the
range. The data has 1 but the range has 526.
```

That's an Apps Script `setValues(values)` dimensional error from inside
`addNewStore()` (likely the trailing `logDappSubmission_(...)` call or a
sales-notes write). It throws **after** the new Hit List row has been
fully written (since the row is correct), so the data is fine — but the
exception escapes addNewStore's try/catch boundary and lands in the new
GAS scanner's error handler.

**Symptoms.**
- Hit List rows land correctly (operator-visible).
- Store Adds dedup log says `error` with this message (audit-trail-misleading).
- A re-fired Telegram Chat Logs row would NOT re-add (idempotent on
  Telegram Update ID), so no double-row risk.

**Fix targets.**
1. **Root cause** in `clasp_mirrors/1NpHrKJW…/Code.js` `addNewStore()` /
   `logDappSubmission_()`. The `526` figure is "all data rows on the Hit
   List sheet"; somewhere a `range.setValues(arr)` is being called with
   `arr.length === 1` against a range covering all data rows. Likely
   pattern: `sheet.getDataRange().setValues([row])` instead of
   `sheet.appendRow(row)` / `sheet.getRange(targetRow, 1, 1, n).setValues([row])`.
2. **Defensive workaround** in
   `google_app_scripts/find_nearby_stores/process_store_adds_telegram_logs.gs`:
   when `addNewStore` throws, fall back to a Hit List lookup by
   `store_key` (the same key `createStoreKey_` builds). If found,
   record `status: added_with_warning` + the exception text in
   `error_message` instead of `status: error`. That way the audit log
   correctly reports the row was added even when addNewStore's tail
   step fails.

**Cost.** ~20 min for (1) once the offending line is found; ~10 min
for (2). Both are independent — do (2) first if you want clean audit
trails fast; do (1) if you want addNewStore stable for the existing
DApp form callers.

**Owner.** Unclaimed.

---

### Extend iching_oracle advisory with QiMenDunJia overlay

**Context.** Today (2026-05-09) we agreed the I-Ching cast and a QMDJ chart
are complementary lenses on the same moment T — I-Ching tells you the
quality of the moment (via random selection from coin throws), QMDJ tells
you the spatial / strategic structure of that same moment (deterministic
from the timestamp). Pairing them on the same T gives the DAO advisor two
classical frameworks reading the same instant: I-Ching as the narrative /
transformational layer, QMDJ as the spatial / strategic overlay. Honest
disclaimer: combining them is a *modern synthesis*, not a traditional
practice; the UI and the GAS prompt should both flag this.

**Spec.** Full design lives in [`ICHING_QMDJ_EXTENSION.md`][qmdj-spec].
Summary:

- **Library.** `lunar-javascript` (6tail family). Drops in cleanly to the
  static-site / `gas/` stack. Don't reimplement.
- **Client.** After coin throw at moment T: also compute the QMDJ chart
  from T (Ju, Six Yi, Three Wonders, Heaven/Earth Plates, Doors, Stars,
  Spirits) and POST alongside the hexagram + changing lines.
- **GAS.** Extend `oracle_advisory_bridge.gs`:
  - `extractDraw_` += `qmdj_chart` field.
  - `staticContext` += new `QMDJ_FRAMEWORK_REFERENCE.md` (cached — what
    the doors/stars/spirits/wonders mean, what counts as auspicious).
  - `dynamicContext` += per-call QMDJ chart block for moment T.
  - `ORACLE_PROMPT_HEADER` adds two new output sections (QMDJ
    configuration of this moment, Combined frame) and extends section 7
    (decisive action) to use QMDJ's directional / timing signal when one
    is present, otherwise to honestly say the chart doesn't surface a
    strong directional read.
- **Caching.** The new framework reference is static across calls and
  belongs in the cached system block — keeps marginal token cost
  reasonable.
- **UI.** Render QMDJ as a *collapsible* "Extended Reading: QiMenDunJia"
  section below the I-Ching reading, not above it. I-Ching narrative
  stays the primary surface.

**Implementation order.** Three independently testable PRs (not one):

1. **Smoke-test lunar-javascript locally**, then wire chart casting +
   9-palace render into the client. No GAS changes yet.
2. **Land `QMDJ_FRAMEWORK_REFERENCE.md`** in `agentic_ai_context` and
   extend `oracle_advisory_bridge.gs` to fetch + include it.
3. **Refine `ORACLE_PROMPT_HEADER`** sections after seeing live output;
   tune the "no clear signal" fallback language so the LLM doesn't
   fabricate directional advice.

**Cost.** Probably 60-90 min per PR. Total ~3-4 hours of focused work
across the three.

**Risks worth re-reading from the spec before starting.** Information
overload, two-oracles-stapled-together coherence, naive
auto-interpretation, modern-synthesis disclaimer. All addressed in the
spec; don't skip the "Risks / things to be careful about" section.

**Owner.** Unclaimed.

[qmdj-spec]: ./ICHING_QMDJ_EXTENSION.md

---

### krake_browser engine implementation (post-scaffold)

**Context.** Three repos scaffolded 2026-05-20:

- [KrakeIO/krake_browser](https://github.com/KrakeIO/krake_browser) — engine (Sinatra + Playwright/CDP), currently README + ARCHITECTURE + DSL only
- [KrakeIO/krake_recipes](https://github.com/KrakeIO/krake_recipes) — generic public recipes (WhatsApp send_message, LinkedIn connect_request, Instagram login, FDA facility_search) + JSON Schema
- [TrueSightDAO/tdg_recipes](https://github.com/TrueSightDAO/tdg_recipes) — DAO-specific recipes (partner_followups/check_in, edgar/submit_contribution)

All three are **PRIVATE** — flip to PUBLIC only after the engine works end-to-end and we have a recorded demo.

Vision: persistent local Chromium that human + LLM share. LLM drives recipes via CDP; pauses with `human_intervention` for 2FA, approvals, anti-bot, judgment calls. Direct evolution of the Krake.io DSL (2014) — `solve_captcha` generalized into `human_intervention` with a prompt + ack channel + screenshot.

See `~/Applications/krake_browser/{README,ARCHITECTURE,DSL}.md` for the design (or the same files on the public repo once it's flipped public).

**Scope (engine MVP).** Implement against ARCHITECTURE.md:

1. `bin/krake_browser_launch` — Chromium launcher with `--user-data-dir=$HOME/.krake_browser/profile --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1`.
2. Sinatra app that attaches to running Chromium via CDP (`playwright-ruby-client` is the natural choice given krake_sinatra's stack).
3. Recipe loader: reads JSON from a configurable `--recipes-dir` (default: local clones of both recipe repos).
4. Recipe executor: walks `actions[]`, dispatches each action via Playwright, suspends on `human_intervention`.
5. MCP server tools: `run_recipe(name, vars)`, `list_recipes()`, `ack_intervention(token, action, payload?)`.
6. MCP events: `intervention_required` (prompt + screenshot + token), `recipe_progress`.
7. Localhost-only binding + token auth on the MCP port. Engine refuses to start if `0.0.0.0` detected anywhere.
8. Reference CLI client: minimal Ruby script connecting to MCP, invoking one recipe, printing intervention prompts to stdout and reading ack from stdin (for testing without a full chat UI).

**Validation criterion.** Run `whatsapp/send_message` against Gary's logged-in WhatsApp Web from any MCP client — recipe pauses for approval of the drafted message, human types Continue, message sends.

**Scope addendum (Gary 2026-05-20).** Items 9–10 land alongside the MVP. **Items 11–13 are engine v0.2** — defer until items 1–10 validate end-to-end (run `whatsapp/send_message` against live WhatsApp Web with one human approval). v0.2 turns the engine from "runs strict recipes" into "self-healing browser concierge" and is where the project becomes meaningfully differentiated; trying to ship it in the MVP will stall the WhatsApp demo. The v0.2 items also compound — guideposts (item 11) need the teach-loop (item 12) to repair drift, and passive observation (item 13) is strictly better than narration so ship 13 as part of 12 if it's not much more work.

9. **Bundle krake_recipes with engine install.** The TDG engine instance should come with platform recipes (Instagram, LinkedIn, WhatsApp, Facebook, FDA) pre-available, not require a separate clone step. Implement as a postinstall clone + scheduled `git pull` of [KrakeIO/krake_recipes](https://github.com/KrakeIO/krake_recipes) into `~/.krake_browser/recipes/krake_recipes/`. Recipes for living sites drift on their own cadence; pull beats pin.
10. **Wrapper-recipe DSL extension for tdg_recipes.** Add three new fields to the recipe schema so a TDG recipe can be a thin layer over a platform recipe:
    - `uses` — path to the platform recipe (e.g. `instagram/dm_send`)
    - `why` — one-paragraph DAO context the LLM reads before deciding to invoke (e.g. "partner check-ins for stores whose primary channel is IG, not WhatsApp — confirm last touch in Hit List first")
    - `vars` — DAO-specific variable defaults that get merged into the platform recipe's variable substitution
    
    Primary use case Gary identified: **partner check-ins** (the load-bearing operational flow) across WA / IG / LinkedIn / FB depending on partner's primary channel. The `why` field becomes the LLM's decision input.

11. **Guidepost model — intent + hint + expected_state alongside strict selectors.** Each action in the DSL gains three optional fields that turn it from a rigid click-here-then-click-there contract into a guidepost the LLM can re-ground at runtime:
    - `intent` — what this step is trying to accomplish ("Open connect-with-note modal")
    - `hint` — natural-language locator advice for the LLM if the strict selector fails ("Click 'Connect'; if hidden, it's under the 'More' button")
    - `expected_state` — observable post-condition the executor checks before moving on ("Textarea for personal note is visible")
    
    Execution order: try `dom_query` / `xpath` first (fast, deterministic, no LLM call). If it returns nothing or `expected_state` doesn't match, escalate to LLM-grounded discovery using `intent` + `hint` (Browser Use / Stagehand semantics — feed the LLM a trimmed accessibility tree, ask for the right element). Strict and flexible coexist in the same recipe; you only pay the LLM cost when the cheap path breaks.

12. **Teach-by-narration loop — continuous DOM repair via human-AI symbiosis.** The mechanism that makes selector drift self-healing instead of silently breaking recipes. Three new MCP tools beyond the MVP set:
    - `read_page_state()` → current URL + serialized DOM (or trimmed accessibility tree) + screenshot. Gives the LLM eyes onto the current tab.
    - `narrate_action(text)` → operator types what they just did manually ("I just clicked the new Connect button, it's now under the three-dot menu"). LLM keeps it as context.
    - `propose_recipe_update(name, patch)` → LLM emits a JSON patch against the recipe and opens it as a PR to krake_recipes or tdg_recipes. Gary reviews + merges; the next scheduled `git pull` makes the fix canonical.

    End-to-end loop: strict selector fails → engine fires `human_intervention` with "I lost the connect button" → Gary does the step manually → narrates → LLM reads page state → drafts a PR with the new selector → Gary merges → next run works. This is the differentiator vs. every other browser-automation tool (which break silently on DOM change). Without this loop, krake_browser is just another Stagehand clone; with it, it's a tool that gets *more reliable over time* through use.

13. **Passive observation — recipe-execution-bounded learning.** Strictly better than narration: Gary just works, the LLM learns from the clickstream. Three modes worth distinguishing; ship only mode (b):

    - (a) *Always-on passive observation across the whole browser* — records every interaction including bank logins, password manager, email. **Non-goal forever.**
    - (b) *Recipe-execution-bounded observation* — when a recipe is running and a step fails, the engine flips on observation mode for the duration of Gary's manual recovery, then off. Bounded by definition (failure triggered it), self-correlating (the recovered selector maps to the failed step), almost zero privacy surface. **This is what ships in v0.2.**
    - (c) *Operator-triggered "watch me"* — Gary says "watch me do this" → LLM begins recording → Gary completes a new flow → LLM drafts a brand-new recipe. Natural extension for greenfield recipe authoring; defer to v0.3.

    **DSL impact:** each guidepost gains a `learned_selectors[]` history with timestamps. At execution time the engine tries selectors in reverse-chronological order so newest wins, but old ones stay as fallbacks (sites sometimes A/B-test old and new DOMs for weeks).

    **Engine adds:** CDP event subscription gated by `recipe_recovery_mode_active` flag (off by default). Click events translate to stable selectors (prefer `aria-label`, then `data-testid`, then computed CSS path). Type events from `<input type=password>` / `<input autocomplete=current-password>` / fields inside `<form autocomplete=off>` are dropped from the log entirely. After Gary completes the recovery, the LLM diffs the failed guidepost against the observed sequence and opens a PR with the new selector(s) appended to `learned_selectors[]`.

14. **LLM form comprehension + pre-fill — `llm_fill_form` action (v0.3).** New DSL action for forms where the human cost is *reading* the form, not typing the answers (FDA facility registration, partner onboarding paperwork, retail shipping intake forms — anything regulatory or compliance-heavy). Engine flow:
    - LLM reads the entire form via the page's DOM or accessibility tree.
    - Uses the recipe's `context` block + (optional) external lookups (web search, the user's other logged-in sessions inherited from the persistent profile, Google Sheets via service-account auth, etc.) to figure out each field's value.
    - Fills every field, attaches `confidence_score` (0.0–1.0) and `reasoning` (one line citing where the value came from — recipe context, form text, external lookup URL) as metadata per field.
    - `human_intervention` surfaces ONLY fields below a configurable confidence threshold (default `0.85`) for explicit review; high-confidence fields are pre-approved. UI shows `show all` toggle for high-stakes forms (regulatory submissions, anything that becomes a legal record).

    **Critical design constraint:** the spot-check surface has to be reliable, because the whole pitch is the human *skips reading the form*. Per-field reasoning shown on hover/click; without this, rubber-stamping → Open Claw failure mode (see the 2026-05-20 blog post anecdote for the cautionary tale).

    **Depends on:** v0.2's LLM-grounded DOM discovery primitive (item 11). Independent of v0.3's "watch me" recording (item 13(c)); both are v0.3 candidates, ship whichever a real form pain-point demands first.

**Blockers.** None. PAT for KrakeIO push lives in `~/Applications/truesight_autopilot/.env` as `KRAKEIO_LLM_PLAYGROUND_PAT`. Use it via `GH_TOKEN=$(grep ^KRAKEIO_LLM_PLAYGROUND_PAT= ~/Applications/truesight_autopilot/.env | cut -d= -f2-)`.

**Already done (no engine required).** (a) All 3 repos flipped to PUBLIC on 2026-05-20 (the original "wait until engine works" was overcautious; design docs + sample recipes are fine to expose). (b) Forward-spec blog post live at [garyteh.com/2026-05-20-from-solve-captcha-to-symbiosis-what-my-2014-dsl-was-trying-to-tell-me.html](https://garyteh.com/2026-05-20-from-solve-captcha-to-symbiosis-what-my-2014-dsl-was-trying-to-tell-me.html) — framed as design journal, links to the three repos.

**After engine works.** Record a 30s screencap of the WhatsApp demo and write a follow-up blog post with honest retro (what worked, what was thinkier-than-it-needed-to-be). HN explicitly skipped as launch venue — Gary called it "kinda lame"; risk of flop > upside, garyjob/blog has zero downside and can cross-post later if the follow-up gets organic traction.

**Owner.** Unclaimed.

---

### Credential vault for service-account keys (AWS Secrets Manager) so cut-over hosts don't ship without creds

**Context.** 2026-05-29: the DApp email-registration flow was down in prod because the standalone `dao_protocol_nelanco` host (stood up in the 2026-05-28 NELANCO cutover) was deployed **without** its Google service-account keys — `edgar_dapp_listener_key.json` existed nowhere on the box and there was no `GOOGLE_CREDS_DIR` in its `.env`, so every email-registration signature write hit `[Errno 2]`. Fixed by hand-scp'ing the 3 SA keys + setting `DAO_PROTOCOL_GOOGLE_CREDS_DIR` (see `NOTES_sentiment_importer.md` § dao_protocol, [dao_protocol#51](https://github.com/TrueSightDAO/dao_protocol/pull/51)). The same class of gap had already bitten the autopilot box. **There is no system of record for these credentials** — they're provisioned by manual SCP from a laptop and scattered across `~/Applications/*/.env`, per-host `config/*.json`, `/opt/truesight_autopilot/config/google/`, and laptop copies. Any new host / re-image silently misses them, and nothing fails at deploy time to catch it.

**Goal / shape.** Stand up a managed secret store as the single source of truth for service-account JSONs + host secrets, fetched at deploy/boot instead of by manual SCP. Prefer **AWS Secrets Manager** or **SSM Parameter Store** (the EC2 fleet already runs in AWS with IAM roles; both give KMS-at-rest, per-secret IAM scoping, CloudTrail audit) over a plaintext folder. Minimum viable slice:
- Store the 3 Google SA keys (`edgar_dapp_listener`, `cypher_defense_gdrive`, `agroverse_qr_code_gdrive`) as secrets.
- Give each host an instance-profile IAM role scoped to **only** the secrets it needs.
- Add a small fetch step to each deploy script (`dao_protocol`, autopilot, Edgar) that pulls its secrets into the expected creds dir on boot/deploy, so `config.py`'s `GOOGLE_CREDS_DIR` resolution (dao_protocol#51) points at a populated dir.
- Stretch: a `deploy --verify-creds` preflight that fails loudly when a required key is absent — would have caught this incident at cutover instead of in prod.

**Design caution (from the 2026-05-29 discussion with Gary).** Do **not** just dump a folder of every credential onto an internet-facing box an LLM can read + give it "SSH in and fix anything" — that concentrates the whole network's secrets on the highest-value target and crosses the autopilot's deliberate "propose-only, never auto-mutate" boundary. Least-privilege per-host scoping; keep a human-approval gate on any write/mutating path; read-only diagnosis can stay autonomous.

**Blockers.** None technical. Decision needed: Secrets Manager vs SSM Parameter Store vs SOPS+age-in-git. Recommend Secrets Manager (native rotation support).

**Owner.** Unclaimed.

---

### Deploy lease machinery effectively inert — 14 open leases on the GAS script, and `close_lease()` misreports success as failure
**Filed 2026-09-10. Updated 2026-09-10 (Sophia, thread 24326). Owner: unclaimed. Governor: Gary.**

**Symptom.** Not two leases — **fourteen** lease files are still `status: open` on scriptId `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v`, accumulated since 2026-08-26: `L-20260826-01`, `L-20260828-02`…`-05`, `L-20260901-06`, `L-20260901-08`, `L-20260901-095538`, `L-20260902-01`, `L-20260905-10`, `L-20260906-01`, `L-20260907-01`, `L-20260909-01`, `L-20260910-01`. The house TTL is **30 minutes**, so all are long expired; each was abandoned mid-ceremony (the pushing session died before closing it). A 14-deep graveyard means the ceremony is not merely occasionally-skipped — it is **effectively not enforcing anything**.

**Impact.** `DEPLOY_PUSH_SOP` §6 treats a zombie lease as an incident. Worse, the deploy tool **fail-opens past** an existing lease rather than refusing, so a zombie provides no protection *and* no alarm — the next deploy proceeds as if the lease were free. Mutex-by-convention is silently degraded to no-mutex whenever a session crashes mid-push.

**Second bug — `close_lease()` reports success as failure.** `deploy_ledger.close_lease()` decides success with `"content" not in res`, but GitHub's DELETE response is `{"commit":…, "content": null}` — the `content` key *is* always present, so the function returns `status: error` **even when the delete worked**. Observed live: two closes returned `error` while the lease files were in fact gone. Impact: a session that trusts the return value will try to "re-close" and **manufacture new zombies**, and a genuine close failure is indistinguishable from the false alarm. Fix: treat a DELETE that returns a `commit` (or HTTP 2xx) as success, or re-`GET` the file to confirm absence.

**Third bug — the deploy ledger fail-opens silently.** `deploy_gas_project.py` resolves its PAT from `$DEPLOY_LEDGER_PAT`, then `$GITHUB_TOKEN`, then `$TRUESIGHT_DAO_AUTOPILOT`. Run from a bare shell that hasn't sourced `/opt/truesight_autopilot/.env`, none is set, so the ledger is **skipped with a one-line warning** while the deploy still proceeds — i.e. a production change can land with **no audit record**. Observed live on the 2026-09-10 repoints: both printed `! deploy ledger unavailable (fail-open)` and were backfilled afterwards by hand. Fix: either make the ledger **fail-closed** for a deploy, or have the deploy wrapper export the PAT itself rather than depending on the caller's shell. Related footgun: `/opt/truesight_autopilot/.env` is not shell-safe (a bare `set -a; . .env` executes a line and errors) — parse it, don't source it.

**Proposed fix.** Close the fourteen zombies (append close records, don't delete). Then fix the two bugs above, and decide the policy: prefer **fail-closed** (refuse a new push while any non-expired-or-expired-but-open lease exists, and surface it) or at minimum, have the deploy tool **log loudly** when it fail-opens past a stale lease so the zombie leaves a trail instead of passing silently.

**Blocker / priority.** Not blocked. Ready for a maintainer with write access to the lease records.

---

### One `clasp push` produced two deploy-ledger records (deploy script *and* the autopilot tool each append)
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24326).**

**Symptom.** The 2026-09-10 push of script `1UrBgqLnnQc6PV4-…` appended **two** records to `ecosystem_change_logs` for a single logical deploy — one written by `tokenomics/scripts/deploy_gas_project.py` and one by the autopilot's `gas_deploy_project` tool wrapper around it. Both are appended to the same append-only ledger.

**Impact.** The deploy ledger is read for audit ("what changed in production, when, by whom"). Duplicate rows for one deploy make the count of deploys wrong and force a reader to detect-and-merge twins. Same class as the duplicate tracking-row quirk in the invalidation tab — a read-then-append with no idempotency key. Severity low (append-only, both records correct), but it erodes trust in an audit surface.

**Proposed fix.** Give each push a single idempotency key (e.g. the lease id, or `<scriptId>:<version>:<sha>`) and have whichever layer writes second detect-and-skip the existing record — rather than both layers writing unconditionally.

**Blocker / priority.** Not blocked. Low severity; file-and-forget until the ledger is next touched.

---

### Intentional: `process_qr_code_updates.js` and `process_tree_planting_link.js` must NOT take the script lock
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24326).**

**Context.** The 2026-09-10 lock work added `LockService.getScriptLock()` to four Telegram-log processors; a regression guard (tokenomics #473, `scripts/test_telegram_log_processor_lock.py`) now asserts that every handler owning a read-then-append dedup set takes the lock. Two files in the same project are **deliberately** lock-free and must stay that way:

- `process_qr_code_updates.js` — the `doGet` router. It **dispatches** to the child processors. GAS script locks are **not reentrant**, so a router that held the lock would deadlock its own children.
- `process_tree_planting_link.js` — holds **no** `getProcessed*MessageIds_` dedup state (verified: it appends rows but has no read-then-append window), so there is no race to close.

**Why filed.** So a future reader or agent doesn't "fix" the inconsistency by adding a lock to the router (deadlock) or assume the guard test is failing open. The guard test pins this: it fails if either file ever *grows* a dedup helper, forcing the author to add the lock **and** re-reason about the router deadlock note.

**Blocker / priority.** Informational — no action. Revisit only if either file gains dedup state.

### `seed_from_sheet.py` rebuilds manifests from the sheet, so any hand-attached field not present in a sheet column is silently wiped on every re-seed
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25671).**

**Symptom.** Re-running `lineage-assets/scripts/seed_from_sheet.py --execute` (the documented way to push sheet state into `qrs/*.json`) destroyed hand-attached lineage data. Concretely: 101 `2024OSCAR_CT_20260820_*` manifests carried a `seedling_photo_url` (the FounderHaus group photo) that existed **only in the JSON** — every full re-seed wrote `seedling_photo_url: ""` over it. A re-seed in thread 25671 was caught before shipping **only** because the diff was inspected; nothing in the script warns.

**Root cause (two parts).** (1) `scripts/lib/manifest.py::build_lineage()` builds lineage **purely** from sheet columns — it emits `seedling_photo_url` from col **R** (`Tree Seedling Photo URL`) and ignores col **S** (`Product Image`) entirely; a fresh `build_manifest()` on the CT row returns `""`. (2) `merge_preserve_events()` preserves only `events` whose `type` is not in `SEED_EVENT_TYPES` — it has **no** preserve path for lineage fields, so a field the sheet doesn't supply is lost by construction. The sheet is therefore the only durable home for any value, by design — but the design is undocumented and the failure is silent.

**Also found.** `COL["product_image"]` (idx 18) is mapped but **read by nothing** — `build_lineage` never emits `product_image`; `git grep product_image qrs/` = 0 files, while **1,558 sheet rows** carry a value in col S. So that column is either dead config or a missing feature — pick one.

**Fixed for the 101 rows (this thread).** The Product Image value was copied into col **R** on those rows (sheet edit), making the photo sheet-durable; a full sheet-wide re-seed then kept **all 104** photo-bearing tree manifests with **0 lost**. See `lineage-assets` PR #10.

**Proposed code fix (~30 min).** In `scripts/lib/manifest.py`: before writing, preserve any existing lineage key the fresh build did not populate (i.e. `for k,v in existing["lineage"].items(): merged["lineage"].setdefault(k, v)` — or skip emitting keys whose sheet cell is empty rather than emitting `""`). Then drop the col-S→col-R manual copy requirement. **Residual known regression, NOT fixed by the sheet workaround:** `qrs/FOUNDERHAUS_BOUGAINVILLEA_20260821_1.json` has `events[1].signed_by` + `events[1].sig_ref` (an Edgar-signed event) that do **not** round-trip through any sheet column — a re-seed drops them. A generic "preserve unknown/signed event fields" merge is the real fix. Blocker: none.

### `lineage-assets` PNG thumbnails are generated by a separate manual pipeline, so newly-seeded QR codes ship with a 404 `qr_image_url`
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25671).**

**Symptom.** `seed_from_sheet.py` writes `qr_image_url` = `.../lineage-assets/main/pngs/<qr_id>.png` for every manifest, and `build_index.py` publishes them to `qrs_index.json` → `truesight.me/physical-assets/serialized/`. But the `pngs/` directory is populated by a **different, manual** pipeline (the `tokenomics` `agroverse_qr_code_generator` batch compiler, invoked over Telegram by the `agroverse_qr_code_manager` SA). Seeding a code therefore yields an index row whose image 404s.

**Observed.** The 40 `2024OSCAR_AGL14_20260911_*` manifests (PR #10) have no corresponding `pngs/*.png`; 1,820 index rows vs 2,376 PNGs — the sets are not maintained in lockstep.

**Impact.** Low on the serialized **listing** page: its row template does not render `qr_image_url` (verified — no `<img>` for it), so rows display correctly. Higher on any per-asset provenance/credential view that does render the image.

**Proposed fix (~30 min).** Either (a) chain PNG generation into the seed flow (call the batch compiler for any manifest lacking a PNG), or (b) have `build_index.py` emit `qr_image_url: null` when the PNG is absent so consumers can fall back gracefully. (a) is truer to the invariant "every serialized asset has an image". Blocker: requires the `tokenomics` PNG compiler to be invokable headlessly (currently Telegram/GAS-driven).

### Serializing bulk kg inventory into N unit QR codes has no event type — it is a direct sheet edit only, with no signed audit trail
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25671).**

**Symptom.** Moving 40 kg of bulk-booked cacao into 40 individually-serialized 1-kg QR codes (AGL14, `2024OSCAR_AGL14_20260911_1..40`) had no expressible `submit_contribution` event. `lookup_event_docs` was checked across `QR CODE REGISTRATION`, `INVENTORY MOVEMENT`, `SALES EVENT`, and the QR-generation docs: none models *split a bulk quantity into N unit serials, set status, post no money movement*. Gary directed a **direct sheet write** instead — correct for avoiding a double-count of the sale (the USD was already booked once in the AGL14 `Transactions` rows 10–13), but it means the serialization act itself carries **no RSA-signed ledger record**.

**Contrast.** The GL side of AGL14 is fully signed (`[MANAGED LEDGER TRANSACTION EVENT]`, rows 10–13 of the AGL14 ledger, per the one-signed-blob-many-rows precedent). The QR side — 40 rows at `Agroverse QR codes` 1784–1823 — is unsigned sheet state only.

**Proposed fix (~60–90 min).** Add a `[SERIALIZATION EVENT]` (or extend `QR CODE REGISTRATION` with a bulk mode) that records: source QR/bulk lot, `split_quantity`, the generated `qr_id` range, target status, manager/custodian, and an explicit `no_financial_posting: true` flag — so the audit trail covers serialization without implying a sale. Until then, serialization remains reconstructable only from the sheet + the manifests it seeds. Blocker: none; needs an event-schema decision by a governor.

---

## Recently shipped

### FBE `Plot ID` canonical-label gap — RESOLVED 2026-09-10 (autopilot guard shipped, [truesight_autopilot#425](https://github.com/TrueSightDAO/truesight_autopilot/pull/425))
**Shipped 2026-09-10 (Sophia, thread 24321; governor go from Gary).** The autopilot no longer silently drops a non-canonical attribute key: `_DAO_GUARANTEED_LABELS` (`FBE → ["Plot ID"]`) is unioned into the catalog `canonical_labels` at merge (`_merge_catalog_labels`), and the legacy normalizer's bare `continue` was replaced with a loud `logger.warning` naming the dropped key + event. Regression test `tests/test_fbe_plot_id_normalization.py`. This makes the Edgar catalog's missing `"Plot ID"` label (gap 1) safe without touching `dao_protocol` (governor deferred that belt-and-suspenders PR).

**Incident it fixes (row-5 clobber).** An FBE for `B-06-108_20260908_research_1` had its `Plot ID` silently dropped, so `fbeUpsertFarm_` fell back to farm-slug matching and overwrote row 5 (`B-06-108`, 114 ha) `plot_type`: `maturing → research`. Row 5 was restored and the `sunmint` registry regenerated same-thread; same failure class as the Sítio Torres duplicate `PL-006`.

**Still open (optional hardening, not shipped).** (a) Add `"Plot ID"` to FBE `canonical_labels` in `dao_protocol`'s `events_catalog.json` — deferred by governor. (b) Make `fbeUpsertFarm_`'s slug fallback refuse to write `plot_type` when >1 row shares the slug (fail safe instead of clobber).

### ✅ Telegram-log processor locks are now LIVE on the pinned webhook deployments (`@45`/`@46`) — RESOLVED 2026-09-10
**Shipped 2026-09-10 (Sophia, thread 24326; governor go from Gary). Supersedes the `## Pending` entry filed earlier the same day that read "locks are live only in `@HEAD`".**

**What changed.** The two pinned deployments that serve the affected webhooks were repointed to fresh versions cut from `@HEAD`:

| Deployment | Webhooks it serves | Repointed to | Locks before | Locks after |
|---|---|---|---|---|
| `@44` `AKfycbyoFCTz…` | FARM_BOUNDARY_EVIDENCE · MEDIA_RETRACTION · PLOT_INVALIDATION · TREE_PLANTING_REJECT | **`@45`** | plot-inval ✅ · FBE ❌ · MR ❌ | ✅ ✅ ✅ |
| `@36` `AKfycbwm9TZ…` | TREE_GROWTH_MONITORING | **`@46`** | ❌ | ✅ |

`@32` (serves only QR_CODE_UPDATE + TREE_PLANTING_LINK) was deliberately **left alone** — both its files are the intentionally-unlocked ones, so a repoint there would be pointless risk.

**Verified, not assumed.** Read the *live version content* via the Apps Script API (`projects.getContent?versionNumber=`) — v45 and v46 both show `LockService.getScriptLock` in `process_farm_boundary_evidence`, `process_media_retraction`, `process_plot_invalidation`, and `process_tree_growth_monitoring`; `process_qr_code_updates` and `process_tree_planting_link` correctly read 0. Deployment→webhook bindings were confirmed by reading the live `dao_protocol` env (the earlier `@44`→FBE/MR mapping was an inference there; it is now observed).

**Caveat.** The underlying `clasp push` / pinned-deployment gap is a *class* of failure that will recur on the next `clasp push` — the root-cause entry in `## Pending` still stands and should own the durable fix (auto-repoint on push, or a post-push deploy hook). This entry only records that the *specific* lock fix is now live.

---

### CEPOTX/CoopCao site code `N-06-66` (Sítio Torres, Pacajá) — RESOLVED 2026-09-10 (governor-confirmed; registry updated)
**Shipped 2026-09-10 (Sophia, thread 25149).** Governor (Gary, thread 24442) **confirmed `N-06-66` is the correct issued CEPOTX site code** for the Sítio Torres (Pacajá) plot — the property of **Alexandre**, a CoopCao director-coordinator — superseding the earlier "outside the observed roster range" concern. `CEPOTX_SITE_CODE_REGISTRY.md` updated in the same PR: the COOPCAO observed range is annotated with `N-06-66` as governor-confirmed, and an anchors-table row was added (`N-06-66` / Sítio Torres (Pacajá) Plot 1 / Alexandre / COOPCAO), tying to the SunMint Plots sheet row 23, `sunmint/plots/index.geojson`, and the agroverse_shop farm page (PRs #308/#309). The follow-up's corroboration steps (re-OCR IMG_9694/9695, re-run the spoken-code clips) are no longer blocking — the code is treated as issued and authoritative.

**Original Pending entry (retained for history).** *Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).* Context: on the 2026-09-09 Pacajá site visit (loc3 — "Sítio Dois", producer **Alexandre**, a CoopCao director), the plot's CEPOTX site code was read as **N-06-66** from a phone-translator screenshot (IMG_9694: "O código dele é N0666"). `CEPOTX_SITE_CODE_REGISTRY.md` listed the **COOPCAO** family as **N-06-02 … N-06-52** — `N-06-66` fell outside that observed range, and the registry is marked "reported / unverified," so no name-match was possible; the code was registered on Gary's assumption. Impact: the code is on public surfaces (SunMint Plots sheet, `plots/index.geojson`, agroverse_shop farm page). Resolution: governor confirmed the code as issued (thread 24442), closing the registry-range question.

### `farm_media_manifest` couldn't parse DMS GPS — every Apple-media item got `latitude: null`
**Shipped 2026-09-10 ([farm-media-daemon#24](https://github.com/TrueSightDAO/farm-media-daemon/pull/24)).** `farm_media_manifest._parse_gps` handled only decimal (`float(split(","))`), so exiftool DMS strings (`3 deg 33' 25.20" S, …`) raised `ValueError` → `None`; `gps_coverage` read `0/N` and `paulo-la-do-sitio-para.json` needed a hand-written `_remediation` block. Now delegates to the daemon's own DMS-aware `farm_media_geo.parse_gps` (one shared parser) + 4 unit tests (decimal, exact DMS sidecar string, equality vs `farm_media_geo`, none/junk). Verified end-to-end on Cristo Rei: `GPS 0/13 → 12/13` (the 13th lacks GPS on the original).


### krake_ror disk-full durability — RESOLVED 2026-09-06 via AMI bake + ASG roll (sophia, thread 22224)
**Shipped 2026-09-06.** Durable fix landed after the 2026-09-06 ENOSPC incident (Bugsnag `Errno::ENOSPC`, getdata.io) per governor direction: baked custom AMI **`ami-0933e020a3e613189`** (`krake_ror_20260906`) from the fixed host — captures `/etc/logrotate.d/krake_ror` (daily + size 200M, rotate 5, copytruncate, delaycompress, `su ubuntu ubuntu`); created LT `lt-085100be44b6079cc` **v4** → new AMI, set `$Default` (v3 = rollback); rolled ASG zero-downtime (scale to 2, validated new instance: HTTP 200 / logrotate present / disk 53%, drain old, terminate). Running instance now `i-0f7f3490dc465136b` (54.224.186.212). Any future recycle boots with logrotate → recurrence closed. Volume growth explicitly NOT done (governor 2026-09-06: 8G root fine with logrotate capping logs). Optional residual: `df /` ≥ 85% alert.

### krake_data disk-full (ENOSPC since Jun 4) — RESOLVED 2026-09-06 via kernel purge + df guardrail (sophia, thread 22224)
**Shipped 2026-09-06.** Second out-of-storage incident caught during the krake_ror sibling sweep — same failure class, worse: root **100% / 0 free** on `krake_data` (`i-07c76510b231d787f`, 52.5.179.48, t3.medium, 316d uptime), rsyslog ENOSPC since **2026-06-04**, systemd-journald failing minutes before diagnosis. Postgres 9.5 `dev_panel` (serves krake_ror + krake_sk_consolidated) safe on separate 50G vol `/krake_data_cache` (`/dev/nvme1n1`, 51%). Root cause: **46 old `linux-image-aws` kernel sets** (`5.4.0-1029…-1089`) + **40 orphaned `/usr/src` header dirs** (the 4.6G bulk — already-`rc` packages never cleaned) + **40 orphaned `/lib/modules` trees**, never purged in 316 days. Remediated per governor "fix it": purged old kernel set, `rm -rf` the 40 orphaned header dirs + 40 orphaned module dirs (kept running `-1092` + newest `-1103`), truncated 512M auth.log, apt cache + journal vacuum + disabled snaps → root **100% → 30% (5.4G free)**. Verified: journald + syslog writing again, Postgres online, dpkg audit clean, running-kernel modules intact, **no reboot needed**. Guardrail added: autopilot cron (30-min) `df-alert-remote-krakedata.sh` (SSH + `server_us.pem`, Telegram at ≥85/93%, same channel as autopilot df-alert) — closes the "no alert → silent 3-month fill" gap. Infra row updated (AWS_DIGITAL_INFRASTRUCTURE.md §2.1). Sibling sweep of remaining fleet (seni_ror 62% healthy; krake_nginx/krake_sk_consolidated need SG/key access) is optional next.

### krake_ror recycled to v5 instance + consolidated fleet df-alert (sophia, thread 22224)
**Shipped 2026-09-09.** The krake_ror ASG recycled 2026-09-09 04:47 UTC — old instance `i-0f7f3490dc465136b` (54.224.186.212) replaced by `i-069771c1f79288216` (**98.81.159.70**) on LT v5 = the durable logrotate-fix AMI `ami-0adfbc216d627e058`. Verified on the new box: both logrotate rules present (`/etc/logrotate.d/krake_ror` + `krake-ror-upstart`), upstart log bounded (~1.2M live, archives compressed), disk 58% stable, puma 5.1.0 healthy — the baked fix survived the recycle as designed. The new instance inherited the old 211M rotated upstart archive via the AMI snapshot; force-rotate compressed it to 1.6M.gz (~210M reclaimed). **Consolidated fleet df-alert guardrail:** `/usr/local/bin/df-alert-fleet.sh` (autopilot cron, 30-min, replaces df-alert-remote-krakedata.sh) probes krake_data 33%, seni_ror 65%, dao_protocol 63%, krake_ror 98.81.159.70 with per-host keys; Telegram at ≥85/93%, never auto-deletes, silent under threshold. Infra rows updated (AWS_DIGITAL_INFRASTRUCTURE.md §2.1). Remaining unreachable from autopilot: krake_nginx (port 22 refused), krake_sk_consolidated (timeout) — need SG/key access to extend coverage.


### [SHIPPED] sunmint cache_satellite_scenes.py null-geometry guard (CEPOTX rename follow-up)
- **Date:** 2026-09-05
- **Issue:** `scripts/cache_satellite_scenes.py` plots loop crashed on explicit `"geometry": null` — `geom = feat.get("geometry", {})` returns None, then `geom.get("type")` raises `AttributeError: 'NoneType' object has no attribute 'get'`. Crashed every satellite run until the sheet's null-geom test rows were removed (2026-09-05). Trees loop was already null-safe.
- **Resolution context:** stale `satellite/plot_{SA-P1,CL-P1,LD-P1}/` dirs + `plots/by-plot/{SA-P1,CL-P1,LD-P1}.geojson` retained as inert residue per governor resolution 2026-09-05 (option c — renames recorded as alias tombstone, agentic_ai_context PR #925). NOT deleted.
- **Shipped 2026-09-06 by Sophia:** one-line guard `geom = feat.get("geometry") or {}` at `scripts/cache_satellite_scenes.py:156` — uploaded via Contents API to sunmint@main (commit 90eaa4c). UAT: pristine original crashes on a null-geom fixture (`AttributeError` line 157, rc=1); fixed script exits 0, caches the real polygon (OK-PLOT: 4 scenes), skips the null feature (manifest plots = [OK-PLOT]). Syntax + py_compile clean.
- **Link:** https://github.com/TrueSightDAO/sunmint/commit/90eaa4c30f957e561ca25b172661ae9d982eb386
### [DONE] Usage/meta logging in truesight_autopilot_transcript — shipped 2026-09-01
- **Date:** 2026-08-31
- **Issue:** The transcript repo AGENTS.md/ROADMAP.md describe `usage.jsonl`, `meta.json`, `messages.jsonl` + `scripts/append_usage.py` + a summarize CLI — but only `transcript.md` is actually written. Consequence: "how much time/tokens did X cost?" cannot be answered exactly (was reconstructed from git merge timestamps for the Rancho Maranta effort, ~15.5h wall-clock / ~360 active min lower bound).
- **Fix:** implement `scripts/append_usage.py` (token/usage rows per tool call) in the transcript repo + meta.json writer; wire into the autopilot transcript append path; then a `summarize` CLI for cost queries.
- **Shipped 2026-09-01 by Sophia:** `scripts/append_usage.py`, `scripts/write_meta.py`, `scripts/summarize_usage.py` + `scripts/tests/test_usage_tools.py` landed on truesight_autopilot_transcript@main (commits bcb39c0, 3a6fef8, fe2ac2d, 216264b). Local suite green (compileall + ruff + format + 5 pytest). Smoke-verified append→summarize end-to-end. Wiring into the autopilot runtime's transcript-append path remains (runtime harness, not in a DAO repo — separate follow-up).

### SunMint satellite cache pipeline: Earth Search STAC (replaces CDSE) — LIVE
**Shipped 2026-08-31. Owner: Sophia.** The CDSE registration path was dropped (registration broken; CDSE no longer offers anonymous Sentinel-2 WMS — only STAC public, `sh.dataspace` needs auth). Replaced with **Earth Search STAC** (AWS-hosted Sentinel-2 L2A, anonymous, no key): `sunmint/scripts/cache_satellite_scenes.py` queries `https://earth-search.aws.element84.com/v1/search` (POST, explicit RFC3339 datetime — `now` token 400s), downloads the lowest-cloud scene's public preview into `satellite/<lat>_<lng>/<scene-date>.jpg` + `satellite/manifest.json`. Verified live: 9 cells / 36 scenes; FounderHaus + Rancho Maranta cells + plot dirs (RM-P1/RM-P2) committed. Map satellite history strip (truesight_me_beta #322) layers `manifest.json` by date with cloud badges; plot-aware caching reads `plots/index.geojson` — the ONLY plot registry (`trees/plots.geojson` is a dead path, guarded). Remaining: confirm the daily workflow auto-commits (06:30 UTC schedule; box token lacks workflow-dispatch scope — a human can trigger via Actions → workflow_dispatch). **No CDSE registration needed — Gary can drop that task.**

### DEPLOY_PUSH_SOP Phase 2 — lease+audit enforced in all deploy tools (SHIPPED 2026-08-25)
**Shipped by sophia.** The deploy-push audit trail is now **enforced in code**, not just documented:
- `ecosystem_change_logs/deploys/` ledger + `scripts/append_deploy_record.py` (Phase 1, manual logging).
- `truesight_autopilot#313` — new `app/deploy_ledger.py` (check_lease/acquire_lease/close_lease/append_deploy_record, 30-min TTL, fail-open on errors, hard-block on a live lease) wired into `gas_deploy_project.py` (blocks `--push` on a clasp scriptId with a live lease), `sync_beta_to_prod.py` (lease on prod repo before merge-upstream), and `deploy.py`+`main.py` (ec2/autopilot lease threaded through the two-phase re-exec, closed on fresh boot). 10 new tests; gas-tool tests made hermetic (they were hitting the real API — a stale test lease actually blocked a duplicate push, proving the lock works).
- `tokenomics#429` — standalone `scripts/deploy_ledger.py` (stdlib-only, for direct LLM checkouts) + `deploy_gas_project.py` lease check/acquire/record/close before any `--push`; `--lease-id` passthrough prevents self-deadlock when the autopilot tool owns the lease.
- Backfilled ledger record `deploy_20260825T160310Z_truesight-autopilot` for the #313 merge itself.
- **Remaining (Phase 3):** CI-level validation (a GitHub Action asserting every push records a ledger entry) — not yet built.

### Telegram attention watchdog — ACTIVATED 2026-06-06

Operator completed the my.telegram.org + Telethon login (the earlier
code-delivery stall resolved on a clean retry); session created, unit
`truesight-autopilot-watchdog` active, log shows `watchdog up as garyjob`.
The June-12 failure mode is now guarded. Possible v2s parked: Sophia-drafted
Telegram replies (the user-session already permits sending), Gmail-leg digest
unification.

### Telegram attention watchdog — minimal v0 (SHIPPED 2026-06-05, activation pending operator login)

Shipped as [truesight_autopilot#102](https://github.com/TrueSightDAO/truesight_autopilot/pull/102)
and deployed to the sophia box same day: read-only Telethon user-session
watcher (`app/attention_watchdog.py`), Saved-Messages nudges (4 h / 2 h dated)
+ daily 9 am digest, 17 heuristic unit tests, systemd unit installed but
**stopped until the operator runs the one-time login**
(`scripts/telethon_login.py` after adding `TELEGRAM_API_ID/HASH` to the box
`.env`). Originally filed 2026-06-06 after the June 12 cacao-serving
coordination miss. Gmail-leg unification remains a possible future follow-up.

### Autopilot tooling gaps ×4 (migrated from the duplicate `OPEN_FOLLOW_UPS.md`) — resolved by 2026-06-03 capability uplift

Sophia filed four items in a separately-created `OPEN_FOLLOW_UPS.md` on
2026-05-31 (large-file updates via GitHub API; SSH key + git client on her box;
`open_fix_pr` repo enum too narrow (still open); `upload_file_to_github` lacking `sha` — ✅ RESOLVED (truesight_autopilot #87, 2026-06-03; re-verified 2026-09-11 by a create→update probe on `agentic_ai_context` → `created` then `updated`, no 422). See `handoffs/MEDIA_GALLERY_PUBLISHER_PLAN.md` PR2.
update support). All four were resolved by the `SOPHIA_CAPABILITY_UPLIFT_PLAN.md`
PRs — verified present 2026-06-06: `app/tools/git_tools.py` (native git
branch+PR with search/replace semantics, no file-size limit),
`app/tools/ssh_tools.py` (`sophia_infra` fleet key), `upload_file_to_github`
auto-fetches `sha` for updates, and `settings.allowed_repos` now includes the
beta/prod site repos. The duplicate file is now a tombstone redirect; this file
is the single backlog.

### `/aum` dedicated page + per-ledger click-through on `/treasury` — 2026-05-20

Mirrors the `/treasury` pattern shipped earlier same day. New `/aum`
page reads `treasury-cache/dao_offchain_treasury.json` and renders
two sections — **Assets by ledger** first (each managed ledger
expanded to show currencies it holds), then **Per currency** (each
currency expanded to its per-ledger split). Both `/aum` and
`/treasury` per-ledger rows are now click-throughs to the source
Google Sheet, via a new `ledger_urls` dict in the GAS
`treasury_breakdown` payload. Landing-page AUM card flipped from
inline `<details>` to `View breakdown →` link; the dead
`wireStatBreakdowns` / `fetchTreasuryCacheOnce` / `renderUsdTreasuryBreakdown` /
`renderAumBreakdown` machinery (~85 lines) was removed from
`index.html`.

GAS also picked up a small `&refresh=1` escape hatch on the
`treasury_breakdown` endpoint for warming the cache after schema
changes without waiting for the cron.

PRs:
- TrueSightDAO/tokenomics#304 (squash `2640d1e`, GAS deploy `@10`)
- TrueSightDAO/truesight_me_beta#134 (squash `26947f7`, prod cherry-pick `25a6a9e`)

### `dao_client onboard_retail_partner` MVP — 2026-04-28

Manifest-driven CLI that automates the deterministic ledger + inventory
steps from `RETAILER_TECHNICAL_ONBOARDING.md` §3:

- Step 1 `[CONTRIBUTOR ADD EVENT]` (with name pre-formatted as
  `<First> - <Store>` to dodge Edgar's auto-rename).
- Step 2 `Contributors!U` (Mailing Address). Explicitly does **not**
  toggle col T — that flag is reserved for online-fulfillment managers
  (Gary + Kirsten only).
- Step 3 `Agroverse Partners` row append.
- Step 13 `[INVENTORY MOVEMENT]` loop for opening-order QR codes.
- Step 14 subprocess `sync_agroverse_store_inventory.py` and
  `sync_partners_velocity.py` so JSON snapshots refresh.

Idempotent at every step. `--dry-run` is the default. Worked-example
manifest in `examples/onboarding/the-way-home-shop.yaml` replays the
2026-04-28 onboarding as a no-op.

Steps still operator-manual in MVP: partner page, discovery surfaces,
photo download, PR creation (steps 4 / 5–10 / 11 / 12 / 15). Script
prints copy-paste instructions at the end. v1 covers those — see the
remaining Pending entry above.

PR: https://github.com/TrueSightDAO/dao_client/pull/11

---

### `[STORE ADD EVENT]` canonical pattern (additive slice) — 2026-04-28

Signed Hit List adds now route through the same Edgar pattern as retail
field reports: dao_client / DApp signs `[STORE ADD EVENT]` → Edgar
`/dao/submit_contribution` → Telegram Chat Logs → `WebhookTriggerWorker`
fires `processStoreAddsFromTelegramChatLogs` GAS scanner → `addNewStore`
on Hit List + audit row on **Store Adds** dedup log
(`1qbZZhf-…`, gid 1208101506; col B `telegram_update_id` is the dedup
key). Verified end-to-end: 3 Psychic Sister referrals (Clary Sage,
Casa de Ritual, La Sirena Botanica) added as Research rows on Hit List
rows 526–528 with referral provenance in Notes + Sales Process Notes;
scanner replay = 0/0/0/0 (perfectly idempotent).

Two follow-ups split out into Pending above:
1. Migrate `dapp/stores_nearby.html` Add Store form off the legacy
   direct GAS GET onto the same Edgar path.
2. Fix the pre-existing `addNewStore()` GAS `setValues` dimensional
   bug so audit logs say `added` instead of `error` even though the
   actual Hit List rows write correctly.

PRs:
- TrueSightDAO/dao_client#9 — `add_hit_list_store.py` module.
- TrueSightDAO/sentiment_importer#1042 — Edgar `[STORE ADD EVENT]` branch.
- TrueSightDAO/tokenomics#250 — `processStoreAddsFromTelegramChatLogs`
  GAS scanner + Store Adds tab schema.

---

## tribomirimbahia Phase 1B — music library tagging

**Context:** Phase 1A done 2026-05-10 (TrueSightDAO/tribomirimbahia#2) — 39 Bico
Duro per-move clips published. Phase 1B is the next sequential step before the
Phase 2 site can do session generation.

**Scope:** Build `tribomirimbahia/data/music_library.json` per spec §5 + §3:

- 12 capoeira tracks (Gary curates the YouTube URLs).
- Per track: `id`, `title`, `youtube_url`, `duration_seconds`, `bpm` (estimate
  via `librosa` or DeepSeek tap), `tempo_category` (Slow/Medium/Fast),
  `style_notes` (berimbau-heavy, drums-focused, etc.).
- Suggested mix: 3–4 slow berimbau (Foundation/warm-up), 4–5 medium drum-heavy
  (Defense/Attacks), 2–3 fast energetic (Aerials/Floreios).

**Hand-off:** Per `AGENT_BRIEF.md` matrix — BPM detection + tagging is DeepSeek
territory (numeric, no cultural nuance). Gary spot-checks the tempo arc since
it affects practice feel.

**Blocker:** Gary needs to curate the 12 YouTube URLs first.

## tribomirimbahia Phase 2 — capoeira.agroverse.shop site build

**Context:** Phase 1A produced `tribomirimbahia/data/moves.json` (39 moves with
YouTube URLs); spec PDF + AGENT_BRIEF.md describe the static-site requirements.

**Scope:** Greenfield build of `~/Applications/capoeira/` (currently empty)
following the AGENT_BRIEF.md "Phase 2 — Core Site Build" section. Mirror
agroverse_shop conventions (no frameworks, static HTML/CSS/vanilla JS).
Mandatory: `agentic_ai_context/DAPP_PAGE_CONVENTIONS.md` for every page.

**Hand-off:** Claude drafts pages; Gary reviews landing copy + Bahia tone before
flipping DNS. The 4 open questions in AGENT_BRIEF.md "Open questions before
Phase 2" need Gary's answers first (deploy target, Stripe account, Bico Duro
consent, fundraising goal).

**Blocker:** Open questions in AGENT_BRIEF.md not yet answered.

## capoeira: curriculum-based session structure

**Context:** Practice tool at `capoeira.agroverse.shop/practice.html`. Phase 1A
shipped (39 moves), data calibrated for 45-min single-theme sessions in
TrueSightDAO/capoeira#7. But Bico Duro's actual teaching (per his spoken
curriculum in cqKMvYbB1Kw — "primeira coisa: ginga; segunda coisa mais
importante: defesa; terceira coisa: ataque") is NOT single-theme; it's
Foundation → Defense → Attacks progression every session.

**Scope:** Add an alternative session-generation mode that composes:
1 Ginga warm-up (Foundation) + 2 Defense moves + 2-3 Attack moves +
optional Flow cool-down (Giro). This un-skips the Foundation and Flow
themes (currently filtered out because they have <4 moves each) and aligns
the practice tool with how Bico Duro actually teaches.

**Where to edit:** `assets/js/session-generator.js` — add a `pickCurriculumSession()`
alongside the existing single-theme path. Add a UI toggle on `practice.html`
("Single-theme drill" vs "Curriculum session"). Default to curriculum once
implemented.

**Blocker:** None — calibrated data + working single-theme algorithm both
shipped TrueSightDAO/capoeira#7.

## capoeira: session-generator algorithm variety

**Context:** Same Phase 1A practice tool. Current `pickMoves()` is greedy on
weighted score; with identical difficulty bias, sessions 1 and 4 in the headless
simulation were byte-identical (same 6 Beginner Attack moves in the same order).

**Scope:** Add randomized tie-breaking — group candidates by `_weight` bucket,
shuffle within bucket, then pick. Or sample with weighted probability rather
than sort+head. Keeps the difficulty bias intent but diversifies outputs.

**Where to edit:** `assets/js/session-generator.js` `pickMoves()` greedy loop.

**Blocker:** None.

## sentiment_importer: repurpose /compare into a backtester

**Context:** Repurposing the `/compare/TICKERS/DATE/PERIOD` view (was
correlation/sentiment overlay) into a strategy backtester — compare buy-and-hold
vs a rebalance-band (cash-sleeve, configurable initial position) across tickers,
reporting realized return / CAGR / Sharpe / maxDD / turnover. Designed jointly
2026-05-25; two specs written, **not yet implemented**.

**Specs (in repo root):**
- `sentiment_importer/BACKTEST_DATA_ENDPOINT.md` — `GET /backtest/data` clean-data
  JSON (real bars, no forward-fill; risk-free = `daily_yield_curves.month_3 ÷ 100`).
  Deliberately **no** split/anomaly detector — the rendered chart is the detector
  (human-in-loop); fix bad data manually via `EodHdPriceRefresher.new.perform(id)`.
- `sentiment_importer/BACKTEST_STRATEGY_ENGINE.md` — JS `runStrategy(bars, riskFree,
  spec)` pure function; engine runs client-side; server only serves data.

**Scope (when greenlit):** build data endpoint first (so series are eyeball-able),
then wire JS engine. Idealized fills for v1 (fractional, no cost). Rolling-window
distribution + signal strategies (macd/rsi/buy_now) parked for later.

**Blocker:** implementation not yet greenlit as of 2026-05-25.

## blog post: "Gary and Claude" — knowing when NOT to automate

**Context:** Write a first-person (Claude-as-teammate voice) post for truesight.me
about the backtester design session above. Angle is **subtraction, not building**:
Claude kept proposing data-quality machinery (scanner → auto-repair → flag-only),
Gary kept stripping it back to "just look at the chart" — landing on Moravec's
paradox (in an interactive tool the human is already in the loop, so a detector is
redundant). "The best anomaly detector was the chart we were already drawing."
Byline: Gary and Claude.

**Scope:** hand-written page in `truesight_me_beta`; promote to prod via
`gh repo sync` (NOT `--force` — beta/prod CNAMEs intentionally diverge). Include a
real PLAY equity-curve screenshot as the punchline. Fits existing llms.txt surface.

**Blocker:** gated on the backtester shipping — write it once the tool works and
there's a real chart to show.

## dao_protocol: enable immediate-after-sale Agroverse inventory refresh

**Context:** The Edgar → dao_protocol extraction left
`DAO_PROTOCOL_AGROVERSE_INVENTORY_GAS_WEBAPP_URL` + `_PUBLISH_SECRET` empty because
the HTTP publish path is **dormant end-to-end** (verified 2026-05-26): GAS project
`1P0Mg33i…` (`update_store_inventory`) has **no** `AGROVERSE_INVENTORY_PUBLISH_SECRET`
script property (so `verifyPublishToken_` → false → the HTTP actions
`publishInventorySnapshot`/`recalculateAndPublishInventory` reject every call as
Unauthorized), the worker's `AGROVERSE_INVENTORY_*` env is unset on the `seni_sk_new`
worker host (Sidekiq **is** running there — the worker just no-ops on the missing env),
and store-inventory freshness is currently maintained only by the GAS **hourly
time-driven `updateStoreInventory` trigger**. dao_protocol's `inventory_snapshot.publish()`
(wired into `dispatch.py` on `[ASSET RECEIPT EVENT]` / sales) no-ops to match — see
`EDGAR_DAO_EXTRACTION_PLAN.md` Outstanding §2.

**Scope (net-new setup, NOT provisioning — there is no existing value to copy):**
1. Mint a shared secret; set it as the `AGROVERSE_INVENTORY_PUBLISH_SECRET` script
   property on GAS `1P0Mg33i…` (Apps Script editor for that project).
2. Put the same value + the deployed `/exec` URL into
   `seni_ror_new:/home/ubuntu/dao_protocol/.env` (`DAO_PROTOCOL_AGROVERSE_INVENTORY_GAS_WEBAPP_URL`
   / `_PUBLISH_SECRET`, chmod 600) and `sudo systemctl restart truesight-dao-protocol`.
3. (Optional) re-enable `seni_sk` on Rails if the immediate path is wanted there too.
4. Verify a signed `[ASSET RECEIPT EVENT]` / sale triggers a snapshot refresh within
   seconds (GAS returns 200, not Unauthorized) instead of waiting up to an hour.

**Payoff:** sub-second store-inventory JSON refresh after a sale/receipt instead of
up to a ~1-hour lag. Purely additive — the hourly trigger already keeps data correct.

**Blocker:** none (opt-in; only worth doing if the up-to-1-hour refresh lag is a
problem in practice).

## Edgar → dao_protocol: post-soak cleanup (revisit ~2026-06-25)

**Context:** The Edgar → dao_protocol migration is functionally complete as of
2026-05-26 — all 6 routes cut over (PR2 `/proxy/gas`, PR3 newsletter/email-agent,
PR4 shipping_rates, PR5 `/dao/submit_contribution`, PR6a `/qr-code-check`+`/link-email`,
PR6b `checkout.session.completed` order-sync delegation, all live), env provisioned,
60 unit tests, payment path sandbox-verified. The remaining items are deliberately
**deferred ~30 days to let the live ramps soak** before removing the Rails rollback
net. Full state: `EDGAR_DAO_EXTRACTION_PLAN.md` Outstanding.

**Do not start before ~2026-06-25** unless the ramps are clearly stable sooner. By
then, confirm via the dao_protocol journal + Bugsnag that the ramped routes have run
clean (esp. `/qr-code-check` payments and `/dao` dispatch), and ideally that a real
checkout reconcile→SOLD has happened.

**Scope (3 parts):**
1. **PR7 cleanup (the soak-gated part)** — remove the now-dead Tenant B code from
   `sentiment_importer`. **Recommended phased + MERGE-NOT-DEPLOY** (keep the branch;
   don't pull onto `seni_ror_new`, so the running Rails keeps the controllers as the
   instant nginx-flip rollback until you're fully confident):
   - Safe first: delete `MetaCheckoutOrderSyncWorker` (dead since PR6b) +
     `NewsletterController`, `EmailAgentController`, `AgroverseShopShippingRatesController`
     + their routes (all fully verified, read/redirect, lowest risk).
   - Hold longer: `qr_code_check_controller` (payment-critical; reconcile→SOLD not yet
     e2e-tested), `proxy_controller`, and the `dao_controller#submit_contribution`
     **action only** (the controller has ~16 other live `/dao/*` routes — surgical removal).
   - The `/stripe_webhook` entry + subscription handling stay on Rails (decision A).
2. **dao_protocol `README.md`** — reframe the "Edgar (source: `sentiment_importer`)"
   framing: this repo now contains the **server** that serves the ramped endpoints
   (extracted from `sentiment_importer`, which remains the Rails trading platform).
   Keep the legit historical PR refs (`sentiment_importer#1024`, `#1028`).
3. **truesight.me blog post** that still references `sentiment_importer` — locate and
   update to dao_protocol where it describes the contribution server. (Mind the
   beta→prod CNAME divergence on publish: `gh repo sync`, NOT `--force`.)

**Blocker:** time-gated — let the ramps soak (~30 days, revisit on/after 2026-06-25).

---

## truesight_autopilot: stop compiling `dao_client` native extensions on every deploy — 2026-05-30

**Context.** Every `deploy_autopilot()` invocation runs `pip install -r requirements.txt`, which includes:

```
truesight-dao-client @ git+https://github.com/TrueSightDAO/dao_client.git
```

pip git-clones the repo into `/tmp/pip-install-*/...`, then builds the wheel — which **compiles `cryptography` + `cffi` native extensions** (cryptography is a transitive dep of dao_client). On a t3.small this takes 30–60 s. The compile is a long-running CPU-bound subprocess that's vulnerable to SIGTERM cascades from parent worker restarts — surfaced as `Phase-two subprocess failed (exit=-15)` errors on 2026-05-30 ([autopilot#83](https://github.com/TrueSightDAO/truesight_autopilot/pull/83) was an LLM-generated PR that misdiagnosed this as OOM; closed). It's also the slowest single step of the deploy by ~10×.

**Options, in increasing order of effort:**

1. **Pin to a release tag + cache `~/.cache/pip` between deploys.** Add `@vX.Y.Z` to the requirements line so pip's resolver short-circuits when the tag is unchanged. Cheapest; eliminates redundant builds for unchanged versions but still rebuilds on each version bump.
2. **Publish `dao_client` as a wheel.** Either to public PyPI (matches DAO transparency posture) or to a private artifact store (GitHub Packages, internal index). pip pulls a binary; no compile. Best long-term; needs CI on dao_client to build + push on each release.
3. **Vendor `dao_client` into `truesight_autopilot`.** Copy `truesight_dao_client/` into autopilot, drop the git+ dep. Decouples deploy speed from dao_client's release cadence. Costs duplication; loses single-source-of-truth.
4. **Switch native deps for pure-Python alternatives.** cryptography → PyCryptodome (also has C, but easier wheels) or pure-Python RSA. Bigger refactor in dao_client; affects signed-event throughput.

**Recommendation.** Start with (1) — five-minute change in `requirements.txt`. If deploy time still dominates after that, do (2). (3) and (4) are escape hatches if dao_client's release cadence becomes a deployment bottleneck.

**Related architectural concern (separate but adjacent).** The deploy's phase-two subprocess runs inside the autopilot worker's cgroup, so any worker restart (LLM tool retry, telegram-adapter race, ELB-driven restart) propagates SIGTERM into the pip subprocess and kills the compile. Fixing the compile cost via (1)/(2) shrinks the window where this can bite. The "right" fix for the cgroup-coupling itself is to run phase-two via `systemd-run --collect --unit deploy.$(date +%s)` so it's isolated from the worker's lifetime — log as a separate follow-up if pip-compile cost stops being the limiting factor.

**Blocker.** None. Ship (1) immediately when convenient.

**Owner.** Unclaimed.

---

## truesight_autopilot: migrate sophia from `certbot --nginx` to `certbot certonly` + repo-owned SSL config — 2026-05-30

**Context.** sophia.truesight.me's TLS deploy uses `certbot --nginx -d sophia.truesight.me ...` in deploy step 4. That mode obtains the Let's Encrypt cert AND mutates the nginx server block in-place — adds `listen 443 ssl`, `ssl_certificate ...`, the 80→443 redirect block, all marked `# managed by Certbot`. Because `/etc/nginx/sites-available/sophia` is a symlink into the repo at `/opt/truesight_autopilot/config/nginx/sophia.conf`, certbot's edits land inside the git checkout. The repo is therefore "dirty" between deploys, and `git pull` refuses to merge with `"Your local changes to the following files would be overwritten"`.

We solved this in [autopilot#77](https://github.com/TrueSightDAO/truesight_autopilot/pull/77) by swapping `git pull` for `git fetch + reset --hard origin/main + clean -fd` in `deploy.py` (matching what `scripts/deploy.sh` already did). Deploys are now idempotent and self-healing: certbot dirties → next deploy resets → certbot re-adds the SSL directives → repeats.

It works, but it's pragmatic rather than clean.

**Goal / shape.** Migrate to `certbot certonly --webroot -w <docroot> -d sophia.truesight.me` so certbot only writes to `/etc/letsencrypt/live/...` and **never touches** the nginx config. The repo's `sophia.conf` becomes the full source of truth — `listen 443 ssl`, `ssl_certificate /etc/letsencrypt/live/sophia.truesight.me/fullchain.pem`, the port-80 redirect server block, all version-controlled. Cert renewal runs via certbot's cron job and reloads nginx without touching any sites-{available,enabled}/sophia file.

**Trade-off snapshot:**

| Concern | Current (autopilot#77) | After migration |
|---|---|---|
| Repo dirty between deploys | yes (expected, self-heals) | no, always clean |
| Bootstrap on a fresh host | certbot --nginx wires SSL automatically | needs an initial cert before nginx with `listen 443 ssl` will start — chicken-and-egg, ~10-line preflight |
| Cert renewal | re-dirties; next deploy resets | silent (certbot cron + `nginx -s reload`) |
| SSL config in version control | partial | full |
| Lines of deploy code | tiny | needs the bootstrap preflight |

**When this becomes worth doing:**
- A second governor architect deploys the same service and the dirty-repo state confuses them.
- A Let's Encrypt edge case (renewal failure, multi-domain cert, account migration) produces broken nginx via the auto-edit path.
- We add a second TLS-bearing subdomain on the same host (the current pattern doesn't compose cleanly — each `certbot --nginx` run re-walks every server block).

**Blockers.** None technical. Choice is taste vs effort. ~2 hours of work: write the cert-presence preflight, fold the SSL directives into `sophia.conf`, change the deploy step, smoke-test on a fresh EC2 (or in a Docker container).

**Owner.** Unclaimed.

---

_(empty — move entries here with a one-line reason when they're no longer
relevant)_

## Closed without shipping
### Tree growth measurement 'reject' path — CLOSED as by-design
**Closed 2026-08-31 (no code). Owner: Sophia + Gary.** The earlier-flagged gap ("no manual reject for growth measurements") is by-design: invalid measurements are auto-rejected at submission by the GAS gates (RSA signature, registered identity, tree-exists in registry, 200 m proximity) — failing rows never land. Test evidence: TEST_TREE_E2E measurements (13.6/13.8/14.2) never reached the tracking tab; only the sentinel-signed test row landed (since removed). Measurement rows are monitoring records only — credits mint exclusively via a future [CARBON CREDIT ISSUANCE EVENT] — so a manual reject UI is unnecessary. E2E test cleanup completed 2026-08-31: test row deleted from 'Tree Growth Measurements'; 2 test photos removed from sunmint/images/growth/.

