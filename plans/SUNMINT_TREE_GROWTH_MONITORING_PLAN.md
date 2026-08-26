# SunMint Tree-Growth Monitoring — Plan

**Status: active — P1a build in progress · Created 2026-08-26 by Sophia Truesight (autopilot) for Gary Teh · Owner: Gary Teh**
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

## 2. Storage — TrueSightDAO/sunmint images/growth/

**Decision (Envoy research, confirmed by Gary 2026-08-26):** reuse the existing blob/asset store.

- **Repo:** `TrueSightDAO/sunmint` — already in `truesight_autopilot/app/config.py` `api_only_repos` as *"blob / asset stores (Contents-API uploads)"* (PAT/Contents-API upload only; never git clone/push). Already used for tree-planting photos (`images/` folder; "GitHub Commit URL" column O in the SunMint Tree Planting sheet).
- **Location:** `images/growth/<submission_id>/01_closeup.jpg` + `02_context.jpg` (subfolder `growth/` so the workflow trigger doesn't fire on ordinary planting photos).
- **Upload path:** farmer browser POSTs signed multipart → Edgar; GAS handler mirrors photos server-side via Contents-API PUT (no PAT on farmer phones).
- **Analysis trigger:** one GitHub Action in `sunmint`, `on: push`, `paths: [images/growth/**]`, `permissions: contents: write` — fires PM002/OpenCV analysis the moment photos land (Contents-API PUTs are real commits → real push events) and commits `images/growth/<submission_id>/analysis.json` back (run log + result commit = public audit trail).
- **Constraint:** Contents API hard cap **25 MB/file** (`_MAX_UPLOAD_BYTES` in `upload_file_to_github.py`). Photos fit comfortably; if ever needed, Git Data API (~100 MB blobs) is a P4+ option.

## 3. Event taxonomy (FINAL — Gary 2026-08-26)

| Event | Cadence | Signed by | Ledger impact | Gate |
|---|---|---|---|---|
| **[TREE GROWTH MONITORING EVENT]** | × N, one per measurement | Farmer — RSA-2048, client-side → Edgar → GAS handler | **NONE** — attribution/audit trail only (tracking tab + per-tree JSON history = monitoring report) | Farmer (own key) |
| **[CARBON CREDIT ISSUANCE EVENT]** (name TBD) | Periodic — aggregates a batch of VVB-verified measurements | Governor-level signer | **The ONLY ledger-booking event** — books the DAO ledger/asset entry at issuance | Governor (mirror [CAPITAL INJECTION EVENT] / `isGovernorByName_` pattern) |

**Rules (Gary clarifications):**
1. **Every measurement = one signed `[TREE GROWTH MONITORING EVENT]`, always.** Client RSA-2048 → Edgar → dispatched → logged to Telegram Chat Logs → written to tracking tab + per-tree JSON history. Unconditional — the base attribution mechanism.
2. **Not every signed event = a ledger entry.** Decision 3 (2026-08-26, researched against Verra / Gold Standard / ACR / 2026 dMRV pilots): monitoring data accumulates as evidence over a crediting period; issuance is a **distinct, periodically-verified event** that mints credits with serial numbers — never a transaction per individual measurement. So: tracking tab + per-tree JSON history = the monitoring report; a real ledger entry happens **only** at issuance.
3. **Issuance is OUT OF SCOPE for P1a** — noted now so nothing needs retrofitting later.

## 4. Backend-in-P1a-scope decision

**Decision (Gary, 2026-08-26): the signed-event backend leg is IN P1a scope — NOT deferred to P4.** Mirrors the `[TREE PLANTING LINK EVENT]` precedent (purpose-built event, signed, dispatched via dao_protocol, GAS-processed, logged to Telegram Chat Logs for attribution, dedup tracking tab):

- **dao_protocol:** register `[TREE GROWTH MONITORING EVENT]` — events_catalog.json entry + dispatch.py ROUTING row (`TREE_GROWTH_MONITORING` → `processTreeGrowthMonitoringFromTelegramChatLogs`) — **PR #146 (open)**
- **GAS handler:** `process_tree_growth_monitoring.gs` (tokenomics, shared agroverse_qr_codes project `1UrBgq…`) — validate sig → mirror photos → read analysis.json → append tracking-tab row (dedup) → per-tree JSON history → Telegram Chat Logs — **PR #430 (open)**
- **Client pages:** `monitor_tree_growth.html` (dapp_beta, PR #81 merged) + `sunmint/monitor-tree-growth/index.html` (truesight_me_beta, PR #312 merged)

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

Per-tree JSON history additionally written to `sunmint/trees/<tree_id>.json` (measurements append via the analysis worker). GeoJSON index (`sunmint/trees/index.geojson` + farm shards) powers the nearest-tree dropdown — no database, static files, derived cache from sheet + on-chain events (P3).

## 6. Build sequencing (Gary correction 2026-08-26 — NO parallel runs)

1. **P1a — dapp_beta `monitor_tree_growth.html`** — finish FULLY first → ✅ merged (PR #80 → #81 photo-first)
2. **P1b — truesight_me_beta `sunmint/monitor-tree-growth/index.html`** (sunmint.truesight.me-facing) → ✅ merged (PR #312)
3. **P1c — dao_protocol registration** → ✅ PR #146 (open)
4. **P1d — GAS handler** (tokenomics) → ✅ PR #430 (open)
5. **P2 — Python worker MVP (single-image)** + **sunmint repo GitHub Action** (`paths: [images/growth/**]`)
6. **P3 — GeoJSON index build script**
7. **P4 — UAT on both beta sites**
8. **Mobile-app work** (AFTER P1a/P1b) — `plans/SUNMINT_MOBILE_APP_PLAN.md` — Capacitor native wrapper; **monitor module is NOT in that plan's scope** (separate extension unit if wanted, reusing P2 worker + P3 index)

**RESUME HERE → next unit: merge P1c (#146) + P1d (#430) → deploy GAS handler (clasp push + TGM_GITHUB_TOKEN Script Property) → P2 (sunmint workflow + worker).**

## 7. Checklist

- [x] Spec v1.4 signed off (photo pair, event taxonomy, decisions 1–3)
- [x] P1a dapp_beta monitor_tree_growth.html (photo-first) — PR #81 merged
- [x] P1b truesight_me_beta sunmint/monitor-tree-growth — PR #312 merged
- [x] P1c dao_protocol registration — PR #146
- [x] P1d GAS handler process_tree_growth_monitoring.gs — PR #430
- [ ] Deploy GAS handler (clasp push + TGM_GITHUB_TOKEN)
- [ ] sunmint repo pm002_analysis workflow (P2)
- [ ] P2 worker single-image update (amend truesight_autopilot #314)
- [ ] GeoJSON index build script (P3)
- [ ] UAT both beta sites (P4)
- [ ] Future: [CARBON CREDIT ISSUANCE EVENT] + issuance phase (out of scope)

## 8. Risks

- Card detection failure on low-quality photos → manual DBH entry fallback
- Cacao allometric equations need field calibration (v1 seeds; plan calibration plots)
- GeoJSON staleness → TTL + rebuild cron
- VVB acceptance of phone-photo DBH → TREEO/Plan Vivo precedent + context photo for identity
