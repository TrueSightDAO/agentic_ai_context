# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** Friday Tech Fest signals + SVH Capital cacao circle on June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## 1. Executive Summary

The convergence is accelerating. Nora (Kopi Bar, Berkeley) is onboarding. More partners are joining. Matheus channels exports through his private Brazilian entity. TrueTech Inc (Delaware C-corp) is the importing entity. Gary's personal bank account collects funds. This worked at pilot scale (~$15K cumulative sales), but the signal is clear: **the tax-write-off infrastructure in the USA jurisdiction is turning from grey to red.**

Three structural options emerged from Tech Fest:

| Option | Jurisdiction | Structure | Best For |
|--------|-------------|-----------|----------|
| **DUNA** | Wyoming, USA | Decentralized Unincorporated Nonprofit Association | DAO legal wrapper, nonprofit mission alignment, member liability protection |
| **Prospera / Wyoming DAO LLC** | Wyoming, USA | For-profit DAO LLC | Tokenized revenue sharing, profit distributions to members |
| **Brazilian CNPJ (LTDA)** | Brazil | Limited liability company | Local export entity, cacao sourcing, Brazilian tax compliance |

**Recommendation:** A **three-entity stack** — Wyoming DUNA (DAO wrapper) → TrueTech Inc (US import/distribution) → Brazilian LTDA (export/sourcing) — with a clear inter-entity agreement for fund flows, carbon credit rights, and tax-advantaged donations.

---

## 2. Current State Assessment

### 2.1 Financial Flows (Current)

```
Brazil Farmers → Matheus (private CNPJ) → Export → TrueTech Inc (DE C-corp) → Gary's personal bank account → DAO treasury / expenses
```

**Risks in current flow:**

