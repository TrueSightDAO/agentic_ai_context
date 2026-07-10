# Sophia Vault Credential Migration — Implementation Plan + Execution Roadmap

**Goal:** Initialize the credential vault on Sophia's production box and migrate
all credentials currently staged as bare files at `/home/ubuntu/` into the
encrypted vault, then verify Sophia's tools can access them.

**Scope:** `truesight_autopilot` repo (Sophia's own code) + on-box operations.
**Related plan:** `SOPHIA_MULTI_TENANT_GOVERNANCE_PLAN.md` (broader governance,
Phase 3 = vault).

> ## ▶ RESUME HERE
>
> **▶ ACTIVE: Pre-flight.** Nothing built yet (plan written 2026-06-14).
> Start at the **Pre-flight checklist**, then Unit 1.
>
> **🛑 Where to STOP (operator gates):** Sophia initializes the vault + adds
> credentials via her existing tool set; the only gate is **UAT** (Unit 4) —
> the governor verifies each credential can be accessed. Sophia opens PRs
> only, never self-merges own-repo PRs.

**Companion docs:** `SOPHIA_MULTI_TENANT_GOVERNANCE_PLAN.md`, `CREDENTIAL_HANDOFF_PROTOCOL.md`,
`AWS_DIGITAL_INFRASTRUCTURE.md` §7.2.

---

## Architecture primer

The vault (`app/vault.py`) is an **encrypted at-rest credential store** at
`/opt/truesight_autopilot/vault/`:

```
vault/
├── vault.key          # Fernet key (AES-128, chmod 600)
├── vault.json.enc     # Encrypted JSON {name → {purpose, scopes, value(enc), ...}}
└── vault_audit.json   # Plaintext audit log
```

**LLM safety:** Sophia tools call `vault.get_value(name)` internally. Sophia
herself only sees `CredentialRef` (name, purpose, scopes, version) — NEVER
the actual value. The `check_credential` chat tool confirms existence without
revealing the secret.

**Access control:** Governor-only. The `/vault` web page requires
email→RSA JWT auth, checked against the Governors cache. Credential
mutation was never a Telegram action.

---

## Current state (pre-migration)

| File at `/home/ubuntu/` | Type | Purpose | In vault? |
|---|---|---|---|
| `KRAKE_IO_PAT` | GitHub PAT | Admin for all Gary's repos | ❌ |
| `NELANCO_aws_20201122.pem` | SSH RSA key | 16 krake/seni hosts | ❌ |
| `server_us.pem` | SSH RSA key | 3 krake core hosts | ❌ |
| `NELANCO_california_20260213.pem` | SSH RSA key | californian_proxy | ❌ |
| `.clasprc-gary.json` | Clasp OAuth | GAS deploys as garyjob@agroverse.shop | ❌ |
| `stripe_test_key` | Stripe test API key | Beta sandbox | ❌ |
| `CYPHER_DEFENCE_OPS_PAT` | GitHub PAT | Cypher-Defense repo ops | ❌ |

The vault itself (`/opt/truesight_autopilot/vault/`) is **NOT initialized** —
the directory doesn't exist on production.

---

## Pre-flight checklist (verify BEFORE Unit 1)

- [ ] Confirm `deploy.sh` has been run recently so the vault module
      (`app/vault.py`, `app/vault_routes.py`, `app/tools/vault_tools.py`)
      is live on the production box.
- [ ] Confirm Sophia's vault tools are registered in her tool set
      (`check_credential`, `get_vault_url`, `report_missing_credential`).
- [ ] Verify `/opt/truesight_autopilot/` is writable (the vault directory
      will be created here).
- [ ] Confirm the `.env` has `VAULT_ENCRYPTION_KEY` or that the Fernet
      key generation path (`vault.key`) is acceptable.
- [ ] Verify the `/vault` web page is reachable at
      `https://sophia.truesight.me/vault` (nginx routes port 443 → 8001).
- [ ] Identify the SSH tool's credential resolution path — does it hardcode
      paths to `/home/ubuntu/*.pem` or can it be updated to call
      `vault.get_value(name)`?

---

## Execution roadmap (resume tracker)

Legend: ☐ todo · ⧗ in progress · ☑ done · 🛑 operator gate

| Unit | Scope | Repo / target | Status |
|------|-------|---------------|--------|
| **0** | This plan (the baton) | `agentic_ai_context` | ☑ |
| **1** | **Initialize vault** — `vault.initialize()` via Sophia's own tool or a one-shot script. Creates `/opt/truesight_autopilot/vault/`, generates `vault.key` (chmod 600), creates empty `vault.json.enc`. Verify via `vault.is_initialized()` → true. | On-box | ☐ |
| **2** | **Add credentials to vault.** For each staged file at `/home/ubuntu/`, read the value, call `vault.add(name, value, purpose, scopes, "Gary Teh")`. Credentials to migrate: | | |
| | 2a: `github_krake_pat` — value from `/home/ubuntu/KRAKE_IO_PAT`, purpose "GitHub PAT for all Gary's repos", scopes `["github", "git_push", "gh_cli"]` | On-box | ☐ |
| | 2b: `ssh_key_nelanco` — value from `/home/ubuntu/NELANCO_aws_20201122.pem`, purpose "SSH key for 16 Nelanco fleet hosts", scopes `["ssh", "infrastructure"]` | On-box | ☐ |
| | 2c: `ssh_key_server_us` — value from `/home/ubuntu/server_us.pem`, purpose "SSH key for 3 US-East Krake hosts", scopes `["ssh", "infrastructure"]` | On-box | ☐ |
| | 2d: `ssh_key_california` — value from `/home/ubuntu/NELANCO_california_20260213.pem`, purpose "SSH key for californian_proxy", scopes `["ssh", "infrastructure"]` | On-box | ☐ |
| | 2e: `clasp_oauth_gary` — value from `/home/ubuntu/.clasprc-gary.json`, purpose "Clasp OAuth token for garyjob@agroverse.shop GAS deploys", scopes `["google_apps_script", "clasp"]` | On-box | ☐ |
| | 2f: `stripe_test_key` — value from `/home/ubuntu/stripe_test_key`, purpose "Stripe test-mode secret key for beta sandbox", scopes `["stripe", "payments", "test"]` | On-box | ☐ |
| | 2g: `github_cypher_defence_pat` — value from `/home/ubuntu/CYPHER_DEFENCE_OPS_PAT`, purpose "GitHub PAT for Cypher-Defense repo ops", scopes `["github"]` | On-box | ☐ |
| **3** | **Update Sophia's tools to use vault.** Update `ssh_run` and any GitHub/clasp tooling to resolve credentials from the vault via `vault.get_value(name)` instead of hardcoded `/home/ubuntu/` paths. **Note:** If the tools already support vault resolution (Phase 3.5/3.6), this unit is verify-only. | `truesight_autopilot` | ☐ |
| **4 🛑** | **UAT — governor verification.** For each credential, verify Sophia can access it: | | |
| | 4a: Ask Sophia "do you have the `github_krake_pat` credential?" → she calls `check_credential("github_krake_pat")` → returns metadata (not value) | Telegram | ☐ |
| | 4b: Ask Sophia to push a test branch to a Krake-owned repo → she resolves `github_krake_pat` from vault → push succeeds | Telegram | ☐ |
| | 4c: Ask Sophia to SSH into `krake_ror` using `ssh_key_server_us` → she resolves from vault → SSH succeeds | Telegram | ☐ |
| | 4d: Ask Sophia to SSH into `krake_redis` using `ssh_key_nelanco` → SSH succeeds | Telegram | ☐ |
| | 4e: Ask Sophia to `clasp status` on the shopping cart GAS project using `clasp_oauth_gary` → works | Telegram | ☐ |
| | 4f: Ask Sophia to verify the `stripe_test_key` exists in vault (metadata only) | Telegram | ☐ |
| **5** | **Update documentation.** Update `AWS_DIGITAL_INFRASTRUCTURE.md` §7.2 to note credentials are now in the encrypted vault at `/opt/truesight_autopilot/vault/` (not bare files at `/home/ubuntu/`). Update `CREDENTIAL_HANDOFF_PROTOCOL.md` to reference vault as the preferred credential staging method going forward. | `agentic_ai_context` | ☐ |
| **6** | **Clean up bare files.** Once UAT confirms all credentials work from the vault, archive (don't delete) the bare files at `/home/ubuntu/`: move them to `/home/ubuntu/.migrated_to_vault/` with a README noting migration date. This prevents accidental use of stale ungoverned credentials. | On-box | ☐ |

---

## UAT script (governor runs this in the handoff topic)

```
U1. "Sophia, check if vault is initialized"
     → She calls vault.is_initialized() → true, lists credential count

U2. "Sophia, do you have the github_krake_pat credential?"
     → check_credential("github_krake_pat") → metadata only (found:true, purpose, scopes, version:1, created_by:Gary Teh, created_at:...)

U3. "Sophia, push a test file to the tokenomics repo using the vault PAT"
     → She resolves github_krake_pat from vault → git push succeeds → reports PR URL

U4. "Sophia, SSH into krake_ror and run hostname"
     → She resolves ssh_key_server_us from vault → ssh succeeds → returns hostname

U5. "Sophia, SSH into krake_redis and run hostname"
     → She resolves ssh_key_nelanco from vault → ssh succeeds → returns hostname

U6. "Sophia, run clasp status on the shopping cart GAS project"
     → She resolves clasp_oauth_gary from vault → clasp status succeeds → lists files

U7. "Sophia, do you have the stripe_test_key?"
     → check_credential("stripe_test_key") → metadata only

All U1–U7 pass → vault migration complete ✅
```

---

## Risks / open items

- **Tool compatibility.** The existing `ssh_run` and GitHub tools may hardcode
  paths to `/home/ubuntu/*.pem` or `.env` values. If they don't support vault
  resolution yet, Unit 3 becomes a code change (adding `vault.get_value()` calls).
  This is the main dependency — check during pre-flight.
- **Key backup.** The `vault.key` is the master encryption key. Losing it
  means losing all credentials. After initialization, export the key via
  `vault.export_key()` and store it securely (operator responsibility).
- **AMI survival.** The vault directory at `/opt/truesight_autopilot/vault/` is
  INSIDE the deploy directory. `deploy.sh` runs `git reset --hard && git clean -fd`
  which may wipe untracked files. Verify `vault/` is in `.gitignore` AND survives
  deploys. If not, move vault dir to `/home/ubuntu/vault/`.
- **Vault on-resume.** After an AMI-based blue-green rebuild, the vault needs
  to be restored from backup (or re-keyed). Document this in the AMI recovery
  runbook at `AWS_DIGITAL_INFRASTRUCTURE.md` §4.5.

---

## Downstream dependency

This plan is a **prerequisite** for Sophia to operate autonomously on the full
Krake/Seni fleet using governed credentials. Once migrated:
- The `CREDENTIAL_HANDOFF_PROTOCOL.md` workflow changes: new credentials go
  directly into the vault (via the `/vault` web page) instead of staging bare
  files at `/home/ubuntu/`.
- The `~/Applications/ssh_config` on the operator's laptop remains the
  fallback; Sophia's `~/.ssh/config` on her box is the primary path.

---

*Plan owner: this doc. Update the resume tracker as each unit lands.*
*Generated-by: claude-code*
