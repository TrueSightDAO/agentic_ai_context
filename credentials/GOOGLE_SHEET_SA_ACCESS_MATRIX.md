# Google Sheet → Service-Account Access Matrix (canonical)

**Purpose.** Answer, in one place: *which service account (SA) can write to which
Google Sheet tab?* This exists because the answer was scattered across
`GOOGLE_API_CREDENTIALS.md`, `GOVERNOR_SHEET_PERMISSION_SYNC_SOP.md`,
`AUTOPILOT_GOOGLE_ACCESS_PLAN.md`, and per-project code — and sessions kept
guessing (see **§5 History**).

**How this was built:** every SA key on the autopilot box was probed against every
tab of the Main Ledger with a **read-only write test** (write an empty string to
the bottom grid row, read back, leave nothing). Results below are observed
behaviour, not documentation paraphrase. **Re-run the script in §4 to refresh.**

**Last probed:** 2026-09-19 (Main Ledger + Cypher Defense Ledger). SunMint sheet probed 2026-09-24 (§2b).

---

## 1. Legend

| Symbol | Meaning |
|---|---|
| ✅ **W** | SA can **write** to that tab |
| 🔒 **PROT** | Tab is **owner-protected** — *no* service account can write; only the sheet owner (or a human granted via the protected-range editor list) can |
| 👁 **read** | SA can read but **not** write (viewer-only) |
| — | SA not applicable / not present |

> **Rule of thumb:** protection is decided by the *owner*, not by anything the SA
> can self-serve. If a tab shows 🔒, the fix is a **human** editing the sheet
> protection — do **not** hunt for a different SA and do **not** report a
> credential problem.

---

## 2. Main Ledger — `1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`

| Tab | qr-code-mgr | ledger-mgr | cypher-defense | edgar-dapp-listener | tdg-scoring | market-research | upc-barcode |
|---|---|---|---|---|---|---|---|
| Ledger history | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Contributors voting weight | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Outstanding Airdrops | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| **Contributors contact information** | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| **Contributors Digital Signatures** | 🔒 | 🔒 | 🔒 | ✅ | 👁 | 🔒 | 👁 |
| offchain transactions | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| offchain asset location | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| off chain asset balance | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Recurring Transactions | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Consignments | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Contribution submission | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Governors | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Intiatives Scoring Rubric | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| TRUESIGHT token details | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| DAO Partners | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Agroverse Active Contributors | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| **States** | 🔒 | 🔒 | 🔒 | ✅ | 👁 | 🔒 | 👁 |
| Currencies | ✅ | ✅ | 🔒 | 🔒 | 👁 | ✅ | 👁 |
| Contributor Staking | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Recent Contributions - 180 | 🔒 | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Commodity Prices Exchange Rate | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Agroverse Price Components | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Agroverse Cacao Category Pricing | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| **Agroverse Cacao Processing Cost** | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Agroverse QR codes | ✅ | 🔒 | ✅ | ✅ | 👁 | ✅ | 👁 |
| Stripe Social Media Checkout ID | ✅ | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Shipment Ledger Listing | ✅ | 🔒 | 🔒 | 🔒 | 👁 | ✅ | 👁 |
| Agroverse SKUs | ✅ | 🔒 | 🔒 | 🔒 | 👁 | ✅ | 👁 |
| Agroverse News Letter Subscribers | ✅ | 🔒 | 🔒 | 🔒 | 👁 | ✅ | 👁 |
| Agroverse News Letter Emails | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Performance Statistics | ✅ | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Monthly Statistics | ✅ | 🔒 | 🔒 | 🔒 | 👁 | 🔒 | 👁 |
| Partner Check-ins | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| Subscription Fulfillment Queue | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| shipment_nfe | ✅ | ✅ | ✅ | ✅ | 👁 | ✅ | 👁 |
| **offchain assets in transit** | 🔒 | ✅ | 🔒 | 🔒 | 👁 | 🔒 | 👁 |

**Column keys** (SA email → key file on the autopilot box):

| Column | Service account | Key file |
|---|---|---|
| qr-code-mgr | `agroverse-qr-code-manager@get-data-io.iam.gserviceaccount.com` | `/opt/truesight_autopilot/config/google/agroverse_qr_code_manager_gdrive_key.json` |
| ledger-mgr | `agroverse-ledger-manager@get-data-io.iam.gserviceaccount.com` | `~/creds/agroverse-ledger-manager-google-credentials.json` |
| cypher-defense | `cypher-defense@get-data-io.iam.gserviceaccount.com` | `/opt/truesight_autopilot/config/google/cypher_defense_gdrive_key.json` |
| edgar-dapp-listener | `edgar-dapp-listener@get-data-io.iam.gserviceaccount.com` | `/opt/truesight_autopilot/config/google/edgar_dapp_listener_key.json` |
| tdg-scoring | `tdg-scoring-peer-reviewer@get-data-io.iam.gserviceaccount.com` | `/opt/truesight_autopilot/config/google/tdg_scoring_gdrive_key.json` |
| market-research | `agroverse-market-research@get-data-io.iam.gserviceaccount.com` | `~/creds/google_credentials.json` |
| upc-barcode | `upc-barcode@get-data-io.iam.gserviceaccount.com` | `/opt/truesight_autopilot/config/google/upc_barcode_gdrive_key.json` |
| sunmint-ledger-mgr | `sunmint-ledger-manager@get-data-io.iam.gserviceaccount.com` | `/opt/truesight_autopilot/config/google/sunmint_ledger_manager_gdrive_key.json` |

