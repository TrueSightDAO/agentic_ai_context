# Fumigation NFS-e — ASTRA SUL BAHIA (24/09/2026, R$ 405,00)

**Surfaced by:** Governor (Gary), thread 10800, 2026-10-09.
**Artifact:** `brazil/sources/2026-09-24_black_king_fumigation_nfse_astra.pdf` (NFS-e, 1 page).

## What this document is

A **Nota Fiscal de Serviços Eletrônica (NFS-e)** issued by the municipality of **Itabuna/BA** for a pest-control service. It is a **billing / tax document** — proof the service was *invoiced*, not proof of what was *done*.

| Field | Value |
|---|---|
| Emissão | 24/09/2026 14:59:10 (Brasília) |
| Competência | 09/2026 |
| Prestador | **ASTRA SUL BAHIA SANEAMENTO BÁSICO LTDA** (ASTRAL SAUDE AMBIENTAL) — CNPJ 07.463.430/0001-99 |
| Tomador | **MATHEUS REIS PEREIRA** — CNPJ 50.042.585/0001-80 |
| Município de prestação | Ilhéus – BA |
| Serviço (item 0713) | *Dedetização, desinfecção, desinsetização, imunização, higienização, desratização, pulverização e congêneres* — CNAE 8122200 |
| Valor | **R$ 405,00** (ISS 2,79%) |
| Chave de acesso | `29148021207463430000199202600000029326090186351088` |
| Pagamento | Banco do Brasil AG 0070-1 C/C 218138-0 · PIX 07.463.430/0001-99 |
| Rodapé | *“SERVIÇO DE FUMIGAÇÃO”* |

## ⚠️ NFS-e ≠ fumigation certificate — that is the gap

| Document | What it proves | Who issues | Do we have it? |
|---|---|---|---|
| **NFS-e** (this file) | that ASTRA *billed* a pest-control service | Itabuna municipality | ✅ yes |
| **Fumigation certificate / laudo / comprovante** | **what** was treated, **where**, with **which product + dose**, **when**, against **which pests**, **validity**, by **which licensed technician** | ASTRA (the pest-control firm) | ❌ **no** |

`OPEN_FOLLOWUPS.md` (B2) already flags that the only warehouse artifact is a *bare* fumigation NFS-e “not cited by any assurance”. This certificate is the missing half — the attestation an FDA/FSVP reviewer would expect behind a pest-control line.

## Three distinct things called “fumigation” on this lane (do not conflate)

