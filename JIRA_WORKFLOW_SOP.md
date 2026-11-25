# Jira / KAN board workflow — SOP

**Status:** compiled 2026-11-24, amended 2026-11-25 (§13) (Sophia Truesight, at Gary's request). Every fact below was read
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

---

## 10. Thread URL — MANDATORY on every ticket (Gary, 2026-11-25)

> **Amended 2026-11-25 — see §13.** The description URL is now the *primary* routing
> signal, not the only one. A Discord channel whose name carries the ticket key
> (`kan-15-…`) resolves on its own, so a ticket can be routed without any description
> edit. §10 stays mandatory — the URL is still what makes a ticket portable across
> transports — but it is no longer a hard blocker for Discord routing.

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

### 10c. Backfill state at migration (2026-11-25) — **NOT APPLIED**

> **Correction (2026-11-25, verified by read-back).** An earlier revision of this table
> claimed 49 thread URLs had been written. That was reported from a script's own success
> counter and is **false**. Verified state below.

| Result | Count |
|---|---:|
| Tickets labelled `sprint-migration` | 57 |
| **Actually carrying a `Thread URL:` block** | **0** |
| Written by hand (KAN-79, the tracking ticket) | 1 |
| **Still needing backfill** | **57** |

**This is an open blocker.** A supervisor that nudges work by thread has nothing to nudge
until the backfill is re-landed *and verified by re-reading a ticket*. Do not trust a write
receipt for this — re-read the persisted description before reporting success.

Source data is available: 77 of 91 handoffs in `handoffs/index.json` carry a
`telegram_topic_url` or `discord_channel_id`.

### 10d. Rule for new tickets

A ticket created without a thread URL is **not actionable by a supervisor**. If you cannot
supply the URL at creation time, still write the `MISSING` line, then create the thread and
patch the ticket. Do not let it default to silence.

---

## 11. Sophia's Jira identity — how "assign to yourself" works

Sophia has her own assignable account on the tenant:

| Field | Value |
|---|---|
| Display name | **`admin+sophia`** (auto-derived from the email at creation) |
| Email | `admin+sophia@truesight.me` |
| `accountId` | `712020:96b5508c-475a-4bab-b6c0-441ad3d7c2ce` |
| `accountType` | `atlassian` (human-type — `POST /user` cannot create `app` accounts) |
| Groups | 7, incl. `jira-users-truesightdao` (product access `jira-software`) |
| Assignable on KAN | **yes** (verified via `user/assignable/search?project=KAN`) |

> ⚠️ **`accountId` is NOT stable — it changes if the account is deleted and re-created.**
> The original account (`712020:d6880b79-56bc-41b7-80e4-1f4c62770a73`, email
> `sophia@truesight.me`) was deleted on 2026-11-25 and re-created under the `admin+sophia@`
> address. The old id still *resolves* via `GET /user?accountId=` — it returns an
> `active: False` tombstone with **no groups and no product access** — which makes it a silent
> trap: assignments to it succeed-looking but notify nobody.
>
> | | Old `d6880b79…` | New `96b5508c…` |
> |---|---|---|
> | `active` | **False** | True |
> | displayName | `sophia` | `admin+sophia` |
> | groups | **none** | 7 |
> | product access | **NONE** | `jira-software` |
>
> **After the replacement, all 58 tickets were reassigned to the new id** and verified by
> re-query (`OLD: 0`, `NEW: 58`). If this account is ever recreated again, sweep for
> `assignee = "<old accountId>"` and reassign — do not assume assignment survived.

Created 2026-11-25 at Gary's instruction. Before it existed, `user/search?query=sophia`
returned **0 results** and the only assignable accounts were Gary plus Atlassian's own Rovo
app identities (`Jira Triage Agent`, `Request Router`, etc. — all `accountType: app`,
auto-provisioned, not user-created and not reusable for this purpose).

**Billing note:** this identity occupies a real Jira seat. Do not create additional seats
speculatively — deactivating a user does not reliably free a seat, so creation is effectively
one-way. *Observed 2026-11-25:* after deletion + re-creation the old account persisted as an
`active: False` tombstone with product access `NONE`, while the new account holds
`jira-software`. Whether the *seat count* actually returned to 1 (vs. the tombstone still
billing) is **not verified** — check the admin billing page before assuming.

**Notification note:** the tenant suppresses `emailAddress` for all accounts other than the
calling token's own (`/myself` returns Gary's, everyone else `null`). So you cannot confirm by
API which address a user's notifications go to. Verify by triggering a real notification and
looking for it in the target mailbox. Note also that **assignment never sends an invitation**
and needs no acceptance — in this IDP-directory tenant, users are provisioned directly as
`Active` with no invite event in the audit log at all.

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

