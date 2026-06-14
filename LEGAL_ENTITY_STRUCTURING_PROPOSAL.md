# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** Friday Tech Fest signals + SVH Capital cacao circle on June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## 1. Executive Summary

The convergence is accelerating. Nora (Kopi Bar, Berkeley) is onboarding. More partners are joining. Matheus channels exports through his private Brazilian entity. TrueTech Inc (Delaware C-corp) handles import and distribution. Gary's personal bank account collects funds.

This worked at pilot scale (~$15K cumulative sales). But three signals are turning from grey to red:

| Signal | Status | Why Now |
|--------|--------|---------|
| **DAO legal wrapper** | 🔴 Red | Member liability shield (Ooki DAO precedent), DAO bank account, governance clarity for TDG holders |
| **Tax-deductible donation channel** | 🟡 Yellow | Impact funds, corporate ESG, foundations need a 501(c)(3) to write checks |
| **Personal bank account** | 🔴 Red | Gary's personal account is the bottleneck — more volume = more personal risk |

### The core insight from our conversation

**TrueTech Inc is just another DAO member.** It contributes voluntarily (import, distribution, bank custody) and gets compensated in TDG — same as Nora, Kirsten, Matheus, or any other partner. No service agreement needed. No principal-agent complexity.

The DAO's legal wrapper (DUNA) is what's actually turning red — not because operations are blocked (TrueTech Inc handles those fine), but because:
1. **TDG holders need to know what entity they're voting on**
2. **Members need liability protection** as the community grows
3. **Impact funds need a donation-receiving entity** to write checks

### Recommended structure: Two-entity stack

```
Wyoming DUNA (nonprofit, DAO legal wrapper)
    ↕ TDG holders govern the DUNA
    ↕ TrueTech Inc = DAO member (voluntary contributor)
    ↕ Brazilian LTDA (CNPJ) = export/sourcing entity
```

No inter-entity agreement between DUNA and TrueTech Inc. TrueTech Inc is a member, not a contractor. The DUNA is the legal wrapper for what TDG holders vote on. TrueTech Inc is one voice among many.

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
| No member liability shield | 🔴 High | Token holders could be treated as general partners (per Ooki DAO precedent) |
| No tax-advantaged donation pathway | 🔴 High | Impact funds, foundations, corporate ESG have no channel |
| Governance ambiguity | 🔴 High | TDG holders don't have a clear answer to "what entity am I voting on?" |
| Tax reporting complexity | 🟡 Medium | C-corp filing + personal income + potential partnership tax treatment |
| Brazil export compliance | 🟡 Medium | Matheus's private entity bears all Brazilian compliance burden |

### 2.2 Current Ledger Snapshot

- **Cumulative sales (all time):** ~$15,736 USD
- **Monthly run rate (2026):** ~$500-1,100/month trending up
- **USD Treasury Balance:** ~$14,622
- **AUM:** ~$28,144
- **Physical assets on ledger:** ~$14,622 across 25+ asset types
- **Partners:** Nora (Kopi Bar), Kirsten, Matheus, Edge & Node, Shuar Design Boutique, and growing
- **TDG issued:** ~2.3M tokens across contributors

### 2.3 The Governance Story Problem

When a TDG holder asks "what entity do my voting rights govern?", the current answer is unsatisfying:

> *"You're voting on the DAO community itself. TrueTech Inc is our operational partner, not the DAO. We're in the process of forming a Wyoming DUNA that will become the formal legal wrapper."*

This is honest but incomplete. A DUNA solves it cleanly:

> *"TDG holders govern the TrueSight DUNA — a Wyoming nonprofit association. The DUNA holds the mission, the brand, the carbon credit rights, and the relationship with TrueTech Inc (one of our DAO members). When you vote with TDG, you're voting on DUNA matters."*

---

## 3. Option Analysis

### 3.1 Option A: Wyoming DUNA (Decentralized Unincorporated Nonprofit Association)

**What it is:** A Wyoming-specific legal entity designed for DAOs. Nonprofit by statute — cannot distribute profits to members. Took effect July 1, 2024. Already adopted by Nouns DAO and Uniswap governance.

