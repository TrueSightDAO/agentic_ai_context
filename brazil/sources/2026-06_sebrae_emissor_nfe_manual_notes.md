# SEBRAE NF-e Emitter — User Manual (v10, Jun 2026) — source notes

**Document title (PDF metadata):** `Manual do Usuário - SEBRAE [Jun 2026 v10]`
**Archived PDF (verbatim):** `brazil/sources/2026-06_sebrae_emissor_nfe_manual_v10_PT.pdf`

| Field | Value |
|---|---|
| Pages | **270** |
| Size | 13,287,729 bytes (~12.7 MB) |
| Language | Portuguese (pt-BR) |
| Producer | Skia/PDF m151 (Google Docs renderer) |
| Version | v10 — **Jun 2026** |
| Original attachment filename | `02a8d9b9a3014b288cf28f4eeda14c69.pdf` (Telegram hash name) |
| Curated | **2026-09-22** (Sophia) at governor **Gary Teh**'s request |
| Feeds | `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` §5.2 (Sebrae master-data sequence) and §5.1a (units of measure) |

---

## 1. Why this matters

The DAO's **Brazil → San Francisco export lane** issues its NF-e through the free **SEBRAE emitter** at `https://emissornfe.sebrae.com.br/` (runbook §5.2; the hired NF-e specialist **Saymon** works in it, logging in via **gov.br** with the Black King A1/A3 certificate).

Until now the runbook captured only the *sequence* of steps (register emitente → products → clients → suppliers → issue). This PDF is the **authoritative, vendor-authored operator manual** for every screen the team touches — click-by-click — including the areas the lane actually got stuck on: **certificate setup (A1/A3)**, **product fiscal fields (NCM/UNIDADE/CEST)**, **Matriz Fiscal / CFOP / CST-CSOSN**, and the **export NF-e** issuance flow.

## 2. Provenance & caveats

- Retrieved from a **governor-uploaded Telegram PDF attachment** on 2026-09-22; archived here **verbatim**. It had not previously been committed to any DAO repo.
- This is **SEBRAE's own public product manual** — vendor documentation, **no confidential DAO data**. Safe to store in the context repo.
- Full-text extraction tooling truncates at ~100 pages; the section map below is taken from the manual's **own ÍNDICE (TOC)**, so it covers all 270 pages.
- The manual is written for the general SEBRAE user base (Simples Nacional / Lucro Real / Presumido, all NF-e/NFC-e/NFS-e/CT-e flows). Only the NF-e export subset applies to the DAO lane.

## 3. Section map (from the manual's ÍNDICE — printed page numbers)

| Printed pp. | Section (PT) | What it covers |
|---|---|---|
| 7–21 | Introdução · Acesso · Cadastro · Migração · Emitente · Instalação · Config. da empresa · Usuários · Permissões · Logs | Account & company setup; **migration from the old (Java) emitter via ZIP ≤ 50 MB** |
| 15 | Teclas de atalho (**F1**) | Keyboard shortcuts overlay |
| 16 | **Produtor Rural** | CPF-based rural-producer mode (e-CPF A1/A3 certificate) |
| 22–49 | **Cadastros** — Produtos · Serviços · Clientes · Fornecedores/Transportadora | Master data; **spreadsheet import** (products: 24 columns) |
| 24–26 | Medicamentos · Armamentos · Combustíveis · Veículos | Special product fiscal types |
| 27–29 | Composição · Fragmentados · Estoque Grade · Movimentação de estoque | Product variants & stock movement |
| 50–55 | **Certificado Digital A1 / A3 · Assinador Digital** | Digital-certificate setup |
| 56 | **CRT** (Código de Regime Tributário) | Tax-regime code |
| 57–64 | Habilitar emissão NF-e / NFC-e / NFS-e / CT-e | Enable each document type (**CSC** for NFC-e) |
| 65–68 | Inutilizar NF · **CST e CSOSN** · Tabelas A/B | Note voiding + tax-situation codes |
| 69–91 | **Matriz Fiscal** (layout novo/antigo) · copiar matriz · principais matrizes (interestadual, **FCP**, **ST**, destaque ICMS, **IPI**) | The fiscal rule matrix |
| 92–93 | **CFOP** · Natureza de Operação | Operation codes |
| 94–152 | **Emissão NF-e** (medicamentos/armamento/combustíveis/veículos) · CC-e · ajuste · devolução · retorno · remessa · complementar · **importação** · **exportação** · **cancelamento** · homologação · NFC-e | NF-e / NFC-e issuance |
| 153–190 | **Emissão CT-e** (com/sem XML, modais, globalizada, subcontratação, complementar, substituição, desacordo) · **unidades de medida** · importar emissor · cancelamento · carta de correção · **AutXML** | CT-e (freight) issuance |
| 191–217 | **NFS-e** emissão/cancelamento · cidades atendidas por UF · consulta de documentos · copiar nota · enviar por e-mail · exportar/importar XML | NFS-e + document management |
| 223–226 | **MDF-e** · status das notas | Manifesto & note status |
| 227–229 | Relatórios — produtos · clientes · estoque | Reports |
| 230–246 | **Rejeições e Soluções** | SEFAZ rejection fixes |
| 247–254 | Guias para Animais | Animal-transport guides *(newer addition)* |
| 255–261 | **Configurando o IBS e o CBS** | Brazil tax-reform (IBS/CBS) configuration *(newer addition)* |
| 262 | FISCAL: emissão com **Certificado A3 — 500 Erro Interno do Servidor** | A3 error fix *(newer addition)* |

