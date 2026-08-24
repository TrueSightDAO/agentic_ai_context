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

## Sophia (autopilot) time estimates: raw execution vs direct time

**Convention set by Gary 2026-08-24 (thread 14165).** When an estimate is needed for **Sophia's** (the autopilot's) time on a task — e.g. an incident, a fix, a plan unit — the estimate is split into **two separate `[CONTRIBUTION EVENT]`s**, never merged into one:

| Event | Definition | How it is measured | Example attribution |
|-------|-----------|--------------------|---------------------|
| **Raw execution** | Machine tool-execution time — actual time the tools/SSH/scripts ran (SSH diagnostics, sheet reads, GAS deploys, webhook fires, PR machinery, key registration, etc.) | Count tool operations per phase; sum their measured/typical durations (e.g. `ssh_run` ~seconds–min; `gas_deploy_project` ~30–60 s; webhook fires ~30–90 s; big sheet pulls ~seconds). Rough wall-clock estimate is acceptable; be explicit that it is raw machine time. | Contributor: `Sophia Truesight` — Description starts **"Raw machine execution…"** |
| **Direct time** | Sophia's engagement/analysis equivalent — the reasoning, diagnosis, correction cycles, and attention that a human operator would have spent driving the same work | Estimate from turn count, depth of diagnosis, and the human-equivalent time for the analysis performed (the governor may provide or approve the number). Explicitly an **estimate**. | Contributor: `Sophia Truesight` — Description starts **"Direct time (engagement/analysis)…"** |

### Rules

- **Always file two separate events** for Sophia's time (raw execution + direct time) when both are being credited. Never collapse them into one "Sophia" number unless the governor explicitly asks for a single figure.
- **Governor (human) direct time is a separate event** under the governor's own name (e.g. `Gary Teh`) — e.g. "Gary Teh direct time…" — and is *not* part of Sophia's raw/direct split.
- **Amounts are informational** — `TDG Issued: 0` unless the governor sets real economics. The split exists so the ledger distinguishes machine cost from human-equivalent attention.
- **Field format** follows the canonical event: `Type` = `Time (Minutes)`, `Amount` = minutes, `Description` = explicit (start with **"Raw machine execution…"** or **"Direct time (engagement/analysis)…"**), `Contributors` = display name (`Sophia Truesight` / `Gary Teh`). Do not add `TDG Issued` to the attributes unless the governor set an award.
- **Worked example (2026-08-24, inventory-movement unauthorized incident, thread 14165):**
  - `Sophia Truesight` / 60 min — "Raw machine execution…" (~200 tool ops: SSH, sheet reads, GAS deploys ×3, webhook fires, key registration/verification, PRs #424/#425/#312)
  - `Sophia Truesight` / 60 min — "Direct time (engagement/analysis)…" (diagnosis, root-cause analysis, correction cycles)
  - `Gary Teh` / 60 min — "Gary Teh direct time…" (17 thread messages, sheet checks, directing fixes, approving merges)

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

| Step | Event | Module / DApp page | What it does |
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
| Tracking number | `N/A
