# Liz Bahia Origin Tour — deck generator

Slides are plain HTML rendered to PDF by headless Chrome. No framework.

## Build
```
google-chrome --headless=new --no-sandbox --disable-gpu \
  --no-pdf-header-footer --print-to-pdf=out.pdf deck.html
```
Slides are fixed 13.333in x 7.5in (16:9), one `<div class="slide">` per page.
`img/` holds the photos (sourced from agroverse.shop partner/farm pages).

## Layout classes
- `.slide` — one page; `page-break-after: always`
- `.stop` — stop-slide variant; left column is vertically centered (`justify-content:center`)
  and bullet font is bumped so the text column fills the frame (fixes the old ~40% dead space).
- `.highlight` — burnt-orange callout box at the foot of a stop slide's left column.
- `.band / .title / .sub` — page header. `.foot` — page footer.
- `.h-photo` — 2.4in tall photo. Right column stacks two of them.

## Known pitfalls
- Do NOT use the `assets/partners/headers/*.jpg` **header** images as body photos —
  several are multi-panel stitched collages (e.g. santos-chocolate-factory-header.jpg)
  and crop badly into a single 16:9 box, showing a seam. Use the single photos under
  `assets/partners/<slug>/` instead.
