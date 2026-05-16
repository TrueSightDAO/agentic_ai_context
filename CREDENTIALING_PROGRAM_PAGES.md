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
