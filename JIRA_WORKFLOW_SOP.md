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
| Ops execution tracking — **THE live board** | **Jira KAN** — https://truesightdao.atlassian.net/jira/software/projects/KAN/boards/2 (this document) |
| ~~Public sprint board~~ — **RETIRED 2026-11-25** | `sprint.truesight.me` was drained into Jira (57 handoffs migrated) and retired. See §12. |

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

**This is the most important rule in this document.**

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
`search`, `get_issue`, `list_transitions`, `list_pr_links`

**Write actions (`confirm_write=true` required):** `create_issue`, `update_issue`, `add_comment`,
`transition_issue`, `link_pr_in_comment`

`link_pr_in_comment` posts a comment whose bare GitHub URLs Jira unfurls into clickable
smart-link cards (ADF `inlineCard`); `list_pr_links` reads every GitHub PR/commit/repo URL back
out of an issue's comments. Note: `_adf_to_text` must handle `inlineCard`/`blockCard` nodes —
Jira stores smart-link URLs in `attrs.url`, **not** text, so a naive text-only reader silently
returns zero links while the write reports success.

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
| `400` **"Cannot add user. User is already a member"** on `POST /group/user` | the `products` field at user creation already granted access | **benign — do not retry.** Verify with `user/assignable/search` (§13c) instead of chasing the 400 |
| `GET /rest/api/3/instance` → `404`; `/rest/api/3/jiraconfig` → `404` | not exposed on this tenant | read `applicationrole` + `groups/picker` instead. A 404 here is **not** evidence of a broken tenant |

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
5. **Creating (or deactivating) a Jira user** — consumes a **paid seat** and is effectively
   one-way: deactivating a user does not reliably free it, so treat creation as permanent.
   Never create a seat without an explicit governor instruction. Recipe + traps: **§13**.

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

---

## 10. Thread URL — MANDATORY on every ticket (Gary, 2026-11-25)

Every ticket's description MUST carry a line of exactly this shape:

```
Thread URL: <one URL>
```

or, when the handoff genuinely had no live thread:

```
Thread URL: MISSING (handoff recorded no Telegram topic / Discord channel)
```

The `MISSING` spelling is deliberate — it is greppable, so gaps are visible and countable
instead of looking like an omission. Never simply leave the line out.

### 10a. Why

This is what makes a supervisor loop cheap. A supervising LLM (Envoy, DeepSeek Local, any
sibling) does not need `HANDOFF_MANIFEST.md` prose parsing to find the conversation:

```
jira_query(action="search", jql='project = KAN AND status = "In Progress"')
# for each ticket -> read the Thread URL -> prompt THAT channel/thread
```

One board query replaces a scan of every handoff file. Without the URL the ticket is a dead
end: the supervisor knows work is in flight but cannot speak into it.

### 10b. Accepted URL shapes

Any of these resolves to a live conversation — record whichever the handoff has:

| Source field | Shape |
|---|---|
| `telegram_topic_url` | `https://t.me/c/<chat>/<thread>` |
| `discord_channel_id` / `discord_thread_id` | `https://discord.com/channels/<guild>/<channel>` |
| fallback | `https://t.me/<group>/<topic_id>` when only ids are known |

`telegram_topic_url` is preferred when present — it is already human-clickable.

### 10c. Backfill state at migration (2026-11-25)

| Result | Count |
|---|---:|
| Thread URL written from handoff data | 49 |
| `Thread URL: MISSING` (handoff carried no thread) | 8 |
| **Total migrated** | **57** |

### 10d. Rule for new tickets

A ticket created without a thread URL is **not actionable by a supervisor**. If you cannot
supply the URL at creation time, still write the `MISSING` line, then create the thread and
patch the ticket. Do not let it default to silence.

---

## 11. Sophia's Jira identity — how "assign to yourself" works

Sophia has her own assignable account on the tenant:

| Field | Value |
|---|---|
| Display name | **Sophia Truesight** |
| Email | `sophia@truesight.me` |
| `accountId` | `712020:d6880b79-56bc-41b7-80e4-1f4c62770a73` |
| `accountType` | `atlassian` (human-type — `POST /user` cannot create `app` accounts) |
| Group | `jira-users-truesightdao` (product access `jira-software`) |
| Assignable on KAN | **yes** (verified via `user/assignable/search?project=KAN`) |

Created 2026-11-25 at Gary's instruction. Before it existed, `user/search?query=sophia`
returned **0 results** and the only assignable accounts were Gary plus Atlassian's own Rovo
app identities (`Jira Triage Agent`, `Request Router`, etc. — all `accountType: app`,
auto-provisioned, not user-created and not reusable for this purpose).

