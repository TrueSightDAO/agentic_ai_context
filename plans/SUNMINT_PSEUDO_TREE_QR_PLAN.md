# SunMint: Pseudo-Tree Slots + QR Assignment — Design & Roadmap (v9)

> **Status:** design / roadmap only — **no code, no schema change, no build units started.**
> **v9 (2026-10-14) — three-tier render logic recorded** (Gary, approved): the provenance image is
> chosen by **what evidence actually exists** — real tree photo (T1) → plot photo *with the caveat
> caption* (T2) → **no image, honest text only** (T3). A bare/best-guess photo is **never** shown.
> See §7.
> **v8 (2026-10-14) — Contract A write-set pinned to EXISTING columns / the reverse-binding mechanism** (Gary):
> (3) capacity exceeded → **REJECT** (never over-mint past `expected_trees`); (4) the **D9 plot-type gate**
> (`restoration`/`enrichment`/`nursery` only) **applies to Contract A's create branch too**; (5) the binding
> **reuses the existing `Linked Plot ID` (col AC)** — **no parallel field**. Verified against the real-link
> path (`process_tree_planting_link.js` ~L1024–1037): binding is stored **on the tree row** (`Status=LINKED`,
> `Linked QR`, `Linked At`); the QR row carries **no tree ref**. So Contract A's write-set is **existing
> columns only** and a pseudo row is **the same code path** as a real row. See §5.1.
> **v7 (2026-10-14) — Contract A is a HANDLER UPGRADE, not a new surface** (Gary): Contract A
> (QR↔Plot link) is **not** a new DApp page or a new event — it **upgrades the EXISTING plot-link path**
> (`process_tree_planting_link.js` ~L936–987; the *"link to a plot (no tree submission)"* picker already
> live on `link_tree_planting.html`). The upgrade = **find-or-create bounded by `expected_trees`** +
> the **status flip `ASSIGNED_TO_TREE` → `ASSIGNED_TO_PSEUDO_TREE`**, which is the **fix for a LIVE GAP**
> (the plot path today reuses the real-tree status, inflating the public counter) — §5.1. **Contract B is
> genuinely new.** A adds **no** UI. See §5.
> **v6 (2026-10-14) — TWO separate contracts** (Gary): **A — QR ↔ Plot link**
> (`[PSEUDO TREE ASSIGN EVENT]`; input **QR + plot_id**; finds-or-creates the slot) and **B — Pseudo
> promotion** (`[PSEUDO TREE PROMOTE EVENT]`; input **plot_id/id + lat/long/photo**; edits the row in
> place). Each has its **own DApp page + CLI module** (§5.1.2/§5.2.2), and both **reuse the shared
> DApp scaffolding** — `routes.js`/`menu.js`/`tdg_balance.js`/`scripts/dao_members_cache.js`,
> `verifySignatureOnLoad()`, the governor/sentinel gate (§5.2.1). See §5.
> **v5 (2026-10-14) — promotion is a DEDICATED event `[PSEUDO TREE PROMOTE EVENT]`** (Gary): the
> existing `[TREE PLANTING EVENT]` flow only **appends** rows and cannot update a row by id, so in-place
> promotion needs its own governor/field-agent-signed event + **two surfaces (DApp page + CLI module)
> calling the same contract** — `[PSEUDO TREE RECONCILE EVENT]` stays dropped (we edit in place, we do
> not create a new linked row). See §5.2 / §8.
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
   Just placeholder slots per eligible plot (bounded by `expected_trees`), each a
   `SunMint Tree Planting`-shaped row with blank K/L, `plot_id` set, stable id. **Creation trigger
   (Gary, 2026-10-14):** a pseudo tree is created **when a QR is linked to a plot that has no
   unlinked slot left** — *"if the plot does not yet have unlinked trees ... a pseudo tree gets
   created. If the plot has unlinked trees ... the QR is linked with the next available unlinked
   tree"* (§5.1). So slots are **demand-driven by the link**, not pre-minted in bulk.
3. **Link QR → pseudo slot — NEW `[PSEUDO TREE ASSIGN EVENT]`** (Gary, 2026-10-14): no real
   mechanism binds a QR to a slot-without-a-tree today, so this is its **own** event (QR row + a row +
   ledger leg). **Promotion is a SEPARATE dedicated event — `[PSEUDO TREE PROMOTE EVENT]` (§5.2)**:
   the existing `[TREE PLANTING EVENT]` flow only **appends** rows (scraped from Telegram) and cannot
   find-and-update a row by id, so in-place promotion needs its own mechanism. **No
   `[PSEUDO TREE RECONCILE EVENT]`** — promotion edits the slot **in place**, it does not create a new
   linked row.
