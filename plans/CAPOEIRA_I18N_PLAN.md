# Capoeira Site — English/Portuguese Toggle with Persisted Preference

**Status:** plan drafted, not yet triggered. No code yet.
**Owner:** Gary Teh · **Drafted by:** Claude Anthropic (Envoy), 2026-09-24, from live repo inspection.
**Requested by:** Gary Teh, 2026-09-24 — "the site is starting to gain more exposure, right now it
is all in English... every single page should allow the user to flip between English and Portuguese
and retain that preference," matching `sunmint.truesight.me`'s existing toggle.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**
> Report the DAO contribution after each merge (§6).

---

## 0. Decisions needed (per §5e — batch these, ask once)

| # | Decision | Proposed default | Needs Gary? |
|---|---|---|---|
| 0.1 | Default language on first visit | **English** (site's current/only language today; unlike SunMint, which defaults to `pt` because its users are Brazilian farmers — capoeira's current audience is presumed English-first, given zero PT exists yet) | Confirm — could also default by browser `navigator.language`. |
| 0.2 | Translation authorship | AI-assisted first-draft Portuguese (same pattern as `LAB_REPORT_TRANSLATION.md`'s Grok-assisted approach), then a **native-Portuguese-reader review pass before the final page goes live** — this serves Tribo Bahia Mirim's actual Brazilian community, so inaccurate PT is a real credibility risk, not just a nice-to-have polish step. | Confirm reviewer (Gary himself, or someone in the Bahia/Bico Duro community) — flagged as a UAT gate either way (§5). |
| 0.3 | No beta environment exists for this repo | Test each page locally (`file://` or a local static server) before merge; treat **PR1 as its own mini-gate** — confirm the mechanism actually works correctly on one real page, in the actual live site, before rolling out to the other 7. | Implicit unless Gary wants a preview branch stood up first (adds scope, not recommended for a display-only feature). |

---

## 1. Pre-flight — captured facts (§5d: no PR below should need to re-discover any of this)

### 1.1 The reference implementation — `sunmint_beta/index.html` (verified live, 2026-09-24)

Confirmed via `git show origin/main:index.html` (952 lines, single-page app) rather than a possibly
stale local clone:

- **Toggle markup** (line ~231): two buttons in a `.lang-toggle` div, `id="langPt"`/`id="langEn"`,
  each `onclick="setLang('pt'|'en')"`, `.active` class for the current selection.
- **Dictionary** (line ~317): `const I18N = { pt: {...}, en: {...} }` — one flat object per language,
  matching string keys (`intro`, `navLabel`, `treeHeading`, etc.) — appropriate there because it's a
  single-page app with one shared vocabulary; **not** directly appropriate for capoeira, which has 8
  physically separate pages (see §1.3).
- **Lookup helper** (line 452): `function t(key) { return (I18N[currentLang] && I18N[currentLang][key]) || I18N.pt[key] || key; }`
  — falls back to `pt` (SunMint's default), then to the literal key if truly missing.
- **Apply function** (line 456): `setLang(lang)` — sets `currentLang`, `localStorage.setItem('sunmint_lang', lang)`,
  `document.documentElement.lang = lang`, toggles both buttons' `.active` class, then:
  ```js
  document.querySelectorAll('[data-i18n]').forEach((el) => { el.textContent = t(el.getAttribute('data-i18n')); });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => { el.setAttribute('placeholder', t(el.getAttribute('data-i18n-placeholder'))); });
  ```
- **Persistence** (line 425): `let currentLang = localStorage.getItem('sunmint_lang') || 'pt';` — read once
  on load; `setLang(currentLang)` is called on page init (line ~939) so the UI matches the stored
  preference immediately.
- **Markup contract**: any element that needs translating carries `data-i18n="key"` (for text content)
  or `data-i18n-placeholder="key"` (for input placeholders); the *initial* HTML content of that element
  is the PT string (SunMint's default language), overwritten by `setLang()` on load/toggle.

### 1.2 Capoeira repo — current state (verified live, 2026-09-24, not from a stale doc)

`PROJECT_INDEX.md`'s capoeira entry (4 pages: index/library/practice/transparency) is **stale** — the
live repo has grown to **8 pages**, confirmed via `git log`/`find` against `origin/main`
(`18d36a7d`, 2026-09-02):

| Page | Lines | Uses `nav.js`? | `<html lang>` |
|---|---|---|---|
| `index.html` | 311 | yes | `en` |
| `practice.html` | 283 | yes | `en` |
| `roda.html` | 397 | yes | `en` |
| `library.html` | 135 | yes | `en` |
| `transparency.html` | 152 | yes | `en` |
| `berimbau.html` | 114 | yes | `en` |
| `community.html` | 117 | yes | `en` |
| `roots.html` | 112 | yes | `en` |

**Every page is English-only today** — zero Portuguese content exists anywhere in the repo. Total
~1,676 lines across 8 files.

- **`assets/js/nav.js`** (55 lines) already exists and is included on **all 8 pages** — a shared
  hamburger-menu behavior script with a documented "markup contract" (its own comment: *"Include with:
  `<script src="assets/js/nav.js" defer></script>`"*, requires `#hamburger-btn` + `#primary-nav-links`
  in each page's own markup). **This plan's `assets/js/i18n.js` should follow the exact same
  convention** — one shared behavior file, a documented minimal per-page markup contract — since it's
  already the established pattern in this specific repo.
- **The nav *links* markup itself is duplicated per page**, not injected from one shared source (unlike
  `agroverse_shop`'s `js/shared-chrome.js`, which does inject nav/footer markup). So adding a toggle
  **button** to the header means either (a) duplicating a small markup snippet across all 8 pages, or
  (b) having `i18n.js` create and insert the toggle DOM nodes itself into a documented mount point —
  **recommend (b)**, consistent with `nav.js`'s existing "minimal markup contract, behavior in JS" style.
- **Deploy**: per `capoeira/README.md`, GitHub Pages deploys **directly from `main`**, custom domain
  `capoeira.agroverse.shop` — **there is no beta/staging repo for this site** (unlike
  `agroverse_shop_beta`/`truesight_me_beta`/`dapp_beta`). Merging a PR to `main` here **is** the
  production deploy. This is why §0.3 above treats PR1 as its own gate and recommends local testing
  before every merge, not just at the end.
- **No i18n code of any kind exists yet** in this repo — confirmed via repo-wide grep for
  `i18n`/`lang-toggle`/`data-i18n`/`localStorage`.

### 1.3 Why capoeira's dictionary shape must differ from SunMint's

SunMint is a single HTML file (a client-side "app" with an internal page-picker dropdown, not real
separate URLs) — one flat `I18N.{pt,en}` object is fine because there's one shared vocabulary.
Capoeira has **8 real, separately-loaded pages** with mostly distinct content. A single giant shared
dictionary would still work correctly, but would bloat every page load with 7 other pages' strings and
invite key collisions as content grows. **Proposed shape:**

- `assets/js/i18n.js` — shared engine: `t()`, `setLang()`, the DOM-apply loop (identical logic to
  SunMint's), localStorage key **`capoeira_lang`** (namespaced, not reusing `sunmint_lang`), and the
  toggle-button DOM injection (§1.2's point (b)).
- `assets/js/i18n/common.js` — one shared dictionary for strings that appear on **every** page: nav
  links, footer, the toggle button labels themselves ("English"/"Português").
- Each page keeps a **small inline `<script>` block** defining `window.I18N_PAGE = { en: {...}, pt: {...} }`
  for that page's own content — `i18n.js` merges `I18N_PAGE` over `I18N_COMMON` at init. This mirrors
  `nav.js`'s existing "shared behavior + small required per-page markup" convention rather than
  introducing a new architectural pattern to this repo.

---

## 2. Authorization envelope (§5e — ask once, not per PR)

| Surface | Envelope |
|---|---|
| `capoeira` repo — **there is no beta repo; every merge to `main` is a live production deploy.** | Pre-authorized for the **engineering** PRs (PR1–PR9 below) **conditional on local testing before each merge** (§0.3) — this is a display-only, additive feature (no checkout/payment/session-booking logic touched), so the blast radius of a visual bug is low, but Gary should say if he wants a human look-over before merge regardless, given there's no staging buffer. |
| **Translation content itself (PT strings)** | **Not** pre-authorized to go live unreviewed — §0.2's native-reader review pass is a real gate, not a formality, given this serves an actual Brazilian community. Flag as UAT (§5), not skippable. |
| `agentic_ai_context` (this plan + manifest row) | Pre-authorized, feature branch + PR (Envoy can't self-merge here — same as every other plan this session). |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Build `assets/js/i18n.js` (shared engine) + `assets/js/i18n/common.js` (nav/footer/toggle strings, en+pt) + wire the toggle into **`index.html` only** as the reference page: mark up its content with `data-i18n`, write `window.I18N_PAGE` for it, AI-draft the PT strings. **This is the mechanism-proving PR — test locally, then merge and verify live on `capoeira.agroverse.shop` before starting PR2.** | `capoeira` |
| **PR2** | Roll the same pattern onto `practice.html` (283 lines — the second-largest page; doing it second, right after the reference page, surfaces any pattern gaps early while the context is still fresh). | `capoeira` |
| **PR3** | `roda.html` (397 lines, the largest page). | `capoeira` |
| **PR4** | `library.html`. | `capoeira` |
| **PR5** | `transparency.html`. | `capoeira` |
| **PR6** | `berimbau.html`. | `capoeira` |
| **PR7** | `community.html`. | `capoeira` |
| **PR8** | `roots.html` (last page — after this, all 8 are covered). | `capoeira` |
| **PR9** | **Cross-page persistence QA pass** (the actual feature Gary asked for, not just per-page toggles working in isolation): confirm that choosing a language on any one page and then navigating to any other page (via the nav links) keeps that language selected — this is the `localStorage` read-on-load working correctly across all 8 pages, not just each page's own toggle button. Fix any page where it doesn't. | `capoeira` |
| **PR10** | Docs: add an `assets/js/i18n.js`-doc-comment "markup contract" (same style as `nav.js`'s own header comment) so a **9th page added later** follows the pattern automatically; update `capoeira/README.md`'s page list (also stale — doesn't mention i18n or all 8 current pages); note in `agentic_ai_context/PROJECT_INDEX.md`'s capoeira row is due for a refresh too (flag via `CONTEXT_UPDATES.md`, don't edit `PROJECT_INDEX.md` directly per §3's canonical-file rule). | `capoeira` / `agentic_ai_context` |
| **UAT** | See §5. **Gate — native-Portuguese-reader review**, not skippable per §0.2/§2. | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (build the shared i18n engine + wire up `index.html` as the reference
> implementation). Fresh roadmap — nothing has started.
>
> **Open before certain units:** §0.1 (default language) and §0.2 (who reviews the PT translations)
> are real governor decisions, not blocking PR1's *engineering* work, but §0.2's reviewer should be
> lined up before PR1's translations are considered done, not after all 8 pages are built.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (i18n engine + common dict + `index.html` reference) | ☐ | ☐ | ☐ |
| PR2 (`practice.html`) | ☐ | ☐ | ☐ |
| PR3 (`roda.html`) | ☐ | ☐ | ☐ |
| PR4 (`library.html`) | ☐ | ☐ | ☐ |
| PR5 (`transparency.html`) | ☐ | ☐ | ☐ |
| PR6 (`berimbau.html`) | ☐ | ☐ | ☐ |
| PR7 (`community.html`) | ☐ | ☐ | ☐ |
| PR8 (`roots.html`) | ☐ | ☐ | ☐ |
| PR9 (cross-page persistence QA) | ☐ | ☐ | ☐ |
| PR10 (docs) | ☐ | ☐ | ☐ |
| UAT (native-PT-reader review) | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** SunMint's exact mechanism (file/line refs), capoeira's real
current page list/sizes/shared-JS convention (verified live, not from the stale `PROJECT_INDEX.md`
entry), the no-beta-repo deploy risk, and the dictionary-shape rationale are all captured in §1. §0.1
and §0.2 are genuine open governor decisions, not undiscovered facts.

---

## 5. UAT — the review gate, not a formality

| Step | Surface | What to expect | Acceptance criterion |
|---|---|---|---|
| 1 | Each page, locally, before its own PR merges | Toggle switches all `data-i18n`/`data-i18n-placeholder` content, `<html lang>` updates | No English string remains visible after switching to `pt`, and vice versa |
| 2 | After PR9, live on `capoeira.agroverse.shop` | Set language on page A, click a nav link to page B | Page B loads already in the chosen language — this is the actual "retain that preference" feature, not just a working toggle |
| 3 | **Native-Portuguese-reader pass** (§0.2) | Read every PT string in context | Flags anything machine-translation-awkward or culturally off before/shortly after the affected pages are live — given this serves Tribo Bahia Mirim's own Brazilian community, this read matters more than usual |
| 4 | Mobile viewport (this site already has a hamburger nav — confirm the toggle doesn't collide with it) | Toggle button visible and usable at phone width | No overlap with the hamburger menu, no horizontal scroll introduced |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first) before starting the next unit.
