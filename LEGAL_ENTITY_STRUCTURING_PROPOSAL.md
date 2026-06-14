# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** Friday Tech Fest signals + SVH Capital cacao circle on June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## 1. Executive Summary

The convergence is accelerating. Nora (Kopi Bar, Berkeley) is onboarding. More partners are joining. Matheus channels exports through his private Brazilian entity. TrueTech Inc (Delaware C-corp) handles import and distribution. Gary's personal bank account collects funds.

This worked at pilot scale. But three signals are turning from grey to red:

| Signal | Status | Why Now |
|--------|--------|---------|
| **DAO legal wrapper** | 🔴 Red | Member liability shield (Ooki DAO precedent), DAO bank account, governance clarity for TDG holders |
| **Tax-deductible donation channel** | 🟡 Yellow | Impact funds, corporate ESG, foundations need a 501(c)(3) to write checks |
| **Personal bank account** | 🔴 Red | Gary's personal account is the bottleneck — more volume = more personal risk |

### The core insight

**TrueTech Inc is just another DAO member.** It contributes voluntarily (import, distribution) and gets compensated in TDG — same as Nora, Kirsten, Matheus, or any other partner. No service agreement needed. No principal-agent complexity.

**The UNA opens its own bank account.** No need for TrueTech Inc to act as custodian. No need for a TrueTech Inc business account as an interim step. Funds flow directly from partners → UNA bank account → tree planting. Gary's personal account is completely out of the picture.

**The Brazilian CNPJ should eventually be owned by the DUNA,** not by Matheus personally. This ensures the export channel is a DAO asset, not dependent on any single individual.

**Only one person needs to report under the CTA.** Gary (40.76% TDG control) is the sole beneficial owner. Every other TDG holder remains pseudonymous — wallet address only. No cascading KYC.

### Recommended structure

```
Wyoming UNA/DUNA (nonprofit, DAO legal wrapper)
    ├── Own bank account (receives partner contributions)
    ├── TDG holders govern the UNA (pseudonymous — wallet only)
    ├── TrueTech Inc = DAO member (voluntary contributor)
    └── Brazilian LTDA (CNPJ) = export/sourcing entity (DUNA-owned)
```

---

## 2. Current State Assessment

### 2.1 Financial Flows

**Current (problematic):**
```
Brazil Farmers → Matheus (private CNPJ) → Export → TrueTech Inc → Gary's personal bank account → DAO expenses
```

**Target (with UNA bank account + DUNA-owned CNPJ):**
```
Brazil Farmers → DUNA-owned CNPJ → Export → TrueTech Inc (import/dist, DAO member) → UNA bank account → tree planting / DAO expenses
```

Gary's personal account and Matheus's private CNPJ are both removed from the flow.

**Risks in current flow:**

| Risk | Severity | Detail |
|------|----------|--------|
| Personal liability | 🔴 High | Gary's personal account commingles DAO funds with personal funds |
| No member liability shield | 🔴 High | Token holders could be treated as general partners (per Ooki DAO precedent) |
| No tax-advantaged donation pathway | 🔴 High | Impact funds, foundations, corporate ESG have no channel |
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

> *"You're voting on the DAO community itself. TrueTech Inc is our operational partner, not the DAO. We're in the process of forming a Wyoming DUNA that will become the formal legal wrapper."*

A UNA/DUNA solves it cleanly:

> *"TDG holders govern the TrueSight UNA — a Wyoming nonprofit association. The UNA holds the mission, the brand, the carbon credit rights, and its own bank account. TrueTech Inc is one of our DAO members. When you vote with TDG, you're voting on UNA matters."*

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

## 4. Option Analysis

### 4.1 Option A: Wyoming UNA → DUNA (Recommended)

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
- Impact funds can write tax-deductible checks (if 501(c)(3) obtained later)
- Legal recognition of on-chain governance
- Clean answer for TDG holders
- Own bank account — Gary's personal account removed from flow
- Auto-converts to DUNA at 100 members
- No state income tax (Wyoming)
- Only 1 person reports under CTA — everyone else stays pseudonymous

**❌ Cons:**
- Cannot distribute profits to TDG token holders
- IRS 501(c)(3) application is separate (6-12 months, $2K-$10K)
- Some banks may hesitate to open accounts for a fresh UNA
- US nexus exposes DAO to US jurisdiction

### 4.2 Option B: Wyoming DAO LLC (For-Profit)

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
- Can distribute profits to TDG holders
- No minimum membership requirement
- Pass-through taxation avoids double taxation

**❌ Cons:**
- ❌ Cannot issue tax-deductible receipts (not a nonprofit)
- Impact funds cannot write tax-deductible checks
- Less mission-aligned than UNA/DUNA
- Higher formation cost ($15K+) — exceeds available treasury
- Governance story is murkier

### 4.3 Option C: Brazilian CNPJ (LTDA) — DUNA-Owned

| Dimension | Detail |
|-----------|--------|
| **Formation cost** | $1,000-$3,000 |
| **Annual cost** | $500-$2,000 (accounting + compliance) |
| **Time to form** | 4-8 weeks |
| **Foreign ownership** | 100% allowed |

