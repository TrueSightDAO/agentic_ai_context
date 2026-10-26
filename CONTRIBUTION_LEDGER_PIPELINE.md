# Contribution → Ledger Pipeline (three stages)

**Read this before reporting that a contribution is "missing from the ledger".** A submission
is expected to sit in staging for up to a quarter. Absence from `Ledger history` is NORMAL —
it is not evidence of a broken pipeline.

Verified live 2026-10-26 against all three sheets.

---

## The chain

```
Edgar (/dao_protocol)
   │  every accepted event, all event types
   ▼
STAGE 1 — Telegram Chat Logs        (raw intake, immediate)
   │  Grok scorer
   ▼
STAGE 2 — Scored Chatlogs           (daily; Status="Pending Review", TDGs Issued=0.00)
   │  governor approval → GAS processAllReviewedRows
   ▼
STAGE 3 — Ledger history            (quarterly consolidation, ~every 3 months)
```

---

## Stage 1 — Telegram Chat Logs

| | |
|---|---|
| Spreadsheet | `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` |
| Tab | `Telegram Chat Logs` |
| Written by | Edgar, immediately on acceptance of **any** event |
| Row key | column A = event id, e.g. `Edgar_20261026020404_2740` |

This is the first home of **every** submission, not just chat-derived ones — the tab name is a
historical artifact. Columns: `A` event id · `E` contributor name · `G` full event body ·
`H` rubric classification · `I` TDGs Provisioned · `J` Status (`Pending` → `Successfully Completed` /
`Full Provision Awarded`).

> ~14,600 rows as of 2026-10-26.

## Stage 2 — Scored Chatlogs

| | |
|---|---|
| Spreadsheet | `1Tbj7H5ur_egQLRugdXUaSIhEYIKp0vvVv2IZ7WTLCUo` |
| Tab | `Scored Chatlogs` |
| Written by | Grok scorer (daily) |
| Service account | **`tdg_scoring` only** — the default Cypher Defense SA gets `403` |

The scorer applies the rubric and sets `Status = "Pending Review"`, `TDGs Issued = "0.00"`.
Governors then approve/reject, and approval is written back as `Reviewed` before the stage-3 transfer.

**`Scored Chatlogs!L` ("Main Ledger Row Number") is the foreign key** into stage 3. A row is
*still pending* iff column `L` is empty. This is how dedup works — rows with `L` populated are
already represented in `Ledger history`.

## Stage 3 — Ledger history

| | |
|---|---|
| Spreadsheet | `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU` (Main Ledger) |
| Tab | `Ledger history` |
| Cadence | **consolidated once every ~3 months** |
| Written by | GAS `processAllReviewedRows` (batch transfer) |

This is the canonical, authoritative record and the basis for TDG issuance/airdrop. ~12,500 rows.

---

## Rules for agents

1. **To confirm a submission was accepted, check Stage 1** — search spreadsheet `1qbZZhf…`
tab `Telegram Chat Logs` for the event id or a distinctive phrase from the description.
2. **NEVER conclude "the ledger is broken" because a row is absent from `Ledger history`.**
A fresh submission is supposed to be absent for up to a quarter.
3. To trace a specific row's progress: Stage 1 row → find it in `Scored Chatlogs` (may take a day)
→ get column `L` value → that row number in `Ledger history`.
4. `Ledger history` is **not** the place to verify a new contribution. Do not sweep all 38 tabs
looking for one.
5. When reporting status, say *which stage* the row is in. "Recorded by Edgar, sitting in stage 1
as `Pending`" is accurate. "Not in the ledger" is misleading.

## Known gotchas

- **Service-account split.** The default SA (`GOOGLE_APPLICATION_CREDENTIALS`) can read the Main Ledger
  and Stage 1, but gets `403` on Stage 2. Use the `tdg_scoring` SA for `1Tbj7H5…`.
- **Canonical field labels.** `CONTRIBUTION EVENT` canonical labels are `Type`, `Amount`,
  `Description`, **`Contributor(s)`**, `TDG Issued` (`app/main.py:1617`). `Contributor` (singular)
  is not the canonical key — prefer `Contributor(s)` when submitting.
- **Rubric.** `Type: Time (Minutes)` → **5 minutes = 8.33 TDG** (1.6667 TDG/min), so 10 min ≈ 16.67 TDG.

---

_Last verified 2026-10-26 — Stage 1 rows 14613–14614 (Gary Teh 10-min tutorial; a corrective
Sophia Truesight 1-min row) both present and `Pending`; Stage 2 reachable only via `tdg_scoring`._
