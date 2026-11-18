# Print-on-Demand Mockup Generation

**Read this** when generating packaging mockups for Agroverse — chocolate bars, pouches, or labels — especially before spending money or renders on a third-party image-generation API.

**Status:** trial-stage. The engine works, the brand-fidelity workaround is settled, but this is **not** wired into any production funnel yet.

---

## TL;DR

1. Use **gotde.cn** to render a photoreal *packaging* mockup. Ask it for **no wordmark**.
2. **Composite the real Agroverse mark ourselves** (Approach A, below). The engine cannot take our logo as input and draws counterfeit letterforms if asked.
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

### ⚠️ Transport — HTTP only

The vendor's TLS certificate **expired 2026-11-17 07:59:59 UTC** (`CN=xiaodeapi.gotde.cn`, TrustAsia). HTTPS fails the handshake; only plain HTTP works.

- Working host: **`xiaodeapi.gotde.cn`**
- The host named in their own docs, `package.gotde.cn`, has a **separately broken certificate** — do not use it.
- Consequence: the API key travels **unencrypted** to a Chinese host. Acceptable for internal experimentation; **not acceptable for a customer-facing funnel.** Do not wire this into `/white-label` until the cert is renewed.

### Endpoints

| Endpoint | Method | Notes |
|---|---|---|
| `/api/v1/templates` | GET | **Public, no key.** `?page=&pageSize=100&include_base_map=true`. Paginate until `total`. |
| `/api/v1/open/package-generate` | POST | Requires `X-API-Key`. **This is the only generation path.** |

There is **no** `/openapi.json`, `/docs`, or `/redoc` (all 404) — the schema below was recovered from FastAPI 422/400 validation messages.

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

### Schema facts, verified

- **Strict validation.** Missing `template_id` → `400 {"success":false,"message":"Field required","field":"body.template_id"}`. Wrong type → `422`.
- **`price` / `access_type` are marketplace metadata only — NOT enforced.** Generating from a `buyout` template at ¥99 works without purchasing. This is **not** a licence to ship that design commercially.
- All 73 templates report `rating: 5.0` — the field carries no signal.
- Output is **1024 × 1536** PNG.
- No account, quota, history, or records endpoint (`/open/history`, `/open/account`, `/open/quota`, `/open/me`, `/open/records` all 404).

---

## Two hard limitations

### 1. The engine accepts no image input

There is **no artwork-upload path**. Proven by type-bombing 16 candidate field names in a single request — `image_url`, `logo`, `logo_url`, `design_image`, `artwork`, `reference_image`, `image_base64`, `mask`, `style_image`, `brand_logo`, `overlay`, `watermark`, `foreground`, `template_image`, `custom_image`, `upload`.

The request returned **200 OK**, meaning FastAPI's strict schema **silently ignored every one**. Had any been a real field, a string where a file/URL was expected would have raised 422. Also 404: `/open/upload`, `/open/image-search`, `/open/file`, `/open/package-generate-from-image`.

**Consequence:** gotde cannot wrap *our* design onto a bar. It prompts an image model from text to invent a mockup. Useful for **concept exploration**; wrong tool for **previewing a customer's uploaded PNG**.

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

```python
lum = 0.299*R + 0.587*G + 0.114*B
dark = lum < 70
cols = where(dark.sum(axis=0) > 300);  rows = where(dark.sum(axis=1) > 300)
# -> x0..x1, y0..y1
```

On the reference render: `x106–917, y32–1506` = 812 × 1475 px.

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
lum = 0.299*a[:,:,0] + 0.587*a[:,:,1] + 0.114*a[:,:,2]
dark = lum < 70
cols = np.where(dark.sum(axis=0) > 300)[0]; rows = np.where(dark.sum(axis=1) > 300)[0]
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

---

## When NOT to use gotde

- **Previewing a customer's uploaded artwork** on a bar → use the **local canvas composite** (paste their true PNG into the measured bbox). Faithful by definition; gotde would hallucinate.
- **Anything needing exact brand typography** → composite locally from real type assets.
- **Customer-facing, pre-cert-renewal** → HTTP-only makes it unsafe to expose.

## Related

- `agroverse/AGROVERSE_PRICE_LIST_AND_ASSETS.md` — logo paths, PDF sizing
- `PRODUCT_DEVELOPMENT_SPECS.md` — product/packaging spec sheets
- `plans/WHITE_LABEL_IMPLEMENTATION_PLAN.md` — white-label product context
- `SUPPLY_CHAIN_AND_FREIGHTING.md` — packaging and unit costs
