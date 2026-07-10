# Review Queue — Standard Operating Procedure

**Audience:** Sophia Truesight, LLM agents, Governors  
**Purpose:** Automatable rules for reviewing and resolving scored chatlogs in the review queue.  
**Goal:** Reduce human governor time to near-zero.  
**Status:** Draft · **Last updated:** 2026-06-28

---

## 1. Data Sources

| Source | URL | Purpose |
|--------|-----|---------|
| Review Queue (Edgar) | `GET https://edgar.truesight.me/dao/review_queue?limit=N` | Pending scored chatlogs |
| DAO Members Registry (primary) | `https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/dao_members.json` | **PRIMARY**: All known DAO members from the Contact sheet — canonical name for matching |
| Full TDG Holder List (supplement) | `https://raw.githubusercontent.com/TrueSightDAO/lineage-credentials/main/_cache/index.json` | SUPPLEMENT: All 469 TDG holders via `members[].display_name` — use if name not in dao_members |
| Scored Chatlogs Sheet | Google Sheets `1Tbj7H5ur_egQLRugdXUaSIhEYIKp0vvVv2IZ7WTLCUo` | Raw scoring data (for deep-dive only) |

**Matching order:** Try `dao_members.json` `name` first (exact, includes all Contact sheet entries). If not found, try `lineage-credentials` `display_name` (exact, 469 holders). If still not found → Skip.

**Important:** `Sophia` (human holder, 1250 TDG, lineage-credentials) ≠ `Sophia Truesight` (AI agent, dao_members.json). `Claude` (human, 3.33 TDG, lineage-credentials) ≠ `Claude Anthropic` (AI agent, dao_members.json). Each list is independently authoritative — do not cross-map between them.

---

## 2. Queue Item Anatomy

```
{
  scoring_hash_key:     "abc123__4567",         // unique queue ID
  scored_chatlogs_row:  6127,                    // row in Scored Chatlogs sheet
  contributor_name:     "Garyjob <garyjob...>",  // AS SCORED by Grok — may be wrong
  found_in_contributors:"TRUE" | "RESOLVE FAILED",// did Grok's name match contributors.json?
  tdgs_provisioned:     "300",                   // Grok's recommended TDG — IGNORE THIS
  tdgs_issued:          "0",                     // currently 0 until reviewed
  contribution_type:    "100TDG For every 1 hour of human effort" | "1TDG For every 1 USD..."
  contribution_description: "...",               // the full [CONTRIBUTION EVENT] text
  reporter_name:        "Edgar",                 // who submitted
  status:               "Pending Review"
}
```

**Key principle:** The `tdgs_provisioned` field is Grok's estimate — it is NOT authoritative.  
The **source of truth** is the `- Amount:` and `- Type:` fields inside `contribution_description`.

---

## 3. Core Rule: TDG Is Always Computed From The Event

**Never use `tdgs_provisioned` as the final TDG.** Always extract and compute:

| Event Type | Extract | Formula |
|-----------|---------|---------|
| `- Type: Time (Minutes)` | `- Amount: N` | `N / 60 * 100` (100 TDG per hour) |
| `- Type: Capital Injection` | `- Amount: N` | `N` (1 TDG per 1 USD) |

**Examples:**

| Amount | Minutes | TDG |
|--------|---------|-----|
| 5 | 5 min | 8.33 |
| 10 | 10 min | 16.67 |
| 15 | 15 min | 25 |
| 20 | 20 min | 33.33 |
| 25 | 25 min | 41.67 |
| 30 | 30 min | 50 |
| 45 | 45 min | 75 |
| 60 | 1 hr | 100 |
| 90 | 1.5 hr | 150 |
| 120 | 2 hr | 200 |
| 180 | 3 hr | 300 |
| 240 | 4 hr | 400 |
| 480 | 8 hr | 800 |

**Multi-contributor events:** The Amount is per-contributor. Each named contributor in `- Contributor(s):` gets the full computed TDG individually. Do not divide.

**Validation:** After computing, compare to `tdgs_provisioned`. Large discrepancies (>50%) should be noted in the review event for audit, but the computed value is what gets approved. Do not skip or reject solely because Grok's estimate differs.

