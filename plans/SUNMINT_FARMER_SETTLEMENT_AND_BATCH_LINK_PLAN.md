# SunMint Farmer Settlement + Batch QR-Tree Linking — Execution Roadmap

**Status:** design ruled (this doc, 2026-09-20 conversation with Gary); no code yet.
**Owner:** Gary Teh · **Drafted by:** Claude Anthropic (Envoy), from a live design conversation.
**Supersedes:** `SUNMINT_TREE_QR_LINKING_PLAN.md` §7 (the old link-time booking:
`-1 Liability` / `+1 "Cacao Tree Planted"` terminal asset). That plan's PR2–PR16 (the DApp,
the QR schema columns, the governor gate, the reject/invalid path) all stay — only the ledger
booking at link time changes, plus everything net-new below.

**Goal:** Give the DAO a complete, symmetric ledger model for the customer→DAO→farmer chain
around SunMint tree planting, and a way to actually execute it at the volume already sitting
unlinked today (**520 sold QRs, 0 linked** — verified live 2026-09-20 via `lineage-assets/qrs_index.json`
`by_status`, and independently via `HANDOFF_MANIFEST.md`'s tracker for the parent plan, which still
reads "first real link pending Gary's go" as of 2026-08-31).

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**
> Report the DAO contribution after each merge (§6).

---

## 0. Decisions (ruled in the 2026-09-20 conversation; a few still open — flagged)

