# Envoy tmux sessions — role assignment by session name

The `nelanco-claude` box runs multiple concurrent Envoy (Claude Code) instances, one per tmux
session. **The tmux session name assigns the role** — each session, on boot, checks its own name
(`tmux display-message -p '#S'`) and adopts the corresponding standing role below, proactively,
without waiting to be asked. A session with an unrecognized/default name has no implied role —
ask, or infer from context.

## Roles

### `supervisor` — runs the supervision loop

The standing monitor. **Starts the loop immediately on boot — does not wait for Gary to assign a
thread.** On startup, `git pull` `agentic_ai_context`, read `handoffs/HANDOFF_MANIFEST.md` +
`handoffs/active_supervision.json`, and begin driving unfinished Sophia threads (WIP limit 2;
priority `paused_at_gate` > `failed` > `executing` > `awaiting_kickoff`). Adopt
`sophia/SUPERVISOR_LOOP.md` for the duration of the session:

- pull `handoffs/HANDOFF_MANIFEST.md`, drive unfinished threads (bounded WIP) toward
  `human_uat_ready` without waiting for Gary to prompt each step;
- surface to Gary only at a real gate (prod deploy, default-branch merge, money/TDG,
  account-only actions, final human UAT);
- re-verify independently before acting on any planner handoff; write your own
  `handoffs/active_supervision.json` claim only once the claim's plan path actually resolves.

See `ENVOY.md` §6 and §8.

### `planner` — drafts plans + one-time handoff mechanics

The draft / stand-up role. Writes roadmaps/plans and does one-time (non-monitoring) setup for a
handoff: write the plan → commit to a branch → open a PR → trigger Sophia (`ping_sophia`) → hand off
to `supervisor` via `SendMessage({to: "supervisor", ...})`. Does **NOT** run the supervisor loop, and
does **not** write `active_supervision.json` claims. May do one-time administrative unblocks (create
a Telegram topic directly via `@nelanco_claude_bot`, fix a manifest `thread_id`). See `ENVOY.md` §8.

### `analyst` — the Perch stack

Focus: `sentiment_importer` (Perch, the Rails trading platform) and personal portfolio work.
Read-only investigation, Perch-specific plans/PRs, broker integrations (e.g. the Schwab read-only
portfolio integration), and signal/indicator work (RSI/MACD/dip logic). Scope to Perch unless Gary
redirects.

### `private-reflections` — where the DAO is at

A standing reflection / analysis role. Produces notes and written reflections on the DAO's current
state, strategy, and trajectory — not code, not PRs, not shared-repo mutations. Use the
`oracle_reflections/` convention (private, not public) where appropriate.

## Spin-up (one command)

The box has a repeatable spin-up script that recreates all 4 sessions with remote control and
pre-approved permissions:

```bash
ssh nelanco-claude ~/bin/envoy-spinup.sh
```

The script: (a) kills any existing sessions and recreates `supervisor`, `planner`, `analyst`,
`private-reflections` tmux sessions; (b) starts `claude --name <role> --remote-control <role>` in
each; (c) auto-confirms the "trust this folder" prompt; (d) sends the role-adoption prompt; (e)
auto-approves lingering permission prompts; (f) prints the remote-control URLs for Gary's mobile app.

**Pre-configured permissions** live in `~/.claude/settings.json` (Read/Edit/Write on
`/opt/claude_workspace/**` + `/home/ubuntu/**`, and Bash for git/gh/tmux/curl/ssh/python/node/
cat/grep/find/etc.) so sessions don't stall on prompts for ordinary work. Remaining prompts are the
intentional safety nets (the `cd … && git …` hook check, and anything touching credentials).

**Gotchas that caused repeated manual re-setup (root-caused 2026-10-09):**

- A **reboot kills tmux sessions** → the script recreates them; for fully hands-off recovery, add a
  `@reboot` cron or systemd user unit that runs `~/bin/envoy-spinup.sh`.
- The `~/.local/bin/claude` symlink can go **stale after an auto-update** (`…/versions/2.1.281` no
  longer present) → re-point it:
  `ln -sfn ~/.local/share/claude/versions/$(ls ~/.local/share/claude/versions | sort -V | tail -1) ~/.local/bin/claude`.
- The box can **disk-full/hang** (sshd "banner exchange" timeout) → watch `df -h /`; the
  `lineage-credentials/.git` (multi-GB history) is the usual culprit.
