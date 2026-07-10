# Autopilot Topic-Role Architecture — Execution Roadmap

**Status as of 2026-05-27:** pre-flight  
**Goal:** Each Telegram topic gets an autonomous role with tailored tools and
behavior. New topics auto-detect and ask for role. Research-heavy roles use
CrewAI for autonomous multi-hour work.

---

## Design

### Topic → Role mapping

| Telegram Topic | Role | Primary Tools | CrewAI? |
|---|---|---|---|
| Content Marketing | Content Marketing Researcher | web_search, web_extract, read_*, upload_file_to_github, list_prs | Yes |
| Events | Event Coordinator | web_search, read_*, create_dao_submission, list_prs | No |
| Digital Infrastructure | SRE / DevOps Engineer | open_fix_pr, deploy, list_prs, read_*, list_directory | No |
| Retailer Outreach | Outreach Coordinator | web_search, read_*, create_dao_submission, list_prs | Possible |
| Import/Export | Logistics Analyst | web_search, read_*, lookup_qr_code | No |
| Inventory Management | Inventory Manager | lookup_qr_code, lookup_qr_batch, submit_contribution, read_* | No |
| General | General DAO Assistant | all tools | No |

### Tool scoping

When a topic has a role assigned, only that role's tool set is sent to the LLM.
This prevents the LLM from calling irrelevant tools (e.g., `deploy_autopilot` in
a Content Marketing context).

### First-message flow

```
New topic → User sends message →
  Autopilot: "I see this is a new topic. What role should I adopt? Options:
    1. Content Marketing Researcher
    2. Event Coordinator
    3. SRE / DevOps Engineer
    4. Retailer Outreach Coordinator
    5. Logistics Analyst
    6. Inventory Manager
    7. General DAO Assistant"
  User: "1" or "Content Marketing Researcher"
  Autopilot: "Got it. I'm now your Content Marketing Researcher. What should we work on?"
  [Role + tool set are persisted in session metadata]
```

### CrewAI for autonomous research

Research roles (Content Marketing, possibly Retailer Outreach) get an additional
`/research` pathway that spawns a CrewAI crew running autonomously. Progress is
pushed to Telegram via the notification channel.

---

## Sequenced plan

### PR1 — Role registry + tool scoping

| Step | Description |
|------|-------------|
| 1a | Create `app/roles.py` — role definitions (name, description, tools, system_prompt_override) |
| 1b | Add `role` field to session storage (`_sessions` dict + `_log_session`) |
| 1c | First-message detection: if session is empty, return role selection prompt |
| 1d | Tool filtering in `_stream_chat`: filter `get_tool_schemas()` by role |
| 1e | Per-role system prompt overrides |
| 1f | Deploy and test on production |

### PR2 — CrewAI integration for research roles

| Step | Description |
|------|-------------|
| 2a | Add `crewai` to `requirements.txt` |
| 2b | Create `app/research.py` — CrewAI crew builder based on role |
| 2c | New `/research` endpoint: accept task, spawn crew, run autonomously |
| 2d | Progress push: crew posts `CrewChatMessage` events to Telegram |
| 2e | Final report: auto-commit to target repo, notify via Telegram |
| 2f | Deploy and test with Content Marketing research task |

### PR3 — Topic auto-naming

| Step | Description |
|------|-------------|
| 3a | When role is set, auto-name the Telegram topic to match |
| 3b | Persist topic name in session index |

---

## Resume tracker

| Unit | Status |
|------|--------|
| PR1 — Role registry + tool scoping | ☐ open |
| PR1 — merged & deployed | ☐ |
| PR2 — CrewAI integration | ☐ |
| PR3 — Topic auto-naming | ☐ |

> **RESUME HERE:** PR1 step 1a — create `app/roles.py`
