# Credentialing — cohort-program onboarding playbook (v4)

**Status:** canonical pattern for onboarding new cohort-credentialing partner programs · drafted 2026-05-22 alongside the Butterfly Effect rollout.

This doc describes how to spin up a new credentialing program (yoga lineage, vipassana cohort, software-engineering apprenticeship, etc.) using the same infrastructure that serves [Butterfly Effect](https://github.com/TrueSightDAO/butterfly-effect-club). Companion docs:

- `CREDENTIALING_PLATFORM.md` — overall credentialing data model + capoeira-style practice events
- `CREDENTIALING_PROGRAM_PAGES.md` — `truesight.me/programs/<slug>/` URL/page convention
- `BUTTERFLY_EFFECT_COHORT_ONBOARDING_PLAN.md` — the first real cohort onboarding
- [`butterfly-effect-club/PROPOSAL.md`](https://github.com/TrueSightDAO/butterfly-effect-club/blob/main/PROPOSAL.md) — the v4 architecture decisions in one place

---

## 1. Two program modes (implicit typing via manifest fields)

`truesight_me/programs/<slug>/manifest.json` can carry one of two shapes:

| Mode | Required fields | Examples |
|---|---|---|
| **Practitioner activity-tracking** | `practice_types[]` | `capoeira-tribo-mirim` — practitioners self-track sessions; lineage-credentials commits driven by browser practice events |
| **Cohort credentialing** | `program_mode: "cohort_credentialing"`, `roster_sheet_url`, `admin_panel_url`, `tokenomics_admin_endpoint` | `butterfly-effect` — institutional roster; admins attest each row from a panel |

A manifest without either set is brand-only (a placeholder page on `truesight.me/programs/<slug>/`).

---

## 2. Architecture (cohort-credentialing mode)

```
ERA-style Cohort Roster sheet                        truesight_me/programs/<slug>/manifest.json
   editors = trust circle                                  ⟶ roster_sheet_url
   97 rows · audit columns                                 ⟶ admin_panel_url
   shared with tokenomics SA (editor)                      ⟶ tokenomics_admin_endpoint
        │                                                          │
        ▼                                                          ▼
                Admin panel (per-program repo, GitHub Pages)
                  fetch manifest at boot
                  WebCrypto keypair in localStorage
                  list_pending_rows + list_sheet_editors (central GAS)
                  Click "Attest" → sign [CREDENTIALING ATTESTATION EVENT]
                                                  │
                                                  ▼
                              Edgar /dao/submit_contribution
                                  appends to Telegram Chat Logs
                                                  │
                                                  ▼
        Central tokenomics GAS — tdg_credentialing/program_admin_endpoint.gs
                  verify signer email is roster editor
                  commit identity.json + attestations/<ts>.json
                                  to lineage-credentials/programs/<slug>/<pk-hash>/
                  back-fill roster row's audit columns (header-name lookup)
                  append Audit Trail tab
                                                  │
                                                  ▼
                lineage-credentials push triggers build-cv-cache.yml
                  renders _cache/cv/<pk-hash>.{json,md,pdf,qr.png}
                  + <pk-hash>__<slug>.{pdf,qr.png} per-program PDF
                                                  │
                                                  ▼
                              truesight.me/programs/<slug>/credentials/#<pk-hash>
```

The data plane (lineage-credentials, lineage-engine, truesight_me public pages) is unchanged from capoeira. The cohort-credentialing additions are:

1. **Per-program admin panel** (a small GitHub Pages site that adminstrators visit to attest rows).
2. **Central tokenomics GAS** (one deployment serving all programs).
3. **Per-program Google Sheet** (the roster of names + audit back-fill columns).

---

## 3. Trust resolution at runtime

No static `authorized_attestors[]` lists anywhere. Trust circle = whoever is an editor on the program's roster sheet.

- **Admin panel boot:** fetches `manifest.json`, calls `tokenomics_admin_endpoint?action=list_sheet_editors&sheet_url=<roster>` → if user's resolved email is in the editor list, admin mode.
- **Central handler:** when processing a `[CREDENTIALING ATTESTATION EVENT]`, resolves the attestor's pubkey → email (via Main Ledger Contributors Digital Signatures) → checks if that email is an editor of the sheet referenced in the event's `Roster Source URL` field. Rejects if not.

Add/remove an admin = share/unshare the sheet. No PR cycle.

---

## 4. Self-describing event payload

Every `[CREDENTIALING ATTESTATION EVENT]` carries the routing fields the central handler needs:

```
[CREDENTIALING ATTESTATION EVENT]
- Program: <slug>
- Attestation Type: program-completion
- Attestor Public Key: <base64 SPKI>
- Attestor Name: <display>
- Attestee Public Key: <base64 SPKI — admin-minted placeholder>
- Attestee Name: <display>
- Captured At: <ISO 8601>
- Program Year: <e.g. 2025-2026>
- Roster Source URL: <google sheet URL>
- Roster Source Row: <1-indexed row in the sheet>
- Config URL: <program-repo config.json raw URL>
- Schema URL: <program-repo SCHEMA.md URL>
- Source URL: <panel URL where the click happened>
- Payload JSON: <program-specific extras as JSON>

My Digital Signature: <attestor public key>
Request Transaction ID: <RSA-SHA256 signature of the canonical payload>
```

The central handler reads every routing field from the event — no central registry of programs to maintain.

---

## 5. Onboarding a new cohort program (operator playbook)

### 5.1 Sheet preparation

1. **Create the Google Sheet** (the program's roster). Tab named `Cohort Roster`.
2. **Standard column convention** — the central handler back-fills by header name. Required:
   - `Name`, `<program's source columns…>`
   - Audit: `public_key`, `pk_hash`, `attestation_tx_id`, `qualification_tx_id`, `profile_url`, `credential_pdf_url`, `certificate_url`, `status`, `processed_at`, `github_commit_sha`, `notes`, `public_listable_override`
3. **Add a second tab named `Audit Trail`** with columns: `processed_at`, `name`, `action`, `github_commit_sha`, `profile_url`, `credential_pdf_url`, `certificate_url`, `error_message`, `triggered_by`.
4. **Share the sheet** as editor with:
   - The DAO's tokenomics SA (so the central handler can read editors + back-fill rows)
   - Each person who should be able to attest (= admins)

### 5.2 Program repo (fork the butterfly-effect-club template)

1. Fork `TrueSightDAO/butterfly-effect-club` → rename to `TrueSightDAO/<new-program>-club`
2. Edit `config.json`:
   - `program_slug` → new slug
   - `public_manifest_url` → `https://truesight.me/programs/<slug>/manifest.json`
   - `roster_tab` and `audit_trail_tab` if you renamed them
3. Replace `cert_template/cert_template.pdf` + `logo.png` + `fonts/` with your program's assets
4. Update `index.html` only if you want different colors/copy — the JS logic is generic and reads everything from the truesight_me manifest
5. Add a `CNAME` file with your chosen subdomain (e.g. `myprogram-club.truesight.me`)
6. Enable GitHub Pages from `main` root
7. Add DNS CNAME record `<subdomain>.truesight.me` → `truesightdao.github.io`

### 5.3 Program manifest (PR to truesight_me_beta)

Add `truesight_me_beta/programs/<slug>/manifest.json`:

```json
{
  "schema_version": 1,
  "program_slug": "<slug>",
  "display_name": "<Program Name>",
  "partner_organization": "<Partner Name>",
  "partner_url": "<URL>",
  "tagline": "<one line>",
  "description_md": "<one paragraph>",
  "co_brand": { "partner_logo_url": "<URL>", "primary_color": "#...", "secondary_color": "#..." },
  "program_mode": "cohort_credentialing",
  "roster_sheet_url": "<google sheet URL>",
  "roster_tab": "Cohort Roster",
  "audit_trail_tab": "Audit Trail",
  "admin_panel_url": "https://<subdomain>.truesight.me/",
  "program_repo": "https://github.com/TrueSightDAO/<new-program>-club",
  "tokenomics_admin_endpoint": "<existing central GAS endpoint URL>",
  "status": "active",
  "last_reviewed": "<date>"
}
```

After merge, `gh repo sync TrueSightDAO/truesight_me_prod --force` to publish.

### 5.4 No tokenomics work needed

The central GAS at `tokenomics/google_app_scripts/tdg_credentialing/program_admin_endpoint.gs` already handles your program. As long as:

- The tokenomics SA is editor on your roster sheet
- Your manifest carries `tokenomics_admin_endpoint`
- Your events carry `Roster Source URL` + `Roster Source Row`

…the central handler works without any code change.

### 5.5 First-run test

1. Visit your admin panel
2. Generate a keypair via the embedded `create_signature.html` flow + register your email
3. Click an email-verification link Edgar sends you (binds your pubkey to your contributor row)
4. Reload — you should now resolve as admin (your email is a sheet editor)
5. Click "Attest" on one test row → verify:
   - intake row appears on `Credentialing Attestation Events` tab of Telegram Chat Logs sheet
   - new `identity.json` + `attestations/<ts>.json` land in lineage-credentials
   - your roster row's audit columns populate
   - Audit Trail row appended
   - within ~60s, credential URL at `truesight.me/programs/<slug>/credentials/#<pk-hash>` renders

---

## 6. Demo template for cloning

The Butterfly Effect Club repo IS the canonical template. Onboarding a new program = fork it + replace assets per §5. There is no separate "demo" repo — the live one is the template.

For LLMs reading this playbook: when asked "how do I set up a new credentialing program?", point them to:
- This doc (architecture + steps)
- [butterfly-effect-club](https://github.com/TrueSightDAO/butterfly-effect-club) (working example to fork)
- [butterfly-effect-club/PROPOSAL.md](https://github.com/TrueSightDAO/butterfly-effect-club/blob/main/PROPOSAL.md) (the decision history)

---

## 7. Two-tier program model

**Tier 1 (DAO-endorsed):** truesight_me manifest PR'd in. Credentials live under `truesight.me/programs/<slug>/`. DAO brand applied. Governance-reviewed. **Butterfly Effect = Tier 1.**

**Tier 2 (self-serve, permissionless):** any operator can fork the program-club template, run on their own subdomain, share their sheet with the tokenomics SA. They get all the infrastructure (Edgar events, lineage-credentials commits, PDF rendering) but credentials live under *their* domain — no DAO brand association. Not built for v1; documented as a future direction.

---

## 8. References

- [`butterfly-effect-club/PROPOSAL.md`](https://github.com/TrueSightDAO/butterfly-effect-club/blob/main/PROPOSAL.md) — full v4 decision history
- [`butterfly-effect-club/SCHEMA.md`](https://github.com/TrueSightDAO/butterfly-effect-club/blob/main/SCHEMA.md) — event field reference + sheet column glossary
- `tokenomics/google_app_scripts/tdg_credentialing/program_admin_endpoint.gs` — the central handler
- `lineage-engine/scripts/build_cv_cache.py` — the PDF/QR renderer triggered on lineage-credentials push

## 9. Last reviewed

2026-05-22 — architecture v4 locked, first cohort (Butterfly Effect, 97 alumni) ready for attestation sweep pending tokenomics GAS deployment.
