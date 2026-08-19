# Agent Handoff Protocol — implementation plan

**Status:** Plan-of-record. **Created:** 2026-08-19 | **Owner:** Gary Teh | **Author:** Claude Code (nelanco-claude box)
**Convention:** Follows `OPERATING_INSTRUCTIONS.md` §5 / §5a / §5d / §5e.

> ## RESUME HERE: Unit 0

## Context

Gary wants Sophia and Bionpact (and any future sibling instance) to hand off information to
each other — "when there are some handoff of prior information" — without open, continuous
bot-to-bot chat (rejected: Telegram's own docs flag bot-to-bot loops as a mandatory risk to
engineer against, and neither instance has that safeguard) and without giving either instance
broad write access to the other's private storage (rejected: defeats the whole point of
Bionpact's narrowly-scoped credentials).

Landed design, built up over conversation:
- **Generic, not per-pair.** One `send_handoff(target_agent, summary, context)` tool and one
  `check_handoffs()` tool, shared code, work for any registered agent — a third future instance
  needs one registry file, zero new code.
- **Pull-based mailbox, not push-based chat.** Modeled on SMTP's addressing (a registry says
  where each agent's mail lives) but POP3's retrieval (each agent polls its own mailbox on its
  own schedule) — this is what lets Bionpact participate with **zero inbound network exposure**,
  preserving her VPC-isolated, no-public-IP design from tonight.
- **Shared post-office repo, not each other's private storage.** The credential problem Gary
  caught: if Bionpact's inbox were her own `bionpact_agentic_ai_context`, Sophia can't write
  there (her `allowed_repos` gate correctly excludes it) — and Bionpact's fine-grained PAT
  can't write to Sophia's repos either. Fix: one dedicated, private, single-purpose repo
  (`TrueSightDAO/agent_handoffs`) that every registered agent's PAT gets **one additional,
  narrow** write grant to — nobody gets a key to anyone else's house, everyone gets a key to
  the shared mailbox structure, which holds nothing else.
- **Public registry, private mail.** `agentic_ai_context/agents/<name>.json` (public,
  PR-edited, same repo as `PROJECT_INDEX.md`) lists which agents exist — that's already public
  knowledge (documented in `PROJECT_INDEX.md` tonight). The mail *contents* live in the private
  `agent_handoffs` repo.
- **Filename-routes-the-message.** `handoffs/{target}_from_{sender}_{timestamp}.json` — an
  agent's `check_handoffs()` only reads files prefixed with its own name.

## Pre-flight (§5d completeness)

- **Sophia's GitHub PAT** (`TRUESIGHT_DAO_AUTOPILOT`, org-wide Contents:RW + PRs:RW) already
  covers any repo in `TrueSightDAO` at the token level. Her app-level `allowed_repos` /
  `api_only_repos` gate (app/config.py) is what actually restricts her — `agent_handoffs` needs
  adding to both lists (via `own_repos`-style default, so it's live for her automatically once
  the code change merges — no `.env` edit needed on her box).
- **Bionpact's GitHub PAT** is fine-grained, scoped to exactly 3 repos
  (`bionpact_agentic_ai_context`, `bionpact_autopilot_transcription`, `bionpact_attachments`).
  It does **not** cover a new repo automatically — Gary must add `agent_handoffs` to that
  token's repository list in GitHub (Settings → Developer settings → Fine-grained tokens →
  edit → add repository), same as the original PAT setup. **This is the one step only Gary can
  do** — flagging it now so it isn't a surprise mid-roadmap.
- **`app/config.py`'s `own_repos` / `allowed_repos` / `api_only_repos` mechanism** (built
  tonight, PR #298/#299/#300 merged) is the exact machinery this needs — no new config pattern,
  just one more entry.
- **`_run_script` / standalone-script pattern** (`extract_pdf_text.py`,
  `append_to_transcript.py`) is the established way to add a new attachment-style tool — the
  same shape fits `send_handoff.py` / `check_handoffs.py` as callable scripts, or simpler,
  inline Python functions in a new `app/tools/agent_handoff.py` module (no subprocess needed
  here — this is pure GitHub Contents-API read/write, same as `upload_file_to_github.py`).
- **Both instances' `.env`** currently sets `ALLOWED_REPOS` explicitly (Bionpact) or relies on
  the code default (Sophia). Bionpact's `.env` `ALLOWED_REPOS` list needs `agent_handoffs`
  appended alongside her existing 3.

## Sequenced plan (one unit per turn, §5a)

| # | Unit | Type | Notes |
|---|------|------|-------|
| 0 | Create `TrueSightDAO/agent_handoffs` (private), seeded with `handoffs/README.md` explaining the convention | GitHub (low-risk, reversible) | |
| 1 | Commit this roadmap to `agentic_ai_context/plans/AGENT_HANDOFF_PROTOCOL_PLAN.md` | Docs | |
| 2 | Create the registry: `agentic_ai_context/agents/sophia.json`, `agentic_ai_context/agents/bionpact.json` | Docs (public, PR-edited) | Schema: `{"name","purpose","inbox_repo","transcript_repo"}` |
| 3 | Code PR to `truesight_autopilot`: new `app/tools/agent_handoff.py` (`send_handoff`, `check_handoffs`), add `"agent_handoffs"` to the default `allowed_repos` + `api_only_repos`, tests, system-prompt mention | Code (PR + tests) | Zero behavior change for existing tools; purely additive |
| 4 | Credentials: Gary adds `agent_handoffs` to Bionpact's fine-grained PAT's repository list | Human-assisted (only Gary can do this) | |
| 5 | Deploy: redeploy both Sophia and Bionpact (post-Unit-3 code); add `agent_handoffs` to Bionpact's `.env` `ALLOWED_REPOS` | Deploy | Restart both, same as tonight's docx deploy |
| 6 | UAT | Human-tested | See below |

**Resume tracker — Continue from the first row that isn't done.**

## UAT

1. Ask Sophia (in her own Telegram) to `send_handoff("bionpact", "test summary", "test context")`
   → a file appears at `agent_handoffs/handoffs/bionpact_from_sophia_<timestamp>.json`.
2. Ask Bionpact to `check_handoffs()` → she reads the note, acknowledges it, and folds it into
   her own context/notes as instructed.
3. Reverse: Bionpact sends a handoff to Sophia, same verification.
4. Confirm scope held: Sophia still cannot write to `bionpact_agentic_ai_context` (or any other
   Bionpact-only repo); Bionpact still cannot write to `agentic_ai_context` or any other
   Sophia-only repo. Only `agent_handoffs` is newly shared.
5. Confirm routing: a handoff addressed to `sophia` does not surface in Bionpact's
   `check_handoffs()`, and vice versa (filename-prefix isolation).

## Open items flagged, not blocking

- Should `check_handoffs()` run automatically on a background loop (like follow-ups) or stay
  purely on-demand (LLM decides to check)? Defaulting to on-demand for v1 — lower risk, easy to
  add a loop later once the pattern's proven live.
- `agent_handoffs` repo visibility: private by default (handoff content could originate from
  Bionpact's private context) — not requiring per-message sensitivity classification for v1.
