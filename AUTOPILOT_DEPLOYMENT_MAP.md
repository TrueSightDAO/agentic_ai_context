# TrueSight DAO Autopilot — Deployment Map

> **Purpose:** If this EC2 box dies, this document tells you how to spin up a
> replacement that functions identically. Last updated: 2026-06-09.

---

## 1. The Box

| Property | Value |
|---|---|
| **Instance ID** | `i-02c699d3d7efbdc82` |
| **Name tag** | `truesight-autopilot` |
| **Type** | `t3.medium` (2 vCPU, 4 GB RAM) |
| **AMI** | `ami-00403f401ee6a4b98` (Ubuntu 22.04) |
| **Disk** | 20 GB EBS (`vol-0159e886ea21577df`) — 72% full |
| **Swap** | 2 GB |
| **Region / AZ** | `us-east-1` / `us-east-1d` |
| **VPC / Subnet** | `vpc-3a79715f` / `subnet-44257d33` |
| **Private IP** | `10.0.0.158` |
| **Public IP** | `52.200.38.206` (Elastic — survives stop/start) |
| **Security Group** | `default` (`sg-e98f788e`) |
| **Key Pair** | `garyjob_aws` |
| **AWS Account** | `440626669078` (Explorya) |
| **IAM Role** | **None** — no instance profile attached |
| **Tags** | `Name=truesight-autopilot`, `Service=autopilot`, `Project=TrueSightDAO` |

---

## 2. Services Running

All services are **native systemd** — no Docker, no PM2, no Supervisor.

| Unit | What | Port | User |
|---|---|---|---|
| `truesight-autopilot.service` | Sophia FastAPI (2 uvicorn workers) | `8001` | `ubuntu` |
| `truesight-autopilot-telegram.service` | Telegram bot adapter | — | `ubuntu` |
| `truesight-autopilot-watchdog.service` | Attention watchdog (read-only nudges) | — | `ubuntu` |
| `nginx.service` | Reverse proxy → sophia.truesight.me | `80`/`443` | `root` |
| `ssh.service` | SSH access | `22` | `root` |
| `monit.service` | System monitoring | `2812` | `root` |

**Nginx config:** `/etc/nginx/sites-enabled/sophia` → proxies `sophia.truesight.me` → `127.0.0.1:8001`
with SSL via Let's Encrypt (certbot).

---

## 3. Code & Data Layout

| What | Path |
|---|---|
| **App code** | `/opt/truesight_autopilot/` (git clone of `TrueSightDAO/truesight_autopilot`) |
| **Python venv** | `/opt/truesight_autopilot/.venv/` |
| **Environment secrets** | `/opt/truesight_autopilot/.env` |
| **Google SA keys** | `/opt/truesight_autopilot/config/google/` (3 JSON files) |
| **Gmail OAuth tokens** | `/opt/truesight_autopilot/config/gmail/` (per-account JSON) |
| **Systemd unit files** | `/opt/truesight_autopilot/systemd/` (symlinked into `/etc/systemd/system/`) |
| **Nginx config** | `/opt/truesight_autopilot/config/nginx/` (symlinked into `/etc/nginx/sites-enabled/`) |
| **Telegram session** | `/opt/truesight_autopilot/.telethon_watchdog.session` |
| **GitHub PAT** | `/home/ubuntu/CYPHER_DEFENCE_OPS_PAT` |
| **Clasp tokens** | `/home/ubuntu/.clasprc*.json` |
| **SSH key** | `/home/ubuntu/.ssh/id_ed25519_truesight_autopilot` |
| **Nginx logs** | `/var/log/nginx/sophia_access.log` + `sophia_error.log` |
| **App logs** | `journalctl -u truesight-autopilot*` |

---

## 4. Installed Software

- **Python 3.10** (system) + venv with FastAPI, uvicorn, boto3, google-api-client, httpx
- **Node.js v20** + `@google/clasp` (global npm)
- **Tesseract OCR** (eng + osd language packs)
- **FFmpeg**
- **Nginx** + Let's Encrypt (certbot)
- **No Docker, no PM2, no Supervisor**

---

## 5. Fleet — SSH Targets

The autopilot connects to these hosts via `~/.ssh/config`:

| Alias | Real Host | Purpose |
|---|---|---|
| `krake-nginx` | `54.226.114.186:2202` | Nginx reverse proxy (Nelanco) |
| `seni-ror` | `54.211.179.126` | Edgar Rails API server |
| `dao-protocol` | `98.93.94.86` | dao_protocol FastAPI (port 8010) |
| `seni-sk` | `34.234.193.80` | Sidekiq worker for Edgar |
| `seni-sql` | `44.193.55.205` | PostgreSQL for Edgar |
| `seni-redis` | `54.234.59.188` | Redis for Edgar |

---

## 6. Credential Inventory & DR Status

| Credential | Location | Backed up? | Recovery method |
|---|---|---|---|
| `.env` (all API keys) | `/opt/truesight_autopilot/.env` | ❌ **Not backed up** | Must reconstruct from service dashboards |
| Google SA keys (3) | `config/google/*.json` | ✅ credential_vault | Restore from laptop backup |
| Gmail OAuth tokens | `config/gmail/*.json` | ✅ credential_vault | Restore from laptop backup |
| GitHub PAT | `/home/ubuntu/CYPHER_DEFENCE_OPS_PAT` | ❌ Regeneratable | GitHub Settings → Developer settings |
| SSH key | `~/.ssh/id_ed25519_truesight_autopilot` | ✅ credential_vault | Restore from laptop backup |
| Clasp tokens | `~/.clasprc*.json` | ✅ credential_vault | Restore from laptop backup |
| Telegram session | `.telethon_watchdog.session` | ❌ Must re-login | Run `scripts/telethon_login.py` interactively |
| SSL cert | `/etc/letsencrypt/live/sophia.truesight.me/` | ✅ Auto-renewed | certbot handles renewal |

