# Build → Document → Story

A three-artifact pipeline that every meaningful change at TrueSight
runs through. First named explicitly by Gary on 2026-05-13 as he
observed three of his own arcs (DApp notification bell, Partner Poke
Scheduler, autopilot self-healing) each producing the same trio of
outputs.

The pattern isn't novel as a concept — software shops have always
shipped code, written docs, and (sometimes) blogged about lessons.
What's specific to TrueSight is the **discipline** of running every
arc through all three by default and treating each as its own
deliverable, not as overhead on the first.

This file is the spec for that discipline.

---

## The three artifacts

Each artifact serves a **different audience** and degrades poorly
when fused with the others:

### 1. Production artifact — for operators of the running system

The code, config, sheet, or deployed change. Lives in the working
repos: `dapp`, `tokenomics`, `truesight_autopilot`, `agroverse_shop`,
etc. PR-reviewed, merged, deployed, used.

Audience: the operator (Gary today; future operators tomorrow)
running the system day-to-day.

What it must contain:
- The change itself (code, schema, config).
- Smoke verification that the change works in production.
- Operator-facing release notes inside the PR description (manual
  setup needed, env vars, gotchas) — sufficient to deploy without
  reading the source.

What it must **not** contain:
- Cross-cutting architecture explanations (those belong in the
  documentation artifact).
- Backstory about *why* the pattern matters (that belongs in the
  story artifact, when it generalizes).

### 2. Documentation artifact — for the next session / next operator

A `.md` file in `agentic_ai_context` that captures the institutional
knowledge not derivable from reading the production code. Reviewed
in its own PR (not bundled with the code change), so the doc gets
the same critical eye the code does.

Audience: the **next** session — could be the same operator a month
later, a different LLM with a fresh context window, a new human
collaborator. They've never seen this conversation.

What it must contain:
- The architecture / contract / convention the production change
  established or modified.
