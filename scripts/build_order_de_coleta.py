#!/usr/bin/env python3
"""Generate the Black King ORDEM DE COLETA (cargo pickup order) for the
Ilheus -> Salvador (SSA) road leg of the Brazil -> SF export lane.

REV 3 (2026-09-29): Gary Teh (+1 442 340-5782, WhatsApp) added as the
PRIMARY on-site pickup contact (on site at the warehouse, ready for the driver
on 30/09/2026); the driver must call/WhatsApp him on arrival.

REV 2 (2026-09-29): now keyed to the ISSUED export NF-e n. 16 (serie 1,
2026-09-22). The order carries the NF-e identification block (chave de acesso,
protocolo, emitente IE/CNPJ, natureza, total) and a fiscal uTrib column beside
the commercial units, so the trucking service can reconcile the physical cargo
against the document the driver must carry. It also FILLS the TRANSPORTADOR /
VOLUMES block that the DANFE left blank (quantidade, especie, peso bruto, peso
liquido) - the exact fields SeaCoast flagged.

Composed from the SAME single source of truth as the issued export documents: it
imports LINES / UTRIB / rows() / CSS from build_black_king_export_docs, so every
quantity reconciles line-by-line with the Rev 12 packing list.

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

# --- Issued export NF-e n. 16 (black King / Matheus) - see runbook 5.3 ---
NFE = {
    "numero": "16",
    "serie": "1",
    "emitida": "22/09/2026",
    "chave": "2926 0950 0425 8500 0180 5500 1000 0000 0161 3000 0003 5",
    "chave_raw": "29260950042585000180550010000000161300000035",
    "protocolo": "129261913151752",
    "natureza": "Exportacao / Export",
    "emitente": "MATHEUS REIS PEREIRA (Black King)",
    "emitente_cnpj": "50.042.585/0001-80",
    "emitente_ie": "205055715",
    "emitente_addr": (
        "Av. Tancredo Neves, 4900, Nossa Senhora da Vitoria, Ilheus - BA, 45655-650"
    ),
    "destinatario": "TRUETECH INC",
    "destinatario_addr": (
        "1423 Hayes St, Hayes Valley, San Francisco CA 94117, USA "
        "(municipio Exterior / UF EX)"
    ),
    "total_brl": "R$ 35.828,76",
    "cfop": "7102",
}

ORDER = {
    "issuer": "OMEGA (Grupo Omega) - Salvador",
    "issuer_cnpj": "01.568.962/0001-04",
    "issuer_ie": "045415317",
    "issuer_addr": "Rua Sao Francisco, 10, Valeria, Salvador - BA",
    "modal": "EXP AEREA / Air export - SSA (Salvador) -> SFO (San Francisco)",
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

# On-site contacts at the pickup warehouse.
# First entry is the PRIMARY contact the driver must call/WhatsApp on arrival.
CONTACTS = [
    ("Gary Teh (TrueSight DAO)", "+1 (442) 340-5782 (WhatsApp)"),
    ("Rebecca", "+55 73 99108-2946"),
    ("Matheus Reis", "+55 11 91413-5328 / +55 73 99109-0002"),
]


def f3(x):
    """3-decimal grouping (fiscal TON quantities)."""
    return f"{x:,.3f}"


def fiscal_unit(r):
    """Fiscal unit of measure for the NF-e line.

    The SSOT's UTRIB map only keys Chapter-18 NCM prefixes; NCM 2106.90.00
    (Cacao Tea, lines 6 and 10) is outside it (u is None) and is declared in
    KG - confirmed on the issued DANFE (KG 12,000 / KG 21,000).
    """
    return r["u"] or "KG"


def order_html():
    rs = rows()
    tnet = sum(r["net_kg"] for r in rs)
    tgross = tnet + 20.0  # 2 HDPE pallets @ 10 kg tare
    tusd = sum(r["usd"] for r in rs)

    k = (
        "<h1>ORDEM DE COLETA DE CARGAS / Cargo Pickup Order</h1>"
        "<p class='sub'>REV 3 - referenciada a NF-e n. 16 (serie 1) emitida em "
        "22/09/2026. Prepared from Packing List PL-2026-0611-001 (Rev 12). "
        "To be issued by Omega. No. ______ (a emitir) - 2026-09-29. "
        "Contato principal na coleta: Gary Teh (WhatsApp) - ver secao 2.</p>"
    )

    # 1. NF-e identification
    k += (
        "<h2>1. Identificacao da NF-e / NF-e identification</h2><table>"
        "<tr><th style='width:34%'>Campo / Field</th><th>Valor / Value</th></tr>"
        f"<tr><td>Nota Fiscal / NF-e</td><td><b>n. {NFE['numero']}, serie "
        f"{NFE['serie']}</b> - emitida {NFE['emitida']}</td></tr>"
        f"<tr><td>Chave de acesso</td><td><b>{NFE['chave']}</b> "
        f"(44 digitos)</td></tr>"
        f"<tr><td>Protocolo de autorizacao</td><td>{NFE['protocolo']}</td></tr>"
        f"<tr><td>Natureza da operacao</td><td>{NFE['natureza']} - CFOP "
        f"{NFE['cfop']}</td></tr>"
        f"<tr><td>Emitente</td><td>{NFE['emitente']} - CNPJ "
        f"{NFE['emitente_cnpj']} - IE {NFE['emitente_ie']}<br>"
        f"{NFE['emitente_addr']}</td></tr>"
        f"<tr><td>Destinatario</td><td>{NFE['destinatario']}<br>"
        f"{NFE['destinatario_addr']}</td></tr>"
        f"<tr><td>Valor total da NF-e</td><td><b>{NFE['total_brl']}</b> "
        "(US$ 6.946,85 @ PTAX 5,1575)</td></tr>"
        "<!--nf-e-id--></table>"
    )

    # 2. Where to collect
    primary = CONTACTS[0]
    others = " - ".join(f"{n} {p}" for n, p in CONTACTS[1:])
    k += (
        "<h2>2. Onde coletar / Where to collect</h2><table>"
        "<tr><th style='width:34%'>Campo / Field</th><th>Valor / Value</th></tr>"
        f"<tr><td>Local de coleta</td><td><b>R. Cel. Paiva, 46, Centro, "
        "Ilheus - BA, 45653-310</b> (armazem fisico / physical "
        "warehouse)</td></tr>"
        "<tr><td><b>Contato principal na coleta / Main pickup contact</b>"
        "<br>(presente no armazem / on site from 30/09/2026)</td>"
        f"<td><b>{primary[0]}</b><br><b>{primary[1]}</b></td></tr>"
        "<tr><td>Outros contatos no local / Other on-site contacts</td>"
        f"<td>{others}</td></tr>"
        f"<tr><td>Remetente / Sender</td><td>{NFE['emitente']} - CNPJ "
        f"{NFE['emitente_cnpj']}</td></tr>"
        "</table>"
        "<p class='note'><b>O motorista deve ligar/WhatsApp para o contato "
        "principal ao chegar ao armazem.</b> Confirmar com a Omega: a ordem "
        "n. 003625 listava a Av. Tancredo Neves, 4900 (endereco registrado), "
        "<b>nao</b> o armazem fisico de coleta em Cel. Paiva, 46.</p>"
    )

    # 3. What will be collected - the driver's manifest
    k += (
        "<h2>3. O que sera coletado / What will be collected</h2>"
        "<p class='note'>Mercadoria em unidades comerciais; a coluna fiscal "
        "reproduz as quantidades de tributacao (uTrib) declaradas na NF-e n. 16 "
        "para conferencia. Confira cada linha antes de carregar.</p><table>"
        "<tr><th>#</th><th>Conteudo / Contents</th><th>Qtd. comercial</th>"
        "<th>Embalagem / Packaging</th><th>Peso liq. (kg)</th>"
        "<th>NF-e qtd. (uTrib)</th></tr>"
    )
    for r in rs:
        emb = EMB.get(r["n"], "Granel / Bulk (kg)")
        k += (
            f"<tr><td>{r['n']}</td><td>{r['en']} / {r['pt']}</td>"
            f"<td class='r'>{r['qty']:g} {r['ucom']}</td>"
            f"<td>{emb}</td><td class='r'>{f4(r['net_kg'])}</td>"
            f"<td class='r'>{f3(r['trib_qty'])} {fiscal_unit(r)}</td></tr>"
        )
    k += (
        f"<tr><td colspan='4' class='r'><b>Total ({len(rs)} linhas)</b></td>"
        f"<td class='r'><b>{f2(tnet)}</b></td><td class='r'></td></tr></table>"
    )

    # 4. Volumes & weights for the transport document (DANFE block left blank)
    k += (
        "<h2>4. Volumes e pesos para o transporte / Volumes &amp; weights</h2>"
        "<p class='note'>Bloco TRANSPORTADOR / VOLUMES TRANSPORTADOS da DANFE "
        "(quantidade, especie, peso bruto, peso liquido) - preencher no "
        "transporte.</p><table>"
        "<tr><th style='width:40%'>Campo / Field</th>"
        "<th>Valor / Value</th></tr>"
        "<tr><td>Quantidade de volumes</td><td><b>2</b></td></tr>"
        "<tr><td>Especie</td><td>2 paletes plasticos HDPE "
        "(1000 x 1200 x 150 mm)</td></tr>"
        f"<tr><td>Peso liquido total</td><td><b>{f2(tnet)} kg</b></td></tr>"
        f"<tr><td>Peso bruto total (inclui 20 kg de tara)</td>"
        f"<td><b>{f2(tgross)} kg</b></td></tr>"
        f"<tr><td>Valor declarado</td><td>{f2(tusd)} USD</td></tr>"
        "</table>"
    )

    # 5. Destination
    k += (
        "<h2>5. Destino / Destination</h2><table>"
        "<tr><th style='width:34%'>Campo / Field</th><th>Valor / Value</th></tr>"
        f"<tr><td>Modalidade</td><td>{ORDER['modal']}</td></tr>"
        f"<tr><td>Consignatario no aeroporto</td><td>{ORDER['destinatario']}"
        f"<br>{ORDER['destinatario_addr']}</td></tr>"
        f"<tr><td>Notify / Consignatario</td><td>{ORDER['consignatario']}"
        "</td></tr>"
        f"<tr><td>Emissor da ordem</td><td>{ORDER['issuer']} - CNPJ "
        f"{ORDER['issuer_cnpj']} - IE {ORDER['issuer_ie']} - "
        f"{ORDER['issuer_addr']}</td></tr>"
        "</table>"
    )

    # 6. Fiscal document + driver fields
    k += (
        "<h2>6. Documento fiscal / Fiscal document</h2><ul>"
        "<li><b>NF-e n. 16 obrigatoria:</b> o transporte rodoviario deve portar "
        f"a NF-e n. {NFE['numero']}, serie {NFE['serie']}, chave "
        f"{NFE['chave_raw']}.</li>"
        "<li><b>TECA do aeroporto:</b> confirmar se o terminal de carga de "
        "Salvador e operado pela INFRAERO ou pela concessionaria "
        "CASSA/Vinci.</li>"
        "<li><b>Transporte:</b> campos de motorista / cavalo / carreta / CNH a "
        "preencher pela Omega na emissao.</li>"
        "</ul>"
    )

    # 7. Observations
    k += (
        "<h2>7. Observacoes / Notes</h2><ul>"
        "<li><b>Endereco de coleta:</b> R. Cel. Paiva, 46, Centro, Ilheus - BA, "
        "45653-310 (armazem fisico). Nao coletar na Av. Tancredo Neves, 4900 "
        "(endereco apenas registrado).</li>"
        "<li><b>Pesos:</b> pesos liquidos por linha conforme PL-2026-0611-001 "
        "Rev 12; o peso bruto inclui 20 kg de tara dos 2 paletes.</li>"
        "<li><b>Quantidades:</b> em unidades comerciais (UN / KG) para "
        "conferencia fisica; quantidades fiscais em TON / KG conforme a NF-e "
        "n. 16.</li>"
        "</ul>"
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
