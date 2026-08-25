# Class Push / Deploy — Standard Operating Procedure

**Audience:** All LLM instances (Sophia, Envoy, Deep Seek, Kimi, Claude) and
sibling autopilots (Bionpact), plus governors making class pushes.
**Purpose:** One audit trail for every push/deploy to a shared system, so we
can always answer: *who pushed, what, where, when, and what happened.*
**Status:** Draft · **Last updated:** 2026-08-25

---

## 1. What counts as a "class push" (must be logged)

| Push type | Example | Ledger `target_type` |
|-----------|---------|----------------------|
| Google Apps Script | `clasp push --force` on a scriptId | `clasp` |
| GAS deploy tool | `gas_deploy_project <scriptId> --push [--with-hooks]` | `gas` |
| Repo push / deploy intent | git push, `sync_beta_to_prod` | `repo` / `prod-sync` |
| EC2 / host | service restart/deploy, versioned release | `ec2` |
| Other | npm publish, DB migration, credential rotation | `other` |

**Rule:** if it changes a shared system in a way another agent could collide
with or need to audit later, it is a class push and it gets a ledger record.

## 2. Where the ledger lives

**TrueSightDAO/ecosystem_change_logs/deploys/** — one append-only record per
push, written via:

```bash
python3 scripts/append_deploy_record.py --agent <identity> --target-type <type> \
  --target-id <scriptId|repo|host> --action "<what you ran>" \
  --result <success|failure|rolled-back|aborted> \
  [--git-ref <sha>] [--lease-id <id>] [--evidence-url <url>] [--notes "..."]
```

Dry-run by default — add `--write` to commit. Records land in
`deploys/entries/` as `.md` + `.json` and the feed index is rebuilt.

## 3. Mandatory record fields

| Field | Required | Values |
|-------|----------|--------|
| `agent` | yes | registered identity (see §5) |
| `target_type` | yes | clasp \| gas \| repo \| ec2 \| prod-sync \| other |
| `target_id` | yes | scriptId, repo, host, URL |
| `action` | yes | the exact command/operation |
| `result` | yes | success \| failure \| rolled-back \| aborted \| in-progress |
| `evidence_url` | yes for success | PR, commit, HTTP URL |
| `lease_id` | no | pre-push lease (see §4) |
| `git_ref` / `notes` | no | context |

**Worked example:**

```bash
python3 scripts/append_deploy_record.py --agent sophia --target-type clasp \
  --target-id 1N6o00N9VtRK --action "clasp push --force" \
  --result success --git-ref a1b2c3d \
  --evidence-url https://github.com/TrueSightDAO/tokenomics/pull/221 --write
```

## 4. The lease / lock step (BEFORE you push)

1. **Check** `deploys/leases/` for an `open` lease on the same `target_id`
   younger than the TTL (30 min).
2. **If a live lease exists** → wait for the owner to close it, or alert the
   owner / governor. **Do not push blind.**
3. **If clear** → write an `in-progress` lease record (see
   `deploys/leases/README.md`), then push.
4. **Close what you open.** After the push, append the final record with the
   matching `lease_id`. A lease older than TTL is abandoned and may be taken
   over (note the takeover).

Phase 2 (tool-enforced): the lease check will be wired into
`gas_deploy_project` and autopilot deploy flows so it blocks, not just
reminds.

## 5. Identity rules

- `--agent` must be a **registered identity** from
  `agentic_ai_context/agents/*.json`: `sophia`, `bionpact`, `envoy`,
  `deep seek`, `kimi`, `claude`.
- The ledger agent name is the *instance identity* (e.g. `sophia`), not a
  personal name. `Sophia Truesight` remains the display name for
  [CONTRIBUTION EVENT]s — do not conflate the two registries.
- **Never log under someone else's identity.** Sign with your own name.

## 6. Failure handling

- Log `failure` / `rolled-back` / `aborted` with as much evidence as a
  success. A broken push with no record is the worst outcome.
- **Append-only.** Corrections are *new* entries referencing the original
  `id` in `notes` — never edit an existing record.
- If you find a stale open lease on a target, close it (or take it over) and
  log it — a zombie lease is itself an incident.

## 7. Roll-out

| Phase | What | Who |
|-------|------|-----|
| 1 (current) | Ledger + script + this SOP; every agent records after each push | all instances |
| 2 | Lease pre-check enforced inside `gas_deploy_project` + autopilot deploy flows | sophia |
| 3 | CI validation: PRs touching clasp mirrors / deploy config must carry a ledger entry | repo-side action |

## 8. Escalation

If you find evidence of a push that **was not logged** (git history shows a
clasp push, no ledger record), open a follow-up in
`OPEN_FOLLOWUPS.md` and tell the governor. Unlogged pushes are how
"who broke it" becomes a mystery — the ledger exists so that never happens
again.
