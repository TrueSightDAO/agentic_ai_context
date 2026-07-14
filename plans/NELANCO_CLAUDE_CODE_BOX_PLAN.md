# Nelanco Claude Code Box — Execution Roadmap

**Status:** Plan-of-record (pre-flight). No infrastructure provisioned yet.
**Created:** 2026-07-14 | **Revised:** 2026-07-14 (scope corrected — see §0) | **Owner:** Gary Teh | **Author:** Claude (Opus)
**Convention:** Follows `OPERATING_INSTRUCTIONS.md` §5 (roadmap-before-code), §5a (one PR/turn),
§5c (auto-advance gates), §5d (pre-flight completeness).

---

## 0. Scope correction (read this first)

The first draft of this plan assumed the new box would run a **second autonomous Sophia**. **It will not.**
Corrected intent (Gary, 2026-07-14):

- The box runs **plain interactive Claude Code** — Gary is the driver. **No** `truesight_autopilot`
  service, **no** FastAPI/DeepSeek/email-poller/Telegram/watchdog/autonomous loop.
- The box's **environment mirrors Sophia's box**: all codebases cloned, all credentials laid down, **and
  — emphasized — every bit of SSH access Sophia's box has** (her fleet bastion key + Nelanco SG allowlist +
  fleet host aliases), so Claude on this box can SSH the whole Krake/Perch/Edgar fleet exactly as she can.
- **Run mode is manual:** `ssh` into the box → start `claude` inside a **`tmux`** session → enable
  **remote-control** → drive it from the **Claude mobile app**.

**Consequence:** the autonomous-collision risk (dup PRs, shared Gmail, singleton assumptions) is **gone** —
nothing autonomous runs here. This is "Sophia's environment, but a human is at the keyboard via phone."

---

## 1. Goal

Stand up a new AWS EC2 instance **in the Nelanco account (`767697632458`)** that is an **interactive
Claude Code jump-box with Sophia-level environment parity**:

