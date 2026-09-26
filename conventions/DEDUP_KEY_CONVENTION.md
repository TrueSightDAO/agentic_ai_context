# Dedup / Identity-Key Convention — key on `Request Transaction ID`, never the transport id

**Status: STANDING convention (governor directive — Gary, 2026-09-26, thread 35944).**

> **Amended 2026-09-26 (§2.1/§2.5/§2.6; Gary, thread 35944):** a digital signature is
> *public by construction*, so the raw `Request Transaction ID` **may** be published in public
> JSON caches / public ledger columns — it is what makes a submission verifiable. Only raw
> **PII** (PIX/CPF/email/phone) is barred from public payloads.

When you design a new ledger / tracking tab (the "contract" between a signed DAO event and a
sheet or table), or when you fix deduplication in an existing one, follow this rule:

> **The dedup key is the signed `Request Transaction ID`.** The *transport id*
> (`telegram_update_id`, the Telegram **message id**, the Telegram **file id**, an HTTP
> request id, a queue offset, …) is **not** a valid dedup key — it is **observability only**.
> Every tab that ingests signed events MUST carry a **dedicated column** holding the
> `Request Transaction ID`, so that dedup is a single-column scan.

Audience: any AI agent or developer writing a scanner, a provisioner, a ledger writer, or
adding a column to a tracking tab.

---

## 1. Why (the failure this prevents)

Keying on the transport id is wrong for three independent reasons:

1. **The transport id changes on re-post.** The *same* tree (or sale, or movement) re-sent
   through Telegram arrives under a **new** `telegram_update_id` / message id. An update-id
   key sees a second event and **double-counts** it. (Observed: 15 live CFR cases.)
2. **One transport id maps many → one.** A single Telegram message can legitimately produce
   **multiple rows** — several photos, several trees, several line items — all sharing one
   update id. An update-id key therefore **cannot** distinguish "a second photo of tree 1"
   from "tree 2".
3. **The transaction id is the unit the ledger actually cares about.** `Request Transaction ID`
   is an RSA signature over the submitted payload: it is stable across re-post, unique per
   signed request, and is the identity the DAO already treats as authoritative. (Verified over
   the CFR `tree planting` tab: **265 rows → 172 distinct txids**, none appearing under more
   than one signer or more than one tree content — so the txid *alone* is the unique key.)

---

## 2. The rule

1. **Dedup key = `Request Transaction ID`.** Scope the key on the txid. Do **not** add a
   `pk_hash` scope unless there is evidence a txid is reused across signers (there is not, as
   of 2026-09-26). The txid **is** the signature over the submitted payload and is **public by
   design** (§2.6) — it is *not* the signer's identity, which is represented separately and
   only as the one-way `pk_hash`.
2. **A dedicated column is mandatory.** Every ingest tab MUST have its own column holding the
   txid. Do not bury it inside a free-text "notes" / "source" blob, and do not re-derive it by
   re-parsing a payload at read time when a column can hold it.
3. **The transport id is demoted, never deleted.** Keep it as a non-key column for
   observability / traceback, but it must not be the dedup key.
4. **Append trailing + migration-safe.** Add the new column at the **end** of the header row and
   never reorder existing columns; the provisioner must add the header to an existing tab
   **without** disturbing current data (`header`-aware, idempotent).
5. **Backfill once, idempotently, dry-run first.** Provide a one-shot `?action=…` lever that
   populates the txid on **existing** rows, with a `&dryRun=1` preview that returns **counts
   only**, and is re-runnable with no effect. The counts-only rule is about keeping the preview
   small and idempotent — **not** secrecy (the txid is public, §2.6). Never emit PII in a preview.
6. **Raw signatures are public; raw PII never is.** A digital signature is *public by
   construction* — verifiable with the signer's public key and revealing nothing about the
   signer. Publishing the `Request Transaction ID` (which **is** the signature over the
   submitted payload) in a public JSON cache or a public ledger column is therefore
   **allowed and encouraged**: it is exactly what makes a submission independently verifiable,
   the point of the TrueChain audit trail. Do **not** hash, truncate, or otherwise degrade it
   "for privacy" — a stable, globally-unique join key is a feature here. What must **never**
   appear in a public payload is raw **PII** (PIX/CPF/email/phone), and the signer's identity
   beyond its one-way `pk_hash`; keep masking those exactly as before.

---

## 3. Parsing the txid from a signed payload

Extract it from the rendered submission text (generic over field name / whitespace):

```js
// The signed block ends with:  My Digital Signature: <b64>  then  Request Transaction ID: <b64>
var m = String(body || '').match(/Request Transaction ID:\s*([^\n]+)/i);
var requestTransactionId = m ? m[1].trim() : '';
```

Do not match on surrounding prose ("generated using …", "Verify submission here …") — those
vary by generator.

---

## 4. Caveats — when the txid alone is not sufficient

`Request Transaction ID` is signed over the payload **including timestamps** (e.g.
`Planting Time`). Therefore:

- A **re-post of the identical signed text** ⇒ **same** txid ⇒ correctly deduped. ✅
- A **re-submission that re-signs** (fresh timestamp) ⇒ **different** txid ⇒ the txid key will
  *not* catch it (and neither would the old message-id key).

When the risk you are defending against is *re-signing* rather than *re-posting*, pair the txid
with a **content fingerprint** (e.g. `lat|lng|species|photo_url`) and treat the fingerprint as a
secondary collapser. Decide explicitly which of the two you are guarding; document the choice in
the tab's own doc.

---

## 5. Worked examples

- **CFR `tree planting` tab (canonical, shipped).** tokenomics **#564** (`3b2ccb18`) adds a
  trailing `request_transaction_id` column + migration-safe `ensurePayoutRegTab_` + idempotent
  `?action=backfillCfrTreeTxIds`; **#566/#567** add row-collapse (`collapseCfrTreeTxDuplicates`,
  keep-first, preview-by-default `?apply=1`, counts-only).
- **SunMint `SunMint Tree Planting` tab (pending).** Currently dedupes on col **D**
  (Telegram Message ID) + col **H** (File ID) — the exact anti-pattern this convention bans.
  Needs `request_transaction_id` as **col V** (col U is reserved for the approved
  Submission-Source work). Tracked in `OPEN_FOLLOWUPS.md` → Pending.

---

## 6. Enforcement

- A new tab that omits the txid column, or a dedup that keys on a transport id, is a
  **convention violation** — send the PR back.
- GAS scanners adding/touching such tabs must still satisfy `tokenomics/AGENTS.md`
  (`doGet ?action=` exposure + in-run idempotent installer + router-registry entry).
- Related: `LEDGER_CONVERSION_AND_REPACKAGING.md`, `tokenomics/AGENTS.md`,
  `conventions/QA_LIVE_LEDGER_TEST_PROCEDURE.md`.
