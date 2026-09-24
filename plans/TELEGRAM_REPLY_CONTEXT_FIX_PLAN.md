# Telegram Reply-To Context Loss — Root Cause + Fix

**Status:** root-caused, plan drafted, not yet triggered. No code yet.
**Owner:** Gary Teh · **Drafted by:** Claude Anthropic (Envoy), 2026-09-24.
**Requested by:** Gary Teh, relaying a finding from the `supervisor` Envoy session: *"a real infra
gap found — Telegram reply_to metadata isn't reaching her box, so when Gary replies to a specific
photo, she loses that context (second occurrence)."*

**Note on "second occurrence":** neither this nor a prior occurrence is filed anywhere in
`OPEN_FOLLOWUPS.md`, `CONTEXT_UPDATES.md`, or `handoffs/active_supervision.json` (checked directly,
not assumed) — this appears to have only ever been observed live and mentioned in chat, never
written down. PR3 below closes that gap so a third occurrence doesn't repeat un-tracked.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**
> Report the DAO contribution after each merge (§6).

---

## 1. Pre-flight — root cause, captured precisely (§5d)

### 1.1 The gap, confirmed by reading the live code (not assumed from the symptom)

`truesight_autopilot/app/telegram_adapter.py` reads `reply_to_message` from an incoming Telegram
update in exactly **two** places, and neither forwards its content anywhere:

- **Line 615–616** (`_bot_was_mentioned()`): reads `reply_to.get("from").username` **only** to check
  whether this message is a reply to one of the bot's *own* messages — used purely for the group
  mention-gate bypass (§ "is this directed at her"). The replied-to message's actual **content**
  (text/caption/photo) is never read here.
- **Line 1972**: checks `reply_to_message.get("forum_topic_created")` — an unrelated check for
  detecting a topic-creation system message, not user reply content.

**Nothing in the codebase ever reads `reply_to_message.text`, `.caption`, or `.photo`.** So when Gary
replies to a specific photo (or any prior message), Telegram's own API hands the bot that message's
full content in `reply_to_message` — the bot simply never looks at it beyond the two narrow checks
above.

### 1.2 Where the fix goes — the exact insertion point

The main message handler builds `dispatch_text` (the string actually sent onward to the LLM) through
a sequence of bracketed-context prefixes, all in one place, lines 2200–2218:

```python
dispatch_text = _strip_bot_mention(msg, text) if not is_voice else text
raw_user_text = dispatch_text
...
dispatch_text = _handoff_prefix(thread_id, dispatch_text) + dispatch_text
...
    dispatch_text = f"[Telegram context: chat_id={chat_id}, thread_id={thread_id}] {dispatch_text}"
else:
    dispatch_text = f"[Telegram context: chat_id={chat_id}] {dispatch_text}"
```

This is the **same established pattern** already used for `[GOVERNOR_IDENTITY: ...]` (`main.py`,
multiple call sites) and `[Telegram context: ...]` itself — a bracketed prefix prepended to the
dispatched text, which the LLM reads as part of the user turn. **The fix should follow this exact
convention**, not invent a new mechanism: build a `[Replying to ...]` prefix from `reply_to_message`
and prepend it the same way, right alongside the existing `[Telegram context: ...]` prefix.

**Checked and ruled out as a duplicate instance:** `_maybe_resume_from_reaction()` (line ~2651) has a
similarly-shaped `f"[Telegram context: ...]"` prefix build at line 2683–2686, but it's a **different
feature** (synthesizing a go-signal from an emoji *reaction*, not a text reply) — it has no
`reply_to_message` involved at all. Confirmed by reading the function: not a second occurrence of
this bug, no fix needed there.

### 1.3 Why the uncaptioned-photo case needs a different treatment than the captioned case

- **Captioned photo / text reply**: `reply_to_message.text` or `.caption` is directly available as a
  string — trivial to surface.
- **Uncaptioned photo**: there's no text to surface. **Out of scope for this fix**: actually
  re-fetching and passing the photo itself to the LLM as a vision input — checked, and **no
  image/vision-passing capability exists anywhere in the current LLM call path**
  (`app/llm/litellm_provider.py` has no `image_url` content-block handling; `download_telegram_file()`
  exists but is only ever used for voice notes today). Adding real vision support is a materially
  bigger, separate feature, not something to fold into a targeted bug fix. **In scope**: at minimum
  surface *that* a reply-to-an-uncaptioned-photo happened, who sent it, and roughly when — turns
  "total silence" into "she knows a reply relationship exists and can ask a clarifying question or go
  look it up," which is the actual root complaint (losing the relationship entirely), even without
  full content recovery.

