# AWS Digital Infrastructure — Deployment Setup

This document describes the **production AWS infrastructure** for TrueSight DAO / Agroverse. Read this before making assumptions about where services run, how traffic is routed, or which EC2 instance hosts what.

---

## ⚠️ CURRENT STATE BANNER — updated 2026-07-15 (authoritative; supersedes older sections below)

Two changes landed 2026-07-15. **Where the text below conflicts with this banner, the banner wins** (a full line-by-line sweep of the older sections is a pending follow-up).

**1. Sophia (autopilot) migrated Explorya → Nelanco** (AMI lift-and-shift):

| | Old (retired) | New (current) |
|---|---|---|
| Instance | `i-02c699d3d7efbdc82` (**STOPPED** 2026-07-15, kept for rollback) | **`i-05276b8ae82d6b88c`** |
| Account | Explorya `440626669078` | **Nelanco `767697632458`** |
| EIP | `52.200.38.206` (`eipalloc-04772e4a20f10c1c4`) | **`3.214.167.219`** (`eipalloc-018e2cad67ecbcd8a`) |
| VPC / subnet / SG | Explorya `sg-e98f788e` | `vpc-d59748af` / `subnet-de8102b9` / `governor-chatbot-sg` (`sg-0d3b6c10480d83248`, 80/443/22) |
| Type | t3.medium | t3.medium |

`sophia.truesight.me` now → **`3.214.167.219`** (Route53 A, Explorya zone `Z0032474227N6EQ3Z4QU`). All 4 systemd units (`truesight-autopilot`, `-telegram`, `-watchdog`, `truesight-vault`) run on the new box; `DRY_RUN=false`; health `:8001` = 200; nginx serves HTTPS 200. Migration was an **AMI copy** (Explorya `ami-0b05acc998af71d0f` → shared → Nelanco copy `ami-049ff1f01152ef25d`) so the box is a byte-for-byte clone (Edgar identity, Telethon session, code all intact). Weekly AMI backup **retargeted** (Cypher-Defense `snapshot_autopilot_ami`): now Name tag `sophia-nelanco` + `CYPHER_DEFENCE_AWS_*` secrets (Nelanco). **Pending follow-ups:** swap `52.200.38.206`→`3.214.167.219` in fleet SG `dao-protocol-beta-sg` allowlist (SSH); reconcile stale `governor_chatbot`/`chatbot.truesight.me` notes; eventually terminate the stopped Explorya box + prune old Explorya AMIs.

**2. New interactive Claude Code box** (`nelanco-claude`): `i-01ad5eca707e4445f`, EIP **`100.57.50.48`**, `claude.truesight.me`, Nelanco `vpc-d59748af`/`subnet-de8102b9`, SG `launch-wizard-1`. Runs Claude Code (driven from the mobile app via `--remote-control`), Sophia-parity env + fleet SSH — **not** autonomous. Plan: `plans/NELANCO_CLAUDE_CODE_BOX_PLAN.md`.

**Gmail OAuth tokens deployed 2026-07-16:**
- `admin_token.json` → `admin@truesight.me` (gmail.modify scope)
- `gary_token.json` → `gary@agroverse.shop` (gmail.modify scope)
- Both at `/home/ubuntu/` on the Claude box
- SSH config added: `Host sophia` → `3.214.167.219` (key at `~/.ssh/id_ed25519_truesight_autopilot`)
- Sophia's public key added to Claude's `~/.ssh/authorized_keys` (bidirectional)

---

## 0. Architecture Overview

### 0.1 High-Level Account Architecture

```mermaid
flowchart TB
    subgraph Internet["Internet"]
        Users["Users / Operators"]
        GitHub["GitHub Pages"]
    end

    subgraph Explorya["AWS Account: Explorya (440626669078)"]
        R53["Route53\ntruesight.me zone"]
        Autopilot["truesight-autopilot\nt3.medium\nsophia.truesight.me"]
        OldEdgar["seni_ror_2026\nSTOPPED"]
        OldSK["seni_sk_2026\nSTOPPED"]
    end

    subgraph Nelanco["AWS Account: Nelanco (767697632458)"]
        Nginx["krake_nginx\nt2.micro\n54.226.114.186"]
        PerchRails["seni_ror_200250915\nt2.small\nPerch (Rails)"]
        EdgarPython["dao_protocol_nelanco\nt3.small\nFastAPI (Edgar)"]
        Sidekiq["seni_sk_auto\nASG × 2\nSidekiq workers"]
        Postgres["seni_sql_2026\nt2.small\nPostgreSQL"]
        Redis["seni_redis_2\nt2.large\nRedis"]
        KrakeROR["krake_ror\nt2.micro\nKrake Rails"]
        KrakeWorkers["krake_sk_consolidated\nt2.small\n4× Sidekiq processes"]
        KrakeRedis["GETDATA_REDIS\nt3a.small\nRedis"]
    end

    Users -->|HTTPS| R53
    R53 -->|edgar/api/chatbot.truesight.me| Nginx
    R53 -->|sophia.truesight.me| Autopilot
    R53 -->|*.truesight.me| GitHub

    Nginx -->|:3000| PerchRails
    Nginx -->|:8000| Autopilot

    PerchRails --> Postgres
    PerchRails --> Redis
    PerchRails --> Sidekiq

    EdgarPython -.->|same interface| PerchRails

    Users -.->|SSH bastion via Sophia EIP| Autopilot
    Autopilot -.->|ProxyJump| Nginx
    Autopilot -.->|ProxyJump| PerchRails
    Autopilot -.->|ProxyJump| EdgarPython

    style Explorya fill:#1a1a2e,color:#fff,stroke:#e94560
    style Nelanco fill:#16213e,color:#fff,stroke:#0f3460
    style Internet fill:#222,color:#fff,stroke:#555
    style OldEdgar fill:#555,color:#999,stroke:#666,stroke-dasharray: 5 5
    style OldSK fill:#555,color:#999,stroke:#666,stroke-dasharray: 5 5
```

### 0.2 Edgar Service Topology

