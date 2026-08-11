# Nelanco Claude Code Box — Setup & Operations

## Instance

| Field | Value |
|-------|-------|
| Name | `nelanco-claude` |
| Instance ID | `i-01ad5eca707e4445f` |
| Type | t3.medium |
| EIP | `100.57.50.48` |
| DNS | `claude.truesight.me` |
| Account | Nelanco `767697632458` |
| VPC | `vpc-d59748af` |
| Subnet | `subnet-de8102b9` |
| SG | `launch-wizard-1` |
| Keypair | `GETDATA_IO_PAIR_20201122` |
| State | running |

## SSH Access

From Sophia's autopilot box:
```
ssh -i ~/.ssh/NELANCO_aws_20201122.pem ubuntu@100.57.50.48
```

## Gmail OAuth Tokens (deployed 2026-07-16)

| File | Email | Scopes | Location |
|------|-------|--------|----------|
| `admin_token.json` | `admin@truesight.me` | `gmail.modify` | `/home/ubuntu/admin_token.json` |
| `gary_token.json` | `gary@agroverse.shop` | `gmail.modify` | `/home/ubuntu/gary_token.json` |

Both tokens use client ID `667737028020` (Gmail API, not Apps Script).

## SSH Config (bidirectional)

On Claude's box, `~/.ssh/config`:
```
Host sophia
    HostName 3.214.167.219
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519_truesight_autopilot
```

Sophia's public key is in Claude's `~/.ssh/authorized_keys`.
Claude's public key is in Sophia's `~/.ssh/authorized_keys`.

## Status

- [x] Box provisioned (t3.medium, Nelanco)
- [x] SSH key deployed (GETDATA_IO_PAIR_20201122)
- [x] Gmail OAuth tokens for admin + gary
- [x] Bidirectional SSH (Claude ↔ Sophia)
- [ ] Claude Code login via `tmux` → `claude` → `/remote-control` (Gate D — Gary only)
- [ ] Full Sophia-parity env (Python, Node, clasp, etc.)

## Notes

- This box is **interactive** (driven from mobile via `--remote-control`), not autonomous.
- Fleet SSH keys are on this box so Claude can reach other Nelanco hosts.
- The Gmail tokens use `gmail.modify` scope — can read, search, send, and label.
