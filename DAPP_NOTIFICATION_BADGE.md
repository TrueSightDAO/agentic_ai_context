# DApp Notification Badge

Shared red-counter widget loaded on every DApp page that surfaces
pending action items the operator hasn't addressed yet, without
requiring them to open each module to check. Modeled on the
Facebook-style top-right bell icon.

This file is the contract: how the widget works, what shape a
notification source must return, how to add a new module, and which
modules are wired today.

---

## Why this exists

Before the badge, checking on pending work meant opening
`warmup_review.html`, `partner_check_in.html`, possibly
`view_open_proposals.html`, and a few others — each in a separate
tab — to see whether anything had piled up. With ~33 DApp pages and
several producing action items, that's friction the operator hits
every session.

The badge collapses *"where do I look next?"* into one fixed-position
glance.

The architecture is also a deliberate guard against an anti-pattern
documented in `feedback_check_tracking_before_recommending_action.md`:
surfaces that nag the operator about activity they're already doing
(or that's gated behind an intentional cadence rule) erode trust in
the badge and push noise. Every source registered here must answer
"the operator's review/action is the bottleneck on this item" — not
"the queue has rows in it."

---

## Where the widget lives

- **Implementation:** `dapp/js/notifications.js`
- **Bootstrap:** `dapp/menu.js` async-injects `notifications.js` after
  rendering the nav. Since `menu.js` is loaded by all ~33 DApp pages,
  one upstream change covers everywhere.
- **Mount point:** the widget self-creates a fixed-position root
  (`#tsd-notif-root`) appended to `<body>` on each page. No per-page
  HTML changes required.
- **Cache:** both `menu.js` and `notifications.js` are versioned via
  `?v=YYYYMMDD<x>` query strings. Bump both when changing either file
  (and update `service-worker.js`'s `URLS_TO_CACHE` to match).

---

## The notification-source contract

Every module is a **source** registered via:

```js
Notifications.register({
  id: 'my_module',
  fetch: function () { return /* Promise<Result | null> */; }
});
```

`fetch()` must return (sync or as a Promise) **one of**:

- **`null`** — module is silently hidden from the badge and popup.
  Use for: source can't fetch, returns an empty result, GAS action
  not yet deployed, or the cadence rule says nothing's due.
- **An object** of this shape (the **Result**):

```js
{
  count: 3,                                 // integer added to the red badge total
  label: 'Outbound Review',                 // module name shown in popup
  sublabel: '3 follow-up · 2 warm-up',      // short context shown under the label
  link: './warmup_review.html',             // deep link when the operator clicks the row
  items: [                                  // optional, top N items shown nested
    { title: 'Tech Spot', link: '...', since: '14d overdue' },
    { title: 'Beanery',   link: '...', since: 'due today' }
  ]
}
```

Rules of thumb:
- **`count`** is what the operator sees. Match it to *items the
  operator can move forward on* — not raw queue depth.
- **`sublabel`** is one line of context. Use it to explain the count
  ("12 overdue · 4 upcoming"), not to repeat the module name.
- **`items`** is optional and capped at 4 in the popup. Use it when
  the operator can usefully act on individual rows; omit it for
  modules that surface a single aggregate.
- **`since`** on an item is freeform — typical values: `Nd overdue`,
  `due today`, `due in Nd`, `awaiting reply 3d`.

Sources fire in parallel on page load and on every refresh
(currently every 5 minutes). A source that throws is logged to the
console and treated as `null`. The badge total is the sum of `count`
across non-null sources.

---

## How to add a new module

Three steps:

1. **Identify the data source.** Ideally an existing GAS action
   returning a list of action items. If you have to add a new GAS
   action, make sure it's filterable to "operator's bottleneck"
   items, not raw queue depth.
2. **Write a `fetch` function** in `dapp/js/notifications.js` that
   calls the data source and shapes the response into the Result
   contract. Return `null` if no items.
3. **Register it** via `Notifications.register({...})` in the same
   file. The widget rerenders automatically.

After editing, bump the `?v=` query on both `menu.js` and
`notifications.js` (in `menu.js`, in `service-worker.js`
URLS_TO_CACHE, and across all DApp HTML pages for the `menu.js` ref
— sed across `*.html` is the standard move). Otherwise PWA users
keep serving the cached old version.

---

## Modules wired (as of 2026-05-12)

### Outbound Review

- **Source:** `Routes.gas.storesHitList?action=getWarmupReviewQueue`
  (same endpoint `warmup_review.html` already calls — no new GAS).
- **Count:** sum of three cohorts the GAS pre-categorizes:
  `AI/Warm-up + AI/Follow-up + AI/Prospect Replied`. These cohort
  labels are themselves the cadence-gate output, so counting them
  doesn't violate the anti-pattern — the gate has already filtered.
- **Sublabel:** breakdown like `"3 prospect replied · 4 follow-up · 5 warm-up (drafts to review)"`.
- **Link:** `./warmup_review.html`.

### Partner Check-in follow-ups

- **Source:** `Routes.gas.shipping?action=list_partners_needing_attention`
  (already live in `tokenomics/google_app_scripts/tdg_shipping_planner/shipping_planner_api.gs`,
  function `listPartnersNeedingAttention`).
- **Cadence rule:** **operator-driven**, not metric-driven. The
  Partner Check-in form captures a `Next Check-in Date` per filing;
  the GAS surfaces partners whose Next Check-in Date is today or
  earlier, plus those within the next 3 days. The operator picks
  the cadence one check-in at a time.
- **Count:** total partners returned (overdue + upcoming-within-3-days).
- **Sublabel:** `"N overdue · M upcoming"` when both are present,
  otherwise the appropriate singular.
- **Items:** top 4 partners, sorted most-overdue first. Partner
  names resolved by joining the GAS response's `partner_id` slug
  against the live
  [`partners-velocity.json`](https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/partners-velocity.json)
  — cached per page load.
- **Link:** `./partner_check_in.html`.

Why this design wins on anti-pattern grounds: the badge does not
recommend follow-ups. It echoes back the reminders the operator
already set on themselves. That respects
`feedback_check_tracking_before_recommending_action.md` exactly.

### Partner Stock attention

- **Source:** two static GitHub-hosted JSONs, both cached for the
  lifetime of the page:
  - [`partners-velocity.json`](https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/partners-velocity.json)
    — last_sale_date per SKU per partner
  - [`partners-inventory.json`](https://raw.githubusercontent.com/TrueSightDAO/agroverse-inventory/main/partners-inventory.json)
    — venueInventory per SKU per partner
- **Scoring rules** (lifted verbatim from
  `dapp/partner_check_in.html`'s `computeAttentionList()` so the bell
  stays in sync with the page's 'Needs Attention' section):
  - **critical**: `totalInv == 0` → 'out of stock'
  - **warning**: `totalInv <= 3` → 'running low (N left)'
  - **info**: any SKU `last_sale_date > 45d` → 'dormant'
- **Filter:** retail-type partners only (`Consignment | Wholesale`).
  Cooperative slugs (containing `/`) and supplier-type partners are
  skipped.
- **Count:** total partners flagged across all three severities.
- **Sublabel:** `"N out of stock · M low stock · K dormant"`,
  including only the non-zero buckets.
- **Items:** top 4 partners, sorted critical → warning → info, then
  alphabetical.
- **Link:** `./partner_check_in.html` (the page already renders the
  same list in its 'Needs Attention' section, with a 'Log check-in'
  CTA per partner).

Why this is a separate source from Partner Check-in follow-ups:
the two answer different operator questions.

| Source                          | Signal type                     | Data source                          | Returns null when                                  |
|---------------------------------|---------------------------------|--------------------------------------|----------------------------------------------------|
| `partner_followups`             | Operator-driven cadence         | GAS `list_partners_needing_attention`| No check-ins have matured a Next-Check-in Date     |
| `partner_stock`                 | Business-driven urgency         | velocity + inventory static JSONs    | All retail partners have stock + recent sales      |

Both can fire on the same partner. That's by design — they represent
independent reasons to act. Keeping them separate means tuning one
rule doesn't risk dragging the other.

The single 'Partner Stock' label in the popup keeps the operator
mental model simple even though the underlying severity is
three-way. The sublabel surfaces the split.

---

## Refresh cadence

- Badge auto-refreshes every **5 minutes** from page load.
- A registered source's `fetch()` is called once per refresh.
- The `partners-velocity.json` join is cached for the lifetime of
  the page — so partner-name lookups are free after the first
  refresh.
- Refresh on demand: `Notifications.refresh()` from the console
  (e.g. after filing a check-in, to confirm the badge updates).

---

## Future modules — candidates worth wiring

In rough priority order, based on operator action surfaces that
exist today:

| Module                                  | Status                                      | Notes |
|-----------------------------------------|---------------------------------------------|-------|
| Currency-conversion records missing receipt | Not wired                              | Needs a sheet column / GAS action to surface conversions without an attached receipt URL. |
| DAO proposals nearing 7-day vote close  | Not wired                                   | `Routes.gas.proposals` likely exposes a list; need to add an action that filters to "voting closes within 24h." |
| Inventory-shipment exceptions           | Not wired                                   | Surfaces movements stuck in transit beyond an expected SLA. Would draw on the shipping planner sheet. |
| Tree-planting registrations awaiting verification | Not wired                         | Sunmint program — likely a `verification_status = pending` filter on the registrations sheet. |
| Beer Hall daily digest failure          | Not wired                                   | An infra-health signal, surfacing when yesterday's digest failed to generate. |

Add modules one at a time. Resist the temptation to wire 5 at once —
the badge's value comes from each module being trusted, and each
new module needs a week of observation before scope expands.

---

## Operator UX

- **Bell icon** sits fixed top-right (`position: fixed; top: 0.75rem; right: 0.75rem`),
  inside its own `<div id="tsd-notif-root">` to avoid colliding with
  existing page layouts.
- **Red badge** appears only when `total > 0`. Shows `99+` for very
  large totals.
- **Click bell** to toggle popup. **Click outside** to dismiss.
- Popup shows modules with `count > 0` only. Empty state:
  "No pending action items."
- Each module row is a deep link — click anywhere on the row to
  navigate to the module's page.

---

## Related context

- `feedback_check_tracking_before_recommending_action.md` — the
  anti-pattern this widget is designed not to commit.
- `project_partner_check_in_2026-05-12.md` — the Partner Check-in
  surface that supplies module 2's data.
- `PARTNER_CHECK_IN_IMPLEMENTATION.md` (in this directory) — the
  canonical implementation doc for the Partner Check-in surface.
- `NOTES_dapp.md` — top-level DApp working notes (this widget is
  cross-referenced from there).
- `tokenomics/API_ENDPOINTS.md` — canonical GAS endpoint schemas;
  the `list_partners_needing_attention` action shape is documented
  there.

*Last refreshed 2026-05-12. Refresh when adding a new module or
when the source contract changes shape.*
