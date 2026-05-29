# Tokenomics Google Apps Script — folder restructure + manifest convention

**Status:** PLANNING — roadmap committed, PR-1 pending.
**Owner:** Gary Teh (+ AI sessions)
**Created:** 2026-05-28
**Convention:** Tracked roadmap required by `OPERATING_INSTRUCTIONS.md` §5 before implementation. Keep the **Resume tracker** current as each unit lands. Reference pattern: `AUTOPILOT_CAPABILITY_MANIFEST_PLAN.md` (the same one-declarative-file-per-deployment-unit idea applied to GAS).

---

## 1. Goal (why this exists)

The autopilot transcript on 2026-05-28 14:03 made the problem concrete:

> "The mirror only has `.clasp.json`. The deployment URL isn't tracked in the repo. Let me check the `assetVerify` URL — it's the same GAS project that handles identity verification…"

The LLM (autopilot or any human session) can't deterministically answer:

1. **If I edit this `.gs` file, which GAS scriptId redeploys?**
2. **What's the `/exec` URL that file's `doGet`/`doPost` runs at?**
3. **What caches go stale on a `clasp push` and need an explicit refresh?**
4. **Who calls this script — what consumers will I break?**

Today the answers live scattered across `.clasp.json`, top-of-file Apps Script project URL comments, READMEs, and the GAS web UI. Some of that state is intentionally gitignored (per `tokenomics/.gitignore`); the rest is undocumented convention. So every "deploy this GAS thing" exchange burns LLM turns reconstructing what should be 1-file lookups.

End state: each GAS project gets its own subfolder with a `manifest.json` carrying everything an LLM (or a `gas_deploy_project` autopilot tool, later) needs to push + refresh.

---

## 2. Audit findings (2026-05-28 walk of `tokenomics/google_app_scripts/` + `clasp_mirrors/`)

### Topology today

- **`tokenomics/google_app_scripts/<theme>/`** — 21 thematic folders (human-readable; canonical source of `.gs` files).
- **`tokenomics/clasp_mirrors/<scriptId>/`** — 51 clasp-managed deploy mirrors, named by opaque scriptId.
- **`.gitignore`** explicitly gitignores `clasp_mirrors/**/*.js`, `clasp_mirrors/**/appsscript.json`, `clasp_mirrors/**/Version.gs`. The clasp mirrors are treated as *derived* artifacts; the **`.gs` sources under `google_app_scripts/<theme>/`** are the source of truth.

### The mismatch (the core problem)

Multiple thematic folders contain **multiple distinct GAS projects** (i.e. multiple `scriptId`s). From the audit:

| Thematic folder | scriptIds it covers |
|---|---|
| `agroverse_qr_codes/`           | 3 (`1MnAs...`, `1N6o...`, `1UrBg...`) |
| `tdg_asset_management/`         | 3 (`15qbf...`, `177OJ...`, `19Wag...`) |
| `tdg_identity_management/`      | 3 (`10NKp...`, `1m8IZ...`, `1zKgM...`) |
| `tdg_inventory_management/`     | 3 (`1QtK-...`, `1dsWe...`, `1duQF...`) |
| `tdg_scoring/`                  | 3 (`1-ts0...`, `1BHAG...`, `1Q5Hf...`) |
| `webhooks/`                     | 3 (overlapping w/ tdg_scoring + tdg_asset_management) |
| `tdg_credentialing/`            | 1 (`1Dj3-...`) |
| `tdg_shipping_planner/`         | 1 (`1Og2g...`) |
| `seacoast_freight_quotation_ingest/` | 1 (`1gi4Y...`, has the only `.clasp.json` checked in) |
| 12 other thematic folders       | 0 or 1 scriptId each |

**Three different folders sometimes reference the same scriptId** — e.g. `1BHAGZd_T1I5...` appears in both `tdg_scoring/` and `webhooks/`. So files of one GAS project are *split across thematic folders.* Editing files in either folder can change the same `/exec` deployment, but nothing in the repo says so.

### How scriptIds are encoded today

- 36 unique scriptIds appear in source-code header comments of the form:
  ```
   * Apps Script project:
   *   https://script.google.com/home/projects/<scriptId>/edit
  ```
