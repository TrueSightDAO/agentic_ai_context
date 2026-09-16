# Brain tier-awareness (MEMBER replies on Discord)

Tracked in Discord channel **#brain-tier-awareness** (`1549762040518672419`).
Parent plan: `plans/DISCORD_MEMBER_TIER.md`. Umbrella: `plans/DISCORD_ADAPTER_PLAN.md`.
Filed from `OPEN_FOLLOWUPS.md` -> "Discord: enable member *replies* - requires the brain to be tier-aware".

## 0. Locked decisions (to confirm with governor before PR1)

- **D1** - Transport for member identity: (a) an explicit, adapter-set `author_role` field on the
  `/chat-blocking` request, gated so only the adapter can set it; or (b) a member-scoped credential.
  Default proposal: **(a)** (lower blast radius), with (b) as a later hardening.
- **D2** - Member capability = read-only "ask / research / draft". Members never issue instructions
  and never authorize WRITE/ADMIN actions.
- **D3** - Governors remain the sole instruction source; no behavioural change for governor turns.

## 1. Purpose

Let a **resolved MEMBER** Discord sender get a tier-appropriate (non-instruction) reply **without
inheriting governor authority**. Today MEMBER is a read tier: recognised and attributed, never replied to.

## 2. Verified state (read from deployed code on the autopilot box, 2026-09-16)

- `app/discord_adapter.py::author_role()` returns `governor` / `member` / `guest`:
  1. env `DISCORD_ALLOWED_USER_IDS` -> governor
  2. sheet col G -> email -> Governors cache -> governor
  3. col G bound to a **real contributor whose col D email is non-empty**, or env `DISCORD_MEMBER_USER_IDS` -> member
  4. else guest
  (Note: a col-G binding alone, with a blank col-D email, resolves to **guest**, not member -
  the runbook text says otherwise; the code is authoritative.)
- `handle_message()`: `if role != "governor": log_observed_message(...); return` - no dispatch, no reply.
- The adapter authenticates a turn by minting a short-lived JWT **for the governor's public key**
  (`create_jwt(public_key)`) and POSTing to `/chat-blocking` with `Authorization: Bearer` + `X-Session-Id`.
- `/chat-blocking` (`app/main.py` ~L4624) -> `verify_payload(...)` (signed) or `verify_jwt(...)` ->
  `_chat_blocking_turn(session_id, user_message, public_key)`. Identity is derived **purely from
  `public_key`**; `governor_name` gates every WRITE tool (`app/main.py` ~L1905-1935). So a member turn
  riding the governor JWT would be treated as the governor -> **privilege escalation**.
- `app/policy.py`: `Role.MEMBER` exists between GUEST and GOVERNOR; `evaluate()` = READ open to all,
  WRITE/ADMIN governor-only.

## 3. Transport options (D1)

- **(a) Explicit role field.** Adapter sets `author_role` (payload field or `X-Author-Role` header) on
  the `/chat-blocking` request; brain gates on it. Requires the field to be trustable - only the adapter
  may set it (signed payload, or a shared-secret header consumed server-side).
- **(b) Member-scoped credential.** Mint a distinct member keypair / scoped token so the brain
  distinguishes a member turn cryptographically. Stronger, larger (key lifecycle for members).

## 4. Brain-side gate

On a Discord-originated turn, apply `{guest < member < governor}` **in the brain**, instead of assuming
"arrived on the governor key => governor". Member turns may converse / research / draft (READ tools)
but may **not** issue instructions or authorize actions.

## 5. Adapter-side dispatch

Flip the `if role != "governor"` guard so the read-only ask/research class is dispatched to members,
keeping governors the sole instruction source.

## 6. Tests

- Unit: role resolution (governor / member / guest) incl. the col-G-with-blank-email -> guest edge.
- Unit: brain gate - a member-role turn is denied every WRITE/ADMIN tool and allowed READ tools.
- Unit: a member turn can never be minted on the governor credential.
- Integration: real handler with side-effects mocked - member turn dispatches a reply; governor unaffected.

## 7. UAT

Live pass in **#brain-tier-awareness**: a bound member sends a message and receives a read-only reply;
a member attempt at a write-class action is refused; a governor turn is unchanged.

## 8. Execution (ONE PR PER TURN)

- PR1 - transport (D1) + trusted-setter wiring.
- PR2 - brain gate (`{guest < member < governor}`) + tests.
- PR3 - adapter dispatch of the read-only class + tests.
- Then UAT in #brain-tier-awareness.

**Gate:** this touches the identity/authority core. Open PRs only; **no production deploy** without an
explicit governor GO.
