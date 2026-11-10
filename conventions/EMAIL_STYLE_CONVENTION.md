# TrueSight DAO — Email House Style

**Binding on every outbound email the DAO sends** — newsletters, partner outreach, retailer
follow-ups, and any LLM-drafted mail in the `*_EMAIL_TEMPLATE.md` family.

Sibling document: `conventions/PDF_STYLE_CONVENTION.md` (documents). This one is for the
inbox. **Both draw on the same palette** — the brand lives in one set of hex values, and
the medium changes the *technique*, never the colours.

Extends the send SOP already recorded in `scripts/send_newsletter.py`:
**no stored name → neutral greeting; a name is never inferred from an email address.**

---

## 1. Palette — inherited, never re-invented

Exact hex values, identical to `PDF_STYLE_CONVENTION.md`. If you need a colour that is not
here, the answer is a palette amendment in one place, not a local hex code.

| Role | Hex | Use in email |
|---|---|---|
| Body text | `#222222` | all body copy — soft near-black, never pure `#000` |
| **Saffron (primary accent)** | `#C98A2D` | thin top rule, section accents, key rules |
| Clay / caramel | `#8A5A1D` | links, emphasis |
| Cacao brown (dark) | `#3D2B1F` | headings |
| Cacao brown (mid) | `#5A4632` | subheads |
| Muted gray | `#888888` | captions, unsubscribe, metadata |
| Rule / table-gray | `#DDDDDD` | dividers, table header fill |

**Link colour:** use `#8A5A1D` inline. Do not rely on the client's default blue — it will not
match, and some clients restyle links unpredictably.

---

## 2. Where email must differ from PDF — and why

These are deliberate divergences, not oversights. Each one has a failure mode behind it.

| PDF rule | Email rule | Why |
|---|---|---|
| External/shared CSS | **Inline styles only** (`style="…"` on each element) | Gmail, Outlook.com and Yahoo strip `<head>` CSS. An external stylesheet silently does nothing. |
| 475pt content width | **600px max, single column** | 600px is the pragmatic client ceiling. Two columns collapse badly on mobile, which is most opens. |
| 33pt saffron header band | **Thin saffron top rule (3–4px)**, not a filled band | A full-width saffron block reads as a *promotional banner* and floods an already busy inbox. The palette is recognisable at 4px. |
| Helvetica Neue (exact) | **Font stack** | Helvetica Neue does not exist on Windows. Stack: `'Helvetica Neue',Helvetica,Arial,sans-serif`. Never a webfont — many clients refuse to load them. |
| ~10pt body | **16px body, 1.6 line-height** | 10pt is print. At inbox scale it is unreadable on a phone. |
| Fixed pt type scale | **px, 3 sizes only** | Keep it boring: 20px heading, 16px body, 13px caption/meta. |
| Tables as real tables | **Real `<table>` for structure**, not for prose | Same idea, different reason: table layout survives Outlook; CSS layout does not. |

---

## 3. Structure — the wrapper

Every email is wrapped, in this order:

```
<body bgcolor="#FFFFFF">
  outer table, width 100%, bgcolor #FFFFFF
    inner table, width 600, align center
      saffron rule  (border-top: 3px solid #C98A2D)
      content       (padding 24px 0, 16px Helvetica stack, #222, line-height 1.6)
      footer        (1px #DDDDDD top rule, 12–13px #888)
```

Rules that follow from this:

- **Set an explicit background colour** on `<body>` and the outer table. Without it, dark-mode
  clients invert the background and can leave dark text on dark.
- **Never rely on margin on `<p>`** — Outlook collapses it. Use `padding` on the wrapper and
  blank-line separation via the HTML source.
- **Footer always carries:** who sent it, and how to get out. Non-negotiable.

### Preheader

A hidden preview line, max ~90 characters, placed as the first element after `<body>`:

```html
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">
  Short teaser that makes sense alone.
</div>
```

Without it, the client fabricates a preview from whatever the first body text is — usually
`Hi,` or a fragment of a heading. It is the single highest-leverage styling change available
and costs one line.

---

## 4. Images

- **Hosted `https://` URLs only. Never base64 / inline images** — Gmail clips messages with
  inline data-URI images and some clients refuse to render them. This is the trap behind
  "can we embed images?": yes, but by URL, not by embedding bytes.
- **`alt` text is mandatory** on every image. Many clients block remote images by default;
  the alt text is what the reader actually sees.
- **`width` constrained to 100% of the 600px column**, `display:block` (kills the phantom
  gap under inline images), `height:auto`, `border:0`.
- **Supply 2x assets** for retina, and size them down in HTML, not in the editor.
- **Image-to-text ratio:** one or two substantive images per newsletter. A wall of images
  with little text lands in Promotions or Spam.
- **Alt text and filename are copy.** `2026-10-09_pallets_ilheus.jpg`, not `IMG_4471.JPG`.

---

### 4.1 Image content correctness

The rules above govern image *mechanics*. They do not govern whether the image **depicts
what we say it depicts** — and that is the failure mode that actually reaches readers,
because it is invisible to every mechanical check.

**The image must depict its own claim.** Right farm (not merely *a* farm), right subject,
right activity, right shipment mode. If the caption says "Paulo's La do Sitio farm, Pará",
the picture must be that farm in Pará — not a different farm in a different state, and not
a map pin marking where it sits. If the letter's thesis is that a shipment moved by **air
cargo**, the hero must not depict a river ferry.

