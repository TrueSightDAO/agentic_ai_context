# Print-on-Demand Mockup Generation

**Read this** when generating packaging mockups for Agroverse — chocolate bars, pouches, or labels — especially before spending money or renders on a third-party image-generation API.

**Status:** trial-stage. The engine works, the brand-fidelity workaround is settled, but this is **not** wired into any production funnel yet.

---

## TL;DR

1. Use **gotde.cn** to render a photoreal *packaging* mockup. Ask it for **no wordmark**.
2. **You can pass the mark in** (`logo_base64` + `logo_position` + `logo_width_ratio`) — but placement is *best-effort*, not pixel-exact. For print, still **composite the real Agroverse mark ourselves** (Approach A, below). The engine cannot render our typeface and draws counterfeit letterforms if asked.
3. Log the `record_id` of every render — the vendor exposes no quota or history API, so **our log is the only spend record**.

---

## Canonical Agroverse bar dimensions

Measured from actual product photography; use these everywhere (POD, white-label print files, label design):

| Dimension | Value |
|---|---|
| Bar | **81 mm × 163 mm** = 3.19" × 6.42" |
| Bag | **2.05" × 4.0"** |
| Print area | **2.0" × 4.0"** |
| Bbox aspect ratio | **0.513** (2.05 : 4) |
| Packaging photo reference | `agroverse_shop_beta` → `assets/images/products/81-dark-chocolate-bar-50g-packaging.jpg` |
| Measured label bbox on that photo | `x1190–1457, y221–741` → 267 × 520 px |

An earlier draft spec used a 4" × 2" **landscape** bar. That is **wrong** — it contradicts both the photograph and the physical product. Portrait only.

---

## The gotde.cn engine

### Credentials

API key is held in the autopilot vault as **`gotde_package_api`** (scopes: `image_generation`, `packaging_mockup`, `white-label-preview`).

```python
from app.vault import Vault
KEY = Vault().get_value("gotde_package_api")
```

Never write the key into a `.env`, repo, log, or doc. Vault only.

### ✅ Transport — HTTPS (certificate renewed)

Verified 2026-11-19: HTTPS works, and the certificate is valid **2026-11-17 → 2027-02-15**.

- Working host: **`xiaodeapi.gotde.cn`** — use HTTPS.
- An earlier revision of this doc said "HTTP only / the key travels unencrypted" — that described a certificate which **expired 2026-11-17 and has since been renewed**. If you hit a TLS failure, re-read the live certificate dates; do not assume this note is current.
- `package.gotde.cn` (the host named in their own docs) is still worth avoiding; `xiaodeapi.gotde.cn` is what we have verified.
- **Multipart is rejected outright.** The endpoint takes `application/json` only. `multipart/form-data` returns `400 Input should be a valid dictionary or object` **even with no file attached** — verified as a control. So artwork cannot ride along as a file part; use `logo_url` / `logo_base64`.

### Endpoints

| Endpoint | Method | Notes |
|---|---|---|
| `/api/v1/templates` | GET | **Public, no key.** `?page=&pageSize=100&include_base_map=true`. Paginate until `total`. |
| `/api/v1/open/package-generate` | POST | Requires `X-API-Key`. **This is the only generation path.** |

There is no spec at the domain root and no `/docs` / `/redoc` (`/openapi.json`, `/api/openapi.json`, `/docs`, `/redoc` all 404) — **but the real OpenAPI document is served at `/api/v1/openapi.json`** (HTTP 200, ~669 KB, 326 paths, `AiCanvaPy 1.0.0`). Fetch it before touching this API: every schema fact below is verifiable there.

> **Method lesson — read the spec, do not probe by guessing.** An earlier revision of this runbook concluded "there is no spec" and recovered the schema by type-bombing field names. That produced two confident, **wrong** conclusions (see the retraction in §1). FastAPI silently ignores unknown keys, so a `200 OK` on a type-bomb proves nothing at all, and a guessed name that fails tells you only that *your guess* was wrong — never that the field is absent.

### Generation request

```python
body = {
    "template_id": 492,
    "design_coverage": "label",        # "label" | "full"
    "background": "white",             # "white" | "kraft" | "gray"
    "width_in": 2.05, "height_in": 4.0,
    "print_width_in": 2.0, "print_height_in": 4.0,
    "extra_requirements": "..."        # free-text prompt
}
# POST with headers {"Content-Type": "application/json", "X-API-Key": KEY}
# -> {"record_id": int, "image_url": "<signed, expires fast>"}
```

**Download `image_url` immediately** — signed links expire within minutes.

