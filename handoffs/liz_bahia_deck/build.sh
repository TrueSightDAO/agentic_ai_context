#!/usr/bin/env bash
# Build the Liz Bahia Origin Tour deck: HTML -> PDF via headless Chrome.
set -e
cd "$(dirname "$0")"
google-chrome --headless=new --no-sandbox --disable-gpu \
  --no-pdf-header-footer --print-to-pdf=out.pdf deck.html 2>&1 | grep -i "written to file" || true
python3 - <<'PY'
import fitz
d=fitz.open('out.pdf'); print("pages:", d.page_count)
PY