| Dimension | Detail |
|-----------|--------|
| **Liability** | Members shielded from personal liability for DAO obligations |
| **Tax status** | Nonprofit entity; can apply for 501(c)(3) tax-exempt status with IRS |
| **Governance** | Smart contract-based voting explicitly recognized by law |
| **Minimum members** | 100 members required for DUNA; UNA has no minimum |
| **Profit distribution** | ❌ Not allowed — all revenue must be reinvested in mission |
| **Formation cost (full-service)** | $100 state filing + $20K-$60K legal fees |
| **Formation cost (OtoCo UNA)** | ~$50 gas, no lawyer needed, auto-converts to DUNA at 100 members |
| **Annual cost** | $60-$200 license tax; no Wyoming state income tax |
| **Bank account** | Can open US bank account with EIN |
| **Time to form** | 4-8 weeks (full-service); 1 day (OtoCo UNA) |

**✅ Pros:**
- Perfect mission alignment (nonprofit, rainforest restoration)
- Impact funds, foundations, and corporate ESG can write tax-deductible checks (if 501(c)(3) obtained)
- Legal recognition of on-chain governance
- Clean answer for TDG holders: "you're voting on the DUNA"
- OtoCo path makes formation near-free (~$50 gas)
- No state income tax (Wyoming)

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
- Less mission-aligned than DUNA
- Doesn't solve the governance story as cleanly (TDG holders voting on a for-profit LLC?)

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
- Does not solve US tax-deduction or liability shield problems

---

## 4. Recommended Path

### The simplified model

```
┌─────────────────────────────────────────────────────┐
│                   DUNA (Wyoming)                      │
│  • DAO legal wrapper                                  │
│  • Holds mission, brand, carbon credits               │
│  • Governed by all TDG holders                        │
│  • Can apply for 501(c)(3) tax exemption              │
│  • TrueTech Inc = one member among many               │
└─────────────────────┬─────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
┌─────────────────┐   ┌─────────────────────────┐
│  TrueTech Inc    │   │  Brazilian LTDA (CNPJ)   │
│  (DE C-corp)     │   │  • Export entity          │
│  • DAO member    │   │  • Farmer payments        │
│  • Import/dist   │   │  • Brazilian compliance   │
│  • Bank custody  │   │  • Owned by DUNA          │
│  • TDG comp      │   └─────────────────────────┘
└─────────────────┘
```

**Key relationships:**

| Relationship | Type | Detail |
|-------------|------|--------|
| DUNA ↔ TrueTech Inc | **Member** | TrueTech Inc is a DAO member, contributes voluntarily, compensated in TDG |
| DUNA ↔ Brazilian LTDA | **Ownership** | DUNA owns or affiliates with the Brazilian entity |
| TrueTech Inc ↔ TDG holders | **Peer** | TrueTech Inc holds TDG like any other member — one voice, one vote |
| TrueTech Inc ↔ Bank | **Custodian** | TrueTech Inc opens a business bank account as a member contribution to the DAO |

### Why DUNA over DAO LLC

| Factor | DUNA Wins | DAO LLC Wins |
|--------|-----------|--------------|
| Tax-deductible donations (impact funds) | ✅ | ❌ |
| Mission alignment (nonprofit) | ✅ | ❌ |
| Clean governance story for TDG holders | ✅ | ⚠️ |
| Member liability shield | ✅ | ✅ |
| Profit distribution to TDG holders | ❌ | ✅ |
| Formation cost (OtoCo path) | ✅ (~$50) | ❌ ($15K+) |

The DUNA's nonprofit constraint aligns perfectly with the mission (restore 10,000 hectares of Amazon rainforest). TrueTech Inc remains the for-profit engine that generates revenue; the DUNA is the mission wrapper that receives donations, plants trees, and issues tax receipts. TDG holders govern the DUNA. TrueTech Inc participates as a member.

---

## 5. Cost Analysis

### Path A: OtoCo On-Chain UNA → DUNA (Recommended — Start Today)

| Item | Cost |
|------|------|
| OtoCo smart contract creation (2+ wallets sign) | ~$50 (gas only) |
| UNA agreement (auto-converts to DUNA at 100 members) | Included |
| Annual Wyoming license tax | $60-$200/yr |
| Registered agent | $100-$200/yr |
| **Total Year 1** | **~$250-500** |
| **Total Ongoing** | **~$200-400/yr** |

**What you get:** Legal personhood, liability protection, ability to open bank account, sign contracts. Auto-converts to DUNA when you hit 100 members. No lawyer needed for formation.

### Path B: Full DUNA via Law Firm (Traditional)

| Item | Cost |
|------|------|
| Wyoming state filing fee | $100 |
| Legal fees (Astraea / Hathaway & Kunz / similar) | $20,000-$60,000 |
| Registered agent | $100-$200/yr |
| Annual license tax | $60-$200/yr |
| **Total Year 1** | **~$20,500-$60,500** |
| **Total Ongoing** | **~$200-400/yr** |

