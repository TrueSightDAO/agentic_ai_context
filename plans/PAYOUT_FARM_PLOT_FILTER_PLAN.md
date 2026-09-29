# report_payout_event.html — Farm/Plot filter + cluster backfill

**Filed:** 2026-09-29, by Claude Anthropic (Envoy/planner), from a design discussion with Gary.
**Status:** drafted, not yet triggered.
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

**Open question for Gary before PR2 (batch submit) is scoped precisely:** does a backfilled
cluster payout share **one** `bankRef`/`receiptUrl`/`paidAt` across all selected trees (e.g. a
single PIX transfer covering all 10), or can amounts/dates differ per tree within the batch? The
"paid him money for 10 trees previously" phrasing reads like one lump transfer — PR2 defaults to
that (one shared amount/date/reference applied to every selected tree, amount optionally per-tree
if entered), confirm or correct before that unit starts.

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
| **PR2** | Batch backfill: multi-select checkboxes on the (now filterable) tree list; a single shared `amount`/`paidAt`/`bankRef`/`receiptUrl` form applied across all checked trees (pending §1.3's confirmation — per-tree overrides if Gary wants them instead); fires one `[PAYOUT EVENT]` per selected tree, sequentially, with a running success/failure summary (don't silently swallow a partial-batch failure). | `dapp` (beta) |
| **PR3** | Beta UAT (§5) → prod promote (§2 always-stop gate) → live verification: Gary backfills Paulo's actual 10 Fazenda Bom Sucesso trees for real, confirms they flip from outstanding to paid in the tree registry. | `dapp` (beta → prod) |

---

## 4. Resume tracker

> **RESUME HERE → PR1.** No governor decision blocks PR1 (read-only filter, additive, no behavior
> change to existing single-tree payout flow). **PR2 needs Gary's answer to §1.3's shared-vs-per-tree
> amount question before it's scoped precisely** — flag before starting that unit, don't assume.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (Farm/Plot filter, read-only) | ☐ | ☐ | ☐ |
| PR2 (batch backfill submit) | ☐ | ☐ | ☐ |
| PR3 (prod promote + live Paulo backfill) | ☐ | — | ☐ |

---

## 5. UAT

| Step | Surface | What to expect | Acceptance criterion |
|---|---|---|---|
| 1 | PR1 unit tests | `treePlotMatch` against known coordinates (e.g. a tree inside PL-002's boundary, one clearly outside all 22 plots) | Correct plot_id/farm_id match; graceful empty for the outside case |
| 2 | PR1 beta, live | Pick Fazenda Bom Sucesso → PL-002, with/without a Program also selected | List narrows correctly on both axes independently and combined |
| 3 | PR2 beta, live | Select 3+ trees in a farm cluster, submit one backfill pass | All selected trees receive a `[PAYOUT EVENT]`; a deliberately-induced mid-batch failure (e.g. one bad `recipientPkHash`) reports which trees succeeded vs. failed, not a silent partial success |
| 4 | PR3, prod | Gary's real Paulo/Bom Sucesso backfill (10 trees) | Trees flip from "outstanding" to "paid" in the tree registry; no duplicate payout events created |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first).
