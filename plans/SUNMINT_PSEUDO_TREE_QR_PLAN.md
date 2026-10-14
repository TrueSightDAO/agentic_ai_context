# SunMint: Pseudo-Tree Slots + QR Assignment — Design & Roadmap (v3)

> **Status:** design / roadmap only — **no code, no schema change, no build units started.**
> **v3 (2026-10-14)** — **Gary's in-place promotion ruling supersedes §2 and §6**: a pseudo tree
> is a `SunMint Tree Planting` row with **blank Latitude/Longitude** + a `plot_id`; *"once it gets
> assigned a lat and long it is no longer a pseudo tree"* — **same row, in place** (no second row,
> no reconcile event, no orphan). **QR codes can be associated with pseudo trees.** v2's
> claim-on-arrival §6 is **replaced**; v1's FIFO matching is gone entirely. See §6.
> **v2 (2026-10-14)** folded in Gary's first simplification: pseudo = blank-K/L row, **no `record_type`
> column**, **no computed geometry** (no spacing grid).
> **Gary (2026-10-14, via Envoy): approved the overall direction / D1–D10 "in spirit."**
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
4. **QR codes CAN be associated with pseudo trees** (Gary, 2026-10-14) — a pseudo slot is a
   first-class link target, valid **before** any real tree exists (SD9).
5. **A pseudo tree becomes REAL in place — the SAME row** (Gary, 2026-10-14): *"pseudo tree is just
   one that has no lat and long but is associated with a plot. Once it gets assigned a lat and long it
   is no longer a pseudo tree."* Promotion writes the real K/L (+ photo + planter) **onto the same
   row** — there is **no second "real tree" row, no `[PSEUDO TREE RECONCILE EVENT]`, and no orphaned
   pseudo row kept as duplicate history.** The signed event that writes K/L **is** the audit trail
   (the ledger is current-state rows + an append-only event log). This **supersedes v2's
   claim-on-arrival §6.**

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
  available ──(QR bound)──▶ assigned ──(real K/L written onto THIS row)──▶ REAL (same row, §6)
      │
      └──(estimate shrinks)──▶ trimmed   (only the never-referenced tail — D8)
```

> **There is no `reconciled` terminal state and no second row.** "Becomes real" is an **in-place
> write** of K/L onto the row — see §6.

**Design intent:** a pseudo tree asserts **nothing** except *"the estimator expects ~N trees here."*
It has no position precisely because its position is unknown.

---

## 2. How a pseudo tree is told apart from a real tree ("a clean way to tell")

**Primary marker (Gary's ruling): blank `Latitude`/`Longitude`.** No new column.

| Aspect | real tree | pseudo tree |
|---|---|---|
| Latitude/Longitude (`K`/`L`) | present | **blank** |
| Photo | present | **absent** |
| id | `Edgar_*` / numeric | **`<plot_id>-pseudo-<N>`** (immutable; **unchanged on promotion**) |
| `plot_id` | derived / set | **set explicitly** |
| tier | `counted`/`farmer-reported`/`sampled` | `spacing-estimate` |
| public label | tree page | **"estimated planting slot, position not yet verified"** (§7) |

**Rule:** the **live** classifier is **blank K/L alone** — a promoted row keeps its id but is *real*
because it now has K/L (§6). The **`-pseudo-` id infix** is only the **allocation namespace + a
provenance marker** (a note that "this row entered as a spacing estimate"), **not** a live state test.
NB: `build_tree_geojson.py`
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
| Status | `available` / `assigned` / `trimmed` — **no `reconciled`**; promotion is in place (§6) |
| Assigned QR Code | FK → `Agroverse QR codes!A` |
| *(no `Reconciled Tree ID` column)* | promotion writes K/L onto **this same row** — the row *is* the real tree (§6) |

*(Written by the `sunmint-ledger-manager` SA — same principal as the `SunMint Plots` tab.)*

**Open question to confirm (D4):** one shared tab (Gary's literal wording) vs a separate
`SunMint Pseudo Trees` tab. Shared is simpler (one id space) but every tree consumer must skip
blank-K/L rows; a separate tab is cleaner isolation but a second registry.

---

## 5. QR → pseudo-slot link (REUSE the link event)

The real path: `[TREE PLANTING LINK EVENT]` → validate → `QR.status := ASSIGNED_TO_TREE` → copy
date/lat/long/photo onto the QR row → governor gate; email; ledger leg.

**Ruling (SD9, Gary 2026-10-14): a QR can be bound to a pseudo slot BEFORE any real tree lands.** The
link does not require — and must not wait for — a real `[TREE PLANTING EVENT]`. That is the whole point:
the QR is printed/handed out now, and a real tree later *claims* the slot (§6). So the pseudo target is
**minted on demand at link time** (D2=(a)) and is a first-class, valid link target with no tree behind it.

**Ruling: reuse/extend that handler** — same atomic pattern, target = a pseudo slot. The pseudo path:
1. resolve signer → governor check (unchanged);
2. validate the QR is linkable (reuse existing preconditions);
3. **bind to a pseudo slot** — allocate the next free `<plot_id>-pseudo-<N>` on the target plot (or
   accept an explicit id), **mint the pseudo row if absent**, mark `assigned`, freeze the id;
4. write the QR row: **plot_id + pseudo slot id + tier** (no lat/long/photo — none exist), set status (→ **D5**);
5. book the **same ledger leg** as the real link (literals per the settlement plan, §5 caveat);
6. optional owner email.

**Difference:** the QR row carries **no position** — the link is a *reservation of a slot*, not an
assertion that a located tree exists.

**Event type:** extend `[TREE PLANTING LINK EVENT]` with a `Link Target` field (pseudo-slot id vs real
tree id) — **not** a new event. The handler branches on whether the target id carries the `-pseudo-`
infix (`pseudo_trees.is_pseudo_id`); keep that branch tight and tested.

**Ledger-literals caveat:** `SUNMINT_TREE_QR_LINKING_PLAN.md §7` was **superseded** by
`plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — book the leg with the settlement plan's
literals.

