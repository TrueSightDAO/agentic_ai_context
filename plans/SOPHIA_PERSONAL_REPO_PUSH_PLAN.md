# Sophia: personal (non-DAO) repo push tool — execution plan

## Goal

Let Sophia push to a contributor's **personal, private, non-DAO** GitHub repo (e.g.
`garyjob/perch-market-analysis`) when explicitly asked to log personal work there, using a
credential the contributor has stored in her credential vault. Today she can't do this at all —
her only git tool (`git_tools.py`) is hardcoded to `TrueSightDAO/*` repos over SSH.

Background: `PERSONAL_CONTRIBUTOR_BACKLOGS.md` (this repo) is an opt-in registry pairing a
contributor → their private repo → a named vault credential. This plan builds the code that
actually consumes that pairing. Requested by Gary Teh (governor), 2026-07-20.

## Authorization envelope (§5e)

- **Pre-authorized:** implementing this in `truesight_autopilot` on a feature branch, opening a
  PR. Writing/running tests locally. No further asks needed for that.
- **Gated (human required, standard §5c gates — not relaxed by this plan):**
  - Merging the PR to `truesight_autopilot`'s default branch.
  - Deploying the merged code to the live `sophia.truesight.me` service (separate step after
    merge — `truesight_autopilot` does not auto-deploy on merge; deploy is `scripts/deploy.sh`
    or the existing `deploy_autopilot` tool, both already governor-gated).
  - **Dependency, also gated:** `TrueSightDAO/agentic_ai_context` PR #699 (adds
    `PERSONAL_CONTRIBUTOR_BACKLOGS.md` to `main`) must be merged before this tool can find any
    registry entries in production — it currently only exists on a feature branch. That PR is
    already open and awaiting Gary's review; this plan doesn't touch it further.
- Nothing about this feature — including the vault credential it consumes — should ever be
  returned in chat/logs. That's an existing, non-negotiable constraint (see pre-flight below),
  not a new gate to ask about.

## Pre-flight (§5d — everything PR1 needs is captured here; no mid-turn cross-file discovery)

### 1. The registry it reads (`PERSONAL_CONTRIBUTOR_BACKLOGS.md`, this repo, on `main` once #699 merges)

Table format (`## Registry` section):
```
| Contributor | Backlog repo | Format | Vault credential name |
|---|---|---|---|
| Gary Teh | `github.com/garyjob/perch-market-analysis` (private) | `BACKLOG.md` — ... | `PERSONAL_GITHUB_PAT` (in `sophia.truesight.me/vault/`) |
```
Convention section says: trigger = contributor explicitly flags personal, non-DAO work; never
act on an unregistered contributor or an unflagged request.

### 2. Existing DAO-repo push pattern to mirror (`truesight_autopilot/app/tools/git_tools.py`)

- `_remote_url(repo)` → `f"git@github.com:TrueSightDAO/{repo}.git"` (line 58) — **the new tool
  must NOT use this; personal repos are arbitrary owners over HTTPS with a PAT, not SSH.**
- `git_push_changes(repo, branch, commit_message, writes, edits, deletes, base_branch, pr_title,
  pr_body, open_pr)` (line 102) does: validate repo against `settings.allowed_repos` /
  `api_only_repos` / `prod_repos` (lines 122–144) → shallow clone (`--depth 1`, optional
  `--branch base_branch`) → **refuse if `branch` is the default/`main`/`master`** (lines 172–178,
  this refusal is the core anti-direct-push guardrail — replicate it exactly) → checkout `-b
  branch` → apply `writes`/`edits`/`deletes` via `_safe_repo_path` (path-traversal guard, line
  88) → commit → push → optionally open a PR via `httpx.post` to
  `https://api.github.com/repos/TrueSightDAO/{repo}/pulls` with `Authorization: Bearer
  {settings.github_pat}` (lines 267–291).
- `TOOL_SPEC = ToolSpec(name=..., description=..., parameters={...})` exported at module level
  (lines 308+) is how it's registered — see discovery mechanism below.

### 3. Vault API (`truesight_autopilot/app/vault.py`, `app/tools/vault_tools.py`)

- `get_vault()` returns the singleton `Vault`. `vault.has_credential(name) -> bool`,
  `vault.get_ref(name) -> CredentialRef` (metadata: purpose/scopes/version/created_by, no
  value), `vault.get_value(name) -> str` (the **only** method that returns the actual secret —
  call it server-side, in the new tool's handler, and never put its return value anywhere that
  reaches the LLM response, a log line, or a returned dict).
