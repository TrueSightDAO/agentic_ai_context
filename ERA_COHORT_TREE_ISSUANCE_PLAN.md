# ERA / Butterfly Effect Cohort → Tree Issuance on BEC Ledger — Execution Roadmap

**Status:** Pre-flight. Design pivoted to the **product / SEF model** (not donation). Updated 2026-06-02.
**Owner:** Gary Teh. **Partner:** ERA Professionals — Butterfly Effect Club (lead: Bilal).
**Goal:** Issue **one tree per attested cohort member**, modeled as a **product** (QR-coded tree-planting
pledge SKU) **exactly like NovaGaia / Sacred Earth Farms (`SEF1`) and Prism Percussions (`PP1`)** — a
**dedicated currency** + a **dedicated managed ledger codenamed `BEC`**, sold at **$1** each. ERA has
transferred **USD $97**.

**Bigger picture (Gary 2026-06-02):** BEC is the **reference implementation of a reusable
"attestation → tree planting" template** — *any* credentialing program (Tribo Bahia Mirim, future
cohorts) that wants to link its attested members to planted trees follows this same pattern. So the
generic mechanism (custom-id product QR keyed to a credential `pk_hash` + a per-program currency/ledger)
and a generalized pattern doc are first-class deliverables, not BEC-specific glue. See §8.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. Update the resume tracker as units land; report the
> DAO contribution after each merge.

---

## 0. Decisions (Gary, 2026-06-02)

| # | Decision | Choice |
|---|----------|--------|
| 0.1 | Event model | **Output is a product QR (like SEF/NovaGaia/Prism); mint TRANSPORT = the existing `[DONATION MINT EVENT]`** (final, 2026-06-02). Earlier explored a new `[SERIALIZED QR MINT EVENT]`, but the donation-mint flow already does custom-id + dedup + MINTED + Edgar/dao_protocol dispatch (`dispatch.py:44`) — reuse beats rebuild. The "donation" label is internal; currency/ledger/landing carry the product identity. Easy future rename if desired. |
| 0.1b | Codebase | Intake + dispatch live in **dao_protocol** (renamed `dao_client` repo; server under `truesight_dao_client/server/`), live on `:8010` since the 2026-05-26 NELANCO cutover — **not** Rails `sentiment_importer`. `[DONATION MINT EVENT]` dispatch already wired → **no server change**. |
| 0.2 | Currency | NEW dedicated currency **`Butterfly Effect Club Tree Planting Pledge - QR Code`** (parallels `NovaGaia Tree Planting Pledge - QR Code`). |
| 0.3 | Ledger | NEW managed ledger **`BEC`** (col V `Ledger Name`), peer of `SEF1` / `PP1` — **not** AGL/SunMint default. Program = **`sunmint`**. |
| 0.4 | Price / count | Flat **$1 per attested member**; total = N × $1. |
| 0.5 | Per-tree → student binding | **`qr_code == pk_hash`** (F1-a). The QR id IS the student's `pk_hash`, shared with the credential page. → **Requires extending the product QR-generation flow to accept explicit ids (PR1).** |
| 0.6 | Origin identity (farm/manager) | **"ERA Butterfly Effect Club"** — not a physical farm. Use as `farm name` (col E) and `Manager Name` (col U). |
| 0.7 | Reusable template | BEC is the **first instance of a general "attestation → tree planting" template**. Build the orchestrator program-parameterized and ship a generalized pattern doc for future programs. §8. |
| 0.8 | Trigger model | **Attestation-driven via a scheduled, idempotent orchestrator** (cron GitHub Action), NOT a one-time batch. Each run mints trees for newly-attested rows lacking `tree_qr_code`; first run backfills the current 95; the 2 pending get picked up automatically when they attest. §11. |
| 0.9 | Sale step | **Mint-only — orchestrator leaves trees `MINTED`; Gary marks `SOLD` manually** (`update_qr_code`/`report_sales`). The $1 is prepaid by ERA; booking to BEC happens at Gary's manual sale. |

---

## 1. Reference model — the SEF rows Gary cited (`20250716_SEF_1/2/3`)

Live rows on `Agroverse QR codes` to mirror for BEC:

