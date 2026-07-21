"""Unit tests for validate_handoff_manifest.py — one fixture per rule.

Each test builds a minimal markdown table (not the real Manifest — see
test_validate_handoff_manifest_integration.py for that) so each rule can be
exercised in isolation, valid case and broken case.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validate_handoff_manifest import validate  # noqa: E402

HEADER = (
    "| Plan file | Handoff title | Handoff date | Status | Telegram topic | "
    "message_thread_id | Resume tracker state | Last manifest update |"
)
SEPARATOR = "|---|---|---|---|---|---|---|---|"


def make_table(rows: list[str]) -> str:
    return "\n".join([HEADER, SEPARATOR, *rows])


def row(
    plan="PLAN_A.md",
    title="Title A",
    date="2026-07-18",
    status="in progress",
    topic="[Topic A](https://t.me/x/1)",
    thread_id="1",
    resume="RESUME HERE = PR1",
    updated="2026-07-18",
):
    return f"| {plan} | {title} | {date} | {status} | {topic} | {thread_id} | {resume} | {updated} |"


def test_valid_table_passes():
    text = make_table(
        [
            row(plan="PLAN_A.md", thread_id="1", topic="[A](https://t.me/x/1)"),
            row(plan="PLAN_B.md", thread_id="2", topic="[B](https://t.me/x/2)"),
        ]
    )
    result = validate(text)
    assert result.ok, result.errors
    assert result.errors == []


def test_missing_column_detected():
    bad_header = (
        "| Plan file | Handoff title | Handoff date | Status | Telegram topic | "
        "Resume tracker state | Last manifest update |"
    )
    bad_sep = "|---|---|---|---|---|---|---|"
    text = "\n".join(
        [
            bad_header,
            bad_sep,
            "| PLAN_A.md | T | 2026-07-18 | in progress | — | RESUME HERE | 2026-07-18 |",
        ]
    )
    result = validate(text)
    assert not result.ok
    assert any("message_thread_id" in e for e in result.errors)


def test_duplicate_plan_file_detected():
    text = make_table(
        [
            row(plan="PLAN_A.md", thread_id="1", topic="[A](https://t.me/x/1)"),
            row(plan="PLAN_A.md", thread_id="2", topic="[A2](https://t.me/x/2)"),
        ]
    )
    result = validate(text)
    assert not result.ok
    assert any("Duplicate" in e and "PLAN_A.md" in e for e in result.errors)


def test_unknown_status_value_warns_not_errors():
    text = make_table([row(status="frobnicated")])
    result = validate(text)
    assert result.ok  # unknown status is a warning, not a hard failure
    assert any("frobnicated" in w for w in result.warnings)


def test_telegram_topic_without_thread_id_is_error():
    text = make_table([row(topic="[A](https://t.me/x/1)", thread_id="—")])
    result = validate(text)
    assert not result.ok
    assert any("both-or-neither" in e for e in result.errors)


def test_thread_id_without_topic_is_error():
    text = make_table([row(topic="—", thread_id="1")])
    result = validate(text)
    assert not result.ok
    assert any("both-or-neither" in e for e in result.errors)


def test_both_empty_is_fine():
    text = make_table([row(topic="—", thread_id="—")])
    result = validate(text)
    assert result.ok, result.errors


def test_duplicate_thread_id_across_plans_detected():
    text = make_table(
        [
            row(plan="PLAN_A.md", topic="[A](https://t.me/x/9)", thread_id="9"),
            row(plan="PLAN_B.md", topic="[B](https://t.me/x/9)", thread_id="9"),
        ]
    )
    result = validate(text)
    assert not result.ok
    assert any("reused across multiple plans" in e for e in result.errors)


def test_needs_verification_placeholder_does_not_trip_duplicate_or_both_or_neither():
    text = make_table(
        [
            row(
                plan="PLAN_A.md",
                topic="[A](https://t.me/x/2622)",
                thread_id="NEEDS VERIFICATION (2622 — reused, see PR)",
            ),
            row(
                plan="PLAN_B.md",
                topic="[B](https://t.me/x/2622)",
                thread_id="NEEDS VERIFICATION (2622 — reused, see PR)",
            ),
        ]
    )
    result = validate(text)
    assert result.ok, result.errors  # flagged for humans, not a CI failure


def test_empty_plan_file_cell_is_error():
    text = make_table([row(plan="—")])
    result = validate(text)
    assert not result.ok
    assert any("empty 'Plan file'" in e for e in result.errors)


def test_no_table_found_is_error():
    text = "# Just a heading\n\nNo table here.\n"
    result = validate(text)
    assert not result.ok
    assert any("No markdown table" in e for e in result.errors)
