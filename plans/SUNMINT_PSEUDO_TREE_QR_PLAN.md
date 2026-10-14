# SunMint: Pseudo-Tree Generation + QR Slot Assignment — Design & Roadmap

> **Status:** design / roadmap only — **no code, no schema change, no build units started.**
> **Gary's shape ruling (2026-10-14) is folded in as authoritative** (§0.1) — it settles SD1–SD7 and
> the §6 reconciliation rules; the remaining open decisions (D2/D4/D5/D7/D8–D12, §8) must be ruled
> before any build unit (§9) begins.
> **Owner:** Gary Teh. **Drafted by:** Sophia Truesight, 2026-10-14, at Gary's request (via Envoy).
> **Companion:** `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` **§8 Addendum** answers **D3** with
> this design.
> **Relation to prior plans:** this **answers open decision D3** of the estimation plan with a third
> option; it **extends** (does not replace) `SUNMINT_TREE_QR_LINKING_PLAN.md`'s real-tree link
> mechanism.

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

### 0.1 Gary's shape ruling (2026-10-14) — AUTHORITATIVE

Gary proposed the concrete shape (pts 1–3) and the reconciliation rules (pt 4); folded in below as the
settled design:

1. **Tell them apart —** a **`record_type`** (or `source`) field on whatever the per-tree record
   becomes: **`pseudo-estimated`** vs **`actual-submission`**, with room for a future
   **`cepotx-survey`** source (if CEPOTX's compiled data lands as a bulk import rather than
   individual farmer submissions). The **honest-state principle** from `growth/GROWTH_MODEL.md`
   applies directly: a pseudo tree's QR / landing-page view must **say so plainly** (e.g. *"estimated
   planting slot, not yet individually verified"*) rather than imply false precision — same spirit as
   the existing `spacing-estimate` / `sampled` / `counted` tiers.
