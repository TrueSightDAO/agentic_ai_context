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

### Remove duplicate script-tag includes on farm/shipment pages (cachedPath console error)
**Filed 2026-08-20. Owner: unclaimed.** Discovered during agroverse_shop_beta#196 (PR0 of
FARM_SHIPMENT_MEDIA_JSON_PLAN): many farm/shipment pages double-include `config.js` /
`farms-data.js` / `partners-data.js`, and `partners-data.js` declares top-level `let cachedPath`,
so the second include throws `Identifier 'cachedPath' has already been declared` — a console error
that violates the media-externalization plan's UAT "zero console errors" requirement on every
affected page. Affected: `farms/oscar-bahia` (FIXED in PR0), `farms/fazenda-santa-ana-bahia`,
`shipments/agl0`, `agl1`, `agl2`, `agl5`, `agl6`, `agl7`, `agl8`, `agl10`, `agl13`, `agl14`.
Fix per page: keep exactly ONE include each of `config.js` / `farms-data.js` / `partners-data.js`
(remove the duplicate second set near the bottom of `<body>`). ~5 min per page. Verify with
`npx playwright test` zero-console-error specs.

### Program onboarding must create BOTH manifests (web + lineage-credentials internal)
**Filed 2026-08-20. Owner: unclaimed.** The IVY yoga onboarding (2026-08-18/19) created only the web-facing
`truesight_me/programs/ivy-yoga/manifest.json`; the internal `lineage-credentials/programs/ivy-yoga/manifest.json`
that `build_cv_cache.py` reads was never created, so the first test attestation (`pk-LaDRlxRBcvN6`) was indexed
but never rendered — fixed 2026-08-20 via `lineage-credentials#17` (added the internal manifest + `fetch-depth: 2`
shallow checkout). The onboarding playbook now documents the internal manifest
(`credentials/CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` §5.3a). Remaining gap: the program-onboard RSA flow
(`process_program_registration_telegram_logs.js` in tokenomics GAS) only collects `[PROGRAM REGISTRATION REQUEST]`
rows as PENDING — provisioning is governor-gated and manual. When that approval/provisioning flow is built or
extended, it should create BOTH manifests (web in `truesight_me`/`truesight_me_beta` + internal in
`lineage-credentials`) as part of approving a program. Until then, agents following the playbook create both.

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

```followup
id: chocolate-subscription-phase2
chat_id: -1003919341801
thread_id: 1939
title: Revisit Chocolate Subscription Phase 2 (fulfillment automation)
created_at: 2026-06-11
condition:
  kind: elapsed_days
  escalate_after_days: 60
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Phase 2 (fulfillment queue sheet + invoice.paid webhook + fulfillment UI +
  sales parser update) was deferred until Linda has successfully received 2
  subscription shipments (~2 months after her first subscribe). When this
  follow-up fires, remind Gary that Phase 2 is ready to build and ask if
  Linda has received 2 shipments yet. If yes, proceed with Phase 2 per
  CHOCOLATE_SUBSCRIPTION_PLAN.md. If not, extend the timer.
  
  Context: Phase 1 (subscribe engine + PDPs + homepage card) is fully built
  and merged. The activation gate in the plan says don't send real subscribers
  until Phase 2 is live, but Gary decided to let Linda subscribe first and
  revisit Phase 2 after 2 successful shipments to validate the model before
  building the automation.
```

```followup
id: warmup-conversion-30day-readout
chat_id: -1003919341801
thread_id: 9346
title: Warm-up conversion 30-day readout check-in
created_at: 2026-07-21
condition:
  kind: elapsed_days
  escalate_after_days: 30
schedule:
  check: weekly
  on_escalate: ping_thread
status: open
description: >
  Pull go_to_market main, read reports/warmup_conver
…