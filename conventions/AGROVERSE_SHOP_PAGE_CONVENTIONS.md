# agroverse_shop Page Conventions (Agroverse e-commerce site)

When creating or updating pages in the **agroverse_shop** repository (deployed at `agroverse.shop`), follow these conventions so all pages look and behave consistently. **AI and developers should use this document** when adding or editing agroverse_shop pages.

This is the counterpart to `TRUESIGHT_ME_PAGE_CONVENTIONS.md` (truesight_me) and `DAPP_PAGE_CONVENTIONS.md` (dapp). All three sites share the same DAO but have different designs and audiences.

---

## 1. Navigation — shared JS component (not inline)

The nav is **injected by a shared JS file**: `js/shared-chrome.js`. Every page includes a placeholder that the script replaces with the canonical nav HTML.

**Rule:** Every page MUST include this at the top of `<body>` (right after the opening tag):

```html
<div id="site-nav"></div>
<script src="/js/shared-chrome.js"></script>
```

**Why this design:** The nav uses **root-relative paths** (`/`, `/blog/`, `/cacao-journeys/`) so it works identically at any directory depth — root, 1-level, 2-level, up to 4 levels deep (e.g., `cacao-journeys/pacific-west-coast-path/experiences/slab-city-salvation-mountain/`). There is no need to adjust `../../` prefixes per page. The single source of truth is `js/shared-chrome.js`.

The nav contains 5 links: Home, Products, Cacao Journeys, Blog, Contact. On the homepage, hash anchors (`#home`, `#products`, `#contact`) are used for smooth scrolling. On other pages, root-relative paths (`/`, `/#products`, `/#contact`) link back to the homepage sections.

### Cart icon and Order History

The cart icon and "Order History" link are injected by `js/universal-nav.js` into the `.nav-links` `<ul>`. Do NOT add cart icon HTML manually — `universal-nav.js` handles it. Ensure both `universal-nav.js` and `navigation.js` are loaded on pages that need them.

### Mobile hamburger

`js/navigation.js` handles mobile menu toggle behavior (hamburger, overlay, link-close, resize-close). It binds to the elements injected by `shared-chrome.js`. Do NOT add inline hamburger JS to new pages — rely on `navigation.js`.

### History

Before 2026-07, the nav was duplicated inline in every HTML file with depth-dependent relative paths (`../../../../`). Multiple Python batch scripts existed to maintain consistency across ~190 pages. Those scripts are now **deprecated**.

---

## 2. Footer — shared JS component (not inline)

The footer is **injected by `js/shared-chrome.js`** (the same file that injects the nav). Every page includes a placeholder before `</body>`:

```html
<div id="site-footer"></div>
```

**Rule:** Every page MUST include this placeholder. The footer contains the canonical link set: Home, Mission, Products, Farms, Shipments, Blog, Partners, Wholesale, Cacao Journeys, Order History, Contact (email), plus the phone number and copyright line.

The footer injection is deferred to `DOMContentLoaded` (footer placeholder is at the bottom of body, after the script tag), so it renders after page content. The nav injects immediately (blocking script).

The footer's `id="contact"` attribute is preserved — it serves as the scroll target for the "Contact" nav link.

### History

Before 2026-07, the footer was duplicated inline across pages with multiple variations (different taglines, missing links, different structures). All pages now use the shared injection.

---

## 3. Required page structure

```html
<!doctype html>
<html lang="en">
<head>
    <!-- page-specific <style> block for CSS variables and styles -->
    <link href="../../css/navigation.css" rel="stylesheet">
    <link href="../../css/cards.css" rel="stylesheet">
    <!-- other shared CSS -->
</head>
<body>
    <div id="site-nav"></div>
    <script src="/js/shared-chrome.js"></script>

    <!-- page content -->

    <div id="site-footer"></div>

    <script src="../../js/navigation.js"></script>
    <script src="../../js/universal-nav.js"></script>
    <script src="../../js/cart.js"></script>
    <!-- page-specific scripts -->
</body>
</html>
```

