# Contribution → Ledger Pipeline (three stages)

**Read this before reporting that a contribution is "missing from the ledger".** A submission
is expected to sit in staging for up to a quarter. Absence from `Ledger history` is NORMAL —
it is not evidence of a broken pipeline.

Verified live 2026-10-26 against all three sheets.

> ### ⚠️ Staleness has two meanings — do not conflate them
>
> | Hop | Expected delay | If it exceeds that |
> |---|---|---|
> | Stage 1 → Stage 2 | **~1 day** | 🔴 **BROKEN** — investigate the scorer |
> | Stage 2 → Stage 3 | **~1 quarter** | 🟢 **NORMAL** — nothing to do |
>
> "Absence from `Ledger history` is normal" applies to the **second row only**.
> It does **not** license concluding a row is healthy merely because Edgar accepted it.
> A row parked in Stage 1 for weeks is a **failure**, and Stage 1 looks perfectly healthy
> while it happens — the write succeeds, the derived view silently freezes.
>
> **Status as of 2026-11-17 09:15 UTC (supersedes the 2026-10-26 note below):** Stage 2 *is*
> running again but is **lagging**. Newest `Scored Chatlogs` date is `20261114` (3 days stale) and
> the newest `Pipeline Health` row is `11/17/2026 01:07` against a **15-minute** cadence — i.e. the
> trigger has silently stopped. `Submissions Left to Score` = 290. See `OPEN_FOLLOWUPS.md` →
> "Stage-2 scoring trigger silent-stalled 2026-11-17".
>
> The 2026-10-26 note below is **retained for history but is no longer the current state** — the
> scorer has since written rows through `20261114`. Do not re-assert "Stage 2 is dead" from it.
>
> **Prior state (2026-10-26, historical):** newest Stage 2 row was dated `20260910`
> (column `L` = `11412`) — the Grok scorer had written nothing for ~6 weeks.

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
`H` rubric classification · `I` TDGs Provisioned · `J` Status · `N` Scoring Hash Key.

> ⚠️ **Header is row 2, not row 1** — a stray `Next Expected Airdrop Date` row sits above it.
> Sampling with row 1 as the header silently shifts every column read.

> **`J` is NOT a reliable scored/unscored signal.** It is documented as `Pending` →
> `Successfully Completed` / `Full Provision Awarded`, but on 2026-11-17 two freshly submitted
> `[CONTRIBUTION EVENT]` rows carried `J = Successfully Completed` with **`I` empty** and **no**
> `Scored Chatlogs` counterpart. Treat `I`/`L` and Stage-2 presence as the truth, not `J`.

> ~15,110 rows as of 2026-11-17.

## Stage 2 — Scored Chatlogs

| | |
|---|---|
| Spreadsheet | `1Tbj7H5ur_egQLRugdXUaSIhEYIKp0vvVv2IZ7WTLCUo` |
| Tab | `Scored Chatlogs` |
| Written by | Grok scorer (**daily — verify it is alive**, see gotchas) |
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
6. **Before calling a row "healthy", confirm Stage 2 is actually moving.** Presence in Stage 1
proves Edgar accepted it — nothing more. If Stage 2's newest row is more than a few days old,
report the row as **stuck in Stage 1 pending a broken scorer**, not as progressing normally.

## Known gotchas

- **Service-account split.** The default SA (`GOOGLE_APPLICATION_CREDENTIALS`) can read the Main Ledger
  and Stage 1, but gets `403` on Stage 2. Use the `tdg_scoring` SA for `1Tbj7H5…`.
- **Canonical field labels.** `CONTRIBUTION EVENT` canonical labels are `Type`, `Amount`,
  `Description`, **`Contributor(s)`**, `TDG Issued` (`app/main.py:1617`). `Contributor` (singular)
  is not the canonical key — prefer `Contributor(s)` when submitting.
- **Rubric.** `Type: Time (Minutes)` → **5 minutes = 8.33 TDG** (1.6667 TDG/min), so 10 min ≈ 16.67 TDG.
- **Stage-2 scorer liveness.** Read the newest row of `Scored Chatlogs` via the `tdg_scoring` SA
  and compare its date to today. The scorer stopping is **silent** — Stage 1 keeps filling, so
  every intake-side surface looks fine. Observed dead on 2026-10-26 (last row `20260910`,
  `L`=`11412`). A "daily" stage that has not written for weeks is a stop-the-line finding, not
  a backlog item.
- **Header offsets.** Stage 1 `Telegram Chat Logs` header is **row 2** (stray row above it);
  Stage 2 `Scored Chatlogs` has **two preamble rows**, so its header is **row 3**. Both have
  already produced false readings in past sessions.
- **`Pipeline Health` is the only liveness signal, and it is negative-evidence only.** It logs
  `OK` rows every 15 minutes while healthy, so a *stopped* trigger produces **no rows at all** —
  not an error. Check the newest timestamp, not the outcome column. On 2026-11-17 the trigger had
  been silent for ~8 hours with the previous 300 outcomes all `OK`.

---

_Last verified 2026-11-17 09:15 UTC — Stage 1 at **15,110** rows, Stage 2 at **7,508**. Today's
two reel contributions (`Edgar_20261117083216_3732` Sophia 210 min, `Edgar_20261117083223_3734`
Gary 45 min) are present in Stage 1 with valid col-N hashes but **not yet in Stage 2**. Stage 2's
newest date is `20261114`; the scoring trigger last fired `11/17 01:07` against a 15-minute cadence._

_Re-verify Stage 2 liveness on every future check of this document — that is the stage that
fails silently, and the one this file exists to stop agents from misreading._
