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

## Git Worktree Isolation

- When autopilot creates a fix PR, it must clone or worktree the target repo under /tmp/autopilot_worktrees/<repo>-<branch>
- If the worktree already exists from another concurrent governor session, append a unique suffix (e.g. -<timestamp>)
- All read_file, edit_file, create_file, delete_file operations must go through the worktree, not the GitHub Content API
- After the PR is opened and pushed, clean up the worktree
- This prevents two concurrent governor sessions from overwriting each other's changes

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

---

## Debugging Autopilot Locally

When an AI agent needs to **test, extend, or debug** the autopilot itself, follow this workflow. **CRITICAL: Never modify code directly. Always route changes through autopilot.** Fix the autopilot infrastructure first, then let autopilot make the code changes.

### 1. Starting Autopilot Locally

```bash
cd /Users/garyjob/Applications/truesight_autopilot
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 > /dev/null 2>&1 &; disown
```

`DRY_RUN=true` is safe — it **only** gates background tasks (email poller, AWS monitor). The fix agent (`open_fix_pr`) **always runs** regardless of DRY_RUN (opens DRAFT PRs, never auto-merges).

Verify: `curl http://localhost:8001/health`

### 2. Authenticating to the Chat API

The governor's RSA keys live in `dao_client/.env`:
- `PUBLIC_KEY` — SPKI base64
- `PRIVATE_KEY` — PKCS#8 base64

**The signing payload must use compact JSON** matching the server-side serialization exactly:

```python
import json, uuid, time, base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Load private key from dao_client/.env
private_key = serialization.load_pem_private_key(
    b"-----BEGIN PRIVATE KEY-----\n" + PRIVATE_KEY.encode() + b"\n-----END PRIVATE KEY-----",
    password=None
)

# Build payload — CRITICAL: separators=(",",":") matches server's json.dumps
payload_obj = {
    "message": "Your message here",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "nonce": str(uuid.uuid4())
}
payload_str = json.dumps(payload_obj, separators=(",", ":"), ensure_ascii=False)
signature = private_key.sign(payload_str.encode(), padding.PKCS1v15(), hashes.SHA256())
sig_b64 = base64.b64encode(signature).decode()

# Send to chat endpoint
resp = requests.post(
    "http://localhost:8001/chat",
    headers={
        "Content-Type": "application/json",
        "X-Public-Key": PUBLIC_KEY,
        "X-Session-Id": str(uuid.uuid4())
    },
    json={"payload": payload_obj, "signature": sig_b64},
    stream=True, timeout=120
)
```

The server expects `X-Public-Key` header plus `{"payload": {...}, "signature": "..."}` body.

### 3. The Golden Rule: Autopilot Does the Work

**Do NOT modify code directly.** If autopilot can't make a change:
- Fix the autopilot infrastructure first (config, env vars, code in `truesight_autopilot/`)
- Then tell autopilot to make the change via chat

The fix agent is safe by design:
- Opens **DRAFT** PRs (never auto-merges)
- Safety hooks block dangerous operations (`rm -rf`, `sudo`, `eval`, etc.)
- Only operates on repos in `ALLOWED_REPOS` (config.py)
- Max 10 iterations with `py_compile` validation before PR

### 4. Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| HTTP 401 from chat API | JSON serialization mismatch | Use `separators=(",", ":")` in `json.dumps()` |
| `open_fix_pr` returns None / empty | Used to be DRY_RUN gate (fixed 2026-05-06) | Ensure `app/fix_agent.py` has no DRY_RUN guard in `run_simple()` |
| Governor not recognized | Key not in `dao_members.json` | Check governor registry cache, verify key matches |
| GitHub 403 on PR creation | PAT scope too narrow | `TRUESIGHT_DAO_AUTOPILOT` needs `Contents:Write` + `Pull requests:Write` on target repos |
| Production Grok key missing | `load_grok_key()` falls back to `market_research/.env` (local-only path) | Add `GROK_API_KEY` directly to `truesight_autopilot/.env` |
| `.env` key drift between local and EC2 | Local `.env` accumulates new keys that never reach production | Run `scripts/deploy.sh` (it has a pre-sync key parity check) |

### 5. Production Deployment

**CRITICAL: Local `.env` must always be a superset of production `.env`.**  
The deploy script syncs the local `.env` to EC2. If production has a key that local doesn't, that key will be lost on deploy.

