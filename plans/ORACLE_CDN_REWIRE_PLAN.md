# Oracle CDN re-wire — adopt `@truesight_dao/dao-client`

**Status:** HANDED OFF to Sophia 2026-06-08 · **Owner:** Sophia (autopilot) · **Sponsor:** Gary
Registered in `SOPHIA_HANDOFFS.md`.

---

## ⚠️ PREFLIGHT — do this FIRST (every handoff)

1. **Refresh your view of the repo — your context clone can be STALE.** Before
   reading or acting on this plan:
   - read it via **`read_repo_file`** (GitHub `main`, always current), **or**
   - `ssh_run(host='autopilot', "cd /opt/truesight_autopilot/context/agentic_ai_context && git fetch origin main && git reset --hard origin/main")` then read.
   *(Last handoff you acted on a stale clone and got confused — don't trust a
   local copy without pulling.)*
2. `git pull` the **oracle** repo's default branch before you branch.

---

## Context

- **`@truesight_dao/dao-client@1.0.0` is PUBLISHED and CDN-live** (npm `latest=1.0.0`;
  unpkg + jsDelivr both return **HTTP 200**). Browser global: **`DaoClient`**
  (esbuild `--global-name=DaoClient`).
- The oracle (`TrueSightDAO/oracle`, deploys `oracle.truesight.me` from `main`)
  is currently **INLINE** — the 2026-06-08 hotfix (oracle #40) reverted the
  broken #38/#39 CDN refactor that referenced the then-**unpublished**
  `@truesight/dao-client` (unpkg 404 → broke prod) and reverted #36's syntax
  errors.
- **Goal:** safely re-introduce the shared package so the oracle loads it from
  the CDN instead of duplicating inline code.

## Hard guards (from the outage postmortem — non-negotiable)

- **Verify the exact CDN URL returns HTTP 200 in the SAME PR** before merging:
  `https://unpkg.com/@truesight_dao/dao-client@1.0.0/dist/dao-client.min.js`
  (and the jsDelivr equivalent). Never reference an unverified/unpublished URL.
- **Pin the exact version** (`@1.0.0`) — never a floating tag.
- **Run a JS syntax check before merge:** `node --check` on every changed
  `*.js`, AND extract each inline `<script>` from `index.html` and `node --check`
  it. The outage was a `SyntaxError` (apostrophe in a single-quoted string +
  `\n` saved as a literal newline) that killed ALL page JS. This guard would
  have caught it.
- **Map before you delete:** confirm the `DaoClient` global exposes an exact
  equivalent for each inline helper you remove (signing, key-gen, canonical
  payload, `check_digital_signature`). Keep the 2026-06-08 fixes intact:
  canonical-signing (sign only up to `--------`), 3-state identity UX
  (pending / verified / unlinked), and the SW kill-switch.

## Sequenced PRs

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This plan (baton) | agentic_ai_context |
| **PR1** | Add the verified `<script src=…@1.0.0…dao-client.min.js>` tag; replace inline DAO-client helpers with `DaoClient.*` **only where the package matches exactly**; preserve the 3-state UX + canonical signing + SW kill-switch. | oracle |
| **PR2** *(optional)* | Same adoption in dapp `create_signature.html` — **beta-first** (`dapp_beta` → promote `dapp_prod`). | dapp_beta |

## Resume tracker

> **RESUME HERE →** PR1 (oracle). After each unit merges, report the DAO
> contribution before the next.

| Unit | Repo | Merged | Contribution |
|---|---|---|---|
| PR0 plan | agentic_ai_context | ☐ | — |
| PR1 oracle CDN adoption | oracle | ☐ | ☐ |
| PR2 dapp parity (optional) | dapp_beta → dapp_prod | ☐ | ☐ |

## Publishing future package versions (no raw token needed)

You publish **via CI**, not a token on your box:
- Workflow: `dao_protocol/.github/workflows/npm-publish-dao-client.yml`.
- Trigger: `gh workflow run npm-publish-dao-client.yml --repo TrueSightDAO/dao_protocol`
  **or** push a `dao-client-v*` tag. It runs `npm publish --access public` using
  the **`NPM_TOKEN`** GitHub Actions secret (already set on dao_protocol).
- **Bump** `packages/dao-client/package.json` `version` first — npm rejects
  re-publishing an existing version. Then update the oracle CDN URL's pinned
  version to match.
- The `NPM_TOKEN` secret is account `sophia_truesight` (owner of the
  `truesight_dao` org). **It expires ~2026-09-06** — see the rotation entry in
  `OPEN_FOLLOWUPS.md`.

## Acceptance

- `oracle.truesight.me` loads with **zero console errors**; the identity flow
  (register → pending → verify → verified) and the draw-submit both work
  end-to-end; the CDN tag resolves 200; `node --check` is clean on all changed
  files.
