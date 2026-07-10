# Resend Verification Email — Implementation Plan & Execution Roadmap

**Status:** HANDED OFF to Sophia 2026-06-08 · **Owner:** Sophia (autopilot) · **Sponsor:** Gary
**Baton for:** the local-LLM → Sophia execution handoff (see `SOPHIA_HANDOFFS.md`).

---

## 1. Problem

The email-verification flow (oracle.truesight.me "Link to DAO Identity", and
dapp `create_signature.html`):

1. User submits `[EMAIL REGISTERED EVENT]` → Edgar appends a **VERIFYING** row
   to *Contributors Digital Signatures* with a one-time verification key (`vk`)
   → GAS mailer (`sendEmailVerification`) emails a link → user clicks →
   `[EMAIL VERIFICATION EVENT]` → row flips **ACTIVE**.
2. **If the email never arrives or is lost, the user is stuck.** Re-submitting
   `[EMAIL REGISTERED EVENT]` is **deduped**: `DaoEmailRegistrationService`
   (`_process_registration`) returns `skipped` (no email) when the key is
   already VERIFYING/ACTIVE.
3. The oracle reuses **one persistent key per browser** (the user's identity +
   reading lineage), so they cannot get a fresh email by re-keying without
   orphaning their lineage. There is no resend path today.

## 2. Goal

A pending user can **resend their verification email** — same pending row, same
`vk` (existing link stays valid), rate-limited, no duplicate rows, no identity
change, signature still required.

## 3. Design decision — resend-on-re-register (no new endpoint)

When a re-submitted `[EMAIL REGISTERED EVENT]` is signed by a key that is
already **VERIFYING** (NOT ACTIVE), instead of returning `skipped`, **re-send
the verification email for the existing row** (reuse its `vk`), gated by a rate
limit. ACTIVE keys still skip (already verified).

- **Why:** reuses the existing signed `[EMAIL REGISTERED EVENT]` path + the
  existing `sendEmailVerification(email, vk, return_url)` GAS call — no new
  endpoint, no new signed event type. The frontend "Resend" is just a re-submit.
- **Rejected alt (v1):** a dedicated `POST /dao/resend_verification` — more
  surface area for no benefit over the re-register reuse.
- **vk policy:** **reuse** the existing `vk` (any in-flight link stays valid);
  do not rotate.
- **Rate limit:** reject a resend if the row's last-sent timestamp is within the
  cooldown window (recommend **60s**). Return a friendly cooldown result, not an
  error.

## 4. Pre-flight checklist (resolve before coding)

- [ ] **Which service is LIVE for `/dao/submit_contribution` + email
      registration** — Rails `sentiment_importer`
      (`app/services/dao_email_registration_service.rb`) vs the `dao_protocol`
      python port (`truesight_dao_client/server/email_registration.py`). Check
      the Edgar→dao_protocol cutover (`EDGAR_DAO_EXTRACTION_PLAN.md`, PR8).
      Implement in the LIVE one; keep the other in **parity**.
- [ ] Confirm the GAS `sendEmailVerification` re-sends fine with an existing
      `vk` (it just emails; should be idempotent).
- [ ] **Rate-limit storage:** add a "verification email last sent at" timestamp
      to the VERIFYING row (a new column on *Contributors Digital Signatures*),
      or reuse an existing timestamp column. Decide + note the column.
- [ ] Confirm the oracle's pending-state UI (PR2's host) is deployed —
      shipped in `TrueSightDAO/oracle` PR #35 (three-state identity UX),
      merged 2026-06-08.

## 5. Sequenced PRs

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This plan (baton) | agentic_ai_context |
| **PR1** | **Server resend-on-pending.** In the live handler (+ parity port): when `existing.status == VERIFYING`, look up the row's `vk`, enforce the cooldown, re-trigger `sendEmailVerification`, return `{ok, resent:true, verification_email_sent:true}` (or `{ok, cooldown:true, retry_after_s}` if rate-limited). ACTIVE → still `skipped`. No duplicate row. | sentiment_importer (+ dao_protocol port) |
| **PR2** | **Oracle resend affordance.** In `showPendingState`, add a "Didn't get it? Resend" link that re-runs the registration submit (re-sign `[EMAIL REGISTERED EVENT]` with the stored email + key) and shows "Sent again — check inbox/spam" or the cooldown message. | oracle |
| **PR3** *(optional)* | **dapp parity.** Mirror the resend affordance in `create_signature.html` pending UI. Beta-first: `dapp_beta` → promote to `dapp_prod`. | dapp_beta |

## 6. Resume tracker

> **RESUME HERE →** PR1 (server resend-on-pending). PR2 depends on PR1 landing
> (so the resend actually mails). After each unit merges, report the DAO
> contribution before the next (see `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`).

| Unit | Repo | Merged | Contribution reported |
|---|---|---|---|
| PR0 plan | agentic_ai_context | ☐ | — |
| PR1 server resend-on-pending | sentiment_importer (+ dao_protocol) | ☐ | ☐ |
| PR2 oracle resend affordance | oracle | ☐ | ☐ |
| PR3 dapp parity (optional) | dapp_beta → dapp_prod | ☐ | ☐ |

## 7. Acceptance tests

- Register a fresh key → pending. Trigger Resend → a new email arrives; the
  link still verifies → ACTIVE.
- Resend within the cooldown window → friendly "please wait ~Ns" result; **no**
  email sent.
- Already-ACTIVE key re-submits → still `skipped` (no email).
- No duplicate VERIFYING rows created by resends.
- Signature still verified on every resend (it's a signed `[EMAIL REGISTERED
  EVENT]`).

## 8. Guardrails

- Rate-limit every resend (anti-spam / anti-abuse).
- Never resend to ACTIVE keys.
- Reuse the existing `vk` so in-flight links stay valid.
- Keep the signed-payload contract intact (canonical body up to `--------`; the
  oracle/dapp fixes already sign correctly).
- Beta-first for any dapp change; oracle deploys from `main`.
