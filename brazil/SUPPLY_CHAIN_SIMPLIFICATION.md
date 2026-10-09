# Supply Chain Simplification — Cooperative-First Sourcing & Ilhéus Wind-Down

> **Decision recorded:** 2026-10-09 · **Authority:** Gary Teh (governor, thread 780) · **Recorded by:** Sophia Truesight (TrueSight DAO Autopilot)
> **Status:** DECIDED — codified; follow-through items tracked in `OPEN_FOLLOWUPS.md`.
> **Sources:** `brazil/CACAO_SOURCING_NETWORK_OVERVIEW.md`, `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md`, `SUPPLY_CHAIN_AND_FREIGHTING.md`, `PURPOSE_AND_MISSION.md`.

---

## 1. The decision (two parts)

1. **Cooperative-first sourcing.** The DAO stops acting as the direct passthrough for independent farmers. All cacao sourcing funnels through the **producer cooperatives** (Coopercabruca / Bahia; CEPOTX / Pará). Governor's words: *"dealing with independent farmers is more hassle than worth it… just funnel everything through the cooperatives moving forward."*
2. **Wind down the Ilhéus (Black King) warehouse.** *"No point maintaining the Ilhéus warehouse too."* No logistics reason remains for a DAO-purpose warehousing facility there.

## 2. Rationale (facts earned over "two cycles")

The 2024 gap — the DAO as passthrough for independent farmers — opened in 2024 and *"started incurring a lot more management overhead than anticipated."* It is being closed after **two cycles** (~two years) of operating the engine by hand. The simplifications below are only safe **because** two cycles of operation produced the underlying facts:

- **Bahia produces cacao year-round** → no need to prestock (Orlantildes).
- **PO → destination port ≈ 5 months** from this patch of the Atlantic rainforest.
- **Pará / CEPOTX in-network conversion comes online 2027** (Jedielcio) → no reason to freight Pará beans to Bahia for conversion *before* arrival at destination port.
- **Vivi** is the only remaining non-cooperative farmer in-network, and **no beans were stocked from him this year**.

> **Principle:** you cannot abstract a layer you have not personally operated. Two cycles is the tuition; the move up an abstraction layer (operator → architect) is earned, not assumed.

## 3. What changes

| Aspect | Before (two-cycle operator model) | After (cooperative-first architect model) |
|---|---|---|
| Independent farmers | DAO passthrough; per-farmer overhead | Funnel through cooperatives; DAO no longer the passthrough |
| Oscar (flagship independent) | Independent intake via Black King lane | **Joining Coopercabruca** (agreed 2026-10-09) → beans move via coop MAPA + NF-e |
| Ilhéus warehouse | DAO-purpose stockpile + demand-sensing | **Wound down** (retire/transfer) |
| Prestock | Multi-year buffer against lead time | None — year-round Bahia supply + 5-mo PO→port |
| Conversion | Freight beans to Bahia → convert | Pará in-network conversion (2027); Bahia hub only for scale until proven |
| DAO role | Operator (fills gaps by hand) | Architect (coordination + proof layer) |

## 4. Keep (non-commodity) vs delegate (commodity)

**Keep in-house:** lineage / verification / QR serialization · finance entity (Próspera LLC) · FSVP (TrueTech Inc as US importer-of-record) · brand + GTM · tree-planting lineage (Sunmint / CRF) · **coordination of the coop/partner network**.

**Delegate:** warehousing (wind down) · conversion (Coopercabruca now; Pará 2027) · freight / customs / docs · farm-to-facility logistics.

**Structural note.** MAPA/GACC attach to the **production enterprise** (the facility that processes/benefits beans), not the exporter/trader. Independent farmers never needed MAPA *if* their beans pass through a registered beneficiation facility — so the **cooperative membership is what supplies that facility**. That is precisely why the coop is the durable funnel.

## 5. Blocking question — Oscar (resolved)

`BRAZIL_EXPORT_LANE_LEARNINGS.md` listed **Oscar** (with Clara, Analuana, Vivi) as **independent** ("no MAPA, no factory"), yet `CACAO_SOURCING_NETWORK_OVERVIEW.md` lists **"Oscar brand cacao — 500 g bars"** on the **Coopercabruca** lane — a mismatch.

**Resolved 2026-10-09: Oscar has agreed to join Coopercabruca.** His 2026 harvest (**108 kg loaded into AGL16 on 2026-10-07**, handled by Matheus Reis) now has a legitimate route through the coop's MAPA + NF-e rather than the retiring independent / Black King lane. Oscar is the flagship farm (AGL4 ceremonial, `2024OSCAR_*` tokenized batches, LA-launch SKUs) — preserving his lane preserves the relationship.

## 6. Open follow-through (tracked in `OPEN_FOLLOWUPS.md`)

1. **Ilhéus wind-down mechanics + FDA/FSVP tail.** The facility carries **4 live obligations** already in `OPEN_FOLLOWUPS.md`: the 2026-09-12 GMP CAPA (filth/pest finding), the pest-control written-assurance addendum (21 CFR 1.511), the unassigned hygiene/pest-control owner, and the Black King CNPJ INAPTA blocker. Because Black King **cannot issue export NF-e** (CNPJ INAPTA), the final stock must clear **through Coopercabruca's paperwork** — which is itself the **first deliberate run of the new model**. Sequence: clear-final-beans-via-Coopercabruca → cure/document the 4 FSVP items in writing → then decommission.
2. **Demand-signal replacement.** Retiring the Ilhéus stockpile removes not only a lead-time buffer but the ability to *"sense demand before committing to a conversion/SKU."* With a 5-month lead time and year-round supply this becomes a **forecast** requirement. Name the replacement before the buffer is gone — never remove a buffer until its replacement is named.
3. **Remaining independents.** Clara, Analuana, and any future inbound independent must be routed to a **cooperative membership** (not merely redirected — a redirect is not a route, since coops take only member-farmed beans). Vivi's disposition is the open case (no beans stocked this year).
4. **Pará 2027.** Confirm the CEPOTX factory online date and validate **export-scale** conversion (currently "unproven"; Bahia remains the conversion/export hub for scale until proven).

## 7. Provenance

- Governor instruction, thread 780, 2026-10-09: cooperative-first sourcing · "No point maintaining the Ilhéus warehouse too" · "Oscar has agreed to join Coopercabruca."
- Prior context: `brazil/CACAO_SOURCING_NETWORK_OVERVIEW.md`, `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md`, `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`, `PURPOSE_AND_MISSION.md`.
