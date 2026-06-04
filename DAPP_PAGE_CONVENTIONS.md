# DApp Page Conventions (TrueSight DAO / Agroverse)

When creating or updating pages in the **dapp** repository (`truesightdao.github.io/dapp` or local `dapp/`), follow these conventions so all pages look and behave consistently. **AI and developers should use this document** when adding or editing dapp pages.

**Reference:** The canonical UX patterns (loading states, error handling, comboboxes, etc.) are in **`dapp/UX_CONVENTIONS.md`**. This document covers **structure, meta tags, navigation, and layout**.

---

## 1. Document structure

- **DOCTYPE:** `<!DOCTYPE html>`
- **Html:** `<html lang="en">`
- **Head order:** charset → description → viewport → title → Open Graph → Twitter Card → Favicon → (optional: Maps/other scripts) → **menu.js** → `<style>`

---

## 2. Required meta tags

```html
<meta charset="UTF-8">
<meta name="description" content="One-line description of the page for search and preview.">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page Name - TrueSight DAO</title>
```

- **Title:** Use `Page Name - TrueSight DAO` (or `Page Name` only if the repo is Agroverse-only and you prefer that). Be consistent with existing pages (e.g. "Shipping Planner - TrueSight DAO", "Sales Reporter").

---

## 3. Open Graph (social / WhatsApp previews)

Include these so shared links show a proper title, description, and image:

```html
<!-- Open Graph tags for WhatsApp, Facebook, LinkedIn, and social media previews -->
<meta property="og:title" content="Page Name - TrueSight DAO">
<meta property="og:description" content="Same or similar one-line description as meta name='description'.">
<meta property="og:image" content="https://github.com/TrueSightDAO/.github/blob/main/assets/20240612_truesight_dao_logo_square.png?raw=true">
<meta property="og:url" content="https://truesightdao.github.io/dapp/your_page.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TrueSight DAO">
```

- **og:url:** Use the canonical URL for this page (e.g. `https://truesightdao.github.io/dapp/restock_recommender.html`).

---

## 4. Twitter Card

```html
<!-- Twitter Card tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Name - TrueSight DAO">
<meta name="twitter:description" content="Same one-line description.">
<meta name="twitter:image" content="https://github.com/TrueSightDAO/.github/blob/main/assets/20240612_truesight_dao_logo_square.png?raw=true">
```

---

## 5. Favicon

```html
<!-- Favicon -->
<link rel="icon" type="image/png" href="https://github.com/TrueSightDAO/.github/blob/main/assets/20240612_truesight_dao_logo_square.png?raw=true">
```

---

## 6. Navigation (menu)

- **Include menu.js** in every page: `<script src="./menu.js"></script>` (in `head`, before `</head>` or before `<style>`).
- **Include tdg_balance.js** in every page: `<script src="./tdg_balance.js"></script>` (after menu.js).
- **Reserve the nav placeholder** in `body` so the dropdown renders.
- **Reserve the TDG balance badge placeholder** after navDropdown so users see their TDG holdings once verified:

```html
<body>
    <div id="navDropdown" style="margin:1rem 0; text-align:center;"></div>
    <div id="tdgBalanceBadge"></div>
    <div class="container">
        ...
    </div>
</body>
```

- **Add new pages to the menu:** In **`dapp/menu.js`**, add an entry to `window.menuItems` with `title`, `url` (e.g. `'./restock_recommender.html'`), and `section` (e.g. `'Inventory & Sales'`).

---

## 7. Body and layout

**Body:** Same base layout on all pages:

```css
body {
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1rem;
    padding: 1rem;
    min-height: 100vh;
    box-sizing: border-box;
    background-color: #f5f5f5;
}
```

**Container:** Main content wrapper:

```css
.container {
    max-width: 600px;   /* or 800px for wider content */
    width: 100%;
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

- Use **max-width: 600px** for forms and narrow tools; **800px** for tables or multi-column layouts (e.g. Shipping Planner).

---

## 8. Typography

- **Page title (h1):** `font-size: 1.8rem; color: #333; margin: 0.5rem 0 1.5rem; text-align: center;`
- **Descriptions / intro:** Centered or left-aligned, `color: #555` or `#333`, `font-size: 1rem`, comfortable line-height.

