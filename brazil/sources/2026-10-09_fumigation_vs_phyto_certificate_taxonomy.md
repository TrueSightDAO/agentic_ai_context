# "Phyto certificate" — four different things, and the fumigation service is not one of them

**Date:** 2026-10-09 · **Author:** Sophia Truesight (autopilot) · thread 10800
**Trigger:** governor question — *"Is the phyto certificate from the fumigation service"*
**Answer: No.**

---

## 1. Short answer

The fumigation company is a **private pest-control contractor**. A **phytosanitary certificate is a
government document** issued only by **MAPA / VIGIAGRO** — specifically by an *accredited federal
agriculture fiscal auditor*. A private dedetização receipt **cannot substitute** for it, and is not
something ASTRA can issue at any price.

### Evidence from our own document
The 2025 NFS-e in `fda_fsvp/suppliers/black_king/20250610_warehouse_fumigation.pdf` carries:

| Field | Value |
|---|---|
| Prestador | **ASTRA SUL BAHIA SANEAMENTO BÁSICO LTDA** (nome fantasia *ASTRAL SAÚDE AMBIENTAL*) |
| CNPJ | `07.463.430/0001-99` · IM `43966` · Simples Nacional |
| Tomador | **MATHEUS REIS PEREIRA** — CNPJ `50.042.585/0001-80` |
| Tomador address (fiscal) | Av. Tancredo Neves, 4900 — Ilhéus/BA |
| **Service code** | **`0713` — Dedetização, desinfecção, desinsetização, imunização, higienização, desratização, pulverização** |
| **CNAE** | **`8122200`** |
| Value | **R$ 300,00** — emitted 09/06/2025 18:01:59 |
| Footer text | *"SERVIÇO DE FUMIGAÇÃO"* |

Two different things appear on this one document, and conflating them is the error:
- **`0713` / CNAE `8122200`** = *pest-control services* — the **legal** classification.
- **"SERVIÇO DE FUMIGAÇÃO"** = **free-text** in the *Outras Informações* block — a **description of a
  service rendered and billed**, not an attestation of phytosanitary status.

⇒ **It is an invoice for work done. It is not, and cannot be, a phytosanitary certificate.**

## 2. The four artefacts this lane colloquially calls "phyto"

| # | Artefact | Who issues it | Ours? | Satisfies APHIS? |
|---|---|---|---|---|
| **1** | **Fumigation / dedetização service** | ASTRA SUL BAHIA — **private company** | ✅ NFS-e **09/06/2025 R$300** · **24/09/2026 R$405** | ❌ **No** |
| **2** | **Phytosanitary Certificate (CF)** | **MAPA / VIGIAGRO** — federal auditor | ❌ **none found in `fda_fsvp` or `agentic_ai_context`** | ✅ **Yes** (export side) |
| **3** | **ISPM#15 wood-packaging mark** | wood-treatment provider (IPPC stamp) | **N/A** — pallets declared **HDPE**, non-wood | n/a |
| **4** | **APHIS import permit** | **USDA APHIS** (via eFile) | ❌ not found | ✅ **Yes** (US side) |

> **#1 ≠ #2 ≠ #3 ≠ #4.** They are four different documents, from four different kinds of issuer, doing
> four different jobs. Chasing #1 harder will never produce #2.

## 3. Who owns what — the split that actually matters

### #2 Phytosanitary Certificate = **Brazil's obligation** (exporter side)
Per MAPA **Normative Instruction 12/2018, Appendix XXVI** (Export of Plants, Plant Parts and Plant
By-Products):

> *"Inspection and certification of plant products for export will take place **by request of the
> exporter**, and follow procedures and criteria for issuing the Phytosanitary Certificate (PC)
> established under MAPA Normative Instruction no. 29, dated 25 July, 2013."*

Issued on condition the **NPPO of the importing country's** requirements are met — i.e. **USDA/APHIS's**
requirements. Since COVID, e-signed with a **QR code** for authenticity; **only accredited federal
agriculture fiscal auditors with a valid token** may issue. It is a **government-to-government**
document — it cannot be purchased from a vendor.

