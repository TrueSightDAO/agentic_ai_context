#!/usr/bin/env python3
"""Generate the commercial Correction Letter for the Black King export docs.

SeaCoast Logistics (freight forwarder) flagged that the invoice went out
without the packing detail - weights, quantities and package types. This letter
supplies that detail, quoted from the SAME single source of truth as the issued
Rev 12 invoice + packing list: it imports rows()/f2/f4/CSS from
build_black_king_export_docs, so every figure reconciles line by line.

It is a COMMERCIAL correction (Carta de Correcao Comercial). It is NOT a fiscal
Carta de Correcao Eletronica (CC-e): no NF-e has been issued for this shipment
(lane status, see brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md).

It carries a full Portuguese section so the Brazilian reader (warehouse /
carrier) knows exactly WHERE to collect and WHAT is to be collected.

Usage: python3 scripts/build_correction_letter.py
Deps:  pip install weasyprint
"""

import sys
from pathlib import Path

from weasyprint import HTML

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_black_king_export_docs import CSS, f2, f4, rows

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "exports"
OUT = OUTDIR / "2026-09-29_correction_letter_black_king_inv_rev12_EN_PT.pdf"

EXPORTER = (
    "Black King - Matheus Reis Pereira (CNPJ 50.042.585/0001-80), "
    "Av. Tancredo Neves, 4900, Qd H, Cs 9, Ilheus, BA, 45655-650, Brazil"
)
IMPORTER = "TrueTech Inc - EIN 88-3411514, 1423 Hayes St, San Francisco, CA 94117, USA"

# Physical pickup address (warehouse) - distinct from the registered (CNPJ)
# address above; see runbook section 2a.
PICKUP_PT = "R. Cel. Paiva, 46 - Centro, Ilheus - BA, 45653-310"
DEST_PT = (
    "Aeroporto de Salvador (SSA) - terminal de carga aerea (TECA), "
    "Praca Gago Coutinho, Sao Cristovao, Salvador - BA"
)

# Package type per line (commercial unit).
PACK = {
    1: "Kraft pouch 8 oz, in carton / Sache kraft 8 oz, em caixa",
    2: "Sealed bag (bulk) / Saco selado (granel)",
    3: "Wrapped bar 500 g, in carton / Barra embrulhada 500 g, em caixa",
    4: "Sealed bag (bulk) / Saco selado (granel)",
    5: "Sealed bag (bulk) / Saco selado (granel)",
    6: "Sealed bag (bulk) / Saco selado (granel)",
    7: "Retail pouch 200 g, in carton / Sache 200 g, em caixa",
    8: "Sealed bag (bulk) / Saco selado (granel)",
    9: "Sealed bag (bulk) / Saco selado (granel)",
    10: "Sealed bag (bulk) / Saco selado (granel)",
    11: "Sealed bag (bulk) / Saco selado (granel)",
}
PACK_PT = {
    1: "Sache kraft 8 oz, em caixa",
    2: "Saco lacrado (granel)",
    3: "Barra embrulhada 500 g, em caixa",
    4: "Saco lacrado (granel)",
    5: "Saco lacrado (granel)",
    6: "Saco lacrado (granel)",
    7: "Sache varejo 200 g, em caixa",
    8: "Saco lacrado (granel)",
    9: "Saco lacrado (granel)",
    10: "Saco lacrado (granel)",
    11: "Saco lacrado (granel)",
}


