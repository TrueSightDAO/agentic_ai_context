#!/usr/bin/env python3
"""Generate the shareable CHOCOLATE_SUBSCRIPTION_PLAN.pdf from the tracked .md.

Usage:  python3 scripts/build_chocolate_subscription_plan_pdf.py
Deps:   pip install markdown weasyprint

Saffron Monk house style per agentic_ai_context/PDF_STYLE_CONVENTION.md:
saffron header band, metadata block, branded tables (no raw pipes), muted footer.
Portrait A4 — prose + narrow status tables.
"""

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "CHOCOLATE_SUBSCRIPTION_PLAN.md"
OUT = ROOT / "CHOCOLATE_SUBSCRIPTION_PLAN.pdf"

# Exact Saffron Monk palette (PDF_STYLE_CONVENTION.md)
SAFFRON = "#C98A2D"
CLAY = "#8A5A1D"
CACAO_DARK = "#3D2B1F"
CACAO_MID = "#5A4632"
BODY = "#222222"
MUTED = "#888888"
RULE = "#DDDDDD"

METADATA = """
<div class="meta">
  <div><span class="k">For:</span> TrueSight DAO / Agroverse contributors</div>
  <div><span class="k">From:</span> Claude (agentic AI) — design ratified with Gary Teh</div>
  <div><span class="k">Date:</span> 2026-06-09</div>
  <div><span class="k">Status:</span> Roadmap aligned · implementation begins at Phase&nbsp;1 PR1.1</div>
</div>
"""

CSS = f"""
@page {{
    size: A4;
    margin: 2.0cm 1.8cm;
    @bottom-center {{
        content: "TrueSight DAO · Agroverse Chocolate Subscriptions · page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: {MUTED};
    }}
}}
body {{
    font-family: "Helvetica Neue", "PingFang SC", "Noto Sans CJK SC", Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.5;
    color: {BODY};
}}
/* h1 → full-width saffron header band */
h1 {{
    background: {SAFFRON};
    color: #ffffff;
    font-size: 18pt;
    font-weight: bold;
    padding: 10pt 14pt;
    margin: 0 0 4pt 0;
    border-radius: 2pt;
}}
.meta {{
    font-size: 8.5pt;
    color: {CACAO_MID};
    margin: 0 0 12pt 0;
    padding-bottom: 8pt;
    border-bottom: 1px solid {RULE};
}}
.meta .k {{ color: {MUTED}; display: inline-block; min-width: 42pt; }}
h2 {{ font-size: 13pt; color: {CACAO_DARK}; border-bottom: 2px solid {SAFFRON};
      padding-bottom: 3pt; margin-top: 16pt; page-break-after: avoid; }}
h3 {{ font-size: 10.5pt; color: {CACAO_MID}; margin-top: 11pt; page-break-after: avoid; }}
table {{ border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 8.5pt; }}
th, td {{ border: 1px solid {RULE}; padding: 4pt 6pt; text-align: left; vertical-align: top; }}
th {{ background: {RULE}; color: {CACAO_DARK}; font-weight: bold; }}
tbody tr:nth-child(even) {{ background: #faf7f1; }}
tr {{ page-break-inside: avoid; }}
blockquote {{ border-left: 3px solid {SAFFRON}; margin: 8pt 0; padding: 4pt 12pt;
              background: #faf5ec; color: {CACAO_MID}; }}
blockquote strong {{ color: {CLAY}; }}
em {{ color: {CACAO_MID}; }}
strong {{ color: {CACAO_DARK}; }}
code {{ font-family: "Andale Mono", Menlo, monospace; font-size: 8pt;
        background: #f3eadd; padding: 0 2pt; color: {CACAO_DARK}; }}
pre {{ background: #f7f1e7; border: 1px solid {RULE}; border-radius: 2pt;
       padding: 7pt 9pt; font-size: 7.5pt; line-height: 1.35; overflow-x: hidden;
       page-break-inside: avoid; }}
pre code {{ background: none; padding: 0; }}
li {{ margin: 2pt 0; }}
a {{ color: {CLAY}; text-decoration: none; }}
hr {{ border: none; border-top: 1px solid {RULE}; margin: 12pt 0; }}
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "smarty"])
    # Inject the metadata block directly after the <h1> title.
    if "</h1>" in body:
        body = body.replace("</h1>", "</h1>" + METADATA, 1)
    html = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
    print(f"built: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
