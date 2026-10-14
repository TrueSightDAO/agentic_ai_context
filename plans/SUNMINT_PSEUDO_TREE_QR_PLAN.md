# SunMint: Pseudo-Tree Generation + QR Slot Assignment — Design & Roadmap

> **Status:** design / roadmap only — **no code, no schema change, no build units started.**
> Governor decisions **D1–D10** in §8 must be ruled before any build unit (§9) begins.
> **Owner:** Gary Teh. **Drafted by:** Sophia Truesight, 2026-10-14, at Gary's request (via Envoy).
> **Relation to prior plans:** this **answers open decision D3** of
> `SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` with a third option; it **extends** (does not replace)
> `SUNMINT_TREE_QR_LINKING_PLAN.md`'s real-tree link mechanism.

---

## 0. Why this doc exists

Gary's ask (2026-10-14, via Envoy):

> *individual, QR-codable **pseudo trees** generated from the plot's density estimate (not just a
> summary count), so a QR can be assigned to a specific tree-like slot **now**, with a clean way to
> tell a pseudo tree apart from a real submitted one, and a later mechanism to link a real tree (once
> CEPOTX data lands) to its pseudo placeholder.*

This is **finer-grained than D3**. D3 (2026-09-08) leaned toward binding NEW cacao-bag QRs to the
**plot** specifically because per-tree photography doesn't scale (phone overheated mid-run; 103
photos → ~88 unique trees for a 0.67 ha pocket). Gary's ask today is **per-pseudo-tree**, not
per-plot and not per-real-tree. So this is a **live extension / answer to D3**, not something to build
silently inside the U3 estimate work.

### Grounding (read before proposing anything — done)

| Source | What it fixes for this design |
|---|---|
| `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` | D3; tiered labels (`spacing-estimate` \| `farmer-reported` \| `sampled` \| `counted`); the 1,100/ha planted-extent rule; **gating** (mature/research never auto-estimated) |
| `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` | The **real** mechanism: `[TREE PLANTING LINK EVENT]` flips a QR to `ASSIGNED_TO_TREE` and copies lat/long/photo/species onto the QR row. Pseudo trees need an **analogous but distinct** path. |
| `tokenomics/SCHEMA.md` | `Agroverse QR codes` col **AC `Linked Plot ID`** (plot-fallback link, plan PR6) already exists; `ASSIGNED_TO_TREE` already in the status enum |
| `SUNMINT_PLOTS_REGISTRY.md` | plot schema, boundary tiers, `plot_type` vocabulary, single-column rule |
| **U3 (live)** | `plots/index.geojson` now carries `expected_trees` + `expected_trees_source`, **governor-editable via the `SunMint Plots` sheet** |

---

## 1. Concept

A **pseudo tree** is a **non-photographed placeholder slot** inside a plot polygon, minted from the
plot's `expected_trees` estimate. It is a *stand-in* for a real tree that has not (yet) been
submitted with evidence.

A **real tree** is an actual `[TREE PLANTING EVENT]` submission — it carries a photo, a planter
signature (`pk_hash`), and (usually) GPS.

Lifecycle of a pseudo tree:

```
  available ──(QR bound)──▶ assigned ──(real tree linked)──▶ reconciled
      │
      └──(estimate shrinks)──▶ retired          (only if never referenced — see D8)
```

**Design intent (credentialing-lineage principle):** a pseudo tree asserts **nothing** about the
physical world except *"the estimator expects roughly N trees here."* It must always be visibly
labelled as an estimate, never confused with a counted/evidenced tree.

---

## 2. How a pseudo tree is told apart from a real tree ("a clean way to tell")

Use **three orthogonal markers**, so no single field has to be inferable by parsing:

