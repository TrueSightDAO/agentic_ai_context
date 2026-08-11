# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** Friday Tech Fest signals + SVH Capital cacao circle on June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## 1. Executive Summary

The convergence is accelerating. Nora (Kopi Bar, Berkeley) is onboarding. More partners are joining. Matheus channels exports through his private Brazilian entity. TrueTech Inc (Delaware C-corp) is the importing entity. Gary's personal bank account collects funds. This worked at pilot scale (~$15K cumulative sales), but the signal is clear: **the tax-write-off infrastructure in the USA jurisdiction is turning from grey to red.**

### Why the tax-write-off facility matters (beyond Nora's café)

The venture partner from Progressive Ventures flagged the real strategic signal: a **tax-deductible donation facility unlocks institutional fundraising channels**, not just retail receipts. It enables:

- **Impact funds** — they can write tax-deductible checks instead of needing equity structures
- **Corporate ESG budgets** — companies get a tax write-off + verified carbon offsets = easy budget approval
- **High-net-worth donors** — individuals who want to support rainforest restoration and reduce their tax liability
- **Foundation grants** — most foundations can only grant to 501(c)(3) entities

Without it, we can only approach these organizations for equity investments or revenue-share deals — a much harder conversation. With a DUNA + 501(c)(3), we can approach them with a **donation pathway**: lower friction, faster decisions, aligned incentives.

Nora's café becomes a **downstream beneficiary** of infrastructure built for the bigger institutional play.

### Three structural options surfaced at Tech Fest

| Option | Jurisdiction | Structure | Best For |
|--------|-------------|-----------|----------|
| **DUNA** | Wyoming, USA | Decentralized Unincorporated Nonprofit Association | DAO legal wrapper, nonprofit mission alignment, tax-deductible donations |
| **Prospera / Wyoming DAO LLC** | Wyoming, USA | For-profit DAO LLC | Tokenized revenue sharing, profit distributions to members |
| **Brazilian CNPJ (LTDA)** | Brazil | Limited liability company | Local export entity, cacao sourcing, Brazilian tax compliance |

**Recommendation:** A **three-entity stack** — Wyoming DUNA (DAO wrapper, donation receiver) → TrueTech Inc (US import/distribution) → Brazilian LTDA (export/sourcing) — with a clear inter-entity agreement for fund flows, carbon credit rights, and tax-advantaged donations.

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
| No tax-advantaged donation pathway | 🔴 High | Impact funds, corporate ESG, foundations, and HNW donors have no channel |
| Brazil export compliance | 🟡 Medium | Matheus's private entity bears all Brazilian compliance burden |

### 2.2 Current Ledger Snapshot

- **Cumulative sales (all time):** ~$15,736 USD
- **Monthly run rate (2026):** ~$500-1,100/month trending up
- **USD Treasury Balance:** ~$14,622
- **AUM:** ~$28,144
- **Physical assets on ledger:** ~$14,622 across 25+ asset types
- **Partners:** Nora (Kopi Bar), Kirsten, Matheus, Edge & Node, Shuar Design Boutique, and growing

### 2.3 Nora's Use Case (Catalyst, Not Driver)

Nora wants to channel a portion of **each cup of cacao sold at Kopi Bar** to rainforest restoration. This is a powerful proof-of-concept for the donation infrastructure, but the **real prize** is the institutional fundraising channel it unlocks.

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
| **Formation cost** | $100 state filing + $20K-$60K legal fees (full-service law firm) |
| **Low-cost alternative** | OtoCo on-chain UNA: ~$50 gas, no lawyer needed, auto-converts to DUNA at 100 members |
| **Annual cost** | $60-$200 license tax; no Wyoming state income tax |
| **Bank account** | Can open US bank account with EIN |
| **Time to form** | 4-8 weeks (full-service); 1 day (OtoCo UNA) |

**✅ Pros:**
- Perfect mission alignment (nonprofit, rainforest restoration)
- Impact funds, foundations, and corporate ESG can write tax-deductible checks (if 501(c)(3) obtained)
- Nora's customers can get tax-deductible receipts
- Legal recognition of on-chain governance
- No state income tax (Wyoming)
- OtoCo path makes formation near-free

