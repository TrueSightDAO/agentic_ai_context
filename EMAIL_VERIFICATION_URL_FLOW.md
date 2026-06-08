# Email Verification URL Flow

How the verification email builds its landing-page URL, and how the landing page
parses the parameters to auto-submit the `[EMAIL VERIFICATION EVENT]`.

**Why this doc exists:** the URL construction logic lives in a GAS script
(`edgar_send_email_verification.gs`) and the parsing logic lives in
`create_signature.html` — neither is obvious from the other. This doc bridges
them so future LLMs or operators setting up a new verification flow (different
site, different landing page, service-identity bot) don't have to
reverse-engineer it.

---

## The flow at a glance

```
Edgar (Rails)
  │
  │  GET ?action=sendEmailVerification&secret=...&email=...&verification_key=...&return_url=...
  ▼
GAS web app (edgar_send_email_verification.gs)
  │
  │  buildSignatureVerificationUrl_(email, vk, returnUrl)
  │    → returnUrl + ?em=<email>&vk=<verification_key>
  │
  │  GmailApp.sendEmail(email, subject, verifyUrl)
  ▼
User clicks link in email
  │
  ▼
Landing page (default: create_signature.html)
  │
  │  readVerifyParams() → { em, vk }
  │  auto-submits [EMAIL VERIFICATION EVENT] via submitSignedEmailEvent()
  │  stripVerifyParamsFromUrl() → cleans URL
  ▼
Edgar flips contributor to ACTIVE
```

---

## URL construction (GAS side)

**File:** `tokenomics/google_app_scripts/tdg_identity_management/edgar_send_email_verification.gs`
**Function:** `buildSignatureVerificationUrl_(email, vk, returnUrl)`

```javascript
function buildSignatureVerificationUrl_(email, vk, returnUrl) {
  const base = String(returnUrl || '').split('#')[0];
  const join = base.indexOf('?') >= 0 ? '&' : '?';
  return base + join + 'em=' + encodeURIComponent(email) + '&vk=' + encodeURIComponent(vk);
}
```

**Key behaviour:**
- `returnUrl` defaults to `https://truesightdao.github.io/dapp/create_signature.html`
  if not provided by Edgar.
- The `#` fragment (if any) is stripped before appending params.
- If `returnUrl` already has a `?`, params are joined with `&` instead of `?`.
- `em` = the contributor's email (lowercased, URL-encoded).
- `vk` = the verification key (a long opaque string, URL-encoded).

**Who calls it:**
- `handleEmailVerificationRequest_()` — the shared handler for both GET and POST.
- Edgar (Rails) passes `return_url` from its `EMAIL_VERIFICATION_GAS_WEBHOOK_URL`
  config or from the `generation_source_url` of the original `[EMAIL REGISTERED EVENT]`.

---

## URL parsing (browser side)

**File:** `dapp_beta/create_signature.html` (or `dapp_prod/create_signature.html`)
**Functions:** `readVerifyParams()`, `stripVerifyParamsFromUrl()`

```javascript
function readVerifyParams() {
  const params = new URLSearchParams(window.location.search || '');
  const vk = (params.get('vk') || '').trim();
  const em = normalizeEmail(params.get('em') || '');
  if (!vk || !em) return null;
  return { vk, em };
}

function stripVerifyParamsFromUrl() {
  const url = new URL(window.location.href);
  url.searchParams.delete('vk');
  url.searchParams.delete('em');
  window.history.replaceState({}, document.title, url.pathname + url.search + url.hash);
}
```

**Key behaviour:**
- Called in `window.onload` — if `?em=` and `?vk=` are present, the page
  auto-submits the `[EMAIL VERIFICATION EVENT]` without requiring a button click.
- After successful submission, `stripVerifyParamsFromUrl()` removes the params
  from the browser's URL bar (clean state, no re-submit on refresh).
- If the user opens the link on a **different browser** (no local keypair), the
  page shows an error: "This is not the original browser that started registration."

**The auto-submit flow:**
```javascript
if (verifyParams) {
  // Show verify section, then auto-click after 0ms
  setTimeout(() => { verifyBtn.click(); }, 0);
}
```

The click handler calls `submitSignedEmailEvent()` with:
```javascript
{
  eventName: 'EMAIL VERIFICATION EVENT',
  attributes: {
    'Verification Key': params.vk,
    Email: params.em
  }
}
```

---

## The `return_url` parameter — how it controls the landing page

Edgar passes `return_url` to the GAS web app. The value comes from the
`generation_source_url` field of the original `[EMAIL REGISTERED EVENT]` — i.e.
the URL of the page where the user entered their email.

| Source | `return_url` value |
|--------|-------------------|
| DApp `create_signature.html` | `https://truesightdao.github.io/dapp/create_signature.html` (default) |
| `lineage-register.html` (self-serve) | `https://truesight.me/lineage-register.html` |
| Service-identity bot setup | A sentinel URL like `https://<bot-slug>.setup/verify` |

This means the verification link always returns the user to **the same page they
started from** — the `return_url` is the `generation_source_url` echoed back.

---

## Service-identity bot variant

For autonomous bots (see `SERVICE_IDENTITY_ONBOARDING.md`), the flow is the same
but the `return_url` is a sentinel URL (not a real page) because no human clicks
it. Instead, a script polls Gmail, finds the email by subject, extracts the
`?em=&vk=` params from the link in the email body, and submits the
`[EMAIL VERIFICATION EVENT]` directly via the bot's keypair.

---

## Key files

| File | Role |
|------|------|
| `tokenomics/.../edgar_send_email_verification.gs` | GAS web app — builds URL, sends email |
| `dapp_beta/create_signature.html` | Landing page — parses URL, auto-submits verification |
| `sentiment_importer/.../dao_email_registration_service.rb` | Edgar (Rails) — triggers the GAS call |
| `agentic_ai_context/SERVICE_IDENTITY_ONBOARDING.md` | Bot variant of this flow |

---

## Testing / debugging

- **Dry run:** run `editorDryRunVerificationEmail()` in the Apps Script editor
  — logs the verify URL without sending email.
- **Resend:** run `editorResendVerificationEmailWithPrompts()` — prompts for
  email, vk, and return_url, then sends.
- **Check the link:** the verify URL is logged at `handler_sending_gmail` stage
  in Apps Script Executions (truncated to 200 chars).

---

## Anti-patterns

- **Hardcoding the landing page URL** in the GAS script instead of using
  `return_url`. The whole point of `return_url` is that the user returns to
  the same page they started from — hardcoding breaks the lineage-register flow.
- **Stripping `return_url` from the Edgar call.** Without it, the default
  (`create_signature.html`) is used, which may not be the right landing page.
- **Not URL-encoding `em` or `vk`.** The `encodeURIComponent` calls in
  `buildSignatureVerificationUrl_` are essential — `vk` can contain `+`, `/`,
  or `=` characters that break raw URL parsing.

*Created 2026-06-07 to document the gap identified during a Telegram conversation
about why the verification link wasn't routing correctly.*