```mermaid
flowchart LR
    subgraph External["External"]
        GAS["Google Apps Script\nWebhooks"]
        Stripe["Stripe"]
        EasyPost["EasyPost\nUSPS Rates"]
    end

    subgraph PerchStack["Perch (sentiment_importer)"]
        Rails["Rails (Puma)\n:3000"]
        SK["Sidekiq Workers\nASG × 2"]
        PG["PostgreSQL\nseni_sql_2026"]
        RD["Redis\nseni_redis_2"]
    end

    subgraph EdgarStack["Edgar (dao_protocol / Python)"]
        FastAPI["FastAPI\n:8010"]
    end

    Nginx["krake_nginx"] -->|POST /dao/submit_contribution| FastAPI

    Rails -->|reads/writes| PG
    Rails -->|Sidekiq queue| RD
    SK -->|reads jobs| RD
    SK -->|WebhookTriggerWorker| GAS
    SK -->|InventorySnapshotWorker| GAS
    SK -->|DaoMembersCacheWorker| GAS

    Rails -->|EasyPost API| EasyPost
    FastAPI -->|Stripe sync| Stripe
    FastAPI -->|GAS proxy| GAS

    style External fill:#2d2d2d,color:#fff,stroke:#888
    style PerchStack fill:#1a3a2e,color:#fff,stroke:#2ecc71
    style EdgarStack fill:#1a2a3e,color:#fff,stroke:#3498db
```

---

## 1. AWS Accounts

| Account | Label | Owner ID | Purpose |
|---------|-------|----------|---------|
| **Explorya** | `explorya` | `440626669078` | TrueSight DAO / Agroverse production. Contains the autopilot, old Perch instances (stopped), and Route53 DNS for `truesight.me`, `agroverse.shop`. |
| **Nelanco** | `nelanco` | `767697632458` | Krake / GetData.io production + **Perch** (Rails) + **Edgar** (dao_protocol Python). Contains the nginx reverse proxy, ALB, Sidekiq workers, Redis, PostgreSQL, and the new `dao_protocol` FastAPI server. |

**Key insight:** The old `seni_ror_2026` / `seni_sk_2026` instances in Explorya were **stopped 2026-05-28**. Perch was migrated to a fresh host in Nelanco. The autopilot remains in Explorya.

---

## 2. EC2 Instance Inventory

### 2.1 Nelanco Account (767697632458) — `us-east-1`

| Name | Instance ID | Type | State | Private IP | Public IP | Purpose |
|------|-------------|------|-------|------------|-----------|---------|
| **krake_nginx** | `i-05a041b6956aa7154` | t2.micro | running | 172.31.26.102 | 54.226.114.186 | **Nginx reverse proxy.** Terminates HTTPS for `edgar.truesight.me`, `api.truesight.me`, `chatbot.truesight.me`. Proxies to backend Rails/Python services. |
| **seni_ror_200250915** | `i-063dc4a3be90bd630` | t2.small | running | 172.31.19.78 | 54.211.179.126 | **Perch (Rails).** `sentiment_importer` — DAO API server. Receives signed event submissions, verifies signatures, logs to Google Sheets, dispatches GAS webhooks. DNS: `edgar.truesight.me` → this host (via nginx proxy). |
| **dao_protocol_nelanco** | `i-05f8770a932b76649` | t3.small | running | 172.31.23.207 | 98.93.94.86 | **Edgar FastAPI server.** Python port of the original submission + dispatch logic. Runs on port 8010. Accepts `POST /dao/submit_contribution`. |
| **dao-protocol-beta** | `i-0b8c6d989594fb229` | t3.small | running | 172.31.20.96 | 54.162.175.189 | **Beta sandbox dao_protocol.** Isolated test instance for Stripe test-mode subscription E2E tests. systemd `dao-protocol-beta.service`, port 8010. DNS: `beta.edgar.truesight.me`. SG: `dao-protocol-beta-sg` (443 open, 22 restricted to autopilot). Keypair: `dao-protocol-beta-key`. |
| **seni_sk_auto** (ASG — 2 instances) | `i-0dfeb7a93f1f78e8e` / `i-09883a010a52509f6` | t2.small | running | 172.31.50.44 / 172.31.84.218 | 34.234.193.80 / 100.53.89.222 | **Sidekiq worker** for Perch (sentiment_importer). ASG-managed; deploy script targets `100.53.89.222` as `seni_sk_nelanco`. Processes background jobs (webhook triggers, inventory snapshots). |
| **krake_ror** | `i-0df7a9e513dc537a6` | t2.micro | running | 172.31.19.151 | 18.205.20.43 | Krake Rails backend (getdata.io). Behind ALB `krake-ror-1`. |
| **krake_sk_consolidated** | `i-09d97cc0780fc8363` | t2.small | running | 172.31.48.178 | 54.160.89.135 | **Consolidated Krake Sidekiq.** Runs 4 Sidekiq processes (general, webhook, crawler, scaler) on one box. Replaces 4 separate krake_sk* instances. Upstart scripts at `/etc/init/krake_sk*.conf`. |
| ~~krake_sk~~ | ~~i-0b82138aa45b4029a~~ | ~~t2.nano~~ | **stopped** | — | — | Replaced by krake_sk_consolidated. |
| ~~krake_sk_webhook~~ | ~~i-02599e3b3a03e38e4~~ | ~~t2.small~~ | **stopped** | — | — | Replaced by krake_sk_consolidated. |
| ~~krake_sk_crawler~~ | ~~i-06fc0dd44fa9cdbf2~~ | ~~t2.small~~ | **stopped** | — | — | Replaced by krake_sk_consolidated. |
| ~~krake_sk_scaler~~ | ~~i-03224db5f5a49709c~~ | ~~t2.micro~~ | **stopped** | — | — | Replaced by krake_sk_consolidated. |
| **krake_data** | `i-07c76510b231d787f` | t3.medium | running | 172.31.19.2 | 52.5.179.48 | Krake data processing. |
| **GETDATA_REDIS** | `i-030c1452b197c920a` | t3a.small | running | 172.31.19.183 | 52.1.162.134 | Redis for Krake. |
| **GETDATA_CACHE** | `i-0d63b472d8a8893f8` | t2.micro | running | 172.31.19.80 | 98.84.169.188 | Krake cache worker. |
| **seni_sql_2026** | `i-08ebe96afbc649a95` | t2.small | running | 172.31.20.143 | 44.193.55.205 | PostgreSQL database for Perch (sentiment_importer). |
| **seni_redis_2** | `i-09ecc8ecc91d09206` | t2.large | running | 172.31.56.185 | 54.234.59.188 | Redis for Perch (Sidekiq, caching). |

