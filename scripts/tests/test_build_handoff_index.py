"""Unit tests for build_handoff_index.py — the §8 machine-readable manifest mirror.

One focused test per behaviour: state mapping (the §2 enum), tolerant table reading
(ragmented manifest), thread-id resolution, the emitted shape, and the drift gate.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import build_handoff_index as b  # noqa: E402
import validate_handoff_manifest as v  # noqa: E402

HEADER = (
    "| Plan file | Handoff title | Handoff date | Status | Telegram topic | "
    "message_thread_id | Auto-start | Resume tracker state | Last manifest update |"
)
SEPARATOR = "|---|---|---|---|---|---|---|---|---|"


def row(
    plan="`plans/PLAN_A.md`",
    title="Title A",
    date="2026-09-15",
    status="in progress",
    topic="[A](https://t.me/c/3919341801/1111)",
    thread_id="1111",
    auto_start="no",
    resume="RESUME HERE = PR1",
    updated="2026-09-15",
):
    return (
        f"| {plan} | {title} | {date} | {status} | {topic} | {thread_id} | "
        f"{auto_start} | {resume} | {updated} |"
    )


def manifest(*rows: str) -> str:
    return "\n".join([HEADER, SEPARATOR, *rows]) + "\n"


def test_cell_splitting_is_shared_with_validator():
    # The builder must read cells exactly as the validator does.
    assert b.split_row is v.split_row


def test_state_enum_matches_supervisor_loop_s2():
    assert b.STATE_ENUM == [
        "awaiting_kickoff",
        "executing",
        "paused_at_gate",
        "sophia_uat",
        "envoy_uat",
        "human_uat_ready",
        "prod_merge",
        "blocked_on_human",
        "failed",
        "done",
        "stale",
    ]


def test_derive_state_maps_known_statuses():
    cases = {
        "in progress": "executing",
        "GO-ready — blocked on Gate D (human: prod merge)": "blocked_on_human",
        "GO-ready — blocked on Gate D": "paused_at_gate",
        "completed": "done",
        "\u2705 COMPLETED 2026-09-14 — merged": "done",
        "new — awaiting kickoff": "awaiting_kickoff",
        "stale": "stale",
        "failed": "failed",
    }
    for status, expected in cases.items():
        state, note = b.derive_state(status)
        assert state == expected, (status, state, expected)
        assert note == ""


def test_derive_state_empty_is_unknown_with_note():
    state, note = b.derive_state("")
    assert state == "unknown" and "empty" in note


def test_build_index_thread_id_value_and_source():
    idx = b.build_index(manifest(row(thread_id="2222")), "handoffs/HANDOFF_MANIFEST.md")
    h = idx["handoffs"][0]
    assert h["telegram_thread_id"] == "2222"
    assert h["telegram_thread_id_source"] == "message_thread_id"


def test_build_index_thread_id_falls_back_to_topic_last_number():
    # A bare-number topic cell "(this thread 24442)".
    r = row(topic="(this thread 24442)", thread_id="—")
    idx = b.build_index(manifest(r), "x")
    assert idx["handoffs"][0]["telegram_thread_id"] == "24442"
    assert idx["handoffs"][0]["telegram_thread_id_source"] == "telegram_topic"


def test_needs_verification_thread_id_is_flagged_not_used():
    r = row(
        topic="[A](https://t.me/c/3919341801/2622)",
        thread_id="NEEDS VERIFICATION (2622 — reused, see PR)",
    )
    idx = b.build_index(manifest(r), "x")
    h = idx["handoffs"][0]
    assert h["telegram_thread_id_needs_verification"] is True
    assert h["telegram_thread_id"] == "2622"  # falls back to the topic's last number


def test_build_index_tolerates_ragged_and_ragged_segmented_manifest():
    # A blank line splits the table (as in the real manifest at line 64) and one
    # row is ragged (unescaped '|' in prose -> extra cell).
    ragged = (
        "| `plans/PLAN_B.md` | Title B | 2026-09-15 | in progress | "
        "[B](https://t.me/c/3919341801/2222) | 2222 | no | a | b | extra |"
    )
    text = manifest(row(thread_id="1111")) + "\n" + ragged + "\n"
    idx = b.build_index(text, "x")
    plans = [h["plan_file"] for h in idx["handoffs"]]
    assert plans == ["`plans/PLAN_A.md`", "`plans/PLAN_B.md`"]
    assert any("ragged" in w for w in idx["warnings"])
    assert any("blank line splits" in w for w in idx["warnings"])


def test_counts_by_state_sums_to_handoff_count():
    text = manifest(
        row(plan="`plans/A.md`", status="in progress"),
        row(plan="`plans/B.md`", status="completed"),
        row(plan="`plans/C.md`", status="new — awaiting kickoff"),
    )
    idx = b.build_index(text, "x")
    assert idx["handoff_count"] == 3
    assert sum(idx["counts_by_state"].values()) == 3
    assert idx["counts_by_state"]["executing"] == 1
    assert idx["counts_by_state"]["done"] == 1
    assert idx["counts_by_state"]["awaiting_kickoff"] == 1


def test_build_index_is_deterministic_apart_from_generated_at(tmp_path):
    text = manifest(row(thread_id="1111"))
    a = b.build_index(text, "x")
    c = b.build_index(text, "x")
    a.pop("generated_at")
    c.pop("generated_at")
    assert a == c


def test_check_index_passes_when_in_sync(tmp_path):
    text = manifest(row(thread_id="1111"))
    index = b.build_index(text, "handoffs/HANDOFF_MANIFEST.md")
    p = tmp_path / "index.json"
    p.write_text(b.render(index), encoding="utf-8")
    result = v.check_index(text, p)
    assert result.ok, result.errors


def test_check_index_detects_added_handoff(tmp_path):
    before = manifest(row(plan="`plans/A.md`", thread_id="1111"))
    index = b.build_index(before, "x")
    p = tmp_path / "index.json"
    p.write_text(b.render(index), encoding="utf-8")
    after = manifest(
        row(plan="`plans/A.md`", thread_id="1111"),
        row(
            plan="`plans/B.md`",
            thread_id="2222",
            topic="[B](https://t.me/c/3919341801/2222)",
        ),
    )
    result = v.check_index(after, p)
    assert not result.ok
    assert any("missing handoff" in e for e in result.errors)


def test_check_index_detects_field_change(tmp_path):
    text = manifest(row(thread_id="1111", status="in progress"))
    index = b.build_index(text, "x")
    p = tmp_path / "index.json"
    p.write_text(b.render(index), encoding="utf-8")
    changed = manifest(row(thread_id="1111", status="completed"))
    result = v.check_index(changed, p)
    assert not result.ok
    assert any("differ" in e or "drift" in e for e in result.errors)


def test_check_index_missing_file_is_error(tmp_path):
    result = v.check_index(manifest(row()), tmp_path / "absent.json")
    assert not result.ok
    assert any("index not found" in e for e in result.errors)


def test_committed_index_matches_real_manifest():
    """The committed handoffs/index.json must mirror the real manifest (no drift)."""
    root = Path(__file__).resolve().parent.parent.parent
    manifest_text = (root / "handoffs" / "HANDOFF_MANIFEST.md").read_text(
        encoding="utf-8"
    )
    result = v.check_index(manifest_text, root / "handoffs" / "index.json")
    assert result.ok, result.errors
