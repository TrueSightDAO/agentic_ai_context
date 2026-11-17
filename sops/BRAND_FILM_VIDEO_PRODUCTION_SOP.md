# SOP — Brand Film Production & QC (`BFP`)

> **Official document class: BRAND FILM PRODUCTION (`abbrev. BFP`).** Use this name when
> referring to the end-to-end produce-and-QC workflow for a TrueSight DAO / Agroverse film.
>
> **Applies to:** any short brand film assembled from archive footage — animatics,
> storyboards-to-motion, product hero cuts.
>
> Filed **2026-11-11** after the Agroverse brand-film build (Gary + Sophia) took **six
> rebuilds** to converge. Every rebuild was caused by a defect this SOP now prevents.
> Governor: Gary Teh. Author: Sophia Truesight.
>
> **Extended 2026-11-17** (§2.4, §7A) after the Agroverse *"Where Flavor Is Decided"*
> Instagram Reel. A delivered cut shipped captions clipping **114 px off each edge**, over a
> title that promised content the footage did not contain — and the session's three "proofs"
> of correctness were all false. Details in §7A.4 and §7A.5.

---

## 0. The headline rule

> **Never let a vision model's claim go straight into an edit.**
> Resolve every pick to a **file**, then **verify the file itself** — full frame, at the
> timestamp you will actually use.

> **And every film ends on a brand endcard built from the site's design tokens (§6.3).**
> No dark plate, no invented colour, no cold stop on footage. Wrap every cut — always.

> **And no text crosses the safe area — ever.** Captions and titles are measured, wrapped and
> **asserted** before the render, never hand-positioned (§7A).

Of the six failed builds on 2026-11-11, **two** came from skipping exactly that step. Details
in §4.

---

## 1. Beat structure — fix it before sourcing anything

Write the beat sheet as a table **before** touching ffmpeg. Every beat needs: time range,
intended subject, and **what would prove the subject is present**. Example from the shipped cut:

| t | Beat | Must show |
|---|---|---|
| 0.0–3.0 | Product | Chocolate bar, overhead → push-in |
| 3.0–4.0 | Aerial | Canopy + river |
| 5.0 | People | Person working the plot |
| 6.5 | Planting | Seedling + stake in open ground |
| 9.5 | Maturity | **Mature cacao — pods on trunk** |
| 11.0–12.5 | Endcard | Logo on brand-correct background |

A beat without a falsifiable "must show" is the beat that ships wrong.

---

## 2. Sourcing footage from the archive

### 2.1 Do NOT prefilter by colour for cacao

The instinct is to screen for "green" clips. **This is the wrong instrument for cacao.**
Cacao is a **dark understorey canopy with brown trunks** — it scores *poorly* on green
dominance. The green sweep on 2026-11-11 surfaced palms and grass while missing every cacao
stand.

**Do this instead:** sample **unfiltered** across the archive. On the session that finally
worked, an unfiltered sample of **80 clips → 79 tiles** found real cacao in one pass.

### 2.2 Field-note: the `cacau-na-veia` folder is not what its name promises

A folder named after cacao (`pacaje_work/pr4_assets/cacau-na-veia-pacaje/`) contained mostly
**people, fermentation sheds, and drying beds**. Gemini rejected all 12 sampled frames:
*"None of the frames clearly feature a mature cacao tree as the primary subject."*

**Folder names describe provenance, not frame content.** Always sample and look.

### 2.3 Use streaming shell for large media scans

A Python per-file colour screen **timed out at 290 s** over 1,769 clips. The equivalent `awk` /
shell one-pass loop completed in a single call. For archive-scale scanning, prefer streaming
shell over Python subprocess-per-file.

### 2.4 Source originals over public HTTPS — a credential test is not an access test

S3 originals under `media.agroverse.shop` are **public-read**. No credentials are required:

```bash
curl -sI "https://s3.us-east-1.amazonaws.com/media.agroverse.shop/raw/<farm>/<file>.MOV"
# HTTP/1.1 206 Partial Content   -> range supported: resumable, seekable
```

