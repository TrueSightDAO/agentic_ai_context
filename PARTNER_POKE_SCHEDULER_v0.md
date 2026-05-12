# Partner Poke Scheduler — v0

Stage 1 of the AI-first vertically integrated supply chain vision Gary
sketched in Beer Hall on 2026-05-12. This file is the plan-as-document
for v0: smallest end-to-end loop that turns the bell's Partner Stock
+ Partner Check-in signals into LLM-drafted poke messages waiting in
Gary's Gmail inbox under a dedicated label, ready for human review
and send.

This file is the **plan**, not the implementation. Per
`MULTI_LLM_ORCHESTRATION.md` §1.2, the plan-as-document comes first
for multi-component builds that span ≥3 repos so the next session
(same model or different) can resume without rebuilding context.
Refresh this file as the implementation lands.

---

## Goal

End-to-end loop that proves the scheduler concept:

1. **Trigger** (cron or on-demand): read Partner Stock + Partner
   Check-in signals — the same data the bell already aggregates.
2. **Filter**: pick the top-N partners flagged by stock/dormancy
   signals AND not poked in the last `MIN_DAYS_SINCE_POKE` days
   (matches the existing `email_agent_drafts.gs` cadence rule).
3. **Generate**: for each flagged partner, call an LLM with focused
   context (partner, reason, recent check-in history) to draft a
   short 2–3 sentence poke message in Gary's voice.
4. **Queue**: create a Gmail draft under label **`AI/Partner Poke`**
   so the draft appears both in the Gmail inbox sidebar and in
   `warmup_review.html` as a fourth cohort tab.
5. **Log**: append a row to a new **`Partner Poke Drafts`** sheet
   tab (mirrors the `Email Agent Drafts` logging pattern), so
   subsequent runs know which partners were poked when.

The operator (Gary) reviews the draft in Gmail or warmup_review,
edits if needed, clicks Send. Standard Gmail send — nothing custom.
After the partner responds (or after Gary checks in offline), Gary
files a Partner Check-in entry via the existing
`partner_check_in.html` flow, which updates cadence for the next
run.

---

## Human-in-the-loop guarantees (hard constraints)

The scheduler never sends anything. It produces drafts only. These
are architectural, not policy — code paths to send are not wired up
in v0:

- **No `GmailApp.send()` call anywhere in v0.** Only
  `GmailApp.createDraft()` followed by `getMessage().createLabel(...)`
  (the same call pattern the existing `email_agent_drafts.gs` uses).
- **No auto Partner Check-in entry on send.** v0 leaves check-in
  filing to the existing manual flow. v0.1 may add auto-checkin
  *after* operator confirms the loop works.
- **Cadence rule prevents re-pokes:** `MIN_DAYS_SINCE_POKE = 7`
  (configurable via Script Properties, matches `email_agent_drafts.gs`).
- **Hard cap per run:** `MAX_DRAFTS_PER_RUN = 5` for v0
  (configurable). Better to have few high-signal drafts than many
  noisy ones.
- **Dry-run mode:** Script Property `DRY_RUN = true` skips Gmail
  draft creation, logs intended drafts to Stackdriver only. Use
  this for the first week of running until trust is calibrated.

---

## Architecture

Three repos touch this change:

```
                  ┌──────────────────────────────────────┐
                  │ tokenomics/google_app_scripts/         │
                  │   holistic_hit_list_store_history/      │
                  │     partner_poke_drafts.gs (NEW)         │
                  │       1. Reads velocity + inventory JSON │
                  │       2. Reads Partner Check-ins tab     │
                  │       3. Filters: flagged + not recently │
                  │          poked + has email on file       │
                  │       4. Calls LLM via UrlFetchApp       │
                  │       5. GmailApp.createDraft + label    │
                  │       6. Append to Partner Poke Drafts    │
                  │          sheet (logging)                 │
                  └──────────────────────────────────────┘
                                  ↓
                  ┌──────────────────────────────────────┐
                  │ tokenomics/google_app_scripts/         │
                  │   holistic_hit_list_store_history/      │
                  │     warmup_review_api.gs (MODIFIED)      │
                  │       Add 'AI/Partner Poke' to the       │
                  │       cohort list returned by            │
                  │       getWarmupReviewQueue               │
                  └──────────────────────────────────────┘
                                  ↓
                  ┌──────────────────────────────────────┐
                  │ dapp/warmup_review.html (MODIFIED)      │
                  │   Add 4th cohort tab 'AI/Partner Poke'   │
                  │   alongside Warm-up / Follow-up /        │
                  │   Prospect Replied                       │
                  │                                          │
                  │ dapp/js/notifications.js (MODIFIED)      │
                  │   getWarmupReviewQueue total includes    │
                  │   AI/Partner Poke count (already does    │
                  │   if the GAS adds it — no code change   │
                  │   needed beyond the sublabel string)     │
                  └──────────────────────────────────────┘
```

---

## Data sources

All read by `partner_poke_drafts.gs`:

