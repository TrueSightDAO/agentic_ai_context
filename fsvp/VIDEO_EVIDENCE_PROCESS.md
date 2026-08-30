# Video evidence analysis for FSVP site visits

How to turn short phone videos (.MOV / .mp4) from a farm site visit into FDA FSVP
inspection-record evidence, the same way it was done for the **Santa Anna Fazenda**
visit (2026-08-30, `walk in the forest.MOV`).

## When to use

A governor attaches a video recorded during a site visit (walking the cacao farm,
fermentation area, drying shed, sorting). Still photos alone don't capture the
continuity of a walk-through; frames from the video supplement them.

## Prerequisites on the autopilot box

- `ffmpeg` / `ffprobe` (installed)
- Grok vision via `app/grok_client.py` (`grok_analyze_images`) with a valid key in
  `/opt/truesight_autopilot/.env`

## Pipeline (validated 2026-08-30)

### 1. Locate + probe the video

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,r_frame_rate -of json "/home/ubuntu/<file>.MOV"
```

Record: duration, codec, resolution, fps, size. This metadata goes into the PDF
caption block (e.g. "7.7s, 1920x1080, 30fps").

### 2. Extract frames with ffmpeg @ 4fps

```bash
mkdir -p /tmp/forest_frames && cd /tmp/forest_frames && rm -f frame_*.jpg
ffmpeg -y -v error -i "/home/ubuntu/<file>.MOV" -vf "fps=4" frame_%03d.jpg
```

4fps is the sweet spot for an ~8s clip: ~31 frames, enough coverage without
redundancy. Adjust up for longer clips if a key scene would be missed.

### 3. Grok vision batch analysis

Load the env, then call `grok_analyze_images` in batches of 8:

```python
from grok_client import grok_analyze_images
ctx = ("Frames from a ~8s video recorded during a CEPOTX cacao farm site visit in the "
       "Brazilian Amazon. Describe each scene briefly; flag good FDA FSVP evidence "
       "(drying shed, fermentation box, cacao pods/trees, sorting).")
res = grok_analyze_images(frames, user_context=ctx)
# res["frames"][i] = {frame, description, fsVP_evidence}
```

What to look for per facility:

| Facility | Evidence frames |
|---|---|
| A — cacao farm | pods on trunk, canopy walk, harvesting practice |
| B — fermentation | wooden fermentation box, dedicated house |
| C — drying | beans spread on drying-shed floor, turnover |

### 4. Select representative frames

Pick 2–3 per facility: one establishing shot + one close-up + one action shot
(e.g. hand on pods). Prefer frames where `fsVP_evidence: true`.

### 5. Embed in the site-visit PDF

In the reportlab generator (`gen_santa_anna.py` pattern):

```python
from reportlab.platypus import Image
E.append(Paragraph("Video evidence frames \u2014 Facility A (cacao farm walk)", h1))
E.append(Paragraph("Extracted from <file>.MOV (7.7s, 1920x1080, 30fps) \u2014 31 frames at 4fps, 3 representative frames shown.", body))
for path, cap in frames:
    E.append(Paragraph(cap, body))
    E.append(Image(path, width=5.4*inch, height=4.05*inch))
```

### 6. File the record

Per `SITE_VISIT_PROCESS.md`: PR the PDF into `fda_fsvp/suppliers/<supplier>/`,
update `entity.json` `source_farms` / `source_documents`, then merge.

## Gotchas

- **The .MOV may not land in `/tmp/tg_attachments`** with the stills. Ask the
  governor to `scp` it to `~/` if the attachment didn't arrive, or check
  `/tmp/tg_attachments/` and `~/` before assuming it's lost.
- **Grok may return a whole-clip summary** instead of per-frame entries when the
  batch is too large or the API throttles — retry in smaller batches (4–8) or
  single frames.
- **No GPS EXIF in phone videos** — geo-location for the PDF must come from the
  governor (or a map lookup), not from the video.
- **Frames are large** (~400–550 KB each) — only embed the selected few; don't
  upload the whole extract set.

## Output contract

A site-visit PDF that contains, alongside the still photos:
- a "Video evidence frames" section naming the source file + probe metadata
- 2–3 captioned frames per facility
- cross-references in the Observations tables (e.g. "see video frame 1")
