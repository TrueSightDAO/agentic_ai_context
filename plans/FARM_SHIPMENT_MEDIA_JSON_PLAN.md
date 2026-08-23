# Farm & Shipment Page Media Externalization — per-page `media.json`

**Repo:** `agroverse_shop` → [TrueSightDAO/agroverse_shop_beta](https://github.com/TrueSightDAO/agroverse_shop_beta) (deploys to **beta.agroverse.shop**). Production is **agroverse_shop_prod** (**agroverse.shop**) — promoted by Gary only, never touched directly (`WORKSPACE_CONTEXT.md` §3f).

**Origin:** Gary's idea, 2026-08-20 (nelanco-claude interactive session) — farm and shipment pages hardcode their photos/YouTube embeds directly in HTML. Abstract this into a **per-page JSON file** (`media.json` next to each page's `index.html`) that a shared loader script reads at page-load time, so adding a new photo or video becomes "upload the asset to GitHub or YouTube, add one JSON entry" — no HTML edit, no redeploy of page markup.

**Why per-page JSON, not one central file (Gary's explicit call):** keeps each file small and scoped to the page it describes; avoids one giant JSON growing unbounded as more farms/shipments are added; matches the existing 1-page-1-directory layout (`farms/<slug>/index.html`, `shipments/<slug>/index.html`).

---

## 0. Pre-flight (§5d Completeness — read this once, not per PR)

### 0.1 Current state — how media is hardcoded today

Confirmed by direct inspection (2026-08-20) of all 7 `farms/*/index.html` and all 11 `shipments/*/index.html`. Two independent problems exist today:

1. **Photos and videos are typed directly into each page's HTML** — an `<img>` tag with a literal `src=`, or an `<iframe src="https://www.youtube.com/embed/<ID>?rel=0">`. Adding one more photo means hand-editing HTML.
2. **The same hero image is often duplicated 2-3 times in one page** (banner img + `.shipment-image` + `.farmer-photo`), each a separate hardcoded `src=`. This has already caused **copy-paste drift**: `shipments/agl4/index.html`'s `.farmer-photo` tag (`alt="Oscar"`) points at `agl14.avif` instead of `agl4.avif` — a real, live bug. The JSON refactor fixes this as a side effect (single hero value, multiple render slots) — call this out to whoever reviews PR1.

### 0.2 Full media inventory (captured now so no PR needs to re-discover it — reading the one file being migrated in each PR is still fine per §5d, this table is for batching/estimation only)

**Farm pages** (`farms/<slug>/index.html`, all at depth 2 from repo root):

| Page | Video sections (`.farm-video-container`) | YouTube IDs | Non-card `<img>` | Notes |
|---|---|---|---|---|
| `oscar-bahia` | 2 | `lh_dAXhE7xQ`, `BI55aQ6B73U` | 0 | Clean 2-video case. **Pilot page (PR0).** |
| `fazenda-santa-ana-bahia` | 3 | `Kn13I7ijufs`, `J80B6TgWtFs`, `PwUu7ACzBdk` | 1 (`fazenda-santa-ana-product.jpg`) | |
| `fazenda-sao-jorge-bahia` | 2 | `sLNS9pZUBVw`, `33nwH67UIag` | 2 (`sao-jorge-matheus-mailan-cacao-pods.jpg`, AGL6 shipment avif) | |
| `paulo-la-do-sitio-para` | 1 | `8PIi57AOEE0` | 0 | |
| `vivi-jesus-do-deus-itacare` | 2 | `FthJ9mftGsY`, `Z2RPqJzqS2k` | 0 | |
| `fazenda-analuana-bahia` | 0 | — | 0 | **No story media today.** Skip — no `media.json` needed unless/until content is added. |
| `fazenda-capelavelha-bahia` | 0 | — | 0 | **No story media today.** Skip, same as above. |

**Shipment pages** (`shipments/<slug>/index.html`, all at depth 2):

| Page | Hero image (dup'd 2-3×) | Farmer photo (distinct from hero?) | YouTube | Notes |
|---|---|---|---|---|
| `agl0` | `agl0.avif` | same as hero | — | Hero appears 3× (banner, `.shipment-image`, `.farmer-photo`) |
| `agl1` | `agl1.avif` | same as hero | — | Hero appears 3× |
| `agl2` | `agl2.avif` | same as hero | `Kn13I7ijufs` | |
| `agl4` | `agl4.avif` | **BUG: currently `agl14.avif`** | `BI55aQ6B73U` | **Pilot page (PR1)** — migration fixes the bug |
| `agl5` | `agl5.avif` | same as hero | — | Hero appears 3× |
| `agl6` | `agl6.avif` | same as hero | `gw2vIxPCcyQ` via **meta-tag + lazy `about:blank` iframe pattern** (different mechanism — see 0.3) | Also has `sao-jorge-matheus-mailan-cacao-pods.jpg` in-body. **Own PR (PR7).** |
| `agl7` | `agl7.gif` | same as hero | — | Hero appears 3× |
| `agl8` | `agl8.avif` | **distinct** — `assets/images/farms/paulo_profile_photo.jpeg` | — | |
| `agl10` | `agl10.avif` | same as hero | — | |
| `agl13` | `agl13.avif` | same as hero | `FthJ9mftGsY` | |
| `agl14` | `agl14.avif` | same as hero | `BI55aQ6B73U` | |

### 0.3 Existing prior-art pattern to retire (not extend)

7 pages (`shipments/agl6`, `partners/kikis-cocoa`, 3× `product-page/...`, 1× `post/...`) already externalize **one** YouTube ID each via a `<meta name="agroverse:youtube:<key>" content="<id>">` tag + a duplicated 8-line inline `<script>` that copies the ID into a lazy `<iframe src="about:blank">`. This is the closest existing precedent for "don't hardcode video IDs in markup" — it validates the direction, but it's a one-off pattern copy-pasted per page (no shared loader, no image support, no multi-item galleries). **Scope decision: only `shipments/agl6` is in this plan's scope** (it's a farm/shipment page); the `partners/`, `product-page/`, and `post/` instances are **out of scope** — different page families, not what Gary asked about. Do not touch them.

### 0.4 Reusable building blocks already in the repo (confirmed present — use these, don't reinvent)

- **CSS classes already styled** in `css/cards.css`: `.farm-videos-container`, `.farm-video-section`, `.farm-video-container`, `.farm-video` (lines ~97-220, incl. a mobile breakpoint). These are visually generic (not actually farm-specific despite the name) — **reuse them as-is for both farm and shipment story galleries. No new CSS file is needed for the gallery.**
- `.shipment-image` and `.farmer-photo` are styled **inline per-page** in each shipment page's `<style>` block (not in a shared CSS file) — confirmed via `grep` (no hits in `css/*.css`). The migration must **not** touch these `<style>` blocks; it only changes what feeds the `src=`/`alt=` of the elements those styles target.
- **Shared-component precedent to follow:** `js/shared-chrome.js` + `AGROVERSE_SHOP_PAGE_CONVENTIONS.md` — placeholder `<div>` in HTML, a script tag, JS fills it in. Same shape as this plan's loader, just JSON-fed instead of hardcoded-string-fed.
- **Fetch/render precedent to follow:** `js/partner-catalog-snippets.js` `run()` — `async` IIFE, `fetch()` wrapped in try/catch that **silently no-ops on any failure** (never throws, never blocks page render), builds DOM nodes with `document.createElement`, inserts relative to an anchor element already on the page.
- `og:image` / `twitter:image` meta tags in `<head>` are **static** and independent of on-page media — confirmed no JSON-LD `image` fields exist on these pages either. **This refactor does not touch `<head>` meta tags and introduces no drift risk there** — leave them exactly as they are.

### 0.5 Test convention for this repo (§9/§11 equivalent — confirmed, do not assume vitest/happy-dom)

`agroverse_shop` uses **Playwright** against a real browser (local `http.server` on :8000, or live `beta.agroverse.shop` in CI) — see `tests/README.md` and `.cursor/rules/ci-and-testing.mdc`. There is **no** vitest/happy-dom setup in this repo (that OPERATING_INSTRUCTIONS §9 default doesn't apply here — Playwright already satisfies the "test before merge" intent more strongly, since it's a real browser). **Every PR in this plan that changes rendering must add or extend a Playwright spec** that: loads the migrated page, asserts the hero image `src` is non-empty and matches `media.json`, asserts each gallery iframe `src` contains the right YouTube ID, and asserts **zero console errors**. Run `npm test` locally before opening each PR (starts the local server automatically).

### 0.6 Authorization envelope (§5e — scoped once, not re-asked per PR)

- **`agroverse_shop_beta`: pre-authorized.** Open branches, commit, push, open PRs freely for every unit below. **Never merge to `main` yourself** — that's the standing always-stop gate (§5c #1), true for every PR in this plan, not just the "big" ones.
- **`agroverse_shop_prod` (agroverse.shop): out of scope entirely.** Do not touch. Promotion beta→prod is Gary's action alone, on his own schedule, after he's satisfied with how the migrated pages look on beta — this plan does not include a "promote to prod" unit.
- **`agentic_ai_context`: pre-authorized for this plan file + the one conventions-doc update in PR8** (that file is not in the do-not-edit list in `OPERATING_INSTRUCTIONS.md` §3 — only `WORKSPACE_CONTEXT.md`/`PROJECT_INDEX.md`/`README.md`/`OPERATING_INSTRUCTIONS.md` are protected).
- **No TDG/money movement anywhere in this plan.** Standard AI-agent `[CONTRIBUTION EVENT]` time reporting after each merged PR is expected (§6, `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`) — that's routine, not a gate.

**✅ Pre-flight Completeness:** no execution unit requires reading a file/state not already captured in this pre-flight. Each `PRn` below only needs to open the specific page(s) it's migrating (trivial, exempted by §5d) plus this plan.

---

## 1. Design — JSON schema

One file per page, **same directory as `index.html`**, named **`media.json`**:

- `farms/<slug>/media.json`
- `shipments/<slug>/media.json`

```json
{
  "schemaVersion": 1,
  "hero": {
    "type": "image",
    "src": "https://raw.githubusercontent.com/TrueSightDAO/truesight_me/main/assets/shipments/agl4.avif",
    "fallback": "../../assets/images/hero/cacao-circles-alt.jpg",
    "alt": "AGL4 - Oscar's Farm"
  },
  "gallery": [
    {
      "type": "youtube",
      "videoId": "lh_dAXhE7xQ",
      "title": "Hear from Oscar: The Family Story",
      "caption": "Oscar shares the story of three generations of cacao wisdom and how his grandfather's vision continues to shape the farm today."
    },
    {
      "type": "image",
      "src": "../../assets/images/shipments/sao-jorge-matheus-mailan-cacao-pods.jpg",
      "alt": "Matheus and Mailan at São Jorge Farm holding cacao pods",
      "title": null,
      "caption": null
    }
  ]
}
```

**Field rules:**

- `hero` — optional object, `null`/omitted if the page has no single "banner" photo (rare; all current shipment pages have one, some farm pages don't).
  - `type`: `"image"` only for now (kept for forward-compat if a hero video is ever wanted).
  - `src`: required. Either a **root-relative repo path** (`../../assets/images/...`, matches existing convention) or a **full URL** (e.g. the existing `raw.githubusercontent.com/TrueSightDAO/truesight_me/...` cross-repo hosting pattern for shipment avifs) — both forms already coexist today, the schema doesn't force a single hosting choice.
  - `fallback`: optional. Path/URL to show `onerror`. If omitted, the loader falls back to the sitewide default `../../assets/images/hero/cacao-circles-alt.jpg` (matches the most common existing fallback).
  - `alt`: required (accessibility; also fixes the current agl4 alt/src mismatch bug by construction).
- `gallery` — array, default `[]`. Each entry:
  - `type`: `"youtube"` or `"image"`.
  - `"youtube"` → `videoId` (required, the bare 11-char ID, not a full URL — loader builds `https://www.youtube.com/embed/<id>?rel=0`).
  - `"image"` → `src` (required, same path/URL rules as hero), `alt` (required).
  - `title`: optional string. If present, loader renders an `<h3>` above the media (matches current farm-page pattern). Omit/`null` to render no heading.
  - `caption`: optional string. If present, loader renders a `<p>` below the media (matches current pattern). Omit/`null` for no caption.

**Not in scope for the JSON:** the `items-grid`/`item-card` blocks ("Shipments from This Farm", "Products from This Shipment") stay exactly as they are — those are cross-reference grids driven by other data relationships, not this page's own story media, and are explicitly out of scope (see `AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md` for that separate system).

---

## 2. Design — loader script (`js/media-gallery.js`)

New file, following the `partner-catalog-snippets.js` fetch/render style and the `shared-chrome.js` placeholder style:

```js
(function () {
  async function run() {
    var heroEls = document.querySelectorAll('[data-media-slot="hero"]');
    var galleryEl = document.getElementById('media-gallery');
    if (!heroEls.length && !galleryEl) return; // page hasn't opted in — no-op

    var data = null;
    try {
      var res = await fetch('./media.json');
      if (!res.ok) return;
      data = await res.json();
    } catch (e) {
      return; // never break the page over a missing/malformed JSON
    }
    if (!data) return;

    // Hero: fill every matching slot (fixes today's copy-paste-per-slot duplication)
    if (data.hero && data.hero.src) {
      heroEls.forEach(function (el) {
        el.src = data.hero.src;
        el.alt = data.hero.alt || '';
        var fallback = data.hero.fallback || '../../assets/images/hero/cacao-circles-alt.jpg';
        el.onerror = function () { el.src = fallback; el.onerror = null; };
      });
    }

    // Gallery: build each item fresh, reusing existing CSS classes (no new CSS)
    if (galleryEl && Array.isArray(data.gallery)) {
      data.gallery.forEach(function (item) {
        var section = document.createElement('div');
        section.className = 'farm-video-section';
        if (item.title) {
          var h3 = document.createElement('h3');
          h3.textContent = item.title;
          section.appendChild(h3);
        }
        var wrap = document.createElement('div');
        wrap.className = 'farm-video-container';
        if (item.type === 'youtube' && item.videoId) {
          var iframe = document.createElement('iframe');
          iframe.className = 'farm-video';
          iframe.src = 'https://www.youtube.com/embed/' + item.videoId + '?rel=0';
          iframe.setAttribute('frameborder', '0');
          iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
          iframe.allowFullscreen = true;
          wrap.appendChild(iframe);
        } else if (item.type === 'image' && item.src) {
          var img = document.createElement('img');
          img.className = 'farm-video';
          img.loading = 'lazy';
          img.src = item.src;
          img.alt = item.alt || '';
          wrap.appendChild(img);
        } else {
          return; // skip malformed entries rather than fail the whole gallery
        }
        section.appendChild(wrap);
        if (item.caption) {
          var p = document.createElement('p');
          p.textContent = item.caption;
          section.appendChild(p);
        }
        galleryEl.appendChild(section);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
```

**Per-page HTML changes required (mechanical, same shape every time):**

1. Any existing hero `<img>` (banner / `.shipment-image` / `.farmer-photo`) gets `data-media-slot="hero"` added and its hardcoded `src=`/`alt=` **removed** (or left as a same-value placeholder — removing is cleaner and makes "not yet loaded" states visibly obvious in review).
2. The existing `.farm-videos-container` (or, for shipment pages that don't have one yet, a new empty `<div class="farm-videos-container" id="media-gallery"></div>` placed where the video/photo section currently sits) has its **entire existing child content deleted** and replaced by the empty `id="media-gallery"` container — the loader rebuilds all children from JSON.
3. Add `<script src="../../js/media-gallery.js"></script>` near the other page-specific scripts at the bottom of `<body>` (depth-relative path, matching `navigation.js`/`cart.js` convention — **not** root-relative like `shared-chrome.js`, since this script isn't loaded on every page site-wide).
4. `agl6` additionally **loses** its bespoke `<meta name="agroverse:youtube:...">` tag and its 8-line inline `<script>` — both are fully superseded by `media.json` + the shared loader (PR7).

No CSS changes anywhere in this plan — `.farm-video-section`/`.farm-video-container`/`.farm-video` already exist and are reused verbatim; `.shipment-image`/`.farmer-photo` inline page styles are untouched (they still just style whatever the now-JS-set `src`/`alt` produces).

---

## 2a. Reference example JSON for the pilot pages (for the PR0/PR1 executor — not required reading for later PRs)

`farms/oscar-bahia/media.json` (PR0):
```json
{
  "schemaVersion": 1,
  "gallery": [
    { "type": "youtube", "videoId": "lh_dAXhE7xQ", "title": "Hear from Oscar: The Family Story", "caption": "Oscar shares the story of three generations of cacao wisdom and how his grandfather's vision continues to shape the farm today." },
    { "type": "youtube", "videoId": "BI55aQ6B73U", "title": "Witness the Cacao Selection Process", "caption": "See how Oscar's team carefully selects cacao beans, maintaining the quality standards passed down through generations." }
  ]
}
```

`shipments/agl4/media.json` (PR1 — note the corrected farmer-photo, fixing the live `agl14.avif` bug):
```json
{
  "schemaVersion": 1,
  "hero": {
    "type": "image",
    "src": "https://raw.githubusercontent.com/TrueSightDAO/truesight_me/main/assets/shipments/agl4.avif",
    "fallback": "../../assets/images/hero/cacao-circles-alt.jpg",
    "alt": "AGL4 - Oscar's Farm"
  },
  "gallery": [
    { "type": "youtube", "videoId": "BI55aQ6B73U", "title": null, "caption": null }
  ]
}
```
(Exact `title`/`caption` text for the agl4 video should be copied from the surrounding `<p>`/`<h3>` in the current markup if any exist — verify against the live file, not just this table, since this plan captured structure/inventory, not necessarily every caption's exact wording.)

---

## 3. Sequenced plan — one PR per turn (§5a)

Every `PRn` below is independently shippable against current `main`, assuming the previous `PRn-1` has already merged (standard sequential dependency — PR0's `js/media-gallery.js` must exist before PR1+ pages can reference it). None require prod, default-branch merge, or money — so **none carry an extra `gate:` marker**; the standing always-stop-before-merge rule (§5c #1) applies to all of them the same way it applies to every PR in this workspace. **PR9 (UAT) is the one exception** — UAT is itself an always-stop trigger per §5c #1.

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | Add `js/media-gallery.js`. Migrate **`farms/oscar-bahia`** only (2-video clean case). Add Playwright spec `tests/media-gallery-farm.spec.ts` (hero N/A for this page — asserts both iframe `src`s + zero console errors). | auto |
| **PR1** | Migrate **`shipments/agl4`** (hero + 1 video; fixes the `agl14.avif` farmer-photo bug as part of the diff — call this out explicitly in the PR description). Add `tests/media-gallery-shipment.spec.ts` (asserts hero `src` correct on all slots + video). | auto |
| **PR2** | Migrate farm pages **`fazenda-santa-ana-bahia`** + **`paulo-la-do-sitio-para`** (5 media items total). Extend the farm Playwright spec to cover both. | auto |
| **PR3** | Migrate farm pages **`fazenda-sao-jorge-bahia`** + **`vivi-jesus-do-deus-itacare`** (6 media items). Extend spec. **Note:** `fazenda-analuana-bahia` and `fazenda-capelavelha-bahia` have zero story media today — no `media.json` needed for either; do not create empty stub files, do not add a script tag to those two pages. | auto |
| **PR4** | Migrate shipment pages **`agl0`, `agl1`, `agl2`** (hero-only ×2 + hero+1-video ×1). Extend shipment spec. | auto |
| **PR5** | Migrate shipment pages **`agl5`, `agl7`, `agl8`** (hero-only ×2 + hero+distinct-farmer-photo ×1 — `agl8`'s farmer photo is a genuinely different image from its hero, verify the JSON keeps them distinct, don't collapse into one hero value). Extend spec. | auto |
| **PR6** | Migrate shipment pages **`agl10`, `agl13`, `agl14`** (hero-only ×1 + hero+1-video ×2). Extend spec. | auto |
| **PR7** | Migrate **`shipments/agl6`** — the special case: retire its `<meta name="agroverse:youtube:agl6-sao-jorge-hot-chocolate">` tag and its bespoke inline lazy-load `<script>` entirely, replacing both with `media.json` + the shared loader (this is the one page proving the new system fully supersedes the old ad-hoc meta-tag pattern, not just coexists with it). Extend spec. | auto |
| **PR8** | Doc update in **`agentic_ai_context`** (separate repo, direct small PR against its `main`): add a short "§8 — Farm/shipment story media (JSON-driven)" section to `conventions/AGROVERSE_SHOP_PAGE_CONVENTIONS.md` documenting the `media.json` schema, the `data-media-slot="hero"` / `id="media-gallery"` placeholder convention, and a link to this plan, so future agents adding a new farm/shipment page follow the new pattern instead of hardcoding. | auto |
| **PR9 — UAT** | Human-facing verification on **beta.agroverse.shop** after PR0-PR8 are all merged (see §4 below). | **gate: UAT (always-stop, §5c)** |

**Recommended (soft) checkpoint, not a hard gate:** PR0 is the pattern everything else replicates 8 more times. Worth Gary skimming PR0's diff once it's open before PR1-PR8 stamp out the same shape — cheap insurance, not a blocking requirement.

**Out of scope, do not add as a unit:** promoting to `agroverse_shop_prod`/production `agroverse.shop`. That's Gary's call, on his own timing, after he's looked at the UAT results on beta.

### Resume tracker

| Unit | PR opened | Merged (human) | Contribution reported |
|---|---|---|---|
| PR0 — loader + oscar-bahia pilot | ☑ | ☑ | ☑ |
| PR1 — agl4 pilot + bug fix | ☑ | ☑ | ☑ |
| PR2 — santa-ana + paulo | ☑ | ☑ | ☑ |
| PR3 — sao-jorge + vivi | ☑ | ☑ | ☑ |
| PR4 — agl0, agl1, agl2 | ☑ | ☑ | ☑ |
| PR5 — agl5, agl7, agl8 | ☑ | ☑ | ☑ |
| PR6 — agl10, agl13, agl14 | ☑ | ☑ | ☑ |
| PR7 — agl6 (retire meta-tag pattern) | ☑ | ☑ | ☑ |
| PR8 — conventions doc update | ☑ | ☑ | ☑ |
| PR9 — UAT on beta | ☑ (n/a, not a PR) | — | — |

**RESUME HERE = Plan complete.** UAT verified on beta.agroverse.shop 2026-08-20 (all 7 criteria pass, Playwright headless vs live beta). Remaining decision: promotion to prod (agroverse_shop_prod) is Gary's separate call, out of plan scope.

---

## 4. UAT (User Acceptance Testing) — PR9

Runs on **beta.agroverse.shop** only, after PR0-PR8 are merged and the beta site has rebuilt (GitHub Pages serves directly from `agroverse_shop_beta`'s `main` — no separate deploy step; live within minutes of merge).

| Step | Surface / URL | What to expect | Interaction | Acceptance criterion |
|---|---|---|---|---|
| U1 | `beta.agroverse.shop/farms/oscar-bahia/` | Two videos render under "Hear from Oscar" / "Cacao Selection Process" headings, same as before migration | Load page, open DevTools console | Both iframes play when clicked; zero console errors |
| U2 | `beta.agroverse.shop/shipments/agl4/` | Hero photo (Oscar's farm) shows correctly in the banner **and** in the "farmer photo" spot — both now the same correct AGL4 image (previously the farmer photo wrongly showed AGL14) | Load page, visually compare banner vs. farmer-photo image | Both images match, no visibly broken/missing image, no console errors |
| U3 | Each remaining migrated farm page (`fazenda-santa-ana-bahia`, `fazenda-sao-jorge-bahia`, `paulo-la-do-sitio-para`, `vivi-jesus-do-deus-itacare`) | All videos + in-body photos present, headings/captions read the same as before migration | Load each page, skim visually against a pre-migration screenshot or memory of the page | No missing media, no layout shift/breakage |
| U4 | Each remaining migrated shipment page (`agl0, agl1, agl2, agl5, agl7, agl8, agl10, agl13, agl14`) | Hero + farmer photo (+ video where applicable) all present | Load each page | No missing media, `agl8`'s farmer photo still shows Paulo (not the shipment hero) |
| U5 | `beta.agroverse.shop/shipments/agl6/` | Video now loads without the old meta-tag/lazy-swap mechanism; in-body photo still present | Load page, confirm video plays | No console errors, no reference to the removed `agroverse:youtube:agl6-...` meta tag needed |
| U6 | Any one migrated page, throttled/offline network (simulate `media.json` fetch failure via DevTools) | Page still renders without crashing; hero falls back to `cacao-circles-alt.jpg` or simply shows nothing broken; no JS error thrown | DevTools → Network → block `media.json` request → reload | No uncaught exception in console; rest of page (nav, footer, cart) still functions |
| U7 | `farms/fazenda-analuana-bahia/` and `farms/fazenda-capelavelha-bahia/` (untouched pages) | Pages render exactly as before — confirms the "skip pages with no media" decision didn't break anything | Load both pages | Unchanged from pre-plan behavior |

**Pass/fail:** all 7 steps must pass before Gary considers promoting to prod (his separate, manual decision — not part of this plan).

---

## 5. Contribution reporting

Standard per-unit convention (`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`, `OPERATING_INSTRUCTIONS.md` §6): after each PR merges, report a `[CONTRIBUTION EVENT]` via `dao_client` before starting the next unit. Contributor name for Sophia's work: **`Sophia Truesight`** exactly (§5b) — never a variant.

---

*Drafted by Claude Anthropic (nelanco-claude interactive session) on 2026-08-20 at Gary's request, for handoff to Sophia. Pre-flight inventory (§0) gathered by direct inspection of `agroverse_shop` — see this file's own commit for the research this plan is based on.*
