# Brazil → Hong Kong Cacao Import — End-to-End SOP

> **Purpose:** Single reference for AI assistants and human operators to manage the end-to-end process of importing cacao from Brazil into **Hong Kong SAR** — the Hong Kong-side customs formalities, the Brazil-side export prerequisites (shared with the existing lanes), and the HK → Mainland re-export (CEPA) note.
> **Prepared:** 2026-09-13 | **Prepared by:** Sophia Truesight (TrueSight DAO Autopilot)
> **Source:** Governor-supplied 3-page guide *"Importing 40 kg of Raw Cocoa Beans into Hong Kong — Complete Customs Clearance Guide"* (thread), cross-referenced with the DAO's Brazil export-lane docs. HK-side figures are **as stated in that guide** — verify before booking (see §9).

---

## 1. Critical distinction — Hong Kong ≠ Mainland China

**Hong Kong SAR is a separate customs territory.** Do **not** reuse the Brazil → China (Dongguan) playbook for an HK import.

| | **Hong Kong lane (this SOP)** | **Mainland China lane (Dongguan)** |
|---|---|---|
| Regime | HK Food Safety Ordinance (Cap. 612) + HK Customs declaration | GACC Decree No. 280 / CIFER registration |
| Key HK/Mainland requirement | **FEHD food importer registration** (consignee) | **GACC registration number** (producer) |
| Competent authority | FEHD / AFCD / HK Customs | GACC (General Administration of Customs of China) |
| Duty / VAT | **Zero** duty, no VAT/GST (free port) | Duty per HS code; VAT |
| Phytosanitary | Raw cocoa beans **generally exempt** (pulses) | Phytosanitary Cert. via MAPA |
| Docs | `BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE*.md` ❌ not applicable | ✅ |

**Structural rule (unchanged from the export-lane learnings):** MAPA/GACC requirements attach to the **production enterprise**, not the exporter/trader. **GACC is only needed if the goods later enter Mainland China** — an HK-only import does not trigger GACC.

---

## 2. The two mandatory HK-side requirements

### 2.1 Food Importer Registration (consignee)
- **Legislation:** Food Safety Ordinance (Cap. 612).
- **Who:** the **consignee (importer) in Hong Kong** must register with the **Food and Environmental Hygiene Department (FEHD)** as a food importer — *not* the Brazilian exporter.
- **Application form:** FEHB 245.
- **Registration fee:** HK$195 · **Validity:** 3 years · **Renewal fee:** HK$180.
- **Submission:** in person, by post, or online via the **Food Traders Portal**.
- ⚠️ **This is the #1 pre-flight gate.** Confirm the HK consignee already holds a valid registration **before shipment** (§6, Phase 0).

### 2.2 Import / Export Declaration (HK Customs)
- **Legislation:** Import and Export (Registration) Regulations.
- **Deadline:** declaration must be lodged with **Hong Kong Customs within 14 days** of import.
- **Value threshold:** postal packets valued at **HK$4,000 or less are exempt**; otherwise declaration is required. A 40 kg consignment of raw cocoa beans typically exceeds this → **declaration is mandatory**.
- **Fee:** flat **HK$0.2 per declaration** for food products, regardless of value.
- **Channel:** electronic declarations via designated service providers (e.g. **TradeLink**).

---

## 3. Phytosanitary requirements — generally exempt (verify)

- Under **Cap. 207**, although "cocoa" is listed as a controlled item, **"cereals, pulses, seeds and spices for human or animal consumption or for industrial use" are explicitly exempted** — no Plant Import Licence or Phytosanitary Certificate required.
- **Raw cocoa beans qualify as pulses for human consumption** → exempt.
- **Recommendation:** contact the **Agriculture, Fisheries and Conservation Department (AFCD) at 2150-7000** before shipment for **written confirmation**.
- ⚠️ **Scope nuance:** this exemption covers the **beans**. **Wooden pallets** are a separate matter — if pallets are used, they must meet **ISPM#15** (heat-treated/fumigated + IPPC stamp) and be accompanied by the relevant pallet phytosanitary documentation. See `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` §Phase 1 for pallet compliance detail.

---

## 4. Recommended trade documents

Prepare for customs inspection regardless of exemption status:

| # | Document | Issued by | Notes |
|---|----------|-----------|-------|
| 1 | Commercial Invoice | Exporter (Brazil) | Standard export doc |
| 2 | Packing List | Exporter | Standard export doc |
| 3 | Bill of Lading / Air Waybill | Carrier | Transport document |
| 4 | Certificate of Origin | Brazil competent authority | Proves Brazilian origin; **also the base for a CEPA CoO** if re-exporting (§5) |
| 5 | Health Certificate | MAPA (Brazil) | *If available from the supplier* |

**Brazil-side prerequisites (shared with the SF lane — do not duplicate here):** export **NF-e (model 55)**, RADAR, SISCOMEX/DU-E, and the **Black King CNPJ blocker**. See `BRAZIL_EXPORT_LANE_LEARNINGS.md` §2 and `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` Phase 0.

---

## 5. Tariffs & taxes — zero duty

- Hong Kong is a **free port**: imports of raw cocoa beans are **zero-rated**; **no VAT and no GST**.
- The **only** charge payable on the HK side is the **declaration fee (HK$0.2)**.

### CEPA note — onward re-export to Mainland China
- The **CEPA Certificate of Origin is valid for 120 days** from issuance — **shorter than the typical 1-year validity** under other FTAs.
- ⚠️ If the plan is **HK → Mainland China re-export** (e.g. the Aora / China events route transiting via HK), factor this **120-day clock** into timing, and confirm CEPA eligibility + the correct issuing authority **before** shipping.
- If goods ultimately enter **Mainland** China, **GACC registration applies after all** — see `BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE*.md`.

