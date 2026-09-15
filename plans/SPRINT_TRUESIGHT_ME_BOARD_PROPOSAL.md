# `sprint.truesight.me` — a public Kanban board over Sophia's handoff pipeline

**Filed:** 2026-09-15, by Claude Anthropic (Envoy), at Gary's request, converged over a multi-turn
design conversation this session. **Status: proposal, ready for review** — every open fork raised
during the conversation is resolved below (§0); nothing is executed yet.

**The actual problem this solves, in Gary's words:** *"Right now I don't know what actually needs my
attention when I go into Telegram or Discord."* Every design choice below is in service of that one
sentence — a supervisor thread that's `executing` normally and a thread that's genuinely
`blocked_on_human` look identical in a chat client until you open each one and read it. The board's
entire value is collapsing that distinction into something scannable in one glance, without opening a
single topic. §2.3's "needs you" treatment is not a nice-to-have section of the board — it is the
board's primary reason to exist; everything else (spec links, deep links, priority signals) is
secondary context once Gary already knows which tickets deserve a look.

---

## 0. What this is, stated plainly (design decisions as they were made)

Gary, over several turns today:

1. Wondered whether syncing tasks to an external tool (Trello/Jira/Pipedrive/Pivotal Tracker) would
   help him track and monitor what Sophia's working on.
