# TrueSight Ledger Explorer — public "blockchain explorer" for the DAO's signed-event ledger

> **Origin:** governor request, thread 37982 (2026-09-28), via Envoy: *"Based on what you know
> so far about the structure of the JSON, come up with a plan for the blockchain explorer and
> figure out how to expose it on our site TrueSight."*

## 0. What already exists (no new ledger needed)

`TrueSightDAO/verify_public_signatures` **is** the ledger. Per its own README: *"Every
RSA-signed event submitted to the DAO ... is published here as one immutable JSON file per
event ... Anyone ... can independently re-verify any attestation offline using only the
standard `openssl` tool. No trusted intermediary required."* That is a blockchain explorer's
subject matter already sitting in public GitHub, machine-generated, append-only, git-history
audited. This plan is a **read surface** over it — no new ledger, no new signing scheme.

## 1. Data contract (verified live, 2026-09-28)

```
verify_public_signatures/
├── index.json                        # root: totals + per-type pointers + txid-mirror stats
├── <event_type>/                     # 34 folders today (contribution_event, tree_planting, …)
│   ├── index.json                    # id -> {url, event_type, submitted_at, contributor_name}
│   ├── <message_id>.json             # PRIMARY event file, e.g. Edgar_20260924125541_071.json
│   └── <sha256(txid)>.json           # CANONICAL MIRROR, same content, txid-addressable
```

- **Root `index.json`** fields (live sample): `total_count` (4,512), `test_events_count`,
  `excluded_pii_count`, per-`event_types{}` `{count, index_url}`, plus ledger-health counters
  `total_txid_count` / `txid_mirror_count` / `txid_dup_groups` / `txid_mirror_collisions`
  (4,433 / 4,433 / 43 / 0 as of this check — the txid-mirror work from earlier this session).
- **Per-type `index.json`**: `events` is a **dict keyed by message_id**, each entry
  `{url, event_type, submitted_at, contributor_name}` — a manifest, not the full record.
- **Individual event file**: the full record — `event_type`, `telegram_message_id`,
  `submitted_at`, `contributor_name`, `public_key` (RSA, PEM body), `signature`,
  `signed_payload` / `signed_text` (human-readable event text), `request_transaction_id`
  (= the signature itself — **this is the "txid"**), `verifiable`, `linked_tree_id`.
- **Two addressing schemes coexist per file** — message_id-named (what the per-type
  `index.json` links to today) and `sha256(request_transaction_id)`-named (the canonical
  mirror). **Correction 2026-09-29 (was wrongly stated as "identical content"):** the two
  files are **near-identical but NOT identical** — the mirror body adds the field
  `request_transaction_id` (`= signature`), the primary message-id record carries only
  `signature`. 8/8 tree_planting events sampled confirmed this. That asymmetry is the
  **generator gap** in §2.3 (the mirror is self-describing; the primary record is not).
  The per-type `index.json` does **not yet** list the mirror filenames — see Gap 3 below.

## 2. Gaps to close before an explorer can be built well (real, verified — not assumed)

1. **No global txid → location index.** Given a txid, there is no single file to fetch that
   says "it's in `tree_planting`, file `<hash>.json`" — a client has to either already know
   the event type, or fan out across all 34 per-type folders. A search-by-txid box needs this.
