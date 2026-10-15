# Brazil → San Francisco Freight Lane — End-to-End SOP Refresh + Machine-Readable Pre-Flight Checklist (Plan)

**Filed:** 2026-10-15 · **Owner:** Sophia · **Governor:** Gary Teh (thread 42300 / orig. freight thread)
**Status:** DRAFT — design-first. **Build gated on completion of the AUM stage** (Gary: *"Once done till the AUM stage, can we update the SOP …"*).

---

## 1. Why this exists

The lane already has a canonical runbook — `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`
(Phases 0–8, *"Last verified 2026-10-02"*) — plus a meta-doc (`brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md`),
sibling SOPs (HK, GCC/ME), and a PDF builder (`scripts/build_brazil_sf_freight_preflight_pdf.py`).
But it has two gaps Gary wants closed:

1. **It stops before the ledger/AUM stage.** Phases 0–8 run Ilhéus → SFO → Kirsten's SF warehouse.
   The Black King build then added a whole **ledger + AUM tail** (asset receipt → inventory movement ×8 →
   repackaging/conversion → cost amortization → §6 `Currencies` rows → `/aum` re-warm → balance verify)
   that is **not** in the runbook. Its hard-won rules — **§5.11 terminology** (transfer = `[INVENTORY MOVEMENT]`;
   transformation = repackaging triad) and the **§5.15 derived-view write trap** (`offchain asset location`
   is a spilled view — never write it) — are also absent.
2. **It is prose, not machine-readable.** An LLM must parse a ~90 KB markdown file to answer
   *"what must be true before this freight moves?"*. Gary's ask: Sophia/LLMs should be able to
   **generate a per-freight pre-flight checklist**, so no step is ever missing when preparing a future freight.

**Goal:** one end-to-end runbook (Ilhéus → SF warehouse → ledger → AUM) **plus** a machine-readable
checklist source that renders both the human PDF and an agent checklist.

---

## 2. Two deliverables

