# SOP — Payout Report Format (pre-payout PDF)

> **Applies to:** any farmer payout (e.g. CFR Anapu tree planting, PIX/BRL) where a PDF
> schedule is produced to accompany the transfer. **This PDF is required BEFORE the
> payout is processed**, so the payer and any reviewer can see exactly who is paid, how
> much, under which PIX key, and *which items* the payment covers.
>
> Filed 2026-10-15 after the CFR Anapu payout PDF (86 trees × R$5 = R$430, one PIX key).
> Governor: Gary. Author: Sophia Truesight.

## 1. Why this format

A payout schedule that lists only opaque ids is not reviewable: the payee and reviewers
must be able to **click through and see the tree (item) being paid for**. This SOP fixes the
structure so every future payout PDF is consistent and verifiable before money moves.

## 2. Required sections (in order)

### 2.1 Summary block
| Field | Meaning |
|---|---|
| Total to transfer | `count × unit_price`, e.g. **R$ 430.00** |
| Items to settle | count + unit price (e.g. `86 at R$5.00 each`) |
| PIX accounts | number of distinct pay-to keys |
| Excluded (duplicates) | count of dropped duplicate captures |
| Status | **NOT PAID — held for governor go** / PAID (date) |

### 2.2 One section per PIX key (grouped)
For each distinct PIX key:
- **Pay-to PIX key** (e.g. CPF `000.000.000-00`) and holder pk (e.g. `pk-…`)
- **Amount** = trees under this key × unit price
- **Tree count** under this key

*(If every item resolves to a single PIX key, this is one block; if several, one block each.)*

### 2.3 Per-item table (one row per payable tree/item)

| # | Tree ID | TxID | See tree (CLICKABLE) | Amount |
|---|---|---|---|---|
| 1 | `Edgar_20261012112915_239` | `<request_txid prefix>` | [view tree](LINK) | R$ 5.00 |

- **Tree ID** = the signed **TREE PLANTING** event's request reference; it equals the
event's `telegram_message_id` (the verified join key into public feeds).
- **TxID** = the `request_transaction_id` (the signed blob). A short prefix is fine; the
full blob is base64 and unreadable in a table.
- **See tree** = a **real clickable link** (see §3).

### 2.4 Excluded section
List every dropped row (duplicate capture) with the reason. Never silently omit.

### 2.5 Footer
Define Tree ID / TxID semantics + the link target template.

## 3. Link rules (the "see the item" link)

- **Primary (GPS-located trees):** `https://cfr.truesight.me/my-trees/?tree=<tree_id>`
  `?tree=` is the page's canonical single-item deep link (scrolls to + expands that card).
  `sunmint.truesight.me/my-trees/` is **404** — use **cfr**.
- **Universal fallback (ALSO works for pseudo trees):**
  `https://beta.truesight.me/ledger/explorer/?q=<tree_id>`
  The Ledger Explorer reads `verify_public_signatures/ledger_index.json`, which is keyed on
  `tree_id` (= planting event `telegram_message_id`) **independent of GPS** — so it resolves
  **every** tree, including coordinate-less pseudo trees.
- **Pseudo trees** (blank lat/lng) do **NOT** appear in `sunmint/trees/index.geojson` (a map
  layer — every feature needs a Point geometry), so their `my-trees?tree=` link shows
  *"not found"* until GPS is assigned. Mark those rows and link them via the **fallback**
  (or note "not yet in live index").

## 4. Tooling note — links MUST be real annotations

- `generate_pdf` renders markdown `[text](url)` as **literal dead text** — its output has
  **no `/Annots`, no `/Link`, no `/URI`** (verified 2026-10-15). Do **not** use it when the
  report needs clickable links.
- Use **reportlab** directly: a `Paragraph` containing `<a href="…">…</a>` produces genuine
  **link annotations**.
- **Verify before sending:** scan the PDF bytes and assert `/Annots`, `/Link`, `/URI` are
  present and the expected count of link URIs is embedded.

## 5. Integrity rules

- **Compute, don't assert.** Derive counts/amounts from the source, never from a claim.
- **Dedupe with TWO independent keys** (e.g. file MD5 **and** the Timemark verification code);
  require both to land on the same keep/drop split before paying.
- **Hold for explicit governor go** — this PDF is the *instruction*, not the authorization.
  Never fire the transfer on the strength of the document alone.

## 6. Pre-payout checklist

- [ ] Total = count × unit price, recomputed from source
- [ ] Grouped by PIX key; every pay-to key listed with its amount
- [ ] One row per payable item, each with Tree ID + TxID + **clickable** link
- [ ] Links verified clickable (`/Annots`/`/URI`) and resolvable
- [ ] Pseudo/not-indexed rows flagged + fallback link applied
- [ ] Excluded duplicates listed with reason
- [ ] STATUS = NOT PAID until governor explicitly says go
