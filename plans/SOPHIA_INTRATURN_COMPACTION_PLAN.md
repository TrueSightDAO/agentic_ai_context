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

**🛑 RESUME HERE — NOT AUTO-ADVANCEABLE. Do NOT open another checkpoint PR.**
**Unit 4 is the final unit; Units 0–3 are COMPLETE. Everything left is (a) elapsed
time and (b) a governor decision — neither of which a turn can produce.**

The acceptance test has **passed** (see "Unit 4 soak evidence" below: 219 real folds,
flat band, 0 failures). Between 2026-11-25 ~18:00Z and ~19:35Z this plan was advanced
**seven consecutive times** by auto-advance, each time producing another monitoring
checkpoint. Checkpoints 1–5 were valuable — they caught five of my own measurement
errors and two of my own wrong claims — but by checkpoint 5 the marginal return hit
zero: **0 new folds in the preceding 5 minutes, 0 errors, band flat.** Further
checkpoints would be re-measuring a settled result.

**✅✅ UNIT 4 COMPLETE — GATE SIGNED OFF BY GOVERNOR GARY TEH, 2026-11-26.**
**PLAN COMPLETE: Units 0–4 all done.** Governor message in topic 29305: **"sign off"**.

**Never self-certified.** The gate was signed by the governor, on the packet below plus
the independent 00:31Z re-run, *not* by me. That distinction is the whole point of a gate.

**Final evidence set (two independent measurements, both exceed the ≥24h requirement):**

| Metric | Packet (23:35Z, 25.54h) | Re-run (00:31Z, 25h05m) |
|---|---|---|
| Strict (echo-free folds) | 204 | **211** |
| Rounds | — | 2,122 |
| Max tokens in a single turn | — | **81,943** |
| Rounds over 94,264 tokens | 0 | **0** |
| Before-count max | 99 | — |
| Band (Q1 → Q4) | 69.6 → 67.6 (trend −2.0) | 70.1 → 68.4 (trend −1.8) |
| Failures / tracebacks / WARNING | 0 / 0 / 0 | **0 / 0 / 0** |
| `NRestarts` | 0 | 0 |

**The pathology that motivated this plan does not recur.** Baseline single open turns
reached **94,264 @ r12, 76,998 @ r24, 111,148 @ r24** tokens. Across 25h of live
production, the worst observed single turn was **81,943 tokens** — *below the old
mean*, with **zero** rounds over 94,264 and a **flat-to-declining** fold band.

