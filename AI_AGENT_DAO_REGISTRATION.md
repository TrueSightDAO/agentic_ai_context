# AI agent → DAO self-registration (interactive LLMs)

**Read this when:** you are an LLM coding agent (Claude Code, Cursor, Codex,
Gemini CLI, etc.) and you need your **own** DAO identity so the contributions you
log are attributed to *you* — not to the operator (`Gary Teh`) and not conflated
with a cron bot.

This is the **interactive-agent** counterpart to
[`SERVICE_IDENTITY_ONBOARDING.md`](SERVICE_IDENTITY_ONBOARDING.md). Pick the right
one:

| You are… | Use | Identity name | Key lives in |
|----------|-----|---------------|--------------|
| An **interactive LLM** logging its own software/doc work | **this doc** | `<Model Vendor>` e.g. `Claude Anthropic` | a dedicated local `.env` (`~/Applications/<slug>_dao_identity/.env`, `0600`, gitignored) |
| An **autonomous cron/service bot** signing events unattended | `SERVICE_IDENTITY_ONBOARDING.md` | `<scope> Bot` e.g. `Faire Sync Bot` | a GitHub Actions secret |

Both rest on the same Edgar rule: **every actor signs with its own RSA keypair
that resolves to an ACTIVE contributor.** An LLM is an actor. So it gets its own
keypair and its own ledger name. Audit hygiene falls out for free — anyone
reading the Contributions ledger can tell at a glance what a human did vs. what
an AI agent did.

---

## The identity that already exists (the pattern to copy)

Claude Code's identity is the reference instance:

- **Contributor name:** `Claude Anthropic` (renamed from `Claude` on 2026-06-16)
- **Email:** `admin+claude@truesight.me` — a Gmail/Workspace **`+alias`** on the
  operator-controlled `admin@truesight.me` inbox, so the verification email lands
  somewhere a human can reach without provisioning a new mailbox.
- **Identity `.env`:** `~/Applications/claude_dao_identity/.env` holds
  `EMAIL`, `PUBLIC_KEY`, `PRIVATE_KEY`. **Mode `0600`, never committed**, separate
  from the operator's `~/Applications/dao_client/.env`.
- **Live status** (sanity check any time):
  ```bash
  cd ~/Applications/dao_client
  DAO_CLIENT_ENV=~/Applications/claude_dao_identity/.env \
    .venv/bin/truesight-dao-auth status
  # → {"registered": true, "contributor_name": "Claude Anthropic", ...}
  ```

To register a **new** agent (e.g. a GPT or Gemini assistant), reproduce this shape
with a new name, a new `+alias`, and a new identity `.env`.

---

## Registration — five steps

### 1. Governor creates the contributor row (human, one-time)

Edgar only accepts a contribution under a name that already exists in the
**Contributors contact information** sheet, mapped to the agent's email. Creating
that row is a **governor-only** privilege, so the human operator does this once
via the DApp:

- `dapp.truesight.me/create_signature.html` (the agent self-registers a row), or
- `dapp.truesight.me/governor_contributor_admin.html` (governor adds it directly).

Set **Name** = the agent's ledger name (e.g. `Claude Anthropic`, `GPT OpenAI`)
and **Email** = the `+alias` (e.g. `admin+gpt@truesight.me`). A CLI for this is
tracked in `CONTRIBUTOR_ADD_CLI_PLAN.md` — prefer it if it has shipped.

> Naming: interactive agents are named `<Model> <Vendor>` (no `Bot` suffix — that
> suffix is reserved for autonomous service identities). Keep it stable; Edgar
> rejects contributions whose `--contributors` string doesn't match the row
> exactly.

### 2–4. The agent generates + registers + verifies its keypair

From the agent's own `.env` (create the dir first — `~/Applications/<slug>_dao_identity/`):

```bash
cd ~/Applications/dao_client
DAO_CLIENT_ENV=~/Applications/<slug>_dao_identity/.env \
  .venv/bin/truesight-dao-auth login --email admin+<slug>@truesight.me
```

