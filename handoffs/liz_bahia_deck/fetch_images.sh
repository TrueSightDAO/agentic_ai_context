#!/usr/bin/env bash
# Re-download the deck photos from the Agroverse site (single photos, NOT header collages).
set -e
cd "$(dirname "$0")/img"
S="https://www.agroverse.shop/assets/partners/santos-chocolate-factory"
curl -sL -o santos_hero.jpg "$S/santos_wife_putting_bars_in_bag.jpg"
curl -sL -o santos1.jpg    "$S/santos_image_seeing_beans_for_first_time.jpg"
curl -sL -o santos2.jpg    "$S/santos_processing_beans.jpg"
# other stops: pulled from the matching partner/farm pages (headers + inline photos)
echo "Add the remaining stop photos from their partner pages as needed."