**What you get:** Full-service — Articles of Organization, Operating Agreement, governance docs, compliance review, smart contract integration.

### Path C: Brazilian LTDA

| Item | Cost |
|------|------|
| Legal + registration fees | $1,000-$3,000 |
| Annual accounting + compliance | $500-$2,000/yr |
| **Total Year 1** | **~$1,500-$5,000** |

### Path D: 501(c)(3) Application (Downstream, After DUNA)

| Item | Cost |
|------|------|
| Tax attorney / CPA for IRS Form 1023 | $2,000-$10,000 |
| IRS filing fee | $600 (Form 1023-EZ) or $2,500 (Form 1023) |
| Timeline | 6-12 months |

---

## 6. Resource Gap Analysis

### ✅ What We Already Have Internally

| Resource | Status | Detail |
|----------|--------|--------|
| **Mission clarity** | ✅ Strong | Restore 10,000 hectares of Amazon rainforest — compelling narrative for donors |
| **On-chain governance** | ✅ Strong | TDG tokens, contribution ledger, Edgar API — DUNA-compatible governance model |
| **Physical operations** | ✅ Strong | Supply chain from Brazil farmers → US distribution → retail (agroverse.shop) |
| **Tree-planting pipeline** | ✅ Strong | sunmint repo, lineage-credentials, existing reforestation partners |
| **Partner network** | ✅ Growing | Nora (Kopi Bar), Kirsten, Matheus, Edge & Node, Shuar Design Boutique |
| **Carbon credit potential** | ✅ Emerging | Trees being planted → future carbon credits → revenue stream |
| **Technical infrastructure** | ✅ Strong | AWS, Edgar API, tokenomics automation, QR inventory tracking |
| **SVH Capital connection** | ✅ Warm intro | June 26 cacao circle — Stanley specializes in web3 legal entity structuring |

### ❌ What We're Missing

| # | Gap | Severity | Why It Matters | Cost to Resolve |
|---|------|----------|----------------|-----------------|
| **1** | **Legal counsel** | 🔴 Critical | DUNA formation requires specialized DAO/crypto legal expertise. SVH may refer. | $15K-$60K (or OtoCo path: ~$50) |
| **2** | **Cash for full-service legal** | 🟡 Medium | Treasury is ~$14,622. Full-service DUNA is $20K-$60K. OtoCo path avoids this. | $0 (OtoCo) or $5K-$45K gap (full-service) |
| **3** | **100 DUNA members** | 🟡 Medium | Wyoming DUNA requires 100 members. Workaround: start with UNA (no minimum). | $0 |
| **4** | **501(c)(3) expertise** | 🟡 Medium | IRS exemption application needs a tax attorney or CPA. 6-12 month timeline. | $2K-$10K |
| **5** | **Brazilian legal representative** | 🟡 Medium | Brazilian LTDA requires a local lawyer. Matheus may have connections. | $1K-$3K |
| **6** | **Multi-entity accounting** | 🟢 Low | DUNA + TrueTech Inc + Brazilian LTDA need consolidated bookkeeping. | $2K-$5K/yr |
| **7** | **Dedicated TrueTech Inc bank account** | 🟢 Low | Quick fix — $0-$500, 1-2 weeks. | $0-$500 |

### What We Could Use as Alternative Currency

| Asset | How It Helps |
|-------|-------------|
| **TDG tokens** (~2.3M issued) | Offer legal counsel a TDG grant as partial compensation (deferred value) |
| **Future carbon credits** | Offer a % of future carbon credit revenue as deferred payment |
| **Revenue share** | Offer legal counsel a % of future DUNA donation revenue |
| **SVH Capital relationship** | They may offer discounted rates, deferred payment, or introductions to pro-bono counsel |

---

## 7. Implementation Timeline

