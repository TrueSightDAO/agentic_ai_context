# report_payout_event.html — Farm/Plot filter + cluster backfill

**Filed:** 2026-09-29, by Claude Anthropic (Envoy/planner), from a design discussion with Gary.
**Status:** PR0–PR2 shipped; **PR3's live Paulo backfill VOID** (2026-09-29, Option A — see §4).
**Trigger:** Gary, on `https://beta.dapp.truesight.me/report_payout_event.html`: *"I am thinking to
be able to filter by plot and farm [alongside the existing program filter]... These might end up
being conflicting from a UI/UX perspective since they don't form a clear hierarchy... The reason
why I am concerned about this is because I deal with payout by clusters. For example with Paulo
from Fazenda Bom Sucesso, I paid him money for 10 trees previously... Now I want to back-record
the transactions so that the trees appear already paid for... as opposed to still outstanding."*

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**

---

## 0. The design question, resolved (from discussion, not re-litigated here)

**Program and Farm/Plot do not nest** — confirmed against real data, not just UI intuition. A
program (e.g. CRF Anapu) is a funding/partnership relationship spanning many different family
properties (each student plants on their own land); a single farm can in principle carry trees
under different programs over time. Neither contains the other.

**Farm → Plot does nest cleanly** — a plot belongs to exactly one farm (`sunmint/plots/index.geojson`'s
`farm_id` field; confirmed e.g. Plot `PL-002` → farm `bom-sucesso`, aka Fazenda Bom Sucesso).

**Resolution:** two independent, combinable facets, not one forced hierarchy — the existing
Program dropdown stays exactly as-is; a new Farm→Plot cascading pair sits alongside it (pick a
farm, its plots populate); both narrow the tree list together (AND), matching the real,
non-hierarchical shape of the data rather than inventing a false nesting.

---

## 1. Pre-flight — current-state audit (read live, 2026-09-29, not assumed)

### 1.1 What exists today

`dapp/report_payout_event.html` (dapp_beta) has exactly one filter: **Program**, populated from
`lineage-engine/scripts/sunmint_program_registry.json` and joined to each pending tree via
`submission_source` URL → host → program slug (`payout-event-utils.js` `programSlugsByHost`/
`programHostForTree`). The tree list itself comes from
`lineage-assets/sunmint_pending.json` (`{status, count, items[]}`) — each item has
`telegram_message_id`, `submitted_name`, `planting_date`, `photo_url`, `latitude`, `longitude`,
`species`, `status`. **No `farm_id`/`plot_id`/`submission_source` field exists on these items
today** — confirmed by inspecting the live feed (13 items, none carry it).

### 1.2 The join that makes Farm/Plot filtering possible without new data collection

Every pending tree already carries `latitude`/`longitude`. `sunmint/plots/index.geojson` (22
`Polygon` features, live, fetched 2026-09-29) has exactly the fields needed:
```json
{"plot_id": "RM-P1", "farm_id": "rancho-maranta", "name": "Rancho Maranta Plot 1 (house)",
 "hectares": 0.4, "status": "planted", "owner": "...", "region": "Altamira, Para", ...}
```
`sunmint/farms/index.json` (`{type, generated_at, farms:[{farm_id, name, region, owner,
plot_count, total_hectares, statuses}]}`) is the farm-level SSOT for the Farm dropdown's display
names. **A point-in-polygon test of each pending tree's lat/long against the plots geojson gives
`plot_id` → `farm_id` for free** — the same mechanism already used by hand this session to confirm
tree `Edgar_20260903083523_004` sits on Plot `PL-002` / Fazenda Bom Sucesso. No change to the
submission form, no backfill of historical records required for the *filter* to work — only for
trees whose lat/long actually falls inside a registered polygon (an un-registered/off-plot tree
simply won't match either dropdown, same graceful-empty behavior the Program filter already has
via `programFilterNotApplied`/`renderProgramFilterNote`).

