#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
for L in en pt; do
  src=deck.html; [ "$L" = pt ] && src=deck_pt.html
  google-chrome --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
    --print-to-pdf=out_$L.pdf "$src" >/dev/null 2>&1
  echo "$L -> $(python3 -c "import fitz;print(fitz.open('out_$L.pdf').page_count,'pages')")"
done
python3 - <<'PY'
import fitz
a=fitz.open('out_en.pdf'); b=fitz.open('out_pt.pdf')
a.insert_pdf(b)
a.save('AGROVERSE_CACAO_ADVENTURES_AUTUMN_SOLSTICE_2026_EN_PT.pdf')
print('merged:', fitz.open('AGROVERSE_CACAO_ADVENTURES_AUTUMN_SOLSTICE_2026_EN_PT.pdf').page_count, 'pages')
PY
