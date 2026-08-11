# Email360 — Plumbing Map, Ledger Integration & Loop Health

## 1. Plumbing Map

### Where customer emails enter

| Entry point | Mechanism | Destination |
|---|---|---|
| **QR scan** (bag traceback) | Customer optionally leaves email on `truesight.me/<sku>/<tree-id>` page | `Agroverse QR codes` tab on Main Ledger → column L (Owner Email) |
| **agroverse.shop checkout** | Shopify/Wix checkout collects email | Wix subscriber list → manually imported to `Agroverse News Letter Subscribers` (legacy rows have no Source) |
| **Email Agent Suggestions** | `go_to_market/scripts/` tools suggest emails from web research | `Email Agent Suggestions` tab on holistic workbook → synced daily by `newsletter_subscriber_sync.gs` |
| **Partnered Hit List** | Stores with Status = "Partnered" and a non-empty Email | `Hit List` tab on holistic workbook → synced daily by `newsletter_subscriber_sync.gs` |

### How emails land in the newsletter workbook

A daily Google Apps Script (`newsletter_subscriber_sync.gs`, scriptId `1XIz0hs7lH4DgjamUwQZeO4DwVTG8tqKjGElL9XB2StrkPXbHYeETOWBx`) runs on a time-driven trigger:

1. Reads `Agroverse QR codes` (Main Ledger) → extracts Owner Email (column L, fallback index 11)
2. Reads `Email Agent Suggestions` (holistic workbook `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`) → extracts `to_email` / `To` / `Email` column
3. Reads `Hit List` (same holistic workbook) → extracts Email only where Status = "Partnered"
4. Dedupes by `(normalized_email + Source)` — same email can appear once per source
5. Appends new rows to `Agroverse News Letter Subscribers` tab on the **Main Ledger** (`1GE7PUq-...`)
6. New rows get Status = `PENDING` (operator must manually confirm → `CONFIRMED`)

### The newsletter workbook (`1ed3q3SJ8ztGwfWit6Wxz_S72Cn5jKQFkNrHpeOVXP8s`)

This is the **canonical send + tracking log**, separate from the Main Ledger. It contains:

| Tab | Purpose | Source |
|---|---|---|
| **Agroverse News Letter Emails** | Send log + open/click tracking. One row per recipient per send. | Appended by `send_newsletter.py`; updated by Edgar `newsletter#open` and `newsletter#click` endpoints |
| **Agroverse News Letter Subscribers** | IMPORTRANGE mirror of the Main Ledger tab | `setup_newsletter_workbook_mirrors.py` writes `=IMPORTRANGE(...)` formula in A1 |
| **Agroverse QR codes** | IMPORTRANGE mirror of the Main Ledger tab | Same script |
| **Agroverse SKUs** | IMPORTRANGE mirror of the Main Ledger tab | Same script |
| **Currencies** | IMPORTRANGE mirror of the Main Ledger tab | Same script |
| **Email 360** | Cross-reference tab — enter an email in B2, spills newsletter sends, QR rows, SKUs, subscriber row, campaigns digest | Built by `setup_newsletter_workbook_mirrors.py` with FILTER formulas |
| **Workbook context** | Human-readable setup notes | Same script |

### Send flow (send_newsletter.py)

1. Operator runs `python3 scripts/send_newsletter.py --mode send --recipients-from-sheet --campaign X --body-md Y`
2. Script reads CONFIRMED subscribers from `Agroverse News Letter Subscribers` (Main Ledger)
3. Optionally excludes buyers of specific SKUs via `--exclude-buyers-of-substring` (reads `Agroverse QR codes` tab, checks Currency column against substring, drops matching Owner Emails)
4. For each recipient:
   - Generates a `message_uuid` (UUID4)
   - Builds MIME message with plain-text + HTML alternative
   - If `--track-opens` (default ON): appends an `<img>` tag pointing to `https://edgar.truesight.me/newsletter/open.gif?mid=<uuid>&r=<b64_recipient>`
   - If `--track-clicks` (default ON): rewrites each markdown link `[text](url)` to `https://edgar.truesight.me/newsletter/click?mid=<uuid>&r=<b64_recipient>&to=<b64_url>`
   - Sends via Gmail API (or creates draft in `--mode draft`)
   - Applies Gmail labels: per-campaign label + `DTC` audience label
