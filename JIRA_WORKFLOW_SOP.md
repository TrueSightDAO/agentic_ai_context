# Jira / KAN board workflow — SOP

**Status:** compiled 2026-11-24 (Sophia Truesight, at Gary's request). Every fact below was read
live from the tenant — see §9 for the exact calls. Re-verify rather than trust a stale copy.

**Applies to:** `truesightdao.atlassian.net`, project **KAN** ("TrueSight DAO", id `10001`),
board 2 — <https://truesightdao.atlassian.net/jira/software/projects/KAN/boards/2>

**Tooling:** `jira_query` in `truesight_autopilot` (`app/tools/jira_tools.py`, PR #628).

---

## 1. Scope — what Jira is, and is not, for here

Jira tracks **ops execution**: partner follow-ups, entity/formation tasks, product iterations.
The KAN board's real tickets are things like "Rusmin — pitch deck for the family office",
"Agroverse CNPJ formation", "Rock salt requirements for Ohio".

It is **not** the DAO's system of record, and this SOP does not make it one:

| Concern | Where it lives |
|---|---|
| Cross-session backlog / tooling gaps | `OPEN_FOLLOWUPS.md` — the **only** backlog file |
| Public sprint board | `sprint.truesight.me` (over `handoffs/index.json`) |
| Ops execution tracking | **Jira KAN** (this document) |

Do **not** mirror `OPEN_FOLLOWUPS.md` into Jira, and do not create a second backlog there.
The Nov 2026 tooling review left this exact question open ("what does Jira give us that the
sprint board + followups file does not?"); this SOP answers it narrowly — **per-ticket stage and
owner accountability**, which a flat markdown list cannot express.

---

## 2. The five stages and what each means

Jira's canonical statuses for KAN, **identical across all four issue types**
(Epic / Subtask / Task / Story):

| # | Status | Status id | Jira category | DAO meaning | Evidence required to enter |
|---|---|---|---|---|---|
| 1 | **Backlog** | `10003` | To Do | Captured, not yet scheduled. The Jira-side equivalent of an `OPEN_FOLLOWUPS.md` pending row. | none — capture freely |
| 2 | **Planned** | `10005` | In Progress | Scoped: a named owner and a definition of done exist. | owner + scope written in the ticket |
| 3 | **In Progress** | `3` | In Progress | Active work — a branch, a thread, or a live conversation is moving it. | linked PR / thread / active dialogue |
| 4 | **In Review** | `10004` | In Progress | Work product exists; awaiting human acceptance (UAT). | PR merged or artifact delivered |
| 5 | **Done** | `10006` | Done | Verified and accepted. | explicit governor acceptance |

### The evidence column is the point

The stage is a **claim**, and the evidence column is what makes the claim checkable. Moving a
ticket forward without the evidence is the Jira-shaped version of declaring victory — the same
anti-pattern the attention-surface protocol exists to prevent (an unmeasured surface reported as
healthy). If the evidence does not exist, the ticket is not in that stage yet.

---

## 3. Runtime discipline — never hard-code a transition id

**This is the most important rule in this document.**\
**This is the most important rule in this document.** <- see note below

Transition ids are **per-current-status** and their **labels do not match the status names**.
Measured on `KAN-12` while it sat in *Planned*, the full set of legal moves was:

| Transition id | Label Jira reports | Destination |
|---|---|---|
| `11` | `Backlog` | Backlog (`10003`) |
| `3` | **`in execution`** | In Progress (`3`) |

Two consequences:

1. **The same numeric id means different things from different statuses.** Id `3` is "in execution"
   here; earlier in the same verification session id `2` performed a different move from a
   different starting status. A global id→stage table would be wrong and would silently send
   tickets to the wrong column.
2. **Labels are not statuses.** `in execution` → *In Progress*; `Backlog` → *Backlog*. Never
   assume the label names the destination.

**Therefore the mandatory sequence for any transition is:**

```
1. jira_query(action="list_transitions", issue_key="KAN-nn")
2. read the returned to.name for each transition — pick by DESTINATION NAME, not by id or label
3. jira_query(action="transition_issue", issue_key="KAN-nn", transition_id=<that id>, confirm_write=true)
```

Never cache a transition id across tickets, and never reuse one you read in an earlier session.

---

## 4. The `jira_query` tool

Credentials come **only** from the encrypted vault. Nothing from env, nothing from chat, nothing logged.

**Read actions (no gate):** `myself`, `list_projects`, `get_project`, `list_issue_types`,
`search`, `get_issue`, `list_transitions`

**Write actions (`confirm_write=true` required):** `create_issue`, `update_issue`, `add_comment`,
`transition_issue`

The write gate is the SOP's second line of defence: a stage change is never one accidental call
away. If a call is refused with
`'<action>' is write-class and requires confirm_write=true`, that is the gate working, not a bug.

Example — read the board:

```
jira_query(action="search", jql="project = KAN ORDER BY key ASC")
```

Example — advance a ticket after reading its transitions:

```
jira_query(action="add_comment", issue_key="KAN-13",
           comment="Blocked on supplier quote — see thread 21099.", confirm_write=true)
jira_query(action="transition_issue", issue_key="KAN-13",
           transition_id="<id whose to.name == 'In Progress'>", confirm_write=true)
```

---

## 5. Credentials — setup and rotation

Three vault entries. **Never** paste a token into chat, a commit, or an env file.

| Vault key | Value |
|---|---|
| `JIRA_BASE_URL` | `https://truesightdao.atlassian.net` |
| `JIRA_EMAIL` | the Atlassian account that owns the token |
| `JIRA_API_TOKEN` | token from <https://id.atlassian.com/manage-profile/security/api-tokens> |

Auth is HTTP Basic (`email:token`) — the method Atlassian documents for non-interactive
bots/CI. If any key is absent the tool returns `{"status": "not_configured"}` rather than
raising, so the tool is safe to deploy before setup exists.

**Rotation:** revoke at the same URL, then rewrite the vault value. No code change, no redeploy.
A token that has been pasted into a chat transcript should be treated as semi-exposed and rotated.

---

## 6. Known tenant quirks — verify before reporting "broken"

| Symptom | Cause | Correct call |
|---|---|---|
| `HTTP 410` from search | Jira **removed** `GET/POST /rest/api/2|3/search` (classic pagination) | `/rest/api/3/search/jql` with `nextPageToken` — what the tool does |
| `HTTP 404 "Issue does not exist or you do not have permission to see it"` on `issue/creatable` | endpoint not usable on this tenant | read `project/{key}.issueTypes` |
| `workflowscheme/project` returns `{"values": []}` | no explicit scheme mapped; default inherited | expected — not an error |
| Anonymous `serverInfo` = 200 but `project/search` = `total: 0` | anonymous visibility does not imply project visibility | always verify **authenticated**, never conclude "0 projects" from an anonymous read |
| Board shows fewer columns than the 5 stages | `Planned`/`In Progress`/`In Review` share Jira's *In Progress* **category** | admin UI board mapping — see §7 |

> Diagnostic discipline: an absolute URL or path in an error message is what a process *tried*,
> not proof of where the fault lies. Establish authenticated ground truth before reporting a
> resource missing.

---

## 7. Governor-only actions (cannot be done from the API)

These need an Atlassian **admin** login. Record them here so no agent promises them:

1. **Board column mapping** — give `Planned`, `In Progress`, `In Review` their own columns if
   they should be visually distinct. Today they collapse into one *In Progress* column.
2. **Workflow scheme changes** — per-issue-type gating (e.g. Epics may not jump Backlog→Done).
   All four types currently share one identical workflow with no restriction.
3. **Org connectors / API-token auth toggle** — Administration → Connectors. If a future
   integration stalls at consent or fails every call, check here first.
4. **Token issuance and revocation** — §5.

---

## 8. Anti-patterns

- **Hard-coding a transition id.** See §3. Worst failure mode in this doc — silent, plausible, wrong column.
- **Using Jira as the backlog.** `OPEN_FOLLOWUPS.md` stays the single pending list (§1).
- **Moving a ticket to Done without acceptance.** Done means a governor accepted it, not that an agent finished typing.
- **Filing a verification ticket and leaving it.** Any ticket created to test the integration must be labelled `safe to delete` and cleaned up.
- **Reporting a stage from memory.** Read it: `jira_query(action="get_issue", issue_key=…)`.
- **Trusting an anonymous read as ground truth.** See §6.

---

## 9. Verification provenance (how §2 and §3 were established)

Read live 2026-11-24 from the autopilot box against `truesightdao.atlassian.net`:

| Call | Result |
|---|---|
| `GET /rest/api/3/myself` | 200 — `Gary Teh <garyjob@agroverse.shop>` |
| `GET /rest/api/3/project/KAN` | `KAN` / "TrueSight DAO" / id `10001`; types Epic, Subtask, Task, Story |
| `GET /rest/api/3/project/KAN/statuses` | the 5 statuses × 4 issue types in §2 |
| `GET /rest/api/3/workflowscheme/project?projectId=10001` | `{"values": []}` |
| `GET /rest/api/3/search/jql?jql=project=KAN` | 14 issues, KAN-2…KAN-16 |
| `GET /rest/api/3/issue/KAN-12/transitions` | id `11`→Backlog, id `3` "in execution"→In Progress |

Board inventory is a **snapshot**, not a constant — re-read it, do not quote this table as current.