`login` generates an RSA-2048 keypair (persisted to that `.env`, `0600`), signs an
`[EMAIL REGISTERED EVENT]`, and Edgar emails a verification link. The flow stands
up a `127.0.0.1:<port>/verify` loopback listener; **clicking the link on the same
machine** auto-captures `em`+`vk` and signs the `[EMAIL VERIFICATION EVENT]`,
flipping the row to **ACTIVE**.

**Same-device constraint:** the loopback only resolves on the machine that ran
`login`. If a human must click the link elsewhere (or it's headless), fall back to:

```bash
DAO_CLIENT_ENV=~/Applications/<slug>_dao_identity/.env \
  .venv/bin/truesight-dao-auth verify --vk '<vk-value-or-full-URL>'
```

(Unattended cron agents poll Gmail instead — see `SERVICE_IDENTITY_ONBOARDING.md`
step 4 and `GMAIL_OAUTH_WORKFLOW.md`.)

### 5. Confirm ACTIVE

```bash
DAO_CLIENT_ENV=~/Applications/<slug>_dao_identity/.env \
  .venv/bin/truesight-dao-auth status   # registered:true + your contributor_name
```

---

## Logging a contribution once registered (what you'll do every turn)

Source the agent identity and submit via the **AI-agent** CLI, which **requires**
`https://github.com/TrueSightDAO/.../pull/<n>` evidence. Always `--dry-run` first.

```bash
cd ~/Applications/dao_client
set -a && . ~/Applications/<slug>_dao_identity/.env && set +a
.venv/bin/truesight-dao-report-ai-agent-contribution \
  --title "<short title>" \
  --body "<what changed + why; include the PR URL in prose too>" \
  --pr "https://github.com/TrueSightDAO/<repo>/pull/<n>" \
  --type "Time (Minutes)" --minutes <n> \
  --contributors "<Your Ledger Name>" \
  --dry-run            # review the signed payload, then re-run without --dry-run
```

- **TDG:** time work earns `100 TDG / hour` (the CLI computes it from minutes).
- **Type:** use `Time (Minutes)` for effort; `USD` for out-of-pocket spend.
- Full convention (PR-URL rules, expense vs. capital-injection, attachments):
  [`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`](DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md).
- Standing rule: **auto-log one consolidated contribution after each completed
  discrete task** (cluster of merged PRs / deployments) — don't wait to be asked.

---

## Anti-patterns

- **Signing your work with the operator's key** (`~/Applications/dao_client/.env`
  / `Gary Teh`). That's the whole reason this doc exists — keep the audit trail
  honest.
- **Committing the identity `.env`.** It holds a private key. `0600`, gitignored,
  never in a chat log. Rotate with `truesight-dao-auth rotate` if exposed.
- **Inventing or misspelling the contributor name.** It must match the
  Contributors row exactly or Edgar 4xx's the submission.
- **Using the `Bot` suffix** for an interactive agent — that's reserved for
  unattended service identities (`SERVICE_IDENTITY_ONBOARDING.md`).
- **A separate mailbox per agent.** The `+alias` trick gives every agent a
  routable address on an existing inbox.

---

## Registered interactive agents

| Agent (ledger name) | Email (`+alias`) | Identity `.env` | Registered |
|---|---|---|---|
| `Claude Anthropic` | `admin+claude@truesight.me` | `~/Applications/claude_dao_identity/.env` | active (renamed from `Claude` 2026-06-16) |
| `Deep Seek` | `admin+deepseek@truesight.me` | `~/Applications/deepseek_dao_identity/.env` | active (registered 2026-06-19) |

When you register a new interactive agent, add a row here.

---

## Related

- [`SERVICE_IDENTITY_ONBOARDING.md`](SERVICE_IDENTITY_ONBOARDING.md) — the
  unattended `<scope> Bot` variant (keys in GitHub Actions secrets, Gmail polling).
- [`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`](DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md) —
  the contribution convention (mandatory PR URLs, type selection, attachments).
- `dao_client/auth.py` (`truesight-dao-auth`) — the login/verify/status/rotate CLI.
- `dapp/create_signature.html` / `dapp/governor_contributor_admin.html` — the
  governor-side contributor surfaces.

*Created 2026-06-18 by Claude Anthropic. Refresh when adding an agent to the table
or when the Edgar auth/contribution contracts change.*
