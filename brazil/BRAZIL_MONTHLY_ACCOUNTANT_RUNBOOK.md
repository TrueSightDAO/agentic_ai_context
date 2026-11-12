# Brazil Monthly Accountant — recurring BRL obligation runbook

> **Status:** SOP, first written 2026-11-12. Owner: Sophia. Applies to the recurring
> accounting fee for the Black King / Mateus Reis lane.
>
> **Read this before booking any monthly accountant payment.** The sequence below is
> ordered deliberately; running the steps out of order produces a negative balance and an
> invisible expense (see §4).

---

## 1. The obligation

| Field | Value |
|---|---|
| **Counterparty** | **Jussileide Bomfim Alves Longo** — accountant |
| CPF (Pix key) | `96466189520` |
| Bank | BCO SANTANDER (BRASIL) S.A. |
| **Billing entity** | **MATEUS REIS PEREIRA** — CNPJ `50.042.585/0001-80` |
| **Amount** | **R$ 500,00 / month** |
| **Due** | 15th of the **following** month (Sept service → due 15.10; Oct service → due 15.11) |
| Document | `RECIBO DE HONORÁRIOS PROFISSIONAIS` (one per service month) |
| Delivery channel | WhatsApp group **“Black King - Contab”** — she is **not** on Telegram; Gary relays |
| Payer of record | Pix from **Zhiwen Teh**, BCO RENDIMENTO (individual, not the LLC) |

Jussileide is the same contracted accountant already recorded in
`brazil/BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md` §contacts (line ~66), alongside
Saymon (NF-e specialist). This fee is the recurring cost of the Black King CNPJ
reinstatement / NF-e work tracked there — **not** a new vendor.

---

## 2. Two-leg booking — order is load-bearing

Paying a BRL obligation from a USD balance is **always two ledger events**, never one.

### Leg 1 — fund the BRL balance

```
python3 -m truesight_dao_client.modules.report_currency_conversion \
  --ledger offchain \
  --warehouse-manager "Gary Teh" \
  --source-currency USD \
  --source-amount <USD actually debited> \
  --target-currency "Brazilian Reis" \
  --target-amount <R$ total> \
  --implied-rate <target/source> \
  --conversion-date <YYYYMMDD> \
  --description "Currency conversion to settle <counterparty> accountant fees <months>" \
  --attached-filename <conversion receipt> \
  --dry-run
```

- `offchain` is the ledger for **every** historical conversion (54/54) — do not invent another.
- `--dry-run` first, always. Drop the flag only after reading the payload back.
- The GAS processor (`currency_conversion_processing.gs`) writes the **two** offchain rows
  itself: source debit **negative**, target credit **positive**. Never hand-write those rows.

### ⏸ Gate — do not proceed until Leg 1 is PROCESSED

Re-read the conversion intake row and confirm `Status = PROCESSED`, then confirm the BRL
balance actually rose by the target amount. If it has not landed, **wait**. Do not resubmit
(see §5).

### Leg 2 — book the expense, one row per service month

```
python3 -m truesight_dao_client.modules.report_dao_expenses \
  --dao-member-name "Gary Teh" \
  --amount 500 \
  --currency "Brazilian Reis" \
  --ledger offchain \
  --description "Accountant fees — Jussileide Bomfim Alves Longo (Mateus Reis Pereira, CNPJ 50.042.585/0001-80) — services rendered <Month>/<Year>. Pix ID <id>, ref <ref>" \
  --attached-filename <recibo .docx/.pdf> \
  --dry-run
```

- **One row per service month**, not one combined row. The recibos are per-month documents;
  combining them loses the monthly P&L attribution.
- Attach the month's own recibo. Put the Pix image on one row (or both) and cite the Pix ID
  in the description of both, so either row reconciles to the single payment.
- The expense is **not** a new obligation being created — it discharges a recibo already
  issued. Description should say “services rendered”, not “advance”.

---

### ⚠️ Book Leg 2 in exactly ONE bucket — never both

This is the trap that actually fired on 2026-11-12, and it is easy to walk into because
each individual row looks correct.

**What happened.** The Sep/Oct recibos were booked **twice**, in two different currency
buckets, from what looked like two different sources of truth:

| Rows | Bucket | Amount each | Basis |
|---|---|---|---|
| **5386 / 5387** | `Brazilian Reis` | **R$500,00** | the recibo's native face value |
| **5544 / 5545** | `USD` | **US$89,54** | R$500 converted at BRL 5.5840 |

Both are arithmetically defensible in isolation. Booked together they count the same two
recibos twice — and the USD side is **doubly wrong**, because Leg 1's conversion rows
(5384/5385, USD 378.05 → R$ 2,085) **already carry the USD cost**. The BRL is the funded
side; expensing a USD equivalent on top charges the DAO twice for one Pix.

