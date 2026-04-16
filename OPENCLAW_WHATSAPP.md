# OpenClaw + WhatsApp

Workspace reference for **group JIDs**, **inbound monitor intent**, and **operational playbooks** when using [OpenClaw](https://docs.openclaw.ai/) with the WhatsApp channel. High-level workspace overview: **`WORKSPACE_CONTEXT.md`**.

**Runtime config** (allowlists, policies) lives on the gateway host in **`~/.openclaw/openclaw.json`** — not in this repo. Keep this file aligned with what the operator actually sets there.

**If the operator asks:** “Which JIDs must **not** be in **`channels.whatsapp.groups`** (or otherwise used for OpenClaw monitoring)?” — answer from **§ [Monitoring exclusion list](#monitoring-exclusion-list-canonical)** below, not from raw IndexedDB dumps alone.

---

## Monitoring exclusion list (canonical)

These group JIDs are **out of scope** for **inbound monitoring** and for **routine OpenClaw targeting**. **Do not** add them to **`channels.whatsapp.groups`** unless the operator explicitly changes policy.

| JID | Reason (short) |
|-----|----------------|
| `120363021728603111@g.us` | Operator: not a monitored destination. |
| `120363045636468285@g.us` | Operator: not a monitored destination. |
| `14158598599-1508719921@g.us` | Operator: hands-off; do not tune or test against without explicit ask. |

*(This is the same set as **Excluded JIDs** further down—kept here under an explicit “monitoring” heading so Q&A is unambiguous.)*

### IndexedDB / `abpropGroupConfigs` (and similar)

Rows in **`model-storage` → `abpropGroupConfigs`** (keys like `(2) ['<jid>@g.us', '25322']`, objects with `groupJid`, `configCode`, etc.) reflect **WhatsApp Web internal experiment/config state**, not the workspace’s OpenClaw monitor policy. **Two JIDs appearing beside each other in that store does not imply both should be monitored or both excluded.** Always match JIDs against **this file** (verified vs exclusion list vs monitor intent).

---

## Verified JIDs (field-tested)

Use these for **`openclaw message send --channel whatsapp --target '<jid>'`**. JIDs are chat addresses, not secrets, but treat this doc as the workspace source of truth—**always confirm with a test send** if unsure, because IndexedDB rows can be easy to mislabel.

| Display name | JID | Notes |
|----------------|-----|--------|
| **The Beer Hall** | `120363041505997891@g.us` | **Verified:** OpenClaw test message delivered and observed in this chat (Apr 2026). |
| **Prompt Haus: AI** / **Founder Haus AI prompt** (*@FounderHaus*, Web3 partner) | `120363195508720633@g.us` | **Verified** (test send Apr 2026). Partner-run channel focused on **AI usage and tooling**. Use for **AI-filtered outbound digests** only (see **[Founder Haus AI digest](#founder-haus-ai-prompt-channel--ai-forward-subset)**). Not assumed for routine full-DAO traffic unless asked. |

**Earlier note:** The same numeric id was once associated with *The Do Nothing Society* via **`model-storage` → `abpropGroupConfigs`**; delivery testing showed messages land in **The Beer Hall**. If *The Do Nothing Society* is a **separate** group, resolve its JID using the playbook below and add a new row after verification.

---

## Excluded JIDs (do not monitor, do not target)

Same JIDs as **[Monitoring exclusion list](#monitoring-exclusion-list-canonical)**. Operator confirmed these **group** JIDs are **not** desired for OpenClaw automation or monitoring—**do not** add them to **`channels.whatsapp.groups`** or send operational traffic there unless the operator overrides.

| JID | Notes |
|-----|--------|
| `120363021728603111@g.us` | Not a monitored destination (confirmed earlier). |
| `120363045636468285@g.us` | Not a monitored destination (confirmed). |
| `14158598599-1508719921@g.us` | Do **not** target or tune OpenClaw against this group—operator: hands-off. |

---

## Intended inbound monitor allowlist (`channels.whatsapp.groups`)

**Authoritative runtime config** for *which groups OpenClaw may handle inbound traffic from* is **`channels.whatsapp.groups`** in **`~/.openclaw/openclaw.json`**. The table below is **workspace intent** so assistants stay aligned when editing that config—**merge with the operator** if it drifts.

| Include for inbound monitoring? | Display name | JID |
|----------------------------------|--------------|-----|
| **Yes (operator default)** | **The Beer Hall** | `120363041505997891@g.us` |
| **Optional** | **Prompt Haus: AI** (*@FounderHaus*) | `120363195508720633@g.us` — add only if the operator wants the **agent to read/respond** there; otherwise keep for **outbound shares** only. |
| **Never** | — | Any JID listed under **Excluded JIDs** above. |

If **`groups`** is **omitted** in config, OpenClaw may treat **all** joined groups as eligible (per [OpenClaw WhatsApp](https://docs.openclaw.ai/channels/whatsapp))—tighten with an explicit list when you want monitoring limited to the rows above.

---

## Lookup: specific JIDs (operator questions / IndexedDB scraps)

Use this when the operator pastes JIDs from DevTools (e.g. `abpropGroupConfigs`) and asks what we already know.

| JID | Excluded from monitoring? | Workspace interaction summary |
|-----|-------------------------|------------------------------|
| `120363041505997891@g.us` | **No** — this is **The Beer Hall**, **default YES** for inbound monitor **intent** (see table above). | **Yes, interacted:** OpenClaw test sends; operator confirmed delivery in this chat. Also seen in IndexedDB with `configCode` **`25322`** — that does **not** change monitor policy. |
| `14158598599-1508719921@g.us` | **Yes** — **[exclusion list](#monitoring-exclusion-list-canonical)**. | **Yes, discussed:** operator said hands-off; listed excluded. A **test send was attempted** once from automation; CLI hit **gateway timeout**, so delivery was **uncertain**—avoid retrying without explicit operator OK. Same `configCode` **`25322`** pattern can appear next to other JIDs in `abpropGroupConfigs`; treat as unrelated to allowlisting. |

---

## Restrict inbound handling (`channels.whatsapp`)

WhatsApp is one linked account; OpenClaw does not register “per-channel” listeners like Slack. **Inbound handling** is gated in **`~/.openclaw/openclaw.json`** under **`channels.whatsapp`**, especially:

- **`groups`** — if set, only these **group JIDs** are allowlisted for group traffic (omit or use documented wildcards only if you intend “all groups”).
- **`groupPolicy`** / **`groupAllowFrom`** — who may **trigger** the agent in groups; see [OpenClaw WhatsApp](https://docs.openclaw.ai/channels/whatsapp).

After changing JIDs or policy, restart or apply config so the gateway picks up changes.

---

## How to find JIDs for other WhatsApp groups or channels

Standard **chat export ZIPs** do **not** include JIDs—use the client or a test send.

1. **Chrome + WhatsApp Web (same machine as the linked account)**  
   Open the **target chat** (so it is active). **F12 → Application → IndexedDB** for `https://web.whatsapp.com`. Inspect **`model-storage`** and **`wawc`** object stores; search values for **`@g.us`** (classic groups) or **`@newsletter`** (**Channels**). Match the id to the **chat title / subject** in the same object when possible.

2. **Confirm with a harmless test**  
   `openclaw message send --channel whatsapp --target '<jid>' -m 'OpenClaw JID check — safe to ignore'` and see **which** chat receives it.

3. **Gateway logs**  
   With pairing resolved, **`openclaw logs --follow --json`** (or Control UI logs) may surface **`chatId` / `toJid` / `remoteJid`** for traffic you care about.

4. **CLI pairing snag (loopback)**  
   If the CLI returns **`pairing required`**, approve the device **without** explicit **`--url`** so the local fallback runs, e.g. **`openclaw devices approve --latest`** (see OpenClaw device pairing / Control UI on [http://127.0.0.1:18789/](http://127.0.0.1:18789/)).

---

## Outbound digests: Beer Hall & Founder Haus AI

Playbook for **session / daily summaries** sent with **`openclaw message send --channel whatsapp --target '<jid>'`**. Keep this aligned with operator expectations: **always label automation**, use **WhatsApp-native formatting**, and **link artifacts** (GitHub PRs/commits, sheets) when reporting shipped work.

### Closed loop (required — agents and operators)

Sending the WhatsApp message **alone** is **not** the end of the workflow. **Every** Beer Hall or Founder Haus digest must **also** append one row to tab **`OpenClaw Beer Hall updates`** on the [Telegram compilation sheet](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit) (`gid` in the URL may vary; tab name is authoritative).

1. **After** the OpenClaw send(s) (or **after** failed sends you are recording), run from **`market_research/`**:
   - **`python3 scripts/append_openclaw_beer_hall_log.py`** with **`--channel`** (`Beer Hall` or `Founder Haus AI`), **`--tldr`** (**Beer Hall:** Message 1 body only — attribution + TLDR; **Founder Haus:** the single digest text), **`--links`**, **`--pr-commit-links`** (**Beer Hall:** from Message 2), **`--openclaw-message-id`** if the CLI printed one (or both IDs in **`--notes`** for Beer Hall), **`--notes`** if the gateway timed out or the post was manual.
2. **Do not** mark the digest task complete until the sheet row exists (exceptions: no `google_credentials.json` / no sheet access — then **`--notes`** must say so and a human must log later).
3. **Git archive (Beer Hall — default for routine publishes):** After the sheet row exists, write a **Markdown + YAML frontmatter** entry into [**TrueSightDAO/ecosystem_change_logs**](https://github.com/TrueSightDAO/ecosystem_change_logs) so the same digest is **versioned for review** and can later be **surfaced on truesight.me**. From **`market_research/`**, with Message 1 and Message 2 bodies in temp files (same text as WhatsApp):  
   **`python3 scripts/archive_beer_hall_changelog.py --repo ../ecosystem_change_logs --slug <short-hint> --tldr-file … --message2-file …`** plus the same **`--links`**, **`--pr-commit-links`**, **`--openclaw-message-id`**, and **`--notes`** you used for the sheet row. Then **`git` commit** and **merge** (PR or direct to `main`, per your governance). Format rationale and layout: see **`ecosystem_change_logs/README.md`**. *Skip only when the operator explicitly waives git archive (e.g. emergency) or the clone is unavailable — then record that in sheet **`notes`**.*

One-time setup: service account **Editor** on the spreadsheet; tab ensured via **`market_research/scripts/ensure_beer_hall_log_sheet.py`**. Details: **§ Beer Hall** step **Dedup log** below.

### GitHub links: TrueSightDAO only (Beer Hall & Founder Haus)

**Beer Hall** and **Founder Haus AI prompt** readers care about **DAO / Agroverse / TrueSight** work—not personal or legacy data-harvesting org repos.

When including **GitHub** URLs (PR, commit, compare, tree) in digests for **either** channel:

- **Include** only repositories under **`https://github.com/TrueSightDAO/`** (e.g. [TrueSightDAO](https://github.com/TrueSightDAO/) org on GitHub).
- **Do not** link codebases under other owners, including personal accounts such as **`https://github.com/garyjob`** or other orgs such as **`https://github.com/KrakeIO`**, even if those repos were edited in the same Cursor session.

**If** the session shipped work **only** outside **`TrueSightDAO/`**: for Beer Hall / Founder Haus, **omit GitHub links** (or describe non-DAO outcomes in plain language **without** external-repo URLs). Non-DAO PRs/commits may still be logged elsewhere (e.g. operator notes, other channels)—not in these two WhatsApp digests.

**Non-GitHub links** remain allowed when DAO-relevant (e.g. Google Sheets, **`truesight.me`**, **`agroverse.shop`**, partner docs)—subject to the usual “plain TLDR first” rule.

### Attribution (required for both channels)

Every digest must open with a clear line that the post is **generated via OpenClaw and Cursor**, **not** manually written by the founder/operator. Examples:

- **Beer Hall:** `*OpenClaw × Cursor — daily state of the DAO (not a manual post from Gary)*`  
  (Adjust the name if someone else is the named operator.)

- **Founder Haus AI prompt:** `*OpenClaw × Cursor — AI / agent tooling update (automated summary; not a manual post from Gary)*`  
  (Stress **tooling and how AIs are used**; see subset rules below.)

### WhatsApp-safe formatting

Use patterns WhatsApp actually renders:

| Use | Avoid (GitHub / docs style) |
|-----|-----------------------------|
| `*bold*`, `_italic_`, `~strikethrough~`, `` `inline code` `` | `**bold**`, `# headings` |
| `- ` or `* ` bullets, `> ` quote | Markdown tables, ` ``` ` fenced code blocks |
| Plain `https://…` URLs (tap-to-open) | Assuming `[text](url)` renders as Markdown links |

For **Beer Hall** specifically, always use **two sequential messages** (see **[Beer Hall — two WhatsApp messages](#beer-hall--two-whatsapp-messages-mandatory)**): **Message 1** = attribution + **TLDR** only; **Message 2** = **Shipped** (PR/commit/sheet bullets) plus optional **Community (Telegram log)**. Do **not** combine TLDR and Shipped in one bubble. For **Founder Haus AI**, a **single** shorter message remains the default unless the operator asks otherwise.

For any channel, avoid **parallel** sends to the same gateway—the gateway may **timeout**; wait **a few seconds** between sequential calls.

### Gateway timeout vs send failure (avoid duplicate WhatsApp posts)

The **`openclaw message send`** CLI often reports **`Error: gateway timeout after 10000ms`** even when the **gateway already accepted the job** and WhatsApp **delivered** the message. **Automatically re-running the same send because it timed out frequently produces duplicate bubbles** in the group.

**Mandatory behavior for agents and operators**

1. **Do not** resend the **same** message body on timeout **without** checking whether the first send actually landed.
2. **Verify first** (pick at least one):
   - **Gateway log:** e.g. **`/tmp/openclaw/openclaw-*.log`** or **`~/.openclaw/logs/gateway.log`** — look for **`[whatsapp] Sent message`** / a successful **`ws`** send result **after** your attempt.
   - **Control UI / logs:** **`openclaw logs`** if configured; or inspect the running gateway terminal output.
   - **Human:** operator confirms the text appears **once** in the target chat.
3. **If verification shows the message arrived:** treat the CLI error as **cosmetic**; proceed (e.g. send **Message 2** only if Message 1 is confirmed, then sheet row). **Do not** send Message 1 again.
4. **If verification shows it did not arrive:** fix gateway health (restart supervised gateway, wait for **`Listening for personal WhatsApp`** / channel ready), then send **once**. Still avoid double-sends in the same minute.
5. **Sheet `notes`:** when the CLI timed out but logs show delivery, record that (e.g. “CLI timeout; gateway log shows Sent message …”) so future readers do not “retry for safety.”

**Playbook edits elsewhere in this file:** any older **“retry once on timeout”** habit is **replaced** by **verify-then-decide** — see **§ When the operator asks** → **Send** below.

### TLDR — plain language, DAO-relevant (required)

The **TLDR** is for **everyone**, including people who are not engineers. It must be easy to read on a phone and make clear **why the update matters for the DAO**.

**Do**

- Use **everyday words**: what happened, who benefits, what is safer/faster/clearer for the community or operations.
- State **relevance to the DAO** explicitly when it helps: e.g. clearer money tracking, less manual work, better outreach to partners, fewer mistakes, more transparency, faster decisions.
- Keep it to **a few short lines** (often 3–5). One idea per line.

**Avoid**

- Leading with jargon, ticket numbers, or repo shorthand **without** a plain-English hook (those belong in the bullet section with links).
- Assuming the reader knows tools by name only (e.g. “merged PR #12” as the TLDR line)—instead: *We tightened how follow-up emails are drafted so volunteers spend less time on busywork* + link below.

**Structure that works**

1. **What we improved or shipped** (plain English).  
2. **Why it matters for TrueSight / the DAO** (outcome, not implementation).  
3. Optional: **who it helps** (governors, contributors, partners, ops).

**Example (illustrative)**

- Weak: *Pushed `body_plain` migration + CI on content_schedule.*  
- Strong: *Follow-up emails now stay readable on all devices, and the pipeline is less likely to break when we scale—less manual fixing for ops.*

Put **technical proof** (commits, PRs, sheet links) in **Beer Hall Message 2** (*Shipped* — see **[two-message rule](#beer-hall--two-whatsapp-messages-mandatory)**), not in the TLDR message. The **`tldr` column** on **`OpenClaw Beer Hall updates`** should use the same plain, DAO-focused wording as Message 1 so the log stays useful for non-technical readers.

For **Founder Haus AI**, the TLDR can emphasize **how we use AI and automation**, but should still open with **outcomes in plain language** before naming tools.

### Beer Hall — full DAO / ops digest

**Target:** **The Beer Hall** — `120363041505997891@g.us`.

### Beer Hall — two WhatsApp messages (mandatory)

Every **Beer Hall** outbound digest uses **exactly two** `openclaw message send` calls to **`120363041505997891@g.us`**, in order, with a **few seconds** pause between them (no parallel sends).

| Message | Contents |
|--------|-----------|
| **1 — TLDR** | **[§ Attribution](#attribution-required-for-both-channels)** line (Beer Hall variant) **only** as the opener, then **plain-language TLDR** per **[§ TLDR](#tldr--plain-language-dao-relevant-required)**. **No** GitHub URLs, **no** PR numbers, **no** *Shipped* headings in this bubble. Optional one line: “Details + links in next message,” if it helps readers on mute notifications. |
| **2 — Shipped** | Start with a short label readers recognize, e.g. `*Shipped*` or `*Shipped (links)*`, then **bullets** with **TrueSightDAO-only** PR/commit/sheet links, grouped by area/repo if helpful. Append **Community (Telegram log)** per **[§ Gathering Telegram Chat Logs](#gathering-telegram-chat-logs-community--24h--supplement-to-git)** and, when there is signal, **Community (DApp Remarks / field)** per **[§ Gathering DApp Remarks](#gathering-dapp-remarks-field--offline--hit-list)** in the **same** message 2 unless the operator splits it (default: keep Shipped + community blocks together). |

**Sheet row (`append_openclaw_beer_hall_log.py`):** Still **one** row per digest. Store the **full** TLDR text in **`tldr`**; put **all** link URLs for Message 2 in **`links`** / **`pr_commit_links`** as today. In **`notes`**, optionally record **two** OpenClaw message IDs if both sends return one (e.g. `msg1=…; msg2=…`).

### Gathering what merged (multi-repo Git poll — default for digests)

When compiling **what shipped and merged** for Beer Hall (or before drafting the TLDR), **poll the TrueSightDAO repos** in the workspace **instead of relying on memory**. This is the same approach as: fetch each clone, log the default branch for the **target calendar day**, and cross-check **`gh` merged PRs**.

1. **Which repos:** Every local git repo whose **`origin`** URL is **`github.com/TrueSightDAO/...`** (case-insensitive) and that matters for DAO / Agroverse / ops. **At minimum**, when clones exist, include **`PROJECT_INDEX.md`** staples: **`agroverse_shop`** → [agroverse_shop_beta](https://github.com/TrueSightDAO/agroverse_shop_beta), **`market_research`** → [content_schedule](https://github.com/TrueSightDAO/content_schedule) / [go_to_market](https://github.com/TrueSightDAO/go_to_market) (GitHub may show the renamed repo on PR URLs), **`agentic_ai_context`**, **`tokenomics`**, **`dapp`**, **`truesight_me`**, **`TrueChain`**, **`qr_codes`**, **`proposals`** — **only if** `origin` is TrueSightDAO. **Exclude** non-DAO orgs (e.g. KrakeIO) from the **link list** and from “what merged” claims for this digest.
2. **Fetch and default branch:** `git fetch origin`; resolve **`origin/HEAD`** (e.g. `main` or `master`) or try **`main`** then **`master`**.
3. **Date window:** Use the **calendar day** the operator treats as “today” and state **timezone** when ambiguous (e.g. **`date`** on the operator machine; note **UTC vs America/Los_Angeles** — midnight boundaries differ). **Commits:** e.g. `git log origin/<default> --since='YYYY-MM-DD 00:00:00' --until='YYYY-MM-DD+1 00:00:00' --pretty=format:'%h | %ci | %s'` (adjust `--since`/`--until` if you use full ISO with offset).
4. **Merged PRs (cross-check):** For each GitHub repo, when **`gh`** is available:  
   `gh pr list -R TrueSightDAO/<repo> --state merged -L 25 --json number,title,mergedAt,url`  
   Keep rows whose **`mergedAt`** starts with the **target date** (UTC date from API is fine; align with operator expectations). **Prefer PR URLs** in the digest bullets. If **`gh`** is missing, rely on `git log` merge commits and commit messages.
5. **Fast-forwards / direct pushes:** If `main` moved with **no** merge commit, still cite **`/commit/<sha>`** for same-day commits after confirming they are on **`origin/<default>`**.
6. **Synthesis (Git):** From the Git inventory, draft the **engineering / shipped** part of the TLDR and bullets (still **TrueSightDAO-only** GitHub links per **[§ GitHub links](#github-links-truesightdao-only-beer-hall--founder-haus)**).

### Gathering Telegram Chat Logs (community / ~24h — supplement to Git)

**Sheet / tab:** [**Telegram Chat Logs**](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit#gid=0) on the [Telegram compilation workbook](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit) (same file as **OpenClaw Beer Hall updates**; **tab name** is authoritative).

**Why:** Surfaces **community contributions and Telegram-side activity** (synced from the DAO Telegram / Edgar pipeline) that **will not appear** in `git log` — use so Beer Hall is not “code-only.”

1. **Tooling (preferred):** From **`market_research/`**, run  
   **`python3 scripts/list_recent_telegram_chat_logs_for_digest.py`**  
   (default **~24h**; `--hours 48` if the operator asks for a wider window). Needs **`google_credentials.json`** and the service account as **Editor** on the spreadsheet (same as **append_openclaw_beer_hall_log.py**).
2. **Manual:** In the UI, filter or sort by **Status date** (or the column your sheet uses for completion date — often **`YYYYMMDD`**) for the **last 24–48 hours**; read **Contribution made** + **Contributor name** (and **Project name** if useful).
3. **Dedup vs what you already have:** Do **not** repeat a story already covered in the **Git poll bullets** or in **yesterday’s Beer Hall TLDR**. Skip noise: **INVALID**/empty/**Unknown**-only rows, spam, or duplicate messages.
4. **“Meaningful” bar:** Prefer substantive contribution text (moderation, documentation, partner outreach, shipping milestones described in-chat) over one-line chatter.
5. **WhatsApp output:** In **Beer Hall Message 2**, after repo bullets, add a small block, e.g. *Community (Telegram log):* with **1–4 short lines** in plain language — no tables, no pasted JSON. Link the [compilation sheet](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit) once if you reference the log.

### Gathering DApp Remarks (field / offline — Hit List)

**Sheet / tab:** [**DApp Remarks**](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=0) on the [Hit List workbook](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit) (same workbook as **Holistic Wellness Hit List** automation; **tab name** is authoritative).

**Why:** Captures **human field notes** and **turn-by-turn partner / store context** (submitted via the DApp or logged as remarks) that **will not appear** in `git log` and is often **absent from Telegram Chat Logs** — use so Beer Hall reflects **offline** sales and follow-up reality, not only code merges.

1. **Tooling (preferred):** From **`market_research/`**, run  
   **`python3 scripts/list_recent_dapp_remarks_for_digest.py`**  
   (default **~48h** on **Submitted At**; **`--hours 72`** or wider if the operator asks). By default the helper **filters out** rows whose **Submitted By** looks like known **Hit List / automation** scripts; pass **`--include-automation`** when you need the full audit trail (e.g. Places pull summaries). Needs **`google_credentials.json`** and the service account as **Editor** on this spreadsheet (see **`market_research/HIT_LIST_CREDENTIALS.md`**).
2. **Manual:** In the UI, sort **Submitted At** descending; read **Shop Name**, **Status**, **Remarks**, **Submitted By** for the same window you use for Telegram.
3. **Dedup vs Git and Telegram:** Do **not** repeat the same story three times. Prefer **one** crisp line in Message 2 that names the **outcome** (e.g. “two new qualified leads logged”, “buyer asked for follow-up Tuesday”) rather than pasting long **Remarks** text.
4. **Privacy / tone:** Treat **Remarks** as potentially sensitive (partner names, staff quotes). Summarize in **plain DAO-relevant language**; do not dump raw sheet paragraphs into WhatsApp.
5. **WhatsApp output:** In **Beer Hall Message 2**, after the Telegram community block (or merged with it if short), add e.g. *Community (field / DApp Remarks):* with **1–4 short lines**. Link the [Hit List / DApp Remarks sheet](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=0) once if you reference it.

When the operator asks for a **daily** or **session** summary:

1. **Gather evidence:** **§ Gathering what merged** (Git poll; mandatory unless waived) **and** **§ Gathering Telegram Chat Logs** (community **~24h**; default supplement so Telegram is not missed) **and** **§ Gathering DApp Remarks** (field / offline **~48h** default via the helper, aligned with the preview script’s shared **`--telegram-hours`** window unless you run the helper separately).
2. **Draft Message 1 (TLDR only):** **[§ Attribution](#attribution-required-for-both-channels)** (Beer Hall) **+** **§ TLDR — plain language, DAO-relevant** — outcomes in everyday language and explicit **why it matters for the DAO**. **No** link list in this draft.
3. **Draft Message 2 (Shipped):** Bullets with **links** where applicable: **merged PR** URLs (preferred once merged), **`/commit/<sha>`** links, relevant **Google Sheets** (e.g. [Contribution Ledger](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit), [Telegram compilation](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit), [Hit List / DApp Remarks](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=0)). **GitHub:** only **`github.com/TrueSightDAO/...`** (see **[GitHub links: TrueSightDAO only](#github-links-truesightdao-only-beer-hall--founder-haus)**). Add **§ Gathering Telegram Chat Logs** and **§ Gathering DApp Remarks** lines here (summarized, deduped) unless the operator splits them.
4. **Typical scope:** shipped **email workflow / email-agent** work (`TrueSightDAO/content_schedule`), **double-entry / Contribution Ledger** and context-doc updates (`TrueSightDAO/agentic_ai_context`), **OpenClaw** setup, Agroverse/DAO code when it was part of the session—**only what the Git poll (and operator-confirmed non-Git work) shows**; plus **community / Telegram** highlights from **Telegram Chat Logs** and **field / offline** highlights from **DApp Remarks** when they add DAO-relevant signal and pass the dedup bar above — no filler.
5. **Git before the post (when there are repo changes):** On **`feature/<topic>`** or **`fix/<topic>`**, **push**, open **PR**, **merge** to default branch when the operator wants it live—then cite **PR** and/or **commits** in **Message 2** (**`github.com/TrueSightDAO/...` only** in these WhatsApp channels). If **`gh`** / **`GH_TOKEN`** is unavailable, cite the **commit** and **compare** URL and note that merge is pending.
6. **Send (Beer Hall — two messages):** `openclaw message send` **Message 1** (TLDR), wait **a few seconds**, then `openclaw message send` **Message 2** (Shipped + optional Telegram block). See **[Beer Hall — two WhatsApp messages](#beer-hall--two-whatsapp-messages-mandatory)**. If the CLI returns **`gateway timeout`**, follow **[Gateway timeout vs send failure](#gateway-timeout-vs-send-failure-avoid-duplicate-whatsapp-posts)** — **verify** in gateway logs or the chat **before** sending again; **never** assume timeout means the message was dropped. Avoid parallel sends to the same gateway.
7. **Sheet log (mandatory — same session as step 6):** Append **one** row via **`market_research/scripts/append_openclaw_beer_hall_log.py`** with **`--channel "Beer Hall"`**, **`--tldr`** (Message 1 body only), **`--links`**, **`--pr-commit-links`** (everything link-heavy from Message 2), **`--openclaw-message-id`** when the CLI returns it (or document both IDs in **`--notes`**), **`--notes`** on timeout or manual paste. See **§ Closed loop** above. Skipping the sheet step is **not** acceptable unless access is impossible and **`notes`** documents follow-up.
8. **Dedup log — one-time / credentials:** Tab **`OpenClaw Beer Hall updates`** on the [Telegram compilation sheet](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit). **Create or migrate** (once): share the spreadsheet with the **`market_research/google_credentials.json`** service account as **Editor**, then run **`market_research/scripts/ensure_beer_hall_log_sheet.py`** (renames legacy **`Beer_Hall_Posts`** if present). **Columns:** `posted_at_utc`, `channel` (**Beer Hall** or **Founder Haus AI**), `tldr`, `links`, `pr_commit_links`, `openclaw_message_id`, `notes`. For rows tied to these digests, **`pr_commit_links`** should follow the same **TrueSightDAO-only GitHub** rule. See **`agentic_ai_context/SETUP_REQUIREMENTS.md`** (**market_research** / **`google_credentials.json`**).

### Preview digest — review recent progress (no WhatsApp send)

Use this when the operator asks to **review recent progress**, **preview a Beer Hall digest**, or **dry-run** the same evidence gathering **without** posting to WhatsApp and **without** touching the **`OpenClaw Beer Hall updates`** sheet.

1. From **`market_research/`**, run **`python3 scripts/generate_beer_hall_preview.py`**  
   Optional flags: **`--since-days N`** (default **7**), **`--telegram-hours`** (default **48**, forwarded to **`list_recent_telegram_chat_logs_for_digest.py`** and the same look-back to **`list_recent_dapp_remarks_for_digest.py`**), **`--dapp-include-automation`** (include script-originated DApp Remarks rows in the preview evidence block), **`--output /path/to.md`**, **`--no-stdout`** (file only — avoid unless you are redirecting and do not want a duplicate stream).  
   **Default output path:** **`agentic_ai_context/previews/beer_hall_preview_latest.md`** (resolved as `../agentic_ai_context/previews/…` next to the `market_research/` folder — typically under **`Applications/`**).  
   **Console (mandatory for operator review):** The script **always prints the full Markdown to stdout** by default. A single status line **`Written to: …`** goes to **stderr** so piping **`> digest.md`** captures only the digest. When the operator asks to **review recent progress**, assistants must run this command in a way that surfaces **stdout in the tool/terminal transcript** (e.g. Cursor **Run command**) — **do not** only write the file and report “done” with no visible body unless the operator explicitly asked for silent mode (`--no-stdout`).
2. The Markdown includes **placeholders** for **Message 1** (TLDR only) and **Message 2** (*Shipped* + links), then **raw evidence**: per-repo **`git log`** on each local **`TrueSightDAO`** clone in the script’s table, optional **`gh pr list --state merged`** excerpts, the **Telegram Chat Logs** helper output (same workbook as **§ Gathering Telegram Chat Logs**), and the **DApp Remarks** helper output (Hit List workbook; **§ Gathering DApp Remarks**).
3. An assistant or the operator **edits** the two messages into **WhatsApp-safe** text (**[§ WhatsApp-safe formatting](#whatsapp-safe-formatting)**; **[two-message rule](#beer-hall--two-whatsapp-messages-mandatory)**). The file may also contain a **suggested draft** for a specific session (still subject to human edit before any send).
4. **Only after approval:** send with **`openclaw message send`** (Beer Hall: **two** sequential messages) and append **`append_openclaw_beer_hall_log.py`** per **§ Closed loop**. A **preview run alone** does **not** replace steps 6–7 in the numbered list above.

### Founder Haus AI prompt channel — AI-forward subset

**Audience:** Web3 partner (*@FounderHaus*) — channel is about **AIs and how they are used**, not the full DAO operating report.

**Target:** **Prompt Haus: AI** — `120363195508720633@g.us` (same row as in **Verified JIDs**).

**Process:**

1. Draft the **Beer Hall** digest first (**Message 1** TLDR + **Message 2** Shipped — see **[Beer Hall — two WhatsApp messages](#beer-hall--two-whatsapp-messages-mandatory)**), including inventory from **§ Gathering what merged** and **§ Gathering Telegram Chat Logs** so the Founder Haus subset is grounded in the same evidence (Founder Haus: keep **Telegram** lines only if they are **AI/agent/tooling**-relevant).
2. Derive a **second, shorter message**: keep only bullets that are **relevant to AI/agent/automation** (e.g. OpenClaw, Cursor workflows, email-agent + LLM context, Grok/draft pipelines, runbook or context-repo changes that teach agentic ops). **Same GitHub rule as Beer Hall:** link only **`https://github.com/TrueSightDAO/...`** repos; do not link personal or non-DAO org repos (e.g. `garyjob`, `KrakeIO`).
3. **Omit or heavily compress:** pure community updates, long non-AI supply-chain narrative, governance detail **unless** it is explicitly about **agentic or AI tooling**.
4. **Send** to **`120363195508720633@g.us`**, then **mandatory sheet row:** **`append_openclaw_beer_hall_log.py`** with **`--channel "Founder Haus AI"`** (same **§ Closed loop** rule as Beer Hall — one row per outbound digest).

**Monitoring:** Treat as **outbound share** unless the operator adds this JID to **`channels.whatsapp.groups`** for inbound handling—see **Intended inbound monitor allowlist** above.

---

## Related

- [OpenClaw WhatsApp channel](https://docs.openclaw.ai/channels/whatsapp)
- [OpenClaw pairing (DM vs node)](https://docs.openclaw.ai/channels/pairing)
- [Control UI](https://docs.openclaw.ai/web/control-ui)