| Aspect | **Real** tree | **Pseudo** tree |
|---|---|---|
| `tree_id` | `Edgar_20260821175134_006` or a numeric Telegram id (from `pick_tree_id`) | **`PS-<plot_id>-<seq>`** e.g. `PS-RM-P2-0007` — a reserved `PS-` prefix never emitted by `pick_tree_id` |
| `tree_kind` (**new property**) | `real` (or absent ⇒ real, for backward compat) | `pseudo` |
| evidence | `photo_url` + `pk_hash` (planter) + GPS | **none** — no photo, no planter, no separate GPS; inherits only the *plot's* boundary evidence |
| tier | `counted` / `farmer-reported` / `sampled` | **`spacing-estimate`** (inherits `expected_trees_source`) |
| QR status when bound | `ASSIGNED_TO_TREE` | **`ASSIGNED_TO_PSEUDO_TREE`** (proposed — D5) |
| geometry | real point | synthetic grid point (D3) or none |

**Rule:** an agent/consumer can always branch on `tree_kind` alone; the `PS-` prefix is a second,
human-visible guard. A pseudo tree must **never** be silently promoted to a real tree — reconciliation
(§5) creates a *link*, it does not relabel the pseudo row.

---

## 3. Where pseudo trees live and how they are generated

**Source of truth for the count:** the plot's `expected_trees` (U3), which already carries
`expected_trees_source` ∈ {`sheet`, `estimate`} and is gated (blank for mature/research). The **tier**
for pseudo trees is derived: `spacing-estimate` (estimate) or `farmer-reported` (if a governor set a
sheet override that came from a farmer count).

**Two build strategies (→ D2):**

- **(a) Allocate-on-demand (recommended).** A pseudo-tree id is minted **only when a QR is actually
  bound** to a slot; the plot's `expected_trees` is the **ceiling**. The persisted registry
  (`SunMint Pseudo Trees` tab, §4) holds **only issued slots** and their state. Scales: a plot with
  `expected_trees = 5556` mints nothing until a QR asks for slot #1.
- **(b) Eager materialization.** Materialize all N slots immediately. Simple to reason about, but
  mints thousands of empty rows per plot — rejected at scale unless capped.

**Why this matters:** a QR binding needs a **durable, stable target**. Under (a), the allocator hands
out the next free `seq` and *persists* it (the slot is real the moment it is issued); under (b) the
whole set is pre-declared. Both keep a *bound* slot frozen forever.

