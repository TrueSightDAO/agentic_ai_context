# Operating instructions for AI agents

**Read this file first** when you load this folder. These rules keep context consistent and prevent conflicts when multiple agents (Claude Code, OpenAI Codex, Gemini CLI, Cursor, etc.) use the same workspace.

---

## 1. Purpose of this folder

This folder (**agentic_ai_context**) is the **shared context** for the workspace under `/Users/garyjob/Applications`. All agents should read it to get up to speed before editing any project. Only one source of truth is maintained here; agents follow the rules below so that context stays useful for everyone.

---

## 2. What to read (in order)

| Order | File | Use it for |
|-------|------|-------------|
| 1 | **OPERATING_INSTRUCTIONS.md** (this file) | Rules for reading and contributing; read first. |
| 2 | **WORKSPACE_CONTEXT.md** | Overview of the workspace: project groups, conventions, cross-repo relationships. |
| 3 | **PROJECT_INDEX.md** | Per-project summary: purpose, stack, entry points, credentials reference. |
| 4 | **agentic_ai_api_credentials** (sibling folder) | Env var names and credential docs only; no secrets. Use when you need to know which env vars a project expects. |
| — | **LEDGER_CONVERSION_AND_REPACKAGING.md** | **Main Ledger conversion / repackaging.** When the task involves combining inventory into new SKUs, `Currency` naming, or cost per unit after conversion, read this file in full (see also **WORKSPACE_CONTEXT.md** §3b). |
| — | **AGROVERSE_QR_CODE_BATCH_GENERATION.md** | **Agroverse serialized QR codes.** When bulk-adding **`Agroverse QR codes`** rows, naming (**`LA`**, **`CC`**, **`CT`**), column **K** GitHub `compiled_` URLs, or running **`tokenomics/.../batch_compiler.py`** / **`to_print/`**, read this playbook (see **WORKSPACE_CONTEXT.md** §5). |
| — | **notes/claude_serialized_qr_sales_YYYY-MM-DD.md** (or newest matching) | **Serialized QR bulk sales via `dao_client`.** When a customer buys many serialized chocolate bars (each with its own QR code) and payment is confirmed (Stripe, etc.), one **`[SALES EVENT]`** per QR code is required (`Item` = QR code ID). Includes fee amortization, `[INVENTORY MOVEMENT]` depletion steps, and live GAS discovery. See **`dao_client/examples/bulk_qr_sales_template.py`** for a reusable script. |
| — | **DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md** | **AI → Edgar `[CONTRIBUTION EVENT]`** convention (PR URLs, explicit body, `dao_client/.env`). **Also covers the `[CONTRIBUTION EVENT]` vs `[CAPITAL INJECTION EVENT]` distinction** — use CONTRIBUTION for time/out-of-pocket expenses; use CAPITAL INJECTION only for external investors wiring into AGL contracts. |
| — | **AGROVERSE_SHOP_NEW_SKU_WEB_CHECKLIST.md** | **agroverse.shop new SKU / PDP.** When launching a new **`product-page/`** SKU, update **farm** and **shipment** HTML grids (**`item-card`** under “Products from This Farm / Shipment”) so discovery matches the PDP; use with **`agroverse_shop/docs/PRODUCT_CREATION_CHECKLIST.md`** (see **WORKSPACE_CONTEXT.md** §4). |
| — | **CMO_SETH_GODIN.md** | **Marketing / CMO consultation.** When the task involves marketing (copy, positioning, campaigns, content, growth, branding), read this file to consult the Agentic AI CMO (Seth Godin) and operate based on his principles and perspective. |
| — | **DR_MANHATTAN.md** | **Strategy / onboarding.** When the task involves strategy, growth, priorities, or onboarding for the Agroverse and TrueSight DAO network, read this file to consult Dr Manhattan and operate based on his perspective. Future use: chatbot for newcomers. |
| — | **GOVERNANCE_SOURCES.md** | **Governance.** Whitepaper (now a static page: `truesight_me/whitepaper/index.html` → truesight.me/whitepaper/; **Google Doc + `fetch_whitepaper.py` deprecated**), proposals (GitHub TrueSightDAO/proposals, Realms; browser for Realms). |
| — | **SYNDICATE_AGREEMENTS.md** | **Syndicate agreement drafting.** When drafting AGL Export Trade Financing Syndicate Agreements, read this first. **Precedence:** Shipment financing = 20% DAO fee; operational fund (invests in other AGLs) = no fee (avoid double-charging). |
| — | **LEAD_LIST_EXTRACTION.md** | **Lead list / Hit List extraction.** When discovering retailer contacts (apothecaries, metaphysical shops) or updating the Hit List, read for Playwright → CSV → append workflow, schema, credentials. |
| — | **TRUECHAIN.md** | **TrueChain integration.** When working on TrueChain (blockchain, mirror service, block explorer, provenance), read TRUECHAIN.md. Includes "For AI Assistants" section, setup, technical proposal. Repo: https://github.com/TrueSightDAO/TrueChain. |
| — | **GITHUB_AGENTIC_AI_SSH.md** | **GitHub pushes by agents.** Dedicated SSH key under `~/.ssh/agentic_ai_github/`; host alias `github.com-agentic-ai` or `GIT_SSH_COMMAND`. **Branch + PR:** new branch per task, PR body with goal / changes / testing / rollout for reviewers; do not push agent work to default branch unless the user explicitly orders it. **If the user explicitly asks to merge to `main` / `master` after the PR:** complete the loop with `gh pr merge` (or web UI) per that doc’s § “When the user requests the full release loop.” Never commit the private key. |
| — | **HANDOFF_MANIFEST.md** | **Active handoff index.** Machine-readable table of all active handoffs from a local LLM to Sophia. Check this first when the governor mentions a "plan" or "handoff." |
| — | **SOPHIA_HANDOFFS.md** | **Sophia handoff registry.** Telegram topic links, session IDs, and status for each handoff. Cross-reference with HANDOFF_MANIFEST.md. |

