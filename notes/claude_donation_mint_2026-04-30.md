# Donation Mint Pattern — `[DONATION MINT EVENT]`

**Date:** 2026-04-30
**Agent:** Claude
**Trial run:** 5 × $5 SunMint Tree Planting Pledges from Will's $25 Venmo donation
(`will.chen85@gmail.com`). All 5 minted successfully end-to-end on rows 1448-1452
of `Agroverse QR codes` with corresponding `+1 Pledge` rows on `offchain
transactions` (rows 3143-3147).

---

## The Pattern

When a DAO governor accepts a cash donation earmarked for SunMint Tree Planting
(currently the only allowed donation currency), they mint a **serialized QR-coded
Pledge** as a tradeable receipt for the donor. Pledges sit on AGL4's offchain
ledger as a +1 inventory unit until the donor "buys" them via a separate
`[SALES EVENT]` (which lands the cash on AGL4 via the existing sales pipeline).

Architecturally this is **two events**, not one:

1. **`[DONATION MINT EVENT]`** — governor only, requires visual proof, leaves the
   QR at `MINTED`.
2. **`[SALES EVENT]`** (existing module, no special handling) — flips MINTED→SOLD,
   lands the $X cash on AGL4 via `process_sales_telegram_logs.gs` →
   `sales_update_main_dao_offchain_ledger.gs`.

Two events are intentional: it audits "minted but not sold" cleanly (e.g. a
governor who minted but never collected the cash), and the second event reuses
the sales pipeline for free.

---

## CLI

```bash
cd ~/Applications/dao_client
source .venv/bin/activate

python -m truesight_dao_client.modules.mint_donation \
  --donation-amount 25 \
  --donor-name "Will" \
  --donor-email will@example.com \
  --proof-file ~/Downloads/wills_donation_venmo_screenshot.PNG
# Prints: Minted QR Code: PLEDGE_20260430_a1b2c3d4

python -m truesight_dao_client.modules.report_sales \
  --item PLEDGE_20260430_a1b2c3d4 \
  --sales-price 25 \
  --sold-by "Gary Teh" --cash-proceeds-collected-by "Gary Teh" \
  --owner-email will@example.com \
  --stripe-session-id "(none)" --shipping-provider N/A --tracking-number N/A
```

The QR id is **client-generated** (`PLEDGE_<YYYYMMDD>_<8hex>`) so the operator can
fire `report_sales` immediately, no polling.

---

## Three server-side gates (GAS — `process_donation_mint_telegram_logs.gs`)

| Gate | Source of truth | Failure status |
|---|---|---|
| Currency allowlist | Hardcoded array `DONATION_MINT_ALLOWED_CURRENCIES` (V1 = single entry) | `REJECTED_INVALID_CURRENCY` |
| Signer is governor | Pattern A — GAS reads the `Governors` tab on the Main Ledger workbook | `REJECTED_NOT_GOVERNOR` |
| Visual proof URL | Regex `^https?://(www\.)?github\.com/TrueSightDAO/` | `REJECTED_NO_VISUAL_PROOF` / `REJECTED_INVALID_PROOF_URL` |
| (defensive) QR collision | `Agroverse QR codes` col A | `REJECTED_QR_CODE_COLLISION` |

All rejections write a row to the **`Donation Pledge`** dedup tab (gid 519599408
on the Telegram compilation workbook, sibling to Telegram Chat Logs). No
`Agroverse QR codes` row is created for rejections.

---

## Server-locked fields (NOT trusted from client)

| Field | Source |
|---|---|
| `Agroverse QR codes` col B `landing_page` | `Currencies` col E |
| `Agroverse QR codes` col C `ledger` | `Currencies` col F |
| `Agroverse QR codes` col U `Manager Name` | Validated governor display name |
| `Agroverse QR codes` col V `Ledger Name` | Parsed `agl<N>` segment from `Currencies` col F URL → uppercased |

Even an authorized governor cannot misroute funds by spoofing these in the
event payload. Single source of truth: `Currencies` tab row 119
(`SunMint Tree Planting Pledge - QR Code` — set `Serializable=TRUE`,
`landing_page=https://agroverse.shop/sunmint-pledge`,
`ledger=https://www.agroverse.shop/agl4`).

---

## Visual proof — file flows through Edgar, NOT directly to GitHub

**Wrong (what tripped on the first iteration):** dao_client uploads photo to
TrueSightDAO/.github via the Contents API, then passes the URL.

**Right:** dao_client sends the file **bytes** via multipart `attachment` field.
Edgar parses `Destination Contribution File Location:` from the signed text and
uploads the bytes via Contents API using `config.github_pat`. Mirrors how
`report_contribution.html` / `[CONTRIBUTION EVENT]` already work.

The CLI auto-computes the destination URL prefixed with the QR id so multi-mint
sessions sharing one source image don't collide:
`github.com/TrueSightDAO/.github/blob/main/assets/donations/PLEDGE_<id>_<basename>`.

---

## Audit trail (closed integrity loop)

For every successful mint the GAS handler writes **three** rows:

1. **`Agroverse QR codes`** — the canonical QR row (status=MINTED until sold).
2. **`Donation Pledge`** dedup tab — Telegram Update ID-keyed audit row with
   donor / amount / governor / proof URL / cross-references.
3. **`offchain transactions`** — `+1 SunMint Tree Planting Pledge - QR Code`
   row, fund handler = governor, **description includes the proof URL**:
   `[DONATION MINT] PLEDGE_<id> — donor: <name> (donation: $X) — proof: <url>`.

The proof URL embedded in (3) closes the integrity loop: an auditor scanning the
offchain ledger can trace any +1 Pledge entry back to the photo of the cash
receipt that funded it without leaving the spreadsheet.

---

## Triggering the scanner

- **Edgar webhook** (primary) — `dao_controller.rb#trigger_immediate_processing`
  fires `?action=processDonationMintsFromTelegramChatLogs` against the
  `agroverse_qr_codes` Apps Script project (script `1slQVojn…`,
  deployment URL `AKfycbySJ86OcVsk5gETTiJ-…`) on every `[DONATION MINT EVENT]`
  submission.
- **Hourly safety-net cron** — self-installs on first scanner invocation via
  `ScriptApp.newTrigger.timeBased.everyHours(1)`. Catches anything the webhook
  missed (Edgar offline / sentiment_importer restart / etc).

---

## Open follow-up

- **DApp page for governor-driven donation recording** — browser equivalent of
  `mint_donation.py`. Mirror `report_contribution.html` shape (form + photo
  upload). Filed in OPEN_FOLLOWUPS.

## PRs landed

| Repo | PR | What |
|---|---|---|
| `tokenomics` | #260 | Initial GAS scanner |
| `tokenomics` | #261 | Server-lock Ledger Name + offchain ledger write |
| `tokenomics` | #262 | Rename dedup tab → `Donation Pledge` |
| `tokenomics` | #263 | QR collision check |
| `tokenomics` | #264 | Self-contained Currencies lookup + doGet route |
| `tokenomics` | #265 | Hourly cron self-installer |
| `sentiment_importer` | #1044 | Edgar `[DONATION MINT EVENT]` dispatch branch |
| `dao_client` | #17 | Initial `mint_donation.py` |
| `dao_client` | #18 | Drop client-side `--ledger-name` |
| `dao_client` | #19 | File upload via Edgar (architecture fix) |
| `agroverse_shop_beta` | #89 | `/sunmint-pledge` donor receipt page |
