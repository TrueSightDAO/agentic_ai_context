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
- `truesight_me/js/ecosystem-change-log-feed.js` (PR `truesight_me_beta#82`) — jsDelivr-primary + raw.github-fallback fetch pattern to copy for GFW resilience.

## 14. Last reviewed

2026-05-16 — initial implementation doc. Phase 0 PR.
