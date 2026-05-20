# Lineage Assets — physical-asset provenance architecture

This doc is the canonical reference for **lineage-assets**: per-QR provenance
manifests for TrueSight DAO physical assets (cacao bags, trees, drums,
memberships, and future supply-chain assets).

Parallel architecture to [`CREDENTIALING_PLATFORM.md`](./CREDENTIALING_PLATFORM.md)
(humans + acts). Same lineage primitive — attested chain — different
population.

---

## Why this exists

Before this refactor (pre-2026-05-20), QR-code data was scattered across two
repos and several scripts:

- `tokenomics/python_scripts/agroverse_qr_code_generator/` — Python QR
  generation
- `tokenomics/google_app_scripts/agroverse_qr_codes/` — GAS web service for
  scan resolution + admin lookups
- `qr_codes/` repo — flat storage of generated PNG images (~731 files,
  no structured metadata)

While `lineage-credentials/` was a clean, designed repo with per-person
manifest files (`programs/<program>/people/<pk-hash>/identity.json`), the
QR-code side had grown organically as a tactical tool — no dedicated repo,
no schema doc, no first-class data model.

**The architectural insight** (surfaced 2026-05-20 in a strategy
conversation about supply-chain traceability + China's new supply-chain
regulation): a cacao bag's QR is exactly the same primitive as a student's
compassionate-action credential. Both are *attested chains* — a known
actor attesting to a verifiable thing. The credentialing platform treats
humans as first-class through `lineage-credentialing`; this doc establishes
the parallel structure for physical assets through `lineage-assets`.

Promoting QR codes to first-class architecture also unlocks the next
strategic move: cross-jurisdiction supply-chain traceability (per the
WEF / China 2026-04 supply chain regulation tailwind). See
`JURISDICTION_STRATEGY.md` (forthcoming) for the per-jurisdiction GitLab
pattern.

---

## Repo layout

