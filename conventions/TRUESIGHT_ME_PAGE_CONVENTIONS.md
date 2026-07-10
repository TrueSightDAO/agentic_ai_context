# truesight_me Page Conventions (TrueSight DAO static site)

When creating or updating pages in the **truesight_me** repository (deployed at `truesight.me`), follow these conventions so all pages look and behave consistently. **AI and developers should use this document** when adding or editing truesight_me pages.

This is the counterpart to `DAPP_PAGE_CONVENTIONS.md` (dapp repo). The two sites share the same DAO but have different audience, tone, and structural conventions.

---

## 1. Navigation — shared JS component (not inline)

The nav is **injected by a shared JS file**: `js/nav.js`. Every page includes a placeholder that the script replaces with the canonical nav HTML.

**Rule:** Every page MUST include these two lines at the top of `<body>`:

```html
<div id="site-nav"></div>
<script src="/js/nav.js"></script>
```

**Why this design:** The nav uses **root-relative paths** (`/index.html`, `/contracts/`) so it works identically at any directory depth — root, 1-level, 2-level deep, etc. There is no need to adjust `../` prefixes per page. The single source of truth is `js/nav.js`; updating it updates every page instantly.

The nav includes these sections: Home, About Us, Projects (dropdown), Proposals, Community (dropdown), Resources (dropdown, including **Smart Contracts** at `/contracts/`), and Blog.

### History

Before 2026-07, the nav was duplicated inline in every HTML file with depth-dependent relative paths (`../`, `../../`). A `scripts/sync_top_nav.py` script enforced consistency. That script is now **deprecated** — all pages use the shared JS injection instead.

---

## 2. Footer — shared JS component (not inline)

The footer is **injected by a shared JS file**: `js/footer.js`. Every page includes a placeholder at the bottom of `<body>`:

```html
<div id="site-footer"></div>
<script src="/js/footer.js"></script>
```

**Rule:** Every page MUST include these two lines before `</body>`. The footer contains all four canonical link sections (Transparency, Governance & Records, Data & Records, Partnerships), "JOIN OUR MOVEMENT" heading, social icons (Telegram + GitHub), and the site credit line. External links use absolute URLs (`https://truesight.me/...`) and internal assets use root-relative paths (`/assets/...`).

The single source of truth is `js/footer.js`. Updating it updates every page instantly.

### History

Before 2026-07, the footer was duplicated inline across pages with four competing variants. Many pages had no footer at all. All pages now use the shared injection.

---

## 3. Google Analytics — hostname-gated

Every page MUST include the GA4 gtag snippet in `<head>`, gated to production only:

```html
<script>
(function() {
  var h = window.location.hostname;
  if (h !== 'truesight.me' && h !== 'www.truesight.me') return;
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-9QN16RFM0T';
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-9QN16RFM0T');
})();
</script>
```

**Rule:** Copy this block verbatim as the first element in `<head>` (before `<meta charset>`). The hostname gate means it silently no-ops on beta and localhost.

---

## 4. Body and layout

Every page wraps content in `<div class="page">`, NOT `<main class="page">`. The `<div id="app">` wrapper is a Sophia-ism — do not add it unless the page's JS specifically requires it.

```html
<body>
    <div id="site-nav"></div>
    <script src="/js/nav.js"></script>
    <div class="page">
        <!-- hero, sections, content -->
    </div>
    <div id="site-footer"></div>
    <script src="/js/footer.js"></script>
    <script src="..." />
</body>
```

---

## 5. Required head elements

In order:

| Element | Notes |
|---|---|
| GA4 gtag | First in `<head>`, hostname-gated |
| `<meta charset="UTF-8">` | |
| `<meta name="viewport">` | `width=device-width, initial-scale=1` |
| `<title>` | `Page Title | TrueSight DAO` or `Page Title — TrueSight DAO` |
| `<meta name="description">` | SEO description |
| OG/Twitter meta (major pages) | `og:title`, `og:description`, `og:image`, `twitter:card` etc. |
| Favicon | Wix CDN: `0e2cde_dd65db118f8f499eb06c159d7262167d%7Emv2.ico` |
| Google Fonts preconnect | `fonts.googleapis.com` + `fonts.gstatic.com` |
| Google Fonts stylesheet | Space Grotesk + Inter |
| `styles/main.css` | Path prefix-adjusted for depth |

