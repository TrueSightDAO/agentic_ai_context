# @truesight_dao/dao-client v1.1.0 — Implementation Plan

> **Status:** Draft — not yet started
> **Owner:** Unclaimed
> **Depends on:** v1.0.1 shipped (PR #69 merged, npm published)

## Motivation

Claude's review of the v1.0.0 `submit()` design (relayed by Gary, 2026-06-07) identified 5 MUST-HAVES that each correspond to a real bug we hit in production:

1. **Canonical bytes must BYTE-match Edgar's verifier** — the Ruby `SignatureVerifier` signs up to and including the first `--------`, then `.strip()`. The JS `PayloadBuilder` must produce identical bytes. Ship a test-vector suite cross-checked against Ruby.
2. **Auto-inject a nonce (Timestamp)** — persistent keys produce identical signatures for identical fields → HTTP 409 "Duplicate submission".
3. **Own the signed-body vs wrapper split** — `fields` = the signed key-values before `--------`. The library owns the wrapper AFTER it (signature, txId, generation source, verify URL).
4. **Surface outcomes, don't flatten** — `{ok, requestHash, slug}` isn't enough. Distinguish 409, 422, signature_verification, and the email lifecycle.
5. **Guard field values against `[... EVENT]` substrings** — Edgar dispatches by substring; a bracketed tag inside a value causes a 422 misdispatch.

## Design decisions

### Additive, not breaking (v1.1.0, not v2.0.0)

Keep the low-level primitives (`CryptoUtils`, `PayloadBuilder.build()`, `EdgarClient.buildShareText()`) as zero-cost escape hatches for odd/future shapes. Add `submitEvent()` as the documented happy path.

### `submitEvent({eventType, fields})` signature

```ts
interface SubmitEventOptions {
  eventType: string;           // e.g. "CONTRIBUTION EVENT"
  fields: Record<string, unknown>;  // key-value pairs, signed
  generationSource?: string;   // default: window.location.origin + pathname
  edgarBase?: string;          // override default Edgar URL
}

interface SubmitEventResult {
  ok: boolean;
  status: 'submitted' | 'duplicate' | 'signature_verification_failed' | 'validation_failed' | 'server_error';
  txId: string;
  slug: string;
  httpStatus: number;
  emailRegistration?: {
    status: 'activated' | 'already_consumed' | 'pending_verification' | 'pubkey_mismatch' | 'not_found';
    contributorEmail?: string;
  };
  error?: string;
}
```

### Canonical bytes contract

```
[EVENT NAME]
- Field1: value1
- Field2: value2
--------
```

- Event name is `[` + trimmed + `]`.
- Fields are sorted by insertion order (preserved from JS object).
- Each field is `- Key: value`.
- Multi-line values get indented continuation.
- Ends with `--------` (no trailing newline in the signed payload — the Ruby verifier does `.strip()` on the message).
- **Timestamp is auto-injected** as the first field: `- Timestamp: <ISO 8601>`.

### Test-vector suite

A JSON file `packages/dao-client/test/vectors/submit-event-vectors.json` with entries like:

```jsonc
[
  {
    "name": "basic contribution event",
    "eventType": "CONTRIBUTION EVENT",
    "fields": { "Type": "Time (Minutes)", "Amount": "40" },
    "expectedCanonical": "[CONTRIBUTION EVENT]\n- Type: Time (Minutes)\n- Amount: 40\n--------",
    // Note: Timestamp is auto-injected, so the canonical string includes it.
    // The test generates a known timestamp or uses a regex match.
    "expectedCanonicalPattern": "^\\[CONTRIBUTION EVENT\\]\\n- Timestamp: \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{3}Z\\n- Type: Time \\(Minutes\\)\\n- Amount: 40\\n--------$"
  }
]
```

Cross-checked against Ruby `SignatureVerifier`: run the same vectors through both and assert they verify.

### Email methods

Convenience methods that wrap `submitEvent` with specific event types and outcome parsing:

- `registerEmail(email)` — submits `[EMAIL REGISTERED EVENT]` with `- Email: <email>` and `- Timestamp: <now>`. Returns `{ok, status, txId}` where status includes `pending_verification`.
- `verifyEmail(email, verificationKey)` — submits `[EMAIL VERIFICATION EVENT]` with `- Email: <email>` and `- Verification Key: <vk>`. Returns `{ok, status, emailRegistration}`.
- `checkRegistration(publicKey?)` — calls Edgar's `check_digital_signature` endpoint. Returns `{registered, pending_verification, contributor_email, ...}`.

### Field value guard

`submitEvent` rejects any field value containing `[` + `EVENT]` (case-insensitive) with a clear error. This prevents the misdispatch bug where a value like `"See [CONTRIBUTION EVENT] notes"` causes Edgar to route the submission to the wrong handler.

### Node guard

`window.location` defaults throw in Node 18+. `submitEvent` accepts `generationSource` as a param (defaulting to `window.location.origin + pathname` when available, requiring it when `window` is undefined).

## Execution checklist

### Phase 1: Test vectors + canonical-bytes alignment

- [ ] Create `packages/dao-client/test/vectors/submit-event-vectors.json` with 10+ test cases covering:
  - Basic event with simple fields
  - Event with multi-line values
  - Event with special characters in values
  - Event with `[... EVENT]` substring in a value (should be rejected)
  - Empty fields
  - Numeric, boolean, and null field values
- [ ] Write a JS test runner that asserts `PayloadBuilder.build()` output matches expected canonical strings
- [ ] Cross-check against Ruby `SignatureVerifier`: export the same vectors as Ruby test fixtures, run through `SignatureVerifier.verify()`, assert they verify
- [ ] Fix any byte-level drift between JS and Ruby canonical builders

### Phase 2: `submitEvent` implementation

- [ ] Add `submitEvent()` method to `DaoClient` class
- [ ] Auto-inject `Timestamp` field as first field in the signed body
- [ ] Implement field value guard (reject `[... EVENT]` substrings)
- [ ] Implement outcome parsing (distinguish 409, 422, signature_verification, etc.)
- [ ] Implement `generationSource` param with Node guard
- [ ] Write unit tests for all outcome paths

### Phase 3: Email methods

- [ ] Add `registerEmail(email)` method
- [ ] Add `verifyEmail(email, verificationKey)` method
- [ ] Add `checkRegistration(publicKey?)` method
- [ ] Write unit tests for email lifecycle outcomes

### Phase 4: Integration test

- [ ] Run a real `submitEvent` against Edgar staging/prod
- [ ] Run a real `registerEmail` + `verifyEmail` round-trip
- [ ] Verify the oracle's 3-state UI works with the new outcome shapes

### Phase 5: Publish

- [ ] Bump version to 1.1.0 in `package.json`
- [ ] Update CHANGELOG
- [ ] Push tag → CI publishes to npm
- [ ] Update oracle and capoeira CDN URLs to `@1.1.0`

## Files to create/modify

| File | Action |
|------|--------|
| `packages/dao-client/src/index.ts` | Add `submitEvent()`, `registerEmail()`, `verifyEmail()`, `checkRegistration()` |
| `packages/dao-client/src/payload.ts` | Add `Timestamp` auto-injection, field value guard |
| `packages/dao-client/src/edgar.ts` | Add outcome parsing helper |
| `packages/dao-client/test/vectors/submit-event-vectors.json` | **Create** — test-vector suite |
| `packages/dao-client/test/submit-event.test.ts` | **Create** — unit tests |
| `packages/dao-client/CHANGELOG.md` | Add v1.1.0 entry |
| `packages/dao-client/package.json` | Bump version |

## Risks

- **Test-vector drift** — if the Ruby `SignatureVerifier` is updated later, the JS test vectors must be updated in lockstep. Mitigation: add a CI step that runs the Ruby test suite against the same vectors.
- **Timestamp nonce breaks existing callers** — any code that calls `submit()` directly (not `submitEvent()`) won't get the auto-injected Timestamp. Mitigation: `submit()` is kept as-is; only `submitEvent()` gets the new behavior. Existing callers migrate at their own pace.
- **Email method error handling** — Edgar's email registration endpoint can return unexpected statuses. Mitigation: the `checkRegistration()` method is the authoritative source; `registerEmail()`/`verifyEmail()` surface the raw response alongside the parsed status.