1. **Warehouse pest-control / dedetização (ASTRA)** — facility hygiene. **Certificate = worth obtaining.** This is the live gap (A4/B2).
2. **Pallet fumigation (ISPM#15)** — applies to **wood** pallets only. Our cargo sat on **plastic HDPE** pallets → **ISPM#15 NOT APPLICABLE, no fumigation cert required** (§7, explicit: *“do not buy a fumigation cert for an exempt pallet”*).
3. **The quoted “Fumigation (3 pallets) R$ 500”** (§7 cost table) — a **pallet** fumigation line that is **likely N/A** given the plastic pallets. Flag as a cost to confirm/drop, not to purchase.

## Address nuance (ties to gap A3)

The NFS-e’s tomador address is **Av. Tancredo Neves, 4900** (the *registered* address) — **not** the storage site **R. Cel. Paiva, 46**. The certificate should state the **actually treated address**, which also helps close the “two storage addresses, no stated linkage” gap (A3).

## Cost-reconciliation gap

§5.9 open-item #3 (cost reconciliation) lists **cintagem R$ 300 + possible diária R$ 1.350/day + airline reissue** — it **does not include this R$ 405**. If the 24/09 fumigation was export prep, it belongs in the reconciled shipment cost. Confirm with Matheus whether this was (a) routine facility pest-control or (b) shipment-prep fumigation.

## Request to make (draft — pending governor go)

Ask for the **fumigation certificate / comprovante / laudo** for the 24/09/2026 service, citing the NFS-e chave above, stating: treated address, product + active ingredient + dose, target pests, date, validity/next-due, and the responsible technician (with registration/ART if applicable).

**Routing note:** ASTRA’s customer of record (tomador) is **Matheus**, so the firm may release the certificate only to him — likely fastest to have **Matheus request it** rather than approach ASTRA cold.

## Cross-references
- `OPEN_FOLLOWUPS.md` — Black King warehouse-maintenance & pest-control written-assurance addendum (B2); fumigation NFS-e registration (A4).
- `brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md` — A3 (two addresses), A4 (register NFS-e), B2 (addendum), C2 (pest-control cadence).
- `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` — §7 (pallet fumigation line), §5.9 (open items).

## 2025 counterpart — same vendor, same service, 15 months earlier

Found in `fda_fsvp/suppliers/black_king/20250610_warehouse_fumigation.pdf`. **Byte-comparison shows it is the same document *type* from the same issuer** (municipal NFS-e, Itabuna/BA).

| Field | **2025-06-10** | **2026-09-24** | Δ |
|---|---|---|---|
| Prestador | ASTRA SUL BAHIA (CNPJ 07.463.430/0001-99) | identical | — |
| Serviço | 0713 · CNAE 8122200 (dedetização etc.) | identical | — |
| Tomador | Matheus Reis Pereira (50.042.585/0001-80) | identical | — |
| Tomador address | Av. Tancredo Neves, 4900 | identical | — |
| Município de prestação | **Ilhéus – BA** | **Ilhéus – BA** | — |
| **Value** | **R$ 300,00** | **R$ 405,00** | **+35%** |
| Payment proof on file | ✅ PIX comprovante | ❌ **none** | ⚠️ |

### Finding 1 — the "cadence" is still NOT evidenced (FSVP B2/C2 stays OPEN)

Two services, **09/06/2025 → 24/09/2026 ≈ 15½ months apart**. Two data points at an irregular interval do **not** demonstrate a *schedule*. The FSVP written-assurance addendum (B2) and the pest-control-cadence action (C2) require a **documented recurring cadence** — this pair is the opposite: it suggests the treatment is **ad hoc**. **Recommendation:** when requesting the certificate, also ask ASTRA for the **service contract / planned cadence** (or state plainly that there is none), so the assurance letter can say what is actually true.

### Finding 2 — the NFS-e itself places the service in **Ilhéus** (helps close gap A3)

The tomador *street* address is the **registered** one (Av. Tancredo Neves, 4900 — matching `entity.json` exactly: *"Avenida Tancredo Neves, 4900, Quadra H, Casa 9"*). **But the `Município de Prestação do Serviço` field reads `Ilhéus - BA`.** That independently corroborates that the treatment was **rendered in Ilhéus** — the municipality where the **R. Cel. Paiva, 46** storage site sits. So the "two storage addresses, no stated linkage" gap (A3) has partial evidence already: the service municipality is Ilhéus; only the street needs confirming on the certificate. *(Register in `entity.json` per A4.)*

### Finding 3 — who actually paid? A reimbursement pattern worth naming

The 2025 file's `20250610_fumigation_invoice.jpeg` is **not an invoice — it is a PIX comprovante**: **Zhiwen Teh (Gary) → Matheus Reis, R$ 300,00, 10/06/2025 19:37**, Nu Pagamentos. So in 2025 the **DAO-side governor paid** a bill invoiced to Matheus.

⚠️ **No payment proof exists for the 2026 R$ 405.** Open item: was it paid, by whom, and does it belong in the shipment cost reconciliation (§5.9 item 3)?

### Finding 4 — CNPJ status records are consistent (no contradiction)

`fda_fsvp/suppliers/black_king/entity.json` says `cadastral_status: "Ativa"`, but its `compiled_at` is **2026-05-26** — which **predates** the INAPTO date of **08/06/2026**. The two records are therefore consistent in time, not contradictory. Worth stating plainly so nobody later mistakes the stale `Ativa` for a live fact.

## Note
This is a record of a document the governor surfaced. Nothing was sent and no payment was made or implied.
