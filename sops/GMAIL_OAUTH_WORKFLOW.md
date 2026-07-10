# Gmail OAuth — local tokens for automation (e.g. outreach + Sheets)

This describes how **you** obtain and store **user** OAuth tokens for a Gmail mailbox (e.g. `garyjob@agroverse.shop`) so assistants or scripts in this workspace can **read/search** and **send** mail **without** checking secrets into Git.

---

## What goes where (never commit secrets)

| Item | Location | In Git? |
|------|----------|--------|
| OAuth Desktop client JSON | `market_research/credentials/gmail/client_secret.json` | **No** — gitignored via `credentials/gmail/.gitignore` and repo `*.json` rules |
| Access + refresh token file | `market_research/credentials/gmail/token.json` | **No** |
| This documentation | `agentic_ai_context/GMAIL_OAUTH_WORKFLOW.md` | Yes (no secrets) |
| Authorization script | `market_research/scripts/gmail_oauth_authorize.py` | Yes |

**Do not** paste refresh tokens, `token.json`, or `client_secret.json` into GitHub, issues, or long-lived chat logs. If you need an AI agent to use Gmail, prefer **workspace file access** to the local `token.json` path after you have authorized on the same machine—or use a secrets manager for production.

---

## One-time Google Cloud setup

1. **Enable Gmail API:**  
   [Enable Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com)

2. **OAuth consent screen** (APIs & Services → OAuth consent screen):  
   - Add app name, user support email.  
   - **Scopes:** include  
     - `https://www.googleapis.com/auth/gmail.modify`  
     (covers read/search, **send**, **drafts**, **labels** — required for `suggest_manager_followup_drafts.py`).  
   - If you previously used only `gmail.readonly` + `gmail.send`, **delete** `token.json` and re-run the authorize script after adding `gmail.modify` to the consent screen.  
   - If the app is in **Testing**, add **`garyjob@agroverse.shop`** (and any test accounts) under **Test users**.

3. **Credentials → Create OAuth client ID → Desktop app** → download JSON → save as:  
   `market_research/credentials/gmail/client_secret.json`

---

## Install dependencies (market_research venv)

From `market_research/`:

```bash
source venv/bin/activate   # or create venv if needed
pip install -r requirements.txt
```

(`google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2` are already listed.)

---

## Authorize in the browser (creates `token.json`)

```bash
cd /path/to/market_research
python3 scripts/gmail_oauth_authorize.py
```

- A browser window opens; sign in as **`garyjob@agroverse.shop`** (or whichever mailbox should be automated).  
- On success, the script writes **`credentials/gmail/token.json`**.  
- Script prints a short **non-secret** summary (paths, scopes, whether a refresh token is present).

**Re-authorize** if you change scopes, revoke access, or rotate the OAuth client: delete `token.json` and run the script again.

**CI / GitHub Actions:** Scripts (`sync_email_agent_followup.py`, `sync_email_agent_training_data.py`, `suggest_manager_followup_drafts.py`) load credentials via **`market_research/scripts/gmail_user_credentials.py`**.

| Mode | Behavior |
|------|-----------|
| **Local** | Use **`credentials/gmail/token.json`** (or leave `GMAIL_TOKEN_JSON` unset). After Google’s client library refreshes the short-lived access token, the **file is updated** so the next run still works. |
| **CI (e.g. GitHub Actions)** | Set **`GMAIL_TOKEN_JSON`** to the **entire JSON string** of `token.json` (a **repository or environment secret**). If non-empty, it **takes precedence** over the file. The library may still **refresh the access token in memory** during the job, but **nothing writes the new tokens back to GitHub** — repository secrets are read-only from the workflow’s point of view. **`GMAIL_TOKEN_JSON` in the secret stays whatever you pasted until you change it.** That is usually fine while the **refresh_token** inside that JSON remains valid. |

### When CI Gmail starts failing (401 / invalid_grant / “refresh token” errors)

- **OAuth refresh in CI does not update the secret.** Do not expect a workflow to “self-heal” the stored token.
- **Fix:** On your machine, run **`python3 scripts/gmail_oauth_authorize.py`** again (or copy a fresh **`credentials/gmail/token.json`** after re-auth), then **replace** the GitHub secret **`GMAIL_TOKEN_JSON`** with the **full new file contents** (same as initial setup).
- Typical causes: refresh token revoked, password/consent changed, OAuth client rotated, scope change requiring new consent, or Google policy expiry for unused refresh tokens.

To create the secret: locally copy the one-line-safe approach — paste the raw file contents into GitHub **Secrets → New repository secret** named e.g. `GMAIL_TOKEN_JSON` (multi-line JSON is supported). In the workflow:

```yaml
env:
  GROK_API_KEY: ${{ secrets.GROK_API_KEY }}
  GMAIL_TOKEN_JSON: ${{ secrets.GMAIL_TOKEN_JSON }}
```

Do **not** commit `token.json` or log `GMAIL_TOKEN_JSON`.

`client_secret.json` is only needed for the **browser** authorize script on a developer machine; scheduled CI jobs typically need only **`GMAIL_TOKEN_JSON`** (+ Sheets service account for sheet writes).

---

## How an AI assistant should use this later

1. **Do not** ask the user to paste refresh tokens into chat unless necessary; prefer **`token.json`** on disk locally, or **`GMAIL_TOKEN_JSON`** from the environment in CI.  
2. Use **`load_gmail_user_credentials()`** (see `scripts/gmail_user_credentials.py`); libraries refresh the short-lived access token using the **refresh_token** in that JSON.  
3. For Sheet-driven outreach: read lead state from the Sheet, call Gmail with those credentials—keep **business logic** in scripts; keep **secrets** off git.

### Hit List + “Email Agent Follow Up” sync

- Script: **`market_research/scripts/sync_email_agent_followup.py`**  
- Reads **Hit List** rows with **Status** = `Manager Follow-up` and non-empty **Email**, queries **Gmail** `in:sent to:…`, appends new rows to **`Email Agent Follow Up`** (dedup by `gmail_message_id`).  
- Details and column schema: **`market_research/HIT_LIST_CREDENTIALS.md`** § Email Agent Follow Up.

### Manager follow-up **draft** suggestions (`garyjob@agroverse.shop`)

- Script: **`market_research/scripts/suggest_manager_followup_drafts.py`**  
- Verifies Gmail profile is **`garyjob@agroverse.shop`** (override with `--expected-mailbox` if needed).  
- Creates **`drafts.create`** in Gmail, applies user label **`Email Agent suggestions`**, appends **`Email Agent Suggestions`** sheet rows.  
- Requires **`gmail.modify`** in consent screen + `token.json` or **`GMAIL_TOKEN_JSON`**; use `--dry-run` first.

---

## Related repo notes

- **`market_research/credentials/gmail/README.md`** — quick pointer for humans.  
- **`WORKSPACE_CONTEXT.md`** §3a — never commit credentials; verify `git status` before push.  
- **`GOOGLE_API_CREDENTIALS.md`** — service accounts & Sheets; **Gmail user mail** uses this OAuth flow, not those service account files.

---

## Rotating or revoking

- **Google Account → Security → Third-party access** — revoke the app if needed.  
- Delete local `token.json` and run `gmail_oauth_authorize.py` again to mint a new refresh token.