**Rule for CSS/JS paths:** The shared-chrome.js is always referenced as `/js/shared-chrome.js` (root-relative). Other JS/CSS files (navigation.js, universal-nav.js, cart.js, cards.css, etc.) still use **depth-relative paths** (`../js/...`, `../../js/...`, etc.) because they are NOT root-relative.

---

## 4. Quick checklist for new pages

- [ ] `<div id="site-nav"></div><script src="/js/shared-chrome.js"></script>` at top of `<body>`
- [ ] `<div id="site-footer"></div>` before `</body>`
- [ ] JS files loaded with depth-relative paths (`../../js/navigation.js`, etc.)
- [ ] CSS files loaded with depth-relative paths (`../../css/navigation.css`, etc.)
- [ ] Cart script dependencies: `config.js`, `cart.js`, `cart-ui.js`, `inventory-service.js`
- [ ] Page content follows existing design patterns (CSS variables, card layouts, etc.)

---

## 5. Anti-patterns — common LLM-generated mistakes

| Anti-pattern | Fix |
|---|---|
| Inline `<header><nav>...</nav></header>` block | Use `<div id="site-nav"></div><script src="/js/shared-chrome.js"></script>` |
| Inline `<footer id="contact">...</footer>` block | Use `<div id="site-footer"></div>` |
| Depth-dependent nav/footer paths (`../../../../`) | Root-relative paths in `shared-chrome.js` handle this automatically |
| Adding cart icon HTML manually | `universal-nav.js` injects it — do not duplicate |
| Adding inline hamburger JS | `navigation.js` handles it — do not duplicate |
| Incorrect CSS path depth | Count directories from page to root: `../../css/` for depth 2, `../../../../css/` for depth 4 |

---

## 6. Where conventions live

| Topic | Location |
|---|---|
| Page structure / nav / footer | This file (agentic_ai_context) |
| truesight_me conventions | `agentic_ai_context/TRUESIGHT_ME_PAGE_CONVENTIONS.md` |
| DApp conventions | `agentic_ai_context/DAPP_PAGE_CONVENTIONS.md` |
| Site voice / tone | `agentic_ai_context/EDITORIAL_TONE.md` §2 (agroverse.shop) |
| Shared chrome source | `agroverse_shop/js/shared-chrome.js` |
| Navigation behavior | `agroverse_shop/js/navigation.js` |
| Cart + order history injection | `agroverse_shop/js/universal-nav.js` |
| New SKU checklist | `agentic_ai_context/AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md` |
| Product creation checklist | `agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md` |
| Blog listing images | `agroverse_shop/.cursor/rules/blog-listing-images.mdc` |
| CI and testing | `agroverse_shop/.cursor/rules/ci-and-testing.mdc` |

---

## 7. Shared component architecture

The nav and footer use this pattern:

1. Each page includes **placeholders** (`<div id="site-nav">`, `<div id="site-footer">`)
2. The `<script src="/js/shared-chrome.js">` is a **blocking script** that:
   - Injects the nav immediately (matching the `#site-nav` placeholder, which is right above the script)
   - Defers footer injection to `DOMContentLoaded` (because the `#site-footer` placeholder comes later in the page)
3. All internal links use **root-relative paths** (`/`, `/blog/`, `/cacao-journeys/`)
4. The homepage uses hash anchors (`#home`, `#products`, `#contact`) for smooth scrolling
5. External links use absolute URLs where applicable

**When adding or changing nav/footer links:** Edit `js/shared-chrome.js` only. Do NOT edit individual HTML pages.

---

## 8. Farm / shipment story media (JSON-driven)

Farm and shipment pages do **not** hardcode their photos and YouTube embeds in HTML. Each page keeps a
`media.json` next to its `index.html`, and the shared loader `js/media-gallery.js` builds the gallery at
page-load time. Adding a photo or video means "upload the asset, add one JSON entry" — no HTML edit.

Plan of record: `agentic_ai_context/plans/FARM_SHIPMENT_MEDIA_JSON_PLAN.md`.

### Source resolution — published-first, local fallback

The loader resolves media in two layers (same fetch-first idiom as `js/inventory-service.js`):

1. **Published** — `https://raw.githubusercontent.com/TrueSightDAO/farm_media_manifests/main/galleries/<slug>.json`
   (machine-published by the farm-media daemon; the raw host is CORS-open). `<slug>` is the page's last path segment.
