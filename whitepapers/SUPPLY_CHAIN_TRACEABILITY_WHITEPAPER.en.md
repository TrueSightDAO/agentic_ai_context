# Verifiable Supply-Chain Traceability for China's Exporters
## Meeting EU & US ESG, Due-Diligence, and Traceability Requirements with the TrueSight Lineage Stack

**White Paper · Version 1.0**

**TrueSight DAO** — *Heal the world with love; restore 10,000 hectares of Amazon rainforest.*

> Bilingual edition: English (this file) + Simplified Chinese (`SUPPLY_CHAIN_TRACEABILITY_WHITEPAPER.zh-CN.md`).

---

## 1. Executive Summary

European and US buyers, retailers, and regulators are making **verifiable supply-chain evidence** a condition of market access. The EU's Corporate Sustainability Reporting Directive (CSRD), Corporate Sustainability Due Diligence Directive (CSDDD), and Deforestation Regulation (EUDR), together with the US Uyghur Forced Labor Prevention Act (UFLPA) enforcement regime, require importers to demonstrate — with documented, granular, tamper-evident evidence — that the goods they buy were produced without deforestation, forced labor, or undisclosed ESG risk. Chinese exporters, however capable, often fail these assessments because their evidence is **paper-based, fragmented, and not independently verifiable**.

TrueSight DAO operates a **production supply-chain traceability stack** that is already live on a physical product line (single-estate ceremonial cacao). The stack combines:

1. **Unit-level QR serialization** — every physical unit carries a unique QR code that resolves to a structured provenance record.
2. **Per-unit lineage manifests** — machine-readable JSON history of origin, processing, custody, and events (append-only).
3. **Blockchain anchoring (TrueChain)** — tamper-evident hashes of every record on a permissioned, audit-ready ledger.
4. **Identity & credentialing** — every actor (factory, farm, auditor, carrier) holds a verifiable identity; every event is an *attested chain*.
5. **Document notarization** — official documents and media (audits, certifications, labor records) stored and linked to the units they concern.
6. **Public verification surfaces** — any stakeholder can scan a unit and see its full provenance, ESG-relevant data, and evidence trail.

This white paper explains how this stack — proven on cacao — can be adapted to help Chinese manufacturers meet EU/US ESG and traceability requirements, improve export ratings, and turn compliance from a cost into a competitive advantage.

---

## 2. The Problem: The Compliance Gap

### 2.1 What the EU and US now demand

| Regime | What it demands of importers (and therefore of exporters) |
|---|---|
| **EU CSRD / ESRS** | Sustainability reporting covering the value chain, including Scope 3 emissions and supply-chain ESG data. EU buyers must collect this data from suppliers. |
| **EU CSDDD** | Mandatory human-rights and environmental due diligence across the value chain — identification, prevention, remediation — regardless of where suppliers are located. |
| **EU EUDR** | Deforestation-free proof for commodities: geolocation of production plots, risk assessment, and a Due Diligence Statement (DDS) per shipment. |
| **US UFLPA / CBP (incl. June 2026 Operational Guidance)** | Rebuttable presumption of forced labor for goods linked to Xinjiang or Entity List parties; documented **supply-chain mapping**, **batch-level traceability records**, third-party social-compliance audits, and forced-labor risk assessments. |

### 2.2 Why Chinese exporters fail these assessments

- **Evidence fragmentation** — data lives across paper records, ERP silos, and multiple tiers of suppliers; it cannot be assembled into one order-level proof.
- **No unit-level identity** — without a serialized identifier on each unit, buyers cannot verify that a claim (origin, batch, labor, carbon) refers to *this* unit rather than a generic certificate.
- **No independent attestation** — self-declared documents are not independently verifiable and are increasingly treated as greenwashing risk.
- **No tamper-evidence** — spreadsheets and PDFs can be altered after the fact; auditors cannot trust their integrity.
- **Data-residency friction** — buyers and regulators in different jurisdictions demand different data controls, slowing evidence exchange.

The result: capable Chinese manufacturers are **downgraded in ESG ratings** and **detained at the border** (US CBP alone reported over 17,000 UFLPA-related detentions from FY2025 through early FY2026), even when their operations are sound.

---

