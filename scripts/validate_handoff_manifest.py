#!/usr/bin/env python3
"""Validate the structural consistency of handoffs/HANDOFF_MANIFEST.md.

Catches the class of drift that let two separate handoff files disagree about
the same plan's status (see plans/HANDOFF_REGISTRY_CONSOLIDATION_PLAN.md):

  - missing/renamed required columns
  - duplicate `Plan file` rows
  - undocumented `Status` values (typos vs the '## Status values' legend)
  - a `Telegram topic` without a `message_thread_id` (or vice versa)
  - a `message_thread_id` reused across more than one `Plan file`

Usage:
    python3 scripts/validate_handoff_manifest.py [path/to/HANDOFF_MANIFEST.md]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_COLUMNS = [
    "Plan file",
    "Handoff title",
    "Handoff date",
    "Status",
    "Telegram topic",
    "message_thread_id",
    "Resume tracker state",
    "Last manifest update",
]

# Status cells are free prose (e.g. "GO-ready — blocked on Gate D"), not a strict
# enum, so we check for a known keyword substring rather than an exact match.
KNOWN_STATUS_KEYWORDS = [
    "in progress",
    "blocked",
    "demo",
    "completed",
    "stale",
    "draft",
    "go-ready",
    "deployed",
    "superseded",
]

EMPTY_MARKERS = {"", "-", "—", "n/a", "na"}


@dataclass
class Row:
    cells: dict[str, str]
    line_no: int

    def get(self, column: str) -> str:
        return self.cells.get(column, "").strip()


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def is_empty(value: str) -> bool:
    value = value.strip()
    if value.lower() in EMPTY_MARKERS:
        return True
    # Treat "— (explanation)" style annotations (e.g. "— (GAS cron, no Telegram
    # handoff)") as empty too — the leading em-dash is this table's convention
    # for "not applicable, here's why".
    return value.startswith("—")


def split_row(line: str) -> list[str]:
    """Split a markdown table row into cells."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line)]


def find_table(text: str) -> tuple[list[str], list[Row]]:
    """Find the first contiguous markdown table whose header has a 'Plan file' column."""
    lines = text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "Plan file" in line:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("No markdown table with a 'Plan file' column found")

    header = split_row(lines[header_idx])
    body_start = header_idx + 2  # skip the header row + the '---|---' separator
    rows: list[Row] = []
    for i in range(body_start, len(lines)):
        line = lines[i]
        if not line.strip().startswith("|"):
            break
        cells = split_row(line)
        if len(cells) != len(header):
            cells = (cells + [""] * len(header))[: len(header)]
        rows.append(Row(cells=dict(zip(header, cells)), line_no=i + 1))
    return header, rows


def validate(text: str) -> ValidationResult:
    result = ValidationResult()
    try:
        header, rows = find_table(text)
    except ValueError as exc:
        result.errors.append(str(exc))
        return result

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing_columns:
        result.errors.append(f"Missing required column(s): {missing_columns}")
        return result

    seen_plans: dict[str, int] = {}
    thread_to_plans: dict[str, list[str]] = {}

    for row in rows:
        plan = row.get("Plan file")
        if is_empty(plan):
            result.errors.append(f"Row at line {row.line_no}: empty 'Plan file' cell")
            continue

        if plan in seen_plans:
            result.errors.append(
                f"Duplicate 'Plan file' row: {plan!r} appears at lines "
                f"{seen_plans[plan]} and {row.line_no}"
            )
        else:
            seen_plans[plan] = row.line_no

        status = row.get("Status").lower()
        if status and not any(keyword in status for keyword in KNOWN_STATUS_KEYWORDS):
            result.warnings.append(
                f"{plan}: Status {row.get('Status')!r} does not contain any known "
                "status keyword — check the '## Status values' legend"
            )

        topic = row.get("Telegram topic")
        thread_id = row.get("message_thread_id")
        topic_empty = is_empty(topic)
        thread_empty = is_empty(thread_id)
        thread_is_placeholder = "needs verification" in thread_id.lower()

        # A placeholder ("NEEDS VERIFICATION") counts as "present" for the
        # both-or-neither check — it's a known-pending value, not a missing one.
        if topic_empty != thread_empty:
            result.errors.append(
                f"{plan}: 'Telegram topic' and 'message_thread_id' must be both-or-neither "
                f"(topic={topic!r}, thread_id={thread_id!r})"
            )

        if not thread_empty and not thread_is_placeholder:
            m = re.search(r"\d+", thread_id)
            if m:
                thread_to_plans.setdefault(m.group(0), []).append(plan)

    for thread_id, plans in thread_to_plans.items():
        if len(plans) > 1:
            result.errors.append(
                f"message_thread_id {thread_id!r} is reused across multiple plans: {plans}"
            )

    return result


def default_manifest_path() -> Path:
    return Path(__file__).resolve().parent.parent / "handoffs" / "HANDOFF_MANIFEST.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="?",
        default=str(default_manifest_path()),
        help="Path to HANDOFF_MANIFEST.md (default: repo's handoffs/HANDOFF_MANIFEST.md)",
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    text = manifest_path.read_text(encoding="utf-8")
    result = validate(text)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    if result.ok:
        print(
            f"OK: {manifest_path} passed validation ({len(result.warnings)} warning(s))"
        )
        return 0

    print(f"FAILED: {len(result.errors)} error(s) in {manifest_path}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
