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

# Active-supervision (§2.6): a supervisor's claim on a thread is trusted for at most this
# long. Beyond it the generator emits ``supervised_by.stale = true`` rather than silently
# trusting an abandoned claim — the same failure shape as the manifest's Status column
# drifting from reality, avoided here by design. Mirrors SUPERVISOR_LOOP.md §2a's
# "verify before trusting a prolonged state" discipline; matches the existing check cadence.
SUPERVISION_STALE_MINUTES = 60

# The supervisor-written claims file. NOT generated — supervisors write it directly so a
# claim/release is a small, self-mergeable docs-only PR, not a heavyweight edit against
# HANDOFF_MANIFEST.md (the contention that caused the PR #1127 merge-conflict incident).
SUPERVISION_FILENAME = "active_supervision.json"

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
#
# Ordering is load-bearing and is NOT the §2 enum order: a Status cell narrates
# history, so a *terminal* word ("complete", "done", "deployed") frequently describes
# a finished sub-step inside an in-flight or human-gated row. The generic terminal
# words therefore sit LAST and the specific stage markers are tested first. Real cases:
#   "build complete — awaiting governor UAT"   -> human_uat_ready (not done)
#   "executing — PR1–PR3 done + deployed"       -> executing       (not done)
#   "deployed — Tier-1 parity gaps in progress" -> executing       (not done)
# ``deployed`` -> done and ``draft`` / ``demo`` -> awaiting_kickoff mirror the
# validator's KNOWN_STATUS_KEYWORDS so every status it accepts also maps to a state.
STATE_RULES: list[tuple[str, str]] = [
    # -- explicit terminal override (beats any history it narrates) --
    (r"\bsuperseded\b", "done"),
    # -- non-terminal health markers --
    (r"\bstale\b", "stale"),
    (r"\bfailed\b|\berrored\b", "failed"),
    # -- human-gated stages (must precede the generic terminal words) --
    (r"human uat|governor uat|human_uat_ready|ready for human", "human_uat_ready"),
    (r"sophia uat", "sophia_uat"),
    (r"envoy uat", "envoy_uat"),
    # A cell naming the human as the blocker is blocked_on_human, not paused_at_gate;
    # 'governor'/'gary' are this DAO's human-gate vocabulary.
    (
        r"await(?:ing)? (?:gary|governor|human)\b|pending (?:gary|governor|human)\b",
        "blocked_on_human",
    ),
    # -- prod-merge stage (pre-done) --
    # 'prod deploy' is deliberately absent: it is a history phrase inside done rows
    # ("... prod deployed + verified"), whereas these three are forward-looking.
    (r"prod merge|merged to prod|promote to prod", "prod_merge"),
    # -- not-yet-started --
    (
        r"await(?:ing)? kickoff|not yet triggered|go[- ]ready|\bnew\b|\bdraft\b|\bdemo\b",
        "awaiting_kickoff",
    ),
    # -- active work (precedes terminal words; see the ordering note above) --
    (r"in progress|in flight|\bexecuting\b|\bwip\b|underway", "executing"),
    # -- generic terminal words (lowest priority) --
    (r"\bdeployed\b", "done"),
    (r"\bcomplet(?:e|ed)\b", "done"),
    (r"\bdone\b", "done"),
]

