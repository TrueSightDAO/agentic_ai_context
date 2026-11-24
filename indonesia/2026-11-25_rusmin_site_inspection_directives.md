# Indonesia site inspection directives — Rusmin collaboration

**JIRA:** [KAN-8](https://truesightdao.atlassian.net/browse/KAN-8) — *Rusmin - execution directives to be associated with letter of intent*
**Prepared by:** Sophia Truesight (autopilot) · **For:** Gary Teh, Director, BionPact Pte Ltd
**Date:** 2026-11-25 · **Status:** draft for governor review — not issued to Rusmin
**Companion to:** `indonesia/2026-11-24_bionpact_loi_work_record.md` (the LOI itself was sent 2026-11-25)

---

## 0. Why this document exists, and its shape

This is the **execution annex** to the Letter of Intent. The LOI says what we intend; this says **what we must physically see and measure** before any cocoa is bought, financed, or shipped.

**Design decision — two registers, one document.** The governor asked whether this should be a checklist, and whether rates belong in it. It needs both, kept apart, because they fail differently:

| Register | Form | Why separate |
|---|---|---|
| **A — Inspection checklist** (§2) | Evidence-based, per station | A fact about the site. Can be **PASS / GAP / ABSENT**. Auditable later for FSVP |
| **B — Commercial capture** (§3) | Rate + unit + source | A number nobody knows until quoted. Cannot pass or fail; can only be **obtained** or **not obtained** |

Conflating them is the usual failure: rates get buried inside a compliance form, and the compliance form starts reading like a negotiation.

**Third column worth having: the Brazil benchmark.** Where TrueSight already knows the number from the Bahia/Amazon lane, it goes in the row. That changes the question from *"collect the rate"* to *"observe the rate against what we already pay"* — the difference between a form and a finding. Where we do not have a benchmark, the column says so rather than guessing.

---

## 1. How to record a finding

Each item below is written so it can be answered in one line and photographed in one frame:

- **PASS** — seen, and as described
- **GAP** — seen, but deficient (say how)
- **ABSENT** — not present at all
- **N/A** — genuinely not applicable (say why)

**Two rules that matter more than the form itself:**

1. **Photograph what you record.** A remark with no image is a claim; an image with no remark is a mystery. Every GAP needs a photo.
2. **Never record a rate you were not quoted.** If Rusmin says "market rate", that is the finding: *"market rate quoted, not specified"*. An estimated number silently becomes a committed number three meetings later.

---

## 2. Register A — inspection checklist

### 2.1 On the farm

| # | Ascertain | Decision it feeds | Evidence |
|---|---|---|---|
| A1 | **Cacao trees / plantation** — planted area (ha), age of trees, spacing, shade regime (full sun / agroforestry) | Whether volume is credible; agroforestry claim in the LOI | Plot walk photos, canopy shots |
| A2 | **Variety** — what is actually planted. Trinitario / Forastero / Criollo, and any *local* name the farmer uses | Flavour positioning + cadmium behaviour is cultivar-dependent (`CACAO_RESEARCH_BIBLIOGRAPHY.md`: genetic variation in Cd partitioning) | Pod and leaf close-ups; ask for the local variety name, do not supply one |
| A3 | **Plot boundaries** — where the plot starts and stops; GPS polygon if possible | Origin claims; deforestation-free assurance | GPS track / 4 corner photos + coordinates |
| A4 | **Fermentation facility** — box type (wood/synthetic), dimensions, batch size, turning schedule (frequency, day by day), duration | This is where flavour is made or lost. Turning regime is a named observation in `fsvp/SITE_VISIT_PROCESS.md` | Photos of boxes, a written turning schedule |
| A5 | **Drying facility** — sun (patio / raised bed) vs mechanical; thickness of bean layer; duration; rain protocol; mould observed anywhere? | Mould is the hazard FSVP names for drying. Mechanical drying too fast → acidic beans | Photos of beds/solar dryer; ask what happens when it rains |
| A6 | **Farmers — photos and stories** | The provenance narrative for agroverse.shop; named farmer = traceable bag | Portraits **with consent** (see §5) |
| A7 | **Post-harvest sorting** — who sorts, where, what is rejected | Rejection rate drives effective yield and price | Photo of sorting area and reject pile |
| A8 | **Pest / disease pressure** — any monilia or witches' broom visible; what is sprayed, if anything | Residue risk; pesticide is a named FSVP contamination row | Ask directly; photograph any spray equipment and product labels |
| A9 | **Soil / water** — is irrigation used; water source; any known soil contamination history | Cadmium and heavy metals enter via soil. **This is the earliest warning we can get** | Ask; note any former mining/industrial use nearby |

> **On cadmium specifically.** Our current understanding is that the **EU is the binding constraint**, not China (`OSCAR_FARM_CHINA_ACTION_PLAN.md` §3 — China sets *no* cocoa cadmium limit; its 0.5 mg/kg figure is the **lead** limit). A targeted search for Brazil-specific cadmium-in-cacao data returned **zero hits** per `CACAO_RESEARCH_BIBLIOGRAPHY.md`. **Indonesia is an equally thin data environment.** So do not accept "Indonesian cocoa is low-cadmium" as a starting assumption — it must be measured, and §2.5 specifies how.

### 2.2 In the factory

| # | Ascertain | Decision it feeds | Evidence |
|---|---|---|---|
| B1 | **Roasting facility** — equipment, batch capacity, temperature/time profile, who controls it | Flavour; also determines whether they can roast to *our* spec or only their own | Photos + the actual profile if they will share it |
| B2 | **Winnowing / cracking** — equipment, nib recovery rate, husk separation method | Yield; shell content is a quality defect | Photos; ask recovery % |
| B3 | **Melanger / refining** — stone vs ball mill, capacity kg/batch, hours per batch, liquor vs powder output | Whether they can produce at our volume; determines lead time | Photos, batch time, capacity |
| B4 | **Fridge / cooling for setting bars** — tempering method, cooling tunnel or fridge, temperature | Bar finish and shelf stability | Photos |
| B5 | **Hygiene and pest control** — cleaning regime, pest control contract, foreign-object controls | The FSVP contamination rows (rocks, debris, cleaning-agent residue) | Photos; ask for the pest-control record |
| B6 | **Traceability in-plant** — can they keep *our* lot separate from others? How is it marked? | **Critical.** If our beans get commingled, every origin and lab claim collapses | Ask to see lot tagging; photograph |
| B7 | **Allergen / cross-contact** — anything else run on the same lines (nuts, dairy)? | Labelling and liability | Ask directly |

### 2.3 Warehousing

| # | Ascertain | Decision it feeds | Evidence |
|---|---|---|---|
| C1 | **Bean storage** — bag type (jute / GrainPro), palletisation, stack height, capacity in tonnes | Quality retention; capacity ceiling | Photos |
| C2 | **Temperature and humidity control** — measured or ambient? Any data logger? | Mould and insect risk; tropical ambient storage is the hard case | Ask for readings; photograph any hygrometer |
| C3 | **Fumigation / IPM practice** — what is used, how often, and is residue a concern | Residue compliance; fumigation records are an FSVP artifact | Ask for the record |
| C4 | **SOP** — does a written warehouse SOP exist? Ask for a copy | The governor's note: *"warehousing facility (check relevant SOP)"*. TrueSight has a Brazil counterpart (`brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md`) but **no Indonesian SOP exists yet** — if they have one, it is a starting point | Copy of the document, if it exists |
| C5 | **Security and shrinkage** — who has keys, any theft history | Cost of doing business | Ask |

### 2.4 Transport and export infrastructure

| # | Ascertain | Decision it feeds | Evidence |
|---|---|---|---|
| D1 | **Farm → warehouse** — who moves it, vehicle type, distance, time, cost per trip | First-mile cost; bean damage risk | Ask; photograph vehicle if present |
| D2 | **Warehouse → factory → back** — same questions, both legs | Middle-mile cost, often forgotten in landed-cost models | Ask |
| D3 | **Trucking company** — named company, not "a trucker" | Contractability and insurance | Name + contact |
| D4 | **Freight forwarder** — company, and **which ports** they actually use for air and for sea | Determines our shipping lane. **Name the port** — Makassar, Surabaya, Jakarta (Tanjung Priok) are very different lanes | Name + port(s) |
| D5 | **Customs clearance agent** — company, licence, experience with cocoa / food | Clearance is where small shipments die | Name + contact |
| D6 | **Export documentation capability** — can they produce phytosanitary cert, certificate of origin, and a **lab report** without us chasing? | If not, we carry that burden | Ask what they can produce |
| D7 | **Container loading** — where, and can they load a full container or only LCL? | LCL for a first shipment is normal but expensive per kg | Ask |

### 2.5 Lab testing

**Use CIC as the template.** We already have a working lab — see §2.5.1. The Indonesian lab should be asked *the same questions CIC already answers*, so the two datasets are comparable. Read §4 for what we have and have not actually received.

| # | Test | Status in what we hold |
|---|---|---|
| E1 | **Heavy metals — Arsenic (As), Cadmium (Cd), Lead (Pb), Copper (Cu)** | ✅ **Evidenced.** ICP-MS, to ANVISA limits — the panel in both reports on file (AGL4/Oscar `LAP-339.2025.B`, AGL8/Paulo `LAP-340.2025.B`) |
| E2 | **Active ingredients — flavanols/flavonoids, theobromine, caffeine** | 🟡 **Reported by the governor as offered by CIC; not visible in the two reports on file.** Whether the Sept-2026 CIC invoice (NF 0097) covers this panel is **unconfirmed** — see §4. Ask CIC to confirm and quote it explicitly |
| E3 | **Ochratoxin A** | 🟡 Planned (**B4**); CIC lists "micotoxinas" among its food-safety analyses — quote it |
| E4 | **Pesticide residues** | 🟡 Planned (**C1**); CIC lists "pesticidas" explicitly |
| E5 | **Microbiological** (salmonella — a named FSVP hazard) | 🟡 CIC lists "microbiológica"; confirm both labs offer it |
| E6 | **Cut test / classification** | ✅ **This is CIC's flagship.** ISO 2451 (export / fine-cacao reference) **and** IN 38/MAPA (Brazil's official norm). CIC is the **only MAPA-habilitated lab** for official cacao bean classification. **Ask Indonesia for its national equivalent and whether the lab is government-accredited** |
| E7 | **pH** | ✅ Included in CIC's cut test at no extra charge |

