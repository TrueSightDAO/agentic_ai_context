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
| `program_slug` | `ivy-yoga` | Matches the service account Gary already created (`ivy-yoga@get-data-io.iam.gserviceaccount.com`) — follow the name already in motion rather than invent a new one. |
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

7. **Assets not yet in hand:** Shahbaz's actual "IVY certificate - blank - v1.2.pdf" (and IVY logo / instructor-name
   font) were sent in the WhatsApp chat but were **not included** in the exported zip's media (WhatsApp trimmed
   attachments on export). The repo scaffold ships with the template's placeholder `cert_template/` assets;
   swapping in the real v1.2 template is a follow-up once Shahbaz hands off the PDF/logo/font files directly
   (not blocking — the admin panel and infra work end-to-end without it, cert *rendering* will look like the
   generic template until swapped).

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

**RESUME HERE → Gary merges the three open PRs below**, then execution resumes at "enable Pages + add DNS" (the
back half of PR1). The harness's own permission layer blocks Claude from self-merging default-branch PRs (hard
stop, correctly enforced even under an explicit "go ahead" instruction earlier in this session) — every PR below
is opened and ready, none are merged.

| Unit | PR | Opened | Merged | Deployed/live | Reported |
|---|---|---|---|---|---|
| PR0 — this plan | [agentic_ai_context#755](https://github.com/TrueSightDAO/agentic_ai_context/pull/755) | ☑ | ☐ **← needs Gary's merge** | n/a | n/a |
| PR1 — repo scaffold | [ivy-yoga-club#1](https://github.com/TrueSightDAO/ivy-yoga-club/pull/1) | ☑ | ☐ **← needs Gary's merge** | ☐ (Pages + DNS blocked on merge) | ☐ |
| PR2 — truesight_me_beta manifest + program page | [truesight_me_beta#293](https://github.com/TrueSightDAO/truesight_me_beta/pull/293) | ☑ | ☐ **← needs Gary's merge** | n/a (beta) | ☐ |
| PR3 — recertification + co-sign | not started | — | — | — | blocked on Gary (§5 open decisions) |
| Promote to prod | n/a | n/a | n/a | n/a | **not requested — do not do** |

**Once Gary merges PR1 + PR2:** enable GitHub Pages on `ivy-yoga-club` (source: `main` root), add the Route53
CNAME (`ivy-yoga.truesight.me` → `truesightdao.github.io`, Explorya zone `Z0032474227N6EQ3Z4QU`), then run the
§6 UAT checklist.

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
   fact rather than a time-bound "still active" assertion)? Not yet built (PR3).

---

## 6. UAT phase (human-tested, beta stack, sample data only — before any real cert circulates)

| # | Surface / URL | What to expect | Interaction | Acceptance criterion |
|---|---|---|---|---|
| 1 | `https://ivy-yoga.truesight.me/` | Admin console loads, boots from `config.json`, shows IVY branding (not Butterfly Effect leftovers) | Open the URL in a browser | Page renders with IVY name/colors, no console errors |
| 2 | Same page | Key generation / email registration flow (`create_signature.html` embed) | Click through, register `garyjob@agroverse.shop` (or another sheet-editor email) | Edgar sends a verification email; clicking it binds the pubkey |
| 3 | Same page, after verification | Reload — should resolve to **admin mode** | Reload the page | UI shows "pending rows" queue, not a locked-out state |
| 4 | IVY roster sheet | Add one **sample** row (Bilal already said the sheet "will just have a sample name for now") | Add a test instructor name | Row appears in the admin panel's pending queue within the sheet's normal refresh window |
| 5 | Admin panel | Click "Attest" on the sample row | Single click | `[CREDENTIALING ATTESTATION EVENT]` fires to Edgar; roster row's audit columns back-fill (`pk_hash`, `attestation_tx_id`, `status`, etc.) |
| 6 | `truesight.me/programs/ivy-yoga/credentials/#<pk-hash>` | Public credential page renders within ~60s of attestation | Visit the URL from the back-filled `profile_url` | Page shows the sample instructor's credential, cert PDF downloadable, QR present |
| 7 | Roster sheet → `Audit Trail` tab | New row appended | Check the tab after step 5 | Row shows `processed_at`, `action`, `github_commit_sha` populated |
| 8 | `ivy-yoga.truesight.me` DNS | Resolves correctly, HTTPS valid | `curl -I https://ivy-yoga.truesight.me/` or browser | 200, valid GitHub Pages TLS cert (may take up to ~1h for cert provisioning after CNAME add) |

**Pass criterion for the whole arc:** all 8 rows pass using the sample row only. Do **not** attest a real instructor
until Gary has resolved the two open decisions in §5 and Shahbaz has handed off the real cert template (§1.7).

---

## 7. References

- `credentials/CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` — playbook this plan instantiates
- `credentials/CREDENTIALING_PLATFORM.md` — data model, deferred co-sign/lineage design
- [`butterfly-effect-club`](https://github.com/TrueSightDAO/butterfly-effect-club) — reference implementation
- [`program-template`](https://github.com/TrueSightDAO/program-template) — fork source
- `truesight_me/programs/butterfly-effect/manifest.json` — real manifest schema this plan's PR2 copies