Other files in this folder (e.g. `AI_SETUP.md`, `GROK_CLI_410_FIX.md`, `CURSOR_AUTO_APPROVE_SETTINGS.md`) are reference docs for setup and fixes; read them when relevant to your task.

---

## 3. Canonical context: do not edit these

The following files are the **authoritative** context. **Do not modify them** unless the user explicitly asks you to update workspace documentation.

- **WORKSPACE_CONTEXT.md**
- **PROJECT_INDEX.md**
- **README.md**
- **OPERATING_INSTRUCTIONS.md**

If you discover something that should change in those files (e.g. a new project, a corrected convention), use **"Suggested context updates"** (see section 5) instead of editing them directly.

---

## 4. Where and how you may contribute

You may add or update context only in the following ways.

### 4.1 Append-only log: `CONTEXT_UPDATES.md`

- **File:** `CONTEXT_UPDATES.md` in this folder.
- **Rule:** **Append only.** Do not remove or rewrite existing lines.
- **Format:** One line per entry: `YYYY-MM-DD | <agent-id> | <short note>`  
  Example: `2025-01-29 | cursor | Noted: krake_local uses Node 20; add to PROJECT_INDEX if human approves.`
- **Use it for:** Short, factual notes (e.g. "X uses Y", "entry point is Z") so other agents or the user can see what was learned. Do not put secrets or long prose here.

### 4.2 Per-agent or per-session notes: `notes/`

- **Folder:** `notes/` inside this folder.
- **Rule:** Create or update only files that identify **you** or the **session**, e.g.:
  - `notes/cursor_2025-01-29.md`
  - `notes/claude_session.md`
  - `notes/grok_notes.md`
- **Do not** overwrite another agent's file unless the filename clearly belongs to you (e.g. your own `*_session.md`).
- **Use it for:** Session summaries, "what I did / what I learned," or structured notes for other agents. Keep filenames predictable (e.g. date or agent name).

### 4.3 Suggested context updates (for human approval)

