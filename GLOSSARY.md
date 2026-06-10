# Glossary — shared terms for LLMs, Sophia & operators

Define a term here the first time it causes confusion, so future agents resolve it
via `search_context` instead of guessing. Keep entries short and factual.

---

## UAT — User Acceptance Testing

The phase where a **human (the operator/governor) validates an end-to-end
experience behaves correctly before it goes live** — the final "does this actually
do what we want, from a real user's point of view" check, distinct from automated
unit/integration tests (which machines run).

**In this workspace, UAT runs on the BETA staging stack, never prod, and never
with real money:**

- Front-end: the **`beta.*`** sites (`beta.agroverse.shop`, `beta.dapp.truesight.me`).
- Back-end: the **beta sandbox** — `beta.edgar.truesight.me` (beta `dao_protocol`)
  in **Stripe TEST mode** (`sk_test_…`), writing **SANDBOX**-labelled rows, isolated
  from prod (see `BETA_SANDBOX_ENDPOINT_PLAN.md`).
- Payments during UAT use **Stripe test cards** (e.g. `4242 4242 4242 4242`) — the
  hosted checkout must show **"TEST MODE"**. If it doesn't, STOP: a real card could
  be charged.

**The point of the beta sandbox is that UAT needs no local setup** — prefer the
beta staging environment over spinning up local instances.

**Current/active UATs:** the Agroverse chocolate-bar **subscription** UAT is run in
**Telegram thread 1955** (Sophia corresponds there); plan: `CHOCOLATE_SUBSCRIPTION_PLAN.md`.

> When an operator says "do the UAT" / "UAT this," they mean: walk the real
> end-to-end flow on beta (test mode), confirm it meets the acceptance criteria,
> and report pass/fail — they are NOT asking for more unit tests.
