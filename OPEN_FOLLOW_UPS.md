# Open Follow-Ups

This document tracks recurring issues, tooling gaps, and infrastructure improvements that need human intervention to resolve. Updated by the autopilot when it encounters a problem it cannot fix on its own.

---

## 1. Large File Updates via GitHub API

**Date:** 2026-05-31  
**Filed by:** Autopilot  
**Priority:** Medium

### Problem

The autopilot cannot update existing files larger than ~15KB on GitHub repos. The `upload_file_to_github` tool only supports creating new files (no SHA parameter for updates), and the `http_fetch` tool has a body parameter limit that truncates payloads larger than ~20KB of base64-encoded content.

This means any edit to a file like `agroverse_shop_beta/farms/paulo-la-do-sitio-para/index.html` (28KB) is impossible through the current toolset.

### What's Needed

One of:

1. **SSH key + git client** on the autopilot box — allows `git clone`, `git commit`, `git push` for any file size. This is the most general solution.
2. **A `github_update_file` tool** — a new tool that accepts `repo`, `path`, `sha`, `content`, `message` and calls the GitHub Contents API's PUT endpoint (which handles large files fine). The current `upload_file_to_github` only does POST (create), not PUT (update).
3. **A `github_create_blob` tool** — exposes the Git Data API's blob creation endpoint, which accepts base64 content. Then the autopilot can chain blob → tree → commit → ref update for any file size.

### Workaround

For now, the autopilot can describe the exact search/replace changes needed, but cannot execute them on files >15KB. A human or another LLM with direct GitHub API access must apply the changes.

### Affected Files (examples)

- `agroverse_shop_beta/farms/paulo-la-do-sitio-para/index.html` (28KB)
- `agroverse_shop_prod/farms/paulo-la-do-sitio-para/index.html` (28KB)
- `truesight_me_prod/js/program-shell.js` (24KB)
- `truesight_me_beta/js/program-shell.js` (24KB)
- Any large HTML/CSS/JS file in the repos

---

## 2. SSH Key / Git Client Missing

**Date:** 2026-05-31  
**Filed by:** Autopilot  
**Priority:** Medium

### Problem

The autopilot box does not have SSH keys configured for GitHub, nor a git client installed. This prevents any native git operations (clone, commit, push, pull, merge).

### What's Needed

- An SSH deploy key added to the TrueSightDAO GitHub org (or a specific set of repos) with write access.
- The private key installed on the autopilot box at `~/.ssh/id_rsa` (or similar).
- `git` installed on the box.

### Benefit

With SSH + git, the autopilot could:
- Clone any repo, make changes, commit, and push — no file size limits.
- Create branches and PRs natively.
- Merge PRs when instructed.
- Handle merge conflicts.

---

## 3. `open_fix_pr` Repo Whitelist

**Date:** 2026-05-31  
**Filed by:** Autopilot  
**Priority:** Low

### Problem

The `open_fix_pr` tool only supports a subset of repos. Notably missing: `agroverse_shop_beta`, `agroverse_shop_prod`, `truesight_me_beta`, `truesight_me_prod`.

### What's Needed

Add these repos to the `open_fix_pr` tool's `repo` enum parameter so the autopilot can open fix PRs on them directly.

---

## 4. `upload_file_to_github` Should Support Updates

**Date:** 2026-05-31  
**Filed by:** Autopilot  
**Priority:** Medium

### Problem

`upload_file_to_github` only creates new files. It fails with "sha wasn't supplied" when the file already exists. It needs an optional `sha` parameter to support updating existing files.

### What's Needed

Add an optional `sha` parameter to `upload_file_to_github`. When provided, the tool should call the GitHub Contents API's PUT endpoint (update) instead of PUT (create).
