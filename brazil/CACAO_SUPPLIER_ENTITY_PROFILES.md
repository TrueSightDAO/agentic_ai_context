# Cacao Supplier Entity Profiles — canonical reference

> **Purpose:** one page answering "who is X, what are their IDs, what can they do,
> what is blocking them, where are their documents" for the four core Agroverse
> cacao entities — **CEPOTX**, **COOPERCABRUCA**, **Santos**, and **Black King**.
> Consolidates the machine-readable `fda_fsvp/suppliers/*/entity.json` profiles,
> the sourcing-network overview, the Black King manifests & NF-e crosswalk, the
> CEPOTX site-code registry, and the Santos/USA production spec into one
> human-readable page.
>
> **Prepared:** 2026-10-14 | **Prepared by:** Sophia Truesight (TrueSight DAO Autopilot)
>
> **Privacy:** entity-level identifiers only (CNPJ / DUNS / FDA-FFR). No personal
> CPFs and no FDA registration PINs are reproduced — consistent with the
> `fda_fsvp` convention. Contacts shown are business contacts already public in
> the DAO repos.

---

## Quick reference — all four at a glance

| | **CEPOTX** | **COOPERCABRUCA** | **Santos** | **Black King** |
|---|---|---|---|---|
| **Type** | Organic cacao coop (Pará) | Regional cacao coop (Bahia) | Bean-to-bar factory (Bahia) | Exporter / trader + warehousing |
| **Principal** | Jader A. da Silva Santos (Pres.) | Orlantildes Santos Pereira (Pres.) | José Carlos ("Santos") | Matheus Reis Pereira |
| **Location** | Altamira, PA | Itabuna, BA | Bahia (Itabuna–Ilhéus circuit) | Ilhéus, BA |
| **CNPJ** | 22.568.369/0001-38 | 31.948.811/0001-42 | — (facility, not a supplier CNPJ on file) | 50.042.585/0001-80 |
| **DUNS** | 903842053 | 946690515 | — | 628340898 |
| **FDA FFR** | 14674182470 | 17660066140 | — | 19088052616 |
| **FDA FSVP status** | VALID (exp. 2026-12-31) | VALID (exp. 2026-12-31) | not an FSVP supplier of record | VALID (exp. 2026-12-31) |
| **MAPA** | applying | ✅ completed 2026-09-02 | n/a | n/a |
| **GACC (China)** | not obtained | not obtained | n/a | not obtained |
| **Role** | Beans + emerging in-network conversion | Conversion + export hub | Converts beans → finished bars | Export coordination + warehousing |
| **Status** | 🟢 Active lane | 🟢 Active lane | 🟡 Planning | 🔴 Blocker (CNPJ INAPTA) |

---

## 1 · CEPOTX — Cooperativa Central de Produção Orgânica da Transamazônica e Xingu

**An organic cacao cooperative based in Altamira, Pará, coordinating four member
cooperatives across the Transamazônica/Xingu region.** Supplies organic cacao
*almonds* (amêndoas de cacau) and — as of Sep 2026 — has begun to build
in-network bean-to-bar conversion capability.

### Identity & identifiers

| Field | Value |
|---|---|
| Legal name | COOPERATIVA CENTRAL DE PRODUCAO ORGANICA DA TRANSAMAZONICA E XINGU |
| Trade name | CEPOTX |
| Legal form | Cooperativa (natureza jurídica 214-3) |
| CNPJ | 22.568.369/0001-38 |
| DUNS | 903842053 |
| FDA FFR number | 14674182470 |
| Registration | opened 2015-06-01 · cadastral status **ATIVA** |
| Address | Avenida Perimetral, 3966, SUDAM II, Altamira, PA 68.374-274, Brazil |

### Contacts

| Contact | Role | Channel |
|---|---|---|
| Jader Adriano da Silva Santos | President (per Rota do Cacau) | — |
| Jedielcio Oliveira | Técnico, Diretoria | — |
| CEPOTX accounting | general | marcelcontabilidade@gmail.com · +55 93 3515-1453 / +55 93 9189-2322 |
| CEPOTX organic desk | general | cepotx.organicos@gmail.com |

### Products & capability

