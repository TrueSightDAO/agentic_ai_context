# Program Partner Onboarding — route decision guide

**Read this first** when onboarding a new program partner (a school, cohort, studio, community —
e.g. ERA Professionals / Butterfly Effect Club, Tribo Bahia Mirim capoeira). It tells you **which of
three routes** to take and the exact procedure + scripts for each. Pick the route by what the partner
actually needs; don't over-build (a credential-only program does **not** need a ledger).

---

## Decision tree

```
Does each member get a verifiable CREDENTIAL / certificate?
│
├─ NO ─────────────────────────────────────────────────────────► Route C (Donation transparency only)
│                                                                  e.g. Tribo Bahia Mirim capoeira
│
└─ YES → it's a credentialing program (use the credentialing platform)
         │
         Does each ATTESTED member also get a TREE (a serialized tree-planting pledge)?
         │
         ├─ NO  ──► Route A (Credential-only)        — NO ledger, NO currency, NO trees
         │           e.g. "Butterfly Effect without trees"
         │
         └─ YES ──► Route B (Credential + trees)      — NEEDS a new managed ledger + currency
                     e.g. "Butterfly Effect with trees" (BEC)
```

A program can also combine Route C (a donation ledger) with A/B. Routes are additive layers, not
mutually exclusive — but **only add the layer the partner needs.**

| Route | Credential pages? | Managed ledger? | Per-member trees? | Reference partner |
|-------|:----------------:|:---------------:|:-----------------:|-------------------|
| **A — Credential-only** | ✅ | ❌ | ❌ | Butterfly Effect (no-trees mode) |
| **B — Credential + trees** | ✅ | ✅ (new, BEC-style) | ✅ | Butterfly Effect Club → `BEC` |
| **C — Donation transparency** | optional | ✅ (donation ledger) | ❌ | Tribo Bahia Mirim → `TBM` |

---

## Route A — Credential-only (no ledger, no trees)

Members get a digital signature, a public credential page, and a certificate PDF. Nothing financial.

1. **Stand up the program** in the credentialing platform — program `config.json` (in a program repo,
   e.g. `butterfly_effects_club/`), a public `truesight.me/programs/<slug>/manifest.json`, and a
   roster sheet (`Cohort Roster` tab). See **`CREDENTIALING_PLATFORM.md`** and
   **`CREDENTIALING_PROGRAM_PAGES.md`** (URL pattern, manifest schema, co-branding, consent).
2. **Roster → identities + attestations.** The program repo's **`scripts/sync_cohort.py`** reads the
   roster, mints a participant keypair per member, signs `[ATTESTATION EVENT]`s to Edgar/dao_protocol,
   commits to **`lineage-credentials`**, and writes the roster audit columns (`pk_hash`,
   `attestation_tx_id`, `profile_url`, `status`, …). Schema: that repo's `SCHEMA.md`.
3. **Credential pages + certs.** **`lineage-engine/scripts/build_cv_cache.py`** renders each member's
   public page at `truesight.me/programs/<slug>/credentials/#<pk_hash>` + PDF/cert
   (`cert_overlay.py`). See **`CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md`**.

**That's it for Route A.** No `Currencies` row, no managed ledger, no QR mint.

---

## Route B — Credential + trees (needs a new managed ledger)

Everything in Route A, **plus** one serialized tree-planting pledge QR per attested member, booked to a
**dedicated managed ledger**. Canonical instance: **ERA Butterfly Effect Club → `BEC`** ledger
(plan of record: **`ERA_COHORT_TREE_ISSUANCE_PLAN.md`**). The mechanism is the reusable
"attestation → tree planting" template.

**Binding convention (the heart of it):** for each member,
- the tree's **`qr_code` == the member's `pk_hash`**, and
- the tree's **`landing_page` == the member's `profile_url`**

so the Agroverse QR row and the `truesight.me/programs/<slug>/credentials/#<pk_hash>` page point at
each other. QR id == pk_hash also gives free idempotency (the mint flow rejects duplicate ids).

### B.1 — One-time SETUP (per program)

1. **Managed ledger** (codename, e.g. `BEC`). Copy the **AGL MANAGED LEDGER TEMPLATE**
   (`1WoGS2_IPFmwM8VI0G-nU9mJ05wwwacDn7QypJKYnxq4`) → "`<CODE> — <Program>`"; **a human must own it**
   (service accounts have no Drive quota — SA copy fails). Share Editor with
   `tokenomics-schema@…` + `agroverse-qr-code-manager@…`. Register a row on `Shipment Ledger Listing`
   (gid 483234653): `Ledger ID=<CODE>`, `Status=SALES IN PROGRESS`, `Transaction Type=Merchant Green
   Pledge`, `Ledger URL=truesight.me/sunmint/<code>`, `Resolved URL=<sheet>`, **`Program=sunmint`**.
   Bootstrap `treasury-cache/managed-ledgers/<CODE>.json` (or run
   `tokenomics/python_scripts/tdg_asset_management/snapshot_managed_ledgers.py --ledger <CODE>`).
   Full recipe: **`MANAGED_LEDGER_EXPLORER_PATTERN.md`**.