4. **QR codes CAN be associated with pseudo trees** (Gary, 2026-10-14) — a pseudo slot is a
   first-class link target, valid **before** any real tree exists (SD9).
5. **A pseudo tree becomes REAL in place — the SAME row** (Gary, 2026-10-14): *"pseudo tree is just
   one that has no lat and long but is associated with a plot. Once it gets assigned a lat and long it
   is no longer a pseudo tree."* Promotion writes the real K/L (+ photo + planter) **onto the same
   row** — there is **no second "real tree" row, no `[PSEUDO TREE RECONCILE EVENT]`, and no orphaned
   pseudo row kept as duplicate history.** The signed event that writes K/L **is** the audit trail
   (the ledger is current-state rows + an append-only event log). This **supersedes v2's
   claim-on-arrival §6.** The write happens via the **dedicated `[PSEUDO TREE PROMOTE EVENT]`**
   (§5.2) — **not** the append-only `[TREE PLANTING EVENT]`.

### 0.2 Grounding (read — done)

| Source | What it fixes |
|---|---|
| `plans/SUNMINT_TREE_ESTIMATION_QR_PLOT_PLAN.md` | D3; tiers (`spacing-estimate`/`farmer-reported`/`sampled`/`counted`); the ×1,100 (~3 m) rule → now only supplies the **count** `expected_trees`, not positions; gating. Its **§8 Addendum** = this design |
| `plans/SUNMINT_TREE_QR_LINKING_PLAN.md` | The **real** mechanism: `[TREE PLANTING LINK EVENT]` → `ASSIGNED_TO_TREE`, copies lat/long/photo onto the QR row. Pseudo slots reuse this shape (§5) |
| `growth/GROWTH_MODEL.md` | **Honest-state principle** — §"How to extend this model" step **4** + anti-patterns; QR Trace-Back Loop (customer → tree page) |
| `tokenomics/SCHEMA.md` | `Agroverse QR codes` col **AC `Linked Plot ID`**; `ASSIGNED_TO_TREE` in the status enum; `SunMint Tree Planting` cols incl. K/L Latitude/Longitude |
| `SUNMINT_PLOTS_REGISTRY.md` | plot schema, `plot_type` vocabulary, single-column rule |
| **U3 (live)** | `plots/index.geojson` carries `expected_trees` + `expected_trees_source`, governor-editable via the `SunMint Plots` tab col **T `Expected Trees`** |
| `dao_client/truesight_dao_client/modules/link_tree_planting.py` | the **CLI template**: a ~6-line `build_event_cli(...)` wrapper (event name + canonical labels + `required_labels` + `dapp_page`) — the promote CLI mirrors this |
| `dao_client/truesight_dao_client/server/data/events_catalog.json` | the **event registry** each event is declared in (`canonical_labels`, `required_fields`, `dapp_page`); the promote event adds an entry here |
| `dapp_beta/link_tree_planting.html` | the **DApp template**: reads public `lineage-assets` caches (`sold_pending_tree.json`, `sunmint_pending.json`) + `sunmint/main/plots/index.geojson`, POSTs via `scripts/edgar_payload_helper.js` → `edgar.truesight.me/dao/submit_contribution` |

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

## 5. Contracts — two separate events, two separate jobs

> **Gary (2026-10-14):** *"A pseudo tree gets created when we attempt to link a QR code to a plot. If
> the plot does not yet have unlinked trees associated with it, then a pseudo tree gets created. If the
> plot has unlinked trees associated with it, then the QR code is linked with the next available
> unlinked tree."* — and — *"the part of setting the lat and long for a pseudo tree should perhaps be a
> contract isn't it? ... callable via the CLI too."*

There are **two distinct contracts**, scoped separately. **A upgrades an existing handler path**
(no new event, no new page); **B is genuinely new** (new event + page + CLI). **Neither** is the append-only `[TREE PLANTING EVENT]` (`events_catalog.json`), which only
**appends** rows and cannot find-and-update a row by id.

