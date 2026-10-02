# Brazil → San Francisco Freight Lane — End-to-End Runbook

> **Audience:** AI agents (Sophia / any autopilot instance), LLMs, and human **Envoys** operating the DAO's Brazil export lane.
> **Canonical file.** If any other document disagrees with this one, **this file wins** — fix the other doc in the same PR.
> **Lane:** Ilhéus, BA (Matheus / Gateway.fy warehouse — **physical pickup: R. Cel. Paiva, 46, Centro**) → road → Salvador (SSA) → air → San Francisco (SFO) → Kirsten's SF warehouse.
> **Commercial basis:** Brazil exporter (Black King, or fallback Coopercabruca) → **TrueTech Inc** (US importer of record, EIN 88-3411514).
> **Last verified:** 2026-10-01. Sources: Seacos/Omega quote thread (May–Jun 2026); Black King accountant WhatsApp thread (2026-09-18 → 21) — see `brazil/sources/2026-09-21_black_king_accountant_thread_notes.md`; **Ilhéus pickup-address confirmation — Gary, thread 10800, 2026-09-29** (see §2a); **NF-e nº 16 issued 2026-09-22** — DANFE + notes at `brazil/sources/2026-09-22_black_king_nfe_16_danfe.pdf`.

---

## 0. Read-me-first — operating contract for agents & Envoys

If you (an AI agent or an Envoy) are asked to "move the Brazil shipment along", obey this contract:

