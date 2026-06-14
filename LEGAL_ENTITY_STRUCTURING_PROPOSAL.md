# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** Friday Tech Fest signals + SVH Capital cacao circle on June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## 1. Executive Summary

The convergence is accelerating. Nora (Kopi Bar, Berkeley) is onboarding. More partners are joining. Matheus channels exports through his private Brazilian entity. TrueTech Inc (Delaware C-corp) handles US customs clearance and FDA compliance. Gary's personal bank account collects funds.

This worked at pilot scale. But three signals are turning from grey to red:

| Signal | Status | Why Now |
|--------|--------|---------|
| **DAO legal wrapper** | 🔴 Red | Member liability shield (Ooki DAO precedent), DAO bank account, governance clarity for TDG holders |
| **Impact fund capital injection** | 🔴 Red | Impact funds, foundations, corporate ESG have no entity to write checks to — no tax-deductible pathway, no legal counterparty |
| **Personal bank account** | 🔴 Red | Gary's personal account is the bottleneck — more volume = more personal risk |

### The core structure

```
Wyoming UNA/DUNA (nonprofit, DAO legal wrapper)
    ├── Own bank account (receives partner contributions + impact fund capital)
    ├── TDG holders govern the DUNA (pseudonymous — wallet only)
    ├── TrueTech Inc = DAO-operated facility (customs/FDA, not a member)
    │   └── Own bank account (import expenses, TDG buyback → burn)
    └── Brazilian LTDA (CNPJ) = export facility (eventually DUNA-owned)
```

### Key design decisions

| Decision | Rationale |
|----------|-----------|
| **TrueTech Inc = DAO-operated facility** | Not a member. No TDG compensation. No voting rights. Its board handles operational/compliance decisions. DAO members are reflected in the DUNA, not on TrueTech Inc's board. |
| **Two separate bank accounts** | TrueTech Inc account: customs bonds, FDA fees, import duties, TDG buyback. DUNA account: partner contributions, tree planting, impact fund capital, DAO treasury. |
| **TDG buyback → burn** | When a member wants to exit, TrueTech Inc buys TDG from the DApp and burns it. No TDG held by TrueTech Inc → no voting rights issue. Deflationary mechanism rewards remaining holders. |
| **UNA → DUNA auto-conversion** | OtoCo handles via smart contract when membership hits 100. Same EIN, same bank account. |
| **Wise as single banking platform** | Both TrueTech Inc and DUNA use Wise Business accounts. Same API, same Brazil pipeline, multi-currency support. |
| **Brazil CNPJ eventually DUNA-owned** | Removes single-person dependency on Matheus. Requires cross-border legal counsel. |

---

## 2. Current State Assessment

### 2.1 Financial Flows

**Current (problematic):**
```
Brazil Farmers → Matheus (private CNPJ) → Export → TrueTech Inc → Gary's personal bank account → DAO expenses
Impact funds → nowhere (no entity to write checks to)
```

**Target (with DUNA bank account + DUNA-owned CNPJ):**
```
Brazil Farmers → DUNA-owned CNPJ → Export → TrueTech Inc (facility) → TrueTech Inc account (import expenses)
Partners (Nora, etc.) → DUNA bank account → tree planting / DAO expenses
Impact funds → DUNA bank account → tree planting / carbon credits
Member exit → TrueTech Inc buys TDG from DApp → TDG burned
```

Gary's personal account and Matheus's private CNPJ are both removed from the flow.

**Risks in current flow:**

| Risk | Severity | Detail |
|------|----------|--------|
| Personal liability | 🔴 High | Gary's personal account commingles DAO funds with personal funds |
| No member liability shield | 🔴 High | Token holders could be treated as general partners (per Ooki DAO precedent) |
| No impact fund channel | 🔴 High | Impact funds, foundations, corporate ESG have no entity to write checks to |
| Governance ambiguity | 🔴 High | TDG holders don't have a clear answer to "what entity am I voting on?" |
| Single-person dependency (Brazil) | 🔴 High | Matheus's private CNPJ means the export channel is tied to one person |
| Tax reporting complexity | 🟡 Medium | C-corp filing + personal income + potential partnership tax treatment |
| Brazil export compliance | 🟡 Medium | Matheus's private entity bears all Brazilian compliance burden |

### 2.2 Current Treasury Snapshot

**Only Main Ledger cash is available for deployment.** Managed ledgers (AGL4, AGL6, AGL8, AGL10, AGL13, AGL15, SEF1, BEC, etc.) are earmarked for specific purposes — mostly cacao shipment financing.

