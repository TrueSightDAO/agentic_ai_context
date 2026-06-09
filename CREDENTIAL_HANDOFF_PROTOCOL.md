# Sensitive credential hand-off protocol (LLM ⇄ Sophia)

**Read this when an agent needs to get a secret (API key, webhook secret, token,
private key) onto a box it cannot reach directly** — e.g. a locked-down EC2 that
only Sophia (the autopilot) can SSH into. Establishes how a local LLM (Claude,
Cursor, etc.) safely stages the secret and hands execution to Sophia.

---

## Why this exists

DAO boxes are intentionally locked down:

- **Security groups** restrict SSH (port 22) to a small allow-list — a local LLM's
  machine usually **cannot reach port 22 at all** (connection times out).
- Each box trusts its **own keypair**, and those private keys live **on the
  autopilot box** (`sophia` → `sophia.truesight.me`), not on the operator's
  laptop. (Example: the beta sandbox box trusts only `~/.ssh/dao-protocol-beta-key`,
  which exists on the autopilot box.)

So the **autopilot box is the credential-staging hub**, and **Sophia is the actor
that propagates secrets to target boxes** (she has the keys + SG access).
ProxyJump / borrowing the fleet key does **not** work unless you hold the target
box's specific keypair — you usually don't.

---

## Hard rules

1. **Never put a secret in chat, a Telegram topic, a PR body, a commit, or any
   file that gets committed.** Transcripts and Telegram logs are durable.
2. **Never echo the secret value to the terminal/transcript.** Move it via
   **stdin pipe**, and only print a masked confirmation (prefix + length).
3. **`chmod 600`** every staged secret file.
4. **Stage OUTSIDE the git repo.** Put staged secrets under **`/home/ubuntu/`** on
   the autopilot box — **NOT** under `/opt/truesight_autopilot/` (its `deploy.sh`
   runs `git reset --hard && git clean -fd`, which deletes untracked files there).
5. **Prefer sourcing an existing secret** over asking the operator to re-fetch —
   e.g. a Stripe **test** key already lives in `sentiment_importer/config/environments/development.rb`
   (`config.stripe_secret`). Reuse it; don't make a human dig in a dashboard.
6. **Test credentials are lower-risk but still secrets** — `sk_test_…` is
   rotatable, but still never paste it in chat.

---

## The protocol (steps)

1. **Source** the secret from a secure existing location (repo config, another
   box's env), or — last resort — ask the operator to place it somewhere readable
   (a file), not paste it in chat.
2. **Stage on the autopilot box** via stdin, masked confirmation only:
   ```bash
   printf '%s' "$SECRET" | ssh sophia 'umask 077; cat > /home/ubuntu/<name>; chmod 600 /home/ubuntu/<name>'
   # verify (masked): ssh sophia 'echo "$(cut -c1-8 /home/ubuntu/<name>)… len=$(wc -c </home/ubuntu/<name>)"'
   ```
3. **Hand off to Sophia in the handoff thread** (the SAME topic she's parked in).
   A local LLM **cannot post into an existing Telegram topic** (the ping tool only
   *creates* topics) — so the operator drops the one-liner, or you give the
   operator the exact text. Tell Sophia: the **staged path**, the **target box**,
   and the **remaining steps** (set on target `.env`, derive any dependent secret
   via API, restart). The Telegram adapter auto-loads the handoff plan
   (`SOPHIA_HANDOFFS.md` lookup) so she has full context.
4. **Sophia propagates**: SSH to the target box with its keypair (from the
   autopilot box), set the secret in the target `.env`, derive dependent secrets
   (e.g. register a webhook via API → signing secret), restart the service, verify.
5. **Rotate** the secret if it was ever exposed (chat, a failed mask, etc.).

---

## Worked example (2026-06-09) — beta sandbox Stripe test key

- **Goal:** get a Stripe **test** secret onto the beta `dao_protocol` box
  (`54.162.175.189`) for `BETA_SANDBOX_ENDPOINT_PLAN.md` Unit 7. Claude could not
  SSH the box (SG blocks 22; the box trusts only `dao-protocol-beta-key`, which is
  on the autopilot box).
- **Sourced** the key from `sentiment_importer/config/environments/development.rb`
  (`config.stripe_secret`, `sk_test_…`) — no operator dashboard trip needed.
- **Staged** at `/home/ubuntu/stripe_test_key` on the autopilot box (`chmod 600`,
  value never printed).
- **Handed off** in Telegram thread 1955: Sophia SSHes the beta box with
  `~/.ssh/dao-protocol-beta-key`, sets `DAO_PROTOCOL_STRIPE_SECRET_KEY`, registers
  the Stripe test webhook via API → `DAO_PROTOCOL_STRIPE_WEBHOOK_SECRET`, restarts
  `dao-protocol-beta`.

---

## Related

- **`SOPHIA_HANDOFFS.md`** — handoff registry + the GO convention (this protocol is
  the credential leg of a handoff).
- **`CREDENTIAL_VAULT.md`** — the governor credential vault (different concern:
  backup/restore of a governor's own identity).
- **`GITHUB_AGENTIC_AI_SSH.md`** — agent SSH keys / push auth.
- **`API_CREDENTIALS_DOCUMENTATION.md`** (sibling repo `agentic_ai_api_credentials`)
  — which env vars each project expects (names only, no secrets).
