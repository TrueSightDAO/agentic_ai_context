# China Ecosystem Mappings Investigation — Task Brief (Peter & Baluka)

**To:** Peter, Baluka — China team (under Liz)
**From:** Autopilot / Governance
**Date:** 2026-08-05
**Status:** Task assignment — deliver mappings report before the in-office review
**Review:** In-office review with Gary, day after tomorrow

> 中文摘要：Peter 与 Baluka 的任务：调查你们现有的技术生态中可用于供应链溯源的「映射（mappings）」——我们每一项核心能力，在你们现有平台/工具/账号中，哪些功能可以承接、哪些缺失、哪些需要重建。交付映射表（状态 → 证据 → 建议），两天后办公室逐项评审。候选平台与基础设施方案由你们自行调查决定，本简报不预设任何建议。

---

## 0. Context: this infrastructure hosts the Trade Accelerator

This investigation serves **Elizabeth Wong's planned Trade Accelerator** — a program that helps Chinese manufacturers/exporters move **actual trade out of China** (physical exports) with verifiable supply-chain traceability.

**The accelerator's programs run on this infrastructure by default.** The platform we stand up in China is the operating backbone for:

- onboarding factories/exporters
- issuing QR lineage manifests per unit/batch
- anchoring records to chain (TrueChain pattern)
- producing the due-diligence / ESG evidence that EU/US buyers and raters accept
- supporting cross-border verification for export transactions

So the mappings you investigate are not an abstract exercise — they determine **which capabilities the accelerator can launch with**. A capability that is missing or broken behind the firewall blocks the corresponding accelerator program.

---

## 1. Why mappings

We deploy a per-unit supply-chain traceability stack: **QR → lineage manifest → blockchain anchor → notarized evidence → scan-verifiable verification**. It currently runs on Google Apps Script + GitHub + GitHub Actions + AWS — most of which is blocked or unreliable behind the Chinese firewall.

Before the Trade Accelerator can operate in mainland China, we need to know exactly which capabilities can be **mapped onto what you already have** (your current ecosystem), and which are missing or need rebuilding. The investigation and the platform choices are yours to make.

---

## 2. The 14 capabilities to map

| # | Capability | Our current implementation |
|---|---|---|
| 1 | Code hosting & version control | GitHub org (TrueSightDAO) |
| 2 | CI/CD (build, test, deploy) | GitHub Actions |
| 3 | Serverless automation runtime | Google Apps Script |
| 4 | Database / ledger | Google Sheets (main ledger) |
| 5 | Object storage & static content | GitHub (lineage-assets JSON manifests) |
| 6 | QR generation / minting | tokenomics GAS (agroverse_qr_code_generator) |
| 7 | QR verification surface | truesight.me/qr/?id= + edgar redirect |
| 8 | Blockchain anchoring | TrueChain (Geth Clique, self-hosted) |
| 9 | Identity / credentialing | lineage-credentials (RSA keypairs) |
| 10 | Notarization / document evidence | notarizations repo |
| 11 | Signed event submission (API) | dao_client → Edgar API |
| 12 | Domain + ICP 备案 | — (needed for mainland) |
| 13 | Team comms & notifications | Telegram |
| 14 | Monitoring & ops | AWS CloudWatch / autopilot |

---

## 3. Master mapping table (to fill — team's investigation)

Fill for each of the 14 capabilities: what in **your current ecosystem** can serve it, what is missing, the evidence, and your recommendation. **No pre-filled candidates** — per governance, the China team decides what to investigate and what to propose.

| # | Capability | Our current implementation | Your ecosystem (fill) | Evidence | Recommendation |
|---|---|---|---|---|---|
| 1 | Code hosting & version control | GitHub org | | | |
| 2 | CI/CD (build, test, deploy) | GitHub Actions | | | |
| 3 | Serverless automation runtime | Google Apps Script | | | |
| 4 | Database / ledger | Google Sheets | | | |
| 5 | Object storage & static content | GitHub (lineage-assets JSON) | | | |
| 6 | QR generation / minting | tokenomics GAS | | | |
| 7 | QR verification surface | truesight.me/qr/?id= | | | |
| 8 | Blockchain anchoring | TrueChain (self-hosted) | | | |
| 9 | Identity / credentialing | lineage-credentials (RSA) | | | |
| 10 | Notarization / document evidence | notarizations repo | | | |
| 11 | Signed event submission (API) | dao_client → Edgar API | | | |
| 12 | Domain + ICP 备案 | — | | | |
| 13 | Team comms & notifications | Telegram | | | |
| 14 | Monitoring & ops | AWS CloudWatch / autopilot | | | |

---

## 4. Deliverable format

For each of the 14 rows, fill:

- **Status** — works / partial / missing
- **Evidence** — test result, screenshot, doc link
- **Recommendation** — your proposed approach + the specific platform (adopt existing / mirror / rebuild, as you determine)

**File:** one MD report `china/CHINA_ECOSYSTEM_MAPPINGS_REPORT.md` in this repo.
**Due:** before the in-office review.

---

## 5. How to investigate (team's discretion)

Use your own method and existing accounts. For each capability:

- Note what works today and what is blocked or unreliable behind the firewall.
- Identify candidate platforms you already know of, or evaluate ones you consider viable.
- Record observed evidence (test results, screenshots, doc links) for each.

---

## 6. In-office review agenda (day after tomorrow)

1. Walk each of the 14 rows of your report.
2. Review your recommendations per capability.
3. Discuss and sign off the China deployment direction.
4. Assign next actions.
5. Confirm pilot scope with Liz (textiles / electronics / agro) for the Trade Accelerator.

---

*Draft v0.2 — internal task brief. Platform choices are the China team's investigation output; this brief deliberately pre-fills nothing.*