**Before deploying:**
```bash
# Show keys that exist in production but NOT locally (will be LOST on deploy):
diff <(ssh truesight-autopilot "grep -v '^#' /opt/truesight_autopilot/.env | grep -v '^$' | cut -d= -f1 | sort") \
     <(grep -v '^#' .env | grep -v '^$' | cut -d= -f1 | sort)
```

**To deploy:**
```bash
cd /Users/garyjob/Applications/truesight_autopilot
bash scripts/deploy.sh
```

The script aborts if production-only keys would be lost (override with `SKIP_KEY_CHECK=1`).

**To verify after deploy:**
```bash
curl -s https://chatbot.truesight.me/health | python3 -m json.tool | grep -E 'status|grok_key|governors'
ssh truesight-autopilot "sudo journalctl -u truesight-autopilot --no-pager -n 5 | grep -i 'initialized'"
```

### 6. Provider Switching

**To switch LLM provider:** Set `LLM_PROVIDER` in `.env` to `bigmodel` or `deepseek`.  
The registry auto-falls-back to DeepSeek if the primary provider fails to initialize.

### 7. Multi-governor

---

## QA Testing Autopilot's Work

When autopilot makes code changes (via `open_fix_pr`), **always verify the fix end-to-end before merging**. Do not trust autopilot's word alone — actually test the change in a browser.

### 5.1 Workflow

1. Autopilot diagnoses and opens a DRAFT PR
2. Merge the PR locally (or just pull the branch) and restart the DApp HTTP server
3. Write a Playwright script that reproduces the reported bug
4. Run the script — verify the bug is gone AND no regressions
5. If the fix passes QA, merge the PR
6. If it fails, tell autopilot what's still broken and iterate

### 5.2 Playwright Quick-Start

```bash
pip3 install playwright
python3 -m playwright install chromium
```

### 5.3 Test Script Template

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Seed localStorage if needed (simulates a signed-in user)
    page.goto("http://localhost:8080/chat.html", wait_until="domcontentloaded")
    page.evaluate("""
        localStorage.setItem('publicKey', '...');
        localStorage.setItem('privateKey', '...');
    """)

    # Navigate to the page under test
    page.goto("http://localhost:8080/TARGET_PAGE.html", wait_until="domcontentloaded")

    # Assertions
    body = page.text_content("body") or ""
    assert "Error message" not in body, "Error message found on page"
    assert "Expected text" in body, "Expected content missing"

    # Screenshot for visual verification
    page.screenshot(path="/tmp/qa_result.png")

    browser.close()
```

### 5.4 Common QA Checks

| Check | How |
|-------|-----|
| No reload loops | Count `framenavigated` events — should be 1 per page load |
| No error messages | Search `body` text for known error strings (`Access restricted`, etc.) |
| Correct UI state | Check element visibility, text content, button states |
| No `routes.js` probe on localhost | Verify `localStorage.getItem('routesMode')` is `null`, not `'proxy'` |
| Service worker not interfering | Test with a fresh browser context (no prior SW registration) |
| Works with seeded localStorage | Pre-populate `publicKey`/`privateKey` to simulate a logged-in user |

### 5.5 Example: QA for create_signature.html Fix

Autopilot diagnosed that `routes.js`'s `no-cors` probe to `script.google.com` was causing `window.location.reload()` on localhost, creating a reload loop when pages had query params. The fix added a localhost guard.

**Test script** (run after applying the fix):

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8080/create_signature.html?em=test%40test.com&vk=abc123",
              wait_until="domcontentloaded")
    time.sleep(2)
    body = page.text_content("body")
    routes_mode = page.evaluate("() => localStorage.getItem('routesMode')")
    assert "Access restricted to authorized governors" not in body
    assert routes_mode is None  # probe did NOT fire
    page.screenshot(path="/tmp/qa_pass.png")
    browser.close()
```

---

## 8. AWS Monitoring (multi-account, May 2026)

### 8.1 Accounts and labels

TrueSight DAO operates AWS workloads across two member-contributed accounts:

| Label       | Account ID    | Provided by | Legacy alias in env / docs    |
|-------------|---------------|-------------|-------------------------------|
| `nelanco`   | `767697632458`| Nelanco     | `CYPHER_DEFENCE_*`            |
| `explorya`  | `440626669078`| Explorya    | `TRUESIGHT_DAO_AUTOPILOT_*`   |

The labels are the contributing-member's name (lowercased). Every log line
from `app/aws_monitor.py` is prefixed with `[<label>]` so journal output
stays disambiguated when monitoring multiple accounts.

