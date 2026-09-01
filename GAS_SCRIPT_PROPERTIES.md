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
4. **How to set a property:** GAS script editor → Project Settings (gear) → **Script properties** → Add script property.
   Project settings URL pattern: `https://script.google.com/home/projects/<SCRIPT_ID>/settings`.
5. **Where the local `.env` / vault lives:** autopilot box `/opt/truesight_autopilot/.env` (`TRUESIGHT_DAO_AUTOPILOT`
   PAT is the org/repo-scoped PAT used for `repository_dispatch` and workflow_dispatch; identity keys are
   `EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY`). Canonical Sophia key copy: `/tmp/sophia_keys_clean.env`.

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

> **TGM_GITHUB_TOKEN is SET (2026-08-31).** This closes the last manual step in the SunMint invalidation loop:
> reject → INVALID → dispatch → auto rebuild → tree gone, fully automatic. If a future dispatch still fails,
> check the token **scope** (needs `repo` / Actions:write for `repository_dispatch`), not its existence.

---

## 3. Deployment / webhook URL registry

| Purpose | Deployment URL (suffix) | Version | Runs code incl. | Notes |
|---|---|---|---|---|
| SunMint planting webhook (`processTreePlantingTelegramLogs`) | `AKfycbyLQjTlM8nzAP…/exec` | @7 | planting handler | fired by dao_protocol `TREE_PLANTING_PROCESSING` env; also `/a/macros/agroverse.shop/`-prefixed twin |
| Tree-planting-links webhook (`processTreePlantingLinksFromTelegramChatLogs`) — LINK + REJECT | `AKfycbyoFCTzIdC1g69ZX3AK894h2siQOKoNSEiuyLDtZJTtarQPHHa5Zl8rjot0vPFUquV2/exec` | **@37** | #449 (col A OR col D reject match) + #450 (rebuild dispatch) | anonymous; pinned version — do NOT run pre-#449 logic on it |
| Growth-monitoring webhook (`processTreeGrowthMonitoringFromTelegramChatLogs`) | `…/exec?action=…` (@HEAD) | @HEAD | #430 | login-walled at @HEAD; timer-driven path is primary |

**dao_protocol box env keys** (provisioned in `/home/ubuntu/dao_protocol/.env`):
- `DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_REJECT` → the `AKfycbyoFCTz…/exec` URL above (SET, loaded in process 2026-08-31)
- `DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_PROCESSING` → the planting `AKfycbyLQjTl…/exec` URL (SET)
- `DAO_PROTOCOL_WEBHOOK_TREE_GROWTH_MONITORING` → growth URL (verify when growth UAT starts)

**Routing entries (dao_protocol `dispatch.py` ROUTING):** `[TREE PLANTING EVENT]` (#149), `[TREE PLANTING REJECT EVENT]` (#150),
`[TREE PLANTING LINK EVENT]`, `[TREE GROWTH MONITORING EVENT]` — all dispatch to the GAS webhooks above.

---

## 4. How to update this file

- **New property set** → add/edit a row with `SET` + date + who verified. No need to re-verify old `SET` entries.
- **New GAS project** → add its script-id prefix + property rows.
- Append a one-line entry to `CONTEXT_UPDATES.md` (`YYYY-MM-DD | <agent> | …`) when you change this file.
- This file lives in `agentic_ai_context` — edit via PR (agents) or direct commit (governors).
