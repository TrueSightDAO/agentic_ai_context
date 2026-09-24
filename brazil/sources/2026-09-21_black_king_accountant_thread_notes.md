# Black King accountant thread — source notes

**Source:** `~/Black King - Contab.zip` → `_chat.txt` (WhatsApp export).
**Thread:** "Black King - Contab" — Gary Teh + **Saymon** ("Nota Fiscal Expert") + **Jussileide** (Accountant) + Matheus.
**Period:** 2026-09-18 → 2026-09-21.
**Curated:** 2026-09-21 (Sophia). Raw ZIP retained by the governor. PII (CPFs / personal-debt values) omitted.
**Feeds:** `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` (Phase 0 correction).

## 1. CNPJ regularization / back taxes
- DARF generated for **NOV.2024 – JUL.2026** (3 pages) — the DAO-funded portion.
- Separate guia for **exercise 2023 (MEI era)**: no discount available; can be future-dated.
- The guia covering **all** debits can only be generated **for the current day** (cannot be post-dated).
- Payment **split**: DAO pays the Nov-2024+ portion; Matheus covers the pre-Nov-2024 period.
- Gary: the DAO-funded comprovante must **not show anything before Nov 2024** (audit use).

## 2. NF-e approval gate (governance)
- Gary, 2026-09-18: henceforth **all notas fiscais must be submitted to Gary for approval before issuance is authorized.**

## 3. The real blocker — structural chain
- Saymon, 2026-09-18: requires an **alteração do contrato social at Junta Comercial**; after Junta approval → **Prefeitura update** → generate **tax guides**. Municipal **licença comercial** for the cacao business is needed (Gary asked when).
- Jussileide: the **carta de procuração** is to be done at the **cartório** directly.

## 4. NF-e emitter
- Saymon proposes the **free Sebrae public emitter**: https://emissornfe.sebrae.com.br/
- Sequence: register **company as emitente** → **produtos** → **clientes** → **fornecedores** → issue.
- Black King **already had an account** on the Sebrae emitter (Matheus used it before).
- **Client TrueTech Inc already registered.**
- Login path: emitter → gov.br → "Seu Certificado Digital" → Black King cert (shows as Matheus) → select Black King.
- ⚠️ Emitter does **not** auto-update FX: **re-key all product values each issuance**.

## 5. Currency / PTAX
- The nota must be issued in **BRL**; the invoice was USD → PTAX reference date needed (invoice used **14/09/2026**).
- Gary: going forward, quote commercial invoices in **BRL** to simplify.

## 6. Timeline pressure
- China partners arrive **2026-09-29**; Gary asked to resolve before then.
- Commercial invoice dated **2026-09-21**, quoted in BRL, sent to Saymon (small difference vs. Saymon's own calculation noted).

## 7. NF-e units-of-measure rejection (2026-09-21)
- Saymon (WhatsApp, 2026-09-21 4:38–4:39 PM): the **erro na nota** is due to the **unidades de medida** used.
- Verbatim: *“existe um norma técnica que especifica a utilização de unidades de medidas para alguns NCMs em caso de Exportação.”*
- Verbatim: *“eu acredito que deverá ser gerada outra invoice com as unidades de medida e os valores corretos.”*
- Action: **regenerate the commercial invoice (Rev 12)** with the NCM-required units of measure and correct values; then re-key the emitter products and re-issue the NF-e draft (still gated on Gary's approval).

## 8. NCM → export uTrib norm table (Gary, 2026-09-21)
- Gary supplied the NCM/uTrib export unit-of-measure table (PDF, 2026-09-21) — the *norma técnica* Saymon cited.
- Chapter 18: **1801.00.00 → TON**, **1802.00.00 → KG**, **1803.10.00 / 1803.20.00 → TON**, **1804.00.00 → TON**, **1805.00.00 → TON**, **1806.*** → **KG**.
- Rev-11 lines under 1801/1803/1804 were declared in UN/KG → must be re-expressed in **TON** for Rev 12 (runbook Appendix E + §5.1a).
- 2106.90.00 (Cacao Tea, lines #6/#10) is outside Chapter 18 → not keyed by this table; confirm its uTrib.
- Flag: "Cacao Husk" (#2) NCM 1803.10.00 is likely wrong (→ 1802.00.00, uTrib KG) — confirm with Saymon.
