# Omega Services — export ON HOLD: CNPJ non-compliance (2026-10-01)

> **Received via Gary, Telegram thread 10800, 2026-10-01.** Cargo status: **already at Salvador airport (SSA)**.
> **Why it matters:** this is the first *live* confirmation that the **CNPJ / exporter-habilitação gate** (runbook §5 Phase 0) is **actively blocking the export** — not merely a pending admin item.

---

## 1. Verbatim notice (Omega Services)

> We would like to inform you that the **export process is currently on hold** due to a **non-compliance with admissibility requirements identified in the CNPJ** registered with the Brazilian Federal Revenue Service.
>
> In view of this situation, we have already submitted a **formal inquiry to the Federal Revenue Service** to clarify the reason for the suspension and determine exactly which outstanding issues need to be addressed.
>
> We expect to receive a response from the Federal Revenue Service and will inform you as soon as we have an update.

---

## 2. What it means

- **It is the CNPJ, not the cargo, not the NF-e.** The NF-e prerequisite is met (nº 16, issued 22/09/2026; XML `cStat` 100). The blocker is the **exporter's legal/registered status at RFB**.
- **"Non-compliance with admissibility requirements"** = the RFB's own gate on the *entidade*. This is consistent with the recorded **SITUAÇÃO CADASTRAL: INAPTO since 08/06/2026**, motivo *"Omissão de Declarações"* (unfiled returns) — see `OPEN_FOLLOWUPS.md` ("Black King CNPJ is INAPTO + e-CNPJ expired").
- **Resolution = CNPJ shows Ativa.** Until then, RADAR/SISCOMEX will not let the export (DU-E) proceed.
- **Omega is the right actor for the inquiry** — they have the SISCOMEX/RFB channel; we need *exactly which* obligations the RFB lists as outstanding, then settle them (the pending **2023 MEI-era guia** is the known candidate).

⚠️ **Do not conflate with the SISCOMEX *representante* error.** A DU-E attempt also returned:

> *"O USUÁRIO NÃO CONSTA COMO REPRESENTANTE DO DECLARANTE OU DO EXPORTADOR, considerando o perfil de acesso selecionado no login…"* and *"O EXPORTADOR INFORMADO NÃO ESTÁ HABILITADO PARA OPERAR NO COMÉRCIO EXTERIOR."*

The **empty *Lista de Representações* ("Nenhum registro adicionado")** in the revised tutorial (2026-10-01) = a **separate** fault (representante link not saved; possible perfil/certificate mismatch). Fixing the representante will **not** clear the CNPJ/habilitação fault, and vice-versa.

---

## 3. Tie-back to the runbook

| Runbook §1 row | Was | Now |
|---|---|---|
| DU-E (Notificação de Exportação Fiscal) | 🟡 unblocked | 🔴 **ON HOLD** (this notice) |
| CNPJ regularization (exit Inapto) | 🟡 in progress | 🔴 **BLOCKING — cargo held at SSA** |
| SISCOMEX / RADAR (brokers registered) | ✅ done (Jun 2026) | 🟡 **representante link failing** (separate fault) |

**Next check (owner: Gary → Omega):** get RFB's enumerated outstanding items from Omega's inquiry; confirm CNPJ status page shows **Ativa**.
