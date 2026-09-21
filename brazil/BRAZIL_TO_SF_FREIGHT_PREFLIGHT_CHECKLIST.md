# Brazil → San Francisco Freight Lane — End-to-End Runbook

> **Audience:** AI agents (Sophia / any autopilot instance), LLMs, and human **Envoys** operating the DAO's Brazil export lane.
> **Canonical file.** If any other document disagrees with this one, **this file wins** — fix the other doc in the same PR.
> **Lane:** Ilhéus, BA (Matheus / Gateway.fy warehouse) → road → Salvador (SSA) → air → San Francisco (SFO) → Kirsten's SF warehouse.
> **Commercial basis:** Brazil exporter (Black King, or fallback Coopercabruca) → **TrueTech Inc** (US importer of record, EIN 88-3411514).
> **Last verified:** 2026-09-21. Sources: Seacos/Omega quote thread (May–Jun 2026); Black King accountant WhatsApp thread (2026-09-18 → 21) — see `brazil/sources/2026-09-21_black_king_accountant_thread_notes.md`.

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

## 1. Status snapshot (2026-09-21)

| Gate | Status | Owner | Notes |
|------|--------|-------|-------|
| SISCOMEX / RADAR (brokers registered) | ✅ done (Jun 2026) | Matheus | 3 Omega brokers registered |
| Omega PoA signed | ✅ done (Jun 2026) | Matheus | Omega can act on the export |
| NCM 1801.00.00 confirmed | ✅ | Omega | no MAPA needed for US |
| **CNPJ regularization (exit Inapto)** | 🟡 in progress | Saymon/Jussileide + Gary | DARF **NOV.2024–JUL.2026** issued & DAO portion paid; **2023 MEI-era guia** pending |
| **e-CNPJ certificate** | ✅ works | Matheus | cert usable via gov.br (no longer the blocker) |
| **Commerce CNAE / IE / SEFAZ-BA** | 🔴 blocked | Saymon | needs **Junta Comercial** contract amendment → Prefeitura update |
| **Municipal licence (licença comercial)** | 🔴 pending | Saymon/Jussileide | needed for the cacao business; not in old doc |
| **NF-e draft** | 🟠 **errored** | Saymon | draft attempted 2026-09-21 → emitter rejected: **incorrect unidades de medida** for NCM 1801/1803/1804 on export (norm table: **Appendix E**) → re-express those lines in **TON** for Rev 12 (§5.1a) |
| **NF-e issued** | 🔴 **not yet** | Saymon | blocked on a corrected invoice (**Rev 12**) with NCM-required export units + values — unit remap in §5.1a; norm source **Appendix E** |
| DU-E (Notificação de Exportação Fiscal) | ⬜ not started | Omega | blocked on NF-e |
| Cargo prep / pallets | ⬜ | Matheus | heat-treated pallets being sourced |
| Air freight | ⬜ | Graziela/Omega | rates only |
| Deadline pressure | — | — | **China partners arrive 2026-09-29** (Gary asked to resolve before then) |

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
| Origin warehouse / cargo | Matheus Reis (Black King, EI) | Gateway.fy | theus.reis.ssa@gmail.com · WA +55 11 91413-5328 · +55 73 99109-0002 |
| Ilhéus warehouse (physical) | Rebecca | — | +55 73 99108-2946 |
| **NF-e specialist (hired)** | **Saymon** | (contractor) | WhatsApp group "Black King - Contab" |
| **Accountant (hired)** | **Jussileide** | (contractor) | WhatsApp group "Black King - Contab" |
| US importer of record | TrueTech Inc | — | EIN 88-3411514 · 1423 Hayes St, San Francisco, CA 94117 |

> **Note:** the old doc said "bypass the accountant; 8 days". **Accountants have now been hired (Saymon + Jussileide)** and the lane is still not through — the bottleneck is the **structural (Junta/Prefeitura)** chain and the **master-data setup**, not the accountant's responsiveness.

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
- [ ] **PoA / procuração.** Note: Jussileide (2026-09-18) says the **carta de procuração is to be done at the cartório** directly.

