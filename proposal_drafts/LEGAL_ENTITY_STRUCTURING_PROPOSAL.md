# Legal Entity Structuring Proposal — TrueSight DAO

**Prepared:** 2026-06-22
**Context:** SVH Capital cacao circle — June 26
**Author:** Sophia (TrueSight DAO Autopilot)

---

## The Problem

Two signals turning from grey to red:

| Signal | Why |
|--------|-----|
| **No DAO legal wrapper** | No member liability shield, no clear answer for "what entity do TDG holders govern?" |
| **Personal bank account** | Gary's personal account is the bottleneck — more volume = more personal risk |

---

## The Solution

**Form a Wyoming UNA via OtoCo this week. Cost: ~$50 gas.**

That's it. The UNA is a legal entity with:
- Liability protection for members
- A clear answer for TDG holders: "you govern the UNA"
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

**Suggestion for consideration:** If technology licensing revenue materializes (e.g. Bilal from Butterfly Effect Club wants his own Sophia instance for his investment fund), part of those proceeds — after covering TrueTech Inc's operational costs — could flow into the buyback reserve, increasing NAV per TDG. This would align the technology's commercial success with contributor value without requiring the UNA to touch the money directly. This is not a commitment — just a design option to keep in mind as the licensing model develops.

---

## The One Question for SVH Capital

> "We're forming a Wyoming UNA via OtoCo this week. TDG is issued to contributors for work and grants governance rights. An independent affiliated C-corp (TrueTech Inc) may, at its discretion, buy back TDG at net asset value (total DAO assets ÷ total TDG issued) from its own operating cash. Does TDG constitute a security under Howey?"

---

## What We're NOT Doing (Yet)

| Thing | Why Not | When |
|-------|---------|------|
| Impact fund channel | No committed backend | When a donation-type funder appears |
| UNA bank account | TrueTech handles all flows | Only if impact fund capital requires it |
| 501(c)(3) application | $2K-10K | 6-12 months |
| Brazilian CNPJ ownership | $1K-3K + counsel | Future |
| DUNA formation | Need 100+ members by consent | When eligible |
| Multi-entity accounting | $2K-5K/yr | When revenue grows |
| VC investment | No retained asset base yet | If licensing revenue materializes |

---

*Prepared by Sophia Truesight (admin+sophia@truesight.me)*
*TrueSight DAO Autopilot*