---

## 7. Disaster Recovery — Spin Up a Replacement

Estimated time: **~45 min** (assuming `.env` values are available).

### Step 1: Launch EC2

```bash
# From AWS Console or CLI in us-east-1d:
# - AMI: Ubuntu 22.04 (ami-00403f401ee6a4b98 or latest)
# - Type: t3.medium
# - Disk: 20 GB gp3
# - Security Group: default (sg-e98f788e)
# - Key Pair: garyjob_aws
# - Tags: Name=truesight-autopilot, Service=autopilot, Project=TrueSightDAO
# - Subnet: subnet-44257d33 (us-east-1d)
# - Auto-assign Public IP: yes
# - Then associate the Elastic IP 52.200.38.206
```

### Step 2: Install Dependencies

```bash
sudo apt update && sudo apt install -y \
  python3 python3-pip python3-venv \
  nginx certbot \
  tesseract-ocr tesseract-ocr-eng tesseract-ocr-osd \
  ffmpeg nodejs npm

# Node.js v20 (Ubuntu 22.04 ships v12 — use nodesource)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g @google/clasp
```

### Step 3: Clone the Repo

```bash
sudo git clone https://github.com/TrueSightDAO/truesight_autopilot.git /opt/truesight_autopilot
sudo chown -R ubuntu:ubuntu /opt/truesight_autopilot
cd /opt/truesight_autopilot
```

### Step 4: Create Virtualenv & Install Python Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Recreate `.env`

**⚠️ This is the critical gap.** The `.env` file is NOT backed up anywhere.
You need to reconstruct it from:

| Variable | Source |
|---|---|
| `TRUESIGHT_DAO_AUTOPILOT` | GitHub Settings → Developer settings → Fine-grained PAT |
| `GMAIL_TOKEN_JSON` | GCP Console → APIs & Services → Credentials (OAuth) |
| `DEEPSEEK_API_KEY` | platform.deepseek.com |
| `TAVILY_API` | app.tavily.com |
| `GROK_API_KEY` | x.ai console |
| `PUBLIC_KEY` / `PRIVATE_KEY` | Edgar identity (generate with `truesight-dao-auth login`) |
| `AWS_ACCESS_KEY_ID_EXPLORYA` / `_SECRET` | AWS IAM Console (Explorya account) |
| `AWS_ACCESS_KEY_ID_NELANCO` / `_SECRET` | AWS IAM Console (Nelanco account) |
| `BUG_SNAG_API` | Bugsnag project settings |
| `JWT_SECRET` | Generate a random string |
| `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` | my.telegram.org → API Development Tools |
| `TELEGRAM_HOME_GROUP_ID` | Telegram group ID (numeric, starts with -100) |

Copy `.env.example` as a template:
```bash
cp .env.example .env
# Edit with all values
```

### Step 6: Restore Credential Files

From a laptop with `credential_vault`:

```bash
# Restore Google SA keys + Gmail tokens
# These are in credential_vault under:
#   ${WORKSPACE}/truesight_autopilot/config/
#
# Copy them to:
#   /opt/truesight_autopilot/config/google/
#   /opt/truesight_autopilot/config/gmail/

# Restore SSH key
#   ~/.ssh/id_ed25519_truesight_autopilot
#   ~/.ssh/config
```

### Step 7: Set Up Nginx + SSL

```bash
sudo ln -sf /opt/truesight_autopilot/config/nginx/sophia.conf /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/sophia /etc/nginx/sites-enabled/
sudo certbot --nginx -d sophia.truesight.me
sudo nginx -t && sudo systemctl reload nginx
```

### Step 8: Install Systemd Units

```bash
sudo cp /opt/truesight_autopilot/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now truesight-autopilot.service
sudo systemctl enable --now truesight-autopilot-telegram.service
sudo systemctl enable --now truesight-autopilot-watchdog.service
```

### Step 9: Run Telegram Login (Interactive)

```bash
cd /opt/truesight_autopilot
source .venv/bin/activate
python3 scripts/telethon_login.py
# Follow the prompts — you'll need the phone number + Telegram verification code
```

### Step 10: Verify

```bash
curl http://localhost:8001/health
# Should return 200 with service status

curl https://sophia.truesight.me/health
# Should return 200 (public endpoint)

sudo systemctl status truesight-autopilot*
# All three should show "active (running)"
```

---

## 8. The `.env` Gap — Why It Matters

The `.env` file on this box holds **all API keys and secrets** needed for the
autopilot to function. It is currently:

- ❌ **Not in `credential_vault`** (which only backs up laptop credentials)
- ❌ **Not in AWS Secrets Manager** (no instance profile exists)
- ❌ **Not in any password manager**

If this box dies without a recent `.env` backup, recovery requires manually
regenerating or looking up ~15 different secrets from 8 different service
dashboards — a 30–60 minute process that's error-prone.

**Recommended fix:** Add `/opt/truesight_autopilot/.env` to `credential_vault`'s
`MANIFEST.txt` (it already handles workspace-relative paths), or set up AWS
Secrets Manager with an instance profile. See `OPEN_FOLLOWUPS.md` for the
tracking entry.

---

## 9. Related Documents

- `agentic_ai_context/OPEN_FOLLOWUPS.md` — tracks the `.env` backup gap
- `credential_vault/README.md` — laptop credential DR runbook
- `truesight_autopilot/README.md` — app architecture
- `truesight_autopilot/.env.example` — template for all env vars