5. Appends one row per send to `Agroverse News Letter Emails` tab on the newsletter workbook

### Tracking flow (Edgar — sentiment_importer)

| Endpoint | Trigger | Action |
|---|---|---|
| `GET /newsletter/open.gif?mid=<uuid>&r=<b64_recipient>` | Email client loads the embedded `<img>` | Calls `Gdrive::NewsletterEmails.record_open!` → updates columns H-K (opened, first_opened_at, last_opened_at, open_count) on the matching row. Returns 302 redirect to the Agroverse logo image. |
| `GET /newsletter/click?mid=<uuid>&r=<b64_recipient>&to=<b64_url>` | Recipient clicks a tracked link | Calls `Gdrive::NewsletterEmails.record_click!` → updates columns L-P (clicked, first_clicked_at, last_clicked_at, click_count, last_clicked_url). Returns 302 redirect to the original URL. |

Both endpoints:
- Skip all auth/rate-limiting before_actions (must work for anyone opening an email)
- Set `Cache-Control: no-store` so repeat opens register
- Silently return on unknown message_uuid (never 500 — broken tracking must not break the email)
- Use a mutex for thread safety on sheet writes

### The Email 360 cross-reference tab

Built by `setup_newsletter_workbook_mirrors.py`. When an email is typed into cell B2:

- **Column A (rows 5+):** FILTER of `Agroverse News Letter Emails` where recipient_email matches B2 — shows all sends, opens, clicks for that person
- **Column R (rows 5+):** FILTER of `Agroverse QR codes` where Owner Email matches B2 — shows all QR codes / bags associated with that email
- **Column AG (rows 5+):** FILTER of `Agroverse SKUs` where SKU code appears in the email's QR-derived unique SKU list — shows product info for what they bought
- **Column BD (rows 5+):** FILTER of `Agroverse News Letter Subscribers` where Email matches B2 — shows subscriber status
- **Cell C3:** TEXTJOIN of distinct campaign names for this email
- **Column DF (rows 5+):** Full mirror of `Currencies` tab for manual reference

### Cross-reference join logic

The Email 360 tab uses two join strategies for QR → SKU:

1. **Direct SKU match** (preferred): If both `Agroverse QR codes` and `Agroverse SKUs` have a recognizable SKU column header, it matches on SKU code directly.
2. **Ledger URL slug → Shipment** (fallback): If no SKU column is found, it extracts the slug from the QR's `ledger` URL (e.g. `https://agroverse.shop/agl4` → `agl4`) and matches against the SKUs `Shipment` column (e.g. `AGL4`).

---

## 2. Ledger Integration Answer

**Open question from GROWTH_MODEL.md:** *"Where exactly does Email360's data flow plug into the DAO ledger?"*

**Answer:** Email360 does **not** write to the DAO ledger via Edgar events. There is no `[CONTRIBUTION EVENT]`, `[INVENTORY MOVEMENT EVENT]`, or any other Edgar event type for email sends, opens, or clicks. The integration is **read-only from the ledger's perspective**:

- The Main Ledger is a **source** of subscriber emails (via `Agroverse News Letter Subscribers` tab) and product/SKU data (via `Agroverse QR codes` and `Agroverse SKUs` tabs)
- The newsletter workbook (`1ed3q3SJ8ztGwfWit6Wxz_S72Cn5jKQFkNrHpeOVXP8s`) is the **canonical write target** for all email activity
- The bridge between them is `IMPORTRANGE` formulas, not Edgar events
- Edgar's role is limited to serving tracking endpoints (`/newsletter/open.gif`, `/newsletter/click`) that update the newsletter workbook directly via the Sheets API

**Implication:** Email360 is a retention loop that operates *alongside* the DAO ledger but is not *integrated into* it. Email activity cannot be queried through Edgar, cannot trigger DApp bell notifications, and cannot be attributed to a contributor's TDG scoring. This is a design gap worth noting for future sprints.

---

## 3. Current-State Assessment

### What data exists today

