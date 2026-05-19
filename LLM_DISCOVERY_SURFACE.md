# LLM discovery surface on truesight.me

This doc is the source-of-truth for the `llms.txt` + `stats/*.json` convention
on **truesight.me**. Future Claude / Codex / autopilot sessions: extend the
existing surface rather than inventing a parallel one. Operators: this is what
makes truesight.me readable to LLM agents that don't execute JavaScript.

## Why this exists

truesight.me's landing page hydrates its headline stats client-side via
`fetch()`. A plain HTTP GET (which is what ChatGPT, Claude with WebSearch,
Grok, Gemini, and most other agents do when given a URL) returns an empty
shell. Without a parallel machine-readable surface the DAO is essentially
invisible to LLM-driven research and discovery.

Shipped 2026-05-18 to fix that. Established by:
- `truesight_me_beta` PRs #119 (llms.txt + stats/current.json), #120 (Beer
  Hall recents), #122 (Beer Hall archive), #123 (repos index), #124 (programs +
  partners + deploy targets + treasury per-ledger), #125 (landing-page tile
  expanders).

## Live URLs

| URL | Refresh | What it carries |
|---|---|---|
| https://truesight.me/llms.txt | manual | Routing map: tells an LLM where to fetch what, with one-line hints per source and "how to answer Q → fetch URL" rules. **The first URL an agent should fetch.** |
| https://truesight.me/stats/current.json | 6h cron | Headline digest: north star, members count + governor list + voting power, treasury totals (per-currency + per-ledger), inventory counts, 10 most recent Beer Hall digests, pointers to every upstream source. **The single-fetch case** — answers most "what / how many / who" questions. |
| https://truesight.me/stats/beerhall_archive.json | 6h cron | Every Beer Hall digest ever published with date, slug, filename, raw_url. Sorted newest-first. For historical "what shipped in March / how did arc X start" queries. |
| https://truesight.me/stats/repos_index.json | 6h cron | Every public, non-archived, non-fork TrueSightDAO repo with description, primary language, topics, README URL, tree URL, and **deploy_target** (which production URL the repo deploys to). For "where is X implemented / what does Y do" queries. |
| https://truesight.me/stats/programs_index.json | 6h cron | Every credentialing program in `lineage-credentials/programs/` with lineage root, authorized attestors, practice / attestation type catalog, source-page URLs. For "what programs does the DAO credential / what's the lineage for X" queries. |
| https://truesight.me/stats/partners_index.json | 6h cron | Active Agroverse partner storage points with SKU count, total inventory units, top-3 products. For "who's carrying inventory / where can I buy product X" queries. |

## The cron + the builder

- **Workflow**: `truesight_me_beta/.github/workflows/stats-refresh.yml`
  Schedule: `37 */6 * * *` (offset from the `:27` advisory-snapshot-refresh
  in `go_to_market` to avoid burst overlap).
- **Builder**: `truesight_me_beta/scripts/build_stats_current.py`
  Pure standard library + `urllib`. No service-account credentials, no
  API keys, no rate-limit-prone services. Reads only public raw.github
  URLs + the unauthenticated GitHub Org API. Safe to run from anywhere.
- **Auto-commit**: workflow commits the regenerated files with
  `[skip ci]` so the nav-consistency / visual-consistency / Pages
  build workflows don't re-trigger every 6h.

## What's deliberately NOT exposed

These are intentional omissions, not gaps:

- **Active GAS deployment URLs** (credentialing webhook, advisory bridge,
  Stripe routing, etc.). The webhook URLs are unauthenticated and would
  let any agent trigger production actions. Kept private; if an LLM
  needs to know "is there a webhook for X" the answer is "ask an operator."
- **Service-account JSON** (Google Sheets credentials, Edgar identity
  RSA keys, autopilot PAT). Always in operator env / Script Properties,
  never in repo, never in `stats/`.
- **Per-partner address / region** (lives on the Agroverse Partners sheet,
  requires `google_credentials.json`). Honestly flagged in
  `partners_index.json.interpretation_hint` rather than pretending the
  data isn't there.
- **Per-contributor email** (privacy — see
  `memory/feedback_no_email_on_public_cv.md`). Member directory
  exposes display name and pk_hash only.

## How to extend the surface

When you notice an LLM consistently hitting a gap (a question that should
be one-fetch but currently requires scraping or human help):

1. **Pick a clean filename** under `stats/<dimension>.json`. One file per
   conceptual dimension (`programs_index`, `partners_index`,
   `repos_index`, `beerhall_archive`). Don't bloat `current.json` —
   keep it for headline numbers + most-recent pointers.
