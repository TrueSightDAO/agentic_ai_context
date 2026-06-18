# CLI Sales Event Audit & Alignment Plan

## Context

Audit of `dapp.truesight.me/report_sales.html` vs `truesight-dao-report-sales` CLI vs `edgar.truesight.me` docs revealed gaps.

Expanded scope: **all 37 DApp modules** in `dapp_beta` were audited against the CLI (`dao_client`) to find every gap. The DApp submits events to Edgar via canonical payloads; the CLI must match those payloads exactly.

---

## Phase 1 — Sales Event (the original gap)

### DApp payload (actual)
```
[SALES EVENT]
- Item: {qr_code}
- Sales price: ${amount}
- Sold by: {manager_name}
- Cash proceeds collected by: {cash_name}
- Owner email: {email}
- Stripe Session ID: {id or (none)}
- Shipping Provider: {provider or (none)}
- Tracking number: {tracking or (none)}
- Attached Filename: {filename or None}
- Submission Source: {url}
--------
```

### CLI current
```
[SALES EVENT]
- Item: {free_text_product_description}
- Sales price: ${amount}
- Sold by: {free_text}
- Cash proceeds collected by: {free_text}
- Submission Source: {free_text}
--------
```

### Edgar docs (stale)
```
[SALES EVENT] - QR Code: ... - Buyer Name: ... - Buyer Email: ... - Amount: ... - Currency: USD
```

### Gaps
1. **`Owner email`** — CLI has it as optional `--owner-email`; DApp always sends it. Should be required.
2. **`Item`** — CLI uses free-text product description; DApp uses QR code ID. Should accept `--qr-code` as primary.
3. **`Stripe Session ID`**, **`Shipping Provider`**, **`Tracking number`**, **`Attached Filename`** — missing from CLI entirely.
4. **`Sold by` / `Cash proceeds collected by`** — CLI accepts free-text; DApp pulls from GAS `list_with_members` (Column U = Manager Name in Agroverse QR codes sheet). CLI should validate or at least document the source.
5. **Edgar docs** — show `Buyer Name`/`Buyer Email`/`Amount`/`Currency` which don't match what the DApp actually sends.

---

## Phase 2 — Full DApp Module Audit

Every DApp module that submits events to Edgar was audited. The following modules have CLI equivalents that need alignment, or no CLI equivalent at all.

### Transaction / Event Modules

| # | DApp Module | CLI Equivalent | Status | Action |
|---|-------------|----------------|--------|--------|
| 1 | `report_sales.html` | `truesight-dao-report-sales` | **Gaps found** | PR1 — align fields |
| 2 | `report_inventory_movement.html` | `truesight-dao-report-inventory-movement` | Needs audit | PR4 — verify payload parity |
| 3 | `report_contribution.html` | `truesight-dao-report-contribution` | Needs audit | PR5 — verify payload parity |
| 4 | `report_dao_expenses.html` | `truesight-dao-report-expense` | Needs audit | PR6 — verify payload parity |
| 5 | `report_capital_injection.html` | `truesight-dao-report-capital-injection` | Needs audit | PR7 — verify payload parity |
| 6 | `report_tree_planting.html` | `truesight-dao-report-tree-planting` | Needs audit | PR8 — verify payload parity |
| 7 | `report_asset_receipt.html` | **No CLI equivalent** | **Missing** | PR9 — add CLI module |
| 8 | `currency_conversion.html` | **No CLI equivalent** | **Missing** | PR10 — add CLI module |
| 9 | `mint_donation.html` | **No CLI equivalent** | **Missing** | PR11 — add CLI module |

### Partner / Store Modules

| # | DApp Module | CLI Equivalent | Status | Action |
|---|-------------|----------------|--------|--------|
| 10 | `partner_add.html` | Needs audit | Unknown | PR12 — audit/add |
| 11 | `partner_check_in.html` | Needs audit | Unknown | PR12 — audit/add |
| 12 | `store_interaction_history.html` | **No CLI equivalent** | **Missing** | PR13 — add CLI module |
| 13 | `stores_by_status.html` | **No CLI equivalent** | **Missing** | PR13 — add CLI module |
| 14 | `stores_nearby.html` | **No CLI equivalent** | **Missing** | PR13 — add CLI module |
| 15 | `warmup_review.html` | **No CLI equivalent** | **Missing** | PR13 — add CLI module |

