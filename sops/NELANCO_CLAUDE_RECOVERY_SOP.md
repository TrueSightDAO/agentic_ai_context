# Recovery Runbook: `nelanco-claude` (Envoy's box) — instance reachability + session restore

**Audience:** Sophia (and any other LLM instance with `aws_query` + `ssh_run`), plus governors
doing manual recovery. **Status:** Active · **Last updated:** 2026-10-25

**What this recovers.** The `nelanco-claude` EC2 box (Envoy's interactive Claude Code seat, and
the box the proactive Sophia-supervisor loop is meant to run on) periodically becomes **fully
unreachable** — SSH and ICMP time out — while AWS still reports the instance `running` with
`SystemStatus: ok` but `InstanceStatus: impaired` (`reachability: failed`). When that happens, the
four Envoy tmux sessions (`supervisor`, `planner`, `analyst`, `private-reflections`) are dead and
unfinished Sophia handoffs sit un-supervised. This runbook brings the box back and restores the
sessions.

**Instance identity (do not change):**

| Field | Value |
|-------|-------|
| Instance | `i-01ad5eca707e4445f` |
| Account | **`nelanco`** (`767697632458`) — NOT `explorya` |
| EIP / SSH | `100.57.50.48` (user `ubuntu`, port 22, SG `sg-003e8016026715f25` allows 0.0.0.0/0:22) |
| DNS | `claude.truesight.me` |
| Fleet alias (Sophia) | `nelanco-claude` (see §4) |

**Incident log (recurring, root cause still unknown):**

- 2026-09-14 — first occurrence; stop/start resolved.
- 2026-09-16/17 — second; `reboot` did **not** recover, stop/start did.
- 2026-10-25 — third (impaired since 2026-10-24T18:02Z, ~1 day down); recovered by stop/start +
  session restore. This runbook is the result.

---

## 1. Detect

If SSH to the box times out, confirm the AWS status before acting — the symptom is specific
(`running` + `SystemStatus ok` + `InstanceStatus impaired`), and the fix is **not** a reboot:

```
aws_query(account="nelanco", service="ec2", operation="DescribeInstanceStatus",
          parameters={"InstanceIds": ["i-01ad5eca707e4445f"]})
```

Impaired ⇒ proceed to §2. If `InstanceStatus` is `ok` but SSH still fails, that is a **different**
problem (key/SG/OS), not this incident — do not stop/start blindly.

## 2. Recover the instance — STOP → START (never reboot)

`RebootInstances` was proven **not** to restore reachability (incident 2). The known-working fix is
a hard `StopInstances` → wait for `stopped` → `StartInstances` → wait for `InstanceStatus: ok`.
Stop/start migrates the instance to different underlying hardware, which clears the fault.

**Step A — stop:**

```
aws_query(account="nelanco", service="ec2", operation="StopInstances",
          parameters={"InstanceIds": ["i-01ad5eca707e4445f"]}, confirm_write=true)
```

