# SunMint Monitor Tree Growth — Plan

**Status: active — P1a build in progress · Created 2026-08-26 by Sophia Truesight (autopilot) for Gary Teh**
**Canonical spec:** `truesight_me_beta/sunmint/reports/sunmint_monitor_tree_growth_spec_v1.pdf` (v1.4) + working copy `monitor_tree_growth_spec.md`

## 1. Why

Per-tree growth evidence a VVB can audit. Phone-camera measurement is proven (TREEO 94–95% DBH accuracy R²≥0.95; ACORN/Agerpoint; Greenstand). Capture = **still photo pair** (TREEO-style): close-up of calibration card on trunk at breast height + context shot (tree identity/species). Photos fit GitHub's 25 MB Contents-API limit — no capping needed.

## 2. Event taxonomy (final — Gary 2026-08-26)

| Event | Cadence | Signed | Ledger impact | Gate |
|---|---|---|---|---|
| **[TREE GROWTH MONITORING EVENT]** | × N, one per measurement | Client RSA-2048 → Edgar → GAS handler | **None** — attribution/audit trail only (tracking tab + per-tree JSON history = monitoring report) | Farmer (own key) |
| **[CARBON CREDIT ISSUANCE EVENT]** (name TBD) | Periodic — aggregates a batch of VVB-verified measurements | Governor-level signer (mirror [CAPITAL INJECTION EVENT] / isGovernorByName_ pattern) | **The ONLY ledger-booking event** — books the DAO ledger/asset entry at issuance | Governor |

**Rule: every measurement = one signed [TREE GROWTH MONITORING EVENT], always. Not every signed event = a ledger entry.** Matches Verra / Gold Standard / ACR / 2026-dMRV-pilot precedent (monitoring accumulates as evidence; issuance is a distinct, periodically-verified event). **Issuance is OUT OF SCOPE for P1a** — noted so no retrofit later.

## 3. Architecture

```
Farmer phone (DApp + SunMint app)          Backend
├─ capture close-up + context photos        ├─ [ingest] receive photos + metadata (Edgar)
├─ auto GPS + timestamp + RSA signature     ├─ [hash] SHA-256 → audit trail
├─ save draft (offline-first, IndexedDB)    ├─ [GAS] validate sig → mirror to sunmint/images/growth/
└─ POST signed metadata + photos → Edgar    ├─ [GitHub Action] OpenCV: card detect → DBH → allometric → PM002 CO₂e → commits analysis.json
                                            ├─ [GAS] append Tree Growth Measurements tab row (dedup by Telegram msg ID)
                                            ├─ [GAS] write per-tree JSON history → Telegram Chat Logs
```

PM002 chain: `ΔBGB=ΔAGB×R` (R=0.32) · `PVCs=((ΔAGB+ΔBGB)×0.47)×44/12×(1−A_pre)(1−A_unc)(1−LD)(1−AR)(1−RB)` (AR=10%, RB=20%).

## 4. Build units (ONE PR PER TURN)

- **P0 ✅** Spec sign-off (Gary)
- **P1a ✅** DApp photo capture — `dapp_beta` `monitor_tree_growth.html` (PR #80 → #81 photo-first, merged)
- **P1b ✅** SunMint mirror — `truesight_me_beta` `sunmint/monitor-tree-growth/index.html` (PR #312, merged)
- **P1c ✅** dao_protocol registration — `[TREE GROWTH MONITORING EVENT]` catalog + dispatch ROUTING (PR #146, open)
- **P1d ⏳** GAS handler — `process_tree_growth_monitoring.gs` (tokenomics): validate sig → mirror photos → read analysis.json → Tree Growth Measurements tab row (dedup) → per-tree JSON history → Telegram Chat Logs. **No ledger booking.**
- **P2 ⏳** Python worker MVP (single-image) + `sunmint` repo GitHub Action (`paths: [images/growth/**]`, `permissions: contents: write`, commits `analysis.json`)
- **P3 ⏳** GeoJSON index build script (`sunmint/trees/index.geojson` + farm shards; derived cache from sheet + on-chain events)
- **P4 ⏳** UAT on both beta sites
- **Future** [CARBON CREDIT ISSUANCE EVENT] + credit issuance phase (out of scope)

## 5. Checklist

- [x] Spec v1.4 signed off
- [x] dapp_beta monitor_tree_growth.html (photo-first, PR #81)
- [x] truesight_me_beta sunmint/monitor-tree-growth (PR #312)
- [x] dao_protocol [TREE GROWTH MONITORING EVENT] registration (PR #146)
- [ ] GAS handler process_tree_growth_monitoring.gs (tokenomics)
- [ ] sunmint repo pm002_analysis workflow
- [ ] P2 worker single-image update
- [ ] GeoJSON index build script (P3)
- [ ] UAT both beta sites

## 6. Risks

- Card detection failure on low-quality photos → manual DBH entry fallback
- Cacao allometric equations need field calibration (v1 seeds; plan calibration plots)
- GeoJSON staleness → TTL + rebuild cron
- VVB acceptance of phone-photo DBH → TREEO/Plan Vivo precedent + context photo

## 7. RESUME HERE

**GAS handler PR (P1d, tokenomics)** — `process_tree_growth_monitoring.gs` mirroring `process_tree_planting_link.js` conventions (TPL_ prefix pattern, shared constants, no second doGet). After that: sunmint workflow (P2) → P2 worker update → P3 → UAT. dao_protocol PR #146 pending review/merge.
