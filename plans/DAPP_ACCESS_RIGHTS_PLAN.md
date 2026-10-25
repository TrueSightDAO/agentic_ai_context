# DApp Access Rights — Plan of Record (UI-slice scope)

**Status:** Plan-of-record. **Created:** 2026-11 | **Owner:** Gary Teh | **Author:** Sophia Truesight (autopilot)
**Convention:** Follows `OPERATING_INSTRUCTIONS.md` §5 / §5a / §5d / §5e.

> ## RESUME HERE: Unit 0 — Julio Almeida's Edgar signing identity (no code; member action)

## Context

Gary (direct, this thread): **"I think UI slice so long as record works for Julio to do what he needs to do."**

Motivation: Gary wants **Julio Almeida** — a human DAO member (`Contributors contact information` row 427, email `davajhabib@outlook.com`, Discord `1554404598381543494`) — to help annotate store records via:
- https://dapp.truesight.me/store_interaction_history.html
- https://dapp.truesight.me/stores_by_status.html

Julio's three stated needs (Gary, verbatim intent): (1) update store records where data is missing, (2) add new store records worth considering to the funnel, (3) add remarks/comments used when generating follow-up emails to store keepers.

**Scope decision:** UI slice only. The full per-contributor ACL system (allowlist-as-CI-validator, append-only grant/revoke fold, contributor-keyed, `expires_at`) is **deferred** — see *Deferred* for why.

The plan text below was drafted after (A) governor-signed grant+revoke and (B) `grantable`-only scope were recommended by Envoy; Gary's direct reply superseded that with the narrower UI-slice instruction.

## Key pre-flight finding: the UI slice is ALREADY SHIPPED

The UI affordances Gary approved already exist in **both beta and prod**. Verified by reading the deployed page sources (quoted snapshots below):

| Page | Affordance | Gate today |
|---|---|---|
| `store_interaction_history.html` | Full **"Update Store Information"** edit form — status, shop type, owner, contact person, email, phone, cell, website, Instagram, follow-up / deferred-until / visit / contact dates, contact method, **remarks, attachments** | `verifySignatureOnLoad()` → if `localStorage.publicKey` resolves to a **registered contributor**, `setInteractionMode('interactive')`. **No role check.** |
| `stores_nearby.html` | **"Save New Store"** | same `interactionMode` signature-presence gate |
| `stores_by_status.html` | browse / filter → opens Store Interaction History | read-only |

Verbatim anchors:
- `store_interaction_history.html` L655 (prod): `<button type="button" class="btn" id="updateStoreBtn" data-requires-signature="true">Update Store Information</button>`
- `store_interaction_history.html` L847: `var interactionMode = 'view-only';` → L964 `function setInteractionMode(mode)`, set to `'interactive'` at L1974 only after `verifySignatureOnLoad()` confirms the key belongs to a registered contributor.
- On no key: L1930 renders *"Read-only mode: no digital signature in this browser…"*; on unregistered key: *"Read-only mode: your signature is not registered…"*.

**Therefore Julio's blocker is NOT a missing UI affordance — it is that he has no registered Edgar signing identity.** He is **absent from `dao_members.json`** (0 hits on name / email / "Almeida"; the J-block shows Junaid / June / Justine / Juliana, no Júlio), so `verifySignatureOnLoad()` lands him in view-only mode.

## Authority model confirmed (pre-flight)

Store writes are **signature-gated, not role-gated**:
- `sentiment_importer/app/controllers/dao_controller.rb` — Edgar verifies the **RSA signature**; the `[STORE ADD EVENT]` and `[RETAIL FIELD REPORT EVENT]` branches carry **no governor/role check** (only genuinely sensitive events, e.g. donation-mint, add a Governors-tab gate — comment at L486: *"Real authorization happens INSIDE the GAS…"*; L614 documents the donation-mint Governors-tab gate as the exception).
- `go_to_market/physical_stores/find_nearby_stores.gs` — `updateStoreStatus()` (L784) / `addNewStore()` (L984): `digital_signature` is *"optional but recommended"* (attribution, not enforcement); **no `Governor` reference anywhere in the 1567-line file**.
- `dapp_beta/scripts/permissions.js` — resolves `(action, public_key) → { allowed }` by **role intersection** (`rolesIntersect(have, required)`). There is **no per-contributor grant mechanism**, and **neither store page loads `permissions.js` at all** (both load only `routes.js`, `menu.js`, `tdg_balance.js`, `scripts/dao_members_cache.js`).

**Consequence:** granting Julio a `store.*` right in a manifest would be **cosmetic** — the capability has no role gate to open. What he lacks is the ability to *attribute* a write to himself, which is a **key**, not a permission.

## Units

### Unit 0 — Julio's signing identity (no code; member/governor action) — RESUME HERE
Gary's condition ("record works for Julio") is met the moment Julio has a registered key.
1. Julio opens `https://dapp.truesight.me/create_signature.html` (beta: `https://beta.dapp.truesight.me/create_signature.html`), generates a keypair in his browser, and registers email `davajhabib@outlook.com`.
2. He completes the `[EMAIL VERIFICATION EVENT]`; `tokenomics/…/tdg_identity_management/dao_members_cache_publisher.gs` then adds his key to `treasury-cache/dao_members.json` (activation trigger or daily cron).
3. Verify: `store_interaction_history.html` shows *"Signature verified — updates enabled."*; the edit form is interactive; a test remark lands in **DApp Remarks** attributed to his key.

**Acceptance:** Julio can edit a Hit List row's status/details and append a remark; both persist and are attributed. **No PR.**

### Unit 1 — (OPT-IN, small) declarative manifest entry for store writes
Only if Gary wants the manifest to be the *documented* source of truth (seed of the general system):
- `treasury-cache/permissions.json`: add `store.edit` + `store.remark_add` with `required_roles: ["member"]` (no regression for existing contributors) and record `grantable: true` for the future ACL.
- `dapp_beta/store_interaction_history.html` + `stores_nearby.html`: additional consult of `permissions.js` (member-allowed default → **no behaviour change**; declarative + future-grant-ready).
- Beta → prod per beta-first flow; **human-gated promote**.
- **Not required for Julio**; purely the seed for the general system.

## Deferred — full per-contributor ACL (5 PRs / 4 repos)
Reason: the ACL is a **UI-affordance layer only, not an enforcement boundary** for store writes (they are signature-gated). Building the general system to serve one consumer is the tail wagging the dog. Revisit when a **second** delegate or module appears.

## Authority routing (§5e)
- **§5c — GAS deploy is human-always.** Any GAS handler unit merges as code but is deployed by Gary, never by Sophia.
- **Out-of-scope merges routed, not assumed:** `sentiment_importer` (private) and `treasury-cache` (machine-owned API-only; a new `.github/workflows/*` validator is not a Sophia branch-edit class) → route to Gary/Envoy.

## §5d Pre-flight Completeness self-cert
✅ Pre-flight Completeness: no execution unit requires reading a file/state not already captured above.

## Resume tracker
| Unit | Advance | PR | Merged | Deployed |
|---|---|---|---|---|
| Unit 0 — Julio identity | (human, no PR) | n/a | n/a | n/a |
| Unit 1 — declarative manifest (opt-in) | `gate: beta review → human prod promote` | ☐ | ☐ | ☐ |

## Changelog
- 2026-11 — filed. Scope narrowed to UI slice on Gary's direct instruction; pre-flight established the slice already ships and the sole blocker is Julio's missing signing identity.
