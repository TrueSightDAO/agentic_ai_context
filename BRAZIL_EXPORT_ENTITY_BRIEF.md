# Brazil Export Entity — Structuring Brief

**TrueSight DAO / Agroverse**
**Prepared for Paloma — FounderHaus (to brief introduced legal counsel)**
**Date: 26 May 2026**
**Classification: Confidential**

---

## 1 · Purpose

TrueSight DAO operates Agroverse, a regenerative-agriculture network. The venture being formalised is a bot-enabled agricultural export bridge from Northern Brazil — beginning in the cacao-producing regions of Bahia and Pará — that moves verified produce from farming cooperatives and producers to buyers abroad.

The first destination market — the United States — is already fully formalised on the import side under a Delaware company, TrueTech Inc, the FDA-FSVP importer of record and the US Customs importer of record. We also intend to export to China and Europe, each served by its own dedicated importer entity.

The Brazilian export side is not yet formalised in a dedicated entity. Today, exports leave Brazil through the personal CNPJ of Matheus Reis Pereira (trading as "Black King"). That arrangement does not scale, concentrates Brazilian tax exposure on an individual, and cannot be operated by software agents.

---

## 2 · Executive Summary

We are evaluating two structural paths for the holding entity that will own the Brazilian export CNPJ. Both solve the same problem — replacing Matheus's personal CNPJ with a dedicated, DAO-owned export entity — but through different jurisdictions and at different cost/complexity.

**Path A — Próspera HoldCo (original proposal):** Incorporate in the Próspera ZEDE (Honduras special economic zone) as the holding company owning the Brazilian export CNPJ.

**Path B — Wyoming UNA/DUNA (alternative):** Form a Wyoming Unincorporated Nonprofit Association (UNA) via OtoCo (~$50 gas, this week) which can later convert to a Decentralized Unincorporated Nonprofit Association (DUNA). The UNA/DUNA would own the Brazilian export CNPJ directly.

**Decision question for counsel:** Can a Wyoming UNA/DUNA legally own a Brazilian Ltda (CNPJ) as a foreign quotaholder? If yes, Path B is simpler and cheaper. If no, we proceed with Path A (Próspera HoldCo) as the final holding entity.

**In one line (either path):**
> DAO contributors → [Holding Entity] → Brazilian Export CNPJ (RADAR + Siscomex), Bahia & Pará → dedicated importers: US (TrueTech Inc, live), China & Europe (TBD) → Agroverse reseller network.

---

## 3 · Background

### TrueSight DAO
A values-driven, open-source organisation building social ventures and recording its operations transparently (governance, treasury, and supply-chain data are published publicly). Agroverse is its flagship program.

### Agroverse
A regenerative-agriculture network connecting Northern-Brazilian (Amazonian and Bahian) farmers and cooperatives directly to conscious buyers. The network handles farm onboarding, FDA/FSVP certification, community warehousing in Brazil and abroad, and last-mile distribution to resellers.

The demand side is already live — 30+ retail and venue partners carry Agroverse cacao (agroverse.shop/partners).

### TrueTech Inc — the existing US import entity
- **Legal name:** TRUETECH INC
- **Form:** C-Corporation, Delaware (IRS Form 1120 filer)
- **EIN:** 88-3411514
- **US Customs importer-of-record no.:** 88-341151400
- **FDA Food Facility Registration:** 12202640780 (VALID, exp. 2026-12-31)
- **D-U-N-S:** 11-903-5208
- **Officer:** Zhiwen Teh (Gary Teh), President

---

## 4 · Current State & Problem

Brazilian exports currently flow through "Black King" — the individual CNPJ of Matheus Reis Pereira (CNPJ 50.042.585/0001-80), an Empresário Individual (micro-enterprise, Simples Nacional) based in Ilhéus, Bahia.

**Why this must change:**
1. **Personal tax liability** — routing DAO-scale export flow through Matheus's individual CNPJ accumulates Brazilian tax exposure on him personally
2. **Not automatable** — building automation on an individual's personal registration is inappropriate and risky
3. **Single point of failure** — a community-wide operation should not depend on one person's personal legal standing, banking, and RADAR limits
4. **Scale & financing** — a Simples Nacional micro-enterprise has limited RADAR capacity