| Data | Where | Completeness |
|---|---|---|
| Subscriber list with source attribution | `Agroverse News Letter Subscribers` (Main Ledger) | Good — emails from QR, Email Agent, Partnered stores. Status column (PENDING/CONFIRMED/TEST) but no unsubscribe tracking. |
| Send log (per-recipient, per-campaign) | `Agroverse News Letter Emails` (newsletter workbook) | Good — 47 rows as of last read. Columns: message_uuid, gmail_message_id, campaign, subject, recipient_email, sent_at_utc, status (draft/sent). |
| Open tracking | Same tab, columns H-K | Good — opened (TRUE/FALSE), first_opened_at, last_opened_at, open_count. Per-row granularity. |
| Click tracking | Same tab, columns L-P | Good — clicked (TRUE/FALSE), first_clicked_at, last_clicked_at, click_count, last_clicked_url. |
| Campaign grouping | Column C (campaign name) | Good — free-text campaign tag, consistent within each send. |
| QR code → email mapping | `Agroverse QR codes` (Main Ledger) | Good — Owner Email column links bags to customers. |
| SKU catalog | `Agroverse SKUs` (Main Ledger) | Good — Product ID, Name, Price, Shipment, GTIN. |

### What's missing

| Missing data | Why it matters |
|---|---|---|
| **Repeat purchase tracking** | No column links a newsletter send to a subsequent purchase. We can see "X opened the newsletter" and "X owns QR code Y" but cannot prove causation. |
| **Tree trace-back ID per customer email** | The QR code tab has `Owner Email` + `Currency` (product description), but there is no column storing a per-customer tree ID. The tree page URL is embedded in the QR's `landing_page` column but is a generic shipment page, not a per-customer tree page. |
| **Unsubscribe / bounce tracking** | No mechanism to record bounces, spam complaints, or unsubscribes. The subscriber list only grows. |
| **Email → Edgar event linkage** | No Edgar event is fired when an email is sent or opened. Cannot attribute email activity to a contributor's TDG score. |
| **Campaign-level aggregate metrics** | No pre-computed dashboard. Must manually FILTER the send log. |

---

## 4. Proposed Health Metrics

These can be computed from existing tabs **without any new data collection**. They measure whether the retention loop is working, not whether we're sending more email.

### Metric 1: Campaign Open Rate

**Formula:** `COUNTIF(opened=TRUE) / COUNTIF(status="sent")` per campaign

**Where:** `Agroverse News Letter Emails` tab, grouped by campaign (column C)

**What it tells you:** Whether subject lines and send timing are effective. A declining open rate suggests content fatigue or list decay.

**Current baseline (from the `two_bahia_bars` campaign):** 24 opened out of 39 sent = **61.5%** (excluding drafts and test sends to garyjob@gmail.com). This is a strong open rate for a first campaign.

### Metric 2: Campaign Click-Through Rate (CTR)

**Formula:** `COUNTIF(clicked=TRUE) / COUNTIF(opened=TRUE)` per campaign

**Where:** Same tab

**What it tells you:** Whether the content drove action. Low CTR with high open rate = interesting subject, weak body/call-to-action.

**Current baseline:** 4 clicked out of 24 opened = **16.7%** for `two_bahia_bars`. The clicked URLs were all product pages, suggesting product interest.

### Metric 3: Subscriber Re-engagement Rate

**Formula:** For recipients who received campaign N and also received campaign N+1, what fraction opened campaign N+1?

**Where:** Cross-reference `Agroverse News Letter Emails` against itself (same recipient_email across multiple campaigns)

**What it tells you:** Whether the loop retains attention across sends. If re-engagement rate drops below 40%, the list is decaying.

**Current state:** Only one campaign (`two_bahia_bars`) has been sent to the full list, so this metric has no baseline yet.

### Implementation note

These metrics should live in a new **Email 360 Health** tab on the newsletter workbook, computed from the existing `Agroverse News Letter Emails` data via `QUERY` or `FILTER` formulas. Do **not** recommend sending more email until the tracker exists — per the anti-pattern rule: "don't do more activity on an unmeasured surface."

---

## 5. Month-N Feasibility Verdict

**The "your tree at month N" push-back** (from GROWTH_MODEL.md §Trees Financed Dashboard Loop) proposes: *"monthly 'your tree at month N — here's a satellite update' email tied to each tree's traceback ID."*

### Verdict: NOT buildable with current data

### What's missing

