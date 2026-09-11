# Sophia Repo-Access Model — retire the master allowlist, invert to a denylist

**Status:** Design plan (governor-directed). **Created:** 2026-09-11 | **Governor:** Gary Teh | **Author:** Sophia Truesight (autopilot `i-05276b8ae82d6b88c`)
**Convention:** `OPERATING_INSTRUCTIONS.md` §5 / §5a / §5d / §5e.
**Repos:** code change in `truesight_autopilot` (**own-repo gate — opens PRs only, governor merges**); this plan + manifest row in `agentic_ai_context`.

> ## RESUME HERE: PR1 (this plan + manifest row) — governor GO received 2026-09-11; awaiting PR1 merge to advance to PR2.

## Context

Gary (thread 25181, 2026-09-11):

> "change your codebase such that there is a list where we specifically indicate you are only allowed to write to via CONTENT API and the rest so long as your PAT allows you to push and pull, you should be able to freely do so ... This will help remove this friction point I keep on seeing over and over again regarding your efforts to create new subdomains."

The trigger is the recurring friction of standing up a new subdomain: every new site needs a new repo, and `create_repo()` refuses any name not pre-listed in `settings.allowed_repos` — a **code** edit + PR + deploy per subdomain.

**Diagnosis** (from reading the live code, not the paste-summary): three lists live in `app/config.py`; the master `allowed_repos` (~35 repos) is the friction. Critically it is **not** the true security boundary — the git credential already reaches the whole org:

- `git_tools.py:45` — SSH key `~/.ssh/id_ed25519_truesight_autopilot`, *"authorised on GitHub as **garyjob**"* → can push any repo in the org.
- PAT `settings.github_pat` (`TRUESIGHT_DAO_AUTOPILOT`) — org-wide Contents:RW + PRs:RW.
- So `allowed_repos` is an **advisory/policy** layer atop an org-wide credential. Widening it does not widen the real blast radius; it only removes per-repo friction.

Two of Gary's asks are **already true**:

- The "Content-API-only list" **exists** — it is `api_only_repos`.
- `upload_file_to_github` already **default-allows** anything in `allowed_repos ∪ api_only_repos` (`upload_file_to_github.py:58`).

And the list is **already env-overridable** without a code change (pydantic-settings; verified: `ALLOWED_REPOS` env rewrites `settings.allowed_repos`). Today's friction is "edit `.env` + `systemctl restart truesight-autopilot`" — not "ship a PR". `/opt/truesight_autopilot/.env` currently sets none of the lists (all on code default).

## Pre-flight (§5d — measured live 2026-09-11)

| Fact | Value |
|---|---|
| Settings class | `BaseSettings`, `SettingsConfigDict(extra="ignore", env_file=".env")` — field-name env override works |
| `allowed_repos` | 35 repos (code literal, `config.py:198`) |
| `api_only_repos` | Contents-API-only class (treasury-cache, … farm-media-raw, agent_handoffs) |
| `prod_repos` | dict prod→beta (4 repos) |
| Guard sites | `git_tools.git_push_changes` (163/172), `github_tools.create_repo` (204) + `_merge_pr_handler` (324/326/333), `upload_file_to_github` (58) |
| Env override | `ALLOWED_REPOS` honored ✅ (no `.env` entry today) |
| Reject on new repo | `create_repo` requires a pre-listed name — **the subdomain friction** |
| Own-repo self-merge | **prompt-only, NOT code-enforced** (no code gate found) |
| Service | `truesight-autopilot.service`, restart needed for config change |
| Route53 | `truesight.me` zone reachable from autopilot (subdomain DNS not a blocker) |

## Design — default-allow + two protected classes

```
contents_api_only_repos   → NEVER clone/branch-edit; Contents-API single-file writes only   (= today's api_only_repos)
protected_repos           → NEVER push/branch/merge; promote via sync_beta_to_prod           (= today's prod_repos)
EVERYTHING ELSE           → default ALLOW: clone, branch, PR, merge own PRs, create_repo
```

Keep those two classes because they are *not* about my safety:

- `contents_api_only_repos` is a **correctness** gate — those repos are machine-owned (GAS/workers); a branch-edit races automation and gets regenerated over.
- `protected_repos` is a **safety** gate — prod forks + intentional CNAME divergence + live domains.

`create_repo` becomes **pattern-gated** so subdomains never need a code change again:

```
create_repo_patterns = ["*-program", "cfr-*", "*-site", ...]   # governor-blessed, one list
```

(A) pattern-gated (**recommended**) or (B) fully open — Gary's call.

**Audit log:** every default-allowed write appends to `ecosystem_change_logs` (restores observability the allowlist gave for free).

**Fail-safe strict mode:** keep `ALLOWED_REPOS` as an optional env var — if set, it acts as an explicit allowlist (today's behaviour). Default unset = default-allow. Governor can re-tighten any time without a code change.

**Phase 2 (separate go):** narrow the credential — GitHub App with per-repo installation, or per-repo deploy keys — so *the list is load-bearing* rather than advisory. This is the truest fix; bigger change.

## Units (§5a — ONE PR PER TURN)

| Unit | Deliverable | Repo | Depends |
|---|---|---|---|
| PR1 | this plan + manifest row | agentic_ai_context | — |
| PR2 | `config.py`: default-allow semantics + `create_repo_patterns`; keep `allowed_repos` as optional strict-mode env; unit tests | truesight_autopilot | PR1 |
| PR3 | guard sites: `git_tools` / `github_tools` / `upload_file_to_github` use the new model; `create_repo` pattern gate; tests | truesight_autopilot | PR2 |
| PR4 | audit log to `ecosystem_change_logs` + tests | truesight_autopilot | PR3 |
| PR5 | de-drift `context.py` REPO CLASSES text + tool descriptions | truesight_autopilot | PR3 |
| PR6 | docs: `GITHUB_AGENTIC_AI_SSH.md`, `AUTOPILOT_CODE_MODIFICATIONS.md` §4; file an OPEN_FOLLOWUPS note | agentic_ai_context | PR5 |
| PR7 (opt) | Phase 2 credential narrowing (design + Gary go) | — | PR6 |

Deploy: `deploy_autopilot` after merge (restart for config).

## Risks

- **Default-allow widens accidental-write surface.** Mitigation: audit log + strict-mode env + keep the two classes. Residual: a hallucinated repo name that exactly matches an existing org repo could be written. Low.
- **`own_repos` self-merge rule is prompt-only** — not fixed by this plan; candidate for the next hardening pass.
- **Rename churn:** renaming `api_only_repos` → `contents_api_only_repos` touches many call sites; keep an alias to avoid breakage.
- **Env override footgun:** `.env` sits beside secrets; but this is existing behaviour, only made optional.

## Open decisions (governor)

1. **Invert to denylist?** yes / keep allowlist / keep allowlist but env-only.
2. **`create_repo`:** pattern-gated (A, recommended) or fully open (B)?
3. **Rename the lists,** or keep current names to minimise churn?
4. **Phase 2 credential narrowing:** include now, or defer to its own plan?
