# DApp permission change flow — `[DAPP PERMISSION CHANGE EVENT]`

How the DApp lets governors edit `treasury-cache/permissions.json` (action → required-roles map) end-to-end. Same dispatch shape as every other governor-signed write event (`[INVENTORY MOVEMENT]`, `[CONTRIBUTOR ADD EVENT]`, `[EMAIL VERIFICATION EVENT]`); the only thing new is the GAS handler on the receiving end and a sheet for the audit trail.

**Status:** v0.1 (initial build, 2026-04-28). Phase 1 (read-only viewer) shipped at [TrueSightDAO/dapp#190](https://github.com/TrueSightDAO/dapp/pull/190). Phase 2 (this flow) ships in the four paired PRs called out in §6.

---

## 1. End-to-end flow

```
Governor edits in DApp
  └── governor_permissions.html (edit mode, governor-only)
  ↓  signed event text via the existing EDGAR_SUBMIT
     (POST https://edgar.truesight.me/dao/submit_contribution)
Edgar
  ├── persists to "Telegram Chat Logs" (universal audit trail —
  │     SAME sheet every other event lands on)
  └── pattern-matches "[DAPP PERMISSION CHANGE EVENT]" → fires GAS webhook
GAS handler — tdg_identity_management/dapp_permission_change_handler.gs
  ├── reads the latest unprocessed event row(s) from Telegram Chat Logs
  ├── verifies the signer is in the Governors tab (independent re-check;
  │     does NOT trust Edgar's pass-through alone)
  ├── reads current permissions.json from raw.githubusercontent.com
  ├── applies the change in-memory (action key → required_roles list)
  ├── PUTs the new content via GitHub Contents API to TrueSightDAO/treasury-cache
  └── appends a row to "Dapp Permission Changes" tab on the
        Telegram-compilation spreadsheet (1qbZZhf-…) with status, commit
        SHA, and any error message.
```

Every layer carries an audit trail: Telegram Chat Logs (event ledger), Dapp Permission Changes (per-change row with status + commit reference), git history on `treasury-cache/permissions.json`.

---

## 2. Event payload format

Mirror the conventions used by `[INVENTORY MOVEMENT]` etc. The signed text body is exactly:

```text
[DAPP PERMISSION CHANGE EVENT]
- Action: contributor.add
- Required Roles (before): governor
- Required Roles (after): governor, operator
- Manifest Schema Version: 1
- Submitted At: 2026-04-28T18:30:00Z
- Submission Source: https://dapp.truesight.me/governor_permissions.html
--------

My Digital Signature: <PEM or raw SPKI base64>

Request Transaction ID: <RSA-SHA256 signature, base64>

This submission was generated using https://dapp.truesight.me/governor_permissions.html

Verify submission here: https://dapp.truesight.me/verify_request.html
```

**Field rules:**

| Field | Required | Notes |
|---|---|---|
| `Action` | yes | Must match a key under `actions` (or `deferred_actions` if promoting from deferred) on the current `permissions.json`. Reject otherwise. |
| `Required Roles (before)` | yes | Comma-separated. Must equal the current `required_roles` of the action (optimistic concurrency check — prevents double-edit clobbering). |
| `Required Roles (after)` | yes | Comma-separated. The new value. Empty string means "no roles" (which makes the action public — see §5 for the security implication). |
| `Manifest Schema Version` | yes | Must equal the current `schema_version` of the manifest. Reject otherwise (forward-compat guard). |
| `Submitted At` | yes | ISO 8601 UTC. Used for ordering when multiple changes arrive close together. |
| `Submission Source` | yes | The dapp URL that originated the change. |

The signature footer block is unchanged from every other DApp event — Edgar already verifies the RSA-SHA256 signature against the supplied public key before persisting.

---

## 3. `Dapp Permission Changes` tab schema

**Spreadsheet:** `TrueSight DAO Telegram compilation` (`1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`)
**Tab:** `Dapp Permission Changes` (gid `1054656840`)

Row 1 (header, frozen, bold) — set on first write by the GAS handler:

| Col | Header | Written by | Notes |
|-----|--------|-----------|-------|
| A | `Telegram Update ID` | GAS | Foreign key into `Telegram Chat Logs` for the originating event row. |
| B | `Submitted At UTC` | GAS | Parsed from the event body. |
| C | `Actor Public Key` | GAS | The signer's RSA public key (truncated to first 60 chars for readability; full key is on the originating Telegram Chat Logs row). |
| D | `Actor Name` | GAS | Resolved via `Contributors Digital Signatures` join. `(unknown)` if signature doesn't resolve. |
| E | `Is Governor` | GAS | `YES` / `NO` — re-checked against the `Governors` tab at processing time. |
| F | `Action` | GAS | The action key being edited. |
| G | `Roles Before (claimed)` | GAS | What the event said the current roles were. |
| H | `Roles Before (actual)` | GAS | What the manifest actually had at processing time. If different from claimed, status=concurrency_conflict. |
| I | `Roles After` | GAS | The new value the event proposes. |
| J | `Status` | GAS | `applied`, `unauthorized`, `concurrency_conflict`, `unknown_action`, `github_failed`, `dry_run`. |
| K | `GitHub Commit SHA` | GAS | Filled when status=applied. |
| L | `GitHub Commit URL` | GAS | Filled when status=applied — clickable link to the commit on github.com. |
| M | `Notes` | GAS | Error message or human-readable detail. |
| N | `Processed At UTC` | GAS | Timestamp the GAS row finished processing. |

The handler treats the originating Telegram Chat Logs row as the foreign key — if a future re-run catches the same `Telegram Update ID`, it skips (idempotency).

---

## 4. GAS handler — design notes

**File:** `tokenomics/google_app_scripts/tdg_identity_management/dapp_permission_change_handler.gs`
**Apps Script project:** existing `1m8IZPs1vFN99cuu-39kbC-OGXggRVtJtXq5rfSB0M1sCQjMdolEUDuGU` (the tdg_identity_management project that already publishes `dao_members.json`).

Why that project:
- Already has Script Property `CONTRIBUTORS_CACHE_GITHUB_PAT` scoped to `contents:write` on `TrueSightDAO/treasury-cache` — same scope this handler needs (it writes a different file in the same repo).
- Already has the `commitJsonToGithub_(...)` helper from `dao_members_cache_publisher.gs` — reused verbatim for `permissions.json`.
- doGet routing pattern is established; this handler adds another `?action=apply_permission_change` branch. **No `secret` query param** — Edgar's `WebhookTriggerWorker` only forwards `action`, matching every other dispatch handler (`processTelegramChatLogs`, `parseAndProcessTelegramLogs`, etc.). The Apps Script deployment URL itself is the access token (functionally unguessable); real authorization is the per-event RSA signature + Governors-tab membership check inside the handler. Even if the URL leaks, an attacker can only force-process events that already exist on Telegram Chat Logs with valid governor signatures, and processing is idempotent on Telegram Update IDs.
- Audit semantically belongs in identity-management (it's "who can do what").

**Independent governor verification.** The handler must not trust Edgar's pass-through alone — it re-resolves the signer's public key against the `Contributors Digital Signatures` tab and confirms the resulting display name appears in the `Governors` tab. Same defense-in-depth pattern as `inventoryMovementStatusFromTelegramRow_()` in the inventory handler. If the signer is not currently a governor, the handler logs `status=unauthorized` to `Dapp Permission Changes` and does NOT touch GitHub.

**Optimistic concurrency.** Before writing, the handler:
1. Fetches `permissions.json` via the GitHub Contents API (gets current SHA + content).
2. Confirms `Required Roles (before)` in the event matches `actions[<action>].required_roles` at that SHA.
3. If mismatch → `status=concurrency_conflict`, no GitHub write. Operator can re-edit from a fresh viewer load.

**JSON write strategy.** Mutate only the targeted action's `required_roles` array. Preserve all other fields (`description`, `surfaces`, `endpoints`, `dedup`) and the rest of the manifest. Pretty-print with 2-space indent + trailing newline (matches the publisher convention).

**Idempotency.** The handler's "have I seen this Telegram Update ID before?" check reads the existing `Dapp Permission Changes` rows. If the event's update ID is already there with a terminal status (`applied`, `unauthorized`, `unknown_action`), skip. If the prior status was `github_failed` or `concurrency_conflict`, retry.

**Failure modes:**
- Signer not a governor → `status=unauthorized`, no GitHub touch.
- `Action` unknown in current manifest → `status=unknown_action`.
- `Required Roles (before)` doesn't match current state → `status=concurrency_conflict`.
- GitHub PUT 409 (stale SHA — someone else committed in the interim) → retry once with fresh SHA. Second 409 → `status=github_failed`.
- GitHub PUT non-200/409 → `status=github_failed`, full response body in `Notes`.

---

## 5. Security model

**The governor RSA signature is the gate.** Same crypto-grade evidence every other DApp write uses. No shared password, no PR-merge-button click; the actor must have a private key whose public key currently appears in `Contributors Digital Signatures` (status=`ACTIVE`) AND whose display name currently appears in the `Governors` tab (auto-derived 4×/year from the leaderboard).

**Why this is stronger than the previous PR-review path:**
- The signature is a verifiable proof of authority that survives repo-history rewrites.
- Audit lives in three places (Telegram Chat Logs, Dapp Permission Changes, git commit history) — no single layer can quietly hide a change.
- A compromised PAT alone can't forge an event because Edgar verifies the RSA signature before persisting.

**What it does NOT defend against:**
- A compromised governor private key. Mitigation: revoke the key on `Contributors Digital Signatures` (status≠ACTIVE) — handler will reject the next event from that key.
- A rogue but legitimate governor. Mitigation belongs at the governance layer (revoke governor status via the leaderboard's parameters; that already takes a DAO vote per the workbook's Governors-tab copy). For higher assurance, future N-of-M can require ≥2 governors to sign matching events within a time window before the GAS commits — added as a `--require-second-signoff` mode later if the threat model demands it.

**Setting `Roles After` to empty string makes the action public.** That's a security expansion. The handler does NOT prevent it (governor authority extends that far by design), but the `Dapp Permission Changes` row + Telegram Chat Logs row + git history make it loud — three audit surfaces that fire simultaneously.

---

## 6. Shipping pieces (paired PRs)

| Order | Repo | What | Status |
|------:|---|---|---|
| 1 | `agentic_ai_context` | This doc + README index entry. | ✅ |
| 2 | `tokenomics` | GAS file `dapp_permission_change_handler.gs` + clasp-mirror sync; deploys via `clasp push` to script id `1m8IZPs1vFN99cuu-39kbC-OGXggRVtJtXq5rfSB0M1sCQjMdolEUDuGU`. Plus secret-removal followup since Edgar's `WebhookTriggerWorker` only forwards `action`. | ✅ ([#253](https://github.com/TrueSightDAO/tokenomics/pull/253) + [#255](https://github.com/TrueSightDAO/tokenomics/pull/255)) |
| 3 | `sentiment_importer` | Edgar dispatch — new branch in `dao_controller.rb` for `[DAPP PERMISSION CHANGE EVENT]`, new `dapp_permission_change_webhook_url` config in `application.rb`. **Edgar deploys via `./deploy.sh` per `reference_edgar_deploy_model.md`.** | ✅ merged ([#1043](https://github.com/TrueSightDAO/sentiment_importer/pull/1043)); awaiting `./deploy.sh` |
| 4 | `dapp` | `governor_permissions.html` edit mode (per-row role toggle, change-detection, "Submit N changes" button, public-role friction prompt, post-apply auto-refresh). | ✅ ([#191](https://github.com/TrueSightDAO/dapp/pull/191)) |
| 5 | `dao_client` | `report_dapp_permission_change.py` — terminal CLI parallel to the DApp UI. Same signed event format, same pipeline, same audit row. Useful for scripted bulk edits or governors without a browser handy. | ✅ ([#12](https://github.com/TrueSightDAO/dao_client/pull/12)) |

A change submitted from the DApp or CLI is fully applied once Edgar's deploy ships. Until then:
- (2) deployed: GAS handler ready; smoke-testable via `applyDapPermissionChangeNow()` from the Apps Script editor.
- (3) merged but not deployed: events would persist on Telegram Chat Logs but not auto-process. Operator can run `applyDapPermissionChangeNow()` manually.
- (3) deployed: full loop closed end-to-end.

### CLI alternative — `report_dapp_permission_change`

For governors who want to make permission changes from the terminal (or in scripted bulk):

```bash
# Auto-resolve roles-before + schema-version from the live manifest:
python -m truesight_dao_client.modules.report_dapp_permission_change \
    --action contributor.add \
    --roles-after "governor,operator"
```

Same signed event, same Edgar pipeline, same `Dapp Permission Changes` audit row. The `Submission Source` field on the audit row records `dao_client://…` so you can tell whether a given change came from the browser or the CLI. Full reference: `dao_client/README.md` table entry for `report_dapp_permission_change.py`.

---

## 7. Future enhancements

- **N-of-M governor sign-off** — require ≥2 governor-signed matching events for sensitive actions (e.g., anything that changes `contributor.add` or makes an action `public`). Add a `MIN_SIGNATURES` Script Property on the GAS project; handler waits for that many distinct-signer events with matching payload + event UTC inside a window before committing.
- **Per-action sensitivity tiers** in `permissions.json` — `sensitivity: high` actions need 2-of-3 governors, `sensitivity: low` is 1-of-3 (the default today).
- **Public-role gate** — when an event sets `Roles After` to empty (i.e., publicly callable), require an extra confirmation step in the DApp UI ("are you sure this action becomes anonymous-callable? type the action name to confirm"). Server-side enforcement still trusts the signature but the UI friction prevents accidental clicks.
- **Time-bounded changes** — `Required Roles (after)` could include an `until: 2026-06-01T00:00Z` timestamp; the GAS auto-reverts when expired. Useful for temporary elevation during onboarding events. Not a v1 concern.

---

## 8. Pointers

- Phase 1 viewer: [`dapp/governor_permissions.html`](https://github.com/TrueSightDAO/dapp/blob/main/governor_permissions.html), [PR #190](https://github.com/TrueSightDAO/dapp/pull/190).
- Manifest source of truth: [`treasury-cache/permissions.json`](https://github.com/TrueSightDAO/treasury-cache/blob/main/permissions.json), see [`treasury-cache/README.md` § permissions.json](https://github.com/TrueSightDAO/treasury-cache#permissionsjson).
- Roles source of truth: `dao_members.json` schema v3+ (`contributors[].roles`) on `treasury-cache`, published by [`dao_members_cache_publisher.gs`](https://github.com/TrueSightDAO/tokenomics/blob/main/google_app_scripts/tdg_identity_management/dao_members_cache_publisher.gs).
- Workflow conventions: `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` § 9.7 (Gmail label convention pattern that this doc mirrors structurally).
- Edgar deploy mechanics: `reference_edgar_deploy_model.md` (Edgar does NOT auto-deploy on merge — run `./deploy.sh` from `sentiment_importer/`).