# Keywords that mark a "blocked" cell as human-only (never supervisor-clearable).
# 'governor'/'gary'/'approval'/'thumbs' are included because this DAO's human gates are
# most often phrased that way ("blocked on Gate D — Gary must ssh in"), not with the
# literal word "human".
HUMAN_GATE_KEYWORDS = (
    "human",
    "governor",
    "gary",
    "approval",
    "thumbs",
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


def default_supervision_path() -> Path:
    return Path(__file__).resolve().parent.parent / "handoffs" / SUPERVISION_FILENAME


def _norm_plan_key(plan: str) -> str:
    """Normalize a plan-file cell/id for supervision matching.

    The manifest wraps plan files in backticks (`` `plans/X.md` ``); a supervisor's
    claims file may not. Compare on the bare path so the two always line up.
    """
    return plan.strip().strip("`").strip()


def _clean_id(value: str | None) -> str | None:
    """Normalize an optional linkage id cell for use as a URL path segment.

    The Manifest sometimes wraps channel/thread ids in backticks (e.g.
    `` `1548896014868676608` ``). Left raw, those backticks are emitted into the
    board's deep-link hrefs and produce a 404-looking broken link. Strip the
    backticks and surrounding whitespace; an empty/None cell stays None.
    """
    if value is None:
        return None
    cleaned = value.strip().strip("`").strip()
    return cleaned or None


def load_supervision(path: Path | None) -> dict[str, dict[str, Any]]:
    """Load ``handoffs/active_supervision.json`` -> {normalized plan: claim}.

    The file is supervisor-written, not generated. A missing or malformed file means
    "no active claims" — the board must degrade to "unclaimed", never error. On a
    duplicate claim for one plan, the last entry wins.
    """
    if path is None:
        return {}
    try:
        path = Path(path)
        if not path.exists():
            return {}
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(raw, dict):
        return {}
    claims = raw.get("claims")
    if not isinstance(claims, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        plan = claim.get("plan_file")
        if not isinstance(plan, str) or not plan.strip():
            continue
        out[_norm_plan_key(plan)] = {
            "supervisor": claim.get("supervisor"),
            "claimed_at": claim.get("claimed_at"),
            "note": claim.get("note"),
        }
    return out


def _parse_iso(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def supervision_entry(
    plan: str,
    supervision: dict[str, dict[str, Any]],
    now: datetime | None = None,
) -> dict[str, Any] | None:
    """Resolve a plan's ``supervised_by`` block, or ``None`` if unclaimed.

    A claim older than ``SUPERVISION_STALE_MINUTES`` — or one whose ``claimed_at``
    cannot be parsed — is emitted with ``stale = true``, so an abandoned claim is
    surfaced, never silently trusted.
    """
    claim = supervision.get(_norm_plan_key(plan)) if supervision else None
    if not claim:
        return None
    claimed_at = claim.get("claimed_at")
    parsed = _parse_iso(claimed_at)
    stale = False
    age_minutes: int | None = None
    if parsed is None:
        stale = True
    else:
        now = now or datetime.now(timezone.utc)
        age_minutes = max(0, int((now - parsed).total_seconds() // 60))
        stale = age_minutes > SUPERVISION_STALE_MINUTES
    return {
        "supervisor": claim.get("supervisor"),
        "claimed_at": claimed_at,
        "note": claim.get("note"),
        "stale": stale,
        "age_minutes": age_minutes,
    }


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


def build_index(
    text: str,
    source: str,
    supervision: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the index dict from the manifest's raw markdown text.

    ``supervision`` maps a normalized plan path to its active claim (§2.6); when
    omitted, every handoff is emitted as unclaimed (``supervised_by = null``).
    """
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
                "discord_channel_id": _clean_id(
                    _first_cell(row, DISCORD_CHANNEL_COLUMNS)
                ),
                "discord_thread_id": _clean_id(
                    _first_cell(row, DISCORD_THREAD_COLUMNS)
                ),
                "auto_start": row.get("Auto-start").lower() or None,
                "last_updated": row.get("Last manifest update"),
                "supervised_by": supervision_entry(plan, supervision or {}),
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


# Clock-derived fields: two builds of the SAME manifest legitimately differ here, so the
# drift gate must ignore them or it would fail on every run with no real change.
SUPERVISION_VOLATILE_KEYS = ("stale", "age_minutes")


def _strip_volatile(index: dict[str, Any]) -> dict[str, Any]:
    """Drop fields that legitimately differ between two builds of the same manifest.

    ``generated_at`` is a timestamp; ``supervised_by.stale`` / ``age_minutes`` are
    derived from ``claimed_at`` vs. the wall clock. None are content, so they must not
    read as drift.
    """
    stripped: dict[str, Any] = {}
    for key, value in index.items():
        if key == "generated_at":
            continue
        if key == "handoffs" and isinstance(value, list):
            rows: list[Any] = []
            for handoff in value:
                row = dict(handoff)
                claim = row.get("supervised_by")
                if isinstance(claim, dict):
                    row["supervised_by"] = {
                        k: v
                        for k, v in claim.items()
                        if k not in SUPERVISION_VOLATILE_KEYS
                    }
                rows.append(row)
            stripped[key] = rows
            continue
        stripped[key] = value
    return stripped


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
        "--supervision",
        default=None,
        help=(
            "Path to active_supervision.json "
            f"(default: {SUPERVISION_FILENAME} beside the manifest)"
        ),
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

    supervision = load_supervision(
        Path(args.supervision)
        if args.supervision
        else manifest_path.resolve().parent / SUPERVISION_FILENAME
    )
    index = build_index(
        manifest_path.read_text(encoding="utf-8"),
        _source_label(manifest_path),
        supervision,
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