---

## 9. Status and loading

- **Status message:** Use an element with `id="status"` for loading/result/error text. Add `aria-live="polite"` for accessibility.
- **Loading state:** Show immediate feedback (e.g. "Loading...") and follow **dapp/UX_CONVENTIONS.md** (dimmed fields, loading class, clear on success/error).
- **Error state:** Use a class such as `.error` with `color: #dc3545` or `#c62828` for error messages.

---

## 9b. Submission result rendering (signed-request flows)

When a page submits a **signed request** to Edgar (or any other DAO endpoint that takes the same `text` payload), show the operator BOTH:

1. **The full signed share text** — every byte that was actually sent, including the human-readable event header + `My Digital Signature:` + `Request Transaction ID:` + the `generated using` + `Verify submission here:` lines. Wrap it in a `<pre>` block so whitespace + line breaks render verbatim.
2. **The server's response** — JSON-serialised via `JSON.stringify(result, null, 2)`, also in a `<pre>` block.

Why both: the share text is what the operator may need to forward to Telegram / WhatsApp / a teammate (and is what they signed); the response is what Edgar actually did with it. A plain status message like `"Submitted. Edgar response: { ... }"` is insufficient — operators routinely need to copy the verbatim payload after submission and copy/paste the JSON to debug a downstream failure.

### Reference implementation

`dapp/report_contribution.html` is the canonical example — its share-text construction is mirrored across most signed-submit pages. Look there before inventing a new layout.

### Minimum shape

```html
<div id="submissionResult" style="display:none; margin-top: 1.5rem;">
  <h3>Transaction request</h3>
  <pre id="requestPre" style="white-space: pre-wrap; word-break: break-word; ...border, padding..."></pre>

  <h3>Edgar response</h3>
  <pre id="responsePre" style="white-space: pre-wrap; word-break: break-word; ...border, padding..."></pre>
</div>
```

```js
document.getElementById('requestPre').textContent  = signedShareText;          // not innerHTML — preserves &, <, > literally
document.getElementById('responsePre').textContent = JSON.stringify(result, null, 2);
document.getElementById('submissionResult').style.display = 'block';
```

Use `.textContent`, not `.innerHTML`, on the `<pre>`s — the signed payload can contain `<` and `&` literals from contributor names or descriptions that would otherwise break the HTML.

### Status line is additive, not a replacement

Keep the existing `#status` element for the short success/error sentence ("Submitted. The contributor row should appear after the next publisher run."). The `<pre>` blocks complement that line — they're for forensic detail.

### Print and copy

Both `<pre>` blocks should be selectable, copyable, and remain fully readable in print mode. See §16 for the `@media print` rules that ensure textareas + `<pre>` blocks expand to their full content height when printed.

### Applies to

Every new dapp page that submits a signed request. Existing pages that don't follow this pattern are a backlog item — fix them when you next touch them. Example PRs:

- `report_contribution.html` — canonical.
- `governor_contributor_admin.html` — migrated 2026-05-29 in dapp PR (link).

---

## 10. Logo and back link

- **Logo (default for full DApp tool pages):** Place the DAO logo **inside `.container`**, **above `<h1>`**, so the layout matches **`stores_nearby.html`**, **`shipping_planner.html`**, **`report_contribution.html`**, and **`store_interaction_history.html`**. Omit only for intentionally minimal pages (e.g. embed-only or redirect stubs).
  ```html
  <div class="container">
      <div style="text-align: center;">
          <img id="logo" height="200px" src="https://github.com/TrueSightDAO/.github/blob/main/assets/20240612_truesight_dao_logo_square.png?raw=true" alt="TrueSight DAO Logo"/>
      </div>
      <h1>Page Title - TrueSight DAO</h1>
      ...
  </div>
  ```