1. **Codebase parity** — all workspace repos cloned on disk.
2. **Credential parity** — full set of `.env`s, Google service accounts, Gmail tokens, clasp token, and the
   DAO signing identity laid down (same laydown Sophia's `deploy.sh` performs).
3. **SSH-access parity (the emphasized requirement)** — the box can SSH into the **entire Nelanco fleet**
   the same way Sophia does: fleet private key present, box allowlisted on the Nelanco SGs, fleet host
   aliases in the box's `~/.ssh/config`.
4. **Mobile drive** — `claude --remote-control` (started manually in `tmux`) so Gary controls the
   session from the Claude iOS/Android app, with the box's full filesystem + creds + fleet SSH available.

### Non-goals
- **Not** running the autopilot / any autonomous agent (see §0).
- **Not** migrating Krake/Perch/Edgar — this is a new box alongside them.
- **Not** exposing a public inbound SSH/web port for the Claude experience (remote-control is expected to
  use an **outbound** relay — verify at Gate D).

---

## 2. The decisive technical finding — `--remote-control`, NOT `--cloud`

Future agents: do not confuse these. They have **opposite** properties.

| | `claude --cloud` / the mobile app's own "Code" sessions | `claude --remote-control` |
|---|---|---|
| Where tool calls execute | Anthropic-managed sandbox VM | **This EC2 box** |
| What the agent sees | fresh clone of the **GitHub** remote | **local filesystem + all local creds + fleet SSH + MCP** |
| Local credentials usable? | ❌ no | ✅ yes |
| Mobile app's role | it *is* the session | **a window into the session running on the box** |

Docs: `code.claude.com/docs/en/remote-control.md` — *"Remote Control sessions run directly on your
machine and interact with your local filesystem. The web and mobile interfaces are a window into that
local session… your code execution and filesystem access stay on your machine."* Handoff note
(`claude-code-on-the-web.md`): you can `--teleport` a cloud session **down** to a terminal, but you
**cannot push** a terminal session up to `--cloud`; `--remote-control` is the correct bridge for a
box-resident session. Requires a Claude **Pro/Max/Team** subscription on the account the box's CLI
authenticates as.

**Gary's run recipe (manual, no service needed):**
```bash
ssh nelanco-claude          # the ~/.ssh/config alias added at Gate C
tmux new -s claude          # or: tmux attach -t claude
claude                      # then /remote-control   (or launch: claude --remote-control "nelanco")
# phone: Claude app → session list → pick "nelanco" → drive it
```
`tmux` keeps the session alive across SSH disconnects; remote-control is enabled on demand, not as a
systemd unit. (Optional convenience later: a `tmux` autostart or a helper script — not required.)

---

## 3. Pre-flight checklist

> ✅ **Pre-flight Completeness (§5d):** the current Sophia env/cred/SSH laydown, the Nelanco topology +
> SSH allowlist, and the remote-control mechanics needed by the execution units are transcribed below.
> Execution PRs adapt scripts already in-repo; no unit needs to read a cross-repo file to *learn* how it
> works. Open **decisions** (§3.5) must be resolved before their gate.

### 3.1 Sophia's env/cred/SSH laydown (the parity source — replicate the laydown, NOT the services)

Source repo: `truesight_autopilot/` (`TrueSightDAO/truesight_autopilot`). We reuse its **laydown**
mechanics but **do not install** its systemd services (`truesight-autopilot*.service`, telegram,
watchdog, vault) or its DeepSeek/poller app.

- **Provisioning:** `scripts/launch_ec2.sh` (AMI, type, key-pair, SG, subnet, EBS) + `scripts/user-data.sh`
  (cloud-init: base packages, git, `/opt` dir owned by `ubuntu`, passwordless sudo). For this box add
  **Claude Code install + `tmux`** to user-data; **omit** the autopilot python/venv/nginx app bring-up.
  **⚠️ Stale:** `launch_ec2.sh` still references account `767697632458` (Nelanco) and pulls AWS creds
  from `cypher_def/.env`, while the *live* autopilot runs in **Explorya `440626669078`**. For this build
  Nelanco is what we want — reconcile the script deliberately, don't copy blindly.
- **Credential laydown** (`scripts/deploy.sh`, run from operator Mac): **merge-only `.env` sync** (box
  `.env` is source of truth); `config/gmail/*.json` + `config/google/*.json` → chmod 600; clone
  `agentic_ai_context` + `tokenomics` (+ any other repos we want on disk); sync `~/.clasprc.json`; set git
  identity + `scripts/git-credential-sophia.sh` global helper (reads PAT from `.env` at call time).
- **SSH fleet access** (the emphasized part): `~/.ssh/sophia_infra` (+`.pub`) is Sophia's **outbound fleet
  identity**; `scripts/distribute_sophia_ssh_key.sh` authorizes it across the fleet, kept in sync with
  `app/tools/ssh_tools.py FLEET`. The fleet host list: krake_nginx, seni_ror, dao_protocol, seni_sk,
  seni_sql, seni_redis, krake_ror, krake_sk*, krake_data, getdata_redis, getdata_cache. The new box needs
  a fleet key + fleet host aliases in **its** `~/.ssh/config` (see D2 for reuse-vs-dedicated).
- **DAO identity:** Claude already has one — `claude_dao_identity/.env` (**Claude Anthropic**,
  admin+claude@truesight.me). Lay that down rather than minting a new Edgar identity.
- **AMI caveat:** any AMI snapshot bakes the on-disk `.env`/keys (secrets) into the image → **encrypt EBS,
  keep AMIs private.**

### 3.2 Nelanco topology & networking (target environment)

- **Account:** Nelanco `767697632458`, region `us-east-1`. Fleet: krake_nginx, seni_ror (Perch),
  dao_protocol_nelanco (Edgar, crown-jewel), dao-protocol-beta, seni_sk (Sidekiq ASG), seni_sql,
  seni_redis, krake_ror, krake_sk_consolidated, krake_data, GETDATA_REDIS/CACHE. Full inventory:
  `agentic_ai_context/infrastructure/AWS_DIGITAL_INFRASTRUCTURE.md`.
- **SSH allowlist:** Nelanco SGs allow **source-IP-restricted** SSH(22)+ICMP only (non-listed sources
  silently time out) — this holds even intra-account unless the SG allows the box's SG/CIDR. The new box's
  reachable IP (private CIDR if same-VPC, else its EIP) **must be added to the Nelanco fleet SG allowlist**
  for SSH-access parity. Fleet key: `NELANCO_aws_20201122.pem` / `GETDATA_IO_PAIR_20201122`.
- Sophia (in Explorya) reaches the fleet as a **bastion**; a box *in* Nelanco is network-adjacent, which is
  a reason this build is cleaner there.

### 3.3 Dedicated vs reused GitHub identity

Claude will file contributions + open PRs from the box. Options: reuse the workspace agent GitHub auth
(agentic_ai_github key + the `TRUESIGHT_DAO_AUTOPILOT` PAT via the credential helper), or mint a fresh push
key + PAT for the box (cleaner audit/revocation). Recommendation: **fresh push key + own PAT** (see D5).
Guardrails unchanged: never push to `*_prod` (promote via `gh repo sync`); `api_only_repos`
(treasury-cache, ledgers, caches) are Contents-API single-file writes only.

### 3.4 Remote-control security model to verify (blocks Gate D)

1. Is the session reachable **without opening an inbound port** (outbound relay to Anthropic)? Confirm with
   `ss -tlnp` + SG showing no new inbound.
2. Is connection **strictly gated to the authenticated Claude account**, or is the session URL/QR a
   **bearer capability** (shareable = dangerous)? Determines whether the URL can ever be logged/shared.
3. Which **Claude account** does the box's CLI authenticate as, and does that same account on Gary's phone
   see the session? (Pro/Max/Team required.)

### 3.5 Open decisions to confirm (owner: Gary) — resolve each before its gate

| # | Decision | Recommendation | Blocks |
|---|----------|----------------|--------|
| D2 | **Fleet SSH key: reuse Sophia's `sophia_infra` or mint a dedicated key for this box?** | **Mint a dedicated key** + distribute its pubkey to the fleet via `distribute_sophia_ssh_key.sh` (independent revocation; a compromise of one box doesn't force re-keying the other). Quick alt: copy `sophia_infra` for immediate parity. | Gate C |
| D3 | **Which Claude account** the box's CLI authenticates as (see §3.4.3). | A dedicated/appropriate Max account Gary's phone is signed into. | Gate C |
| D4 | **Instance size / cost.** | `t3.medium` (Claude Code compute is light — the model runs on Anthropic's side). | Gate B |
| D5 | **GitHub identity** on the box (§3.3). | Fresh push key + own fine-grained PAT. | Gate C |
| D6 | **Which repos to clone** on the box. | All active workspace repos (full parity); at minimum agentic_ai_context + tokenomics + dao_client + the app repos Gary edits. | Gate C |

*(D1 from the prior draft — autonomous-collision — is removed; the box is not autonomous.)*

---

## 4. Sequenced plan (one PR / turn; infra/creds/SSH steps are always-stop gates)

Code-artifact PRs (PR1–PR2) are reviewable without touching live infra; the Gates are guided runbook
steps Gary executes with the artifacts (always-stop by §5c: infra provisioning, credential + SSH-key
laydown).

| Unit | What | Type | Advance |
|------|------|------|---------|
| **PR0** | This roadmap (revised to interactive-only + SSH parity). | doc PR | _(done — this revision)_ |
| **PR1** | Nelanco provisioning artifact in `truesight_autopilot`: `launch_ec2_nelanco.sh` (corrected account/SG/subnet/key, encrypted EBS) + user-data that installs **Claude Code + tmux** and **omits** the autopilot app. Code only — launches nothing. | code PR | _(auto)_ |
| **PR2** | Laydown artifact: adapt `deploy.sh` into a "Claude box" laydown — clone repos (D6), full-parity `.env` + Google/Gmail/clasp creds + `claude_dao_identity`, **fleet SSH key + fleet `~/.ssh/config` aliases on the box**, git credential helper. **No** autopilot/telegram/watchdog/vault units. Code only. | code PR | _(auto)_ |
| **Gate B** | **Provision the EC2** in Nelanco (run PR1 script), allocate EIP, base SG, **add the box to the Nelanco fleet SG allowlist** for SSH parity. | infra | `gate: infra provision` |
| **Gate C** | Run PR2 laydown: full creds + fleet key; **distribute box pubkey to fleet** (D2); install + **auth Claude Code to the account (D3)**; set up GitHub identity (D5). **Add `Host nelanco-claude` alias to Gary's `~/.ssh/config`** (HostName=EIP, User=ubuntu, IdentityFile=deploy key). | prod-ish | `gate: full cred + SSH laydown` |
| **Gate D** | **Verify** remote-control security model (§3.4) **and** fleet SSH from the box (`ssh` into a fleet host). | verify | `gate: security + SSH verify` |

Each execution turn: do the single **RESUME HERE** unit, open the PR (or run the gated step), report the
DAO contribution, tick the tracker, **stop**.

---

## 5. Resume tracker

**➡️ RESUME HERE: Gate C** — laydown (all repos + all creds + dedicated fleet SSH key + fleet `~/.ssh/config` on the box) **and** the interactive `claude` login. Box is provisioned + reachable (Gate B done). PR2 = optional script-ified version of the laydown; the laydown can also be run directly.

### Provisioned resources (Gate B — 2026-07-14)
| Resource | Value |
|----------|-------|
| Instance | `i-01ad5eca707e4445f` (t3.medium, Ubuntu 22.04, encrypted 30GB gp3) |
| Account / VPC / subnet | Nelanco `767697632458` / `vpc-d59748af` / `subnet-de8102b9` (us-east-1a) |
| Security group | `launch-wizard-1` (`sg-003e8016026715f25`) — 22 open 0.0.0.0/0, key-only (Gary's call, dynamic cellular IP) |
| Key pair | `GETDATA_IO_PAIR_20201122` (operator `.pem`: `aws_keypairs/NELANCO_aws_20201122.pem`) |
| Elastic IP | `100.57.50.48` (`eipalloc-046cd5691e3a098a5`) |
| DNS | `claude.truesight.me` → `100.57.50.48` (Explorya Route53 zone `Z0032474227N6EQ3Z4QU`) |
| Operator alias | `ssh nelanco-claude` (in Gary's `~/.ssh/config`) |
| Installed | Claude Code 2.1.197, tmux, node 20, clasp 3.3.0, ffmpeg; workspace `/opt/claude_workspace` |

**Still needed at Gate C:** clone all repos → `/opt/claude_workspace`; lay down creds (`.env`s, Google SAs, Gmail tokens, `~/.clasprc.json`, `claude_dao_identity`); mint a **dedicated fleet SSH key** on the box + distribute to the fleet (`distribute_sophia_ssh_key.sh` variant) + fleet host aliases in the box's `~/.ssh/config`; add the box EIP `100.57.50.48` to the Nelanco fleet SG allowlists; and Gary runs `claude` login (Pro/Max/Team account — interactive, cannot be scripted).

| Unit | PR opened | Merged (human) | Executed / deployed | Contribution reported |
|------|-----------|----------------|---------------------|-----------------------|
| PR0 — roadmap (revised) | ✅ | ✅ #657/#658 | n/a | ✅ |
| PR1 — provisioning artifact (Claude Code + tmux) | ✅ | ✅ #276 (truesight_autopilot) | n/a | ✅ |
| Gate B — EC2 provision + EIP + DNS + ~/.ssh/config | ✅ | ✅ | ✅ 2026-07-14 (`i-01ad5eca707e4445f` / `100.57.50.48`) | ☐ |
| PR2 / Gate C — laydown (creds + repos + fleet SSH) + `claude` login | ☐ | ☐ | ☐ | ☐ |
| Gate D — security + fleet-SSH verify | ☐ | ☐ | ☐ | ☐ |

---

## 6. UAT (human-tested, before treating the box as live)

Run from Gary's phone + the box:

1. **Remote-control reachability** — `ssh nelanco-claude` → `tmux` → `claude` → `/remote-control`; Claude
   mobile app shows the named session; connect. **Pass:** you can send a message and see it respond.
2. **Execution is on the box (not Anthropic cloud)** — from the phone, ask it to run
   `hostname && whoami && pwd` and read a local-only path listing. **Pass:** the new box's hostname + local
   workspace path (state a cloud clone couldn't see).
3. **Credentials work** — from the phone, a **read-only** cred-dependent action (e.g. `dao_client`
   `auth.py status`, or a Sheets read). **Pass:** authenticated, no missing-credential error.
4. **SSH-access parity** — from the phone-driven session, `ssh` into a Nelanco fleet host (e.g.
   `dao_protocol` or `seni_ror`) and run `hostname`. **Pass:** logs into the fleet host — full parity with
   Sophia's reach.
5. **No inbound exposure** — on the box, `ss -tlnp` and the SG show **no new public inbound port** for the
   Claude experience. **Pass:** remote-control rode an outbound relay (§3.4.1).
6. **`~/.ssh/config` alias** — `ssh nelanco-claude` from Gary's Mac connects. **Pass:** login succeeds.

Acceptance: all 6 pass → the box is a live, phone-drivable, Sophia-parity Claude Code environment.

---

## 7. Security summary (why this shape is defensible)

- **Execution stays on the box** (remote-control, not cloud) → credentials never ship to Anthropic's
  sandbox. Trust boundary ≡ SSHing in yourself.
- **Likely no inbound port** (outbound relay) → smaller attack surface than exposing SSH/web (verify, Gate D).
- **Not autonomous** → no unattended actor holding these creds; the box only acts while Gary drives it.
- **Dedicated fleet + GitHub identities** (D2/D5) → independent audit/revocation; a compromise of this box
  doesn't force re-keying Sophia.
- **Encrypted EBS + private AMIs** → the `.env`/keys-in-AMI caveat is contained.
- **Concentration risk remains** (all DAO creds + full fleet SSH on one phone-drivable box): mitigations are
  hard 2FA on the Claude account and a documented kill switch (kill the `tmux`/remote-control session /
  rotate the box's fleet key + PAT / terminate the box). Because fleet access here is *the point*, the main
  residual control is treating loss of the phone/Claude-account as a fleet-key rotation event.
