# SunMint: Pseudo-Tree Slots + QR Assignment — Design & Roadmap (v4)

> **Status:** design / roadmap only — **no code, no schema change, no build units started.**
> **v4 (2026-10-14) — PR1: all open D-decisions ruled by Gary.** D1 (id `PS-<plot_id>-<seq>`),
> D2 (allocate-on-demand), D4 (**one** registry), D5 (`ASSIGNED_TO_PSEUDO_TREE`), D6 (new
> **`[PSEUDO TREE ASSIGN EVENT]`**; promotion reuses the existing link/submission; `[PSEUDO TREE
> RECONCILE EVENT]` **dropped**), D7/D8 (no separate row to reconcile; an unbound submission fills the
> first/any open slot — §6.1), D9/D10 (unchanged). See §8.
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
   Namespace: the id prefix **`PS-<plot_id>-<seq>`** (a real id is `Edgar_*`/numeric) — the
   **live** discriminator is **blank K/L alone** (§2).
2. **Generate pseudo trees — as placeholder rows only.** No spacing grid, no computed positions.
   Just N placeholder slots per eligible plot (N bounded by `expected_trees`), each a
   `SunMint Tree Planting`-shaped row with blank K/L, `plot_id` set, stable id.
3. **Link QR → pseudo slot — NEW `[PSEUDO TREE ASSIGN EVENT]`** (Gary, 2026-10-14): no real
   mechanism binds a QR to a slot-without-a-tree today, so this is its **own** event (QR row + a row +
   ledger leg). **Promotion reuses the existing `[TREE PLANTING LINK EVENT]`/submission mechanism**
   (§6); there is **no** `[PSEUDO TREE RECONCILE EVENT]`.
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
| id | `Edgar_*` / numeric | **`PS-<plot_id>-<seq>`** (immutable; **unchanged on promotion**) |
| `plot_id` | derived / set | **set explicitly** |
| tier | `counted`/`farmer-reported`/`sampled` | `spacing-estimate` |
| public label | tree page | **"estimated planting slot, position not yet verified"** (§7) |

**Rule:** the **live** classifier is **blank K/L alone** — a promoted row keeps its id but is *real*
because it now has K/L (§6). The **`PS-` prefix** is only the **allocation namespace + a
provenance marker** (a note that "this row entered as a spacing estimate"), **not** a live state test.
**D1 (Gary: id scheme not load-bearing):** we keep **`PS-<plot_id>-<seq>`** — legible at a glance and
self-deduplicating within a plot — but a plain tree-id would be equally valid, since the row **is** a
normal tree row.
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
compute nothing. A pseudo slot is just an id: `PS-<plot_id>-<seq>`, `seq ∈ 1..expected_trees`.

**Durability:** once a slot is **referenced** (QR bound) its id is **frozen forever** (never
renumbered), so a printed/handed-out QR keeps pointing at the same slot even if the estimate changes.

**Mint policy (→ D2):**
- **(a) Allocate-on-demand (recommended).** Mint `PS-<plot_id>-1` the first time a QR binds to
  the plot; `expected_trees` is the ceiling. A plot with 5,556 expected trees mints nothing until
  asked. Pairs naturally with in-place promotion (§6).
- **(b) Materialize all N rows up front.** Complete but mints thousands of empty rows per plot.

---

## 4. Storage & schema

**Shape (Gary): "same shape as a real `SunMint Tree Planting` row but with blank K/L (and no photo),
`plot_id` set, stable id."** → the pseudo rows live in the **`SunMint Tree Planting`** sheet
(same tab), distinguished by blank K/L (→ **D4, settled**).

| Field | Value for a pseudo slot |
|---|---|
| Tree ID | `PS-<plot_id>-<seq>` |
| Plot ID | FK → `SunMint Plots!A` (**set**) |
| Latitude / Longitude | **blank** |
| Photo | **blank** |
| Tier | `spacing-estimate` / `farmer-reported` |
| Status | `available` / `assigned` / `trimmed` — **no `reconciled`**; promotion is in place (§6) |
| Assigned QR Code | FK → `Agroverse QR codes!A` |
| *(no `Reconciled Tree ID` column)* | promotion writes K/L onto **this same row** — the row *is* the real tree (§6) |

*(Written by the `sunmint-ledger-manager` SA — same principal as the `SunMint Plots` tab.)*

**D4 — SETTLED (Gary, 2026-10-14): ONE registry, not two.** A pseudo tree is simply a
`SunMint Tree Planting` row with blank K/L and `plot_id` set. **No separate `SunMint Pseudo Trees`
tab.** Tree consumers skip **blank-K/L** rows (the live discriminator, §2).

