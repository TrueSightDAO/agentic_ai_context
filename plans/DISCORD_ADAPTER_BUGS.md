# Discord adapter — bug supervision

Tracked in Discord channel **#adapter-bugs** (`1549118558955634819`).
Parent design record: `plans/DISCORD_ADAPTER_PLAN.md`.

## Scope

Standing channel for Discord-adapter (and cross-adapter) bug findings and their fixes.
One finding = one PR; this channel tracks state across findings.

## Open items

- **Stale "...needs approval — open the DApp..." prompt string** — *fixed in production*
  2026-09-14 (present in both adapters; removed). See also #dapp-chat-approval-leak.
- **Discord resume-registry re-writes the same entries repeatedly** —
  `_discord_resume_awaiting.json` churns on every loop tick (journalctl). Investigate.
- **Chat-blocking timeout / 429 storm** *(re-referenced here from #member-tier, where it was
  mis-filed)* — a live governor turn produced 10× Discord 429s in ~40 s against the same
  message; `call_chat` timeout is 180 s. Fix direction: immediate ack reaction + raise
  `_CHAT_TIMEOUT` + edit-in-place progress. Mirrors the OPEN_FOLLOWUPS.md "429 storm" item.

## State

- **RESUME HERE →** take the 429/timeout item and the resume-registry rewrite, one PR each.
