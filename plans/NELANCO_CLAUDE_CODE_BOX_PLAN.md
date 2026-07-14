# Nelanco Claude Code Box — Execution Roadmap

**Status:** Plan-of-record (pre-flight). No infrastructure provisioned yet.
**Created:** 2026-07-14 | **Owner:** Gary Teh | **Author:** Claude (Opus)
**Convention:** Follows `OPERATING_INSTRUCTIONS.md` §5 (roadmap-before-code), §5a (one PR/turn),
§5c (auto-advance gates), §5d (pre-flight completeness).

---

## 1. Goal

Stand up a new AWS EC2 instance **in the Nelanco account (`767697632458`)** that is simultaneously:

1. **A full "second Sophia"** — the autonomous `truesight_autopilot` stack (background monitoring,
   diagnosis, PR opening), with **full credential parity** to the existing Sophia box.
2. **An interactive Claude Code jump-box** that Gary drives **from the Claude mobile app** (iOS/Android)
   via **`claude --remote-control`**, with the box's full local filesystem + credentials available to
   the session.

Both roles live on one box, co-located with the Nelanco fleet (Krake / Perch / Edgar).

### Non-goals
- Not migrating the Krake/Perch/Edgar production services — this is a new box alongside them.
- Not exposing an inbound SSH/web port to the public internet for the Claude experience
  (remote-control is expected to use an **outbound** relay — see §3.4, **must verify**).

---

## 2. The decisive technical finding — `--remote-control`, NOT `--cloud`

Future agents: do not confuse these. They have **opposite** properties.

| | `claude --cloud` / the mobile app's own "Code" sessions | `claude --remote-control` |
|---|---|---|
| Where tool calls execute | Anthropic-managed sandbox VM | **This EC2 box** |
| What the agent sees | fresh clone of the **GitHub** remote | **local filesystem + all local creds + MCP** |
| Local credentials usable? | ❌ no | ✅ yes |
| Mobile app's role | it *is* the session | **a window into the session running on the box** |

Docs: `code.claude.com/docs/en/remote-control.md` — *"Remote Control sessions run directly on your
machine and interact with your local filesystem. The web and mobile interfaces are a window into that
local session… your code execution and filesystem access stay on your machine."* One-way handoff note
(`claude-code-on-the-web.md`): you can `--teleport` a cloud session **down** to a terminal, but you
**cannot push** a terminal session up to `--cloud`; `--remote-control` is the correct bridge for a
box-resident session. Requires a Claude **Pro/Max/Team** subscription on the account the box's CLI
authenticates as.

**Implication for this box:** the interactive half is `claude remote-control` running as a persistent
service; the phone connects by finding the session by name in the Claude app session list.

---

## 3. Pre-flight checklist

> ✅ **Pre-flight Completeness (§5d):** the current Sophia deploy model, systemd units, Nelanco topology,
> identity-onboarding flow, and remote-control mechanics needed by the execution units are transcribed
> below. Execution PRs adapt existing scripts they already have in-repo; no unit needs to read a
> cross-repo file to *learn* how it works. Open **decisions** (§3.5) must be resolved before their gate.

### 3.1 Current Sophia / truesight_autopilot deploy model (the template to fork)

Source repo: `truesight_autopilot/` (`TrueSightDAO/truesight_autopilot`).

- **Provisioning:** `scripts/launch_ec2.sh` (AMI, type, key-pair, SG, subnet, EBS) + `scripts/user-data.sh`
  (cloud-init: python3.11/venv, git, nginx, Node 20 + clasp, `/opt/truesight_autopilot` owned by `ubuntu`,
  seeds `authorized_keys` with the agentic_ai_github pubkey, passwordless sudo, CloudWatch agent).
  **⚠️ Stale:** `launch_ec2.sh` still references account `767697632458` (Nelanco) and pulls AWS creds
  from `cypher_def/.env`, while the *live* autopilot runs in **Explorya `440626669078`**. For this
  build Nelanco is actually what we want — reconcile the script deliberately, don't copy blindly.