### D1 — Runbook refresh (prose): `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`
- **Add Phase 9 — Ledger & AUM settlement** (see §3) — the missing tail.
- **Absorb post-2026-10-02 reality:** NF-e nº **18** issued (supersedes nº 16); AWB **`047-3175-3223`**
  (gross **349 kg**); DU-E **`26BR001795400-0`**; **FDA Prior Notice filed** `F26X30142399` — flip §5.6's stale
  `unfiled` line; pallet material reconciled (**plastic HDPE → ISPM#15 N/A**), retire the §1 "heat-treated" contradiction.
- **Carry the Black King build rules** into the runbook as first-class agent rules: **§5.11** terminology, **§5.15**
  derived-view trap, the `+AWB` clone-name validator snag (supersede-and-migrate, no rename primitive).
- **Fix drift:** bump "Last verified", artifact-link every row.

### D2 — Machine-readable checklist source (NEW): `brazil/brazil_sf_freight_checklist.json`
A structured array of gate objects — the **single source of truth** for the lane:

```json
{
  "id": "phase0.entity_readiness.cnpj_status",
  "phase": 0,
  "gate": "CNPJ situação cadastral = Ativa (not Inapto)",
  "owner": "Saymon/Jussileide",
  "blocks": "NF-e issuance",
  "evidence": "e-CAC Situação Fiscal print",
  "tracker": "https://… (optional live re-check, e.g. SISCOMEX habilitação §5.4)",
  "human_doc_ref": "BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md §5.4",
  "applies_to": ["all"],
  "last_verified": "2026-10-02",
  "exercised": true
}
```

- **Single source:** the runbook's phase tables **and** the PDF are **generated from this file**
  (extend `scripts/build_brazil_sf_freight_preflight_pdf.py` to read it). No double-maintenance.
- **Agent consumption:** Sophia / any LLM reads the JSON, filters by lane + cargo, and emits a **per-freight
  pre-flight checklist** ("for an air shipment of X kg cacao Bahia→SF: these N gates must be green; owner + evidence per gate").
- **Freshness:** each gate carries `last_verified` + an optional `tracker`, so the agent **checks the signal**
  (SISCOMEX status, AGL15/USD balance, FDA PN status) instead of trusting prose.
- **`exercised` flag:** false until a live freight has actually run that gate end-to-end.

---

## 3. End-to-end phase model (target)

| Phase | Covers | In runbook today |
|---|---|---|
| 0 | Entity, tax & regulatory readiness (CNPJ, e-CNPJ, CNAE/IE, municipal licence, MAPA-if-China) | ✅ |
| 1 | FX & commercial documents (PTAX / BACEN; dual USD+BRL) | ✅ |
| 2 | NF-e draft & **Gary-approval gate** | ✅ |
| 3 | Cargo prep at origin (Ilhéus) — SKUs, cartons, pallets | ✅ |
| 4 | Inland transport (Ilhéus → Salvador) | ✅ |
| 5 | Airport & export processing (weighing, DU-E, AWB) | ✅ |
| 6 | Air freight (SSA → SFO) | ✅ |
| 7 | US import, customs & **last-mile → Kirsten's warehouse** | ✅ (thin) |
| 8 | (reserved / reporting) | ✅ |
| **9 (NEW)** | **Ledger & AUM settlement** — asset receipt; `[INVENTORY MOVEMENT]` ×8 (Matheus → Kirsten); repackaging/conversion triad; cost amortization; §6 `Currencies` rows; `/aum` re-warm; balance verify | ❌ **missing** |

---

## 4. Dependencies / gates

- **AUM stage must complete first** (Gary's instruction): the lane's true cost — including the Black King
  landed-cost amortization build (the $4,896.33 pool, the `+AWB` clone naming, the 8-currency chain) — is only
  **final once the chain lands**. Write §9 from the *completed* build, not the plan (`plans/FREIGHT_COST_AMORTIZATION_PLAN.md`).
- **Cargo arrival** (standing gate): the ledger tail cannot be **exercised** end-to-end until the cargo physically
  arrives; the SOP can *document* it beforehand, but the checklist `exercised` flag stays **false** until then.
- **Open sub-items the refresh must absorb or cross-link** (`OPEN_FOLLOWUPS.md`): SISCOMEX diarization (§5.4, #1486);
  Ilhéus exit checklist; CNPJ-reinstatement runbook; FDA PN §5.6 stale line; AGL15 two-defect cleanup (thread 42300).

---

## 5. Build sequence (post-AUM)

1. **Unit 1** — Extract the JSON gate model from the current runbook (Phases 0–8) → `brazil_sf_freight_checklist.json`.
   No prose change yet; verify it regenerates the existing PDF faithfully.
2. **Unit 2** — Add **Phase 9** (ledger/AUM tail) to the JSON **and** the prose, sourced from the completed
   Black King build + `FREIGHT_COST_AMORTIZATION_PLAN.md`.
3. **Unit 3** — Repoint `build_brazil_sf_freight_preflight_pdf.py` so the runbook's phase tables **and** the PDF
   generate from the JSON (single source of truth).
4. **Unit 4** — Add the **agent checklist generator** (small script / Sophia tool): given lane + cargo params,
   emit the pre-flight checklist (MD/PDF).
5. **Unit 5** — Sweep stale items (§5.6 PN → FILED; pallet contradiction retired; "Last verified" bumped);
   regenerate PDF + JSON; attach the PDF to the thread.

---

## 6. Acceptance

- `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` covers **Phase 0 → 9** (arrival → SF warehouse → ledger → AUM),
  every row artifact-linked.
- `brazil_sf_freight_checklist.json` is the **single source**; prose + PDF are generated from it (no double-maintenance).
- **Sophia can generate a per-freight pre-flight checklist** from the JSON for a described future shipment,
  with owner + evidence + tracker per gate.
- **No-regression check:** no gate omits a step the Black King freight actually needed (diff against the
  build's ~43 documented steps).
