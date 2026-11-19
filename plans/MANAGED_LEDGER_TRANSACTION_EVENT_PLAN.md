# MANAGED LEDGER TRANSACTION EVENT — Completion Plan

**Created 2026-10-27 (session: contracts C1/C2/C3 + MLTE tab). Owner: unclaimed. Governor: Gary Teh.**

**Why this document exists.** `FREIGHT_COST_AMORTIZATION_PLAN.md` §3-E2 treats MLTE as a
freight-lane concern. It is not — it is the general primitive for *any* signed movement
between managed ledgers (freight cash-out, inter-ledger holdings, claim retirement).
The freight plan is one consumer. This plan owns the event.

---

## 1. Where the work actually stands (verified live, 2026-10-27)

### 1.1 What exists

| Piece | State | Evidence |
|---|---|---|
| **Client CLI** | ✅ shipped, ⚠️ **stale shape** | `dao_protocol` PR #187 (2026-10-15); `truesight_dao_client/modules/report_managed_ledger_transaction.py`; `truesight-dao-report-managed-ledger-transaction` console script |
| **GAS derivation engine** | ✅ shipped | `tokenomics` PR #599 (2026-10-27); `google_app_scripts/1orWgdGckts55owiYOysR_y4sde52T_eUmrtDGAEkb4YV5DlUfJ0JZC5J/managed_ledger_transaction_processing.js` |
| **`Managed Ledger Transactions` tab** | ✅ created 2026-10-27 | `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`; sheetId `1766290154`; 17 cols A–Q; 0 data rows; 39 tabs total |

### 1.2 What is missing

| Piece | State | Evidence |
|---|---|---|
| Edgar events catalog entry | ❌ | `GET edgar.truesight.me/events-catalog` → **v12**, 49 events, **zero** MANAGED |
| `dispatch.ROUTING` tag | ❌ | `dao_protocol/truesight_dao_client/server/dispatch.py` — 0 hits for MANAGED |
| Webhook env var | ❌ | no `DAO_PROTOCOL_WEBHOOK_MANAGED_*` provisioned on the dao_protocol box |
| Row-creator (parser wiring) | ❌ | `parseManagedLedgerTransactionMessage` defined at L327, **called from nowhere** in all of tokenomics |

**Consequence.** No rows can be created, so the processor's `NEW`-gate has **never been exercised once**. The event has never executed end to end.

---

## 2. Does #599 supersede §3-E2?

**Yes — completely, on the design. And it silently orphaned the client.**

§3-E2 (2026-10-15) specified a deliberately simple shape: parse a signed
`Row N — Entity/Amount/Currency/Transaction Type` blob → append each row to the
target ledger's `Transactions` tab → dedupe on the Edgar hash. One ledger.

#599 (2026-10-27) is a different animal:

| Dimension | §3-E2 planned | #599 shipped |
|---|---|---|
| Granularity | append given rows | **derive** 4 rows from a declaration |
| Ledgers touched | one (`Ledger`) | **two** (`source` + `destination`), each opened by URL |
| Transaction types | — | `injection` / `movement` / `retirement` (`ALLOWED_TRANSACTION_TYPES`, L31) |
| Write gating | none | `retirement` derived but refused at commit (`COMMITTABLE_TRANSACTION_TYPES`, L36 → `BLOCKED`) |
| Price resolution | per-key `Currencies` lookup | `loadCurrencyPrices_()`; unknown key **throws**, never values at $0 |
| Balance proof | none | `assertLedgerBalances_` (L250) both sides |
| Failure atomicity | none | `appendRowsAtomically_` (L287) rolls back source rows if destination write throws |
| Dedupe key | **Edgar hash** | `Status === 'NEW'` — **different guarantee, see §6** |

The important inversion: **§3-E2 assumed the client was done and the server was the residual.** #599 built the server. The client stayed on the old §3-E2 shape. So the stale half is now the one §3-E2 called shipped.

---

## 3. The tab (created 2026-10-27)

Created via the `agroverse-ledger-manager@get-data-io.iam.gserviceaccount.com` SA
(`canEdit=True`), headers only, no data rows.

Location: `https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit`
— the sheet `TELEGRAM_LOGS_URL` resolves to, which is what L413 actually opens.

