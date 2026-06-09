# Beta Sandbox Endpoint (`beta.edgar.truesight.me`) — implementation plan + execution roadmap

**Goal:** Stand up a persistent, **isolated** beta **dao_protocol** instance on its
own NELANCO EC2 box at **`beta.edgar.truesight.me`**, wired to **Stripe test mode**,
so beta checkouts — and **Sophia, headlessly** — can run true end-to-end
subscription tests (subscribe → test charge → webhook → fulfillment queue) without
touching prod or charging a real card. This is the piece that unblocks
**Phase 2 E2E testing** of `CHOCOLATE_SUBSCRIPTION_PLAN.md` and any future
Stripe-touching work.

> ## ▶ RESUME HERE
>
> **▶ ACTIVE: Unit 1 — provision the NELANCO EC2 box.** Nothing built yet (plan
> written 2026-06-09). Start at the **Pre-flight checklist** (RunInstances dry-run
> + Stripe test keys + SANDBOX sheet), then Unit 1.
>
> **🛑 Where to STOP (operator gates):** Sophia builds + opens PRs with green CI +
> an Operator Test Runbook, but **STOPS** at: (a) **provisioning approval** before
> `RunInstances` (a real billable box), (b) the **Stripe-dashboard steps** (test
> keys + register the test webhook — operator-only), and (c) **prod Rails
> delegation deploy** (touches prod Edgar). She does the headless infra/code/test
> in between. **Unit 8 is mandatory: update `AWS_DIGITAL_INFRASTRUCTURE.md`** so
> the new box never slips through the cracks.

**Companion docs:** `CHOCOLATE_SUBSCRIPTION_PLAN.md` (the feature this unblocks;
its Phase-2 webhook moves to dao_protocol here), `AWS_DIGITAL_INFRASTRUCTURE.md`
(fleet inventory — Unit 8 updates it), `STRIPE_LEDGER_ROUTING.md` (the 5 Stripe
flows + the Rails→dao_protocol delegation pattern, PR6b), `EDGAR_DAO_EXTRACTION_PLAN.md`
(decision A — `/stripe_webhook` entry stays on Rails; we *delegate* sub events),
`project_ec2_sg_remediation` (do NOT replicate the world-open default SG).

---

## Decisions (ratified with Gary, 2026-06-09)

| # | Decision |
|---|----------|
| Host | **Its own standalone EC2 box** (not co-located on `dao_protocol_nelanco`). Isolation matters because **Sophia drives it autonomously** — zero blast radius into prod Edgar/treasury. |
| Account / region | **NELANCO = AWS account `767697632458`**, `us-east-1`, IAM user `truesight_dao_autopilot`. Creds: **`AWS_ACCESS_KEY_ID_NELANCO` / `AWS_SECRET_ACCESS_KEY_NELANCO` / `AWS_REGION_NELANCO`** in `truesight_autopilot/.env` (mirrored on the prod box). NELANCO unblock confirmed (sts + EC2 read verified 2026-06-09). |
| Uptime | **Always-on** (small instance, e.g. `t3.small`). Elastic IP so DNS is stable. |
| Stack | **Lightweight beta `dao_protocol`** (Python/FastAPI), NOT a beta Rails Edgar. |
| Mode | `DAO_PROTOCOL_ENVIRONMENT=development` + **Stripe TEST key**; rows labelled **SANDBOX**. A code **`sk_live` guard** refuses a live key when `environment=development`. |
| Webhook | The chocolate-subscription webhook handler **moves into dao_protocol** (so beta is lightweight + Sophia-testable). **Prod:** Rails `/stripe_webhook` stays the shared entry and **delegates** the sub events to (prod) dao_protocol — the PR6b pattern. **Beta:** the Stripe **test** webhook points **directly** at `beta.edgar.truesight.me` (no Rails). |
| Data isolation | A separate **SANDBOX fulfillment-queue** sheet/tab — test rows never mix with prod. |
| Inventory | **Sophia MUST update `AWS_DIGITAL_INFRASTRUCTURE.md`** with the new box (Unit 8) — non-negotiable. |

---

## Pre-flight checklist (verify BEFORE provisioning)

- [ ] **RunInstances permission** — `aws ec2 run-instances --dry-run` with the
      NELANCO creds returns `DryRunOperation` (not `UnauthorizedOperation`). Read
      access already confirmed (sts OK, `describe-instances` = 15). Write/launch is
      the unverified bit.
- [ ] **Route53 access** — confirm a hosted zone for `truesight.me` (or `edgar.truesight.me`)
      in NELANCO and `ChangeResourceRecordSets` permission for the A record.
- [ ] **Instance shape + AMI** — `t3.small`, Ubuntu LTS AMI id for `us-east-1`;
      subnet/VPC chosen.
- [ ] **Locked-down SG** — create a NEW security group: **443** (Stripe webhook +
      site) open; **22** restricted to operator/Tailscale IPs. **Do NOT** reuse the
      world-open default SG the remediation project flagged on the 16 prod boxes.
- [ ] **Keypair** — beta box gets its own key (mint a beta key or reuse
      `~/.ssh/agentic_ai_github/id_ed25519`); record where it lives (never commit).
- [ ] **Stripe TEST creds (operator-gated)** — `sk_test_…` secret key + the test
      webhook signing secret, from the Stripe dashboard (test mode).
- [ ] **Google SA for the SANDBOX sheet** — confirm a service account can write the
      new SANDBOX tab (reuse `agroverse-qr-code-manager@…` or a test SA).
- [ ] **dao_protocol deploy story on a fresh box** — `requirements-server.txt`,
      systemd unit, the box's own `.env` (test keys + SANDBOX ids).

