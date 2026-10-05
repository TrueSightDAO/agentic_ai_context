# Brazil → San Francisco Freight Lane — End-to-End Runbook

> **Audience:** AI agents (Sophia / any autopilot instance), LLMs, and human **Envoys** operating the DAO's Brazil export lane.
> **Canonical file.** If any other document disagrees with this one, **this file wins** — fix the other doc in the same PR.
> **Lane:** Ilhéus, BA (Matheus / Gateway.fy warehouse — **physical pickup: R. Cel. Paiva, 46, Centro**) → road → Salvador (SSA) → air → San Francisco (SFO) → Kirsten's SF warehouse.
> **Commercial basis:** Brazil exporter (Black King, or fallback Coopercabruca) → **TrueTech Inc** (US importer of record, EIN 88-3411514).
> **Last verified:** 2026-10-02 (FDA Prior Notice gate, §5.6). Sources: Seacos/Omega quote thread (May–Jun 2026); Black King accountant WhatsApp thread (2026-09-18 → 21) — see `brazil/sources/2026-09-21_black_king_accountant_thread_notes.md`; **Ilhéus pickup-address confirmation — Gary, thread 10800, 2026-09-29** (see §2a); **NF-e nº 16 issued 2026-09-22** — DANFE + notes at `brazil/sources/2026-09-22_black_king_nfe_16_danfe.pdf` ; **NF-e nº 18 issued 2026-10-02** — `brazil/sources/2026-10-02_black_king_nfe_18_danfe.pdf`; **SISCOMEX habilitação dropped on 6-month inactivity — Iolanda (Omega) via Gary, 2026-10-02** (§5.4). **Airport weighing — gross-weight divergence (349 kg, DU-E ref `26BR0017954000`), 2026-10-02** — `brazil/sources/2026-10-02_airport_weighing_weight_divergence.md` (§5.5).

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
| SISCOMEX / RADAR (brokers registered) | ✅ done (Jun 2026) | Matheus | 3 Omega brokers registered — primary source: `brazil/sources/2026-05-18_omega_siscomex_representante_tutorial_notes.md` |
| Omega PoA signed | ✅ done (Jun 2026) | Matheus | Omega (forwarder) can act on the export — **distinct** from the e-CAC/cartório procuração in §5 Phase 0 |
| NCM 1801.00.00 confirmed | ✅ | Omega | no MAPA needed for US |
| **CNPJ regularization (exit Inapto)** | 🟡 in progress | Saymon/Jussileide + Gary | DARF **NOV.2024–JUL.2026** issued & DAO portion paid; **2023 MEI-era guia** pending |
| **e-CNPJ certificate** | ✅ works | Matheus | cert usable via gov.br (no longer the blocker) |
| **Commerce CNAE / IE / SEFAZ-BA** | ✅ **IE active** | Saymon | **IE 205055715 now printed on the DANFE** (NF-e nº 16) — IE/SEFAZ-BA credentialing evidently completed. Formerly flagged as *unreconciled* (order nº 003625 carried an IE the runbook said did not exist); the DANFE confirms it is real. |
| **Municipal licence (licença comercial)** | 🔴 pending | Saymon/Jussileide | needed for the cacao business; not in old doc |
| **NF-e draft** | ✅ **superseded** | Saymon | draft errored 2026-09-21 on **unidades de medida**; fixed by the Rev 12 unit remap (§5.1a). **Now moot — the NF-e was issued (see next row).** |
| **NF-e issued** | ✅ **issued** | Saymon | **NF-e nº 16, série 1, emitida 22/09/2026** — chave `2926 0950 0425 8500 0180 5500 1000 0000 0161 3000 0003 5`, protocolo `129261913151752`, **R$ 35.828,76**. All 11 lines, NCMs and the TON/KG remap match Rev 12 (§5.3). Evidence: DANFE — `brazil/sources/2026-09-22_black_king_nfe_16_danfe.pdf`; signed **XML** — `brazil/sources/2026-09-22_black_king_nfe_16.xml` (+ reconciliation notes `brazil/sources/2026-09-22_black_king_nfe_16_xml_reconciliation.md`). XML `cStat` **100 (Autorizado)**. |
| **NF-e issued (CURRENT)** | ✅ **issued** | Saymon/Matheus | **NF-e nº 18, série 1, emitida 02/10/2026** — chave `2926 1050 0425 8500 0180 5500 1000 0000 0181 3000 0000 56`, protocolo `129261914544464`, **R$ 33.384,57**. **9 lines — matches Rev 14 line-for-line** (§5.3b). Evidence: DANFE — `brazil/sources/2026-10-02_black_king_nfe_18_danfe.pdf`. **Supersedes nº 16** (11 lines / R$ 35.828,76), issued on the superseded Rev-12 cargo. |
| **SISCOMEX/RADAR habilitação (DU-E prerequisite)** | 🔴 **BLOCKED → being restored** | Iolanda (Omega) → Saymon | ⚠️ Per **Iolanda Santos** (Omega, SISCOMEX/customs) to Gary, 2026-10-02: **6 months with no SISCOMEX movements** → the RADAR habilitação was **dropped by default** (*por padrão*), so Black King is currently **not habilitado** and the DU-E cannot be registered. Iolanda must run an **update** but **her laptop broke and her A1 digital certificate only works on a laptop**; she gave the **step-by-step to Saymon**, who is executing it and will send her a **print** for confirmation. Detail + standing risk: **§5.4** and `brazil/sources/2026-10-02_siscomex_habilitacao_inactivity_notes.md`. |
| DU-E (Notificação de Exportação Fiscal) | ✅ **REGISTERED** | Omega | **DU-E `26BR001795400-0`** printed on the issued AWB (§5.7) — the habilitação blocker (§5.4) is evidently cleared. |
| **Airport weighing (Salvador) — gross weight** | ✅ **CLOSED** | Omega / airline | AWB **`047-3175 3223`** confirms **gross 349,000 kg** — **matches Rev 15**. No further reissue. (§5.5 / §5.7). |
| **FDA Prior Notice (US import)** | ⬜ **AWB in hand — awaiting arrival date** | Iolanda (Omega) | **Mandatory** US food-import filing. Cite AWB **`047-3175-3223`**; only the flight **arrival date** is still needed for the §5.6 timing window. |
| Cargo prep / pallets | ������ | Matheus | ⚠️ **contradiction (flagged 2026-10-02):** this row said *heat-treated* pallets, but the export-doc generator (§5.5, `pallets_html`) declares **plastic HDPE (Huatai), non-wood → ISPM#15 N/A, no fumigation**. The flight evidence (`349 kg` weighed) is consistent with the **plastic** pallets. Confirm with Matheus and retire whichever is wrong. |
| Air freight | ✅ **booked — TP028** | Graziela/Omega | **TAP `TP028`** SSA→SFO. **HAWB + MAWB both issued** (`047-3175-3223`), **executed 05/OCT/2026**; a **consolidation** (MAWB consignee = 5 Continent Logistics LLC). See §5.7 / §5.8. |
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
| US importer of record | TrueTech Inc | — | EIN 88-3411514 · 1423 Hayes St, San Francisco, CA 94117 · **WhatsApp +1 442 340-5782** (`wa.me/+14423405782`, supplied by Gary 2026-10-02) — this is the **FONE/FAX `(14) 42340-5782` printed in the DESTINATÁRIO block on NF-e nº 18**. |

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
  - ⚠️ **If the pallets are plastic HDPE (per §5.5 / the §1 row), ISPM#15 is NOT APPLICABLE** (non-wood is exempt) and no phytosanitary cert is required. Reconcile the pallet material first — do not buy a fumigation cert for an exempt pallet.
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
- [x] **Airport weighing — 349,000 kg gross** (§5.5): Commercial Invoice + Packing List **reissued at gross 349 kg** (**Rev 15**, `exports/2026-10-02_*_rev15_*`). ⬜ SeaCoast reissues **HAWB/MAWB**; ⬜ **CC-e** on NF-e nº 18 to align the declared bruto (322,06 → 349). Owner: Gary → Omega.
- [x] **Air waybill issued** — **`047-3175-3223`**, SSA→SFO on **TP028**, gross **349,000 kg** == Rev 15; DU-E `26BR001795400-0` (§5.7). **MAWB issued 05/OCT/2026** (consolidated; consignee 5 Continent Logistics LLC) (§5.8). Flight **arrival date** pending. ⚠ Confirm the HAWB-vs-MAWB charge difference (~USD 800) with Graziela/Omega.
- [ ] **Send the air waybill (AWB) to Iolanda (Omega)** once SeaCoast reissues it — she needs it to **file the FDA Prior Notice** (§5.6).
- [ ] **Desembaraço de exportação** (Gerson Argolo).
- [ ] **Correction Letter to SeaCoast** (freight forwarder) — Daniel flagged that the issued invoice lacked **weights, quantity and package type**. Draft: `exports/2026-09-29_correction_letter_black_king_inv_rev12_EN_PT.pdf` (generated by `scripts/build_correction_letter.py` from the Rev 12 SSOT; carries a **Portuguese pickup section** — where to collect + what is collected — for the Brazilian warehouse/carrier). ⚠️ This is a **commercial** companion to NF-e nº 16 (issued 2026-09-22), **not** a fiscal **CC-e**; the DANFE's own TRANSPORTADOR/VOLUMES block is **blank** — the weights/quantity/package-type Daniel flagged — so a commercial letter (or a CC-e, once the carrier data exists) is what closes it. Owner: Gary → Black King signs → SeaCoast.

