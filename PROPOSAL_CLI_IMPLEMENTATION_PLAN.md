# Proposal CLI Implementation Plan

**Date:** 2026-06-16
**Thread:** 3966
**Status:** Ready for execution

## Goal

Extend `dao_client` (Python/FastAPI, repo `dao_protocol`) so that **Sophia** (the autopilot) can create and vote on proposals directly via CLI — without needing the DApp browser form. The server-side (`dao_protocol`) already routes `[PROPOSAL CREATION]` and `[PROPOSAL VOTE]` events to the GAS webhook (`process_dapp_payloads`). Only the CLI stubs need to be filled in.

## Current State

- `truesight_dao_client/modules/create_proposal.py` — exists but has **empty `canonical_labels=[]`** — no structured fields
- `truesight_dao_client/modules/review_proposal.py` — exists but has **empty `canonical_labels=[]`** — no structured fields
- `pyproject.toml` — both console scripts already registered (`truesight-dao-create-proposal`, `truesight-dao-review-proposal`)
- `truesight_dao_client/server/dispatch.py` — already routes `[PROPOSAL CREATION]` and `[PROPOSAL VOTE]` to `process_dapp_payloads` webhook
- **No server-side changes needed** — the dispatch table already handles both event types

## Changes Required

### 1. `modules/create_proposal.py` — Add canonical labels and CLI flags

| Flag | Required | Description |
|------|----------|-------------|
| `--type` | Yes | Proposal type: `standard`, `vendor`, `governance`, `budget` |
| `--title` | Yes | Short proposal title (max 120 chars) |
| `--content` | Yes* | Full proposal body |
| `--body-file` | No* | Path to file containing proposal body (alternative to `--content`) |
| `--performance-metrics` | No | URL or reference to performance data (for vendor proposals) |

\* Exactly one of `--content` or `--body-file` is required.

**Canonical labels:** `['Type', 'Title', 'Content', 'Performance Metrics']`

### 2. `modules/review_proposal.py` — Add canonical labels and CLI flags

| Flag | Required | Description |
|------|----------|-------------|
| `--proposal-id` | Yes | PR number or proposal identifier |
| `--vote` | Yes | `approve`, `reject`, or `abstain` |
| `--comment` | No | Optional rationale for the vote |

**Canonical labels:** `['Proposal ID', 'Vote', 'Comment']`

### 3. `pyproject.toml` — No change needed

Both console scripts are already registered.

## Execution Roadmap

| Step | File | Change | Effort |
|------|------|--------|--------|
| 1 | `modules/create_proposal.py` | Add canonical labels, `--type`, `--title`, `--content`, `--body-file`, `--performance-metrics` | ~40 lines |
| 2 | `modules/review_proposal.py` | Add canonical labels, `--proposal-id`, `--vote`, `--comment` | ~25 lines |
| 3 | Test | Run `truesight-dao-create-proposal --dry-run` to verify payload format | 5 min |
| 4 | Deploy | `pip install -e .` to update the installed package | 1 min |

## Checklist

- [ ] Step 1: Add canonical labels to `create_proposal.py`
- [ ] Step 1: Add `--type` flag (choices: standard, vendor, governance, budget)
- [ ] Step 1: Add `--title` flag (required)
- [ ] Step 1: Add `--content` flag (required unless `--body-file` provided)
- [ ] Step 1: Add `--body-file` flag (alternative to `--content`)
- [ ] Step 1: Add `--performance-metrics` flag (optional)
- [ ] Step 2: Add canonical labels to `review_proposal.py`
- [ ] Step 2: Add `--proposal-id` flag (required)
- [ ] Step 2: Add `--vote` flag (choices: approve, reject, abstain)
- [ ] Step 2: Add `--comment` flag (optional)
- [ ] Step 3: Dry-run test
- [ ] Step 4: Deploy

## How Sophia Will Use It

Once implemented, Sophia can create proposals directly:

```bash
truesight-dao-create-proposal \
    --type governance \
    --title "Establish Legal Holding Entity for Brazil Export Operations" \
    --body-file /tmp/proposal_body.md
```

And vote on them:

```bash
truesight-dao-review-proposal \
    --proposal-id 617 \
    --vote approve \
    --comment "Both paths well-researched, defer to counsel"
```

## Related Documents

- `LEGAL_ENTITY_STRUCTURING_PROPOSAL.md` — V1 lean SVH doc
- `LEGAL_ENTITY_STRUCTURING_PROPOSAL_v2.md` — V2 full capital channels
- `BRAZIL_EXPORT_ENTITY_BRIEF.md` — Brazil export entity brief (updated with Prospera + UNA paths)
