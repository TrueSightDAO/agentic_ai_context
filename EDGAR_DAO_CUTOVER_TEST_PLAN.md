# Edgar → `dao_protocol` — cutover test plan (checklist)

Companion to **`EDGAR_DAO_EXTRACTION_PLAN.md`** — part of the execution roadmap checklist. Run a
route's block **before ramping that route's gate**; don't open any traffic % until its block is green.

**Legend:** `[x]` ✅ passed (this session) · `[ ]` ⬜ pending (endpoint not built yet) · 🧑 **MANUAL**
(needs operator) · ⚠️ finding/decision needed.

**Test surfaces:**
- Python (impl, gate off): `https://edgar.truesight.me/dao-protocol/<path>` (test prefix)
- Rails (current live): `https://edgar.truesight.me/<path>`

---

## PR2 — `/proxy/gas/:name`  · IMPL DONE (dao_protocol#34) · ✅ RAMPED LIVE 2026-05-25

**Ramp DONE (option A chosen):** `location /proxy/gas/` added to `seni_ror_new:edgar.conf` →
`proxy_pass http://127.0.0.1:8010` (path preserved). Real `https://edgar.truesight.me/proxy/gas/*`
now served by the Python service. Verified: `GET /proxy/gas/qrCodes` → **200** (GAS JSON; was 401),
unknown → 404, `/ping` (Rails) → 200. Backup refreshed (sentiment_importer#1059). The 401 finding
below is now **RESOLVED** by the ramp.

**Functional — Python forwards to each allowlisted GAS (run 2026-05-25, all ✅):**
- [x] `assetVerify` → 200, upstream `{"error":"Signature parameter missing"}`
- [x] `qrCodes` → 200, upstream `Missing required parameters: qr_code and email_address`
- [x] `stores` → 200, upstream `Invalid parameters (lat/lng…)`
- [x] `storesHitList` → 200, upstream GAS HTML
- [x] `shipping` → 200, upstream `Invalid or missing action parameter`
- [x] `proposals` → 200, upstream `Invalid mode`
- [x] `OPTIONS` preflight → 200 + `Access-Control-Allow-Origin: *`
- [x] unknown name → 404 `{"error":"unknown gas endpoint: …"}`
- [x] 5 mocked unit tests (GET raw-query, POST body+content-type, 502, OPTIONS, 404) pass

**Not run / manual:**
- [x] ✅ Live WRITE-GAS POST path — `POST /proxy/gas/feedback` (invalid/benign body) forwarded
  through Python to GAS and returned GAS's response (a Google auth/redirect HTML for the bad
  payload). Confirms POST forwarding works end-to-end; no record created.

