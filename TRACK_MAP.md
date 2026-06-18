# TrueSight DAO — Active Track Map

> **Live dependency map.** Updated as tracks shift. Tracks 1–4 (Vault & Key Registry, Chocolate Subscriptions Phase 1, Edgar/Perch Separation, Partner Onboarding) are **completed** and removed from this map.

---

## Dependency Overview

```mermaid
flowchart TD
    G[Graeme Read / Amazon Restoration Partnership]:::new
    T5[Legal Entity Structuring]:::offline
    T6[GACC / Brazil Compliance]:::offline
    T7[Brazil Export Entity<br/>CNPJ / NF-e / CNAE]:::gate --> T8
    T7 --> T9
    T7 --> T10
    T7 --> T11
    T7 --> T12
    T8[Chocolate Subscription Delivery]:::blocked
    T9[China / Aora Events<br/>100 chocolate bars]:::blocked
    T10[Chives Root Consignment<br/>10 bags ceremonial cacao]:::blocked
    T11[Michael Johnson Consignment]:::blocked
    T12[Kopi Bar Jul 10 Tasting<br/>Nora Haron]:::blocked

    classDef gate fill:#e74c3c,color:#fff,stroke:#c0392b,stroke-width:2px
    classDef blocked fill:#f39c12,color:#fff,stroke:#e67e22
    classDef offline fill:#95a5a6,color:#fff
    classDef new fill:#3498db,color:#fff
```

---

## Track Details

### Legal Entity Structuring {#legal-entity-structuring}