---

## 5 · Proposed Structure — Two Paths

### Path A: Próspera HoldCo (original proposal)

```
DAO contributors (TDG holders)
    ↓
Próspera HoldCo (Honduras ZEDE)
    ↓ owns
Brazilian Export CNPJ (Ltda, RADAR + Siscomex)
    ↓ exports to
TrueTech Inc (US import, Delaware C-corp) — already live
```

- **Tier 1 — Próspera HoldCo.** A new entity incorporated in the Próspera jurisdiction acts as the holding/operating company and owner of the Brazilian export entity.
- **Tier 2 — Brazilian Export CNPJ.** A new Brazilian company, owned/controlled by the Próspera HoldCo, incorporated to export Northern-Brazilian agricultural products. It obtains RADAR habilitation and operates in Portal Único Siscomex in its own name.
- **Tier 3 — Destination-market importers** (one per market). US: TrueTech Inc (already established); China and Europe: TBD.

**Pros:** Designed path for foreign-owned Brazilian entity; Próspera counsel already identified (Layon Costa, Tools for the Commons)
**Cons:** Higher cost ($5K-15K+), longer timeline (2-6 months), unknown banking

---

### Path B: Wyoming UNA/DUNA (alternative)

```
DAO contributors (TDG holders)
    ↓
Wyoming UNA/DUNA (US nonprofit association, ~$50 via OtoCo)
    ↓ owns
Brazilian Export CNPJ (Ltda, RADAR + Siscomex)
    ↓ exports to
TrueTech Inc (US import, Delaware C-corp) — already live
```

- **Tier 1 — Wyoming UNA.** Formed via OtoCo smart contract (~$50 gas, this week). Two wallet addresses sign. Auto-converts to DUNA when membership exceeds 100.
- **Tier 2 — Brazilian Export CNPJ.** Same as Path A — a new Brazilian company owned by the UNA/DUNA.
- **Tier 3 — Destination-market importers.** Same as Path A.

**Pros:** Very low cost (~$50), this week, US jurisdiction (Wyoming), Wise banking available, simpler ownership mapping
**Cons:** Unclear whether a Wyoming UNA/DUNA (nonprofit association) can legally own a Brazilian for-profit Ltda — this is the core question for counsel

**Key question for Layon Costa:** Can a Wyoming UNA/DUNA hold equity in a Brazilian Ltda as a foreign quotaholder, or does Brazilian law require an intermediate for-profit holding entity (like a Próspera corporation)?

---

## 6 · Ownership — Mapped to DAO Contributor Ledger

Regardless of which path, the holding entity is not owned by a single founder. Its beneficial ownership is intended to map to the DAO's existing contributor ledger: the individuals recorded in the Main Ledger's "Contributors contact information" tab, each owning in proportion to the governance tokens (TDG) they have earned.

**Snapshot — 26 May 2026:**
- 316 contributors hold a non-zero TDG balance across ~2,263,640 TDG issued

| # | Contributor | TDG controlled | Ownership % |
|---|------------|---------------|-------------|
| 1 | Gary Teh | 955,459 | 40.77% |
| 2 | Garis Pang | 67,653 | 2.89% |
| 3 | Fatima Toledo | 65,853 | 2.81% |
| 4 | Val Lapidus | 62,143 | 2.65% |
| 5 | Jacob Nelan | 60,726 | 2.59% |
| 6 | Priscilla Huang | 58,590 | 2.50% |
| 7 | Kelvin Chew | 58,360 | 2.49% |
| 8 | Vlatko Gigov | 50,584 | 2.16% |
| 9 | Aléksa Mil | 44,820 | 1.91% |
| 10 | Johnson Teh | 38,665 | 1.65% |
| 11 | Anika Giftge | 37,560 | 1.60% |
| 12 | Gautam Mittal | 33,450 | 1.43% |
| 13 | Richard Chu | 30,243 | 1.29% |
| 14 | Matheus Reis | 29,693 | 1.27% |
| 15 | Emelin | 25,621 | 1.09% |
| ... | +301 more contributors | ≈ 644,000 | ≈ 28.5% |

---

## 7 · What We Need From Counsel

### Core decision question (for Layon Costa / Tools for the Commons)

