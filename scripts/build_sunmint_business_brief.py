# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, Image)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

SAFFRON=colors.HexColor("#E8A33D"); CACAO=colors.HexColor("#4A2C1A")
INK=colors.HexColor("#1F1B16"); MUTED=colors.HexColor("#6B6157")
RULE=colors.HexColor("#D9CFC2"); BAND=colors.HexColor("#FBEFD9")

PW,PH=letter; LM=RM=0.78*inch; TM=0.60*inch; BM=0.62*inch; CW=PW-LM-RM
DOC_TITLE="TrueSight DAO — How the Business Works"
RUNNING="A short brief for a first conversation  ·  October 2026"
FOOTSRC="Canonical source: agentic_ai_context/BUSINESS_MODEL.md  ·  figures read from the public registry, Oct 2026"

import os
# Figures are committed under assets/sunmint_brief/ so the brief is reproducible
# from a clean clone. Fall back to /tmp for legacy local runs.
_HERE=os.path.dirname(os.path.abspath(__file__))
def _asset_dirs():
    """Yield candidate asset dirs by walking up from this script (depth-agnostic)."""
    d = _HERE
    for _ in range(6):
        yield os.path.join(d, "assets", "sunmint_brief")
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent


def FIG(name):
    """Resolve a figure: committed repo assets first, then the legacy /tmp copy."""
    for d in list(_asset_dirs()) + ["/tmp"]:
        cand = os.path.join(d, name)
        # isfile, not exists: the asset *directory* exists on a clean clone even
        # when it is empty, and exists() would hand that directory to reportlab
        # as an image path -> "Cannot open resource <dir>".
        if os.path.isfile(cand):
            return cand
    raise SystemExit(
        "missing figure %s - expected assets/sunmint_brief/%s" % (name, name)
    )


def S(name, **kw):
    b=dict(fontName="Helvetica", fontSize=10, leading=14, textColor=INK,
           alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    b.update(kw); return ParagraphStyle(name, **b)

s_h1  =S("h1", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=CACAO, spaceBefore=12, spaceAfter=5)
s_body=S("body", fontSize=10, leading=14.6, spaceAfter=7)
s_lead=S("lead", fontSize=11.2, leading=16, spaceAfter=9)
s_cap =S("cap", fontSize=8.4, leading=11, textColor=MUTED, spaceBefore=4, spaceAfter=8)
s_bul =S("bul", fontSize=10, leading=14.2, leftIndent=13, bulletIndent=2, spaceAfter=5.5)
s_num =S("num", fontSize=10, leading=14.2, leftIndent=19, bulletIndent=2, spaceAfter=6)
s_small=S("small", fontSize=8.6, leading=11.4, textColor=MUTED)
s_mn  =S("mn", fontName="Helvetica-Bold", fontSize=21, leading=22, textColor=CACAO)
s_ml  =S("ml", fontSize=8.2, leading=10.4, textColor=MUTED)

def P(t, st=s_body, **kw): return Paragraph(t, st, **kw)

def header_footer(c, doc):
    c.saveState()
    c.setFillColor(SAFFRON); c.rect(0, PH-0.34*inch, PW, 0.34*inch, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9.2)
    c.drawString(LM, PH-0.225*inch, DOC_TITLE)
    c.drawRightString(PW-RM, PH-0.225*inch, "Page %d of 3" % c.getPageNumber())
    c.setFillColor(MUTED); c.setFont("Helvetica", 7.4)
    c.drawString(LM, PH-0.34*inch-0.16*inch, RUNNING)
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(LM, BM-0.10*inch, PW-RM, BM-0.10*inch)
    c.setFillColor(MUTED); c.setFont("Helvetica", 6.8)
    c.drawString(LM, BM-0.245*inch, FOOTSRC)
    c.restoreState()

def metric(n, label): return [Paragraph(n, s_mn), Paragraph(label, s_ml)]
# ================= PAGE 1 =================
story=[]
story.append(P("We help finance the trees farmers plant — and sell the cacao they produce",
               S("tag", fontName="Helvetica-Bold", fontSize=13, leading=16.5, textColor=CACAO, spaceAfter=7)))
story.append(P(
 "We help finance the trees farmers plant in the Brazilian Amazon: a fixed payment for every tree an independent "
 "check confirms is actually in the ground, paid straight to the planter. <b>What we sell is the cacao those trees "
 "help produce.</b> We don't sell the plantings, and a tree is not a product on offer. Every bag carries a QR code "
 "designed to resolve to a public record of a specific tree — where it is, what it is, who planted it. The cacao is the "
 "business. The provenance is what makes it defensible.", s_lead))

mdata=[[metric("245","trees recorded in the<br/>public registry today"),
        metric("16","farms across the<br/>Brazilian Amazon"),
        metric("424","hectares under<br/>management"),
        metric("0","carbon credits<br/>ever issued")]]
mt=Table(mdata, colWidths=[CW/4.0]*4)
mt.setStyle(TableStyle([
  ("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,-1),BAND),
  ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),6),
  ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
  ("LINEAFTER",(0,0),(-2,-1),0.6,colors.HexColor("#EADFCB"))]))
