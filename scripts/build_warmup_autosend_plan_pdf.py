#!/usr/bin/env python3
"""Generate the shareable WARMUP_AUTOSEND_PLAN.pdf from WARMUP_AUTOSEND_PLAN.md.

Usage:  python3 scripts/build_warmup_autosend_plan_pdf.py
Deps:   pip install markdown weasyprint

Portrait A4 — the doc is prose + narrow tables, comfortable in portrait.
Same Saffron Monk palette as build_attention_surfaces_pdf.py.
"""

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "WARMUP_AUTOSEND_PLAN.md"
OUT = ROOT / "WARMUP_AUTOSEND_PLAN.pdf"

CSS = """
@page {
    size: A4;
    margin: 2.0cm 1.8cm;
    @bottom-center {
        content: "TrueSight DAO · Warm-up Auto-send Plan · page " counter(page) " of " counter(pages);
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
h1 { font-size: 16pt; color: #4a2f1b; border-bottom: 3px solid #c8801a; padding-bottom: 5pt; }
h2 { font-size: 12.5pt; color: #4a2f1b; border-bottom: 1px solid #e0d3c2; padding-bottom: 3pt; margin-top: 14pt; page-break-after: avoid; }
h3 { font-size: 10.5pt; color: #4a2f1b; margin-top: 10pt; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 7pt 0; font-size: 8.5pt; }
th, td { border: 1px solid #d8c9b5; padding: 3.5pt 5pt; text-align: left; vertical-align: top; }
th { background: #f3eadd; color: #4a2f1b; }
tr { page-break-inside: avoid; }
blockquote { border-left: 3px solid #c8801a; margin: 7pt 0; padding: 2pt 10pt; background: #faf5ec; color: #5d4a33; }
em { color: #5d4a33; }
code { font-family: Menlo, monospace; font-size: 8pt; background: #f3eadd; padding: 0 2pt; }
li { margin: 2pt 0; }
a { color: #8a5310; text-decoration: none; }
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "smarty"])
    html = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
    print(f"built: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
