# Omega SISCOMEX representante registration tutorial — source notes

**Source:** Email from **Iolanda Santos** (Omega Services) → Matheus Reis + Gary Teh.
**Subject:** `RE: Quote Gary` · **Date:** Mon **2026-05-18 14:09 UTC** · **Gmail msg id:** `19e3b6ba626fbcd8` (thread `19e2102a34ab546a`).
**Attachment (archived alongside this note):** `2026-05-18_omega_siscomex_representante_tutorial.pdf` — original filename `TUTORIAL - CADASTRO DE REPRESENTENTE NO SICOMEX.pdf` (566,758 bytes · 3 pages · Portuguese).
**Curated:** 2026-09-22 (Sophia) at governor **Gary Teh**'s request (thread 10800).
**Feeds:** `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` §1 (SISCOMEX/RADAR row) and §5 Phase 0 (PoA item).

## 1. Why this matters

This is the **primary source** for how a customs broker / despachante is added as a **representante** of the exporter in SISCOMEX / RADAR. The runbook recorded the outcome ("3 Omega brokers registered", "Omega PoA signed", ✅ Jun 2026) but the authoritative step-by-step lived **only in the governor's mailbox**. This note + the archived PDF make it citable.

## 2. What Omega said (verbatim, PT)

Iolanda Santos — 2026-05-18:

> "Encaminhamos anexo tutorial para inclusão dos despachantes da Omega junto ao radar/SISCOMEX. Essa inclusão é feita com o **certificado digital e-CPF do responsável legal da empresa**."

Iolanda Santos — 2026-05-26 (the *how*):

> "Quanto a inclusão no radar, é necessário você acessar em sua máquina e fazer a inclusão através do **Portal Único** (https://portalunico.siscomex.gov.br/portal/) **seguindo as instruções no tutorial**."

Completion confirmation — Gerson Argolo (Omega), 2026-05-26:

> "Confirmamos que o **cadastro siscomex está ok**."

## 3. The three despachantes registered (the "CPF" list from the earlier step)

| # | Despachante | CPF |
|---|---|---|
| 1 | Valéria Requião Barretto | 420.749.165-15 |
| 2 | Lazaro Barbosa Reis | 237.915.355-87 |
| 3 | Mauricio Costa Bezerra | 374.003.555-20 |

> These CPFs are business-operational identifiers (professional despachantes), not personal financial data. The governor can request a redaction if preferred.

## 4. The mechanism, in the archived PDF's own words

The attached `TUTORIAL - CADASTRO DE REPRESENTENTE NO SICOMEX.pdf` is a 3-page click-by-click screenshot guide:

| Page | Instruction |
|---|---|
| 1 | Go to `https://portalunico.siscomex.gov.br/portal/` → click **IMPORTADOR/EXPORTADOR** |
| 2 | Click **NÃO SOU UM ROBÔ** → **ACESSAR COM CERTIFICADO DIGITAL** → click **CADASTRO DE INTERVENIENTES** |
| 3 | Fill: **CNPJ/CPF** (the entity represented = Black King) · **Tipo de atuação** = *IMPORTADOR/EXPORTADOR* · **Dados de Despachante / CPF** (the despachante's CPF) · **Data final** (end date of the representation) · tick **GESTOR DO CATÁLOGO DE PRODUTOS** → click **ADICIONAR** |

Key point: the CPF entered at page 3 is the **despachante's**, keyed by Black King's **legal representative** using the company **e-CPF certificate**. This is the "sign the PoA → then enter their CPF in Siscomex" mechanic; it is **not** a separate PoA and is **not** the Governor's own e-CAC/cartório procuração (see checklist §5 Phase 0 for that distinct instrument).

## 5. Chain of record (May–Jun 2026)

1. **2026-05-13** — Helesson Bastos (Omega) lists what's pending for the new exporter: POA, registration in the customs system, fixed service value.
2. **2026-05-14** — Gary: Black King already registered with SISCOMEX; Matheus is registering the **3 CPF numbers as customs brokers** and will revert with signed docs.
3. **2026-05-18** — Matheus sends the **signed procuração**; Iolanda sends the **tutorial** + the 3 CPFs.
4. **2026-05-26** — Iolanda: habilitação OK; inclusion done via Portal Único. Gerson Argolo: "cadastro siscomex está ok".
5. **2026-06-08** — Graziela green-lights the shipment (palletize with Matheus).

## 6. Caveat / provenance note

- The PDF was retrieved from Gmail attachment storage (read scope `gmail.modify`) on **2026-09-22** and archived here verbatim; it had not previously been committed to any DAO workspace/repo.
- "SICOMEX" (as spelled in the filename) = **SISCOMEX**.