| Col | SEF value | BEC value |
|-----|-----------|-----------|
| A `qr_code` | `20250716_SEF_1` (date_NAME_serial) | **F1-dependent** — `pk-<hash>` *or* `YYYYMMDD_BEC_<n>` |
| B `landing_page` | `truesight.me/sunmint-tree-planting-pledges/sef1` (static, from Currency) | **PER-ROW = the student's `profile_url`** (Roster col I), e.g. `https://truesight.me/programs/butterfly-effect/credentials/#pk-<hash>`. **Not** static-from-Currency — scanning the tree resolves to the owner's credential page. |
| C `ledger` | `truesight.me/sunmint/sef1` | `truesight.me/sunmint/bec` (TBD) |
| D `status` | `SOLD` | `MINTED` → `SOLD` after `report_sales` |
| E/F/G/H farm/state/country/year | Sacred Earth Farms / Oregon / USA / 2025 | **which farm hosts these trees? (TBD)** |
| I `Currency` | `NovaGaia Tree Planting Pledge - QR Code` | `Butterfly Effect Club Tree Planting Pledge - QR Code` |
| S `Product Image` / T `Price` | (image) / `5` | (image TBD) / `1` |
| U `Manager Name` | Sacred Earth Farms | ERA / Butterfly Effect Club (TBD exact contributor name) |
| V `Ledger Name` | **`SEF1`** | **`BEC`** |

**Key takeaways:** (a) the **product** flow already supports **non-AGL ledger codenames** (`SEF1`, `PP1`)
— so the donation-path `agl\d+`-only regex constraint is moot here. (b) SEF QR ids are **serial**
(`…_SEF_1`), **not** owner identities — the tree binds to a buyer at sale time, not at mint.

---

## 2. Roster reality (read 2026-06-02 via `butterfly_effects_club/google_credentials.json`)

Sheet `1pApVCRqsDw9AjPUTc3fMUfMh-8H4Ne1HYuQ_d6xItog`, tab `Cohort Roster`:

- **97 rows; 95 attested**; **only 95 have a `pk_hash`** — missing on **Hajira Sajjid (row 49)** and
  **Harram Gulfam (row 55)** (the 2 unattested). → **Issue 95 now, 2 once they attest.**
- Cols: `Name, School, Learner Type, Graduation Date, public_key, pk_hash, attestation_tx_id,
  qualification_tx_id, profile_url, …`. **No email anywhere.** 84 Students + 13 Teachers; Narowal 46 /
  IMSG Islamabad 32 / CMS Karachi 19. pk_hashes unique, ≤15 chars.

---

## 3. Fork F1 — RESOLVED (Gary 2026-06-02): `qr_code == pk_hash`, extend the product flow

The QR id IS the student's `pk_hash` (one shared key across the QR row and the credential page
`…/credentials/#pk-…`; deterministic + idempotent). Because the product generation flow
(`BATCH QR CODE REQUEST` → Currency+Quantity+Manager) **auto-assigns serial ids with no custom-id
input**, this requires **PR1: extend the product QR-generation flow (GAS + `batch_qr_generator`) to
accept an explicit id list** (the 95 pk_hashes). This is the affirmative answer to the original
"do we need to extend dao_client?" — **yes**, plus a matching GAS change.

---

## 4. Pre-flight checklist

- [x] **4.1 Roster access / schema / counts** — §2. 95 issuable now, 2 blocked on pk_hash.
- [x] **4.2 Reference model captured** — §1 (SEF1 / PP1 are non-AGL product ledgers).
- [x] **4.3 Fork F1 RESOLVED** — `qr_code == pk_hash`; extend product flow (PR1). §3.
- [ ] **4.4 BEC ledger created** — copy "AGL MANAGED LEDGER TEMPLATE"
      `1WoGS2_IPFmwM8VI0G-nU9mJ05wwwacDn7QypJKYnxq4` → "BEC — Butterfly Effect Club"; register on
      `Shipment Ledger Listing` (gid 483234653): A `BEC`, C `ACTIVE`, D desc, H Transaction Type
      (`Merchant Green Pledge` for sunmint), L Ledger URL, AB Resolved URL, **AC `sunmint`**; SA
      `tokenomics-schema@…` bypasses col-AC protection. `treasury-cache/managed-ledgers/BEC.json`.
- [ ] **4.5 Currency row** — add `Butterfly Effect Club Tree Planting Pledge - QR Code` to `Currencies`
      (C `TRUE`, E landing_page, F `ledger` URL, farm cols); full-width A→Z sort (range-protected).