- **Credential laydown** (`scripts/deploy.sh`, run from operator Mac; `EC2_HOST` alias, key
  `~/.ssh/agentic_ai_github/id_ed25519`): `git reset --hard origin/main` at `/opt/truesight_autopilot`;
  **merge-only `.env` sync** (box `.env` is source of truth, never overwrite existing values);
  `config/gmail/*.json` + `config/google/*.json` → chmod 600; clone `agentic_ai_context` + `tokenomics`
  into `context/`; generate/scp `~/.ssh/sophia_infra` outbound fleet key; sync `~/.clasprc.json`; set git
  identity + install `scripts/git-credential-sophia.sh` global helper (reads PAT from `.env` at call time);
  nginx + certbot.
- **Service model (systemd, `User=ubuntu`):** `truesight-autopilot.service` (uvicorn `app.main:app`
  `:8001`, `--workers 1` **required** — module-level per-session state), `-telegram.service`,
  `-watchdog.service` (Telethon), `truesight-vault.service` (`:8002`).
- **`.env` key inventory** (names; from `.env.example`): `TRUESIGHT_DAO_AUTOPILOT` (PAT), `GMAIL_TOKEN_JSON`,
  `DEEPSEEK_*`, `TAVILY_API`, `GROK_API_KEY`, `EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY` (Edgar identity),
  `AWS_ACCOUNTS`, `AWS_ACCESS_KEY_ID_NELANCO`/`_SECRET_ACCESS_KEY_NELANCO`/`_REGION_NELANCO`,
  `AWS_*_EXPLORYA`, `BUG_SNAG_API`, `JWT_SECRET`, `TELEGRAM_API_ID`/`_HASH`/`_HOME_GROUP_ID`,
  `TELEGRAM_BOT_API_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`, `GMAIL_TOKENS_DIR`, `CONTEXT_REPOS_DIR`, etc.
- **AMI caveat:** weekly AMI snapshot Action bakes the on-disk `.env` (secrets) into the image → **encrypt
  EBS, keep AMIs private.**

### 3.2 Nelanco topology & networking (target environment)

- **Account:** Nelanco `767697632458`, region `us-east-1`. Hosts krake_nginx, seni_ror (Perch),
  dao_protocol_nelanco (Edgar, crown-jewel), dao-protocol-beta, seni_sk (Sidekiq ASG), seni_sql, seni_redis,
  krake_ror, krake_sk_consolidated, krake_data, GETDATA_REDIS/CACHE. Full inventory:
  `agentic_ai_context/infrastructure/AWS_DIGITAL_INFRASTRUCTURE.md`.
- **SSH allowlist:** Nelanco SG allows **source-IP-restricted** SSH(22)+ICMP only (non-listed sources
  silently time out). The new box's **Elastic IP must be added to the Nelanco SG allowlist** if it needs
  to SSH the fleet (Sophia does, as a bastion). Fleet key: `NELANCO_aws_20201122.pem` /
  `GETDATA_IO_PAIR_20201122`.
- **Fleet host list** Sophia's `ssh_run` trusts (keep in sync via `scripts/distribute_sophia_ssh_key.sh`
  ↔ `app/tools/ssh_tools.py FLEET`): krake_nginx, seni_ror, dao_protocol, seni_sk, seni_sql, seni_redis,
  krake_ror, krake_sk*, krake_data, getdata_redis, getdata_cache.

### 3.3 Dedicated identities (do NOT reuse Sophia's)

Per `SERVICE_IDENTITY_ONBOARDING.md`, every actor gets its own keypair. This box needs its own:

- **Edgar/DAO signing identity:** new RSA keypair → `[CONTRIBUTOR ADD EVENT]` → `[EMAIL REGISTERED]` →
  `[EMAIL VERIFIED]` → ACTIVE. New `EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY` in the box `.env`. **Never copy
  Sophia's** — keeps the audit trail and revocation independent. Contributor display name: **TBD**
  (decision §3.5).
