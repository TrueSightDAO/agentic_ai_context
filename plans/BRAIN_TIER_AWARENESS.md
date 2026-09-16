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
- **D4** (added 2026-09-16, governor direction) - **Sentinel is its own identity tier, distinct from
  governor, but carries governor-tier RIGHTS** under this gate's WRITE/ADMIN policy check. Governor and
  sentinel are fundamentally different identity classes - one human, one bot - and must **not** be
  conflated for attribution/audit purposes: a sentinel-originated turn must still be logged and attributed
  as **sentinel** (e.g. "Claude Anthropic", "Sophia"), never silently relabeled `governor` in logs or
  `governor_name`. What D4 grants is the *authorization level* (able to pass the same WRITE/ADMIN policy
  check a governor turn passes), not the *identity label*. Sentinels are the DAO's AI-agent contributors
  (`Is Sentinel`=TRUE in "Contributors contact information" col W - e.g. Claude Anthropic, Deep Seek,
  Kimi, Sophia herself); they already carry elevated standing elsewhere (editor access independent of
  formal governorship, per `GOVERNOR_SHEET_PERMISSION_SYNC_PLAN.md`). `author_role()` currently has **no
  sentinel check at all** (verified 2026-09-16, see §2) - a sentinel's Discord account would silently
  resolve to member or guest today. PR2 must add an explicit sentinel check (e.g. a col-W lookup analogous
  to the existing col-G governor lookup, or a `DISCORD_SENTINEL_USER_IDS` env allowlist analogous to
  `DISCORD_MEMBER_USER_IDS`), returning a **distinct `sentinel` role** (not `governor`) that
  `app/policy.py::evaluate()` authorizes at the same WRITE/ADMIN level as governor. This likely means
  `Role.SENTINEL` alongside (not aliased to) `Role.GOVERNOR` in the rights hierarchy - exact code shape is
  Sophia's call in PR2, but the label must never collapse into `governor`.

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
- **Gap (drives D4):** `author_role()` has no notion of "sentinel" at all - it only checks the env
  governor allowlist, the col-G->Governors-cache binding, and the member fallback. A sentinel's Discord
  account, if not separately on `DISCORD_ALLOWED_USER_IDS` or bound to a governor email, would resolve to
  `member` (bound + real email) or `guest` (unbound) - and today has no path to governor-equivalent
  rights at all, nor a distinct `sentinel` label. Must be closed in PR2.

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
- Unit: a sentinel-flagged Discord account resolves to a distinct **`sentinel`** role (never relabeled
  `governor`) and is authorized for WRITE/ADMIN at governor-equivalent rights (D4).
- Unit: a sentinel turn's audit/attribution stays `sentinel` (e.g. `governor_name`/log fields never
  silently read "governor" for a bot-originated turn).
- Unit: brain gate - a member-role turn is denied every WRITE/ADMIN tool and allowed READ tools.
- Unit: a member turn can never be minted on the governor credential.
- Integration: real handler with side-effects mocked - member turn dispatches a reply; governor unaffected.

## 7. UAT

Live pass in **#brain-tier-awareness**: a bound member sends a message and receives a read-only reply;
a member attempt at a write-class action is refused; a governor turn is unchanged.

## 8. Execution (ONE PR PER TURN)

- PR1 - transport (D1) + trusted-setter wiring. **MERGED #478** (signed `author_role` claim on JWT).
- PR2 - brain gate (`{guest < member < governor}`, plus `sentinel` at governor-equivalent rights) + tests.
  **Must include D4**: a distinct `sentinel` role (author_role() sentinel check, evaluated before the
  member fallback) authorized at governor-tier RIGHTS but never relabeled/attributed as `governor`.
  **MERGED #480** (2026-09-16, squash `08ea0973`): `Role.SENTINEL` (distinct, not aliased) +
  `has_governor_rights()`; `author_role()` sentinel check after governor / before member;
  `_run_tool_sync` WRITE/ADMIN gate accepts `("governor","sentinel")` and forces the asserted tier
  onto the resolved identity; `[GOVERNOR_IDENTITY:]` injected only for a true governor; sentinel turn
  attributed by its own name.
- PR3 - adapter dispatch of the read-only class + tests.
- Then UAT in #brain-tier-awareness.

## RESUME HERE

**Next unit: PR3** - flip the adapter's `if role != "governor": log_observed_message(); return` guard in
`app/discord_adapter.py::handle_message()` so a resolved **member** turn is dispatched to the brain
(read-only ask/research class) instead of only being observed. Governor + sentinel turns keep full
authority; member turns must be denied every WRITE/ADMIN tool by the PR2 gate. Add tests + integration
handler test with side-effects mocked. Open PR + merge (no prod deploy); then UAT in #brain-tier-awareness.

PR2 note for PR3: a sentinel/member turn already carries `author_role` + `author_name` through the
`/chat-blocking` + `/chat` paths (PR2), so PR3 only needs to stop dropping non-governor turns.

**Gate:** this touches the identity/authority core. Open PRs only; **no production deploy** without an
explicit governor GO.