2. **Currency row.** Add a dedicated `Currencies` row **`<Program> Tree Planting Pledge - QR Code`**
   (col C `TRUE`, col E default landing_page, **col F `ledger` = `truesight.me/sunmint/<code>`**,
   col G farm/origin = the program name). Full-width A→Z re-sort after (range-protected — use the
   `tokenomics-schema` SA). One currency + one ledger **per program** (NovaGaia/SEF1 shape).
3. **Allowlist + deploy.** Add the exact currency string to `DONATION_MINT_ALLOWED_CURRENCIES` in
   `tokenomics/google_app_scripts/agroverse_qr_codes/process_donation_mint_telegram_logs.gs`, then
   deploy with the **manifest-driven deployer** (the post-2026-05 clasp refactor — do **not** hand-edit
   the mirror): `tokenomics/scripts/deploy_gas_project.py <scriptId> --push [--with-hooks]`. It syncs
   the tracked source → mirror, strips stale files, and `clasp push --force`. It **refuses to push** on
   uncommitted source changes or a **clasp-identity mismatch** — this scriptId's `owner_email` is
   **`admin@truesight.me`** (per `google_app_scripts/agroverse_qr_codes/manifest.json`), so
   `clasp logout && clasp login` as admin@truesight.me first (or `CLASPRC_PATH=~/.clasprc-admin.json`).
   `--list` shows all deployable scriptIds; full doc: `tokenomics/docs/gas_deploy_workflow.md`.
   (The handler already derives non-AGL Ledger Names like `BEC` and honors a per-row `landing_page`.)

### B.2 — Ongoing minting (scheduled, mint-only)

- **Engine:** `dao_protocol` (the renamed `dao_client` repo) module
  **`truesight_dao_client.modules.link_attestations_to_trees`** — program-parameterized, idempotent,
  `--dry-run` default. For each attested roster row lacking `tree_qr_code`, it calls **`mint_donation`**
  (`[DONATION MINT EVENT]`, signed by a **governor**) with `--qr-code <pk_hash> --landing-page
  <profile_url> --currency "<Program> Tree Planting Pledge - QR Code" --donation-amount <price>` and a
  shared cohort `--proof-file`. The QR lands **`MINTED`**.
- **Config + schedule live in the PROGRAM repo** (not dao_protocol): a manifest
  (`dao_protocol/examples/attestation-trees/<slug>.yaml` — see `butterfly-effect.yaml`) and a cron
  GitHub Action (e.g. `butterfly_effects_club/.github/workflows/mint_cohort_trees.yml`) that
  `pip install`s dao_protocol and runs the module `--execute`. First run backfills the existing cohort;
  later runs pick up new attestations automatically (idempotent on `tree_qr_code`).
- **Why donation-mint, not a new event:** it already does custom-id + dedup + `MINTED` + Edgar/
  dao_protocol dispatch (`server/dispatch.py`); reuse beats rebuild. The "donation" label is internal —
  the currency, ledger, and credential landing page carry the program identity.

### B.3 — Roster annotation (answers "how do we mark a tree is associated?")

**Not automatic at attestation.** `sync_cohort.py` only writes the credential columns. The **mint
orchestrator** (`link_attestations_to_trees`) writes the tree columns **after** it mints:

| Roster col | Header | Written by | Value |
|-----------|--------|-----------|-------|
| (past P) | `tree_qr_code` | `link_attestations_to_trees` | the QR id (== `pk_hash`); presence = tree issued → **idempotency marker** |
| (past P) | `tree_issued_at` | same | ISO 8601 UTC |

It also appends a `tree_issued` row to the program's `Audit Trail` tab. Document the two new columns in
the program repo's `SCHEMA.md`. These columns are disjoint from `sync_cohort.py`'s columns (it owns
A–P), so the two scripts never clobber each other.

### B.4 — Asset balance on the managed ledger (how trees show up + tally)

The managed-ledger sheet (SEF1-style Balance tab, right section `Asset Name | Amount`) is a **rollup of
its own `Transactions` tab** by `Currency` where `Transaction Type = Assets`. Model: **create N assets →
sell M via QR → (N−M) remain**.