### Phase 1 — FX & commercial documents
- [ ] Commercial invoice + packing list present, **dual USD+BRL**, dated, with **declared PTAX date**.
- [ ] Current revision pointer pinned below (see §5.1). Evidence: PDFs in `exports/`.

### Phase 2 — NF-e draft & Gary-approval gate
- [ ] **Draft NF-e prepared** in the Sebrae emitter (master data see §5.2). Owner: Saymon.
- [ ] **🛑 Gary approves the draft** (hard gate §0.2). Evidence: approval message in thread 10800.
- [ ] **NF-e issued** (modelo 55, CFOP 7.101/7.102, exportação). Evidence: XML + DANFE.
- [ ] XML + DANFE sent to Graziela/Omega; Omega PIX details to Gary.

### Phase 3 — Cargo prep at origin (Ilhéus)
- [ ] Cargo photos shared. Owner: Matheus.
- [ ] **ISPM#15 pallet compliance:** fumigated or heat-treated, **IPPC stamp legible on all sides**, original Phytosanitary Certificate to accompany docs.
- [ ] Packing arranged at Matheus's Ilhéus warehouse.

### Phase 4 — Inland transport (Ilhéus → Salvador)
- [ ] Road transport booked. Cost: **BRL 6,615.00 + 0.15% ad-valorem** (with Salvador palletization); **BRL 7,290.00 + 0.15%** without.
- [ ] Collection scheduled by Omega (pickup at Matheus's warehouse).

### Phase 5 — Airport & export processing (Salvador)
- [ ] Palletization + fumigation at Salvador (if not at origin): **BRL 195 (3 pallets) + BRL 500 (fumigation) = BRL 695**.
- [ ] Airline booking confirmed + quote revalidated (Graziela).
- [ ] **Export docs:** AWB, Commercial Invoice, Packing List, Phytosanitary Cert (pallets), IPPC details.
- [ ] **DU-E registered** (Notificação de Exportação Fiscal). Owner: Omega.
- [ ] **Desembaraço de exportação** (Gerson Argolo).

### Phase 6 — Air freight (SSA → SFO)
- [ ] Air freight booked. Tiered: 200 kg ≈ $3.50/kg · 300 kg ≈ $3.40 · 500 kg ≈ $3.30 · 750 kg ≈ $3.30 · 1000 kg ≈ $3.20.
- [ ] Brazil airport charges: ≈ $0.30/kg (min $250). US airline terminal ≈ $212.50.
- [ ] Gross ≈ 320 kg / net ≈ 300 kg (per Rev 11 packing list).

### Phase 7 — US import, customs & final delivery
- [ ] US import handling ≈ $125. US customs clearance ≈ $150. FDA processing ≈ $100 (if required).
- [ ] Bond (single-entry, if req.): max($100, $6 per $1,000 of value+duty). MPF 0.3464% (min $33.58, max $651.50). Duty if applicable. Customs exam ≈ $250 (random).
- [ ] Delivery SFO → **Kirsten's SF warehouse**.

### Phase 8 — Ledger & reporting (DAO)
- [ ] Record the **`[INVENTORY MOVEMENT]`** for the shipment once the destination ledger name is confirmed.
- [ ] File the **contribution event(s)** for the round (with PR/evidence links).
- [ ] Update this runbook's status snapshot (§1).

#### 5.1 Current commercial revision
- **Invoice INV-2026-0611-001 Rev 11 (+BRL)**, dated 2026-09-21, **$6,946.85 USD / R$ 35,828.38 BRL** @ PTAX 5.1575 (18/09/2026). Files: `exports/2026-06-11_commercial_invoice_black_king_to_truetech_rev11_EN_PT_BRL.pdf` (and the dated `inv_rev11_brl_dated.pdf`). Packing list `PL-2026-0611-001 Rev 11`.
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

> ⚠️ **Rev 12 required (2026-09-21).** The NF-e draft errored on **unidades de medida**: a technical norm (*norma técnica*) mandates specific units of measure for some NCMs in case of export. Saymon: *“deverá ser gerada outra invoice com as unidades de medida e os valores corretos.”* → regenerate the commercial invoice with the **correct units + values** before the NF-e can be issued. Rev 11's mixed **UN / KG** units must be re-mapped to what each NCM requires.

#### 5.1a Rev 12 — required export units (NCM remap)

> Source: NCM→uTrib export-unit norm table supplied by Gary 2026-09-21 (**Appendix E**). Chapter-18 raw/intermediate forms (**1801 beans/nibs, 1803 paste/mass, 1804 butter/fat**) must be declared in **TON** (tonelada métrica líquida); 1802 (husks) and finished 1806* use **KG**. Rev 11 declared the 1801/1803/1804 lines in **UN / KG** → this is the rejection.

| # | NCM | Rev-11 qty | Rev-11 unit | Rev-12 required unit | Rev-12 qty (≈ t, see caveat) |
|---|-----|-----------|-------------|----------------------|------------------------------|
| 1 | 1801.00.00 | 129 | UN | **TON** | ≈ 0.0293 |
| 2 | 1803.10.00 | 20 | KG | **TON** *(or 1802→KG — confirm)* | 0.0200 |
| 3 | 1803.10.00 | 37 | UN | **TON** | ≈ 0.0185 |
| 4 | 1801.00.00 | 80 | KG | **TON** | 0.0800 |
| 5 | 1801.00.00 | 10 | KG | **TON** | 0.0100 |
| 6 | 2106.90.00 | 12 | KG | *(confirm — not Ch.18)* | — |
| 7 | 1803.10.00 | 169 | UN | **TON** | ≈ 0.0338 |
| 8 | 1801.00.00 | 15 | KG | **TON** | 0.0150 |
| 9 | 1801.00.00 | 99.5 | KG | **TON** | 0.0995 |
| 10 | 2106.90.00 | 21 | KG | *(confirm — not Ch.18)* | — |
| 11 | 1804.00.00 | 5 | KG | **TON** | 0.0050 |

> ⚠️ The ≈ t column is a **mechanical kg→t / unit-weight conversion only** (8 oz pouch = 0.2268 kg; 500 g = 0.5 kg; 200 g = 0.2 kg) and is **illustrative** — Saymon to confirm the actually-declared quantities and the values on Rev 12.
> ⚠️ **Flag (line #2):** "Cacao Husk" is normally NCM **1802.00.00** (uTrib **KG**), not 1803.10.00 (uTrib TON). If it truly is 1802 it stays KG — confirm the correct NCM with Saymon rather than blanket-converting.
> ⚠️ **Flag (#6/#10):** NCM **2106.90.00** (Cacao Tea) is outside Chapter 18 and is **not keyed** by this table — confirm its export uTrib independently.

#### 5.2 Sebrae emitter — master-data sequence (in order)
1. **Register the company as emitente** (Saymon, in progress). Black King **already had an account** (Matheus used it before). Login: `https://emissornfe.sebrae.com.br/` → **gov.br** → *Seu Certificado Digital* → Black King cert (shows as Matheus) → select Black King.
2. **Register products.**
3. **Register clients** — **TrueTech Inc already registered.**
4. **Register suppliers (fornecedores).**
5. **Then issue** the export NF-e (CFOP 7.101/7.102).
- Emitter alternatives if needed: SEFAZ-BA web emitter (free); national free emitter for BA.

---

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
| 2026-09-21 | Added **Appendix E** (NCM → export uTrib norm table, supplied by Gary) + **§5.1a Rev-12 unit remap** (1801/1803/1804 → TON); §1/§8 NF-e rows now point at the concrete fix. |

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
