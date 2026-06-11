# Sophia Watch-and-Notify — Execution Roadmap

**Status as of 2026-06-10:** pre-flight
**Repo under change:** `truesight_autopilot` (Sophia)
**Owner:** Gary Teh · **Driver:** Claude Code

**Why:** A turn is a bounded request→response (adapter hard-caps it at 180s) with one
executor per topic. When Sophia kicks off a long async op (AMI/snapshot bake, instance
boot, deploy, CI) she has been *promising* "I'll let you know when it's done" — but
**nothing watches it**, so the follow-up never fires. Proven 2026-06-10: she said she'd
report when `ami-05da693e385f7585a` finished; it reached `available` at 23:52Z and she
said nothing (and wouldn't). This builds the missing capability so that promise is real.

> **RESUME HERE:** PR-A step 1 — `app/watch_runner.py`.

---

## Design

- **Detached poller, not in-turn blocking.** The executor must NOT block-wait on a slow op
  — it holds the per-topic lock (see `SOPHIA_THREAD_CONCURRENCY_PLAN.md`) and would freeze
  the topic. So the watcher is a **separate detached process** (`subprocess.Popen(...,
  start_new_session=True)`), exactly like `app/ci_pingback.py`. It survives the turn, polls
  on its own, and posts back to the originating Telegram topic when the op reaches a
  terminal state.
- **Sophia registers it via a tool.** `watch_aws_resource` (and `watch_url`) launch the
  poller and return immediately. Only *after* a watcher is registered may Sophia truthfully
  say "I'll let you know." The tool descriptions enforce this.
- **Notifies the right topic.** The tool reads `session_id` (`tg:<chat>:<thread>`) from the
  tool context and passes chat+thread to the poller, which sends via the Telegram Bot API
  (`TELEGRAM_BOT_API_KEY`, already in the service env).
- **Generic by kind.** `watch_runner --kind {ami,snapshot,instance_running,volume,http}`.
  AWS kinds poll via the existing `aws_tools.aws_query` (reuses all account/region/cred
  plumbing). `http` polls a URL until a status/substring matches (covers deploy/health).
  CI is already covered by `ci_pingback`; a `github_actions` kind can be added later.
- **Bounded + honest on timeout.** Each watcher has a max duration; if the op isn't terminal
  by then it posts "⏳ still not done after N — stopping watch, ping me to re-check" so it
  never lies by silence and never runs forever.

---

## Pre-flight checklist

- [x] Tool auto-discovery: `tool_registry._iter_tool_modules()` picks up any `app/tools/*.py`
      exporting `TOOL_SPEC`/`TOOL_SPECS` — a new `watch_tools.py` is found automatically.
- [x] `ctx` carries `session_id` to handlers; parse `tg:<chat>:<thread>`.
- [x] `aws_query(account, service, operation, parameters, region)` returns JSON and handles
      creds/accounts (`nelanco`/`explorya`); reuse it for AWS probes.
- [x] `TELEGRAM_BOT_API_KEY` is in the service env (inherited by the detached process).
- [ ] Confirm watcher doesn't double-fire (dedupe identical resource+topic).

## Sequenced plan

### PR-A — watch_runner + tools + tests (one PR)
| Step | Description | Files |
|------|-------------|-------|
| 1 | `app/watch_runner.py` — detached CLI poller. `--kind` maps to (describe op, id key, state path, done/failed states). Loop: probe → terminal? notify+exit : sleep; on deadline notify "stopping". Reuses `ci_pingback.send_telegram` + `aws_tools.aws_query`. | `app/watch_runner.py` |
| 2 | `app/tools/watch_tools.py` — `watch_aws_resource` (resource_kind enum + id) and `watch_url`. Handler parses chat/thread from `ctx['session_id']`, launches the detached poller, returns "👁 Watching … I'll post here when done." Strong descriptions: only promise follow-up after registering. | `app/tools/watch_tools.py` |
| 3 | Tests — kind→spec mapping, terminal-state detection, session_id→chat/thread parse, tool launches a detached process (mock Popen) and returns the confirmation. | `tests/test_watch_*.py` |
| 4 | Deploy + live verify (re-run the AMI case; confirm a real ping on completion). | — |

## Test plan
- Pure-unit: `_resource_spec(kind)` mapping; `_extract_state(kind, describe_json)`; terminal
  classification (done/failed/pending/not-found); `_chat_thread_from_session("tg:-100:5")`.
- Tool: `watch_aws_resource` with a mocked `subprocess.Popen` → asserts the argv (kind, id,
  chat, thread) and the human confirmation string; rejects a non-Telegram session.

## Rollout
Deploy via the targeted path (no `git clean`). Restart `truesight-autopilot` (tool lives in
the main app) + `truesight-autopilot-telegram` if touched. Live test: have Sophia start a
throwaway AWS op (or re-watch the existing AMI) and confirm the topic gets the completion ping.

## Resume tracker
| Unit | Code | Merged | Deployed |
|------|------|--------|----------|
| PR-A — watch_runner + tools + tests | ☐ | ☐ | ☐ |

> **RESUME HERE:** PR-A step 1 — `app/watch_runner.py`.