### 2.2 Explorya Account (440626669078) — `us-east-1`

| Name | Instance ID | Type | State | Private IP | Public IP | Purpose |
|------|-------------|------|-------|------------|-----------|---------|
| ~~**truesight-autopilot**~~ | `i-02c699d3d7efbdc82` | t3.medium | **STOPPED 2026-07-15** | 10.0.0.158 | 52.200.38.206 | **RETIRED — migrated to Nelanco** (`i-05276b8ae82d6b88c`, EIP `3.214.167.219`). Kept stopped for rollback. See top banner. |
| **seni_ror_2026** | `i-0ac8462aa6bb54986` | t2.small | **stopped** | 10.0.0.162 | — | **Old Perch (Rails).** Stopped 2026-05-28. Replaced by `seni_ror_200250915` in Nelanco. |
| **seni_sk_2026** | `i-0bb43299c84c5ccd5` | t2.small | **stopped** | 10.0.0.14 | — | **Old Sidekiq.** Stopped 2026-05-28. Replaced by new `seni_sk_auto` in Nelanco. |

---

## 3. DNS & Traffic Routing

### 3.1 Route53 — `truesight.me` Zone (Explorya)

| Record | Type | Target | Notes |
|--------|------|--------|-------|
| `edgar.truesight.me` | A | `54.226.114.186` | Points to **krake_nginx** (Nelanco). Currently proxies to `seni_ror_200250915` (Rails Perch, port 3002). Will be repointed to the Python Edgar server (`dao_protocol_nelanco`, port 8010). |
| `perch.truesight.me` | A | `54.226.114.186` | Points to **krake_nginx** (Nelanco). Proxies to `seni_ror_200250915` (Rails Perch, port 3002). Canonical domain for the Rails `sentiment_importer` (Perch, formerly called "Edgar"). |
| `beta.edgar.truesight.me` | A | `54.162.175.189` | Points directly to **dao-protocol-beta** (Nelanco). Standalone beta sandbox for Stripe test-mode E2E tests. |
| `api.truesight.me` | A | `54.226.114.186` | Also krake_nginx. |
| `chatbot.truesight.me` | A | `54.226.114.186` | Also krake_nginx. Proxies to `seni_ror_200250915:8000` (governor chatbot / autopilot). |
| `sophia.truesight.me` | A | `3.214.167.219` | → **truesight-autopilot in Nelanco** (`i-05276b8ae82d6b88c`); was `52.200.38.206` (Explorya) until the 2026-07-15 migration. |
| `claude.truesight.me` | A | `100.57.50.48` | → **nelanco-claude** interactive Claude Code box (`i-01ad5eca707e4445f`, Nelanco). Added 2026-07-14. |
| `dapp.truesight.me` | CNAME | `truesightdao.github.io` | GitHub Pages. |
| `beta.dapp.truesight.me` | CNAME | `truesightdao.github.io` | GitHub Pages (beta). |
| `truesight.me` | A | `185.199.108.153` + 3 more | GitHub Pages. |
| `www.truesight.me` | CNAME | `TrueSightDAO.github.io` | GitHub Pages. |
| `agroverse.shop` | — | (separate zone) | Route53 zone `Z03648011LL9LLYA2X5F5` in Explorya. |

### 3.2 Traffic Flow

```
Internet → Route53 → krake_nginx (54.226.114.186)
  ├── edgar.truesight.me/ → seni_ror_200250915:3002 (Rails Perch)
  ├── perch.truesight.me/  → seni_ror_200250915:3002 (Rails Perch)
  ├── api.truesight.me/   → redirects to GAS QR checking
  └── chatbot.truesight.me/ → seni_ror_200250915:8000 (governor chatbot)

Internet → Route53 → sophia.truesight.me → truesight-autopilot (52.200.38.206:8000)

Internet → Route53 → GitHub Pages
  ├── truesight.me
  ├── dapp.truesight.me
  └── agroverse.shop
```

### 3.3 Nginx (krake_nginx)

The nginx reverse proxy on `krake_nginx` (54.226.114.186) terminates HTTPS and routes:

| Domain | Upstream | Target | Port |
|--------|----------|--------|------|
| `edgar.truesight.me` | `trends_server` | `seni_ror_200250915` (Rails Perch) | 3002 |
| `perch.truesight.me` | `trends_server` | `seni_ror_200250915` (Rails Perch) | 3002 |
| `chatbot.truesight.me` | `governor_chatbot` | `100.52.234.163` (old autopilot) | 8001 |
| `api.truesight.me` | — | Redirects to GAS QR checking | — |
| `truesight.me` | `shadi_server` | `50.87.178.128` (deprecated) | 80 |

**Config:** `/etc/nginx/sites-enabled/nginx_krake_ng.conf` on `krake_nginx`.

**Key upstream definitions:**
- `trends_server` = `54.211.179.126:3002` → `seni_ror_200250915` (Rails Perch/sentiment_importer)
- `governor_chatbot` = `100.52.234.163:8001` → old autopilot IP (⚠️ needs updating to `52.200.38.206`)
- `edgar` = `18.232.199.204:8081` → `edgar.getdata.io` (Krake legacy)

**SSL certs** live at `/home/ubuntu/ssl_certs/`:
- `truesight_edgar.key` + `edgar_truesight_me_combined.crt`
- `perch_truesight.key` + `perch_truesight_me_combined.crt`
- `chatbot_truesight.key` + `chatbot_truesight_me_combined.crt`
- `STAR_truesight_me.crt` + `truesight.key`
- `STAR_getdata_io_combined.crt` + `getdata_io.key`

