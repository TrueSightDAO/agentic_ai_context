# Sentinel Role — Implementation Plan & Execution Roadmap

## Overview

Introduce a **Sentinel** role for AI agents (starting with the TrueSight DAO Autopilot) that grants governor-equivalent operational privileges (inventory moves, sales, QR updates, contributions) without governance authority (proposals, votes, permission changes).

The Sentinel flag lives on **Contributors contact information** column W (`Is Sentinel`). The `dao_members_cache_publisher.gs` reads it when building the `roles` array in `dao_members.json`. The GAS inventory movement handler (`process_movement_telegram_logs.js`) checks the signer's sentinel role dynamically instead of using a hardcoded trusted-agent list.

## Pre-flight Checklist

- [x] **Confirmed sheet location**: `Contributors contact information` tab, column W (`Is Sentinel`).
- [x] **Confirmed publisher reads `Governors` tab** to derive `roles` — same pattern used for Sentinel.
- [x] **Confirmed `dao_members.json` schema v3** already has `roles: ["governor", "member"]` — adding `"sentinel"` is additive.
- [x] **Confirmed `dao_protocol` `contributors.py`** returns the full contributor record including `roles` — no client change needed.
- [x] **Decision**: Sentinels get `["member", "sentinel"]` so existing member checks still pass.
- [x] **Autopilot key status** changed from `VERIFYING` → `ACTIVE` on row 119 of `Contributors Digital Signatures`.

## Sequenced Plan

### PR 1: Update `dao_members_cache_publisher.gs` to read Sentinel column

**Goal**: The publisher reads column W (`Is Sentinel`) from `Contributors contact information` and includes `"sentinel"` in the `roles` array when `TRUE`.

**Changes to** `tokenomics/google_app_scripts/tdg_identity_management/DaoMembersCache.js`:

1. Added constant for the sheet reference:
   ```js
   const DAO_MEMBERS_CACHE_CONTACT_SHEET = 'Contributors contact information';
   const DAO_MEMBERS_CACHE_SENTINEL_COL = 23; // Column W = index 22 (0-based)
   ```

2. Reads the `Contributors contact information` sheet to build a `sentinelByName` map (same pattern as `governorsByName`).

3. In the contributor assembly loop, after checking `governorsByName`, also checks `sentinelByName`:
   ```js
   if (sentinelByName[k]) roles.push('sentinel');
   ```

4. Updated the `counts` block to include a `sentinels` count.

**Status**: ✅ **Done** — PR #362 merged, deployed as GAS version @18, cache refreshed.

**Result**: `dao_members.json` now has 4 sentinels:
- Sophia Truesight (`roles: ["member", "sentinel"]`)
- truesight-autopilot (`roles: ["member", "sentinel"]`)
- Claude Anthropic (`roles: ["member", "sentinel"]`)
- Kimi Moon (`roles: ["member", "sentinel"]`)

---

### PR 2: Replace hardcoded TRUSTED_AGENTS with dynamic sentinel role check in `process_movement_telegram_logs.js`

**Goal**: The GAS inventory movement handler currently has a hardcoded `TRUSTED_AGENTS = ['autopilot@agroverse.shop']` list. Replace this with a dynamic check: if the signer has `Is Sentinel = TRUE` in `Contributors contact information` AND the submission includes `- Approved By:` a governor, authorize the movement.

**Changes to** `tokenomics/google_app_scripts/tdg_identity_management/process_movement_telegram_logs.js`:

1. Remove the `TRUSTED_AGENTS` constant and `isTrustedAgent_()` function.
2. Add a new function `isSentinelByName_(contributorName)` that reads `Contributors contact information` Column W and returns TRUE if the contributor has `Is Sentinel = TRUE`.
3. In `inventoryMovementStatusFromTelegramRow_`, replace:
   ```javascript
   // OLD: hardcoded trusted agent check
   if (isTrustedAgent_(res.contributorName)) {
     const approvedBy = extractApprovedBy_(contribution);
     if (approvedBy && isGovernorApproved_(approvedBy)) return 'NEW';
   }
   ```
   With:
   ```javascript
   // NEW: dynamic sentinel role check
   if (isSentinelByName_(res.contributorName)) {
     const approvedBy = extractApprovedBy_(contribution);
     if (approvedBy && isGovernorApproved_(approvedBy)) return 'NEW';
   }
   ```

**Status**: ⏳ **On hold** — DeepSeek is working on a change to this file. Awaiting completion before proceeding.

---

### PR 3: Re-process the 30 stuck inventory movements

**Goal**: The 30 June 18 submissions are sitting in the Inventory Movement sheet with STATUS = "unauthorized". After PR 2 deploys, re-run the GAS handler or manually flip their STATUS to "NEW" so the second handler picks them up.

**Status**: ⏳ Blocked on PR 2.

---

### PR 4: (Optional) Update `governors.rb` to use cache roles

**Goal**: Remove the hardcoded `TRUSTED_AGENTS` list from `sentiment_importer`'s `governors.rb` and instead check the `dao_members.json` roles field.

**Deferred**: The Rails app's Telegram Chat Logs column S stamp still works fine with the hardcoded list. Only do this if the hardcoded list becomes a maintenance burden.

**Status**: ☐ Deferred

---

### PR 5: (Optional) Add Sentinel-aware event gating in `dao_protocol`

**Goal**: The Python `EdgarClient` could optionally check the signer's roles before submitting certain event types (e.g., reject `[PROPOSAL CREATION]` if roles don't include `"governor"`).

**Deferred**: Edgar already handles this server-side. Client-side gating is a nice-to-have for faster feedback.

**Status**: ☐ Deferred

---

## Resume Tracker

| Step | PR | Status |
|------|-----|--------|
| Update `dao_members_cache_publisher.gs` | tokenomics PR #362 | ✅ Done |
| Replace hardcoded TRUSTED_AGENTS with sentinel role check | tokenomics PR (TBD) | ⏳ On hold (DeepSeek working on file) |
| Re-process 30 stuck inventory movements | Manual / re-trigger | ⏳ Blocked on PR 2 |
| Remove TRUSTED_AGENTS from `governors.rb` | sentiment_importer PR (deferred) | ☐ |
| Client-side event gating in `dao_protocol` | dao_protocol PR (deferred) | ☐ |

**RESUME HERE** → **PR 2: Replace hardcoded TRUSTED_AGENTS with dynamic sentinel role check in `process_movement_telegram_logs.js`** (waiting for DeepSeek to finish their change first).

## Notes

- The `Contributors contact information` sheet has header row 4. Column W (index 22, 0-based) = `Is Sentinel`.
- The autopilot's RSA key (row 119 of `Contributors Digital Signatures`) was changed from `VERIFYING` → `ACTIVE` by Gary on 2026-06-18.
- The `dao_members_cache_publisher.gs` was deployed as GAS version @18 on 2026-06-18.
- 4 sentinels are now in `dao_members.json`: Sophia Truesight, truesight-autopilot, Claude Anthropic, Kimi Moon.
