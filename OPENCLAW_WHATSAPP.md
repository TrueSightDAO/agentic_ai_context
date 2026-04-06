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

If the body is long, split into **two sequential messages**; the gateway may **timeout** if sends are parallel—wait **a few seconds** between calls.

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

Put **technical proof** (commits, PRs, sheet links) in the **bullets below** the TLDR. The **`tldr` column** on **`OpenClaw Beer Hall updates`** should use the same plain, DAO-focused wording so the log stays useful for non-technical readers.

For **Founder Haus AI**, the TLDR can emphasize **how we use AI and automation**, but should still open with **outcomes in plain language** before naming tools.

### Beer Hall — full DAO / ops digest

**Target:** **The Beer Hall** — `120363041505997891@g.us`.

When the operator asks for a **daily** or **session** summary:

1. **TLDR** at the top, following **§ TLDR — plain language, DAO-relevant** (above): outcomes in everyday language and explicit **why it matters for the DAO** before any technical bullets.
2. **Bullets** with **links** where applicable: **merged PR** URLs (preferred once merged), **`/commit/<sha>`** links, relevant **Google Sheets** (e.g. [Contribution Ledger](https://docs.google.com/spreadsheets/d/1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU/edit), [Telegram compilation](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit)).
3. **Typical scope:** shipped **email workflow / email-agent** work (`TrueSightDAO/content_schedule`), **double-entry / Contribution Ledger** and context-doc updates (`TrueSightDAO/agentic_ai_context`), **OpenClaw** setup, Agroverse/DAO code when it was part of the session—**only what was actually done**, no filler.
4. **Git before the post (when there are repo changes):** On **`feature/<topic>`** or **`fix/<topic>`**, **push**, open **PR**, **merge** to default branch when the operator wants it live—then cite **PR** and/or **commits** in the digest. If **`gh`** / **`GH_TOKEN`** is unavailable, cite the **commit** and **compare** URL and note that merge is pending.
5. **Dedup log:** Tab **`OpenClaw Beer Hall updates`** on the [Telegram compilation sheet](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ/edit). **Create or migrate** (once): share the spreadsheet with the **`market_research/google_credentials.json`** service account as **Editor**, then run **`market_research/scripts/ensure_beer_hall_log_sheet.py`** (renames legacy **`Beer_Hall_Posts`** if present). **Columns:** `posted_at_utc`, `channel` (**Beer Hall** or **Founder Haus AI**), `tldr`, `links`, `pr_commit_links`, `openclaw_message_id`, `notes`. After each **`openclaw message send`**, append a row so future digests **do not repeat** or **miss** items. See **`agentic_ai_context/SETUP_REQUIREMENTS.md`** (**market_research** / **`google_credentials.json`**).
6. **Reliability:** If **`gateway timeout`** appears, **retry once** after a short sleep; avoid firing multiple sends in parallel against the same gateway.

### Founder Haus AI prompt channel — AI-forward subset

**Audience:** Web3 partner (*@FounderHaus*) — channel is about **AIs and how they are used**, not the full DAO operating report.

**Target:** **Prompt Haus: AI** — `120363195508720633@g.us` (same row as in **Verified JIDs**).

**Process:**

1. Draft the **Beer Hall** digest first (complete picture).
2. Derive a **second, shorter message**: keep only bullets that are **relevant to AI/agent/automation** (e.g. OpenClaw, Cursor workflows, email-agent + LLM context, Grok/draft pipelines, runbook or context-repo changes that teach agentic ops).
3. **Omit or heavily compress:** pure community updates, long non-AI supply-chain narrative, governance detail **unless** it is explicitly about **agentic or AI tooling**.

**Monitoring:** Treat as **outbound share** unless the operator adds this JID to **`channels.whatsapp.groups`** for inbound handling—see **Intended inbound monitor allowlist** above.

---

## Related

- [OpenClaw WhatsApp channel](https://docs.openclaw.ai/channels/whatsapp)
- [OpenClaw pairing (DM vs node)](https://docs.openclaw.ai/channels/pairing)
- [Control UI](https://docs.openclaw.ai/web/control-ui)