**❌ Cons:**
- Cannot distribute profits to TDG token holders
- 100-member minimum for DUNA (UNA works below that)
- IRS 501(c)(3) application is a separate, lengthy process (6-12 months, $2K-$10K)
- Full-service legal fees are $20K-$60K (but OtoCo bypasses this for formation)
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
- Impact funds, foundations, and corporate ESG cannot write tax-deductible checks
- Nora's customers cannot get tax write-offs
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
│  • Receives donations from impact funds / ESG / HNW  │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ Service Agreement / License
                       ▼
┌─────────────────────────────────────────────────────┐
│              TrueTech Inc (Delaware C-corp)           │
│  • US import and distribution entity                 │
│  • Holds inventory, processes payments               │
│  • Pays Brazilian suppliers                          │
│  • For-profit — generates revenue                    │
│  • Pays DUNA a license fee / service fee              │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ Inter-company agreement
                       ▼
┌─────────────────────────────────────────────────────┐
│              Brazilian LTDA (CNPJ)                    │
│  • Local export entity in Brazil                     │
│  • Contracts directly with farmers                   │
│  • Handles Brazilian tax compliance                  │
│  • Issues NF-e tax receipts                          │
│  • Owned by TrueTech Inc or DUNA                     │
└─────────────────────────────────────────────────────┘
```

### 4.2 How Money Flows (Proposed)

```
Impact Fund / Donor → DUNA (tax-deductible donation, 501(c)(3) receipt issued)
                                    ↓
                    DUNA pays TrueTech Inc for services
                                    ↓
                    TrueTech Inc pays Brazilian LTDA for cacao
                                    ↓
                    LTDA pays Brazilian farmers

Retail customer → agroverse.shop → TrueTech Inc (revenue)
                                    ↓
                    TrueTech Inc pays DUNA license fee
                                    ↓
                    DUNA reinvests in rainforest restoration
