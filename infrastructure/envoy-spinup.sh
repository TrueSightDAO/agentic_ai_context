#!/usr/bin/env bash
# Spin up the 4 Envoy tmux sessions (supervisor, planner, analyst, private-reflections).
# Canonical copy: agentic_ai_context/infrastructure/envoy-spinup.sh
# Box location: /home/ubuntu/bin/envoy-spinup.sh  (keep the two in sync)
# Usage: ssh nelanco-claude ~/bin/envoy-spinup.sh
set -euo pipefail

ROLES=(supervisor planner analyst private-reflections)
# supervisor runs the autonomous loop -> bypass permission prompts; others stay guarded.
PERMS=(bypassPermissions bypassPermissions bypassPermissions bypassPermissions)

# Every session loads the shared workspace context FIRST (git pull + core onboarding),
# then adopts its role. This guarantees no session starts without reading
# agentic_ai_context, regardless of role.
ONBOARD="First load your context: run \`git -C /opt/claude_workspace/agentic_ai_context pull\`, then read /opt/claude_workspace/agentic_ai_context/{OPERATING_INSTRUCTIONS.md,WORKSPACE_CONTEXT.md,PROJECT_INDEX.md,ENVOY.md}. Then:"

PROMPTS=(
  "$ONBOARD Adopt your supervisor role and start the loop now: read handoffs/HANDOFF_MANIFEST.md and handoffs/active_supervision.json, then supervise Sophia unfinished threads (WIP limit 2; priority paused_at_gate > failed > executing > awaiting_kickoff) per sophia/SUPERVISOR_LOOP.md. Report which threads you pick up."
  "$ONBOARD Adopt your planner role per ENVOY_TMUX_SESSIONS.md (draft plans + one-time handoff mechanics; do NOT run the supervisor loop), then wait for direction."
  "$ONBOARD Adopt your analyst role per ENVOY_TMUX_SESSIONS.md (the Perch/sentiment_importer stack), then wait for direction."
  "$ONBOARD Adopt your private-reflections role per ENVOY_TMUX_SESSIONS.md (DAO state/strategy notes, not code/PRs), then wait for direction."
)

for i in "${!ROLES[@]}"; do
  role="${ROLES[$i]}"
  tmux kill-session -t "$role" 2>/dev/null || true
  tmux new-session -d -s "$role"
  tmux send-keys -t "$role" "claude --name $role --permission-mode ${PERMS[$i]} --remote-control $role" Enter
  sleep 8
  tmux send-keys -t "$role" Enter
  sleep 10
  tmux send-keys -t "$role" "${PROMPTS[$i]}" Enter
done

sleep 25
for round in 1 2 3; do
  for role in "${ROLES[@]}"; do tmux send-keys -t "$role" "2" Enter; done
  sleep 8
done

echo "=== remote-control URLs ==="
for role in "${ROLES[@]}"; do
  url=$(tmux capture-pane -t "$role" -p 2>/dev/null | grep -oE "https://claude.ai/code/session_[A-Za-z0-9]+" | head -1)
  echo "$role: ${url:-<not ready yet>}"
done