- **Canonical URL:** Set `og:url` to the URL users actually open in production (e.g. **`https://dapp.truesight.me/...`** when that is the live host), not only the GitHub Pages mirror, when they differ.
- **Back link:** If you use a back link, reuse the same pattern as other pages (`#backLink`, blue link with left arrow).

---

## 11. TDG Balance Badge

- **Include on all pages:** After the user's digital signature is verified, their TDG voting rights and estimated value are shown in a compact badge below the nav and above the main content.
- **Implementation:** Add `<div id="tdgBalanceBadge"></div>` after `navDropdown`, and include `<script src="./tdg_balance.js"></script>` in head.
- **Behavior:** `tdg_balance.js` checks for `publicKey` in localStorage, fetches holdings from the API, and renders a clickable badge linking to `withdraw_voting_rights.html`.
- **Rationale:** Users (especially during onboarding) see their TDG holdings immediately on any page, without visiting the cash-out page first.

---

## 12. UX patterns (see UX_CONVENTIONS.md)

- **Remote data loading:** Show loading state immediately; dim/disable fields; restore after load or error.
- **Errors:** Clear, actionable messages; red for errors; offer next steps.
- **Large lists:** Use searchable dropdown/combobox pattern where appropriate.
- **Digital signature:** If the page requires auth, follow the verification-on-load pattern described in UX_CONVENTIONS.md.

---

## 13. Checklist for new or updated pages

- [ ] `<!DOCTYPE html>`, `<html lang="en">`
- [ ] Meta: charset, description, viewport, title (`Page Name - TrueSight DAO`)
- [ ] Open Graph: og:title, og:description, og:image, og:url, og:type, og:site_name
- [ ] Twitter Card: twitter:card, twitter:title, twitter:description, twitter:image
- [ ] Favicon link
- [ ] `<script src="./menu.js"></script>` and `<script src="./tdg_balance.js"></script>`
- [ ] Body: flex, column, align center, margin/padding 1rem, min-height 100vh, background #f5f5f5
- [ ] `<div id="navDropdown">` and `<div id="tdgBalanceBadge"></div>` before `.container`
- [ ] `.container`: max-width, width 100%, white background, padding, border-radius 8px, box-shadow
- [ ] **DAO logo** inside `.container`, centered, above `h1` (see **§10**), unless the page is intentionally minimal
- [ ] h1: 1.8rem, #333, centered
- [ ] Status/loading: `id="status"`, `aria-live="polite"`, error class for errors
- [ ] New page added to `menu.js` → `menuItems` with correct section
- [ ] UX patterns from `dapp/UX_CONVENTIONS.md` followed where applicable (loading, errors, etc.)
- [ ] If the page calls a Google Apps Script web app: deploy **Who has access** so the DApp can call it (see **§14**); use `fetch` + JSON `ContentService` like existing pages — not JSONP

---

## 14. Google Apps Script web apps (fetch, CORS, `file://`)

DApp pages call deployed web apps with **`fetch()`** and query parameters — same pattern as **`stores_nearby.html`** and **`shipping_planner.html`**. **JSONP is not required** for these endpoints when deployment settings are correct.

**If the browser reports CORS** (`No 'Access-Control-Allow-Origin'`, often with **`origin 'null'`** when you open the HTML via **`file://`**):

1. In Apps Script: **Deploy → Manage deployments** — the web app **Who has access** must include the caller (typically **Anyone** for public DApp + local file testing). If access is **Only myself** or too narrow, Google may return an HTML sign-in or error page that **does not** include CORS headers; the failure surfaces as CORS, not as a clear 403 in the console.
2. **Execute as:** **Me** is the usual setting.
3. Use **New deployment** / new version after code changes; paste the current **`.../exec`** URL into the DApp (`API_BASE_URL`, etc.).
4. Response body: match existing APIs — `ContentService.createTextOutput(JSON.stringify(payload)).setMimeType(ContentService.MimeType.JSON)` (see **`tokenomics/google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`**, **`holistic_hit_list_store_history/store_interaction_history_api.gs`**).

