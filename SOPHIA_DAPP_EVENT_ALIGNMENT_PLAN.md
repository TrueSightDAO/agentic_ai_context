# Sophia ↔ DApp Event Alignment — Execution Roadmap

**Status as of 2026-06-18:** DRAFT — produced after the SALES/INVENTORY-MOVEMENT
mis-route + submit_contribution incidents. Pending execution.
**Repo under change:** `truesight_autopilot` (Sophia's brain — `app/main.py`, `app/tools/`).
**Owner:** Gary Teh · **Driver:** Claude.

> ⛔ **Own-repo gate:** open PRs only, **NEVER self-merge** `truesight_autopilot` PRs.
> Every new behavior behind a flag defaulting to current behavior until soak-verified.

> **RESUME HERE:** PR1 — catalog-merge correctness (sync load + update-not-just-add).

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

### PR1 — Catalog-merge correctness *(highest leverage)*
- Load the events-catalog **synchronously at startup** (or block first
  `submit_contribution` until first load) — close the 120s window (G1).
- Change the merge to **UPDATE** `canonical_labels` **and** `required_fields` for
  events already present, not just add new ones (G2). Catalog wins over the
  stale hardcoded snapshot.
- Tests: stub catalog with changed required fields → Sophia adopts them; Edgar
  down → falls back to snapshot; boot-window submit waits for/uses the catalog.

### PR2 — Catalog-driven field normalization *(highest-frequency gap)*
- Replace the per-event `_FIELD_ALIASES` with a **generic normalizer** that maps
  LLM-supplied keys to the catalog's `canonical_labels` for **all** events
  (case/space/underscore-insensitive; use catalog `aliases` if present) (G3).
- **Stop silently dropping** non-canonical keys for events with no hardcoded alias
  map — either map via the catalog or surface them, never drop blind.
- Tests: for ≥5 event types incl. ones with no old alias map, LLM-natural keys
  normalize correctly and nothing is dropped.

### PR3 — Intent→event disambiguation + completeness *(this incident's class)*
- Strengthen `lookup_event_docs` / the submit flow so the LLM reliably picks the
  right event for an intent and fills important canonical fields (G4): e.g.
  "sale" → SALES EVENT incl. `Cash proceeds collected by` + `Owner email`;
  "move/transfer custody" → INVENTORY MOVEMENT; never conflate.
- Consider gating: `submit_contribution` requires a prior `lookup_event_docs`
  for the event type in-session, else it injects the catalog spec inline.
- Tests: a "sales" intent yields SALES EVENT with the cash-proceeds field; an
  inventory-movement intent stays INVENTORY MOVEMENT.

### PR4 — Auto-generated fallback snapshot *(kills staleness)*
- A small script/CI step that writes a committed snapshot of the catalog
  (`app/data/events_catalog_snapshot.json`) used as the offline fallback, so the
  fallback is regenerated from Edgar, never hand-maintained (G5). Document refresh.
- Tests: snapshot loads as fallback when Edgar is unreachable.

### PR5 — (rollout) deploy + UAT — see §6.

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
| PR1 — catalog-merge correctness | `auto` | ☐ | ☐ | ☐ | — | ☐ |
| PR2 — catalog-driven normalization | `auto` | ☐ | ☐ | ☐ | — | ☐ |
| PR3 — intent→event disambiguation | `gate: review picking logic before next` | ☐ | ☐ | ☐ | U1 | ☐ |
| PR4 — auto-generated fallback snapshot | `auto` | ☐ | ☐ | ☐ | U4 | ☐ |
| PR5 — rollout + UAT | `gate: UAT` | ☐ | ☐ | ☐ | U1–U5 | ☐ |

> **RESUME HERE:** PR1 — make the events-catalog fully authoritative: load it
> synchronously at boot (close the 120s window) and have the merge UPDATE (not
> just add) required_fields + canonical_labels for existing events. Open a PR;
> do not self-merge.

## 9. Notes
- The catalog being complete means this is mostly a **consumption-correctness**
  effort, not a 30-event hand-coding effort — keep that framing.
- Pairs with the doc fix (agentic#552, dao_protocol#122) that corrected the
  INVENTORY MOVEMENT "depletion" wording (it transfers custody person-to-person;
  it does not deplete an asset location).
- `Advance` markers per §5c (auto-advance) — see OPERATING_INSTRUCTIONS §5c.