### Phase 6 — Air freight (SSA → SFO)
- [ ] Air freight booked. Tiered: 200 kg ≈ $3.50/kg · 300 kg ≈ $3.40 · 500 kg ≈ $3.30 · 750 kg ≈ $3.30 · 1000 kg ≈ $3.20.
- [ ] Brazil airport charges: ≈ $0.30/kg (min $250). US airline terminal ≈ $212.50.
- [x] **Weights:** **Rev 15 = net 302,06 / gross 349,00 kg** (as weighed at Salvador) — the CI + PL now carry this. *Superseded:* Rev 14 gross 322,06; Rev 12 net 344.06 / gross 364.06; Rev 11 ≈ 300 / 320.

### Phase 7 — US import, customs & final delivery
- [ ] US import handling ≈ $125. US customs clearance ≈ $150. **FDA Prior Notice — required, not optional** (§5.6): Iolanda files it once the AWB is in hand; ≥ 4 h before arrival by air, ≤ 15 days ahead via PNSI. FDA processing ≈ $100.
- [ ] Bond (single-entry, if req.): max($100, $6 per $1,000 of value+duty). MPF 0.3464% (min $33.58, max $651.50). Duty if applicable. Customs exam ≈ $250 (random).
- [ ] Delivery SFO → **Kirsten's SF warehouse**.

