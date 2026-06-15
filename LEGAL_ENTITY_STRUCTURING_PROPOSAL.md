# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** SVH Capital cacao circle — June 26
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
    └── Contractual relationship with TrueTech Inc

TrueTech Inc (Delaware C-corp, independent entity)
    ├── Own cap table and shareholders (Gary)
    ├── Own bank account (commercial operations: imports, sales, revenue)
    ├── May buy back TDG at NAV using operating cash reserves (discretionary)
    └── Buyback reserve formula published on truesight.me

Brazilian LTDA (CNPJ) = export facility (eventually DUNA-owned)
```

### Key design decisions

| Decision | Rationale |
|----------|-----------|
| **TrueTech Inc = independent entity** | Not a subsidiary of the DUNA. Separate cap table, separate shareholders. Contractual relationship, not structural. Avoids UBIT and 501(c)(3) jeopardy. |
| **Two separate bank accounts** | TrueTech Inc account: commercial operations (imports, sales, revenue). DUNA account: partner contributions, tree planting, impact fund capital. |
| **TDG buyback at NAV** | TrueTech Inc may buy back TDG at net asset value (total DAO assets ÷ total TDG issued) using its own operating cash reserves. This is a business decision, not a DUNA obligation. |
| **Buyback reserve formula on truesight.me** | The formula governing redemption capacity is published on the TrueSight DAO website. Buybacks are not guaranteed — they depend on available reserves calculated by the formula. |
| **UNA first, DUNA if eligible** | Wyoming DUNA requires 100+ members joined by mutual consent under a blockchain-based governance agreement. If we don't meet this, UNA is the current stopgap. No auto-upgrade from UNA to DUNA exists in statute. |
| **Wise as primary banking platform** | Both TrueTech Inc and DUNA use Wise Business accounts. Wise handles standard bank transfers and PIX. Non-standard rails (Venmo, Zelle, Western Union) are executed manually from TrueTech's bank account as needed. |
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
Brazil Farmers → DUNA-owned CNPJ → Export → TrueTech Inc (commercial) → TrueTech Inc account (import expenses)
Partners (Nora, etc.) → DUNA bank account → tree planting / DAO expenses
Impact funds → DUNA bank account → tree planting / carbon credits
Member exit → Member submits DApp withdrawal → TrueTech Inc may buy back at NAV → TDG deducted
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

> *"You're voting on the DAO community itself. TrueTech Inc is a separate independent company, not the DAO. We're in the process of forming a Wyoming DUNA that will become the formal legal wrapper."*

A UNA/DUNA solves it cleanly:

> *"TDG holders govern the TrueSight DUNA — a Wyoming nonprofit association. The DUNA holds the mission, the brand, the carbon credit rights, and its own bank account. TrueTech Inc is an independent company that has a contractual relationship with the DUNA — it handles commercial operations. When you vote with TDG, you're voting on DUNA matters."*

---

## 3. Beneficial Ownership & State Transparency Laws

### 3.1 Federal CTA — Moot

As of FinCEN's March 2025 interim final rule, all U.S.-formed entities and their U.S. beneficial owners are exempt from BOI reporting. "Reporting company" now means only foreign-formed entities registered to do business in a U.S. state.

A Wyoming UNA/DUNA is U.S.-formed. **Neither the entity nor Gary files BOI to FinCEN.** The CTA section from earlier versions of this document is no longer relevant.

### 3.2 State Transparency Laws — The Live Risk

The real compliance risk is at the state level:

| State | Law | Status | Impact on UNA/DUNA |
|-------|-----|--------|-------------------|
| **New York** | LLC Transparency Act | Effective Jan 1, 2026 | Requires beneficial owner disclosure for LLCs formed or registered in NY. Does not directly apply to Wyoming UNAs, but may affect NY-based members or operations. |
| **California** | Advancing its own version | In progress | Similar to NY. If passed, would require disclosure for entities operating in CA. |
| **Wyoming** | No state-level transparency law | N/A | Wyoming has no beneficial ownership registry. This is one of the advantages of forming here. |

**Current posture:** A Wyoming UNA/DUNA is not directly subject to any state transparency law. If the DAO later registers to do business in NY or CA (e.g., opens a physical office), those states' laws may apply. For now, no BOI filing is required at any level.

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

Once the DUNA is formed and has a bank account, impact funds can write checks directly. The donation is **not tax-deductible** for the fund, but many impact funds can still deploy capital via:
- **Program-Related Investments (PRIs)** — foundations can make PRIs without requiring 501(c)(3) status of the recipient
- **Direct impact investment** — fund tree planting in exchange for verified impact reports + future carbon credit rights
- **TDG as governance stake** — fund gets voting rights in the DUNA proportional to their contribution

**The pitch:**
> *"Fund tree planting through our Wyoming DUNA. You get verified impact reports, future carbon credits, and voting rights in the DAO that governs the reforestation pipeline. Tax-deductible receipts coming once we secure 501(c)(3) status."*

### 4.3 Pathway B: Fiscal Sponsorship Bridge (1-3 Months)

A fiscal sponsor (e.g. The Giving Block, Endaoment, Players Philanthropy Fund) acts as an umbrella 501(c)(3) that receives donations on the DUNA's behalf and issues tax-deductible receipts. The sponsor takes 5-10% as a fee.

**This is the fastest path to tax-deductible donations** — the DUNA doesn't need its own 501(c)(3) yet. The sponsor handles compliance.

### 4.4 Pathway C: DUNA's Own 501(c)(3) (6-12 Months)

The DUNA applies for IRS 501(c)(3) tax-exempt status. This requires a tax attorney or CPA specializing in nonprofit exemption ($2K-$10K). Once obtained, the DUNA can issue tax-deductible receipts directly.

**The key insight:** The DUNA is the prerequisite for all three pathways. Without it, impact funds have no entity to write checks to at all.

---

## 5. Implementation Timeline — Parallel Tracks

| Track | What | Cost | Timeline |
|-------|------|------|----------|
| **Track A: TrueTech Inc Wise** | Opens Wise Business account for commercial transactions (import, customs, FDA) | $0-500 | This week (1-2 days) |
| **Track B: UNA Formation** | Gary + TrueTech Inc sign OtoCo → UNA formed | ~$50 gas | This week (1 day) |
| **Track C: UNA Wise** | UNA gets EIN → opens its own Wise Business account for mission/treasury | $0 | 2-4 weeks (after UNA formed + EIN) |

**No dependency between tracks.** TrueTech Inc's account handles the commercial side immediately. The UNA account handles the mission side when it's ready.

### Full Timeline

| Phase | What | Cost | Timeline | % of Treasury |
|-------|------|------|----------|--------------|
| **Phase 1a: This week** | TrueTech Inc opens Wise Business account (commercial transactions) | $0-500 | 1-2 days | 0-12% |
| **Phase 1b: This week** | Gary + TrueTech Inc sign OtoCo → UNA formed | ~$50 gas | 1 day | ~1.2% |
| **Phase 2: Next 2-4 weeks** | UNA gets EIN → opens its own Wise Business account | $0 | 2-4 weeks | 0% |
| **Phase 3: After UNA account** | Migrate partner contributions (Nora, etc.) to UNA Wise account | $0 | Ongoing | 0% |
| **Phase 4: 1-3 months** | Fiscal sponsorship bridge for tax-deductible donations | $500-2K | 1-3 months | 12-48% |
| **Phase 5: 6-12 months** | 501(c)(3) application via tax attorney | $2K-10K | 6-12 months | 48-242%* |
| **Phase 6: Future** | DUNA-owned Brazilian CNPJ | $1K-3K | After DUNA | 24-73%* |

*\*Requires fundraising or revenue growth before proceeding.*

### 5.1 DUNA Formation — Requirements Check

Wyoming's DUNA statute requires:
- **100+ members** joined by mutual consent under a governing agreement
- **Blockchain-based governance** (smart contracts, token voting, etc.)
- **Election to form under the DUNA Act** (not auto-conversion from UNA)

**Important:** There is no statutory auto-upgrade from UNA to DUNA. The statute's automatic conversion runs downward only: if a DUNA falls below 100 members, it auto-converts into a plain Wyoming UNA. To form a DUNA, you must elect to form under the DUNA Act and meet its requirements.

**Current status:** We have ~350 contributors with TDG. The question is whether those 350 are "members by mutual consent" under a governing agreement. If yes, DUNA formation is possible now. If not, UNA is the current stopgap.

**Action item:** Verify with OtoCo whether their smart contract actually automates DUNA formation, or if that's a claim to confirm directly. If OtoCo only handles UNA formation, we may need a law firm for the DUNA.

---

## 6. TDG Governance Rights

### 6.1 What TDG Is

TDG tokens represent **voting rights in the DAO entity** (UNA or DUNA form). They are issued to contributors for work — cacao logistics, contribution scoring, software development, partner onboarding — and grant governance power over:
- The organization's strategic direction
- Budget allocation and program funding
- Partner relationships and reforestation commitments

**TDG is not a financial security or profit-sharing instrument.** It is a governance right that happens to be transferable/tradeable. This distinction is critical for securities law compliance.

### 6.2 Member Exit Options

Contributors can see in real time what liquidity capacity exists. If a contributor wants to exit, they have two options:

1. **Sell on the secondary market** — if liquidity exists and a buyer appears
2. **Request redemption from TrueTech at NAV** — subject to available reserves calculated by the published formula

### 6.3 Current Withdrawal Flow (Live Today)

When a member chooses to redeem, they use the existing DApp withdrawal page:

> **https://dapp.truesight.me/withdraw_voting_rights.html**

**The flow:**
```
1. Member connects wallet and signs in on the DApp
2. DApp shows their total voting rights, value per right, and available USD reserves
3. Member enters the number of voting rights to cash out
4. Member selects their Withdrawal Method from the dropdown:
   - PIX (Brazil) — handled via Wise
   - PayLah (Singapore)
   - Venmo (USA) — executed manually from TrueTech bank account
   - Zelle (USA) — executed manually from TrueTech bank account
   - PayPal (International)
   - WiseTransfer (International) — handled via Wise
   - Western Union (International) — executed manually from TrueTech bank account
