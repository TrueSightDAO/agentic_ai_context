"""Unit tests for build_handoff_index.py — the §8 machine-readable manifest mirror.

One focused test per behaviour: state mapping (the §2 enum), tolerant table reading
(ragmented manifest), thread-id resolution, the emitted shape, and the drift gate.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
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


# --- PR1a: status->state ordering (the "false all-clear" fix) ---------------


def test_human_uat_beats_complete():
    state, note = b.derive_state(
        "**build complete \u2014 awaiting governor UAT** (PR1\u2013PR5 merged/done)"
    )
    assert state == "human_uat_ready" and note == ""


def test_in_flight_marker_beats_terminal_words():
    assert (
        b.derive_state("**executing \u2014 PR1\u2013PR3 done + deployed**")[0]
        == "executing"
    )
    assert (
        b.derive_state("deployed \u2014 Tier-1 parity gaps in progress")[0]
        == "executing"
    )


def test_governor_uat_alias_maps_to_human_uat_ready():
    assert b.derive_state("awaiting governor UAT")[0] == "human_uat_ready"


def test_governor_named_blocker_is_human_gated():
    assert (
        b.derive_state("draft \u2014 awaiting governor review")[0] == "blocked_on_human"
    )
    assert (
        b.derive_state("active \u2014 first LINK pending Gary go")[0]
        == "blocked_on_human"
    )
    assert (
        b.derive_state("**GO-ready \u2014 blocked on Gate D** (Gary must `ssh` in)")[0]
        == "blocked_on_human"
    )


def test_prod_deploy_history_is_done_not_prod_merge():
    state, _ = b.derive_state(
        "**COMPLETE \u2014 PR1\u2013PR7 merged; PR7 prod deployed**"
    )
    assert state == "done"


# --- PR1b: Discord channel/thread linkage columns ---------------------------


def test_discord_columns_are_read_when_present():
    hdr = (
        "| Plan file | Handoff title | Handoff date | Status | Telegram topic | "
        "message_thread_id | Auto-start | Resume tracker state | Last manifest update | "
        "Discord channel id | Discord thread id |"
    )
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    body = (
        "| `plans/D.md` | Title D | 2026-09-15 | in progress | [D](https://t.me/c/1/1) | 1 | "
        "no | RESUME = PR1 | 2026-09-15 | 923012941937250375 | |"
    )
    idx = b.build_index("\n".join([hdr, sep, body]) + "\n", "x")
    h = idx["handoffs"][0]
    assert h["discord_channel_id"] == "923012941937250375"
    assert h["discord_thread_id"] in ("", None)


def test_discord_columns_absent_do_not_break_build():
    idx = b.build_index(manifest(row(thread_id="1111")), "x")
    h = idx["handoffs"][0]
    assert h["discord_channel_id"] in ("", None)
    assert h["telegram_thread_id"] == "1111"


# --- PR4b: active-supervision visibility (plan §2.6) ------------------------


def _sup(**claims):
    """Build a supervision map keyed by normalized plan path."""
    return {
        plan: {
            "supervisor": c.get("supervisor"),
            "claimed_at": c.get("claimed_at"),
            "note": c.get("note"),
        }
        for plan, c in claims.items()
    }


def test_unclaimed_handoff_emits_null_supervised_by():
    idx = b.build_index(manifest(row()), "x", {})
    assert idx["handoffs"][0]["supervised_by"] is None


def test_no_supervision_arg_defaults_to_unclaimed():
    idx = b.build_index(manifest(row()), "x")
    assert idx["handoffs"][0]["supervised_by"] is None


def test_claim_attaches_active_supervision_badge():
    sup = _sup(
        **{
            "plans/PLAN_A.md": {
                "supervisor": "envoy",
                "claimed_at": "2026-09-15T13:00:00Z",
                "note": "driving PR5 UAT",
            }
        }
    )
    now = datetime(2026, 9, 15, 13, 30, tzinfo=timezone.utc)
    entry = b.supervision_entry("`plans/PLAN_A.md`", sup, now)
    assert entry["supervisor"] == "envoy"
    assert entry["stale"] is False
    assert entry["age_minutes"] == 30
    assert entry["note"] == "driving PR5 UAT"


def test_claim_goes_stale_past_threshold():
    sup = _sup(
        **{
            "plans/PLAN_A.md": {
                "supervisor": "sophia",
                "claimed_at": "2026-09-15T13:00:00Z",
            }
        }
    )
    now = datetime(2026, 9, 15, 14, 5, tzinfo=timezone.utc)  # 65 min later
    entry = b.supervision_entry("plans/PLAN_A.md", sup, now)
    assert entry["stale"] is True
    assert entry["age_minutes"] == 65


def test_threshold_boundary_is_not_stale():
    sup = _sup(
        **{
            "plans/PLAN_A.md": {
                "supervisor": "envoy",
                "claimed_at": "2026-09-15T13:00:00Z",
            }
        }
    )
    now = datetime(2026, 9, 15, 14, 0, tzinfo=timezone.utc)  # exactly 60 min
    assert b.supervision_entry("plans/PLAN_A.md", sup, now)["stale"] is False


def test_unparseable_claimed_at_is_stale_not_trusted():
    sup = _sup(
        **{"plans/PLAN_A.md": {"supervisor": "envoy", "claimed_at": "not-a-date"}}
    )
    entry = b.supervision_entry("plans/PLAN_A.md", sup)
    assert entry["stale"] is True
    assert entry["age_minutes"] is None


def test_load_supervision_missing_file_is_empty(tmp_path):
    assert b.load_supervision(tmp_path / "nope.json") == {}


def test_load_supervision_none_path_is_empty():
    assert b.load_supervision(None) == {}


def test_load_supervision_malformed_is_empty(tmp_path):
    p = tmp_path / "active_supervision.json"
    p.write_text("{not valid json", encoding="utf-8")
    assert b.load_supervision(p) == {}


def test_load_supervision_normalizes_backticks(tmp_path):
    p = tmp_path / "active_supervision.json"
    p.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "claims": [
                    {
                        "plan_file": "`plans/PLAN_A.md`",
                        "supervisor": "envoy",
                        "claimed_at": "2026-09-15T13:00:00Z",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    sup = b.load_supervision(p)
    assert sup["plans/PLAN_A.md"]["supervisor"] == "envoy"


def test_strip_volatile_ignores_computed_supervision_fields():
    def idx(gen, stale, age):
        return {
            "generated_at": gen,
            "handoffs": [
                {
                    "plan_file": "`plans/A.md`",
                    "supervised_by": {
                        "supervisor": "envoy",
                        "claimed_at": "2026-09-15T13:00:00Z",
                        "note": None,
                        "stale": stale,
                        "age_minutes": age,
                    },
                }
            ],
        }

    assert b._strip_volatile(idx("T1", False, 5)) == b._strip_volatile(
        idx("T2", True, 90)
    )


def test_drift_gate_passes_when_only_clock_derived_fields_differ(tmp_path):
    # A committed index must not read as drift when rebuilt later, even though
    # supervised_by.stale flipped with the clock — the gate compares content.
    (tmp_path / "handoffs").mkdir()
    sup_path = tmp_path / "handoffs" / "active_supervision.json"
    sup_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "claims": [
                    {
                        "plan_file": "plans/PLAN_A.md",
                        "supervisor": "envoy",
                        "claimed_at": "2026-09-15T13:00:00Z",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    text = manifest(row())
    idx = b.build_index(text, "x", b.load_supervision(sup_path))
    assert idx["handoffs"][0]["supervised_by"]["supervisor"] == "envoy"
    (tmp_path / "handoffs" / "index.json").write_text(b.render(idx), encoding="utf-8")
    result = v.check_index(text, tmp_path / "handoffs" / "index.json")
    assert result.ok, result.errors