story.append(mt)
story.append(P("Registry figures from SunMint <i>trees/</i> and <i>farms/</i>, October 2026.", s_small))
story.append(Spacer(1,10))

story.append(Image(FIG("bmfig_p1.png"), width=CW*0.80, height=CW*0.80*(768.0/1344.0)))
story.append(P("<b>Figure 1 — The cycle.</b> Capital funds per-tree payments. Planting produces evidence. "
               "Cacao sales send proceeds back toward the next round.", s_cap))

story.append(P("How the money flows", s_h1))
story.append(P("Capital funds a pool. A fixed payment is made <b>for every tree an independent check confirms was "
               "actually planted</b> — straight to the planter's phone by PIX, with no fixed total and no advance. "
               "The planting is photographed and signed into a public registry, which turns a promise into a "
               "countable record. Larger capital commitments release against verified planting, not against plans.", s_body))
story.append(P("That payment is <b>a cost we carry, funded by the capital we raise — not a product we sell</b>. "
               "Revenue comes from the cacao: those trees are harvested, the beans packed, and the bags sold "
               "wholesale, on consignment, or direct.", s_body))
# ================= PAGE 2 =================
story.append(__import__('reportlab.platypus', fromlist=['PageBreak']).PageBreak())

story.append(P("Who buys", s_h1))
story.append(P("Four channels, three of them running today. Impact funders sit alongside them, but buy something "
               "different — outcomes and reporting, never credits.", s_body))
ch=[[ "Cafés and specialty retailers","Wholesale — an opening order of a set number of bags, priced per bag"],
    [ "Venues without upfront capital","Consignment — a smaller opening order, settled as it sells"],
    [ "Direct consumers","Sold online, with QR provenance on every bag"],
    [ "Impact funders","Verified planting data and reporting — <b>not</b> credits"]]
ct=Table([[Paragraph(a,S("a",fontName="Helvetica-Bold",fontSize=10.6,leading=15,textColor=CACAO)),
           Paragraph(b,S("b",fontSize=10.6,leading=15))] for a,b in ch], colWidths=[CW*0.40,CW*0.60])
ct.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
  ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),8),
  ("TOPPADDING",(0,0),(-1,-1),18),("BOTTOMPADDING",(0,0),(-1,-1),18),
  ("LINEBELOW",(0,0),(-1,-2),0.4,RULE),
  ("LINEBELOW",(0,-1),(-1,-1),0.4,RULE)]))
story.append(ct)
story.append(Spacer(1,4))
story.append(Spacer(1,6))
story.append(P("<b>One constraint worth knowing:</b> a donation cannot carry a right to future carbon credits — "
               "granting one would break its deductibility. So we never offer, imply, or hint at one.", s_body))