- Only `seacoast_freight_quotation_ingest/.clasp.json` is checked in. Every other folder's `.clasp.json` is either nonexistent or gitignored.
- 51 `clasp_mirrors/<scriptId>/` folders exist (a superset of the 36 source-comment scriptIds — extras are likely deprecated or unmirrored projects).

### How `/exec` URLs are encoded today

- The `/exec` URLs (the deployment endpoints, distinct from scriptIds) appear scattered through comments in `.gs` files and references in `dapp/`, `docs/`, etc.
- They are **not** in any structured config in the repo.
- Pulled from the audit, 28 distinct `/exec` URLs are referenced across the 21 thematic folders. One `AKfycbygmwRbyqse...` URL appears in three different folders — it's the anonymous Edgar dispatch endpoint shared across modules.

### How cache-refresh hooks are encoded today

- Not at all in a structured way. The transcript that prompted this roadmap was Gary watching the autopilot rediscover `handleDaoMembersCacheRefreshRequest_` by reading the .gs source.
- A safe-by-default action ("after clasp push, hit every cache-refresh URL we know about") doesn't exist; current ops is "deploy and remember to also curl the refresh URL."

---

## 3. Decisions locked

| Decision | Value | Notes |
|---|---|---|
| Source-of-truth layout | **One subfolder = one GAS project** (one scriptId) under `google_app_scripts/` | Mirrors the `clasp_mirrors/<scriptId>/` 1:1, just with a human-readable folder name. |
| Discoverability | `manifest.json` at each project folder root | Same one-declarative-file pattern as the autopilot `TOOL_SPEC`. |
| Thematic discoverability (kept) | `google_app_scripts/INDEX.md` groups projects by domain | Old thematic folders disappear as folders; live on as headings in an index. |
| Sources stay under `google_app_scripts/` | `.gs` files remain the canonical, version-controlled artifact | `clasp_mirrors/` remains the gitignored deploy scratch. No move; only the thematic→project restructure. |
| Per-project deploy script | `google_app_scripts/<project>/deploy.sh` reads `manifest.json`, syncs to `clasp_mirrors/<scriptId>/`, `clasp push`, then hits each `post_push_hooks[].url` | Single command per project. Replaces "deploy and remember to curl the refresh URL." |
| Autopilot integration (later) | `gas_deploy_project(folder)` tool added to the capability manifest after PR-final lands | One Telegram message → one GAS project deployed + caches refreshed. Out of scope for this roadmap. |
| Shared helpers | Duplicated per project (GAS has no cross-project import); source-of-truth `_shared/` source + per-folder pre-push copy step | The honest GAS answer. Symlinks not used (Windows checkouts break). |

### `manifest.json` schema (v1)

```json
{
  "name": "TDG Credentialing — practice event processing",
  "scriptId": "1Dj3-m_ejxYJ4UQK2zNadnqNHJIvPQfj-VYvH9_Gnap6MYRmOJhK3B0VR",
  "owner_email": "admin@truesight.me",
  "deployments": {
    "head":               "https://script.google.com/macros/s/AKfyc.../exec",
    "anonymous_admin_v1": "https://script.google.com/macros/s/AKfycbzYmzg.../exec"
  },
  "post_push_hooks": [
    {
      "label": "refresh dao_members cache",
      "url":   "https://script.google.com/macros/s/AKfyc.../exec?action=refresh_dao_members_cache",
      "method": "POST",
      "body":  {"secret": "$DAO_MEMBERS_CACHE_SECRET"}
    }
  ],
  "consumer_callers": [
    "dapp/governor_permissions.html",
    "truesight_autopilot — via http_fetch + roles"
  ],
  "shared_helpers_from": ["../_shared/signature.gs"],
  "notes": "Anonymous-callable deployment (AKfycbz...) is the one autopilot should use for shell-driven backfill — see reference_credentialing_gas_deployments."
}
```

Every field except `name` + `scriptId` is optional. `post_push_hooks[].body` may reference `$ENV_VAR` placeholders that the deploy script resolves from `.env` at push time.

---

## 4. Pre-flight checklist (confirm before PR-1)

Operator-gated — Gary or a human must resolve these:

