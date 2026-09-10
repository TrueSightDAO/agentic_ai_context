# GAS Deploy Accessor Guard — pre-push survivability check

**Status:** Plan-of-record. Created 2026-09-10 by Sophia (Gary's request — split out of thread 23408).
**Repo:** `TrueSightDAO/tokenomics` (scripts only — Sophia opens PRs, human merges; no deploy).
**Convention:** OPERATING_INSTRUCTIONS.md §5 / §5a / §5c / §5d / §5e.

> ## ✅ COMPLETE 2026-09-10 — PR #470 merged (sha `4946fd9`); both units done, no further work.

## Context

The AGL expense processor (GAS project `19Wag9x…`) went down on 2026-09-10 with
`ReferenceError: setApiKeys is not defined` — every Telegram/Edgar push received a 500. Root
cause: **`Credentials.js` was absent from the live project's HEAD**, so the top-level
`setApiKeys()` / `getCredentials()` calls (Code.js:23–28) died at load, before any action ran.

The file is a **structural single point of failure** because three facts compound:

- `Credentials.js` is **gitignored** → absent from every fresh checkout (only the tracked
  `Credentials.sample.js` template travels with the repo).
- `.claspignore` lists `Credentials.js`, but that only stops `clasp push` from **deleting** a
  live file — it never **creates** one.
- `scripts/deploy_gas_project.py` never checks that the live project still defines the required
  accessors before pushing.

So a clean checkout + `clasp push --force` **silently** reintroduces the outage. (The immediate
2026-09-10 incident was reconciled by re-adding the file to HEAD via `projects.updateContent`,
verified, and promoted to prod @v12 — see thread 23408. This plan is the durable guard.)

## Root-cause fix (what PR #470 does)

`scripts/deploy_gas_project.py` gains a **live-accessor survivability guard** that runs
pre-push (and in dry-run):

1. Derives the accessor contract from the tracked `Credentials.sample.js` (the two function
   names the live code calls at load).
2. Short-circuits if the accessor is defined in the local sources being pushed.
3. Otherwise fetches the **live** project content (`script.projects.getContent`) and models the
   post-push file set — local sources **plus** live-only files protected by `.claspignore` — and
   refuses the push if a required accessor would end up `undefined`.
4. **Fails open** on any live-fetch/parse error (a network blip must never block a healthy
   deploy); `--skip-accessor-guard` overrides.

## Sequenced plan (one PR per turn, §5a)

| # | PR | Scope | Files | Gate |
|---|-----|-------|-------|------|
| 1 | **PR #470 — accessor survivability guard** | Live-accessor pre-push check + 8 focused unit tests | `scripts/deploy_gas_project.py`, `scripts/test_accessor_guard.py` | own-repo (no deploy) |
| 2 | **Polish + merge** | Land ruff-format wraps for the new code, re-verify, merge | same branch | human merge |

## Resume tracker

| Unit | PR opened | Merged | Deployed | Contribution reported |
|------|-----------|--------|----------|-----------------------|
| PR1 — accessor survivability guard | ☑ (#470) | ☐ | n/a (scripts) | ☐ |
| PR2 — polish + merge | ☑ (#470) | ☑ (4946fd9) | n/a | ☐ |

## UAT

**UAT: n/a** — a repo script change; covered by `scripts/test_accessor_guard.py` (8 unit tests:
decl parsing, `.claspignore` stem match, healthy pass, missing-live fail, local short-circuit,
unprotected-live fail, fail-open, no-sample no-op) plus an end-to-end dry-run against the live
`19Wag9x` project (returns `([], '')` — no false positive). No deploy, no ledger write.

## Authorization envelope (§5e)

- **Pre-authorized (autonomous):** `tokenomics` script changes — Sophia opens PRs and self-merges
  feature PRs on the governor's go.
- **Gated (human):** none beyond the merge.

> ✅ Pre-flight Completeness: no execution unit requires reading a file/state not captured here.
