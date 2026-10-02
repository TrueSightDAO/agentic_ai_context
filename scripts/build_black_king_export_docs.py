#!/usr/bin/env python3
"""Generate the Black King -> TrueTech export commercial invoice + packing list.

Rev 13 (2026-10-02): the physical cargo changed. Rev-12 lines 6 (Cacao Tea
AGL8) and 8 (Cacao Almonds AGL13) are NOT in the shipment; one new nominal
line was added for 5 kg of Para cacao-almond samples. Result: 10 lines,
28 boxes (23 regular + 5 irregular), 322.06 kg net / 342.06 kg gross.
The NCM -> uTrib unit remap introduced in Rev 12 is unchanged.

Rev 12 applies the NCM -> export uTrib (tributary unit of measure) norm cited by
Saymon (Black King's accountant): on EXPORT, Chapter-18 raw / intermediate cocoa
headings 1801 (beans/nibs), 1803 (paste/mass) and 1804 (butter/fat) MUST be
declared in TON (tonelada metrica liquida); 1802 (husks) and 1806 (preparations)
use KG. Rev 11 declared the 1801 / 1803 / 1804 lines in mixed UN / KG, which is
the units-of-measure error the NF-e emitter rejected.

Layout: the PRIMARY line-item table is now stated in the mandated units of
measure (uTrib), because that is what the norm governs and what the NF-e
validates. The commercial units (uCom) are retained as a traceability reference
so the two revisions can be reconciled line by line. USD / BRL values and totals
are unchanged from Rev 11.

Usage: python3 scripts/build_black_king_export_docs.py
Deps:  pip install weasyprint
"""

from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "exports"

PTAX = 5.1575  # BACEN PTAX venda 18/09/2026
OZ = 0.028349523125  # kg per avoirdupois ounce

# n, ncm, qty, ucom, pack_kg (kg per commercial unit), usd_total, en, pt
LINES = [
    (
        1,
        "1801.00.00",
        129,
        "UN",
        8 * OZ,
        856.56,
        "Cacao Nibs Kraft Pouch 8oz - Ilheus 2024",
        "Nibs de Cacau - Sache Kraft 8oz - Ilheus 2024",
    ),
    (
        2,
        "1803.10.00",
        20,
        "KG",
        1.0,
        355.71,
        "Cacao Husk (KG) - Ilheus, Brazil",
        "Casca de Cacau (KG) - Ilheus, Brasil",
    ),
    (
        3,
        "1803.10.00",
        37,
        "UN",
        0.5,
        580.9,
        "Cacao Mass Bar 500g - Ilheus 2024",
        "Barra de Massa de Cacau 500g - Ilheus 2024",
    ),
    (
        4,
        "1801.00.00",
        80,
        "KG",
        1.0,
        1969.48,
        "Cacao Nibs (KG) - Ilheus 2024",
        "Nibs de Cacau (KG) - Ilheus 2024",
    ),
    (
        5,
        "1801.00.00",
        10,
        "KG",
        1.0,
        0.1,
        "Cacao Almonds (KG) - AGL8",
        "Amendoas de Cacau (KG) - AGL8",
    ),
    (
        6,
        "1803.10.00",
        169,
        "UN",
        0.2,
        1752.53,
        "Ceremonial Cacao Pouch 200g - AGL8",
        "Sache de Cacau Cerimonial 200g - AGL8",
    ),
    (
        7,
        "1801.00.00",
        99.5,
        "KG",
        1.0,
        1012.91,
        "Cacao Nibs (KG) - AGL13",
        "Nibs de Cacau (KG) - AGL13",
    ),
    (
        8,
        "2106.90.00",
        21,
        "KG",
        1.0,
        213.83,
        "Cacao Tea (KG) - AGL13",
        "Cha de Cacau (KG) - AGL13",
    ),
    (
        9,
        "1804.00.00",
        5,
        "KG",
        1.0,
        86.66,
        "Coopercabruca Cacao Butter (KG)",
        "Manteiga de Cacau Coopercabruca (KG)",
    ),
    (
        10,
        "1801.00.00",
        5,
        "KG",
        1.0,
        0.05,
        "Cacao Almonds samples (KG) - Para",
        "Amendoas de Cacau amostras (KG) - Para",
    ),
]

