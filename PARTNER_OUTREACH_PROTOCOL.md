# Partner outreach protocol — interim (retail / consignment “yes”)

**Status:** INTERIM **v0.1** — hypothesis until validated on additional Partnered stores.  
**Last reviewed:** 2026-03-27  
**Owner:** Agroverse / TrueSight (human: Gary + AI assist)

**Promotion to v1.0 when:** At least **N** additional Partnered locations follow this playbook with no contradictory evidence (set N when you have baseline volume — e.g. 3–5).

---

## 1. Goal (one sentence)

Move holistic retail leads from **Manager Follow-up** to a clear **consignment / retail yes** on Agroverse ceremonial cacao, with you as the **human in the loop** for every send.

---

## 2. Non-goals

- Fully automated sending without your approval.
- Promising terms we cannot honor (pricing, exclusivity, minimums).
- Using this doc as legal advice; use signed agreements where needed.

---

## 3. Evidence and tooling (ground truth)

| Artifact | Purpose |
|----------|---------|
| **Hit List** (Google Sheet) | Store row: Status, Email, Store Key, notes, dates. |
| **States** tab | Exact allowed `Status`, `Shop Type`, `State` strings for sheet + dapp. |
| **Email Agent Suggestions** tab | **Draft** queue: `gmail_draft_id`, `pending_review`; script `suggest_manager_followup_drafts.py` (mailbox `garyjob@agroverse.shop`). |
| **Email Agent Follow Up** tab | Log of **sent** messages (sync from Gmail). |
| **Email Agent Training Data** tab | Chronological **in + out** mail for **Partnered** stores; use `analysis_notes` for tags. |
| **`market_research/HIT_LIST_CREDENTIALS.md`** | IDs, how to run sync/format scripts. |

When you learn something material, tag the training row and **add one bullet** under §10 Changelog in this file.

---

## 4. Stages and exit criteria (Hit List `Status`)

Document *your* bar for moving a row. Adjust as you learn.

| Stage | Exit criteria (examples — fill with your real bar) |
|--------|-----------------------------------------------------|
| Research | Enough fit to justify outreach. |
| Shortlisted | Queued for contact or visit. |
| Contacted | First message or call logged. |
| **Manager Follow-up** | Visit or staff interaction; **decision-maker path known**; **next action is your follow-up**. |
| Meeting Scheduled | Call/visit on calendar. |
| Followed Up | Ping sent; awaiting reply. |
| Partnered | Verbal or written **yes** on carrying / consignment; onboarding in motion. |

**Manager Follow-up** is the main stage for **drafted follow-up prompts** (see §8).

---

## 5. Cadence and touch pattern (hypothesis)

Fill from training data review:

- **First follow-up after visit:** within ___ days.
- **If no reply:** second ping at ___ days; then ___.
- **Stop / park:** move to **On Hold** with a dated note when ___.

---

## 6. Message principles

Derived from wins (update as `analysis_notes` solidify):

- **Farm-first / relationship:** …
- **Consignment framing:** …
- **Avoid:** …

---

## 7. Artifacts checklist

| Artifact | When to use |
|----------|-------------|
| Short intro + farm link | … |
| Wholesale / consignment terms | … |
| Samples policy | … |

---

## 8. Objections and responses (living table)

| Objection | Approach | Notes / example stores |
|-----------|----------|-------------------------|
| Price | | |
| Shelf space | | |
| Already stocked cacao | | |

---

## 9. Human-in-the-loop follow-up workflow (recommended)

**Objective:** Periodically surface **one suggestion at a time** (or a small batch) so you can **edit, send in Gmail,** and **log** without losing context.

### 9.1 Principles

1. **Draft-only by default** — scripts/agents produce **suggested** subject + body; you send.
2. **Ground in facts** — thread snippets + Hit List fields + this protocol; no invented agreements.
3. **Audit trail** — after send, rely on **Email Agent Follow Up** sync (and optional note on Hit List).
4. **Spaced prompts** — avoid duplicate drafts for the same store on the same day.

### 9.2 Data model (minimal)

