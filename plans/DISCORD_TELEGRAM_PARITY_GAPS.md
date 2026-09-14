# Discord adapter — parity gaps vs Telegram (prioritized)

Diffed `app/discord_adapter.py` (674 lines) against `app/telegram_adapter.py` (2719 lines)
function-by-function on 2026-09-14. Discord already has: mention-gate, governor resolution
(env allowlist + sheet-bound email fallback), basic send, `log_observed_message`, and
`post_typing` (just added). Everything below is present in Telegram and absent in Discord.

## Tier 1 — directly caused tonight's confusion, fix first

1. **Live progress visibility during long turns.** Telegram shows "🔄 Thinking… (round N)",
   "⚙️ ssh run …", etc. as the turn progresses (`call_chat_with_progress`,
   `_run_turn_with_auto_advance`, `_is_progress_query`/`_fetch_progress_snapshot`). Discord has
   nothing between "dispatching turn" and the final reply — this is almost certainly why Gary
   repeatedly thought she'd "stopped responding" tonight when she was actually mid-turn.
   Even a simplified version (edit one message in place with the current round number, using
   Discord's message-edit endpoint) would close most of this gap.
2. **Attachment / file handling.** `extract_attachment_file_id`, `extract_voice_file_id`,
   `download_telegram_file`, `_auto_process_attachment` (HEIC/photo/document auto-processing,
   OCR, EXIF/GPS extraction). Discord currently can't receive or act on any file at all — a
   hard functional gap, not just UX.
3. **Message edit support.** `edit_message_text` — needed for #1 above (editing a progress
   message in place) and generally useful (e.g. correcting a reply without re-posting).

## Tier 2 — real functionality gaps, second wave

4. **Voice message input/output** — `_handle_voice_reply`, `send_voice`, `send_voice_action`.
5. **Per-channel always-respond override** — mirrors `_should_always_respond`
   (`TELEGRAM_ALWAYS_RESPOND_CHAT_IDS`, shipped tonight on the Telegram side, PR #417). Discord
   has no equivalent knob yet.
6. **Reaction-based go-signal** — `reaction_emoji_verdict`, `_reaction_reactor_authorized`,
   `handle_message_reaction`, `_maybe_resume_from_reaction`. Discord supports reactions natively
   (same gateway event shape as Telegram's), should be a fairly direct port.
7. **`/verify` binding flow** — `_maybe_handle_verification`, so a new Discord user can bind
   their account without a governor manually seeding a sheet row.

## Tier 3 — lower priority / evaluate need before building

8. **Handoff/Exec-plan auto-advance mechanics** (`_handoff_plan_and_auto_start_for_thread`,
   `_looks_like_go_signal`, `_handoff_prefix`, etc.) — evaluate whether Exec roadmaps should ever
   run on Discord at all before porting this; may be intentionally Telegram-only.
9. **Slash-style commands** (`_handle_research_command`, `_handle_reset`, `_handle_ship_command`)
   — Discord has native slash commands, which would be a cleaner reimplementation than porting
   Telegram's text-command parsing verbatim.
10. **Interactive components** (`send_message_with_keyboard`/`answer_callback_query` →
    Discord's buttons/select-menus) — different API shape, not a direct port.
11. **Deploy-complete notifications** (`send_deploy_notification`) — decide which channel should
    receive these, if any.
12. **Markdown conversion** (`markdown_to_telegram_html`) — lower urgency since Discord's native
    markdown is closer to standard, but worth a pass for edge cases (tables, etc. render
    differently).

## Process note

One PR per turn, same convention as every other roadmap this session — work down the list in
priority order, Tier 1 first. Each item should get its own PR/turn rather than one giant change.