**✅ Pros:** Formalizes exports, Brazilian tax compliance, farmer contracting, removes single-person dependency
**❌ Cons:** Bureaucratic, consumes significant portion of available treasury ($1K-$3K of $4,126)

---

## 5. Recommended Path: OtoCo UNA → Bank Account

### Step 1: Form the UNA (This Week)

Gary + TrueTech Inc (2 wallets) sign [OtoCo's](https://otoco.io) on-chain UNA smart contract.
- **Cost:** ~$50 gas
- **Time:** 1 day
- **Result:** Wyoming UNA formed. Legal personhood achieved. Liability shield active.

### Step 2: Get EIN + Open Bank Account (Next 2-4 Weeks)

1. UNA applies for IRS EIN (free, online)
2. UNA opens a **[Wise Business](https://wise.com)** account (we already use Wise for Brazil transfers)
3. If Wise won't accept a fresh UNA, fall back to **[Mercury](https://mercury.com)** or **[Relay](https://relayfi.com)**

**Important:** The UNA → DUNA conversion (at 100 members) uses the **same EIN and same bank account**. No reset needed.

### Step 3: Route Partner Contributions Through the UNA Account

```
Nora's coffee sales → UNA bank account → tree planting
Other partner contributions → UNA bank account → DAO expenses
```

TrueTech Inc continues handling import and distribution as a DAO member, compensated in TDG. It doesn't need to touch the DAO's money.

### Step 4 (Later): Form DUNA-Owned Brazilian CNPJ

Once the UNA is established and cash flow allows, form a Brazilian LTDA owned by the DUNA to replace Matheus's private CNPJ.
- Cost: $1,000-$3,000
- Timeline: After UNA bank account is operational
- Result: Export channel becomes a DAO asset, not dependent on any single individual

### Why this works

| Before | After |
|--------|-------|
| Gary's personal account collects all funds | UNA bank account collects DAO funds |
| Gary bears personal liability | UNA provides liability shield |
| Matheus's private CNPJ is the export channel | DUNA-owned CNPJ is the export channel |
| TDG holders vote on "the community" | TDG holders vote on the UNA |
| No clear answer for impact funds | UNA can pursue 501(c)(3) |
| TrueTech Inc needed as custodian | TrueTech Inc is just a member |
| 350+ TDG holders potentially exposed to KYC | Only Gary reports — everyone else pseudonymous |

---

## 6. Cost Analysis

### Path A: OtoCo UNA → Bank Account (Recommended — Do Now)

| Item | Cost |
|------|------|
| [OtoCo](https://otoco.io) smart contract (2+ wallets) | ~$50 gas |
| [IRS EIN application](https://www.irs.gov/ein) | Free |
| Bank account minimum deposit | $0-$500 |
| Annual Wyoming license tax | $60-$200/yr |
| Registered agent | $100-$200/yr |
| **Total Year 1** | **~$250-$750** |
| **% of available treasury** | **~6-18%** |

### Path B: Full DUNA via Law Firm (Future, If Needed)

| Item | Cost |
|------|------|
| State filing | $100 |
| Legal fees | $20,000-$60,000 |
| Annual costs | $200-$400/yr |
| **Total Year 1** | **~$20,500-$60,500** |
| **% of available treasury** | **~500-1,500%** — requires fundraising |

### Path C: Brazilian LTDA (DUNA-Owned)

| Item | Cost |
|------|------|
| Formation | $1,000-$3,000 |
| Annual compliance | $500-$2,000/yr |
| **% of available treasury** | **~24-73%** — significant but feasible |

### Path D: 501(c)(3) Application (Downstream)

| Item | Cost |
|------|------|
| Tax attorney | $2,000-$10,000 |
| IRS filing fee | $600-$2,500 |
| Timeline | 6-12 months |

---

## 7. Resource Gap Analysis

### ✅ What We Have

| Resource | Status |
|----------|--------|
| Mission clarity (10,000 hectares) | ✅ Strong |
| On-chain governance (TDG, Edgar API) | ✅ Strong |
| Physical supply chain (Brazil → US → retail) | ✅ Strong |
| Tree-planting pipeline (sunmint, lineage-credentials) | ✅ Strong |
| Partner network (Nora, Kirsten, Matheus) | ✅ Growing |
| Technical infrastructure (AWS, QR inventory) | ✅ Strong |
| SVH Capital connection (June 26) | ✅ Warm intro |
| Available cash for formation | ✅ ~$4,126 (enough for OtoCo + bank account) |

### ❌ What We're Missing

| Gap | Severity | Cost to Resolve |
|-----|----------|-----------------|
| Legal counsel for DUNA/501(c)(3) | 🟡 Medium | $50 (OtoCo) or $20K-$60K (full-service) |
| 100 DUNA members | 🟢 Low | $0 (use UNA workaround) |
| 501(c)(3) expertise | 🟡 Medium | $2K-$10K (later) |
| Brazilian legal rep for CNPJ | 🟡 Medium | $1K-$3K (later) |
| Multi-entity accounting | 🟢 Low | $2K-$5K/yr (later) |

**Total cash needed for Year 1: ~$250-$750** — well within available treasury of ~$4,126.

---

## 8. Implementation Timeline

| Phase | What | Cost | Timeline |
|-------|------|------|----------|
| **Phase 1: This week** | Gary + TrueTech Inc sign OtoCo → UNA formed | ~$50 gas | 1 day |
| **Phase 2: Next 2-4 weeks** | UNA gets EIN → opens bank account (Wise) | $0-$500 | 2-4 weeks |
| **Phase 3: Ongoing** | Route partner contributions through UNA account | $0 | After bank account |
| **June 26** | Ask SVH Capital about DUNA + 501(c)(3) pathway | $0 | One conversation |
| **Later** | UNA auto-converts to DUNA at 100 members | $0 | Automatic |
| **Later** | Form DUNA-owned Brazilian LTDA | $1K-3K | 4-8 weeks |
| **Later** | 501(c)(3) application | $2K-10K | 6-12 months |

---

## 9. Questions for SVH Capital (June 26)

### Primary

1. **UNA bank account:** Will a freshly-formed Wyoming UNA (no credit history, no operating track record) be able to open a US bank account? Any recommended banks that work with DAO entities? We already use Wise for Brazil transfers — will they accept a UNA?

2. **DUNA formation:** Can you refer us to a Wyoming law firm specializing in DUNA formation? Or is the OtoCo UNA → DUNA path sufficient for our stage?

3. **Governance clarity:** Can a Wyoming UNA/DUNA issue TDG tokens to a for-profit C-corp (TrueTech Inc) as member compensation?

4. **501(c)(3) pathway:** Realistic timeline and cost for IRS exemption for a DAO that plants trees?

5. **DUNA-owned Brazilian CNPJ:** Can a Wyoming DUNA directly own a Brazilian LTDA? If not, what's the cleanest intermediate structure (e.g., US holding LLC owned by DUNA)?

6. **TDG as compensation:** Would your referred counsel consider a partial TDG token grant to reduce cash outlay?

### Secondary

7. What do impact funds look for in a DAO's legal structure before writing a check?
8. How should the UNA/DUNA structure carbon credit rights?
9. Is there a practical upper limit on UNA/DUNA members before compliance complexity increases?

---

## 10. Clarifying Questions for the DAO

1. Should TDG tokens represent membership in the UNA directly, or a separate membership token?
2. Is TrueTech Inc comfortable being a DAO member compensated in TDG, with no separate service agreement?
3. Should the UNA own the Brazilian LTDA directly, or via a separate holding LLC?
4. Apply for 501(c)(3) immediately after UNA formation, or wait for a donation track record?
5. Carbon credits: asset of the UNA (mission-locked) or TrueTech Inc (tradeable)?
6. When should we transition from Matheus's private CNPJ to a DUNA-owned CNPJ — immediately or after the UNA bank account is operational?

---

## 11. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Bank refuses to open account for fresh UNA | Medium | High | Use Mercury, Relay, or other DAO-friendly banks; have TrueTech Inc as backup custodian |
| IRS denies 501(c)(3) for DAO | Low | High | Clear charitable purpose; crypto-nonprofit precedent exists |
| Wyoming UNA/DUNA law changes | Low | Medium | Monitor; Wyoming is pro-DAO |
| Brazilian LTDA formation delays | Medium | Low | Matheus continues using private entity interim |
| TDG classified as security | Low | High | UNA membership tokens generally not securities; consult SVH-referred counsel |
| Insufficient treasury for full-service legal | High | Medium | OtoCo path costs ~$50; full-service requires fundraising first |

---

## 12. Appendix: Key Terms

| Term | Definition |
|------|------------|
| **DUNA** | Decentralized Unincorporated Nonprofit Association — Wyoming entity for DAOs (effective July 2024) |
| **UNA** | Unincorporated Nonprofit Association — simpler precursor to DUNA, no 100-member minimum |
| **DAO LLC** | Wyoming LLC with DAO designation under the DAO Supplement Act (2021) — for-profit |
| **LTDA** | Limitada — Brazilian limited liability company |
| **CNPJ** | Cadastro Nacional da Pessoa Jurídica — Brazilian federal tax ID for businesses |
| **501(c)(3)** | US IRS tax exemption for charitable, religious, educational organizations |
| **[OtoCo](https://otoco.io)** | On-chain entity formation platform — creates Wyoming UNAs/DUNAs via smart contract |
| **TDG** | TrueSight DAO Governance token — voting rights in the DAO |
| **CTA** | Corporate Transparency Act — US law requiring Beneficial Ownership Information reporting to FinCEN |
| **BOI** | Beneficial Ownership Information — report filed with FinCEN under the CTA |
| **FinCEN** | Financial Crimes Enforcement Network — US Treasury bureau |
| **[Mercury](https://mercury.com)** | DAO-friendly US bank (backup option) |
| **[Relay](https://relayfi.com)** | Small business banking (backup option) |
| **[Wise](https://wise.com)** | International money transfer and multi-currency business account provider |
| **Ooki DAO** | CFTC enforcement action establishing precedent that DAO token holders may be treated as general partners |
