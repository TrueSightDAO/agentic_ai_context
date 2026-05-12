# Partner Check-in Module — Implementation Plan

**Status:** v0.2 — implementation shipped (Kimi 2026-05-12) + review-pass (Claude 2026-05-12). See §14 for open review notes.
**Owner:** Agroverse / TrueSight (human: Gary + AI assist)  
**Last updated:** 2026-05-12

---

## 1. Problem Statement

Agroverse Partners (consignment / wholesale / popup) go quiet between restocks. Without periodic contact, partners run out of stock and do not re-order, which degrades sell-through velocity and leaves capital idle on their shelves. The existing tooling is **reactive** — `restock_recommender.html` triggers only when a partner texts us. We need a **proactive** lightweight system to:

1. Surface which partners likely need a "poke" (running low, out of stock, or dormant).
2. Log each poke as a signed, auditable event with notes, method, stock status, and next check-in date.
3. Show per-partner check-in history so operators don't re-poke blindly.

---

## 2. Design Principles

| Principle | Decision |
|-----------|----------|
| **Reuse existing infra** | Signed events → Edgar → Telegram Chat Logs → GAS scanner → Sheet. Same pipeline as `[RETAIL FIELD REPORT EVENT]`. |
| **One new DApp page** | `partner_check_in.html` — mobile-first, loads `partners-velocity.json` + `partners-inventory.json` for partner list and "needs poke" scoring. |
| **One new sheet tab** | `Partner Check-ins` on the **Main Ledger** (`1GE7PUq-…`). Source of truth for history. |
| **Extend existing GAS** | Add `get_partner_check_ins` action to the **Shipping Planner** API (`Routes.gas.shipping`). Avoids new clasp mirror + deployment URL. |
| **Scanner in existing project** | `process_partner_check_in_telegram_logs.gs` lives in `google_app_scripts/find_nearby_stores/` and deploys into the same clasp mirror as the retail field report scanner. |
| **CLI parity** | `dao_client check_in_partner` mirrors `update_store` so operators can log check-ins from terminal. |

---

## 3. Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Operator opens dapp/partner_check_in.html                               │
│  → loads partners-velocity.json (list)                                   │
│  → loads partners-inventory.json (stock levels)                          │
│  → calls Shipping Planner ?action=get_partner_check_ins (history)        │
│  → computes "needs poke" list client-side                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Operator selects partner, fills form, clicks "Log Check-in"             │
│  → RSA-signed [PARTNER CHECK-IN EVENT] POST to Edgar                     │
│  → Edgar verifies signature, appends to Telegram Chat Logs               │
│  → WebhookTriggerWorker enqueues GAS scanner                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  GAS scanner (find_nearby_stores mirror)                                 │
│  → reads Telegram Chat Logs for [PARTNER CHECK-IN EVENT]                 │
│  → dedup on Update ID                                                    │
│  → appends row to Main Ledger → Partner Check-ins tab                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. New Event Type — `[PARTNER CHECK-IN EVENT]`

### 4.1 Signed text format (DApp + CLI)

```text
[PARTNER CHECK-IN EVENT]
Partner ID: the-way-home-shop
Contributor Name: Gergana - The Way Home Shop
Check-in Date: 2026-05-12
Method: Text
Stock Status: Low
Restock Needed: Yes
Restock SKU: 8-ounce-organic-cacao-nibs
Restock Quantity: 12
Next Check-in Date: 2026-05-26
Notes: Gergana says sales slowed after the rainy season. Suggested a cacao circle demo.
Update ID: PCI_20260512120000_a1b2c3
--------
```

### 4.2 Field definitions

| Label | Required? | Source / validation |
|-------|-----------|---------------------|
| `Partner ID` | Yes | `Agroverse Partners`!A (slug). Must exist. |
| `Contributor Name` | Yes | `Contributors contact information`!A. Must match the partner's col E. |
| `Check-in Date` | Yes | ISO 8601 date (`YYYY-MM-DD`). Default: today. |
| `Method` | Yes | `Text` / `WhatsApp` / `Instagram` / `Facebook Messenger` / `Phone` / `Email` / `In Person` / `Other`. Dropdown on DApp. |
| `Stock Status` | Yes | `Low` / `Out` / `OK` / `Unknown`. Dropdown on DApp. |
| `Restock Needed` | Yes | `Yes` / `No` / `Maybe`. Dropdown on DApp. |
| `Restock SKU` | No | SKU slug drawn from `partners-velocity.json` items (e.g. `8-ounce-organic-cacao-nibs`), or `Other` if the partner asked for a SKU they don't currently carry. Only meaningful when `Restock Needed = Yes`. |
| `Restock Quantity` | No | Integer (units of `Restock SKU`). Only meaningful when `Restock Needed = Yes`. |
| `Next Check-in Date` | No | ISO 8601 date. Operator's commitment to re-poke. |
| `Notes` | No | Free-form remark. |
| `Update ID` | Yes | `PCI_<14-digit UTC timestamp>_<6-hex>` (e.g. `PCI_20260512120000_a1b2c3`). Dedup key. The hex suffix prevents same-second collisions during CLI batch use (backfill). |

