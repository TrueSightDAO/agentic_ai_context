# SunMint Farmer Settlement + Batch QR-Tree Linking — Execution Roadmap

**Status:** design ruled (2026-09-20; revisions **+ one retraction** same day — see history below); no code yet.
**⚠️ Decision 0.12 RETRACTED** (purchases stay **main-only**); units PR2b/PR3.2 **withdrawn**.
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
4. **Retraction (same day):** Decision 0.12 — "purchases fundable from any ledger" — was ruled then **retracted** by Gary (*"We should only have it on the main"*). Purchases stay **main-only**; the redesign (§8.3/§8.4) is cancelled, units PR2b/PR3.2 are withdrawn, and §8 is kept as a **record**. See §0.12/§8.
5. **Clarity fix (same day):** after the retraction, §0.9's row lead-in and the §7 bullet both read *"RETRACTED"* — which conflated the **caveat** (which STANDS) with **Decision 0.12** (which was retracted). Reworded to **"Caveat REINSTATED … it was Decision 0.12 that was retracted, not this."** No substance change; removes a misread risk.

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
| 0.9 | **`[TREE PURCHASE EVENT]` reuses the existing `[ASSET RECEIPT EVENT]` mechanism** | Verified live 2026-09-20 (§1.10): the `Asset Receipts` tab + `asset_receipt_ingest` GAS project + `dao_client`'s existing `report_asset_receipt.py` CLI already do exactly this shape (pay cash, book an offchain asset row). No new event, no new CLI needed for v1 — submit with `Currency = "Cacao Tree Purchased - Not Planted"`. **Caveat REINSTATED 2026-09-20 (Gary, same day) — the main-only caveat STANDS; it was Decision 0.12 that was retracted, not this.** Gary first ruled (Decision 0.12) the purchase asset must be bookable on any ledger, then **retracted that rule**: *"We should only have it on the main."* So `[TREE PURCHASE EVENT]` stays `[ASSET RECEIPT EVENT]` + `Currency = "Cacao Tree Purchased - Not Planted"` **booked on main only** — the original v1 shape. The ledger-target extension (**PR2b**) and the reconciliation generalization (**PR3.2**) are **withdrawn** (never built). PR3/PR5/PR7 as-built already assume main-only, so **no merged code needs reverting** — see §8. |
| 0.10 (RESOLVED 2026-09-20) | **`[FARMER PAYMENT EVENT]` generalizes the existing CFR `payouts` mechanism, pending a source-level check** | The live `payouts` tab (§1.7) already has the right shape (`tree_planting_id`, `bank_ref`, `receipt_url`, `program_slug`) and its Tier-1 writes are confirmed unaffected by the CFR-specific Tier-2 blocker. **Not yet confirmed:** whether its GAS handler currently books real ledger legs (`-cash`/`-Liability`/`+Asset`) or only logs to the tracking tab — needs a `clasp pull` check on the `qr_code_web_service.js` project (§1.10) before PR4 starts, since that determines how much of PR4 is "generalize" vs. "build from scratch alongside an existing tracking tab." **RESOLVED 2026-09-20 (source-level check done):** the handler is **log-only** — `process_payout_event_telegram_logs.js` (action `processPayoutEventsFromTelegramChatLogs`) writes only to the Tier-1 `payouts` + Tier-2 `payout events` tracking tabs; its sole "ledger" mention is a comment and no file in the project writes a ledger row. **⇒ PR4 = BUILD the missing booking alongside the existing tracking tab (not "generalize").** |

