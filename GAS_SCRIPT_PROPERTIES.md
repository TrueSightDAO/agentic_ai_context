# GAS Script Properties — Registry & Convention

**Canonical reference for every Google Apps Script project's Script Properties and web-app deployment URLs.**
The point of this file: **never re-check whether a property is set.** Each entry has a `Status` column;
if it says `SET`, it is set — move on. If `NOT SET`, that's an open item (file it in OPEN_FOLLOWUPS.md if it blocks work).

> Created 2026-08-31 (Sophia). Convention + registry per Gary's direction: "whatever convention we adopt for
> this we should do the same for other GAS scripts."

---

## 1. Convention (the rules)

1. **Secrets/credentials for GAS projects live in Script Properties** — never in committed source.
   `PropertiesService.getScriptProperties().getProperty('KEY')` reads them at execution time
   (a deploy that pins a version still sees Script Properties changes — no re-deploy needed for value updates).
2. **A property whose value is set in Script Properties is `SET` here — do not re-verify.**
   If you suspect it changed, check the GAS project's Script Properties directly (URLs below) rather than guessing.
3. **Web-app deployment URLs are pinned to numbered versions** (e.g. `@37`), not `@HEAD` — `@HEAD` is login-walled
   even with `ANYONE_ANONYMOUS`. After clasp-pushing code, create a new version + deployment and update the env/URL
   that references it (see the SunMint reject saga 2026-08-30: anonymous webhook ran stale v32 while HEAD had the fix).
   **Bitten a 2nd time 2026-09-10 (thread 24269):** the reject webhook was pinned at `@41`; `clasp push` updated
   `@HEAD` only, so the reject silently ran the OLD first-match code. The repoint is ONLY done when
   `deploy_gas_project.py` is given `--deployment-id <id>` — without it the repoint is **silently skipped** (see
   OPEN_FOLLOWUPS.md "silently skips the pinned-deployment repoint"). Always pass `--deployment-id`; a reject is
   one-shot per submitted event, so a consumed-by-stale-code reject needs a **fresh** event to re-fire.
4. **How to set a property:** GAS script editor → Project Settings (gear) → **Script properties** → Add script property.
   Project settings URL pattern: `https://script.google.com/home/projects/<SCRIPT_ID>/settings`.
5. **Where the local `.env` / vault lives:** autopilot box `/opt/truesight_autopilot/.env` (`TRUESIGHT_DAO_AUTOPILOT`
   PAT is the org/repo-scoped PAT used for `repository_dispatch` and workflow_dispatch; identity keys are
   `EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY`). Canonical Sophia key copy: `/tmp/sophia_keys_clean.env`.

6. **The secret accessor (`Credentials.js`) is TRACKED and PUSHED — never `.claspignore`d or gitignored.**
   `clasp push` = `projects.updateContent` = **REPLACES** the project's remote file set: any file *not* in the
   pushed set is **DELETED** live. So `.claspignore`-ing `Credentials.js` is exactly what *caused* a push to
   delete the live accessor — incidents **2026-08-21** and **2026-09-06** (`ReferenceError: setApiKeys is not
   defined` on `@HEAD`, project `19Wag9x…`), and `1BHAGZd_…` had no accessor on `@HEAD` at all.
   **Rule (Gary, 2026-09-18):** keep a **secret-free** `Credentials.js` whose `setApiKeys()` is a no-op and whose
   `getCredentials()` reads Script Properties; **track it** (add a `.gitignore` negation) and **push it** like any
   other source. Model: `google_app_scripts/1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/Credentials.js`.
   A `Credentials.js` that still holds real secrets must have them moved to Script Properties **first**, then the
   file is sanitised to the pointer form and tracked. Do NOT add `Credentials.js` to `.claspignore`.

---

## 2. Registry — known Script Properties

