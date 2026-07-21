"""Integration test: run the validator against the real, committed Manifest.

Unit tests exercise the rules against small synthetic fixtures. This test
proves the parser round-trips against the actual content in
handoffs/HANDOFF_MANIFEST.md — the same real-file check that would have
caught prior drift had it existed before the 2026-07-18 consolidation.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validate_handoff_manifest import default_manifest_path, validate  # noqa: E402


def test_real_manifest_has_no_hard_errors():
    manifest_path = default_manifest_path()
    assert manifest_path.exists(), f"expected manifest at {manifest_path}"

    text = manifest_path.read_text(encoding="utf-8")
    result = validate(text)

    assert result.ok, (
        "handoffs/HANDOFF_MANIFEST.md failed structural validation:\n"
        + "\n".join(result.errors)
    )


def test_real_manifest_known_needs_verification_rows_are_flagged_not_broken():
    """The three thread_id-2622 rows should be marked NEEDS VERIFICATION, not
    silently 'fixed' with a guessed value, and should not trip the duplicate
    check (they're intentionally excluded pending human confirmation)."""
    manifest_path = default_manifest_path()
    text = manifest_path.read_text(encoding="utf-8")
    result = validate(text)

    assert result.ok, result.errors
    assert "NEEDS VERIFICATION" in text
    assert text.count("NEEDS VERIFICATION") >= 3


def test_real_manifest_has_auto_start_column_defaulted_to_no():
    """No handoff is opted into Auto-start yet — every row should be 'no'
    until a plan author explicitly marks one 'yes'."""
    manifest_path = default_manifest_path()
    text = manifest_path.read_text(encoding="utf-8")
    result = validate(text)
    assert result.ok, result.errors
    assert "| Auto-start |" in text