**Display (optional, → D3):** to show tree-like slots on the impact map, generate deterministic
**synthetic grid** points inside the polygon (seeded by `plot_id` so they're stable between builds),
flagged `geometry_source: "synthetic_grid"`. These are **viz only** — they are not, by themselves,
issued slots.

---

## 4. Storage & schema

### 4a. Pseudo-tree registry (new tab, → D4)

Proposed: a new tab **`SunMint Pseudo Trees`** in the SunMint ledger (`1qbZZhf-…`), one row per
**issued** pseudo tree:

| Col | Header | Notes |
|---|---|---|
| A | Pseudo Tree ID | `PS-<plot_id>-<seq>` |
| B | Plot ID | FK → `SunMint Plots!A` |
| C | Seq | integer slot index within the plot |
| D | Tier | `spacing-estimate` / `farmer-reported` / `sampled` |
| E | Estimated At | when the slot was minted |
| F | Status | `available` / `assigned` / `reconciled` / `retired` |
| G | Assigned QR Code | FK → `Agroverse QR codes!A` (once bound) |
| H | Assigned At | |
| I | Reconciled Tree ID | FK → `SunMint Tree Planting` (once a real tree lands) |
| J | Reconciled At | |
| K | Notes | |

*(Written by the `sunmint-ledger-manager` SA — same principal as the `SunMint Plots` tab.)*

### 4b. Index emission (→ D4)

Two options: emit pseudo trees into the **existing** `trees/index.geojson` with `tree_kind`, or a
**separate** `trees/pseudo_index.geojson`. Recommendation: **one index + `tree_kind`** (the map and
consumers filter), because a single join key space keeps the reconciliation and the QR linkage simple.

---

## 5. QR binding to a pseudo tree (analogous to, but distinct from, the real path)

The real path (`SUNMINT_TREE_QR_LINKING_PLAN.md`) is:

```
[TREE PLANTING LINK EVENT]  →  validate QR.status=SOLD & row.status=NEW
                            →  QR.status := ASSIGNED_TO_TREE
                            →  copy planting date/lat/long/photo onto the QR row
                            →  governor gate; email owner; book ledger fulfillment
```

Pseudo binding mirrors this shape but with three differences:

1. **Target** is a `PS-` slot, not a `SunMint Tree Planting` row (§1.1).
2. **Status** flips to `ASSIGNED_TO_PSEUDO_TREE` (proposed — D5), keeping the two paths
   distinguishable in the ledger **without** inspecting columns.
3. **No planting evidence to copy** (there is none) — instead the QR row gets the **pseudo tree id +
   plot id + tier**, so the owner sees *"your bag is earmarked for 1 of ~N expected trees on plot
   RM-P2 (spacing estimate)"* — honest, not a false precision claim.

**Event (→ D6):** a new **`[PSEUDO TREE ASSIGN EVENT]`** (recommended, separate event type — same
rationale as §0.1 of the linking plan: it touches the QR row + the pseudo tab + (optionally) sends
email, so folding it into the generic `[QR CODE UPDATE EVENT]` overloads a handler other flows keep
simple). New CLI module mirrors `modules/link_tree_planting.py`.

---

## 6. Real → pseudo reconciliation (once CEPOTX data lands)

When a **real** `[TREE PLANTING EVENT]` arrives that spatially belongs to a plot with assigned pseudo
slots, reconcile:

1. Match the real tree to an **assigned** pseudo slot on the same plot (§7 → D7 for auto vs manual).
2. Write `SunMint Pseudo Trees` cols I/J (`Reconciled Tree ID`, `Reconciled At`) and set
   `Status := reconciled`.
3. **Transfer the QR binding** to the real tree: `QR.status := ASSIGNED_TO_TREE`, copy the real
   planting evidence onto the QR row (i.e. hand off to the existing real-link mechanics), clear
   `Linked Plot ID`/pseudo fields as appropriate.
4. Emit **`[PSEUDO TREE RECONCILE EVENT]`** (→ D6) so the transfer is an auditable signed record.

**Invariant:** the pseudo row is **never deleted** (audit history) and **never relabelled** a real
tree; reconciliation is a *link*, not a rename.

**Priority rule:** slot assignment prefers real trees over pseudo (a real tree landing in a plot should
claim the QR before a fresh pseudo slot does, if both are possible).

---

## 7. Interaction with the editable estimate (U3) — the safety case (→ D8)

Because `expected_trees` is **governor-editable** (U3), the slot set can move under existing bindings.
Policy:

- **A `seq` that has ever been issued (status ≠ `available`) is FROZEN forever** — never renumbered,
  never deleted, even if `expected_trees` shrinks below its index.
- **Growth:** append new `available` seqs up to the new ceiling.
- **Shrink:** only trim **never-issued** tail slots. If the ceiling drops below the highest issued
  `seq`, keep the issued slots and simply stop minting new ones (the plot is *over-subscribed* relative
  to the estimate → flag for a transect sample, per the estimation plan's cross-check rule).

This keeps every QR binding valid across estimate edits — the same "referenced rows are immutable"
discipline the tree registry already uses for audit.

---

## 8. Open decisions (D1–D10) — all NEED a governor ruling

| # | Decision | Options | **Recommendation** |
|---|---|---|---|
| **D1** | Pseudo-tree ID scheme | `PS-<plot>-<seq>` vs opaque uuid | **`PS-<plot_id>-<seq>`** — human-readable, sorts by plot, provably non-colliding with `Edgar_*`/numeric real ids |
| **D2** | Materialize vs allocate | (a) on-demand (b) eager | **(a) allocate-on-demand** — scales; `expected_trees` is the ceiling, only issued slots persist |
| **D3** | Synthetic geometry | none vs seeded grid | **seeded grid `geometry_source:"synthetic_grid"`** for map viz, flagged synthetic (stability via `plot_id` seed) |
| **D4** | Storage | separate index vs `tree_kind` in `trees/index.geojson` | **one index + `tree_kind`** (single join key space) |
| **D5** | QR status when pseudo-bound | reuse `ASSIGNED_TO_TREE`+col vs new `ASSIGNED_TO_PSEUDO_TREE` | **new `ASSIGNED_TO_PSEUDO_TREE`** — distinguishable in the ledger without column inspection |
| **D6** | Event types | extend `[TREE PLANTING LINK EVENT]` vs new events | **new `[PSEUDO TREE ASSIGN EVENT]` + `[PSEUDO TREE RECONCILE EVENT]`** |
| **D7** | Reconciliation trigger | auto spatial-join vs manual per tree | **auto-join + governor review list** (mirrors the linking plan's D4) |
| **D8** | Estimate shrink/grow safety | see §7 | **freeze issued seqs; trim only never-issued tail** |
| **D9** | Gating | which `plot_type`s may mint pseudo trees | **`restoration` / `enrichment` / `nursery` only** — never `mature` / `research` / blank (run the estimator first) |
| **D10** | Public "trees planted" counter | does a pseudo-assigned bag count? | **NO** — `ASSIGNED_TO_PSEUDO_TREE` must **not** be added to `agroverse_shop`'s `SOLD \| ASSIGNED_TO_TREE` filter (that counts *real* trees). Counting a spacing estimate as "planted" would be a false precision claim. |

---

## 9. Mapped work units (sequenced; **none started**)

| Unit | Scope | Repo | Gate |
|---|---|---|---|
| **PR0** | **this doc** | `agentic_ai_context` | review |
| **PR1** | D1–D10 ruled; this doc updated with the rulings | `agentic_ai_context` | **governor** |
| **PR2** | `build_plots_geojson.py`: emit `pseudo_slots` count (no ids) + gating; optional seeded synthetic grid — **no allocation yet** | `sunmint` | D3/D9 |
| **PR3** | `SunMint Pseudo Trees` tab schema + allocator (`sunmint-ledger-manager` write) | `sunmint` | D2/D4 |
| **PR4** | `[PSEUDO TREE ASSIGN EVENT]` handler + `dao_client` module + governor gate | `tokenomics`, `dao_protocol` | D5/D6 |
| **PR5** | DApp surface (`dapp_beta/assign_pseudo_tree.html`) + permissions action | `dapp_beta`, `treasury-cache` | D6 |
| **PR6** | Reconciliation: `[PSEUDO TREE RECONCILE EVENT]` + auto-join + review list | `tokenomics`, `dao_protocol` | D7 |
| **PR7** | Render pseudo slots / assigned state on `sunmint.html` + `/sunmint/plots/` | `truesight_me_beta` | — |
| **PR8** | Live UAT on beta → promotion (always-stop gate) | — | **governor** |

Per `OPERATING_INSTRUCTIONS.md` §5a: **one PR per execution turn, then stop.** Report the DAO
contribution after each merge (§6).

---

## 10. Related

- `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` — D3, tier labels, the 1,100/ha rule, gating
- `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` — the **real** link mechanism this mirrors
- `plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — ledger literals, `Linked Plot ID` col AC
- `SUNMINT_PLOTS_REGISTRY.md` — plot schema, `plot_type` vocabulary, single-column rule
- `SUNMINT_E2E_RUNBOOK.md` — rebuild + beta/prod render flow
- `tokenomics/SCHEMA.md` — `Agroverse QR codes`, `SunMint Tree Planting`, `SunMint Plots` schemas
- U3 (live) — `expected_trees` + `expected_trees_source`, governor-editable via the sheet
