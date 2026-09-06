# Sophia Session Context Compaction — Execution Roadmap

**Status as of 2026-09-05: COMPLETE** — PR0→PR3 merged (#401–#404), deployed live at `e1fc54f`, verified folding real sessions in production (see §9 tracker).
**Repo under change:** `truesight_autopilot` (Sophia)
**Owner:** Gary Teh · **Driver:** Sophia (self-executed, Envoy supervising via Telegram)
**Reference incident:** 2026-09-05 — multiple long-running Telegram threads (mention-gate fix,
HEIC/GPS fix, Tencent Cloud migration) grew to 38,000–50,000 tokens of session context per LLM
call after many hours/turns. Each round now takes 30+ seconds of pure DeepSeek processing time
before any tool executes, compounding across 15–25+ round turns into multi-minute turns. This is
what makes the single-worker event loop "busy" long enough for `/health` to occasionally miss its
probe window (the exact case the 2026-09-02/03 restart-message fix, PR #392, made visible instead
of hiding behind a generic "restarting" message — that fix surfaced the symptom; this plan
addresses the underlying cause).

> **RESUME HERE:** Unit 0 — commit this plan; then PR0 (compaction library + tests, no wiring yet).

---

## 1. Background — what's actually happening, evidence-based

- `app/main.py:137` — `_sessions: dict[str, list[dict[str, str]]] = {}`, the full raw conversation
  history per session, held in memory and (via `_load_or_create_session`) mirrored to a local JSON
  file under `SESSION_LOG_DIR` (`/opt/truesight_autopilot/sessions/<hash>.json` in prod). **Nothing
  ever shrinks this — every turn appends, nothing is ever removed.**
- Confirmed on the live box: one real session file has 554 messages (272 assistant + 266 tool, only
  15 actual user turns) — each user message triggers many assistant/tool round-trips (tool-using
  turns), and every one of those round-trips stays in history forever.
- Confirmed live token counts (journalctl, `LLM RESP ... tokens=N`) on today's active threads:
  consistently 38,000–50,000 tokens per call, all of it re-sent on every single round of every
  future turn in that thread.
- `deepseek-v4-flash`'s context window is large (128K-class per DeepSeek's public model card) — **this
  is not close to hitting a hard error today**, so there's no cliff-edge urgency. It is a pure
  latency/cost/availability degradation: bigger context → slower DeepSeek response → longer turns →
  more windows where the single event loop is legitimately busy → more BUSY messages, more queued
  Telegram messages, more perceived "overload." It also costs more per call (DeepSeek bills by
  token) — a 50K-token call costs ~6-7x what a fresh 8K-token call would, on every single round.
- No token-counting utility exists anywhere in the codebase today (`grep` for `tiktoken`,
  `count_tokens`, `token_counter` — zero hits). `litellm` (already a hard dependency, per
  `requirements.txt`) ships its own `litellm.token_counter()` and `litellm.get_max_tokens(model)` —
  reuse these, don't add a new dependency.
- Existing per-turn structure is a gift for cheap summarization: per
  `SOPHIA_THREAD_CONCURRENCY_PLAN.md` invariant 7 (already shipped, PR3), **every completed turn
  already ends with a detailed "✅ Done this turn — actions taken" natural-language report** embedded
  in the assistant's own message content. This is already a distilled summary of what happened —
  compaction can reuse this text directly instead of paying for a fresh LLM summarization call on
  every compaction.
- Hard format constraint (must not violate): DeepSeek requires that any assistant message
  containing `tool_calls` be immediately followed by `tool`-role messages with matching
  `tool_call_id`s. `_sanitise_tool_messages` (from the concurrency plan's PR0) already heals
  accidental violations of this on load — compaction must never introduce new ones. **Any
  compaction boundary must fall on a full turn boundary** (right after a completed `user` →
  ...→ final assistant reply chain, never mid-tool-call-sequence).
- Concurrency invariants from `SOPHIA_THREAD_CONCURRENCY_PLAN.md` still apply and must not be
  broken: single-writer/single-executor per session (a per-`session_id` async lock already wraps
  the append+turn+log critical section) — **compaction must happen inside that same lock**, not as
  a separate racing operation.
- The GitHub transcript publish (`_publish_transcript`, async, per-turn, writes to the public
  `truesight_autopilot_transcript` repo) is a **separate, complete, uncompacted historical record**
  for DAO transparency/audit — compaction only touches the *live working copy* used to build the
  next LLM call; it must never reduce what's in the audit trail.

---

## 2. Target design — invariants

1. **Compaction never changes what's provably true** — the audit trail (GitHub transcript,
   session-log JSON backup taken pre-compaction) always has the full, uncompacted history available
   for a human or a future session to reconstruct exactly what happened.