- **⚠ The mint does NOT create the managed-ledger asset balance — it only creates the QR-code entry**
  (on the `Agroverse QR codes` tab) plus a `+1` audit row on the **Main** `offchain transactions` ledger.
  So for now you **manually seed** the program ledger's asset inventory: one `Transactions` row on the
  managed-ledger sheet — `Entity = <holder>`, `Amount = N`, `Currency = <program pledge>`,
  `Type = Assets`. (BEC: seeded `97`, `Entity = Gary Teh` — the holder.)
- **Holder + proceeds = the operator, not the program.** The QR `Manager Name` (col U) is set to the
  **governor who signs** the mint (e.g. Gary Teh), so holdings default to them; sales use
  `report_sales --sold-by "<holder>" --cash-proceeds-collected-by "<holder>"` so **proceeds transfer to
  the holder**. (Use the program name only for provenance — `farm name` col E — not as the holder.)
- **Sale is manual + decrements the asset.** Trees stay `MINTED`; the operator marks `SOLD`
  (`report_sales --attachment <payment proof>`). Each sale routes a `-1 Assets` row to the program
  ledger (via col V `Ledger Name`), so N seeded − M sold = remaining. (Auto-sell is possible but not the
  default.)
- **🔮 Future enhancement (Gary 2026-06-02):** the **mint should also create the managed-ledger asset
  balance** (a `+1 Assets` row on the program ledger per QR), so created/sold tally automatically with
  no manual seed. Until then, seed manually and don't double-count (if minting starts creating the
  balance, drop the manual seed). Tracked in `ERA_COHORT_TREE_ISSUANCE_PLAN.md`.
- **Serialized page.** Run `lineage-assets/scripts/seed_from_sheet.py --execute` then `build_index.py`
  and push — the trees appear at **`truesight.me/physical-assets/serialized/`** automatically
  (`infer_asset_type` maps any currency containing "tree" → `tree`; no allowlist change). See
  **`LINEAGE_ASSETS.md`**.

### B.5 — Tree badge on the public credential page (answers "how to indicate on the profile?")

Extend **`lineage-engine/scripts/build_cv_cache.py`** to render a "🌳 Tree planted" badge on the
member's credential page. Because `qr_code == pk_hash`, the builder can look the member up
deterministically in **`lineage-assets/qrs_index.json`** (entry where `qr_id == pk_hash`,
`asset_type == "tree"`) and, if present, link to the tree's `scan_target` /
`edgar.truesight.me/agroverse/qr-code-check?qr_code=<pk_hash>`. **No extra data plumbing** — it rides
the QR row the mint already created. (Tracked as the credential-badge PR in `ERA_COHORT_TREE_ISSUANCE_PLAN.md`.)

---

## Route C — Donation transparency (managed ledger, no per-member trees)

For programs funded by **donations** with a public audit trail, but no per-member credential trees.
Canonical instance: **Tribo Bahia Mirim capoeira → `TBM`** (explorer at `mirim-bahia.truesight.me`).

1. Create a **managed ledger** + public **explorer page** per **`MANAGED_LEDGER_EXPLORER_PATTERN.md`**
   (template copy → `Shipment Ledger Listing` row, `Program=fundraiser` or `sunmint` → 
   `treasury-cache/managed-ledgers/<CODE>.json` → explorer repo reading the raw JSON + CNAME).
2. Wire the **producer** (Stripe/Pix reconciler or `snapshot_managed_ledgers.py`) to publish the JSON.
3. Cross-currency (USD↔BRL for Pix) uses the DApp **`currency_conversion.html`** →
   `[CURRENCY CONVERSION EVENT]` flow (see `PROJECT_INDEX.md` dapp row).

No `Currencies` pledge row, no QR mint, no attestation→tree linking.

---

## Where each piece lives (quick map)

| Concern | Repo / file |
|---------|-------------|
| Credentialing platform + program pages | `CREDENTIALING_PLATFORM.md`, `CREDENTIALING_PROGRAM_PAGES.md`; program repo `config.json` + `sync_cohort.py`; `lineage-engine`, `lineage-credentials` |
| Mint engine (generic, reusable) | `dao_protocol` → `truesight_dao_client/modules/link_attestations_to_trees.py` + `mint_donation.py` |
| Per-program mint config + schedule | the **program repo** (manifest + cron) |
| Tree-mint server flow (signed event) | `tokenomics/google_app_scripts/agroverse_qr_codes/process_donation_mint_telegram_logs.gs`; dispatch in `dao_protocol/.../server/dispatch.py` |
| Managed ledger + treasury cache | `MANAGED_LEDGER_EXPLORER_PATTERN.md`; `treasury-cache`; `snapshot_managed_ledgers.py` |
| Serialized-QR public listing | `lineage-assets` (`seed_from_sheet.py` + `build_index.py`); `LINEAGE_ASSETS.md` |
| BEC plan of record (worked example of Route B) | `ERA_COHORT_TREE_ISSUANCE_PLAN.md` |