| Risk | Severity | Detail |
|------|----------|--------|
| Personal liability | 🔴 High | Gary's personal account commingles DAO funds with personal funds |
| Tax reporting complexity | 🟡 Medium | C-corp filing + personal income + potential partnership tax treatment |
| No member liability shield | 🔴 High | Token holders could be treated as general partners (per Ooki DAO precedent) |
| No tax-advantaged donation pathway | 🟡 Medium | Impact funds and retail donors (Nora's customers) have no tax-deductible channel |
| Brazil export compliance | 🟡 Medium | Matheus's private entity bears all Brazilian compliance burden |

### 2.2 Current Ledger Snapshot

- **Cumulative sales (all time):** ~$15,736 USD
- **Monthly run rate (2026):** ~$500-1,100/month trending up
- **USD Treasury Balance:** ~$14,622
- **AUM:** ~$28,144
- **Physical assets on ledger:** ~$14,622 across 25+ asset types
- **Partners:** Nora (Kopi Bar), Kirsten, Matheus, Edge & Node, Shuar Design Boutique, and growing

### 2.3 Nora's Use Case (Catalyst)

Nora wants to channel a portion of **each cup of cacao sold at Kopi Bar** to rainforest restoration. For this to work as a **tax write-off for her business**, the receiving entity must be a **qualified 501(c)(3) nonprofit** or equivalent. A for-profit C-corp (TrueTech Inc) cannot issue tax-deductible receipts. This is the key signal pushing the tax infrastructure from grey to red.

---

## 3. Option Analysis

### 3.1 Option A: Wyoming DUNA (Decentralized Unincorporated Nonprofit Association)

**What it is:** A Wyoming-specific legal entity designed for DAOs. Nonprofit by statute — cannot distribute profits to members. Took effect July 1, 2024. Already adopted by Nouns DAO and Uniswap governance.

| Dimension | Detail |
|-----------|--------|
| **Liability** | Members shielded from personal liability for DAO obligations |
| **Tax status** | Nonprofit entity; can apply for 501(c)(3) tax-exempt status with IRS |
| **Governance** | Smart contract-based voting explicitly recognized by law |
| **Minimum members** | 100 members required |
| **Profit distribution** | ❌ Not allowed — all revenue must be reinvested in mission |
| **Formation cost** | $100 state filing + $20K-$60K legal fees |
| **Annual cost** | $60-$200 license tax; no Wyoming state income tax |
| **Bank account** | Can open US bank account with EIN |
| **Time to form** | 4-8 weeks |

**✅ Pros:**
- Perfect mission alignment (nonprofit, rainforest restoration)
- Nora's customers can get tax-deductible receipts (if 501(c)(3) obtained)
- Impact funds can write tax-deductible checks
- Legal recognition of on-chain governance
- No state income tax (Wyoming)

**❌ Cons:**
- Cannot distribute profits to TDG token holders
- 100-member minimum (we may not have 100 verified DAO members yet)
- IRS 501(c)(3) application is a separate, lengthy process (6-12 months)
- Higher legal fees than a simple LLC
- US nexus exposes DAO to US jurisdiction

### 3.2 Option B: Wyoming DAO LLC (For-Profit)

**What it is:** A Wyoming LLC with a "DAO" designation under the Wyoming DAO Supplement Act (2021). For-profit structure.

| Dimension | Detail |
|-----------|--------|
| **Liability** | Full LLC liability protection for members |
| **Tax status** | Pass-through taxation (default); can elect C-corp or S-corp |
| **Governance** | Smart contract governance allowed |
| **Minimum members** | None |
| **Profit distribution** | ✅ Allowed — can distribute to token holders |
| **Formation cost** | $100 state filing + $15K-$50K legal fees |
| **Annual cost** | $60-$200 license tax; no Wyoming state income tax |
| **Bank account** | Can open US bank account with EIN |

**✅ Pros:**
- Can distribute profits to TDG holders (aligns with tokenomics)
- No minimum membership requirement
- Lower legal fees than DUNA
- Pass-through taxation avoids double taxation

**❌ Cons:**
- ❌ Cannot issue tax-deductible receipts (not a nonprofit)
- Nora's customers cannot get tax write-offs
- Impact funds cannot write tax-deductible checks
- Less mission-aligned than DUNA

### 3.3 Option C: Brazilian CNPJ (LTDA)

**What it is:** A Brazilian limited liability company (LTDA) — the most common structure for foreign-owned businesses in Brazil. 100% foreign ownership allowed.

| Dimension | Detail |
|-----------|--------|
| **Liability** | Limited liability for shareholders |
| **Tax status** | Brazilian corporate taxes (IRPJ, CSLL, PIS, COFINS, ICMS) |
| **Foreign ownership** | 100% allowed for most sectors |
| **Formation cost** | $1,000-$3,000 (legal + registration) |
| **Annual cost** | $500-$2,000 (accounting + compliance) |
| **Time to form** | 4-8 weeks (bureaucratic) |

**✅ Pros:**
- Formalizes Matheus's export operations
- Brazilian tax compliance for cacao sourcing
- Can issue Brazilian tax receipts (NF-e)
- Enables direct contracting with Brazilian farmers

**❌ Cons:**
- Bureaucratic formation process
- Ongoing compliance burden (Brazilian tax complexity)
- Requires local Brazilian legal representative
- Does not solve US tax-deduction problem

### 3.4 Option D: TrueTech Inc — Dedicated Bank Account (Interim)

**What it is:** Keep TrueTech Inc (Delaware C-corp) as the importing entity but open a dedicated business checking account. This is the **minimum viable fix** for the immediate commingling risk.

| Dimension | Detail |
|-----------|--------|
| **Cost** | $0-$500 (bank account setup) |
| **Time** | 1-2 weeks |
| **Risk reduction** | Separates personal from business funds |
| **Tax deduction** | ❌ Still cannot issue tax-deductible receipts |

---

## 4. Recommended Structure: Three-Entity Stack

### 4.1 The Stack

```
┌─────────────────────────────────────────────────────┐
│               Wyoming DUNA (DAO Wrapper)              │
│  • Legal entity for TrueSight DAO                    │
│  • Holds governance / IP / brand                     │
│  • Applies for 501(c)(3) status                      │
│  • Issues tax-deductible receipts                    │
│  • Owns carbon credit rights                          │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ Service Agreement / License
                       ▼
┌─────────────────────────────────────────────────────┐
│            TrueTech Inc (Delaware C-Corp)             │
│  • US import & distribution entity                   │
│  • Holds inventory (US-side)                         │
│  • Processes retail sales (agroverse.shop)           │
│  • Pays royalties/license fees to DUNA               │
│  • Dedicated business bank account ✓                 │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ Inter-company agreement
                       ▼
┌─────────────────────────────────────────────────────┐
│         Brazilian LTDA (CNPJ) — Export Entity         │
│  • Owned by TrueTech Inc or DUNA                     │
│  • Contracts directly with farmers                   │
│  • Handles Brazilian export compliance               │
│  • Issues NF-e tax receipts                          │
│  • Manages Brazil-side inventory                     │
└─────────────────────────────────────────────────────┘
```

### 4.2 How Money Flows (Proposed)

```
Farmers → Brazilian LTDA (pays farmers, handles Brazil taxes)
   → Exports cacao → TrueTech Inc (imports, pays duties, holds US inventory)
      → Sells to: 
         • Retail (agroverse.shop) → revenue stays in TrueTech
         • Wholesale partners (Kopi Bar, etc.) → revenue stays in TrueTech
      → TrueTech pays license fee / royalty to DUNA
         → DUNA funds rainforest restoration
            → Issues tax-deductible receipts to donors

Nora's customers: Buy cacao at Kopi Bar
   → Nora donates portion to DUNA (tax-deductible for her business)
   → DUNA plants trees → carbon credits → DUNA treasury
```

### 4.3 Carbon Credit & Tree-Planting Flow

Nora's "per cup → plant a tree" model works cleanly with this stack:

1. Kopi Bar sells a cup of cacao
2. Nora transfers $X per cup to the **DUNA** (not to TrueTech Inc)
3. DUNA issues a **tax-deductible receipt** to Kopi Bar LLC
4. DUNA funds tree planting in the Amazon (via existing sunmint / lineage-credentials pipeline)
5. Carbon credits generated → held by DUNA → can be sold to impact funds
6. Impact funds get tax write-offs + verified carbon offsets

### 4.4 Impact Fund Compatibility

Progressive Ventures' managing partner mentioned impact funds seek tax write-offs. With a DUNA + 501(c)(3):

- Impact funds can make **tax-deductible donations** (not equity investments)
- Funds can also purchase **carbon credits** from the DUNA at market rates
- Dual pathway: charitable donation + carbon offset purchase

---

## 5. Phased Implementation Roadmap

### Phase 0: Immediate (1-2 weeks) — $0-$500

| Action | Cost | Priority |
|--------|------|----------|
| Open dedicated business checking account for TrueTech Inc | $0-$500 | 🔴 Critical |
| Stop commingling DAO funds with personal accounts | $0 | 🔴 Critical |
| Document current fund flows in a simple spreadsheet | $0 | 🟡 Medium |

### Phase 1: Short-term (1-3 months) — $15K-$60K

| Action | Cost | Priority |
|--------|------|----------|
| Form Wyoming DUNA (legal counsel) | $20K-$60K | 🔴 High |
| File for EIN | $0 | 🔴 High |
| Open DUNA bank account | $0-$500 | 🔴 High |
| Draft inter-entity agreement (DUNA ↔ TrueTech) | $5K-$15K | 🟡 Medium |
| Begin IRS 501(c)(3) application process | $2K-$10K | 🟡 Medium |

### Phase 2: Medium-term (3-6 months) — $3K-$5K

| Action | Cost | Priority |
|--------|------|----------|
| Form Brazilian LTDA (CNPJ) | $1K-$3K | 🟡 Medium |
| Transfer export operations from Matheus's private entity | $1K-$2K | 🟡 Medium |
| Set up inter-company transfer pricing | $1K-$2K | 🟢 Low |

### Phase 3: Long-term (6-12 months)

| Action | Priority |
|--------|----------|
| Obtain IRS 501(c)(3) determination letter | 🔴 High |
| Launch public donation/tree-planting page | 🟡 Medium |
| Integrate carbon credit sales into DUNA revenue | 🟢 Low |
| Onboard impact fund partners | 🟡 Medium |

---

## 6. Ongoing Cost Projections

| Entity | Annual Cost | Notes |
|--------|-------------|-------|
| Wyoming DUNA | $200-$500 | License tax + registered agent + filing fees |
| TrueTech Inc (DE C-corp) | $300-$500 | Delaware franchise tax + registered agent |
| Brazilian LTDA | $1,000-$2,000 | Brazilian accounting + compliance |
| Legal counsel (retainer) | $5K-$15K | Entity maintenance, contract review |
| Accounting | $2K-$5K | Multi-entity bookkeeping |
| **Total ongoing** | **~$8,500-$23,000/year** | Scales with transaction volume |

---

## 7. Clarifying Questions for SVH Capital (June 26 Meetup)

These are designed to get the most value from Stanley and the SVH Capital team given their web3 legal entity expertise:

### 7.1 DUNA-Specific Questions

1. **DUNA + 501(c)(3) feasibility:** Has SVH seen a Wyoming DUNA successfully obtain IRS 501(c)(3) status? What's the realistic timeline and success rate?

2. **DUNA + for-profit subsidiary:** Can a DUNA wholly own a for-profit C-corp (TrueTech Inc) as a subsidiary, or must they be separate with a service agreement? What are the tax implications of each structure?

3. **100-member minimum:** We likely have fewer than 100 verified DAO members. Can we use a Wyoming UNA (Unincorporated Nonprofit Association — no minimum) as a stepping stone that converts to DUNA when we hit 100 members? OtoCo offers this on-chain conversion path.

4. **DUNA and TDG tokens:** How does the DUNA's nonprofit status interact with our existing TDG governance token? Can TDG holders still vote on DUNA matters? Can the DUNA issue tokens?

### 7.2 Brazil-US Cross-Border Questions

5. **Brazilian LTDA ownership:** Should the Brazilian LTDA be owned by the DUNA (nonprofit) or by TrueTech Inc (for-profit)? What are the tax implications of each for Brazilian remittance of profits?

6. **Transfer pricing:** What's the recommended transfer pricing methodology for cacao moving from Brazilian LTDA → TrueTech Inc → US market? Arm's length pricing based on comparable transactions?

### 7.3 Impact Fund Questions

7. **Impact fund structure:** For impact funds that want both a tax write-off AND a return (e.g., recoverable grants), what entity structure accommodates this? Can a DUNA issue recoverable grants?

8. **Carbon credit ownership:** Should carbon credits from tree planting be held by the DUNA (nonprofit) or by a separate for-profit entity? What's the optimal tax treatment for carbon credit sales?

### 7.4 Governance Questions

9. **Governor liability:** With a DUNA wrapper, are DAO governors still personally liable for DAO decisions? How does Wyoming's liability shield interact with fiduciary duties?

10. **Multi-sig treasury:** Can the DUNA's bank account be controlled by a multi-sig (e.g., Gnosis Safe) or does Wyoming law require human signatories? What's the recommended treasury management setup?

### 7.5 Practical Questions

11. **Formation timeline:** How long would SVH estimate for the full three-entity stack (DUNA + TrueTech improvements + Brazilian LTDA)? What are the critical path items?

12. **Cost estimate:** Rough budget for legal work to set up the DUNA + inter-entity agreements? We want to budget realistically.

13. **Nora's use case:** A Berkeley café wants to donate per-cup proceeds to rainforest restoration and give her customers a tax write-off. Is a DUNA + 501(c)(3) the cleanest path, or is there a simpler interim structure (e.g., fiscal sponsorship by an existing 501(c)(3))?

---

## 8. Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| DUNA 501(c)(3) application denied | Medium | High | Fiscal sponsorship as backup; operate as taxable nonprofit |
| Brazilian LTDA formation delays | High | Medium | Start process early; use experienced Brazilian law firm |
| DUNA 100-member requirement not met | High | Medium | Start with Wyoming UNA (no minimum), convert later |
| Legal costs exceed budget | Medium | Medium | Phase the work; start with Phase 0 (bank account) immediately |
| Regulatory change (SEC/CFTC) | Low | High | Wyoming DUNA is the most DAO-friendly framework available |
| Multi-entity accounting complexity | Medium | Low | Use DAO-native accounting tools (Toku, Llama, etc.) |

---

## 9. Recommendation

**Immediate action (this week):**
1. Open a dedicated business checking account for TrueTech Inc — stop commingling funds

**Short-term (before SVH meeting):**
2. Review this document and refine the questions for Stanley

**At the SVH Capital meeting (June 26):**
3. Lead with Nora's use case — it's the most concrete, urgent signal
4. Ask the 13 questions above
5. Gauge SVH's interest in being our legal counsel for entity structuring

**Post-meeting:**
6. Based on SVH's guidance, decide between DUNA-first or UNA-first path
7. Budget for Phase 1 legal costs
8. Begin DUNA formation paperwork

---

## 10. References

- Wyoming DUNA Act (2024): W.S. 17-32
- Wyoming DAO Supplement Act (2021): W.S. 17-31
- Toku DUNA 101 Guide: https://www.toku.com/resources/duna-101-a-founders-guide-to-wyomings-dao-legal-framework
- Falcon Rappaport & Berkman: Wyoming DUNA vs Offshore comparison
- Astraea Counsel: DAO LLC Formation Guide 2025
- OtoCo: On-chain UNA → DUNA conversion
- Ooki DAO CFTC ruling (2023): precedent for DAO member liability without legal wrapper
- Nouns DAO DUNA transition (2024): first major DAO to adopt Wyoming DUNA
- Uniswap governance DUNA adoption (2025)