| # | Decision | Choice |
|---|----------|--------|
| 0.1 | **The four-ledger-item model** | Ruled — see §1.3. Two liabilities (customer-side, farmer-side), two assets (unconfirmed-paid, confirmed-unassigned). |
| 0.2 | **Naming (parallel construction)** | `Trees to be planted` (Liability, owed to customer — unchanged) / `Trees purchased, not planted` (Asset, Path A) / `Trees to be paid for` (Liability, Path B, renamed from "trees planted, not yet paid for" for symmetry with 0.2's customer-side name) / `Trees planted, not associated with QR code` (Asset, the pool). **Open:** exact literal-string spelling for the ledger (mirrors the existing `Cacao Tree To Be Planted` convention — not a `Currencies` tab row, just a literal string) — proposed in §1.3, needs a final confirm before PR1 since it's baked into code once shipped. |
| 0.3 | **Link event can draw from EITHER asset-side state, not just the settled pool** | Ruled (Gary, 2026-09-20): "a QR code can be already linked to a tree or a plot before we even paid the farmers because the cooperatives are slow." So `[TREE PLANTING LINK EVENT]` must accept a confirmed-planted tree/plot regardless of whether the farmer has been paid yet. See §1.4 for the mechanics — this is the trickiest revision to the existing handler. |
| 0.4 | **Keep the ledger items, don't go off-ledger** | Ruled (implicitly, across the conversation) — the ledger is the DAO's audited liability/asset system of record (feeds treasury-cache, monthly stats); the QR row is the human-facing/payment-traceability record. Both coexist; this was never really in tension once the model settled — see §1.3's closing note. |
| 0.5 | **Allocation priority for batch linking** | Ruled (Gary): a SOLD QR with a **distinct, not-yet-used** Owner Email gets a **specific photographed tree** (1:1) + a personalized notification email. A QR with a **repeat email or no email** gets a **plot**-level association instead (no manufactured fake specificity). |
| 0.6 | **Expense traceability** | Ruled: every asset/liability unit on the farmer side should carry a reference back to whichever `[TREE PURCHASE EVENT]` / `[FARMER PAYMENT EVENT]` funded it, so a specific QR's fulfillment can always be traced to a real expense record. |
| 0.7 (OPEN) | **Reuse the existing CFR `[PAYOUT EVENT]` sink, or a new dedicated farmer-payment event?** | The CFR `[PAYOUT EVENT]` (tokenomics #504) already exists but writes to a **private** "cfr program" sheet, not a managed ledger's `Transactions` tab, and is currently **inert** (blocked on an OAuth re-consent click — see `HANDOFF_MANIFEST.md`'s CRF row). Proposed default below (§3, PR4): a **new**, ledger-targeted `[FARMER PAYMENT EVENT]` for the general (non-CFR-specific) case, leaving CFR's own PIX-specific sink as-is for its own purposes. Needs Gary's confirm before PR4. |
| 0.8 (OPEN) | **Aging policy for stalled Path A / Path B units** | Not yet chosen between (a) active follow-up/nudge automation or (b) a passive aging report for Gary to act on manually. Proposed default below (§3, PR9): start with (b), the cheaper option — no code to build automation prematurely. Needs Gary's confirm before PR9, can be skipped/deferred without blocking anything else in this plan. |

---

## 1. Pre-flight — captured facts (§5d: no PR below should need to re-discover any of this)

### 1.1 Verified live state, 2026-09-20

- **QR status distribution** (`lineage-assets/qrs_index.json`, generated 2026-08-20): `MINTED: 1125,
  SAMPLE: 90, SOLD: 520, ON CONSIGNMENT: 35, GIFT: 3, EXPENSED: 3`. **No `ASSIGNED_TO_TREE` entries at
  all** — confirms zero real links have ever landed.
- **`HANDOFF_MANIFEST.md`** row for `plans/SUNMINT_TREE_QR_LINKING_PLAN.md`: status "active — reject/
  invalid UAT done (2026-08-31); first real LINK pending Gary go." Telegram topic: thread **11596**
  ("SunMint tree-QR linking").
- **`sold_pending_tree.json`** (same cache generation): `count: 414` sold-pending-tree candidates at
  that time (a subset of the 520 SOLD — those with a non-empty Owner Email and no tree link yet, per
  the PR3 endpoint's own filter).
- A real, already-known unbooked instance of exactly the Path-B gap below: Gary's own note (Telegram,
  CFR thread 30026) — *"we did already do a payout to Paulo priorly for planting 10 trees. We just
  haven't captured it on chain yet."* This is the concrete first case to backfill once PR4 ships.

### 1.2 What already exists and is reused as-is

- **Sale-time booking** (`sales_update_managed_agl_ledgers.js` / the AGL4-special-cased sibling):
  books `+1 "Cacao Tree To Be Planted"` (Liability) on every sale. **Unchanged by this plan.**
- **`[TREE PLANTING EVENT]`** — farmer's raw submission, lands in `SunMint Tree Planting` sheet
  (`1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`, gid `176124122`), `Status=NEW`. Schema: columns
  A–Q per `SUNMINT_TREE_QR_LINKING_PLAN.md` §1.1 (already captured there — Contributor Handle,
  Photo, Lat/Long, Submitted Name, Specie, GitHub Commit URL for the mirrored photo, etc.). **Today
  this books nothing to any ledger** — PR3 below is the first writer that changes that.
- **`[TREE PLANTING LINK EVENT]` / `process_tree_planting_link.gs`** — governor-gated, links one
  `SOLD` QR to one `NEW` SunMint row, writes QR columns D/N/O/P/Q/R (status → `ASSIGNED_TO_TREE`,
  date/lat/long/photo), writes SunMint columns M/R/S (status → `LINKED`, linked QR + timestamp),
  emails the QR's Owner Email, stamps QR column X. **PR5 below revises its ledger-booking step only**
  — the DApp page, governor gate, reject/invalid path, and email step are untouched.
- **`Agroverse QR codes` schema** (full column list already captured in
  `SUNMINT_TREE_QR_LINKING_PLAN.md` §1.2 and `tokenomics/SCHEMA.md` line 869) — columns L (Owner
  Email), N/O/P/R (tree evidence), V (Ledger Name), Z (Stripe Session ID — the existing payment-
  traceability FK), AA (Sold Date), AB (Tree Planted Notification Sent Date).
- **CFR `[PAYOUT EVENT]`** (tokenomics #504, `AKfycbxQDdGnwS7G6iJhNj9japW-9sFA7EUvrnznmJCu44S5ZHqOoIks2be4FXbIVpuaOHVW/exec`)
  — sinks to a private "cfr program" sheet (Tier-1 payouts / Tier-2 payout events tabs), **not** a
  managed ledger. Currently **inert**: the hourly safety-net trigger isn't installed because the
  deploying user hasn't granted `script.scriptapp` (per `GAS_SCRIPT_PROPERTIES.md`). Not modified by
  this plan — see Decision 0.7.
- **Literal-string ledger convention** — `Cacao Tree To Be Planted` is a plain string in the
  `Transactions`/`offchain transactions` `Inventory Type` column, never registered in the `Currencies`
  tab (verified by grep, no writer ever touches `Currencies` for it). Every new item in this plan
  follows the same convention — no `Currencies` tab changes anywhere in this plan.

### 1.3 The four-ledger-item model (ruled this conversation)

| Ledger item | Category | Booked by (this plan) |
|---|---|---|
| `Cacao Tree To Be Planted` | Liability (owed to **customer**) | Unchanged — existing sale-time booking (§1.2) |
| `Cacao Tree Purchased - Not Planted` *(proposed literal string, §0.2)* | Asset (our claim on the **farmer** to deliver) | PR2 — new `[TREE PURCHASE EVENT]` |
| `Cacao Tree - To Be Paid For` *(proposed literal string, §0.2)* | Liability (owed to the **farmer**) | PR3 — extended `[TREE PLANTING EVENT]` ingestion |
| `Cacao Tree Planted - Unassigned` *(proposed literal string, §0.2)* | Asset (fully settled, nobody has a claim) | PR3 (Path A reclass) or PR4 (Path B settlement) |

Two farmer-side entry paths, both converging on the same pool:

- **Path A (DAO pays first):** PR2 books `+1 Cacao Tree Purchased - Not Planted`. When the matching
  `[TREE PLANTING EVENT]` confirmation lands (PR3), reclass `-1 Purchased-Not-Planted` /
  `+1 Planted-Unassigned` — **no cash**, it already moved in PR2.
- **Path B (farmer plants first):** PR3 books `+1 Cacao Tree - To Be Paid For` directly (no prior
  purchase event to consume). When the DAO eventually pays (PR4), `-1 To Be Paid For` /
  `+1 Planted-Unassigned` — **cash leg lands here**.

**Why the ledger stays, not just the QR sheet (Decision 0.4):** the ledger is what treasury-cache /
monthly-statistics / any future balance-sheet report already reads uniformly across every other
Liability/Asset row in this workspace; the QR row (payment ref in column Z, tree evidence in N/O/P/R)
is the human-facing record of a **settled, discharged** pair — the two aren't competing
representations, the ledger is the audit trail and the QR row is the receipt.

### 1.4 The "link before farmer paid" caveat (Decision 0.3) — mechanics

Because a confirmed-planted tree can be linked to a QR **before** its farmer-side liability is
settled, `[TREE PLANTING LINK EVENT]`'s eligible source pool is **both** asset-side-confirmed states,
not just the fully-settled one:

| Source state | Link event effect | What's left open afterward |
|---|---|---|
| `Cacao Tree Planted - Unassigned` (fully settled) | `-1 Cacao Tree To Be Planted` / `-1 Planted-Unassigned` | Nothing — fully closed on both sides. |
| `Cacao Tree - To Be Paid For` (confirmed, farmer unpaid) | `-1 Cacao Tree To Be Planted` **only** | The farmer liability stays open, **now tagged "committed to QR `<qr_code>`."** A later `[FARMER PAYMENT EVENT]` against this specific unit discharges the liability directly — it does **not** re-enter the `Planted-Unassigned` pool, because it's already spoken for. |

This is the one genuinely novel wrinkle: a `Cacao Tree - To Be Paid For` unit needs a **committed /
uncommitted** flag once it can be consumed by a link before payment. PR3 introduces the flag (default
uncommitted); PR5 sets it on link; PR4's payment path checks it to decide whether to re-pool or
discharge-in-place. Concretely, this is a tracking-tab column (mirrors the existing `Tree Planting
Link` tracking tab pattern from the parent plan), not a Sheets formula — the SunMint submission row
itself already gets a `Linked QR Code` column (existing, `SunMint Tree Planting` col R) the moment
either type of link happens, which **is** the commitment signal; PR4 just needs to check that column
before deciding whether to re-pool.

### 1.5 Image association at link time

- **Tree-level link (existing behavior, unchanged):** `process_tree_planting_link.gs` already copies
  the SunMint submission's photo (col I `Photo of Tree Planted`) onto the QR row's column R. Nothing
  to build here.
- **Plot-level link (net-new, PR6):** no single tree photo exists for a plot-level fallback. Reuse the
  same source the plot boundary itself came from — precedent: `AGROVERSE_SUNMINT_FARM_LISTING.md`'s
  Fazenda Clara entry describes plots built from "a 7-pt hull from geotagged media" — i.e. plots
  already have an associated media collection (`farm_media_manifests`). PR6 resolves a **representative
  image** for the target plot (first/cover image from that plot's manifest entry, same convention the
  farm/program media galleries already use) and writes it to the QR row's column R alongside a new
  "Linked Plot ID" column (see PR6).

---

## 2. Authorization envelope (§5e — ask once, not per PR)

| Surface | Envelope |
|---|---|
| `tokenomics` GAS source files (this repo, clasp mirrors under `google_app_scripts/`) | Pre-authorized — feature branch + PR per unit, human reviews before merge. |
| `tokenomics` clasp deploy (pushing a merged GAS change live) | **Always-stop gate (§5c: production deploy).** Ask once per PR that needs it. |
| `dao_client` / `dao_protocol` (Python CLI + dispatch routing) | Pre-authorized — low blast radius, feature branch + PR. |
| `dapp_beta` (plot-picker UI additions to `link_tree_planting.html`) | Pre-authorized for beta. Promotion to `dapp_prod` is a separate, later ask. |
| **Ledger money-movement** (PR2/PR4's real cash-booking steps, and the batch RUN in general) | **Always-stop gate (§5c: TDG/money).** Same posture as the parent plan's own RUN gate. |
| **Backfilling Paulo's known-unbooked payout (§1.1)** | Falls under the ledger money-movement gate above — do this as the **first real use** of PR2/PR4 once built, not before, and not silently bundled into a "docs" PR. |
| **UAT (§5)** | Always-stop gate — validate end-to-end on beta/synthetic data before this touches real farmer or customer records. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Register the three new literal-string ledger items (§1.3) in `tokenomics/SCHEMA.md`'s documentation (a docs-only note next to the existing `Cacao Tree To Be Planted` convention — these are not `Currencies` tab rows, same as today). Confirms Decision 0.2's exact spelling with Gary before any code depends on it. | `tokenomics` (docs only) |
| **PR2** | New handler for `[TREE PURCHASE EVENT]` (Path A entry): fields `Farmer/Cooperative`, `Amount`, `Currency` (BRL/USD), `Tree Count`, `Ledger`, `Proof` (attachment), `Fund Handler`. Books `-cash` (resolved currency) + `+N "Cacao Tree Purchased - Not Planted"` on the resolved managed ledger. Plus `dao_client` CLI module (same shape as `modules/report_ai_agent_contribution.py`) and `dispatch.py` routing. | `tokenomics` + `dao_protocol` |
| **PR3** | Extend `[TREE PLANTING EVENT]` ingestion (`process_tree_planting_telegram_logs.gs` / its cron): on each new `NEW` submission, attempt to match an open, uncommitted `Cacao Tree Purchased - Not Planted` unit for that farmer/ledger (match key: `Manager Name` + `Ledger Name`, FIFO consumption). If found → reclass to `+1 Planted-Unassigned` (no cash). If not found → book `+1 "Cacao Tree - To Be Paid For"` directly (Path B). Add the **uncommitted/committed** tracking column described in §1.4. | `tokenomics` |
| **PR4** | New `[FARMER PAYMENT EVENT]` (Path B settlement — pending Decision 0.7's confirm on reuse-vs-new). Fields mirror PR2. On submit: check whether the target `Cacao Tree - To Be Paid For` unit is already **committed** to a QR (§1.4) — if so, discharge the liability directly (no re-pool); if not, `-1 To Be Paid For` / `+1 Planted-Unassigned`. Cash leg lands here either way. **First real use of this + PR2, once built, is the Paulo backfill (§1.1) — under the money-movement gate (§2).** | `tokenomics` + `dao_protocol` |
| **PR5** | Revise `process_tree_planting_link.gs`'s ledger-booking step per §1.4's table: accept a source from **either** `Planted-Unassigned` or `Cacao Tree - To Be Paid For`; book `-1 Cacao Tree To Be Planted` always, plus `-1` from whichever source state, with the "committed" tag set when sourcing from the not-yet-paid state. **Removes** the old `+1 "Cacao Tree Planted"` terminal-asset line entirely (superseded, §7 of the parent plan). Everything else in the handler (DApp gate, email, reject path) is untouched. | `tokenomics` |
| **PR6** | Plot-level link path: accept a plot id (from `sunmint/plots/index.geojson`) as an alternative to a SunMint submission row. New QR column "Linked Plot ID." Resolves + writes a representative plot image per §1.5 instead of a single tree photo. Same ledger effect as PR5 (a plot-level confirmed-tree unit is just another instance of the same asset/liability states, sourced from an aggregate rather than one submission — needs a plot-level equivalent of the `Planted-Unassigned`/`To Be Paid For` bookkeeping, likely one ledger unit per tree the plot represents, not one unit per plot). | `tokenomics` + `dapp_beta` |
| **PR7** | Expense-traceability reference: new column on `Agroverse QR codes` (or the relevant tracking tab) populated at link time (PR5/PR6) with the `[TREE PURCHASE EVENT]` or `[FARMER PAYMENT EVENT]` id that funded the linked unit (Decision 0.6). | `tokenomics` |
| **PR8** | Batch allocation tool: given all `SOLD`+unlinked QRs and all eligible confirmed units (`Planted-Unassigned` + `To Be Paid For`, per §1.4 — both are linkable), compute the pairing per Decision 0.5 (distinct unused email → individual tree; repeat/no email → plot) and drive PR5/PR6's link event once per pair, governor-confirmed before execution (not silently auto-run against real data). | `dao_client` (CLI/script) |
| **PR9** | Aging report for stalled Path A (`Purchased - Not Planted` sitting unconfirmed) and Path B (`To Be Paid For` sitting unpaid) units — per Decision 0.8's default (passive report, not active nudging). Skippable/deferrable without blocking RUN below. | `dao_client` or `truesight_autopilot` (reporting script) |
| **PR10** | Docs: `tokenomics/SCHEMA.md` new columns + new literal-string items (finalize PR1's draft), `tokenomics/API.md` new events, this plan's resume tracker, `CONTEXT_UPDATES.md` entry. | `tokenomics` / `agentic_ai_context` |
| **RUN** | First real use: (a) backfill Paulo's known payout via PR2+PR4 (§1.1), (b) first real batch-link run via PR8 against real sold QRs and real confirmed trees. **Ledger-money-movement + batch-execution gate (§2) — needs explicit `go`.** | — |
| **UAT** | See §5. **Always-stop gate.** | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (register the three new literal-string ledger items in `SCHEMA.md`,
> confirm exact spelling with Gary). Nothing in this plan has started yet — this is a fresh
> roadmap from a same-day design conversation (2026-09-20).
>
> **Blocking opens before certain units:** PR4 needs Decision 0.7 confirmed (reuse CFR's
> `[PAYOUT EVENT]` sink vs. a new dedicated event) before it can be scoped precisely. PR9 needs
> Decision 0.8 confirmed (active nudge vs. passive report) — but PR9 is not on the critical path
> to RUN, so it can slip without blocking anything else.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (register ledger items in SCHEMA.md) | ☐ | ☐ | ☐ |
| PR2 (`[TREE PURCHASE EVENT]` handler + CLI + routing) | ☐ | ☐ | ☐ |
| PR3 (extend `[TREE PLANTING EVENT]` ingestion — Path A/B split) | ☐ | ☐ | ☐ |
| PR4 (`[FARMER PAYMENT EVENT]` — pending Decision 0.7) | ☐ | ☐ | ☐ |
| PR5 (revise `process_tree_planting_link.gs` booking per §1.4) | ☐ | ☐ | ☐ |
| PR6 (plot-level link path + image resolution) | ☐ | ☐ | ☐ |
| PR7 (expense-traceability reference field) | ☐ | ☐ | ☐ |
| PR8 (batch allocation tool) | ☐ | ☐ | ☐ |
| PR9 (aging report — pending Decision 0.8; non-blocking) | ☐ | ☐ | ☐ |
| PR10 (docs) | ☐ | ☐ | ☐ |
| RUN (Paulo backfill + first real batch link) | ☐ | — | ☐ |
| UAT | ☐ | — | ☐ |

✅ **Pre-flight Completeness (§5d):** every cross-repo fact each PR above needs is captured in §1 —
current QR/link status counts, the existing handler's exact behavior and column layout, the CFR
payout sink's location and blocked state, and the literal-string ledger convention. The one thing
deliberately **not** pre-resolved is Decision 0.7 (reuse vs. new event) and 0.8 (aging policy) —
those are genuine open governor decisions, not undiscovered facts, and are called out explicitly
rather than assumed.

---

## 5. UAT — synthetic data first, then the real Paulo backfill

Follow the parent plan's reusable synthetic-test procedure (`SUNMINT_TREE_QR_LINKING_PLAN.md` §10)
for the mechanics below — same principle: exercise real code paths, never submit a real `[SALES
EVENT]` for a test, use a clearly-test-labeled QR (`TEST_...`), invalidate it afterward.

| Step | Surface | What to expect | Acceptance criterion |
|---|---|---|---|
| 1 | `[TREE PURCHASE EVENT]` against a test farmer/ledger | `+1 Cacao Tree Purchased - Not Planted` booked | Ledger row correct, cash leg correct |
| 2 | Test `[TREE PLANTING EVENT]` for the same farmer/ledger | Matches the open purchase unit → reclass to `+1 Planted-Unassigned`, no new cash | Reclass row correct, no double cash |
| 3 | A second test `[TREE PLANTING EVENT]` with **no** open purchase unit | Books `+1 Cacao Tree - To Be Paid For` directly | Liability row correct |
| 4 | Link a test `SOLD` QR against the **Path B** (unpaid) unit from step 3 | `-1 Cacao Tree To Be Planted` only; the `To Be Paid For` unit gets tagged committed to this QR | QR shows linked; farmer liability still open and now tagged |
| 5 | `[FARMER PAYMENT EVENT]` against that same committed unit | Discharges directly (`-1 To Be Paid For`), does **not** create a new `Planted-Unassigned` row | No phantom pool unit created |
| 6 | Link a test `SOLD` QR against the **Path A** (settled pool) unit from step 2 | `-1 Cacao Tree To Be Planted` / `-1 Planted-Unassigned` | Both sides fully closed |
| 7 | Plot-level link (PR6) against a test QR with a repeat/no-email profile | QR gets a plot id + representative image, not a single tree photo | Correct plot reference + image |
| 8 | Batch tool (PR8) dry-run against real (not test) data | Produces a proposed pairing list without executing | Governor can review before any real link fires |
| 9 | **Real RUN**: Paulo's 10-tree payout backfilled via PR2+PR4 | Ledger shows the real historical expense, tagged/reconciled | Matches Gary's own account of what was actually paid |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first) before starting the next unit.

---

## 7. Open items carried forward from the design conversation (not blocking, worth remembering)

- Exact literal-string spelling for the three new ledger items (Decision 0.2) — PR1 is where this
  gets locked in; changing it after PR2+ ship means a migration, not a rename.
- Whether `Cacao Tree - To Be Paid For`'s "committed to QR X" tag should live on the SunMint tracking
  tab (as proposed, reusing the existing `Linked QR Code` column) or needs its own explicit column —
  proposed default is "reuse the existing column, it already means exactly this," revisit only if PR3
  finds a reason it doesn't.
- PR6's plot-level ledger bookkeeping (one unit per tree the plot represents, vs. one unit per plot)
  is flagged as needing its own small design pass when PR6 starts — not fully resolved here.
