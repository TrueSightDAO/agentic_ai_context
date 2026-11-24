# Recurring Transaction Enrollment SOP — monthly TDG payees

**What this covers:** adding a person or entity to the `Recurring Transactions` tab of the Main Ledger so the monthly automation pays them TDG on a schedule (warehousing stipends, subscriptions, virtual offices, infrastructure costs).

**Last verified:** 2026-11-23, against the live sheet and the live GAS source.

---

## 1. The pieces

| | |
|---|---|
| Ledger spreadsheet | `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU` (PRODUCTION) |
| Registry tab | `Recurring Transactions` |
| Output tab | `Ledger history` — writes col B = `Recurring Tokenizations` |
| GAS script id | `1LxWu9hOs56JZ6Mbxra3eDv74xjpjgkJQW40xjpQBIHObsqiv1D5jr5fK` |
| GAS source | `tokenomics/google_app_scripts/1LxWu9hOs56JZ6Mbxra3eDv74xjpjgkJQW40xjpQBIHObsqiv1D5jr5fK/tdg_recurring_tokenization_monthly.js` |
| Script owner | `garyjob@agroverse.shop` |
| Trigger | scheduled; manual fallback `<deployment>/exec?action=processRecurringTransactions` |

**Tokenization rate:** col D is interpreted as USD, and the row written to `Ledger history` hardcodes col D = `1TDG For every 1 USD of liquidity injected`, so **col D collapses to 1 TDG per USD** on this path (160 → 160 TDG).

---

## 2. ⛔ The tab is owner-protected — you cannot write it

`Recurring Transactions` is protected as a **whole sheet** (`sheetId 33812003`) with **no editor list**, i.e. owner-only.

All ten service accounts were tested on 2026-11-23 and **every one was refused**:

| Service account | Result |
|---|---|
| agroverse-ledger-manager, edgar-aws-billing-automation, tokenomics-schema, edgar-dapp-listener, sophia-truesight, agroverse-market-research, agroverse-qr-code-manager, cypher-defense | `APIError [400] You are trying to edit a protected cell or object` |
| tdg_scoring | `403` — no permission |
| upc_barcode | `PermissionError` |

This is **not** a credential problem. Do not spend time hunting for a service account that works; there isn't one. `credentials/google_sheet_sa_access_matrix.json` states it plainly: `"Recurring Transactions": {"write": []}`.

### Therefore the row is written one of two ways

1. **The governor pastes it by hand** into the next free row (fastest, no code).
2. **A one-time GAS function** appended to the automation's own project and run from the Apps Script editor as `garyjob@agroverse.shop`. This is the sanctioned precedent — see `add_claude_pro_row.js` in the same project folder.

An agent may **prepare** the row (and PR the helper), but must not claim it is done until a human has run it and the row has been read back.

---

## 3. The row schema

Nine columns, A–I. Verified against live rows 12–25.

| Col | Field | Notes |
|---|---|---|
| **A** | Description | Free text. Convention: `<Name> - <Place> <Type>\n\nStart Date: <YYYYMMDD>` |
| **B** | Source | **Must exactly equal the `Ledger history` col A contributor name.** See §4.3. |
| **C** | Transaction Type | **Exactly** `Tokenization` |
| **D** | Amount (USD) | **Must be a real number**, not text. See §4.1. |
| **E** | Billing Period | **Exactly** `Monthly` |
| **F** | Most Recent Tokenization Date | `YYYYMMDD`. Drives the payout window. See §5. |
| **G** | Start Date | `YYYYMMDD`. Supplies the day-of-month for the cadence. |
| **H** | (AWS-billing key) | Blank on GAS-enrolled rows. `GARYJOB` on the AWS-billing row. |
| **I** | Automation Location | `Automation Location\n\n<url>`. **Documentation only — never read.** See §6. |

### Reference row — a warehousing stipend

```
A: Pinky Blau - Palo Verde California USA Warehousing

   Start Date: 20261123
B: Pinky Blau
C: Tokenization
D: 160
E: Monthly
F: 20261123
G: 20261123
H: (blank)
I: Automation Location

   https://script.google.com/home/projects/1LxWu9hOs56JZ6Mbxra3eDv74xjpjgkJQW40xjpQBIHObsqiv1D5jr5fK/edit
```

---

## 4. Four traps that fail SILENTLY

The automation has no error reporting. A malformed row is simply **skipped forever** and nothing anywhere tells you why. Check all four before considering the enrollment done.

### 4.1 Col D must be a number, not text

`fetchRecurringTransactions()` filters on:

```js
typeof amount === 'number' && !isNaN(amount)
```

If `160` lands as the **string** `"160"` — which is what happens when a value arrives via CSV paste, or when a helper writes it quoted — `typeof` is `'string'`, the condition fails, and **the row is dropped with no log line**. Write it as a JS number.

> Sanity check the type, not just the visible value. `'160'` and `160` look identical in the sheet.

### 4.2 Col C and E must match exactly

`type === 'Tokenization'` and `frequency === 'Monthly'`. Not `tokenization`, not `Monthly Tokenization`, not `Monthly ` with a trailing space.

### 4.3 Col B must EXACTLY equal the Ledger contributor name

`tokenizedAlready()` de-duplicates by exact string comparison:

```js
if (ledgerContributor === contributor && ledgerStartDate === description && ledgerDate === expected_date)
```

