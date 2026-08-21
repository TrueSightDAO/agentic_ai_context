# Sunmint Tree Planting → QR Code Linking — Execution Roadmap

**Status:** PR2–PR8 built and merged; Sophia shipped substantial follow-on work 2026-08-20/21
(reject/invalid path, sentinel gate, doPost webhook, public-cache DApp rewrite) — **but a
2026-08-21 audit found two live data-corruption bugs that must be fixed before RUN. See §8.**
**Owner:** Gary Teh.
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

> **RESUME HERE → RUN** (first live link — governor picks one real SOLD+email QR and one real NEW
> Sunmint submission, confirms via `link_tree_planting.html`, verifies QR row + SunMint row +
> ledger Transactions row + owner inbox by hand). **Ledger-money-movement gate (§2) — needs an
> explicit go, not yet given.** After RUN: UAT (§5, always-stop gate).
>
> **PR-FIX1 (tokenomics #405) and PR-FIX2 (tokenomics #404) are both merged, deployed, and
> independently re-verified (2026-08-21)** — both live data-corruption bugs from the §8 audit are
> fixed: `SOLD_DATE_COL` in the sales-processing project and `SOLD_DATE_COL_DEST` in the QR-codes
> project both now correctly resolve to column AA.
>
> **A third incident hit during the PR-FIX1 deploy, fixed same-day:** the sales-processing
> project's live, gitignored `Credentials.js` (defines `setApiKeys()`/`getCredentials()`, called
> unconditionally at module load) got deleted by a `clasp push --force` from a folder that never had
> it locally — the exact same footgun as the earlier SunMint `Credentials.js` incident, this time
> hitting the **real, live sales webhook** (every function in the project failed with
> `ReferenceError: setApiKeys is not defined`, not just tree-planting). Caught by independently
> curling the live `/exec` endpoint rather than trusting the "deployed" self-report. Fixed by
> restoring `Credentials.js` as idempotent no-op seeding (Script Properties, the actual secret
> storage, were untouched); the fix was first deployed to a **new** deployment ID by mistake
> (leaving the real production URL still broken) — caught by independently curling the production
> URL specifically, corrected by redeploying **in place** to the existing production deployment ID
> and deleting the stray new one. Both the fix and the correction were independently verified via
> direct HTTP checks, not from Sophia's self-reports.
>
> **tokenomics #403 and dao_protocol #145 (doPost-based idempotency work) — closed 2026-08-21,
> governor-confirmed.** Per §9/this section's own decision criterion: `DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_LINK`
> was found unset in `dao_protocol`'s live env (root cause of the perceived gap), has since been
> set, and the existing `?action=processTreePlantingLinksFromTelegramChatLogs` GET path was
> re-tested end-to-end — confirmed delivering immediately. The mandated pattern (Sheet write +
> `doGet` trigger, §9) already works; the payload-carrying `doPost` mechanism was unnecessary.
> `#403`'s one valid finding (REJECT-event idempotency) remains an open follow-up, to be solved via
> the existing tracking-tab dedup pattern (keyed on Telegram row / Telegram Update ID), not a new
> Request-Transaction-ID scheme.
>
> **All deploys are done (2026-08-19/21).** All 4 live GAS targets pushed, deployed, and verified:
> QR-codes mirror (`1UrBgqLnnQc6...`, PR4 handler + PR2 stamp + PR-FIX2), `qr_code_web_service.js`
> (`1MnAsIQAxc...`, PR2 picker fix + PR3 endpoint), SunMint Tree Planting (`1Jp8qNIBCZaR...`, PR3
> endpoint), sales-processing (`1dsWecVwbN0d...`, PR2 stamp + PR-FIX1). `GOVERNOR_READ_KEY`
> provisioned on both endpoints by Gary; both verified returning real data end-to-end.
>
> **Earlier incidents during initial deploy, both fixed same-day (tokenomics #393, #394, #395):**
> (1) `Code.js` — a stale, byte-identical duplicate of `process_qr_code_updates.js` sitting in git
> but never actually meant to be live — got pushed alongside it and broke the QR-codes webhook with
> a duplicate top-level `const` SyntaxError; fixed with `.claspignore`, verified restored within
> minutes. (2) SunMint's live, gitignored `Credentials.js` got deleted by a `clasp push --force` run
> without it present locally; the underlying Script Properties turned out to be untouched (separate
> storage from source files), so nothing was actually lost — just the two functions that read them,
> which were redeployed as idempotent no-op seeding. **Lesson applied to the 4th target
> (sales-processing) before touching it initially:** pulled the actual live source into an isolated
> read-only copy first and diffed against git — found `manifest.json`'s `source_files` field was
> wrong (the real live file was `Parse Telegram ChatLogs.js`, not `process_sales_telegram_logs.js`)
> and a third file (`telegram_webhook_listener.js`) was never deployed at all and would have
> collided on a top-level `const creds` if pushed — both excluded via `.claspignore`. That same
> lesson was **not** re-applied before the later PR-FIX1 deploy (see the third incident above) —
> worth hardening the deploy process itself (Sophia's own follow-up recommendation: a
> "`Credentials.js` presence check" gate before any `clasp push --force`).

| Unit | Built | Merged | Contribution reported |
|------|:----:|:------:|:---------------------:|
| PR0 (this roadmap) | ☑ | ☑ (#756) | ☐ |
| ~~PR1 (re-sale guard fix)~~ | RETIRED — no gap existed, see §1.4 | — | — |
| PR2 (Sold Date column + stamping) | ☑ | ☑ (tokenomics #389) | ☐ |
| PR3 (governor-gated read endpoints ×2) | ☑ | ☑ (tokenomics #390) | ☐ |
| PR4 (link handler + ledger + email) | ☑ | ☑ (tokenomics #391) | ☐ |
| ↳ clasp deploy of PR4 (+ PR2/PR3 deploys, all 4 GAS targets) | ☑ | ☑ (tokenomics #393, #394, #395) | ☐ |
| PR5 (dispatch.py routing) | ☑ | ☑ (dao_protocol #142) | ☐ |
| PR6 (CLI module) | ☑ | ☑ (dao_protocol #143) | ☐ |
| PR7 (dapp link_tree_planting.html + treasury-cache permission) | ☑ | ☑ (dapp_beta #62, treasury-cache #11) | ☐ |
| PR8 (docs) | ☑ | ☑ (tokenomics #392, this update) | ☐ |
| PR9 (reject/invalid path, TREE PLANTING REJECT EVENT) | ☑ | ☑ (tokenomics #396) | ☐ |
| PR10 (fix Sold Date/Notification column collision — **has its own bug, see §8 PR-FIX1**) | ☑ | ☑ (tokenomics #398) | ☐ |
| PR11 (sentinel gate — governor OR sentinel) | ☑ | ☑ (tokenomics #399) | ☐ |
| PR12 (doPost webhook for immediate TREE PLANTING LINK processing) | ☑ | ☑ (tokenomics #397) | ☐ |
| PR13 (reject-event scan filter fix) | ☑ | ☑ (tokenomics #402) | ☐ |
| PR14 (dapp: UX-conform + dropdown pickers) | ☑ | ☑ (dapp_beta #63) | ☐ |
| PR15 (dapp: Mark Invalid control) | ☑ | ☑ (dapp_beta #64) | ☐ |
| PR16 (dapp: public-cache rewrite, removes settings wall) | ☑ | ☑ (dapp_beta #66; `lineage-assets` cache generator + 30-min cron) | ☐ |
| **PR-FIX1** (fix sales-processing project still stamping Sold Date to col W — live, active data corruption of an unrelated review workflow) | ☑ | ☑ (tokenomics #405) | ☐ |
| **PR-FIX2** (fix Sold Date/Notification off-by-one — both currently resolve to col AB, colliding with each other) | ☑ | ☑ (tokenomics #404) | ☐ |
| RUN (first live link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

**tokenomics #403 / dao_protocol #145 (doPost idempotency mechanism) — CLOSED, not merged** (2026-08-21,
governor-confirmed): superseded by confirming the existing GET-trigger path already works once the
missing env var was set. See RESUME HERE note above for the full rationale.

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

---

## 8. Post-deploy audit findings (Claude, 2026-08-21) — read before RUN

Sophia shipped substantial follow-on work 2026-08-20/21 (PR9–PR16 above) beyond this plan's original
scope: a reject/invalid path, sentinel gating, an immediate `doPost` webhook, and a full architecture
improvement replacing the DApp's key-gated-endpoint settings wall with public GitHub JSON caches (matches
the `review_queue.html`/`dao_members.json` convention — genuinely better than this plan's original design).
**All of that is verified live and working.** But auditing it (pulling actual live GAS source into isolated
read-only copies and diffing against git — same method used for the original 4th deploy target) surfaced
two live bugs that must be fixed before RUN.

### 8.1 PR-FIX1 (CRITICAL, live, active) — sales-processing project never got the column-collision fix

PR10 (tokenomics #398) moved the `Agroverse QR codes` Sold Date stamp off column W after discovering W is
actually **"Review Email Sent Date"**, live-owned by an unrelated retailer-review-follow-up workflow
(`go_to_market` email-agent scripts) — but the fix only touched `process_qr_code_updates.js` (the QR-codes
project, `1UrBgqLnnQc6...`). **The sales-processing project's live file — confirmed via isolated `clasp
pull`, not just git —**
`google_app_scripts/1dsWecVwbN0dOvilIz9r8DNt7LD3Ay13V8G9qliow4tZtF5LHsvQOFpF7/Parse Telegram ChatLogs.js`
line 205 **still has `const SOLD_DATE_COL = 22; // Column W`.** This is the primary path most real sales go
through — **every sale processed here is currently overwriting the review workflow's "Review Email Sent
Date" with today's date, live, right now.** Fix: update `SOLD_DATE_COL` in that file to match wherever
PR-FIX2 below lands the corrected value, `clasp push` + `clasp deploy` to the confirmed live deployment ID
`AKfycbzc15gptNmn8Pm726cfeXDnBxbxZ1L31MN6bkfBH7ziiz4gxl87vJXEhAAJJhZ5uAxq` (recorded in `manifest.json`'s
probe and re-verified live 2026-08-20), verify via a plain GET (expect unchanged `"No valid action
specified"` default response — same baseline-diff method used throughout this plan's deploy).
`process_sales_telegram_logs.js` and `telegram_webhook_listener.js` in that same directory are **not**
live (confirmed via the same isolated pull) — don't bother editing them, they're dead weight in git.

### 8.2 PR-FIX2 (CRITICAL, live) — the fix itself has an off-by-one; Sold Date and Notification-Sent collide

In the QR-codes project (live, confirmed via isolated `clasp pull` diffed byte-identical to git HEAD):
- `process_qr_code_updates.js`: `const SOLD_DATE_COL_DEST = 27; // Column AA`
- `process_tree_planting_link.js`: `const TPL_NOTIFICATION_SENT_COL = 27; // Column AB`

Both are **27**. This codebase's own 0-based-index convention (`getRange(row, CONST + 1)`) means index 27
resolves to **column AB** (1-based column 28), not AA — A=0…Z=25, AA=26, AB=27. So `SOLD_DATE_COL_DEST`'s
comment is wrong and its value collides with `TPL_NOTIFICATION_SENT_COL`: **Sold Date and Tree Planted
Notification Sent Date currently silently overwrite each other in the same column (AB).** Fix:
`SOLD_DATE_COL_DEST` should be **26** (targets AA, matching its own comment and SCHEMA.md's documentation).
`TPL_NOTIFICATION_SENT_COL = 27` (AB) is correct as-is — leave it. After fixing, `clasp push` +
`clasp deploy` the QR-codes project (deployment ID
`AKfycbxMz8cAkJ-MT3FhxRc9SxLZZzm7J83-EZPnv5M7V_9QHKywC3aKUeaR2tqELheq3e7X`), and PR-FIX1 above must use
the corrected AA value too (both must agree). Update `SCHEMA.md`'s AA row description if it currently
documents the wrong index. **Do this fix before RUN** — RUN's own notification write would otherwise land
in the same colliding column, and the UAT acceptance criteria (§5 step 4: "W already had a Sold Date; X
gets today's date") already refer to stale column letters that need updating to AA/AB throughout §5 too.

### 8.3 Cleanup (not urgent, but flagged — avoid a third incident)

- **`Code.js` in the QR-codes project git checkout is dead** (confirmed not live via isolated pull —
  doesn't even exist in the live file list) but keeps getting edited as if it were live: PR12's commit
  (`6ef80e2`) added a `processTreePlantingLinkCron` doGet branch to `Code.js` — that branch will never run.
  It's also redundant: the live `process_qr_code_updates.js` already exposes the equivalent action
  (`?action=processTreePlantingLinksFromTelegramChatLogs`, from this plan's original PR4). Recommend
  **deleting `Code.js` from git entirely** in this directory — it has now caused two incidents (a real
  production SyntaxError when it got pushed by accident earlier, and this dead-code edit) purely by
  existing and looking legitimate. Same applies to any other `google_app_scripts/<id>/Code.js` that's
  confirmed non-live if anyone wants to do a wider sweep, but that's out of scope here.
- **Chronological ordering regressed.** This plan's original §1.6 wanted the QR picker sorted by Sold Date.
  The new cache-based picker (`lineage-assets/scripts/sync_pending_caches.py`) sources sold-QR data from
  `qrs_index.json` instead and doesn't sort by Sold Date at all. Minor, not blocking — flagging so it isn't
  assumed to already be true.
- **Native `<select>` vs the established searchable-combobox convention.** `UX_CONVENTIONS.md`'s
  "Combobox/Searchable Dropdowns" section documents a searchable pattern (`update_qr_code.html`,
  `report_inventory_movement.html`) specifically for large lists. PR14 used plain `<select id="qr_select">`
  / `<select id="sunmint_select">` instead — functional, but with **414 sold-QR items** in one unsearchable
  native dropdown, this is a real usability gap against the documented convention for exactly this
  scenario. Worth upgrading to the combobox pattern; not blocking RUN/UAT.
- **Identity-verification transitional state missing.** `UX_CONVENTIONS.md`'s "Verifying your digital
  signature..." pattern (loading message before the welcome/form reveal) isn't present on
  `link_tree_planting.html`. Cosmetic.

---

## 9. Required request pattern (Gary, 2026-08-21) — verify PR9/PR12/#403 conform

**Mandated pattern:** user clicks (DApp) → `dao_protocol` (Python) → `dao_protocol` writes to the Google
Sheet → `dao_protocol` sends a **`doGet`** to GAS (a trigger, not a payload carrier) → GAS reads what was
just written and handles the follow-up business logic.

**This is already what PR5 (this plan, `dao_protocol` #142) implements, and it's still intact and live
today** — verified by reading `truesight_dao_client/server/routes/dao.py`'s `submit_contribution` handler
directly (not assuming): it writes **synchronously** to `Telegram Chat Logs` via `sheets/telegram_raw_log.py`
(comment on that line: "synchronous; user-visible state, no-race rule"), *then* asynchronously
(`background.add_task`) calls `dispatch.dispatch_event(text)`, which — for every event tag in the
`ROUTING` table, PR5's `[TREE PLANTING LINK EVENT]` entry included — calls `webhook_trigger.trigger(url,
action)`: a plain **GET** with `?action=<name>` and no payload (the one exception, `ONBOARDING_INVITATION`,
adds a few extra query params, never the full event text). GAS's `doGet` handler reads the just-written
row from `Telegram Chat Logs` itself. This is uniform across every other event type in the dispatcher — PR5
did not deviate from it.

**PR12 (tokenomics #397) added a *second*, non-standard `doPost` endpoint** on `process_tree_planting_link.js`
that receives the full signed event text directly (bypassing the sheet-write-then-GET-trigger pattern
above), and PR9/#403/dao_protocol#145 have been iterating on that `doPost` path's gaps (LINK-marker-only,
governor-only, non-idempotent). **#403's PR description claims "Rails dispatch GET passes no event text;
Telegram feed dead since 2024" as the reason a payload-carrying endpoint is needed** — this appears to
conflate legacy **Rails** (`sentiment_importer`/Perch — a different, mostly-retired codebase for DAO
purposes since the 2026-05-26 `dao_protocol` cutover, see `WORKSPACE_CONTEXT.md` §6) with the *current*
`dao_protocol` dispatch mechanism audited above, which is Python/FastAPI, not Rails, and does *not* rely on
an actual Telegram bot/chat scrape — "Telegram Chat Logs" is just the sheet's legacy name; `dao_protocol`
writes to it directly via the Sheets API, not through Telegram at all.

**Before building more on the doPost path, check the actually-boring possible explanation first:** is
`DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_LINK` actually set in `dao_protocol`'s live env? If it's unset,
`dispatch_event` logs "no webhook URL... GAS cron will process" and silently falls back to the **cron**
(minutes-scale delay, not broken, just slow) — which would *look* like "the GET path doesn't deliver
immediately" without there being any architectural problem at all, just a missing config value. If that's
the actual gap, the fix is setting one env var, not a new ingestion mechanism.

**Action:** before continuing #403/dao_protocol#145, confirm whether `DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_LINK`
is set. If unset → set it (the deployment URL for the QR-codes project's live deployment,
`AKfycbxMz8cAkJ-MT3FhxRc9SxLZZzm7J83-EZPnv5M7V_9QHKywC3aKUeaR2tqELheq3e7X`) and re-test the existing
`?action=processTreePlantingLinksFromTelegramChatLogs` GET path end-to-end before assuming the doPost
mechanism is necessary at all. If it's already set and the GET path is still confirmed (with evidence, not
assumption) not delivering immediately, then there may be a real gap worth documenting precisely — but the
fix should still follow the mandated pattern (Sheet write + `doGet` trigger), not a payload-carrying
`doPost`. Either way, `[TREE PLANTING REJECT EVENT]`'s idempotency (#403's real, valid finding) belongs in
the **existing tracking-tab dedup** that every other event type already uses (keyed on Telegram row /
`Telegram Update ID`), not a new `Request Transaction ID`-based scheme unique to this one path.
