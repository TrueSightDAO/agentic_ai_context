# Task: Deploy dao_protocol onboarding invitation fix

## Status
- [ ] PR #56 merged — code ready
- [ ] Deploy to `dao_protocol_nelanco` EC2
- [ ] Verify onboarding email fires on `[CONTRIBUTOR ADD EVENT]`

## What changed

**PR:** https://github.com/TrueSightDAO/dao_protocol/pull/56

Added a second webhook trigger in `truesight_dao_client/server/dispatch.py` for `[CONTRIBUTOR ADD EVENT]` that fires the GAS `sendOnboardingInvitation` handler. Also added `trigger_with_params()` to `webhook_trigger.py` for webhooks that need extra query params.

The GAS handler (`edgar_send_onboarding_invitation.gs`) is already deployed in the same Apps Script project as the email verification handler. It sends a Seth-Godin-voiced email with the `create_signature.html?em=<email>` link pre-filled.

## Deploy steps

```bash
# SSH to the dao_protocol server
ssh ubuntu@98.93.94.86

# Find the repo directory (likely /opt/dao_protocol or /home/ubuntu/dao_protocol)
cd /opt/dao_protocol

# Pull the merged code
git pull origin main

# Reinstall (if installed via pip install -e .)
source .venv/bin/activate
pip install -e .

# Restart the service
sudo systemctl restart dao-protocol
# OR if using supervisor: sudo supervisorctl restart dao-protocol
# OR if using screen/tmux: kill the old process and restart

# Check it's running
curl http://localhost:8010/healthz
```

## Env vars

The onboarding webhook URL defaults to `DAO_PROTOCOL_WEBHOOK_EMAIL_VERIFICATION` if `DAO_PROTOCOL_WEBHOOK_ONBOARDING_INVITATION` is not set. Since both handlers live in the same GAS project, this should work without changes. But verify:

```bash
# Check current env
grep ONBOARDING /opt/dao_protocol/.env
```

## Verification

After deploy, trigger a test `[CONTRIBUTOR ADD EVENT]` via the DApp or CLI and confirm:

1. The contributor receives the onboarding email (Seth-Godin-voiced, with `create_signature.html?em=<email>` link)
2. The existing `CONTRIBUTOR_ADD_PROCESSING` webhook still fires (sheet append still works)
3. No errors in the dao_protocol logs: `journalctl -u dao-protocol --no-pager -n 50`

## Related docs

- `agentic_ai_context/AWS_DIGITAL_INFRASTRUCTURE.md` — server IPs, SSH keys, architecture
- `agentic_ai_context/CMO_SETH_GODIN.md` — the email voice principles
