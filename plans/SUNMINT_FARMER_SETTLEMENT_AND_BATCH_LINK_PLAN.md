# SunMint Farmer Settlement + Batch QR-Tree Linking — Execution Roadmap

**Status:** design ruled (2026-09-20, two revisions same day — see history below); no code yet.
**Owner:** Gary Teh · **Drafted by:** Claude Anthropic (Envoy), from a live design conversation.
**Supersedes:** `SUNMINT_TREE_QR_LINKING_PLAN.md` §7 (the old link-time booking:
`-1 Liability` / `+1 "Cacao Tree Planted"` terminal asset). That plan's PR2–PR16 (the DApp, the QR
schema columns, the governor gate, the reject/invalid path) all stay untouched — only the
ledger-booking step at link time changes.

**Revision history (same day, both real design corrections, not indecision):**
1. **First draft:** three new ledger line-items tracking farmer-side state.
2. **Second draft:** simplified to "ledger only records cash events" — the three items became
   row-derived state instead of ledger rows.
3. **This draft (reverted back to real ledger items, refined):** Gary caught the flaw in draft 2 —
   "ledger only for cash" isn't actually the right cut line. A prepayment before the tree is
   confirmed is a **prepaid asset** (real value retained, at real risk if the farmer never delivers)
   and a confirmed-but-unpaid tree is an **accrued liability** (a real obligation the moment it's
   incurred) — both are standard accrual-accounting items that should be **on the ledger** regardless
   of whether cash moved at that exact instant. Draft 2's "just book cash, derive state from columns"
   made it impossible to tell "paid and delivered" from "paid and the farmer vanished with it" — which
   is precisely the risk this whole plan exists to make visible. **The customer side is still left
   row-derivable on top of its existing ledger row** (§1.3) — that case is genuinely different, because
   a working ledger row for it already exists; nothing is lost by not duplicating it.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**
> Report the DAO contribution after each merge (§6).

---

## 0. Decisions (ruled in the 2026-09-20 conversation)

| # | Decision | Choice |
|---|----------|--------|
| 0.1 (REVISED) | **The ledger carries real accrual items, not just cash events** | Reverted (Gary, 2026-09-20) — see revision history above. Three ledger items: `Cacao Tree Purchased - Not Planted` (Asset), `Cacao Tree - To Be Paid For` (Liability), `Cacao Tree Planted - Unassigned` (Asset, the settled pool). |
| 0.2 | **Existing customer liability booking is untouched** | Ruled — "harmless legacy." No PR here modifies `sales_update_managed_agl_ledgers.js`. The **link event** discharges it via its own new write (§1.2) — that's a different code path, not a change to the sales handler. |
| 0.3 | **Ledger location rule** | Ruled, confirmed explicitly: a managed ledger funding its **own** future trees books that spend on **itself**. Main/general treasury fronting a tree generically books on **main**. `Cacao Tree - To Be Paid For` **always** sits on main ledger regardless of eventual funding source (Gary's own words: "trees planted yet paid is liability always sitting on our main ledger") — it only gets ledger-located once actually paid. A transfer is needed **only** when a pool unit sitting on one ledger gets claimed by a different ledger's QR after the fact — self-funded and already-linked-before-payment need no transfer (§1.4). |
| 0.4 | **Link event can draw from a confirmed tree whether or not the farmer has been paid** | Ruled: "cooperatives are slow" — fulfilling the customer isn't gated on paying the farmer. See §1.2. |
| 0.5 | **Allocation priority for batch linking** | Ruled: distinct, not-yet-used owner email → a specific photographed tree (1:1) + personalized notification. Repeat email or no email → a plot-level association instead. |
| 0.6 | **Every ledger write and every row mutation is a signed event** | Ruled — six events enumerated in §1.5, including the reconciliation match (now a real ledger reclassification, not just a column write, which makes this requirement even more clearly correct than in draft 2). |
| 0.7 (OPEN) | **Does the reconciliation match need a governor click, or fire automatically and just be system-signed?** | Proposed default: automatic + system-signed — a governor click per match would reintroduce the one-at-a-time bottleneck. Flagged, not confirmed. |
| 0.8 (OPEN) | **Aging policy for stalled prepayments or unpaid confirmed trees** | Not yet chosen between active nudging and a passive report. Default: passive report (§3, PR8), non-blocking. |
| 0.9 | **`[TREE PURCHASE EVENT]` reuses the existing `[ASSET RECEIPT EVENT]` mechanism** | Verified live 2026-09-20 (§1.10): the `Asset Receipts` tab + `asset_receipt_ingest` GAS project + `dao_client`'s existing `report_asset_receipt.py` CLI already do exactly this shape (pay cash, book an offchain asset row). No new event, no new CLI needed for v1 — submit with `Currency = "Cacao Tree Purchased - Not Planted"`. **Caveat, not yet resolved:** this existing pipeline books only onto the **main** ledger's offchain transactions tab — it has no way to target a specific managed ledger (AGL8, etc.) directly. So until/unless that's extended, every purchase defaults to main-ledger funding (§0.3's "self-funded by a specific managed ledger" path is a phase-2 enhancement, not v1). |
| 0.10 (OPEN) | **`[FARMER PAYMENT EVENT]` generalizes the existing CFR `payouts` mechanism, pending a source-level check** | The live `payouts` tab (§1.7) already has the right shape (`tree_planting_id`, `bank_ref`, `receipt_url`, `program_slug`) and its Tier-1 writes are confirmed unaffected by the CFR-specific Tier-2 blocker. **Not yet confirmed:** whether its GAS handler currently books real ledger legs (`-cash`/`-Liability`/`+Asset`) or only logs to the tracking tab — needs a `clasp pull` check on the `qr_code_web_service.js` project (§1.10) before PR4 starts, since that determines how much of PR4 is "generalize" vs. "build from scratch alongside an existing tracking tab." |