## 3. What We Already Have: The TrueSight Lineage Stack

The stack below is **in production** for single-estate cacao. Every component already exists as code, data, and public infrastructure.

### 3.1 Unit-level QR serialization (proven: 1,457+ units)

- Every physical unit carries a **serialized QR code** (e.g. `2024OSCAR_20260121_12`).
- The QR is the **unit identity**: it resolves farm + vintage + batch and its full ledger history. It is deliberately distinct from the retail GTIN, which only identifies the product *type*.
- Existing QRs keep working unchanged; new units are minted with a label (QR + farm + origin) and a matching JSON manifest in one run.

### 3.2 Per-unit lineage manifests (`lineage-assets`)

- One JSON file per unit: `qr_id`, `asset_type`, `status`, `current_holder`, `lineage` (farm, region, harvest, SKU), and an **append-only `events` array** (minted → consigned → sold → …).
- Schema is explicitly **additive**: new asset types (`textile_lot`, `electronics_batch`, `agri_lot`, …) are added without changing the wrapper.
- Git history per file = an audit trail per asset; any stakeholder can fetch a unit's file independently.

### 3.3 Blockchain anchoring (TrueChain)

- A permissioned Ethereum network (Geth, Clique Proof-of-Authority) with purpose-built registries: `ShipmentRegistry`, `FarmRegistry`, `ProductRegistry`, `InvoiceRegistry`, `QRCodeRegistry`, `SalesReceiptRegistry`, `ContributionRegistry`.
- Records are **append-only and tamper-evident** via hashed payloads; a mirror service writes hashes to the chain and returns a transaction hash that links the sheet row ↔ chain record.
- Factories never need a wallet: evidence is anchored in the background, and anyone can verify without a blockchain client.

### 3.4 Identity & credentialing (attested chains)

