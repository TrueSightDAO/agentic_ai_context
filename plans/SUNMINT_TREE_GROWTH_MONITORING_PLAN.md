# SunMint Tree-Growth Monitoring — Plan

**Status: active — UAT pending · Updated 2026-08-26 (corrected hosting) · Owner: Gary Teh**
**Canonical spec:** `truesight_me_beta/sunmint/reports/sunmint_monitor_tree_growth_spec_v1.pdf` (v1.4) · working copy: `monitor_tree_growth_spec.md` (v1.4)
**Companion plan:** `plans/SUNMINT_MOBILE_APP_PLAN.md` (native mobile wrapper — separate unit, see §6)

---

## 1. Why (and the photo-not-video decision)

The SunMint model requires per-tree growth evidence a VVB can audit. Phone-camera measurement is the proven pattern (TREEO 94–95% DBH accuracy R²≥0.95; ACORN/Agerpoint moving ground-truth to phone; Greenstand photo-verified; CommuniTree/Taking Root on Plan Vivo).

**Decision (Gary, 2026-08-26): capture is a STILL PHOTO PAIR, not video** — matching TREEO (certified dMRV tool, Global Tree C-Sink standard): a **close-up** of the calibration/reference card (ISO-7810) against the trunk at breast height (the measurement evidence → DBH → allometric → biomass → CO₂e) plus a **wider context shot** (tree identity + species verification). Two photos per submission; schema is plural-aware (supports N photos).

**Why photo beats video here:**
- 25 MB GitHub Contents-API cap is comfortably clear (photo ~2–8 MB; no duration/bitrate capping logic needed)
- Simpler, faster, deterministic analysis (single-image OpenCV, no frame extraction)
- Matches the certified-dMRV precedent (TREEO) and how verification apps use multiple angles

## 2. Storage — TrueSightDAO/sunmint images/growth/ + canonical index

**Decision (Envoy research, confirmed by Gary 2026-08-26):** reuse the existing blob/asset store.