### Governance Modules (DApp-only — no CLI needed)

| Module | Reason |
|--------|--------|
| `create_proposal.html` | Requires interactive voting UI — DApp-only |
| `review_proposal.html` | Requires interactive voting UI — DApp-only |
| `view_open_proposals.html` | Read-only browsing — DApp-only |
| `withdraw_voting_rights.html` | Requires interactive form + signature — DApp-only |
| `verify_request.html` | Verification of shared text — DApp-only |
| `notarize.html` | Document notarization — DApp-only |
| `governor_permissions.html` | Governor admin panel — DApp-only |
| `governor_contributor_admin.html` | Governor admin panel — DApp-only |
| `program_registrations_review.html` | Review workflow — DApp-only |

### Inventory / QR / Operations Modules (DApp-only — no CLI needed)

| Module | Reason |
|--------|--------|
| `scanner.html` | Camera-based QR scanning — DApp-only |
| `update_qr_code.html` | Interactive QR lookup/edit — DApp-only |
| `batch_qr_generator.html` | Batch generation — DApp-only |
| `view_inventory_holdings.html` | Read-only browsing — DApp-only |
| `restock_recommender.html` | Interactive calculator — DApp-only |
| `shipping_planner.html` | Interactive calculator — DApp-only |
| `repackaging_planner.html` | Interactive calculator — DApp-only |
| `fulfill_subscriptions.html` | Interactive obligation browser — DApp-only |
| `register_farm.html` | Interactive form — DApp-only |
| `submit_feedback.html` | Simple form — DApp-only |

### Identity / Core (DApp-only)

| Module | Reason |
|--------|--------|
| `create_signature.html` | WebCrypto key generation — browser-only |
| `chat.html` | Chat interface — DApp-only |
| `index.html` | Landing page — DApp-only |

---

## Sequenced PRs

### PR 1: Update CLI `report_sales` module

**Scope:** `dao_client` repo — `truesight_dao_client/modules/report_sales.py`

Changes:
- Add `--qr-code` as primary item identifier (maps to `Item` in payload)
- Make `--owner-email` required (was optional)
- Add optional `--stripe-session-id`, `--shipping-provider`, `--tracking-number`
- Add optional `--attached-filename`
- Default `--submission-source` to `CLI` if not provided
- Keep backward compat: `--item` still works but logs deprecation warning if used without `--qr-code`
- Update `--help` to show all fields matching DApp

**Gate:** PR merged + deployed to PyPI

---

### PR 2: Update Edgar docs page

**Scope:** `dapp_beta` repo — the `edgar.truesight.me` docs page

Changes:
- Replace stale `[SALES EVENT] - QR Code: ... - Buyer Name: ... - Buyer Email: ... - Amount: ... - Currency: USD` with actual DApp format
- Show the real payload: `Item`, `Sales price`, `Sold by`, `Cash proceeds collected by`, `Owner email`, etc.
- Note that `Stripe Session ID`, `Shipping Provider`, `Tracking number` are optional

**Gate:** PR merged + deployed to beta, reviewed, then promoted to prod

---

### PR 3: Re-submit Gergana's sale with correct format

**Scope:** One-time CLI invocation

After PRs 1+2 are live, re-submit:
```
truesight-dao-report-sales \
  --qr-code 2024OSCAR_20260121_32 \
  --sales-price 17.50 \
  --sold-by "Gergana - The Way Home Shop" \
  --cash-proceeds-collected-by "Gary Teh" \
  --owner-email info@thewayhomeshop.com \
  --submission-source "https://dapp.truesight.me/report_sales.html"
```

**Gate:** Governor confirms submission succeeded

---

### PR 4: Audit CLI `report_inventory_movement` against DApp

**Scope:** `dao_client` repo — `truesight_dao_client/modules/report_inventory_movement.py`

Action:
- Read DApp `report_inventory_movement.html` payload format
- Compare field-by-field with CLI
- Align any gaps (missing fields, wrong labels, optional/required mismatch)

**Gate:** PR merged + deployed to PyPI

---

### PR 5: Audit CLI `report_contribution` against DApp

**Scope:** `dao_client` repo — `truesight_dao_client/modules/report_contribution.py`

Action:
- Read DApp `report_contribution.html` payload format
- Compare field-by-field with CLI
- Align any gaps