2. **Compaction only touches the *in-memory working copy* fed to the next LLM call** — reduces
   token count, does not delete history from disk/GitHub.
3. **Compaction boundaries always land on a full turn boundary** — never inside a `tool_calls` →
   `tool` sequence. A "turn" = one `user` message through the final assistant reply that has no
   further pending tool calls.
4. **The most recent M turns (or last N messages, whichever floor is tighter) always stay verbatim,
   uncompacted** — recent context is exactly where the model needs full fidelity (it's mid-task).
5. **Everything older than that gets folded into a single compact summary block**, reusing each
   turn's own "✅ Done this turn" report text where present (cheap — no LLM call), falling back to a
   one-time LLM summarization call only for older segments that predate that reporting convention or
   otherwise lack a usable marker.
6. **Trigger is token-count-based, checked once at the start of a turn** (via
   `litellm.token_counter`), not time-based or message-count-based — the actual cost we're managing
   is tokens, so gate on tokens directly. Default threshold: configurable, start conservative (e.g.
   20,000 tokens) so it engages well before the 38-50K range seen today, leaving headroom.
7. **Compaction happens inside the existing per-session async lock**, immediately before the
   history is handed to the LLM — same critical section that already serializes same-session
   turns, so no new concurrency surface is introduced.
8. **Never automatic on day one.** Ship as a manually-invocable operation first (a tool/script an
   operator or Sophia can run against one specific session), proven safe against real bloated
   sessions, before wiring it to fire automatically inside the turn path.

→ *Recent turns stay perfectly sharp; everything older becomes a compact, still-accurate digest;
nothing is ever truly lost (it's on GitHub and in the pre-compaction backup); the model's working
context stops growing without bound.*

---

## 3. Architecture decisions (with rationale)

- **Token counting via `litellm.token_counter(model=..., messages=...)`**, not a hand-rolled
  estimator. It already ships with the dependency in use; using anything else risks drifting from
  what DeepSeek actually charges/limits.
- **Summary storage: a single synthetic message inserted at the front of the retained tail**, role
  `user` (matching the existing precedent — `GOVERNOR_IDENTITY` context is already prepended to a
  `user` message's content in exactly this style, `app/main.py:3158`), content prefixed
  `[CONTEXT SUMMARY — turns 1–K compacted, full history in transcript repo]:\n<summary text>`. Using
  a real message role (not inventing a new one) keeps this compatible with every LLM provider
  already wired in (DeepSeek, Claude via litellm, BigModel).
  *(Rejected alt: a `system`-role summary — some providers/DeepSeek tool-calling modes are picky
  about multiple system messages mid-conversation; a prefixed `user` message is the same pattern
  already proven safe in this codebase for GOVERNOR_IDENTITY.)*
- **Reuse existing "✅ Done this turn" reports** as the primary summarization source (regex/string
  extraction, no LLM call) for any turn that has one; only call the LLM to summarize a segment when
  no such marker exists in it. This keeps the steady-state cost of compaction near zero — it's
  mostly free text reuse, not a second inference pass.
  *(Rejected alt: LLM-summarize every compacted segment fresh, every time — correct but needlessly
  expensive at scale; the codebase already produces a good-enough summary for free on every turn.)*
- **Full pre-compaction backup before touching a session** — copy the session's on-disk JSON to
  `<hash>.pre-compact-<timestamp>.json` before rewriting it, so a bad compaction is trivially
  reversible without needing to re-derive from the GitHub transcript.
- **Manual-first rollout** (a `compact_session(session_id)` tool, or a standalone script) before any
  automatic wiring into the live turn path — matches how this codebase has repeatedly de-risked
  session-state changes before (see `SOPHIA_THREAD_CONCURRENCY_PLAN.md`'s own PR0 "safety net before
  behavior changes" approach, and this session's own precedent of the box's uncommitted-runtime-state
  caution during the mention-gate deploy).

---

## 4. Pre-flight checklist

- [x] Confirm `litellm.token_counter` gives sane numbers against `deepseek-v4-flash` on the actual
      box (spot-check against the journalctl `tokens=N` figures already logged for the same calls).
- [x] Confirm the exact JSON shape of 2-3 real bloated session files (`/opt/truesight_autopilot/sessions/*.json`)
      matches the assumed `full_history`/`recent_messages` schema before writing compaction code
      against it.
- [x] Confirm `_sanitise_tool_messages` behavior at the exact compaction boundary — write a test that
      compacts a real captured `tool_calls`/`tool` sequence and asserts the sanitiser sees zero
      dangling messages afterward.
- [x] Local `.venv` runs the existing pytest suite green before starting.
- [x] Confirm deploy mechanism unchanged from prior fixes this week (git-pull + service restart via
      `deploy_autopilot`, preserving uncommitted runtime-state files — same caution as the
      mention-gate deploy).

---

## 5. Sequenced plan (each PR independently shippable, one PR per turn)

### PR0 — Compaction library + tests, NOT wired into the live turn path yet
| Step | Description | Files |
|------|-------------|-------|
| 0a | `app/context_compaction.py` (new): `count_tokens(messages, model) -> int` (wraps `litellm.token_counter`), `find_turn_boundaries(messages) -> list[int]` (indices where a full turn ends — never inside a `tool_calls`/`tool` pair), `extract_done_this_turn(messages, start, end) -> str \| None` (regex/string extraction of the "✅ Done this turn" block, if present), `compact_history(messages, keep_last_n_turns, token_threshold, model) -> list[dict]` (the actual compaction: no-op if under threshold; otherwise folds everything before the retained tail into one summary message per invariant 5). | `app/context_compaction.py` |
| 0b | Backup helper: before compaction touches an on-disk session file, copy it to `<hash>.pre-compact-<UTC-timestamp>.json` in the same directory. | `app/context_compaction.py` |
| 0c | Unit tests: token counting sanity; turn-boundary detection never lands mid-`tool_calls`; "Done this turn" extraction on real captured examples; full compaction round-trip on a real bloated session fixture (redacted/synthetic) — assert `_sanitise_tool_messages` finds 0 dangling before/after; assert token count actually drops; assert the retained tail is byte-identical to the original tail. | `tests/test_context_compaction.py` |
| 0d | No wiring into `main.py`'s turn path yet — this PR only adds the library + tests, self-contained and zero behavior change for any live session. | — |

### PR1 — Manual trigger tool (de-risking step, per invariant 8)
| Step | Description | Files |
|------|-------------|-------|
| 1a | A tool (`compact_session_manual` or similar, following the existing tool-registration pattern in `app/tools/`) that takes a `session_id`/thread reference, loads it under the per-session lock, runs `compact_history`, writes the backup, saves the compacted version, reports before/after token counts. | `app/tools/*.py` (new or existing session-admin module) |
| 1b | Restrict to governor-only (mirror the existing `POLICY ALLOW ... by Gary Teh (role=governor)` pattern already used for `ssh_run`/`deploy_autopilot` — this is an infra-adjacent action). | same file / `app/policy.py` if a new gate is needed |
| 1c | Tests: tool refuses for non-governor; tool runs end-to-end against a real (test) bloated session; verifies backup file exists before compaction proceeds. | `tests/` |
| 1d | **Manual validation (not a code step):** run this manually against 1-2 of today's actual bloated live sessions (e.g. the mention-gate-fix or Tencent thread's session file) on the box, confirm the next turn in that thread still works correctly and the model doesn't lose track of in-flight work. Report results back before proceeding to PR2. |  |

### PR2 — Automatic wiring into the live turn path
| Step | Description | Files |
|------|-------------|-------|
| 2a | At the start of turn processing (inside the existing per-session lock, before the history is handed to the LLM — likely in `_chat_blocking_turn` / the equivalent for `/chat` streaming), call `count_tokens`; if over threshold, run `compact_history` before proceeding with this turn's LLM call. | `app/main.py` |
| 2b | Config: `settings.context_compaction_token_threshold` (default from invariant 6, e.g. 20000), `settings.context_compaction_keep_last_turns` (default e.g. 6), both overridable via env for tuning without a code change. | `app/config.py` |
| 2c | Log every automatic compaction clearly (before/after token count, turns compacted) so it's visible in journalctl and debuggable if something looks off afterward. | `app/main.py` |
| 2d | Tests: a turn that crosses the threshold triggers compaction before the LLM call; a turn under threshold does not; compaction failure (exception) does not crash the turn — falls back to running uncompacted rather than blocking the user. | `tests/` |

### PR3 — (rollout, not a PR) Deploy + verify — see §7.

---

## 6. Test plan

- **Unit** (`pytest -q`): token counting, turn-boundary detection, "Done this turn" extraction,
  full compaction round-trip integrity (no dangling tool_calls, tail byte-identical, token count
  drops), manual-tool governor gate, automatic-trigger threshold logic, graceful fallback on
  compaction failure.
- **Real-data validation (PR1 step 1d):** manually compact 1-2 of this week's actual bloated
  sessions on the live box; confirm the thread continues to function correctly on its next real
  turn (no lost context that mattered, no format errors).
- **Regression:** the existing `SOPHIA_THREAD_CONCURRENCY_PLAN.md` concurrency repro test (K
  concurrent same-session calls → 0 dangling `tool_calls`) must still pass with compaction wired in
  — compaction must not reintroduce the class of bug that plan fixed.

## 7. Rollout / deploy plan (gated on Gary's go — do not auto-deploy)

1. Merge PR0 → deploy → no behavior change, safe.
2. Merge PR1 → deploy → manually compact 1-2 real bloated sessions, verify live, report back.
3. On Gary's go: merge PR2 → deploy → watch the next few naturally-long threads for: token counts
   staying bounded, turn latency improving, no lost-context complaints.
4. If threshold/retained-turn-count need tuning, that's a config change, not a redeploy of logic.

## 8. Risks & mitigations

- *Compaction drops something the model actually needed* (e.g. a specific PR URL or file path
  mentioned only once, long ago) → mitigated by: keeping the "Done this turn" reports (which
  specifically call out PR URLs, file paths, key results) rather than a lossy generic summary; full
  transcript remains on GitHub and can be searched (`search_transcript` tool already exists) if the
  model needs to look something up it no longer has inline.
- *Compaction corrupts the tool_calls/tool pairing* → mitigated by: boundary detection tested
  explicitly against this failure mode; `_sanitise_tool_messages` still runs as a second line of
  defense on load regardless.
- *Race between compaction and an in-flight turn* → mitigated by: compaction runs inside the same
  per-session lock that already serializes turns; nothing new to race against.
- *Threshold badly tuned (too aggressive → loses useful context; too lax → doesn't help)* → starts
  conservative (20K), tunable via env without a redeploy, and PR1's manual-validation step catches
  bad behavior before PR2 makes it automatic.

---

## 9. Resume tracker

| Unit | Code | Merged | Deployed | Real-data validated | DAO contribution reported |
|------|------|--------|----------|----------------------|---------------------------|
| Commit this plan | ✓ | n/a | n/a | n/a | ☐ |
| PR0 — Compaction library + tests | ✓ (#401) | ✓ | ✓ | n/a (no wiring yet) | ☐ |
| PR1 — Manual trigger tool | ✓ (#402) | ✓ | ✓ | ✓ (§1d: `361e612c0b6b` 84,009→16,597 tok; `22f8f538dedd` 66,247→12,533 tok; tails byte-identical, 0 dangling) | ☐ |
| PR2 — Automatic wiring | ✓ (#403, `2a05df1`) | ✓ | ✓ | ✓ (post-deploy watch: live folds `489bd3d72796` 141→120, 142→99 + `d6a0767ddfc8` 75→68; backups + summaries verified) | ☐ |
| PR3 — per-round re-check (rollout fix) | ✓ (#404, `e1fc54f`) | ✓ | ✓ | ✓ (live at `e1fc54f`; health 200; 4 call sites incl. `_run_tool_round_loop`) | ☐ |

**RESUME HERE:** none — **COMPLETE (2026-09-05).** Deployed and verified live; compaction re-checks at turn
start and after every tool round; kill-switch `CONTEXT_COMPACTION_AUTO` (default on) for instant rollback.
Optional follow-up: file DAO contribution(s) for PR0–PR3.