⇒ This is the document **Omega / Matheus** would have to obtain via **VIGIAGRO**, and the one nobody
answered the 29/09 question about.

### #4 APHIS import permit = **OUR obligation** (importer of record = TrueTech Inc)
For cocoa beans, APHIS treats the commodity as **seeds**, so the applicable manual is
**"Seeds Not for Planting"**. The requirement is looked up in **ACIR** (Agricultural Commodity Import
Requirements — APHIS's single authoritative database since 30 Sep 2022, which **replaced** FAVIR and
three import manuals), and the permit is applied for via **APHIS eFile**. ACIR "also [lets you] check
whether you need to apply for a permit."

⇒ **This is squarely ours.** No amount of work in Brazil produces it — it is filed in the US, by the
importer.

## 4. NEW HYPOTHESIS — the 15 kg of **raw beans** may be holding all 302 kg

This is the sharpest thing this review produced.

| Cargo | Form | APHIS exposure |
|---|---|---|
| Nibs (29.26 + 80 + 99.50 kg) | **ground / processed** | low — processed product |
| Mass bar, ceremonial pouch (18.50 + 33.80 kg) | **ground / pasted** | low |
| Cacao butter (5 kg) | **rendered fat** | low |
| Cacao tea (21 kg) | dried plant material | medium |
| **"Cacao Almonds" — 10 kg + 5 kg = `15 kg`** | **WHOLE COCOA BEANS** (*amêndoas de cacau*) | **HIGH — literal seeds** |

Articles **0004 (10 kg)** and **0009 (5 kg, Pará samples)** on PN `F26X30142399` are **whole cocoa
beans**, not tree nuts and not processed product. Cocoa beans are *"technically considered seeds"* and
fall under APHIS's *Plants and Plant Products Not for Propagation* regime.

⇒ **If APHIS targeting keyed on seed material, 15 kg of raw beans could hold the other 287 kg.**
A single unpermitted seed line is enough. This is new, specific, and cheap to test.

Note also the 2023 precedent consignment (Coopercabruca, 100 kg) cleared **without** any APHIS permit or
phyto certificate on file — consistent with it having been a **processed** (nibs) shipment. **The
product mix may be what changed**, not the lane.

## 5. Our own process document may be the root cause

`fsvp/SHIPMENT_DOCUMENTATION_PROCESS.md` (Notes, last line) states:

> *"US lane does **not** need MAPA (only the China/GACC lane does) — see
> `brazil/BRAZIL_EXPORT_LANE_LEARNINGS.md`."*

If a phytosanitary certificate **is** required for cocoa beans from Brazil, then **that sentence is the
root cause of this omission** — it is precisely the assumption a CBP agriculture hold would falsify.

⚠️ **Flagged for governor review, not silently changed.** Amending a process doc on the strength of an
unverified requirement would repeat the error this whole thread is correcting.

## 6. The single highest-value next check

Before emailing anyone: **run the ACIR lookup for cocoa beans (Theobroma cacao) originating in Brazil**,
and read off the requirement set — then re-run it for **processed** forms (nibs/mass/butter, headings
1803/1804/1806) to see whether the answer differs from **whole beans** (1801).

That converts this from a *plausible taxonomy* into a **definitive, quotable requirement list** — and
it tells us whether the exposure is the whole consignment or just the 15 kg of raw beans.

## 7. What this changes in the pending ask

The email I had drafted asked Graziela/broker in general terms about "a phytosanitary certificate".
**Re-cut it** to name the artefact precisely:

1. **MAPA / VIGIAGRO Phytosanitary Certificate** — was one requested from the exporter, and was it issued?
2. **APHIS import permit** — does this HTS line require one; is one on file for TrueTech?
3. **What did the agriculture hold actually cite?** Any emergency action notice or CBP message?
4. **Which article triggered it** — and specifically, is it the **15 kg of whole beans**?

*Analysis only. Nothing sent, nothing purchased, no money moved.*