### 1.3 The backfill/batch need — Gary's actual driver

Today the page pays out **one tree at a time** (`FIELDS = ['amount', 'paidAt', 'bankRef',
'programSlug', 'recipientPkHash', 'receiptUrl']`, one tree selected via the picker or a `?tree_id=`
deep link). Gary's Paulo example needs **one bulk action across a cluster**: select Fazenda Bom
Sucesso → Plot PL-002 (or all of Paulo's plots), multi-select the ~10 relevant trees, and record
one backdated payout pass across all of them — closing out `Cacao Tree - To Be Paid For` liability
per Scenario 3 step 3 of `plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` (farmer plants
first, DAO pays later — discharge directly, no re-entry into the unassigned pool). **This plan is
the concrete UI for that discharge**, not a new accounting model — the ledger mechanics were
already designed in that earlier plan; this wires a batch entry point to them.
>
> **⚠️ PREMISE CORRECTION (2026-09-29, thread 35944).** The Scenario-3 framing above is **not what
> happened for Paulo.** Live recon of `offchain transactions` shows the DAO **paid first** (row 2824,
> `-R$40 Brazilian Reis`, 2026-04-09, `[DAO Inventory Expense Event]`) with the trees confirmed
> **later** — the **Path A / prepaid-asset** case, which accrues **no `Cacao Tree - To Be Paid For`
> liability**. The batch-discharge mechanic described here therefore does **not apply** to the Paulo
> cluster (see §4's SUPERSEDED note). The UI remains correct for a genuine Path-B cluster (paid
> *after* planting).

**RESOLVED (Gary, 2026-09-29):** *"I did a one time amount for 10 trees."* — a single lump sum
covered the cluster, so the batch shares **one** `amount`/`paidAt`/`bankRef`/`receiptUrl`; no
per-tree overrides needed. **But source-recon of the payout sink (see §1.4) shows this answer is
not by itself sufficient to build PR2** — the remaining question (batch TOTAL vs PER-TREE) was
**RESOLVED (Gary, 2026-09-29):** *"I did a one time amount for 10 trees"* = the entered figure is the
batch **TOTAL**, so each per-tree event carries **total ÷ N**. Built and merged in PR2 (`dapp_beta` #146).

---

### 1.4 Payout-sink recon (found 2026-09-29 while scoping PR2 — corrects §3's original mechanic)

Read of the live sink `tokenomics/google_app_scripts/1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT/process_payout_event_telegram_logs.js`
(action `processPayoutEventsFromTelegramChatLogs`):

- The Edgar catalog says **one row per TRANSFER** — *"tree_planting_id is carried as a list because a
  single transfer may cover N trees."* **But the booking fn does not loop the list:**
  `fpeBookLedger_` **breaks at the first matching SunMint row** (`if (sun) { treeId = ids[k]; break; }`)
  and `fpeComputeLegs_` hard-codes **`-1`** `Cacao Tree - To Be Paid For` **once per event**.
  ⇒ a single 10-id `[PAYOUT EVENT]` discharges only **ONE** unit of liability, not ten (silent
  under-booking — the cash leg would also be a single lump).
- Therefore the plan's original PR2 mechanic (*"fires one `[PAYOUT EVENT]` per selected tree"*) is
  **correct for the current sink and is kept** — but each per-tree event must carry a **per-tree
  `amount`**, never the batch lump (else cash over-books N×), while `paidAt`/`bankRef`/`receiptUrl`
  are shared across all N events (same PIX) so the rows still reconcile to one statement line.
- No sink change is required for PR2 **as long as it emits N single-tree events.** (If the DAO later
  wants true multi-tree single-event booking, the sink must loop the ids and sum `-N` liability —
  out of scope here; noted for the owner of `tokenomics`.)

---

## 2. Authorization envelope (§5e)

| Surface | Envelope |
|---|---|
| `dapp` (beta) — filter UI, spatial-join util, tests | Pre-authorized — beta repo, feature branch + PR, self-mergeable per standing `*_beta` authority. |
| Promoting to `dapp_prod` (live governor-facing payout tool) | **Always-stop gate (§5c)** — ask once before the prod sync, after beta UAT (§5) passes, not per-PR. |
| PR2's batch-submit mechanics (actually firing multiple `[PAYOUT EVENT]`s) | Needs Gary's answer to §1.3's open question before it's scoped — not blocking PR1. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Farm/Plot filter, read-only (narrows the list, no batch action yet): fetch `sunmint/plots/index.geojson` + `sunmint/farms/index.json`; add a `treePlotMatch(tree, plotsGeojson)` point-in-polygon helper to `payout-event-utils.js` (mirrors the existing `programSlugsByHost`/`treesForProgram` pattern — pure functions, unit-testable, same file); add Farm and Plot `<select>` elements beside the existing Program `<select>` in `report_payout_event.html`, Plot options cascading from the chosen Farm; both combine with Program via AND, matching §0. Graceful-empty note (mirroring `renderProgramFilterNote`) when a tree's coordinates don't fall in any registered plot. Tests in `dapp/tests/payout-event-utils.test.js` (unit) + `tests/report_payout_event.spec.ts` (Playwright, matching existing conventions). | `dapp` (beta) |
| **PR2** | Batch backfill: multi-select checkboxes on the (now filterable) tree list; ONE batch `amount`/`paidAt`/`bankRef`/`receiptUrl` form for the cluster (Gary 2026-09-29: a single lump sum covered Paulo's 10 trees). **Fires one `[PAYOUT EVENT]` PER SELECTED TREE — NOT one multi-tree event** (§1.4: the sink discharges exactly −1 `To Be Paid For` per event, so an N-id event under-books the liability), sequentially, with a running success/failure summary (never silently swallow a partial-batch failure). Shared `paidAt`/`bankRef`/`receiptUrl`; **per-event `amount` = batch total ÷ N** (the one remaining confirmation: TOTAL vs PER-TREE, §1.3). | `dapp` (beta) |
| **PR3** | Beta UAT (§5) → prod promote (§2 always-stop gate) → live verification: Gary backfills Paulo's actual 10 Fazenda Bom Sucesso trees for real, confirms they flip from outstanding to paid in the tree registry. **⚠️ Live-backfill half SUPERSEDED 2026-09-29 (Option A, thread 35944): the Paulo cluster is prepaid (Path A), not a Scenario-3 discharge — DO NOT fire. The batch feature itself stays valid for future Path-B clusters.** | `dapp` (beta → prod) |

---

## 4. Resume tracker

> **⚠️ PR3 — AWAITING GOVERNOR (human money gate; do NOT auto-execute).** Prod promote ☑ **DONE** 2026-09-29 (Gary's explicit *"promote to prod"* → `dapp_prod` synced; see the UPDATE block below). The **only** remaining PR3 step is Gary firing the **live Paulo / Fazenda Bom Sucesso backfill** — a money action Sophia must never take. This marker is therefore a **waiting-on-governor gate, not an executable unit.** PR2 is **built ☑ /
> merged ☑ / reported ☑** (dapp_beta #146, sha 3b38bf1): batch backfill UI + `splitBatchAmount`, firing
> **one single-tree `[PAYOUT EVENT]` per selected tree** each carrying **total ÷ N** (§1.4 sink recon).
> §1.3 is RESOLVED (Gary 2026-09-29: *"one time amount for 10 trees"* = batch TOTAL ÷ N). **PR3 cannot
> start without Gary's explicit go** (§2/§5c): promote `dapp_beta` → `dapp_prod` after beta UAT passes,
> then Gary backfills Paulo's real 10 Fazenda Bom Sucesso trees for real and confirms they flip
> outstanding → paid. **Never promote to prod or fire payouts without the governor's go.**
>
> **UPDATE (2026-09-29): PROD PROMOTE DONE** — Gary said *"promote to prod"*; `dapp_beta` →
> `dapp_prod` synced (fork merge, non-forced; deploy ledger `deploy_20260929T041546Z_dapp-prod`).
> New farm/plot filter + URL-sync code verified present in `dapp_prod` main. **Only remaining PR3
> step: Gary fires the live Paulo backfill and confirms the 10 Fazenda Bom Sucesso trees flip
> outstanding → paid** — Sophia does not move money, so this step stays with the governor.
>
> **⚠️ SUPERSEDED (2026-09-29, thread 35944) — DO NOT fire the Paulo backfill.** Gary ruled
> **Option A** for the Paulo / Fazenda Bom Sucesso cluster: the batch is **NOT** fired. Recon found
> the DAO **paid first** (`offchain transactions` row 2824, `-R$40 Brazilian Reis`, 2026-04-09,
> `[DAO Inventory Expense Event]` with the PDF receipt) and the trees were confirmed **later** — i.e.
> **Path A (prepaid asset), not Path B / Scenario 3** — so there is **no `Cacao Tree - To Be Paid For`
> liability for this farmer to discharge**; the live `To Be Paid For` balance (+2) belongs to Gary, not
> Paulo. Firing the 10 payouts would have **double-booked the cash** (R$40 already expensed at row
> 2824) and written a phantom `-10` liability on top. The correct handling is a **reclassification** of
> the bespoke `Cacao tree seedling (per seedling, …)` +10 asset onto canonical footing — tracked in the
> **reclassification work** (see §1.3 PREMISE CORRECTION and thread 35944), **not here**. **PR3's
> "live Paulo backfill" step is therefore void.** The **batch-submit feature itself (PR2) remains
> valid** for any future cluster that is genuinely Path B (farmer paid *after* planting) and does not
> collide with an existing expense event.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (Farm/Plot filter, read-only) | ☑ | ☑ | ☑ |
| PR2 (batch backfill submit) | ☑ | ☑ | ☑ |
| PR3 (prod promote + live Paulo backfill) | ☑ prod promote | ☑ dapp_prod synced 2026-09-29 | ☒ live Paulo backfill VOID — superseded 2026-09-29 (Option A: reclassify, don't fire) |

---

### 4.1 Ad-hoc additions (not in the original PR0–PR3 scope)

| Item | What shipped | Where | Merged |
|---|---|---|---|
| URL filter sync | Farm/Plot/Program filters now also mirror into the URL (`?farm=&plot=&program=`): changing a facet updates the URL (via `history.replaceState`, non-default facets only so a pristine link stays clean); opening a shared link restores the filtered view, composing with the existing `?tx=`/`?tree_id=` deep links. Requested by Gary 2026-09-29: *"when I update farm, plot, program the URL should also update"*. | `dapp_beta` #147 (sha d149729) | ☑ |

---

## 5. UAT

| Step | Surface | What to expect | Acceptance criterion |
|---|---|---|---|
| 1 | PR1 unit tests | `treePlotMatch` against known coordinates (e.g. a tree inside PL-002's boundary, one clearly outside all 22 plots) | Correct plot_id/farm_id match; graceful empty for the outside case |
| 2 | PR1 beta, live | Pick Fazenda Bom Sucesso → PL-002, with/without a Program also selected | List narrows correctly on both axes independently and combined |
| 3 | PR2 beta, live | Select 3+ trees in a farm cluster, submit one backfill pass | All selected trees receive a `[PAYOUT EVENT]`; a deliberately-induced mid-batch failure (e.g. one bad `recipientPkHash`) reports which trees succeeded vs. failed, not a silent partial success |
| 4 | ~~PR3, prod~~ **SUPERSEDED 2026-09-29** | Paulo/Bom Sucesso is prepaid (Path A) — DO NOT fire (Option A, thread 35944) | n/a for this cluster; use a future **Path-B** cluster to UAT the batch feature |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first).
