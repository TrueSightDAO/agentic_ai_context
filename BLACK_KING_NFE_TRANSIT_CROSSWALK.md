# Black King (Matheus Reis Pereira) - NF-e / transit-register crosswalk

**Generated:** 2026-09-18 - Sophia Truesight (autopilot) - thread 31905
**Revision 3** (2026-09-18): added the **Taraval Street destination rule** (NF-e destino
`TRUETECH INC - TARAVAL ST, 3041` ⟹ physical recipient **Val Lapidus**) and flagged the
NF11/NF12/NF14 register-vs-NF-e destination conflict. Revision 2 corrected cardinality to 1:N
and removed an empty-key join artifact.
See `` CHANGELOG `` at the foot.

**Purpose:** the authoritative join between the **15 SEFAZ-issued NF-e** (keyed by
44-digit *chave*) and the **arrival register** (keyed by *tracking number*). The two source
documents share **no common key** - this file **is** the crosswalk.

---

## Sources

| Source | What it provides |
|---|---|
| Main Ledger `shipment_nfe` tab (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`) | NF-e #, chave, issue date, value, recipient, SEFAZ status, `Supersedes`/`Superseded By`, **Parcel Tracking Number** binding |
| Main Ledger `offchain assets in transit` tab (gid `1888711771`) | the **arrival register** - per-parcel tracking # -> destination member -> ledger line # -> status |
| `CORREIOS_SHIPMENTS.md` (agentic_ai_context) | 14-track Correios index; shipping receipts + post-arrival holders per parcel |
| `fda_fsvp/suppliers/black_king/notas_fiscais/` | the 15 DANFE PDFs (chave-named) |
| `black_king_shipments.json` / `BLACK_KING_SHIPMENT_MANIFESTS.md` (Rev-9) | FDA prior-notice-based US-lane manifests + EO-14324 context |

## Join key - and its cardinality

**Tracking number** - `shipment_nfe!K` (*Parcel Tracking Number*) <-> register column K.

**Cardinality is 1 : N.** One NF-e covers a **product-mix box**; the register records **one row
per product line**, so a single NF-e maps to **one OR MANY** register rows. Example: NF12
(`CP340993869BR`) -> **3** register rows (AGL8 40 g bars + husk + insulated box).

**Blank is NOT a key.** An NF-e or register row with a blank/`NA` tracking does **not** join to
another blank - doing so produces a false many-to-many. Blank on the NF-e side = *no parcel*;
blank on the register side = *tracking not recorded*.

---

## Destination rule - "Taraval Street" in an NF-e = Val Lapidus

**Governor-confirmed (Gary Teh, thread 31905, stated twice):** *"If anything is to Taraval
street in the Nota fiscal it is actually landing at Val Lapidus location."*

The DANFE *DESTINATARIO* on this corridor almost always reads the **TrueTech Inc fiscal
address** `TRUETECH INC - TARAVAL ST, , 3041 SAO FRANCISCO EXTERIOR-EX` - **verified in 13 of
the 15 DANFE PDFs** (`black-king-nota-fiscal-raw/nfe/`, PyMuPDF grep of the destinatario
block). So an NF-e reading "Taraval St" means the goods are **physically landing at
Val Lapidus (3041 Taraval St, San Francisco, CA 94116)** - not at a generic "TrueTech" site.

| NF-e destinatario text | Physical recipient |
|---|---|
| `TRUETECH INC - TARAVAL ST, 3041 SAO FRANCISCO EXTERIOR-EX` | **Val Lapidus** (3041 Taraval St, SF 94116) |
| `ANDREA CATALINA FALCON RIOS DE PABST - RUA LINDENGUT, 10 GLARUS` | Andrea Catalina (CH) - NF5 |
| `AGNIESKA MARECKA - UL. KOSCIUSZKI 10 LOK, 1 POLONIA` | Aga Marecka (PL) - NF9 |

> **Corollary - Taraval != Hayes.** **1423 Hayes St** (the other TrueTech address,
> `WORKSPACE_CONTEXT.md` Sec 3c) is a **different** physical site, held by **Kirsten
> Ritschel**. Do not conflate the two TrueTech addresses. See
> `references/SHIPPING_ADDRESSES_REFERENCE.md`.

---

## Table 1 - NF-e -> register lines (all 15; 1:N)

| NF-e | Date | Value (R$) | Recipient | SEFAZ | Tracking | Register rows | State |
|---:|---|---:|---|---|---|---|---|
| 1 | 2024-11-04 | 2,000.00 | TRUETECH INC | Autorizada | `CP340992695BR` | **0** | register gap (arrived per Correios index) |
| 2 | 2024-11-04 | 4,500.00 | TRUETECH INC | Autorizada | `CP340992687BR` | **0** | register gap (arrived per Correios index) |
| 3 | 2025-01-30 | 544.80 | TRUETECH INC | Autorizada | `CP340992735BR` | **1** (row 2) | linked |
| 4 | 2025-02-19 | 2,362.00 | TRUETECH INC | Autorizada | *(blank)* | 0 | **no parcel** |
| 5 | 2025-02-25 | 1,125.00 | ANDREA CATALINA F. RIOS DE PABST | Autorizada | `CP340993838BR` | **2** (rows 10, 11) | linked (1:N) |
| 6 | 2025-03-06 | 2,000.00 | TRUETECH INC | **Cancelada** | `NA` | 0 | superseded by NF7 |
| 7 | 2025-03-06 | 2,000.00 | TRUETECH INC | Autorizada | *(blank)* | 0 | **no parcel** |
| 8 | 2025-03-06 | 1,000.00 | TRUETECH INC | Autorizada | `CP340992761BR` | **1** (row 12) | linked |
| 9 | 2025-03-06 | 500.00 | AGNIESKA MARECKA | Autorizada | `CP340993237BR` | **1** (row 14) | linked |
| 10 | 2025-04-01 | 800.00 | TRUETECH INC | Autorizada | `74 4476 6210` (DHL) | **1** (row 13) | linked |
| 11 | 2025-04-28 | 500.00 | TRUETECH INC | Autorizada | `CP340993988BR` | **1** (row 16) | linked |
| 12 | 2025-06-04 | 466.71 | TRUETECH INC | Autorizada | `CP340993869BR` | **3** (rows 17, 18, 19) | linked (1:N) |
| 13 | 2025-06-20 | 2,250.00 | TRUETECH INC | **Cancelada** | `NA` | 0 | superseded by NF14 |
| 14 | 2025-06-20 | 2,250.00 | TRUETECH INC | Autorizada | `CP340993299BR` | **1** (row 20) | linked |
| 15 | 2025-09-23 | 1,000.00 | TRUETECH INC | Autorizada | *(blank)* | 0 | **no parcel** |

> **NF1 / NF2 caveat.** Both carry tracking numbers *, and the Correios index shows those
> parcels arrived* (shipping receipts + post-arrival holders exist), **but they have no row in
> the arrival register**. They are therefore a **register gap**, not a verified register link.
> The register is **missing 3 of the 14 Correios trackings**: `CP340992130BR`, `CP340992687BR`
> (NF2), `CP340992695BR` (NF1). **The register is not a superset of the shipping index.**
>
> **Destination per the rule:** both carry the Taraval destinatario, so by the destination rule
> they land at **Val Lapidus**. Their register rows are missing (see `OPEN_FOLLOWUPS.md`).

> **⚠️ Destination conflict - NF11 / NF12 / NF14.** These three NF-e carry the **Taraval**
> destinatario (⟹ **Val Lapidus** by the rule above), **but** the arrival register routes their
> trackings (`CP340993988BR`, `CP340993869BR`, `CP340993299BR`) to **Kirsten Ritschel /
> 1423 Hayes St**. Either the register destination member is mislabelled, or those parcels went
> physically to Hayes despite a Taraval NF-e. **Unresolved - needs governor confirmation before
> the register is rewritten** (no silent data mutation). Filed in `OPEN_FOLLOWUPS.md`.

## Table 2 - arrival register -> NF-e (all 19 rows)

| Reg. row | Destination | Origin asset | Qty | Courier | Tracking # | Ledger line(s) | Status | NF-e |
|---:|---|---|---:|---|---|---:|---|---|
| 2 | Val Lapidus | 8 oz Kraft Pouch | 120 | Correios | `CP340992735BR` | 296 | Arrived | **NF3** |
| 3 | Val Lapidus | Cacao Mass Bar 40 g | 125 | Correios | `CP327946643BR` | 10 | Arrived | none |
| 4 | Val Lapidus | Cacao Mass Bar 500 g | 10 | Correios | `CP327946643BR` | 9 | Arrived | none |
| 5 | Val Lapidus | Cacao Nibs 8 oz pouches | 44 | Correios | `CP327946643BR` | 11 | Arrived | none |
| 6 | Nima Kaz (FounderHaus BR) | 8 oz Kraft Pouch | 50 | Correios | `QN226716310BR` | 248, 316 | Arrived | none |
| 7 | Hans Martin Heierling (CH) | 8 oz Kraft Pouch | 25 | Correios | `CP340993268BR` | 313, 364 | Arrived | none |
| 8 | Aga Marecka (PL) | 8 oz Kraft Pouch | 25 | Correios | `CP340993271BR` | 311 | **Rejected** | none |
| 9 | Aga Marecka (PL) | Cacao Mass Bar 500 g | 10 | Correios | `CP340993271BR` | 312 | **Rejected** | none |
| 10 | Andrea Catalina (CH) | Cacao Mass Bar 500 g | 10 | Correios | `CP340993838BR` | 357, 452 | Arrived | **NF5** |
| 11 | Andrea Catalina (CH) | 8 oz Kraft Pouch | 25 | Correios | `CP340993838BR` | 359, 454 | Arrived | **NF5** |
| 12 | Val Lapidus | Cacao Mass Bar 500 g | 19 | Correios | `CP340992761BR` | 462, 463 | Arrived | **NF8** |
| 13 | Val Lapidus | Cacao Molasses 250 ml | 20 | DHL | `74 4476 6210` | 484 | Arrived | **NF10** |
| 14 | Aga Marecka (PL) | Cacao Mass Bar 500 g | 10 | Correios | `CP340993237BR` | 469, 470 | Arrived | **NF9** |
| 15 | Kirsten Ritschel | Cacao Husk (KG) | 1 | (none) | *(blank)* | (none) | **Rejected** | **none** |
| 16 | Kirsten Ritschel | Cacao Nibs (KG) | 20 | Correios | `CP340993988BR` | 505 | Arrived | **NF11** |
| 17 | Kirsten Ritschel | Cacao Mass Bar 40 g (AGL8) | 115 | Correios | `CP340993869BR` | 25,26,31,32 | Arrived | **NF12** |
| 18 | Kirsten Ritschel | Cacao Husk loose g (AGL8) | 1.343 | Correios | `CP340993869BR` | 27,28,29,30 | Arrived | **NF12** |
| 19 | Kirsten Ritschel | 22 L Insulated Box | 1 | Correios | `CP340993869BR` | 638 | Arrived | **NF12** |
| 20 | Kirsten Ritschel | Cacao Mass Bar 500 g (AGL10) | 40 | Correios | `CP340993299BR` | 734, 735 | Arrived | **NF14** |

---

## The states

### A. NF-e linked to an arrived parcel (8)
NF3, NF5, NF8, NF9, NF10, NF11, NF12, NF14.

> **Weight reconciliation check (passes):** NF3 declares **27.24 kg cacao nibs**; the register
> binds `CP340992735BR` to **120 x 8 oz (227 g) Kraft Pouches = 120 x 0.227 = 27.24 kg**. The
> crosswalk reconciles, it is not just a join.

### B. NF-e with tracking but NO register row - register gap (2)
**NF1** (`CP340992695BR`) - **NF2** (`CP340992687BR`). Both `Autorizada`; both parcels appear in
`CORREIOS_SHIPMENTS.md` with shipping receipts, so they likely arrived - but the arrival register
has no row. Fix = add the register rows (or note the exemption).

### C. NF-e issued, NO parcel - invoiced but never landed (3)
**NF4** (R$2,362, 19/02/2025) - **NF7** (R$2,000, 06/03/2025) - **NF15** (R$1,000, 23/09/2025).
All `Autorizada`, tracking blank. **Write-off candidates** - no arrival, no FDA prior notice, no
shipping receipt.

- NF7 is the reissue of the **cancelled NF6** (both 06/03/2025, both R$2,000, 40 x 500 g bars).
- NF15 (20 x 500 g bars, 23/09/2025) sits ~6 weeks **after** EO-14324 (de-minimis suspension
  effective 2025-08-29) - the post-cutoff lane produced no prior notice.

### D. Cancelled / superseded (2)
**NF6 -> NF7** and **NF13 -> NF14** - cancel-and-reissue pairs (same value, same issue date).
R$4,250 is duplicated, **not** lost cargo.

### E. Register rows with NO NF-e (8 rows / 5 parcels)
- **`CP327946643BR`** - AGL2/AGL6-era SF parcel (rows 3-5). Predates the NF-e set.
- **`QN226716310BR`** - FounderHaus **Brazil-domestic** (Nima Kaz) (row 6).
- **`CP340993268BR`** - **Switzerland** (Hans Martin Heierling) (row 7).
- **`CP340993271BR`** - **Poland**, **Rejected** by Brazilian customs (rows 8-9).
- **(row 15)** - Kirsten husk, **trackingless**, **Rejected** (1 row).

> **Note:** Europe consignments *do* normally carry an NF-e - **NF5** (Andrea Catalina, CH) and
> **NF9** (Aga Marecka, PL) both exist. So the Europe parcels above are a **genuine documentation
> gap**, not 'no NF-e by design'. `CP340993271BR` is the **rejected 1st Poland parcel** - its
> sibling (2nd Poland parcel `CP340993237BR`) *is* covered by NF9.

---

## Corridor summary

| NF-e state | Count |
|---|---:|
| Linked to >=1 register row | **8** |
| Tracking but no register row (register gap) | **2** (NF1, NF2) |
| Issued, never shipped (write-off candidates) | **3** (NF4, NF7, NF15) |
| Cancelled / superseded | **2** (NF6, NF13) |
| **Total NF-e** | **15** |

| Register state | Count |
|---|---:|
| Rows joined to an NF-e | **11** |
| Rows with no NF-e | **8** (5 distinct parcels) |
| **Total register rows** | **19** |

**Bottom line for the tax accountant:** of 15 chaves, **8** tie to a physically arrived parcel
(1 NF-e : N register lines), **2** are arrived-but-unregistered (NF1, NF2), **2** were
cancelled/reissued, and **3** (NF4, NF7, NF15) are invoiced-but-never-shipped write-off
candidates. On the register side, **8 of 19 rows** (5 parcels) carry **no** NF-e and need one
issued or an exemption noted.

---

## CHANGELOG

**Rev 3 (2026-09-18)** - destination rule added after governor input (thread 31905):
1. **"Taraval St" NF-e destination rule.** Encoded the governor-confirmed rule that an NF-e
   whose destinatario reads `TRUETECH INC - TARAVAL ST, 3041` lands physically at **Val Lapidus**
   (3041 Taraval St, SF 94116). Verified 13/15 DANFE PDFs carry that destinatario.
2. **NF11 / NF12 / NF14 destination conflict flagged** (Taraval NF-e vs Hayes register rows) -
   left unresolved pending governor confirmation; no register rows changed.
3. **NF1 / NF2** annotated with their rule-derived destination (Val Lapidus) pending register rows.

**Rev 2 (2026-09-18)** - corrections after governor review:
1. **Cardinality fixed to 1:N.** Rev 1 listed each NF-e once; NF5 (2 rows) and NF12 (3 rows) were
   collapsed, silently dropping register lines. Table 1 now shows the row count and row ids.
2. **Empty-key join artifact removed.** Rev 1 joined blank-tracking NF4/NF7/NF15 to the
   blank-tracking register row 15 (Kirsten husk) and falsely reported NF4/7/15 -> row 15.
   Blank is **not** a key. Row 15 is now correctly listed as its own no-NF-e Rejected parcel.
3. **NF1 / NF2 status corrected.** Rev 1 marked them 'linked'; they have **no register row**
   (register gap). Corrected count of linked NF-e: **8** (was 10).

**Rev 1 (2026-09-18)** - initial crosswalk (PR #1269).