| Col | Header | `MLTE_COL` |
|---|---|---|
| A | Telegram Update ID | `UPDATE_ID: 0` |
| B | Telegram Message ID | `MESSAGE_ID: 1` |
| C | Managed Ledger Transaction Log Message | `LOG_MESSAGE: 2` |
| D | Reporter Name | `REPORTER: 3` |
| E | Source Ledger Name | `SRC_NAME: 4` |
| F | Source Ledger URL | `SRC_URL: 5` |
| G | Destination Ledger Name | `DST_NAME: 6` |
| H | Destination Ledger URL | `DST_URL: 7` |
| I | Transaction Type | `TYPE: 8` |
| J | Assets | `ASSETS: 9` |
| K | Assets Entity | `ASSETS_ENTITY: 10` |
| L | Equity Entity | `EQUITY_ENTITY: 11` |
| M | Value USD Number | `VALUE_USD: 12` |
| N | Effective Date | `DATE: 13` |
| O | Description | `DESCRIPTION: 14` |
| P | **Status** | `STATUS: 15` |
| Q | Ledger Lines Number | `LEDGER_LINES: 16` |

`Status` (P) is the control column. Exact values: `NEW`, `PROCESSED`, `BLOCKED`, `FAILED`.
Naming follows the house convention (`Capital Injection`, `Asset Receipts` tabs read
"Telegram Update ID", "… Log Message", "Reporter Name").

---

## 4. The processor's mechanics (how double-execution is prevented)

```js
for (var i = 1; i < data.length; i++) {
  if (row[MLTE_COL.STATUS] !== 'NEW') continue;   // L426 — the only gate
  ...
  sheet.getRange(rowNumber, MLTE_COL.STATUS + 1).setValue('PROCESSED');
  sheet.getRange(rowNumber, MLTE_COL.LEDGER_LINES + 1).setValue(lineRefs);
}
```

Terminal states written back:

- `PROCESSED` — committed; Q holds refs like `source:X=812-813; destination:Y=45-46`
- `BLOCKED` — derivation succeeded but the type is write-gated (`retirement`)
- `FAILED` — JSON parse error, derivation refusal, or commit error

**Two caveats that must reach any operator:**

1. **`FAILED` is not always "nothing happened."** Rollback covers the append step
   (§2). It does **not** cover the gap where rows append successfully and the
   *status write* then throws — the row is mislabelled `FAILED` while balances moved.
   **Before resetting any `FAILED` row to `NEW`, confirm col Q is empty.** If Q holds
   line refs, the commit landed; re-running would double-count.
2. **`NEW` is a human-only transition.** It appears exactly once in the codebase
   (L426, as a comparison) and is never assigned. Only the (unwritten) row-creator
   should ever write it.

---

## 5. 🔴 THE BLOCKER — the client and the engine do not speak the same language

This is the decision this plan exists to force. **It cannot be patched around.**

**What the shipped CLI declares to Edgar** (`canonical_labels`):

```
Ledger · Ledger URL · Date · Amount · Currency · Sender · Recipient ·
Description · Attached Filename · Destination Managed Ledger Transaction File Location
```

**What the engine's parser reads** (`parseManagedLedgerTransactionMessage`, L327):

```
Source Ledger · Source Ledger URL · Destination Ledger · Destination Ledger URL ·
Transaction Type · Assets Entity · Equity Entity · Claim Currency Key ·
Effective Date · Description · Request Transaction ID · My Digital Signature

plus, repeated:
  - Asset: <quantity> | <currency key>
```

**Overlap: one label (`Description`).** Nine of ten CLI labels resolve to `null` via
`extractField_`. `deriveTransactionRows_` throws at its first guard. A live
submission would fail on **every** row.

Known conflict — `conventions/CHOCOLATE_BAR_PRODUCTION_ACCOUNTING.md` §11.7 describes
this exact class of problem ("INCOMPATIBLE field names for the same event").

### Options

| # | Option | Cost | Consequence |
|---|---|---|---|
| **A** | **Rewrite the CLI to emit the #599 shape** | medium — new canonical_labels, N-line `- Asset:` input, `Transaction Type` enum, dual `Source`/`Destination` | Engine stands as-is. Governor must type two ledger URLs + a type + asset lines. Most faithful to the balance-proof design. |
| **B** | **Adapt the engine parser to the CLI shape** | medium — derive `source`/`destination`/`type` from `Ledger`/`Sender`/`Recipient`; single `Amount`+`Currency` becomes one `- Asset:` line | Keeps the shipped CLI. But the CLI shape **cannot express** multi-asset declarations or 4-row injections — the freight case (AGL15 −$2,098.354 + holdings in AGL8/AGL13) becomes inexpressible. |
| **C** | Two events: keep the simple CLI shape as MLTE, add a new event for typed multi-row | high — two primitives to register, route, document | Cleanest conceptually; worst timeline. |

