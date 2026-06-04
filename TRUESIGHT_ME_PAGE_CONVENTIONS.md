# truesight_me Page Conventions (TrueSight DAO static site)

When creating or updating pages in the **truesight_me** repository (deployed at `truesight.me`), follow these conventions so all pages look and behave consistently. **AI and developers should use this document** when adding or editing truesight_me pages.

This is the counterpart to `DAPP_PAGE_CONVENTIONS.md` (dapp repo). The two sites share the same DAO but have different audience, tone, and structural conventions.

---

## 1. Navigation — inline, NOT shared

Unlike the DApp which uses `menu.js`, truesight_me pages **inline the full `<nav class="site-header">`** in every HTML page. There is no shared JavaScript component.

**Why:** The site predates component-based architecture. A script (`scripts/sync_top_nav.py`) enforces consistency by auto-replacing the `<nav>` block across all pages from the canonical template.

**Rule:** Every page MUST include the full `<nav class="site-header">...</nav>` block. Do NOT omit it. Do NOT use absolute root-relative paths (`href="/"`). The paths must use the relative prefix convention for the page's directory depth:

| Page depth | Nav prefix | Example link |
|---|---|---|
| Root (`index.html`, `about-us.html`, etc.) | `""` | `href="index.html"` |
| 1 level (`security-dashboard/index.html`, `blog/index.html`) | `"../"` | `href="../index.html"` |
| 2 levels (`agroverse-shipments/agl1/index.html`) | `"../../"` | `href="../../index.html"` |

**After creating a new page:** Run `python3 scripts/sync_top_nav.py` to auto-fix the nav paths. Run `python3 scripts/sync_top_nav.py --check` to verify without modifying.

---

## 2. Footer — inline, full canonical

Every page MUST include the full `<footer class="footer">` block containing all four link sections (Transparency, Governance & Records, Data & Records, Partnerships), "JOIN OUR MOVEMENT" heading, social icons (Telegram + GitHub), and the site credit line. Do NOT substitute a minimal footer.

**Reference implementation:** `about-us.html` lines 241-304. Copy the entire `<footer>...</footer>` block and adjust any relative image paths (e.g., Telegram icon at `../assets/telegram-icon.jpg` for depth-1 pages).

**Rule:** The canonical footer contains 16 links across 4 sections. All 16 must be present. The footer is the site-wide footer — it belongs on every page regardless of the page's specific topic.

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
    <nav class="site-header">...</nav>
    <div class="page">
        <!-- hero, sections, footer -->
    </div>
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

**Rule for CSS paths:** Adjust `href` relative to the page's directory depth. Root pages: `styles/main.css`. Depth-1 pages: `../styles/main.css`.

---

## 6. Hamburger menu JavaScript

Every page MUST include the hamburger menu JS at the end of `<body>`. Copy from the canonical (about-us.html lines 392-399). The handler must include:

1. Menu toggle click handler
2. Dropdown toggle click handler (mobile-only)
3. Close-on-link-click handler
4. Close-on-overlay-click handler (clicking outside the menu closes it)

**Rule:** Copy the entire hamburger `<script>` block verbatim. Do not simplify it.

---

## 7. nav-matching disclaimer

The `<nav>` block comment (`<!-- Site-standard header matching beta.truesight.me -->`) is optional but serves as a signal to future LLMs that the nav is shared infrastructure, not page-specific.

---

## 8. Quick checklist for new pages

- [ ] GA4 gtag (first in head, hostname-gated)
- [ ] Full `<nav class="site-header">` with relative paths (run `sync_top_nav.py` after)
- [ ] Full `<footer class="footer">` with all 4 sections + social icons + credit line
- [ ] `<div class="page">` wrapper (not `<main class="page">`)
- [ ] Stylesheet paths depth-adjusted (`../styles/main.css` for subdirectories)
- [ ] Image paths in footer depth-adjusted (`../assets/telegram-icon.jpg`)
- [ ] Hamburger JS with all 4 handlers (toggle, dropdown, close-on-link, close-on-overlay)
- [ ] Page link in `index.html` (if applicable) relative to page depth

---

## 9. Anti-patterns — common LLM-generated mistakes

When an LLM generates a truesight_me page from scratch, these mistakes recur:

| Anti-pattern | Fix |
|---|---|
| Missing `<footer>` entirely or minimal footer | Copy full canonical footer from `about-us.html` |
| Absolute nav paths (`href="/"`) | Use relative paths per depth; run `sync_top_nav.py` |
| Missing GA4 gtag | Copy the hostname-gated snippet verbatim |
| `<main class="page">` instead of `<div class="page">` | Use `<div class="page">` |
| Adding `<div id="app">` wrapper | Remove it unless page JS requires it |
| `<title>` without site suffix | Use `Page Title — TrueSight DAO` or `Page Title | TrueSight DAO` |
| Simpler hamburger JS (missing handlers) | Copy full version with all 4 handlers from canonical |
| Custom favicon | Use the Wix CDN favicon URL |

### Example: security-dashboard/index.html (2026-06-04)

Sophia (truesight_autopilot) generated the initial version which was missing: GA4 gtag, full footer (had a 2-line placeholder), and overlay-click handler in hamburger JS. Nav paths were absolute (`/about-us.html`) instead of relative (`../about-us.html`). Fixed by running `sync_top_nav.py` for paths, then manually adding GA, full footer, and overlay handler.

---

## 10. Where conventions live

| Topic | Location |
|---|---|
| Page structure / nav / footer / GA | This file (agentic_ai_context) |
| DApp conventions (separate concerns) | `agentic_ai_context/DAPP_PAGE_CONVENTIONS.md` |
| Site voice / tone | `agentic_ai_context/EDITORIAL_TONE.md` §2 (agroverse.shop) |
| Repository overview | `agentic_ai_context/NOTES_truesight_me.md` |
| Nav sync script | `truesight_me/scripts/sync_top_nav.py` |

When in doubt, **copy structure from `about-us.html`** (the cleanest canonical page) and adjust content.