2. **Add a builder function** to `truesight_me_beta/scripts/build_stats_current.py`.
   Read from public raw.github / unauthenticated GitHub API where
   possible. If you need authenticated data, route through a separate
   workflow that has the credential as a secret AND surface only the
   aggregated digest, not the raw credential-bearing payload.
3. **Wire the call** into `main()` so the 6h cron picks it up.
4. **Update `llms.txt`** with: (a) a line under "Public data sources"
   describing the file + one-line use-case hint, (b) a line under
   "How to answer questions about the DAO" with a "Q → fetch URL" rule.
5. **Update this doc's table** so future sessions see the extension.
6. **Sync prod**: `gh repo sync TrueSightDAO/truesight_me_prod --source TrueSightDAO/truesight_me_beta --force` after the beta merge.

Don't:
- Don't add a new file without updating `llms.txt` — the routing map
  is what makes the new file discoverable.
- Don't put live numbers in `llms.txt` itself — it's a stable map,
  not a refresh target.
- Don't try to be exhaustive in a single file — separate dimensions
  into separate files. Agents can fetch what they need.

## The deploy-target lookup

`scripts/build_stats_current.py` carries a small hand-maintained
`REPO_DEPLOY_TARGETS` dict mapping repo name → production URL. Keep it
in sync as new repos ship public surfaces. Repos that don't deploy
(libraries, CLIs, data caches) or that deploy privately (GAS webhooks)
have `deploy_target: null` in the rendered index — no need to add them.

When adding a new public web surface, the convention is:
- truesight.me subdomain → add to the lookup
- agroverse.shop subdomain → add to the lookup
- Standalone domain → add to the lookup
- GAS web app URL → don't add (kept private)
- Internal-only Rails / EC2 → don't add

## Landing-page tile expanders (companion UX)

`truesight_me_beta/index.html` carries `<details class="stat-breakdown">`
expanders under the `USD Treasury Balance` and `Assets Under Management`
tiles. They lazy-fetch `treasury-cache/dao_offchain_treasury.json` on
first open and render the per-ledger / per-currency breakdown inline.
Same data the LLM stats surface uses. If you add a new tile whose
headline number rolls up multiple underlying values, follow the same
pattern — add a `<details>` block, give it `data-breakdown="<key>"`,
add a render function in the `wireStatBreakdowns()` block.

## Footgun: DO NOT `gh repo sync --force` to truesight_me_prod

**2026-05-19 incident.** A previous session ran
`gh repo sync TrueSightDAO/truesight_me_prod --source TrueSightDAO/truesight_me_beta --force`
after every beta merge. The `--force` flag overwrote `truesight_me_prod`'s
`CNAME` file (`truesight.me`) with beta's value (`beta.truesight.me`),
because both repos carry a `CNAME` file at root but they are intentionally
*different*. GitHub Pages then released the `truesight.me` claim. The
production site went down with "The custom domain `truesight.me` is
already taken" until a manual CNAME restore.

Rules for promoting beta → prod:

- **Never** pass `--force` to `gh repo sync` when the source and target
  repos hold a divergent CNAME file (or any file that's allowed to
  differ between repos). The default non-force sync is fast-forward
  only and will refuse to clobber.
- If `gh repo sync` (no force) refuses because of CNAME divergence,
  do **not** force through it. The right move is: rebase the
  divergent file in source to match target, or use a sync flow that
  excludes the file.
- **truesight_me_prod has a self-healing guardrail** (`/.github/workflows/protect-cname.yml`)
  that runs on every push to main and auto-restores `CNAME` to
  `truesight.me` if it drifts. The same pattern is worth replicating
  on any prod fork whose CNAME differs from its beta source.
- The right structural fix would be: a custom sync script that
  excludes a configurable allow-list of files (CNAME, anything in
  `_site/`, etc.) before pushing. Not yet built. Until then, the
  guardrail workflow + this rule are the discipline.

Same caveat applies to **agroverse_shop_prod** ← **agroverse_shop_beta**
(`agroverse.shop` vs `beta.agroverse.shop`). When force-syncing that
pair, the same risk exists. If it ever bites, copy the
`protect-cname.yml` pattern with `agroverse.shop` as the target value.

## Verification checklist

After any change touching this surface:

- [ ] `python3 scripts/build_stats_current.py` runs locally without
      errors and writes all expected files.
- [ ] Each rewritten JSON file parses (`python3 -m json.tool`).
- [ ] `llms.txt` mentions every file under `stats/`.
- [ ] The beta PR merges + `gh repo sync` promotes to prod.
- [ ] `gh api repos/TrueSightDAO/truesight_me_prod/contents/<new-file>?ref=main`
      confirms the file is on prod tree (CDN may still serve stale for
      ~5 min; tree query bypasses).