#### 2.5.1 How CIC does it — our benchmark lab

**Centro de Inovação do Cacau (CIC)**, Ilhéus/BA — at UESC/IPAF, Rodovia Jorge Amado km 16. Contact `recepcao@pctsul.org` (análises) / `cic@pctsul.org` (parcerias, financeiro) / WhatsApp (73) 99142-0002. **We are an existing customer** — invoiced for análises on BLACK KING (NF 0097, VENDA 120634, 30 Sep 2026).

**Published rates and sample requirements** (from CIC's own service FAQ, 2026):

| Service | Price | Sample | Turnaround |
|---|---|---|---|
| Cut test / classification — **ISO 2451 + IN 38/MAPA** (pH included) | **R$120** / sample | **~1.5 kg** beans | ~10 business days |
| Cupping — *unroasted* beans, sensory defects | **R$150** / sample | ~500 g | ~10 business days |
| Sensory — liquor / finished chocolate | **R$400** | 500 g finished, or 2 kg beans if CIC must prepare | — |
| **ADQ** — quantitative descriptive analysis (for comparing lots precisely) | **R$2,500** | 2 kg beans or 1.5 kg finished | — |
| Metals / mycotoxins / microbiological / pesticides | *quoted per package* | — | — |
| Soil analysis | *quoted* | — | — |

**Method notes worth copying into the Indonesian ask:**

- **One shipment can cover several tests.** ~1.5 kg covers ISO 2451 + IN 38 + cupping together — do not send three parcels where one will do.
- **Sample logistics are the customer's risk.** CIC accepts hand delivery (Mon–Fri 08:00–12:00, 13:00–16:50) or carrier — **Águia Branca, Cidade Sol, Azul Cargo** — or Correios. Transit is entirely the client's responsibility.
- **Metals and similar packages may need a dedicated submission form**; routine tests need only clear lot identification.
- **Results arrive by email** as a laudo; packages are quoted by a human, not off a price list.
- **The bioactive panel is not on the public catalogue.** CIC's published list names *metals, mycotoxins, microbiological, pesticides, "entre outras"* — the alkaloid/flavanol panel sits behind "among others". **This is exactly why it must be asked for explicitly rather than assumed.**

**What to ascertain about the lab itself:**

- Which **laboratory** — name, and is it accredited (KAN / ISO 17025)?
- **Sampling protocol** — composite or single-origin? How many beans, from how many bags? *"Send us a report"* is not a sampling plan.
- **Matrix tested** — beans, nibs, liquor, or powder. Metals **concentrate with cocoa-solids content**, so a clean nib result does **not** transfer to powder or a high-percentage bar. This distinction has already mattered once (`OSCAR_FARM_CHINA_ACTION_PLAN.md` §3).
- Turnaround time and cost per sample.

### 2.6 Digital and payments

| # | Ascertain | Decision it feeds | Evidence |
|---|---|---|---|
| F1 | **Internet access** — can they upload to `sunmint.truesight.me` (or a new mirror) from the farm *and* the factory? Speed, and is it mobile data or fixed line? | Whether farmer-side data entry is even possible. **Test it live** — do not ask "is there internet", ask them to load a page | Photo of a speed test on site |
| F2 | **Payment rail** — what is used locally. Brazil runs on **PIX**; Indonesia's nearest analogues are **QRIS** (QR payments) and **BI-FAST** (instant bank transfer) — *confirm which is actually used in this region* | How we pay farmers without cash and without an OJK-licensed lending structure (see the LOI's trade-advance framing) | Name of service; **fee**, per-transaction and percentage |
| F3 | **Banking** — which bank, and can they receive an international transfer? | Whether payment runs direct or through an intermediary | Ask |
| F4 | **Fees, explicitly** — does the payment service charge, and who bears it? | Changes the real cost per kg | Ask directly; do not infer |