### 4.3 Edgar dispatch

Edgar (`sentiment_importer/app/controllers/dao_controller.rb`) needs to:
1. Verify RSA signature.
2. Append payload to **Telegram Chat Logs** col G (same workbook `1qbZZhf-…`).
3. Enqueue `WebhookTriggerWorker` with action `processPartnerCheckInsFromTelegramChatLogs`.

**If Edgar does not yet recognize this event type**, the generic `submit_contribution` endpoint still works (it logs any signed text to Telegram Chat Logs). The scanner picks it up by scanning for the `[PARTNER CHECK-IN EVENT]` header. However, adding explicit routing in Edgar's `WebhookTriggerWorker` is cleaner. For MVP, we rely on the generic path + cron safety net.

---

## 5. New Sheet Tab — `Partner Check-ins`

### 5.1 Location

**Main Ledger** (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`) — new tab.

### 5.2 Columns

| Col | Header | Type | Notes |
|-----|--------|------|-------|
| A | `Submitted At` | ISO 8601 datetime | When the scanner appended the row. |
| B | `Partner ID` | String | Slug from `Agroverse Partners`!A. |
| C | `Contributor Name` | String | From `Contributors contact information`!A. |
| D | `Check-in Date` | Date (`YYYY-MM-DD`) | When the check-in happened. |
| E | `Method` | String | Dropdown: `Text`, `Phone`, `In Person`, `Email`, `Other`. |
| F | `Stock Status` | String | Dropdown: `Low`, `Out`, `OK`, `Unknown`. |
| G | `Restock Needed` | String | Dropdown: `Yes`, `No`, `Maybe`. |
| H | `Restock Quantity` | Number | Integer (nullable). |
| I | `Next Check-in Date` | Date (`YYYY-MM-DD`) | Operator's scheduled follow-up (nullable). |
| J | `Notes` | String | Free-form, capped at 2000 chars by scanner. |
| K | `Update ID` | String | `PCI_…` — dedup key. Unique constraint (scanner-enforced). |
| L | `Digital Signature` | String | Public key (first 64 chars) of the signer. |
| M | `Submitted By` | String | Resolved contributor name from signature lookup. |
| N | `Restock SKU` | String | SKU slug (or `Other`). Nullable. Only meaningful when `Restock Needed = Yes`. Appended at col N (not inserted at H) so existing cols A–M dedup/lookup logic stays intact. |

### 5.3 Scanner behavior

- **Idempotent**: dedup on `Update ID` (col K). Re-runs skip already-recorded IDs.
- **Locking**: `LockService.getScriptLock()` for 180s, same as retail field report scanner.
- **Scan window**: trailing 200 rows of Telegram Chat Logs (same batch size).
- **Error handling**: malformed rows are skipped and logged; valid rows are committed.

---

## 6. DApp Page — `partner_check_in.html`

### 6.1 Layout (mobile-first)

```
┌─────────────────────────────────────┐
│  Partner Check-in                   │
│  ———                                │
│  [🔍 Search partner…       ]        │
│                                     │
│  ┌─ Needs Attention (3) ─┐         │
│  │ ⚠️ The Way Home Shop   │         │
│  │    1 bag left · last   │         │
│  │    sale 48 days ago    │         │
│  │    [Log check-in]      │         │
│  │ …                      │         │
│  └────────────────────────┘         │
│                                     │
│  ─── All Partners ───               │
│  [Partner dropdown]                 │
│                                     │
│  ┌─ History ─┐                      │
│  │ 2026-05-01 Text · Low │          │
│  │ "Sales slowed…"        │          │
│  └───────────┘                      │
│                                     │
│  ─── Log Check-in ───               │
│  Check-in Date: [2026-05-12]        │
│  Method: [Text ▼]                   │
│  Stock Status: [Low ▼]              │
│  Restock Needed: [Yes ▼]            │
│  Restock Qty: [12      ]            │
│  Next Check-in: [2026-05-26]        │
│  Notes: [_______________]           │
│                                     │
│  [Submit Check-in]                  │
│  (requires digital signature)       │
└─────────────────────────────────────┘
```

### 6.2 "Needs Attention" scoring (client-side)

For each partner in `partners-velocity.json`:

1. **Load inventory** from `partners-inventory.json`.
2. **Load history** from Shipping Planner `get_partner_check_ins`.
3. **Compute flags**:
   - `inventory === 0` → **Out of stock** (critical)
   - `inventory <= 3 && monthly_rate > 0` → **Running low** (warning)
   - `last_sale_date && daysSince(last_sale_date) > 45` → **Dormant** (info)
   - `next_check_in_date && next_check_in_date <= today` → **Overdue** (warning)
4. **Sort**: Out of stock → Running low → Overdue → Dormant.

### 6.3 Signature-gated submit

Same pattern as `store_interaction_history.html`:
- Read-only mode if no `localStorage.publicKey`.
- Form fields disabled; banner prompts signature creation.
- Submit signs the event text with `RSASSA-PKCS1-v1_5` + SHA-256.
- POSTs multipart to `EdgarClient.submit` endpoint.

### 6.4 Deep-linking

URL param `?partner_id=the-way-home-shop` pre-selects the partner (refresh-safe).

---

## 7. GAS Scanner — `process_partner_check_in_telegram_logs.gs`

### 7.1 File location

- **Canonical**: `tokenomics/google_app_scripts/find_nearby_stores/process_partner_check_in_telegram_logs.gs`
- **Mirror**: `tokenomics/clasp_mirrors/1NpHrKJW…/process_partner_check_in_telegram_logs.js`
- **Dispatch branch** in mirror `Code.js`:

```javascript
if (e.parameter.action === 'processPartnerCheckInsFromTelegramChatLogs') {
  var out = processPartnerCheckInsFromTelegramChatLogs();
  return ContentService.createTextOutput(JSON.stringify(out)).setMimeType(ContentService.MimeType.JSON);
}
```

### 7.2 Parser

`parsePartnerCheckInText_(text)` — mirrors `parseRetailFieldReportText_`:
- Splits on `--------`.
- Extracts `Label: Value` lines.
- Lowercases + snake-cases labels.
- Returns key→value map.

### 7.3 Sheet append

`appendPartnerCheckInRow_(fields)` — appends one row A–M to `Partner Check-ins`.

### 7.4 Cron safety net

Time-driven trigger: every 30 minutes on `processPartnerCheckInsFromTelegramChatLogs`.

---

## 8. Shipping Planner API Extension

### 8.1 New actions in `shipping_planner_api.gs`

#### `get_partner_check_ins`

```
GET ?action=get_partner_check_ins&partner_id=the-way-home-shop
```

Returns `{ status: 'success', data: { partner_id, check_ins: [...] } }`.

- Reads `Partner Check-ins` tab on Main Ledger.
- Filters by `Partner ID` (col B).
- Sorts by `Check-in Date` descending.
- Caps at 50 rows.

#### `list_partners_needing_attention`

```
GET ?action=list_partners_needing_attention
```

Returns `{ status: 'success', data: { partners: [...] } }`.

- Reads `Partner Check-ins` tab for latest check-in per partner.
- Reads `Agroverse Partners` for active partner list.
- Returns partners whose `Next Check-in Date` has passed or is within 3 days.
- **Note**: Full "out of stock / running low / dormant" scoring stays client-side (the DApp has `partners-inventory.json` + `partners-velocity.json`). This action is a lightweight server-side fallback.

### 8.2 Mirror sync

```bash
cd tokenomics/
cp google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs \
   clasp_mirrors/1Og2g8Q0_SdM9A5mJNO-tq_9r8XMQ00ybBmss4L3tItBAJ01-KdM-w40c/Code.js

cd clasp_mirrors/1Og2g8Q0_SdM9A5mJNO-tq_9r8XMQ00ybBmss4L3tItBAJ01-KdM-w40c/
clasp push
clasp deploy --deploymentId <existing> --description "Add partner check-in actions"
```

**Note**: `shipping_planner_api.gs` is canonical; `Code.js` in the mirror is gitignored. The `.gs` → `.js` copy is a one-time manual step at deploy time.

---

## 9. dao_client CLI Module — `check_in_partner.py`

### 9.1 Usage

```bash
python3 -m truesight_dao_client.modules.check_in_partner \
  --partner-id the-way-home-shop \
  --contributor-name "Gergana - The Way Home Shop" \
  --method Text \
  --stock-status Low \
  --restock-needed Yes \
  --restock-quantity 12 \
  --next-check-in-date 2026-05-26 \
  --notes "Sales slowed after rainy season."
```

### 9.2 Fields

Same as DApp form. `--partner-id` and `--contributor-name` are required. `--check-in-date` defaults to today. `--update-id` auto-generates `PCI_<timestamp>`.

---

## 10. Files to Create / Modify

### New files

| File | Purpose |
|------|---------|
| `agentic_ai_context/PARTNER_CHECK_IN_IMPLEMENTATION.md` | This plan. |
| `dapp/partner_check_in.html` | DApp page. |
| `tokenomics/google_app_scripts/find_nearby_stores/process_partner_check_in_telegram_logs.gs` | GAS scanner (canonical). |
| `tokenomics/google_app_scripts/find_nearby_stores/process_partner_check_in_telegram_logs.js` | Mirror copy (gitignored, for clasp). |
| `dao_client/truesight_dao_client/modules/check_in_partner.py` | CLI module. |

### Modified files

| File | Change |
|------|--------|
| `dapp/menu.js` | Add `Partner Check-in` nav entry under "Retail & field activity". Bump `?v=` query. |
| `dapp/routes.js` | No change — reuses `Routes.gas.shipping` and `Routes.edgar.submit`. |
| `tokenomics/google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs` | Add `get_partner_check_ins` and `list_partners_needing_attention` actions. |
| `tokenomics/clasp_mirrors/1Og2g8Q0…/Code.js` | Add `get_partner_check_ins` branch to `doGet`. |
| `tokenomics/clasp_mirrors/1NpHrKJW…/Code.js` | Add `processPartnerCheckInsFromTelegramChatLogs` dispatch branch. |
| `tokenomics/SCHEMA.md` | Document `Partner Check-ins` tab columns A–M. |

### Manual setup (not in repo)

| Step | Who |
|------|-----|
| Create `Partner Check-ins` tab on Main Ledger with headers A–**N** (note: `Restock SKU` is col N, added per v0.2). | Operator (Gary) |
| Add dropdown validations for Method, Stock Status, Restock Needed. | Operator |
| Add time-driven trigger for `processPartnerCheckInsFromTelegramChatLogs` (30 min). | Operator |
| Deploy Shipping Planner web app with new version. | Operator |
| Update Edgar's `WebhookTriggerWorker` to enqueue partner check-in scanner (optional — cron safety net covers it). | Dev (future) |

---

## 11. Testing Checklist

### 11.1 DApp page

- [ ] Load `partner_check_in.html` without signature → read-only, banner shows.
- [ ] Create signature → form enables.
- [ ] Partner dropdown populates from `partners-velocity.json`.
- [ ] "Needs Attention" section surfaces partners with low inventory.
- [ ] Select partner → history loads from `get_partner_check_ins`.
- [ ] Fill form → submit → Edgar returns 200.
- [ ] Deep link `?partner_id=the-way-home-shop` pre-selects partner.

### 11.2 GAS scanner

- [ ] Run `processPartnerCheckInsFromTelegramChatLogs` manually → processes 0 rows if no events.
- [ ] Submit one event via DApp → scanner appends 1 row to `Partner Check-ins`.
- [ ] Re-run scanner → same event skipped (dedup on Update ID).
- [ ] Check lock service: concurrent runs don't race.

### 11.3 Shipping Planner API

- [ ] `?action=get_partner_check_ins&partner_id=the-way-home-shop` returns rows.
- [ ] `?action=list_partners_needing_attention` returns partners with overdue next check-in.

### 11.4 CLI

- [ ] `python3 -m truesight_dao_client.modules.check_in_partner --dry-run` prints signed text.
- [ ] `--execute` POSTs to Edgar, scanner picks it up.

---

## 12. Future Enhancements (out of scope for v1)

- **Email reminder**: GitHub Action reads `Partner Check-ins` tab daily and emails operator a "partners needing attention" digest.
- **Partner self-check-in**: Partners text a keyword (e.g. "RESTOCK") to a Twilio number, which Edgar turns into an unsigned `[PARTNER CHECK-IN EVENT]`.
- **Auto-restock**: When `Restock Needed = Yes` + `Restock Quantity` is set, auto-populate `restock_recommender.html` with that quantity.

---

## 13. Changelog

- **2026-05-12** — v0.1 drafted (Kimi).
- **2026-05-12** — v0.2 review-pass (Claude):
  - Fixed contributor-name auto-fill in `dapp/partner_check_in.html` — removed `partner_name` fallback that reproduced the The Way Home Shop col-T-clear / Edgar auto-rename incident from 2026-04-28. Field now stays blank when `contributor_contact_id` is absent (which is currently always — that field doesn't exist in `partners-velocity.json` yet) and prompts the operator for the canonical `First Name - Store Name` format.
  - Added `_<6-hex>` suffix to Update ID in DApp + CLI (`PCI_<ts>_<6-hex>`) to prevent same-second collisions during CLI batch use.
  - Added `Restock SKU` field (col N) through DApp form (select populated from `velocity.partners[slug].items` + `Other` fallback), CLI `--restock-sku`, event text format, GAS scanner append, sheet schema, Shipping Planner API lookup. Unlocks the §12 "Auto-restock" future enhancement (wiring `Restock Needed = Yes` + `Restock SKU` + `Restock Quantity` into the Restock Recommender) without a future schema migration.

---

## 14. Open Review Notes (Claude, 2026-05-12)

Items surfaced by the review-pass. Items 1–3 have been implemented in v0.2; items 4–7 remain.

### Resolved in v0.2

1. **[blocking-for-go-live] Contributor Name auto-fill was actively wrong.** `partners-velocity.json` has zero `contributor_contact_id` occurrences (verified), so the original fallback to `partner_name` (e.g. `"Edge and Node, House of Web3"`) would silently pre-fill a non-canonical name and reproduce the The Way Home Shop incident on the first check-in. Fixed — field stays blank, placeholder + hint point to canonical format.

2. **[polish-for-v1.1, applied now] Update ID `PCI_<14-digit ts>` collides for batch CLI use.** Two events in the same second silently dedup to one. Won't bite human DApp flow; will bite scripted backfills. Fixed — both DApp and CLI now generate `PCI_<ts>_<6-hex>`.

3. **[polish-for-v1.1, applied now] Restock Quantity had no SKU.** Single integer was meaningless across multi-SKU partners. Added `Restock SKU` as col N (append, not insert, to avoid disrupting existing cols A–M).

### Open (not yet addressed)

4. **[blocking-for-observability] `ADVISORY_SNAPSHOT.md` does not pull from `Partner Check-ins`.** The original motivation for this build was that LLM advisors couldn't see Gary's offline outreach. Until the snapshot generator (`market_research` / `agentic_ai_context` advisory pipeline) reads the new tab and surfaces a rollup (e.g. "last 14 days of check-ins by partner"), advisors still won't anchor on this data — they'll keep recommending generic outreach actions. Tracked in `agentic_ai_context/OPEN_FOLLOWUPS.md`.

5. **[polish] `Notes` 2000-char cap (scanner-side).** Tight if operators capture both context and decision in one note. Bump to 4000+ when convenient.

6. **[polish] Hit List vs Partner Check-in seam isn't documented.** Pre-Partnered prospect conversations live in DApp Remarks (Hit List); post-Partnered check-ins live here. Worth one sentence in §1 saying these are intentionally separate, so a future LLM doesn't try to unify them prematurely.

7. **[polish] `PROJECT_INDEX.md` and `WORKSPACE_CONTEXT.md` don't yet point at this surface.** A new event type + sheet tab + DApp page warrants pointer lines in both so future onboarding AIs find it. Low-priority but cheap.

### Operational gotchas to surface to operators (not in code yet)

- **Tab creation must precede the first clasp-push of the scanner.** Otherwise the first `processPartnerCheckInsFromTelegramChatLogs` run will call `ensurePartnerCheckInsSheet_` and create the tab with the v0.2 headers including `Restock SKU` at col N — which is correct, but means dropdown validations Gary adds manually must be applied *after* the auto-create. Order: clasp-push → run scanner once manually → operator adds dropdown validations + col widths.
- **`contributor_contact_id` enrichment is the path to make auto-fill actually work.** Until `market_research/scripts/sync_partners_velocity.py` joins `Agroverse Partners`!E into the output JSON, every check-in submission requires manual typing of the canonical name. Worth queuing as its own follow-up.

---
