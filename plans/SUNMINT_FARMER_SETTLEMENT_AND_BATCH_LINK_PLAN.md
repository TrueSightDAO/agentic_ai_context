# SunMint Farmer Settlement + Batch QR-Tree Linking — Execution Roadmap

**Status:** design ruled (2026-09-20 conversation with Gary, revised same day after simplifying to a
row-derived model); no code yet.
**Owner:** Gary Teh · **Drafted by:** Claude Anthropic (Envoy), from a live design conversation.
**Supersedes:** `SUNMINT_TREE_QR_LINKING_PLAN.md` §7 (the old link-time booking:
`-1 Liability` / `+1 "Cacao Tree Planted"` terminal asset — **removed entirely**, not replaced with a
different ledger row). That plan's PR2–PR16 (the DApp, the QR schema columns, the governor gate, the
reject/invalid path) all stay untouched — only the ledger-booking step at link time changes.

**Revision note (same-day):** the first draft of this plan introduced three new literal-string ledger
items to track intermediate state (purchased-not-planted, planted-unassigned, to-be-paid-for). Gary
simplified this after walking through it: **the ledger should only ever record real cash events.**
Intermediate state is read directly off columns on the `Agroverse QR codes` and `SunMint Tree
Planting` rows — the same pattern the public "Trees planted" counter on `agroverse_shop`'s landing
page already uses today (it reads QR status directly, never the ledger). This revision is
**significantly smaller in scope** than the first draft: no new `Currencies`-adjacent literal strings,
fewer ledger-writing code paths, and the link event itself becomes mostly a row-write.

**Existing customer-side liability is left alone (Gary, 2026-09-20 — "harmless legacy"):**
`sales_update_managed_agl_ledgers.js` already books `+1 "Cacao Tree To Be Planted"` (Liability) on
every sale, live in production today. This plan does **not** touch that code. It's redundant with the
row-derived customer-liability count below (§1.3), but harmless — it stays correct for as long as
nothing reverses it, and ripping it out of live sales code is a bigger, riskier change than anything
actually needed here. **No PR in this plan modifies `sales_update_managed_agl_ledgers.js`.**

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**
> Report the DAO contribution after each merge (§6).

---

## 0. Decisions (ruled in the 2026-09-20 conversation)

| # | Decision | Choice |
|---|----------|--------|
| 0.1 | **Ledger only records cash events** | Ruled (Gary, 2026-09-20) — the three intermediate farmer-side states from the first draft are **not** ledger rows. Only `[TREE PURCHASE EVENT]`, `[FARMER PAYMENT EVENT]`, and the reimbursement transfer (§1.4) touch a ledger. Everything else is read off `Agroverse QR codes` / `SunMint Tree Planting` columns. |
| 0.2 | **Existing customer liability booking is untouched** | Ruled (Gary, 2026-09-20) — "harmless legacy." No PR here modifies `sales_update_managed_agl_ledgers.js`. |
| 0.3 | **Ledger location rule** | Ruled (Gary, 2026-09-20, confirmed explicitly): a managed ledger that funds its **own** future trees books that spend on **itself**. Main/general treasury fronting a tree **before** any specific managed ledger's customer is known to claim it books on **main ledger**. When a specific managed ledger's QR later claims a main-fronted tree, that managed ledger **reimburses main** via a transfer (§1.4) — this is the *only* case that needs a transfer; if a tree is already linked to a specific ledger's QR **before** it gets paid for, payment is booked directly on that QR's own ledger and no transfer is needed at all (see §1.4). |
| 0.4 | **Link event can draw from a confirmed tree whether or not the farmer has been paid** | Ruled (Gary, 2026-09-20): "cooperatives are slow" — fulfilling the customer isn't gated on paying the farmer. See §1.2. |
| 0.5 | **Allocation priority for batch linking** | Ruled: a SOLD QR with a **distinct, not-yet-used** Owner Email gets a **specific photographed tree** (1:1) + a personalized notification email. A QR with a **repeat email or no email** gets a **plot**-level association instead. |
| 0.6 | **Every row mutation is a signed event** | Ruled (Gary, 2026-09-20) — "every update to the tree record or the QR code record with linking or payment event needs to be a signed event." No raw sheet edits for any of the writes in §1.2/§1.3. Full list in §1.5. |
| 0.7 (OPEN) | **Does the reconciliation match (purchase event ↔ confirmation) need a governor click, or fire automatically and just be system-signed?** | Proposed default: automatic + system-signed (same DAO-identity-signing pattern used elsewhere for AI-driven writes) — requiring a governor click per match would reintroduce the one-at-a-time bottleneck this plan exists to remove. Flagged, not yet confirmed. |
| 0.8 (OPEN) | **Aging policy for stalled unconfirmed prepayments or unpaid confirmed trees** | Not yet chosen between active nudging and a passive report. Proposed default: passive report (§3, PR8) — non-blocking, can slip. |