On 2026-11-17 a session probed the archive with `aws s3 ls` and boto3, got
`NoCredentialsError`, and concluded *"the archive is unreachable, therefore this footage does
not exist"* — then recommended **changing the content plan** on that basis. The footage was
downloadable the entire time. The lesson is general:

> **A credential failure proves you lack credentials. It does not prove the object is
> unavailable (Rule 11).** Test the public URL before concluding a resource is missing —
> and before recommending a plan change that depends on the gap being real.

**Probe path variants too.** One clip lived at `raw/sitio-torres-pacaja-para/` (folder spelled
out) while its manifest slug was `sitio-torres`. A single exact-path attempt would have missed
it; folder names describe provenance, not identity (§2.2).

---

## 3. Building contact sheets and querying vision models

### 3.1 Make tiles, keep a manifest, never lose the mapping

```bash
# extract 1 frame per clip at a safe seek point
# build contact sheets of N tiles each
# WRITE A MANIFEST: tile index -> absolute source path
grep -E '^<idx> ' tiles.list.txt
```

The manifest is the **only** bridge from a vision model's answer back to a real file. Without
it, a tile index is meaningless.

### 3.2 Ask for botanical identity, not a vibe

| ❌ Weak prompt | ✅ Strong prompt |
|---|---|
| "Is this good for the reforestation beat?" | "Identify the plant species. Does it show **jorquette branching**, oblong leaves, **pods on the trunk/limb**? Answer `is_cacao: true/false` with a confidence." |

A vibe question returns a vibe answer. On 2026-11-11 a vibe-graded frame turned out to be a
**dwarf coconut palm** — the model only named the mismatch when asked directly for species.

### 3.3 Timestamp traps

- **Seek points fail silently.** In one 33-clip folder only **9** yielded frames at the chosen
  seek offsets. Re-extract with safer seek points (e.g. `-ss` after input, or lower offsets)
  rather than assuming those clips are empty.
- **Sample several timestamps per clip and pick the best.** The first acceptable cacao frame was
  graded *"litter_dominated: true"* (dead leaves filling the bottom third). Probing **10
timestamps** in the same clip found **t=6.5 s at grade 8/10** — *"clear cauliflory… higher angle
that keeps dead ground litter from dominating."* The clip was fine; the timestamp was wrong.

---

## 4. The three verification failures this SOP exists to prevent

### 4.1 Tile indices get hallucinated

A vision model returned candidates `g0`, `g16`, and **`g79`** for a contact-sheet range of
**`g0…g78`**. **`g79` does not exist.** Only `g0` and `g16` were real.

**Rule:** validate every returned index against the manifest **and against the sheet's actual
range** before use. Silently mapping a phantom tile to "the nearest real file" is how the wrong
footage enters a cut.

### 4.2 A vision "best pick" can be flatly wrong — check the full frame

A model's top pick (tile 51) was built into a 2.5 s beat. QC on the built clip returned:
*"unidentifiable cut stump / wild grass."*

Checking the **full uncropped photo** against the crop:

```
A (full photo):  {"has_cacao": false}
B (center crop): {"has_cacao": false}
```

**There was no cacao in that photo at all**, cropped or not. The pick was a misfire on a
contact sheet.

**Rule:** verify a pick on the **full frame**, not a tile, and not a crop. Confirm the subject
before spending a render.

### 4.3 A cross-dissolve is not a glitch

QC flagged a frame as *"severe ghosting glitch — chocolate packaging bleed."* A dedicated
**5-frame probe across that transition** returned every frame as `normal_blend`, with
`any_genuine_artefact_after_fade_completes: false`.

The camera grid had simply sampled at **t=2.9 s — inside the fade**. The frame was a normal
cross-dissolve.

**Rule:** when QC reports an artefact at a known transition, **probe the transition** with a
dense frame series before "repairing" anything. Repairing a non-defect costs a rebuild and can
introduce a real one. Verdict flips to PASS when probed properly — as it did here.

---

## 5. Paperwork masquerading as content — check the *endcard* too

Two builds shipped the wrong subject because nobody asked "what is actually in this frame?":

