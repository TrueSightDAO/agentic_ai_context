# China Team Technical Brief: Traceability Infrastructure & Great-Firewall Readiness

**To:** Baluka, Peter — China team (under Liz)
**From:** Autopilot / Governance
**Date:** 2026-08-04
**Status:** Draft v0.1 — for investigation & feedback

> 中文摘要：本文档为技术简报，面向中国团队（Baluka 与 Peter）。目标是 (1) 梳理我们已有的供应链溯源代码库；(2) 评估现有技术栈（Google Apps Script、GitHub、GitHub Actions、AWS）在中国防火墙内的可用性；(3) 请团队调查自身现有技术基础设施，明确哪些功能在防火墙内可用、哪些不可用；(4) 以 Gitee 与腾讯云为候选平台，规划中国区部署架构。

---

## 1. Purpose

This brief gives the China team the technical picture we already have, and sets the investigation tasks needed to operate inside mainland China:

1. **Map the codebases** that already implement supply-chain traceability (Section 3).
2. **Assess the current stack** — Google Apps Script, GitHub, GitHub Actions, AWS/EC2, TrueChain — against the Chinese firewall (Section 4).
3. **Investigate the China team's own tech infrastructure** (Section 7) — what is supported, what is not, behind the firewall.
4. **Plan the China deployment** with **Gitee** and **Tencent Cloud** as the two known candidates (Section 6).

The business context: Chinese exporters are capped below AAA on MSCI ESG ratings and face EU/US due-diligence barriers (CSRD/CSDDD/EUDR/UFLPA) because they lack **verifiable supply-chain evidence**. Our traceability stack — already live in Brazil — closes that gap. The China team's job is to make the same stack operable inside mainland China.

---

## 2. The capability we are deploying

Per-unit, tamper-evident supply-chain traceability:

1. **QR serialization** — every physical unit carries a unique QR code (e.g. `2024OSCAR_20260121_12`) resolving to a structured provenance record.
2. **Per-unit lineage manifests** — append-only JSON history of origin, processing, custody, events.
3. **Blockchain anchoring** — tamper-evident hashes on a permissioned, audit-ready chain.
4. **Identity & credentialing** — every actor holds a verifiable identity; every event is an attested chain.
5. **Document notarization** — audits, certifications, labor records stored, hashed, linked to units.
6. **Verification surfaces** — scan a QR to see full provenance + evidence in seconds; can render an export-ready due-diligence packet.

---

## 3. Codebases that support this (what exists today)

All repos live under the `TrueSightDAO` GitHub org and are public.

| Repo | What it is | How it supports traceability |
|---|---|---|
| **lineage-assets** | Per-asset provenance manifests, `qrs/<qr-id>.json` (append-only), additive schema (`SCHEMA.md`), `scripts/seed_from_sheet.py` | The per-unit provenance record — the core of traceability. Schema designed to accept new asset types (`textile_lot`, `electronics_batch`, `agri_lot`) without refactor. |
| **lineage-credentials** | Humans + acts: every actor gets a keypair; attested chains | Identity layer — who attested each event; the basis for labor/compliance attestations. |
| **TrueChain** | Private Ethereum (Geth, Clique PoA), chain id 98794616, gas price 0; registries: Shipment, Farm, Product, Invoice, QR, SalesReceipt, Contribution; mirror service Sheets→chain→tx hash | Immutable, tamper-evident anchoring of every record; the audit trail. |
| **tokenomics** (`google_app_scripts/`) | Google Apps Script automation: inventory management (sales/movements/QR), contribution scoring, expenses, ledger updates | QR generation, inventory movements, ledger sync — the operational automation. |
| **notarizations** | Document/media evidence storage + hashing + linking | Evidence layer: audits, certifications, labor records attached to units. |
| **dao_client** | Python CLI for Edgar signed events (INVENTORY MOVEMENT, SALES EVENT, QR REGISTRATION, …) | Programmatic submission of traceability events; scripting/automation. |
| **agroverse-inventory** | Inventory state (ledger mirror) | Current inventory/custody status per unit. |
| **truesight_autopilot** | The autopilot (Sophia) + agent tooling + `.github/workflows` | Automation, SRE, CI/CD orchestration. |
| **dapp_beta** | DApp frontend (report_contribution.html, etc.) | User-facing submission/verification UI (to be replaced by China-native surfaces). |
| **go_to_market** | GAS SEO monitoring, outreach scripts | Marketing/outreach tooling (GAS-dependent — see Section 4). |