1. **Read this file top to bottom before acting.** Never guess how a step works; if this doc is wrong, fix it (same PR) before proceeding.
2. **NF-e APPROVAL GATE — never issue, and never let anyone issue, a nota fiscal without Gary Teh's explicit approval first.** Gary, 2026-09-18: *"toda vez que for emitir uma nota fiscal ... todas as notas fiscais ... precisam ser submetidas à minha aprovação antes de sua emissão."* Draft → **Gary approves** → then issue.
3. **MONEY RULE — DAO funds cover ONLY Black King obligations from Nov 2024 onward.** Any payment record (comprovante/DARF) driven by DAO money **must not show anything before Nov 2024** (audit requirement). Never move money without an explicit governor command.
4. **CURRENCY RULE — the NF-e is issued in BRL.** State the **PTAX reference date** explicitly and use the official **BACEN PTAX** rate for that date (https://www.bcb.gov.br/conversao). Commercial invoices from now on are **dual USD + BRL** (or BRL) so the NF-e can be issued without re-deriving values. See §3.
5. **Evidence:** every completed step gets an artifact (PDF / XML / screenshot / ledger event) filed under `agentic_ai_context/exports/` (or the relevant repo) and linked in the checklist row.
6. **Ledger events:** use `lookup_event_docs` → `submit_contribution` for inventory movements, sales, and contributions. A signed submission IS the authorization — there is no DApp approval gate.
7. **Say what you verified vs. assumed.** Update this file whenever reality diverges from it.

---

## 1. Status snapshot (2026-09-29)

| Gate | Status | Owner | Notes |
|------|--------|-------|-------|
| SISCOMEX / RADAR (brokers registered) | 🟡 **representante link failing** | Matheus | ⚠️ **Reality diverged 2026-09/10:** a DU-E registration attempt returned *"O usuário não consta como representante do declarante ou do exportador…"*, and the *Lista de Representações* was **empty** (*"Nenhum registro adicionado"*). Original "3 Omega brokers registered (Jun 2026)" — primary source: `brazil/sources/2026-05-18_omega_siscomex_representante_tutorial_notes.md`; a **revised** tutorial was received 2026-10-01. **Roster may have rotated** (archived #3 *Mauricio Costa Bezerra* absent from Gary's 2026-10-01 list, which adds *Jackson Pereira Ferreira*) — **pending Gary's confirmation (replace vs. add)**. |
| Omega PoA signed | ✅ done (Jun 2026) | Matheus | Omega (forwarder) can act on the export — **distinct** from the e-CAC/cartório procuração in §5 Phase 0 |
| NCM 1801.00.00 confirmed | ✅ | Omega | no MAPA needed for US |
| **CNPJ regularization (exit Inapto)** | 🔴 **BLOCKING — cargo held at SSA** | Saymon/Jussileide + Gary | **Confirmed live 2026-10-01**: Omega reports the export is **on hold** — the RFB flagged **CNPJ non-compliance with admissibility requirements** (matches **Inapto since 08/06/2026**, motivo *Omissão de Declarações*); Omega has filed a **formal RFB inquiry** to enumerate the outstanding items. DARF **NOV.2024–JUL.2026** issued & DAO portion paid; **2023 MEI-era guia** still pending. **Resolution requires the CNPJ to show Ativa.** Source: `brazil/sources/2026-10-01_omega_export_hold_cnpj_notice.md` |
| **e-CNPJ certificate** | ✅ works | Matheus | cert usable via gov.br (no longer the blocker) |
| **Commerce CNAE / IE / SEFAZ-BA** | ✅ **IE active** | Saymon | **IE 205055715 now printed on the DANFE** (NF-e nº 16) — IE/SEFAZ-BA credentialing evidently completed. Formerly flagged as *unreconciled* (order nº 003625 carried an IE the runbook said did not exist); the DANFE confirms it is real. |
| **Municipal licence (licença comercial)** | 🔴 pending | Saymon/Jussileide | needed for the cacao business; not in old doc |
| **NF-e draft** | ✅ **superseded** | Saymon | draft errored 2026-09-21 on **unidades de medida**; fixed by the Rev 12 unit remap (§5.1a). **Now moot — the NF-e was issued (see next row).** |
| **NF-e issued** | ✅ **issued** | Saymon | **NF-e nº 16, série 1, emitida 22/09/2026** — chave `2926 0950 0425 8500 0180 5500 1000 0000 0161 3000 0003 5`, protocolo `129261913151752`, **R$ 35.828,76**. All 11 lines, NCMs and the TON/KG remap match Rev 12 (§5.3). Evidence: DANFE — `brazil/sources/2026-09-22_black_king_nfe_16_danfe.pdf`; signed **XML** — `brazil/sources/2026-09-22_black_king_nfe_16.xml` (+ reconciliation notes `brazil/sources/2026-09-22_black_king_nfe_16_xml_reconciliation.md`). XML `cStat` **100 (Autorizado)**. |
| DU-E (Notificação de Exportação Fiscal) | 🔴 **ON HOLD** | Omega | **Blocked by the CNPJ/exporter-habilitação gate (not paperwork).** Omega, 2026-10-01 (cargo **already at Salvador airport**): *"the export process is currently on hold due to a non-compliance with admissibility requirements identified in the CNPJ…"*; Omega has filed a formal **RFB inquiry**. The NF-e prerequisite *is* met (nº 16 issued 22/09/2026) — but **§5 Phase 0** is not. Source: `brazil/sources/2026-10-01_omega_export_hold_cnpj_notice.md` |
| Cargo prep / pallets | ⬜ | Matheus | heat-treated pallets being sourced |
| Air freight | ⬜ | Graziela/Omega | rates only |
| Deadline pressure | — | — | **China partners arrive 2026-09-29** (Gary asked to resolve before then) |

> 📎 **Source (SISCOMEX/RADAR representante registration):** Omega's original step-by-step tutorial is archived at `brazil/sources/2026-05-18_omega_siscomex_representante_tutorial_notes.md` (+ the PDF alongside). Primary source for the "3 Omega brokers registered" row above.
>
> ⚠️ **Correction vs. the old doc:** the previous "THREE root causes" (expired e-CNPJ, missing-commerce-CNAE-via-e-CAC, CNPJ Inapto) are **partly stale**. e-CNPJ now works; the CNAE route is superseded by a **Junta Comercial → Prefeitura** chain; the Inapto path now has concrete DARF mechanics.

---

## 2. Roles & contacts

| Role | Name | Company | Contact |
|------|------|---------|---------|
| Freight forwarder / coordinator | Graziela Vedana | Seacos Logistic | Graziela@5cl.rs · WhatsApp +1 603-560-0588 |
| Export operations | Isis Ribeiro | Omega Services | isis.ribeiro@omegaservicos.com.br |
| Export pricing | Ana Barros | Omega Services | ana.barros@omegaservicos.com.br |
| SISCOMEX / customs | Iolanda Santos | Omega Services | iolanda.santos@omegaservicos.com.br |
| Desembaraço (export clearance) | Gerson Argolo | Omega Services | gerson.argolo@omegaservicos.com.br |
| Commercial / management | Helesson Bastos | Omega Services | helesson.bastos@omegaservicos.com.br |
| Origin warehouse / cargo | Matheus Reis (Black King, EI) | Gateway.fy | theus.reis.ssa@gmail.com · WA +55 11 91413-5328 · +55 73 99109-0002 · **pickup: R. Cel. Paiva, 46, Centro** (§2a) |
| Ilhéus warehouse (physical) | Rebecca | — | +55 73 99108-2946 · **R. Cel. Paiva, 46, Centro, Ilhéus - BA, 45653-310** |
| **NF-e specialist (hired)** | **Saymon** | (contractor) | WhatsApp group "Black King - Contab" |
| **Accountant (hired)** | **Jussileide** | (contractor) | WhatsApp group "Black King - Contab" |
| US importer of record | TrueTech Inc | — | EIN 88-3411514 · 1423 Hayes St, San Francisco, CA 94117 |

> **Note:** the old doc said "bypass the accountant; 8 days". **Accountants have now been hired (Saymon + Jussileide)** and the lane is still not through — the bottleneck is the **structural (Junta/Prefeitura)** chain and the **master-data setup**, not the accountant's responsiveness.
>
> **⚠️ Delivery channel — Saymon & Jussileide are NOT on Telegram.** They are contractors on the WhatsApp group **“Black King - Contab”** and have **no access to this Telegram thread (10800)**. Any artifact meant for them (invoices, packing lists, the Rev 12 PDFs, emitter instructions) must be **relayed by Gary into that WhatsApp group** — posting a file in thread 10800 does **not** reach them. Likewise, Saymon's replies arrive in WhatsApp and must be transcribed into the runbook/source-notes by whoever holds that channel. OpenClaw's verified JID list contains **only** The Beer Hall + Prompt Haus — `“Black King - Contab”` is **not** a verified OpenClaw target, so there is currently no automated delivery path to Saymon.

### Addresses — legal (CNPJ) vs. physical warehouse

Two different Ilhéus addresses appear in this lane. **Do not conflate them** — this states the linkage left open as *"two storage addresses … with no stated linkage"* in `OPEN_FOLLOWUPS.md`:

| Role | Address | Appears on |
|------|---------|------------|
| **Physical warehouse / cargo pickup** | **R. Cel. Paiva, 46 — Centro, Ilhéus - BA, 45653-310** | Omega road collection (Phase 4); the canonical scripts warehouse; the 2024-10-13 storage-warehouse site visit |
| **Black King registered (CNPJ) address** | Av. Tancredo Neves, 4900, Qd H, Cs 9, Nossa Senhora da Vitória, Ilhéus, BA, 45655-650 | FDA FFR / `entity.json`, GACC registration, and the NF-e **emitente** row (Appendix A) |

> **Confirmed by Gary, thread 10800, 2026-09-29:** *"This is the correct pickup location — R. Cel. Paiva, 46 - Centro, Ilhéus - BA, 45653-310, Brazil."* CEP validated (45653-310 = Rua Coronel Paiva, Centro, Ilhéus/BA).
>
> ⚠️ **Reconcile with Omega before the truck rolls.** Pickup order **nº 003625** (Omega, 2026-09-29) shows **Local Coleta = Av. Tancredo Neves, 4900** (the *registered* address), **not** R. Cel. Paiva, 46. Confirm the driver collects at the **physical warehouse**.

---

## 3. Currency & FX rule (BRL / PTAX)

- The **NF-e must be issued in BRL**. The commercial invoice may be USD (or dual USD+BRL).
- **Declare the PTAX reference date** on the invoice and NF-e. Use the **official BACEN PTAX** rate for that date: https://www.bcb.gov.br/conversao.
- **Sebrae emitter does NOT auto-update FX.** Saymon, 2026-09-21: *"toda vez que for emitir uma nota fiscal, será necessário alterar o valor de todos os produtos."* → **re-key every product value on every issuance.**
- **Convention (Gary, 2026-09-21):** going forward, commercial invoices are quoted in **BRL (dual USD+BRL)** to simplify NF-e issuance.
- **Worked example (Rev 11, dated 2026-09-21):** total **$6,946.85 USD = R$ 35,828.38 BRL** @ PTAX venda **5.1575 (18/09/2026)**. (No PTAX is published on weekends → nearest business day.)

---

## 4. Documentation model — three layers (do not conflate)

See **Appendix C**. Summary:

- **Brazilian customs** sees: **Black King → TrueTech Inc** (NF-e + DU-E + customs commercial invoice all match).
- **Tax / transfer pricing** sees: **Black King → TrueSight DAO LLC (Próspera) → TrueTech Inc**.
- **FDA** sees: **Black King (facility) → TrueTech Inc (importer)**. Próspera never registers (not a food facility).

**Never put Próspera on the NF-e, DU-E, or customs invoice.**

---

## 5. Lane state machine — Phases 0–8

Each phase: **Owner** · **Gate/exit criteria** · **Evidence**.

### Phase 0 — Entity, tax & regulatory readiness  ← *current blocker*
- [ ] **CNPJ regularized (exit Inapto).** Owner: Saymon/Jussileide. Evidence: CNPJ status page (`solucoes.receita.fazenda.gov.br` / e-CAC) shows **Ativa**.
  - DARF **NOV.2024–JUL.2026** generated & paid (DAO portion = Nov 2024+).
  - Separate **2023 MEI-era guia** handled separately (can be future-dated; no discount).
  - ⚠️ The full-debits DARF can only be generated **for the current day** — regenerate on the payment day.
- [ ] **Company contract amended at Junta Comercial.** Owner: Saymon. (`alteração do contrato social`)
- [ ] **Prefeitura updated → municipal licence (licença/alvará comercial) for the cacao business.** Owner: Saymon/Jussileide. — *missing from the old doc; currently the key unknown.*
- [ ] **Tax guides (guias de tributos) generated.** Owner: Jussileide.
- [ ] **Commerce CNAE active** (46.23-1/04 *comércio atacadista de cacau*). ⚠️ **Open question:** the old doc's "10-min e-CAC CNAE" path is contradicted by Saymon's Junta-Comercial route — confirm with Saymon whether Black King is an Empresário Individual or an Ltda, and which path actually applies. **Do not assume.**
- [ ] **IE at SEFAZ-BA** obtained (needs the commerce CNAE first). Evidence: Consulta de Inscrição Estadual.
- [ ] **e-CNPJ certificate valid.** ✅ (verified working — Matheus logs in via gov.br).
- [ ] **SEFAZ NF-e credentialing** (modelo 55) approved.
- [ ] **PoA / procuração (Governor admin access) — e-CAC / cartório.** ⚠️ **Distinct from the §1 Omega forwarder PoA (✅ Jun 2026, done).** This is the procuração granting the Governor admin access to Black King's *federal* affairs; Jussileide (2026-09-18) says the **carta de procuração is to be done at the cartório** directly. It does **not** cover SEFAZ-BA / NF-e. For the *forwarder* PoA + SISCOMEX representante registration (a different instrument, already done), see the §1 SISCOMEX/RADAR row and `brazil/sources/2026-05-18_omega_siscomex_representante_tutorial_notes.md`.

### Phase 1 — FX & commercial documents
- [ ] Commercial invoice + packing list present, **dual USD+BRL**, dated, with **declared PTAX date**.
- [ ] Current revision pointer pinned below (see §5.1). Evidence: PDFs in `exports/`.

### Phase 2 — NF-e draft & Gary-approval gate
- [x] **Draft NF-e prepared** in the Sebrae emitter (master data see §5.2). Owner: Saymon. *(Saymon works in WhatsApp “Black King - Contab”, not Telegram — Gary relays.)*
- [x] **🛑 Gary approves the draft** (hard gate §0.2). Evidence: approval message in thread 10800.
- [x] **NF-e issued** (modelo 55, CFOP 7.101/7.102, exportação). Evidence: XML + DANFE. — **issued 2026-09-22: NF-e nº 16, série 1, chave `2926 0950 0425 8500 0180 5500 1000 0000 0161 3000 0003 5`, R$ 35.828,76.**
- [ ] XML + DANFE sent to Graziela/Omega; Omega PIX details to Gary.

### Phase 3 — Cargo prep at origin (Ilhéus)
- [ ] Cargo photos shared. Owner: Matheus.
- [ ] **ISPM#15 pallet compliance:** fumigated or heat-treated, **IPPC stamp legible on all sides**, original Phytosanitary Certificate to accompany docs.
- [ ] Packing arranged at Matheus's Ilhéus warehouse — **R. Cel. Paiva, 46, Centro, Ilhéus - BA, 45653-310** (physical pickup site — §2a).

### Phase 4 — Inland transport (Ilhéus → Salvador)
- [ ] Road transport booked. Cost: **BRL 6,615.00 + 0.15% ad-valorem** (with Salvador palletization); **BRL 7,290.00 + 0.15%** without.
- [ ] Collection scheduled by Omega (pickup at **Matheus's Ilhéus warehouse — R. Cel. Paiva, 46, Centro** — §2a). ⚠️ Omega pickup order **nº 003625** (2026-09-29) lists **Local Coleta = Av. Tancredo Neves, 4900** (the *registered* address) — confirm with Omega the driver collects at **Cel. Paiva**, not the legal address.
  - **Ordem de coleta (corrected draft — REV 2):** `exports/2026-09-29_ordem_de_coleta_black_king_ilheus_ssa.pdf` — generated by `scripts/build_order_de_coleta.py` from the Rev 12 line table (reconciles line-by-line). **REV 2 is keyed to the issued NF-e nº 16** (§5.3): it carries the full NF-e identification block (nº/série, chave de acesso, protocolo, emitente IE/CNPJ, natureza/CFOP, total), the pickup address + on-site contacts, the 11-line manifest in **commercial units with a fiscal uTrib column**, and **fills the TRANSPORTADOR / VOLUMES TRANSPORTADOS block the DANFE left blank** (2 volumes · paletes HDPE · líquido 344,06 kg · bruto 364,06 kg). Driver must carry NF-e nº 16.

### Phase 5 — Airport & export processing (Salvador)
- [ ] Palletization + fumigation at Salvador (if not at origin): **BRL 195 (3 pallets) + BRL 500 (fumigation) = BRL 695**.
- [ ] Airline booking confirmed + quote revalidated (Graziela).
- [ ] **Export docs:** AWB, Commercial Invoice, Packing List, Phytosanitary Cert (pallets), IPPC details.
- [ ] **DU-E registered** (Notificação de Exportação Fiscal). Owner: Omega.
- [ ] **Desembaraço de exportação** (Gerson Argolo).
- [ ] **Correction Letter to SeaCoast** (freight forwarder) — Daniel flagged that the issued invoice lacked **weights, quantity and package type**. Draft: `exports/2026-09-29_correction_letter_black_king_inv_rev12_EN_PT.pdf` (generated by `scripts/build_correction_letter.py` from the Rev 12 SSOT; carries a **Portuguese pickup section** — where to collect + what is collected — for the Brazilian warehouse/carrier). ⚠️ This is a **commercial** companion to NF-e nº 16 (issued 2026-09-22), **not** a fiscal **CC-e**; the DANFE's own TRANSPORTADOR/VOLUMES block is **blank** — the weights/quantity/package-type Daniel flagged — so a commercial letter (or a CC-e, once the carrier data exists) is what closes it. Owner: Gary → Black King signs → SeaCoast.

### Phase 6 — Air freight (SSA → SFO)
- [ ] Air freight booked. Tiered: 200 kg ≈ $3.50/kg · 300 kg ≈ $3.40 · 500 kg ≈ $3.30 · 750 kg ≈ $3.30 · 1000 kg ≈ $3.20.
- [ ] Brazil airport charges: ≈ $0.30/kg (min $250). US airline terminal ≈ $212.50.
- [ ] Net **344.06 kg** / gross **364.06 kg** (Rev 12 packing list, derived from documented pack sizes) — Rev 11 stated ≈ 300 / 320 kg; **reconcile against the weighed shipment**.

### Phase 7 — US import, customs & final delivery
- [ ] US import handling ≈ $125. US customs clearance ≈ $150. FDA processing ≈ $100 (if required).
- [ ] Bond (single-entry, if req.): max($100, $6 per $1,000 of value+duty). MPF 0.3464% (min $33.58, max $651.50). Duty if applicable. Customs exam ≈ $250 (random).
- [ ] Delivery SFO → **Kirsten's SF warehouse**.

### Phase 8 — Ledger & reporting (DAO)
- [ ] Record the **`[INVENTORY MOVEMENT]`** for the shipment once the destination ledger name is confirmed.
- [ ] File the **contribution event(s)** for the round (with PR/evidence links).
- [ ] Update this runbook's status snapshot (§1).

#### 5.1 Current commercial revision
- **Invoice INV-2026-0611-001 Rev 12 (+BRL)**, dated 2026-09-21, **$6,946.85 USD / R$ 35,828.38 BRL** @ PTAX 5.1575 (18/09/2026) — *values unchanged from Rev 11; only the declared units of measure changed.* Files: `exports/2026-06-11_commercial_invoice_black_king_to_truetech_rev12_EN_PT_BRL.pdf`; packing list `exports/2026-06-11_packing_list_black_king_to_truetech_rev12_EN_PT.pdf`. Generated reproducibly by `scripts/build_black_king_export_docs.py` (merged `agentic_ai_context` #1333, `c3ac61a`). **Rev 11 is superseded** (its mixed UN/KG units are what the emitter rejected).
- **Superseded:** Rev 11 — `exports/2026-06-11_commercial_invoice_black_king_to_truetech_rev11_EN_PT_BRL.pdf` (and `inv_rev11_brl_dated.pdf`).
- **Line items (Rev 11):**

| # | NCM | Description | Qty | Unit | USD |
|---|-----|-------------|-----|------|-----|
| 1 | 1801.00.00 | Cacao Nibs Kraft Pouch 8oz — Ilhéus 2024 | 129 | UN | $856.56 |
| 2 | 1803.10.00 | Cacao Husk (KG) — Ilhéus | 20 | KG | $355.71 |
| 3 | 1803.10.00 | Cacao Mass Bar 500g — Ilhéus 2024 | 37 | UN | $580.90 |
| 4 | 1801.00.00 | Cacao Nibs (KG) — Ilhéus 2024 | 80 | KG | $1,969.48 |
| 5 | 1801.00.00 | Cacao Almonds (KG) — AGL8 | 10 | KG | $0.10* |
| 6 | 2106.90.00 | Cacao Tea (KG) — AGL8 | 12 | KG | $0.12* |
| 7 | 1803.10.00 | Ceremonial Cacao Pouch 200g — AGL8 | 169 | UN | $1,752.53 |
| 8 | 1801.00.00 | Cacao Almonds (KG) — AGL13 | 15 | KG | $118.05 |
| 9 | 1801.00.00 | Cacao Nibs (KG) — AGL13 | 99.5 | KG | $1,012.91 |
| 10 | 2106.90.00 | Cacao Tea (KG) — AGL13 | 21 | KG | $213.83 |
| 11 | 1804.00.00 | Coopercabruca Cacao Butter (KG) | 5 | KG | $86.66 |

*Nominal $0.01/unit values used to satisfy emitter validation.

> ✅ **Rev 12 regenerated + merged (2026-09-21).** Applied The NF-e draft errored on **unidades de medida**: a technical norm (*norma técnica*) mandates specific units of measure for some NCMs in case of export. Saymon: *“deverá ser gerada outra invoice com as unidades de medida e os valores corretos.”* → the commercial invoice + packing list were regenerated in the NCM-mandated export units (PR #1333, `c3ac61a`); see the merged PDFs in `exports/`. **Finalized 2026-09-21 (PR #1335, `f7acdff`):** the red DRAFT banner and all draft/hedge wording were removed from both PDFs; units and USD/BRL values unchanged. *Attribution: the packing-list-consistency confirmation (PL follows Saymon's norm by construction — same generator, shared `LINES`/`UTRIB` table) came from **Envoy**, not governor Gary Teh, and is **not** an authorization.*

#### 5.1a Rev 12 — required export units (NCM remap)

> Source: NCM→uTrib export-unit norm table supplied by Gary 2026-09-21 (**Appendix E**). Chapter-18 raw/intermediate forms (**1801 beans/nibs, 1803 paste/mass, 1804 butter/fat**) must be declared in **TON** (tonelada métrica líquida); 1802 (husks) and finished 1806* use **KG**. Rev 11 declared the 1801/1803/1804 lines in **UN / KG** → this is the rejection.

| # | NCM | Rev-11 qty | Rev-11 unit | Rev-12 required unit | Rev-12 qty (≈ t, see caveat) |
|---|-----|-----------|-------------|----------------------|------------------------------|
| 1 | 1801.00.00 | 129 | UN | **TON** | ≈ 0.0293 |
| 2 | 1803.10.00 | 20 | KG | **TON** | 0.0200 |
| 3 | 1803.10.00 | 37 | UN | **TON** | ≈ 0.0185 |
| 4 | 1801.00.00 | 80 | KG | **TON** | 0.0800 |
| 5 | 1801.00.00 | 10 | KG | **TON** | 0.0100 |
| 6 | 2106.90.00 | 12 | KG | KG *(not in norm table)* | — |
| 7 | 1803.10.00 | 169 | UN | **TON** | ≈ 0.0338 |
| 8 | 1801.00.00 | 15 | KG | **TON** | 0.0150 |
| 9 | 1801.00.00 | 99.5 | KG | **TON** | 0.0995 |
| 10 | 2106.90.00 | 21 | KG | KG *(not in norm table)* | — |
| 11 | 1804.00.00 | 5 | KG | **TON** | 0.0050 |

> The ≈ t column is a **mechanical kg→t / unit-weight conversion** (8 oz pouch = 0.2268 kg; 500 g = 0.5 kg; 200 g = 0.2 kg), now applied on the merged Rev 12 PDFs — Saymon to confirm the declared quantities match the weighed shipment.
> **Applied as provided:** every line is declared in the exact uTrib the norm table gives for its NCM — no unit substituted or reclassified. Line #2 stays under 1803.10.00 → **TON** as listed.
> ℹ️ **Not in the table:** NCM **2106.90.00** (Cacao Tea, #6/#10) is outside Chapter 18 and is not keyed by this norm, so no unit was supplied for it; those lines remain **KG** as declared on the invoice.

> 📎 **Operator manual archived (2026-09-22):** `brazil/sources/2026-06_sebrae_emissor_nfe_manual_v10_PT.pdf` — *SEBRAE NF-e Emitter User Manual v10, Jun 2026, 270 pp (PT-BR)* — with distilled notes at `brazil/sources/2026-06_sebrae_emissor_nfe_manual_notes.md`. Authoritative click-by-click for every step below (certificate A1/A3, product fiscal fields incl. **UNIDADE**, Matriz Fiscal/CFOP/CST-CSOSN, export NF-e, rejeições).

#### 5.2 Sebrae emitter — master-data sequence (in order)
1. **Register the company as emitente** (Saymon, in progress). Black King **already had an account** (Matheus used it before). Login: `https://emissornfe.sebrae.com.br/` → **gov.br** → *Seu Certificado Digital* → Black King cert (shows as Matheus) → select Black King.
2. **Register products.**
3. **Register clients** — **TrueTech Inc already registered.**
4. **Register suppliers (fornecedores).**
5. **Then issue** the export NF-e (CFOP 7.101/7.102).
- Emitter alternatives if needed: SEFAZ-BA web emitter (free); national free emitter for BA.

---

#### 5.3 NF-e nº 16 — issued 2026-09-22 (reconciled vs. Rev 12)

The export NF-e **was issued by Black King on 2026-09-22**. DANFE archived: `brazil/sources/2026-09-22_black_king_nfe_16_danfe.pdf`.

| Field | Value |
|-------|-------|
| NF-e number / série | **16 / série 1** |
| Chave de acesso | `2926 0950 0425 8500 0180 5500 1000 0000 0161 3000 0003 5` (44 digits, checks out) |
| Protocolo de autorização | `129261913151752` · emissão **22/09/2026** |
| Emitente | **Matheus Reis Pereira** — CNPJ 50.042.585/0001-80 · **IE 205055715** · Av. Tancredo Neves, 4900, Ilhéus-BA 45655-650 |
| Destinatário | **TrueTech Inc** — 1423 Hayes St, Hayes Valley, San Francisco CA 94117 · município *Exterior*, UF `EX` |
| Natureza da operação | **Exportação** · CFOP **7102** on every line · CST 0300 |
| Total | **R$ 35.828,76** → **US$ 6.946,85** @ PTAX 5,1575 |
| Frete / seguro / desconto | R$ 0,00 (frete por conta do **emitente**, 0) |
| Simples Nacional | “ME/EPP optante pelo Simples — não gera direito a crédito de ICMS/ISS/IPI” |

**Line-by-line vs. Rev 12 (R$ @ 5,1575):** all **11 lines present in order**, with the **NCMs and the TON/KG remap matching §5.1a exactly** — the uTrib fix is confirmed applied (1801/1803/1804 → TON; 2106.90.00 → KG). Line R$ totals differ from Rev 12 by **≤ R$ 0,81 per line** (rounding of BRL-unit values), summing to **R$ 35.828,76 vs R$ 35.828,38** on the invoice — a **R$ 0,38** difference.

**Two fields on the DANFE are still BLANK** and matter operationally:
1. **TRANSPORTADOR / VOLUMES TRANSPORTADOS** — razão social, placa, CNPJ, **quantidade, espécie, peso bruto, peso líquido** all empty. ⚠️ This is almost certainly what SeaCoast (**Daniel**) means by *“without the weights, quantity and package type”* — see Phase 5.
2. **Destinatário CEP** printed as `00000-000` (a foreign-address placeholder).

> ⚠️ **Value caveat (unchanged):** the declared TON quantities are the mechanical kg→t conversion (§5.1a). The NF-e is issued on those; any deviation from the *weighed* shipment is corrected downstream (DU-E / CC-e), not by silent edits here.

> ✅ **This closes two former 🔴 blockers in §1:** *IE / SEFAZ-BA* (IE 205055715 is real and printed) and *NF-e issued*. **DU-E** is now unblocked.

## 6. Hard rules & approval gates (checklist)

- [ ] **No NF-e issuance without Gary's explicit approval.**
- [ ] **DAO money = Nov-2024 obligations only**; comprovantes must not show pre-Nov-2024.
- [ ] **NF-e in BRL**; PTAX date declared; official BACEN rate.
- [ ] **Do not issue until CNPJ is Ativa, IE active, SEFAZ NF-e credentialed.**
- [ ] **Never put Próspera on the customs-layer documents.**
- [ ] **No production deploys / no money moves without an explicit governor command.**

---

## 7. Cost model (June 2026 quote — verify before booking)

| Item | BRL | USD est. |
|------|-----|----------|
| Road Ilhéus → Salvador | 6,615.00 + 0.15% ad-valorem | — |
| 3 pallets | 195.00 | — |
| Fumigation (3 pallets) | 500.00 | — |
| Air freight (tiered) | — | $3.20–3.50/kg |
| Export documentation | — | $95.00 |
| Brazil airport charges | — | $0.30/kg (min $250) |
| US airline terminal | — | $212.50 |
| US import handling | — | $125.00 |
| US customs clearance | — | $150.00 |
| FDA processing (if req.) | — | $100.00 |
| MPF (0.3464%) | — | $33.58–651.50 |
| Freight-only total (approx, excl. payload) | — | ≈ **$3,550** |

---

## 8. Failure modes & troubleshooting

| Symptom | Cause | Action |
|---------|-------|--------|
| CNPJ shows **Inapto** | missed declarations | settle DARF; verify status; blocks ALL issuance |
| NF-e emitter rejects product value | FX not updated | re-key BRL values for the current PTAX date (no auto-FX) |
| "Exportação" missing in operation type | first-time exporter | call SEFAZ-BA support (they enable the export profile) |
| "IE não encontrada" | IE propagation delay | wait up to 24h |
| Foreign buyer not found | not registered | add **TrueTech Inc** with **Exterior** flag (already done) |
| DARF for **all** debits can't be future-dated | system limitation | regenerate the DARF on the payment day |
| Matheus can't make outbound calls | number flagged | use WhatsApp; Rebecca for warehouse |
| NF-e rejected: **unidades de medida** | NCM technical norm requires specific units on export (NCM 1801/1803/1804 → **TON**; 1802/1806 → KG — **Appendix E**) | regenerate the invoice (Rev 12) with NCM-required units (§5.1a) + correct values; re-key emitter products |

---

## Appendix A — Export NF-e enablement & issuance SOP

> **Situation:** Black King (CNPJ 50.042.585/0001-80, Ilhéus BA) needs modelo-55 NF-e for export (DU-E requires it; **NFA-e is not accepted**). NF-e needs an **IE**, which needs a **commerce CNAE** — and per Saymon (2026-09-18) the route now runs through a **Junta Comercial contract amendment** and a **Prefeitura update/municipal licence** before the IE/tax guides. **Confirm the exact path with Saymon** (see §5 Phase 0 open question) rather than assuming the old e-CAC-only path.
>
> **Bilingual self-service guide (older):** `exports/2026-06-16_export_nfe_enablement_black_king_self_service_guide.pdf`.

**NF-e emission basics (once enabled):**

| Field | Value |
|-------|-------|
| Operation type | Exportação (código 6.501) |
| Model | **55** |
| CFOP | **7.101** (produção própria) / **7.102** (revenda) |
| Emitente | Black King — CNPJ 50.042.585/0001-80; IE **[assigned in Phase 0]**; Av. Tancredo Neves, 4900, Qd H, Cs 9, Ilhéus, BA, 45655-650 |
| Destinatário | **TrueTech Inc** — Exterior; país EUA (2496); EIN 88-3411514; 1423 Hayes St, San Francisco, CA 94117 |
| ICMS / IPI | **Isento** |
| PIS/COFINS | **Suspensão** (export regime) |
| Currency | **BRL** @ declared PTAX date |

**Deliver:** XML + DANFE to Graziela (Graziela@5cl.rs), Isis, Ana, Iolanda; Omega PIX details to Gary.

---

## Appendix B — Coopercabruca fallback route

| Field | Value |
|-------|-------|
| Entity | COOPERATIVA DOS CACAUICULTORES DO SUL DA BAHIA — COOPERCABRUCA |
| CNPJ | 31.948.811/0001-42 |
| CNAE | 10.93-7-01 |
| Location | Travessa Belo Horizonte, 166, Pontalzinho, Itabuna, BA, 45603-070 |
| Contact | coopercabruca@gmail.com · +55 73 9138-8884 |
| FDA FSVP | VALID — FDA FFR 17660066140 |
| Prior export | 100 kg cacao SSA→SFO, Nov 2023 (Omega) |

**Mechanism — exportação indireta:** (1) Black King domestic NF-e to Coopercabruca (CFOP 5501/6501, "remessa com fim específico de exportação"); (2) Coopercabruca issues the export NF-e to TrueTech (CFOP 7101/7102); (3) Coopercabruca handles DU-E + despacho; (4) ship from Itabuna. Edge: adds an intermediary + margin; export NF-e carries Coopercabruca's CNPJ.

---

## Appendix C — Triangular trade documentation (two-layer flow)

> Context: Próspera ZEDE structure — Brazilian Export Partner → TrueSight DAO LLC (Próspera) → TrueTech Inc (US) → retailers.

**Layer 1 — Brazilian customs (NF-e + DU-E + customs commercial invoice).** All show the physical destination: **Black King → TrueTech Inc**. The Próspera intermediary is invisible to Brazilian customs.

**Layer 2 — Tax/transfer pricing.**
```
Black King (BR)      → TrueSight DAO LLC (Próspera, HN)   cost + small margin (arm's-length)
TrueSight DAO LLC    → TrueTech Inc (US)                  wholesale price
TrueTech Inc         → Retailers                          wholesale/retail
```
Profit booked at the Próspera layer (1% flat tax, ZEDE regime).

**FDA/FSVP:** Black King / Coopercabruca / CEPOTX = food facilities (FFR + DUNS); TrueTech Inc = US FSVP + CBP importer of record; **Próspera = none** (never touches product).

**Key principle:** Brazil customs sees *Black King → TrueTech*; tax authorities see *Black King → Próspera → TrueTech*; FDA sees *Black King (facility) → TrueTech (importer)*. **Never put Próspera on the customs-layer docs.**

---

## Appendix D — Change log

| Date | Change |
|------|--------|
| 2026-09-21 | Full rewrite into end-to-end operator runbook (agent + Envoy contract). Corrected stale Phase 0 (e-CNPJ now works; CNAE path superseded by Junta/Prefeitura chain; Inapto has DARF mechanics). Added: municipal-licence chain, Gary NF-e approval gate, BRL/PTAX rule, Sebrae master-data sequence, treasury/audit rule, Saymon & Jussileide contacts, Phases 0–8, failure modes. Source notes: `brazil/sources/2026-09-21_black_king_accountant_thread_notes.md`. |
| 2026-09-21 | **Rev 12 regenerated + merged** (PR #1333): commercial invoice + packing list re-expressed in the NCM-mandated export units (1801/1803/1804/1805 → TON; 1802/1806 → KG), USD/BRL values unchanged; reproducible generator `scripts/build_black_king_export_docs.py` added. §5.1 current-revision pointer moved to Rev 12; Rev 11 marked superseded. |
| 2026-09-21 | Added **Appendix E** (NCM → export uTrib norm table, supplied by Gary) + **§5.1a Rev-12 unit remap** (1801/1803/1804 → TON); §1/§8 NF-e rows now point at the concrete fix. |
| 2026-09-21 | **Rev 12 finalized** (PR #1335, `f7acdff`): removed the red DRAFT banner + all draft/hedge wording from both PDFs; generator + both PDFs merged. Units and USD/BRL values unchanged. *Attribution: the packing-list-consistency confirmation — that the PL already follows Saymon's norm by construction (same generator, shared `LINES`/`UTRIB` table) — came from **Envoy**, not governor Gary Teh, and is **not** a governor authorization.* |
| 2026-09-29 | **Ordem de coleta REV 2** — the trucking pickup order rebuilt keyed to the issued **NF-e nº 16** (Gary, thread 10800): new NF-e identification block (chave/protocolo/emitente IE/CFOP/total), fiscal uTrib column beside commercial units, and the **filled** TRANSPORTADOR/VOLUMES block (2 vol · 344,06 kg net · 364,06 kg gross) that the DANFE left blank. Fixed an SSOT gap (NCM 2106.90.00 lines 6/10 printed `None` as the fiscal unit → now resolved to **KG**, matching the DANFE). Regenerated the PDF. |
| 2026-09-29 | **NF-e nº 16 recorded as issued** (22/09/2026, chave `2926…0035`, R$ 35.828,76) — reconciled line-by-line vs. Rev 12 (§5.3); DANFE archived to `brazil/sources/`. Flipped §1 *IE/SEFAZ-BA* and *NF-e issued* 🔴→✅, unblocked DU-E; noted the **blank TRANSPORTADOR/VOLUMES block** (the weights/qty/package-type gap); corrected the now-stale “no NF-e issued” wording in the Correction Letter + ordem de coleta generators (regenerated both PDFs). |
| 2026-09-29 | **NF-e nº 16 XML archived + reconciled** (SeaCoast-requested; Gary, thread 10800) — signed/authorized XML saved to `brazil/sources/2026-09-22_black_king_nfe_16.xml`; line-by-line match vs Rev 12 PL (fiscal sum **344,00 kg** vs PL commercial 344,06 kg — 3-decimal TON rounding); confirmed the XML `<transp>` is **empty except `modFrete=1` (FOB)** — the same blank the ordem de coleta REV 3 fills. Notes: `brazil/sources/2026-09-22_black_king_nfe_16_xml_reconciliation.md`. |
| 2026-09-21 | **Saymon/Jussileide are NOT on Telegram** — they are contractors on WhatsApp “Black King - Contab”. Added a delivery-channel warning to §2 so no agent assumes a thread-10800 post reaches them; artifacts for the accountant are relayed by Gary. No automated path (“Black King - Contab” is not in OpenClaw's verified JID list). |
| 2026-10-01 | **DU-E confirmed ON HOLD — CNPJ non-compliance (Omega).** Cargo already at **Salvador airport**; Omega filed a formal **RFB inquiry** into the CNPJ *admissibility* failure. Corrected three §1 rows (DU-E 🟡→🔴 ON HOLD · CNPJ 🟡→🔴 BLOCKING · SISCOMEX/RADAR ✅→🟡 representante link failing) and bumped `Last verified`. Added source note `brazil/sources/2026-10-01_omega_export_hold_cnpj_notice.md`. Flagged that the two faults (CNPJ/habilitação vs. SISCOMEX representante) are **distinct**. Docs-only. |

---

## Appendix E — NCM → export unit of measure (uTrib) reference

> Source: NCM/uTrib norm table supplied by Gary **2026-09-21** (transcribed to `brazil/sources/2026-09-21_black_king_accountant_thread_notes.md` §8). This is the *norma técnica* Saymon cited as the cause of the Rev 11 NF-e rejection. Applies to **Chapter 18 (cocoa)** headings on **export** operations. Raw/intermediate forms → **TON**; husks + finished preparations → **KG**.

| NCM | uTrib (export) | Description | Rev-11 lines |
|-----|----------------|-------------|-------------|
| 1801.00.00 | **TON** | Tonelada Métrica Líquida | #1, #4, #5, #8, #9 |
| 1802.00.00 | **KG** | Quilograma | — (see #2 flag) |
| 1803.10.00 | **TON** | Tonelada Métrica Líquida | #2, #3, #7 |
| 1803.20.00 | **TON** | Tonelada Métrica Líquida | — |
| 1804.00.00 | **TON** | Tonelada Métrica Líquida | #11 |
| 1805.00.00 | **TON** | Tonelada Métrica Líquida | — |
| 1806.10.00 | **KG** | Quilograma | — |
| 1806.20.00 | **KG** | Quilograma | — |
| 1806.31.10 / 1806.31.20 | **KG** | Quilograma | — |
| 1806.32.10 / 1806.32.20 | **KG** | Quilograma | — |
| 1806.90.00 | **KG** | Quilograma | — |

**Not covered by this table (confirm with Saymon):** NCM **2106.90.00** (Rev-11 lines #6, #10 — Cacao Tea) is outside Chapter 18; confirm its export uTrib independently.

---

## Related documents

- `SUPPLY_CHAIN_AND_FREIGHTING.md` — freight cost logic, unit economics
- `CONSIGNMENT_OPTIMAL_QUANTITY_PROPOSAL.md` — bag quantities / inventory
- `LEDGER_CONVERSION_AND_REPACKAGING.md` — repackaging / bag conversion
- `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md` — consolidated Jun–Aug 2026 learnings
- `brazil/BRAZIL_EXPORT_ENTITY_BRIEF.md` — legal structuring (Próspera LLC)
- `PROSPERA_ENTITY_OPERATING_AGREEMENT.md` — Próspera ZEDE operating agreement (Art. XI)
- `fda_fsvp/suppliers/black_king/entity.json`, `fda_fsvp/suppliers/coopercabruca/entity.json`, `fda_fsvp/truetech_inc.entity.json`