**Never dress a placeholder as evidence.** Map screenshots, logo slates, generic stock, and
AI renders must never be presented as farm, product, or packing photography. A location pin
is a *location*, not a farm. A rendered illustration is not a photograph of a real bag.
Where no honest photograph exists, ship the newsletter with fewer images rather than with a
substitute that asserts something untrue — §4 already sets a low bar of "one or two
substantive images", and zero is better than a false one.

**Filename and alt text are untrusted inputs, not verification.** Both are written by the
same person who made the mistake, and a wrong image almost always carries a confident,
plausible filename. `freight-cargo-boat-header.jpg` looks exactly like a cargo boat;
`cacao-flower-to-bar.jpg` looks exactly like flower-to-bar production. Neither is evidence.
Open the pixels.

**People in photographs — consent before publication.** For any public marketing send,
confirm that every *identifiable* person in the frame has agreed to appear, including
bystanders who are not the subject of the photo. A crowded dock or ferry deck is not
consent. Default preference: use people-free assets for public sends; a product or packing
photograph can almost always be taken without strangers in it. Where people are the point
— team, farmers, packing day — treat consent as a prerequisite of the send, not a
follow-up to it.

**Verification is a line item, not a vibe.** Before a campaign is approved, each image gets
a row: `filename | claimed subject | caption/alt text | verdict`. Verdict is reached by
opening the image, not by reading its name. Anything not explicitly verified is, for send
purposes, unverified.

#### 4.1.1 Candidate automation (recorded, not built)

This class of defect is mechanically detectable: a vision model given the candidate image
together with its proposed caption/alt text can be asked whether the image supports the
claim — right subject, right scene type (photo vs map vs render), and whether identifiable
people are present. That would catch a map screenshot captioned as a farm, a wrong-farm
photo, and an unconsented crowd, without depending on a human noticing after the fact.

Not built as of 2026-11. Recorded here so the gap is written down rather than rediscovered.
See `OPEN_FOLLOWUPS.md` for status.

---

## 5. Copy and typography limits

- **Subject:** aim ≤50 characters. No ALL CAPS, no emoji, at most one exclamation mark.
  Longer subjects truncate on mobile — assume ~35 chars are visible.
- **One primary call to action.** Multiple competing links split attention and depress
  click-through on every one of them.
- **Paragraphs: 2–4 sentences.** Long unbroken blocks are not read in an inbox.
- **scannable structure:** short paragraphs, `-` bullets, bold lead-ins. Not a wall.
- **Plain-text parity is required** — every send must carry a real `text/plain` alternative,
  not an HTML-only message with a "view online" crutch. The sender already builds this via
  `markdown_to_plain`, so keep both parts fed from the same source copy.
- **Personalisation per the send SOP:** `{{greeting}}` / `{{first_name}}` fill per recipient;
  **absent name → neutral `Hi,`**. Never derive a name from an email local-part.

---

## 6. Deliverability is part of aesthetics

A beautiful email nobody receives is a failed email.

- **Never buy or import a list.** Confirmed opt-in only.
- **Consistent From name and address** across campaigns — recognition drives opens, and
  inconsistency looks like spoofing.
- **Keep the image count low and the text substantial** (see §4) — a high image-to-text
  ratio is a spam signal.
- **Honour unsubscribes immediately.** One ignored opt-out damages the domain, not the
  recipient.
- **Don't send to the same list more often than there is something to say.** A milestone is a
  reason; a reminder is not.

---

## 7. Verification before any list send

1. **Send a single-address sample to yourself first** (`--to <your address>`), on its own
   campaign tag so it cannot contaminate real campaign statistics.
2. **Open it on a phone, not just desktop.** Most opens are mobile.
3. **Check the plain-text part** — some readers only ever see that.
4. **Confirm the preheader reads sensibly alone**, without the subject for context.
5. **Click every link.** Confirm tracked links resolve to the intended destination.
6. **Confirm images load**, and that alt text is what appears when they do not.
7. **Dark mode**: background is explicit, text stays legible.
8. **Re-read the subject as a stranger** — would you open it, and from whom does it appear to come?

---

## 8. Ship checklist

- [ ] 600px single-column wrapper; explicit `bgcolor` on body and outer table
- [ ] All styles **inline**; no `<head>` CSS, no webfonts, no external stylesheet
- [ ] Font stack `'Helvetica Neue',Helvetica,Arial,sans-serif`; 16px body / 1.6 line-height
- [ ] Palette from §1 only — no ad-hoc hex values
- [ ] Thin saffron rule at top (**not** a filled banner)
- [ ] Preheader text present, ≤90 chars, sensible standalone
- [ ] Images: hosted `https://`, `alt` on all, `display:block`, width-constrained, 2x assets
- [ ] Subject ≤50 chars, no ALL CAPS, no emoji
- [ ] One primary CTA
- [ ] Footer with sender identity + unsubscribe
- [ ] Real `text/plain` alternative
- [ ] Greeting per recipient; neutral `Hi,` where no name is stored
- [ ] Single-address sample reviewed on mobile before the list send

---

## 9. Current implementation gap — recorded, not resolved

As of 2026-11, `scripts/send_newsletter.py:markdown_to_html` emits **bare `<p>` and `<a>`
tags**: no wrapper, no max-width, no font stack, no colour, no preheader. Only the footer
block and image substitution carry any inline style at all.

So §3 and §4 describe a **target state**, not current behaviour. Until the renderer emits
the wrapper described above, newsletters will look plain — which is not *wrong*, just
unbranded. Closing it is a small, contained change to `markdown_to_html` plus a preheader
parameter, and it is worth doing before the next large campaign because it affects every
future send.

**A convention that the code does not yet meet should say so plainly**, otherwise the next
reader assumes the emails already look like this.
