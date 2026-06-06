# Sentinel Role — Implementation Plan & Execution Roadmap

## Overview

Introduce a **Sentinel** role for AI agents (starting with the TrueSight DAO Autopilot) that grants governor-equivalent operational privileges (inventory moves, sales, QR updates, contributions) without governance authority (proposals, votes, permission changes).

The Sentinel flag lives on **Contributors contact information** as a new column. The `dao_members_cache_publisher.gs` reads it when building the `roles` array in `dao_members.json`. The `dao_protocol` Python client already returns `roles` — no client-side change needed for lookups.

## Pre-flight Checklist

- [x] **Confirmed sheet location**: `Contributors contact information` tab, column W (`Is Sentinel`). Columns A–V are: Name, Wallet, ETH Wallet, Email, Address, Phone, Discord, Telegram, Twitter, Projects, LinkedIn, Facebook, Github, Instagram, Website, Tax ID, WhatsApp Chat Log ID, Digital Signature, TikTok, Is Store Manager, Mailing Address, Venmo.
- [x] **Confirmed publisher reads `Governors` tab** to derive `roles` — same pattern will be used for Sentinel.
- [x] **Confirmed `dao_members.json` schema v3** already has `roles: ["governor", "member"]` — adding `"sentinel"` is additive.
- [x] **Confirmed `dao_protocol` `contributors.py`** returns the full contributor record including `roles` — no client change needed.
- [ ] **Decision**: Should Sentinels also get `"member"` in their roles array? (Proposal: yes — `["sentinel", "member"]` so existing member checks still pass.)
- [ ] **Decision**: Should the `sentiment_importer`'s `TRUSTED_AGENTS` hardcoded list in `governors.rb` be removed in favor of the cache? (Proposal: defer to a follow-up PR — the Rails app still needs the Telegram Chat Logs column S stamp, which reads the Governors tab directly, not the cache.)

## Sequenced Plan

### PR 1: Add `Is Sentinel` column to Contributors contact information sheet

**Goal**: Add column W with header `Is Sentinel` and populate `TRUE` for the autopilot identity (`admin@truesight.me` / `truesight-autopilot`).

**Changes**:
- Add header `Is Sentinel` to cell W4 on `Contributors contact information`
- Set W4 value to `TRUE` for the row matching `truesight-autopilot` (or `admin@truesight.me`)

**Manual step**: Requires editing the Google Sheet directly (no code change).

**Status**: ☐ Not started

---

### PR 2: Update `dao_members_cache_publisher.gs` to read Sentinel column

**Goal**: The publisher reads column W (`Is Sentinel`) from `Contributors contact information` and includes `"sentinel"` in the `roles` array when `TRUE`.

**Changes to** `tokenomics/google_app_scripts/tdg_identity_management/dao_members_cache_publisher.gs`:

1. Add constant for the sheet reference:
   ```js
   const DAO_MEMBERS_CACHE_CONTACT_SHEET = 'Contributors contact information';
   const DAO_MEMBERS_CACHE_SENTINEL_COL = 23; // Column W = index 22 (0-based)
   ```

2. Read the `Contributors contact information` sheet to build a `sentinelByName` map (similar to `governorsByName`):
   - Header row is 4, data starts at row 5
   - Column A = Name, Column W = Is Sentinel
   - Normalize names to lowercase for matching

3. In the contributor assembly loop, after checking `governorsByName`, also check `sentinelByName`:
   ```js
   if (sentinelByName[k]) roles.push('sentinel');
   ```
   This produces `roles: ["governor", "member", "sentinel"]` or `roles: ["member", "sentinel"]`.

4. Update the `counts` block to include a `sentinels` count.

**Testing**:
- Run `publishDaoMembersCacheNow()` from the Apps Script editor
- Verify `dao_members.json` on `treasury-cache` main branch shows `"roles": ["member", "sentinel"]` for `truesight-autopilot`
- Verify the autopilot's `for_self()` lookup returns the updated roles

**Status**: ☐ Not started

---

### PR 3: (Optional) Update `governors.rb` to use cache roles

**Goal**: Remove the hardcoded `TRUSTED_AGENTS` list from `sentiment_importer`'s `governors.rb` and instead check the `dao_members.json` roles field.

**Deferred**: This is a separate concern — the Rails app's Telegram Chat Logs column S stamp still works fine with the hardcoded list. Only do this if the hardcoded list becomes a maintenance burden.

**Status**: ☐ Deferred

---

### PR 4: (Optional) Add Sentinel-aware event gating in `dao_protocol`

**Goal**: The Python `EdgarClient` could optionally check the signer's roles before submitting certain event types (e.g., reject `[PROPOSAL CREATION]` if roles don't include `"governor"`).

**Deferred**: Edgar already handles this server-side. Client-side gating is a nice-to-have for faster feedback.

**Status**: ☐ Deferred

---

## Resume Tracker

| Step | PR | Status |
|------|-----|--------|
| Add `Is Sentinel` column to sheet | Manual sheet edit | ☐ |
| Update `dao_members_cache_publisher.gs` | tokenomics PR | ☐ |
| Remove `TRUSTED_AGENTS` from `governors.rb` | sentiment_importer PR (deferred) | ☐ |
| Client-side event gating in `dao_protocol` | dao_protocol PR (deferred) | ☐ |

**RESUME HERE** → **Step 1: Add the `Is Sentinel` column to the Google Sheet.**

## Notes

- The `Contributors contact information` sheet has header row 4. Column W (index 22, 0-based) is currently empty/unused. We'll use it for `Is Sentinel`.
- The `dao_members_cache_publisher.gs` reads `Contributors Digital Signatures` (header row 1) and `Contributors voting weight` (header row 4) and `Governors` (data starts row 11). Adding a read from `Contributors contact information` (header row 4, data row 5+) follows the same pattern.
- The `truesight-autopilot` contributor name in `Contributors Digital Signatures` is `truesight-autopilot` and the email is `admin@truesight.me`. The corresponding row in `Contributors contact information` needs to have `truesight-autopilot` in column A for the name join to work.