---

## 2b. SunMint sheet — `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`

Title: **TrueSight DAO Telegram compilation**. This sheet carries the SunMint
source tabs (tree planting, plots, farms, planting links, growth measurements) and
is the daily input to the three `sunmint` repo index-rebuild workflows. Its sharing
list is **separate from the Main Ledger's** — a Main-Ledger SA is *not*
guaranteed read here.

| Tab | sunmint-ledger-mgr |
|---|---|
| SunMint Tree Planting | ✅ **W** |
| SunMint Plots | ✅ **W** |
| SunMint Registered Farms | ✅ **W** |
| Tree Planting Link | ✅ **W** |
| Tree Growth Measurements | ✅ **W** |
| Telegram Chat Logs | ✅ **W** |

**Probed 2026-09-24** by reading every tab and writing an empty string to the bottom
of the grid, then reading back (nothing left behind). The SA has **Editor** on the
whole sheet — no 🔒 tabs observed.

**Note (2026-09-24).** This SA was created *because* the previous CI SA's access to
this sheet was revoked around 2026-09-18, silently freezing all three published
SunMint indexes for 7 days (see `OPEN_FOLLOWUPS.md` → SunMint index freeze entry).
**Any CI job that reads this sheet should use `sunmint-ledger-manager`, and a
rotation must update the `sunmint` repo secret `GOOGLE_SERVICE_ACCOUNT_JSON` too.**

---

## 3. Which SA for what — quick rules

1. **Contributors contact information** (partner/farmer contact rows) →
   **`agroverse-ledger-manager`** (broadest writer). `edgar-dapp-listener`,
   `cypher-defense`, `agroverse-qr-code-manager`, `agroverse-market-research`
   also work here.
2. **Contributors Digital Signatures** → **`edgar-dapp-listener` only.**
3. **States** → **`edgar-dapp-listener` only.**
4. **offchain assets in transit** → **`agroverse-ledger-manager` only.**
5. **Agroverse QR codes** → `agroverse-qr-code-manager`,
   `cypher-defense`, `edgar-dapp-listener`, or `agroverse-market-research`.
   **Not** `agroverse-ledger-manager`.
6. **Shipment Ledger Listing / Agroverse SKUs / Newsletter Subscribers / Stats** →
   `agroverse-qr-code-manager` or `agroverse-market-research`.
7. **Any 🔒 tab** → stop. A **human** must lift the protection. Report it as a
   *sheet-permission* ask, never as a credentials fault.
8. **`upc-barcode` / `tdg-scoring-peer-reviewer`** are **read-only** on the Main
   Ledger — never use them for a write.
9. **SunMint sheet (§2b) — anything tree/plot/farm related** →
   **`sunmint-ledger-manager`**. It is the canonical SA for SunMint sheets and the
   one wired into the `sunmint` repo's index-rebuild workflows. A Main-Ledger SA may
   or may not read this sheet; don't rely on it.

### Default choice
When you genuinely don't know and the tab shows ✅ for it: **use
`agroverse-ledger-manager` on the Main Ledger** — it is the widest writer, and
covers the tab that prompted the last incident.

---

## 4. Refresh script (re-probe and regenerate)

See `scripts/probe_sheet_sa_access.py` in this repo — it walks every SA key and
every tab, performs the empty-write probe, and prints the matrix. Re-run it after
any permission change, a governor rotation (see
`GOOGLE_API_CREDENTIALS.md` → Governor Sheet Permission Sync SOP), or when a new
SA is added. Cheap, read-only-in-effect, safe to run any time.

---

## 5. History

- **2026-09-24** — Added §2b (SunMint sheet) + the `sunmint-ledger-manager` SA.
  A CI credential's sheet access was revoked ~2026-09-18; the three `sunmint`
  index-rebuild workflows went stale for 7 days (one failing loudly, two reporting
  false-green). The replacement SA is documented here so the sharing list is no
  longer tribal knowledge.
- **2026-09-19** — Matrix created. Motivated by a session that probed the
  `Contributors contact information` tab with a *missing* key file
  (`FileNotFoundError`), then mis-read the subsequent protected-range metadata as
  "no service account can ever write this" and escalated a non-existent blocker.
  Governor corrected it; `agroverse-ledger-manager` writes the tab fine. Root
  cause: no per-tab SA mapping existed, so the session reasoned from prose instead
  of testing.
- **Lesson encoded above:** "a `FileNotFoundError` on a credential is a *path*
  bug, not an access verdict — and protection metadata is not a write test."
