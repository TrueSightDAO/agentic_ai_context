# SunMint Boundary Media Invalidation — Design Doc (PR-B)

> **Purpose:** decide how boundary media submissions get **invalidated / retracted**
> when they are wrong, stale, or contradicted — and how that triggers a **recalculation
> of the plot polygon**. This is the correction workflow behind the "allow the ability
> to invalidate a media submission which triggers a recalculation of the plot" ask.
>
> **Status:** design lock (governor + Gary, 2026-09-01, thread 11074). No code yet —
> this is the decision record before the event + handler + UI PRs.

## 1. Why this matters

The boundary pipeline produces the plot polygon from **ground photos with embedded GPS**
(`approx` hull). A bad submission (wrong location, stray GPS, mixed-farm photos, stale
walk) produces a wrong polygon → wrong hectare count → wrong carbon-credit basis later.
Corrections must be possible, **auditable**, and **automatic where the satellite can
judge**.

## 2. What "invalidate" means

- **Soft-invalidate, never delete.** Media is evidence. On retraction the item keeps its
  row but gains `invalidated_at` + `invalidated_by` + `invalidated_reason` + `retraction_source`.
  It drops out of polygon computation but stays in the record (audit trail, disputes, DAO lineage).
- **Recalculation trigger:** dropping the invalidated item's GPS point(s) → **re-run the
  convex hull** on the remaining points → update the plot row (Coordinates, Hectares) →
  regenerate `plots/index.geojson` → impact map updates automatically. Same
  `extract_plot_gps.py` pipeline, minus the invalidated item.
- **Not a ledger event for credits** — like the boundary evidence itself, invalidation
  accumulates as plot record state; it is NOT booked to the ledger. Only a future
  CARBON CREDIT ISSUANCE EVENT books the ledger (and it reads the final, valid polygon).

## 3. The 3-tier retraction model (LOCKED)

Who can invalidate a boundary media submission:

| Tier | Actor | Scope | Mechanism |
|---|---|---|---|
| **1. Submitter / farm lead** | the farmer who submitted, or anyone tied to the submission (farm owner/lead who was part of the boundary walk) | their own submission(s) | signed `MEDIA RETRACTION EVENT` from the app |
| **2. Governor** | TrueSight DAO governor | anything, by default | same event, role check on server |
| **3. Sentinel (automated)** | the satellite-monitoring pipeline | submissions contradicted by Sentinel-2 evidence | machine-generated retraction event (no human needed) |

- **Identity basis:** the submitter's DAO email/signature (the app's existing
  "Link email" RSA keypair → Edgar). The farm record carries the submitter/lead contact;
  the handler compares retractor == submitter or listed farm contact **OR** role == governor.
  Otherwise the retraction is **rejected**.
- **Sentinel triggers** (examples):
  - Area mismatch: Sentinel-2-derived vegetated area vs the GPS-hull hectares diverges
    beyond a threshold → flag stale/overclaimed boundary.
  - Boundary drift: repeated scenes show the plot edge moved vs the recorded polygon.
  - No recovery: verified/planted plot shows no canopy development over N scenes → flag
    the submission set for review.
  - Sentinel retractions are tagged `retraction_source: sentinel` and require no human
    signature; they still record `invalidated_by: sentinel-<job>`.

## 4. Event design

New catalog event: **`MEDIA RETRACTION EVENT`** (dao_protocol events_catalog + dispatch
ROUTING row, mirroring the FBE pattern).

Canonical labels:
- `Plot ID` (required) — the plot the media belongs to
- `Media URL(s)` (required) — one or more media items to invalidate
- `Reason` (required) — free text, farmer or governor
- `Retractor Email` (required) — who is retracting (the submitter/lead or governor)
- `Retraction Source` (enum: `farmer` | `lead` | `governor` | `sentinel`)
- `Farm Name` — context
- `Extracted GPS` — echoed for audit

Dispatch: `[MEDIA RETRACTION EVENT]` → GAS webhook action
`processMediaRetractionFromTelegramChatLogs` (new .gs mirroring
`process_farm_boundary_evidence.gs`).

## 5. GAS handler shape (`processMediaRetraction.gs`)

1. Scan Telegram Chat Logs for the `[MEDIA RETRACTION EVENT]` marker (or receive via doGet webhook).
2. Dedup by Telegram Message ID (new "Media Retractions" tracking tab).
3. **Authorize** — resolve retractor email → DAO role. If not submitter/lead/governor → reject.
4. **Apply** — set `invalidated_at/by/reason/source` on each Media URL in the SunMint Plots tab
   (the plot row's media cells), keep the row.
5. **Recalculate** — drop invalidated items' GPS; re-run convex hull on the remainder.
6. **Fallback guard** — if < 3 distinct points remain, **no polygon can form**:
   - Keep the **last-good boundary** + set `boundary_state: needs_revision` + warning flag,
     OR set `boundary_state: pending` and hide the polygon until new media arrives.
   - Default: keep last-good + flag (farmer sees "boundary pending review — send new photos").
7. **Regenerate** `plots/index.geojson` (invoke rebuild workflow) → impact map reflects it.
8. **Notify** — Telegram reply to the submitter thread: "Media X invalidated — plot recalculated."

## 6. UI plan (`limites-da-fazenda/`)

- Media list (PR-A, merged) gains per-item **"Invalidar"** button when the viewer is the
  submitter/lead (email linked) or a governor.
- Click → reason modal → submit signed `MEDIA RETRACTION EVENT` → offline-queueable
  (same IndexedDB pattern) → flushes on reconnect.
- After processing: item shows greyed + "invalidado" badge; polygon + hectares update on
  the impact map; the plot status chip shows `needs_revision` when the fallback guard trips.
- Sentinel-driven invalidations show as read-only badges (no button) with the satellite
  reason line.

## 7. Sequencing (ONE PR PER TURN, after approval)

| # | Deliverable | Repo |
|---|---|---|
| PR-B1 | This design doc (lock) | agentic_ai_context |
| PR-B2 | `MEDIA RETRACTION EVENT` catalog + dispatch ROUTING row | dao_protocol |
| PR-B3 | `processMediaRetraction.gs` handler + doGet router case + SCHEDULE_TRIGGERS entry | tokenomics |
| PR-B4 | Farm app: invalidate buttons + reason modal + offline queue + badges | sunmint_beta |
| PR-B5 | `gate: UAT` — farmer retract → hull recalc → polygon updates; sentinel path unit-test | sunmint_beta / sunmint |
| post | Promote to prod **only with governor approval** | — |

## 8. Open questions (defaults set, overridable)

- **Sentinel thresholds** — area-mismatch % and scene count (defaults: >20% divergence over
  3+ scenes flags; revisit when satellite cache matures).
- **Lead definition** — "tied to the submission" = farm record's `owner` + any email that
  submitted media for that plot (recorded on the plot row). Extendable to farm contacts list.
- **Restore path** — a wrongly-retracted item can be re-activated by a governor
  (`MEDIA RETRACTION EVENT` with `source: governor`, `reason: revert`) — cheap to add, yes.

## 9. Related
- `SUNMINT_BOUNDARY_SUBMISSION_PLAN.md` — the upstream pipeline this corrects
- `SUNMINT_PLOTS_REGISTRY.md` — plots schema, boundary tiers, media rules
- `dao_protocol/.../events_catalog.json` + `dispatch.py` — FBE pattern to mirror
- `tokenomics/.../process_farm_boundary_evidence.gs` — handler pattern to mirror
- `sunmint_beta/limites-da-fazenda/index.html` — UI host (PR-A merged)