**✅ RESOLVED FINDING (ramped to Python, option A) — Rails `/proxy/gas` was returning 401:**
Live Rails `/proxy/gas/*` returned **401 for every name + OPTIONS** (while `/ping` is 200). Root
cause: `proxy_controller.rb` does `skip_before_action :require_login, raise: false`, but
`require_login` is **not** a registered `before_action` — so the skip is a no-op. A *different*
global filter (prime suspect **`rate_limit_bot_calls`**) 401s the unauthenticated/bot-like proxy
calls. So the proxy's intended unauth'd access is **broken in production today** — latent, because
the DApp's GFW client-flip isn't wired yet, so nothing live calls it. The **Python port behaves as
intended** (no such filters). **Cutover implication:** there is no "parity" to preserve here —
ramping `/proxy/gas` to Python *fixes* a currently-401 endpoint. *Operator decision:* either (a)
ramp `/proxy/gas` → Python (recommended; it's the working impl), or (b) fix Rails first
(`skip_before_action :rate_limit_bot_calls` on `proxy#gas`) if you want Rails to stay primary.

---

## PR3 — newsletter + email-agent tracking pixels  · IMPL DONE (dao_protocol#35) · ramp pending
Verified via the test prefix 2026-05-25 (bogus ids → redirect only, no sheet write):
- [x] `/newsletter/open.gif` → 302 → logo
- [x] `/newsletter/click` → 302 → decoded `to` URL (b64url); bad/missing/`javascript:` → fallback `agroverse.shop`
- [x] `/email_agent/open.gif` → 302 → logo
- [x] `/email_agent/click` → 302 → decoded target
- [x] 7 mocked unit tests (redirects, b64 decode, safe-redirect, recipient guard, sheet-error-never-breaks-redirect)
- [x] deployed — google libs present + Edgar SA key readable by the service (so real writes will work)
- [ ] 🧑 confirm a **real** open/click bumps the sheet counters (`Agroverse News Letter Emails` H–K / L–P; `Email Agent Drafts` N / O) — operator opens a real tracked email; automated tests avoid this to not pollute live stats

## PR4 — `/agroverse_shop/shipping_rates`  · IMPL DONE (dao_protocol#36) · ramp pending
- [x] valid address → EasyPost USPS rates JSON (live)
- [x] **EXACT PARITY vs Rails** (2026-05-25, "1 Infinite Loop" 8oz → GroundAdvantage $5.70 / Priority $8.26 / Express $31.11 — identical ids, amounts, deliveryDays on both)
- [x] 5 mocked unit tests
- [ ] 🧑 confirm agroverse_shop client GAS fallback still covers proxy errors (operator)
- _note: `deliveryDays` shows "3-7 business days" for all three — EasyPost's modern service names (GroundAdvantage/Priority/Express) don't match the estimate regexes → default. Pre-existing in **both** Rails and Python (faithful parity, not a regression)._

## PR4b — `/qr-code-check`  · PENDING IMPL
- [ ] ⬜ `SAMPLE`/`GIFT`/`SOLD` → landing redirect + UTM params
- [ ] ⬜ unknown qr → 404
- [ ] 🧑 a real `MINTED` scan → Stripe **test-mode** checkout → `?session_id=` reconcile → `SOLD` + QR Code Sales row (operator; touches Stripe + ledger)

## PR5 — `/dao/*` submit_contribution (per signed event)  · IMPL DONE (dao_protocol#37 verifier, #38 intake+dispatch) · gate off
- [x] RSA verify (valid + tampered + malformed) — `crypto/verify.py`, validated vs the **real** example payload (PR5a)
- [x] intake logic (no-signature/failed/success branches, dedup→409) + 17-branch dispatch routing — 28 mocked unit tests; route mounted (GET→405) via test prefix
- [ ] webhook URLs (`DAO_PROTOCOL_WEBHOOK_*`) provisioned in box `.env` — **at ramp** (server-side, like EasyPost key)
- [ ] EMAIL REGISTERED/VERIFICATION onboarding (`DaoEmailRegistrationService`) + attachment→GitHub upload — **deferred** (flagged), not yet ported
- live per-event tests below remain operator-driven (real ledger/GAS):

For **each** event type: valid signature → accept + correct ledger write; **tampered signature → reject**; correct dispatch.
- **Special-dispatch events** (fire `WebhookTriggerWorker` → GAS/GitHub): `ASSET RECEIPT`, `CONTRIBUTOR ADD`, `CREDENTIALING ATTESTATION`, `CURRENCY CONVERSION`, `DAPP PERMISSION CHANGE`, `DONATION MINT`, `EMAIL REGISTERED`, `EMAIL VERIFICATION`, `QR CODE UPDATE`, `REPACKAGING BATCH`, `RETAIL FIELD REPORT`, `SALES`, `STORE ADD`, `WARMUP SEND`.
- **Log-only events** (verify + append, no special dispatch): `CONTRIBUTION`, `CAPITAL INJECTION`, `DAO EXPENSES`, `INVENTORY MOVEMENT`, `TREE PLANTING`, proposal create/review, `WITHDRAW VOTING RIGHTS`.
- [ ] ⬜ signature verify (valid + tampered) — automatable via `dao_client` once `crypto/verify.py` lands
- [ ] ⬜ each log-only event → correct ledger row (compare Rails vs Python output for the same signed payload)
- [ ] 🧑 `EMAIL VERIFICATION` (loopback click must happen on the operator's machine — same-device constraint)
- [ ] 🧑 `DONATION MINT` / `SALES` (touch real ledgers) — dogfood with operator's own key via the `split` cohort
- [ ] 🧑 `DAPP PERMISSION CHANGE` (needs a governor signature)

## PR6 — Stripe cluster  · PENDING IMPL
- [ ] ⬜ `/meta_checkout` create session (no-payment path)
- [ ] 🧑 `/stripe_webhook` `checkout.session.completed` — fire a Stripe **test-mode** checkout (operator)
- [ ] 🧑 `qr-code-check` `MINTED` → pay (test card `4242…`) → `SOLD` + QR Code Sales (operator)

---

## Testing-execution policy (Gary, 2026-05-25)
- **Default: test on this local machine** — drive the Python service with `dao_client` + the operator's
  key against the `/dao-protocol/*` test prefix (or the ramped real path). Signature verify + log-only
  events + read endpoints can be tested here.
- **Operator runs the ledger-mutating ones.** There is no test ledger — any real signed financial event
  writes to the live Google Sheets. So **Gary executes (or supervises) events that mutate financial
  ledger state** — `DONATION MINT`, `SALES`, `INVENTORY MOVEMENT`, `CURRENCY CONVERSION`, real QR-code
  sales, Stripe checkouts — so they're legitimate intended entries, not test pollution. The agent does
  not fire those autonomously.

## Operator (🧑) summary — what needs you
1. ✅ **`/proxy/gas` 401 — DONE.** Ramped to Python (option A); the latent 401 is fixed.
2. ✅ **Live POST check — DONE** (`/proxy/gas/feedback` forwards through Python; no record created).
3. When PR5/PR6 land: per the policy above — dogfood non-mutating signed events + signature verify on
   the local machine; **you** run the ledger-mutating events (`DONATION MINT`/`SALES`/Stripe checkout),
   the `EMAIL VERIFICATION` loopback (same-device), and governor-signature events.
