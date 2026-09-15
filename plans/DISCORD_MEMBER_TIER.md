# Discord adapter — MEMBER-tier interaction

Tracked in Discord channel **#member-tier** (`962081045044424774`).
Parent design record: `plans/DISCORD_ADAPTER_PLAN.md`.

## Purpose

Enable **actual MEMBER-tier interaction** on Discord. Today the tier model is effectively
binary: a governor gets a reply, everyone else gets nothing.

- `app/policy.py` already defines `Role.MEMBER` (between `GUEST` and `GOVERNOR`).
- The identity binding already resolves a sheet-bound contributor to **MEMBER**.
- **But** `discord_adapter.handle_message` only *replies* to **GOVERNOR**-role senders — a
  resolved MEMBER is recognised (logged as context) yet receives no reply.

Close that gap: let a resolved **MEMBER** sender get a tier-appropriate (non-instruction,
data-only) reply, so "member level interaction in Discord" actually exists.

## State

- 2026-09-15 — Gary confirmed this is a distinct task and scoped the channel to it. The
  chat-blocking timeout/429 discussion that had been sitting in this channel is
  re-referenced to `plans/DISCORD_ADAPTER_BUGS.md`.
- **RESUME HERE →** design the MEMBER reply path (brain tier-awareness + adapter dispatch,
  one PR) + tests, then UAT in **#member-tier**.
