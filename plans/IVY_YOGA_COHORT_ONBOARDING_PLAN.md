# IVY (Liv for Yoga) — cohort credentialing onboarding: plan of record

**Status:** plan-of-record, drafted 2026-08-18 by Claude (interactive session, Gary driving). Second program on the
TrueSight DAO credentialing platform, following the same shape as
[Butterfly Effect](https://github.com/TrueSightDAO/butterfly-effect-club) (`BUTTERFLY_EFFECT_COHORT_ONBOARDING_PLAN.md`).

**Companion docs (read before executing):**
- `credentials/CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` — the canonical operator playbook this plan instantiates
- `credentials/CREDENTIALING_PLATFORM.md` — overall data model
- [`butterfly-effect-club/PROPOSAL.md`](https://github.com/TrueSightDAO/butterfly-effect-club/blob/main/PROPOSAL.md) — the v4 architecture decision log this program reuses verbatim

**Source context:** `WhatsApp Chat - ERA DAO.zip` (~/), messages 8/17–8/18/26. Bilal (ERA Professionals) is building
IVY, a yoga-teacher-training certification based on Olivia's "Liv for Yoga" curriculum (Bikram Chaudhry's 26-posture
regimen lineage). First real cohort not until fall 2027 — **no launch urgency**; this plan stands up the
infrastructure now while it's easy to get right.

---

## 0. Naming decisions (locked)

| Item | Value | Rationale |
|---|---|---|
| `program_slug` | `ivy-yoga` | Matches the service account Gary already created — follow the name already in motion rather than invent a new one. (Its real email turned out to be `ivy-yoga-get-data-io-iam-gserv@get-data-io.iam.gserviceaccount.com`, not the shorter `ivy-yoga@...` everyone assumed — see §1 update below.) |
| Subdomain | `ivy-yoga.truesight.me` | `<slug>.truesight.me`, same pattern as `butterfly-effect-club.truesight.me`... adjusted to slug form for consistency with the SA/manifest slug. |
| GitHub repo | `TrueSightDAO/ivy-yoga-club` | `<slug>-club`, per the template's own fork-name convention (`CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` §5.2). |
| Workspace path | `/opt/claude_workspace/ivy_yoga_club` | Underscored, mirrors `butterfly_effects_club/` local convention. |
| `display_name` | `IVY` | As used by Bilal throughout the WhatsApp thread. |
| `partner_organization` | `ERA Professionals` | Same parent org as Butterfly Effect. |
| Lineage note for copy | "based on Olivia's Liv for Yoga training program, rooted in Bikram Chaudhry's 26-posture regimen" | Bilal's own wording, 8/17/26 12:08 PM. |

---

## 1. Pre-flight (§5d — every cross-repo fact an execution unit needs, captured here)

All of the following were verified live during this planning session — no execution unit needs to re-discover them:

1. **Roster sheet (already created by Bilal, shared by Gary):**
   `https://docs.google.com/spreadsheets/d/1IrzM8z9X0bt-1Zp21s6DNxlL_1XaT-8Fq6e3YaQRcnU/edit`

2. **Central tokenomics credentialing GAS already resolves this sheet — live-tested 2026-08-18:**
   ```
   GET https://script.google.com/macros/s/AKfycbytzZtEhKEHCmxoSbhQXrg5Clc7imS24BFT134nu9yN4QvMCuQfhzEHgbuT8PRYcxgtGQ/exec
       ?action=list_sheet_editors&sheet_url=<IVY roster URL>
   → {"status":"ok","editors":["garyjob@agroverse.shop","garyjob@gmail.com",
      "danesh@onemarketcapital.com","arshad@onemarketcapital.com",
      "bilal@onemarketcapital.com","shahbaz@onemarketcapital.com"]}
   ```
   Confirms **no tokenomics-side code change is needed** (matches playbook §5.4 — "No tokenomics work needed"; the
   central handler is generic across programs). This endpoint value is the `tokenomics_admin_endpoint` to put in the
   IVY manifest — same URL as Butterfly Effect's, verbatim.

   **⚠️ Open item, not blocking:** `ivy-yoga@get-data-io.iam.gserviceaccount.com` (the SA Gary shared the sheet
   with) does **not** appear in the `list_sheet_editors` response above. The humans who matter (Bilal, Shahbaz,
   Gary) do resolve correctly, so admin-panel auth will work. But if a future local/CI script needs to read the
   sheet via that SA's JSON key (`~/ivy_yoga_google_private_key.json`), verify the share actually landed —
   re-share from the Sheet's own "Share" dialog if the SA still doesn't show as an editor there.

3. **Real manifest schema to model IVY's on** (not the older placeholder in the onboarding playbook — this is the
   file actually in production today): `truesight_me/programs/butterfly-effect/manifest.json`. Full field list:
   `schema_version, program_slug, display_name, partner_organization, partner_url, partner_contact_label, tagline,
   description_md, co_brand{partner_logo_url,primary_color,secondary_color}, source_pages[], membership_filter
   {primary_program}, credential_visibility_default, issuer_lineage_root, status, certificate{strategy,available,
   label}, program_mode, roster_sheet_url, roster_tab, audit_trail_tab, admin_panel_url, program_repo,
   tokenomics_admin_endpoint, last_reviewed`.

