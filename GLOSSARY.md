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

---

## Thread vs. Channel — the unit of "one piece of open work" per platform

A single piece of handed-off work (a plan, a bug, a one-off request) is tracked as a
different container depending on which platform it lives in:

- **Telegram:** the unit is a **thread** — a forum **topic** inside the single
  TrueSight DAO Ops supergroup (`chat_id -1003919341801`), identified by its
  `message_thread_id` (e.g. thread `27138`). Telegram threads are how the vast
  majority of Sophia handoffs are parked/executed (see `sophia/SOPHIA_HANDOFFS.md`).
- **Discord:** the unit is a **channel** — a distinct channel in the TrueSight DAO
  guild (e.g. `#discord-parity`, `#adapter-bugs`), not a Discord *thread* object.
  As of 2026-09-14 the guild has no active Discord threads (`GET
  /guilds/{id}/threads/active` returns empty) — Sophia's Discord adapter opens a new
  **channel** per work item instead (see `plans/DISCORD_ADAPTER_PLAN.md`).

**Why this matters for a supervisor (`sophia/SUPERVISOR_LOOP.md`) or anyone auditing
open work:** "check the threads" only covers Telegram. A full sweep of open/unfinished
work must separately enumerate Discord **channels** (`GET /guilds/{guild_id}/channels`)
— there is no single API call that returns "all open units" across both platforms.

---

## Provenance page — the per-asset "where did this come from" page

When a governor or agent says **"provenance page"** (or "QR provenance page"), they
mean the **public, per-asset page rendered from a QR code's lineage manifest**:

- **URL:** `https://truesight.me/qr/?id=<qr_id>` — e.g.
  `https://truesight.me/qr/?id=2024SA_20251227_35`.
- **Reads `?id=<qr_id>`** from the query string (`#<qr_id>` fragment is an accepted
  fallback). ⚠️ **`?q=` is NOT a valid parameter** — the page ignores it and renders
  "No QR id supplied". Always use `?id=`.
- **Source:** per-asset manifest JSON at
  `https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/qrs/<qr_id>.json`
  (see `LINEAGE_ASSETS.md`), plus a certificate-PDF probe.
- **Template:** `truesight_me_beta/qr/index.html` — static HTML + vanilla JS, dispatched
  on `asset_type`; also live on prod. Page title: **"QR Provenance | TrueSight DAO"**.
- **Edgar-resolve is NOT the provenance page.** `edgar.truesight.me/agroverse/qr-code-check?qr_code=<id>`
  is the URL *printed inside the physical QR*; Edgar 302-redirects it (currently to
  agroverse.shop product pages, via column B of the **Agroverse QR codes** sheet).

**SunMint certificate download.** When a SunMint certificate exists for a tree / QR, it
is published at `lineage-assets/certs/<qr_id>__cert.pdf`; the provenance page HEAD-probes
that URL and shows a **"⬇️ Download SunMint certificate (PDF)"** button **only when the
probe returns 200** (the URL-probe route — see `sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md`
and `OPEN_FOLLOWUPS.md`).
