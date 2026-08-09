# Deployment Architecture Framework — TrueSight DAO (Global) + China Cluster
# 部署架构框架 —— TrueSight DAO（全球） + 中国集群（待调研）

**Status: Framework v1.** China-side cells are intentionally blank pending investigation with the China team (Luca).

---

## 1. Purpose / 目的

This framework maps how each deployment is (or will be) run, across two tracks:

- **Track A — Global (TrueSight DAO) / 全球主栈:** AWS + Google Apps Script + GitHub Actions + GitHub Pages. Fully described in `AWS_DIGITAL_INFRASTRUCTURE.md`.
- **Track B — China cluster / 中国独立集群:** a standalone cluster serving **raw materials & manufacturers** (原材料与制造商). Google services (Apps Script, Google Sheets) are **not accessible in China**, so those layers are left **blank by design** until investigation fills them.

---

## 2. How to use / 使用方式

- Cells marked **[FILL IN]** are open questions for the China-side investigation.
- Cells marked **BLANK — Google unavailable in China** are intentionally empty: the global implementation uses Google services blocked in China; a replacement is required but not yet chosen.
- Track A cells are references (not exhaustive) — full detail lives in the infra doc.

---

## 3. Architecture layer framework / 分层对照框架

| Layer 层 | Track A — Global 全球（现状） | Track B — China 中国（待调研） |
|---|---|---|
| Cloud hosting 云托管 | AWS EC2 — Explorya (440626669078) + Nelanco (767697632458) | **[FILL IN]** 阿里云 / 腾讯云 / 自建？ |
| Reverse proxy / ingress 反向代理 | krake_nginx (t2.micro) — HTTPS 终止 | **[FILL IN]** |
| DAO API / submission 事件入口 | Edgar dao_protocol (FastAPI) :8010 + Perch (Rails) :3002 | **[FILL IN]** 独立提交端点？ |
| Background workers 后台任务 | Sidekiq (seni_sk_auto ASG ×2) | **[FILL IN]** |
| Database 数据库 | PostgreSQL seni_sql_2026 | **[FILL IN]** |
| Cache / queue 缓存与队列 | Redis seni_redis_2 | **[FILL IN]** |
| Ledger / record-keeping 账本 | Google Sheets via Google Apps Script | **BLANK — Google 不可用** **[FILL IN]** 本地 DB / ERP？ |
| Automation / webhooks 自动化与钩子 | GAS webhooks (WebhookTriggerWorker 等) | **BLANK — Google 不可用** **[FILL IN]** |
| Raw-material lots 原材料批次 | — (GAS/Sheets) | **BLANK — Google 不可用** **[FILL IN]** 如何记录批次？ |
| Manufacturer onboarding 制造商入驻 | — (GAS/Sheets + 邮箱验证) | **BLANK — Google 不可用** **[FILL IN]** |
| CI/CD | GitHub Actions（每周 AMI 快照、安全仪表盘） | **[FILL IN / VERIFY]** GitHub 在中国可用但需验证速度/镜像 |
| Source control 源码 | GitHub repos (TrueSightDAO) | **[FILL IN]** Gitee 镜像？ |
| Static sites 静态站点 | GitHub Pages | **[FILL IN]** |
| DNS / domains 域名 | Route53 (truesight.me) | **[FILL IN]** 需 ICP 备案 |
| Secrets 密钥 | ~/dao_protocol/.env (chmod 600); GitHub Secrets | **[FILL IN]** |
| Monitoring 监控 | Monit + health endpoints + security dashboard | **[FILL IN]** |
| Backup 备份 | 每周 AMI 快照（GitHub Action） | **[FILL IN]** |

---

## 4. Service-by-service framework / 逐服务框架

For each service: role → global deployment → China equivalent → open questions.

| # | Service 服务 | Global 全球 (Track A) | China 中国 (Track B) | Open questions 待确认 |
|---|---|---|---|---|
| 1 | DAO 事件提交 | dao_protocol FastAPI :8010 (`POST /dao/submit_contribution`) | **[FILL IN]** | 中国集群是否运行独立提交端点？与全球账本如何同步？ |
| 2 | 原材料批次记录 | Google Sheets (via GAS) — CN 不可用 | **BLANK — Google 不可用** | 现有手工流程？数据模型？ |
| 3 | 制造商入驻 | GAS 邮箱验证 + contributor add | **BLANK — Google 不可用** | 入驻流程？合规要求？ |
| 4 | 库存 / QR 码 | qr_codes repo + agroverse-inventory ledgers | **[FILL IN]** | QR 标准是否沿用？批次命名？ |
| 5 | 支付 | Stripe sync (GAS proxy) | **[FILL IN]** | 支付宝 / 微信支付？ |
| 6 | 通知 / 消息 | Telegram bot (Sophia) + GAS webhook | **[FILL IN]** | 微信 / 钉钉 / 企业微信？ |
| 7 | 邮件 | Gmail (OAuth) | **[FILL IN]** | 网易 / 腾讯企业邮？ |

---

## 5. China-side investigation checklist / 中国侧调研清单

1. **云厂商与地域**：阿里云 / 腾讯云 / 华为云 / 自建机房？ICP 备案状态？
2. **GitHub 可用性**：GitHub Actions / Pages 在中国可用但可能受限 — 需要镜像（Gitee）或自托管 runner？
3. **账本替代**：Google Sheets 被封锁 — 用什么记账？PostgreSQL？ERP？本地应用？
4. **原材料批次现状**：目前如何记录批次 / 供应商 / 制造商？
5. **数据连通**：中国集群与全球 DAO 的关系 — 独立账本 or 定期同步？数据合规 / 隐私边界？
6. **域名与备案**：任何公网端点都需要 ICP 备案
7. **监控告警**：等价物（云监控 / Prometheus？）
8. **密钥管理**：等价物（云 KMS / Vault？）
9. **备份策略**：等价物
10. **团队分工**：谁负责中国集群运维 / 部署？

---

## 6. Blank-by-design sections / 刻意留空的原因

| Section 章节 | Global implementation 全球实现 | Why blank for China 为何留空 |
|---|---|---|
| Google Apps Script | 事件处理、webhook 分发、库存快照 | Google 服务在中国不可用；替代方案待调研 |
| Google Sheets ledger | 账本、贡献者、库存记录 | 同上 |
| Gmail | 邮箱验证、通知 | 同上（待调研替代） |
| GitHub Pages | 前端静态站点 | 可用但受限；镜像方案待调研 |
| Stripe | 支付 | 在中国不运营；支付宝 / 微信待调研 |

---

## 7. Next steps / 下一步

1. 与 Luca 对齐本框架 — 确认中国侧部署形态（独立集群假设）
2. 填写第 5 节调研清单
3. 每完成一项 → 回填对应 **[FILL IN]** 单元格
4. 框架更新通过 PR 提交到 `agentic_ai_context/infrastructure/`
