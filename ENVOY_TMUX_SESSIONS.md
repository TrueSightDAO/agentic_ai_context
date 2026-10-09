# Envoy tmux sessions — role assignment by session name

The `nelanco-claude` box runs multiple concurrent Envoy (Claude Code) instances, one per tmux
session. **The tmux session name assigns the role** — each session, on boot, checks its own name
(`tmux display-message -p '#S'`) and adopts the corresponding standing role below, proactively,
without waiting to be asked. A session with an unrecognized/default name has no implied role —
ask, or infer from context.

## Roles

### `supervisor` — runs the supervision loop

The standing monitor. Adopt `sophia/SUPERVISOR_LOOP.md` for the duration of the session:

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

## Recovery (after reboot / disconnect)

```bash
ssh nelanco-claude
tmux new-session -d -s <role>
tmux send-keys -t <role> 'claude --name <role> --remote-control <role>' Enter
```

The session then reads this file + `OPERATING_INSTRUCTIONS.md` and adopts its role. The remote-control
URL is printed to the pane; relay it to Gary to connect from the mobile app.
