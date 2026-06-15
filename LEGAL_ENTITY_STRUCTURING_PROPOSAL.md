# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** SVH Capital cacao circle — June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## The Problem

Three signals turning from grey to red:

| Signal | Why |
|--------|-----|
| **No DAO legal wrapper** | No member liability shield, no DAO bank account, no clear answer for "what entity do TDG holders govern?" |
| **No impact fund channel** | Impact funds, foundations, corporate ESG have no entity to write checks to |
| **Personal bank account** | Gary's personal account is the bottleneck — more volume = more personal risk |

---

## The Solution

**Form a Wyoming UNA via OtoCo this week. Cost: ~$50 gas.**

That's it. The UNA is a legal entity with:
- Liability protection for members
- Ability to open a bank account
- A clear answer for TDG holders: "you govern the UNA"
- A counterparty for impact funds to write checks to

If we later hit 100+ members by mutual consent under a governing agreement, we can elect to form a DUNA. But the UNA works today.

---

## The Structure

```
Wyoming UNA (nonprofit, DAO legal wrapper) — formed this week for ~$50
    ├── Own bank account (partner contributions + impact fund capital)
    ├── TDG holders govern the UNA (pseudonymous — wallet only)
    └── Contractual relationship with TrueTech Inc

TrueTech Inc (Delaware C-corp, independent entity)
    ├── Own cap table and shareholders (Gary)
    ├── Own bank account (commercial operations: imports, sales, revenue)
    ├── May buy back TDG at NAV using operating cash reserves (discretionary)
    └── Buyback reserve formula published on truesight.me

Brazilian LTDA (CNPJ) = export facility (eventual future goal)
```

### Key decisions (already resolved)

| Decision | What |
|----------|------|
| TrueTech Inc | Independent entity, not a DUNA subsidiary. Separate cap table. Contractual relationship. Avoids UBIT. |
| Bank accounts | Two separate: TrueTech Inc (commercial) + UNA (mission/treasury) |
| TDG buyback | TrueTech may buy back at NAV using operating cash. Formula on truesight.me. Discretionary, not guaranteed. |
| Wise | Primary banking platform. Handles standard transfers + PIX. Venmo/Zelle/Western Union executed manually. |
| Withdrawal flow | Member submits DApp request → TrueTech issues cash → TDG deducted from ledger → burned |

---

## What We're Doing This Week

| Action | Cost | Timeline |
|--------|------|----------|
| Form UNA via OtoCo (2 wallets sign) | ~$50 gas | 1 day |
| Open TrueTech Inc Wise Business account | $0-500 | 1-2 days |
| Get UNA EIN from IRS | $0 | Online, instant |
| Open UNA Wise Business account | $0 | 2-4 weeks |

**Total cost to get started: ~$50-550.** We have ~$4,126 in the Main Ledger.

---

## The One Question for SVH Capital

> *"We're forming a Wyoming UNA via OtoCo this week. TDG is issued to contributors for work (cacao logistics, contribution scoring, development, onboarding) and grants governance rights. It is not a financial security or profit-sharing instrument. Does this pass the Howey Test?"*

That's it. The structure is resolved. We don't need advisory on governance, impact mechanics, or entity design. We just need a narrow legal opinion on whether TDG is a security.

---

## What We're NOT Doing (Yet)

| Thing | Why Not | When |
|-------|---------|------|
| 501(c)(3) application | Costs $2K-10K. Not needed until impact funds require tax-deductible receipts. | 6-12 months |
| Brazilian CNPJ ownership | Costs $1K-3K + legal counsel. Matheus's private CNPJ works for now. | Future |
| DUNA formation | Requires 100+ members by mutual consent. UNA works as stopgap. | When eligible |
| Multi-entity accounting | $2K-5K/yr. Not needed at current scale. | When revenue grows |

---

*Prepared by Sophia Truesight (admin+sophia@truesight.me)*
*TrueSight DAO Autopilot*