**The rule.** Leg 2 is booked in the **target** currency only (`Brazilian Reis`). Never also
post a source-currency (`USD`) equivalent of the same document. The source-currency cost
lives in Leg 1 and nowhere else.

**Detection.** Pre-flight assertion 3 must search **every** currency bucket, not just the one
you intend to write to. Grep `offchain transactions` for the counterparty + billing CNPJ and
inspect **all** currencies returned:

```
# per service month, expect ONE row total across ALL currencies
# 500 BRL in Brazilian Reis  XOR  ~89.54 USD  — never both
```

A row in a *different* bucket than the one you're about to write is the signature of this
bug, and a same-currency-only check will never find it.

**Fix if it fires.** Both rows are signed, so neither can be edited in place
(`OPERATING_INSTRUCTIONS.md` §9c.4c — an amount change is a restatement). Append **one
unsigned reversal row per duplicated row** in the bucket being zeroed, and do **not** re-enter
the expense — the surviving row already is the correct entry:

| Reversal | Amount | Currency | Zeroes |
|---|---|---|---|
| 5797 | +89.54 | USD | 5544 (Sept) |
| 5798 | +89.54 | USD | 5545 (Oct) |

Verify the four rows net to **0.00**, and write each reversal's amount with
`USER_ENTERED` then read it back as an `UNFORMATTED_VALUE` float (§9c.5a) — `RAW` types it as
text and every `sum()` silently ignores it.

**Note on row identity.** 5544 and 5545 are *not* duplicates of each other — they are
September and October. They are duplicates of 5386 and 5387. Confirm month-by-month before
zeroing anything; treating the pair as mutually duplicate would erase a real month's expense.

---

## 3. Pre-flight and post-flight assertions

**Before submitting anything:**

1. Read the recibos and confirm the amounts sum **exactly** to the Pix amount. (Sept R$500 +
   Oct R$500 = R$1,000 = the Pix. Any mismatch means stop and reconcile the documents first.)
2. Confirm the **implied rate** is sane against the reference rate of the day. If the USD
   debit is outside a plausible band for the BRL received, the conversion and the payment do
   not reconcile — investigate before booking.
3. **Search for existing rows first.** Grep the `offchain transactions` Description column for
   the counterparty name, the billing CNPJ, and “accountant”. Zero hits is the expected
   clean-slate state; any hit means part of this is already booked.
4. Confirm the `Brazilian Reis` balance currently reads the expected opening figure.

**After Leg 2:**

5. `Brazilian Reis` must return to **exactly** its pre-conversion value. A pure pass-through
   leaves the BRL balance unchanged — no value is created, the real cost sits in the USD leg.
   *If it does not return to the opening figure, arithmetic is wrong somewhere: stop.*
6. Verify the written amount back as an **`UNFORMATTED_VALUE` float**, not a formatted string
   (§9c.5a — `RAW` input silently types numbers as text and `QUERY sum()` then ignores them).
7. Confirm the offchain net for `Brazilian Reis` across all rows equals the stated balance
   (col B of `off chain asset balance` is a **stored** value the processor increments — it is
   **not** a `SUMIFS` formula, so it will not self-heal if a row is added out of band).

---

## 4. Why the order matters — the failure mode this avoids

If the expense lands **before** the conversion is `PROCESSED`, the BRL balance goes negative
for as long as the gap persists. That is not merely cosmetic:

- `treasury-cache-publisher` **silently drops negative balances** at three separate guards
  (`treasury-cache/gas/treasury-cache-publisher/Code.gs` L208 / L269 / L332).
- Consequence: the DApp holdings page shows **no BRL row at all**, so a correctly-booked
  expense looks entirely unbacked to anyone reading the holdings view.

The conversion must therefore be *seen to land* before the expense is submitted.

---

## 5. Duplicate discipline

`report_dao_expenses` **is not idempotent across a retry** — a `HTTP 200` +
`signature_verification: success` response does not mean the POST cannot be repeated. On
2026-11-05 a verification re-run double-posted a −R$5,027.70 expense (offchain rows 5356 /
5357, distinct `Request Transaction ID`s), driving Brazilian Reis to −4,897.70.

Therefore:

- **Never** re-execute a submit “just to check”. Verify by **reading the sheet**, not by
  resubmitting.
- After the gate, scan for rows matching (entity, amount, currency, description) before
  submitting Leg 2.
- If a duplicate does slip through, the correction is **append-only**: one unsigned
  `[SANCTIONED ONE-OFF CORRECTION]` reversal row, **never** a row edit or delete
  (`OPERATING_INSTRUCTIONS.md` §9c.4b / §9c.4c — signed rows bind their signature and
  scoring hash to content; editing or deleting forges the attestation).

> The underlying gap is already filed in `OPEN_FOLLOWUPS.md` — “`report_dao_expenses` is not
> idempotent across a retry”. Do not re-file it; add instances there if it recurs.

