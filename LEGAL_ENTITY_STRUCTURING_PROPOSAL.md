# Legal Entity Structuring Proposal

**TrueSight DAO** | Prepared for SVH Capital Meeting — June 26, 2025

---

## Executive Summary

The TrueSight DAO is at an inflection point. Partner onboarding is accelerating (Nora's Kopi Bar, Kirsten's network, Matheus's Brazil operations), and the volume of funds flowing through the network is scaling. Currently, funds flow through Gary's personal bank account and Matheus's private Brazilian CNPJ — both single points of failure and liability exposure.

**The core problem:** The DAO needs a legal wrapper — not just for tax write-offs, but for:
1. **Member liability shield** — Ooki DAO precedent means unincorporated DAO members can be treated as general partners
2. **DAO bank account** — funds should not flow through any individual's personal account
3. **Institutional fundraising channel** — impact funds, foundations, and corporate ESG need a tax-deductible donation pathway

**The proposed solution:** A Wyoming UNA (Unincorporated Nonprofit Association) formed via OtoCo, which auto-converts to a DUNA (Decentralized Unincorporated Nonprofit Association) when membership exceeds 100. TrueTech Inc operates as a voluntary DAO member, not a separate legal layer. Wise serves as the single banking platform for both entities.

---

## Section 1: The Simplified Model

### Core Structure

```
Wyoming UNA/DUNA (nonprofit, 501(c)(3) aspirant)
    ↓ Holds: mission, brand, carbon credits, treasury
    ↓ Governed by: all TDG holders
    ↓ Bank: Wise Business account

TrueTech Inc (Delaware C-corp, DAO member)
    ↓ Role: import, distribution, payment processing
    ↓ Compensated in: TDG (like any other contributor)
    ↓ Bank: Wise Business account (interim, then separate)

Brazilian LTDA (CNPJ) — eventual DUNA-owned
    ↓ Role: farmer payments, export documentation
    ↓ Currently: Matheus's private CNPJ
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **TrueTech Inc = DAO member** | No service agreement needed. TrueTech Inc contributes voluntarily, compensated in TDG like Nora, Kirsten, Matheus. |
| **UNA → DUNA auto-conversion** | OtoCo handles this via smart contract when membership hits 100. Same EIN, same bank account. |
| **Wise as single banking layer** | Both TrueTech Inc and the DUNA use Wise Business accounts. Same API, same Brazil pipeline, multi-currency support. |
| **Brazil CNPJ eventually DUNA-owned** | Removes single-person dependency on Matheus. Requires cross-border legal counsel. |

---

## Section 2: Financial Flow

### Current Flow

```
Nora / partners → Gary's personal bank account → tree planting / expenses
Brazil farmers → Matheus's private CNPJ → export → TrueTech Inc
```

### Interim Flow (this week — TrueTech Inc Wise account)

```
Nora / partners → TrueTech Inc Wise Business → tree planting / expenses
Brazil farmers → Matheus's private CNPJ → export → TrueTech Inc
```

### Target Flow (after UNA bank account)

```
Nora / partners → UNA Wise Business → tree planting / expenses
Brazil farmers → DUNA-owned CNPJ → export → UNA Wise Business
TrueTech Inc Wise → import/distribution expenses only
```

---

## Section 3: CTA Beneficial Ownership — Who Reports

The Corporate Transparency Act (CTA) requires reporting Beneficial Ownership Information (BOI) to FinCEN for anyone who exercises "substantial control" over the entity or owns ≥25% of its ownership interests.

### "Substantial Control" Defined

Under the CTA, an individual has substantial control if they:
1. Serve as a senior officer (CEO, CFO, COO, etc.)
2. Have authority to appoint or remove senior officers or a majority of the board
3. Have substantial influence over important decisions — including:
   - Authority over bank accounts or treasury
   - Authority over smart contract upgrades or governance parameters
   - Power to bind the entity to contracts
   - Control over the entity's direction or purpose

### How This Maps to Our DAO

From the Contributors Voting Weight ledger (Sheet ID: 1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU, gid=1460794618):

| Rank | Contributor | % Controlled | CTA Trigger? |
|------|------------|-------------|--------------|
| 1 | **Gary Teh** | **40.76%** | ✅ **Yes** — >25% threshold + substantial control |
| 2 | Garis Pang | 2.89% | ❌ No |
| 3 | Fatima Toledo | 2.81% | ❌ No |
| 4-350+ | All others | <3% each | ❌ No |

**Result:** Only Gary needs to report name, DOB, address, and ID for the CTA BOI filing. The other ~350 TDG holders remain pseudonymous — wallet address only.

**For the initial UNA formation (2 signers):** Gary + TrueTech Inc representative. Both provide their personal information for the CTA filing and Wise bank signatory requirements.

---

## Section 4: Implementation Timeline

| Phase | What | Cost | Timeline | % of Treasury |
|-------|------|------|----------|--------------|
| **Phase 1a: This week** | TrueTech Inc opens Wise Business account (interim) | $0-500 | 1-2 weeks | 0-12% |
| **Phase 1b: This week** | Gary + TrueTech Inc sign OtoCo → UNA formed | ~$50 gas | 1 day | ~1.2% |
| **Phase 2: Next 2-4 weeks** | UNA gets EIN → opens its own Wise Business account | $0 | 2-4 weeks | 0% |
| **Phase 3: After UNA account** | Migrate partner flows to UNA Wise account | $0 | Ongoing | 0% |
| **Phase 4: 6-12 months** | 501(c)(3) application via tax attorney | $2K-10K | 6-12 months | 48-242%* |
| **Phase 5: Future** | DUNA-owned Brazilian CNPJ | $1K-3K | After DUNA | 24-73%* |

*\*Requires fundraising or revenue growth before proceeding.*

### Available Treasury

Only the **Main Ledger** cash is available for deployment. Managed ledgers are earmarked for cacao shipment financing.

| Account | Amount | Available? |
|---------|--------|-----------|
| Main Ledger USD | $3,476.27 | ✅ Yes |
| Main Ledger USDT | $66.93 | ✅ Yes |
| Main Ledger Brazilian Reis | ~$583.53 | ✅ Yes |
| **Total Available** | **~$4,126.73** | ✅ Yes |
| Managed Ledgers | Various | ❌ No — earmarked for cacao shipments |

---

## Section 5: Resource Gap Analysis

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
| 3 | **Brazilian legal representative** | 🟡 Medium | Brazilian LTDA requires a local lawyer as legal representative | $1K-3K |
| 4 | **Multi-entity accounting** | 🟢 Low | Three entities need consolidated bookkeeping | $2K-5K/yr |

---

## Section 6: Governance Clarity — The Story for TDG Holders

When TDG holders ask "what entity am I voting on?", the answer is:

> *"TDG holders govern the TrueSight DAO community — its mission, its partnerships, its reforestation commitments. TrueTech Inc is a DAO member who contributes import and distribution services voluntarily, compensated in TDG like any other contributor. The Wyoming UNA/DUNA is the legal wrapper that formalizes this. When you vote with TDG, you're voting on the DAO's direction — and eventually, the DUNA's governance."*

**Key points:**
- TrueTech Inc is not the DAO — it's a member of the DAO
- TDG voting rights govern the mission, not a corporation
- The UNA/DUNA provides the legal wrapper without changing who holds power
- Only Gary (40.76% holder) needs to report under CTA — everyone else stays pseudonymous

### TDG Buyback & Exit Liquidity

If a TDG holder wants to sell their tokens, the UNA/DUNA could use its treasury to buy TDG from the DApp, providing exit liquidity. This is a treasury management decision voted on by TDG holders. The UNA holds the purchased TDG as an asset on its balance sheet.

**Question for SVH:** Can a Wyoming UNA/DUNA use its treasury to purchase its own membership tokens (TDG) from members on a secondary market (our DApp) as a liquidity provision mechanism?

---

## Section 7: Questions for SVH Capital (June 26)

1. **DUNA formation:** Do you work with or can you refer us to a Wyoming law firm that specializes in DUNA formation for DAOs? (Hathaway & Kunz, Astraea, etc.)

2. **Cost efficiency:** What's the leanest way to get a DUNA in place — full-service law firm or is OtoCo's on-chain UNA → DUNA path sufficient for our stage?

3. **501(c)(3) pathway:** Once DUNA is formed, what's the realistic timeline and cost for the IRS exemption application for a DAO that plants trees?

4. **TDG as compensation:** Would your referred counsel consider a partial TDG token grant to reduce the cash outlay?

5. **Brazilian entity:** Can a Wyoming DUNA own or affiliate with a Brazilian LTDA, or does that need a separate US holding LLC in between?

6. **Governance clarity:** We have a for-profit C-corp (TrueTech Inc) as a voluntary DAO member and a DAO with token voting rights. How do we structure the UNA/DUNA so TDG holders are clearly voting on DAO matters, and TrueTech Inc is clearly a member — not the thing being governed?

7. **TDG buyback:** Can a Wyoming UNA/DUNA use its treasury to purchase its own membership tokens (TDG) from members on a secondary market (our DApp) as a liquidity provision mechanism? If a member wants to exit, can the UNA buy their TDG back without triggering nonprofit distribution concerns?

---

## Section 8: Service Provider Reference

| Service | Purpose | Link | Cost |
|---------|---------|------|------|
| **OtoCo** | On-chain UNA formation (smart contract + 2 wallets) | https://otoco.io | ~$50 gas |
| **Skala.io** | Alternative UNA formation with pre-filled bank apps | https://skala.io | Custom pricing |
| **Wise** | Business bank account for TrueTech Inc + eventual DUNA | https://wise.com | $0 setup, per-transaction fees |
| **Mercury** | Backup bank option (crypto-friendly) | https://mercury.com | $0 |
| **Relay** | Backup bank option (smaller, more flexible) | https://relayfi.com | $0 |
| **IRS EIN** | Free Employer Identification Number | https://www.irs.gov/ein | $0 |
| **Wyoming SOS** | Wyoming Secretary of State — business entity search | https://wyoming.gov | N/A |

---

## Section 9: Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **UNA can't open bank account quickly** | 🟡 Medium | TrueTech Inc Wise account serves as interim custodian. No operational delay. |
| **Wise rejects UNA application** | 🟡 Medium | Fall back to Mercury or Relay. Or keep TrueTech Inc as custodian longer. |
| **501(c)(3) takes longer than expected** | 🟢 Low | DUNA can operate without 501(c)(3) — just can't issue tax-deductible receipts. Fundraising can proceed via grants and impact investments. |
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