# Rev-13 line -> Rev-12 line reference (reconciliation with NF-e no. 16).
REV12_REF = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 9, 8: 10, 9: 11, 10: "new"}

# Boxes per Rev-13 line: (regular, irregular). Regular = 10 kg Mercado Livre
# boxes; irregular = original retail / non-standard boxes.
BOXES = {
    1: (0, 1),
    2: (2, 0),
    3: (0, 1),
    4: (8, 0),
    5: (0, 1),
    6: (0, 1),
    7: (10, 0),
    8: (2, 0),
    9: (0, 1),
    10: (1, 0),
}

# NCM -> export uTrib, per the norm table (Gary, 2026-09-21).
UTRIB = {
    "1801": "TON",
    "1802": "KG",
    "1803": "TON",
    "1804": "TON",
    "1805": "TON",
    "1806": "KG",
}


def rows():
    """Return one dict per invoice line with all derived quantities/values."""
    out = []
    for n, ncm, qty, ucom, pk, usd, en, pt in LINES:
        net_kg = qty * pk
        u = UTRIB.get(ncm[:4])
        trib_qty = net_kg / 1000.0 if u == "TON" else net_kg
        uval = usd / trib_qty if trib_qty else 0.0
        out.append(
            {
                "n": n,
                "ncm": ncm,
                "qty": qty,
                "ucom": ucom,
                "pk": pk,
                "usd": usd,
                "en": en,
                "pt": pt,
                "net_kg": net_kg,
                "u": u,
                "trib_qty": trib_qty,
                "uval": uval,
                "brl": usd * PTAX,
            }
        )
    return out


def f2(x):
    return f"{x:,.2f}"


def f4(x):
    return f"{x:,.4f}"


def f6(x):
    return f"{x:,.6f}"


def head(title, doc):
    return (
        f"<h1>{title}</h1><p class='sub'>{doc}</p>"
        "<p class='sub'>Rev 13 - 2026-10-02. Units of measure per the NCM "
        "to export-uTrib norm (Appendix E). Supersedes Rev 12.</p>"
        "<h2>Parties / Partes</h2><table>"
        "<tr><th style='width:30%'>Field / Campo</th><th>Value / Valor</th></tr>"
        "<tr><td>Exporter (Seller)</td><td>Black King - Matheus Reis Pereira "
        "(CNPJ 50.042.585/0001-80), Av. Tancredo Neves, 4900, Qd H, Cs 9, "
        "Ilheus, BA, 45655-650, Brazil</td></tr>"
        "<tr><td>Importer (Buyer)</td><td>TrueTech Inc - EIN 88-3411514, "
        "1423 Hayes St, San Francisco, CA 94117, USA</td></tr>"
        "<tr><td>Incoterms</td><td>FOB - freight paid by buyer</td></tr>"
        "<tr><td>Currency / Moeda</td><td>USD (BRL for reference)</td></tr>"
        "<tr><td>Exchange rate</td><td>BACEN PTAX 18/09/2026 - venda 5.1575 "
        "BRL/USD</td></tr>"
        "<tr><td>Mode / Route</td><td>Air / Aereo - SSA (Salvador) to "
        "SFO (San Francisco)</td></tr></table>"
    )


def uval_cell(r):
    return f2(r["uval"]) if r["u"] else "n/a *"