2. **No global chronological feed.** Each per-type `index.json` is internally unordered
   (insertion-order dict) and there is no root-level "latest N events across all types" view —
   the thing a landing page ("recent activity") needs. (Note: a **different** repo,
   `lineage-assets`, gained an `events_ordered` + `submitted_at` sort key this session via PR
   #520 — same idea, different ledger. Reuse that convention here, don't reinvent it.)
3. **Per-type index doesn't carry the canonical (txid-mirror) URL**, only the message_id one.
   An explorer that wants to *cite* an event durably should link the txid-hash file (the
   README's stated purpose of the mirror), not the message_id file.
   ✅ **CLOSED 2026-09-29 (PR7).** The explorer reads the GLOBAL `ledger_index.json` (PR1),
   which already carries `canonical_url` on every row — verified: `canonical_url` present in
   **all 4,440** rows. So no per-type-index change was needed; the fix was purely the
   explorer's *display* (cite the canonical URL only). ⚠️ **Residual generator gap (filed,
   NOT yet fixed):** `sync_sunmint_signatures.py:683` adds `request_transaction_id` to the
   **mirror** only, so the primary message-id record is not self-describing. Filed in
   `OPEN_FOLLOWUPS.md` for a one-line generator fix (either URL should be independently
   citable).

None of these require changing how events are signed or published — they're additive
generated-index work, same shape as the mirror work already shipped this session.

## 3. Scope

### In scope
1. **Global reverse index** (`ledger_index.json` at repo root) — flat list, one row per
   event, carrying `txid_hash` (the mirror filename), `event_type`, `submitted_at`,
   `contributor_name`, `canonical_url`, `message_id_url`. Sorted by `submitted_at` desc
   (reuse the `events_ordered` convention from `lineage-assets` PR #520). This is the single
   fetch an explorer needs for "search by txid" (client-side lookup in one JSON) and
   "recent activity" (already sorted).
2. **Explorer UI** — a new static page: search box (txid or message_id) → event detail view
   with the human-readable `signed_payload`, contributor, date, and a "Verify with openssl"
   snippet (README already documents the offline-verify command — surface it, don't
   reinvent it); a "recent activity" feed; browse-by-type; browse-by-contributor.
3. **Cross-links** — an event detail view for a `tree_planting`/`asset_receipt_event`
   should link out to the just-shipped **My Trees** module (`sunmint_beta`/`cfr-anapu`,
   PR #87, merged this session) when `linked_tree_id` is present — the explorer becomes the
   "show me the receipt" complement to My Trees' "show me my trees."
4. **Nav exposure** — ✅ **rescoped 2026-09-29.** The explorer already lives at
   `truesight_me_beta/ledger/explorer/` and is **already linked** in that site's shared
   dropdown (`js/nav.js` → "Ledger Explorer"). That is the **canonical** explorer. The
   original "add it to cfr + sunmint + dapp navs" was per-site duplication with no user need
   on the two farmer-facing sites, and is **dropped** (§5 PR5). Prod exposure
   (`truesight.me` still lacks `/ledger/explorer/` + the nav link) is a governed promotion,
   held for explicit governor approval.

### Out of scope (this plan)
- Any change to how events are signed, verified, or published (`sync_sunmint_signatures.py`
  stays as-is beyond the additive index generator).
- A write/submit surface — this is read-only, public, no auth.
- Redesigning the per-type `index.json` schema consumed by existing tooling — the new
  `ledger_index.json` is additive, nothing existing is renamed or removed.

## 4. Architecture decision

**Static, serverless, client-side-fetch** — same doctrine already established this session
for the payout/recipient work (*"the dapp should read from public GitHub JSON caches ...
NOT key-gated GAS endpoints"*, `sync_pending_caches.py` docstring). The explorer fetches
`ledger_index.json` + individual event files directly from `raw.githubusercontent.com` /
GitHub Pages; no backend, no auth, no rate-limit-shared GAS project. This also sidesteps the
GAS-concurrency-queueing class of bug just fixed in the payout page (#133/#134) — there is no
GAS in this design at all.

**Where it lives:** a new page, not a new repo — `dapp_beta` already hosts the DApp's public
utility pages (`report_payout_event.html`, `verify_request.html`, etc.) and already has the
shared `routes.js` / `menu.js` / CDN conventions to reuse. Proposed path:
`dapp_beta/ledger_explorer.html` (beta: `beta.dapp.truesight.me/ledger_explorer.html`).

> **2026-09-29 correction (governor rescope).** The explorer had **already been built
> independently at `truesight_me_beta/ledger/explorer/`** (with `js/ledger_explorer_utils.js`
> + tests) and is **already linked** in that site's shared dropdown. That landing-site page is
> the **canonical** explorer. The `dapp_beta/ledger_explorer.html` built under PR2–4 became a
> **duplicate** and is **retired**; `dapp_beta#141` (which would have nav-linked it) is
> **closed unused**, and the duplicate files themselves were **deleted 2026-09-29
> (`dapp_beta#142`)** — renderer + utils + test, un-wired from `package.json`. PR6 UAT ran
> against the canonical page (**PASSED 2026-09-29**); prod promotion is held for governor
> approval.

## 5. Roadmap (ONE PR PER TURN, §5a)

| # | Deliverable | Repo | Depends on |
|---|---|---|---|
| **PR0** | This roadmap + handoff-manifest row | agentic_ai_context | — |
| **PR1** | `ledger_index.json` generator (global reverse index: txid_hash → type/url, `submitted_at`-sorted `events_ordered`, reuses the mirror machinery from `sync_sunmint_signatures.py`) + wire into the existing sync cron; freshness stamp (`generated_at`) | truesight_autopilot | PR0 |
| **PR2** | Explorer shell — `dapp_beta/ledger_explorer.html`: search box (txid or message_id) → event detail card, sourced from `ledger_index.json` + the individual event file; "verify with openssl" snippet from the README | dapp_beta | PR1 |
| **PR3** | Recent-activity feed (uses `events_ordered`, already sorted — no new sort logic) + browse-by-type + browse-by-contributor filters | dapp_beta | PR2 |
| **PR4** | Cross-link: event detail view links out to the My Trees module when `linked_tree_id` is present (and vice versa — My Trees links back to the ledger event for a tree's payout/receipt) | dapp_beta (+ small `sunmint_beta`/`cfr-anapu` link-out addition) | PR3 |
| ~~**PR5**~~ | ~~Nav exposure on cfr/sunmint/dapp~~ — **DROPPED 2026-09-29**: the canonical explorer `truesight_me_beta/ledger/explorer/` is already nav-linked; the `dapp_beta` duplicate is retired; `dapp_beta#141` closed unused | — | n/a |
| **PR6** | `gate: UAT` — ✅ **PASSED 2026-09-29** on the canonical explorer (`beta.truesight.me/ledger/explorer/`): page 200, totals `ledger_index.count` 4,440 == root `total_txid_count`, txid→event file 200, static client-side source, **0 GAS hits**, nav link present | truesight_me_beta | PR4 |
| **PR7** | **Cite the canonical ledger URL, not the message-id URL** (closes §2.3; the ⚠️ asymmetry above). New `canonicalLedgerUrl(row)` helper; card shows only the `sha256(txid)` mirror URL. Also in this unit (governor-approved 2026-09-29): **SunMint PWA SW update self-heal** (`sunmint_beta`) + **retire the `dapp_beta` explorer duplicate**. | truesight_me_beta + sunmint_beta + dapp_beta | PR6 |
| **PR8** | **Cross-link tree-planting events to the SunMint PROGRAM** (Gary 2026-09-29: "Sunmint link only on trees planting events. and make sure to link to the specific tree"). New `buildSunmintTreeLink(ev)` (+ `isTreePlantingEvent`, `sunmintTreeQuery`, `SUNMINT_PROGRAM_URL`); the event card renders a **Program** block deep-linked to the specific tree via `sunmint.html?tree=<tree_id>`. Join key VERIFIED: registry `sunmint/trees/index.geojson` `tree_id` == the planting event's `telegram_message_id`. Non-planting events render no block. | truesight_me_beta | PR7 |
| *(post-UAT)* | **PROD PROMOTION EXECUTED 2026-09-29** on explicit governor command (`sync_beta_to_prod(truesight_me_prod)` → merge `61bd0f0`, deploy record `deploy_20260929T023925Z`). Verified live: `truesight.me/ledger/explorer/` **200**, prod `js/nav.js` carries the Ledger Explorer entry, CNAME preserved (`truesight.me`). ⚠️ **PR8 (SunMint cross-link) is NOT in prod** — it merged (`10c2380`) *after* this sync, so it rides the next governed carry (see PR8 row). | — | UAT pass |

## 6. Constraints (rules — same as every plan this cycle)

- **Beta-first**, UAT gate before calling it done.
- **ONE PR PER TURN** — execute one PR, report, stop.
- **Local test suite** before pushing; static HTML/JS — verify tags balanced + `node --check`
  on extracted JS.
- **No GAS dependency** in the explorer — client-side fetch of public JSON only (§4).
- **Don't create variant plan/backlog files.**
- **Independent re-verification, not self-report** — per this session's established pattern
  (Envoy verifies every merged PR live with its own signed-in/cold-load test before telling
  the governor it's ready to UAT), each PR here should get the same treatment: e.g. PR1's
  freshness stamp checked against a live fetch, PR2's search box checked against a real txid
  a fresh browser context, not just the local test suite passing.

## 7. Checklist

### PR1 — global reverse index
- [ ] Read `sync_sunmint_signatures.py`'s existing mirror logic (sha256(txid) naming, the
      lock file, the re-GET-and-retry-on-409 pattern) — reuse, don't reimplement
- [ ] Generate `ledger_index.json` at repo root: `events_ordered` (submitted_at desc) +
      `events` dict keyed by `txid_hash` → `{event_type, submitted_at, contributor_name,
      canonical_url, message_id_url}`
- [ ] `generated_at` freshness stamp
- [ ] Wire into the existing cron run (additive step, same push)
- [ ] Verify live: fetch the published file, confirm count matches root `index.json`'s
      `total_txid_count`
- [ ] Open PR, report URL

### PR2 — explorer shell
- [ ] `dapp_beta/ledger_explorer.html`: search box, event detail card
- [ ] "Verify with openssl" snippet (copy the README's documented command, don't invent one)
- [ ] Open PR, report URL

### PR3 — recent activity + browse
- [ ] Recent-activity feed from `events_ordered`
- [ ] Browse-by-type, browse-by-contributor
- [ ] Open PR, report URL

### PR4 — cross-links to My Trees
- [ ] Ledger event detail → My Trees link when `linked_tree_id` present
- [ ] My Trees tree card → ledger event link for its payout/receipt event
- [ ] Open PR, report URL

### PR5 — nav exposure — ~~DROPPED~~ (2026-09-29)
- ~~Dropdown entry on `cfr.truesight.me`, `sunmint.truesight.me`, `dapp.truesight.me`~~
- Superseded: the canonical explorer `truesight_me_beta/ledger/explorer/` is already linked in
  its own nav (`js/nav.js`); the `dapp_beta` duplicate is retired; `dapp_beta#141` is closed.
  No PR5 PR needed.

### PR6 — UAT gate ✅ PASSED 2026-09-29 (on `beta.truesight.me/ledger/explorer/`)
- [x] Search resolves a real txid → correct event (index row → event file 200, cold-context checked)
- [x] Search by message_id works (index lookup by `telegram_message_id`)
- [x] Recent-activity feed matches root `index.json` totals (`ledger_index.count` 4,440 == `total_txid_count` 4,440)
- [x] My Trees cross-links resolve (fixed same day — `cfr-anapu#20` re-vendor; link keys on `request_transaction_id`/`?tx=`)
- [x] Nav entry present on the canonical host (`beta.truesight.me/js/nav.js` → Ledger Explorer)
- [x] No GAS calls — static client-side fetch of `raw.githubusercontent.com` (0 Apps-Script refs)

### PR7 — cite the canonical URL + PWA self-heal + retire the duplicate ✅ 2026-09-29
- [x] `canonicalLedgerUrl(row)` helper (mirror preferred, message-id only as last-resort fallback)
- [x] Card cites the `sha256(txid)` URL only; the "Ledger URL (message id)" row removed
- [x] `sunmint_beta`: `CACHE_NAME` v11→v12 + `SKIP_WAITING` hook + shared `sw-update.js` "reload to update" banner on all 4 pages
- [x] Retire `dapp_beta/ledger_explorer.html` + `_utils.js` + its test (un-wire from `package.json`)
- [x] ⚠️ Residual: file the `sync_sunmint_signatures.py:683` generator gap in `OPEN_FOLLOWUPS.md`
- [x] Verified live: beta explorer cites canonical only; sunmint SW v12 + `sw-update.js` served; dapp dup → 404

### PR8 — SunMint program cross-link (tree-planting only, deep-linked to the tree) ✅ 2026-09-29
- [x] `isTreePlantingEvent()` — true only for `[TREE PLANTING EVENT]` / `tree_planting`, NOT the link/reject variants
- [x] `sunmintTreeQuery()` — `telegram_message_id` → `?tree=` (verified key), fallback `linked_tree_id` → `?qr=`, else `null`
- [x] `buildSunmintTreeLink(ev)` — `''` when unresolved, so the card skips the block
- [x] Event card renders a **Program** block ("View this tree on SunMint →") beside **Linked tree**
- [x] 8 new unit tests incl. the live-verified Gary-cited event round-trip
- [x] Verified: 56/56 node tests; `node --check` clean; merged truesight_me_beta#409
- [x] Verified live: repo `main` carries the helper + card wiring; `sunmint.html?tree=Edgar_20260821175134_006` → 200 and the page has the `?tree=`/`?qr=` restore logic

## 8. Do / Don't
- **Do** reuse the existing mirror/lock/retry machinery from `sync_sunmint_signatures.py`.
- **Do** keep this entirely client-side static — no backend, no GAS.
- **Do** independently re-verify each PR live (this session's established discipline), not
  just trust the test suite or a self-report.
- **Don't** change the signing/verification scheme or the existing per-type `index.json`
  consumers.
- **Don't** create variant plan/backlog files.

## 9. Related
- `TrueSightDAO/verify_public_signatures` README — the ledger's own documentation, the
  source of truth for the data contract in §1.
- This session's txid-mirror work (truesight_autopilot PR #517–519) — the mirror scheme
  this plan's index generator (PR1) builds on.
- This session's `lineage-assets` PR #30/#520 — the `recipient_pk_hash` cache-first pattern
  and the `events_ordered` chronological-index convention, both directly reused here (§4, §5).
- `plans/SUNMINT_PLOT_EXPLORER_PLAN.md` — a differently-scoped "explorer" (physical
  plots/trees/media, not ledger events); no overlap, but the same "explorer" framing/format.
