# Brazil Export Lane — Consolidated Learnings

**Compiled:** 2026-08-23 (Sophia, for Bionpact/Onaya + Elizabeth Wong's "Nano of Trade")
**Scope:** Everything learned Jun–Aug 2026 across the Brazil export operation — Black King infrastructure, MAPA/GACC (China lane), trader-vs-producer model, cooperative routes, gov.br access.

---

## 1. The Players & Structure

| Entity | Role | CNPJ / ID | Status |
|--------|------|----------|--------|
| **Black King** (Matheus Reis Pereira) | Exporter/trader — consolidates from multiple farms, processes (sort/grade/pack), issues export NF-e | CNPJ 50.042.585/0001-80 (Empresário Individual 213-5, ME, Simples) | ⚠️ CNPJ **INAPTA** + expired e-CNPJ + no commerce CNAE → cannot issue NF-e |
| **Coopercabruca** (Coop. Sul da Bahia) | Producer cooperative (Bahia) — member-farmer beans, MAPA-ready | CNPJ 31.948.811/0001-42 | ✅ Has IE + NF-e; MAPA registration being set up for China |
| **CEPOTX** (Coop. Transamazônica e Xingu) | Producer cooperative (Pará) — organic almonds | CNPJ 22.568.369/0001-38 | ✅ Exporting already; sends beans to Matheus for processing |
| **TrueTech Inc** | US importer-of-record (FSVP, Customs 88-341151400) | EIN 88-3411514 | ✅ Active |
| **TrueSight DAO LLC** (Próspera ZEDE) | Coordination/trade entity — books profit, does NOT own Brazilian entities | Próspera LLC (OA signed 2026-07-18) | ✅ Formed; notarization/PT translation in progress |
| **Independent farmers** (Oscar, Clara, Analuana, Vivi, etc.) | Grow/ferment beans; no MAPA, no factory | — | Source from Bahia + Pará |

**Key structural rule:** MAPA/GACC requirements attach to the **production enterprise** (the facility that processes/benefits beans), NOT the exporter/trader. A trader buys from producers and ships under their registrations (or its own if it processes).

---

## 2. Black King Infrastructure Issues (7 concurrent)

1. **CNPJ INAPTA** (situação cadastral) — motive: "omissão de declarações" (2+ years missed: DCTF/ECF/ECD/DAS), dated 2026-06-08. Blocks NF-e + risks RADAR suspension.
2. **e-CNPJ digital certificate EXPIRED** early June 2026 — blocks all gov portals (e-CAC, SEFAZ, SISCOMEX).
3. **Missing commerce CNAE** — only service CNAE (82.30-0-01); no IE; no NF-e credentialing. Fix: add secondary CNAE 46.23-1/04 (comércio atacadista de cacau).
4. **Outstanding federal tax debts** — amounts being confirmed via e-CAC (Situação Fiscal) + REGULARIZE (Dívida Ativa).
5. **RADAR misconception** — RADAR does NOT change CNPJ cadastral status; CNPJ must be Ativa to keep RADAR. Graziela (Seacos) initially claimed RADAR "changes CNPJ to APTO" — not accurate.
6. **Unprofessional accounting** — current accountant does it "as a favor"; declarations lapsed. Vini sourcing export-savvy replacement (~USD 1,000–2,000/yr).
7. **Local legal representative requirement** — Brazilian companies need one (like Singapore); Paloma (Haus Florianópolis) is skittish; Vini's firm's monthly fees reflect this service.

---

## 3. MAPA Registration (China lane)

- **What:** MAPA establishment registration — registers the **facility**, not the farm. Category for cacao beans: **"BENEFICIADOR DE AMÊNDOA DE CACAU"** (NCM 1801.00.00), nível **básico (geral)**, **vistoria dispensada** (no on-site inspection).
- **Who needs it:** Coopercabruca ✅ (applying), CEPOTX ✅ (applying), Black King (optional — as its own beneficiation facility), new DAO/BR CNPJ (optional). **Independent farmers ❌** — they don't need it IF beans pass through a registered beneficiation facility.
- **Independent-farmer coverage play:** Black King (or a new CNPJ) registering its own facility covers beans from unregistered farmers — the beans become "covered" on entering the registered facility. This upgrades trader → production enterprise in China's eyes.
- **Registration links:** Solicita (`solicita.agricultura.gov.br`) → SIPEAGRO (`sistemasweb.agricultura.gov.br/sipeagro/`). Requires e-CNPJ or gov.br linked to CNPJ.
- **US lane does NOT need MAPA** — only China (GACC/CIFER asks for the "competent authority" production number). US runs on FDA FFR + FSVP + Prior Notice + per-shipment phytosanitary.

---

## 4. GACC/CIFER — China lane rules (from Ling, China side)

- **One application per CNPJ** — 3 separate entities (even sharing one factory) = 3 separate GACC registrations. Cannot merge.
- **MAPA number entered at first login and LOCKED** — cannot be changed after.
- Two product categories: "Confectionery, Chocolate" (NCM 1806) vs "cocoa beans/other products" (NCM 1801/1803). Separate applications per category.
- Shared materials OK across entities: factory photos, line video, process flow, floor plan. Company-specific: CNPJ, labels, ingredient lists (descending order).
- Files ≤4MB (jpg/jpeg/gif/png/bmp/pdf). No withdrawal after submission. **Save the 18-digit receipt number** and return to Ling.
- Docs: CNPJ + Chinese translation, facility/product photos, labels, flow chart, ingredient list EN descending, floor plan.
- Ling's walkthroughs (EN + ZH DOCX) filed at `agentic_ai_context/exports/2026-07-29_ling_cifer_guide_english.docx` and `..._chinese.docx`.

---

## 5. Trader vs Producer & the Routes

- **Trader (Black King / new BR CNPJ):** consolidates independent beans (Bahia + Pará), processes/benefits, issues export NF-e, owns RADAR. MAPA optional (as beneficiador).
- **Producer cooperative (Coopercabruca):** only member-farmer beans in Bahia, freshly harvested/with-farm. Holds MAPA + GACC. **Cannot absorb independent warehouse stock.**
- **China direct route:** China side can bypass the DAO entirely and work directly with Orlantildes/Coopercabruca (Bahia beans) — DAO plays no role structurally. CEPOTX (Pará) flow blocked if Black King down → tree-planting arrangement off table.
- **Worst case:** US/EU DAO distribution networks shut down (no capital for stock inventory); independent warehouse inventory stranded (write-off); China lane unaffected (direct coop route).
- **Trading company bridge:** "por conta e ordem" (IN RFB 1.861/2018) — trading company exports in its own name; bypasses Black King's CNPJ problem; fee 0.5–2% FOB; invoice in trading company's name. Cost check pending with Graziela/Omega.

---

## 6. Gary's gov.br / e-CPF Path (admin access)

- CPF 039.733.078-22 exists. gov.br account registered (2026-08).
- **Ouro level** requires ICP-Brasil digital certificate (e-CPF A1/A3) — facial recognition won't match foreign databases.
- Providers in Florianópolis (nearest Jurerê first): AR SC Digital (Ingleses), SESCON Grande Florianópolis (Centro, does home visits), CDL Florianópolis, AR Validar, Plátano Digital (remote/video).
- **Procuração Eletrônica** (e-CAC) from Matheus → Gary can act on Black King's federal affairs (e-CAC, CNAE fix, declarations, certidões). Does NOT cover SEFAZ-BA/NF-e.
- **Option B: transform Empresário Individual (213-5) → Ltda (206-2)** — enables Gary as administrator/quotaholder; durable; kills single-point-of-failure; but needs Inapta cleared first. Decision doc: `brazil/BLACK_KING_ADMIN_ACCESS_OPTIONS.md`.

---

## 7. Freight SOP (Ilhéus → San Francisco)

- **Canonical doc:** `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` (7 phases, cost summary, Appendices A/B). PDF: `exports/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.pdf`.
- **Current blocker:** Phase 0 — NF-e cannot be issued (the 7 issues above).
- **Omega quotation (May 2026):** road transport BRL 6,615 + 0.15% ad-valorem; palletization BRL 195 (excluded — pallets on hand); fumigation BRL 500; export docs $95; air freight $3.20–3.50/kg tiered; Brazil airport $0.30/kg (min $250); US terminal $212.50; US handling $125; clearance $150; FDA $100; MPF 0.3464%; bond max($100, $6/$1k).
- **Freight-only total (internal transfer, excl. payload):** ≈ **US$ 3,550** (Brazil ≈ $1,319 @ 5.40 FX + air/export ≈ $1,722 + US ≈ $509).
- **Shipment docs:** INV-2026-0611-001 Rev2 FOB $7,032.53 + PL-2026-0611-001 (EN + PT PDFs in exports/).

---

## 8. Canonical Doc Pointers

- `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` — freight SOP
- `brazil/BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE.md` — China lane (incl. MAPA section, Ling's walkthrough references)
- `brazil/BLACK_KING_ADMIN_ACCESS_OPTIONS.md` — Procuração vs Ltda decision
- `exports/2026-08-23_brazil_china_lane_oscar_beans_briefing_elizabeth.pdf` — Elizabeth briefing
- `exports/2026-07-29_ling_cifer_guide_english.docx` / `..._chinese.docx` — CIFER walkthroughs
- `exports/TrueSight_DAO_LLC_Prospera_Operating_Agreement_signed_v1.0.pdf` — Próspera OA (signed 2026-07-18; notarization + PT translation in progress via Adriana Maciel, tradutora juramentada)

---

*Compiled by Sophia (TrueSight autopilot) 2026-08-23 for Bionpact/Onaya and Elizabeth Wong's "Nano of Trade" research.*
