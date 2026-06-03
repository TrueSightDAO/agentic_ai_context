# Sophia capability uplift — git, clasp, SSH fleet access, AWS write

**Date opened:** 2026-06-03
**Operator:** Gary Teh
**Executor:** Claude Code (this plan per `OPERATING_INSTRUCTIONS.md` §5)
**Driving complaint:** Sophia (truesight_autopilot, `sophia.truesight.me`, EC2 `i-02c699d3d7efbdc82` in Explorya) keeps hitting missing-permission walls — she cannot do native git (clone/commit/push, edit files >15KB), cannot run clasp deploys (`gas_deploy_project` tool exists but node/clasp/`.clasprc.json` are absent on the box), cannot SSH into the rest of the EC2 fleet, and her `aws_query` tool is software-gated to read-only even though the IAM credentials are Administrator. Filed by Sophia herself in `OPEN_FOLLOW_UPS.md` (items 1–4, 2026-05-31) plus Gary's 2026-06-03 additions (SSH fleet access, AWS write).

**Hard requirement:** every fix must be baked into `truesight_autopilot/scripts/deploy.sh` (and `user-data.sh` where relevant) so future deployments / fresh boxes ship with these capabilities — no one-off hand provisioning that evaporates on the next rebuild.

---

## Verified current state (2026-06-03, probed live)

| Capability | Box state | Gap |
|---|---|---|
| git binary | git 2.34.1 installed | no global identity, no credentials (no `~/.git-credentials`, no helper) — cannot push |
| git tooling (LLM surface) | only GitHub Contents-API tools | create-only `upload_file_to_github` (no sha → no updates); httpx body limits break >15KB files; no native git tool |
| node / clasp | **absent** | `gas_deploy_project` tool refuses to run |
| `~/.clasprc.json` | **absent** | clasp would be unauthenticated even if installed |
| SSH keys | only `authorized_keys` (inbound) | no outbound private key → cannot reach fleet |
| AWS | boto3 creds for `explorya` + `nelanco` (IAM = Administrator) | `aws_query` software allowlist blocks all write-class ops |
| `open_fix_pr` repos | `settings.allowed_repos` | missing `agroverse_shop_beta`, `truesight_me_beta`, `agroverse-inventory`, `.github`, `treasury-cache`; orchestration_specs description list drifts from config |

Local (operator Mac): clasp 3.3.0 under nvm node v20.19.1; `~/.clasprc.json` present (tokens). GETDATA fleet hosts authorize `GETDATA_IO_PAIR_20201122`.

## Key decisions

1. **Git auth = HTTPS + PAT** (workspace convention; `TRUESIGHT_DAO_AUTOPILOT` PAT already in box `.env`). Credential helper script reads the PAT from `/opt/truesight_autopilot/.env` at call time, so PAT rotation never strands git.
2. **Large-file edits via search/replace semantics** in the new git tool — the LLM passes diff hunks, not whole files, so file size stops mattering.
3. **Guardrail kept: Sophia never pushes to `main`/`master` directly** — the git tool always branches + opens a PR (merge stays human/`merge_pr`-gated as today).
4. **Dedicated SSH keypair `sophia_infra` (ed25519)** rather than reusing `GETDATA_IO_PAIR_20201122` — independently revocable, auditable in `authorized_keys` by comment. Private key lives gitignored at `truesight_autopilot/config/ssh/sophia_infra` on the operator Mac (provisioning source of truth) and is synced to the box by `deploy.sh` like the Gmail/Google creds. Pubkey appended once to each fleet host's `authorized_keys` (re-runnable script).
5. **clasp auth = sync operator's `~/.clasprc.json`** to the box (clasp login is interactive OAuth; the token file is the portable artifact). Pinned clasp 3.3.0 to match the operator Mac.
6. **AWS write ops allowed but deliberate:** write-class operations require `confirm_write: true` in the tool call, and a short hard denylist blocks catastrophic/irreversible account-level ops (CloseAccount, organizations Leave*/Delete*, iam DeleteUser on the root automation user, etc.). Reads stay friction-free.

---

## Sequenced plan + RESUME TRACKER

> **RESUME HERE →** PR1 (git capability, truesight_autopilot).

| Unit | Repo | Scope | Status |
|---|---|---|---|
| **PR0** | agentic_ai_context | This plan file | merged ☑ |
| **PR1** | truesight_autopilot | **Git capability:** `app/tools/git_tools.py` (`git_push_changes`: shallow clone → branch → full-content writes and/or search-replace edits → commit → push → open PR; PAT from settings; refuses default-branch pushes), `upload_file_to_github` auto-sha update support, `allowed_repos` additions + orchestration_specs list de-drifted, `deploy.sh` git identity + credential-helper provisioning step | merged ☐ |
| **PR2** | truesight_autopilot | **clasp capability:** `deploy.sh` installs Node 20 (NodeSource) + `@google/clasp@3.3.0` idempotently, syncs `~/.clasprc.json` (mode 600, warn-if-missing); `user-data.sh` gets node for fresh boxes | merged ☐ |
| **PR3** | truesight_autopilot | **SSH fleet + AWS write:** `app/tools/ssh_tools.py` (`ssh_run(host, command)` against host registry mirroring `AWS_DIGITAL_INFRASTRUCTURE.md` §2/§7), `config/ssh/` gitignored key dir + `deploy.sh` sync + keygen-if-missing, `scripts/distribute_sophia_ssh_key.sh` (operator-run, idempotent), `aws_query` write support (`confirm_write` + denylist) | merged ☐ |
| **OPS1** | — | Distribute `sophia_infra.pub` to fleet `authorized_keys` (run from operator Mac) | done ☐ |
| **OPS2** | — | Run `deploy.sh` against the box; verify live: git push round-trip, `clasp login --status`, `ssh_run` against seni_ror, aws_query write dry-check | done ☐ |
| **DOC1** | agentic_ai_context | Mark `OPEN_FOLLOW_UPS.md` items 1–4 resolved; add `sophia_infra` row to `AWS_DIGITAL_INFRASTRUCTURE.md` §7; append `CONTEXT_UPDATES.md`; tick this tracker | merged ☐ |
| **DAO** | — | Single consolidated `[CONTRIBUTION EVENT]` via dao_client | done ☐ |

## Pre-flight checklist

- [x] Box reachable (`ssh truesight-autopilot`) — confirmed
- [x] `TRUESIGHT_DAO_AUTOPILOT` PAT present in box `.env` — confirmed (used by existing GitHub tools)
- [x] Operator `~/.clasprc.json` exists locally — confirmed (clasp 3.3.0)
- [x] Fleet host IPs current — use `AWS_DIGITAL_INFRASTRUCTURE.md` §2 (2026-06-02), NOT stale `~/.ssh/config` aliases (e.g. local `seni_redis_2` alias points at an old IP)
- [x] IAM already Administrator for both accounts — no console work needed for AWS writes

## Rollback

- Git: remove `~/.gitconfig` + helper script on box.
- clasp: `sudo npm rm -g @google/clasp`; delete `~/.clasprc.json` on box.
- SSH: remove `sophia_infra` line from each host's `authorized_keys` (grep the key comment), delete key from box.
- AWS: revert PR3 (gate returns to read-only).