---

## 4. The Three Scenarios

### SCENARIO A: Contributor Name Must Match a Known TDG Holder Exactly

**Problem:** Grok extracted a name that doesn't match any DAO member.  
**Rule:** The final `contributor_name` in the review event **must match exactly** — first against `dao_members.json` (all Contact sheet names), then `lineage-credentials/_cache/index.json` (469 TDG holders). Character-for-character, whitespace-for-whitespace. No fuzzy matching.

**Normalization map — apply BEFORE matching against BOTH lists independently:**

| Raw contributor_name from Grok | → Canonical Name (exact) | Matches via |
|-------------------------------|--------------------------|-------------|
| `Garyjob <garyjob@gmail.com>` | `Gary Teh` | both |
| `Gary Teh <garyjob@gmail.com>` | `Gary Teh` | both |
| `GaryTeh` | `Gary Teh` | both |
| `Sophia Truesight (admin+sophia@truesight.me)` | `Sophia Truesight` | dao_members.json |
| `Sophia Truesight` | `Sophia Truesight` | dao_members.json |
| `Claude Anthropic` | `Claude Anthropic` | dao_members.json |
| `Kimi Moon <admin+kimi@truesight.me>` | `Kimi Moon` | dao_members.json |
| `Kimi (Moonshot AI)` | `Kimi Moon` | dao_members.json |
| `Deep Seek` | `Deep Seek` | dao_members.json |
| `Elizabeth Wong` | `Elizabeth Wong` | dao_members.json |
| `Claude` (ambiguous — could be Claude Anthropic or human Claude) | _(escalate if not in either list)_ | — |
| `Edgar` | _(not a contributor — check `- Contributor(s):` in event body)_ | — |
| Any name with `<email>` suffix | Strip ` <email>`, then match | |
| Any name with `(...)` suffix | Strip ` (...)`, then match | |

**Note:** `Sophia` (human, 1250 TDG, lineage-credentials) ≠ `Sophia Truesight` (AI agent, dao_members.json). `Claude` (human, 3.33 TDG, lineage-credentials) ≠ `Claude Anthropic` (AI agent, dao_members.json). These are separate entities — do not conflate.

**Algorithm:**
1. Strip email brackets ` <...>` and parentheticals `(...)` from the raw name.
2. Remove `@`-containing words.
3. Trim whitespace, collapse multiple spaces.
4. **Exact match** against `dao_members.json` `name` field first (includes all Contact sheet entries, sentinels, etc.). If found → use that name.
5. **Exact match** against `lineage-credentials` `display_name` field second (469 TDG holders). If found → use that name.
6. If no match in either list → **Skip** with reason `"Unrecognized contributor: <raw name>"`.

**Special case — "Edgar":** Edgar is the submission agent, not a DAO contributor. Check the `- Contributor(s):` line in the event description. Use those names instead. If no named contributors in the event body → Skip with reason `"Edgar submitted but no contributor named in event"`.

---

### SCENARIO B: Compute TDG From Event (AI Agents Included)

**Rule:** All contributors earn TDG based on the work described in the event — including AI agents (Sophia, Claude, Kimi, Deep Seek).

**Decision table:**

| Has meaningful work description? | Amount present? | Action |
|----------------------------------|----------------|--------|
| Yes | Yes | Compute TDG from Amount + Type, **Approve** |
| Yes | No (missing Amount) | **Skip** — "Cannot compute TDG: missing Amount in event" |
| No (empty/placeholder description) | Any | **Reject** — "No meaningful contribution described" |

**Steps:**
1. Parse `contribution_description` for `- Type:` and `- Amount:`.
2. Compute TDG using the formula in §3.
3. Approve with the computed TDG.

---

### SCENARIO C: Edgar Should Enforce TDG Computation Server-Side

**Problem:** Currently, the Approve action submits a `tdgs_issued` value that Edgar trusts verbatim. A buggy or malicious client could submit an inflated TDG amount.

**Proposed defense-in-depth: Edgar recomputes TDG server-side.**

