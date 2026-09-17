# PII Event Envelope — encrypt + commit PII-bearing DAO events

**Status:** DESIGN PROPOSED (2026-09-18) — awaiting governor option pick. **No code yet.**
**Thread:** 31842 · **Spawned from:** CRF payout work (thread 30026) · **Supersedes-risk:** `cfr-anapu#11` (P4, held unmerged)

---

> **Refined 2026-09-18 (thread 30026): the envelope applies at the PUBLIC-JSON boundary, not the browser.**
> Gary: *"I meant stuff written into telegram chat logs would be unencrypted. But stuff written into the
> json github repo should be encrypted if it contains PII for later verification purposes."*
> → The intake (col G) and the private `cfr program` sheet stay **plaintext**; the **public JSON repos**
> (`verify_public_signatures/**`, ADVISORY snapshots) carry **ciphertext + commitment**. Encryption runs
> **server-side at the JSON emitter** — so there is **no browser key custody**, and **P4 is NOT forked**
> (§11.6 proceeds; the envelope is a separate JSON-layer unit). §5 below is kept for the record of the
> first framing but is **superseded by this refinement**.

## 1. Goal (Gary, 2026-09-18)

> *"Extend the emitter for events with PII … encrypt it and then write it such that we could
> somehow verify later on that such events with PII are submitted without knowing exactly the
> details."*

Two requirements, and they are **coupled**:

1. **Confidentiality** — a PII field (PIX key / CPF / bank detail) must not be readable by anyone
   who sees the event payload.
2. **Verifiability without disclosure** — later, anyone must be able to confirm that *a* submission
   with *that* value happened, **without** the value having ever been in the clear.

This is the item **§11.7 of `CRF_ANAPU_SUNMINT_COHORT_PROPOSAL.md` explicitly deferred**
(*"a DAO-held symmetric key … deferred, not decided"*) — now being decided.

## 2. Not a reinstatement of §11.2

§11.2 (2026-09-17) **rejected** the earlier `tokenomics#499` design (`66089d6`, `pix_key_cipher`),
which bound privacy to a **governor's RSA private key**. Gary's reason: *"There is no key material to
lose, rotate, or mis-handle."*

The envelope is **different in kind**: it adds **commitment + selective disclosure**. Confidentiality
is a means; the *point* is auditable proof of submission. The key-custody objection must still be
answered (§6) — which is why custody is a first-class design constraint here.

## 3. Envelope design (hybrid; standard primitives only)

**Rule: WebCrypto / libsodium primitives only — never hand-rolled crypto.**

```
1. data_key      = random 256-bit AES key
2. ciphertext,iv = AES-256-GCM(data_key, canonical_json(pii_fields))
3. wrapped_key   = RSA-OAEP-SHA256(operator_pubkey, data_key)      # or ECDH-P256 + HKDF
4. commitment    = SHA-256( salt ‖ canonical_json(pii_fields) )    # salt = random 128-bit

envelope = {
  tag, event_type, envelope_version, alg,
  # --- cleartext, non-PII ---
  pk_hash, program_slug, pix_key_type, pix_key_masked, submission_source, created_at_utc,
  # --- protected ---
  iv, ciphertext, wrapped_key, commitment, commitment_salt, kdf
}
```

Non-PII metadata (the `pk_hash ↔ program` linkage, the masked key, the type) stays **cleartext** so
routing, dedup, and display work without decryption. Only the PII *value* is sealed.

## 4. "Verify without knowing" = three separable properties

These are often conflated; keep them apart in any implementation and test.

| Property | What it proves | Mechanism |
|---|---|---|
| **Existence / audit** | *an* event with commitment `C` was submitted by `pk_hash P` at time `T` | Edgar ledger row + RSA signature — verifiable with **no** plaintext |
| **Integrity** | the sealed payload is untampered | envelope hash + signature |
| **Selective disclosure** | *this* value was what was committed | operator later reveals `(value, salt)`; anyone checks `H(salt ‖ value) == C` |

Selective disclosure is the property §11.2 could not provide: you can prove *which* PIX you committed
later, having never exposed it.