Do not assume a CORS error means the `.gs` response format is wrong; **verify deployment access first.**

### Static host (GitHub Pages / `dapp.truesight.me`) and `doGet` vs `doPost`

- The DApp is **static HTML** on **GitHub Pages** (or a custom domain such as **`https://dapp.truesight.me/`**). It is **not** required to serve pages from **HtmlService** inside Apps Script to talk to a backend.
- A deployed **Web app** URL (`…/macros/s/…/exec`) can implement **`doGet`** and/or **`doPost`**. Either handler can be called from the static site with **`fetch()`** (GET with query string, or POST with a JSON body / `application/x-www-form-urlencoded`, depending on what the script expects).
- **`doPost` is not “only available when the HTML is hosted by Google Apps Script.”** HtmlService is a separate pattern (serving UI from GAS). For data APIs, many projects use **only** `doGet` for simplicity; choosing POST is a **design** decision (e.g. avoids very long URLs, avoids accidental logging of query strings, clearer semantics for writes), not a platform lock-in.
- **Writes (e.g. append a row to “Recent Field Agent Location”)** still need **rate limiting / dedupe** on the server and/or **debouncing** in the browser so map panning or repeated loads do not over-fill the sheet. Prefer **idempotent** or **“log at most once per window per key”** rules.
- If POST ever fails with CORS in a given browser, treat it like GET: confirm **Web app deployment access**, response MIME type, and that the handler returns **`ContentService`** JSON (not an accidental HTML error page).

### Field agent location (`stores_nearby` → sheet → Places → Hit List)

- **Goal:** When a **signed** contributor uses **`stores_nearby.html`**, the first eligible **store search** `GET` to the **Stores Nearby** GAS web app can include **`save_location=true`** and **`digital_signature`**. GAS appends one row to spreadsheet **`1eiqZr3LW…`** tab **`Recent Field Agent Location`** (`gid=881847228`) with **`Status` = `pending`**.
- **Throttle:** **`localStorage`** key `tsd_field_agent_loc_last_ms_v1:<publicKey prefix>` — at most one ping per **24 hours** per key unless the page URL includes **`save_location=true`** (test override). The client only attaches **`save_location` once per page load** after a successful response that includes `field_agent_location` (or after the fetch completes so retries work).
- **GAS:** `tokenomics/clasp_mirrors/1NpHrKJW8Q4suu6-f5gXQcbjHqUZtGOG-KcIf81M1GG8lDShm5-fLphD2/Code.js` — `doGet` search branch; JSON echo **`field_agent_location`**: `{ saved, location_id?, reason? }`. **Redeploy** the web app after `clasp push`. Row 1 on the tab must match the six canonical headers (GAS overwrites row 1 when safe: **no data in row 2+**).
- **Downstream:** **`market_research/scripts/field_agent_location_places_pull.py`** — reads **`pending`**, applies **20 mi / 24 h** dedupe against prior **`pulled`** rows before calling **Places Nearby** (tunable via **`--dedupe-miles`** / **`--dedupe-hours`**, or **`--no-recent-dedupe`**), appends deduped **Hit List** rows (**Research**), sets **`pulled`** / **`ignored because already pulled`**, and appends an automation summary to **DApp Remarks**. **CI:** `market_research/.github/workflows/field_agent_location_places_pull.yml`.
- **Schema / credentials:** **`tokenomics/SCHEMA.md`** (§4 Holistic wellness Hit List), **`market_research/HIT_LIST_CREDENTIALS.md`** (field agent subsection).

---

## 15. Where conventions live

| Topic              | Location                          |
|--------------------|-----------------------------------|
| Page structure     | This file (agentic_ai_context)    |
| Meta, nav, layout | This file                        |
| Loading, errors, UX| **dapp/UX_CONVENTIONS.md**       |
| Menu entries       | **dapp/menu.js**                 |
| GAS + fetch + CORS + static host / POST + field agent ping | This file §14 |

When in doubt, **copy structure and meta tags from an existing page** (e.g. `shipping_planner.html`, `report_sales.html`) and then adjust content and styles.

