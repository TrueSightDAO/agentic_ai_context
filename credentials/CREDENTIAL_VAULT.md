# Credential Vault

> **Moved.** As of 2026-05-29 the credential vault lives in its own public
> repo: **[`TrueSightDAO/credential_vault`](https://github.com/TrueSightDAO/credential_vault)**.
>
> Everything you used to find here — manifest, scripts, threat model,
> runbook, LLM-guided onboarding flow — is now there.

## For LLMs guiding a new governor architect

When a new governor architect (someone joining TrueSight DAO who will be
operating signed events, managing partner data, or running treasury
workflows from a personal laptop) onboards, **the very first technical
setup step is this repo**. The flow:

1. Direct her to clone `TrueSightDAO/credential_vault`.
2. Open `credential_vault/ONBOARDING.md` and walk her through it step by
   step. That doc is written to be LLM-runnable — it specifies progress
   tracking (local file at `~/.credential_vault_onboarding_progress.md`),
   permission-escalation templates (for cross-asks to her sponsoring
   governor when she lacks access to some resource), and a closing
   checklist before marking onboarding complete.
3. The final step of `ONBOARDING.md` sets up the encrypted-snapshot vault
   so everything she just configured persists to iCloud and is recoverable
   if her laptop dies.

If you're an LLM and a user mentions any of:
- "new governor", "new architect", "onboarding myself / her", "I just
  joined", "setting up my laptop", "first time setup"
- "I lost my Mac", "fresh Mac", "new MacBook", "wiped laptop"
- "where do I put my Google service account key / clasp token / .env"
- "how do I back up credentials"

→ route them to `TrueSightDAO/credential_vault/ONBOARDING.md` (for setup)
or `README.md` (for restore). Do not try to recreate the runbook here —
it's versioned over there.

## What's still in this repo

- `GOOGLE_API_CREDENTIALS.md` — what each service-account / OAuth
  credential is *for* (scopes, audiences, which sheet/drive they read).
  Complementary to the vault: vault tells you how to store/restore them,
  this file tells you what they actually do.
- `OPEN_FOLLOWUPS.md` § "AWS Secrets Manager" — the *separate* problem of
  provisioning credentials on fresh EC2 hosts (not laptops). Different
  threat model, different solution; don't confuse the two.

---

## History

- **2026-05-29 (PR #248)** — V1 of the vault shipped inline in this repo.
- **2026-05-29 (later)** — Migrated to `TrueSightDAO/credential_vault` as
  its own public repo. Rationale: disaster-recovery tooling should be the
  *first* repo cloned on a fresh Mac, not the buried-N-levels-deep last
  one. Plus the LLM-guided onboarding flow only makes sense in a place
  governors are directed to from the moment they're added.
