# QA Live-Ledger Test Procedure

**Applies to:** any E2E/QA verification that writes real ledger events (`[ASSET RECEIPT EVENT]`, `[INVENTORY MOVEMENT]`, `[SALES EVENT]`, etc.) against the **main ledger** (1GE7PUq-…) or its public-facing surfaces (treasury/AUM figures, truesight.me, dapp).

**Status:** mandatory convention. Supersedes ad-hoc live-ledger testing.

---

## Why this exists

On **2026-08-27** the autopilot verified asset-receipt-ingest fixes (PRs #411/#427/#431) by submitting two live `[ASSET RECEIPT EVENT]`s against the main ledger:

| Currency | Qty | Unit price | Offchain rows |
|---|---|---|---|
| `QA Verification Sticker 4x3cm (Test 20260827)` | 100 | **$100** (bad fallback) | 4178 |
| `QA Verification Sticker 4x3cm Round2 (Test 20260827b)` | 100 | $0.0581 | 4179 |

Both created **Currencies rows** (col A = name, col B = unit price) and **positive offchain inventory legs** that were never removed. The `$100` rate × qty 100 inflated the public treasury figure by **~$10,000 for 2 days** (was $27,862.31, corrected to $17,899.20). The bad price came from the ingest fallback `unitCost = parseLandedCostFromDescription_(desc) || amount` when no paired contribution/landed-cost was available.

The run was **ad-hoc** — no checked-in script, no cleanup step. This document makes cleanup mandatory.

---

## The procedure

### 1. Before you test

- Prefer a **sandbox/scratch ledger** whenever the flow under test allows it (clone the ledger, point the ingest at the clone).
- If the test MUST run against the live ledger, name every test item with `(Test YYYYMMDD)` in the currency name (e.g. `QA Verification Sticker 4x3cm (Test 20260827)`) so it is unambiguously identifiable.
- State the cleanup plan **before** submitting: which rows/currencies will be created, and how they will be removed.

### 2. While you test

- Record every submitted event's update ID / offchain row numbers as you go (they are the cleanup keys).
- Do not batch more than one test run per currency name; a `(Test YYYYMMDD)` suffix plus a Round suffix (`...b`) is fine.

### 3. Self-clean — IMMEDIATELY after verification completes (same session, before closing the task)

> **The cleanup is PART of the E2E run, not a follow-up task.** See the
> mandatory run checklist below — the expense-off and row-deletion steps are
> numbered items in the run itself, and the run is not complete until the
> treasury figure is verified back at its pre-test value.

For every test item created by the run:

### 3a. Asset-receipt E2E run — mandatory run checklist

Every asset-receipt E2E run (any currency, live or sandbox ledger) executes ALL of the following, in order:

1. **Submit** the test `[ASSET RECEIPT EVENT]` (currency named `… (Test YYYYMMDD)`).
2. **Verify ingest** — confirm `asset-receipt-ingest` processed it: offchain leg written, audit tab logged the update ID.
3. **Verify Currencies row** — if the ledger is live, confirm NO rate row was created for the test currency (QA guard fires; log shows `QA GUARD: skipped …`). If a rate row WAS created, that is a test failure — fix before proceeding.
4. **Expense off** — submit the paired `[EXPENSE EVENT]` / `[DAO Inventory Expense Event]` for the exact qty, so the positive offchain leg nets to zero (or delete the offchain rows, documented in the audit trail).
5. **Delete the test Currencies row** (if one was created) from the live `Currencies` tab.
6. **Verify treasury/AUM** returns to its pre-test value (e.g. `tdg_wix_dashboard` recalc; truesight.me/dapp unchanged).
7. **Record** the run + cleanup in `OPEN_FOLLOWUPS.md` (update IDs, rows deleted, before/after treasury).

Steps 4–7 are **mandatory** — a run that stops after step 3 is incomplete and MUST NOT be reported as passed.

1. **Expense off the inventory**: submit an `[EXPENSE EVENT]` (or `[DAO Inventory Expense Event]`) for the exact quantity received, referencing the same currency, so the positive offchain leg nets to zero — **or** delete the positive offchain rows directly (documented in the audit trail).
2. **Delete the test Currencies row(s)** from the live `Currencies` tab (exact col-A match, `(Test …)` names only). Never leave a test rate row — it multiplies any lingering quantity into phantom treasury value.
3. **Re-verify the treasury/AUM figure** returns to its pre-test value (e.g. `tdg_wix_dashboard` recalc; confirm truesight.me/dapp shows the same balance as before the test).
4. **Record the cleanup** in `OPEN_FOLLOWUPS.md` under `## Pending` (or close out the existing entry): update IDs, rows deleted, currencies deleted, before/after treasury figures.

### 4. Do NOT

- ❌ Leave `(Test` currencies in the live Currencies tab beyond the verification window (max 1 business day, and only if a legit expense-off is pending).
- ❌ Reuse a `(Test)` currency name across runs without cleaning the first run's rows first.
- ❌ Let a test receipt ride on the ingest fallback price (`unitCost = amount`) — always pair a contribution or explicit landed cost, or use a sandbox ledger.

---

## Companion guard (tokenomics asset-receipt-ingest)

`asset_receipt_ingest/Code.gs` now **skips creating a Currencies rate row** for currency names matching the test pattern (`(Test` / ` test ` / `test$`). The offchain leg is still written so ingest QA can verify end-to-end, but no rate row exists to multiply into treasury value. A stray test receipt therefore cannot inflate AUM — and the convention above still requires expensing the offchain rows off.

---

## Escalation

If you find a phantom test row in the ledger that was NOT cleaned up (currency contains `(Test`, or rows whose description/update ID matches a QA run):

1. Delete the offchain legs and Currencies rows (they are test data, not real inventory).
2. Re-run the treasury recalc and confirm the public figure drops back.
3. File a follow-up in `OPEN_FOLLOWUPS.md` with the update IDs so the QA session that leaked them is traced.

---

*First incident: 2026-08-27 (submitted) → 2026-08-29 (cleaned + this convention written). Treasury $27,862.31 → $17,899.20.*