### Logo input and placement — the fields that DO exist

`PackageGenerateRequest` has four logo fields, verified against `/api/v1/openapi.json` and exercised live (rec=59–64).

| Field | Constraints | Meaning |
|---|---|---|
| `logo_url` | string, ≤2048 chars, png/jpeg/webp | Public http(s) URL of the mark |
| `logo_base64` | string, ≤12,000,000 chars | Raw base64, optional `data:image/…;base64,` prefix. Mutually exclusive with `logo_url` |
| `logo_position` | `top-left`, `top-center`, `top-right`, `center-left`, `center`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right` | Default **`bottom-center`** |
| `logo_width_ratio` | number, **0.05 – 0.60** | Default **`0.22`** |

```python
body["logo_base64"] = "data:image/jpeg;base64," + base64.b64encode(open(mark_rgb, "rb").read()).decode()
body["logo_position"] = "bottom-center"
body["logo_width_ratio"] = 0.22
```

Use `logo_base64` whenever the mark is not publicly hosted — that is our case. A 102 KB source JPEG encodes to ~137 KB of base64, far inside the 12 MB cap.

> ⚠️ **These are generative controls, not layout controls.** The vendor's own schema text says the logo is passed to the model as a reference image and the position/size is written into the prompt: *"生成式控制，位置为'尽力对齐'而非像素级精确"* — generative control, position is best-effort, **not pixel-precise**. The response echoes back `logo_url` and `logo_position`, but **an echo is not proof the mark was drawn there — check the pixels.** For print-critical output, keep Approach A (deterministic composite) as the final step.

### Schema facts, verified

- **Strict validation.** Missing `template_id` → `400 {"success":false,"message":"Field required","field":"body.template_id"}`. Wrong type → `422`.
- **`price` / `access_type` are marketplace metadata only — NOT enforced.** Generating from a `buyout` template at ¥99 works without purchasing. This is **not** a licence to ship that design commercially.
- All 73 templates report `rating: 5.0` — the field carries no signal.
- Output is **1024 × 1536** PNG.
- **There is a records endpoint:** `GET /api/v1/open/package-generate/records` lists prior renders (record id, `template_id`, logo fields, prompt, `created_at`). Still 404: `/open/history`, `/open/account`, `/open/quota`, `/open/me`, `/open/records`, `/open/packages` — the working path is `/open/package-generate/records`.

---

## Two hard limitations

### 1. ~~The engine accepts no image input~~ — **RETRACTED 2026-11-19**

**This section was wrong. Do not rely on it.** The schema has four real logo fields (see *Logo input and placement* above) and they work live.

How the error happened, because it is the reusable part:

- 16 candidate field names were "type-bombed" in one request — `image_url`, `logo`, `logo_url`, `design_image`, `artwork`, `reference_image`, `image_base64`, `mask`, `style_image`, `brand_logo`, `overlay`, `watermark`, `foreground`, `template_image`, `custom_image`, `upload`.
- It returned **200 OK**, which was read as "every field was ignored." **That inference is invalid.** FastAPI ignores *unknown* keys silently, so `200` is the expected response **whether or not** a field is real. A `422` would only have shown that a *correctly named* field rejected the supplied type.
- The guessed names simply were not the API's names. `logo_url`, `logo_base64`, `logo_position` and `logo_width_ratio` were real the entire time.
- The authoritative spec was sitting at `/api/v1/openapi.json` throughout.

**Correct method:** fetch the OpenAPI document and read `components.schemas.PackageGenerateRequest`. Never conclude "the field does not exist" from "my guessed name failed."

**Consequence, corrected:** gotde *can* be handed our mark and told where to put it — best-effort. It still cannot reproduce our typeface (§2), and placement is model-directed rather than exact, so a deterministic composite remains the reliable path for print.

### 2. It draws counterfeit typography

Ask for "AGROVERSE" and the engine synthesises **pseudo-glyphs** — measured as 10 discrete letterform blobs, evenly spaced on the bar at y≈515, OCR confidence 13–89. It is *not* our typeface and it re-invents the marks on every render, so no prompt wording fixes it.

> **OCR caveat — don't repeat my mistake.** At native resolution the type on the bar is small and tilted, so plain `tesseract` returns noise and it is tempting to conclude "the engine renders no text." **That conclusion is wrong.** Text does render. Crop the print area and upscale 3× before OCR and it reads cleanly (`AGROVERSE … CEREMONIAL CACAO … PARA BRAZIL … 81% CACAO … 50g`). Verify by cropping before claiming a render is textless.

---

## Approach A — the approved method ✅

**Suppress the wordmark, then composite the real mark ourselves.**

Chosen by the governor over the alternative (dropping the mark on its original saffron badge), because the keyed-gold treatment sits inside the design language of a dark espresso panel rather than reading as a pasted-on sticker.

### Step 1 — prompt for no wordmark

```
Ceremonial grade cacao packaging. Deep espresso-brown background with warm gold
hairline rules. NO text, NO wordmark, NO lettering, NO logo. Clean unmarked panel,
generous negative space. Minimal, premium, editorial.
```

Confirm the panel is clean (crop + 3× upscale + OCR should return near-nothing) before compositing.

### Step 2 — find the panel bbox

Threshold on luminance, then take the row/column spans with enough dark pixels:

Segment the bar as the largest **non-background** region — do **not** threshold on absolute luminance:

```python
a = np.asarray(Image.open(render).convert("RGB")).astype(int)
h, w, _ = a.shape
border = np.concatenate([a[0:3].reshape(-1, 3), a[-3:].reshape(-1, 3),
                         a[:, 0:3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
bg = np.median(border, axis=0)                 # sample the real background
mask = np.abs(a - bg).sum(axis=2) > 36         # anything unlike the background
cols = np.where(mask.sum(axis=0) > max(8, h * 0.05))[0]
rows = np.where(mask.sum(axis=1) > max(8, w * 0.05))[0]
# -> x0..x1, y0..y1
```

> **Why not `lum < 70`:** that was the previous recipe and it is broken. Templates with warm or light grounds (saffron, parchment, gold) have almost no pixels below 70, so the detector degenerates and reports a near-full-frame bbox — which is how a **portrait** bar got mis-measured as **landscape (ar 1.34)**. With the recipe above the same renders measure portrait, **ar 0.48–0.67**.
>
> **Sanity check:** a genuine bar bbox has `width/height ≈ 0.48–0.67` and is clearly taller than wide. If your detector returns ar > 1, the **detector** is wrong, not the render.

### Step 3 — key the saffron background off the logo

The authorised mark sits on flat saffron `#FFB020`. Soft-key it to alpha:

```python
bg = np.array([255., 176., 32.])
dist = np.abs(rgb - bg).sum(axis=2)
alpha = np.clip((dist - 40) / 110.0, 0, 1)   # soft edge, no halo
trim to alpha > 0.25
```

### Step 4 — recolour to gold and place

Tint to `(232, 178, 84)` on a dark panel, size to **~62% of panel width**, place centred horizontally at **~10% down** the panel.

### Reference implementation

```python
from PIL import Image
import numpy as np

HI = "20230711 - Agroverse logo for trademark filing.jpeg"
base = Image.open(render_path).convert("RGB")
a = np.asarray(base).astype(int)
border = np.concatenate([a[0:3].reshape(-1, 3), a[-3:].reshape(-1, 3),
                         a[:, 0:3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
bgc = np.median(border, axis=0)
maskb = np.abs(a - bgc).sum(axis=2) > 36
cols = np.where(maskb.sum(axis=0) > max(8, a.shape[0] * 0.05))[0]
rows = np.where(maskb.sum(axis=1) > max(8, a.shape[1] * 0.05))[0]
x0, x1, y0, y1 = cols.min(), cols.max(), rows.min(), rows.max()

src = Image.open(HI).convert("RGB"); sa = np.asarray(src).astype(float)
alpha = np.clip((np.abs(sa - np.array([255.,176.,32.])).sum(axis=2) - 40)/110.0, 0, 1)
ys, xs = np.where(alpha > 0.25)
mask = Image.fromarray((alpha[ys.min():ys.max()+1, xs.min():xs.max()+1]*255).astype(np.uint8), "L")

gold = Image.new("RGBA", mask.size, (232, 178, 84, 0)); gold.putalpha(mask)
pw = int((x1-x0+1) * 0.62); th = int(mask.height * pw / mask.width)
lg = gold.resize((pw, th), Image.LANCZOS)
out = base.copy()
out.paste(lg, (x0 + ((x1-x0+1)-pw)//2, y0 + int((y1-y0)*0.10)), lg)
out.save("branded.png")
```

### Quality check — upscale factor

Always report `composited_width / source_mark_width`. **Target ≤ 1.1×.** Above ~2× the mark goes visibly soft in print.

---

## The logo asset (important)

Use the **trademark filing** mark: **668 × 944 px**, ~104 KB, saffron background.

With it, the composite runs at **1.08× upscale → effectively native.**

The old approach used `favicon-192x192.jpeg` and ran at **3.70× upscale**, which is visibly soft on a physical bar. Do not use the favicon for print.

**Authoritative locations and PDF sizing already live in `agroverse/AGROVERSE_PRICE_LIST_AND_ASSETS.md`** — read that for the three repo paths and the 0.625" × 0.88" document sizing. Not restated here to avoid drift.

### ⚠️ Open blocker: no vector artwork

There is **no SVG or high-resolution vector** Agroverse mark anywhere in the repos. The 668 × 944 JPEG is the ceiling. This limits:

- print-resolution label files (a 300 DPI 2" label needs 600 px; we are near that, but with no headroom for enlargement)
- white-label customer print files
- any large-format use

Filed as a real brand-asset gap — it will bite the white-label print pipeline regardless of gotde, so it is not an engine problem.

---

## Template library

73 templates, two categories:

| Category | Count | Character |
|---|---|---|
| **Pro** | 23 | American retro / diner / sport / road-trip (Route 66, baseball, muscle cars) |
| **内销** (domestic) | 50 | Chinese classical — landscape, auspicious creatures, lanterns, porcelain, celestial |

All 1200 × 800, all rated 5.0. ID range **452–553**, non-contiguous.

**Nothing in the library fits Agroverse.** The Pro set is Americana, the 内销 set is Chinese classical; neither has ceremonial-cacao, Amazonian, or specialty-food branding. Treat gotde as a **background/style scaffold** — brand identity comes entirely from `extra_requirements`, and even then the chosen template's own motif bleeds through (template #549's blue fox appeared in an unrelated prompt's output). Warm/gold-adjacent options worth trying: `472`, `536`, `537`; earthy/handcrafted: `长城映霞`, `江山如画`.

**Template #492 与光同行** ("Walking with the Light") is the one most exercised — 内销, free, single continuous panel, accepts the keyed-gold mark well.

---

## Render log

Vendor exposes no history API, so this table is the spend record. Append every render.

| Record | Template | Coverage | Background | Prompt | Outcome |
|---|---|---|---|---|---|
| 21 | 549 | label | kraft | prompt A | succeeded, URL lapsed before capture |
| 22 | 549 | label | kraft | prompt A | succeeded, captured |
| 23 | 521 | — | — | paid-template probe | OK — **no purchase gate** |
| 24 | 493 | — | — | paid-template probe | OK — **no purchase gate** |
| 41 | 492 | label | white | A | OK |
| 42 | 492 | label | kraft | A | OK |
| 43 | 492 | label | gray | A | OK |
| 44 | 492 | full | white | A | OK — text legible |
| 45 | 492 | label | kraft | B (botanical) | OK — template motif dominates |
| 46 | 492 | — | — | 16-field type-bomb | 200 OK — **all fields ignored** |
| 47 | 492 | label | white | no-wordmark | OK — clean base |
| 48 | 492 | label | kraft | no-wordmark | OK — clean base, **used for Approach A** |
| 59 | 480 | label | white | A + logo_base64 | OK — mark accepted, `bottom-center` @ 0.22, ar 0.54 |
| 60 | 482 | label | white | A + logo_base64 | OK — ar 0.51 |
| 61 | 452 | label | white | A + logo_base64 | OK — ar 0.67 |
| 62 | 472 | label | white | A + logo_base64 | OK — ar 0.67 |
| 63 | 536 | label | white | A + logo_base64 | OK — ar 0.66 |
| 64 | 480 | label | white | A + logo, **top-left @ 0.40** | OK — position control; ar 0.48 |

> Geometry drift is real: template **480 returned ar 0.54 as rec 59 and 0.48 as rec 64** from the same payload apart from logo params. Measure every render; never assume a fixed output size.

---

## When NOT to use gotde

- **Previewing a customer's uploaded artwork** on a bar → use the **local canvas composite** (paste their true PNG into the measured bbox). Faithful by definition; gotde would hallucinate.
- **Anything needing exact brand typography** → composite locally from real type assets.
- **Customer-facing exposure** → the certificate is currently valid, so TLS is no longer the blocker. The real blockers are brand fidelity (§2) and best-effort logo placement — not transport.

## Related

- `agroverse/AGROVERSE_PRICE_LIST_AND_ASSETS.md` — logo paths, PDF sizing
- `PRODUCT_DEVELOPMENT_SPECS.md` — product/packaging spec sheets
- `plans/WHITE_LABEL_IMPLEMENTATION_PLAN.md` — white-label product context
- `SUPPLY_CHAIN_AND_FREIGHTING.md` — packaging and unit costs