### 2.7 Capacity

| # | Ascertain | Unit | Why |
|---|---|---|---|
| G1 | **Farm production** — annual output, and how much is already committed elsewhere | tonnes/yr | Free volume is what we can actually buy; total output flatters |
| G2 | **Factory processing** — monthly throughput | tonnes/month | The real bottleneck is usually here, not the farm |
| G3 | **Storage capacity** | tonnes | Determines whether they can hold a lot for us |
| G4 | **Seasonality** — harvest months; is there a main and a mid crop? | calendar | Drives our shipping windows and cash flow |
| G5 | **Growth headroom** — what would they need to double output? | narrative | Tells us the honest constraint |

---

## 3. Register B — commercial capture

Same rule throughout: **a number, or an explicit "not quoted".** No estimating.

| Item | Rate / value | Unit | Basis (per what?) | Brazil benchmark |
|---|---|---|---|---|
| Farm-gate bean price | | IDR / kg | wet or dried? fermented? | ☐ known — cite source |
| Fermentation service, if separate | | IDR / kg | | ☐ none |
| Drying, if separate | | IDR / kg | | ☐ none |
| Factory processing fee | | IDR / kg | liquor? nibs? | ☐ known — cite source |
| Farm → warehouse freight | | IDR / kg or / trip | | ☐ known — cite source |
| Warehouse → factory freight | | IDR / kg or / trip | | ☐ known — cite source |
| Warehousing | | IDR / kg / month | | ☐ known — cite source |
| Lab — metals (4-metal panel) | | IDR / sample | per ICP-MS run | ☐ known (AGL4/AGL8) |
| Lab — active ingredients | | IDR / sample | | ☐ none — never commissioned |
| Export clearance / agent | | IDR / shipment | | ☐ known — cite source |
| Sea freight | | USD / container | which port → which port | ☐ known — cite source |
| Air freight | | USD / kg | | ☐ known — cite source |
| Payment service fee | | % or flat | | PIX ≈ 0 for individuals |
| **Landed cost to destination** | | USD / kg | **the number that matters** | ☐ known — cite source |

