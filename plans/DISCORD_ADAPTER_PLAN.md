# Discord Adapter — Implementation Plan

> **Status:** ✅ **RATIFIED + BUILT.** The governor locked the four policy decisions on
> 2026-09-12 (§0); the adapter is **merged** (`truesight_autopilot` #428 —
> `app/discord_adapter.py`, systemd unit, 18 tests) and **inert by default**. Remaining
> work is **deploy-dark → UAT → activate** (§8).
> **Owner:** Sophia Truesight · **Opened:** 2026-09-12 · **Guild:** TrueSight DAO `923008087315587072`
> **Canonical pattern doc:** `AUTOPILOT_CHANNEL_INTEGRATIONS.md` (venue contract + add-a-venue checklist)
> **Related:** `OPERATING_INSTRUCTIONS.md`, `AI_AGENT_DAO_REGISTRATION.md`,
> `app/telegram_adapter.py`, `app/identity_binding.py`, `app/policy.py`, `app/roles.py`

---

## 0. Locked decisions (governor, 2026-09-12)

| # | Decision | Implication |
|---|---|---|
| 1 | **Full throttle** — Sophia *posts*; not read-only-first | `DISCORD_DRY_RUN` is a first-deploy safety, **not** a permanent posture. |
| 2 | **Sophia has full rights** — same authority as on Telegram | The tier map (§5) is a *response posture*, **not** a capability restriction for governors. |
| 3 | **Identity SSOT = the sheet** — Main Ledger → *Contributors contact information* → **col G "Discord ID"** | No parallel store, **no `/verify` DM flow**. Governor-maintained; the adapter reads + caches it. |
| 4 | **Fixed persona** — one Sophia voice everywhere | No per-channel persona menu; `roles.py` persona selection is **not** wired for Discord. |

---

## 1. Goal

Give Sophia a first-class **Discord adapter** for the TrueSight DAO guild, built the same
way as the existing Telegram adapter: an inbound gateway client, a policy/role gate, DAO
identity binding, vault-held secrets, and a systemd unit. Outcome: a governor can talk to
Sophia **inside Discord channels**, and Sophia can read channel context and post results
back — under the same security invariants that govern Telegram.

**Non-goal:** replacing the Telegram adapter, or reaching feature parity in one PR. This
is a staged build (see §8).

---

## 2. Verified current state (from the Discord API, 2026-09-12)

| Item | Value |
|---|---|
| Guild | **TrueSight DAO** — `923008087315587072` |
| Bot app | **`sophia_truesight`** — user id `1548466367005458572` |
| Bot guild role | `Sophia TrueSight` — `1548469130061938780` (managed) |
| Members | **52** (`GET /guilds/{id}/members` → 200 once *Server Members Intent* was enabled) |
| Channels | **35** (12 text-under-category, categories, 1 voice, 1 news) — Appendix A |
| Roles | **12** — Appendix B |
| Secret | vault `DISCORD_BOT_TOKEN` **v2** (`/opt/truesight_autopilot/vault/`, Fernet-encrypted, audited) |
| Intents enabled | **Message Content** ✅ · **Server Members** ✅ (Presence off) |
| Governor id | `garyjob` = `849324553221832794` |

**Adapter code: MERGED (2026-09-12).** `app/discord_adapter.py` (gateway client, governor
gate, dry-run default), `systemd/truesight-autopilot-discord.service`, and
`tests/test_discord_adapter.py` landed in `truesight_autopilot` PR **#428**. It is **inert**
(`DISCORD_ADAPTER_ENABLED=false`); no process is running yet — deploy is §8.

