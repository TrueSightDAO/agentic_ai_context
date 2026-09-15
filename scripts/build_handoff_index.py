#!/usr/bin/env python3
"""Build handoffs/index.json — the machine-readable mirror of HANDOFF_MANIFEST.md.

`SUPERVISOR_LOOP.md` §8 asks for a generated index of the handoff manifest carrying:

  1. the §2 supervisor **state enum**,
  2. both the Telegram ``message_thread_id`` **and** the Discord channel/thread id,
  3. a ``last_updated`` timestamp.

This script derives all three from ``handoffs/HANDOFF_MANIFEST.md`` (the single source
of truth) and emits ``handoffs/index.json``. Cell splitting is delegated to
``validate_handoff_manifest.py`` so the builder and the validator read cells identically.

Discord ids come from the optional ``Discord channel id`` / ``Discord thread id``
columns (option (a) of the §8 scoping decision). Those columns do not exist yet, so
the fields are emitted as ``null`` until a plan author adds them — a row is never
dropped for lacking them.

The long prose ``Resume tracker state`` column is intentionally **not** mirrored: the
index is the machine-facing state view; the manifest stays the source for prose.

Robustness note: the committed manifest is currently **not one contiguous table** — a
blank line and a stray row fragment split it, and ``validate_handoff_manifest.find_table``
stops at the first break (it therefore only ever sees the first 3 rows). This builder
instead gathers every handoff-shaped row across all segments and *reports* the raggedness
as a warning, so no row is silently dropped. Those warnings are the signal to repair the
manifest.

Usage:
    python3 scripts/build_handoff_index.py             # write handoffs/index.json
    python3 scripts/build_handoff_index.py --stdout     # print, do not write
    python3 scripts/build_handoff_index.py --check      # exit 1 if the committed index drifts
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_handoff_manifest import (  # noqa: E402
    Row,
    default_manifest_path,
    is_empty,
    split_row,
)

SCHEMA_VERSION = 1

# The §2 supervisor state enum, in the order SUPERVISOR_LOOP.md lists it.
STATE_ENUM = [
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

# Ordered (regex, state) rules; first match wins. Matched against the lower-cased
# Status cell ONLY (never the whole row), so prose in other columns cannot leak in.
# ``deployed`` -> done and ``draft`` / ``demo`` -> awaiting_kickoff mirror the
# validator's KNOWN_STATUS_KEYWORDS so every status it accepts also maps to a state.
STATE_RULES: list[tuple[str, str]] = [
    (r"\bsuperseded\b", "done"),
    (r"\bdeployed\b", "done"),
    (r"\bcomplet(?:e|ed)\b", "done"),
    (r"\bdone\b", "done"),
    (r"\bstale\b", "stale"),
    (r"\bfailed\b|\berrored\b", "failed"),
    (
        r"await(?:ing)? kickoff|not yet triggered|go[- ]ready|\bnew\b|\bdraft\b|\bdemo\b",
        "awaiting_kickoff",
    ),
    (r"sophia uat", "sophia_uat"),
    (r"envoy uat", "envoy_uat"),
    (r"human uat|ready for human|human_uat_ready", "human_uat_ready"),
    (r"prod merge|merged to prod|prod deploy|promote to prod", "prod_merge"),
    (r"in progress|in flight|executing|\bwip\b|underway", "executing"),
]

# Keywords that mark a "blocked" cell as human-only (never supervisor-clearable).
HUMAN_GATE_KEYWORDS = (
    "human",
    "money",
    "secret",
    "treasury",
    "dns",
    "domain",
    "account",
    "org",
)

# Optional manifest columns for the Discord side of the linkage (option (a)).
DISCORD_CHANNEL_COLUMNS = [
    "Discord channel id",
    "Discord channel",
    "discord_channel_id",
]
DISCORD_THREAD_COLUMNS = ["Discord thread id", "Discord thread", "discord_thread_id"]

URL_RE = re.compile(r"https?://[^\s)]+")
DIGITS_RE = re.compile(r"\d+")


def derive_state(status_raw: str) -> tuple[str, str]:
    """Map a prose Status cell to a §2 state enum value.

    Returns ``(state, note)``. ``note`` is non-empty only when the mapping could not
    be made (``state == "unknown"``) so the caller can surface a warning instead of
    silently dropping the row.
    """
    text = (status_raw or "").strip()
    low = text.lower()
    if is_empty(text):
        return "unknown", "empty Status cell"
    if "blocked" in low or "paused" in low:
        if any(keyword in low for keyword in HUMAN_GATE_KEYWORDS):
            return "blocked_on_human", ""
        return "paused_at_gate", ""
    for pattern, state in STATE_RULES:
        if re.search(pattern, low):
            return state, ""
    return "unknown", f"Status {text!r} matched no state rule"


def collect_handoff_rows(text: str) -> tuple[list[str], list[Row], list[str]]:
    """Gather every handoff row across all table segments in the manifest.

    A row is "handoff-shaped" when its first cell names a markdown plan file (it
    contains ``.md``). That cleanly excludes the ``## Status values`` legend table
    (whose first cells are bare words like ``completed``) and any other 2-column
    table in the document.

    Ragged rows (wrong cell count, e.g. an unescaped ``|`` in prose) are padded or
    truncated to the header width — matching ``find_table``'s behaviour — and reported.
    Blank lines and stray non-``|`` text *inside* the row region are reported too, and
    skipped rather than silently ending the table the way ``find_table`` does.

    Returns ``(header, rows, warnings)``.
    """
    lines = text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "Plan file" in line:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("No markdown table with a 'Plan file' column found")

    header = split_row(lines[header_idx])
    ncols = len(header)

    rows: list[Row] = []
    warnings: list[str] = []
    first_row_line: int | None = None
    last_row_line: int | None = None

    for i in range(header_idx + 2, len(lines)):
        stripped = lines[i].strip()
        if not stripped.startswith("|"):
            continue
        cells = split_row(lines[i])
        if not cells or ".md" not in cells[0]:
            continue  # legend / non-handoff table row
        if len(cells) != ncols:
            warnings.append(
                f"line {i + 1}: ragged row has {len(cells)} cells, expected {ncols} "
                "— padded/truncated"
            )
            cells = (cells + [""] * ncols)[:ncols]
        first_row_line = first_row_line or i + 1
        last_row_line = i + 1
        rows.append(Row(cells=dict(zip(header, cells)), line_no=i + 1))

    if first_row_line and last_row_line:
        for lineno in range(first_row_line, last_row_line):
            probe = lines[lineno - 1].strip()
            if probe == "":
                warnings.append(f"line {lineno}: blank line splits the handoff table")
            elif not probe.startswith("|") and not probe.startswith("#"):
                warnings.append(
                    f"line {lineno}: stray text inside the handoff table "
                    "(missing leading '|' — malformed row fragment)"
                )

    return header, rows, warnings


def _first_cell(row: Row, columns: list[str]) -> str | None:
    for column in columns:
        if column in row.cells:
            value = row.get(column)
            if value and not is_empty(value):
                return value
    return None


def _resolve_thread_id(row: Row) -> tuple[str | None, bool, str]:
    """Return (thread_id, needs_verification, source_note)."""
    thread_cell = row.get("message_thread_id")
    needs_verification = "needs verification" in thread_cell.lower()
    if not is_empty(thread_cell) and not needs_verification:
        match = DIGITS_RE.search(thread_cell)
        if match:
            return match.group(0), False, "message_thread_id"
    topic_numbers = DIGITS_RE.findall(row.get("Telegram topic"))
    if topic_numbers:
        # The thread id is the LAST number in the topic cell: a cell is either
        # "(this thread 24442)" or a t.me URL "[x](https://t.me/c/<chat>/<thread>)",
        # where the FIRST number is the chat id, not the thread id.
        return topic_numbers[-1], needs_verification, "telegram_topic"
    return None, needs_verification, ""


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_index(text: str, source: str) -> dict[str, Any]:
    """Build the index dict from the manifest's raw markdown text."""
    _header, rows, warnings = collect_handoff_rows(text)
    handoffs: list[dict[str, Any]] = []

    for row in rows:
        plan = row.get("Plan file")
        if is_empty(plan):
            warnings.append(f"line {row.line_no}: empty 'Plan file' — row skipped")
            continue

        status_raw = row.get("Status")
        state, note = derive_state(status_raw)
        if state == "unknown":
            warnings.append(f"{plan}: {note}")

        thread_id, needs_verification, thread_source = _resolve_thread_id(row)
        topic_cell = row.get("Telegram topic")
        url_match = URL_RE.search(topic_cell)

        handoffs.append(
            {
                "plan_file": plan,
                "title": row.get("Handoff title"),
                "handoff_date": row.get("Handoff date"),
                "state": state,
                "status_raw": status_raw,
                "telegram_thread_id": thread_id,
                "telegram_thread_id_source": thread_source or None,
                "telegram_thread_id_needs_verification": needs_verification,
                "telegram_topic": topic_cell or None,
                "telegram_topic_url": url_match.group(0) if url_match else None,
                "discord_channel_id": _first_cell(row, DISCORD_CHANNEL_COLUMNS),
                "discord_thread_id": _first_cell(row, DISCORD_THREAD_COLUMNS),
                "auto_start": row.get("Auto-start").lower() or None,
                "last_updated": row.get("Last manifest update"),
            }
        )

    counts = {state: 0 for state in STATE_ENUM}
    counts["unknown"] = 0
    for handoff in handoffs:
        counts[handoff["state"]] = counts.get(handoff["state"], 0) + 1

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _utcnow(),
        "source": source,
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "state_enum": STATE_ENUM,
        "handoff_count": len(handoffs),
        "counts_by_state": counts,
        "handoffs": handoffs,
        "warnings": warnings,
    }


