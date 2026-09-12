# Shipping Addresses Reference — Saved Ship-To Addresses

> Saved for easy retrieval when a shipping/checkout form asks for a delivery address.
> Same shelf as `BANKING_ACH_REFERENCE.md`.
> Keep addresses here only when a governor explicitly asks to file them for reuse.

---

## Brazil — Ilhéus, Bahia (recipient: Zhiwen Teh)

> Filed 2026-09-12 by Sophia (thread 26920) at Gary's request.
> Source: Gary Teh via Telegram, after setting the address up in Mercado Libre.

### Structured form

```json
{
  "address": {
    "zipCode": "45653005",
    "street": "Avenida Soares Lopes",
    "number": "1590",
    "additionalInformation": "Edf Mansao Dom Eduardo Ap 801"
  },
  "recipient": {
    "fullName": "Zhiwen Teh",
    "phone": ""
  }
}
```

### Human-readable form

Zhiwen Teh  
Av. Soares Lopes, 1590 — Edf. Mansão Dom Eduardo, Ap 801  
Cidade Nova (per CEP range; see note) — Ilhéus, BA  
CEP 45653-005 — Brazil

### Notes / gotchas when filling a form (e.g. Mercado Libre)

- **Street field holds the street name ONLY** (`Avenida Soares Lopes`). Do NOT append the building
  name — postal-database street matching and label printing can fail. Put the building + apartment
  in the complement / "additional information" field (`Edf Mansao Dom Eduardo Ap 801`).
- **Bairro (neighbourhood) is derived from the CEP** by the carrier/ML — there is no separate field.
  Correct the CEP and the auto-resolved neighbourhood line updates on its own.
- **Phone: blank.** Fill in before use (the recipient may not be reachable on a local Ilhéus line).

### CEP corrigendum (verify before printing a label)

Avenida Soares Lopes splits CEP by house number:

| Nº on Av. Soares Lopes | Bairro | CEP |
|---|---|---|
| até 774/775 | Centro | 45653-005 |
| 776 → fim | Cidade Nova | 45652-065 |

Nº **1590** is past 776, so by the postal table it should be **Cidade Nova → 45652-065**, not
Centro 45653-005. **Gary's saved payload uses 45653-005.** If ML/Correios accept 45653-005 for nº 1590
and neighbours use it, it may be fine — but confirm against the Correios logradouros table before relying
on it for a delivery label.

---

## Other saved addresses (for cross-reference)

These already live elsewhere in the workspace; listed here so a future lookup lands in one place:

| Purpose | Address | Source |
|---|---|---|
| Brazil warehouse (canonical, used in scripts) | R. Cel. Paiva, 46 — Centro, Ilhéus - BA, 45653-310 | `PURCHASE_AGREEMENT_PDFS.md`, `plans/AORA_EXPERIENCE_PLAN.md` |
| Brazil export entity (Sertão/cargo docs) | Av. Tancredo Neves, 4900, Qd H, Cs 9, Nossa Senhora da Vitória, Ilhéus, BA, 45655-650 | `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`, `brazil/BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE.md` |
| US ship-to (vendor billing/shipping) | 1423 Hayes St, San Francisco, CA 94117 (TrueTech Inc / Kirsten Ritschel) | `WORKSPACE_CONTEXT.md` §3c |