---

## 5. QR → pseudo-slot binding — NEW `[PSEUDO TREE ASSIGN EVENT]` (D6, Gary 2026-10-14)

The **real** path: `[TREE PLANTING LINK EVENT]` → validate → `QR.status := ASSIGNED_TO_TREE` → copy
date/lat/long/photo onto the QR row → governor gate; email; ledger leg.

**Binding a QR to a pseudo slot is a DIFFERENT act** — it reserves a slot with **no tree behind it** —
so it gets its **own event: `[PSEUDO TREE ASSIGN EVENT]`** (D6). No existing mechanism does this today,
so there is nothing to reuse; the handler follows the same *atomic pattern* (QR row + a row + ledger
leg + governor gate) but is a **distinct event type**.

**Ruling (SD9): a QR MAY be bound to a pseudo slot BEFORE any real tree exists.** The slot is **minted
on demand at assign time** (D2=(a)) and is a first-class, valid link target with **no tree behind it**.
The QR is printed/handed out now; a real tree later **promotes that same slot in place** (§6).

Steps:
1. resolve signer → governor check (same as the link handler);
2. validate the QR is linkable (reuse existing preconditions);
3. **bind to a pseudo slot** — allocate the next free `PS-<plot_id>-<seq>` on the target plot (or
   accept an explicit id), **mint the pseudo row if absent**, mark `assigned`, freeze the id;
4. write the QR row: **plot_id + slot id + tier** (no lat/long/photo — none exist), set status
   **`ASSIGNED_TO_PSEUDO_TREE`** (D5);
5. book the ledger leg (literals per the settlement plan — caveat below);
6. optional owner email.

**Difference from the real link:** the QR row carries **no position** — the assign is a *reservation
of a slot*, not an assertion that a located tree exists.

**Promotion is NOT a new event.** When the real submission lands it writes real K/L (+ photo) onto the
**SAME row** via the **existing `[TREE PLANTING LINK EVENT]`/submission mechanism** (§6). There is
**no `[PSEUDO TREE RECONCILE EVENT]`** (D6 — dropped).