| Build | What the beat was supposed to be | What it actually was |
|---|---|---|
| V2 `A5a.mp4` endcard | Brand logo | **A person holding a table / paperwork** |
| V2 beat 5 | Reforesting / regrowth | **A hand-held "Classificação do Cacau" form** with logo bleed, zero trees |

Both were caught only by running Gemini over **all** the candidate endcard clips and asking for
a plain description of each tile:

> `i:1 "Person holding paperwork table"` ← in use
> `i:2 "Clean Agroverse logo endcard with tree emblem and tagline"` ← **correct**

**Rule:** QC the **endcard** with the same rigour as the picture. Ask "describe what is in this
frame", not "does this look like a logo?" — a leading question gets a leading answer.

---

## 6. Brand tokens — read them, never invent them

Backgrounds, inks, and logo variants are **specified in the site repo**. Read the `:root` block:

```bash
curl -s https://raw.githubusercontent.com/TrueSightDAO/agroverse_shop_beta/main/index.html \
  | grep -iE -- '--color-|logo img|<body' | head -30
```

**Agroverse tokens (as of 2026-11-11, `agroverse_shop_beta/index.html` `:root`):**

| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#ffffff` | Page background |
| `--color-bg-light` | `#f7f7f7` | Header / light panels |
| `--color-primary` | `#3b3333` | Body ink |
| Logo gold | `#ffb020` | The site's actual emblem colour |

**And the rule that settles most endcard arguments:**

```css
.logo img { background: white; }
```

The site puts the logo on **`#ffffff`**.

### 6.1 The measured failure

An endcard was built on **`#f9f9f4`** — a cream invented by eye. It passed a casual glance and
was **off-spec**. Caught by the governor, not by QC.

**Rule:** sample the actual pixel (`#%02x%02x%02x` of a corner) and compare it to the token
before shipping. "Close enough" is how brand drift starts.

### 6.2 Two logo variants exist — pick deliberately

| Asset | Colour | Behaviour |
|---|---|---|
| Wordmark variant | **near-black ink** (mean luma ≈ 29.6) | **Invisible on dark** — this caused the original "logo doesn't show up" complaint |
| `favicon-192x192.jpeg` | **gold `#ffb020`** (18,453 px of that exact hue) | The site's real header emblem |

**Dark background + black-ink logo = invisible.** If a logo disappears, check ink colour
before changing the background. And if the gold emblem is needed at size, source a **vector or
high-res** file — the favicon is only 192×192 and goes soft when scaled.

### 6.3 The standard endcard — MANDATORY final frame

> **Rule (approved by the governor 2026-11-11): every brand film ends on a brand endcard
> built from the site's own design tokens.** No dark plate, no invented colour, no
> footage-only cold stop. This is not optional styling — it is the brand close.

**Why this is a rule and not a preference:** the endcard is the last thing a viewer sees and
the only frame guaranteed to be on screen long enough to read. A dark plate swallowed a
black-ink logo entirely ("the logo doesn't show up clearly"), and an eyeballed cream
(`#f9f9f4`) drifted off-spec. Both defects were in the *final frame* — the frame with the
least excuse for being wrong.

#### The recipe

| Element | Spec | Source of truth |
|---|---|---|
| Background | **`#ffffff`** (`--color-bg`) | `agroverse_shop_beta/index.html` `:root` |
| Alternate plate | `#f7f7f7` (`--color-bg-light`) | same |
| Logo | **gold `#ffb020` emblem** (site header mark) | `assets/images/logo/favicon-192x192.jpeg` |
| Body / tagline ink | **`#3b3333`** (`--color-primary`) | same |
| Composition | Logo centred, tagline directly beneath | — |
| Hold | **≥ 2.5 s**, ideally 3.0 s, after the last picture beat | §6.3.2 |

**Default treatment = the site's own header pairing: gold emblem on a `#ffffff` plate.** If the
governor picks a different token-valid variant, record the choice in the deliverable notes; do
not quietly substitute a similar-looking colour.

> **The site settles it:** `.logo img { background: white; }` — the canonical pairing is the
> logo on **white**. Any endcard that is not built on a site token is off-spec by definition.

#### 6.3.1 Mandatory verification before the endcard ships

