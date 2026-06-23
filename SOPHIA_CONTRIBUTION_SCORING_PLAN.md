# Sophia — Score the Contribution Review Backlog

**Status:** Draft · plan-of-record · **Created:** 2026-06-23
**Handoff thread:** _(register on GO — see HANDOFF_PROTOCOL_OVERVIEW.md)_
**Owner on execution:** Sophia Truesight (autopilot, **Sentinel**)

---

## 1. Goal & interpretation

"Score all the contributions" = **review and finalise the Pending-Review backlog** in
`Scored Chatlogs`. These rows are *already* Grok-scored (each has a provisioned TDG amount);
"scoring" here means a Sentinel **reviews each one and submits a `[CONTRIBUTION REVIEW EVENT]`**
(Approve at the right TDG / Reject with reason / Skip+flag), so reviewed rows flow
`Reviewed → Transferred to Main Ledger` and the TDG is actually issued.

This is **not** Grok-scoring (that already happened) and **not** re-scoring from scratch — the
default is to **finalise Grok's provisioned amount**, with judgement only on contributor
resolution and obvious junk (see §5 policy). Re-scoring against the rubric is out of scope unless
§5 is changed by the governor.

> ⚠️ **This issues real TDG at scale.** Backlog as of 2026-06-23:
> **906 Pending-Review rows · ~90,694 TDG total** · 768 resolved (Col I = `TRUE`) ·
> 138 unresolved (`FALSE` / `RESOLVE FAILED`). Mass auto-approval is **gated** (see §6/§7).

---

## 2. Pre-flight checklist (confirm before any submission)

- [ ] **Identity** — Sophia signs review events with her own key; Edgar resolves it to
  **"Sophia Truesight"** and accepts because she is a **Sentinel** (`dao_members.json` roles
  include `sentinel`). Confirm the autopilot's Edgar keypair is the one registered to that name.
- [ ] **Submission tool** — there is **no review CLI yet** (PR6 of `SCORING_REVIEW_QUEUE_PLAN.md`
  was never built). Build it first (Phase 0) or POST signed events directly. Prefer the CLI
  (tested + reusable): `truesight-dao-report-contribution-review`.
- [ ] **Endpoints (prod Edgar, already live):**
  - `GET https://edgar.truesight.me/dao/review_queue?limit=N&after_filename=…` — paginated queue
    (cursor = `next_filename`, `has_more`), each item = the cache JSON
    (`scoring_hash_key`, `contributor_name`, `tdgs_provisioned`, `found_in_contributors`,
    `contribution_description`, `scored_chatlogs_row`, …).
  - `POST https://edgar.truesight.me/dao/submit_contribution_review` (multipart `text=<signed>`).
    Edgar **verifies Sentinel auth** and **rejects unknown contributor names (422)** — so a
    hallucinated name cannot be issued TDG (defense in depth, already deployed).
- [ ] **Contributor roster** — the canonical name list is `treasury-cache/dao_members.json`
  (= Contributors contact information Col A). Use it for resolution; do **not** invent names.
- [ ] **Backstops already in place:** GAS write-back matches `(hash + contributor)` and writes
  Col A; the transfer script re-validates the contributor before issuing TDG; the GAS
  double-counting guard makes re-submission idempotent.

---

## 3. Mechanism

```
Sophia turn:
  1. GET /dao/review_queue (page through with the cursor)
  2. For each item → apply the §5 policy → decide {Approve@tdg | Reject@reason | Skip+flag}
  3. For Approve/Reject: build [CONTRIBUTION REVIEW EVENT], sign as Sophia Truesight,
     POST /dao/submit_contribution_review  (ALWAYS include "- Contributor Name:" so splits
     land on the right row and Edgar can validate it)
  4. Skip → no event; add to the "needs human review" list
  5. Edgar → appends to Telegram Chat Logs + triggers GAS processApprovalRejections
     → Scored Chatlogs row → Reviewed + TDG + Col A → transfer script → Ledger history
```

The event payload (canonical, matches `report_contribution.html` / `dao_client`):
```
[CONTRIBUTION REVIEW EVENT]
- Action: Approve
- Scoring Hash Key: <hash>
- TDGs Issued: <amount>
- Contributor Name: <resolved roster name>
--------

My Digital Signature: <Sophia's public key>
Request Transaction ID: <RSA signature over the header up to and including -------->
```

---

## 4. Scoping for Sophia's turn cap (§5a)

Each review ≈ 1–2 tool calls; the autopilot turn cap is `CHAT_MAX_TOOL_ROUNDS` (≈30). So a
turn processes a **batch of ≤ 10 items**, reports, then (per the Advance marker) auto-advances to
the next batch or stops at a gate. 906 rows ≈ ~90 batches — designed to grind down over many
auto-advanced turns, not one mega-turn.

---

## 5. Review policy (the rubric Sophia applies per item)

