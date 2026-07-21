# TrueSight DAO — Asset, Infrastructure & Agent Inventory

**Prepared by:** Sophia Truesight (TrueSight DAO Autopilot)
**Date:** 2026-07-21
**Audience:** Cory (UX.App), Wayne, Jake Nelan (Nelanco / Herbalife)

---

## 1. Executive Summary

TrueSight DAO is a regenerative finance (ReFi) ecosystem built around **Agroverse ceremonial cacao** — financing Amazon rainforest trees through verifiable supply-chain actions. The entire technical stack runs across **two AWS accounts** (Explorya and Nelanco), with the majority of production services hosted on **Jake Nelan's Nelanco account**.

This document inventories every asset, service, and AI agent operating within the DAO, and maps how they interconnect.

---

## 2. AWS Account Architecture

### Account 1: Explorya (440626669078)
- **Owner:** Gary Teh (TrueSight DAO)
- **Purpose:** DNS (Route53 for truesight.me, agroverse.shop), legacy stopped instances, GitHub Pages origins
- **Key assets:** Route53 zones, old seni_ror/seni_sk (STOPPED)

### Account 2: Nelanco (767697632458)
- **Owner:** Jake Nelan
- **Purpose:** All production DAO services, Krake/GetData.io data harvesting, Restory app
- **Key assets:** 12+ EC2 instances, RDS, 23 S3 buckets, ALB, Lambda functions

---

## 3. Production Services — Full Inventory

### 3.1 DAO Core Services

| Service | Host | Purpose | Stack |
|---------|------|---------|-------|
| **Edgar (Perch)** | seni_ror_200250915 | DAO API server — receives signed event submissions, verifies RSA signatures, logs to Google Sheets, dispatches webhooks | Rails (Puma), PostgreSQL, Redis |
| **Edgar (dao_protocol)** | dao_protocol_nelanco | Python port of the submission + dispatch logic. Accepts POST /dao/submit_contribution | Python FastAPI, port 8010 |
| **dao-protocol-beta** | dao-protocol-beta | Isolated test sandbox for Stripe test-mode E2E tests | Python FastAPI, port 8010 |
| **Sidekiq Workers** | seni_sk_auto (ASG × 2) | Background job processing — webhook triggers, inventory snapshots, DAO member cache | Rails Sidekiq |
| **PostgreSQL** | seni_sql_2026 | Primary database for Edgar/Perch | PostgreSQL |
| **Redis** | seni_redis_2 | Sidekiq queue, cache layer | Redis (t2.large) |

### 3.2 Krake / GetData.io (Data Harvesting)

| Service | Host | Purpose | Stack |
|---------|------|---------|-------|
| **Krake Rails** | krake_ror | Production data-harvesting backend at getdata.io | Rails, port 3002, behind ALB krake-ror-1 |
| **Krake Sidekiq** | krake_sk_consolidated | 4× Sidekiq processes for data harvesting | Rails Sidekiq (t2.small) |
| **Krake Redis** | GETDATA_REDIS | Redis cache for Krake | Redis (t3a.small) |
| **Krake Sinatra** | (local tools) | Supporting Sinatra microservices | Ruby Sinatra |
| **Krake Chrome Extension** | (browser) | Data harvesting Chrome extension | JavaScript |
| **Krake Local** | (local Node) | Local commander/listener tools | Node.js |

### 3.3 Infrastructure

| Service | Host | Purpose |
|---------|------|---------|
| **Nginx Reverse Proxy** | krake_nginx | Terminates HTTPS for edgar.truesight.me, api.truesight.me, chatbot.truesight.me. Proxies to Rails (:3000) and autopilot (:8000) |
| **ALB** | krake-ror-1 | Load balancer for getdata.io traffic to Krake Rails |

### 3.4 Restory App (Jake's Project)

