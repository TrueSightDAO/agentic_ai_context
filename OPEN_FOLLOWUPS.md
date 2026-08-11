# Open follow-ups (cross-session backlog)

> **This is the ONLY open-followups file.** Do not create variant filenames
> (`OPEN_FOLLOW_UPS.md`, `FOLLOWUPS.md`, `TODO.md`, …) — a duplicate
> `OPEN_FOLLOW_UPS.md` existed 2026-05-31 → 2026-06-06 and split the backlog
> across two files until it was merged back here; that file is now a tombstone
> pointing at this one. Sophia / autopilot agents: file new tooling gaps and
> follow-ups **here**, under `## Pending`, via PR.

Short list of **scoped follow-up tasks** future AI agents (Claude / Cursor /
Codex / Kimi / etc.) and humans can pick up between sessions. The bar is:

- One thing that didn't ship in the original PR but logically belongs after it.
- Small enough to fit in a single session (rough cap: ~60 min of focused work).
- Self-contained — the entry has enough context that someone who didn't write
  the original code can act on it without reverse-engineering history.

This file is **not** a replacement for `CONTEXT_UPDATES.md` (which is the
append-only event log) or for project-specific TODOs that live next to the
code (e.g. `# TODO:` comments, `dapp/UX_CONVENTIONS.md`, repo READMEs, or the
"Q5 parked" pattern inside individual proposal docs like
`PARTNER_VELOCITY_PROPOSAL.md`). It is the place for **cross-repo /
cross-session** items that would otherwise rot in chat transcripts.

## Workflow for agents picking up an entry

1. Read the entry. If the **Blocker** still applies, leave it alone.
2. If you're going to ship it, claim it informally by appending a line to
   `CONTEXT_UPDATES.md` (`<agent-id> | starting OPEN_FOLLOWUPS#…`) so parallel
   sessions don't duplicate work.
3. Open a PR. When merged, **move** the entry to the bottom of this file
   under `## Recently shipped` with the PR link, and append a one-line entry
   to `CONTEXT_UPDATES.md`. Keep the **Pending** list short.
4. If the entry is no longer relevant (priorities shifted, blocker permanent,
   etc.), move it to `## Closed without shipping` with a one-line reason.
   Don't silently delete history.

---

## Pending

### Promote `tls_cert_check.sh` fleet TLS monitor into the truesight_autopilot repo
**Filed 2026-08-09. Owner: unclaimed.** The daily fleet-wide TLS health monitor
(`/opt/truesight_autopilot/scripts/tls_cert_check.sh` + `tls-cert-check.timer`/`.service`
on the autopilot box) is deployed and verified but lives only on the box. Promote it
into the `truesight_autopilot` repo (`scripts/tls_cert_check.sh` + a `systemd/` unit
pair + unit tests) so it's version-controlled, testable, and re-deployable. Update
`TLS_CERTIFICATE_RENEWAL_RUNBOOK.md` §3 to point at the repo path once merged.

---

### Complete Etsy order monitoring OAuth setup (blocked on Etsy app approval)
**Filed 2026-07-02. Owner: Gary.** Etsy order monitoring GAS code is written and
pushed to the `agroverse_shop_checkout` GAS project (script ID `1ovx-Hq5L5MgzF32qB_cPV_G5Hc6XshKMAYOmiJY8tZ355gzWUqvFCPvn`).
The Etsy app "Agroverse" at https://www.etsy.com/developers/your-apps is in
**Pending Personal Approval** — until Etsy approves it, OAuth returns
"application not recognized."

Once approved, RESUME steps:
1. Add redirect URI `https://agroverse.shop/etsy/callback` to Etsy app settings.
2. In GAS Script Properties, add `ETSY_SHOP_ID` (your shop ID number).
3. Run `setupEtsyOAuth()` in the GAS editor → visit auth URL → copy code → run `completeEtsyOAuth("CODE")`.
4. Alternatively, use `python3 agroverse_shop/scripts/etsy_oauth.py` locally (not yet created — build it or use GAS).
5. Change the time-driven trigger from `syncStripeOrders` to `syncAllOrders`.
6. Verify by running `syncEtsyOrders()` manually.

Credentials already stored:
- Sophia vault: `etsy_api` (v1)
- Local: `agroverse_shop/.env`
- GAS Script Properties: `ETSY_KEYSTRING`, `ETSY_SHARED_SECRET` (done)

Repo: `TrueSightDAO/agroverse_shop_beta`, commits `624ea22` + `e8eec32`.

### [RESOLVED 2026-06-22, optional hardening remains] QR_CODE_REPOSITORY_TOKEN ↔ lineage-assets write
**Resolved by Claude:** PNG storage was repointed to `lineage-assets` (tokenomics #373/#375) but the
old `QR_CODE_REPOSITORY_TOKEN` (a fine-grained PAT scoped to `qr_codes`) 403'd on `lineage-assets`.
Unblocked by setting the `QR_CODE_REPOSITORY_TOKEN` secret on `TrueSightDAO/tokenomics` to the value of
`market_research/.env` **`ORACLE_ADVISORY_PUSH_TOKEN`** (verified Contents:write on lineage-assets).
Full QR pipeline now goes green — PNG + batch zip both land in lineage-assets (verified HTTP 200).
**Optional hardening (owner, ~5 min, non-blocking):** `ORACLE_ADVISORY_PUSH_TOKEN` is really the
oracle/advisory push token — reusing it for QR uploads couples two unrelated systems (rotating that
token would silently break QR generation). Cleaner: mint a dedicated fine-grained PAT with
**Contents: Read and write** on `TrueSightDAO/lineage-assets` (and `qr_codes` if any legacy reads remain),
then `gh secret set QR_CODE_REPOSITORY_TOKEN --repo TrueSightDAO/tokenomics`. Context:
`QR_GENERATION_DAO_CLIENT_POSTMORTEM.md` RESOLUTION.

### QR render workflow should emit qrs/<id>.json manifest + rebuild qrs_index.json
**Filed 2026-06-22. Owner: unclaimed.** The tokenomics batch QR workflow
(`agroverse_qr_code_web_service/batch_webhook_handler.py` → `github_webhook_handler.py`) uploads only
the compiled **PNG** to `lineage-assets/pngs/`. It does NOT write the per-QR `qrs/<id>.json` manifest
or rebuild `qrs_index.json` — which is what `truesight.me/physical-assets/serialized` reads. So a
workflow-generated QR will have a PNG but won't appear on the serialized page. `lineage-assets/scripts/
qr_generator/batch_compiler.py` already does the full PNG+manifest+index flow (the postmortem used it
manually for batch b08d324b). Either (a) extend the workflow handler to also build+commit the manifest
and rebuild the index, or (b) retire the simple workflow generator and unify QR generation on
`batch_compiler.py`. Gated behind the token grant above (no point until PNGs upload).