**Domain routing notes:**
- Both `edgar.truesight.me` and `perch.truesight.me` currently share the same `trends_server` upstream (Rails Perch). The plan is to eventually repoint `edgar.truesight.me` to the Python `dao_protocol` server on `98.93.94.86:8010`.
- `chatbot.truesight.me` points to old autopilot IP `100.52.234.163` — should be updated to the current EIP `52.200.38.206`.
- `truesight.me` points to `shadi_server` (50.87.178.128) which appears deprecated/offline.
- `api.truesight.me` does not proxy — it redirects (302) to the GAS QR checking script.

The ALB `krake-ror-1` handles `getdata.io` traffic to the Krake Rails app (port 3002).

---

## 4. Service Architecture

### 4.1 Perch (DAO API) — `sentiment_importer`

```
krake_nginx (54.226.114.186:443)
  └── seni_ror_200250915 (54.211.179.126:3002) — Rails (Puma)
        ├── seni_sql_2026 (44.193.55.205) — PostgreSQL
        ├── seni_redis_2 (54.234.59.188) — Redis (Sidekiq, cache)
        └── seni_sk_auto (34.234.193.80) — Sidekiq workers
              └── WebhookTriggerWorker → GAS webhooks
              └── AgroverseInventorySnapshotPublishWorker → GAS
              └── DaoMembersCacheRefreshWorker → GAS
```

**Key endpoints:**
- `POST /dao/submit_contribution` — signed event intake (multipart form)
- `POST /dao/express_submit_contribution` — invoice/UPC workflow
- `GET /dao/check_digital_signature` — public key lookup
- `GET /agroverse_shop/shipping_rates` — USPS rates via EasyPost
- `GET /newsletter/open.gif` — email open tracking pixel
- `GET /newsletter/click` — email click tracking redirect
- `GET /proxy/gas/<name>` — GAS proxy for regions blocking script.google.com

### 4.2 Edgar (FastAPI) — Python Port

```
dao_protocol_nelanco (98.93.94.86:8010)
  └── POST /dao/submit_contribution — canonical DAO event intake (replaces Rails Perch route)
  └── GET /healthz — health check
  └── GET /proxy/gas/<name> — GAS proxy
  └── GET /agroverse_shop/shipping_rates — USPS rates
  └── GET /qr-code-check — QR code lookup
  └── POST /stripe/order-sync — Stripe order sync
```

The `dao_protocol` server is a **Python port** of Perch's core submission + dispatch logic. It runs independently and can accept submissions. Currently both Perch (Rails) and `dao_protocol` are live, but `edgar.truesight.me` DNS still points to the Rails instance via nginx.

### 4.3 Autopilot (Governor Chat + SRE)

```
truesight-autopilot (52.200.38.206:8000)
  └── POST /chat — governor chat (RSA-signed or JWT)
  └── POST /fix — autonomous fix PR agent
  └── GET /health — health check
  └── Background: Gmail poller, AWS monitor
```

Runs on a **dedicated EC2** separate from Perch (Rails) to protect critical infrastructure. Code at `/opt/truesight_autopilot`, systemd service `truesight-autopilot.service`.

**Telegram identifiers (Sophia):**
- Bot: **`@truesight_autopilot_bot`** (id `8217115914`).
- **Working group: `TrueSight DAO Ops` = `-1003919341801`** (forum/topics enabled; the bot is a **group admin with Manage Topics**). This is `TELEGRAM_HOME_GROUP_ID` in the box `.env` — where `create_telegram_topic` opens topics for execution handoffs triggered off-Telegram.
- Watchdog user-session = Gary's account `garyjob` (id `2102593402`) — read-only nudges (see §4.5 / OPEN_FOLLOWUPS).

**Execution-handoff path (local LLM → Sophia):** a governor crafts a plan + roadmap with a local LLM and commits the roadmap to `agentic_ai_context` (the baton), then runs **`truesight-dao-ping-sophia`** (`dao_client`/`dao_protocol` module `ping_sophia`, governor-signed → Sophia `/chat-blocking`, **governor-only, 403 otherwise**) telling Sophia to open a topic + load the plan + post a kickoff. Sophia uses the `create_telegram_topic` tool; the governor steps into that topic in `TrueSight DAO Ops` and monitors execution (one autopilot session per topic). Validated end-to-end 2026-06-07.

### 4.4 GitHub Pages (Static Sites)

| Site | Repo | Domain |
|------|------|--------|
| TrueSight DAO landing | `truesight_me_prod` | `truesight.me` |
| DApp | `dapp_prod` (fork of `dapp_beta`) | `dapp.truesight.me` |
| DApp (beta) | `dapp_beta` | `beta.dapp.truesight.me` |
| Agroverse Shop | `agroverse_shop_prod` | `agroverse.shop` |
| Capoeira practice | `capoeira` | `capoeira.agroverse.shop` |
| Tribo Mirim Bahia ledger | `tribomirimbahia` | `mirim-bahia.truesight.me` |
| Oracle | `oracle` | `oracle.truesight.me` |
| Butterfly Effect Club | `butterfly-effect-club` | `butterfly-effect-club.truesight.me` |

---

## 4.5 Autopilot (Sophia) Upgrade & Disaster Recovery — EIP blue-green + AMI

**The autopilot box has an Elastic IP** — `eipalloc-04772e4a20f10c1c4` (`52.200.38.206`) — and
`sophia.truesight.me` points to it. That stable EIP is the enabler: you can swap the underlying EC2 box
and **Route53 never changes**. Point Route53 at the EIP **once** (done); thereafter every upgrade/replace
is just "move the EIP."