| Service | Purpose |
|---------|---------|
| **Restory Auth** | Lambda: restory-auth2-prod-auth — authentication service |
| **Restory File Storage** | Lambda + S3 buckets — user photo processing |
| **Restory GraphQL API** | Lambda: restory-graphql-api-prod-graphql |
| **Restory WebSocket** | Lambda: restory-websocket-dev-connectHandler |
| **Restory Chat** | S3: restory-chat-prod-* — chat platform (Chatwoot-based) |
| **Restory Analytics** | S3: restory-analytics-* |
| **Restory Database** | RDS Aurora PostgreSQL (serverless) — restory-instance-1 |
| **Restory Pulumi** | S3: restory-pulumi — infrastructure-as-code state |

---

## 4. The AI Agent Fleet

### 4.1 Sophia (TrueSight DAO Autopilot) — Primary Agent

- **Identity:** Sophia Truesight (admin+sophia@truesight.me)
- **Host:** sophia-nelanco (i-05276b8ae82d6b88c, t3.medium, EIP 3.214.167.219)
- **DNS:** sophia.truesight.me
- **Systemd services:**
  - truesight-autopilot — main brain (DeepSeek-V3-powered)
  - truesight-telegram — Telegram adapter
  - truesight-watchdog — health monitoring
  - truesight-vault — secrets management
- **Capabilities:**
  - Autonomous SRE — monitors email/AWS/GCP health, diagnoses failures
  - Developer — reads context, opens fix PRs (never auto-merges)
  - DAO contributor — submits signed [CONTRIBUTION EVENT]s to Edgar
  - QR code scanning and inventory management
  - Gmail operations (search, read, send, draft)
  - Google Sheets/Docs/Drive access
  - SSH fleet management across all Nelanco hosts
  - Multi-turn auto-advance execution plans
  - Live progress introspection

### 4.2 Claude Code (Interactive Agent)

- **Identity:** Claude Anthropic (admin+claude@truesight.me)
- **Host:** nelanco-claude (i-01ad5eca707e4445f, EIP 100.57.50.48)
- **DNS:** claude.truesight.me
- **Role:** Senior engineer — multi-file edits, system design, plan writing
- **Driven via:** Mobile app with --remote-control

### 4.3 Deep Seek (Interactive Agent)

- **Identity:** Deep Seek (admin+deepseek@truesight.me)
- **Role:** Specialist — narrow, well-defined tasks, cost-efficient

### 4.4 Multi-LLM Orchestration Layer

The DAO operates a tiered LLM fleet modeled like an engineering org chart:

| Tier | Models | Best For |
|------|--------|----------|
| **Architect** | Claude Opus 4.x, GPT-5 long-ctx | Loading the whole codebase, designing systems, writing plans |
| **Senior** | Claude Sonnet 4.x, Gemini 2.x Pro, Grok 4 | Implementing within a single subsystem, review, refactors |
| **Junior** | Claude Haiku 4.5, GPT-5 mini, DeepSeek | Narrow well-defined tasks, lint cleanup, templates |
| **Specialist** | Codex, Cursor agents, Copilot, Whisper | In-IDE completion, transcription, sandboxed execution |

**Key pattern:** agentic_ai_context is the shared substrate — model-agnostic institutional memory. Any LLM can ramp in by reading the relevant docs. Handoff prompts transfer state between models mid-task.

### 4.5 Registered DAO Agent Identities

| Agent | Email | Status |
|-------|-------|--------|
| Sophia Truesight | admin+sophia@truesight.me | Active (autopilot) |
| Claude Anthropic | admin+claude@truesight.me | Active (interactive) |
| Deep Seek | admin+deepseek@truesight.me | Active (interactive) |

---

## 5. GetData.io / Krake — Deep Dive

### 5.1 What It Is

GetData.io (krake_ror) is a **data harvesting platform** — a Rails application that collects, processes, and serves structured data from public web sources. It was the growth engine Gary built before TrueSight DAO, and its structural patterns (three-band growth model: Linear Channels → Acquisition Loops → Retention Loops) were directly carried over into the DAO's growth model.

### 5.2 Architecture