---

## 6. Real → pseudo promotion = IN PLACE, SAME ROW (Gary's ruling, 2026-10-14)

Gary: *"pseudo tree is just one that has no lat and long but is associated with a plot. Once it gets
assigned a lat and long it is no longer a pseudo tree."*

**A pseudo slot becomes a real tree by writing its Latitude/Longitude (plus photo + planter) onto the
SAME row.** There is:

- **no second "real tree" row** to create and cross-link;
- **no `[PSEUDO TREE RECONCILE EVENT]`**;
- **no orphaned pseudo row** retained as a duplicate copy of history.

**The signed planting event that writes K/L IS the audit trail.** This matches how the rest of the
ledger works — **current-state rows + a full append-only event log** — rather than keeping a dead
duplicate row. Nothing is deleted, so nothing about the pre-promotion state is lost: the row's prior
state (blank K/L, `assigned`) is recoverable from the event log.

Steps when a real planting for a **QR-bound** pseudo slot is recorded:

1. Write **real K/L + photo + planter** onto the **existing pseudo row** (same `Tree ID`).
2. The row now carries a position ⇒ it **is** a real tree. Its blank-K/L discriminator (§2) flips
   by construction — **no relabel needed**, and its **id is unchanged** (§2 / SD2).
3. Copy the planting evidence onto the **QR row** and set the QR status to the real-tree state
   (`ASSIGNED_TO_TREE`) — the QR link itself is unchanged (it already pointed at this row).
4. Emit the **signed planting event** that carries the K/L — that event is the promotion's audit record.

**Id is immutable across promotion.** A promoted row **keeps `<plot_id>-pseudo-<N>`**; the `-pseudo-`
infix is a **provenance marker**, not a live state test — **live pseudo-vs-real is decided by blank
K/L alone** (§2).

### 6.1 Open — a real tree arriving WITHOUT a bound pseudo slot → **D13**

Gary's ruling covers the **QR-bound** path (a pseudo slot exists; a real planting promotes it in
place). The independent case — a `[TREE PLANTING EVENT]` or `cepotx-survey` bulk import that arrives
with its **own K/L and no associated pseudo slot** — is **not** covered. v2's FIFO "claim the next
free slot" is **DROPPED** (it re-introduces exactly the slot-matching machinery Gary's model removes).

- **(a) Stand alone (recommended):** it lands as a normal real tree row; pseudo slots are untouched.
  No matching step; loses nothing.
- **(b) Auto-claim the next free pseudo slot:** the import promotes that slot in place. Re-introduces
  an allocation/match step with no clear owner.

**→ D13 needs a ruling. Recommendation: (a).**

## 7. Honest state — the visible label (Gary's ruling)

