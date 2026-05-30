# Sophia Development Workflow

## How to extend the Sophia codebase

Sophia (truesight_autopilot) runs on an EC2 instance at `100.52.234.163`. The code lives at `/opt/truesight_autopilot/` and is a git clone of `github.com/TrueSightDAO/truesight_autopilot`.

### Development workflow

1. **Clone the repo locally** (on your dev machine, NOT on the EC2):
   ```bash
   git clone git@github.com:TrueSightDAO/truesight_autopilot.git
   ```

2. **Make code changes** in your local clone, commit, push to a branch, and open a PR.

3. **Deploy to EC2** by either:
   - Merging to `main` and then SSHing into the EC2 to `git pull` + `systemctl restart truesight-autopilot`, OR
   - Using the autopilot's `/admin/deploy` endpoint (which does `git pull` + restart).

### Mirror folder pattern

When extending Sophia's codebase, the recommended pattern is:

1. **`git clone`** the `truesight_autopilot` repo into a **mirror folder** on your dev machine.
2. Make code changes from that **git repo** (not from a detached copy).
3. Commit, push, PR, merge, then deploy.

This ensures:
- Version history is preserved
- Changes are reviewable via PRs
- Multiple developers/agents can collaborate without conflicts
- The deployed instance always reflects the `main` branch

### Key files

| File | Purpose |
|------|---------|
| `/opt/truesight_autopilot/app/main.py` | FastAPI app, tool dispatch, chat streaming |
| `/opt/truesight_autopilot/app/config.py` | Settings, allowed repos, credentials |
| `/opt/truesight_autopilot/app/fix_agent.py` | Autonomous fix agent (open_fix_pr) |
| `/opt/truesight_autopilot/app/github_client.py` | GitHub API client |
| `/opt/truesight_autopilot/app/tools/` | Tool implementations (one per domain) |
| `/opt/truesight_autopilot/app/tool_registry.py` | Capability manifest / tool discovery |
| `/opt/truesight_autopilot/app/roles.py` | Role system (general, infrastructure, etc.) |
| `/opt/truesight_autopilot/app/llm/` | LLM provider abstraction (DeepSeek, etc.) |
| `/opt/truesight_autopilot/.env` | Environment variables (secrets) |

### Self-improvement loop

Sophia is part of a cybernetic adversarial loop. When patterns of errors are detected (repeated OCR failures, misread QR codes, failed submissions, context gaps, protocol violations), Sophia should:

1. Identify the pattern
2. Propose a code-level fix
3. Open a PR via `open_fix_pr` on `truesight_autopilot`
4. Report the PR URL for human review

### DNS / Infrastructure

- `sophia.truesight.me` → A record → `100.52.234.163` (the autopilot EC2)
- `oracle.truesight.me` → CNAME → `truesightdao.github.io` (GitHub Pages)
- The oracle-advisory endpoint lives at `http://100.52.234.163:8001/oracle-advisory` (same box as autopilot)
- Route53 hosted zone: `truesight.me` in AWS account `explorya`
