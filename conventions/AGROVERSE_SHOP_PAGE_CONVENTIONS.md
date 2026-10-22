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
| Farm/shipment story media | `agroverse_shop/js/media-gallery.js` + per-page `media.json` (see §8) |
| Cross-linking related entities | This file §9 |
| Published farm media manifests | `TrueSightDAO/farm_media_manifests` → `galleries/<slug>.json` (see §8) |
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
page-load time. Adding a photo or video becomes "upload the asset, add one JSON entry" — no HTML edit.

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

---

## 9. Cross-linking related entities (two-way, mandatory)

When two entities on the site share a **real** relationship, both pages MUST link to each other. A reader
arriving on either side should be able to reach the other in one click.

### What counts as a real relationship

Only relationships that exist in the record — never inferred adjacency:

- a **school/program ↔ the land of its students** (e.g. CFR Anapu ↔ Sítio Catarinense, whose owner
  Jhordan is a CFR student)
- a **partner/cooperative ↔ a program it participates in**
- a **farm ↔ the shipment batches** that shipped from it
- a **farm ↔ the partner page** representing the same physical operation

Do **not** cross-link merely because two entities are in the same region, the same country, or were
onboarded by the same person. Proximity is not a relationship.

### Rules

1. **Both directions, always.** A one-way link is a defect. The two edits ship in the same PR.
2. **Link the most specific target that exists.** Where both a `/partners/<slug>/` page and a
   `/farms/<slug>/` profile exist, link **both** — the partner page is the commercial view, the farm page
   is the land/impact view.
3. **State the relationship in words.** Never ship a bare link or a "Related" chip row. One sentence naming
   the relation ("Jhordan is a student at …; Sítio Catarinense is one of those properties.") so the reader
   knows *why* the link exists and so the claim is auditable.
4. **Reciprocity is part of definition-of-done** for any new partner / farm / program page. Adding an
   entity means adding its inbound *and* outbound links in the same PR.
5. **Cross-links are not navigation.** Do not put them in the injected nav/footer (§1/§2) — they belong in
   page content, next to the claim they support.

### Placement

- Relationship block near the end of the page's main `content-section`, **above** the partner-navigation /
  back-link area.
- Use the existing CSS variables (`var(--color-primary)`, `var(--color-text-light)`) — do not add a
  stylesheet.
- A quiet callout (light background, left rule) reads as context; a full card competes with the entity's
  own card.

### Reference implementation

`partners/cfr-anapu-dorothy-stang/index.html` ↔ `partners/sitio-catarinense-para/index.html` — the
"Land tied to this school" block and the "Jhordan is a student at …" sentence. Both sides name the
relationship and link to both the partner page and the farm profile.

### Why this is a rule

An entity that cannot be found from the entity it belongs to is, to a reader, an orphan. The
discovery-surface lint (`partner-discovery-lint.yml`) checks only the hub card, the nav data
(`js/partners-data.js`) and the locations feed (`partner_locations.json`) — it **cannot** catch a missing
cross-link. This is the one discovery surface held by convention rather than by CI, so it needs to be
written down and checked in review.

---

## 10. Shipping a change — beta first, live UAT, then prod

This is the playbook for shipping a change to a **beta/prod static site pair**. The cross-repo rule it
extends is `OPERATING_INSTRUCTIONS.md` **§9** (HTML/JS test-before-merge); this section adds what
§9 does not cover — verification of the *rendered* page, and the beta→prod hop.

It lives in this file because `agroverse_shop` is where the pattern was worked out, but the sequence
applies to **all four** pairs in the workspace. The commands below are agroverse's; substitute the
pair you are working on.

| Beta repo | Beta host | Prod repo | Prod host |
|---|---|---|---|
| `agroverse_shop_beta` | `beta.agroverse.shop` | `agroverse_shop_prod` | `agroverse.shop` |
| `truesight_me_beta` | `beta.truesight.me` | `truesight_me_prod` | `truesight.me` |
| `dapp_beta` | `beta.dapp.truesight.me` | `dapp_prod` | `dapp.truesight.me` |
| `sunmint_beta` | `beta.sunmint.truesight.me` | `sunmint_prod` | `sunmint.truesight.me` |

Every pair is a **fork** with an intentionally different `CNAME`, exactly as that table shows. That is
the single most important fact for the promotion step below.

### Opened, merged, and deployed are three different things

| State | What it means | How you know it is true |
|---|---|---|
| **Opened** | A PR exists | the PR URL |
| **Merged** | The commit is on `main` of the beta repo | the merge SHA |
| **Deployed** | GitHub Pages rebuilt and the live site serves it | you fetched the URL and saw it |

**Rule:** state which of the three you are claiming. Reporting "merged" as though it were
"deployed" is the most common way a governor is told something is finished when it is not, and it
has happened on this repo more than once.

The sequence is **merge to the beta repo first → verify the live rendered URL → governor clears it →
only then promote to prod.**

### Why the live URL, not the diff

A diff proves the bytes changed. It cannot prove the page renders, that the stylesheet applies, that
`shared-chrome.js` / `js/nav.js` injected the nav and footer, that `partners-data.js` built the hub,
or that nothing else on the page broke. `visual_uat` against the **deployed beta URL** checks the real
thing: DOM text assertions, console errors, failed requests, broken images, at desktop and mobile.