- `vault_tools.py`'s `check_credential(name)` / `report_missing_credential(name, purpose)` are
  the existing chat-safe wrappers (metadata only, never the value) — reuse
  `report_missing_credential`'s message shape for the "credential not in vault" error case
  instead of writing new copy.
- Access policy: `policy.py::may_access_secret(identity) -> bool` is `True` only for governors —
  already the right gate to import and check.

### 4. Fetching the registry file (`truesight_autopilot/app/tools/github_tools.py`)

- `read_repo_file(repo: str, path: str, ref: str = "main") -> dict` (line 23) hits
  `https://api.github.com/repos/TrueSightDAO/{repo}/contents/{path}`, returns `{"type": "file",
  "content": <decoded str>, "size": ..., "url": ..., "encoding": ...}` (base64-decoded already).
  Call `read_repo_file("agentic_ai_context", "PERSONAL_CONTRIBUTOR_BACKLOGS.md", "main")` to get
  the registry text — **no new fetch code needed.**
- Parse: split the `## Registry` table into rows, match the row whose **Contributor** cell
  equals the calling governor's name (exact match — see identity source below). No general
  markdown parser needed; the table has a fixed 4-column shape (see §1). Extract **Backlog repo**
  and **Vault credential name** cells from the matched row. No new JSON sidecar file — the `.md`
  table is the single source of truth; keep the parser tolerant of the backtick/markdown
  formatting already in those cells (strip backticks, parenthetical asides like `(private)`).

### 5. Identity at dispatch time (`truesight_autopilot/app/main.py` line ~1689)

Tool handlers receive a `context` dict: `{"history": ..., "session_id": ..., "governor_name":
...}`. **`context["governor_name"]` is the calling identity** — this is what the new handler
cross-checks against the registry's Contributor column. This is the critical guardrail that
doesn't exist anywhere else in the codebase yet: every other write tool (`git_push_changes`,
etc.) operates on DAO-owned resources where any governor may act; this tool operates on a
**personally-owned** resource, so it must refuse if the registry row for the *calling* governor
doesn't match the *requested* repo — Gary's session must not be able to push to a different
contributor's repo even if one is registered.

### 6. Tool auto-discovery + role/policy gating

- `tool_registry.py::_iter_tool_modules()` walks `app/tools/*.py` via `pkgutil.iter_modules` and
  collects any module-level `TOOL_SPEC` / `TOOL_SPECS`. **No manual registration step** — drop a
  new file `app/tools/personal_git_tools.py` with a `TOOL_SPEC` and it's discovered automatically.