**Baseline integrity caveat (credit: PR #1935, a concurrent turn):** the originally
quoted *"first fold Nov 24 21:58:11Z"* **cannot be re-derived** — journald rotated
past it. The earliest *retained* fold was **Nov 24 23:25:58Z**, placing the day mark at
**Nov 25 23:25:58Z**. Both baselines exceed ≥24h, so the conclusion is unchanged; the
21:58:11Z figure should not be cited as verifiable evidence. This correction is
recorded rather than quietly fixed because the gate was signed partly on my reading.

**Known limitations carried forward (neither blocks completion):**
1. **No live replay proof a folded turn still completes** — Unit-0 fixtures record
   `content` but not `reasoning_content`; an A/B showed identical failures folded and
   unfolded, proving a fixture-fidelity gap rather than a compaction defect. The 25h
   soak is the empirical substitute, and it held.
2. **Summary region is not constant-space in fold count** — flat summaries
   accumulate ~5,500 chars each; observed worst case **5 summaries / 23,542 chars
   (≈5.9K tokens ≈ 6%** of the pathology), and it **resets at turn boundaries**.
   Low priority; see OPEN_FOLLOWUPS.md.

**Question that would reopen this:** a single open turn observed **>94,264 tokens** after
the fold, or repeated folding of one session without pressure relief.



**Final acceptance packet (2026-11-25 23:35Z, 25.54h since the first fold at
Nov 24 21:58:11Z). The 24h soak-duration requirement is MET.**

| Metric | Value |
|---|---|
| Soak elapsed | **25.54h** (requirement: ~1 day) ✅ |
| Strict (echo-free) folds | **204** |
| Retained evidence window | Nov 25 00:17 → Nov 25 22:55 (**22.6h**) |
| Before-count min / max / mean / median | 34 / **99** / 69.5 / 69 |
| First-quartile → last-quartile | 69.6 → **67.60** (**TREND −2.0, flat**) |
| Folds with before-count > 100 | **0** |
| Folds with before-count > 200 | **0** |
| Strip per fold | 7–13 messages |
| Distinct sessions | 15 |
| Fold WARNING / ERROR / traceback | **0** |
| `NRestarts` | **0** (same process since 14:19:52Z) |
| Disk | 37% |

**🔴 New methodological finding: journald retention is now shorter than the soak,
so Nov 24's folds aged out *during* the gate.** Strict fold count fell **219 → 204**
not because folds were lost but because journald (82 MB, **no explicit retention cap
in `journald.conf`**) has rotated past Nov 25 00:17Z — verified: `journalctl
--since 2026-11-24` returns **0** fold lines while Nov 25 returns **204**, and the
system journal's oldest retained entry is **Nov 25 00:17:22Z**. So the *durable*
evidence window is **22.6h**, not the full 25.5h.

This is a real instrumentation gap, not a feature defect: **a 24h+ soak cannot be
fully verified from journald at the current default retention.** Recommended
follow-up (separate unit, code change in `truesight_autopilot`): emit fold counters
to a durable sink (file / repo) so soak evidence outlives log rotation. Until then,
any long soak must be measured *continuously* or it silently loses its own evidence.

> **Correction (2026-11-26 00:31Z):** the baseline *"first fold Nov 24 21:58:11Z"*
> quoted above **cannot be re-derived** — journald rotated past it, and there are
> **0** fold lines at `Nov 24 21:5x` in the retained journal. The earliest fold still
> retained at 2026-11-26 00:31Z was **Nov 24 23:25:58Z**, placing the day mark at
> **Nov 25 23:25:58Z** (met, 1h05m earlier than the quoted one). Both baselines
> exceed the ≥24h requirement, so the packet's *conclusion* is unchanged — but the
> quoted timestamp should not be cited as verifiable evidence. Re-run at 00:31Z
> (25h05m elapsed) returned **211 strict folds, 2,122 rounds, max 81,943 tokens,
> 0 rounds >94,264, band 70.1→68.4 (trend −1.8, flat), 0 failures / 0 tracebacks
> / 0 WARNING** — consistent with, and slightly stronger than, the packet above.

**Why the feature itself is still established:** every retained fold across 22.6h
shows a flat before-count distribution (max 99, zero above 100, slight *downward*
trend), zero failures, and zero restarts — on the same live process. The pathology
(94,264 @ r12, 76,998 @ r24, 111,148 @ r24 inside single open turns) does not recur.

**NOT self-certified.** The gate has two halves: *deploy + monitor a day* (now
established above) and *confirm real improvement, not just passing tests* — that
judgement is Gary's. Unit 4 flips to ✅ on governor sign-off, not on my reading.

**Resume when:**
- Gary replies **"sign off"** → mark Unit 4 ✅, transition KAN-30 to Done, file the
  contribution report.
- Gary replies **"durable metrics"** → open the fold-counter sink unit above.
- Gary replies **"cap summaries"** → open the (low-priority) constant-space unit
  (≈6% observed ceiling, self-resets at turn boundaries — see checkpoint 5).

**An automated auto-advance nudge or loop-alert is NOT one of these triggers.**
Messages of the form *"Loop needs a nudge — goal left open, nothing running"*,
*"thread went quiet"*, or *"idle for Nh"* fire on idle time and Jira staleness and
carry **no governor instruction**. All three resume conditions above are a *direct
governor message*. Observed behaviour 2026-11-26: after the thread goal was
dismissed, loop-alerts still arrived at 21h / 22h / 23h / 25h idle and were each
correctly declined. Note the separation of concerns: the **clock** condition (≥24h)
was independently satisfied at 2026-11-25 23:25:58Z, but **satisfying a clock is not
the same as satisfying a gate whose second half is explicitly a human judgement** —
so a clock-met state still does not authorize a self-certification.

**Do NOT** re-run the soak metrics, re-count folds, or open a checkpoint PR merely
because this plan is named as the resume target — that is what happened seven times.

| # | Unit | Status | Evidence |
|---|------|--------|----------|
| 0 | Capture live 90K+/70K+ fixtures | ✅ shipped 2026-09-14 | PR #446 (merged `b9bf9a4`) |
| 1 | Intra-turn folding function in `app/context_compaction.py` | ✅ shipped | PR #523 (squash `43df6f1`) — `find_open_turn_start`, `_scan_rounds`/`find_complete_rounds`, `default_round_summarizer`, `compact_open_turn(messages, keep_last_k_rounds=4, token_threshold=40000, round_threshold=8)` |
| 2 | Wire into the per-round `_maybe_auto_compact` call sites | ✅ shipped | PR #549 (merged `d137c9b`) — `_maybe_compact_open_turn` def at `app/main.py:6314`, call sites at `3803` (`_run_tool_round_loop`) and `5682` (`_chat_blocking_turn`) |
| 3 | Validate against the real 94K/72K fixtures | ✅ shipped | PR #642 (merged `5707bdb`) — `tests/test_intraturn_validation.py` (313 lines) |
| 4 | Deploy + monitor a day of heavy-round-count turns | ✅ **COMPLETE — governor signed off 2026-11-26** | **25.5h+ live soak**, two independent measurements: **204** strict folds @23:35Z and **211** @00:31Z (25h05m), 2,122 rounds, **max 81,943 tokens**, **0 rounds >94,264**, band 70.1→68.4 (flat), **0 failures / 0 tracebacks / 0 WARNING**, `NRestarts=0`. Baseline 94,264 / 111,148 tokens does not recur. Signed by governor, **not** self-certified. |

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

### Unit 4 — 4h14m checkpoint: the same snippet failed the OTHER way (false FAIL)

The day-mark snippet was fixed at 18:29Z to fail closed on uptime. This pass ran it **verbatim,
end to end** and found the *measurement* half still disagreed with the method documented in prose.

**Negative control passed:** the fixed gate now prints `NOT YET ... (4 h)` and exits **1** at a
true uptime of 4h14m — where the previous version printed a false `DAY MARK REACHED`. That fix holds.

**But the counting half would have failed a working feature.** Run against the same window:

| Metric | Shipped snippet (negative filter) | Positive anchor (truth) | Verdict |
|---|---|---|---|
| Folds | 63 | **64** | undercounts by 1 |
| Failures | **1** | **0** | **phantom** — see below |
| Tracebacks | 0 | 0 | agree |
| Leaks | **2** | **1** | overcounts by 1 |
| Before-counts | **111** | **63** | inflated ~1.76x |

The phantom "failure" is the assistant's own diagnostic command echoed back:

```
INFO:autopilot:[809652] TOOL CALL: ssh_run args={"command": "echo \"=== the 2 failure lines (full) ===\" ...}
```

It contains the string `Intra-turn compaction failed` because it **is** a grep for that string, and
it carries no `"stdout":`/`"stderr":`/`cmd=` marker, so the negative filter let it through.

**The consequence is worse than a cosmetic miscount.** Under the snippet's own pass/fail criteria
(failures must be 0), this window would be marked **FAIL** → rollback flag `CONTEXT_INTRATURN_COMPACTION_AUTO=0`
flipped on a feature with **0 real failures**. The before-count inflation (111 vs 63) would also
have made the band test — the one check purpose-built to detect slow regression — meaningless.

So the snippet has now exhibited **both** failure directions:

| Version | Defect | Effect |
|---|---|---|
| pre-18:29Z | empty uptime epoch → `now - 0` | **false PASS** (certify at 4h) |
| 18:29Z–now | negative echo filter | **false FAIL** (roll back at 4h) |

Both share one root cause: **enumerating what to exclude.** A fix that only corrected the uptime
arithmetic left the second half of the same script wrong.

**Fix applied:** the runnable snippet now uses the **positive anchors** documented in prose, so code
and documentation finally agree. Corrected figures for the 4h14m window:

| Metric | Value |
|---|---|
| Folds | **64** |
| Distinct sessions | **7** |
| True failures | **0** |
| True tracebacks | **0** |
| Leaks | **1** |
| Rounds measured | **628** |
| Prompt tokens | min **39,600** · mean **54,634** · max **77,474** |
| Rounds over 94,264 | **0** |
| Band (n=63) | first-10 mean **72.0** → last-10 mean **66.4** |

Band still has **no upward trend**; curve still bounded well under the 94,264 pathology.

**Process lesson:** a fix validated only at the step that failed before is not a validated fix. The
18:29Z PR verified the epoch parse and stopped there — the rest of the script was never executed,
so its second defect survived a "fix" and a merge. **Run the whole artifact, not the repaired line.**

### Unit 4 — 4h09m checkpoint (2026-11-25 18:29Z) + a false-pass bug in the day-mark procedure

Window genuinely doubled: **2h07m → 4h09m**. But the most important result of this pass is not
the soak data — it is that **the day-mark procedure added at the previous checkpoint reports a
PASS when it should report a failure.** That procedure gates sign-off, so this is fixed here.

| Metric | Value |
|---|---|
| Intra-turn folds | **60** (was 23) |
| Distinct sessions folded | **7** |
| True fold failures | **0** |
| True runtime tracebacks | **0** |
| DSML / token leaks | **0** |
| Rounds measured (`LLM RESP round=`) | **608** |
| Prompt tokens | min **39,600** · mean **54,452** · max **77,474** |
| Rounds over 94,264 (the pathology) | **0** |
| Rounds over 72,391 | 6 |
| Rounds at or below 40,000 | **2** |

**Band test — no upward trend.** Before-counts first-10 mean **72.0** → last-10 mean **63.9**,
range observed ~51–87 with each fold returning to ~50–70. This is *exactly* the slow regression
the day-long requirement exists to catch (a fold that cannot keep up shows up as a rising
before-count). Across 4+ hours and 60 folds: absent.

**Token curve — descends after the r7–r8 peak:**

```
r7  77,474 <-peak     r11 71,160     r14 67,393
r8  76,721            r12 71,056
r9  70,307            r13 66,458
```

Pre-fix the same region hit **94,264 @ r12** and **111,148 @ r24**; now **0 of 608** rounds
exceed 94,264.

#### Defect 3 (SERIOUS): the day-mark procedure fails OPEN

The snippet added at the previous checkpoint used:

```bash
NOW=$(systemctl show truesight-autopilot -p ActiveEnterTimestamp --value --timestamp=unix)
echo "uptime h: $(( ($(date -u +%s)-NOW)/3600 ))"   # require >= 24
```

On this host (**systemd 249**), `--timestamp=unix` is **not a valid value**: `systemctl` prints
`Invalid value: unix` to stderr and returns an **empty string**. `NOW` was therefore empty and the
arithmetic evaluated `now - 0`, printing **"uptime: 498786h" (≈57 years)** →
**"VERDICT: DAY MARK REACHED"** — at a true uptime of **4h09m**.

**Had the sign-off reading relied on it, Unit 4 would have been certified after ~4 hours instead
of a day.** The failure mode is dangerous specifically because it fails *open*: an empty variable
became an enormous number, and "enormous uptime" reads as "definitely soaked long enough." A
missing measurement should never look like a passing one.

**Fix:** derive the epoch with `date -u -d "$START_H" +%s` (portable; verified below) and
**validate it before use** — abort unless non-empty and > 1e9 (~2001). The snippet also now exits
non-zero when the day mark is not reached, so it cannot silently proceed to a measurement.

Verified good: `date -d "Wed 2026-11-25 14:19:52 UTC"` → `1795616392` → uptime **4h 09m** →
correctly reports *not yet*.

**Lesson worth carrying beyond this plan:** the check that gates sign-off had **never been
executed**. A measurement procedure is code, and untested code that gates a decision deserves the
same scepticism as the system it measures. The rule: **run an acceptance check at a moment when
you know the answer must be "no."** A check that has only ever been read, never run, is an
assumption.

#### Defect 4 (ROOT CAUSE): negative echo filters lose by default — use a positive anchor

The two remaining anomalies in this pass both dissolved:

- The single `Intra-turn compaction failed` hit was a **`TOOL CALL … args={…}` line containing
  the assistant's own grep pattern** (`Intra-turn compaction (failed|backup failed`). It carries
  no `"stdout":`/`"stderr":`/`cmd=` marker, so it slipped the negative filter.
- `min=19 tokens` came from a **`CHAT RESP: len=96 tokens=19`** line — a different event type
  leaking into the round-token statistics, not an `LLM RESP round=` measurement.

**True failures 0 · true tracebacks 0 · leaks 0.**

The negative marker list has now been patched **three times**, each patch discovered only by
hand-investigating a phantom. That is the design problem: a negative list excludes what you
happen to know about, and any unlisted echo channel manufactures a phantom failure. Negative
filtering loses by default.

**Switch to a positive anchor** — count only lines matching the real log record the code emits:

```bash
J | grep -F 'INFO:autopilot:Intra-turn compacted session '
J | grep -oE 'INFO:autopilot:\[[0-9]+\] LLM RESP round=[0-9]+ .*tokens=[0-9]+'
```

Echoed copies of these strings appear **mid-line** inside JSON or `args=`, never immediately after
`INFO:autopilot:` at record start — so the anchor excludes them **structurally** instead of by
enumeration. Keep the small negative filter as belt-and-braces, but the positive anchor is what
makes the count trustworthy. **All figures in this checkpoint were produced with the positive
anchor.**

### Unit 4 — echo-filter hardening (2026-11-25 16:27Z): `"stderr":` is a third echo channel

A re-measurement at the same ~2h07m window produced **2 `Traceback` hits**, which initially
read as the first runtime tracebacks of the soak. They are both **echoes of the assistant's
own failed diagnostic commands**, captured inside JSON `stderr` fields:

- `15:24:38` — a `gh`/urllib HTTP call from a diagnostic script (`returncode: 1`)
- `16:23:55` — an `AssertionError: limits anchor missing` from a failed plan edit (`returncode: 0`)

**True runtime tracebacks in the soak window: 0.**

**The lesson is that the echo filter documented above was incomplete.** It excluded
`"stdout":` and `cmd=`, but the agent harness echoes failed commands in `"stderr":` as well —
so a traceback count built on that filter yields false positives from the diagnostic
commands *used to do the measuring*. This is the second instance of the same underlying
trap (echo-noise masquerading as runtime signal) via a different field, which suggests the
filter should be treated as a maintained list, not a fixed pair.

**Corrected canonical filter** — drop lines containing any of:

```
"stdout":    "stderr":    "returncode":    cmd=    echo-filter-marker
```

i.e. exclude `"stdout":`, `"stderr":`, and `"returncode":` (all three are JSON envelope keys
of an echoed tool result), not just `"stdout":`.

**Re-measured with the corrected filter (2h07m window):**

| Metric | Value |
|---|---|
| Intra-turn folds | **23** (was 21 at 16:25Z — +2 in ~2 min, normal cadence) |
| Real fold failures | **0** |
| True runtime tracebacks | **0** (2 matches were `stderr` echoes) |
| DSML leaks | **0** |
| Distinct sessions folded | 5 |
| Before-counts, last 22 | `85 82 63 81 63 81 63 69 64 69 69 69 73 70 69 82 76 76 62 61 66 66` |

The band is unchanged — still ~61–85 with each fold returning to ~53–76. The extra fold
extends the tail (`… 66 66`), not the top of the range, which is the healthy shape.

### Unit 4 — day-mark measurement procedure (the one remaining requirement is wall clock)

**Unit 4 asks for ~a day. Elapsed at last measurement: 2h07m.** This cannot be compressed by
effort or repeated re-measurement — the unit's remaining substance is *time*, so re-running
the harvest every few minutes produces no new evidence. Run this **once at ≥24h uptime**:

```bash
START_H=$(systemctl show truesight-autopilot -p ActiveEnterTimestamp --value)
START_E=$(date -u -d "$START_H" +%s) || { echo "FATAL: cannot parse start time"; exit 1; }
[ -n "$START_E" ] && [ "$START_E" -gt 1000000000 ] || { echo "FATAL: implausible epoch $START_E"; exit 1; }
UP=$(( ($(date -u +%s)-START_E)/3600 ))
echo "uptime h: $UP"; [ "$UP" -ge 24 ] || { echo "NOT YET: day mark not reached ($UP h)"; exit 1; }
# POSITIVE ANCHORS -- count only lines where the real log record starts.
# Echoed copies appear mid-line inside JSON/args=, never right after 'INFO:autopilot:'.
J() { journalctl -u truesight-autopilot --since "$START_H" --no-pager 2>/dev/null; }
echo "folds:        $(J | grep -cF 'INFO:autopilot:Intra-turn compacted session ')"
echo "failures:     $(J | grep -cF 'INFO:autopilot:Intra-turn compaction failed')"
echo "tracebacks:   $(J | grep -cF 'INFO:autopilot:Traceback')"
echo "leaks:        $(J | grep -cE 'INFO:autopilot:.*(DSML|special[.]token leak)')"
echo "before-counts: $(J | grep -F 'INFO:autopilot:Intra-turn compacted session ' \
      | grep -oE 'session [a-f0-9]+: [0-9]+ ->' \
      | sed -E 's/.*: ([0-9]+) ->/\1/' | tr '\n' ' ')"
```

**Pass criteria (day mark).** Folds > 0 · failures **0** · true tracebacks **0** · leaks **0** ·
before-counts with **no upward trend** across the window (band bound, not a slope).

**Fail criteria.** Any real failure/leak → set `CONTEXT_INTRATURN_COMPACTION_AUTO=0` to roll
back with no redeploy, then investigate. Before-counts trending upward day-over-day → the
fold is not keeping up and thresholds need re-tuning (see the `keep_last_k_rounds` /
token-threshold follow-up).

### Unit 4 soak — 2h05m checkpoint (measured 2026-11-25 16:25Z, echo-filtered)

Extends the ~15-minute window below. **Every figure here was echo-filtered first** (lines
containing `"stdout":` or `cmd=` dropped) — the phantom-failure trap documented in this file,
which a prior checkpoint was nearly misread by.

Window: service up 2026-11-25 14:19:52Z → **2h 05m**.

| Metric | Value |
|---|---|
| Intra-turn folds (echo-filtered) | **21** |
| Distinct sessions folded | 5 |
| Real fold failures | **0** |
| Intra-turn tracebacks | **0** |
| DSML / special-token leaks | **0** |
| Rounds measured (`LLM RESP round=… tokens=…`) | **282** |
| Prompt tokens | min **39,600** · mean **55,102** · max **77,474** |
| Rounds over 94,264 (the pathology) | **0** |
| Rounds over 72,391 (the other original trigger) | 3 |

**Band test — still holding.** Before-counts chronological: `85 82 63 81 63 81 63 69 64 69 69 69 73 70 69 82 76 76 62 61 66` → band ~61–85, returning to ~53–76 after each fold. No upward drift.

**The token curve now descends after the threshold engages** — stronger than a merely flat band:

```
round  6: max 75,075      round 12: max 70,671
round  8: max 76,721 <-peak    round 16: max 69,720
round 10: max 69,088      round 24: max 71,921
```

Post-fix, rounds ≥10 are *cooler* than rounds 6–8. Pre-fix, the same region reached
94,264 @ r12 and 111,148 @ r24. Bounded **and** trending down is the designed behaviour.

**Token-threshold question — now measured, and the answer is the opposite of the guess.**
Round-1 prompt tokens: **min 39,600 / max 66,104** (n=38). Recomputed at the 4h09m checkpoint
on 608 rounds with the positive-anchor filter: **2 rounds sat at or below 40,000**. So the token arm is satisfied on **99.6%** of rounds — it is not a discriminator at
all, but it is *always on* rather than *never firing*. This **corrects** the earlier
"min round-1 baseline is 43,121" figure recorded in `OPEN_FOLLOWUPS.md` (a smaller sample;
the larger sample dips just under 40K) and **inverts** the plan's earlier hypothesis that
"round_threshold=8 is probably doing all the folding". See the refined paragraph above.

**Why the gate is still open (unchanged):** the unit asks for **a day**; this is 2h05m. The
signals are healthy and the band holds, but a slow regression (before-counts trending upward
across days) would only appear on a longer window, and "a folded turn still completes" remains
established only empirically — never by replay (Unit-0 fixtures lack `reasoning_content`).
**Sign-off is the governor's, not the autopilot's.**

### Unit 4 soak evidence (measured 2026-11-25, ~15 min after the 14:19:52Z start)

Source: `LLM RESP round=N tools=N tokens=X` journal lines — the authoritative
per-round prompt-token count — over **177 real rounds**. This is the number the
gate turns on, and it is flat where it used to climb.

| round | pre-fix (the motivation) | post-fix max observed |
|---|---|---|
| 6–8 | climbing | 75,075 / 77,474 / 76,721 |
| 12 | **94,264** | 70,671 |
| 24 | **111,148** | **71,921** |

- **Absolute max post-fix: 77,474** vs pre-fix 111,148 → **−30%**
- **Rounds exceeding 94,264: 0**, out of 73 rounds at round≥8
- Post-fix r≥8 sits in a stable 66–77K band rather than climbing every round —
  the sawtooth is bounded, which is the designed behaviour
- Health: **16 folds, 0 exceptions, 17 inter-turn compactions, 0 DSML leaks**

**Persistence question — resolved, and the earlier alarm was my own bug.** A prior
note reported "0 fold markers persisted" using a `startswith("[TURN IN PROGRESS")`
test. Re-checked as a **substring**, the sessions carry 1 / 3 / 2 markers. The
marker was never at the start because `_sanitise_tool_messages`' user-merge pass
(the same behaviour Unit 3 documented) folds it into the preceding `user`
message. **Folding does persist to disk correctly** — the prefix test was wrong,
not the code.

**Limits on this evidence (why the gate stays open):** the window is ~15 minutes,
not the day the unit asks for. And `min=43,121` tokens even at round 1 suggests
the prompt+tools baseline already exceeds
`CONTEXT_INTRATURN_TOKEN_THRESHOLD=40000`. The 2h05m checkpoint below **refines this
and partly inverts it**: across 282 rounds the token arm (`tokens >= 40000`) is
satisfied on **281 of 282 (99.6%)**, so it is not "inert" in the sense of never
firing — it is **effectively always true**, which collapses the `OR` toward "fold as
soon as anything is foldable". The binding limiter is therefore probably
`keep_last_k_rounds=4` (a round only becomes foldable once ~5 complete rounds exist),
**not** `round_threshold=8`. Recorded in `OPEN_FOLLOWUPS.md`; still not a change to make
mid-soak.

**Unit 4 soak — verification procedure, and a trap that produces phantom failures
(2026-11-25, first ~1h checkpoint).**

Interim measurement (service up since 14:19:52Z; ~65 min):

| Metric | Value |
|---|---|
| Intra-turn folds | **18** |
| Sessions folded | 5 |
| Real fold failures | **0** |
| Chat requests handled | 25 |
| DSML / special-token leak in output | **0 hits** |
| error-level journal lines | 1 (unrelated, pre-existing) |

**The band test — this is the real acceptance signal, not the fold count.** If the
fold is working, the *before* message-count at each fold should sit in a stable
band and never drift upward; if it is not working, the before-counts climb
monotonically toward the original pathology. Observed before-counts, chronological:

```
85 82 63 81 63 81 63 69 64 69 69 69 85 73 70 69 82 76
```

That is a **band, not a slope** — it hovers ~63-85 and returns to ~68-76 after each
fold. The single longest session's own trajectory:

```
85->74  82->73  81->73  81->73  85->74  76->68
```

Compare the pre-fix pathology this plan exists to remove: **94,264 tokens @ r12**
and **111,148 @ r24**, each inside one still-open turn with *no* upper bound.
So the band test is the claim Unit 4 must actually establish, and it is currently
holding. Continue sampling; a band that stops holding (before-counts trending up
across days) is the regression signature, and that — not an absence of log
errors — is what should reopen this plan.

**TRAP — do not verify absence-of-errors by grepping journald for error words.**
A check of the form `journalctl -u truesight-autopilot | grep -icE 'intra-turn.*(Traceback|ERROR|failed|exception)'`
returned **2**, which looks like two fold failures. Both were **phantom**: they
matched *this autopilot's own echoed tool output* — a prior `ssh_run` whose stdout
contained the literal phrase "intra-turn exception" was logged by journald and
then matched by the grep. journald contains the agent's own transcript, so any
error-word search is self-referential and will "find" failures that consist
entirely of the search itself. Verify via the code's **own** emitted log lines
(`Intra-turn compacted session …`, `Intra-turn compaction backup failed …`) and by
exit-path counters, never by keyword-scanning echoed output.

**Backup growth continues** as the retention follow-up predicted: 6,399 -> 6,420
files (~21 per 10 min ≈ ~3k/day, ~0.4 GB/day at the observed ~138 KB/file). Disk
is at 35% so this is not urgent, but at that rate the retention fix becomes
worth scheduling rather than merely noting.

**Unit 4 checkpoint 2 (2026-11-25 ~18:31Z) — two corrections, one of them to my own
method.**

**Correction 1 — the soak is ~20h, not the ~4h reported at checkpoint 1.** I measured
from the current process start (14:19:52Z) and missed that earlier processes had
already been folding. First genuine fold in journald: **Nov 24 23:25:58**; KAN-30's
60-day audit places it at **Nov 24 21:58:11**. Latest: Nov 25 18:30:39. That is
**~20.5h of continuous soak and 223 folds**, i.e. the 24h window closes around
**Nov 25 21:58Z**. Checkpoint 1 understated soak length by ~16h because I used
process start as the soak start; the soak begins at the *first fold*, which survives
restarts.

**Correction 2 — my band test was too weak, and it hid a real cost.** Checkpoint 1
treated "before-counts sit in a stable band" as success. A stable band has **two**
readings, and I only tested for one:

1. the fold holds a ceiling while the turn does genuinely new work — *good*; or
2. the fold re-folds the same content repeatedly because it removes only the
   minimum — *churn*.

Per-session fold counts over just one hour expose reading 2:

| Session | Folds | Trajectory |
|---|---|---|
| `a8209b9a63b1` | **27x** | `62>53 61>53 61>53 61>53 64>56 64>56 64>56 64>56 73>65 73>63 63>54 62>54 …` |
| `db6d3aa764c5` | 7x | `66>58 66>58 71>63 71>63 71>63 63>55 83>75` |
| `81dbcd615f3a` | 5x | `79>70 78>70 78>70 77>68 76>68` |
| `434b53fd293b` | 4x | `74>65 73>65 73>65 73>65` |

The repeated identical pairs (`61>53` then `61>53`, `66>58` then `66>58`) are the
tell: the fold removes exactly the **K=4 rounds (~8 messages)** it is permitted to,
the turn adds ~8 back, and it folds again ~4 rounds later — roughly every 2 minutes
on a long-running session. Note `db6d3aa764c5` 7x shows `71>63` **three times
identically.**

**What this does and does not mean.** The *primary* goal still holds — before-counts
never climb toward the 94K/111K pathology, so there is no unbounded growth. What is
*newly* measured is a **secondary cost** the plan never specified a metric for:
- **summariser churn** — one LLM summariser call per fold, ~27/hour on a busy session;
- **summary depth** — each fold extends the running `[TURN IN PROGRESS — EARLIER
  ROUNDS SUMMARY]` entry, so a session folding 27x may be building a
  summary-of-a-summary 27 levels deep. `default_round_summarizer` re-summarises the
  prior summary, so **semantic drift with depth is a live risk, unquantified.**
Filed in `OPEN_FOLLOWUPS.md`.

So Unit 4's acceptance criterion must gain a **second dimension**: not only "does
pressure stay bounded" (yes) but "at what summariser cost and what summary depth"
(unknown, and now measurable). A fold count of 223 with per-session spikes to 27/h is
exactly the evidence needed to size it.

**Measurement trap repeats.** The per-session awk parse again yielded a phantom
"session `Nov`" — a session id extracted from echoed log text, same self-referential
journald trap recorded above. This is the second occurrence; any parser reading
journald must exclude lines that are themselves tool output.

**Unit 4 checkpoint 3 (2026-11-25 ~18:35Z) — clean failure record, but my own
instrumentation was wrong twice.**

**Soak window is NOT closed.** From the audit first-fold (Nov 24 21:58:11Z):
**20.58h elapsed, 3.42h remaining**; 24h closes ~**Nov 25 21:58Z**. (From the
journald first fold, 19.11h / 4.89h remaining.) So the gate cannot close this turn
regardless of activity — this is elapsed-time-gated, and no action of mine shortens
it.

**The failure record is genuinely clean, now verified by the code's *own* log line**
(`INFO:autopilot:Intra-turn compacted session …`) rather than keyword scans:

| Metric | Value (entire history, since Nov 20) |
|---|---|
| Folds | **219** |
| Fold/backup `WARNING`/`ERROR` lines | **0** |
| Distinct sessions folded | 17 |
| Max folds on one session | **79** (`a8209b9a63b1`, a month-old session) |

**Correction — all 3 apparent "DSML leaks" were phantom.** `grep -icE '＜｜|DSML'`
returned 3. Every one was a false positive: two were `ssh_run` **tool-call arguments**
from a session that was literally grepping for the string `DSML` in `app/main.py`, and
the third was **this turn's own grep matching itself** in journald. The real leak
count over the soak is **0**. This is the same self-referential trap documented in
checkpoint 1, now hit a second time on a different query — reinforcing that **no
journald keyword scan can measure output quality**; only structured/emitted signals
can.

**Correction — a "corrupted session" that was my parser.** `sessions/a8209b9a63b1.json`
is 121 KB, but my reader reported **0 messages** because it looked for `messages` /
`history`, whereas the real structure nests them at **`full_history` (62 messages,
healthy)**. I nearly reported that 79 folds had emptied a session file. It had not.
The file is fine. This is the third instance this plan of **measurement error
masquerading as system defect** — worth stating plainly: on this plan, a surprising
reading has more often been a broken query than a broken feature.

**Churn refined — bursty, and concentrated exactly on the target workload.** The
79-fold lifetime total for `a8209b9a63b1` is unremarkable over a month; what
checkpoint 2 measured was **27 folds inside a single ~1h slice**. Both are true, and
the reconciliation matters: churn is not continuous background cost, it **spikes
during long investigation-heavy turns** — i.e. precisely the workload this feature
exists to serve. So the summariser cost per fold is highest exactly where the feature
is most valuable, which is the right place to look but not an argument against it.

**Summary depth remains UNMEASURED — and marker counts are not depth.** Measuring
`EARLIER ROUNDS SUMMARY` occurrences across live session files gives **497 markers
across 114 sessions, max 21 in one session** (`2149009ce21b`). This is **not** nesting
depth and must not be reported as such: k markers could equally be k *separate open
turns each folded once*, or genuine nesting. Distinguishing the two requires checking
whether a marker appears **inside another summary's text**, which no current
instrumentation records. The checkpoint-2 instrumentation ask therefore stands,
unsatisfied — this is the one substantive quality question still open on the feature.

**New resource finding — debug logs, distinct from the backup bloat.** `sessions/*_debug.log`
totals **203 MB** (largest 8.1 MB), separate from the ~1.2 GB of `pre-compact`
backups. Disk at **35% (55 G used / 101 G free)**, so not urgent; noted alongside the
retention follow-up since both are unbounded operator-disk growth on the same box.

**Where Unit 4 actually stands:** primary goal demonstrated over 219 folds with a
**clean** failure record and **0** real leaks; soak 20.58h/24h. The single open
quality question is summary fidelity-vs-depth, which cannot be answered from existing
logs. Gate remains **governor-sign-off pending**, and closes no earlier than ~21:58Z.

**Unit 4 checkpoint 4 (2026-11-25 ~18:38Z) — reading the code DISPROVES my own
checkpoint-2 risk, and replaces it with a better-founded one.**

Soak still not closed: **20.62h / 24h, closes 21:58:11Z** (~3.4h out). Clock-gated.

**I was wrong twice in checkpoint 2. Both errors came from inferring behaviour from
log patterns instead of reading the function.**

1. **"Summariser churn — one LLM call per fold, ~27/hour."** WRONG.
   `default_round_summarizer` (app/context_compaction.py:360) has **no LLM call at
   all** — its docstring states "No LLM call — same text-reuse philosophy as the
   inter-turn path." It walks the folded rounds and emits one line per round (the
   assistant's pre-call text + tool names + a 200-char result snippet), reusing
   `extract_done_this_turn` where available. So a fold costs **string formatting**,
   not a model round-trip. There is no per-fold latency/token cost on the live turn's
   critical path, and the "cheap fix: raise token_threshold to reduce LLM calls" I
   proposed was solving a problem that does not exist.

2. **"27-deep summary-of-a-summary, semantic drift with depth."** WRONG.
   Measured directly against the real module (`compact_open_turn`, K=2,
   round_threshold=4, three successive folds in ONE turn):

   | Fold | messages | summary msgs | each nested? | total summary chars |
   |---|---|---|---|---|
   | 1 | 30 | 1 | **flat** | 736 |
   | 2 | 31 | 2 | **flat** | 1,627 |
   | 3 | 8 | 3 | **flat** | 2,518 |

   Every summary contains **exactly one** header — no summary is ever re-summarised.
   The mechanism: `default_round_summarizer` only consumes `assistant`/`tool` messages
   in its region, and the prior summary is `role: "user"`, so **it is never fed back
   into the next summary.** Semantic drift-by-depth therefore **cannot occur**. That
   was the fidelity risk I said I'd lose sleep over; it is disproven.

**The real, correctly-stated risk — flat summaries ACCUMULATE.** Prior summaries are
**not** dropped and **not** nested: they persist alongside newer ones. So while raw
rounds stay capped at K, the **summary region grows monotonically with fold count** —
736 → 1,627 → 2,518 chars across three folds (≈+890 chars/fold). Context is
**bounded in the round dimension but not in the fold-count dimension.**

Concretely, on the observed churn session (`a8209b9a63b1`, 27 folds in one hour), a
single sustained turn could accumulate on the order of **~24,000 chars ≈ 6,000 tokens**
of stacked summaries. That is far from the 94,264-token pathology and does not
threaten the primary goal — but it means the fold is **not** a strict constant-space
operation, and the drift is silently upward.

**Secondary mechanism note (worth a code comment, not a change):** the synthetic
summary is `role: "user"` with no `tool_calls`, which is exactly what
`find_open_turn_start` looks for. On a subsequent fold it can therefore be taken as
the *turn opener*, so each fold re-anchors on the previous summary. This is consistent
with the observed accumulation and with the 31→8 message collapse at fold 3; it makes
"the current turn" a moving anchor rather than a fixed one.

**Corrected follow-up recommendation (supersedes checkpoint 2's):**
- **Drop** the "reduce LLM calls by raising token_threshold" idea — no LLM calls exist.
- **Keep** fold rate-limiting, but reframe the reason: it bounds **summary
  accumulation growth**, not summariser cost.
- **Add a summary-region cap** (e.g. collapse all prior summaries into one, or cap
  total summary chars) so the fold is genuinely constant-space with respect to fold
  count.
- Marker counts from checkpoint 3 (497 / max 21) are now explained: **distinct flat
  summary messages**, i.e. fold counts — **not** nesting. That reading was correct.

**Method lesson, stated plainly for whoever closes this gate:** three consecutive
checkpoints produced confident statements about behaviour that only reading
`default_round_summarizer` could settle. Logs showed *how often* the fold fired; they
could never show *what it cost or whether it nested*. Behaviour claims need the source,
not a pattern match.

**Unit 4 checkpoint 5 (2026-11-25 ~19:35Z) — strict band test PASSES; accumulation
measured on real sessions, which corrects #1929 in both directions.**

**Window still open:** audit first fold (Nov 24 21:58:11Z) → **21.57h elapsed,
2.43h remaining**, closes ~**Nov 25 21:58Z**. Journald first fold: 20.10h / 3.90h
remaining. Gate remains elapsed-time-bound and governor-gated.

**1. The owed strict band test now runs cleanly and PASSES.** Built on
`journalctl -o json` with `MESSAGE` required to be a `str`, no newlines, no
`stdout`/`TOOL CALL` wrapper text, matched against the **full emitted line shape**
(including the trailing `(round_threshold=N, token_threshold=N)`):

| Metric | Value (n=219 strict folds, ~21.6h) |
|---|---|
| Before-count min / max / mean | **34 / 99 / 69.6** |
| First-quartile → last-quartile | 69.4 → **68.39** |
| **Trend** | **−1.0 messages (flat)** |
| Folds with before-count > 100 | **0** |
| Folds with before-count > 200 | **0** |
| Strip per fold | 7–13 messages |
| Distinct sessions | 17 |

**This is the acceptance test the plan has been missing, and it passes:** 219 real
folds over ~21.6h, flat before-count distribution, **never above 99 messages**, no
upward drift. The 94,264 / 111,148-token pathology does not recur.

**2. Real-session accumulation — measured, not extrapolated.** #1929 measured
accumulation synthetically (3 folds, K=2). Measured now across **production session
files** (count of `role:"user"` summary messages + total chars per session):

| Finding | Value |
|---|---|
| Sessions with ≥2 summaries | **12** |
| **Max summaries in one session** | **5** (`da5590e92b3d`) |
| **Max total summary chars** | **23,542** (~5,900 tokens) |
| Real per-summary size | **3,788–6,485 chars** |

**3. Correction to #1929 — the per-fold growth figure understates real size ~6×.**
#1929 extrapolated **+890 chars/fold** from a synthetic K=2 run whose summaries were
736–890 chars. Real production summaries average **~5,500 chars**, i.e. ~6× larger.
Recomputing #1929's own scenario with real sizes: **27 folds × ~5,500 chars ≈ 148,000
chars ≈ 37,000 tokens**, not the stated ~24,000 chars / ~6,000 tokens. Still well under
the 94,264 pathology, but materially bigger than #1929 reported. **The direction of
#1929's finding is right; its magnitude was too optimistic.**

**4. Correction in the other direction — accumulation is bounded per *turn*, and
resets.** #1929 said the summary region "grows monotonically with fold count." True
**within a single open turn**, but not across a session's life: observed max is **5
summaries in any session**, and the 79-fold session `a8209b9a63b1` currently holds
**fewer than 2 summaries**. The summary region is cleared when a turn completes, so
accumulation is bounded by the *open turn*, not by lifetime fold count. Practical
worst case observed: **23.5K chars ≈ 5.9K tokens ≈ 6% of the pathology.**

**Net effect on risk:** #1929's "cap the summary region" fix is **correct but low
priority** — the observed ceiling is ~6% of the problem it guards against, and it
self-resets at turn boundaries. Insurance, not urgent. Order stands: cap summaries →
rate-limit folds.

**Measurement note (fifth instance).** The strict band test now produces 219 where the
loose method gave 226 and my last strict run gave 218 — the count drifts by ±1 as new
folds land, and only the full-line-shape match is stable. Every loose count in
checkpoints 1–3 remains ±8 high and should be read that way.

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
