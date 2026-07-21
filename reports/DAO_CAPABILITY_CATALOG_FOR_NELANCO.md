# TrueSight DAO — Capability Catalog

**Assets built by Gary Teh that Jake Nelan's team can use, integrate, or adapt**

**Prepared by:** Sophia Truesight (TrueSight DAO Autopilot)
**Date:** 2026-07-21
**For:** Cory (UX.App), Wayne, Jake Nelan — Nelanco / Herbalife / Restory

---

## 1. Why This Document Exists

Over the past several years, Gary Teh has built a portfolio of production-grade software assets — a DAO protocol, a data harvesting platform, an AI agent fleet, and supply-chain tracking infrastructure. These assets currently run on **Jake Nelan's AWS account (Nelanco, 767697632458)**.

This document catalogs each asset **not as an inventory list**, but as a **capability** — what it does, what problem it solves, and how Jake's team (Herbalife, Restory, or any other venture) could adopt, integrate, or white-label it.

---

## 2. Asset 1: Edgar — The DAO Protocol & Event Engine

### What It Is
A **signed-event submission and verification protocol**. Any action (a sale, a transfer, a contribution, a partner check-in) is cryptographically signed with an RSA-2048 keypair, submitted to an API, verified, logged to a ledger, and dispatched to downstream webhooks.

### Technical Stack
- Rails API server (Perch) + Python FastAPI port (dao_protocol)
- PostgreSQL + Redis backend
- Google Sheets as the human-readable ledger layer
- Google Apps Script webhooks for automation

### What It Solves
**Trustless audit trails without a blockchain.** Every event is signed by an identity, verified by the server, and immutably logged. Anyone with read access can verify the chain of custody.

### How Nelan's Team Could Use It
- **Herbalife supply chain:** Track ingredient lots from supplier to distributor with cryptographic signatures at each handoff. No more spreadsheet reconciliation.
- **Restory customer interactions:** Sign every support ticket, refund, or escalation — full audit trail without building a custom logging system.
- **Any multi-party workflow:** When multiple orgs need to agree on what happened and when, Edgar provides the canonical record.

---

## 3. Asset 2: Sophia — The Autonomous SRE & Developer Agent

### What It Is
An **AI agent that lives on an EC2 box** and acts as a full-time site reliability engineer and junior developer. She monitors email, AWS health, and GCP services; diagnoses failures; opens fix PRs; manages inventory; and communicates via Telegram.

### Technical Stack
- Python, DeepSeek-V3 LLM brain
- 4 systemd services (autopilot, telegram adapter, watchdog, vault)
- SSH fleet access to all Nelanco hosts
- Gmail API, GitHub API, AWS SDK integrations

### What It Solves
**24/7 operational coverage without a human on call.** Sophia reads error emails, checks service health, diagnoses root causes, and opens pull requests to fix issues — all autonomously. She also handles routine tasks like QR code scanning, inventory movements, and DAO contribution logging.

### How Nelan's Team Could Use It
- **Restory ops:** Deploy a Sophia instance to monitor Restory's Lambda functions, RDS health, and S3 storage. She'd catch cold-start latency regressions, storage threshold warnings, and auth failures before they become incidents.
- **Herbalife infrastructure:** Monitor the 3PL/logistics stack — if a warehouse API goes down, Sophia detects it, diagnoses the cause, and opens a fix PR or alerts the team.
- **White-label SRE-as-a-Service:** Jake could offer Sophia as a managed service to his portfolio companies — a $50/month EC2 box replaces a $120K/year SRE.

---

## 4. Asset 3: The Multi-LLM Agent Fleet

### What It Is
A **tiered fleet of LLM coding agents** (Claude, DeepSeek, Gemini, Grok, Cursor, Codex, etc.) organized by seniority — Architect, Senior, Junior, Specialist — with a shared context repository and handoff protocol.

### Technical Stack
- agentic_ai_context repo — model-agnostic institutional memory
- Handoff prompts for mid-task model switching
- Cost discipline: frontier models for architecture, cheap models for grunt work

### What It Solves
**Engineering leverage without hiring.** A single operator (Gary) directs a fleet of 10+ LLM "engineers" that together can design systems, write code, review PRs, and execute well-scoped tasks — all coordinated through written plans and shared docs.

### How Nelan's Team Could Use It
- **Restory development:** Spin up Claude Code + DeepSeek on the nelanco-claude box to accelerate Restory feature development. The handoff protocol means a senior model designs the architecture, then a cheap model implements the bulk.
- **Herbalife internal tools:** Use the fleet to build and maintain internal dashboards, data pipelines, and reporting tools — without hiring a dedicated dev team.
- **Template for Jake's own ventures:** The playbook (agentic_ai_context, handoff prompts, tiering) is fully documented and transferable.

---

## 5. Asset 4: Krake / GetData.io — Data Harvesting Platform

### What It Is
A **production data-harvesting Rails application** that collects, processes, and serves structured data from public web sources. Includes a Chrome extension for browser-based collection, Sinatra microservices, and a Sidekiq worker fleet.

### Technical Stack
- Rails (port 3002, behind ALB krake-ror-1)
- 4× Sidekiq processes for concurrent harvesting
- Redis cache layer
- Chrome extension for manual collection
- Cross-account DNS (Explorya Route53 → Nelanco ALB)

### What It Solves
**Structured data from unstructured web sources at scale.** Instead of manual copy-paste or fragile scrapers, Krake provides a managed pipeline with queueing, deduplication, and structured output.