5. Member enters their account details for the selected method
6. Member submits — request is recorded in the ledger
7. TrueTech Inc may buy back the TDG at NAV using operating cash reserves
8. Member's TDG balance is deducted from the ledger
9. TDG is effectively burned — removed from circulation
```

**Payout coverage note:** Wise handles standard bank transfers and PIX. Non-standard rails (Venmo, Zelle, Western Union) are executed manually by Gary from TrueTech's bank account as needed.

### 6.4 Buyback Reserve Formula

There is no separate "impact fund" backend or committed buyback reserve. TrueTech's buyback capacity is simply its **available operating cash flow**.

TrueTech's buyback reserve formula is published on **truesight.me** and calculated as:

> **Reserve = X% of monthly sales volume**

This formula determines what portion of TrueTech's revenue gets set aside for potential token redemptions versus reinvestment, operations, and growth. Reserve capacity scales with TrueTech sales volume per this published policy.

**Key characteristics:**
- Buybacks are **not guaranteed or promised** — available based on current reserves calculated by the published formula
- **Transparent and tied to business performance** — if sales grow, reserve capacity grows; if sales decline, redemption capacity declines
- **Discretionary on TrueTech's side** — TrueTech commits to the formula, not to individual redemption demands if reserves are insufficient
- TrueTech may also participate in secondary markets for TDG as a buyer if strategically sensible (e.g., buying at discount to retire and consolidate governance power)
- No Raydium or DEX swap involved
- No open market purchase — direct redemption against TrueTech's operating cash
- TDG is deducted from the ledger, reducing total supply
- Deflationary mechanism rewards remaining holders

### 6.5 What Exists Today

| Component | What It Does | Status |
|-----------|-------------|--------|
| **DApp withdrawal page** | Member signs in, sees balance, submits request | ✅ Live at dapp.truesight.me/withdraw_voting_rights.html |
| **Withdrawal Method dropdown** | PIX, PayLah, Venmo, Zelle, PayPal, WiseTransfer, Western Union | ✅ Live |
| **Ledger deduction** | TDG balance deducted on withdrawal | ✅ Live |
| **TrueTech Inc payout** | Cash issued to exiting member via selected method | ✅ Live |
| **Buyback budget automation** | GAS script calculates daily budget from 30-day sales × asset/TDG | ✅ Live ($0.093/day) |
| **Buyback price automation** | ASSET_PER_TDG_ISSUED calculated from total assets ÷ total TDG | ✅ Live ($0.0067/TDG) |
| **Reserve formula publication** | Published on truesight.me | ✅ Live |

### 6.6 What Changes with the DUNA

The buyback budget and price are already fully automated by the existing tokenomics GAS script:

| Metric | Formula | Current Value |
|--------|---------|--------------|
| **Buyback budget** | (30-day sales ÷ 30) × min(Asset/TDG, 1 - Treasury yield) | **$0.093/day** |
| **Buyback price** | Total DAO assets ÷ Total TDG issued | **$0.0067/TDG** |
| **Execution** | `createDailyTdgBuyBackTransactions()` — creates ledger entries daily | ✅ Automated |

With the DUNA, the only change is the source account — from Gary's personal account to TrueTech Inc's Wise account. The automation stays the same.

| Aspect | Today | With DUNA |
|--------|-------|-----------|
| **Who issues cash** | TrueTech Inc (from Gary's personal account) | TrueTech Inc (from its own Wise account via API) |
| **Who authorizes** | Automated — GAS script calculates budget daily | Same — DUNA governance can adjust formula |
| **Buyback price** | Automated — ASSET_PER_TDG_ISSUED ($0.0067) | Same — formula-driven |
| **Buyback budget** | Automated — $0.093/day from 30-day sales × asset/TDG | Same — scales with revenue |
| **TDG deduction** | Ledger entry | Same — ledger entry |
| **Transparency** | On-chain via Edgar API + Wise API reconciliation | Same |

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
| **Member exit mechanism** | ✅ Live | DApp withdrawal page + cash receipt channel + ledger deduction |
| **Buyback automation** | ✅ Live | Budget and price calculated daily by GAS script |
| **Reserve formula published** | ✅ Live | Published on truesight.me |

### ❌ What We Need to Acquire

| # | Need | Severity | Why | Est. Cost |
|---|------|----------|-----|-----------|
| 1 | **Legal counsel (DUNA formation)** | 🟡 Medium | Verify DUNA eligibility (100+ members by mutual consent) and formation path. Confirm OtoCo's DUNA claims. | $5K-15K |
| 2 | **501(c)(3) tax attorney** | 🟡 Medium | IRS tax exemption application requires specialized expertise | $2K-10K |
| 3 | **Brazilian legal representative** | 🟡 Medium | Brazilian LTDA requires a local lawyer as legal representative | $1K-3K |
| 4 | **Multi-entity accounting** | 🟢 Low | DUNA + TrueTech Inc + Brazilian LTDA need consolidated bookkeeping | $2K-5K/yr |

---

## 8. Questions for SVH Capital (June 26)

The original SVH approach was to seek advisory input on governance structure — that work is now complete via this discussion. The only remaining legal gate is a narrow **Howey analysis**: does issuing governance tokens (TDG) to contributors for work count as a security offering under SEC law?

This is a counsel question, not a strategic workshop. The structure is resolved. Bring this doc, flag the Howey question as the one thing requiring their legal review, and clarify that you're not seeking capital or advisory on impact mechanics.

1. **DUNA formation:** Can you refer us to a Wyoming law firm that specializes in DUNA formation? We need to verify whether our ~350 TDG holders qualify as "members by mutual consent."

2. **OtoCo verification:** OtoCo claims to automate UNA formation via smart contract. Do they also handle DUNA formation, or is that a separate process requiring a law firm?

3. **UNA vs. DUNA:** If we don't meet the 100-member threshold for DUNA, is a Wyoming UNA sufficient as a stopgap? What are the practical limitations?

4. **Howey analysis (the one thing):** TDG is issued to contributors for work (cacao logistics, contribution scoring, development, onboarding) and grants governance rights. It is not a financial security or profit-sharing instrument. Does this pass the Howey Test? This is the narrow legal question requiring their review.

5. **501(c)(3) pathway:** Once DUNA is formed, what's the realistic timeline and cost for IRS exemption for a DAO that plants trees?

6. **Brazilian entity:** Can a Wyoming DUNA own or affiliate with a Brazilian LTDA, or does that need a separate US holding LLC in between?

7. **TrueTech Inc independence:** TrueTech Inc is a separate Delaware C-corp with its own cap table and shareholders. Contractual relationship with DUNA, not structural. Does this avoid UBIT and 501(c)(3) jeopardy?

8. **TDG buyback:** TrueTech Inc may buy back TDG at NAV using operating cash, publishing a reserve formula on truesight.me. Buybacks discretionary, not guaranteed. Can this continue under a DUNA structure?

---

## 9. Service Provider Reference

| Service | Purpose | Link | Cost |
|---------|---------|------|------|
| **OtoCo** | On-chain UNA formation (smart contract + 2 wallets) | https://otoco.io | ~$50 gas |
| **Skala.io** | Alternative UNA formation with pre-filled bank apps | https://skala.io | Custom pricing |
| **Wise** | Business bank account for TrueTech Inc + eventual DUNA | https://wise.com | $0 setup, per-transaction fees |
| **Mercury** | Backup bank option (crypto-friendly) | https://mercury.com | $0 |
| **Relay** | Backup bank option (smaller, more flexible) | https://relayfi.com | $0 |
| **IRS EIN** | Free Employer Identification Number | https://www.irs.gov/ein | $0 |
| **Wyoming SOS** | Wyoming Secretary of State — business entity search | https://wyoming.gov | N/A |
| **The Giving Block** | Fiscal sponsorship for crypto-native nonprofits | https://thegivingblock.com | 5-10% fee |
| **Endaoment** | On-chain fiscal sponsorship for DAOs | https://endaoment.org | Variable |

---

## 10. Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **UNA can't open bank account quickly** | 🟡 Medium | TrueTech Inc Wise account serves as interim. No operational delay. |
| **Wise rejects UNA application** | 🟡 Medium | Fall back to Mercury or Relay. Or keep TrueTech Inc as custodian longer. |
| **501(c)(3) takes longer than expected** | 🟢 Low | DUNA can operate without 501(c)(3) — just can't issue tax-deductible receipts. Fundraising can proceed via grants and impact investments. |
| **Brazil CNPJ ownership complex** | 🟡 Medium | Add a US holding LLC between DUNA and Brazilian LTDA. Adds ~$100/yr in filing costs. |
| **Single-person dependency (Brazil)** | 🔴 High | Matheus's private CNPJ is the only export channel. Mitigation: DUNA-owned CNPJ as eventual structure. |
| **DUNA eligibility unclear** | 🟡 Medium | Need legal counsel to verify whether ~350 contributors qualify as "members by mutual consent." If not, UNA is the stopgap. |
| **Buyback reserve insufficient** | 🟢 Low | TrueTech publishes formula transparently on truesight.me. Members know buybacks are discretionary and tied to business performance. |
| **Howey risk (TDG as security)** | 🟡 Medium | Narrow legal question for SVH-referred counsel. TDG is a governance right, not a security or profit-sharing instrument. |

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
9. For DUNA: verify eligibility (100+ members by mutual consent) and engage legal counsel to elect formation under the DUNA Act

---

*Prepared by Sophia Truesight (admin+sophia@truesight.me)*
*TrueSight DAO Autopilot*