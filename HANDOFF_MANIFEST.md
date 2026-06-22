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
| `SCORING_REVIEW_QUEUE_PLAN.md` | Scoring Review Queue (cache generator, Edgar endpoint, DApp review UI) | 2026-06-18 | in progress | **2026-06-22: PR4 DEPLOYED.** Handler merged (tokenomics #367); duplicate-`doGet` deploy-blocker fixed (#368); then `clasp push`ed 1BHAGZd with the gary account (also repaired a drifted @HEAD: removed orphan Code.js, restored Credentials.js, single doGet). Created **anonymous versioned deployment @2** `AKfycbzati5N6aT1slb5C8SAIfs11avrAg_8Wf_ecXXMmoUp0K6I3-TnDwIlv1Cth4IHOQMq` — `?exec=processApprovalRejections` **verified live** → `{"status":"ok","processed":0,"skipped":0}` (Telegram @1 deployment untouched). **PR4-WIRE DONE:** Edgar `DAO_PROTOCOL_GAS_REVIEW_WEBHOOK_URL` = @2 /exec URL set on `dao_protocol_nelanco` + service restarted (var confirmed in process env, /ping 200) — **automated write-back path now live end-to-end.** Optional backup: `installReviewProcessingTrigger()` in the GAS editor. **RESUME HERE = PR7** (human-run real E2E UAT on beta); then **PR8** promote. Webhook URL + steps in plan §12. | 2026-06-22 |
| `SOPHIA_DAPP_EVENT_ALIGNMENT_PLAN.md` | Sophia↔DApp Event Alignment (all event types) | 2026-06-18 | parked GO-ready | Parked GO-ready in **thread 6416** ([topic](https://t.me/c/3919341801/6416)). **ONE PR PER TURN (§5a):** on GO run **PR1 ONLY then STOP** (catalog merge UPDATE — `_refresh_events_catalog` updates required_fields + canonical_labels for events already in the dicts, not just adds new). Then PR2 load-timing → PR3 fallback snapshot → PR4 normalizer (flagged) → PR5 stop-dropping-keys (needs PR4) → PR6 intent→event picking (review gate) → PR7 enforce-lookup (needs PR6) → PR8 UAT. `truesight_autopilot` own-repo gate — opens PRs only, NEVER self-merges; RESUME HERE = PR1. Catalog already complete (30 events) — consumption-correctness effort. | 2026-06-18 |
| `CLI_SALES_EVENT_ALIGNMENT_PLAN.md` | CLI Sales Event Audit & Alignment with DApp | 2026-06-17 | in progress | Parked GO-ready in **thread 6311** ([topic](https://t.me/c/3919341801/6311)); on GO runs PR1 (update CLI report_sales module in dao_client) → PR2 (update Edgar docs) → PR3 (re-submit Gergana's sale); **dao_client repo gate** — opens PRs only, NEVER self-merges; RESUME HERE = PR1 | 2026-06-17 |
| `PUBLIC_KEY_LOOKUP_CACHE_PLAN.md` | Public-Key Lookup Cache (content-addressed per-key governor store; retires the 5-min vault cache-lag bug) | 2026-06-16 | blocked | Parked GO-ready in **thread 5712** ([topic](https://t.me/c/3919341801/5712)). **ONE PR PER TURN (§5a):** on GO run **PR1 ONLY then STOP** (GAS generator emits `treasury-cache/public_keys/<sha256>.json`); next turn resumes PR2 (incremental + revocation); then PR3 (`governor_registry.resolve_key`). Do NOT chain PRs in one turn — that choked Sophia 2026-06-16 (round-cap → empty response; see `CONTEXT_UPDATES.md`). **HOLD PR4 (`vault_routes.py`) until in-flight `track_registry` work merges** (collision); `truesight_autopilot` own-repo gate — opens PRs only, NEVER self-merges; RESUME HERE = PR1; UAT U1–U5 on beta = completion gate | 2026-06-16 |
| `SOPHIA_VAULT_CREDENTIAL_MIGRATION_PLAN.md` | Vault Initialization & Credential Migration (migrate /home/ubuntu/ bare credentials into encrypted vault) | 2026-06-14 | blocked | Parked GO-ready in **thread 3981** ([topic](https://t.me/c/3919341801/3981)); on GO runs Units 1-6: init vault, add 7 credentials, update tools, UAT (U1-U7), docs, cleanup; **own-repo gate**; RESUME HERE = Unit 1 | 2026-06-14 |
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
