# Sophia Emoji-Reaction GO Signal — Execution Roadmap

**Status:** New. Not started.
**Owner:** Gary Teh.
**Requested by:** Gary Teh (via DeepSeek Local), 2026-08-29.
**Repo:** [`TrueSightDAO/truesight_autopilot`](https://github.com/TrueSightDAO/truesight_autopilot) (Sophia's own codebase).
**Auto-start:** yes — begin executing from RESUME HERE immediately; do NOT wait for a go-signal.

**Goal:** Let an authorized governor authorize a parked handoff with an emoji **reaction** on the message
Sophia posted with her "ready / resume here" proposal, instead of typing a text go-signal. Any standard emoji
reaction from an allowed user on a resume-awaiting message becomes a go-signal equivalent to typing
"go for it" — **except 👎 (thumbs down)**, which is excluded.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. Update the resume tracker as units land; report the DAO
> contribution after each merge (§6). §5a: **one PR per execution turn, then stop.**
> **Own-repo gate:** `truesight_autopilot` is Sophia's own repo — she **opens PRs only, never self-merges**;
> a human (Gary) merges each PR and approves the deploy.

---

## 0. Decisions

| # | Decision | Choice |
|---|----------|--------|
| 0.1 | Emoji set | **Deny-list, not allow-list.** Any standard emoji (`ReactionTypeEmoji` → `{"type":"emoji","emoji":"…"}`) counts as go-ahead — including 👍, 🔥, 👏 (clap), 😁 (smile), and ❤️ (love) — **except `👎` (thumbs down)**, which is explicitly not a go. Ignore `ReactionTypeCustomEmoji` (paid/custom emoji carry `custom_emoji_id`, not `emoji`). |
| 0.2 | Reaction scope | Only on messages Sophia **herself posted that are flagged "resume-awaiting"** (a message carrying a resume/go proposal). A reaction on any other message (status update, log, etc.) is ignored — never a resume trigger. |
| 0.3 | Authorized users | Reuse the existing security gate — `is_allowed(user_id, allowed)` plus the governor fallback via `resolve_identity` (`app/telegram_adapter.py:1604-1636`). The reacting user must pass the same gate a text "go" sender would. |
| 0.4 | Registry lifetime | `message_id → {thread_id, text}` registry persisted to a small JSON file (survives Sophia restart between the "ready" post and the reaction, which can be minutes to days apart). Bounded; entries pruned once consumed or after a TTL. |
| 0.5 | Addressed-only interaction | **None.** Reactions are not text messages; the "address by name" convention (`sophia/SOPHIA_HANDOFFS.md` §addressed-only) does not apply. A reaction on a resume-awaiting message is inherently addressed. |
| 0.6 | Backward compat | Text go-signals (`_GO_SIGNAL_RE`) keep working unchanged. The reaction path is additive. |

---

## 1. Current behavior (read in full 2026-08-29)

### 1.1 The go-signal path today

- `app/telegram_adapter.py:340-345` — `_GO_SIGNAL_RE` matches text like `go for it`, `go`, `proceed`,
  `ship it`, `resume`, `RESUME HERE`, `^\s*go\s*$`.
- `:348-355` — `_looks_like_go_signal(text)` wraps the regex.
- `:358-406` — `_handoff_prefix(thread_id, text)` injects, into a registered handoff topic, a block telling
  Sophia to "read the plan, resume from RESUME HERE, treat a short go-signal as full authorization".
- A governor types a short go-signal in the topic → it dispatches as a normal message through
  `call_chat_with_progress` (serialized per topic via `_thread_dispatch_lock`, `:1732-1740`) → Sophia resumes.

The feature adds a **second, reaction-based** way to produce that same go-signal.

### 1.2 Why reactions are currently invisible

- `app/telegram_adapter.py:504-510` — `get_updates(offset)` calls Telegram `getUpdates` with **no
  `allowed_updates`** parameter. Telegram's default excludes `message_reaction` (and
  `message_reaction_count`), so Sophia never receives reaction updates.
- `app/telegram_adapter.py:2145-2152` — the `run()` poll loop only reads `upd.get("message")`,
  `upd.get("edited_message")`, and `upd.get("callback_query")`. Even if a `message_reaction` update were
  delivered, it is silently dropped.

### 1.3 Telegram `message_reaction` shape

A `message_reaction` update looks like:

```json
{ "update_id": 1,
  "message_reaction": {
    "chat": {"id": -1003919341801, "title": "TrueSight DAO Ops", "type": "supergroup"},
    "message_id": 1234,
    "user": {"id": 2102593402, "is_bot": false, "username": "garyjob"},
    "date": 1700000000,
    "old_reaction": [],
    "new_reaction": [{"type": "emoji", "emoji": "👍"}]
  } }
```

Key facts: **no `message_thread_id` field** — the topic must come from Sophia's own record of which thread
she posted `message_id` in. Standard emoji reactions are `ReactionTypeEmoji` with an `emoji` string.

### 1.4 Message-id capture gotcha

`send_message` (`:578-601`) chunks long replies via `chunk_text` and returns the `message_id` **only of the
first chunk**. Sophia's ready/GO prompt ("…Reply "go for it"…") typically lands on the **last** chunk of a
multi-chunk kickoff, and a governor will react to the message that *says* "go for it". So the resume registry
must capture **every chunk's** `message_id` for a resume-awaiting post — not just the first.

---

## 2. Implementation plan

**Stack:** Python/FastAPI, the existing `app/telegram_adapter.py` long-poll adapter + `app/config.py`
settings. All changes are in `truesight_autopilot`. No new dependencies.

