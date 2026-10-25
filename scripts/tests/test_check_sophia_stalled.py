"""Unit tests for check_sophia_stalled.py — the per-thread/channel staleness check
supervisor runs on every mention-trigger wake."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import check_sophia_stalled as m

SOPHIA = m.SOPHIA_TELEGRAM_BOT_ID
GOV = 2102593402
THREAD = 41950
CHANNEL = 1559700152510578769
NOW = datetime(2026, 10, 21, 12, 0, 0, tzinfo=timezone.utc)


def write_messages(path: Path, *records):
    with path.open("a") as fh:
        for record in records:
            fh.write(json.dumps(record) + "\n")


def sophia_msg(thread_id=THREAD, minutes_ago=0, **overrides):
    record = {
        "update_id": 1,
        "message_id": 500,
        "chat_id": -1003919341801,
        "thread_id": thread_id,
        "from_id": SOPHIA,
        "from_username": "truesight_autopilot_bot",
        "date": int((NOW - timedelta(minutes=minutes_ago)).timestamp()),
        "text": "working on it",
    }
    record.update(overrides)
    return record


class FakeDiscordResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = [] if payload is None else payload

    def json(self):
        return self._payload


def discord_msg(author_id=m.SOPHIA_DISCORD_BOT_ID, minutes_ago=0):
    timestamp = (NOW - timedelta(minutes=minutes_ago)).isoformat()
    return {"id": "1", "author": {"id": str(author_id)}, "timestamp": timestamp}


# --- argument validation ----------------------------------------------------
def test_requires_exactly_one_target(tmp_path):
    with pytest.raises(ValueError):
        m.is_sophia_stalled(messages_path=tmp_path / "messages.jsonl")
    with pytest.raises(ValueError):
        m.is_sophia_stalled(
            telegram_thread_id=THREAD,
            discord_channel_id=CHANNEL,
            messages_path=tmp_path / "messages.jsonl",
        )


# --- Telegram half -----------------------------------------------------------
def test_recent_sophia_message_is_not_stalled(tmp_path):
    messages = tmp_path / "messages.jsonl"
    write_messages(messages, sophia_msg(minutes_ago=2))
    assert not m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


def test_old_sophia_message_is_stalled(tmp_path):
    messages = tmp_path / "messages.jsonl"
    write_messages(messages, sophia_msg(minutes_ago=6))
    assert m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


def test_default_threshold_is_five_minutes(tmp_path):
    """Gary, 2026-10-21: 'if 5 minutes no logs from Sophia ... then is stalled for sure.'"""
    messages = tmp_path / "messages.jsonl"
    write_messages(messages, sophia_msg(minutes_ago=5.5))
    assert m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )
    write_messages(messages, sophia_msg(minutes_ago=4.9))
    assert not m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


def test_custom_threshold_is_respected(tmp_path):
    messages = tmp_path / "messages.jsonl"
    write_messages(messages, sophia_msg(minutes_ago=8))
    assert not m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, threshold_minutes=10, now=NOW
    )


def test_no_sophia_message_ever_is_stalled(tmp_path):
    messages = tmp_path / "messages.jsonl"
    assert m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


def test_governor_messages_in_the_thread_do_not_count_as_sophia_activity(tmp_path):
    messages = tmp_path / "messages.jsonl"
    write_messages(messages, sophia_msg(from_id=GOV, from_username="garyjob", minutes_ago=0))
    assert m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


def test_sophia_message_in_a_different_thread_does_not_count(tmp_path):
    messages = tmp_path / "messages.jsonl"
    write_messages(messages, sophia_msg(thread_id=999999, minutes_ago=0))
    assert m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


def test_uses_the_most_recent_of_several_sophia_messages(tmp_path):
    messages = tmp_path / "messages.jsonl"
    write_messages(
        messages,
        sophia_msg(minutes_ago=20),
        sophia_msg(minutes_ago=2),  # most recent -- should win
        sophia_msg(minutes_ago=15),
    )
    assert not m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


def test_unparseable_line_is_skipped_not_fatal(tmp_path):
    messages = tmp_path / "messages.jsonl"
    messages.write_text("not json at all\n")
    write_messages(messages, sophia_msg(minutes_ago=1))
    assert not m.is_sophia_stalled(
        telegram_thread_id=THREAD, messages_path=messages, now=NOW
    )


# --- Discord half -------------------------------------------------------------
def test_recent_sophia_discord_message_is_not_stalled():
    http = lambda *a, **kw: FakeDiscordResponse(200, [discord_msg(minutes_ago=2)])
    assert not m.is_sophia_stalled(
        discord_channel_id=CHANNEL,
        discord_token="tok",
        discord_http_get=http,
        now=NOW,
    )


def test_old_sophia_discord_message_is_stalled():
    http = lambda *a, **kw: FakeDiscordResponse(200, [discord_msg(minutes_ago=10)])
    assert m.is_sophia_stalled(
        discord_channel_id=CHANNEL,
        discord_token="tok",
        discord_http_get=http,
        now=NOW,
    )


def test_discord_messages_from_others_do_not_count():
    http = lambda *a, **kw: FakeDiscordResponse(
        200, [discord_msg(author_id=999999, minutes_ago=0)]
    )
    assert m.is_sophia_stalled(
        discord_channel_id=CHANNEL,
        discord_token="tok",
        discord_http_get=http,
        now=NOW,
    )


def test_no_discord_token_fails_toward_caution():
    assert m.is_sophia_stalled(
        discord_channel_id=CHANNEL, discord_token=None, discord_http_get=lambda *a, **kw: None
    )


def test_discord_non_200_fails_toward_caution():
    http = lambda *a, **kw: FakeDiscordResponse(500, {})
    assert m.is_sophia_stalled(
        discord_channel_id=CHANNEL,
        discord_token="tok",
        discord_http_get=http,
        now=NOW,
    )


def test_discord_http_exception_fails_toward_caution():
    def raising(*a, **kw):
        raise m.requests.RequestException("network down")

    assert m.is_sophia_stalled(
        discord_channel_id=CHANNEL,
        discord_token="tok",
        discord_http_get=raising,
        now=NOW,
    )


# --- CLI ------------------------------------------------------------------------
def test_cli_prints_true_and_exits_1_when_stalled(tmp_path, capsys):
    messages = tmp_path / "messages.jsonl"
    rc = m.main(["--telegram-thread-id", str(THREAD), "--messages-path", str(messages)])
    assert rc == 1
    assert capsys.readouterr().out.strip() == "true"


def test_cli_prints_false_and_exits_0_when_not_stalled(tmp_path, capsys):
    messages = tmp_path / "messages.jsonl"
    write_messages(messages, sophia_msg(minutes_ago=0, date=int(datetime.now(timezone.utc).timestamp())))
    rc = m.main(["--telegram-thread-id", str(THREAD), "--messages-path", str(messages)])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "false"


def test_cli_requires_exactly_one_target(tmp_path):
    with pytest.raises(SystemExit):
        m.main(["--messages-path", str(tmp_path / "messages.jsonl")])