| Phase | What | Cost | Timeline |
|-------|------|------|----------|
| **Now** | Open TrueTech Inc business bank account | $0-500 | 1-2 weeks |
| **Now** | Summon OtoCo on-chain UNA (2 wallets sign) | ~$50 gas | 1 day |
| **Next** | Use UNA to open a DAO bank account | $0 | 2-4 weeks |
| **June 26** | Ask SVH Capital about DUNA formation + legal counsel referrals | $0 | One conversation |
| **Next** | Engage Wyoming DAO lawyer (via SVH referral or OtoCo network) for UNA → DUNA | $5K-15K | After SVH |
| **Later** | When >100 members, UNA auto-converts to DUNA | $0 | Automatic |
| **Later** | Form Brazilian LTDA (via Matheus's connections) | $1K-3K | 4-8 weeks |
| **Later** | 501(c)(3) application via tax attorney | $2K-10K | 6-12 months |

**Total cash needed for Year 1 (OtoCo path): ~$500-2,500** — well within treasury.

---

## 8. Questions for SVH Capital (June 26 Cacao Circle)

### Primary questions (governance + liability)

1. **DUNA formation:** Do you work with or can you refer us to a Wyoming law firm that specializes in DUNA formation for DAOs? (Hathaway & Kunz, Astraea, etc.)

2. **OtoCo viability:** Is the OtoCo on-chain UNA → DUNA path sufficient for our stage, or do we need full-service legal from day one?

3. **Governance clarity:** We have a for-profit C-corp (TrueTech Inc) that operates as a voluntary DAO member, compensated in TDG. Can a Wyoming DUNA issue TDG tokens to a for-profit C-corp as member compensation?

4. **501(c)(3) pathway:** Once DUNA is formed, what's the realistic timeline and cost for IRS exemption for a DAO that plants trees?

5. **Brazilian entity:** Can a Wyoming DUNA own or affiliate with a Brazilian LTDA, or does that need a separate holding structure?

6. **TDG as compensation:** Would your referred counsel consider a partial TDG token grant to reduce the cash outlay?

### Secondary questions (fundraising + operations)

7. **Impact fund readiness:** What do impact funds typically look for in a DAO's legal structure before writing a check?

8. **Carbon credits:** How should the DUNA structure carbon credit rights — as an asset of the DUNA or a separate vehicle?

9. **Member cap:** Is there a practical upper limit on DUNA members before compliance complexity increases?

---

## 9. Clarifying Questions for the DAO

Before engaging counsel, the DAO should align on:

1. **TDG and the DUNA:** Should TDG tokens represent membership in the DUNA directly, or should there be a separate membership token?

2. **TrueTech Inc's role:** Is TrueTech Inc comfortable being a DAO member compensated in TDG, with no separate service agreement?

3. **Brazilian entity ownership:** Should the DUNA own the Brazilian LTDA directly, or should it be owned by a separate holding entity?

4. **501(c)(3) timing:** Do we apply for IRS exemption immediately after DUNA formation, or wait until we have a track record of donations?

5. **Carbon credit rights:** Should carbon credits be an asset of the DUNA (nonprofit, mission-locked) or of TrueTech Inc (for-profit, tradeable)?

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| OtoCo UNA not recognized by banks | Medium | High | Have backup: use TrueTech Inc account as custodian until DUNA is fully formed |
| IRS denies 501(c)(3) for DAO | Low | High | Structure as 501(c)(3) with clear charitable purpose (rainforest restoration); precedent exists for crypto-native nonprofits |
| Wyoming DUNA law changes | Low | Medium | Monitor legislation; Wyoming is pro-DAO and unlikely to retroactively restrict |
| Brazilian LTDA formation delays | Medium | Low | Matheus continues using his private entity as interim |
| TDG token classified as security | Low | High | DUNA membership tokens are generally not securities; consult with SVH-referred counsel |

---

## 11. Appendix: Key Terms

| Term | Definition |
|------|------------|
| **DUNA** | Decentralized Unincorporated Nonprofit Association — Wyoming entity for DAOs (effective July 2024) |
| **UNA** | Unincorporated Nonprofit Association — simpler precursor to DUNA, no 100-member minimum |
| **DAO LLC** | Wyoming LLC with DAO designation under the DAO Supplement Act (2021) — for-profit |
| **LTDA** | Limitada — Brazilian limited liability company |
| **CNPJ** | Cadastro Nacional da Pessoa Jurídica — Brazilian federal tax ID for businesses |
| **501(c)(3)** | US IRS tax exemption for charitable, religious, educational organizations |
| **OtoCo** | On-chain entity formation platform — creates Wyoming UNAs/DUNAs via smart contract |
| **TDG** | TrueSight DAO Governance token — voting rights in the DAO |
| **TrueTech Inc** | Delaware C-corporation — DAO member handling import, distribution, bank custody |

---

*This proposal was generated by Sophia (TrueSight DAO Autopilot) based on research, ledger analysis, and strategic conversation with Gary Teh. It is not legal advice. Consult qualified legal counsel before forming any entity.*