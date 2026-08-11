# Sentinel Role in dao_members.json + GAS Auth

## Context

- `dao_members_cache_publisher.gs` reads 3 sheets (Contributors Digital Signatures, Contributors voting weight, Governors) but **not** `Contributors Contact Information` Column W ("Is Sentinel")
- The members page (`truesight.me/members.html`) has a Sentinels section that filters `dao_members.json` for `roles: ['sentinel']` — currently hidden because nobody has that role
- The GAS inventory movement auth (`process_movement_telegram_logs.js`) has a **hardcoded** trusted-agent path (`TRUSTED_AGENTS = ['autopilot@agroverse.shop']`) — brittle and doesn't match Sophia's actual contributor name ("Sophia Truesight")
- The autopilot's RSA key is now ACTIVE in Contributors Digital Signatures (row 119)
- 30 inventory movement submissions from June 18 are stuck with STATUS = "unauthorized" in the Inventory Movement sheet

## Tasks

### Task 1 — Add sentinel role to `dao_members_cache_publisher.gs`

**File:** `tokenomics/google_app_scripts/tdg_identity_management/dao_members_cache_publisher.gs`

- Add `Contributors Contact Information` to the list of sheets read
- Read columns A (name) and W (Is Sentinel)
- Build a `sentinelsByName` lookup
- In the roles assembly (currently adds `'member'` and optionally `'governor'`), add `'sentinel'` for matching names
- This makes the Sentinels section on `members.html` light up AND provides the data source for the GAS auth check

### Task 2 — Replace hardcoded trusted-agent with dynamic sentinel role check

**File:** `tokenomics/google_app_scripts/tdg_inventory_management/process_movement_telegram_logs.js`

- Remove the `TRUSTED_AGENTS` constant and `isTrustedAgent_()` function
- Add a new function `isSentinelByName_(contributorName)` that reads `Contributors Contact Information` Column W and returns TRUE if the contributor has `Is Sentinel = TRUE`
- In `inventoryMovementStatusFromTelegramRow_`, replace the hardcoded trusted-agent check with a dynamic sentinel role check:

```javascript
// OLD: hardcoded trusted agent check
if (isTrustedAgent_(res.contributorName)) {
  const approvedBy = extractApprovedBy_(contribution);
  if (approvedBy && isGovernorApproved_(approvedBy)) return 'NEW';
}

// NEW: dynamic sentinel role check
if (isSentinelByName_(res.contributorName)) {
  const approvedBy = extractApprovedBy_(contribution);
  if (approvedBy && isGovernorApproved_(approvedBy)) return 'NEW';
}
```

### Task 3 — Trigger a fresh `dao_members.json` publish

- After Task 1 deploys, trigger the cache refresh (Edgar webhook or manual)
- Verify Sentinels section appears on `truesight.me/members.html`

### Task 4 — Re-process the 30 stuck inventory movements

- The 30 June 18 submissions are in the Inventory Movement sheet with STATUS = "unauthorized"
- After Task 2 deploys, either:
  - (a) Re-run the GAS handler against those rows, OR
  - (b) Manually flip their STATUS to "NEW" so the second handler picks them up

### Task 5 — Document in OPEN_FOLLOWUPS.md

- File a follow-up entry documenting the fix for cross-session recall

## Execution Roadmap

| Step | What | Repo | PR | Gate |
|------|------|------|----|------|
| 1 | Add Contributors Contact Information read + sentinel role to `dao_members_cache_publisher.gs` | `tokenomics` | PR1 | Merge + deploy |
| 2 | Trigger cache refresh → verify Sentinels section appears on truesight.me/members.html | — | — | Gary confirms |
| 3 | Replace hardcoded TRUSTED_AGENTS with dynamic sentinel role check in `process_movement_telegram_logs.js` | `tokenomics` | PR2 | Merge + deploy |
| 4 | Re-process the 30 stuck rows (flip STATUS or re-trigger handler) | — | — | Gary confirms |
| 5 | File follow-up in OPEN_FOLLOWUPS.md | `agentic_ai_context` | PR3 | Merge |

## RESUME HERE

On **"go for it"**, execute **Step 1** (PR1 for `dao_members_cache_publisher.gs`), then stop and report.
