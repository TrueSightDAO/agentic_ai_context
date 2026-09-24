# Envoy tmux session layout — bootstrap & recovery

**Purpose:** Claude Code sessions on `nelanco-claude` occasionally get disconnected (crash,
network blip, box reboot). This doc lets **one freshly-booted Claude, in one tmux pane**,
recreate the standard multi-session workspace from nothing — no need for Gary to re-explain
each seat's role by hand.

**What survives a disconnect vs. what doesn't:** the auto-memory system
(`/home/ubuntu/.claude/projects/-opt-claude-workspace/memory/`, `MEMORY.md`) and this repo
persist automatically regardless of session state — nothing is lost there. What's lost is the
**tmux process and the live conversation** in whichever pane died. Recovery means recreating the
tmux session and getting a fresh `claude` invocation in it to re-adopt the right role — it does
not mean restoring the old conversation transcript.

---

## 1. The canonical layout

Three persistent, named tmux sessions, each running `claude` from `/opt/claude_workspace`, each
with `/remote-control` active so Gary can drive it from the mobile app:

| tmux session name | Role | Primary doc to read | Scope |
|---|---|---|---|
| `planner` | Drafts/refreshes §5-compliant execution roadmaps. **Does not** run ongoing monitoring/supervision loops. | `ENVOY.md`, `OPERATING_INSTRUCTIONS.md` §5 | DAO/Envoy work — writes plans to `plans/`, files handoffs, hands off to `supervisor` via `SendMessage` (never triggers Sophia directly except when Gary explicitly asks planner itself to) |
| `supervisor` | Runs the proactive supervision loop — drives claimed handoffs in `handoffs/HANDOFF_MANIFEST.md` through R1/R2/R3 UAT toward `human_uat_ready` / prod merge, without waiting for Gary to prompt each step. | `sophia/SUPERVISOR_LOOP.md`, `ENVOY.md` points 6–7 | DAO/Envoy work — the one seat that actively pings Sophia's Telegram threads and checks on her progress |
| `analyst` | Gary's **personal** portfolio-management seat — not Envoy/DAO work. | (no fixed onboarding doc — orients around `sentiment_importer`'s live DB + Mobile API directly) | `sentiment_importer` (Perch: RSI/MACD/Bollinger/dip-recovery signals, `seni_ror`/`seni_sql`), general market data for Gary's own brokerage positions |

Ad hoc sessions (e.g. `reflections`, created 2026-09-24 as a private, non-DAO space) can be spun
up the same mechanical way but have no fixed role or onboarding doc — they're just another named
seat. This doc only covers the three **standing** roles above.

**Self-orientation convention (governs all three, and any future named role added here):** the
first action any Claude Code instance on this box takes is to check its own tmux session name
(`tmux display-message -p '#S'`). If it matches a name in the table above, read that row's doc
and adopt the role immediately — proactively, without waiting for Gary to ask. A session with an
unrecognized or default numeric name has no implied role; ask Gary or infer from context. This
convention is what makes a single-session reboot (not just a full box reset) self-healing: a
fresh `claude` relaunched into the existing `supervisor` pane, for instance, re-reads
`SUPERVISOR_LOOP.md` on its own and picks the loop back up.

---

## 2. Recovery recipe — recreating a missing session

Run from **any** tmux pane on this box (doesn't need to be one of the three itself). Repeat per
missing session; skip any that already exist (`tmux list-sessions` to check first).

```bash
tmux new-session -d -s <name> -c /opt/claude_workspace 'claude'
sleep 2
tmux send-keys -t <name>:0.0 "<first message, see below>"
sleep 1
tmux send-keys -t <name>:0.0 Enter
```

**First message per role** (this is what gets a brand-new `claude` process to self-orient
immediately, rather than waiting for the self-orientation convention above to be independently
rediscovered — belt-and-suspenders, since the freshly-spawned instance hasn't necessarily read
this file yet on its very first tool round):

- **`planner`:** `Read agentic_ai_context/OPERATING_INSTRUCTIONS.md, WORKSPACE_CONTEXT.md, PROJECT_INDEX.md, then ENVOY.md. Your tmux session is named "planner" — per agentic_ai_context/ENVOY_TMUX_SESSIONS.md, that means you draft and refresh execution roadmaps; you do not run the supervision loop.`
- **`supervisor`:** `Read agentic_ai_context/OPERATING_INSTRUCTIONS.md, WORKSPACE_CONTEXT.md, PROJECT_INDEX.md, then ENVOY.md and sophia/SUPERVISOR_LOOP.md. Your tmux session is named "supervisor" — per agentic_ai_context/ENVOY_TMUX_SESSIONS.md, run that loop now: pull HANDOFF_MANIFEST.md and drive unfinished threads proactively.`
- **`analyst`:** `Your tmux session is named "analyst" — per agentic_ai_context/ENVOY_TMUX_SESSIONS.md, this is Gary's personal portfolio-management seat (sentiment_importer/Perch + general market data), not DAO/Envoy relay work. Orient around Perch's live DB and Mobile API, not HANDOFF_MANIFEST.md.`

Then enable remote control on each so Gary can pick it up from his phone:

```bash
tmux send-keys -t <name>:0.0 "/remote-control"
sleep 1
tmux send-keys -t <name>:0.0 Enter
```

**Full from-scratch bootstrap** (all three missing — e.g. after a box reboot): run the block
above for `planner`, `supervisor`, and `analyst` in turn. Verify with
`tmux list-sessions` (expect all three, plus whichever pane you're bootstrapping from) and a
`tmux capture-pane -t <name>:0.0 -p` spot-check on each to confirm `claude` actually launched
clean (not stuck on an update prompt, permission dialog, or crash) before considering the
session recovered.

---

*Companion to `ENVOY.md` (owns the role philosophy/protocol) and `sophia/SUPERVISOR_LOOP.md`
(owns the supervisor loop mechanics) — this doc owns only the tmux-session-layout mechanics.
Last updated 2026-09-24.*