- [ ] Sample the actual corner pixel and print it as `#%02x%02x%02x` — it must **equal** the token
- [ ] Confirm logo ink vs background gives real contrast (a black-ink mark on dark = invisible)
- [ ] Gemini: `endcard_on_white: true`, `logo_clear: true`, `tagline_legible: true`
- [ ] Confirm the tagline reads correctly **character-for-character** (OCR/vision misreads brand
      copy more often than it misreads pictures)
- [ ] `burned_in_third_party_text_or_logo: "none"` — a logo over someone else's form is a fail

#### 6.3.2 Hold length — the endcard must be readable

A 0.5 s endcard is a flash frame, not a brand close. Reserve **≥ 2.5 s** (3.0 s preferred) of
the total runtime for the card, **after** the final picture beat. If the cut is time-boxed,
shorten a middle beat — never the endcard.

#### 6.3.3 The endcard is content — QC it like content

Do **not** QC the endcard with a leading question ("does this look like a logo?"). Ask
**"describe what is in this frame"** across *all* candidate endcard clips first. A leading
question is how a person holding paperwork got shipped as our brand close (§5).

---

## 7. Rendering: never let a timeout truncate a write

An ffmpeg render killed by a tool timeout leaves a **half-written MP4**:

```
[mov,mp4,m4a] moov atom not found
A4c.mp4: Invalid data found when processing input
```

**Rule:** for any render that could plausibly exceed the tool timeout, launch it detached and
poll:

```bash
nohup ffmpeg -y ... > build.log 2>&1 &
# then, separately:
ffprobe -v error -select_streams v -show_entries stream=nb_frames,width,height \
        -show_entries format=duration -of default=nw=1 OUT.mp4
```

**Never treat a file as usable until `ffprobe` confirms `nb_frames` and `duration`.** A
successful exit code is not proof — a killed process can leave a plausible-looking file.

---

## 7A. Captions & titles — make overflow structurally impossible

> Filed 2026-11-17 after the *"Where Flavor Is Decided"* Agroverse Reel. The cut was
> delivered with **6 of 14 caption lines running off both edges** — up to **114 px clipped per
> side** — and every check that had been run passed it.

### 7A.1 The cause: `drawtext` has no width constraint

This looks correct and is not:

```bash
drawtext=text='…':fontsize=58:x=(w-text_w)/2:box=1:boxcolor=black@0.45:boxborderw=28
```

`x=(w-text_w)/2` **centres** a line; it does not **fit** it. When `text_w > w` the line is
centred *past both edges* and `ffmpeg` clips it silently — no warning, no non-zero exit.
`boxborderw=28` then paints another **56 px** of background beyond the glyph extent, so the
visible overflow is worse than the text metrics alone suggest.

**Sizing the box is the whole job, and the box is `boxborderw*2 + text_w`.**

### 7A.2 The rule: render captions as PNG overlays, with a hard assertion

Measure with real font metrics, wrap, auto-shrink — then **abort the render** if anything
crosses the safe area:

```python
from PIL import ImageFont
SAFE    = 90            # px each side, 1080-wide portrait
CONTENT = W - 2 * SAFE  # 900

def fit(lines, fontpath, start):
    fs = start
    while fs > 18:
        f = ImageFont.truetype(fontpath, fs)
        if all(f.getbbox(l)[2] - f.getbbox(l)[0] <= CONTENT for l in lines):
            return f, fs
        fs -= 1
    raise SystemExit("caption cannot fit")

# …draw onto a transparent 1080x1920 RGBA canvas, then:
l, t, r, b = img.getbbox()
assert l >= SAFE and (W - r) >= SAFE, f"OVERFLOW left={l} right={W - r}"
```

Then `overlay=0:0` the PNG onto the beat. Because the overlay is placed **unmodified at the
origin**, the PNG's `getbbox()` **is** the on-screen extent — which is what makes the
verification in §7A.4 sound.

Measured on that build: worst-case margin went from **−114 px (clipped)** to **+91 px (clear)**,
max line width **897 of 1080**. Apply the same assertion to the **endcard/outro** text, which is
usually drawn separately and is easy to forget.

