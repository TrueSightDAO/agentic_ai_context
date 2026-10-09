# Ilhéus Warehouse — Management & Action Register

> **Purpose:** single reference for warehouse management at the Ilhéus (Black King / Matheus Reis) facility — site facts, compliance obligations, hygiene/pest-control ops, inventory & asset management, and wind-down actions. Cross-session SSOT; do not duplicate `OPEN_FOLLOWUPS.md` entries (link them).
> **Facility:** Black King / Matheus Reis Pereira — R. Cel. Paiva, 46, Centro, Ilhéus/BA (storage) — CNPJ 50.042.585/0001-80.
> **Compiled:** 2026-10-09 · **Thread:** 41062 · **By:** Sophia Truesight (TrueSight DAO Autopilot).
> **Sources:** thread 41062 transcript (2026-10-08 → 09); Telegram contribution stream (`ADVISORY_SNAPSHOT.md`, last 7 days); `OPEN_FOLLOWUPS.md`; `brazil/SUPPLY_CHAIN_SIMPLIFICATION.md`; `brazil/SUPPLY_CHAIN_AND_FREIGHTING.md` §2; `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md`; FSVP records.

---

## 1. Site & physical facts (data completeness)

| # | Action | Owner | Status |
|---|---|---|---|
| A1 | Record the **physical-facts block** (address, L×W×H, floor area) in `SUPPLY_CHAIN_AND_FREIGHTING.md` §2; mirror in `fda_fsvp/suppliers/black_king/entity.json` `facilities[]` | Sophia / Gary | **OPEN** — only a single tape span (~4.30 m, one wall) captured; footprint unknown |
| A2 | Capture the **floor plan** — digitize the whiteboard MAP (see `ILHEUS_WAREHOUSE_FLOOR_MAP.md`) and/or a measured sketch | Gary / Matheus | **OPEN** — whiteboard photographed 2026-10-09 |
| A3 | Reconcile the **two storage addresses** (FDA FFR `entity.json`: Av. Tancredo Neves 4900; site visit: Rua Coronel Paiva 46) and state the linkage | Sophia | **OPEN** (FSVP gap) |
| A4 | Register the **storage-location address(es)** + the fumigation NFS-e in `entity.json` | Sophia | **OPEN** |

## 2. FDA / FSVP compliance — 4 live obligations

Cross-linked (do NOT duplicate) from `OPEN_FOLLOWUPS.md` 2026-10-09 entries.

| # | Obligation | Fix | Owner | Status |
|---|---|---|---|---|
| B1 | **2026-09-12 GMP CAPA** (filth/pest finding) | File CAPA PDF `YYYYMMDD_Black King_<doctype>.pdf` with root cause + preventive action + verification walk | Sophia / Gary | **OPEN** |
| B2 | **Warehouse maintenance & pest-control written-assurance addendum (21 CFR 1.511)** | Black King–signed addendum: address(es) + linkage, cleaning SOP, pest-control cadence (ASTRA SUL BAHIA), humidity control, inspection-readiness checklist | Sophia / Matheus | **OPEN** |
| B3 | **Assign an owner** for hygiene / pest-control / inspection-readiness cadence | Name an accountable owner (candidate: part-time office/warehouse administrator) + written cadence | Gary | **OPEN** — root cause of the 09-12 finding |
| B4 | **Black King CNPJ INAPTO + e-CNPJ expired** — export NF-e lane blocked | Reinstatement: file missed DCTF/ECF/ECD/DAS, renew e-CNPJ, add CNAE 46.23-1/04, clear debts | Gary / accountant | **OPEN** |

## 3. Hygiene & pest-control operations

| # | Action | Owner | Status |
|---|---|---|---|
| C1 | Written **cleaning SOP + cadence** (floor wipe-down, dust/mold removal, dry-check before leaving) | Matheus / owner | **OPEN** — act performed 2026-10-09 (contribution logged), not yet codified |
| C2 | **Pest-control cadence** — schedule + log fumigation (ASTRA vendor; NFS-e `20250610_warehouse_fumigation.pdf`) | Matheus / owner | **OPEN** |
| C3 | **On-site equipment** — mop/vacuum, dehumidifier, insect repellent (Mercado Libre MLB20684318 proposed); verify suitability | Gary / Matheus | **OPEN** |
| C4 | **Air freshening + drying** before leaving | Matheus | **In practice** (2026-10-09) |
| C5 | Monthly **inspection-readiness walk** with photo evidence | owner | **OPEN** |

## 4. Inventory & asset management

| # | Action | Owner | Status |
|---|---|---|---|
| D1 | Reconcile **physical stock vs ledger** — 274 kg La Do Sitio (2024) + 34 kg ceremonial; AGL8 263.58 kg; AGL16 Oscar 108 kg (loaded 2026-10-07) | Sophia / Matheus | **OPEN** |
| D2 | **Mold currency swap** — mint 40 g mold; Matheus 50 g mold −1 → Gary 40 g mold +1 (pending name/cost + decrement source) | Sophia / Gary | **PARKED** |
| D3 | **Mold capacity QC** — molds hold ~200 g when filled (207 g water measured 2026-10-09) | Gary | **Done 2026-10-09** |
| D4 | **Equipment register** (whiteboard): 20× chocolate mold, label maker, weighing machine, tape, kraft pouches (nibs/caramel), plastic bags, trolley, 6× 80-mesh nibs | Sophia | **OPEN** |
| D5 | Ledger **holder accuracy** for Matheus-warehouse rows on `offchain asset location` | Sophia | periodic |

## 5. Strategic / wind-down

| # | Action | Owner | Status |
|---|---|---|---|
| E1 | **Ilhéus exit checklist** — clear final beans via Coopercabruca run; cure-or-moot the 4 FSVP items in writing; document disposition; close the DAO-token warehousing arrangement | Gary | **OPEN** (medium) |
| E2 | **Demand-signal replacement** for the retired prestock — name it before removing the buffer | Gary | **OPEN** (decision) |
| E3 | Confirm **Matheus warehousing arrangement closed out** | Gary / Matheus | **OPEN** |

## 6. Priority register (top 8)

| Priority | Item | Why |
|---|---|---|
| P1 | B4 CNPJ INAPTO reinstatement | Blocks every export NF-e via Black King |
| P2 | B3 Assign hygiene/pest-control owner | Root cause of the 09-12 FDA finding |
| P3 | B2 Pest-control written-assurance addendum | Live FSVP gap (21 CFR 1.511) |
| P4 | B1 GMP CAPA for 09-12 finding | Live FSVP gap; regulator-facing |
| P5 | A1/A2 Site physical-facts + floor plan | No canonical dimensions exist |
| P6 | D1 Physical-vs-ledger stock reconciliation | Inventory accuracy |
| P7 | E1 Ilhéus exit checklist | Decision made; execution unplanned |
| P8 | D2 Mold 50→40 g swap | Awaits governor fields |

## 7. Governance notes

- **Authority:** `BRAZIL_EXPORT_LANE_LEARNINGS.md` (7 Black King issues) · `brazil/SUPPLY_CHAIN_SIMPLIFICATION.md` (cooperative-first + Ilhéus wind-down, decided 2026-10-09, thread 780).
- **Structural rule:** MAPA/GACC attach to the **production enterprise** (processing facility), not the exporter/trader — the **cooperative is the durable funnel**.
- **Ledger authority:** the Main Ledger is authoritative; whiteboard / physical observations are unaudited working notes.
- **Contribution logging:** warehouse-management acts are logged as `[CONTRIBUTION EVENT]` (2026-10-09: mold QC 60 min, floor upkeep 60 min, whiteboard layout 15 min).
