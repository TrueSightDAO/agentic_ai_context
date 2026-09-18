# Telegram governor mention-gate — silent drops under load

**Status:** parked — bug identified via log archaeology; not yet investigated at the
code/runtime level. No PR yet. Not a §5c gate — safe to pick up any time, no governor GO needed
to start investigating.

## Symptom

Gary Teh (governor) sent unmentioned Telegram messages in two active topics on 2026-09-18 that
produced **zero response and zero log trace**, and only went through after an explicit
`@truesight_autopilot_bot` mention on a resend. This contradicts the intended design: governor
messages are supposed to bypass the group mention-gate entirely (`_sender_is_governor()` in
`truesight_autopilot/app/telegram_adapter.py`, the "2026-09 UX fix" documented inline at
~line 693).

## Evidence

Verified live via `sudo journalctl -u truesight-autopilot` on the autopilot box (`ssh sophia`)
cross-referenced with `claude_telegram_monitor/messages.jsonl`, on 2026-09-18 ~01:10–01:23 UTC:

- **Thread 31905** ("Black King NF-e ↔ in-transit crosswalk"), chat `-1003919341801`:
  - msg 32480 @ 01:12:52 UTC, unmentioned: *"If anything is to Taraval street in the Nota fiscal
    it is actually landing at Val Lapidus location"* → **no `CHAT REQ` log entry ever created.**
  - msg 32499 @ 01:16:16 UTC, identical text, still unmentioned → **also never dispatched.**
  - msg 32504 @ 01:18:04 UTC, same text + explicit `@truesight_autopilot_bot` → dispatched
    immediately (`CHAT REQ [298619]` logged 01:18:18). This eventually became agentic_ai_context
    PR #1271 (merged) — so the content landed, just three tries and 5+ minutes later than it
    should have.
- **Thread 30026** ("CFR partnership"), same chat:
  - msg 32500 @ 01:16:22 UTC, unmentioned: *"Deploy to GAS"* → **no `CHAT REQ` log entry.**
  - msg 32510 @ 01:20:12 UTC, resent as *"@truesight_autopilot_bot deploy GAS"* — outcome not
    confirmed at time of writing; the worker was still mid-turn on an unrelated third topic.
- **Contrast:** dozens of other unmentioned governor messages in the *same two threads, same
  session, same evening* dispatched normally (e.g. "status?", "Go", "Merge P4", "Deploy",
  "Promote", "sync to prod" — all unmentioned, all worked). So this is **not** a wholesale
  regression of the governor bypass — it's an intermittent failure under some specific condition,
  which makes it easy to miss and annoying to reproduce on demand.

## Working theory (unconfirmed — needs code-level verification, not just log absence)

- The service is single-worker (documented precedent: `truesight_autopilot` PR #480 postmortem,
  `sophia_manual_restart_freezes_threads` — one blocking call anywhere freezes ALL threads). At
  the time of both drops, the worker was confirmed busy on a **different, concurrent topic's
  turn** — live-verified at 01:22:48 UTC it was mid-turn on a third, unrelated topic (a GAS
  `Credentials.js` secrets scan, no `thread_id` in the Telegram context at all).
- `_sender_is_governor()` (telegram_adapter.py, ~line 686) wraps `resolve_identity()` in a bare
  `except Exception: return False`, with **no logging on either branch**. A governor-bypass
  failure and a genuine non-governor sender are indistinguishable from the logs.
- The gate's own "log as observed" fallback (`log_observed_message()`, ~line 713) **only fires
  when `public_key is not None`**, and even then it's a best-effort POST to `/chat/observe` with
  `logger.warning` only on *failure* — nothing logs success either. So a gated message leaves
  **zero trace regardless of which way the gate check went.**
- Plausible mechanism: under single-worker load, `resolve_identity()`'s Column-X binding lookup
  (a network/Sheets call — step 1, the env-allowlist check, is offline and shouldn't be affected)
  times out or throttles, falls through toward `Role.GUEST`, and the message gets silently gated.
  **This is a hypothesis, not a confirmed root cause** — no code path was actually traced live
  this session, only inferred from the absence of a `CHAT REQ` log line.

## What actually needs to happen (investigation, likely 1 PR once root-caused)

1. Add logging at the gate-decision point (`telegram_adapter.py` ~2066–2079) that states, per
   incoming message: mentioned? governor? thread-locked? always-respond? and the final verdict —
   so this stops being undiagnosable after the fact.
2. Add a log line inside `_sender_is_governor()`'s `except` branch (what exception, if any) and
   on `resolve_identity()`'s network-lookup path (timeout vs. genuine non-match vs. success).
3. Once instrumented, reproduce under load (or catch the next live occurrence) to see which
   branch actually fired for the two dropped messages above.
4. Fix whatever the instrumentation reveals — likely a `resolve_identity()` timeout/caching fix,
   or (if it turns out to be something else, e.g. a queuing/coalescing bug unrelated to the gate
   itself) whatever that turns out to be. Don't assume the working theory above is correct before
   the logging confirms it.

## Not urgent / not a gate

This is a UX/diagnosability bug, not data loss or money movement — the workaround (tag
`@truesight_autopilot_bot` when nudging a thread that's visibly busy) is safe and already in use.
No governor GO needed to start; opening PRs against `truesight_autopilot` for logging/fixes is a
normal code change, not a §5c always-stop gate.

## RESUME HERE

Not started. First unit: add the diagnostic logging described above (steps 1–2), land it, then
go collect a live repro before attempting a fix.