- When something should change in **WORKSPACE_CONTEXT.md**, **PROJECT_INDEX.md**, or **README.md**, do **not** edit those files yourself.
- Instead, produce a **suggested update** in one of these ways:
  - Append a line to **CONTEXT_UPDATES.md** (see 4.1) describing the change and that it needs human approval, or
  - Write the suggested change in a short note under **notes/** (e.g. `notes/suggested_project_index_update_2025-01-29.md`) and mention that a human should apply it to the canonical file.

---

## 5. Execution convention: roadmap checklist before implementation

**Before writing implementation code for any multi-step build, migration, or refactor, produce a written execution roadmap checklist and commit it to a *tracked* file in this repo (not a gitignored `notes/*.md`).** The roadmap must let any agent or session **stop and resume from where the last one left off** — this is a hard prerequisite, not an optional nicety.

A compliant roadmap includes:

- A **pre-flight checklist** — access, credentials, prerequisites, and decisions to confirm *before* coding.
- A **sequenced plan** — the ordered units of work (e.g. `PR0…PRn`), each independently shippable.
- A **resume tracker** — a status row per unit (e.g. `merged ☐` / `contribution reported ☐`) plus a prominent **"RESUME HERE"** pointer to the first unfinished step.

Keep the roadmap **tracked and current**: update the resume tracker as each unit lands. Per the contribution convention, after each unit merges, **report the DAO contribution before starting the next** (see `DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`).

**Reference example:** `EDGAR_DAO_EXTRACTION_PLAN.md` (Edgar → `dao_protocol` extraction).

---

## 6. Contribution reporting — use dao_client (dao_protocol repo)

When Gary Teh asks you to report a contribution (time, expenses, or any `[CONTRIBUTION EVENT]`), **do not** use the `create_dao_submission` or `submit_contribution` tools. Instead, use the **dao_client** CLI from the **`dao_protocol`** repo:

```bash
cd ~/Applications/dao_client  # or wherever dao_protocol is checked out
source .venv/bin/activate
truesight-dao-report-contribution \
    --type "Time (Minutes)" --amount <minutes> \
    --description "<what was done>" \
    --contributors "Gary Teh" \
    --tdg-issued <computed TDG>
```

- **Time contributions:** 100 TDG per 1 hour → `--tdg-issued` = `100 * minutes / 60`
- **USD expenses:** `--type "USD"` and `--tdg-issued` matches the dollar amount
- **AI agent work:** Use `truesight-dao-report-ai-agent-contribution` instead (requires PR URLs)
- **Always `--dry-run` first** so Gary can review before the real submission
- The `.env` credentials live in `dao_client/.env` (never committed)

Full convention: `agentic_ai_context/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`

## 7. Summary for agents

- **Read first:** OPERATING_INSTRUCTIONS.md → WORKSPACE_CONTEXT.md → PROJECT_INDEX.md (and credentials folder when needed).
- **Pushing code (any repo you edit):** Create a **feature branch**, push with the agent SSH key (`GITHUB_AGENTIC_AI_SSH.md`), open a **Pull Request** whose description stands alone for humans (**goal**, **changes**, **testing**, **rollout / follow-ups**). Do not push agent work directly to the default branch unless the user explicitly orders it.
- **Do not edit:** WORKSPACE_CONTEXT.md, PROJECT_INDEX.md, README.md, OPERATING_INSTRUCTIONS.md unless the user explicitly asks.
- **You may:** Append to `CONTEXT_UPDATES.md`; create/update your own files under `notes/`; suggest changes via CONTEXT_UPDATES or a note instead of editing canonical docs.
- **Before implementing:** For any multi-step build / migration / refactor, commit a *tracked* **execution roadmap checklist** (pre-flight + sequenced plan + resume tracker) **first** — see §5.

---

## 8. dao-client version bump rule

**Any code change to `dao_protocol/packages/dao-client/` MUST bump the version in `package.json` in the same PR, before merge.**

This applies to:
- New features (methods, exports, types)
- Bug fixes (test fixes, validation fixes)
- Refactors that change the public API or behavior

It does **not** apply to:
- Changes to `test/` files only (no source change)
- Documentation-only changes (comments, README)
- CI/workflow changes (`.github/`)

**How to bump:**
- Patch: `1.1.0-rc.2` → `1.1.0-rc.3` (bug fixes, minor additions)
- Minor: `1.1.0-rc.2` → `1.2.0-rc.1` (new features, breaking-ish changes)
- Major: `1.1.0-rc.2` → `2.0.0-rc.1` (breaking changes)

**Why:** The CI publish workflow (`npm-publish-dao-client.yml`) only triggers on pushes to `main` that change `packages/dao-client/package.json`. Without a version bump, the code lands on `main` but never reaches npm — and the Butterfly Effect Club, oracle, and dapp all consume the npm package, not the repo directly.

**Enforcement:** This is a human-review rule. The PR description should call out the version bump explicitly. If a PR merges without a bump, the next agent who notices should open a follow-up PR that bumps the version.

---

## 9. HTML/JS test-before-merge rule

**Any code change to an HTML/JS repo (oracle, capoeira, truesight_me, truesight_me_beta, agroverse_shop, agroverse_shop_beta, dapp_beta, butterfly-effect-club, tribomirimbahia, aora, or any other repo containing `index.html` or frontend JavaScript) MUST be tested with a local JSDom/happy-dom test suite before the PR is merged.**

### Why

Without local testing, the review cycle becomes: submit PR → governor finds bugs → fix → resubmit → governor reviews again. This wastes the governor's time. Testing locally first means the governor reviews working code, not broken code.

### How to set up the test suite

For any HTML/JS repo that doesn't already have one:

```bash
# In the repo root
npm init -y
npm install --save-dev vitest happy-dom
```

Create `vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    environment: 'happy-dom',
    include: ['test/**/*.test.ts'],
  },
});
```

Update `package.json`:
```json
"scripts": {
  "test": "vitest run"
}
```

### What to test

- **DOM state changes** — does the function show/hide the right elements?
- **Link/URL correctness** — are hrefs set correctly?
- **Event handlers** — do click handlers produce the right DOM changes?
- **Edge cases** — what happens when elements are missing?
- **Regression** — does the fix break anything else?

### Process

1. Write the test first (it should fail, proving the bug exists)
2. Apply the fix
3. Run `npm test` — all tests pass
4. Open the PR with both the fix and the tests
5. The governor reviews once, confident the code works

### Repos that already have this setup

| Repo | Test file | How to run |
|------|-----------|------------|
| oracle | `test/credentials.test.ts` | `npm test` |

When you add this setup to a new repo, update this table.

---

## 10. dao-client version audit rule

**Whenever a new version of `@truesight_dao/dao-client` is published to npm, ALL repos that reference it must be bumped in the same session, before the session ends.**

### Why

If only one repo is bumped and others are left on the old version, the old version's bugs (like the `1.1.0-rc.1` constructor crash) continue to break those pages. The governor should not have to chase down stale versions across repos.

### Audit table

| Repo | Uses dao-client? | Current version | Last bumped |
|------|-----------------|----------------|-------------|
| oracle | ✅ | `1.1.0-rc.3` | 2026-06-09 |
| capoeira | ❌ | — | — |
| butterfly-effect-club | ❌ | — | — |
| truesight_me_beta | ❌ | — | — |
| dapp_beta | ❌ | — | — |
| agroverse_shop_beta | ❌ | — | — |
| tribomirimbahia | ❌ | — | — |
| aora | ❌ | — | — |

### Process

1. Publish the new version to npm (CI handles this automatically on merge)
2. Search all org repos for the old version string: `search_code("@truesight_dao/dao-client@<old-version>")`
3. For each repo found, open a PR bumping to the new version
4. Run the repo's test suite (`npm test`) to confirm nothing broke
5. Merge each PR
6. Update this audit table

### Enforcement

This is a human-review rule. The PR description for any dao-client publish should call out which repos need bumping. If a repo is missed, the next agent who notices should open a follow-up PR.

---

## 11. Handoff protocol for all LLMs

- **Read first:** OPERATING_INSTRUCTIONS.md → WORKSPACE_CONTEXT.md → PROJECT_INDEX.md (and credentials folder when needed).
- **Pushing code (any repo you edit):** Create a **feature branch**, push with the agent SSH key (`GITHUB_AGENTIC_AI_SSH.md`), open a **Pull Request** whose description stands alone for humans (**goal**, **changes**, **testing**, **rollout / follow-ups**). Do not push agent work directly to the default branch unless the user explicitly orders it.
- **dao-client version bump rule:** Any code change to `dao_protocol/packages/dao-client/` MUST bump the version in `package.json` in the **same PR**, before merge. This triggers the CI publish workflow so the npm package stays in sync with `main`. See §8 for the full rule.
- **Do not edit:** WORKSPACE_CONTEXT.md, PROJECT_INDEX.md, README.md, OPERATING_INSTRUCTIONS.md unless the user explicitly asks.
- **You may:** Append to `CONTEXT_UPDATES.md`; create/update your own files under `notes/`; suggest changes via CONTEXT_UPDATES or a note instead of editing canonical docs.
- **Before implementing:** For any multi-step build / migration / refactor, commit a *tracked* **execution roadmap checklist** (pre-flight + sequenced plan + resume tracker) **first** — see §5.

---

## 8. dao-client version bump rule

**Any code change to `dao_protocol/packages/dao-client/` MUST bump the version in `package.json` in the same PR, before merge.**

This applies to:
- New features (methods, exports, types)
- Bug fixes (test fixes, validation fixes)
- Refactors that change the public API or behavior

It does **not** apply to:
- Changes to `test/` files only (no source change)
- Documentation-only changes (comments, README)
- CI/workflow changes (`.github/`)

**How to bump:**
- Patch: `1.1.0-rc.2` → `1.1.0-rc.3` (bug fixes, minor additions)
- Minor: `1.1.0-rc.2` → `1.2.0-rc.1` (new features, breaking-ish changes)
- Major: `1.1.0-rc.2` → `2.0.0-rc.1` (breaking changes)

**Why:** The CI publish workflow (`npm-publish-dao-client.yml`) only triggers on pushes to `main` that change `packages/dao-client/package.json`. Without a version bump, the code lands on `main` but never reaches npm — and the Butterfly Effect Club, oracle, and dapp all consume the npm package, not the repo directly.

**Enforcement:** This is a human-review rule. The PR description should call out the version bump explicitly. If a PR merges without a bump, the next agent who notices should open a follow-up PR that bumps the version.

---

## 9. Handoff protocol for all LLMs

When the governor mentions a "plan," "handoff," or asks you to pick up work from another agent:

### 7.1 Pull first, search second

**Always `git pull` the agentic_ai_context remote `main` branch before searching for plan files.**
Plans are committed to the remote by the handing-off LLM (Claude, Cursor, etc.) and may not be
in your local clone. Searching your local cache without pulling will miss new or updated files.

```bash
cd agentic_ai_context && git pull origin main
```

### 7.2 Check the handoff manifest

Read `HANDOFF_MANIFEST.md` — it lists every active handoff with its plan file, status, and
resume tracker state. This is the fastest way to find what you should be working on.

### 7.3 Cross-reference with SOPHIA_HANDOFFS.md

`SOPHIA_HANDOFFS.md` has Telegram topic links and session IDs for rejoining conversations.
Use it when you need to pick up a conversation mid-stream.

### 7.4 Read the plan file

Once you've identified the right plan file from the manifest, read it in full before proposing
any actions. Pay attention to the **pre-flight checklist** and **resume tracker** — they tell
you what's been done and what's next.

### 7.5 If the manifest is empty or unclear

If `HANDOFF_MANIFEST.md` doesn't list the plan the governor mentioned:
1. Pull the remote again (in case it was just committed)
2. Search for the filename pattern (`*PLAN*.md`, `*HANDOFF*.md`)
3. Check `SOPHIA_HANDOFFS.md` registry
4. If still not found, ask the governor for the exact filename

### 7.6 Sophia-specific: update the manifest on handoff

When Sophia (the autopilot) starts, resumes, or completes a handoff, she updates the
relevant row in `HANDOFF_MANIFEST.md` (Status, Resume tracker state, Last manifest update)
and commits it to `main`.

Following this protocol prevents the confusion that occurred on 2026-06-08, where Sophia
searched her local cache for "verification plan" and found a stale file instead of pulling
the remote to discover `RESEND_VERIFICATION_PLAN.md`.

Following these rules keeps the shared context consistent and allows other agents to read and use it reliably.
