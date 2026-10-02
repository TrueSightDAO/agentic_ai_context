# Airport weighing — Salvador: WEIGHT DIVERGENCE (gross 349 kg)

> **RESOLVED 2026-10-02:** Daniel / SeaCoast asked for the reissue → **Rev 15** Commercial Invoice + Packing List at **gross 349 kg** (`exports/2026-10-02_*_rev15_*`). See §5.5. Open: SeaCoast reissues HAWB/MAWB; **CC-e on NF-e nº 18** (bruto 322,06 → 349).

> **Source:** a weighing/notification document relayed by Gary (thread 10800, 2026-10-02 21:17 UTC), from the
> Brazilian export/freight side (forwarder / airport agent — **sender to be confirmed by Gary**; the text says
> *"fazermos a correção junto à CIA AÉREA"*, i.e. airline-side correction).

## The message (normalized)

**PT:** *"Prezados, boa tarde. Gentileza notar que a carga foi pesada no Aeroporto, e foi constatada divergência de
peso. Precisamos que sejam reemitidos: Commercial Invoice e Packing List com a informação de peso bruto = 349 kg.
Vamos reemitir HAWB e MAWB. Precisamos de todas as documentações de acordo, para fazermos a correção junto à CIA
AÉREA. Segue abaixo comprovação de pesagem."*

**EN:** *"The cargo was weighed at the airport and a **weight divergence** was found. We need the **Commercial
Invoice and Packing List reissued with gross weight = 349 kg**. We will reissue the **HAWB and MAWB**. We need all
documents consistent so we can make the correction with the **airline**. Proof of weighing below."*

## ⚠️ OCR correction (8→9 confusion)

The auto-OCR read the figure as **"348kg"** (80.1% confidence). Higher-fidelity re-OCR of the same image reads
**"349kg"**, and the **weigh ticket itself reads `349,000`** — so **349 kg** is correct. (Same class as the QR
date-misread pattern; the weigh ticket is the tie-breaker.)

## The weighing table (from the image)

| Field | Value |
|---|---|
| DOC. LIBERATÓRIO | **`DUE-26BR0017954000`** ← *apparent **DU-E** reference — see below* |
| AWB | **`04731753223`** |
| QT. VOLUME | **2** |
| PESO | **349,000** kg (gross) |
| CNPJ/CPF EXPORTADOR | **50.042.585/0001-80** — Black King ✓ |

## Reconciliation vs our documents

| | kg |
|---|---|
| Net (Rev 14 / NF-e nº 18) | **302,06** |
| **Our documented gross** (Rev 14 / NF-e nº 18) | **322,06** — 27 boxes, ~20 kg box tare, **pallet weight NOT included** |
| **Airport measument (gross)** | **349,00** |
| Divergence | **+26,94** |

**Explanation (CORRECTED 2026-10-02, same day).** An earlier draft of this note wrongly blamed pallet mass.
Reading `scripts/build_black_king_export_docs.py` shows the Rev-14 gross **already included the pallet tare**
(`tnet + 20` = 2 × 10 kg **plastic HDPE** pallets, non-wood / ISPM#15 N/A). What the model omitted was the
**CARTON tare**: 349,00 − 322,06 = **26,94 kg ≈ 1 kg × 27 boxes**.

So: **gross 349,00 = net 302,06 (product) + carton tare 26,94 (27 boxes) + pallet tare 20,00 (2 × 10 kg HDPE)**.
This is the Rev-15 model. **Confirm the ~1 kg/carton figure with SeaCoast** if they can break it out.

## What was asked of us

1. **Reissue the Commercial Invoice and Packing List with gross = 349 kg** (net 302,06 stays).
2. The forwarder then reissues **HAWB + MAWB** and corrects with the airline.

## ⚠️ Fiscal consequence — NF-e nº 18 states gross 322,06

NF-e nº 18 (issued 02/10/2026) declares **bruto 322,060 / líquido 302,060 / 2 pallets**. Reissuing commercial docs
at **349 kg** makes them **diverge from the issued NF-e**. Unlike adding/removing lines, a **CC-e CAN amend the
weight/freight fields** of an NF-e — so the correction route here is a **CC-e on nº 18** (fiscal) in addition to
the commercial reissue. **Confirm with Saymon/Matheus** — do NOT assume.

## Lane implication (needs confirmation)

The image is dated 2026-10-02 and shows **the cargo weighed at the airport** with a **DU-E-looking reference**
(`26BR0017954000`). If that is the **registered DU-E**, then the export processing (Phase 5) is **underway** —
which implies the **SISCOMEX habilitação was restored** (no habilitação ⇒ no DU-E). **This is NOT confirmed**;
ask Gary/Omega to confirm whether (a) the DU-E is registered and (b) Iolanda's habilitação update went through.