- **GitHub push identity:** generate a fresh Ed25519 push key on the box (analog of Sophia's
  `id_ed25519_truesight_autopilot`) + its **own** fine-grained PAT (Contents R/W + PR R/W on
  `TrueSightDAO/*`). Guardrails still apply: never push to `*_prod` (promote via `gh repo sync`),
  `api_only_repos` (treasury-cache, ledgers, caches) are Contents-API single-file writes only.

### 3.4 Remote-control mechanics & the security model to verify

- Start: `claude --remote-control "<name>"` (or `/remote-control` in-session), or **server mode**
  `claude remote-control` to host multiple sessions (prints session URL + QR). Run under systemd/tmux so
  it survives reboot/disconnect. Connect from phone: Claude app → session list → by name.
- **MUST-VERIFY before laying down the full credential set (blocks Gate D):**
  1. Is the session reachable **without opening an inbound port** (outbound relay to Anthropic)? Expected
     yes — confirm hands-on with `ss -tlnp` / SG showing no new inbound.
  2. Is connection **strictly gated to the authenticated Claude account**, or is the session URL/QR a
     **bearer capability** (shareable = dangerous)? Determines whether the URL can ever be logged/shared.
  3. Which **Claude account** does the box's CLI authenticate as, and does that same account on Gary's
     phone see the session? (Pro/Max/Team required.)

### 3.5 Open decisions to confirm (owner: Gary) — resolve each before its gate

| # | Decision | Recommendation | Blocks |
|---|----------|----------------|--------|
| D1 | **Autonomous collision:** two Sophias can't both poll the same Gmail/repos (dup PRs; singleton assumptions). | New Nelanco box becomes **primary** autonomous agent; **demote old Explorya box to standby/retired**. One active autonomous actor, now co-located with fleet. Alt: partition by inbox/repo, or keep new box `DRY_RUN=true` until cutover. | Gate E |
| D2 | **Contributor display name** for the box's Edgar identity. | e.g. `Sophia Nelanco` or a new name — must be pre-created exactly on the Contributors ledger. | Gate A |
| D3 | **Fleet bastion access** — does this box need to SSH-administer the Nelanco fleet, or only run Claude Code against the codebase? | If admin needed: allowlist its EIP + distribute key. If not: **skip fleet SSH** to shrink blast radius. | Gate B |
| D4 | **Claude account** the box authenticates as (see §3.4.3). | A dedicated/appropriate Max account Gary's phone is signed into. | Gate C |
| D5 | **Instance size / cost.** | `t3.medium` (parity with Sophia; Claude Code compute is light — model runs on Anthropic side). | Gate B |

---

## 4. Sequenced plan (one PR / turn; infra/creds/identity steps are always-stop gates)

Most steps are **human-gated** by rule (§5c always-stop: infra provisioning, credential laydown, DAO
identity issuance, autonomous-actor enablement). Code-artifact PRs (PR1–PR2) are reviewable without
touching live infra; the Gates are guided runbook steps Gary executes with the artifacts.

| Unit | What | Type | Advance |
|------|------|------|---------|
| **PR0** | This roadmap file. | doc PR | _(this turn)_ |
| **PR1** | Nelanco provisioning artifacts in `truesight_autopilot`: `launch_ec2_nelanco.sh` (corrected account/SG/subnet/key), `user-data` tweaks, encrypted EBS. Code only — does **not** launch anything. | code PR | _(auto)_ |
| **PR2** | Deploy/laydown for the new box: adapt `deploy.sh` for full-parity `.env` + cred laydown, **add `truesight-autopilot-remote-control.service`** (persistent `claude remote-control` under systemd), Claude Code install in `user-data`. Code only. | code PR | _(auto)_ |
| **Gate A** | Mint the box's **Edgar identity** (CONTRIBUTOR ADD → EMAIL REG/VERIFY → ACTIVE) + fresh GitHub push key + PAT. | identity | `gate: DAO identity issuance` |
| **Gate B** | **Provision the EC2** in Nelanco (run PR1 script), allocate EIP, SG, allowlist per D3. | infra | `gate: infra provision` |
| **Gate C** | Run PR2 laydown: full creds, install + **auth Claude Code to the account (D4)**, start remote-control service. **Add `Host` alias for the box to Gary's `~/.ssh/config`** (mirrors the `sophia` alias — HostName=EIP, User=ubuntu, IdentityFile=the deploy key). | prod-ish | `gate: full cred laydown` |
| **Gate D** | **Verify remote-control security model** (§3.4) hands-on. Gate for enabling autonomous loop. | verify | `gate: security verify` |
| **Gate E** | **Autonomous cutover** per D1: enable autopilot loop as primary, demote Explorya box. | autonomy/money | `gate: enable autonomous actor` |