**Primary:** Hit List tab **`Email Agent Suggestions`** — one row per proposed touch; the real message body lives in **Gmail as a draft** (see `market_research/HIT_LIST_CREDENTIALS.md`). Optional Gmail **label** on those drafts: **`Email Agent suggestions`** (filter in Gmail like a category).

**Cadence (implemented in `suggest_manager_followup_drafts.py`):** At most **one `pending_review` draft per recipient** (`to_email`). The next draft is allowed only after **≥ N days** (default 7) since the latest **`sent_at`** for that address in **`Email Agent Follow Up`**. After you send, sync the follow-up tab and mark the suggestion **`sent`** so the pipeline stays honest; increase N for softer touch (e.g. 10–14 for 2nd+ follow-up — optional future enhancement).

Optional columns **on Hit List** later (if you want eligibility rules without scanning suggestions):

| Column | Use |
|--------|-----|
| `next_followup_not_before` | Date; script only suggests if **today ≥** this. |
| `last_draft_prompt_utc` | When a draft was last generated (avoid spam). |

Until those exist, scripts can use **defaults** (e.g. eligible = Manager Follow-up + Email + no pending suggestion for that `store_key` — configurable).

### 9.3 Script / agent flow (phased)

**Phase A — Today (no LLM required)**  
- Scheduled **calendar reminder** or weekly habit: run a script that prints the next **N** Manager Follow-up stores with Email + last sent date + link to Gmail search.  
- You draft in Gmail using **§6–8** and **training examples**.

**Phase B — Gmail draft + `Email Agent Suggestions` tab (preferred)**  
- Script: **`market_research/scripts/suggest_manager_followup_drafts.py`**:  
  - Read Hit List (**Manager Follow-up** + Email + shop + notes).  
  - Optional **`--use-grok`**: fetch **full** Gmail thread bodies (plain/HTML) for that address, cap size, call **Grok** (`GROK_API_KEY`) for JSON subject/body; otherwise use the built-in template + snippets.  
  - **Create** `drafts.create` in Gmail (To/Subject/Body). Optionally apply label **`Email Agent suggestions`**.  
  - **Append** one row to tab **Email Agent Suggestions** (`gmail_draft_id`, `subject`, `body_preview`, `status=pending_review`, etc.).  
- You **open Drafts** (or filter by label), edit if needed, **Send**.  
- Run **`sync_email_agent_followup.py`** so **Email Agent Follow Up** logs the sent message; update suggestion row `status` to `sent` (manually until a small reconciler exists).

**Phase C — LLM-assisted (optional)**  
- Same as B but body/subject generated via API (e.g. Grok) with **system prompt** = condensed §4–8 + store facts; **must** show citations (last message date, quoted phrase).  
- Still **no auto-send** unless you add an explicit `--send` later (not recommended initially).

### 9.4 Where prompting happens

| Channel | Pros | Cons |
|---------|------|------|
| **Terminal + Markdown file** | Simple, gitignored output OK | Easy to ignore |
| **Gmail Draft + `Email Agent Suggestions`** | Native send flow; label filters like a category | Needs draft-creation script |
| **New Sheet tab (body only)** | Visible on phone | Duplicates Gmail; easy to drift out of sync |
| **Cursor / AI session** | Rich editing | Ephemeral unless you save |
| **Email to yourself** | Hard to miss | Another inbox |

**Recommendation:** **Phase B** — **Gmail draft** as source of truth for the message, **Sheet tab** for queue metadata, optional label **`Email Agent suggestions`**. Add a **calendar reminder** if you want a nudge separate from Gmail.

### 9.5 Safety checks before any future auto-send

- Written **opt-in** from you per message or per week.
- **Max recipients** per run.
- **BCC yourself** on first automated send tests (if ever).

### 9.6 Optional: daily GitHub Action + Google Calendar as the “inbox”

This matches the idea: **the calendar event carries the proposed email**; **you signal approval**; **the next scheduled run sends** via Gmail. The thing that “runs again” is the **GitHub Action** (or a small VM), not an ad-hoc Cursor session.

#### Is it viable?