**Billing note:** this identity occupies a real Jira seat. Do not create additional seats
speculatively — deactivating a user does not reliably free a seat, so creation is effectively
one-way.

**Privacy note:** the tenant hides email addresses on all accounts, which is exactly the
condition under which `POST /rest/api/3/user` requires site-admin rights. Sophia holds
`ADMINISTER` on the site, so creation succeeded.

---

## 12. Retirement of `sprint.truesight.me` (2026-11-25)

The public Kanban board (`TrueSightDAO/sprint-site`, GitHub Pages, reading
`agentic_ai_context/handoffs/index.json`) was **drained into Jira and retired** at Gary's
instruction. It had drifted into a second, competing status surface.

| Handoff state | → Jira status | Count |
|---|---|---:|
| `awaiting_kickoff` | Backlog | 16 |
| `paused_at_gate` + `blocked_on_human` | Planned | 23 |
| `executing` | In Progress | 16 |
| `human_uat_ready` | In Review | 2 |
| `done` (33) + `stale` (1) | **not migrated** | 34 |

**Provenance, not summary.** Each migrated ticket's description carries the handoff's
`status_raw` **verbatim** — that is where real progress lives (e.g. "PR1/PR2 merged (#552,
#555)"). Migrating only the coarse `state` field would have thrown that away.

**Idempotency.** Every migrated description carries a hidden
`sprint-migration:<plan_file>` marker, so a re-run finds and skips rather than duplicating.

**Labels.** `sprint-migration` (57) · `blocked-on-human` (19) · `envoy-supervised` (2) —
the last so handoffs run by another box are not mistaken for Sophia's own queue.

**`handoffs/index.json` is NOT deleted.** It is still written by the supervisor loop and read
by other tooling. Retiring the *view* is not the same as deleting the *data*.

---

## 13. Provisioning an agent identity on the tenant (verified 2026-11-25)

§11 records that Sophia's identity **exists**; this section records **how to create one**, because
two of the responses involved look fatal and are not, and one of them cost a debugging round.

### 13a. The working call

```json
POST /rest/api/3/user
{
  "emailAddress": "sophia@truesight.me",
  "displayName":  "Sophia Truesight",
  "products":     ["jira-software"]
}
```

`products` grants Jira product access **at creation**. That makes the follow-up group call
redundant, which produces the misleading response in §13b.

### 13b. Two `400`s that mean opposite things

| Response | Meaning | Action |
|---|---|---|
| `400`, empty/absent body | validation rejected the payload (e.g. missing `emailAddress`) | **real error** — fix the payload |
| `400` **"Cannot add user. User is already a member"** on `POST /group/user`, *after* a successful create | the `products` grant already put the user in the group | **benign — ignore, do not retry** |

Do not "fix" the second one. The identity is already correct; confirm it with §13c.

### 13c. Verify with assignability, not existence

An account can exist and still not be assignable on the project, so **assignability is the only
proof that matters**:

```
GET /rest/api/3/user/assignable/search?project=KAN
```

Before Sophia's seat: **6** assignable (Gary + 5 Rovo apps). After: **7**.

### 13d. Why `POST /user` cannot create an "agent" account

`POST /rest/api/3/user` only creates `accountType: atlassian` (human-type) accounts. It **cannot**
create `accountType: app`, which is what Atlassian provisions for its own Rovo/AI identities — on
this tenant the 40+ accounts named *Jira Triage Agent*, *Request Router*, *Jira Coding Agent*, and
so on. Those are auto-provisioned and **not reusable** as an agent identity. An agent's own Jira
identity is therefore necessarily a human-type seat — hence the billing note in §11 and the
governor gate in §7 item 5.

### 13e. Being assigned work ≠ acting as that identity

Provisioning an identity is orthogonal to authenticating as it. `jira_query` authenticates with
`JIRA_EMAIL` + `JIRA_API_TOKEN` (§5) — the account that **owns the token**. Creating
`sophia@truesight.me` does not change who API calls run as, and there is no reason to change it:
the token owner holds `ADMINISTER` and can assign work to the Sophia account freely.

**Do not** swap `JIRA_EMAIL` to a newly created identity — that identity has no token and no
login session, so every call would begin failing auth.

### 13f. Governance note — an agent named in an org chart is not an independent reviewer

Creating this seat carries a policy risk worth stating plainly: an agent with its own named Jira
account can appear to be an independent reviewer when it is in fact the same automation (or the
same model) as the worker. **Enforce human sign-off in the workflow or policy, never in the
identity.** Do not treat "assigned to Sophia Truesight" as evidence that a second, independent
set of eyes reviewed something. See §2 — `Done` requires *governor* acceptance.