To send a per-customer "your tree at month N" email, we need:

```
customer_email → tree_id → tree_status_at_month_N
```

Currently:

| Data | Exists? | Detail |
|---|---|---|
| Customer email → QR code | ✅ | `Agroverse QR codes` tab, Owner Email column |
| QR code → Currency (product description) | ✅ | Same tab, Currency column |
| QR code → ledger URL (shipment page) | ✅ | Same tab, `ledger` column (e.g. `https://agroverse.shop/agl4`) |
| QR code → tree ID | ❌ | The QR code's `landing_page` points to a **shipment** page (`/shipments/agl4`), not a per-customer tree page. There is no column storing a tree ID. |
| Customer email → tree ID | ❌ | No join table or column exists. |
| Tree ID → satellite update | ❌ | No tree-status data source exists (no satellite imagery pipeline, no tree-growth tracker). |

### What would need to change

**Minimum viable path:**

1. **Add a `tree_id` column** to `Agroverse QR codes` (or a new `customer_trees` tab) that maps each QR code to the specific tree it financed. This requires the tree-planting partner (e.g. Sun Mint) to provide per-tree IDs at the time of planting.

2. **Build a tree-status data source** — even a manual spreadsheet with tree age, species, and last-updated date would suffice for v0. Satellite imagery integration is aspirational.

3. **Extend `send_newsletter.py`** (or write a new script) to:
   - Query `Agroverse QR codes` for all trees owned by each recipient
   - Compute "month N" from the tree's planting date
   - Generate a personalized email body with tree status
   - Send via the existing Gmail + tracking pipeline

4. **Add a `tree_id` column to the `Agroverse News Letter Emails` tab** (or a separate join table) so future analysis can measure whether tree-status emails drive higher re-purchase rates than product-focused emails.

### Recommendation

Do not build month-N until:
- The tree-planting partner provides per-tree IDs (blocked on Sun Mint / Fazenda integration)
- At least one full cycle of the basic Email360 retention loop has been measured (see §4 health metrics)
- The subscriber list has >100 CONFIRMED emails (currently ~15 confirmed, ~30 total)

A more achievable v1 is **"your bag at month N"** — use the existing QR code creation date to compute how long ago the customer bought, and send a re-order reminder for the same SKU. This requires no new data columns, only a script change.

---

## Appendix: Key Files & Repos

| File | Repo | Purpose |
|---|---|---|
| `google_app_scripts/newsletter_subscriber_sync/newsletter_subscriber_sync.gs` | `tokenomics` | Daily GAS that pulls emails from QR codes, Email Agent Suggestions, and Partnered Hit List into the Main Ledger's `Agroverse News Letter Subscribers` tab |
| `scripts/send_newsletter.py` | `go_to_market` | Sends/drafts newsletters via Gmail API, logs to newsletter workbook, embeds tracking pixels/links |
| `scripts/setup_newsletter_workbook_mirrors.py` | `go_to_market` | Creates IMPORTRANGE mirrors + Email 360 cross-reference tab on the newsletter workbook |
| `scripts/migrate_newsletter_emails_sheet.py` | `go_to_market` | One-off migration of legacy send log from Main Ledger to dedicated workbook |
| `app/models/gdrive/newsletter_emails.rb` | `sentiment_importer` | Rails model that reads/updates the `Agroverse News Letter Emails` tab (used by Edgar tracking endpoints) |
| `app/controllers/newsletter_controller.rb` | `sentiment_importer` | Serves `/newsletter/open.gif` and `/newsletter/click` tracking endpoints |
| `config/routes.rb` | `sentiment_importer` | Routes for newsletter tracking endpoints |
| `GROWTH_MODEL.md` | `agentic_ai_context` | Growth model doc with Email360 retention loop section and open questions |

## Appendix: IMPORTRANGE Authorization Caveat

The `setup_newsletter_workbook_mirrors.py` script writes `=IMPORTRANGE(...)` formulas into the newsletter workbook using the `agroverse-market-research` service account. However, **IMPORTRANGE requires a one-time human click-through** to authorize access to the source spreadsheet. The service account cannot complete this. If the newsletter workbook's mirror tabs show `#REF!` errors, a human must open the workbook and click "Allow access" on each IMPORTRANGE prompt.