- **Repo:** `TrueSightDAO/sunmint` — in `truesight_autopilot/app/config.py` `api_only_repos` as *"blob / asset stores (Contents-API uploads)"*. Already used for tree-planting photos (`images/` folder; "GitHub Commit URL" column O in the SunMint Tree Planting sheet).
- **Photos:** `images/growth/<submission_id>/01_closeup.jpg` + `02_context.jpg` (subfolder `growth/` so the workflow trigger doesn't fire on planting photos). Upload: farmer browser POSTs signed multipart → Edgar; GAS handler mirrors server-side via Contents-API PUT (no PAT on farmer phones).
- **Canonical tree index (P3, DONE):** `trees/index.geojson` in the `sunmint` data repo (treasury-cache pattern — data + generator + workflow together):
  - `trees/index.geojson` — 18 real trees, 13 with coordinates, 5 in the no-GPS bucket (`geometry: null`, incl. FounderHaus `FOUNDERHAUS_BOUGAINVILLEA_20260821_1`)
  - `scripts/build_tree_geojson.py` — generator (reads the `SunMint Tree Planting` sheet via `GOOGLE_SERVICE_ACCOUNT_JSON`, emits index)
  - `.github/workflows/rebuild-tree-index.yml` — daily 06:00 cron + `repository_dispatch` + manual; commits back as Sophia Truesight
  - Secrets set: `GOOGLE_SERVICE_ACCOUNT_JSON` + `GH_PAT_TOKEN`; workflow tested end-to-end (run 33007358090 success, auto-commit "Update tree index")
- **Analysis trigger (P2):** one GitHub Action in `sunmint`, `on: push`, `paths: [images/growth/**]`, `permissions: contents: write` — fires PM002/OpenCV analysis when photos land, commits `images/growth/<submission_id>/analysis.json` back (run log + result commit = public audit trail).
- **Constraint:** Contents API hard cap **25 MB/file**; photos fit comfortably (Git Data API ~100 MB is a P4+ option if ever needed).

## 3. Event taxonomy (FINAL — Gary 2026-08-26)

| Event | Cadence | Signed by | Ledger impact | Gate |
|---|---|---|---|---|
| **[TREE GROWTH MONITORING EVENT]** | × N, one per measurement | Farmer — RSA-2048, client-side → Edgar → GAS handler | **NONE** — attribution/audit trail only (tracking tab + per-tree JSON history = monitoring report) | Farmer (own key) |
| **[CARBON CREDIT ISSUANCE EVENT]** (name TBD) | Periodic — aggregates a batch of VVB-verified measurements | Governor-level signer | **The ONLY ledger-booking event** — books the DAO ledger/asset entry at issuance | Governor (mirror [CAPITAL INJECTION EVENT] / `isGovernorByName_` pattern) |

**Rules (Gary clarifications):**
1. **Every measurement = one signed `[TREE GROWTH MONITORING EVENT]`, always.** Client RSA-2048 → Edgar → dispatched → logged to Telegram Chat Logs → written to tracking tab + per-tree JSON history. Unconditional — the base attribution mechanism.
2. **Not every signed event = a ledger entry.** Decision 3 (2026-08-26, Verra / Gold Standard / ACR / 2026 dMRV pilots): monitoring data accumulates as evidence over a crediting period; issuance is a **distinct, periodically-verified event** that mints credits with serial numbers — never a transaction per individual measurement.
3. **Issuance is OUT OF SCOPE for P1a** — noted now so nothing needs retrofitting later.

## 4. Backend-in-P1a-scope decision (DONE)

**Decision (Gary, 2026-08-26): the signed-event backend leg is IN P1a scope — NOT deferred to P4.** Mirrors the `[TREE PLANTING LINK EVENT]` precedent.

- **dao_protocol:** `[TREE GROWTH MONITORING EVENT]` — events_catalog.json entry + dispatch.py ROUTING row (`TREE_GROWTH_MONITORING` → `processTreeGrowthMonitoringFromTelegramChatLogs`) — **PR #146 MERGED**
- **GAS handler:** `process_tree_growth_monitoring.gs` (tokenomics, shared agroverse_qr_codes project `1UrBgq…`) — validate sig → mirror photos → read analysis.json → append tracking-tab row (dedup) → per-tree JSON history → Telegram Chat Logs — **PR #430 MERGED, clasp-pushed to version 33 (live via @HEAD webhook)**; `TGM_GITHUB_TOKEN` Script Property still to set

## 5. Tree Growth Measurements tracking-tab schema

New tab on the SunMint spreadsheet (SOURCE_SHEET_URL spreadsheet), one row per measurement:

| Col | Field |
|---|---|
| A | Telegram Update ID |
| B | Telegram Message ID (dedup key) |
| C | Tree ID (QR Code) |
| D | Species |
| E | DBH (cm) |
| F | AGB (kg) |
| G | CO2e (kg) |
| H | Latitude |
| I | Longitude |
| J | Measured At |
| K | Close-up Photo URL |
| L | Context Photo URL |
| M | Analysis Commit URL |
| N | Analysis SHA-256 |
| O | Farmer Signature |
| P | Contributor Name |
| Q | Status |
| R | Processed Timestamp |

Per-tree JSON history additionally written to `sunmint/trees/<tree_id>.json` (measurements append via the analysis worker). GeoJSON index (`sunmint/trees/index.geojson`) powers the nearest-tree dropdown — no database, static files, derived cache from sheet + on-chain events.

## 6. Build sequencing (CORRECTED 2026-08-26 — hosting fix + status)

**⚠️ CRITICAL CORRECTION:** `sunmint.truesight.me` is served by **`sunmint_prod`** (staging `sunmint_beta` → beta.sunmint.truesight.me) — a COMPLETELY SEPARATE repo from `truesight_me_beta` (which serves beta.truesight.me). Monitor Tree lives as a **sibling page inside `sunmint_beta`/`sunmint_prod`** alongside the simplified Plant Tree page (`sunmint_beta/index.html` root). Product intent: SunMint is the simplified field-agent/farmer experience — NEVER link out to the full dApp (dapp.truesight.me shows voting rights/cash-out/the full event dropdown — the complexity SunMint exists to avoid).

1. **P1a — dapp_beta `monitor_tree_growth.html`** — ✅ PR #80 → #81 (photo-first) merged
2. **P1b — ORIGINAL truesight_me_beta `sunmint/monitor-tree-growth/`** — ❌ **MIS-SCOPED — REVERTED** (truesight_me_beta#313, merged; wrong domain, dead code removed)
3. **P1b′ — CORRECTED: `sunmint_beta/monitor-tree-growth/index.html`** — ✅ PR #9 merged (+ #10 nav dropdown, #11 logo/lang-toggle/APK CTA, #12 GeoJSON index + sort fix, #13 canonical-index fetch, #14 tree detail panel; **#15 layout fix OPEN**)
4. **P1c — dao_protocol registration** — ✅ PR #146 merged
5. **P1d — GAS handler** (tokenomics) — ✅ PR #430 merged + deployed (v33)
6. **P2 — analysis worker + sunmint workflow** — `tree_growth_analysis.py` merged (truesight_autopilot#314); photo-mirror/analysis workflow scaffolded in `sunmint` repo
7. **P3 — GeoJSON index build script** — ✅ DONE (treasury-cache pattern; secrets set; tested)
8. **P4 — UAT on beta.sunmint.truesight.me** — NEXT
9. **Mobile-app work** — `plans/SUNMINT_MOBILE_APP_PLAN.md` (Capacitor native wrapper; monitor module NOT in that plan's scope — separate extension unit if wanted, reusing P2 worker + P3 index)

**RESUME HERE → next unit: merge sunmint_beta#15 (layout fix) → FounderHaus coords backfill (needs SA Editor grant on tree sheet; geocoded HQ -27.4389516, -48.4997079 matches Aug-19 pair) → UAT on beta.sunmint.truesight.me → promote via `sync_beta_to_prod(sunmint_prod)` (tool now supports sunmint via truesight_autopilot#316).**

## 7. Checklist

- [x] Spec v1.4 signed off (photo pair, event taxonomy, decisions 1–3)
- [x] P1a dapp_beta monitor_tree_growth.html (photo-first) — PR #81 merged
- [x] P1b′ sunmint_beta monitor-tree-growth (corrected hosting) — PRs #9–#14 merged (#15 open)
- [x] P1c dao_protocol registration — PR #146 merged
- [x] P1d GAS handler — PR #430 merged + deployed (v33)
- [x] P3 GeoJSON index (sunmint repo, treasury-cache pattern) — secrets set, workflow tested
- [ ] TGM_GITHUB_TOKEN Script Property on GAS project
- [ ] FounderHaus coords backfill (needs SA Editor grant on sheet)
- [ ] UAT on beta.sunmint.truesight.me (P4)
- [ ] Promote to sunmint_prod (sync_beta_to_prod)
- [ ] Future: [CARBON CREDIT ISSUANCE EVENT] + issuance phase (out of scope)

## 8. Risks

- Card detection failure on low-quality photos → manual DBH entry fallback
- Cacao allometric equations need field calibration (v1 seeds from literature)
- FounderHaus + 4 other trees lack GPS coords → no-GPS bucket in dropdown until backfilled
- SA `cypher-defense` is read-only on the tree sheet → coords backfill + tracking-tab writes need Editor grant
- GitHub Pages rebuild lag after merges (verify with cache-busted fetch)