---

## Architecture

```
beta.agroverse.shop /subscribe/...  (GAS environment=development → Stripe TEST)
        │  test-card subscription (hosted, or via Stripe API for Sophia)
        ▼
Stripe (TEST mode)
        │  invoice.paid / checkout.session.completed (TEST webhook)
        ▼
beta.edgar.truesight.me  (Route53 + EIP → nginx :443 + Let's Encrypt)
        │
        ▼
beta dao_protocol  (systemd, :8010, DAO_PROTOCOL_ENVIRONMENT=development,
   Stripe TEST key, sk_live guard)  → subscription webhook handler
        ▼
SANDBOX fulfillment-queue sheet  (isolated test rows)

PROD (unchanged): Rails /stripe_webhook (shared entry) → delegates sub events
   → prod dao_protocol → prod fulfillment queue.   Live keys, PRODUCTION rows.
```

---

## Execution roadmap (resume tracker)

Legend: ☐ todo · ⧗ in progress · ☑ done · 🛑 operator gate

**Protocol:** Sophia builds each unit with green CI + an **Operator Test Runbook**
in the PR body; **opens PRs, never merges/promotes**; STOPS at the 🛑 gates.

| Unit | Scope | Repo / target | Status |
|------|-------|---------------|--------|
| **0** | This plan (the baton) | `agentic_ai_context` | ☑ |
| **1 🛑** | **Provision** the EC2 (adapt `truesight_autopilot/scripts/launch_ec2.sh`: NELANCO creds, `t3.small`, locked-down SG, tags `Service=dao-protocol-beta`), allocate **EIP**, base packages, Python venv, **nginx + Let's Encrypt** TLS. **Gate:** operator approves the billable `RunInstances`. | NELANCO EC2 | ☐ |
| **2** | **Route53** A record `beta.edgar.truesight.me` → EIP; verify HTTPS reachable. | Route53 | ☐ |
| **3** | **Deploy beta dao_protocol** — clone `dao_protocol` (dao_client repo), `requirements-server.txt`, systemd unit `dao-protocol-beta`, nginx `:443 → 127.0.0.1:8010`. Box `.env`: `DAO_PROTOCOL_ENVIRONMENT=development`, `DAO_PROTOCOL_STRIPE_SECRET_KEY=sk_test_…`, SANDBOX sheet id, test webhook secret. | box | ☐ |
| **4** | **Code: env guard** — in `dao_protocol` config/`stripe_client`, refuse a `sk_live_` key when `environment=development` (fail closed); confirm SANDBOX labeling. + green CI + OTR. | `dao_protocol` | ☐ |
| **5** | **Code: subscription webhook handler in dao_protocol** — `invoice.paid` + first `checkout.session.completed` → SANDBOX fulfillment-queue row, idempotent on invoice id; lifecycle (`payment_failed`/`subscription.deleted`/refund) per `CHOCOLATE_SUBSCRIPTION_PLAN.md` PR2.2. + tests. | `dao_protocol` | ☐ |
| **6 🛑** | **Prod Rails delegation** — extend `sentiment_importer` `/stripe_webhook` to delegate sub `invoice.paid` to (prod) dao_protocol (PR6b pattern). **Gate:** operator deploys (touches prod Edgar). | `sentiment_importer` | ☐ |
| **7 🛑** | **Stripe TEST webhook** — register `https://beta.edgar.truesight.me/stripe_webhook` in Stripe **test** mode; store signing secret on the box. **Gate:** Stripe-dashboard step (operator), or Sophia via Stripe API if test key provisioned. | Stripe | ☐ |
| **8** | **Update `AWS_DIGITAL_INFRASTRUCTURE.md`** — add the box to the fleet inventory: instance id, EIP, region/account (`767697632458`/`us-east-1`), role (dao-protocol-beta / sandbox), systemd unit, subdomain, SG id, creds reference (`AWS_*_NELANCO`). **Mandatory — do not skip.** | `agentic_ai_context` | ☐ |
| **9** | **Headless E2E test (Sophia-runnable)** — script: create test customer + `pm_card_visa` + subscription via Stripe **test API** → Stripe delivers `invoice.paid` to the beta endpoint → assert the SANDBOX queue row. Document as the canonical Sophia E2E. | `dao_protocol` | ☐ |
| **10** | **Update `CHOCOLATE_SUBSCRIPTION_PLAN.md` Phase 2** — point PR2.2 webhook at dao_protocol (beta-tested here); note prod Rails delegation. | `agentic_ai_context` | ☐ |

> **🛑 STOP gates summary:** Unit 1 (approve billable launch), Unit 6 (prod Edgar
> deploy), Unit 7 (Stripe dashboard). Everything else Sophia does headlessly.

---

## Risks / open items

- **Cost** — always-on `t3.small` ≈ $15/mo. Acceptable for a shared sandbox;
  revisit if idle.
- **SG hygiene** — the new box must ship a **scoped** SG (443 + restricted 22),
  explicitly not the world-open default flagged in `project_ec2_sg_remediation`.
- **Secret sprawl** — beta box holds only **test** Stripe keys + a SANDBOX SA;
  the `sk_live` guard (Unit 4) is the backstop against a misconfig charging real
  cards.
- **Plan coupling** — Unit 5/6 move the subscription webhook to dao_protocol,
  changing `CHOCOLATE_SUBSCRIPTION_PLAN.md` Phase 2 (Unit 10 keeps them in sync).
- **Inventory drift** — Unit 8 is the guard; if skipped, the box becomes shadow
  infra. Mandatory.

---

*Plan owner: this doc. Update the resume tracker as each unit lands; report the DAO
contribution before starting the next.*
