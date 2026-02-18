# Operating instructions for AI agents

**Read this file first** when you load this folder. These rules keep context consistent and prevent conflicts when multiple agents (Claude Code, OpenAI Codex, Gemini CLI, Cursor, etc.) use the same workspace.

---

## 1. Purpose of this folder

This folder (**agentic_ai_context**) is the **shared context** for the workspace under `/Users/garyjob/Applications`. All agents should read it to get up to speed before editing any project. Only one source of truth is maintained here; agents follow the rules below so that context stays useful for everyone.

---

## 2. What to read (in order)

| Order | File | Use it for |
|-------|------|-------------|
| 1 | **OPERATING_INSTRUCTIONS.md** (this file) | Rules for reading and contributing; read first. |
| 2 | **WORKSPACE_CONTEXT.md** | Overview of the workspace: project groups, conventions, cross-repo relationships. |
| 3 | **PROJECT_INDEX.md** | Per-project summary: purpose, stack, entry points, credentials reference. |
| 4 | **agentic_ai_api_credentials** (sibling folder) | Env var names and credential docs only; no secrets. Use when you need to know which env vars a project expects. |
| — | **CMO_SETH_GODIN.md** | **Marketing / CMO consultation.** When the task involves marketing (copy, positioning, campaigns, content, growth, branding), read this file to consult the Agentic AI CMO (Seth Godin) and operate based on his principles and perspective. |
| — | **DR_MANHATTAN.md** | **Strategy / onboarding.** When the task involves strategy, growth, priorities, or onboarding for the Agroverse and TrueSight DAO network, read this file to consult Dr Manhattan and operate based on his perspective. Future use: chatbot for newcomers. |
| — | **GOVERNANCE_SOURCES.md** | **Governance.** Whitepaper (truesight.me/whitepaper → Google Doc), proposals (GitHub TrueSightDAO/proposals, Realms). Pull whitepaper via `scripts/fetch_whitepaper.py`; browser for Realms. |
| — | **SYNDICATE_AGREEMENTS.md** | **Syndicate agreement drafting.** When drafting AGL Export Trade Financing Syndicate Agreements, read this first. **Precedence:** Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee (avoid double-charging). |

Other files in this folder (e.g. `AI_SETUP.md`, `GROK_CLI_410_FIX.md`, `CURSOR_AUTO_APPROVE_SETTINGS.md`) are reference docs for setup and fixes; read them when relevant to your task.

---

## 3. Canonical context: do not edit these

The following files are the **authoritative** context. **Do not modify them** unless the user explicitly asks you to update workspace documentation.

- **WORKSPACE_CONTEXT.md**
- **PROJECT_INDEX.md**
- **README.md**
- **OPERATING_INSTRUCTIONS.md**

If you discover something that should change in those files (e.g. a new project, a corrected convention), use **“Suggested context updates”** (see section 5) instead of editing them directly.

---

## 4. Where and how you may contribute

You may add or update context only in the following ways.

### 4.1 Append-only log: `CONTEXT_UPDATES.md`

- **File:** `CONTEXT_UPDATES.md` in this folder.
- **Rule:** **Append only.** Do not remove or rewrite existing lines.
- **Format:** One line per entry: `YYYY-MM-DD | <agent-id> | <short note>`  
  Example: `2025-01-29 | cursor | Noted: krake_local uses Node 20; add to PROJECT_INDEX if human approves.`
- **Use it for:** Short, factual notes (e.g. “X uses Y”, “entry point is Z”) so other agents or the user can see what was learned. Do not put secrets or long prose here.

### 4.2 Per-agent or per-session notes: `notes/`

- **Folder:** `notes/` inside this folder.
- **Rule:** Create or update only files that identify **you** or the **session**, e.g.:
  - `notes/cursor_2025-01-29.md`
  - `notes/claude_session.md`
  - `notes/grok_notes.md`
- **Do not** overwrite another agent’s file unless the filename clearly belongs to you (e.g. your own `*_session.md`).
- **Use it for:** Session summaries, “what I did / what I learned,” or structured notes for other agents. Keep filenames predictable (e.g. date or agent name).

### 4.3 Suggested context updates (for human approval)

- When something should change in **WORKSPACE_CONTEXT.md**, **PROJECT_INDEX.md**, or **README.md**, do **not** edit those files yourself.
- Instead, produce a **suggested update** in one of these ways:
  - Append a line to **CONTEXT_UPDATES.md** (see 4.1) describing the change and that it needs human approval, or
  - Write the suggested change in a short note under **notes/** (e.g. `notes/suggested_project_index_update_2025-01-29.md`) and mention that a human should apply it to the canonical file.

---

## 5. Summary for agents

- **Read first:** OPERATING_INSTRUCTIONS.md → WORKSPACE_CONTEXT.md → PROJECT_INDEX.md (and credentials folder when needed).
- **Do not edit:** WORKSPACE_CONTEXT.md, PROJECT_INDEX.md, README.md, OPERATING_INSTRUCTIONS.md unless the user explicitly asks.
- **You may:** Append to `CONTEXT_UPDATES.md`; create/update your own files under `notes/`; suggest changes via CONTEXT_UPDATES or a note instead of editing canonical docs.

Following these rules keeps the shared context consistent and allows other agents to read and use it reliably.