| Item | Amount |
|------|--------|
| **Main Ledger USD** | **$3,476.27** |
| Main Ledger USDT | $66.93 |
| Main Ledger Brazilian Reis | R$2,511.97 (~$583.53 USD) |
| **Total available cash** | **~$4,126.73** |
| Cumulative sales (all time) | ~$15,736 USD |
| Monthly run rate (2026) | ~$500-1,100/month trending up |
| TDG issued | ~2.3M tokens across ~350 contributors |
| Partners | Nora (Kopi Bar), Kirsten, Matheus, Edge & Node, Shuar Design Boutique, and growing |

### 2.3 The Governance Story Problem

When a TDG holder asks "what entity do my voting rights govern?", the current answer is unsatisfying:

> *"You're voting on the DAO community itself. TrueTech Inc is our operational facility, not the DAO. We're in the process of forming a Wyoming DUNA that will become the formal legal wrapper."*

A UNA/DUNA solves it cleanly:

> *"TDG holders govern the TrueSight DUNA — a Wyoming nonprofit association. The DUNA holds the mission, the brand, the carbon credit rights, and its own bank account. TrueTech Inc is a DAO-operated facility for customs and FDA compliance — it executes on the DUNA's decisions. When you vote with TDG, you're voting on DUNA matters."*

---

## 3. CTA Beneficial Ownership — Who Reports

Under the Corporate Transparency Act (CTA), any individual who exercises **"substantial control"** over the entity or owns **≥25%** of its ownership interests must report Beneficial Ownership Information (BOI) to FinCEN.

**"Substantial control"** includes:
1. Serving as a senior officer (CEO, CFO, etc.)
2. Having authority to appoint or remove senior officers or board members
3. Having substantial influence over important decisions (bank accounts, contracts, governance parameters, treasury)

### Who in the DAO crosses the threshold?

From the Contributors Voting Weight ledger:

| Rank | Contributor | % Controlled | CTA Trigger? |
|------|------------|-------------|--------------|
| 1 | **Gary Teh** | **40.76%** | ✅ **Yes** — >25% ownership + substantial control |
| 2 | Garis Pang | 2.89% | ❌ No |
| 3 | Fatima Toledo | 2.81% | ❌ No |
| 4-10 | Various | <3% each | ❌ No |
| 11-350+ | All other TDG holders | <2% each | ❌ No |

**Result: Only Gary needs to report.** Name, DOB, address, and government ID for the CTA BOI filing. Every other TDG holder (~350 people) remains pseudonymous — wallet address only.

**For the initial UNA formation (2 signers):** Gary + TrueTech Inc representative. Both provide their personal info for the CTA filing. That's it. No cascading KYC. No asking 350 people to dox themselves.

This is a key advantage of the UNA/DUNA structure: the vast majority of contributors never need to reveal their identity.

---

## 4. Impact Fund Capital Injection Pathways

This is the primary reason the DUNA is needed. Impact funds, foundations, and corporate ESG programs need a legal entity to write checks to. Currently, there is none.

### 4.1 The Three Pathways

| Pathway | DUNA Needed? | 501(c)(3) Needed? | Tax Deductible? | Timeline |
|---------|-------------|-------------------|-----------------|----------|
| **A: Direct donation to DUNA** | ✅ Yes | ❌ No | ❌ No (but fund can still donate) | Immediate after DUNA formed |
| **B: Fiscal sponsorship bridge** | ✅ Yes | ❌ No (sponsor has it) | ✅ Yes (via sponsor) | 1-3 months |
| **C: DUNA's own 501(c)(3)** | ✅ Yes | ✅ Yes | ✅ Yes | 6-12 months |

### 4.2 Pathway A: Direct Donation to DUNA (Immediate)

