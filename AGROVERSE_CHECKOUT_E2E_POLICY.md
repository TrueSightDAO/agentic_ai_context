# Agroverse checkout: required E2E verification before merge

**Policy, effective 2026-07-18.** Any change to `agroverse_shop_beta`/`agroverse_shop_prod` that touches
checkout or the checkout Google Apps Script must be verified with a **real, live end-to-end run reaching an
actual Stripe Checkout session** before merging to `main`. This applies to any LLM agent (Claude, Sophia,
etc.) or human making these changes.

This is a specialization of **`OPERATING_INSTRUCTIONS.md` §9** (HTML/JS test-before-merge rule) for
checkout/GAS code specifically: §9's JSDom/happy-dom unit tests stub the network boundary and cannot catch
a live contract mismatch on either side of it (see "Why" below) — checkout/GAS changes need the real,
live round trip on top of, not instead of, the §9 unit tests. See also **`OPERATING_INSTRUCTIONS.md` §5e**
for how to scope the authorization envelope up front so verifying and syncing a fix like this doesn't
require asking the governor once per repo it touches.

## What triggers this policy

A PR touching any of:

- `js/checkout.js` (retail cart checkout)
- `js/white-label.js` (white-label checkout)
- `js/checkout-shipping-calculator.js`
- `js/config.js`'s `GOOGLE_SCRIPT_URL` constant
- `google-app-script/agroverse_shop_checkout/agroverse_shop_checkout.gs` (or any deployment-ID change for it)
- `js/subscribe.js` (subscription checkout)

## Why: the incident that prompted this

On 2026-07-18, two real production-affecting bugs were found only by actually driving the checkout flow with
a browser, not by the repo's existing mocked Playwright specs:

1. **Stale GAS deployment URL.** `js/config.js`'s `GOOGLE_SCRIPT_URL` pointed at a deleted Apps Script
   deployment. `script.google.com` returned Google Drive's generic "file not found" HTML (not a JSON error),
   so every checkout call silently failed with "load failed" on the payment step — on **both** beta and
   prod. This shipped and sat broken for an unknown period because nothing exercised the real deployment
   URL; the mocked specs stub the network call entirely.
2. **Shipping-rate field-name mismatch.** `white-label.js`'s `calculateShipping()` read
   `rate.service`/`rate.rate`/`rate.delivery_days` from the GAS response, but the GAS actually returns
   `rate.name`/`rate.amount`/`rate.deliveryDays` (confirmed live; matches the canonical
   `checkout-shipping-calculator.js` used by the retail cart). Every white-label shipping rate rendered as
   `"undefined — $NaN (? days)"`, and the order total was `NaN` — this would have reached Stripe with a
   broken amount. A mocked spec asserting on request *shape* would never catch a response-field mismatch
   like this; only a real round trip to the real GAS does.

Both bugs were caught and fixed the same day, once someone (in this case, an LLM agent) actually drove the
full flow — register, verify email, upload a design, fill shipping, submit — in a real browser against the
real Edgar + GAS backend, all the way to a real `checkout.stripe.com` session.

## The required check

Use **`scripts/e2e-checkout-verify.js`** in `agroverse_shop_beta` (Playwright, Node). It:

1. Registers a test account (real email verification — needs a readable inbox, e.g. `admin@truesight.me` via
   a Gmail API token; see `SERVICE_IDENTITY_ONBOARDING.md` / `CREDENTIAL_HANDOFF_PROTOCOL.md` for how an
   agent obtains that access).
2. Visits the real verification link (same-device, same persistent browser profile).
3. Uploads a test design image (auto-fits a throwaway pixel to satisfy the 600×1200 requirement).
4. Fills a real shipping address, waits for real shipping rates from the GAS, and **asserts the rendered
   rate text does not contain `"undefined"` or `"NaN"`** — this is what would have caught bug #2 above.
5. Submits the order and **asserts the browser actually lands on `checkout.stripe.com` with a `cs_test_...`
   session** (on beta/localhost) — this is what would have caught bug #1 above.

Run it in two steps (email verification needs a human/inbox in the loop):

```bash
cd agroverse_shop_beta  # or a worktree with the change applied
node scripts/e2e-checkout-verify.js register "<test-email>" [profileDir] [baseUrl]
# check the inbox for the verification email, then:
node scripts/e2e-checkout-verify.js continue "<verification-url>" [profileDir] [baseUrl]
```

The script exits non-zero and prints `FAIL: <reason>` on any of: verification not landing on the gallery,
upload not appearing, broken shipping-rate rendering, a disabled submit button, or not reaching a real
Stripe test session. Treat any `FAIL` as a merge blocker.

**Do not merge a checkout/GAS-touching PR on the strength of the mocked specs alone.** Those specs
(`tests/white-label-stripe-sandbox.spec.ts` etc.) are still valuable for fast regression coverage of request
*shape*, but they stub the network boundary and cannot catch a live contract mismatch on either side of it.

## Prod parity

`agroverse_shop_prod` is a real fork of `agroverse_shop_beta`, not the same repo — fixes merged to beta's
`main` do **not** automatically reach prod. When a checkout/GAS fix lands on beta, check whether prod's
`main` is missing the same commits (`git log origin/main..beta/main` after adding beta as a remote) and sync
them over via a normal branch + PR (never push directly to prod's `main`). See `PROJECT_INDEX.md`'s
`agroverse_shop` row for the beta/prod repo split.