Add to Edgar's `POST /dao/submit_contribution_review` handler:

```
1. Receive the review event: action, scoring_hash_key, contributor_name, tdgs_issued (client-submitted), signed_text
2. Fetch the cache file from treasury-cache/review-queue/<hash>.json to get contribution_description
3. Parse - Type: and - Amount: from contribution_description
4. Compute server_tdg = Amount / 60 * 100  (for Time) or Amount (for Capital)
5. If |tdgs_issued - server_tdg| <= 1.0: accept, write tdgs_issued as-is
6. If |tdgs_issued - server_tdg| > 1.0: WARN in logs, but write SERVER_COMPUTED TDG (server_tdg)
   - Append a note to the review event: "[EDGAR OVERRIDE] Client submitted {tdgs_issued}, server computed {server_tdg}"
7. If cannot parse Amount from event: REJECT with 400 "Cannot compute TDG from event — missing Amount"
```

**This makes Edgar the TDG authority.** Client submits their computed value, but Edgar validates and overrides if necessary.

---

## 5. Decision Flow

```
FOR each item in review queue:
  1. NORMALIZE contributor name (Scenario A map)
     → Exact match against dao_members.json?
       YES → continue
       NO  → SKIP (unrecognized contributor)
  2. EXTRACT Amount + Type from contribution_description
     → Cannot parse?
       SKIP (missing Amount)
  3. COMPUTE TDG from rubric (Amount / 60 * 100 for Time, Amount for Capital)
  4. HAS meaningful work?
     YES → APPROVE with computed TDG
     NO  → REJECT (no meaningful contribution)
```

**Approve payload:**
```json
{
  "action": "Approve",
  "scoring_hash_key": "<key>",
  "contributor_name": "<exact name from dao_members.json>",
  "tdgs_issued": "<computed>"
}
```

**Reject payload:**
```json
{
  "action": "Reject",
  "scoring_hash_key": "<key>",
  "reason": "<specific reason>"
}
```

**Skip payload:**
```json
{
  "action": "Skip",
  "scoring_hash_key": "<key>",
  "reason": "<what needs human decision>"
}
```

---

## 6. Auto-Processing Limits

- **Max auto-approves per session:** 100
- **Max auto-rejects per session:** 50
- If >10 consecutive items require Skip → stop, report to governor
- Every action is logged with reasoning
- Review events signed with the reviewing agent's RSA key

---

## 7. Post-Review Report

```
Review Session Summary
- Items reviewed: N
- Approved: N (total TDG issued: X)
- Rejected: N
- Skipped (needs human): N
  - Name normalization failures: N
  - Missing Amount: N
  - Unrecognized contributor: N

Skipped items:
  <hash_key>: <reason>
  ...
```

---

## 8. How to Submit Reviews

Via `dao_client` CLI (PR6 — pending):
```bash
dao_client report_contribution_review \
  --hash-key <scoring_hash_key> \
  --action Approve \
  --contributor "Gary Teh" \
  --tdg 300
```

Via direct POST:
```
POST https://edgar.truesight.me/dao/submit_contribution_review
Content-Type: multipart/form-data
  action=Approve
  scoring_hash_key=<key>
  contributor_name=Gary Teh
  tdgs_issued=300
  signed_text=<RSA-signed [CONTRIBUTION REVIEW EVENT]>
```

---

## 9. Required Changes

| Change | Where | Priority |
|--------|-------|----------|
| Edgar server-side TDG computation (Scenario C) | `dao_protocol/truesight_dao_client/server/routes/dao.py` → `submit_contribution_review` handler | High |
| `report_contribution_review` CLI (PR6) | `dao_client` | Medium |
| Confirm AI agents are in `dao_members.json` as `member` role | `treasury-cache/dao_members.json` | Done — Sophia, Claude, Kimi, Deep Seek already present |

---

## 10. Maintenance

- Update the normalization map (§4, Scenario A) when new name variants appear.
- `dao_members.json` is the source of truth — contributor names there are exact canon.
- Revisit auto-processing limits (§6) monthly.