**Rule for CSS paths:** Adjust `href` relative to the page's directory depth. Root pages: `styles/main.css`. Depth-1 pages: `../styles/main.css`. Depth-2 pages: `../../styles/main.css`.

---

## 6. Hamburger menu JavaScript

The hamburger menu and dropdown toggle behavior is handled by the inline script in each page. It must include all four handlers:

1. Menu toggle click handler
2. Dropdown toggle click handler (mobile-only)
3. Close-on-link-click handler
4. Close-on-overlay-click handler (clicking outside the menu closes it)

Since the nav HTML is injected by `js/nav.js` (which runs synchronously), the hamburger JS runs after the nav is in the DOM and binds to the injected elements correctly.

**Rule:** Copy the hamburger `<script>` block from `index.html` or `about-us.html`. The script's `querySelector('.menu-toggle')` etc. find the elements injected by `nav.js`.

---

## 7. Quick checklist for new pages

- [ ] GA4 gtag (first in head, hostname-gated)
- [ ] `<div id="site-nav"></div><script src="/js/nav.js"></script>` at top of `<body>`
- [ ] `<div id="site-footer"></div><script src="/js/footer.js"></script>` before `</body>`
- [ ] `<div class="page">` wrapper (not `<main class="page">`)
- [ ] Stylesheet paths depth-adjusted (`../styles/main.css` for subdirectories)
- [ ] Hamburger JS with all 4 handlers (toggle, dropdown, close-on-link, close-on-overlay)
- [ ] Page link in `index.html` (if applicable)

---

## 8. Anti-patterns — common LLM-generated mistakes

When an LLM generates a truesight_me page from scratch, these mistakes recur:

| Anti-pattern | Fix |
|---|---|
| Inline `<nav class="site-header">` HTML block | Use `<div id="site-nav"></div><script src="/js/nav.js"></script>` — nav is shared via JS injection |
| Depth-dependent nav paths (`../`, `../../`) | Root-relative paths in `nav.js` handle this automatically |
| Missing footer or inline footer | Use `<div id="site-footer"></div><script src="/js/footer.js"></script>` — footer is shared via JS injection |
| Missing GA4 gtag | Copy the hostname-gated snippet verbatim |
| `<main class="page">` instead of `<div class="page">` | Use `<div class="page">` |
| Adding `<div id="app">` wrapper | Remove it unless page JS requires it |
| `<title>` without site suffix | Use `Page Title — TrueSight DAO` or `Page Title \| TrueSight DAO` |
| Simpler hamburger JS (missing handlers) | Copy full version with all 4 handlers from canonical |
| Custom favicon | Use the Wix CDN favicon URL |

---

## 9. Where conventions live

| Topic | Location |
|---|---|
| Page structure / nav / footer / GA | This file (agentic_ai_context) |
| DApp conventions (separate concerns) | `agentic_ai_context/DAPP_PAGE_CONVENTIONS.md` |
| Site voice / tone | `agentic_ai_context/EDITORIAL_TONE.md` §2 (agroverse.shop) |
| Repository overview | `agentic_ai_context/NOTES_truesight_me.md` |
| Shared nav source | `truesight_me/js/nav.js` |
| Shared footer source | `truesight_me/js/footer.js` |

When in doubt, **copy structure from `index.html`** (the canonical page) and adjust content.

---

## 10. Shared component architecture

Both nav and footer use the same pattern:

1. Each page includes a **placeholder** `<div>` element and a `<script>` tag with a **root-relative path** (`/js/nav.js`, `/js/footer.js`)
2. The JS file finds the placeholder by ID (`site-nav`, `site-footer`) and replaces it with the canonical HTML
3. All internal links in the HTML use **root-relative paths** (`/index.html`, `/contracts/`, `/assets/...`)
4. External links use absolute URLs (`https://truesight.me/...`)

This architecture means:
- **Any nesting depth works** — root-relative paths resolve correctly from any directory
- **One source of truth** — changing `js/nav.js` or `js/footer.js` updates every page
- **No build step needed** — works directly from the web server

**When adding or changing nav/footer links:** Edit `js/nav.js` or `js/footer.js` only. Do NOT edit individual HTML pages.
