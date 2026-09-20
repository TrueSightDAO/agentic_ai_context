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
  new "Linked Plot ID" column (PR1).

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
| **PR1** | Register the three new literal-string ledger items in `tokenomics/SCHEMA.md` (docs only, confirms exact spelling before code depends on it). Add "Linked Plot ID" column to `Agroverse QR codes` (needed by PR6). Document that the "committed" signal reuses the existing `SunMint Tree Planting` `Linked QR Code`/`Linked At` columns — no new column there. | `tokenomics` (docs + one schema column) |
| **PR2** | `[TREE PURCHASE EVENT]` handler: books `-cash` + `+N Cacao Tree Purchased - Not Planted` on the funding ledger (or main, if generic/undesignated per §0.3). `dao_client` CLI module + `dispatch.py` routing. | `tokenomics` + `dao_protocol` |
| **PR3** | Extend `[TREE PLANTING EVENT]` ingestion: on each new confirmed submission, query the farmer's `Purchased - Not Planted` ledger balance (FIFO by farmer). Match found → `-1 Purchased-Not-Planted / +1 Planted-Unassigned`, **emit the system-signed reconciliation event**. No match → `+1 Cacao Tree - To Be Paid For` on main ledger. | `tokenomics` |
| **PR4** | `[FARMER PAYMENT EVENT]` handler: governor picks a confirmed-unpaid SunMint row for a farmer. Checks `Linked QR Code`: populated → pay from that QR's own ledger, `-1 To Be Paid For` only. Empty → pay from funding/main ledger, `-1 To Be Paid For / +1 Planted-Unassigned`. **First real use, once built, is the Paulo backfill (§1.1) — under the ledger-money gate (§2).** | `tokenomics` + `dao_protocol` |
| **PR5** | Revise `process_tree_planting_link.gs` per §1.3/§1.4: independent `-1 Cacao Tree To Be Planted` write (new code path, sales handler untouched) always fires; source-dependent effect (pool vs. unpaid-liability) as specified; reimbursement transfer fires only in the cross-ledger pool case. Everything else in the handler (DApp gate, email, reject path) untouched. | `tokenomics` |
| **PR6** | Plot-level link path: accept a plot id (from `sunmint/plots/index.geojson`) as an alternative to a SunMint submission row for the batch tool's repeat/no-email case. Writes "Linked Plot ID" + a representative image per §1.6. Needs its own consumption accounting (a plot represents many trees' worth of pool supply, not one) — small design pass at PR6 start. | `tokenomics` + `dapp_beta` |
| **PR7** | Batch allocation tool: given all `SOLD`-unlinked QRs and all eligible confirmed units (`Planted-Unassigned` pool **and** `To Be Paid For` confirmed-unpaid rows, per §0.4), compute the pairing per Decision 0.5 and drive PR5/PR6's link event once per pair — governor-confirmed dry-run before real execution. | `dao_client` (CLI/script) |
| **PR8** | Aging report for stalled `Purchased - Not Planted` balances and `To Be Paid For` liabilities — per Decision 0.8's default (passive report). Non-blocking, can slip. | `dao_client` or `truesight_autopilot` |
| **PR9** | Docs: `tokenomics/SCHEMA.md` finalize, `tokenomics/API.md` new events, this plan's resume tracker, `CONTEXT_UPDATES.md` entry. | `tokenomics` / `agentic_ai_context` |
| **RUN** | (a) Backfill Paulo's known payout via PR2+PR4 (§1.1). (b) First real batch-link run via PR7. **Ledger-money + batch-execution gate (§2) — needs explicit `go`.** | — |
| **UAT** | See §5. **Always-stop gate.** | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (register the three literal-string ledger items, add "Linked Plot ID"). Fresh
> roadmap, reverted same-day to real ledger items after the draft-2 simplification proved to drop
> real accrual information — nothing has started.
>
> **Open before certain units:** PR3 needs Decision 0.7 confirmed (proposed default stated, doesn't
> block starting). PR8 needs Decision 0.8 confirmed — non-blocking, can slip past RUN.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (register ledger items + Linked Plot ID column) | ☐ | ☐ | ☐ |
| PR2 (`[TREE PURCHASE EVENT]` handler + CLI + routing) | ☐ | ☐ | ☐ |
| PR3 (reconciliation match, system-signed) | ☐ | ☐ | ☐ |
| PR4 (`[FARMER PAYMENT EVENT]` handler) | ☐ | ☐ | ☐ |
| PR5 (revise `process_tree_planting_link.gs`) | ☐ | ☐ | ☐ |
| PR6 (plot-level link path + image resolution) | ☐ | ☐ | ☐ |
| PR7 (batch allocation tool) | ☐ | ☐ | ☐ |
| PR8 (aging report — pending Decision 0.8; non-blocking) | ☐ | ☐ | ☐ |
| PR9 (docs) | ☐ | ☐ | ☐ |
| RUN (Paulo backfill + first real batch link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** current QR/link status counts, the existing handler's exact
behavior, the existing sale-time booking's exact behavior (and why it's left alone), the ledger
literal-string convention, and the full four-item model are all captured in §1. Decisions 0.7 and 0.8
are genuine open governor calls, not undiscovered facts, and don't block PR1.

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
