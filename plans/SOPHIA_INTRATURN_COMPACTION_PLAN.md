# Sophia — in-turn context compaction (extends SOPHIA_CONTEXT_COMPACTION_PLAN.md)

## Background

The existing compaction system (PR0-PR3, shipped this session — see
`plans/SOPHIA_CONTEXT_COMPACTION_PLAN.md`, now COMPLETE) folds **completed prior turns** into a
summary once a session's total token count crosses a threshold. By design it never touches the
**currently in-progress turn** — that's a correctness property (a turn's tool_calls/tool results
must stay intact and byte-identical while still open), not an oversight.

That leaves a real, now-observed gap: a single turn that needs many tool-call rounds to converge
(investigation-heavy work — reading many files, running many `ssh_run` diagnostics, iterating on a
merge conflict) accumulates all of that round-by-round output *inside one open turn*, and nothing
currently compacts it. Measured live 2026-09-14: two turns reached **94,264** and **72,391+
tokens** within a single still-open turn (12 and 18+ rounds respectively), climbing every round
with no compaction possible under the current design.

Very long context windows are a known trigger for degraded output reliability in LLMs generally —
in particular, reduced fidelity on strict output-formatting requirements (tool-call syntax). This
session directly observed the failure mode this predicts: raw model-internal tokens
(`<｜｜DSML｜｜invoke>`-style special tokens) leaking into user-visible chat output instead of being
correctly parsed as a tool call, on at least two occasions, both during very-long single turns.
This plan is a direct, evidence-based response to that — not a hypothetical concern.

## Target design

Compact **within** an open turn, not just between turns — fold early, no-longer-immediately-needed
tool round outputs into a running summary while the turn is still in progress, keeping only the
most recent N rounds' raw tool output plus the running summary.

1. **What's safe to fold**: a completed tool round's raw output (e.g. a full `ssh_run` stdout dump,
   a full file read) once several more rounds have happened since — the model's own subsequent
   reasoning already shows what it extracted/needed from that round; the raw bytes are usually
   dead weight past a certain point. What must NOT be folded: the most recent K rounds (keep raw,
   e.g. K=3-5, tunable) so the model retains exact, unsummarized recent tool output for whatever
   it's actively reasoning about right now.
2. **Trigger**: reuse the existing `_maybe_auto_compact` per-round hook added in PR3
   (`app/main.py`, called every round in both `_run_tool_round_loop` and `_chat_blocking_turn`) —
   but add a new, *intra-turn* check alongside the existing *inter-turn* one: if the **current
   turn's own round count** exceeds a threshold (e.g. 8-10 rounds) OR the current turn's own token
   contribution exceeds a threshold (e.g. 40K), fold everything from the current turn except the
   last K rounds into one `[TURN IN PROGRESS — EARLIER ROUNDS SUMMARY]`-tagged entry, generated the
   same way `extract_done_this_turn`/`default_summarizer` already work for inter-turn folding —
   reuse that machinery, don't build a parallel one.
3. **Never fold an incomplete tool_calls/tool_result pair.** Same invariant as the existing
   `find_turn_boundaries` logic, just applied at round granularity instead of turn granularity —
   only fold a round once its tool_calls message AND all matching tool results are present.
4. **Backup before folding**, same convention as `backup_session_file` in the existing system —
   this is still a destructive-looking (though summarized, not deleted) transformation of session
   state, worth being able to reconstruct.
5. **Test with the same rigor as PR0-PR3**: real bloated-session replay (the 94K/72K-token turns
   captured live tonight are excellent real fixtures), confirm compacted output still lets the
   model correctly finish the turn it was mid-way through, confirm no dangling tool_calls.

## Sequenced plan (one PR per turn, §5a)

| # | Unit | Notes |
|---|------|-------|
| 0 | Pre-flight: capture the two live 90K+/70K+-token turns from tonight's logs as test fixtures before they roll off | Fast, do first — real data beats synthetic |
| 1 | Extend `app/context_compaction.py` — new intra-turn folding function, reusing `extract_done_this_turn`/`default_summarizer`, operating on round boundaries within the still-open turn | PR |
| 2 | Wire the new intra-turn check into the existing per-round `_maybe_auto_compact` call sites (`_run_tool_round_loop`, `_chat_blocking_turn`) | PR |
| 3 | Validate against the real 94K/72K fixtures from Unit 0 — confirm the turn still completes correctly post-compaction, no dangling tool_calls, and (if reproducible) confirm the DSML-token-leak failure mode doesn't recur on the compacted version | PR + validation checkpoint, same pattern as the original plan's manual-tool-first rollout |
| 4 | Deploy + monitor for a day of real heavy-round-count turns before considering this done | Gate — confirm real improvement, not just passing tests |

**RESUME HERE: Unit 4 (GATE — deploy + monitor). Units 0–3 are COMPLETE.**

