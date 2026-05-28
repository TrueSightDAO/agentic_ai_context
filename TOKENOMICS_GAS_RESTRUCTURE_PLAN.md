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

**RESUME HERE → PR-0 (this file) committed; PR-1 in progress (manifest.json added to each existing thematic folder; no file moves yet).** PR-2…PR-N held until pre-flight checklist (§4) is resolved.

| Unit | PR | Merged | Deployed | Contribution reported |
|---|---|---|---|---|
| **PR-0** Roadmap (this file)        | agentic_ai_context#TBD | ☐ | n/a | ☐ |
| **PR-1** manifest.json convention   | tokenomics#TBD | ☐ | ☐ (no GAS changes) | ☐ |
| Pre-flight checklist resolved (§4)  | n/a (operator) | ☐ | n/a | n/a |
| **PR-2** restructure folder 1       | tokenomics#TBD | ☐ | ☐ | ☐ |
| **PR-3** restructure folder 2       | tokenomics#TBD | ☐ | ☐ | ☐ |
| … one PR per thematic folder …      | tokenomics#TBD | ☐ | ☐ | ☐ |
| **PR-final-1** deploy.sh per project | tokenomics#TBD | ☐ | ☐ | ☐ |
| **PR-final-2** autopilot gas_deploy_project tool *(separate roadmap)* | truesight_autopilot#TBD | ☐ | ☐ | ☐ |

Per `OPERATING_INSTRUCTIONS.md` §5 + the DAO contribution convention: after each PR merges, report the contribution before starting the next, and tick both boxes here.

---

## 8. Out of scope (deliberate)

- **Migrating GAS projects off Apps Script** — the `dao_protocol` extraction handles the Edgar-facing endpoints, but the contributor-edge GAS modules (Sheet-side automation) are deliberately staying on Apps Script for now. Same logic as the autopilot capability-manifest call: the spreadsheet edge is a feature, not a debt.
- **Re-architecting the `clasp_mirrors/` directory.** It's working as a derived-artifact convention; PR-1 + PR-2…PR-N strengthen the upstream rather than replace the downstream.
- **Auto-merging the autopilot `gas_deploy_project` tool with the existing dao_protocol shape.** Separate concern, separate roadmap when needed.