- **Supplies:** organic cacao almonds (amêndoas de cacau).
- **Emerging conversion:** in-network bean-to-bar now exists — **Fazenda Cleide
  factory** (fermentation → roast → winnow → melanger → press → mould → cold-hold,
  visited 2026-09-08) and **La do Sítio stage-1** (roast/winnow/cold-hold, visited
  2026-09-07). Export-scale conversion is still unproven; Bahia remains the
  conversion/export hub for scale.

### Network structure

CEPOTX coordinates **four member cooperatives**:

| Prefix (site codes) | Cooperative | Location | Note |
|---|---|---|---|
| U-06-NN | **COPOPS** — Cooperativa de Produtos Orgânicos de Perpétuo Socorro | Uruará, PA | has its own entity profile (CNPJ 08.578.736/0001-53) |
| B-06-NN | **COOPOXIN** | Pará | largest captured roster |
| N-06-NN | **COOPCAO** | Pacajá region, PA | — |
| — | **COPOTRAN** | Pará | roster not yet captured |

Site codes follow the `X-06-NN` scheme; **one code per property, not per person**
(a producer may hold several). Full producer rosters + anchor farms live in
`CEPOTX_SITE_CODE_REGISTRY.md`. Prefix-letter meaning is **not yet documented —
do not decode or derive**.

### Certifications

| Scheme | Detail |
|---|---|
| **USDA NOP organic** (7 CFR Part 205) | IMOcert Latinoamerica · client `26 11336 NOP` · **certificate 6400011336** · effective 2026-10-02 · anniversary 2027-07-05 · scopes Crops + Handling · **50 growers** · ~347.40 ha cacao (113,235.41 kg) + 111,536.88 kg processed almonds |
| FITOSanitário | held |
| CIC or CVACBA | held |

