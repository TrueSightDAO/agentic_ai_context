# Warm-up Conversion Improvement Plan — Fixing the Reply-Rate Collapse

**Status:** IN PROGRESS — PR0 (this plan) + PR1 landing this turn
**Date:** 2026-07-18
**Owner:** Gary Teh (human) + Claude Code (AI assist, acting in CMO capacity per governor request)
**Repos affected:** [TrueSightDAO/go_to_market](https://github.com/TrueSightDAO/go_to_market) (implementation),
[TrueSightDAO/agentic_ai_context](https://github.com/TrueSightDAO/agentic_ai_context) (this plan)
**Related docs:** `WARMUP_AUTOSEND_PLAN.md` (the auto-send graduation this plan follows up on — its own
§6 "Watch item" predicted exactly the failure mode found here), `sops/AGROVERSE_NEWSLETTER_WORKFLOW.md` §1b
(Email 360 — this is the B2B outbound sibling), `growth/GROWTH_MODEL.md` (Email360 Retention Loop + Direct
Marketing channel), `HIT_LIST_STATE_MACHINE.md` (the 13-state pipeline this modifies).

**Goal (governor's framing):** increase conversion rate **without alienating the people we're reaching out to.**

---

## TL;DR

`WARMUP_AUTOSEND_PLAN.md` graduated first-touch warm-up sending to automation on 2026-06-05. Six weeks
later a stats review + direct Gmail audit (every one of the 333 threads sent since launch, not a sample)
found: throughput doubled as designed (✅), the pending-review backlog target was hit (✅), but **genuine
prospect replies collapsed from ~6% to 0.3%** (1 real reply in 333 sends) and **zero new Partnered stores
or Manager Follow-up escalations** landed in six-plus weeks — despite roughly 2x'ing outbound volume.
Reply-detection itself was verified correct (zero false negatives found); the problem is real, not a
monitoring gap.

The strongest lead: `Hosts Circles` prospects (venues that host sound baths, breathwork, moon circles,
etc.) convert at **11.8% vs 6.6%** for everyone else (~1.8x) and supplied 3 of the 14 current Partnered
stores off 7.6% of the list — but that tier is (correctly) excluded from auto-send and routed to manual
review, so the channel that scaled 2x is exactly the lower-converting general population, while the
best-converting segment's throughput never grew. Two addresses (Esalen Institute Gift Shop, 7 Rays
Holistic Center) are confirmed dead-end auto-responder mailboxes still being freshly re-touched every
send cycle, and a duplicate-logging bug has written 740 redundant audit rows for those two alone.

**The plan:** stop wasting sends on confirmed dead ends, segment the pitch instead of blasting one script
at every shop type, and give the best-converting segment a dedicated fast lane — all while keeping every
existing anti-spam guardrail (drip cadence, lint-clean gate, no increase in touch frequency to any single
prospect) intact, because "don't alienate" is a hard constraint, not a nice-to-have.

---

## 1. Assessment — what the data says (recap of the 2026-07-18 audit)

### 1.1 Volume and backlog — working as designed

| Metric | Baseline (2026-06-05) | Now (2026-07-18) | Verdict |
|---|---|---|---|
| Warm-up send throughput | bursty, ~27/week | steady ~51/week (333 sends / 7 weeks) | ✅ drip cadence works |
| Pending-review backlog | 98 rows, median 24 days | 48 rows, median 1.2 days | ✅ target (<2 days) met |
| Bounce handling | not yet built | 18 caught day 1, 5 more wrong-address catches since | ✅ working |

### 1.2 Reply/conversion — collapsed, confirmed by direct Gmail audit

- Checked **all 333 threads** sent since launch (not a sample). **7 had any inbound message.** Of those:
  2 were stale day-1 bounce notices, 3 were a third-party "Mailsuite Reminder" tool's own nag messages
  (not from the recipient), 1 was a confirmed genuine auto-responder, and **1 was a real human reply**
  (Blackbirdspiritual — correctly classified `hard_no`, Gary's close was appropriate).
- **Zero false negatives found** — the automated classifier/promoter caught everything a manual read did.
  The collapse is real, not a detection bug.
- At the pre-launch baseline rate (~6%, from the original 232-thread audit), 333 sends should have
  produced ~18-20 replies. We got 1.
- Zero new **Partnered** (still 14), zero new **Manager Follow-up** escalations (still ~33), Hit List
  total essentially flat (669→670) despite 6+ weeks of ~2x'd outbound.

### 1.3 Open-rate check — rules out a pure deliverability story

| | Pre-launch | Post-launch |
|---|---|---|
| Open rate | 84.7% | 67.5% |
| Click-through | 5.9% | 4.0% |

Open rate is down but still healthy, and **flat week-over-week since launch** (66-77%, no decay trend).
People are seeing the emails at a normal rate; the funnel breaks specifically between *opened* and
*acted on*. That points at targeting/content, not sender reputation or list exhaustion.

### 1.4 The `Hosts Circles` signal

| Segment | n | Partnered/Manager Follow-up rate |
|---|---|---|
| `Hosts Circles` = Yes | 51 | **11.8%** (6 rows) |
| Everyone else | 619 | 6.6% (41 rows) |

~1.8x, and this 7.6%-of-the-list segment supplied 3 of the 14 current Partnered stores (21%) — including
the store the original 2026-06-05 audit named as the one live conversion. This segment is **excluded from
auto-send by design** (routed to human review) — correct for quality, but it means throughput on the
best-converting segment hasn't moved since launch while the rest of the list got 2x'd.

### 1.5 Two confirmed dead-end addresses, and a duplicate-logging bug

Read the actual reply bodies directly: `info@esalen.org` and `hemla@7raysholisticcenter.com` are genuine
automated out-of-office / high-volume auto-responders (verified text: "Due to high volumes...", "I am out
of the office until..."), each triggered on **2 separate, distinct outreach cycles** with zero human
engagement ever. Yet the pipeline keeps generating **fresh** drafts to them (7 Rays has a new pending
draft as of today) and the reply-detection step re-logs the *same* underlying auto-reply as a new DApp
Remarks row **every hourly run** because there's no idempotency check — 750 rows logged, only 10 distinct
real events, **740 pure duplicate noise** (~20% of the entire 3,764-row DApp Remarks audit tab).

### 1.6 Content

The warm-up copy is one fixed script (Amazon restoration → tree-per-bag → QR code → 30-sec reel) with
only the shop name substituted, sent identically to an astrology store, a yoga studio, a wellness clinic,
and an apothecary alike — despite `Shop Type` and `Hosts Circles` activity type already sitting in the
sheet as targetable signal that isn't used.

---

## 2. Design principles and guardrails (the "don't alienate" constraint)

These are non-negotiable across every unit below — inherited from `WARMUP_AUTOSEND_PLAN.md` §2 and
tightened where this plan's changes could otherwise increase outreach pressure:

1. **No increase in touch frequency to any single prospect.** Every change here re-targets or reduces
   sends to already-eligible rows; none of it adds new cadence, new follow-up steps, or shortens the
   min-days-since-sent gate.
2. **Confirmed dead ends get *fewer* touches, not different ones.** Parking an auto-responder-only
   address is a strict reduction in contact attempts to that mailbox — it can never make the experience
   worse for a prospect, only stop pestering an inbox nobody reads.
3. **Segmented copy still passes the existing 12-rule linter and the lint-clean gate before auto-send.**
   New template variants are not exempt from `preview_warmup_drafts.py`'s red/yellow checks.
4. **Fast-tracking `Hosts Circles` review is a human-attention reallocation, not a new send channel.**
   It surfaces existing manually-reviewed drafts sooner; it does not auto-send them (they stay excluded
   from PR1 of `WARMUP_AUTOSEND_PLAN.md` by design — that exclusion is a quality control, not a bug).
5. **UAT before scaling any content change.** Segmented templates get a human read-through on a sample
   before the linter/auto-send gate is allowed to pass them at volume (see §5 UAT).
6. **Anti-patterns list from `GROWTH_MODEL.md` still applies in full** — no reactivation nagging, no
   gamification, no volume-as-qualification.

---

## 3. Pre-flight checklist (§5d completeness)

- [x] Root cause of the reply collapse confirmed via direct Gmail audit (not just Sheets data) —
      no cross-repo state left to re-discover; findings are captured in §1 above.
- [x] Duplicate-logging bug's exact mechanism identified: `promote_warmup_replies()` in
      `scripts/suggest_warmup_prospect_drafts.py` (`go_to_market`) has no idempotency check before
      appending a DApp Remarks row for a suppressed auto-reply — re-detects and re-logs the same
      message every hourly run because Status never leaves `AI: Warm up prospect` for auto-reply rows.
- [x] Existing idempotency pattern to reuse identified: genuine replies already get a Gmail label
      (`AI/Prospect Replied`) applied and the message resource's `labelIds` is already fetched as part
      of the existing `full = service.users().messages().get(..., format="full")` call inside
      `inbound_reply_details()` — no new API call needed to check/apply a second marker label.
- [x] Existing terminal status to reuse for parking identified: `On Hold` (already used by
      `classify_warmup_replies.py` for `soft_no` outcomes) — no new Hit List status value needed.
- [x] Threshold sanity-checked against real data: both confirmed dead-end addresses (Esalen, 7 Rays)
      already have exactly 2 distinct auto-reply-only cycles on record with zero genuine reply ever —
      a park-after-2 threshold flags both immediately without being trigger-happy on a single
      temporary out-of-office responder.
- [x] Credentials verified working this session: `market_research/google_credentials.json` (Sheets,
      read-only tested), `market_research/credentials/gmail/token.json` (`gmail.modify` scope, used
      read-only this session).
- [x] Repo/workflow topology confirmed: reply promotion runs hourly via
      `.github/workflows/email-agent-sync-followup.yml` step "Promote warm-up replies"; draft
      generation + reply promotion also run daily via `manager-followup-drafts.yml`. Both call
      `scripts/suggest_warmup_prospect_drafts.py` — a single code change lands in both paths.

**✅ Pre-flight Completeness:** no execution unit below requires reading a file/state not already
captured above.

## 3a. Authorization envelope (§5e — batched once, for the whole arc)

- **Pre-authorized for this arc:** opening PRs on `go_to_market` and `agentic_ai_context` for every unit
  below; running scripts in `--dry-run` (read-only) against production Sheets/Gmail to verify behavior
  before a PR is opened.
- **Gated (ask once, not per-PR):** **merging any PR to `main`** on either repo. `go_to_market`'s
  automation runs directly off `main` via scheduled GitHub Actions — merging **is** the production
  deploy for these scripts (no beta/staging split exists for this repo the way it does for the web
  properties). Per OPERATING_INSTRUCTIONS §5c ("merging code to a default branch" is an always-stop
  gate), Claude opens PRs and reports them; **Gary merges.**
- **Also gated:** enabling any new template variant at auto-send volume beyond the UAT sample (§5) — the
  first live batch of any new content is a human-reviewed sample, not a blind switch-over.

---

## 4. Sequenced plan — one PR per turn

### PR0 — this plan (`agentic_ai_context`)
Documentation only. No behavior change.

### PR1 — Stop wasting sends on confirmed dead ends *(this turn)*
`go_to_market` / `scripts/suggest_warmup_prospect_drafts.py`:
- Add a Gmail label-based idempotency marker (`AI/Auto-reply Logged`) so a suppressed auto-reply is
  logged to DApp Remarks **once**, not once per hourly run. Reuses the `labelIds` already present on
  the message resource fetched inside `inbound_reply_details()` — zero new Gmail API calls.
- Track a per-row auto-reply streak in Hit List `Notes` (`auto_reply_streak=N`); when a *new* (not a
  re-detection of the same message) auto-reply-only cycle brings the streak to **2**, flip Status
  `AI: Warm up prospect` → `On Hold` with a `parked: auto-responder only, no human reply after N
  touches (date)` marker, and stop drafting to that address. Strictly reduces contact attempts to a
  mailbox nobody reads — cannot make any prospect's experience worse.
- `--auto-reply-park-threshold` (default 2) CLI flag, tunable without a code change.
- No change to send volume, cadence, or content for any row that has ever produced a genuine reply.

### PR2 — Segment the first-touch pitch by prospect type
`go_to_market` / `scripts/suggest_warmup_prospect_drafts.py` + `templates/warmup_outreach_reference.md`:
- 3 template framings keyed off existing `Shop Type` / `Hosts Circles` columns (no new scraping):
  ceremonial/spiritual framing, retail-merchandising framing, and a `Hosts Circles`-specific framing
  ("cacao ceremony as a bookable addition to your circle") for the highest-converting segment.
- Every variant still must clear the existing 12-rule linter before auto-send is eligible.
- **UAT gate (§5):** Gary reads a sample (10-15 drafts, spread across the 3 variants) before the
  linter/auto-send path is allowed to run them at volume.

### PR3 — Give the best-converting segment a fast lane + close the metrics gap
`go_to_market`:
- Surface `Hosts Circles = Yes` pending-review drafts distinctly (sort-first / flagged) in
  `preview_warmup_drafts.py` so they get same-day human attention — reallocating attention, not adding
  a send path.
- Add reply-rate-by-segment (`Hosts Circles` yes/no) and by-channel (auto vs. human-sent) to a recurring
  readout, and actually run it on a calendar cadence (the original plan's 30-day readout was never done
  — this is 6 weeks overdue). Log the readout cadence itself in `agentic_ai_context` so it isn't silently
  skipped again.

---

## 5. UAT phase

- **PR1 (parking logic):** not human-facing in the sense of a UI, but is prospect-facing in effect
  (reduced touches to 2 known rows day one). **Verification before merge:** dry-run output must show
  exactly `Esalen Institute Gift Shop` and `7 Rays Holistic Center` (and no others) crossing the
  threshold on this data snapshot — confirms the logic doesn't over-fire on the rest of the 66-row
  warm-up queue. UAT: n/a beyond that dry-run check (no live human-facing surface changes).
- **PR2 (segmented templates):** UAT is mandatory and explicit — Gary reads 10-15 sample drafts across
  the 3 variants in Gmail draft form (not sent) before the auto-send linter path is allowed to touch
  them. Acceptance criterion: no variant reads as more generic/spammy than the current single template;
  each variant is recognizably more specific to that shop type than today's copy.
- **PR3 (fast lane + readout):** UAT is the first real readout itself — confirm the `Hosts Circles`
  segment's reply rate is being measured correctly against a manually-recomputed spot check.

---

## 6. Resume tracker

> **RESUME HERE →** PR1 is done (Sophia's #170, merged). PR2 is open (#169) and rebased cleanly on top
> of PR1 — **awaiting the UAT read-through with Gary** before the linter/auto-send path is allowed to
> run the new segmented copy at volume; do not enable it blind. PR3 in progress.

| Unit | Scope | Repo | Opened | Merged (human) | Contribution reported |
|---|---|---|---|---|---|
| PR0 | This plan | agentic_ai_context | ✅ [#697](https://github.com/TrueSightDAO/agentic_ai_context/pull/697) | ☐ | ☐ |
| PR1 | Dedupe auto-reply logging + auto-park confirmed dead ends | go_to_market | ✅ [#170](https://github.com/TrueSightDAO/go_to_market/pull/170) (Sophia) | ✅ | ☐ |
| PR2 | Segmented first-touch templates + UAT | go_to_market | ✅ [#169](https://github.com/TrueSightDAO/go_to_market/pull/169) | ☐ (UAT pending) | ☐ |
| PR3 | Hosts Circles fast lane + segment/channel readout | go_to_market | ☐ | ☐ | ☐ |

**Note on PR1 (2026-07-19):** Claude opened [#168](https://github.com/TrueSightDAO/go_to_market/pull/168)
implementing PR1 the same turn this plan was committed to `agentic_ai_context` `main`. Sophia
independently pulled the same plan from `main` and shipped an equivalent, functionally-identical PR1
as [#170](https://github.com/TrueSightDAO/go_to_market/pull/170) (idempotent auto-reply logging via a
Gmail label, park-after-2-cycles to `On Hold`), which Gary merged first. #168 was closed as a duplicate
once discovered; #169 (PR2) was rebased onto the post-#170 `main` and merges cleanly (disjoint code
regions — reply-promotion vs. draft-generation). **Lesson for future plans handed off this way:**
committing a roadmap to `agentic_ai_context/plans/*.md` on `main` is the exact surface Sophia watches
per the handoff protocol (`OPERATING_INSTRUCTIONS.md` §"Handoff protocol") — she can pick it up and
start executing even without an explicit `truesight-dao-ping-sophia` trigger, so an interactive session
building the same roadmap in parallel should check `git log` on the target repo before opening each PR,
not just before starting the turn.

---

## 7. Success metrics and rollback

| Metric | Baseline (2026-07-18, this audit) | Target (30 days post PR3) |
|---|---|---|
| Genuine reply rate, general (non-Circles) cohort | 0.3% (1/333) | ≥ 2% |
| `Hosts Circles` cohort human-review turnaround | unmeasured (mixed into general backlog) | same-day |
| DApp Remarks duplicate rows from auto-reply detection | 740 of 750 | 0 new duplicates |
| Rows parked as confirmed dead ends | 0 | matches count of rows crossing the streak threshold (2 known today) |
| New Partnered / Manager Follow-up from the warm-up channel | 0 in 6 weeks | ≥ 1 in 30 days |

**Rollback:** PR1 is purely subtractive (fewer sends, deduped logging) — reverting just restores today's
(worse) behavior, no data loss. PR2's template variants ship behind the same `WARMUP_AUTOSEND_ENABLED`
kill switch as the rest of the auto-send system; a bad variant is caught in UAT before it can reach that
switch. PR3 is additive tooling (sorting + a readout) with no send-path change to roll back.

---

## Changelog

- **2026-07-18** — Plan created from the 2026-07-18 stats deep-dive + full 333-thread Gmail audit
  (see conversation record / DApp Remarks + Email Agent Follow Up data as of that date). PR1 scoped and
  implementation started same day.
