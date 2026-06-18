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

Incorporate a new entity in the **Próspera jurisdiction** which will, in turn, own/control a new **Brazilian company (CNPJ)** dedicated to exporting agricultural products out of Northern Brazil (Bahia and Pará), starting with cacao. The Brazilian entity will hold its own RADAR license and Siscomex access so it can file export declarations in its own name, independent of any individual's personal CNPJ.

The Próspera entity is owned by the DAO's contributors — the people on our contributor ledger, in proportion to the governance tokens (TDG) they have earned — not by a single founder.

**In one line:**
> DAO contributors → Próspera HoldCo → Brazilian Export CNPJ (RADAR + Siscomex), Bahia & Pará → dedicated importers: US (TrueTech Inc, live), China & Europe (TBD) → Agroverse reseller network.

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

## 5 · Proposed Structure

- **Tier 1 — Próspera HoldCo.** A new entity incorporated in the Próspera jurisdiction acts as the holding/operating company and owner of the Brazilian export entity.
- **Tier 2 — Brazilian Export CNPJ.** A new Brazilian company, owned/controlled by the Próspera HoldCo, incorporated to export Northern-Brazilian agricultural products. It obtains RADAR habilitation and operates in Portal Único Siscomex in its own name.
- **Tier 3 — Destination-market importers** (one per market). US: TrueTech Inc (already established); China and Europe: TBD.
- **Operating model.** Autonomous AI agents prepare documents, reconcile the ledger, and orchestrate filings; a licensed Brazilian customs broker and accountants remain in the loop as required by law.

---

## 6 · Ownership — Mapped to DAO Contributor Ledger

The Próspera HoldCo is not owned by a single founder. Its beneficial ownership is intended to map to the DAO's existing contributor ledger: the individuals recorded in the Main Ledger's "Contributors contact information" tab, each owning in proportion to the governance tokens (TDG) they have earned.

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

### For Brazilian foreign-trade / customs & tax counsel
- Most suitable Brazilian legal form for an export-only entity that will be foreign-owned
- Foreign-ownership mechanics (resident legal representative, RDE registration)
- RADAR habilitation modality, documentation, timeline
- Siscomex / Portal Único access and API vs. despachante aduaneiro requirements
- Tax regime selection (Simples vs. Lucro Presumido vs. Lucro Real)
- Transfer-pricing between Brazilian entity, Próspera HoldCo, and TrueTech Inc
- Clean migration path from Black King arrangement
- Multi-market and multi-product export implications

### For Próspera-jurisdiction incorporation counsel
- Appropriate Próspera entity type for holding company owning a Brazilian subsidiary
- Banking, substance, and reporting requirements
- Interaction with TrueTech Inc (US)
- Suitability for DAO/tokenised governance and AI-agent-operated subsidiaries

### On ownership & securities (for both counsel)
- How to translate a ~316-holder, continuously-updating, TDG-weighted contributor base into recognised ownership
- Securities-law treatment of TDG-as-ownership across Próspera, Brazil, and US
- Snapshot/cut-off mechanics and KYC requirements

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
| Próspera (ZEDE) | Special economic/governance jurisdiction |
| TDG | TrueSight DAO governance token |