### 7A.3 Portrait / Reel geometry

- Target **1080×1920, 30 fps, yuv420p, `-video_track_timescale 15360`** on every segment.
  Identical params are required for a stream-copy concat (§8).
- Keep text out of the **Reels UI zones**: roughly the bottom ~250 px (caption/CTA overlay) and
  the right ~120 px (action rail). A band starting at y≈1140 with the last glyph below y≈1560
  cleared Instagram's overlay in testing — **confirm on the published post**, not just locally.
- Sourced phone footage often reports `1920×1080` **with `rotate=90`** — it is already portrait.
  Do **not** transpose it, and do not infer landscape from the raw width/height.

### 7A.4 Verify on the RENDERED frames — and don't trust these three proxies

The source PNG being correct says **nothing** about what got composited. Pull a frame from the
**final concatenated file** and check it there.

Three methods that produced **false verdicts** on the 2026-11-17 build. All three looked
authoritative:

| ❌ Method | Why it lies |
|---|---|
| **Bright-pixel extent** over the frame | Counts sunlit foliage, white shirts, sky. Reported *“CLIPPED, L=0”* on all 7 beats **and** *“173 text pixels”* in a left strip where no caption pixel existed. Wrong in both directions. |
| **OCR at downscaled resolution** | A 540-px downscale OCR'd poorly and reported a beat as having **no subtitle at all**. At full resolution the text was present. OCR false-negatives on small text over busy backgrounds. |
| **Frame diff at mismatched timestamps** | Diffing a segment frame at t=2.0 s against a source frame from a *different* moment differences the whole scene, so every beat reads as “clipped”. |

✅ **Do instead:**

1. **Geometry** — read `getbbox()` off the caption PNG (valid because of the `0:0` overlay): the
   authoritative on-screen margin.
2. **Legibility** — OCR a **full-resolution crop** of the caption band (never downscaled) and
   diff the returned string against the intended text.
3. **Presence & continuity** — per-beat `ffprobe` plus `volumedetect`. A silent beat is a
   production bug the picture checks will not catch, and `-v error` **hides** `volumedetect`
   output (it logs at info level) — an empty result there means a broken probe, not silence.

### 7A.5 The title must be falsifiable against the beats

A cut shipped titled **“28 FLAVOR WORLDS”** over footage of farmers explaining four *farm
decisions*. Nothing in the archive showed anyone tasting 28 anything — the title promised a
catalogue the footage never delivered. **The governor caught it; QC did not.**

**Rule:** every line on the endcard/outro must map to a **specific beat that shows it.** Put the
mapping in the beat sheet (§1):

| Outro line | Beat | Proof |
|---|---|---|
| Commodity or selected | b0–b1 | `cacau-na-veia` IMG_9556 |
| Fermented hot or cool | b2 | `santa-ana` IMG_8072 |
| Roasted at 120 °C | b3 | `sitio-torres` IMG_9697 |

If a line has no beat, **change the line** — never widen the claim to cover weaker footage. And
if the claim comes from the content-calendar row, treat it as unverified too: the row for this
Reel described flavor *tasting notes* for footage that was actually about flavor *determinants*.

### 7A.6 ASR subtitles are not publishable text

`faster-whisper` output is a **translation**, not a quote. Observed in a single pass:
`cacau → “cow”`, `amêndoas → “amênd”`, `optou → “opitou”`.

- **Never** put ASR text on screen as a quotation until a speaker of the source language has
  checked it.
- **Numeric claims are a hard gate.** *“120 °C / 25–30 min”* is an instruction a viewer may act
  on; an ASR mishear there is a correctness bug, not a typo.
- Where possible render **source-language subtitles** with the translation beneath, so nothing
  is translation-mediated.

---

## 8. Stitching

- Keep **every beat as its own encoded clip** at identical geometry/fps before stitching.
  Mismatched inputs are the main cause of broken `xfade` chains.
- Target a **single consistent** `width,height,fps` across all beats (e.g. `1280,720,24/1`).
- Verify the total duration against the arithmetic sum of beats **minus** overlap:
  `total = sum(beats) − (n−1) × fade`