**Gate:** PR merged + deployed to PyPI

---

### PR 6: Audit CLI `report_dao_expenses` against DApp

**Scope:** `dao_client` repo — `truesight_dao_client/modules/report_dao_expenses.py`

Action:
- Read DApp `report_dao_expenses.html` payload format
- Compare field-by-field with CLI
- Align any gaps

**Gate:** PR merged + deployed to PyPI

---

### PR 7: Audit CLI `report_capital_injection` against DApp

**Scope:** `dao_client` repo — `truesight_dao_client/modules/report_capital_injection.py`

Action:
- Read DApp `report_capital_injection.html` payload format
- Compare field-by-field with CLI
- Align any gaps

**Gate:** PR merged + deployed to PyPI

---

### PR 8: Audit CLI `report_tree_planting` against DApp

**Scope:** `dao_client` repo — `truesight_dao_client/modules/report_tree_planting.py`

Action:
- Read DApp `report_tree_planting.html` payload format
- Compare field-by-field with CLI
- Align any gaps

**Gate:** PR merged + deployed to PyPI

---

### PR 9: Add CLI `report_asset_receipt` module

**Scope:** `dao_client` repo — new module

Action:
- Read DApp `report_asset_receipt.html` payload format
- Create CLI module matching all fields
- Register in CLI command tree

**Gate:** PR merged + deployed to PyPI

---

### PR 10: Add CLI `currency_conversion` module

**Scope:** `dao_client` repo — new module

Action:
- Read DApp `currency_conversion.html` payload format
- Create CLI module matching all fields (source/target currency, amount, FX rate, receipt attachment)
- Register in CLI command tree

**Gate:** PR merged + deployed to PyPI

---

### PR 11: Add CLI `mint_donation` module

**Scope:** `dao_client` repo — new module

Action:
- Read DApp `mint_donation.html` payload format
- Create CLI module matching all fields (donor name/email, amount, proof file, notes)
- Register in CLI command tree

**Gate:** PR merged + deployed to PyPI

---

### PR 12: Audit/add partner modules

**Scope:** `dao_client` repo

Action:
- Read DApp `partner_add.html` and `partner_check_in.html` payload formats
- Compare with any existing CLI equivalents
- Add missing modules or align gaps

**Gate:** PR merged + deployed to PyPI

---

### PR 13: Update Edgar docs page (comprehensive)

**Scope:** `dapp_beta` repo — the `edgar.truesight.me` docs page

Changes:
- Document ALL event types with their real payload formats (not just SALES EVENT)
- Include: INVENTORY MOVEMENT, CONTRIBUTION EVENT, EXPENSE EVENT, CAPITAL INJECTION EVENT, TREE PLANTING EVENT, ASSET RECEIPT EVENT, CURRENCY CONVERSION EVENT, DONATION MINT EVENT, PARTNER ADD EVENT, PARTNER CHECK-IN EVENT
- For each: required fields, optional fields, example payload

**Gate:** PR merged + deployed to beta, reviewed, then promoted to prod

---

## RESUME HERE

Phase 1 — PR 1: Update CLI `report_sales` module in `dao_client` repo.

## Acceptance

### Phase 1 — Sales Event
- [ ] PR 1 merged: CLI accepts all DApp fields, `--owner-email` required
- [ ] PR 2 merged: Edgar docs show correct payload format
- [ ] PR 3 done: Gergana's sale re-submitted with complete payload

### Phase 2 — Inventory & Asset Modules
- [ ] PR 4 merged: `report_inventory_movement` aligned
- [ ] PR 5 merged: `report_contribution` aligned
- [ ] PR 6 merged: `report_dao_expenses` aligned
- [ ] PR 7 merged: `report_capital_injection` aligned
- [ ] PR 8 merged: `report_tree_planting` aligned

### Phase 3 — Missing CLI Modules
- [ ] PR 9 merged: `report_asset_receipt` added
- [ ] PR 10 merged: `currency_conversion` added
- [ ] PR 11 merged: `mint_donation` added

### Phase 4 — Partner Modules
- [ ] PR 12 merged: partner modules audited/added

### Phase 5 — Edgar Docs Overhaul
- [ ] PR 13 merged: all event types documented

### Contribution
- [ ] Contribution reported for the work