### Phase 8 — Ledger & reporting (DAO)
- [ ] Record the **`[INVENTORY MOVEMENT]`** for the shipment once the destination ledger name is confirmed.
- [ ] File the **contribution event(s)** for the round (with PR/evidence links).
- [ ] Update this runbook's status snapshot (§1).

#### 5.1 Current commercial revision
- 🚨 **SUPERSEDED 2026-10-02 → see §5.1b (Rev 13).** The physical cargo changed (Rev-12 lines 6 + 8 dropped, 5 kg Pará samples added); Rev 13 = **10 lines, 28 boxes, 322.06 kg net / 342.06 kg gross, $6,828.73 USD / R$ 35,219.17 BRL**. The paragraph below is kept for reconciliation history only.
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

#### 5.1b Rev 13 — superseded (2026-10-02)

> 🚨 **SUPERSEDED 2026-10-02 → see §5.1c (Rev 14).** Kept for reconciliation history.

> **Source:** governor Gary Teh, thread 10800, 2026-10-02 (physical count + corrections).

**What changed vs Rev 12:**

| Change | Rev-12 line | Boxes | Net kg | USD |
|--------|-------------|-------|--------|-----|
| **Removed** — Cacao Tea (KG) AGL8 (Paulo's) | 6 | −2 | −12.00 | −$0.12 |
| **Removed** — Cacao Almonds (KG) AGL13 (Vivi's) | 8 | −2 | −15.00 | −$118.05 |
| **Added** — Cacao Almonds **samples** (KG) — Pará | new 10 | +1 | +5.00 | +$0.05 *(nominal)* |
| **Rev 13** | **10 lines** | **28** | **322.06** | **$6,828.73** |

**Totals:** **10 lines · 28 boxes (23 regular + 5 irregular) · 2 pallets · 322.06 kg net / 342.06 kg gross · $6,828.73 USD / R$ 35,219.17 BRL** @ PTAX 5.1575 (18/09/2026).

- Files: `exports/2026-10-02_commercial_invoice_black_king_to_truetech_rev13_EN_PT_BRL.pdf`; packing list `exports/2026-10-02_packing_list_black_king_to_truetech_rev13_EN_PT.pdf`.
- Generated reproducibly by `scripts/build_black_king_export_docs.py` (merged #1482, `f782ebc`). The carton count is now carried **on the packing list itself** (previously only on the CC-e).
- **Units:** the NCM→uTrib remap from Rev 12 (§5.1a) is **unchanged** — 1801/1803/1804 → TON; 2106.90.00 → KG.
- 🚨 **Fiscal divergence:** NF-e **nº 16** (authorized 2026-09-22) was issued on the **11-line / R$ 35.828,76** Rev-12 cargo. The physical cargo is now **10 lines / R$ 35,219.17**. A CC-e cannot add/remove lines or move the tax base — the correction route must come from **Saymon/Matheus**. **Do not treat the lane as document-consistent until this is resolved.**

#### 5.1c ⭐ Rev 14 — current (physical cargo), 2026-10-02

> **Source:** governor Gary Teh, thread 10800, 2026-10-02 ("remove line 2" + full physical box breakdown).

**What changed vs Rev 13:** Rev-13 **line 2 (Cacao Husk KG — Ilheus, 20 kg, 2 regular boxes) is NOT in the shipment** — removed. **Corrected 2026-10-02:** the *Cacao Mass Bar 500g — Ilheus 2024* line ships in **two thermic boxes** (was modelled as one).

**Physical box breakdown (governor, from the warehouse):**

| Regular boxes (10 kg Mercado Livre) | Boxes |
|---|---|
| Oscar cacao nibs | 8 |
| Paulo cacao almonds (AGL8) | 1 |
| Samples from Pará (cacao almonds) | 1 |
| Vivi cacao nibs (AGL13) | 10 |
| Vivi cacao tea (AGL13) | 2 |
| **Regular total** | **22** |

| Irregular boxes | Boxes |
|---|---|
| Nibs Kraft Pouch 8oz — Ilheus 2024 *(thermic)* | 1 |
| Mass Bar 500g — Ilheus 2024 *(thermic)* | **2** |
| Ceremonial Cacao Pouch 200g — AGL8 *(thermic)* | 1 |
| Coopercabruca Cacao Butter (KG) *(irregular)* | 1 |
| **Irregular total** | **5** |

> **Box model:** Paulo's Cacao Almonds (AGL8, 10 kg) ships in a **regular 10 kg box**; the *Cacao Mass Bar 500g* ships in **2 thermic boxes**. Final: **22 regular + 5 irregular = 27 boxes**.

**Totals:** **9 lines · 27 boxes (22 regular + 5 irregular) · 2 pallets · 302.06 kg net / 322.06 kg gross · $6,473.02 USD / R$ 33,384.60 BRL** @ PTAX 5.1575 (18/09/2026).

- Files: `exports/2026-10-02_commercial_invoice_black_king_to_truetech_rev14_EN_PT_BRL.pdf`; packing list `exports/2026-10-02_packing_list_black_king_to_truetech_rev14_EN_PT.pdf`.
- Generated reproducibly by `scripts/build_black_king_export_docs.py`.
- **Units:** the NCM→uTrib remap from Rev 12 (§5.1a) is **unchanged** — 1801/1803/1804 → TON; 2106.90.00 → KG.
- ✅ **Fiscal divergence RESOLVED (2026-10-02):** NF-e **nº 18** was issued on this exact physical cargo — **9 lines, 27 caixas, 2 pallets, 302,06 kg net / 322,06 kg gross, R$ 33.384,57** — which reconciles to Rev 14 line-for-line (see §5.3b; R$ 0,03 rounding delta vs the invoice's R$ 33.384,60). NF-e **nº 16** (11 lines / R$ 35.828,76) is **superseded** and must not be presented to customs. The lane is now **document-consistent**.

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

#### 5.3b NF-e nº 18 — issued 2026-10-02 (reconciled vs. Rev 14) ⭐ CURRENT

> **Source:** DANFE `brazil/sources/2026-10-02_black_king_nfe_18_danfe.pdf` (1 page, emitida 02/10/2026), supplied by Gary in thread 10800, 2026-10-02.
> **This is the NF-e that matches the physical cargo.** Nº 16 is superseded.

| Field | Value |
|-------|-------|
| NF-e | **nº 18, série 1** |
| Chave de acesso | `2926 1050 0425 8500 0180 5500 1000 0000 0181 3000 0000 56` |
| Protocolo de autorização | `129261914544464` |
| Emitente | **Matheus Reis Pereira** — CNPJ 50.042.585/0001-80 · IE 205055715 · Av. Tancredo Neves, 4900, Nossa Senhora da Vitória, Ilhéus-BA 45655-650 |
| Destinatário | **TRUETECH INC** — 1423 Hayes St, Hayes Valley, San Francisco CA 94117 (UF **EX**, município *Exterior*) |
| Natureza da operação | **Exportação** |
| Data de emissão | **02/10/2026** |
| Total (produtos = nota) | **R$ 33.384,57** → **US$ 6.473,00** @ PTAX 5,1575 |
| ICMS / ST / IPI / PIS / COFINS / FCP | all **0,00** (exportação) |
| Simples Nacional | “ME/EPP optante pelo Simples Nacional. Não gera direito a crédito fiscal de ICMS, ISS e IPI.” |

**TRANSPORTADOR / VOLUMES TRANSPORTADOS block — NOW FILLED** (nº 16 left it blank — this is the weights/quantity/package-type Daniel of SeaCoast flagged, §5 Phase 5):

| Quantidade | Espécie | Peso bruto | Peso líquido |
|---|---|---|---|
| **2** | **PALLETS** | **322,060 kg** | **302,060 kg** |

> Informações complementares: *“Peso Liquido - 302,06 Kg; Peso Bruto - 322,06 Kg; Pallets - 2; **Caixas - 27**;”* — the carton count that was previously only on our CC-e is now **on the NF-e itself**.

**Line-by-line vs. Rev 14** — all **9 lines present**, in the emitter's product-code order (not invoice order); NCMs and the TON/KG remap match §5.1a exactly (1801/1803/1804 → TON; 2106.90.00 → KG):

| NF-e code | Description (NF-e) | NCM | uTrib | Qty (TON/KG) | ≈ kg | R$ |
|---|---|---|---|---|---|---|
| 2000000000013 | Cacao Almonds samples (KG) Pará | 18010000 | TON | 0,005 | 5 | 0,26 |
| 2000000000002 | Cacao Nibs Kraft Pouch 8oz — Ilhéus 2024 | 18010000 | TON | 0,029 | 29 | 4.418,25 |
| 2000000000004 | Cacao Mass Bar 500g — Ilhéus 2024 | 18031000 | TON | 0,018 | 18 | 2.995,89 |
| 2000000000005 | Cacao Nibs (KG) — Ilhéus 2024 | 18010000 | TON | 0,080 | 80 | 10.158,40 |
| 2000000000006 | Cacao Almonds (KG) — AGL8 | 18010000 | TON | 0,010 | 10 | 0,50 |
| 2000000000008 | Ceremonial Cacao Pouch 200g — AGL8 | 18031000 | TON | 0,034 | 34 | 9.038,12 |
| 2000000000010 | Cacao Nibs (KG) — AGL13 | 18010000 | TON | 0,100 | ≈ 99,5 | 5.223,75 |
| 2000000000011 | Cacao Tea (KG) — AGL13 | 21069090 | KG | 21,000 | 21 | 1.102,50 |
| 2000000000012 | Coopercabruca Cacao Butter (KG) | 18040000 | TON | 0,005 | 5 | 446,90 |
| | **Sum of lines** | | | | **≈ 302** | **33.384,57** |

**Reconciliation checks:**
- **9 lines** — matches Rev 14. **No husk line** (removed in Rev 14) · **no AGL8 tea / AGL13 almonds** (removed in Rev 13). ✅
- **Caixas 27** · **Pallets 2** · **net 302,06** · **gross 322,06** — all match Rev 14. ✅
- **Total R$ 33.384,57** vs Rev 14 invoice **R$ 33.384,60** — **R$ 0,03** (3-centavo rounding on BRL-unit values). ≤ the R$ 0,38 delta the nº 16 reconciliation showed. ✅
- **AGL13 nibs** declared as **0,100 TON** vs Rev 14's **99,5 kg** — the emitter rounds to 3 decimals of a tonne (0,0995 → 0,100); acceptable, and the net-weight field still reads 302,06. ✅

> ⚠️ **Not yet registered in SISCOMEX / not yet given to the carrier.** The NF-e **is** issued and authorized (protocolo present), but per §5 Phase 5 the DU-E + despacho still follow, and the driver must carry **nº 18** (not nº 16).
> ������ **Downstream updates needed:** the **ordem de coleta** (§5 Phase 4, currently keyed to nº 16 — 11 lines / 344,06 kg) and the **SeaCoast correction letter** (§5 Phase 5) are both now **stale** — they must be re-keyed to **nº 18 / Rev 14 / 302,06 kg**. The weights (302,06/322,06) and quantity (2 pallets) the SeaCoast letter asked for are now already on the NF-e itself.

#### 5.4 SISCOMEX/RADAR habilitação — the 6-month inactivity rule ⚠️ KEEP IN MIND

> **Source:** Iolanda Santos (Omega, SISCOMEX/customs) on a call with Gary, 2026-10-02 (thread 10800). Notes: `brazil/sources/2026-10-02_siscomex_habilitacao_inactivity_notes.md`.

A SISCOMEX/RADAR **habilitação is dropped by default after ~6 months with no movement** (*“por padrão”* — Iolanda). Black King went ~6 months with no SISCOMEX movement, so its habilitação was **blocked** and it cannot register the **DU-E**.

**Recovery (in progress):** the company (or its representative) runs an **update/movement** in SISCOMEX/RADAR to restore the habilitação. Iolanda wrote the **step-by-step**; **Saymon is executing it** and will send her a **print**; she then confirms.

**⚠️ Standing risk — single-certificate / single-machine.** Iolanda's **A1 certificate only works on her laptop**, which **broke** — so she could not run the update herself and the lane stalled on a hardware failure. **Keep more than one certificate-capable device + custodian for Black King.**

**Maintenance rule — going forward:** during any shipping season, **never let a habilitação idle 6 months**; log a movement (even an administrative/zero one) or diarize the expiry. Do not discover this at DU-E time.


#### 5.5 Airport weighing — gross-weight divergence (349 kg) ������ NEW 2026-10-02

> **Source:** `brazil/sources/2026-10-02_airport_weighing_weight_divergence.md` (Gary, thread 10800).

Salvador airport weighed the consignment and found a **divergence**: **gross = 349,000 kg** (`349,000` on the ticket; AWB **`04731753223`**, DOC. LIBERATÓRIO **`DUE-26BR0017954000`**, **2 volumes**, exportador **50.042.585/0001-80** ✓). Requested of us (**confirmed 2026-10-02: the ask came from Daniel / SeaCoast**, the forwarder): **reissue the Commercial Invoice + Packing List at gross 349 kg**; SeaCoast then reissues **HAWB + MAWB** for the airline correction.

**Why it differs from our docs.** Rev 14 modelled gross = net **302,06** + **20 kg pallet tare** (2 × 10 kg **plastic HDPE** pallets — *non-wood, ISPM#15 N/A*) = **322,06**. It **omitted the CARTON tare**. 349,00 − 322,06 = **26,94 kg ≈ 1 kg × 27 boxes**. So the divergence is **carton tare, not pallet mass** (⚠️ corrected same day — an earlier draft of this section wrongly blamed heat-treated pallets; the pallets are plastic and were already counted).

**✈️ Airline identified — TAP Air Portugal (IATA prefix `047`).** The AWB `04731753223` begins with the airline prefix **`047` = TAP Air Portugal (IATA `TP`)** — so the Salvador→US leg is TAP Air Cargo. (Ticket's `DUE-26BR0017954000` looks like the DU-E; see the caveat above.)

**⏳ HAWB/MAWB reissue is gated on flight-status confirmation (2026-10-02).** Per **Isis Ribeiro** (Omega, *Export operations* — §2), on WhatsApp: *"As soon as we confirm the flight status, we will send the documentation"* (the **HAWB and MAWB**). So the AWB reissue waits on the **flight being confirmed**, not on anything from Black King — our Rev 15 CI + PL are already with them.

**������ Cargo storage — answered by Isis.** On where the cargo is held in the interim: *"storage is done in the **airport cargo warehouse (Caer)**”* — and it must be kept **away from direct sunlight**. (Cacao is heat/light-sensitive; the TECA/Caer airport terminal is the interim hold.)

**������ Role split — Iolanda vs Isis (Omega).** Distinct: **Iolanda Santos = SISCOMEX / customs** (the habilitação fix, §5.4); **Isis Ribeiro = Export operations** (flight status, HAWB/MAWB, day-to-day export coordination). Graziela Vedana (Seacos) = forwarder/coordinator; Matheus Reis (Black King / Gateway.fy) = origin warehouse/pickup.

**⚠️ Fiscal:** NF-e nº 18 declares **bruto 322,060 / líq. 302,060**. Reissuing commercial docs at 349 kg **diverges from the issued NF-e**. Weights/freight **can** be amended by a **CC-e** (unlike lines/tax base) → the route is a **CC-e on nº 18** + the commercial reissue. **Confirm with Saymon/Matheus.**


#### 5.6 FDA Prior Notice — required for the US leg ������������ NEW 2026-10-02

> **Source:** `brazil/sources/2026-10-02_fda_prior_notice_awb_request.md` (Iolanda Santos / Omega, Gary, thread 10800).

**FDA Prior Notice (PN) is mandatory** for this cacao shipment (a US food import) — it is *not* the optional "if required" line in Phase 7. **Iolanda (Omega, SISCOMEX/customs) will file it.**

**⚠️ Blocking dependency — the PN cannot be filed without the air waybill (AWB).** Iolanda asked Gary directly: *"envie-me o conhecimento de embarque aéreo para que eu possa emitir a notificação prévia à FDA"* (send me the air waybill so I can file the FDA prior notice). The AWB is being **reissued by SeaCoast**, itself gated on **flight-status confirmation** (§5.5). Critical path:

`flight confirmed → SeaCoast reissues HAWB/MAWB → AWB sent to Iolanda → Iolanda files FDA PN → arrival → US customs/CBP`

**⏱️ Timing (21 CFR 1.279):** PN must be **received + confirmed by FDA no less than 4 hours before arrival by air**; and generally **no more than 15 calendar days before arrival** if filed via FDA **PNSI** (or 30 days via CBP ABI/ACE). Filed too early → rejected; too late → cargo refused/held.

**������ Roles:** Isis Ribeiro (Omega) = international/export ops — owns the **shipment status + flight**; Iolanda Santos (Omega) = SISCOMEX/customs — owns the **US-side FDA PN filing**. (Iolanda confirmed she was **back at the office** the morning of 2026-10-02.)

**������ FSVP context:** `fsvp/SHIPMENT_DOCUMENTATION_PROCESS.md` doc #4 = *FDA prior notice* — "filed per FDA PNSI before arrival"; the per-shipment pack lives in `fda_fsvp/suppliers/black_king/`.

**Status:** ⬜ AWB sent to Iolanda (blocked on flight confirmation, §5.5) · ⬜ FDA PN filed (Iolanda).

#### 5.7 Air waybill (HAWB) issued ✅ NEW 2026-10-02

> **Source:** `brazil/sources/2026-10-02_air_waybill_hawb_issued.md`; doc `exports/2026-10-02_air_waybill_black_king_hawb_047-3175-3223.pdf`.

**The air waybill is issued** (Uxcomex process 50505; carrier's agent **Maritime and Air Transports Ltda**, CNPJ `02.992.800/0001-61`, signed **Helesson Bastos**). It **confirms the 349 kg gross** ✅ — no further reissue needed.

| Field | Value |
|---|---|
| AWB no. | **`047-3175 3223`** (TAP prefix `047`, SSA) |
| Document ref | `00093-0926TEA` **— master counterpart issued 05/OCT/2026 ({S}5.8)** |
| Route | **SSA Salvador → SFO San Francisco**, requested flight **`TP028`** (TAP); **date blank** |
| Pieces | **2** — 02 pallets with **27 boxes** with bars of chocolate; 110×77×90 + 110×104×100 cm |
| **Gross weight** | **349,000 kg** ✅ **matches Rev 15 exactly** |
| Chargeable | 349 kg @ **USD 2,30/kg** = **USD 802,70** |
| Total prepaid | **USD 857,70** (weight 802,70 + CCC 15,00 + AWB 20,00 + XBC 20,00) |
| DU-E | **`26BR001795400-0`** → registered ⇒ SISCOMEX habilitação restored (§5.4) |
| RUC | `6BR50042585200000000000000001987510` |

⚠ **HS discrepancy — verify with Omega.** The AWB lists **`1810.00.00`** (cocoa powder); our invoice declares **`1801.00.00`** (cocoa beans). Three others (**1803.10.00 / 2106.90.00 / 1804.00.00**) match. Likely an AWB data-entry transposition of 1801 → confirm.

**What this unblocks:** the AWB is the missing prerequisite for the **FDA Prior Notice** (§5.6). Only the flight **date** remains blank — so the PN is still gated on Isis's flight-status confirmation.

#### 5.8 Master Air Waybill (MAWB) issued ✅ NEW 2026-10-05

> **Source:** `brazil/sources/2026-10-05_air_waybill_mawb_issued.md`; doc `exports/2026-10-05_air_waybill_black_king_mawb_047-3175-3223.pdf`.

**The master air waybill is issued** — the airline-level counterpart of the HAWB (§5.7). **Same AWB number `047-3175-3223`** (same Uxcomex process 50505).


| | HAWB | **MAWB** |
|---|---|---|
| Endpoint | `AirWaybillHAWB` | `AirWaybillAWB` |
| **Shipper** | Black King | **Maritime & Air Transports Ltda** (the agent) |
| **Consignee** | TrueTech Inc (importer of record) | **5 Continent Logistics LLC**, Manchester NH, EIN `82-4285211` |
| Nature | 02 pallets / 27 boxes | **CONSOLIDATED CARGO AS PER ATTACHED MANIFEST ON HAWB** |
| Gross | 349,000 kg | **349,000 kg** |
| Weight charge | **USD 802,70** (349 @ 2,30) | **USD 2,30 MINIMUM** |
| Total prepaid | **USD 857,70** | **USD 57,30** |
| FX | (blank) | **USD 1 = BRL 5,180900** |
| Executed | (blank) | **05/OCT/2026**, Salvador |

**Key reading:** this was a **consolidation** — Black King's cargo rides inside 5 Continent Logistics' master shipment; the airline delivers to the **forwarder's US agent**, who delivers to TrueTech. **MAWB consignee ≠ HAWB consignee** is expected for a consolidated air shipment.

⚠ **Charge reconciliation to flag** — the MAWB bills a **USD 2,30 minimum** (total prepaid **USD 57,30**) while the HAWB bills the **full USD 802,70 weight charge** (total **USD 857,70**). Consistent with consolidation economics (the house carries the weight charge; the master a nominal minimum), but **worth confirming with Graziela/Omega** so the ~USD 800 is not double-counted.

**For the FDA Prior Notice, cite AWB `047-3175-3223`** — both waybills share this number (§5.6).

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
| SISCOMEX/DU-E — company **not habilitado**, habilitação dropped | **~6 months with no SISCOMEX movement** → RADAR habilitação blocked/dropped **by default** | the company (or its representative) runs an **update/movement** in SISCOMEX to restore it — needs a valid **A1 certificate on a working machine** (a broken laptop stalled this on 2026-10-02, §5.4). Prevent by logging periodic movements. |
| Airport scale disagrees with our **gross** (CI + PL rejected, AWB blocked) | our gross model omits the **carton** tare (it *does* include the 20 kg pallet tare); airport weighs product **+ cartons + pallets** | reissue the Commercial Invoice + Packing List at the **ticket** gross (§5.5); **CC-e** the NF-e if already issued; forwarder reissues HAWB/MAWB. |
| FDA Prior Notice **not filed** / filed without the AWB (cargo refused or held at US port) | PN is mandatory for US food imports; needs the AWB, which waits on the flight | get the AWB to Iolanda as soon as SeaCoast reissues HAWB/MAWB (§5.6); file PN ≥ 4 h before arrival by air (≤ 15 d via PNSI) |

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
| 2026-10-02 | **NF-e nº 18 issued — fiscal divergence RESOLVED.** DANFE filed (`brazil/sources/2026-10-02_black_king_nfe_18_danfe.pdf`); §5.3b added (line-by-line vs Rev 14); §1 + §5.1c updated. 9 lines / 27 caixas / 2 pallets / 302,06 net / 322,06 gross / **R$ 33.384,57** — matches Rev 14; nº 16 superseded. The TRANSPORTADOR/VOLUMES block nº 16 left blank (weights/quantity/package type) is now filled on nº 18. **New stale items: ordem de coleta + SeaCoast correction letter must be re-keyed to nº 18.** |
| 2026-10-02 | **SISCOMEX habilitação drop (6-month inactivity) documented** — Iolanda (Omega) to Gary: no SISCOMEX movements for 6 months → RADAR habilitação dropped by default; DU-E blocked. **§1 DU-E row corrected** (“unblocked” → blocked on habilitação); new **§5.4** (inactivity rule + single-certificate risk + Saymon/Iolanda recovery); §8 failure-mode row; source note `brazil/sources/2026-10-02_siscomex_habilitacao_inactivity_notes.md`. |
| 2026-10-02 | **Airport weighing weight-divergence documented (349 kg gross)** — Salvador weighed the cargo at **349,000 kg** vs our documented 322,06 (+26,94 ≈ 2 pallets); forwarder asks for reissued **Commercial Invoice + Packing List at 349 kg** + **HAWB/MAWB**; weighing doc carries a DU-E ref **`26BR0017954000`**. New **§5.5** + §1 row; DU-E caveat; §8 row; Phase 5/6 updated. **CC-e on NF-e nº 18** likely needed. |
| 2026-10-02 | **FDA Prior Notice gate documented** — Iolanda (Omega) requested the **air waybill** to file the **FDA Prior Notice** (mandatory for the US food import). New **§5.6** + §1 row; Phase 5 AWB-to-Iolanda item; Phase 7 "if required" corrected; §8 row. Blocked on flight confirmation → AWB reissue. |
| 2026-10-02 | **Air waybill (HAWB) issued** — AWB **`047-3175 3223`** (TAP `TP028`, SSA→SFO), gross **349,000 kg == Rev 15**; DU-E `26BR001795400-0` registered; chargeable 349 kg @ $2.30 = $802.70, total prepaid $857.70. New **§5.7** + source note + doc. HS discrepancy flagged (1810 vs 1801). |
| 2026-10-05 | **MAWB issued** — master counterpart of the HAWB (**same AWB `047-3175-3223`**), a **consolidation** (MAWB consignee **5 Continent Logistics LLC**, EIN 82-4285211), executed **05/OCT/2026**. Charges: master total prepaid **USD 57,30** (2,30 minimum) vs house **USD 857,70** — flagged for reconciliation. New **§5.8** + source note + doc. |
| 2026-10-02 | **Rev 15 — Commercial Invoice + Packing List reissued at gross 349 kg** (Daniel / SeaCoast ask, §5.5). Gross restated 322,06 → **349,00** = net 302,06 + carton tare 26,94 (27 boxes) + pallet tare 20,00 (2 × 10 kg HDPE). **Net, lines, boxes, USD/BRL unchanged.** `exports/2026-10-02_*_rev15_*`; generator gains the Rev-15 gross model + a `GROSS_WEIGHED` invariant. Also **corrected the same-day §5.5 draft** (pallet→carton tare; pallets are plastic HDPE, not heat-treated wood). |
| 2026-09-29 | **NF-e nº 16 recorded as issued** (22/09/2026, chave `2926…0035`, R$ 35.828,76) — reconciled line-by-line vs. Rev 12 (§5.3); DANFE archived to `brazil/sources/`. Flipped §1 *IE/SEFAZ-BA* and *NF-e issued* 🔴→✅, unblocked DU-E; noted the **blank TRANSPORTADOR/VOLUMES block** (the weights/qty/package-type gap); corrected the now-stale “no NF-e issued” wording in the Correction Letter + ordem de coleta generators (regenerated both PDFs). |
| 2026-09-29 | **NF-e nº 16 XML archived + reconciled** (SeaCoast-requested; Gary, thread 10800) — signed/authorized XML saved to `brazil/sources/2026-09-22_black_king_nfe_16.xml`; line-by-line match vs Rev 12 PL (fiscal sum **344,00 kg** vs PL commercial 344,06 kg — 3-decimal TON rounding); confirmed the XML `<transp>` is **empty except `modFrete=1` (FOB)** — the same blank the ordem de coleta REV 3 fills. Notes: `brazil/sources/2026-09-22_black_king_nfe_16_xml_reconciliation.md`. |
| 2026-09-21 | **Saymon/Jussileide are NOT on Telegram** — they are contractors on WhatsApp “Black King - Contab”. Added a delivery-channel warning to §2 so no agent assumes a thread-10800 post reaches them; artifacts for the accountant are relayed by Gary. No automated path (“Black King - Contab” is not in OpenClaw's verified JID list). |

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