| GAS Project (script id prefix) | Property | Purpose | Status | Notes / last verified |
|---|---|---|---|---|
| `1UrBg…` (agroverse_qr_codes — tree planting / QR / growth) | **`TGM_GITHUB_TOKEN`** | GitHub token for `repository_dispatch` (`tree-index-rebuild`) + photo mirroring | **SET (2026-08-31)** | repo-scoped PAT (the `.env` `TRUESIGHT_DAO_AUTOPILOT` one works — proven HTTP 204). Set by Gary. Do NOT re-check. |
| `1UrBg…` (agroverse_qr_codes — same project) | **`FBE_GH_PAT`** | GitHub PAT for `repository_dispatch` (`plots-index-rebuild`) from the FBE handler | **SET (2026-09-01)** | repo-scoped PAT; needs **Actions: write** on `TrueSightDAO/sunmint` (same pattern as TGM_GITHUB_TOKEN). Set by Gary at script settings. Do NOT re-check. |
| `1UrBg…` | `GOOGLE_SERVICE_ACCOUNT_JSON` (via Credentials.js seeding) | sheet/service-account access | SET | seeding-only Credentials.js; actual secrets in Script Properties (2026-08-21 audit) |
| Shipping Planner (EasyPost) | `ORIGIN_ADDRESS_*` | Kirsten's SF origin for restock shipping | SET | verified in BOTTLENECK_REVIEW_RESTOCK_RECOMMENDER.md |
| Shipping Planner (EasyPost) | `EASYPOST_API_KEY` | EasyPost credentials | SET | idem |
| Etsy order-monitoring GAS | `ETSY_KEYSTRING`, `ETSY_SHARED_SECRET` | Etsy OAuth | SET | OPEN_FOLLOWUPS.md 2026-07-02 (app approval still pending) |
| Etsy order-monitoring GAS | `ETSY_SHOP_ID` | shop id | NOT SET | OPEN_FOLLOWUPS.md — Gary to add |
| PARTNER_POKE_SCHEDULER | `ANTHROPIC_API_KEY`, `GROK_API_KEY` | AI pokes | SET | PARTNER_POKE_SCHEDULER_v0.md |
| inventory publish GAS | `AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT` | inventory snapshot publish | SET | EDGAR_DAO_EXTRACTION_PLAN.md (no `…_PUBLISH_SECRET`) |
| Wix-token GAS (deprecated) | Wix tokens | wix integration | N/A (deprecated) | NOTES_tokenomics.md — never commit secrets; Script Properties only |
| TrueChain GAS | RPC URL | "View on TrueChain" | SET | TRUECHAIN.md — RPC URL kept private |
| `1MnAsIQA…` (QR web service + telegram-log processors) | **`CFR_PROGRAM_SPREADSHEET_ID`** | private `cfr program` sheet id for the payout sinks (§11.8 step 3) | **NOT SET** | Sheet provisioned 2026-09-17 (`17KwmxYOpTVR89ybRlOkDXoN9PF3UcaNu3REg2wNa83w`, "20260917 - CFR ANAPU PROGRAM"). Set via GAS editor UI → Project Settings. **Blocks Tier-2 CFR writes only; Tier‑1 `payouts` writes are unaffected.** Verified unset 2026-09-18 (registration sink returns the SS11.8 not-set error). |

> **TGM_GITHUB_TOKEN is SET (2026-08-31).** This closes the last manual step in the SunMint invalidation loop:
> reject → INVALID → dispatch → auto rebuild → tree gone, fully automatic. If a future dispatch still fails,
> check the token **scope** (needs `repo` / Actions:write for `repository_dispatch`), not its existence.

---

## 3. Deployment / webhook URL registry