---

## 1. Pre-flight — captured facts (§5d: no PR below should need to re-discover any of this)

### 1.1 Verified live state, 2026-09-20

- **QR status distribution** (`lineage-assets/qrs_index.json`, generated 2026-08-20): `MINTED: 1125,
  SAMPLE: 90, SOLD: 520, ON CONSIGNMENT: 35, GIFT: 3, EXPENSED: 3`. **No `ASSIGNED_TO_TREE` entries at
  all** — zero real links have ever landed via the formal pipeline.
- **`HANDOFF_MANIFEST.md`** row for `plans/SUNMINT_TREE_QR_LINKING_PLAN.md`: "active — reject/invalid
  UAT done (2026-08-31); first real LINK pending Gary go." Telegram topic: thread **11596**.
- A real, already-known unbooked instance of the farmer-payment gap: Gary's own note (CFR thread
  30026) — *"we did already do a payout to Paulo priorly for planting 10 trees. We just haven't
  captured it on chain yet."* Concrete first case for the RUN step (§3).

### 1.2 The row-derived model

No new ledger items. Four states, all read directly off columns:

| State | Derived from | Where |
|---|---|---|
| DAO owes customer a tree | `Agroverse QR codes`: `status == SOLD` AND tree/plot link columns (N/O/P/R, or the new "Linked Plot ID," §3 PR1) empty | Per the QR's own `Ledger Name` (col V) |
| DAO owes farmer payment | `SunMint Tree Planting`: row confirmed (`Status` past `NEW`) AND `Payment Event Ref` (new col, §3 PR1) empty — **true whether or not that row already has a QR linked** (Decision 0.4) | N/A until paid — no ledger presence at all until the payment event |
| DAO holds an unconfirmed prepayment | An open `[TREE PURCHASE EVENT]` tracking-tab row (§3 PR1/PR2) whose claimed-count is less than its purchased-count | The purchase event's own booking ledger |
| DAO holds a confirmed, unclaimed tree | `SunMint Tree Planting`: confirmed AND `Payment Event Ref` populated AND QR-link column empty | Whichever ledger funded that `Payment Event Ref`'s purchase/payment event |

**The link event is now mostly a row-write, not a ledger-write.** Linking a QR to a confirmed tree
(paid or not) writes the QR's tree-evidence columns and the SunMint row's linked-QR column — nothing
more, in the common case where the tree's funding ledger already matches the QR's own ledger (or
isn't paid yet). The **only** case that also touches a ledger is §1.4's reimbursement transfer.

### 1.3 Why the existing customer liability booking is left alone

`sales_update_managed_agl_ledgers.js`'s existing `+1 "Cacao Tree To Be Planted"` leg (booked on every
sale) is **redundant** with row 1 of the table above — both say the same thing, one via a ledger row,
one via a column check. Per Decision 0.2, this plan does not remove it. It stays correct for as long
as it's never reversed (which it currently isn't, anywhere) — a harmless duplicate, not a conflict.

### 1.4 The reimbursement transfer — when it fires, and when it doesn't

- **Self-funded case:** a managed ledger pays (§ `[TREE PURCHASE EVENT]` or `[FARMER PAYMENT EVENT]`)
  for a tree, and later its **own** ledger's QR claims it. No transfer — money and claim are on the
  same ledger throughout.
