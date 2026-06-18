# CLI Sales Event Audit & Alignment Plan

## Context

Audit of `dapp.truesight.me/report_sales.html` vs `truesight-dao-report-sales` CLI vs `edgar.truesight.me` docs revealed gaps:

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

### PR 2: Update Edgar docs page

**Scope:** `dapp_beta` repo — the `edgar.truesight.me` docs page

Changes:
- Replace stale `[SALES EVENT] - QR Code: ... - Buyer Name: ... - Buyer Email: ... - Amount: ... - Currency: USD` with actual DApp format
- Show the real payload: `Item`, `Sales price`, `Sold by`, `Cash proceeds collected by`, `Owner email`, etc.
- Note that `Stripe Session ID`, `Shipping Provider`, `Tracking number` are optional

**Gate:** PR merged + deployed to beta, reviewed, then promoted to prod

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

## RESUME HERE

PR 1: Update CLI `report_sales` module in `dao_client` repo.

## Acceptance

- [ ] PR 1 merged: CLI accepts all DApp fields, `--owner-email` required
- [ ] PR 2 merged: Edgar docs show correct payload format
- [ ] PR 3 done: Gergana's sale re-submitted with complete payload
- [ ] Contribution reported for the work
