# Black King Administrative Access — Decision Document

**Context:** Gary needs the ability to handle Black King's administrative processes (e-CAC, CNAE, declarations, SEFAZ/NF-e prep) so Brazil exports don't stall on a single point of failure (Matheus).

**CNPJ confirmed facts (via Brasil API, Receita Federal data):**
- Razão social: MATHEUS REIS PEREIRA | Fantasia: BLACK KING
- **Natureza jurídica: Empresário (Individual) — 213-5**
- Porte: Micro Empresa · Simples Nacional: **Ativa** (since 2023-03-22)
- Capital social: R$ 10.000,00 · QSA: **empty** (no partners by definition)
- CNAE fiscal: 82.30-0-01 (feiras/exposições) + 8 secondary — **none cacao/commerce**
- Situação cadastral: **INAPTA** — motivo **OMISSÃO DE DECLARAÇÕES** (2026-06-08)

---

## Option A — Procuração Eletrônica (e-CAC)

Matheus grants an electronic power of attorney to Gary's CPF/gov.br in e-CAC. No corporate change.

### Pros
- **Fast** — hours to days, entirely digital, free
- **No corporate restructuring** — no Junta Comercial, no contrato social, no name change
- **Scoped** — can be limited to specific services or "all"
- **Revocable** — Matheus can revoke anytime
- **No tax impact** — Simples Nacional untouched
- **Covers the federal side** — e-CAC, CNPJ data changes (the CNAE fix!), declarations, Certidões
- **Low risk** — reversible, no legal restructuring costs

### Cons
- **No ownership** — Gary gets no equity or permanent rights
- **Revocable = fragile** — dependency on Matheus remains; single point of failure persists
- **State-level gap** — SEFAZ-BA (IE, NF-e credentialing, NF-e emission) does NOT automatically follow the e-CAC PoA; Bahia has its own access rules
- **NF-e emission still needs the e-CNPJ** — PoA doesn't replace the digital certificate for the actual NF-e
- **Max 5 years validity** — must be re-granted
- **Doesn't fix Inapta status or debts** — those still need Matheus's declarations/payments
- **Terminates on Matheus's death/incapacity** — the fragility the DAO wants to avoid
- **Banks may not accept it** — banking mandates usually need their own forms

---

## Option B — Transform to Sociedade Limitada (Ltda)

Convert natureza 213-5 → 206-2 (Sociedade Limitada Unipessoal, or Ltda with partners) via DBE event 225, add Gary as administrator (and optionally quotaholder). CNPJ stays the same.

### Pros
- **Formal, durable authority** — Gary as named administrator in the contrato social; survives Matheus
- **Real ownership option** — Gary (or DAO-aligned entities) can become quotaholders; foreign individuals with CPF can hold quota in a Brazilian Ltda
- **Eliminates the single point of failure** — the core strategic risk
- **Aligns with the full-stack plan** — this can BE the "new Brazilian CNPJ" vehicle instead of creating a fresh one
- **Banking mandates can name Gary** — smoother for PIX, invoices, treasury
- **Better liability structure for Matheus** — Ltda separates personal assets better than EI
- **Cleaner governance** — contrato social, administração clause, formal QSA
- **Future-proof** — add partners/investors later (fits AGL/triangular structure)

### Cons
- **Slower** — Junta Comercial + DBE event 225 + Receita Federal; days to weeks
- **Costs** — Brazilian lawyer/accountant (est. R$ 1.500–5.000+), Junta fees, possibly Simples re-registration handling
- **Name change** — must gain "Ltda" suffix (Black King Ltda)
- **Must update state records** — SEFAZ-BA IE, NF-e credentialing re-issued under the new nature
- **Inapta status is a blocker** — declarations must be filed / debts resolved BEFORE or as part of the transformation; RFB may reject while Inapta
- **More ongoing compliance** — Ltda carries heavier formal obligations (annual ECF/ECD, DAS under new QSA, board formalities)
- **Tax nuances** — Simples continues but DAS can shift with QSA/administrator; foreign-quotaholder reporting (e-Financeira/RDE) may apply
- **Irreversible-ish** — restructuring is much harder to unwind than revoking a PoA

---

## Option C — Hybrid (recommended path)

1. **Now:** Procuração Eletrônica to unblock federal admin (CNAE, declarations, Certidões) — days
2. **In parallel:** Regularize Inapta (file declarations, settle/negotiate debts)
3. **Strategic:** Transform to Ltda + add Gary as administrator (and DAO-aligned quotaholder) as the durable structure — while the GACC/China lane (3–6 months) runs

---

## Decision matrix

| Criterion | A: Procuração | B: Ltda transform |
|---|---|---|
| Speed | ★★★★★ | ★★ |
| Cost | ★★★★★ (free) | ★★ |
| Durability / survives Matheus | ★ | ★★★★★ |
| Removes single point of failure | ★★ | ★★★★★ |
| Covers SEFAZ-BA / NF-e | ★★ (partial) | ★★★★ |
| Ownership / full-stack play | — | ★★★★★ |
| Reversibility | ★★★★★ | ★★ |
| Works while CNPJ is Inapta | ★★★★ | ★★ (blocked until regularized) |
| Ongoing compliance burden | ★★★★★ (none) | ★★ |

---

**Bottom line:** Procuração unblocks today; the Ltda transformation is the durable fix that matches the DAO's strategic direction. Do both — PoA first, transform when Inapta is cleared.
