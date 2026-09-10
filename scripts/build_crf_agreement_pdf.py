#!/usr/bin/env python3
"""Build the bilingual (EN/PT) Tree Planting Support Agreement for
Casa Familiar Rural de Anapu "Dorothy Stang" (CRF) <-> CEPOTX <-> TrueTech Inc.

Source of truth: CRF_ANAPU_TREE_PLANTING_SUPPORT_AGREEMENT.md (repo root).
The MD is split on the <!-- PART-A-EN --> / <!-- PART-B-PT --> markers.

Modeled on the CEPOTX precedent (build_agreement_v2.py, 2026-09-04): same
TrueTech Inc (SunMint/Agroverse) supporter shape, same bilingual-A4 layout,
same logo header + embedded Gary Teh signature, same ISO-7810 card-at-trunk
monitoring clause and native-Amazon species list.

Difference vs. CEPOTX: the planter/beneficiary is a SCHOOL's students, paid
direct-to-student via PIX (per verified tree, no fixed total), with a Lineage
"Route B (Credential + trees)" technical annex and a minors/consent clause.

Renders to a signable PDF via weasyprint. Read-only apart from that PDF.
"""
import base64
import html as _html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path("/home/ubuntu/sunmint_agreement")  # logo + signature PNGs
MD = ROOT / "CRF_ANAPU_TREE_PLANTING_SUPPORT_AGREEMENT.md"
OUT = ROOT / (
    "Tree_Planting_Support_Agreement_CRF_Anapu_Dorothy_Stang_20260910_bilingual_EN-PT.pdf"
)
LOGO = ASSETS / "logo.png"
SIG = ASSETS / "gary_teh_signature.png"
DATE_EN = "10 September 2026"
DATE_PT = "10 de setembro de 2026"

logo_b64 = base64.b64encode(LOGO.read_bytes()).decode()
sig_b64 = base64.b64encode(SIG.read_bytes()).decode()

CSS = """
@page {
    size: A4;
    margin: 1.6cm 1.7cm 2.0cm 1.7cm;
    @bottom-center {
        content: "TrueTech Inc \\00b7 TrueSight DAO \\2014 Tree Planting Support Agreement / Acordo de Apoio ao Plantio de \\00c1rvores \\00b7 page " counter(page) " of " counter(pages);
        font-size: 7.5pt; color: #8a7b6b;
    }
}
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 9.6pt; line-height: 1.5; color: #2c2419; }
.header { text-align: center; margin-bottom: 4pt; }
.header img.logo { height: 1.35cm; margin: 0 auto 2pt auto; }
.header .doclabel { font-size: 8pt; letter-spacing: 2.5px; color: #8a5310; text-transform: uppercase; margin-top: 2pt; }
h1 { font-size: 16pt; color: #4a2f1b; text-align: center; margin: 8pt 0 2pt 0; }
.subtitle { text-align: center; font-size: 10pt; color: #5d4a33; margin-bottom: 14pt; }
.lang-banner { background: #faf5ec; border: 1.5px solid #c8801a; color: #4a2f1b; text-align: center; font-size: 11pt; font-weight: bold; padding: 6pt; margin: 12pt 0; page-break-before: always; page-break-after: avoid; }
.lang-banner.first { page-break-before: avoid; margin-top: 4pt; }
h2 { font-size: 12pt; color: #4a2f1b; border-bottom: 1.5px solid #c8801a; padding-bottom: 2pt; margin: 15pt 0 6pt 0; page-break-after: avoid; }
p { margin: 4pt 0; text-align: justify; }
ul, ol { margin: 4pt 0 4pt 0; padding-left: 18pt; }
li { margin: 2.5pt 0; text-align: justify; }
.sig-table { width: 100%; border-collapse: collapse; margin-top: 8pt; }
.sig-table td { border: none; padding: 0; vertical-align: bottom; }
.sig-img { height: 2.1cm; }
.party { background: #faf5ec; border-left: 3px solid #c8801a; padding: 6pt 10pt; margin: 8pt 0; page-break-inside: avoid; }
.note { background: #faf5ec; border: 1px solid #c8801a; padding: 6pt 10pt; margin: 8pt 0; page-break-inside: avoid; font-size: 9.2pt; }
.small { font-size: 8pt; color: #5d4a33; }
strong { color: #4a2f1b; }
code { font-family: "Courier New", monospace; font-size: 8.8pt; background: #f3eadd; padding: 0 2pt; }
table.data { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.2pt; table-layout: fixed; }
table.data th, table.data td { border: 1px solid #d8c9b5; padding: 4pt 6pt; text-align: left; vertical-align: top; word-wrap: break-word; }
table.data th { background: #f3eadd; color: #4a2f1b; }
hr { border: none; border-top: 1px solid #e0d3c2; margin: 10pt 0; }
.sigline { border-bottom: 1px solid #2c2419; height: 2.6cm; }
"""


def inline(s: str) -> str:
    s = _html.escape(s)
    s = re.sub(r"\\*\\*(.+?)\\*\\*", r"<strong>\\1</strong>", s)
    s = re.sub(r"(?<!\\*)\\*(?!\\*)(.+?)(?<!\\*)\\*(?!\\*)", r"<em>\\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\\1</code>", s)
    return s