- Parallel architecture to our human-credentialing platform: **every actor gets its own keypair**; every event is an *attested chain* — a known actor attesting to a verifiable thing.
- Applies to people (factory managers, auditors, workers' representatives) and assets alike.

### 3.5 Document notarization

- A public repository for uploading and storing official documents and media that verify supply-chain processes — audits, certifications, labor records, factory photos/video — linked to the units they concern.
- Documents are hashed and timestamped, so "this certificate belongs to this batch" is provable.

### 3.6 Public verification surfaces

- `truesight.me/qr/?id=<qr_id>` — scan any unit to see its provenance timeline, status, holder, and events.
- Product Verification listing (`truesight.me/physical-assets/serialized/`) — searchable/filterable index across all units.
- The same surface can render an **export-ready due-diligence packet**: origin, batch records, attestations, and linked documents.

### 3.7 Cross-jurisdiction data residency (designed, not yet deployed)

The architecture is designed to split into per-jurisdiction repos (`lineage-assets-china`, `lineage-assets-eu`, …), each hosted **in-jurisdiction** to satisfy data-residency rules, with cross-border queries via API rather than data replication. This matters for Chinese exporters whose data must stay in China while EU/US buyers verify evidence remotely.

---

## 4. How the Stack Maps to a Chinese Export Factory

| Step | Factory activity | Our component | Output |
|---|---|---|---|
| 1 | Register factory, facilities, and supply-chain map | Identity + credentialing; farm/facility registry | Verified actor identity, supply-chain map |
| 2 | Serialize each export unit | QR minting (label + manifest) | Unit QR + JSON manifest |
| 3 | Record production events (materials in, QC, batch, labor, energy) | Lineage events (append-only) | Batch-level traceability records |
| 4 | Attach evidence (audits, certifications, labor docs, photos) | Document notarization | Linked, hashed evidence per unit |
| 5 | Anchor everything | TrueChain mirror service | Tamper-evident hashes + tx hash per record |
| 6 | Generate order-level due-diligence packet | Verification surface / report builder | CSRD/CSDDD/EUDR/UFLPA-ready packet |
| 7 | Buyer/regulator verifies | Scan QR or open packet | Independent verification in seconds |

This is the **same pipeline we run for cacao** — origin farm → processing → custody → sale — generalized to any manufactured export unit.

---

## 5. ESG & SDG Mapping

### 5.1 Regulation → data need → our component

| Regulation | Data need | Our component that satisfies it |
|---|---|---|
| CSRD / ESRS (incl. Scope 3) | Value-chain ESG data points | Lineage events mapped to ESRS datapoints; per-unit carbon/energy/water fields |
| CSDDD | Human-rights & environmental due-diligence trail | Attested actor chain, audit attestations, corrective-action log |
| EUDR | Geolocation, deforestation-free proof, DDS per shipment | Geo lineage fields, farm/facility registry, per-lot DDS packet |
| UFLPA / CBP 2026 | Supply-chain map, batch-level traceability, third-party audits, risk assessment | Batch-level QR lineage, notarized audit docs, risk-assessment export |

### 5.2 Our components → SDGs

| Component | SDG contribution |
|---|---|
| Unit traceability & batch records | **SDG 12** Responsible Consumption and Production |
| Labor attestations & no-forced-labor evidence | **SDG 8** Decent Work and Economic Growth |
| Geolocation & deforestation-free evidence | **SDG 15** Life on Land (and **SDG 13** Climate Action via per-unit emissions data) |
| Food-safety batch trace (agri exports) | **SDG 2** Zero Hunger |
| Blockchain + credentialing technology | **SDG 9** Industry, Innovation and Infrastructure |
| Audit trail, anti-corruption, governance | **SDG 16** Peace, Justice and Strong Institutions |
| Multi-stakeholder verification (factory ↔ auditor ↔ buyer) | **SDG 17** Partnerships for the Goals |

---

## 6. Pilot Plan

### 6.1 Phase 0 — Alignment (weeks 0–2)

- Identify 1–3 export factories in high-scrutiny sectors (textiles, electronics, agro-products) with an EU/US buyer relationship.
- Confirm target markets and the specific evidence each buyer/regulator requires.
- Engage via the existing China partner channel (Jerri/Ling team, Aora program network).

### 6.2 Phase 1 — Onboard one factory (weeks 2–6)

- Register factory identity + supply-chain map; mint QRs for one export order.
- Seed lineage manifests for that order (materials → production → QC → packing).
- Attach available documents (audits, certifications, labor records) via notarization.
- Anchor to TrueChain; generate a demo due-diligence packet.
- Success metric: a buyer accepts the packet as sufficient evidence.

### 6.3 Phase 2 — ESG data model & ratings (weeks 6–12)

- Map lineage events to ESRS datapoints and buyer ESG questionnaires.
- Add optional third-party auditor attestation integration.
- Produce periodic ESG reports from live data (not static PDFs).

### 6.4 Phase 3 — Scale (months 3–12)

- Per-jurisdiction data residency (lineage-assets-china, …).
- Sector templates (textile / electronics / agri) and multi-factory rollout.
- Buyer-facing verification portals and marketplace integrations.

---

## 7. Integrity & Governance Guardrails

- **The platform does not certify compliance.** It makes evidence *verifiable* — the integrity of claims is anchored, while the truth of claims rests with the attesting actors and independent auditors. This is the anti-greenwashing design.
- **Attestation model**: every event names the actor who attested it; actors are identifiable; auditors are third-party where regulation requires.
- **Append-only**: records can be corrected only by appending a correction, never by editing history.
- **Data residency**: per-jurisdiction hosting keeps export data inside the required jurisdiction.
- **Open verification**: any stakeholder can verify without special software — scanning a QR is enough.

---

## 8. Mission Tie-Back

The TrueSight DAO exists to **restore 10,000 hectares of Amazon rainforest**. Traceability is how we fund and extend that mission: every verified unit in our own supply chain finances reforestation, and deploying the same infrastructure for Chinese exporters creates a revenue stream that continues to fund the mission — while genuinely helping manufacturers comply, compete, and export.

---

## 9. Next Steps

1. **Review this white paper** (EN + zh-CN) with the partner group.
2. **Select pilot factory(ies)** and target EU/US buyer(s).
3. **Stand up Phase 0/1** with the China partner team.
4. **Extend the lineage schema** for the pilot's asset types (additive change).
5. **Generate the zh-CN PDF** via the CJK-capable publishing pipeline (aora convention).

---

*TrueSight DAO · 2026 · truesight.me · This white paper is a proposal; the China-export use case is an extension of the production cacao stack.*
