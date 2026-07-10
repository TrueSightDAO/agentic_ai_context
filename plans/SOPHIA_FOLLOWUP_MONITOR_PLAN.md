# Sophia Durable Follow-up Monitor — Execution Roadmap (handoff to Sophia)

**Status as of 2026-06-11:** handed off to Sophia — parked GO-ready (see HANDOFF_MANIFEST.md)
**Repo under change:** `truesight_autopilot` (Sophia's OWN codebase)
**Designed by:** Gary Teh + Claude (this conversation) · **Implemented by:** Sophia (autopilot)

> ⛔ **Own-repo gate (non-negotiable):** this is Sophia's own codebase. Sophia **opens PRs
> only and NEVER self-merges `truesight_autopilot` PRs** — a human reviews + merges (the
> Autopilot-Hardening Phase-2 dogfood gate). Every commit carries the
> `Generated-by: Sophia (TrueSight Autopilot)` trailer.

> **RESUME HERE:** PR1 step 1 — the follow-up store (schema + parser + state sidecar).

---

## 1. Why

A chat turn is bounded (180s) and ends when it replies, so when Sophia promises a *future*
or *multi-day* follow-up ("I'll email Matheus, check tomorrow, ping you the day after"),
**nothing keeps that promise** — there is no durable, scheduled, human-reply-aware mechanism.
Proven twice: an AMI finished and she never reported; the Import/Export thread-10 Nota Fiscal
chase would silently die. `watch_and_notify` (already shipped) covers **short, machine-checkable**
ops (AWS/HTTP, ≤1h). This builds the **long / human / multi-day / scheduled** case.

## 2. Design (locked with Gary — see the conversation)

A **durable follow-up registry + a daily comb loop**, where the loop spins up a *full Sophia
turn in the originating thread* when a follow-up's condition strikes.

**Storage split (Gary's call):**
- **Definition** lives in **`OPEN_FOLLOWUPS.md`** (the one backlog), as a fenced, parseable
  block. Closed out *there* on completion/abort (moved to "Recently shipped"/"Resolved").
- **Mutable scheduling state** (`last_checked`, `next_check`, `attempts`, `last_pinged`,
  `status`) lives in a cheap sidecar **`followups/state.json`** the loop owns — so daily
  checks never churn the 1600-line doc / spam PRs.
- **Working context = the thread transcript.** Before each spun-up turn Sophia loads the
  thread's existing transcript (`tg:<chat>:<thread>`), so she has full history **and Gary's
  interjections**. Gary can read along and steer her next pass (his messages queue via the
  per-topic lock/ack already shipped). The sidecar is *only* scheduling bookkeeping.

**Hard invariants (Gary's requirements):**
- **Every follow-up MUST carry a `thread_id`.** `add_followup` refuses without one. The thread
  is simultaneously the *context source*, the *output channel*, and the *steer/abort point* —
  this is the guardrail against silently looping in the background forever.
- **Control surface, all from inside a thread:** **list** (`list_followups`), **steer**
  (interject in the thread → queues), **abort** ("drop this" → `close_followup`, or
  `status: aborted` in the `.md`).
- **On strike → a full Sophia turn in the thread** (Gary's choice over notify-only): she loads
  the transcript + the new evidence, processes with her normal (role-gated) tools, reports in
  the thread. This reuses the per-topic executor lock/queue/ack and the Telegram path — no new
  side-channel. Bounded, visible, abortable.
- **Restart-safe by construction:** the loop is in-process (like `email_poller`) but **stateless**
  — all state is on disk, so a restart just re-combs the durable list and resumes.

**Probes (first two only):**
- `gmail_reply` — reuse `email_poller`'s Gmail service; query for a reply from a named sender
  since the follow-up's `created_at` (optionally subject/attachment match). The Matheus case.
- `elapsed_days` — pure time escalation ("ping on day N regardless").
- (AWS/HTTP probes from `watch_and_notify` can be folded in later — out of scope here.)

**Schema (the `followup` block in `OPEN_FOLLOWUPS.md`):**
```followup
id: matheus-nota-fiscal-aglXX        # stable slug
chat_id: -1003919341801
thread_id: 10                         # REQUIRED
title: Chase Matheus for the Nota Fiscal (AGL-XX)
created_at: 2026-06-11
condition:                            # what "strikes"
  kind: gmail_reply
  from: matheus@…
  subject_contains: Nota Fiscal       # optional
schedule:
  check: daily
  escalate_after_days: 2
  on_escalate: ping_thread
status: open                          # open | resolved | aborted
```

**Lifecycle:**
```
promise → add_followup (writes .md block + sidecar state; REQUIRES thread_id)
  ↓ hourly comb (in-process; restart-safe — state on disk)
  read .md defs + sidecar state → run probe
  ├─ strikes      → spin FULL Sophia turn in thread (load transcript + evidence)
  │                 → she processes + reports → close_followup → move to Resolved in .md
  ├─ escalate day → ping_thread (once; record last_pinged)
  └─ abort (NL in thread / status:aborted) → close out in .md
```

## 3. Pre-flight checklist

- [ ] Confirm `email_poller`'s Gmail service can be reused read-only for a reply query
      (sender + since-date); if its scope is too narrow, note what's needed.
- [ ] Confirm the spun-up turn can reuse the existing per-topic executor lock so a loop-turn
      and a live governor message in the same thread never overlap (they must serialize).
- [ ] Decide the loop's home: extend an existing background loop or a new `followup_loop`
      started in the same lifespan block as `email_poller`/`aws_monitor`.
- [ ] `OPEN_FOLLOWUPS.md` parser must IGNORE all the existing prose entries — only act on
      fenced ` ```followup ` blocks. Never mangle the human backlog.
- [ ] Reaffirm the own-repo gate: open PRs, never self-merge; `Generated-by` trailer.

## 4. Sequenced plan (each PR independently shippable; open PR, human merges)

### PR1 — Store: schema + parser + state sidecar
| Step | Description |
|------|-------------|
| 1 | `app/followups.py` — parse ` ```followup ` blocks out of `OPEN_FOLLOWUPS.md` (leave prose untouched); load/merge `followups/state.json`; `list_open()`, `get(id)`, `upsert_state(id, …)`, `set_status(id, status)` (the last also edits the `.md` block + moves it to Resolved/Aborted). |
| 2 | Atomic state writes (tmp + `os.replace`), like `_log_session`. |
| 3 | Tests: parse a mixed doc (prose + 2 followup blocks) → only the blocks; round-trip state; status change rewrites the block + leaves prose intact; **`thread_id` missing → parse error surfaced, not silently dropped.** |

### PR2 — Tools: add / list / close (+ honesty gate)
| Step | Description |
|------|-------------|
| 1 | `app/tools/followup_tools.py` — `add_followup` (**requires `thread_id`**; derives chat/thread from `ctx.session_id` if omitted; writes the `.md` block + seeds sidecar state; refuses non-Telegram sessions). |
| 2 | `list_followups` — default: all `status: open`, current thread flagged; `--this-thread` filters. Human-readable (title, thread link, condition, next check, attempts, escalation day). |
| 3 | `close_followup` — resolve or abort by id; updates `.md` + sidecar. |
| 4 | **Honesty:** one line in the base system prompt — *"Never promise a future/multi-day/async follow-up unless you've called `add_followup` (which requires a thread_id). Otherwise say you can't reliably auto-chase yet and ask to be reminded."* |
| 5 | Tests: add requires thread_id; add→list shows it; close removes from open; non-Telegram session refused. |

### PR3 — Probes: gmail_reply + elapsed_days
| Step | Description |
|------|-------------|
| 1 | `app/followup_probes.py` — `elapsed_days(followup, now)` and `gmail_reply(followup, now)` (reuse `email_poller` Gmail service; query sender + since `created_at`; optional subject/attachment). Each returns `{struck: bool, evidence: str}`. |
| 2 | Tests: elapsed_days fires only on/after the escalation day; gmail_reply struck/not-struck with a mocked Gmail service; never throws (network error → not struck). |

### PR4 — Comb loop + spun-up turn + escalation + abort
| Step | Description |
|------|-------------|
| 1 | `followup_loop()` (started with the other background loops): hourly, for each open follow-up whose `next_check` is due → run its probe. |
| 2 | **Strike → spin a full Sophia turn IN the thread**: build a seed message (follow-up context + probe evidence + "process and report in this thread"), run it through the SAME per-topic-locked turn path so it serializes with any live governor message; post the reply to the thread. |
| 3 | **Escalation**: on `escalate_after_days` with no strike → `ping_thread` once (record `last_pinged`); don't re-ping. |
| 4 | **Abort**: a governor message recognized as "drop/stop this follow-up" in the thread → `close_followup(aborted)`; also honor a manual `status: aborted` in the `.md`. |
| 5 | Idempotency: update `next_check`/`attempts` each tick; never double-fire; a resolved/aborted entry is skipped. |
| 6 | Tests: due-vs-not-due selection; strike path calls the turn-runner once with the right thread; escalation pings once; aborted/resolved skipped; loop survives a probe exception. |

### PR5 — (rollout) Deploy + UAT — see §6.

## 5. Test plan (unit, per PR)

Pure-unit, no network/boto3/real Telegram: parser (prose ignored, blocks parsed, missing
thread_id surfaced); state round-trip + atomic write; tool arg validation (thread_id required);
probe firing logic (mocked Gmail); loop selection/idempotency/strike-dispatch (mock the
turn-runner + Telegram send). Mirror the existing `tests/test_*` conventions.

## 6. UAT — operator acceptance (Gary runs these in Telegram)

Sophia must demo each before the handoff is "completed". Run from a real topic.

| # | Scenario | Pass criteria |
|---|----------|---------------|
| U1 | **Promise creates a tracked follow-up.** Ask Sophia to do something needing a future check. | She calls `add_followup`; replies that it's tracked; no bare "I'll let you know" without it. |
| U2 | **List.** "What follow-ups are you monitoring?" | Returns the open list with each item's thread; this thread flagged. "…in this thread" filters. |
| U3 | **No thread_id ⇒ refused.** (Force a follow-up with no thread context.) | `add_followup` refuses — never starts a thread-less silent loop. |
| U4 | **Time escalation.** Create a follow-up with `escalate_after_days: 0–1` and no real condition. | Within an hour of due, the loop **pings that thread** once (not repeatedly). |
| U5 | **Gmail strike → autonomous turn.** Create a `gmail_reply` follow-up; send a matching reply. | Loop detects it, **spins a Sophia turn in the thread**, she reports/acts there. |
| U6 | **Abort.** In the thread: "drop that follow-up." | `close_followup`; `list_followups` no longer shows it; the `.md` block → Resolved/Aborted. |
| U7 | **Steer.** Interject mid-chase. | Your message queues (ack) and is taken into the next pass, not dropped. |
| U8 | **Restart-safety.** Restart `truesight-autopilot` mid-window. | The follow-up persists and the loop resumes; nothing lost. |
| U9 | **Completion closes the backlog entry.** Finish the task. | Sophia calls `close_followup`; the `OPEN_FOLLOWUPS.md` block is moved to Resolved with a one-liner. |

**Gate:** handoff is `completed` only after U1–U9 pass and each PR is **merged by a human**
(Sophia opens, never self-merges).

## 7. Rollout

Deploy via the targeted path (`git checkout -B main origin/main` on the box, **no `git clean`**
— `sessions/`+`followups/` must survive), restart `truesight-autopilot`. Then run UAT U1–U9.

## 8. Resume tracker

| Unit | PR opened | Merged (human) | Deployed | UAT |
|------|-----------|----------------|----------|-----|
| PR1 — Store (schema/parser/state) | ☐ | ☐ | ☐ | — |
| PR2 — Tools (add/list/close + honesty) | ☐ | ☐ | ☐ | U1–U3 |
| PR3 — Probes (gmail_reply/elapsed_days) | ☐ | ☐ | ☐ | — |
| PR4 — Comb loop + turn + escalate + abort | ☐ | ☐ | ☐ | U4–U8 |
| PR5 — Deploy + UAT | ☐ | — | ☐ | U9 + full pass |

> **RESUME HERE:** PR1 step 1 — `app/followups.py` (parser + state sidecar). Open a PR; **do
> not self-merge** (human reviews). Report progress in the handoff topic.
