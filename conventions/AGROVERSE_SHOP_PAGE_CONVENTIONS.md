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
