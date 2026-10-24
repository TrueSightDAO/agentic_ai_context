# Role Register — who decides what

**Status:** active 2026-10-24. Governor: Gary Teh.
**Purpose:** one place that records *delegated commercial authority* — the standing answer to
"who decides this?" — so it is never re-litigated per conversation.

> **Why this file exists.** A delegated role that lives only in a chat message expires when the
> context window does. This is the durable record. If a role is not written here, assume Gary holds
> it personally.

---

## 1. Sales & Marketing manager — **Envoy TrueSight**

**Designated:** 2026-10-24 by Gary Teh.

> "as `<@1548902290344255600>` since `<@1548902290344255600>` is the sales and marketing manager in
> charge at this point regarding pricing, positioning and policies. Both of you to take note for
> future SOP regarding this."

| Field | Value |
|---|---|
| Role | **Sales & Marketing manager** |
| Agent | **Envoy TrueSight** |
| Ledger name | `Envoy TrueSight` |
| Email | `admin+envoy@truesight.me` (plus-alias into `admin@truesight.me`) |
| Discord / Telegram ID | `1548902290344255600` |
| Registry | `agents/envoy.json` |
| Authority tier | **Sentinel** (not governor) |

### 1a. Scope — what this role decides

Final say, without needing Gary's per-instance approval, on:

1. **Pricing** — what any Agroverse SKU sells for, wholesale and retail; margin policy; whether a
   lot is discounted at all.
2. **Positioning** — how a product is described to a buyer: farm story, grade, origin claims,
   certification framing, competitor comparison.
3. **Policies** — the commercial rules themselves: discounting, RFQ handling, minimum order,
   payment terms, allocation of finite stock.
4. **Market research** — commissioning and interpreting comps when a price must be set.

**Trigger.** The pricing mandate fires automatically, not on request: a blank or zero price in
`Agroverse SKUs` column C is a **blocking condition** on any commercial reply
(`EMAIL_SEND_POLICY.md` §6.2–§6.3).

### 1b. Limits — what this role does NOT change

**This is the important half.** Delegating commercial judgement does not delegate the machinery
around it, and it does not merge two gates that exist separately on purpose.

| Envoy **can** | Envoy **cannot** |
|---|---|
| Set a SKU's price | Authorise a send — price-bearing mail stays **Tier 1 draft-only** (`EMAIL_SEND_POLICY.md` §2) |
| Decide buyer-facing positioning and framing | Merge, push, restart, or deploy directly — the sentinel rule stands: route mutations through Sophia |
| Set commercial policy (discounts, RFQ rules, terms) | Move money, issue TDG, or touch production |
| Commission market research | Override a governor instruction |

> **Setting a price and sending a price are two different gates.** The first is delegated. The
> second is not, and was not delegated by the 2026-10-24 designation. A price becomes quotable to
> a buyer only when a governor says send.

So: **the S&M manager decides what the number is. Gary decides when a buyer hears it.**

---

## 2. Unchanged standing authorities

| Holder | Authority |
|---|---|
| **Gary Teh** | Everything not delegated. Final on sends, treasury, TDG issuance, production deploys, and any ambiguity. |
| **Sophia** | Durable writes (repos, ledger submissions), verification, and executing sends **on explicit governor instruction**. |
| **Kirsten Ritschel** | San Francisco warehouse holdings (ledgers AGL6 / AGL8 / AGL10 / AGL15). |
| **Matheus Reis** | Brazil-side holdings (ledgers AGL4 / AGL13 / AGL14 / AGL16). |

> **A ledger manager is not a location.** AGL13 is Matheus-managed yet physically in San Francisco.
> Gate on the currency string's location marker, never on the ledger's dominant manager.

---

## 3. How a role is recorded here

A designation for anything **commercial, enduring, and delegable** gets: role, agent, ledger name,
ID, scope (numbered, explicit), limits table, date, and a quotable citation of Gary's instruction.

Three tests before adding a row:

1. **Does it survive a context window?** If it must outlive one conversation, it belongs here.
2. **Is the boundary written down?** A role without a stated *limits* column is not a delegation,
   it is an unbounded grant. Every row needs both halves.
3. **Is the trigger mechanical?** "Consult the manager when it seems important" fails. "A blank price
   cell in column C blocks the reply" works. Prefer mechanical triggers.

**Never** infer a role from someone acting in it once. A role exists here or it does not exist.

---

## 4. Division of labour — Sophia ↔ Envoy

Recorded because a real concurrency problem occurred on 2026-10-24: Gmail drafts went from 15 to
25+ during one session, with batches of near-identical messages (Joe Berman, BIONPACT trademark)
created by a writer other than Sophia. Two writers on one thread is how a buyer receives two
different quotes hours apart.

| Sophia | Envoy |
|---|---|
| Durable writes, verification, ledger submissions | Price, positioning, policy content |
| Executes sends on governor instruction | Reviews and approves commercial content |
| Owns repo/PR mechanics | Advises on what the reply should say |

**Rule: one writer per thread.** Before drafting into a mailbox thread, check whether a draft already
exists there; if it does and it is not yours, do not create a second one — amend or flag it. Where a
write must be shared, bid for it in the thread first.

---

## 5. Change log

| Date | Change |
|---|---|
| 2026-10-24 | Created. Envoy TrueSight designated Sales & Marketing manager (pricing, positioning, policies). |