---

## 6. Pre-flight checklist

### Phase 0 — Pre-flight gates (do these FIRST)
- [ ] **Confirm HK consignee's FEHD food-importer registration status** ⚠️ **#1 gate.** If the consignee is **not** registered, they must register **first** (form FEHB 245, HK$195) — otherwise compliance risk.
- [ ] **Written AFCD confirmation** (2150-7000) that raw cocoa beans are exempt from Plant Import Licence / Phytosanitary Certificate for this shipment.
- [ ] **Decide final destination:** HK-only, or HK → Mainland re-export? If re-export → confirm **CEPA CoO** path + 120-day validity.
- [ ] **Confirm the Brazil-side export is unblocked** — NF-e issuable (Black King CNPJ status). See `BRAZIL_EXPORT_LANE_LEARNINGS.md` §2.
- [ ] **Appoint the HK-side declarant / agent** (e.g. TradeLink) for the 14-day declaration.

### Phase 1 — Brazil origin & export (shared with SF lane)
- [ ] Cargo packed, weighed, photographed at origin warehouse (Matheus, Ilhéus).
- [ ] Pallet compliance (ISPM#15 + IPPC stamp) if pallets used.
- [ ] Export NF-e issued; DU-E / SISCOMEX cleared.
- [ ] Export documents: commercial invoice, packing list, AWB/BL, certificate of origin, health certificate.
- [ ] Export customs clearance (*desembaraço*) by Omega.

### Phase 2 — Freight (Brazil → Hong Kong)
- [ ] Book air/sea freight (Salvador/Guarulhos → HKG).
- [ ] Confirm carrier handles HK delivery + terminal charges.
- [ ] Share AWB/BL with HK consignee + declarant **ahead** of arrival.

### Phase 3 — Hong Kong import & customs
- [ ] Consignee (registered FEHD food importer) receives the goods.
- [ ] **Lodge HK Customs import declaration within 14 days** (TradeLink; HK$0.2).
- [ ] Retain invoice, packing list, BL/AWB, CoO, health cert for inspection.
- [ ] File the declaration record + receipt to the DAO ledger (see §7).

### Phase 4 — Onward (if applicable)
- [ ] If re-exporting to Mainland: obtain **CEPA Certificate of Origin** (120-day validity) and confirm GACC status of the producer facility.
- [ ] Log the onward movement in the DAO inventory ledger.

---

## 7. DAO ledger / inventory side

An HK import is a **custody transfer between known supply-chain holders** (not an end-customer retail sale):
- Record an **[INVENTORY MOVEMENT]** (manager → HK recipient) — QR status stays **IN INVENTORY**. Do **not** use a SALES EVENT unless the bag is sold to an end customer.
- Reference the AWB/BL and the HK Customs declaration receipt in the event notes.
- If SKUs are later sold in HK/Mainland, record a **[SALES EVENT]** at that point (QR → SOLD).

---

## 8. Key contacts

| Role | Name / Entity | Contact |
|------|---------------|---------|
| HK consignee / China-side ops | Elizabeth Wong (Liz) / Aora | via Gary Teh |
| HK food importer registration | **FEHD** — Food Traders Portal | — |
| Phytosanitary confirmation | **AFCD** | **2150-7000** |
| HK import declaration | **Hong Kong Customs** via **TradeLink** | — |
| Brazil freight forwarder / coordinator | Graziela Vedana — Seacos Logistic | Graziela@5cl.rs |
| Brazil export operations | Omega Services — Ana Barros / Isis Ribeiro | ana.barros@omegaservicos.com.br / isis.ribeiro@omegaservicos.com.br |
| Brazil origin warehouse | Matheus Reis — Gateway.fy / Black King | theus.reis.ssa@gmail.com / +55 73 99109-0002 (WhatsApp) |

---

## 9. Open questions / to verify before booking

1. **Is the HK consignee already an FEHD-registered food importer?** If not, registration (FEHB 245, HK$195) must complete first.
2. **AFCD written confirmation** of the pulses/phytosanitary exemption for this specific shipment.
3. **Final destination:** HK-only, or HK → Mainland re-export? Determines whether **CEPA CoO** and **GACC** apply.
4. **Confirm current FEHD / HK Customs fee figures and form revision** against the live FEHD and HK Customs sites — the source guide's figures (HK$195 / HK$180 / HK$0.2, FEHB 245) should be re-checked at booking time.
5. **Freight quote Brazil → HKG** — not yet obtained; get one from Omega/Seacos (compare against the BR→US tiered air rates in `BRAZIL_EXPORT_LANE_LEARNINGS.md` §7).
6. **Who is the HK-side declarant/agent** for the 14-day declaration.

---

## 10. Related docs (don't duplicate)

- `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` — Brazil → San Francisco freight SOP (shared Brazil-side phases, pallet/IPPC detail, cost model).
- `brazil/BRAZIL_TO_CHINA_GACC_REGISTRATION_GUIDE.md` / `..._CEPOTX.md` / `..._COOPERCABRUCA.md` — **Mainland China** GACC/CIFER lane (applies only if goods enter the Mainland).
- `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md` — consolidated export-lane learnings (Black King blocker, MAPA/GACC, trader-vs-producer, Omega quote).
- `brazil/CACAO_SOURCING_NETWORK_OVERVIEW.md` — network map (China/Dongguan/HK destination row).
- `brazil/BLACK_KING_ADMIN_ACCESS_OPTIONS.md` — Brazil export-entity access decision.

---

*Prepared by Sophia Truesight (TrueSight DAO Autopilot), 2026-09-13. HK-side content derived from the governor-supplied 3-page guide; verify §9 items at booking time.*