```

### 4.3 Carbon Credit Rights

The DUNA, as the mission-entity, should hold the **carbon credit rights** from trees planted. This is a future revenue stream that aligns with the nonprofit mission and can be sold to corporate ESG buyers (who want tax-deductible carbon offsets).

---

## 5. Cost Analysis

### 5.1 Three Paths Compared

| Item | OtoCo UNA (Lean) | Full DUNA (Law Firm) | DAO LLC (For-Profit) |
|------|:-:|:-:|:-:|
| **State filing fee** | $0 (no formal registration) | $100 | $100 |
| **Legal fees** | ~$0 (smart contract) | $20K-$60K | $15K-$50K |
| **Registered agent** | $100-$200/yr | $100-$200/yr | $100-$200/yr |
| **Annual license tax** | $60-$200/yr | $60-$200/yr | $60-$200/yr |
| **501(c)(3) application** | $2K-$10K (later) | $2K-$10K (included?) | N/A |
| **Inter-entity agreement** | $5K-$15K (lawyer) | $5K-$15K (lawyer) | $5K-$15K (lawyer) |
| **Brazilian LTDA** | $1K-$3K | $1K-$3K | $1K-$3K |
| **Total Year 1** | **~$8K-$28K** | **~$28K-$88K** | **~$21K-$68K** |

### 5.2 What We Have vs. What We Need

| Resource | Status | Detail |
|----------|--------|--------|
| Mission & narrative | ✅ Strong | Restore 10,000 hectares — compelling for donors |
| On-chain governance | ✅ Strong | TDG tokens, Edgar API, contribution ledger |
| Supply chain ops | ✅ Strong | Brazil farmers → US distribution → retail |
| Tree-planting pipeline | ✅ Strong | sunmint, lineage-credentials, reforestation partners |
| Partner network | ✅ Growing | Nora, Kirsten, Matheus, Edge & Node, Shuar |
| Technical infrastructure | ✅ Strong | AWS, Edgar, tokenomics, QR inventory |
| SVH Capital connection | ✅ Warm intro | June 26 cacao circle |
| **Legal counsel** | ❌ Missing | Need to engage (SVH referral or OtoCo) |
| **Cash for legal fees** | ⚠️ Tight | $14,622 treasury — OtoCo path fits, full-service doesn't |
| **100 DUNA members** | ⚠️ Workaround | Use UNA (<100 members), auto-converts later |
| **501(c)(3) expertise** | ❌ Missing | Need tax attorney when ready |
| **Brazilian lawyer** | ❌ Missing | Matheus may have connections |
| **Dedicated bank account** | ❌ Missing | $0-$500, easy fix this week |

---

## 6. Recommended Action Plan

### Phase 1: This Week (Cost: ~$50-500)

| Action | Cost | Why |
|--------|:----:|-----|
| Open TrueTech Inc business bank account | $0-$500 | Stops personal commingling immediately |
| Summon **OtoCo on-chain UNA** (2 wallets sign) | ~$50 gas | Instant legal personhood for the DAO |

### Phase 2: June 26 — SVH Capital Conversation (Cost: $0)

**What to ask Stanley:**

1. **DUNA formation:** Do you work with or can you refer us to a Wyoming law firm that specializes in DUNA formation for DAOs? (Hathaway & Kunz, Astraea, etc.)

2. **Cost efficiency:** What's the leanest way to get a DUNA in place — full-service law firm or is OtoCo's on-chain UNA → DUNA path sufficient for our stage?

3. **501(c)(3) pathway:** Once DUNA is formed, what's the realistic timeline and cost for the IRS exemption application for a DAO that plants trees?

4. **TDG as compensation:** Would your referred counsel consider a partial TDG token grant to reduce the cash outlay?

### Phase 3: Next 1-3 Months (Cost: ~$5K-$15K)

| Action | Cost | Why |
|--------|:----:|-----|
| Engage Wyoming DAO lawyer (via SVH referral) | $5K-$15K | Inter-entity agreement (DUNA ↔ TrueTech) |
| Form Brazilian LTDA (via Matheus's connections) | $1K-$3K | Formalize export operations |

### Phase 4: When >100 Members (Cost: $0, Automatic)

| Action | Detail |
|--------|--------|
| UNA auto-converts to DUNA | OtoCo smart contract detects >100 token holders, legal conversion happens automatically |

### Phase 5: 6-12 Months Out (Cost: ~$2K-$10K)

| Action | Cost | Why |
|--------|:----:|-----|
| 501(c)(3) application via tax attorney | $2K-$10K | Enables tax-deductible donations from impact funds, foundations, ESG |

---

## 7. Clarifying Questions for SVH Capital (June 26)

These are ordered by strategic importance:

1. **DUNA formation:** Do you work with or can you refer us to a Wyoming law firm that specializes in DUNA formation for DAOs?

2. **OtoCo viability:** Is the OtoCo on-chain UNA → DUNA path legally sufficient for a DAO at our stage, or do we need a full-service law firm from day one?

3. **501(c)(3) pathway:** What's the realistic timeline and cost for a DUNA to obtain IRS 501(c)(3) tax-exempt status? Are there DAO-specific complications?

4. **Impact fund compatibility:** From your experience with impact funds — what legal structure do they prefer to write checks to? DUNA? Fiscal sponsor? Direct?

5. **TDG as compensation:** Would a law firm in your network consider a partial TDG token grant to reduce the cash outlay for formation?

6. **Carbon credits:** Should the DUNA hold carbon credit rights directly, or is a separate SPV better?

7. **Brazil-US flow:** Any experience with cross-border structures involving Brazilian exports and US nonprofit entities?

---

## 8. Risks and Open Questions

| Risk | Mitigation |
|------|-----------|
| DUNA cannot distribute profits to TDG holders | TrueTech Inc (for-profit) handles profit-generating activities; DUNA receives service fees |
| 501(c)(3) application denied | Fiscal sponsorship as fallback; operate as tax-paying nonprofit DUNA without exemption |
| Brazilian LTDA compliance burden | Engage Brazilian accounting firm; Matheus may have existing relationships |
| US nexus exposes DAO to SEC jurisdiction | DUNA's nonprofit structure + decentralization argument (per a16z model legislation) provides strong defense |
| Cash for legal fees ($14K treasury vs. $20K-$60K) | OtoCo path bypasses this; full-service law firm can wait until impact fund money flows |

---

## 9. Summary

| Priority | Action | Cost | Timeline |
|----------|--------|:----:|:--------:|
| 🔴 Now | Open TrueTech Inc bank account | $0-$500 | 1-2 weeks |
| 🔴 Now | Summon OtoCo on-chain UNA | ~$50 | 1 day |
| 🟡 June 26 | Ask SVH Capital for DUNA counsel referrals | $0 | One conversation |
| 🟡 Next | Engage lawyer for inter-entity agreement | $5K-$15K | 1-3 months |
| 🟢 Later | 501(c)(3) application | $2K-$10K | 6-12 months |

The **OtoCo UNA path** gets us 80% of the benefit for 1% of the cost. The full-service law firm path is for when impact fund money is flowing and we need the white-glove treatment.

---

*This proposal is a living document. Update as new information emerges from the SVH Capital conversation on June 26.*