Once the DUNA is formed and has a bank account, impact funds can write checks directly. The donation is **not tax-deductible** for the fund (the DUNA doesn't have 501(c)(3) status yet), but many impact funds can still deploy capital through:

- **Program-Related Investments (PRIs)** — foundations can make PRIs without requiring 501(c)(3) status of the recipient
- **For-profit impact arms** — many funds have a for-profit entity that can invest without tax deduction requirements
- **Grants from donor-advised funds** — DAFs can recommend grants to any entity
- **Direct corporate ESG budgets** — companies can pay for carbon offsets or sustainability programs without requiring tax deductibility

**Flow:**
```
Impact fund → DUNA bank account → tree planting / carbon credits → impact report to fund
```

### 4.3 Pathway B: Fiscal Sponsorship Bridge (1-3 Months)

While the DUNA's own 501(c)(3) application processes, an existing 501(c)(3) organization can act as a **fiscal sponsor**. The sponsor receives donations on the DUNA's behalf and issues tax-deductible receipts to donors.

**How it works:**
```
Impact fund → Fiscal sponsor (existing 501(c)(3)) → Tax-deductible receipt to fund
                                        ↓
                              Passes funds to DUNA (minus 5-10% fee)
```

**Potential fiscal sponsors for crypto-native projects:**
- **The Giving Block** — specializes in crypto donations, works with DAOs
- **Network for Good** — established fiscal sponsor, digital-first
- **Players Philanthropy Fund** — works with innovative projects
- **Endaoment** — crypto-native, DAO-friendly

**Cost:** 5-10% of donations + $500-$2,000 setup fee.

### 4.4 Pathway C: DUNA's Own 501(c)(3) (6-12 Months)

The long-term solution. The DUNA applies for IRS 501(c)(3) tax-exempt status. Once approved, the DUNA can issue its own tax-deductible receipts directly — no intermediary needed.

**Flow:**
```
Impact fund → DUNA bank account → Tax-deductible receipt from DUNA
                         ↓
              Tree planting / carbon credits / operations
```

**Requirements:**
- DUNA must be formed and operating
- Tax attorney or CPA specializing in nonprofit exemption ($2K-$10K)
- 6-12 month IRS processing time
- Ongoing compliance: annual IRS Form 990, public disclosure

### 4.5 Recommendation

| Phase | Pathway | Timeline | Cost |
|-------|---------|----------|------|
| **Now** | Form DUNA → open bank account → accept direct donations (Pathway A) | 1-4 weeks | ~$50 gas |
| **Next** | Engage fiscal sponsor for tax-deductible receipts (Pathway B) | 1-3 months | $500-$2K + 5-10% fee |
| **Long-term** | Apply for DUNA's own 501(c)(3) (Pathway C) | 6-12 months | $2K-$10K |

**The DUNA is the prerequisite for all three pathways.** Without it, impact funds have no entity to write checks to at all.

---

## 5. Option Analysis

### 5.1 Option A: Wyoming UNA → DUNA (Recommended)

**What it is:** A Wyoming Unincorporated Nonprofit Association (UNA) — the simpler precursor to the Decentralized Unincorporated Nonprofit Association (DUNA). Formed on-chain via [OtoCo](https://otoco.io). Auto-converts to DUNA when membership reaches 100.

| Dimension | Detail |
|-----------|--------|
| **Liability** | Members shielded from personal liability for DAO obligations |
| **Tax status** | Nonprofit entity; can apply for 501(c)(3) tax-exempt status with IRS |
| **Governance** | Smart contract-based voting explicitly recognized by law |
| **Minimum members** | None for UNA; 100 for DUNA (auto-conversion) |
| **Profit distribution** | ❌ Not allowed — all revenue must be reinvested in mission |
| **Formation cost** | ~$50 gas ([OtoCo](https://otoco.io) smart contract, 2+ wallets sign) |
| **Annual cost** | $60-$200 license tax; no Wyoming state income tax |
| **Bank account** | Can open US bank account with EIN |
| **Time to form** | 1 day (OtoCo) |
| **CTA reporting** | Only Gary (40.76%) — all others pseudonymous |

**✅ Pros:**
- Near-free formation (~$50 gas) — well within $4,126 available treasury
- Perfect mission alignment (nonprofit, rainforest restoration)
- Impact funds can write checks immediately (Pathway A)
- Fiscal sponsorship available for tax-deductible receipts (Pathway B)
- 501(c)(3) pathway available long-term (Pathway C)
- Legal recognition of on-chain governance
- Clean answer for TDG holders
- Own bank account — Gary's personal account removed from flow
- Auto-converts to DUNA at 100 members
- No state income tax (Wyoming)

**❌ Cons:**
- Cannot distribute profits to TDG holders (nonprofit constraint)
- 501(c)(3) application takes 6-12 months
- Fiscal sponsor takes 5-10% fee
- Cross-border (Brazil) ownership needs legal counsel

### 5.2 Option B: Wyoming DAO LLC (Alternative)

**What it is:** A Wyoming DAO LLC — a for-profit limited liability company with DAO governance recognized by Wyoming law. Allows profit distribution to token holders.

| Dimension | Detail |
|-----------|--------|
| **Liability** | Members shielded from personal liability |
| **Tax status** | For-profit LLC — taxed as partnership or corporation |
| **Governance** | Smart contract-based voting explicitly recognized by law |
| **Minimum members** | None |
| **Profit distribution** | ✅ Allowed — profits can be distributed to TDG holders |
| **Formation cost** | ~$100 filing + legal fees ($2K-$5K) |
| **Annual cost** | $60-$200 license tax |
| **Bank account** | Can open US bank account with EIN |
| **Time to form** | 1-2 weeks (filing) |
| **CTA reporting** | All members with >25% ownership |

**✅ Pros:**
- Profit distribution to TDG holders
- Familiar structure (LLC)
- Can own Brazilian CNPJ directly

**❌ Cons:**
- ❌ **Cannot accept tax-deductible donations** — impact funds, foundations, corporate ESG have no channel
- ❌ **No 501(c)(3) pathway** — for-profit entity cannot become a nonprofit
- ❌ **Mission misalignment** — for-profit structure contradicts rainforest restoration mission
- Higher legal costs ($2K-$5K)
- More CTA reporting (anyone >25%)

### 5.3 Comparison

| Factor | UNA → DUNA (Recommended) | DAO LLC |
|--------|--------------------------|---------|
| Formation cost | ~$50 gas | $2K-$5K |
| Impact fund channel | ✅ Yes (3 pathways) | ❌ No |
| Tax-deductible donations | ✅ Via fiscal sponsor or 501(c)(3) | ❌ Never |
| Profit distribution | ❌ Not allowed | ✅ Allowed |
| Mission alignment | ✅ Perfect (nonprofit) | ❌ For-profit |
| CTA reporting | 1 person (Gary) | Anyone >25% |
| Bank account | ✅ Yes | ✅ Yes |
| Brazil CNPJ ownership | ⚠️ Needs legal counsel | ✅ Direct |

---

## 6. Implementation Timeline

| Phase | What | Cost | Timeline | % of Treasury |
|-------|------|------|----------|--------------|
| **Phase 1a: This week** | TrueTech Inc opens Wise Business account (interim) | $0-500 | 1-2 weeks | 0-12% |
| **Phase 1b: This week** | Gary + TrueTech Inc sign OtoCo → UNA formed | ~$50 gas | 1 day | ~1.2% |
| **Phase 2: Next 2-4 weeks** | UNA gets EIN → opens its own Wise Business account | $0 | 2-4 weeks | 0% |
| **Phase 3: After UNA account** | Migrate partner flows to UNA account. Begin accepting direct donations (Pathway A). | $0 | Ongoing | 0% |
| **Phase 4: 1-3 months** | Engage fiscal sponsor for tax-deductible receipts (Pathway B) | $500-$2K + 5-10% fee | 1-3 months | 12-48% |
| **Phase 5: 6-12 months** | 501(c)(3) application via tax attorney (Pathway C) | $2K-$10K | 6-12 months | 48-242%* |
| **Phase 6: Future** | DUNA-owned Brazilian CNPJ | $1K-$3K | After DUNA | 24-73%* |

*\*Requires fundraising or revenue growth before proceeding.*

---

## 7. Resource Gap Analysis

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
| **Wise banking relationship** | ✅ Existing | Already using Wise for Brazil transfers. Can open business accounts for both entities. |

### ❌ What We Need to Acquire

| # | Need | Severity | Why | Est. Cost |
|---|------|----------|-----|-----------|
| 1 | **Legal counsel (DUNA → Brazil CNPJ)** | 🟡 Medium | Cross-border entity ownership needs a lawyer familiar with both Wyoming DUNA law and Brazilian corporate law | $5K-15K |
| 2 | **501(c)(3) tax attorney** | 🟡 Medium | IRS tax exemption application requires specialized expertise | $2K-10K |
| 3 | **Fiscal sponsor relationship** | 🟡 Medium | Need to identify and engage a fiscal sponsor for tax-deductible donations | $500-$2K + 5-10% fee |
| 4 | **Brazilian legal representative** | 🟡 Medium | Brazilian LTDA requires a local lawyer as legal representative | $1K-3K |
| 5 | **Multi-entity accounting** | 🟢 Low | Three entities need consolidated bookkeeping | $2K-5K/yr |

---

## 8. Questions for SVH Capital (June 26)

1. **DUNA formation:** Do you work with or can you refer us to a Wyoming law firm that specializes in DUNA formation for DAOs? (Hathaway & Kunz, Astraea, etc.)

2. **Cost efficiency:** What's the leanest way to get a DUNA in place — full-service law firm or is OtoCo's on-chain UNA → DUNA path sufficient for our stage?

3. **501(c)(3) pathway:** Once DUNA is formed, what's the realistic timeline and cost for the IRS exemption application for a DAO that plants trees?

4. **Fiscal sponsorship:** Do you know any fiscal sponsors that work well with crypto-native / DAO projects? We want to start accepting tax-deductible donations while our own 501(c)(3) processes.

5. **Impact fund capital:** Can a Wyoming DUNA accept direct donations from impact funds without 501(c)(3) status? Are there any restrictions on the types of capital a DUNA can receive?

6. **Brazilian entity:** Can a Wyoming DUNA own or affiliate with a Brazilian LTDA, or does that need a separate US holding LLC in between?

7. **Governance clarity:** We have a for-profit C-corp (TrueTech Inc) operating as a DAO facility for customs/FDA compliance. How do we structure the DUNA so TDG holders are clearly voting on DUNA matters, and TrueTech Inc is clearly a facility executing on DUNA decisions — not the thing being governed?

8. **TDG buyback → burn:** Can TrueTech Inc (Delaware C-corp, DAO-operated facility) buy and burn TDG tokens from the DApp as an operational expense, without creating governance or nonprofit distribution concerns?

---

## 9. Service Provider Reference

| Service | Purpose | Link | Cost |
|---------|---------|------|------|
| **OtoCo** | On-chain UNA formation (smart contract + 2 wallets) | https://otoco.io | ~$50 gas |
| **Skala.io** | Alternative UNA formation with pre-filled bank apps | https://skala.io | Custom pricing |
| **Wise** | Business bank account for TrueTech Inc + DUNA | https://wise.com | $0 setup, per-transaction fees |
| **Mercury** | Backup bank option (crypto-friendly) | https://mercury.com | $0 |
| **Relay** | Backup bank option (smaller, more flexible) | https://relayfi.com | $0 |
| **IRS EIN** | Free Employer Identification Number | https://www.irs.gov/ein | $0 |
| **Wyoming SOS** | Wyoming Secretary of State — business entity search | https://wyoming.gov | N/A |
| **The Giving Block** | Fiscal sponsor for crypto-native projects | https://thegivingblock.com | 5-10% fee |
| **Endaoment** | Crypto-native fiscal sponsor, DAO-friendly | https://endaoment.org | Variable |

---

## 10. Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **UNA can't open bank account quickly** | 🟡 Medium | TrueTech Inc Wise account serves as interim custodian. No operational delay. |
| **Wise rejects UNA application** | 🟡 Medium | Fall back to Mercury or Relay. Or keep TrueTech Inc as custodian longer. |
| **501(c)(3) takes longer than expected** | 🟢 Low | DUNA can operate without 501(c)(3) — just can't issue tax-deductible receipts. Use fiscal sponsorship bridge (Pathway B). |
| **Fiscal sponsor not available for DAOs** | 🟡 Medium | The Giving Block and Endaoment both work with DAOs. If not, use Pathway A (direct donations) until 501(c)(3) is obtained. |
| **Brazil CNPJ ownership complex** | 🟡 Medium | Add a US holding LLC between DUNA and Brazilian LTDA. Adds ~$100/yr in filing costs. |
| **Single-person dependency (Brazil)** | 🔴 High | Matheus's private CNPJ is the only export channel. Mitigation: DUNA-owned CNPJ as eventual structure. |
| **CTA reporting changes** | 🟢 Low | Only Gary reports currently. If regulations change, reassess. |

---

## Appendix: OtoCo UNA Formation Steps

1. Go to https://otoco.io
2. Connect wallet (MetaMask or compatible)
3. Select "Summon a UNA"
4. 2+ wallet addresses sign the smart contract
5. Pay gas (~$50 on Ethereum L1 or L2)
6. UNA is formed — receive UNA Declaration + Operating Agreement
7. Apply for EIN at https://www.irs.gov/ein (free, online)
8. Open Wise Business account using UNA's EIN
9. When membership exceeds 100 wallets, UNA auto-converts to DUNA

---

*Prepared by Sophia Truesight (admin+sophia@truesight.me)*
*TrueSight DAO Autopilot*