**Yes** for a **personal Google account**, using **OAuth** (refresh token + client id/secret) stored as **GitHub Actions secrets**. Operational cost: re-auth if the refresh token is revoked, scope changes, and careful secret hygiene.

**Caveats**

| Topic | Detail |
|--------|--------|
| **Auth** | Calendar event creation + Gmail send require **user** OAuth (not the Hit List **Sheets** service account). Add something like `https://www.googleapis.com/auth/calendar.events` to the same OAuth client you use for Gmail, regenerate **refresh token**, store as repo secrets. |
| **GitHub** | Use a **private** repo, branch protection, and secrets named e.g. `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN`. |
| **Idempotency** | After send, **mark the event** (title prefix `SENT:`, or private extended property `sentAt=…`) so duplicate runs never double-send. |
| **Approval signal** | There is no universal “approve email” flag. Practical options: **(A)** you add a line at top of description: `SEND_APPROVED` (easy to inspect), **(B)** you **Accept** the invite and the job checks attendee `responseStatus === "accepted"` (verify with your calendar client), **(C)** a Sheet row the event META block points to (`approved=TRUE`). Combining **A + META store_key** is usually clearest. |
| **Description length** | Keep full thread history out of the event; use snippets + Sheet links. |
| **Security** | Anyone who can change `.github/workflows/` and get a run can misuse secrets. Treat the workflow as production code. |

#### Two-phase schedule (same repo, one or two workflow files)

**Job 1 — Daily “prompt” (e.g. morning)**  

1. Read **Manager Follow-up** + Email from Hit List.  
2. Pick the next lead (rules TBD: oldest follow-up, round-robin, etc.).  
3. Pull recent Gmail thread context.  
4. Build **SUBJECT** + **BODY** (template first; LLM optional).  
5. **Insert** a Calendar event: title e.g. `[Agroverse follow-up] {shop_name}`, short time slot, **description**:

   ```text
   META store_key=... hit_list_row=... to=partner@store.com protocol=v0.1
   ---
   SUBJECT: ...
   ---
   BODY:
   ...
   ```

**Job 2 — Daily (or hourly) “send approved”**  

1. List events with your **pending** marker (title prefix / extended property) **and** not yet `SENT`.  
2. Parse description; require **explicit approval** (your rule).  
3. Call Gmail `users.messages.send` (or raw RFC 2822).  
4. Mark event **sent**; optional Sheet log; rely on **Email Agent Follow Up** sync for history.  
5. Cap sends per run (e.g. 1–3).

Skipping a day: if you do not approve, Job 2 does nothing; Job 1 can avoid stacking multiple pending events per store (check calendar first).

#### Simpler stepping stone (aligned with §9.3 Phase B)

**Automation ends at Gmail `drafts.create`**, with a row on **`Email Agent Suggestions`** and optional label **`Email Agent suggestions`**. You tap **Send** in Gmail—no Calendar approval state machine. Calendar remains optional for mobile prompts only.

#### Implementation sketch

Script(s) under `market_research/scripts/`, workflow `.github/workflows/followup_prompt.yml` with `schedule` + `workflow_dispatch`. Never commit tokens.

---

## 10. Changelog (interim)

- **2026-03-27** — v0.1 created. Linked training tab + Hit List workflows. §9 outlines phased HIL follow-up; Phase B script not implemented yet.
- **2026-03-27** — §9.6: GitHub Actions + Google Calendar as approval carrier; two-phase cron; secrets and idempotency; Gmail-draft simpler path.
- **2026-03-27** — Primary HIL path: Gmail **draft** + Hit List tab **Email Agent Suggestions** + optional label **Email Agent suggestions**; §9.2–9.4 updated. Scripts: `ensure_email_agent_suggestions_sheet.py`, `format_email_agent_suggestions_sheet.py`.

---

## 11. Link index

- Dapp (stores): https://dapp.truesight.me/stores_nearby.html  
- Hit List: see `market_research/HIT_LIST_CREDENTIALS.md`  
- Gmail OAuth: `agentic_ai_context/GMAIL_OAUTH_WORKFLOW.md` (if present) or `market_research/credentials/gmail/README.md`