---

## 6. `BRL` vs `Brazilian Reis` — do not confuse the buckets

**Both currencies exist** on this ledger and are not interchangeable at the typing level.
Use the literal string **`Brazilian Reis`**. `BRL` is a separate bucket (rows 4881–4884 record
a 1:1 `BRL ⇄ Brazilian Reis` normalisation pair, and a negative `BRL` line exists in another
ledger). Typing `BRL` lands the expense in the wrong bucket: the row posts, the hash footer
looks valid, and the **`Brazilian Reis` balance does not move**.

---

## 7. Standing risks — ranked

| # | Gap | Status |
|---|---|---|
| **0** | This runbook (docs only). | ✅ This document |
| **1** | No `--idempotency-key` on `report_dao_expenses`; a retry double-posts. | Filed in `OPEN_FOLLOWUPS.md` |
| **2** | No `--reverse-of <row>` — a correction needs a reversal row **plus** a hand-sync of the balance column, which is itself a footgun. | Not filed |
| **3** | No `BRL → Brazilian Reis` alias/normalisation on input. | Not filed |
| **4** | Monthly manual conversion. Keeping a standing **BRL float** (~R$2,000) would eliminate most conversions and all negative-balance windows, at the cost of parked capital carrying BRL FX exposure. | Governor decision |

Items 2 and 3 are the two cheapest code-level wins: `--reverse-of` removes the hand-sync step,
and the alias removes the wrong-bucket trap permanently.

---

## 8. Worked example — 2026-11 payment (Sept + Oct)

| Doc | Amount | Service month | Due |
|---|---|---|---|
| Recibo 1 | R$ 500,00 | September 2026 | 15.10.2026 |
| Recibo 2 | R$ 500,00 | October 2026 | 15.11.2026 |
| **Pix** | **R$ 1,000,00** | paid 12/11/2026 08:16 | Pix ID `E689008102026111211167d4YZBTFAm`, ref `579736505` |

**Actual ledger shape (verified live 2026-11-12 — this is not hypothetical):**

| Step | Rows | Effect on `Brazilian Reis` |
|---|---|---|
| Leg 1 conversion | offchain **5384 / 5385** | +2,085.00 → balance **2215.00** |
| CRF Anapu 217-tree payout | **NOT BOOKED** | (−1,085.00) owed |
| Leg 2 Sept recibo | pending | −500.00 |
| Leg 2 Oct recibo | pending | −500.00 |
| **Closing** | | **130.00** |

The conversion was **not** R$1,000 for the accountant alone. Rows 5384/5385 record
**USD 378.05 → R$ 2,085.00** on `20261112`, blended rate 5.5151 (Wise fee USD 4.67; bank leg
USD 373.38 @ 5.5840), with a memo stating it funds the **217-tree CRF Anapu payout of
R$1,085.00** and that *"unspent residual of R$ 1,000.00 remains in the Brazilian Reis
balance"* — i.e. **one conversion funded two separate obligations**.

### ⚠️ The R$1,085.00 CRF Anapu payout is NOT on the ledger

Searched every Brazilian Reis row for the amount and for the Pix E2E
`E68900810202611121118xTBTdiHgQD7`: **zero hits.** It exists only as prose inside the
conversion memo. Balance row 25 reads **2215.00**, and the sum of all **74** Brazilian Reis
rows is **2215.00** (delta `0E-8`) — so the balance is internally consistent but **overstated
by R$1,085.00 against real cash**.

Booking only the accountant fee therefore leaves the balance at **1215.00** while the actual
account holds roughly **zero**. The payout needs its own evidence and its own expense row
before the account reads true. **Do not treat the account as reconciled until it is booked.**

**Generalised lesson for future months:** the closing assertion (“balance returns to opening”)
must cover **every** disbursement the conversion memo refers to — not just the one being
booked. Read the memo as an obligation list, not a single-purpose note.

**Attachment path trap hit in practice (2026-11-12).** These files live in the directory of the
**adapter that received them**. This session was **Discord**, so the three attachments were in
`/tmp/discord_attachments/` — *not* `/tmp/tg_attachments/`, where a Telegram upload would land.
Passing the `tg_` path to `--attachment` fails silently with a file-not-found. Check the real
path (`find /tmp -name '<hash>*'`) before every submit.

**Anomalies to note on the documents** (not blockers): both recibos carry the identical footer
date *“10 de Outubro de 2026”*, so the October invoice is signed before the month it bills —
likely a templated footer, but the Brazilian tax accountant may want it redated. And the Pix
payer is **Zhiwen Teh personally**, not TRUESIGHT DAO LLC and not the BR entity — if the cost
should sit on the BR entity's books, book it as an intercompany advance rather than a direct
expense, and say so in the description.