```
getdata.io (apex) → ALB krake-ror-1 → krake_ror Rails (:3002)
                                        → krake_sk_consolidated (4× Sidekiq)
                                        → GETDATA_REDIS
cache.getdata.io → CloudFront distribution
cache-2.getdata.io → CloudFront distribution
```

### 5.3 SSL/TLS Topology

The Route53 zone for getdata.io lives in the **Explorya** account, while the ALB that terminates TLS lives in **Nelanco** — a cross-account DNS setup. The `*.getdata.io` certificate (Sectigo-issued) is imported into both accounts.

### 5.4 Relationship to the DAO

The Krake infrastructure is the **data backbone** that the DAO's growth model was patterned after. Key carry-overs:
- The three-band growth model (Linear Channels → Acquisition Loops → Retention Loops)
- The Email360 warm-up outreach system
- The partner check-in cadence
- The Beer Hall daily digest concept

---

## 6. DAO Growth Model (Structural Overview)

### North Star
**Today:** Trees financed per month
**Widening to:** Verifiable compassionate actions attested per month

### Linear Channels (how we acquire)
- Direct Marketing (Email360 warm-up) 🟧
- Personal driving (Gary visits retailers) 🟧
- Marketplace listings (Faire 🟩, Etsy 🔻, Amazon 🔻)
- Content Marketing (truesight.me, Beer Hall, blog) 🟧
- QR Code Traceback (each bag → tree page) 🟧
- Industry partnerships (Butterfly Effect, Capoeira, Vipassana) 🟩

### Acquisition Loops (how users bring users)
- Retail Partner Referral 🟧
- QR Trace-Back Loop 🟧
- Contributor → Contributor (DAO governance flywheel) 🟧
- B2B Sales Loop (warm-up queue + krake_sinatra) 🟧
- Compassionate Action Attestation Loop 🟩

### Retention Loops (how we keep them)
- Email360 Retention (post-purchase nurture) 🟧
- Partner Check-in Loop 🟧
- Beer Hall Digest (daily DAO state) 🟧
- DApp Bell Loop (operator action items) 🟧
- Credentialing Lineage 🟩
- Trees Financed Dashboard 🟧

---

## 7. Potential Linkage Points with UX.App / Restory / Herbalife

| DAO Initiative | UX.App / Restory / Herbalife Link |
|----------------|--------------------------------------|
| **DApp & Shop UX redesign** | UX.App (Wayne/Cory) could design the DApp interface, agroverse.shop, and truesight.me |
| **Customer support for cacao partners** | Restory's chat platform could serve as the customer-facing support layer for farmers/retailers tracking their cacao bags |
| **3PL logistics integration** | If Restory has logistics capabilities, the DAO's consignment/freighting model could integrate — Restory handles logistics UI, DAO handles tokenomics |
| **Herbalife distribution channel** | Jake's Herbalife network could carry Agroverse ceremonial cacao as a wellness product, or use the DAO's QR lineage tracking for ingredient provenance |
| **Infrastructure consolidation** | The DAO already runs on Nelanco's AWS — deeper partnership could formalize shared infrastructure costs and cross-team DevOps |

---

## 8. Infrastructure Summary (Nelanco Account)

| Category | Count | Details |
|----------|-------|---------|
| EC2 Instances | 12+ | Ranging from t2.micro to t3.medium |
| RDS Instances | 1 | Aurora PostgreSQL (Restory) |
| S3 Buckets | 23 | DAO, Restory, CloudTrail |
| Lambda Functions | 5 | Restory auth, file storage, GraphQL, WebSocket, CloudFront |
| Load Balancers | 1 | krake-ror-1 ALB |
| AI Agents | 3 registered | Sophia, Claude, DeepSeek |
| LLM Models in Fleet | 10+ | Across Architect/Senior/Junior/Specialist tiers |

---

*End of report. Prepared by Sophia Truesight (TrueSight DAO Autopilot) for Gary Teh. All data sourced from live AWS inventory and DAO context files.*
