# Feature Implementation Convention

> **Standard format for all feature implementation documents across TrueSight DAO's digital infrastructure.**
> This convention applies to every project: autopilot, tokenomics, dapp, market_research, go_to_market, dao_client, and all others.

---

## 1. Why This Convention

### Problem

Feature implementations across the DAO have been documented inconsistently. Some documents start with technical details, others with context, others with a checklist. This makes it hard for:
- **Governors** to quickly understand *why* a feature exists
- **Developers** to understand *how* to implement it
- **AI agents** to parse and act on the plan
- **Future maintainers** to understand design decisions

### Vision

Every feature implementation in the DAO follows a single, predictable structure:

1. **Why** — the problem, vision, and success criteria
2. **How** — the implementation details, architecture, and design decisions
3. **When** — the execution roadmap with concrete checkpoints

This consistency reduces onboarding time, eliminates ambiguity, and makes every document machine-readable by AI agents.

### Success Criteria

- Any governor can open any implementation document and find the "Why" in the first section
- Any developer can open any implementation document and find the technical details in the second section
- Any AI agent can parse any implementation document and extract actionable tasks from the third section
- Every `.md` has a corresponding `.pdf` in Saffron Monk style

---

## 2. Implementation Details

### 2.1 Document Structure

Every feature implementation document MUST have exactly three sections, in this order:

```
# [TITLE]

> [One-line summary / tagline]

---

## 1. Why

### Problem Statement
[What problem does this feature solve? What pain point exists today?]

### Vision
[What does success look like? How does this serve the DAO's mission?]

### Success Criteria
[Measurable outcomes — how will we know this is done?]

---

## 2. Implementation Details

### Architecture / Design
[How does this work? Key components, data flow, integrations.]

### Key Decisions
[Design choices and why they were made. What alternatives were considered?]

### Risks & Mitigations
[What could go wrong and how will we handle it?]

### Dependencies
[What needs to exist before this can be built?]

---

## 3. Execution Roadmap

### Phase 1: [Name]
- [ ] Task 1 — [owner]
- [ ] Task 2 — [owner]
- [ ] **Checkpoint:** [what success looks like at end of this phase]

### Phase 2: [Name]
- [ ] Task 1 — [owner]
- [ ] **Checkpoint:** [what success looks like at end of this phase]

### Phase N: [Name]
- [ ] Task 1 — [owner]
- [ ] **Checkpoint:** [what success looks like at end of this phase]
```

### 2.2 Section Rules

#### Section 1: Why
- **Must** be the first content section after the title and tagline
- **Must** include a problem statement grounded in current reality
- **Must** include a vision that ties back to the DAO's mission (10,000 hectares of Amazon rainforest)
- **Must** include concrete, measurable success criteria
- **Should** reference existing context files where relevant

#### Section 2: Implementation Details
- **Must** describe the architecture or design at a level appropriate to the audience
- **Must** document key design decisions and alternatives considered
- **Must** identify risks and mitigations
- **Must** list dependencies (people, systems, credentials, data)
- **Should** include diagrams or data flow descriptions where helpful
- **Should** reference relevant runbooks, API docs, or schema files

#### Section 3: Execution Roadmap
- **Must** be a checklist with `- [ ]` items
- **Must** be organized into phases
- **Must** have a checkpoint at the end of each phase (what "done" looks like)
- **Should** assign owners to tasks where known
- **Should** include estimated effort or time where possible
- **May** include links to related PRs, issues, or documents

### 2.3 File Naming

- Use `SCREAMING_SNAKE_CASE.md` for implementation documents
- The `.pdf` version uses the same base name: `IMPLEMENTATION_PLAN.md` → `IMPLEMENTATION_PLAN.pdf`
- Store in the relevant project's docs/ directory or the project root
- Cross-project features go in `agentic_ai_context/`

### 2.4 PDF Generation

Every `.md` implementation document MUST have a corresponding `.pdf` generated using the **Saffron Monk** style (see `PDF_STYLE_CONVENTION.md`).

**Workflow:**
1. Write the `.md` file
2. Generate the `.pdf` using the `generate_pdf` tool
3. Commit both files in the same PR

---

## 3. Execution Roadmap

### Phase 1: Establish Convention (this PR)
- [x] Create `FEATURE_IMPLEMENTATION_CONVENTION.md`
- [x] Create `PDF_STYLE_CONVENTION.md` (extracted from `generate_pdf` tool)
- [x] Generate `.pdf` versions of both documents
- [ ] **Checkpoint:** Both documents merged to `agentic_ai_context` main branch

### Phase 2: Retroactive Compliance
- [ ] Audit existing implementation documents across all repos for compliance
- [ ] Update top-priority documents to match the new convention
- [ ] **Checkpoint:** All active implementation documents follow the convention

### Phase 3: Enforcement
- [ ] Add a PR checklist item: "Does this feature have an implementation document following FEATURE_IMPLEMENTATION_CONVENTION.md?"
- [ ] Add a GitHub Action or autopilot check that validates new implementation documents
- [ ] **Checkpoint:** Convention is automatically enforced

---

*Last updated: 2026-06-07*