---

## 16. Print stylesheet (textareas + `<pre>` + signed payloads)

Every form-bearing DApp page must keep its **input boxes and result blocks legible when printed** — the operator routinely prints a confirmation page as a receipt or to share with a partner who isn't on Telegram. Browsers truncate textareas by default in print mode (they only render what fits the on-screen scroll box), which silently cuts off long descriptions / event payloads.

Add this `@media print` block to **every page that has a `<textarea>` or a result `<pre>`** (typically in `<head>` or in `styles/main.css`):

```css
@media print {
  /* All textareas expand to show every line of their content.
     Default browser behaviour clips to the visible scroll box. */
  textarea {
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
    white-space: pre-wrap;
    page-break-inside: auto;
    border: 1px solid #999;       /* subtle outline so it still reads as a field */
  }

  /* Signed-request result blocks (§9b) must also expand and wrap. */
  pre {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    overflow: visible !important;
    page-break-inside: auto;
  }
}
```

### Why this lives globally

Per-page overrides are fragile (every new page invents its own print rule). Add the block once to `styles/main.css` (or whichever shared stylesheet the DApp uses for global typography) so every page inherits it. Per-page additions only when a page has additional non-default elements that also need print treatment.

### Backlog

Any page that has a `<textarea>` and renders OK on screen but cuts off when printed has this exact bug. Fix opportunistically when touched; sweep if there's a clear set.

---

## 17. Anti-patterns — common LLM-generated mistakes

When an LLM generates a DApp page from scratch, these mistakes recur. Review new LLM-generated pages against this list specifically.

### Body / layout mistakes

| Anti-pattern | Convention |
|---|---|
| Custom wrapper class (`.wrap`, `.page`, etc.) instead of `.container` | Use `.container` with `max-width: 600px` (form) or `800px` (table/lists), white bg, border-radius, box-shadow per §7 |
| Custom body background (`#faf8f4`, `#fff`, etc.) | Use `#f5f5f5` with flex column centering per §7 |
| Minified/one-line CSS | Use readable multi-line CSS matching existing pages |
| Omitting the `#tdgBalanceBadge` div | Include after `navDropdown` per §6/§11 |
| Omitting the DAO logo from `.container` | Include centered logo above `h1` per §10 |
| `<title>` using middot (`·`) instead of dash | Use `Page Name - TrueSight DAO` per §2 |

### Meta tag mistakes

| Anti-pattern | Convention |
|---|---|
| Generic `og:url` (`.../dapp/`) instead of page-specific | Use the specific page URL per §3 |
| Missing `og:site_name` | Always include `content="TrueSight DAO"` per §3 |
| Missing Twitter Card tags entirely | Include all four (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`) per §4 |

### Form / submission mistakes

| Anti-pattern | Convention |
|---|---|
| Status messages in JS only, no `<pre>` blocks | §9b — always render both the signed share text AND server response in `<pre>` blocks |
| No `@media print` styles | §16 — every page with `<textarea>` or `<pre>` must include the print block |
| No `aria-live="polite"` on status | §9 — add to the status element |

### Quick audit command

After creating or reviewing an LLM-generated page, diff against `report_contribution.html` (the canonical page) for structural blocks:

```bash
diff <(grep -oE '<meta|og:|twitter:|#tdg|#navDropdown|\.container|\.body|@media' report_contribution.html | sort) \
     <(grep -oE '<meta|og:|twitter:|#tdg|#navDropdown|\.container|\.body|@media' new_page.html | sort)
```

Missing blocks will show as removed lines and are immediate flags.

### Example: program_registrations_review.html (2026-06-04)

Sophia (truesight_autopilot) generated the initial version which missed: Twitter Card, `og:site_name`, specific `og:url`, `#tdgBalanceBadge`, DAO logo, `@media print`, `aria-live`, §9b `<pre>` blocks, and used a custom `.wrap` class with non-standard body styling. The page worked functionally but looked like a foreign import. Fixed in dapp_beta#42 — the diff serves as a reference for what LLMs miss.