## 13. Offline owner — MANDATORY on every ticket (Gary, 2026-11-29)

**Access decision (2026-11-29):** *everyone lives in Discord; nobody gets a Jira seat unless
they must actually act inside Jira.*

That decision has a structural consequence. Jira assignees are now a very small set (Gary,
`admin+sophia`), while **the person whose progress you chase is usually offline and not in
Jira at all** — a farmer, a co-packer, a freight broker, a partner in another timezone.
Assignee therefore answers the wrong question. Every ticket's description MUST carry a line
of exactly this shape:

```
Offline Owner: <Name> · Discord: <@handle or <@user_id>> · Check-in: <YYYY-MM-DD>
```

or, when no offline person has been identified yet:

```
Offline Owner: MISSING (no offline person identified yet)
```

The `MISSING` spelling is deliberate — greppable, so gaps are visible and countable instead of
looking like an omission. Same discipline as §10. Never simply leave the line out.

### 13a. Assignee ≠ Offline Owner

This is the whole point of the convention, so it is stated plainly:

| | Assignee | Offline Owner |
|---|---|---|
| Means | who acts **inside Jira** | who you chase **in the real world** |
| Typical values | `admin+sophia`, `Gary Teh` | Kirsten, a farmer, a freight broker, a partner |
| Changes when | the working agent changes | the human relationship changes |

A ticket may legitimately be assigned to `admin+sophia` while its offline owner is Kirsten.
Overloading `assignee` to mean "the person to chase" is an anti-pattern: it would fire
notifications at the wrong human and make the board unreadable.

**One offline owner per ticket.** If two people each owe you a different thing, split the
ticket — otherwise neither is actually being followed.

### 13b. Which channel — and why the thread URL is NOT repeated here

Discord is the contact of record, because the 2026-11-29 access decision puts the whole
team there and a supervisor can *speak into* Discord programmatically.

**Do not duplicate the conversation URL in this line.** §10 already mandates a `Thread URL:`
per ticket and is the single channel-of-record. §13 names the **person**; §10 names the
**place**. Keeping them separate means one place to fix when a conversation moves.

Phone / WhatsApp may be recorded as well, but **is not sufficient alone** — a supervisor
loop cannot post into WhatsApp, so a ticket whose only contact is a phone number is a dead
end in the same way §10a describes. Record the number *in addition to* a Discord handle.

### 13c. Resolving the person

Every offline owner should resolve to a row in the Main Ledger's
`Contributors contact information` tab:

| Field | Column |
|---|---|
| Name | A |
| **Discord ID** | **G** |
| Email | D |
| Phone / WhatsApp | F |

If the person is not on the ledger, that is a **prerequisite gap, not a detail** — they cannot
be nudged and cannot be credited. File it before treating the ticket as actionable.

### 13d. Why — the supervisor loop

A supervising LLM does not need to parse `HANDOFF_MANIFEST.md` prose to find who to chase:

```
jira_query(action="search", jql='project = KAN AND status != Done AND text ~ "Offline Owner: MISSING"')
# -> every ticket with no named offline owner: the gap list
```

```
jira_query(action="search", jql='project = KAN AND status != Done AND text ~ "Offline Owner"')
# -> read each Offline Owner + §10 Thread URL, then nudge in the right Discord channel
```

One board query replaces a scan of every handoff file.

### 13e. Known limitation — a date inside prose is not queryable

JQL's `text ~` matches the *string*, but it cannot compare or sort a `YYYY-MM-DD` embedded in
description prose. So this ships in two phases:

| Phase | What | Admin needed |
|---|---|---|
| **1 (this spec)** | The greppable description line | **none** — works today |
| **2 (future)** | A real **date** custom field, `Next offline check-in` | **Atlassian admin** (§7) |