- `policy.py::classify_action(tool_name)` has a `write_tools` set (line ~294, includes
  `"git_push_changes"`) and an as-yet-empty `secret_tools` set (line ~322, comment: *"Phase 3
  will add vault access tools here"*) — **add the new tool's name to both**: `write_tools`
  because it mutates a remote repo, `secret_tools` because it's the first tool that actually
  calls `vault.get_value()` to *use* a secret (not just check for one). Confirm in `main.py`
  around line 1670 how `ActionClass.SECRET` is enforced today (currently unused since
  `secret_tools` is empty) — if it isn't wired to a stronger gate than `WRITE` yet, that's fine
  to note as a pre-existing gap, not something this PR needs to fix, but the classification
  should be correct regardless.
- `roles.py`: tools with no `tools=[...]` restriction on a role are available to that role (the
  "General DAO Assistant" role, `tools=[]`, means "all"). No change needed there unless a
  specialized role's tool allowlist should include it — out of scope for PR1; the general role
  covers Gary's use case.

### ✅ Pre-flight Completeness (§5d)

No execution unit below requires reading a file/state not already captured above.

## Sequenced plan (§5a — ONE PR, one execution turn)

**PR1 — `truesight_autopilot`: `personal_git_tools.py`**

- New file `app/tools/personal_git_tools.py`:
  - `push_to_personal_repo(target_repo, branch, commit_message, writes=None, edits=None,
    deletes=None, pr_title="", pr_body="") -> dict` handler. Steps, per §4/§5 above:
    1. Read `context["governor_name"]`; refuse if empty.
    2. `read_repo_file("agentic_ai_context", "PERSONAL_CONTRIBUTOR_BACKLOGS.md", "main")`, parse,
       find the row for this governor.
    3. Refuse (clear message, points at the registry doc) if: no row found; row's repo doesn't
       match `target_repo`; row has no credential name; `branch` is empty/default/`main`/`master`
       (mirror `git_tools.py`'s exact refusal).
    4. `vault.has_credential(name)` → if false, return `report_missing_credential`'s message
       shape.
    5. `token = vault.get_value(name)` — used immediately to build the HTTPS remote URL
       (`https://x-access-token:{token}@github.com/{target_repo}.git`), passed to `git` via a
       short-lived env var or credential helper, **never** interpolated into a logged string, a
       `subprocess` arg list visible in `ps`, or the returned dict.
    6. Clone (depth 1), checkout `-b branch`, apply `writes`/`edits`/`deletes` (reuse the same
       validation semantics as `git_tools.py`'s `_safe_repo_path` / edit-count-must-be-1 rules —
       either factor those two helpers into a small shared module imported by both files, or
       duplicate them; prefer factoring since it's ~20 lines and avoids drift, but don't change
       `git_tools.py`'s existing public behavior or its tests).
    7. Commit, push, open PR against the personal repo via the GitHub REST API using the **same
       vault token** (personal repos aren't under `TrueSightDAO`, so `settings.github_pat` is not
       usable here — the vault credential itself must have repo-scoped PR-creation permission,
       which is Gary's design choice per his existing `PERSONAL_PAT` / `PERSONAL_GITHUB_PAT`).
    8. Return `{"status": "success", "repo": ..., "branch": ..., "pr_url": ...}` — never include
       the token or any header containing it.
  - `TOOL_SPEC` with a description that's explicit about scope: personal/non-DAO only, requires a
    registry entry, governor-only.
- Edit `app/policy.py`: add the tool name to `write_tools` and `secret_tools` (§6).
- Tests (new `tests/test_personal_git_tools.py`, following the existing `tests/test_vault*.py` /
  git_tools test patterns in this repo): registry-row-not-found refusal; repo-mismatch refusal;
  missing-credential refusal; default-branch-push refusal; a happy path against a `file://` test
  remote (same trick `git_tools.py`'s own tests use — check `tests/` for the existing pattern
  before writing a new one) confirming the token never appears in the returned dict or logs.
- PR description: goal, changes, testing (what the new tests cover), rollout (note the #699
  dependency from the authorization envelope above; note deploy is a separate, later, gated
  step).

## Resume tracker

**RESUME HERE →** PR1 opened (truesight_autopilot#280) — awaiting human review + merge. Do not
merge or deploy without the governor's explicit go-ahead (see authorization envelope above).

| Unit | Status | PR opened | Merged (human) | Deployed (human, separate gate) |
|---|---|---|---|---|
| PR1 — `personal_git_tools.py` + policy.py classification + tests | done, PR open | ☑ [#280](https://github.com/TrueSightDAO/truesight_autopilot/pull/280) | ☐ | ☐ |

Dependency: `agentic_ai_context` PR #699 — **merged** 2026-07-21. Registry is live on `main`.

**Correction found during PR1 (2026-07-21):** §6 above says to add the tool to both
`write_tools` and `secret_tools` in `policy.py`. That's wrong — `policy.py::evaluate()` treats
`ActionClass.SECRET` as an *unconditional* deny ("secret values are never returned through
chat"), checked before `WRITE`, which would make the tool permanently uncallable. The tool never
returns the credential value (only uses it server-side), so it belongs in `write_tools` only.
PR #280 implements it correctly; this note is so a future reader of this plan doesn't copy the
original (wrong) instruction.

## UAT

Human-facing surface: Sophia's chat interface (Telegram / DApp `chat.html`), invoked by a
governor asking her to log personal work.

1. **Surface:** Telegram DM or topic where Gary chats with Sophia (post-deploy, on the live
   service — this step happens only after the deploy gate, separately from PR1 merging).
2. **Interaction:** Gary asks Sophia to log a test entry to his personal backlog repo.
3. **Expect:** Sophia reports a PR URL against `garyjob/perch-market-analysis` (not a direct push
   to its default branch); the PR contains a sensible `BACKLOG.md` edit.
4. **Eyeball:** open the PR — confirm no token/credential value appears anywhere in the diff,
   commit message, or PR body.
5. **Negative check:** ask Sophia (or have her simulate) a push attempt for a repo NOT in the
   registry, or for a different contributor's repo — confirm she refuses with a clear message
   rather than silently no-op'ing or, worse, acting on the wrong repo.
6. **Acceptance:** pass = PR appears correctly scoped and credential-free; refusal cases refuse
   with clear messages; fail = any credential leakage, any push to an unregistered/mismatched
   repo, or any direct push to a default branch.

## Notes for whoever executes PR1

- This is security-sensitive code in a live autonomous service. Favor refusing and returning a
  clear error over any ambiguous case (unmatched registry row, malformed table, empty governor
  name) — same "never fail open" posture `git_tools.py` already uses for `prod_repos` /
  `api_only_repos`.
- Report the DAO contribution for this PR per `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md` after it
  merges, before considering the plan complete.