def invoice_html():
    rs = rows()
    tusd = sum(r["usd"] for r in rs)
    tbrl = sum(r["brl"] for r in rs)
    k = head(
        "Commercial Invoice / Fatura Comercial",
        "INV-2026-0611-001 (Rev 13) - bilingual EN / PT - USD + BRL",
    )
    k += (
        "<h2>Line Items - declared units of measure (uTrib) / "
        "Itens da Fatura</h2>"
        "<p class='note'>Norm: 1801 / 1803 / 1804 / 1805 = <b>TON</b>; "
        "1802 / 1806 = KG. This is the column the NF-e emitter validates and "
        "the correction Rev 11 needed.</p><table>"
        "<tr><th>#</th><th>NCM</th><th>Description / Descricao</th>"
        "<th>Qty (uTrib)</th><th>uTrib</th><th>Unit USD / uTrib</th>"
        "<th>Total USD / BRL</th></tr>"
    )
    for r in rs:
        u = r["u"] or "n/a *"
        k += (
            f"<tr><td>{r['n']}</td><td>{r['ncm']}</td>"
            f"<td>{r['en']} / {r['pt']}</td>"
            f"<td class='r'>{f6(r['trib_qty'])}</td><td>{u}</td>"
            f"<td class='r'>{uval_cell(r)}</td>"
            f"<td class='r'>{f2(r['usd'])} / {f2(r['brl'])}</td></tr>"
        )
    k += "</table>"
    k += (
        "<p class='note'>* NCM 2106.90.00 (Cacao Tea, line 8) is "
        "outside Chapter 18 and is not keyed by the norm table; it is "
        "declared in KG.</p>"
    )
    k += (
        "<h2>Commercial reference (uCom) / Referencia comercial</h2>"
        "<p class='note'>Unchanged from Rev 11 - retained for line-by-line "
        "reconciliation, not for the NF-e declaration.</p><table>"
        "<tr><th>#</th><th>NCM</th><th>Qty</th><th>uCom</th>"
        "<th>Unit USD</th><th>Total USD</th></tr>"
    )
    for r in rs:
        k += (
            f"<tr><td>{r['n']}</td><td>{r['ncm']}</td>"
            f"<td class='r'>{r['qty']:g}</td><td>{r['ucom']}</td>"
            f"<td class='r'>{f4(r['usd'] / r['qty'])}</td>"
            f"<td class='r'>{f2(r['usd'])}</td></tr>"
        )
    k += "</table>"
    k += (
        "<h2>Totals / Totais</h2><table>"
        "<tr><th style='width:40%'>Field / Campo</th><th>Value / Valor</th>"
        "</tr>"
        f"<tr><td>Subtotal (lines 1-10)</td><td>{f2(tusd)} USD / "
        f"R$ {f2(tbrl)} BRL</td></tr>"
        f"<tr><td>Total Invoice Value</td><td>{f2(tusd)} USD / "
        f"R$ {f2(tbrl)} BRL</td></tr>"
        "<tr><td>BRL basis</td><td>USD total x BACEN PTAX venda 5.1575 "
        "(18/09/2026)</td></tr>"
        "<tr><td>ICMS / IPI</td><td>Isento (export)</td></tr>"
        "<tr><td>PIS / COFINS</td><td>Suspensao (export regime)</td></tr>"
        "</table>"
    )
    k += pallets_html()
    k += boxes_html()
    k += flags_html()
    k += (
        "<h2>Revision Note / Nota de Revisao (Rev 12 to Rev 13)</h2><ul>"
        "<li><b>Rev-12 lines 6 (Cacao Tea AGL8, 12 kg) and 8 (Cacao Almonds "
        "AGL13, 15 kg) removed</b> - not in the physical shipment.</li>"
        "<li><b>New line 10:</b> 5 kg Para cacao-almond samples, regular "
        "box, nominal value $0.05.</li>"
        "<li>Totals: <b>10 lines, 28 boxes (23 regular + 5 irregular)</b>, "
        f"{f2(tusd)} USD / R$ {f2(tbrl)} BRL @ PTAX 5.1575.</li></ul>"
    )
    return k


