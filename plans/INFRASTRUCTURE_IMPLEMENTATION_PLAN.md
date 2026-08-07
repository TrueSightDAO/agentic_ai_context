# TrueSight DAO — Infrastructure Implementation Plan

**From Cafe Strategy Session, July 2025**

Gary is handing off ops/sales/marketing to focus on digital infrastructure. This plan sequences the 9 workstreams identified in the cafe/dinner strategy session into a phased implementation timeline.

**North Star:** Build the operating system for regenerative commerce — where any regenerative producer can plug in, get QR-coded inventory, track sales, and have proceeds automatically flow to tree planting.

---

## Phase 0: Foundation (Weeks 1-2)

### 0.1 — Ops Hire Job Description
**Effort:** 2-3 hours | **Owner:** Sophia drafts, Gary reviews

- Draft role scope: day-to-day coordination Sophia cannot handle (physical logistics, farmer relationships, warehouse coordination, customer support)
- List specific tasks currently falling through cracks
- Suggest posting channels (Beer Hall, LinkedIn, impact-jobs boards)
- **Deliverable:** Published JD in agentic_ai_context

### 0.2 — Gary Handoff: Role Boundaries
**Effort:** 1 hour | **Owner:** Gary + Sophia

- Update OPERATING_INSTRUCTIONS.md to reflect new role boundaries
- Define escalation paths: ops questions → ops hire (once hired), sales channel → Liz, digital infra → Gary
- **Deliverable:** Updated operating instructions

### 0.3 — SKU Registry Design (Foundation)
**Effort:** 4-6 hours | **Owner:** Sophia

- Design the generic SKU registry schema
- Define fields: name, category, material_composition (JSON), unit_cost, default_price, tree_planting_allocation_pct, manager, is_white_label, parent_sku
- Design ledger template for auto-instantiation
- **Deliverable:** SKU registry schema doc + GAS design

---

## Phase 1: SKU Infrastructure (Weeks 3-5)

### 1.1 — Edgar SKU Onboarding Endpoint
**Effort:** 6-8 hours | **Owner:** Sophia

- Build `POST /dao/register_sku` endpoint on Edgar
- Fields: name, category, material_composition, unit_cost, tree_planting_allocation_pct, manager
- Validate and return SKU ID
- Update Edgar API docs
- **Deliverable:** Working SKU registration endpoint

### 1.2 — Dynamic Ledger Instantiation
**Effort:** 4-6 hours | **Owner:** Sophia

- Build GAS function `createSkuLedger(skuName)` that duplicates a template sheet
- Wire into SKU registration flow
- Columns: QR Code, Status, Manager, Sale Price, Tree Planting Allocation, Date Sold
- **Deliverable:** Auto-created ledger per new SKU

### 1.3 — Material Composition Recording
**Effort:** 2-3 hours | **Owner:** Sophia

- Add material_composition JSON column to SKU registry
- Define schema: `{"cacao": 0.7, "coconut_sugar": 0.15, "packaging": 0.1}`
- Expose via Edgar API for QR code lookup transparency
- **Deliverable:** Material composition visible on SKU records

### 1.4 — QR Code Namespace per SKU
**Effort:** 2-3 hours | **Owner:** Sophia

- Update AGROVERSE_QR_CODE_BATCH_GENERATION.md to accept `sku` parameter
- QR codes become namespaced: `2025SKUNAME_20260721_001`
- Update batch compiler to handle multiple SKU namespaces
- **Deliverable:** SKU-specific QR code batches

---

## Phase 2: Brand Onboarding (Weeks 5-6)

### 2.1 — Brand Onboarding Protocol
**Effort:** 4-6 hours | **Owner:** Sophia

- Create BRAND_ONBOARDING_PROTOCOL.md in agentic_ai_context
- Define what info Sophia needs from brand owners
- Document how to register SKU, submit inventory movements, submit sales
- Include common error states and resolutions
- **Deliverable:** Published onboarding protocol

### 2.2 — Sophia as Brand Interface
**Effort:** 3-4 hours | **Owner:** Sophia

- Ensure `submit_contribution` tool accepts `on_behalf_of` / `brand` parameter
- Test end-to-end flow with simulated brand owner
- Document the flow for future sessions
- **Deliverable:** Sophia can onboard brands independently

---

## Phase 3: White-Label & Revenue (Weeks 6-8)

### 3.1 — White-Label Chocolate Infrastructure
**Effort:** 6-8 hours | **Owner:** Sophia

- Design white-label SKU model: base product + custom branding overlay
- Add fields to SKU registry: is_white_label, parent_sku, branding_asset_url, minimum_order_qty
- Build white-label order flow: company selects base → uploads logo → Sophia creates SKU → QR codes with custom metadata
- Wire to Stripe for bulk corporate orders (invoice flow)
- **Deliverable:** Working white-label order pipeline

