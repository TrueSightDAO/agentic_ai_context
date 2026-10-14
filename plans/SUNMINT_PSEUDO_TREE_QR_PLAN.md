# SunMint: Pseudo-Tree Slots + QR Assignment — Design & Roadmap (v2)

> **Status:** design / roadmap only — **no code, no schema change, no build units started.**
> **v2 (2026-10-14)** folds in **Gary's simplification ruling**: a pseudo tree is a
> `SunMint Tree Planting`-shaped row with **blank Latitude/Longitude** and **no photo**, `plot_id` set,
> **stable id**. This **replaces v1's `record_type` column** and **removes all computed geometry**
> (no spacing grid). Reconciliation becomes **claim-on-arrival (FIFO within a plot)**, replacing v1's
> spatial nearest-match. The cleared open decisions are in §8.
> **Owner:** Gary Teh. **Drafted by:** Sophia Truesight, 2026-10-14, at Gary's request (via Envoy).
> **Companion:** `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` **§8 Addendum** answers **D3** with
> this design.
> **Relation to prior plans:** answers open decision **D3** of the estimation plan with a third option;
> **extends** (does not replace) `SUNMINT_TREE_QR_LINKING_PLAN.md`'s real-tree link mechanism.

---

## 0. Why this doc exists

Gary's ask (2026-10-14): *individual, QR-codable **pseudo trees** from the plot's density estimate
(not just a summary count), so a QR can be assigned to a specific tree-like slot **now**, with a clean
way to tell a pseudo tree apart from a real submitted one, and a later mechanism to link a real tree
(once CEPOTX data lands) to its pseudo placeholder.*

