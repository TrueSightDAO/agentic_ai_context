# Sunmint Tree Planting → QR Code Linking — Execution Roadmap

**Status:** Pre-flight complete, ready for PR1. **Owner:** Gary Teh. **Requested by:** Gary Teh, 2026-08-18.
**Goal:** Give a governor (or Sophia / an authorized LLM agent, signing as themselves) a way to link a
farmer-submitted `[TREE PLANTING EVENT]` (landing in the `SunMint Tree Planting` sheet) to a **sold**
`Agroverse QR codes` row — flip its status, copy the planting evidence onto the QR row, notify the QR
owner by email, and book the ledger fulfillment entry. A dedicated governor-only DApp module drives it.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. Update the resume tracker as units land; report the DAO
> contribution after each merge (§6). §5a: **one PR per execution turn, then stop.**

---

## 0. Decisions (Gary, 2026-08-18)

| # | Decision | Choice |
|---|----------|--------|
| 0.1 | Event/transport shape | **Dedicated event type `[TREE PLANTING LINK EVENT]`** (not an extension of `[QR CODE UPDATE EVENT]`) — it must atomically touch three sheets (QR row, SunMint Tree Planting row, managed-ledger Transactions) plus send an email; folding that into the generic QR-update handler would overload a handler other flows depend on staying simple. |
| 0.2 | DApp surface | **Dedicated page** `dapp/link_tree_planting.html` (not a mode bolted onto `update_qr_code.html`), governor/sentinel-gated like `review_queue.html`. |
| 0.3 | Everything else in the 2026-08-18 discussion | **Confirmed as-is** — reuse `ASSIGNED_TO_TREE` as the post-link status, reuse the existing `Cacao Tree To Be Planted` liability line as the pre-link "tree to be planted" currency, add a new `Cacao Tree Planted` line classified **`Asset`** as the fulfillment leg (§7), reuse the `Owner Email` (col L) onboarding-email pattern for the notification. |
| 0.4 | Merge cadence for PR2–PR8 | **Merge each as it lands** (Gary, 2026-08-18) — branch off updated `main` for each subsequent PR rather than opening the whole stack unmerged. |

---

## 1. Pre-flight — captured facts (§5d: no PR below should need to re-discover any of this)

### 1.1 Where a Sunmint submission lands today

- Farmer app `sunmint_beta`/`sunmint_prod` (`index.html`) signs `[TREE PLANTING EVENT]` and POSTs to Edgar
  (offline-queue pattern documented in `sunmint_beta/README.md`).