## 5. Impact on P4 (§11.6) — a design fork

If adopted, `payout_registration.html` submits **ciphertext + commitment**, not the plaintext
`pix_key`. Therefore **P4 (`cfr-anapu#11`) is HELD unmerged** pending the option pick. Its
**Edgar-route plumbing is retained** (`EDGAR_SUBMIT_URL`, `ensureKeyPair`, `signText`, `submit()`
rewrite, provenance-last ordering); only the **payload builder** (`buildPayoutRegistrationEventText`)
changes to emit the envelope.

**Open decision (governor):** does the envelope **REPLACE** the raw-PIX-to-private-sheet transport,
or sit **alongside**?

**Recommendation — replace, with the sink decrypting:**

```
emitter → ciphertext + commitment → Edgar → intake (any surface: now safe)
        → sink decrypts with the operator key
        → `cfr program` / payout registrations gets plaintext (operator must be able to PAY)
        → ciphertext + commitment retained for audit / re-verification
```

Net: §11.2's *load-bearing consequence* (*"the intake must stay private"*) is **defused** — the
payload is safe even on a public surface. The ACL stays as defense-in-depth, but is no longer the only
thing between a CPF and the open web.

**Interim note:** while the envelope is undecided, P4's plaintext path keeps §11.2's consequence live;
this is the argument for option (b) **hold-and-rebase** over (a) merge-then-amend — see thread 30026.

## 6. Hard parts — must be solved BEFORE code (this is where §11.2's cipher died)

1. **Key custody.** NOT browser `localStorage`.
   - (a) governor key in the existing **Fernet vault** (`app/vault.py`, `/opt/truesight_autopilot/vault/`);
   - (b) **AWS KMS** envelope encryption — no key material on disk, IAM-gated.
   - **Lean: (b)** — audit trail + no at-rest key to mishandle.
2. **Escrow / recovery.** Key loss ⇒ **unrecoverable payouts**. Mitigate: **multi-recipient wrap**
   (wrap `data_key` to 2-of-3 governors) **plus** one offline escrow key held by Gary.
3. **Multi-recipient.** 2-of-3 governor wrap so no single key loss bricks a student's payout.
4. **Key separation.** Signing key (RSA, Edgar identity) ≠ encryption key (RSA-OAEP). Never reuse.
5. **Canonical JSON.** Deterministic serialization is mandatory for the commitment to be stable
   across emitters/verifiers (key order, number formatting, unicode normalization).

## 7. Test obligations

- Commitment is **stable** across re-serialization of the same logical PII object.
- Envelope contains **no** plaintext PII (mirror of the existing
  `tokenomics/scripts/test_payout_registration_privacy_guard.py`).
- A reveal of the **wrong** value fails against `C`; the right `(value, salt)` passes.
- Ciphertext **fails to decrypt** under a non-operator key.
- A non-governor **cannot** extract `data_key` (KMS/vault access gate).

## 8. Rollout

| Unit | Change | Repo | Gate |
|---|---|---|---|
| E1 | This design + `§11.10` cross-ref + manifest row | `agentic_ai_context` | auto |
| E2 | Envelope emitter + commitment (generic, not payout-only) | `truesight_autopilot` | auto |
| E3 | Sink decrypt + retain ciphertext/commitment | `tokenomics` | auto |
| E4 | Rebase P4 (`cfr-anapu#11`) onto the envelope | `cfr-anapu` / `dapp_beta` | auto (beta); prod on UAT |
| E5 | Operator key provisioning (KMS CMK + IAM + escrow) | — | **`gate: human`** |

## 9. Open questions for the governor

1. **Replace or alongside** the raw-PIX transport? *(recommend: replace, sink decrypts)*
2. **Custody:** Fernet vault or **AWS KMS**? *(recommend: KMS)*
3. **Escrow:** 2-of-3 governor wrap + offline key acceptable?
4. **Scope:** payout-only first, or a **generic** PII envelope for any future PII event?
   *(recommend: build it generic — E2 is emitter-side and cheap to generalize)*
