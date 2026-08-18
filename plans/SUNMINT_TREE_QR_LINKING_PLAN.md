# Sunmint Tree Planting → QR Code Linking — Execution Roadmap

**Status:** All units (PR2–PR8) built and merged. **Owner:** Gary Teh.
**Requested by:** Gary Teh, 2026-08-18.

**Errata (2026-08-18, same day):** PR1 as originally scoped ("patch the SOLD-only re-sale guard") was
built on a wrong read of the sale-processing code, caught before any file was touched — see the corrected
§1.4. **PR1 is retired.** Its one real, much smaller finding (a cosmetic picker-UI filter) is folded into
PR2. PR numbering elsewhere in this doc is left as-is (PR2…PR8) rather than renumbered.
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

### 1.4 Re-sale guard — CORRECTED 2026-08-18 (no gap; PR1 retired)

Original plan assumed `process_sales_telegram_logs.js` / `Parse Telegram ChatLogs.js`
(`1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7`) gate re-sale on the live
`Agroverse QR codes` **status** column and would need to learn `ASSIGNED_TO_TREE`. **Traced the actual
code before writing anything and that's wrong:**

- `updateAgroverseQrStatus(qrCode)` (`process_sales_telegram_logs.js:392-410`) unconditionally
  `.setValue('SOLD')`s column D — no status read, no guard, nothing to patch.
- The real re-sale prevention is `buildQrOnSheetLookup_()` (line 657), fed by `existingQrCodes` —
  **`QR Code Sales` sheet column E** (`parseTelegramChatLogs():886-889` and the single-row variant at
  `:1076-1078`). A QR that has ever appeared as a row on `QR Code Sales` is permanently in that dedup
  lookup and any later `[SALES EVENT]` mentioning it is rejected as a duplicate — **independent of
  `Agroverse QR codes.status`**. So a QR that flips `SOLD → ASSIGNED_TO_TREE` is already protected from
  re-sale today, before this plan does anything.