def letter_html():
    rs = rows()
    tnet = sum(r["net_kg"] for r in rs)
    k = (
        "<h1>Correction Letter / Carta de Correcao (Comercial)</h1>"
        "<p class='sub'>Commercial document correction - NOT a fiscal CC-e. "
        "Rev 12 / 2026-09-29.</p>"
        "<h2>Parties / Partes</h2><table>"
        "<tr><th style='width:30%'>Field / Campo</th>"
        "<th>Value / Valor</th></tr>"
        f"<tr><td>Exporter / Exportador</td><td>{EXPORTER}</td></tr>"
        f"<tr><td>Importer / Importador</td><td>{IMPORTER}</td></tr>"
        "<tr><td>Invoice / Fatura</td><td>INV-2026-0611-001 (Rev 12), "
        "2026-09-21</td></tr>"
        "<tr><td>Packing list / Lista de embalagem</td>"
        "<td>PL-2026-0611-001 (Rev 12)</td></tr>"
        "<tr><td>Route / Rota</td><td>SSA (Salvador) -> SFO (San Francisco), "
        "air / aereo</td></tr></table>"
    )
    k += (
        "<h2>Correction / Correcao</h2>"
        "<p>The commercial invoice referenced above was issued <b>without the "
        "packing detail</b>. This letter supplies - and, where needed, corrects "
        "- the following, consistent with the accompanying packing list "
        "(Rev 12):</p><ul>"
        f"<li><b>Weights / Pesos:</b> net <b>{f2(tnet)} kg</b> / liquido; "
        f"gross <b>{f2(tnet + 20)} kg</b> / bruto (includes 20 kg pallet "
        "tare).</li>"
        "<li><b>Quantities &amp; package types / Quantidades e embalagens:</b> "
        "see the annex table below.</li>"
        "<li><b>Outer packaging / Embalagem externa:</b> 2 plastic HDPE "
        "pallets, 1000 x 1200 x 150 mm, tare 10 kg each / 2 paletes de HDPE, "
        "tara 10 kg cada.</li></ul>"
        "<p class='note'>This letter corrects <b>commercial-document "
        "content only</b>: it does not change the invoice value, the parties, "
        "or the nature of the goods. Because <b>no NF-e has been issued</b> "
        "for this shipment, no fiscal Carta de Correcao Eletronica (CC-e) "
        "applies.</p>"
    )
    k += (
        "<h2>Annex - packing detail / Anexo - detalhe da embalagem</h2><table>"
        "<tr><th>#</th><th>Description / Descricao</th>"
        "<th>Qty (commercial) / Qtd</th>"
        "<th>Package type / Embalagem</th>"
        "<th>Net kg / Liq.</th></tr>"
    )
    for r in rs:
        k += (
            f"<tr><td>{r['n']}</td><td>{r['en']} / {r['pt']}</td>"
            f"<td class='r'>{r['qty']:g} {r['ucom']}</td>"
            f"<td>{PACK.get(r['n'], '-')}</td>"
            f"<td class='r'>{f4(r['net_kg'])}</td></tr>"
        )
    k += "</table>"
    k += (
        "<h2>Totals / Totais</h2><table>"
        "<tr><th style='width:40%'>Field / Campo</th>"
        "<th>Value / Valor</th></tr>"
        f"<tr><td>Lines / Linhas</td><td>{len(rs)}</td></tr>"
        f"<tr><td>Net weight / Peso liquido</td><td>{f2(tnet)} kg</td></tr>"
        f"<tr><td>Gross weight / Peso bruto</td>"
        f"<td>{f2(tnet + 20)} kg</td></tr>"
        "<tr><td>Packages / Volumes</td><td>2 pallets (HDPE)</td></tr>"
        "</table>"
    )
    # ---- Portuguese pickup section (for the Brazilian warehouse / carrier) ----
    k += (
        "<h2>Se\u00e7\u00e3o em Portugu\u00eas \u2014 Instru\u00e7\u00f5es de Coleta</h2>"
        "<p>Esta se\u00e7\u00e3o \u00e9 para o leitor no Brasil (armaz\u00e9m / "
        "transportadora) e informa exatamente <b>onde coletar</b> e "
        "<b>o que ser\u00e1 coletado</b>.</p>"
        "<h3>1. Onde coletar / local de coleta</h3>"
        f"<p><b>{PICKUP_PT}</b> (armaz\u00e9m f\u00edsico / dep\u00f3sito). "
        "Este \u00e9 o ponto de retirada da carga.</p>"
        "<p>Contatos no local: Rebecca \u2014 +55 73 99108-2946; "
        "Matheus Reis (Black King) \u2014 +55 11 91413-5328 / "
        "+55 73 99109-0002.</p>"
        f"<p><b>Destino:</b> {DEST_PT}. "
        "Modalidade: exporta\u00e7\u00e3o a\u00e9rea SSA \u2192 SFO.</p>"
        "<h3>2. O que ser\u00e1 coletado / itens</h3>"
        "<table><tr><th>#</th><th>Descri\u00e7\u00e3o</th><th>Quantidade</th>"
        "<th>Embalagem</th><th>Peso l\u00edq. (kg)</th></tr>"
    )
    for r in rs:
        k += (
            f"<tr><td>{r['n']}</td><td>{r['pt']}</td>"
            f"<td class='r'>{r['qty']:g} {r['ucom']}</td>"
            f"<td>{PACK_PT.get(r['n'], 'A granel (kg)')}</td>"
            f"<td class='r'>{f4(r['net_kg'])}</td></tr>"
        )
    k += (
        "</table>"
        "<h3>3. Volumes e pesos</h3><table>"
        "<tr><th style='width:45%'>Item</th><th>Valor</th></tr>"
        "<tr><td>Volumes / paletes</td><td>2 paletes pl\u00e1sticos HDPE "
        "(1000 \u00d7 1200 \u00d7 150 mm)</td></tr>"
        f"<tr><td>Peso l\u00edquido</td><td>{f2(tnet)} kg</td></tr>"
        "<tr><td>Peso bruto (inclui 20 kg de tara)</td>"
        f"<td>{f2(tnet + 20)} kg</td></tr></table>"
        "<p><b>Observa\u00e7\u00e3o:</b> a NF-e de exporta\u00e7\u00e3o ainda "
        "<b>n\u00e3o foi emitida</b>. O transporte rodovi\u00e1rio deve portar a "
        "NF-e; a emiss\u00e3o est\u00e1 pendente de aprova\u00e7\u00e3o.</p>"
    )
    k += (
        "<p>Sincerely / Atenciosamente,</p>"
        "<p style='margin-top:1.6cm'>"
        "___________________________________<br>"
        "Black King - Matheus Reis Pereira<br>"
        "CNPJ 50.042.585/0001-80<br>"
        "Date / Data: ______</p>"
        "<p class='sub'>Prepared by TrueSight DAO on behalf of the exporter. "
        "Figures quoted from the Rev 12 invoice + packing list (shared "
        "source-of-truth). To be signed by Black King before submission.</p>"
    )
    return k


def main():
    OUTDIR.mkdir(exist_ok=True)
    html = (
        '<html><head><meta charset="utf-8"><style>'
        f"{CSS}</style></head><body>{letter_html()}</body></html>"
    )
    HTML(string=html).write_pdf(OUT)
    print("built:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
