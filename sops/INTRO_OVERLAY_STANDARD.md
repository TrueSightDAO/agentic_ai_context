# SOP — Intro overlay standard (logo + title sizing across masters)

> **Status: PROVISIONAL.** Canonical values below are taken from the newest shipped masters
> (v5–v9). They must be **reconciled against the `100-year-old-trees` master**, which Gary named
> as the visual reference — that master was **not measurable on this box** (see §5).
>
> **Trigger:** building or changing any reel **master** intro frame.
> **Owner of the numbers:** this file. Builders cite it; they do not re-derive.
> **Last measured:** 2026-11-24.

---

## 1. Why this exists

The intro frame is the **first thing a viewer sees and the only frame every master shares**. If its
logo and title sit at different sizes across masters, a channel of reels reads as several brands.

This was measured, not assumed. Three build directories on the autopilot box each rendered their
own intro overlay, with no shared source of truth:

| Build dir | Content band (y) | Side margins (L/R) | Title size |
|---|---|---|---|
| `av_build`, `av_build2` (v1–v4) | `297 → 899` | **186 / 185** | 58px |
| `av_build3` (v5–v9) | `283 → 607` | **253 / 253** | 46px |
| `reel_pacaja` (older session) | `117 → 658` | **125 / 125** | — |

Consequences visible in the numbers:

- The logo's top edge sits at y=297, y=283, or y=117 depending on which build made the master.
- Side margins differ by **2×** (125 → 253), so logos render at different apparent weights.
- Two masters played back-to-back do not match.

**Nothing in the codebase prevented this**, because the numbers had no normative home. Worse:
`build_reel8.py` already cites **"SOP §4"** in a comment for this overlay — and no such section
existed in any repo. This file is that missing section.

---

## 2. The token set

Every intro overlay must be composed from these named parameters. **No magic numbers in a builder.**

| Token | Meaning | Notes |
|---|---|---|
| `MARK_H` | logo mark height in px | governs the logo's visual weight |
| `BADGE` | badge/label block height | below the mark |
| `PAD` | vertical padding inside the band | currently `28` |
| `CY` | y-coordinate of the band's centre | currently `286` |
| `TITLE_PX` | title font size in px | see §4 line limit |
| `MARGIN_MIN` | minimum side margin | floor, not a target |
| `TITLE_MAX_W` | maximum title line width | currently `880` |

> ⚠️ `MARK_H` and `BADGE` are declared in the builders but their exact values were not captured in
> this measurement pass. **Pin them in §3 when the standard is locked** — do not leave them implicit.

---

## 3. Canonical values (PROVISIONAL — see §5)

Taken from `build_reel8.py` / the v5–v9 masters, the newest and tightest geometry in circulation:

| Parameter | Value | Evidence |
|---|---|---|
| `CY` | `286` | declared in builder; measured content starts y=283 |
| `PAD` | `28` | declared in builder |
| `TITLE_PX` | `46` | declared in builder |
| `TITLE_MAX_W` | `880` | declared in builder |
| `MARGIN_MIN` | `90` | declared as a floor; measured actual 253 |
| `MARK_H` | **to be pinned** | declared, value not captured |
| `BADGE` | **to be pinned** | declared, value not captured |

**Measured result of this set** (agroverse, 1080×1920):

- content band `y 283 → 607`
- side margins `253 / 253` (perfectly symmetric)
- title block gap `440 → 479`

F5 renders narrower (`y 283 → 571`, margins `373 / 373`) because Chinese glyphs at the same px size
occupy less advance width. **This is expected and correct** — the band top (`283`) and centre (`286`)
must match across markets even though the text width differs. Match the **band**, not the width.

---

## 4. Rules

1. **One source of truth.** Builders read these tokens; they never hardcode a px value.
2. **Title: maximum 2 lines.** A third line breaks the band and pushes captions into the UI.
3. **`MARGIN_MIN` is a floor.** Text must never come closer than this to either edge. Assert it.
4. **Symmetric margins.** Left and right must match within 2px. Asymmetry is a bug.
5. **Band alignment is cross-market.** The agroverse and F5 variants must share `CY` and band top,
   even though rendered text widths differ.
6. **Logo crop guard.** Never resize the logo non-integrally or crop its mark; the `LOGO_CROP` box
   protects the mark's aspect. A crop that clips the mark is a failed render, not a stylistic choice.
7. **Assert before encode.** Any build must assert the above and abort — not warn — before spending
   minutes on an encode:

```python
assert abs(margins["L"] - margins["R"]) <= 2,          "asymmetric side margins"
assert min(margins["L"], margins["R"]) >= MARGIN_MIN,  "text inside margin floor"
assert band_top == CANON_BAND_TOP,                     "band not aligned to standard"
assert title_lines <= 2,                               "title exceeds 2 lines"
assert tw1 <= TITLE_MAX_W,                             "title line too wide"
```

---

## 5. ⚠️ Open reconciliation — the 100-year-old-trees master

Gary named the **`100-year-old-trees` master** as the reference whose logo and font sizes "seem
appropriate". **Those numbers were not measured**, because that master is not present on the
autopilot box. What was searched, and came back negative:

| Search | Result |
|---|---|
| `/media/media_masters/` | only `pacaja-roast/` — no trees master |
| Whole-disk `*master*` / `*share*` / `*reel*` filename sweep | no trees/100 candidates |
| Builder scripts mentioning trees / arvore / hierarchical | none relevant |
| `/tmp/canon_render.py` | is a **SunMint certificate** renderer, unrelated |
| Transcript history (`search_transcript`) | no such attachment |
| Repo code search | no such asset |

Therefore the values in §3 are **the current shipped set, not a measured match to the reference.**
They are adopted provisionally because they are the newest and tightest, and because leaving the
question open keeps three geometries alive.

**To close this:** supply either (a) the trees master file, or (b) a single frame grab of its intro,
and the numbers in §3 get overwritten with the measured reference values. Until then, no new master
should claim this standard as final. **Never write numbers into this table that were not measured
from an artifact someone can point at.**

---

## 6. Relationship to the artifact ladder

The intro overlay is a property of the **Master** rung (`MEDIA_ARCHIVE_PIPELINE.md` § *Terminology*):

- A **master** carries its own rendered intro. The overlay is baked in, not a separate layer.
- **Share copies** inherit the master's overlay unchanged — never re-render the intro for a share copy.
- Changing the overlay means a **new master** (v8 → v9), not a patch to a share copy.

---

## 7. Checklist before encoding a master

- [ ] Tokens read from this file, none hardcoded
- [ ] Band top and `CY` match §3
- [ ] Side margins symmetric within 2px, both ≥ `MARGIN_MIN`
- [ ] Title ≤ 2 lines, no line wider than `TITLE_MAX_W`
- [ ] Logo mark not clipped by `LOGO_CROP`
- [ ] agroverse and F5 variants share band top even if widths differ
- [ ] Assertions placed **before** the encode call
- [ ] If `MARK_H` / `BADGE` are still unpinned, pin them here in the same PR

---

## 8. References

- `MEDIA_ARCHIVE_PIPELINE.md` — artifact ladder (clip / beat / segment / cut / variant / master / share copy / reel) and the QC gate
- `sops/INSTAGRAM_CAPTION_SOP.md` — caption register; the caption must not contradict the on-screen text
- `growth/CMO_SETH_GODIN.md` — consistency builds trust
