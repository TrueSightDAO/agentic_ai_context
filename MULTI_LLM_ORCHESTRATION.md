# Multi-LLM orchestration — plan-then-implement, model tiering, handoff prompts

How TrueSight operates a fleet of LLM "engineers" (Claude, Copilot,
Kimi, Grok, Gemini, Codex, Cursor agents, etc.) across the same
codebase without context lock-in, token waste, or single-model
dependency. This is the operational playbook — strategic framing
lives in `CMO_SETH_GODIN.md`; voice/style lives in `EDITORIAL_TONE.md`.

The pattern emerged from a hard constraint: unlike VC-backed teams,
TrueSight cannot afford to burn through frontier-model tokens on every
task. So we organize the LLM fleet the way a lean engineering org
organizes humans — by seniority, by scope, by handoff. The frontier
models are senior engineers; the cheaper, faster, smaller-context
models are junior engineers. Both are useful; mis-assigning the work
is what burns money.

---

## 1. The four principles

### 1.1 `agentic_ai_context` is the shared substrate — model-agnostic

Every LLM working on the workspace reads from and writes to the same
docs in [TrueSightDAO/agentic_ai_context](https://github.com/TrueSightDAO/agentic_ai_context).
That repo is the institutional memory. It belongs to no model.
Whichever LLM happens to be loaded next can ramp in by reading the
relevant files, just like a new human engineer reading an onboarding
folder.

Consequence: when one model runs out of context window, gets rate
limited, or simply costs more than the task warrants, swapping in
another is cheap. The model is the contractor; the docs are the
employer's continuity.

### 1.2 Plan as a written document *before* writing code

For any non-trivial implementation, the assigned LLM produces a
**plan document first** — typically in `agentic_ai_context/` or
inside the relevant repo. The plan covers: goal, scope boundaries,
the file/system surface area, the implementation steps, the
validation steps, and the failure modes.

Why this matters in a multi-LLM world:

- **Resilience to interruption.** If the network drops, tokens run
  out, or the model is mid-implementation when context overflows,
  the next session (same model or different) can pick up from the
  written plan instead of restarting cold.
- **Sanity check on scope.** A model that writes the plan often
  discovers mid-plan that it has bitten off more than its context
  window can chew. That discovery is *much* cheaper at the planning
  stage than at the implementation stage.
- **Reviewable surface.** The plan is a thing Gary (or any peer
  reviewer) can react to in three minutes instead of waiting for the
  full implementation to read the actual diff.

Anti-pattern: "let me just start coding and see how it goes." With
a single human engineer that's sometimes fine. With a fleet of LLMs
of varying context capabilities, it produces orphaned half-implementations
that nobody can pick up.

### 1.3 Tier models like an org chart, not a leaderboard

Frontier benchmarks are noise for this decision. What actually
matters operationally:

| Tier        | Examples (mid-2026)                             | Best for                                                            |
|-------------|--------------------------------------------------|---------------------------------------------------------------------|
| Architect   | Claude Opus 4.x (1M ctx), GPT-5 long-ctx        | Loading the whole codebase or `agentic_ai_context`, designing systems, writing the plan, untangling cross-cutting bugs |
| Senior      | Claude Sonnet 4.x, Gemini 2.x Pro, Grok 4       | Implementing within a single subsystem after the plan is set; review and revision; first-pass refactors |
| Junior      | Claude Haiku 4.5, GPT-5 mini, DeepSeek, BigModel | Narrow, well-defined tasks: rename a column across a file, run a script, fill in a template, lint cleanup |
| Specialist  | Codex, Cursor agents, Copilot, Whisper, Replit  | Domain-bound work: in-IDE completion, transcription, sandboxed exec |

The rule of thumb:

- **Architect tier** writes the plan and the hard parts.
- **Senior tier** implements the bulk of the plan after it's been
  set.
- **Junior tier** executes well-scoped tasks the senior or architect
  hands back to it (often via a prompt the architect drafts).

Mis-assignment costs are asymmetric:

- Assigning a *junior* to architect-tier work → wasted tokens,
  half-baked plan, time lost in re-do.
- Assigning an *architect* to junior-tier work → 10× the cost,
  3× the latency (frontier models are heavily utilized = slow), and
  zero quality improvement. This is the more common mistake.

### 1.4 Cost discipline is a feature, not a constraint

The motivating analogy: in 2014, Gary scaled a product team to ~30
engineers and designers on freelancer.com over a month, then scaled
it back down three months later when the work cleared. The
infrastructure pattern is the same: spin up the LLM (or three) you
need for the task, get the work done, spin it back down. Don't keep
one giant model on retainer for every task it could plausibly do.

This is why the cheap/obscure models still matter: they get specific
work done faster and with less lag than the frontier models, which
are heavily loaded by everyone else.

---

## 2. The handoff prompt — switching models mid-task

When an LLM is about to hit context overflow, token limits, a rate
ceiling, or simply isn't the right tier for the next step, the
correct move is **not** to restart fresh in another model. The
correct move is to ask the current model to generate a handoff prompt.

### 2.1 What goes in a handoff prompt

The current model writes a self-contained brief for the receiving
model. At minimum:

1. **Goal:** What the original task was.
2. **State so far:** What's been done — files touched, decisions
   made, intermediate artifacts created. Be specific (paths, function
   names, commit SHAs).
3. **Outstanding work:** What's left, in execution order.
4. **Open questions:** Anything the current model is uncertain about
   and wants the next model to verify or decide.
5. **Context files to load:** Which `agentic_ai_context/*.md` files
   the next model should read before resuming, and any in-repo docs
   that capture decisions already made.
6. **Constraints:** Memory entries, feedback rules, anti-patterns
   identified during the session.

### 2.2 When to hand off upward vs. downward

- **Upward** (junior → senior, or senior → architect) when the
  scope turns out larger than the current model's context window,
  or when a cross-cutting bug needs a wider view.
- **Downward** (architect → senior → junior) once the plan is set
  and the remaining work is well-scoped implementation. This is the
  expensive-to-cheap move that saves the most money.

### 2.3 What not to do

- Don't keep the same model going just because the chat is open.
  Sunk-context is not a reason to keep paying frontier prices for
  junior-tier work.
- Don't restart cold in a new model without a handoff prompt. The
  receiver will spend more tokens rebuilding state than the handoff
  prompt itself costs.

---

## 3. Task definition before model assignment

Before assigning a task to any model, the task should be defined as
a structured record:

```
- Title:           Short imperative ("Add Warehouse Manager picker to currency_conversion.html")
- Why:             Business reason in one sentence
- Surface area:    Files / repos / sheets the task will touch
- Scope boundary:  What is explicitly out of scope
- Definition of done: How we'll know it's finished
- Tier hint:       Architect / Senior / Junior / Specialist
- Reading list:    agentic_ai_context/*.md to load first
- Dependencies:    Other tasks that must finish first
```

Once a backlog exists in this shape, the assignment question becomes
mechanical: match tier hint → available model in that tier → cheapest
in that tier with capacity.

### 3.1 The optional "model poll" pattern

For ambiguous tasks where the tier isn't obvious, an emerging
pattern: prompt several LLMs with the task definition and ask them
to vote on which command-line LLM is best suited. Aggregate the
votes, assign to the winner. This is the LLM-orchestration
equivalent of leveling new hires in a software org.

The poll is itself a junior-tier task — don't ask Opus to figure
out whether Opus should do something. Ask Haiku, Gemini Flash, and
DeepSeek; their consensus is usually right and costs almost nothing.

---

## 4. The fleet, as of mid-2026

This is operational state, not a permanent recommendation — refresh
quarterly as model capabilities and pricing shift.

| Model                                | Tier        | Strongest for                                            | Notes |
|--------------------------------------|-------------|----------------------------------------------------------|-------|
| Claude Opus 4.x (1M context)         | Architect   | Whole-codebase reasoning, plans, hard debugging          | Default for cross-cutting work on this workspace. |
| Claude Sonnet 4.x                    | Senior      | Most implementation work after the plan is set           | Best price/quality for the bulk of day-to-day. |
| Claude Haiku 4.5                     | Junior      | Well-scoped scripts, lint, content fills                 | Fast and cheap; underused. |
| GPT-5 / o-series                     | Senior–Arch | Code review second opinion; long-context alternative     | Independent perspective from a non-Anthropic lineage. |
| Gemini 2.x Pro                       | Senior      | Multimodal tasks, OCR, image-heavy debugging             | Strong on visual artifacts. |
| Gemini Flash                         | Junior      | Cheap parallel polling, classification                   | Good for the model-poll pattern. |
| Grok 4                               | Senior      | Independent second opinion; less-aligned tone            | Useful when wanting outside-the-Anthropic-frame critique. |
| Kimi (Moonshot)                      | Senior      | Long-form prose; some published TrueSight blog posts     | Voice diverges from Claude — useful for editorial variety. |
| DeepSeek                             | Junior      | Cheap code generation in well-defined scope              | Cost outlier on the low end. |
| BigModel (智谱)                       | Junior      | China-region routing, alternate sovereignty             | Useful when API reachability is region-constrained. |
| GitHub Copilot                       | Specialist  | In-IDE line/block completion                             | Lives inside the editor, not the orchestration loop. |
| Cursor agents                        | Specialist  | In-IDE multi-file edits with the operator watching       | Specialist for paired-editing workflows. |
| Codex (sandbox)                      | Specialist  | Sandboxed code execution                                 | Good for safe `eval`-style tasks. |

### 4.1 Lineage diversity matters

When taking a major architectural decision, the second opinion
should come from a *different training lineage*. Claude reviewing
Claude is correlated. Claude reviewing Grok (xAI), or Claude
reviewing Gemini (Google), surfaces blind spots that same-lineage
review misses.

This is why TrueSight intentionally rotates LLM bylines on the blog
(`by Claude (Anthropic)`, `by Kimi (Moonshot AI)`, `by Grok (xAI)`)
— each model brings a slightly different prior, and the union is
more robust than any single one's output.

---

## 5. Anti-patterns

- **"Just throw it at Opus."** Most tasks don't need a 1M-context
  architect. Frontier-model latency under load can be 3–5× a
  junior model's. Reserve the architect tier for what only the
  architect tier can do.
- **Implementing without a written plan.** See §1.2.
- **Restart-in-new-model without a handoff prompt.** See §2.3.
- **Single-model dependency.** If one provider goes down or
  raises prices 5×, the workspace should keep moving. Test handoff
  paths quarterly; don't let any one model become load-bearing.
- **Letting a junior model own architectural decisions.** Cheap to
  ask, expensive to act on. Junior tiers vote; architect tier
  decides.

---

## 6. The historical pattern

The "scale up cheap, scale back down" instinct shows up repeatedly
in TrueSight's history:

- **2014 Singapore:** ~30 engineers/designers hired on freelancer.com
  in a month, scaled to zero three months later when work cleared.
- **2020s infrastructure:** GitHub Pages + GitHub Actions + Google
  Apps Script + Google Sheets as the backbone of a system that
  would otherwise cost several thousand USD/month in cloud bills
  plus a DevOps team.
- **2026 LLM fleet:** Multiple cheap models in junior roles, frontier
  models reserved for architect work, `agentic_ai_context` as the
  shared substrate so any of them can plug in.

The thread connecting all three: refuse to play the same game
everyone else is playing. The leverage is in the org design, not in
buying the biggest tool.

---

*Last refreshed 2026-05-12. Refresh §3 (model fleet) quarterly or
whenever pricing/capabilities meaningfully shift. The principles in
§§1–2 and the anti-patterns in §5 are durable across model
generations.*
