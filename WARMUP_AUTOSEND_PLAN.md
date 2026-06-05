# Warm-up Auto-send Plan — Reallocating Human Attention in B2B Outreach

**Status:** APPROVED — execution in progress
**Date:** 2026-06-05
**Owner:** Gary Teh (human) + Claude Code (AI assist)
**Repos affected:** [TrueSightDAO/go_to_market](https://github.com/TrueSightDAO/go_to_market) (implementation), [TrueSightDAO/agentic_ai_context](https://github.com/TrueSightDAO/agentic_ai_context) (this plan)
**Related docs:** `HIT_LIST_STATE_MACHINE.md` (the 13-state pipeline this modifies), `PARTNER_OUTREACH_PROTOCOL.md` §9 (the human-in-the-loop convention this graduates from), `EMAIL360.md` (the DTC retention-loop sibling — this plan covers the **B2B outbound** loop)

---

## TL;DR (for the Beer Hall)

We studied 60 days of Agroverse retail-partner outreach data and found the human
bottleneck is in the wrong place. Gary spends his outreach time clicking "send"
on AI-drafted first-touch emails — 98 of which are currently waiting a **median
24 days** for that click — while the rare prospects who actually *reply* wait
**29 hours median (worst case 10 days)** for his response. The replies are where
partners come from: all 14 current retail partners trace back to a human
conversation, not a first-touch email.

**The change:** the AI now sends the routine, machine-checked first-touch emails
itself (drip-fed, capped per day, kill-switched), and Gary's attention is
redirected to the moment a human replies — every reply gets an AI-drafted
response within the hour for him to edit and approve. Nothing a prospect writes
is ever answered by an unattended machine.

**Why DAO members should care:** same human hours → more genuine partner
conversations per week → faster Agroverse retail expansion → more cacao moving
→ more trees planted. And the playbook is reusable for any DAO outreach surface.

---

## 1. Assessment — what the data says

### 1.1 Why now

Three artifacts surfaced on 2026-06-05 that prompted the audit: two AI-automated
cold-pitch email sequences received at DAO inboxes (burner domains, rotating
fake personas, a reply-handling bot that answered a buying signal with the
single word "No"), and a Stanford GSB clip of Ken Griffin arguing AI has erased
the outbound-scale moat — his example being a 25-year-old who used
signal-triggered, AI-personalized outreach to build a pet-insurance business
that sold for $1B. The spam specimens demonstrate the failure mode: **they
automated the cheap part (sending) and abandoned the prospect at the expensive
part (the reply)**. The Griffin clip demonstrates the prize: the differentiator
is signal quality and reply handling, not send volume. Our pipeline had the
inverse problem — excellent reply handling (when it happens) but a human gate
throttling the cheap part.

### 1.2 Pipeline state (Hit List workbook, 2026-06-05)

| Metric | Value |
|---|---|
| Hit List rows total | 669 across 14 states |
| Rows in `AI: Warm up prospect` (ready for first touch) | 79 |
| Rows in `Manager Follow-up` | 34 |
| Partnered | 14 |
| Drafts generated (Email Agent Drafts, all time) | 470 — 183 sent / 189 discarded / **98 pending_review** |
| Pending-review backlog age | **median 24 days** (74 warm-ups, 24 follow-ups) |
| Send pattern | bursty — 93 sends on Sun 2026-05-03, 74 on Fri 2026-04-24 (weekend batch sessions) |
| Draft→send latency (sent cohort) | median 1.1 d, **p75 = 12 d**, max 30 d |

### 1.3 Engagement ground truth (Gmail thread audit, 232 sent threads)

| Metric | Value |
|---|---|
| Genuine prospect replies (tracking-tool noise removed) | **14 ≈ 6%** — healthy for cold B2B |
| Replies that were real opportunities | 3 — one shop asked for samples (shipped), one live wholesale conversation, one became a **Partnered** store |
| Gary's response latency to genuine replies | **median 28.8 h, max 239 h** |
| Response latency on the thread that converted to Partnered | **0.1–1 h** |
| Copy quality complaints in any reply | **0** (worst feedback: a constructive "show product photos on your site") |

The pixel-based "97% open rate" is discounted — Apple Mail / Gmail proxy
prefetch fires tracking pixels without a human open. Replies are the only
ground truth.

### 1.4 Verdict

1. **The send-click is the pipeline bottleneck.** Cron jobs qualify, enrich,
   and draft 24/7; everything then queues on a weekend batch session.
2. **Human attention is mis-allocated.** ~94% of sends never get a reply — yet
   they consume the operator's review time, while the 6% who raise their hand
   wait days. The fastest-handled reply became a partner; the slowest soft-no
   sat 10 days.
3. **The graduation criterion was already met.** `HIT_LIST_STATE_MACHINE.md`
   (operator review loop) defined the test: *"If reply rate stays healthy AND
   no pattern of bad copy in the lint-reviewed sample, that's the signal to
   drop the unflagged tier to fully auto-send."* Reply rate ~6%, bad-copy
   complaints zero. The evidence gate is cleared.
4. **Burst sending is itself a risk.** 93 sends in one day from one Gmail
   account is a deliverability gamble; a daily drip is safer and produces a
   steady, manageable reply flow instead of reply pile-ups.

**Principle adopted: allocate human attention by demonstrated prospect intent,
not by pipeline stage.**

---

## 2. Design principles and guardrails

1. **Auto-send only the machine-checked tier.** A draft auto-sends only if the
   12-rule linter (`preview_warmup_drafts.py`) raises **zero red and zero
   yellow flags**. Flagged drafts stay in the human review queue exactly as
   today.
2. **Replies are always human-approved.** Automation may *draft* a response and
   *notify*, never send one. (Lesson from the spam specimens: the moment of
   engagement is precisely where unattended automation destroys deals.)
3. **Drip, don't burst.** Default cap 12 sends/day, weekdays, business hours
   (Pacific). Protects sender reputation and smooths reply load.
4. **Kill switch + dry-run default.** Repo variable `WARMUP_AUTOSEND_ENABLED`
   gates the workflow; the script defaults to `--dry-run` and only sends with
   explicit `--execute`.
5. **Full audit trail.** Every auto-send flows through the existing
   `sync_email_agent_followup.py` reconcile (status flip, label swap
   `AI/Warm-up` → `AI/Sent Warm-up`, `Email Agent Follow Up` log row), so the
   sent history is indistinguishable in structure from human sends.
6. **Anti-patterns we will never adopt** (from the specimens): rotating fake
   personas, lookalike burner domains, contradictory canned answers,
   abandoning a thread after a warm reply, volume masquerading as
   qualification.
7. **First touches and cadenced no-reply follow-ups only.** Anything after a
   prospect speaks is human territory.

---

## 3. Implementation plan — sequenced PRs on `go_to_market`

### PR1 — Auto-send the linter-clean warm-up tier

New `scripts/send_clean_warmup_drafts.py`:

- Reads `Email Agent Drafts` rows `status='pending_review'`,
  `gmail_label='AI/Warm-up'` (same selection as `preview_warmup_drafts.py`).
- Reuses the existing `_lint()` rules and adds one new **red** rule:
  `email_domain_mismatch` — recipient is on a custom (non-freemail) domain that
  differs from the Hit List `Website` domain. (Catches the observed misfire
  where a warm-up went to a shop's *marketing agency* inbox.)
- Clean tier = zero red **and** zero yellow flags. Everything else is skipped
  and left for the human review loop.
- Sends via Gmail API `drafts().send()` (the draft already exists in the
  operator's mailbox — sending preserves thread, attachments, and labels).
- Caps sends per run (`--max-sends`, default 12), oldest first;
  optionally `--require-hosts-circles no` to exclude high-leverage AW=Yes
  prospects from auto-send (default: AW=Yes drafts are **excluded** — they get
  human eyes, consistent with the linter's blue flag).
- After sending, invokes the `sync_email_agent_followup.py` reconcile path so
  status/labels/log update in the same run.
- `--dry-run` default prints the would-send list with lint results.

New workflow `.github/workflows/warmup_autosend.yml`:

- `schedule`: weekdays 17:05 UTC (≈ 9 am PT) + `workflow_dispatch`.
- Gated on repo variable `WARMUP_AUTOSEND_ENABLED == 'true'`.
- Secrets: `GOOGLE_CREDENTIALS_JSON`, `GMAIL_TOKEN_JSON` (both already exist on
  the repo for sibling workflows).
- `concurrency` group to prevent overlapping runs.

### PR2 — Reply acceleration: auto-draft + notify

New `scripts/draft_prospect_reply_responses.py`:

- Detects genuine inbound replies on warm-up / follow-up threads (reuses the
  detection logic in `backfill_warmup_reply_remarks.py`; filters tracking-tool
  noise such as Mailsuite reminder messages).
- For each new reply with no existing response draft: builds full context
  (thread history, Hit List row, DApp Remarks) and generates a Grok-drafted
  reply **in-thread** as a Gmail draft, labeled `AI/Reply-Draft`.
- Sends a notification email to the operator (subject:
  `[Reply] <shop> — <one-line gist>`; body: the prospect's message, the draft
  text, a Gmail deep-link) so the median human response drops from ~29 h to
  same-session.
- Idempotent on Gmail `message_id` (a processed-marker via the existing DApp
  Remarks audit pattern).

Workflow `reply_draft_responses.yml`: hourly, same secrets + `GROK_API_KEY`.

### PR3 — Reply classification + soft-no auto-parking

New `scripts/classify_warmup_replies.py`:

- LLM-classifies each genuine inbound reply into:
  `interested | question | soft_no_with_date | soft_no | hard_no |
  wrong_contact | referral`.
- Automatic Hit List updates for the unambiguous negatives:
  - `soft_no_with_date` ("reach out in September") → Status
    `Deferred / Revisit later` + `Follow Up Date` set from the parsed date.
  - `hard_no` ("we are not interested") → Status `Rejected`.
  - `referral` (named alternative shops) → referred names appended to
    `Sales Process Notes` for discovery triage.
- `interested` / `question` / ambiguous → untouched (they ride PR2's
  notification path).
- Every classification writes a `DApp Remarks` audit row with the model
  rationale, using the shared `hit_list_dapp_remarks_sheet.py` apply-semantics.

Runs inside PR2's hourly workflow (classification informs the notification
subject line).

---

## 4. Pre-flight checklist

- [x] Gmail user OAuth token valid with `gmail.modify` (verified 2026-06-05)
- [x] Linter + clean-tier definition exists (`preview_warmup_drafts.py`)
- [x] `reconcile_drafts_status_to_sent()` exists (`sync_email_agent_followup.py`)
- [x] Evidence gate met (reply rate ~6%, zero copy complaints — §1.4)
- [x] Repo secrets present on `go_to_market`: `GOOGLE_CREDENTIALS_JSON`,
      `GMAIL_TOKEN_JSON`, `GROK_API_KEY` (used by sibling workflows)
- [ ] Repo variable `WARMUP_AUTOSEND_ENABLED` created (set `true` to arm; PR1
      ships with the variable unset = disarmed)
- [ ] Operator confirms daily cap (default **12**) and AW=Yes exclusion default
- [ ] First armed run observed end-to-end (manual `workflow_dispatch`)

---

## 5. Execution roadmap — resume tracker

> **RESUME HERE →** PR1 (auto-send script + workflow) is the first unfinished
> unit. Update this table as units land; report the DAO contribution after each
> merge before starting the next (per `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`).

| Unit | Scope | Repo | Merged | Contribution reported |
|---|---|---|---|---|
| PR0 | This plan (md + pdf) | agentic_ai_context | ☐ | ☐ |
| PR1 | `send_clean_warmup_drafts.py` + `warmup_autosend.yml` + `email_domain_mismatch` lint rule | go_to_market | ☐ | ☐ |
| PR2 | `draft_prospect_reply_responses.py` + notification + hourly workflow | go_to_market | ☐ | ☐ |
| PR3 | `classify_warmup_replies.py` + soft-no auto-parking | go_to_market | ☐ | ☐ |
| Post | Arm `WARMUP_AUTOSEND_ENABLED`, observe first run, drain 98-draft backlog | operations | ☐ | — |

---

## 6. Success metrics and rollback

| Metric | Baseline (2026-06-05) | Target (30 days) |
|---|---|---|
| Pending-review backlog age (median) | 24 days | < 2 days |
| Draft→send latency (p75) | 12 days | < 3 days |
| Operator response latency to genuine replies (median) | 28.8 h | < 4 h |
| Genuine reply rate | ~6% | ≥ 5% (must not degrade) |
| Bounce / spam-complaint rate | ~0 | 0 sustained |
| Genuine partner conversations per week | ~1 | 3+ |

**Rollback:** set `WARMUP_AUTOSEND_ENABLED=false` (instant, no deploy);
drafts simply accumulate in the human review queue as they do today. PR2/PR3
are read-and-draft only — disabling their workflow restores the status quo.

**Watch item:** if the auto-sent cohort's reply rate falls materially below the
human-reviewed cohort's, re-tighten the clean-tier definition (e.g. require
`Hosts Circles` crawl freshness, or re-include yellow flags as blockers) before
resuming.

---

## Changelog

- **2026-06-05** — Plan created from the outreach-data audit (470 drafts, 232
  thread Gmail audit). Approved by Gary same day; execution started.