### 1.4 Existing test coverage to extend, not build from scratch

`truesight_autopilot/tests/test_telegram_adapter.py` already exists with 78 test functions — this is
where the fix's regression tests belong, following the file's own existing conventions (checked, not
assumed — read the file's test style before writing new ones in PR1).

---

## 2. Authorization envelope (§5e — ask once, not per PR)

| Surface | Envelope |
|---|---|
| `truesight_autopilot` PR + tests | Pre-authorized — feature branch + PR, human reviews before merge. |
| **Deploying the fix live** (restarting `truesight-autopilot` on the autopilot box) | **Always-stop gate (§5c: production deploy)** — this is the DAO's live governor-facing chat service; a bad restart affects every in-flight thread across every topic (per `sophia_manual_restart_freezes_threads` precedent already documented elsewhere in this repo). Ask once before PR2's deploy step, not per-thread. |
| Filing the "why was this never documented" gap (PR3) | Pre-authorized — docs only. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | The fix, in `telegram_adapter.py` at the §1.2 insertion point: extract `reply_to_message`'s sender + text/caption (or a "replying to an uncaptioned photo/document from X" marker when no text exists) into a new `[Replying to ...]` bracketed prefix, prepended to `dispatch_text` alongside the existing `[Telegram context: ...]` prefix. **Tests in the same PR** (`tests/test_telegram_adapter.py`, extending existing conventions): reply-to-text, reply-to-captioned-photo, reply-to-uncaptioned-photo, reply-to-document, and a **no-reply regression case** confirming `dispatch_text` is byte-identical to today's output when there's no `reply_to_message` at all (this must not change behavior for the overwhelming majority of messages that aren't replies). | `truesight_autopilot` |
| **PR2** | Deploy PR1 to the live autopilot box and verify: have Gary reply to an actual photo in a real Telegram thread, confirm via `journalctl`'s `CHAT REQ` log line (same verification method used throughout this session) that the dispatched text now contains the `[Replying to ...]` prefix, and confirm Sophia's actual response demonstrates she used that context correctly (not just that the prefix is present — that she *acted* on it). **Deploy step is the §2 always-stop gate — needs explicit `go`.** | `truesight_autopilot` (deploy) |
| **PR3** | File this properly: an `OPEN_FOLLOWUPS.md`-style entry (or close it immediately, since PR1/PR2 fix it same-session) documenting the root cause found in §1.1, so a "second occurrence" gap like this — real, live-observed, but never written down — doesn't recur silently a third time. Also worth a one-line `CONTEXT_UPDATES.md` entry per that file's own append-only convention. | `agentic_ai_context` |
| **RUN/UAT** | See §5. Folded into PR2's live verification above — this fix has no separate staging environment beyond "verify on the live box," same as most `truesight_autopilot` changes (it's a single deployed service, not a beta/prod pair). | — |

---

## 4. Resume tracker

> **RESUME HERE → PR1** (the fix + tests). Fresh roadmap — nothing has started.
>
> No open governor decisions block this — the fix is narrowly scoped and the root cause is fully
> captured in §1. The only gate is PR2's deploy step (§2), which is a standing, expected gate for any
> `truesight_autopilot` change, not something specific to this fix.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☐ | ☐ |
| PR1 (fix + tests) | ☐ | ☐ | ☐ |
| PR2 (deploy + live verification) | ☐ | — | ☐ |
| PR3 (file the gap so it's tracked) | ☐ | ☐ | ☐ |

✅ **Pre-flight Completeness (§5d):** the exact two existing `reply_to_message` read-sites, the exact
insertion point for the fix (with surrounding code quoted), why the emoji-reaction code path is *not*
a duplicate instance, why full photo-content recovery is explicitly out of scope, and the existing
test file to extend are all captured in §1 — PR1 should not need to re-discover any of this.

---

## 5. UAT

| Step | Surface | What to expect | Acceptance criterion |
|---|---|---|---|
| 1 | Unit tests (PR1) | Reply-to-text, reply-to-captioned-photo, reply-to-uncaptioned-photo, reply-to-document, no-reply regression | All pass; no-reply case proves zero behavior change for non-reply messages |
| 2 | Live, PR2 | Gary replies to a real photo Sophia posted earlier in an active thread | `journalctl`'s `CHAT REQ` line shows the `[Replying to ...]` prefix with the correct sender + text/caption |
| 3 | Live, PR2 | Same live test | Sophia's response demonstrably references the replied-to content correctly — the actual fix, not just the plumbing |

---

## 6. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first) before starting the next unit.
