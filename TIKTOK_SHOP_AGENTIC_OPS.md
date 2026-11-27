# TikTok Shop — manual-first agentic ops experiment

**Status:** compiled 2026-11-28 (Sophia Truesight). Manual-first in progress; API registration blocked.
**Governor:** Gary Teh · **Track owner:** Envoy (Jira) / Sophia (execution)
**Epic:** [KAN-112](https://truesightdao.atlassian.net/browse/KAN-112) — Agroverse US DTC: TikTok agentic ops experiment
**Audience:** future AI agents and humans picking this up cold.

---

## 1. Why this is manual-first

The obvious architecture is: TikTok Shop API → orders → ledger. That path is **blocked twice over**, and both blocks are TikTok-side, not ours.

| Wall | Detail |
|---|---|
| **AM gate** | Registering as a **seller (in-house) developer** at `partner.us.tiktokshop.com` returns *"Account ineligible for seller developer registration — only sellers with an assigned account manager (AM) can register."* AM assignment is itself a growth-tier reward. |
| **Rate limit** | Falling back to **ISV** registration hit a signup rate limit. |

Root cause of hitting the AM gate at all: an email already tied to a seller account is **routed to the seller-developer path only** — you never get offered the ISV path. Registering under a fresh, non-shop email is the documented way to reach `developer type = ISV`.

**Decision:** don't block the commercial experiment on a TikTok org-chart decision. Run the experiment manually now; keep the API registration running in parallel (KAN-118).

### The API track, so nobody re-runs the same failure

- Register ISV at `partner.us.tiktokshop.com` (US market — `partner.tiktokshop.com` is rest-of-world) using an email that has **never touched a TikTok Shop**.
- Create app type **Custom** (not Public — public means App Store listing + multi-week review).
- Enable scopes: **Shop Authorized Information**, **Order Information**, **Product Basic** (+ Finance optional).
- Capture **App Key / App Secret / Service ID**. Secret goes to the vault — never a repo, never an env file, never chat.
- Authorization: `https://services.us.tiktokshop.com/open/authorize?service_id=<SERVICE_ID>&state=<single-use>` → returns `code` (30 min, single-use) → exchange at `GET https://auth.tiktok-shops.com/api/v2/token/get` (`app_key`, `app_secret`, `auth_code`, `grant_type=authorized_code`).
- Business calls: `https://open-api.tiktokglobalshop.com`, with `app_key`, `timestamp` (10-digit Unix **seconds**), `sign` query params + `x-tts-access-token` header. `sign` = hex HMAC-SHA256 over `app_secret + path + sorted-params + body`, keyed with `app_secret`.
- **Access token lives 7 days.** Any integration needs a scheduled refresh loop or the channel dies weekly. Design this in, don't bolt it on.
- Live shop likely can't authorize a development app; test against a **Development Shop** test account until review clears.

⚠️ Do **not** conflate this with the **TikTok Content Posting API** (`developers.tiktok.com`) — separate product, separate app, separate review. See `MEDIA_ARCHIVE_PIPELINE.md`, which treats TikTok as a media *distribution* consumer.

---

## 2. Where the tracking lives

**Canonical content spreadsheet:** `1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ`

TikTok was added as three tabs **inside the existing content workbook**, beside `Instagram Content Schedule` and friends — not in a new silo. TikTok is a content channel; its ops belong with content ops.

### `TikTok Content Schedule`
Mirrors the Instagram tab's shape so anyone who knows one knows the other.
`primary_key · status · Week · Date Range · Theme Focus · Post Day · Day of Week · Post Type · Theme · Description · Caption · Hashtags · CTA · Sound / Audio · Tool Suggestions · Published Video URL · Posted By · Shop Product Tagged · Experiment Arm · Notes`

### `TikTok Video Metrics`
Leading indicators — explicitly **not** the success metric.
`snapshot_date · primary_key · video_url · views · likes · comments · shares · saves · avg_watch_secs · followers_gained · profile_visits · product_clicks · shop_orders_attributed · notes`

### `TikTok Orders`
The outcome. This tab is what makes the experiment measurable.
`order_date · tiktok_order_id · sku · qty · gross_revenue_usd · status · attributed_primary_key · attributed_video_url · customer_note · ledger_row_ref`

**Why Orders is a separate tab from Metrics:** it structurally prevents the classic error of concluding "the video did well, therefore it sold product." Views live in one place, money in another. You can't accidentally read one as the other.

---

## 3. Experiment arms

Recorded in the spreadsheet's `Configuration` tab alongside the status vocabulary.

| Arm | Setup | What it isolates |
|---|---|---|
| **A** | Listening only — no product tags | Organic discovery baseline |
| **B** | Product tagged on a **new** video | Tag lift on fresh content |
| **C** | Product tagged on an **existing high-performing** video | Retro-tag lift (uses KAN-115's top videos) |

A is the control. Without it, B and C have no denominator and any lift is unattributable.

---

## 4. The success metric (KAN-119)

**Primary:** TikTok Shop attributed **orders and gross revenue** — read off the `TikTok Orders` tab — over a **2–4 week** window.

**Explicitly not a metric:** views, likes, comments, shares, followers. These are recorded in `TikTok Video Metrics` as leading indicators only. Engagement is a hypothesis about the path to revenue, not the goal.

**Attribution rule (must not be fudged):** an order counts toward an arm only if (a) a real `tiktok_order_id` exists in Seller Center, **and** (b) `order_date` falls inside that arm's window. "I think that sale came from TikTok" does not count. This rule exists because it is the single easiest place to accidentally lie to ourselves.

---

## 5. Logging cadence

Deliberately minimal. A cadence that isn't kept is worse than no cadence — it produces a sparse table that looks like data.

| When | Time | What |
|---|---|---|
| **Daily** | ~5 min | New orders → `TikTok Orders`. Snapshot `TikTok Video Metrics` for videos posted in the last 7 days. |
| **Weekly (Mon)** | ~15 min | Full metrics snapshot for **all** live videos. Status sweep on `TikTok Content Schedule`. |

---

## 6. Pre-existing drift found while verifying (NOT fixed — out of scope)

Flagged because it affects whether any comparison is trustworthy:

- **`Published Content Index` holds only 2 data rows** despite the org having far more published assets.
- **`F5 Content Schedule` is header-only** (0 rows) — the forward calendar is effectively empty.
- **Instagram tab status vocabulary is inconsistent:** it uses `PROPOSED` and `SUPERSEDED`, neither of which appears in `Configuration`'s "Instagram Reel Status" list; and **182 of 245 rows have a blank status**.

**Consequence:** do **not** use the Instagram tab's status counts as a reliable denominator for any TikTok-vs-Instagram comparison. TikTok is being tracked cleanly from day one rather than inheriting this. Worth its own follow-up if comparisons matter.

---

## 7. Task map

| Key | Task | Blocked on |
|---|---|---|
| KAN-113 | List 1–3 existing Agroverse products manually in Seller Center | Gary (manual) |
| KAN-114 | Tracking tab + manual logging cadence | ✅ **Built.** Data entry ongoing. |
| KAN-115 | Performance data on ~18+ existing @thecacaofanatic videos | Gary supplies raw numbers; Sophia analyses |
| KAN-116 | New content matched to existing account voice | KAN-115 |
| KAN-117 | Tag products in new + existing high-performing videos | KAN-113, KAN-115 |
| KAN-118 | API registration (ISV + AM request) | TikTok rate limit / AM gate |
| KAN-119 | Define + track the real success metric | ✅ defined; needs order data |