### 8.2 Env-var convention (`/opt/truesight_autopilot/.env` on production)

```
AWS_ACCOUNTS=nelanco,explorya
AWS_ACCESS_KEY_ID_NELANCO=<value>
AWS_SECRET_ACCESS_KEY_NELANCO=<value>
AWS_REGION_NELANCO=us-east-1
AWS_ACCESS_KEY_ID_EXPLORYA=<value>
AWS_SECRET_ACCESS_KEY_EXPLORYA=<value>
AWS_REGION_EXPLORYA=us-east-1
```

Source of truth for the keypair values is `cypher_def/.env` (vars
`CYPHER_DEFENCE_AWS_KEY/SECRET` and `TRUESIGHT_DAO_AUTOPILOT_AWS_KEY/SECRET`).
The autopilot `.env` is a re-mapping of those values into the
DAO-member-labeled namespace.

Backwards-compat: if `AWS_ACCOUNTS` is unset, `AWSMonitor` falls back to
the legacy single-account env (`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`
/ `AWS_REGION`) under the implicit label `default` — unchanged behavior
for any single-account deployment.

### 8.3 What gets monitored

- **CloudWatch** (`AWS/EC2` namespace): per-instance `StatusCheckFailed`
  metric, polled every 5 minutes. Active for both accounts.
- **Cost Explorer** (`get_cost_and_usage`): daily blended cost by service,
  polled once per 24h cycle. Active for both accounts.
- **AWS Health** (`describe_events`): graceful-degrades on accounts without
  Business/Enterprise support — `SubscriptionRequiredException` flips a
  per-account flag at first call, logs INFO once, and the polling loop
  silently skips the call thereafter. Currently disabled on both accounts
  (neither has a paid support plan); can be re-enabled by upgrading the
  account's support tier without code changes.

### 8.4 Verifying production state

```
ssh truesight-autopilot 'sudo journalctl -u truesight-autopilot --since "2 minutes ago" --no-pager | grep autopilot.aws'
```

Expected lines on a healthy startup (both accounts):
```
[nelanco]  AWS CloudWatch connected (account 767697632458, region us-east-1)
[explorya] AWS CloudWatch connected (account 440626669078, region us-east-1)
[nelanco]  AWS Health API unavailable (account lacks Business support). ...
[explorya] AWS Health API unavailable (account lacks Business support). ...
[nelanco]  AWS daily spend (YYYY-MM-DD): $X
[explorya] AWS daily spend (YYYY-MM-DD): $X
```

If only one account appears, check the env vars and look for a
`AWS_ACCESS_KEY_ID_<LABEL> or AWS_SECRET_ACCESS_KEY_<LABEL> missing` warning.

---

## 9. AI/proposed fix labels (PR + Gmail, May 2026)

When autopilot's email-triage loop opens a fix PR for an external error
signal, **two `AI/proposed fix` labels** are applied so Gary can find both
the PR and the source email with a single search string:

1. **GitHub PR label** — `github_client.open_pr()` accepts a `labels=[...]`
   parameter and idempotently creates+attaches them in the target repo
   (warm yellow `#f4a300`, the operator-attention convention). Both
   `FixAgent.run_simple()` and `FixAgent.run()` pass
   `labels=["AI/proposed fix"]` when opening their PRs.
2. **Gmail label on the source email** — `EmailPoller._handle()` captures
   the PR URL returned by each handler. When non-None, it calls
   `_apply_gmail_label(msg_id, "AI/proposed fix")`, which idempotently
   get-or-creates the Gmail label and attaches it via
   `users.messages.modify`. Failures log a warning but never roll back the
   PR — the GitHub PR is the authoritative artifact, the Gmail label is
   just an inbox-side index.

Operator UX: search "label:AI/proposed fix" in Gmail to triage what's
awaiting review; same string in the GitHub PR list filter shows the
corresponding PRs.

---

## 10. Email classifiers (current coverage as of May 2026)

`app/email_poller.py` Tier-1 rule-based classifier dispatches actionable
emails to typed handlers:

