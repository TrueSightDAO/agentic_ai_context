# Farmer & Plot Onboarding Guide — FDA FSVP (EN/PT)

**Deliverable (2026-09-07, thread 23261):** bilingual illustrated PDF guide for Jedielcio
(facilitator for future FDA FSVP site inspections). PDF + generator on the autopilot box:

- PDF: `/home/ubuntu/deliverables/FSVP_Onboarding_Guide_EN_PT.pdf` (9 pp, ~8.9 MB)
- Generator: `/home/ubuntu/deliverables/gen_guide_compact.py` (reportlab; reruns to recreate)
- Verified captions: `/home/ubuntu/deliverables/photo_captions_verified.json`

## WhatsApp send protocol (v4, 2026-09-07 — Gary)
Before photos, the farmer opens the WhatsApp message with **Farm Name + CEPOTX site code**
(e.g. La do Sítio — V-06-29) so every photo is tied to the right property. Then each photo is
sent as a **document (attach / anexar), NOT as an image message** — WhatsApp strips
GPS/EXIF location data from image messages, while documents keep the original file with its
coordinates intact. Renaming + per-farm folders stay back-office (see v2 policy). The guide
carries this on p1 (how-to) and p8 (GPS quick note).

## File naming policy (v2, 2026-09-07 — Gary)
**The farmer NEVER renames photos on the phone.** Phones produce IMG_xxxx; nobody hand-renames
40+ files on a phone. The rule `FARMCODE_YYYYMMDD_n` (e.g. LASITIO_20260907_01 · RM_20260815_02)
and "each farm in its own folder" is OUR back-office step, applied AFTER photos arrive. The guide
tells the farmer: "send the photos as they are / envie as fotos como estão". Keep this framing.

## Content (mirrors governor Gary's checklist)

### A · Onboarding a new farmer / Cadastro de novo produtor(a)
1. Photo of farmer owner(s) in front of the farm — Foto do(s) proprietário(s) em frente à fazenda
2. Story about the farm — História sobre a fazenda (text field)
3. Video recording of the farmer speaking about his farm — Vídeo do produtor falando sobre a fazenda
4. Age of the trees — Idade das árvores (field)
5. Type of cacao trees — Tipo de cacaueiros (field)
6. Hectares of the farm — Hectares da fazenda (field)
7. Photo of the cacao trees (+ lat/long) — Foto dos cacaueiros (+ GPS)
8. Photo of the fermentation tank/boxes (+ lat/long)
9. Photo of the drying station (+ lat/long)
10. Bean-to-bar only (farms with that capability):
    a. Roaster (+ lat/long) — Torrador
    b. Cracker & winnower (+ lat/long) — Quebrador/ventilador
    c. Melanger (+ lat/long) — **placeholder (no real example photo yet)**
    d. Chocolate mold (+ lat/long) — Forma de chocolate
    e. Fridge (+ lat/long) — Refrigerador/câmara fria

### B · Onboarding a new reforestation plot / Cadastro de novo talhão de reflorestamento
1. Photo of each corner of the plot (polygon, GPS each corner) — 4 corner photos
2. Total count of trees on the plot (field)
3. Count of each tree species on the plot (field)
4. Video walking along the plot + photos of individual trees (+ GPS)

### C · Every six months / A cada seis meses (monitoring)
1. Video of walking along the plot
2. Photos of individual trees (+ GPS)

## Real photos used as examples (Grok-verified contents, 2026-09-07)

| Checklist item | Source photo | Source farm | Verified content |
|---|---|---|---|
| Farmer in front of farm | raimundo-geniza-hero-8236.jpg | Raimundo & Geniza (agroverse_shop_beta assets) | Farmer on wooden deck overlooking farm |
| Farmer video still | fs8_hero_farmer_pod.jpg | cvp/web (FS8 family) | Farmer holding ripe cacao pod |
| Cacao trees / grove | plot2_IMG_7659.jpg | Rancho Maranta p2 | People among cacao trees |
| Fermentation | fermentation_facility.jpg | La do Sitio FSVP set 2026-09-07 | Wooden shed + fermentation barrels |
| Drying station | drying_station.jpg | La do Sitio (HEIC→JPG) | Beans drying behind mesh |
| Roaster | roasting_station.jpg | La do Sitio FSVP set | Stainless roaster |
| Cracker & winnower | cracking_and_winnowing.jpg | La do Sitio FSVP set | Blue tabletop unit |
| Chocolate mold | cabrellon-mold.png | agentic_ai_context assets | Clear plastic bar mold |
| Fridge | fridge_for_making_bar.jpg | La do Sitio FSVP set | Upright freezer |
| Plot corners (4) | corner_IMG_7624–7627.jpg | Rancho Maranta p1 | Young cacao in field |
| Plot walk | plot2_IMG_7657/7658.jpg | Rancho Maranta p2 | Two men walking in grove |
| Individual trees | tree_IMG_8884/8885/8891.jpg | La do Sitio trees extract | Cacao saplings |
| Storage / inspection | storage_facility.jpg | La do Sitio FSVP set | Men inspecting cocoa sacks |

**Not used:** founderhaus_group_planting.jpg (not farmer-owner portrait); plot2_IMG_7660.jpg (damaged
sapling); pdfpage1_img0.png (equipment-PDF extract = chocolate bar on mold, NOT a melanger).

## Layout guard (v6, 2026-09-08 — Gary)
Each numbered item's heading and its example photo are wrapped in `KeepTogether` so the photo
can never be pushed to the next page away from its heading (Gary's requirement: the melanger
photo must appear immediately after the '10c · Photo of the melanger (+ GPS)' heading).
Generator now imports KeepTogether and wraps 10b and 10c (heading + photo_block). Verified on
printed page 6: 10c heading y≈298 → melanger photo y≈318–497, nothing between. Rebuild with:
```
python3 /home/ubuntu/deliverables/gen_guide_compact.py
```

## Melanger photo (v5, 2026-09-08 — Gary supplied)
Real melanger photo now embedded (item 10c). Gary sent a photo; staged at
`/tmp/guide_assets/small/melanger.jpg` (1280×960, downscaled q70) and the generator's
placeholder panel was replaced with a `photo_block`. PDF rebuilt: page 5 shows
"Example: melanger (grind/refine) — supplied photo / Exemplo: melanger (moagem/refino) — foto fornecida."
Background context: previously no farm in our network had a melanger installed (La do Sitio at
Stage 1, roast → crack & winnow; Kingma melanger on the 'to acquire' list per
BEAN_TO_BAR_EQUIPMENT_INVENTORY.md and the 2026-09-07 CEPOTX site-visit report). The supplied
photo resolves the evidence gap; the Stage-2 caveat no longer appears in the PDF.

## Regenerate
```
python3 /home/ubuntu/deliverables/gen_guide_compact.py
```
(outputs `/tmp/guide_assets/FSVP_Onboarding_Guide_EN_PT_compact.pdf`).