4. **Fork target confirmed to exist:** `TrueSightDAO/program-template` (default branch `main`) — sanitized mirror
   of butterfly-effect-club with `TODO` placeholders, per `CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` §5.2/§6.

5. **DNS precedent (Explorya AWS account `440626669078`, Route53 zone `Z0032474227N6EQ3Z4QU` for `truesight.me`):**
   existing record —
   ```
   butterfly-effect-club.truesight.me.  CNAME  300  truesightdao.github.io
   ```
   IVY's record will be the identical shape, just the new subdomain. `truesight.me` DNS lives in the **Explorya**
   AWS account, not Nelanco — use `AWS_ACCESS_KEY_ID_EXPLORYA` / `AWS_SECRET_ACCESS_KEY_EXPLORYA` from
   `truesight_autopilot/.env`.

6. **`truesight_me` local clone tracks the beta repo**, not prod: `origin` = `TrueSightDAO/truesight_me_beta`.
   Per the beta-first rule (`WORKSPACE_CONTEXT.md` §3f), this plan lands the manifest in **beta only**.
   Promotion to `truesight_me_prod` (`gh repo sync`) is a **human-only, explicitly-requested action** — not part
   of this plan's execution units.

7. **✅ Resolved 2026-08-18 (same session):** Gary hand-delivered "IVY certificate - blank - v1.2.pdf" and the
   filled "IVY certificate - sample.pdf" (the WhatsApp export had dropped both from its media). Full program name
   is **Indus Valley Yoga**; co-signers are **Bilal Musharraf** (Founding Board Member) and **Olivia Anselmo**
   (Creator, Original Hot Yoga Teacher Training, Liv for Yoga LLC). Fonts identified from embedded PDF font-subset
   names and confirmed against github.com/google/fonts: **Cormorant Garamond** (body/name/dates), **Inter**
   (labels), **Great Vibes** (the two co-signer signatures). All three are open-source (OFL) — full family files
   vendored in `ivy-yoga-club/cert_template/fonts/` (not the PDF's subsetted glyphs, so any recipient name renders
   correctly). Overlay coordinates in `cert_config.json` reverse-engineered by word/image bounding-box extraction
   (pdfplumber + pymupdf) against both PDFs. Logo extracted from the PDF's embedded image, real brand color sampled
   as `#A84504`. Pushed as a second commit on the same `ivy-yoga-club#1` PR branch (§3 PR1).
   **New finding, not yet buildable:** the real design has two overlay field *types* the platform doesn't support
   yet — `signature_bilal`/`signature_olivia` (rendered only once each co-signer independently attests — this is
   Gary's dual-signature design, now visible baked into the actual artwork) and a cosmetic `certificate_id`
   (`IVY-TT-<year>-<seq>`, no generator exists for the sequence). Both documented with real coordinates in
   `cert_config.json` for **PR3** to implement against — see §5.

---

## 2. Authorization envelope (§5e — scoped once, for this whole arc)

Per Gary's instruction this session ("go ahead with execution all the way until ready for UAT"):

- **Pre-authorized, no further asks this arc:** creating/configuring `TrueSightDAO/ivy-yoga-club` (new, empty repo —
  no prod risk); PRs + merges within that repo; enabling GitHub Pages on it; adding the Route53 CNAME in Explorya
  (additive DNS record, mirrors an existing working pattern exactly, zero blast radius to other subdomains); PR +
  merge to **`truesight_me_beta`** (not prod).
- **Always gated, not in this plan's scope:** promoting `truesight_me_beta` → `truesight_me_prod` (human-only,
  `gh repo sync`, per `WORKSPACE_CONTEXT.md` §3f); any first *real* (non-sample) attestation/certificate issuance —
  UAT uses sample data only, per Bilal's own 8/18 message ("It will just have a sample name for now").