- [x] **4.6 Origin identity** — `farm name` (col E) = **"ERA Butterfly Effect Club"** (not a physical
      farm); state/country/year left blank unless Gary says otherwise.
- [x] **4.7 Manager name** — col U = **"ERA Butterfly Effect Club"**. (If it must match a
      `Contributors`/`Contributors Digital Signatures` entry for downstream lookups, confirm/create that
      contributor row — verify during SETUP.)
- [ ] **4.8 Signer + proof + sales attribution** — governor signer (Gary Teh); proof = ERA $97 receipt;
      `--sold-by`/`--cash-proceeds-collected-by` = Gary Teh; `--stripe-session-id "(none)"`, shipping/tracking `N/A`.

---

## 5. Sequenced plan

| Unit | Scope | Repo |
|------|-------|------|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **SETUP** ✅ DONE 2026-06-02 | BEC ledger sheet `19CDo-Pdu6tClb_dux42IkFzGwNT_sGvEYIKmLnmp3aY` (Gary-owned, shared to schema + qr-manager SAs) · `Currencies` row 24 (`Butterfly Effect Club Tree Planting Pledge - QR Code`, B=1, F=`truesight.me/sunmint/bec`, farm=`ERA Butterfly Effect Club`) · `Shipment Ledger Listing` row 19 (`BEC`, SALES IN PROGRESS, Merchant Green Pledge, Trees=95, Program=sunmint) · `treasury-cache/managed-ledgers/BEC.json` published (commit `b031169`). Leftovers: `Transactions!B1` contract URL (stale tribomirimbahia link); `truesight.me/sunmint/bec` redirect (verify). | sheets / treasury-cache / tokenomics |
| **PR1** ✅ MERGED 2026-06-02 | Reuse `[DONATION MINT EVENT]`: **GAS** (`process_donation_mint_telegram_logs.gs`, tokenomics #329) — allowlist += BEC currency; `ledgerNameFromCurrencies_` generalized (non-AGL slugs → `BEC`); per-row `landing_page` (col B) override. **CLI** (`mint_donation.py`, dao_protocol #57) — `--donor-email` optional + `--landing-page`. Backward-compatible. **⚠ Held: clasp deploy** (sync mirror `1MnAsIQAxcSfZO_…` + bump `Version.gs` + `clasp push`/`deploy`). | tokenomics / dao_protocol |
| **PR2** | **`link_attestations_to_trees.py`** orchestrator — **program-parameterized** (manifest: program slug, roster sheet id + SA creds, attested-filter, currency, ledger codename, origin identity, binding=`pk_hash`), modeled on `onboard_retail_partner.py`. **MINT-ONLY** (no sale): read roster → for each attested row lacking `tree_qr_code`, call **`mint_donation`** (`--qr-code <pk_hash> --landing-page <profile_url> --currency "Butterfly Effect Club Tree Planting Pledge - QR Code" --donor-name <Name> --donation-amount 1`, shared cohort `--proof-file`, signed as a governor) → QR lands `MINTED` → **write roster annotation** (`tree_qr_code` + `tree_issued_at`, append `Audit Trail` `tree_issued` row — §9). `--dry-run` default; idempotent (skip rows whose `tree_qr_code` is set); logs rows skipped for missing pk_hash. BEC ships as the first manifest (`examples/attestation-trees/butterfly-effect.yaml`). | `dao_client` |
| **PR2b** | **Scheduled trigger (lives in the PROGRAM repo, not dao_client)** — `butterfly_effects_club/.github/workflows/mint_cohort_trees.yml` (cron, ~hourly), next to `sync_cohort.py`. `pip install`s dao_client and runs PR2 `--execute` with `manifests/butterfly-effect.yaml`. Idempotent on `tree_qr_code`. Secrets (already pattern-matched to that repo): roster SA creds + signer key. Future programs add their own manifest + cron; the dao_client engine is reused unchanged. §12. | butterfly_effects_club |
| **PR3** | **Generalized pattern doc** `CREDENTIAL_ATTESTATION_TREE_LINKING.md` (peer of `MANAGED_LEDGER_EXPLORER_PATTERN.md`) — reusable template (§8/§9) + cross-refs (`OPERATING_INSTRUCTIONS.md` §2 / `WORKSPACE_CONTEXT.md` / `PROJECT_INDEX.md` / `CREDENTIALING_PLATFORM.md`) + `butterfly_effects_club/SCHEMA.md` (document the new roster cols) + `CONTEXT_UPDATES.md`. | `agentic_ai_context` / butterfly_effects_club |
| **RUN** | First run: `--dry-run` → `--execute` → **mint 95 (`MINTED`)** + annotate roster → verify sample via `lookup_qr_code`. **Gary marks SOLD** (manual) → `snapshot_managed_ledgers.py --ledger BEC` to confirm BEC totals. **Surface on serialized page**: `lineage-assets/scripts/seed_from_sheet.py --execute` then `build_index.py`, commit/push `lineage-assets` (§10). After PR2b, the 2 pending + all future attestations are handled automatically. | — |

---

## 6. Resume tracker

> **✅ DONE (2026-06-02): 95 trees minted + sold end-to-end.** Full battle-tested runbook + gotchas are in
> **`PROGRAM_PARTNER_ONBOARDING.md` §B.6** (the canonical reusable guide — read that for future programs).
> Shipped: BEC ledger + currency + registration + treasury JSON; donation-mint GAS (BEC support, dynamic
> currency validation, per-row landing_page, **mint→managed-ledger**) deployed; webhook repointed off the
> deprecated `1slQVojn` script to `1MnAsIQA`; 95 minted (`qr_code=pk_hash`, holder=Gary) + 95 sold ($1,
> proceeds=Gary); $2 capital injection processed (Asset+Equity); `/sunmint/bec` redirect; serialized
> listing refreshed; `/qr/` farm-link fix; `sunmint.html` BEC card. Sales→ledger self-heals hourly.
>
> **REMAINING → PR4 (credential-page tree badge + qr link).** `lineage-engine/build_cv_cache.py` looks up
> `qr_id==pk_hash` in `qrs_index.json` → adds a `tree` field → credential front-end (shared
> `TrueSightProgramShell`) renders a "🌳 tree planted" badge linking to `truesight.me/qr/?id=<pk_hash>`;
> rebuild CVs. Spec in `PROGRAM_PARTNER_ONBOARDING.md` §B.6 item 6. Plus trivial: add
> `truesight_me/assets/shipments/bec.avif` (sunmint card image). The 2 unattested (Hajira, Harram) get
> trees automatically when they attest + the orchestrator re-runs.
>
> **Execution model (Gary 2026-06-02):** create **97** assets on the BEC ledger (✅ seeded `97`,
> `Entity=Gary Teh`) → **sell 95** via QR `[SALES EVENT]` (`--attachment ~/Applications/tmp/era_payment.jpeg`,
> `--sold-by/--cash-proceeds-collected-by "Gary Teh"`) → 2 remain. **Holder + proceeds = Gary Teh.**
> The mint creates **only the QR entry** today (asset balance seeded manually); **🔮 future: make the mint
> create the managed-ledger asset balance** so it tallies without a manual seed (don't double-count —
> drop the seed when that lands). Deploy path uses the **refactored manifest-driven
> `deploy_gas_project.py`** (no hand-editing mirrors).

| Unit | Built | Merged | Contribution reported |
|------|:----:|:------:|:---------------------:|
| PR0 (roadmap) | ☑ | ☑ (#260) | ☐ |
| Pre-flight 4.1–4.8 | ☑ | — | — |
| SETUP (BEC ledger + currency) | ☑ | ☑ | ☐ |
| PR1 (donation-mint GAS + CLI deltas) | ☑ | ☑ (tok #329, dao_protocol #57) | ☐ |
| ↳ clasp deploy of GAS | ☐ | — | — |
| PR2 (`link_attestations_to_trees.py` + BEC manifest) | ☑ | ☑ (dao_protocol #58) | ☐ |
| PR2b (cron + manifest in butterfly_effects_club) | ☐ | ☐ | ☐ |
| PR3 (onboarding/route docs) | ☑ `PROGRAM_PARTNER_ONBOARDING.md` | ☐ | ☐ |
| PR4 (tree badge on credential page — `build_cv_cache.py`) | ☐ | ☐ | ☐ |
| RUN (mint 95; Gary marks SOLD; surface) | ☐ | — | ☐ |

---

## 8b. Route decision (where this fits)

This plan is the worked example of **Route B (Credential + trees)** in the general
**`PROGRAM_PARTNER_ONBOARDING.md`** decision guide. That doc routes any new partner to:
**Route A** credential-only (no ledger), **Route B** credential + trees (new ledger — this plan), or
**Route C** donation transparency (capoeira/TBM). Onboard future partners via that guide.

---

## 8. Reusable template — "attestation → tree planting" for any program

BEC is instance #1. A future credentialing program links its attested members to trees by supplying a
**manifest** + a one-time **SETUP**; no new code per program.

**Per-program manifest (what changes):**

| Field | BEC value | Notes |
|-------|-----------|-------|
| `program_slug` | `butterfly-effect` | Matches the credentialing program; roster lives in its sheet. |
| `roster_sheet_id` + `roster_tab` + `sa_credentials` | `1pApVCRq…` / `Cohort Roster` / `butterfly-effect-club@…` | Read access via the program's SA. |
| `attested_filter` | `status==processed && attestation_tx_id != ''` | Which rows are eligible. |
| `id_source` | `pk_hash` (Roster col F) | QR id (col A) == credential `pk_hash` (the binding convention; skip rows lacking it). |
| `landing_page_source` | `profile_url` (Roster col I) | Per-row QR `landing_page` (col B) = the member's credential page. The second half of the binding. |
| `currency` | `Butterfly Effect Club Tree Planting Pledge - QR Code` | **One dedicated `Currencies` row per program** (NovaGaia shape, not the shared SunMint currency). Convention: **`<Program Name> Tree Planting Pledge - QR Code`**. |
| `ledger_codename` | `BEC` | **One dedicated managed ledger per program** (peer of `SEF1`/`PP1`), Program=`sunmint`. e.g. future Tribo Bahia Mirim → `Tribo Bahia Mirim Tree Planting Pledge - QR Code` → ledger `TBM`. |
| `origin_identity` | `ERA Butterfly Effect Club` | `farm name` (E) + `Manager Name` (U). |
| `price` | `1` | Per-tree sale price. |

**Generic mechanism (build once, reuse):** (1) product QR-generation accepts **explicit ids** (PR1);
(2) `link_attestations_to_trees.py` (PR2) runs the read→mint→sell loop from a manifest, idempotently;
(3) the **two-way binding** for every program: **QR id (col A) == credential `pk_hash`** AND **QR
`landing_page` (col B) == the member's `profile_url`** — so the Agroverse QR row and the
`truesight.me/programs/<slug>/credentials/#<pk_hash>` page point at each other.

**Per-program SETUP (one-time, ~30 min):** create the managed ledger (template copy + Shipment Ledger
Listing row + treasury-cache JSON), add the `Currencies` row, drop a manifest. Documented in
`CREDENTIAL_ATTESTATION_TREE_LINKING.md` (PR3).

**Candidate next programs:** Tribo Bahia Mirim capoeira; future ERA alumni cohorts; any
`CREDENTIALING_PLATFORM.md` program.

---

## 9. Roster annotation — marking that a tree is linked to a certificate

The `Cohort Roster` already has a clean audit-column convention: **A–D ERA-owned** (don't overwrite),
**E–P written by `sync_cohort.py`** (`pk_hash`, `attestation_tx_id`, `profile_url`, `status`, …), plus an
**`Audit Trail`** tab (per-action log). Follow that pattern — the orchestrator (PR2) owns **new columns
past P**, disjoint from `sync_cohort.py`, so no clobber (document in `butterfly_effects_club/SCHEMA.md`):

| New col | Label | Filled when | Value |
|---------|-------|-------------|-------|
| Q | `tree_qr_code` | after the tree's `[SALES EVENT]` lands | the BEC QR id (**== `pk_hash`**). Presence = tree issued → **idempotency marker** (skip set rows on re-run). |
| R | `tree_issued_at` | same | ISO 8601 UTC. |
| (opt) S | `tree_ledger_url` | same | `edgar.truesight.me/agroverse/qr-code-check?qr_code=<pk_hash>` for click-through. |

Also append an **`Audit Trail`** row: `action = tree_issued`, with `name`, `processed_at`, and the QR
id / ledger URL — mirroring the existing `profile_created` / `certificate_issued` actions.

**Template note:** every program's roster gets the same `tree_qr_code` / `tree_issued_at` columns,
written by the orchestrator. `tree_qr_code` is the per-program idempotency key on the roster side.

---

## 10. Surfacing on `truesight.me/physical-assets/serialized/`

The serialized listing reads `lineage-assets/qrs_index.json` ← `build_index.py` aggregates per-QR
manifests `lineage-assets/qrs/<qr_id>.json` ← **`seed_from_sheet.py` reads the whole `Agroverse QR
codes` tab** (no currency/ledger allowlist) and classifies `asset_type` via `infer_asset_type`
(currency containing **"tree"** → `"tree"`). BEC currency contains "Tree", so **BEC QRs auto-classify
as trees and require no config**. To surface them after minting:

```
cd lineage-assets
GOOGLE_APPLICATION_CREDENTIALS=… python3 scripts/seed_from_sheet.py --execute   # writes qrs/<pk_hash>.json
python3 scripts/build_index.py                                                  # regenerates qrs_index.json
git commit -am "chore: seed BEC cohort trees into qrs index" && git push       # GitHub Pages / raw serves it
```

No scheduled workflow exists in `lineage-assets` today → this refresh is part of **RUN** (and a CI cron
is a reasonable follow-up). Each manifest's `current_landing_page` will be the student's `profile_url`
(per the per-row landing_page), and `edgar_resolve_url` = `…/qr-code-check?qr_code=<pk_hash>`.

---

## 12. Where the code lives (engine vs config)

| Piece | Repo | Why |
|-------|------|-----|
| **Generic mint engine** `link_attestations_to_trees.py` + per-item id/landing extension | **dao_client** | Reusable across all programs (decision 0.7). dao_client is the established home for Edgar-event orchestrators. **Do NOT** put generic logic in a program repo — it wouldn't be reusable. |
| GAS per-item id/landing change | **tokenomics** | Server-side product QR-generation flow. |
| **Per-program manifest** (`butterfly-effect.yaml`) + **cron workflow** + new roster columns + SCHEMA update | **butterfly_effects_club** (the program repo) | Program-specific config, secrets, schedule, schema. Sits next to `sync_cohort.py` + its workflow + the roster SA creds. |
| Managed ledger + currency + treasury JSON | sheets / treasury-cache | Per-program data plane (done for BEC). |
| QR surfacing | **lineage-assets** | `seed_from_sheet.py` + `build_index.py` (program-agnostic; reads whole QR tab). |

**Rule for future programs:** new repo (or section) drops a *manifest + cron* and reuses the dao_client
engine + the tokenomics GAS + lineage-assets surfacing unchanged.

---

## 11. Trigger model — attestation → auto-mint (scheduled, mint-only)

The flow is **event-driven, not a one-off batch.** When a program manager attests a student, the
credentialing pipeline writes the roster row (`pk_hash`, `attestation_tx_id`, `profile_url`, `status`).
A **scheduled orchestrator** (PR2 on a cron Action, PR2b) then picks it up:

```
every ~hour:
  for each roster row where status=processed AND pk_hash set AND tree_qr_code empty:
      mint BEC QR (id=pk_hash, landing_page=profile_url, status=MINTED)   # PR1 product flow
      write roster tree_qr_code + tree_issued_at + Audit Trail 'tree_issued'
```

- **Idempotent on `tree_qr_code`** → each run only handles newly-attested students; safe to run forever.
  The **first run backfills the current 95**; the 2 without `pk_hash` are picked up automatically once
  they attest. No separate backfill vs steady-state code path.
- **Mint-only.** Trees land `MINTED`; **Gary marks `SOLD` manually** (decision 0.9). The sale books the
  $1 to the BEC ledger.
- **Loosely coupled** (chosen over minting inside the credentialing GAS): reuses everything we built,
  no cross-workbook writes from the credentialing handler; cost is a minutes-to-hour delay (fine).

**Template:** the scheduled trigger is part of the reusable pattern — each program gets a manifest +
a cron entry; new attestations → trees with zero per-event work.

---

## 7. Open questions for ERA / Gary

- **Fork F1** (§3): id == pk_hash (extend product flow) vs SEF-style serial + student ref field?
- **Farm/geography** for BEC trees (4.6) and **Manager name** (4.7)?
- BEC `landing_page` / `ledger` URL slugs (mirror `…/sunmint-tree-planting-pledges/sef1` →
  `…/butterfly-effect`?), and is a public BEC explorer page wanted now or later?
- The 2 pending members — auto-issue once `pk_hash` appears, or hand back to ERA to nudge attestation?
- Physical planting `[TREE PLANTING EVENT]` (geo/species/photo) — who/when, decoupled from issuance.