**Step B — poll until `stopped`** (usually < 60 s; incident 1 once sat in `stopping` for a while —
keep polling, don't panic):

```
aws_query(account="nelanco", service="ec2", operation="DescribeInstances",
          parameters={"InstanceIds": ["i-01ad5eca707e4445f"]})
```

**Step C — start:**

```
aws_query(account="nelanco", service="ec2", operation="StartInstances",
          parameters={"InstanceIds": ["i-01ad5eca707e4445f"]}, confirm_write=true)
```

**Step D — poll until healthy** (`InstanceStatus.Status == "ok"`, not merely `initializing`; this
takes ~30–60 s after `StartInstances`):

```
aws_query(account="nelanco", service="ec2", operation="DescribeInstanceStatus",
          parameters={"InstanceIds": ["i-01ad5eca707e4445f"]})
```

The EIP (`100.57.50.48`) survives stop/start — it is an Elastic IP associated with the instance.

## 3. Restore the Envoy tmux sessions

After the box is reachable again (give sshd a few seconds after `InstanceStatus: ok`), verify and
restore. The two systemd units (`claude-telegram-monitor.service`, `envoy-mention-watcher.service`)
auto-start on boot and should already be `active`; the **tmux sessions do not** auto-start and must
be recreated.

**Step 1 — confirm reachability + units:**

```
ssh_run(host="nelanco-claude", command="uptime; systemctl is-active claude-telegram-monitor.service envoy-mention-watcher.service")
```

**Step 2 — check sessions (will show "no server" after a stop/start):**

```
ssh_run(host="nelanco-claude", command="tmux ls")
```

**Step 3 — spin up the four sessions** (kills any stale sessions and recreates
`supervisor` / `planner` / `analyst` / `private-reflections`; allow ~2–3 min for the script's
internal sleeps):

```
ssh_run(host="nelanco-claude", command="~/bin/envoy-spinup.sh", timeout_secs=300)
```

**Step 4 — verify all four sessions are alive and running `claude` with bypass permissions:**

```
ssh_run(host="nelanco-claude", command="tmux ls; pgrep -af 'claude --name'")
```

Expected: four `claude --name <role> --permission-mode bypassPermissions --remote-control <role>`
processes, one per session.

**Step 5 — confirm the supervisor actually adopted its loop** (the spin-up prompt can get garbled
by its own "confirm trust" `2` keystrokes and the supervisor can drift onto a tangent). Capture the
pane and check it is `git pull`-ing `agentic_ai_context` and reading `handoffs/HANDOFF_MANIFEST.md`,
not doing something unrelated:

```
ssh_run(host="nelanco-claude", command="tmux capture-pane -t supervisor -p | tail -30")
```

If it drifted, redirect it (send Escape then the role directive — see §6 gotchas).

## 4. Fleet access (Sophia prerequisite)

Sophia reaches the box via `ssh_run(host="nelanco-claude", …)`, which resolves through the
`FLEET` registry in `app/tools/ssh_tools.py`. The `nelanco-claude` entry must exist (added
2026-10-25, `key: ~/.ssh/sophia_infra`). Sophia's public key
(`truesight-autopilot-…`, the `~/.ssh/sophia_infra` key) is already in the box's
`~/.ssh/authorized_keys`, and the box's SG allows `0.0.0.0/0:22`, so no further key/SG work is
needed. If `ssh_run` ever returns "unknown host", the FLEET entry regressed — re-add it.

## 5. Verification checklist

- [ ] `DescribeInstanceStatus` → `InstanceState: running`, `SystemStatus: ok`, `InstanceStatus: ok`
- [ ] `ssh_run(host="nelanco-claude", command="uptime")` returns (box is back, not just status-ok)
- [ ] `claude-telegram-monitor.service` and `envoy-mention-watcher.service` are `active`
- [ ] `tmux ls` shows exactly `supervisor`, `planner`, `analyst`, `private-reflections`
- [ ] `pgrep -af "claude --name"` shows four processes with `--permission-mode bypassPermissions`
- [ ] Supervisor pane shows it pulling/reading the handoff manifest (loop adopted), not drifting

## 6. Gotchas

- **Never `RebootInstances`** — it does not restore reachability for this fault (incident 2).
  Always stop → start.
- **`~/.local/bin/claude` can be a stale symlink** to a 0-byte placeholder in
  `~/.local/share/claude/versions/<ver>` (the auto-updater tries and fails because the npm prefix
  is root-owned). Harmless today because `claude` resolves to `/usr/bin/claude` (v2.1.197) — but if
  sessions start failing with "Permission denied", check `readlink -f ~/.local/bin/claude` and
  re-point or remove it. The box prints `✘ Auto-update failed: no write permission to npm prefix`
  on every session start — cosmetic, ignore (or fix the npm prefix ownership separately).
- **The spin-up script sends literal `2` keystrokes** to auto-confirm the "trust folder" prompt. If
  no such prompt appears, those `2`s reach Claude as stray input and can make a session (especially
  `supervisor`) misinterpret its directive. Re-direct via `tmux send-keys -t supervisor Escape` then
  the role prompt (see `ENVOY_TMUX_SESSIONS.md`).
- **Box-down = un-supervised Sophia threads.** Treat an impaired box as urgent: unfinished handoffs
  are not being supervised while it's dark. Consider a CloudWatch alarm on
  `StatusCheckFailed_Instance` for `i-01ad5eca707e4445f` so a recurrence pages someone (tracked in
  `OPEN_FOLLOWUPS.md`).
- **Credentials.** AWS calls use account `nelanco` (`truesight_dao_autopilot` IAM user, creds in
  `AWS_ACCESS_KEY_ID_NELANCO` / `AWS_SECRET_ACCESS_KEY_NELANCO` in the autopilot `.env`). The
  operator Mac's `~/.aws/credentials` `[nelan]` profile is **stale (InvalidClientTokenId)** — do not
  rely on it.

## 7. Escalation

If stop/start does not restore reachability after a full poll cycle, or if the failure recurs faster
than ~1/week, stop and surface to Gary rather than looping: the recurring root cause (host-level AWS
hardware fault vs. guest-OS hang) has not been determined, and may need `get-console-output` review
or an AWS support case. See `OPEN_FOLLOWUPS.md` §"`nelanco-claude` (Envoy's box) — recurring
instance-reachability failure".
