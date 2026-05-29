#!/usr/bin/env bash
#
# restore_credentials.sh — decrypt a credential vault snapshot back to $HOME.
#
# Usage:
#   restore_credentials.sh                        # restore latest snapshot
#   restore_credentials.sh <path-to-snapshot>     # restore specific snapshot
#   restore_credentials.sh --list                 # list available snapshots
#   restore_credentials.sh --dry-run [snapshot]   # show what WOULD be written
#
# Requires the passphrase in ~/.credential_vault_passphrase (created by you
# on the new Mac, contents pasted from LastPass).
#
# Refuses to overwrite existing files unless --force is passed. Default
# behavior on conflict: skip and warn. This means a first-run restore on a
# clean Mac just works; an accidental run on an active Mac doesn't clobber.
#
# See CREDENTIAL_VAULT.md for the disaster-recovery runbook.

set -euo pipefail

PASSPHRASE_FILE="${HOME}/.credential_vault_passphrase"
VAULT_DIR="${HOME}/Library/Mobile Documents/com~apple~CloudDocs/credential_vault"

DRY_RUN=0
FORCE=0
SNAPSHOT=""
LIST_ONLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --force)   FORCE=1 ;;
    --list)    LIST_ONLY=1 ;;
    -h|--help)
      sed -n '3,18p' "$0"
      exit 0 ;;
    -*)
      echo "Unknown flag: $1" >&2; exit 1 ;;
    *)
      SNAPSHOT="$1" ;;
  esac
  shift
done

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

if (( LIST_ONLY )); then
  if [[ ! -d "$VAULT_DIR" ]]; then
    log "Vault dir not present: $VAULT_DIR"
    exit 1
  fi
  log "Snapshots in $VAULT_DIR (newest first):"
  ls -lt "$VAULT_DIR"/credentials-*.age 2>/dev/null | grep -v latest | head -40
  exit 0
fi

# ─── Resolve which snapshot to restore ─────────────────────────────────
if [[ -z "$SNAPSHOT" ]]; then
  if [[ -L "$VAULT_DIR/credentials-latest.age" ]]; then
    SNAPSHOT="$VAULT_DIR/$(readlink "$VAULT_DIR/credentials-latest.age")"
  else
    SNAPSHOT=$(ls -t "$VAULT_DIR"/credentials-*.age 2>/dev/null | grep -v latest | head -1 || true)
  fi
fi

if [[ -z "$SNAPSHOT" || ! -f "$SNAPSHOT" ]]; then
  log "ERROR: no snapshot found. Tried: ${SNAPSHOT:-(none)}"
  log "       Run --list to see what's available."
  exit 1
fi

if [[ ! -s "$PASSPHRASE_FILE" ]]; then
  log "ERROR: passphrase file not found or empty at $PASSPHRASE_FILE"
  log "       On a fresh Mac: paste passphrase from LastPass and:"
  log "         printf 'YOUR_PASSPHRASE' > $PASSPHRASE_FILE && chmod 600 $PASSPHRASE_FILE"
  exit 2
fi

log "Restoring from: $(basename "$SNAPSHOT")"
log "  size: $(stat -f %z "$SNAPSHOT") bytes"
log "  mtime: $(stat -f %Sm "$SNAPSHOT")"

if (( DRY_RUN )); then
  TAR_FLAGS=(-tzv)
  log "DRY RUN: listing archive contents — nothing will be written"
else
  TAR_FLAGS=(-xz)
  if (( FORCE )); then
    TAR_FLAGS+=(-v)
    log "FORCE mode: existing files will be OVERWRITTEN"
  else
    # macOS tar (libarchive) honors --keep-old-files: skip + report on conflict.
    TAR_FLAGS+=(--keep-old-files -v)
    log "Default mode: existing files will be SKIPPED (use --force to overwrite)"
  fi
fi

# ─── Decrypt + extract ─────────────────────────────────────────────────
if ! openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 \
       -pass file:"$PASSPHRASE_FILE" -in "$SNAPSHOT" \
     | tar "${TAR_FLAGS[@]}" -f - -C "$HOME"; then
  log "ERROR: restore pipeline failed. Most common cause: wrong passphrase."
  exit 3
fi

log "Done."