> **On the Brazil benchmark column:** the TrueSight Brazil lane already has freight, warehouse, and lab data in `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`, `brazil/ILHEUS_WAREHOUSE_MANAGEMENT.md`, and the two lab reports. Those should be filled in from source **before** this table goes to Rusmin, so the comparison is available in the room rather than reconstructed afterwards.

---

## 4. The gap worth stating plainly

**The ask to Indonesia is broader than the evidence we currently hold.**

The two reports we actually hold — AGL4/Oscar and AGL8/Paulo — cover **four heavy metals by ICP-MS against ANVISA**. Flavanols, theobromine, caffeine, ochratoxin A and pesticide residues do **not** appear as results in either report.

> **Correction (2026-11-25).** An earlier draft of this document said these had *"never been commissioned anywhere."* **That overstated the evidence.** What is actually known: two lab reports are on file and neither shows the bioactive panel. **Absence from two reports is not proof we never bought it** — and we are an existing CIC customer with a Sept-2026 analyses invoice (NF 0097) whose line items are **inside the attached NFSe PDF, which has not been opened.** The honest status is *"not evidenced in the reports on file"*, and the governor reports that CIC does offer caffeine, flavonoid and theobromine testing. **First action: confirm with CIC what NF 0097 covered and get the bioactive panel quoted explicitly.**

