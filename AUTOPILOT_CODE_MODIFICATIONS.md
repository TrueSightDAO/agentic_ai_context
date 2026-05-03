# Autopilot Code Modifications — DeepSeek Agentic Loop

> How `truesight_autopilot` accepts governor chat requests to modify any TrueSightDAO repo, runs a DeepSeek agentic loop, and opens a PR for human review.

## Architecture

```
Governor (DApp chat.html)
        │
        │ POST /chat  {"message": "Add retry to hit_list_enrich_contact.py"}
        ▼
┌─────────────────────────────────────────────────────┐
│  truesight_autopilot (EC2)                          │
│                                                     │
│  1. LLMClient.chat() decides to call open_fix_pr    │
│  2. open_fix_pr tool routes to FixAgent.run()       │
│  3. FixAgent creates branch autopilot/fix-<ts>      │
│  4. Agentic loop (max 10 rounds):                   │
│     ├── read_file     (any repo under TrueSightDAO)  │
│     ├── grep_code     (search across repo)           │
│     ├── edit_file     (string replacement)           │
│     ├── create_file   (new file)                     │
│     └── delete_file   (remove file)                  │
│  5. Opens PR (DRAFT) — never auto-merges             │
│  6. Logs [CONTRIBUTION EVENT] to Edgar               │
│  7. Returns PR URL to chat                           │
└─────────────────────────────────────────────────────┘
```

## Repo Discovery

The agent calls `list_org_repos()` to discover all repos in `TrueSightDAO` at runtime. No hardcoded list — any unarchived repo is fair game.

## Content API Only — No Clones

**The agent NEVER clones repos.** All read/write operations go through the GitHub Content API (`GET /repos/{owner}/{repo}/contents/{path}`, `PUT /repos/{owner}/{repo}/contents/{path}`, `DELETE /repos/{owner}/{repo}/contents/{path}`).

This is critical for repos like `.github` which contain large static assets and would be expensive/destructive to clone. The `GitHubClient` has a docstring warning against cloning.

## Permissions

GitHub PAT (`TRUESIGHT_DAO_AUTOPILOT`) needs `Contents: write` on repos you want the agent to modify. For read-only discovery, `Contents: read` on the org is sufficient.

## Typical Repos (example — agent discovers these dynamically)

| Repo | Purpose |
|------|---------|
| `dapp` | DApp HTML/JS pages |
| `tokenomics` | GAS, Python scripts |
| `truesight_me` / `truesight_me_prod` | Static site |
| `agroverse_shop` / `agroverse_shop_prod` | E-commerce site |
| `dao_client` | Python CLI + auth |
| `market_research` | Research pipelines |
| `sentiment_importer` | Edgar Rails API |
| `.github` | README only (read, no write) |
| `truesight_autopilot` | Itself (self-heal) |

## Tool Descriptions (FixAgent)

### read_file
Read a file from any TrueSightDAO repo on a given branch.
- `repo` (str): Repo name
- `path` (str): Path relative to repo root
- `ref` (str, default: branch): Branch name

### grep_code
Search for a pattern across a repo.
- `repo` (str): Repo name
- `pattern` (str): Regex or string to search
- `path` (str, optional): Limit to subdirectory

### edit_file
Replace exact string in a file on the branch. Uses GitHub API commit.
- `repo` (str): Repo name
- `path` (str): File path
- `old_string` (str): Exact text to replace (include surrounding context for uniqueness)
- `new_string` (str): Replacement text

### create_file
Create a new file on the branch.
- `repo` (str): Repo name
- `path` (str): File path
- `content` (str): File content

### delete_file
Delete a file from the branch.
- `repo` (str): Repo name
- `path` (str): File path

### py_compile
Validate Python syntax of a file on the branch (downloads + checks locally).
- `repo` (str): Repo name
- `path` (str): File path

## Safety

- **Never auto-merges.** All fixes open as PRs. The PR is created as **DRAFT** so it cannot be merged by accident.
- **Safety hooks** block: `rm -rf`, `sudo`, `--force`, `curl|bash`, `chmod 777`, `eval()`, `exec()`.
- **Max 10 iterations** per fix loop.
- **Rate limited:** Max 5 PRs/day per repo (configurable via `MAX_PR_PER_DAY`).
- **Branch naming:** `autopilot/fix-<unix-ts>` — never touches main.
- **Edgar logging:** Every fix loop logs a `[CONTRIBUTION EVENT]` with PR URL and description.
- **Self-healing scope:** Autopilot can fix itself but changes still go through PR review.

## Chat Integration

The DApp `chat.html` calls `POST /chat` with:
```json
{
  "message": "Add a rate limiter to hit_list_enrich_contact.py",
  "payload": { "message": "..." },
  "signature": "..."
}
```

The response during a fix loop is streamed via SSE:

```
event: progress
data: {"step": 1, "message": "Reading hit_list_enrich_contact.py..."}

event: progress
data: {"step": 2, "message": "Adding retry_with_backoff decorator..."}

event: complete
data: {"pr_url": "https://github.com/TrueSightDAO/market_research/pull/42", "summary": "Added retry logic with 3 attempts and exponential backoff"}
```

If streaming is not available (simple request/response), the endpoint blocks and returns the PR URL directly:
```json
{
  "response": "I've opened a fix PR: https://github.com/TrueSightDAO/market_research/pull/42",
  "pr_url": "https://github.com/TrueSightDAO/market_research/pull/42"
}
```

## Edgar Logging

After opening a PR, autopilot submits a `[CONTRIBUTION EVENT]` to Edgar via `dao_client/modules/report_ai_agent_contribution.py`:

- **Contributor:** `autopilot@agroverse.shop`
- **Title:** `[autopilot] <repo>: <short description>`
- **Body:** Root cause, what was changed, safety review link
- **PR URL:** Link to the opened PR
- **TDGs:** 0 (autopilot doesn't earn TDGs)

## Onboarding a New Repo

To add a repo to autopilot's scope:
1. Ensure `TRUESIGHT_DAO_AUTOPILOT` PAT has `Contents: write` on the new repo
2. That's it. The agent discovers repos dynamically via `list_org_repos()`.
3. If the repo has a non-`main` default branch, the agent will learn this from the discovery response.

## Limitations

- **Non-Python files** validated by py_compile only. JS/HTML are syntax-checked on PR review.
- **Binary files** (images, PDFs) cannot be read or edited.
- **Large files** (>1MB) will be truncated by GitHub API.
- **Multi-file renames** not supported — delete then create instead.
- **Dependencies** (requirements.txt, package.json) can be edited but the agent won't `npm install` or `pip install` on the EC2.
