# GitHub SSH — dedicated key for Agentic AI (`git push`)

This workspace uses a **separate Ed25519 key** for automated or agent-driven `git push` to GitHub, so your personal SSH key and day-to-day identity stay untouched.

## Paths (this machine)

| | Path |
|--|------|
| **Directory** | `/Users/garyjob/.ssh/agentic_ai_github/` |
| **Private key** | `/Users/garyjob/.ssh/agentic_ai_github/id_ed25519` |
| **Public key** | `/Users/garyjob/.ssh/agentic_ai_github/id_ed25519.pub` |

Portable form: **`$HOME/.ssh/agentic_ai_github/id_ed25519`** (and `.pub`).

**Rules**

- **Never** commit the **private** key into any repository (including `agentic_ai_context`).
- Permissions: directory `700`, private key `600`, public key `644`.

## One-time: add the public key to GitHub

1. Show the public key:  
   `cat ~/.ssh/agentic_ai_github/id_ed25519.pub`
2. GitHub → **Settings** → **SSH and GPG keys** → **New SSH key**  
   - Title e.g. `Agentic AI — MacBook` (or `Cursor agent`).
   - Key type: **Authentication Key**.
   - Paste the **single line** from `.pub`.
3. Confirm access:  
   `ssh -i ~/.ssh/agentic_ai_github/id_ed25519 -T git@github.com`  
   Expect: `Hi <username>! You've successfully authenticated...`

**Org / repo policies:** If the org enforces SSO, **authorize** this key for the org on the key’s GitHub page. For restricted repos, the GitHub user that owns this key needs **write** access.

## SSH config (recommended): host alias `github.com-agentic-ai`

Append to **`~/.ssh/config`** (create the file if missing; `chmod 600 ~/.ssh/config`):

```sshconfig
# Dedicated key for Agentic AI / automation (see agentic_ai_context/GITHUB_AGENTIC_AI_SSH.md)
Host github.com-agentic-ai
    HostName github.com
    User git
    IdentityFile ~/.ssh/agentic_ai_github/id_ed25519
    IdentitiesOnly yes
```

Then use **SSH remote URLs** with that host:

```bash
# Example: clone
git clone git@github.com-agentic-ai:TrueSightDAO/agentic_ai_context.git

# Example: fix remote in existing repo
git remote set-url origin git@github.com-agentic-ai:TrueSightDAO/your-repo.git
```

## One-off push without changing `origin`

From the repo directory:

```bash
GIT_SSH_COMMAND='ssh -i ~/.ssh/agentic_ai_github/id_ed25519 -o IdentitiesOnly=yes' git push origin main
```

Replace `main` with your branch.

## Passphrase

The generated key may use an **empty passphrase** so agents can push without interactive prompts. That is convenient and **higher risk** if the private key file is copied. To harden: regenerate with `ssh-keygen` and a passphrase, then load the key into **ssh-agent** / macOS Keychain for the session.

## Regenerating

If the key is compromised or rotated:

```bash
rm ~/.ssh/agentic_ai_github/id_ed25519 ~/.ssh/agentic_ai_github/id_ed25519.pub
ssh-keygen -t ed25519 -f ~/.ssh/agentic_ai_github/id_ed25519 -C "agentic-ai-github-TrueSightDAO"
```

Remove the old public key from GitHub, add the new `.pub`, update any CI references.

## Pull requests — branch-first workflow (agents)

**Convention for any codebase the agent edits and pushes:** do **not** push directly to `main` (or the default production branch) unless the user explicitly orders it.

1. **`git fetch`** the remote and branch from an up-to-date default branch (usually `main` / `master`).
2. **Create a new branch** per change set, with a clear prefix, e.g. `feature/…`, `fix/…`, `docs/…`, `seo/…`.
3. **Commit** with a clear subject and body: *what* changed, *why*, how to verify, risks, rollback hints.
4. **`git push -u origin <branch>`** using **`GIT_SSH_COMMAND`** or the **`github.com-agentic-ai`** host (see above).
5. **Open a Pull Request** on GitHub (web UI or `gh pr create` if available). The PR description must stand alone for human reviewers:
   - **Goal** — one sentence.
   - **Changes** — bullet list of files/areas.
   - **Testing** — what was run (e.g. `npm test`, `npm run sitemap`, manual checks).
   - **Rollout / follow-ups** — Sheets, clasp, env, or anything not in git.
6. **Leave merge** to humans unless the user says otherwise.

The compare URL is usually:

`https://github.com/<org>/<repo>/compare/<base>...<branch>?expand=1`

Replace `<base>` with the default branch name the repo uses.

## For AI agents (Cursor, etc.)

When the user asks you to **push to GitHub** and this machine should use the automation key:

1. Prefer remotes using **`git@github.com-agentic-ai:`** after the user has added the `Host` block above, **or**
2. Use **`GIT_SSH_COMMAND`** as shown, with **`~/.ssh/agentic_ai_github/id_ed25519`**.

Follow **§ Pull requests — branch-first workflow** above unless the user explicitly requests a direct push to default branch.

Confirm the remote is **SSH**, not HTTPS (`https://github.com/...`), or the SSH key will not apply.