---

## 4. Current infrastructure and its Great-Firewall status

| Component | Current host | GFW status (as commonly reported — **verify**) | Works behind GFW? | China replacement / mirror |
|---|---|---|---|---|
| **Google Apps Script** (runtime, `script.google.com`, `googleapis.com`) | Google cloud (US) | Google services are blocked in mainland China | ❌ No | Tencent CloudBase / 微信云开发 (WeChat Cloud Development) serverless; Aliyun 函数计算 FC; 云效 |
| **Google Sheets** (Main Ledger, data plane) | Google cloud | Blocked; also PIPL data-residency concern | ❌ No | Tencent Cloud Database / COS / self-hosted DB; per-jurisdiction ledger |
| **GitHub** (code + lineage-assets JSON + Actions) | GitHub (US) | `github.com` unreliably accessible; `raw.githubusercontent.com` often blocked; Actions runners are outside China | ⚠️ Partial — automation that runs outside China is fine; **day-to-day dev from inside China is unreliable** | **Gitee (码云)** — git hosting + Gitee Go CI/CD + Gitee Pages; GitHub→Gitee mirror sync |
| **GitHub Actions** (CI/CD) | GitHub runners | Runners outside China; usable for builds/deploys targeting external hosts | ⚠️ Partial — builds fine, but China-side triggering/pushing is unreliable | **Gitee Go**, **Tencent Cloud CODING CI/CD**, Aliyun 云效流水线, self-hosted Jenkins |
| **AWS EC2 (US East)** — autopilot, Edgar API, truesight.me | AWS us-east-1 | AWS not wholesale-blocked, but high latency + intermittent instability; PIPL data-residency issue for Chinese supply-chain data | ⚠️ Partial (reachable, not optimal) | **Tencent Cloud CVM** / lightweight servers; keep offshore endpoints only for cross-border verification |
| **TrueChain (private POA chain)** | Self-hosted nodes | Self-hosted — runs anywhere incl. mainland | ✅ Yes | Can run on Tencent Cloud CVM; no GFW issue; public RPC needs ICP if mainland-hosted public endpoint |
| **Telegram** | — | Blocked in mainland | ❌ No | WeChat / 企业微信; (we already run an mtproto_proxy for governance comms) |
| **truesight.me / edgar.truesight.me** (verification surfaces) | AWS US | Reachable but slow/unstable from mainland | ⚠️ Partial | China-hosted verification mirror + **WeChat Mini Program** for QR scanning |

---

## 5. Summary: works as-is / needs mirror / needs replacement

### ✅ Works as-is behind the firewall
- **TrueChain** private chain (self-hosted) — anchoring, hashing, audit trail.
- **lineage-assets JSON manifests** (content itself) — data format is portable; hosting is the issue.
- **All schema/format decisions** — additive JSON, append-only events, per-unit identity — are platform-agnostic.

### 🔁 Needs a mirror (same capability, China-hosted copy)
- **Git** hosting → **Gitee** (mirror TrueSightDAO repos; Gitee Go for CI).
- **CI/CD** → **Gitee Go** or **Tencent CODING**.
- **Object storage / static content** → **Tencent COS** (+ CDN).
- **Verification pages** → China-hosted copy of `truesight.me/qr/?id=` surface; domain needs **ICP 备案**.

### 🔧 Needs replacement (fundamentally different runtime)
- **Google Apps Script** → Tencent CloudBase / 微信云开发 (serverless + DB, WeChat-native) or Aliyun FC.
- **Google Sheets data plane** → Tencent Cloud DB / COS / ledger mirror (per-jurisdiction).
- **Telegram-based flows** → WeChat / 企业微信.