2. **Local** — the hand-authored `./media.json` beside the page.

The published file wins on **membership** (so "uploaded ⇒ published" holds by construction). Each published
entry is then enriched with the local curation fields — `caption`, `section`, `alt`, `fallback`, `aspect` —
matched by id/`src`. `hero` and `farmer` stay **local-first**: the publisher emits no farmer slot and only a
filename-only hero `alt`, so the human-authored values are authoritative for those two.

If neither file is available the loader does nothing (no error). A malformed entry is skipped rather than
failing the whole gallery, and a bad image `src` falls back to `fallback` (default
`../../assets/images/hero/cacao-circles-alt.jpg`).

### Placeholder conventions

| Placeholder | Where | Fills |
|---|---|---|
| `data-media-slot="hero"` | each hero `<img>` (`.shipment-image`, `.farmer-photo`, banner) | `hero.src` + `hero.alt`; sets `onerror` → `hero.fallback` |
| `data-media-slot="farmer"` | a farmer profile `<img>` **distinct** from the hero (agl8 pattern) | `farmer.src` + `farmer.alt`; only filled if `farmer` exists in JSON |
| `id="media-gallery"` | the gallery container | **every** item in `gallery` (single-container / legacy style) |
| `data-media-gallery="<section>"` | each gallery container on a multi-section page | only items whose `section` equals that value |

Every `data-media-slot="hero"` element on the page is filled from the one `hero` entry — that is what
replaced the old copy-paste-per-slot duplication. A page that has none of these placeholders is a no-op
(the loader returns immediately), so the script is safe to leave on any page.

### `media.json` schema

```json
{
  "schemaVersion": 1,
  "hero":   { "type": "image", "src": "<url or ../../relative>", "fallback": "../../assets/images/hero/cacao-circles-alt.jpg", "alt": "AGL4 - Oscar's Farm" },
  "farmer": { "type": "image", "src": "<url or ../../relative>", "alt": "..." },
  "gallery": [
    { "type": "youtube", "videoId": "sLNS9pZUBVw", "title": "...", "caption": "...", "section": "story-videos", "aspect": "portrait" },
    { "type": "image",   "src": "../../assets/images/farms/sao-jorge-IMG_1616.jpg", "alt": "...", "title": "...", "caption": "...", "section": "photos" }
  ]
}
```

Per-item keys:

- `type` — `youtube` or `image` (required; anything else is skipped)
- `videoId` — YouTube id for `youtube` items (embedded as `https://www.youtube.com/embed/<id>?rel=0`)
- `src` — image URL or depth-relative path for `image` items
- `alt` — image alt text (accessibility; always set it for images)
- `title` — optional `<h3>` heading above the media
- `caption` — optional paragraph below the media
- `fallback` — image shown on load error (defaults to `cacao-circles-alt.jpg`)
- `section` — routes the item to the matching `data-media-gallery="<section>"` container
- `aspect` — `"portrait"` gives the centered 420px 9:16 frame used for vertical videos; omit for landscape

The `farmer` block and the `section`/`aspect` keys are optional; `hero` and `gallery` are the common case.

### Wiring a page

1. Add `data-media-slot="hero"` to the hero `<img>` and remove its hardcoded `src`/`alt`.
2. Replace the gallery's existing child content with an empty container — `id="media-gallery"` (all items) or
   `data-media-gallery="<section>"` (per-section).
3. Add `<script src="../../js/media-gallery.js"></script>` with the other page-specific scripts at the end of
   `<body>` — **depth-relative** (like `navigation.js`/`cart.js`), not root-relative like `shared-chrome.js`,
   because this loader is not site-wide.
4. Add `media.json` beside `index.html`.

**Failure mode to watch:** a page with a `#media-gallery` container but no `media.json` (and no published
collection) renders an **empty** gallery — silently, with no console error. If a gallery looks blank, check
that the JSON file exists and is valid before debugging the script.

**When adding/changing farm or shipment story media:** edit `media.json` (and upload the asset) — do NOT
hardcode `<img>`/`<iframe>` into the page HTML.