### Replace / upgrade the box (blue-green, near-zero downtime, rollback-able)
1. Have a recent **AMI** of the current box (cadence below).
2. **Launch the new box** at the target size (e.g. `t3.medium`) from the latest AMI — or fresh Ubuntu 22.04 + `scripts/user-data.sh`.
3. On the new box: `git pull` + `scripts/deploy.sh` (AMIs are point-in-time — always pull latest code), restore `.env`, start services, **health-check** `:8001/health` + Telegram adapter + `dao_protocol :8010` + Monit `:2812`.
4. **Reassociate the EIP** to the new instance: `aws ec2 associate-address --allocation-id eipalloc-04772e4a20f10c1c4 --instance-id <new-id>` (Explorya creds, `us-east-1`). `sophia.truesight.me` flips instantly; **no Route53 edit needed.**
5. Verify, then **stop** (don't terminate) the old box for a few days as rollback; terminate once confident.
6. **Rollback** = reassociate the EIP back to the old instance.

> The Telegram adapter is **outbound-polling**, so it doesn't depend on the inbound IP — the EIP matters for SSH, the web API (`:8001`/`:443`), Monit, and `sophia.truesight.me`.

### AMI backup cadence (DR + source for step 2)
- **Weekly AMI — AUTOMATED 2026-06-07** via GitHub Action **`Cypher-Defense/.github/workflows/snapshot_autopilot_ami.yml`** (Sundays 03:00 UTC + `workflow_dispatch`), script **`scripts/aws/snapshot_autopilot_ami.py`**. Resolves the instance by **Name tag `truesight-autopilot`** (not a hardcoded ID — survives resizes / blue-green), `create-image --no-reboot`, tags AMI + snapshots `ManagedBy=snapshot_autopilot_ami`, **retains newest 8 (~2 months)** and prunes older AMIs + their backing snapshots. Repo secrets `TRUESIGHT_DAO_AUTOPILOT_AWS_KEY/SECRET` (account that owns the instance). First validated run: `ami-0dae91c5216989753`.
- ⚠️ The AMI contains the on-disk **`.env` (secrets)** → keep it **private** (default in-account); never share cross-account/publicly.
- AMI ≠ latest code — a new box still runs `deploy.sh` to pull current code.

### Known issues this addresses / to watch
- **Deploy OOM (2026-06-06):** `pip install dao_client` was OOM-killed (SIGTERM) on the 2 GB box (it runs two services). Immediate fix: **t3.medium (4 GB) + 2 GB swap** (Sophia's `infrastructure/autopilot_upgrade_proposal_2026-06-06.pdf`). Since the EIP exists, do it **blue-green** (launch t3.medium from AMI → deploy → reassociate EIP) for zero downtime + rollback, not an in-place resize. Also consider lightening deploy memory (prebuilt wheels / `pip --no-cache-dir`).
- **dao_protocol is NOT on this box** (verified 2026-06-06 — no `:8010` listener). It runs on `dao_protocol_nelanco` (Nelanco, `98.93.94.86`). The proposal's "two services / co-located" claim was wrong — the autopilot box is single-service (autopilot + telegram + watchdog).
- **Self-deploy restarts all units** as of `truesight_autopilot#107` (main + telegram + watchdog); a fresh box must run the same `deploy.sh`.

### Post-cutover verification — run on EVERY resize / new box / EC2 event
After a stop/start resize, an EIP reassociate, or a fresh box, confirm before walking away (the units auto-start on boot, but given session-duplication stakes, verify explicitly):
- [ ] `describe-instances` → expected `InstanceType`, `State=running`
- [ ] `ssh sophia` reachable on the EIP (`52.200.38.206`)
- [ ] **All three units active:** `systemctl is-active truesight-autopilot truesight-autopilot-telegram truesight-autopilot-watchdog` → all `active`. **Confirm the watchdog especially** — it must reconnect cleanly.
- [ ] `free -m` shows expected RAM; `swapon --show` shows the 2 GB swap (re-add on a fresh box)
- [ ] `curl localhost:8001/health` → `status: ok` (give the heavy app ~10–20 s after a restart)
- [ ] Monit `:2812` listening
- [ ] `git pull` to current `main` + restart all units (AMIs / stopped boxes lag the repo)

### Status
- **2026-06-06:** resized in-place **t3.small → t3.medium** (4 GB) + **2 GB swap**; all units (incl. watchdog) verified active; box pulled to current `main` (incl. PDF house style). Pre-resize backup AMI `ami-0e1f8559e760c5fd9`. EIP held → no Route53 change.
- **2026-06-07:** weekly-AMI TODO **DONE** — automated via the Cypher-Defense GitHub Action above (first AMI `ami-0dae91c5216989753`). Also shipped (`truesight_autopilot#114`): Sophia can now run sudo / install packages on her **own** box via `ssh_run(host='autopilot', …)` (loopback self-host; `sophia_infra.pub` self-trusted in the box's own `authorized_keys` by `deploy.sh`); the system prompt embeds a live **host-identity block** (instance id/type/region via IMDS) so she stops hallucinating her location; `GROK_API_KEY` added to the box `.env` (`/health` → `grok_key_set: true`).

---

## 5. Perch Migration (2026-05-28)

The old Perch infrastructure in the **Explorya** account was **stopped** on 2026-05-28:

| Old (Explorya — stopped) | New (Nelanco — running) |
|--------------------------|--------------------------|
| `seni_ror_2026` (t2.small) | `seni_ror_200250915` (t2.small) |
| `seni_sk_2026` (t2.small) | `seni_sk_auto` (t2.small, new ASG) |
| — | `dao_protocol_nelanco` (t3.small, new) |

The DNS `edgar.truesight.me` was updated to point to `krake_nginx` (54.226.114.186), which proxies to the new Rails host.

---

## 6. Key Configuration Files

### 6.1 Perch (sentiment_importer)

- **`config/application.rb`** — All webhook URLs, API keys, secrets
- **`config/tsd_configuration.rb`** — DAO-specific configuration
- **`deploy.sh`** — Deploy script (pre-compiles assets, migrates DB, restarts systemd)
- **`app/controllers/dao_controller.rb`** — Main submission + dispatch logic
- **`app/services/dao_email_registration_service.rb`** — Email verification flow
- **`app/workers/webhook_trigger_worker.rb`** — GAS webhook dispatcher

### 6.2 dao_protocol

- **`truesight_dao_client/server/dispatch.py`** — Event dispatch routing (port of Rails `trigger_immediate_processing`)
- **`truesight_dao_client/server/routes/dao.py`** — `POST /dao/submit_contribution` handler
- **`truesight_dao_client/server/jobs/webhook_trigger.py`** — GAS webhook HTTP client
- **`.env`** — Server-side env vars (webhook URLs, secrets)

### 6.3 Autopilot

- **`app/main.py`** — FastAPI app
- **`app/fix_agent.py`** — Autonomous fix PR agent
- **`app/email_poller.py`** — Gmail monitoring
- **`app/aws_monitor.py`** — AWS CloudWatch/Cost monitoring
- **`scripts/deploy.sh`** — Deploy to EC2

---

## 7. SSH Access

| Host | SSH Alias | Key | User |
|------|-----------|-----|------|
| krake_nginx | `krake_nginx` | `GETDATA_IO_PAIR_20201122` | ubuntu |
| seni_ror_200250915 | `seni_ror` | `GETDATA_IO_PAIR_20201122` | ubuntu |
| dao_protocol_nelanco | — | `GETDATA_IO_PAIR_20201122` | ubuntu |
| dao-protocol-beta | — | `dao-protocol-beta-key` (ed25519, on autopilot) | ubuntu |
| seni_sk_auto | `seni_sk` | `GETDATA_IO_PAIR_20201122` | ubuntu |
| seni_sql_2026 | `seni_sql` | `GETDATA_IO_PAIR_20201122` | ubuntu |
| seni_redis_2 | — | `GETDATA_IO_PAIR_20201122` | ubuntu |
| truesight-autopilot | — | `garyjob_aws` | ubuntu |

### 7.1 Reaching Nelanco hosts from a non-allowlisted network — **bastion via Sophia**

**Symptom:** `ssh ubuntu@54.211.179.126` (or any Nelanco host) **times out** from a
laptop / phone-hotspot / café network, even though the key is correct.

**Why:** the Nelanco Security Group allowlists inbound SSH (22) and ICMP to a short
list of source IPs — it is *allow-only*, so any source not on the list is **silently
dropped** (hence *timeout*, not *connection refused*). The **autopilot/Sophia Elastic
IP `52.200.38.206` is on that allowlist**; arbitrary dynamic IPs (e.g. T-Mobile
cellular) are not. This is cross-account (Explorya ↔ Nelanco) over the public
internet, so gating is purely source-IP based — there is no VPC peering.

**Fix — use Sophia as a ProxyJump bastion** (the TCP hop to the target then
originates from `52.200.38.206`, which *is* allowlisted; auth to the target still
uses your **local** Nelanco key):

```bash
KEY=~/Applications/aws_keypairs/NELANCO_aws_20201122.pem
ssh -J sophia -i "$KEY" ubuntu@54.211.179.126   # Perch (seni_ror, sentiment_importer)
ssh -J sophia -i "$KEY" ubuntu@98.93.94.86       # Edgar (dao_protocol FastAPI + DAO secrets)
```

`sophia` is a working `~/.ssh/config` alias (`HostName sophia.truesight.me`). This is
the **standard, durable way** for any operator / LLM to reach the Nelanco boxes — do
**not** widen the SG to `0.0.0.0/0` to avoid it (these are treasury-grade hosts; see §9).

**Secrets stay on the box.** The GAS web apps are public (`ANYONE_ANONYMOUS`); only the
shared secret is gated. DAO secrets (e.g. `DAO_PROTOCOL_EMAIL_VERIFICATION_GAS_SECRET`,
`..._WEBHOOK_URL`) live in `~/dao_protocol/.env` on the dao_protocol box. Run any
secret-bearing call **from that box** (`set -a; . ~/dao_protocol/.env; set +a; curl …`)
so the secret never lands in a local shell history or transcript. Example — force a
`dao_members.json` cache refresh:

```bash
ssh -J sophia -i "$KEY" ubuntu@98.93.94.86 \
  'set -a; . ~/dao_protocol/.env; set +a;
   curl -s "${DAO_PROTOCOL_EMAIL_VERIFICATION_GAS_WEBHOOK_URL}?action=refresh_dao_members_cache&secret=${DAO_PROTOCOL_EMAIL_VERIFICATION_GAS_SECRET}&force=1"'
```

### 7.2 SSH Keys on the Autopilot Box (Sophia @ sophia.truesight.me)

Sophia's `~/.ssh/` holds all fleet SSH keys. PEM keys are staged at `/home/ubuntu/`
(AMI-survivable, outside `/opt/truesight_autopilot/`). Future blue-green rebuilds:
copy from `/home/ubuntu/` to `~/.ssh/` if missing. `~/.ssh/config` maps each host
alias to the correct key via `IdentityFile`.

| Key file | Type | Covers | Host aliases |
|----------|------|--------|-------------|
| `id_ed25519_truesight_autopilot` | ed25519 | DAO fleet | `krake-nginx`, `seni-ror`, `dao-protocol`, `seni-sk`, `seni-sql`, `seni-redis` |
| `NELANCO_aws_20201122.pem` | RSA (PEM) | Krake/Seni fleet (16 hosts) | `krake_redis`, `krake_sk`, `krake_sk_2`, `krake_sk_3`, `krake_sk_crawler`, `krake_crawler`, `krake_sk_webhook`, `krake_scaler`, `krake_ng`, `seni_ror_nelanco`, `seni_redis`, `seni_redis_2`, `seni_data`, `seni_sk`, `seni_sk_nelanco`, `dao_protocol_nelanco` |
| `server_us.pem` | RSA (PEM) | Krake core hosts (3 hosts) | `krake_ror`, `krake_data`, `krake_data_2` |
| `NELANCO_california_20260213.pem` | RSA (PEM) | California proxy (1 host) | `californian_proxy` |

**Verification:** After key provisioning, test one host per key:
```bash
ssh -i ~/.ssh/NELANCO_aws_20201122.pem -o StrictHostKeyChecking=no ubuntu@krake_ng -p 2202 hostname
ssh -i ~/.ssh/server_us.pem -o StrictHostKeyChecking=no ubuntu@krake_ror hostname
ssh -i ~/.ssh/NELANCO_california_20260213.pem -o StrictHostKeyChecking=no ubuntu@californian_proxy hostname
```

**On AMI-based rebuild:** `/home/ubuntu/` is captured by the weekly AMI snapshot
(`Cypher-Defense/.github/workflows/snapshot_autopilot_ami.yml`). After launching
from AMI, ensure `~/.ssh/config` references all keys and test connectivity.
`deploy.sh` does NOT wipe `/home/ubuntu/`.

---

## 8. Monitoring

| Service | URL |
|---------|-----|
| Perch health | `https://edgar.truesight.me/ping` |
| Edgar (dao_protocol) health | `http://98.93.94.86:8010/healthz` |
| Beta Edgar health | `https://beta.edgar.truesight.me/ping` |
| Autopilot health | `http://52.200.38.206:8000/health` |
| Governor chatbot | `https://chatbot.truesight.me` |
| Monit (Rails) | `http://54.211.179.126:2812/seni_ror` |
| Monit (Sidekiq) | `http://3.83.175.151:2812/sidekiq` (old — verify) |

---

## 9. Security Groups

| Group | Name | Used By |
|-------|------|---------|
| `sg-4314630c` | `default` (Nelanco) | All Nelanco instances. Allows SSH, HTTP/HTTPS, internal traffic. |
| `sg-e98f788e` | `default` (Explorya) | Autopilot. |
| `sg-093be54e48c6478e8` | `edgar-2026-05-10` | Old Perch instances (stopped). |

> **SSH/ICMP are source-IP allowlisted, not open.** The Sophia/autopilot EIP
> `52.200.38.206` is allowlisted; random operator IPs are not — reach these hosts via
> the **Sophia bastion** (§7.1), not by widening the SG. The crown-jewel host is
> **`dao_protocol`** (`98.93.94.86`) — it holds the DAO submit/dispatch logic and the
> GAS/Stripe/webhook secrets in `~/dao_protocol/.env`; Perch/`seni_ror` runs only the
> `sentiment_importer` Rails app. Do **not** expose either to `0.0.0.0/0`; prefer SSM
> Session Manager if direct access is ever needed.

---

## 10. Common Pitfalls

1. **Perch is NOT `getdata.io`.** `perch.truesight.me` = `sentiment_importer` (Rails trading platform). `edgar.truesight.me` = `dao_protocol` (Python/FastAPI — the canonical DAO API). `getdata.io` = `krake_ror` (different codebase, different server). Do not conflate.

2. **Service topology:** `POST /dao/submit_contribution` is handled exclusively by the Python `dao_protocol` server. The nginx flip was completed in PR8a (2026-06-07) — `edgar.truesight.me` DNS → `seni_ror_new` nginx → `dao_protocol_nelanco:8010`. The Rails Perch (`sentiment_importer`) no longer handles DAO submissions. Legacy `dao_controller.rb` actions still exist in the Rails codebase but are dead code (scheduled for deletion in PR8d).

3. **Old Perch instances are stopped.** `seni_ror_2026` and `seni_sk_2026` in Explorya were stopped 2026-05-28. Do not try to SSH into them or deploy to them.

4. **Nginx routing:** `edgar.truesight.me` → DNS to `seni_ror_new` (3.90.179.151) → local nginx → `/dao/*` routes go to `dao_protocol_nelanco:8010`, trading routes go to `127.0.0.1:3002` (Rails). The nginx config is on `seni_ror_new`, NOT krake_nginx.

5. **Webhook URLs are env-configured.** The `dao_protocol` server reads webhook URLs from `DAO_PROTOCOL_WEBHOOK_*` env vars. The Rails Perch reads from `config/application.rb`. They are independent — a change to one does not affect the other.

---

## 11. Deployment Guide — How Each Service Ships

This section documents how each service is deployed. Use this when setting up a new box, recovering from failure, or onboarding a new operator.

### 11.1 Perch (sentiment_importer — Rails)

| Aspect | Detail |
|--------|--------|
| **Host** | `seni_ror_200250915` (54.211.179.126) |
| **Code** | `TrueSightDAO/sentiment_importer` |
| **Deploy** | `deploy.sh` on the box — `git pull`, `bundle install`, `rake assets:precompile`, `rake db:migrate`, `sudo service puma restart` |
| **Process** | Puma (Rails) on port 3000, behind nginx on krake_nginx |
| **Sidekiq** | `seni_sk_auto` ASG (2 instances). Deploy via `capistrano` or manual `git pull + bundle exec sidekiq -C config/sidekiq.yml` |
| **DB** | PostgreSQL on `seni_sql_2026` (44.193.55.205) |
| **Redis** | `seni_redis_2` (54.234.59.188) |
| **Env vars** | `config/application.rb` + `config/tsd_configuration.rb` |
| **Health** | `https://edgar.truesight.me/ping` |

### 11.2 Edgar (dao_protocol) (FastAPI — Python)

| Aspect | Detail |
|--------|--------|
| **Host** | `dao_protocol_nelanco` (98.93.94.86) |
| **Code** | `TrueSightDAO/dao_client` (server lives in `truesight_dao_client/server/`) |
| **Deploy** | `deploy.sh` on the box — `git pull`, `pip install -r requirements.txt`, `sudo systemctl restart truesight-dao-protocol` |
| **Process** | systemd `truesight-dao-protocol.service`, port 8010 |
| **Env vars** | `~/dao_protocol/.env` (chmod 600) — GAS webhook URLs, Stripe keys, Google SA keys |
| **Health** | `http://98.93.94.86:8010/healthz` |
| **Beta sandbox** | `dao-protocol-beta` (54.162.175.189), systemd `dao-protocol-beta.service`, same deploy pattern |

### 11.3 Autopilot (Sophia — FastAPI)

| Aspect | Detail |
|--------|--------|
| **Host** | `truesight-autopilot` (52.200.38.206 — EIP) |
| **Code** | `TrueSightDAO/truesight_autopilot` |
| **Deploy** | `scripts/deploy.sh` on the box — `git pull`, `pip install -r requirements.txt`, restarts 3 systemd units: `truesight-autopilot`, `truesight-autopilot-telegram`, `truesight-autopilot-watchdog` |
| **Processes** | 3 systemd units (main API, Telegram adapter, Telegram watchdog) |
| **Env vars** | `/opt/truesight_autopilot/.env` — LLM API keys, AWS creds, Telegram tokens, Gmail OAuth |
| **Health** | `http://52.200.38.206:8000/health` |
| **AMI backup** | Weekly automated via Cypher-Defense GitHub Action (Sundays 03:00 UTC). Retains newest 8. |
| **Blue-green** | EIP-based: launch new box from AMI → deploy → reassociate EIP. No DNS change. |

### 11.4 Krake (getdata.io — Rails + Sidekiq)

| Aspect | Detail |
|--------|--------|
| **Rails host** | `krake_ror` (18.205.20.43) — ASG-managed, behind ALB `krake-ror-1` |
| **Sidekiq host** | `krake_sk_consolidated` (54.237.53.162) — ASG-managed, auto-heals |
| **Code** | `KrakeIO/krake_ror` (private) |
| **Sidekiq processes** | 5 Upstart scripts on consolidated box:
  - `/etc/init/krake_sk.conf` — general queues (`config/sidekiq.yml`)
  - `/etc/init/krake_sk_webhook.conf` — webhook queues (`config/sidekiq_webhook.yml`)
  - `/etc/init/krake_sk_crawler.conf` — crawler queues (`config/sidekiq_crawler.yml`)
  - `/etc/init/krake_sk_scaler.conf` — scaler queues (`config/sidekiq_scaler.yml`)
  - `/etc/init/krake_publisher.conf` — s3_cacher queue (`config/sidekiq_s3_cacher.yml`) |
| **Deploy** | `git pull` on the box → `bundle install` → `sudo restart krake_sk` (and siblings) |
| **Redis** | `GETDATA_REDIS` (52.1.162.134) — shared across all 5 Sidekiq processes |
| **Monit** | `/etc/monit/conf.d/krake_sk.conf` — monitors all 5 processes, restarts on failure or >65% memory |
| **AMI** | `ami-046aefdade31fd70a` (`krake-sk-consolidated-2026-06-21`) — created from the consolidated box after setup |
| **ASG** | `krake_sk_consolidated` — Min=1, Max=1, Desired=1. Launch template `krake-sk-consolidated` (t2.small). Auto-heals on instance failure. |

**To deploy a code change to Krake Sidekiq:**
1. SSH to the consolidated box: `ssh -J sophia -i "$KEY" ubuntu@54.237.53.162`
2. `cd /home/ubuntu/krake_ror && git pull && bundle install`
3. `sudo restart krake_sk && sudo restart krake_sk_webhook && sudo restart krake_sk_crawler && sudo restart krake_sk_scaler`
4. If krake_publisher changed: `cd /home/ubuntu/krake_publisher && git pull && bundle install && sudo restart krake_publisher`

### 11.5 GitHub Pages (Static Sites)

| Aspect | Detail |
|--------|--------|
| **Deploy** | Push to `main` on the beta repo → GitHub Pages auto-deploys. For prod: `sync_beta_to_prod` (fork sync, never force). |
| **Beta-first flow** | All changes go to `*_beta` repos first. After review, promote to `*_prod` via `sync_beta_to_prod`. |
| **Key repos** | `truesight_me_beta` → `truesight_me_prod`, `dapp_beta` → `dapp_prod`, `agroverse_shop_beta` → `agroverse_shop_prod` |
| **CNAMEs** | Beta and prod repos have different CNAME files — `sync_beta_to_prod` is a non-force merge-upstream to preserve this. |

### 11.6 Security Dashboard

| Aspect | Detail |
|--------|--------|
| **Code** | `TrueSightDAO/Cypher-Defense` |
| **Scanner** | `scripts/security_scan/compile_security_report.py` — runs 4 sub-scanners (AWS, web, GitHub, phishing) |
| **Schedule** | Daily at 06:00 UTC via GitHub Action `.github/workflows/security-dashboard-daily.yml` |
| **Output** | Published to `TrueSightDAO/treasury-cache/managed-ledgers/security-dashboard.json` |
| **Frontend** | `truesight.me/security-dashboard/` — static page reads the JSON from treasury-cache |
| **AWS discovery** | Fully dynamic — uses `boto3 describe_instances()` across all regions. No hardcoded instance IDs. New boxes appear automatically. |
| **Credentials** | GitHub Actions secrets `CYPHER_DEFENCE_AWS_KEY/SECRET` (Nelanco) + `TRUESIGHT_DAO_AUTOPILOT_AWS_KEY/SECRET` (Explorya). Currently using broad keys — should be scoped to read-only (see OPEN_FOLLOWUPS.md). |

### 11.7 Krake Publisher (GETDATA_CACHE)

| Aspect | Detail |
|--------|--------|
| **Host** | Consolidated onto `krake_sk_consolidated` (54.237.53.162) |
| **Code** | `KrakeIO/krake_publisher` (private) |
| **Process** | Upstart `/etc/init/krake_publisher.conf` — runs `bundle exec sidekiq -e production -C config/sidekiq_s3_cacher.yml` |
| **Env vars** | In `/home/ubuntu/.profile`: `AWS_S3_BUCKET=cache.getdata.io`, `KRAKE_REDIS_HOST=redis.getdata.io`, etc. |
| **Deploy** | `cd /home/ubuntu/krake_publisher && git pull && bundle install && sudo restart krake_publisher` |
| **Monit** | Monitored alongside the 4 krake_sk processes in `/etc/monit/conf.d/krake_sk.conf` |

---

## 12. Infrastructure Consolidation History

### 2026-06-11 — Krake SK + Publisher Consolidation

**Before (6 instances, ~$55/mo):**
- `krake_sk` (t2.nano) — general Sidekiq
- `krake_sk_webhook` (t2.small) — webhook Sidekiq
- `krake_sk_crawler` (t2.small) — crawler Sidekiq
- `krake_sk_scaler` (t2.micro) — scaler Sidekiq
- `GETDATA_CACHE` (t2.micro) — s3_cacher Sidekiq
- All managed by separate ASGs

**After (1 instance, ~$17/mo):**
- `krake_sk_consolidated` (t2.small) — all 5 Sidekiq processes on one box
- ASG-managed (auto-heals), AMI-backed
- Old ASGs disabled (Min=0, Max=0, Desired=0)
- Old instances terminated

**Savings: ~$38/mo**
