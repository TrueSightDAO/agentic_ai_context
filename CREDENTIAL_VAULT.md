# Credential Vault — V1

**Goal.** If Gary's MacBook is destroyed, replaced, or wiped, every service
credential the workspace uses can be restored from iCloud Drive with a single
script + one passphrase from LastPass. Roughly 46 files across ~/Applications
`.env`/`credentials/`/`config/`, plus `~/.clasprc-*.json`, `~/.config/gh/`,
`~/.ssh/id_rsa`, and `~/.aws/credentials`.

**Scope.** Credentials only — not source code (those live in GitHub), not
agentic context (lives in committed `agentic_ai_context/` repo), not memory
(noted as an intentional gap; see "Open follow-up" below).

**Status.** V1 shipped 2026-05-29.

---

## Threat model

| Threat | V1 stance |
|---|---|
| MacBook lost / stolen / dead | ✅ Covered — encrypted snapshot in iCloud Drive, passphrase in LastPass. |
| MacBook compromised + attacker has both filesystem + LastPass | ❌ Out of scope. Same exposure as plaintext on disk today. |
| iCloud account breach + LastPass breach (simultaneous) | ❌ Out of scope. Requires correlating two separate breaches across providers; defense via strong passphrase + 2FA on both. |
| Per-credential rotation / least-privilege per-service | ❌ Tier-2 problem. Not addressed by V1. |
| New EC2 host needs creds at provision time | ❌ Different problem — see `OPEN_FOLLOWUPS.md` § "Credential vault for service-account keys (AWS Secrets Manager)". |

**The honest summary.** V1 buys you "MacBook died, here's how I get back" for
~3 hours of one-time setup. It does **not** change your exposure surface on
the laptop itself — credentials are still plaintext on disk while you're using
them. That's fine and intentional; making them not-plaintext on a working
laptop is a vastly more invasive project (per-app keychain integration, etc.)
that doesn't reduce real risk.

---

## Components

| File | Purpose |
|---|---|
| `agentic_ai_context/CREDENTIAL_MANIFEST.txt` | Explicit allowlist of paths to include. Edit to add/remove. |
| `agentic_ai_context/scripts/backup_credentials.sh` | tars manifest → `openssl enc -aes-256-cbc -pbkdf2 -iter 600000` → iCloud Drive. |
| `agentic_ai_context/scripts/restore_credentials.sh` | Inverse. Defaults to latest snapshot; `--keep-old-files` (skip-on-conflict) by default. |
| `~/Library/LaunchAgents/me.truesight.credential-backup.plist` | launchd agent: WatchPaths over credential parent dirs + 3am nightly heartbeat. |
| `~/.credential_vault_passphrase` | 0600 file holding the LastPass-managed passphrase. Read by both scripts. NOT included in the vault itself. |
| `~/Library/Mobile Documents/com~apple~CloudDocs/credential_vault/` | iCloud Drive folder containing `credentials-YYYYMMDD-HHMMSS.age` snapshots + `credentials-latest.age` symlink. Retention 30. |

**Note on the `.age` extension.** Snapshots use `.age` for grep-ability even
though encryption is via `openssl enc` (not the `age` binary). Rationale: V1
needed unattended encryption, and `age` has no passphrase-from-file flag.
LibreSSL 3.3.6 ships on macOS and supports `-pbkdf2 -iter` natively, so no
brew install is required during restore. If the workspace ever moves to a
GUI-attended backup, switching to real `age` is a 5-line script change.

---

## First-time setup

1. **Generate a strong passphrase** (≥ 20 chars, random) — diceware works,
   or `openssl rand -base64 32`. Store it in LastPass under an entry named
   `truesight credential vault`.

2. **Write it to disk** so launchd can read it unattended:
   ```bash
   printf 'YOUR_PASSPHRASE_HERE' > ~/.credential_vault_passphrase
   chmod 600 ~/.credential_vault_passphrase
   ```
   (Note: `printf` not `echo` — `echo` would append a trailing newline that
   `openssl` would treat as part of the passphrase.)

3. **Manual first backup** to verify the pipeline + populate the vault:
   ```bash
   ~/Applications/agentic_ai_context/scripts/backup_credentials.sh
   ```
   This prints a count of files included + any missing manifest paths.
   Expect output to land at
   `~/Library/Mobile Documents/com~apple~CloudDocs/credential_vault/credentials-<ts>.age`.

4. **Verify roundtrip** to a scratch dir before trusting it:
   ```bash
   mkdir -p /tmp/vault_test
   HOME=/tmp/vault_test \
     ~/Applications/agentic_ai_context/scripts/restore_credentials.sh --dry-run
   ```
   (`--dry-run` lists the archive contents without writing.)

