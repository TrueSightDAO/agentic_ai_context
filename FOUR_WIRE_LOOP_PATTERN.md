# The Four-Wire Loop Pattern

A recurring architectural shape across TrueSight's substrate: any
"system that surfaces a signal and acts on it (with the operator as
the merge gate)" decomposes into the **same four small components**.
First named explicitly in the May 13 blog post
*[The system that broke is the system that proposes the fix](https://truesight.me/blog/posts/the-system-that-broke-is-the-system-that-proposes-the-fix.html)*
(Field Signals · #4); already implicit across at least four shipped
systems. This file generalizes the pattern so future loops can be
designed cheaply and reviewers can spot the shape (or its absence)
in PRs.

The pattern's mechanical claim: **any operator-as-merge-gate workflow
is a composition of four wires plus a visibility layer**, and once
the four wires close, the operator's role shifts from triage to
judgment. That shift is the whole point.

---

## The four wires

A closed loop needs all four. Skipping one leaks scope or burns trust:

### 1. Report path

The system emits a structured signal when something happens. Should
be **automatic** (not operator-triggered), **idempotent** (safe to
re-fire), and **structured** (downstream classifier can match without
LLM-cost ambiguity).

Examples in the wild:
- `BugsnagHandler` attached to autopilot's root logger at
  `logging.ERROR` (auto-fires on any exception or `logger.error`)
- `partners-velocity.json` + `partners-inventory.json` re-published
  after every operator action that affects them
- `[ASSET RECEIPT EVENT]` Edgar payload submitted by operator via
  `dao_client/.../report_asset_receipt.py`

### 2. Classify path

A regex / dispatcher / filter that decides *whether* a signal is
actionable and *what kind* of action it warrants. Tier-1 rule-based
classification is preferred — keeps the loop's per-event cost
predictable. LLM classification only when the cost of getting it
wrong is high enough to justify the per-call expense.

Examples:
- `email_poller._classify()` checks sender domain + subject regex
  to label emails as `github_failure` / `bugsnag_error` /
  `gas_error` / `security_alert`
- DApp bell's `partner_stock` source applies severity rules
  (`critical` / `warning` / `info`) at render time
- GAS dispatchers in `tokenomics/.../*_telegram_logs.gs` route
  Telegram-Chat-Logs rows to the right sheet by event-type substring

### 3. Lookup path

Resolve the signal to a target. *Which repo do we open the PR
against? Which partner do we poke? Which managed ledger do we
update?* Should pull from a **single source of truth** — usually a
sheet column, JSON file, or env-var dict — and **fail open** when
the lookup misses (log a warning, return null, do not invent a
target).

Examples:
- `BUGSNAG_PROJECT_REPOS` JSON env var (Bugsnag project name → repo)
- `Agroverse Partners!E` (`partner_id` slug → `contributor_contact_id`),
  joined with `Contributors contact information!A→D`
  (`contributor_contact_id` → email)
- `Shipment Ledger Listing` registry (currency-conversion ledger
  name → managed AGL spreadsheet ID)

### 4. Dedup path

Once an action is taken, *don't take it again* for the same
underlying signal. Without this wire, the loop spams (autopilot
opening fix PRs every time Bugsnag re-emails about a regressing
error; the scheduler pestering a partner every day on the same
out-of-stock signal). The dedup key has to be **stable across
re-occurrences** — Bugsnag's `error_id`, the operator-driven
`Next Check-in Date` column, the audit-log row's `Update ID` —
not derived from a transient field like timestamp.

The dedup write should happen **only after the action succeeds**.
Otherwise a transient failure (rate-limited LLM call, GitHub 502)
poisons future retries.

Examples:
- `/opt/truesight_autopilot/state/bugsnag_triaged_errors.json`
  keyed on Bugsnag `error_id`
- `Partner Poke Drafts` tab on Hit List, dynamic re-poke gate
  computed from `days_since_last_poke` + `days_until_stockout / 2`
- `Update ID` column on Partner Check-ins tab (col K),
  `poke-auto-<draft_id>` for autopilot-filed rows

---

## The visibility layer (two more wires, separate concern)

Operationally separate from the four wires above but always shipped
together. The visibility layer makes the operator's review surface
**findable in one place** so they don't have to remember which tab,
inbox, or page to check.

- **Action label** on the artifact the loop produces (e.g.
  `AI/proposed fix` GitHub PR label)
- **Source label** on whatever inbound signal triggered the loop
  (e.g. `AI/proposed fix` Gmail label on the email that triggered
  the PR), so a single search string finds both surfaces

Other instances of the visibility layer in the workspace:
- DApp notification bell — single badge total, click expands to
  per-source breakdown (see `DAPP_NOTIFICATION_BADGE.md`)
- `Partner Poke Drafts` audit log tab — every loop iteration leaves
  a row, so the operator can grep for what's been tried

---

## Worked examples — same shape, different domains

### Autopilot self-healing (May 13, 2026)

Documented end-to-end in `AUTOPILOT_CODE_MODIFICATIONS.md` §§9–11.

| Wire | Implementation |
|------|----------------|
| Report  | `BugsnagHandler` attached at `logging.ERROR` in `app/main.py` |
| Classify| `BUGSNAG_SENDER` + `BUGSNAG_SUBJECTS` regexes in `app/email_poller.py` |
| Lookup  | `BUGSNAG_PROJECT_REPOS` JSON env var |
| Dedup   | `/opt/truesight_autopilot/state/bugsnag_triaged_errors.json` keyed on Bugsnag `error_id` |
| Visibility (action) | `AI/proposed fix` GitHub PR label (auto-created in target repo, #f4a300) |
| Visibility (source) | `AI/proposed fix` Gmail label on the source email |

### Partner Poke Scheduler (May 12, 2026)

Documented in `PARTNER_POKE_SCHEDULER_v0.md`.

| Wire | Implementation |
|------|----------------|
| Report  | Partner Stock signals (out-of-stock / low / dormant) computed from `partners-velocity.json` + `partners-inventory.json` |
| Classify| Bell's `partner_stock` source + dynamic-cadence gate (`days_until_stockout < POKE_THRESHOLD_DAYS` + `days_since_last_poke >= max(3, days_until_stockout/2)`) |
| Lookup  | `Agroverse Partners!E` → `Contributors contact information!A→D` (resolves which partner to poke + how to reach them; falls back to self-poke when no email on file) |
| Dedup   | `Partner Poke Drafts` audit log tab on Hit List spreadsheet |
| Visibility (action) | `AI/Partner Poke` Gmail label on the draft + 4th cohort tab on `warmup_review.html` |
| Visibility (source) | DApp bell's Outbound Review count + Partner Stock attention card |

### DApp notification bell (May 12, 2026)

Documented in `DAPP_NOTIFICATION_BADGE.md`. The bell is itself a
*classify-and-display* surface for multiple loops; it doesn't act,
it surfaces. Treat it as the visibility layer for whatever loops
publish to it.

### Future: shipping decisions, sourcing quotas, video-to-page propagation

Per the *AI-first vertically integrated supply chain* vision Gary
sketched in Beer Hall on 2026-05-12, the same four-wire pattern is
the natural shape for the upstream stages too:

- **Shipping calculus** (Brazil → SF freight): report = inventory
  level at SF + sales velocity; classify = expected days-of-cover
  threshold; lookup = which freight provider + which Brazil-side
  inventory pool; dedup = active shipment ledger row.
- **Sourcing quotas** (when Gary travels to Brazil): report =
  upcoming demand projection; classify = farm-vs-speculative-source
  budget split; lookup = farm capacity ledger; dedup = the planned
  sourcing visit's authorization row.
- **Video → page propagation** (capoeira-style): report = new video
  upload to a watched folder; classify = transcription → topic
  match; lookup = which site/section to publish to; dedup = video
  hash.

Each is the same four wires.

---

## When to use it

- The system has a **clearly-classifiable signal** (or one classifier
  away from clear).
- The action is **well-scoped** (a draft PR, a Gmail draft, a sheet
  row append) and the operator can review-then-merge cheaply.
- A **stable dedup key exists** (or can be derived).
- The operator's marginal cost of approval is **lower than the
  current marginal cost of triage**.

---

## When not to use it

- The signal is so noisy that classify-path false-positives would
  dominate (then build a better signal source first).
- The action is **irreversible** without operator review (then the
  loop's "merge gate" needs to be much heavier than a click —
  consider a different pattern entirely, e.g. a Discovered Protocol
  workflow, see `discovered-protocols-…` blog post).
- There's no stable dedup key (then dedup degrades to "skip if
  acted in the last N minutes" which is a leaky form of correctness).
- The lookup target depends on judgment that an LLM can't reliably
  produce (then the loop needs a human in the lookup path too,
  which makes it a different pattern).

---

## Anti-patterns

1. **Skipping the dedup wire** — every system that ships without
   dedup eventually spams. The error gets re-fired, the cron
   re-runs, the scheduler re-evaluates; the loop fires again.
   `error_id` for Bugsnag; `Update ID` for Partner Check-ins;
   `gmail_draft_id` for warmup. Build it from day one.
2. **Fail-closed on lookup miss** — if the lookup table doesn't
   include a target, the loop should *log + skip*, not *invent a
   target* (don't auto-pick a "default repo" — humans miss the
   warning sign).
3. **Dedup write before action confirmation** — write the dedup
   entry only after the action succeeded. Otherwise transient
   failures (rate limits, network blips) poison future retries
   for that signal forever.
4. **LLM in the classify path when a regex would do** — the
   per-event cost adds up quickly. Tier-1 rule-based is the
   default; Tier-2 LLM only when ambiguity is high enough to
   justify the spend.
5. **No visibility layer** — if the operator can't search the
   review queue with a single label / badge / filter, they will
   miss things and lose trust in the loop. Two labels (action
   + source) for one search string is the minimum.
6. **Loop without merge gate** — autonomous repair is a
   different pattern with much heavier safety requirements
   (see `AUTOPILOT_CODE_MODIFICATIONS.md` §§4–5 for autopilot's
   safety-hooks rules). The four-wire loop's safety property
   *is* the merge gate.

---

## Adding a new loop — checklist

When proposing a new four-wire loop in a PR or design doc, name
each wire explicitly:

- [ ] **Report path:** what signal, fired by what, in what shape?
- [ ] **Classify path:** what's actionable vs noise? Tier-1 rules
      or Tier-2 LLM?
- [ ] **Lookup path:** what's the single source of truth that maps
      signal → target? What happens when the lookup misses?
- [ ] **Dedup path:** what's the stable dedup key? Where's it
      stored? When does the dedup entry get written (must be
      after action confirmation)?
- [ ] **Visibility — action label:** what label / badge / artifact
      lets the operator find the loop's output?
- [ ] **Visibility — source label:** what marks the inbound signal
      as already-triaged so the operator can find the upstream
      context?
- [ ] **Merge gate:** what's the operator's review surface, and how
      heavy is the click? (For draft PRs and Gmail drafts: one click.
      For higher-blast-radius actions: needs more deliberate gating.)
- [ ] **Failure modes:** which wire fails most often? What does
      degraded behavior look like? (Usually: one wire returns
      null/empty and the loop becomes a no-op, which is correct.)

---

## Why this pattern reappears

The pattern is recurrent because the underlying constraint is
recurrent: **TrueSight's operating model has the operator as the
judgment layer and the substrate as the toil layer**. Every domain
where toil and judgment can be cleanly separated — every domain
where a signal can be detected, routed, mapped to a target, and
deduped without operator input — fits this shape.

Conversely, domains where toil and judgment are *fused* (the
operator's evaluation of the signal is itself the action — e.g.
deciding whether a partner relationship is worth investing in,
deciding whether a new farm is trustworthy, attuning to zeitgeist)
do not fit this pattern and should not be retrofitted into it. See
*[The Do Nothing Society](https://truesight.me/blog/posts/the-do-nothing-society-let-machines-run-the-chain-let-humans-hold-the-soul.html)*
for the long-form argument.

---

## Related context

- **Blog: The system that broke is the system that proposes the
  fix** (Field Signals · #4) — the post that named this pattern
  out loud, with the autopilot self-healing instance as the
  worked example.
- **`AUTOPILOT_CODE_MODIFICATIONS.md`** §§9–11 — the autopilot
  loop in detail.
- **`PARTNER_POKE_SCHEDULER_v0.md`** — the scheduler loop in
  detail.
- **`DAPP_NOTIFICATION_BADGE.md`** — the visibility-layer
  contract for any module that wants to publish to the bell.
- **`MULTI_LLM_ORCHESTRATION.md`** — when the action a wire takes
  is itself an LLM call, this doc covers the tier/handoff rules.

*Last refreshed 2026-05-13. Refresh when a new instance of the
pattern ships and is worth adding to the worked-examples table, or
when an anti-pattern shows up in production that's worth naming.*