| Purpose | Deployment URL (suffix) | Version | Runs code incl. | Notes |
|---|---|---|---|---|
| SunMint planting webhook (`processTreePlantingTelegramLogs`) | `AKfycbyLQjTlM8nzAP…/exec` | **@8** (was @7) | planting handler + ingestion evidence gate (#464) | fired by dao_protocol `TREE_PLANTING_PROCESSING` env; also `/a/macros/agroverse.shop/`-prefixed twin. Repointed 2026-09-10. |
| Tree-planting-links webhook (`processTreePlantingLinksFromTelegramChatLogs`) — LINK + REJECT | `AKfycbyoFCTzIdC1g69ZX3AK894h2siQOKoNSEiuyLDtZJTtarQPHHa5Zl8rjot0vPFUquV2/exec` | **@44** (was @41/@37) | #449 (col A OR col D reject match) + #450 (rebuild dispatch) + #463 (reject invalidates ALL rows sharing tree id) | anonymous; pinned version — do NOT run pre-#449 logic on it. Repointed @41→@44 on 2026-09-10 (thread 24269). |
| Growth-monitoring webhook (`processTreeGrowthMonitoringFromTelegramChatLogs`) | `…/exec?action=…` (@HEAD) | @HEAD | #430 | login-walled at @HEAD; timer-driven path is primary |
| **Payout processing webhook** (`processPayoutEventsFromTelegramChatLogs`, `processPayoutRegistrationsFromTelegramChatLogs`) | `AKfycbxQDdGnwS7G6iJhNj9japW-9sFA7EUvrnznmJCu44S5ZHqOoIks2be4FXbIVpuaOHVW/exec` | **@32** (2026-09-18; was @30 — #518 added the `script.scriptapp` scope) | §12.7 Q3b payout-event sink (#504 + #513 trigger fix) + §11.8 payout-registration sink + both router branches | anonymous (ANYONE_ANONYMOUS); smoke 2026-09-18: `?action=getPayoutEvents` → `{"status":"success","data":{"count":0,"items":[]}}`, `?action=processPayoutEventsFromTelegramChatLogs` → `{"success":true,"recorded":0,...}`. **Created because @HEAD is login-walled** — do not point an anonymous webhook at @HEAD. **Live trigger status 2026-09-18 (Sophia):** the hourly safety-net trigger is **NOT installed** — the deploying user (`admin@truesight.me`) has not granted `script.scriptapp`, which deployment **@32** newly requires. Every `ScriptApp` call therefore fails with `You do not have permission to call ScriptApp.getProjectTriggers`, so the sink is **inert** and the Tier-2 `payout events` tab has **no writer**. Fix = open the project as the owner, run `processPayoutEventsFromTelegramChatLogs` once, click **Allow** (then set the `CFR_PROGRAM_SPREADSHEET_ID` Script Property). |

**dao_protocol box env keys** (provisioned in `/home/ubuntu/dao_protocol/.env`):
- `DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_REJECT` → the `AKfycbyoFCTz…/exec` URL above (SET, loaded in process 2026-08-31)
- `DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_PROCESSING` → the planting `AKfycbyLQjTl…/exec` URL (SET)
- `DAO_PROTOCOL_WEBHOOK_TREE_GROWTH_MONITORING` → growth URL (verify when growth UAT starts)
- `DAO_PROTOCOL_WEBHOOK_PAYOUT_PROCESSING` → the payout `AKfycbxQDdGnw…/exec` URL (@30) — **NOT SET** as of 2026-09-18; the GAS hourly cron (installed by the sink, #513) is the operative path until wired. Verified: `dao_protocol:/home/ubuntu/dao_protocol/.env` has no `…_PAYOUT_*` key.
- `DAO_PROTOCOL_WEBHOOK_CFR_PROGRAM_REGISTRATION_PROCESSING` → the CFR program-submission `AKfycbxQDdGnw…/exec` URL (same deployment as `…_PAYOUT_PROCESSING`) — **NOT SET** as of 2026-09-24. Wired in `dispatch.py` (dao_protocol #179) as a **2nd** target on the tree/monitoring/boundary routes (additive — the SunMint targets are untouched). Missing key → logged + skipped (SunMint unaffected); the CFR sink stays inert until this is set **and** Edgar restarts. See OPEN_FOLLOWUPS.md 2026-09-24.

**Routing entries (dao_protocol `dispatch.py` ROUTING):** `[TREE PLANTING EVENT]` (#149), `[TREE PLANTING REJECT EVENT]` (#150),
`[TREE PLANTING LINK EVENT]`, `[TREE GROWTH MONITORING EVENT]` — all dispatch to the GAS webhooks above.

**CFR mirror (additive, dao_protocol #179, 2026-09-24):** `[TREE PLANTING EVENT]`, `[TREE GROWTH MONITORING EVENT]`
and `[FARM BOUNDARY EVIDENCE EVENT]` each carry a **second** target `("CFR_PROGRAM_REGISTRATION_PROCESSING",
"processCfrProgramSubmissionsFromTelegramChatLogs")` (§11.5). ADDITIVE ONLY — `dispatch_event` fires every target
of a matched entry, so the SunMint targets above must never be replaced (else the public `SunMint Tree Planting`
tab goes dark). Guarded by `tests/test_cfr_program_dispatch_routing.py`.

---

## 4. How to update this file

- **New property set** → add/edit a row with `SET` + date + who verified. No need to re-verify old `SET` entries.
- **New GAS project** → add its script-id prefix + property rows.
- Append a one-line entry to `CONTEXT_UPDATES.md` (`YYYY-MM-DD | <agent> | …`) when you change this file.
- This file lives in `agentic_ai_context` — edit via PR (agents) or direct commit (governors).