After phase 2 the nudge query becomes comparable rather than grep-only:

```
project = KAN AND status != Done AND "Next offline check-in" <= endOfDay()
```

Creating a custom field is a governor/admin action under §7. **An agent must not create
fields unasked**, and phase 1 deliberately needs no admin so the convention is usable now.

### 13f. Relationship to existing labels

The `blocked-on-human` label (19 tickets) is **not** the same thing:

- `blocked-on-human` = the ticket is **stalled** pending a human decision.
- `Offline Owner` = who you **follow up with**, whether or not the ticket is stalled.

A ticket can have an offline owner and not be blocked (routine progress chase), or be
`blocked-on-human` with no offline owner yet (`MISSING`). Do not conflate them.

### 13g. Backfill state — **NOT APPLIED**

No existing ticket has been backfilled with an `Offline Owner:` line. Same discipline as
§10c: **re-read the persisted description before reporting success.** A write receipt is not
evidence.

### 13h. Rule for new tickets

A ticket created without an `Offline Owner:` line is **not followable**. If you cannot name
the person at creation time, write the `MISSING` line anyway, then patch it once known. Do not
let it default to silence.

---

## 13. Channel-name convention — `kan-<n>-<slug>` (Gary, 2026-11-25)

**The rule:** if a Discord channel is the conversation for a JIRA ticket, its name MUST start
with that ticket's key, lowercased, followed by a slug:

```
kan-15-cacao-mug-iteration      → KAN-15
kan-16-cacao-legacy-project-singapore → KAN-16
```

### 13a. Why (measured, not aesthetic)

| Property | Measured value |
|---|---|
| Collisions across all **78** KAN titles | **0** |
| Title characters kept, key-prefixed | **31.5** avg |
| Discord name limit | 40 chars |

So the convention costs ~8 characters of title and is unambiguous across the whole board.
It is **measured against real data**, not a preference.

The load-bearing win is routing: the supervisor loop (`app/jira_loop.py`) can resolve a
target from the channel name alone via `target_from_channel_name()`, with
`LOOP_JIRA_CHANNEL_FALLBACK` (default **on**). It removes the need to hand-write a
`Thread URL:` into every description — a field that was populated on **0 of 57**
migrated tickets, i.e. a requirement nobody followed.

### 13b. Precedence

1. **`Thread URL:`** in the description — always wins (explicit, survives a rename).
2. **Keyed channel name** — fallback, only when there is no URL.
3. **Neither** → the ticket is reported in the sweep's `unmapped` digest. **Never guess.**

### 13c. Hard rules

- **One key per channel.** `kan-15-cacao-mug` — never two keys in one name.
- **Never rename a channel without establishing the association from the ticket's own
  summary.** A shared generic token (`agroverse`, `cacao`) is **not** an association:
  scanning 78 tickets against 113 channels produced 69 "matches" on that basis, nearly
  all false positives. Only rename where the channel is unambiguously *that ticket's*
  conversation.
- **Key at the start, hyphenated.** `foo-kan-15` does not parse. The parser is
  `^kan-(\d+)(?![0-9])`, so `kan-250-x` → `KAN-250`, never `KAN-25`.
- **Renaming is reversible and safe.** Discord keeps history and the channel id; the key is
  a prefix, not a replacement. Do not delete a channel to "re-create it with the right name".

### 13d. Current state (2026-11-25)

| Ticket | Channel | id |
|---|---|---|
| KAN-15 | `kan-15-cacao-mug-iteration` | `1567010139993677884` |
| KAN-16 | `kan-16-cacao-legacy-project-singapore` | `1569368154218569850` |

**2 of 113** text channels carry a key. The convention is deliberately being introduced
**gradually and only where verified** — a wrong rename misroutes a nudge to the wrong
conversation, which is worse than an unmapped ticket (an unmapped ticket is *reported*; a
misrouted nudge is *silent*). `keyed_channels` in the sweep digest reports coverage, so the
number to watch is that count rising.

### 13e. Naming a new channel

When creating a channel for a ticket, name it in the same breath:

```
kan-<n>-<short-slug>     # e.g. kan-45-cli-sales-event-audit
```

Then no description edit and no URL are needed for the loop to find it.