def pallets_html():
    return (
        "<h2>Palletization / Paletizacao</h2><table>"
        "<tr><th style='width:40%'>Field / Campo</th><th>Value / Valor</th>"
        "</tr>"
        "<tr><td>Pallet type</td><td>Plastic HDPE (Huatai) - non-wood"
        "</td></tr>"
        "<tr><td>Footprint / height</td><td>1000 x 1200 x 150 mm</td></tr>"
        "<tr><td>Tare weight</td><td>10 kg each</td></tr>"
        "<tr><td>Pallet count / total tare</td><td>2 / 20 kg</td></tr>"
        "<tr><td>ISPM#15</td><td>NOT APPLICABLE - plastic is exempt</td>"
        "</tr>"
        "<tr><td>Fumigation / Phytosanitary cert</td><td>Not required"
        "</td></tr></table>"
    )


def boxes_html():
    rs = rows()
    reg = sum(BOXES[r["n"]][0] for r in rs)
    irr = sum(BOXES[r["n"]][1] for r in rs)
    k = (
        "<h2>Boxes / Volume count / Caixas</h2>"
        "<p class='note'>Regular = 10 kg boxes (Mercado Livre); "
        "irregular = original retail / non-standard boxes.</p><table>"
        "<tr><th>#</th><th>Description / Descricao</th><th>Net kg</th>"
        "<th>Regular</th><th>Irregular</th><th>Total</th></tr>"
    )
    for r in rs:
        a, b = BOXES[r["n"]]
        k += (
            f"<tr><td>{r['n']}</td><td>{r['en']} / {r['pt']}</td>"
            f"<td class='r'>{f4(r['net_kg'])}</td>"
            f"<td class='r'>{a}</td><td class='r'>{b}</td>"
            f"<td class='r'>{a + b}</td></tr>"
        )
    k += (
        f"<tr><th>Total</th><th></th><th class='r'></th>"
        f"<th class='r'>{reg}</th><th class='r'>{irr}</th>"
        f"<th class='r'>{reg + irr}</th></tr></table>"
    )
    return k


def flags_html():
    return (
        "<h2>Units of measure applied / Unidades aplicadas</h2><ul>"
        "<li>Each line is declared in the exact uTrib the provided norm table "
        "gives for its NCM: <b>1801 / 1803 / 1804 / 1805 -&gt; TON</b> "
        "(tonelada metrica liquida); <b>1802 / 1806 -&gt; KG</b> "
        "(quilograma). No unit has been substituted or reclassified.</li>"
        "<li><b>Lines 6 and 10 (Cacao Tea, NCM 2106.90.00):</b> this NCM is "
        "outside the provided table, so no unit was supplied for it; the line "
        "is declared in KG.</li>"
        "<li><b>Net weight:</b> sum of lines, derived from documented pack "
        f"sizes = {f2(sum(r['net_kg'] for r in rows()))} kg.</li>"
        "<li><b>Box count:</b> "
        f"{sum(v[0] + v[1] for v in BOXES.values())} boxes = "
        f"{sum(v[0] for v in BOXES.values())} regular + "
        f"{sum(v[1] for v in BOXES.values())} irregular (Rev 13).</li>"
        "<li><b>uTrib quantity</b> = net kg / 1000 for TON lines, else kg; "
        "<b>uTrib unit value</b> = line USD total / qTrib.</li></ul>"
    )