| Situation | Decision |
|-----------|----------|
| Genuine `[CONTRIBUTION EVENT]`, provisioned TDG > 0, **contributor resolved** (Col I `TRUE`) | **Approve** at Grok's provisioned amount, `Contributor Name` = the row's name |
| Col I = `FALSE` / `RESOLVE FAILED`, but Sophia maps the contributor to **exactly one** roster name from the event's `My Digital Signature` / stated name | **Approve** with the resolved name (Edgar re-validates; 422 ⇒ treat as unresolved → Skip) |
| Col I unresolved and **no confident single match** | **Skip + flag** for human (never guess a name) |
| Obvious duplicate / test / spam / empty / nonsensical | **Reject** with a one-line reason |
| Provisioned amount = 0 | **Skip** (transfer ignores 0 anyway) |
| Amount looks anomalous vs the contributor's norm, or any judgement call | **Skip + flag** (do not silently adjust) |

**Hard rules:**
- **Default = finalise Grok's amount.** Do **not** re-score or adjust amounts; flag instead.
- **Never** invent / guess a contributor. The name written becomes who receives the TDG.
- **Always** send `Contributor Name` (so splits land on the right row + Edgar validates).
- Splits (one hash, multiple contributors) are independent rows — review each separately.

---

## 6. Human gates (mandatory before mass issuance)

1. **Dry-run sample (Phase 2):** Sophia produces a **proposed-decisions report** for the full
   906 (or a first slice) — `{row, contributor, provisioned, decision, reason}` — **without
   submitting anything**. Written to a tracked file / sheet for the governor.
2. **GATE-1 (governor):** Gary reviews the proposed decisions — especially the 138 unresolved
   resolutions and any Rejects/Skips — and replies `go` to authorise issuance. Sophia does **not**
   submit before this.
3. **Batched issuance (Phase 3):** Sophia executes the approved decisions in ≤10-item batches,
   reporting per batch (approved count, TDG issued, skipped/flagged). Auto-advance between batches;
   **pause and report** on any batch with >2 unexpected 422s or anomalies.
4. **GATE-2 (optional):** re-confirm with the governor after the first ~50 issued before
   auto-grinding the remainder.

---

## 7. Sequenced plan + resume tracker (§5c Advance markers)

| Unit | Advance | State |
|------|---------|-------|
| **PR0 — review CLI** (`truesight-dao-report-contribution-review` in dao_client) ← **RESUME HERE** | `auto` | ☐ build + test the signed `[CONTRIBUTION REVIEW EVENT]` submitter (or confirm direct-POST helper). Opens PR only; human merges. |
| PR1 — scoring policy module + dry-run reporter | `auto` | ☐ code that pages `review_queue`, applies §5, emits the proposed-decisions report (no submits) |
| Phase 2 — produce the dry-run report over all 906 | `gate: governor reviews report` | ☐ artifact for GATE-1 |
| **GATE-1** — governor authorises issuance | `gate: reply 'go'` | ☐ **STOP** — no TDG issued before this |
| Phase 3 — batched issuance (≤10/turn) | `auto` (after GATE-1) | ☐ submit approved decisions; per-batch report; skipped→flag list |
| GATE-2 — checkpoint after first ~50 | `gate: spot-check` | ☐ confirm a sample landed in Ledger history correctly |
| Phase 4 — finish remaining batches | `auto` | ☐ grind to zero; final report |

**RESUME HERE = PR0.** One PR per turn for PR0/PR1; Phase 3/4 are ≤10-item batches per turn.
`dao_client` / `truesight_autopilot` repos: **open PRs only, never self-merge.**

---

## 8. UAT (before GATE-1 sign-off)

- Submit **one** Approve for a known resolved row via the new CLI → verify Scored Chatlogs flips
  `Reviewed` + correct TDG + Col A, then `Transferred to Main Ledger`, and a matching Ledger
  history row appears. (We proved this path 2026-06-23 with the Claude Sentinel batch — 8/8
  single-contributor rows transferred.)
- Submit one **unresolved** row with a deliberately wrong name → expect Edgar **422** (no write).
- Confirm a Skip leaves the row `Pending Review` and adds it to the flag list.

---

## 9. Safety / rollback

- Edgar **422** blocks unknown contributors; GAS double-counting guard makes resubmits no-ops.
- A wrongly-approved row (before transfer) can be reset to `Pending Review` in the sheet; once
  `Transferred to Main Ledger`, reversal is a manual ledger correction — hence GATE-1.
- If a batch misbehaves, **stop** (the queue + sheet are the source of truth; nothing is lost).
- Do not exceed ~10 submits/turn (turn cap) and pace to respect Sheets/GAS quotas.

---

## 10. Open decisions for the governor (resolve before GO)

1. **Amount policy:** finalise Grok's provisioned amounts (default), or have Sophia re-score
   against the Initiatives Scoring Rubric? (Default = finalise.)
2. **Unresolved 138:** let Sophia attempt resolution + Skip-the-rest (default), or hand **all**
   unresolved to a human?
3. **Auto vs gated:** full auto-advance after GATE-1, or GATE every N batches?
4. **Rejects:** may Sophia Reject obvious junk, or Skip-and-flag everything non-approvable?