where `contributor` came from Recurring col B and `ledgerContributor` from `Ledger history` col A. **Any** drift — a trailing space, an accent, `Pinky B.` vs `Pinky Blau` — defeats the de-dup guard, and the person is re-paid **every single run**, forever. Pin col B character-for-character to the ledger name.

### 4.4 Col G must contain a parseable 8-digit date

`convertToYYYYMMDD()` extracts the first `\d{8}` from the cell. A human-formatted `Nov 23, 2026` will parse as `N/A`, and the row is dropped (`startDateStr !== 'N/A'` is a filter condition).

---

## 5. Start-date semantics — getting the first payout right

`calculateTokenizationDates(start_date, recent_check_date)`:

1. Reads **F** as `recent_check_date` and **G** as `start_date`.
2. Starts at **F + 1 month**, then **overwrites the day-of-month with G's day**.
3. Emits every monthly pivot while `pivot <= today`.

**Consequence:** the answer depends on **F**, not G, for *which* months are paid — but on **G** for the day of the month.

| F | Result |
|---|---|
| `F = today` | next pivot is next month → **first payout next month**, nothing retroactive |
| `F = last month, same day` | pivot == today → **that month is paid now** (a backfill) |
| `F = several months back` | **catch-up payment for every missed month** |

**F self-heals.** `updateLastCheckDate()` overwrites F with the run date on *every* pass, whether or not anything was tokenized. So a conservative `F = today` costs at most one month of delay and is the safe default for a brand-new enrollee whose start date is ambiguous.

**Pinned-day quirk:** because step 2 forces G's day onto every pivot, an enrollee whose G day is **31** gets 28/30-day months clamped, and — combined with F self-healing to the run date — can be paid **twice in one calendar month**. Prefer G days ≤ 28 unless the billing date genuinely matters.

---

## 6. Column I is documentation only

**The automation never reads column I.** It reads columns A–G only.

This matters because it is a very easy thing to get backwards. An earlier audit concluded that three rows (Jenifer Runnion, HackerDojo, Will Chen) were "missing column I and therefore may never be paid." **Their payout records disprove it** — all three were tokenized successfully with column I blank.

Populate column I anyway, to match rows 13–22 and to preserve the human trail to the owning script. But never treat a missing column I as a bug, and never "fix" a non-paying row by adding one.

---

## 7. The email / identity question

**This payout path does not need an email.** It reads only:

- `Recurring Transactions` (A–G)
- `Ledger history` (A–H)

It **never** touches `Contributors contact information`, Edgar, or digital signatures. Column B is a free-text label matched against the ledger — it is not an identity join.

So an email-less contributor **can** be paid. But decide this deliberately, because `[CONTRIBUTOR ADD EVENT]` **does** hard-require `Contributor Email`, and without it the person has **no registered DAO identity and no digital signature**. Precedent: ~27% of the contributors tab (330 of 1,218 rows) has a blank email.

The two concerns are separate:

| Question | Answer |
|---|---|
| Can they be paid monthly without an email? | **Yes** |
| Do they have a signed DAO identity without one? | **No** |

If the governor says "no email needed," record that decision in the contributor's Notes cell so it is not relitigated every session.

---

## 8. Procedure

1. **Confirm the person is genuinely new** — read `Ledger history` for any prior `Recurring Tokenizations` rows under their name. Duplicate enrollment double-pays.
2. **Register them as a contributor** (`Contributors contact information`) — or confirm they already have a row. Record in Notes why there is no email, if there isn't.
3. **Decide F and G.** Default `F = G = today`. Confirm with the governor whether the first payout should be this month (backfill) or next.
4. **Write the row** — governor pastes it, or run a one-time helper as the script owner. Write col D as a **number**.
5. **Read the row back** and verify columns A–I *and* `typeof D === 'number'`. A helper such as `verifyPinkyBlauRow()` in `add_pinky_blau_row.js` logs this, flagging a non-numeric amount explicitly.
6. **Report** the row number and the values to the governor. Do not report "enrolled" from a successful write alone — only from a read-back.

---

## 9. Recovery — if the trigger stops paying

Known issue on this project: `script.projects.run` can fail for **every** function with `"server error occurred while reading from storage. Error code NOT_FOUND"`, even for pure in-memory functions. The `/exec` web path bypasses it.

If the monthly trigger goes quiet:

1. Recreate the web-app deployment (`executeAs: USER_DEPLOYING`, `access: ANYONE_ANONYMOUS`) if it has been undeployed.
2. Trigger a catch-up: `GET <deployment>/exec?action=processRecurringTransactions`. The response returns immediately; the actual run continues server-side past the client timeout.
3. Verify by reading the newest `Recurring Tokenizations` rows in `Ledger history`.

Full history of this incident is in `OPEN_FOLLOWUPS.md` ("TDG Monthly Recurring Tokenization: GAS `:run` API NOT_FOUND quirk").

---

## 10. Checklist

- [ ] Not already enrolled (no prior `Recurring Tokenizations` rows in `Ledger history`)
- [ ] Col B **exactly** equals the `Ledger history` col A name
- [ ] Col C is exactly `Tokenization`
- [ ] Col D is a **number** (verified by `typeof`, not by eye)
- [ ] Col E is exactly `Monthly`
- [ ] Col F and G are 8-digit `YYYYMMDD`
- [ ] First-payout window confirmed with the governor
- [ ] Row read back and all nine columns verified
- [ ] Row number reported