**Can a Wyoming UNA/DUNA legally own a Brazilian Ltda as a foreign quotaholder?**

This determines which path we take. If yes, we proceed with Path B (UNA/DUNA, ~$50, this week). If no, we proceed with Path A (Próspera HoldCo).

### For Brazilian foreign-trade / customs & tax counsel (either path)
- Most suitable Brazilian legal form for an export-only entity that will be foreign-owned
- Foreign-ownership mechanics (resident legal representative, RDE registration)
- RADAR habilitation modality, documentation, timeline
- Siscomex / Portal Único access and API vs. despachante aduaneiro requirements
- Tax regime selection (Simples vs. Lucro Presumido vs. Lucro Real)
- Transfer-pricing between Brazilian entity, holding entity, and TrueTech Inc
- Clean migration path from Black King arrangement
- Multi-market and multi-product export implications

### For Próspera-jurisdiction incorporation counsel (Path A only)
- Appropriate Próspera entity type for holding company owning a Brazilian subsidiary
- Banking, substance, and reporting requirements
- How a Próspera entity is recognised as a foreign quotaholder in Brazil
- Interaction with TrueTech Inc (US)
- Suitability for DAO/tokenised governance and AI-agent-operated subsidiaries

### On ownership & securities (for both paths)
- How to translate a ~316-holder, continuously-updating, TDG-weighted contributor base into recognised ownership of the holding entity
- Securities-law treatment of TDG-as-ownership across the relevant jurisdictions
- Snapshot/cut-off mechanics and KYC requirements for owners of record

---

## 8 · Brazilian Supply Base

| Trade name | Legal name | CNPJ | Location | Products |
|-----------|-----------|------|----------|----------|
| Coopercabruca | Cooperativa dos Cacauicultores do Sul da Bahia | 31.948.811/0001-42 | Itabuna, BA | cacao nibs, mass, molasses |
| Black King* | Matheus Reis Pereira (Empresário Individual) | 50.042.585/0001-80 | Ilhéus, BA | nibs, mass, molasses, tea, husk, ceremonial cacao |
| CEPOTX | Coop. Central de Produção Orgânica da Transamazônica e Xingu | 22.568.369/0001-38 | Altamira, PA | organic cacao almonds |
| Mu Gelato | Mu Gelato Sorvetes Artesanais Ltda | 23.655.374/0001-40 | Florianópolis, SC | chocolate-coated coffee bean candy |
| Hau Cacau | Hau Cacau Superalimentos Ltda | (on file) | Porto Alegre, RS | cacao mass |

*\* "Black King" is both a verified supplier AND the individual currently used as the export vehicle this project replaces.*

---

## 9 · Key Person

**Gary Teh** (Zhiwen Teh) — President, TrueTech Inc; proposed responsible principal for the new structure
- Brazilian CPF: 039.733.078-22
- Email: garyjob@truesight.me / garyjob@agroverse.shop

---

## 10 · Data Room & Compliance Status

- **FSVP/FDA compliance:** All suppliers carry VALID FDA Food Facility Registrations (exp. 2026-12-31)
- **Public document repository:** github.com/TrueSightDAO/fda_fsvp
- **Machine-readable profiles:** entity.json in each supplier folder
- **Transparency surfaces:** truesight.me (DAO), truesight.me/agroverse (program)

---

## 11 · Glossary

| Term | Definition |
|------|-----------|
| CNPJ | Brazilian company tax/registration ID |
| CPF | Brazilian individual tax ID |
| RADAR | Receita Federal license for foreign trade via Siscomex |
| Siscomex / Portal Único | Brazil's Integrated Foreign Trade System |
| DU-E | Declaração Única de Exportação — single export declaration |
| Despachante aduaneiro | Licensed Brazilian customs broker |
| FSVP | FDA Foreign Supplier Verification Program |
| FDA FFR | FDA Food Facility Registration number |
| D-U-N-S | Dun & Bradstreet business identifier |
| EIN | US Employer Identification Number |
| UNA | Unincorporated Nonprofit Association (Wyoming) |
| DUNA | Decentralized Unincorporated Nonprofit Association (Wyoming) |
| Próspera (ZEDE) | Special economic/governance jurisdiction (Honduras) |
| TDG | TrueSight DAO governance token |