def render(index: dict[str, Any]) -> str:
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n"


def _strip_volatile(index: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in index.items() if key != "generated_at"}


def _source_label(manifest_path: Path) -> str:
    repo_root = Path(__file__).resolve().parent.parent
    try:
        return str(manifest_path.resolve().relative_to(repo_root))
    except ValueError:
        return str(manifest_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="?",
        default=str(default_manifest_path()),
        help="Path to HANDOFF_MANIFEST.md (default: repo's handoffs/HANDOFF_MANIFEST.md)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output path (default: index.json beside the manifest)",
    )
    parser.add_argument(
        "--stdout", action="store_true", help="Print the index instead of writing it"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if the committed index has drifted from the manifest",
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    output_path = (
        Path(args.output)
        if args.output
        else manifest_path.resolve().parent / "index.json"
    )

    index = build_index(
        manifest_path.read_text(encoding="utf-8"), _source_label(manifest_path)
    )
    rendered = render(index)

    if args.stdout:
        sys.stdout.write(rendered)
        return 0

    if args.check:
        if not output_path.exists():
            print(f"DRIFT: {output_path} does not exist — run the builder")
            return 1
        committed = json.loads(output_path.read_text(encoding="utf-8"))
        if _strip_volatile(committed) == _strip_volatile(index):
            print(
                f"OK: {output_path} is up to date ({index['handoff_count']} handoffs)"
            )
            return 0
        print(
            f"DRIFT: {output_path} is stale — regenerate with "
            "scripts/build_handoff_index.py"
        )
        return 1

    output_path.write_text(rendered, encoding="utf-8")
    for warning in index["warnings"]:
        print(f"WARNING: {warning}", file=sys.stderr)
    print(
        f"Wrote {output_path} — {index['handoff_count']} handoffs, "
        f"{len(index['warnings'])} warning(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