- **Deferred to a separate decision, tracked but not executed here (see §5 below):** the recertification-button
  and dual-signature (Bilal + Olivia) feature work — blocked on two open calls Gary hasn't made yet (fee/branding
  model; whether Olivia re-signs every renewal or only Bilal does).

---

## 3. Sequenced plan

| Unit | What | Repo(s) touched | Advance |
|---|---|---|---|
| **PR0** | This plan doc | `agentic_ai_context` | _(auto)_ |
| **PR1** | Fork `program-template` → `ivy-yoga-club`; configure `config.json`/`CNAME`/`README`; PR + merge; enable GitHub Pages; add Route53 CNAME | `ivy-yoga-club` (new), Explorya Route53 | _(auto — greenfield, no prod risk)_ |
| **PR2** | Add `programs/ivy-yoga/manifest.json` (Tier-1 DAO-endorsed listing); PR + merge | `truesight_me_beta` | _(auto — beta only)_ |
| **PR3** *(future, gated)* | Recertification button (date-gated re-attest) + dual-signature (Bilal + Olivia) columns/flow | `tokenomics` GAS, `ivy-yoga-club`, `lineage-credentials` schema | `gate: awaiting Gary's decision on (a) fee/branding model, (b) does Olivia re-sign every renewal` |
| **Promote** *(human-only)* | `truesight_me_beta` → `truesight_me_prod` via `gh repo sync` | `truesight_me_prod` | `gate: prod promote — always-stop` |

**PR1 detail:**
1. `gh repo fork TrueSightDAO/program-template --clone=false --org=TrueSightDAO --fork-name=ivy-yoga-club`
2. Clone to `/opt/claude_workspace/ivy_yoga_club`, branch `feature/ivy-yoga-scaffold`
3. Edit `config.json`: `program_slug: "ivy-yoga"`, `program_display_name: "IVY"`, `partner_organization:
   "ERA Professionals"`, `admin_console_url: "https://ivy-yoga.truesight.me/"`, `public_manifest_url:
   "https://truesight.me/programs/ivy-yoga/manifest.json"`, schema/config URLs pointed at `ivy-yoga-club`
4. Update `CNAME` → `ivy-yoga.truesight.me`
5. Update `README.md` placeholders (program name, live surfaces, quick-start paths)
6. Leave `cert_template/` as the template's placeholder assets; add a `TODO_CERT_ASSETS.md` note pointing at the
   pending Shahbaz hand-off (pre-flight item 7)
7. PR → merge → `gh api repos/TrueSightDAO/ivy-yoga-club/pages -X POST -f build_type=legacy -F
   source[branch]=main -F source[path]=/`
8. Route53: `UPSERT` CNAME `ivy-yoga.truesight.me` → `truesightdao.github.io`, TTL 300, zone
   `Z0032474227N6EQ3Z4QU`, Explorya credentials