---

## 6. China deployment target architecture (proposal)

```
┌─────────────────────────────────────────────────────────────┐
│  China side (mainland)                                      │
│  · Gitee org         — code + Gitee Go CI/CD                │
│  · Tencent CloudBase — serverless functions (GAS analogue)  │
│  · Tencent COS+CDN  — JSON manifests, verification assets   │
│  · Tencent Cloud DB — ledger mirror (data residency)        │
│  · WeChat Mini Program — QR scan → provenance view          │
│  · TrueChain node (CVM) — anchoring                         │
│  · Domain with ICP 备案 — public verification surface       │
└─────────────────────────────────────────────────────────────┘
        │  cross-border verification API (read-only)           │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Offshore side (existing)                                   │
│  · TrueChain + lineage-assets + notarizations (existing)    │
│  · EU/US buyers / rating agencies verify via API/QR         │
└─────────────────────────────────────────────────────────────┘
```

**Key design points:**
- **Per-jurisdiction data residency** — the `lineage-assets-china` / `lineage-assets-brazil` repo pattern is already designed in our codebase; China data stays in China, cross-border queries are read-only API.
- **WeChat Mini Program for QR verification** — this is the China-native equivalent of scanning a QR; strong fit for Chinese manufacturers/buyers.
- **ICP 备案** is mandatory for any public web service hosted on mainland domains — factor into timelines.
- **Mirror, don't fork** — keep TrueSightDAO repos as source of truth; Gitee is a synchronized mirror, not a divergent fork.

---

## 7. Investigation checklist — Baluka & Peter

Please investigate and report back (this is the core ask of this brief):

1. **Current tech infrastructure** — what do you (the China team) currently run? List: code hosting, CI/CD, serverless/runtime, databases, storage, domains, compliance (ICP), team tooling.
2. **Which of our existing features work behind the firewall as-is?** Test: can you reach GitHub reliably? GAS? `truesight.me`? AWS-hosted APIs? Record observed behavior (reachable / slow / blocked).
3. **Gitee** — confirm: org setup, Gitee Go availability & free-tier limits, Gitee Pages, repo-size/private-repo limits, GitHub→Gitee sync options. What is supported vs not?
4. **Tencent Cloud** — confirm: CODING DevOps (git + CI/CD), CloudBase (serverless, WeChat 云开发), COS + CDN, CVM pricing, ICP 备案 process & timeline, WeChat Mini Program dev account.
5. **WeChat integration** — mini-program QR scanning: feasibility, approval requirements, API surface.
6. **Data residency** — any Chinese legal constraints (PIPL / data-classification) on storing factory supply-chain data in mainland vs offshore. What must stay in-country?
7. **Feature gaps** — for each of our core capabilities (QR minting, lineage events, anchoring, notarization, verification), name the China-side component that would provide it and any feature that does not exist yet.

Output: a short report (MD) — per item: **status (works / partial / missing) → evidence → recommendation**. File it in this repo under `china/`.

---

## 8. Open questions / next steps

1. **Liz to confirm** scope: is this for a pilot factory (textiles/electronics/agro) or platform build-out?
2. **Baluka & Peter to deliver** the Section 7 investigation report (target: within 2 weeks).
3. **Autopilot to support**: once the team confirms candidates, I can (a) set up Gitee mirror + Gitee Go workflow, (b) scaffold a Tencent CloudBase function mirroring our GAS logic, (c) draft the WeChat Mini Program spec, (d) prepare the per-jurisdiction `lineage-assets-china` deployment.
4. **Timeline**: investigation (wk 0–2) → target architecture sign-off (wk 2–3) → pilot deployment (wk 3–8).

---

*Draft v0.1 — internal. GFW status items marked "verify" are reported/common knowledge as of 2026; the China team's investigation (Section 7) is the authoritative check.*