---

## 1. Pre-flight — captured facts (§5d: no PR below should need to re-discover any of this)

### 1.1 Verified live state, 2026-09-20

- **QR status distribution** (`lineage-assets/qrs_index.json`, generated 2026-08-20): `MINTED: 1125,
  SAMPLE: 90, SOLD: 520, ON CONSIGNMENT: 35, GIFT: 3, EXPENSED: 3`. **No `ASSIGNED_TO_TREE` entries at
  all** — zero real links have ever landed via the formal pipeline.
- **`HANDOFF_MANIFEST.md`** row for the parent plan: "active — reject/invalid UAT done (2026-08-31);
  first real LINK pending Gary go." Telegram topic: thread **11596**.
- A real, already-known unbooked instance of the farmer-liability gap: Gary's own note (CFR thread
  30026) — *"we did already do a payout to Paulo priorly for planting 10 trees. We just haven't
  captured it on chain yet."* Concrete first case for the RUN step (§3).
- **Literal-string ledger convention** (unchanged): `Cacao Tree To Be Planted` is a plain string in
  the `Transactions`/`offchain transactions` `Inventory Type` column, never a `Currencies` tab row.
  All three new items follow the same convention — no `Currencies` tab changes anywhere in this plan.
- **No new tracking tab needed** (a change from the very first draft's assumption): a ledger balance
  for `Cacao Tree Purchased - Not Planted` **per farmer** is just the sum of that farmer's `+`/`-`
  rows on that item — matching FIFO consumption is a ledger-balance query, the same pattern already
  used elsewhere in this ledger (per-contributor, per-currency balances). PR3's reconciliation reads
  that balance directly; nothing separate to maintain.

### 1.2 The four-item model, end to end

| Ledger item | Category | Booked by |
|---|---|---|
| `Cacao Tree To Be Planted` | Liability (customer) | Existing sale-time code (untouched, §0.2) — **and discharged by the link event's own write (§1.4), not by editing the sales handler** |
| `Cacao Tree Purchased - Not Planted` | Asset | `[TREE PURCHASE EVENT]` (new, PR2) |
| `Cacao Tree - To Be Paid For` | Liability | Reconciliation step (PR3), when a confirmation has no open purchase balance to match |
| `Cacao Tree Planted - Unassigned` | Asset (the settled pool) | Reconciliation step (PR3, Path A match) or `[FARMER PAYMENT EVENT]` (PR4, Path B settlement of an uncommitted unit) |

Two farmer-side entry paths converge on the pool, exactly as first modeled:

- **Path A (DAO pays first):** PR2 books `+1 Purchased - Not Planted`. Confirmation arrives (PR3),
  matches the open balance → `-1 Purchased - Not Planted` / `+1 Planted - Unassigned`. No new cash —
  it already moved in PR2.
- **Path B (farmer plants first):** confirmation arrives with no open purchase balance (PR3) →
  `+1 Cacao Tree - To Be Paid For` directly, on **main ledger always** (§0.3). Eventually paid (PR4):
  if the unit was never linked to a QR in the meantime → `-1 To Be Paid For` / `+1 Planted -
  Unassigned` (cash lands here, on the funding/main ledger). If it **was** already linked (tagged
  "committed" — see §1.4) → `-1 To Be Paid For` only, paid **directly from the linked QR's own
  ledger**, no pool entry created (it's already spoken for).

### 1.3 Why the existing customer liability booking is left alone, and how it still gets discharged

`sales_update_managed_agl_ledgers.js` already books `+1 "Cacao Tree To Be Planted"` on every sale.
This plan does not modify that file (§0.2). But the ledger still needs to end up accurate once a QR
is fulfilled — so the **link event** (PR5, in `process_tree_planting_link.gs`, a completely different
handler) writes its own **independent** `-1 Cacao Tree To Be Planted` reversal at link time. This
gives an accurate, fully-reconciled ledger without ever touching the sales code path.

### 1.4 The link event — two source variants, and when a transfer fires

| Source | Link event's ledger effect | What's left open |
|---|---|---|
| `Cacao Tree Planted - Unassigned` (settled pool) | `-1 Cacao Tree To Be Planted` / `-1 Planted - Unassigned`. **If the pool unit's ledger differs from the QR's own ledger, also fire the reimbursement transfer** (§0.3): claiming ledger `-cash`, the ledger that actually funded the pool unit `+cash`. | Nothing — fully closed, transfer settles any cross-ledger attribution. |
| `Cacao Tree - To Be Paid For` (confirmed, farmer unpaid) | `-1 Cacao Tree To Be Planted` only. | The farmer liability stays open, tagged **committed to `<qr_code>`** — this reuses the existing `SunMint Tree Planting` columns `Linked QR Code` / `Linked At` (already written by the current handler), no new column needed. A later `[FARMER PAYMENT EVENT]` against this unit checks that column, sees it's committed, and discharges directly (§1.2, Path B, second branch) — paid from the QR's own ledger, **no transfer needed**, because the payment event already knows which ledger to charge. |

### 1.5 Every signed event this plan introduces or touches

| Event | Signer | Ledger effect |
|---|---|---|
| `[TREE PURCHASE EVENT]` (new) | Governor | `-cash` + `+N Cacao Tree Purchased - Not Planted` on the funding/main ledger |
| `[TREE PLANTING EVENT]` (existing, unchanged) | Farmer's own identity | None directly — triggers PR3's reconciliation |
| Reconciliation match (new) | System identity (§0.7's default) | `-1 Purchased-Not-Planted / +1 Planted-Unassigned` (match found) **or** `+1 Cacao Tree - To Be Paid For` on main (no match) |
| `[FARMER PAYMENT EVENT]` (new) | Governor | `-cash` + either `-1 To Be Paid For` only (committed unit, paid from the linked QR's ledger) or `-1 To Be Paid For / +1 Planted-Unassigned` (uncommitted, paid from funding/main) |
| `[TREE PLANTING LINK EVENT]` (existing, revised) | Governor (already the one handler with real server-side enforcement) | `-1 Cacao Tree To Be Planted` always, plus §1.4's source-dependent effect |
| Reimbursement transfer | Governor | `-cash` on the claiming ledger, `+cash` on the ledger that funded the pool unit — fires only inside the link event's pool-source case, only when ledgers differ |

**Hard invariant, unchanged from draft 2:** no raw sheet edit ever writes to any of these ledger rows
or to the `Linked QR Code` / `Linked At` / tree-evidence columns. Every write is one of the six events
above.

### 1.6 Image association at link time (unchanged)

- **Tree-level link:** `process_tree_planting_link.gs` already copies the SunMint submission's photo
  (col I) onto the QR row. Unchanged.
- **Plot-level link (net-new, PR6):** resolve a representative image from the target plot's media
  collection (`farm_media_manifests`, same source plots already use for their boundary hull — see
  `AGROVERSE_SUNMINT_FARM_LISTING.md`'s Fazenda Clara precedent), written to the QR row alongside a
  new "Linked Plot ID" column (PR1). The live `SunMint Plots` tab (§1.7) is the plot registry to join
  against — it already carries `Plot ID`, `Farm ID`, `Media`, `Coordinates`.

### 1.7 Tab inventory — `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` (verified live 2026-09-20)

This is the spreadsheet Gary linked — the same one every `[…EVENT]` type's Telegram-log-fallback
lands on (tab `Telegram Chat Logs`, gid `0`), plus one dedicated tab per event type. Full list (37
tabs) pulled live via the Sheets API (`market_research/google_credentials.json` service account):

`Telegram Chat Logs`, `Plot Invalidation`, `Media Retraction`, `Farm Boundary Evidence`, `SunMint
Plots`, `SunMint Registered Farms`, `Tree Growth Measurements`, `SunMint Tree Planting`, `Tree
Planting Link`, `Inventory Movement`, `Program Registrations`, `Credentialing Attestation Events`,
`Credentialing Events`, `Asset Receipts`, `New Contributor`, `Warmup Sends`, `Dapp Permission
Changes`, `Stores Visits Field Reports`, `Store Adds`, `Capital Injection`, `Proposal Submissions`,
`QR Code Generation`, `QR Code Sales`, `Donation Pledge`, `QR Code Update`, `Voting Rights Cash-Outs`,
`Scored Expense Submissions`, `Document Notarizations`, `States`, `OpenClaw Beer Hall updates`,
`SeaCoast Logistic Email Message Log`, `Currency Creation`, `Currency Conversion`, `Partner
Check-ins`, `Repackaging Settlement`, `payouts`.

**The six relevant to this plan, with their live current headers:**

| Tab | Live columns (2026-09-20) | Relevance |
|---|---|---|
| `SunMint Tree Planting` (gid `176124122`) | Telegram Update ID, Telegram Chatroom ID, Telegram Chatroom Name, Telegram Message ID, **Contributor Name**, Contribution Made, Status date, Telegram File IDs, Photo of Tree Planted, Submitted Name, Latitude, Longitude, Status, Specie, GitHub Commit URL, Cost of Tree, Tree Planting Time, **Linked QR Code**, **Linked At**, **Plot ID** | Already has `Linked QR Code`/`Linked At` (the reused "committed" signal) and a `Plot ID` column — confirms plots are already tracked per-submission today, upstream of this plan. **`Contributor Name`** (verified DAO identity), not `Submitted Name` (free text), is the correct match key for PR3's farmer-balance lookup. No `Ledger`/`AGL` column at all — confirms ledger attribution genuinely isn't knowable at confirmation time (§0.3). |
| `Tree Planting Link` (gid `1868446525`) | Row Number, Telegram Update ID, QR Code, SunMint Submission Message ID, Outcome, Reason, Processed Timestamp, Updated By | Existing dedup/outcome tracking tab from the parent plan's PR4 — unchanged by this plan. |
| `Asset Receipts` (gid `77510441`) | Telegram Update ID, Processed At (ISO), **Currency Name**, Amount, Fund Handler, **Offchain Row**, Status | The reuse target for `[TREE PURCHASE EVENT]` (§0.9). `Offchain Row` confirms it targets one canonical (main) offchain tab, not a chosen managed ledger. |
| `payouts` (gid `606329241`) | created_at_utc, telegram_update_id, program_slug, submission_source, recipient_pk_hash, amount, currency, **tree_planting_id**, bank_ref_type, bank_ref, paid_at, receipt_url, status, supersedes_row, error_message | The reuse target for `[FARMER PAYMENT EVENT]` (§0.10) — `tree_planting_id` is already exactly the join key PR4 needs. No ledger/offchain-row reference field, unlike `Asset Receipts` — supports the §0.10 caveat that this may currently be log-only. |
| `SunMint Plots` (gid `526449180`) | Plot ID, Farm ID, Plot Name, Hectares, Status, Boundary Authority, Plot Type, Owner, Region, Verified At, Media, Notes, Coordinates, Latitude, Longitude, Invalidated By, (blank), Invalidated At, Invalidated Reason | Plot registry PR6 joins against for the plot-fallback link and its representative image. |
| `SunMint Registered Farms` (gid `2011737890`) | Telegram Update ID, Telegram Chatroom ID, Telegram Chatroom Name, Telegram Message ID, Contributor Name, Contribution Made, Status date, Telegram File IDs | Farm registry — potentially useful later for mapping a farm to "its own" managed ledger (§0.3's self-funded path), not required for v1 (§0.9's caveat). |

### 1.8 New tabs and columns actually needed

**No new tabs.** Every event this plan introduces reuses an existing tab (§1.7) or an existing
ledger `Transactions`/`offchain transactions` tab (for the three new literal-string items, same
convention as `Cacao Tree To Be Planted` — no `Currencies` row, no dedicated tab).

**New columns:**

| Sheet | New column | Purpose |
|---|---|---|
| `Agroverse QR codes` (tokenomics ledger `1GE7PUq…`) | **Linked Plot ID** | PR6's plot-fallback link target — no equivalent column exists today (checked against the full A–AB schema in `SUNMINT_TREE_QR_LINKING_PLAN.md` §1.2 and `tokenomics/SCHEMA.md`). |
| `SunMint Tree Planting` | **Payment Event Ref** | Records which `[TREE PURCHASE EVENT]`/`[FARMER PAYMENT EVENT]` (its `Telegram Update ID` or `Asset Receipts`/`payouts` row reference) funded this specific confirmed tree — the traceability link Decision 0.6 in the earlier conversation asked for. Nothing existing plays this role; `Cost of Tree` (col P) records an amount, not a reference. |

**No new columns needed on:** `Asset Receipts`, `payouts`, `Tree Planting Link`, `SunMint Plots`,
`Agroverse QR codes`'s existing tree-evidence columns (N/O/P/R), or `SunMint Tree Planting`'s
`Linked QR Code`/`Linked At` (already do the job, §1.4).

### 1.9 `tokenomics/SCHEMA.md` updates needed (PR1 + PR9)

1. Document the three new literal-string ledger items (`Cacao Tree Purchased - Not Planted`,
   `Cacao Tree - To Be Paid For`, `Cacao Tree Planted - Unassigned`) next to the existing `Cacao Tree
   To Be Planted` entry, same "not a `Currencies` row" convention note.
2. `Agroverse QR codes` sheet section — add column **"Linked Plot ID"** to the table (next available
   column after the parent plan's additions).
3. `SunMint Tree Planting` sheet section — this tab isn't documented in `SCHEMA.md` at all yet (only
   in `SUNMINT_TREE_QR_LINKING_PLAN.md` §1.1, which is a plan doc, not the schema reference). **Add a
   proper `SCHEMA.md` section for it** (it's a live, 20-column, actively-written sheet) — full current
   header row, including the already-live `Linked QR Code`/`Linked At`/`Plot ID` (never formally
   schema'd) and the new `Payment Event Ref`.
4. New `SCHEMA.md` sections, similarly missing today, for **`Asset Receipts`**, **`payouts`**, and
   **`SunMint Plots`** — all three are live, actively-written tabs with zero `SCHEMA.md` presence.
   Document their current real headers (§1.7) verbatim.
5. `tokenomics/API.md` / `API_ENDPOINTS.md` — register `[TREE PURCHASE EVENT]` (or note it's an
   `[ASSET RECEIPT EVENT]` variant, §0.9) and `[FARMER PAYMENT EVENT]` (or note it generalizes the
   existing payout mechanism, §0.10) and the reconciliation match's system-signed event.

### 1.10 GAS projects — what's missing, and where

| Project (script id) | File(s) | What's missing for this plan |
|---|---|---|
| `asset_receipt_ingest` (`1o2lzpdTZBYTTFdXzWJoATxznbqL959b_O7_no2Gd-OV4ryOPZOsqxtpU`), file `Code.gs`. Deployed: `.../AKfycbzcXBXYKmKiYg-tS2cqf60gWVm0ro17ndWVMnxNkc0dimaGUW3CYoi4b8nMZzVbENaw/exec`. | `Code.gs` | **Likely nothing for v1** (§0.9) — verify `Currency Name` isn't allowlist-restricted to existing values; if it is, add the three new literal strings to that allowlist. **Not locally mirrored** (`tokenomics/clasp_mirrors/` has no directory for this script id) — needs a `clasp pull` before this verification, flagged as PR2's first step rather than assumed. |
| QR-codes project (`1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v`) | `process_tree_planting_link.gs` | PR5: remove the old `+1 "Cacao Tree Planted"` write; add the two-source-variant logic (§1.4), the reimbursement transfer, and the plot-fallback branch (PR6). |
| SunMint Tree Planting project (`1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF`) | `process_tree_planting_telegram_logs.gs` | PR3: new reconciliation function — on each new `NEW` row, query the `Cacao Tree Purchased - Not Planted` ledger balance for that farmer (`Contributor Name`, §1.7), match or book the liability, write `Payment Event Ref`, emit the system-signed reconciliation event. |
| `qr_code_web_service.js` project (`1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT`) — **same project that already implements** `processPayoutEventsFromTelegramChatLogs` (per `GAS_SCRIPT_PROPERTIES.md`) | `qr_code_web_service.js` (+ wherever the payout handler's own file is — not yet identified locally, needs a `clasp pull`) | PR4: §0.10's source-level check first (does it book real ledger legs today?), then either generalize the existing handler or add the missing booking logic alongside the existing `payouts` tracking write. Also add the "already-linked → pay from that QR's ledger" branch (§1.2, Path B second branch), which nothing existing does today. |
| `dao_protocol` (`truesight_dao_client/server/dispatch.py`) | `dispatch.py` | **Verified live 2026-09-20, a real discrepancy found:** despite `GAS_SCRIPT_PROPERTIES.md` claiming `[TREE PLANTING EVENT]` / `[TREE PLANTING REJECT EVENT]` / payout routing entries exist ("#149/#150"), the live `ROUTING` table has **none of them** — only `[TREE PLANTING LINK EVENT]` and `[ASSET RECEIPT EVENT]` are actually routed. All three others rely solely on their GAS cron fallback (minutes-scale delay) today. Add routing entries for `[TREE PURCHASE EVENT]`/`[FARMER PAYMENT EVENT]` (PR2/PR4, latency optimization, same pattern as every other row) — and flag the stale-doc discrepancy for a docs fix (PR9), separately from this plan's own scope. |
| `dao_client` (`truesight_dao_client/modules/`) | `report_asset_receipt.py` (exists) · no `report_payout_event.py` (CLI gap — only a DApp page, `dapp_beta/report_payout_event.html`, exists today) | Confirmed: `[ASSET RECEIPT EVENT]`'s CLI already exists, reusable as-is for `[TREE PURCHASE EVENT]` (§0.9) — **no new CLI needed for PR2**. A CLI wrapper for the payout/farmer-payment side doesn't exist yet — worth adding in PR4 if a CLI (not just the DApp page) is wanted for governor use. |

---

## 2. Authorization envelope (§5e — ask once, not per PR)

| Surface | Envelope |
|---|---|
| `tokenomics` GAS source files | Pre-authorized — feature branch + PR per unit, human reviews before merge. |
| `tokenomics` clasp deploy | **Always-stop gate (§5c: production deploy).** Ask once per PR that needs it. |
| `dao_client` / `dao_protocol` | Pre-authorized — low blast radius, feature branch + PR. |
| `dapp_beta` (plot-picker UI additions) | Pre-authorized for beta. Prod promotion is a separate later ask. |
| **Any ledger-writing event** (`[TREE PURCHASE EVENT]`, `[FARMER PAYMENT EVENT]`, `[TREE PLANTING LINK EVENT]`'s ledger effect, the reimbursement transfer, and the RUN step in general) | **Always-stop gate (§5c: TDG/money).** |
| **Backfilling Paulo's known-unbooked payout (§1.1)** | Falls under the ledger-money gate above — first real use of PR2/PR4, not bundled into a docs PR. |
| **UAT (§5)** | Always-stop gate. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | `tokenomics/SCHEMA.md` updates per §1.9 (five items: three ledger literals, `Agroverse QR codes`'s new "Linked Plot ID" column, first-ever `SCHEMA.md` sections for `SunMint Tree Planting`/`Asset Receipts`/`payouts`/`SunMint Plots`). Add "Linked Plot ID" to `Agroverse QR codes` and "Payment Event Ref" to `SunMint Tree Planting` (§1.8) — the only two real schema changes; everything else in §1.9 is documenting sheets that already exist live but were never written up. | `tokenomics` (docs + two schema columns) |
| **PR2** | `clasp pull` the `asset_receipt_ingest` project (§1.10, not yet locally mirrored) and verify `Currency Name` isn't allowlist-restricted. If it's open-ended: **no code change** — `[TREE PURCHASE EVENT]` ships as documentation (submit via the existing `report_asset_receipt.py` CLI with `Currency = "Cacao Tree Purchased - Not Planted"`) plus a `dispatch.py` routing entry for latency (§1.10). If restricted: add the three new literal strings to the allowlist. | `tokenomics` (+ `dao_protocol` for routing) |
| **PR3** | Extend `process_tree_planting_telegram_logs.gs` (SunMint Tree Planting project, §1.10): on each new confirmed submission, query the `Cacao Tree Purchased - Not Planted` ledger balance for that farmer (`Contributor Name`, §1.7 — FIFO). Match found → `-1 Purchased-Not-Planted / +1 Planted-Unassigned`, write `Payment Event Ref`, **emit the system-signed reconciliation event**. No match → `+1 Cacao Tree - To Be Paid For` on main ledger. | `tokenomics` |
| **PR4** | First, `clasp pull` the `qr_code_web_service.js` project (§1.10) and confirm §0.10: does the existing payout handler book real ledger legs today, or only log to `payouts`? Then either generalize it or add the missing booking. New/generalized `[FARMER PAYMENT EVENT]` handler: governor picks a confirmed-unpaid SunMint row for a farmer. Checks `Linked QR Code`: populated → pay from that QR's own ledger, `-1 To Be Paid For` only. Empty → pay from funding/main ledger, `-1 To Be Paid For / +1 Planted-Unassigned`. **First real use, once built, is the Paulo backfill (§1.1) — under the ledger-money gate (§2).** | `tokenomics` + `dao_protocol` |
| **PR5** | Revise `process_tree_planting_link.gs` per §1.3/§1.4: independent `-1 Cacao Tree To Be Planted` write (new code path, sales handler untouched) always fires; source-dependent effect (pool vs. unpaid-liability) as specified; reimbursement transfer fires only in the cross-ledger pool case. Everything else in the handler (DApp gate, email, reject path) untouched. | `tokenomics` |
| **PR6** | Plot-level link path: accept a plot id (from `sunmint/plots/index.geojson`) as an alternative to a SunMint submission row for the batch tool's repeat/no-email case. Writes "Linked Plot ID" + a representative image per §1.6. Needs its own consumption accounting (a plot represents many trees' worth of pool supply, not one) — small design pass at PR6 start. | `tokenomics` + `dapp_beta` |
| **PR7** | Batch allocation tool: given all `SOLD`-unlinked QRs and all eligible confirmed units (`Planted-Unassigned` pool **and** `To Be Paid For` confirmed-unpaid rows, per §0.4), compute the pairing per Decision 0.5 and drive PR5/PR6's link event once per pair — governor-confirmed dry-run before real execution. | `dao_client` (CLI/script) |
| **PR8** | Aging report for stalled `Purchased - Not Planted` balances and `To Be Paid For` liabilities — per Decision 0.8's default (passive report). Non-blocking, can slip. | `dao_client` or `truesight_autopilot` |
| **PR9** | Docs: finalize `tokenomics/SCHEMA.md` (§1.9), `tokenomics/API.md` new events, this plan's resume tracker, `CONTEXT_UPDATES.md` entry, and a `GAS_SCRIPT_PROPERTIES.md` correction for the routing-table discrepancy found in §1.10 (the doc claims `[TREE PLANTING EVENT]`/`[TREE PLANTING REJECT EVENT]`/payout routing exists; live `dispatch.py` has none of them). | `tokenomics` / `agentic_ai_context` |
| **RUN** | (a) Backfill Paulo's known payout via PR2+PR4 (§1.1). (b) First real batch-link run via PR7. **Ledger-money + batch-execution gate (§2) — needs explicit `go`.** | — |
| **UAT** | See §5. **Always-stop gate.** | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (SCHEMA.md updates + the two real new columns, §1.9). Fresh roadmap, reverted
> same-day to real ledger items after the draft-2 simplification proved to drop real accrual
> information — nothing has started.
>
> **Open before certain units:** PR2 and PR4 each start with a `clasp pull` verification step (§1.10,
> §0.9/§0.10) — neither project is locally mirrored today, so the exact scope of "generalize existing
> handler" vs. "add new booking logic" isn't fully known until that pull happens. PR3 needs Decision
> 0.7 confirmed (proposed default stated, doesn't block starting). PR8 needs Decision 0.8 confirmed —
> non-blocking, can slip past RUN.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (SCHEMA.md updates + Linked Plot ID + Payment Event Ref columns) | ☐ | ☐ | ☐ |
| PR2 (verify/extend `asset_receipt_ingest`; `[TREE PURCHASE EVENT]` + routing) | ☐ | ☐ | ☐ |
| PR3 (reconciliation match in `process_tree_planting_telegram_logs.gs`, system-signed) | ☐ | ☐ | ☐ |
| PR4 (verify/generalize `payouts` handler; `[FARMER PAYMENT EVENT]`) | ☐ | ☐ | ☐ |
| PR5 (revise `process_tree_planting_link.gs`) | ☐ | ☐ | ☐ |
| PR6 (plot-level link path + image resolution) | ☐ | ☐ | ☐ |
| PR7 (batch allocation tool) | ☐ | ☐ | ☐ |
| PR8 (aging report — pending Decision 0.8; non-blocking) | ☐ | ☐ | ☐ |
| PR9 (docs, incl. the GAS_SCRIPT_PROPERTIES.md routing-table correction) | ☐ | ☐ | ☐ |
| RUN (Paulo backfill + first real batch link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** current QR/link status counts, the existing handler's exact
behavior, the existing sale-time booking's exact behavior (and why it's left alone), the ledger
literal-string convention, the full four-item model, the live tab inventory (§1.7), the new-columns
list (§1.8), the SCHEMA.md gap list (§1.9), and the GAS-project map (§1.10) are all captured in §1.
Decisions 0.7 and 0.8 are genuine open governor calls, not undiscovered facts. The `clasp pull`
verifications flagged for PR2/PR4 are genuine unknowns (the projects aren't locally mirrored) — they
don't block starting PR1, but PR2/PR4 each begin with that check rather than assuming the answer.

---

## 5. UAT — synthetic data first, then the real Paulo backfill

Same principle as the parent plan's §10: exercise real code paths, never submit a real `[SALES
EVENT]` for a test, use a clearly-test-labeled QR, invalidate it afterward.

| Step | Surface | What to expect | Acceptance criterion |
|---|---|---|---|
| 1 | `[TREE PURCHASE EVENT]` for a test farmer/ledger, N=5 | `-cash` + `+5 Purchased-Not-Planted` booked | Correct amounts, correct ledger |
| 2 | Test `[TREE PLANTING EVENT]` for the same farmer | Matches → `-1 Purchased-Not-Planted / +1 Planted-Unassigned`, no new cash | Reclass correct, system-signed event present |
| 3 | A 6th test confirmation (purchase balance exhausted) | No match → `+1 Cacao Tree - To Be Paid For` on main | Liability booked correctly on main regardless of farmer's usual ledger |
| 4 | Link a test `SOLD` QR against the unpaid unit from step 3 | `-1 Cacao Tree To Be Planted` only; SunMint row's `Linked QR Code`/`Linked At` now populated (the commitment signal) | QR shows linked; `To Be Paid For` liability still open on main |
| 5 | `[FARMER PAYMENT EVENT]` against that same committed unit | Pays from the linked QR's own ledger; `-1 To Be Paid For` only, no new pool entry | No phantom pool unit created; correct paying ledger |
| 6 | Link a test QR against a `Planted-Unassigned` pool unit funded by a **different** ledger than the QR's own | `-1 Cacao Tree To Be Planted` / `-1 Planted-Unassigned` + reimbursement transfer fires | Both ledgers show correct legs, governor-signed |
| 7 | Plot-level link (PR6) against a repeat-email test QR | QR gets a plot id + representative image, not a single tree photo | Correct plot reference + image |
| 8 | Batch tool (PR7) dry-run against real (not test) data | Proposed pairing list, no execution | Governor reviews before any real link fires |
| 9 | **Real RUN**: Paulo's 10-tree payout backfilled via PR2+PR4 | Ledger shows the real historical expense | Matches Gary's own account of what was actually paid |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first) before starting the next unit.

---

## 7. Open items carried forward

- Decision 0.7 (automatic vs. governor-confirmed reconciliation match) and 0.8 (aging policy) — both
  flagged, neither blocks PR1.
- PR6's plot-level consumption accounting (one plot represents many trees' worth of supply) needs its
  own small design pass when PR6 starts.
- Whether the reconciliation match's "system identity" should be a dedicated identity or reuse an
  existing one (e.g. the autopilot's own DAO signing identity) — pick at PR3, not a blocking unknown.
- §0.9's caveat: `asset_receipt_ingest` only books onto the main ledger today — self-funded-by-a-
  specific-managed-ledger purchases (§0.3's other path) are a phase-2 enhancement, not v1, unless PR2
  decides to extend it.
- §0.10's open question (does the existing `payouts` handler book real ledger legs or only log) is
  the single biggest unknown left in this plan — resolve it first thing in PR4, before scoping the
  rest of that PR.
- A CLI wrapper for the farmer-payment side (`dao_client`, mirroring `report_asset_receipt.py`)
  doesn't exist yet — only the DApp page does. Worth adding in PR4 if governor CLI use is wanted.
