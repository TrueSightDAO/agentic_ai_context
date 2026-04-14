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
