# Ledger conversion and repackaging (Main Ledger)

**For AI assistants:** Read this file **before** answering questions about **combining Main Ledger inventory into a new product**, **repackaging**, **input vs output `Currency`**, **cost per unit of output**, or **suggested names for new production lines**. This is the **canonical playbook** for that workflow (also linked from **`WORKSPACE_CONTEXT.md`** §3b).

**Related:** Main Ledger spreadsheet ID — **`GOOGLE_API_CREDENTIALS.md`**. Sheet/column layout — **`tokenomics/SCHEMA.md`**. Typical API credentials path — **`tokenomics/python_scripts/schema_validation/gdrive_schema_credentials.json`**.

---

## Definition

**Ledger conversion and repackaging** means: at a **specific place / operator** (e.g. **Kirsten’s location**, **Matheus’ location**), inventory **consumes** one or more **input** `Currency` lines and **creates** **output** unit(s), recorded as **`Currency`** strings on the Main Ledger.

---

## Standard user prompt (natural language)

The user may say something like:

*“[Operator] mentioned they converted **N** bags of [input description] **in their possession on the main ledger** into **M** bags of **[net weight] [product]**.”*

### Default assistant deliverables (unless narrowed)

1. **Input currencies** — exact Main Ledger **`Currency`** strings for each material input (cacao source, empty pouch line, etc.), resolved using **`offchain asset location`** for that **Location** (manager) and the conventions below.
2. **Cost per unit of output** — formula and number: use **`offchain asset location`** Col D **Unit Cost** for that holder’s rows; total \(= \sum_i (\text{qty}_i \times \text{unit cost}_i)\) for all inputs, then **cost per output** \(= \text{total} / M\). Add labor/overhead only if separate ledger lines are allocated. Prefer **snapshot unit costs** at booking time when historical accuracy matters; say when numbers are **current sheet** only.
3. **Suggested new `Currency` name** — use the **standard template** below (explicit weight + source).

---

## Standard `Currency` name for new repackaging outputs

**Prefer this pattern** for **200 g ceremonial** (and analogous explicit outputs) so **net weight** and **cacao source** are readable without parsing a short `+` composite:

```text
Ceremonial Cacao Kraft Pouch - Alibaba:269035810001023771 | Cacao Mass | 200 grams | <SOURCE_DESCRIPTOR> | <Operator> YYYYMMDD | <City> - <AGLnn>
```

### Slots (adapt per run)

| Segment | Meaning |
|--------|--------|
| `Ceremonial Cacao Kraft Pouch - Alibaba:269035810001023771` | Empty **ceremonial kraft** shell from that supplier ref (change `269035810001023771` only if pouch stock is a different catalog line). |
| `\| Cacao Mass \| 200 grams \|` | **Explicit** net weight and product form for the **filled** unit (adjust **200** / wording if the product differs). |
| `<SOURCE_DESCRIPTOR>` | **Input** identity, e.g. `8 Ounce Nibs CP340992735BR`, or bulk line when cross-ledger rules exist. |
| `<Operator> YYYYMMDD` | Handler and **booking** date (e.g. `Kirsten 20260330`). |
| `<City> - <AGLnn>` | Ops convention (e.g. `San Francisco - AGL4` when Oscar-linked); align with existing rows or ask the user. |

### Legacy naming

Older rows may use a **short** composite such as `Ceremonial … Alibaba:… + 8 Ounce Package Kraft Pouch CP… | Kirsten …`. **New** repackaging outputs should use the **pipe / explicit** template above unless the user asks otherwise.

---

## Signals in sheet data

- **`Alibaba:…`** — empty **kraft/pouch** stock from that order. **`20250219006`**-style tokens — alternate **pouch/material** line (see **`Currencies`** / **`offchain asset location`**).
- **`CP`…`BR`** — usually **Correios** (Brazil Post) tracking from Ilheus area → U.S.; see **`WORKSPACE_CONTEXT.md`** §4 (Correios note).
- **`8 Ounce Package Kraft Pouch  CP…BR`** — often **two spaces** before `CP` in the canonical nib retail line for that batch.
- One output **`Currency`** repeats on **`Agroverse QR codes`**; totals on **`offchain asset location`** / **`off chain asset balance`**. Disambiguate runs by **operator + YYYYMMDD**.

### Sheets (per SCHEMA)

| Sheet | Use | Key columns |
|-------|-----|-------------|
| **`offchain asset location`** | Who holds what; **unit cost** | A `Currency`, B Location (manager), C amount, D unit cost, E total value |
| **`off chain asset balance`** | Network totals by `Currency` | — |
| **`Currencies`** (Main Ledger) | Catalog names, weights, prices + repackaging audit trail | A Currency, B Price in USD, K–M weights/SKU, **N Raw request text** (repackaging), **O Composition JSON URL** (repackaging) |
| **`Currency Creation`** (Ops sheet `1qbZZhf…`, gid `2120959876`) | Per-output processing log for the repackaging planner flow | A Created at (ISO), B `{request_id}#{index}`, C Suggested Currency, D Unit Cost (USD), E Holder, F Payload JSON |
| **`Telegram Chat Logs`** (Ops sheet `1qbZZhf…`) | Intake log for all DApp submissions including `[REPACKAGING BATCH EVENT]` | Col G holds the full signed text; Edgar writes it on `submit_contribution` |
| **`Agroverse QR codes`** | Per-unit QR view | `Currency`, Manager Name, status |