| Source                                           | What it provides                                       |
|--------------------------------------------------|--------------------------------------------------------|
| `partners-velocity.json`                         | `partner_name`, `partner_type`, last_sale_date per SKU |
| `partners-inventory.json`                        | `venueInventory` per SKU per partner                   |
| Main Ledger `Partner Check-ins` tab              | Last check-in date + method + notes per partner        |
| Agroverse Partners sheet (`contributor_contact_id` column E) | Canonical contact per partner; maps to an email via the contributor sheet |

For `list_partner_contributors`, the Shipping Planner API already
exposes the mapping via `?action=list_partner_contributors`. The
contributor row in turn carries an email (we'll need to confirm
exactly which column; see "Open questions" below).

---

## The LLM call

**Provider:** Anthropic Claude (default); fall back to OpenAI / DeepSeek
via Script Properties (`LLM_PROVIDER`) if Anthropic credit is depleted
(known incident 2026-05-11). Junior-tier model is enough — the drafts
are 2–3 sentences and the partner context is short. `claude-haiku-4-5`
or `gpt-5-mini` both work.

**Prompt shape (focused, no system bloat):**

```
You are drafting a short, friendly message from Gary at Agroverse to
an existing retail partner who carries our cacao. Your draft will be
reviewed and edited by Gary before sending — do NOT include sign-offs
or pleasantries Gary would naturally add himself.

Context:
- Partner: <partner_name> in <location>
- Carries: <SKUs they stock>
- Current signal: <out of stock | running low (N left) | last sale Xd ago>
- Last check-in: <date> via <method>; notes: <notes>
- Last contact age: <days>

Constraints:
- 2-3 sentences maximum.
- Conversational, not corporate. Don't say "I noticed..." or "I'm
  reaching out to..." — those sound auto-generated.
- Suggest one specific next step (a restock check, a quick call, a
  visit if Gary's in the area).
- Don't include a signature or greeting Gary would add himself.

Output: JSON {"subject": "...", "body": "..."}
```

**Why JSON output:** lets the GAS function easily set the Gmail draft
subject + body separately. Subject defaults to `Quick check-in —
<partner_name>` if the LLM doesn't return one.

**Why Haiku-tier:** matches the
`MULTI_LLM_ORCHESTRATION.md` tiering rule — junior model for
narrow, well-scoped task. Don't pay architect prices for a 2-3
sentence draft.

**API key:** stored as Script Property `ANTHROPIC_API_KEY` (or
`OPENAI_API_KEY`, etc., depending on `LLM_PROVIDER`). Gary adds via
Apps Script Project Settings → Script Properties.

---

## The Gmail draft

Mirrors the `email_agent_drafts.gs` pattern exactly:

```js
var draft = GmailApp.createDraft(toEmail, subject, body, { htmlBody: htmlBody });
// Attach the AI/Partner Poke label
var label = GmailApp.getUserLabelByName('AI/Partner Poke')
            || GmailApp.createLabel('AI/Partner Poke');
draft.getMessage().getThread().addLabel(label);
```

**Label name:** `AI/Partner Poke` (chosen to slot into the existing
`AI/<purpose>` family used by warmup_review.html).

**Body format:** plain text + lightweight HTML wrapper (matches
existing pattern). Footer line includes the protocol version string
`PARTNER_POKE_SCHEDULER v0` so future audits can trace which drafts
came from which scheduler version.

**Recipient:** resolved by joining `partner_id` → `contributor_contact_id`
(via `Agroverse Partners!E`) → contributor email. Skip partners
whose contributor row has no email — log a warning so Gary knows to
backfill.

---

## Run modes

Three ways to invoke `runPartnerPokeDrafts()`:

1. **Manual from Apps Script IDE** — Run button on the GAS file. Best
   for the first runs, lets the operator inspect Stackdriver logs.
