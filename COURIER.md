# Courier — local media upload daemon (this Mac → Sophia `/media/to_process`)

> **Courier** is the launchd daemon on Gary's Mac that reliably moves large farm/event media
> zips to Sophia's Media Archives Pipeline (MAP) intake funnel — chunked, resumable across
> sleep/wake and flaky/low-throughput internet, with per-zip completion notifications.
>
> This is the **local front door** to [`MEDIA_ARCHIVE_PIPELINE.md`](MEDIA_ARCHIVE_PIPELINE.md)
> (and `FARM_MEDIA_INTAKE_GO_LIVE_PLAN.md`). See "How it feeds MAP" below.

## TL;DR for a fresh LLM session

1. Zips to upload go in **`~/Applications/upload_to_sophia/`**.
2. Courier (launchd job **`com.garyjob.courier`**) picks them up automatically — no manual step.
3. When a zip finishes, macOS fires a notification *"<name>.zip is in /media/to_process — tell
   Sophia the context for this zip."* — that's the cue to inform Sophia of the zip's farm/context
   (a zip not in `zip_farm_ids` is fail-closed skipped).
4. Courier skips + deletes any zip already in Sophia's archive manifest — don't re-upload.

## Components (all on the local machine)

| Path | What it is |
|---|---|
| `~/Applications/upload_to_sophia/` | **Drop folder** — put `*.zip` here to upload |
| `~/Applications/upload_to_sophia/done/` | Retired zips after a verified upload |
| `~/Applications/chunked_upload.sh` | The one-shot uploader (processes the drop folder, then exits) |
| `~/Applications/courier.sh` | Courier's forever-loop wrapper (calls the uploader, polls every 60 s) |
| `~/Library/LaunchAgents/com.garyjob.courier.plist` | launchd agent (KeepAlive) — survives sleep/wake, reboot, crash |
| `~/Applications/courier.log` | Combined stdout/stderr log |
| `~/.cache/chunked_upload/<zipname>/` | Per-zip cache: split chunks + sha256 manifests (resume state) |

## How one zip flows through

1. **Discover** — the uploader finds every `*.zip` in the drop folder (alphabetical order).
2. **Already-processed guard** — it fetches Sophia's archive manifest (the `"zip"` field of every
   `/media/processed/*.archive.json` and `/media/upload_zips/*.archive.json`) and, if a local
   zip's name is already there, **deletes the local copy and skips it** (it was archived before).
3. **Hash** — full-file `shasum -a 256` (cached to avoid re-hashing on resume).
4. **Split** — `split -b 500M` into `part_XXXX` chunks (cached).
5. **Upload each chunk** — `rsync -avP --inplace --append` to a staging dir on Sophia
   (`/media/to_process_staging/<zipname>/`), gated on an internet check (`nc 1.1.1.1:443`),
   with retry. Each chunk's sha256 is verified on the remote after transfer.
6. **Reassemble + verify** — `cat part_* > <zipname>`, then full-file sha256 compared to local.
7. **Promote** — atomic `mv` into `/media/to_process/` (owned `ubuntu:ubuntu`), so the MAP
   claimer (`farm_media_intake.timer`, 300 s settle) picks it up.
8. **Notify + retire** — macOS notification fires; the local zip moves to `done/` and its cache
   is cleared.

## Key behaviors

- **Resumable / sleep-wake safe.** Courier is a launchd `KeepAlive` agent: when the Mac sleeps it
  suspends and resumes on wake. Chunks + sha256 manifests are cached, so a kill/restart (or a
  sleep that drops the SSH connection) resumes from the last good chunk via `rsync --append` — no
  restart-from-zero.
- **Internet-aware.** `wait_for_net()` blocks until `1.1.1.1:443` is reachable before each chunk,
  so an outage just pauses rather than erroring.
- **Never trusts the network.** Every chunk and the reassembled file are sha256-verified; a
  mismatch deletes the remote chunk and re-uploads.
- **Fail-safe guard.** Deletion of an "already processed" zip only happens on a *positive*
  manifest match — a failed manifest fetch means no deletion, just upload.

## Gotchas (local machine environment)

- **macOS ships rsync 2.6.9**, which does **not** support `--append-verify` (rsync ≥3.0.0).
  Use `--inplace --append` — do not "upgrade" the flag back to `--append-verify`.
- **macOS bash is 3.2** — no `mapfile`/`readarray`; the scripts use `while IFS= read` loops.
- The scripts assume SSH `sophia` resolves via `~/.ssh/config` and needs no passphrase.

## Operations

```bash
# status / logs
launchctl print gui/$(id -u)/com.garyjob.courier | grep -E "state|pid"
tail -f ~/Applications/courier.log

# stop / start
launchctl bootout  gui/$(id -u)/com.garyjob.courier
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.garyjob.courier.plist

# run once by hand (no daemon)
bash ~/Applications/chunked_upload.sh
```

## How it feeds MAP (remote side)

`/media/to_process/` is the MAP intake front door on the autopilot box
(`sophia` = `sophia.truesight.me`). `farm_media_intake.timer` claims a settled zip →
`/media/processing/`, then the archive worker resolves it via the `zip_farm_ids` map
(`/opt/truesight_autopilot/media_archive_daemon_config.yaml`) → S3 `raw/<farm_id>/`, then
promotes to `/media/processed/` (writing a `.archive.json` sidecar).

**A zip absent from `zip_farm_ids` is fail-closed skipped.** That's why the completion
notification says "tell Sophia the context": the human step adds the zip → farm_id mapping (or
tells Sophia which farm it is) so the archive worker doesn't skip it.

## Replication checklist (other machines)

1. Copy the files (`chunked_upload.sh`, `courier.sh`, the plist) and adjust absolute paths /
   `REMOTE_HOST` / SSH identity to the target machine.
2. Ensure tools present: `nc`, `rsync`, `split`, `shasum` (all present on a stock macOS/Linux box).
3. `mkdir -p ~/Applications/upload_to_sophia`; `chmod +x` the scripts.
4. Install the plist at `~/Library/LaunchAgents/` and
   `launchctl bootstrap gui/$(id -u) <plist>` (macOS). On Linux, use systemd `--user` instead of
   launchd.
5. Config is env-overridable (`UPLOAD_DIR`, `REMOTE_HOST`, `REMOTE_DEST`, `CHUNK_BYTES`,
   `MAX_RETRIES`, …) — see the header of `chunked_upload.sh`.