def pl_html():
    rs = rows()
    tnet = sum(r["net_kg"] for r in rs)
    k = head(
        "Packing List / Lista de Embalagem",
        "PL-2026-0611-001 (Rev 13) - bilingual EN / PT",
    )
    k += (
        "<h2>Packing Detail / Detalhe da Embalagem</h2>"
        "<p class='note'>Declared in the mandated export uTrib, with the "
        "commercial unit retained for reconciliation.</p><table>"
        "<tr><th>#</th><th>Description / Descricao</th><th>Qty</th>"
        "<th>uCom</th><th>Net kg</th><th>Qty (uTrib)</th><th>uTrib</th>"
        "</tr>"
    )
    for r in rs:
        u = r["u"] or "n/a *"
        k += (
            f"<tr><td>{r['n']}</td><td>{r['en']} / {r['pt']}</td>"
            f"<td class='r'>{r['qty']:g}</td><td>{r['ucom']}</td>"
            f"<td class='r'>{f4(r['net_kg'])}</td>"
            f"<td class='r'>{f6(r['trib_qty'])}</td><td>{u}</td></tr>"
        )
    k += "</table>"
    k += pallets_html()
    k += boxes_html()
    k += (
        "<h2>Weights / Pesos</h2><table>"
        "<tr><th style='width:40%'>Field / Campo</th><th>Value / Valor</th>"
        "</tr>"
        f"<tr><td>Net weight (derived, sum of lines)</td>"
        f"<td>{f2(tnet)} kg</td></tr>"
        f"<tr><td>Gross weight (+ 20 kg pallet tare)</td>"
        f"<td>{f2(tnet + 20)} kg</td></tr>"
        "</table>"
    )
    k += flags_html()
    k += (
        "<h2>Revision Note / Nota de Revisao (Rev 12 to Rev 13)</h2><ul>"
        "<li><b>Rev-12 line 6 (Cacao Tea AGL8, 12 kg) and line 8 (Cacao "
        "Almonds AGL13, 15 kg) are NOT in the shipment</b> - removed.</li>"
        "<li><b>One new line added:</b> 5 kg of Para cacao-almond samples, "
        "in a regular box (nominal declared value - samples).</li>"
        "<li>Result: <b>10 lines, 28 boxes = 23 regular + 5 irregular</b>, "
        "net 322.06 kg / gross 342.06 kg.</li>"
        "<li>The NCM to export-uTrib unit remap introduced in Rev 12 is "
        "unchanged; no unit was substituted.</li>"
        "<li>Carton count now carried on this packing list (it previously "
        "lived only on the CC-e).</li></ul>"
    )
    return k


CSS = """
@page { size: A4; margin: 1.4cm 1.2cm;
  @bottom-center { content: "TrueSight DAO - Black King export docs - page "
    counter(page) " of " counter(pages); font-size: 7pt; color: #888; } }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 8pt; line-height: 1.35; color: #222; }
h1 { font-size: 15pt; color: #3D2B1F; margin: 0; }
h2 { font-size: 10.5pt; color: #5A4632; border-bottom: 1.5px solid #C98A2D;
  padding-bottom: 2pt; margin: 12pt 0 4pt; page-break-after: avoid; }
.sub { font-size: 9pt; color: #5A4632; margin: 2pt 0 6pt; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0;
  font-size: 7pt; table-layout: fixed; }
th, td { border: 1px solid #DDD; padding: 2.5pt 3pt; text-align: left;
  vertical-align: top; word-wrap: break-word; overflow-wrap: break-word; }
th { background: #DDD; color: #3D2B1F; font-weight: bold; }
tr { page-break-inside: avoid; }
.note { font-size: 7pt; color: #5A4632; }
ul { margin: 3pt 0 3pt 14pt; padding: 0; }
li { margin: 2pt 0; }
.r { text-align: right; }
"""

DOCS = [
    (
        "2026-10-02_commercial_invoice_black_king_to_truetech_rev13_EN_PT_BRL.pdf",
        invoice_html,
    ),
    ("2026-10-02_packing_list_black_king_to_truetech_rev13_EN_PT.pdf", pl_html),
]


def main():
    OUTDIR.mkdir(exist_ok=True)
    for name, fn in DOCS:
        html = (
            f'<html><head><meta charset="utf-8"><style>{CSS}</style>'
            f"</head><body>{fn()}</body></html>"
        )
        path = OUTDIR / name
        HTML(string=html).write_pdf(path)
        print("built:", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
