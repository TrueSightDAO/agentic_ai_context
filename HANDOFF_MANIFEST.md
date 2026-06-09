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
| `CHOCOLATE_SUBSCRIPTION_PLAN.md` | Agroverse Chocolate Subscriptions | 2026-06-09 | blocked | Parked at RESUME HERE (Phase 1 PR1.1); awaiting governor "go for it" | 2026-06-09 |
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
