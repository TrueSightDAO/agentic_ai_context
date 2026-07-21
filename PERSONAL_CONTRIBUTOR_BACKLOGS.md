# Personal contributor backlogs — per-contributor registry

Some contributors periodically ask an agent (Sophia, Claude Code, Cursor, etc.) to do
**personal, non-DAO work** for them — market/trading analysis via Perch (`perch.truesight.me`),
or other personal tasks they explicitly flag as such. This is **not** DAO work and the results
do not belong in this repo or any other DAO-shared artifact. Instead, each contributor who wants
a running backlog keeps one in their **own private repo**, and registers it here so any agent
picking up a personal request from them knows where to log it.

## Registry

| Contributor | Backlog repo | Format | Vault credential name |
|---|---|---|---|
| Gary Teh | `github.com/garyjob/perch-market-analysis` (private) | `BACKLOG.md` — **Queue** (upcoming items) + **Log** (dated entries, most recent first) | `PERSONAL_GITHUB_PAT` (in `sophia.truesight.me/vault/`) |

The **Vault credential name** column is a pointer, not a secret — it names which vault entry an
agent should use for that contributor's repo. It does not by itself grant access; see "Credential
custody" below for what still has to exist in code before this pairing is actionable.

Add yourself here (one row) if you want an agent to log your personal work.
The repo must be **private** and under **your own** account — never a DAO org.

## Convention (for any agent)

**Trigger:** the contributor explicitly flags something as personal, non-DAO work they want
logged (market/trading analysis, or another task they call out as personal) — and *only* that.
Don't log unrelated requests just because they happen in the same session, and don't infer
"personal" from context alone — it must be stated.

**Action:**
1. Check the table above for that contributor. If listed: `git pull` their repo first, do the
   work, append a dated entry to `BACKLOG.md`'s **Log** section (what was asked, what was found,
   any follow-up worth revisiting), add follow-ups to **Queue**, commit + push.
2. If the contributor **isn't listed** but wants this: offer to set up a private repo for them
   (use `garyjob/perch-market-analysis`'s `BACKLOG.md` as the template) and add a row to this
   table — only after they confirm. Don't assume a standing repo exists for someone who hasn't
   registered one.
3. If a contributor is listed but the current request isn't personal work, don't touch their
   repo — the registry is opt-in for a specific trigger, not a general activity log.

## Credential custody for non-DAO repos (open item, 2026-07-18)

Sophia's `truesight_autopilot` git tooling (`app/tools/git_tools.py`) is currently hardcoded to
`TrueSightDAO/*` repos only (SSH key `id_ed25519_truesight_autopilot`, `allowed_repos` gate) — it
has **no existing path** for pushing to a contributor's personal repo. The credential vault
(`sophia.truesight.me/vault/`, governor-authenticated, real feature — see `truesight_autopilot`
`app/vault.py` / `app/vault_routes.py`) can *store* a named credential like `PERSONAL_GITHUB_PAT`,
and Sophia's chat tools can *check* whether one exists (`check_credential`) without ever seeing
the raw value in chat (`SECRET` tier — vault page only, by design). But nothing currently
*consumes* a vault credential to act on a non-DAO repo.

**This table is designed to double as the allowlist for that future tool**, not just human
documentation: repo + credential name are paired per row, so a tool can (1) look up the
contributor's row here, (2) refuse to act if repo/credential aren't both present and paired
exactly as listed, (3) call `vault.get_value(credential_name)` server-side only — never exposing
the raw value to the LLM/chat layer — and (4) push to *only* that repo, branch + PR, never the
default branch (same guardrail `git_tools.py` already uses for DAO repos). That tool doesn't
exist yet; building it is a real feature (new code path in a live autonomous service, touching
credential handling) and needs its own roadmap per `OPERATING_INSTRUCTIONS.md` §5, even though
the scope is now small and well-defined by this table.

## Why a registry instead of one hardcoded repo

Any contributor working with Sophia or Claude Code may want their own personal backlog. A flat
opt-in table here lets each person register their own private repo without any agent (or this
doc) needing to special-case names in prose or code.
