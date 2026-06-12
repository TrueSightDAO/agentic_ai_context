# Placard Generation SOP

**Purpose:** Generate branded landscape placards with QR codes for event table displays (e.g., SF Tech Fest, farmers markets, pop-ups).

**Last updated:** 2026-06-11

---

## 1. Prerequisites

- Python packages: `qrcode[pil]`, `pillow`, `requests`
- Agroverse logo file at: `/opt/truesight_autopilot/tokenomics/agroverse_qr_code_web_service/logos/agroverse_logo.jpeg`
- GitHub PAT with write access to `TrueSightDAO/lineage-assets` (stored in `.env` as `TRUESIGHT_DAO_AUTOPILOT`)
- DejaVuSans fonts at `/usr/share/fonts/truetype/dejavu/`

## 2. QR Code Registration

First, register the QR code via the GAS web app:

```
GET /exec?action=registerSingleQRCode&
  qr_code=<EVENT>_<COLLECTION>_<YYYYMMDD>_<N>&
  landing_page=<URL>&
  farm_name=<EVENT NAME>&
  state=<STATE>&
  country=<COUNTRY>&
  year=<YYYY>&
  currency=<PRODUCT NAME>&
  status=SAMPLE&
  manager=<NAME>&
  creation_date=<YYYYMMDD>
```

**Naming convention:** `{EVENT}_{COLLECTION}_{YYYYMMDD}_{N}`
- Event: e.g., SFTF (SF Tech Fest), FMF (Farmers Market)
- Collection: e.g., FR (Friends of the Rainforest)
- Date: YYYYMMDD of the event
- Number: sequential per event

**Example:** `SFTF_FR_20260612_2`

## 3. Generate Placard

Run the placard generation script with these parameters:

| Parameter | Description | Example |
|-----------|-------------|--------|
| QR_CODE | The QR code identifier | `SFTF_FR_20260612_2` |
| EVENT_NAME | Event display name | `SF Tech Fest 2026` |
| COLLECTION | Collection name | `Friends of the Rainforest` |
| ORIGIN | Origin text | `Brazilian Amazon Rainforest` |
| LANDING_URL | Short URL for display | `agroverse.shop/friends-of-the-rainforest` |
| MISSION | Mission statement | `Every purchase helps restore 10,000 hectares...` |

**Layout (landscape 1650x1275):**
- Top: Saffron banner with event name
- Left: QR code (570px) with "Scan to support..." below
- Right: Collection subtitle, info box (Origin, Collection, Batch, Web link), mission text
- Bottom: Green band with DAO branding
- Border: Saffron rounded border with corner accents

**Design rules:**
- QR code generated at native resolution (box_size=10, border=4) — never resize
- Agroverse logo embedded in QR center at 22% size
- Text uses word wrap with `draw_wrapped_text()` helper — never let text overflow the right edge
- Info box items: label in gray (140,140,140), value in dark (40,40,40)
- Values truncated with "..." if they exceed available width
- Mission text wraps within `right_w` width

## 4. Upload

Upload the placard PNG to `TrueSightDAO/lineage-assets/pngs/{QR_CODE}_placard.png`:

```python
PUT /repos/TrueSightDAO/lineage-assets/contents/pngs/{QR_CODE}_placard.png
```

If the file already exists, get the SHA first and include it in the update payload.

## 5. Verify

Check the raw URL renders correctly:
```
https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/pngs/{QR_CODE}_placard.png
```

Verify:
- QR code is square and scannable
- No text overflows the right edge
- All text is within box boundaries
- Colors match the brand (saffron #E67E22, green #2E7D32)

## 6. Troubleshooting

| Issue | Fix |
|-------|-----|
| QR code looks squished | Generate at native resolution — never resize the QR image |
| Text overflows right edge | Reduce QR box_size (10→8) to give more room, or reduce font size |
| Text overflows info box | Truncate long values with "..." or reduce font size |
| Mission text cut off | Use `draw_wrapped_text()` with `right_w` as max_width |
| GitHub upload 422 | File exists — get SHA first, include in update payload |
| GitHub upload 403 | Token doesn't have write access — check `TRUESIGHT_DAO_AUTOPILOT` PAT scopes |

## 7. Quick Reference: Full Command

### Using the CLI tool (recommended)

The CLI tool at `/opt/truesight_autopilot/scripts/placard_generator.py` handles PNG generation and GitHub upload in one step:

```bash
python3 /opt/truesight_autopilot/scripts/placard_generator.py \
  --qr-code "SFTF_FR_20260612_2" \
  --event "SF Tech Fest 2026" \
  --collection "Friends of the Rainforest" \
  --origin "Brazilian Amazon Rainforest" \
  --url "agroverse.shop/friends-of-the-rainforest"
```

Use `--dry-run` to test locally without uploading.

## 8. Context for Future AI Incarnations

When a governor asks you to generate a placard for an event:

1. **Check this SOP first** — it has all the parameters and design rules
2. **Use the CLI tool** at `/opt/truesight_autopilot/scripts/placard_generator.py`
3. **Run with --dry-run first** to verify the output, then without for the real upload
4. **The PNG goes to** `TrueSightDAO/lineage-assets/pngs/{QR_CODE}_placard.png`
5. **The raw URL is** `https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/pngs/{QR_CODE}_placard.png`
6. **Always verify** the QR is square and no text overflows the right edge

**Key lessons learned (do not repeat these mistakes):**
- Never resize a QR code image — generate at native resolution
- Always use word wrap for text that could overflow the right edge
- The GitHub API has a 10-property limit on repository_dispatch client_payload
- The qr_codes repo is archived — use lineage-assets/pngs/ instead
- The default GITHUB_TOKEN in workflows can't write to other repos — use a PAT with cross-repo access
