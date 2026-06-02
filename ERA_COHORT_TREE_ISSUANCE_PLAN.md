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
| 0.1 | Event model | **Product QR-code, like SEF / NovaGaia / Prism — NOT a `[DONATION MINT EVENT]`.** Mint as a product, sell via `report_sales` ($1). |
| 0.2 | Currency | NEW dedicated currency **`Butterfly Effect Club Tree Planting Pledge - QR Code`** (parallels `NovaGaia Tree Planting Pledge - QR Code`). |
| 0.3 | Ledger | NEW managed ledger **`BEC`** (col V `Ledger Name`), peer of `SEF1` / `PP1` — **not** AGL/SunMint default. Program = **`sunmint`**. |
| 0.4 | Price / count | Flat **$1 per attested member**; total = N × $1. |
| 0.5 | Per-tree → student binding | **`qr_code == pk_hash`** (F1-a). The QR id IS the student's `pk_hash`, shared with the credential page. → **Requires extending the product QR-generation flow to accept explicit ids (PR1).** |
| 0.6 | Origin identity (farm/manager) | **"ERA Butterfly Effect Club"** — not a physical farm. Use as `farm name` (col E) and `Manager Name` (col U). |
| 0.7 | Reusable template | BEC is the **first instance of a general "attestation → tree planting" template**. Build the orchestrator program-parameterized and ship a generalized pattern doc for future programs. §8. |

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
| **PR1** | Extend product QR-generation (GAS `qr_code_web_service.gs`/generation handler + `dao_client batch_qr_generator`) to accept **per-item `qr_code` (=pk_hash) AND per-item `landing_page` (=profile_url)** instead of the static-from-Currency landing_page. (Other cols — ledger/currency/farm/manager — still from Currency/manifest.) Clasp deploy. | tokenomics / dao_client |
| **PR2** | **`link_attestations_to_trees.py`** orchestrator — **program-parameterized** (manifest: program slug, roster sheet id + SA creds, attested-filter, currency, ledger codename, origin identity, price, binding=`pk_hash`), modeled on `onboard_retail_partner.py`. For the program: read roster → generate/ensure QR rows (id = pk_hash, landing_page = profile_url) → `report_sales --sales-price <price>` → **write roster annotation** (new col `tree_qr_code` + `tree_issued_at`, append `Audit Trail` `tree_issued` row — §9). `--dry-run` default; idempotent (skip rows whose `tree_qr_code` is already set / QR already SOLD); logs rows skipped for missing pk_hash. BEC ships as the first manifest (`examples/attestation-trees/butterfly-effect.yaml`). | `dao_client` |
| **PR3** | **Generalized pattern doc** `CREDENTIAL_ATTESTATION_TREE_LINKING.md` (peer of `MANAGED_LEDGER_EXPLORER_PATTERN.md`) — reusable template (§8/§9) + cross-refs (`OPERATING_INSTRUCTIONS.md` §2 / `WORKSPACE_CONTEXT.md` / `PROJECT_INDEX.md` / `CREDENTIALING_PLATFORM.md`) + `butterfly_effects_club/SCHEMA.md` (document the new roster cols) + `CONTEXT_UPDATES.md`. | `agentic_ai_context` / butterfly_effects_club |
| **RUN** | `--dry-run` → `--execute` 95 → verify sample via `lookup_qr_code` → confirm 95 SOLD on BEC = $95 (run `snapshot_managed_ledgers.py --ledger BEC`) → **surface on serialized page**: `lineage-assets/scripts/seed_from_sheet.py --execute` then `build_index.py`, commit/push `lineage-assets` (§10). Re-run for the 2 on attestation. | — |

---

## 6. Resume tracker

> **RESUME HERE → PR1 (extend product QR-generation for per-item `qr_code` + `landing_page`).** SETUP
> is done; minting can't run until PR1 lands.

| Unit | Built | Merged | Contribution reported |
|------|:----:|:------:|:---------------------:|
| PR0 (roadmap) | ☑ | ☑ (#260) | ☐ |
| Pre-flight 4.1–4.8 | ☑ | — | — |
| SETUP (BEC ledger + currency) | ☑ | ☑ | ☐ |
| PR1 (per-item id + landing_page) | ☐ | ☐ | ☐ |
| PR2 (`link_attestations_to_trees.py`) | ☐ | ☐ | ☐ |
| PR3 (docs) | ☐ | ☐ | ☐ |
| RUN (95 now / 2 later) | ☐ | — | ☐ |

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

## 7. Open questions for ERA / Gary

- **Fork F1** (§3): id == pk_hash (extend product flow) vs SEF-style serial + student ref field?
- **Farm/geography** for BEC trees (4.6) and **Manager name** (4.7)?
- BEC `landing_page` / `ledger` URL slugs (mirror `…/sunmint-tree-planting-pledges/sef1` →
  `…/butterfly-effect`?), and is a public BEC explorer page wanted now or later?
- The 2 pending members — auto-issue once `pk_hash` appears, or hand back to ERA to nudge attestation?
- Physical planting `[TREE PLANTING EVENT]` (geo/species/photo) — who/when, decoupled from issuance.