**Ledger-literals caveat:** `SUNMINT_TREE_QR_LINKING_PLAN.md §7` was **superseded** by
`plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — book the leg with the settlement plan's
literals.

### 5.1 QR owner experience — what the provenance page shows (Gary, 2026-10-14)

When the owner scans a **pseudo-bound** bag, the provenance page (`qr/index.html`) renders the
**plot's** evidence — because the individual tree is, honestly, not yet located:

| QR state | Provenance page renders |
|---|---|
| **`ASSIGNED_TO_PSEUDO_TREE`** | The **plot's `media` photo** (from `plots/index.geojson` `media` prop — the *same field* `SUNMINT_PLOTS_REGISTRY.md` defines and the `/sunmint/plots/` gallery already renders) + the honest copy **"Earmarked for 1 of ~N expected trees on Plot `RM-P2` (spacing estimate). Position not yet verified."** — **no map pin** (there is no position). |
| **`ASSIGNED_TO_TREE`** (after promotion, §6) | Falls back to the **real tree's own photo** + planting evidence (+ map pin, lat/long now known). |

- **Field pinned:** the plot image comes from the `media` array on the plot record (component 1 of
  `SUNMINT_PLOTS_REGISTRY.md` §Media; example `"media": ["images/RM-P1/img_7624.jpg"]`), served from
  `sunmint/images/<plot_id>/`. **No new field.**
- **The switch is automatic:** the page must **runtime-resolve** the linked row (it already fetches
  `trees/index.geojson` and joins on `qr_code`) — when that row acquires K/L + photo it **is** real,
  so the same page renders the real photo with **no re-link**. (Do **not** cache the pseudo image in
  the manifest — the manifest re-seed drops hand-added fields; read the registry at runtime.)
- **Honesty extends to the image** (SD5): the plot photo is real evidence of the *plot*, **not** of
  *this tree* — the caption must say so. This is still **more** grounding than today's bare asset page.
- **Implementation:** PR7 (below). The page **does not read the plots registry today**, so PR7 adds
  that join.

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

**Id is immutable across promotion.** A promoted row **keeps `PS-<plot_id>-<seq>`**; the `PS-`
prefix is a **provenance marker**, not a live state test — **live pseudo-vs-real is decided by blank
K/L alone** (§2).

### 6.1 A real submission with no bound slot → fills the first/any open slot (D7/D8, Gary)

Gary: *"when a real submission's lat/long lands inside a plot that has multiple open (unassigned) pseudo
slots, which slot does it fill? (Probably doesn't matter since they're interchangeable pre-fill —
first/any open slot in that plot.)"*

- **QR-bound path:** the real submission fills **the slot its QR is bound to** (the assigned one) —
  unambiguous, in place.
- **No bound slot** (bulk `cepotx-survey`, or a farmer submission with no QR): it fills the **first/any
  open (unassigned) slot in its plot** — lowest free `seq`; slots are interchangeable, so the choice
  carries no meaning. **No spatial matching, no radius.**
- **No open slot** (all assigned, or none minted): it **stands alone** as a normal real tree row.

**D13 is thereby resolved** (Gary's D7/D8 answer): an unbound real submission fills the first/any open
slot — not "stands alone" as previously recommended.

**D7/D8 are otherwise moot:** there is no separate row to reconcile and no slot to "freeze" for safety
— the row *is* the tree, promoted in place. The only survivor is the **allocator's stability rule**:
an allocated id is **never renumbered** (referenced ids are frozen), so a printed QR keeps resolving;
an **estimate shrink trims only the never-referenced tail** (D8).

## 7. Honest state — the visible label (Gary's ruling)

Maps directly onto `growth/GROWTH_MODEL.md` (§"How to extend this model" step 4 *"Set status
honestly"* + the anti-patterns). The **QR Trace-Back Loop** (customer scans bag → tree page) is the
surface that must render it. A pseudo-bound bag's page must read, plainly:

> **Plot `RM-P2` — estimated slot #14.** Position not yet verified. This bag is earmarked for one of
> ~N trees expected on this plot (spacing estimate); a specific tree will be linked once a real,
> located submission claims this slot.

**Consequence (→ D10):** a pseudo-assigned bag must **not** increment any public "trees planted"
counter — counting a spacing estimate as planted is the false-precision claim honesty forbids.

**Plot-image fallback (Gary, 2026-10-14 — ruled).** While a bag is pseudo-bound and the slot has
**no real photo**, the provenance page shows the **plot's** `media` image under the precise caption
*"photo shows the plot where this tree is expected, not the individual tree."* Once real K/L + photo
are written (§6) and the QR flips to `ASSIGNED_TO_TREE`, the page falls back to the **real tree's own
photo** + map. Full render matrix in **§5.1**. This extends SD5 from the *label* to the *image*.

---

## 8. Decisions — settled vs open

### Settled by Gary's rulings (2026-10-14)

| # | Decision | Ruling |
|---|---|---|
| **SD1** | Distinction marker | **blank Latitude/Longitude** (+ `PS-` prefix). **No `record_type` column** |
| **SD2** | Pseudo id | **`PS-<plot_id>-<seq>`**, immutable — frozen on reference, **unchanged on promotion**; the `PS-` prefix is a provenance namespace, **not** a live state test |
| **SD3** | Geometry | **NONE** — no grid, no computed positions (v1 grid dropped) |
| **SD4** | Assign mechanism | **NEW `[PSEUDO TREE ASSIGN EVENT]`** (D6) — same atomic pattern as the real link, distinct event type |
| **SD5** | Honesty | QR/landing page: **"Plot X — estimated slot #N. Position not yet verified."** + **plot `media` image** (not the tree's), caption *"plot, not the individual tree"* (§5.1) |
| **SD6** | Promotion | **In place, same row** — real K/L written onto the pseudo row makes it real; **no second row, no reconcile event, no orphan** (supersedes v2 FIFO-claim) |
| **SD7** | Ambiguity | **N/A** — in-place promotion removes matching entirely; nothing to disambiguate |
| **SD8** | Row shape | same as `SunMint Tree Planting`, blank K/L, no photo, `plot_id` set |
| **SD9** | Link timing | **A QR MAY be bound to a pseudo slot BEFORE any real tree exists** (Gary, 2026-10-14) — the slot is created on demand to receive the binding, not awaited from a submission |
| **SD10** | Promotion | A pseudo row becomes real by gaining K/L **on itself**; the **signed planting event is the audit trail** — **no duplicate row** (Gary, 2026-10-14) |
| **SD11** | Row id (D1) | **`PS-<plot_id>-<seq>`** — kept for legibility + per-plot dedup; **not load-bearing** (a plain tree-id would do, since the row **is** a normal tree row) |
| **SD12** | Registry (D4) | **ONE registry** — a pseudo tree is just a `SunMint Tree Planting` row with blank K/L; **no separate tab** |
| **SD13** | QR status (D5) | **new `ASSIGNED_TO_PSEUDO_TREE`** — keeps the ledger legible without inspecting lat/long |
| **SD14** | Events (D6) | **New `[PSEUDO TREE ASSIGN EVENT]`** for QR→slot binding; promotion = existing link/submission; **no `[PSEUDO TREE RECONCILE EVENT]`** |
| **SD15** | Unbound submission (D7/D8) | Fills the **first/any open slot in the plot** (lowest free `seq`); none open → stands alone. **No spatial matching** |

### Settled in PR1 (Gary, 2026-10-14)
| # | Decision | Ruling |
|---|---|---|
| **D1** | Row id scheme | **`PS-<plot_id>-<seq>`** — legibility + per-plot dedup; **not load-bearing** (SD11) |
| **D2** | Mint up front vs on demand | **allocate-on-demand** (pairs with in-place promotion) |
| **D4** | Where pseudo rows live | **ONE registry** — `SunMint Tree Planting`, blank K/L (SD12) |
| **D5** | QR status when pseudo-bound | **new `ASSIGNED_TO_PSEUDO_TREE`** (SD13) |
| **D6** | Events | **new `[PSEUDO TREE ASSIGN EVENT]`**; promotion = existing link/submission; **no reconcile event** (SD14) |
| **D7/D8** | Reconciliation / freeze safety | **moot** — no separate row; unbound submission fills first/any open slot (SD15); allocator id never renumbered; trim only never-referenced tail |
| **D9** | Gating — which `plot_type`s may mint | **`restoration`/`enrichment`/`nursery` only** — never `mature`/`research`/blank |
| **D10** | Public "trees planted" counter | **NO** — pseudo-assigned QRs never count (honest state) |
| **D13** | Real tree with no bound slot | **fills the first/any open slot** — supersedes the earlier "stands alone" recommendation (SD15) |

*(v1's D7/D11/D12 — reconcile trigger, match radius, ambiguity — **CLOSED**: with in-place promotion there is **no matching step at all**.)*

---

## 9. Mapped work units (sequenced; **none started**)

| Unit | Scope | Repo | Gate |
|---|---|---|---|
| **PR0** | this doc (v2→v4) + the estimation-plan §8 addendum | `agentic_ai_context` | review |
| **PR1** | **this revision**: D1/D2/D4/D5/D6/D7/D8/D9/D10/D13 ruled; docs updated (v4) | `agentic_ai_context` | **governor** |
| **PR2** | pseudo-slot **allocator** (`PS-<plot_id>-<seq>` next-free + freeze-on-reference) + make `build_tree_geojson.py` skip blank-K/L rows / carry `plot_id` — **no QR coupling**. **NB:** the allocator already merged (`sunmint` #6) but uses `PSEUDO_INFIX = "-pseudo-"` + a FIFO docstring — **must be renamed to the `PS-` prefix (D1) and de-FIFO'd** to match this v4 plan | `sunmint` | SD1/SD11 |
| **PR3** | mint pseudo rows (blank K/L, no photo, plot_id) into the target tab via `sunmint-ledger-manager` SA | `sunmint` | D2/D4 |
| **PR4** | **NEW `[PSEUDO TREE ASSIGN EVENT]`** + `dao_client` field; book leg per settlement literals | `tokenomics`, `dao_protocol` | D5/D6 |
| **PR5** | DApp surface for binding a QR to a pseudo slot + permissions action | `dapp_beta`, `treasury-cache` | D5 |
| **PR6** | **In-place promotion** (existing link/submission writes K/L onto the pseudo row) + unbound-submission fill (`cepotx-survey`) | `tokenomics`, `dao_protocol` | SD6/SD15 |
| **PR7** | Render pseudo slots + assigned state + the **honest-state label** on the tree page, `sunmint.html`, `/sunmint/plots/` | `truesight_me_beta` | SD5  — render matrix §5.1 |
| **PR8** | Live UAT on beta → promotion (always-stop) | — | **governor** |

Per `OPERATING_INSTRUCTIONS.md` §5a: **one PR per execution turn, then stop.**

---

## 10. Related

- `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` — D3; **§8 Addendum** answers D3 with this design
- `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` — the **real** link mechanism this reuses
- `plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — ledger literals (supersedes linking-plan §7)
- **Rulings:** all D-decisions settled 2026-10-14 (Gary, via Envoy) — see §8
- `growth/GROWTH_MODEL.md` — honest-state principle; QR Trace-Back Loop
- `SUNMINT_PLOTS_REGISTRY.md` — plot schema, `plot_type` vocabulary
- `tokenomics/SCHEMA.md` — `Agroverse QR codes`, `SunMint Tree Planting`, `SunMint Plots`
- U3 (live) — `expected_trees` + `expected_trees_source`, governor-editable (`SunMint Plots` col T)
