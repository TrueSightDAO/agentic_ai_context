#!/usr/bin/env bash
#
# backup_credentials.sh — encrypt the credential manifest into iCloud Drive.
#
# Reads ~/Applications/agentic_ai_context/CREDENTIAL_MANIFEST.txt, tars the
# listed paths preserving structure relative to $HOME, and pipes through
# `openssl enc -aes-256-cbc -pbkdf2 -iter 600000` using the passphrase in
# ~/.credential_vault_passphrase. Output lands in:
#
#   ~/Library/Mobile Documents/com~apple~CloudDocs/credential_vault/
#       credentials-YYYYMMDD-HHMMSS.age
#       credentials-latest.age            (symlink, always points at newest)
#
# Retention: keeps the 30 most recent snapshots, prunes older ones.
#
# Designed to be safe under launchd WatchPaths: includes a 60-second debounce
# so rapid edits don't produce dozens of near-identical snapshots.
#
# Exit codes:
#   0  — backup succeeded, or skipped due to debounce
#   1  — manifest missing
#   2  — passphrase file missing
#   3  — encrypt failed (output not written, tmpfile cleaned up)
#
# See CREDENTIAL_VAULT.md for the threat model + restore runbook.

set -euo pipefail

MANIFEST="${HOME}/Applications/agentic_ai_context/CREDENTIAL_MANIFEST.txt"
PASSPHRASE_FILE="${HOME}/.credential_vault_passphrase"
VAULT_DIR="${HOME}/Library/Mobile Documents/com~apple~CloudDocs/credential_vault"
RETENTION=30
DEBOUNCE_SEC=60

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

# ─── Pre-flight ────────────────────────────────────────────────────────
[[ -f "$MANIFEST" ]] || { log "ERROR: manifest not found at $MANIFEST"; exit 1; }
[[ -s "$PASSPHRASE_FILE" ]] || {
  log "ERROR: passphrase file not found or empty at $PASSPHRASE_FILE"
  log "       Create it with: printf 'YOUR_PASSPHRASE' > $PASSPHRASE_FILE && chmod 600 $PASSPHRASE_FILE"
  exit 2
}

# Refuse to run if passphrase file is world-readable (defense in depth)
PERMS=$(stat -f '%Sp' "$PASSPHRASE_FILE")
if [[ "$PERMS" != *"------"* && "$PERMS" != "-rw-------" ]]; then
  log "WARNING: tightening passphrase file perms to 600 (was $PERMS)"
  chmod 600 "$PASSPHRASE_FILE"
fi

mkdir -p "$VAULT_DIR"

# ─── Debounce: skip if a backup ran within DEBOUNCE_SEC ────────────────
# `|| true` because empty-glob `ls` returns nonzero and would trip pipefail.
LATEST=$(ls -t "$VAULT_DIR"/credentials-*.age 2>/dev/null | head -1 || true)
if [[ -n "${LATEST:-}" ]]; then
  NOW=$(date +%s)
  MTIME=$(stat -f %m "$LATEST")
  AGE_SEC=$((NOW - MTIME))
  if (( AGE_SEC < DEBOUNCE_SEC )); then
    log "Recent backup ${AGE_SEC}s ago at $(basename "$LATEST") — skipping"
    exit 0
  fi
fi

# ─── Resolve manifest paths ────────────────────────────────────────────
declare -a PATHS=()
declare -a MISSING=()
while IFS= read -r line || [[ -n "$line" ]]; do
  # strip CR (in case manifest was edited on a system with CRLF), trim
  line="${line%$'\r'}"
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  expanded="${line/#\~/$HOME}"
  if [[ -e "$expanded" ]]; then
    # Path must live under $HOME to be safely re-rooted on restore.
    if [[ "$expanded" != "$HOME"* ]]; then
      log "WARNING: manifest path is outside \$HOME — skipping: $line"
      continue
    fi
    PATHS+=("${expanded#$HOME/}")
  else
    MISSING+=("$line")
  fi
done < "$MANIFEST"

if (( ${#PATHS[@]} == 0 )); then
  log "ERROR: manifest produced zero existing paths — refusing to write empty vault"
  exit 1
fi

if (( ${#MISSING[@]} > 0 )); then
  log "Note: ${#MISSING[@]} manifest path(s) not present on this host:"
  for m in "${MISSING[@]}"; do log "  - $m"; done
fi

# ─── Build encrypted snapshot ──────────────────────────────────────────
TS=$(date +%Y%m%d-%H%M%S)
OUT="$VAULT_DIR/credentials-${TS}.age"
TMP="$OUT.tmp"

cleanup() {
  rm -f "$TMP"
}
trap cleanup EXIT

log "Encrypting ${#PATHS[@]} path(s) → $(basename "$OUT")"

# tar streams from $HOME so the archive contains $HOME-relative paths;
# openssl enc consumes the stream with PBKDF2 (600k iter) + AES-256-CBC.
if ! ( cd "$HOME" && tar -czf - "${PATHS[@]}" ) | \
       openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -salt \
                   -pass file:"$PASSPHRASE_FILE" -out "$TMP"; then
  log "ERROR: encrypt pipeline failed"
  exit 3
fi

mv "$TMP" "$OUT"
trap - EXIT

# Update the "latest" symlink atomically (so restore always knows newest)
ln -sfn "$(basename "$OUT")" "$VAULT_DIR/credentials-latest.age"

SIZE=$(stat -f %z "$OUT")
log "Wrote $(basename "$OUT") (${SIZE} bytes)"

# ─── Prune old snapshots beyond RETENTION ──────────────────────────────
# (portable to bash 3.2 on macOS — no mapfile)
SNAPSHOTS=()
while IFS= read -r snap; do
  SNAPSHOTS+=("$snap")
done < <(ls -t "$VAULT_DIR"/credentials-*.age 2>/dev/null | grep -v latest || true)
if (( ${#SNAPSHOTS[@]} > RETENTION )); then
  i=$RETENTION
  while (( i < ${#SNAPSHOTS[@]} )); do
    rm -f "${SNAPSHOTS[i]}"
    log "Pruned $(basename "${SNAPSHOTS[i]}")"
    i=$((i+1))
  done
fi

log "Done."
