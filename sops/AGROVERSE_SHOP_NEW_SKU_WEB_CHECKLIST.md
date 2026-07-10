# Agroverse Shop — new SKU / PDP: do not miss farm & shipment cross-listings

Read this when adding a **new sellable SKU** on **agroverse.shop** (new `product-page/<slug>/index.html`, new chocolate bar / ceremonial line / etc.). **Merchant Center, JSON-LD, and sitemap** are covered in **`agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md`**. This doc covers the **on-site discovery grid** links that are easy to skip.

---

## Why this exists

Product pages often already link **to** the correct **farm** and **shipment** in body copy. Visitors still expect every SKU tied to a farm/shipment to appear under:

- **`farms/<farm-slug>/index.html`** → section **“Products from This Farm”** (`<div class="items-grid">` … `<a class="item-card" href="../../product-page/…">`)
- **`shipments/aglN/index.html`** → section **“Products from This Shipment”** (same `item-card` pattern)

If those grids omit the new PDP, the SKU is **under-discovered** even though the PDP and feed are correct.

---

## Checklist (after the PDP exists)

1. **Identify** the canonical **shipment id** (e.g. **AGL4**, **AGL2**, **AGL8**) and **farm profile path** (e.g. `farms/oscar-bahia/`, `farms/fazenda-santa-ana-bahia/`, `farms/paulo-la-do-sitio-para/`) from the PDP or ledger copy.
2. **Edit both HTML files** and append an **`item-card`** next to sibling products:
   - Reuse the same structure as existing cards: `href` to `../../product-page/<slug>/index.html`, `item-card-image`, `item-card-body`, **`<h3>`** title, **`<div class="item-meta">`** with **price** and **`From AGLn`** (match wording on sibling lines).
3. **Images:** Prefer the same hero image as the PDP (or an existing product shot already on the farm/shipment page) so cards stay visually consistent.
4. **Homepage / catalog:** If the product should appear in the main shop grid, update **`index.html`** (and **`js/products.js`** / feeds per **`PRODUCT_DEVELOPMENT_SPECS.md`** §1) — do not assume the homepage was updated when only the PDP was added.
5. **Verify locally:** Open the farm page and shipment page; confirm the new card navigates to the PDP and does not 404.
6. **Wholesale banner on the new PDP:** every PDP carries a thin "Selling Agroverse in your shop?" banner linking to **`/wholesale/`** (added in **agroverse_shop_beta#77**, post-rollout default). For ceremonial / per-bag SKUs the banner sits between the Add-to-Cart block and the product description; for per-kilogram bulk SKUs it sits between the price and the description. Match the existing pattern — copy from a sibling PDP rather than freehand. The banner href is **`../../wholesale/`** from any `product-page/<slug>/` location.

---

## Repo paths (workspace)

- **Farm pages:** `agroverse_shop/farms/*/index.html`
- **Shipment pages:** `agroverse_shop/shipments/agl*/index.html`
- **Product checklist (feeds, Merchant Center, schema):** `agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md`
- **Specs / Sheet workflow:** `agentic_ai_context/PRODUCT_DEVELOPMENT_SPECS.md`

---

## Example (81% 50g bars, 2026-04)

- **`organic-81-dark-chocolate-bar-50g-oscar-bahia-2024`** → cards added to **`shipments/agl4/index.html`** and **`farms/oscar-bahia/index.html`**.
- **`organic-81-dark-chocolate-bar-50g-fazenda-santa-ana-bahia-2023`** → cards added to **`shipments/agl2/index.html`** and **`farms/fazenda-santa-ana-bahia/index.html`**.

Treat that pairing as the default pattern for **farm-origin SKUs** tied to a single AGL.

---

## PDP image layout — hero + `.gallery` underneath

Every product page follows the same image structure: **one hero shot at full container width, optional supplementary shots in a `.gallery` grid directly below it inside the same `<div class="product-image-container">`**. Do not put any image gallery **above** the hero. Do not use `<figure>` + `<figcaption>` for product photos — the alt text is the caption.

Reference implementation: **[`agroverse_shop/product-page/organic-81-dark-chocolate-bar-50g-oscar-bahia-2024/index.html`](https://github.com/TrueSightDAO/agroverse_shop_beta/blob/main/product-page/organic-81-dark-chocolate-bar-50g-oscar-bahia-2024/index.html)**.

### Markup

```html
<div class="product-header">
  <div class="product-image-container">
    <img alt="<descriptive alt>" class="product-image" src="../../assets/images/products/<hero>.jpg"/>
    <div class="gallery">
      <img alt="<descriptive alt>" loading="lazy" src="../../assets/images/products/<close-up-or-back>.jpg"/>
      <img alt="<descriptive alt>" loading="lazy" src="../../assets/images/products/<packaging-or-on-shelf>.jpg"/>
      <!-- add more <img loading="lazy"> as needed; auto-fit handles layout -->
    </div>
  </div>
  <div class="product-info">
    …
  </div>
</div>
```

### CSS (paste into the page's existing `<style>` block, next to `.product-image`)

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0 0;
}
.gallery img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}
```

### Why these rules

- **Hero at top**: families and resellers want to see the **product** first. Packaging shots before the product confuses the visual hierarchy.
- **`.gallery` inside `.product-image-container`**: PDP layouts use `position: sticky` on `.product-image-container` so the hero and supplementary shots scroll together with the description. Putting `.gallery` outside the container loses the sticky.
- **Fixed 220px height + `object-fit: cover`**: keeps mixed-aspect-ratio shots (front-of-bag portrait, on-shelf landscape) visually consistent. Without this, mixed aspect ratios make the row look ragged.
- **`loading="lazy"` on supplementary shots**: hero stays eager; below-the-fold images don't block paint.
- **No `<figcaption>`**: the alt text already describes the image, screen readers pick it up, and visible captions clutter the visual line. Reserve captions for blog / cacao-journey content where the photo carries narrative.

### When you have packaging photos to show on a ceremonial / cacao bag SKU

Use these standard shots (placed at `agroverse_shop/assets/images/products/packaging/`):

- `front.jpeg` — bag front
- `back.jpeg` — bag back, showing the traceability QR

Both go in the `.gallery` grid below the hero (which is the farm-portrait shot, not the bag). Do **not** put the bag shots above the hero with figcaptions like "Front of the bag" / "Back — scan the QR code…" — that's the legacy (pre-2026-04-27) pattern; cleanup PRs are migrating older PDPs to this convention.
