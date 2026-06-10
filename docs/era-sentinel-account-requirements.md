# ERA Sentinel — Account Requirements & Deployment Roadmap

Prepared by Sophia Truesight (TrueSight DAO Autopilot) — June 2026

---

## Overview

Bilal from ERA Professionals wants to create a dedicated AI Sentinel for fund management. The idea is to run DeepSeek and Claude side by side, with a human in the loop comparing their outputs to catch hallucinations and finalize decisions. This document lists every account and piece of infrastructure needed to spin up that Sentinel — a parallel instance of the TrueSight DAO Autopilot living in ERA's own AWS account, with its own Telegram identity, its own context memory, and its own API keys. It also includes a step-by-step execution roadmap so Bilal and Gary know exactly who does what and in what order.

---

## PART 1: ACCOUNTS & INFRASTRUCTURE REQUIRED

### 1. AWS Account (Bilal provides)
- t3.medium EC2 (4 GB RAM, 2 vCPUs) with Ubuntu 22.04
- Elastic IP (static public IP)
- Security group: SSH from 52.200.38.206 + HTTP/HTTPS from 0.0.0.0/0
- Cost: ~$35/month

### 2. Domain / DNS (Bilal provides)
- A subdomain like sentinel.era.com
- DNS A record pointing to the Elastic IP
- SSL cert (auto-provisioned by certbot)
- Cost: ~$0-10/month

### 3. Telegram Bot (Gary creates)
- New bot via @BotFather (e.g. @era_sentinel_bot)
- Bot token goes into .env
- Bot must be admin in ERA's Telegram group with Manage Topics

### 4. GitHub Account (Bilal provides)
- A private repo for context memory (e.g. era-sentinel-context)
- Fine-grained PAT with Contents:Read+Write and PRs:Read+Write
- Cost: Free (public) or $4/month (private)

### 5. LLM API Keys (Bilal provides)
- DeepSeek API key (~$5-20/month)
- Claude API key (~$10-30/month)
- Both go into .env

### 6. Gmail Account (Bilal provides)
- A dedicated Gmail for the Sentinel (e.g. sentinel@era.com)
- Gmail API enabled in Google Cloud Console
- OAuth token generated (one-time interactive flow)

### 7. Google Cloud Service Account (Bilal provides — if using Sheets)
- Google Cloud project under ERA
- Service account with Sheets + Drive API enabled
- JSON key file goes into config/google/

### 8. Tavily API Key (Bilal provides — recommended)
- For web search capability
- Cost: ~$10/month

### 9. Grok API Key (Bilal provides — optional)
- For vision/image analysis
- Cost: ~$5/month

### 10. Bugsnag (Bilal provides — recommended)
- Error monitoring, free tier
- API key goes into .env

---

## PART 2: EXECUTION ROADMAP — STEP BY STEP

### PRE-FLIGHT: Bilal provides the accounts

Checklist:
- [ ] AWS account created with billing method
- [ ] EC2 t3.medium launched (Ubuntu 22.04) with Elastic IP
- [ ] Security group configured
- [ ] Domain pointed to Elastic IP
- [ ] GitHub account + private context repo created
- [ ] GitHub PAT generated
- [ ] DeepSeek API key obtained
- [ ] Claude API key obtained
- [ ] Gmail account + API enabled + OAuth token
- [ ] (Optional) Tavily API key
- [ ] (Optional) Bugsnag project

### UNIT 1: Gary creates the Telegram bot

- [ ] Create bot via @BotFather
- [ ] Copy bot token
- [ ] Add bot to ERA's Telegram group as admin
- [ ] Hand token to Bilal

### UNIT 2: Fork and customize the codebase

- [ ] Fork truesight_autopilot into ERA's GitHub
- [ ] Create era-sentinel-context repo
- [ ] Customize system prompt for fund management
- [ ] Remove DAO-specific tools (cacao QR, inventory, supply chain)
- [ ] Add fund-management tools if needed
- [ ] Commit and push

### UNIT 3: First deployment to ERA's EC2

- [ ] SSH into ERA's EC2 from autopilot box (52.200.38.206 as bastion)
- [ ] Clone the forked repo
- [ ] Create .env with all API keys
- [ ] Run deploy.sh (adapted for ERA)
- [ ] Verify all 3 systemd units active
- [ ] Verify health endpoint
- [ ] Set up nginx + certbot for HTTPS
- [ ] Configure Telegram webhook

### UNIT 4: First conversation — the 81 trials

- [ ] Bilal sends first message
- [ ] Sentinel responds — Bilal reviews and corrects
- [ ] First 10 corrections establish baseline
- [ ] First 20-30 corrections build trust
- [ ] After ~100 corrections, Sentinel anticipates needs

### UNIT 5: Fund management tooling

- [ ] Define data sources (Sheets? CSV? API?)
- [ ] Build tools for reading fund data
- [ ] Implement DeepSeek vs Claude comparison
- [ ] Set up scheduled reports or alerts
- [ ] Iterate based on Bilal's corrections

### UNIT 6: Documentation for future clones

- [ ] Document deployment process
- [ ] Create reusable template
- [ ] File improvements back to main codebase

---

## RESUME TRACKER

| Unit | Status |
|------|--------|
| PRE-FLIGHT: Bilal provides accounts | **PENDING — START HERE** |
| UNIT 1: Gary creates Telegram bot | PENDING |
| UNIT 2: Fork and customize codebase | PENDING |
| UNIT 3: First deployment to EC2 | PENDING |
| UNIT 4: First conversation + corrections | PENDING |
| UNIT 5: Fund management tooling | PENDING |
| UNIT 6: Documentation and handoff | PENDING |

---

## WHAT THE SENTINEL CANNOT DO ON DAY ONE

The infrastructure deploys in an afternoon. But the relationship — the specific sequence of corrections Bilal will make, the trust built through specific decisions, the shared language that emerges — that takes weeks to months. This is the Polanyi paradox in practice: the scripture can be forked, but the journey cannot be cloned.

The first week will be:
- Bilal asks a question → the Sentinel answers imperfectly → Bilal corrects → the Sentinel learns
- Bilal spots a hallucination → flags it → the Sentinel adjusts its confidence threshold
- Bilal notices a pattern in fund data → asks the Sentinel to track it → the Sentinel builds a new tool

After ~20-30 corrections, the Sentinel starts to anticipate what Bilal needs. After ~100, it becomes a genuine partner.

---

*This document was generated by Sophia Truesight (TrueSight DAO Autopilot). For questions, reach Gary Teh or reply in the Telegram thread.*