# Internal Capital Strategy Memo — TrueSight DAO

**Not for SVH Capital meeting. Internal reference only.**

---

## Purpose

This memo captures the capital-formation strategy thinking that was removed from the SVH-facing proposal to avoid creating securities-law exposure in the meeting document. The SVH doc asks a narrow Howey question. This memo explores the broader economic model.

---

## Revenue Distribution Model

### The Principle

The DAO is the proving ground — it surfaces bugs, edge cases, and feature gaps through real operations. The technology gets battle-tested here, then the polished product gets licensed out.

### The Flow

```
Licensing revenue → TrueTech Inc (collects)
    → TrueTech Inc margin (operational costs, support, hosting)
    → Surplus → TDG buyback from DApp → burned
    → All TDG holders benefit via NAV growth
```

### Who Governs the Terms

| What | Who Decides |
|------|-------------|
| Minimum license fee | DAO governance (TDG vote) |
| TrueTech Inc margin cap | DAO governance (TDG vote) |
| Buyback allocation % | DAO governance (TDG vote) |
| Licensee approval | DAO governance (TDG vote) |

### Why This Works

- **TrueTech Inc** handles the commercial side (contracts, invoices, support, liability) — it's a for-profit C-corp, so it can do this cleanly
- **The UNA** never touches the money directly — avoids UBIT and 501(c)(3) jeopardy
- **TDG holders** benefit through NAV growth (buyback → burned → deflationary pressure) — not through direct revenue distribution
- **DAO governance** controls the economics without touching the money — sets the terms, TrueTech Inc executes

---

## The Data Flywheel Moat

```
Ecosystem → raw operational data → DAO operations
    → Sophia + Edgar learn and improve
    → Better automation, better protocols
    → Licensed back to new orgs
    → More data from licensees (anonymized) → flywheel accelerates
```

The code can be cloned. The network of verified farmers, provenance data, and governance trust cannot. And that network lives in the **UNA** — governed by TDG holders — not in TrueTech Inc.

---

## Design Constraint: Ecosystem Stability

Any new capital channel must not destabilize the TDG buyback mechanism. TrueTech Inc's buyback capacity is finite — it comes from operating cash flow.

**Guardrails:**
1. **Lockups for capital-injected TDG** — if TDG is ever issued for capital (not currently planned), vesting schedules apply. Contributors who earned TDG through labor have priority exit.
2. **Published reserve cap** — formula on truesight.me explicitly states maximum redemption capacity. If TDG issuance exceeds it, new issuances pause.
3. **NAV self-limits capital channels** — at current NAV ($0.0018/TDG), no rational fund would buy TDG above NAV. The channel is naturally self-limiting.

---

## Productization Signals

### Bilal (Butterfly Effect Club)
- Wants to use Sophia for his investment fund
- Team of 5
- Self-hosted instance — their data stays with them

### Liz
- Wants Sophia for deal flow management
- Wants Edgar's protocol for her own trading operations
- Self-hosted instance — their data stays with them

### What This Means

Two concrete leads for a licensing model. If either converts to a paying customer, TrueTech Inc gains:
- Recurring licensing revenue
- IP assets (the autopilot software)
- A reference customer for future licensees

This would make TrueTech Inc VC-investable — it would have an asset base beyond pass-through cacao trading.

---

*Prepared by Sophia Truesight (admin+sophia@truesight.me)*
*TrueSight DAO Autopilot*