---

## Repackaging planner flow (`dapp/repackaging_planner.html`)

**Single-sitting, Edgar-routed submit** — same shape as every other DApp page.

1. **Compose** on the DApp: pick holder → add input rows (ledger + custom) → add output rows (units M + weight per output + label). Cost is allocated by weight: `cost_per_gram = total_input_cost / Σ(M × weight_per_unit_g)`, each output's `unit_cost = cost_per_gram × weight_per_unit_g`. A `| YYYYMMDD` suffix is auto-appended to output Currency names if no date token is present, to avoid collisions on the Main Ledger `Currencies` tab.
2. **Sign + POST** `FormData { text, attachment? }` to `https://edgar.truesight.me/dao/submit_contribution`. The `text` is a `[REPACKAGING BATCH EVENT]` block with human-readable bullets for inputs/outputs/totals plus a trailing `Batch Payload (base64 JSON): <b64>` line carrying the structured composition + the standard signature block (`My Digital Signature: …`, `Request Transaction ID: …`, `--------`).
3. **Edgar** writes the row to `Telegram Chat Logs` (col G) and enqueues `WebhookTriggerWorker` against the repackaging Apps Script with `?action=processRepackagingBatchesFromTelegramChatLogs`. Controller branch in `sentiment_importer/app/controllers/dao_controller.rb#trigger_immediate_processing`; webhook URL in `config.repackaging_processing_webhook_url`.
4. **The Apps Script** (`agroverse-inventory/gas/repackaging-currency-ingest`, script `1StT6vogwlOYOqtpSiqwnF9PJmScivbBxIj2Hhplfd4YQbCfuWIerrUV0`) `doGet` scans col G for `[REPACKAGING BATCH EVENT]` rows, base64-decodes the inline JSON, dedups via `Currency Creation` col B (`{request_id}` exact or `{request_id}#` prefix), and calls `processBatchData_()`. Core writes:
   - `Currency Creation`: **N rows**, one per output, keyed `{request_id}#{index}`.
   - Main Ledger `Currencies`: **N rows** (col A name, col B USD, col N raw request text, col O composition JSON URL); body re-sorted by col A.
   - `currencies.json` on GitHub (`TrueSightDAO/agroverse-inventory`, rewritten via contents API).
   - `currency-compositions/{request_id}.json` on GitHub (full batch — inputs + outputs + totals + holder + optional proof attachment).
5. **Legacy doPost** (token-authenticated via `AGROVERSE_INVENTORY_PUBLISH_SECRET`) still works for direct submits, but the canonical path is Edgar-driven.

### Where each piece lives

| Surface | Repo / path |
|---------|-------------|
| Planner UI | `dapp/repackaging_planner.html` |
| Edgar route | `sentiment_importer/app/controllers/dao_controller.rb` (`[REPACKAGING BATCH EVENT]` branch) + `config/application.rb` (`repackaging_processing_webhook_url`) |
| GAS processor | `agroverse-inventory/gas/repackaging-currency-ingest/{Code.gs,appsscript.json,.clasp.json}` — script `1StT6vogwlOYOqtpSiqwnF9PJmScivbBxIj2Hhplfd4YQbCfuWIerrUV0`; `webapp.access = ANYONE_ANONYMOUS` so the public `/exec` URL survives future `clasp deploy` rounds |
| Inventory API (cross-ledger unit cost) | `tokenomics/google_app_scripts/tdg_inventory_management/web_app.gs` — `augmentWithLedgers` now looks up AGL `Balance` unit costs from the main `Currencies` tab via `resolveAglUnitCost_()` |
| Schema | `tokenomics/SCHEMA.md` — `Currency Creation` and `Currencies` N/O columns documented there |

---

## Workflow checklist

1. Main Ledger ID + sheet names from **`tokenomics/SCHEMA.md`**.
2. Sheets API pull; filter **`offchain asset location`** Col B by **operator** name.
3. Map **cacao/input** and **empty pouch** lines to exact **`Currency`** strings (Correios / Alibaba / farm text as in catalog).
4. **Cost:** \(\sum \text{qty} \times \text{Unit Cost}\) ÷ **output count**; sanity-check **`off chain asset balance`** if the output line exists.
5. **Name:** emit **standard template** with user-confirmed date, AGL, city if needed.

### Allocation / edge cases

If **input bag count** ≠ **output bag count** but the user defines a single batch, use **full $ of stated inputs** ÷ **stated outputs** unless they specify otherwise. Confirm **M** (and QR rows) if ambiguous. Labor, labels, and other lines are **additive** when documented.

---

## Cross-ledger conversions (managed AGLs) — upcoming

**Do not assume rules yet.** The user will define flows where inputs live on **managed ledgers** (e.g. **AGL13**: **bulk cacao nibs** → **packaged 200 g ceremonial**). Wait for explicit instructions (which spreadsheet, which `Currency`, how cost flows). Extend **this file** when those rules are provided.