That is not a reason to drop the ask — active-ingredient data is exactly what the premium-story positioning needs, and the LOI already leans on quality rather than yield. But it has three consequences:

1. **Budget it.** If the bioactive panel has not already been run, this is new spend, not a routine request.
2. **Do not present it as existing practice** to Rusmin, or we will be asked to show our own reports and will have four metals and no flavanols.
3. **Order it consistently.** If we test Indonesia for flavanols and never test Brazil, we have no comparison and cannot claim either is better. The honest sequence is to commission the same panel on **one Brazil lot** as a control.

---

## 5. Boundary conditions for the visit

- **Rusmin is a warm contact, not an audited supplier.** This checklist is thorough because the *facts* must be thorough, not because the relationship is adversarial. Language should stay collegial — the visit is "help us understand your operation", not "we are evaluating whether you qualify". The FSVP paperwork, if we proceed, is a separate downstream artifact.
- **Consent for photos of people.** `A6` asks for farmer photos and stories. Those may later appear on agroverse.shop. **Ask permission at the time, and record that it was given.** A portrait taken without consent cannot be published, which makes it worthless for the purpose it was taken for.
- **Never invent coordinates.** `fsvp/SITE_VISIT_PROCESS.md` is explicit on this: if EXIF GPS is absent — and messaging-app transit usually strips it — take coordinates from a device on site or from the governor. A compliance document with guessed coordinates is worse than one with none.
- **Nothing here is a commitment.** Rates captured are observations for modelling, not agreed prices. No volume, price, or exclusivity should be implied during the visit.

---

## 6. Downstream — what this feeds

If the visit proceeds well, this document is the **input** to three existing artefacts, so no second trip is needed:

| Artefact | Process |
|---|---|
| **FSVP site-visit log** | `fsvp/SITE_VISIT_PROCESS.md` — the canonical 7-page PDF. Its observation rows (farm: salmonella/insects/foreign objects; fermentation: non-cacao inclusion/pesticides; drying: mould/foreign objects/cleaning residue) are **already covered** by §2.1 A4–A5 and §2.2 B5, so capture with that structure in mind |
| **Supplier entity profile** | `brazil/CACAO_SUPPLIER_ENTITY_PROFILES.md` pattern — entity.json + source documents |
| **Farm page** | `agroverse/AGROVERSE_FARM_PAGE_CONVENTIONS.md` — why A6 (photos, stories, variety) is asked for on site |

---

## 7. Open questions for the governor

| # | Question |
|---|---|
| 1 | **Who attends?** Photo/measurement discipline is much easier with two people. Is this Gary alone, or with Rusmin hosting throughout? |
| 2 | **Which site(s)?** One farm + one factory, or a circuit? Affects how much of §2 is realistic in one visit |
| 3 | **Does Rusmin see this document in advance, or is it our internal brief?** It reads differently depending on the answer — advance sharing turns it into a request, internal keeps it a prompt sheet |
| 4 | **Budget approval** for the expanded lab panel (§4) — needed before we ask anyone for it |
| 5 | **Fill the Brazil benchmark column** before issue — should I populate it from `brazil/` sources now? |
| 6 | **Confirm NF 0097's line items with CIC** (`recepcao@pctsul.org`), and ask them to quote the **flavonoid / theobromine / caffeine** panel explicitly — it is not on their public catalogue, so it needs naming |
| 7 | **Should the CD test (ISO 2451 + IN 38) be requested of Indonesia too?** It is cheap (R$120), fast (~10 days), and is the classification buyers actually recognise. Indonesia has its own national norm — ask which |
