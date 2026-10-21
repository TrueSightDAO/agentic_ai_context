#!/usr/bin/env python3
"""Check whether Sophia has gone quiet (stalled) in a specific thread/channel.

Called by `supervisor` every time it's woken (per the mention-trigger prompts in
`claude_telegram_monitor`'s `envoy_trigger` package — see
`plans/ENVOY_MENTION_TRIGGER_PLAN.md`), to answer one narrow, objective question:
**has Sophia posted anything in the thread/channel that triggered this wake within
the last N minutes?** If not, she's stalled.

Deliberately does NOT try to verify "is she truly done" — confirming a completion
claim actually holds (the PR is really merged, the deploy is really live) is
task-specific judgment that belongs with the supervising LLM looking at the actual
evidence, not something a generic script can know. This tool answers exactly the one
question it's built for: staleness, not correctness.

Per Gary (2026-10-21): "If 5 minutes no logs from Sophia on that channel or thread
then is stalled for sure." Threshold defaults to 5 minutes accordingly. No evidence
of her ever posting there at all is treated the same as stalled — the caution this
check exists for cuts the same way in both cases.

Usage:
    python3 scripts/check_sophia_stalled.py --telegram-thread-id 41950
    python3 scripts/check_sophia_stalled.py --discord-channel-id 1559700152510578769
    python3 scripts/check_sophia_stalled.py --telegram-thread-id 41950 --threshold-minutes 10

Prints exactly ``true`` or ``false`` to stdout. Exit code mirrors it (1 = stalled/true,
0 = not stalled/false) so it composes in shell conditionals too.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

SOPHIA_TELEGRAM_BOT_ID = 8217115914  # @truesight_autopilot_bot
SOPHIA_DISCORD_BOT_ID = 1548466367005458572  # sophia_truesight, DISCORD_ADAPTER_PLAN.md §2

DEFAULT_THRESHOLD_MINUTES = 5

DEFAULT_MESSAGES_PATH = Path("/opt/claude_workspace/claude_telegram_monitor/messages.jsonl")
DEFAULT_ENV_PATH = Path("/opt/claude_workspace/claude_telegram_monitor/.env")

HttpGet = Callable[..., Any]


def load_discord_token(env_path: Path = DEFAULT_ENV_PATH) -> str | None:
    if not env_path.exists():
        return None
    for line in env_path.read_text().splitlines():
        if line.startswith("DISCORD_BOT_TOKEN="):
            return line.split("=", 1)[1].strip()
    return None


def last_sophia_telegram_timestamp(
    thread_id: int, messages_path: Path = DEFAULT_MESSAGES_PATH
) -> datetime | None:
    """Most recent message FROM Sophia in this Telegram thread, or None if she has
    never posted there (per this log — the listener only sees activity since it
    joined; see claude_telegram_monitor's own documented limitation)."""
    if not messages_path.exists():
        return None

    latest: datetime | None = None
    with messages_path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("from_id") != SOPHIA_TELEGRAM_BOT_ID:
                continue
            if record.get("thread_id") != thread_id:
                continue
            date = record.get("date")
            if date is None:
                continue
            timestamp = datetime.fromtimestamp(date, tz=timezone.utc)
            if latest is None or timestamp > latest:
                latest = timestamp
    return latest


def last_sophia_discord_timestamp(
    channel_id: int, token: str, http_get: HttpGet | None = None
) -> datetime | None:
    """Most recent message FROM Sophia in this Discord channel (last 100 messages),
    or None if she isn't among them."""
    http_get = http_get or requests.get
    headers = {"Authorization": f"Bot {token}"}
    try:
        resp = http_get(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            headers=headers,
            params={"limit": 100},
            timeout=15,
        )
    except requests.RequestException:
        return None
    if getattr(resp, "status_code", None) != 200:
        return None

    latest: datetime | None = None
    for message in resp.json():
        author = message.get("author") or {}
        if str(author.get("id")) != str(SOPHIA_DISCORD_BOT_ID):
            continue
        raw_timestamp = message.get("timestamp")
        if not raw_timestamp:
            continue
        timestamp = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
        if latest is None or timestamp > latest:
            latest = timestamp
    return latest


def is_sophia_stalled(
    *,
    telegram_thread_id: int | None = None,
    discord_channel_id: int | None = None,
    threshold_minutes: int = DEFAULT_THRESHOLD_MINUTES,
    messages_path: Path = DEFAULT_MESSAGES_PATH,
    discord_token: str | None = None,
    discord_http_get: HttpGet | None = None,
    now: datetime | None = None,
) -> bool:
    """True if Sophia hasn't posted in the given thread/channel within
    ``threshold_minutes`` — or has never posted there at all. Exactly one of
    ``telegram_thread_id`` / ``discord_channel_id`` must be given.
    """
    if (telegram_thread_id is None) == (discord_channel_id is None):
        raise ValueError("pass exactly one of telegram_thread_id or discord_channel_id")

    now = now or datetime.now(timezone.utc)

    if telegram_thread_id is not None:
        last = last_sophia_telegram_timestamp(telegram_thread_id, messages_path)
    else:
        token = discord_token if discord_token is not None else load_discord_token()
        if not token:
            return True  # can't check at all -- fail toward caution, not false confidence
        last = last_sophia_discord_timestamp(discord_channel_id, token, discord_http_get)

    if last is None:
        return True  # no evidence she's ever worked here -- treated the same as stalled

    elapsed_minutes = (now - last).total_seconds() / 60.0
    return elapsed_minutes > threshold_minutes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--telegram-thread-id", type=int)
    parser.add_argument("--discord-channel-id", type=int)
    parser.add_argument(
        "--threshold-minutes", type=int, default=DEFAULT_THRESHOLD_MINUTES
    )
    parser.add_argument("--messages-path", type=Path, default=DEFAULT_MESSAGES_PATH)
    args = parser.parse_args(argv)

    if (args.telegram_thread_id is None) == (args.discord_channel_id is None):
        parser.error("pass exactly one of --telegram-thread-id or --discord-channel-id")

    stalled = is_sophia_stalled(
        telegram_thread_id=args.telegram_thread_id,
        discord_channel_id=args.discord_channel_id,
        threshold_minutes=args.threshold_minutes,
        messages_path=args.messages_path,
    )
    print("true" if stalled else "false")
    return 1 if stalled else 0


if __name__ == "__main__":
    raise SystemExit(main())
