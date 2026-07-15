# Sophia (truesight_autopilot) — Explorya → Nelanco Migration Roadmap

**Status:** Plan-of-record (pre-flight). Not started.
**Created:** 2026-07-14 | **Owner:** Gary Teh | **Author:** Claude (Opus)
**Convention:** `OPERATING_INSTRUCTIONS.md` §5 / §5a / §5c / §5d.
**Sibling:** `plans/NELANCO_CLAUDE_CODE_BOX_PLAN.md` (the interactive Claude Code box, already provisioned in Nelanco 2026-07-14 — this migration consolidates Sophia into the same account).

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