5. **Load the launchd agent** so future edits to credential files trigger
   automatic backups:
   ```bash
   launchctl load -w ~/Library/LaunchAgents/me.truesight.credential-backup.plist
   ```
   Confirm it loaded:
   ```bash
   launchctl list | grep me.truesight.credential-backup
   ```
   Touch any credential file (e.g. re-save a `.env`) and a new snapshot
   should appear within a couple of seconds.

---

## Restore runbook (fresh / wiped MacBook)

1. Install Xcode CLT (`xcode-select --install`) and clone
   `agentic_ai_context` from GitHub. Everything else needed by the restore
   script (`openssl`, `tar`, `bash`) is pre-installed.

2. Open LastPass on a phone or another device; copy the
   `truesight credential vault` passphrase.

3. Sign into iCloud so `~/Library/Mobile Documents/com~apple~CloudDocs/`
   becomes visible. Verify the vault is there:
   ```bash
   ls -lt ~/Library/Mobile\ Documents/com~apple~CloudDocs/credential_vault/
   ```

4. Plant the passphrase file (same `printf` invocation as setup step 2).

5. Restore. Defaults to latest snapshot:
   ```bash
   ~/Applications/agentic_ai_context/scripts/restore_credentials.sh
   ```
   Files land in their original `$HOME`-relative locations. Existing files
   are **skipped** by default; pass `--force` if you want overwrite.

6. Re-clone `~/Applications/*` repos as needed; their `.env` files and
   `config/*.json` SA keys are already in place from step 5.

7. Reinstall the launchd agent (same as setup step 5).

**Expected end-to-end time on a fresh Mac:** 15 minutes excluding repo
re-cloning.

---

## Day-to-day operation

You shouldn't have to touch this. Once the launchd agent is loaded, every
time you save a file under a watched credential path, a new encrypted
snapshot is written to iCloud Drive ~60 seconds later (script-level
debounce + launchd's 120-second `ThrottleInterval` smooth bursts).

Sanity check that backups are still running:
```bash
ls -lt ~/Library/Mobile\ Documents/com~apple~CloudDocs/credential_vault/ | head -5
```
The newest snapshot should be no older than ~24 hours (because of the 3am
nightly heartbeat) — if it is, something has stopped the launchd agent and
it's worth a `launchctl list | grep credential-backup` plus a peek at
`/tmp/credential_vault_backup.err`.

---

## Maintenance

**Adding a new credential.** Edit `CREDENTIAL_MANIFEST.txt`, run the script
once by hand to verify. If the new path lives under a directory not already
in the plist's `<WatchPaths>`, also add it there and `launchctl unload &&
launchctl load` the plist so the watcher picks it up.

**Rotating the passphrase.** Pick a new passphrase, write it to LastPass,
update `~/.credential_vault_passphrase`. Run the backup script once to
produce a freshly-encrypted snapshot under the new passphrase. **Old
snapshots remain readable only with the old passphrase** — if you don't
want them readable at all, delete them from iCloud Drive (the script's
retention will get the rest naturally).

**Manifest hygiene.** When you uninstall a service or rotate to a new repo,
remove the old paths from the manifest so missing-path warnings stay
meaningful.

---

## Open follow-ups (not blocking V1)

- **Memory dir not vaulted.** `~/.claude/projects/-Users-garyjob-Applications/memory/`
  contains feedback/project/reference memories that aren't committed to any
  git repo. If the laptop dies before they're written to a recall surface
  (and most aren't), they're lost. V1 deliberately excludes them per scope
  decision; if you want them in, add the dir to `CREDENTIAL_MANIFEST.txt`
  and the directory's parent to `<WatchPaths>`. ~50 KB cost.

- **Verify-on-restore checksum.** The script trusts that openssl + tar
  round-tripped correctly. Adding a SHA-256 of the cleartext tar inside the
  manifest header and verifying after decrypt would close that gap. Worth
  doing once a snapshot has been restored at least once in anger.

- **Tier-2: per-credential vaulting.** When the workspace grows past one
  operator, single-passphrase becomes a sharing problem. SOPS + age + a
  shared age recipient set, or Bitwarden Organization with per-cred items,
  are the obvious next moves. Not relevant for solo operation.

- **Tier-3: host-side vault for EC2 fleet.** See
  `OPEN_FOLLOWUPS.md` § "Credential vault for service-account keys (AWS
  Secrets Manager) so cut-over hosts don't ship without creds". That's a
  separate concern: standing up an SSM/Secrets-Manager source of truth so
  fresh EC2 hosts can pull their service accounts at boot, instead of
  cutovers needing manual SCP from the laptop.
