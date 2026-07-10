#!/usr/bin/env python3
"""Generate PROSPERA_ENTITY_OPERATING_AGREEMENT.pdf from the matching .md.

Usage:  python3 scripts/build_prospera_operating_agreement_pdf.py
Deps:   pip install markdown weasyprint

Portrait A4 legal instrument. Saffron Monk palette (PDF_STYLE_CONVENTION.md).
Overlap-safe layout copied from build_usa_santos_production_spec_pdf.py.
"""

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "PROSPERA_ENTITY_OPERATING_AGREEMENT.md"
OUT = ROOT / "PROSPERA_ENTITY_OPERATING_AGREEMENT.pdf"
LOGO = ROOT / "assets" / "truesight_dao_logo_long.png"

CSS = """
@page {
    size: A4;
    margin: 2.0cm 1.8cm;
    @bottom-center {
        content: "TrueSight DAO LLC (Próspera ZEDE) · Operating Agreement — DRAFT v0.1 · page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #8a7b6b;
    }
}
body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.5;
    color: #2c2419;
}
h1 {
    font-size: 16pt; color: #ffffff; background: #c8801a;
    padding: 9pt 12pt; margin: 0 0 12pt 0; border-radius: 2pt;
    page-break-after: avoid;
}
h2 { font-size: 12.5pt; color: #4a2f1b; border-bottom: 1px solid #e0d3c2; padding-bottom: 3pt; margin-top: 16pt; page-break-after: avoid; }
h3 { font-size: 10.5pt; color: #4a2f1b; margin-top: 10pt; page-break-after: avoid; }

/* Overlap-safe tables: fixed layout + wrapping so cells never overflow columns. */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
    font-size: 8.8pt;
    table-layout: fixed;
}
th, td {
    border: 1px solid #d8c9b5;
    padding: 4pt 6pt;
    text-align: left;
    vertical-align: top;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}
th { background: #f3eadd; color: #4a2f1b; }
tr, thead, h1, h2, h3 { page-break-inside: avoid; }
blockquote { border-left: 3px solid #c8801a; margin: 8pt 0; padding: 4pt 12pt; background: #faf5ec; color: #5d4a33; page-break-inside: avoid; }
em { color: #5d4a33; }
code { font-family: Menlo, monospace; font-size: 8pt; background: #f3eadd; padding: 0 2pt; }
li { margin: 2pt 0; }
a { color: #8a5310; text-decoration: none; }
hr { border: none; border-top: 1px solid #e0d3c2; margin: 12pt 0; }
strong { color: #4a2f1b; }
.doc-logo { display: block; height: 46pt; width: auto; margin: 0 0 14pt 0; }
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "smarty"])
    logo_html = (
        f'<img class="doc-logo" src="{LOGO.as_uri()}" alt="TrueSight DAO">'
        if LOGO.exists()
        else ""
    )
    html = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{logo_html}{body}</body></html>'
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
    print(f"built: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
