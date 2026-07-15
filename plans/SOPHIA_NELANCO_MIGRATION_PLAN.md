# Sophia (truesight_autopilot) — Explorya → Nelanco Migration Roadmap

**Status:** ✅ **EXECUTED 2026-07-15 — via AMI lift-and-shift (Gary's method), not the fresh-provision path the sections below describe.** Sophia is live in Nelanco.
**Created:** 2026-07-14 | **Owner:** Gary Teh | **Author:** Claude (Opus)
**Convention:** `OPERATING_INSTRUCTIONS.md` §5 / §5a / §5c / §5d.
**Sibling:** `plans/NELANCO_CLAUDE_CODE_BOX_PLAN.md` (the interactive Claude Code box, Nelanco).

---

## ✅ What actually happened (2026-07-15) — AMI approach

Instead of provision-fresh + `deploy.sh` + copy `.env`/session (M1–M2 below), we did an **AMI lift-and-shift** (faithful byte-for-byte clone — carried the Edgar identity, Telethon session, code, nginx, systemd units intact):

1. Created fresh AMI of live Sophia `--no-reboot` (Explorya `ami-0b05acc998af71d0f`, snapshot `snap-0006425e5c71f1623`) — no disruption.
2. Shared AMI+snapshot to Nelanco (unencrypted → simple) → **copied** to Nelanco-owned `ami-049ff1f01152ef25d`.
3. Launched new box **`i-05276b8ae82d6b88c`** (t3.medium, `subnet-de8102b9`, SG `governor-chatbot-sg`) **passive** (user-data disabled the 4 services + `DRY_RUN=true`) so it couldn't double-act.
4. Associated EIP **`3.214.167.219`** (reused an idle EIP — account at allocation cap).
5. Validated faithful clone (identity/session/code intact).
6. **Cutover:** stopped old services → flipped new to production (`DRY_RUN=false`, all 4 active, health 200) → **Route53** `sophia.truesight.me`→`3.214.167.219` → new box serves HTTPS 200.
7. **Backup retargeted** (Cypher-Defense PR #41): Name tag `sophia-nelanco` + `CYPHER_DEFENCE_AWS_*` (Nelanco).
8. **Old Explorya box `i-02c699d3d7efbdc82` STOPPED** (kept for rollback, not terminated).
9. AWS infra doc updated (top banner).

**Still pending (hand-offs):**
- **Fleet SG swap** (auto-mode gated): in `dao-protocol-beta-sg`, add `3.214.167.219/32:22`, remove `52.200.38.206/32:22`. (Rest of fleet reachable intra-VPC via `sophia_infra`.)
- Verify Sophia's SRE fleet tooling from the new box; her carried-over `~/.ssh/config` aliases may need aligning.
- Eventually: terminate the stopped Explorya box + prune old Explorya AMIs; release the now-free old EIP `52.200.38.206`.

*(The M1–M6 sections below are the original plan-of-record, kept for reference.)*

---

## 1. Goal & rationale

Relocate the autonomous **Sophia** autopilot from the **Explorya** account to **Nelanco**, co-located
with the Krake/Perch/Edgar fleet she manages.

- **Today:** Sophia runs in Explorya `440626669078` (instance `i-02c699d3d7efbdc82`, t3.medium, EIP
  `52.200.38.206`, `sophia.truesight.me`) and reaches the Nelanco fleet as a **cross-account bastion** —
  her EIP is allowlisted on the Nelanco fleet SGs.
- **After:** Sophia runs in Nelanco `767697632458` (`vpc-d59748af`), same VPC as the fleet. Removes the
  cross-account hop, simplifies SG allowlisting, and puts both agents (Sophia + the new Claude Code box)
  in one account.

**Non-goal:** changing Sophia's behavior/services — this is a lift-and-shift. Route53 for
truesight.me/agroverse.shop stays in Explorya regardless.

**This is a blue-green migration** (stand up new, cut over, decommission old) — never an in-place move.

---

## 2. Pre-flight (§5d — capture before executing)

- **Old box facts:** Explorya `i-02c699d3d7efbdc82`, EIP `52.200.38.206`, `/opt/truesight_autopilot`,
  systemd units `truesight-autopilot.service` (uvicorn `app.main:app` :8001, **--workers 1 required**),
  `-telegram.service`, `-watchdog.service` (Telethon), `truesight-vault.service` (:8002). Nginx + certbot
  for `sophia.truesight.me`.
- **`.env` is the source of truth on the box** (deploy.sh is merge-only). It holds Sophia's **own Edgar
  identity** (`EMAIL`/`PUBLIC_KEY`/`PRIVATE_KEY`) + accumulated secrets. **MUST be copied from the old box
  to the new box verbatim — NOT regenerated** (regenerating loses Sophia's identity/keys).
- **Telethon watchdog session:** `.telethon_watchdog.session` on the old box authenticates the user-session
  watchdog. Copy it, or re-run `scripts/telethon_login.py` on the new box (interactive).
- **Fleet SG allowlist:** `52.200.38.206/32:22` is present on the fleet SGs (confirmed on
  `dao-protocol-beta-sg`). Enumerate **all** fleet SGs that allowlist `52.200.38.206` so the new EIP can
  replace it. (Or: since the new box is same-VPC, allow the box SG / VPC CIDR instead of a public EIP.)
- **DNS:** `sophia.truesight.me` A-record lives in **Explorya** Route53 → repoint to the new EIP at cutover.
- **AMI backup:** the Cypher-Defense Action `snapshot_autopilot_ami.yml` resolves the box by **Name tag** —
  keep/adjust the tag so backups follow the new box.
- **Provisioning creds:** Nelanco AWS keys are local (`truesight_autopilot/.env` `AWS_*_NELANCO`). Keypair
  `GETDATA_IO_PAIR_20201122`; SSH SG `launch-wizard-1` or a dedicated one; subnet in `vpc-d59748af`.
- **Note:** `scripts/launch_ec2.sh` already *targets* Nelanco `767697632458` (it was stale for the Explorya
  box) — so it's closer to correct for this migration; still confirm subnet/SG/key.

> ✅ Pre-flight Completeness: the box facts, service model, `.env`/session/DNS/SG dependencies are captured
> above; execution units edit scripts already in-repo. Enumerate the exact fleet-SG set (Gate M4) before
> that gate.

---

## 3. Sequenced plan (one unit / turn; infra/DNS/decommission are always-stop gates)

| Unit | What | Advance |
|------|------|---------|
| **M1** | Provision new Sophia box in Nelanco (reuse `launch_ec2.sh` w/ confirmed Nelanco subnet/SG/key; encrypted EBS; **run the autopilot user-data**, unlike the Claude box). | `gate: infra provision` |
| **M2** | Lay down: run `deploy.sh` at the new box, **then copy the OLD box `.env` + `.telethon_watchdog.session` verbatim** (source of truth). Start + verify the 4 systemd units; health `:8001`. | `gate: cred laydown` |
| **M3** | Allocate a dedicated EIP for the new box; **add it to every fleet SG that currently allowlists `52.200.38.206`**. Verify new box → fleet SSH. | `gate: infra/SG change` |
| **M4** | Soak on the new box (chat via DApp, Telegram adapter, watchdog nudge, email poller) with **old box still live** — no DNS change yet. Compare behavior. | verify |
| **M5** | **Cut over** `sophia.truesight.me` → new EIP (Explorya Route53). Nginx/certbot on the new box. | `gate: prod DNS` |
| **M6** | **Decommission:** stop old Explorya box, remove `52.200.38.206` from fleet SGs, release the old EIP, repoint the AMI-backup Action's Name tag. | `gate: decommission` |

**Rollback (any point pre-M6):** repoint `sophia.truesight.me` back to `52.200.38.206`; the old box is
untouched until M6.

---

## 4. Resume tracker

**➡️ RESUME HERE: M1** (not started). Decisions to confirm first: (a) single active Sophia during soak —
run new box services in `DRY_RUN=true` until cutover to avoid double-acting against the same Gmail/repos;
(b) copy vs re-login the Telethon session; (c) dedicated SSH SG vs `launch-wizard-1`.

| Unit | Provisioned | Verified | Cutover/Deployed | Contribution |
|------|-------------|----------|------------------|--------------|
| M1 — provision Nelanco box | ☐ | ☐ | n/a | ☐ |
| M2 — laydown + copy .env/session | ☐ | ☐ | n/a | ☐ |
| M3 — EIP + fleet SG allowlist | ☐ | ☐ | ☐ | ☐ |
| M4 — soak (old box still live) | ☐ | ☐ | n/a | ☐ |
| M5 — DNS cutover | ☐ | ☐ | ☐ | ☐ |
| M6 — decommission Explorya box | ☐ | ☐ | ☐ | ☐ |

---

## 5. Key risks

- **Double-acting autopilot during soak (M4):** two live Sophias against the same Gmail/repos collide. Keep
  the new box `DRY_RUN=true` until M5, or stop the old box's services during soak.
- **`.env` regeneration:** if M2 regenerates instead of copying the old `.env`, Sophia loses her Edgar
  identity + accumulated secrets. **Copy verbatim.**
- **Telethon session:** if not copied, the watchdog needs an interactive re-login on the new box.
- **Fleet SG swap:** removing `52.200.38.206` too early (before the new EIP is allowlisted + verified) cuts
  Sophia's fleet access. Add-new-then-remove-old, never the reverse.
- **Single-worker services:** the autopilot main service must stay `--workers 1` (module-level per-session
  state) — carry the systemd units as-is.
