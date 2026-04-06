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
| **Prompt Haus: AI** (*@FounderHaus*) | `120363195508720633@g.us` | **Verified** (test send Apr 2026). **FounderHaus**-related group—handy to **share experiment / progress updates** when the operator wants that audience to see what you have tried (not assumed for routine DAO traffic unless asked). |

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

## Related

- [OpenClaw WhatsApp channel](https://docs.openclaw.ai/channels/whatsapp)
- [OpenClaw pairing (DM vs node)](https://docs.openclaw.ai/channels/pairing)
- [Control UI](https://docs.openclaw.ai/web/control-ui)
