# NF-e nº 16 — XML reconciliation (SeaCoast-requested)

> **Source artifact:** `brazil/sources/2026-09-22_black_king_nfe_16.xml` — the signed, SEFAZ-authorized `nfeProc` XML (versão 4.00).
> **Supplied by:** Gary, thread 10800, **2026-09-29**, in response to **SeaCoast Logistics'** request for the XML version of the NF-e.
> **Companion:** `brazil/sources/2026-09-22_black_king_nfe_16_danfe.pdf` (rendered DANFE).

## 1. Authorization (authoritative)

| Field | Value |
|-------|-------|
| Chave de acesso | `29260950042585000180550010000000161300000035` |
| Protocolo (nProt) | `129261913151752` |
| **cStat / xMotivo** | **100 — Autorizado o uso da NF-e** |
| dhRecbto | 2026-09-22T09:38:04-03:00 |
| verAplic | `SEFAZBA_NFENP_v7.0.5` |
| autXML (authorised to download the XML) | CNPJ `13.937.073/0001-56` = **BAHIA SECRETARIA DA FAZENDA** (SEFAZ Bahia) |

## 2. Identification

- nNF **16**, série **1**, model **55**, tpNF 1 (saída), idDest 3 (exterior), natOp **Exportacao**, tpAmb 1 (produção).
- `dhEmi` 2026-09-22T09:38:02-03:00.
- **Emitente:** MATHEUS REIS PEREIRA, CNPJ 50.042.585/0001-80, IE 205055715, CRT 1 (Simples Nacional) — address **Avenida Tancredo Neves, 4900** (the **legal / CNPJ** address, **not** the pickup warehouse at R. Cel. Paiva, 46).
- **Destinatário:** TRUETECH INC, país 2496 (EUA), UF **EX** (Exterior).
- **Exporta:** `UFSaidaPais` **BA**, `xLocExporta` **SALVADOR**.
- **Total:** vProd = vNF = **R$ 35.828,76**; ICMS / PIS / COFINS = 0 (isento / suspensão — export regime).

## 3. Line-by-line vs. Rev 12 packing list

| # | Item | NCM | uTrib | XML qTrib | XML kg | PL net kg | Δ kg | vProd (R$) |
|---|------|-----|-------|-----------|--------|-----------|------|------------|
| 1 | Cacao Nibs Kraft Pouch 8oz | 1801.00.00 | TON | 0,0290 | 29,00 | 29,2567 | −0,257 | 4.418,25 |
| 2 | Cacao Husk (KG) | 1803.10.00 | TON | 0,0200 | 20,00 | 20,0000 | 0,000 | 1.835,00 |
| 3 | Cacao Mass Bar 500g | 1803.10.00 | TON | 0,0180 | 18,00 | 18,5000 | −0,500 | 2.995,89 |
| 4 | Cacao Nibs (KG) | 1801.00.00 | TON | 0,0800 | 80,00 | 80,0000 | 0,000 | 10.158,40 |
| 5 | Cacao Almonds AGL8 | 1801.00.00 | TON | 0,0100 | 10,00 | 10,0000 | 0,000 | 0,50 |
| 6 | Cacao Tea AGL8 | 2106.90.00 | KG | 12,0000 | 12,00 | 12,0000 | 0,000 | 0,60 |
| 7 | Ceremonial Cacao Pouch 200g | 1803.10.00 | TON | 0,0340 | 34,00 | 33,8000 | +0,200 | 9.038,12 |
| 8 | Cacao Almonds AGL13 | 1801.00.00 | TON | 0,0150 | 15,00 | 15,0000 | 0,000 | 608,85 |
| 9 | Cacao Nibs AGL13 | 1801.00.00 | TON | 0,1000 | 100,00 | 99,5000 | +0,500 | 5.223,75 |
| 10 | Cacao Tea AGL13 | 2106.90.00 | KG | 21,0000 | 21,00 | 21,0000 | 0,000 | 1.102,50 |
| 11 | Coopercabruca Cacao Butter | 1804.00.00 | TON | 0,0050 | 5,00 | 5,0000 | 0,000 | 446,90 |
| **Σ** | | | | | **344,00** | **344,06** | **−0,06** | **35.828,76** |

All 11 lines, their **NCMs** and the **TON/KG uTrib remap** agree with the Rev 12 packing list. The fiscal sum **344,00 kg** differs from the PL commercial net **344,06 kg** only by a **60 g rounding artifact** (3-decimal TON on lines 1 / 3 / 7 / 9). The 2-HDPE-pallet **gross is 364,06 kg**.

## 4. ⭐ Transport block — EMPTY (why SeaCoast asked)

The XML's `<transp>` contains **only `<modFrete>1</modFrete>`**:

- **modFrete 1** = contratação do frete **por conta do destinatário** (**FOB**) — matches the PL Incoterm "FOB — freight paid by buyer".
- **No** `transportadora`, **no** `veicTransp`, **no** `vol` (volumes), **no** `pesoL` / `pesoB`.

This is the **same blank the DANFE left in TRANSPORTADOR / VOLUMES TRANSPORTADOS** — and exactly the gap the **ordem de coleta (REV 3)** fills:

> **2 paletes plásticos HDPE · líquido 344,06 kg · bruto 364,06 kg · espécie: 2 paletes HDPE (1000 × 1200 × 150 mm).**

The **XML + the ordem de coleta together give SeaCoast the complete customs + transport picture.**

## 5. Observations for the accountant (not blockers)

- **Lines 5 & 6** carry near-nominal values (R$ 0,05/kg; ≈22 kg together valued at **R$ 1,10**). Presumably a sample / placeholder allocation — flagged to Saymon / Matheus, **not** a SeaCoast matter. The **total** vNF R$ 35.828,76 is unchanged.
- **CFOP 7102** (revenda) on all lines — consistent with runbook Appendix A (7101 produção própria / 7102 revenda).
- **Line 2** (Cacao Husk) is declared under **NCM 1803.10.00** (→ TON); note husk is often classified 1802 (→ KG per Appendix E). Declared as-is by the accountant; recorded for traceability only.
