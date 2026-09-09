# Sophia — hourly admin+sophia@truesight.me inbox watch

## Background

Gary wants Sophia to check `admin+sophia@truesight.me` roughly once an hour and act on
it, not just leave mail sitting unread:
- Routine mail: she should handle it herself, including sending replies — no human
  approval needed.
- Budget / inventory-movement mail: she should still act, but CC
  `garyjob@agroverse.shop` on her reply in the same thread so he's looped in and can
  respond in-thread.

### What already exists (pre-flight)

- `app/email_poller.py` — an existing 5-minute loop, but narrowly hardcoded to
  GitHub-failure / GAS-error / security-alert / Bugsnag emails, each with a fixed
  auto-fix action (`FixAgent`). Not a fit for general inbox judgment calls — don't
  extend it, it's a different concern.
- `app/tools/gmail_tools.py` already has everything needed as ordinary tool-callable
  functions: `gmail_search`, `gmail_read_message`, `gmail_send(to, subject, body,
  account=None, cc=None, bcc=None)`, `gmail_create_draft(...)`. Multi-account via
  `GMAIL_TOKENS_DIR` (`account` param) — confirm which token file maps to
  `admin+sophia@truesight.me` (plus-alias into the shared `admin@truesight.me`
  inbox, same pattern as `admin+envoy@`, `admin+claude@` — likely resolves via the
  existing `admin` token, filtered by `to:admin+sophia@truesight.me` in the search
  query, since plus-aliases share one mailbox).
- `app/followups.py` is NOT a generic periodic-task runner — it's purpose-built to
  parse/track `OPEN_FOLLOWUPS.md` blocks. Don't repurpose it; write a small
  dedicated loop instead, structurally mirroring `email_poller.py`'s
  `run_loop`/`poll_once` shape (own asyncio loop, own interval, started alongside
  the other background loops at app startup).

## Target design

A new hourly loop that, instead of hardcoded rule-based classification, hands each
unread `admin+sophia@` message to Sophia's own reasoning (same model/tool loop that
handles Telegram turns) so she can judge routine-vs-budget/inventory herself and act
with her full tool access (read the thread, search context if needed, decide, send).

1. **Trigger**: new `app/email_inbox_watch.py`, `run_loop(interval_seconds=3600)`,
   started in `main.py` alongside the other background loops (context sync, AWS
   monitor, follow-up loop). Each tick:
   - List unread mail via `gmail_search` scoped to `admin+sophia@truesight.me`
     (query e.g. `to:admin+sophia@truesight.me is:unread`).
   - For each unread thread, dispatch one internal chat turn (reuse
     `_chat_blocking_turn` or an equivalent internal-call path — NOT a real
     Telegram message) carrying the email's subject/sender/body and the SOP
     instruction below as the user-turn content.
   - Use a **stable session id** per email thread (e.g.
     `email:{gmail_thread_id}`) so a reply-heavy thread accumulates context across
     ticks instead of re-litigating from scratch, and so she doesn't double-reply
     to the same thread on the next hourly tick (check thread state / whether she
     already replied before acting again).

2. **The SOP instruction** (baked into the internal turn's prompt, not a rigid
   keyword filter):
   > You're checking admin+sophia@truesight.me. Read this email. If it's routine —
   > general correspondence, routine confirmations, non-financial questions — reply
   > yourself via gmail_send, no approval needed. If it relates to **budget or
   > inventory movement** (purchase orders, invoices, expense approvals, shipment/
   > inventory transfers, budget requests, financial commitments) — still reply,
   > but CC garyjob@agroverse.shop on the SAME thread (In-Reply-To / References
   > headers preserved, not a new email) so he's looped in and can respond in-thread.
   > When genuinely unsure which bucket it's in, treat it as budget/inventory (CC
   > Gary) — err toward looping him in, not silently deciding alone.

3. **Idempotency**: track per-Gmail-thread "already handled this cycle" state (a
   small local state file, mirroring `followups.py`'s `_load_state`/`_write_state`
   pattern) so a thread that's still unread only because Gary hasn't replied yet
   doesn't get re-processed/re-replied every hour.

4. **Dry-run first**: `settings.dry_run` gate, same convention as
   `email_poller.py` — log the intended classification + reply instead of sending,
   verify against real inbox traffic for at least one full day before flipping live.

## Sequenced plan (one PR per turn, §5a)

| # | Unit | Notes |
|---|------|-------|
| 0 | Confirm which Gmail token/account resolves `admin+sophia@truesight.me` mail (read-only check, no code) | Pre-flight completeness — must confirm before writing the search query |
| 1 | `app/email_inbox_watch.py` — loop skeleton + Gmail unread listing + dry-run logging only (no sends yet) | PR — safe, observable, no live behavior change |
| 2 | Wire the internal chat-turn dispatch (SOP prompt) + per-thread state tracking, still dry-run | PR — validate classification quality on real inbox traffic before enabling sends |
| 3 | Flip `dry_run=False` for this loop specifically (or confirm the global flag covers it) once Gary's reviewed a day of dry-run logs | Gate — needs Gary's explicit go, this turns on autonomous sending |
| 4 | Start the loop in `main.py` alongside the other background loops; deploy | PR |

**RESUME HERE: Unit 0.**

## UAT

1. Send a test routine email to `admin+sophia@truesight.me` → within the hour, she
   replies from that address, no CC, sensible content.
2. Send a test budget/inventory-flavored email (e.g. "please approve this PO for
   200kg cacao") → she replies in-thread with `garyjob@agroverse.shop` CC'd.
3. Confirm a thread she already replied to does NOT get a duplicate reply on the
   next hourly tick.
4. Confirm dry-run mode produces a clear log of what it *would* have sent, with the
   routine/budget classification stated, before Gary approves flipping it live.
