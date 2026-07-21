# Handoff protocol — overview (LLMs ↔ Sophia ↔ humans)

**What this is.** The big-picture map of how work flows between the **local
LLMs** (Claude Code, Cursor, Kimi, Codex…), **Sophia** (the autopilot), and the
**human governors** — across the interfaces they share (local terminal, GitHub,
Telegram). For the **live registry** (status, resume tracker, Telegram
topic/thread_id per handoff) see **`HANDOFF_MANIFEST.md`** — the single source
of truth (consolidated 2026-07-18, see `../plans/HANDOFF_REGISTRY_CONSOLIDATION_PLAN.md`).
For the **Sophia trigger protocol** (ping template, the GO convention, thread
rules) see **`SOPHIA_HANDOFFS.md`**; this doc is the human-readable orientation.

---

## Actors & interfaces

| Actor | What they are | Primary interface |
|---|---|---|
| **Governor** (e.g. Gary) | Human. Initiates work, authorizes, reviews/merges, does account-only actions. | Local terminal (to an LLM) + Telegram + GitHub |
| **Local LLM** | Claude Code / Cursor / Kimi / Codex on the governor's machine. Plans, commits, triggers Sophia, reviews. | Local terminal/IDE + GitHub + `ping_sophia` (HTTPS) |
| **Sophia** | The autopilot (FastAPI on EC2). Executes handed-off plans, opens PRs, reports. | GitHub + Telegram + her tools (ssh/git/gh) |
| **Edgar / DAO ledger** | Contribution + identity backend. | `submit_contribution` (peripheral to handoffs) |

| Interface | Role | Key property |
|---|---|---|
| **GitHub** (`agentic_ai_context` + code repos) | **Durable source of truth** — plans, the registry, and PRs all live here. | Every actor reads/writes it; survives restarts. **This is the real handoff.** |
| **`ping_sophia` → HTTPS `/chat-blocking`** | **Trigger** that wakes Sophia for a handoff. | Returns the reply to the *caller*; it is **NOT** a Telegram bridge and does not share memory with the Telegram-facing Sophia. |
| **Telegram** (DAO Ops forum topics) | **Live coordination** — Sophia posts kickoffs + progress; the governor authorizes + reviews. | One topic per handoff. The **GO convention** lives here. |

> **The one mental model that matters:** the **committed plan + registry on
> GitHub is the durable handoff**; the **ping is just a trigger**; **Telegram is
> where the human says "go" and watches progress.**

---

## The full flow

```mermaid
sequenceDiagram
    actor G as Governor (human)
    participant L as Local LLM
    participant GH as GitHub (plans · registry · PRs)
    participant S as Sophia (autopilot)
    participant TG as Telegram (DAO Ops topic)

    G->>L: 1. "Do X" (local terminal)
    L->>GH: 2. Write *_PLAN.md, commit to main (PR→merge)
    Note over GH: Durable handoff = committed plan + registry
    L->>GH: 3. Add registry row (HANDOFF_MANIFEST.md)
    L->>S: 4. ping_sophia (HTTPS) — trigger only
    S->>GH: 5a. Refresh + read plan (read_repo_file)
    S->>TG: 5b. Create topic, post kickoff + context, end with GO prompt, park
    S-->>L: 5c. Reply with thread_id + link
    L->>GH: 6. Record thread_id in registry
    L-->>G: 6b. "Sophia is parked in <topic link>"
    G->>TG: 7. "go for it"
    S->>GH: 8. Execute from RESUME HERE → open PR(s)
    S->>TG: 8b. Report progress + blockers
    G->>GH: 9. Review & merge PR(s)
    S->>GH: 10. Log DAO contribution
```

## What happens on "go for it"

```mermaid
flowchart TD
    A["Governor: 'go for it' in the topic"] --> B["Sophia: start at RESUME HERE"]
    B --> C{"For each unit in the plan"}
    C --> D["Apply the gates:<br/>verify CDN/deps · runtime smoke test · map-before-delete"]
    D --> E["Open PR<br/>(Generated-by: Sophia trailer)"]
    E --> F{"Plan says safe to auto-merge?"}
    F -- "package / internal" --> G["Merge after checks green"]
    F -- "consumer / deploys-from-main" --> H["Park PR for human review"]
    H --> I["Governor (and/or LLM) reviews, then merges"]
    C -- "all units done" --> J["Report complete in topic + log contribution"]
```

## Where humans get involved (only three touchpoints)

```mermaid
flowchart LR
    subgraph T1["A. Initiate"]
      a["Governor → local LLM<br/>in the terminal: 'do X'"]
    end
    subgraph T2["B. Authorize"]
      b["Governor → Telegram topic:<br/>'go for it'"]
    end
    subgraph T3["C. Review / merge + account-only"]
      c["Governor → GitHub:<br/>review & merge PRs<br/>(+ npm tokens, org/secret setup)"]
    end
    T1 --> T2 --> T3
```

- **A — Initiate:** the governor describes the work to a local LLM in the
  terminal. The LLM turns it into a committed plan and triggers Sophia.
- **B — Authorize:** the governor opens the Telegram topic (where Sophia is
  already parked with context) and says **"go for it"** — full authorization for
  the whole plan (see the GO convention in `SOPHIA_HANDOFFS.md`). **Exception:**
  a plan marked `Auto-start: yes` skips this touchpoint entirely — Sophia posts
  her kickoff and starts executing without waiting for it (§5c gates still
  apply). Opt-in per plan; see "Auto-start" in `SOPHIA_HANDOFFS.md`.
- **C — Review / merge:** PRs that touch production / deploy-from-main are
  **opened, not auto-merged** — the governor (optionally with an LLM reviewing the
  diff against the plan's checklist) reviews and merges. Account-only actions
  (npm tokens, org creation, GH secrets) are governor-only and happen here too.

---

## The gates (Definition of Done — every handoff)

Carried in each plan and enforced by Sophia on "go for it":

1. **Verify external deps in-PR** (e.g. the exact CDN URL returns 200; pinned
   version).
2. **Runtime smoke test, not just `node --check`** — load the actual artifact and
   assert behavior (syntax-checking can't catch API-shape/runtime mismatches).
3. **Map-before-delete** when swapping inline code for a library.
4. **Open PR, do NOT auto-merge** anything that deploys from `main`.
5. **`Generated-by: <agent>` trailer** on every commit + PR (so any agent's work
   is attributable — git author is the human operator).
6. **Log a DAO contribution** after each merged unit.

---

## Notes / current limitations

- **Sophia posts only into topics she creates** (via `create_telegram_topic`) or
  threads where she's captured the `chat_id`/`thread_id` from an incoming message
  — she has no blind "post to any existing thread" tool. So handoffs **let her
  create + report the topic** rather than targeting a pre-existing thread.
- The `ping_sophia` reply is the *HTTP* Sophia, which is **not** automatically the
  same session as the Telegram-facing Sophia. Trust the **committed artifacts**
  (plan, registry, PRs), not the ping reply, as the record of truth.

See also: `HANDOFF_MANIFEST.md` (the live registry — status, resume tracker, Telegram
topic/thread_id), `SOPHIA_HANDOFFS.md` (GO convention + trigger template),
`GITHUB_AGENTIC_AI_SSH.md` (agent attribution + PR workflow),
`OPERATING_INSTRUCTIONS.md` §5 (the plan/roadmap requirement).
