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

**RESUME HERE: Unit 0.**

## UAT

1. Feed a captured 90K+-token real turn through the new intra-turn compactor → confirm the model
   still produces a coherent, correct final answer for what it was doing, and total context stays
   well under the pre-fix peak.
2. Confirm a turn that's naturally short (under the round/token threshold) is completely unaffected
   — no behavior change for the common case.
3. Confirm no dangling/malformed tool_calls after folding, same check the original compaction
   plan's PR0 tests already cover — reuse those test patterns.