- `[TREE PLANTING EVENT]` is **not** in `dao_protocol/truesight_dao_client/server/dispatch.py`'s `ROUTING`
  table → no immediate webhook; it only reaches the destination sheet via the **GAS cron fallback**
  (`processTelegramLogs` cron in the SunMint project, script id
  `1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF`, file
  `google_app_scripts/sunmint_tree_planting/process_tree_planting_telegram_logs.gs`), scanning
  `Telegram Chat Logs` (spreadsheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`) for the
  `[TREE PLANTING EVENT]` marker in column G.
- Destination tab: **`SunMint Tree Planting`** (same spreadsheet, gid `176124122`). Schema
  (`tokenomics/SCHEMA.md` line 528, mirrors the literal `appendRow` order in
  `process_tree_planting_telegram_logs.js:286-304`):

  | Col | Header | Notes |
  |-----|--------|-------|
  | A | Telegram Update ID | |
  | B | Telegram Chatroom ID | |
  | C | Telegram Chatroom Name | |
  | D | Telegram Message ID | **stable dedup key** (`getProcessedMessageIds` reads this column) |
  | E | Contributor Handle | |
  | F | Contribution Made | full signed submission text |
  | G | Status date | planting date `YYYYMMDD` |
  | H | Telegram File IDs | |
  | I | Photo of Tree Planted | photo URL |
  | J | Submitted Name | resolved contributor name (matched by public signature against `Contributors Digital Signatures`) |
  | K | Latitude | |
  | L | Longitude | |
  | M | Status | new rows land `NEW` |
  | N | Specie | |
  | O | GitHub Commit URL | photo mirrored to `TrueSightDAO/sunmint` `images/` |
  | P | Cost of Tree | |
  | Q | Tree Planting Time | |

  **There is no QR-code column on this tab today.** Linking is 100% manual/undocumented right now.

### 1.2 `Agroverse QR codes` — full schema (already captured, `tokenomics/SCHEMA.md` line 866)

Spreadsheet `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, gid `472328231`.

| Col | Header | Notes |
|-----|--------|-------|
| A | qr_code | |
| B | landing_page | |
| C | ledger | |
| D | status | enum in `process_qr_code_updates.js:499-509`: `SCHEDULED_FOR_MINTING, MINTED, WAREHOUSED, ON CONSIGNMENT, CACAO CIRCLE, LOST, SOLD, EXPENSED, ASSIGNED_TO_TREE, GIFT` — **`ASSIGNED_TO_TREE` already exists**, unused by any writer today. |
| E–H | farm name / state / country / Year | |
| I | Currency | must match `Currencies!A` |
| J | QR code creation date | **not** a sale date (see §1.6) |
| K | QR code location | |
| L | Owner Email | written by `process_qr_code_updates.js` (`New Email` field) |
| M | Onboarding Email Sent Date | stamped by `sendEmailForQRCode`/`processBatch` in `qr_code_web_service.js` (§1.5) |
| N | Tree Planting Date (YYYYMMDD) | **unused stub** — this plan's PR4 is the first writer |
| O | Latitude | unused stub |
| P | Longitude | unused stub |
| Q | Planting Video URL | unused stub (Sunmint app doesn't collect video today — leave blank on write) |
| R | Tree Seedling Photo URL | unused stub |
| S | Product Image | |
| T | Price | |
| U | Manager Name | |
| V | Ledger Name | resolves to a row on `Shipment Ledger Listing` (e.g. `AGL4`, `BEC`, `SEF1`) |
| Z | Stripe Session ID | FK → `Stripe Social Media Checkout ID` col C |

### 1.3 Status enum already anticipates this feature — landing-page count is already safe

- `dapp/update_qr_code.html` line 375 already lists `ASSIGNED_TO_TREE` in its New Status dropdown.
- `agroverse_shop/index.html` line ~1712 renders "Trees planted" from `data.soldBagsCount`, sourced from
  the GAS project `1Y8sJ22lZuqQYS_kF_3ItMuyfiAzbJ4wRA1xGC_bGx7FPB7uLTvrUObly` (`Code.js:166` and the
  identical `agroverse_wix_site_updates.js:176`):
  `var soldCount = data.slice(1).filter(row => row[3] === "SOLD" || row[3] === "ASSIGNED_TO_TREE").length;`
  → **introducing `ASSIGNED_TO_TREE` does not regress the public tree count**; no PR needed there.
- `truesight_me/scripts/build_stats_current.py` has no independent SOLD-only counter — confirmed clean.

### 1.4 Re-sale gap (must fix before ASSIGNED_TO_TREE goes live) — PR1

- Sale-processing scripts that must not allow re-selling an already-`ASSIGNED_TO_TREE` QR:
  `tokenomics/google_app_scripts/1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/process_sales_telegram_logs.js`
  and the sibling `Parse Telegram ChatLogs.js` in the same script-id folder — both reference the literal
  string `"SOLD"` for availability checks. **PR1 reads these two files' exact guard conditions and patches
  them to also treat `ASSIGNED_TO_TREE` as unavailable-for-sale** (do not assume the fix shape yet — the
  exact line/condition is PR1's first read, which is in-repo and single-purpose, not a cross-repo
  discovery, so it doesn't violate §5d).

### 1.5 Ledger booking at sale time (the existing "tree to be planted" currency)

`tokenomics/google_app_scripts/1duQFfTO0Pj0lC4tPVNmMOhNOS1GvJgzqVxXbsEDu-eqt_64DwxvrOVyl/sales_update_managed_agl_ledgers.js:352-378`
(and the AGL4-only sibling `1wmgYPwfRDxpiboa8OH-C6Ndovklf8HaJY305n7dhRzs7BmUBQg7fL_sZ/sales_update_main_dao_offchain_ledger.js:199`)
appends, to the relevant managed ledger's `Transactions` tab, on every sale:

```
Row 1: [Sales Date, message, inventoryContributorName, -1, inventoryType,                  'Assets']
Row 2: [Sales Date, message, cashContributorName,       salePrice, 'USD',                   'Assets']
Row 3: [Sales Date, message, `SunMint Tree Planting Contract - ${aglContractName}`, 1, 'Cacao Tree To Be Planted', 'Liability']
```

`Cacao Tree To Be Planted` is a **literal string**, not a `Currencies` tab row (confirmed via grep — it
never appears in `Currencies`-tab-writing code). **This is the "tree to be planted" currency item the
requester asked about — it already exists.** No `Currencies` tab change is needed for this plan; the
fulfillment leg (§1.6, PR4) follows the same literal-string convention, not a new `Currencies` row.

### 1.6 QR row has no sale date — chronological listing needs one (PR2)

Column J is QR **creation** date, not sale date. No column captures "date this row's status became
`SOLD`." **PR2** adds column **W `Sold Date`** to `Agroverse QR codes` and stamps it wherever status is
set to `SOLD`:
  - `process_qr_code_updates.js` — the `New Status` branch (`extracted.status`, line ~266-271 in
    `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v/process_qr_code_updates.js`).
  - `process_sales_telegram_logs.js` and `Parse Telegram ChatLogs.js`
    (`1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/`) — wherever they write `SOLD` to
    column D of `Agroverse QR codes` (same files touched by PR1; **PR2 should land after PR1, but is a
    distinct, independently-revertible change to the same two files** — keep the diffs non-overlapping).
  - Backfill: **not in scope for this plan** — rows sold before PR2 ships will sort last / show blank in
    PR5's chronological list. Acceptable; flagged in §7 as an open question if Gary wants a backfill pass.

### 1.7 Governor gating — confirmed there is no free server-side enforcement anywhere in this stack

- `dao_protocol/truesight_dao_client/server/dispatch.py` has **zero** role/governor checks for any event
  type — it is a generic signed-submission relay (confirmed via full-file grep for `governor`).
- `dapp/review_queue.html`'s `checkAuth()` (lines 394-416) is **client-side only** — it fetches
  `treasury-cache/dao_members.json`, checks `roles.indexOf('governor')`, and disables buttons. Its own
  code comment claims "Edgar re-verifies the signer server-side," but that verification is **signature
  validity only**, not role — confirmed by reading the GAS handler behind its target event
  (`[CONTRIBUTION REVIEW EVENT]` → `processApprovalRejections` in
  `1BHAGZd_T1I5mQnqnAFqUJKX2x_N8Uv05n1O2OohRA908Ja8wVwVxaR7K/grok_scoring_for_telegram_and_whatsapp_logs.js`),
  which has **no governor/role check at all**.
- The one real reusable pattern found: `isGovernorByName_(contributorName)` in
  `19Wag9x-sjbLVgIsPh2vj90ZG7Rgq2iGaVOomAeAvtg6CdZKJHLZ9AJrC/Code.js:376-388` — opens
  `OFFCHAIN_TRANSACTIONS_SHEET_URL` (`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, gid `0`), reads tab
  `Governors` column A, case-insensitive name match. **GAS projects can't share code across clasp
  mirrors** — every mirror in this codebase duplicates small helpers locally (established convention,
  e.g. every mirror ships its own `Version.gs`). **PR4 copies this ~15-line function verbatim** into the
  new handler's file rather than inventing a new pattern.
- Because this handler moves ledger money and sends email, **PR4 must be the first governor-gated
  handler in the codebase with real server-side enforcement** — reject (log + skip, write nothing) if the
  resolved contributor name isn't in `Governors`.

### 1.8 Owner-email notification pattern to reuse

`qr_code_web_service.js` (`1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT`) — two working
examples: `processBatch()` (lines ~1771-1861, batches by email, retry-verified column stamp) and the
simpler single-QR `sendEmailForQRCode(qrCode)` (lines ~1900-1936): reads `Owner Email` (col L), a
`DocumentApp` template with a `{{TRACKING_LINK}}` placeholder, `MailApp.sendEmail({to, subject, htmlBody})`,
stamps a "sent" column. **This lives in a different clasp mirror than PR4's handler** (GAS can't
cross-call), so PR4 duplicates a trimmed version (`MailApp.sendEmail` directly, no template doc — a
literal string body is enough for v1) rather than reusing this file. New stamp column: **X `Tree Planted
Notification Sent Date`** on `Agroverse QR codes` (column M is already spoken for — "Onboarding Email
Sent Date" is a different email).

### 1.9 CLI module pattern to follow

`dao_client/truesight_dao_client/modules/update_qr_code.py` (full file already read, 41 lines) — thin
wrapper around `edgar_client.build_event_cli(event_name=..., canonical_labels=[...], dapp_page=...)`.
PR3 follows this exact shape.

### 1.10 Repo-sync open item (do not guess during PR3 — resolve in PR3's own turn, it's in-repo)

`dao_client` and `dao_protocol` both contain an apparently-identical `truesight_dao_client/` tree
(confirmed: `modules/update_qr_code.py`, `modules/report_tree_planting.py`,
`server/dispatch.py`/`data/events_catalog.json` all exist in both, byte-for-byte unchecked). Whether one
is a fork/mirror of the other, or `dao_protocol` vendors a frozen copy, was **not resolved this session**.
PR3 must check `git remote -v` / recent commit history in both before deciding whether it needs to open a
matching PR in the second repo, or whether one is derived/generated and shouldn't be hand-edited. This is
a same-repo `git log` check, not a cross-repo *design* discovery, so it satisfies §5d.

---

## 2. Authorization envelope (§5e — ask once, not per PR)

| Surface | Envelope |
|---------|----------|
| `tokenomics` GAS **source files** (this repo, clasp mirror `.js`/`.gs` under `google_app_scripts/`) | Pre-authorized — feature branch + PR per unit, human reviews before merge. |
| `tokenomics` **clasp deploy** (pushing a merged GAS change live to the production webhook) | **Always-stop gate (§5c: production deploy).** Ask once per PR that needs it, not silently bundled with merge. |
| `dao_client` / `dao_protocol` (Python CLI) | Pre-authorized — low blast radius, feature branch + PR, no deploy step (installed from source/pip on demand). |
| `dapp` (→ `dapp_beta` first, never `dapp_prod` directly) | Pre-authorized for `dapp_beta`. Promotion `dapp_beta` → `dapp_prod` is a **separate always-stop gate**, not bundled into this plan's PRs — ask when that promotion is actually wanted. |
| **Ledger money-movement** (PR4's fulfillment booking, run against a real managed ledger) | **Always-stop gate (§5c: TDG/money).** The RUN step (§4) that first executes PR4 against production data needs an explicit `go`, same as the BEC precedent (`ERA_COHORT_TREE_ISSUANCE_PLAN.md` §0.9 — mint-only, human confirms the money-moving step). |
| **UAT** (§5) | Always-stop gate — human validates end-to-end on beta before this is used against real QR/email data. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|------|-------|------|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Read the exact SOLD-availability guard in `process_sales_telegram_logs.js` + `Parse Telegram ChatLogs.js` (script id `1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7`); patch so `ASSIGNED_TO_TREE` is also treated as unavailable-for-sale, same as `SOLD`. Independent, ships alone, no dependency on later units. | `tokenomics` |
| **PR2** | Add column **W `Sold Date`** to `Agroverse QR codes`; stamp it wherever status is set to `SOLD` in `process_qr_code_updates.js` (New Status branch) and in the two sale-processing files touched by PR1 (non-overlapping diff from PR1). | `tokenomics` |
| **PR3** | Governor-gated read endpoints on `qr_code_web_service.js` (mirror `1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT`): (a) `list_sold_pending_tree=true` → QR rows where `status=SOLD`, `Owner Email` non-empty, `Tree Planting Date` (col N) empty, sorted by col W descending, each row includes qr_code/owner email/sold date; (b) a **new** read endpoint on the SunMint-tree-planting project (script id `1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF`, which has no `doGet` at all today — confirm this in PR3's own read, it's in-repo) → rows where `Status` (col M) = `NEW`, sorted by col G (planting date) ascending, each row includes Telegram Message ID / photo URL / species / lat-long / submitted name. Both gated by a shared-secret query param (new Script Property, e.g. `GOVERNOR_READ_KEY`) since both return PII/pre-decision data — do not ship these as open endpoints. | `tokenomics` |
| **PR4** | New handler `process_tree_planting_link.gs` in the QR-codes mirror (script id `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v`, alongside `process_qr_code_updates.js`). Parses `[TREE PLANTING LINK EVENT]` (fields: `QR Code`, `SunMint Submission Message ID`, `Updated by`, `Submission Source`). Resolves signer → contributor name (same lookup as `process_tree_planting_telegram_logs.js`) → **governor check** (§1.7, copied `isGovernorByName_`) → reject silently-logged if not governor. Validates QR status is exactly `SOLD` and SunMint row status is exactly `NEW` (idempotency / no double-link). On pass: writes QR cols D/N/O/P/Q/R (status→`ASSIGNED_TO_TREE`, planting date/lat/long/photo from the SunMint row; leave Q blank), writes SunMint row col M→`LINKED` plus two new cols **R `Linked QR Code`**, **S `Linked At`**; appends the ledger fulfillment pair (§1.5/§7) to the managed ledger resolved via QR col V; sends the owner-email (§1.8) and stamps QR col X. New tracking tab `Tree Planting Link` (mirrors the `QR Code Update` tab shape) for dedup. Cron fallback `processTreePlantingLinkCron`, consistent with every other event type. **⚠ clasp deploy held** — see §2 gate. | `tokenomics` |
| **PR5** | Route `[TREE PLANTING LINK EVENT]` in `dispatch.py`'s `ROUTING` (env key e.g. `TREE_PLANTING_LINK`, action `processTreePlantingLinkFromTelegramChatLogs`) for immediate processing — additive, harmless without the env var set (falls back to PR4's cron), ships after PR4 is live. | `dao_protocol` |
| **PR6** | CLI module `truesight_dao_client/modules/link_tree_planting.py` (pattern in §1.9): `event_name='TREE PLANTING LINK EVENT'`, `canonical_labels=['QR Code', 'SunMint Submission Message ID', 'Updated by']`, `dapp_page='link_tree_planting.html'`. Resolve the `dao_client`/`dao_protocol` sync question (§1.10) as this PR's first step; open a matching PR in the second repo only if that check shows they need independent changes. | `dao_client` (+ possibly `dao_protocol`) |
| **PR7** | Dedicated DApp module `dapp/link_tree_planting.html` (→ lands in `dapp_beta` first, §2). Client-side governor/sentinel gate exactly like `review_queue.html`'s `checkAuth()`. Left list = PR3(a) endpoint (QR, owner email, sold date, chronological). Right list = PR3(b) endpoint (submission, photo thumbnail, species, planting date, chronological). Governor picks one of each, confirms, signs `[TREE PLANTING LINK EVENT]` via the same RSA-keypair-in-localStorage flow as `update_qr_code.html`. | `dapp` (→ `dapp_beta`) |
| **PR8** | Docs: `tokenomics/SCHEMA.md` new columns (`Agroverse QR codes` W/X, `SunMint Tree Planting` R/S) and new tab (`Tree Planting Link`); `tokenomics/API.md` / `API_ENDPOINTS.md` new event + endpoints; `CONTEXT_UPDATES.md` entry. | `tokenomics` / `agentic_ai_context` |
| **RUN** | First live link: governor picks one real SOLD+email QR and one real NEW submission on **beta** data if possible, else a low-stakes real pair; confirms via `link_tree_planting.html`; verifies QR row + SunMint row + ledger Transactions row + owner inbox by hand. **Ledger-money-movement gate (§2).** | — |
| **UAT** | See §5. **Always-stop gate.** | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (tokenomics: patch the ASSIGNED_TO_TREE re-sale gap).

| Unit | Built | Merged | Contribution reported |
|------|:----:|:------:|:---------------------:|
| PR0 (this roadmap) | ☐ | ☐ | ☐ |
| PR1 (re-sale guard fix) | ☐ | ☐ | ☐ |
| PR2 (Sold Date column + stamping) | ☐ | ☐ | ☐ |
| PR3 (governor-gated read endpoints ×2) | ☐ | ☐ | ☐ |
| PR4 (link handler + ledger + email) | ☐ | ☐ | ☐ |
| ↳ clasp deploy of PR4 | ☐ | — | — |
| PR5 (dispatch.py routing) | ☐ | ☐ | ☐ |
| PR6 (dao_client CLI module) | ☐ | ☐ | ☐ |
| PR7 (dapp link_tree_planting.html) | ☐ | ☐ | ☐ |
| PR8 (docs) | ☐ | ☐ | ☐ |
| RUN (first live link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** no execution unit above requires reading a cross-repo file/state not
already captured in §1. The two items explicitly deferred to their own PR's first step (§1.4's exact
guard-condition text, §1.10's fork/vendor relationship) are same-repo, single-file reads at the start of
the PR that owns them, not cross-repo design discovery.

---

## 5. UAT — beta stack, before this touches real owner inboxes

Human-tested, on **beta** data (or the lowest-stakes real SOLD+email QR Gary is willing to spend, if a
beta QR isn't practical — this mirrors the BEC precedent of a small real-money test run, not a mocked one).

| Step | Surface | What to expect | Interaction | Acceptance criterion |
|------|---------|-----------------|--------------|----------------------|
| 1 | `dapp_beta` → `link_tree_planting.html`, signed in as a **non-governor** test identity | Page loads, both lists render read-only / actions disabled, badge shows "not a governor" | Load the page | No link action is submittable |
| 2 | Same page, signed in as governor | Left list shows real SOLD+email QR rows in chronological (sold-date) order; right list shows real NEW submissions in chronological (planting-date) order | Load the page | Both lists populated, correctly ordered, no PII leaks to non-governor session (re-check step 1 after this) |
| 3 | Same page | Pick one QR + one submission, submit | Click confirm, sign | Success toast; no console errors |
| 4 | `Agroverse QR codes` sheet | Row's status flips to `ASSIGNED_TO_TREE`; N/O/P/R populated from the submission; W already had a Sold Date; X gets today's date | Inspect the row | All fields correct, no other rows touched |
| 5 | `SunMint Tree Planting` sheet | Row's status flips to `LINKED`; R/S populated | Inspect the row | Correct, idempotent — re-running PR4 against the same pair (retry) does not double-write |
| 6 | Managed ledger `Transactions` tab (resolved via the QR's Ledger Name) | New `-1 Cacao Tree To Be Planted` / `+1 Cacao Tree Planted` pair appended | Inspect the ledger | Matches §7's resolved accounting decision |
| 7 | Owner's inbox (the email in QR col L — **use a test address for UAT, not a real customer**) | Notification email arrives | Check inbox | Correct QR code / tracking link referenced |
| 8 | `agroverse_shop` landing page | "Trees planted" counter unchanged (still counts the now-`ASSIGNED_TO_TREE` row) | Reload the page | Counter did not drop |
| 9 | Attempt to re-sell the same QR (simulate a `[SALES EVENT]` against it) | Rejected, same as a `SOLD` QR would be (PR1) | Submit a test sale against the linked QR | Sale is blocked |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client` (`truesight-dao-report-ai-agent-contribution`,
`--dry-run` first) before starting the next unit.

---

## 7. Decisions resolved after initial PR execution began

- **Ledger classification of the fulfillment leg — RESOLVED (Gary, 2026-08-18).** §1.5's existing
  sale-time entry is `+1 "Cacao Tree To Be Planted"` classified `Liability`. PR4's fulfillment write is a
  **two-line pair**: `-1 "Cacao Tree To Be Planted"` (`Liability`, discharges the sale-time obligation) +
  `+1 "Cacao Tree Planted"` classified **`Asset`** (not `Liability` — once fulfilled it's no longer an
  obligation, it's a countable asset the DAO can point to; also gives a running per-ledger count of
  fulfilled pledges via existing ledger-summary tooling, same benefit originally proposed under the
  liability-pair option).
- **Backfill.** QR rows already `SOLD` before PR2 ships won't have a `Sold Date` (§1.6) — acceptable gap,
  or worth a one-time backfill pass (e.g. from the linked Stripe session's created-at, where available)?
- **`dao_client` vs `dao_protocol` sync** (§1.10) — resolved in PR6, but if Gary already knows the
  relationship (e.g. "dao_protocol vendors a frozen copy, never hand-edit it"), stating it now saves PR6 a
  git-archaeology detour.
- **Sunmint app video collection.** QR col Q `Planting Video URL` is left blank by this plan (the farmer
  app doesn't collect video). Worth adding to `sunmint_beta` later, or is video out of scope entirely for
  this program?
