# Glossary — shared terms for LLMs, Sophia & operators

Define a term here the first time it causes confusion, so future agents resolve it
via `search_context` instead of guessing. Keep entries short and factual.

---

## UAT — User Acceptance Testing

The phase where a **human (the operator/governor) validates an end-to-end
experience behaves correctly before it goes live** — the final "does this actually
do what we want, from a real user's point of view" check, distinct from automated
unit/integration tests (which machines run).

**Two stages — machine self-UAT ALWAYS precedes human UAT (Gary 2026-09-09):**

1. **Machine self-UAT (mandatory, all Sophia instances / agents).** Before asking a
   human to test, the implementing agent runs its own end-to-end verification of the
   same acceptance criteria against the live **beta** staging surface (or a locally
   served equivalent, stated explicitly) — headless browser / Playwright / scripted
   walk of the real flow — and reports pass/fail evidence per criterion in the
   handoff. This is the agent proving the change works before a human spends time on it.
2. **Human UAT (the always-stop gate).** The governor/operator walks the real flow on
   beta (test mode) and gives the final sign-off before go-live.

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
>
> When an agent asks a human to UAT, it MUST already have run its own **self-UAT**
> (stage 1 above) and reported the evidence — the human UAT is a second, independent
> confirmation, never the first exercise of the change.
