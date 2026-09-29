#!/usr/bin/env python3
"""Generate the Black King ORDEM DE COLETA (cargo pickup order) for the
Ilheus -> Salvador (SSA) road leg of the Brazil -> SF export lane.

The order is composed from the SAME single source of truth as the issued
export documents: it imports LINES / UTRIB / rows() / CSS from
build_black_king_export_docs, so every quantity reconciles line-by-line with
the Rev 12 packing list. The merchandise block is stated in the COMMERCIAL
units of the issued packing list (the "units" version); the fiscal NF-e layer
(uTrib TON / KG) is declared separately on the Rev 12 invoice + packing list.

Usage: python3 scripts/build_order_de_coleta.py
Deps:  pip install weasyprint
"""

import sys
from pathlib import Path

from weasyprint import HTML

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_black_king_export_docs import CSS, f2, f4, rows

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "exports"
OUT = OUTDIR / "2026-09-29_ordem_de_coleta_black_king_ilheus_ssa.pdf"

ORDER = {
    "issuer": "OMEGA (Grupo Omega) - Salvador",
    "issuer_cnpj": "01.568.962/0001-04",
    "issuer_ie": "045415317",
    "issuer_addr": "Rua Sao Francisco, 10, Valeria, Salvador - BA",
    "modal": "EXP AEREA / Air export - SSA (Salvador) -> SFO (San Francisco)",
    "remetente": "MATHEUS REIS PEREIRA (Black King) - CNPJ 50.042.585/0001-80",
    "remetente_addr": "R. Cel. Paiva, 46, Centro, Ilheus - BA, 45653-310",
    "destinatario": (
        "EMP. BRASILEIRA DE INFRAESTRUTURA AEROPORTUARIA (INFRAERO) - "
        "CNPJ 00.352.294/0015-16 - ISENTO"
    ),
    "destinatario_addr": "Praca Gago Coutinho, Sao Cristovao, Salvador - BA",
    "consignatario": "CNPJ 50.042.585/0001-80 - MATHEUS REIS PEREIRA",
}

# Packaging label per line (commercial unit) for the order's Embalagem column.
EMB = {
    1: "Pouch kraft 8 oz / Sache kraft 8 oz",
    3: "Bar 500 g / Barra 500 g",
    7: "Pouch 200 g / Sache 200 g",
}


def order_html():
    rs = rows()
    tnet = sum(r["net_kg"] for r in rs)
    tusd = sum(r["usd"] for r in rs)
    k = (
        "<h1>ORDEM DE COLETA DE CARGAS / Cargo Pickup Order</h1>"
        "<p class='sub'>Prepared from Packing List PL-2026-0611-001 (Rev 12, "
        "commercial units). To be issued by Omega. No. ______ (a emitir) - "
        "2026-09-29.</p>"
    )
    k += (
        "<h2>Partes / Parties</h2><table>"
        "<tr><th style='width:30%'>Campo / Field</th>"
        "<th>Valor / Value</th></tr>"
        f"<tr><td>Emissor / Issuer</td><td>{ORDER['issuer']} - CNPJ "
        f"{ORDER['issuer_cnpj']} - IE {ORDER['issuer_ie']} - "
        f"{ORDER['issuer_addr']}</td></tr>"
        f"<tr><td>Modalidade / Mode</td><td>{ORDER['modal']}</td></tr>"
        f"<tr><td>Remetente / Sender</td><td>{ORDER['remetente']} - "
        f"{ORDER['remetente_addr']}</td></tr>"
        f"<tr><td>Destinatario / Airport consignee</td><td>"
        f"{ORDER['destinatario']} - {ORDER['destinatario_addr']}</td></tr>"
        f"<tr><td>Consignatario / Notify</td><td>{ORDER['consignatario']}"
        "</td></tr></table>"
    )
    k += (
        "<h2>MERCADORIA / Merchandise - commercial units (Rev 12)</h2>"
        "<p class='note'>Contents, volumes and packaging per the issued "
        "packing list (commercial units); net kg from documented pack sizes. "
        "The fiscal NF-e layer is declared separately in TON / KG - see the "
        "Rev 12 packing list &amp; invoice.</p><table>"
        "<tr><th>#</th><th>Conteudo / Contents</th><th>Vol(s)</th>"
        "<th>Embalagem / Packaging</th><th>Peso liq. (kg)</th>"
        "<th>Nota Fiscal</th><th>Valor USD</th></tr>"
    )
    for r in rs:
        emb = EMB.get(r["n"], "Granel / Bulk (kg)")
        k += (
            f"<tr><td>{r['n']}</td><td>{r['en']} / {r['pt']}</td>"
            f"<td class='r'>{r['qty']:g} {r['ucom']}</td>"
            f"<td>{emb}</td><td class='r'>{f4(r['net_kg'])}</td>"
            "<td>[NF-e a emitir]</td>"
            f"<td class='r'>{f2(r['usd'])}</td></tr>"
        )
    k += "</table>"
    k += (
        "<h2>Volumes &amp; pesos / Volumes &amp; weights</h2><table>"
        "<tr><th style='width:40%'>Campo / Field</th>"
        "<th>Valor / Value</th></tr>"
        f"<tr><td>Linhas / Lines</td><td>{len(rs)}</td></tr>"
        "<tr><td>Volumes / Pallets</td><td>2 plastic HDPE pallets "
        "(1000 x 1200 x 150 mm)</td></tr>"
        f"<tr><td>Peso liquido / Net weight</td><td>{f2(tnet)} kg</td></tr>"
        f"<tr><td>Peso bruto / Gross weight (+20 kg tare)</td>"
        f"<td>{f2(tnet + 20)} kg</td></tr>"
        f"<tr><td>Valor declarado / Declared value</td>"
        f"<td>{f2(tusd)} USD</td></tr></table>"
    )
    k += (
        "<h2>Observacoes / Notes</h2><ul>"
        "<li><b>Endereco de coleta / Pickup address:</b> R. Cel. Paiva, 46, "
        "Centro, Ilheus - BA, 45653-310 (armazem fisico / physical warehouse). "
        "Confirmar com a Omega: a ordem n. 003625 listava a Av. Tancredo "
        "Neves, 4900 (endereco registrado), nao o armazem fisico.</li>"
        "<li><b>Nota Fiscal:</b> a NF-e de exportacao (modelo 55) ainda "
        "<b>nao foi emitida</b>; a coluna fica em branco e o transporte "
        "rodoviario deve portar a NF-e. Emissao pendente de aprovacao do Gary "
        "(gate 0.2).</li>"
        "<li><b>TECA do aeroporto:</b> confirmar se o terminal de carga de "
        "Salvador e operado pela INFRAERO ou pela concessionaria CASSA/Vinci "
        "(concessao 2017).</li>"
        "<li><b>Transporte:</b> campos de motorista / cavalo / carreta / CNH "
        "a preencher pela Omega na emissao.</li></ul>"
    )
    return k


def main():
    OUTDIR.mkdir(exist_ok=True)
    html = (
        '<html><head><meta charset="utf-8"><style>'
        f"{CSS}</style></head><body>{order_html()}</body></html>"
    )
    HTML(string=html).write_pdf(OUT)
    print("built:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
