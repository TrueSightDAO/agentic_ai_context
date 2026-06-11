# Git Worktree Convention

**Established:** 2026-06-11 by Gary Teh (thread 2799)
**Applies to:** All Sophia incarnations (TrueSight Autopilot)

## Why

Sophia operates across multiple Telegram threads simultaneously. Each thread may have its own active git branch, pending changes, and PR. Using a single git clone for all threads causes cross-thread state clashes — a `git checkout` or `git stash` in one thread disrupts the worktree state another thread depends on.

## The rule

**All write activities (PRs, file uploads, commits) MUST use a dedicated git worktree.**

Never modify files in the primary clone (`/opt/truesight_autopilot/`) directly for a feature branch. Instead:

```bash
# Create a worktree for a feature
cd /opt/truesight_autopilot
git worktree add /tmp/worktrees/<repo>-<feature> -b <feature-branch>

# Work in the worktree
cd /tmp/worktrees/<repo>-<feature>
# ... make changes, commit, push ...

# Clean up after PR is merged
git worktree remove /tmp/worktrees/<repo>-<feature>
```

## Naming convention

Worktree directories live under `/tmp/worktrees/` and are named `<repo>-<feature>`:

- `truesight_autopilot-live-progress-pr1`
- `agentic_ai_context-handoff-registry`
- `dao_client-fix-webhook`

## Cleanup

Worktrees are ephemeral. After the PR is merged and the branch deleted, remove the worktree:

```bash
git worktree remove /tmp/worktrees/<repo>-<feature>
```

If a worktree directory is left behind (e.g. after a crash), it can be force-removed:

```bash
git worktree prune  # cleans stale worktree metadata
rm -rf /tmp/worktrees/<repo>-<feature>  # removes the directory
```

## Exceptions

- **Read-only operations** (reading files, searching code) can use the primary clone or `read_repo_file` — no worktree needed.
- **Deploy operations** (`deploy_autopilot`, `git pull` on the production checkout) run on the primary clone, not a worktree.
- **Emergency hotfixes** to production may bypass this rule, but must be documented.

## Enforcement

This is a convention, not a technical gate. Future incarnations of Sophia should follow it by habit. If you find yourself modifying files in the primary clone for a feature branch, stop and create a worktree instead.
