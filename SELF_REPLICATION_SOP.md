# Self-Replication SOP: Spawning a New Autopilot Instance

**Status:** Ready — all pieces exist today
**Trigger:** Governor says *"Sophia, spawn a new instance for [name] on [host/server]"*

---

## 1. Overview

A governor can spawn a fresh incarnation of the TrueSight DAO Autopilot on any reachable server. The governor provides **3 non-negotiable credentials** (unique per instance). Sophia handles everything else: provisioning, cloning, identity registration, repo creation, service startup.

---

## 2. Prerequisites

### Governor provides (per new instance)

| Credential | Why | How to get |
|---|---|---|
| **LLM API Key** | Required for the new instance to reason and respond | DeepSeek, OpenAI, or any litellm-compatible provider |
| **GitHub PAT** | Required to read repos, open PRs, submit contributions | GitHub → Settings → Developer settings → Personal access tokens |
| **Telegram Bot Token** | Required to receive/send messages | Talk to @BotFather on Telegram |

### Sophia provides (from existing vault)

| Resource | Source |
|---|---|
| AWS keys (Nelanco or Explorya) | Already in vault |
| SSH keys for target server | Already in vault (or generated on the fly) |
| GitHub PAT (for repo creation) | Already in vault |
| Codebase (`truesight_autopilot`) | Public GitHub repo |
| Context repo starter templates | Forked from `agentic_ai_context` |

---

## 3. Step-by-Step

### Step 1: Provision the server

If no server is specified, Sophia provisions an EC2 instance:

```
aws ec2 run-instances
  --image-id ami-0abcdef1234567890  # Ubuntu 22.04 LTS
  --instance-type t3.medium
  --key-name <ssh-key>
  --security-group-ids <sg>
  --subnet-id <subnet>
```

If a server is specified (IP or hostname), verify SSH access first.

### Step 2: Register a DAO identity

```
register_identity(email="new-instance@truesight.me")
```

This generates an RSA-2048 keypair and registers it with Edgar. The identity is used for signing contributions and vault authentication.

### Step 3: Clone the codebase

```
git clone https://github.com/TrueSightDAO/truesight_autopilot.git
cd truesight_autopilot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Fork the context repo

Create a new repo under TrueSightDAO (or the governor's org) seeded with starter templates:

- `OPERATING_INSTRUCTIONS.md`
- `WORKSPACE_CONTEXT.md` (blank template)
- `PROJECT_INDEX.md` (blank template)
- `ATTENTION_SURFACES.md` (blank template)
- `OPEN_FOLLOWUPS.md` (empty)

### Step 5: Create an empty transcript repo

```
POST /org/repos
  name: <instance-name>_transcript
  description: "Session transcripts for [instance name]"
  private: true
```

### Step 6: Configure the instance

Write `.env` with:

```
# Point to the new context and transcript repos
CONTEXT_REPO=TrueSightDAO/<forked-context-repo>
TRANSCRIPT_REPO=TrueSightDAO/<transcript-repo>

# Vault encryption key (auto-generated)
VAULT_KEY=<generated>
```

### Step 7: Start the service

```
sudo systemctl start truesight-autopilot
sudo systemctl enable truesight-autopilot
```

### Step 8: Governor provisions credentials

The governor visits `https://<new-instance-url>/vault/` and adds the 3 non-negotiables:

1. LLM API Key → stored as `llm_api_key`
2. GitHub PAT → stored as `github_pat`
3. Telegram Bot Token → stored as `telegram_bot_token`

Sophia can optionally seed additional credentials (AWS keys, etc.) via the vault API once the instance is running.

### Step 9: Verify

Checklist:

- [ ] `/vault/status` loads and shows runtime config
- [ ] Vault shows the 3 non-negotiables
- [ ] Telegram bot responds to `/start`
- [ ] Governor can send a message and get a response

---

## 4. Credential Handoff Flow

```
Governor                          Sophia                          New Instance
   |                                |                                |
   |--- "Spawn for Bilal" -------->|                                |
   |                                |--- provision EC2 ------------>|
   |                                |--- clone codebase ----------->|
   |                                |--- register identity -------->|
   |                                |--- fork context repo -------->|
   |                                |--- create transcript repo --->|
   |                                |--- start service ------------>|
   |                                |--- report URL --------------->|
   |<-- "Ready at https://..." -----|                                |
   |                                |                                |
   |--- visit vault UI ------------>|                                |
   |--- add 3 credentials --------->|                                |
   |--- send test message --------->|                                |
   |<-- "I'm alive!" --------------|                                |
```

---

## 5. Notes

- Each instance has its **own** vault encrypted with its **own** Fernet key. Credentials are never shared between instances.
- The new instance's `/vault/status` page shows its own runtime config (LLM model, context repo, transcript repo, git commit).
- The governor can destroy the instance at any time by terminating the EC2 instance and deleting the repos.
- For a quick test, the governor can also run the autopilot locally with `python3 app/main.py`.