Each execution turn: do the single **RESUME HERE** unit, open/PR (or run the gated step), report the
DAO contribution, tick the tracker, **stop**.

---

## 5. Resume tracker

**➡️ RESUME HERE: PR0** — merge this roadmap, then next turn starts **PR1**.

| Unit | PR opened | Merged (human) | Executed / deployed | Contribution reported |
|------|-----------|----------------|---------------------|-----------------------|
| PR0 — roadmap | ☐ | ☐ | n/a | ☐ |
| PR1 — provisioning artifacts | ☐ | ☐ | n/a | ☐ |
| PR2 — laydown + remote-control unit | ☐ | ☐ | n/a | ☐ |
| Gate A — identities | ☐ | ☐ | ☐ | ☐ |
| Gate B — EC2 provision | ☐ | ☐ | ☐ | ☐ |
| Gate C — cred laydown + remote-control + ~/.ssh/config | ☐ | ☐ | ☐ | ☐ |
| Gate D — security verify | ☐ | ☐ | ☐ | ☐ |
| Gate E — autonomous cutover | ☐ | ☐ | ☐ | ☐ |

---

## 6. UAT (human-tested, before treating the box as live)

Run from Gary's phone + a browser, against the **new box**:

1. **Remote-control reachability** — Claude mobile app → session list shows the box's named session;
   connect. **Expect:** live session view. **Pass:** you can send a message and see it respond.
2. **Execution is on the box (not Anthropic cloud)** — from the phone, ask it to run
   `hostname && whoami && pwd` and read a workspace-only file that isn't on GitHub (e.g. a local `.env`
   path listing, not contents). **Expect:** the new box's hostname + local workspace path. **Pass:** it
   sees local-only state a cloud clone couldn't.
3. **Credentials work** — from the phone, run a **read-only, dry-run** cred-dependent action (e.g.
   `dao_client` `auth.py status`, or a Sheets read). **Expect:** authenticated success. **Pass:** no
   missing-credential error.
4. **No inbound exposure** — on the box, `ss -tlnp` and the Nelanco SG show **no new public inbound port**
   for the Claude experience. **Pass:** remote-control rode an outbound relay (§3.4.1).
5. **Autonomous loop in DRY_RUN** — autopilot runs with `DRY_RUN=true`, logs an intended action without
   opening a real PR. **Pass:** it would act but didn't, and does **not** collide with Explorya Sophia.
6. **`~/.ssh/config` alias** — `ssh <alias>` from Gary's Mac connects to the box. **Pass:** login succeeds.

Acceptance: all 6 pass → flip autonomous loop live per Gate E / D1.

---

## 7. Security summary (why this shape is defensible)

- **Execution stays on the box** (remote-control, not cloud) → credentials never ship to Anthropic's
  sandbox. Trust boundary ≡ SSHing in yourself.
- **Likely no inbound port** (outbound relay) → smaller attack surface than exposing SSH/web (verify, D/§3.4).
- **Dedicated identities** (Edgar + GitHub) → independent audit/revocation; not entangled with Sophia.
- **Encrypted EBS + private AMIs** → the `.env`-in-AMI caveat is contained.
- **Concentration risk remains** (all DAO creds on one phone-drivable box): mitigations are hard 2FA on the
  Claude account, a documented kill switch (stop `remote-control` unit / rotate identities / revoke PAT),
  and — if D3 says so — *withholding* fleet-bastion SSH so a box compromise ≠ fleet compromise.
