# Capoeira → `@truesight_dao/dao-client` swap (PR2 execution plan)

**Status:** HANDED OFF to Sophia 2026-06-08 · **Owner:** Sophia (autopilot) · **Sponsor:** Gary
**Parent roadmap:** `TRUESIGHT_DAO_CLIENT_JS_ROADMAP.md` (this is its **PR2**, with the
post-outage corrections + gates). **Topic:** `tg:-1003919341801:1658`.

---

## ⚠️ PREFLIGHT — do this FIRST (every handoff)

1. **Refresh your repo view — your context clone can be STALE.** Read this plan
   via `read_repo_file` (GitHub `main`), or `git fetch origin main && git reset
   --hard origin/main` your context clone, before acting. (See
   `SOPHIA_HANDOFFS.md` § "Before you start".)
2. `git pull` the **capoeira** repo default branch before branching.

## 🔴 HARD BLOCKER — do NOT start until the package is fixed

The master roadmap is stale on three facts; the truth as of 2026-06-08:

- **Scope is `@truesight_dao/dao-client`** (NOT `@truesight/...` — that org never
  existed). Published; account `sophia_truesight`, org `truesight_dao`.
- **`1.0.0` is BROKEN for browser use.** It's built with esbuild
  `--global-name=DaoClient` on `export class DaoClient`, so `window.DaoClient`
  is the **module namespace** — the class is at `DaoClient.DaoClient` and the
  helpers at `DaoClient.DaoClient.base64ToArrayBuffer`. Calling
  `DaoClient.base64ToArrayBuffer(...)` throws `is not a function`. **This broke
  oracle prod (oracle #42, reverted in #43).**
- **The fix is `1.0.1`** — global-shape fix being done in topic **1638**
  (`window.DaoClient` must BE the class). **This capoeira swap depends on
  `@1.0.1`.** Do not begin PR2 until `1.0.1` is published and you've confirmed
  `typeof window.DaoClient.base64ToArrayBuffer === 'function'` against the live
  bundle.

## Context

- Capoeira (`TrueSightDAO/capoeira`, static GitHub Pages, **deploys from
  `main`**) reimplements the DAO signing/identity boilerplate inline in
  **`assets/js/practice-event-submit.js`**.
- Goal: replace the generic primitives with the shared package; keep
  capoeira-specific logic inline.

## Swap surface (grounded in the actual file)

**Replace with `DaoClient.*` (only where the package has an exact equivalent):**
`base64ToArrayBuffer`, `arrayBufferToBase64`, `base64ToBase64Url`,
`generateKeypair`, `publicKeyToSlug`, `signRequestText` (RSASSA-PKCS1-v1_5/SHA-256).

**KEEP inline (capoeira-specific — NOT in the package):** `buildPracticeEventText`
(session object → `[PRACTICE EVENT]` attributes), `submitSession`,
`backfillUnsent`, `getCvUrl`, `ensureKeypair`/`getStoredPublicKey` storage glue
(unless the package's storage API matches exactly).

**Map each helper to the real `DaoClient` API before deleting it** — verify the
method exists and has the same signature against the `@1.0.1` bundle.

## Hard guards (from the 2026-06-08 oracle outage — non-negotiable)

1. **Pin `@1.0.1`** and **verify the exact unpkg URL returns HTTP 200 in the same
   PR**: `https://unpkg.com/@truesight_dao/dao-client@1.0.1/dist/dao-client.min.js`
   (+ jsDelivr mirror).
2. **Runtime smoke test, not just `node --check`.** `node --check` only validates
   syntax — it CANNOT catch the global-shape / API mismatch that broke the oracle
   twice. Add a check that loads the **actual published bundle** and asserts
   `typeof DaoClient.<each used method> === 'function'`, plus one base64
   round-trip and one sign. Gate the merge on it.
3. **Script load order.** `practice-event-submit.js` may call into the helpers at
   load (e.g. `backfillUnsent`), so `DaoClient` must be defined first. Load the
   CDN `<script>` **without `defer`** (or placed before `practice-event-submit.js`)
   — do not assume `defer` ordering like the oracle did.
4. **Open the PR, do NOT auto-merge.** Capoeira deploys from `main`, and this
   integration has broken the oracle twice. Open the PR, run the smoke test,
   report in topic 1658 so we can spin it up and eyeball a real practice-session
   submission before merging.
5. Every commit + PR carries `Generated-by: Sophia (TrueSight Autopilot)`.

## Sequenced PRs

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This plan (baton) | agentic_ai_context |
| **PR2** | Add the verified `@1.0.1` CDN tag (correct load order); swap the generic helpers to `DaoClient.*`; keep capoeira-specific logic; smoke test. | capoeira |

## Resume tracker

> **RESUME HERE →** Wait for `@1.0.1` (topic 1638). Then PR2 in `capoeira`.

| Unit | Repo | Blocked on | Merged | Contribution |
|---|---|---|---|---|
| PR0 plan | agentic_ai_context | — | ☑ | — |
| PR2 capoeira swap | capoeira | `@truesight_dao/dao-client@1.0.1` | ☐ | ☐ |

## Acceptance

- A real practice session on capoeira: keygen → build `[PRACTICE EVENT]` → sign →
  submit to Edgar → credential link appears — all working in a browser, **zero
  console errors**; CDN tag resolves 200; smoke test green; `backfillUnsent`
  still works.
