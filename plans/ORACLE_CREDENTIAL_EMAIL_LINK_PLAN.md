# Oracle Credential Email Link — Implementation Plan

**Status:** Draft · **Owner:** Gary Teh · **Started:** 2026-06-07

## Problem

The oracle credential page at `truesight.me/programs/truesight-grounding/credentials/#pk-iWL9OH9hpE_D` shows the practitioner as anonymous (`practitioner_name: ""`) because the oracle keypair is generated locally in the browser and never linked to a DAO identity.

The `create_signature.html` page at `dapp.truesight.me/create_signature.html` already solves this for the DApp — it generates an RSA keypair, submits an `[EMAIL REGISTERED EVENT]` to Edgar, and the user verifies via email. But the oracle page already has a keypair in localStorage from `oracle-draw-submit.js`. We don't need to generate new keys — we just need the email-registration step.

## Key Insight

The oracle page (`oracle.truesight.me`) auto-generates an RSA keypair on first load and stores it in `localStorage` under the same keys as the DApp:
- `publicKey`
- `privateKey`

These are the same keys used to sign `[PRACTICE EVENT]` submissions to Edgar. The credential page at `truesight.me/programs/truesight-grounding/credentials/` reads the credential data from `lineage-credentials` and renders the `practitioner_name` field — which is currently empty.

By adding an email-registration flow to the credential page (or the oracle page), the practitioner can link their existing keypair to their email. Once verified, Edgar associates the public key with the email in `dao_members.json`, and the credential page can look up the name.

## Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  oracle.truesight.me│     │  Credential Page  │     │     Edgar        │
│  (has keypair in LS)│     │  (truesight.me/   │     │  (DAO API)       │
│                     │     │   programs/...)   │     │                  │
│  ┌─────────────┐    │     │  ┌─────────────┐  │     │  ┌────────────┐  │
│  │ publicKey   │    │     │  │ Email input │  │     │  │ dao_members│  │
│  │ privateKey  │    │     │  │ + Link btn  │──┼─────┼─>│ .json      │  │
│  └─────────────┘    │     │  └─────────────┘  │     │  └────────────┘  │
│         │           │     │         │          │     │                  │
│         │ same keys │     │         │ signs    │     │                  │
│         ▼           │     │         ▼          │     │                  │
│  ┌─────────────┐    │     │  ┌─────────────┐  │     │                  │
│  │ [PRACTICE   │    │     │  │ [EMAIL      │──┼─────┼─>                │
│  │  EVENT]     │    │     │  │  REGISTERED │  │     │                  │
│  └─────────────┘    │     │  │  EVENT]     │  │     │                  │
│                     │     │  └─────────────┘  │     │                  │
└─────────────────────┘     └──────────────────┘     └──────────────────┘
```

## Implementation

### Phase 1: Add email-link section to credential page

**File:** `truesight_me_beta/programs/truesight-grounding/credentials/index.html`

Add a new section below the credential body that:

1. **Checks localStorage** for existing `publicKey` and `privateKey`
2. **If keys exist:** Shows an email input + "Link to my DAO identity" button
3. **If no keys:** Shows a message "Use the oracle at oracle.truesight.me to generate your keypair first"
4. **On submit:** Signs an `[EMAIL REGISTERED EVENT]` with the existing keypair and sends to Edgar
5. **On success:** Shows "Check your email for a verification link"
6. **On verification:** The credential page refreshes and shows the practitioner's name

**Key difference from create_signature.html:**
- `create_signature.html` generates a NEW keypair AND registers email
- This flow uses the EXISTING keypair and only registers email
- The `[EMAIL REGISTERED EVENT]` payload is identical — Edgar doesn't care whether the key is new or existing

### Phase 2: Credential page name resolution

**File:** `truesight_me_beta/js/program-shell.js`

The `renderCredential` function currently reads `cv.display_name` or falls back to `slug`. After Phase 1, the practitioner's email is linked to their public key in `dao_members.json`. The credential page should:

1. After loading the CV, check if `practitioner_name` is empty
2. If empty, look up the public key in `dao_members.json` (via the cached copy at `treasury-cache/dao_members.json`)
3. If found, display the contributor name instead of the slug

This is a nice-to-have — the primary fix is Phase 1, which makes the name appear in the `practitioner_name` field of future practice events.

### Phase 3 (optional): Add link to oracle page itself

**File:** `oracle/index.html`

Add a small "Link this oracle to your DAO identity" link/button on the oracle page itself, so practitioners don't need to navigate to the credential page to register their email.

## Execution Roadmap

### PR 1: Credential page email-link section

- Edit `truesight_me_beta/programs/truesight-grounding/credentials/index.html`
- Add email registration section below credential body
- Reuse `EdgarPayloadHelper` from the DApp (or inline the signing logic)
- Submit `[EMAIL REGISTERED EVENT]` with existing keypair
- Show status messages inline

### PR 2: Verification flow

- The standard Edgar verification flow already exists (email → verification link → `[EMAIL VERIFICATION EVENT]`)
- No code changes needed — this works out of the box once PR 1 is deployed

### PR 3: Name resolution on credential page

- Edit `truesight_me_beta/js/program-shell.js`
- After CV load, if `practitioner_name` is empty, look up `dao_members.json` by public key
- Display contributor name if found

### PR 4: Promote to prod

- `sync_beta_to_prod(truesight_me_prod)` after each PR is reviewed and merged

## Checklist

- [ ] **PR 1:** Add email registration section to credential page
  - [ ] Add HTML section with email input + button
  - [ ] Add JS to check localStorage for existing keys
  - [ ] Add JS to sign and submit `[EMAIL REGISTERED EVENT]`
  - [ ] Add status messages (loading, success, error)
  - [ ] Deploy to beta and verify
- [ ] **PR 1 verification:** Test end-to-end on beta
  - [ ] Open credential page with existing oracle keypair in localStorage
  - [ ] Enter email and click "Link"
  - [ ] Verify `[EMAIL REGISTERED EVENT]` is submitted to Edgar
  - [ ] Check email for verification link
  - [ ] Click verification link
  - [ ] Verify `dao_members.json` now has the oracle public key associated with the email
- [ ] **PR 2:** (No code changes — verification flow already exists)
- [ ] **PR 3:** Name resolution on credential page
  - [ ] Add `dao_members.json` lookup by public key
  - [ ] Display contributor name when found
  - [ ] Deploy to beta and verify
- [ ] **PR 4:** Promote to production
  - [ ] `sync_beta_to_prod(truesight_me_prod)`
  - [ ] Verify live on truesight.me

## Open Questions

1. **Where should the email-link section live?** On the credential page (truesight.me/programs/...) or on the oracle page (oracle.truesight.me)? The credential page is where the name is displayed, so it makes sense there. But the oracle page is where the practitioner spends their time. Answer: start on the credential page, add to oracle page as Phase 3.

2. **Should we show the email-link section to ALL visitors or only when localStorage has keys?** Only when localStorage has keys — otherwise it's confusing noise.

3. **What if the practitioner has multiple oracle keypairs?** Each keypair is independent. They'd need to link each one separately. This is fine — the credential page only shows the current browser's keypair.

4. **Does the credential page on truesight.me have access to the oracle.truesight.me localStorage?** No — they're different origins. The practitioner would need to be on the credential page's origin (truesight.me) for the keys to be accessible. However, `oracle-draw-submit.js` stores keys under the same `localStorage` keys (`publicKey`/`privateKey`) on `oracle.truesight.me`. The credential page on `truesight.me` won't see those keys.

   **Resolution:** The email-link section should live on the **oracle page** (`oracle.truesight.me`), not the credential page. The oracle page already has the keys. After linking, the credential page can resolve the name via `dao_members.json` lookup (Phase 3).

   Alternatively, we could add the email-link to BOTH pages — the oracle page for the primary flow, and the credential page with a note saying "Use the oracle to link your identity" if no keys are found.

## See Also

- `dapp/create_signature.html` — existing email registration flow (reference implementation)
- `oracle/assets/js/oracle-draw-submit.js` — existing keypair management on oracle page
- `truesight_me_beta/js/program-shell.js` — credential page rendering
- `truesight_me_beta/programs/truesight-grounding/credentials/index.html` — credential page HTML
- `agentic_ai_context/CREDENTIALING_PROGRAM_PAGES.md` — credentialing surface spec
