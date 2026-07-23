# DAO client — AI agent contribution submissions (convention)

When an **AI coding assistant** completes work that should appear on the **DAO contribution ledger** (`[CONTRIBUTION EVENT]` via **Edgar**), use the **`dao_client`** Python repo so the payload matches the DApp: same RSA signing, same `POST /dao/submit_contribution` endpoint as human operators.

**Repo:** [TrueSightDAO/dao_client](https://github.com/TrueSightDAO/dao_client)  
**Credentials:** `dao_client/.env` (never commit) — `EMAIL`, `PUBLIC_KEY`, `PRIVATE_KEY` from `python3 auth.py login --email …`.

---

## Required convention (machine-checkable + human-readable)

1. **Use the dedicated CLI** (do not hand-curl Edgar for this class of work):
   ```bash
   cd ~/Applications/dao_client
   source .venv/bin/activate   # if using venv
   python3 modules/report_ai_agent_contribution.py \
     --title "Short one-line title" \
     --body-file path/to/description.md \
     --pr https://github.com/TrueSightDAO/some-repo/pull/123 \
     --pr https://github.com/TrueSightDAO/other-repo/pull/456
   ```
   Or pass `--body` instead of `--body-file` for a short inline description (still include PR URLs inside the text if you use `--body`).

2. **At least one merged (or ready) GitHub PR URL** under **`https://github.com/TrueSightDAO/`** must be supplied with **`--pr`** (repeatable). The script rejects non–TrueSightDAO URLs so personal forks do not pollute the audit trail.

   **PR or commit URL evidence (2026-07-22):** when the work was merged **directly, without a PR** — e.g. the governor explicitly said "merge and deploy" in an interactive session rather than routing through a reviewed PR — a **commit URL** is acceptable in its place: `https://github.com/TrueSightDAO/<repo>/commit/<sha>` (full or short SHA, 7+ hex chars). The script validates this the same way it validates PR URLs (TrueSightDAO org only, real pattern match — a bare `.../commits/<branch>` listing page does NOT count as evidence, it has to be a specific commit). **Prefer a real PR whenever one exists** — only fall back to a commit URL when there genuinely isn't a PR to cite. This convention exists so **all LLMs** hit the same fallback instead of getting stuck (this was discovered when a session had four units of work merged directly with no PR, and the submission had no way to comply until this fallback was added).

3. **Be explicit in the body** (bullet list is ideal):
   - **What changed** (repos, files, behavior).
   - **Why** (safeguard, bugfix, operator workflow).
   - **Evidence:** every **`--pr`** link again inside the body under a **“GitHub”** or **“Pull requests”** heading so the Telegram / sheet line is self-contained when someone scrolls without the CLI args.

4. **`Type` field** must be one of the canonical rubric entries: `"Time (Minutes)"`, `"USD"`, `"USDT sent"`, `"USDT received"`, or `"AI Agent (software & documentation)"`. The module validates this against `VALID_CONTRIBUTION_TYPES` from `report_contribution.py` and rejects invalid values.

5. **`Amount` / `TDG Issued`** default to **`0`** unless the operator sets real economics for the session.

6. **`Contributor(s)`** defaults to `"Gary Teh"` (derived from `EMAIL` in `.env`). Override with `--contributors "Display Name"` when the human sponsor should be credited instead. Do NOT use "Garyjob" or "garyjob@gmail.com" — always "Gary Teh".

7. **`--generation-source`** may point at this doc or the Cursor session URL so `This submission was generated using …` is traceable:
   ```text
   https://github.com/TrueSightDAO/agentic_ai_context/blob/main/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md
   ```

8. **`--dry-run`** prints the signed payload only (no POST). Use before the real submission when debugging.

---

## Browser equivalent

Human flow: [DAO Contribution Report](https://dapp.truesight.me/report_contribution.html) (`[CONTRIBUTION EVENT]`). The CLI mirrors that event and attribute names expected by Edgar / scoring.

---

## Event selection: `[CONTRIBUTION EVENT]` vs `[CAPITAL INJECTION EVENT]`

Future AIs and humans often confuse these two events. Here is the decision tree:

| Scenario | Event | Module / DApp page |
|----------|-------|-------------------|
| You (or a contributor) spent personal money on DAO operations — software, tools, travel, supplies | `[CONTRIBUTION EVENT]` — Type: **USD** | `report_contribution.py` / `report_contribution.html` |
| You (or a contributor) volunteered time | `[CONTRIBUTION EVENT]` — Type: **Time** | `report_contribution.py` / `report_contribution.html` |
| An **external investor** wires funds directly into an AGL-managed contract or ledger | `[CAPITAL INJECTION EVENT]` | `report_capital_injection.py` / `report_capital_injection.html` |

**Rule of thumb:** If the money came *out of your pocket* for day-to-day DAO work → **Contribution**. If the money is *new investment capital* entering an AGL contract from an outside party → **Capital Injection**.

## Double-entry purchase workflow (`[ASSET RECEIPT EVENT]`)

When a contributor purchases a **physical item** for DAO inventory (non-serialized, non-QR-coded), the ledger requires **two events** to maintain double-entry accounting. Example: buying a Moka Express on Amazon for DAO operations.

### Flow

| Step | Event | Module | What it does |
|------|-------|--------|--------------|
| 1 | `[CONTRIBUTION EVENT]` — Type: **USD** | `report_contribution.py` | Records cash outflow (`--amount <total>`, `--contributors "Gary Teh"`). Attach the invoice PDF with `--attachment`. Set `--destination-contribution-file-location` to a GitHub blob URL — Edgar uploads the file there. |
| 2 | `[ASSET RECEIPT EVENT]` | `report_asset_receipt.py` | Records positive inventory leg. `--currency` = exact Currencies!A name, `--amount` = unit count (1 for single items), `--fund-handler` = who holds it, `--description` must include the PDF blob URL and cash-leg row reference. |

### Downstream (Edgar → GAS)

After both events land in Telegram Chat Logs:
1. **Edgar** `trigger_immediate_processing` matches `[ASSET RECEIPT EVENT]` → enqueues `WebhookTriggerWorker` → calls `asset-receipt-ingest` GAS
2. **GAS** (`tokenomics/google_app_scripts/asset_receipt_ingest/`) processes the row:
   - Creates **Currencies** row (col A = Currency name, col B = landed unit cost)
   - Sorts Currencies A→Z
   - Creates **offchain transactions** positive inventory leg (+1 unit, Fund Handler, description with PDF link)
   - Appends audit row to **Asset Receipts** tab (dedup key = Telegram update_id)

### Conventions

- **`Currency` name**: `"<Product> (<vendor>, order <id>)"` — e.g. `"Bialetti Moka Express 18 Cup (ASIN B0000AN3QK, order 111-9241674-1033036)"`
- **PDF upload**: Set `Destination Contribution File Location` to `https://github.com/TrueSightDAO/.github/blob/main/assets/<YYYYMMDD>_<vendor>_<id>_invoice.pdf` — Edgar uploads via `--attachment`
- **Offchain description**: `"Received 1 unit of <Product>. Pairs offchain USD row N. Invoice: <GitHub blob URL>"`
- **`--attachment` flag**: Available on all dao_client modules since `build_event_cli` supports it. Sends file as multipart alongside the signed event.

### GAS webhook URL

- **Exec URL**: `https://script.google.com/macros/s/AKfycbzcXBXYKmKiYg-tS2cqf60gWVm0ro17ndWVMnxNkc0dimaGUW3CYoi4b8nMZzVbENaw/exec`
- **Clasp mirror**: `tokenomics/clasp_mirrors/1o2lzpdTZBYTTFdXzWJoATxznbqL959b_O7_no2Gd-OV4ryOPZOsqxtpU/`
- **Edgar webhook config**: `dao_protocol` .env → `OFFCHAIN_PROCESSING_WEBHOOK_URL`

## Cash sales via `[SALES EVENT]` (no Stripe checkout)

When selling serialized QR-coded products for cash (not through Stripe):

| Field | Correct value | Incorrect value | Why |
|-------|--------------|-----------------|-----|
| Stripe Session ID | **`(none)`** | `N/A` | GAS normalizes `(none)` to empty and skips the Stripe checkout lookup. `N/A` passes through as a literal string and triggers log noise. |
| Shipping Provider | `N/A` | — | Local pickup / hand delivery |
| Tracking number | `N/A` | — | No shipping label |

For serialized QR products, `[SALES EVENT]` per QR code IS sufficient — the downstream chain (QR Code Sales → offchain transactions → treasury cache) handles inventory depletion. A separate `[INVENTORY MOVEMENT]` is only needed for bulk/non-serialized inventory tracked by weight or count.

**Ledger assignment ≠ physical possession:** A QR code tracked under AGL6 ledger can physically be in Gary Teh's car. The `manager_name` tracks who manages the record, not who holds the bag.

## Related context

- **`tokenomics/SCHEMA.md`** — `Telegram Chat Logs`, **Governor** column **S**, **Inventory Movement**, **Scored Expense Submissions**.
- **`sentiment_importer`** — **TRADING PLATFORM ONLY**, not the DAO API. DAO submissions go through **`dao_protocol`** (FastAPI, Python). The Rails Edgar app appends to Telegram Chat Logs via the legacy code path; all new DAO traffic routes through dao_protocol.
- **`WORKSPACE_CONTEXT.md`** § Edgar / tokenomics / DApp relationships.

---

## Anti-patterns

- Submitting without **any** `github.com/TrueSightDAO/.../pull/` (or, for a direct merge with no PR, `.../commit/<sha>`) link when code or docs landed in GitHub.
- Vague one-line descriptions with no file/PR reference.
- Using a non–`dao_client` signing path that drifts from DApp canonical formatting.
