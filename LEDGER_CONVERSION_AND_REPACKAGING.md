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

## Reading an existing compound name (interpretation, not creation) 🆕 2026-10-15

The section above covers *writing* a new compound name. This covers the opposite direction — given a name
already on the sheet, how to read it correctly. Two real mistakes happened in the same session before this
was written down, so both are kept as worked examples.

**The short-name segment is the physical shell, not a different item.** A long/compound name's *first*
pipe-delimited segment is almost always the same `Currencies` row as a standalone short name elsewhere —
per the template above, `<base-shell> | Cacao Mass | <weight> | <source> | <operator-date> | <city-AGL>`
is **the base shell, qualified**, not a new SKU. `Ceremonial Cacao Kraft Pouch - 20250219006 | Cacao Mass |
200 grams | Paulo 2024 | Santos 018-2025 016-2025 || Ilheus - AGL8` **is** `Ceremonial Cacao Kraft Pouch -
20250219006` (the empty-pouch shell purchased from ShenZhen) once filled and attributed to AGL8 — the same
physical pouches, not two inventories that happen to share a batch code.

**Before treating two differently-named buckets as "the same" or "different," trace provenance — don't
guess from the string.** Walk each name's full transaction history back to its origin event (the row that
first created a positive balance with no prior source). Two outcomes:
- **Continuous, traceable descent with a plausible physical story** (e.g. the short name's origin event is
  a purchase, and the long name's holder/quantity plausibly came from consuming that same purchase) →
  **it's a relabel**, not a transformation needing a value entry. Fix by moving the physical count between
  buckets (append-only), nothing else.
- **No traceable origin at all** (the bucket's balance appears from nothing — no purchase, no injection, no
  prior row) → that's the actual defect, but the fix is still usually "find the real source and move the
  count there," not "invent a value transfer to explain it."

**Don't default to booking a value transfer (Equity/Liability) just because a consumption crosses a ledger
boundary.** A Main-owned shared resource (generic packaging stock) consumed by one AGL's production is a
**relabel of existing stock**, not a new contribution, *unless* the resource was genuinely something the
consuming AGL didn't already have a claim to. The tell: if the same physical units were already going to be
attributed to that AGL's production regardless of which bucket they were sitting in, no value entry is
needed — just move the count. (Compare: Main `offchain transactions` r4858, 2026-10-07 — packaging
genuinely **expensed off** and billed to AGL16 **as a liability** — that case involved an actual third-party
cost recovery, not a same-item relabel. The two patterns look similar on the surface; only provenance
tracing tells them apart.)

**Location-suffix (`+ <AWB/ref> - <City>`) is always a relabel, never a value event.** This suffix marks a
physical relocation of the exact same goods tied to a specific shipment/reference — never book Equity,
Liability, or Expense against a `+<ref>-<city>` conversion; it is pure `[CURRENCY CONVERSION EVENT]`
bookkeeping, same pattern as the repackaging settlement's `#REF!` lesson: substrate-only, append-only.

### Sheets (per SCHEMA)

| Sheet | Use | Key columns |
|-------|-----|-------------|
| **`offchain asset location`** | Who holds what; **unit cost** | A `Currency`, B Location (manager), C amount, D unit cost, E total value |
| **`off chain asset balance`** | Network totals by `Currency` | — |
| **`Currencies`** (Main Ledger) | Catalog names, weights, prices + repackaging audit trail | A Currency, B Price in USD, K–M weights/SKU, **N Raw request text** (repackaging), **O Composition JSON URL** (repackaging) |
| **`Currency Creation`** (Ops sheet `1qbZZhf…`, gid `2120959876`) | Per-output processing log for the repackaging planner flow | A Created at (ISO), B `{request_id}#{index}`, C Suggested Currency, D Unit Cost (USD), E Holder, F Payload JSON |
| **`Telegram Chat Logs`** (Ops sheet `1qbZZhf…`) | Intake log for all DApp submissions including `[REPACKAGING BATCH EVENT]` and `[REPACKAGING SETTLEMENT EVENT]` | Col G holds the full signed text (Edgar writes it on `submit_contribution`). **Col R is the processor dedup gate** — GAS handlers scan Col G for their event tag and skip rows where Col R already has `PROCESSED:<EVENT_TYPE>` (e.g. `PROCESSED:REPACKAGING_SETTLEMENT`). See `tokenomics/SCHEMA.md` § Telegram Chat Logs, column R for the full convention. |
| **`Agroverse QR codes`** | Per-unit QR view | `Currency`, Manager Name, status |

---

## Defining new output currencies (QR-ready)

Repackaging emits **new `Currency` lines**. To make them immediately QR-able, define them with the **`[CURRENCY DEFINITION EVENT]`** (Edgar CLI `truesight-dao-define-currency`) — see `agroverse/AGROVERSE_QR_CODE_BATCH_GENERATION.md` §2b. It writes the full QR-ready field set (col C `Serializable=TRUE` + cols E–J farm/ledger/landing/year) and sorts the tab A→Z. This **replaces the manual gspread fill** that repackaging batches used to require before QR generation would succeed.

---

## Cross-ledger cost allocation (generic — freight, packing, shared cost)

**For AI assistants:** read this whenever one external cost (freight, packing, tooling, a shared service) must be **borne by more than one ledger**, or is **financed** by a third party. This is the **generic** rule; the freight-specific worked example and the full pre-flight checklist are in `brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` §5.16.

1. **Allocate by the real driver, never evenly.** Each ledger's share = cost × that ledger's fraction of the usage driver (shipped **kg**, units, CBM). Cite the source of truth; shares must **sum to the total**.
2. **Cash waterfall.** A ledger self-funds from **cash it already holds**; a financier injects **only the shortfall** (= share − cash, floored at 0) — never the full share, and never “for symmetry” when cash already covers it.
3. **Book to the substrate, never the view.** Append signed rows to the **substrate** tab (`offchain transactions` on Main; `Transactions` on an AGL) — **never** to `offchain asset location`, `off chain asset balance`, or `Balance`, which are array-formula **views**. A write into a spill range breaks the tab to `#REF!` (see the Brazil checklist §5.15 incident; enforced by `agroverse-inventory#18`).
4. **Entity labeling on a cross-ledger injection.** The **Equity** row's `Entity` = the **financier**; the **Assets** row's `Entity` = the **human custodian** (the person who holds/moves the cash). **Never the same name on both legs.**
5. **Reciprocal recording.** A cross-ledger investment needs **both halves** — the **investor's Asset-side claim** *and* the **investee's Equity-side liability**. A one-sided entry leaves the two books disagreeing; verify investor.Asset == investee.Equity before calling a leg done.
6. **Currencies catalog.** A **new asset-type name** needs a Main Ledger **`Currencies`** row with a **`Price in USD`**, or `/aum` silently values it at **$0**. Add it with the booking.
7. **Verification.** After booking, re-read **`/aum` and `/treasury`** (watch stale cache); confirm Amount cells landed **numeric, not text** (`sum()` drops text); and read the **substrate and the derived view** live before declaring done. Driver/landed unit-cost folding (rule 1) uses `unit_cost = (Σ input cost + allocated shipping) / quantity`.

When the allocated cost lands **in inventory**, fold it into unit cost by the same driver: `unit_cost = (Σ input cost + allocated shipping) / quantity` — precedent forms `=(C7+C3)/C2` (AGL7/AGL10, hardcoded) or `=Transactions!$D$5/…` (AGL6, ledger-linked).

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

---

## Settlement handler (post-batch finalisation)

After the batch is processed and the `currency-compositions/<request_id>.json` is live, submit a `[REPACKAGING SETTLEMENT EVENT]` (via `dao_client` `post_repackaging_cleanup` or `dapp/repackaging_settlement.html`). Edgar logs it to **Telegram Chat Logs col G**.

The downstream GAS handler (`processPostRepackagingCleanup_` in `agroverse-inventory/gas/repackaging-currency-ingest/Code.gs`, same script as the batch processor) scans col G for `[REPACKAGING SETTLEMENT EVENT]` rows and applies the settlement deterministically:
1. **Deplete inputs** from `offchain asset location` (col C)
2. **Add output locations** to `offchain asset location` (new rows, idempotent)
3. **Set Currencies metadata** (col C=TRUE, E–J, M=SKU via `--sku-mapping` substring match)
4. **Append structured audit row** to **`Repackaging Settlement`** tab on the ops sheet (`1qbZZhf…`)
5. **Mark col R** with `PROCESSED:REPACKAGING_SETTLEMENT` (dedup gate — future scans skip this row)

**Trigger:** The GAS public exec URL `?action=processPostRepackagingCleanup` (same deployment as the batch webhook). If the `DAO_PROTOCOL_WEBHOOK_POST_REPACKAGING_CLEANUP` env var is set on the Edgar/dao_protocol box, the dispatch layer fires it automatically on `submit_contribution`. Otherwise the GAS cron or a manual trigger (`doGet` with `?action=…`) is the fallback.

**Dedup convention (critical for all GAS handlers reading Telegram Chat Logs):**
- Processors scan **col G** for their event tag and **skip** rows where **col R** already has a `PROCESSED:<EVENT_TYPE>` marker.
- See `tokenomics/SCHEMA.md` column R for the full convention listing all known `PROCESSED:` markers.

---
## Cross-ledger conversions (managed AGLs) — upcoming

**Do not assume rules yet.** The user will define flows where inputs live on **managed ledgers** (e.g. **AGL13**: **bulk cacao nibs** → **packaged 200 g ceremonial**). Wait for explicit instructions (which spreadsheet, which `Currency`, how cost flows). Extend **this file** when those rules are provided.
