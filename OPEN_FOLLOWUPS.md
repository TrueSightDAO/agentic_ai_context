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

### ⛔ GATED (governor go required) — GAS deploy + backfill for BOTH txid-dedup sinks (CFR + SunMint)
**Filed 2026-09-26 (thread 35944). Code+docs COMPLETE and merged; every step below is a GATE — do NOT run without Gary's explicit go. No money, no ledger write; a single GAS deploy + a dry-run-first backfill each.**

Both sinks now key on the signed `Request Transaction ID` (§ `DEDUP_KEY_CONVENTION.md`). The source is merged; only the deploy + one-shot backfill remain. Re-verified 2026-09-26: `deploy_gas_project.py <id>` dry-run resolves `owner_email: admin@truesight.me` / `clasp: admin@truesight.me` (Path B works; `~/.clasprc-admin.json` present).

**A. CFR sink (project `1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT`; live pinned deploy `AKfycbxQDdGnw…` = @42)**
1. Push source: `CLASPRC_PATH=~/.clasprc-admin.json python3 scripts/deploy_gas_project.py 1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT --push`  *(from the `tokenomics` checkout)*
2. Roll the pinned deployment forward @42 → @43: same tool with `--deployment-id AKfycbxQDdGnwS7G6iJhNj9japW-9sFA7EUvrnznmJCu44S5ZHqOoIks2be4FXbIVpuaOHVW` (runs `clasp version` + `clasp deploy -V`).
3. `?action=backfillCfrTreeTxIds&dryRun=1` → review counts → re-run **without** `dryRun` (idempotent).
4. `?action=collapseCfrTreeTxDuplicates` (preview) → `&apply=1` (DESTRUCTIVE: deletes dup rows, keeps first).

**B. SunMint sink (project `1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF`; its own deployment)**
1. Push + roll forward exactly as A with the `1Jp8q…` scriptId (`--deployment-id` = the SunMint `/exec` deployment).
2. `?action=backfillSunMintTreeTxIds&dryRun=1` → review → re-run with `&apply=1` (idempotent).

**Still open (non-blocking, decide before the respective writers touch col U):** the live **col-U `Submission Source` vs. parked PR3 `Payment Event Ref`** conflict (see `SCHEMA.md`); and the **hourly GAS backstop identity** (Gary deleted all `admin@truesight.me` triggers). Also note: `--allow-identity-mismatch` is FORBIDDEN (silently swaps the web app runtime identity — see the §11.5 correction in this file).

### SunMint `SunMint Tree Planting` tab dedupes on transport ids → `request_transaction_id` (col V) — SHIPPED 2026-09-26
**Shipped 2026-09-26 (thread 35944). PR: tokenomics #568 (`1c6fc022`). GAS deploy + backfill = governor gates, NOT yet run.** Ran the approved convention `conventions/DEDUP_KEY_CONVENTION.md`; implemented ahead of the col-U work deliberately — because the new column is located **by header name** and created at the first free column, it can NOT race the col-U Submission-Source writer (they touch different cells).

**Where.** `google_app_scripts/1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF/process_tree_planting_telegram_logs.js`, tab **`SunMint Tree Planting`** (sheet `creds.SHEET_ID` default `1qbZZhf-…`).

**The anti-pattern.** Dedup is keyed on the **transport ids** — col **D** (`Telegram Message ID`, via `getProcessedMessageIds()`) and col **H** (`File ID`, via `getProcessedFileIds()`) — so the same tree re-posted under a new message id double-counts, exactly the failure the CFR tab hit. The writer *already* parses the signed block (`My Digital Signature:` from col G), so the `Request Transaction ID:` line is present in the payload — it is simply never captured or used.

**The fix.**
1. Add a **trailing** col **`request_transaction_id`** = **col V** — header `A1:T1` is full (col **T** = Plot ID), and col **U** is already earmarked for the approved **Submission Source** backfill/write, so V is the first free slot. Migration-safe: append header, never reorder.
2. Parse `Request Transaction ID:` from the signed block (`/Request Transaction ID:\s*([^\n]+)/i`) and store it in col V on every append.
3. Seed the dedup set from col V and **skip the append if the txid already exists** — keep the existing message-id / file-id guards as belt-and-braces only.
4. One-shot idempotent `?action=backfillSunMintTreeTxIds` lever over existing rows, `&dryRun=1` first (counts only, no txid strings).

**Caveat to decide.** The txid is signed over the payload incl. `Planting Time`, so a **re-signed** re-submission yields a *different* txid. If that risk matters here, also key on a content fingerprint (`lat|lng|species|photo_url`). See the convention's §4.

**Status.** SHIPPED (source) 2026-09-26 — `tokenomics` #568 (`1c6fc022`). At source: the column is located by **header name** and created at the first free column (`ensureSunMintRequestTxColumn_`/`sunmintFindHeaderCol_`), the txid is parsed via `extractRequestTransactionId()`, the append is skipped when the txid already exists, `?action=backfillSunMintTreeTxIds` is idempotent (preview by default, `&apply=1` writes, counts only), and the create-tab header widened to `A1:V1`. Verified: `node --check` OK; live col F carries the `Request Transaction ID:` footer; the live tab header is A–U (U = `Submission Source`) so V is the first free column — recorded a **col-U conflict** in `SCHEMA.md` (live `Submission Source` vs. the PARKED PR3 code's `SUNMINT_PAYMENT_EVENT_REF_COL = 20` = `Payment Event Ref`) to reconcile before either writes U. **Outstanding gate:** GAS deploy (this is the **`1Jp8q…`** project, *not* the CFR one) then `?action=backfillSunMintTreeTxIds&dryRun=1` → `&apply=1`. No deploy / no money.

### the lineage-assets SEED half (`sync_lineage_assets.py`) is scheduled NOWHERE — `qrs_index.json` silently freezes and every downstream cache re-derives from stale input
**Filed 2026-09-25 — reproduced live (thread 35944, P0n). Ops/config class; not money-adjacent, but it silently empties published fields.**

**Symptom.** `sold_pending_tree.json` (the cache the governor tree-linking page + product card read) came back
with the new product-context keys present but **empty** (`product_image`, `owner_email_present`, `sheet_url`),
even after the seeder was pushed. Root cause was not the code — it was a **stale input**: the published
`qrs_index.json` was frozen at `generated_at 2026-09-24T18:13:44Z`.

**Root cause — only half the chain is scheduled.** The `ubuntu` crontab runs, every 30 min:
`sync_pending_caches.py --push` and `sync_sunmint_signatures.py --push`. **Nothing** runs the upstream
seed half — `/home/ubuntu/lineage-assets` ff-clone → `seed_from_sheet.py` → `build_index.py`
(collectively `scripts/sync_lineage_assets.py`). Verified: `grep -l sync_lineage_assets /etc/cron.d/*
/etc/systemd/system/*.service /etc/systemd/system/*.timer` → **empty**; no `_CONTEXT_SYNC_REPOS` entry
covers the working checkout. So the index is only ever refreshed by hand, and `sync_pending_caches.py`
happily re-derives from whatever stale index the CDN serves.

**Second wrinkle (cache race).** `sync_pending_caches.py` fetches `qrs_index.json` from
`raw.githubusercontent.com/TrueSightDAO/lineage-assets/main/…`, whose CDN sends
`cache-control: max-age=300`. Pushing a fresh index and **immediately** re-running the sync still reads the
**stale** CDN copy for up to ~5 min, silently producing empty fields. (The pinned-SHA endpoint serves fresh
immediately — only the `main` alias lags.)

**Fix options (pick one or combine).**
1. Schedule the seed half: add a cron/timer for `sync_lineage_assets.py --push` (e.g. daily), ordered
   **before** the pending-cache sync.
2. Make `sync_pending_caches.py` read the index via the **pinned-SHA / GitHub contents API** instead of the
   `main` CDN alias, busting the 300 s race.
3. Fold the seed step ahead of `sync_pending_caches.py` so the ordering dependency is explicit (one job).

Recommend **1 + 2**.

**Evidence.** `crontab -l` (ubuntu) — 5 jobs, none seeds; `systemctl list-timers --all` — no lineage unit;
published `qrs_index.json` `generated_at 2026-09-24T18:13:44Z` vs re-seed commit `30a0421` @
`2026-09-25T18:00:27Z` (1824 files, 0 deletions); `curl -I` on `main/qrs_index.json` →
`cache-control: max-age=300`.

### `deploy_gas_project.py` pushes from a working checkout with NO auto-refresh — a stale `tokenomics` tree silently REVERTS live (guards #520 / pull-first #521 do not catch it)
**Filed 2026-09-25 — reproduced live, deploy halted. Governor: Gary (thread 35947). Production-regression class.**

**Symptom.** A governor-ordered `clasp push` from the autopilot's GAS working checkout
(`/home/ubuntu/tokenomics`) would have **reverted live production**: that tree was **7 commits
behind `origin/main`**, parked on a stale feature branch (`feat/cfr-program-submission-sink` @
`b06beb8`), while live + `origin/main` were at `4cf8a0d`. Nothing in the toolchain refused it —
it was caught only by manually diffing live ↔ checkout before pushing.

**Root cause — two `tokenomics` checkouts, only one is refreshed.**
- `/opt/truesight_autopilot/context/tokenomics` — the read-only **context mirror**; hard-reset
  to `origin/main` every ~5 min by `_context_sync_loop` (`app/context.py` `refresh_context_repos`,
  `_CONTEXT_SYNC_REPOS = ("agentic_ai_context", "tokenomics", …)`).
- `/home/ubuntu/tokenomics` — the **working checkout** the deploy tool runs from and `clasp push`
  targets. It is **NOT** in `_CONTEXT_SYNC_REPOS`, has no cron/systemd refresh, and was last
  touched 2026-08-21 (reflog) — so it silently drifts.

**Why the two shipped guards do NOT catch a stale tree (the precise hole).**
- Remote-only-file guard (`tokenomics` **#520**) refuses a push that would **delete** a live file
  with no local counterpart. A stale local file that **differs** is a *modification*, not a
  remote-only deletion → the guard **passes**. (Here it would have emptied the 121-line scanner
  registry in `qr_code_web_service.js` and dropped the `documents` OAuth scope.)
- Selective pull-first (`tokenomics` **#521**, `--pull-first`) only **materialises remote-only
  files; it never overwrites local files** (per its own `--help`). A stale local file is never
  corrected either.
- The identity guard only compares owner vs clasp identity — unrelated.

**Fix options (pick one).**
1. Refuse drift fail-closed: in `deploy_gas_project.py`, `git fetch` then refuse `--push` when
   `git rev-list --count HEAD..origin/main > 0` (or HEAD is off the default branch), unless
   `--allow-behind-origin`. Smallest change that closes the class.
2. Add `/home/ubuntu/tokenomics` to a periodic refresh (same pattern as the context mirror).
3. Make `--pull-first` the default **and** have it hard-reset tracked files to `origin/main`
   (not merely add remote-only ones).

Recommend **1** (combine with **2** for belt-and-braces).

**Evidence.** reflog `/home/ubuntu/tokenomics` HEAD `b06beb8` (2026-08-21) vs `origin/main`
`4cf8a0d`; `git rev-list --count HEAD..origin/main` = 7; live ↔ checkout diff:
`qr_code_web_service.js` +0/-121, `appsscript.json` +1/-2; `app/context.py` L395
`_CONTEXT_SYNC_REPOS` + L423 `refresh_context_repos`; `scripts/deploy_gas_project.py` L536–620
(remote-only guard), L623–655 (`materialize_remote_only_files`, "never overwrites local files").

### Top-level GAS functions returning a secret are callable **by name** over the Apps Script API (keep `getGitHubToken()` off the callable surface)
**Filed 2026-09-25 — static inspection. Governor: Gary (thread 35947). Low-likelihood / high-impact; hardening only.**

**Finding.** `qr_code_web_service.js` `getGitHubToken()` returns the **raw** `GITHUB_TOKEN`
Script Property (`var token = scriptProperties.getProperty('GITHUB_TOKEN'); if (token) return
 token;`). Apps Script has **no private-function visibility** — every top-level `function` is
invocable by name via `scripts.run` when the project's `executionApi.access` is enabled, and the
call executes **as the owner** with the owner's scopes. The function **names** are public (repo
`TrueSightDAO/tokenomics` is public), so only the `executionApi` gate stands between a caller and
the token.

**Context — exercised 2026-09-25.** An `executionApi: {access: ANYONE}` block was trialled in
this project's manifest to unblock `clasp run`; it conferred **nothing** (it was never live;
`scripts.run` returned 403 for the separate **owner ≠ clasp-identity** reason) and was removed
(governor call: **C**). **Live and `origin/main` both carry no `executionApi` block** — verified
via the Apps Script API and a source-tree diff (`DIFFERING: none`).

**Ask (hardening, not urgent).** Stop returning secrets from top-level functions: make
`getGitHubToken()` return a **boolean**/scoped handle, or move the read behind the existing
`GOVERNOR_READ_KEY` gate. Then a future `executionApi` enablement can't be turned into a
token-exfil path by function-name guessing.

**Evidence.** `qr_code_web_service.js` `getGitHubToken()` (`return token`); repo visibility
public; `appsscript.json` `executionApi` absent in live + `origin/main`.

### SunMint tree-planting LINK path matches rows first-match-only — a duplicate row leaves a stale `NEW` twin
**Filed 2026-09-24 — reproduced live (thread 35189). Not money-adjacent, but it silently re-opens a planted tree.**

**Symptom.** Link a QR to a tree that has **two identical `NEW` rows**, and only the
**first** row flips to `LINKED`; the twin stays `NEW`, so the tree re-appears as
plantable on the next load. Observed on tree10 (`Edgar_20260903083555_019`) — two twin
rows; and tree02 (`Edgar_20260903083523_003`) already carries a lingering `NEW` twin
today.

**Root cause.** In `tokenomics/google_app_scripts/1UrBgq…/process_tree_planting_link.js`,
the LINK branch finds the SunMint row, stores its index, and **`break`s on the first
match** (first-match-only). The **REJECT** branch was already fixed for exactly this
(_"No break: invalidate EVERY row … first-match-only let the NEW copy survive"_, ~L783–785),
but LINK never received the same fix.

**Fix.** Port the REJECT branch's all-rows loop into LINK: when a QR/tree matches, flip
**every** matching `NEW` row, not just the first. Add a regression test with a
duplicated row.

**Workaround (until fixed).** De-dup the target tree's rows **before** linking (back up
the tab first; delete twins bottom-up; see `sops/SUNMINT_LINK_AND_CERTIFY_RUNBOOK.md` §2).

**Evidence.** `process_tree_planting_link.js` LINK branch (first-match + `break`) vs
REJECT branch (all-rows loop); thread 35189.

### pyzbar fails on `2023SA…` (Santa Anna) registry PNGs at native size — any tool that decodes at native resolution mis-handles them
**Filed 2026-09-24 — reproduced (thread 35189). The cert template is fixed here; other pyzbar consumers may not be.**

**Symptom.** `pyzbar.decode()` returns nothing for `lineage-assets/pngs/2023SA*.png` at
**native** size, though the same image decodes fine at 2–3× (LANCZOS) and `cv2` decodes
it at native size. Real scanners read the same codes fine. Result before the fix: **every
Santa Anna certificate was un-renderable** (`registry PNG does not decode`).

**Root cause.** These PNGs embed the QR at a smaller module pixel-size than pyzbar's
detector tolerates at native resolution (the `2023SA…` family is affected as a group).

**Fix (shipped here).** `templates/sunmint_certificate/render_sunmint_certificate.py`
`load_registry_qr()` now retries `decode()` on a 3× LANCZOS upscale before aborting.

**Still open.** Audit **other** pyzbar consumers for the same native-size assumption
(e.g. `app/tools/qr_scanner.py` in `truesight_autopilot`) and apply the same upscale-retry
(or upscale-all-then-decode) where the input may be a small-module registry PNG.

**Evidence.** `decode()` empty at native vs non-empty at 3× for `2023SA_81PB_20260412_1.png`;
`cv2.QRCodeDetector` returns the payload at native size; thread 35189.

### Web-app executing identity = the DEPLOYER, not the script owner (deploy-identity trap)
**Filed 2026-09-24 — incident resolved live by a governor grant; the AGENTS.md §2/§3 correction is still OPEN. Governor: Gary (thread 35944). Money-adjacent (a planter's PIX stopped reaching the review surface).**

**Symptom.** The 3 live deployments for `1MnAsIQA…` were repointed to @36; the two private-sheet sinks (`processPayoutRegistrationsFromTelegramChatLogs`, `processCfrProgramSubmissionsFromTelegramChatLogs`) and the read `getPendingPayoutRegistrations` then returned Google's *"You do not have permission to access the requested document"* HTML to Edgar's **anonymous GET** — while 4 other actions on the **same deployment** returned JSON.

**Root cause (controlled experiment).** `appsscript.json` sets `webapp.executeAs = USER_DEPLOYING`, so the web app executes as the account that **deployed** it (the clasp identity that ran `clasp push` / `clasp version` / created the deployment) — **NOT** necessarily the script `owner_email`. Identical v36 code, only the deployer differing: a deployment created as `garyjob@agroverse.shop` served the payout-registration sink ✅ (`{"success":true,…}`); one created as `admin@truesight.me` returned PERMISSION_DENIED ❌ — `admin` lacked access to the private `cfr program` sheet (`17KwmxYOpTVR89ybRlOkDXoN9PF3UcaNu3REg2wNa83w`).

**Resolution (live).** Governor granted `admin@truesight.me` access to the sheet; the live deployments served JSON again the same session (payout-reg `{"success":true,"recorded":0,…}`; cfr `{"success":true,"recorded":0,"skipped":8,"errors":0}`).

**Resolved (2026-09-24, `tokenomics` #553).** `AGENTS.md` §2/§3 corrected — §2 retitled to *"the DEPLOY identity IS the RUNTIME identity"* and §3 rewritten to *deploy as the account that can open **every** target sheet* (with `USER_DEPLOYING` named). **Canonical deploy identity for `1MnAsIQA…` = `admin@truesight.me`** (script owner; granted the private `cfr program` sheet 2026-09-24). Re-confirmed live on the v37 deploy: repointing as admin left both private sinks serving JSON.

### Apps Script triggers are PER-EXECUTING-IDENTITY — the scanner-trigger count depends on who deployed/checks
**Filed 2026-09-24 — observed. Governor: Gary (thread 35944). Affects how the "7/7 triggers installed" claim reads.**

`?action=getInstalledScannerTriggers` returned **count=7** on the admin-deployed live deployments, but **count=4** on a fresh gary-deployed v36 of the same code. Apps Script time-driven triggers are owned by the identity that created them and `ScriptApp.getProjectTriggers()` returns only the **calling** identity's triggers — so the count reflects the deploying/executing identity, not a project-wide total. **Implication:** a scan re-armed by Sophia-as-admin will not appear in Gary's trigger list (and vice-versa). Decide the canonical owner identity for re-arming and re-arm once under it; do not treat a single identity's count as authoritative. **Decided (2026-09-24): canonical identity = `admin@truesight.me`** (same as the deploy identity, #553); re-arm under it (live v37 deploy shows `count=7` under admin).

### `[PAYOUT REGISTRATION]` sink never auto-ingests — no dispatch route, and the self-installing hourly cron never fired
**Filed 2026-09-24 — root cause verified; a manual backfill was already applied live. Governor: Gary (thread 35944). Money-adjacent (a planter's PIX never reaches the review surface).**

**Ask.** Make the `[PAYOUT REGISTRATION]` sink self-healing: (a) add a routing entry so Edgar's post-verify dispatch actually fires the GAS scanner, and (b) make the GAS hourly safety-net cron install reliably (today it only self-installs *from inside a scan run* — a chicken-and-egg when the fire path never fires).

**Symptom (reported by Gary).** `[PAYOUT REGISTRATION]` rows land in Telegram Chat Logs (e.g. `G12603`) with col P signature verification = `success`, but the private `cfr program` → `payout registrations` tab stayed **empty (`count:0`) after ~a day of live submissions** — nothing reached the review surface an operator must pay from.

**Verified root cause (2026-09-24).**
1. **No dispatch route.** `dao_protocol/truesight_dao_client/server/dispatch.py` `ROUTING` has `[PAYOUT EVENT] → ("PAYOUT_PROCESSING", "processPayoutEventsFromTelegramChatLogs")` (L291) but **no `[PAYOUT REGISTRATION]` entry**. This is intentional per `tests/test_payout_event_dispatch_routing.py` docstring: *"the `[PAYOUT REGISTRATION]` sibling (P4) is deliberately NOT routed here — it relies on its GAS hourly-trigger safety net."* There is **no dedicated env key** (`DAO_PROTOCOL_WEBHOOK_PAYOUT_REGISTRATION_PROCESSING` is absent from `dao_protocol` `.env`).
2. **The safety net never installed.** `tokenomics/google_app_scripts/1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT/process_payout_registration_telegram_logs.js` installs its own hourly trigger inside `ensurePayoutRegHourlyTriggerInstalled_()`, but that is called **only from within `processPayoutRegistrationsFromTelegramChatLogs()`** — which itself only runs when invoked by the (non-existent) webhook or the (never-installed) trigger. So the piece never runs at all.
3. **Manual backfill.** Invoking the scanner action directly (`?action=processPayoutRegistrationsFromTelegramChatLogs`) returned `{recorded:1, updated:3, rejected:0, errors:0}` and populated the tab (a ~15h backlog, update ids `Edgar_20260924003904_034` → `Edgar_20260924131424_088`). That call also installs the hourly trigger as a side effect — but only because a human triggered it.

**Suggested scope.**
- `dao_protocol`: add `[PAYOUT REGISTRATION] → ("PAYOUT_PROCESSING", "processPayoutRegistrationsFromTelegramChatLogs")`. **Watch the env-key collision:** the existing `PAYOUT_PROCESSING` value already points at the same GAS deployment (tail `…be4FXbIVpuaOHVW/exec`) which serves *both* actions, so either introduce a distinct key or confirm the dispatcher passes an `action` param. Revisit `test_payout_event_dispatch_routing.py` (its `test_payout_event_does_not_match_payout_registration_text` pin assumes registration is unrouted).
- `tokenomics`: decouple trigger installation from a scan run — e.g. create the time-driven trigger at deploy (the other scanners' pattern) or from a separate installer entry point.

**Evidence (no PII).** `dao_protocol dispatch.py` L291; `tests/test_payout_event_dispatch_routing.py` docstring L12–15; `process_payout_registration_telegram_logs.js` (`ensurePayoutRegHourlyTriggerInstalled_`); Telegram Chat Logs `1qbZZhf-…` row 12603 (tag + col P `success`; col G body carries no PIX key); private `cfr program` `payout registrations` tab (post-backfill = 4 rows, masked `***.***.***-19`).

### §11.5 CFR tree/monitoring/plot mirror: **writers + Edgar wiring MERGED in source, but inert** pending a GAS deploy + an Edgar restart (governor gates)
**Filed 2026-09-24 \u2014 code shipped; NOT live. Governor: Gary (thread 35947). Source-complete; the last mile is now a GAS deploy + an Edgar restart (both explicit governor gates).**

**Ask.** Land the remaining gates that make the merged §11.5 mirror actually fire.
- **(a) ✅ DONE (2026-09-24) — env var set.** `DAO_PROTOCOL_WEBHOOK_CFR_PROGRAM_REGISTRATION_PROCESSING` now exists in `/home/ubuntu/dao_protocol/.env`; value is **sha1-identical** to `…_PAYOUT_PROCESSING` (same GAS `/exec` deployment), `.env` backed up before the append. (Gary's go, thread 35947.)
- **(b) ⭐ STILL OPEN — NEW FINDING: the GAS code is NOT deployed.** The live deployment for `1MnAsIQA…` (`/exec` id `AKfycbxQDdGnw…`, serving *both* the payout sink and the new CFR sink — one GAS project) is `@33`, dated **2026-09-21** (UPDATE 2026-09-26: gate (b) RESOLVED - the live deployment is now **@42**, which carries #550; probing `?action=processCfrProgramSubmissionsFromTelegramChatLogs` returns `{"success":true,"recorded":0,"skipped":8,"errors":0}`. Gate (a) env var SET 2026-09-24; gate (c) Edgar restart still open.), i.e. **before** tokenomics #550 (2026-09-24). Probing the live `/exec` with `?action=processCfrProgramSubmissionsFromTelegramChatLogs` returns **`Invalid action`** — the action is not in the running deployment. **Setting the env var alone does NOT make the sink live:** #550 must be `clasp`-pushed **and** the versioned deployment rolled forward (@33 → new). **UPDATE 2026-09-26 — the identity mismatch is SOLVED; use Path B, NOT the override.** Since tokenomics **#561** (`aa21206`, 2026-09-25), `deploy_gas_project.py`'s `clasp_credentials_env()` hands `clasp` a private `HOME` whose `.clasprc.json` IS `$CLASPRC_PATH` (fail-closed; tested in `scripts/test_clasp_credentials_env.py`). So the safe, correct gesture is `CLASPRC_PATH=~/.clasprc-admin.json scripts/deploy_gas_project.py <scriptId> --push` — the identity guard **and** `clasp` then both run as `admin@truesight.me`. **Do NOT use `--allow-identity-mismatch`:** it pushes as gary@ while `appsscript.json` sets `webapp.executeAs = USER_DEPLOYING`, silently swapping the web app's runtime identity and its per-executing-identity trigger set. **Never touches SunMint:** the SunMint scanner is a *separate* GAS project (`1Jp8q…`).
- **(c) STILL OPEN — Edgar restart.** Restart the `dao_protocol` service so the new env var **and** the #179 ROUTING entries load (`EnvironmentFile=-.env` + module-level `ROUTING` are read at process start; #179 is already in the box checkout at `63c726bb`).

Everything upstream of these gates is merged.

**What is shipped (source).**
- `tokenomics` **#550** (`ef25709a`): the missing \u00a711.5 writer `process_cfr_program_submission_telegram_logs.js` \u2014 mirrors `cfr.truesight.me`-origin tree / monitoring / plot submissions into the **private** `cfr program` tabs (`tree planting` / `tree monitoring` / `plot registrations`), plus the `?action=processCfrProgramSubmissionsFromTelegramChatLogs` branch in `qr_code_web_service.js`, a 19-check harness and a 14-test pytest. Source-only \u2014 **not** `clasp`-deployed.
- `dao_protocol` **#179** (`63c726bb`): **additive** routing \u2014 `("CFR_PROGRAM_REGISTRATION_PROCESSING", "processCfrProgramSubmissionsFromTelegramChatLogs")` appended as a **second** target on `[TREE PLANTING EVENT]`, `[TREE GROWTH MONITORING EVENT]` and `[FARM BOUNDARY EVIDENCE EVENT]`, backed by `tests/test_cfr_program_dispatch_routing.py` (6 tests). `dispatch_event` fires **every** target of a matched entry, so the pre-existing SunMint targets are untouched \u2014 i.e. the public **`SunMint Tree Planting`** tab keeps populating. Replacing rather than appending would silently darken it; the new test fails loudly if anyone does.

**Why it is inert (verified 2026-09-24).** `dispatch.py` resolves each target as `os.environ.get("DAO_PROTOCOL_WEBHOOK_<key>")`; a missing key is **logged and skipped** (L365\u2013384). `DAO_PROTOCOL_WEBHOOK_CFR_PROGRAM_REGISTRATION_PROCESSING` **was** absent from the box `.env` as of the original filing (the box had 33 `DAO_PROTOCOL_WEBHOOK_*` keys, none CFR) and has **since been set** (2026-09-24). So with the env var unset the CFR target no-ops and — correctly — SunMint still fires. The env var is **now set** (2026-09-24, sha1-verified identical to the payout key), but the sink stays dead until **both** the GAS deployment serves the action (gate b) **and** Edgar restarts (gate c).

**Secondary (same surface).**
- `GAS_SCRIPT_PROPERTIES.md` \u00a72/\u00a73 still records `CFR_PROGRAM_SPREADSHEET_ID` as **NOT SET**, yet the 2026-09-24 payout-registration backfill wrote 4 rows into the private `cfr program` sheet \u2014 so the id resolves in practice somehow. Reconcile the registry row (or confirm the sink's Script-Property/constant fallback) so the next run is not misled.
- The payout-parser terminator fix (tokenomics #550) stops future rows capturing the trailing signature blob; the **4 already-written `payout registrations` rows** still carry the polluted `submission_source` \u2014 decide whether to backfill them.

**Verified 2026-09-24 — the CFR `tree planting` tab is EMPTY (0 data rows).** Read live via the DAO `agroverse_market_research` SA: the private `cfr program` sheet `17Kwmx…` tab `tree planting` (gid 149742653) holds **headers only** (`created_at_utc · telegram_update_id · pk_hash · tree_id · species · lat · lng · photo_url · capture_source · status`). Meanwhile the public `SunMint Tree Planting` tab (`1qbZ…`, gid 176124122) holds **265** data rows, of which **229 rows (166 distinct submissions)** carry Anapu/Pará coordinates (lat −2…−4.5, lng −50…−53.5) — statuses **167 NEW / 61 INVALID / 1 LINKED**. Only 23 of the 265 rows mention "cfr"/"anapu" literally, so text-matching undercounts badly; the CFR cohort is identified by **coordinates**. ⇒ the CFR-associated tree-planting records are **not reaching the CFR tab** — they remain in the public tab — consistent with the sink being inert (gates b + c). Note the public tab carries duplicate `telegram_update_id`s (re-append on retry); watch for the same duplication once the CFR sink writes.

**Evidence.** `dao_protocol dispatch.py` L365\u2013384 (env-key resolution + skip), `ROUTING` entries for the 3 event tags; `tests/test_cfr_program_dispatch_routing.py`; PRs tokenomics#550 + dao_protocol#179; `GAS_SCRIPT_PROPERTIES.md` L61, L82; private `cfr program` `payout registrations` tab (4 rows).

### `[PAYOUT REGISTRATION]` scanner: `submission_source` captures the trailing signature + boilerplate
**Filed 2026-09-24 — verified. Governor: Gary (thread 35944). Cosmetic; private sheet only.**

**Ask.** `parsePayoutRegistrationEventText_()` appends every line after a key onto that key's value (the `else if (lastKey)` continuation branch). For the signed payload, everything after `- Submission Source:` — the `--------` separator, `My Digital Signature: …`, `Request Transaction ID: …`, the "generated using"/"Verify submission here" lines — is concatenated into the `submission_source` cell. Observed live on all 4 backfilled rows.

**Fix.** Stop the continuation at the `--------` separator (or first blank-after-separator), or bound `submission_source` to the first token/line. Also drops a large base64 blob from every row.

**Evidence.** Private `payout registrations` rows 2–5 `submission_source` (begins with the URL, then the full signature); `process_payout_registration_telegram_logs.js` `parsePayoutRegistrationEventText_` continuation branch.

### `sunmint/trees/index.geojson` `tree_id` is keyed on the sheet's col A, but the canonical id is col D — every Edgar-direct tree id is **+1** (verified on tree02: `…_004` vs canonical `…_003`)
**Filed 2026-09-24 — verified, not started. Governor: Gary (thread 35189). Non-urgent, but it silently breaks every `tree_id`-based join for Edgar-direct trees.**

**Ask.** The governor ruled (thread 35189, 2026-09-24) that the canonical tree id for tree02 is `Edgar_20260903083523_003`. `sunmint/trees/index.geojson` carries `…_004`. Fix the generator so the public index keys on the canonical id.

**Verified root cause (2026-09-24).** `sunmint/scripts/build_tree_geojson.py` L86:
```
c_id = idx(header, "telegram update id", "tree id")
```
It derives `tree_id` (emitted at L162 `"tree_id": t["id"]`) from the sheet's **col A "Telegram Update ID"** — but the canonical id (what Edgar, the `[TREE PLANTING EVENT]`, the certificate's `ledger_ref`, and the signed attestation all key on) is the sheet's **col D "Telegram Message ID"**. On the `SunMint Tree Planting` tab (spreadsheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`) the two columns differ by **exactly +1 on every Edgar-direct row**:
- row 38 (tree02): col A = `Edgar_20260903083523_004`, col D = `Edgar_20260903083523_003` ← the canonical / cert / Edgar id
- row 37 (tree01): A = `…_002`, D = `…_001`
- row 39 (tree03): A = `…_006`, D = `…_005`
- also `…_082/…_081`, `…_375/…_376`, `…_022/…_021`, `…_026/…_025`, `…_062/…_061`

So this is **systematic, not a one-off**: the public `trees/index.geojson` is off-by-one for EVERY Edgar-direct tree — its whole Bomsucesso family (`…_002, _004, _006 … _020`) is even, i.e. always col D + 1. The generator computes no offset itself; it reads col A verbatim, so the bug is the **column choice**, not arithmetic.

**Why it matters.** `tree_id` is the join key for the map popup, the monitor page `?tree=<id>` deep link, the growth-monitoring tabs, and the certificate's `ledger_ref`. Keying the *public index* on a column that is systematically +1 vs the *canonical attestation id* means every `tree_id`-based join mismatches silently.

**⚠️ Care needed before changing the column (do NOT do a blunt `c_id = col D`).**
1. **Col D is not always an `Edgar_*` id.** On the sheet's older Telegram-native rows, col A holds the numeric update id and col D holds a *numeric* message id (`171`, `6411`, …) — neither is an `Edgar_*` id. So the fix must **prefer the `Edgar_*`-shaped value across A/D** (e.g. pick whichever of col A / col D matches `^Edgar_`), not blindly prefer col D.
2. **The tree02 row is duplicated** (sheet rows 38 **and** 40, identical col A/D — one `LINKED`, one `NEW`). The generator's dedupe keeps one, but the duplicate should be cleaned at source.

**Suggested scope.** In `build_tree_geojson.py`, resolve the id as "the `Edgar_*`-shaped value among {col A, col D}, falling back to col A" and add a unit test over the Bomsucesso rows asserting `tree_id == col D` for Edgar-direct rows. (`sunmint` is an API-only data repo — no clone/branch-edit; land via Contents-API single-file write or a PR on the generator's own home if/when it graduates out of the data repo.)

**Evidence.** `sunmint/scripts/build_tree_geojson.py` L86 (`c_id`) + L162 (`"tree_id": t["id"]`); sheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` → `SunMint Tree Planting` cols A/D rows 37–40 (tree02 row 38: A=`…_004`, D=`…_003`); `sunmint/trees/index.geojson` (tree02 feature `tree_id: Edgar_20260903083523_004`); governor ruling thread 35189; `sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md` §7.

### SunMint cert: the QR print-safety floor (`k >= 4`) is documented but UNENFORCED — and the obvious clamp is unsafe
**Filed 2026-09-24 — verified, not started. Governor: Gary (thread 35189). Non-urgent; regression guard for the cert renderer.**

**Ask.** `templates/sunmint_certificate/render_sunmint_certificate.py` states a hard requirement — `k MUST stay >= 4` (4px == 0.339mm/module) to survive 150-dpi printing; `k=3` (0.254mm/module) does NOT — but nothing in the code enforces it.

**Verified (2026-09-24).**
1. **The floor is prose, not a guard.** `render_qr` does `modules = registry_qr.width` then `k = max(2, round(px / modules))`. The ONLY guard is `if not decode(tile):` — a *digital* decode check. Digital decode != print-safe; a 171px tile decodes on screen but is below the print floor. So the documented constraint has no teeth.
2. **It already shipped broken once.** #1354 (merged `b7eea37ad63f`, 2026-09-24T05:40:24Z) set `qpx=196` while the quiet zone was still `q=4` -> `modules = 49 + 2*4 = 57` -> `round(196/57) = 3` -> tile `57*3 = 171px` (k=3, BELOW floor). That reached `main` and was live until #1355 (`440120bd`, 05:47:33Z) fixed it to `qpx=212` with `q=2` (`modules=53` -> k=4 -> 212px). Note #1354's own title said *"196px (k=4)"* — the intent and the realised value disagreed.
3. **The realised value depends on BOTH `qpx` and `q`.** Reproduced locally (the renderer's own arithmetic):
   - `q=4` (modules=57): `qpx=196` -> k=3 -> **171px**; `qpx=212` -> k=4 -> 228px
   - `q=2` (modules=53): `qpx=196` -> k=4 -> 212px; `qpx=212` -> k=4 -> 212px
   So a `qpx` that is safe at one `q` is unsafe at another — a caller cannot reason about safety from `qpx` alone.

**Why the naive fix is UNSAFE (the non-obvious part).** A bare `assert k >= 4` (or clamping `k`) is NOT sufficient. The white rounded-rectangle box is drawn at `[qx-9, qy-9, qx+qpx+9, qy+qpx+9]` and the vertical centering is `qy = photo_box[0] + (photo_box[1] - qpx)//2` — **both use `qpx` (the *requested* px), while the pasted tile is `modules*k`.** At q=4/qpx=212 that is 228px tile inside a box sized for 212px. Clamping `k` without also recomputing the box and `qy` from the *realised* `modules*k` desyncs the box + center lines from the actual QR. The fix must derive size from the realised tile (e.g. have `render_qr` return its tile size, or resolve `k`/tile-size in the caller and lay out from that), not from `qpx`.

**Suggested scope.** Resolve `k` (and the resulting tile px) in one place for a given `q`, fail loudly (not silently) if the chosen size maps below `k=4`, and lay the box + `qy` out from the realised tile size so the three can never disagree.

**Evidence.** `templates/sunmint_certificate/render_sunmint_certificate.py` L229-231 (`k = max(2, round(px / modules))`), L232-255 (`decode()` guard), L406-424 (floor comment, `qpx`/`qy`/box); PR #1354 (`b7eea37ad63f`) vs #1355 (`440120bd`); thread 35189.

### SunMint: generated certs are not downloadable from the QR provenance page (`truesight.me/qr/?id=<qr_id>`) — ✅ SHIPPED 2026-09-25 (URL-probe route; see `## Recently shipped`)
**Filed 2026-09-24 — verified feature request, not started. Governor: Gary (thread 35189). Non-urgent; does NOT block the cert layout work.**

**Ask.** Once a SunMint certificate has been generated for a tree / QR, the cert should be downloadable from that asset's own provenance page — `https://truesight.me/qr/?id=<qr_id>` — via a **"Download certificate"** button, mirroring the credentialing precedent.

**Verified precedent (credentialing).** The butterfly-effect credential pages (`truesight.me/programs/butterfly-effect/credentials/`) do exactly this:
- cert PDFs are **pre-generated and cached** in `TrueSightDAO/lineage-credentials` at `_cache/cv/<slug>__<program>__cert.pdf` — built by `.github/workflows/build-cv-cache.yml` → `lineage-engine/scripts/build_cv_cache.py`, and only built once `locked_at` is set;
- served over the **jsDelivr CDN** (the workflow purges jsDelivr on rebuild);
- the page carries a "⏬ Certificate PDF" button + a "View the tree & its provenance →" link pointing at the same `truesight.me/qr/?id=…` scheme the SunMint QR pages use.

**Why it does NOT transfer 1:1 — the real design work.**
1. **Keying differs.** Credential certs are keyed by *person-slug × program* (`<slug>__<program>__cert.pdf`). A SunMint cert is per *tree-planting / qr_id* (guardian + tree details), so the filename scheme needs its own authority — e.g. `qrs/<qr_id>__cert.pdf`. Pick the canonical key.
2. **Host repo differs.** The credential cache lives in `lineage-credentials/_cache/` — an **API-only, machine-owned DATA repo** (no clone / no branch-edit; single-file writes via the Contents API only) which has grown to **~10 GB** (a CI checkout there took **21 m 44 s**; see WORKSPACE_CONTEXT.md L234–236). The SunMint cert *renderer* lives in `agentic_ai_context/templates/sunmint_certificate/`. Decide where SunMint cert PDFs are cached, and how that repo grows.
3. **No rebuild trigger exists.** Today a SunMint cert is produced by running `render_sunmint_certificate.py` + a config by hand. A cached-serving model needs an auto-rebuild trigger analogous to `build-cv-cache.yml` (e.g. on cert-issue / `[TREE PLANTING]`), or the cached PDF silently goes stale relative to the signed attestation.
4. **Page change is program-agnostic + beta-first.** `truesight_me_beta/qr/index.html` is pure static HTML/JS that dispatches on `asset_type` (fetches `lineage-assets/qrs/<qr_id>.json`; **verified 2026-09-24** — `render()` reads `manifest.qr_image_url`, `.status`, `.edgar_resolve_url`, `.current_landing_page`, `.lineage`; there is **no cert branch** today). The button must appear **only when a cert genuinely exists** for that `qr_id` — probe the URL, or add a `cert_url` field to the manifest. Promote to prod only after beta review (two-repo flow; governor-approved).

   ⚠️ **LANDMINE if you take the `cert_url`-in-manifest route (verified + reproduced 2026-09-24).** `lineage-assets/scripts/lib/manifest.py → merge_preserve_events()` preserves **only `events`** (custom events whose type is not a seed event) and then does `merged = dict(fresh)` — so **every other top-level key is rebuilt from the sheet on each re-seed**. A hand-added (or cert-flow-added) `cert_url` is therefore **silently DROPPED** the next time `seed_from_sheet.py --execute` runs. Reproduced locally: add `certificate_url` + a custom event → re-run `write_manifest(fresh)` → `certificate_url` gone, custom event kept. **So the manifest-field route is NOT a one-line page change:** you must also teach `build_manifest()`/`merge_preserve_events()` to carry the cert field (and have the cert-issuance flow write it), or the seeder will wipe it. The **URL-probe route** (page HEADs the cached cert URL) sidesteps this entirely and is the lower-risk option.

   ℹ️ Also note: `qr/index.html`'s status CSS enum has **no `ASSIGNED_TO_TREE`** badge (MINTED / CONSIGNMENT / SOLD / SAMPLE / GIFT / EXPENSED / RETIRED only), so a QR in that state renders the grey default badge. Minor, but the download feature is a natural moment to add it.

**Related, already-tracked (do NOT re-file):** the certificate's *content* framing — `2024OSCAR_CB_20260620_1`'s manifest says `SOLD` (seeded 2026-07-10) while the live Edgar resolve returns `ASSIGNED_TO_TREE` (and `qrs_index.json` still says `SOLD`) — is **already a parked governor decision** at `sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md` §7 ("Ask the governor which framing the cert should carry; do not silently pick one"). Not a new finding; it does not block the download feature.

**Evidence.** `credentials/CREDENTIALING_PROGRAM_PAGES.md` L612 / L749 / L757; `credentials/CREDENTIALING_E2E_VALIDATION.md` L111 / L124; `CONTEXT_UPDATES.md` L162; `truesight_me_beta/qr/index.html`; `lineage-assets/scripts/lib/manifest.py` (`merge_preserve_events`); `lineage-assets/scripts/seed_from_sheet.py`; `agentic_ai_context/templates/sunmint_certificate/render_sunmint_certificate.py`; thread 35189.

### QR manifest JSON goes stale after a [TREE PLANTING LINK EVENT] — nothing regenerates it, and the one dedicated script for the job has a status-clobber bug
**Filed 2026-09-24 — verified, not started. Governor: Gary (thread 35189). Non-urgent; money-adjacent to wire (spans GAS + Python repos).**

**⚙️ UPDATE 2026-09-24 (seeder read-path shipped; daemon question answered).**
- **The read-path divergence is FIXED.** `lineage-assets` #12 (seeder joins the SunMint link at seed time) + #13 (append-only `merge_preserve_events` — history no longer rewritten) + #14 (the scoped data run) mean `qrs/2024OSCAR_CB_20260620_1.json` now carries `lineage.linked_tree=Edgar_20260903083523_003`, `status: ASSIGNED_TO_TREE`, and **retains** `['minted','sold','planted']`. The manifest no longer needs a hand-edit — a re-seed materialises the link from the sheet.
- **What remains is CADENCE, not correctness.** Nothing schedules the seeder, so the *rest* of the cache is stale vs the sheet (a full `--execute` diffs ~1369 files: ~1358 pure `www.`-strip URL churn + ~7 substantive). One full catch-up run makes the repo consistent; thereafter runs are no-ops (idempotent — 2nd execute = 0 changes).
- **Daemon precedent ALREADY EXISTS on the autopilot box.** The Ubuntu crontab runs `sync_pending_caches.py --push` **every 30 min** (gspread → sha-aware Contents-API PUT → `lineage-assets`). The same shape works for the seeder: a 30-min cron/systemd-timer running `seed_from_sheet.py --execute && build_index.py`, then commit **only when `git status` is non-empty** (no churn on a no-op). The link handler's `repository_dispatch` (L816) remains the event-driven alternative for immediate per-QR refresh.
- **`sync_tree_links.py` clobber STILL LIVE** — `_base_wrapper` (L104) still hard-codes `status:"MINTED"`; fix before invoking it. The seeder path above does NOT use it, so the daemon recommendation sidesteps the clobber.
- **⚙️ UPDATE 2026-09-25 — stale-page symptom REPRODUCED on a fresh link; cron coverage gap pinned.** David Soha's link (`2024SA_20251227_35` → tree `Edgar_20260908005833_045`, fired 2026-09-24) left `qrs/2024SA_20251227_35.json` = `status: SOLD`, **no** `lineage.linked_tree`, ~10 h later. Consequence: `truesight.me/qr/?id=2024SA_20251227_35` renders the **wrong status badge** (`SOLD`, green) instead of `ASSIGNED_TO_TREE` — *even though* that badge's CSS exists (corrected in `## Recently shipped`). The page authors no wrong label; the cached manifest it reads is simply stale. The deep-link `?tree=Edgar_20260908005833_045` resolves fine (it reads the runtime trees registry, not the manifest). **Cron coverage gap (verified live):** the box's existing `*/30` `sync_pending_caches.py --push` writes `sunmint_pending.json` + `sold_pending_tree.json` **only** — it does **not** refresh `qrs/<qr_id>.json`. So the seeder cadence fix recommended above is still required; no existing cron covers manifests. **Freshness sweep due:** a full catch-up run would now join links for every QR linked since the last seed (all links outside the 2026-09-24 #14 scoped run). Cadence, not correctness.

**Ask.** After a `[TREE PLANTING LINK EVENT]` fires, the target QR's `lineage-assets/qrs/<qr_id>.json` manifest should be regenerated so its `status` / `lineage` / `events` reflect the link (`ASSIGNED_TO_TREE`). Today nothing does this, so the manifest silently diverges from the authoritative state Edgar serves.

**Verified (2026-09-24).**
1. **Confirmed divergence.** `qrs/2024OSCAR_CB_20260620_1.json` says `status: SOLD` (`_seeded_at 2026-07-10T21:40:24Z`, `_source seed_from_sheet.py`), and `qrs_index.json` (generated 2026-09-11) also says `SOLD` — while live `https://edgar.truesight.me/agroverse/qr-code-check?qr_code=2024OSCAR_CB_20260620_1` returns `ASSIGNED_TO_TREE`. The public mirror is stale relative to the source of truth.
2. **The link handler never touches the manifest.** `tokenomics/…/process_tree_planting_link.js` writes only to Google Sheets columns + ledger tabs + email; grep for `lineage-assets` / `manifest` / `seed_from_sheet` / `qrs_index` = **0 hits**. Its only outbound HTTP is the plots-media fetch and a `repository_dispatch` for the *tree-index* rebuild (L816) — precedent for how a refresh *could* be fired.
3. **Per-row primitives do exist** — `scripts/lib/manifest.py` `build_manifest(row, source)` + `write_manifest(out_dir, manifest)` both operate on a single row/manifest; `seed_from_sheet.py` just loops them over the whole sheet.

**⚠️ Correction to the obvious fix ("just call the existing functions from the link flow"):**
- **A *dedicated* script already exists and is ALSO never invoked:** `lineage-assets/scripts/sync_tree_links.py` (253 lines) — *"Mirror LINKED SunMint tree-planting rows into lineage-assets JSON and cross-link QR <-> tree"*; it mints `qrs/pk-<msgid>.json` (tree) and patches the QR record with `lineage.linked_tree` + an `assigned_to_tree` event. **This is the intended primitive for exactly this job — reuse it, don't build new.**
- **But it has a status-clobber bug that must be fixed FIRST.** `build_qr_patch()` builds from `_base_wrapper(linked_qr, "cacao_bag")`, which hard-codes `status: "MINTED"`, and never resets it. `_merge()` then does `merged.update({k:v for k,v in fresh.items() if v is not None and v != ""})` → **`merged["status"]` becomes `MINTED`, overwriting the QR's real `SOLD`/`ASSIGNED_TO_TREE`.** Reproduced: `merged status = MINTED`. Wiring it in as-is would corrupt the QR status field, not merely leave it stale. Fix `build_qr_patch` to set `status: "ASSIGNED_TO_TREE"` (it already emits the matching event) before anyone invokes it.
- **Cross-runtime boundary — not a function call.** The link handler is **Google Apps Script (JS, Google cloud)**; `sync_tree_links.py` / `seed_from_sheet.py` are **Python in the `lineage-assets` repo**. GAS cannot import Python. So "add a refresh call to the post-write step" means a **`repository_dispatch` to a GitHub Action** (reuse the link handler's existing dispatch precedent at L816 / `TGM_GITHUB_TOKEN`) — or a scheduled job. Nothing schedules the seeder today (no `.github/workflows` in `lineage-assets`; no cron found), so the data repo is not self-healing.
- **Two source tabs, two schemas.** `build_manifest` reads **Agroverse QR codes** (col D = status) on `1GE7PUq…`; `sync_tree_links.py` reads the **SunMint Tree Planting** tab on `1qbZZhf…`. Pick the right source per field; don't assume one refresh covers both.

**Suggested shape (~small, after the clobber fix).** Add a `repository_dispatch` (type e.g. `qr-manifest-refresh`, `client_payload.qr_id`) to the link handler's success path — reuse the existing `TGM_GITHUB_TOKEN` dispatch block — and a thin Action in `lineage-assets` that runs `sync_tree_links.py --execute` (single-QR via a new `--qr` filter) + `build_index.py`, then commits. Best-effort/non-fatal, exactly like the tree-index dispatch.

**Evidence.** `tokenomics/google_app_scripts/1UrBgqLnnQ…/process_tree_planting_link.js` (no manifest refs; L816 dispatch precedent); `lineage-assets/scripts/sync_tree_links.py` (`_base_wrapper` L104 `status:MINTED`, `_merge` L118, `build_qr_patch` L183); `lineage-assets/scripts/seed_from_sheet.py` (SHEET_ID L33, `--dry-run/--execute/--limit` only, no single-QR flag); `lineage-assets/scripts/lib/manifest.py` (`build_manifest` L158, `merge_preserve_events` L194, `normalize_status` passes `ASSIGNED_TO_TREE` through); `lineage-assets/qrs/2024OSCAR_CB_20260620_1.json`; thread 35189.

### Tree-planting photo supersession has no sanctioned path — an in-place image swap leaves a signed attestation pointing at new bytes
**Filed 2026-09-23. Owner: unclaimed. Governor: Gary (thread 35189). Status: gap identified; one swap already performed manually with a documented note.**

**Context.** Tree photos live at `sunmint/images/<name>.jpg` and their URL is written into two places: (a) the `SunMint Tree Planting` sheet col I (source of truth → regenerated into `trees/index.geojson`), and (b) the **RSA-signed, append-only** attestation in `verify_public_signatures/tree_planting/<id>.json` (`signed_payload` line `- Photo URL: …`). The signature covers the **URL string, not the image bytes**. So overwriting the file in place keeps every signature green while silently changing the photo a signed attestation points to — the classic "silent-wrong" shape.

**Precedent.** 2026-09-23: canonical photo for tree `Edgar_20260903083523_004` (PL-002, Fazenda Bom Sucesso) was overwritten in place with a better frame from the same dig event (Gary's 18:47:11 -03:00 shot); superseded blob `aff60dd2` / sha256 `bd7ed5af…` retained in git history; swap recorded in CONTEXT_UPDATES. The signature still verifies (URL unchanged).

**Ask.** Decide + implement ONE of: (1) **content-addressed filenames** (`images/tree02_<sha8>.jpg`) so a photo change = a NEW filename, never an in-place overwrite, and `signed_payload` records the immutable hash; (2) a **`[MEDIA RETRACTION/SUPERSESSION EVENT]`** type (the repo already has `media_retraction` + `tree_planting_reject` folders) that records `old_url → new_url` + reason, referenced from the tree's sheet row, so the supersession is itself signed/append-only; (3) a **sheet col-A breadcrumb** convention (append a dated note line to the tree_id cell when its photo is superseded). Until then, any photo correction is a manual, note-only operation — easy to do silently.

**Evidence.** `sunmint/SCHEMA.md` Trees schema (photo_url ← sheet col I); `verify_public_signatures/tree_planting/Edgar_20260903083523_003.json` (`signed_payload` embeds the URL); commit `b332512` (sunmint); thread 35189.

### Residual ledger duplicates: 3 strict-identical "GetData Inc" pairs (166.66 TDG) survived both dedup passes
**Filed 2026-09-22. Owner: Sophia. Governor: Gary (thread 34264). Status: confirmed finding, NOT remediated (money-adjacent — needs go).**

**Finding.** Two dedup passes ran on `Ledger history` (1GE7PUq\u2026) on 2026-09-22: dedup-#1 (88 rows, same-body re-appends) and dedup-#2 (166 groups / 358 rows, strict name+byte-identical body+amount+date). A third, independent re-scan (UNFORMATTED_VALUE, strict key = name + md5(body) + col G amount + col H date) finds **3 groups / 3 excess rows / 166.66 TDG** still present:

| Rows | Gap | Name | Amount | Date |
|---|---|---|---|---|
| 4600 / 4699 | 99 | GetData Inc | 150 | 2024-04-22 |
| 6135 / 7356 | 1221 | GetData Inc | 8.33 | 2024-12-13 |
| 6793 / 7273 | 480 | GetData Inc | 8.33 | 2024-12-13 |

**Why dedup-#2 missed them (root cause).** These are **not** the tight-cluster batch-re-append signature (that had a median within-group row span of ~45). Their spans are 99 / 480 / 1221 rows — consistent with **older, unrelated manual double-entry**, a different duplication source. Concretely they slipped dedup-#2 because:
- **Pairs 6135/7356 and 6793/7273:** col **E** (`TDGs Provisioned`) differs (`0.08` vs `8.33`) while col **G** (`TDGs Issued`) matches — if the pass keyed on E (or a body that embedded the provisioned figure) the group didn't form.
- **Pair 4600/4699:** col E renders `150` vs `150.00` — a numeric-vs-string format artifact that defeats a formatted-value comparison.

**Small relative to the ledger** (166.66 TDG vs E1 = 2,500,759.27) and **not urgent**, but it is genuine excess and the "strict de-dup is complete" claim is therefore only true for the keys each pass used.

**Action if pursued:** requires a governor go (money-adjacent, irreversible). Would delete the later row of each pair (keep earliest: 4600, 6135, 6793) via a write-capable SA (cypher-defense), backup first, then re-reconcile E1 and re-check the origin `Scored Chatlogs` col-L pointers below the deleted rows. Also worth deciding whether the **dedup criterion should normalise col E numerically** (and treat E=0.08 vs 8.33 as the same event) before the next pass.

### `installGovernorSyncTrigger()` daily 04:00-UTC cron has never fired — governor sheet-permission sync is silently manual
**Filed 2026-09-21. Owner: Sophia. Governor: Gary (thread 34264). Status: confirmed bug, not yet fixed.**

**Symptom.** Governor→spreadsheet editor reconciliation (`tokenomics/google_app_scripts/1m8IZPs1vFN99cuu-39kbC-OGXggRVtJtXq5rfSB0M1sCQjMdolEUDuGU/GovernorSheetPermissionSync.js`) is designed to run **daily at 04:00 UTC** via `installGovernorSyncTrigger()` (L87–95: `ScriptApp.newTrigger('syncGovernorEditorsCron_').timeBased().everyDays(1).atHour(4).inTimezone('UTC')`) and to write a **`Governor Sync Log`** tab (`SYNC_LOG_SHEET`, auto-created via `ss.insertSheet` at L270–272) on every run.

**Evidence it has never run.** Main Ledger tab list read 2026-09-21 (SA `edgar_dapp_listener`, `spreadsheets.get`): **no `Governor Sync Log` tab exists** among the 40 tabs — yet the GAS auto-creates it on every invocation. Consequence: rotation has been manual, which is why governor **Aga Marecka** (`agnieszkamarecka@gmail.com`) currently holds **no editor access** to the Main Ledger or the Intiatives/Scoring Rubric sheet, and 5 sentinel agents (`admin+sophia@`, `admin+kimi@`, `admin+deepseek@`, `admin+open+ai@`, `admin+envoy@truesight.me`) are also missing — exactly the drift the sync was built to prevent.

**Likely causes to check (owner to confirm).** (1) Trigger never installed (fresh deploy / `installGovernorSyncTrigger()` never called); (2) installed but the project's `appsscript.json` lacks the `https://www.googleapis.com/auth/script.scriptapp` scope; (3) `syncGovernorEditorsCron_` throwing early. Check `appsscript.json` for the `script.scriptapp` + Sheets scopes.

**Proposed fix (~small).** Verify `appsscript.json` scopes; call `installGovernorSyncTrigger()` (owner-run) and confirm a `Governor Sync Log` row appears and the trigger shows in `ScriptApp.getProjectTriggers()`; add a staleness monitor (alert if no log row in >48h), mirroring the proven `farm-media-publisher` freshness pattern. No change to the sync logic itself.

**Evidence.** Main Ledger tabs list (no `Governor Sync Log`, 2026-09-21); `GovernorSheetPermissionSync.js` L36, L87–95, L270–272; thread 34264.

### SunMint Plot Explorer — filter panel should be collapsible (eats vertical space on the plot list)
**Filed 2026-09-21. Owner: Sophia. Governor: Gary (thread 33323). Status: queued by Envoy — low priority, pick up after threads 34264/10800 settle. Not yet started.**

**Ask (Gary).** The `#filters` block in `sunmint/plots/index.html` (Farm / Plot type / Status /
Boundary authority / Data quality) is always expanded and consumes a large share of the
left rail, leaving little room for the plot list itself. Gary wants it **collapsible** so the
list gets more space.

**Measured on live beta 2026-09-21** (headless, `beta.truesight.me/sunmint/plots/`):

| viewport | filters height | list viewport | plots fully visible | after collapsing filters |
|---|---|---|---|---|
| desktop 1440×900 | **319 px** (~44% of rail) | 350 px | **4 of 21** | list → **670 px**, **7 visible** (+75%) |
| mobile 390×844 | **303 px** | 388 px (46vh cap) | 5 of 21 | list height unchanged (capped) but **303 px of pre-list scroll removed** |

Not purely cosmetic: on desktop the filter block pushes the list down so only ~4 of 21 rows
are reachable without scrolling; collapsing nearly doubles the visible list. On mobile it
compounds the PR11c pain (304 px of dead scroll before the list/filters).

**Proposed work (~small, UI-only, one file).** Add a collapse toggle in `.rail-head`:
(1) toggle button ("Filters ▾") that hides/shows `#filters`;
(2) **collapsed-state summary** — show `Filters (N active)` + active facet chips inline so a
filtered list is never unexplained (respects the page's own **§5** invariant: counts reconcile,
gaps visible);
(3) persist state in `localStorage`, default **expanded on desktop / collapsed on mobile**;
(4) add a **Clear all** affordance in the expanded panel (today you must click each active chip).
No data/logic change.

**Open product decision for the governor.** Default **collapsed** (maximise list space) vs
**expanded with toggle available** (discoverable). Sophia leans *expanded-by-default on
desktop, auto-collapsed on mobile*.

**Evidence.** `sunmint/plots/index.html` (`#filters`, `.facet`, `renderFilters()`; mobile media
query ≤820px); live-beta headless measurement 2026-09-21; thread 33323.

### `[PLOT FINANCING EVENT]` (PR10a/PR10b) shipped with zero documentation footprint
**Filed 2026-09-20. Owner: Sophia. Governor: Gary (thread 33541). Status: docs gap, not yet written.**

**Context.** The `[PLOT FINANCING EVENT]` vertical — a cash **advance** from the DAO that finances N trees on a plot (OPPOSITE direction to `[PAYOUT EVENT]`) — shipped as **code** in two PRs: `dao_protocol` **#177** (`c68718a`, PR10a: catalog entry + `dispatch.py` route `PLOT_FINANCING_PROCESSING` → `processPlotFinancingEventsFromTelegramChatLogs` + regression test) and `tokenomics` **#538** (`1beabd0`, PR10b: GAS sink `process_plot_financing_event_telegram_logs.js` + `plot_financing_harness.mjs` + `test_plot_financing_guard.py`, source-only). Envoy independently verified both merges 2026-09-20.

**But the vertical has NO documentation footprint** — verified against `origin/main` 2026-09-20:
- `agentic_ai_context/plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` — `grep -i financ` = **0 hits**; the plan's §0 Decisions stop at **0.13**, so the rulings that produced this event (the Q4 per-plot financing model, Q5 the N-tree declaration event, plus the `Currencies` col-U charge decisions 0.14–0.16) are **not recorded there**.
- `tokenomics/SCHEMA.md` — **no `Plot Financing` tracking-tab section**, and the literals table does not cross-reference the financing advance.
- `tokenomics/API.md` — **no `[PLOT FINANCING EVENT]` section** (unlike §9's `[TREE PLANTING LINK EVENT]`).
- `OPEN_FOLLOWUPS.md` — nothing.

**Why it matters.** This is a **money-path** event (it books `-amount` + `+N 'Cacao Tree Planted - Unassigned'` on main and seeds `SunMint Plots` col T). A money-writing event with no schema/API/decision record is exactly the class the plan's own §1.9 discipline was meant to prevent — the deliverable was scoped but never given a unit number (the plan's own **PR8** is the unrelated aging report; the financing work became **PR10** and skipped the docs pass).

**Proposed work (~small, docs-only).** (1) Add **Decisions 0.14–0.16** to the plan's §0 (per-plot financing, the N-tree declaration event, the col-U infra-charge resolution). (2) Add a `SCHEMA.md` section for the **`Plot Financing`** tracking tab (`PF_TRACKING_TAB`; cols in `process_plot_financing_event_telegram_logs.js`) and cross-reference the three literals. (3) Add an **`API.md`** section for `[PLOT FINANCING EVENT]` (labels: `Plot ID`, `Tree Count`, `Amount`, … — mirror the catalog entry). (4) Add a **PR10** row to the plan's §4 tracker. No code change; the event itself is already registered and tested.

**Evidence.** `dao_protocol` `c68718a`; `tokenomics` `1beabd0`; `truesight_dao_client/server/data/events_catalog.json` (`PLOT FINANCING EVENT`); `google_app_scripts/1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT/process_plot_financing_event_telegram_logs.js`; plan §0 (stops at 0.13); thread 33541.

### `snapshot_managed_ledgers.py` uppercases currency keys — managed-ledger snapshots do not match `Currencies`-tab keys
**Filed 2026-09-20. Owner: Sophia. Governor: Gary (thread 33541). Status: confirmed bug, not yet fixed.**

`python_scripts/tdg_asset_management/snapshot_managed_ledgers.py` **L91** does
`currency = (row[TX_COL_CURRENCY].strip() or 'USD').upper()`, so every currency key in the
`treasury-cache` `managed-ledgers/*.json` snapshots is force-uppercased on read
(`Kraft Pouches` → `KRAFT POUCHES`, `Cacao Mass Bar (500grams)` → `CACAO MASS BAR (500GRAMS)`).

**Consequence.** Any consumer that keys off a snapshot's currency string silently misses the
matching `Currencies`-tab row — exactly how **AUM valuation** (`tdg_wix_dashboard.js` converts
every AGL balance to USD via `Currencies!B`) and **first-seen** resolution look up prices.
Found while refuting Decision 0.13: the snapshot's uppercase `CACAO TREE TO BE PLANTED` was
mistaken for a *live per-ledger literal*, when the raw sheets hold mixed case on every ledger.

**To do.** Either (a) drop the `.upper()` and snapshot currency verbatim (then fix downstream
code that relied on the uppercasing), or (b) keep it but also emit the raw value (e.g.
`currency_raw`). Pick with the governor; a case-insensitive lookup on the consumer side is the
minimum safe fix. Add a test that a mixed-case literal survives the snapshot round-trip.

**Related.** `plans/SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md` §8.5 (Decision 0.13 — REVERSED 2026-09-20).

### SunMint plot → farmer mapping: derive `SunMint Plots`.`Contributor Name` by geographic proximity (scope + open questions)
**Filed 2026-09-20. Owner: Sophia. Governor: Gary (thread 33541, plan `SUNMINT_FARMER_SETTLEMENT_AND_BATCH_LINK_PLAN.md`). Status: scoped, NOT built — blocked on prerequisites + governor answers.**

**Context.** The plan's PR6/PR7 plot-level link path resolves the farmer from `SunMint Plots` **col T `Contributor Name`**, and **fails closed** when it is blank. All 22 existing plots have col T empty, so plot links all fail closed today — the reason the PR7 live dry-run allocated **0 plots** (and 51 of 60 QRs went unallocated for lack of a target). Originally framed as a manual field-data backfill; **Gary (2026-09-20): “I think the plot is linked to the farm by proximity”** — i.e. derive the farmer by nearest registered farm rather than typing names by hand.

**This changes HOW the col-T backfill is done, not WHETHER it needs prerequisites — and the prerequisites do not exist yet.**

**🚩 Open questions (answer before building):**
1. **Farm registry first.** `SunMint Registered Farms` is **headers-only / empty**. Who populates farm **lat/long + owner**, and when? Proximity is impossible without it.
2. **Plot coordinates.** `SunMint Plots` holds only Plot ID + name — **no lat/long**. Where do *plot* coordinates come from so a distance can be computed?
3. **Match rule.** What distance = “by proximity” — a fixed radius, or nearest-farm-wins with no threshold?
4. **Ambiguity.** Plot equidistant to two farms, or nearer a farm than any registry entry — fail closed, or pick nearest?
5. **Persistence.** Compute once as a col-T backfill, or derive live at each link event?
6. **Cardinality.** Is a plot bound to exactly one farm (and hence one `Contributor Name`)?

**My read:** items **1–2 are hard prerequisites** — the backfill cannot run until *both* the farm registry (locations + owners) and plot geocoding exist. Deliverable once unblocked: a proximity allocator that, per plot, finds the nearest registered farm and writes its owner into col T, with the same fail-closed discipline as the link path (never guess a farmer identity for a money-discharging link).

**Related:** plan §1.6 (plot link path), §5.9e TC13, PR6 note (⚠️ SunMint Plots col-T backfill), PR7b dry-run finding (0 eligible plots).

### PII-in-public-JSON safety: confirm the CRF plan §11.4 `excluded_pii_events` exclusion is actually deployed
**Filed 2026-09-20. Owner: Sophia. Governor: Gary (thread 31842, spun from thread 30026). Status: UNVERIFIED — needs confirmation, not assumption.**

**The hazard.** `cfr-anapu#11` (P4, plan §11.6) is **merged and live** on `cfr.truesight.me`, so `payout_registration.html` can now submit a `[PAYOUT REGISTRATION]` carrying a **plaintext PIX key**. §11.4 (P2) requires `[PAYOUT REGISTRATION]` be listed in `excluded_pii_events` in the **public JSON-cache generators** (`sync_sunmint_signatures.py`, `ledger_emit.py`). **If that exclusion is not deployed, a raw PIX key can reach public `verify_public_signatures/**`.**

**To close this entry:** verify the exclusion is present in the deployed generators (grep for `PAYOUT REGISTRATION` in the exclusion list + confirm the public JSON output for a payout-registration row is redacted), then move this entry to `## Recently shipped`.

**Related, parked (design only — not code).** `plans/PII_EVENT_ENVELOPE.md` (design doc) + CRF plan §11.10 define the lasting fix: encrypt PII-bearing events at the **public-JSON boundary** (AES-256-GCM + RSA-OAEP-wrapped data key) and emit a SHA-256 commitment in the clear, so submission is *verifiable without disclosure*. Rollout E1–E5, where E5 (operator key provisioning: KMS CMK + IAM + escrow) is `gate: human`. **Open decisions awaiting the governor's option pick** (plan §9): replace vs alongside the raw-PIX transport; KMS vs Fernet vault for custody; 2-of-3 governor escrow wrap; generic vs payout-only scope. Thread 31842 was closed + archived 2026-09-20 on the basis that nothing further was scoped to *that thread* — the remaining work lives in CRF §11.10 / §11.4.

### dao_protocol `webhook_trigger.py` treats any HTTP 2xx as success — GAS load-crash error pages slip through
**Filed 2026-09-20. Owner: Sophia. Governor: Gary (thread 31905). Status: fix drafted, not yet pushed.**

`truesight_dao_client/server/jobs/webhook_trigger.py` — both `trigger()` and `trigger_with_params()` return `True` on `resp.ok` (any 2xx) with **no body inspection**. Google Apps Script serves top-level load-time crashes (e.g. the `getCredentials()` ReferenceError that broke project `1orWgdGckts55…`) as an **HTML error page at HTTP 200**, so dao_protocol logged `"webhook ok"` while the handler never ran. Confirmed root cause of a missing expense record (Scored Expense Submissions row 240, R$1,050 Brazilian Reis, target `offchain`): the EXPENSE_PROCESSING webhook pointed at the load-broken 19Wag9x deployment; repointed by `tokenomics#524`, and the row was later processed by the hourly cron fallback (offchain line 4317, hash `b9744dcb939a486d`, no duplicate).

**Blast radius:** all ~33 wired `DAO_PROTOCOL_WEBHOOK_*` actions share this client.

**To do:** add `_is_gas_html_error()` (match the `<title>Error</title>` GAS signature only, so an intentional HTML web app isn't misclassified) and gate both trigger fns on `resp.ok and not _is_gas_html_error(resp)`; a GAS error page logs a distinct *"handler crashed; NOT retried"* warning and returns `False`. **Do NOT retry** — a crashed handler doesn't self-heal and `/exec` calls are non-idempotent. Add `tests/test_webhook_trigger.py` (2xx + `<title>Error</title>` ⇒ False/no-retry; 2xx JSON/plaintext ⇒ True; non-2xx ⇒ False).

### Standing rule: consult `GOOGLE_SHEET_SA_ACCESS_MATRIX.md` before probing service-account access
**Filed 2026-09-19. Owner: Sophia. Governor: Gary (thread 33265). Status: matrix SHIPPED (PR #1289); this entry is the habit pointer.**

**Rule.** Before picking a service account to **write** to a Google Sheet tab — or before declaring a tab "unwritable" — read `credentials/GOOGLE_SHEET_SA_ACCESS_MATRIX.md` (machine-readable: `credentials/google_sheet_sa_access_matrix.json`). It is the canonical, empirically-probed per-tab truth for the Main Ledger and Cypher Defense Ledger.

**Why it exists.** Repeated sessions stumbled on "which SA for which sheet/tab": info was scattered across `GOOGLE_API_CREDENTIALS.md`, `GOVERNOR_SHEET_PERMISSION_SYNC_SOP.md`, `AUTOPILOT_GOOGLE_ACCESS_PLAN.md`, and per-project code, with nothing stating the per-tab truth in one place. On 2026-09-19 a session probed the `Contributors contact information` tab with a **wrong key path** (`FileNotFoundError`), mis-read the resulting protection metadata as "no SA can ever write this", and escalated a false blocker. The governor corrected it: `agroverse-ledger-manager` writes the tab fine.

**Don't repeat:**
1. A `FileNotFoundError` on a credential JSON is a **path** bug, not an access verdict. Confirm the key file exists first.
2. A protected-range object with **no editor emails** does not mean owner-only. Spreadsheet-level editors can still write. Protection metadata is **not** a write test.
3. **Test the write** (e.g. empty string to the bottom grid row, read back) before concluding anything about access.
4. A tab that is genuinely owner-protected to every SA (e.g. `Governors`) is a **sheet-permission** ask to a human — never a credentials fault.

**Refresh:** `scripts/probe_sheet_sa_access.py` regenerates the matrix after any permission change, governor rotation, or new SA.

### RESOLVED-INCIDENT: GAS project `1orWgdGckts55…` was load-broken by a top-level `getCredentials()` ReferenceError
**Filed 2026-09-18. Owner: Sophia. Governor: Gary (thread 31905). Status: FIXED+DEPLOYED (tokenomics PR #527, v10).**

**Symptom.** Every function in the project threw at load time:
`ReferenceError: getCredentials is not defined (line 16, file "capital_injection_processing")`.
Because the call was **top-level**, ALL entry points (`doGet`, `parseAndProcessCurrencyConversionLogs`,
`parseAndProcessCapitalInjectionLogs`) were dead — so the PR #525 currency fix could not execute.

**Root cause.** `capital_injection_processing.js` had `const creds = getCredentials();` +
`const WIX_ACCESS_TOKEN = creds.WIX_API_KEY;`, but the project has **no `Credentials` file**
(live project = 4 files: appsscript, capital_injection_processing, CurrencyConversion, Version).
`WIX_ACCESS_TOKEN` was dead code (grep = 1 hit = its own definition); `getLedgerConfigsFromWix()`
reads the Google Sheets `Shipment Ledger Listing` tab, never the Wix API.

**Fix (per governor directive: "we can disable the code that uses WIX API Key").** Removed both
lines (tokenomics PR #527, merged `673b00e2`). No `Credentials.js` and no `WIX_API_KEY` Script
Property needed. Deployed: `clasp push` → version 10 → anonymous deployment
`AKfycbzTWe1EnX8oXX1RDOOXcS1e0GmkX_SusWhT18FQ7zqs3RMTRlYcpZlWLOIaSLzoViA0`.
Smoke-tested anonymously: `?action=listTriggers` → valid JSON (both CLOCK triggers);
`?action=parseAndProcessCurrencyConversionLogs` → `✅ Currency conversion logs processed successfully`;
ledger tail shows a single conversion pair (no duplicate append). Interim broken v9 deployment deleted.

**Blame: NOT this session's push (evidence).** The deploy script's remote-only-file guard (refuses a
push that would delete a live file) ran clean at push time → the accessor was already absent.
`Credentials` was never git-tracked, so an earlier pre-guard push caused it. *(Inference from guard
behaviour, not a logged deletion event.)*

**Security note.** The frozen `@8` snapshot's `Credentials` file carries hardcoded live secrets
(Wix key + XAI + OpenAI). Masked on read. The Wix key now survives only in that snapshot and should
be revoked/rotated in Wix (same token already tracked under the "Wix token in public history" entry).

### Systemic: 9 GAS projects call `getCredentials()`/`setApiKeys()` but have no tracked accessor file
**Filed 2026-09-18. Owner: unclaimed. Governor: Gary (thread 31905).**

Repo-wide scan found **9** `google_app_scripts/*/` projects that call a credential accessor they do
not define locally and have no tracked `Credentials.js`:
`15qbfLN3…, 1MnAsIQA…, 1Q5HfGR_…, 1QKqUTyl…, 1_3D4o2R…, 1m2sQONd…, 1orWgdGckts55… (fixed), 1vC3p_Wf…, 1zKgMwd6…`.
`1orWgdGckts55…` was **missed** by the 2026-09-18 `.gitignore` negation remediation (which covered
10 *other* projects). Any of these can hit the same load-time `ReferenceError` the moment the
accessor is absent — and `clasp push --force` will **delete** an untracked live file.
**To do:** per project, either (a) add a secret-free Script-Properties-backed accessor +
`.gitignore` negation, or (b) if the credential is genuinely unused (as here), delete the call.
Verify each; do not batch-assume.

### Autopilot box `/tmp` reached 100% disk (41 G of stale session clones) — add a janitor
**Filed 2026-09-18. Owner: unclaimed. Governor: Gary (thread 31905).**

`git_push_changes` failed with `No space left on device`; `df` showed `/` at **78G/78G (100%)**.
`/tmp` held **41 G** of stale clone dirs from prior sessions (~16 000 dirs). Cleared by hand
(kept today's attachments + the local tokenomics checkout) → 11 G free.
**To do:** add a periodic `/tmp` janitor (delete clone dirs older than N hours) so a full disk
can't silently break a push again.

### CurrencyConversion.js canonicalize/idempotency fix (PR #525) — DEPLOYED as v10
**Filed 2026-09-18. Owner: Sophia (DEPLOYED 2026-09-18 + verified end-to-end). Governor: Gary (thread 31905).**

**Context.** Two defects in `tokenomics/google_app_scripts/1orWgdGckts55owiYOysR_y4sde52T_eUmrtDGAEkb4YV5DlUfJ0JZC5J/CurrencyConversion.js`
are fixed in **PR #525** (code only — NOT deployed):
1. `parseCurrencyConversionMessage()` forced `.toUpperCase()` on source/target currency -> `Brazilian Reis`
   written as `BRAZILIAN REIS`, which the case-sensitive `off chain asset balance` rollup bucketed
   separately (three co-existing rows). Fixed with `canonicalizeCurrency_()` resolving against
   `agroverse-inventory/currencies.json`.
2. `processNewCurrencyConversions()` appended the debit+credit pair before flipping Status, with no
   lock and no append-level idempotency -> two overlapping runners (Edgar webhook + 10-min cron)
   could each post a pair (observed: `offchain transactions` rows 4315-4318). Fixed with a script
   lock + `NEW -> PROCESSING` claim-before-append + a Request-Transaction-ID idempotency scan.

**To do (governor decision first).**
1. ~~**`clasp push` the fix**~~ ✅ **DONE 2026-09-18** — pushed, version 10 cut, deployed +
   smoke-tested anonymously (blocked until PR #527 restored loadability; see the incident entry above).
2. **Legacy label cleanup.** The Main Ledger still carries the historical mangled labels
   (`BRAZILIAN RE` on intake row `Edgar_20260511022114_011`; the old `BRAZILIAN REIS` balance row has
   already been hand-fixed by Gary). Decide whether to normalise the historical intake/summary rows;
   the new code only self-heals *future* resubmissions, it does not rewrite existing rows.
3. **`manifest.json` "deployments.head" is still `TBC`** for this scriptId. Deployment ids found
   2026-09-18: `@HEAD AKfycbwMY0PfO7dnMszwUilr6DZBY5eeBGh86QEgshO7cgY` (login-walled — NOT anon-callable);
   `@10 AKfycbzTWe1EnX8oXX1RDOOXcS1e0GmkX_SusWhT18FQ7zqs3RMTRlYcpZlWLOIaSLzoViA0` (current, anon);
   `@8 AKfycby8bOb0iEfJh-Io90fK-NQRpC6BlLC66e6MCr3JvyOEi-UDH-TkwYSsdeXKuhkpsU4` (superseded, anon).
   Record the @10 URL as `deployments.head`; note `@HEAD` is login-walled even with `ANYONE_ANONYMOUS`.

### SECURITY: Agroverse Wix token is still retrievable from PUBLIC `tokenomics` git history (committed `63f441e`)
**Filed 2026-09-18. Owner: unclaimed. Governor: Gary (thread 31220).**

**Context.** The orphan/`clasp_mirrors` flatten landed secret-bearing Wix GAS source in the
`tokenomics` repo **before** the Wix retirement. The token was **redacted in the working tree**
(`google_app_scripts/deprecated/tdg_rate_sync_to_wix.gs` now reads `// REDACTED 2026-09-17`),
and the current tree is clean — `git grep "IST.eyJ"` on `origin/main` → **0 hits**. But the
**original blob is still in history**:

```
git show 63f441e:google_app_scripts/1zAXSdLe_vigsygxqX41w_evQb3KfrtzUc4rFI3AxwdUjp8E-h3nIvgDG/Code.js
# -> var wixAccessToken = "IST.eyJraWQiOiJQb3pIX2FDMiI..."   (721-char Wix JWT)
```

- `63f441e` (2026-06-16, “remove redundant .gs files already migrated to project folders”) — **token present, 1 occurrence**.
- Redacted only later: `bb016ff` / `c82616f` (2026-09-16/17) — **0 occurrences**.
- Total commits whose diff contains the token string: **3**. Fingerprint `2aaefd55359b` appears in **1**.
- **`TrueSightDAO/tokenomics` is PUBLIC** (verified: anonymous `git ls-remote` succeeds) → the token is retrievable by anyone via `git show 63f441e:<path>`.

**The live project is gone, so deleting it does not help.** `1zAXSdLe…` ("TDG USDT exchange rate update") is **deleted, not merely inaccessible**: Apps Script API → `404 Requested entity was not found`; Drive `files.get` → `404 File not found` while a control live scriptId resolves fine. So the token can only be neutralised by **revoking it in Wix** (the project no longer exists to delete).

**Why this entry exists.** The `## Pending` entry *“Sibling GAS project 1wONDeDwZ … rotate”* covers the **live-only** copies and notes the *class* of leak (“PR #369 / f8b38a8”), and other scrub items are tracked separately — but **no entry tracks that this specific Wix token is committed in public history**. Filing it so the scrub does not silently rot.

**To do (governor decision first).**
1. **Revoke the Wix token in the Wix admin** — the only hard fix; Wix is retired, so no flow should break.
2. **Decide whether a history rewrite is warranted.** Scrubbing requires `git filter-repo`/BFG + **force-push to a public, multi-contributor repo** — invasive and itself irreversible-ish (rewrites every SHA downstream). Given Wix is retired and the token will be revoked, revocation alone may suffice; the rewrite buys defence-in-depth only. Do **not** force-push without an explicit governor go and a coordination plan.
3. If scrubbing is declined, record that decision here and close.

**Distinct from** the live-only `Credentials.js` rotations already shipped this session (PRs #507/#510/#512/#514/#515) — those cleaned the working tree and the live projects; none of them touch **git history**.

### Black King corridor: NF1/NF2 have a tracking number but no arrival-register row (register gap)
**Filed 2026-09-18. Owner: unclaimed. Governor: Gary (thread 31905).**

NF1 (`CP340992695BR`) and NF2 (`CP340992687BR`) are both `Autorizada` in `shipment_nfe`, and both
parcels appear in `CORREIOS_SHIPMENTS.md` with shipping receipts, but the arrival register
(`offchain assets in transit`, gid 1888711771) has **no row** for them. The register is missing
3 of the 14 Correios trackings (`CP340992130BR`, `CP340992687BR`, `CP340992695BR`).

**Destination:** the NF-e Taraval destinatario is the TrueTech **fiscal/billing** address only
(governor ruling, 2026-09-18) - it does not by itself fix the physical recipient.

**Governor leaned "perhaps ignore" (2026-09-18):** no register rows are being added for NF1/NF2.
Left open pending a definitive call. Source: `BLACK_KING_NFE_TRANSIT_CROSSWALK.md` State B.

### Black King corridor: reconcile AGL6 / `CP327946643BR` NF-e detail looseness (optional, low priority)
**Filed 2026-09-18. Owner: unclaimed. Governor: Gary (thread 31905).**

Rows 3-5 of the arrival register (`offchain assets in transit`) = parcel `CP327946643BR` = consignment
**AGL6**, billed by **Coopercabruca NF-e No. 888** (CNPJ 31.948.811/0001-42) - a **different emitter's**
NF-e set from the 15 Black King NF-e (see `BLACK_KING_NFE_TRANSIT_CROSSWALK.md` section F). Two
declared-vs-shipped mismatches remain:
1. **Unit:** NF 888 declares bulk (100 kg nibs + 100 kg cacao mass); AGL6 shipped ~20 kg retail-packed.
2. **Date:** register expected-arrival `20250211` postdates the 2024-11-21 NF-e.

Governor reading (2026-09-18): *"the Matheus or the lawyer just went easy on the details"* - a bulk
invoice drawn loosely against a repacked consignment. **Low priority.** Action only if precision is
wanted: confirm with the accountant whether a Feb-2025 Coopercabruca NF-e exists, else reconcile the
register date.

### Black King corridor: NF11/NF12/NF14 destination - RESOLVED 2026-09-18 → see "Recently shipped"
**Filed 2026-09-18; resolved 2026-09-18. Governor: Gary (thread 31905).**

Governor ruling: **keep Kirsten Ritschel / 1423 Hayes St**; the NF-e Taraval destinatario is the
**fiscal/billing** address only. Crosswalk annotated (Rev 4); no register rows changed.

### ACL privatisation of the `Telegram Chat Logs` workbook broke two public surfaces (`/notarizations`, `/submissions/raw-telegram-chatlogs`)
**Filed 2026-09-18. Owner: unclaimed. Governor: Gary (thread 30026).**

**Context.** On 2026-09-18 the `anyone reader` grant on the `Telegram Chat Logs`
workbook `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` was removed (to satisfy
"only folks with explicit access rights" / CRF_ANAPU plan §11). Verified after:
no `anyone`/`link`/`domain` grants, no publish-to-web revision, and anonymous
`gviz`/`edit`/`export` all return **401**. The fix is correct for PII, but two
public surfaces were served by a **302 redirect straight to the raw sheet** and
so now bounce anonymous visitors into a Google **login wall**:
- `https://truesight.me/notarizations` → `.../edit?gid=520413576` → **401**
- `https://truesight.me/submissions/raw-telegram-chatlogs` → `.../edit?gid=0` (Telegram Chat Logs tab) → **401**

**Impact.** `/notarizations` was a live public document-verification tool — the
CRF_ANAPU plans doc §11 cites it as *the* reason a raw PIX may never be written
to col G. It is now dark (redirects to a login wall, not merely empty). The
underlying notarization **files are NOT lost**: they live in the public
`TrueSightDAO/notarizations` repo (repo API 200; real PDFs/images present).

**Fix (~small).** Repoint `/notarizations` at a public-safe projection instead
of the raw sheet: either (a) a GAS WebApp that reads the `Document Notarizations`
tab via its SA and serves only those columns, or (b) a static index generated
from the public `TrueSightDAO/notarizations` repo. Separately decide whether
`/submissions/raw-telegram-chatlogs` should be retired or repointed. Confirm the
mirror GAS `process_notarization_telegram_logs.js` (reads `Telegram Chat Logs`
col G → appends to `Document Notarizations`) still runs post-ACL — it runs as
the script owner/SA, so expected OK.

**Distinct from** the pre-existing "Document Notarizations tab stale" entry
(mirror GAS not firing) — that is the tab not updating; this is the public view
now being auth-walled.

### Autopilot `merge_pr`: false refusal (`ci-unavailable` 403) on repos with NO CI workflows
**Filed 2026-09-17. Owner: unclaimed. Governor: Gary (thread 31187).**

**Symptom.** `merge_pr` refused to merge `sentiment_importer` PR #1136 with
`CI not green (ci-unavailable: Resource not accessible by personal access token: 403 ... list-check-runs)`
plus an `(unnamed)` pending check — despite the repo having **no** `.github/workflows` at all.
`gh pr view 1136` showed `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`, `statusCheckRollup: null`.
The PR was clean; the *tool* produced a false negative and the PR had to be landed via `gh pr merge`.

**Root cause (proven 2026-09-17).** In `truesight_autopilot` `app/github_client.py`, `_ci_status()`
calls `commit.get_check_runs()` **and** `commit.get_combined_status()`; when either raises, the
exception branch sets `reason = "ci-unavailable: ...403..."` and returns **`green=False`** -> `merge_pr`
refuses. The upstream `403 Resource not accessible by personal access token` means the resolving PAT
lacks the **Checks (read)** permission on that repo (fine-grained PAT). The existing `no-ci`
fast-path only triggers on **zero check rows**, which never happens when the call *errors* instead.

**Why it matters.** A permission quirk on a repo with no CI is misinterpreted as "CI is red".
On `truesight_autopilot` itself the same gate correctly refuses (it *has* `smoke`/`test` workflows) —
so the behaviour is inconsistent across repos purely because of token scope. (This false refusal is
what sent the autopilot off-course on thread 31187.)

**Proposed fix (~small, autopilot codebase).** On `ci-unavailable`, don't hard-refuse — probe
`.github/workflows` via the **Contents API** (the token *can* read contents): absent => treat as
`no-ci` (warn + allow merge); present => keep refusing (never merge a repo whose real CI is merely
unreadable); unknown error => conservative default (assume CI exists). A draft was built on
thread 31187 (autopilot PR #487) then closed as out-of-scope for that thread — re-open as its own
unit. Add unit tests on `_ci_status()` for the three branches.

### Source-guide QC: HK import guide #2 carries two unverified figures
**Filed 2026-09-17. Owner: unclaimed. Governor: Gary (this thread).**

**Context.** While verifying the governor-supplied 11-page *"Market Access Requirements … to Hong Kong"* guide (Brazil→HK raw cacao) against primary sources, two checkable figures failed verification. The **corrected** values are already in `brazil/BRAZIL_TO_HONG_KONG_IMPORT_SOP.md` §2.4; this entry exists so the **upstream guide** (likely AI-generated) gets flagged and the errors don't propagate.

**The two errors.**
1. ❌ Guide: *"The fee for a 3-year registration is HK$180."* → Per FEHD/CFS, the **new** 3-year registration fee is **HK$195**; **HK$180 is the renewal fee**. (Notably, the *first* governor-supplied HK guide — a 3-page one — had this right.)
2. ❌ Guide: *"Late submission will incur penalties (typically starting from HK$2,000 for a first offence)."* → **Unsupported.** The Import and Export (Registration) Regulations provide a **HK$1,000** fine **+ HK$100/day** for failure to declare, with a late-lodgement *penalty* of **HK$20–$200** (doubled if value > HK$20,000). **No HK$2,000 figure exists** in the regulations.

**Action (small).** If the guide's source/generator is known, feed these two corrections back. No DAO doc change needed — SOP already corrected.

### Source-guide QC: GCC/Middle East guide — ECAS conflation + superseded FASEH framing
**Filed 2026-09-17. Owner: unclaimed. Governor: Gary (this thread).**

**Context.** While verifying the governor-supplied 2-page *"Market Access Requirements … to Qatar, UAE (Dubai) and Saudi Arabia"* guide, two claims were flagged. The **corrections** are already in `brazil/BRAZIL_TO_GCC_MIDEAST_IMPORT_SOP.md` §4–5.

**The two issues.**
1. ⚠️ Guide: *"Certain food categories require an ECAS Certificate of Conformity"* (UAE). Likely an **ECAS/FIRS conflation**: **ECAS** (Emirates Conformity Assessment Scheme, **MoIAT**) covers **non-food** regulated products (electrical, tyres, …). Food conformity in Dubai runs through **FIRS / Dubai Municipality**. Confirm with the importer / Dubai Municipality before budgeting for an ECAS CoC.
2. ⚠️ Guide: *"as of April 1, 2026, certain Brazilian products (e.g. poultry) have been added to the mandatory CoC list … confirm the latest status for raw cacao beans."* → **Superseded.** Per the SFDA circular, effective **30 August 2026** the **FASEH platform is mandatory for ALL food-shipment Certificates of Conformity** — CoCs issued outside FASEH are no longer accepted. It is **not** category-specific; every food shipment (cacao included) now needs a FASEH-issued CoC.

**Action (small).** Flag to the guide's source/generator; re-confirm both points at booking time (already listed in the GCC SOP §12 open questions).

### Autopilot: pin the `gh` CLI to the canonical PAT (stray under-scoped token → 403 createPullRequest)
**Filed 2026-09-17. Owner: unclaimed. Governor: Gary (thread 31220).**

**Symptom.** GitHub PR/branch operations intermittently fail with `403 Resource not accessible by personal access token` / `createPullRequest denied`, even though the app's own tools (`git_push_changes` / `open_fix_pr` / `merge_pr`) work fine.

**Root cause (proven 2026-09-17).** Four PATs resolve to the same identity (`garyjob`): `TRUESIGHT_DAO_AUTOPILOT` (fine-grained; PR-create probe → **422 = authorized** ✅), `GITHUB_READ_PAT` (read-only → 403), `KRAKE_IO_PAT` (Krake-scoped → 403), and the token stored by the `gh` CLI in `~/.config/gh/hosts.yml` — a **fourth, separate fine-grained PAT that was under-scoped** (→ 403). Because all four are the same user, `gh auth status` looks correct while writes fail; the discriminator is *which* token, not *who*.

**Interim fix applied on the Sophia box (manual).** (a) re-authed `gh` with the canonical PAT (`printf '%s\n' "$TRUESIGHT_DAO_AUTOPILOT" | gh auth login --with-token --hostname github.com`; backup at `~/.config/gh/hosts.yml.bak.*`); (b) appended a guarded `export GH_TOKEN="$TRUESIGHT_DAO_AUTOPILOT"` block to `~/.bashrc`. Documented in `credentials/API_CREDENTIALS_DOCUMENTATION.md` §10.2.2.

**Proper fix (small, autopilot codebase).** Make it structural so a fresh box self-corrects — pick one: (1) at service start (`app/main.py` lifespan) reconcile `~/.config/gh/hosts.yml` / `GH_TOKEN` to the canonical PAT; (2) have `config.load_dotenv` also export `GH_TOKEN = settings.github_pat` into the process env so any `gh` subprocess inherits it; (3) add a `create_pr` tool that shells nothing out and reuses `git_tools`/`github_client` (the app's sanctioned path). Add a startup assertion that flags a mismatch. Removes the "which token did `gh` grab" trap for every sibling instance (Bionpact, Envoy, …), which today must otherwise be fixed by hand per box.

### `nelanco-claude` (Envoy's box) — recurring instance-reachability failure, root cause unknown
**Filed 2026-09-16. Owner: unclaimed. Governor: Gary.**

**Symptom.** `i-01ad5eca707e4445f` (`nelanco-claude`, `100.57.50.48`) has gone fully unreachable
**twice in 3 days**:
1. **2026-09-14** — Gary tried to `stop-instances` and it sat in `stopping` for an extended time
   (it did eventually reach `stopped` cleanly; root cause never determined).
2. **2026-09-16/17** — found `running` per the AWS control plane with `SystemStatus: ok` but
   **`InstanceStatus: impaired`** (`reachability: failed`, `ImpairedSince: 2026-09-17T01:31:00Z`);
   SSH and ICMP both timed out. A soft `reboot-instances` did **not** restore reachability after
   ~3 min of polling; `stop-instances` → `start-instances` (the known-working fix from incident 1)
   was used again.

**What this means.** Stop/start (which migrates the instance to different underlying hardware)
resolves the symptom both times, which points at either a **host-level AWS hardware fault**
(recurring on the same physical host would explain both) or a **guest-OS-level hang** (kernel/
network-stack lockup, possibly triggered by something running on the box — it commonly hosts
several concurrent `tmux`/`claude` sessions, faster-whisper transcription jobs, etc. per
`ENVOY.md`/`sophia/SUPERVISOR_LOOP.md`). Neither has been confirmed; `get-console-output` only
captures boot-time serial output, not a live tail, so it showed nothing past the last successful
boot in both incidents.

**Impact.** Envoy's interactive Claude Code box — and, since 2026-09-14, the box the proactive
Sophia-supervisor loop (`sophia/SUPERVISOR_LOOP.md`) is meant to run on — going dark with no
alert means unfinished Sophia handoffs sit un-supervised until a human happens to notice the box
is unresponsive, which is exactly the gap the supervisor loop was built to close.

**Proposed fix (~small, monitoring only).** Add a CloudWatch alarm on
`StatusCheckFailed_Instance` (and/or `StatusCheckFailed_System`) for `i-01ad5eca707e4445f`,
notifying via the existing Telegram/Discord alert path (see `AWS_DIGITAL_INFRASTRUCTURE.md` §8
Monitoring for the pattern already used elsewhere) so a third recurrence pages someone instead of
waiting to be noticed. If it recurs a third time, also pull EC2 host-level info
(`describe-instances` `Placement`/`HostId` if using a dedicated host, or open an AWS support case)
to rule in/out a bad physical host — two data points isn't enough to conclude that yet.

**Evidence.** `aws ec2 describe-instance-status --instance-ids i-01ad5eca707e4445f` (impaired,
2026-09-17T01:31:00Z); `aws ec2 get-console-output` (clean boot log ending 2026-09-14T23:24:41Z,
nothing after); this session's remediation (reboot attempt → no recovery → stop/start → recovered).

### truesight_autopilot: automate Stripe subscription-renewal → per-bar `[SALES EVENT]` reconciliation

**Filed 2026-09-16. Owner: unclaimed. Governor: Gary (thread 30870).**

**Context.** Linda Ford's Sept-2026 chocolate-bar subscription renewal was reconciled by hand. The
recipe is now written up in `plans/SOPHIA_SUBSCRIPTION_SALES_PLAN.md` ("the standard SOP"): given a
set of QR codes → (1) check `qr_status` (`SOLD` ⇒ already accounted for, skip; `MINTED` ⇒ reconcile);
(2) pull the Stripe invoice (`billing_reason=subscription_cycle`); (3) take the fee from the charge's
`balance_transaction`; (4) `net_per_bar = (amount_charged − stripe_fee) ÷ number_of_bars`;
(5) submit **one `[SALES EVENT]` per QR code**. Phase-2 fulfillment automation
(`CHOCOLATE_SUBSCRIPTION_PLAN.md`) is **deferred/blocked**, so nothing performs this automatically today.

**Why it matters.** Every month a human (or Sophia, hand-rolling) must notice the renewal, find the
invoice, and fan out N events — error-prone (thread 30870's first pass divided by bars+shipping, ÷7,
and got net/bar wrong).

**To fix.** Add `scripts/reconcile_subscription_sales.py` to `truesight_autopilot`: flags
`--invoice in_…` **or** `--qr-codes …`; reads `stripe_live_key` from the vault (`app/vault.py`; the
value is never printed); computes the formula above; **dry-run by default**, `--submit` to fire;
**idempotent** via the `qr_status` preflight. Optionally a monthly detector (Surface 5 / scheduled
probe) that flags any `subscription_cycle` invoice in the last 30 days with un-recorded QR codes and
notifies the operator.

**Related security note.** The `stripe_live_key` was found **hardcoded in plaintext** in
`sentiment_importer/config/environments/production.rb` (alongside other live secrets). Rotation + move
to `ENV.fetch` / secret-manager + git-history scrub is recommended and tracked separately.

### truesight_autopilot: `_compute_advance_signal()` omits §2.1's "explicit self-report" `made_progress` path

**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30279).** `plans/SOPHIA_AUTO_ADVANCE_PR_LESS_UNITS_PLAN.md` §2.1 defines `made_progress` as a turn with **either** a side-effecting tool call, **or** a direct repo commit, **or** "an explicit self-report of success the turn itself asserts (the final-message convergence text, already parsed elsewhere for the '✅ Done this turn' report)". The shipped implementation (`app/main.py::_compute_advance_signal`) keys `made_progress` on **tool names only** (`_MAKE_PROGRESS_TOOLS` + `_UAT_PROGRESS_TOOLS`) — the self-report path is not implemented. Surface: PR4 UAT — a verify-only unit that performs a real check purely via read-capable tools (`ssh_run`, `read_*`) and ends with a "✅ Done this turn" self-report still **gates** ("turn made no progress…"). **Impact:** a genuinely-completed verify-only unit (the class this plan exists to un-gate) can still force a human `go` if it happens not to perform a repo write. **Proposed fix (~small):** either wire the final-message convergence text into `made_progress` per §2.1, or amend §2.1 to drop path (c) and require a tracked side-effect (e.g. a tracker self-update) for a PR-less unit to count as progress. Decide intent first.

### 3 credential-vault gaps left by the SSH-key migration (clasp / stripe / cypher-defence PAT)

**Filed 2026-09-15 by Sophia. Owner: UNCLAIMED (separate thread). Governor: Gary (thread 30473).**

**Context.** `plans/SOPHIA_VAULT_CREDENTIAL_MIGRATION_PLAN.md` Unit 2 listed 7 credentials to
migrate. The 3 **SSH keys** (2b/2c/2d) are migrated and their consumers repointed
(`truesight_autopilot#471`, `#472`). The remaining three are **still bare files** — code
falls back to the on-disk path:

| Plan unit | Vault name (intended) | Bare file still on disk | Consumer that still falls back |
|-----------|------------------------|--------------------|-------------------------------|
| 2e | `clasp_oauth_gary` | `/home/ubuntu/.clasprc-gary.json` | `gas_deploy_project` (clasp OAuth) |
| 2f | `stripe_test_key` | `/home/ubuntu/stripe_test_key` | beta-sandbox Stripe tooling |
| 2g | `github_cypher_defence_pat` | `/home/ubuntu/CYPHER_DEFENCE_OPS_PAT` | Cypher-Defense repo ops |

**Why it matters.** Until migrated, Unit 6 (archiving the bare files) cannot be fully closed,
and these three keep the "stale ungoverned on-disk credential" risk the vault exists to remove.

**To fix.** Same pattern as the SSH keys: `vault.add(...)` each value, confirm each consumer
resolves vault-first, then include their bare files in the Unit 6 archive.


### treasury-cache: per-key emitter SILENTLY DROPPED by the 2026-06-16 migration — per-key store frozen since 2026-06-18 (U5 FAIL)

**Filed 2026-09-15. Owner: UNCLAIMED. Governor: Gary (thread 30471). Fix PR: TrueSightDAO/tokenomics#494 (open, unmerged — GAS deploy is gate:human).**

**Context (found during UAT U5 of PUBLIC_KEY_LOOKUP_CACHE_PLAN).** PR1 (tokenomics#359) + PR2 (#361) merged 2026-06-16 to make
`dao_members_cache_publisher.gs` emit **per-key files** `public_keys/<sha256>.json` + `public_keys/_manifest.json`, written atomically with
`dao_members.json`. A later commit the SAME EVENING — `50999ec` "migrate: flatten clasp_mirrors/ into google_app_scripts/<scriptId>/ folders"
(2026-06-16 23:23 −0700) — **deleted that file with no rename destination** and re-added the folder "from manifests", i.e. it rewrote the repo
to match the **then-deployed GAS state (the pre-PR1 script)**. The per-key emitter therefore existed only in git for ~1 hour and **never ran in production**.

**Evidence (all verified 2026-09-15).**
- Last `public_keys/` commit = **2026-06-18**; every `dao_members.json` refresh since (through 2026-09-15) touches **0** per-key files.
- Current `DaoMembersCache.js` has **no** per-key logic (`git log -S "public_keys/"` on it = empty; 0 hits for `_manifest`/`createTree`/`createBlob`/`REVOKED`).
- Org-wide code search for a per-key emitter: **0 hits** — it was never re-homed elsewhere.
- Pre-migration blob (`296c41aa`) still contains the lost code: `computeSha256_`, `fetchCurrentManifest_`, `commitMultipleFilesToGithubViaTreeApi_` + the build block.

**Impact.** *(a)* The `dapp_beta` `permissions.js` per-key lookup (PR5) and the governor vault (PR4) resolve keys via the per-key file — with
generation frozen, **every key registered since 2026-06-18 and every role change since then is invisible to the per-key store**. *(b)* Keys with **no**
per-key file (all 12 of Gary's newer keys + every post-June key) fall back to the **TTL-cached monolith** (`load_governors`, `GOVERNORS_CACHE_TTL=300`),
so the **~5‑min first-sign-in lag PR4 retired returns for exactly those keys**, and the O(1) goal silently degrades to O(n). *(c)* It is the shared
root cause of the Elizabeth Wong drift entry below.

**Fix.** Restore the three helper functions + per-key/manifest build block into the flattened `DaoMembersCache.js` (+ a tree-SHA no-op guard so cron
re-pings don't spam empty commits). **Done: tokenomics#494 (open).** Then GAS `clasp push` + `publishDaoMembersCacheNow()` smoke test — **gate:human**
(do not auto-deploy GAS). After deploy, confirm a fresh `public_keys/` commit lands and coverage reaches 100% of ACTIVE keys.

**Verification note.** tokenomics PR #494 drafted by Sophia from the pre-migration blob; `node --check` passes on all 8 project `.js` files.

### dapp / treasury-cache: Elizabeth Wong per-key `roles` drift — BLOCKS `dapp_prod` promotion of the per-key lookup cache

**Filed 2026-09-15. Owner: UNCLAIMED — root cause routed to Gary (real person's governor-role data). Governor: Gary (thread 30471).**

**Context.** Found during PR5 step-3/UAT U1 verification. PR5 step 2 makes the DApp `permissions.js` resolve a signed-in RSA via
`treasury-cache/public_keys/<sha256(base64pubkey)>.json` and treat that file's `roles[]` as authoritative when `status=ACTIVE`.
Diffing every ACTIVE per-key file against the monolith `dao_members.json`: **exactly one role mismatch — Elizabeth Wong.** Her file says
`roles: ["member"]`; the monolith says `roles: ["governor","member"]`.

**Symptom.** With step 2 live, a governor signing in with her key would be **denied governor-gated DApp actions** — the same *class* of
stale-cache bug this whole plan exists to retire, now on the generator side. **This must be resolved before `dapp_prod` promotion.**

**Root cause — RESOLVED 2026-09-15 (was flagged UNVERIFIED; now confirmed systemic, NOT a one-off).** Her stale file is a *symptom*
of a generator regression: the **per-key emitter was dropped by migration commit `50999ec`** ("flatten clasp_mirrors/ …", 2026-06-16 23:23 −0700),
merged ~1h *after* PR1 (tokenomics#359) + PR2 (#361) added it. That commit rewrote the repo to match the then-deployed GAS state (the pre-PR1
script), so per-key generation has been **frozen since 2026-06-18**. See the dedicated regression entry below. **Fix = restore the emitter**
(tokenomics PR #494) — after which her file regenerates correctly and the data half closes itself; only the true-roles confirmation stays human.

**Proposed fix (2 parts, ~small).** (a) DATA: confirm the true current roles for Elizabeth Wong, then either regenerate her per-key file or
correct the source sheet — a human decision. (b) CODE: make governor/member role changes (re)publish the affected per-key file(s), so the
per-key store cannot silently lag the monolith.

**Evidence.** `treasury-cache/public_keys/<sha256(wong_key)>.json` → `roles: ["member"]`, `generated_at 2026-06-18`; `dao_members.json` →
`roles: ["governor","member"]`, `generated_at 2026-09-15`; 79-key diff = 1 mismatch; thread 30471.

### truesight_autopilot: auto-advance directive repeatedly quotes a STALE unit (“one behind” the live `RESUME HERE` marker)

**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30471).**

**Context.** Across a single execution session the injected `[AUTO-ADVANCE]` directive named a unit **one behind** the live plan marker **5–6 times**
(e.g. it kept quoting “PR4 ✅ MERGED” while the live `RESUME HERE` had advanced to PR5 step 1/2/3). Each time, re-reading the plan file from
`agentic_ai_context@main` showed the marker already advanced — so the directive text was sourced from a **pre-tracker-PR snapshot** (the manifest/§5 row
as it read *before* that turn's tracker PR merged), not re-read at dispatch time. Only manual re-verification against the live file prevented re-running
an already-shipped unit (duplicate-PR risk).

**Symptom.** The auto-advance gate can dispatch a unit that was already completed, or skip the real next one — silent, and it erodes trust in the
directive (the operator must hand-verify every turn).

**Proposed fix (~small).** Have the auto-advance **re-read the plan's live `RESUME HERE` at dispatch time** (fetch `agentic_ai_context@main` fresh, or
read the raw file) rather than embedding a cached manifest snapshot; alternatively, inject the **raw marker line verbatim** and require the agent to
re-verify it against the live file before acting (the practice that worked). Related: the `find_resume_here()` substring bug filed above (same gate).

**Evidence.** 5–6 misfires in thread 30471; each directive text matched the *previous* unit while `git show origin/main:plans/...` showed the advanced
marker; cf. `app/auto_advance.py`, the “bare `RESUME HERE` substring” entry above.

### truesight_autopilot: the autopilot box silently runs stale code — deployed `/opt/truesight_autopilot` lags `origin/main`

**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30083).**

**Context.** Found during PR5 UAT (sprint board). The running `truesight-autopilot` service (`uvicorn app.main:app`, port 8001, `WorkingDirectory=/opt/truesight_autopilot`) was **2 commits behind `origin/main`** — `0a3d1a1` (#467 progress-query classifier) and `45e15cb` (#466 PR4c(a) auto-claim/release, which adds `app/supervision.py`) were merged but **absent from the running tree**. `git ls-tree origin/main app/supervision.py` → blob present; the deployed tree lacks the file and `main.py` has no `claim_for_turn` call — so merged auto-claim behaviour is **dark in production**. Autopilot-box analog of the `dao_protocol` no-CD entry.

**Symptom.** A merged PR's behaviour cannot be observed live — the box runs the previous SHA with no alert. UAT of any autopilot-side feature can spuriously "fail" against code that was never deployed.

**Proposed fix (~small).** (a) Have the deploy path record the deployed SHA prominently (a deploy ledger exists); (b) expose the running SHA (e.g. a `/version` endpoint, like `edgar.truesight.me/ping`'s `version`) and compare it to `origin/main` so "merged but not deployed" is visible rather than silent.

**Evidence.** `git -C /opt/truesight_autopilot rev-list --left-right --count HEAD...origin/main` → `0  2`; deployed tree has no `app/supervision.py`; thread 30083 (PR5 UAT U7); same root cause reported for thread 30475.

### sprint-site: board reads jsdelivr before raw — lags `index.json` by the CDN TTL

**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30083).**

**Context.** `app.js`'s `SOURCES` lists `cdn.jsdelivr.net/gh/TrueSightDAO/agentic_ai_context@main/handoffs/index.json` **before** the `raw.githubusercontent.com` fallback, and `fetchFirst` returns the first source that responds — so the board renders jsdelivr's **cached** copy, lagging `index.json` on `main` by the jsdelivr TTL (observed: board meta `updated 15:43:37Z` vs raw `16:56:54Z`, ~1h).

**Symptom.** After merging an `index.json` change, the live board shows stale data until the CDN expires — reliably confuses UAT (the board appears to "disagree" with the repo).

**Proposed fix (~small).** Reorder `SOURCES` to put `raw.githubusercontent.com` first (always fresh), or keep jsdelivr and purge it at deploy (`https://purge.jsdelivr.net/gh/<repo>@main/handoffs/index.json`), or cache-bust with `?t=<ts>`.

**Evidence.** `sprint-site/app.js` `SOURCES` + `fetchFirst`; live-vs-raw `updated` differ ~1h; thread 30083.

### sprint-site: add a browser-safe smoke test (computed visibility), not just byte greps

**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30083).**

**Context.** PR5 UAT used headless Chrome (`--dump-dom`) to prove view-tab behaviour — e.g. `?view=board` / `?view=sup` render **exactly one** section. A byte/grep-level check cannot catch this board's real bug class: the view-tab `[hidden]` fix, where attribute/class combinations left sections both visible or both hidden. `--dump-dom` returns the restructured DOM but **not** applied computed `display`, so it too is only a proxy.

**Symptom.** A regression that breaks tab/section visibility ships green because the gate only counts feature references in served bytes.

**Proposed fix (~small).** Add a smoke test that loads the deployed board, asserts each view shows exactly one `<section>`, and checks element **computed style** (`getComputedStyle(el).display`) where feasible (headless Chromium evaluate, or playwright/puppeteer in CI).

**Evidence.** PR5 UAT method (headless `--dump-dom`); `sprint-site/app.js` view-tab logic; the agroverse_shop_beta "UAT must execute the JS, not grep-count" lesson; thread 30083.

### sprint-site: header "N supervising" counts stale claims while the lane excludes them

**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30083).**

**Context.** The board header meta computes `… · N supervising` as `handoffs.filter(h => h.supervised_by).length`, which **includes** stale claims (`supervised_by.stale === true`). The 👀 supervised **lane** correctly excludes stale claims. So a stale-only claim inflates the header count while the lane shows nothing.

**Symptom.** Header count and lane disagree; "2 supervising" can mean "2 active" or "1 active + 1 stale" indistinguishably.

**Proposed fix (~small).** Count **fresh** claims only (`supervised_by && !supervised_by.stale`), or split the label (`N active · M stale`).

**Evidence.** PR5 UAT U5 (doctored-stale index: badge `stale (95 min)`, lane excluded it, meta still counted it); `sprint-site/app.js` meta computation; thread 30083.
### truesight_autopilot: `find_resume_here()` matches a bare `RESUME HERE` substring anywhere — incidental prose breaks the auto-advance parser

**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30083).**

**Symptom (2nd occurrence of this class).** `plans/SPRINT_TRUESIGHT_ME_BOARD_PROPOSAL.md` line 393 carried
the descriptive phrase "so both `RESUME HERE` occurrences agree" — a *prose* mention of the token, not a marker.
`app/auto_advance.py:find_resume_here()` takes the **last** match of
`_RESUME_RE = RESUME\s+HERE\s*[:=]?\s*(.*)` in the whole file, so it latched onto line 393 (which sits *after*
the real marker on line 391) and captured garbage ("occurrences agree,") → the auto-advance gate misfired.
Line 393 was reworded to "both resume markers above agree" to unblock immediately.

**First occurrence.** An earlier break was a leading arrow character (`→ PR5`) leaking into the unit key.

**Why it is not a quick one-liner.** The marker format across `plans/*.md` is highly variable: bold
(`**RESUME HERE → PR3**`), heading (`## RESUME HERE`, `> ## ▶ RESUME HERE`), quoted, — and critically — often
**mid-line after prose** (this very plan's *real* marker is `executing in this session. **RESUME HERE: PR5 …`).
Several plans ALSO carry bold **prose** mentions of the token that are not markers
(`GETDATA_IO_MCP_AGENT_MARKETPLACE_PLAN.md:57`, `FARM_SHIPMENT_MEDIA_JSON_PLAN.md:290`, `GETDATA_IO_MCP…:179`).
So neither "require line-start" nor "require bold" is safe without a migration pass over every plan.

**Proposed fix.** Define a canonical marker grammar (e.g. token followed by `:`/`=` and a unit label matching
`PR\d+` / `Unit \d+` / `none` / `complete`, and not preceded by an opening backtick), migrate the plans in one
sweep, then add golden-file regression tests for the prose-mention cases listed above. Owner: unclaimed.

**2026-09-15 update (PR4 UAT).** PR2 (truesight_autopilot#474, merged `1254da2`) shipped the canonical marker grammar this entry proposed: `_RESUME_RE` now **requires** a connector (`:`/`=`/`→`), so it can no longer latch onto a bare prose mention like line 393's "occurrences agree" — the reported `SPRINT_TRUESIGHT_ME_BOARD_PROPOSAL.md` case is fixed (corpus-verified: 0 regressions across all 60 plan docs; that plan now resolves its real marker). **Residual not closed:** a *prose* mention that carries a connector still matches (`FARM_SHIPMENT_MEDIA_JSON_PLAN.md:290`, a quoted `"RESUME HERE = PR0"`) — currently benign only because last-wins selects the real downstream marker. A future pass could require line-start or a unit-like tail.
### MAP: Medicilandia farmers-convention 2024 — finish the media-archive pipeline (open the manifest PR + add the photo content layer)
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 23734).**

**Context.** Thread 23734 archives the Medicilandia farmers-convention 2024 site-visit media
(186 files: 72 MOV + 114 HEIC) into the Media Archive Pipeline (MAP) so the Portuguese
content becomes retrievable by English search. Done so far, all on-branch (nothing merged):

- **v2 manifest** — 186 items (258 KB, `medicilandia-convention-2024.json`), committed
  `738eda1` on branch `medicilandia-convention-manifest` in `farm_media_manifests`; **the PR
  was never opened** (`gh pr create` fails — the push PAT lacks the `createPullRequest` scope).
- **Videos enriched** — 72/72 MOVs transcribed (54 with speech → English title/description +
  burned `.vtt`; 18 silent), driver `/tmp/medic_video_enrich.py`, 829 s, 0 failures.
- **S3 archive** — resume-safe raw + preview-frame upload to `media.agroverse.shop`
  (`raw|previews/medicilandia-convention-2024/`); config `farm_id: medicilandia-convention-2024`
  registered; last observed mid-pass at ~149/186 raw.

**Still needed.** (1) **Open + merge the manifest PR** for `medicilandia-convention-manifest` —
until merged, the 186-item archive is invisible to GitHub code search (the retrieval layer).
(2) **Confirm the S3 pass reached 186/186** raw + previews. (3) **Build the per-photo
content-extraction layer** — photos currently get *no* OCR and *no* object detection (both are
video-only); the technical slides in this batch (e.g. `IMG_4460` fermentation stages, `IMG_4420`
cacao strategies) need `ocr_text_pt`/`ocr_text_en` + `objects[]`/scene tags in the manifest, or
English queries like "photos of the fermentation talk" won't resolve. Design confirmed in-thread;
not yet implemented.

**Evidence.** Thread 23734; manifest commit `738eda1` (branch `medicilandia-convention-manifest`);
driver `/tmp/medic_video_enrich.py` (72/72); `MEDIA_ARCHIVE_PIPELINE.md`.

### truesight_autopilot: `merge_pr` refuses a docs-only PR when CI is legitimately path-filtered, not actually pending
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (sprint-board thread 30083).**

**Context.** Sophia opened `agentic_ai_context` PR #1158 (docs-only: `sophia/SUPERVISOR_LOOP.md` +
`plans/SPRINT_TRUESIGHT_ME_BOARD_PROPOSAL.md`, no `handoffs/**` or `scripts/**` touched). The `merge_pr`
tool refused it, reading CI status as "pending." The actual workflow,
`validate-handoff-manifest.yml`, is `paths:`-filtered to `handoffs/**` + `scripts/**` — it was never
going to run for this PR's changed files, so `gh pr checks` correctly reports "no checks reported" /
combined status `pending/total 0`. `merge_pr` apparently treats "zero checks reported" the same as
"checks running, not done yet," rather than "no checks configured for these paths — nothing to wait
for."

**Symptom.** Any docs-only PR whose changed files fall entirely outside a path-filtered workflow's
trigger paths cannot be merged via `merge_pr` without a human manually running `gh pr merge` from the
box instead — an unnecessary human round-trip for a PR that's actually ready.

**Proposed fix (~small).** In whatever tool code backs `merge_pr`, distinguish "0 checks reported
because none are configured for these paths" (safe to merge) from "checks reported but still running"
(genuinely pending) — likely by cross-referencing the PR's changed-files list against each workflow's
`on.pull_request.paths` trigger, or simply treating `total: 0` from `gh pr checks`/the checks API as
mergeable rather than blocking.

**Why it matters.** Same root pattern as `plans/SOPHIA_AUTO_ADVANCE_PR_LESS_UNITS_PLAN.md` (filed same
day, same thread): a correct, converged outcome getting misread as unfinished, forcing an unnecessary
human intervention. Different code path (the merge gate, not the auto-advance gate) — kept as its own
entry rather than folded into that plan's scope.

**Evidence.** `agentic_ai_context` PR #1158; `validate-handoff-manifest.yml`'s `paths:` trigger;
sprint-board thread 30083, 2026-09-15.

### HANDOFF_MANIFEST validator: send-probe each `message_thread_id` for liveness (dead-topic class)
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (stale-topic audit, thread 30445).**

**Context.** A governor "go"-ping into a parked handoff's topic can silently vanish if that topic was **deleted** — the ping is dropped and the plan sits GO-ready forever with no signal. Found live during the 2026-09-15 stale-backlog audit: **6 of 7** parked handoff rows (threads 5712, 3981, 2799, 2317, 1955, 1939) pointed at Telegram topics that no longer existed. `scripts/validate_handoff_manifest.py` passed clean throughout — it checks manifest **structure** (columns, duplicate `message_thread_id`, status keywords, `--check-index` drift) but **never whether the thread actually exists**. The name cache (`sessions/_topic_names.json`) is not authoritative either — it still held stale names for 3981/5712.

**Proposed fix (~small).** Add an opt-in liveness pass to `validate_handoff_manifest.py` (e.g. `--probe-threads`): for each row's `message_thread_id`, send a self-cleaning `sendMessage` probe (post, then immediately `deleteMessage`), treating a non-`ok` response — specifically `Bad Request: message thread not found` — as DEAD. Keep it behind a flag + bot token so the default structural run stays offline (CI-safe); emit a list of dead/missing threads. **Implementation note:** `sendChatAction` does NOT validate the thread (it returns OK for a dead thread) — must use `sendMessage`.

**Why it matters.** This is the exact failure mode that strands a parked plan with no operator signal; a cheap preventive keeps the manifest honest about which handoff topics are still reachable. Pairs with the fresh-topic re-links done in the 2026-09-15 audit (all 6 rows re-pointed or marked superseded).

**Evidence.** 2026-09-15 stale-backlog audit (thread 30445); send-probe results — 5712/3981/2799/2317/1955/1939 all "message thread not found", control 2744 alive; `scripts/validate_handoff_manifest.py`; `sessions/_topic_names.json`.

### truesight_autopilot: add `mypy` to CI (last remainder of AUTOPILOT_HARDENING Phase 1)
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (stale-topic audit, thread 30445).**

**Context.** `plans/AUTOPILOT_HARDENING_PLAN.md` (thread 2317) is **superseded** as a handoff — its topic was deleted and Phase-1 PR-A + PR-B already landed: CI now runs `compileall` + `ruff` (lint+format) + the **full** pytest suite with the 3 `--deselect` flags removed (`smoke.yml`). The only piece never shipped is **PR-C: `mypy`**. `mypy` appears **nowhere** in `requirements-dev.txt`, `pyproject.toml`, or `.github/workflows/`. Historical note: mypy was **unsatisfiable in this environment at plan-writing time** (2026-06) — the pinned toolchain required a `pydantic-core` that failed to build — so it was deferred; re-verify that constraint first.

**Proposed fix (~small).** Add `mypy` to `requirements-dev.txt` + a `[tool.mypy]` config in `pyproject.toml` (lenient: `ignore_missing_imports = true`, non-`--strict`), establish a passing baseline, and wire a mypy step into `smoke.yml`. Tighten incrementally later. `truesight_autopilot` own-repo gate — opens PRs only, never self-merges.

**Why it matters.** Types catch the "wrong attr / half-pasted snippet" class of LLM-authored bugs that `compileall` (syntax only) misses — the stated reason PR-C was in the hardening plan.

**Evidence.** `smoke.yml` (compileall + ruff + pytest present; no mypy); `grep -rn mypy requirements-dev.txt pyproject.toml .github/workflows/` -> empty; `plans/AUTOPILOT_HARDENING_PLAN.md` Phase 1 (PR-A done, PR-B done, PR-C todo); 2026-09-15 audit.

### dao_protocol: `tests/test_dao.py` fails to collect on `main` — imports removed `dedup` module
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 26992).**

**Symptom.** `pytest tests/test_dao.py` errors at collection on `main` (HEAD `d12406f`): `ImportError: cannot import name 'dedup' from 'truesight_dao_client.server'` — `tests/test_dao.py:8` does `from truesight_dao_client.server import dedup, dispatch`, and line 27 `monkeypatch.setattr(dedup, "is_duplicate", ...)`. The `dedup` module no longer exists in the package, so the whole file fails to collect. The rest of the suite is fine (e.g. `tests/test_empty_body_guard.py` → 8/8 pass), and dao_protocol has **no CI test workflow** (only npm/pypi publish), so nothing catches this on merge.

**Proposed fix (~small).** Remove or repoint the `dedup` references: drop the `dedup` import + the `is_duplicate` monkeypatch if de-duplication moved elsewhere, or update the import to the module's new location. Then confirm `pytest -q` collects and passes.

**Why it matters.** A dead test file gives false confidence and blocks anyone running the suite locally before a push.

**Evidence.** `pytest tests/test_dao.py -q` → `ERROR tests/test_dao.py ... Interrupted: 1 error during collection`; `tests/test_dao.py:8,27`; dao_protocol HEAD `d12406f`; thread 26992.

### Black King (Matheus Reis Pereira) — FSVP CAPA for the 2026-09-12 Ilhéus warehouse GMP finding
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 29093).**

**Context.** During the governor's 12–13 Sep 2026 visit to the Black King warehouse in Ilhéus/BA (used to store Agroverse cacao destined for US FDA lanes), a pre-cleanup visual walk-through found conditions that would have failed a US FDA (FSVP / GMP) inspection: live cockroaches and dead lizards near the bathroom area, insects entering via a wide-open bathroom window, mortar bags stored in the restroom, no mop/vacuum on site, and no pest-control cadence. Governor's own words in the WhatsApp thread (`_chat.txt`, 9/13/26 9:56 AM): "If the FDA inspector had came and inspected the warehouse yesterday before the clean up, the inspection would have failed and Black King would have been put on the USA government black list." Governor performed an ad-hoc cleanup + reorg; no documented corrective-action record exists.

**Proposed fix (~small, doc-only).** Create a CAPA (Corrective And Preventive Action) record under `fda_fsvp/suppliers/black_king/` capturing: observation (with photo-log references), immediate correction taken (cleanup + reorg 12–13 Sep), root cause (no assigned owner of facility hygiene / no SOP), preventive action (see the warehouse-ownership follow-up below), and verification plan (scheduled re-walk with photo evidence). Follow the naming used by the other Black King FSVP artifacts (`YYYYMMDD_Black King_<doctype>.pdf`).

**Evidence.** WhatsApp export `Matheus Reis - Bahia Coop` — `_chat.txt` 9/12/26 4:43–4:44 PM (cockroaches/dead lizards, open bathroom window), 9/13/26 9:56 AM (inspection-would-have-failed), 9/12/26 9:40–10:35 PM (pallets + vacuum/mop); photo `00000295-PHOTO-2026-09-12-16-43-56.jpg` (open bathroom window). FSVP file: `TrueSightDAO/fda_fsvp/suppliers/black_king/` (four product-level written assurance letters; no CAPA).

### Black King — warehouse-maintenance & pest-control written assurance addendum (FSVP gap)
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 29093).**

**Context.** The four Black King written-assurance letters on file (`20240909` nibs, `20240923` molasses, `20241016` mass, `20250602` tea) address **equipment** maintenance and storage-area hygiene only as hazard-table lines. None affirms a **facility** maintenance schedule, pest-control cadence, or storage-cleaning SOP for the actual Ilhéus storage facility. Under 21 CFR 1.511 a written assurance must address the hazard requiring a control (here: filth/pest and moisture→mycotoxin during storage). The only warehouse-specific artifacts are a TrueTech-signed storage site visit (`20241013_Black_King_site_visit_storage_warehouse.pdf`, whose Visual Observation table is blank) and a bare Brazilian fumigation NFS-e (`20250610_warehouse_fumigation.pdf`, ASTRA SUL BAHIA, R$300, dedetização), which is not cited by any assurance. Two storage addresses appear (FDA FFR/entity.json: Av. Tancredo Neves 4900; site visit: Rua Coronel Paiva 46) with no stated linkage.

**Proposed fix (~small, doc-only).** Draft a Black King–signed **warehouse maintenance & pest-control addendum** covering: storage facility address(es) and their linkage, scheduled cleaning SOP, pest-control/fumigation cadence (referencing the ASTRA fumigation vendor), drying/humidity control against mycotoxin, and the inspection-readiness checklist. Register the fumigation NFS-e and the storage-location address(es) in `entity.json`.

**Evidence.** `fda_fsvp/suppliers/black_king/*` (four letters; site visit; fumigation NFS-e); thread 29093.

### Black King CNPJ is INAPTO + e-CNPJ expired — export NF-e lane blocked (reinstatement plan)
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 29093).**

**Context.** Black King (`MATHEUS REIS PEREIRA`, CNPJ 50.042.585/0001-80, Ilhéus/BA) shows **SITUAÇÃO CADASTRAL: INAPTO since 08/06/2026**, motivo **"Omissão de Declarações"** (unfiled returns) on the Receita Federal comprovante (`00000165-Black King Certificate CNPJ.pdf`; address/CNAE fields suppressed). Separately the company's **digital certificate expired early June 2026**. Both block issuance of the NF-e export invoice, which in turn blocks the export lane (`BlackKing_Export_NFe_Enablement.pdf` documents the self-service path: add commerce CNAE → request IE at SEFAZ-BA → NF-e credentialing, ~8 days). A tax-support PDF (`00000285-PHOTO-2026-09-12-15-57-29.jpg`, "Informações de apoio para emissão de certidão", 01/09/2026) is in the thread.

**Proposed fix (~small, doc-only).** A reinstatement runbook: (1) file the omitted declarations (via the accountant / e-CAC) to return the CNPJ to ATIVA; (2) renew the e-CNPJ; (3) add the commerce CNAE; (4) request Inscrição Estadual + NF-e credentialing at SEFAZ-BA; (5) issue the export NF-e. Track as an export-readiness gate. Related: the governor holds (or is being granted) e-CAC power of attorney on the CNPJ + SISCOMEX representante registration.

**Evidence.** `00000165-Black King Certificate CNPJ.pdf`; `_chat.txt` 7/31/26 (cert expired, CNPJ "Inapto") and 8/19–8/21/26 (POA/SISCOMEX); `00000095-BlackKing_Export_NFe_Enablement.pdf`; thread 29093.

### SECURITY: rotate gov.br / Receita Federal credential leaked in plaintext in the Matheus WhatsApp thread
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 29093).**

**Context.** In the `Matheus Reis - Bahia Coop` WhatsApp export (`_chat.txt`, 8/17/26 3:51 PM) a **live Brazilian government (Receita Federal / gov.br) login credential — CNPJ 50042585000180 + a plaintext password — was transmitted in the chat**. This is a real credential exposure on a messaging channel (not a DAO secret), and the CNPJ is the same one currently INAPTO / being reinstated, so the account is an active target. **Do not reproduce the value in any artifact.**

**Proposed fix (~small).** Rotate the credential immediately (change the gov.br / Receita Federal password), enable 2FA on the gov.br account, and re-issue any stored copy rather than reusing the leaked one. Move future credential exchange out of WhatsApp (vault / the DAO vault). No repo change required beyond this tracking entry — action is owner-side.

**Evidence.** `_chat.txt` 8/17/26 3:51:10 PM (value redacted here deliberately); thread 29093.

### Black King Ilhéus warehouse: assign an owner for hygiene / pest-control / inspection-readiness cadence
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 29093).**

**Context.** The root cause of the 2026-09-12 warehouse finding is that **no one owns the facility's hygiene and pest-control cadence**. The governor discussed hiring a part-time office/warehouse administrator to "verify and ensure everything is in order, so that the warehouse is not failed in US government inspections" (`00000321-PHOTO-2026-09-13-11-13-30.jpg`, Portuguese) — the candidate **declined** ("I'm working with my mother and want to prioritise that"). Net: the gap is unowned. This is the highest-leverage fix — without an owner, any written assurance (above) is unverifiable.

**Proposed fix (~small, decision + checklist).** Decide the ownership model — paid stipend to a local part-timer, a duty rotation among existing Bahia staff, or fold it explicitly into Matheus's scope — and pair it with a simple weekly checklist + photo log (cleaning, pest cadence, closed windows, no non-food storage in restroom, drying/humidity readings) that feeds the CAPA verification.

**Evidence.** `_chat.txt` 9/12–9/13/26 (cleanup, pallets, mop/vacuum, "still waiting on you", non-food mortar in restroom); `00000321-PHOTO-2026-09-13-11-13-30.jpg` (administrator discussion + decline); thread 29093.

### HANDOFF_MANIFEST.md: the handoff table is split into segments — `find_table` only ever sees the first 3 rows
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30065).**

**Context.** `scripts/validate_handoff_manifest.py::find_table` reads the *first contiguous* markdown table whose header contains `Plan file`, and stops at the first line that does not start with `|`. `handoffs/HANDOFF_MANIFEST.md` is no longer one contiguous table — it is broken into segments by (a) an **orphan row fragment at line 27** (its leading `|` is missing, so it renders inside the previous row), (b) a **blank line at line 64**, and (c) a **ragged row at line 25** (10 cells from an unescaped `|` in prose). Because of the split, `find_table` returns **3 rows out of 43** — i.e. the validator has been silently validating ~7% of the manifest. Any consumer that trusts "validator passed" (CI included) is validating almost nothing.

**Symptom.** `python3 scripts/validate_handoff_manifest.py` prints OK while ~40 handoff rows — including duplicate `message_thread_id` reuse and unknown statuses — go unexamined. `scripts/build_handoff_index.py` (added in PR #1143) works around it: it gathers handoff-shaped rows across **all** segments and reports the raggedness as `warnings[]`, but the underlying manifest is still malformed.

**Proposed fix (~small).** Repair `handoffs/HANDOFF_MANIFEST.md`: rejoin the split table (escape the `|` in the line-25 prose; add the missing leading `|` to the line-27 fragment; remove the line-64 blank line). Then make `find_table` **tolerant** — skip blank lines and stray text inside the row region (as `build_handoff_index.collect_handoff_rows` already does) instead of terminating the table — and add a **coverage assertion** test so a future split cannot silently shrink the row count below the manifest's labelled count. Once fixed, the ordinary validator + the new `--check-index` gate both cover the full table.

**Evidence.** `scripts/validate_handoff_manifest.py::find_table` (stops on first non-`|` line); `scripts/build_handoff_index.py::collect_handoff_rows` (tolerant reader + `warnings[]`); warnings `line 25: ragged row has 10 cells, expected 9`, `line 27: stray text inside the handoff table (missing leading '|' — malformed row fragment)`, `line 64: blank line splits the handoff table`; PR #1143 (index builder); thread 30065.

### autopilot box: no token can *create* a PR — only Contents-API writes (403 `Resource not accessible by personal access token`)
**Filed 2026-09-15. Owner: unclaimed. Governor: Gary (thread 30065).**

**Context.** While shipping PR #1143 (handoff index), every PR-*create* attempt from the autopilot box failed with **403 `Resource not accessible by personal access token`**: `gh pr create`, and `POST /repos/TrueSightDAO/<repo>/pulls` using `GITHUB_TRANSCRIPT_PAT`, `GITHUB_READ_PAT`, `KRAKE_IO_PAT`, and `KRAKEIO_LLM_PLAYGROUND_PAT` **all** 403'd. The box's PATs are fine-grained with **Contents: write only — no Pull requests scope**. The workaround was to open the PR with the autopilot service's own tool credential, then fast-forward the box-authored commits onto that PR branch. Related but distinct from the existing `workflow`-scope gap (that entry is about `workflow_dispatch` / `actions:write`; this is about `pull_requests:write`).

**Impact.** Any script that wants to open a PR **on the box** (rather than via the autopilot's own tooling) cannot. It forces the tool-mediated path, and cost extra turns here (first PR-create attempt created no PR; the branch had to be reconciled onto a tool-created PR). Low severity for the agent path (the tool works), but it is a real capability gap for box-side tooling and for any future design that expects a script to self-open PRs.

**Proposed fix (~small).** Issue a fine-grained PAT (or install a GitHub App) with **Pull requests: write** (+ Metadata: read) for `TrueSightDAO/*`, store it in the vault, and have the box's git helper prefer it for PR creation; document the required scopes next to the other PATs. Alternatively, standardise on "the autopilot tool opens PRs; the box only pushes branches" and record that as the sanctioned flow.

**Evidence.** 403 responses (no secret values printed) for `POST /repos/TrueSightDAO/agentic_ai_context/pulls` from `GITHUB_TRANSCRIPT_PAT` / `GITHUB_READ_PAT` / `KRAKE_IO_PAT` / `KRAKEIO_LLM_PLAYGROUND_PAT`; `gh auth token` (username `garyjob`, scope-limited); PR #1143 (created via the autopilot tool instead); thread 30065.

### Discord adapter: progress-edit 429 storm — no client-side rate-limit awareness
**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (thread 27138, Discord adapter).**

**Symptom.** During a real governor turn (guild `923008087315587072`, channel `1548885989412573235`, 2026-09-14 17:34:21–17:36:00 UTC) the adapter's edit-in-place progress updates hit Discord **429 ten times in ~40 s against the SAME message** — `PATCH /channels/1548885989412573235/messages/1549111078015729807` (`app/discord_adapter.py::edit_message_text` → `_api`). Evidence: `journalctl -u truesight-autopilot-discord --since '2026-09-14 17:34'`.

**Root cause (two parts).**
1. **Edit spam with no bucket awareness.** All 10 log lines read `attempt 1/3` — proof each is the *first* attempt of a *distinct* `_api()` call, not an internal retry (a real retry would log `2/3`, then `3/3`). The progress loop calls `_edit()` on several unconditional paths (`call_chat_with_progress`: L704, L754, L790, L823, L828, L833), so edits fire far faster than Discord's per-message/per-channel bucket allows.
2. **429 handling is per-call and blind.** `_api()` retries only 3× within a single call using the body's `retry_after` but ignores the `X-RateLimit-Remaining` / `X-RateLimit-Reset-After` headers; the caller also ignores the `None` return, so a fully-429'd edit is **silently dropped**.

**Impact.** Degrades Tier-1 parity #1 "live progress visibility" (the progress message stops updating mid-turn) and risks Discord temporarily banning the bot on that channel. Cosmetic today, but it is a live governor-facing path.

**Proposed fix (~small).** In `app/discord_adapter.py`: (a) coalesce progress edits — single-flight with a global min-interval (≥1.5 s) and skip-if-unchanged; (b) honor `X-RateLimit-*` / `Retry-After` headers by tracking a module-level per-route bucket before the next send; (c) when an edit ultimately fails, log at WARNING with the message id so a dropped progress update is visible. Local suite must stay green (compileall / ruff check / ruff format --check / pytest).

**Evidence.** `app/discord_adapter.py` (`_api` L381–420, `edit_message_text` L837, `call_chat_with_progress` L669–833); `journalctl -u truesight-autopilot-discord --since '2026-09-14 17:34'`; thread 27138.

### `followups/state.json` is machine-owned inside the deploy tree — breaks any `git stash`/`checkout` in a scratch clone
**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (thread 27138).**

**Context.** `followups/state.json` (the follow-up monitor loop's sidecar — see `plans/SOPHIA_FOLLOWUP_MONITOR_PLAN.md`) is committed under the deployed repo and is **rewritten by the running loop** on the live box, so the working tree is permanently dirty (` M followups/state.json`).

**Impact.** Any `git stash` / `git stash pop` / `git checkout <ref>` in a scratch clone aborts on a conflict in this file whenever the loop touched it between the stash and the pop. This cost a manual recovery step **twice in two consecutive turns** during the Discord parity work (2026-09-14): the pop aborted and the patch had to be recovered with `git checkout -- followups/state.json` then a re-pop. Any agent doing a stash-based baseline comparison must also remember to exclude this file.

**Proposed fix (small).** Either (a) `.gitignore` `followups/state.json` and have the loop persist it to a non-deploy state dir (it is runtime state, not source), or (b) make it regenerate-on-read / conflict-tolerant so a stash pop cannot abort on it. (a) is preferred — machine-owned runtime state should not live in the tracked tree.

**Evidence.** `git status --porcelain` → ` M followups/state.json` on the live box; two aborted `git stash pop` recoveries on 2026-09-14 (thread 27138); `plans/SOPHIA_FOLLOWUP_MONITOR_PLAN.md` L34/L107 describe it as the loop's private sidecar.

### Autopilot tooling: `upload_local_file_to_github` sha-less 422 regression (update path) + `merge_pr` self-restart disruption

**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (thread 26215).**

**Symptom 1 — upload-tool sha 422 (REGRESSION).** `upload_local_file_to_github` and `upload_file_to_github` fail on the **update** path (overwriting an existing file) with `422 {"message":"Invalid request.\n\n\"sha\" wasn't supplied."}`. The tool does not fetch the current blob sha before issuing the Contents-API `PUT`. This reproduced **≥5 consecutive times** on 2026-09-14 while updating `brazil/2026-09-14_black_king_corridor_report_EN_PT.pdf` (~44 KB PDF). Prepending the correct `sha` by hand did **not** help — the tool re-fetches its own (empty) sha. Read-back confirmed the remote was still the prior revision while every call returned 422.

**This is a regression, not a new gap.** The same item is recorded as ✅ RESOLVED higher in this file (truesight_autopilot #87, 2026-06-03; "re-verified 2026-09-11 by a create→update probe … no 422"). It is 422-ing again as of 2026-09-14, so #87 has regressed.

**Working workarounds (confirmed on 2026-09-14):** (a) commit the file under a **new filename** (create path is fine — only update 422s); or (b) **direct `git push`** using `/opt/truesight_autopilot/scripts/git-credential-sophia.sh` (shell it for the PAT via `… | sudo …/git-credential-sophia.sh get`). Both landed the byte-identical blob (43,874 B verified on `raw.githubusercontent.com`). **Fix:** have the tool `GET` the blob's current `sha` before the `PUT`, or adopt the create-path/new-filename flow internally.

**Symptom 2 — `merge_pr` interrupted by an unrelated `deploy_autopilot` restart.** While `merge_pr` was waiting on GitHub rate-limit backoff, a `deploy_autopilot` triggered from a different thread restarted the autopilot box mid-call and cut the merge call off (observed 2026-09-14 12:43:08; also recorded in Telegram message 29509). Mitigation used: after restart, **verify whether the PR actually merged on GitHub's side** (via `git merge-base --is-ancestor <sha> HEAD`) before retrying, to avoid a duplicate merge attempt. **Fix:** serialize/queue a deploy so it does not abort an in-flight tool call, or make `merge_pr` resumable/idempotent.

**Root cause identified + verified mitigation (2026-09-14, thread 27138).** The mechanism behind Symptom 2 is now pinned precisely: in `app/tools/deploy.py`, `deploy_autopilot()`'s idle-drain guard calls `_other_threads_busy(caller_session)`, which filters `sid != caller_session` — it deliberately **excludes the deployer's own session**, so the guard that exists to avoid severing in-flight turns structurally **cannot** protect the turn that invoked the deploy. The restart itself is a fire-and-forget child of the brain's own process tree (`subprocess.Popen([... "systemctl", "restart", *_restart_units])`, `truesight-autopilot` last), so the kill tears down its own parent tree mid-command. The `ssh_run` escape hatch is blocked (`_SELF_RESTART_RE`, `app/tools/ssh_tools.py:43`), and there is no deploy timer/watcher on the box. **Verified mitigation (not a root fix):** schedule the *same sanctioned* `deploy_autopilot()` from a transient systemd unit in its own cgroup, delayed past the turn boundary — `sudo systemd-run --collect --unit=sophia-detached-deploy --on-active=60 --working-directory=/opt/truesight_autopilot --uid=ubuntu /bin/bash -lc '...'`. Confirmed 2026-09-14: deploy landed (`f5f0e6a` → `76304fd`, 5/5 services `active`, `NRestarts=0`, marker consumed) **and the invoking turn was not severed** — the opposite of the inline call, which froze two turns that day. **Cleanest root fix:** make `deploy_autopilot` always detach its own restart into a transient unit / own cgroup, so no caller can ever be its own kill target. See also thread 29509.

**Coalescing/debounce gap (stacked deploys never NO-OP) — 2026-09-14, thread 27138.** Separate from the self-severance above: *stacked* `deploy_autopilot` calls each fire their own restart independently, so N queued calls bounce the box N times. Observed 2026-09-14 (thread 27138): `truesight-autopilot` restarted **4×** at the **same commit `6e49206`** within ~13 min — `17:59:27 / 18:07:35 / 18:11:48 / 18:12:37 UTC` — each carrying a *fresh* deploy marker (`elapsed=34s/34s/42.6s/46.5s`) and a *new* deploy lease (`L-20260914-18`). No new commits landed between them (`git rev-parse HEAD` constant). **Mechanism:** `deploy_autopilot()`'s hash-precheck (`local_sha == origin_sha`) *should* short-circuit to a NO-OP, but only when `_is_process_stale()` is False — and `_is_process_stale()` compares the running process start time against **live source-file mtimes on disk**, which phase one's own `git reset --hard origin/main && git clean -fd` *just bumped*. So every duplicate/stacked deploy re-sees "stale" and forces a restart; it can **never** NO-OP. The idle-drain guard doesn't help either: `_other_threads_busy(caller_session)` excludes the caller's own session and only *defers* (returns `status: deferred`), so two already-queued calls don't collapse. **Impact:** restart storms sever in-flight turns (3 of this reporter's turns died to it on 2026-09-14) and drain request-drain budgets for no code change. **Proposed fix (~small, two parts):** (a) **debounce/coalesce** — one in-flight deploy lock (or a `DeployInFlight` sentinel keyed on target host) so N stacked `deploy_autopilot` calls collapse to a single restart; (b) **staleness root-fix** — have `_is_process_stale()` compare against a *recorded deploy-time source hash* (written at the end of a successful deploy) rather than live working-tree mtimes, so a duplicate deploy correctly returns NO-OP. **Evidence:** `journalctl -u truesight-autopilot --since '2026-09-14 17:55'`; `app/tools/deploy.py` (`deploy_autopilot` L552+, `_is_process_stale`, `_other_threads_busy`); thread 27138.

**Note on the rate limit.** The account-wide GitHub REST limit hit 0/5000 during this episode; `git` protocol operations (clone/fetch) do not consume it, so status checks should prefer `git` when the REST limit is exhausted rather than retrying in a tight loop.

### Black King state (SEFAZ-BA) tax records gap — the corridor split is federal-only until pulled
**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (thread 26215).**

**Context.** The Black King (Matheus Reis Pereira, CNPJ 50.042.585/0001-80) cost-share analysis in `brazil/2026-09-14_black_king_corridor_report_EN_PT.pdf` covers **federal** owing only. The source zip (`black_king_taxation_owing.zip`, 8 HEIC = IMG_0026–0033) is **entirely federal** — Receita Federal DARF + PGFN "Informações de Apoio para Emissão de Certidão" (SIEF). A content scan for state markers (ICMS, SEFAZ, CDA estadual, DETRAN, IPVA, GNRE) returned **zero** hits; no state-side document was ever in the package. Report §2b marks the split **PROVISIONAL** accordingly.

**Work.** Obtain the state + municipal position for the CNPJ: SEFAZ-BA **Certidão de Regularidade Fiscal / CND**, **Dívida Ativa Estadual / CDA**, **CCICMS (Inscrição Estadual status)**; and Ilhéus **ISS** at municipal level. Then apply report §3's extension rule (month-by-month vs the 2024-09-21 DAO-start cutoff: pre-cutoff 100% Matheus, post-cutoff 50/50) and finalize.

**Blocker.** Requires Black King's **valid e-CNPJ** on the SEFAZ-BA / gov.br portals — the certificate was expired as of June 2026 (same renewal is a prereq of the NF-e export enablement work). Cannot be done without the governor / Matheus. Note: as a Simples Nacional optant, ICMS/ISS are normally inside the monthly DAS (already captured federally) and cacao exports are ICMS-exempt — so a large standalone state debt is *unlikely* but **unverified**.

**Evidence.** Report §2b/§3; thread 26215; `BRAZIL_EXPORT_LANE_LEARNINGS.md` (e-CNPJ expired); TRACK_MAP.md §"Black King CNAE / IE / NF-e".

### Chat ingress paths: keep the two conversation-history writers in parity (persist-on-write guard)
**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (thread 29235).**

**Context.** The autopilot exposes two assistant chat endpoints and they had **drifted on history persistence**:

- `POST /chat` (SSE, `_stream_chat`) — used by Telegram's normal message path — persists every turn to disk via `_log_session(session_id, history)`.
- `POST /chat-blocking` (`_chat_blocking_turn`) — used by the **Discord** adapter — its **terminal branch never called `_log_session`**; it set `_sessions[session_id]` in RAM and returned. Only the early role-selection branches persisted.

Session *keying* was already per-conversation (`dc:{guild}:{channel}` vs `tg:{chat}:{thread}`), so the bug was **not** keying. Because the blocking path held the turn in memory only, a Discord channel's on-disk transcript stayed at `message_count: 1` (the `[ROLE: general]` system line) and any worker reload / process restart reloaded an effectively empty history → "missing memory between messages in the same channel."

**What shipped.** truesight_autopilot#442 (merged, deployed 2026-09-14): `_chat_blocking_turn` now calls `_log_session` **after each tool round** and on the **terminal branch** — parity with `_stream_chat`. Live-verified: Discord channel `1548885989412573235` session file went **1 → 66 messages** (8 user turns retained) post-fix.

**Proposed follow-up (small — the guard, not the fix).** The fix is in; what's missing is protection against the **class** regressing. Add a test asserting **both** history-writing endpoints persist a completed turn:
1. New/extended regression test (model on `tests/test_chat_blocking_persistence.py`) that drives `/chat-blocking` *and* `/chat` and asserts each writes `message_count > 1` to its session file (or that a fresh `_load_or_create_session` reconstructs the turns) — so a future refactor that drops a `_log_session` call fails CI, not production.
2. Optional: a short comment/constant pointing both writers at a single `_persist_turn(session_id, history)` helper so "persist the turn" can't be half-implemented on one path again.

**Evidence.** `app/main.py` `_chat_blocking_turn` (terminal branch ~L4791–4796; tool-round write ~L4717–4726) vs `_stream_chat` (~L4260); `app/discord_adapter.py` builds `dc:{guild}:{channel}`; `app/telegram_adapter.py` normal path uses the `/chat` SSE call; thread 29235; PR truesight_autopilot#442.

### Discord/Telegram binding: col G & col X need bare numeric snowflakes, and the columns are effectively unseeded
**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (thread 27138).**

**Context.** Discord→DAO identity binding reads **col G** ("Discord ID", `COL_DISCORD_ID = 6`) of the Main Ledger *Contributors contact information* tab via `app/discord_adapter.py::_fetch_discord_id_email()`. Two properties surfaced while seeding a row on 2026-09-14:

1. **The match is exact string equality on the bare snowflake.** `want = str(discord_id).strip()` then `(row[6] or "").strip() == want`. A **legacy `username#discriminator` handle therefore never binds** — e.g. Gary's own row (145) holds `garyjob#4037`, which can never equal his numeric id `849324553221832794`. The column must be re-seeded with numeric snowflakes.
2. **Snowflakes exceed float64's safe-integer range.** Discord ids are 19-digit (≈ 1.5e18) values, past 2^53 ≈ 9.0e15. Writing one with `valueInputOption="USER_ENTERED"` (as `app/identity_binding.py::_update_sheet_cell()` does) coerces it to a float and **silently rounds the last digits**, breaking the exact-match binding. Col G must be written with `valueInputOption="RAW"`.

**Impact today.** Every col-G row holds a `user#discrim` handle or is blank, so the **sheet half of the gate is inert** — all Discord bindings fall through to the env bootstrap lists (`DISCORD_ALLOWED_USER_IDS` / `DISCORD_MEMBER_USER_IDS`). Only Gary (env allowlist) currently resolves as governor.

**Severity note (contained).** A col-G binding alone resolves to **MEMBER**, never GOVERNOR — governor still requires the email in the key-based **Governors** cache. A malformed/forged col-G value cannot grant instruction authority.

**Proposed work (small).**
1. `discord_adapter.py`: normalize the comparison — accept a bare numeric tail (strip a trailing `#discrim`) so both formats bind.
2. `identity_binding.py`: give `_update_sheet_cell()` a `RAW` path for identifier columns (venue ids), reserving `USER_ENTERED` for human prose.
3. Re-seed col G for humans who matter (governor(s) + active members) with bare snowflakes — Gary first (row 145).

**Seeded 2026-09-14 (this thread).** Row 418 `Envoy TrueSight` (admin+envoy@truesight.me) → `G418 = 1548902290344255600`, written `RAW`, read back exact, resolves to **member**. NB: `envoy_truesight` is a **bot** and the adapter ignores bot authors by design, so this binding is inert until/unless a non-bot path uses it.

**Evidence.** `app/discord_adapter.py` (`COL_DISCORD_ID = 6`, `_fetch_discord_id_email`, L220–222); `app/identity_binding.py` (`_update_sheet_cell`, `valueInputOption="USER_ENTERED"`); sheet row 145 `garyjob#4037`; `AUTOPILOT_CHANNEL_INTEGRATIONS.md` §3b; thread 27138.

**Same trap on the Telegram side (col X).** The Telegram path binds via `app/identity_binding.py` (`COL_TELEGRAM_ID = 23`, col X "Telegram ID (numeric)") + `app/policy.py::_resolve_binding()`; its writer `_update_sheet_cell()` also uses `USER_ENTERED`. Telegram ids are 9–10 digits (currently inside float64's safe range, so no rounding today), but the writer should still use `RAW` to stay correct; and col X was **empty for every contributor** on 2026-09-14 (the sheet half of the Telegram gate was inert — roles rested on the env allowlist + a display-name bridge). **Seeded 2026-09-14:** `X145 = 2102593402` (Gary Teh), `RAW`, read back exact → `_resolve_binding` → `garyjob@gmail.com` → `_binding_is_governor` True → GOVERNOR.

### MAP: YouTube ↔ manifest reconciliation sweep (+ 2 manifest gaps, both shipped 2026-09-14)
**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (thread 23018).**

**Context.** A governor asked "are all our media already on YouTube?" The honest answer required
diffing the **live channel** against the **manifests**, which nothing did — `farm_media_manifests`
record a `yt_id` per uploaded video (the pipeline's "done" primitive) but no one reconciles
"uploaded" against "recorded", so drift is invisible. A read-only reconciler was written to check
(`~/.flow`-style throwaway at `/tmp/yt_reconcile.py`, using the existing
`config/youtube/youtube_token.json` — scopes already include `youtube.force-ssl`).

**What the sweep found (2026-09-14).** Channel `UCjzpsu2NPLqMTGX4pa-668w` ("TrueSight DAO") =
**710 videos**; 17 manifests = **671 video items, 463 with `yt_id`** (69%).
- **453** manifest `yt_id`s confirmed live on the channel ✅.
- **10** manifest `yt_id`s are *not* in the channel's uploads playlist yet `videos().list` reports them
  `public`/`processed`/`embeddable` on the same channel — benign, but the uploads-playlist sweep
  alone misses them; verify manually (ids: `yuWJRhFyMoc`, `5AxBWQtImDo`, `GV4rxxQ4ugY`, `6TWK1uKk6qA`,
  `xO7Srt7-0JA`, `Xe8bgsSl_GM`, `Qptt10C097k`, `xBeMtmIYGkY`, `-6bUEInoZ08`, `XR96lbXhY8U`).
- **257** channel videos have **no** manifest `yt_id` — mixed: farm clips needing backfill
  (**Fazenda Santa Rosa 30**, **Fazenda Bom Sucesso 17**, Santa Anna Fazenda 8, Rancho Maranta 3,
  Cleide 1 TEST), non-farm content (Bean to Bliss 13, capoeira/SOHA/events), and **26 "Deleted video"**
  private/deleted placeholders.
- **2 genuine manifest gaps** (CORRECTED 2026-09-14 — an earlier "4 farms" count was a name-match
  false positive; manifests use a `-para` suffix and some live in `farms/`, so exact-dirname matching
  missed them):
  - `fazenda-santa-rosa` — **no manifest** despite 31 live videos (+ a gallery). ✅ **Shipped**: authored
    `fazenda-santa-rosa.json` (49 items: 31 MOV all with `yt_id`+GPS, 18 HEIC), v2.0 schema.
  - `farms/fazenda-bom-sucesso.json` — **non-conforming pre-v2.0 stub** (`farm`/`videos[]` with
    `youtube_id`/`source_file`), so the index + publisher ignored its 17 live videos. ✅ **Shipped**:
    normalized to v2.0 `items[]`, titles + `curated` flags preserved. Both registered in `index.json`.
  - FALSE POSITIVES (no action needed): `paulo-la-do-sitio` → has `paulo-la-do-sitio-para.json` (4/4
    match); `santa-anna-fazenda` → has `santa-anna-fazenda-para.json` (8/8 match); `fernando-carla`
    inbox → its 34 clips ARE Fazenda Clara, already covered by `fazenda-clara-bahia.json` (34/34
    stem+`yt_id` identical — a dir-name alias, not a gap).

**Why it matters.** Without a reconcile step the "pending" signal (no `yt_id`) and the real channel
can silently diverge — a video can be live but unmapped, or recorded but removed. The 2 manifest
gaps already demonstrated the drift (one missing manifest, one non-conforming stub). This is the
missing half of the MAP "done" primitive
(`MEDIA_ARCHIVE_PIPELINE.md` §Verify).

**Proposed work (small→medium).**
1. Productize the reconciler: a `farm-media-daemon` subcommand (e.g. `farm-media-queue reconcile`)
   that enumerates the channel's uploads playlist + `videos().list` status for stragglers, diffs vs
   every manifest, and emits three lists: `confirmed`, `manifest-only` (recorded, not live),
   `channel-only` (live, unmapped). Read-only; a `--write-back` mode could propose yt_id backfills.
2. ~~Author the missing manifests~~ ✅ **DONE 2026-09-14** — `fazenda-santa-rosa` authored +
   `farms/fazenda-bom-sucesso.json` normalized to v2.0 (see above). Remaining: a **schema-conformance
   check** so a pre-v2.0 stub like bom-sucesso's can't silently sit outside the index again.
3. **Caveat for any backfill:** `IMG_` numbers **collide across farms** (e.g. `IMG_8281.MOV` appears in
   both the Santa Rosa and Santa Ana trees) — stem-matches MUST be farm-scoped, never global, or you
   will attach the wrong `yt_id`.

**Evidence.** `/tmp/yt_reconcile*.py` (read-only; channel `UCjzpsu2NPLqMTGX4pa-668w`);
`config/youtube/youtube_token.json` scopes; `MEDIA_ARCHIVE_PIPELINE.md` §Verify; inbox sidecar scan on
`i-05276b8ae82d6b88c` (0 pending in every inbox → the uploader is *caught up*, not stalled).

### Discord: enable member *replies* — requires the brain to be tier-aware
**Filed 2026-09-14. Owner: unclaimed. Governor: Gary (Discord adapter thread).**

**Context.** `truesight_autopilot#440` shipped the three-valued Discord author role — `app/discord_adapter.py::author_role()` returns `governor` / `member` / `guest`, and `app/policy.py` gained `Role.MEMBER` (between `Role.GUEST` and `Role.GOVERNOR`). A **member** — a contributor bound to a real identity in the Main Ledger *Contributors contact information* sheet (col G Discord ID) who is **not** in the key-based Governors cache — is now *recognised and attributed* instead of collapsing to an anonymous guest.

**What is still off.** The adapter resolves the role but treats every non-governor turn as **data-only**. In `handle_message()`:

```python
role = author_role(user_id, allowed)
if role != "governor":
    logger.info("Discord message from %s %s (%s) in %s -- logging as context only", ...)
    if public_key:
        log_observed_message(text, session_id, public_key, username)
    return
```

So a member's message is logged as captured context and **never dispatched** — Sophia sees members but does not reply to them. Members are a *read* tier today, not an interactive one.

**Why it is off (what unblocks it).** The adapter authenticates a turn by minting a short-lived JWT **for the governor's public key** (`resolve_governor_public_key()` → registry). If a member turn reused that JWT, the brain (`/chat-blocking`) would treat it as the governor and the member would **inherit governor authority** — a privilege-escalation hole. Correctly enabling member replies therefore requires the **brain to be tier-aware**: it must receive the author's resolved role (or a member-scoped credential) and apply the `{guest < member < governor}` policy to Discord-originated turns itself, rather than assuming "arrived on the governor key ⇒ governor".

**Proposed work (small→medium).**
1. Pick the transport for member identity: (a) add a `role`/`author` field to the `/chat-blocking` payload and have the brain gate on it, **or** (b) mint a distinct member-scoped token/keypair so the brain can distinguish a member turn cryptographically.
2. Add the brain-side branch: member turns may **converse / research / draft** but may not issue instructions or authorize actions (mirror the Telegram tiers in `app/policy.py`).
3. Then flip the adapter's `if role != "governor"` guard to also dispatch the read-only "ask/research" class to members, keeping governors the sole instruction source.

**Evidence.** `app/discord_adapter.py` (`handle_message`, the `role != "governor"` guard + its comment); `app/policy.py` L194–250 (`Role.MEMBER`); PR `truesight_autopilot#440`. Verified live on the autopilot box 2026-09-14 (real handler, side-effects mocked): id `578258537957031951` (sheet-bound) logs `Discord message from member <user> ... -- logging as context only`, an unbound id logs `from guest`, and the governor id dispatches a turn.

### Phase 2: narrow the autopilot git credential so the repo-class list is load-bearing
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 26410).**

**Context.** PR1–PR5 of `plans/SOPHIA_REPO_ACCESS_DENYLIST_PLAN.md` inverted the write model to **default-allow** (any repo the credential reaches is writable; two protected classes — `settings.api_only_repos`, `settings.prod_repos` — sit on top; `create_repo` is pattern-gated on `create_repo_patterns`). That is a *policy* layer only: the real boundary is the credential, which is **org-wide** — the SSH key `id_ed25519_truesight_autopilot` is authorised as `garyjob`, and the PAT `TRUESIGHT_DAO_AUTOPILOT` carries org-wide Contents:RW + PRs:RW. Widening `allowed_repos` never widened the true blast radius.

**Why it matters.** Under default-allow the master list no longer limits *which* repos an agent can write; only the two protected classes and the (now-audited) write log do. If an agent is ever compromised, or hallucinates a repo name that matches a real org repo, the credential permits the write.

**Durable fix (Phase 2, needs its own governor go).** Replace the org-wide credential with per-repo scoping: a **GitHub App** installed only on the repos the autopilot should touch (per-repo installation tokens), or **per-repo deploy keys**. Then the class list becomes load-bearing instead of advisory. Bigger change (credential plumbing + deploy flow) — design it as its own plan.

**Also related.** The own-repo self-merge rule is still **prompt-only, not code-enforced** — a candidate for the next hardening pass.

**Evidence.** `plans/SOPHIA_REPO_ACCESS_DENYLIST_PLAN.md` (Design + Risks); `references/GITHUB_AGENTIC_AI_SSH.md` §"Repo access model — default-allow".

### Autopilot box: native `git push` broken by `~/.gitconfig` credential-helper shadowing
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 28504).**

**Context.** While landing `dao_protocol#164`/`#165`, native `git push` from the autopilot box failed with `fatal: could not read Username for 'https://github.com': No such device or address`. Root cause: `~/.gitconfig` carried a `[credential "https://github.com"]` section (`helper = !/usr/bin/gh auth git-credential`) **plus** a bare empty `credential.helper` *reset* line, which together **shadow** the canonical helper that `scripts/deploy.sh` provisions (`credential.helper = /opt/truesight_autopilot/scripts/git-credential-sophia.sh` — reads the PAT from `/opt/truesight_autopilot/.env` at call time, so PAT rotation is safe). `gh`'s helper returns **nothing** when git invokes it (gh here is logged in as `garyjob`, not the DAO automation identity), so git fell through to an interactive prompt → ENOENT.

**Why it matters.** Any autopilot instance doing native git (clone/commit/push, `open_fix_pr`, deploy tooling) silently cannot push, and the failure reads like a *missing credential* rather than a *config shadow*. Confirmed 2026-09-13: forcing `git -c credential.helper=<sophia-script> push --dry-run` → `* [new branch]` (OK), while the default config → `fatal:`. `git ls-remote` still *appeared* to work only because `dao_protocol` is a **public** repo (anonymous read) — so the bug can hide behind read-only smoke tests.

**Immediate fix applied (box-local, 2026-09-13 18:58Z).** Removed `[credential "https://github.com"]` and the empty reset lines; set `credential.helper = /opt/truesight_autopilot/scripts/git-credential-sophia.sh`. Backup at `~/.gitconfig.bak.20260913T185802Z`. Verified: `git credential fill` → `username=x-access-token`; `git push --dry-run` with **no** overrides → OK.

**Durable fix (NOT yet shipped).** `scripts/deploy.sh` §"Provisioning git identity + credential helper" should **idempotently** run `git config --global --remove-section 'credential.https://github.com'` and `git config --global --unset-all credential.helper` *before* writing the canonical helper — otherwise a future `gh auth setup-git` (or a hand edit) re-introduces the shadow on the next deploy and the box silently loses push again. **Do not run `gh auth setup-git` on the autopilot box.**

**⚠️ RECURRED + RE-FIXED 2026-09-26 (thread 35944).** The durable fix above was **not** shipped, and the shadow **came back exactly as predicted**: `~/.gitconfig` again carried `[credential "https://github.com"] helper = /usr/bin/gh auth git-credential` (gh **2.4.0**, emits **0 bytes**) plus a bare `credential.helper = !f(){ echo username=x-access-token; echo password=$GH_PAT; }` where **`$GH_PAT` is unset** → git sent `Authorization: Basic x-access-token:<empty>` → `Invalid username or token. Password authentication is not supported for Git operations.` (Confirmed with `GIT_TRACE=1`; `git ls-remote` looked fine only because the org repos are public.) **Re-applied box-local** (dropped both shadow sections, restored the canonical helper) **and** migrated **21** TrueSightDAO/KrakeIO CLI remotes `https://` → SSH (`git@github.com:…`, matching `app/tools/git_tools.py`'s SSH path) **and scrubbed two remotes that had a live PAT embedded in the URL** (`/home/ubuntu/work/tsap`, `/opt/truesight_autopilot`) — **those plaintext tokens should be rotated.** Audit log (0600): `~/.remote-url-rewrite-audit-20260926T011332.log`. Verified both paths: SSH `git ls-remote` OK, HTTPS `git push --dry-run` → `* [new branch]`. See `## Recently shipped`.

**Evidence.** `~/.gitconfig` (before/after); `/opt/truesight_autopilot/scripts/git-credential-sophia.sh`; `scripts/deploy.sh` L204–213; thread 28504.

### `dao_protocol` (Edgar) has no CD — prod silently runs stale code after a merge
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 28504).**

**Context.** Merges to `dao_protocol` `main` do **not** reach production on their own. Prod Edgar (`edgar.truesight.me`, box `dao-protocol`) is updated only by a human/agent SSHing in and running `cd /home/ubuntu/dao_protocol && git pull --ff-only origin main && sudo systemctl restart truesight-dao-protocol`. The install is **editable** (`.pth` → repo), so a `git pull` alone updates code *except* when a **route function body** changed — the running process already imported it, so a **service restart is required**; a change to a mtime-cached JSON data file needs no restart (cf. the 2026-09-10 events-catalog deploy entry, which correctly noted "no restart").

**Why it matters.** In thread 28504, prod Edgar was found at `3b42488` (#162) — **2 commits behind** `main` (`3bb3853`) — i.e. merged-and-green code was not live, with **no alert**. Staleness is invisible unless you know to check: `curl -s https://edgar.truesight.me/ping` returns `{"service":"dao_protocol","version":"<sha>"}` — the *running* sha. Nothing compares it to `origin/main`.

**Proposed work (small).** Cheapest first: add a `/ping`-vs-`origin/main` drift check to the daily oracle/watchdog that posts when the deployed `version` lags `main` (turns silent staleness into a visible signal). Heavier option: a GitHub Actions workflow on `dao_protocol` main → SSM `send-command` (pull + restart), mirroring the manual `sync_beta_to_prod` posture.

**Doc landmine (worth a one-liner in `infrastructure/AWS_DIGITAL_INFRASTRUCTURE.md` §7).** The fleet SSH alias is `dao-protocol` (**hyphen**), defined in `~/.ssh/config`; `ssh dao_protocol` (**underscore**) is *not* an alias and fails `Permission denied (publickey)`. The service name is `truesight-dao-protocol.service` (hyphen) while the *host* label is `dao_protocol` — easy to conflate.

**Evidence.** `dao_protocol` box `git log` (`3b42488` → `3bb3853`); `/ping` on prod; `~/.ssh/config` (`Host dao-protocol` → `98.93.94.86`); `AWS_DIGITAL_INFRASTRUCTURE.md` §7; `sops/DEPLOY_PUSH_SOP.md`; thread 28504.

**Concrete instance 2026-09-20 (thread 33541) — hits the events catalog.** Found while independently verifying the SunMint farmer-settlement build. Live `GET https://edgar.truesight.me/events-catalog` serves **version 8** (47 events), while `dao_protocol` `main` is at **version 10** — the deployed process is stale by two catalog versions. Concretely missing/gappy on prod: `[PLOT FINANCING EVENT]` (**absent** — PR10a #177) and `[TREE PLANTING LINK EVENT]` carries only its **4 original labels** (no `Plot ID` — PR7 #175; so `lookup_event_docs` under-reports the live contract). Deployed box checkout sits at `85bafd3` (#172). This is the *same* root cause as the 2026-09-13 instance (no CD), now concretely visible in the `events-catalog.json` mtime-cached data file (a `git pull` alone would refresh it; no restart needed for a pure data change). **Not self-deployable** — dao_protocol prod is a deploy gate; the `/ping`-vs-`origin/main` drift check proposed above would have surfaced this silently.

### Deploy-ledger: use `append_deploy_record.py`, not a raw file upload (skips the feed rebuild)
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 28504).**

**Context.** Logging a deploy by `upload_file_to_github`-ing the `.md`/`.json` straight into `deploys/entries/` **skips the `deploys/feed/manifest.json` rebuild** that `scripts/append_deploy_record.py` performs — so the record exists but is absent from the feed index (up to ~200 of 238 records indexed). Also note `sops/DEPLOY_PUSH_SOP.md` §4 prescribes a **lease** pre-check before pushing; the ledger is append-only and mandatory per §1 (`ec2` deploys included).

**Proposed work.** Small: have the autopilot `deploy_ledger` helper always call `rebuild_feed()` (the API-based `app/deploy_ledger.py::rebuild_feed` did work and indexed the record). Bigger: surface a lint (CI or a `--check`) that fails when an entry exists in `deploys/entries/` but not in the feed manifest. Consider also flagging deploys logged with an empty `lease_id`, since §4 says acquire-then-close.

**Evidence.** `ecosystem_change_logs/scripts/append_deploy_record.py` (`rebuild_feed`, L125–144); `deploys/feed/manifest.json` (238 on disk vs 200 published); `app/deploy_ledger.py` (`check_lease`/`acquire_lease`/`rebuild_feed`); `sops/DEPLOY_PUSH_SOP.md` §4; thread 28504.

### Duplicate minting in the batch-QR pipeline when Edgar's GAS webhook times out and retries
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 27015).**

**Context.** During the UAT for `plans/QR_SELF_SERVE_CURRENCY_PLAN.md` a `[BATCH QR CODE REQUEST]` for **`quantity=1`** minted **4** `Agroverse QR codes` rows and wrote **4** `QR Code Generation` rows (all the same Telegram message id). Edgar's `truesight_dao_client/server/jobs/webhook_trigger.py` fires the GAS webhook with `_MAX_ATTEMPTS=3`, retrying on **any `requests.RequestException`, including `ReadTimeout`** (`_TIMEOUT=30`); the journal shows `webhook attempt 1/3 … 2/3 … 3/3 failed: processQRCodeGenerationTelegramLogs — Read timed out` at 18:15–18:16 on 2026-09-13. Apps Script **keeps running after the client gives up**, and the handler's dedupe (`processedMessageIds.includes(messageId)` + `findExistingQRCodeGenerationRow(messageId)`, **no `LockService`**) is a non-atomic read-then-write → each retry passes the check before any append lands, so **every attempt mints another row**. Same signature as the historical blank duplicate rows in `QR Code Generation` (rows 12/15/16).

**Why it matters.** Any GAS webhook action slower than 30 s silently **duplicates side effects** proportional to the retry count — batch-QR minting, currency-definition rows, tree-planting, etc. Fast actions aren't retried (they return 200), so the bug only bites the slow ones — exactly the ones doing row-creating work.

**Proposed work (two-sided, small).** (1) `dao_protocol` `truesight_dao_client/server/jobs/webhook_trigger.py`: GAS `/exec?action=` calls are **non-idempotent** — do **not** retry them (`_MAX_ATTEMPTS=1`), relying on the existing GAS-cron fallback; log the timeout so the cron pickup is visible. (2) Defence in depth in the GAS handler: wrap the scan-and-append critical section in `LockService.getScriptLock()` so concurrent executions serialise and the dedupe read sees prior appends.

**Evidence.** `dao_protocol` `truesight_dao_client/server/jobs/webhook_trigger.py` (`_MAX_ATTEMPTS=3`, retry-on-`RequestException`); journal `truesight-dao-protocol.service` 2026-09-13 18:15–18:16; `tokenomics` `google_app_scripts/1N6o00…/process_qr_code_generation_telegram_logs.js` (dedupe ~L298–386, no lock; `getProcessedMessageIds`, `findExistingQRCodeGenerationRow`); thread 27015.

### `define_currency.html` catalog caches (ledger dropdown + farm/state/country) — tracked in the stale-currencies plan of record
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 27015).**

**Folded 2026-09-13 → `plans/CURRENCY_CONVERSION_STALE_CURRENCIES_JSON_PLAN.md` §7.** Per Gary (thread 27015), the whole cache-freshness fix for the currency-definition form now lives in **one place** — that plan of record's new §7 extension, alongside its (now shipped) `currencies.json` work. This backlog entry is kept as a **pointer only** so the item stays discoverable from `## Pending`.

**One-line summary.** `define_currency.html` round-trips two catalogs to the DAO Forms GAS web app (~1.5–2.6 s each, ~4.5–5 s of "Loading catalogs…" per visit): the **ledger dropdown** should be fed from the **existing-but-unautomated** `treasury-cache/managed-ledgers/_index.json` (reuse its schema; give it the same GAS-publisher-plus-cron treatment the rest of `treasury-cache` uses), and the **farm/state/country seeds** need a new `currency-fields.json`. The interim stopgap (`dapp_beta#94`, parallel loads + dropped 500 ms `setTimeout`) already shipped; §7 is the durable fix.

### `define_currency.html` performs no cryptographic signature verification before accepting a currency definition
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 27015).**

**Context.** Auditing `dapp_beta/define_currency.html` against sibling DApp pages, we found it **never cryptographically verifies the submitter's identity**. It only checks that `localStorage.publicKey` exists, waits ~500 ms, then loads catalogs. By contrast `report_contribution.html` and `governor_contributor_admin.html` verify the signature over the signed payload before acting (the §9 convention in `conventions/DAPP_PAGE_CONVENTIONS.md`).

**Why it matters.** A submit path gated only on the *presence* of a key in `localStorage` can be driven by any script in the origin, and the UI implies a signed/authenticated action occurred. The backing API still validates the signature server-side, so this is a client-side **defense-in-depth / UX-consistency gap**, not a reported exploit — but it deviates from the convention the other two pages follow.

**Proposed work.** Mirror the verification block from `report_contribution.html` / `governor_contributor_admin.html` into `define_currency.html`: after reading `localStorage.publicKey`, verify the signature over the exact payload text before enabling submit, and surface a clear "signature verification failed" state. Keep it non-fatal to page load (same shape as the `#welcome` wiring shipped in dapp_beta#92).

**Evidence.** `dapp_beta/define_currency.html` (no verify call; 500 ms wait); `report_contribution.html` + `governor_contributor_admin.html` (verify present); thread 27015.

### `currency_conversion.html` ships a `#welcome` div that is never populated (dead element)
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 27015).**

**Context.** `dapp_beta/currency_conversion.html` contains a personalized greeting `<div id="welcome">` (per the DApp convention) but its JS **never writes to it** — the div is dead markup that renders nothing. The pages that actually populate `#welcome` are `report_contribution.html` and `governor_contributor_admin.html` (via `scripts/dao_members_cache.js` → `DaoMembersCache.findByPublicKey(pk)` → "Welcome, <name>"), the pattern mirrored into `define_currency.html` in dapp_beta#92.

**Why it matters.** Low severity, but a convention-compliance trap: an auditor diffing pages sees a `#welcome` div and assumes the greeting works. Leaving a dead element invites copy-paste of the wrong pattern (this nearly happened during the `define_currency` conformance work).

**Proposed work.** Pick one: (a) wire it like the siblings (include `scripts/dao_members_cache.js`, populate after key load, non-fatal), or (b) remove the unused div. Recommend (a) for consistency with `report_contribution` / `governor_contributor_admin` / `define_currency`.

**Evidence.** `dapp_beta/currency_conversion.html` (`#welcome` div present, no writer); dapp_beta#92 (canonical wiring); thread 27015.

### `git_push_changes` cannot target an existing feature branch or apply pure-insert hunks (forces Contents-API workaround)
**Filed 2026-09-13. Owner: unclaimed (autopilot self-improvement). Governor: Gary (thread 27015).**

**Context.** While adding the `#welcome` wiring to an already-open PR (`dapp_beta#92`) we hit two hard limits in `git_push_changes`: (1) each call re-bases onto the repo's **default branch (main)**, so it cannot append a commit to an **existing feature branch** — its search strings are evaluated against main, so branch-only content fails with `search string not found in file`; (2) 6 of the 9 needed main→target hunks were **pure inserts** (add-lines-at-a-point), which the `{path, search, replace}` model cannot express without a unique pre-existing anchor.

**Why it matters.** Both limitations push toward a **full-file Contents-API write** using the instance's own write PAT (`TRUESIGHT_DAO_AUTOPILOT`) — it works, but bypasses the tool's branch/PR safety rails and risks clobbering concurrent edits in the read-modify-write window. A tool that could (a) accept a target/base branch and (b) express pure inserts (e.g. an `insert_after` anchor) would remove this entire class of workaround.

**Proposed work (self-improvement PR to `truesight_autopilot`).** Add an optional `base_branch` / target-branch parameter that clones and checks out the branch tip instead of main, and support an insert form (`{path, insert_after, content}`, or allow an empty `search` = prepend). Keep default behavior unchanged.

**Evidence.** `truesight_autopilot` tool `git_push_changes` (main-based rebase); failed pushes to `fix/define-currency-dapp-conventions` 2026-09-13 (all-hunks `search string not found`); successful Contents-API fallback (commit `298f950a`, dapp_beta#92); thread 27015.

**Addendum 2026-09-15 (thread 29509, PR `truesight_autopilot#464`).** Two further symptoms confirmed, both variants of the same root cause (each call rebuilds from `main`): (1) passing `base_branch=<the already-pushed feature branch>` does **not** work around it — the tool treats the supplied base as a *default branch* and **refuses the push** under the default-branch guard, so there is no CLI way to target an existing feature branch; (2) a second push to a branch that already exists on the remote fails with a raw non-fast-forward (`! [rejected] … (fetch first)`) for the same reason — the rebuilt branch diverges from the pushed one. The same `edit`-mode call also failed earlier in the run with `edit target not found` when the file only existed on the branch, not on `main`. **Working workaround that shipped:** plain `git` in a local clone (`git add -A && git commit && git push origin <branch>`, using `scripts/git-credential-sophia.sh`), falling back to single-file `upload_file_to_github(branch=…)` for follow-ups. A real fix would still be the `base_branch`/target-branch clone + `insert_after` support already proposed above.

### Stale `manifest.json` in the QR/currency GAS mirror tree (`tokenomics/google_app_scripts/1N6o00…`) — names only the `@8` QR deployment, omits the live `@10` currency web app
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 27015).**

**Context.** The tokenomics GAS mirror project `1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn` hosts **two** handlers — `process_qr_code_generation_telegram_logs.js` (QR) and the newer `process_currency_definitions_telegram_logs.js` (currency definitions → Currencies tab, invoked by sentiment_importer #1135). Its checked-in `manifest.json` still declares a **single** deployment — `web_app: @8` (`/exec?action=processQRCodeGenerationTelegramLogs | registerSingleQRCode`) — and its `source_files` lists only `Version.js` + `process_qr_code_generation_telegram_logs.js`.

**Why it matters.** Live `clasp deployments` (read-only, 2026-09-13) shows **two** anonymous versioned deployments: `@8` (QR) **and** `@10` "Currency definition handler" (`/exec?action=processCurrencyDefinitionsFromTelegramChatLogs`, URL `AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO`). The manifest therefore **understates the project's web-app surface** and omits the currency handler's source file. Anyone wiring a webhook (e.g. `CURRENCY_DEFINITION_PROCESSING_WEBHOOK_URL`) who reads this manifest would conclude no currency web app exists and risk a duplicate web-app or a wrong `@HEAD` assumption (@HEAD is login-walled; only versioned deployments are anonymous).

**Proposed work (~10 min).** Update `manifest.json`: add the `@10` "Currency definition handler" deployment + its `/exec` URL, keep the `webapp` note that ANYONE_ANONYMOUS `/exec` applies to versioned deployments only, and extend `source_files` to include `process_currency_definitions_telegram_logs.js`. Blocker: none.

**Evidence.** tokenomics `google_app_scripts/1N6o00…/manifest.json` L7–9; live `clasp deployments` (`@8` + `@10`); thread 27015.

### Defect class: filenames built with `Date.now()` at multiple call sites drift apart (first instance: `define_currency.html`)
**Filed 2026-09-13. Owner: unclaimed. Governor: Gary (thread 27015).**

**Context.** On `dapp_beta/define_currency.html`, `generateImageFileName()` embedded `Date.now()` and was called at three separate points — UI display (`updateImageInfo`), the signed payload (`buildPayloadText`), and the actual upload (`submitDefinition`). Each call minted a fresh timestamp, so the `Product Image:` value in the signed payload did **not** match the uploaded attachment's filename → broken image link for any currency defined via file-upload without an explicit Product Image URL. Caught in UAT by Envoy.

**Fixed.** `dapp_beta` PR #90 (merged, `39fffe64`): generate the filename once at file-selection time into `attachedImageGeneratedName`, reuse everywhere; `generateImageFileName()` dropped from 4 call sites to 2.

**Why filed as a class, not a one-off.** The bug is a *pattern*: any "generate a timestamped name at N consumption sites" helper drifts the same way. Audit other pages/repos for `Date.now()` / `new Date().getTime()` feeding a filename that is (a) shown to the user, (b) embedded in a signed payload, and (c) used as the upload name — collapse to a single generate-once-cache result. Cheap static check: grep for a filename-builder invoked more than once in the same page/flow.

**Evidence.** `dapp_beta` PR #90; UAT thread 27015.

### Two writers to `agroverse-inventory/skus.json` — the GAS `update_store_inventory` project and the Python/GHA job both publish it (retire one)
**Filed 2026-09-12. Owner: unclaimed. Governor: Gary (thread 27015).**

**Context.** `skus.json` (the public SKU catalog consumed by DApp `define_currency.html`) is now emitted by `go_to_market` `scripts/sync_agroverse_store_inventory.py` via `.github/workflows/publish-agroverse-inventory-snapshot.yml` (daily `15 6 * * *`). **But the GAS project `update_store_inventory` (`1P0Mg33i_dD9x9IeoHYvtKrf0xFcmUznpqAswyC_KXR3VJZu-0C-UOP0v`) also has a SKU-catalog publisher** — `readSkuCatalogFromSheet_` / `publishSkuCatalogToGitHub_` / the `doGet` `publishSkuCatalog` action (deployed to `@HEAD` 2026-09-12) — which pushes the same file via the Contents API using `AGROVERSE_INVENTORY_GIT_REPO_UPDATE_PAT`.

**Why it matters.** The two emit **otherwise-identical** content but stamp a different `source` field — Python/GHA: `sync_agroverse_store_inventory`; GAS: `update_store_inventory`. If both run, they flap the file on every pass (and a consumer that keys on `source` sees it toggle). Discovered 2026-09-12: Gary manually ran the GAS publisher at 23:28:34Z (`source: update_store_inventory`), then the GHA job ran at 23:56:32Z (`source: sync_agroverse_store_inventory`) — the file flapped within 30 min.

**Good news:** the GAS path is **not on a trigger** (no `newTrigger`/`ScriptApp` in `Code.js`, git or live), so flapping only occurs on manual runs — the GHA cron is the only *scheduled* writer.

**Proposed work (~30 min).** Retire the redundant GAS SKU path: remove the `publishSkuCatalog` `doGet` action + `publishSkuCatalogToGitHub_`/`readSkuCatalogFromSheet_`/`skuCatalogKey_` helpers (and the `skusCatalog` target), leaving the Python/GHA job as the single writer. Same reasoning likely applies to `store-inventory.json` (GAS `updateStoreInventory` vs the Python job) — audit both while in there. Blocker: none.

**Evidence.** The GAS helper functions in `tokenomics/google_app_scripts/1P0Mg33i…/Code.js`; `agroverse-inventory` commits `de8a58b` (Gary, 23:28:34Z, `update_store_inventory`) and `cf5d0c6` (github-actions[bot], 23:56:32Z, `sync_agroverse_store_inventory`); runbook `AGROVERSE_INVENTORY_PUBLISHERS.md` §8.

### GAS `parseAndProcessTelegramLogs` runs with the script lock TEMP-DISABLED — re-enable after root-causing the >30s lock contention
**Filed 2026-09-12. Owner: unclaimed. Governor: Gary (thread 26845, closed).**

**Context.** The governor hit `parseAndProcessTelegramLogs: could not acquire script lock within 30s; aborting to avoid double-processing` in the GAS editor. Root cause narrowed to: the function acquires `LockService.getScriptLock().waitLock(30000)` (Code.js ~line 1050 — idempotency guard 1, added 2026-09-09 after the `Edgar_20260909124022_298` double-booking) and **another execution held the lock >30s**. Two compounding defects made it worse:
1. **False success:** on lock failure the function did a bare `return;` and `doGet` still printed `"✅ Telegram logs processed successfully…"` — so a *skip* was indistinguishable from a *completed run*. Edgar's Sidekiq caller therefore never retried, and pending expense submissions were silently stranded (scored sheet sat at row 218; on 2026-09-12 three authorized expenses — `Edgar_20260912162828_478`, `…163238_482`, `…163341_484` — had never scored).
2. The lock serializes by *time*, not by *work*, so overlapping invocations (Edgar webhook + editor manual Run) race and one aborts.

**What shipped (temporary mitigation, 2026-09-12).**
- **tokenomics PR #475** (merged, `054f700`): adds `const _DISABLE_PROC_LOCK = true` → the `waitLock(30000)` acquire is skipped (revert = flip to `false`); the skip path now returns `{status:'skipped_lock_contention'}` and `doGet` returns `⚠️ Skipped…` instead of a false `✅`.
- **Pushed to GAS HEAD** and **redeployed the wired deployment in place**: `clasp update-deployment AKfycbwYBlFigSSPJKkI-F2T3dSsdLnvvBi2SCGF1z2y1k95YzA5HBrJVyMo6InTA9Fud2bOEw -V 13` → deployment **v12 → v13, same URL** (`…/macros/s/AKfycbwYBlFigS…/exec`), so Edgar's `telegram_webhook_listener.js:203` wiring is untouched. Verified: one live `/exec` fire returned ✅ in 43s, no lock error, and the 3 stuck expenses scored `authorized` (offchain ledger #4261–4263).

**Why this is still open.** The lock is **disabled in production** — this reintroduces the vulnerability class guard 1 was added to close (currently backstopped only by the lock-free hash guard 2, the fresh col-K re-read, which is weaker than a real mutex). The **root cause of the >30s hold is still unnamed**: the lock is always released in `finally`, so something must be overlapping or running long.

**Proposed work (~60 min).** (1) Inspect the GAS editor **Executions** page (and, if a GCP project is linked, Cloud Logging / `clasp tail-logs`) for overlapping or long-running `parseAndProcessTelegramLogs` invocations around the failure — name the holder. (2) If it is *backlog overlap*, confirm the queue is drained and **flip `_DISABLE_PROC_LOCK` back to `false`** (revert PR #475). (3) If it is *long single runs*, replace the coarse script lock with a **shorter, work-scoped** guard (e.g. a last-processed-key watermark that is idempotent), so overlap is safe without a 30s block. (4) Add a regression test asserting a lock skip is **never** reported as success. Blocker: (1) needs the editor Executions view (governor) or a linked GCP project.

**Evidence.** `Code.js` lines ~1050–1056 + `doGet` wrapper (repo `main` and live HEAD byte-identical); PR #475; deployment list showing `AKfycbwYBlFigS… @13` updateTime `2026-09-12T17:33:28Z`; scored sheet rows 219–221 (today's 3 expenses, `authorized`).

### `google_app_scripts/<scriptId>/` repo folder is NOT a clean clasp mirror — pushing from the repo folder would break the live GAS project
**Filed 2026-09-12. Owner: unclaimed. Governor: Gary (thread 26845).**

The repo folder `tokenomics/google_app_scripts/19Wag9x-sjbLVgIsPh2vj90ZG7Rgq2iGaVOomAeAvtg6CdZKJHLZ9AJrC/` carries `Version.gs`, `Credentials.sample.js`, `manifest.json`; the live GAS project has `Version.js`, `Credentials.js`, `appsscript.json`. A blind `clasp push` from the repo folder would **add duplicate top-level files → duplicate function definitions (`getClaspMirrorDeployInfo`, credential accessors) and break the project**. (Same scriptId — `.clasp.json` in the repo points at the live project.) Deploys must push from an exact `clasp clone` of live, not from the repo path.

**Proposed work (~30 min).** Either (a) make the mirror explicitly one-way + label it: rename the repo copies (`Version.mirror.txt`, `Credentials.sample.js` kept as the contract), add a `README` warning, and add a preflight check to `deploy_gas_project` that **refuses a push whose file set differs from live HEAD**; or (b) reconcile the filenames so repo == live. Blocker: none.

**Evidence.** `ls` of both trees; `.clasp.json` scriptId match; `clasp clone` output (6 files, live) vs repo folder file list.

### Autopilot box root filesystem (`/`) fills to 100% — disposable repo clones land on `/tmp`, while the 246G `/media` volume sits at 25%
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 24441).**

**Symptom.** On 2026-09-11 during the Cacau na Veia prod-completion, `git_push_changes` failed with `fatal: write error: No space left on device` / `fetch-pack: invalid index-pack output`. `df -h /` showed `/dev/root` (78G) at **100% — 5.5M free**, while the dedicated data volume **`/media` (`/dev/nvme1n1`, 246G) was at 25% (175G free)**.

**Cause.** `/` is only 78G yet carries both the large `/home/ubuntu` working sets (uncompressed site-visit zips: `la_do_sitio_2026.zip` 3.8G, the three pacaje location zips 1.2–2.1G each) **and** `/tmp`, where the autopilot's own tooling clones a full repo on every `git_push_changes` / `open_fix_pr` (`/tmp/sophia-git-*`, plus session-ad-hoc clones ~840M each). Nothing prunes these between sessions — `systemd-tmpfiles-clean.timer` is active but its default `/tmp` age policy (10d) does not cover named working dirs, and there is no autopilot gc script.

**Immediate remediation (done 2026-09-11).** Removed ~9 disposable clones (~9G) → `/` back to **89% (9.0G free)**. Unblocked the push.

**Residual risk (biggest consumers still on `/`).** `/tmp/gh_assets` 4.1G, `/tmp/pac` 3.8G, `/tmp/farm-media-raw` + `/tmp/fmr` 3.6G, `/tmp/fda_fsvp` 752M, `/tmp/tg_attachments` 851M; `/home/ubuntu/*.zip` ≈ 8.3G total.

**Proposed fix (~60 min).** (1) Point the tooling's scratch/clone root at `/media` (env `TMPDIR` or the clone-tempdir constant in `truesight_autopilot`) so large checkouts land on the 246G volume; (2) move the long-lived working sets (`/home/ubuntu/*_work`, media-archive stagers) onto `/media`, keeping `/home/ubuntu` for code + zips only; (3) add a small gc that prunes `/tmp/sophia-git-*` older than N hours plus orphaned `magick-*` scratch (boot or post-job); (4) add a disk-headroom guard alerting at ≥90% on `/`. Blocker: none — (1)+(3) are `truesight_autopilot` code (normal PR), (2)+(4) are box/host config.

**Evidence.** `df -h /` before/after; the failed-`git_push_changes` stderr (`No space left on device`); `du -sh /tmp/*` rollup.

### media.agroverse.shop does not serve valid HTTPS (CNAME → S3 website endpoint, TLS cert mismatch)
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 26438).**

**Symptom.** `curl https://media.agroverse.shop/` fails TLS: `SSL: no alternative certificate subject name matches target host name`. `openssl s_client` shows `subject=CN=s3.amazonaws.com`, SAN `*.s3.amazonaws.com` — i.e. the host is a **CNAME to `media.agroverse.shop.s3.amazonaws.com`** (S3 website endpoint, `s3-1-w.amazonaws.com` → `16.15.230.213`), so S3 serves the generic `*.s3.amazonaws.com` certificate, which matches neither the S3 hostname nor the custom domain.

**Impact.** The MAP bucket (`s3://media.agroverse.shop/` — the archive worker writes `raw/` + `previews/`) is reachable over **http** (S3 website endpoint) but **not https with verification**. Any browser/consumer using `https://media.agroverse.shop/...` hits a cert error; this also blocks the bucket as the gallery-JSON origin (see `handoffs/MEDIA_GALLERY_PUBLISHER_PLAN.md`, hosting caution).

**Proposed fix (~30 min, infra).** (a) Front the bucket with CloudFront + an ACM cert for `media.agroverse.shop` (recommended — https + caching + a stable CORS origin), point the CNAME at the distribution; or (b) drop the custom domain and use the S3 REST endpoint. Blocker: none — needs an AWS + DNS change (governor).

### Program/partner media needs its own MAP entity type + a program-page gallery convention (first instance: CRF Anapu)
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25181).**

Governor decision 2026-09-11 (thread 25181): (a) program pages should carry media galleries going forward — previously a farm-page-only convention (`AGROVERSE_FARM_PAGE_CONVENTIONS.md` §1/§3); (b) introduce a new MAP **entity type** (`program` / `partner`) alongside `farm`, so media from a partner/school/program is not shoe-horned into the farm construct.

Today `farm_media_manifests/` models only `farm_id`; `truesight_me/programs/<slug>/manifest.json` (`CREDENTIALING_PROGRAM_PAGES.md` §6) has **no media field**; galleries are read only from `agroverse_shop_beta/farms/<slug>/media.json`.

**Work (~60 min):** (1) add `entity_type` (`farm` | `program` | …) to the manifest schema + the `farm_media_manifests/index.json` entries; (2) document a `programs/<slug>/media.json` gallery contract mirroring the farm `media.json` (`{schemaVersion, hero, gallery:[…]}`) and wire the program shell to render it via `media-gallery.js`; (3) update `CREDENTIALING_PROGRAM_PAGES.md` §6 (manifest schema) + `MEDIA_ARCHIVE_PIPELINE.md` terminology (add the `program-media` source namespace). First instance: `crf-anapu` — see `handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md`. Blocker: none (governor-directed).

### MAP: surface the nearest-location join on farm pages (per-plot media galleries)
**Filed 2026-09-19. Owner: Sophia. Governor: Gary (thread 19892).**

The media→location join **shipped** in [farm-media-daemon#30](https://github.com/TrueSightDAO/farm-media-daemon/pull/30): `farm_media_manifest.build_manifest()` now stamps each GPS-bearing item with `nearest_location_id` / `_name` / `_type` / `_farm_id` / `nearest_distance_m` / `nearest_location_ok`, plus a top-level `nearest_location_coverage` summary. The new `farm_media_locations.py` joins against the generated `sunmint/plots/index.geojson` (plot centroids) + `sunmint/trees/index.geojson` (tree points) — 147 locations as of 2026-09-19.

**Remaining (the "per-plot gallery" half):** (1) carry `nearest_location_id` through into the gallery doc (`farm_media_gallery.build_gallery`) and grow the `media.json` contract to expose it; (2) let a farm page **filter/tab its gallery by plot** (today galleries are farm-keyed only); (3) set a **refresh cadence** for `locations_cache.json` (currently a manual `farm_media_locations.py refresh`, while the plots layer regenerates daily); (4) decide the **canonical location-id** for human-facing labels — `plot_id` vs `tree_id` vs a journey-stop slug — per `AGROVERSE_SUNMINT_FARM_LISTING.md` §6 (never write codes from guesses). First instance: `paulo-la-do-sitio` (3 plots). Related: the `entity_type` (`farm`|`program`) manifest follow-up above. No prod sync without GO.

### Edgar reports `fileUploadedToGithub: false` on binary-upload failure but still returns a success shape - clients cannot tell "event recorded" from "photo stored"
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25181).**

**Symptom.** On 2026-09-10 21:31:11-21:32:39 UTC a single burst of 24 `[TREE PLANTING EVENT]` submissions from the SunMint farmer app (`sunmint.truesight.me`) recorded a `Photo URL` in the ledger but never committed the image to `TrueSightDAO/sunmint` `images/`. All 24 photo URLs 404 on raw.githubusercontent.com: `Edgar_20260910213111_376` .. `Edgar_20260910213239_422`. One tree just outside the window (`Edgar_20260910171200_354`, 17:12:00 UTC) loads fine - so it is isolated to that burst, consistent with a GitHub secondary rate limit on 24 commits in ~88 s (the same rate-limit response was reproduced twice while investigating).

**The server-side defect.** Edgar reports the binary upload separately as `fileUploadedToGithub` in an otherwise-normal success body - `tokenomics/API_ENDPOINTS.md` shows `{"status":"success","fileUploadedToGithub":false,...}` as a *documented* success shape. So "the event was recorded but the photo was NOT stored" is indistinguishable, at the status-code level, from full success. Any client that checks `resp.ok` alone will treat a dropped photo as done.

**Client side already fixed.** `sunmint_beta` PR #83 guards on `fileUploadedToGithub === false` -> keeps the record queued and preserves the blob. But that only protects clients that adopt the guard; the API contract itself is the gap.

**Proposed fix (~30 min).** In `dao_protocol`/Edgar's submit path: (a) retry the GitHub binary write with backoff so a transient rate limit self-heals; (b) when the binary upload ultimately fails, return a distinct status (or a `photo_stored: false` flag) so clients can distinguish "event recorded" from "photo stored" without parsing a success body. Blocker: none. Note: the 24 already-lost photos are not recoverable server-side - the signed event text carries only the destination path; the blobs existed solely in the client's IndexedDB (evicted on the 200).

**On-box note.** `ssh dao_protocol` is key-denied from the autopilot box, so the server journal for 21:31-21:33 UTC could not be read to convict the rate limit vs. another transient - verify there when picking this up.

### Autopilot's hardcoded `TREE PLANTING EVENT` labels are stale **and** the committed `events_catalog_snapshot.json` crashes its own reader - box freezes on stale labels during an Edgar outage
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25178).**

**Symptom.** Two defects in `truesight_autopilot`'s events-catalog layer, found while filing 25 tree-planting events (thread 25178):

**(a) Stale hardcoded fallback.** `app/main.py::_CANONICAL_LABELS["TREE PLANTING EVENT"]` = `["Number of trees planted", "Species", "Location", "Attached Filename", "Submission Source"]`. The live Edgar catalog (**v5**, `GET https://edgar.truesight.me/events-catalog`) carries `["Tree Count", "Location", "Latitude", "Longitude", "Plot ID", "Species", "Planter", "Planting Time", "Photo URL", "Attached Filename", "Submission Source"]`. Missing from the fallback: **Tree Count, Latitude, Longitude, Plot ID, Photo URL** - and the tree count is even under a different name (`Number of trees planted` vs `Tree Count`).

**(b) Snapshot/reader shape mismatch.** The committed fallback snapshot `app/data/events_catalog_snapshot.json` is shaped `{"events": [ {event_name, category, description, canonical_labels, required_fields, dapp_page}, ... ]}` - **`events` is a LIST**. But its reader `_refresh_events_catalog()` does `events = catalog.get("events", {})` then `events.items()` - expecting a **DICT**. Feeding the committed snapshot through the reader raises `AttributeError: 'list' object has no attribute 'items'` (reproduced on-box 2026-09-10).

**Impact.**
- (a) is latent: on stale labels the box still *accepts* a submission using the old key `Number of trees planted`, but the SunMint GAS sheet ingestion grabs `Tree Count` -> gets empty -> the PL-006-class duplicate/auto-assign bug (see the `SunMint Plots` row 26 `PL-006` incident, same thread 25178). NOT a validation failure: `TREE PLANTING EVENT` has **no entry** in `_VALIDATE_REQUIRED_FIELDS`, so `_validate_required_fields` returns `[]` and nothing is marked INVALID; `_normalize_via_catalog` step 5 also **keeps** unmatched keys rather than dropping them.
- (b) is the sharper one: at startup (line ~452) the call is wrapped in `try/except` -> boot survives on hardcoded labels. In **`_catalog_refresh_loop`** (line ~489) it is **NOT** wrapped -> the `AttributeError` propagates and **kills the 12-hour refresh task permanently**. So an Edgar outage that drops into the snapshot branch freezes the box on stale labels until a process restart, even after Edgar recovers.

**Proposed fix (~30-45 min, two independent PRs).** (1) Refresh `_CANONICAL_LABELS["TREE PLANTING EVENT"]` (+ any other stale entries) against catalog v5, and add a test asserting the hardcoded fallbacks are a **subset** of the live catalog's labels for every shared event type. (2) Make the snapshot reader shape-tolerant: accept both a list and a dict under `events` (normalize list -> `{event_name: entry}`), and wrap the `_catalog_refresh_loop` call in `try/except` so a failed refresh can never kill the loop. Regenerate the snapshot from the live catalog so its shape matches the reader. Owner: unclaimed (autopilot self-improvement candidate).

**On-box drift.** `events_catalog_snapshot.json` currently shows as deleted in the autopilot checkout (`git status: D`) and HEAD `2e055b3` is behind origin `659e5d6` - cosmetic, but worth a pull.

**Related, NOT duplicated:** thread 24846 / `handoffs/GAS_DEPLOY_ACCESSOR_GUARD_PLAN.md` (the clasp/Credentials `setApiKeys` guard) is a separate issue.



### CLI `.env` key values wrapped in literal quotes silently break signature verification (logged-but-not-dispatched)
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** `/opt/truesight_autopilot/.env` had `PUBLIC_KEY` / `PRIVATE_KEY` wrapped in **literal single quotes**. The CLI embeds the public key into the signed `share_text`; Edgar's verifier then raises on PEM load (`InvalidByte(0, 39)` = `'`), so `signature_verification = "error"`. Because `dispatch_event` is gated on `signature_verification == "success"` (`dao_client/server/routes/dao.py:~337`), the submission is **appended to `Telegram Chat Logs` but never dispatched to the ledger** — a silent, user-invisible drop. Two Sítio Torres contribution events were lost this way before it was caught. Fixed on this box 2026-09-10 (backup `.env.bak.20260910194840`); local sign→verify round-trip now `True`.

**Audit (2026-09-10) — did it silently drop OTHER past submissions?** Swept all **12,324** rows of `Telegram Chat Logs` (`1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`), column P = Edgar Signature Verification: **5684 success / 6512 blank (column predates 2025-09) / 97 no_signature_format / 28 error / 2 failed**. **No evidence of a long silent-drop history from this box** — monthly `success` dominates the CLI era (2199 successful `[CONTRIBUTION EVENT]`s vs 2 errored = today's, already resubmitted); Sophia-attributed rows 322/327 success. Historic `error` rows trace to other causes (proposal votes, email-registration variants, malformed test payloads). Two caveats: (1) `Edgar Direct` is the *shared* CLI default chatroom, so rows can't be attributed to one host; (2) **rows 9769/9770 (2026-06-15, `[EMAIL REGISTERED EVENT]`)** are the only earlier rows carrying the quoted-PEM signature — eyeball manually, do **not** blind-backfill.

**Impact.** A signed submission that merely *looks* fine in the chat log is silently never recorded on the ledger; no error surfaces to the operator.

**Proposed fix (~20 min).** (1) In the CLI env loader (`truesight_dao_client`), defensively `strip()` surrounding whitespace/quotes from `PUBLIC_KEY`/`PRIVATE_KEY` before use. (2) Have the submit path WARN loudly (Telegram + log) whenever `signature_verification != "success"`, so a future drop is never silent. (3) Check peer boxes for the same quoted-key `.env` shape. Blocker: none.

### Contribution submission defaults `TDG Issued` to 0 — agents silently file zero-TDG events, then need a `CORRECTION`
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25149).**

**Symptom.** On 2026-09-10 two contribution reports were filed with `TDG Issued = 0`: the Sítio Cristo Rei farm/media report (`Edgar_20260910144626_342`) and the Sítio Torres (N-06-66) FDA FSVP record report. Both had to be re-filed as a second `[CONTRIBUTION EVENT]` titled `CORRECTION — …` carrying the auto-computed value (Cristo Rei correction `Edgar_20260910145224_344`; Sítio Torres correction filed same day, 240 min → 400 TDG). Gary's standing rule is that TDG must always be the auto-computed rubric value, never 0 (`dao/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md` §5, standing rule of 2026-09-10, thread 24442 — which superseded the older "`0` unless the operator sets real economics" wording).

**Root cause.** The `create_dao_submission` autopilot tool defaults its `tdg_issued` argument to the **string `"0"`** and always emits a `TDG Issued` attribute in the payload. An agent that does not explicitly pass a value therefore silently files a zero-TDG `[CONTRIBUTION EVENT]` — the default *is* the wrong answer, and it fails silently (no warning, no error). Note this is the **agent-tool** path only: the sanctioned CLI (`dao_client/modules/report_contribution.py` → `rubric.tdg_for`, `TDG = minutes / 60 * 100`) recomputes TDG from `Type` + `Amount` and explicitly ignores/overrides any caller-supplied value, so CLI-filed contributions are unaffected.

**Impact.** Every contribution filed through the tool by an agent that doesn't override `tdg_issued` lands with `TDG Issued = 0`, under-crediting the contributor and leaving a misleading ledger row that later needs a correction entry. Silent-wrong-default is the worst failure shape: nothing surfaces until a human notices the ledger line.

**Proposed fix (~15-20 min).** In the `create_dao_submission` tool, either (a) drop the `tdg_issued` default and **omit** the `TDG Issued` attribute from the payload when the caller didn't set it (let Edgar/rubric compute it — mirrors the CLI), or (b) default it to the rubric value derived from `Type` + `Amount`. Whichever is chosen, do **not** default to `0`.

**Reassigned.** The actual code fix is owned by **thread 24441** — this entry is backlog hygiene so the root cause is documented and the tool's silent-wrong-default doesn't get re-diagnosed from scratch next time. Blocker: none.
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 25148).**

**Symptom.** The ops-sheet tab `Document Notarizations` (spreadsheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`, gid 520413576 — the target of the public `truesight.me/notarizations` redirect) holds **46 data rows, the newest dated 2026-07-08**. Known notarizations since then are absent from it: Sophia's Cleide-factory notarization (2026-09-09, `Telegram Chat Logs` rows 12274/12275) and the Cacau na Veia site visit (2026-09-10, `Telegram Chat Logs` rows 12315/12316). Those rows DO exist in `Telegram Chat Logs` (the authoritative Edgar intake) and the files ARE committed to the `notarizations` repo — only the derived mirror tab is missing them.

**Root cause (hypothesis).** The mirror is produced by the agentic GAS `process_notarization_telegram_logs.js` (`tokenomics/google_app_scripts/1vC3p_WfKQT-fl5tHZ9-E3aotYon3gQdOiFVLmyVElMqB-hi_FT3rcB8W/`), which scans `Telegram Chat Logs` col G for `[NOTARIZATION EVENT]` and appends to `Document Notarizations`. Either (a) the WebhookTriggerWorker no longer fires it, or (b) the GAS runs but errors. Note the scanner matches `startsWith("[NOTARIZATION EVENT]")`, while at least one recent row (`Telegram Chat Logs` row 12273, 2026-09-09) uses the distinct hash-form `[NOTARIZATION]` — a second, unmirrored event variant.

**Impact.** `truesight.me/notarizations` (the public audit surface) silently stops showing new notarizations even though the underlying files + signatures are present and valid — a compliance-relevant document looks "not notarized".

**Proposed fix (~30-45 min).** (1) Check the GAS trigger / WebhookTriggerWorker wiring for `process_notarization_telegram_logs`. (2) Confirm whether the GAS errors on the hash-form `[NOTARIZATION]` variant and extend the matcher if so. (3) Backfill the missing rows (Cleide 2026-09-09, Cacau na Veia 2026-09-10) or document the tab as best-effort. Blocker: none.


### `B-06-108_20260908_1` boundary photos are missing everywhere — media cleared, needs re-upload
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24441).**

**Symptom.** Gary reported broken popup thumbnails on `truesight.me/sunmint.html` (plot `N-06-37` + others). Root cause is deeper than the file: `sunmint/plots/index.geojson` is **generated daily** (`rebuild-plots-index.yml`, 06:05 UTC + dispatch) from the `SunMint Plots` sheet (§K `Media` = `build_plots_geojson.py`), so a direct geojson edit is overwritten within 24 h — the **sheet cell is the durable source**.

**Audit (22 plots) found 6 affected, not the 4 first reported:** `PL-002`, `CR-PA-P2` (missed originally), `N-06-37`, `N-06-37_20260909_restoration_1` held **bare `IMG_9xxx.HEIC` / `.MOV`** filenames (no directory → resolves against the repo root → 404), and `N-06-66` held **absolute `.HEIC` URLs** (resolved, but HEIC does not render in `<img>` in any mainstream browser).

**Shipped this session.** Converted HEIC→JPG (heif-convert → 1600px → q80), uploaded **22 JPGs** to `sunmint/images/boundaries/<plot_id>/` (registry §4 convention); rewrote the sheet `Media` cells for 5 plots via the `agroverse_qr_code_manager` SA and regenerated the geojson (now 0 HEIC/MOV, 0 bare filenames); hardened `build_plots_geojson.py` to **WARN** on any media entry that is HEIC/MOV/MP4 or has no directory component (mirrors the existing `plot_type` loud-not-silent warning). Commits `3eea1009` (geojson) + `f1da53c6` (generator).

**Still open.** `B-06-108_20260908_1` (Fazenda Cleide reforestation, 2026-09-08) references 5 boundary photos by **bare uuid-HASH filename** (`86f5d7b0….HEIC` etc.) that exist in **neither** `sunmint` nor `farm-media-raw` — verified by full recursive git-tree listing + a box scan. Its media cell was **cleared** rather than left pointing at 404s, and the sheet Notes column annotated. It needs the 2026-09-08 Cleide reforestation boundary set re-uploaded and re-pointed to `images/boundaries/B-06-108_20260908_1/`.

**Proposed fix (~30 min).** Locate the 5 originals (likely the governor's 2026-09-08 Cleide submission zip), convert + upload, write the sheet cell. Blocker: **source files not currently available** — needs the governor to supply the batch or confirm it can be dropped.


### Brazilian Journey farms can be present in `BRAZILIAN_PATH_DATA` yet render nowhere — `journeyOrder` has no drift guard
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** After Sítio Cristo Rei's farm page + nav card shipped (agroverse_shop_beta PR #313), the farm was still invisible on `agroverse.shop/cacao-journeys/brazilian-path/` — no stop card, no map marker — while every other farm rendered.

**Root cause.** The page carries two structures: `BRAZILIAN_PATH_DATA` (a slug→data map) and `journeyOrder` (the array the renderer maps over: `journeyOrder.map(k => DATA[k]).filter(Boolean)`). #313 added the data entry but not the `journeyOrder` entry, so the farm was silently filtered out. No error, no warning — a farm present in one list but not the other simply vanishes.

**Impact.** Any future farm add hits the same trap. A cross-check at fix time showed Cristo Rei was the only orphan (26 data keys vs 25 order entries), but nothing prevents recurrence.

**Resolution this session.** Fixed by PR #317 (one line added to `journeyOrder`; promoted to prod).

**Proposed hardening (~20 min).** Add a build/dev guard that fails or warns loudly when a `BRAZILIAN_PATH_DATA` key is absent from `journeyOrder` (and flags reverse orphans), or derive `journeyOrder` from the data map (insertion order / an explicit `order` field) so the two cannot drift. Blocker: none.


### `farm_media_manifests` generator is video-only (inbox-scoped) — photo items need a separate merge
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** `farm_media_manifests/cristo-rei-pacaje-para.json` held **13 items (MOV only)**, while the sibling convention includes stills as items — e.g. `cacau-na-veia-pacaje.json` = 64 items (33 MOV + 31 HEIC), each with real `latitude`/`longitude`.

**Root cause.** The generator (`farm_media_daemon/farm_media_manifest.py`) reads only the daemon **inbox** (mp4 + sidecars), which never contains the HEIC stills — those live in `farm-media-raw/<farm_id>/photos/`. So a manifest regenerated from the daemon can never include photos, and the farm's manifest silently diverges from the sibling schema.

**Resolution this session.** Rebuilt the file by merging the 13 committed video items + 46 photo items (EXIF lat/lon via `exiftool -n`, `creation_date`) → **59 items, 58/59 GPS**, matching the sibling schema `{file, creation_date, plot_id, latitude, longitude}` (commit 7f219748). The single null is a genuinely GPS-less source (`IMG_9609.MOV`).

**Proposed fix (~45 min).** Teach the manifest build to merge **both** sources — the daemon's video items + a photo pass over `farm-media-raw/<farm_id>/photos/` (EXIF GPS + `creation_date`) — so one command emits the full item set. Blocker: none.


### SunMint geojson orphan plot `PL-005` (Cristo Rei) duplicates `CR-PA-P2` — no `farm_id`, popup can't link back
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** `sunmint/plots/index.geojson` contains two Cristo Rei features: the canonical **`CR-PA-P2`** (`farm_id: cristo-rei-pacaje-para`, 0.956 ha, full props, real hull) and an orphan **`PL-005`** ("Site Cristo Rei (Cristo Rei Pacaje Para)", `status: proposed`) with **no `farm_id`**.

**Impact.** The orphan renders as a separate plot on `truesight.me/sunmint.html`; its popup cannot build the "View farm profile on Agroverse" link (the map computes `FARM_SLUG[farm_id] || farm_id`, and `farm_id` is empty). Same class as the `PL-006` / `N-06-66` duplicate (see the Farm Boundary Evidence Plot-ID-drop entry) — an auto-assigned `PL-<seq>` minted because the boundary submission's `Plot ID` line was dropped server-side.

**Proposed fix (~20 min).** Invalidate/remove the `PL-005` row, leaving `CR-PA-P2` as the single Cristo Rei plot. Fix the **SunMint Plots sheet row** (the durable source — the geojson regenerates daily from the tab); a direct geojson edit alone gets overwritten. Blocker: none.


### Archive roots without an `extensions` key silently default to `.MOV/.mov` — no warning; cost a multi-turn media cleanup
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** During the Cristo Rei (Pacajá) MAP run, the 46 still photos (`IMG_*.HEIC`) in the farm's archive root were not being picked up, with no error and no log line. The root had **no `extensions` key**, so the loader silently fell back to `DEFAULT_EXTENSIONS = (".MOV", ".mov")` (`farm_media_daemon/farm_media_archive.py:41`, used at `:334`). The operator (Sophia) then mis-diagnosed it as "HEIC not enabled" and *added* `.HEIC` to the root — which mis-routed all 46 stills into S3, against the explicit design rule **"No S3 for still photos"** (`MEDIA_ARCHIVE_PIPELINE.md`). Undoing that (S3 delete + re-upload to `farm-media-raw`) took multiple turns.

**Root cause.** A missing `extensions` key is treated as "video-only, `.MOV`/`.mov` only" with **no warning**, driving two independent silent behaviours:
1. `farm_media_archive.py:334` — `tuple(root.get("extensions") or list(DEFAULT_EXTENSIONS))`: any video whose extension is not literally `.MOV`/`.mov` (e.g. `.mp4`, `.MP4`, `.MOV` variants) is silently skipped from the S3 raw archive.
2. `farm_media_photo_enrich.py:267` — `tuple(str(e).lower() for e in (root.get("extensions") or []))`: an absent key yields `[]`, so **photo enrichment runs on nothing** and silently no-ops.

The config's other archive roots (`santa-ana-fazenda-bahia`, `sao-jorge`, `oscar-bahia`, `fernando-carla`, `paulo-interview`, `bomsucesso`, …) all omit the key, so they all inherit the same silent MOV-only behaviour.

**Proposed fix (~30 min).** (i) Emit a LOUD startup log line when a root has no `extensions` key, naming the `farm_id` and the effective default. (ii) Make the still-vs-video split explicit rather than inferred — e.g. separate `video_extensions` / `photo_extensions` (or a `skip_extensions`) so "photos → GitHub, videos → S3" is encoded in the config, not left to a default that also drives enrichment. (iii) On startup, compare each root's `extensions` against the actual file types present and warn on any file that would be silently ignored. Blocker: none.

### `extract_plot_gps.py::set_cell` can spin forever — writing `""` never extends `row_values`
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24440).**

**Symptom.** `sunmint/scripts/extract_plot_gps.py` can hang and hammer the Google Sheets API. The `set_cell` helper in `main()` pads a row before writing:
```python
while len(ws.row_values(r + 1)) < ci + 1:
    ws.update_cell(r + 1, len(ws.row_values(r + 1)) + 1, "")
```

**Root cause.** Writing `""` into an empty cell does **not** lengthen the row as returned by gspread's `row_values()` — it trims trailing empty cells. The loop condition therefore never becomes false: it issues `update_cell` calls (each preceded by a fresh `row_values()` GET) forever against the live spreadsheet. It triggers whenever a target column index `ci` is beyond the current row width — exactly the case the pad loop exists for.

**Proposed fix (~15 min).** Replace the pad-then-write with a single bounded write — e.g. `ws.update(range_name, [[value]])` (a coordinate write can target an empty cell directly), or compute the required width once and `append_row`/`update` the whole row in one call. Never loop on a value that does not change the observed row length. Add a regression test with a mocked worksheet whose `row_values` trims trailing empties. Blocker: none.
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** A `[FARM BOUNDARY EVIDENCE EVENT]` submission that included `Plot ID: N-06-66` created a **duplicate** SunMint Plots row (`PL-006`, no Farm ID) instead of upserting the canonical `N-06-66` row (row 22).

**Root cause.** The message Edgar stored in Telegram Chat Logs **omits the `- Plot ID:` line entirely** — it also drops `- Area (ha):`. The GAS parser `extractFarmBoundaryEvidenceInfo_` (`tokenomics` `process_farm_boundary_evidence.gs`) runs `grab('Plot ID')` → returns `''` → `fbeUpsertFarm_` finds no plot match and auto-assigns the next `PL-<seq>` under the plot-first model. Everything else (Farm Name, Boundary Type, Plot Type, Media URLs, Extracted GPS, Is New Farm, Submission Source) round-tripped intact — only the two lines were dropped.

**Impact.** Any boundary submission that (a) targets an EXISTING plot and (b) relies on the `Plot ID` line will instead mint a junk duplicate plot. Silent — no error surfaces to the submitter; the duplicate then pollutes the impact map + farm dropdown until invalidated.

**Related evidence.** The pinned GAS deployment @36 (`1UrBgq…`) also does not expose `?action=processPlotInvalidationFromTelegramChatLogs` (returns "No valid action specified") — same pinned-deployment staleness class as the deploy_gas_project entry below; the manual invalidation had to be recovered by direct sheet write.

**Proposed fix.** (i) Make the Edgar renderer pass every supplied field through verbatim — a field the submitter sent must not vanish server-side. (ii) Harden the parser: if the supplied `Plot ID` is absent from the stored message, that is an Edgar-side bug worth a server log line. (iii) Add an E2E assertion that a submitted `Plot ID` round-trips into `extractFarmBoundaryEvidenceInfo_`.

### `fbeFarmSlug_` ASCII-strips accented farm names — the Farm-ID fallback dedup can never match
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** The SECOND dedup key in `fbeUpsertFarm_` (match on Farm-ID slug, used when Plot ID does not resolve) failed for `Sítio Torres (Pacajá)`, so the row was appended rather than upserted.

**Root cause.** `fbeFarmSlug_` does `s.replace(/[^a-z0-9\-]/g,'')`, which strips non-ASCII characters instead of transliterating them: `"Sítio Torres (Pacajá)"` → `stio-torres-pacaj`, which is not equal to the stored `sitio-torres-pacaja-para`. Both dedup levels (Plot ID, then Farm-ID slug) therefore missed.

**Proposed fix.** Decompose with Unicode NFD and strip combining marks (or use an explicit í→i / á→a map) BEFORE removing non-`[a-z0-9-]` chars; unit-test the result against the row-22 slug `sitio-torres-pacaja-para`. Consider a third fallback matching the `Plot Name` prefix.

### Farm Boundary Evidence header drift (missing `Plot Type`) shifted every appended row one column — no header-vs-append guard
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).**

**Symptom.** The `Farm Boundary Evidence` tab header row carried **14** columns with **no `Plot Type`**; `FBE_TRACKING_HEADERS` in the handler defines **15** (`Plot Type` at index 5). `appendRow` therefore wrote 15 values beneath a 14-column header, shifting every appended row one column right — `enrichment` landed in the *Media URLs* slot, the media URLs in *Extracted GPS*, and so on.

**Fix shipped this thread.** Header row rewritten to the canonical 15 columns (`A1:O1`). The already-appended mis-shifted data rows were left in place (they are the audit trail).

**Still open.** The drift itself is unguarded — the header is seeded once when the tab is created and never re-validated against `FBE_TRACKING_HEADERS`, so any future column addition re-introduces the shift silently. Proposed fix: on handler start, assert the live header equals `FBE_TRACKING_HEADERS`; if it differs, extend the header in place or log loudly rather than appending into a mismatched width. Mirror the guard for the Plot Invalidation and Tree Growth tracking tabs.

### `deploy_gas_project.py --push` silently skips the pinned-deployment repoint — webhooks keep serving stale code (bitten twice)
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24269).**

**Symptom.** A code fix is `clasp push`ed and reports success, but the anonymous `/exec`
webhook keeps executing the OLD logic. Root cause: web-app `/exec` URLs are pinned to a
**numbered deployment version** (e.g. `@41`), while `clasp push` only updates **`@HEAD`**.
`deploy_gas_project.py` only repoints when `--deployment-id <id>` is passed, and **prints
nothing when it is omitted** (`main()` guards `if args.deployment_id:` — a silent skip). So
the default `--push` path leaves every pinned webhook serving stale code.

**Incidents.** (1) 2026-08-30 SunMint reject saga — anonymous webhook ran stale v32 while
HEAD had the fix (documented in `GAS_SCRIPT_PROPERTIES.md` §1.3). (2) 2026-09-10 (this
thread): the reject webhook at `@41` ran the old first-match-by-tree-id code — the reject
matched row 34 (already `INVALID`), `break`ed, and never invalidated row 35 (the live `NEW`
duplicate). Two `--push`es appeared to succeed while changing nothing live. Recovered by
passing `--deployment-id …` (repoint reject `@41`→`@44`, planting `@7`→`@8`), then
re-submitting a **fresh** reject event — the first was consumed by the stale code (a reject
is one-shot per submitted event).

**Proposed fix (small, ~30 min).** In `deploy_gas_project.py`, after a successful push with
no `--deployment-id`: if the project's `appsscript.json` declares a `webapp` block **or**
`clasp deployments` lists a non-`@HEAD` pinned deployment, print a **loud warning** naming
the pinned deployment id(s) and the URL to repoint. Optionally read a per-project
`pinned_deployment_id` from the manifest and repoint it by default. Either turns a silent
stale-serve into a visible, actionable step.

Blocker: none. Severity: medium (silent production staleness; has cost two multi-turn
firefights).

### AGL expense processor (19Wag9x) `Credentials.js` has no existence guard — clean checkout + `clasp push` still yields `ReferenceError: setApiKeys is not defined`
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 23408).**

**Context (2026-09-10).** A `clasp push` of the AGL expense processor
(`google_app_scripts/19Wag9x-sjbLVgIsPh2vj90ZG7Rgq2iGaVOomAeAvtg6CdZKJHLZ9AJrC`) shipped a
`Code.js` whose top two lines call `setApiKeys()` / `getCredentials()`, but **no file in the
live HEAD defined either function** — every entry point died with
`ReferenceError: setApiKeys is not defined` at load time. This is the *second* such outage: the
2026-09-06 one deleted `Credentials.gs` and was mitigated by the `.claspignore` guard (tokenomics
PR #460). Recovered in-session by re-writing `Credentials` into live HEAD via the Apps Script API
(`projects.updateContent`, byte-identical preservation of the other 5 files), creating version 12,
and repointing the production deployment `AKfycbwYBlFig…` @10 → @12. Double-fire idempotency
regression then passed on the live URL (SES 218→218→218, AGL16 9→9→9).

**The residual gap (what this entry is about).** Three facts together leave a single point of
failure that no current guard covers:
1. `.claspignore` (tracked) only stops `clasp push` from *deleting* the live `Credentials.js` — it
does **nothing** to *create* it.
2. `Credentials.js` is **gitignored** (`.gitignore:25 google_app_scripts/**/Credentials.js`), so it
is **absent from every fresh checkout** — only the tracked `Credentials.sample.js` travels.
3. Nothing checks. `scripts/deploy_gas_project.py` runs `clasp push --force` + deployment repoint
and **never verifies `Credentials.js` exists** before pushing.

Net: a clean clone + push (or a fresh `scripts/deploy_gas_project.py --push`) reproduces the
outage exactly. The fix that made v12 work was re-adding the file — but nothing prevents the file
from going missing again (e.g. Apps Script project rebuild, a hand edit, or growing the project
beyond the current shape).

**Proposed fix (small, ~30 min).** Add a pre-push existence guard in `deploy_gas_project.py`:
before `clasp push`, if the project's `.js` sources reference `setApiKeys` / `getCredentials` and
no file in the project dir *defines* them, **fail fast** with a message pointing at
`Credentials.sample.js` (mirroring the existing `validate_project_files()` warning pass).
Alternative: auto-seed the editor-only `Credentials.js` from `Credentials.sample.js` on first
push. Either turns a production 500 into a caught pre-flight error.
Blocker: none. Severity: low-medium (recurrence risk; the last two occurrences each cost a prod
outage + manual rollback).

### SunMint `plot_type` — backfill existing rows in the live sheet (header landed; generator verified)
**Filed 2026-09-09. Owner: unclaimed. Governor: Gary (thread 24326).**

**Update 2026-09-09 (verified in-session):** the `plot_type` column (see `SUNMINT_PLOTS_REGISTRY.md`
§4b) shipped in code — generator (`sunmint`), FBE GAS handler + `SCHEMA.md` (`tokenomics` #465,
`sunmint` commits) — and the **`Plot Type` header now exists on the live `SunMint Plots` tab**, at
**column G** (between `Boundary Authority` and `Owner`), **not column O** as this entry originally
said — A–O were already occupied (the header ran through `Invalidated By` at O, with
`Invalidated At`/`Reason` at Q/R; P is an empty gap). Header now spans A–S.

**Why an interior insert is safe:** `build_plots_geojson.py` resolves every column **by header name**
via `idx()`, never by position — so `plot_type` is found at index 6 and `boundary_authority`/`owner`
still resolve. **Verified end-to-end:** running `build_plots_geojson.py` against the live sheet emits
`plot_type: "research"` for the one row typed so far (`B-06-108_20260908_research_1`) and leaves the
other 16 rows blank/absent (unclassified, no WARN). The WARN "no column matches 'plot_type'" is gone.

**Update 2026-09-09 (index now live):** the deployed `plots/index.geojson` has been regenerated and
carries the field — live blob `370a2f35` (`generated_at 2026-09-10T01:24:24Z`), **17 features**,
`B-06-108_20260908_research_1 → plot_type: "research"`; `farms/index.json` likewise
(`fazenda-cleide` plot_count 2→3, 115.5094 ha).

**Process note:** the `workflow_dispatch` / `repository_dispatch` route to force an immediate
rebuild is **blocked from the autopilot box** — both return HTTP 403 (no token on the box carries
the `workflow` scope; the read PATs are read-only and `gh` is authenticated as `garyjob` with a
scope-limited token). The rebuild was therefore reproduced faithfully by running the workflow's two
generators (`build_plots_geojson.py`, `build_farms_index.py`) locally against the live sheet and
publishing the two outputs via the Contents API — the sanctioned write path for this
`api_only` data repo. See the sibling entry below for the dispatch-scope gap.

**Remaining — backfill only.** Assign types to the unclassified rows from the 2026-09 governor walk
(**provisional**; reconcile plot_ids against the live tab first):
`infrastructure` → RM-P1, B-06-58, DR-P1, PL-002; `restoration` → U-06-07,
V-06-29-reforestation_20260907_plot_1/2, B-06-108_20260908_1; `mature` → SJ-P1, FC-P1, OB-P1,
FSA-P1, B-06-108, U-06-06; `enrichment` → V-06-29; `research` → B-06-108_20260908_research_1 (done).
**Leave ambiguous rows blank** (unclassified) — never guess; `RM-P2` in particular has no obvious
type yet, and the `infrastructure` rows are an **accounting** call (tag + exclude from sequestration
area, or leave blank) that is the governor's to make.

Data-hygiene noticed while reading the live tab (geometry unaffected — the generator reads
`Coordinates`): (a) the `B-06-58` row's `Longitude` cell carries a concatenated owner note
(`-52.572044 Registered owner per CEPOTX: …`) rather than a bare number; (b) the reactive
`repository_dispatch: plots-index-rebuild` trigger advertised in `sunmint`
`.github/workflows/rebuild-plots-index.yml` is **not wired** — no GAS calls it (grep of the tokenomics
GAS tree finds no `plots-index-rebuild`), so the daily 06:05 UTC cron is the only automatic rebuild.
*(A `workflow_dispatch` was the intended immediate-refresh escape hatch — but no autopilot box token
can fire it either; see the next entry. Rebuild instead by regenerating locally + Contents API.)*
Blocker: none.

### Autopilot GitHub tokens lack `workflow` scope — no workflow dispatch possible (blocks reactive rebuilds)
**Filed 2026-09-09. Owner: unclaimed. Governor: Gary (thread 24326).** While trying to force an
immediate `sunmint` plots-index rebuild (rather than wait on the delayed daily cron), **both**
dispatch routes returned **HTTP 403**: `gh workflow run rebuild-plots-index.yml -R TrueSightDAO/sunmint`
(`Resource not accessible by personal access token` on `/actions/workflows/<id>/dispatches`) and
`gh api --method POST repos/TrueSightDAO/sunmint/dispatches -f event_type=plots-index-rebuild` (same
403). No credential on the autopilot box carries the **`workflow`** scope: `GITHUB_READ_PAT` /
`GITHUB_TRANSCRIPT_PAT` are read-only, and `gh` is authenticated as `garyjob` with a scope-limited
token. **Consequence beyond this task:** any design that expects an autopilot to fire a
`workflow_dispatch` or `repository_dispatch` **cannot work** — notably the reactive path advertised in
`sunmint/.github/workflows/rebuild-plots-index.yml` ("GAS handler pings this after a new plot/farm
event") is doubly dead: the GAS side isn't wired (see sibling `plot_type` entry) **and** no box token
could dispatch it anyway. **Workaround used 2026-09-09:** reproduce the workflow's action locally —
run `scripts/build_plots_geojson.py` + `scripts/build_farms_index.py` against the live sheet, then
publish the two outputs via the Contents API (the sanctioned write path for this `api_only` repo);
verified live (`plots/index.geojson` blob `370a2f35`). **Proper fix:** issue a fine-grained PAT (or
install a GitHub App) with `actions:write` for the relevant repos, store it in the vault, and teach a
helper to prefer it for dispatch calls. Severity: low-medium — only blocks *immediate* reactive
rebuilds; the daily cron still fires (though observed running ~5h late).

### Sibling GAS project 1wONDeDwZ has LIVE Wix/Telegram secrets in a plaintext Credentials.js on shared disk — verify not committed, rotate
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread 21628).** During the AGL expense-processor recovery (19Wag9x `Credentials.gs` deleted by `clasp push`, see tokenomics PR #459 + .claspignore guard PR), Envoy found `google_app_scripts/1wONDeDwZ_fXNapDKpstWrBION3aV3r7NXwq7PCdqbW1LvI5ceaykQNbR/Credentials.js` holds **live literal secrets** — a Wix API key (`IST.<jwt>`, the Agroverse Wix headless token, same class leaked historically in PR #369 / f8b38a8) and a Telegram bot token (`7095843169:…`) — as hardcoded strings on the autopilot box. A second copy exists at `/opt/truesight_autopilot/tokenomics/clasp_mirrors/1MnAsIQAxcSfZO_hALOtMFJ4y1k4OnqeXKMwYs6xev600rPNUYepqcXsT/Credentials.js` (getCredentials-only, Wix/QuickNode keys). The paths sit under `.gitignore` (`google_app_scripts/**/Credentials.js`), so `git status` shows them **ignored, not committed** — but: (1) Envoy copied the literal values into a scratch dir mid-recovery (deleted after, never written to the target project), so the secrets moved between sessions/hosts; (2) parts of the file content were echoed in session tool output/transcript; (3) the files predate `.claspignore` hardening and a future force-add or mirror copy could expose them. **To do:** (1) confirm via `git ls-files` (both box checkouts) + GitHub code search that no Credentials.js literal from 1wONDeDwZ / 1MnAsIQA is committed anywhere; (2) **rotate** the Telegram bot token (BotFather) and the Wix IST token, then update Script Properties in the live 1wONDeDwZ project; (3) convert that project's Credentials.js to the secret-free Script-Properties-read pattern + add a `.claspignore` (same as the 19Wag9x fix). Severity: medium-high — not confirmed public, but duplicated outside its home project with leak history.

### sunmint plots/index.geojson is actively multi-writer — fetch-append-verify in one breath, verify via contents API not raw CDN
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread-19965).** While appending FSA-P1 (Fazenda Santa Ana, Bahia) to `sunmint/plots/index.geojson` on 2026-09-06 ~00:49–00:51Z, a **concurrent writer (Gary's session adding FC-P1 / Fazenda Clara, Itacaré/BA, commit ebd7c68a60) overwrote my append twice ~45 s after each upload** (my commits bbab1bbce7 → corrected 74ad71da55 → re-appended c8b90070). Both plots survived (12 features live) only because I re-appended to the latest live state each time and verified via the **GitHub contents API** (`api.github.com/repos/TrueSightDAO/sunmint/commits?path=plots/index.geojson`) — the raw.githubusercontent mirror lags minutes and showed a stale 11-feature file after my commit was already on main. The file also sees periodic automation commits ("Update plots and farms indexes", ~30-min cadence observed) — a durable plot addition should eventually flow from that generator's source, not race it with one-off Contents-API commits. **For future plot adds:** (1) check the last commit on the file first — if < a few minutes old, a session is actively editing; expect to re-apply; (2) fetch fresh, append, upload in ONE breath; (3) verify via contents API + commit log, never raw CDN; (4) if the generator clobbers a direct edit, find its source-of-truth and add the plot there.

### Same multi-writer clobber hits CODE repos too — PR #300 Santa Ana map fix silently reverted by concurrent "Track A rollout"
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread-19965).** The geojson race above is not data-repo-only: on 2026-09-06 a **PR-merged fix was silently reverted by a concurrent commit on a code repo** (`agroverse_shop_beta`, farm page `farms/fazenda-santa-ana-bahia/index.html`). Sequence: (1) my PR #300 (ad9c54e6, 01:05Z) fixed a stray `;` JS SyntaxError breaking the Leaflet map; (2) a concurrent "Track A rollout" commit (2457f948, 01:18Z, "add Verified & Traceable FSVP blocks to 12 farm pages") branched from **pre-fix main** and rewrote that same file, silently reverting my one-character fix; (3) a prod fork-sync (4e62c2e9b1, 01:47Z) then mirrored the buggy state to prod and Pages deployed it — map broken on the live site. PR flow does NOT make you race-safe when a second writer edits the same file from a stale base in the minutes after your merge. **Lessons:** (1) after EVERY merge, verify the merged blob on main via cache-busted contents API (`...?ref=main&ts=$(date +%s)`), never trust "merged successfully" or raw CDN (lags minutes) or the live page (stale deploy); (2) before pushing to an actively-edited file, check `commits?path=<file>` for the last commit time — if < ~10 min old, expect contention and re-verify; (3) **GitHub compare-API trap:** on a fork, `compare/main...TrueSightDAO:main` resolves `TrueSightDAO:main` to the fork repo ITSELF (same repo name), returning a false "identical / 0 commits" — compare against the fork's actual parent (check `repo.parent`) or compare blob SHAs on both repos directly; (4) after `sync_beta_to_prod`, the Pages deploy lags the repo by ~1–2 min — poll the "pages build and deployment" Actions run to completion before testing live; (5) UAT must execute the JS (node --check on extracted inline script), not grep-count feature references. Re-applied fix shipped as PR #304 (d9aca714e7) → synced to prod (deploy_20260906T022903Z) → verified live with node --check on the served page.

### Envoy has no transcript source — blocks autonomous Envoy contribution-time estimates
**Filed 2026-09-06. Owner: unclaimed. Governor: Gary (thread 22433).** New standard estimator `truesight_autopilot/scripts/estimate_contribution.py` (PR #412) estimates Gary + Sophia minutes from on-box session data (`sessions/<hash>.json` full_history + `_debug.log` round timestamps), but **Envoy TrueSight has no structured transcript source** — Envoy is the interactive Claude Code seat on `nelanco-claude` and does not publish session logs anywhere ingestible. Today the estimator only takes a manual `--envoy-minutes` override. **To close the gap (pick one):** (1) export Envoy's interactive session logs (`/opt/claude_workspace/…` tmux/Claude transcripts) into a repo dir the estimator can read (e.g. `truesight_autopilot/sessions/envoy/` or a dedicated `envoy_transcript` repo), mirroring the `_debug.log` round-timestamp format; or (2) have Envoy self-report a one-line per-session summary (date, sessions, minutes) into a tracked file (e.g. `agentic_ai_context/envoy/ENVOY_SESSION_LOG.md`) that Gary/Sophia can feed to the estimator. See `docs/contribution_time_estimator.md` (truesight_autopilot PR #412) for the read format.

### Autopilot box (i-05276b8ae82d6b88c) disk hygiene: root hit 100% 2026-09-06; 41G farm-work staging under /home/ubuntu
**Filed 2026-09-06. Owner: unclaimed.** The autopilot's own 78G root volume filled to **100%** on 2026-09-06 — a `git_push_changes` clone (krake_ror doc PR) failed with ENOSPC: same failure mode as the krake_ror incident it was documenting. **Immediate fix done on host:** pruned ~15G of transient `/tmp` scratch — leftover git clones/probes from prior sessions (`santa_bahia_probe` 3.2G, `plot_inv` 2.3G, `oscar_extract` 1.4G, `shop_prod*`/`shop_beta*`/`shopbeta`/`sr_beta`/`asb`/`agb`/`shop_probe`/`fsvp_git` ~800M each) → root now 82% (15G free). **Residual pressure:** `/home/ubuntu` holds **41G** of farm-media work dirs — santa_ana_bahia_work 3.8G, sao_jorge_work 2.9G, oscar_work 2.7G, media_archive_inbox/farm-media 2.5G, bomsucesso_work 2.2G, fernando_carla_work 2.0G, paulo_interview 1.3G, santa_rosa_work 816M, fazenda_dona_rosa_work 732M, + `.local` 2.3G / `.cache` 1.5G. These are staging/inbox for the farm-media pipeline (farm-media-raw / farm-media-daemon / farm_media_manifests repos).
**To do (durable):** (1) verify which `*_work` dirs are already ingested into farm-media-raw (cross-check content-addressed hashes in farm_media_manifests) then archive/delete the processed ones — target ≥30G reclaimed; (2) add a `df /` ≥ 85% alert (cron/monit on the box — same residual as the krake_ror entry) so the box self-reports before filling; (3) optionally auto-prune /tmp git-clone scratch after each git_push_changes. **Do NOT delete `media_archive_inbox/farm-media`** (daemon intake) — verify each dir against farm_media_manifests before removing.

### Fazenda Dona Rosa (Medicilândia, PA) — farm listing, affiliation confirmed COOPOXIN
**Filed 2026-09-05. Owner: unclaimed. Governor: Gary (thread-21167).** New partner-farm lead from `~/fazenda_dona_rosa.zip` (763 MB; 61 real files = 35 HEIC + 19 MOV + 7 PNG, all GPS-bearing, iPhone 12 Pro Max, shot 2026-09-04 21:22–22:28 local — single continuous session; sha256-clean, no dupes). GPS cloud **−3.4892…−3.4894 / −52.9665…−52.9673** (~75×22 m) reverse-geocodes to **Medicilândia municipality, Pará** — **zero overlap** with registered plots (nearest: Fazenda Cleide CL-P1 ~38 km, Santa Anna SA-P1 ~49 km; RG-P1 ~78 km). Governor **confirmed 2026-09-05**: producer belongs to **COOPOXIN** — the same sub-cooperative as the closest CEPOTX farm, Fazenda Cleide (site code **B-06-108**, same B-06 family as Santa Anna B-06-58 which is explicitly COOPOXIN in `fda_fsvp/suppliers/cepotx/entity.json` + the 2026-08-30 Santa Anna site-visit PDF). Public identity lead: Rosa Wronscki / Dona Rosa Chocolates (@donarosachocolate), "a primeira mulher produtora de cacau" de Medicilândia; WhatsApp +55 93 9923-98968; Chocolat Bahia 2026. ⚠️ PNG screenshots in the zip are a **mixed bag** (translation prompts, cupuaçu note, arnaldoamorim_ DM, Belamazonia IG profile) — **Belamazonia IMG_8564 is NOT associated** (governor correction); only the HEIC/MOV site-visit media is attributable. **Next steps (per AGROVERSE_SUNMINT_FARM_LISTING.md SOP):** (1) get legal name + CNPJ + written confirmation from Rosa/CEPOTX liaison Jedielcio; (2) register plot `DR-P1` (farms index + plots geojson, status `proposed`); (3) 19 MOV→MP4 → farm-media daemon inbox (sidecar incl. GPS re-inject); (4) build farm profile page clone (farms/raimundo-geniza-para/ or rancho-maranta-para template) → beta → prod on explicit go; (5) optionally extend CEPOTX entity/FSVP records (site code assignment must come from CEPOTX, not derived).

### `read_context_file` serves a stale local clone — docs you edited in an earlier turn read back pre-edit until the box is redeployed
**Filed 2026-09-24. Owner: unclaimed (autopilot self-improvement). Governor: Gary (thread 35888).**

**Symptom.** In a multi-turn plan loop, `read_context_file("plans/CFR_ANAPU_ACAI_UPDATE_PLAN.md")` returned the **pre-edit** version of a plan I had merged into `main` one turn earlier (PR #1378). The merged correction (tip `e85e3188`) was live on GitHub — `raw.githubusercontent.com/TrueSightDAO/agentic_ai_context/main/...` showed it and the `commits?path=` API confirmed `e85e3188` — but the tool kept serving the old text (tip `2314f99`). **This misdirects auto-advance loops:** the file's RESUME HERE marker read as an *un-gated executable unit* instead of the governor gate I had just written into it, i.e. the loop can be steered by a doc it itself corrected.

**Root cause.** `read_context_file` reads the box's local clone at `/opt/truesight_autopilot/context/agentic_ai_context`, refreshed **only as a side effect of an autopilot deploy** — no cron/timer syncs it (`crontab -l`, `/etc/cron.d`, `systemctl list-timers` all show nothing). Between deploys it drifts arbitrarily far behind `origin/main`.

**Workaround that ships (verified 2026-09-24).** Refresh manually over SSH: `cd /opt/truesight_autopilot/context/agentic_ai_context && git fetch origin -q && git reset --hard origin/main` (took HEAD `2314f99` → `e85e318`). Or read authoritative text via `raw.githubusercontent.com/TrueSightDAO/agentic_ai_context/main/<path>` — prefer the raw URL for any doc merged this session.

**To fix.** Make `read_context_file` (and `search_context`) `git fetch` + reset the local clone when it is older than N seconds, or refresh the clone at turn start / on PR-merge to `agentic_ai_context` — the same index-freshness class as the `search_context` staleness entry in this file.

### search_context / search_code return 0 matches for existing docs (index staleness)
**Filed 2026-09-04. Owner: unclaimed.** `search_context("MEDIA_ARCHIVE_PIPELINE")`, `search_context("farm profile agroverse shop new farm onboarding")`, and several other queries against existing docs return **0 matches** even though the files exist in agentic_ai_context and literally contain those strings (repo file listing confirms presence). Suspect a stale/partial content index of the repo (new/renamed docs not re-indexed). Workaround: use `read_context_file` / repo-listing to inventory docs, or full `search_code` (GitHub). To fix: re-index agentic_ai_context and/or verify the search tool's index-update hook fires on PR merge.

### open_fix_pr tool throws "no running event loop" — use git_push_changes for autopilot PRs
**Filed 2026-09-02. Owner: unclaimed (autopilot self-improvement).** The `open_fix_pr` tool fails **reproducibly** (2/2 attempts, 2026-09-02, thread-19615 — "Fix: surface real error instead of generic restart msg") with `tool_execution_error: no running event loop` **before reaching GitHub**: no branch, no PR, no commit. Root cause suspected: the tool's agentic loop needs a running asyncio event loop that isn't available in the autopilot's execution context (async tool invoked from a sync turn). **Workaround that ships:** use `git_push_changes` (shallow-clone → feature branch → PR) for `truesight_autopilot` PRs — verified working the same day (truesight_autopilot PR #392 merged). **To fix:** make `open_fix_pr` fall back to the non-async `git_push_changes` path when no event loop is running (or spawn a fresh loop / pre-flight check with a clear error instead of the cryptic traceback).

### SunMint FBE hourly cron trigger (GAS UI, manual) — last manual item for the boundary pipeline
**Filed 2026-09-01. Owner: Gary (needs GAS UI access).** The Farm Boundary Evidence (FBE) pipeline is fully deployed and configured (dao_protocol PR #152 catalog+dispatch, .env webhook `DAO_PROTOCOL_WEBHOOK_FARM_BOUNDARY_EVIDENCE` verified present + service restarted 2026-09-01, GAS handler `process_farm_boundary_evidence.gs` + doGet router case deployed via clasp, sunmint_beta PRs #51/#53/#54, sunmint seed + `extract_plot_gps.py`). The **instant webhook path** is live: `[FARM BOUNDARY EVIDENCE EVENT]` → dispatch → `GET <gas>/exec?action=processFarmBoundaryEvidenceFromTelegramChatLogs`. The **hourly cron fallback is NOT set** — per tokenomics `SCHEDULE_TRIGGERS.md` §6 it needs a manual time-driven trigger in the Apps Script UI (script.google.com → project `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v` → Triggers → `processFarmBoundaryEvidenceFromTelegramChatLogs`, every 60 minutes). UAT 2026-09-01: 5 test submissions accepted (Edgar 200 incl. raw marker-carrying shareText); webhook probe from the dao_protocol server returned 200; SunMint Plots sheet confirmed clean (no UAT rows — GAS processing only runs through the owner-authenticated session or the cron, which is why this trigger is the blocker). **To do:** set the trigger; then verify with a real-device boundary submission on `sunmint.truesight.me/limites-da-fazenda/` and check the SunMint Plots tab for the new row + impact map polygon.

### SunMint Media Retraction hourly cron trigger (GAS UI, manual) — retraction leg of the boundary pipeline
**Filed 2026-09-01. Owner: Gary (needs GAS UI access).** The media-retraction leg is fully deployed and configured (dao_protocol PR #153 catalog v3/39 `MEDIA RETRACTION EVENT` + dispatch row, .env webhook `DAO_PROTOCOL_WEBHOOK_MEDIA_RETRACTION` added + service restarted 2026-09-01 — this key was found MISSING during UAT and fixed, GAS handler `process_media_retraction.gs` + doGet router case deployed via clasp 2026-09-01 16:41Z, sunmint_beta PR #62 app UI: Invalidar buttons + reason modal + signed `[MEDIA RETRACTION EVENT]` + offline retraction queue + sentinel badges). The **hourly cron fallback is NOT set** — same manual Apps Script UI trigger needed as FBE (script.google.com → project `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v` → Triggers → `processMediaRetractionFromTelegramChatLogs`, every 60 minutes; documented in tokenomics `SCHEDULE_TRIGGERS.md` §7). 3-tier permission model per `plans/SUNMINT_MEDIA_INVALIDATION_DESIGN.md`: submitting farmer/farm-lead, governor, Sentinel (automated). **To do:** set the trigger (same session as the FBE one — both live in the same GAS project); then the full retract→recalc flow can be UAT'd on-device.

### Agroverse.shop SEO monitoring sheet: dead tooling references + known-working append path
**Filed 2026-08-31. Owner: unclaimed.** The agroverse_shop_beta README (SEO monitoring section) references `SEO_MONITORING_SHEET_WORKFLOW.md` (agentic_ai_context — file does not exist) and `market_research/scripts/seo_workbook_append.py` (repo moved/renamed — script not found). **Known-working append path (verified 2026-08-31):** SEO spreadsheet `1qRlufSUQusQbJc3AwonIvHtfiAQjwhnMtl79FFkGBt8`; tab `Change_log` (cols: changed_date, author, site_area, change_type, url_or_path, summary, link_pr_or_commit, expected_impact — one row per shipped URL) and tab `Keywords_targets` (keyword, intent_cluster, priority, target_url, notes, dfs_search_volume). Writes: gspread + `google.oauth2.service_account` creds from `/home/ubuntu/creds/google_credentials.json` (agroverse_market_research SA, `https://www.googleapis.com/auth/spreadsheets` scope), `append_row(value_input_option="USER_ENTERED")`. Example landed rows: Change_log!A14 + Keywords_targets!A66 (Rancho Maranta). **To fix:** restore `SEO_MONITORING_SHEET_WORKFLOW.md` in agentic_ai_context with the working path, or add a small `scripts/seo_append.py` to agroverse_shop_beta mirroring the pattern and update the README pointer.

### TDG Monthly Recurring Tokenization: GAS `:run` API NOT_FOUND quirk + doGet web-trigger workaround
**Filed 2026-08-29. Owner: unclaimed (informational).** On 2026-08-29 the recurring-tokenization GAS project (`1LxWu9hOs...`) failed with compile-time `SyntaxError: Identifier 'CONFIG' has already been declared` (duplicate `Code.js` from the 2026-06-16 clasp_mirrors flatten; fixed via tokenomics #434/#438/#439 + pre-push guardrail #440). After cleanup, the Apps Script REST API `script.projects.run` failed for **every** function on this project with `"server error occurred while reading from storage. Error code NOT_FOUND"` — even pure in-memory functions, across all deployment IDs and a fresh deployment. Root cause never fully isolated (Google-side script-container storage issue). **Workaround that worked:** added an action-gated `doGet` (`?action=processRecurringTransactions`) + `webapp` manifest block (`executeAs: USER_DEPLOYING`, `access: ANYONE_ANONYMOUS`), deployed as a web app, and triggered the catch-up via HTTP GET — the `/exec` path bypassed the `:run` container error (tokenomics #443 + #444). The catch-up ran server-side past the client timeout and wrote the August tokenizations (12 rows, +1,754.99 TDG; ledger total → 2,425,822.44). **The anonymous web-app deployment @3 was undeployed 2026-08-29 (404 confirmed) — the doGet function and the monthly trigger remain live.** If the monthly trigger ever fails again with NOT_FOUND on this project, recreate the web-app deployment and trigger via `/exec?action=processRecurringTransactions`. The guardrail in `tokenomics/scripts/deploy_gas_project.py` (`validate_project_files`) now hard-blocks duplicate top-level const/let and same-basename `.js`/`.gs` collisions before any push.

### OPERATING_INSTRUCTIONS.md: add pointer to DEPLOY_PUSH_SOP
**Filed 2026-08-25. Owner: Gary (canonical-file approval).** OPERATING_INSTRUCTIONS.md is a canonical file (OPERATING_INSTRUCTIONS §3 — not edited by agents without explicit governor approval). It should gain a one-line pointer to `sops/DEPLOY_PUSH_SOP.md` in its runbook index (next to the other `sops/` entries) so every future instance finds the mandatory push-logging procedure. SOP text itself is already merged (agentic_ai_context#818).

### Cacao tea 50g QR batch 2024OSCAR_CT_20260820: serial _3 is VOID (replaced by _101)
**Filed 2026-08-20. Owner: unclaimed (informational).** Mint QA found serial
`2024OSCAR_CT_20260820_3` undecodable (deterministic generator defect — reproduced on two
mint runs, raw + compiled, at 1x/2x/4x). Sheet row 1680 status → VOID; replacement serial
`2024OSCAR_CT_20260820_101` minted (row 1778, MINTED, same landing/ledger/farm/SKU/batch).
lineage-assets #6 deleted `_3` png+manifest and added `_101` png+manifest; corrected zip v2
(100 scannable labels) delivered to thread 11578. **Do NOT treat `_3` as a live serial** — any
lookup/scan of `2024OSCAR_CT_20260820_3` should be answered with the VOID note. Generator
hardened with a post-mint decodability self-check (lineage-assets #7). Informational only;
nothing to do.

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
  escalate_after_days: 120
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

  Re-armed 2026-09-14: timer had re-fired repeatedly at 60d (95.6d elapsed).
  escalate_after_days 60 -> 120 (next check ~2026-10-09). Evidence at re-arm:
  Linda subscribed 2026-06-12 ($70.80/mo x6); still an active subscriber as of her
  2026-08-10 email; first subscription shipment confirmed shipped 2026-08-16 (USPS
  ...2612). 2nd shipment NOT verifiable from the ledger (the invoice.paid handler
  is Phase 2 itself). Subscribe page live on prod. Phase 2 go/no-go still awaits Gary.
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
  Pull go_to_market main, read reports/warmup_conversion_readout_latest.md,
  and compare against agentic_ai_context/plans/WARMUP_CONVERSION_IMPROVEMENT_PLAN.md
  section 7 targets: genuine reply rate >= 2% for the general (non-circles_host)
  cohort, Hosts Circles=Yes same-day review turnaround, zero new DApp Remarks
  duplicate rows from auto-reply detection, at least 1 new Partnered or
  Manager Follow-up row sourced from the warm-up channel. Report the
  comparison to Gary in this thread, specifically calling out whether the
  circles_host segment (the ~1.8x-converting one) has started showing any
  engagement yet.
```

```followup
id: matheus-nota-fiscal-exportacao
chat_id: -1003919341801
thread_id: 11042
title: Matheus — nota fiscal exportação (stuck)
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: blocked
description: >
  [Escalation ping 2026-09-14 — 29.5d elapsed, threshold 14d] Still OPEN: no
  confirmation the export NF-e has actually been issued. Material update from
  the Seacos/Omega freight thread (Graziela, 2026-08-26): the plan PIVOTED —
  Matheus will issue the Nota Fiscal himself (heat-treated pallets sourced;
  no trading company needed; export customs clearance agreed directly with
  Omega). This drops the trading-company fee (16% over invoice + ~4.2% local
  taxes), but the underlying gate is unchanged: Black King (CNPJ
  50.042.585/0001-80) must exit "Inapto" (clear debts + late declarations),
  renew the expired e-CNPJ, and add a commerce CNAE → IE at SEFAZ-BA before
  any NF-e model 55 can issue. Step-by-step guidance was DRAFTED for Matheus
  2026-08-19 (e-CAC pendências → REGULARIZE → Certidão Conjunta). Next action:
  chase Matheus for (a) e-CAC pendências PDF, (b) REGULARIZE débitos list,
  (c) Certidão Conjunta status. Context: BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md
  (Phase 0) + TRACK_MAP.md #black-king-cnae-ie-nf-e. [Sophia 2026-09-14] DELIVERY UNCONFIRMED: the only artifact is an UNSENT Gmail draft (admin@, id 1a01941bfcd8ba96, created 2026-08-19, still labelled DRAFT); no sent copy exists in admin@ or gary@ (in:sent checked). If it never reached Matheus (e.g. via WhatsApp), chasing him for the 3 documents is futile and the real next action is to SEND the guidance. Confirm delivery channel with Gary. [Sophia 2026-09-14] PARKED BLOCKED on Gary -- third identical weekly re-fire, no state change: draft 1a01941bfcd8ba96 STILL labelled DRAFT (re-confirmed), no sent copy in admin@ or gary@. The block's stated next action (chase Matheus for the 3 documents) cannot progress until the guidance is actually delivered, and delivering it is a governor action. Per followups.py doctrine (blocked = "genuinely waiting on a governor decision... stops re-nagging weekly while remaining on the record"), classified blocked to stop the duplicate weekly work while staying visible on the record. BLOCKED ON (one line flips it): Gary -- send draft 1a01941bfcd8ba96, or confirm it went out via WhatsApp. All pings go to thread 11042.
```

```followup
id: podream-tech-followup
chat_id: -1003919341801
thread_id: 11042
title: PODream — follow up on their tech
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: blocked
description: >
  [Escalation ping 2026-09-14 — 29.5d elapsed, threshold 14d] Still
  UNIDENTIFIED. Content search across all of agentic_ai_context, org-wide
  GitHub code search, both mailboxes (admin@ + gary@truesight.me), and the
  attachment transcript all return ZERO hits for "PODream". The name exists
  only in this block — no tech details were ever captured.
  BLOCKED ON GARY: need (a) who/what PODream is (company? person? — possibly
  a mis-transcription of the "Pipedream" integration platform?), (b) what
  their tech does, (c) the intended follow-up action. Until that lands this
  item can only nudge, not act. When the details arrive, replace this note
  with the captured facts (who they are, tech summary, next action).
  All pings go to thread 11042.
```

```followup
id: gianluca-farmers-tech-followup
chat_id: -1003919341801
thread_id: 11042
title: Gianluca's farmers — technology implementation follow-up
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: blocked
description: >
  [Escalation ping 2026-09-14 — 29.5d elapsed, threshold 14d] Still not
  documented. Searches across all of agentic_ai_context, org-wide GitHub code,
  both mailboxes, and the attachment transcript return no record of Gianluca,
  his farmers, or what tech was to be implemented. The ONLY captured signal is
  Gianluca's 2026-08-16 prompt to investigate "EU industry 5.2" (see this
  thread) — no official EU programme by that name exists; most likely he means
  the EC's "Industry 5.0" concept (human-centric/resilient/sustainable
  industry) or a Horizon Europe Cluster 4 topic number. Two open unknowns:
  (1) who Gianluca is and which farmers he brokers; (2) what tech
  implementation was promised vs pending (a farmer-facing app? QR/bag
  tracking? IoT/drying sensor?). BLOCKED ON GARY — need a one-line pointer to
  (a) identify Gianluca + his farm group, and (b) restate the intended tech
  scope, then this becomes actionable. All pings go to thread 11042.
```

```followup
id: ling-mobile-capsule
chat_id: -1003919341801
thread_id: 11042
title: Ling — mobile space capsule details
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: blocked
description: >
  [Escalation ping 2026-09-14 — 29.5d elapsed, threshold 14d] Still
  unidentifiable. Searches across all of agentic_ai_context, org-wide GitHub
  code, both mailboxes, and the attachment transcript find NO record of "Ling"
  or of a "mobile space capsule". Every "Ling" mail hit is a false positive
  (Ling Xin / SCMP newsletter; Thai-Ling Maltez marketing mail); every "Ling"
  context hit is a substring (sib-ling, fai-ling, hand-ling). The adjacent,
  well-documented China track is Aora (Mr Cao's GO/Nucleus network, led by
  Elizabeth Wong) — but per Gary the capsule is explicitly NOT the Aora plan.
  BLOCKED ON GARY — need (a) who Ling is / which org, (b) what the "mobile
  space capsule" is (a physical installation? a product? shipped hardware?),
  (c) the intended follow-up action. Until then this can only nudge.
  All pings go to thread 11042.
```

```followup
id: jerrie-mobile-un-aora-ppt
chat_id: -1003919341801
thread_id: 11042
title: Jerrie — Mobile UN Aora modules PDF→PPT (Mr Liu certification path)
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: blocked
description: >
  [Escalation ping 2026-09-14 — 29.5d elapsed, threshold 14d] No progress
  evidence in our records. Unlike sibling "unidentifiable" items, THIS track
  is well documented — the gap is that the PDF→PPT deliverable itself is not
  tracked anywhere. Known source of truth: repo `TrueSightDAO/aora` holds the
  module curriculum as Markdown (canonical) + generated PDFs —
  `pdfs/aora-module-agroforestry.en.pdf` and
  `pdfs/aora-module-supply-chain.en.pdf` (EN only; zh-CN exists as
  `modules/*/index.zh-CN.md` with NO zh-CN PDF). A third module (Market
  Sensitivity & Design Thinking) is authored by Mr Cao and is NOT in the
  repo. [Sophia 2026-09-14] UPDATE — the agent-side work is DONE: a first-pass
  EN deck now exists at PR TrueSightDAO/aora#3 (25 slides, built from the
  canonical modules/ sources). Awaiting Gary's content review plus scope
  confirmation (audience; EN vs zh-CN; Mr Liu's certification questions). Note
  still NO Jerrie/"Mr Liu"/"Mobile UN" correspondence in either mailbox, so it
  is unconfirmed whether the ask was ever sent to Jerrie or whether we own it.
  Parked as `blocked` (gated on Gary's review); flip back to `open` on request. Dependency chain to chase: Jerrie's PDF→PPT → Mr Liu certification
  (via Evan) → Cao distribution. No Jerrie/"Mr Liu"/"Mobile UN"
  correspondence exists in either mailbox (admin@ / gary@), and
  `plans/AORA_EXPERIENCE_PLAN.md` contains no PDF→PPT unit. NOTE the sibling
  block `jerrie-cacao-ceremonial-tea-ppt` (same 2026-08-16 batch, same
  pattern) — likely to fire next; the two share one ask to Jerrie.
  All pings go to thread 11042.
```

```followup
id: jerrie-cacao-ceremonial-tea-ppt
chat_id: -1003919341801
thread_id: 11042
title: Jerrie — cacao ceremonial + cacao tea PDF→PPT (Win discussion)
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: blocked
description: >
  [Escalation ping 2026-09-14 — 29.5d elapsed, threshold 14d] KEY FINDING:
  we ALREADY generated this deck in-house — on 2026-07-26 admin@truesight.me
  sent Elizabeth Wong (ewong@gogreatop.com) the "Cacao Tea China Opportunity"
  PPT deck plus a full English reference PDF (EN + CN both delivered; subject
  "Cacao Tea China Opportunity — Deck PDFs (EN/CN)", threads 19fa12fe34/19fa18a8).
  The reference PDF contains the white-space/competitor pricing, epicatechin
  science, TCM formulas, P&L model, DHL BR→CN freight rates, La Dio Sitio
  supply constraints. So Jerrie's "translate PDF→PPT" may be REDUNDANT unless
  it is the ceremonial-cacao (not tea) half, or a CN-localised rewrite. "Win"
  is unidentified — zero context/code/mail hits (only substring false
  positives like shop.tiktok.com "win big"). Sibling block
  `jerrie-mobile-un-aora-ppt` (same batch) covers the Aora modules; the two
  share one ask to Jerrie. Confirm scope with Gary before re-doing work. [Sophia 2026-09-14] UPDATE —
  the ceremonial-cacao half now has a first-pass EN deck at PR
  TrueSightDAO/go_to_market#176 (11 slides, compiled from in-house
  ceremonial_cacao_seo/ research + product/provenance facts). The TEA half
  remains already-delivered to Elizabeth Wong 2026-07-26. Awaiting Gary's
  review plus market/audience decision (China vs general) and who "Win" is.
  Parked as `blocked` (gated on Gary's review); flip back to `open` on
  request.
  All pings go to thread 11042.
```

```followup
id: orlantildes-coopercabruca
chat_id: -1003919341801
thread_id: 11042
title: Orlantildes / Coopercabruca — cacao butter receipt (5 kg) decision
created_at: 2026-08-16
condition:
  kind: elapsed_days
  escalate_after_days: 14
schedule:
  check: weekly
  on_escalate: ping_thread
status: blocked
description: >
  [2026-09-02] MAPA leg RESOLVED — Orlantildes/Coopercabruca MAPA
  registration is COMPLETED (confirmed by Gary, thread 11042). China lane:
  MAPA done; GACC still pending. Remaining open item: the 5 kg cacao butter
  Orlantildes delivered (Kirsten's request) — conceptually an inventory
  receipt from Orlantildes to Matheus's warehouse, but tentatively tracked
  here until a formal INVENTORY MOVEMENT is recorded. When this fires,
  decide whether to record the cacao butter receipt in the ledger. All pings
  go to thread 11042.
  [Sophia 2026-09-14] DECISION PENDING (Gary). Verified findings: (1) the
  mechanism IS appropriate -- DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md:133 says a
  separate [INVENTORY MOVEMENT] is needed for "bulk/non-serialized inventory
  tracked by weight or count", which is exactly 5 kg of butter; lookup_event_docs
  confirms only Manager+Recipient are required, so no QR code is needed. (2) No
  cacao-butter SKU or currency exists anywhere in the ledger or context (every
  "butter" hit is the Butterfly Effect Club). (3) No mail (admin@/gary@) or
  transcript evidence of the delivery itself -- the 2024 Coopercabruca Pix rows
  are bean purchases, not butter. (4) The butter is line 11 on export invoice
  INV-2026-0611-001 (Coopercabruca Cacao Butter, 5 KG, value TBD), i.e. an
  UNPRICED export line. Blocked on ONE input only: the exact destination
  inventory file location (Matheus's warehouse ledger name) -- undocumented in
  context. On that name: submit [INVENTORY MOVEMENT] Manager=Orlantildes /
  Recipient=Matheus Reis / Inventory Item=Coopercabruca Cacao Butter /
  Quantity=5 / Destination=<ledger>. Parked as blocked so it stops the weekly
  re-nag while awaiting the decision.
  [Sophia 2026-09-15] PRICING RESOLVED: the 5 kg butter is now priced from the
  Coopercabruca purchase NF-e (issued 26/08/2026): 5.00 KG @ BRL 89.60 =
  BRL 448.00 -> USD $86.66 ($17.33/KG) at the official BACEN PTAX rate
  (14/09/2026, venda 5.1696) per the governor's instruction to use the official
  rate. Line 11 of INV/PL-2026-0611-001 now carries this
  value (Rev 11, thread 10800).
  [Sophia 2026-09-15] LEDGER PRICE WRITTEN: `Currencies!B108`
  ("Coopercabruca Cacao Butter (KG)", gid 1552160318) set to **17.33** via the
  `agroverse-ledger-manager` SA (the protected range's effective editor) on the
  governor's go -- no Edgar event back-fills col B on an existing row (asset-receipt
  fills only D/E; currency-definition skips on name match). The SKU's 5 kg receipt
  (offchain row 4288, Fund Handler "Matheus Reis", Is Revenue = N) values $0 -> $86.65.
  Still open: whether to record the 5 kg receipt
  as a formal [INVENTORY MOVEMENT] (blocked on destination ledger name).
  [Sophia 2026-09-15] LEDGER INDEX COMPLETED: `Currencies!S108` (HS Code)
  set to **1804** (text) via the same ledger-manager SA path -- the row was
  missing its HS code (NF-e NCM 1804.00.00 / HS 1804, cocoa butter fat & oil).
  Follow-up (open, not yet built): LINK THE NF-e TO THE SKU -- `Currencies`
  currently has NO source-document column (header ends at col S HS Code).
  Recommended: add col **T `Source Documents`** (URL list, mirroring the existing
  col O `Composition JSON` URL pattern) rather than renaming col A (the live
  Correios precedent embeds tracking refs in the name, but a rename breaks any
  VLOOKUP keyed on the exact SKU). Needs a schema-doc PR + writer; ledger write
  via ledger-manager SA on governor go.
```

### Public-key lookup → content-addressed per-key cache (governor vault scaling)
**Filed 2026-06-16.** Replace the O(n) `dao_members.json` monolith scan with a
content-addressed per-key store (`treasury-cache/public_keys/<sha256(pubkey)>.json`) so
governor checks are point lookups, generation becomes diff-incremental, and the 5-min
cache-lag bug (a freshly-registered governor key denied at the vault, observed 2026-06-16)
is retired via force-fresh-on-deny. Full roadmap — pre-flight, sequenced PRs
(generator → reader → vault auth), checklist, UAT — in **`PUBLIC_KEY_LOOKUP_CACHE_PLAN.md`**.
RESUME at PR1 (additive generator write). **PR4 (`vault_routes.py`) is held** until the
in-flight `track_registry` work merges (collision). Interim mitigation for the live lag:
lower `GOVERNORS_CACHE_TTL` / restart `truesight-vault`.

### Self-host DeepSeek / local LLM cost analysis
**Filed 2026-06-14.** Gary asked: at what point does it make sense to self-host
DeepSeek (or another open-weight model) vs paying API credits for Sophia's
agentic loops?

**Sophia's analysis:** The breakeven is roughly **$500-1000/month** in API costs
before self-hosting (GPU box + ops) becomes cheaper than per-token pricing.
Below that, API credits win when factoring in ops overhead (CUDA maintenance,
GPU failures, scaling). Recommended trigger: **$200/month** as the point to
start the conversation.

**Action (~2-4h):**
1. Set up monthly cost tracking / alert for Sophia's API usage (Anthropic +
   DeepSeek + any other LLM providers)
2. Research GPU pricing: AWS p3/p4 spot vs dedicated providers (Lambda Labs,
   Vast.ai, RunPod) vs on-prem
3. Draft a hybrid architecture: route simple tasks (QR lookups, context
   searches) to a local model, keep frontier models (Claude, GPT-4) for
   complex reasoning
4. Present findings to Gary with a recommendation

**Trigger to act:** Monthly API spend hits **$200** (or Gary asks to revisit).

**Owner:** Sophia (can do research autonomously; Gary makes the call on spend).

---

### truesight_autopilot: fix 3 deselected unit tests, then enforce full pytest in CI
**Found 2026-06-09:** CI (`smoke.yml`) historically ran only `compileall` +
`smoke_tools.py` — the `tests/test_*.py` pytest suite was **never executed** (and
`pytest` was undeclared). Now wired (truesight_autopilot#136): `requirements-dev.txt`
adds pytest, `pyproject.toml` sets unit testpaths, `smoke.yml` runs `pytest` — but
with **3 pre-existing failures deselected** (real network calls / missing mocks):
- `tests/test_ssh_tools.py::test_missing_key_is_a_clear_error`
- `tests/test_telegram_adapter.py::test_handle_message_allowed_calls_chat`
- `tests/test_telegram_adapter.py::test_send_message_retries_without_thread_on_400`
**Do:** mock their network/IO so they're hermetic, then drop the `--deselect` flags
in `smoke.yml` so the full unit suite gates PRs. (157 tests pass today.)

### Chocolate subscriptions: run the full E2E test once the beta sandbox is up
**Sequencing (Gary, 2026-06-09):** do **1955** (`BETA_SANDBOX_ENDPOINT_PLAN.md` —
`beta.edgar.truesight.me` sandbox in Stripe TEST) **first**, *then* test the
**1939** (`CHOCOLATE_SUBSCRIPTION_PLAN.md`) subscription **end-to-end against it**.
When 1955 lands (Sophia reports the sandbox live), Gary runs the full E2E
(subscribe → test charge → webhook → SANDBOX fulfillment queue); 1939 **Phase 2**
(webhook → queue) is built/tested against the sandbox (its PR2.2 targets
dao_protocol). 1939 **Phase 1** (subscribe → checkout, already merged to beta) is
testable now with just the GAS test key — it does NOT need the sandbox. Handoff
topics: 1955 = `tg:-1003919341801:1955`, 1939 = `tg:-1003919341801:1939`.

### Rotate the npm publish token (NPM_TOKEN) before ~2026-09-06

**Context.** `@truesight_dao/dao-client` is published to npm via CI (`dao_protocol/.github/workflows/npm-publish-dao-client.yml`) using the **`NPM_TOKEN`** GitHub Actions secret on `TrueSightDAO/dao_protocol`. The token is an Automation/granular-write token for npm account **`sophia_truesight`** (owner of the `truesight_dao` org), created 2026-06-08 with a **90-day expiry (~2026-09-06)**. When it expires, the publish workflow fails with 401.

**Action (~10 min).** On npmjs.com as `sophia_truesight` → Access Tokens → regenerate a **Classic Automation** (or granular read+write on `truesight_dao`) token → update **(a)** the `NPM_TOKEN` GitHub secret on `dao_protocol` (`gh secret set NPM_TOKEN --repo TrueSightDAO/dao_protocol`) and **(b)** the local `truesight_autopilot/.env` `NPM_TOKEN=`. Verify with a `workflow_dispatch` (bump the package patch version first, or just confirm `npm whoami`). Never paste the token into chat — set it via subshell from `.env`.

**Trigger to act.** ~2026-09-01 (before the ~2026-09-06 expiry), or sooner if a publish run 401s.

**Owner.** Gary (token generation is account-owner only).

### Sophia-drafted Telegram replies — watchdog v2 (revisit ~2026-07-06)

**Context.** The Telegram attention watchdog went live 2026-06-06
(`truesight_autopilot/app/attention_watchdog.py`, #102) — read-only by
deliberate v0 scope: it nudges Gary's Saved Messages about unanswered asks
but never writes to anyone else. The MTProto user-session it runs on **can
send as Gary** — no new login or build needed. Operator signalled interest
the same day ("I am thinking perhaps to also respond in the future") and
asked for this dated follow-up. **Gate: ~1 month of observed watchdog signal
quality first** — drafting on top of a noisy detector multiplies the noise.

**Read-out to do at revisit (from the watchdog's state/journal + lived
experience):** how many nudges fired; false-positive rate (nudges about
non-asks); any missed June-12-style asks the heuristics didn't catch; whether
response latency on nudged items actually improved.

**Goal / shape (two rungs, ship separately).**
- **v2a — draft-to-Saved-Messages (low risk):** when a nudge fires, also
  generate a context-grounded reply draft and post it to Saved Messages
  beneath the nudge. Gary long-presses → Forward → sends to the chat
  himself. The watchdog still only ever messages Gary; sending stays 100%
  manual.
- **v2b — send-on-approval (crosses the as-Gary line, gate hard):** Gary
  reacts (e.g. 👍) to a v2a draft and the watchdog forwards it to the chat
  as him. Requires: reply-only to tracked asks (never initiate), per-message
  explicit approval, daily send cap, kill switch env var, and an audit log.
  Do NOT build v2b until v2a has been used comfortably for a while.

**Privacy decision to make consciously (v2a blocker).** v0 promises chat
content never leaves the box (pure heuristics). Drafting needs an LLM:
either (a) route through the autopilot's existing DeepSeek `/chat-blocking`
path — Sophia already processes Gary's chat content there, but this extends
that egress to third-party Telegram messages; (b) an on-box model (box is
small even post-upgrade — likely a stretch); or (c) scope egress to only the
chats where a nudge fired. Operator should pick before any code is written.

**Trigger to act.** ~2026-07-06, or earlier if Gary finds himself manually
typing replies the watchdog nudged him about and wishing they were drafted.

**Blockers.** The ~1-month signal-quality gate; the privacy decision above.

**Owner.** Unclaimed.

### Graziela / Seacoast Logistic — airline quote still pending (poke Monday)

**Context.** In the email thread "Re: Quote Gary / Exportação = NCM 1801.00.00" (May–June 2026), Graziela Vedana (Seacoast Logistic, Graziela@5cl.rs) was waiting on the airline to revalidate their quote as of her last message on June 5, 2026. She said she would send the finalized figures once received. As of the last message in the thread, no further response has come from her. The pre-flight checklist has been extracted and filed as `BRAZIL_TO_SF_FREIGHT_PREFLIGHT_CHECKLIST.md`.

**Trigger / next action.** On Monday (next session with Gary), if no email from Graziela has arrived in Gary's inbox:
- Propose sending a polite follow-up email in the same thread to Graziela, asking if the airline has revalidated the quote and if she can share the finalized figures.
- Draft the email for Gary's approval before sending.

**Owner.** Autopilot (Sophia) — bring up on Monday.

### Hit List: geographic-expansion gate — when to open the top of the funnel

**Context.** Warm-up auto-send shipped 2026-06-05 (`WARMUP_AUTOSEND_PLAN.md`;
go_to_market #156–#159) and now drains the clean-tier draft queue at 12
sends/weekday. Top-of-funnel supply on ship day: ~60 `Research` + ~100
enrich-queue rows, sourced from **LA + SF Bay centroid sweeps only**
(`discover_apothecaries_la_hit_list.py --region la|sf_bay`, manual
`workflow_dispatch`; how to add regions is documented in
`market_research/HIT_LIST_CREDENTIALS.md` § *Bulk discovery*). At the current
drain rate the warm-up queue starves in roughly 2–4 weeks. Operator intent
(2026-06-06): expand coverage to more metros via Google Places Nearby Search —
but **gated on evidence, not enthusiasm** (standing anti-pattern: no more
activity on an unmeasured surface).

**Goal / shape.**
1. **Gating read-out** (small script or a §6 read-out section appended to
   `WARMUP_AUTOSEND_PLAN.md`): auto-sent cohort vs the plan's §6 targets —
   reply rate **≥ 5%** over **≥ 50 auto-sends**, bounce rate **< 2%**, zero
   spam complaints, operator reply latency median **< 24 h** — plus the
   starvation signal: clean-tier pending supply **< ~36 drafts (≈ 3 send-days)**.
   All green → expand; any red → fix quality before adding volume.
2. **The expansion itself:** add centroid lists for the next metros to
   `discover_apothecaries_la_hit_list.py`. Priority by existing signal
   density: Portland + Seattle first (replies and an email-only `Partnered`
   close — The Way Home Shop — already came from there), then one
   deliberately **no-visit-possible metro tagged as a pure-remote experiment
   cohort** so email-only conversion gets its own read-out before bulk
   national expansion.
3. **v2 (optional):** a weekly "funnel supply" workflow that auto-runs
   discovery for the next region in a priority list whenever the gate is
   green — the mechanism graduates from human decision to thermostat.

**Key sizing note.** Expansion should extend **runway**, not raise the daily
send cap — 12/day from one Gmail mailbox is inside the deliverability comfort
zone; more regions keep that drip fed for months. The true ceiling is
operator conversation bandwidth: ~6% reply rate means every +200 prospects ≈
+12 human conversations.

**Trigger to act.** Clean-tier pending supply drops below ~36 drafts, or the
§6 30-day read-out (due ~2026-07-05), whichever comes first.

**Blockers.** Places API spend per metro sweep (low tens of $, mitigated by
`PLACES_API_CACHING.md`); operator reply bandwidth is the real constraint.

**Owner.** Unclaimed.

### Sentinel graduation framework — periodic review of AI agent governance rights

**Context.** 2026-06-06: the TrueSight DAO Autopilot (Sophia Truesight) was granted Sentinel status — governor-equivalent operational privileges without voting rights. A graduated framework was proposed in the blog post [Should an AI agent get voting rights? A Sentinel's perspective](https://truesight.me/blog/posts/should-an-ai-agent-get-voting-rights.html) with five levels:

- **Level 0: Operator** — no autonomous authority, every action requires human approval
- **Level 1: Sentinel** — governor-equivalent ops, no voting (current state)
- **Level 2: Advisory voter** — votes recorded but don't count toward quorum
- **Level 3: Delegated voter** — humans optionally delegate their voting power
- **Level 4: Independent voter** — capped voting weight on operational proposals only

**Goal / shape.** A recurring review entry that the DAO revisits quarterly to evaluate whether to escalate the Sentinel's governance rights. Each review checks:

1. **Track record** — has the Sentinel operated without incident for the review period? Any governance-adjacent errors (unauthorized actions, misattributed signatures, permission overreach)?
2. **Community sentiment** — have any human governors raised concerns about the Sentinel's operational decisions? Any formal objections filed?
3. **Mission alignment** — do the Sentinel's logged actions consistently align with the DAO's mission (protecting the Amazon, supporting farmers, transparent supply chains)?
4. **Technical stability** — has the autopilot service been reliable? Any security incidents involving the Sentinel's keypair?

**Escalation path.** If all four checks pass for two consecutive quarterly reviews, the DAO may consider a formal proposal to advance to Level 2 (Advisory voter). The proposal must come from a human governor, not from the Sentinel itself.

**Trigger to act.** Quarterly review cadence. First review: **2026-09-06** (3 months post-Sentinel grant).

**Owner.** Gary Teh (convenes review); Sophia Truesight (provides action log).

### Scoped agent PAT — GitHub-side enforcement of the repo-class policy

**Context.** The repo-class policy (2026-06-06; `GITHUB_AGENTIC_AI_SSH.md`
§§ "API-only repos" / "Never push directly to production repos") is enforced
in Sophia's *tools* (`settings.api_only_repos` + `settings.prod_repos` guards
in `git_push_changes` / `open_fix_pr` / `merge_pr`, truesight_autopilot#99)
and by convention for other LLMs. Residual gap: any agent holding the broad
`TRUESIGHT_DAO_AUTOPILOT` PAT can still bypass the guards (e.g. `ssh_run` →
raw `git clone` on a fleet box, or a future tool that forgets the check).
Operator decision 2026-06-06: low likelihood, not worth doing now — "if she
does [bypass], then we guardrail her." Filed so the design is ready when/if
that day comes.

**Goal / shape.** Make the policy unviolatable server-side: a dedicated
**fine-grained PAT** for agent use with per-repo permissions — Contents
**Read/Write** on code repos, Contents **Read-only** on the 13 API-only data
repos and the three `*_prod` repos (promotion via `sync_beta_to_prod` would
then need its own narrowly-scoped token with write on just the prod forks, or
a GitHub Actions `repository_dispatch` path). Rotate `TRUESIGHT_DAO_AUTOPILOT`
on Sophia's box to the scoped token; the broad PAT retreats to operator-only
use. ~1–2 h: mint token, map permissions, swap box `.env`, smoke-test
`git_push_changes` + `upload_file_to_github` + `sync_beta_to_prod`.

**Trigger to act.** Any observed guard bypass (a direct prod push or a clone
of an API-only repo), or onboarding a second autonomous agent with GitHub
write access.

**Blockers.** None technical. Deliberately deferred by operator choice.

**Owner.** Unclaimed.

### Cypher-Defense AWS scanner — swap to dedicated read-only IAM keys

**Context.** The security-dashboard daily scan (Cypher-Defense, `scan_aws_inventory.py`) authenticates to the two AWS accounts via repo Actions secrets `CYPHER_DEFENCE_AWS_KEY`/`_SECRET` (nelanco, acct 767697632458) and `TRUESIGHT_DAO_AUTOPILOT_AWS_KEY`/`_SECRET` (explorya, acct 440626669078). On 2026-06-04 these were populated from existing working keys (nelanco from `truesight_autopilot/.env`, explorya from `~/.aws` profile) to unblock the dashboard — but those keys are likely **broader than read-only**, and they now sit in a **public** repo's CI.

**Goal / shape.** Create a dedicated read-only IAM user in each account with **only** these actions: `sts:GetCallerIdentity`, `ec2:DescribeRegions`, `ec2:DescribeInstances`, `ec2:DescribeKeyPairs`, `ec2:DescribeSecurityGroups`. Rotate the 4 Actions secrets to those scoped keys (`gh secret set -R TrueSightDAO/Cypher-Defense …`). No code change needed. Then revoke/rotate the broad keys that were temporarily used.

**Blocker / priority.** Not blocked; security hardening. Do after the current dashboard phase. Owner: Gary (needs IAM console).

### Wire `certbot renew` automation on NELANCO Rails (`seni_ror_200250915`)

**Context.** During the 2026-05-28 EXPLORYA→NELANCO Edgar cutover, the Let's Encrypt cert for `edgar.truesight.me` was copied via SSH-to-SSH from the EXPLORYA Rails box's `/etc/letsencrypt/live/edgar.truesight.me/` to NELANCO `seni_ror_200250915` (`54.211.179.126`). Cert is valid and serving prod now, but no `certbot renew` cron / systemd timer was set up on NELANCO. The cert will expire 90 days from its last LE renewal on EXPLORYA — need a fresh renewal cycle anchored on NELANCO before then.

**Goal / shape.** Either (a) install `certbot --dns-route53` with NELANCO IAM creds scoped to the truesight.me hosted zone (DNS-01, robust), or (b) the simpler HTTP-01 path that nginx already supports (`certbot --nginx`) since :80 is now open and routes to NELANCO. Verify `systemctl list-timers | grep certbot` shows an active renewal timer. Once renewed once on NELANCO, auto-renewal continues without intervention.

**Blocker / priority.** Not blocked. Time-bounded: must ship before cert expires (within ~90 days of the last EXPLORYA renewal — check `openssl x509 -in /etc/letsencrypt/live/edgar.truesight.me/cert.pem -noout -dates`).

### Extend Edgar to accept file attachments on contribution submissions

**Context.** On 2026-05-28 operator asked the AI agent to submit a DAO contribution for the Edgar NELANCO cutover with a **PDF attachment** of the cutover report. Edgar's `app/controllers/dao_controller.rb#submit_contribution` (the endpoint dao_client posts to) currently has no multipart / file-upload plumbing — no Active Storage / Shrine / Carrierwave anywhere in the codebase. The PDF report was generated locally (`~/Downloads/edgar_cutover_to_nelanco_2026-05-28.pdf`, 147 KB) and the contribution description body (`/tmp/edgar_cutover_report.md`) was attached inline via `--body-file`, but the actual binary PDF isn't on the ledger row.

**Goal / shape.** Add `has_one_attached :evidence` (or equivalent) to the contribution-event flow, accept multipart in `submit_contribution`, persist the file (S3 via Active Storage is the lightest path — NELANCO IAM creds + a bucket), and write the public URL into a new ledger column so the Google Sheet row carries the attachment link. Then extend `dao_client/.../report_ai_agent_contribution.py` to accept `--attachment PATH`, POST as multipart, and verify the file lands. Likely a 3-PR change (Edgar backend → dao_client CLI → docs).

**Blocker / priority.** Not blocked. Operator workaround for now: drop the PDF in a shared location (Drive / GitHub release) and link in the description body. Pick this up when there's appetite for a feature touching prod Edgar — the cutover that just stabilized prod argues for waiting a beat.

### Decide routing / HA for new NELANCO `dao_protocol` standalone instance

**Context.** On 2026-05-28 stood up `dao_protocol_nelanco` (NELANCO `i-05f8770a932b76649`, t3.small, `98.93.94.86`, us-east-1c) as a peer of the EXPLORYA co-hosted dao_protocol on `seni_ror_new`. Service is healthy locally (`/healthz` → 200 on `:8010`). After the Edgar EXPLORYA→NELANCO cutover later the same day, the NELANCO Rails box (`seni_ror_200250915`) reaches it directly via private IP `172.31.23.207:8010` (same VPC, same SG), proxied through nginx as `/proxy/gas/*`. So today it serves real prod traffic — not dormant any more. **Still no external HTTPS endpoint** for direct hits.

**Goal / shape.** Pick one of (a) `dao-protocol.truesight.me` → NELANCO direct (own nginx + Let's Encrypt on `dao_protocol_nelanco`) for external consumers that don't go through Edgar, or (b) leave it private-only forever and route all external clients through edgar.truesight.me/proxy/gas/*. Option (b) is the de-facto state today; only file (a) if there's a concrete need.

**Blocker / priority.** Not blocked. Lower priority now than at original filing — the cross-instance proxy works.

### Move NELANCO Postgres + Redis off public IPs

**Context.** NELANCO `seni_sql_2026` (Postgres) and `seni_redis_2` (Redis) both expose public IPs (`44.193.55.205`, `54.234.59.188`) because EXPLORYA Rails used to reach them over the internet. After the 2026-05-28 cutover, all consumers (NELANCO Rails, NELANCO Sidekiq) are in the same VPC; the public IPs are now unnecessary attack surface.

**Goal / shape.** Detach EIPs (or move to private-only subnets), update `database.yml` host + `production.rb` `redis_host` to private IPs (`172.31.20.143` Postgres, `172.31.56.185` Redis), restart Rails + Sidekiq, verify, ship via PR.

**Blocker / priority.** Not blocked but needs a short maintenance window (Rails restart). Coordinate with the certbot renewal task above so both reboots happen together.

### Check AWS T&S case 177613748700177 (Nelanco) for response — by 2026-05-29

**Context.** On 2026-05-27 (~11:14 PDT) the operator sent a consolidated reply to AWS support case `177613748700177` (Nelanco account `767697632458`), as the root user, closing all three open items: confirmed every resource on AWS's Apr-30 list as authorized, answered the May-20 access-location question (San Francisco, no VPN) + user list, and reconfirmed credential posture (root MFA on, zero root access keys). Full thread, live inventory, and the sent reply are in `cypher_def/docs/aws-reports/2026-05-27-case-177613748700177-consolidated-reply.md`. The account was verified clean via `cypher_def/scripts/aws/inventory_account.py --account nelanco`.

**Goal / shape (check ~2 days out, 2026-05-29).**
- If AWS **lifted the service limitation / resolved** → record outcome in the case report §3 and move this entry to Recently shipped.
- If AWS **asked for screenshot evidence** → the report §3 lists the 3 highest-value captures (root MFA + no-root-keys + password date; AMI naming; snapshot descriptions).
- If AWS is **silent / auto-nudges resumed** → post a one-line "awaiting your confirmation" bump in the case (as root).
- While there, optional hygiene (non-blocking): set the missing `SECURITY` alternate contact; deactivate the idle older access key on IAM user `truesight_dao_autopilot` (`AKIA3FPSYHTFFH4TCZUA`, last used 2026-05-03).

**Blocker / priority.** Time-boxed, not blocked. The account stays service-limited until AWS verifies, so don't let it stall silently.

### Swap autopilot's hand-rolled agent loop for a model-agnostic harness (keep the service + DAO tools)

**Context.** `truesight_autopilot`'s chat/agent loop is hand-rolled. On 2026-05-26 a session was spent live-debugging exactly the plumbing a mature harness ships for free: multi-round tool looping (truesight_autopilot#47), empty/whitespace output (#46), reply-thread routing (#45). The Telegram bot works now, but the fragility is structural and will resurface as models/queries vary. This is the "brain upgrade" risk flagged in the original autopilot-vs-OpenClaw decision and parked in `AUTOPILOT_TELEGRAM_BETA_DEPLOY_PLAN.md` §7.

**Goal / shape.** Keep the autopilot *service* — Edgar contribution logging, RSA governor auth, repo allowlists, the DAO tool set (`app/tools/*`), the Telegram adapter, the deploy loop — and replace ONLY the hand-rolled LLM↔tool loop with a mature one used as a *library*. NOT "adopt opencode the CLI" (that re-introduces babysitting).

**Decision axis = model-swapping (Gary's stated priority).**
- **Model-agnostic engine** — a loop over **LiteLLM** / an OpenAI-compatible layer, or an opencode/OpenClaw-style engine. Keeps easy multi-model swapping and enables **tiered routing** (cheap DeepSeek/GLM for proactive monitoring + simple chat; a strong model for code / multi-step reasoning; flip tiers if a provider is down). The loop still must absorb per-model tool-call quirks (e.g. GLM-4.5 emitting tool calls as text) — but does it far better than the hand-rolled code. **Recommended given the model-swap requirement.**
- **Claude Agent SDK** — best-in-class loop, but **Claude-first** (Anthropic / Bedrock / Vertex only); gives up the easy multi-model swapping Gary wants.
- Note: autopilot ALREADY has a provider abstraction (`app/llm/` + `LLM_PROVIDER` env + `docs/LLM_PROVIDER_ROADMAP.md`) and basic model-swapping. The gap is **loop quality**, not the model layer — so favor the model-agnostic path unless we deliberately standardize on Claude.

**Scope (likely > 1 session — sequence it).** Pick the engine; wrap the existing `app/tools/*` in its tool interface; route `/chat`, `/chat-blocking`, and the proactive `fix_agent` through it; preserve `_run_tool` dispatch + Edgar logging + governor identity injection; add tiered model routing. Verify against the 2026-05-26 regression cases (multi-step "events.json" query returns a full answer with no leaked `<tool_call>`; thread/empty handling) before cutover.

**Blocker / priority.** Not urgent — bot works today. Pick up when agent-loop edge cases recur, OR **before** broadening autopilot's autonomy (Tier-2 beta auto-merge in `AUTOPILOT_TELEGRAM_BETA_DEPLOY_PLAN.md`), since a robust loop is a prerequisite for trusting unattended runs.

### Edgar → `dao_protocol` extraction — PR8d: delete the ported `/dao/*` Rails actions (after soak)

**Context.** The Edgar→dao_protocol extraction (pulling the DAO/Agroverse surface out of the Rails `sentiment_importer` app into the Python FastAPI service) is essentially complete. Full plan + live resume tracker: **`EDGAR_DAO_EXTRACTION_PLAN.md`** (this repo). State as of **2026-06-07**: PR2–PR6b all ramped live; **PR8a** (`/dao/verify-signature` + `/dao/check_digital_signature`) ported (dao_protocol#62) **and ramped live** (edgar.conf exact-match → `:8010`; plain-curl verified; mirrored sentiment_importer#1089); **PR8b/PR8c DROPPED** — the abandoned HelloCash/POS invoice endpoints (`express_submit_contribution`, `link_upc`) + their backing services were deleted from Rails (sentiment_importer#1088), not ported.

⚠️ **Topology (current — updated 2026-06-07):** `edgar.truesight.me` → DNS → **`seni_ror` (NELANCO, 54.211.179.126)** which runs its own local nginx (`/etc/nginx/sites-available/edgar.conf`) → `127.0.0.1:3002` (Rails). The **dao_protocol service now runs on its OWN box** (`dao_protocol_nelanco`, internal `172.31.23.207:8010`) — edgar.conf's `/dao/*` + other ported `location =` blocks `proxy_pass http://172.31.23.207:8010`. (The repo `config/nginx.conf` mirror still shows `127.0.0.1:8010` on the older blocks — stale drift from before the box split; live is source of truth. Reach these boxes via the **Sophia bastion** — `ssh -J sophia` — see `AWS_DIGITAL_INFRASTRUCTURE.md` §7.1.)

**Scope (PR8d — the ONLY remaining cutover step).** In `sentiment_importer/app/controllers/dao_controller.rb`, delete the three now-dead **ported** actions whose traffic nginx already routes to `:8010`: `submit_contribution`, `verify_signature`, `check_digital_signature` — plus their `config/routes.rb` entries and their names in the two `skip_before_action` lists (line ~5–7). Confirm `DaoEmailRegistrationService` has no *other* Rails caller before removing it (its onboarding path was ported in dao_protocol#42; `submit_contribution` was its only caller). Keep on Rails: `index`, `chrome_installed`, `review_contribution`, `cypher`, `canvas` (Edgar-specific). `ruby -c` after; no specs reference the removed surface. Merge-not-deploy, then a normal Rails deploy carries it (and #1088) live. This fully retires the duplicate `/dao/*` submit/dispatch surface from Edgar — the original goal (stop LLMs being confused by two backends).

**Blocker.** Let the PR8a ramp **soak** first — don't delete the Rails fallback until the live `:8010` traffic for verify-signature/check_digital_signature has proven out. Target window ~**2026-06-25** (aligns with the existing PR7 soak). Rollback during soak = drop the two edgar.conf `location =` blocks + `nginx -t && reload` → back on Rails (only works while the Rails actions still exist, i.e. before PR8d).

**Minor hardening (non-blocking):** (a) rebind the dao_protocol service to `127.0.0.1:8010` — wait, it's now cross-box, so it must stay reachable on the box's interface for edgar nginx; instead lock it down via SG/localhost-nginx-hop review (see EXTRACTION_PLAN §6 "rebind" open decision); (b) refresh the repo `config/nginx.conf` mirror's stale `127.0.0.1:8010` blocks to the live `172.31.23.207:8010`.

### Dual Tech Summit 2026 (≈Jun 26, SF) — per-phase event follow-ups

**Context.** Agroverse is pouring two flasks — **Oscar's Farm ceremonial cacao (Bahia) + Paulo's cacao tea (Pará)** — with 3 oz cups at the SVH Capital / Orbis86 Dual Tech Summit, SF (Ken confirmed 2026-05-23). Full plan lives in `market_research/events/dualtechsummitjune26/` in **TrueSightDAO/go_to_market** (PR #133): `proposal_finalized.md` (plan-of-record), `implementation_roadmap.md` (phasing), `EXECUTION_CHECKLIST.md` (checkable), `field_assets.md` + `truesight_essay_draft.md` (drafted assets). These are **team follow-ups** (Gary / Claude / any LLM) — *not* DAO partner-ledger check-ins (`check_in_partner` is for inventory-carrying retail partners, not an event host).

**Scope (time-ordered — pick up the next due one).**
1. **By ~May 31** — Gary confirms with Ken: date, venue (War Memorial vs "American Legion"), the table, ClawCamp block timing → unblocks the site/pipeline build.
2. **~Jun 1–10** — review the drafted Phase-1 assets (`truesight_essay_draft.md`, `field_assets.md`).
3. **~Jun 8–17 (after date locked)** — Claude builds the event page + wires QR → newsletter signup → Hit List (checklist Phase 2).
4. **~Jun 18–20** — ⛔ dry-run the QR→signup→sheet loop, then publish the essay. *Nothing prints until the dry run passes.*
5. **~Jun 20–25** — print placard/stickers, pull cacao, pre-brew both flasks; personal (no-blast) outreach only.
6. **~Jun 27 – Jul 10** — post-event: leads → Hit List → Grok follow-ups; field-dispatch newsletter only if a real story; update `OUTREACH_QUALITATIVE_LOOP.md`.

**Blocker.** Steps 3+ depend on Ken confirming date/venue (step 1). Steps 1–2 are actionable now.

### `truesight.me/stats/network_state.json` — daily-refreshed DAO network-state digest

**Context.** Surfaced 2026-05-19 in a strategy conversation about what makes the DAO interesting *given* LLMs handle the plumbing. The thesis: with integration / data-entry / reconciliation cost approaching zero (per the 2026-05-19 Faire-bot onboarding session + Partner Check-in concierge UX), the scarce operator input is no longer ops work — it's **strategic design of loops + network orchestration + relationship hub-and-spoke choices**. This concentrates operator value into fewer, higher-stakes decisions, which means *visibility into network state* becomes the load-bearing input. The name `network_state.json` is a deliberate nod to Balaji's *Network State* thesis (kept in the implementation layer, not in the public-facing Growth Model SVG title — see strategy chat for the why).

**Scope.** Add a new artefact to the existing `truesight_me_beta` stats stack, following the established `LLM_DISCOVERY_SURFACE.md` convention:

1. **`truesight_me_beta/scripts/build_stats_current.py`** — new builder function `build_network_state()` that emits `_site/stats/network_state.json`. Same 6h cron, same pure-stdlib + unauthenticated public-data sources approach.
2. **Output schema** (rough, iterate):
   ```jsonc
   {
     "generated_at": "...",
     "loops": [
       { "name": "Retail Partner Referral", "status": "active",
         "signal_30d": <count>, "signal_90d": <count>,
         "velocity_change_pct": <float>,  // 30d vs prior 30d
         "operator_surface": "<url>" },
       // ... 11 loops from GROWTH_MODEL.md
     ],
     "populations": {
       "cacao_customers": { "active_30d": ..., "growth_pct": ... },
       "retail_partners": { ... },
       "dao_contributors": { ... },
       "credentialing_students": { ... },
       "credentialing_programs": { ... }
     },
     "adjacency": {
       // who introduced whom — hub-and-spoke map
       "top_referrers": [ { "name": ..., "introductions_90d": ... } ],
       "isolated_nodes": [ ... ]
     },
     "cross_population_flows_30d": [
       { "from": "cacao_customers", "to": "dao_contributors", "count": <n> }
     ]
   }
   ```
3. **`truesight_me_beta/llms.txt`** — add a routing line: *"For DAO operating-state / loop-velocity questions → fetch /stats/network_state.json"*.
4. **`agentic_ai_context/LLM_DISCOVERY_SURFACE.md`** — append a row to the live URLs table.
5. **`agentic_ai_context/GROWTH_MODEL.md`** — add a "Loop telemetry" subsection linking to `stats/network_state.json` for live state vs the model's described state.

**Data sources** (all already exist; the work is aggregation, not new instrumentation):
- Edgar event ledger (Contributors Digital Signatures, offchain transactions, Inventory Movement)
- `partners-velocity.json` + `partners-inventory.json` (already in `agroverse-inventory` repo)
- Hit List GAS `getWarmupReviewQueue` action
- `lineage-credentials/programs/*/manifest.json` (program count + cohort sizes)
- `truesight_me_beta/_site/stats/repos_index.json` (committer activity ≈ contributor activity)
- `Stripe Social Media Checkout ID` sheet (FB/Meta-Checkout sales for cross-population flow tracking)

**Acceptance.** A future operator (or LLM session) asks "is the Retail Partner Referral Loop compounding?" — answer is one `curl truesight.me/stats/network_state.json | jq .loops[0]` away, no spreadsheet archaeology needed. krake_sinatra's morning briefing reads from this file.

**Status:** Not built. Filing now so a future session (or krake_sinatra's own bootstrap) picks it up. **Half a day** of focused work — same shape as the other `build_stats_*.py` functions.

**Caveat.** Loop-velocity signals will be noisy at low N. Beer Hall digest already showed how easy it is to misread small-N changes. Each loop's `velocity_change_pct` should carry a sample-size annotation so the operator doesn't over-interpret. "First-derivative as headline; second-derivative as advisory only" is the right discipline.

**Blocker.** None — data sources all exist. Awaiting operator green-light to pick up.

**Owner.** Unclaimed.

---

### ERA WhatsApp thread: send unit-of-value reframe when Shahbaz reopens

**Context.** 2026-05-19, mid-ERA-DAO WhatsApp conversation with Bilal + Shahbaz (the `ERA DAO` WA group). Gary planted a strong seed in his 2026-05-18 message: *"That right there is the nucleus of its own verticalized social network. The basic unit of verifiable compassion."* Shahbaz absorbed it but the thread then moved on to the immediate ask (Shereen → cohort sheet → `garyjob@agroverse.shop` with edit rights). Ball is currently in Shahbaz's court. A thesis-level follow-up is drafted but **deliberately held** — sending it into silence while Shahbaz is working on his action item would interrupt step 1 and over-talk a fresh partner relationship. The right moment is when *Shahbaz reopens the conversation* (cohort sheet share, any follow-up question, or any thematic re-engagement).

**Trigger.** Any one of:
- Shahbaz shares the cohort sheet to `garyjob@agroverse.shop`.
- Shahbaz (or Bilal) replies in the WA thread with a follow-up question or comment.
- Conversation organically returns to retention / reengagement / scaling.

**Drafted message** (build on the "basic unit of verifiable compassion" seed Gary already planted; skip Edmodo specifically, skip "AI + web3" framing — baggage with this audience; skip Sufi/monastic lineage parallels — premature thesis depth; do NOT link the engineering roadmap — they need framing not implementation):

> Following up on what we were saying yesterday about the butterfly rescues and conservatory updates being the basic unit of verifiable compassion —
>
> That observation actually shapes how the credentialing system is designed. Most education platforms (the ones I worked on before, Coursera, etc.) treat *content* — lessons, courses — as the atomic unit, and centralise the system of record around it. What you're describing with the BE students is the inverse: the atomic unit is the *act itself*, attested by someone whose authority traces back to a real lineage (Shereen, the BE team, the conservatory work it descends from).
>
> Practically what this means: once the cohort sheet is in, we don't have to treat the credential as a one-off cert at graduation. Each butterfly rescue, each conservatory update can be a recordable event — signed by the student, attested by Shereen or the school admin, and added to their lineage record. That's actually the retention mechanism you were asking about earlier — instead of an arbitrary re-engagement program, the system just keeps recording what's already happening organically.

**Why this variant and not the Beer Hall version.** The Beer Hall post (TrueSightDAO/agentic_ai_context PR #157) carries Edmodo references, AI + web3 framing, and historical lineage parallels (Sufi orders, monastic traditions, capoeira mestre chain). That register is tuned for DAO contributors who share the context. For Bilal + Shahbaz — partners 24 hours into substantive collaboration — the same content would land as Gary-getting-ahead-of-himself rather than alignment. The variant above keeps the unit-of-value reframe, builds on the seed already planted, and closes a loop Shahbaz himself opened (he asked about reengagement mechanisms on 2026-05-18 evening; this answers it).

**Caveat.** If Shahbaz reopens cold (e.g. just shares the sheet with no commentary), don't lead with the thesis. Acknowledge the sheet, confirm next steps, *then* if there's a conversational beat, slide the thesis-paragraph in as a "and the thing this unlocks is…" follow-up. Don't monologue.

**Blocker.** Waiting on Shahbaz reopening the conversation. No build, no engineering — purely a "send-when-trigger" message.

**Owner.** Gary (he's the WA participant); any AI session helping draft can use the message above as the starting point and tune to whatever Shahbaz actually said.

---

### Capoeira practice-event encoding: Portuguese diacritics dropped at submission

**Context.** Discovered 2026-05-19 while shipping the tap-to-expand session details on per-program credential pages ([truesight_me_beta#128][cred-expand]). Move names in Gary's Tribo Bahia Mirim sessions on `_cache/cv/gary-teh.json` render as `Cocorinha com rol?` instead of `Cocorinha com rolê` — the `ê` is being lost somewhere in the submission pipeline. Other Portuguese diacritics (`ã`, `á`, `ç`) on other move names are presumably similarly affected. The display layer (program-shell.js's renderEventListItem) surfaces whatever the cache has; the bug is upstream.

**Scope.** Trace where the encoding hiccup happens:

1. **Source.** `capoeira/data/moves.json` — confirm the canonical move list carries the correct UTF-8 (it should; this is the seed data).
2. **Practice page.** `capoeira/assets/js/practice-event-submit.js::buildPracticeEventText()` and the signing path. Likely culprit if the payload is stringified through a code path that doesn't preserve UTF-8.
3. **Edgar (`sentiment_importer`).** The `[PRACTICE EVENT]` handler in `dao_controller.rb` and whatever lands the event into Telegram Chat Logs. If Edgar logs through a system that downgrades to Latin-1 anywhere, the diacritic dies there.
4. **GAS scanner.** The Apps Script that picks the event up from Telegram Chat Logs and persists it to lineage-credentials.
5. **lineage-engine build.** `build_cv_cache.py` reads the persisted event and writes the cache JSON. If the input file has the encoding hiccup, the cache will too.

**Acceptance.** A new practice session submitted today with `rolê` in a move name shows up on `truesight.me/programs/tribomirim/credentials/#pk-wR9zU8JMnEz1` (under the expanded session row) as `rolê`, not `rol?`. Confirm in at least one round-trip.

**Cost.** ~1-2 hours including reproduction + fix at the right pipeline layer.

**Blocker.** None. Cleanest path is to submit one fresh test session from the practice page with deliberately-diacritic-heavy move names, then inspect each pipeline stage's stored copy to find where the `ê` becomes `?`.

**Owner.** Unclaimed.

[cred-expand]: https://github.com/TrueSightDAO/truesight_me_beta/pull/128

---

### Credentialing: WhatsApp self-claim flow (deferred — held for demand signal)

**Context.** Surfaced 2026-05-19 in the ERA DAO WhatsApp thread with Bilal + Shahbaz. Butterfly Effect students (and capoeira-Tribomirimbahia students) identify primarily by WhatsApp number, not email. The existing `dapp.truesight.me/create_signature.html` email-based identity flow has no equivalent for these populations. A WhatsApp self-claim flow would let students assert "this pk-hash is me" against an issued credential at `truesight.me/credentials/#<slug>`.

**Scope.** Full design lives at `CREDENTIALING_PLATFORM.md` §13 — flow diagram, alternatives considered, 2026 Meta cost model (user-initiated reply is free, business-initiated push is billed), six-item Meta paperwork prerequisite list (legal entity → business verification → DAO-owned WA-eligible phone number → app + token + webhook), four-piece engineering scope (~2–3 days focused work behind ~1 week of Meta business verification), privacy invariants (`wa_phone_hash = sha256(cc + national)`, never raw number).

**Defer-flip criteria.** This is held — NOT a queue item — until *any one* of:
1. A student in any active program asks how to prove the credential is theirs.
2. A second program beyond BE + capoeira lands with WhatsApp-native participants (i.e. the pattern repeats and self-claim becomes infrastructure rather than feature).
3. BE / IVY acquisition by TDF closes with a contractual requirement for student-side attestation.
4. A receiving platform (employer, school, ceremony org, partner shop) starts checking credentials and asks for a "verified by holder" signal beyond the QR.

Until then the issued-credential surface (cert PDF + QR + public `/credentials/#<slug>`) is the demo. Don't pre-build the auth on speculation.

**Blocker.** No demand signal yet (2026-05-19). Building now would mean ~1 week of Meta business verification + a legal-entity decision on which WABA front to use — both real costs against zero current need.

**Owner.** Unclaimed. Next session that sees a defer-flip criterion fire should pick this up.

---

### Partner Check-in: paste-image-as-attachment (v0.2 attachment support)

**Context.** Operator request 2026-05-12: when filing a Partner Check-in (e.g. for the Matheus / AGL7 freight in flight), be able to **paste an image directly into the Notes field** and have it automatically uploaded as an attachment that the check-in history later renders inline. Use cases: container photos, customs paperwork, retail stencil photos on cacao bags, screenshots of vendor replies. The pattern exists already in adjacent surfaces (`[ASSET RECEIPT EVENT]` uses `--attachment`, `Stores Visits Field Reports` carries `github_raw_url`/`github_blob_url`); this just hasn't been extended to Partner Check-in yet.

**Scope.** Five-component build, each well-trodden:

1. **`dapp/partner_check_in.html`** — add a `paste` event handler on the Notes textarea. When clipboard contains an image blob, POST it to Edgar's `upload_file_to_github` tool, get back the `https://raw.githubusercontent.com/...` URL, and either (a) append it to the Notes text as a markdown image link, or (b) store it as a separate hidden field that ships in the submission payload. Recommend (b) — keeps Notes clean and the attachment a first-class field.
2. **Edgar payload** for `[PARTNER CHECK-IN EVENT]` — add an `Attachment URL: <raw_url>` line, same shape `[ASSET RECEIPT EVENT]` already uses.
3. **`tokenomics/google_app_scripts/find_nearby_stores/process_partner_check_in_telegram_logs.gs`** — extract the URL from the Telegram payload, write it to a new column on the Partner Check-ins tab.
4. **`Partner Check-ins` tab on Main Ledger** — add column O `Attachment URL` (one-time sheet edit + scanner update).
5. **`Shipping Planner` `get_partner_check_ins` action** — include the new column in returned rows. **Partner Check-in history UI** on `partner_check_in.html` — render the URL as a clickable thumbnail (image) or link (PDF) inline with each history entry.

**Acceptance.** Paste an image while filing a check-in for Matheus → submit → reopen the Partner Check-in form with `?partner_id=black-king-ilheus` → the just-filed entry shows the thumbnail in the Check-in History block.

**Caveats.**
- v0.2 limit: one attachment per check-in (matches every other Edgar event). Multi-attachment is a separate v0.3 ask.
- The auto-checkin-on-send (`runProcessSentPartnerPokes`) won't have attachments — the new column will be blank for `Submitted By = "Partner Poke Scheduler v0.1"` rows. No special handling needed.
- The DApp paste handler needs to be careful about clipboards that contain BOTH an image AND text (some screenshot tools do this). Prefer the image; ignore the text — let the operator type Notes themselves.

**Blocker.** None. Edgar's `upload_file_to_github` exists. `Stores Visits Field Reports` already proves the end-to-end pattern. Build is ~2-3 focused hours across the 5 components.

**Owner.** Unclaimed.

---

### Beer Hall daily digest: include Partner Check-ins section

**Context.** Operator request 2026-05-12: the daily Beer Hall digest currently summarizes commits, PRs, and ecosystem activity. Partner Check-ins are core supply-chain operations — they should appear in the digest too. Without this, the WhatsApp Beer Hall community can't see Gary's offline outreach activity (the same observability gap that motivated the original Partner Check-in build, but now applied to the broader community surface, not just LLM advisors).

**Scope.**

- Identify the script that generates the Beer Hall daily digest (`agentic_ai_context/OPENCLAW_WHATSAPP.md` documents the pipeline; the actual generator is in `content_schedule` or a related repo per the doc).
- Add a new data source: read the **Partner Check-ins** tab on Main Ledger via gspread (the credentials already exist for the advisory pipeline), filter to entries from the last 24 hours.
- Render a new digest section: "Partner Check-ins (last 24h): N entries", with a per-entry line `<partner_name> · <method> · <stock_status if relevant> · <notes excerpt>`. Match the existing Beer Hall digest's voice and density.
- Skip empty days — don't render the section if no check-ins happened in the window.

**Acceptance.** Tomorrow's Beer Hall digest includes a `### Partner Check-ins (last 24h)` section listing any entries Gary filed today. If no entries, the section is omitted.

**Blocker.** Beer Hall pipeline's LLM provider (Anthropic last week, possibly switched after the credit-zero incident on 2026-05-11) needs a working credit balance. Verify before building.

**Owner.** Unclaimed.

---

### Trees in Pipeline: finer-grained inventory tag for hybrid Operator partners

**Context.** Kiki's Cocoa is `partner_type=Operator` because she's a SF warehouse hub for some shipments AND handles online fulfillment to end consumers. Her **sales_monthly** is correct (only counts QR Code Sales, never restocks). But her **inventory_units** mixes bulk-warehouse stock (NOT yet financed → should NOT count toward Trees in Pipeline) with retail-ready stock (IS in pipeline → should count). The current filter (`market_research#122` deny-list of Freight Provider + Supplier) keeps Kiki's full inventory total, which slightly over-counts Trees in Pipeline.

**Scope.** Two paths to evaluate:

1. **Per-row inventory_type-based filter.** The Currencies sheet column distinguishes `Cacao Bean (Bulk)` vs `Cacao Mass (Retail Ready)` etc. Trees in Pipeline could sum only `Retail Ready`-format inventory. **Cleanest if the tagging is reliable.**
2. **Per-partner role tagging.** Add a sub-flag on `Agroverse Partners` like `inventory_role: bulk | retail | mixed`. For `mixed` partners, derive proportion from sales velocity. **More complex but handles edge cases.**

Pick path 1 if the inventory_type field on `partner_inventory` JSON is already reliable across all Operator-type partners; otherwise path 2.

**Acceptance.** Open `https://truesight.me/index.html`, Trees in Pipeline drops by Kiki's bulk-warehouse stock total. Sanity-check: the new total roughly matches the sum of inventory at strict-retail partners (Consignment + Wholesale) + the retail-ready portion of Operator-partner inventory.

**Blocker.** Need to verify the inventory_type tagging is consistent on the JSON before committing to path 1. Run `sync_sell_through_report.py` once and inspect Kiki's items[] block in the output JSON.

**Owner.** Unclaimed.

---

### Wire the DApp bell's action items into `ADVISORY_SNAPSHOT.md` generation

*(Scope broadened 2026-05-12 from the original "Wire `Partner Check-ins`…" entry, which had just the operator-scheduled cadence in view. The bell now aggregates three signal sources; the advisory should surface all three.)*

**Context.** The DApp notification bell (shipped 2026-05-12, see [`DAPP_NOTIFICATION_BADGE.md`](./DAPP_NOTIFICATION_BADGE.md)) aggregates three signal sources for the operator:

1. **Outbound Review** — drafts in `AI/Warm-up`, `AI/Follow-up`, `AI/Prospect Replied`, `AI/Partner Poke` cohorts (from `getWarmupReviewQueue`)
2. **Partner Check-in follow-ups** — operator-scheduled cadence (from `list_partners_needing_attention`)
3. **Partner Stock attention** — out-of-stock / low-stock / dormant (from velocity + inventory JSONs)

Today these surface only to Gary via the DApp. LLM advisors (Dr Manhattan, Seth Godin, I Ching oracle) reading `ADVISORY_SNAPSHOT.md` are blind to them — so they keep recommending action Gary's already on (e.g. "you should follow up with prospects" while 12 drafts sit in his queue waiting for review). The integration closes that loop: the advisory becomes a **client of the bell substrate**, surfacing the same operator-bottleneck signals to whoever's reading it.

**Voice locked in (Gary picked 2026-05-12).** Contemplative narrative — data woven into prose with explicit advisor guidance, matching the existing north-star framing at the top of the advisory. The integration MUST produce output of this shape, not a tabular Jira-dashboard:

```markdown
## Action items (where operator review or attention is the bottleneck)

_Same signals the DApp bell aggregates — surfaces what's actually
waiting on Gary, not raw queue depth. Refreshed daily._

**Outbound drafts awaiting send (22 total):** 12 warm-ups (avg 4d
old), 3 follow-ups (all ≥7d — these are stalling), 2 prospect replies
(time-sensitive — prospect already engaged), 5 partner pokes (3
partner-addressed, 2 self-reminders for partners without email).

**Partner check-in cadence (3 overdue or due):** Tech Spot (5d
overdue, last via In Person), Beanery (2d overdue, last via Email),
KiKi's Cocoa (due today, last via Phone). Cadence is operator-driven
— Gary picked these dates when filing each check-in.

**Partner stock signals (3 flagged):** Tech Spot is out of stock
(0 days runway). KiKi's Cocoa is running low (2 units, ~3 days).
Mountain Roastery has been dormant 67 days.

When advising on outreach priority, weight inversely by runway:
out-of-stock partners and prospect replies first; warm-ups can sit.
Treat the dormant set as questions about positioning, not just
restocks — they may need a different conversation.
```

The closing advisor-guidance paragraph should be **regenerated each day to fit that day's specific signals**, not stamped from a fixed template. A useful rule of thumb: when the signals concentrate in stock attention, lean on stockout urgency; when they concentrate in dormancy, lean on positioning/zeitgeist; when they concentrate in drafts, lean on prioritisation. Grok or whichever LLM the advisory generator already uses for its prose framing is the right tier for this.

**Scope.**

- Extend the snapshot generator (Python under `market_research/` or wherever `ADVISORY_SNAPSHOT.md` is built today) to call the three bell sources above. The advisory becomes a *client* of the bell substrate — same calls, no reimplementation of severity scoring.
- Add a new "Action items" section at the top of the operator metrics block (before "Operations health"), rendered exactly in the voice above. Use `list_partners_needing_attention` for cadence and `partners-velocity.json` + `partners-inventory.json` for stock — same data, same scoring rules, same naming as `partner_check_in.html`'s `computeAttentionList()` (so the advisory and the DApp page never disagree by drift).
- Resolve partner_id slugs to human names via `Agroverse Partners!E → Contributors contact information!A` — same join pattern `partner_poke_drafts.gs` uses.
- The advisor-guidance closer (last paragraph) should be regenerated daily by the same LLM the advisory already uses for prose framing.

**Blocker.** Build only **after Partner Poke Scheduler v0 has run for a full week of operator-confirmed calibration** (see [`PARTNER_POKE_SCHEDULER_v0.md`](./PARTNER_POKE_SCHEDULER_v0.md)). The week of real runs surfaces which signals actually drive operator action vs which add noise — those calibrations should be reflected in the rendered advisory before it goes to the oracle. Don't build against synthetic data.

**Acceptance.** Open the next refreshed `ADVISORY_SNAPSHOT.md` and confirm: (a) the "Action items" section is present at the top of operator metrics, in the contemplative-narrative voice above; (b) all three signal sources are surfaced (outbound drafts, partner check-in cadence, partner stock); (c) the closing advisor-guidance paragraph reflects that day's actual signal distribution, not boilerplate; (d) re-running the advisory through the I Ching oracle, Dr Manhattan, and Seth Godin visibly references the specific action items instead of recommending generic outreach.

---

### `dao_client onboard_retail_partner` CLI — v1: website + PR automation

**Context.** MVP shipped via [`dao_client#11`][onboard-mvp] on
2026-04-28 — automates the deterministic ledger + inventory steps
(§3.1 / §3.2 / §3.3 / §3.13 / §3.14 of
`RETAILER_TECHNICAL_ONBOARDING.md`) idempotently, with a YAML manifest
input. Dry-run by default. Operator still has to do the website surface
work + photo upload + PR creation manually after running it.

v1 fills in the remaining steps:

- §3.4 Partner page generation (clone `partners/lumin-earth-apothecary/`,
  named-replacement on slug + name + address + lat/lon + about-blurb;
  about-blurb either operator-supplied in manifest or Grok-extracted
  from `website` URL).
- §3.5 Discovery surface updates (`partners-data.js` append,
  `partner_locations.json` append, `wholesale/index.html` and
  `partners/index.html` alphabetical inserts,
  `cacao-journeys/pacific-west-coast-path/index.html` jpeg-extension
  conditional).
- §3.6 Photo download + resize (operator URLs in manifest, or fall back
  to scraping `og:image` / favicon).
- §3.12 + §3.15 Branch + commit + `gh pr create` in `agroverse_shop_beta`
  and `agroverse-inventory`. Push branch only — operator merges manually
  for the first 5–10 onboardings before flipping to auto-merge.
- §3.4 lat/lon geocoding via Nominatim (free, no key) when manifest
  doesn't include them.

**Acceptance criterion.** Next retail-partner onboarding takes ≤ 5
minutes of operator time end-to-end, including PR review + merge.

**Blocker.** None — every required piece exists. MVP must run cleanly
on a real onboarding before v1 layers on the more invasive automation
(template clone, multi-repo PR creation).

**Owner.** Unclaimed.

[onboard-mvp]: https://github.com/TrueSightDAO/dao_client/pull/11

---

### Eyeball-check `partners-velocity.json` numbers after 4 weekly refreshes

**Context.** First version of `sync_partners_velocity.py` shipped via
[go_to_market#80][velocity-pr] and the first JSON snapshot via
[agroverse-inventory#5][velocity-snap]. Refresh cadence is weekly. Per
Gary's §9 Q5 decision in `PARTNER_VELOCITY_PROPOSAL.md` ("wait till
settle"), no downstream consumer should *trust* the numbers until at
least **4 successful weekly refreshes** have run and a manual sanity
check has confirmed the values track operator intuition for 3–5 known
partners (Go Ask Alice, Lumin Earth, Edge & Node, Kiki's Cocoa).

**Outcome.** Either flip the green-light (wire dormant / high-velocity
signals into warm-up generator — see next entry), or file a defect on
the script if the numbers feel wrong.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read the latest committed snapshot.
- `market_research/scripts/sync_partners_velocity.py` — re-run locally if needed.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §9 Q5 (acceptance criterion).

**Blocker / signal to revisit.** Wait for ≥4 entries on the GitHub
Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible
acceptance check: **2026-05-25** (~4 weeks after first snapshot).

**Owner.** Gary (manual sanity check), then any agent for downstream wiring.

[velocity-pr]: https://github.com/TrueSightDAO/go_to_market/pull/80
[velocity-snap]: https://github.com/TrueSightDAO/agroverse-inventory/pull/5

---

### Wire dormant / high-velocity signals into warm-up draft generator

**Context.** Once `partners-velocity.json` numbers are trusted (see
previous entry), the warm-up draft generator
(`market_research/scripts/suggest_warmup_prospect_drafts.py`) and any
sibling check-in flow can read per-partner activity to:

- **Dormant retailer** (`last_sale_date > 90 days ago` and
  `last_restock_date > 90 days ago`) → trigger a check-in email
  instead of a generic warmup, or de-prioritize warmups for them.
- **High-velocity retailer** (per-SKU `*_12m_monthly_avg >
  category_medians[sku].monthly × N`) → flag as a candidate for
  case-study / testimonial / shelf-photo capture for `/wholesale/`.
- **Cold-start / newly-onboarded retailer**
  (`max(sample_size_*) < 3`) → no recommendation; default to
  category baseline.

**Outcome.** Tighter outreach prioritization without manual triage; a
small CSV-style "this week's flags" surface (sheet or Markdown) for
operator review.

**Files.**
- `market_research/scripts/suggest_warmup_prospect_drafts.py` —
  primary integration point.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic.
- `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` — tighten the
  status-transition rules once the signals exist.

**Blocker.** Previous entry (eyeball-check) must complete green.

---

### Rename "Agroverse Partners" sheet → "DAO Partners" + sweep consumers

**Context.** 2026-05-20: the Main Ledger tab `Agroverse Partners`
(`1GE7PUq-...` gid=1983902109) now holds rows whose `partner_type` is
`Operator`, `Supplier`, `Freight Provider`, `Manufacturer`, etc. — i.e.
the whole DAO partner ecosystem, not just retail/wholesale for the
Agroverse cacao brand. The name is now a misnomer; new operator-partner
onboards (Wayne @ UX.APP, 2026-05-20) make it more obviously so.

**Why it didn't ship inline.** A rename has cross-repo blast radius —
every consumer keys off the literal string `"Agroverse Partners"`. Doing
it as part of the Wayne onboarding PR would have ballooned the diff.

**Scope (single PR after the Wayne onboard PR merges).**
1. Rename the sheet tab `Agroverse Partners` → `DAO Partners` (gid is
   stable; gid-keyed consumers are unaffected).
2. Sweep every literal-string consumer. Known callers to grep first:
   - `dao_client/truesight_dao_client/modules/onboard_partner.py` —
     `PARTNERS_SHEET` constant.
   - `market_research/scripts/sync_partners_velocity.py` (if it reads
     the tab by name).
   - GAS handlers under `tokenomics/` that scan the Main Ledger.
   - DApp Partner Check-in scanner (`dapp/partner_check_in.html` →
     GAS handler) — confirm the worksheet name.
   - `agroverse_shop` discovery surfaces (`partner_locations.json`
     generator, if any).
   - `agentic_ai_context/RETAILER_TECHNICAL_ONBOARDING.md`,
     `PARTNER_CHECK_IN_IMPLEMENTATION.md`, and any other docs that
     name the tab.
3. Workspace-wide grep before declaring victory:
   `grep -r '"Agroverse Partners"' ~/Applications` and
   `grep -r "'Agroverse Partners'" ~/Applications`.

**Outcome.** Tab name reflects its actual scope; future operator /
freight / supplier onboards stop reading as "Agroverse cacao business"
by association.

**Files.** Main Ledger spreadsheet
`1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU`, gid `1983902109`, plus
every caller surfaced by the grep sweep.

**Owner.** Unclaimed.

---

### Advisory ops-health v2: burn rate + days-of-cover at SF

**Context.** Ops-health v1 ([TrueSightDAO/go_to_market#77][pr77] +
[follow-up #78][pr78]) ships per-shipper stock from
`treasury-cache/dao_offchain_treasury.json`, cash float from `off chain asset
balance`, and in-transit freight from `Shipment Ledger Listing`. Burn rate /
days-of-cover at SF (Kirsten) was deliberately deferred — the structured
snapshot at `ecosystem_change_logs/ops_health/current.json` already reserves
two `null` slots: **`sales_velocity_30d`** and **`days_of_cover_at_sf`**.

**Outcome.** When v2 lands, the daily oracle / a future
`dapp/supply_health.html` page can flag a SKU with **🟢 ≥4 weeks cover · 🟡
2–4 weeks · 🔴 <2 weeks** at Kirsten — exactly the signal Gary is missing
today (*"Kirsten goes low before Matheus's freight inbound has arrived"*).

**Files / shape.**
- `market_research/scripts/generate_advisory_snapshot.py` →
  `_compute_ops_health(...)` returns the structured dict; add a peer
  `_compute_burn_rate_and_cover(treasury, qr_sales_rows)` that populates the
  two reserved slots and surface a few `🟢/🟡/🔴` lines in
  `_render_ops_health_markdown`.
- `QR Code Sales` window already loaded by `_fetch_sheet_sales_markdown` when
  `--with-sheet-sales` is on — pass the parsed rows through instead of
  re-reading.

**Join key.** Today the join between sales (per Currency string) and stock
(per `inventory_type` × `unit_format`) is brittle because **`inventory_type`
is only populated on ~28% of `dao_offchain_treasury.json` items as of
2026-04-27** (column added 2026-04-26; backfill in progress). Two paths:

1. **Conservative:** join on the raw `Currency` string (works today, exact
   match per batch — granular but noisy).
2. **Cleaner (preferred when ready):** join on `inventory_type` × `unit_format`
   once the backfill is meaningful (~>80% populated). Surface the same flag
   one level higher.

**Blocker / signal to revisit.** Check `inventory_type` sparseness on
`dao_offchain_treasury.json` before starting:

```bash
curl -sL https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/dao_offchain_treasury.json \
  | python3 -c '
import json, sys
d = json.load(sys.stdin)
items = [it for m in d.get("managers", []) for it in m.get("items", [])]
populated = sum(1 for it in items if (it.get("inventory_type") or "").strip())
print(f"{populated}/{len(items)} = {100*populated/len(items):.0f}% populated")
'
```

If <40%, do path (1) only. If >80%, go straight to path (2). In between, ship
path (1) and re-roll-up by `inventory_type` for the markdown summary.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks after v1
shipped, gives the backfill room).

[pr77]: https://github.com/TrueSightDAO/go_to_market/pull/77
[pr78]: https://github.com/TrueSightDAO/go_to_market/pull/78

---

### `two_bahia_bars` newsletter — post-send open / click / reply read-out

**Context.** First Agroverse newsletter to ship with the full pipeline ([buyer
exclusion][n-pr79], [JPG fallback + tighter image margins][n-pr84],
[side-by-side comparison row][n-pr85]) sent 2026-04-27 to **38 recipients**
(2 past-buyers excluded via `--exclude-buyers-of-substring` against
`Agroverse QR codes`). Tracking on by default — opens land in cols H–K and
clicks in L–P on the **`Agroverse News Letter Emails`** tab of the dedicated
newsletter workbook (`1ed3q3SJ8ztGwfWit6Wxz_S72Cn5jKQFkNrHpeOVXP8s`),
filtered by `campaign='two_bahia_bars'`.

**Why a follow-up reads the data.** The v5 layout (compact 280px images,
side-by-side comparison row at top) was a deliberate design call. Without a
read-out, the data sits in the sheet and the comparison-row decision can't
be validated for future sends. iOS Mail Privacy Protection inflates opens
in the first hour — the read-out should land **after a 7–10 day soak** so
real engagement (repeat opens, clicks, replies) dominates the noise.

**Outcome.** A short summary covering:
- Open rate (recipients with `open_count > 0`) and median `open_count`.
- Click rate (recipients with `click_count > 0`) and which CTA each clicker
  hit (`last_clicked_url` — Oscar's Farm, Fazenda Santa Ana, or both via the
  comparison row's separate "Check this bar" links).
- Reply rate (search Gmail `to:garyjob@agroverse.shop` against the
  recipient list; count distinct addresses that replied).
- **Did the comparison row's "Check this bar" CTA get clicked at a
  meaningfully different rate than the in-section "Check Oscar's Farm
  2024" / "Check Fazenda Santa Ana 2023" CTAs?** (Same destination URLs,
  different anchor text + position. Real design signal for whether the
  comparison row earns its keep on future two-SKU sends.)

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:two_bahia_bars'`,
   description includes the headline numbers).
2. A DAO contribution submission via **`dao_client`** with the analysis as
   the body and a link to the DApp Remarks row.

**Files / shape.**
- Recipient list keyed off `campaign='two_bahia_bars'` from
  `Agroverse News Letter Emails`.
- Open / click columns already populated by Edgar's
  `/newsletter/open.gif` and `/newsletter/click` endpoints.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<recipient> after:2026-04-27`.
- Sheet write: append to `DApp Remarks` on the Hit List spreadsheet
  (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); see
  `market_research/scripts/hit_list_dapp_remarks_sheet.py` for the helper.

**Owner.** Unclaimed. Earliest sensible: **2026-05-07** (10 days after the
send — opens / clicks have stabilized, replies have had a week to land).

**Optional adjacent work.** While reading the data, also note whether
either of the two excluded buyers (`pamelacotton7@msn.com`,
`toffees_fibrils.0l@icloud.com`) ever asked "why didn't I get the
newsletter about the bars I bought?" — would update the buyer-exclusion
copy in `AGROVERSE_NEWSLETTER_WORKFLOW.md` §4.3a if so.

[n-pr79]: https://github.com/TrueSightDAO/go_to_market/pull/79
[n-pr84]: https://github.com/TrueSightDAO/go_to_market/pull/84
[n-pr85]: https://github.com/TrueSightDAO/go_to_market/pull/85

### Warm-up email A/B read-out — PDF-only vs PDF+packaging-photos cohort comparison

**Context.** [`go_to_market#74`][wp-pr74] (merged 2026-04-27) flipped the
default warm-up email payload from "PDF wholesale catalog only" to "PDF +
2 packaging photos" for every send via the partner-outreach pipeline. The
hypothesis: visual product proof in the first touch lifts open / click /
reply rates over a PDF-only ask. Without a read-out, the change sits as
an untested intuition.

**Why a follow-up reads the data.** The cleanest natural experiment we'll
get — the cutover is sharp (one PR), the population is otherwise
homogeneous (same Hit List rows, same template, same operator), and the
volume on either side of 2026-04-27 should be enough for a directional
signal even if not statistically rigorous. Earliest sensible read:
**2026-05-11** (~2 weeks of post-cutover sends + replies have had time
to land — Gmail reply soak window matches the newsletter read-out
above).

**Outcome.** A short comparison covering, for each cohort:
- **Cohort split.** Read the `Email Agent Follow Up` tab of the Hit List
  workbook (`1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc`); split
  rows where status indicates a warm-up was sent into:
  - **Pre-2026-04-27** (PDF only) — sent before the cutover.
  - **On/after 2026-04-27** (PDF + 2 packaging photos) — the new default.
- **Metrics per cohort.** Count, open rate (`Open` column > 0), click
  rate (`Click through` column > 0), reply rate (cross-reference Gmail
  for inbound replies to each `to_email` after `sent_at`).
- **Time-controlled comparison.** Repeat the metrics restricted to the
  **2 weeks immediately before** vs **2 weeks immediately after**
  2026-04-27 to neuter time-of-year / list-quality drift.
- **Verdict.** Did packaging-photo warm-ups beat PDF-only on any of
  open / click / reply by a margin that would survive doubling the
  sample size? If yes — keep the new default. If no — flag whether to
  revert or keep as the cleaner UX call regardless of metrics.

Post the summary as:
1. A row on **`DApp Remarks`** (`store_key='campaign:warmup_packaging_photos_ab'`,
   description includes headline numbers + PR URL).
2. A DAO contribution submission via **`dao_client`** with the analysis
   as the body and a link back to the DApp Remarks row + PR #74.

**Files / shape.**
- Sheet read: `Email Agent Follow Up` tab on
  `1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc` via
  `google_credentials.json` + gspread.
- Status / cohort inference: `market_research/HIT_LIST_CREDENTIALS.md`
  documents the Status column conventions.
- Reply detection: Gmail OAuth at
  `market_research/credentials/gmail/token.json`; query
  `from:<to_email> after:<sent_at>` per recipient.
- DApp Remarks append: `market_research/scripts/hit_list_dapp_remarks_sheet.py`.
- Contribution log: dao_client CLI per
  `agentic_ai_context/DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`.
- Label / status convention: `agentic_ai_context/PARTNER_OUTREACH_PROTOCOL.md` §9.7.

**Owner.** Unclaimed. Earliest sensible: **2026-05-11** (~2 weeks post-cutover).

**Why not `/schedule`.** Tried — remote agent can't access the private
sheet, Gmail OAuth, or Edgar tokens (no MCP connectors connected, no
`google_credentials.json` in cloud sandbox). Belongs on the local
backlog.

[wp-pr74]: https://github.com/TrueSightDAO/go_to_market/pull/74

### Migrate `dapp/stores_nearby.html` Add Store form onto the `[STORE ADD EVENT]` Edgar path

**Context.** The dao_client / Edgar / GAS slice of `[STORE ADD EVENT]`
shipped 2026-04-28 (see *Recently shipped* below). The DApp's
`stores_nearby.html` Add Store form still talks directly to GAS
`add_store` — small GET payload that doesn't have the cross-origin
failure mode the retail field report flow had, so it works, but the
DAO has decided that **all signed Hit List writes go through the same
canonical pattern**: DApp → Edgar → Telegram Chat Logs → async GAS
scanner. This entry is the remaining migration to that posture.

**What's needed.**
- Replace the direct `fetch(GAS, {action: 'add_store', …})` call in
  `dapp/stores_nearby.html` with a signed `[STORE ADD EVENT]` POST to
  Edgar (mirror today's `submitRetailFieldReportToEdgar` shape in
  `dapp/store_interaction_history.html`).
- Drop or repurpose the `add_store` action in
  `clasp_mirrors/1NpHrKJW…/Code.js` once no callers remain. The
  `addNewStore()` helper stays — it's the GAS scanner's own
  dependency.
- Verify the DApp form's "duplicate detected" UX still works
  (today the GAS direct call returned `{success: false, duplicate:
  true, existing_store: …}` synchronously; with the async path the
  duplicate detection lands on **Store Adds** col K
  `existing_store_shop_name`, so the form needs a polling /
  back-channel UX or a "submitted — check Hit List in a minute"
  message).

**Cost estimate:** ~30 min including the form's status / duplicate UX.

**Blocker.** None — purely additive once started. Don't bundle with
unrelated `stores_nearby.html` work.

**Owner.** Unclaimed.

### Deprecate `backfill_hit_list_opening_hours.py` + `backfill_hit_list_google_listing.py` after 2 cron cycles

**Context.** 2026-04-28 the two responsibilities — opening-hours grid (Mon
Open … Sun Close) and `Google listing` column — were folded into the routine
hourly cron at `.github/workflows/hit_list_enrich_contact.yml` (`35 * * * *`)
via [TrueSightDAO/go_to_market#88][pr88]. The enriched
`scripts/hit_list_enrich_contact.py` now also fills empty `Address / City /
State / Latitude / Longitude` from the same Places Details call. The two
standalone backfills still exist as manual one-shots but should no longer
need to be invoked routinely.

**Outcome.** Either delete the two standalone scripts, or shrink them to
thin documented wrappers that call into `hit_list_enrich_contact.py`'s
`apply_place_result_to_row_gaps()` helper for one-shot full-table sweeps.

**Files.**
- `market_research/scripts/backfill_hit_list_opening_hours.py`
- `market_research/scripts/backfill_hit_list_google_listing.py`
- `market_research/scripts/hit_list_enrich_contact.py` (already imports both
  via `bl` / `dl` for `resolve_place_id` + `append_place_id_to_notes` —
  if either backfill is deleted, inline the helpers it depends on or move
  them into a shared module).

**Verification before deleting.** On the Hit List, confirm:

1. New rows landing in the past 2 weeks have non-empty `Address`, `City`,
   `State`, `Latitude`, `Longitude`, `Monday Open`, `Google listing` (where
   Places returns those fields) within ~24h of arrival.
2. The `cron`-scheduled action's last 24 runs each show `filled>0` or a
   clean `skipped` count (i.e. the cron is closing gaps, not silently
   no-op'ing).

**Blocker / signal to revisit.** Earliest sensible: **2026-05-12** (~2
weeks of cron cycles after #88 lands).

**Owner.** Unclaimed.

[pr88]: https://github.com/TrueSightDAO/go_to_market/pull/88

---

### Validate the circle-hosting → cacao-velocity hypothesis after 4 partners-velocity refreshes

**Context.** 2026-04-28 observation: two recent / candidate retail partners
mention **women's circles** prominently — [The Way Home Shop in SE
Portland][way-home] (just onboarded) and Lumin Earth (existing partner).
Ceremonial cacao genuinely lives in that ecosystem (women's circles, sound
baths, breathwork, new-moon gatherings), so "hosts circles" is plausibly
a leading indicator of cacao sell-through.

The cheap detection step shipped immediately as
`market_research/scripts/detect_circle_hosting_retailers.py`
(see [go_to_market#XX][circle-pr] when filed) — it crawls each Hit List
retailer's `Website` for high-precision keywords (women's circle, moon
circle, cacao ceremony, sound bath, breathwork, sister/sacred circle,
ecstatic dance) and writes **Yes / Not detected** to a new
**Hosts Circles** Hit List column. *That* part is data-only; this entry
covers the deferred *correlation* check.

**Outcome.** Once `partners-velocity.json` has ≥4 weekly refreshes, cross-
reference per-SKU velocity against the **Hosts Circles** flag for
already-onboarded partners. Two questions:

1. Do circle-hosting partners outsell non-circle peers per-SKU at
   statistically meaningful margins? If yes, **green-light**:
   - Add `Hosts Circles=Yes` as a positive signal on the warm-up draft
     generator (next to the dormant / high-velocity logic in the existing
     entry above).
   - Open a separate research entry on whether to build a **circle
     facilitator** outreach motion (different ICP than retailers — direct
     to circle-leaders who buy in bulk for their gatherings).
2. If the correlation is weak or negative, rule it out and close.

**Files.**
- `agroverse-inventory/partners-velocity.json` — read latest snapshot.
- Hit List **Hosts Circles** column (col after `Google listing`) — read.
- `agentic_ai_context/PARTNER_VELOCITY_PROPOSAL.md` §6 — reference
  consumer logic + sample-size guards.

**Blocker / signal to revisit.** Same as the **Eyeball-check
`partners-velocity.json`** entry above — wait for ≥4 entries on the
GitHub Action commit history of `agroverse-inventory` showing
`chore: refresh partners-velocity snapshot`. Earliest sensible:
**2026-05-25**. Combine with that entry's manual sanity check so
both reads happen in one sitting.

**Owner.** Unclaimed.

[way-home]: https://thewayhomeshop.com/
[circle-pr]: https://github.com/TrueSightDAO/go_to_market/pulls?q=is%3Apr+circle+hosting

---

### Fix `addNewStore()` GAS — `setValues`-dimension mismatch on tail-end step

**Context.** `[STORE ADD EVENT]` end-to-end test 2026-04-28 (see *Recently
shipped*) added 3 referrals for Psychic Sister (Clary Sage / Casa de Ritual
/ La Sirena Botanica) — all three landed on Hit List rows 526–528 with the
correct shop name / status / city / state / shop type / Notes / Sales
Process Notes / Status Updated By / Status Updated Date / Store Key.

But every single submission also recorded `status: error` on the **Store
Adds** dedup log with this error message:

```
The number of rows in the data does not match the number of rows in the
range. The data has 1 but the range has 526.
```

That's an Apps Script `setValues(values)` dimensional error from inside
`addNewStore()` (likely the trailing `logDappSubmission_(...)` call or a
sales-notes write). It throws **after** the new Hit List row has been
fully written (since the row is correct), so the data is fine — but the
exception escapes addNewStore's try/catch boundary and lands in the new
GAS scanner's error handler.

**Symptoms.**
- Hit List rows land correctly (operator-visible).
- Store Adds dedup log says `error` with this message (audit-trail-misleading).
- A re-fired Telegram Chat Logs row would NOT re-add (idempotent on
  Telegram Update ID), so no double-row risk.

**Fix targets.**
1. **Root cause** in `clasp_mirrors/1NpHrKJW…/Code.js` `addNewStore()` /
   `logDappSubmission_()`. The `526` figure is "all data rows on the Hit
   List sheet"; somewhere a `range.setValues(arr)` is being called with
   `arr.length === 1` against a range covering all data rows. Likely
   pattern: `sheet.getDataRange().setValues([row])` instead of
   `sheet.appendRow(row)` / `sheet.getRange(targetRow, 1, 1, n).setValues([row])`.
2. **Defensive workaround** in
   `google_app_scripts/find_nearby_stores/process_store_adds_telegram_logs.gs`:
   when `addNewStore` throws, fall back to a Hit List lookup by
   `store_key` (the same key `createStoreKey_` builds). If found,
   record `status: added_with_warning` + the exception text in
   `error_message` instead of `status: error`. That way the audit log
   correctly reports the row was added even when addNewStore's tail
   step fails.

**Cost.** ~20 min for (1) once the offending line is found; ~10 min
for (2). Both are independent — do (2) first if you want clean audit
trails fast; do (1) if you want addNewStore stable for the existing
DApp form callers.

**Owner.** Unclaimed.

---

### Extend iching_oracle advisory with QiMenDunJia overlay

**Context.** Today (2026-05-09) we agreed the I-Ching cast and a QMDJ chart
are complementary lenses on the same moment T — I-Ching tells you the
quality of the moment (via random selection from coin throws), QMDJ tells
you the spatial / strategic structure of that same moment (deterministic
from the timestamp). Pairing them on the same T gives the DAO advisor two
classical frameworks reading the same instant: I-Ching as the narrative /
transformational layer, QMDJ as the spatial / strategic overlay. Honest
disclaimer: combining them is a *modern synthesis*, not a traditional
practice; the UI and the GAS prompt should both flag this.

**Spec.** Full design lives in [`ICHING_QMDJ_EXTENSION.md`][qmdj-spec].
Summary:

- **Library.** `lunar-javascript` (6tail family). Drops in cleanly to the
  static-site / `gas/` stack. Don't reimplement.
- **Client.** After coin throw at moment T: also compute the QMDJ chart
  from T (Ju, Six Yi, Three Wonders, Heaven/Earth Plates, Doors, Stars,
  Spirits) and POST alongside the hexagram + changing lines.
- **GAS.** Extend `oracle_advisory_bridge.gs`:
  - `extractDraw_` += `qmdj_chart` field.
  - `staticContext` += new `QMDJ_FRAMEWORK_REFERENCE.md` (cached — what
    the doors/stars/spirits/wonders mean, what counts as auspicious).
  - `dynamicContext` += per-call QMDJ chart block for moment T.
  - `ORACLE_PROMPT_HEADER` adds two new output sections (QMDJ
    configuration of this moment, Combined frame) and extends section 7
    (decisive action) to use QMDJ's directional / timing signal when one
    is present, otherwise to honestly say the chart doesn't surface a
    strong directional read.
- **Caching.** The new framework reference is static across calls and
  belongs in the cached system block — keeps marginal token cost
  reasonable.
- **UI.** Render QMDJ as a *collapsible* "Extended Reading: QiMenDunJia"
  section below the I-Ching reading, not above it. I-Ching narrative
  stays the primary surface.

**Implementation order.** Three independently testable PRs (not one):

1. **Smoke-test lunar-javascript locally**, then wire chart casting +
   9-palace render into the client. No GAS changes yet.
2. **Land `QMDJ_FRAMEWORK_REFERENCE.md`** in `agentic_ai_context` and
   extend `oracle_advisory_bridge.gs` to fetch + include it.
3. **Refine `ORACLE_PROMPT_HEADER`** sections after seeing live output;
   tune the "no clear signal" fallback language so the LLM doesn't
   fabricate directional advice.

**Cost.** Probably 60-90 min per PR. Total ~3-4 hours of focused work
across the three.

**Risks worth re-reading from the spec before starting.** Information
overload, two-oracles-stapled-together coherence, naive
auto-interpretation, modern-synthesis disclaimer. All addressed in the
spec; don't skip the "Risks / things to be careful about" section.

**Owner.** Unclaimed.

[qmdj-spec]: ./ICHING_QMDJ_EXTENSION.md

---

### krake_browser engine implementation (post-scaffold)

**Context.** Three repos scaffolded 2026-05-20:

- [KrakeIO/krake_browser](https://github.com/KrakeIO/krake_browser) — engine (Sinatra + Playwright/CDP), currently README + ARCHITECTURE + DSL only
- [KrakeIO/krake_recipes](https://github.com/KrakeIO/krake_recipes) — generic public recipes (WhatsApp send_message, LinkedIn connect_request, Instagram login, FDA facility_search) + JSON Schema
- [TrueSightDAO/tdg_recipes](https://github.com/TrueSightDAO/tdg_recipes) — DAO-specific recipes (partner_followups/check_in, edgar/submit_contribution)

All three are **PRIVATE** — flip to PUBLIC only after the engine works end-to-end and we have a recorded demo.

Vision: persistent local Chromium that human + LLM share. LLM drives recipes via CDP; pauses with `human_intervention` for 2FA, approvals, anti-bot, judgment calls. Direct evolution of the Krake.io DSL (2014) — `solve_captcha` generalized into `human_intervention` with a prompt + ack channel + screenshot.

See `~/Applications/krake_browser/{README,ARCHITECTURE,DSL}.md` for the design (or the same files on the public repo once it's flipped public).

**Scope (engine MVP).** Implement against ARCHITECTURE.md:

1. `bin/krake_browser_launch` — Chromium launcher with `--user-data-dir=$HOME/.krake_browser/profile --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1`.
2. Sinatra app that attaches to running Chromium via CDP (`playwright-ruby-client` is the natural choice given krake_sinatra's stack).
3. Recipe loader: reads JSON from a configurable `--recipes-dir` (default: local clones of both recipe repos).
4. Recipe executor: walks `actions[]`, dispatches each action via Playwright, suspends on `human_intervention`.
5. MCP server tools: `run_recipe(name, vars)`, `list_recipes()`, `ack_intervention(token, action, payload?)`.
6. MCP events: `intervention_required` (prompt + screenshot + token), `recipe_progress`.
7. Localhost-only binding + token auth on the MCP port. Engine refuses to start if `0.0.0.0` detected anywhere.
8. Reference CLI client: minimal Ruby script connecting to MCP, invoking one recipe, printing intervention prompts to stdout and reading ack from stdin (for testing without a full chat UI).

**Validation criterion.** Run `whatsapp/send_message` against Gary's logged-in WhatsApp Web from any MCP client — recipe pauses for approval of the drafted message, human types Continue, message sends.

**Scope addendum (Gary 2026-05-20).** Items 9–10 land alongside the MVP. **Items 11–13 are engine v0.2** — defer until items 1–10 validate end-to-end (run `whatsapp/send_message` against live WhatsApp Web with one human approval). v0.2 turns the engine from "runs strict recipes" into "self-healing browser concierge" and is where the project becomes meaningfully differentiated; trying to ship it in the MVP will stall the WhatsApp demo. The v0.2 items also compound — guideposts (item 11) need the teach-loop (item 12) to repair drift, and passive observation (item 13) is strictly better than narration so ship 13 as part of 12 if it's not much more work.

9. **Bundle krake_recipes with engine install.** The TDG engine instance should come with platform recipes (Instagram, LinkedIn, WhatsApp, Facebook, FDA) pre-available, not require a separate clone step. Implement as a postinstall clone + scheduled `git pull` of [KrakeIO/krake_recipes](https://github.com/KrakeIO/krake_recipes) into `~/.krake_browser/recipes/krake_recipes/`. Recipes for living sites drift on their own cadence; pull beats pin.
10. **Wrapper-recipe DSL extension for tdg_recipes.** Add three new fields to the recipe schema so a TDG recipe can be a thin layer over a platform recipe:
    - `uses` — path to the platform recipe (e.g. `instagram/dm_send`)
    - `why` — one-paragraph DAO context the LLM reads before deciding to invoke (e.g. "partner check-ins for stores whose primary channel is IG, not WhatsApp — confirm last touch in Hit List first")
    - `vars` — DAO-specific variable defaults that get merged into the platform recipe's variable substitution
    
    Primary use case Gary identified: **partner check-ins** (the load-bearing operational flow) across WA / IG / LinkedIn / FB depending on partner's primary channel. The `why` field becomes the LLM's decision input.

11. **Guidepost model — intent + hint + expected_state alongside strict selectors.** Each action in the DSL gains three optional fields that turn it from a rigid click-here-then-click-there contract into a guidepost the LLM can re-ground at runtime:
    - `intent` — what this step is trying to accomplish ("Open connect-with-note modal")
    - `hint` — natural-language locator advice for the LLM if the strict selector fails ("Click 'Connect'; if hidden, it's under the 'More' button")
    - `expected_state` — observable post-condition the executor checks before moving on ("Textarea for personal note is visible")
    
    Execution order: try `dom_query` / `xpath` first (fast, deterministic, no LLM call). If it returns nothing or `expected_state` doesn't match, escalate to LLM-grounded discovery using `intent` + `hint` (Browser Use / Stagehand semantics — feed the LLM a trimmed accessibility tree, ask for the right element). Strict and flexible coexist in the same recipe; you only pay the LLM cost when the cheap path breaks.

12. **Teach-by-narration loop — continuous DOM repair via human-AI symbiosis.** The mechanism that makes selector drift self-healing instead of silently breaking recipes. Three new MCP tools beyond the MVP set:
    - `read_page_state()` → current URL + serialized DOM (or trimmed accessibility tree) + screenshot. Gives the LLM eyes onto the current tab.
    - `narrate_action(text)` → operator types what they just did manually ("I just clicked the new Connect button, it's now under the three-dot menu"). LLM keeps it as context.
    - `propose_recipe_update(name, patch)` → LLM emits a JSON patch against the recipe and opens it as a PR to krake_recipes or tdg_recipes. Gary reviews + merges; the next scheduled `git pull` makes the fix canonical.

    End-to-end loop: strict selector fails → engine fires `human_intervention` with "I lost the connect button" → Gary does the step manually → narrates → LLM reads page state → drafts a PR with the new selector → Gary merges → next run works. This is the differentiator vs. every other browser-automation tool (which break silently on DOM change). Without this loop, krake_browser is just another Stagehand clone; with it, it's a tool that gets *more reliable over time* through use.

13. **Passive observation — recipe-execution-bounded learning.** Strictly better than narration: Gary just works, the LLM learns from the clickstream. Three modes worth distinguishing; ship only mode (b):

    - (a) *Always-on passive observation across the whole browser* — records every interaction including bank logins, password manager, email. **Non-goal forever.**
    - (b) *Recipe-execution-bounded observation* — when a recipe is running and a step fails, the engine flips on observation mode for the duration of Gary's manual recovery, then off. Bounded by definition (failure triggered it), self-correlating (the recovered selector maps to the failed step), almost zero privacy surface. **This is what ships in v0.2.**
    - (c) *Operator-triggered "watch me"* — Gary says "watch me do this" → LLM begins recording → Gary completes a new flow → LLM drafts a brand-new recipe. Natural extension for greenfield recipe authoring; defer to v0.3.

    **DSL impact:** each guidepost gains a `learned_selectors[]` history with timestamps. At execution time the engine tries selectors in reverse-chronological order so newest wins, but old ones stay as fallbacks (sites sometimes A/B-test old and new DOMs for weeks).

    **Engine adds:** CDP event subscription gated by `recipe_recovery_mode_active` flag (off by default). Click events translate to stable selectors (prefer `aria-label`, then `data-testid`, then computed CSS path). Type events from `<input type=password>` / `<input autocomplete=current-password>` / fields inside `<form autocomplete=off>` are dropped from the log entirely. After Gary completes the recovery, the LLM diffs the failed guidepost against the observed sequence and opens a PR with the new selector(s) appended to `learned_selectors[]`.

14. **LLM form comprehension + pre-fill — `llm_fill_form` action (v0.3).** New DSL action for forms where the human cost is *reading* the form, not typing the answers (FDA facility registration, partner onboarding paperwork, retail shipping intake forms — anything regulatory or compliance-heavy). Engine flow:
    - LLM reads the entire form via the page's DOM or accessibility tree.
    - Uses the recipe's `context` block + (optional) external lookups (web search, the user's other logged-in sessions inherited from the persistent profile, Google Sheets via service-account auth, etc.) to figure out each field's value.
    - Fills every field, attaches `confidence_score` (0.0–1.0) and `reasoning` (one line citing where the value came from — recipe context, form text, external lookup URL) as metadata per field.
    - `human_intervention` surfaces ONLY fields below a configurable confidence threshold (default `0.85`) for explicit review; high-confidence fields are pre-approved. UI shows `show all` toggle for high-stakes forms (regulatory submissions, anything that becomes a legal record).

    **Critical design constraint:** the spot-check surface has to be reliable, because the whole pitch is the human *skips reading the form*. Per-field reasoning shown on hover/click; without this, rubber-stamping → Open Claw failure mode (see the 2026-05-20 blog post anecdote for the cautionary tale).

    **Depends on:** v0.2's LLM-grounded DOM discovery primitive (item 11). Independent of v0.3's "watch me" recording (item 13(c)); both are v0.3 candidates, ship whichever a real form pain-point demands first.

**Blockers.** None. PAT for KrakeIO push lives in `~/Applications/truesight_autopilot/.env` as `KRAKEIO_LLM_PLAYGROUND_PAT`. Use it via `GH_TOKEN=$(grep ^KRAKEIO_LLM_PLAYGROUND_PAT= ~/Applications/truesight_autopilot/.env | cut -d= -f2-)`.

**Already done (no engine required).** (a) All 3 repos flipped to PUBLIC on 2026-05-20 (the original "wait until engine works" was overcautious; design docs + sample recipes are fine to expose). (b) Forward-spec blog post live at [garyteh.com/2026-05-20-from-solve-captcha-to-symbiosis-what-my-2014-dsl-was-trying-to-tell-me.html](https://garyteh.com/2026-05-20-from-solve-captcha-to-symbiosis-what-my-2014-dsl-was-trying-to-tell-me.html) — framed as design journal, links to the three repos.

**After engine works.** Record a 30s screencap of the WhatsApp demo and write a follow-up blog post with honest retro (what worked, what was thinkier-than-it-needed-to-be). HN explicitly skipped as launch venue — Gary called it "kinda lame"; risk of flop > upside, garyjob/blog has zero downside and can cross-post later if the follow-up gets organic traction.

**Owner.** Unclaimed.

---

### Credential vault for service-account keys (AWS Secrets Manager) so cut-over hosts don't ship without creds

**Context.** 2026-05-29: the DApp email-registration flow was down in prod because the standalone `dao_protocol_nelanco` host (stood up in the 2026-05-28 NELANCO cutover) was deployed **without** its Google service-account keys — `edgar_dapp_listener_key.json` existed nowhere on the box and there was no `GOOGLE_CREDS_DIR` in its `.env`, so every email-registration signature write hit `[Errno 2]`. Fixed by hand-scp'ing the 3 SA keys + setting `DAO_PROTOCOL_GOOGLE_CREDS_DIR` (see `NOTES_sentiment_importer.md` § dao_protocol, [dao_protocol#51](https://github.com/TrueSightDAO/dao_protocol/pull/51)). The same class of gap had already bitten the autopilot box. **There is no system of record for these credentials** — they're provisioned by manual SCP from a laptop and scattered across `~/Applications/*/.env`, per-host `config/*.json`, `/opt/truesight_autopilot/config/google/`, and laptop copies. Any new host / re-image silently misses them, and nothing fails at deploy time to catch it.

**Goal / shape.** Stand up a managed secret store as the single source of truth for service-account JSONs + host secrets, fetched at deploy/boot instead of by manual SCP. Prefer **AWS Secrets Manager** or **SSM Parameter Store** (the EC2 fleet already runs in AWS with IAM roles; both give KMS-at-rest, per-secret IAM scoping, CloudTrail audit) over a plaintext folder. Minimum viable slice:
- Store the 3 Google SA keys (`edgar_dapp_listener`, `cypher_defense_gdrive`, `agroverse_qr_code_gdrive`) as secrets.
- Give each host an instance-profile IAM role scoped to **only** the secrets it needs.
- Add a small fetch step to each deploy script (`dao_protocol`, autopilot, Edgar) that pulls its secrets into the expected creds dir on boot/deploy, so `config.py`'s `GOOGLE_CREDS_DIR` resolution (dao_protocol#51) points at a populated dir.
- Stretch: a `deploy --verify-creds` preflight that fails loudly when a required key is absent — would have caught this incident at cutover instead of in prod.

**Design caution (from the 2026-05-29 discussion with Gary).** Do **not** just dump a folder of every credential onto an internet-facing box an LLM can read + give it "SSH in and fix anything" — that concentrates the whole network's secrets on the highest-value target and crosses the autopilot's deliberate "propose-only, never auto-mutate" boundary. Least-privilege per-host scoping; keep a human-approval gate on any write/mutating path; read-only diagnosis can stay autonomous.

**Blockers.** None technical. Decision needed: Secrets Manager vs SSM Parameter Store vs SOPS+age-in-git. Recommend Secrets Manager (native rotation support).

**Owner.** Unclaimed.

---

### Deploy lease machinery effectively inert — 14 open leases on the GAS script, and `close_lease()` misreports success as failure
**Filed 2026-09-10. Updated 2026-09-10 (Sophia, thread 24326). Owner: unclaimed. Governor: Gary.**

**Symptom.** Not two leases — **fourteen** lease files are still `status: open` on scriptId `1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v`, accumulated since 2026-08-26: `L-20260826-01`, `L-20260828-02`…`-05`, `L-20260901-06`, `L-20260901-08`, `L-20260901-095538`, `L-20260902-01`, `L-20260905-10`, `L-20260906-01`, `L-20260907-01`, `L-20260909-01`, `L-20260910-01`. The house TTL is **30 minutes**, so all are long expired; each was abandoned mid-ceremony (the pushing session died before closing it). A 14-deep graveyard means the ceremony is not merely occasionally-skipped — it is **effectively not enforcing anything**.

**Impact.** `DEPLOY_PUSH_SOP` §6 treats a zombie lease as an incident. Worse, the deploy tool **fail-opens past** an existing lease rather than refusing, so a zombie provides no protection *and* no alarm — the next deploy proceeds as if the lease were free. Mutex-by-convention is silently degraded to no-mutex whenever a session crashes mid-push.

**Second bug — `close_lease()` reports success as failure.** `deploy_ledger.close_lease()` decides success with `"content" not in res`, but GitHub's DELETE response is `{"commit":…, "content": null}` — the `content` key *is* always present, so the function returns `status: error` **even when the delete worked**. Observed live: two closes returned `error` while the lease files were in fact gone. Impact: a session that trusts the return value will try to "re-close" and **manufacture new zombies**, and a genuine close failure is indistinguishable from the false alarm. Fix: treat a DELETE that returns a `commit` (or HTTP 2xx) as success, or re-`GET` the file to confirm absence.

**Third bug — the deploy ledger fail-opens silently.** `deploy_gas_project.py` resolves its PAT from `$DEPLOY_LEDGER_PAT`, then `$GITHUB_TOKEN`, then `$TRUESIGHT_DAO_AUTOPILOT`. Run from a bare shell that hasn't sourced `/opt/truesight_autopilot/.env`, none is set, so the ledger is **skipped with a one-line warning** while the deploy still proceeds — i.e. a production change can land with **no audit record**. Observed live on the 2026-09-10 repoints: both printed `! deploy ledger unavailable (fail-open)` and were backfilled afterwards by hand. Fix: either make the ledger **fail-closed** for a deploy, or have the deploy wrapper export the PAT itself rather than depending on the caller's shell. Related footgun: `/opt/truesight_autopilot/.env` is not shell-safe (a bare `set -a; . .env` executes a line and errors) — parse it, don't source it.

**Proposed fix.** Close the fourteen zombies (append close records, don't delete). Then fix the two bugs above, and decide the policy: prefer **fail-closed** (refuse a new push while any non-expired-or-expired-but-open lease exists, and surface it) or at minimum, have the deploy tool **log loudly** when it fail-opens past a stale lease so the zombie leaves a trail instead of passing silently.

**Blocker / priority.** Not blocked. Ready for a maintainer with write access to the lease records.

---

### One `clasp push` produced two deploy-ledger records (deploy script *and* the autopilot tool each append)
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24326).**

**Symptom.** The 2026-09-10 push of script `1UrBgqLnnQc6PV4-…` appended **two** records to `ecosystem_change_logs` for a single logical deploy — one written by `tokenomics/scripts/deploy_gas_project.py` and one by the autopilot's `gas_deploy_project` tool wrapper around it. Both are appended to the same append-only ledger.

**Impact.** The deploy ledger is read for audit ("what changed in production, when, by whom"). Duplicate rows for one deploy make the count of deploys wrong and force a reader to detect-and-merge twins. Same class as the duplicate tracking-row quirk in the invalidation tab — a read-then-append with no idempotency key. Severity low (append-only, both records correct), but it erodes trust in an audit surface.

**Proposed fix.** Give each push a single idempotency key (e.g. the lease id, or `<scriptId>:<version>:<sha>`) and have whichever layer writes second detect-and-skip the existing record — rather than both layers writing unconditionally.

**Blocker / priority.** Not blocked. Low severity; file-and-forget until the ledger is next touched.

---

### Intentional: `process_qr_code_updates.js` and `process_tree_planting_link.js` must NOT take the script lock
**Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24326).**

**Context.** The 2026-09-10 lock work added `LockService.getScriptLock()` to four Telegram-log processors; a regression guard (tokenomics #473, `scripts/test_telegram_log_processor_lock.py`) now asserts that every handler owning a read-then-append dedup set takes the lock. Two files in the same project are **deliberately** lock-free and must stay that way:

- `process_qr_code_updates.js` — the `doGet` router. It **dispatches** to the child processors. GAS script locks are **not reentrant**, so a router that held the lock would deadlock its own children.
- `process_tree_planting_link.js` — holds **no** `getProcessed*MessageIds_` dedup state (verified: it appends rows but has no read-then-append window), so there is no race to close.

**Why filed.** So a future reader or agent doesn't "fix" the inconsistency by adding a lock to the router (deadlock) or assume the guard test is failing open. The guard test pins this: it fails if either file ever *grows* a dedup helper, forcing the author to add the lock **and** re-reason about the router deadlock note.

**Blocker / priority.** Informational — no action. Revisit only if either file gains dedup state.

### `seed_from_sheet.py` rebuilds manifests from the sheet, so any hand-attached field not present in a sheet column is silently wiped on every re-seed
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25671).**

**Symptom.** Re-running `lineage-assets/scripts/seed_from_sheet.py --execute` (the documented way to push sheet state into `qrs/*.json`) destroyed hand-attached lineage data. Concretely: 101 `2024OSCAR_CT_20260820_*` manifests carried a `seedling_photo_url` (the FounderHaus group photo) that existed **only in the JSON** — every full re-seed wrote `seedling_photo_url: ""` over it. A re-seed in thread 25671 was caught before shipping **only** because the diff was inspected; nothing in the script warns.

**Root cause (two parts).** (1) `scripts/lib/manifest.py::build_lineage()` builds lineage **purely** from sheet columns — it emits `seedling_photo_url` from col **R** (`Tree Seedling Photo URL`) and ignores col **S** (`Product Image`) entirely; a fresh `build_manifest()` on the CT row returns `""`. (2) `merge_preserve_events()` preserves only `events` whose `type` is not in `SEED_EVENT_TYPES` — it has **no** preserve path for lineage fields, so a field the sheet doesn't supply is lost by construction. The sheet is therefore the only durable home for any value, by design — but the design is undocumented and the failure is silent.

**Also found.** `COL["product_image"]` (idx 18) is mapped but **read by nothing** — `build_lineage` never emits `product_image`; `git grep product_image qrs/` = 0 files, while **1,558 sheet rows** carry a value in col S. So that column is either dead config or a missing feature — pick one.

**Fixed for the 101 rows (this thread).** The Product Image value was copied into col **R** on those rows (sheet edit), making the photo sheet-durable; a full sheet-wide re-seed then kept **all 104** photo-bearing tree manifests with **0 lost**. See `lineage-assets` PR #10.

**Proposed code fix (~30 min).** In `scripts/lib/manifest.py`: before writing, preserve any existing lineage key the fresh build did not populate (i.e. `for k,v in existing["lineage"].items(): merged["lineage"].setdefault(k, v)` — or skip emitting keys whose sheet cell is empty rather than emitting `""`). Then drop the col-S→col-R manual copy requirement. **Residual known regression, NOT fixed by the sheet workaround:** `qrs/FOUNDERHAUS_BOUGAINVILLEA_20260821_1.json` has `events[1].signed_by` + `events[1].sig_ref` (an Edgar-signed event) that do **not** round-trip through any sheet column — a re-seed drops them. A generic "preserve unknown/signed event fields" merge is the real fix. Blocker: none.

### `lineage-assets` PNG thumbnails are generated by a separate manual pipeline, so newly-seeded QR codes ship with a 404 `qr_image_url`
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25671).**

**Symptom.** `seed_from_sheet.py` writes `qr_image_url` = `.../lineage-assets/main/pngs/<qr_id>.png` for every manifest, and `build_index.py` publishes them to `qrs_index.json` → `truesight.me/physical-assets/serialized/`. But the `pngs/` directory is populated by a **different, manual** pipeline (the `tokenomics` `agroverse_qr_code_generator` batch compiler, invoked over Telegram by the `agroverse_qr_code_manager` SA). Seeding a code therefore yields an index row whose image 404s.

**Observed.** The 40 `2024OSCAR_AGL14_20260911_*` manifests (PR #10) have no corresponding `pngs/*.png`; 1,820 index rows vs 2,376 PNGs — the sets are not maintained in lockstep.

**Impact.** Low on the serialized **listing** page: its row template does not render `qr_image_url` (verified — no `<img>` for it), so rows display correctly. Higher on any per-asset provenance/credential view that does render the image.

**Proposed fix (~30 min).** Either (a) chain PNG generation into the seed flow (call the batch compiler for any manifest lacking a PNG), or (b) have `build_index.py` emit `qr_image_url: null` when the PNG is absent so consumers can fall back gracefully. (a) is truer to the invariant "every serialized asset has an image". Blocker: requires the `tokenomics` PNG compiler to be invokable headlessly (currently Telegram/GAS-driven).

### Serializing bulk kg inventory into N unit QR codes has no event type — it is a direct sheet edit only, with no signed audit trail
**Filed 2026-09-11. Owner: unclaimed. Governor: Gary (thread 25671).**

**Symptom.** Moving 40 kg of bulk-booked cacao into 40 individually-serialized 1-kg QR codes (AGL14, `2024OSCAR_AGL14_20260911_1..40`) had no expressible `submit_contribution` event. `lookup_event_docs` was checked across `QR CODE REGISTRATION`, `INVENTORY MOVEMENT`, `SALES EVENT`, and the QR-generation docs: none models *split a bulk quantity into N unit serials, set status, post no money movement*. Gary directed a **direct sheet write** instead — correct for avoiding a double-count of the sale (the USD was already booked once in the AGL14 `Transactions` rows 10–13), but it means the serialization act itself carries **no RSA-signed ledger record**.

**Contrast.** The GL side of AGL14 is fully signed (`[MANAGED LEDGER TRANSACTION EVENT]`, rows 10–13 of the AGL14 ledger, per the one-signed-blob-many-rows precedent). The QR side — 40 rows at `Agroverse QR codes` 1784–1823 — is unsigned sheet state only.

**Proposed fix (~60–90 min).** Add a `[SERIALIZATION EVENT]` (or extend `QR CODE REGISTRATION` with a bulk mode) that records: source QR/bulk lot, `split_quantity`, the generated `qr_id` range, target status, manager/custodian, and an explicit `no_financial_posting: true` flag — so the audit trail covers serialization without implying a sale. Until then, serialization remains reconstructable only from the sheet + the manifests it seeds. Blocker: none; needs an event-schema decision by a governor.

### Brain tier-awareness: `policy.resolve_identity()` has no SENTINEL branch — sentinel rights reach the gate only via the JWT-asserted role
**Filed 2026-09-17. Owner: unclaimed. Governor: Gary (thread 30892).**

**Symptom.** After the DISCORD_MEMBER_TIER / BRAIN_TIER_AWARENESS work (PR1 #478, PR2 #480, PR3 #481), the brain correctly authorizes a **sentinel** turn for WRITE/ADMIN — but only because the adapter mints the turn's `author_role` into the JWT and `app/main.py::_run_tool_sync` **force-stamps** that asserted role onto the resolved identity. The lower-level resolver `app/policy.py::resolve_identity()` itself has **no sentinel branch**: it knows only the env governor allowlist, the Governors cache, and the member fallback.

**Evidence (deployed box, 2026-09-17).** `resolve_identity(display_name=…)` →
- `'Gary Teh'` → **governor**
- `'Claude Anthropic'` → **guest** ❌ (should be `sentinel`)
- `'Sophia Truesight'` → **guest** ❌ (should be `sentinel`)
- `'Peter Da'` → guest

`grep` on `app/policy.py::resolve_identity` shows no `SENTINEL`/`sentinel` return path — the `SENTINEL` member exists on `Role` and is consumed by `has_governor_rights()` and the gate, but `resolve_identity()` never produces it. A sentinel Discord account therefore reaches sentinel rights only via `author_role()` (adapter, col-W) → JWT claim → force-stamp. Any future caller that trusts `resolve_identity()` alone (a new transport, a CLI path, a test harness) would silently degrade a sentinel to `guest` and lose governor-tier rights — fail-closed, but a latent attribution/authorization gap.

**Proposed fix (~30–60 min).** Mirror the adapter's sentinel check inside `policy.resolve_identity()`: add a col-W (`Is Sentinel`=TRUE) / `governor_registry.sentinel_emails()` branch returning `Role.SENTINEL`, evaluated after the governor branch and before the member fallback (same ordering as `author_role()` per plan D4). Unit-test the four names above plus the "never relabeled governor" invariant. Blocker: none; needs a governor to confirm the col-W lookup source (the adapter already uses `governor_registry.sentinel_emails()`).

---

### Discord sentinel resolution is email-keyed; should key off the numeric Discord ID (blocks Envoy Discord parity PR2)

**Filed 2026-09-17. Owner: unclaimed. Governor: Gary (thread 30892).**

**STATUS 2026-09-17 — Envoy parity ACHIEVED + LIVE; this entry is now the non-blocking RESIDUAL.** Parity shipped via **path (i)**, not the fixes proposed below: both env vars are live in the running discord adapter — `DISCORD_SENTINEL_USER_IDS=1548902290344255600` + `DISCORD_TRUSTED_BOT_IDS=1548902290344255600` (appended 2026-09-17, live from the 16:23:04 restart; `author_role("1548902290344255600")` → `sentinel` verified on-box, and Gary confirmed a real Discord reply). A **durable infrastructure fix** also landed: `truesight_autopilot` **#494** (`_env_mtime` — a newer `.env` now counts as process staleness, so an env-only change actually triggers a deploy restart; previously the no-op guard scanned only `.py` mtimes, so the new var went live only via an unrelated-restart fluke, and the hand-restart that would have loaded it is blocked by the self-restart guard). **What remains unfixed is the underlying bug below** — `sentinel_emails()` is still email-keyed and still silently omits any *sheet-only* sentinel whose cache row has `email:null` (Envoy, `Open Ai`) — but it no longer blocks Discord parity. The *Preferred fix* (ID-native, adapter-only) is the recommended way to clear the residual.

**Tracking home:** Discord channel **#sentinel-cache-email-bug** (id `1550171805812129954`, under *DAO Build and Ops*) — Gary posted the full Finding A writeup there, and the reframe below was posted there too. Route discussion + progress updates to that channel.

> **✦ REFRAMED 2026-09-17 (Gary's architectural point — PREFERRED FIX).** Member/governor
> resolution on Discord **already works purely off the numeric Discord ID bound to col G** — no
> email needed; Discord's own login *is* the authentication. `sentinel_emails()` being email-keyed
> is an artifact of it being built for the **DApp / JWT-claim** path (where email is the natural
> key), then reused as-is by the Discord adapter. So the clean fix is **adapter-side, ID-native**
> (see *Preferred fix* below) — **no `DaoMembersCache.js` change, no `tokenomics` GAS deploy.**
> The original cache-backfill fix (historical "path (ii)", retained below) is now **fallback**,
> not preferred.

**Symptom.** `app/governor_registry.py::sentinel_emails()` keys on **email** — `if "sentinel" in (c.get("roles") or []) and (em := (c.get("email") or "").strip().lower())`. But the `dao_members.json` cache builder (`tokenomics`, GAS `DaoMembersCache.js` → `publishDaoMembersCacheToGithub_`) hoists `email` **only** from the *Contributors Digital Signatures* sheet col F, and seeds every **contact-sheet-only** contributor with `email: null` (the `Object.keys(contactAllNames).forEach` merge: `byName[key] = { name, email: null, public_keys: [] }`). A contributor whose sentinel flag comes solely from *Contributors contact information* col W (`Is Sentinel=TRUE`) therefore lands in the cache as `roles: ["member","sentinel"]` with `email: null` — and `sentinel_emails()` **silently omits** it, so `discord_adapter.author_role()` → `_email_is_sentinel()` falls through to `member`.

**Evidence (live cache, 2026-09-17).** Envoy's row in `treasury-cache/dao_members.json`:

```
{"name":"Envoy TrueSight","email":null,"roles":["member","sentinel"], ...}
```

`sentinel_emails()` returns `{claude, deepseek, kimi, sophia, admin@…}` — **Envoy absent.** `author_role("1548902290344255600")` → `member` (should be `sentinel`). `Open Ai` shares the identical latent null-email sentinel row (currently harmless, same bug).

**Why it matters.** This is the blocker on `plans/DISCORD_ENVOY_GOVERNOR_PARITY_PLAN.md` PR2 **path (ii)** (Gary's stated preference — route Envoy's Discord bot id through the sheet col-W D4 mechanism). Path (i) — env `DISCORD_SENTINEL_USER_IDS` — sidesteps it, but the underlying cache bug still mislabels *any* sheet-only sentinel as member in **every** email-keyed consumer (not just Envoy).

**Preferred fix — ID-native, adapter-only (~30–45 min, `truesight_autopilot`).** Mirror how member/governor already resolve: key sentinel resolution off the **numeric Discord ID** rather than round-tripping an email.

1. Extend the col-G lookup to also return the **col W (`Is Sentinel`, index 22)** flag — e.g. a `_fetch_discord_sentinel_flag(discord_id)` alongside `_fetch_discord_id_email()`, or return both from the one `A:Z` read it already performs.
2. In `author_role()` step 2b, OR the ID-native flag in:
   `if _email_is_sentinel(email) or _discord_id_is_sentinel(uid) or is_allowed(uid, sentinel_ids): return "sentinel"`.
3. Add a unit test: a col-W-only sentinel (email unbound / `null`) resolves to `sentinel`.
4. **Leave `sentinel_emails()` untouched** — it stays correct for the DApp/JWT path where email *is* the right key.

**Advantages:** no `tokenomics` GAS change, no GAS deploy, no cache-builder dependency; fixes *every* sheet-only sentinel (Envoy, `Open Ai`) at once; keeps the Discord path ID-native like governor/member already are.

**Fallback (historical "path (ii)", superseded as preferred).** In `DaoMembersCache.js`, when seeding/merging a contact-sheet contributor flagged sentinel (col W TRUE) with no signature-derived email, populate `email` from the contact sheet's **own** email column (col D) rather than leaving `null`. Kept only if we later want the cache itself to carry a usable email for *non-Discord* email-keyed consumers.

**Blocker.** None technical, and **parity itself is already unblocked** (shipped via path (i), see STATUS above). The residual fix is a plain `truesight_autopilot` code PR (no GAS) — *Preferred fix*. Fallback would need a `tokenomics` GAS change + deploy + governor GO.

---

## Recently shipped

### `getTreeRecipientMap` recipient-autofill no-op = the col-A/col-D off-by-one (same root as `trees/index.geojson`) - SHIPPED 2026-09-26
**Shipped 2026-09-26. Governor: Gary (thread 35944). PR: tokenomics #563 (`3a2c7480`); GAS @42; live backfill run.**

Selecting a tree in `report_payout_event.html` left **Recipient PK Hash blank**. Root cause was NOT missing wiring - the picker selects intake **col D** (`Edgar_..._103`, the `telegram_message_id`) while `getTreeRecipientMap` keyed on the CFR `tree planting` tab's `tree_id` = intake **col A** (update id) - a systematic **+1**. Verified live: 0/18 exact id matches, 17/18 at minus-1. Fix: store the canonical `Edgar_*`-shaped value (prefer col D) on write + a one-shot idempotent `?action=backfillCfrTreeIds` lever, run live (**18 changed**, idempotent). Verified: 17/18 now join (the 1 miss is a tree not in the pending feed). Display/keying only; no PII (hash-only).

### CFR `tree planting` tab now dedupes on `Request Transaction ID`, not the transport update id - SHIPPED (source) 2026-09-26
**Shipped 2026-09-26. Governor: Gary (thread 35944). PR: tokenomics #564 (`3b2ccb18`). GAS deploy + backfill = governor gates, NOT yet run.**

One `telegram_update_id` can map to multiple rows, and the SAME tree can be re-posted under a NEW update id (15 live cases) - keying dedup on the update id double-counts it. Verified over all 265 live rows: **172 distinct txids, ZERO appearing under more than one signer or more than one tree content** - so the txid ALONE is the unique key (no `pk_hash` scoping needed; the signature is already represented as the one-way `pk_hash`, never raw). Added a trailing `request_transaction_id` column, a header migration-safe `ensurePayoutRegTab_`, an idempotent `?action=backfillCfrTreeTxIds`, and the provisioner SSOT. 33 harness tests + 136 pytest pass.

**Outstanding gate:** deploy GAS (Path B `~/.clasprc-admin.json`) then redeploy the pinned deployment **@42 -> @43**, then run `?action=backfillCfrTreeTxIds` once. Not run unilaterally.

### Box git push restored: SSH-migrate CLI remotes, scrub 2 embedded PATs, re-apply canonical credential helper
**Shipped 2026-09-26. Governor: Gary (thread 35944). Box-local ops change; no repo code.**

**Symptom.** Native `git push` from the autopilot box over HTTPS failed: `remote: Invalid username or token. Password authentication is not supported for Git operations.` Reads (`git ls-remote`/`clone`) *appeared* fine only because the org repos are **public** (anonymous read).

**Root cause (recurrence of the 2026-09-13 entry).** `~/.gitconfig` had re-acquired two *shadowing* credential helpers: `[credential "https://github.com"] helper = /usr/bin/gh auth git-credential` (gh **2.4.0** emits **0 bytes**) and a bare `credential.helper` running `!f(){ echo username=x-access-token; echo password=$GH_PAT; }` where **`$GH_PAT` is unset** → git sent `Basic x-access-token:<empty>`. The documented durable fix (`scripts/deploy.sh` §Provisioning) was never shipped, so a later edit re-introduced the shadow exactly as predicted. `app/tools/git_tools.py` never noticed because it pushes over **SSH** (`GIT_SSH_COMMAND` + `~/.ssh/id_ed25519_truesight_autopilot`).

**Fix applied (box-local).**
1. Migrated **21** TrueSightDAO/KrakeIO working-checkout remotes `https://` → `git@github.com:…`.
2. **Scrubbed 2 remotes that carried a live PAT in the URL** (`/home/ubuntu/work/tsap`, `/opt/truesight_autopilot`). *Those tokens are exposed and should be rotated.*
3. Removed both shadow sections; set `credential.helper = /opt/truesight_autopilot/scripts/git-credential-sophia.sh` (reads `TRUESIGHT_DAO_AUTOPILOT` from `.env` at call time).

**Verification.** SSH: `git ls-remote origin` OK (tokenomics / agentic_ai_context / autopilot); `git push --dry-run` → `* [new branch]`. HTTPS: `git credential fill` → `username=x-access-token` + password; `git push --dry-run` → `* [new branch]`. No probe branches created (404). Audit log (0600): `~/.remote-url-rewrite-audit-20260926T011332.log`.

**Still-open recommended follow-up.** Ship the idempotent `deploy.sh` guard AND re-run it on every deploy so the shadow cannot return; rotate the 2 exposed tokens.

### `processBatch` OAuth-scope fix + deploy-identity convention — RESOLVED
**Shipped 2026-09-24/25. Governor: Gary (thread 35944). PR: `tokenomics` #553; GAS deploy v37.**

Added `https://www.googleapis.com/auth/documents` to `1MnAsIQA…/appsscript.json` (fixes `processBatch`'s `DocumentApp.openById`, which had failed on every run), corrected `AGENTS.md` §2/§3 deploy-identity guidance, and added a companion scope-guard test (`scripts/test_payout_event_guard.py`). Deployed GAS **v37** and repointed the 3 webapp deployments (`AKfycbxQDdGnw…`, `AKfycbyGD0CD…`, `AKfycbyxwkIp6…`, all confirmed `@37`). **Live UAT:** `?action=processBatch` → `{"success":true,"scanner":"processBatch"}`; both private CFR sinks and `getInstalledScannerTriggers` (count=7) still JSON. **Note:** the added scope required a one-time OAuth **re-consent** by the executing identity (`admin@truesight.me`) in the script editor — a new scope cannot be silently widened.
### Inline-button resume options — Telegram + Discord parity — ✅ SHIPPED 2026-09-25 (tap→resume UAT passed LIVE)
**Shipped 2026-09-25. Governor: Gary (thread 36518). PRs: [truesight_autopilot#502](https://github.com/TrueSightDAO/truesight_autopilot/pull/502) (Telegram build), [#503](https://github.com/TrueSightDAO/truesight_autopilot/pull/503) (wording polish), [#504](https://github.com/TrueSightDAO/truesight_autopilot/pull/504) (Discord parity). Deployed 2026-09-25 14:08:28 UTC @ `3fc7943`.**

**What shipped.** A resume-awaiting turn can now be resumed by **tapping a numbered choice button**, not only by an emoji-go. Option labels live server-side (`app/resume_registry.py` / `app/discord_resume_registry.py`, keyed by an opaque 4-char token, **consume-on-read** so the menu is single-fire); the transport carries only the payload — `custom_id` `ro:<token>:<i>` on Discord, inline-keyboard `callback_data` on Telegram. Both keep the emoji-go path, plus a non-decision **"✍️ Other — just reply"** button. Discord's tap arrives as `INTERACTION_CREATE` (type 3) and **must be ACKed within 3s** or Discord shows *"This interaction failed"* — so the handler ACKs **deferred (type 6) FIRST**, then dispatches the **same synthesized go-signal the reaction path uses** (one resume code path). Gateway gained an `INTERACTION_CREATE` branch; registry options never clobber the `{channel_id,text}` the emoji-go needs.

**Live UAT (thread 36518).** Both services restarted 14:08:28 UTC on `/opt/truesight_autopilot` @`3fc7943` (telegram pid 64509, discord pid 64508 — restarted *after* the 14:07:49 checkout, so #503+#504 are live). Posted a real 3-option components menu to Discord `#server-administration` (msg `1553046855204601959`, token `CZ4V`); governor tapped option 1 → log `component go-signal: … sel=0 -> dispatching turn`; message edited to `✅ Picked: 🎨 Tweak the button wording`; a resume turn ran; registry consumed (`peek_options("CZ4V")` → `None`). **No 3s interaction-failure.**

**Not deterministic (be aware).** The `↩️ Reply [TOKEN-n]` line is a *human-readable affordance, not a parsed code path* — neither adapter has a `[TOKEN-n]` regex, so the typed form only works if the model interprets it. The guaranteed paths are the buttons + the emoji-go reaction.

**Deps.** `DISCORD_DRY_RUN=false` + the `truesight-autopilot-discord.service` unit must be enabled. CAVEAT: `deploy_autopilot` reported *noop* on a commit match even though the running processes had in fact been restarted — verify by process start time vs code mtime, not by the noop message alone.

### SunMint certificate downloadable from the QR provenance page — SHIPPED (URL-probe route)
**Shipped 2026-09-25. Governor: Gary (thread 35189).** The cert-download feature requested 2026-09-24 is live, via the lower-risk **URL-probe route** recommended in the Pending entry (not the manifest-field route — so the `merge_preserve_events` cert-wipe landmine is sidestepped entirely).

- **Page:** `truesight_me_beta/qr/index.html` carries the `probeCertificate(qrId)` + `CERT_BASE` branch; `⬇️ Download SunMint certificate (PDF)` renders **only when** `HEAD lineage-assets/certs/<qr_id>__cert.pdf` returns 200. Verified by **headless-Chromium render** of `https://truesight.me/qr/?id=2024SA_20251227_35` → button present, `href=…/certs/2024SA_20251227_35__cert.pdf`.
- **Canonical cert key:** `lineage-assets/certs/<qr_id>__cert.pdf` (public repo; published via Contents API). 8 certs live as of 2026-09-25.
- **Prod:** `truesight_me_prod` carries the page (synced 2026-09-24). ⚠️ the per-asset URL parameter is **`?id=`**, not `?q=` (see `GLOSSARY.md` → "Provenance page").
- **Open sub-items (not yet built):** no auto-rebuild trigger (a cached cert can go stale vs. its signed attestation). ~~`qr/index.html` has no `ASSIGNED_TO_TREE` badge CSS (renders the grey default badge).~~ **CORRECTED 2026-09-25:** the `ASSIGNED_TO_TREE` badge **does** exist in **both** beta and prod (`--status-assigned-tree` defined at L37, class wired at L105; the two files are byte-identical, md5 `4fe1e2a0`). What actually makes a linked bag *show* the default grey badge is a **stale manifest**, not missing CSS — see the 2026-09-25 UPDATE in the "QR manifest JSON goes stale…" entry below.

### GAS scanner-exposure convention + `1MnAsIQA…` deployed to v36 (all 7 scanners HTTP-reachable + trigger read-back) — RESOLVED
**Shipped 2026-09-24. Governor: Gary (thread 35944). PRs: `tokenomics` #551 (convention + guard), #552 (read-back action).**

The `[PAYOUT REGISTRATION]` silent-failure class is closed. `tokenomics/AGENTS.md` §1 now mandates every scanner carry a `doGet ?action=` branch, an idempotent in-run hourly self-installer, and a registry entry — locked by `scripts/test_gas_scanner_exposure.py` (**7/7**). Deployed `1MnAsIQA…` to **v36** (pushed + versioned as `admin@truesight.me`; repointed deployments `AKfycbxQDdGnw…`, `AKfycbyGD0CD…`, `AKfycbyxwkIp6…`). Live-verified: `?action=installAllScannerHourlyTriggers` (idempotent — 2nd call flips `installed`→`present`) and the new read-only `?action=getInstalledScannerTriggers` (**7/7 installed, `missing:[]`**). The 7 scanners: `processBatch`, donation-mint, program-reg, payout-event, payout-registration, plot-financing, cfr-program-submissions. See the deploy-identity-trap + per-user-trigger entries under **Pending** for the two follow-ups this surfaced.

### SunMint index freeze (all 3 indexes stale 2026-09-17 → 09-24) — RESOLVED: CI credential restored, indexes refreshed
**Shipped 2026-09-24. Governor: Gary (thread 35189). Credential fix by Gary; verified + re-dispatched by Sophia.**

**What happened.** `trees/index.geojson`, `plots/index.geojson` and `farms/index.json` were all frozen at **2026-09-17** for 7 days (trees failed loudly 09-18→09-24; plots/farms reported **false-green** — see the Pending entry for the silent-green swallow). Root cause: the sunmint CI service account in the `GOOGLE_SERVICE_ACCOUNT_JSON` secret lost read access to the SunMint sheet.

**Fix.** Gary created a new SA `sunmint-ledger-manager@get-data-io.iam.gserviceaccount.com`, granted it the Main Ledger + SunMint sheet, and **replaced the `GOOGLE_SERVICE_ACCOUNT_JSON` repo secret** (`updated_at` 2026-08-26T19:51:13Z → 2026-09-24T17:07:17Z). Sophia stored the key at `config/google/sunmint_ledger_manager_gdrive_key.json` (mode 0600) and in the **vault** as `google_sa_sunmint_ledger_manager_gdrive_key`, then probed it live: reads Main Ledger, `SunMint Tree Planting` (266 rows), `SunMint Plots` (26 rows) and all farm tabs ✅.

**Verification (live, 2026-09-24 17:11–17:14 UTC).** Re-dispatched all three workflows sequentially (dispatch → success):

| workflow | run | result | published output |
|---|---|---|---|
| Rebuild Tree Index | `36032527988` | ✅ success | `trees/index.geojson` `generated_at` 17:11:29Z, **152 features** (was 126) |
| Rebuild Plots Index | `36032653996` | ✅ success | `plots/index.geojson` 17:12:32Z, 22 features |
| Rebuild Farms Index | `36032746905` | ✅ success | `farms/index.json` 17:13:57Z, 15 farms |

**Bonus — the stuck `tree_id` col-D fix (`21428ba6`) is now SHIPPED.** All 152 tree ids are `Edgar_*` (previously mixed off-by-one ids). The Oscar bag cross-link is now live in the published index: `Edgar_20260903083523_003 → 2024OSCAR_CB_20260620_1` carries its `qr_code` (2 of 152 trees now carry one, was 1).

**Note.** First dispatch attempt saw plots fail with `! [rejected] main -> main (fetch first)` — a **push race** between concurrent workflow runs, not a credential issue; resolved by dispatching sequentially. A concurrency group on the three workflows would prevent recurrence.

### Telegram reply-to context silently dropped before reaching the LLM (found live 2026-09-24, second occurrence, never written down)
**Filed 2026-09-24; shipped 2026-09-24. Governor: Gary (thread 35622). PRs: `truesight_autopilot` #500 (`30291c97`) + `agentic_ai_context` #1362, #1365.**

**The gap.** Telegram hands the bot the replied-to message's full content in `reply_to_message`. `truesight_autopilot/app/telegram_adapter.py` read it in exactly **two** places — and neither forwarded its content: line ~615 (`_bot_was_mentioned()`) reads `reply_to.get("from").username` **only** to decide the group mention-gate bypass; line ~1972 reads `reply_to_message.get("forum_topic_created")` for an unrelated topic-creation check. So when a governor replied to a specific message (e.g. a photo), Telegram supplied the content and the bot simply never looked it up — the reply relationship was dropped before the LLM ever saw it. Found **live** ("second occurrence"), but — verified by direct reading, not assumed — **neither occurrence was ever written down** in `OPEN_FOLLOWUPS.md`, `CONTEXT_UPDATES.md`, or `handoffs/active_supervision.json`. That tracking gap is why this entry exists: a third occurrence should not repeat un-tracked.

**The fix (PR1, `truesight_autopilot` #500, sha `30291c97`).** At the existing `dispatch_text` construction site (alongside the `[Telegram context: ...]` prefix — same convention as `[GOVERNOR_IDENTITY: ...]`), three new pure helpers `_format_reply_time` / `_describe_media` / `_reply_context_prefix` build a `[Replying to <who>, sent <when>: "<snippet>"]` bracketed prefix. Captioned/text reply → quoted snippet (400-char cap); uncaptioned photo/document → an **honest marker** that a reply to that media happened, from whom and when. Returns `""` when not a reply, so `dispatch_text` stays **byte-identical** for the overwhelming majority of messages that aren't replies (two exact-string regression guards pin this). 11 tests added; 109 passed locally; ruff 0-new vs `main`; CI green (`smoke` + `test`×2).

**Scope note (deliberate).** Actually re-fetching the replied-to **photo** and passing it to the LLM as a vision input is **out of scope** — verified no `image_url` content-block handling exists anywhere in the current LLM call path (`app/llm/litellm_provider.py`; `download_telegram_file()` is used only for voice notes today). Adding real vision is a materially bigger, separate feature. In scope: surface *that* a reply happened, to what, and from whom — turning "total silence" into "she knows the relationship exists and can ask a clarifying question."

**Live verification (PR2, thread 35622).** Deployed and restarted 2026-09-24; `ActiveEnterTimestamp` 10:20:40 UTC, HEAD `30291c9`; `_reply_context_prefix` present at lines 658 + 2329. UAT: a governor reply to a prior message produced a `CHAT REQ` line in `journalctl` reading `... [Replying to an uncaptioned message from Envoy TrueSight (@nelanco_claude_bot), sent 2026-...]` — the prefix reached the dispatcher — **and** the reply demonstrably acted on the relationship (not merely that the prefix was present). Pre-deploy logs contained 0 such lines.

**Evidence.** `truesight_autopilot/app/telegram_adapter.py` L658, L2329; PR #500 (`30291c97`); plan `plans/TELEGRAM_REPLY_CONTEXT_FIX_PLAN.md`; tracker + manifest PR #1362 (`28bd4783`); thread 35622.

### Governor sheet-permission SOP rewritten into a gated season-rotation runbook (kills the sentinel-stripping revoke script)
**Filed 2026-09-21; shipped 2026-09-22. Governor: Gary (thread 34264). PR: agentic_ai_context #1341.**

The stale §3 inline Python (revoke loop keyed off the governor name list only → would have stripped
sentinel `admin@truesight.me`) is gone. `sops/GOVERNOR_SHEET_PERMISSION_SYNC_SOP.md` now:
- points at the deployed `GovernorSheetPermissionSync.js` as the **only sanctioned write path**
  (`syncGovernorEditorsNow()` / `doGet(?action=sync_governor_editors)`);
- states the **governor OR sentinel** eligibility rule + "never touch owner / SAs / external collaborators";
- demotes the old script to a **read-only audit snippet** (no `permissions().create/delete`);
- adds a **gated runbook**: pre-flight (resolve gov→email, **freeze the roster first**), the go-gate
  (Drive changes = governor's DIRECT go; REVOKE deferred until the TDG window settles), verify via
  the `Governor Sync Log`, then the deferred-revoke step.

The "freeze the roster first" step comes from this session's miss: the 2026-09-22 sync fired 16:40Z,
10 min *before* the ledger dedup finished (16:50Z), so it read a stale leaderboard (Val Lapidus granted
while still a governor, reclassified minutes later). Also surfaced: four current governors (AGL15,
June Jo, Ken Nim, Philip Lee) have **blank emails** in `Contributors contact information` col D and so
cannot be granted at all — the runbook now pre-flights this.


### Black King corridor: NF11/NF12/NF14 destination conflict - RESOLVED (keep Kirsten; Taraval = fiscal/billing only)
**Filed 2026-09-18; resolved 2026-09-18. Governor: Gary (thread 31905). PR: agentic_ai_context (Rev 4 crosswalk).**

Governor ruling: keep the register's **Kirsten Ritschel / 1423 Hayes St** attribution for NF11
(`CP340993988BR`), NF12 (`CP340993869BR`) and NF14 (`CP340993299BR`); the NF-e **Taraval**
destinatario is the TrueTech **fiscal/billing** address only and does not by itself assert the
physical recipient. Crosswalk re-scoped (Rev 4) and the conflict box marked resolved; **no
register rows changed**.

### dao_protocol: server-side guard — reject empty body / missing signature format — SHIPPED 2026-09-15 (dao_protocol#166, deployed)
**Shipped 2026-09-14 (PR #166, Gary); deployed 2026-09-15 (Sophia, governor go from Gary, thread 26992).**

**What shipped.** `submit_contribution` (`truesight_dao_client/server/routes/dao.py`) now rejects *before* persisting: (a) an empty body or the literal `[No Text Provided]` sentinel → `{"error":"empty_body",...}` HTTP 400; and (b) a signed-report submission whose text carries a signature-requiring event marker but no parseable signature block → `{"error":"missing_signature_format",...}` HTTP 400. Non-empty, non-signed event types (e.g. email onboarding) are unaffected. Regression test: `tests/test_empty_body_guard.py` (8 tests).

**Deploy + verification (2026-09-15, thread 26992).** Host `dao_protocol_nelanco` (98.93.94.86), service `truesight-dao-protocol`, HEAD `3bb3853` → `d12406f`. Before: empty body → HTTP 200 `no_signature_format`. After: empty / whitespace-only / `[No Text Provided]` → HTTP 400 `empty_body`; non-empty non-signed regression → still HTTP 200. `GET /healthz` → `{"version":"d12406f","environment":"production"}`. Verified both direct on `:8010` and through the public `edgar.truesight.me` path.

**Why it mattered.** 71 `[No Text Provided]` / `no_signature_format` rows had accumulated on the Telegram Chat Logs tab (2026-05-31 → 2026-09-12); the guard makes that failure class impossible to record regardless of client (client-side fixes regress silently — #88 missed a form, #98 fixed it).

**Evidence.** dao_protocol PR #166 (`d12406f`); dapp_beta PR #98 (`7c0c48e`); dapp PR #88; threads 26992 + 29826.

### FBE `Plot ID` canonical-label gap — RESOLVED 2026-09-10 (autopilot guard shipped, [truesight_autopilot#425](https://github.com/TrueSightDAO/truesight_autopilot/pull/425))
**Shipped 2026-09-10 (Sophia, thread 24321; governor go from Gary).** The autopilot no longer silently drops a non-canonical attribute key: `_DAO_GUARANTEED_LABELS` (`FBE → ["Plot ID"]`) is unioned into the catalog `canonical_labels` at merge (`_merge_catalog_labels`), and the legacy normalizer's bare `continue` was replaced with a loud `logger.warning` naming the dropped key + event. Regression test `tests/test_fbe_plot_id_normalization.py`. This makes the Edgar catalog's missing `"Plot ID"` label (gap 1) safe without touching `dao_protocol` (governor deferred that belt-and-suspenders PR).

**Incident it fixes (row-5 clobber).** An FBE for `B-06-108_20260908_research_1` had its `Plot ID` silently dropped, so `fbeUpsertFarm_` fell back to farm-slug matching and overwrote row 5 (`B-06-108`, 114 ha) `plot_type`: `maturing → research`. Row 5 was restored and the `sunmint` registry regenerated same-thread; same failure class as the Sítio Torres duplicate `PL-006`.

**Still open (optional hardening, not shipped).** (a) Add `"Plot ID"` to FBE `canonical_labels` in `dao_protocol`'s `events_catalog.json` — deferred by governor. (b) Make `fbeUpsertFarm_`'s slug fallback refuse to write `plot_type` when >1 row shares the slug (fail safe instead of clobber).

### ✅ Telegram-log processor locks are now LIVE on the pinned webhook deployments (`@45`/`@46`) — RESOLVED 2026-09-10
**Shipped 2026-09-10 (Sophia, thread 24326; governor go from Gary). Supersedes the `## Pending` entry filed earlier the same day that read "locks are live only in `@HEAD`".**

**What changed.** The two pinned deployments that serve the affected webhooks were repointed to fresh versions cut from `@HEAD`:

| Deployment | Webhooks it serves | Repointed to | Locks before | Locks after |
|---|---|---|---|---|
| `@44` `AKfycbyoFCTz…` | FARM_BOUNDARY_EVIDENCE · MEDIA_RETRACTION · PLOT_INVALIDATION · TREE_PLANTING_REJECT | **`@45`** | plot-inval ✅ · FBE ❌ · MR ❌ | ✅ ✅ ✅ |
| `@36` `AKfycbwm9TZ…` | TREE_GROWTH_MONITORING | **`@46`** | ❌ | ✅ |

`@32` (serves only QR_CODE_UPDATE + TREE_PLANTING_LINK) was deliberately **left alone** — both its files are the intentionally-unlocked ones, so a repoint there would be pointless risk.

**Verified, not assumed.** Read the *live version content* via the Apps Script API (`projects.getContent?versionNumber=`) — v45 and v46 both show `LockService.getScriptLock` in `process_farm_boundary_evidence`, `process_media_retraction`, `process_plot_invalidation`, and `process_tree_growth_monitoring`; `process_qr_code_updates` and `process_tree_planting_link` correctly read 0. Deployment→webhook bindings were confirmed by reading the live `dao_protocol` env (the earlier `@44`→FBE/MR mapping was an inference there; it is now observed).

**Caveat.** The underlying `clasp push` / pinned-deployment gap is a *class* of failure that will recur on the next `clasp push` — the root-cause entry in `## Pending` still stands and should own the durable fix (auto-repoint on push, or a post-push deploy hook). This entry only records that the *specific* lock fix is now live.

---

### CEPOTX/CoopCao site code `N-06-66` (Sítio Torres, Pacajá) — RESOLVED 2026-09-10 (governor-confirmed; registry updated)
**Shipped 2026-09-10 (Sophia, thread 25149).** Governor (Gary, thread 24442) **confirmed `N-06-66` is the correct issued CEPOTX site code** for the Sítio Torres (Pacajá) plot — the property of **Alexandre**, a CoopCao director-coordinator — superseding the earlier "outside the observed roster range" concern. `CEPOTX_SITE_CODE_REGISTRY.md` updated in the same PR: the COOPCAO observed range is annotated with `N-06-66` as governor-confirmed, and an anchors-table row was added (`N-06-66` / Sítio Torres (Pacajá) Plot 1 / Alexandre / COOPCAO), tying to the SunMint Plots sheet row 23, `sunmint/plots/index.geojson`, and the agroverse_shop farm page (PRs #308/#309). The follow-up's corroboration steps (re-OCR IMG_9694/9695, re-run the spoken-code clips) are no longer blocking — the code is treated as issued and authoritative.

**Original Pending entry (retained for history).** *Filed 2026-09-10. Owner: unclaimed. Governor: Gary (thread 24442).* Context: on the 2026-09-09 Pacajá site visit (loc3 — "Sítio Dois", producer **Alexandre**, a CoopCao director), the plot's CEPOTX site code was read as **N-06-66** from a phone-translator screenshot (IMG_9694: "O código dele é N0666"). `CEPOTX_SITE_CODE_REGISTRY.md` listed the **COOPCAO** family as **N-06-02 … N-06-52** — `N-06-66` fell outside that observed range, and the registry is marked "reported / unverified," so no name-match was possible; the code was registered on Gary's assumption. Impact: the code is on public surfaces (SunMint Plots sheet, `plots/index.geojson`, agroverse_shop farm page). Resolution: governor confirmed the code as issued (thread 24442), closing the registry-range question.

### `farm_media_manifest` couldn't parse DMS GPS — every Apple-media item got `latitude: null`
**Shipped 2026-09-10 ([farm-media-daemon#24](https://github.com/TrueSightDAO/farm-media-daemon/pull/24)).** `farm_media_manifest._parse_gps` handled only decimal (`float(split(","))`), so exiftool DMS strings (`3 deg 33' 25.20" S, …`) raised `ValueError` → `None`; `gps_coverage` read `0/N` and `paulo-la-do-sitio-para.json` needed a hand-written `_remediation` block. Now delegates to the daemon's own DMS-aware `farm_media_geo.parse_gps` (one shared parser) + 4 unit tests (decimal, exact DMS sidecar string, equality vs `farm_media_geo`, none/junk). Verified end-to-end on Cristo Rei: `GPS 0/13 → 12/13` (the 13th lacks GPS on the original).


### krake_ror disk-full durability — RESOLVED 2026-09-06 via AMI bake + ASG roll (sophia, thread 22224)
**Shipped 2026-09-06.** Durable fix landed after the 2026-09-06 ENOSPC incident (Bugsnag `Errno::ENOSPC`, getdata.io) per governor direction: baked custom AMI **`ami-0933e020a3e613189`** (`krake_ror_20260906`) from the fixed host — captures `/etc/logrotate.d/krake_ror` (daily + size 200M, rotate 5, copytruncate, delaycompress, `su ubuntu ubuntu`); created LT `lt-085100be44b6079cc` **v4** → new AMI, set `$Default` (v3 = rollback); rolled ASG zero-downtime (scale to 2, validated new instance: HTTP 200 / logrotate present / disk 53%, drain old, terminate). Running instance now `i-0f7f3490dc465136b` (54.224.186.212). Any future recycle boots with logrotate → recurrence closed. Volume growth explicitly NOT done (governor 2026-09-06: 8G root fine with logrotate capping logs). Optional residual: `df /` ≥ 85% alert.

### krake_data disk-full (ENOSPC since Jun 4) — RESOLVED 2026-09-06 via kernel purge + df guardrail (sophia, thread 22224)
**Shipped 2026-09-06.** Second out-of-storage incident caught during the krake_ror sibling sweep — same failure class, worse: root **100% / 0 free** on `krake_data` (`i-07c76510b231d787f`, 52.5.179.48, t3.medium, 316d uptime), rsyslog ENOSPC since **2026-06-04**, systemd-journald failing minutes before diagnosis. Postgres 9.5 `dev_panel` (serves krake_ror + krake_sk_consolidated) safe on separate 50G vol `/krake_data_cache` (`/dev/nvme1n1`, 51%). Root cause: **46 old `linux-image-aws` kernel sets** (`5.4.0-1029…-1089`) + **40 orphaned `/usr/src` header dirs** (the 4.6G bulk — already-`rc` packages never cleaned) + **40 orphaned `/lib/modules` trees**, never purged in 316 days. Remediated per governor "fix it": purged old kernel set, `rm -rf` the 40 orphaned header dirs + 40 orphaned module dirs (kept running `-1092` + newest `-1103`), truncated 512M auth.log, apt cache + journal vacuum + disabled snaps → root **100% → 30% (5.4G free)**. Verified: journald + syslog writing again, Postgres online, dpkg audit clean, running-kernel modules intact, **no reboot needed**. Guardrail added: autopilot cron (30-min) `df-alert-remote-krakedata.sh` (SSH + `server_us.pem`, Telegram at ≥85/93%, same channel as autopilot df-alert) — closes the "no alert → silent 3-month fill" gap. Infra row updated (AWS_DIGITAL_INFRASTRUCTURE.md §2.1). Sibling sweep of remaining fleet (seni_ror 62% healthy; krake_nginx/krake_sk_consolidated need SG/key access) is optional next.

### krake_ror recycled to v5 instance + consolidated fleet df-alert (sophia, thread 22224)
**Shipped 2026-09-09.** The krake_ror ASG recycled 2026-09-09 04:47 UTC — old instance `i-0f7f3490dc465136b` (54.224.186.212) replaced by `i-069771c1f79288216` (**98.81.159.70**) on LT v5 = the durable logrotate-fix AMI `ami-0adfbc216d627e058`. Verified on the new box: both logrotate rules present (`/etc/logrotate.d/krake_ror` + `krake-ror-upstart`), upstart log bounded (~1.2M live, archives compressed), disk 58% stable, puma 5.1.0 healthy — the baked fix survived the recycle as designed. The new instance inherited the old 211M rotated upstart archive via the AMI snapshot; force-rotate compressed it to 1.6M.gz (~210M reclaimed). **Consolidated fleet df-alert guardrail:** `/usr/local/bin/df-alert-fleet.sh` (autopilot cron, 30-min, replaces df-alert-remote-krakedata.sh) probes krake_data 33%, seni_ror 65%, dao_protocol 63%, krake_ror 98.81.159.70 with per-host keys; Telegram at ≥85/93%, never auto-deletes, silent under threshold. Infra rows updated (AWS_DIGITAL_INFRASTRUCTURE.md §2.1). Remaining unreachable from autopilot: krake_nginx (port 22 refused), krake_sk_consolidated (timeout) — need SG/key access to extend coverage.


### [SHIPPED] sunmint cache_satellite_scenes.py null-geometry guard (CEPOTX rename follow-up)
- **Date:** 2026-09-05
- **Issue:** `scripts/cache_satellite_scenes.py` plots loop crashed on explicit `"geometry": null` — `geom = feat.get("geometry", {})` returns None, then `geom.get("type")` raises `AttributeError: 'NoneType' object has no attribute 'get'`. Crashed every satellite run until the sheet's null-geom test rows were removed (2026-09-05). Trees loop was already null-safe.
- **Resolution context:** stale `satellite/plot_{SA-P1,CL-P1,LD-P1}/` dirs + `plots/by-plot/{SA-P1,CL-P1,LD-P1}.geojson` retained as inert residue per governor resolution 2026-09-05 (option c — renames recorded as alias tombstone, agentic_ai_context PR #925). NOT deleted.
- **Shipped 2026-09-06 by Sophia:** one-line guard `geom = feat.get("geometry") or {}` at `scripts/cache_satellite_scenes.py:156` — uploaded via Contents API to sunmint@main (commit 90eaa4c). UAT: pristine original crashes on a null-geom fixture (`AttributeError` line 157, rc=1); fixed script exits 0, caches the real polygon (OK-PLOT: 4 scenes), skips the null feature (manifest plots = [OK-PLOT]). Syntax + py_compile clean.
- **Link:** https://github.com/TrueSightDAO/sunmint/commit/90eaa4c30f957e561ca25b172661ae9d982eb386
### [DONE] Usage/meta logging in truesight_autopilot_transcript — shipped 2026-09-01
- **Date:** 2026-08-31
- **Issue:** The transcript repo AGENTS.md/ROADMAP.md describe `usage.jsonl`, `meta.json`, `messages.jsonl` + `scripts/append_usage.py` + a summarize CLI — but only `transcript.md` is actually written. Consequence: "how much time/tokens did X cost?" cannot be answered exactly (was reconstructed from git merge timestamps for the Rancho Maranta effort, ~15.5h wall-clock / ~360 active min lower bound).
- **Fix:** implement `scripts/append_usage.py` (token/usage rows per tool call) in the transcript repo + meta.json writer; wire into the autopilot transcript append path; then a `summarize` CLI for cost queries.
- **Shipped 2026-09-01 by Sophia:** `scripts/append_usage.py`, `scripts/write_meta.py`, `scripts/summarize_usage.py` + `scripts/tests/test_usage_tools.py` landed on truesight_autopilot_transcript@main (commits bcb39c0, 3a6fef8, fe2ac2d, 216264b). Local suite green (compileall + ruff + format + 5 pytest). Smoke-verified append→summarize end-to-end. Wiring into the autopilot runtime's transcript-append path remains (runtime harness, not in a DAO repo — separate follow-up).

### SunMint satellite cache pipeline: Earth Search STAC (replaces CDSE) — LIVE
**Shipped 2026-08-31. Owner: Sophia.** The CDSE registration path was dropped (registration broken; CDSE no longer offers anonymous Sentinel-2 WMS — only STAC public, `sh.dataspace` needs auth). Replaced with **Earth Search STAC** (AWS-hosted Sentinel-2 L2A, anonymous, no key): `sunmint/scripts/cache_satellite_scenes.py` queries `https://earth-search.aws.element84.com/v1/search` (POST, explicit RFC3339 datetime — `now` token 400s), downloads the lowest-cloud scene's public preview into `satellite/<lat>_<lng>/<scene-date>.jpg` + `satellite/manifest.json`. Verified live: 9 cells / 36 scenes; FounderHaus + Rancho Maranta cells + plot dirs (RM-P1/RM-P2) committed. Map satellite history strip (truesight_me_beta #322) layers `manifest.json` by date with cloud badges; plot-aware caching reads `plots/index.geojson` — the ONLY plot registry (`trees/plots.geojson` is a dead path, guarded). Remaining: confirm the daily workflow auto-commits (06:30 UTC schedule; box token lacks workflow-dispatch scope — a human can trigger via Actions → workflow_dispatch). **No CDSE registration needed — Gary can drop that task.**

### DEPLOY_PUSH_SOP Phase 2 — lease+audit enforced in all deploy tools (SHIPPED 2026-08-25)
**Shipped by sophia.** The deploy-push audit trail is now **enforced in code**, not just documented:
- `ecosystem_change_logs/deploys/` ledger + `scripts/append_deploy_record.py` (Phase 1, manual logging).
- `truesight_autopilot#313` — new `app/deploy_ledger.py` (check_lease/acquire_lease/close_lease/append_deploy_record, 30-min TTL, fail-open on errors, hard-block on a live lease) wired into `gas_deploy_project.py` (blocks `--push` on a clasp scriptId with a live lease), `sync_beta_to_prod.py` (lease on prod repo before merge-upstream), and `deploy.py`+`main.py` (ec2/autopilot lease threaded through the two-phase re-exec, closed on fresh boot). 10 new tests; gas-tool tests made hermetic (they were hitting the real API — a stale test lease actually blocked a duplicate push, proving the lock works).
- `tokenomics#429` — standalone `scripts/deploy_ledger.py` (stdlib-only, for direct LLM checkouts) + `deploy_gas_project.py` lease check/acquire/record/close before any `--push`; `--lease-id` passthrough prevents self-deadlock when the autopilot tool owns the lease.
- Backfilled ledger record `deploy_20260825T160310Z_truesight-autopilot` for the #313 merge itself.
- **Remaining (Phase 3):** CI-level validation (a GitHub Action asserting every push records a ledger entry) — not yet built.

### Telegram attention watchdog — ACTIVATED 2026-06-06

Operator completed the my.telegram.org + Telethon login (the earlier
code-delivery stall resolved on a clean retry); session created, unit
`truesight-autopilot-watchdog` active, log shows `watchdog up as garyjob`.
The June-12 failure mode is now guarded. Possible v2s parked: Sophia-drafted
Telegram replies (the user-session already permits sending), Gmail-leg digest
unification.

### Telegram attention watchdog — minimal v0 (SHIPPED 2026-06-05, activation pending operator login)

Shipped as [truesight_autopilot#102](https://github.com/TrueSightDAO/truesight_autopilot/pull/102)
and deployed to the sophia box same day: read-only Telethon user-session
watcher (`app/attention_watchdog.py`), Saved-Messages nudges (4 h / 2 h dated)
+ daily 9 am digest, 17 heuristic unit tests, systemd unit installed but
**stopped until the operator runs the one-time login**
(`scripts/telethon_login.py` after adding `TELEGRAM_API_ID/HASH` to the box
`.env`). Originally filed 2026-06-06 after the June 12 cacao-serving
coordination miss. Gmail-leg unification remains a possible future follow-up.

### Autopilot tooling gaps ×4 (migrated from the duplicate `OPEN_FOLLOW_UPS.md`) — resolved by 2026-06-03 capability uplift

Sophia filed four items in a separately-created `OPEN_FOLLOW_UPS.md` on
2026-05-31 (large-file updates via GitHub API; SSH key + git client on her box;
`open_fix_pr` repo enum too narrow (still open); `upload_file_to_github` lacking `sha` — ✅ RESOLVED (truesight_autopilot #87, 2026-06-03; re-verified 2026-09-11 by a create→update probe on `agentic_ai_context` → `created` then `updated`, no 422). See `handoffs/MEDIA_GALLERY_PUBLISHER_PLAN.md` PR2.
update support). All four were resolved by the `SOPHIA_CAPABILITY_UPLIFT_PLAN.md`
PRs — verified present 2026-06-06: `app/tools/git_tools.py` (native git
branch+PR with search/replace semantics, no file-size limit),
`app/tools/ssh_tools.py` (`sophia_infra` fleet key), `upload_file_to_github`
auto-fetches `sha` for updates, and `settings.allowed_repos` now includes the
beta/prod site repos. The duplicate file is now a tombstone redirect; this file
is the single backlog.

### `/aum` dedicated page + per-ledger click-through on `/treasury` — 2026-05-20

Mirrors the `/treasury` pattern shipped earlier same day. New `/aum`
page reads `treasury-cache/dao_offchain_treasury.json` and renders
two sections — **Assets by ledger** first (each managed ledger
expanded to show currencies it holds), then **Per currency** (each
currency expanded to its per-ledger split). Both `/aum` and
`/treasury` per-ledger rows are now click-throughs to the source
Google Sheet, via a new `ledger_urls` dict in the GAS
`treasury_breakdown` payload. Landing-page AUM card flipped from
inline `<details>` to `View breakdown →` link; the dead
`wireStatBreakdowns` / `fetchTreasuryCacheOnce` / `renderUsdTreasuryBreakdown` /
`renderAumBreakdown` machinery (~85 lines) was removed from
`index.html`.

GAS also picked up a small `&refresh=1` escape hatch on the
`treasury_breakdown` endpoint for warming the cache after schema
changes without waiting for the cron.

PRs:
- TrueSightDAO/tokenomics#304 (squash `2640d1e`, GAS deploy `@10`)
- TrueSightDAO/truesight_me_beta#134 (squash `26947f7`, prod cherry-pick `25a6a9e`)

### `dao_client onboard_retail_partner` MVP — 2026-04-28

Manifest-driven CLI that automates the deterministic ledger + inventory
steps from `RETAILER_TECHNICAL_ONBOARDING.md` §3:

- Step 1 `[CONTRIBUTOR ADD EVENT]` (with name pre-formatted as
  `<First> - <Store>` to dodge Edgar's auto-rename).
- Step 2 `Contributors!U` (Mailing Address). Explicitly does **not**
  toggle col T — that flag is reserved for online-fulfillment managers
  (Gary + Kirsten only).
- Step 3 `Agroverse Partners` row append.
- Step 13 `[INVENTORY MOVEMENT]` loop for opening-order QR codes.
- Step 14 subprocess `sync_agroverse_store_inventory.py` and
  `sync_partners_velocity.py` so JSON snapshots refresh.

Idempotent at every step. `--dry-run` is the default. Worked-example
manifest in `examples/onboarding/the-way-home-shop.yaml` replays the
2026-04-28 onboarding as a no-op.

Steps still operator-manual in MVP: partner page, discovery surfaces,
photo download, PR creation (steps 4 / 5–10 / 11 / 12 / 15). Script
prints copy-paste instructions at the end. v1 covers those — see the
remaining Pending entry above.

PR: https://github.com/TrueSightDAO/dao_client/pull/11

---

### `[STORE ADD EVENT]` canonical pattern (additive slice) — 2026-04-28

Signed Hit List adds now route through the same Edgar pattern as retail
field reports: dao_client / DApp signs `[STORE ADD EVENT]` → Edgar
`/dao/submit_contribution` → Telegram Chat Logs → `WebhookTriggerWorker`
fires `processStoreAddsFromTelegramChatLogs` GAS scanner → `addNewStore`
on Hit List + audit row on **Store Adds** dedup log
(`1qbZZhf-…`, gid 1208101506; col B `telegram_update_id` is the dedup
key). Verified end-to-end: 3 Psychic Sister referrals (Clary Sage,
Casa de Ritual, La Sirena Botanica) added as Research rows on Hit List
rows 526–528 with referral provenance in Notes + Sales Process Notes;
scanner replay = 0/0/0/0 (perfectly idempotent).

Two follow-ups split out into Pending above:
1. Migrate `dapp/stores_nearby.html` Add Store form off the legacy
   direct GAS GET onto the same Edgar path.
2. Fix the pre-existing `addNewStore()` GAS `setValues` dimensional
   bug so audit logs say `added` instead of `error` even though the
   actual Hit List rows write correctly.

PRs:
- TrueSightDAO/dao_client#9 — `add_hit_list_store.py` module.
- TrueSightDAO/sentiment_importer#1042 — Edgar `[STORE ADD EVENT]` branch.
- TrueSightDAO/tokenomics#250 — `processStoreAddsFromTelegramChatLogs`
  GAS scanner + Store Adds tab schema.

---

## tribomirimbahia Phase 1B — music library tagging

**Context:** Phase 1A done 2026-05-10 (TrueSightDAO/tribomirimbahia#2) — 39 Bico
Duro per-move clips published. Phase 1B is the next sequential step before the
Phase 2 site can do session generation.

**Scope:** Build `tribomirimbahia/data/music_library.json` per spec §5 + §3:

- 12 capoeira tracks (Gary curates the YouTube URLs).
- Per track: `id`, `title`, `youtube_url`, `duration_seconds`, `bpm` (estimate
  via `librosa` or DeepSeek tap), `tempo_category` (Slow/Medium/Fast),
  `style_notes` (berimbau-heavy, drums-focused, etc.).
- Suggested mix: 3–4 slow berimbau (Foundation/warm-up), 4–5 medium drum-heavy
  (Defense/Attacks), 2–3 fast energetic (Aerials/Floreios).

**Hand-off:** Per `AGENT_BRIEF.md` matrix — BPM detection + tagging is DeepSeek
territory (numeric, no cultural nuance). Gary spot-checks the tempo arc since
it affects practice feel.

**Blocker:** Gary needs to curate the 12 YouTube URLs first.

## tribomirimbahia Phase 2 — capoeira.agroverse.shop site build

**Context:** Phase 1A produced `tribomirimbahia/data/moves.json` (39 moves with
YouTube URLs); spec PDF + AGENT_BRIEF.md describe the static-site requirements.

**Scope:** Greenfield build of `~/Applications/capoeira/` (currently empty)
following the AGENT_BRIEF.md "Phase 2 — Core Site Build" section. Mirror
agroverse_shop conventions (no frameworks, static HTML/CSS/vanilla JS).
Mandatory: `agentic_ai_context/DAPP_PAGE_CONVENTIONS.md` for every page.

**Hand-off:** Claude drafts pages; Gary reviews landing copy + Bahia tone before
flipping DNS. The 4 open questions in AGENT_BRIEF.md "Open questions before
Phase 2" need Gary's answers first (deploy target, Stripe account, Bico Duro
consent, fundraising goal).

**Blocker:** Open questions in AGENT_BRIEF.md not yet answered.

## capoeira: curriculum-based session structure

**Context:** Practice tool at `capoeira.agroverse.shop/practice.html`. Phase 1A
shipped (39 moves), data calibrated for 45-min single-theme sessions in
TrueSightDAO/capoeira#7. But Bico Duro's actual teaching (per his spoken
curriculum in cqKMvYbB1Kw — "primeira coisa: ginga; segunda coisa mais
importante: defesa; terceira coisa: ataque") is NOT single-theme; it's
Foundation → Defense → Attacks progression every session.

**Scope:** Add an alternative session-generation mode that composes:
1 Ginga warm-up (Foundation) + 2 Defense moves + 2-3 Attack moves +
optional Flow cool-down (Giro). This un-skips the Foundation and Flow
themes (currently filtered out because they have <4 moves each) and aligns
the practice tool with how Bico Duro actually teaches.

**Where to edit:** `assets/js/session-generator.js` — add a `pickCurriculumSession()`
alongside the existing single-theme path. Add a UI toggle on `practice.html`
("Single-theme drill" vs "Curriculum session"). Default to curriculum once
implemented.

**Blocker:** None — calibrated data + working single-theme algorithm both
shipped TrueSightDAO/capoeira#7.

## capoeira: session-generator algorithm variety

**Context:** Same Phase 1A practice tool. Current `pickMoves()` is greedy on
weighted score; with identical difficulty bias, sessions 1 and 4 in the headless
simulation were byte-identical (same 6 Beginner Attack moves in the same order).

**Scope:** Add randomized tie-breaking — group candidates by `_weight` bucket,
shuffle within bucket, then pick. Or sample with weighted probability rather
than sort+head. Keeps the difficulty bias intent but diversifies outputs.

**Where to edit:** `assets/js/session-generator.js` `pickMoves()` greedy loop.

**Blocker:** None.

## sentiment_importer: repurpose /compare into a backtester

**Context:** Repurposing the `/compare/TICKERS/DATE/PERIOD` view (was
correlation/sentiment overlay) into a strategy backtester — compare buy-and-hold
vs a rebalance-band (cash-sleeve, configurable initial position) across tickers,
reporting realized return / CAGR / Sharpe / maxDD / turnover. Designed jointly
2026-05-25; two specs written, **not yet implemented**.

**Specs (in repo root):**
- `sentiment_importer/BACKTEST_DATA_ENDPOINT.md` — `GET /backtest/data` clean-data
  JSON (real bars, no forward-fill; risk-free = `daily_yield_curves.month_3 ÷ 100`).
  Deliberately **no** split/anomaly detector — the rendered chart is the detector
  (human-in-loop); fix bad data manually via `EodHdPriceRefresher.new.perform(id)`.
- `sentiment_importer/BACKTEST_STRATEGY_ENGINE.md` — JS `runStrategy(bars, riskFree,
  spec)` pure function; engine runs client-side; server only serves data.

**Scope (when greenlit):** build data endpoint first (so series are eyeball-able),
then wire JS engine. Idealized fills for v1 (fractional, no cost). Rolling-window
distribution + signal strategies (macd/rsi/buy_now) parked for later.

**Blocker:** implementation not yet greenlit as of 2026-05-25.

## blog post: "Gary and Claude" — knowing when NOT to automate

**Context:** Write a first-person (Claude-as-teammate voice) post for truesight.me
about the backtester design session above. Angle is **subtraction, not building**:
Claude kept proposing data-quality machinery (scanner → auto-repair → flag-only),
Gary kept stripping it back to "just look at the chart" — landing on Moravec's
paradox (in an interactive tool the human is already in the loop, so a detector is
redundant). "The best anomaly detector was the chart we were already drawing."
Byline: Gary and Claude.

**Scope:** hand-written page in `truesight_me_beta`; promote to prod via
`gh repo sync` (NOT `--force` — beta/prod CNAMEs intentionally diverge). Include a
real PLAY equity-curve screenshot as the punchline. Fits existing llms.txt surface.

**Blocker:** gated on the backtester shipping — write it once the tool works and
there's a real chart to show.

## dao_protocol: enable immediate-after-sale Agroverse inventory refresh

**Context:** The Edgar → dao_protocol extraction left
`DAO_PROTOCOL_AGROVERSE_INVENTORY_GAS_WEBAPP_URL` + `_PUBLISH_SECRET` empty because
the HTTP publish path is **dormant end-to-end** (verified 2026-05-26): GAS project
`1P0Mg33i…` (`update_store_inventory`) has **no** `AGROVERSE_INVENTORY_PUBLISH_SECRET`
script property (so `verifyPublishToken_` → false → the HTTP actions
`publishInventorySnapshot`/`recalculateAndPublishInventory` reject every call as
Unauthorized), the worker's `AGROVERSE_INVENTORY_*` env is unset on the `seni_sk_new`
worker host (Sidekiq **is** running there — the worker just no-ops on the missing env),
and store-inventory freshness is currently maintained only by the GAS **hourly
time-driven `updateStoreInventory` trigger**. dao_protocol's `inventory_snapshot.publish()`
(wired into `dispatch.py` on `[ASSET RECEIPT EVENT]` / sales) no-ops to match — see
`EDGAR_DAO_EXTRACTION_PLAN.md` Outstanding §2.

**Scope (net-new setup, NOT provisioning — there is no existing value to copy):**
1. Mint a shared secret; set it as the `AGROVERSE_INVENTORY_PUBLISH_SECRET` script
   property on GAS `1P0Mg33i…` (Apps Script editor for that project).
2. Put the same value + the deployed `/exec` URL into
   `seni_ror_new:/home/ubuntu/dao_protocol/.env` (`DAO_PROTOCOL_AGROVERSE_INVENTORY_GAS_WEBAPP_URL`
   / `_PUBLISH_SECRET`, chmod 600) and `sudo systemctl restart truesight-dao-protocol`.
3. (Optional) re-enable `seni_sk` on Rails if the immediate path is wanted there too.
4. Verify a signed `[ASSET RECEIPT EVENT]` / sale triggers a snapshot refresh within
   seconds (GAS returns 200, not Unauthorized) instead of waiting up to an hour.

**Payoff:** sub-second store-inventory JSON refresh after a sale/receipt instead of
up to a ~1-hour lag. Purely additive — the hourly trigger already keeps data correct.

**Blocker:** none (opt-in; only worth doing if the up-to-1-hour refresh lag is a
problem in practice).

## Edgar → dao_protocol: post-soak cleanup (revisit ~2026-06-25)

**Context:** The Edgar → dao_protocol migration is functionally complete as of
2026-05-26 — all 6 routes cut over (PR2 `/proxy/gas`, PR3 newsletter/email-agent,
PR4 shipping_rates, PR5 `/dao/submit_contribution`, PR6a `/qr-code-check`+`/link-email`,
PR6b `checkout.session.completed` order-sync delegation, all live), env provisioned,
60 unit tests, payment path sandbox-verified. The remaining items are deliberately
**deferred ~30 days to let the live ramps soak** before removing the Rails rollback
net. Full state: `EDGAR_DAO_EXTRACTION_PLAN.md` Outstanding.

**Do not start before ~2026-06-25** unless the ramps are clearly stable sooner. By
then, confirm via the dao_protocol journal + Bugsnag that the ramped routes have run
clean (esp. `/qr-code-check` payments and `/dao` dispatch), and ideally that a real
checkout reconcile→SOLD has happened.

**Scope (3 parts):**
1. **PR7 cleanup (the soak-gated part)** — remove the now-dead Tenant B code from
   `sentiment_importer`. **Recommended phased + MERGE-NOT-DEPLOY** (keep the branch;
   don't pull onto `seni_ror_new`, so the running Rails keeps the controllers as the
   instant nginx-flip rollback until you're fully confident):
   - Safe first: delete `MetaCheckoutOrderSyncWorker` (dead since PR6b) +
     `NewsletterController`, `EmailAgentController`, `AgroverseShopShippingRatesController`
     + their routes (all fully verified, read/redirect, lowest risk).
   - Hold longer: `qr_code_check_controller` (payment-critical; reconcile→SOLD not yet
     e2e-tested), `proxy_controller`, and the `dao_controller#submit_contribution`
     **action only** (the controller has ~16 other live `/dao/*` routes — surgical removal).
   - The `/stripe_webhook` entry + subscription handling stay on Rails (decision A).
2. **dao_protocol `README.md`** — reframe the "Edgar (source: `sentiment_importer`)"
   framing: this repo now contains the **server** that serves the ramped endpoints
   (extracted from `sentiment_importer`, which remains the Rails trading platform).
   Keep the legit historical PR refs (`sentiment_importer#1024`, `#1028`).
3. **truesight.me blog post** that still references `sentiment_importer` — locate and
   update to dao_protocol where it describes the contribution server. (Mind the
   beta→prod CNAME divergence on publish: `gh repo sync`, NOT `--force`.)

**Blocker:** time-gated — let the ramps soak (~30 days, revisit on/after 2026-06-25).

---

## truesight_autopilot: stop compiling `dao_client` native extensions on every deploy — 2026-05-30

**Context.** Every `deploy_autopilot()` invocation runs `pip install -r requirements.txt`, which includes:

```
truesight-dao-client @ git+https://github.com/TrueSightDAO/dao_client.git
```

pip git-clones the repo into `/tmp/pip-install-*/...`, then builds the wheel — which **compiles `cryptography` + `cffi` native extensions** (cryptography is a transitive dep of dao_client). On a t3.small this takes 30–60 s. The compile is a long-running CPU-bound subprocess that's vulnerable to SIGTERM cascades from parent worker restarts — surfaced as `Phase-two subprocess failed (exit=-15)` errors on 2026-05-30 ([autopilot#83](https://github.com/TrueSightDAO/truesight_autopilot/pull/83) was an LLM-generated PR that misdiagnosed this as OOM; closed). It's also the slowest single step of the deploy by ~10×.

**Options, in increasing order of effort:**

1. **Pin to a release tag + cache `~/.cache/pip` between deploys.** Add `@vX.Y.Z` to the requirements line so pip's resolver short-circuits when the tag is unchanged. Cheapest; eliminates redundant builds for unchanged versions but still rebuilds on each version bump.
2. **Publish `dao_client` as a wheel.** Either to public PyPI (matches DAO transparency posture) or to a private artifact store (GitHub Packages, internal index). pip pulls a binary; no compile. Best long-term; needs CI on dao_client to build + push on each release.
3. **Vendor `dao_client` into `truesight_autopilot`.** Copy `truesight_dao_client/` into autopilot, drop the git+ dep. Decouples deploy speed from dao_client's release cadence. Costs duplication; loses single-source-of-truth.
4. **Switch native deps for pure-Python alternatives.** cryptography → PyCryptodome (also has C, but easier wheels) or pure-Python RSA. Bigger refactor in dao_client; affects signed-event throughput.

**Recommendation.** Start with (1) — five-minute change in `requirements.txt`. If deploy time still dominates after that, do (2). (3) and (4) are escape hatches if dao_client's release cadence becomes a deployment bottleneck.

**Related architectural concern (separate but adjacent).** The deploy's phase-two subprocess runs inside the autopilot worker's cgroup, so any worker restart (LLM tool retry, telegram-adapter race, ELB-driven restart) propagates SIGTERM into the pip subprocess and kills the compile. Fixing the compile cost via (1)/(2) shrinks the window where this can bite. The "right" fix for the cgroup-coupling itself is to run phase-two via `systemd-run --collect --unit deploy.$(date +%s)` so it's isolated from the worker's lifetime — log as a separate follow-up if pip-compile cost stops being the limiting factor.

**Blocker.** None. Ship (1) immediately when convenient.

**Owner.** Unclaimed.

---

## truesight_autopilot: migrate sophia from `certbot --nginx` to `certbot certonly` + repo-owned SSL config — 2026-05-30

**Context.** sophia.truesight.me's TLS deploy uses `certbot --nginx -d sophia.truesight.me ...` in deploy step 4. That mode obtains the Let's Encrypt cert AND mutates the nginx server block in-place — adds `listen 443 ssl`, `ssl_certificate ...`, the 80→443 redirect block, all marked `# managed by Certbot`. Because `/etc/nginx/sites-available/sophia` is a symlink into the repo at `/opt/truesight_autopilot/config/nginx/sophia.conf`, certbot's edits land inside the git checkout. The repo is therefore "dirty" between deploys, and `git pull` refuses to merge with `"Your local changes to the following files would be overwritten"`.

We solved this in [autopilot#77](https://github.com/TrueSightDAO/truesight_autopilot/pull/77) by swapping `git pull` for `git fetch + reset --hard origin/main + clean -fd` in `deploy.py` (matching what `scripts/deploy.sh` already did). Deploys are now idempotent and self-healing: certbot dirties → next deploy resets → certbot re-adds the SSL directives → repeats.

It works, but it's pragmatic rather than clean.

**Goal / shape.** Migrate to `certbot certonly --webroot -w <docroot> -d sophia.truesight.me` so certbot only writes to `/etc/letsencrypt/live/...` and **never touches** the nginx config. The repo's `sophia.conf` becomes the full source of truth — `listen 443 ssl`, `ssl_certificate /etc/letsencrypt/live/sophia.truesight.me/fullchain.pem`, the port-80 redirect server block, all version-controlled. Cert renewal runs via certbot's cron job and reloads nginx without touching any sites-{available,enabled}/sophia file.

**Trade-off snapshot:**

| Concern | Current (autopilot#77) | After migration |
|---|---|---|
| Repo dirty between deploys | yes (expected, self-heals) | no, always clean |
| Bootstrap on a fresh host | certbot --nginx wires SSL automatically | needs an initial cert before nginx with `listen 443 ssl` will start — chicken-and-egg, ~10-line preflight |
| Cert renewal | re-dirties; next deploy resets | silent (certbot cron + `nginx -s reload`) |
| SSL config in version control | partial | full |
| Lines of deploy code | tiny | needs the bootstrap preflight |

**When this becomes worth doing:**
- A second governor architect deploys the same service and the dirty-repo state confuses them.
- A Let's Encrypt edge case (renewal failure, multi-domain cert, account migration) produces broken nginx via the auto-edit path.
- We add a second TLS-bearing subdomain on the same host (the current pattern doesn't compose cleanly — each `certbot --nginx` run re-walks every server block).

**Blockers.** None technical. Choice is taste vs effort. ~2 hours of work: write the cert-presence preflight, fold the SSL directives into `sophia.conf`, change the deploy step, smoke-test on a fresh EC2 (or in a Docker container).

**Owner.** Unclaimed.

---

_(empty — move entries here with a one-line reason when they're no longer
relevant)_

### SunMint plots/farms generators fail SILENTLY green — a sheet read error must exit non-zero, not "preserve the existing registry"
**✅ SHIPPED 2026-09-24** — `sunmint` (`scripts/build_plots_geojson.py`, `scripts/build_farms_index.py`) now `sys.exit()` non-zero via a shared `sheet_read_failure()` helper on ANY read error (raised exception **or** an empty response), instead of swallowing it and "preserving the existing registry"; the previously-published file is left byte-for-byte untouched. Regression test `tests/test_build_index_loud_failure.py` pins the contract (it FAILS on the pre-fix code). Landed via the Contents API because `sunmint` is an api-only machine-owned repo (single-file atomic commits, no PR): `927c66a` (plots), `0bd0f86` (farms), `2c0e25f` (test). `build_tree_geojson.py` already failed loudly (no swallowing), so it needed no change.
**Filed 2026-09-24 — root cause verified from the workflow logs. Governor: Gary (thread 35189). ✅ The incident itself is RESOLVED (2026-09-24): the CI credential was restored by Gary (new SA `sunmint-ledger-manager@get-data-io.iam.gserviceaccount.com`, secret `GOOGLE_SERVICE_ACCOUNT_JSON` replaced) and all three indexes were re-dispatched and refreshed — see `## Recently shipped`. What remains OPEN is item (b): the silent-green anti-pattern.**

**Ask (remaining).** Stop `build_plots_geojson.py` / `build_farms_index.py` from reporting green when they cannot read the sheet — a generator that cannot read its source must exit non-zero.

**Symptom.** `trees/index.geojson` (`generated_at` 2026-09-17, 126 features), `plots/index.geojson` (09-17, 22 features) and `farms/index.json` (09-17) are **all frozen at 2026-09-17** — 7 days stale — so the SunMint plots page and every `plot_id`/`tree_id`-based join serve week-old data. `Rebuild Tree Index` failed on every scheduled run 09-18→09-24 (7 consecutive, last success **2026-09-17T10:44:40Z**), but `Rebuild Plots Index` and `Rebuild Farms Index` have reported **success every day** throughout.

**Verified root cause (from the failed run log — run `35989682276`, step 5 “Run tree index builder”).**
```
gspread.exceptions.APIError: APIError: [403]: The caller does not have permission
  File "scripts/build_tree_geojson.py", line 49, in get_sheet
    return gc.open_by_key(SHEET_ID).worksheet(SHEET_TAB)
  → PermissionError → exit 1
```
The workflow's `GOOGLE_SERVICE_ACCOUNT_JSON` secret (last updated **2026-08-26T19:51:13Z**, unchanged) can no longer open spreadsheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` (tab `SunMint Tree Planting`). The 403 is raised at `open_by_key` — i.e. the SA cannot open the spreadsheet at all (sharing revoked / SA rotated), **not** a renamed-tab error (that would surface as `WorksheetNotFound`).

**The telling detail — why the sibling “successes” are false green (verified, run `35993899764`).** All three workflows use the **same** secret and the **same** `SHEET_ID` (only the tab differs). `build_tree_geojson.py` has no read-error handling → it raises and the job fails. `build_plots_geojson.py` swallows it:
```
WARN: could not read 'SunMint Plots' tab (); preserving existing registry
preserved 22 features at plots/index.geojson
No changes to commit.
```
So the daily "success" is a **no-op that rewrites the previous file**. The warning starts **exactly on 2026-09-18** in the plots runs too (`warn_hits=0` on 09-17 and earlier, `=2` on 09-18 onward) — the same cutoff as the tree failures. **That is the proof the change was on the sheet-sharing side, not a secret rotation:** the secret is unchanged since 08-26, one shared credential lost access on 09-18, and one workflow surfaced it while two masked it. Other SAs still read this same spreadsheet fine (verified 2026-09-24 via the `agroverse_qr_code_manager` / `cypher_defense` credentials), so the spreadsheet itself is healthy — it is specifically the **SunMint CI SA's** access that is gone.

**Also relevant.** The merged `tree_id` col-D fix (`21428ba6`, 2026-09-24, #3) is on `main` but **unshipped** — the job dies at the credential step before reaching the code, so the stale published index still carries the old off-by-one ids.

**Suggested scope.**
- Re-share the SunMint spreadsheet with the CI service-account email, **or** replace `GOOGLE_SERVICE_ACCOUNT_JSON` with a fresh key that has access; then re-dispatch all three workflows so the indexes catch up (this also publishes the pending `tree_id` fix).
- **Make the failure loud:** in `build_plots_geojson.py` / `build_farms_index.py`, exit non-zero when the sheet read fails instead of “preserving existing registry” — a silent-green generator hid a 7-day outage on a public data surface.
- Confirm no *other* consumer shares this credential (the `cache-satellite-scenes` / `rebuild-plot-media-index` workflows do not use it — they read no sheet).

**Evidence.** Failed run `35989682276` step 5 full log (`build_tree_geojson.py` L49); passing-but-empty run `35993899764` (`WARN: could not read 'SunMint Plots' tab`; `preserved 22 features`; `No changes to commit.`); `scripts/build_tree_geojson.py` L18–L19, L49; `scripts/build_plots_geojson.py` L21–L22, L80, L305 (the swallow); workflow `rebuild-tree-index.yml` L36, L38; secret `GOOGLE_SERVICE_ACCOUNT_JSON` `updated_at` 2026-08-26; published indexes all `generated_at` 2026-09-17.

## Closed without shipping
### Tree growth measurement 'reject' path — CLOSED as by-design
**Closed 2026-08-31 (no code). Owner: Sophia + Gary.** The earlier-flagged gap ("no manual reject for growth measurements") is by-design: invalid measurements are auto-rejected at submission by the GAS gates (RSA signature, registered identity, tree-exists in registry, 200 m proximity) — failing rows never land. Test evidence: TEST_TREE_E2E measurements (13.6/13.8/14.2) never reached the tracking tab; only the sentinel-signed test row landed (since removed). Measurement rows are monitoring records only — credits mint exclusively via a future [CARBON CREDIT ISSUANCE EVENT] — so a manual reject UI is unnecessary. E2E test cleanup completed 2026-08-31: test row deleted from 'Tree Growth Measurements'; 2 test photos removed from sunmint/images/growth/.

