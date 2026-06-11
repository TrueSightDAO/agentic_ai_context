# Handoff Manifest — active execution handoffs

Machine-readable index of all active handoffs from a local LLM to **Sophia** (the autopilot).
Sophia updates this file when she starts, resumes, or completes a handoff.

**Protocol for all LLMs:**
1. Before acting on any handoff, `git pull` agentic_ai_context remote `main` to get the latest plans.
2. Check this manifest first to see what's active.
3. Cross-reference with `SOPHIA_HANDOFFS.md` for Telegram topic context.

---

| Plan file | Handoff title | Handoff date | Status | Resume tracker state | Last manifest update |
|-----------|---------------|--------------|--------|---------------------|---------------------|
| `SOPHIA_LIVE_PROGRESS_PLAN.md` | Live Progress Introspection (report what the executing turn is doing when Gary asks mid-turn, instead of a canned queued ack) | 2026-06-11 | blocked | Parked GO-ready in **thread 2799** ([topic](https://t.me/c/3919341801/2799)); on GO runs PR1 (`_live_progress` record + richer ack) → PR2 (progress-query answered immediately, lock-bypassing); **own-repo gate: opens PRs only, NEVER self-merges**; UAT U1–U5 = completion gate | 2026-06-11 |
| `SOPHIA_MULTI_TENANT_GOVERNANCE_PLAN.md` | Sophia Multi-Tenant Governance, Identity & Vault — **PHASE 0 only** (policy layer + tool-layer auth + data-vs-instruction boundary + guest-default) | 2026-06-11 | blocked | Parked GO-ready in **thread 2744** ([topic](https://t.me/c/3919341801/2744)); on GO runs **Phase 0 only** (RESUME HERE = PR0.1 `app/policy.py`), then STOPS for human merge + Phase 0 UAT (P0.1–P0.4) before Phase 1; **own-repo gate: opens PRs only, NEVER self-merges**; do NOT enter any collaborative group until Phase 0 ships | 2026-06-11 |
| `SOPHIA_FOLLOWUP_MONITOR_PLAN.md` | Durable Follow-up Monitor (thread-bound, multi-day; gmail_reply + elapsed_days; on strike spins a Sophia turn in the thread) | 2026-06-11 | in progress | Parked GO-ready in **thread 2622** ([topic](https://t.me/c/3919341801/2622)); Gary gave GO 2026-06-11; on GO runs PR1→PR4 (RESUME HERE = PR1 `app/followups.py`); **own-repo gate: opens PRs only, NEVER self-merges**; UAT U1–U9 is the completion gate | 2026-06-11 |
| `AUTOPILOT_HARDENING_PLAN.md` | Autopilot Hardening (Sophia's own codebase) | 2026-06-10 | blocked | Parked GO-ready in **thread 2317**; on GO runs Phase 1 PR-A→; **opens PRs only, never self-merges own-repo PRs** (human merges — Phase-2 gate dogfooded) | 2026-06-10 |
| `BETA_SANDBOX_ENDPOINT_PLAN.md` | Beta Sandbox Endpoint (beta.edgar.truesight.me) | 2026-06-09 | blocked | Parked GO-ready in **thread 1955**; on GO runs Unit 1→10, STOPS at operator gates (launch approval / prod deploy / Stripe dashboard); Unit 8 = mandatory AWS infra-doc update | 2026-06-09 |
| `CHOCOLATE_SUBSCRIPTION_PLAN.md` | Agroverse Chocolate Subscriptions — Phase 1 | 2026-06-09 | blocked | Parked GO-ready in **thread 1939** (supersedes 1924); on GO runs Phase 1 PR1.1–1.6 then STOPS at the operator test gate for Gary | 2026-06-09 |
| `RESEND_VERIFICATION_PLAN.md` | Resend verification email | 2026-06-08 | in progress | PR1 merged + deployed; PR2 (oracle) next | 2026-06-08 |
| `SANDBOX_THEOBROMA_1_HANDOFF_DEMO.md` | THEOBROMA-1 (cacao brew demo) | 2026-06-07 | demo · live | — | 2026-06-08 |

## Status values

| Status | Meaning |
|--------|---------|
| `in progress` | Sophia is actively working on this handoff |
| `blocked` | Sophia is waiting on a dependency (human action, PR review, etc.) |
| `demo · live` | Handoff is live/demo, no active execution needed |
| `completed` | All PRs merged, contribution reported, handoff closed |
| `stale` | No activity for 30+ days; may need re-assessment |

## How to update

When Sophia starts, resumes, or completes a handoff, she updates the relevant row's
**Status**, **Resume tracker state**, and **Last manifest update** columns and commits
this file to `main`.