| # | Contract | Input | Event | Effect |
|---|---|---|---|---|
| **A** | **QR ↔ Plot link** (§5.1) — **HANDLER UPGRADE to the existing plot-link path**, *not* a new surface | **QR code + `plot_id`** | **existing** `[TREE PLANTING LINK EVENT]` (Plot ID attr) | finds-or-**creates** a pseudo slot (bounded by `expected_trees`), **binds the QR**; flips status to `ASSIGNED_TO_PSEUDO_TREE` |
| **B** | **Pseudo promotion** (§5.2) | **`plot_id`/pseudo-id + lat/long/photo** | `[PSEUDO TREE PROMOTE EVENT]` | writes the real data onto that slot **in place** (pseudo → real) |

The **input differs**: A keys on the **plot** (the handler *chooses* the slot); B keys on the
**slot/location** (real values land on a specific row). Both are governor-/field-agent-gated.

### 5.1 Contract A — QR ↔ Plot link — UPGRADE to the EXISTING plot-link path (Gary 2026-10-14)

**This is NOT a new event and NOT a new page** (Gary, 2026-10-14). The `[TREE PLANTING LINK EVENT]`
handler (`tokenomics/…/process_tree_planting_link.js`) **already ships a plot branch** — the *"— or link
to a plot (no tree submission) —"* picker on the live **`dapp.truesight.me/link_tree_planting.html`**,
which submits the **same** `[TREE PLANTING LINK EVENT]` with a **`Plot ID`** attribute instead of a
tree-submission id (handler lines ~**936–987**). That path today already: resolves the plot → writes a
**representative plot image** onto the QR row (`tplResolvePlotImage_`) → **leaves lat/long blank**
(*"a plot has no single coordinate"*). Contract A = an **upgrade to that existing path** — three changes
(below), **no new surface**.

> **LIVE GAP — the bug this upgrade fixes (Gary 2026-10-14).** Gary: *"we already have this DApp"* —
> correct, and reading it surfaced a real defect. The existing plot branch has **zero capacity/slot
> concept** (no `expected_trees` check, no cap — verified: no such reference in the handler) **and sets
> the QR status to the SAME `ASSIGNED_TO_TREE` a real tree link uses**. That status is exactly what
> `agroverse_shop`'s public "trees planted" counter filters on
> (`agroverse_wix_site_updates.js::getSoldRowsCount()` → `row[3] === "SOLD" || row[3] === "ASSIGNED_TO_TREE" || …`,
> sheet `1GE7PUq…` "Agroverse QR codes", feeding **both** the `TREES_FINANCED` **and** `HECTARES` public
> stats under *"1 bag = 1 tree planted = hectares restored"*). So **every plot-level link would inflate the
> public tree/hectare count, unlimited, with no pseudo/estimate distinction** — the exact false-precision
> D10 forbids.
>
> **Honest scoping of live exposure (Sophia, verified 2026-10-14):** a scan of the live "Agroverse QR
> codes" sheet (all **1,823** rows) shows **15** `ASSIGNED_TO_TREE` rows — **all genuine tree-level
> links** (lat+long set; **col AC "Linked Plot ID" empty**); **0** rows carry a plot-only link (col AC has
> **no** non-empty cell in any row; header is 28 cols A–AB). So the path is **armed but appears not yet
> fired** — a **latent** bug (**0 hits to date**), which the status flip closes **prospectively**. ⚠️
> Confirm: (a) whether the tokenomics revision carrying the plot branch is the **deployed** GAS revision;
> (b) whether any plot write lands outside the range read (e.g. a per-ledger tab). **If any plot link
> has landed, the counter is already wrong.**
>
> **The fix (three changes):** (1) **find-or-create bounded by `expected_trees`** (step 3 below);
> (2) **stop reusing `ASSIGNED_TO_TREE`** — flip plot links to the new **`ASSIGNED_TO_PSEUDO_TREE`** so
> the public counter stops counting them (**no `agroverse_shop` change needed** — the existing filter
> simply no longer matches); (3) **plot-image write-on-link stays exactly as-is** (already correct).

**Ruling (SD9): a QR MAY be bound to a pseudo slot BEFORE any real tree exists.** The slot is **minted
on demand at assign time** (D2=(a)) and is a first-class, valid link target with **no tree behind it**.
The QR is printed/handed out now; a real tree later **promotes that same slot in place** (§6).