**PR2 detail:** copy `truesight_me/programs/butterfly-effect/manifest.json` shape, substitute IVY values
(roster_sheet_url = the IVY sheet from §1.1, admin_panel_url = `https://ivy-yoga.truesight.me/`, program_repo =
`https://github.com/TrueSightDAO/ivy-yoga-club`, tokenomics_admin_endpoint = the URL verified live in §1.2,
description_md drafted from Bilal's framing, `status: "active"`).

---

## 4. Resume tracker

**RESUME HERE → PR3 (gated) — see below.** All PR0–PR2 units plus the 2026-08-20 credentialing session fixes are
merged and live; the only remaining unit is PR3, blocked on Gary's two open decisions (§5).

| Unit | PR | Opened | Merged | Deployed/live | Reported |
|---|---|---|---|---|---|
| PR0 — this plan | [agentic_ai_context#755](https://github.com/TrueSightDAO/agentic_ai_context/pull/755) | ☑ | ☑ | ✅ plan doc on main | ☑ |
| PR1 — repo scaffold | [ivy-yoga-club#1](https://github.com/TrueSightDAO/ivy-yoga-club/pull/1) | ☑ | ☑ | ☑ | ☑ |
| PR1-fix — panel had `butterfly-effect` hardcoded into the live attestation path (`Program` field, manifest URL, localStorage keys) | [ivy-yoga-club#2](https://github.com/TrueSightDAO/ivy-yoga-club/pull/2) | ☑ | ☑ | ☑ | ☑ |
| PR1-fix2 — wrong SA email + stale SCHEMA.md column tables | [ivy-yoga-club#4](https://github.com/TrueSightDAO/ivy-yoga-club/pull/4) (supersedes broken #3) | ☑ | ☑ | ☑ | ☑ |
| GitHub Pages enabled on `ivy-yoga-club` | n/a (repo setting) | — | — | ☑ (`status: built`, HTTPS cert approved) | n/a |
| Route53 CNAME `ivy-yoga.truesight.me` → `truesightdao.github.io` | n/a (DNS) | — | — | ☑ (`INSYNC`, Explorya zone `Z0032474227N6EQ3Z4QU`) | n/a |
| PR2 — truesight_me_beta manifest + program page | [truesight_me_beta#293](https://github.com/TrueSightDAO/truesight_me_beta/pull/293) | ☑ | ☑ | ☑ (manifest live on prod `truesight.me/programs/ivy-yoga/manifest.json`) | ☑ |
| Promote beta → `truesight_me_prod` | n/a (Gary completed manually) | — | ☑ | ☑ (`truesight.me/programs/ivy-yoga/`, CNAME preserved) | n/a |
| Cohort Roster sheet restructured (tab rename, `Status`→`Teaching Status`, 12 audit columns, `Audit Trail` tab added) | n/a (Sheets API, `ivy-yoga-get-data-io-iam-gserv@...` SA, granted Editor 2026-08-18) | — | — | ☑ (verified: `Cohort Roster` + `Audit Trail` tabs, Shamshad Haider's row intact) | n/a |
| PR3 — recertification + co-sign | not started | — | — | — | **blocked on Gary** (§5 open decisions) |

**Post-plan session fixes (2026-08-20, all merged + E2E-verified):**
- lineage-credentials#17 — internal `programs/ivy-yoga/manifest.json` + `fetch-depth: 2` (build was 20–60 min, now ~2.5 min)
- agentic_ai_context#770 — playbook §5.3a: internal data-repo manifest step (REQUIRED for every future program)
- lineage-engine#19 — `registry.json` `ivy-yoga` entry (program-scoped QR/logo compositing)
- lineage-engine#20 — vendored IVY v1.2 cert assets (logo/template/config/fonts) + renderer field support (cert PDFs now render)
- ivy-yoga-club#5 — "Roster sheet ↗" link always visible in console header
- **E2E (dummy data, live stack):** sheet insert → sign-in → attest → registry + certificate render, verified end-to-end
  (pk-AFaVWSOevda8 → dummy-e2e-test-2-cert; base + cert PDFs return 200 via raw + jsDelivr)

**Status:** infrastructure complete + verified; **PR3 is the only remaining unit**, gated on Gary's decisions
(a) fee/branding model and (b) whether Olivia re-signs every renewal.

✅ **Pre-flight Completeness (§5d):** no execution unit in PR1/PR2 requires reading a file/state not already
captured in §1 above.

---

## 5. Open decisions carried forward (not resolved by this plan)

1. **Fee / branding model.** Butterfly Effect is CSR-flavored ($1/certificate → Amazon tree, folded into the
   Sunmint "network of partners" anti-greenwashing framing). IVY is explicitly commercial (Bilal: training +
   certification fees + studio-financing margin, three income streams). Whether IVY certs carry the same
   reforestation fee, sit under the same partner-network branding, or get a distinct commercial structure — Gary's
   call, not yet made. Doesn't block PR1/PR2 (infra is fee-agnostic); **does** block issuing the first real
   (non-sample) certificate.
2. **Recertification scope.** Gary's design: the "Attest" button on an already-certified row re-activates once the
   last-attestation date passes a per-program staleness threshold (stored in the new manifest, e.g.
   `recertification_period_days`). Implementable as a UI/GAS gating rule on the *existing* attestation event log —
   no new field needed, "last renewal" = latest attestation timestamp for that credential. Not yet built (PR3).
3. **Dual signature (Bilal + Olivia).** Two independent named-role buttons, both required, PDF regenerates only
   once both land. This is the exact "co-signed credentials... deferred in v1" case `CREDENTIALING_PLATFORM.md`
   names yoga lineages as the reason to keep the data model open for. Needs `manifest.json.authorized_attestors`
   to grow from a flat list to role-tagged entries (`program_director`, `lineage_authority`). Open sub-question:
   does Olivia need to re-sign on every renewal, or just Bilal (her signature being a one-time lineage-provenance
   fact rather than a time-bound "still active" assertion)? **Confirmed real, not speculative** — the actual v1.2
   cert artwork (§1.7) shows exactly this: an underline + printed name/title for each co-signer, with a script
   ("Great Vibes" font) signature that only renders once that person has attested (visible in
   `reference_sample_filled.pdf`, absent in `cert_template.pdf`). `cert_config.json` has real coordinates for both
   (`overlay_fields.signature_bilal` / `signature_olivia`) for PR3 to implement against. Not yet built (PR3).

---

## 6. UAT phase (human-tested, sample data only — before any real cert circulates)

| # | Surface / URL | What to expect | Interaction | Acceptance criterion | Status |
|---|---|---|---|---|---|
| 1 | `https://ivy-yoga.truesight.me/` | Admin console loads, boots from `config.json`, shows IVY branding | Open the URL in a browser | Page renders with IVY name/colors, no console errors | ✅ **Automated-verified 2026-08-18** — headless check, `#keygenCard` renders, zero console errors, screenshot confirms branding |
| 2 | Same page | Key generation / email registration flow (`create_signature.html` embed) | Click through, register `garyjob@agroverse.shop` (or another sheet-editor email) | Edgar sends a verification email; clicking it binds the pubkey | ☐ **Human-only** — needs Gary/Bilal/Shahbaz to click through; Claude cannot do this on anyone's behalf (it's an identity-binding step by design) |
| 3 | Same page, after verification | Reload — should resolve to **admin mode** | Reload the page | UI shows "pending rows" queue, not a locked-out state | ☐ Depends on #2 |
| 4 | IVY roster sheet (`Cohort Roster` tab) | A sample row exists | n/a — already true | Row visible with empty audit columns | ✅ **Already satisfied** — Shamshad Haider's row (from Shahbaz's original sample) survived the 2026-08-18 restructure untouched |
| 5 | Admin panel | Click "Attest" on the sample row | Single click | `[CREDENTIALING ATTESTATION EVENT]` fires to Edgar; roster row's audit columns back-fill (`pk_hash`, `attestation_tx_id`, `status`, etc.) | ☐ **Human-only** — needs a signed-in admin (depends on #2/#3) |
| 6 | `truesight.me/programs/ivy-yoga/credentials/#<pk-hash>` | Public credential page renders within ~60s of attestation | Visit the URL from the back-filled `profile_url` | Page shows the sample instructor's credential, cert PDF downloadable, QR present | ☐ Depends on #5 |
| 7 | Roster sheet → `Audit Trail` tab | New row appended | Check the tab after step 5 | Row shows `processed_at`, `action`, `github_commit_sha` populated | ☐ Depends on #5 |
| 8 | `ivy-yoga.truesight.me` + `truesight.me/programs/ivy-yoga/` DNS/Pages | Resolves correctly, HTTPS valid | `curl -I` or browser | 200, valid GitHub Pages TLS cert | ✅ **Verified 2026-08-18** — both live, HTTPS cert approved, prod promotion completed (CNAME preserved) |

**Pass criterion for the whole arc:** all 8 rows pass using the sample row only. Do **not** attest a real instructor
until Gary has resolved the two open decisions in §5 and Shahbaz has handed off the real cert template (§1.7 —
**now resolved**, real v1.2 template + fonts are live in the repo).

**What's left is entirely human-in-the-loop.** Steps 2/3/5/6/7 require someone with roster-sheet-editor access
(Gary, Bilal, Shahbaz, Danesh, or Arshad) to actually click through the sign-in flow and hit "Attest" once —
that's the whole remaining UAT surface. Suggested next action: visit `https://ivy-yoga.truesight.me/`, sign in
with any of those emails, verify via the link Edgar sends, then attest Shamshad Haider's row and watch it flow
through to the public credential page.

---

## 7. References

- `credentials/CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` — playbook this plan instantiates
- `credentials/CREDENTIALING_PLATFORM.md` — data model, deferred co-sign/lineage design
- [`butterfly-effect-club`](https://github.com/TrueSightDAO/butterfly-effect-club) — reference implementation
- [`program-template`](https://github.com/TrueSightDAO/program-template) — fork source
- `truesight_me/programs/butterfly-effect/manifest.json` — real manifest schema this plan's PR2 copies