- [ ] **Source-of-truth for `/exec` URLs.** The audit captured 28 URLs from in-repo comments; some projects have multiple deployments (HEAD + versioned). For each scriptId, list every live deployment in the GAS web UI — this becomes the `deployments` map. Without it, the manifests are incomplete.
- [ ] **Cache-refresh hooks discovery.** For each scriptId, list every cache that goes stale on a clasp push (the `treasury-cache` files, `truesight.me/stats/*.json`, in-script `CacheService` blobs, etc.) and the URL/action that refreshes each. Some are pull-with-TTL (no hook needed); some require an explicit POST.
- [ ] **Owner-email per scriptId.** Most are presumably `admin@truesight.me`. Confirm the exceptions. `clasp push` runs under whichever account `clasp login` was last invoked as; the manifest documents the *intended* owner.
- [ ] **The 51 → 36 delta.** `clasp_mirrors/` has 51 folders but only 36 distinct scriptIds appear in source comments. Decide which of the extras are: (a) deprecated and removable, (b) live but unmirrored to a thematic folder, (c) orphan clones.
- [ ] **Shared `_shared/` directory.** Confirm the helpers (signature verification, common Sheet handles) that are duplicated across projects today. Pick the canonical copy per helper.
- [ ] **Restructure tolerance for `.gitignore`.** Confirm `clasp_mirrors/<scriptId>/Code.js` should stay gitignored under the new layout. (Yes by default — the source lives at `google_app_scripts/<project>/*.gs`.)

Decisions already locked (no action needed): manifest schema v1, one-folder-per-project layout, `deploy.sh`-per-project, autopilot tool deferred to a follow-up.

---

## 5. Execution roadmap — sequenced PRs

Each PR is independently mergeable; the resume tracker (§7) makes any stop point picked up by the next session.

