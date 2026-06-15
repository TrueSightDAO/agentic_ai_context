# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** SVH Capital cacao circle — June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## The Problem

Three signals turning from grey to red:

| Signal | Why |
|--------|-----|
| **No DAO legal wrapper** | No member liability shield, no clear answer for "what entity do TDG holders govern?" |
| **No impact fund channel** | Impact funds, foundations, corporate ESG have no entity to write checks to |
| **Personal bank account** | Gary's personal account is the bottleneck — more volume = more personal risk |

---

## The Solution

**Form a Wyoming UNA via OtoCo this week. Cost: ~$50 gas.**

That's it. The UNA is a legal entity with:
- Liability protection for members
- A clear answer for TDG holders: "you govern the UNA"
- A counterparty for impact funds to write checks to
- **No bank account needed** — TrueTech Inc handles all money flows

If we later hit 100+ members by mutual consent under a governing agreement, we can elect to form a DUNA. But the UNA works today.

---

## The Structure

```
Wyoming UNA (nonprofit, DAO legal wrapper) — formed this week for ~$50
    ├── No bank account needed — TrueTech Inc handles all money flows
    ├── TDG holders govern the UNA (pseudonymous — wallet only)
    └── Contractual relationship with TrueTech Inc

TrueTech Inc (Delaware C-corp, independent entity)
    ├── Own cap table and shareholders (Gary)
    ├── Own bank account (ALL money flows: commercial, partner contributions, buybacks)
    ├── May buy back TDG at NAV using operating cash reserves (discretionary)
    └── Buyback reserve formula published on truesight.me

Brazilian LTDA (CNPJ) = export facility (eventual future goal)
```

### Key decisions (already resolved)

| Decision | What |
|----------|------|
| TrueTech Inc | Independent entity, not a DUNA subsidiary. Separate cap table. Contractual relationship. Avoids UBIT. |
| Bank accounts | **One account** — TrueTech Inc handles everything. UNA doesn't need its own. |
| TDG buyback | TrueTech may buy back at NAV using operating cash. Formula on truesight.me. Discretionary, not guaranteed. |
| Wise | Primary banking platform. $0 to open, no minimum deposit. Handles standard transfers + PIX. Venmo/Zelle/Western Union executed manually. |
| Withdrawal flow | Member submits DApp request → TrueTech issues cash → TDG deducted from ledger → burned |

---

## What We're Doing This Week

| Action | Cost | Timeline |
|--------|------|----------|
| Form UNA via OtoCo (2 wallets sign) | ~$50 gas | 1 day |
| Open TrueTech Inc Wise Business account | **$0** (no fees, no minimum deposit) | 1-2 days |

**Total cost: ~$50.** We have ~$4,126 in the Main Ledger.

---

## The One Question for SVH Capital

> *"We're forming a Wyoming UNA via OtoCo this week. TDG is issued to contributors for work (cacao logistics, contribution scoring, development, onboarding) and grants governance rights. It is not a financial security or profit-sharing instrument. Does this pass the Howey Test?"*

That's it. The structure is resolved. We don't need advisory on governance, impact mechanics, or entity design. We just need a narrow legal opinion on whether TDG is a security.

---

## What We're NOT Doing (Yet)

| Thing | Why Not | When |
|-------|---------|------|
| UNA bank account | TrueTech Inc handles all money flows. No need. | Only if impact fund capital requires separate home |
| 501(c)(3) application | Costs $2K-10K. Not needed until impact funds require tax-deductible receipts. | 6-12 months |
| Brazilian CNPJ ownership | Costs $1K-3K + legal counsel. Matheus's private CNPJ works for now. | Future |
| DUNA formation | Requires 100+ members by mutual consent. UNA works as stopgap. | When eligible |
| Multi-entity accounting | $2K-5K/yr. Not needed at current scale. | When revenue grows |

---

*Prepared by Sophia Truesight (admin+sophia@truesight.me)*
*TrueSight DAO Autopilot*