Maps directly onto `growth/GROWTH_MODEL.md` (§"How to extend this model" step 4 *"Set status
honestly"* + the anti-patterns). The **QR Trace-Back Loop** (customer scans bag → tree page) is the
surface that must render it. A pseudo-bound bag's page must read, plainly:

> **Plot `RM-P2` — estimated slot #14.** Position not yet verified. This bag is earmarked for one of
> ~N trees expected on this plot (spacing estimate); a specific tree will be linked once a real,
> located submission claims this slot.

**Consequence (→ D10):** a pseudo-assigned bag must **not** increment any public "trees planted"
counter — counting a spacing estimate as planted is the false-precision claim honesty forbids.

**Plot-image fallback (Gary, 2026-10-14 — approved in spirit).** While a bag is pseudo-bound and the
slot has **no real photo**, the provenance page shows the **plot's** image (from the `sunmint`
`plots/media.json` index / geojson `media` prop — 15/22 plots populated) under the precise caption
*"photo shows the plot where this tree is expected, not the individual tree."* Once real K/L + photo
are written (§6), the page switches to the real tree's photo + map. This extends SD5 from the *label*
to the *image*. (The QR page does **not** read the plots registry today — see PR7.)

---

## 8. Decisions — settled vs open

### Settled by Gary's rulings (2026-10-14)

| # | Decision | Ruling |
|---|---|---|
| **SD1** | Distinction marker | **blank Latitude/Longitude** (+ `pseudo-` id prefix). **No `record_type` column** |
| **SD2** | Pseudo id | **`<plot_id>-pseudo-<N>`**, immutable — frozen on reference, **unchanged on promotion**; the `-pseudo-` infix is a provenance namespace, **not** a live state test |
| **SD3** | Geometry | **NONE** — no grid, no computed positions (v1 grid dropped) |
| **SD4** | Link mechanism | **Reuse/extend `[TREE PLANTING LINK EVENT]`** — same atomic pattern |
| **SD5** | Honesty | QR/landing page: **"Plot X — estimated slot #N. Position not yet verified."** |
| **SD6** | Promotion | **In place, same row** — real K/L written onto the pseudo row makes it real; **no second row, no reconcile event, no orphan** (supersedes v2 FIFO-claim) |
| **SD7** | Ambiguity | **N/A** — in-place promotion removes matching entirely; nothing to disambiguate |
| **SD8** | Row shape | same as `SunMint Tree Planting`, blank K/L, no photo, `plot_id` set |
| **SD9** | Link timing | **A QR MAY be bound to a pseudo slot BEFORE any real tree exists** (Gary, 2026-10-14) — the slot is created on demand to receive the binding, not awaited from a submission |
| **SD10** | Promotion | A pseudo row becomes real by gaining K/L **on itself**; the **signed planting event is the audit trail** — **no duplicate row** (Gary, 2026-10-14) |

### Blessed in spirit (Gary, 2026-10-14) — refinements still flagged

| # | Decision | Options | **Recommendation** |
|---|---|---|---|
| **D2** | Mint all N rows up front vs allocate-on-demand | (a) on-demand (b) materialize | **(a)** — scales; pairs with claim-on-arrival |
| **D4** | Where pseudo rows live | (a) shared `SunMint Tree Planting` tab (b) separate tab | **(a)** per Gary's wording — consumers skip blank-K/L rows |
| **D5** | QR status when pseudo-bound | reuse `ASSIGNED_TO_TREE` vs new `ASSIGNED_TO_PSEUDO_TREE` | **new status**, valid with **no tree behind it** (SD9) — so D10's counter guard is a status check, not a column check |
| **D8** | Estimate shrink safety | — | **freeze referenced slots; trim only the never-referenced tail** |
| **D9** | Gating — which `plot_type`s may mint | all vs subset | **`restoration`/`enrichment`/`nursery` only** — never `mature`/`research`/blank |
| **D10** | Public "trees planted" counter | count pseudo-assigned? | **NO** (honest state) |
| **D13** | Real tree arriving with **no** bound pseudo slot (bulk / independent) | (a) stands alone (b) auto-claims a free slot | **(a)** — no matching; see §6.1 |

*(v1's D7/D11/D12 — reconcile trigger, match radius, ambiguity — are **CLOSED**: with in-place promotion there is **no matching step at all**.)*

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
| **PR6** | **In-place promotion** (write K/L onto the pseudo row) + `cepotx-survey` bulk path | `tokenomics`, `dao_protocol` | SD6 |
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