> ⚠️ Individual farm organic claims (e.g. Sítio Raimundo & Geniza "IBD NOP
> since 2006") rest on **farmer narration only** — treat as unverified until the
> IBD certificate document is received (see `20260910_RFQ_cepotx_600kg_raimundo_geniza.md` §4).

### Regulatory registrations

| Regime | Status |
|---|---|
| FDA FSVP (importer TrueTech Inc) | **VALID** · created 2024-06-28 · expires 2026-12-31 · written assurance + supplier evaluation on file |
| MAPA (Brazil export) | **applying** (per RFQ 2026-09-10) |
| GACC (China) | **not obtained** (3–6 mo estimated) |

### Source farms (representative)

Paulo — La do Sítio (V-06-29) · Fazenda Cleide (B-06-108, COOPOXIN) · Santa Anna
Fazenda (B-06-58, COOPOXIN) · Sítio Raimundo & Geniza (U-06-07, COPOPS) · Fazenda
Santa Rosa (U-06-06, COPOPS) · Fazenda Dona Rosa (Medicilândia, pending code) ·
Sítio Torres (N-06-66, COOPCAO) · Sítio Cacau na Veia (N-06-37, COOPCAO).

### Key documents

- Machine profile: `fda_fsvp/suppliers/cepotx/entity.json`
- Roster / site codes: `fda_fsvp/suppliers/cepotx/site_codes.md`, `CEPOTX_SITE_CODE_REGISTRY.md`
- Open RFQ: `fda_fsvp/suppliers/cepotx/20260910_RFQ_cepotx_600kg_raimundo_geniza.md`
- Organic certificate: `20261002_CEPOTX_usda_nop_organic_certificate.pdf`
- Site-visit PDFs (2024 & 2026 series) under `fda_fsvp/suppliers/cepotx/`

### Open issues

- GACC registration not obtained; raw-bean lane needs a China-side warehouse.
- MAPA export-registration number pending (blocks port-of-entry confirmation).
- B-06-56 vs B-06-58 discrepancy on Ana Lucia Araujo — verify with CEPOTX before legal use.

---

## 2 · COOPERCABRUCA — Cooperativa dos Cacauicultores do Sul da Bahia

**A regional cacao cooperative in southern Bahia, and one of Agroverse's earliest
verified suppliers (initial site visit 2023-06).** Operates the conversion +
export hub for the Bahia lane.

### Identity & identifiers

| Field | Value |
|---|---|
| Legal name | COOPERATIVA DOS CACAUICULTORES DO SUL DA BAHIA - COOPERCABRUCA |
| Trade name | COOPERCABRUCA |
| Legal form | Cooperativa (natureza jurídica 214-3) |
| CNPJ | 31.948.811/0001-42 |
| DUNS | 946690515 |
| FDA FFR number | 17660066140 |
| Registration | opened 2018-10-30 · status **ATIVA** · primary CNAE 10.93-7-01 (cocoa/chocolate products) |
| Address | Travessa Belo Horizonte, 166, Pontalzinho, Itabuna, BA 45.603-070, Brazil |

### Contacts

| Contact | Role | Channel |
|---|---|---|
| Orlantildes Santos Pereira | President / CEO | — |
| Coopercabruca | general | coopercabruca@gmail.com · +55 73 9138-8884 |

### Products & capability

- **Supplies:** cacao nibs, cacao mass, cacao molasses.
- **Hub role:** has IE + NF-e; **all chocolate factories and the DAO warehouse are
  here**; roasting can **only** happen here regardless of source region.
- **Constraint:** converts/exports beans from **own members only**; does **not**
  provide warehousing; needs the exact SKU spec upfront.

### Source farms

Fazenda Santa Ana (USDA Organic certified) · Fazenda Analuana · Fazenda São Jorge.

### Certifications

FITOSanitário · CIC (Cacao Innovation Center) · IBD NOP organic.

### Regulatory registrations

| Regime | Status |
|---|---|
| FDA FSVP (importer TrueTech Inc) | **VALID** · created 2023-09-17 · expires 2026-12-31 |
| MAPA (Brazil export) | ✅ **COMPLETED 2026-09-02** |
| GACC (China) | **not obtained** · self-application pathway (Decree 280) — see the GACC guide below |

### Key documents

- Machine profile: `fda_fsvp/suppliers/coopercabruca/entity.json`
- China registration guide: `brazil/BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE_COOPERCABRUCA.md`
- Initial site visit + assurance/evaluation letters (2023 & 2024 series) under `fda_fsvp/suppliers/coopercabruca/`

### Open issues

- GACC registration not yet obtained (critical path for the China lane).
- Needs exact SKU/packaging spec before conversion can be scheduled.

---

## 3 · Santos (José Carlos) — Bahia bean-to-bar chocolate factory

**A craft bean-to-bar chocolate processor in the Bahia (Itabuna–Ilhéus) circuit,
run by José Carlos ("Santos"), a 40+ year veteran of the Bahian cacao industry.**
Relayed to the DAO through **Fatima Toledo**. This is the conversion partner for
the proposed USA finished-bar arrangement.

> ⚠️ **Thinnest profile of the four.** Much of what follows comes from a single
> planning spec (`brazil/USA_SANTOS_PRODUCTION_SPEC.md`) and the Bahia site-visit
> deck. Treat commercial terms as *indicative*, not contracted.

### Identity

| Field | Value |
|---|---|
| Principal | **José Carlos ("Santos")** — 40+ yr Bahia cacao veteran |
| Entity type | Bean-to-bar chocolate factory / converter (not a cacao-supplier CNPJ on file) |
| Location | Bahia — on the Itabuna / Ilhéus circuit |
| Relayed via | **Fatima Toledo** (Bahia relationships) |
| Supplier CNPJ / DUNS / FFR | — (not held in the DAO records; facility profile, not an FSVP supplier) |

### Products & capability

- Converts cacao beans → **finished chocolate bars** (currently scoped at **81%
  cacao / 50 g**, engineered in the **Cabrellon Italian polycarbonate mold**, 4
  cavities × 50 g).
- Small-batch craft scale; capacity to confirm for a **100 kg (~2,000 bar)** batch.

### Proposed arrangement (USA lane — PLANNING PHASE)

| Question | Answer |
|---|---|
| What | 81% cacao, 50 g chocolate bars for the USA market |
| How much | **100 kg** (≈2,000 bars) per batch |
| How often | **Twice a year** — Mar 20 & Sep 20 (equinoxes, Brazil) |
| We provide | Cacao beans + Cabrellon mold (delivered via Matheus / Black King) + Agroverse-branded outer packaging |
| Santos provides | Production labor (bean-to-bar) + internal food-grade foil |
| Santos returns | ≈2,000 finished bars + cacao-tea residue + our mold |
| Prior quote | **R$130/kg for 70% bars** (reference only; not locked for 81%/50 g) |

> 🛑 **Viability gate:** no production begins until **last year's bars arrive in
> San Francisco and are inspected** for transit survival / quality / shelf state.

### Contract/source documents

- `brazil/USA_SANTOS_PRODUCTION_SPEC.md` (the requirement spec)
- `agroverse/BEAN_TO_BAR_EQUIPMENT_INVENTORY.md` (equipment tier for the format)
- Bahia circuit deck: `handoffs/liz_bahia_deck/` (site visit 30 Sep)
- Related Coopercabruca record: `20240814_Coopercabruca_site_visit_santos_factory.pdf`

### Open items (to review with Santos via Fatima)

1. **Viability gate** — pending inspection of last year's bars in SF.
2 — **Capacity** — can Santos hit 100 kg (~2,000 bars) in one equinox cycle?
3. **Pricing** — per-cycle price for 81% / 50 g at 100 kg volume.
4. **Foil** — confirm food-grade internal foil suitable for 50 g bars.
5. **Lead time** — how far ahead must beans + mold arrive?
6. **Mold count** — is one Cabrellon mold sufficient, or are more needed?

---

## 4 · Black King — Matheus Reis Pereira

**The individual CNPJ of Matheus Reis Pereira, operating as "Black King" — the
Brazilian export coordinator, trader, and warehouser for the DAO's Bahia
corridor.** Handles moving beans + molds to Santos and exporting finished goods.
This is the de-facto vehicle currently used for Brazilian cacao exports, and is
intended to be relieved by a dedicated DAO-owned Brazilian entity.

### Identity & identifiers

| Field | Value |
|---|---|
| Legal name | MATHEUS REIS PEREIRA |
| Trade name | BLACK KING |
| Legal form | Empresário Individual (micro-enterprise; Simples Nacional) |
| CNPJ | 50.042.585/0001-80 |
| DUNS | 628340898 |
| FDA FFR number | 19088052616 |
| Registration | opened 2023-03-22 · status **Ativa** · share capital R$ 10,000 |
| Registered address | Avenida Tancredo Neves, 4900, Quadra H, Casa 9, Nossa Senhora da Vitória, Ilhéus, BA 45655-650, Brazil |
| Warehouse (operational) | R. Cel. Paiva, 46 – Centro, Ilhéus, BA 45653-310 |

### Contacts

| Contact | Role | Channel |
|---|---|---|
| Matheus Reis Pereira | Owner / Empresário | theus.reis.ssa@gmail.com · +55 73 99109-0002 |

### Products & capability

- **Supplies:** cacao nibs, cacao mass, cacao molasses, cacao tea, cacao husk,
  ceremonial cacao, caramelized cacao.
- **Logistics / warehousing:** operates the **Ilhéus warehouse**; offers Bahia
  warehousing **in exchange for DAO tokens** (lets the DAO stockpile multi-year
  and sense demand before committing to a conversion/SKU).
- **Coordinator:** delivers cacao beans + the Cabrellon mold to Santos each
  production cycle, and exports the finished bars.

### Source farms

Oscar Martins da Silva Miranda (CNPJ 57.563.732/0001-07, Ubatã, BA) · Fazenda Clara ·
Fazenda Analuana · Vivi / Jesus do Deus (Itacaré) · Fazenda São Jorge · Fazenda
Capela Velha.

### Certifications

FITOSanitário · CIC (Cacao Innovation Center) · IBD NOP organic.

### Regulatory registrations & status

| Regime | Status |
|---|---|
| FDA FSVP (importer TrueTech Inc) | **VALID** · created 2024-09-07 · expires 2026-12-31 |
| GACC (China) | not obtained |
| **CNPJ (Receita Federal)** | 🔴 **INAPTA since 2026-06-08** — omissão de declarações (2+ yrs of missed DCTF/ECF/ECD/DAS) |
| e-CNPJ | expired |
| CNAE | service only (82.30-0-01) — **no commerce/export CNAE**; no Inscrição Estadual (IE); no NF-e model 55 credentialing at SEFAZ-BA |

> 🔴 **Corridor blocker:** because of the INAPTA status + missing IE/NF-e
> credentialing, **no export NF-e can be issued** — this blocks every channel
> routed through Black King. Requires CNAE **46.23-1/04** (wholesale cacao),
> IE at SEFAZ-BA, and NF-e model 55 credentialing to clear.

### Commercial — shipment manifests

- **US lane totals** (Rev 9): **182.67 kg · USD 4,884.60** origin value (excl.
  never-shipped Shipments 8 & 13, per governor ruling).
- **15 SEFAZ-issued NF-e** cross-walked to the arrival register (the two sources
  share no common key — see the crosswalk).
- Non-US lanes also recorded: **Europe** (Poland, Switzerland/Zurich) and
  **FounderHaus** (Brazil-domestic).

### Key documents

- Machine profile: `fda_fsvp/suppliers/black_king/entity.json`
- Manifests + origin unit costs: `BLACK_KING_SHIPMENT_MANIFESTS.md` (`black_king_shipments.json`)
- NF-e ↔ transit crosswalk: `BLACK_KING_NFE_TRANSIT_CROSSWALK.md`
- Correios index: `CORREIOS_SHIPMENTS.md`
- Warehouse management: `brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md`
- DANFE PDFs: `fda_fsvp/suppliers/black_king/notas_fiscais/`

### Open issues

- CNPJ INAPTA / e-CNPJ expiry / missing export CNAE + IE + NF-e credentialing — the corridor's #1 bottleneck.
- Two storage addresses on file (Av. Tancredo Neves 4900 per FFR vs R. Cel. Paiva 46 per site visit) — linkage to be reconciled.
- FSVP gap: no CAPA record on file (see `OPEN_FOLLOWUPS.md`).

---

## 5 · How the entities relate

```
   FARM / COOP SOURCES                     CONVERSION / EXPORT (Brazil)          IMPORT (US)
   ─────────────────────                   ────────────────────────────          ───────────
   CEPOTX (Pará, organic)   ─┐
   COOPERCABRUCA (Bahia)    ─┼─►  Black King (Matheus)  ──┐
   member coops (COPOPS…)   ─┘    export coordination     ├─►  TrueTech Inc  ─►  US retailers
                                 + Ilhéus warehousing     │    (Delaware C-corp,
                                                          │     FSVP + CBP
                       Santos (José Carlos) ─────────────┘     importer of record)
                       bean-to-bar converter (Bahia)
                                                          │
                          (Holding co leg)  TrueSight DAO LLC (Próspera ZEDE)
```

### Shared network identifiers

| Entity | Role | Key IDs |
|---|---|---|
| **TrueTech Inc** | US FSVP + CBP importer of record | EIN **88-3411514** · CBP IOR 88-341151400 · FDA FFR 12202640780 · DUNS 119035208 |
| **TrueSight DAO LLC** | Holding / trading co (Próspera ZEDE) | Próspera resident permit 86901452542528 |
| **COPOPS** | CEPOTX member cooperative (own FSVP entity) | CNPJ 08.578.736/0001-53 |

### Geography (map coordinates)

| Site | Lat | Lng |
|---|---|---|
| Altamira, PA (CEPOTX) | -3.204065 | -52.209961 |
| Itabuna, BA (Coopercabruca / Santos) | -14.793173 | -39.275034 |
| Ilhéus, BA (Black King) | -14.792599 | -39.045384 |

---

## 6 · Canonical sources

| Domain | Source of truth |
|---|---|
| Machine-readable entity profiles | `TrueSightDAO/fda_fsvp` → `suppliers/<name>/entity.json` + `entities.index.json` |
| Network overview & lanes | `brazil/CACAO_SOURCING_NETWORK_OVERVIEW.md` |
| CEPOTX rosters / site codes | `CEPOTX_SITE_CODE_REGISTRY.md`, `fda_fsvp/suppliers/cepotx/site_codes.md` |
| Black King manifests / NF-e | `BLACK_KING_SHIPMENT_MANIFESTS.md`, `BLACK_KING_NFE_TRANSIT_CROSSWALK.md` |
| Santos production spec | `brazil/USA_SANTOS_PRODUCTION_SPEC.md` |
| Brazil export structuring | `briefs/BRAZIL_EXPORT_ENTITY_BRIEF.md` |
| China registration | `brazil/BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE_COOPERCABRUCA.md` |

---

*Prepared by Sophia Truesight (TrueSight DAO Autopilot) — 2026-10-14. Update this
page when an entity's identifiers, registrations, or role change; keep the
machine-readable `entity.json` files as the field-level source of truth.*