| 0.11 (RESOLVED 2026-09-20) | **Committed-unit `[FARMER PAYMENT EVENT]`: one leg or a cross-ledger transfer?** | Ruled by Gary: emit the **cross-ledger transfer (3 legs, not 1)**. Cash must come from the ledger the QR code is associated with — that is where the cash provision for the tree actually sits. If the QR is linked to a tree whose liability is on main, cash transfers **FROM the QR's own ledger TO main**. This simultaneously (1) discharges the customer-side liability on the QR's own ledger, (2) discharges the farmer-payment liability (`-1 To Be Paid For`) on main, and (3) resolves the DAO's negative balance from having pre-paid. **Supersedes the earlier "no transfer needed" wording in §1.4/§1.5 for the committed variant** (corrected below). |
| 0.12 (**RETRACTED 2026-09-20**) | **`Cacao Tree Purchased - Not Planted` must be assignable to ANY managed ledger** | **RULED then RETRACTED by Gary the same day.** He first ruled it (*"Cacao tree purchased - not yet planted needs to be assignable to any ledger…"*), which would have promoted §0.9's phase-2 caveat to a v1 architecture change and triggered unit PR2b (§8). **He then retracted:** *"We should only have it on the main."* ⇒ the purchase asset stays **main-only**; **PR2b** (any-ledger ingest) and **PR3.2** (reconciliation reads funding ledger) are **withdrawn** (never built). PR3–PR7b as-built assume main-only ⇒ **correct, nothing to revert.** §8 is retained as a **record only**. |
| 0.13 (RULED 2026-09-20) | **The `Cacao Tree To Be Planted` liability currency literal is PER-LEDGER, not constant** | Flagged by Gary; **VERIFIED TRUE against live data 2026-09-20** (treasury-cache `managed-ledgers/*.json` summaries + the main ledger's `offchain transactions` Currency column): the **main** ledger books the sale-time liability as `Cacao Tree To Be Planted` *(mixed case)*, while **managed ledgers** book it as `CACAO TREE TO BE PLANTED` *(UPPERCASE)* — live on **SEF1** (4 rows), **PP1** (2 rows), **AGL6** (44 rows). The managed-ledger contributor is likewise suffixed per-ledger (`SunMint Tree Planting Contract - <agl>`, `RESERVATION_EVENT_SPEC.md` leg 3). **This is a silent defect in already-merged PR5**, which hard-codes the mixed-case main literal unconditionally (`process_tree_planting_link.js` `TPL_CUSTOMER_LIABILITY_LITERAL`, L81) — see **§8.5**. **Requirement RULED; fix design = unit PR5.2 — standalone, and INDEPENDENT of the retracted Decision 0.12.** This is the *customer-side* liability, located by which ledger the **SALE** booked on, so it is unaffected by where the purchase asset sits. No code until sign-off. |

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
- **Verified live 2026-09-20 — real, uncleaned test-data residue already exists**, directly relevant
  to this plan's UAT hygiene (§5): main ledger `offchain transactions` rows 4133/4134 and 4135/4136
  (from the parent plan's 2026-08-22 `TEST_AGL4_20260822_2`/`_3` runs) booked real `-1`/`+1`
  `Cacao Tree To Be Planted`/`Cacao Tree Planted` pairs that were never reversed — only the QRs
  themselves got `INVALIDATED`. The main ledger's `Cacao Tree Planted` balance is overstated by +2
  units right now. Remediation proposed, not executed, in §5.10.

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
| `Cacao Tree - To Be Paid For` (confirmed, farmer unpaid) | `-1 Cacao Tree To Be Planted` only. | The farmer liability stays open, tagged **committed to `<qr_code>`** — this reuses the existing `SunMint Tree Planting` columns `Linked QR Code` / `Linked At` (already written by the current handler), no new column needed. A later `[FARMER PAYMENT EVENT]` against this unit checks that column, sees it's committed, and discharges directly (§1.2, Path B, second branch) — the committed payment emits a **cross-ledger transfer (3 legs)** (§0.11, Gary 2026-09-20): cash transfers **from the QR's own ledger to main**, discharging the customer-side liability on the QR's own ledger, the farmer liability on main, and the DAO's pre-paid negative balance. (Supersedes the earlier "no transfer needed" wording.) |

### 1.5 Every signed event this plan introduces or touches

| Event | Signer | Ledger effect |
|---|---|---|
| `[TREE PURCHASE EVENT]` (new) | Governor | `-cash` + `+N Cacao Tree Purchased - Not Planted` **on main** (Decision 0.12 retracted 2026-09-20 — purchases stay main-only) |
| `[TREE PLANTING EVENT]` (existing, unchanged) | Farmer's own identity | None directly — triggers PR3's reconciliation |
| Reconciliation match (new) | System identity (§0.7's default) | `-1 Purchased-Not-Planted / +1 Planted-Unassigned` (match found) **or** `+1 Cacao Tree - To Be Paid For` on main (no match) |
| `[FARMER PAYMENT EVENT]` (new) | Governor | **Committed ⇒ cross-ledger transfer (3 legs)** (§0.11): `-cash` on the linked QR's own ledger, `+cash` on main, `-1 To Be Paid For` on main. **Uncommitted ⇒** `-cash` on funding/main + `-1 To Be Paid For / +1 Planted-Unassigned` on main. |
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
| `payouts` (gid `606329241`) | created_at_utc, telegram_update_id, program_slug, submission_source, recipient_pk_hash, amount, currency, **tree_planting_id**, bank_ref_type, bank_ref, paid_at, receipt_url, status, supersedes_row, error_message | The reuse target for `[FARMER PAYMENT EVENT]` (§0.10) — `tree_planting_id` is already exactly the join key PR4 needs. No ledger/offchain-row reference field, unlike `Asset Receipts` — supports the §0.10 caveat that this may currently be log-only. **PR4 correction (2026-09-20):** re-verified at source — `[PAYOUT EVENT]` was **already routed** (`dispatch.py` → `processPayoutEventsFromTelegramChatLogs`, #170) **and already catalogued** with `Tree Planting IDs` among its canonical labels, so a tree-id-bearing payout already flows end-to-end; **no `[FARMER PAYMENT EVENT]` tag and no routing entry were needed**. The handler now **books** the ledger legs from `tree_planting_id` (PR4 step 2, `tokenomics#534`). |
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
| SunMint Tree Planting project (`1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF`) | `process_tree_planting_telegram_logs.gs` | PR3: new reconciliation function — on each new `NEW` row, query the `Cacao Tree Purchased - Not Planted` ledger balance for that farmer (`Contributor Name`, §1.7), match or book the liability, write `Payment Event Ref`, emit the system-signed reconciliation event. **PR3.2 (§8):** currently reads the balance from **main only** (`contributorsSheetId`) — must be generalized to the funding ledger under Decision 0.12. |
| `qr_code_web_service.js` project (`1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT`) — **same project that already implements** `processPayoutEventsFromTelegramChatLogs` (per `GAS_SCRIPT_PROPERTIES.md`) | `qr_code_web_service.js` (+ wherever the payout handler's own file is — not yet identified locally, needs a `clasp pull`) | PR4: §0.10's source-level check first (does it book real ledger legs today?), then either generalize the existing handler or add the missing booking logic alongside the existing `payouts` tracking write. Also add the "already-linked → pay from that QR's ledger" branch (§1.2, Path B second branch), which nothing existing does today. |
| `dao_protocol` (`truesight_dao_client/server/dispatch.py`) | `dispatch.py` | **Corrected 2026-09-20 (PR2) — the previous claim here was *wrong*, not merely stale:** an earlier draft said the live `ROUTING` table had *none* of the tree-planting/payout entries. Re-verified against `dispatch.py` while executing PR2: it **does** route `[TREE PLANTING EVENT]` → `processTreePlantingTelegramLogs` (#149, 2026-08-29), `[TREE PLANTING REJECT EVENT]` → `processTreePlantingLinksFromTelegramChatLogs` (#150, 2026-08-30), `[PAYOUT EVENT]` → `processPayoutEventsFromTelegramChatLogs` (#170, 2026-09-17), plus `[TREE PLANTING LINK EVENT]` and `[ASSET RECEIPT EVENT]`. So **no routing entry was needed for PR2**. PR4 may still add a `[FARMER PAYMENT EVENT]` entry if that new event is introduced (same latency-optimization pattern); no `[TREE PURCHASE EVENT]` entry is needed, since purchases submit as the already-routed `[ASSET RECEIPT EVENT]`. PR9's `GAS_SCRIPT_PROPERTIES.md` "correction" item therefore shrinks to a confirmation. **PR4 confirmation (2026-09-20), fully verified at source:** the `[PAYOUT EVENT]` route (#170) already carries tree-id payouts and the catalog already lists `Tree Planting IDs` — so PR4 added **no** `[FARMER PAYMENT EVENT]` entry (introducing a declared-but-unrouted tag would be drift, which `test_catalog_dispatch_coverage.py` exists to catch). PR4 instead extended the `PAYOUT EVENT` catalog semantics + a regression pin (`dao_protocol#174`). |
| `dao_client` (`truesight_dao_client/modules/`) | `report_asset_receipt.py` (exists) · no `report_payout_event.py` (CLI gap — only a DApp page, `dapp_beta/report_payout_event.html`, exists today) | Confirmed: `[ASSET RECEIPT EVENT]`'s CLI already exists, reusable as-is for `[TREE PURCHASE EVENT]` (§0.9) — **no new CLI needed for PR2**. A CLI wrapper for the payout/farmer-payment side doesn't exist yet — worth adding in PR4 if a CLI (not just the DApp page) is wanted for governor use. **Not closed in PR4 (2026-09-20):** PR4 reused the existing `[PAYOUT EVENT]` path (DApp page + Telegram), so no CLI wrapper was added — flag as a possible PR4.1 if a governor-facing CLI is later wanted. |

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
| **PR2** ✅ (docs-only, `tokenomics` #530) | `clasp pull` the `asset_receipt_ingest` project and verify `Currency Name` isn't allowlist-restricted. **Result: open-ended** (handler auto-creates the `Currencies` row), so **no code change** — documented `[TREE PURCHASE EVENT]` as the `[ASSET RECEIPT EVENT]` + `Currency = "Cacao Tree Purchased - Not Planted"` convention in `API.md` §10/§11 + `API_ENDPOINTS.md`. **No `dispatch.py` entry needed** — `[ASSET RECEIPT EVENT]` is already routed. | `tokenomics` |
| ~~**PR2b**~~ (WITHDRAWN 2026-09-20 — Decision 0.12 retracted) | **Cancelled; never built.** Was to extend the `[ASSET RECEIPT EVENT]` ingest (`asset_receipt_ingest/Code.gs`) with a ledger-target field so `Cacao Tree Purchased - Not Planted` could book on any managed ledger, mirroring `[DAO Inventory Expense Event]`'s `Target Ledger`. Gary retracted the underlying rule (*"We should only have it on the main"*) ⇒ purchases stay main-only and this unit is **cancelled**. Struck here for audit; the analysis is kept in §8. | — |
| **PR3** | Extend `process_tree_planting_telegram_logs.gs` (SunMint Tree Planting project, §1.10): on each new confirmed submission, query the `Cacao Tree Purchased - Not Planted` ledger balance for that farmer (`Contributor Name`, §1.7 — FIFO). Match found → `-1 Purchased-Not-Planted / +1 Planted-Unassigned`, write `Payment Event Ref`, **emit the system-signed reconciliation event**. No match → `+1 Cacao Tree - To Be Paid For` on main ledger. **PR3 as-built is correct under the retracted 0.12** — it reads main, and main is the only ledger purchases book on (the PR3.2 generalization is withdrawn). | `tokenomics` |
| **PR4** | First, `clasp pull` the `qr_code_web_service.js` project (§1.10) and confirm §0.10: does the existing payout handler book real ledger legs today, or only log to `payouts`? Then either generalize it or add the missing booking. New/generalized `[FARMER PAYMENT EVENT]` handler: governor picks a confirmed-unpaid SunMint row for a farmer. Checks `Linked QR Code`: populated ⇒ **cross-ledger transfer** (§0.11): `-cash` on the QR's own ledger / `+cash` on main / `-1 To Be Paid For` on main. Empty ⇒ `-cash` on funding/main + `-1 To Be Paid For / +1 Planted-Unassigned` on main. **First real use, once built, is the Paulo backfill (§1.1) — under the ledger-money gate (§2).** | `tokenomics` + `dao_protocol` |
| **PR5** | Revise `process_tree_planting_link.gs` per §1.3/§1.4: independent `-1 Cacao Tree To Be Planted` write (new code path, sales handler untouched) always fires; source-dependent effect (pool vs. unpaid-liability) as specified; reimbursement transfer fires only in the cross-ledger pool case. Everything else in the handler (DApp gate, email, reject path) untouched. | `tokenomics` |
| **PR5.2** (Decision 0.13; **design pending sign-off**, then gated GAS deploy — the **only** §8-era unit that survives the 0.12 retraction) | Resolve the tree-liability **currency literal per ledger** instead of hard-coding main's. Live data shows main uses `Cacao Tree To Be Planted` (mixed case) but managed ledgers use `CACAO TREE TO BE PLANTED` (uppercase). PR5's `TPL_CUSTOMER_LIABILITY_LITERAL` must become a **per-ledger lookup** (main/+AGL4 → mixed case; managed → uppercase), and the `Planted - Unassigned` / `To Be Paid For` literals checked the same way. Without this, a managed-ledger QR link writes a **spurious second liability** (the ingest auto-creates a `Currencies` row for any new literal — PR2) instead of discharging the real one. | `tokenomics` |
| **PR6** | Plot-level link path: accept a plot id (from `sunmint/plots/index.geojson`) as an alternative to a SunMint submission row for the batch tool's repeat/no-email case. Writes "Linked Plot ID" + a representative image per §1.6. Needs its own consumption accounting (a plot represents many trees' worth of pool supply, not one) — small design pass at PR6 start. | `tokenomics` + `dapp_beta` |
| **PR7** | Batch allocation tool: given all `SOLD`-unlinked QRs and all eligible confirmed units (`Planted-Unassigned` pool **and** `To Be Paid For` confirmed-unpaid rows, per §0.4), compute the pairing per Decision 0.5 and drive PR5/PR6's link event once per pair — governor-confirmed dry-run before real execution. | `dao_client` (CLI/script) |
| **PR8** | Aging report for stalled `Purchased - Not Planted` balances and `To Be Paid For` liabilities — per Decision 0.8's default (passive report). Non-blocking, can slip. | `dao_client` or `truesight_autopilot` |
| **PR9** | Docs: finalize `tokenomics/SCHEMA.md` (§1.9), `tokenomics/API.md` new events, this plan's resume tracker, `CONTEXT_UPDATES.md` entry, and a `GAS_SCRIPT_PROPERTIES.md` **confirmation** for the §1.10 routing check (the doc's claim that `[TREE PLANTING EVENT]`/`[TREE PLANTING REJECT EVENT]`/payout routing exists is **correct** — PR2's re-verification found the earlier "none of them" wording in this plan was itself the error, now fixed). | `tokenomics` / `agentic_ai_context` |
| **RUN** | (a) Backfill Paulo's known payout via PR2+PR4 (§1.1). (b) First real batch-link run via PR7. **Ledger-money + batch-execution gate (§2) — needs explicit `go`.** | — |
| **UAT** | See §5. **Always-stop gate.** | — |

---

## 4. Resume tracker

> **RESUME HERE → RUN (ledger-money gate, HELD by Gary) — **PR7b complete 2026-09-20** (`dao_protocol` #176, `c537ce1f`). PR7b collapsed the PR7 over-count: eligible `SunMint Tree Planting` rows are grouped to **one unit per physical tree** by **photo-URL identity** (138 rows → 125 trees; 50 duplicate rows collapsed), because Gary's *option (b)* row-level key (col A `Telegram Update ID`) duplicates **identically to col D** and would not have fixed it — the twins are byte-identical re-ingests of the same tree, and the handler links only the first `NEW` row. A tree group is skipped if **any** of its rows is already linked, so a linked tree is never re-offered. Live re-run: **9/9 pairings → distinct trees**. Dry-run default + `--execute` needs `--yes` unchanged. Verified: tests **18/18**, full pytest **206 passed** (pre-existing fails/collection-errors unchanged, re-confirmed on `main`). **No ledger event, no `clasp` deploy.** **⚠️ Decision 0.12 RETRACTED 2026-09-20:** Gary first ruled the purchase asset assignable to any ledger, then retracted (*"We should only have it on the main"*). Purchases stay **main-only**; units **PR2b/PR3.2 are WITHDRAWN** (never built); **no merged code needs reverting** (PR3–PR7b as-built assume main-only ⇒ correct). §8 kept as a record; the only survivor is **PR5.2** (Decision 0.13). **Decision 0.13 (§8.5):** the tree-liability currency literal is **per-ledger** (main=`Cacao Tree To Be Planted`; managed=`CACAO TREE TO BE PLANTED`) — verified live; PR5's hard-coded literal is a **silent money-path defect** (unit PR5.2). Next: **RUN** — Paulo's 10-tree backfill (§1.1) + first real batch link — under the **ledger-money gate (§2): explicit governor go only**, and **Gary has personally held it** (*“Don’t do the live run… let me look at it and decide”*). Open prerequisite before RUN: the **`SunMint Plots` `Contributor Name` (col T) backfill**, now reframed by Gary as **proximity-computed** (“the plot is linked to the farm by proximity”) rather than manually typed — scoped as a **separate follow-up** (🚩 open questions filed in `OPEN_FOLLOWUPS.md`), not built; until done, plot links fail closed.

> **PR5 shipped 2026-09-20 — `tokenomics` #536 (`458729e`); GAS source-only (no deploy):** rewrote the link-time ledger effect in `process_tree_planting_link.js` per §1.3/§1.4. Removed the old fixed `-1 Cacao Tree To Be Planted` / `+1 Cacao Tree Planted` pair. New pure, I/O-free `tplComputeLegs_(opts)` (mirrors PR4's `fpeComputeLegs_`): always `-1 Cacao Tree To Be Planted` (customer-liability discharge, §1.3) on the QR's own managed ledger (or main when the QR routes to main); **pool source** also `-1 Cacao Tree Planted - Unassigned` (on main, where PR3 books pool units) **plus the reimbursement transfer** (`-cash` QR ledger / `+cash` main) **only when the QR's ledger ≠ main**; **committed source** = the discharge leg alone. New `tplResolveSource_(farmer)` derives the source from the farmer's aggregate `Planted - Unassigned` balance (≥1 ⇒ pool, else committed) — never throws, fails closed to committed; this mirrors PR3's farmer-aggregate FIFO abstraction, so the ledger derives the accounting fact rather than trusting an external submitter's claim (Envoy confirmed 2026-09-20, rejecting a payload source-hint). New `tplWriteLegs_` appends each leg and flags a partial write without rollback (Sheets has no cross-sheet transaction; §5.9c precedent); `appendTreePlantingLedgerFulfillment_` rewired to resolve source → compute legs → write, never throwing. Call site now passes the SunMint row's `Contributor Name` (col J = idx 9) + `Cost of Tree` (col P = idx 15). Untouched: the governor gate, email path, reject path, up-front managed-ledger resolution guard, and **every sale-time code path (§0.2)**. Verified: `node --check` clean, no duplicate global consts in the shared GAS project, harness **14/14** (`scripts/tree_planting_link_harness.mjs`), pytest guard **10/10** (`scripts/test_tree_planting_link_guard.py`), `tokenomics` `pytest scripts/` **81→91**. **No `clasp push`/deploy** and no ledger event executed (both always-stop gates). One number flagged for review: §1.4 gives the transfer legs as bare `±cash`; PR5 uses the SunMint `Cost of Tree` (col P) as the per-tree cash a funding ledger fronted.
>
> **PR6 shipped 2026-09-20 — `tokenomics` #537 (`50db2849`) + `dapp_beta` #103 (`83e613c3`); GAS source-only (no deploy):** added the **plot-level link path** (§1.6) to `process_tree_planting_link.js`. A link event may now carry a **`Plot ID`** instead of a SunMint submission message id. New helpers `tplParsePlotId_`, `tplResolvePlotRow_`, `tplResolvePlotContributor_` (reads `SunMint Plots` **col T `Contributor Name`**), `tplPickPlotImage_`/`tplResolvePlotImage_` (first `kind:image` `url`, else first video `thumbnail`), and a plot-fallback branch mirroring the SunMint-row block (resolve → write QR `Linked Plot ID` AC + photo + plot lat/lng → book via PR5's `appendTreePlantingLedgerFulfillment_`). **Farmer identity is resolved from the registry, never the payload** (Envoy, 2026-09-20 — option 2; option 3's per-submission assertion contradicts the PR5 “ledger derives the fact” ruling, and option 1's fuzzy name-match could misattribute a real payment discharge to the wrong farmer, a worse failure mode than a blocked link). **Fails closed** (`REJECTED`) when the Plot ID is unknown or its `Contributor Name` is blank. **Consumption accounting (the design pass §1.6 flagged):** a plot spans many trees' worth of pool supply, but a link event consumes exactly **one** pool unit (1:1 — the plot is the evidence/target, not a multiplier), same as a tree-level link. **No cash legs** for a plot link: a plot has no per-tree `Cost of Tree`, so the pool-source reimbursement-transfer amount is unbookable; the discharge + `Planted - Unassigned` inventory legs still book. `dapp_beta` `link_tree_planting.html` gains a **plot picker** (options from `sunmint/plots/index.geojson`), mutually exclusive with the submission picker; Reject stays tree-submission-only. New schema: `SunMint Plots`.`Contributor Name` (col T). Verified: `node --check` clean, no duplicate global consts, harness **14→28** (`scripts/tree_planting_link_harness.mjs`), pytest guard **10→16** (`scripts/test_tree_planting_link_guard.py`), full `pytest -q` **96→102** passed (the 6 pre-existing `schema_validation` collection errors unchanged). **No `clasp push`/deploy** and no ledger event executed. ⚠️ **Data note for Gary (separate from this code):** the `SunMint Plots` `Contributor Name` backfill for the 22 existing plots is a field-knowledge task (who actually owns/planted each), not derivable from any existing table — until populated, plot links fail closed (correct).
>
> **PR7 shipped 2026-09-20 — `dao_protocol` #175 (`94d0b142`), the `dao_client` package (repo `dao_client` redirects to `dao_protocol`); no ledger event, no deploy:** the batch allocation tool — `truesight_dao_client/modules/batch_link_sunmint.py` + a `truesight-dao-batch-link-sunmint` entry point. `compute_allocations(qrs, tree_units, plots)` is a **pure** function (unit-testable without any sheet): it sorts the SOLD‑unlinked QR backlog deterministically (sold date, then QR code) and walks it per Decision 0.5 — a **distinct, not-yet-used owner email claims a specific photographed tree 1:1**; a **repeat email or a blank email takes a plot association**, and **plots are reusable** (round-robin over the eligible set, since a plot spans many trees' worth of supply). `--max-links` caps the run; anything past the cap (or with no available unit of either kind left) is reported **unallocated**, never silently dropped. `build_link_attributes()` emits **exactly one** of `SunMint Submission Message ID` (tree) / `Plot ID` (plot) — matching the PR6 GAS parser contract verbatim; farmer identity stays **server-side** (this tool never asserts it). Sheet loaders: the sold-unlinked QR set (`SOLD` / `TREE_PLANTING_FUNDS_TRANSFERRED`, no `Linked Plot ID`), eligible tree units (`SunMint Tree Planting` status `NEW`, photographed, unlinked), and plots with a registry-held `Contributor Name` (**col T**, fail-closed). **Safety:** dry-run is the **default**; `--execute` **refuses without `--yes`** (rc=2) and fires nothing — the link event books ledger rows, i.e. the plan's **ledger-money gate**. **Catalog:** `TREE PLANTING LINK EVENT` gains the **`Plot ID`** label + `required_fields` relaxes to `[QR Code]` (PR6 shipped the label in GAS/dapp only, so `lookup_event_docs` had been under-reporting the contract). Verified: `compileall` OK, `ruff check`/`format --check` clean, new pure-core tests **12/12** (`tests/test_batch_link_sunmint.py`, incl. an execute-without-`--yes` refusal), full `dao_protocol` pytest **200 passed** (main baseline **188** — the 5 failures + 2 collection errors are pre-existing, verified by running `main`). **No ledger event, no `clasp push`/deploy.**
>
> **PR7b shipped 2026-09-20 — `dao_protocol` #176 (`c537ce1f`); no ledger event, no deploy:** **Gary's *option (b)*, as literally stated, was a no-op — the live PR7 dry-run falsified its premise, so this ships the fix that actually delivers his rule (“one signed RSA per tree”).** Gary's intent was right and the over-count was real: the first live dry-run showed **138 eligible `SunMint Tree Planting` rows resolving to only 125 distinct trees** (9 duplicate groups), and the allocator proposed **3 QRs onto one tree**. But the 13 “extra” rows are **byte-for-byte identical in every column** — same photo URL, lat/long and planting timestamp (`hashlib` full-row hash: 138 rows → 125 distinct) — and **col A (`Telegram Update ID`) carries the *same* duplication as col D** (both 138 → 125), so a col-A key would not have distinguished them. Root cause: a Telegram message **ingested more than once**, not “several trees in one message” — the link handler matches by Message ID and stamps the first `NEW` row `LINKED`, so a twin row is a redundant artifact. **The real row-level tree key is the physical tree, whose identity is its photo URL** (the batch filenames are literally `bomsucesso_tree01…tree10`). Fix: new pure `select_tree_units()` **groups eligible rows by photo-URL identity and emits one unit per physical tree** (carrying `identity`/`source_row`/`duplicate_rows` for audit), and **skips a group entirely if *any* of its rows is already linked (col R)** so a linked tree can never be re-offered via a leftover twin. `compute_allocations()` also de-dupes defensively by identity. **Live re-run after the fix: 125 tree units (was 138), 50 duplicate rows collapsed, 9/9 pairings map to *distinct* trees.** Dry-run default + `--execute`-needs-`--yes` **unchanged**. Verified: `compileall` + `ruff check`/`format --check` clean, tests **18/18** (6 new), full `dao_protocol` pytest **206 passed** (5 pre-existing failures + 2 pre-existing collection errors re-confirmed on `main`). **No ledger event, no `clasp push`/deploy.** 🚩 **RUN held:** Gary — *“Don’t do the live run… let me look at it and decide”* — no `--execute` until he reviews personally and gives explicit go.
>
> **⚠️ Open decision surfaced at PR3 (§0.7 / §7) — needs Gary's confirmation before deploy, non-blocking:** the plan asks for a *system-signed* reconciliation event, but **GAS holds no signing key** — it cannot emit an RSA-signed event the way Edgar / `edgar_client.py` does. PR3 therefore uses the codebase's existing handler-effect pattern (direct, idempotent append whose `Description` names the system identity, triggered by the farmer's own already-signed `[TREE PLANTING EVENT]` — same as `appendTreePlantingLedgerFulfillment_`). Promoting the match to a *fully signed* event needs a dedicated system signing identity; §7 says "pick at PR3" — this is the pick, flagged rather than silently assumed.
>
> **PR2 shipped 2026-09-20 — `tokenomics` #530 (`6149616`), docs-only:** the `clasp pull` on `asset_receipt_ingest` resolved both of §1.10's open questions — (1) **`Currency Name` is open-ended** (the handler auto-creates the `Currencies` row for any new literal, so **no allowlist change** was needed → PR2 took the docs-only branch, documenting `[TREE PURCHASE EVENT]` as the `[ASSET RECEIPT EVENT]` + `Currency = "Cacao Tree Purchased - Not Planted"` convention in `API.md` §10/§11 and `API_ENDPOINTS.md`); and (2) **§1.10's routing claim was *wrong*, not merely stale** — live `dispatch.py` *does* route `[TREE PLANTING EVENT]` (#149), `[TREE PLANTING REJECT EVENT]` (#150), `[PAYOUT EVENT]` (#170), `[TREE PLANTING LINK EVENT]`, and `[ASSET RECEIPT EVENT]`, so **no routing entry was needed either** (§1.10 corrected below; PR9's doc-correction item shrinks to a no-op). **PR1 shipped 2026-09-20 — `tokenomics` #529
> (`e8bdc2a`):** §1.9's five doc items done (three ledger literals under a new *Tree-Planting Ledger
> Literals* section, `Linked Plot ID` AC on `Agroverse QR codes`, `Payment Event Ref` U on `SunMint
> Tree Planting`, and first-ever sections for `SunMint Plots` / `Asset Receipts` / `payouts`). Note: the
> plan's claim that `SunMint Tree Planting` was undocumented was **stale** — it was already documented
> A–S; only `Plot ID` was missing, added here. (The `clasp pull` in PR2 is a read, not a deploy — it
> does not hit the GAS always-stop gate, which applies to `clasp push`.)
>
> **Open before certain units:** PR2/PR4's `clasp pull` verifications are **done** — §0.9's Currency allowlist is open-ended (PR2) and §0.10's payout handler is log-only (PR4 builds the booking). §0.11 is ruled. Remaining open: Decision 0.7 (reconciliation-match automation — default stated) and Decision 0.8 (aging policy), both non-blocking.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☑ | ☑ |
| PR1 (SCHEMA.md updates + Linked Plot ID + Payment Event Ref columns) | ☑ | ☑ | ☑ |
| PR2 (verify/extend `asset_receipt_ingest`; `[TREE PURCHASE EVENT]` + routing) | ☑ | ☑ | ☐ | <!-- Contribution = explicit-go gate; evidence tokenomics#530 -->
| PR3 (reconciliation match in `process_tree_planting_telegram_logs.gs`, system-signed) | ☑ | ☑ | ☐ | <!-- + PR3.1 idempotency guard: tokenomics#532 (merged 49e362f) -->
| PR4 (verify/generalize `payouts` handler; `[FARMER PAYMENT EVENT]`) | ☑ | ☑ | ☐ | <!-- Merged tokenomics#533/#534/#535 + dao_protocol#174; reuses [PAYOUT EVENT]; partial-write coverage #535. Contribution = explicit-go gate -->
| PR5 (revise `process_tree_planting_link.gs`) | ☑ | ☑ | ☐ | <!-- Merged tokenomics#536; balance-derived source discriminator + cross-ledger transfer; harness 14/14 + guard 10/10. Contribution = explicit-go gate -->
| PR6 (plot-level link path + image resolution) | ☑ | ☑ | ☐ | <!-- Merged tokenomics#537 (50db2849) + dapp_beta#103 (83e613c3); registry-resolved farmer (SunMint Plots col T Contributor Name, fail-closed), Linked Plot ID AC + plot image (image→video-thumbnail), no cash legs (no Cost of Tree), 1:1 consumption; harness 28/28 + guard 16/16. Contribution = explicit-go gate -->
| PR7 (batch allocation tool) | ☑ | ☑ | ☐ | <!-- Merged dao_protocol#175 (94d0b142); Decision 0.5 (distinct-email→tree 1:1, repeat/blank→reusable plot round-robin), dry-run default + `--execute` needs `--yes`, catalog `Plot ID` label; tests 12/12, suite 200 vs 188. Contribution = explicit-go gate -->
| PR7b (one tree unit per physical tree — dedupe over-count) | ☑ | ☑ | ☐ | <!-- Merged dao_protocol#176 (c537ce1f); live dry-run exposed 138 rows → 125 distinct trees; collapse by photo-URL identity. Contribution = explicit-go gate -->
| ~~PR2b~~ (any-ledger `Purchased - Not Planted` — **WITHDRAWN**, Decision 0.12 retracted) | — | — | — |
| ~~PR3.2~~ (PR3 reads funding ledger — **WITHDRAWN**, Decision 0.12 retracted) | — | — | — |
| PR5.2 (per-ledger liability currency literal — Decision 0.13; **design pending sign-off**, §8.5 — **survives** the 0.12 retraction) | ☐ | ☐ | ☐ |
| PR8 (aging report — pending Decision 0.8; non-blocking) | ☐ | ☐ | ☐ |
| PR9 (docs, incl. the GAS_SCRIPT_PROPERTIES.md routing-table correction) | ☐ | ☐ | ☐ |
| RUN (Paulo backfill + first real batch link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

> **Contribution column note:** PR2's Contribution box is left ☐ on purpose — filing contribution reports (and any TDG) is an **explicit-governor gate**, so it is not auto-filed as part of a unit. (PR0/PR1's boxes were ticked during the planner/earlier close-out; happy to re-verify.) Say the word and I'll file the PR1–PR2 contribution reports.

✅ **Pre-flight Completeness (§5d):** current QR/link status counts, the existing handler's exact
behavior, the existing sale-time booking's exact behavior (and why it's left alone), the ledger
literal-string convention, the full four-item model, the live tab inventory (§1.7), the new-columns
list (§1.8), the SCHEMA.md gap list (§1.9), and the GAS-project map (§1.10) are all captured in §1.
Decisions 0.7 and 0.8 are genuine open governor calls, not undiscovered facts. The `clasp pull`
verifications flagged for PR2/PR4 are genuine unknowns (the projects aren't locally mirrored) — they
don't block starting PR1, but PR2/PR4 each begin with that check rather than assuming the answer.

---

## 5. UAT — comprehensive per-scenario test cases, with mandatory cleanup

### 5.0 Test-data hygiene — read before running anything below

**This is not optional cleanup — it's a hard requirement, per `OPERATING_INSTRUCTIONS.md` §5g** ("E2E
test writes — standing authorization, mandatory self-cleanup"): test writes to live sheets/ledgers are
pre-authorized without a per-run governor ask, **on the condition that** (1) every field that ends up
in a human-facing view is unambiguously marked as test data, and (2) every test write that adds value
to a ledger is reversed in the **same turn** it's created — never left for a "later cleanup pass."

**Why this matters here specifically, verified live 2026-09-20 (not hypothetical):** the parent
plan's own 2026-08-22 test runs violated exactly this rule. Ledger rows 4133/4134 (`TEST_AGL4_
20260822_2`) and 4135/4136 (`TEST_AGL4_20260822_3`) on the main ledger's `offchain transactions` tab
each booked a real `-1 Cacao Tree To Be Planted` / `+1 Cacao Tree Planted` pair that was **never
reversed** — only the QR itself got `INVALIDATED`. Right now, today, the main ledger's `Cacao Tree
Planted` balance is overstated by +2 units and `Cacao Tree To Be Planted` is understated by -2, purely
from leftover test data. (One other run, rows 4127/4128, happened to book `0.00000000` and washed out
harmlessly — not by design, by luck.) **§5.6 below proposes the remediation; it is not executed by this
plan without a separate explicit go, since it means editing the live main ledger.**

**Rules for every test case below:**
1. **Tag everything.** QR codes: `TEST_<scenario>_<YYYYMMDD>_<n>`. SunMint submissions: `TEST-
   <scenario>-<YYYYMMDD>-<n>`. Farmer/cooperative name on `[TREE PURCHASE EVENT]`/`[FARMER PAYMENT
   EVENT]`: a clearly fake name, e.g. `Test Farmer <n>`, never a real farmer's name even at $0.01.
2. **Never submit a real `[SALES EVENT]`** to get a test QR to `SOLD` — set the `status` column
   directly via a sheet edit, per the parent plan's own §10 rule (a real sales-pipeline submission
   pollutes real revenue reporting even at $0/$0.01).
3. **Trivial nominal amounts only for cash-moving test events** (`[TREE PURCHASE EVENT]`, `[FARMER
   PAYMENT EVENT]`, the reimbursement transfer) — **$0.01**, not $0 (a $0 sales amount was found to be
   silently dropped as `IGNORED` by a different parser, tokenomics #407 — don't assume $0 is safe
   anywhere in this stack without checking first). These are still real cash-adjacent, governor-signed
   events under this plan's own §2 always-stop gate — run them with Gary present, not unattended.
4. **Reverse every ledger row in the same turn**, immediately after the test case's acceptance
   criterion is confirmed — not "later," not "at the end of the session." Each test case below states
   its own reversing entry explicitly.
5. **Never delete a signed event or a ledger row.** Reverse with an equal-and-opposite entry
   (referencing the original in its description, same convention every existing reversal in this
   workspace uses); invalidate/void a *status*, don't erase a *record*. The audit trail is the point.
6. **Log every run** in §5.7's table — this is what let the 2026-08-22 leftovers be found and named
   precisely just now, instead of being invisible.

### 5.1 TC1 — Path A: purchase, then a matching confirmation (§1.2, Scenario 2)

- **Setup:** none beyond a test farmer name.
- **Steps:** (a) Submit `[TREE PURCHASE EVENT]` (or `[ASSET RECEIPT EVENT]` per §0.9), `Currency =
  "Cacao Tree Purchased - Not Planted"`, `Amount = 1`, `Fund Handler = Test Farmer TC1`, on a test
  managed ledger if one is designated, else main. (b) Submit a test `[TREE PLANTING EVENT]` with
  `Contributor Name = Test Farmer TC1` (must match exactly — §1.7 confirmed this is the reconciliation
  match key).
- **Expected:** (a) books `+1 Cacao Tree Purchased - Not Planted`. (b) PR3's reconciliation matches it
  → `-1 Purchased-Not-Planted / +1 Planted-Unassigned`, no new cash, a system-signed reconciliation
  event is emitted, and the SunMint row's `Payment Event Ref` points at (a)'s event.
- **Cleanup (same turn):** reverse the pool entry with `-1 Planted-Unassigned` (referencing this test
  in its description). Mark the SunMint test row's `Status` via `[TREE PLANTING REJECT EVENT]` (the
  existing, already-proven reject/invalidate mechanism — HANDOFF_MANIFEST's 2026-08-31 note confirms
  "plant → live → invalidate → gone" is fully proven end-to-end) rather than leaving it dangling
  `LINKED`/confirmed forever, unlike the 2026-08-22 precedent.

### 5.2 TC2 — Path B: confirmation with no open purchase balance (§1.2, Scenario 3 step 1)

- **Setup:** a test farmer name with **no** open `Purchased - Not Planted` balance.
- **Steps:** submit a test `[TREE PLANTING EVENT]`, `Contributor Name = Test Farmer TC2`.
- **Expected:** PR3 finds no match → `+1 Cacao Tree - To Be Paid For` booked on **main ledger**
  (regardless of any ledger this farmer might otherwise be associated with — §0.3).
- **Cleanup (same turn):** reverse with `-1 Cacao Tree - To Be Paid For` on main. Invalidate the
  SunMint test row via `[TREE PLANTING REJECT EVENT]`.

### 5.3 TC3 — Link against an unpaid confirmed tree (§1.4, "committed" variant)

- **Setup:** one open `Cacao Tree - To Be Paid For` unit (reuse TC2's mechanics, or a fresh one — don't
  clean up TC2's liability until after this test consumes it, since this test needs it to still exist).
- **Steps:** create a test QR, set `status = SOLD` directly (never a real `[SALES EVENT]`, rule 2).
  Submit `[TREE PLANTING LINK EVENT]` linking that QR to the unpaid SunMint row.
- **Expected:** `-1 Cacao Tree To Be Planted` only. `To Be Paid For` liability **stays open**. SunMint
  row's `Linked QR Code`/`Linked At` populated (the commitment signal, §1.4) — verify this is the
  **only** change to that liability; nothing else moved.
- **Cleanup (same turn):** reverse the `-1 Cacao Tree To Be Planted` write with `+1` (referencing this
  test). Set the QR to `INVALIDATED` (existing convention — never delete). The still-open `To Be Paid
  For` liability carries into TC4 below (that's the point of this pairing) — clean it up there, not
  here, to avoid a double-reversal.

### 5.4 TC4 — Farmer payment against an already-committed unit (§1.2, Scenario 3 step 3, second branch)

- **Setup:** TC3's committed `To Be Paid For` unit (still open at the end of TC3, by design).
- **Steps:** submit `[FARMER PAYMENT EVENT]` against that unit, $0.01 nominal (rule 3), governor-signed,
  Gary present.
- **Expected:** checks the SunMint row's `Linked QR Code` (still populated from TC3, even though that
  QR is now `INVALIDATED` — confirm the payment handler doesn't choke on an invalidated-but-linked QR)
  → emits the **cross-ledger transfer** (§0.11): `-cash` on that QR's own ledger, `+cash` on main, plus `-1 To Be Paid For` on main — **no** new `Planted -
  Unassigned` entry created (verify this explicitly — a phantom pool unit here is the exact bug this
  test exists to catch).
- **Cleanup (same turn):** reverse **both** $0.01 cash legs (equal-and-opposite on each ledger) and
  `+1 Cacao Tree - To Be Paid For` (undoing the discharge). This fully closes out both TC3 and TC4's
  chain — confirm no residual balance remains anywhere for `Test Farmer TC3`/its QR.

### 5.5 TC5 — Link against the settled pool, same ledger (§1.4, pool variant, no transfer)

- **Setup:** a confirmed, paid `Planted - Unassigned` unit already funded on the **same** ledger a
  test QR will belong to (chain TC1's pool entry before its own cleanup, or mint a fresh one on the
  same ledger).
- **Steps:** create a test QR on that same ledger, `status = SOLD` directly. Submit `[TREE PLANTING
  LINK EVENT]` against the pool unit.
- **Expected:** `-1 Cacao Tree To Be Planted` / `-1 Planted - Unassigned`. **No** reimbursement transfer
  fires (same ledger throughout) — explicitly verify no transfer event was emitted.
- **Cleanup (same turn):** reverse both legs (`+1` each, referencing this test). QR → `INVALIDATED`.

### 5.6 TC6 — Link against the settled pool, cross-ledger (§1.4, pool variant, transfer fires)

- **Setup:** a confirmed, paid `Planted - Unassigned` unit funded on ledger A (e.g. main, or a test
  managed ledger). A test QR belonging to a **different** ledger B, `status = SOLD` directly.
- **Steps:** submit `[TREE PLANTING LINK EVENT]` linking ledger B's QR to ledger A's pool unit.
- **Expected:** `-1 Cacao Tree To Be Planted` (ledger B) / `-1 Planted - Unassigned` (ledger A) **+ the
  reimbursement transfer**: `-$0.01` (nominal, rule 3) on ledger B, `+$0.01` on ledger A, governor-
  signed. Verify both ledgers' legs independently — this is the highest-risk case to get wrong (real
  cash crossing ledgers) and the one most worth a second pair of eyes before confirming pass.
- **Cleanup (same turn):** reverse all four legs (two unit legs, two cash legs) with equal-and-opposite
  entries on their respective ledgers. QR → `INVALIDATED`.

### 5.7 TC7 — Plot-level link (PR6)

- **Setup:** a test QR with a **repeat email** (reuse an email already on another test QR) or **no
  email at all**, `status = SOLD` directly. A test plot id in `SunMint Plots` (or reuse an existing
  real plot — read-only reference, no write needed to the plot registry itself).
- **Steps:** submit the plot-fallback variant of `[TREE PLANTING LINK EVENT]` with a plot id instead of
  a SunMint submission id.
- **Expected:** QR gets "Linked Plot ID" populated + a representative image from that plot's media
  collection (not a single tree's photo). Ledger effect follows §1.4 same as a tree-level link, sourced
  from whatever pool/liability unit PR6's consumption accounting resolves for that plot.
- **Cleanup (same turn):** reverse whatever ledger legs fired (per whichever source variant applied,
  same as TC5/TC6's cleanup shape). QR → `INVALIDATED`. No write to `SunMint Plots` itself to clean up
  if it was read-only.

### 5.8 TC8 — Batch tool dry-run (PR7)

- **Setup:** none — this reads real (not test) data by design.
- **Steps:** run the batch allocator in dry-run mode against the real backlog of `SOLD`-unlinked QRs
  and eligible confirmed units.
- **Expected:** a proposed pairing list is produced. **No link event fires, no ledger write occurs.**
- **Cleanup:** none needed — nothing was written. If the tool has no dry-run mode yet, this test case
  is the reason to build one before PR7 is considered done, not a workaround for its absence.

### 5.9 TC9 — Real RUN: Paulo's 10-tree payout backfill (§1.1)

- **Setup:** this is **not a test** — it's the first real production use, backfilling Gary's own
  already-known unbooked payout. No `TEST_` labeling, no cleanup step, because nothing here should be
  reversed — it's real.
- **Steps:** submit the real `[TREE PURCHASE EVENT]`/`[FARMER PAYMENT EVENT]` for Paulo's 10 trees at
  their real historical amount, under the ledger-money gate (§2), governor present.
- **Expected:** ledger shows the real historical expense, matching Gary's own account. This is the
  plan's actual deliverable, not a rehearsal.
- **No cleanup** — verify instead: re-read the booked rows back and confirm they match what Gary
  actually recalls paying, same as every other "never trust a self-report" verification pattern used
  throughout this workspace.

### 5.9b TC10 — PR3 reconciliation idempotency (added on Envoy review, 2026-09-20)

- **Setup:** a test farmer (`Test Farmer TC10`) with an **open** `Cacao Tree Purchased - Not Planted` balance (one `[TREE PURCHASE EVENT]`, §5.1 mechanics), plus one `[TREE PLANTING EVENT]`.
- **Steps:** (a) submit the planting event → PR3 books Path A once. (b) **Re-fire the reconciliation for the same SunMint row** without creating a new row (re-run `processTreePlantingFromTelegramChatLogs`, or simulate a duplicate delivery / status re-set to `NEW`).
- **Expected:** the second invocation **books nothing** — the row-level idempotency guard (`tokenomics` #532) detects the already-written `SunMint Tree Planting row N` marker in the ledger `Description` and returns early. The `Cacao Tree Purchased - Not Planted` balance moves exactly once; no second `-1/+1` pair appears.
- **Why:** PR3's only gate is `rowStatus === 'NEW'`; the upstream `processedMessageIds` dedup is read-once and protects the *message*, not the *row* (it does not cover a status re-set, a duplicate delivery inside one run, or a manual re-run), and Path B writes nothing back to the row. This TC proves the guard closes that hole.
- **Cleanup (same turn):** reverse Path A's pool entry (`-1 Planted-Unassigned`, referencing this test) and the purchase (`-1 Purchased-Not-Planted`). Invalidate the SunMint test row via `[TREE PLANTING REJECT EVENT]`.

### 5.9c TC11 — PR4 partial-write (added on Envoy review, 2026-09-20)

- **Setup:** the PR4 booking path in a **3-leg** scenario (committed payment, §0.11) where one target tab is unresolvable mid-write — e.g. the QR’s own ledger resolves but the main `offchain transactions` tab is missing.
- **Steps:** fire a tree-id-bearing `[PAYOUT EVENT]` whose `Linked QR Code` is populated, with the main-ledger leg’s target absent so leg 1 lands and legs 2–3 fail.
- **Expected:** the handler books **no** further legs, does **not** throw, and the Tier-1 tracking row records `status = LEDGER_NOT_BOOKED` with `error_message = PARTIAL_WRITE_1_OF_3` (the already-landed leg is **not** rolled back). Fully-failed boundary ⇒ `PARTIAL_WRITE_0_OF_3`.
- **Why:** Sheets has no cross-sheet transaction, so a mid-write failure is inherently un-rollback-able — the correct design is to **flag loudly, never hide**. This TC pins that the partial-write case is *tested* (not merely implicit) and that the inconsistency is surfaced for human reconciliation.
- **Cleanup (same turn):** reverse the single landed leg (reference this test), and clear the test Tier-1 row’s `status`/`error_message`.
- **Executable proof:** `tokenomics` #535 — `scripts/payout_event_guard_harness.mjs` (3 cases: `PARTIAL_WRITE_1_OF_3`, `PARTIAL_WRITE_0_OF_3`, and an end-to-end asserting the tracking row reads `LEDGER_NOT_BOOKED` + `PARTIAL_WRITE_1_OF_3`).

### 5.9d TC12 — PR5 link-time source variants + fail-closed (added on PR5, 2026-09-20)

- **Setup:** a `[TREE PLANTING LINK EVENT]` whose QR resolves to a managed ledger; exercise both source branches (an open pool unit vs none) and both same-ledger/cross-ledger routing cases.
- **Steps:** (a) file the link with the farmer holding **no** open pool balance ⇒ **committed**; (b) file it with an open `Cacao Tree Planted - Unassigned` unit and the QR on **main** ⇒ **pool, same-ledger**; (c) same, QR on a **managed** ledger ⇒ **pool, cross-ledger**; (d) make the main `offchain transactions` tab unresolvable mid-write ⇒ partial write.
- **Expected:** (a) exactly **one** `-1 Cacao Tree To Be Planted` leg; (b) **two** legs (`-1 To Be Planted` + `-1 Planted - Unassigned` on main), **no cash legs**; (c) **four** legs incl. the transfer (`-cash` QR / `+cash` main, amount = SunMint `Cost of Tree`); (d) no throw, legs already landed **not** rolled back, the partial write surfaced (index of the failed leg) in the log.
- **Why:** pins that the source is **derived from the ledger balance** (not asserted by the submitter) and that the transfer fires **only** across ledgers — the two accounting invariants §1.4's bare prose leaves implicit.
- **Cleanup (same turn):** reverse every leg booked by the test, and re-zero the farmer's `Planted - Unassigned` balance if the setup seeded one.
- **Executable proof:** `tokenomics` #536 — `scripts/tree_planting_link_harness.mjs` (14 cases: committed/pool × same/cross-ledger, the discriminator, and a `NO_MAIN_TAB` partial-write) + `scripts/test_tree_planting_link_guard.py` (10 source-invariant guards).

### 5.9e TC13 — PR6 plot-level link + registry-resolved farmer (added on PR6, 2026-09-20)

- **Setup:** a sold QR with a managed ledger; a `SunMint Plots` row (a) with `Contributor Name` set, (b) with it blank, (c) absent.
- **Steps:** (a) file `[TREE PLANTING LINK EVENT]` with `- Plot ID: <known>`; (b) same with a plot whose `Contributor Name` is blank; (c) a nonexistent Plot ID; (d) a plot with a `kind:image` asset; (e) a plot (e.g. `V-06-29`) with **only** video assets.
- **Expected:** (a) QR `Linked Plot ID` (col AC) written + representative image attached + ledger legs booked sourced from the **plot's** `Contributor Name`; (b) & (c) **fail closed** (`REJECTED`, no QR write, no ledger leg); (d) the `kind:image` URL attached; (e) the first video's **`thumbnail`** attached (no throw). A plot link books **no cash legs** (no per-tree `Cost of Tree`). Exactly **one** pool unit is consumed (1:1).
- **Why:** pins that (i) farmer identity comes from the **registry, not the payload**, (ii) a plot's many-trees-worth of supply still consumes only one unit per link, and (iii) the image-resolution fallback + the fail-closed paths hold — the three invariants §1.6 leaves implicit.
- **Cleanup (same turn):** reverse every leg booked by the test, clear the QR's `Linked Plot ID`/photo, and re-zero the farmer's `Planted - Unassigned` balance if seeded.
- **Executable proof:** `tokenomics` #537 — `scripts/tree_planting_link_harness.mjs` (28 cases incl. plot resolve, blank-name fail-closed, image-vs-thumbnail, non-200 fetch) + `scripts/test_tree_planting_link_guard.py` (16 source-invariant guards).


### 5.9f TC14 — PR7 batch allocation tool (added on PR7, 2026-09-20)

- **Setup:** a mix of SOLD‑unlinked QRs — two sharing one owner email, one with a **blank** email, one with a **distinct** email; a set of eligible `SunMint Tree Planting` units (status `NEW`, photographed, unlinked) **smaller** than the distinct-email count; and one reusable plot with a registry `Contributor Name`.
- **Steps:** (a) run `truesight-dao-batch-link-sunmint --dry-run` and inspect the plan; (b) `--execute` **without** `--yes`; (c) `--execute --yes` against a **test** ledger with the plan capped via `--max-links`; (d) re-run the same command.
- **Expected:** (a) a deterministic plan: each **distinct** email → a tree (1:1), the **repeat** email and the **blank** email → the **same reusable plot** (round-robin), and any QR with no unit left listed as **unallocated** (never dropped); (b) **rc=2**, nothing submitted, no ledger row written; (c) one `[TREE PLANTING LINK EVENT]` per planned pair, each carrying **exactly one** of `SunMint Submission Message ID` / `Plot ID`, farmer resolved server-side (never from the payload); (d) the already-linked QRs drop out of the plan (the loader excludes them) — **no double link**.
- **Why:** pins the three invariants the tool exists to guarantee — Decision 0.5's allocation priority, that a **plot is reusable** while a **tree is 1:1**, and that the money-writing path is **gated behind `--yes`** in addition to the §2 ledger-money gate.
- **Cleanup (same turn):** reverse every leg booked by the test and clear each test QR's link columns (`Linked Plot ID` / photo), same shape as TC5–TC7.
- **Executable proof:** `dao_protocol` #175 — `tests/test_batch_link_sunmint.py` (12 pure-core cases: each Decision-0.5 branch, plot reuse, `--max-links` cap, determinism, the either/or attribute contract, and the execute-without-`--yes` refusal).
- **PR7b invariants (added on the PR7 live dry-run, 2026-09-20):** (i) **one unit per physical tree** — rows describing the same tree (identical photo URL) collapse to a single unit; (ii) a tree group is **skipped when *any* of its rows is already linked** (col R), so a linked tree is never re-offered via a leftover twin; (iii) **no two pairings ever share a target tree** (1:1 preserved even under duplicate input); (iv) distinct trees with a shared Message ID stay distinct. Live evidence: 138 rows → **125 units**, **9/9** pairings → distinct trees. (Root cause: col A duplicates identically to col D — the *photo-URL identity* is the row-level tree key, not col A.)
- **Executable proof (PR7b):** `dao_protocol` #176 — `tests/test_batch_link_sunmint.py` adds 6 cases (18/18 total) for the four invariants above.
### 5.10 Historical residue — proposed remediation, not executed here

Per §5.0's finding: rows 4133/4134 and 4135/4136 on the main ledger's `offchain transactions` tab
(from the parent plan's 2026-08-22 test runs, QRs `TEST_AGL4_20260822_2`/`_3`, both already
`INVALIDATED`) were never reversed. **Proposed fix, pending Gary's go** (editing the live main ledger
is not something this plan does unprompted): append one reversing pair per leftover test —
`+1 Cacao Tree To Be Planted` / `-1 Cacao Tree Planted`, each referencing the original row number and
this plan's remediation note in its description, contributor `SunMint Tree Planting Contract - agl4`
to match the originals. This is a small, standalone unit — can run before PR1 or any time after,
independent of the rest of this roadmap's sequencing.

### 5.11 Log of runs

Append one row per test case executed, same convention as the parent plan's §10 — so the next person
(or LLM) doesn't have to re-derive what's already been validated, and so a future audit can see every
test's cleanup was actually confirmed, not just planned.

| Date | Test case | Ledger rows touched | Cleanup confirmed? | Notes |
|---|---|---|---|---|
| — | — | — | — | (no UAT run yet — PR0–PR4 are code/docs units; UAT is an always-stop gate, §5) |

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
- §0.9's main-only caveat **REINSTATED 2026-09-20 (Decision 0.12 retracted)** — Gary first ruled the purchase asset
  assignable to **any** ledger, then retracted (*"We should only have it on the main"*). Purchases stay
  **main-only**; units **PR2b** (any-ledger ingest) and **PR3.2** (reconciliation reads funding ledger) are
  **withdrawn**. PR3–PR7b as-built assume main-only ⇒ **correct, nothing to revert.** §8 retained as a
  record; **PR5.2** (Decision 0.13) is the only survivor.
- §0.10 **RESOLVED 2026-09-20** — the `payouts` handler is **log-only**; PR4 BUILDS the missing booking. §0.11 **RULED 2026-09-20** — committed payment = cross-ledger transfer (3 legs).
- A CLI wrapper for the farmer-payment side (`dao_client`, mirroring `report_asset_receipt.py`)
  doesn't exist yet — only the DApp page does. Worth adding in PR4 if governor CLI use is wanted.

---

## 8. Impact assessment — Decision 0.12 (**RETRACTED 2026-09-20**) — purchases fundable from ANY ledger

**Status: RETRACTED by Gary the same day — this assessment is kept as a RECORD ONLY.** The rule "purchases may fund any ledger" was withdrawn (*"We should only have it on the main"*). ⇒ the redesign (§8.3) is **cancelled**, units **PR2b/PR3.2 withdrawn**, and **no code follows from §8.1–8.4**. Only **§8.5** (Decision 0.13 — a separate *customer-side* defect) remains actionable via **PR5.2**.

### 8.1 The v1 assumption being changed

**⚠️ RETRACTED — retained for the record.** §0.9's original v1 simplification was *"all purchases fund main ⇒ pool units live on main."* Gary's (now-retracted) ruling had removed the "fund main" clause: cash can come from **any** managed ledger (incl. main).
The purchase asset (`Cacao Tree Purchased - Not Planted`) must therefore be *bookable on any ledger*,
and every downstream balance read that assumed "main" must be re-examined.

### 8.2 Affected already-merged units (file:line evidence)

| Unit | What it assumes "main" | Breaks if a purchase funds a managed ledger | Severity |
|---|---|---|---|
| **PR3** `reconcileTreePlanting_` (`process_tree_planting_telegram_logs.js` L460-461, L517) | Reads the farmer's open `Purchased - Not Planted` balance **only** from `contributorsSheetId` = main (`1GE7PUq…`); books **Path B on main always** | A managed-ledger purchase is **invisible** → balance reads 0 → **Path B mis-books** (`+1 To Be Paid For` on main) and the FIFO consumption (Path A) never fires → **double-count** (farmer paid twice for one tree). | **HIGH** |
| **PR5** `tplResolveSource_` (`process_tree_planting_link.js` L445-456) | Derives pool-vs-committed by summing `Cacao Tree Planted - Unassigned` **"on the main offchain tab"** (`TPL_MAIN_DAO_LEDGER_URL`) | A pool unit booked on a managed ledger is missed → source wrongly resolves **'committed'** → the `-1 Planted-Unassigned` leg + cross-ledger reimbursement **never fire** → tree over-paid. | **HIGH** |
| **PR3/PR5 pool concept** (`Planted - Unassigned`) | Pool units implicitly live on **main** | Pool balance becomes **per-ledger**; the "farmer-aggregate FIFO" abstraction (sum across one tab) is no longer a single-tab scan. | **HIGH** (conceptual) |
| **PR7** allocator (`batch_link_sunmint.py` L54-57, L305) | Reads eligible units from `SunMint Tree Planting` on Gary's `1qbZZhf…` sheet; QR sheet on main | Reads are **source-agnostic** today, but once pool units are per-ledger the allocator's "settled-pool balance" cap (`--cap`) must be ledger-aware. | **MEDIUM** |
| **PR4** payout booking (`process_payout_event_telegram_logs.js`) | Legs hard-code main vs "QR ledger" via `treePlantingId`; **cash-out leg = `-amount` on the QR's ledger, +cash main** | If the *funding* ledger ≠ QR ledger ≠ main, the 3-leg committed transfer has the **wrong source leg**. Needs a "funding ledger" input. | **MEDIUM** |
| **PR6** plot link path | Resolves farmer from `SunMint Plots` col T; no cash legs | Largely unaffected (no Cost-of-Tree) — **verify** only. | **LOW** |
| **PR2** `[TREE PURCHASE EVENT]` = `[ASSET RECEIPT EVENT]` | Ingest writes offchain leg to a single hard-coded `mainSs` (`ASSET_RECEIPT_MAIN_SPREADSHEET_ID`) | This is the **root**: no ledger-target field exists. Everything else inherits the gap. | **ROOT** |

### 8.3 Candidate design (**MOOT** — 0.12 retracted; design cancelled)

1. **Root (PR2b):** add a ledger-target field to the `[ASSET RECEIPT EVENT]` ingest, mirroring the
   proven `[DAO Inventory Expense Event]`'s `Target Ledger` label (validated server-side against the
   treasury cache `ledgers[]` — entries carry `{ledger_name, ledger_url}`, 19 live). Resolve
   `ledger_name → spreadsheetId` via `Shipment Ledger Listing` L→AB (the same map PR5's
   `resolveManagedLedgerSpreadsheetUrl_` uses). **Default → main when the field is absent**
   (fully backward-compatible).
   - ⚠️ **Trap:** the CLI's existing `Destination Contribution File Location` label is an
     **attachment-pairing** field, NOT a ledger selector. A **distinct** label is required.
2. **PR3.2:** teach `reconcileTreePlanting_` to locate the funding ledger (per-purchase ledger tag)
   rather than scanning main only.
3. **PR5.2 (if needed):** make `tplResolveSource_` scan the funding ledger(s).

### 8.4 Open questions for the governor (**MOOT** — 0.12 retracted; Q1–Q6 no longer needed. **Q7** remains via §8.5)

- **Q1 — Ledger selection:** is the funding ledger chosen **per purchase event** (governor names it at
  submit time), or **inferred** from the farmer/plot's associated ledger? This determines the whole shape.
- **Q2 — Literal location:** do pool units (`Planted - Unassigned`) stay **canonical on main** (with a
  ledger tag) or live **on the funding ledger**? The former keeps PR5's single-tab scan viable; the
  latter requires per-ledger scanning.
- **Q3 — `To Be Paid For`:** §0.3 currently says the liability "**always** sits on main." Does that
  stand, or does it move to the funding ledger too?
- **Q4 — Reimbursement:** when a managed-ledger-funded tree is claimed by a different ledger's QR, is
  the transfer still funding-ledger → main, or direct funding-ledger → QR-ledger?
- **Q5 — Migration:** any existing main-booked purchase rows that should be re-tagged? (Assume none in
  v1, confirm.)
- **Q6 — Sequencing:** PR2b before or after RUN? If RUN (first batch link) fires with purchases
  main-only, its results are still correct under the old model — but re-running after PR2b may differ.
- **Q7 — Per-ledger currency literals (Decision 0.13, §8.5):** confirm the direction — **(a)** make every ledger use one canonical literal at write time, or **(b)** keep the per-ledger spelling and resolve it in code. Option (b) is safer for existing balances (no migration) but means PR5.2/PR4 must carry a ledger→literal map.

### 8.5 Per-ledger liability-currency literal defect (Decision 0.13)

Gary's recollection is **verified true**. Same economic item, different literal by ledger:

| Ledger | Live sale-time tree-liability literal | Evidence |
|---|---|---|
| **main** (+ AGL4, books on main) | `Cacao Tree To Be Planted` *(mixed case)* | main `offchain transactions` Currency col |
| **SEF1** | `CACAO TREE TO BE PLANTED` *(UPPERCASE)* | treasury-cache `managed-ledgers/SEF1.json` summary |
| **PP1** | `CACAO TREE TO BE PLANTED` | `managed-ledgers/PP1.json` |
| **AGL6** | `CACAO TREE TO BE PLANTED` (44 rows) | `managed-ledgers/AGL6.json` |

**The defect:** PR5 (merged) hard-codes `TPL_CUSTOMER_LIABILITY_LITERAL = 'Cacao Tree To Be Planted'` (`process_tree_planting_link.js` L81) and uses it unconditionally. For a QR on a managed ledger the link event therefore writes a **mixed-case** discharge leg that does **not** match the **uppercase** liability the sale-time booker actually raised. Because the ingest auto-creates a `Currencies` row for any unseen literal (PR2 finding), the result is not an error but a **silent spurious second liability** — the real liability stays open and a phantom appears. **Severity: HIGH** (money-path, already merged, silent).

**Fix scope (proposed, PR5.2):** make the literal a **per-ledger resolution** (main/+AGL4 → mixed case; managed → UPPERCASE); audit the sibling literals (`Planted - Unassigned`, `To Be Paid For`) the same way; add a guard test that the literal matches the ledger's actual sale-time spelling. **No code until the §8 redesign is signed off.**
