# Discord adapter — typing indicator

Tracked in Discord channel **#show-typing** (`1548896014868676608`).
Parent design record: `plans/DISCORD_ADAPTER_PLAN.md`.

## Purpose

The Telegram adapter keeps a typing indicator alive while the brain is working; the
Discord adapter does not. Add a background typing loop to `app/discord_adapter.py`:
before `call_chat(...)` starts, POST the channel's typing state on a short interval and
stop the loop when the reply posts — mirroring the Telegram pattern.

## State

- 2026-09-14 — finding filed in the guild (Discord adapter has **no** typing indicator);
  Gary confirmed the idea is good.
- **RESUME HERE →** implement the typing loop (one PR) + unit tests, then UAT in
  **#show-typing**.