- Worked examples drawn from real shipped instances.
- Anti-patterns surfaced during the build (so the next session
  doesn't re-litigate them).
- Pointers to the production artifact (PR URLs, file paths) so
  readers can verify any claim against the code.

What it must **not** contain:
- Code that should be in the production repo (don't dual-source).
- Conversational shape ("I asked Gary, then he said…") — write for
  cold readers, not transcript readers.
- Editorial voice for outsiders (that belongs in the story
  artifact).

### 3. Story artifact — for outsiders aligned with the mission

A blog post on `truesight.me/blog` (typically as a `Field Signals`
or `Operator Notes` series entry). Long-form, voiced, and shaped
to land for a reader who doesn't operate TrueSight day-to-day but
might be running their own version of the same problem.

Audience: aligned outsiders (other operators, advisors, the wider
community in Beer Hall, someone who'd find the lesson useful even
if they never use Edgar / DApp / autopilot specifically).

What it must contain:
- A concrete-fact-and-paradox opener — see
  `EDITORIAL_TONE.md` §1.1 / §1.7.
- A specific shipped instance as the worked example (not a generic
  "here's how we'd do it" essay).
- The lesson generalized to other contexts (so the post is useful
  to readers who'll never run our exact stack).
- A contemplative pull-back close, not a CTA.

What it must **not** contain:
- The full code listing or step-by-step reproduction (that's the
  production artifact's job).
- Marketing-flavored claims (TrueSight blog voice is quiet
  contrarianism, not announcements).
- Credit-grab framing ("we built X first") — see banned-vocabulary
  list in `EDITORIAL_TONE.md` §1.5.

---

## The sequence is not always strict

Most arcs run **build → document → story** in that order — code
ships, then the doc captures it, then (sometimes) a story emerges.
But the sequence flexes when the work warrants:

- **Document → build → story** when the architecture is novel
  enough that writing the plan up front is the cheap way to find
  scope problems early. Both `PARTNER_POKE_SCHEDULER_v0.md` and
  `MULTI_LLM_ORCHESTRATION.md` were written before any of the
  code they describe.
- **Story → document → build** is rare but legitimate when a
  blog post crystallizes a thesis the operator wants to act on
  (the May 12 Beer Hall vision Gary sketched produced the
  AI-first-supply-chain framing that's now shaping the next
  several arcs).

The discipline isn't about *order*; it's about ensuring **all three
artifacts get produced** for any work that warrants them.

---

## When to skip the story artifact

Most everyday production work does not warrant a blog post. The
filter:

- The lesson **generalizes** beyond TrueSight's specific stack.
- The shipped instance is **specific enough** to be a real receipt
  (not vague "we should do X someday").
- The operator's reaction at the end of the arc is **"this is
  worth telling outsiders about"**, not just **"this is shipped."**

If only the documentation artifact warrants writing — fine, ship
two artifacts. The discipline is "all three when warranted," not
"three for everything."

---

## Worked examples — three artifacts, one arc each

### Autopilot self-healing (May 13, 2026)

| Artifact | Where |
|----------|-------|
| Production | `truesight_autopilot` PRs #38, #39, #40, #41 (outbound + classifier + mapping + dedup); deployed to `truesight-autopilot` EC2 host |
| Documentation | `AUTOPILOT_CODE_MODIFICATIONS.md` §§9–11 |
| Story | `truesight.me/blog/posts/the-system-that-broke-is-the-system-that-proposes-the-fix.html` (Field Signals · #4) |

### DApp notification bell + Partner Poke Scheduler (May 12, 2026)

| Artifact | Where |
|----------|-------|
| Production | `dapp` PRs #233, #234, #236, #242, #243, #247, #248, #249, #250 (bell widget + 3 sources + bell-deep-links + typeahead); `tokenomics` PR #286 (`partner_poke_drafts.gs`) |
| Documentation | `DAPP_NOTIFICATION_BADGE.md`, `PARTNER_POKE_SCHEDULER_v0.md` |
| Story | `truesight.me/blog/posts/the-shared-memory-is-the-moat.html` (Field Signals · #2) — the broader thesis that contains both as instances |

### Currency Conversion event (May 7, 2026)

| Artifact | Where |
|----------|-------|
| Production | `dapp/currency_conversion.html` + `tokenomics` GAS processor + Edgar webhook |
| Documentation | (entry in the relevant `tokenomics/SCHEMA.md` and `agentic_ai_context/PARTNER_CHECK_IN_IMPLEMENTATION.md` cross-references) |
| Story | (skipped — operational utility, no generalizable lesson worth blogging) |

The skipped third artifact is correct here, not a gap. Currency
conversion is a useful tool for the team; the lesson behind it
(double-entry offchain accounting) was already covered in
*Plug-and-play architecture: why every service reads from one
sheet*.

---

## Why this discipline matters

Each artifact failing produces a specific kind of debt:

| Artifact missing | Debt produced |
|------------------|---------------|
| Production       | The change isn't real. The story is vapor; the doc is fiction. |
| Documentation    | Institutional knowledge leak. The next session re-derives the architecture from the code, often poorly, often re-litigating decisions that were already made. |
| Story            | Aligned outsiders never see the lesson. The DAO's public surface drifts toward only being the most recent shipped feature, never the *patterns* the work embodies. |

The Build → Document → Story discipline keeps all three debts from
accumulating. It doesn't make any single arc faster. It makes the
*next* arc faster, because the next session can start where this
arc ended.

---

## Anti-patterns

1. **Code without doc** — the most common debt. The code ships, the
   knowledge stays in the operator's head, the next session
   re-derives it. Especially toxic for cross-repo conventions
   (e.g. the `AI/proposed fix` label convention spans `truesight_autopilot`,
   `dapp` Gmail, every repo autopilot might open a PR against
   — undocumented, this looks like noise; documented, it's a
   contract).
2. **Doc without code** — premature optimization. Writing the
   doc for a system that hasn't shipped invites the doc to drift
   from reality before reality exists.
3. **Story without code** — vapor. TrueSight's blog credibility
   comes from *receipts*: every Field Signals post points at a
   shipped instance. A story without a corresponding shipped
   thing reads as marketing and undermines the next post that
   does have a receipt.
4. **Bundling the three into one PR** — the artifacts have
   different review needs. Code review checks correctness;
   documentation review checks completeness; story review checks
   voice. Bundle and you get sloppy reviews on at least two of
   the three.
5. **Treating the doc as overhead on the code** — when the code
   ships and the doc is "I'll write that next week," the doc
   doesn't get written. Make the doc its own PR, opened the same
   day or the next day, with the same merge urgency.

---

## Adding a new arc — checklist

When starting a new arc that's likely to warrant the full pipeline:

- [ ] **Production** — what's the smallest shippable unit that
      validates the architecture? PR open within the working
      session.
- [ ] **Documentation** — what convention / contract / decision
      did this establish that the next session needs to know?
      `agentic_ai_context/<NAME>.md` opened as its own PR.
- [ ] **Story** (optional, decide consciously) — does the lesson
      generalize beyond TrueSight's specific stack? If yes, draft
      a Field Signals or Operator Notes post following
      `EDITORIAL_TONE.md` §1.
- [ ] **Cross-links** — production PR description points at the
      doc; doc points at the production PRs; story points at
      both.
- [ ] **Operator review** — for the story artifact specifically,
      preview locally before merging (`localhost:8095/blog/posts/<slug>.html`)
      so the voice match gets a final eye before publish.

---

## Related context

- `EDITORIAL_TONE.md` — voice rules for the story artifact.
- `MULTI_LLM_ORCHESTRATION.md` §1.2 — the doc-as-handoff principle
  (write the plan as a doc before code, especially for non-trivial
  builds spanning ≥3 repos).
- `FOUR_WIRE_LOOP_PATTERN.md` — the technical loop pattern this
  pipeline often produces stories about.
- `feedback_auto_log_dao_contribution.md` — the contribution
  ledger is a fourth-class artifact (every shipped arc gets a
  `[CONTRIBUTION EVENT]` row that captures the time + PRs in
  one place); treat as the receipt for the production artifact.

*Last refreshed 2026-05-13. Refresh when a new arc surfaces a
pattern variant worth naming, or when an anti-pattern recurs in
production work that's worth adding to §"Anti-patterns".*