| Action key       | Trigger                                                        | Handler status                                            |
|------------------|----------------------------------------------------------------|------------------------------------------------------------|
| `github_failure` | Subject matches `workflow run failed / action required / scheduled workflow failed` | **Active.** Extracts repo + run_id, fetches log, diagnoses via LLM, runs FixAgent, opens PR with `AI/proposed fix` label, applies Gmail label to source email. |
| `bugsnag_error`  | Sender matches `@bugsnag.com` AND subject matches `[bugsnag] / new error / error in / reopened / spike in errors` | **v0 stub.** Parses project + error_class, logs the triage, returns None. PR-creation deferred to v0.1 pending an operator-maintained Bugsnag-project → github-repo mapping. |
| `gas_error`      | Subject matches `google apps script / script has failed / execution error` | TODO — classifier active, handler logs only. |
| `security_alert` | Subject matches `security alert / dependabot / vulnerability`  | TODO — classifier active, handler logs only. |

The Tier-2 path (LLM classification for ambiguous emails) is intentionally
not wired — keeps cost predictable. New senders / subject patterns get
added as Tier-1 regexes when worth typing.

### 10.1 Adding a new classifier

1. Define the regex(es) at module top (sender + subject when both are
   useful gates).
2. Add a branch in `_classify()` returning a new action key.
3. Add a branch in `_handle()` calling a new `_handle_<action>()` method.
4. The handler returns `pr_url | None`; the dispatcher applies the
   `AI/proposed fix` Gmail label automatically when non-None is returned.

### 10.2 Bugsnag handler v0.1 (queued)

Once the operator-maintained Bugsnag-project → github-repo mapping
ships (likely as `BUGSNAG_PROJECT_REPOS` JSON env var or a config file),
`_handle_bugsnag_error()` should:

1. Look up the repo for the parsed project name.
2. Call `FixAgent().run_simple(repo, issue_description=f"{error_class}: {first_stack_frame}")`.
3. Return the PR URL so the dispatcher labels the source email.


---

## 11. Bugsnag self-improvement loop (May 2026)

The outbound side of the Bugsnag loop is wired in `app/main.py`'s
`_init_bugsnag()` and combines with the inbound `bugsnag_error` classifier
(§10) to form a closed self-improvement loop:

```
autopilot crash / logger.error(...)
  → BugsnagHandler attached to root logger at logging.ERROR
  → bugsnag.notify() → Bugsnag dashboard
  → Bugsnag emails 'New error in autopilot' to notifications@bugsnag.com
  → autopilot's email_poller picks it up (via Gmail polling)
  → bugsnag_error classifier (§10) triages
  → AI/proposed fix PR opened against truesight_autopilot
  → AI/proposed fix Gmail label applied to the source email
  → operator reviews the PR, merges or rejects
```

### Configuration

Two env vars in `/opt/truesight_autopilot/.env`:

| Var                       | Required | Notes                                                           |
|---------------------------|----------|-----------------------------------------------------------------|
| `BUG_SNAG_API`            | Yes      | API key from Bugsnag project settings. Empty = self-reporting silently disabled. The env var name matches the existing autopilot/.env convention; `config.py` also accepts `BUGSNAG_API_KEY` as an alias. |
| `BUGSNAG_RELEASE_STAGE`   | No       | Default `production`. Bugsnag's `notify_release_stages` is `["production", "staging"]` — anything else is logged but not sent. |

### What gets reported

- **Uncaught exceptions** in any module that uses Python's standard
  logging (which is everything in autopilot).
- **`logger.error(...)` calls** anywhere in the codebase — the
  `BugsnagHandler` is attached to the root logger at level `logging.ERROR`.
- **Not reported:** `logger.warning(...)` or `logger.info(...)`. Add
  another handler tier if those need to surface.

### Reaching beyond just autopilot

`bugsnag_error` doesn't filter by project — it fires on any email from
`@bugsnag.com` matching the subject regex. So autopilot now triages
errors from **every Bugsnag project Gary has**, not just its own. First
production run picked up a `HTTPError in S3CacheJsonPagesDiff@s3_cacher`
from the `[Krake Publisher]` project automatically. Side effect: this
broadens the bugsnag_error v0.1 follow-up from "map autopilot → autopilot"
to a more general project-name → repo-name lookup table.

### Verification on production

```
ssh truesight-autopilot 'sudo journalctl -u truesight-autopilot --since "2 minutes ago" --no-pager | grep -iE "bugsnag"'
```

Expected on a healthy startup:
```
INFO:autopilot:Bugsnag self-reporting enabled (release_stage=production, project_root=/opt/truesight_autopilot)
```

To test the inbound side end-to-end: trigger any `logger.error(...)` in
autopilot (or wait for Bugsnag to email about a real upstream error),
watch for the `bugsnag_error` classification line in the journal, then
check Gmail for the `AI/proposed fix` label on the source email.

