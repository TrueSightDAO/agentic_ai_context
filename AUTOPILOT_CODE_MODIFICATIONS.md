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

---

## Two-Stage Vision Pipeline (QR Codes, Cacao Bags)

When a governor uploads images via `/chat/upload`:

```
User uploads HEIC image
        │
        ├── 1. HEIC → JPEG conversion (macOS sips)
        ├── 2. pyzbar: authoritative barcode scan (QR, EAN13, UPC, CODE128, etc.)
        │         Returns exact decoded values. Multi-scale (full res + 50%).
        │
        ├── 3. Grok (xAI): vision analysis via grok-4-1-fast-non-reasoning
        │         Provides visual context: product guess, farm name, label text,
        │         photo quality, QR label location, QR/barcode GUESSES with
        │         confidence scores (0.0-1.0). Gimped by "Grok GUESSED" prefix.
        │
        └── 4. DeepSeek: receives pyzbar authoritative codes + Grok visual context
                  Uses lookup_qr_code tool to resolve against DAO ledger
                  Suggests dao_client commands (INVENTORY MOVEMENT, etc.)
```

### Grok System Prompt

`app/grok_client.py` contains the prompt that teaches Grok about Agroverse QR naming conventions (`2024OSCAR_20260330_33`, `LA_CC_20260414_1`, `CC` vs `CT` product tokens). Grok returns JSON with `qr_codes_guessed` (with confidence), `barcodes_guessed`, `image_description`, `label_text_visible`, `photo_quality`, `qr_label_location`, `qr_label_present`.

### QR Scanner (pyzbar)

`app/tools/qr_scanner.py` wraps libzbar via pyzbar for local, fast, reliable barcode reading. Supports: QRCODE, EAN13, EAN8, UPC-A, UPC-E, CODE128, CODE39, I25. Fallback to `zbarimg` CLI if pyzbar unavailable.

### Agentic Chat Loop

The chat pipeline (`_stream_chat` in `main.py`) now supports up to **5 rounds** of tool calls (was 2). After each round, if the LLM returns more tool calls, they're executed and the loop continues. Only exits when the LLM returns text without tool calls.

### DeepSeek XML Tool-Call Fallback

DeepSeek-chat sometimes emits tool calls as XML in the content field (`<function_calls><invoke name="...">`) instead of using the OpenAI `tool_calls` array. `LLMClient.extract_tool_calls()` in `llm_client.py` detects this XML syntax, parses it into proper tool calls, and strips the XML from visible content. Logged via `_log_raw_llm()` for debugging.

### Governor Identity Injection

On first message per session, the autopilot injects `[GOVERNOR_IDENTITY: You are speaking with Gary Teh. When they say 'I', 'me', or 'my', they mean Gary Teh.]`. Looked up from the governor registry (`dao_members.json`) by matching the RSA public key. This means the LLM knows who the user is without them having to say "I'm Gary."

---

## Session Management & Debugging

### Session Persistence

Sessions are keyed by `public_key + X-Session-Id` header. The frontend (`chat.html`) generates a UUID stored in `sessionStorage` — persists across page refreshes within the same tab, resets in a new tab. Sessions survive server restarts (loaded from `/tmp/autopilot_sessions/` on startup).

### Debug Logs

Three log types in `/tmp/autopilot_sessions/`:

| File | Contents |
|------|----------|
| `{hash}.json` | Full conversation history — all messages, tool calls, and tool results |
| `{hash}_debug.log` | Raw DeepSeek responses pre-parsing — catches XML leaks, QR misreads, malformed JSON |
| `_latest.json` | Quick pointer to the most recently active session (hash + timestamp) |

### Production Considerations

For production (`chatbot.truesight.me`):

1. **Persistent storage**: `/tmp/` is volatile on EC2 restarts. Use `/opt/truesight_autopilot/sessions/` (persistent EBS mount). Configure via `SESSION_LOG_DIR` env var.

2. **Rotation**: Sessions and debug logs grow unbounded. Add a cron job or in-process cleanup: delete sessions older than 7 days, keep max 50 session files.

3. **Privacy**: Session logs contain full conversation history including QR codes, product names, and governor identity. These should be treated as sensitive — restrict filesystem permissions (600 for log files) and omit from EC2 AMIs and snapshots.

4. **Debug log toggle**: Raw LLM logging (`_debug.log`) can be noisy in production. Consider gating behind an env var: `LOG_RAW_LLM=true` or `DEBUG=true`.

5. **Multi-governor**: Each governor gets their own session file (keyed by public_key + session ID). No cross-contamination. When onboarding new governors, ensure their names are in the governor registry (`GOVERNOR_NAMES` env var or `dao_members.json`).