**The one real (much smaller) finding:** `qr_code_web_service.js`'s `list=true` endpoint (doc comment:
"return QR codes where column D is NOT 'SOLD'") — the "available to sell" picker — filters out `SOLD` but
not `ASSIGNED_TO_TREE`. Purely cosmetic, but cheap to fix. **Folded into PR2 and shipped there** (`tokenomics` PR #389).

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
  - `process_sales_telegram_logs.js`'s `updateAgroverseQrStatus()` and its `Parse Telegram ChatLogs.js`
    sibling (`1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/`) — wherever they write `SOLD` to
    column D of `Agroverse QR codes`.
  - Backfill: **not in scope for this plan** — rows sold before PR2 shipped sort last / show blank in
    PR3's chronological list. Acceptable; not revisited.

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

### 1.10 Repo-sync — RESOLVED 2026-08-18 (during PR6)

`dao_client` and `dao_protocol` are **the same git repository** — both local checkouts on this box have
`origin` pointing at `https://github.com/TrueSightDAO/dao_protocol.git`, and identical commit history for
every file checked (e.g. `modules/update_qr_code.py`). `dao_client` is a second, legacy-named local clone,
not a fork or a vendored copy. **One PR against `dao_protocol` is sufficient** for any `truesight_dao_client`
change; pulling either local checkout picks up the other's merges. No separate `dao_client` PR was needed
for PR6.

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
| ~~**PR1**~~ | **RETIRED 2026-08-18** — premise was wrong, see §1.4 errata. No file was touched. | — |
| **PR2** ✅ MERGED (tokenomics #389) | Added column **W `Sold Date`** to `Agroverse QR codes`; stamped wherever status is set to `SOLD` in `process_qr_code_updates.js` (New Status branch) and in `process_sales_telegram_logs.js`/`Parse Telegram ChatLogs.js`. Folded in the retired PR1's one real finding: `qr_code_web_service.js`'s `list=true`/`list_with_members=true` picker filters — exclude `ASSIGNED_TO_TREE` alongside `SOLD`. | `tokenomics` |
| **PR3** ✅ MERGED (tokenomics #390) | Governor-gated read endpoints on `qr_code_web_service.js` (mirror `1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT`): (a) `list_sold_pending_tree=true` → QR rows where `status=SOLD`, `Owner Email` non-empty, `Tree Planting Date` (col N) empty, sorted by col W descending, each row includes qr_code/owner email/sold date; (b) a **new** read endpoint on the SunMint-tree-planting project (script id `1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF`, which has no `doGet` at all today — confirm this in PR3's own read, it's in-repo) → rows where `Status` (col M) = `NEW`, sorted by col G (planting date) ascending, each row includes Telegram Message ID / photo URL / species / lat-long / submitted name. Both gated by a shared-secret query param (new Script Property, e.g. `GOVERNOR_READ_KEY`) since both return PII/pre-decision data — do not ship these as open endpoints. | `tokenomics` |
| **PR4** ✅ MERGED (tokenomics #391) | New handler `process_tree_planting_link.gs` in the QR-codes mirror (script id `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v`, alongside `process_qr_code_updates.js`). Parses `[TREE PLANTING LINK EVENT]` (fields: `QR Code`, `SunMint Submission Message ID`, `Updated by`, `Submission Source`). Resolves signer → contributor name (same lookup as `process_tree_planting_telegram_logs.js`) → **governor check** (§1.7, copied `isGovernorByName_`) → reject silently-logged if not governor. Validates QR status is exactly `SOLD` and SunMint row status is exactly `NEW` (idempotency / no double-link). On pass: writes QR cols D/N/O/P/Q/R (status→`ASSIGNED_TO_TREE`, planting date/lat/long/photo from the SunMint row; leave Q blank), writes SunMint row col M→`LINKED` plus two new cols **R `Linked QR Code`**, **S `Linked At`**; appends the ledger fulfillment pair (§1.5/§7) to the managed ledger resolved via QR col V; sends the owner-email (§1.8) and stamps QR col X. New tracking tab `Tree Planting Link` (mirrors the `QR Code Update` tab shape) for dedup. Cron fallback `processTreePlantingLinkCron`, consistent with every other event type. **⚠ clasp deploy held** — see §2 gate. | `tokenomics` |
| **PR5** ✅ MERGED (dao_protocol #142) | Route `[TREE PLANTING LINK EVENT]` in `dispatch.py`'s `ROUTING` (env key e.g. `TREE_PLANTING_LINK`, action `processTreePlantingLinkFromTelegramChatLogs`) for immediate processing — additive, harmless without the env var set (falls back to PR4's cron), ships after PR4 is live. | `dao_protocol` |
| **PR6** ✅ MERGED (dao_protocol #143) | CLI module `truesight_dao_client/modules/link_tree_planting.py` (pattern in §1.9): `event_name='TREE PLANTING LINK EVENT'`, `canonical_labels=['QR Code', 'SunMint Submission Message ID', 'Updated by', 'Submission Source']`. **§1.10 resolved: `dao_client` and `dao_protocol` are the same git repository** (same `origin` remote, identical file history) — `dao_client` is a second, legacy-named local clone on this box, not a separate fork/vendor copy. One PR sufficed. | `dao_protocol` (== `dao_client`) |
| **PR7** ✅ MERGED (dapp_beta #62; companion treasury-cache #11) | Dedicated DApp module `dapp_beta/link_tree_planting.html`. Gated via `window.Permissions.requireRole('tree_planting.link')` (the established permissions.js pattern, not `review_queue.html`'s older manual `checkAuth()`) — required a small companion PR adding the `tree_planting.link` action to `treasury-cache/permissions.json`. Left list = PR3(a) endpoint. Right list = PR3(b) endpoint, via an **operator-configured** endpoint URL (localStorage) since the Sunmint Tree Planting GAS project has no known deployment URL yet (`manifest.json` marks it "TBC"). Signs via `EdgarPayloadHelper`. | `dapp_beta` + `treasury-cache` |
| **PR8** ✅ MERGED (tokenomics #392; this plan-doc update) | Docs: `tokenomics/SCHEMA.md` new columns (`Agroverse QR codes` W/X, `SunMint Tree Planting` R/S), status enum, and a corrected pre-existing mismatch (column O was documented as "Notarization URL", actually "GitHub Commit URL"); `tokenomics/API.md` / `API_ENDPOINTS.md` new event + endpoints; this plan's resume tracker + `CONTEXT_UPDATES.md` entry. | `tokenomics` / `agentic_ai_context` |
| **RUN** | First live link: governor picks one real SOLD+email QR and one real NEW submission on **beta** data if possible, else a low-stakes real pair; confirms via `link_tree_planting.html`; verifies QR row + SunMint row + ledger Transactions row + owner inbox by hand. **Ledger-money-movement gate (§2).** | — |
| **UAT** | See §5. **Always-stop gate.** | — |

---

## 4. Resume tracker

> **RESUME HERE → clasp deploy** (tokenomics: `process_qr_code_updates.js` + new
> `process_tree_planting_link.js` in mirror `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v`,
> and `qr_code_web_service.js` + `process_tree_planting_telegram_logs.js` in their mirrors — see §2 gate).
> All 7 code/docs PRs (PR2–PR8) are merged. **Before deploying**, provision the `GOVERNOR_READ_KEY` Script
> Property (same value) on both the QR-codes mirror and the SunMint Tree Planting mirror — PR3's read
> endpoints fail closed without it. After deploy: RUN (first live link, ledger-money-movement gate) → UAT
> (always-stop gate).

| Unit | Built | Merged | Contribution reported |
|------|:----:|:------:|:---------------------:|
| PR0 (this roadmap) | ☑ | ☑ (#756) | ☐ |
| ~~PR1 (re-sale guard fix)~~ | RETIRED — no gap existed, see §1.4 | — | — |
| PR2 (Sold Date column + stamping) | ☑ | ☑ (tokenomics #389) | ☐ |
| PR3 (governor-gated read endpoints ×2) | ☑ | ☑ (tokenomics #390) | ☐ |
| PR4 (link handler + ledger + email) | ☑ | ☑ (tokenomics #391) | ☐ |
| ↳ clasp deploy of PR4 | ☐ | — | — |
| PR5 (dispatch.py routing) | ☑ | ☑ (dao_protocol #142) | ☐ |
| PR6 (CLI module) | ☑ | ☑ (dao_protocol #143) | ☐ |
| PR7 (dapp link_tree_planting.html + treasury-cache permission) | ☑ | ☑ (dapp_beta #62, treasury-cache #11) | ☐ |
| PR8 (docs) | ☑ | ☑ (tokenomics #392, this update) | ☐ |
| RUN (first live link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** no execution unit above required reading a cross-repo file/state not
captured in §1. The two items deferred to their own PR's first step (§1.4's exact guard-condition text,
§1.10's fork/vendor relationship) were same-repo, single-file reads at the start of the PR that owned
them, not cross-repo design discovery — both resolved during execution (§1.4, §1.10), confirming the gate
held. All units PR2–PR8 are now built and merged; only the deploy/RUN/UAT gates remain (§2).

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
| 9 | Attempt to re-sell the same QR (simulate a `[SALES EVENT]` against it) | Rejected by the existing `QR Code Sales` dedup (§1.4) — pre-existing behavior, not new in this plan | Submit a test sale against the linked QR | Sale is blocked |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client` (`truesight-dao-report-ai-agent-contribution`,
`--dry-run` first) before starting the next unit.

---

## 7. Decisions resolved after initial PR execution began, and remaining open items

- **Ledger classification of the fulfillment leg — RESOLVED (Gary, 2026-08-18).** §1.5's existing
  sale-time entry is `+1 "Cacao Tree To Be Planted"` classified `Liability`. PR4's fulfillment write is a
  **two-line pair**: `-1 "Cacao Tree To Be Planted"` (`Liability`, discharges the sale-time obligation) +
  `+1 "Cacao Tree Planted"` classified **`Asset`** (not `Liability` — once fulfilled it's no longer an
  obligation, it's a countable asset the DAO can point to; also gives a running per-ledger count of
  fulfilled pledges via existing ledger-summary tooling, same benefit originally proposed under the
  liability-pair option).
- **`dao_client` vs `dao_protocol` sync — RESOLVED** (§1.10) — same repository, one PR sufficed.

**Still open (not blocking RUN/UAT, but worth Gary's call eventually):**
- **Backfill.** QR rows already `SOLD` before PR2 shipped don't have a `Sold Date` — acceptable gap, or
  worth a one-time backfill pass (e.g. from the linked Stripe session's created-at, where available)?
- **Sunmint app video collection.** QR col Q `Planting Video URL` is left blank by this plan (the farmer
  app doesn't collect video). Worth adding to `sunmint_beta` later, or is video out of scope entirely for
  this program?