- Re-verify after stitch: `nb_frames`, `duration`, geometry.
- If a constituent clip is missing from disk, **rebuild it from its validated source** — do not
  substitute a similar-looking clip.

---

## 9. QC gate before delivery

Run a **frame grid across the whole cut** and ask for a structured verdict. Minimum fields:

```json
{
  "verdict": "PASS | FAIL",
  "arc_reads_correctly": true,
  "beats_present": [ ... ],
  "burned_in_third_party_text_or_logo": "none",
  "logo_endcard_ok": true,
  "cacao_beat_present": true,
  "quality_problems": []
}
```

**Ship only on `verdict: PASS` with an empty `quality_problems`.** Then and only then compress
for delivery (a Discord/Telegram attachment cap is typically 25 MB).

---

## 10. Rights / provenance — a hard gate, not a footnote

**Every third-party clip in the cut needs confirmed provenance before public release.**
Layering a clean music licence onto uncleared footage does not make the piece clean.

- [ ] List every clip not shot by us
- [ ] Confirm we have rights (licence, release, or ownership) **in writing**
- [ ] Note de-branding applied (logos blurred/cropped) and that it does not create a
      derivative-works problem
- [ ] Keep the answer attached to the film's QC record

On 2026-11-11 the **Neofloresta aerial clip** went into a PASSING cut while its provenance was
still unconfirmed. It was flagged every cycle and never silently accepted.

---

## 11. Rebuild log — the honest scoreboard

The 2026-11-11 build converged on the **sixth** attempt. Each rejection was a **real defect**:

| Version | Defect | Caught by |
|---|---|---|
| V2 | "Regrowth" beat was a classification form | vision QC |
| V2 | Endcard was a person holding paperwork | all-candidates QC |
| V4 | Beat 5 was a coconut palm, not cacao | species-specific prompt |
| V5 | Cacao pick had no cacao in it at all | full-frame check |
| V6 | Endcard background `#f9f9f4` vs spec `#ffffff` | **governor** |
| **V6 final** | — | **PASS, `quality_problems: []`** |

**Keep this table in the deliverable record.** A build that took six attempts is not a failure
of process — hiding that it took six is.

---

## 12. Quick checklist

- [ ] Beat sheet with falsifiable "must show" per beat
- [ ] Unfiltered archive sampling (no colour prefilter for cacao)
- [ ] Tile → file manifest kept; every vision index validated against real range
- [ ] Species asked for explicitly, with confidence
- [ ] Full **uncropped** frame verified for every pick
- [ ] Best timestamp probed per clip (≥6–10 samples)
- [ ] Transitions probed densely before accepting an "artefact" verdict
- [ ] **Endcard present as the final frame**, built on a site token (§6.3) — `#ffffff` default
- [ ] **Endcard holds ≥ 2.5 s** after the last picture beat (§6.3.2)
- [ ] Endcard QC'd with "describe what is in this frame" across all candidates
- [ ] Tagline verified character-for-character
- [ ] Brand tokens read from `index.html :root`; corner pixel sampled and compared
- [ ] Logo ink colour checked against background
- [ ] Renders detached + `ffprobe`-verified (frames, duration, geometry)
- [ ] Arc QC returns **PASS** with empty `quality_problems`
- [ ] Third-party clip provenance confirmed before public release
- [ ] Music licence logged (§ BFM SOP §6)
- [ ] Rebuild log included in the deliverable record
- [ ] Captions/titles rendered as **measured PNG overlays** with a safe-area `assert` (§7A.2) — endcard text too
- [ ] No line exceeds the safe area, verified on **rendered** frames from the final concat (not the source PNG) (§7A.4)
- [ ] Portrait geometry confirmed (1080×1920 @30, `timescale 15360`); `rotate=90` honoured, **not** transposed (§7A.3)
- [ ] Every outro/endcard line mapped to a beat that actually shows it (§7A.5)
- [ ] ASR subtitles checked by a source-language speaker; numeric claims verified (§7A.6)
- [ ] **Every beat has audio** — `volumedetect` at info level, not `-v error` (§7A.4)
