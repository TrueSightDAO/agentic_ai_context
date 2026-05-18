# CREDENTIALING_PROGRAM_PAGES.md

**Per-program credentialing surfaces on `truesight.me` — co-branded with partner organizations, QR-discoverable from printed certificates.**

> **Status (2026-05-16):** Phase 0 documentation. No code shipped yet. URL shape is **decided** because it gets etched into physical certificate QR codes — read § "URL shape (permanent)" before generating any certs.

---

## 1. Purpose

The DAO already has a per-person credentialing surface at `truesight.me/credentials/#<slug>` backed by the `TrueSightDAO/lineage-credentials` repo. It answers *"what has this individual done?"* — but not the inverse question partners need: *"who has gone through our program?"*

Partner programs (Tribo Bahia Mirim capoeira lineage, ERA Professionals' Butterfly Effect, and future) want:

1. **A program-scoped member listing** — a page they can point at to showcase their cohort.
2. **A program-scoped per-person profile path** — for QR codes printed on physical certificates handed to participants. Scan → land on a co-branded version of that person's CV.
3. **Co-branding** — partner identity sits alongside TrueSight DAO branding, signalling shared issuance without requiring the partner to host their own site.

This document specifies how those surfaces are built without forking the underlying credentials store.

## 2. Why repurpose credentialing, not fundraising

The existing `truesight.me/fundraisers.html` frames programs from the funder's perspective. Tribo Mirim does have a donation component, but the *primary activity* — kids learning capoeira, building lineage records — is experiential learning. ERA's Butterfly Effect is purely experiential, no fundraising angle at all. Reframing as **experiential learning credentialing** unlocks both use cases under one platform and creates a durable language partners can adopt.

`fundraisers.html` stays for programs that *are* primarily donation drives (e.g., AGL shipment financing). The new `programs.html` is its sibling — different lens, different audience.

## 3. URL shape (permanent)

The URL embedded in a printed certificate QR is **immutable** — once a cert is handed to a participant, the path it points at must work indefinitely. We commit to the following shape:

```
truesight.me/programs/<program-slug>/credentials/#<member-slug>
```

**Examples:**

- `truesight.me/programs/butterfly-effect/credentials/#maria-santos-2026`
- `truesight.me/programs/tribomirim/credentials/#gary-teh`

**Why this shape (not the alternatives we considered):**

| Shape | Verdict |
|---|---|
| `truesight.me/programs/<p>/credentials/#<slug>` ✅ | Co-branded path, reinforces partnership in the URL itself. Scales cleanly per partner. **Chosen.** |
| `truesight.me/credentials/#<slug>` (program inferred from record) | Shortest URL but no co-brand hint; ties co-branding entirely to render-time logic. |
| `truesight.me/be/<slug>` (per-program short prefix) | Compact but forces a vanity-route table that grows per partner. |

**Rules for `<program-slug>`:**

- Lowercase, hyphen-separated, ASCII only, max 32 characters.
- Stable for the life of the program. Renaming a program slug breaks every printed certificate.
- Must match the corresponding directory under `programs/` in `truesight_me`.

**Rules for `<member-slug>`:**

- Owned by the `TrueSightDAO/lineage-credentials` repo (`_cache/index.json` members list).
- For partner programs issuing certs to participants who are not already DAO contributors: the member-slug is minted at certificate-generation time, recorded in `lineage-credentials`, and never reused.

## 4. File layout (`truesight_me_beta` / `_prod`)

```
truesight_me/
├── programs.html                              ← parent index page (lists all programs)
└── programs/
    ├── butterfly-effect/
    │   ├── index.html                         ← co-branded program landing
    │   ├── manifest.json                      ← program metadata (see §6)
    │   ├── members.html                       ← cohort listing
    │   └── credentials/
    │       └── index.html                     ← per-member co-branded CV (QR target)
    ├── tribomirim/
    │   ├── index.html
    │   ├── manifest.json
    │   ├── members.html
    │   └── credentials/
    │       └── index.html
    └── ... future partner programs
```

`programs/<slug>/credentials/index.html` is a thin wrapper around the canonical CV renderer at `truesight.me/credentials/index.html`. It re-fetches the same `_cache/cv/<member-slug>.json` from `lineage-credentials` and adds a co-brand header sourced from `../manifest.json`.

## 5. Data sources

| Surface | Source |
|---|---|
| Member listing (per program) | `TrueSightDAO/lineage-credentials/_cache/index.json` filtered by `primary_program == "<program-slug>"` |
| Per-member CV | `TrueSightDAO/lineage-credentials/_cache/cv/<member-slug>.json` |
| Program metadata + co-brand | `truesight_me/programs/<slug>/manifest.json` (committed to the truesight_me repo) |
| Program practice events | `cv.programs[<program-slug>].recent_events[]` inside each member's CV JSON (already populated by the existing `capoeira.agroverse.shop/practice.html` → `lineage-credentials` cron) |

Fetch path uses the **jsDelivr-primary, raw.githubusercontent-fallback** pattern already shipped in `js/ecosystem-change-log-feed.js` (see `truesight_me_beta#82`, `_prod#1`, 2026-05-14). Reuse `TrueSightEcosystemFeed.repoFetch` or follow the same pattern for the credentials fetcher to keep GFW users included.

## 6. Manifest schema (`programs/<slug>/manifest.json`)

```json
{
  "schema_version": 1,
  "program_slug": "butterfly-effect",
  "display_name": "Butterfly Effect",
  "partner_organization": "ERA Professionals",
  "partner_url": "https://era-professionals.com/butterfly-effect/",
  "partner_contact_label": "Bilal (program lead)",
  "tagline": "Experiential learning for youth, credentialed on-chain.",
  "description_md": "One paragraph or short markdown describing the program's mission and how participants earn credentials.",
  "co_brand": {
    "partner_logo_url": "https://raw.githubusercontent.com/TrueSightDAO/.github/main/assets/butterfly-effect-logo.png",
    "primary_color": "#A66B2E",
    "secondary_color": "#F2E4CE"
  },
  "source_pages": [
    "https://era-professionals.com/butterfly-effect/"
  ],
  "membership_filter": {
    "primary_program": "butterfly-effect"
  },
  "credential_visibility_default": "public",
  "issuer_lineage_root": "Butterfly Effect",
  "status": "onboarding",
  "last_reviewed": "2026-05-16"
}
```

**Field notes:**

- `program_slug` MUST equal the directory name under `programs/`.
- `membership_filter.primary_program` is the value the `members.html` page matches against `lineage-credentials/_cache/index.json[].primary_program`.
- `co_brand.partner_logo_url` is loaded into the landing + members + credentials wrapper. Hosting in `TrueSightDAO/.github/assets/` keeps the URL stable and CDN-friendly.
- `credential_visibility_default` accepts `"public"` (default for adult cohorts and certificate recipients) or `"private"` (for programs serving minors without parental release). The members.html page filters on a future `public_listable` flag on the member record; until that flag exists in `lineage-credentials`, treat this as advisory.
- `status` controls how the parent `programs.html` index renders the program card. Accepts:
  - `"active"` (default if absent) — fully operational; cohort exists or will populate from `lineage-credentials` as members earn credentials.
  - `"onboarding"` — partner is being onboarded; manifest + pages exist so the URL surface is reachable for partner review, but no participants have been credentialed yet. `programs.html` shows an *Onboarding* pill on the card so visitors know the cohort hasn't started.
  - `"archived"` — program is no longer accepting new participants but historical cohort pages stay live (so previously printed QR codes keep resolving). `programs.html` may demote or hide archived cards depending on operator preference.
- `last_reviewed` bumps every time partner copy or branding changes — keeps the manifest from going stale silently.

## 7. Co-branding pattern

Three places where the partner brand appears:

1. **`programs/<slug>/index.html`** — full-bleed landing with partner logo, tagline, description, "View cohort" CTA into members.html, "Visit partner site" link out to `partner_url`. TrueSight DAO branding kept in the standard nav header (it's still hosted on truesight.me).
2. **`programs/<slug>/members.html`** — partner logo + program name as the H1; member tiles use the standard credentials surface chrome below.
3. **`programs/<slug>/credentials/index.html`** — partner badge above the CV header: *"Credentialed via Butterfly Effect (ERA Professionals)"*. The CV body itself is the canonical render.

Single-line partner-attribution badge stays present on every program-scoped surface so a QR scanner immediately sees the co-issuance signal.

## 8. QR code generation (printed certificates)

The URL pattern from §3 is the QR payload. Generation tooling:

- **Reuse** `tokenomics/google_app_scripts/agroverse_qr_codes/batch_compiler.py` and the `to_print/` pipeline — same physical-print flow already used for Agroverse cacao bag QR codes. See `agentic_ai_context/AGROVERSE_QR_CODE_BATCH_GENERATION.md` for the print template + naming conventions.
- **Variant** needed: clone `batch_compiler.py` into a `cert_compiler.py` variant that takes `(program_slug, member_slug, member_display_name)` tuples and emits the QR target URL `truesight.me/programs/<program_slug>/credentials/#<member_slug>`. Defer until the first cohort is ready to print — not blocking the web pages.

## 9. Privacy and consent

The default credentialing UX treats member CV pages as public — DAO contributors self-opt-in by registering an identity. Partner programs serving minors or non-DAO-contributors need a different model:

- **Certificate recipients are opt-in by the act of being handed a printed cert.** Issuing the cert IS the consent moment (the partner organization captures the underlying release form before printing).
- **Until the cert is issued, the participant should not appear in the program members listing.** Practically: `lineage-credentials` should set `public_listable: false` on freshly-minted member records and only flip to `true` when the cert is generated.
- **`programs/<slug>/manifest.json::credential_visibility_default`** is a programme-wide hint; per-member overrides on the credential record always win.

If a participant or guardian later requests removal, the operator flips `public_listable: false` on the credential record; both the members listing and direct hits to `programs/<slug>/credentials/#<member-slug>` should degrade to a "this credential is no longer publicly viewable" notice rather than a 404 (the QR is on a physical cert that can't be recalled).

## 10. White-label upgrade path

Today we ship **co-branded** — partner branding sits alongside TrueSight DAO branding on truesight.me-hosted pages. If a partner later wants **white-label** (their own domain, no TrueSight chrome):

1. Partner stands up their own static host (GitHub Pages, Vercel, Cloudflare Pages).
2. They mirror or proxy the credentials fetch path: `_cache/cv/<slug>.json` from `lineage-credentials` (public repo, no auth needed).
3. They render their own version of `credentials/index.html` with their full branding.
4. The QR codes already in the field still resolve at `truesight.me/programs/<slug>/credentials/#<slug>` — that path continues to serve the co-branded page indefinitely. Newly issued certs after the white-label cutover encode the partner's domain instead.

The co-branded path is **never retired** so existing physical certs keep working.

## 11. Phased rollout

| Phase | What ships | Repos |
|---|---|---|
| **0** (this doc) | Implementation specification only | `agentic_ai_context` |
| **1** | `programs.html`, `programs/butterfly-effect/{index,manifest,members,credentials}.html`, `programs/tribomirim/{...}` | `truesight_me_beta` → mirror to `truesight_me_prod` |
| **2** | Butterfly Effect cohort: real member slugs minted in `lineage-credentials`; `members.html` populates | `lineage-credentials` + `truesight_me_prod` |
| **3** | `cert_compiler.py` variant for printed-cert QR generation | `tokenomics` |
| **4** | First Butterfly Effect cohort certs printed and handed out | (operator workflow, no repo) |
| **5** | (Optional) `public_listable` flag in `lineage-credentials` member records to gate minors / non-consenting participants | `lineage-credentials` |
| **6** | (Optional) White-label upgrade — partner runs their own renderer pointing at the same `_cache/cv/<slug>.json` | partner repo |

Phase 4 must not start before Phases 1 + 2 are live and verified — printed QR codes pointing at a 404 are unrecoverable.

## 12. Open questions

1. **Member slug minting for non-DAO participants.** Existing DAO contributors get slugs from their email + name on registration. Butterfly Effect kids won't go through DAO registration. Who/what mints `<member-slug>` and writes the record into `lineage-credentials`? Likely a partner-operator-run script that takes a cohort CSV and produces slug + initial CV JSON. Spec out separately when Bilal's first cohort data is ready.
2. **Photo on the cert / profile.** Adult DAO contributor CVs are typically text-only. A kid's certificate profile probably benefits from a photo — but again, consent. Punt to Phase 2 with explicit guidance from Bilal on what ERA's release form already covers.
3. **Multiple programs per member.** `primary_program` is exclusive in today's data model. A learner who participates in both Butterfly Effect AND Tribo Mirim would only appear in one listing. If this becomes a real case, expand `lineage-credentials` to also expose a `programs[]` array per member (we already have it inside the CV JSON; just needs to surface in `_cache/index.json`).

## 13. References

- `truesight_me/credentials/index.html` — canonical CV renderer.
- `truesight_me/members.html` — canonical member directory.
- `https://raw.githubusercontent.com/TrueSightDAO/lineage-credentials/main/_cache/index.json` — source-of-truth members list.
- `https://raw.githubusercontent.com/TrueSightDAO/lineage-credentials/main/_cache/cv/<slug>.json` — per-member CV JSON.
- `agentic_ai_context/AGROVERSE_QR_CODE_BATCH_GENERATION.md` — QR generation tooling reused for printed certs.
- `tokenomics/google_app_scripts/agroverse_qr_codes/batch_compiler.py` — QR PNG batch compiler to clone for `cert_compiler.py`.
- `lineage-engine/scripts/qr_code.py` — `generate_qr_with_logo(url, out_path, logo_path)` — already powers the canonical TrueSight-logo QR; reused for every per-program QR by swapping `logo_path`.
- `lineage-engine/scripts/build_cv_cache.py` — engine that emits `_cache/cv/<slug>.{json,md,pdf,qr.png}`; extension point for the per-program artifacts in §15.
- `truesight_me/js/ecosystem-change-log-feed.js` (PR `truesight_me_beta#82`) — jsDelivr-primary + raw.github-fallback fetch pattern to copy for GFW resilience.

## 14. Last reviewed

2026-05-16 — Phase 0 doc + Phase 1 implementation + Phase 1 nav/status follow-ups all shipped.
**2026-05-17 — §15 Phase 3a added (per-credential QR + PDF, per surface).**
**2026-05-17 — §16 Onboarding a new program — file-by-file playbook added.**

---

## 15. Phase 3a — per-credential QR + PDF, per surface

> **Scope:** every credential page surface (canonical and each program-scoped one) carries its own QR with the appropriate logo in the centre, encoding the production URL of *that surface*. The matching PDF embeds the same QR so a printed copy resolves to the same place. PDFs regenerate on every new event that affects the CV.

### 15.1 Surfaces and what each QR encodes

The QR payload is always a fully-qualified production URL — never a relative path, never a local-dev host.

| Page | QR centre logo | QR payload |
|---|---|---|
| `truesight.me/credentials/#<slug>` | TrueSight DAO mark (`lineage-engine/scripts/truesight_icon.png`, existing) | `https://truesight.me/credentials/#<slug>` |
| `truesight.me/programs/<program-slug>/credentials/#<slug>` | Program partner logo (`lineage-engine/scripts/program_assets/<program-slug>/logo.png`, new — vendored) | `https://truesight.me/programs/<program-slug>/credentials/#<slug>` |

The canonical surface continues to use the existing TrueSight-logo QR (no change). The per-program surface gets a sibling QR with the partner logo swapped in.

### 15.2 Artifact naming (in `lineage-credentials/_cache/cv/`)

```
_cache/cv/
├── <slug>.json                       canonical CV JSON (existing)
├── <slug>.md                         canonical markdown (existing)
├── <slug>.pdf                        canonical PDF (existing) — embeds <slug>.qr.png
├── <slug>.qr.png                     canonical QR with TrueSight logo (existing)
├── <slug>__<program-slug>.qr.png     per-program QR with partner logo (new)
└── <slug>__<program-slug>.pdf        per-program PDF embeds the matching QR (new)
```

Rules:

- `<slug>` is the canonical member slug from `_cache/index.json`. Unchanged.
- `<program-slug>` matches the directory under `truesight_me/programs/`. Same value as `cv.programs[<program-slug>]`.
- Double underscore (`__`) is the namespace separator. Reserved — never appears inside a `<slug>` or a `<program-slug>`. Allows simple suffix-strip parsing.
- New files only emitted when the CV has a corresponding `cv.programs[<program-slug>]` record AND a logo asset for that program exists in `lineage-engine/scripts/program_assets/<program-slug>/`.
- If a CV is in multiple programs, it gets multiple `__<program>` artifacts — one pair per program.
- Files no longer "needed" (e.g., a program was deleted from the CV) are NOT cleaned up by the build; physical QR codes in the field already point at them. Stale program artifacts are tolerated forever, just like the URL paths themselves are never retired (see §10).

### 15.3 Program logo vendoring (`lineage-engine/scripts/program_assets/`)

```
lineage-engine/scripts/
├── truesight_icon.png            existing — canonical centre logo
└── program_assets/
    ├── tribomirim/
    │   └── logo.png              square PNG, transparent background, ≥256px
    ├── butterfly-effect/
    │   └── logo.png
    └── <future-program-slug>/
        └── logo.png
```

Logos are vendored into `lineage-engine` (not fetched from `truesight_me/programs/<slug>/manifest.json::co_brand.partner_logo_url`) because:

- Build determinism: the QR-render step shouldn't require network at build time.
- Audit trail: a logo change becomes a git diff visible in PR review.
- License clarity: the partner has to explicitly commit a logo for us to use — implicit consent moment.

The truesight_me-side `manifest.json::co_brand.partner_logo_url` continues to drive the *web* co-brand strip (where network fetch is fine). The two references — the truesight_me manifest URL and the lineage-engine vendored PNG — are independent and may diverge. The vendored PNG is canonical for QR generation; the manifest URL is canonical for on-page chrome.

**Adding a new program:**

1. Partner sends the logo (or the operator extracts it from the partner site).
2. Commit it to `lineage-engine/scripts/program_assets/<program-slug>/logo.png`. Same `<program-slug>` as the truesight_me directory.
3. Next `build_cv_cache.py` run picks it up automatically and starts emitting per-program QR+PDF for every CV that has a record in that program.

If a logo isn't yet vendored, the build logs a warning and skips that program's artifact — no error, no broken CV.

### 15.4 build_cv_cache.py extension

Augments the existing per-CV write loop in `lineage-engine/scripts/build_cv_cache.py`:

```python
# existing — unchanged
qr_target = (cv.get('qr_code') or {}).get('target_url') or CREDENTIAL_PROFILE_URL.format(slug=slug)
qr_path = cv_dir / f'{slug}.qr.png'
render_qr(slug, qr_target, qr_path)
# ... write json/md/pdf as today ...

# new — per-program QR + PDF
for program_slug, program_record in (cv.get('programs') or {}).items():
    logo_path = SCRIPT_DIR / 'program_assets' / program_slug / 'logo.png'
    if not logo_path.is_file():
        continue  # warn-and-skip
    program_url = PROGRAM_CREDENTIAL_URL.format(program=program_slug, slug=slug)
    program_qr_path = cv_dir / f'{slug}__{program_slug}.qr.png'
    render_qr_with_custom_logo(program_url, program_qr_path, logo_path)
    if write_pdfs:
        program_pdf_html = render_html(cv, md, program_qr_path, program_scope=program_slug)
        render_pdf(program_pdf_html, cv_dir / f'{slug}__{program_slug}.pdf')
```

`PROGRAM_CREDENTIAL_URL = 'https://truesight.me/programs/{program}/credentials/#{slug}'`.

`render_html` gets an optional `program_scope` parameter so the PDF can render a co-brand header instead of (or alongside) the TrueSight chrome — same visual model as the on-page credentials wrapper.

### 15.5 Page placement (`truesight_me`)

#### Canonical `credentials/index.html` (already shipped, no change in this phase)

The existing "⬇ Download PDF" button already references `_cache/cv/<slug>.pdf`. The QR image is already displayed by the canonical renderer. No change.

#### Program-scoped `programs/<p>/credentials/index.html` (this phase)

Extend `js/program-shell.js` so the `renderCredential(manifest)` function:

1. Adds a QR section to the rendered HTML. Image src: `https://cdn.jsdelivr.net/gh/TrueSightDAO/lineage-credentials@main/_cache/cv/<slug>__<program-slug>.qr.png` (with raw.githubusercontent fallback per §5).
2. Adds a "⬇ Download credential PDF" button below the QR, pointing at `_cache/cv/<slug>__<program-slug>.pdf` (same dual-CDN pattern).
3. If the per-program QR PNG 404s (e.g., logo not yet vendored, build hasn't run since the program was added), gracefully falls back to the canonical `<slug>.qr.png` so the page still shows *something* scannable. Note: the fallback QR encodes the canonical URL, not the program-scoped one — that's intentional. A scan still resolves to a working credential page; the centre logo just doesn't carry the partner mark.

### 15.6 Regeneration trigger

`lineage-credentials` already runs a GitHub Action on push that invokes `build_cv_cache.py` and commits the regenerated `_cache/` artifacts back to `main`. Phase 3a piggybacks on that same trigger — adding `__<program>` artifacts to the build's emitted file set means they regenerate on the same cadence as the canonical artifacts.

**Implicit debounce:** events arriving in the same commit produce one rebuild. Events arriving across N commits within a CI run produce one rebuild per commit; if that becomes thrashy in practice (e.g., 5+ rebuilds per hour during active practice), add a `concurrency: group=build-cv-cache, cancel-in-progress=true` line to the workflow so only the latest queued run actually executes. Not needed at current event volume; revisit if it gets loud.

**Explicit rebuild trigger:** operator can `gh workflow run build-cv-cache.yml` to force a rebuild without a new event commit. Used after vendoring a new program logo, after adding a new program directory, etc.

### 15.7 Display on the page (HTML/CSS snippet)

```html
<section class="credential-qr">
  <h3>Scan this credential</h3>
  <img class="credential-qr-img" src="<jsdelivr-url>/_cache/cv/<slug>__<program>.qr.png" alt="QR code linking to this credential" />
  <p class="credential-qr-hint">Or follow: <code><https://truesight.me/programs/<program>/credentials/#<slug>></code></p>
  <a class="btn-link" href="<jsdelivr-url>/_cache/cv/<slug>__<program>.pdf" target="_blank" rel="noopener">⬇ Download credential PDF</a>
</section>
```

Style: QR sits at ~180×180 on desktop, ~140×140 on mobile, padded white box, centred under the program-section content and above the credential footer. Distinct from the canonical credentials page's QR placement so users immediately see "this is the program-stamped version."

### 15.8 Phased rollout for Phase 3a itself

| Sub-phase | What ships | Repos |
|---|---|---|
| **3a.0** (this doc) | This §15 addendum | `agentic_ai_context` |
| **3a.1** | Vendor `tribomirim/logo.png` + `butterfly-effect/logo.png` into `lineage-engine/scripts/program_assets/` | `lineage-engine` |
| **3a.2** | `build_cv_cache.py` extended to emit per-program QR + PDF when logos are present | `lineage-engine` |
| **3a.3** | Force a `lineage-credentials` rebuild — first cohort of per-program QR/PDF artifacts committed | `lineage-credentials` (auto from GH Action) |
| **3a.4** | `js/program-shell.js` displays the QR + PDF download on `programs/<p>/credentials/#<slug>` | `truesight_me_beta` → `_prod` |
| **3a.5** | Manual verification — scan the QR on a real phone, confirm it resolves to the production URL with the program co-brand chrome visible | (operator) |

3a.1 + 3a.2 can ship in the same `lineage-engine` PR. 3a.3 is automatic — no PR. 3a.4 is its own truesight_me PR pair (beta + prod mirror).

### 15.9 Open questions for Phase 3a

1. **Logo aspect ratios.** The existing `qr_code.py::generate_qr_with_logo` thumbnails the logo to fit within `logo_ratio * qr_size` (default 20%). Square logos with transparent background work best. The vendoring step needs an operator-side normalize pass (crop to square, transparent BG, ≥256px). Document the operator checklist in `lineage-engine/scripts/program_assets/README.md` when 3a.1 ships.
2. **Multiple programs per CV.** A CV with `cv.programs = {tribomirim: ..., butterfly-effect: ...}` will get two `__<program>` pairs. The canonical credentials page already shows all programs; the program-scoped pages each show one. No conflict — different surfaces for different audiences.
3. **What if the logo URL in `truesight_me/programs/<p>/manifest.json::co_brand.partner_logo_url` and the vendored logo in `lineage-engine/program_assets/<p>/logo.png` diverge?** They're allowed to. The web UI uses the manifest URL (fetchable, can be a CDN-hosted hi-DPI asset); the QR uses the vendored PNG (must be local + reasonable resolution + correct aspect for QR-centre overlay). If a partner sends a re-branded logo, update both.

---

## 16. Onboarding a new program — file-by-file playbook

You have the spec above. This section is the operational sequence — what an AI or operator does start to finish to add **one** new program (e.g. a third partner after Tribo Bahia Mirim and Butterfly Effect). Steps assume `~/Applications/truesight_me/` is a clone of `truesight_me_beta` and that beta→prod promotion follows `NOTES_truesight_me.md` § "Beta vs. production split".

### 16.1 Pick the two slugs

Two slug fields exist and **they don't have to match** — read this before touching anything.

| Field | Used by | Example (Tribo) |
|---|---|---|
| `manifest.program_slug` + directory name `programs/<slug>/` | The website URL: `truesight.me/programs/<program_slug>/...` | `tribomirim` |
| `manifest.membership_filter.primary_program` | The `lineage-credentials` `_cache/index.json[].primary_program` value the cohort listing matches on | `capoeira-tribo-mirim` |

`program_slug` is the URL slug you commit to forever (it's in printed cert QR codes — see §3). `primary_program` is whatever the lineage-credentials side already calls the program in `_cache/index.json` — usually set by the practice-platform integration upstream. If the program has no live practice integration yet, set `primary_program` to a value the future integration will use; the cohort just stays empty until then.

### 16.2 Branch + scaffold

```bash
cd ~/Applications/truesight_me
git checkout main && git pull --ff-only
git checkout -b feat/program-<program_slug>

# Copy an existing program as the template — Tribo is a good baseline
cp -R programs/tribomirim programs/<program_slug>
```

Four files now exist under `programs/<program_slug>/`:

- `manifest.json` — program metadata
- `index.html` — co-branded landing page
- `members.html` — cohort listing
- `credentials/index.html` — per-member CV wrapper (QR target for printed certs)

All three HTML files share `js/program-shell.js` for runtime rendering — you do NOT touch JS. Per-program differences are purely metadata in `manifest.json` + a handful of static strings in the HTML.

### 16.3 Fill `manifest.json`

Open `programs/<program_slug>/manifest.json` and edit (see §6 for full schema):

- `program_slug` — must equal the directory name
- `display_name` — what shows on the landing page H1 and program card
- `partner_organization`, `partner_url`, `partner_contact_label`
- `tagline` — one-sentence hook for the card on `programs.html`
- `description_md` — one short paragraph for the landing page body
- `co_brand.partner_logo_url` — prefer a stable URL (TrueSightDAO/.github/assets/ or the partner's CDN)
- `co_brand.primary_color` / `secondary_color` — hex; used for badge accents
- `source_pages[0]` — partner's own program page (also lifted onto each CV)
- `membership_filter.primary_program` — see §16.1
- `issuer_lineage_root` — for capoeira this is the master / mestre name; for institutional programs it's the partner org name
- `status` — `"onboarding"` until the first cohort exists, then `"active"`
- `last_reviewed` — today's date (YYYY-MM-DD)

### 16.4 Hand-edit the three HTMLs

Each HTML file has a small number of program-name strings. Find-and-replace the **template** program's name in each. Diffing `tribomirim/` against `butterfly-effect/` shows exactly which lines vary:

| File | Strings to update |
|---|---|
| `index.html` | `<title>` · `<meta name="description">` · `<meta property="og:url">` (`https://www.truesight.me/programs/<slug>/`) · `<meta property="og:title">` · `<h1 id="program-name">` |
| `members.html` | `<title>` · `<meta name="description">` · `<h1>` · the "no participants on file yet" copy block |
| `credentials/index.html` | `<title>` · `<meta name="description">` |

Everything else (nav, footer, layout, fetch logic) is shared and stays untouched.

### 16.5 Add a card to `programs.html`

Open `programs.html` and add another `<a class="program-card">` block inside `<div class="programs-grid">`, matching the existing pattern. Required:

- `href="programs/<program_slug>/index.html"`
- `data-program-slug="<program_slug>"` — wires the status pill (`onboarding`/`active`/`archived`) from manifest.json onto the card automatically
- `<div class="name">` — display name
- `<div class="partner">` — partner organization + short subtitle
- `<div class="tagline">` — one-sentence hook (can mirror `manifest.tagline` or rephrase for card context)
- `<span class="cta">View program →</span>` — the CTA text is **"View program →"** (the card navigates to the program landing, NOT the cohort; the cohort link is on the landing page itself — see 2026-05-16 fix in `truesight_me_beta#110`)

### 16.6 Verify locally

```bash
cd ~/Applications/truesight_me
python3 -m http.server 8765
```

Open `http://localhost:8765/programs.html` in a browser:

1. New card appears in the grid (and shows an *Onboarding* pill if `manifest.status === "onboarding"`)
2. Click "View program →" → lands on `/programs/<program_slug>/index.html` with partner logo + tagline + description rendered from manifest
3. From there, click "View cohort →" → lands on `/programs/<program_slug>/members.html` (empty state if no members yet — that's correct)
4. (Optional, once first member exists in `lineage-credentials`) visit `/programs/<program_slug>/credentials/#<member-slug>` and confirm the co-branded CV renders

### 16.7 PR + merge + promote to prod

```bash
git add programs.html programs/<program_slug>/
git commit -m "Add <Display Name> program scaffold (status: onboarding)"
git push -u origin feat/program-<program_slug>
gh pr create --title "Add <Display Name> program scaffold" --body "..."
gh pr merge <PR#> --squash --delete-branch

# Promote beta → prod (see NOTES_truesight_me.md):
gh repo sync TrueSightDAO/truesight_me_prod \
  --source TrueSightDAO/truesight_me_beta --branch main
```

Wait ~60–90 s for the prod `pages build and deployment` workflow, then cache-bust to verify:

```bash
curl -s "https://truesight.me/programs.html?$(date +%s%N)" | grep -c '<program_slug>'
```

**Ignore** the `Visual Consistency Tests` CI failure — broken since at least 2026-05-15 (`Process from config.webServer exited early.`), not introduced by your PR.

### 16.8 After the first cohort member exists

When `lineage-credentials/_cache/index.json` gets a member with the matching `primary_program`:

1. The members listing populates automatically on next page load (no code change needed)
2. Each member's CV page (`/credentials/#<member-slug>`) and the program-scoped wrapper (`/programs/<program_slug>/credentials/#<member-slug>`) both work; canonical QR at `_cache/cv/<member-slug>.qr.png` is generated by `lineage-engine/scripts/qr_code.py` (see `CREDENTIALING_PLATFORM.md` §9)
3. Flip `manifest.status` from `"onboarding"` → `"active"` and bump `last_reviewed`, ship as a small follow-up PR through the same beta→prod promote path

### 16.9 Per-program QR + PDF (Phase 3a)

For the program-scoped credential wrapper to carry the partner-logo QR + matching PDF (instead of the generic TrueSight QR), follow Phase 3a (§15):

1. Vendor the partner logo at `lineage-engine/scripts/program_assets/<program_slug>/logo.png` (square, transparent background, ≥256px)
2. Trigger a `build-cv-cache.yml` workflow run on `lineage-credentials`
3. The new `_cache/cv/<slug>__<program_slug>.qr.png` + `.pdf` artifacts emit on the next build (skipped silently if no vendored logo exists)

Skip this step until the partner is ready to print physical certificates — the canonical TrueSight QR works as a default and a scan still resolves to the program-scoped credential URL when §15.5 fallback is in place.

### 16.10 Printed-cert QR codes (defer until first cohort prints)

See §8. Tooling: clone `tokenomics/google_app_scripts/agroverse_qr_codes/batch_compiler.py` into a `cert_compiler.py` variant. Not blocking program-page rollout.

---

## 17. Phase 3b — partner-branded PDF templates (certificate output)

> **Scope:** the PDF that lives at `_cache/cv/<slug>__<program>.pdf` currently has the same body as the canonical CV PDF — only the embedded QR differs (§15). Phase 3b makes the per-program PDF a *real certificate* — partner-branded, suitable for printing on heavy paper, handed to the participant as proof of completion. The canonical PDF stays as it is (no change to `_cache/cv/<slug>.pdf`).

> **Status (2026-05-17):** Phase 3b is **specified only**. No code yet. Ship when Bilal needs the first physical Butterfly Effect certificates, or when a Tribo Mirim student progresses from "practice log" to "lineage milestone" and wants a printable artifact.

### 17.1 Why this is a separate phase from 3a

Phase 3a's contract was minimal: same PDF body, QR points at the program-scoped URL. That's enough to fulfill "every credential page has its own QR + downloadable PDF". Phase 3b answers a different question: *"what does the PDF actually look like when you print it on cardstock and hand it to a kid?"*

Splitting the phases means partner programs can onboard, accumulate practice records, and let participants self-serve a downloadable proof PDF *before* the operator has to commit to the visual design of a certificate. The Phase 3a PDF is "good enough to share digitally"; the Phase 3b PDF is "good enough to frame on a wall."

### 17.2 What Phase 3b changes (in the rendering pipeline)

The change point is `lineage-engine/scripts/build_cv_cache.py::render_html(cv, md, qr_path)`. Today it returns a single shared CSS + body for both canonical and per-program PDFs. Phase 3b adds an optional `program_scope` argument:

```python
def render_html(cv, md_body, qr_path=None, program_scope: str | None = None) -> str:
    """When program_scope is set, render the partner-branded certificate
    template instead of the canonical CV template. Both templates share
    the same Markdown body but differ in chrome (header banner, footer
    signature lines, paper size hint, ornamentation)."""
```

The per-CV write loop in `build()` passes `program_scope=<url-program-slug>` for each per-program PDF emit (§15.4 already iterates `cv.programs`; just plumb the argument through).

### 17.3 Per-program PDF template files

Phase 3b introduces a new asset class in `lineage-engine`:

```
lineage-engine/scripts/program_assets/
├── <url-program-slug>/
│   ├── logo.png                  (existing — drives QR centre and the certificate header banner)
│   ├── cert_template.html        (new — partial HTML that wraps the CV body in a certificate frame)
│   └── cert_styles.css           (new — partner-branded typography + colours)
```

`cert_template.html` is a small Jinja-like template (or just a Python `.format()` string — keep it dependency-free) with named slots:

```html
<!-- programs/tribomirim/cert_template.html -->
<div class="cert-banner">
  <img class="cert-logo" src="{partner_logo_uri}" alt="{partner_name}" />
  <div class="cert-program">{program_display_name}</div>
  <div class="cert-issuer">Lineage root: {issuer_lineage_root}</div>
</div>
<div class="cert-body">{cv_body_html}</div>
<div class="cert-footer">
  <div class="cert-signature-line">
    <div class="cert-sig-blank"></div>
    <div class="cert-sig-label">{lineage_root_signatory}</div>
  </div>
  <div class="cert-qr-block">
    <img class="cert-qr" src="{qr_uri}" />
    <div class="cert-qr-caption">scan to verify · {credential_url}</div>
  </div>
  <div class="cert-meta">Issued by TrueSight DAO · {issued_at}</div>
</div>
```

`cert_styles.css` is partner-specific — Tribo Mirim leans warm earth tones, Butterfly Effect leans transformation-blue, etc. Inherits paper size + page margins from a shared `program_assets/_cert_base.css` to keep page geometry consistent across partners.

### 17.4 Template variables

The render path passes these into `cert_template.html.format(**ctx)`:

| Variable | Source | Notes |
|---|---|---|
| `partner_logo_uri` | `program_assets/<slug>/logo.png` as `file:///…` | Same vendored PNG as the QR centre |
| `partner_name` | `program_assets/<slug>/manifest_mirror.json::partner_organization` OR fetched from `truesight_me/programs/<slug>/manifest.json` at build time | One source-of-truth; pick the lazier one |
| `program_display_name` | `manifest::display_name` | "Tribo Bahia Mirim — Capoeira lineage" |
| `issuer_lineage_root` | `manifest::issuer_lineage_root` | "Bico Duro" |
| `lineage_root_signatory` | `manifest::lineage_root_signatory` (new manifest field) | "Mestre Bico Duro" — printed name on the signature line |
| `cv_body_html` | `render_markdown(cv) → md → html` | Same body that drives the canonical CV |
| `qr_uri` | `_cache/cv/<slug>__<program>.qr.png` as `file:///…` | Per-program QR, embedded |
| `credential_url` | `PROGRAM_CREDENTIAL_URL.format(...)` | Human-readable scan target |
| `issued_at` | First non-zero `recent_events[].captured_at` OR most recent event for "in progress" certs; for "completion" certs, the explicit completion event timestamp | See §17.6 |

### 17.5 Paper / page geometry

Defaults that work for both home printers and a print shop:

- Page size: A4 (Brazil + most international). Override via `cert_template.html::@page` block per partner if needed (US Letter for North-America-only programs).
- Margins: 18mm top/bottom, 16mm left/right — leaves room for a frame ornament without crowding text.
- Single page is the goal. If the CV body is long enough to push to page 2, the template should overflow the body — the banner + signature lines stay on page 1 so a single physical print still looks like a certificate.
- Background colour: pure white (printable). Banner gradient or ornament is fine; never use a full-bleed photographic background (eats ink, looks bad on paper).

### 17.6 Completion signal (the "are we ready to print" gate)

Today's `_cache/cv/<slug>__<program>.pdf` regenerates on every practice event — fine for digital sharing, problematic for physical printing (you don't want to hand someone a certificate, then have a newer version supersede it days later).

Two signals Phase 3b introduces:

1. **`cv.programs[<program>].status`** — `in_progress` (default) or `completed`. Set explicitly by an attestor event (e.g., a `corda-promotion` event in capoeira-tribo-mirim, or a per-program completion event for Butterfly Effect). The template branches on this:
   - `in_progress` → the PDF says "Practice log · as of {issued_at}" in the meta line
   - `completed` → the PDF says "Certificate of completion · {completed_at}"
2. **`cv.programs[<program>].locked_at`** — once set (by the attestor's completion event), the cert PDF stops regenerating on subsequent events for that program. The on-disk artifact freezes at the completion-time snapshot. Subsequent practice events still update the canonical `<slug>.pdf` and the *on-screen* program-scoped credential view (`programs/<p>/credentials/#<slug>`) — only the PRINTABLE PDF freezes, because that's the artifact that ends up in someone's hands as the final proof.

Implementation: in `build_cv_cache.py` §15.4 loop, after resolving `url_program_slug`, check `cv.programs[<data_slug>].locked_at`. If present AND the per-program PDF already exists on disk AND its mtime ≥ `locked_at`, skip the PDF rewrite. The QR still regenerates (PNG is cheap, harmless). This keeps the regen pipeline simple — no separate "certificate freeze" workflow needed.

### 17.7 On-screen vs printable distinction

After Phase 3b, the program-scoped credential page shows **two** PDF download options instead of one:

| Button | What it links to | When to use |
|---|---|---|
| "⬇ Practice log PDF" | `_cache/cv/<slug>__<program>.pdf` (current per-program PDF, renamed in label) | Quick share — current state, regenerated on every event |
| "⬇ Certificate PDF" | `_cache/cv/<slug>__<program>__cert.pdf` (new — built only when `locked_at` is set) | Print on cardstock, hand to participant |

The "Certificate PDF" button is hidden (or shown as "Pending completion attestation") until `locked_at` exists for that CV-program pair. This makes the completion moment a visible product event for the participant, not just a sysadmin operation.

Both PDFs embed the same per-program QR. Both QR scans resolve to the same `programs/<p>/credentials/#<slug>` URL. The certificate just has more visual gravity and freezes at the completion state.

### 17.8 Operator workflow to add a partner-branded cert template

1. Partner sends visual direction (colours, typography preference, optional ornament SVG). If they don't have one, the operator drafts something simple-but-on-brand and the partner approves.
2. Operator creates `lineage-engine/scripts/program_assets/<url-slug>/cert_template.html` + `cert_styles.css`. References the existing `logo.png` already vendored from Phase 3a.
3. Adds optional `lineage_root_signatory` field to the partner's manifest (`truesight_me/programs/<slug>/manifest.json`).
4. Local smoke test: pick a real CV in that program (or use `--slug <test-slug>` if `build_cv_cache.py` gets that flag), run a build, open the resulting `__cert.pdf` in Preview / Adobe to eyeball the layout. Iterate.
5. PR the template files. CI re-runs `build_cv_cache.py`; if any CV in that program has `locked_at` set, the cert PDF gets emitted on the next push.
6. To "lock" a CV (turn the printable cert switch on for one participant), an authorized attestor commits a completion event under `programs/<data-slug>/<pk-hash>/attestations/*.json`. Build picks it up, freezes the cert, surfaces the "⬇ Certificate PDF" button on the page.

### 17.9 Why not just template the canonical PDF too?

Two reasons to keep the canonical PDF on its existing simple template:

1. **Single source of truth for "all programs / no program"**. The canonical page (`/credentials/#<slug>`) summarizes a contributor's entire DAO record, possibly across multiple programs. A certificate template is single-program by nature.
2. **The operator's print-day workflow is partner-specific.** Certificates printed for Tribo Mirim look different from certificates printed for Butterfly Effect; the canonical PDF needs to remain "neutral" so it can be handed to job-application reviewers, governance committees, etc.

### 17.10 Phased rollout for Phase 3b

| Sub-phase | What ships | Repos |
|---|---|---|
| **3b.0** (this section) | This §17 addendum to the spec | `agentic_ai_context` |
| **3b.1** | `render_html(program_scope=...)` signature + a fallback that returns the existing template when `program_scope` is `None` | `lineage-engine` |
| **3b.2** | `program_assets/<slug>/cert_template.html` + `cert_styles.css` for the first partner that needs it. Tribo Mirim is the natural first target — Bico Duro can sign milestone certificates; Butterfly Effect waits until Bilal has a cohort | `lineage-engine` |
| **3b.3** | `locked_at` / `status` fields in lineage-credentials event schema + read path in `build_cv_cache.py` | `lineage-engine` + `lineage-credentials` |
| **3b.4** | Page change: "⬇ Practice log PDF" relabel + conditional "⬇ Certificate PDF" button | `truesight_me_beta` → `_prod` |
| **3b.5** | First cohort member's locked certificate printed on real cardstock + visual sign-off | (operator) |

3b.1 and 3b.2 can ship in the same `lineage-engine` PR if they target the same partner. 3b.3 is the heavier change — it touches the data schema, so it benefits from its own PR.

### 17.11 Open questions for Phase 3b

1. **Multi-program completion**: a CV could be `completed` for Tribo Mirim and `in_progress` for Butterfly Effect simultaneously. The per-program scoping naturally handles this (each `<slug>__<program>__cert.pdf` is independently locked) — no design change needed, but worth a sentence in the operator playbook.
2. **Re-issuance**: what if a certificate needs to be re-issued (typo on the participant's name, completion record amended)? Treat it as a new event that overwrites `locked_at` to the new timestamp; the cert PDF rewrites; the old artifact is preserved in git history if anyone needs the prior snapshot.
3. **Cohort batch-print**: when ERA needs to print 30 Butterfly Effect certificates at once, the operator probably wants a single multi-page PDF (each page is one cert). Phase 3b emits per-CV PDFs only; a batch wrapper is Phase 3c territory (or just an operator-side `pdfunite` command — defer until volume warrants tooling).
4. **Frame ornament asset**: optional SVG corner-ornaments / dingbats per program (Tribo Mirim might use a stylized berimbau; Butterfly Effect literally a butterfly outline). Vendor in the same `program_assets/<slug>/` directory if used. No design change required for the engine — just another file the template references.

### 17.12 What's intentionally NOT in Phase 3b

- **Cohort dashboards for partners** ("show me everyone we've certified this quarter") — that's a separate `programs/<p>/cohort.html` surface, deferred indefinitely.
- **Notification on certification** (email the participant or their guardian when `locked_at` flips) — operator's email workflow; not engine plumbing.
- **NFT / on-chain attestation of the certificate** — if/when this matters, it's a layer on top of `locked_at`. Out of scope here.
- **Verifiable Credentials (W3C VC) format export** — possibly a Phase 4 export pipeline. The on-chain proof of issuance lives in the existing DAO ledger already; VC export is just a presentation format.

### 17.13 Two strategies — partner-supplied PDF overlay vs HTML template

Not every partner brings the same starting materials. Some (ERA's Butterfly Effect) hand us a finished PDF that already encodes their visual brand — borders, ornaments, signature blocks, school co-branding — and just need us to fill in name + date + QR. Others (a future small program with no design resources of their own) need us to *generate* the certificate from a clean HTML/CSS template. Phase 3b supports both, dispatched on a single manifest field.

#### 17.13.1 Manifest declaration

```json
{
  "...": "...",
  "certificate": {
    "strategy": "pdf_overlay",
    "pdf_template": "cert_template.pdf",
    "font_files": ["fonts/EBGaramond-Italic-VariableFont_wght.ttf"],
    "overlay_fields": {
      "recipient_name": {
        "x_pt": 429.5, "y_pt": 268,
        "font": "EBGaramond-Italic", "size_pt": 32,
        "anchor": "center", "color": "#1a2a5a",
        "max_width_pt": 600
      },
      "date": {
        "x_pt": 178, "y_pt": 140,
        "font": "EBGaramond-Italic", "size_pt": 14,
        "anchor": "center", "color": "#1a2a5a",
        "format": "%-d %B %Y"
      },
      "qr": {
        "x_pt": 750, "y_pt": 80,
        "size_pt": 70
      }
    }
  }
}
```

Two strategies supported:

| Strategy | Manifest field | When to use |
|---|---|---|
| `"html_template"` (default if absent) | `certificate.html_template` (file ref, optional override) | Partner has no design materials; generate from `program_assets/<slug>/cert_template.html` + `cert_styles.css` as spec'd in §17.3 |
| `"pdf_overlay"` | `certificate.pdf_template` + `font_files` + `overlay_fields` | Partner provides a finished PDF; engine overlays name + date + QR at supplied coordinates |

Future strategies (e.g., `"svg_template"`, `"wallet_card"`) can be added with the same dispatch — they're new branches in `build_cv_cache.py::render_certificate(cv, manifest)`.

#### 17.13.2 `overlay_fields` semantics (pdf_overlay strategy)

Coordinates are in **PDF points** (1pt = 1/72 inch). Origin is the **bottom-left** of the page, matching PDF native convention (this is the opposite of HTML/CSS where origin is top-left — easy to forget when reading off a measuring tool).

| Field | Required | Default | Notes |
|---|---|---|---|
| `x_pt`, `y_pt` | yes | — | Position; if `anchor=center`, this is the centre of the text/image; if `anchor=left`/`right`, it's the corresponding baseline-anchor |
| `font` | for text fields | system default | Must reference a registered font name; load via `font_files` |
| `size_pt` | for text fields | 12 | Glyph size in points |
| `anchor` | no | `left` | `left` \| `center` \| `right` |
| `color` | no | `#000` | Hex colour for text |
| `format` | for `date` only | `%Y-%m-%d` | strftime pattern; applied to `locked_at` or the latest event timestamp depending on completion state |
| `max_width_pt` | no | unlimited | If set, name auto-shrinks (-2pt steps) until it fits — prevents long names overflowing the cert |
| `size_pt` | for `qr` | 64 | Square QR width |

#### 17.13.3 PDF overlay implementation

A new module `lineage-engine/scripts/cert_overlay.py` does the heavy lifting:

```python
def render_certificate_pdf_overlay(
    template_pdf: Path,
    out_path: Path,
    fields: dict,
    *,
    recipient_name: str,
    issued_at: datetime,
    qr_path: Path,
    font_files: list[Path],
) -> None:
    """Open the template PDF, overlay text + QR at the specified coordinates,
    write the merged PDF to out_path. Single-page templates only; multi-page
    handled by repeating the page-1 overlay (not expected use case)."""
```

Implementation libraries:
- `pypdf` (already in lineage-engine via `qr_code.py` chain) to read the template page
- `reportlab` to draw text + image on a fresh canvas
- `pypdf.PdfWriter` to merge the canvas atop the template

Single-page templates are the only supported variant for V1. Multi-page certs (handout packets, etc.) are deferred.

#### 17.13.4 build_cv_cache.py dispatch

The existing `cv.programs` loop already emits `<slug>__<program>.qr.png` + `<slug>__<program>.pdf` (Phase 3a). Phase 3b adds a third artifact: `<slug>__<program>__cert.pdf` — the actual partner-branded certificate.

```python
# After §15.4 per-program QR + practice-log PDF emit:
cert_strategy = (manifest.get('certificate') or {}).get('strategy', 'html_template')
if cert_strategy == 'pdf_overlay':
    overlay_render(
        template_pdf=PROGRAM_ASSETS_DIR / url_program_slug / manifest['certificate']['pdf_template'],
        out_path=cv_dir / f'{slug}__{url_program_slug}__cert.pdf',
        fields=manifest['certificate']['overlay_fields'],
        recipient_name=cv.get('display_name') or slug,
        issued_at=resolve_issued_at(cv, url_program_slug),
        qr_path=cv_dir / f'{slug}__{url_program_slug}.qr.png',
        font_files=[PROGRAM_ASSETS_DIR / url_program_slug / fp for fp in manifest['certificate'].get('font_files') or []],
    )
elif cert_strategy == 'html_template':
    # Deferred — implement when a real partner needs it.
    pass
```

The HTML strategy stays no-op until a real partner without their own PDF shows up; ships as a stub branch so the dispatch logic exists.

#### 17.13.5 Where the manifest lives

`certificate.strategy` is on the **truesight_me** program manifest (`truesight_me/programs/<slug>/manifest.json`), NOT the lineage-credentials data-side manifest. Reason: the certificate is a publication artifact, not a data event; the URL-side manifest is the source of truth for "how do we render this program's outputs."

`build_cv_cache.py` must therefore fetch the truesight_me manifest at build time (or use a vendored mirror). Cheapest path: at the top of the build, for each `url_program_slug` known to the registry, fetch `https://raw.githubusercontent.com/TrueSightDAO/truesight_me_prod/main/programs/<slug>/manifest.json` once and cache the dict for the rest of the run. Network dependency added — keep it on a soft fail (warn + skip cert emit if the manifest can't be fetched), don't break the whole build over it.

#### 17.13.6 The first partner to use this — Butterfly Effect (ERA + Narowal Public School)

Bilal supplied:
- `Final Certificate Without Name and Date.pdf` — the blank template (859×612pt, school-co-branded, signatory: Shereen Abdullah, "Butterfly Effect Club Program 2025-2026")
- `Final Certificate With Name and Date.pdf` — a hand-filled scanned sample (showed where name + date land)
- Requested font: `EBGaramond-Italic-VariableFont_wght`
- QR placement: not specified — operator-proposed bottom-right corner, ~70pt square, inside the ornamental border; iterate if Bilal asks for somewhere else

The cert is school-cohort-specific. Future Butterfly Effect cohorts at other schools or in other years will likely want different templates — the engine handles this naturally because the template is per-program, not per-deployment; if needed, split into `butterfly-effect-narowal-2025` and `butterfly-effect-<next-school>-<year>` programs in the registry.

---

## 18. Phase 4 — contribution freshness (three sources, two surfaces)

> **Scope:** today the credential page at `truesight.me/credentials/#<slug>` only reflects what's in the **Ledger history** tab of the Main Ledger spreadsheet, which is the canonical governor-reviewed record — but it only rolls over once per quarter. Contributors logging work today don't see it on their credential for up to ~3 months. Phase 4 closes the freshness gap by adding two more data sources alongside Ledger history, with a clear web-vs-PDF doctrine for what each surface includes.

> **Status (2026-05-18):** Phase 4 is **specified only**. No code yet. Implementation follows the same Phase 0 → Phase N spec-then-code discipline.

### 18.1 Why three sources

A credential answers two slightly different questions:

| Question | What it needs |
|---|---|
| "Has the DAO formally recognized this work?" | Settled records with a TDG amount attached |
| "What has this contributor done lately?" | Submitted activity, even if pending review |

Today the credential page only answers the first. Phase 4 makes it answer both, distinctly. The data divides cleanly into three sources:

| Source | Spreadsheet · Tab | Freshness | Authority | What it covers |
|---|---|---|---|---|
| **Ledger history** | `1GE7PUq…` · `Ledger history` | Updated quarterly | Canonical · TDG-settled · governor-approved | All manual contributions + GAS-tokenized recurring contributions, after they've been promoted |
| **Scored Chatlogs (pending)** | `1Tbj7H5…` · `Scored Chatlogs` (col L empty) | Daily — every new submission | Submitted, not yet reviewed | Manual contributions awaiting governor scoring since 2024-12-13 (start date of this sheet) |
| **Recurring Transactions (derived pending)** | `1GE7PUq…` · `Recurring Transactions` | Spec-of-recurring (column F = last tokenization date) | Settled-on-cadence · expected-but-not-yet-tokenized | Derived: pending recurring charges since last tokenization, computed from `(today - F) × billing-period × amount` |

### 18.2 Dedup — single primary key

The dedup story is unusually clean because the existing GAS that promotes Scored Chatlogs → Ledger history already records the join on the source row:

- **`Scored Chatlogs!L` ("Main Ledger Row Number")** is the foreign key. When a scoring is approved, the GAS writes the Ledger history row number into Scored Chatlogs column L.
- **Rule for Phase 4**: a Scored Chatlogs row is "pending" iff column L is empty. Rows with column L populated are already covered by Ledger history; skip them.
- No fuzzy matching, no timestamp-based join, no contributor-name normalization. The GAS owns the dedup; we just honor it.

### 18.3 Two presentation surfaces, two doctrines

| Surface | Includes | Rationale |
|---|---|---|
| **Web credential page** (`truesight.me/credentials/#<slug>` and per-program `programs/<p>/credentials/#<slug>`) | **All three sources, visually distinct** | The web is the live view. A contributor logging work today should see it the next day, even if unreviewed. A reader looking at the same page should be able to tell at a glance which entries are formally recognized vs claimed. |
| **Printed PDF certificate** (`<slug>__<program>__cert.pdf`, `<slug>.pdf`) | **Ledger history only** | The PDF is the formal frozen artifact handed out — a printable cert with "pending review" entries would undercut its meaning. Same doctrine as §17.6 / Phase 3b: certificates print canonical state, never speculative state. |

The on-screen `<slug>.pdf` (the existing canonical CV PDF) follows the same rule as the printed cert — canonical only — so the contributor's "Download PDF" never produces a snapshot that mixes pending claims with recognized work.

### 18.4 Web page layout

Section ordering on `credentials/#<slug>` (and the program-scoped equivalent):

```
1. [hero / identity / governance section — existing]

2. == Recognized contributions ==
     (sourced from Ledger history; this is the existing list)
     - TDG amounts displayed
     - Items grouped by Initiative / Project / etc. as today
     - Status implied: "recognized"

3. == Recent activity (pending governor review) ==
     ⚠ Submitted since 2024-12-13. Not yet TDG-settled.
        Recurring contributions auto-tokenized by GAS aren't shown here —
        they appear in Recognized contributions after each quarterly settlement.
     (sourced from Scored Chatlogs WHERE col L is empty)
     - No TDG amounts (TDGs Provisioned shown as advisory, with "pending" label)
     - Each item gets a "pending" pill
     - Items chronologically descending

4. == Expected recurring (since last tokenization) ==
     ⚠ Derived from Recurring Transactions registry. Auto-tokenized periodically.
     (computed: for each active recurring entry, list the period(s) since
      column F's Most Recent Tokenization Date with implied amount)
     - Shown with "auto · pending tokenization" pill
     - Suppress entirely if last tokenization < 7 days ago (no actionable
       freshness gap yet)

5. [existing footer / links / etc.]
```

Visual treatment for the status pills:

- **Recognized**: no pill (default; section header is enough)
- **Pending review**: warm-amber pill, same palette as the `Onboarding` pill on `programs.html` — signals "in progress / not yet final"
- **Auto · pending tokenization**: muted-grey pill — signals "the system will get to this on schedule, no action needed from anyone"

Caveat banners must be at the top of each non-canonical section (not buried in a tooltip) so a casual reader who skims the page can't mistake pending entries for recognized ones.

### 18.5 The 2024-12-13 floor

Scored Chatlogs's first entry was 2024-12-13. Any contributor whose pending claims would fall before that date can't be surfaced through this source — the freshness gap for older claims is unaffected by Phase 4. The caveat banner in section 3 of the web layout must include "since 2024-12-13" verbatim so readers know what they're looking at.

### 18.6 Recurring Transactions — derived pending

The `Recurring Transactions` tab is a *registry* of recurring rewards/charges, not a per-event log. Schema (headers on row 4):

| Col | Field |
|---|---|
| A | Description (e.g., "Wix - TrueSight.Me") |
| B | Source |
| C | Transaction Type (e.g., "Vault Draw down") |
| D | Amount (USD) |
| E | Billing Period (Monthly / Quarterly / …) |
| F | Most Recent Tokenization Date (YYYYMMDD) |
| G | Start Date |
| H | Edgar AWS Billing Automation Security Key Identifier |
| I | Automation Remarks |

The lineage-engine build can compute "expected recurring activity since last tokenization" per recurring entry: number of billing-period units between F and today × D = pending recurring weight (USD). This isn't a contribution **claim** — it's a confidence-grade estimate of what the next quarterly tokenization will roll forward.

Surface only when the gap is meaningful (≥ 7 days since column F) and only on records associated with the slug being viewed. The association may be by **B Source** + a name-match against the contributor list, or by a future explicit pk-hash column on the tab if it becomes worth adding.

### 18.7 lineage-engine implementation outline

New fetcher: `lineage-engine/scripts/fetch_pending_chatlogs.py` (mirrors `fetch_contributions.py`'s shape but reads `1Tbj7H5…` / `Scored Chatlogs` and filters where col L is empty).

New fetcher: `lineage-engine/scripts/fetch_recurring_registry.py` (reads `1GE7PUq…` / `Recurring Transactions`, headers row 4; computes derived pending entries per contributor since column F).

`build_cv_cache.py::build_unified_cv` then merges three streams into the CV record under separately-named keys:

```python
cv['dao_contributions']           # existing — Ledger history settled
cv['pending_contributions']       # new — Scored Chatlogs col L empty
cv['expected_recurring']          # new — derived from Recurring Transactions
```

The HTML renderer reads all three; the markdown renderer (used for the PDF) reads only `cv['dao_contributions']`. That's the entire doctrine split — one render path branches on `program_scope`, the markdown→PDF path is unchanged.

### 18.8 Per-program credential pages

The per-program page (`programs/<p>/credentials/#<slug>`) already shows ONLY records from that program (filtered in §15.4). Phase 4 surfaces the same three sources but filtered to that program — so "Recent activity (pending)" for Butterfly Effect on Bilal's page lists only Butterfly Effect-related Scored Chatlogs entries, not all his DAO submissions.

Filter key for Scored Chatlogs → program: needs investigation. The Scored Chatlogs schema doesn't have a `program` column natively. Likely a fuzzy match against column B (Project Name) — e.g., entries whose Project Name contains the program's display name. Defer the filtering implementation until Phase 4 actually ships; document the open question here so it doesn't get re-derived.

### 18.9 Phased rollout for Phase 4

| Sub-phase | What ships | Repos |
|---|---|---|
| **4.0** (this section) | This §18 addendum | `agentic_ai_context` |
| **4.1** | `fetch_pending_chatlogs.py` + `build_unified_cv` merges `pending_contributions` into the CV. Web page renders the new section with caveat banner. PDF unchanged. | `lineage-engine` + `truesight_me` |
| **4.2** | `fetch_recurring_registry.py` + derived `expected_recurring`. Web page renders the third section. PDF still unchanged. | `lineage-engine` + `truesight_me` |
| **4.3** | Per-program filter for Scored Chatlogs by project name fuzzy-match | `lineage-engine` |
| **4.4** | (Optional) Operator dashboard surface showing aggregate pending → settled latency per quarter — useful for the governance team to monitor scoring throughput | separate, future |

4.1 and 4.2 are independent and can ship in any order. 4.1 is the bigger user-visible win (Scored Chatlogs is daily-updated and covers manual contributions; Recurring Transactions is slower-moving).

### 18.10 Open questions for Phase 4

1. **Scored Chatlogs → per-program filter** (§18.8). Needs a join key from Scored Chatlogs row to a `programs/<p>` membership. Either via column B fuzzy match or by adding a new column on the sheet. Punt until 4.3.
2. **Naming for "Expected recurring"** — is there a better label than "Expected"? "Accruing", "Pre-tokenization", "Auto-pending" all candidates. Decide when 4.2 lands.
3. **Order of sections 3 and 4 on the web page** — recent activity first, or expected recurring first? Recent activity is human-driven and more interesting per-contributor; expected recurring is system-driven and rarely actionable. Lean recent first; revisit after operator review.
4. **What happens if a Scored Chatlogs entry has col L populated but the referenced Ledger history row doesn't exist?** Treat as orphan; skip from both lists. Log a warning. Should be vanishingly rare given the GAS owns both writes.

### 18.11 What's intentionally NOT in Phase 4

- **Backfilling pre-2024-12-13 pending entries** — historical claims weren't tracked in this sheet; no source to surface from. The freshness gap there is a documentation/expectations issue, not a data integration one.
- **Re-issuing PDF on every Scored Chatlogs append** — the PDF stays canonical-only, so it only regenerates when Ledger history changes (quarterly cadence). Avoids cert PDF churn for every minor submission.
- **Web page caching strategy for the new sources** — same jsDelivr-primary + raw.github-fallback as the rest of the lineage feed. The cache-buster pattern shipped in `truesight_me_beta` `e36743e` already handles the freshness story for index.json; the new per-CV reads benefit from the same default.
- **Verifiable Credentials (W3C VC) export including pending claims** — claims-vs-credentials distinction is hard there. Skip for now.