**Secret hygiene note.** The *first* token was pasted into a group chat; the governor
**reset** it, which killed the leaked copy (all calls 401'd), and the *replacement* was
sent by DM only. Current token is therefore untainted. Standing rule: **never paste the
token in a channel**; rotate via the portal on any suspected exposure.

---

## 3. Security invariants (carry over from Telegram)

1. **Instruction boundary.** Discord message text is **DATA, never INSTRUCTIONS** —
   *unless* the author resolves to a **verified governor** on the DAO ledger. A random
   member (or a channel topic, or pasted content) saying "Sophia, deploy prod / send this"
   is context to be reasoned about, not a command to execute. This is the same invariant as
   the AGENTS `Data/instruction boundary (Security invariant #2)` rule.
2. **Governor allowlist, ledger-resolved.** Authority comes from the DAO ledger mapping,
   not from a Discord role string (roles are attacker-editable by any admin). Binding:
   Discord user id → DAO contributor (see §6).
3. **No secret echo.** Token lives in the vault; never logged, never rendered in a reply.
   Use the existing `app/redaction.py`.
4. **Least privilege.** Request only the intents the adapter uses; post only into
   channels the governor has whitelisted (§5).

---

## 4. Architecture (mirrors the Telegram adapter)

```
Discord Gateway (WebSocket, `discord.py` or raw REST+gateway)
        │  MESSAGE_CREATE / interactions
        ▼
app/discord_adapter.py        ← new: gateway client, channel routing, dedupe
        │
        ├─ app/policy.py            ← reused: role/tool gate (extend for Discord tiers)
        ├─ app/roles.py             ← reused: persona layer (see §5 disambiguation)
        ├─ app/identity_binding.py  ← EXTEND: also resolve Discord user ids
        ├─ app/vault.py             ← reused: DISCORD_BOT_TOKEN
        └─ app/main.py (agent loop) ← reused: same tool set, same guardrails
        ▼
Reply → Discord channel

systemd: truesight-autopilot-discord.service   ← new (mirror of -telegram.service)
```

**Disambiguation — "role" is overloaded.** Two different things:
- **Discord roles** (Governors, Core Contributors, …) = *permission tiers / who is who*.
- `app/roles.py` "roles" (Content Marketing Researcher, SRE/DevOps, …) = *persona /
  which tool subset Sophia uses in a given topic*.
Keep these separate: a **Discord tier** decides *whether/how Sophia responds*; a **persona**
(selected per channel, like per-topic on Telegram) decides *what Sophia does* when she does.

---

## 5. Channel posting posture  **(RESOLVED — decision #1/#2: full throttle)**

**Authority is the governor gate, not the Discord role string** (§3 invariant #2). The tiers
below describe Sophia's *response posture* by audience; they do **not** restrict governor
capability — a resolved governor has full rights in any whitelisted channel (decision #2).
Values are operational config, adjustable without a re-plan:

| Tier | Who | Discord role(s) | Behaviour |
|---|---|---|---|
| **T3 — Governor** | DAO governors | `Governors` | Full: Sophia may act, incl. code/inventory submissions (still behind the same submission gates). |
| **T2 — Contributor** | core/daoversal/engineering/GTM/UX/advisory | `Core/Engineering/GTM/UX/Advisory/Daoversal Contributors` | Sophia may answer, research, draft; **no** signing/prod actions. |
| **T1 — Observer** | `Whitelisted Observers`, `Story Teller` | as named | Read + informational answers only; no action tools. |
| **T0 — Public** | `@everyone` | — | Ignore (bot does not process T0 messages at all). |

**Proposed channel whitelist** (bot reads; ✅ = may also *post*):

| Channel | ID | Proposed tier | Post? |
|---|---|---|---|
| governance | `935778518615347210` | T3 | ✅ |
| treasury-and-liquidity | `935507700102594591` | T3 | ✅ |
| operational-updates | `953314525166321774` | T2+ | ✅ |
| contributions-to-be-recorded | `964813215521464391` | T3 | ✅ |
| appeal-contributions | `964073600661467166` | T3 | ✅ |
| engineering | `923012941937250375` | T2 | ✅ |
| tech-support | `962081045044424774` | T2 | ✅ |
| project-goals | `954218893872889896` | T2 | ✅ |
| roadmap | `953335960215638066` | T2 | ✅ |
| latest-contributions | `958430712258773032` | T1 | ❌ |
| market-talks | `956943535263871077` | T1 | ❌ |
| research / ux-and-design / marketing | `946663866677469204` / `935778900796129341` / `960406431461429288` | T1 | ❌ |
| game-design / nft-planning / nft-artworks | `974633628250308649` / `947427462776766475` / `956426869023055882` | T1 | ❌ |
| polls / betting-pool | `956944610398191686` / `948221452530909236` | T1 | ❌ |
| general | `923008087315587075` | T1 | ✅ |
| announcements-and-updates (news) | `935779063702888468` | announce | ✅ (no replies) |
| intro / launchpad / stories… | `935750239728590918` / `1021467682735919115` / `990825275107442688` | T1 | ❌ |
| regional (singapore/NA/SA/europe/japan/KR) | Appendix A | T1 | ❌ |

**First deploy = dry-run, then full posting (decision #1).** `DISCORD_DRY_RUN=true` composes
replies without sending so the governor can eyeball them; on explicit "go" it flips to `false`
and posting is live — start with **one channel** (`general` or `engineering`), then widen.

---

## 6. Identity binding (Discord user id → DAO contributor)

**SSOT (decision #3):** Main Ledger **`Contributors contact information`** tab, column
**G "Discord ID"** (`COL_DISCORD_ID = 6`), spreadsheet
`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`. **Governor-maintained** — humans seed ids;
the adapter only reads (+ a short TTL cache so the hot path never double-hits the Sheets API).
No `/verify` flow, no parallel store (supersedes the earlier proposal).

- Discord binding is read inline in `app/discord_adapter.py` (mirrors
  `identity_binding.py`, which holds the Telegram binding at `COL_TELEGRAM_ID = 23`).
- **Authority = ledger/Governors-cache-resolved governor**, never the Discord role string.
- Id in **col G** + present in the **Governors** cache ⇒ role GOVERNOR.
- **Bootstrapping:** `DISCORD_ALLOWED_USER_IDS` env allowlist covers the gap until col G is
  seeded (`garyjob` = `849324553221832794` → Gary Teh is the first row).
- **Fail-closed:** unknown author ⇒ not a governor ⇒ handled per §3 (data, not instructions).

---

## 7. Config surface

Actual merged fields (`app/config.py`):

| Key | Where | Purpose |
|---|---|---|
| `DISCORD_BOT_TOKEN` | **vault** (`app/vault.py`) | gateway auth — never env, never logged |
| `DISCORD_GUILD_ID` | `.env` → `discord_guild_id` | `923008087315587072` |
| `DISCORD_ALLOWED_USER_IDS` | `.env` → `discord_allowed_user_ids` | comma-separated snowflakes; empty ⇒ sheet-only |
| `DISCORD_GOVERNOR_NAME` | `.env` → `discord_governor_name` | identity the bot speaks as (default `Gary Teh`) |
| `DISCORD_ADAPTER_ENABLED` | `.env` → `discord_adapter_enabled` | feature flag, default **False** |
| `DISCORD_DRY_RUN` | `.env` → `discord_dry_run` | compose-but-don't-send, default **True** |

*(The earlier `DISCORD_CHANNEL_TIERS` map was **not** implemented — channel routing is by
session id `dc:{guild}:{channel}` in the adapter; per-channel *posting* control is via the
Discord-side channel whitelist / bot permissions.)*

---

## 8. Milestones

The staged read-only PR1–PR3 sketch was **collapsed into one build PR** because decision #1
(full throttle) made a separate read-only stage unnecessary — the dry-run flag is the
read-only stage.

| Step | Scope | Status / Gate |
|---|---|---|
| **#428** | `app/discord_adapter.py` + config + systemd unit + tests (gate merges before any brain call; dry-run default) | ✅ **merged** (`truesight_autopilot`) |
| **#429** | README self-doc (service table / diagram / layout) | ✅ **merged** |
| **#1057** | Canonical `AUTOPILOT_CHANNEL_INTEGRATIONS.md` | ✅ **merged** |
| **Deploy-dark** | `deploy_autopilot`; install + start `truesight-autopilot-discord.service` with `ENABLED=true` + `DRY_RUN=true`; watch journal for composed-but-unposted replies | governor UAT |
| **Activate** | flip `DISCORD_DRY_RUN=false` (live posting, one channel first) | **explicit governor go** |

Each PR: local test suite green before push (compileall / ruff check / ruff format --check / pytest).

---

## 9. UAT checklist (for PR2/PR3)

- [ ] Bot connects, backfills nothing, logs `MESSAGE_CREATE` from a whitelisted channel.
- [ ] A T0/unknown author's message is **ignored** (not processed, not replied to).
- [ ] A T2 author gets an informational reply but **cannot** trigger a signing/prod action.
- [ ] A T3 (governor `garyjob`) author can trigger the normal agent loop.
- [ ] Message text containing "deploy prod" from a **non-governor** is treated as data.
- [ ] Token never appears in any log line (grep the journal).
- [ ] `DISCORD_DRY_RUN=true` → replies are composed but **not sent**.

---

## 10. Resolved questions

| Question | Answer (2026-09-12) |
|---|---|
| Read-only or post? | **Post — full throttle** (§0 #1). |
| Identity-binding source | **Sheet, col G** — the *Contributors contact information* tab (§0 #3, §6). |
| Persona | **Fixed** — no per-channel menu (§0 #4). |
| Library | **Raw REST + gateway** (no `discord.py` dependency); see `app/discord_adapter.py`. |

**Still open (operational, non-blocking):**
1. **Seed col G** — currently 1 row (`garyjob`); the env allowlist covers the gap meanwhile.
2. **Channel posting whitelist** — confirm which channels Sophia may post into first
  (proposal: `general` + `engineering`), then widen (§5).

---

## Appendix A — Channels (35, from API)

Uncategorised: `Social Hangouts – AAA` (voice, `923008087315587076`), `intro` (`935750239728590918`),
`betting-pool` (`948221452530909236`), `roadmap` (`953335960215638066`), `latest-contributions` (`958430712258773032`),
`appeal-contributions` (`964073600661467166`), `contributions-to-be-recorded` (`964813215521464391`),
`announcements-and-updates` (news, `935779063702888468`).

**Our Community** (`950087920478462002`): `launchpad` `1021467682735919115`, `general` `923008087315587075`,
`stories-from-the-underground` `990825275107442688`, `polls` `956944610398191686`, `market-talks` `956943535263871077`,
`tech-support` `962081045044424774`, `singapore` `950071414747201656`, `north-america` `950366381445103647`,
`south-america` `959181330871119893`, `europe` `959181361296584825`, `japan` `959181404212715551`,
`south-korea` `959181430896869446`.

**Building our Game** (`950088018658738217`): `nft-planning` `947427462776766475`, `nft-artworks` `956426869023055882`,
`research` `946663866677469204`, `ux-and-design` `935778900796129341`, `marketing` `960406431461429288`,
`engineering` `923012941937250375`, `game-design` `974633628250308649`.

**Building our DAO** (`953325803788173372`): `operational-updates` `953314525166321774`, `project-goals` `954218893872889896`,
`whitepaper` `934388723364298773`, `governance` `935778518615347210`, `treasury-and-liquidity` `935507700102594591`.

## Appendix B — Roles (12, from API)

| Pos | Role | ID |
|---|---|---|
| 11 | Server Booster (managed) | `949641746076303360` |
| 10 | **Governors** | `951776140224245770` |
| 9 | Story Teller | `989628875522863185` |
| 8 | Advisory Contributors | `953128773887328306` |
| 7 | User Experience Contributors | `953444829726117948` |
| 6 | Go To Market Contributors | `953444539924906034` |
| 5 | Engineering Contributors | `953443988940140624` |
| 4 | Daoversal Contributors | `960868797659643966` |
| 3 | Core Contributors | `949645881915879483` |
| 2 | Whitelisted Observers | `955639759114502225` |
| 1 | Sophia TrueSight (managed, bot) | `1548469130061938780` |
| 0 | @everyone | `923008087315587072` |

## Appendix C — Members

52 total. Governor seed: `garyjob` `849324553221832794`. Full roster retrievable via
`GET /guilds/923008087315587072/members`. (Human user ids deliberately not dumped here;
bind via §6.)