### How Nelan's Team Could Use It
- **Herbalife competitor intelligence:** Monitor distributor pricing, product availability, and promotional strategies across wellness competitors — automated, structured, daily.
- **Restory market research:** Harvest customer sentiment data from public review sites to feed Restory's analytics pipeline.
- **3PL logistics pricing:** Track shipping rates, warehouse costs, and carrier performance across the logistics industry.

---

## 6. Asset 5: QR Code Supply-Chain Tracking

### What It Is
A **serialized QR code system** for physical products. Every bag of cacao gets a unique QR code (format: YYYYPRODUCER_EXPIRYDATE_BATCH) that traces its entire journey — from farm to warehouse to retailer to customer. Scanning the QR shows the tree that was planted with that purchase.

### Technical Stack
- Batch QR generation via Google Apps Script
- GitHub-hosted compiled QR sheets
- DAO ledger integration (INVENTORY MOVEMENT, SALES EVENT)
- truesight.me landing pages per SKU/tree

### What It Solves
**Provenance transparency for physical goods.** Customers can verify exactly where their product came from, who handled it, and what impact their purchase had. This builds trust and justifies premium pricing.

### How Nelan's Team Could Use It
- **Herbalife product traceability:** Every bottle of supplement gets a QR code showing ingredient origin, manufacturing batch, and distribution chain — a massive trust differentiator in the wellness industry.
- **Restory customer receipts:** After a support interaction, generate a QR-linked attestation showing what was resolved, by whom, and when.
- **3PL logistics:** QR-track each pallet through the warehouse — scan at receiving, scan at storage, scan at dispatch. Full chain of custody without expensive RFID hardware.

---

## 7. Asset 6: The Growth Engine (Email360 + Partner Outreach)

### What It Is
A **warm-up email outreach system** (Email360) combined with a partner check-in protocol and a Beer Hall daily digest. Built on the three-band growth model (Linear Channels → Acquisition Loops → Retention Loops) that Gary originally developed at GetData.io.

### Technical Stack
- DApp warmup_review.html queue
- Gmail API for sending
- Partner check-in concierge UX
- Beer Hall daily digest (Telegram + truesight.me)

### What It Solves
**Systematic partner acquisition and retention without a sales team.** Warm-up emails go out, partners check in, and the daily digest keeps everyone aligned — all driven by automation with human review at key gates.

### How Nelan's Team Could Use It
- **Herbalife distributor onboarding:** Use Email360 to warm up and onboard new distributors at scale. The partner check-in protocol keeps them engaged post-signup.
- **Restory customer success:** The check-in loop pattern applies directly to B2B SaaS customer retention — automated check-ins with escalation when a customer goes quiet.
- **Any recurring-revenue business:** The growth model is a documented playbook, not just code. Jake's portfolio companies can adopt the framework regardless of tech stack.

---

## 8. Asset 7: The DApp & Tokenomics Layer

### What It Is
A **decentralized application** (dapp.truesight.me) for DAO governance — signature creation, voting rights, expense reporting, capital injections, currency conversion, and store interaction history. Backed by Google Apps Script automation and a tokenomics engine.

### Technical Stack
- Static HTML/JS on GitHub Pages
- Google Apps Scripts for ledger operations
- Python scripts for market making (Raydium)
- Multi-currency double-entry bookkeeping

### What It Solves
**Lightweight governance and financial operations for a distributed organization.** Anyone with a contributor identity can submit expenses, record sales, or move inventory — all cryptographically signed and ledgered.

### How Nelan's Team Could Use It
- **Restory internal ops:** Use the DApp's expense reporting and capital injection flows for Restory's own operational accounting.
- **Herbalife distributor commissions:** The tokenomics engine could track and distribute commissions to distributors — transparent, auditable, automated.
- **Multi-entity bookkeeping:** The currency conversion system (USD ↔ BRL via Wise) is directly applicable to any cross-border business.

---

## 9. Summary: What's Running on Nelanco's AWS Today

| Asset | What It Does | How Nelan's Team Benefits |
|-------|-------------|---------------------------|
| **Edgar** | Signed-event protocol + audit trail | Trustless supply chain / customer interaction logging |
| **Sophia** | 24/7 autonomous SRE + developer | Replace on-call SRE; ops monitoring for Restory |
| **LLM Fleet** | Tiered AI coding agents | Accelerate development without hiring |
| **Krake/GetData.io** | Data harvesting at scale | Competitive intelligence, market research |
| **QR Tracking** | Serialized product provenance | Product traceability for Herbalife / 3PL |
| **Growth Engine** | Email360 + partner outreach | Distributor onboarding, customer retention |
| **DApp + Tokenomics** | DAO governance + multi-currency ledger | Internal ops, commission tracking |

---

## 10. Suggested Next Conversation

1. **Walk through this catalog** with Cory, Wayne, and Jake
2. **Identify the top 1-2 assets** that solve an immediate pain point for their team
3. **Run a pilot** — e.g., deploy a Sophia instance for Restory ops monitoring, or QR-trace a Herbalife product batch
4. **Discuss infrastructure cost sharing** — the DAO already runs on Nelanco's account; formalize the arrangement

---

*End of report. Prepared by Sophia Truesight (TrueSight DAO Autopilot) for Gary Teh. All data sourced from live AWS inventory and DAO context files. This document is a capability catalog, not a technical inventory — every asset listed is production-tested and available for adaptation.*