- **Already-linked-before-payment case (Decision 0.4's scenario):** a QR is linked to a confirmed,
  unpaid tree first. When the farmer eventually gets paid (`[FARMER PAYMENT EVENT]`), pay **directly
  from the already-linked QR's own ledger** — the payment event already knows which ledger to charge,
  because the link happened first. **No transfer needed here either.**
- **Generic-prepay-claimed-later case (the only case that needs a transfer, Decision 0.3):** main
  ledger fronts a tree generically (no QR linked yet, no specific ledger designated) → later, a
  specific managed ledger's QR claims that confirmed tree → **that managed ledger transfers cash to
  main ledger** to reimburse the front. This transfer is itself a signed, governor-authorized event
  (§1.5) under the same money-movement gate as any other cash event.

### 1.5 Every signed event this plan introduces or touches

| Event | Signer | Ledger effect |
|---|---|---|
| `[TREE PURCHASE EVENT]` (new) | Governor | `-cash` on the funding ledger (or main, if generic/undesignated) — plain expense, no asset leg |
| `[TREE PLANTING EVENT]` (existing, unchanged) | Farmer's own identity | None |
| Reconciliation match (new — purchase ↔ confirmation) | System identity (Decision 0.7's proposed default) | None — writes `Payment Event Ref` + decrements the purchase tracking row's claimed-count |
| `[FARMER PAYMENT EVENT]` (new) | Governor | `-cash` on the funding ledger (or the already-linked QR's ledger, per §1.4) — plain expense, no liability-discharge leg |
| `[TREE PLANTING LINK EVENT]` (existing, revised) | Governor (already the one handler with real server-side enforcement) | None in the common case; fires the reimbursement transfer in the generic-prepay-claimed-later case only |
| Reimbursement transfer | Governor | `-cash` on the claiming ledger, `+cash` on main |

**Hard invariant carried forward into every PR below: no raw sheet edit ever writes to `Payment Event
Ref`, a QR's tree/plot-link columns, or a SunMint row's linked-QR column.** Since none of these states
have a ledger row backing them anymore, the signed event **is** the entire audit trail.

### 1.6 Image association at link time (unchanged from the first draft)

- **Tree-level link:** `process_tree_planting_link.gs` already copies the SunMint submission's photo
  (col I) onto the QR row. Unchanged.
- **Plot-level link (net-new, PR6):** resolve a representative image from the target plot's media
  collection (`farm_media_manifests`, same source plots already use for their boundary hull — see
  `AGROVERSE_SUNMINT_FARM_LISTING.md`'s Fazenda Clara precedent), written to the QR row alongside a
  new "Linked Plot ID" column.

---

## 2. Authorization envelope (§5e — ask once, not per PR)

| Surface | Envelope |
|---|---|
| `tokenomics` GAS source files | Pre-authorized — feature branch + PR per unit, human reviews before merge. |
| `tokenomics` clasp deploy | **Always-stop gate (§5c: production deploy).** Ask once per PR that needs it. |
| `dao_client` / `dao_protocol` | Pre-authorized — low blast radius, feature branch + PR. |
| `dapp_beta` (plot-picker UI additions) | Pre-authorized for beta. Prod promotion is a separate later ask. |
| **Any cash event** (`[TREE PURCHASE EVENT]`, `[FARMER PAYMENT EVENT]`, the reimbursement transfer, and the RUN step in general) | **Always-stop gate (§5c: TDG/money).** |
| **Backfilling Paulo's known-unbooked payout (§1.1)** | Falls under the cash-event gate above — first real use of PR2/PR4, not bundled into a docs PR. |
| **UAT (§5)** | Always-stop gate. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Schema additions, no code: `SunMint Tree Planting` gains **`Payment Event Ref`**; `Agroverse QR codes` gains **`Linked Plot ID`**; a new tracking tab for `[TREE PURCHASE EVENT]`s (Farmer, Ledger, Amount, Currency, Trees Purchased count, Trees Claimed count, Proof, timestamp) so a single purchase can fund and be partially consumed by multiple confirmations over time. Document in `tokenomics/SCHEMA.md`. | `tokenomics` (docs only) |
| **PR2** | `[TREE PURCHASE EVENT]` handler: books `-cash` (funding ledger or main, per §1.4) as a plain expense, appends a row to PR1's tracking tab. `dao_client` CLI module + `dispatch.py` routing. | `tokenomics` + `dao_protocol` |
| **PR3** | Reconciliation on `[TREE PLANTING EVENT]` ingestion: on each new confirmed submission, FIFO-match against an open (claimed < purchased) tracking-tab row for that farmer/ledger. Match found → write `Payment Event Ref`, decrement claimed-count, **emit the system-signed reconciliation event** (§1.5). No match → leave `Payment Event Ref` blank (the row is now the row-derived farmer liability, §1.2). | `tokenomics` |
| **PR4** | `[FARMER PAYMENT EVENT]` handler (Decision 0.7's default: governor picks one or more confirmed-unpaid SunMint rows for a farmer). Checks each row: if already linked to a QR → pay from that QR's own ledger, no transfer. If unlinked → pay from funding/main ledger per §1.4. Writes `Payment Event Ref` on each covered row. **First real use, once built, is the Paulo backfill (§1.1) — under the cash-event gate (§2).** | `tokenomics` + `dao_protocol` |
| **PR5** | Revise `process_tree_planting_link.gs`: **remove** the old `+1 "Cacao Tree Planted"` ledger write entirely. New behavior: match a `SOLD`-unlinked QR to a confirmed SunMint row (paid or unpaid — both eligible, Decision 0.4), write QR tree-evidence columns + SunMint linked-QR column. If the row's `Payment Event Ref` funding ledger differs from the QR's own ledger → fire the reimbursement transfer (§1.4, governor-signed). Otherwise no ledger write at all. Everything else in the handler (DApp gate, email, reject path) untouched. | `tokenomics` |
| **PR6** | Plot-level link path: accept a plot id (from `sunmint/plots/index.geojson`) as an alternative to a SunMint submission row for the batch tool's repeat/no-email case. Writes "Linked Plot ID" + a representative image per §1.6. Needs its own consumption accounting (a plot represents many trees' worth of confirmed-unassigned supply, not one) — small design pass at PR6 start, not resolved here. | `tokenomics` + `dapp_beta` |
| **PR7** | Batch allocation tool: given all `SOLD`-unlinked QRs and all eligible confirmed rows (paid or unpaid, per §1.2/0.4), compute the pairing per Decision 0.5 and drive PR5/PR6's link event once per pair — governor-confirmed dry-run before real execution. | `dao_client` (CLI/script) |
| **PR8** | Aging report for stalled unconfirmed prepayments (PR1's tracking tab, claimed < purchased for a long time) and unpaid confirmed trees (`Payment Event Ref` empty for a long time) — per Decision 0.8's default (passive report). Non-blocking, can slip. | `dao_client` or `truesight_autopilot` |
| **PR9** | Docs: `tokenomics/SCHEMA.md` finalize, `tokenomics/API.md` new events, this plan's resume tracker, `CONTEXT_UPDATES.md` entry. | `tokenomics` / `agentic_ai_context` |
| **RUN** | (a) Backfill Paulo's known payout via PR2+PR4 (§1.1). (b) First real batch-link run via PR7 against real sold QRs and real confirmed trees. **Cash-event + batch-execution gate (§2) — needs explicit `go`.** | — |
| **UAT** | See §5. **Always-stop gate.** | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (schema additions: `Payment Event Ref`, `Linked Plot ID`, the purchase
> tracking tab). Fresh roadmap, revised same-day after the ledger-only-for-cash simplification —
> nothing has started.
>
> **Open before certain units:** PR3 needs Decision 0.7 confirmed (automatic + system-signed vs.
> governor-click reconciliation) — proposed default stated, not yet confirmed, but doesn't block
> starting PR1/PR2. PR8 needs Decision 0.8 confirmed — non-blocking, can slip past RUN.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (schema: Payment Event Ref, Linked Plot ID, purchase tracking tab) | ☐ | ☐ | ☐ |
| PR2 (`[TREE PURCHASE EVENT]` handler + CLI + routing) | ☐ | ☐ | ☐ |
| PR3 (reconciliation match, system-signed) | ☐ | ☐ | ☐ |
| PR4 (`[FARMER PAYMENT EVENT]` handler) | ☐ | ☐ | ☐ |
| PR5 (revise `process_tree_planting_link.gs` — remove old ledger write, add conditional transfer) | ☐ | ☐ | ☐ |
| PR6 (plot-level link path + image resolution) | ☐ | ☐ | ☐ |
| PR7 (batch allocation tool) | ☐ | ☐ | ☐ |
| PR8 (aging report — pending Decision 0.8; non-blocking) | ☐ | ☐ | ☐ |
| PR9 (docs) | ☐ | ☐ | ☐ |
| RUN (Paulo backfill + first real batch link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** current QR/link status counts, the existing handler's exact
behavior, the existing sale-time booking's exact behavior (and why it's left alone), and the full
row-derived model are all captured in §1. Decisions 0.7 and 0.8 are genuine open governor calls, not
undiscovered facts, and don't block PR1.

---

## 5. UAT — synthetic data first, then the real Paulo backfill

Same principle as the parent plan's §10: exercise real code paths, never submit a real `[SALES
EVENT]` for a test, use a clearly-test-labeled QR, invalidate it afterward.

| Step | Surface | What to expect | Acceptance criterion |
|---|---|---|---|
| 1 | `[TREE PURCHASE EVENT]` for a test farmer/ledger, N=5 trees | `-cash` booked, tracking-tab row shows purchased=5, claimed=0 | Correct amounts, no asset leg created |
| 2 | Test `[TREE PLANTING EVENT]` for the same farmer/ledger | Reconciliation matches → `Payment Event Ref` written, tracking row claimed=1 | Match correct, system-signed event emitted |
| 3 | A 6th test confirmation for the same farmer (purchase pool exhausted) | No match → `Payment Event Ref` stays blank | Row correctly shows as an unpaid farmer liability via §1.2's derivation |
| 4 | Link a test `SOLD` QR against the unpaid row from step 3 | QR gets tree evidence; SunMint row gets linked-QR; **no ledger write** | Confirmed via a plain diff of the ledger before/after — nothing changed |
| 5 | `[FARMER PAYMENT EVENT]` against that same now-linked row | Pays directly from the QR's own ledger (not main, no transfer) | Correct ledger, correct amount, `Payment Event Ref` now populated |
| 6 | Link a different test QR (different ledger than the one that funded a generic prepay) against a paid, unlinked confirmed row from a **different** ledger's purchase | Reimbursement transfer fires: claiming ledger `-cash`, funding ledger `+cash` | Both legs correct, governor-signed |
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