| PR | Work | Touches | Shippable result |
|---|---|---|---|
| **PR-0** *(this file)* | Roadmap committed. Audit findings + schema + sequence. | `agentic_ai_context/` | Future sessions skip the discovery. |
| **PR-1** | **Manifest-only.** Add `manifest.json` to each existing thematic folder describing every scriptId it covers (one manifest per scriptId, named by scriptId or the project's intended folder name). **No file moves yet.** Audit-derived; humans + LLMs can already answer "which scriptId owns this file" by reading the manifest. | `tokenomics/google_app_scripts/<theme>/` | Discoverability win, zero deploy disruption. **Highest priority — gets most of the value with smallest risk.** |
| **PR-2…PR-N** | **Restructure, one thematic folder at a time.** Each PR splits one current thematic folder into one or more project subfolders, `git mv`-ing the `.gs` files into the right project folder, updating the manifest, updating any consumer references in `dapp/` / `truesight_autopilot/` / docs / READMEs. Land each independently so blast radius stays small. | `tokenomics/google_app_scripts/` + downstream consumers | Each project deploys as one self-contained unit. |
| **PR-final-1** | **`deploy.sh` per project.** Reads `manifest.json`, syncs sources to `clasp_mirrors/<scriptId>/`, `clasp push`, hits each `post_push_hooks[].url`. Replaces ad-hoc deploy instructions in READMEs. | All project folders | One command per project. |
| **PR-final-2** *(deferred, separate roadmap)* | **`gas_deploy_project(folder)` autopilot tool.** Wraps `deploy.sh` via the capability manifest pattern. | `truesight_autopilot/app/tools/` | Telegram message → GAS deploy + cache refresh, end-to-end. |

### Subfolder restructure plan (PR-2…PR-N)

Folders that already are 1:1 with one scriptId — minor work (rename if needed, add manifest):

- `agroverse_notarizations/`, `agroverse_site_statistics/`, `find_nearby_stores/`, `holistic_hit_list_store_history/`, `newsletter_subscriber_sync/`, `pipeline_metrics_snapshot/`, `seacoast_freight_quotation_ingest/`, `sunmint_tree_planting/`, `tdg_credentialing/`, `tdg_proposal/`, `tdg_shipping_planner/`, `wix_workflows/`

Folders covering multiple scriptIds — split into one project subfolder per scriptId:

- `agroverse_qr_codes/` → 3 children
- `tdg_asset_management/` → 3 children
- `tdg_identity_management/` → 3 children
- `tdg_inventory_management/` → 3 children
- `tdg_scoring/` → 3 children
- `webhooks/` → multiple, with potential merges back into `tdg_scoring/` / `tdg_asset_management/` once the actual ownership is documented

Folders to investigate before touching:

- `_clasp_default/` (only contains `Version.gs` — likely a shared-helper pattern)
- `asset_receipt_ingest/`, `deprecated/`

Total PR estimate: 1 audit + 1 manifest-convention PR + ~12-15 restructure PRs + 1 deploy.sh PR ≈ **15-17 PRs**.

---

## 6. Risks & foot-guns

1. **`clasp_mirrors/` is the deploy artifact, not the source.** Don't push from a clasp_mirror without first syncing from `google_app_scripts/<project>/`. The `deploy.sh` shape in §3 enforces that. A direct `cd clasp_mirrors/<scriptId> && clasp push` can ship un-versioned local edits.
2. **Apps Script global-scope.** Two projects can have functions named the same. Once each project folder is self-contained, file-level renames during the split must not introduce cross-project name collisions that the LLM (or a contributor) didn't anticipate.
3. **Cache-refresh order.** Some hooks must fire in a specific sequence (e.g. refresh the `dao_members` cache *before* the `treasury` cache that depends on it). PR-final-1's deploy.sh should respect `post_push_hooks[]` order rather than parallelising blindly.
4. **The 51 → 36 clasp_mirror delta.** Some mirrors may have no source under `google_app_scripts/` — they're orphans or copies of historical state. Don't auto-delete; mark as `orphan_mirror` in PR-1's audit-derived index and resolve case-by-case in PR-2…PR-N.
5. **Owner-email drift.** A clasp_mirror that was last pushed under a wrong Google account silently mismatches its manifest's `owner_email`. The pre-flight checklist makes this explicit; the deploy script should sanity-check `clasp login` identity vs `manifest.owner_email` before pushing.
6. **`/exec` URL leakage.** `/exec` URLs aren't secrets *per se* (anyone with the URL can call them) but they're not meant to be widely indexed either. The manifest stays in the repo (which is private), and the autopilot's reach over `http_fetch` is scope-restricted; the README mentions of URLs that are already public stay public.

---

## 7. Resume tracker

**RESUME HERE → PR-0 + PR-1 + PR-1b + PR-1c + PR-1d + PR-1e + PR-1f all merged. Audit state: 36 healthy / 13 orphans / 1 unmirrored.** PR-1f minted 2 of 3 missing mirrors (`1MnAsIQA…` and `1gi4YKh2…`) via `clasp clone` and `git rm`'d the redundant in-folder `.clasp.json` for seacoast. The third (`1zKgMwd6…`, Gmail digital-signature ingestion, admin@truesight.me) failed with `The caller does not have permission` — needs operator action (clasp login as admin@ or share the GAS project with the current account). Remaining: mint 1 missing mirror (`1zKgMwd6…`, operator-gated), resolve the 13 remaining orphan dispositions per `docs/gas_orphan_mirror_dispositions.md`, shared-helpers canonicalisation.

| Unit | PR | Merged | Deployed | Contribution reported |
|---|---|---|---|---|
| **PR-0** Roadmap (this file)        | [agentic_ai_context#232](https://github.com/TrueSightDAO/agentic_ai_context/pull/232) | ✅ | n/a | ✅ |
| **PR-1** manifest.json convention   | [tokenomics#317](https://github.com/TrueSightDAO/tokenomics/pull/317) | ✅ | ☐ (no GAS changes) | ✅ |
| **PR-1b** pre-flight audits (orphan mirrors / consumer_callers / `/exec` probe) | [tokenomics#318](https://github.com/TrueSightDAO/tokenomics/pull/318) | ✅ | ☐ (no GAS changes) | ✅ |
| **PR-1c** cache-refresh hook audit (mirror-grounded) | [tokenomics#319](https://github.com/TrueSightDAO/tokenomics/pull/319) | ✅ | ☐ (no GAS changes) | ✅ |
| **PR-1d** owner_email assignment (3 admin@, 40 gary@) | [tokenomics#320](https://github.com/TrueSightDAO/tokenomics/pull/320) | ✅ | ☐ (no GAS changes) | ✅ |
| **PR-1e** orphan cleanup — 4 deletes + 1 routing + dispositions doc | [tokenomics#321](https://github.com/TrueSightDAO/tokenomics/pull/321) | ✅ | ☐ (no GAS changes) | ✅ |
| **PR-1f** mint 2 of 3 missing mirrors via `clasp clone` | [tokenomics#322](https://github.com/TrueSightDAO/tokenomics/pull/322) | ✅ | ☐ (no GAS changes) | ☐ |
| **Operator pre-flight (§4) remaining** — mint 1 missing mirror (`1zKgMwd6…`, needs admin@ login or share), 13 remaining orphan dispositions (see `docs/gas_orphan_mirror_dispositions.md`), shared-helpers canonicalisation | n/a (operator) | ☐ | n/a | n/a |
| **PR-2** restructure folder 1       | tokenomics#TBD | ☐ | ☐ | ☐ |
| **PR-3** restructure folder 2       | tokenomics#TBD | ☐ | ☐ | ☐ |
| … one PR per thematic folder …      | tokenomics#TBD | ☐ | ☐ | ☐ |
| **PR-final-1** deploy.sh per project | tokenomics#TBD | ☐ | ☐ | ☐ |
| **PR-final-2** autopilot gas_deploy_project tool *(separate roadmap)* | truesight_autopilot#TBD | ☐ | ☐ | ☐ |

### Audit artifacts in tokenomics from PR-1b + PR-1c

- `docs/gas_orphan_mirror_audit.md` — 33 healthy / 18 orphans / **3 unmirrored** (real bug surface — `clasp push` would fail until mirrors are minted). [PR-1b]
- `docs/gas_exec_probe_audit.md` — flat table of every `/exec` URL probe result; all 18 returned HTTP 200. [PR-1b]
- `docs/gas_cache_refresh_hook_audit.md` — 6 scriptIds with cache-refresh patterns. 5 emit `notifyTreasuryCachePublisher_` (the GAS-side trigger); 1 dispatches on `'refresh_dao_members_cache'` (the receiver). All 3 consumer references are GAS-to-GAS (in tokenomics itself), not from the workspace HTTP callers — so PR-final-1's `deploy.sh` doesn't need to make the cache-refresh call itself. [PR-1c]
- `scripts/audit_orphan_clasp_mirrors.py` / `scripts/crawl_gas_consumers.py` / `scripts/probe_gas_exec_urls.py` / `scripts/crawl_gas_cache_refresh_hooks.py` — idempotent re-runners.
- `scripts/gen_gas_manifests.py` — now merges instead of overwrites; preserves `consumer_callers`, `probe_*` deployments, `candidate_cache_refresh_hooks` across regenerations.

### Grounding-source note

PR-1c switched the source-of-truth from `.gs` header-comment URLs in `google_app_scripts/<theme>/` to `clasp_mirrors/<scriptId>/Code.js` (the bundled JS clasp actually pushes). Per Gary's correction 2026-05-28: each mirror IS one GAS project; its `Code.js` is authoritative for what the project contains. The header-comment proxy missed real handlers (e.g. `dao_members_cache_publisher.gs` defines the cache-refresh dispatch without carrying the header URL).

A future improvement to `gen_gas_manifests.py` would re-ground its primary scriptId → file mapping on mirror Code.js too; PR-1c only applied the grounding to the new cache-refresh sweep.

Per `OPERATING_INSTRUCTIONS.md` §5 + the DAO contribution convention: after each PR merges, report the contribution before starting the next, and tick both boxes here.

---

## 8. Out of scope (deliberate)

- **Migrating GAS projects off Apps Script** — the `dao_protocol` extraction handles the Edgar-facing endpoints, but the contributor-edge GAS modules (Sheet-side automation) are deliberately staying on Apps Script for now. Same logic as the autopilot capability-manifest call: the spreadsheet edge is a feature, not a debt.
- **Re-architecting the `clasp_mirrors/` directory.** It's working as a derived-artifact convention; PR-1 + PR-2…PR-N strengthen the upstream rather than replace the downstream.
- **Auto-merging the autopilot `gas_deploy_project` tool with the existing dao_protocol shape.** Separate concern, separate roadmap when needed.