| Field | Detail |
|-------|--------|
| **Status** | 🟡 Offline research |
| **Owner** | Gary / Paloma |
| **Goal** | Choose holding entity structure (DUNA vs Próspera) for DAO-owned Brazilian export CNPJ |
| **Key docs** | [`BRAZIL_EXPORT_ENTITY_BRIEF.md`](./BRAZIL_EXPORT_ENTITY_BRIEF.md) — full structuring brief with two paths (Próspera HoldCo vs Wyoming UNA/DUNA), ownership mapping to TDG holders, and questions for counsel Layon Costa |
| **Next milestone** | Mon Jun 22, 2026 · 11am PDT — call with Layon Costa (counsel), Breno, Paloma. [Google Meet](https://meet.google.com/eht-bdgp-tdh) |
| **Dependencies** | None — parallel work |
| **Blocks** | None — parallel to all other tracks |

---

### GACC / Brazil Compliance {#gacc-brazil-compliance}

| Field | Detail |
|-------|--------|
| **Status** | 🟡 Offline prep |
| **Owner** | Gary / Paloma |
| **Goal** | Regulatory filing prep for Brazil-to-China cacao export (GACC registration). This is a **prerequisite** for exporting to China — separate from the Aora events themselves. |
| **Key docs** | [`BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE.md`](./BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE.md) — GACC registration requirements and process |
| **Dependencies** | None — parallel work |
| **Blocks** | None — parallel to all other tracks |

---

### Brazil Export Entity (CNPJ / NF-e / CNAE) ← THE GATE {#brazil-export-entity}

| Field | Detail |
|-------|--------|
| **Status** | 🔴 Critical blocker |
| **Owner** | Matheus / Paloma / Gary |
| **Goal** | Create new Brazilian CNPJ with correct CNAE (46.23-1/04 — wholesale cacao trade), Inscrição Estadual (IE) at SEFAZ-BA, and NF-e model 55 credentialing. Replace Black King's personal CNPJ as the export vehicle. |
| **Expected timeline** | **5–20 business days** to change/add CNAE for a Microempresa (ME). Cost: R$400–R$2,100 depending on state and accounting services. [Source: Matheus, 2026-06-19](https://github.com/TrueSightDAO/.github/blob/main/attachments/2026-06-19_matheus_cnae_timeline.jpg) |
| **Next check-in** | **~2026-06-26** (5 business days from 2026-06-19) — earliest possible completion |
| **Key docs** | [`BRAZIL_EXPORT_ENTITY_BRIEF.md`](./BRAZIL_EXPORT_ENTITY_BRIEF.md) — explains why Black King's current CNPJ (service CNAEs only, no IE, no NF-e model 55) cannot legally issue export invoices. See §4 for the full diagnosis. |
| **Context** | Current state: Black King (CNPJ 50.042.585/0001-80) is an Empresário Individual with only service CNAEs (82.30-0-01). Cannot issue export NF-e. New entity needs CNAE 46.23-1/04 + IE + NF-e model 55 credentialing at SEFAZ-BA. |
| **Downstream chain** | Matheus (CNPJ/NF-e/CNAE) → Omega Services (logistics) → SeaCoast Logistics (freight) → Kirsten (receives) |
| **Dependencies** | None — parallel to [Legal Entity Structuring](#legal-entity-structuring) and [GACC / Brazil Compliance](#gacc-brazil-compliance) |
| **Blocks** | [Chocolate Subscription Delivery](#chocolate-subscription-delivery), [China / Aora Events](#china-aora-events), [Chives Root Consignment](#chives-root-consignment), [Michael Johnson Consignment](#michael-johnson-consignment), [Kopi Bar Jul 10 Tasting](#kopi-bar-jul-10-tasting) |

---

### Chocolate Subscription Delivery {#chocolate-subscription-delivery}

| Field | Detail |
|-------|--------|
| **Status** | 🟡 Blocked |
| **Owner** | Gary / Linda (first subscriber) |
| **Goal** | Fulfill chocolate bar subscriptions. Phase 1 (subscribe engine + PDPs + homepage card) is built and merged. Phase 2 (fulfillment automation) deferred until export entity clears. |
| **Key docs** | [`CHOCOLATE_SUBSCRIPTION_PLAN.md`](./CHOCOLATE_SUBSCRIPTION_PLAN.md) — full subscription plan with Phase 1/2 split |
| **Dependencies** | 🔴 **Blocked by** [Brazil Export Entity](#brazil-export-entity) — cannot ship bars without legal export |

---

### China / Aora Events (100 chocolate bars) {#china-aora-events}

| Field | Detail |
|-------|--------|
| **Status** | 🟡 Blocked |
| **Owner** | Gary / Elizabeth Wong (Liz) / Jerri |
| **Goal** | Aora pilot in China with GO/Nucleus network. 100 chocolate bars (50g, 81% cacao) for experiential learning events. Gary backpack-carry to China. |
| **Key docs** | [`AORA_EXPERIENCE_PLAN.md`](./AORA_EXPERIENCE_PLAN.md) — full execution roadmap with PERT chart, critical path, revenue model ($10 retail, $6 back to DAO), and blocker table |
| **Event plan** | Jerri shared a 40-page detailed event plan (Jul 2026 beta + Autumn public launch). [Full PDF](https://github.com/TrueSightDAO/.github/blob/main/attachments/2026-06-19_aora_agroverse_event_plan.pdf) |
| **July beta** | 10-15 seed families (ages 6-12), co-invited by Teacher Evan + Liz. 90-min immersive experience. Gary as "Guardian of the Cacao Rainforest." 4-tier technical plan (1C recommended: 1 projector + 6 scenes). 15-item risk register. |
| **Dependencies** | 🔴 **Blocked by** [Brazil Export Entity](#brazil-export-entity) — bars must be produced in Brazil and exported legally |

---

### Chives Root Consignment (10 bags ceremonial cacao) {#chives-root-consignment}

| Field | Detail |
|-------|--------|
| **Status** | 🟡 Blocked |
| **Owner** | Chives Root / Gary |
| **Goal** | Ship 10 bags of ceremonial cacao to Chives Root for consignment-based sales |
| **Dependencies** | 🔴 **Blocked by** [Brazil Export Entity](#brazil-export-entity) — bags must be exported from Brazil first |

---

### Michael Johnson Consignment {#michael-johnson-consignment}

| Field | Detail |
|-------|--------|
| **Status** | 🟡 Blocked |
| **Owner** | Michael Johnson / Gary |
| **Goal** | Ship ceremonial cacao to Michael Johnson for consignment-based sales |
| **Dependencies** | 🔴 **Blocked by** [Brazil Export Entity](#brazil-export-entity) — bags must be exported from Brazil first |

---

### Kopi Bar Jul 10 Tasting (Nora Haron) {#kopi-bar-jul-10-tasting}

| Field | Detail |
|-------|--------|
| **Status** | 🟡 Blocked |
| **Owner** | Nora Haron / Gary |
| **Goal** | Organize a chocolate tasting event at Kopi Bar on July 10. Nora wants to host. |
| **Dependencies** | 🔴 **Blocked by** [Brazil Export Entity](#brazil-export-entity) — chocolate bars must clear the full supply chain first |

---

### Graeme Read / Amazon Restoration Partnership {#graeme-read}

| Field | Detail |
|-------|--------|
| **Status** | 🔵 New / Exploratory |
| **Owner** | Gary / Graeme Read / Jonathan Hakem |
| **Goal** | Explore partnership with Graeme Read — fellow contributor restoring 10,000 hectares of Amazon rainforest through single-estate cacao, QR traceability, and community dashboard at truesight.me. Nearly identical mission. |
| **Key docs** | [Introduction screenshot](https://github.com/TrueSightDAO/.github/blob/main/attachments/2026-06-19_graeme_read_introduction.jpg) — Jonathan Hakem intro via WhatsApp |
| **Dependencies** | None — exploratory |
| **Blocks** | None |

---

## Quick Reference

| Track | Status | Owner | Next Check-in | Blocked By |
|-------|--------|-------|---------------|------------|
| Legal Entity Structuring | 🟡 Offline | Gary / Paloma | Jun 22 call w/ Layon | — |
| GACC / Brazil Compliance | 🟡 Offline | Gary / Paloma | — | — |
| Brazil Export Entity (CNPJ/NF-e/CNAE) | 🔴 Gate | Matheus / Paloma / Gary | ~2026-06-26 | — |
| Chocolate Subscription Delivery | 🟡 Blocked | Gary | — | Brazil Export Entity 🔴 |
| China / Aora Events (100 bars) | 🟡 Blocked | Gary / Liz / Jerri | — | Brazil Export Entity 🔴 |
| Chives Root Consignment (10 bags) | 🟡 Blocked | Chives Root / Gary | — | Brazil Export Entity 🔴 |
| Michael Johnson Consignment | 🟡 Blocked | Michael Johnson / Gary | — | Brazil Export Entity 🔴 |
| Kopi Bar Jul 10 Tasting | 🟡 Blocked | Nora / Gary | 2026-07-10 | Brazil Export Entity 🔴 |
| Graeme Read / Amazon Restoration Partnership | 🔵 New | Gary / Graeme / Jonathan | — | — |

---

*Last updated: 2026-06-19. Update this file when track statuses change.*