2. **Generate pseudo trees —** derive point positions from the **same 3 m-spacing grid behind
   `expected_trees`** (U2's density model), **scoped to the plot polygon**, each with a **stable id**
   (e.g. **`<plot_id>-pseudo-<N>`**) so it is a **durable target** for a QR link — *not a
   recomputed-every-run throwaway*.
3. **Link QR → pseudo tree —** **reuse or extend `[TREE PLANTING LINK EVENT]`'s shape/handler**
   rather than inventing a parallel mechanism — the **same atomic pattern (QR row + a tree row +
   ledger leg)**, just pointed at a **pseudo-tree row** instead of a real `SunMint Tree Planting` row
   for now.
4. **Reconcile later (real tree lands) —** **nearest-pseudo-tree match within a radius** when a real
   tree submission / CEPOTX import lands in the same plot; **re-point the QR's link to the real tree
   id**, **retire (not delete — audit trail) the pseudo row**, and **flip `record_type` on the
   surviving link**. Needs an **explicit match radius** + a policy for **ambiguous collisions** (two
   real trees near one pseudo slot, or vice versa) — those are **never silently auto-resolved**
   (→ §6, decisions D11/D12).

### 0.2 Grounding (read before proposing anything — done)

| Source | What it fixes for this design |
|---|---|
| `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` | D3; tiered labels (`spacing-estimate` / `farmer-reported` / `sampled` / `counted`); the **plot_hectares × 1,100 (~3 m spacing)** rule, applied to **planted extent only**, cross-checked vs the farmer report; **gating** (mature / cabruca / native / explicitly-numbered never auto-estimated). Its **§8 Addendum** now answers D3 = this design |
| `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` | The **real** mechanism: `[TREE PLANTING LINK EVENT]` flips a QR to `ASSIGNED_TO_TREE` and copies lat/long/photo/species onto the QR row. Pseudo trees **reuse this shape**, pointed at a pseudo row (§5) |
| `growth/GROWTH_MODEL.md` | **Honest-state principle** — §"How to extend this model" step **4** (*"Set status honestly"*) + the **anti-patterns** section. The **QR Trace-Back Loop** (customer → tree page) is the surface where the honesty label must actually render |
| `tokenomics/SCHEMA.md` | `Agroverse QR codes` col **AC `Linked Plot ID`** (plot-fallback link, plan PR6) already exists; `ASSIGNED_TO_TREE` already in the status enum |
| `SUNMINT_PLOTS_REGISTRY.md` | plot schema, boundary tiers, `plot_type` vocabulary, single-column rule |
| **U3 (live)** | `plots/index.geojson` now carries `expected_trees` + `expected_trees_source`, **governor-editable via the `SunMint Plots` sheet** (col **T `Expected Trees`**) |

---

## 1. Concept

A **pseudo tree** is a **non-photographed placeholder slot** inside a plot polygon, minted from the
plot's `expected_trees` estimate. It is a *stand-in* for a real tree that has not (yet) been
submitted with evidence.

A **real tree** is an actual `[TREE PLANTING EVENT]` submission — it carries a photo, a planter
signature (`pk_hash`), and (usually) GPS.

Lifecycle of a pseudo tree:

```
  available ──(QR bound)──▶ assigned ──(real tree linked)──▶ reconciled ──(QR re-pointed)──▶ retired
      │
      └──(estimate shrinks)──▶ retired          (only if never referenced — see D8)
```

**Design intent (credentialing-lineage principle, restated by Gary 2026-10-14):** a pseudo tree
asserts **nothing** about the physical world except *"the estimator expects roughly N trees here."*
It must always be visibly labelled as an estimate, never confused with a counted/evidenced tree.

---

## 2. How a pseudo tree is told apart from a real tree ("a clean way to tell")

**Primary marker (Gary's ruling): the `record_type` field** on the per-tree record.

| `record_type` | Meaning | Evidence carried | Tier |
|---|---|---|---|
| **`actual-submission`** | A real `[TREE PLANTING EVENT]` — a farmer/student submitted it | `photo_url` + planter `pk_hash` + GPS | `counted` / `farmer-reported` / `sampled` |
| **`pseudo-estimated`** | A slot derived from `expected_trees` (this doc) | **none** — inherits only the *plot's* boundary evidence | `spacing-estimate` |
| *(future)* **`cepotx-survey`** | CEPOTX's compiled survey data, imported as a **bulk** set rather than individual submissions | survey source ref (TBD) | TBD |

Id scheme (Gary): **`<plot_id>-pseudo-<N>`**, e.g. `RM-P2-pseudo-0007`. This is (a) human-readable,
(b) sorts by plot, and (c) provably distinct from the real ids `pick_tree_id` emits (`Edgar_*` /
numeric) — no prefix reservation needed.

**Supporting markers** (so no consumer has to parse the id):

| Aspect | real | pseudo |
|---|---|---|
| `record_type` | `actual-submission` (or absent ⇒ real, for backward compat) | `pseudo-estimated` |
| QR status when bound | `ASSIGNED_TO_TREE` | see **D5** |
| geometry | real point | grid point (`geometry_source: "spacing_grid"`, §3) |
| public label | tree page | **"estimated planting slot, not yet individually verified"** (§7) |

**Rule:** an agent/consumer branches on `record_type` alone. A pseudo tree must **never** be silently
promoted to a real tree — reconciliation (§6) **flips `record_type` on the surviving link** and
retires the pseudo row; it never relabels the pseudo row in place.

---

## 3. Where pseudo trees live and how they are generated (Gary's ruling, §0.1 pt 2)

**Source of the count:** the plot's `expected_trees` (U3), which carries `expected_trees_source` ∈
{`sheet`, `estimate`} and is gated (blank for mature/research). **Tier:** `spacing-estimate` when
`estimate`; `farmer-reported` when a governor set a sheet override that came from a farmer count.

**Positions:** derived from the **same 3 m-spacing grid** behind `expected_trees` (the
`plot_hectares × 1,100` model), **scoped to the plot polygon** — i.e. lay the grid inside the polygon
boundary, so points fall only on the planted extent, not a bounding box. Deterministically seeded by
`plot_id` so the grid is stable between builds. Each point gets `geometry_source: "spacing_grid"`.

**Durability (the load-bearing requirement):** ids are **stable and durable** — `<plot_id>-pseudo-<N>`
is a target a QR can be bound to; it is *not* recomputed-every-run. Concretely: once a slot is
**referenced** (bound to a QR), its id + position are **frozen forever**, even if the estimate later
changes (§6 safety / D8).

**Generate-all vs allocate-on-demand (→ D2):**

- **(a) Allocate-on-demand.** Mint an id only when a QR is actually bound; `expected_trees` is the
  ceiling; persist only issued slots. Scales — a plot with 5,556 expected trees mints nothing until a
  QR asks for slot #1. **Consistent with Gary's durability rule** (issued slots are real + frozen).
- **(b) Materialize the full grid.** Write all N slots up front. Simpler to reason about and gives a
  complete map layer, but mints thousands of empty rows per plot unless capped.

Gary's phrasing (*"derive point positions … each with a stable id … a durable target"*) reads as:
**the grid is computed, ids are deterministic, and referenced ids freeze** — which both options
satisfy. D2 picks between them.

---

## 4. Storage & schema

### 4a. The per-tree record

Gary's ruling puts `record_type` *"on whatever the per-tree record becomes."* Two placements (→ D4):

- **(a) One per-tree record space** — pseudo slots live alongside real trees (the tree registry /
  `trees/index.geojson`), distinguished by `record_type`. **One join key space**; the map and the QR
  linkage stay simple. **Recommended.**
- **(b) A separate `SunMint Pseudo Trees` tab + index** — cleaner separation, but a second id space and
  a reconciliation join across two registries.

### 4b. Pseudo-slot state (if (a), the extra columns live on the pseudo rows; if (b), a new tab)

| Field | Notes |
|---|---|
| Pseudo Tree ID | `<plot_id>-pseudo-<N>` |
| Plot ID | FK → `SunMint Plots!A` |
| Seq (`N`) | integer slot index within the plot |
| record_type | `pseudo-estimated` |
| Tier | `spacing-estimate` / `farmer-reported` |
| Estimated At | when minted |
| Status | `available` / `assigned` / `reconciled` / `retired` |
| Assigned QR Code | FK → `Agroverse QR codes!A` |
| Assigned At | |
| Reconciled Tree ID | FK → the real tree once it lands |
| Reconciled At | |

*(Written by the `sunmint-ledger-manager` SA — same principal as the `SunMint Plots` tab.)*

---

## 5. QR → pseudo-tree link (Gary's ruling, §0.1 pt 3 — REUSE the link event)

The real path (`SUNMINT_TREE_QR_LINKING_PLAN.md`) is:

```
[TREE PLANTING LINK EVENT]  →  validate QR.status=SOLD & row.status=NEW
                            →  QR.status := ASSIGNED_TO_TREE
                            →  copy planting date/lat/long/photo onto the QR row
                            →  governor gate; email owner; book ledger leg
```

**Ruling: reuse/extend this exact shape — do NOT invent a parallel mechanism.** The pseudo path is
the same **atomic pattern (QR row + a tree row + ledger leg)**, with the target being a
**pseudo-tree row** instead of a real `SunMint Tree Planting` row. Concretely, the same handler:

1. resolves the signer → governor check (unchanged);
2. validates the QR is linkable (reuse the existing status preconditions);
3. **binds to a pseudo row** — allocate the next free `<plot_id>-pseudo-<N>` on the target plot (or
   accept an explicit id), mark it `assigned`, and **freeze its id + position**;
4. writes the QR row: pseudo tree id + plot id + tier, and sets the QR status (→ **D5**);
5. books the **same ledger leg** the real link books, and (optionally) emails the owner.

**Difference from the real path, and why:** there is **no planting evidence to copy** (none exists),
so instead of lat/long/photo the QR row carries the **pseudo tree id + plot id + tier**, and the
public label is the honest-state string (§7). The link is a *reservation of a slot*, not an assertion
that a specific tree exists.

**Event type:** per the ruling, **extend `[TREE PLANTING LINK EVENT]`** (e.g. an added
`Link Target` / `Record Type` field) rather than minting `[PSEUDO TREE ASSIGN EVENT]`. This supersedes
this doc's first draft (which had recommended separate events). The one caution: folding two targets
into one handler means the handler must branch on `record_type` — keep that branch tight and tested, or
revisit D6.

**Ledger-literals caveat (correction to carry forward):** the link-time ledger booking in
`SUNMINT_TREE_QR_LINKING_PLAN.md §7` was **superseded** by
`plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md`. PR4 must book the pseudo-assign ledger leg
using the **settlement plan's literals**, not the old §7.

---

## 6. Real → pseudo reconciliation (Gary's ruling, pt 4)

When a **real** `[TREE PLANTING EVENT]` (or a bulk `cepotx-survey` import) lands in a plot that has
assigned pseudo slots, reconcile by **nearest-pseudo match within a radius**:

1. Compute the nearest **assigned** pseudo slot to the real tree's point, **within `MATCH_RADIUS_M`**
   (→ **D11**; recommend starting at **~6 m ≈ 2× the 3 m grid spacing**, tightened once real GPS
   accuracy is known).
2. **Uniqueness required.** Auto-reconcile **only** when the match is *unique* — exactly one candidate
   on each side (one real tree ↔ one pseudo slot) within the radius. Write the pseudo row's
   `Reconciled Tree ID` / `Reconciled At` and set `Status := reconciled`.
3. **Re-point the QR's link to the real tree id**: QR → `ASSIGNED_TO_TREE`, copy the real planting
   evidence onto the QR row (hand off to the existing real-link mechanics), and **flip the surviving
   link's `record_type` from `pseudo-estimated` → `actual-submission`** (the link now points at a real
   tree).
4. **Retire, never delete:** the pseudo row is set **`Status := retired`** and kept **forever** for the
   audit trail — it is **not** deleted and **not** renumbered.
5. Emit the auditable signed reconcile record (reuse the extended link event, or a reconcile variant).

**Ambiguous collisions are NEVER auto-resolved** (Gary's explicit constraint):

- **Two real trees near one pseudo slot** → do not pick one; enqueue **all** onto a governor **review
  list** (with distances).
- **One real tree near two pseudo slots** → do not pick one; enqueue onto the review list.
- **≥2 candidates within the radius on either side** → **review list, no write**.
- **No candidate within radius** → leave both sides untouched; the real tree simply stands as its own
  `actual-submission` row and the pseudo slot stays `assigned` (the QR keeps pointing at the pseudo
  slot until a human rules).

**Priority rule:** a **real tree** landing in a plot should claim the QR **before** a fresh pseudo slot
does, when both are possible.

**Invariant:** the pseudo row is **never deleted** (audit history) and **never relabelled in place**;
reconciliation is a *link re-point* + a `record_type` flip on the **surviving** link, plus a
`retired` status on the pseudo row.

**Bulk `cepotx-survey` import:** if CEPOTX's data lands as a bulk set rather than individual
submissions, §2's `cepotx-survey` record_type is the landing shape — reconcile those rows to pseudo
slots by the same spatial join (§6.1–6.5), at import time rather than per-submission.

---

## 7. Honest state — the visible label (Gary's ruling, §0.1 pt 1)

This is the part that keeps the whole scheme defensible, and it maps directly onto
`growth/GROWTH_MODEL.md`:

- **`GROWTH_MODEL.md` §"How to extend this model" step 4 — *"Set status honestly."*** A pseudo tree is
  the 🟩/⬜ case at the per-record level: it must not be presented as signal it hasn't produced.
- **The anti-patterns section** is the cautionary mirror: a surface that *manufactures* the impression
  of evidenced work is exactly what we refuse to do.
- **The QR Trace-Back Loop** (customer buys cacao → scans QR → lands on the tree page) is the surface
  where this must actually render. A pseudo-bound bag's page must read, plainly:

  > **Estimated planting slot — not yet individually verified.** This bag is earmarked for 1 of ~N
  > trees expected on plot `RM-P2` (spacing estimate). A specific tree will be linked once evidence
  > is submitted.

**Consequence (→ D10):** a pseudo-assigned bag must **not** increment any public "trees planted"
counter. Counting a spacing estimate as planted is precisely the false-precision claim the honest-state
principle forbids.

---

## 8. Decisions — settled vs open

### Settled by Gary's ruling (2026-10-14)

| # | Decision | Ruling |
|---|---|---|
| **SD1** | Distinction field | **`record_type`**: `pseudo-estimated` / `actual-submission` / (future) `cepotx-survey` |
| **SD2** | Pseudo-tree id | **`<plot_id>-pseudo-<N>`**, stable + durable; referenced ids frozen |
| **SD3** | Generation source | **3 m-spacing grid** behind `expected_trees` (U2), **scoped to the plot polygon** |
| **SD4** | Link mechanism | **Reuse/extend `[TREE PLANTING LINK EVENT]`** — same atomic pattern, no parallel mechanism |
| **SD5** | Honesty | QR/landing page must say **"estimated planting slot, not yet individually verified"** |
| **SD6** | Reconcile outcome | **Re-point QR to real tree id · retire (not delete) pseudo row · flip `record_type` on the surviving link** |
| **SD7** | Ambiguity | **Never silently auto-resolve** ambiguous collisions — route to a governor review list |

### Still open — NEED a ruling

| # | Decision | Options | **Recommendation** |
|---|---|---|---|
| **D2** | Materialize the full grid vs allocate-on-demand | (a) on-demand (b) materialize | **(a)** — scales; referenced ids frozen either way |
| **D4** | Where the per-tree record lives | (a) one space + `record_type` (b) separate pseudo tab | **(a)** — one join key space |
| **D5** | QR status when pseudo-bound | reuse `ASSIGNED_TO_TREE` vs new `ASSIGNED_TO_PSEUDO_TREE` | **new status** — but note: if reused, D10's counter guard needs a *column* check, which is weaker |
| **D7** | Reconcile trigger | auto spatial-join vs manual | **auto-join + governor review list** (mirrors linking-plan D4) |
| **D8** | Estimate shrink/grow safety | see §6-of-first-draft rule | **freeze referenced slots; trim only never-referenced tail** |
| **D9** | Gating — which `plot_type`s may mint | all vs subset | **`restoration` / `enrichment` / `nursery` only** — never `mature` / `research` / blank |
| **D10** | Public "trees planted" counter | count pseudo-assigned? | **NO** — `pseudo-estimated` must not be counted as planted (honest state) |
| **D11** | Reconciliation match radius (`MATCH_RADIUS_M`) | ~3 m vs ~6 m vs GPS-accuracy-derived | **start ~6 m (2× grid), tighten with real GPS accuracy** |
| **D12** | Ambiguous-collision policy | auto-pick nearest vs review list | **review list — never auto-resolve** (per SD7) |

---

## 9. Mapped work units (sequenced; **none started**)

| Unit | Scope | Repo | Gate |
|---|---|---|---|
| **PR0** | **this doc** + the estimation-plan §8 addendum | `agentic_ai_context` | review |
| **PR1** | D2/D4/D5/D7/D8–D12 ruled; these docs updated with the rulings | `agentic_ai_context` | **governor** |
| **PR2** | `build_plots_geojson.py`: emit the **3 m spacing grid** scoped to the polygon with `<plot_id>-pseudo-<N>` ids + `record_type`, gated by `plot_type` — **no allocation/QR coupling yet** | `sunmint` | SD3/D9 |
| **PR3** | Pseudo-slot state (tab or columns) + allocator + **freeze-on-reference** | `sunmint` | D2/D4/D8 |
| **PR4** | **Extend `[TREE PLANTING LINK EVENT]`** handler to accept a pseudo target (`record_type` branch) + `dao_client` field — *not* a new event; book the leg per the settlement plan's literals | `tokenomics`, `dao_protocol` | D5 |
| **PR5** | DApp surface for binding a QR to a pseudo slot + permissions action | `dapp_beta`, `treasury-cache` | D5 |
| **PR6** | Reconciliation (§6): nearest-match within radius, unique-only, **review list** for ambiguity; `cepotx-survey` bulk path | `tokenomics`, `dao_protocol` | D7/D11/D12 |
| **PR7** | Render pseudo slots / assigned state + the **honest-state label** on the tree page, `sunmint.html`, `/sunmint/plots/` | `truesight_me_beta` | SD5 |
| **PR8** | Live UAT on beta → promotion (always-stop gate) | — | **governor** |

Per `OPERATING_INSTRUCTIONS.md` §5a: **one PR per execution turn, then stop.** Report the DAO
contribution after each merge (§6).

---

## 10. Related

- `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` — D3, tier labels, the ×1,100 (~3 m) rule, gating;
  **§8 Addendum** answers D3 with this design
- `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` — the **real** link mechanism this reuses
- `plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — ledger literals (supersedes linking-plan §7), `Linked Plot ID` col AC
- `growth/GROWTH_MODEL.md` — honest-state principle (§"How to extend this model" step 4 + anti-patterns); QR Trace-Back Loop
- `SUNMINT_PLOTS_REGISTRY.md` — plot schema, `plot_type` vocabulary, single-column rule
- `SUNMINT_E2E_RUNBOOK.md` — rebuild + beta/prod render flow
- `tokenomics/SCHEMA.md` — `Agroverse QR codes`, `SunMint Tree Planting`, `SunMint Plots` schemas
- U3 (live) — `expected_trees` + `expected_trees_source`, governor-editable (`SunMint Plots` col T)