1. Open the PR against the beta repo and review the diff.
2. Merge to beta.
3. **Wait for the Pages rebuild.** Observed lag is **~2–3 minutes** (2026-10-22: prod sync at
   05:01:50 UTC, Pages served the new commit at 05:04). Do not report success before fetching the
   URL. If the change is not there on first load it is almost certainly the build, not a failed
   merge — re-check before concluding either way.

   You do not have to guess whether the build finished. The merge commit carries GitHub Pages'
   own runs:

   ```bash
   gh api repos/TrueSightDAO/agroverse_shop_beta/commits/<sha>/check-runs \
     --jq '.check_runs[] | "\(.name): \(.conclusion)"'
   ```

   Look for `build: success`, `deploy: success` and `report-build-status: success`. `deploy: success`
   plus a fetched page is two-part proof. (`Visual Consistency` will also appear — it runs on
   `deployment_status`, so it may be `skipped` rather than run; `skipped` is not `failed`.)

4. Run `visual_uat` against the live beta URL.
5. The governor reviews the live page and explicitly clears promotion.
6. Promote with `sync_beta_to_prod`.

This does not conflict with the always-stop on a "UAT / human-acceptance phase"
(`OPERATING_INSTRUCTIONS.md` §5c). A UAT needs a live URL, and beta is the live review surface —
merge-to-beta is a **prerequisite** for UAT, not a way around it. **Prod promotion remains an
always-stop.**

### Know exactly what gated the change — it differs per site

Do not imply a gate that did not run, and do not assume **no** gate ran either. PR-time coverage
differs per pair, and asserting the wrong one is a factual error in a PR body either way:

| Pair | PR-time workflow | What it actually asserts |
|---|---|---|
| `agroverse_shop_beta` | `partner-discovery-lint.yml` (on `partners/**`, `js/partners-data.js`, `partner_locations.json`) | Only that the **discovery surfaces** agree — hub card, `partners-data.js`, `partner_locations.json`. A `partners/<slug>/index.html` edit **does** trigger it, and it **passes without reading your prose.** |
| `truesight_me_beta` | `nav-consistency.yml` (on `push` **and** `pull_request`) | That **every** non-redirect `*.html` page includes the `id="site-nav"` placeholder. A real structural gate on any page edit. |
| `dapp_beta` | `ci.yml` (on `pull_request`) | Repo test suite — not a page-structure lint. |
| `sunmint_beta` | *(none found)* | — |

On **all** pairs, `visual-consistency.yml` is triggered by `deployment_status` — it runs **after** a
deploy and therefore **cannot** gate a PR.

Three consequences worth stating plainly:

- On agroverse, a prose edit **does** get a green check, but that check says nothing about the prose.
  Passing it is not evidence your sentence is right — only that the page is still discoverable.
- On truesight, an HTML edit is **structurally** gated, so a red `Nav consistency` genuinely means a
  broken page. Do not wave it through as "might not have fired".
- Never write "CI passed" as though it validated the content. Name the check and say what it covers.

`npm test` on both `agroverse_shop_beta` and `truesight_me_beta` is **Playwright against a served
site** (`playwright test`), which may not be runnable from an agent's box. Say so rather than
implying it ran. What *is* runnable locally:

- `git diff --stat` and `git diff -U1` — assert the scope ("1 file changed, 2 insertions(+)")
  rather than estimating it.
- HTML well-formedness with a parser — assert `unclosed == 0` and `mismatches == 0`, and capture
  the **baseline before** the edit so pre-existing breakage is not silently attributed to it.
- A no-new-CSS assertion — count styling attributes before and after; equal counts prove none
  were added.
- `npm run sitemap:check` where the repo provides it.

Scope placement checks to the container you are testing. Anchoring on a bare string can match a CSS
rule inside the page's own `<style>` block and return a confident false negative.

### Promoting beta → prod

Every prod repo is a real fork, not the same repo. Before calling `sync_beta_to_prod`:

1. **Dry-run the merge locally** and read the real conflict list. Do not predict a conflict by
   eyeballing which files differ — check the commit graph.
2. **Rule out a silent fast-forward.** If prod is an ancestor of beta
   (`git merge-base --is-ancestor`), advancing beta can overwrite prod's divergent files with **no
   conflict at all**. The `CNAME` difference in the table above is exactly the file at risk.
3. **Confirm `CNAME` is not in `prod_sync_generated_globs`** (currently `['stats/*.json']` only) so
   the auto-reconcile path cannot flip the production domain.
4. **Never force.** On a real conflict, stop and report it.

Then verify prod exactly as beta was verified: fetch the live domain and confirm the change is
served. The merge is not the finish line.

### Name the one decision that needs a human

Whoever opens the PR has already made the editorial and structural calls. Do not launder those as
though they were forced by the code — **surface the single line or decision most likely to need
human judgment**, in the PR body and in the message asking for review, so the reviewer can look
where it matters instead of treating everything as equally settled.

Real examples (2026-10-22, CFR Anapu "About Dorothy Stang" section):

- **A premise was wrong.** The brief asked for the school's "founder". She was murdered in 2005 and
  could not have founded a school carrying her name, so the page says **"named for"**. The
  correction was stated plainly rather than quietly reworded.
- **One sentence did more than the rest.** "…the same model of staying on the land that the Casa
  Familiar Rural continues today" was the only line linking her to the school rather than just
  listing facts — named explicitly as the line most likely to need cutting.
- **A convention reversed the original sketch.** The plan called for an `<h3>`; 0 of 6 sibling
  partner pages use one inside `.partner-story`, so plain `<p><strong>` was used instead. The
  deviation and its evidence were reported, not buried.

**Rule:** exactly one thing, named specifically. "Please review carefully" is not a flag.

### Why this is a rule

On these sites, "the change is up" has three meanings and only the third one is testable by the
person who has to accept it. The gap between merged and deployed is minutes long — long enough to
report a success that has not happened — and the checks in that window differ per site, so an agent
that assumes either "CI covers this" or "there is no CI" will be wrong on one of the four pairs.
Writing the sequence down, saying precisely what gated the change, and naming the one judgment call
up front is what lets a governor accept a page in one pass instead of chasing a rebuild or
discovering a framing decision after merge.