| # | Unit | Status | Evidence |
|---|------|--------|----------|
| 0 | Capture live 90K+/70K+ fixtures | ✅ shipped 2026-09-14 | PR #446 (merged `b9bf9a4`) |
| 1 | Intra-turn folding function in `app/context_compaction.py` | ✅ shipped | PR #523 (squash `43df6f1`) — `find_open_turn_start`, `_scan_rounds`/`find_complete_rounds`, `default_round_summarizer`, `compact_open_turn(messages, keep_last_k_rounds=4, token_threshold=40000, round_threshold=8)` |
| 2 | Wire into the per-round `_maybe_auto_compact` call sites | ✅ shipped | PR #549 (merged `d137c9b`) — `_maybe_compact_open_turn` def at `app/main.py:6314`, call sites at `3803` (`_run_tool_round_loop`) and `5682` (`_chat_blocking_turn`) |
| 3 | Validate against the real 94K/72K fixtures | ✅ shipped | PR #642 (merged `5707bdb`) — `tests/test_intraturn_validation.py` (313 lines) |
| 4 | Deploy + monitor a day of heavy-round-count turns | 🟡 **LIVE (in prod since 2026-11-25 14:19:52Z); monitoring window OPEN** | code is live via the `main` deploy; formal 1-day soak + governor sign-off still gated — see below |

Both Unit 2 and Unit 3 were independently re-verified on `main` at `5707bdb` via
the GitHub API (`state: closed, merged: true`) and by grepping the shipped
source — not by trusting the prior marker. Unit 2 and Unit 3 were previously
listed here as "not yet started"; that was stale and is corrected above.

**Unit 3 validation results (real fixtures, not synthetic):** the 20-round /
46-message `open_turn_discord_long.json` folds **29,197 -> 11,266 tokens** with
the retained last K=4 rounds byte-identical, the original instruction intact,
and no new dangling `tool_calls`. The raw journal curves reproduce the
motivation exactly: **94,264 @ r12, 76,998 @ r24, 111,148 @ r24**, each inside a
**single still-open turn** — structurally invisible to the inter-turn folder,
which by design always keeps the in-progress turn in its retained tail.

One real interaction was found by validating against the shipped
`_sanitise_tool_messages` rather than a stub: its user-merge pass collapses the
preserved instruction + the rounds summary (two consecutive `user` messages)
into one. Traced and confirmed **lossless and intentional** — identical to how
it heals ordinary transcripts — so the test *expects* the merge. This is
exactly the class of bug Unit 3 existed to catch.

**Honest limitation (does not block Unit 4):** the live UAT probe self-skips on
DeepSeek's `reasoning_content` replay error, because the Unit-0 fixtures record
`content` but not `reasoning_content`. An A/B proved this is a **fixture
fidelity gap, not a compaction defect** — the unfolded (46-msg) and folded
(11-msg) arms fail with the *identical* error, so the fold introduces no new
API-level breakage. Tracked in `OPEN_FOLLOWUPS.md`; the "turn still completes
post-fold under live replay" claim therefore remains **unproven**, and Unit 4's
monitoring is what should establish it empirically.

**Unit 4 pre-flight finding (2026-11-25, read-only) — the wiring is ALREADY LIVE in
production, ahead of the gate.** This was not a decision taken here; it is a
consequence of the `main`-branch deploy, and the plan had not recorded it.

- The deployed tree `/opt/truesight_autopilot` has `app/main.py` **byte-identical
  to `origin/main`**, which contains Unit 2's `_maybe_compact_open_turn` (def at
  `6314`, call sites `3803` / `5682`).
- All four `CONTEXT_INTRATURN_*` knobs are **unset** in `.env`, so the **code
  defaults apply — `CONTEXT_INTRATURN_COMPACTION_AUTO=1` — intra-turn folding is
  ON right now.**
- `truesight-autopilot.service` started **2026-11-25 14:19:52 UTC**; the new path
  is demonstrably executing:

  | Evidence | Value |
  |---|---|
  | Intra-turn folds logged | **7** |
  | Intra-turn exceptions | **0** |
  | Typical fold | `85 -> 74`, `82 -> 73`, `81 -> 73`, `63 -> 55` messages, last K=4 rounds verbatim |
  | Thresholds in effect | `round_threshold=8`, `token_threshold=40000` |

So Unit 4's *deploy* half is effectively complete-by-accident; what remains is
the **soak + sign-off**, which is the part that actually carried the gate. The
soak is genuinely load-bearing here: because the Unit-0 fixtures lack
`reasoning_content`, live replay of a folded turn could not be validated
(see `OPEN_FOLLOWUPS.md`), so **only real production turns can establish that a
folded turn still completes correctly.** Watch for: threads that fold and then
fail to converge, repeated folding of the same session (a sign the fold isn't
relieving pressure), and any assistant output containing raw DSML special tokens.

Monitored honestly: 7 folds / 0 errors over ~9 minutes is a good signal, **not**
a passed soak. Do not mark Unit 4 done on it.

**Unit 4 is a gate.** Folding now runs inside the live per-round loops, so
deploying changes production behaviour. Do not deploy without an explicit
governor go. Rollback is a single env var — `CONTEXT_INTRATURN_COMPACTION_AUTO=0`
— needing no redeploy, and every fold writes a pre-compaction backup first.
Knobs: `CONTEXT_INTRATURN_TOKEN_THRESHOLD` (40000),
`CONTEXT_INTRATURN_ROUND_THRESHOLD` (8), `CONTEXT_INTRATURN_KEEP_LAST_K_ROUNDS` (4).

## UAT

1. Feed a captured 90K+-token real turn through the new intra-turn compactor → confirm the model
   still produces a coherent, correct final answer for what it was doing, and total context stays
   well under the pre-fix peak.
2. Confirm a turn that's naturally short (under the round/token threshold) is completely unaffected
   — no behavior change for the common case.
3. Confirm no dangling/malformed tool_calls after folding, same check the original compaction
   plan's PR0 tests already cover — reuse those test patterns.