[`TrueSightDAO/lineage-assets`](https://github.com/TrueSightDAO/lineage-assets)
(public; created 2026-05-20):

```
lineage-assets/
├── README.md
├── SCHEMA.md                      # per-QR JSON wrapper + asset-type extensions
├── qrs/                           # one file per QR-coded asset
│   ├── 2024PF_20250505_01.json
│   ├── 2025_20250829_4027ff6b.json
│   ├── …                          # 1457 files at initial seed
│   └── …
└── scripts/
    └── seed_from_sheet.py         # idempotent sync from Agroverse QR codes sheet
```

---

## Per-QR JSON schema

The canonical wrapper (every file) and per-asset-type extensions are
defined in
[`lineage-assets/SCHEMA.md`](https://github.com/TrueSightDAO/lineage-assets/blob/main/SCHEMA.md).

Quick reference:

```jsonc
{
  "qr_id":            "string (matches filename, ID from Agroverse QR codes sheet col A)",
  "asset_type":       "cacao_bag | tree | drum | membership | …",
  "schema_version":   "v0",
  "minted_at":        "ISO 8601 date",
  "minted_by":        "string (contributor name)",
  "status":           "MINTED | CONSIGNMENT | SOLD | RETIRED",
  "current_holder":   { "partner_id": "string", "partner_name": "string" } | null,
  "lineage":          { /* asset-type-specific */ },
  "events":           [ /* append-only history */ ],
  "current_landing_page": "string (the URL Edgar redirects to TODAY — preserved for reference)",
  "qr_image_url":     "raw.github URL into the qr_codes repo",
  "scan_target":      "https://truesight.me/qr/?id=<qr_id>  (the new surface)",
  "edgar_resolve_url": "https://edgar.truesight.me/agroverse/qr-code-check?qr_code=<qr_id>"
}
```

---

## The truesight.me/qr/ rendering surface

[`truesight.me/qr/?id=<qr_id>`](https://truesight.me/qr/) is the
public-facing renderer. Single template page at
`truesight_me_beta/qr/index.html` (also live on prod) that:

1. Reads `?id=<qr_id>` from the URL (or `#<qr_id>` fragment as a fallback)
2. Fetches `https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/qrs/<qr_id>.json`
3. Dispatches on `asset_type` to render the appropriate lineage view
4. Renders QR image, status badge, lineage cells, current-holder block,
   event timeline, footer with Edgar resolve URL

Pure static HTML + vanilla JS. No backend. No build pipeline beyond
GitHub Pages.

Mirrors the existing
[`truesight.me/credentials/#<slug>`](https://truesight.me/credentials/)
pattern exactly — same JSON-driven, static-HTML approach.

---

## Edgar's redirect — current state + future switch

**Current production behaviour (unchanged):**

```
phone scans QR
    → URL embedded in QR: https://edgar.truesight.me/agroverse/qr-code-check?qr_code=<id>
    → Edgar looks up the QR row in Agroverse QR codes sheet
    → Edgar reads column B (landing_page) for that QR
    → Edgar 302-redirects to that URL (currently agroverse.shop product pages, etc.)
```

**The new truesight.me/qr/ surface is currently demo-only.** Direct URLs
like `https://truesight.me/qr/?id=<qr_id>` work and render the provenance
view, but the actual QR scans in the wild still resolve to the existing
landing pages. This is intentional: don't disrupt the existing user
experience while the new surface is being reviewed.

**The step-function switch** (when ready):

1. **Review the new page with Kirsten and operator**, iterate on
   visual design + content depth as needed.
2. **Pick one test QR**. Update its column B value in the Agroverse QR
   codes sheet from current value → `https://truesight.me/qr/?id=<qr_id>`.
   Scan the physical QR. Confirm round-trip.
3. **Scale.** Bulk-update column B for the appropriate cohort (probably
   all active MINTED + CONSIGNMENT, leave SOLD as-is, or apply per-SKU
   rules).
4. **No QR regeneration needed.** Every QR in the wild already points
   at Edgar; only Edgar's redirect target changes.

No Edgar code change is required for the switch — purely a data update on
the Agroverse QR codes sheet. Per-QR override is possible (column B is
per-row), so the switch can be partial / gradual / experimental.

---

## Why JSON-per-QR rather than aggregated

- **Append-only events per asset.** Easy to diff one asset's history
  without pulling a large aggregate file.
- **Independently fetchable** by the truesight.me renderer. No index
  lookup needed — the URL ID maps directly to a file path.
- **Git history per file = audit trail per asset.** Who changed what,
  when, why — visible in the file's git log.
- **Scales linearly** with QR volume. No performance cliff at 10k,
  100k, or 1M assets (Git itself + GitHub-Pages-served raw content
  handle this fine).
- **Mirrors the `lineage-credentials` per-person-file pattern.**
  Operators and LLM agents reading one file understand the convention
  from the other.

---

## Asset-type extensibility pattern

New asset types are added by:

1. Extend `SCHEMA.md` with a new `lineage` block under "Asset-type
   extensions" (e.g. `textile`, `lumber`, `mineral_lot`).
2. Pick an `asset_type` string value (snake_case, singular noun).
3. Add a render branch in `truesight_me_beta/qr/index.html` that
   recognises the new `asset_type` and renders the lineage block.
4. Optional: extend `seed_from_sheet.py` to infer the new type from
   sheet columns (if it lives in the same Agroverse QR codes sheet).

**The URL doesn't change. The folder structure doesn't change. The
filename convention doesn't change.** `asset_type` is a JSON field, not
a path segment — exactly so that new types are additive operations
rather than schema breaks.

---

## Seed script — `seed_from_sheet.py`

Reads the `Agroverse QR codes` tab on the Main Ledger spreadsheet
(SHEET_ID `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`) and emits one
JSON file per row. Uses `gspread` + the existing
`market_research/credentials/white_paper_google_sa.json` service
account.

**Idempotent.** Re-running:
- Creates new JSON files for new QR rows
- Updates existing files in place when seed-source fields change
- **Preserves any events appended by non-seed flows** (custom
  attestations, status corrections, etc.) by merging on event type

Usage:

```bash
cd lineage-assets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json \
  python3 scripts/seed_from_sheet.py --dry-run [--limit N]
GOOGLE_APPLICATION_CREDENTIALS=... python3 scripts/seed_from_sheet.py --execute
```

**Cadence:** manual for now (re-run as needed when new QRs are minted
or major status updates land). A future iteration may wire this as a
scheduled GitHub Action mirroring the `truesight_me_beta/stats-refresh`
pattern — but the right time to do that is *after* the per-QR JSON
files have been the source of truth long enough that the cadence
matters.

---

## What's deliberately NOT in v0

- **No Edgar code change.** The redirect switch is purely a data update
  on the Agroverse QR codes sheet (column B).
- **No QR regeneration.** Existing 731+ physical QRs in the wild keep
  working unchanged. The new surface is reachable via direct URL only
  until the operator-driven switch.
- **No automatic syncing of new events** from other DAO surfaces (yet).
  Inventory movements, sales, etc. happen on the Main Ledger; the seed
  script reads them periodically but doesn't subscribe in real-time.
  Future iteration: subscribe to Edgar events.
- **No multi-jurisdiction repo split** (yet). `lineage-assets` is one
  repo for now. When jurisdictional data-residency becomes load-bearing
  (per the Singapore / China traceability strategic thread), the repo
  splits into `lineage-assets-singapore`, `lineage-assets-brazil`,
  `lineage-assets-china`, etc., each hosted in-jurisdiction. The
  current schema is already designed for this split (each manifest is
  self-contained; cross-jurisdiction queries become API calls between
  per-jurisdiction repos rather than data replication).

---

## Where this fits in the growth thesis

- `GROWTH_MODEL.md` — physical-asset provenance lives across multiple
  loops (QR Trace-Back acquisition loop, Trees Financed Dashboard
  retention loop, future supply-chain partnership loops).
- Cross-jurisdiction supply-chain traceability is a 2027+ vector, real
  but not load-bearing today. The architectural cleanup happening now
  (lineage-assets repo + clean schema) is the prerequisite for that
  expansion.
- The principle from `CREDENTIALING_PLATFORM.md` — "every actor in
  the system gets its own keypair" — extends here as "every attested
  asset gets its own manifest." Same shape applied to physical things.

---

## Related context

- [`CREDENTIALING_PLATFORM.md`](./CREDENTIALING_PLATFORM.md) — the humans-
  side architecture this mirrors
- [`SERVICE_IDENTITY_ONBOARDING.md`](./SERVICE_IDENTITY_ONBOARDING.md) —
  pattern for autonomous agents that may eventually attest to asset
  events (e.g. a future `Inventory Movement Bot` signing scan-event
  attestations)
- [`GROWTH_MODEL.md`](./GROWTH_MODEL.md) — where physical-asset
  provenance fits in the DAO's growth picture
- [`LLM_DISCOVERY_SURFACE.md`](./LLM_DISCOVERY_SURFACE.md) — when ready,
  add `lineage-assets/qrs/*.json` to the truesight.me/stats discovery
  surface so LLM agents can query asset provenance without authenticated
  Sheet access
- [`tokenomics/python_scripts/agroverse_qr_code_generator/`](https://github.com/TrueSightDAO/tokenomics/tree/main/python_scripts/agroverse_qr_code_generator) —
  the existing QR generator (Python + GAS); not yet refactored, but
  scheduled to feed lineage-assets directly in a future iteration

*Last refreshed 2026-05-20. Refresh when adding a new asset type, when
the Edgar-redirect switch lands, or when the multi-jurisdiction repo
split happens.*