### 2.1 Sequenced units (one PR per execution turn)

| Unit | Change | Own-repo merge |
|------|--------|----------------|
| **PR1** | `get_updates` sends `allowed_updates=["message","edited_message","callback_query","message_reaction"]`; `run()` dispatches `upd.get("message_reaction")` to a new `handle_message_reaction(reaction, allowed)`; handler parses `chat_id`, `message_id`, reacting `user`, and `new_reaction` emoji set, and — for now — logs the reaction + authorized/go verdict (no resume yet). Add `settings.emoji_go_blocked` (default `["👎"]`; the deny-list — a reaction whose `new_reaction` contains only `ReactionTypeEmoji` entries and none in the blocked set is a go; `ReactionTypeCustomEmoji` ignored). Unit tests for the parser (reaction shape → go/blocked/custom verdict, authorized-user check). | Human merges |
| **PR2** | New `app/resume_registry.py`: `mark_resume_awaiting(message_id, thread_id, text)`, `is_resume_awaiting(message_id)`, `lookup(message_id) → {thread_id, text}`, persisted to a small JSON file. Hook the ready/GO-prompt post path so the kickoff's **every chunk** `message_id` is marked (fix/thread the chunk-id capture from §1.4). Tests. | Human merges |
| **PR3** | Wire it together: in `handle_message_reaction`, if reacting user is allowed (same gate as §1.1) AND the reaction is a go (per §0.1 deny-list) AND `message_id` is resume-awaiting → synthesize a go-signal message for that thread (e.g. a `[emoji-go: <emoji> from <user>] go for it` text) and enqueue it through the **same** `_thread_dispatch_lock` + `call_chat_with_progress` path a text go-signal uses. Mark the registry entry consumed. Tests (incl. "👎 is not a go", "reaction on non-resume message is ignored", "non-allowed reactor ignored"). | Human merges |
| **PR4** | Docs + conventions: update `agentic_ai_context/sophia/SOPHIA_HANDOFFS.md` (document reaction-as-go alongside the text GO convention) and `agentic_ai_context/DEEPSEEK_LOCAL.md` if needed. Doc-only. | Human merges |

### 2.2 Gates (always-stop, human in the loop)

| Gate | When | Who |
|------|------|-----|
| **Own-repo merge** | After each PR1–PR4 opens | Gary merges |
| **Prod deploy** | After PR1–PR3 merged | Gary approves `scripts/deploy.sh` + systemd restart (always-stop) |
| **UAT** | After deploy | Gary runs §5 below |

---

## 3. Pre-flight (captured; no execution unit needs to re-discover these)

- `app/telegram_adapter.py:504-510` `get_updates` — currently no `allowed_updates`; `httpx.get(_api("getUpdates"), params={"timeout", "offset"})`.
- `app/telegram_adapter.py:2106-2152` `run()` — poll loop; `:2147` message extraction; `:2150` callback_query.
- `app/telegram_adapter.py:340-406` `_GO_SIGNAL_RE` / `_looks_like_go_signal` / `_handoff_prefix`.
- `app/telegram_adapter.py:578-601` `send_message` — returns first-chunk `message_id` only (§1.4 gotcha).
- `app/telegram_adapter.py:1604-1636` security gate — `is_allowed(user_id, allowed)` + `resolve_identity` governor fallback.
- `app/telegram_adapter.py:1732-1740` — `_thread_dispatch_lock` + `call_chat_with_progress` (the enqueue path PR3 must reuse).
- `app/config.py:313-317` `telegram_allowed_user_ids` (comma-separated string).
- `app/config.py:328` `telegram_home_group_id`.
- Ready/GO prompt ("✅ Ready. Reply go for it…") is **LLM-generated** via the `create_telegram_topic` / `post_to_telegram_topic` tools — PR2 must flag it at the post site, not by a fragile string match.

> ✅ Pre-flight Completeness: no execution unit requires reading a file/state not already captured in the pre-flight.

---

## 4. Resume tracker

**RESUME HERE = PR2**

| Unit | PR opened | Merged (human) | Contribution reported | Deployed |
|------|-----------|----------------|-----------------------|----------|
| PR1 — receive reactions | ☑ [#331](https://github.com/TrueSightDAO/truesight_autopilot/pull/331) | ☑ | ☑ | — |
| PR2 — resume registry + flag | ☐ | ☐ | ☐ | — |
| PR3 — reaction → go-signal | ☐ | ☐ | ☐ | — |
| PR4 — docs | ☐ | ☐ | ☐ | — |
| Deploy (gate) | — | — | — | ☐ |
| UAT (gate) | — | — | — | ☐ |

---

## 5. UAT (human, on a test topic — never a live handoff)

1. **Surface:** a scratch topic in TrueSight DAO Ops. Have Sophia post a fake "✅ Ready — reply go for it" message.
2. **Action:** Gary reacts with a standard emoji (e.g. 👍, then ❤️, 🔥, and a non-thumbs-down emoji) to that message.
3. **Expect:** Sophia posts a short ack and proceeds exactly as if "go for it" had been typed; the registry entry is consumed.
4. **Negative 1:** Gary reacts 👎 → no resume (explicitly excluded).
5. **Negative 2:** a non-allowlisted account reacts 👍 → no resume (Sophia stays parked).
6. **Negative 3:** Gary reacts 👍 to a plain status/log message (not resume-awaiting) → no resume.
7. **Acceptance:** 1–6 all pass; text go-signals still work (regression check).

---

## 6. Completion definition

All of PR1–PR4 merged, prod deployed, UAT §5 green, `sophia/SOPHIA_HANDOFFS.md` updated, DAO contributions reported per §6.
