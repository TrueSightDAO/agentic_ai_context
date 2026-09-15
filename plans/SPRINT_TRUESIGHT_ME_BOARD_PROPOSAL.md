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
board's primary reason to exist; everything else (spec links, conversation deep links) is secondary
context once Gary already knows which tickets deserve a look.

---

## 0. What this is, stated plainly (design decisions as they were made)

Gary, over several turns today:

1. Wondered whether syncing tasks to an external tool (Trello/Jira/Pipedrive/Pivotal Tracker) would
   help him track and monitor what Sophia's working on.
2. Refined this to: **a Kanban board hosted on `truesight.me` itself**, not a third-party tool.
3. Refined the location to: **its own subdomain**, e.g. `sprint.truesight.me` — not
   `sophia.truesight.me` (keeps it separate from the autopilot's own operational surface).
4. Specified **auth like `capoeira`/Butterfly Effect/SunMint** — the DAO's standard client-side RSA
   keypair pattern, not a governor-only login. (Superseded by point 6b below: the board ended up
   needing no write action at all, so no auth of any kind — the *spirit* of "public, no login wall"
   still holds, just more simply than originally scoped.)
5. Originally specified that an authenticated visitor should be able to, beyond viewing, **"sign a
   ticket for prioritizing"** — via a signed DAO event, same pattern as SunMint.
6. On the authority question this raised (does a signed vote *drive* the supervisor's queue, or just
   *inform* it): **"Contributor sign off is just advisory. Envoy should have autonomy on what to
   prioritize based on the context envoy has."** — resolved: advisory only.
6b. **Simplified, same day: no signed event at all.** *"Perhaps I just mention this to envoy instead
   of a new event."* Prioritization doesn't need a cryptographic voting primitive — Gary (or anyone)
   sees a ticket on the board, clicks through to its live Telegram/Discord thread (point 7 below), and
   says so directly, the same way any instruction reaches Envoy/Sophia today. Point 6's *advisory-only*
   resolution still holds — it just applies to a chat message instead of a signed vote. This removes
   the entire signing/auth/event-catalog surface from the build (§1.2/§1.3 below are kept as audit
   trail for *why* that path was considered and dropped, not as design this proposal still uses).
7. Wants **one place to see the implementation spec and click through to the live conversation**
   (Telegram or Discord) where a ticket's work is actually happening — this is now also *how*
   prioritization happens (point 6b), not just a separate nice-to-have.
8. Wants **distinct columns showing where each ticket currently is**, so a glance answers "what needs
   my attention and why" — not a flat list.
9. Flagged that `truesight.me` already links out to a **dead, unused Trello board**
   (`quests/index.html`, `quests/join/index.html`) and wants that link **repointed to this board once
   it ships** — not before, and not blocking this proposal.
10. On `quests/join/index.html` specifically (a Trello *invite* link today): **"Not invite concept."**
   The new board has no join/invite flow to mirror — resolved, both files repoint the same way, no
   special-case needed (§1.4, §3).
11. **Confirmed, same day, once Sophia's PR0 found the Discord ids were null for all 43 rows:**
   *"Can we ensure the hand off also tracks discord channels??"* — not optional, not something to skip
   because the manifest happens not to carry the columns yet. Elevated to its own unit, **PR1b** (§4),
   ahead of the board itself.

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

### 1.2 The DAO-standard signing pattern — considered for prioritization, superseded (§0 point 6b)

`sunmint_beta/index.html` has a client-side RSA keypair pattern (`localStorage` keypair generated on
first use, `signText()`, POST to `${EDGAR_BASE}/dao/submit_contribution`, optional email linking) that
would have been the natural fit for "sign a ticket to prioritize" (§0 point 5, original). **Not used —
Gary simplified prioritization to a direct chat message instead (§0 point 6b), so this build needs no
auth of any kind.** Kept here only as the audit trail for why that path was seriously considered before
being dropped in favor of something simpler; if a future write-action is ever added to this board, this
is still the pattern to reuse.

### 1.3 The event catalog — considered, not needed (§0 point 6b)

`dao_protocol/truesight_dao_client/server/data/events_catalog.json` (72 entries, read directly) would
have been where a new `HANDOFF PRIORITY SIGNAL EVENT` type got registered. **Not needed** — with
prioritization reduced to a chat message via the existing Telegram/Discord click-through (§2.4), there
is no new event type, no catalog entry, and no `verify_public_signatures` bucket to build. Noted here so
a future reader doesn't wonder whether this was overlooked.

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
and unused. **Both files repoint the same way** — `quests/join/index.html` needs no separate "invite"
handling, per §0 point 10 ("Not invite concept"). Repointing is the **last** unit of this roadmap
(§4 PR6), gated on the new board being live and UAT-passed — not before.

---

## 2. Target architecture

### 2.1 Hosting — a new static subdomain, same pattern as `cfr-anapu`

New repo `TrueSightDAO/sprint` (or similar), GitHub Pages (`gh-pages` branch — the token-scope
workaround already proven twice this session's prior work), Route53 CNAME `sprint.truesight.me`. Pure
static site, **fully read-only**: fetches public JSON (§1.1), renders client-side — **no backend, no
auth, no write path at all**, since prioritization is now a chat message, not a page action (§0 point
6b). Simpler than `sunmint_beta`/`capoeira`/`cfr-anapu`, which all have a signed-submission surface this
board doesn't need.

### 2.2 Data sources (all already public, all already read this session)

| Data | Source | New? |
|---|---|---|
| Ticket list + state + spec link + Telegram thread | `agentic_ai_context/handoffs/index.json` | **Needs to ship** (§1.1 gap) — not new design |
| Discord channel/thread id (for click-through, §0 point 7) | Same `index.json`, extended | **New field** — already anticipated in `SUPERVISOR_LOOP.md` §8's own spec: "both Telegram thread_id **and** Discord channel/thread id" |
| Implementation spec content | The plan file `index.json` points at, fetched raw (jsDelivr-primary/raw-fallback, same pattern as `program-shell.js`) | No — reuse existing fetch pattern |

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
deep link, and the current resume-tracker one-liner (already in the manifest — "why" per §0 point 8).
The Telegram/Discord deep link doubles as the prioritization mechanism (§2.4) — there's no on-page
action beyond navigating to the conversation.

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

### 2.4 Prioritization — advisory, resolved (§0 points 6 + 6b)

No on-page action, no signed event. A visitor who thinks a ticket deserves attention clicks its
Telegram/Discord deep link and says so, in the actual conversation, the same way anyone already
directs Envoy/Sophia today. This:

- **Never** reorders columns, never changes a ticket's state, never feeds any automated selection
  logic — there is no data structure representing "priority" at all.
- **Is** additional context a supervisor (Envoy, DeepSeek Local, or Sophia self-checking) may weigh
  alongside everything else `SUPERVISOR_LOOP.md` §3 already considers when choosing what to work on
  next — exactly the same judgment-based selection that already exists, expressed through the same
  chat channel that already carries every other instruction.

`SUPERVISOR_LOOP.md` §3 gets a small addition recording this boundary explicitly (§4 PR4 below) — not
because new code needs to honor it, but so "a chat message isn't an automatic override" is written down
as canonical, not just remembered from this conversation.

### 2.5 What does NOT change

- `HANDOFF_MANIFEST.md` stays the human-editable, git-diffable source of truth; `index.json` is a
  generated mirror, not a fork of it.
- **No auth anywhere on this surface, of any kind** — reading is fully public (same as the
  credentialing program pages, same as SunMint's public map), and there is no longer a write action
  that would need one.
- Sophia's/Envoy's own execution authority (§5 of `SUPERVISOR_LOOP.md`) is untouched — this board adds
  visibility, nothing else.

---

## 3. Pre-flight — verify before PR1 (§5d completeness gate)

1. **Confirm `index.json`'s exact shape isn't already half-specified elsewhere** — `SUPERVISOR_LOOP.md`
   §8 names the two required id fields but not a full schema; write the schema as part of PR1, not
   assume one.
2. **`truesight_me_beta` also carries the same two Trello redirect files** (confirmed present in the
   audit — not re-verified byte-for-byte identical to prod's copies); diff them before PR6 so both
   beta and prod get consistent treatment. Since §0 point 10 resolved `quests/join/index.html` to the
   same treatment as `quests/index.html`, this is now a pure code-diff task with no open question
   attached.

### 3.1 Results — PR0 complete (2026-09-15, Sophia)

**Item 1 — `index.json` schema: ✅ ALREADY SHIPPED.** `handoffs/index.json` is live on `main` (schema v1:
`state_enum`, `handoffs[]` with `plan_file`/`title`/`state`/`telegram_thread_id`/`last_updated`,
`counts_by_state`), generated by `scripts/build_handoff_index.py` (merged #1143) and drift-gated by
`scripts/validate_handoff_manifest.py --check-index` (merged #1145). **The plan's PR1 is therefore already
done** — the roadmap rebases to PR1a/PR2 below.

**Item 2 — beta/prod Trello stubs: ✅ BYTE-IDENTICAL.** All four files match (etag `8c0435d5…` for both
`quests/index.html`, `384971e2…` for both `quests/join/index.html`). Each stub carries **four** redirect
layers (GTM snippet, `meta refresh`, `link rel=canonical`, `window.location.replace` + fallback `<a>`);
PR6 must repoint all four, in all four files. No open question (§0 point 10).

**Blocker found — the board would render a false "all-clear".** `build_handoff_index.py` `STATE_RULES`
maps Status→state by first-match regex, ordered so `complet(e|ed)`/`done` are tested **before**
`human uat`. A row reading *"build complete — awaiting governor UAT"* (CRF Anapu) therefore maps to
`done`, not `human_uat_ready`; a bare `"blocked"` with no `HUMAN_GATE_KEYWORDS` hit maps to
`paused_at_gate`, never `blocked_on_human`; and `governor UAT` is absent from the human-UAT regex. Live
index reports `human_uat_ready: 0, blocked_on_human: 0` across 43 rows. **Must be fixed (PR1a) before the
board ships**, or `sprint.truesight.me/` shows nothing needs Gary.

✅ **Pre-flight Completeness:** both original items resolved (code reads only); one new code defect
surfaced, folded into PR1a below. One **gate before PR2**: the repo name `sprint` matches no blessed
`create_repo_patterns` glob — confirm the name (or a `…-site`-suffixed variant) before scaffolding.

---

## 4. Sequenced execution roadmap (one PR per turn — §5a)

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | ✅ **DONE (2026-09-15)** — pre-flight resolved (§3.1). No code. | — |
| **PR1** | ✅ **ALREADY SHIPPED** — `handoffs/index.json` + `build_handoff_index.py` (#1143) + `--check-index` drift gate (#1145) are live on `main`; the board's data source already exists. | — |
| **PR1a** | `agentic_ai_context`: fix `build_handoff_index.py` `STATE_RULES` ordering so `human uat` / `governor uat` / `ready for human` are tested **before** `complete`/`done`, and widen `HUMAN_GATE_KEYWORDS` (add `governor`, `approval`, `thumbs`) so genuinely human-gated rows land in `blocked_on_human`. Regenerate `index.json` (drift gate) + correct the manifest row. **Prerequisite for PR2** — without it the default "Needs You" view is wrong. | auto |
| **PR1b** | `agentic_ai_context`: Gary confirmed Discord tracking is required, not optional (2026-09-15). Add the **`Discord channel id`** / **`Discord thread id`** columns `build_handoff_index.py` already anticipates by name (its own docstring: "those columns do not exist yet") to `HANDOFF_MANIFEST.md`'s header row, populate them for every row that actually runs in a Discord channel today (at minimum `DISCORD_ADAPTER_PLAN.md` and `DISCORD_ENVOY_GOVERNOR_PARITY_PLAN.md` — cross-reference `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §2's venue registry for the real channel ids rather than guessing), leave blank for Telegram-only rows, regenerate `index.json` (drift gate), and add a line to the manifest's own "How to update" section so future handoffs populate it when relevant. **Prerequisite for PR2's Discord deep-link cards** — without it every card's Discord link is null, same failure shape PR1a just fixed for state. Can be folded into PR1a's turn if already touching this file/schema, or run as its own turn — supervisor's call. | auto |
| **PR2** | New `TrueSightDAO/sprint` repo scaffold: static page, fetches `index.json`, renders the §2.3 Kanban columns + cards (spec link, Telegram/Discord deep link, resume-tracker one-liner), **defaulting to the "Needs You" view** with the full board one click away. Fully read-only, no auth. Deploy dark (Pages not yet DNS-mapped). | auto |
| **PR3** | Route53 CNAME `sprint.truesight.me`; verify live, 200, valid cert (same steps already proven for `cfr.truesight.me`). | auto |
| **PR4** | `sophia/SUPERVISOR_LOOP.md`: add the advisory-only boundary (§2.4) as a canonical rule, referencing `sprint.truesight.me` by name — a chat-message priority signal is context for the supervisor's judgment, never an automatic override. Docs-only, self-mergeable per this repo's own convention. | auto |
| **PR5** | UAT (§5) on the live board. | auto |
| **PR6** | Repoint `truesight_me_prod` + `_beta`'s `quests/index.html` **and** `quests/join/index.html` (both, identically — §0 point 10) from Trello to `sprint.truesight.me`. | **`gate: human`** — touches a live, indexed, public-facing prod URL; gated on PR5's UAT passing |

**RESUME HERE → PR1a.**

---

## 5. UAT

- **U1** — Load `sprint.truesight.me`. Confirm every ticket from `HANDOFF_MANIFEST.md` appears in the
  correct column, with a working spec link and a working Telegram/Discord deep link.
- **U2** — Confirm `blocked_on_human` / `human_uat_ready` tickets are visually distinct ("needs you")
  from everything else, **and** confirm `sprint.truesight.me/` (root, no path) defaults to that view
  rather than the full board. With zero such tickets, confirm it renders an explicit all-clear state,
  not an empty/broken-looking page.
- **U3** — Click a card's Telegram deep link and a card's Discord deep link; confirm both land in the
  correct live conversation.
- **U4** — After PR6: confirm `truesight.me/quests/` and `/quests/join/` both land on the new board,
  and the old Trello links are gone from both prod and beta.

---

## 6. Open decisions remaining

**None.** Every fork raised during this conversation (hosting location, auth model — now "no auth at
all" — prioritization mechanism and its advisory authority, click-through requirement, column/state
design, and `quests/join/index.html`'s treatment) is resolved per §0. §3's two remaining pre-flight
items are code-only reads, not decisions.

---

## 7. Rollout

Per the pattern established for every other roadmap this session: **park in a new Telegram topic** for
a supervisor (Envoy or Sophia) to pick up and drive per `sophia/SUPERVISOR_LOOP.md`, rather than
executing in this session. RESUME HERE (§4) = PR1a.
