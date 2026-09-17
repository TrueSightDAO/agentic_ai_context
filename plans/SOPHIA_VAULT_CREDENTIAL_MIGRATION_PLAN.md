# Sophia Vault Credential Migration — Implementation Plan + Execution Roadmap

**Goal:** Initialize the credential vault on Sophia's production box and migrate
all credentials currently staged as bare files at `/home/ubuntu/` into the
encrypted vault, then verify Sophia's tools can access them.

**Scope:** `truesight_autopilot` repo (Sophia's own code) + on-box operations.
**Related plan:** `SOPHIA_MULTI_TENANT_GOVERNANCE_PLAN.md` (broader governance,
Phase 3 = vault).

> ## ▶ RESUME HERE  (updated 2026-09-16)
>
> **▶ ACTIVE: deploy-gated.** As of 2026-09-15 the vault is **live with 42
> credentials** and the SSH keys are migrated:
> - **Unit 1 ☑** vault initialized 2026-06-15.
> - **Unit 2 ☑ (SSH keys)** — `ssh_key_nelanco_aws`, `ssh_key_server_us`,
>   `ssh_key_nelanco_california` are in the vault, **byte-identical** to the
>   bare PEMs (verified by pubkey fingerprint). ⚠️ Names differ from this
>   plan's original 2b/2c/2d (`ssh_key_nelanco`/`ssh_key_california`); the
>   **code** was repointed to the existing names rather than renaming entries.
> - **Unit 3 ☑** — `ssh_run` is vault-native + **host-aware**
>   (`FLEET[host]["vault_key"]`, PR **truesight_autopilot#471**); df-alert cron
>   scripts repointed to `scripts/fleet_probe.py` (PR **#472**).
> - **Unit 5 ◐** — `AWS_DIGITAL_INFRASTRUCTURE.md` §7.2 +
>   `CREDENTIAL_HANDOFF_PROTOCOL.md` updated (this PR).
> - **Unit 4 ☑ UAT — PASSED 2026-09-15** (deployed `1254da2`). SSH keys
>   resolve **from the vault** and fingerprint-match the on-box PEMs; every
>   reachable fleet host returns rc=0. ⚠️ U2: vault name is
>   **`krake_io_pat`**, not `github_krake_pat` (live `GET /user` → `garyjob`).
>   ⚠️ `krake_ror`/`krake_redis` UAT hosts are network-unreachable
>   (SG/timeout — NOT auth); proven via `krake_data` (server_us) +
>   `seni_redis` (nelanco) instead.
> - **Unit 6 ✅ CLOSED — WILL NOT ARCHIVE (Gary, 2026-09-16).** Gary's explicit
>   decision: **do NOT archive any bare `*.pem`** — “You will mess up your ability
>   to enter into boxes as well as GitHub ssh.” Both `~/.ssh/*.pem` AND the
>   top-level `/home/ubuntu/*.pem` stay **in place**. The 3 top-level dups
>   archived on 2026-09-15 as step (a) were **restored** the same day. Rationale:
>   the bare PEMs are the load-bearing identity for box entry + the
>   `~/.ssh/config` aliases; the vault is an ADDITIONAL resolution path, not a
>   replacement. The migration's value is already banked (vault + vault-native
>   tools); archiving the originals only removes the safety net. ⚠️ **Future
>   instances: do NOT re-attempt this archive.**
> - **krake_nginx pin** — pre-existing gap found in UAT (trusts the box ed25519
>   key, NOT server_us as its comment claimed); fixed in PR **#476**.
>
> **Out of scope / separate thread:** `clasp_oauth_gary`, `stripe_test_key`,
> `github_cypher_defence_pat` were NOT migrated — filed in `OPEN_FOLLOWUPS.md`
> (UAT U6/U7 = not-in-vault).
>
> **🛑 Where to STOP (operator gates):** UAT **PASSED**; the only remaining
> gate is the governor/Gary decision on archiving `~/.ssh/*.pem` (Unit 6).
> Deploys are governor-run.

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
| **1 ☑** | **Initialize vault** — `vault.initialize()` via Sophia's own tool or a one-shot script. Creates `/opt/truesight_autopilot/vault/`, generates `vault.key` (chmod 600), creates empty `vault.json.enc`. Verify via `vault.is_initialized()` → true. | On-box | ☐ |
| **2 ◐** | **Add credentials to vault.** (SSH keys ☑ done; 2e–2g NOT migrated — see OPEN_FOLLOWUPS) For each staged file at `/home/ubuntu/`, read the value, call `vault.add(name, value, purpose, scopes, "Gary Teh")`. Credentials to migrate: | | |
| | 2a: `github_krake_pat` — value from `/home/ubuntu/KRAKE_IO_PAT`, purpose "GitHub PAT for all Gary's repos", scopes `["github", "git_push", "gh_cli"]` | On-box | ☐ |
| | 2b: `ssh_key_nelanco` — value from `/home/ubuntu/NELANCO_aws_20201122.pem`, purpose "SSH key for 16 Nelanco fleet hosts", scopes `["ssh", "infrastructure"]` | On-box | ☐ |
| | 2c: `ssh_key_server_us` — value from `/home/ubuntu/server_us.pem`, purpose "SSH key for 3 US-East Krake hosts", scopes `["ssh", "infrastructure"]` | On-box | ☐ |
| | 2d: `ssh_key_california` — value from `/home/ubuntu/NELANCO_california_20260213.pem`, purpose "SSH key for californian_proxy", scopes `["ssh", "infrastructure"]` | On-box | ☐ |
| | 2e: `clasp_oauth_gary` — value from `/home/ubuntu/.clasprc-gary.json`, purpose "Clasp OAuth token for garyjob@agroverse.shop GAS deploys", scopes `["google_apps_script", "clasp"]` | On-box | ☐ |
| | 2f: `stripe_test_key` — value from `/home/ubuntu/stripe_test_key`, purpose "Stripe test-mode secret key for beta sandbox", scopes `["stripe", "payments", "test"]` | On-box | ☐ |
| | 2g: `github_cypher_defence_pat` — value from `/home/ubuntu/CYPHER_DEFENCE_OPS_PAT`, purpose "GitHub PAT for Cypher-Defense repo ops", scopes `["github"]` | On-box | ☐ |
| **3 ☑** | **Update Sophia's tools to use vault.** PR#471 (ssh_run vault-native + host-aware), PR#472 (df-alert → `scripts/fleet_probe.py`) Update `ssh_run` and any GitHub/clasp tooling to resolve credentials from the vault via `vault.get_value(name)` instead of hardcoded `/home/ubuntu/` paths. **Note:** If the tools already support vault resolution (Phase 3.5/3.6), this unit is verify-only. | `truesight_autopilot` | ☐ |
| **4 ☑** | **UAT — PASSED 2026-09-15** (deployed `1254da2`). In-scope (SSH) verified live; per-item results below. | | |
| | 4a: ⚠️ vault name is **`krake_io_pat`** — `check_credential("github_krake_pat")`→found:false; `check_credential("krake_io_pat")`→**found:true** | Telegram | ☑ |
| | 4b: vault PAT resolves + authenticates (live non-mutating `GET /user` → **`garyjob`**) | Telegram | ☑ |
| | 4c: ⚠️ `krake_ror` network-unreachable (TCP22 timeout); `ssh_key_server_us` proven via `krake_data` → **`ip-172-31-19-2`** | Telegram | ☑ |
| | 4d: `krake_redis` is a config alias, not a FLEET host; `ssh_key_nelanco_aws` proven via `seni_redis` → **`ip-172-31-56-185`** | Telegram | ☑ |
| | 4e: ❌ OUT OF SCOPE — `clasp_oauth_gary` NOT in vault (filed) | Telegram | — |
| | 4f: ❌ OUT OF SCOPE — `stripe_test_key` NOT in vault (filed) | Telegram | — |
| **5 ☑** | **Update documentation.** (PR #1198) Update `AWS_DIGITAL_INFRASTRUCTURE.md` §7.2 to note credentials are now in the encrypted vault at `/opt/truesight_autopilot/vault/` (not bare files at `/home/ubuntu/`). Update `CREDENTIAL_HANDOFF_PROTOCOL.md` to reference vault as the preferred credential staging method going forward. | `agentic_ai_context` | ☐ |
| **6 🛑** | **Clean up bare files.** Once UAT confirms all credentials work from the vault, archive (don't delete) the bare files at `/home/ubuntu/`: move them to `/home/ubuntu/.migrated_to_vault/` with a README noting migration date. This prevents accidental use of stale ungoverned credentials. Top-level dups archived 2026-09-15; `~/.ssh/*.pem` HELD pending governor/Gary decision (21 config aliases + fallback safety net). | On-box | ◐ |

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

RESULTS — run 2026-09-15 on deployed `1254da2`:
U1 ✅ vault initialized, 42 credentials
U2 ⚠️ name is `krake_io_pat` (not `github_krake_pat`) — found:true
U3 ✅ vault PAT authenticates (live GET /user → garyjob)
U4 ✅ ssh_key_server_us from vault (via krake_data; krake_ror network-unreachable)
U5 ✅ ssh_key_nelanco_aws from vault (seni_redis → ip-172-31-56-185)
U6 ❌ out of scope — clasp_oauth_gary not in vault (filed)
U7 ❌ out of scope — stripe_test_key not in vault (filed)

In-scope (the 3 SSH keys): ALL PASS ✅ → vault migration complete for the
SSH-key scope. krake_nginx pin gap found + fixed (PR #476). Unit 6 partial
(top-level dups archived; `~/.ssh/*.pem` held).
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