**Recommendation: A.** Option B would re-introduce the exact limitation §3-E2 already
identified — that the simple single-ledger shape "fits no other primitive" for the
AGL15 freight cash-out. Building #599 and then constraining the client to the shape
#599 superseded wastes the engine. Option A is also the only one that preserves
`assertLedgerBalances_` as a real proof rather than decoration.

**Decision required from the governor.** Do not start step 3 before this is ruled.

---

## 6. Idempotency gap (found during this audit — not in §3-E2's carry-over)

§3-E2 specified: *"dedupe on the Edgar hash."* #599 did **not** carry that forward.
Its guard is `Status === 'NEW'`.

These are different guarantees:

- `NEW`-gate prevents **reprocessing a row that already exists** ✅
- Edgar-hash dedupe prevents **the same submission creating a second row** ❌

Without the second, a parser invoked twice (retry, webhook re-fire, cron overlap) appends
a duplicate declaration row and the processor commits it a second time — balances move twice.

**Fix.** The row-creator must key on Edgar's submission hash: before appending, scan
cols A/B (`Update ID`/`Message ID`) for the incoming identifiers and skip on match.
Both columns exist precisely for this; they are currently unpopulated by design because
no row-creator exists.

---

## 7. Sequence with gates

| # | Step | Owner | Gate |
|---|---|---|---|
| 1 | Create `Managed Ledger Transactions` tab, 17 headers A–Q | Sophia | ✅ **done 2026-10-27** |
| 2 | **Rule on §5** — client rewrite (A) vs parser adapt (B) vs split (C) | **Governor** | **blocks 3–6** |
| 3 | Register: `events_catalog.json` entry + `dispatch.ROUTING` tag. Note `tests/test_catalog_dispatch_coverage.py` enforces `ROUTING ⊆ catalog`, so these must land together. | code PR | |
| 4 | Align client ↔ engine per the §5 ruling | code PR | |
| 5 | Wire `parseManagedLedgerTransactionMessage` to a caller → append `NEW` rows **with Edgar-hash dedupe (§6)** | code PR | |
| 6 | Provision `DAO_PROTOCOL_WEBHOOK_MANAGED_TRANSACTION` on the dao_protocol box `.env` + restart (GAS `/exec` deployment URL; cron is the fallback) | Governor | **explicit go — live infra** |
| 7 | Prove the loop: one minimal `injection` end to end, verify `PROCESSED` + Q line refs + both ledgers balance | Governor + Sophia | **explicit go — moves a real balance** |

Steps 3–5 are one coherent `dao_protocol` PR each, or one PR if they stay small.

---

## 8. Consumers this unblocks

- **Freight cost amortisation** (`FREIGHT_COST_AMORTIZATION_PLAN.md` §3-E2) — AGL15's
  −$2,098.354 USD cash-out leg plus two "equity holdings" rows in AGL8/AGL13. Fits no
  other primitive: `[CAPITAL INJECTION EVENT]` writes only to the receiving ledger;
  `[DAO Inventory Expense Event]` always appends a negative Assets row.
- **AGL14 precedent** — rows 10–13 of the AGL14 ledger are a genuine signed GL
  submission (`[MANAGED LEDGER TRANSACTION EVENT]`, one-signed-blob-many-rows) that was
  **hand-typed from the signed text**; no automated handler ever consumed it.
- **Inter-ledger holdings** (`conventions/INTER_LEDGER_HOLDINGS.md`).

---

## 9. Related entries

- `OPEN_FOLLOWUPS.md` — `[MANAGED LEDGER TRANSACTION EVENT] — client CLI shipped; Edgar catalog/routing registration still the residual (Black King §3-E2)` (2026-10-15; **superseded in part**, now points here)
- `conventions/CHOCOLATE_BAR_PRODUCTION_ACCOUNTING.md` §11.7 — the INCOMPATIBLE field-names conflict
- `conventions/INTER_LEDGER_HOLDINGS.md`
- `FREIGHT_COST_AMORTIZATION_PLAN.md` §3-E2 — one consumer, not the owner
