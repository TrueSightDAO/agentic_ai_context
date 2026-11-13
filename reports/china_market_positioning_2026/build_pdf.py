#!/usr/bin/env python3
"""Generate CHINA_MARKET_ENTRY_DECISIONS.pdf from china_market_report.md.

Saffron Monk brand palette per agentic_ai_context/conventions/PDF_STYLE_CONVENTION.md.
CJK coverage: this box has no Helvetica Neue / Noto Sans CJK installed, so the
font stack falls back to WenQuanYi Zen Hei for Chinese glyphs (verified present
via fc-list) layered under Liberation Sans for Latin text. Verify CJK renders
with `pdftotext CHINA_MARKET_ENTRY_DECISIONS.pdf - | grep '嘉荣'` after building —
do not trust a visual glance alone (see PDF_STYLE_CONVENTION.md's ReportLab warning,
same failure mode applies to any font substitution, not just ReportLab).
"""

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "china_market_report.md"
OUT = ROOT / "CHINA_MARKET_ENTRY_DECISIONS.pdf"

CSS = """
@page {
    size: A4;
    margin: 2.1cm 1.8cm 2.3cm 1.8cm;
    @bottom-center {
        content: "TrueSight DAO — China Market Entry Decisions — page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #888888;
    }
}
body {
    font-family: "Liberation Sans", "WenQuanYi Zen Hei", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #222222;
}
h1 {
    font-size: 19pt; font-weight: bold; color: #ffffff; background: #C98A2D;
    padding: 10pt 14pt; margin: 0 0 6pt 0;
    page-break-after: avoid;
}
h1 + p {
    font-size: 9pt; color: #888888; margin: 0 0 14pt 0;
}
h2 { font-size: 14pt; font-weight: bold; color: #3D2B1F; border-bottom: 1px solid #DDDDDD; padding-bottom: 3pt; margin-top: 18pt; page-break-after: avoid; }
h3 { font-size: 11pt; font-weight: bold; color: #5A4632; margin-top: 11pt; page-break-after: avoid; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
    font-size: 9pt;
    table-layout: fixed;
}
th, td {
    border: 1px solid #DDDDDD;
    padding: 4pt 6pt;
    text-align: left;
    vertical-align: top;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}
th { background: #DDDDDD; color: #3D2B1F; font-weight: bold; }
tr:nth-child(even) td { background: #FAFAFA; }
tr, thead, h1, h2, h3, blockquote { page-break-inside: avoid; }
blockquote { border-left: 3px solid #C98A2D; margin: 8pt 0; padding: 4pt 12pt; background: #FAF5EA; color: #5A4632; }
em { color: #5A4632; }
code { font-family: "Andale Mono", Menlo, monospace; font-size: 8pt; background: #F3EADD; padding: 0 2pt; }
li { margin: 2pt 0; }
a { color: #8A5A1D; text-decoration: none; }
hr { border: none; border-top: 1px solid #DDDDDD; margin: 12pt 0; }
strong { color: #3D2B1F; }
img { display: block; max-width: 70%; max-height: 13cm; height: auto; margin: 10pt auto 3pt auto; border: 1px solid #DDDDDD; border-radius: 2pt; page-break-inside: avoid; }
img + em, p > em:only-child { display: block; text-align: center; font-size: 8.5pt; color: #888888; margin-top: 0; }
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    # Drop the source's own leading "# Title" line — the PDF supplies its own
    # saffron header band + metadata block instead (house style requires one
    # header band, not two stacked titles).
    lines = text.split("\n", 1)
    text = lines[1] if lines[0].startswith("# ") else text
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "smarty"])

    title = "Agroverse 81% Bar — China Market Entry Decisions"
    meta = "For: Gary Teh  &middot;  From: Envoy (Claude), reconciled against Sophia's field audit &amp; errata  &middot;  Date: 2026-11-14  &middot;  Status: decision memo, v3"

    html = (
        f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
        f"<h1>{title}</h1><p>{meta}</p>{body}</body></html>"
    )
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
    print(f"built: {OUT}")


if __name__ == "__main__":
    main()
