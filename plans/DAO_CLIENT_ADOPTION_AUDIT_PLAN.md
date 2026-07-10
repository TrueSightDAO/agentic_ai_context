# DAO Client adoption audit — stop hand-rolling; use the library methods

**Status:** HANDED OFF to Sophia 2026-06-08 · **Owner:** Sophia (autopilot) · **Sponsor:** Gary

Verify that **oracle** and **capoeira** use the **high-level `@truesight_dao/dao-client`
methods** instead of hand-rolling signing / payload-building / submission /
identity flows — then migrate the gaps. Both consumers currently reimplement
everything inline (oracle was reverted to inline in #43; capoeira was never
swapped), so they're duplicating logic the library now owns — the exact source
of the bugs this whole effort started from.

## Preflight
Refresh first: read this via `read_repo_file` (GitHub `main`). (See
`SOPHIA_HANDOFFS.md` § "Before you start".)

## The library surface now available (v1.1.0)

`new DaoClient()` instance methods (browser global `DaoClient` is the class):
- **`submitEvent({ eventType, fields, … })`** — canonical text + nonce + sign +
  FormData + POST + parse, in one call (replaces hand-rolled signing+submit).
- **`registerEmail(email)`** / **`verifyEmail(email, vk)`** — email lifecycle.
- **`checkRegistration()`** — Edgar status (registered / pending / contributor).
- **`getSlug()`**, **`generateKeyPair()`**, **`verifyPayload()`**.
- statics: `arrayBufferToBase64`, `base64ToArrayBuffer`, `base64ToBase64Url`.

> PR1 must first **confirm the exact published API** of the version being pinned
> (currently `latest = 1.1.0-rc.1`) — audit/migrate against what's actually
> shipped, not this list from memory.

## What each consumer hand-rolls today (the gap)

**Oracle** — `assets/js/oracle-draw-submit.js`: `signRequestText`,
`buildPracticeEventText`, `submitSession`, `generateKeypair`, `publicKeyToSlug`,
base64 helpers. `index.html`: `handleDaoIdentityLink`, `handleVerificationParams`,
`checkDaoRegistration`, base64 helpers.
**Capoeira** — `assets/js/practice-event-submit.js`: `signRequestText`,
`buildPracticeEventText`, `submitSession`, `generateKeypair`, `publicKeyToSlug`,
base64 helpers.

## Target mapping (hand-rolled → library)

| Hand-rolled (both consumers) | Replace with |
|---|---|
| sign + build canonical text + FormData + POST a PRACTICE EVENT | `client.submitEvent({ eventType: 'PRACTICE EVENT', fields })` |
| `handleDaoIdentityLink` (oracle) | `client.registerEmail(email)` |
| `handleVerificationParams` (oracle) | `client.verifyEmail(email, vk)` |
| `checkDaoRegistration` (oracle) | `client.checkRegistration()` |
| `publicKeyToSlug` / cv-url | `client.getSlug()` |
| key gen + base64 helpers | `DaoClient.generateKeyPair()` / the statics |

**Keep consumer-side** (the right boundary): event-specific **field assembly**
(what goes in `fields` — hexagrams/QMDJ for oracle, session shape for capoeira),
UI rendering (the oracle's **3-state identity UX**), `localStorage` session
history + `backfillUnsent`, reading-permalink logic.

## Sequenced PRs

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This plan | agentic_ai_context |
| **PR1** | **Audit + gap report** — enumerate the published API; per consumer, table every signing/identity/submission site → using-library? / hand-rolled? / target method. Post the report in the topic. | (audit) |
| **PR2** | **Oracle migration** to the high-level methods (drop the hand-rolled signing/identity; keep field assembly + 3-state UX + kill-switch). | oracle |
| **PR3** | **Capoeira migration** to the high-level methods (keep session shape + backfill). | capoeira |

## Gates (every migration PR)

1. **Pin the version** + **verify it serves on unpkg (200) in-PR** + **confirm
   the methods exist** in that version.
2. **Depend on a verified library:** PR2/PR3 require `submitEvent` to be correct
   — i.e. the **canonical test-vector suite green** (byte-match Edgar's verifier,
   nonce, generationSource, outcome surfacing). If that's only in `1.1.0` final,
   migrate against `1.1.0`, not the rc.
3. **Runtime smoke test**, not just `node --check`.
4. **Fix load order** (global is the class now; ensure it's defined before use).
5. **Map-before-delete**; **preserve** the canonical-signing correctness, the
   oracle 3-state UX, the SW kill-switch, and capoeira's backfill.
6. **Open PR, do NOT auto-merge** (both deploy from `main`); report for review.
7. `Generated-by: Sophia (TrueSight Autopilot)` on every commit + PR.

## Relationship to existing plans

This **supersedes the "swap the base64 helpers" framing** of Issue 2 (oracle) /
Issue 3 (capoeira) in `DAO_CLIENT_INTEGRATION_FIXES.md` — the target is the FULL
high-level API, not just the helpers (half-adopting helpers is what broke prod).
Update that tracker as PR2/PR3 land.

## Resume tracker

> **RESUME HERE →** PR1 (audit + gap report — read-only, can run now). PR2/PR3
> migrate once the library's high-level methods are verified (see Gate 2).

| Unit | Repo | Blocked on | Done |
|---|---|---|---|
| PR0 plan | agentic_ai_context | — | ☑ |
| PR1 audit + gap report | — | — | ☐ |
| PR2 oracle migration | oracle | verified library (Gate 2) | ☐ |
| PR3 capoeira migration | capoeira | verified library (Gate 2) | ☐ |

## Acceptance

- A gap report for both consumers (every signing/identity/submission site
  classified).
- Oracle + capoeira contain **no hand-rolled** signing / canonical-payload /
  FormData-POST / identity code — they call `submitEvent` / `registerEmail` /
  `verifyEmail` / `checkRegistration` on the pinned version.
- Each works end-to-end in a browser (cast → submit → credential link; link →
  pending → verified), zero console errors, shipped via reviewed PRs.