def md_to_html(md: str) -> str:
    out, lines, i = [], md.split("\\n"), 0
    while i < len(lines):
        st = lines[i].strip()
        if not st:
            i += 1
            continue
        if st.startswith("### "):
            out.append(f"<h2>{inline(st[4:])}</h2>")
            i += 1
            continue
        if st.startswith("## "):
            out.append(f"<h2>{inline(st[3:])}</h2>")
            i += 1
            continue
        if st.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1

            def cells(r):
                return [c.strip() for c in r.strip("|").split("|")]

            head = cells(rows[0])
            body = [cells(r) for r in rows[2:]] if len(rows) > 2 else []
            t = ['<table class="data">']
            t.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</table>")
            out.append("".join(t))
            continue
        if re.match(r"^[-*] ", st):
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i].strip()):
                items.append(inline(lines[i].strip()[2:]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\\d+\\. ", st):
            items = []
            while i < len(lines) and re.match(r"^\\d+\\. ", lines[i].strip()):
                items.append(inline(re.sub(r"^\\d+\\. ", "", lines[i].strip())))
                i += 1
            out.append("<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>")
            continue
        out.append(f"<p>{inline(st)}</p>")
        i += 1
    return "\\n".join(out)


text = MD.read_text(encoding="utf-8")
A, B = "<!-- PART-A-EN -->", "<!-- PART-B-PT -->"
en_md = text.split(A, 1)[1].split(B, 1)[0]
pt_md = text.split(B, 1)[1]
en_md = re.sub(r"^\\s*##\\s+PART A.*?\\n", "", en_md)
pt_md = re.sub(r"^\\s*##\\s+PARTE B.*?\\n", "", pt_md)

EN = (
    '<div class="lang-banner first">PART A \\u2014 ENGLISH \\u00b7 PARTE A \\u2014 INGL\\u00caS</div>\\n'
    + md_to_html(en_md)
)
PT = (
    '<div class="lang-banner">PART B \\u2014 PORTUGU\\u00caS \\u00b7 PARTE B \\u2014 PORTUGU\\u00caS '
    "(tradu\\u00e7\\u00e3o / translation)</div>\\n"
    + md_to_html(pt_md)
)

SIG = f"""
<hr/>
<h2>13. Signatures \\u00b7 Assinaturas</h2>
<div class="note">
<p><strong>Language.</strong> This Agreement has been prepared in English and Portuguese. Both versions have been read and understood by the parties. In case of any divergence of interpretation, the <strong>English text shall prevail</strong>.</p>
<p><strong>Idioma.</strong> Este Acordo foi redigido em ingl\\u00eas e portugu\\u00eas. Ambas as vers\\u00f5es foram lidas e compreendidas pelas partes. Em caso de diverg\\u00eancia de interpreta\\u00e7\\u00e3o, <strong>prevalece o texto em ingl\\u00eas</strong>.</p>
</div>
<p>IN WITNESS WHEREOF, the parties have executed this Tree Planting Support Agreement as of <strong>{DATE_EN}</strong>.<br/>
EM TESTEMUNHO DO QUE FOI ACORDADO, as partes assinam este Acordo de Apoio ao Plantio de \\u00c1rvores em <strong>{DATE_PT}</strong>.</p>

<table class="sig-table">
<tr>
  <td style="width:50%; padding-right:14pt;">
    <p><strong>For TrueTech Inc (Supporter) / Pela TrueTech Inc (Apoiador)</strong></p>
    <img class="sig-img" src="data:image/png;base64,{sig_b64}" alt="Gary Teh signature"/>
    <p class="small" style="margin-top:2pt;">Gary Teh<br/><strong>President, TrueTech Inc / Presidente, TrueTech Inc</strong><br/>Date / Data: {DATE_EN}</p>
  </td>
  <td style="width:50%; padding-left:14pt; vertical-align:bottom;">
    <p><strong>For CEPOTX (Implementing Partner) / Pela CEPOTX (Parceiro Implementador)</strong></p>
    <div class="sigline"></div>
    <p class="small" style="margin-top:2pt;">Jedielcio Oliveira<br/>Representative, CEPOTX / Representante, CEPOTX \\u2014 Cooperativa Central de Produ\\u00e7\\u00e3o Org\\u00e2nica da Transamaz\\u00f4nica e Xingu<br/>Date / Data: ____________</p>
  </td>
</tr>
<tr>
  <td style="width:50%; padding-right:14pt; vertical-align:bottom;" colspan="2">
    <p><strong>Acknowledged for the beneficiary institution / Reconhecido pela institui\\u00e7\\u00e3o benefici\\u00e1ria</strong></p>
    <div class="sigline"></div>
    <p class="small" style="margin-top:2pt;">Representative, Casa Familiar Rural de Anapu \\u201cDorothy Stang\\u201d<br/>Representante, Casa Familiar Rural de Anapu \\u201cDorothy Stang\\u201d \\u2014 Anapu, Par\\u00e1<br/>Date / Data: ____________</p>
  </td>
</tr>
</table>
"""

html = f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>

<div class="header">
  <img class="logo" src="data:image/png;base64,{logo_b64}" alt="TrueSight DAO"/>
  <div class="doclabel">TrueSight DAO \\u00b7 SunMint Regenerative Finance \\u00b7 Agroverse \\u00b7 English / Portugu\\u00eas</div>
</div>
<h1>Tree Planting Support Agreement<br/><span style="font-size:11pt; color:#5d4a33;">Acordo de Apoio ao Plantio de \\u00c1rvores</span></h1>
<div class="subtitle">TrueTech Inc \\u2014 SunMint / Agroverse \\u00b7 CEPOTX &amp; Casa Familiar Rural de Anapu \\u201cDorothy Stang\\u201d</div>

{EN}
{PT}
{SIG}

</body></html>"""

from weasyprint import HTML  # noqa: E402

HTML(string=html).write_pdf(OUT)
print(f"built: {OUT} ({OUT.stat().st_size} bytes)")
