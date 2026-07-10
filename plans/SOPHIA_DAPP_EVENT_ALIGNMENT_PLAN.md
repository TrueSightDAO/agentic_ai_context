# Sophia ↔ DApp Event Alignment — Execution Roadmap

**Status as of 2026-06-18:** DRAFT — produced after the SALES/INVENTORY-MOVEMENT
mis-route + submit_contribution incidents. Pending execution.
**Repo under change:** `truesight_autopilot` (Sophia's brain — `app/main.py`, `app/tools/`).
**Owner:** Gary Teh · **Driver:** Claude.

> ⛔ **Own-repo gate:** open PRs only, **NEVER self-merge** `truesight_autopilot` PRs.
> Every new behavior behind a flag defaulting to current behavior until soak-verified.

> **RESUME HERE:** PR1 — catalog merge: UPDATE existing events, not just add (G2).

---

## 1. Why

Two incidents (2026-06-18) exposed that Sophia mis-handles DApp event submissions:
the SALES request that turned into looping INVENTORY MOVEMENT calls, and the
`submit_contribution` crash. Root question Gary raised: **not just sales — does
Sophia correctly handle EVERY DApp event type?** This roadmap audits all event
modules and closes the systemic gaps.

## 2. The three-way map (audit result)

**DApp pages** (`dapp/`) and **`dao_client` CLI modules** (`dao_protocol/.../modules/`)
together define **~30 signed event types**. Edgar serves the authoritative
definition of all of them at **`https://edgar.truesight.me/events-catalog`** —
**verified 2026-06-18: 30 events, each with `required_fields` + `canonical_labels`.**

So the catalog is complete. **The gaps are in how Sophia consumes it:**

| # | Gap | Impact |
|---|-----|--------|
| G1 | **Catalog loads 120s AFTER boot**, then every 12h | A 2-minute post-deploy window where only the ~9 hardcoded events exist; everything else is unvalidated/unknown. |
| G2 | **Merge only ADDS required_fields for NEW events** — never UPDATES an event already hardcoded | A stale/wrong hardcoded required-field set (or canonical labels) can't be corrected by the catalog. Hardcoded = 9 of 30; the other 21 ride entirely on the catalog. |
| G3 | **Field normalization (`_FIELD_ALIASES`) is hardcoded per-event for ~4 events** | For the other ~26 event types, LLM-natural keys not in canonical labels are **silently dropped** → malformed/incomplete submissions. **This is the highest-frequency real-world gap.** |
| G4 | **No intent→event disambiguation** | "process a sale" can be mis-routed to INVENTORY MOVEMENT; correct canonical fields (e.g. SALES EVENT's `Cash proceeds collected by`, `Owner email`) may be omitted even when known. This is the class of bug from this incident. |
| G5 | **Stale hardcoded fallback** (9 of 30) | When Edgar is unreachable, 21 event types have no/wrong local definition. |

**Events Sophia hardcodes (9):** INVENTORY MOVEMENT, SALES EVENT, CONTRIBUTION
EVENT, CAPITAL INJECTION EVENT, QR CODE REGISTRATION (separate `register_qr_code`
endpoint), QR CODE EVENT, QR CODE UPDATE EVENT, TREE PLANTING EVENT, DAO Inventory
Expense Event. **Catalog has 30** (adds CURRENCY CONVERSION, ASSET RECEIPT, DAPP
PERMISSION CHANGE, NOTARIZATION, PARTNER ADD/CHECK-IN, CONTRIBUTOR ADD, REPACKAGING
BATCH, RETAIL FIELD REPORT, STORE ADD, PROGRAM/FARM REGISTRATION, DONATION MINT,
VOTING RIGHTS WITHDRAWAL, BATCH QR CODE, PROPOSAL CREATION/VOTE, EMAIL
REGISTERED/VERIFICATION, CREDENTIALING ATTESTATION/QUALIFICATION, PRACTICE,
WARMUP SEND).

**Design principle:** the catalog is the single source of truth. The fix is to
make Sophia **trust it fully, immediately, and use it for normalization + event
picking** — not to hand-maintain 30 hardcoded definitions.

## 3. Pre-flight checklist

- [x] Confirm the events-catalog is authoritative + complete (30 events, all with
      required + canonical) — **done 2026-06-18**.
- [ ] Confirm the catalog JSON schema per event (field names: `required_fields`,
      `canonical_labels`, plus any `aliases`/`category`/`dapp_page`).
- [ ] Decide: keep a hardcoded fallback at all? Proposal: **auto-generate** a
      committed snapshot from the catalog (never hand-maintained) — see PR4.
- [ ] Confirm `lookup_event_docs` already surfaces canonical labels to the LLM
      (it does) and whether "call it before submit" is enforced or advisory.
- [ ] Baseline: log which event types Sophia is actually asked to submit (freq)
      to prioritise verification.
- [ ] Own-repo gate; all behind flags defaulting to current behavior.

## 4. Sequenced plan (one PR per turn — §5a)

Each unit is **single-concern, self-contained, independently shippable**, with its
own tests + contribution, sized to ONE execution turn. Cross-PR context (the gap
analysis, catalog schema) lives in §2–§3 so no PR re-discovers it. Every brain
change ships behind a flag defaulting to current behavior. **Dependency gates:** a
PR that needs a *prior* PR's merged code is marked `gate` in §8 (don't auto-advance
onto an unmerged dependency in Sophia's own human-merged repo).

### PR1 — Catalog merge: UPDATE existing events, not just add (G2)
Change the merge in `_refresh_events_catalog` so an event already in
`_CANONICAL_LABELS` / `_VALIDATE_REQUIRED_FIELDS` has its labels **and** required
fields **updated** from the catalog (catalog wins), instead of only adding new
events. Tests: catalog with changed required/labels for an existing event → adopted;
new event → still added.

### PR2 — Catalog load timing: close the boot-window gap (G1)
Load the catalog **synchronously at startup** (or block the first
`submit_contribution` until the first load completes), with a capped fetch timeout
and snapshot fallback. Touches the startup/loop path, not PR1's merge function.
Tests: a submit during the boot window validates against the catalog; fetch
timeout → snapshot, turn still completes.

### PR3 — Auto-generated fallback snapshot (G5)
Script/CI step that fetches the catalog and writes a committed
`app/data/events_catalog_snapshot.json`; load it as the offline fallback (seeds all
~30 events, replacing the stale hardcoded 9). Standalone. Tests: Edgar unreachable
→ snapshot loads, all events known. Doc: how/when to refresh.

### PR4 — Generic catalog-driven field normalizer (G3a)
Add a normalizer that maps LLM-supplied keys to the catalog's `canonical_labels`
for **all** event types (exact + case/space/underscore-insensitive + catalog
`aliases` if present), behind `CATALOG_NORMALIZE` (default off; the old
`_FIELD_ALIASES` stays as fallback). New code path; does not change behavior until
flagged on. Tests: ≥5 event types incl. ones with no old alias map normalize.

### PR5 — Stop silently dropping non-canonical keys (G3b) — needs PR4
When a supplied key can't be mapped to a canonical label, **surface it** (warn +
pass through / attach), never drop blind. Builds on PR4's normalizer. Tests: an
unmappable key is preserved/flagged, not lost.

### PR6 — Intent→event picking guidance (G4a)
Strengthen `lookup_event_docs` output + the system-prompt so the LLM reliably
picks the right event for an intent and fills important canonical fields (sale →
SALES EVENT incl. `Cash proceeds collected by` + `Owner email`; custody transfer →
INVENTORY MOVEMENT; never conflate). Standalone (lookup/prompt only). Tests:
"sales" intent → SALES EVENT with cash-proceeds; "transfer" → INVENTORY MOVEMENT.

### PR7 — Enforce lookup-before-submit (G4b) — needs PR6
`submit_contribution` requires a prior in-session `lookup_event_docs` for the
event type, else it injects the catalog spec inline before validating. Builds on
PR6. Tests: submit without prior lookup → spec injected/guided; with lookup → proceeds.

### PR8 — (rollout, not a PR) deploy + UAT — see §6.

## 5. Per-event verification checklist (UAT matrix)

For each high-frequency event, submit on **beta** and confirm the right fields
land (tick as verified). Group by priority:

- **Tier 1 (frequent):** ☐ CONTRIBUTION ☐ SALES ☐ INVENTORY MOVEMENT
  ☐ ASSET RECEIPT ☐ CAPITAL INJECTION ☐ CURRENCY CONVERSION
- **Tier 2:** ☐ PARTNER CHECK-IN ☐ STORE ADD ☐ RETAIL FIELD REPORT
  ☐ CONTRIBUTOR ADD ☐ PARTNER ADD ☐ NOTARIZATION ☐ TREE PLANTING ☐ DONATION MINT
- **Tier 3 (rare / specialised):** ☐ DAPP PERMISSION CHANGE ☐ REPACKAGING BATCH
  ☐ PROGRAM/FARM REGISTRATION ☐ VOTING RIGHTS WITHDRAWAL ☐ BATCH QR CODE
  ☐ QR CODE / QR CODE UPDATE ☐ PROPOSAL CREATION/VOTE ☐ CREDENTIALING ×2
  ☐ PRACTICE ☐ WARMUP SEND ☐ EMAIL REGISTERED/VERIFICATION

## 6. UAT (operator-runnable on beta)
| # | Scenario | Expected |
|---|----------|----------|
| U1 | Ask Sophia to record a **sale** (sold-by X, cash-collected-by Y) | Emits **SALES EVENT** with `Sold by`, `Cash proceeds collected by`, `Owner email` populated — NOT inventory movement |
| U2 | Ask for an event type **not** in the old hardcoded 9 (e.g. ASSET RECEIPT, CURRENCY CONVERSION) | Correct event, correct required fields, no dropped keys |
| U3 | Submit within 2 min of a deploy | Validated against the catalog (no boot-window gap) |
| U4 | Edgar catalog unreachable | Falls back to the snapshot; still validates |
| U5 | LLM uses natural field names | Normalized to canonical; nothing silently dropped |

**Completion gate:** PRs human-merged; U1–U5 pass; Tier-1 events verified on beta.

## 7. Risks
- Catalog schema drift → PR1 must be defensive (missing keys → keep snapshot).
- Over-eager normalization mapping a key to the wrong canonical label → keep it
  conservative (exact/alias match only; never fuzzy-guess).
- Sync catalog load slows boot → cap the fetch timeout, fall back to snapshot.

## 8. Resume tracker
| Unit | Advance | PR opened | Merged (human) | Deployed | UAT | Contribution |
|------|---------|-----------|----------------|----------|-----|--------------|
| PR1 — catalog merge UPDATE (G2) | `auto` | ☐ | ☐ | ☐ | — | ☐ |
| PR2 — catalog load timing (G1) | `auto` | ☐ | ☐ | ☐ | — | ☐ |
| PR3 — fallback snapshot (G5) | `auto` | ☐ | ☐ | ☐ | U4 | ☐ |
| PR4 — generic normalizer, flagged (G3a) | `auto` | ☐ | ☐ | ☐ | — | ☐ |
| PR5 — stop dropping keys (G3b) | `gate: needs PR4 merged first` | ☐ | ☐ | ☐ | U5 | ☐ |
| PR6 — intent→event picking (G4a) | `gate: review picking logic` | ☐ | ☐ | ☐ | U1 | ☐ |
| PR7 — enforce lookup-before-submit (G4b) | `gate: needs PR6 merged first` | ☐ | ☐ | ☐ | — | ☐ |
| PR8 — rollout + UAT | `gate: UAT` | ☐ | ☐ | ☐ | U1–U5 | ☐ |

**Dependency notes:** PR1–PR4 + PR6 are independent (open off `main`). PR5 needs PR4's
normalizer merged; PR7 needs PR6's picking guidance merged — hence their `gate` markers
(don't auto-advance onto an unmerged dependency in a human-merged repo).

> **RESUME HERE:** PR1 — catalog merge UPDATE: change `_refresh_events_catalog` so an
> event already in `_CANONICAL_LABELS` / `_VALIDATE_REQUIRED_FIELDS` gets its
> required_fields + canonical_labels UPDATED from the catalog (catalog wins), not just
> new events added. Open a PR; do not self-merge.

## 9. Notes
- The catalog being complete means this is mostly a **consumption-correctness**
  effort, not a 30-event hand-coding effort — keep that framing.
- Pairs with the doc fix (agentic#552, dao_protocol#122) that corrected the
  INVENTORY MOVEMENT "depletion" wording (it transfers custody person-to-person;
  it does not deplete an asset location).
- `Advance` markers per §5c (auto-advance) — see OPERATING_INSTRUCTIONS §5c.
