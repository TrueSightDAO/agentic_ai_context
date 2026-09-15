"""Unit tests for the PR4c-b supervision drift gate (check_supervision).

Exercises the three drift shapes against synthetic fixtures so each rule is proven in
isolation: an orphan claim (hard error) and active-but-unclaimed / stale-claim (warnings).
Named with the `test_validate_handoff_manifest*` prefix so the existing CI path filter
covers it without a workflow edit.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validate_handoff_manifest import check_supervision  # noqa: E402

HEADER = (
    "| Plan file | Handoff title | Handoff date | Status | Telegram topic | "
    "message_thread_id | Auto-start | Resume tracker state | Last manifest update |"
)
SEPARATOR = "|---|---|---|---|---|---|---|---|---|"


def make_table(rows: list[str]) -> str:
    return "\n".join([HEADER, SEPARATOR, *rows])


def row(plan="PLAN_A.md", status="in progress", thread_id="1", **kw):
    return (
        f"| {plan} | Title | 2026-07-18 | {status} | [T](https://t.me/x/{thread_id}) | "
        f"{thread_id} | no | RESUME HERE = PR1 | 2026-07-18 |"
    )


def write_claims(tmp_path: Path, claims: list[dict]) -> Path:
    p = tmp_path / "active_supervision.json"
    p.write_text(json.dumps({"schema_version": 1, "claims": claims}), encoding="utf-8")
    return p


def test_orphan_claim_is_error(tmp_path):
    """A claim naming a plan absent from the manifest fails CI (author-fixable)."""
    text = make_table([row(plan="`plans/PLAN_A.md`")])
    sup = write_claims(
        tmp_path,
        [
            {
                "plan_file": "plans/GONE.md",
                "supervisor": "Envoy",
                "claimed_at": "2026-07-18T00:00:00Z",
            }
        ],
    )
    result = check_supervision(text, sup)
    assert not result.ok, result.errors
    assert any("orphan claim" in e for e in result.errors), result.errors


def test_matching_claim_is_clean(tmp_path):
    """A claim that lines up with a manifest row and is fresh -> no error."""
    text = make_table([row(plan="`plans/PLAN_A.md`", status="executing")])
    now = datetime(2026, 7, 18, 0, 30, tzinfo=timezone.utc)
    sup = write_claims(
        tmp_path,
        [
            {
                "plan_file": "plans/PLAN_A.md",
                "supervisor": "Envoy",
                "claimed_at": "2026-07-18T00:00:00Z",
            }
        ],
    )
    result = check_supervision(text, sup, now=now)
    assert result.ok, result.errors
    assert result.warnings == [], result.warnings


def test_active_row_without_claim_warns_not_errors(tmp_path):
    """An active handoff nobody claimed is a nudge, never a hard gate."""
    text = make_table([row(plan="`plans/PLAN_A.md`", status="executing")])
    sup = write_claims(tmp_path, [])
    result = check_supervision(text, sup)
    assert result.ok, result.errors
    assert any("no supervisor claim" in w for w in result.warnings), result.warnings


def test_terminal_row_without_claim_is_silent(tmp_path):
    """A done/awaiting-kickoff row legitimately carries no claim -> no warning."""
    text = make_table(
        [
            row(plan="`plans/DONE.md`", status="**COMPLETE — merged**", thread_id="1"),
            row(plan="`plans/NEW.md`", status="new — awaiting kickoff", thread_id="2"),
        ]
    )
    sup = write_claims(tmp_path, [])
    result = check_supervision(text, sup)
    assert result.ok, result.errors
    assert result.warnings == [], result.warnings


def test_stale_claim_warns(tmp_path):
    """A claim older than SUPERVISION_STALE_MINUTES is surfaced as stale."""
    text = make_table([row(plan="`plans/PLAN_A.md`", status="executing")])
    now = datetime(2026, 7, 18, 5, 0, tzinfo=timezone.utc)  # 5h after claim
    sup = write_claims(
        tmp_path,
        [
            {
                "plan_file": "plans/PLAN_A.md",
                "supervisor": "Envoy",
                "claimed_at": (now - timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        ],
    )
    result = check_supervision(text, sup, now=now)
    assert result.ok, result.errors
    assert any("STALE" in w for w in result.warnings), result.warnings


def test_missing_claims_file_is_not_an_error(tmp_path):
    """No active_supervision.json -> nothing to cross-reference (fail-soft)."""
    text = make_table([row(plan="`plans/PLAN_A.md`", status="executing")])
    result = check_supervision(text, tmp_path / "does_not_exist.json")
    assert result.ok, result.errors
    assert result.warnings == [], result.warnings


def test_anchor_plan_key_matches_claim(tmp_path):
    """OPEN_FOLLOWUPS.md#anchor form is compared on the same normalized key."""
    text = make_table([row(plan="`OPEN_FOLLOWUPS.md#some-anchor`", status="executing")])
    now = datetime(2026, 7, 18, 0, 30, tzinfo=timezone.utc)
    sup = write_claims(
        tmp_path,
        [
            {
                "plan_file": "OPEN_FOLLOWUPS.md#some-anchor",
                "supervisor": "Envoy",
                "claimed_at": "2026-07-18T00:00:00Z",
            }
        ],
    )
    result = check_supervision(text, sup, now=now)
    assert result.ok, result.errors
    assert not any("no supervisor claim" in w for w in result.warnings), result.warnings