### 3.2 — White-Label Documentation
**Effort:** 2 hours | **Owner:** Sophia

- Create WHITE_LABEL_CHOCOLATE_PLAN.md
- Document pricing model, minimums, lead times
- Create corporate one-pager for outreach
- **Deliverable:** Published white-label docs

---

## Phase 4: Non-Profit & Tax Layer (Weeks 8-12)

### 4.1 — Non-Profit Vehicle Research
**Effort:** 4-6 hours | **Owner:** Sophia researches, Gary decides

- Research options: existing 501(c)(3) partner vs. new entity vs. fiscal sponsorship
- Compare costs, timelines, compliance requirements
- Interview 2-3 potential fiscal sponsors
- **Deliverable:** Recommendation memo

### 4.2 — Tree-Gifting Ledger
**Effort:** 4-6 hours | **Owner:** Sophia

- Design tree-gifting ledger: track which trees are gifted, to whom, under which corporate donation
- Integrate with SunMint tree planting data
- QR code on chocolate bar links to tree certificate
- **Deliverable:** Working tree-gifting tracking system

### 4.3 — Corporate Donation Flow
**Effort:** 6-8 hours | **Owner:** Sophia + Gary

- Build end-to-end flow: company pays → non-profit issues tax receipt → tree planted in employee's name → QR code links to certificate
- Wire to Stripe with tax receipt generation
- **Deliverable:** Complete corporate gifting pipeline

---

## Phase 5: Scale & Distribution (Weeks 12+)

### 5.1 — Channel Distribution Readiness Gate
**Effort:** 3-4 hours | **Owner:** Sophia

- Define readiness metrics: inventory levels, fulfillment cycle time, pending orders
- Build simple dashboard showing these metrics
- Document threshold where Liz's channel push becomes safe
- **Deliverable:** Distribution readiness dashboard

### 5.2 — Liz Channel Distribution Enablement
**Effort:** Ongoing | **Owner:** Liz (sales) + Sophia (data)

- Once supply chain is stable, enable channel distribution partners
- Sophia provides real-time inventory and fulfillment data
- **Deliverable:** Channel partner onboarding flow

---

## Timeline Summary

```
Week 1-2   ████████░░░░░░░░░░░░  Phase 0: Foundation (ops hire JD, role boundaries, SKU design)
Week 3-5   ██████████████░░░░░░  Phase 1: SKU Infrastructure (Edgar endpoint, ledgers, QR)
Week 5-6   ██████████████████░░  Phase 2: Brand Onboarding (protocol, Sophia interface)
Week 6-8   ████████████████████  Phase 3: White-Label (infrastructure, docs)
Week 8-12  ████████████████████  Phase 4: Non-Profit (research, tree-gifting, corporate flow)
Week 12+   ████████████████████  Phase 5: Scale (distribution gate, channel enablement)
```

---

## Dependency Map

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5
  │            │            │            │            │
  │            ├── 1.1 SKU Endpoint     │            │
  │            ├── 1.2 Dynamic Ledgers  │            │
  │            ├── 1.3 Material Comp    │            │
  │            └── 1.4 QR Namespace     │            │
  │                                     │            │
  │                     2.1 Protocol ───┤            │
  │                     2.2 Interface ──┘            │
  │                                                  │
  │                                   3.1 White-Label┤
  │                                   3.2 Docs ──────┤
  │                                                   │
  │                                    4.1 Research ──┤
  │                                    4.2 Tree-Gift ─┤
  │                                    4.3 Corp Flow ─┘
  │
  └── 0.1 Ops Hire (parallel) ──► 5.1 Distribution Gate ──► 5.2 Channel Enablement
```

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Ops hire takes >4 weeks to find | High | Medium | Start hiring immediately; Sophia handles more coordination in interim |
| SKU registry scope creep | Medium | Medium | Ship minimal viable SKU registry first, iterate |
| Non-profit legal complexity | Medium | High | Start research early; fiscal sponsorship is fastest path |
| White-label demand doesn't materialize | Low | Low | Build infrastructure is low-cost; validate with 1-2 pilot partners first |
| Supply chain can't keep up with channel distribution | Medium | High | Build readiness dashboard; gate channel push on metrics |

---

## Quick Start

**Immediate next steps (this week):**

1. **Sophia** drafts the ops hire JD → Gary reviews
2. **Sophia** designs the SKU registry schema → Gary approves
3. **Gary** updates OPERATING_INSTRUCTIONS.md with new role boundaries
4. **Sophia** begins Phase 1.1 (Edgar SKU endpoint) in parallel

*"Build the machine that onboards them automatically — that's 10x more valuable than onboarding them one by one."*