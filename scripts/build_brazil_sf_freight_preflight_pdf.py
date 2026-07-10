#!/usr/bin/env python3
"""Generate BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.pdf from the markdown source.

Usage:  python3 scripts/build_brazil_sf_freight_preflight_pdf.py
Deps:   pip install markdown weasyprint
"""

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md"
OUT = ROOT / "BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.pdf"

CSS = """
@page {
    size: A4;
    margin: 1.6cm 1.4cm;
    @bottom-center {
        content: "TrueSight DAO · Brazil to SF Freight Preflight · page " counter(page) " of " counter(pages);
        font-size: 7.5pt;
        color: #888888;
    }
}
body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    line-height: 1.4;
    color: #222222;
}
h1 {
    font-size: 16pt;
    color: #3D2B1F;
    border-bottom: 0;
    padding: 0;
    margin-top: 0;
}
h2 { font-size: 11pt; color: #5A4632; border-bottom: 1.5px solid #C98A2D; padding-bottom: 3pt; margin-top: 14pt; page-break-after: avoid; }
h3 { font-size: 10pt; color: #5A4632; margin-top: 10pt; page-break-after: avoid; }
h4 { font-size: 9pt; color: #5A4632; margin-top: 8pt; page-break-after: avoid; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 6pt 0;
    font-size: 7.5pt;
    table-layout: fixed;
}
th, td {
    border: 1px solid #DDDDDD;
    padding: 3pt 4pt;
    text-align: left;
    vertical-align: top;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
th { background: #DDDDDD; color: #3D2B1F; font-weight: bold; }
tr { page-break-inside: avoid; }
blockquote {
    color: #5A4632;
    border-left: 3px solid #C98A2D;
    padding-left: 8pt;
    margin-left: 0;
    font-size: 8pt;
}
code {
    font-family: "Andale Mono", Menlo, monospace;
    font-size: 7.5pt;
    background: #f3eadd;
    padding: 0 2pt;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
pre {
    background: #f3eadd;
    padding: 5pt 7pt;
    font-size: 7.5pt;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
}
pre code { background: none; padding: 0; }
li { margin: 2pt 0; }
a { color: #8A5A1D; text-decoration: none; }
hr { border: none; border-top: 2px solid #C98A2D; margin: 14pt 0; }
strong { color: #3D2B1F; }
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "smarty"])
    html = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
    print(f"built: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