**Input = QR code + `plot_id`** (NOT a slot id). The handler owns the **find-or-create** decision
(Gary's logic, verbatim):

1. resolve signer → governor check (same as the link handler);
2. validate the QR is linkable (reuse existing preconditions);
3. **find-or-create the slot, bounded by capacity** — *"if the plot does not yet have unlinked trees
   ... a pseudo tree gets created. If the plot has unlinked trees ... the QR is linked with the next
   available unlinked tree"*:
   - **(a)** look up the plot's **existing unlinked trees** (real **or** pseudo) — not yet QR-bound;
   - **(b)** if **≥1** exists → bind the QR to the **next available** one (**no new row**); **tiebreak =
     oldest first** (lowest `seq`), deterministic (Gary);
   - **(c)** if **none** exists → check the plot's **`expected_trees` capacity**; if **under** the cap,
     **create** a new pseudo row (`PS-<plot_id>-<seq>`, blank K/L) then bind the QR; if **at/over** the
     cap, **REJECT** — **never over-mint past `expected_trees`** (Gary ruling #3; flag for governor review,
     same spirit as the estimation plan's over-subscribed cross-check);
4. write the QR row: **`Linked Plot ID` (col AC) = plot_id** (exactly as today), set status
   **`ASSIGNED_TO_PSEUDO_TREE`** (pseudo case) — or **`ASSIGNED_TO_TREE`** unchanged if a **real** unlinked
   tree was found/filled (D5); write the representative **plot image** (pseudo case only — the real case
   already carries the tree's own photo, unchanged);
5. write the **tree row** (real **or** pseudo, whichever was picked/created) — **exactly the three writes
   the real-link path already does** (`Status := LINKED`, `Linked QR := <qr_code>`, `Linked At := now`);
6. book the ledger leg (literals per the settlement plan — caveat below);
7. optional owner email.

**Binding is stored on the TREE row, not the QR row (Gary ruling #5, verified 2026-10-14).** Reading the
real-link path (`process_tree_planting_link.js` ~L1024–1037) settles the wiring with **zero new columns
anywhere**: the QR row gets `ASSIGNED_TO_TREE` + copied date/lat/long/photo, and the **`SunMint Tree
Planting` row** gets **`Status=LINKED` + `Linked QR`=qr_code + `Linked At`=ISO** (`{TPL_SUNMINT_STATUS_COL,
TPL_SUNMINT_LINKED_QR_COL, TPL_SUNMINT_LINKED_AT_COL}` = cols **M/R/S**). "Which tree is this QR bound to?"
is answered by **scanning tree rows for a matching `Linked QR`** — the QR side stores **no** tree ref. A
pseudo row **is** a `SunMint Tree Planting` row, so this is **literally the same code path — no branching**.

**The find query ("next available unlinked tree for plot X").** Scan `SunMint Tree Planting` for
**`plot_id == X AND Status != LINKED`** — this covers **real AND pseudo uniformly** (both live in the one
tab — SD12/D4). `plot_id` is a header-resolved column on that tab (`build_tree_geojson.py`:
`idx(header, "plot id", …)`; SCHEMA.md Trees schema: *"Plot ID … explicit override — wins when present"*).
This **confirms the earlier call to drop a separate pseudo-tree tab**: one tab, one column set, the
existing `Linked QR`/`Status` mechanism just works **unmodified** once pseudo rows exist in it.

**Plot-type gate applies to the create branch too (Gary ruling #4).** Contract A may mint a pseudo row
**only** on a `restoration`/`enrichment`/`nursery` plot (**D9**) — never `mature`/`research`/blank. The
reuse branch (b) is unaffected (it mints nothing).

**"Unlinked" is the exact test** for (a)/(b): pseudo (blank K/L) **and** no QR bound to it. The slot
the QR binds to is then **frozen** (its id never renumbered — D8).

**Difference from the real link:** the QR row carries **no position** — the assign is a *reservation
of a slot*, not an assertion that a located tree exists.

**Promotion is NOT a new event.** When the real submission lands it writes real K/L (+ photo) onto the
**SAME row** via the **existing `[TREE PLANTING LINK EVENT]`/submission mechanism** (§6). There is
**no `[PSEUDO TREE RECONCILE EVENT]`** (D6 — dropped).

**Ledger-literals caveat:** `SUNMINT_TREE_QR_LINKING_PLAN.md §7` was **superseded** by
`plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — book the leg with the settlement plan's
literals.

#### 5.1.1 QR owner experience — what the provenance page shows (Gary, 2026-10-14)

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

#### 5.1.2 Surfaces — Contract A: **NONE NEW** (Gary 2026-10-14)

**No new DApp page, no new CLI module.** The *"link to a plot (no tree submission)"* option already
lives on the existing **`dapp_beta/link_tree_planting.html`** (+ its **`modules/link_tree_planting.py`**
wrapper) — same page, same styling, same picker. Contract A changes only the **handler behind that
existing option**, so Gary's UI/UX-consistency ask (§5.2.1) is satisfied **trivially**: nothing new is
built at the surface layer. (The handler upgrade is PR4, §9.)

---

### 5.2 Contract B — Pseudo promotion — `[PSEUDO TREE PROMOTE EVENT]` (Gary, 2026-10-14)

**Why a dedicated event.** The existing `[TREE PLANTING EVENT]` flow only **appends** new rows
(scraped from Telegram chat logs); it has **no** "find this specific existing row by *id* and update
it" capability. Promoting a pseudo tree **in place** (Gary's same-row model, §6) therefore needs its
own mechanism. This **walks back** the earlier suggestion to "reuse the submission mechanism" for
promotion — the submission mechanism *creates*, it does not *edit*.

> **`[PSEUDO TREE PROMOTE EVENT]`** — governor- or field-agent-signed. Payload: **plot_id** (or the
> pseudo tree id) **+ Latitude + Longitude + Photo URL** (+ Species/Planter/Planting Time as the real
> planting needs). The handler **finds the matching pseudo row** (blank K/L *and* matching `plot_id`,
> i.e. an open slot) and **writes the real values onto it in place** — same `Tree ID`, which flips
> from pseudo to real the moment this lands (§6). It does **not** append a row.

- **Distinct from `[PSEUDO TREE ASSIGN EVENT]`** (§5): that one binds a **QR** to a slot; this one
  writes **location + photo** onto the slot. Different act, different payload, different surface.
- **Rejected server-side** if the signer isn't a governor/field agent (same Governors-tab gate as the
  other tree events). **Reject** if no open pseudo row matches the plot, or if the payload lacks a
  photo (unverifiable planting — `[TREE PLANTING EVENT]`'s rule: *no photo ⇒ cannot be verified ⇒ reject*).
- **QR side-effect** (only when the target slot is QR-bound): copy the planting evidence onto the QR
  row and set its status to **`ASSIGNED_TO_TREE`** (from `ASSIGNED_TO_PSEUDO_TREE`), so the provenance
  page switches from the plot image to the real tree photo (§5.1). An **unbound** promotion has no QR
  to touch.
- **No `[PSEUDO TREE RECONCILE EVENT]`** (still dropped): we **edit in place**, we do **not** create a
  new linked row — so there is nothing to "reconcile."

#### 5.2.1 UI/UX consistency — new DApp pages match the existing DApp (Gary, 2026-10-14)

The one **new** page (`promote_pseudo_tree.html` — Contract B) **must reuse the shared DApp
scaffolding** — **no one-off styling**. Verified present in `dapp_beta`:

- Load the same shared scripts: **`routes.js`**, **`menu.js`**, **`tdg_balance.js`**,
  **`scripts/dao_members_cache.js`** (and, for submits, `scripts/edgar_payload_helper.js`).
- Use the same **signature-auth gate pattern** (`verifySignatureOnLoad()`) and set
  `API_ENDPOINT = window.Routes.edgar.submit` → `edgar.truesight.me/dao/submit_contribution`.
- Use the same **governor/sentinel gating convention** as `review_queue.html` /
  `link_tree_planting.html`: roles resolved from **`treasury-cache/dao_members.json`**
  (`roles.indexOf('governor')` / `'sentinel'`), controls **disabled** unless authorized, and the
  `✓ Governor` badge. The **same gate** applies server-side to both events.
- Same **"Saffron Monk" / earthen palette** + layout as the rest of the DApp (the `link_tree_planting.html`
  `<style>` block is the reference).

#### 5.2.2 Surfaces — Contract B (Pseudo promotion)

Both surfaces call the **same contract** (the event above):

| Surface | Shape | Template to mirror |
|---|---|---|
| **DApp page** — e.g. `dapp_beta/promote_pseudo_tree.html` | Fetch the plot's **open pseudo slots** by `plot_id` (so the user sees *which* slots are free), pick one, submit lat/long/photo. Reads public caches (same `lineage-assets`/`sunmint` geojson convention) and POSTs via `scripts/edgar_payload_helper.js` → `edgar.truesight.me/dao/submit_contribution`. | **`dapp_beta/link_tree_planting.html`** (the plot-select + submit-link shape) |
| **CLI module** — e.g. `dao_client/truesight_dao_client/modules/promote_pseudo_tree.py` | Same two operations: **list** open pseudo trees for a plot; **submit** the lat/long/photo update. Scriptable, no browser. Declares the event in `events_catalog.json`. | **`modules/link_tree_planting.py`** (a `build_event_cli(...)` wrapper) |

- **"Fetch pseudo trees by plot id"** = the read backing **both** surfaces. Pseudo trees are rows with
  **blank K/L + a matching `plot_id`** (§2) — so the list is a registry read, and the **DApp/CLI must
  not hard-code slot ids** (the allocator owns them, §PR2).
- **Contract-first:** the DApp page and the CLI **must** accept/submit the *same* payload fields, so a
  promotion is scriptable end-to-end with no browser (Gary: *"callable via the CLI too"*).

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
4. Emit the **signed `[PSEUDO TREE PROMOTE EVENT]`** (§5.2) that carries the K/L — that event is the
   promotion's audit record. (The append-only `[TREE PLANTING EVENT]` is **not** used here — it cannot
   edit a row by id.)

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

**Three-tier render logic (Gary, 2026-10-14 — approved).** The image on the provenance page is chosen
by **what evidence actually exists** — a bare/best-guess photo is **never** shown:

| Tier | Row state | Page renders | Caption |
|---|---|---|---|
| **T1 — real tree** | QR `ASSIGNED_TO_TREE`; the tree row carries K/L + its own photo | the **tree's own photo** + map pin + planting evidence | *(none — the evidence is of this tree)* |
| **T2 — pseudo, plot *has* media** | QR `ASSIGNED_TO_PSEUDO_TREE`; plot `media` non-empty; slot has no real photo | the **plot's `media` photo** (from `plots/index.geojson`); **no map pin** | *"photo shows the plot where this tree is expected, not the individual tree."* |
| **T3 — pseudo, plot has *no* media** | QR `ASSIGNED_TO_PSEUDO_TREE`; plot `media` empty | **no photo** — the honest estimate text only (**never** a bare/placeholder image passed off as evidence) | the estimate copy above + *"No plot photo available yet."* |

**Golden rule (the caveat Gary flagged).** A photo is rendered **only** when it is real evidence — of
*this tree* (T1) or of *the plot* (T2, explicitly captioned). **T3 deliberately shows no image** rather
than ship a bare photo a customer could mistake for their tree. Same honesty commitment as D10, applied
to the *image* (SD5). Tier selection is a **runtime** decision (T1 vs T2/T3 = the row's real-vs-blank
K/L; T2 vs T3 = whether the plot's `media` is non-empty), so promotion flips the tier with **no re-link**.

---

## 8. Decisions — settled vs open

### Settled by Gary's rulings (2026-10-14)

| # | Decision | Ruling |
|---|---|---|
| **SD1** | Distinction marker | **blank Latitude/Longitude** (+ `PS-` prefix). **No `record_type` column** |
| **SD2** | Pseudo id | **`PS-<plot_id>-<seq>`**, immutable — frozen on reference, **unchanged on promotion**; the `PS-` prefix is a provenance namespace, **not** a live state test |
| **SD3** | Geometry | **NONE** — no grid, no computed positions (v1 grid dropped) |
| **SD4** | Assign mechanism | **UPGRADE to the existing plot-link path** (NOT a new event) — input **QR + `plot_id`**; handler **finds-or-creates** the slot, **bounded by `expected_trees`** (Contract A, §5.1) |
| **SD5** | Honesty | QR/landing page: **"Plot X — estimated slot #N. Position not yet verified."** + **plot `media` image** (not the tree's), caption *"plot, not the individual tree"* (§5.1) |
| **SD6** | Promotion | **In place, same row** — real K/L written onto the pseudo row makes it real; **no second row, no reconcile event, no orphan** (supersedes v2 FIFO-claim) |
| **SD7** | Ambiguity | **N/A** — in-place promotion removes matching entirely; nothing to disambiguate |
| **SD8** | Row shape | same as `SunMint Tree Planting`, blank K/L, no photo, `plot_id` set |
| **SD9** | Link timing | **A QR MAY be bound to a pseudo slot BEFORE any real tree exists** (Gary, 2026-10-14) — the slot is **created on demand (find-or-create) at link time**, not awaited from a submission |
| **SD10** | Promotion | A pseudo row becomes real by gaining K/L **on itself**; the **signed planting event is the audit trail** — **no duplicate row** (Gary, 2026-10-14) |
| **SD11** | Row id (D1) | **`PS-<plot_id>-<seq>`** — kept for legibility + per-plot dedup; **not load-bearing** (a plain tree-id would do, since the row **is** a normal tree row) |
| **SD12** | Registry (D4) | **ONE registry** — a pseudo tree is just a `SunMint Tree Planting` row with blank K/L; **no separate tab** |
| **SD13** | QR status (D5) | **new `ASSIGNED_TO_PSEUDO_TREE`** — keeps the ledger legible without inspecting lat/long **and drops these rows out of the public "trees planted" counter filter** (§5.1 live gap) |
| **SD14** | Events (D6) | **No new event for A** — QR→slot binding **upgrades the existing `[TREE PLANTING LINK EVENT]`** plot branch; **one** new event for B (`[PSEUDO TREE PROMOTE EVENT]`); **no `[PSEUDO TREE RECONCILE EVENT]`** |
| **SD16** | Promotion event (D6, Gary 2026-10-14) | **NEW dedicated `[PSEUDO TREE PROMOTE EVENT]`** — edits a pseudo row in place (lat/long/photo). Needed because `[TREE PLANTING EVENT]` only **appends** (no update-by-id). Governor/field-agent-signed. **Two surfaces, one contract**: DApp (`promote_pseudo_tree.html`) + CLI (`promote_pseudo_tree.py`). **No reconcile event** |
| **SD17** | Two contracts (Gary 2026-10-14) | **A** QR↔Plot link = **HANDLER UPGRADE** to the existing plot-link path (input **QR + plot_id**, find-or-create bounded by `expected_trees`) — **no new event/page** **≠** **B** Pseudo promotion `[PSEUDO TREE PROMOTE EVENT]` (input **id + lat/long/photo**, in-place) — **genuinely new** (own page + CLI) |
| **SD18** | DApp UI/UX (Gary 2026-10-14) | The one **new** page (B's `promote_pseudo_tree.html`) **reuses the shared DApp scaffolding** — `routes.js`, `menu.js`, `tdg_balance.js`, `scripts/dao_members_cache.js`, `verifySignatureOnLoad()`, governor/sentinel gate (§5.2.1). **No one-off styling.** A adds **no** page. |
| **SD19** | Live gap fixed (Gary 2026-10-14) | The existing plot-link path reuses `ASSIGNED_TO_TREE`, so it would inflate the public tree/hectare counter (unlimited, no estimate distinction). **Contract A's status flip → `ASSIGNED_TO_PSEUDO_TREE` is the fix.** Verified **0 plot-level links to date** (latent) — §5.1 |
| **SD20** | Contract A write-set (Gary 2026-10-14) | **Existing columns only, no parallel field.** QR row: `Linked Plot ID`=plot_id (col AC), status `ASSIGNED_TO_PSEUDO_TREE`\|`ASSIGNED_TO_TREE`, plot image (pseudo only). Tree row: `Status=LINKED`, `Linked QR`=qr_code, `Linked At`=now (**same 3 writes as the real path**, cols M/R/S). **Binding lives on the TREE side**; find-unlinked = `plot_id==X AND Status!=LINKED` over the one tree tab |
| **SD15** | Unbound submission (D7/D8) | Fills the **first/any open slot in the plot** (lowest free `seq`); none open → stands alone. **No spatial matching** |

### Settled in PR1 (Gary, 2026-10-14)
| # | Decision | Ruling |
|---|---|---|
| **D1** | Row id scheme | **`PS-<plot_id>-<seq>`** — legibility + per-plot dedup; **not load-bearing** (SD11) |
| **D2** | Mint up front vs on demand | **create-or-reuse at link time, bounded by `expected_trees`** — reuse the plot’s next **unlinked** slot (oldest first), else create if **under cap** (else reject) (Contract A, §5.1); pairs with in-place promotion |
| **D4** | Where pseudo rows live | **ONE registry** — `SunMint Tree Planting`, blank K/L (SD12) |
| **D5** | QR status when pseudo-bound | **new `ASSIGNED_TO_PSEUDO_TREE`** (SD13) |
| **D6** | Events | **ONE new event** — `[PSEUDO TREE PROMOTE EVENT]` (Contract B); Contract A **upgrades the existing plot-link path** (no new event); **no reconcile event** (SD14/SD16) |
| **D7/D8** | Reconciliation / freeze safety | **moot** — no separate row; unbound submission fills first/any open slot (SD15); allocator id never renumbered; trim only never-referenced tail |
| **D9** | Gating — which `plot_type`s may mint | **`restoration`/`enrichment`/`nursery` only** — never `mature`/`research`/blank. **Applies to Contract A's create branch too** (Gary ruling #4): the link handler may mint a pseudo row only on a gated plot type; the reuse branch mints nothing |
| **D10** | Public "trees planted" counter | **NO** — pseudo-assigned QRs never count (honest state) |
| **D13** | Real tree with no bound slot | **fills the first/any open slot** — supersedes the earlier "stands alone" recommendation (SD15) |

*(v1's D7/D11/D12 — reconcile trigger, match radius, ambiguity — **CLOSED**: with in-place promotion there is **no matching step at all**.)*

---

## 9. Mapped work units (sequenced; **none started**)

| Unit | Scope | Repo | Gate |
|---|---|---|---|
| **PR0** | this doc (v2→v4) + the estimation-plan §8 addendum | `agentic_ai_context` | review |
| **PR1** | **this revision**: D1/D2/D4/D5/D6/D7/D8/D9/D10/D13 ruled; **two contracts** + UI/UX consistency; docs updated (v4→v6) | `agentic_ai_context` | **governor** |
| **PR2** | pseudo-slot **allocator** (`PS-<plot_id>-<seq>` next-free + freeze-on-reference) + make `build_tree_geojson.py` skip blank-K/L rows / carry `plot_id` — **no QR coupling**. **NB:** the allocator already merged (`sunmint` #6) but uses `PSEUDO_INFIX = "-pseudo-"` + a FIFO docstring — **must be renamed to the `PS-` prefix (D1) and de-FIFO'd** to match this v4 plan | `sunmint` | SD1/SD11 |
| **PR3** | mint pseudo rows (blank K/L, no photo, plot_id) into the target tab via `sunmint-ledger-manager` SA | `sunmint` | D2/D4 |
| **PR4** | **Contract A** — **upgrade the EXISTING plot-link handler** (`process_tree_planting_link.js` ~L936–987): find-or-create bounded by `expected_trees` (**reject past cap**; **D9 gate on the create branch**) + **status flip → `ASSIGNED_TO_PSEUDO_TREE`** (**the live-gap fix**) + keep plot-image write + tree-row reverse-binding (`Status=LINKED`/`Linked QR`/`Linked At`). **Existing columns only. No new event.** | `tokenomics` | D5/D9/D10/SD19/SD20 |
| **PR4b** | **Contract B** — **NEW `[PSEUDO TREE PROMOTE EVENT]`** (§5.2) — writes **lat/long/photo in place**; QR side-effect when bound. Register in `events_catalog.json` | `tokenomics`, `dao_protocol` | SD6/SD16 |
| **PR4c** | **Surfaces** — **Contract B only** (A adds none): DApp `promote_pseudo_tree.html` + CLI `promote_pseudo_tree.py` (§5.2.2), mirroring `link_tree_planting.*` + shared DApp scaffolding (§5.2.1) | `dapp_beta`, `dao_client`, `treasury-cache` | SD16/SD17/SD18 |
| **PR5** | permissions action (`ASSIGNED_TO_PSEUDO_TREE` gate) for **B’s** new page | `dapp_beta`, `treasury-cache` | D5 |
| **PR6** | Unbound-submission fill (§6.1) — a bulk `cepotx-survey`/farmer submission with **no** QR lands on the first/any open slot (promotion is now PR4b's event) | `tokenomics`, `dao_protocol` | SD15 |
| **PR7** | Render pseudo slots + assigned state + the **honest-state label** on the tree page, `sunmint.html`, `/sunmint/plots/`, `qr/index.html` — per render matrix **§5.1.1** | `truesight_me_beta` | SD5 |
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
