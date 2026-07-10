# Butterfly Effect cohort onboarding — execution plan

**Status:** Plan-of-record · drafted 2026-05-18
**Partner:** ERA Professionals — Butterfly Effect program (lead: Bilal)
**Platform:** TrueSight DAO credentialing — `truesight.me/programs/butterfly-effect/`

---

## 1. Context (why this doc exists today)

Earlier today, Bilal introduced the rest of his ERA team and discussions opened on onboarding **not just the current cohort** but **all of ERA's existing students** (current + historical alumni) into the TrueSight DAO credentialing platform.

This is the moment the platform's *proof surface* stops being over-served. Two months of credentialing-platform infrastructure had a single live demo participant; over the next 1–2 weeks it will have its first real consumer at material scale. This doc records what we agreed to build, defer, and decide so the team can move at ERA's natural pace without waiting on us.

## 2. What we are building this week

### 2.1 Cohort batch-import CLI

**Where:** `dao_client/modules/onboard_program_cohort.py` (new module — pattern mirrors the existing `onboard_retail_partner.py` from the Way Home Shop work).

**What it does:** Takes a manifest (program slug + roster CSV) supplied by ERA's team. For each row, mints a participant identifier under `lineage-credentials/programs/butterfly-effect/<id>/`, populates `identity.json` and a `practice/` completion event, triggers the rebuild workflow. `--dry-run` default; `--execute` to apply. Idempotent so re-runs are safe.

**Why first:** unblocks ERA's team from manually editing JSON files in a Git repo. Without it, every new student is a bottleneck on us.

### 2.2 `public_listable` consent flag

**Where:** new field on `lineage-credentials/programs/butterfly-effect/<id>/identity.json`. Default is operator-controlled per cohort; ERA decides what makes sense for their consent posture.

**What it does:** When `false`, the participant is hidden from the cohort listing on `truesight.me/programs/butterfly-effect/members.html` — but their per-participant credential URL still resolves. So a printed certificate's QR code always works, even for participants who opt not to appear in the public roster.

**Why now:** the deferred Phase 5 of `CREDENTIALING_PROGRAM_PAGES.md` becomes immediately relevant the moment minors enter the system. ERA needs the option per student.

### 2.3 Certificate template year-as-variable

**Where:** `lineage-engine/scripts/program_assets/butterfly-effect/cert_config.json` — add a new overlay field `program_year`, wire it into `cert_overlay.py`.

**What it does:** The current template hard-codes "Butterfly Effect Club Program 2025–2026" in the design. For historical cohorts (2023, 2024) we need year-as-data. Adding it as an overlay field lets one template serve every cohort year.

**Why now:** ERA's historical alumni include cohorts from earlier years. Without this, every year-cohort needs its own template file — multiplying the asset surface for no design reason.

## 3. What we are writing this week (operator-facing doc, not code)

### 3.1 `PROGRAM_OPERATOR_HANDOFF.md`

**Where:** `agentic_ai_context/PROGRAM_OPERATOR_HANDOFF.md` — generalized so the next partner organization can inherit it.

**What it contains:**
- What's automated end-to-end (cron rebuild, QR generation, PDF generation, deduplication)
- What the partner operator does manually (roster preparation, consent decisions, certificate sign-off)
- Where the partner sends issues, questions, or scope changes
- What to expect during the first batch onboarding (timing, friction points, who reviews)

**Why now:** ERA's team showing up is the first real test of whether the platform can be operated by an organization that doesn't share our context. A doc handed to their team is more valuable than any additional automation we could ship.

## 4. What we are deferring (and why)

### 4.1 Autopilot ↔ credentialing integration

The principle is decided: **yes**, the autopilot service should eventually be aware of credentialing events. But the first concrete step is read-access — autopilot tools (`query_credential_state(slug)`, `list_program_cohort(program)`) exposed in `truesight_autopilot/app/llm_client.py::get_tool_schemas()` so governor chat can answer "how many Butterfly Effect students completed in 2024?" with real data.

Read-access becomes useful only once there's a real cohort to query. Event-subscription (autopilot fires actions on credential changes) waits until read-access has surfaced a real pattern worth automating. Bidirectional write-access is not in scope.

**Defer until:** first 10–20 real students are imported and live on the platform.

### 4.2 Phase 4.2 / 4.3 of the credential page freshness work

Both useful, neither bottleneck right now. Wait for real cohort use to surface actual friction; patch then. Premature optimization of features that may not match the partner's real workflow.

### 4.3 Additional partner programs

Tribo Bahia Mirim + Butterfly Effect already cover two tenants without real cohorts; adding a third would compound the over-served-platform problem. Onboarding a second partner organization should wait until Butterfly Effect has real students moving through.

## 5. What ERA's team needs to decide

These are open questions only ERA can answer. They block parts of Section 2's work.

| # | Question | Blocks |
|---|---|---|
| 5.1 | **Per-student consent model** — who decides `public_listable` for each student? What's the default — opt-in or opt-out? How is consent captured before the operator records it? | §2.2 going live |
| 5.2 | **Past cohorts** — which years are in scope (2023? 2022? earlier)? Approximate student count per year? Are there students whose contact info or photos shouldn't surface even with `public_listable: true`? | Scope of §2.1 first run |
| 5.3 | **First batch size** — we strongly recommend starting with a small batch (~5–10 students) before bulk-importing the full history. Catches edge cases before they multiply. | §2.1 execution |
| 5.4 | **Photos** — does ERA hold photo consent for participants? If yes, photos can appear on credential pages; if no, text-only profiles. | Future credential page enhancement |
| 5.5 | **Certificate review** — who at ERA signs off on each batch of certificate PDFs before they're handed to participants? | Operational workflow handoff |

## 6. Sequencing principle

```
Cohort onboarding CLI (§2.1)
        ↓
ERA imports first batch (5-10 students)
        ↓
We observe friction → patch → expand batch size
        ↓
Once 10-20 real students are live: autopilot read-access integration
        ↓
Once autopilot has surfaced a real signal pattern: decide on event-subscription
```

The principle: each step generates the data the next step needs. Don't build N+1 before step N has produced real evidence of what's needed.

## 7. References

- Phase 0 spec — overall architecture: [`CREDENTIALING_PROGRAM_PAGES.md`](./CREDENTIALING_PROGRAM_PAGES.md)
- Phase 4.1 freshness layer (shipped 2026-05-18) — §18 of the spec doc above
- Platform pages: [`truesight.me/programs/butterfly-effect/`](https://truesight.me/programs/butterfly-effect/)
- Sample participant data shape: [`TrueSightDAO/lineage-credentials/programs/butterfly-effect/`](https://github.com/TrueSightDAO/lineage-credentials/tree/main/programs/butterfly-effect)
- Retail-partner onboarding CLI (pattern for §2.1): [`TrueSightDAO/dao_client/modules/onboard_retail_partner.py`](https://github.com/TrueSightDAO/dao_client/blob/main/truesight_dao_client/modules/onboard_retail_partner.py)

---

*This document is the plan-of-record for the ERA Professionals / Butterfly Effect cohort onboarding effort. Updates should be appended as decisions evolve; the structure (build / write / defer / decide / sequencing) is the canonical shape future partner onboardings should follow.*
