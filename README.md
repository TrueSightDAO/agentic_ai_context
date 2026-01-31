# Agentic AI Context

This repository holds **workspace context** for AI coding assistants (Claude Code, OpenAI Codex, Gemini CLI, Cursor, etc.). Read the files here to get up to speed on what the entire workspace is about before making changes.

## Onboarding (new to the DAO or Agroverse?)

Clone this repo and give your LLM access to it so it can get up to speed quickly:

```bash
git clone git@github.com:TrueSightDAO/agentic_ai_context.git
cd agentic_ai_context
```

Then point your editor or LLM at this folder (or at least `OPERATING_INSTRUCTIONS.md` → `WORKSPACE_CONTEXT.md` → `PROJECT_INDEX.md`). Your AI will have context on the TrueSight DAO, Agroverse (ceremonial cacao, agroverse.shop, reseller partners), Krake, and the rest of the workspace — conventions, credentials reference, and CMO playbook included.

## Contents

| File | Purpose |
|------|---------|
| **OPERATING_INSTRUCTIONS.md** | **Read this first.** Rules for reading and contributing; canonical vs. append-only vs. per-agent. |
| **WORKSPACE_CONTEXT.md** | High-level overview of the workspace: projects, tech stack, relationships, and conventions. |
| **PROJECT_INDEX.md** | Per-project summary: purpose, stack, entry points, and links to credentials/docs. |
| **CONTEXT_UPDATES.md** | Append-only log for agent notes; do not remove or rewrite lines. |
| **notes/** | Per-agent / per-session notes; create files like `cursor_2025-01-29.md`, `claude_session.md`. |
| **AI_SETUP.md** | How to check/install Claude Code, OpenAI Codex, and Gemini CLI on this machine. |
| **GOOGLE_API_CREDENTIALS.md** | Google API credentials, service accounts, OAuth clients, and ledger spreadsheet IDs (workspace-wide). |
| **CMO_SETH_GODIN.md** | **Agentic AI CMO** — Seth Godin persona and principles; read when doing marketing (copy, positioning, campaigns, growth). Consult this for CMO perspective. |
| **DR_MANHATTAN.md** | **Agentic AI — Dr Manhattan** — Strategic advisor for Agroverse + TrueSight DAO growth; read when doing strategy, priorities, or onboarding. Future use: chatbot for newcomers. |
| **GOVERNANCE_SOURCES.md** | **Governance** — Whitepaper (truesight.me/whitepaper → Google Doc), proposals (GitHub TrueSightDAO/proposals, Realms). Pull whitepaper via `scripts/fetch_whitepaper.py`; browser for Realms. |
| **scripts/fetch_whitepaper.py** | **API to pull whitepaper** — Fetches whitepaper content (export URL or Google Docs API). Run from `scripts/` with `-o ../WHITEPAPER_SNAPSHOT.md` to write snapshot. |
| **WHITEPAPER_SNAPSHOT.md** | **Whitepaper content** — Snapshot of truesight.me/whitepaper (Google Doc). Refresh with `scripts/fetch_whitepaper.py -o ../WHITEPAPER_SNAPSHOT.md` or paste from browser. |
| **DAPP_PAGE_CONVENTIONS.md** | **DApp page structure** — Meta tags, Open Graph, Twitter Card, favicon, nav, body/container layout, and UX pointers. **Follow this when creating or editing pages in the dapp repo** so all pages match existing conventions. See also `dapp/UX_CONVENTIONS.md` for loading/error/combobox patterns. |

## How to use (for AIs)

1. **First:** Read `OPERATING_INSTRUCTIONS.md` for rules on reading and contributing.
2. **Before editing any project:** Read `WORKSPACE_CONTEXT.md` to understand the workspace as a whole.
3. **Before touching a specific repo:** Check `PROJECT_INDEX.md` for that project’s purpose, stack, and where credentials/docs live.
4. **Marketing / CMO consultation:** When the task involves marketing (copy, positioning, campaigns, content, growth), read `CMO_SETH_GODIN.md` to consult the Agentic AI CMO (Seth Godin) and operate based on that context.
5. **Strategy / onboarding (Dr Manhattan):** When the task involves strategy, growth, priorities, or onboarding for the DAO/Agroverse network, read `DR_MANHATTAN.md` to consult Dr Manhattan and operate based on that context.
6. **DApp pages (dapp repo):** When creating or editing HTML pages in the **dapp** repository, read **`DAPP_PAGE_CONVENTIONS.md`** and follow its structure (meta tags, Open Graph, favicon, nav, body/container, status/loading). For UX patterns (loading states, errors, comboboxes), also follow **`dapp/UX_CONVENTIONS.md`**.
7. **API keys and env vars:** See the sibling repo **agentic_ai_api_credentials** for `env.template` and `API_CREDENTIALS_DOCUMENTATION.md`; no secrets are stored there.

## Location

- **Context (this repo):** Clone from `git@github.com:TrueSightDAO/agentic_ai_context.git` (or your local path, e.g. `/Users/garyjob/Applications/agentic_ai_context`).
- **Credentials reference:** `/Users/garyjob/Applications/agentic_ai_api_credentials` (or see PROJECT_INDEX for credential docs; no secrets in this repo).
- **Workspace root (multi-root):** Typically `/Users/garyjob/Applications` — contains many project directories; adjust for your machine.

Keep `WORKSPACE_CONTEXT.md` and `PROJECT_INDEX.md` updated when you add repos or change architecture so all AIs stay in sync.