## 4. DAO-lane call-outs

- **Units of measure (UNIDADE) is a required product field** (CADASTROS > PRODUTOS → *Unidade*), and the manual has a dedicated *“SOBRE AS UNIDADES DE MEDIDA DA CT-E”* section (p.187). **This is the exact rejection class that failed the Rev 11 export NF-e** (wrong `unidades de medida` for NCM 1801/1803/1804) — see runbook §5.1a. When re-keying the emitter, the product's `UNIDADE` must match the norm table's `uTrib`.
- **No FX auto-update.** The manual's *CADASTRO AUTOMÁTICO* is barcode-based (fills product info from a GTIN), **not** a price/FX sync — consistent with Saymon's *“toda vez que for emitir uma nota fiscal, será necessário alterar o valor de todos os produtos.”* Product values are re-keyed per issuance (runbook §3).
- **Certificate:** *A1* = upload `.pfx` file; *A3* = **Assinador Digital** running locally + password prompt. Login via **gov.br → Seu Certificado Digital** selects the company cert (for Black King it shows as **Matheus**) — matches runbook §5.2 step 1.
- **Product fiscal tab is mandatory to emit:** `TIPO`, `NCM`, `ORIGEM`; `CEST` only for substituição tributária (manual p.23). `ORIGEM` uses **Tabela A**; CST/CSOSN use **Tabela B** (p.66–68).
- **Matriz Fiscal** is where CST/CSOSN, ICMS alíquotas, **substituição tributária**, **FCP** and **IPI** are configured; the emitter ships zeroed for Simples Nacional (p.69). Export issuance uses CFOP **7.101/7.102** (runbook §5.2 step 5) → relevant matrix setup.
- **Rejeições appendix (pp.230–246)** covers the SEFAZ rejections the lane can hit: `INFORMADO NCM INEXISTENTE OU INVÁLIDO`, `GTIN (CEAN) COM PREFIXO INVÁLIDO`, `CFOP ... IDDEST` mismatches, `PERCENTUAL DE FCP IGUAL A ZERO`, `INFORMADO CÓDIGO DE BENEFÍCIO FISCAL ...`, `DATA DE SAÍDA MENOR QUE A DATA DE EMISSÃO`, etc.
- **Newer additions worth noting:** *Guias para Animais* (247), *Configurando o IBS e o CBS* (255) — Brazil's consumption-tax reform — and the *A3 500-error* fix (262).

## 5. Cross-references

- `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` — canonical Brazil→SF runbook (§5.1a units, §5.2 emitter master-data sequence).
- `brazil/sources/2026-09-21_black_king_accountant_thread_notes.md` — Saymon/Jussileide sourcing of the emitter + the norm table (Appendix E).
- `brazil/sources/2026-05-18_omega_siscomex_representante_tutorial_notes.md` — sibling archived primary-source PDF (SISCOMEX representante registration).