2. **Apps Script menu** — install a custom menu in the Hit List
   container so Gary can run from the spreadsheet UI ("Email Agent
   drafts → Partner Pokes").
3. **Daily cron** (v0.1 only — *not* in v0): time-based trigger that
   runs the function every morning. Postpone until v0 has run cleanly
   for a week. Don't automate before trust is calibrated.

---

## Logging

New sheet tab `Partner Poke Drafts` on the **Hit List** spreadsheet
(co-located with the existing `Email Agent Drafts` tab for the cold-
outreach pipeline). Headers:

```
suggestion_id, created_at_utc, partner_id, partner_name, to_email,
gmail_draft_id, subject, body_preview, llm_provider, llm_model,
signal_reason, status, notes
```

`status` enum: `draft_created` | `skipped_no_email` |
`skipped_recent_poke` | `skipped_cap_reached` | `llm_error`.

This sheet is the audit trail. Subsequent runs read it to enforce
`MIN_DAYS_SINCE_POKE`.

---

## What's deferred to v0.1+

Intentionally out of scope for v0 — don't build until v0 ships and
runs cleanly:

- **Daily cron trigger.** Manual runs only in v0.
- **Auto Partner Check-in entry on send.** Operator still files
  check-ins manually via `partner_check_in.html`.
- **Telegram / SMS channels.** Email only in v0. The
  `partner_check_in.html` form already captures `method` per
  contact, so v0.1+ can route drafts to different channels.
- **Multi-language drafts.** English only in v0; v0.1+ adds
  Portuguese for Brazil-side partners (we have those).
- **A/B testing different prompts.** v0 picks one prompt and
  measures qualitative operator feedback before iterating.
- **Cohort-tab UI in warmup_review.html.** Drafts are visible via
  Gmail inbox label + by extending `getWarmupReviewQueue` to include
  the new label. A dedicated tab in `warmup_review.html` is nice to
  have but not blocking — defer until v0.1 if the basic loop works
  via Gmail alone.

---

## Open questions for Gary before implementing

1. **Email source confirmation.** The Shipping Planner
   `list_partner_contributors` action returns
   `{partner_id, contributor}`. Where does the contributor's email
   live — `Agroverse Partners` sheet column ?, the `Members
   Directory` cache, or somewhere else? Need this resolved before
   the recipient resolution logic can ship.

2. **`MIN_DAYS_SINCE_POKE` default.** `email_agent_drafts.gs` uses 7
   days. That's reasonable for existing partners too, but Gary may
   want longer (14? 30?) — these are warm relationships, not cold
   outreach. Default 7 unless operator says otherwise.

3. **`MAX_DRAFTS_PER_RUN` default.** v0 sets 5; operator can raise
   via Script Properties. Worth confirming.

4. **LLM provider preference.** Anthropic Claude Haiku by default,
   but the Anthropic credit-zero incident on 2026-05-11 means Gary
   may want OpenAI or DeepSeek as the primary. Configurable; just
   needs a default.

5. **Cohort tab in warmup_review.html — yes/no for v0?** Easier path
   is *no* — rely on Gmail label visibility. But if the bell's
   notification badge already shows the count (it will, since
   `getWarmupReviewQueue` returns the new label), the operator may
   want to review pokes alongside warmups in the same UI.

---

## Implementation sequence

In priority order, smallest deployable units first:

1. **`partner_poke_drafts.gs`** (new file in
   `tokenomics/.../holistic_hit_list_store_history/`) — modeled on
   `email_agent_drafts.gs`. Includes the LLM call, the partner
   filtering, the Gmail draft creation, the logging. Ship to
   tokenomics repo. **Gary's manual setup:** clasp-push, add
   `ANTHROPIC_API_KEY` (or alternative) to Script Properties,
   create the `Partner Poke Drafts` sheet tab.
2. **Add `'AI/Partner Poke'` to `warmup_review_api.gs`'s cohort list**
   so the bell's count includes it automatically.
3. **(Optional v0.1)** Add 4th cohort tab to `warmup_review.html` —
   only if Gary wants a UI surface beyond Gmail.
4. **Update `DAPP_NOTIFICATION_BADGE.md`** to note that the
   Outbound Review count now includes Partner Pokes.
5. **Run the first batch manually** with `DRY_RUN = true`. Gary
   reads the Stackdriver logs, confirms the drafts look right.
   Flip `DRY_RUN = false`, run again. Real Gmail drafts appear.

---

## Success criteria for v0

v0 is done when:

- [ ] Manual invocation of `runPartnerPokeDrafts()` produces ≤5 Gmail
      drafts under `AI/Partner Poke` label, all addressed to real
      partners with valid emails, with body text in Gary's voice.
- [ ] Each draft is logged in `Partner Poke Drafts` sheet with full
      audit trail.
- [ ] Re-running within 7 days produces zero new drafts (cadence
      rule works).
- [ ] The bell's Outbound Review count automatically includes the
      new partner-poke drafts (no code change needed once the GAS
      surfaces the label).
- [ ] Gary sends one draft (with or without edits) and the partner
      replies. Loop closed.
- [ ] Gary's qualitative reaction: "yes, keep generating these" —
      not "stop, the tone is wrong."

If any criterion fails, log the failure mode in this file's
follow-ups and iterate before moving to v0.1.

---

## Related context

- `DAPP_NOTIFICATION_BADGE.md` — the bell that surfaces the signals
  this scheduler acts on.
- `feedback_check_tracking_before_recommending_action.md` — the
  anti-pattern this scheduler is *risking*. Mitigated by:
  (a) operator-driven cadence (drafts only fire for partners
  already flagged by stock/velocity signals), (b) hard
  `MIN_DAYS_SINCE_POKE` cap, (c) human-in-the-loop send gate.
- `project_partner_check_in_2026-05-12.md` — the surface the
  scheduler reads from and writes back to.
- `tokenomics/google_app_scripts/holistic_hit_list_store_history/email_agent_drafts.gs`
  — the existing cold-outreach draft generator the new GAS function
  mirrors structurally.
- `EDITORIAL_TONE.md` — voice reference for the LLM prompt. The 1:1
  messaging voice is closer to "warm but professional" than the
  long-form blog voice; the prompt explicitly forbids
  auto-generated-sounding phrases.

---

*Plan written 2026-05-12. Refresh as implementation lands; mark
"v0 shipped" when the success criteria all check. Move v0.1+ items
above the deferred line when they get scheduled.*
