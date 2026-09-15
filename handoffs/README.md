# handoffs/ — the handoff registry

This directory holds the **single source of truth** for active execution handoffs and the
machine-readable artifact derived from it.

| File | Role |
|---|---|
| `HANDOFF_MANIFEST.md` | **Source of truth.** Human-facing table: one row per active handoff, with status, Telegram linkage, and the prose `Resume tracker state`. Edit this by hand. |
| `index.json` | **Generated.** Machine-facing mirror consumed by the supervisor loop (`SUPERVISOR_LOOP.md` §2/§8): the state enum, Telegram `message_thread_id` *and* Discord channel/thread ids, plus `generated_at`. |

## Regenerating `index.json`

```bash
python3 scripts/build_handoff_index.py            # write handoffs/index.json
python3 scripts/build_handoff_index.py --stdout    # print, do not write
python3 scripts/build_handoff_index.py --check     # exit 1 if the committed index has drifted
```

**Never hand-edit `index.json`** — it is overwritten on the next regeneration. Change
`HANDOFF_MANIFEST.md` and re-run the builder. `--check` is the intended CI gate.

## Discord linkage

`index.json` carries `discord_channel_id` / `discord_thread_id` per handoff. The manifest
does not yet have those columns, so the fields are `null` until a plan author adds
`Discord channel id` / `Discord thread id` to the manifest header. A row is never dropped
for lacking them.

## Known manifest defects (as of 2026-09-15)

The builder emits `warnings[]` for structural problems it recovers from. Currently:

- **line 25** — a row with 10 cells (an unescaped `|` inside prose), padded/truncated.
- **line 27** — an orphan row fragment (its leading `|` is missing), so it renders inside
the previous row.
- **line 64** — a blank line splits the manifest into two table segments.

Consequence: `scripts/validate_handoff_manifest.py` (which stops at the first break) only
ever sees the **first 3 of 42** rows. The builder is tolerant and reads all segments, but
the underlying manifest should be repaired.
