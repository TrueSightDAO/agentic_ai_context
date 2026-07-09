#!/usr/bin/env python3
"""Generate USA_SANTOS_PRODUCTION_SPEC.pdf from USA_SANTOS_PRODUCTION_SPEC.md.

Usage:  python3 scripts/build_usa_santos_production_spec_pdf.py
Deps:   pip install markdown weasyprint

Portrait A4 — prose + spec tables. Saffron Monk palette (PDF_STYLE_CONVENTION.md).

Overlap-safe layout rules baked in (see PDF_STYLE_CONVENTION.md "Overlap safety"):
  - table-layout: fixed + word-wrap so long cell text wraps instead of
    overflowing into the neighbouring column / off the page.
  - vertical-align: top + generous cell padding so multi-line rows never
    collide with adjacent row text.
  - page-break-inside: avoid on rows, headings, blockquotes so boxes are not
    split across a page boundary (which reads as overlap).
  - saffron header band as a block with its own margin, never absolutely
    positioned over body text.
"""

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "USA_SANTOS_PRODUCTION_SPEC.md"
OUT = ROOT / "USA_SANTOS_PRODUCTION_SPEC.pdf"

CSS = """
@page {
    size: A4;
    margin: 2.0cm 1.8cm;
    @bottom-center {
        content: "TrueTech Inc · USA — Santos Production Spec · page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #8a7b6b;
    }
}
body {
    font-family: "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", Helvetica, Arial, sans-serif;
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
img { display: block; max-width: 62%; max-height: 15cm; height: auto; margin: 10pt auto 4pt auto; border: 1px solid #d8c9b5; border-radius: 2pt; page-break-inside: avoid; }
img + em, p > em { display: block; text-align: center; font-size: 8.5pt; color: #8a7b6b; }
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "smarty"])
    html = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
    print(f"built: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
