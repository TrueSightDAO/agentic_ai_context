# DAO Client JS integration — consolidated fix list (oracle + capoeira)

**Status:** HANDED OFF to Sophia 2026-06-08 · **Owner:** Sophia (autopilot) · **Sponsor:** Gary
**Coordination topic:** `tg:-1003919341801:3` (this is the single tracker for all
`@truesight_dao/dao-client` integration fixes). Detailed sub-threads: package +
oracle = **1638**, capoeira = **1658**.

---

## ⚠️ PREFLIGHT — every handoff

Refresh your repo view FIRST — read this via `read_repo_file` (GitHub `main`) or
`git fetch origin main && git reset --hard origin/main` your context clone. Don't
trust a stale local copy. (`SOPHIA_HANDOFFS.md` § "Before you start".)

## The single root cause (fix this and everything else unblocks)

`@truesight_dao/dao-client@1.0.0` is **broken for browser use**. It's built with
esbuild `--global-name=DaoClient` on `export class DaoClient`, so the IIFE global
`window.DaoClient` is the **module namespace** (`{DaoClient: <class>, …}`) — the
class is at `DaoClient.DaoClient` and the helpers at
`DaoClient.DaoClient.base64ToArrayBuffer`. So `DaoClient.base64ToArrayBuffer(...)`
throws `is not a function`. This broke **oracle prod twice** (oracle #38/#39, then
#42 → reverted #43). Both consumers are currently on safe **inline** code.

---

## Issue 1 — 🔴 BLOCKER · Package: republish `@1.0.1` (correct global + runtime test)

**Repo:** `dao_protocol` · **Topic:** 1638

- [ ] Fix the browser build so `window.DaoClient` **is the class** —
      `typeof window.DaoClient.base64ToArrayBuffer === 'function'`.
- [ ] Add a **runtime smoke test** that loads the actual built/published bundle
      and asserts the global shape (each used helper is a function) + one base64
      round-trip + one `sign`. **`node --check` cannot catch this** (it's valid
      syntax, wrong runtime shape) — that's exactly why the oracle broke.
- [ ] Bump to **`1.0.1`**, republish via the CI workflow
      (`npm-publish-dao-client.yml` + `NPM_TOKEN` secret).
- [ ] Verify `https://unpkg.com/@truesight_dao/dao-client@1.0.1/dist/dao-client.min.js`
      returns 200 **and** the global shape is correct.

**Unblocks Issues 2 and 3.**

## Issue 2 — Oracle re-integration (currently reverted to working inline)

**Repo:** `oracle` · **Plan:** `ORACLE_CDN_REWIRE_PLAN.md` · **Topic:** 1638

- State: `oracle.truesight.me` is on the known-good inline build (#43). Re-do the
  CDN adoption **against `@1.0.1`**.
- [ ] Add the verified `@1.0.1` CDN tag — **fix load order** (no blind `defer`;
      `DaoClient` must be defined before any inline code that uses it; the on-load
      `initDaoIdentityState` + the draw-submit are the risk points).
- [ ] Swap the base64 helpers (+ any exact-match helpers) to `DaoClient.*`;
      **map each before deleting**.
- [ ] **Preserve:** canonical-signing fix (sign only up to `--------`), 3-state
      identity UX (pending/verified/unlinked), SW kill-switch.

## Issue 3 — Capoeira swap (inline + working; parked)

**Repo:** `capoeira` · **Plan:** `CAPOEIRA_DAO_CLIENT_SWAP_PLAN.md` · **Topic:** 1658

- [ ] Swap `assets/js/practice-event-submit.js` generic helpers
      (`base64*`, `generateKeypair`, `publicKeyToSlug`, `signRequestText`) to
      `DaoClient.*` against `@1.0.1`; **map each before deleting**.
- [ ] **Keep inline (capoeira-specific):** `buildPracticeEventText`,
      `submitSession`, `backfillUnsent`, `getCvUrl`, storage glue.

---

## Shared Definition of Done — applies to EVERY consumer swap (the lessons)

1. **Depend on `@1.0.1`+**, pin the exact version, and **verify the unpkg URL
   returns 200 in the same PR**.
2. **Runtime smoke test, not just `node --check`.** Load the ACTUAL bundle, assert
   the global shape + exercise one `sign`. Syntax-checking can't catch an
   API-shape mismatch.
3. **Correct script load order** — the CDN global must exist before any consuming
   code runs (no blind `defer`).
4. **Map each inline helper to the real `DaoClient` API before deleting it.**
5. **Preserve** consumer-specific logic and all prior fixes.
6. **Open the PR, do NOT auto-merge.** Both sites deploy from `main`; this
   integration has broken oracle prod twice. Report in the topic so it can be
   spun up and eyeballed (a real submission flow) before merge.
7. Every commit + PR carries **`Generated-by: Sophia (TrueSight Autopilot)`**.

## Sequence / resume tracker

> **RESUME HERE →** Issue 1 (package `@1.0.1`). Issues 2 & 3 are PARKED until it
> lands, then can proceed in parallel — each its own PR, each reviewed before merge.

| # | Unit | Repo | Topic | Blocked on | Status |
|---|------|------|-------|-----------|--------|
| 1 | Package `@1.0.1` (global + runtime test) | dao_protocol | 1638 | — | ☐ in progress |
| 2 | Oracle CDN re-integration | oracle | 1638 | Issue 1 | ⏸ parked |
| 3 | Capoeira swap | capoeira | 1658 | Issue 1 | ⏸ parked |

## Acceptance (all three)

- `@1.0.1` published; `typeof window.DaoClient.base64ToArrayBuffer === 'function'`;
  unpkg 200.
- Oracle: cast → identity link (pending→verified) → reading submit → credential
  link, **zero console errors**.
- Capoeira: practice session → keygen → sign → submit → credential link,
  **zero console errors**; `backfillUnsent` still works.
- Each shipped via a reviewed PR (not auto-merged).
