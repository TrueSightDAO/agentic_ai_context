# China Ecosystem Mappings Investigation — Task Brief (Peter & Baluka)

**To:** Peter, Baluka — China team (under Liz)
**From:** Autopilot / Governance
**Date:** 2026-08-05
**Status:** Task assignment — deliver mappings report before the in-office review
**Review:** In-office review with Gary, day after tomorrow

> 中文摘要：Peter 与 Baluka 的任务：在你们现有的技术生态中，调查可用于供应链溯源的「映射（mappings）」——我们每一项核心能力，在你们现有平台/工具/账号中，有哪些功能可以承接、哪些需要镜像（Gitee / 腾讯云）、哪些必须重建。交付映射表（状态 → 证据 → 建议），两天后办公室逐项评审。

---

## 1. Why mappings

We deploy a per-unit supply-chain traceability stack: **QR → lineage manifest → blockchain anchor → notarized evidence → scan-verifiable verification**. It currently runs on Google Apps Script + GitHub + GitHub Actions + AWS — most of which is blocked or unreliable behind the Chinese firewall.

Before we can operate in mainland China, we need to know exactly which capabilities can be **mapped onto what you already have** (your current ecosystem), and which need **Gitee / Tencent Cloud / WeChat** counterparts.

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

## 3. Master mapping table (fill + verify)

**Their current ecosystem** = what you already run that can serve this capability.
**Gitee / Tencent / WeChat** = pre-filled from public knowledge — **VERIFY with real accounts**.
**Verdict** = 采用 (adopt existing) / 镜像 (mirror) / 重建 (rebuild).

| # | Capability | Their ecosystem (to fill) | Gitee | Tencent Cloud | WeChat | Verdict |
|---|---|---|---|---|---|---|
| 1 | Code hosting | ? | Gitee repos [OK] | CODING [OK] | — | |
| 2 | CI/CD | ? | Gitee Go [PARTIAL] | CODING CI/CD [OK] | — | |
| 3 | Serverless runtime | ? | — | CloudBase / SCF [OK] | 微信云开发 [OK] | |
| 4 | Database / ledger | ? | — | MySQL / TDSQL [OK] | 云开发数据库 [OK] | |
| 5 | Object storage / static | ? | Gitee Pages (static) | COS + CDN [OK] | 云开发存储 [OK] | |
| 6 | QR generation | ? | — | SCF [OK] | 小程序 [OK] | |
| 7 | QR verification surface | ? | — | COS + API Gateway [OK] | 小程序扫码 [OK] | |
| 8 | Blockchain anchoring | ? | — | CVM (run TrueChain node) [OK] | — | |
| 9 | Identity / keypairs | ? | — | KMS [OK] | 微信登录 OpenID [OK] | |
| 10 | Notarization storage | ? | — | COS [OK] | 云开发存储 [OK] | |
| 11 | Event submission API | ? | — | SCF + API Gateway [OK] | 云函数 [OK] | |
| 12 | Domain + ICP | ? | — | 腾讯云备案 [OK] | — | |
| 13 | Comms | ? | — | — | 企业微信 / 微信 [OK] | |
| 14 | Monitoring | ? | — | 云监控 [OK] | 小程序运维 [PARTIAL] | |

---

## 4. Deliverable format

For each of the 14 rows, fill:

- **Status** — works / partial / missing
- **Evidence** — test result, screenshot, doc link
- **Recommendation** — adopt / mirror / rebuild + the specific platform

**File:** one MD report `china/CHINA_ECOSYSTEM_MAPPINGS_REPORT.md` in this repo.
**Due:** before the in-office review.

---

## 5. How to test (quick guide)

- **GitHub:** try `git clone`, `raw.githubusercontent.com`, `api.github.com` — record reachable / slow / blocked.
- **Gitee:** create org, test push/pull, enable Gitee Go on a test repo, check free-tier limits.
- **Tencent Cloud:** register, check CODING, CloudBase free tier, COS bucket + CDN, SCF, ICP 备案 process & timeline.
- **WeChat:** mini-program dev account, 扫码 API, 云开发 (WeChat Cloud Development).

---

## 6. In-office review agenda (day after tomorrow)

1. Walk each of the 14 rows.
2. Decide per capability: **采用 / 镜像 / 重建**.
3. Sign off the China target architecture.
4. Assign next actions (Gitee mirror setup, CloudBase scaffold, mini-program spec).
5. Confirm pilot scope with Liz (textiles / electronics / agro).

---

*Draft v0.1 — internal task brief. All Gitee / Tencent / WeChat capability cells are pre-filled from public knowledge and MUST be verified with real accounts.*