2. Refined this to: **a Kanban board hosted on `truesight.me` itself**, not a third-party tool.
3. Refined the location to: **its own subdomain**, e.g. `sprint.truesight.me` — not
   `sophia.truesight.me` (keeps it separate from the autopilot's own operational surface).
4. Specified **auth like `capoeira`/Butterfly Effect/SunMint** — the DAO's standard client-side RSA
   keypair pattern, not a governor-only login.
5. Specified that an authenticated visitor should be able to, beyond viewing, **"sign a ticket for
   prioritizing."**
6. On the authority question this raises (does a signed vote *drive* the supervisor's queue, or just
   *inform* it): **"Contributor sign off is just advisory. Envoy should have autonomy on what to
   prioritize based on the context envoy has."** — resolved: advisory only.
7. Wants **one place to see the implementation spec and click through to the live conversation**
   (Telegram or Discord) where a ticket's work is actually happening.
8. Wants **distinct columns showing where each ticket currently is**, so a glance answers "what needs
   my attention and why" — not a flat list.
9. Flagged that `truesight.me` already links out to a **dead, unused Trello board**
   (`quests/index.html`, `quests/join/index.html`) and wants that link **repointed to this board once
   it ships** — not before, and not blocking this proposal.

Every one of these is treated as **resolved design input** below, not re-opened for debate — this doc
exists to turn a converged conversation into a buildable, corrigible plan (§5e of
`OPERATING_INSTRUCTIONS.md`: batch the decisions once).

---

## 1. Current-state architecture audit (read directly, 2026-09-15)

### 1.1 The data already exists — this is a rendering problem, not a data-modeling problem

`handoffs/HANDOFF_MANIFEST.md` is already the single source of truth for every active handoff: plan
file, status, Telegram topic + `message_thread_id`, resume-tracker narrative, last-update date. It is
**already public** — `agentic_ai_context` is a public GitHub repo (confirmed via `gh api
repos/TrueSightDAO/agentic_ai_context --jq .private` → `false`), so a static site can fetch it
directly with zero new credentials.

`sophia/SUPERVISOR_LOOP.md` §2 already defines the exact state machine a Kanban board's columns
should be:

```
awaiting_kickoff → executing → paused_at_gate → sophia_uat → envoy_uat → human_uat_ready
  → prod_merge → done
(failed, blocked_on_human, stale — off the happy path, always visible)
```

This is not a new taxonomy to invent — Gary's "distinct columns... what needs my attention and why"
(§0 point 8) is answered by rendering *this* enum as columns, with `blocked_on_human` and
`human_uat_ready` visually distinguished as "needs you" (§2.3 below), since those two states are
*already*, by definition, the only ones requiring Gary specifically.

**The one real gap:** `handoffs/index.json` — the *machine-readable* mirror of the manifest — was
already identified as missing in `SUPERVISOR_LOOP.md` §8 ("Enabling work — not yet shipped"), months
before this conversation, for exactly this reason: no consumer (a supervisor LLM, or now this board)
should have to regex-parse a giant Markdown table to get structured state. Shipping it is Phase 1 of
this proposal's roadmap, not a new idea.

### 1.2 The DAO-standard signing pattern — already used by SunMint, reusable unmodified

`sunmint_beta/index.html` (read directly, 2026-09-15):

```js
// line 447
const EDGAR_SUBMIT_URL = `${EDGAR_BASE}/dao/submit_contribution`;

// lines 465-479 — client-side keypair, generated on first use, persisted locally
let publicKey = localStorage.getItem('publicKey');
let privateKey = localStorage.getItem('privateKey');
// ... generateKeyPair() if absent ...
localStorage.setItem('publicKey', publicKey);
localStorage.setItem('privateKey', privateKey);

// line 483
async function signText(privateKeyBase64, text) { /* RSASSA-PKCS1-v1_5 / SHA-256 */ }

// line 553 — optional portability, not required to sign
localStorage.getItem('sunmint_linked_email')
```

This is **exactly** "auth like SunMint" (§0 point 4): no login screen, no password, no OAuth. A
visitor's browser silently holds a keypair; the *first* time they sign something, that keypair becomes
their durable (locally-persisted) identity, optionally linked to an email for cross-device
portability. `sprint.truesight.me` reuses this verbatim — **zero new auth infrastructure.**

### 1.3 The event catalog — where "sign a ticket to prioritize" actually plugs in

`dao_protocol/truesight_dao_client/server/data/events_catalog.json` (72 entries, read directly) is the
canonical, single-source-of-truth registry Edgar serves at `GET /events-catalog`. Each entry:

```json
"CONTRIBUTION EVENT": {
  "category": "Contribution & Finance",
  "description": "...",
  "canonical_labels": ["Type", "Amount", "Description", "Contributor(s)", "TDG Issued"],
  "required_fields": ["Type", "Amount"],
  "dapp_page": "report_contribution.html"
}
```

"Sign a ticket to prioritize" (§0 point 5) is a **new entry in this same catalog** —
`HANDOFF PRIORITY SIGNAL EVENT` — not a new subsystem. A signer POSTs a signed event body to the same
`/dao/submit_contribution` endpoint every other DAO page already uses; it lands in the public ledger
and (per the existing convention used for every other event type) `verify_public_signatures` picks it
up on its normal sync cadence, giving the board a public, auditable read source with no bespoke
backend.

### 1.4 The dead Trello link (§0 point 9) — exact location, confirmed live

`truesight_me_prod/quests/index.html` and `truesight_me_prod/quests/join/index.html` (also present,
presumably identically, in `truesight_me_beta`) are meta-refresh redirect stubs:

```html
<!-- quests/index.html -->
<meta http-equiv="refresh" content="0; url=https://trello.com/b/8VG6IfzF/truesight-dao" />

<!-- quests/join/index.html -->
<meta http-equiv="refresh" content="0; url=https://trello.com/invite/b/6835f79b6e99af69da284fd7/ATTIe8d570ecf44a8ab60adb3dce899a94ab85082E7D/truesight-dao" />
```

`truesight.me/quests/` is a live, indexed URL path pointing at a Trello board that (per Gary) is dead
and unused. Repointing it is the **last** unit of this roadmap (§7 PR8), gated on the new board being
live and UAT-passed — not before.

---

## 2. Target architecture

### 2.1 Hosting — a new static subdomain, same pattern as `cfr-anapu`

New repo `TrueSightDAO/sprint` (or similar), GitHub Pages (`gh-pages` branch — the token-scope
workaround already proven twice this session's prior work), Route53 CNAME `sprint.truesight.me`. Pure
static site: fetches public JSON (§1.1, §1.3), renders client-side, POSTs signed events directly to
Edgar (§1.2) — **no backend of its own**, same shape as `sunmint_beta`/`capoeira`/`cfr-anapu`.

### 2.2 Data sources (all already public, all already read this session)

| Data | Source | New? |
|---|---|---|
| Ticket list + state + spec link + Telegram thread | `agentic_ai_context/handoffs/index.json` | **Needs to ship** (§1.1 gap) — not new design |
| Discord channel/thread id (for click-through, §0 point 7) | Same `index.json`, extended | **New field** — already anticipated in `SUPERVISOR_LOOP.md` §8's own spec: "both Telegram thread_id **and** Discord channel/thread id" |
| Implementation spec content | The plan file `index.json` points at, fetched raw (jsDelivr-primary/raw-fallback, same pattern as `program-shell.js`) | No — reuse existing fetch pattern |
| Priority signals | `verify_public_signatures`'s `handoff_priority_signal_event/` bucket (new bucket, same repo, same sync mechanism as every other event type) | New bucket, existing mechanism |

### 2.3 Board layout — columns are the existing state enum, not a new one

Per Gary's clarification mid-build (§0 point 8), the board is a literal Kanban, not a flat table.
Columns map directly onto `SUPERVISOR_LOOP.md` §2's state enum:

```
┌──────────────┬───────────┬────────────────┬─────────────┬──────────────┐
│ Awaiting     │ Executing │ Paused at gate │ UAT         │ NEEDS YOU    │
│ kickoff      │           │                │ (R1/R2)     │ ← highlighted│
├──────────────┼───────────┼────────────────┼─────────────┼──────────────┤
│              │           │                │             │ blocked_on_  │
│              │           │                │             │ human        │
│              │           │                │             │ human_uat_   │
│              │           │                │             │ ready        │
└──────────────┴───────────┴────────────────┴─────────────┴──────────────┘
          Done / superseded / stale — collapsed footer, not a column
```

Each card: ticket title, plan-file link (renders the spec inline on click, §2.2), Telegram/Discord
deep link, current resume-tracker one-liner (already in the manifest — "why" per §0 point 8), and — if
any exist — its priority-signal count (§2.4).

**"Needs you" is not a vibe, it's the literal §2 definition** of `blocked_on_human` and
`human_uat_ready` — nothing new to design here, just render those two states with visual weight.

**Default landing view = "Needs You," not the full board.** Given the problem statement above, the
board's root URL (`sprint.truesight.me/`) should open directly on the `blocked_on_human` +
`human_uat_ready` cards — the answer to "what needs my attention right now" — with the full Kanban
(all columns) one click away, not the default. A zero-card "needs you" state is itself useful
information ("nothing's blocked on you, everything's moving") and should render as an explicit
all-clear, not an empty page that looks broken. Each "needs you" card's deep link is the thing Gary
actually clicks through Telegram/Discord for — the card exists specifically so he never has to
*discover* that a thread needs him by opening it cold.

### 2.4 Prioritization — advisory, resolved (§0 point 6)

A signed `HANDOFF PRIORITY SIGNAL EVENT` increments a visible counter on that ticket's card. It:

- **Never** reorders columns, never changes a ticket's state, never feeds any automated selection
  logic.
- **Is** additional context a supervisor (Envoy, DeepSeek Local, or Sophia self-checking) may weigh
  alongside everything else `SUPERVISOR_LOOP.md` §3 already considers when choosing what to work on
  next — exactly the same judgment-based selection that already exists, now with one more input.

`SUPERVISOR_LOOP.md` §3 gets a small addition recording this boundary explicitly (§7 PR7 below), so
the authority model is canonical, not just remembered from this conversation.

### 2.5 What does NOT change

- `HANDOFF_MANIFEST.md` stays the human-editable, git-diffable source of truth; `index.json` is a
  generated mirror, not a fork of it.
- No governor/JWT auth anywhere on this surface — reading is fully public (same as the credentialing
  program pages, same as SunMint's public map), matching "auth like SunMint" (§0 point 4) precisely:
  auth is only invoked for the one write action (signing a priority vote).
- Sophia's/Envoy's own execution authority (§5 of `SUPERVISOR_LOOP.md`) is untouched — this board adds
  visibility and an advisory signal, nothing else.

---

## 3. Pre-flight — verify before PR1 (§5d completeness gate)

1. **How does an event type with no dedicated GAS webhook route actually get logged?** Every other
   event type in `events_catalog.json` this session's research touched had either a GAS handler or a
   `dao_protocol` dispatch route. Confirm whether `HANDOFF PRIORITY SIGNAL EVENT` needs one written
   (even a trivial pass-through to a ledger row) or whether Edgar already has a generic fallback that
   logs any cataloged event type without a bespoke handler. This determines whether PR3 (§7) is a
   config-only catalog entry or needs actual backend code.
2. **Confirm `index.json`'s exact shape isn't already half-specified elsewhere** — `SUPERVISOR_LOOP.md`
   §8 names the two required id fields but not a full schema; write the schema as part of PR1, not
   assume one.
3. **`quests/join/index.html`'s semantics** (§1.4) — it's currently a Trello *invite* link, which is a
   different action than "browse the board." Confirm with Gary whether `join/` should redirect to
   `sprint.truesight.me` too (if the board itself has an implicit "join" moment — e.g., the
   first-signature keypair-creation flow) or whether it should point somewhere else entirely (a DAO
   onboarding page) now that Trello's own invite concept doesn't map 1:1. Don't guess this one — ask
   before PR8.
4. **`truesight_me_beta` also carries the same two Trello redirect files** (confirmed present in the
   audit — not re-verified byte-for-byte identical to prod's copies); diff them before PR8 so both
   beta and prod get consistent treatment.

✅ **Pre-flight Completeness:** items 1–2 and 4 are code-only reads any executing agent resolves
directly at low cost, folded into PR1/PR2 below. Item 3 is a human question, called out explicitly
rather than assumed, and gates PR8 specifically (not the rest of the roadmap).

---

## 4. Sequenced execution roadmap (one PR per turn — §5a)

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | Pre-flight completion: resolve §3 items 1, 2, 4 (code reads only). No code. | auto |
| **PR1** | `agentic_ai_context`: ship `handoffs/index.json` (the §1.1/§8 gap) — generated from `HANDOFF_MANIFEST.md`, schema includes Telegram thread id **and** Discord channel/thread id (§2.2), validated by extending `scripts/validate_handoff_manifest.py`. This alone already unblocks every supervisor LLM's §2 state-reading, independent of the board. | auto |
| **PR2** | `dao_protocol`: register `HANDOFF PRIORITY SIGNAL EVENT` in `events_catalog.json` (+ a minimal backend handler if PR0 found one is needed). Fields: `Handoff` (plan-file path or manifest key), `Submission Source`. No numeric "amount" — a signal is binary (signed = one vote), aggregated by count. | auto |
| **PR3** | New `TrueSightDAO/sprint` repo scaffold: static page, fetches `index.json`, renders the §2.3 Kanban columns + cards (spec link, Telegram/Discord deep link, resume-tracker one-liner), **defaulting to the "Needs You" view** with the full board one click away. Read-only — no signing yet. Deploy dark (Pages not yet DNS-mapped). | auto |
| **PR4** | Route53 CNAME `sprint.truesight.me`; verify live, 200, valid cert (same steps already proven for `cfr.truesight.me`). | auto |
| **PR5** | Add the sign-in-to-prioritize flow: reuse `sunmint_beta`'s keypair/signing code verbatim (§1.2), POST `HANDOFF PRIORITY SIGNAL EVENT` to Edgar, render the live count per card by reading `verify_public_signatures`'s new bucket. | auto |
| **PR6** | `sophia/SUPERVISOR_LOOP.md`: add the advisory-only boundary (§2.4) as a canonical rule, referencing `sprint.truesight.me` by name. Docs-only, self-mergeable per this repo's own convention. | auto |
| **PR7** | UAT (§5) on the live board. | auto |
| **PR8** | Repoint `truesight_me_prod` + `_beta`'s `quests/index.html` (and `quests/join/index.html` per §3 item 3's resolved answer) from Trello to `sprint.truesight.me`. | **`gate: human`** — touches a live, indexed, public-facing prod URL; gated on PR7's UAT passing and §3 item 3's answer |

**RESUME HERE → PR0.**

---

## 5. UAT

- **U1** — Load `sprint.truesight.me` with no signature/keypair present. Confirm every ticket from
  `HANDOFF_MANIFEST.md` appears in the correct column, with a working spec link and a working
  Telegram/Discord deep link.
- **U2** — Confirm `blocked_on_human` / `human_uat_ready` tickets are visually distinct ("needs you")
  from everything else, **and** confirm `sprint.truesight.me/` (root, no path) defaults to that view
  rather than the full board. With zero such tickets, confirm it renders an explicit all-clear state,
  not an empty/broken-looking page.
- **U3** — Sign a priority vote on a test ticket (test-tagged per §5g standing E2E authorization).
  Confirm the count increments on next load and the underlying signed event is visible in
  `verify_public_signatures`.
- **U4** — Confirm a second signature from a different keypair increments the count again (no
  double-count/dedup bug on a single identity re-signing — decide and test the intended behavior:
  one signal per identity per ticket, most likely).
- **U5** — Confirm nothing about `sunmint_beta`/`capoeira`/other existing signers changed — the shared
  signing code path is additive, not modified in a way that could regress an existing page.
- **U6** — After PR8: confirm `truesight.me/quests/` and `/quests/join/` land on the new board (or the
  §3-item-3-resolved target), and the old Trello links are gone from both prod and beta.
- **U7** — Confirm test data cleanup per §5g.

---

## 6. Open decisions remaining (small — most of this was resolved in conversation)

1. **§3 item 1** — does `HANDOFF PRIORITY SIGNAL EVENT` need a real backend handler, or does Edgar's
   existing generic path cover it? Resolves in PR0.
2. **§3 item 3** — `quests/join/index.html`'s target once Trello's invite concept doesn't apply. Needs
   Gary's answer before PR8 specifically; does not block PR0–PR7.

Everything else raised during this conversation (hosting location, auth model, prioritization
authority, click-through requirement, column/state design) is treated as resolved per §0.

---

## 7. Rollout

Per the pattern established for every other roadmap this session: **park in a new Telegram topic** for
a supervisor (Envoy or Sophia) to pick up and drive per `sophia/SUPERVISOR_LOOP.md`, rather than
executing in this session. RESUME HERE (§4) = PR0.