Finer-grained than D3 (which leaned plot-level because per-tree photography doesn't scale). v2
**answers it with almost no new machinery**, per Gary's second ruling:

### 0.1 Gary's ruling (2026-10-14) — AUTHORITATIVE

1. **Tell them apart — a pseudo tree has NO Latitude/Longitude** (blank `SunMint Tree Planting!K/L`)
   and **no photo**. A real GPS-tagged submission always has them. **Blank K/L *is* "not yet
   individually verified"** — and it is *more* honest than a fabricated map point, because we only
   know the plot holds ~N estimated trees, not where each one is. **No new column is needed.**
   Discriminator: the id prefix **`<plot_id>-pseudo-<N>`** (a real id is `Edgar_*`/numeric).
2. **Generate pseudo trees — as placeholder rows only.** No spacing grid, no computed positions.
   Just N placeholder slots per eligible plot (N bounded by `expected_trees`), each a
   `SunMint Tree Planting`-shaped row with blank K/L, `plot_id` set, stable id.
3. **Link QR → pseudo slot — reuse/extend `[TREE PLANTING LINK EVENT]`** (same atomic pattern:
   QR row + a row + ledger leg), pointed at a pseudo slot instead of a real row.
4. **Reconcile later (real tree lands) — CLAIM-ON-ARRIVAL (FIFO).** A real tree landing in plot X
   **claims any unclaimed pseudo slot in that plot** (first-available). They are interchangeable
   placeholders, so there is **no spatial matching, no match radius, and no ambiguous-collision
   handling** — v1's D7/D11/D12 collapse away.

### 0.2 Grounding (read — done)

| Source | What it fixes |
|---|---|
| `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` | D3; tiers (`spacing-estimate`/`farmer-reported`/`sampled`/`counted`); the ×1,100 (~3 m) rule → now only supplies the **count** `expected_trees`, not positions; gating. Its **§8 Addendum** = this design |
| `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` | The **real** mechanism: `[TREE PLANTING LINK EVENT]` → `ASSIGNED_TO_TREE`, copies lat/long/photo onto the QR row. Pseudo slots reuse this shape (§5) |
| `growth/GROWTH_MODEL.md` | **Honest-state principle** — §"How to extend this model" step **4** + anti-patterns; QR Trace-Back Loop (customer → tree page) |
| `tokenomics/SCHEMA.md` | `Agroverse QR codes` col **AC `Linked Plot ID`**; `ASSIGNED_TO_TREE` in the status enum; `SunMint Tree Planting` cols incl. K/L Latitude/Longitude |
| `SUNMINT_PLOTS_REGISTRY.md` | plot schema, `plot_type` vocabulary, single-column rule |
| **U3 (live)** | `plots/index.geojson` carries `expected_trees` + `expected_trees_source`, governor-editable via the `SunMint Plots` tab col **T `Expected Trees`** |

---

## 1. Concept

A **pseudo tree** is a **placeholder slot** for a tree the estimator expects but which has **not been
photographed or located** — a `SunMint Tree Planting`-shaped row with **blank K/L** and **no photo**.

A **real tree** is an actual `[TREE PLANTING EVENT]` submission — photo + planter `pk_hash` + GPS.

Lifecycle:

```
  available ──(QR bound)──▶ assigned ──(real tree arrives in same plot)──▶ reconciled ──▶ retired
      │
      └──(estimate shrinks)──▶ trimmed   (only the never-referenced tail — D8)
```

**Design intent:** a pseudo tree asserts **nothing** except *"the estimator expects ~N trees here."*
It has no position precisely because its position is unknown.

---

## 2. How a pseudo tree is told apart from a real tree ("a clean way to tell")

**Primary marker (Gary's ruling): blank `Latitude`/`Longitude`.** No new column.

| Aspect | real tree | pseudo tree |
|---|---|---|
| Latitude/Longitude (`K`/`L`) | present | **blank** |
| Photo | present | **absent** |
| id | `Edgar_*` / numeric | **`<plot_id>-pseudo-<N>`** |
| `plot_id` | derived / set | **set explicitly** |
| tier | `counted`/`farmer-reported`/`sampled` | `spacing-estimate` |
| public label | tree page | **"estimated planting slot, position not yet verified"** (§7) |

**Rule:** a consumer branches on **blank K/L + the `pseudo-` id prefix.** NB: `build_tree_geojson.py`
does **NOT** drop blank-coordinate rows today — it emits them with `geometry: null` (verified
2026-10-14). So pseudo slots stay off the *map* only because their geometry is null; the builder must
be taught to **skip blank-K/L rows from the tree index** (or tag them) in PR2, so placeholders never
appear as map features. Consistent with "no fabricated point."

*(v1's `record_type` column is **dropped**. If a future `cepotx-survey` bulk import ever needs
distinguishing from real submissions, it can carry a source label then — not now.)*

---

## 3. What a pseudo slot is (no geometry)

**Count source:** the plot's `expected_trees` (U3) — tier `spacing-estimate` (or `farmer-reported` if
a governor set a sheet count from a farmer). Gated (blank for mature/research).

**No positions.** v1's "3 m spacing grid scoped to the polygon" is **DROPPED** — with no lat/long we
compute nothing. A pseudo slot is just an id: `<plot_id>-pseudo-<N>`, `N ∈ 1..expected_trees`.

**Durability:** once a slot is **referenced** (QR bound) its id is **frozen forever** (never
renumbered), so a printed/handed-out QR keeps pointing at the same slot even if the estimate changes.

**Mint policy (→ D2):**
- **(a) Allocate-on-demand (recommended).** Mint `<plot_id>-pseudo-1` the first time a QR binds to
  the plot; `expected_trees` is the ceiling. A plot with 5,556 expected trees mints nothing until
  asked. Pairs naturally with claim-on-arrival.
- **(b) Materialize all N rows up front.** Complete but mints thousands of empty rows per plot.

---

## 4. Storage & schema

**Shape (Gary): "same shape as a real `SunMint Tree Planting` row but with blank K/L (and no photo),
`plot_id` set, stable id."** → the pseudo rows live in the **`SunMint Tree Planting`** sheet
(same tab), distinguished by blank K/L + the `pseudo-` id prefix (→ **D4**).

| Field | Value for a pseudo slot |
|---|---|
| Tree ID | `<plot_id>-pseudo-<N>` |
| Plot ID | FK → `SunMint Plots!A` (**set**) |
| Latitude / Longitude | **blank** |
| Photo | **blank** |
| Tier | `spacing-estimate` / `farmer-reported` |
| Status | `available` / `assigned` / `reconciled` / `trimmed` |
| Assigned QR Code | FK → `Agroverse QR codes!A` |
| Reconciled Tree ID | FK → the real tree, once it claims this slot |

*(Written by the `sunmint-ledger-manager` SA — same principal as the `SunMint Plots` tab.)*

**Open question to confirm (D4):** one shared tab (Gary's literal wording) vs a separate
`SunMint Pseudo Trees` tab. Shared is simpler (one id space) but every tree consumer must skip
blank-K/L rows; a separate tab is cleaner isolation but a second registry.

---

## 5. QR → pseudo-slot link (REUSE the link event)

The real path: `[TREE PLANTING LINK EVENT]` → validate → `QR.status := ASSIGNED_TO_TREE` → copy
date/lat/long/photo onto the QR row → governor gate; email; ledger leg.

**Ruling: reuse/extend that handler** — same atomic pattern, target = a pseudo slot. The pseudo path:
1. resolve signer → governor check (unchanged);
2. validate the QR is linkable (reuse existing preconditions);
3. **bind to a pseudo slot** — allocate the next free `<plot_id>-pseudo-<N>` on the target plot (or
   accept an explicit id), mark `assigned`, freeze the id;
4. write the QR row: **plot_id + pseudo slot id + tier** (no lat/long/photo — none exist), set status (→ **D5**);
5. book the **same ledger leg** as the real link (literals per the settlement plan, §5 caveat);
6. optional owner email.

**Difference:** the QR row carries **no position** — the link is a *reservation of a slot*, not an
assertion that a located tree exists.

**Event type:** extend `[TREE PLANTING LINK EVENT]` with a `Link Target`/`Record Type` field — **not**
a new event. Keep the `record_type` branch tight and tested.

**Ledger-literals caveat:** `SUNMINT_TREE_QR_LINKING_PLAN.md §7` was **superseded** by
`plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — book the leg with the settlement plan's
literals.

---

## 6. Real → pseudo reconciliation = CLAIM-ON-ARRIVAL (Gary's ruling)

When a **real** `[TREE PLANTING EVENT]` (or a bulk `cepotx-survey` import) lands in plot X:

1. **Claim the next unclaimed pseudo slot in that plot** — FIFO (`<plot_id>-pseudo-<lowest free N>`).
   No distance test, no radius, no ambiguity — slots are interchangeable placeholders.
2. Write the real tree's **real K/L + photo + planter** onto the **real tree row** (the pseudo row
   stays blank-K/L).
3. **Re-point the QR's link to the real tree id**: QR → `ASSIGNED_TO_TREE`, copy the real planting
   evidence onto the QR row (hand off to existing real-link mechanics).
4. **Retire, never delete:** the pseudo row → `Status := reconciled`, kept forever for audit; the
   surviving link's identity is the real tree.
5. Emit the auditable signed reconcile record.

**No-candidate case:** if a real tree lands in a plot with **no** unclaimed pseudo slot (all claimed,
or none minted), it simply stands as its own `actual-submission` row — nothing to reconcile.

**Priority rule:** a real tree claims a slot **before** a fresh QR is assigned a new pseudo slot.

**Invariant:** pseudo rows are **never deleted** and **never given a position**; reconciliation is a
*slot claim* + a QR re-point, plus `reconciled` on the pseudo row.

**Bulk `cepotx-survey`:** lands as real-shaped rows with K/L → claim slots by the same FIFO, at import
time.

---

## 7. Honest state — the visible label (Gary's ruling)

Maps directly onto `growth/GROWTH_MODEL.md` (§"How to extend this model" step 4 *"Set status
honestly"* + the anti-patterns). The **QR Trace-Back Loop** (customer scans bag → tree page) is the
surface that must render it. A pseudo-bound bag's page must read, plainly:

> **Plot `RM-P2` — estimated slot #14.** Position not yet verified. This bag is earmarked for one of
> ~N trees expected on this plot (spacing estimate); a specific tree will be linked once a real,
> located submission claims this slot.

**Consequence (→ D10):** a pseudo-assigned bag must **not** increment any public "trees planted"
counter — counting a spacing estimate as planted is the false-precision claim honesty forbids.

---

## 8. Decisions — settled vs open

### Settled by Gary's rulings (2026-10-14)

| # | Decision | Ruling |
|---|---|---|
| **SD1** | Distinction marker | **blank Latitude/Longitude** (+ `pseudo-` id prefix). **No `record_type` column** |
| **SD2** | Pseudo id | **`<plot_id>-pseudo-<N>`**, stable; referenced ids frozen |
| **SD3** | Geometry | **NONE** — no grid, no computed positions (v1 grid dropped) |
| **SD4** | Link mechanism | **Reuse/extend `[TREE PLANTING LINK EVENT]`** — same atomic pattern |
| **SD5** | Honesty | QR/landing page: **"Plot X — estimated slot #N. Position not yet verified."** |
| **SD6** | Reconcile | **Claim-on-arrival (FIFO within plot)** → re-point QR to real tree; retire pseudo row |
| **SD7** | Ambiguity | **N/A** — interchangeable slots; nothing to disambiguate |
| **SD8** | Row shape | same as `SunMint Tree Planting`, blank K/L, no photo, `plot_id` set |

### Still open — NEED a ruling

| # | Decision | Options | **Recommendation** |
|---|---|---|---|
| **D2** | Mint all N rows up front vs allocate-on-demand | (a) on-demand (b) materialize | **(a)** — scales; pairs with claim-on-arrival |
| **D4** | Where pseudo rows live | (a) shared `SunMint Tree Planting` tab (b) separate tab | **(a)** per Gary's wording — consumers skip blank-K/L rows |
| **D5** | QR status when pseudo-bound | reuse `ASSIGNED_TO_TREE` vs new `ASSIGNED_TO_PSEUDO_TREE` | **new status** — so D10's counter guard is a status check, not a column check |
| **D8** | Estimate shrink safety | — | **freeze referenced slots; trim only the never-referenced tail** |
| **D9** | Gating — which `plot_type`s may mint | all vs subset | **`restoration`/`enrichment`/`nursery` only** — never `mature`/`research`/blank |
| **D10** | Public "trees planted" counter | count pseudo-assigned? | **NO** (honest state) |

*(v1's D7/D11/D12 — reconcile trigger, match radius, ambiguity — are **CLOSED** by claim-on-arrival.)*

---

## 9. Mapped work units (sequenced; **none started**)

| Unit | Scope | Repo | Gate |
|---|---|---|---|
| **PR0** | this doc (v2) + the estimation-plan §8 addendum | `agentic_ai_context` | review |
| **PR1** | D2/D4/D5/D8/D9/D10 ruled; docs updated | `agentic_ai_context` | **governor** |
| **PR2** | pseudo-slot **allocator** (`<plot_id>-pseudo-<N>` next-free + freeze-on-reference) + make `build_tree_geojson.py` skip blank-K/L rows / carry `plot_id` — **no QR coupling** | `sunmint` | SD1/SD3 |
| **PR3** | mint pseudo rows (blank K/L, no photo, plot_id) into the target tab via `sunmint-ledger-manager` SA | `sunmint` | D2/D4 |
| **PR4** | **Extend `[TREE PLANTING LINK EVENT]`** to accept a pseudo target + `dao_client` field; book leg per settlement literals | `tokenomics`, `dao_protocol` | D5 |
| **PR5** | DApp surface for binding a QR to a pseudo slot + permissions action | `dapp_beta`, `treasury-cache` | D5 |
| **PR6** | **Claim-on-arrival** reconciliation (FIFO claim + QR re-point) + `cepotx-survey` bulk path | `tokenomics`, `dao_protocol` | SD6 |
| **PR7** | Render pseudo slots + assigned state + the **honest-state label** on the tree page, `sunmint.html`, `/sunmint/plots/` | `truesight_me_beta` | SD5 |
| **PR8** | Live UAT on beta → promotion (always-stop) | — | **governor** |

Per `OPERATING_INSTRUCTIONS.md` §5a: **one PR per execution turn, then stop.**

---

## 10. Related

- `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` — D3; **§8 Addendum** answers D3 with this design
- `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` — the **real** link mechanism this reuses
- `plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — ledger literals (supersedes linking-plan §7)
- `growth/GROWTH_MODEL.md` — honest-state principle; QR Trace-Back Loop
- `SUNMINT_PLOTS_REGISTRY.md` — plot schema, `plot_type` vocabulary
- `tokenomics/SCHEMA.md` — `Agroverse QR codes`, `SunMint Tree Planting`, `SunMint Plots`
- U3 (live) — `expected_trees` + `expected_trees_source`, governor-editable (`SunMint Plots` col T)
