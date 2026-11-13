# PDF Generation SOP — Multibyte (CJK) Support & Verification

> Origin: 2026-11-13. A consolidated contribution record for Elizabeth Wong covering three Chinese
> DeepSeek invoices (CNY 600.00 → USD 90.00 → 90.00 TDG) rendered **every Chinese character as
> `IIIIIIIIIIIIIIIIIIII`**. Gary caught it. The PDF had already been presented once.
>
> This SOP exists so that defect cannot recur silently.

## 1. Scope

Applies to **every** PDF produced by the autopilot or any DAO tooling — contribution records,
receipts, payout reports, decks, invoices, partner documentation. A document containing **any**
non-Latin text is in scope, including:

- Simplified/Traditional Chinese (invoices, vendor names, seals, 大写 amounts)
- Japanese kana, Korean hangul
- Portuguese/Spanish accented Latin (renderable in WinAnsi, but verify — see §6)
- Arabic, Hebrew, Devanagari, Cyrillic — anything outside `WinAnsiEncoding`

## 2. The defect and its root cause

The autopilot's `generate_pdf` (`truesight_autopilot/app/tools/pdf_tools.py`, `app/tools/pdf_tools.py`)
registered only reportlab's **base-14 Type1 fonts with `WinAnsiEncoding`**.

`WinAnsiEncoding` is a 256-glyph Latin-1 codepage. **CJK codepoints have no mapping in it.**
reportlab does not raise — it silently substitutes a fallback glyph, producing visible `I` runs (or
blank space). The document looks plausible at a glance, which is why this shipped.

**Why it went unnoticed:** Latin-only documents are unaffected. The bug only manifests in documents
with multibyte content — exactly the ones submitted by non-English-speaking partners.

## 3. Requirement (MUST)

Any PDF containing non-Latin text MUST have an appropriate **TrueType/OpenType font
subset-embedded** in the file.

1. **Detect before render.** Probe the content (and the title/header) for codepoints outside
   `WinAnsi`. Only pay the embedding cost when multibyte text is actually present.
2. **Embed, don't reference.** The font must be *subset-embedded* so the PDF renders correctly on a
   machine that has no CJK fonts installed — the recipient's laptop, a phone, an email preview.
3. **Route per-run, not wholesale.** Switch to the CJK face **only for the CJK runs**, keeping
   Helvetica for Latin copy. Swapping the *entire* document to a CJK face destroys the house
   (Saffron Monk) typography — the fix must not trade one defect for another.
4. **Cover non-paragraph paths too.** Headers/footers drawn with raw `canvas.drawString` have no
   markup engine. Those need manual per-run advance using `pdfmetrics.stringWidth(text, font, size)`.
5. **Never degrade silently.** If no embeddable CJK font is found, **log a warning**. Do not produce
   a PDF that quietly renders `I` runs.

## 4. Font selection — the trap

**Noto Sans CJK is the obvious choice and it does not work.** Its `.ttc` ships **PostScript (CFF)
outlines**, which reportlab's `TTFont` refuses:

```
TTFError: TTC file "NotoSansCJK-Regular.ttc": postscript outlines are not supported
```

Use a **TrueType-outline** CJK face. Verified working on the autopilot box:

| Font | Path | Status |
|---|---|---|
| WenQuanYi Micro Hei | `/usr/share/fonts/truetype/wqy/wqy-microhei.ttc` | **works** (preferred) |
| WenQuanYi Zen Hei | `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` | works |
| AR PL UMing | `/usr/share/fonts/truetype/arphic/uming.ttc` | works |
| Noto Sans CJK | `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` | **fails** — PostScript outlines |

Register a `.ttc` with `TTFont(name, path, subfontIndex=0)`.

## 5. Verification gate (MUST — this is the part that was skipped)

**A PDF is not done until its text has been extracted back out and checked.** Visual inspection is
insufficient: `I` runs look like column alignment, and reviewers who cannot read the script will not
notice blank glyphs.

Minimum checks before delivery:

```python
import fitz  # pymupdf

doc = fitz.open(path)
text = "\n".join(p.get_text() for p in doc)

# 1. Every multibyte string present verbatim
assert "杭州深度求索人工智能基础技术研究有限公司" in text

# 2. The corruption signature is absent
assert not re.search(r"\bI{4,}\b", text)

# 3. Markup did not leak into the rendered text
assert "<font" not in text and "&amp;" not in text

# 4. The CJK font is actually embedded
fonts = [f for p in doc for f in p.get_fonts()]
assert any(f[3] and f[1] not in ("", None) for f in fonts)  # a TrueType face, embedded

# 5. Figures survived the change
assert "90.00" in text and "600.00" in text
```

**Report the check results, not just the file.** When a governor has already caught one rendering
defect, asserting "fixed" without evidence is not acceptable — state which strings were probed and
what came back.

## 6. WinAnsi is not automatically safe

`WinAnsiEncoding` covers Latin-1 plus a handful of extras. Characters **outside** it also fall back
silently:

- `¥` (U+00A5) is in WinAnsi — but `￥` (U+FFE5, fullwidth) is **not**
- Romanian/Turkish/Polish glyphs: `ș`, `ț`, `ş`, `ğ`, `ł`, `ą` — **not** in WinAnsi
- Em/en dashes, curly quotes, `€` are fine

So a Portuguese or Spanish document using only accented Latin-1 vowels is safe, but **do not assume**
— run §5 anyway.

## 7. Checklist (every PDF)

1. Does the content contain any non-ASCII character? → probe, don't eyeball.
2. If yes: is a TrueType-outline CJK/multibyte face embeddable on this host? (§4)
3. Is the face routed **only** to multibyte runs so Latin typography survives? (§3.3)
4. Are canvas-drawn titles/headers handled with per-run advance? (§3.4)
5. **Run the §5 gate.** All five checks must pass.
6. Report the probe results to the governor alongside the file.
7. If a check fails, **do not send the PDF** — fix, re-render, re-verify.

## 8. Known-good implementation

Patched and verified 2026-11-13 against `pdf_tools.py`:

- `_cjk_font()` — probes the candidate list once, caches, warns if none usable
- `_has_cjk(text)` / `_CJK_RUN` — regex covering radicals → unified ideographs (U+2E80–U+9FFF),
  compatibility ideographs, U+3000–303F punctuation, kana, fullwidth forms (U+FF00–FFEF)
- `_wrap_cjk(text, font)` — wraps CJK runs in `<font name="...">` for `Paragraph` paths
- `_draw_mixed(canvas, x, y, text, size, latin, cjk)` — per-run `drawString` with `stringWidth` advance

Verified output: `AAAAAA+WenQuanYiMicroHei-0` embedded TrueType, 10/10 CJK strings round-tripping,
zero `I`-run signatures, all 11 financial figures intact.

## 9. Outstanding

- [ ] Land the §8 patch in `truesight_autopilot/app/tools/pdf_tools.py` as a PR (requires the full
      local test gate: compileall, ruff, ruff format, pytest). Patched + render-verified on the box
      but **not yet committed**.
- [ ] Audit previously generated PDFs for the same defect — any document sent with Chinese
      invoices, Brazilian/Portuguese supplier names, or non-Latin partner names is suspect.
- [ ] Consider a shared `pdf_render.py` helper so decks (`SLIDE_DECK_STANDARD.md`) and reports both
      get multibyte support from one implementation rather than two.
