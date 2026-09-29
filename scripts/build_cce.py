"""Generate the fiscal Carta de Correcao Eletronica (CC-e) content for NF-e n. 16.

The CC-e is a SEFAZ event filed against an ALREADY-ISSUED NF-e. It may only
complement/correct the "volumes of the merchandise" data that the issued NF-e
n. 16 left blank: its <transp> block carries only <modFrete>1</modFrete> (FOB),
with no transportadora, no <vol>, no pesoL / pesoB. That is exactly the detail
SeaCoast (Daniel) flagged and Black King's accountant asked to be supplied.

The event supplies, in the standard CC-e wording:
    - peso bruto / peso liquido
    - quantidade de caixas
    - quantidade de pallets

Values come from the Rev 12 SSOT (rows() in build_black_king_export_docs, the
same LINES table the invoice + packing list are generated from) plus the box
counts supplied by Gary (thread 10800, 2026-09-29).

Box packing rule (Gary, thread 10800, 2026-09-29): items whose commercial unit
is KG (bulk) ship in 10 kg boxes (Mercado Libre boxes, Matheus' warehouse);
items whose commercial unit is UN ship in their original boxes.

This CC-e content is RELAYED BY GARY to the accountant (Saymon / Jussileide,
WhatsApp group "Black King - Contab") -- they are NOT on Telegram. It is NOT a
commercial document and carries no signature: the EMITTER (Black King) files
the CC-e event electronically against NF-e n. 16.

Usage: python3 scripts/build_cce.py
Deps:  pip install weasyprint
"""

import sys
from pathlib import Path

from weasyprint import HTML

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_black_king_export_docs import CSS, rows


def ptn(x, nd=2):
    """Brazilian decimal separator: 364.06 -> 364,06."""
    return (
        f"{x:,.{nd}f}".replace(",", "\u00a0").replace(".", ",").replace("\u00a0", ".")
    )


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "exports"
OUT = OUTDIR / "2026-09-29_cc-e_black_king_nfe16_volumes_PT.pdf"

# --- NF-e n. 16 identification (issued 2026-09-22, cStat 100) -----------------
NFE_NUM = "16"
NFE_SERIE = "1"
NFE_CHAVE = "2926 0950 0425 8500 0180 5500 1000 0000 0161 3000 0003 5"

# --- Volumes (from the Rev 12 SSOT + Gary's box counts, thread 10800) ---------
PALLET_COUNT = 2
PALLET_TARE_KG = 20.0  # 2 x HDPE pallets @ 10 kg
BOXES = {
    1: 1,  # Cacao Nibs Kraft Pouch 8oz (UN, original box)
    2: 2,  # Cacao Husk (KG -> 10 kg boxes)
    3: 1,  # Cacao Mass Bar 500g (UN, original box)
    4: 8,  # Cacao Nibs (KG)
    5: 1,  # Cacao Almonds AGL8 (KG)
    6: 2,  # Cacao Tea AGL8 (KG)
    7: 1,  # Ceremonial Cacao Pouch 200g (UN, original box)
    8: 2,  # Cacao Almonds AGL13 (KG)
    9: 10,  # Cacao Nibs AGL13 (KG)
    10: 2,  # Cacao Tea AGL13 (KG)
    11: 1,  # Coopercabruca Cacao Butter (KG)
}


def doc_html():
    rs = rows()
    tnet = sum(r["net_kg"] for r in rs)
    tboxes = sum(BOXES.values())
    tgross = tnet + PALLET_TARE_KG

    k = "<h1>Carta de Corre&#231;&#227;o Eletr&#244;nica &#8212; CC-e</h1>"
    k += (
        f"<p class='sub'>Referente &#224; NF-e n&#186; {NFE_NUM}, s&#233;rie "
        f"{NFE_SERIE}, chave de acesso {NFE_CHAVE}.</p>"
    )
    k += (
        "<p>Por meio desta, ficam complementadas as informa&#231;&#245;es "
        "referentes aos volumes da mercadoria constantes na NF-e acima "
        "mencionada, conforme segue:</p>"
    )
    k += (
        "<table>"
        "<tr><th style='width:55%'>Descri&#231;&#227;o / Campo</th>"
        "<th>Valor</th></tr>"
        f"<tr><td>Peso bruto</td><td class='r'>{ptn(tgross)} kg</td></tr>"
        f"<tr><td>Peso l&#237;quido</td><td class='r'>{ptn(tnet)} kg</td></tr>"
        f"<tr><td>Quantidade de caixas</td><td class='r'>{tboxes}</td></tr>"
        f"<tr><td>Quantidade de pallets</td>"
        f"<td class='r'>{PALLET_COUNT}</td></tr>"
        "</table>"
    )
    k += (
        "<p>As informa&#231;&#245;es acima referem-se exclusivamente aos dados "
        "de peso e acondicionamento/volumes da mercadoria, permanecendo "
        "inalterados os demais dados e valores constantes na NF-e original.</p>"
    )

    # ---- Annex: per-line box breakdown (traceability for the emitter) --------
    k += (
        "<h2>Anexo &#8212; detalhamento por item / Annex &#8212; per-line "
        "detail</h2><table>"
        "<tr><th>#</th><th>Descri&#231;&#227;o</th>"
        "<th>Qtd. comercial</th><th>Caixas</th>"
        "<th>Peso l&#237;q. (kg)</th></tr>"
    )
    for r in rs:
        k += (
            f"<tr><td>{r['n']}</td><td>{r['pt']}</td>"
            f"<td class='r'>{r['qty']:g} {r['ucom']}</td>"
            f"<td class='r'>{BOXES.get(r['n'], 0)}</td>"
            f"<td class='r'>{ptn(r['net_kg'], 4)}</td></tr>"
        )
    k += (
        f"<tr><td></td><td><b>Total</b></td><td></td>"
        f"<td class='r'><b>{tboxes}</b></td>"
        f"<td class='r'><b>{ptn(tnet)}</b></td></tr>"
        "</table>"
    )
    k += (
        "<p class='note'>Regra de embalagem: itens com unidade comercial "
        "<b>KG</b> (granel) s&#227;o acondicionados em caixas de <b>10 kg</b> "
        "(caixas Mercado Livre); itens com unidade <b>UN</b> seguem nas "
        "<b>caixas originais</b>. O peso bruto acima inclui a tara dos "
        f"{PALLET_COUNT} pallets HDPE ({ptn(PALLET_TARE_KG)} kg) e <b>n&#227;o</b> "
        "inclui a tara das caixas. Emitente: Matheus Reis Pereira "
        "(Black King) &#8212; CNPJ 50.042.585/0001-80, IE 205055715.</p>"
    )
    return k


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{doc_html()}</body></html>"
    HTML(string=html).write_pdf(str(OUT))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
