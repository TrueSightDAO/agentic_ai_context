# Edgar → `dao_protocol` — cutover test plan (checklist)

Companion to **`EDGAR_DAO_EXTRACTION_PLAN.md`** — part of the execution roadmap checklist. Run a
route's block **before ramping that route's gate**; don't open any traffic % until its block is green.

**Legend:** `[x]` ✅ passed (this session) · `[ ]` ⬜ pending (endpoint not built yet) · 🧑 **MANUAL**
(needs operator) · ⚠️ finding/decision needed.

**Test surfaces:**
- Python (impl, gate off): `https://edgar.truesight.me/dao-protocol/<path>` (test prefix)
- Rails (current live): `https://edgar.truesight.me/<path>`

---

## PR2 — `/proxy/gas/:name`  · IMPL DONE (dao_protocol#34) · ramp pending

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
- [ ] 🧑 Live WRITE-GAS POST (`qrCodeGenerator`, `daoForms`, `feedback`) — skipped to avoid real
  side effects; covered by the mocked POST test. *Operator:* approve a benign POST payload if you
  want a live write-path proxy check.

**⚠️ FINDING — Rails `/proxy/gas` returns 401 (decision needed):**
Live Rails `/proxy/gas/*` returns **401 for every name + OPTIONS** (while `/ping` is 200). Root
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

## PR3 — newsletter + email-agent tracking pixels  · PENDING IMPL
- [ ] ⬜ `/newsletter/open.gif` → 1×1 gif + logs open
- [ ] ⬜ `/newsletter/click` → logs + 302 to decoded `to` URL
- [ ] ⬜ `/email_agent/open.gif`, `/email_agent/click`
- [ ] 🧑 confirm Main Ledger tabs update (`Agroverse News Letter Emails`, `Email Agent Drafts`) — sheet check

## PR4 — `/agroverse_shop/shipping_rates`  · PENDING IMPL
- [ ] ⬜ valid address → EasyPost USPS rates JSON
- [ ] ⬜ `mirror`/shadow vs Rails on a sample of real addresses (read-only → safe to shadow)
- [ ] 🧑 confirm agroverse_shop client GAS fallback still covers proxy errors

## PR4b — `/qr-code-check`  · PENDING IMPL
- [ ] ⬜ `SAMPLE`/`GIFT`/`SOLD` → landing redirect + UTM params
- [ ] ⬜ unknown qr → 404
- [ ] 🧑 a real `MINTED` scan → Stripe **test-mode** checkout → `?session_id=` reconcile → `SOLD` + QR Code Sales row (operator; touches Stripe + ledger)

## PR5 — `/dao/*` submit_contribution (per signed event)  · PENDING IMPL
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

## Operator (🧑) summary — what needs you
1. ⚠️ **Decide the `/proxy/gas` 401**: ramp to Python (recommended — Python is the working impl) **or** fix Rails (`skip_before_action :rate_limit_bot_calls` on `proxy#gas`). Unblocks the PR2 ramp.
2. Approve a benign POST payload if you want a live write-GAS proxy check (else the mocked POST test stands).
3. When PR5/PR6 land: dogfood signed events with your own key/governor signature, do the `EMAIL VERIFICATION` loopback on your machine, and trigger a Stripe test-mode checkout.