story.append(Spacer(1,14))
story.append(P("What we sell — and what we don't", s_h1))
story.append(P(
 "<b>What we sell is cacao</b> — a physical product with a traceable origin. What we finance is the planting "
 "behind it. Those are two different things and worth keeping apart: the planting is a cost we carry; the cacao "
 "is what a customer pays for. Nobody buys a tree from us, and we don't sell plantings at all.", s_body))
story.append(P(
 "We are also not in the carbon-credit business — we don't buy credits, we don't sell credits, and we have never "
 "issued one. A credit rests on a claim about a future that didn't happen, a counterfactual baseline nobody can "
 "see. Our claim is a specific tree at a specific coordinate, photographed on a specific day. Smaller, yes. "
 "Considerably harder to argue with.", s_body))

story.append(Spacer(1,12))
story.append(P("<b>If credit origination ever makes sense, the door is open.</b> The methodology has moved to Verra "
               "VM0047, which benchmarks performance from satellite data rather than a static baseline, and Hong Kong's "
               "Core Climate exchange settles forestry projects in HKD and RMB. Neither is a commitment — both are "
               "reasons this isn't a dead end.", s_body))
# ================= PAGE 3 =================
story.append(__import__('reportlab.platypus', fromlist=['PageBreak']).PageBreak())

story.append(P("So what does the QR on the bag actually show?", s_h1))
story.append(P("The bag is the thing we sell. The QR is how a buyer can see where it came from — it is designed to resolve to a "
               "public page showing a specific tree's coordinates, photograph, species, planter and planting date, "
               "plus the signed record behind it, which anyone can check and nobody can quietly alter. It's "
               "evidence of origin attached to a product, not a product in itself.", s_body))

story.append(Image(FIG("bmfig_p3.png"), width=CW*0.68, height=CW*0.68*(768.0/1344.0)))
story.append(P("<b>Figure 2 — Evidence of origin.</b> The bag is the product; the QR is designed to resolve to a public "
               "provenance record; the planter was paid direct; the record is signed and tamper-evident.", s_cap))

story.append(P("Some things we'd rather say ourselves", s_h1))
story.append(P("If this goes further, these will come up. Better that we raise them.", s_body))
story.append(P("<b>The planting is financed, not sold.</b> We pay per verified tree as a cost of doing business. "
               "No customer buys a planting from us, and no revenue line depends on one.", s_bul, bulletText="•"))
story.append(P("<b>Our records are attested, not independently verified.</b> A farmer signs for what they planted. "
               "No third party has yet inspected that a photo shows the species claimed at the coordinate claimed. "
               "That audit is what would make this credit-grade — and it's a step we haven't taken.", s_bul, bulletText="•"))
story.append(P("<b>The bag-to-tree link is a working pilot.</b> 16 trees carry a linked QR today; 229 more are "
               "recorded but not yet linked to a bag. The mechanism works; it isn't deployed everywhere.", s_bul, bulletText="•"))
story.append(P("<b>We're not on a blockchain.</b> No chain, no tokens. What we have is a public append-only record "
               "with a version history — every change attributable, timestamped, and diffable.", s_bul, bulletText="•"))

story.append(P("What would be useful from a first conversation", s_h1))
story.append(P("A handful of bags with people who will actually scan them and push back; an hour with someone who "
               "knows VM0047 properly, before we pay for a verification body; and a view on whether provenance-first "
               "reforestation has a listing route at this scale — or whether we stay deliberately credit-free. If "
               "anything above overstates our position, we'd rather hear it from you than discover it later.", s_body))

doc=BaseDocTemplate(os.path.join(_HERE,"out.pdf"), pagesize=letter,
    leftMargin=LM, rightMargin=RM, topMargin=TM+0.52*inch, bottomMargin=BM)
fr=Frame(LM, BM, CW, PH-TM-BM-0.52*inch, id="f",
         leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="m", frames=[fr], onPage=header_footer)])
doc.build(story)
print("built")
