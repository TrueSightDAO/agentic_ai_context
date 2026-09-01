# SunMint E2E Runbook

**Last validated:** 2026-08-29 (full-chain E2E, all green)
**Author:** Sophia Truesight (admin+sophia@truesight.me)

---

## 1. Purpose

Reproducible end-to-end test + operating guide for the SunMint tree pipeline:
email linking (digital signature), tree planting, growth monitoring, and
sentinel rights (mark-invalid). Written after the 2026-08-29 E2E that found
and fixed 6 real production bugs.

---

## 2. Pipeline map (as built)

```
Farmer site (beta.sunmint.truesight.me / sunmint.truesight.me)
  index.html  -> [EMAIL REGISTERED EVENT] / [TREE PLANTING EVENT]
  monitor-tree-growth/ -> [TREE GROWTH MONITORING EVENT] / [TREE PLANTING REJECT EVENT]
        |
        v  POST https://edgar.truesight.me/dao/submit_contribution (RSA-signed text)
Edgar = dao_protocol (Python/FastAPI, box: dao_protocol_nelanco)
  - verifies signature (RSA-2048, keypair in localStorage of the browser)
  - appends every submission to Telegram Chat Logs (sheet 1qbZZhf-..., tab "Telegram Chat Logs")
  - background dispatch_event(text) -> ROUTING table -> GAS webhook ?action=...
        |
        v
GAS webhooks (deployed /exec URLs)
  @7  (1Jp8q...)   ?action=processTreePlantingTelegramLogs        -> SunMint Tree Planting tab
  @36 (1UrBgq...)  ?action=processTreeGrowthMonitoringFromTelegramChatLogs -> Tree Growth Measurements tab
  (1UrBgq...)      ?action=processTreePlantingLinksFromTelegramChatLogs    -> Tree Planting Link tab
        |
        v
SunMint Tree Planting / Tree Growth Measurements tabs (sheet 1qbZZhf-...)
        |
        v
rebuild-tree-index.yml (GitHub Action) -> trees/index.geojson (public tree index)

PUBLIC ATTESTATION LEDGER (since 2026-08, A1-A4):
  Edgar (post-verify) -> ledger_emit.emit() (immediate) -> verify_public_signatures/<type>/<msg_id>.json
  30-min cron (autopilot box, sync_sunmint_signatures.py --push) -> reconciliation, idempotent by message ID
        |
        v
  https://raw.githubusercontent.com/TrueSightDAO/verify_public_signatures/main/index.json
  https://raw.githubusercontent.com/TrueSightDAO/verify_public_signatures/main/tree_planting/171.json
  Each file: public_key (PEM) + signature (base64) + signed_payload (exact bytes signed)
  Verify:  openssl dgst -sha256 -verify pub.pem -signature sig.bin payload.txt
```

---

## 3. Key identifiers

| Thing | Value |
|---|---|
| Edgar submit URL | https://edgar.truesight.me/dao/submit_contribution |
| SunMint sheets | 1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ |
|  - tabs | Telegram Chat Logs / SunMint Tree Planting / Tree Growth Measurements / Tree Planting Link |
| GAS 1Jp8q (planting) | 1Jp8qNIBCZaRTlmOmbJoJmYnSFyXtQkUHP2Qv5uqKZpt0Ugo-e25nhASF |
|  - deployment @7 | AKfycbyLQjTlM8nzAP-dybkOaCoOe02ahLPwUUnY6B6UAsCTJ80w49CFc_C7YM0k1ldp5Wew/exec |
| GAS 1UrBgq (webhook) | 1UrBgqLnnQc6PV4-gMIDh2SYwWu62wTdSrV30xk9q_eVr2UdoxdzXN38v |
|  - deployment @36 | AKfycbwm9TZDLPrG1vui3KjR4WHnydQAJXa5U7KHMygRnS9vN6oAwBLUw1q23nzzkmlSe0vq/exec |
| dao_protocol box | ssh dao_protocol_nelanco (ubuntu@ip-172-31-23-207, Nelanco PEM) |
| service | truesight-dao-protocol.service ; env /home/ubuntu/dao_protocol/.env |
| env keys | DAO_PROTOCOL_WEBHOOK_TREE_PLANTING_LINK / TREE_PLANTING_PROCESSING / TREE_GROWTH_MONITORING |
| Sophia identity | admin+sophia@truesight.me (sentinel=true, governor=false) |
| Sophia keys | /tmp/sophia_keys_clean.env (PUBLIC_KEY/PRIVATE_KEY raw base64 SPKI/PKCS8) |
| Tree index | TrueSightDAO/sunmint main trees/index.geojson |
| Write-capable SA | /opt/truesight_autopilot/config/google/edgar_dapp_listener_key.json |

---

## 4. The E2E procedure

### 4.0 Prereqs
- Playwright: cd /home/ubuntu/dapp_beta && NODE_PATH=/home/ubuntu/dapp_beta/node_modules node <script>.js
- Sophia keypair: source /tmp/sophia_keys_clean.env (strip the single-quote wrappers from .env values first)
- Keys are raw base64 SPKI/PKCS8 (NO PEM armor) - exactly what the site's localStorage expects

### 4.1 Email link
1. Launch chromium (headless) with addInitScript injecting localStorage.setItem('publicKey'|'privateKey', ...)
2. Open https://beta.sunmint.truesight.me/ , fill #emailInput with the test address, click #emailSubmitBtn
3. Expect: "Verifique seu email para confirmar o link." and emailRegistration.ok == true
4. If already ACTIVE: skipped:true, reason:public_key_already_active (expected for Sophia's key)

### 4.2 Sentinel check
- GET https://edgar.truesight.me/dao/check_digital_signature?signature=<URLENCODED pubkey>
- MUST urlencode the key (base64 has + and / which FastAPI mangles as space/path separators)
- Expect: {"registered":true,"contributor_name":"Sophia Truesight","is_sentinel":true}

### 4.3 Plant a tree (index.html)
1. Same browser, geolocation 44.560058,-123.262181, permissions: ['geolocation']
2. Set capturedPhotoBlob via bare identifier: page.evaluate(() => canvas.toBlob(b => { capturedPhotoBlob = b; },'image/jpeg',0.9))
   (it is a top-level lexical let - NOT on window)
3. Select species (e.g. 'Cacao - Criolla'), click #treeSubmitBtn
4. Expect POST 200, signature_verification: success, fileUploadedToGithub: true
5. Ledger: Telegram Chat Logs row [TREE PLANTING EVENT]

### 4.4 Monitor a tree (monitor-tree-growth/)
1. Same browser/keypair; select a tree from #treeSelect (or manual Tree ID input if not in index)
2. Set closeupBlob + contextBlob via bare-identifier canvas trick (top-level lets at ~line 438)
3. Fill DBH, click submit; expect "Measurement sent successfully!" AND a POST to edgar (capture via page.on('request'))
4. Ledger: row [TREE GROWTH MONITORING EVENT]

### 4.5 Mark invalid (sentinel rights)
- Gate: loadContributorIdentity() -> isCurrentUserGovernor() must be true (isGov || isSent)
- markTreeInvalid() builds [TREE PLANTING REJECT EVENT] text and shows it via navigator.share/prompt
- It makes NO network submission - it's share-by-hand by design. No ledger write happens.
- To prove the gate: invoke it, expect the confirm dialog + generated reject text.

### 4.6 Verify ingestion
1. Manually fire the webhook (or wait for auto-dispatch):
   curl -sL "https://script.google.com/macros/s/<@7>/exec?action=processTreePlantingTelegramLogs"
   curl -sL "https://script.google.com/macros/s/<@36>/exec?action=processTreeGrowthMonitoringFromTelegramChatLogs"
2. Check SunMint Tree Planting tab grew; check Tree Growth Measurements tab has the row
3. Trigger rebuild-tree-index.yml; confirm trees/index.geojson count grew

---

## 5. Incident traps (each cost real time - do not repeat)

1. clasp push deletes gitignored Credentials.js (2026-08-29, also 2026-08-19):
   clasp syncs the local folder; if Credentials.js is absent locally and not in .claspignore,
   push REMOVES it from the live project -> webhook dies with ReferenceError: setApiKeys is not defined.
   Fix: restore a seeding-only Credentials.js (getCredentials() reads Script Properties - secrets
   survive pushes) via Apps Script API updateContent (clasp refuses to push conflicting files);
   .claspignore now includes Credentials.js (PR #448).
2. git_push_changes edits can write empty files (2026-08-29, sunmint_beta #22):
   a failed edit-anchor match wrote a 0-byte index.html and merged it (beta served empty for ~10min).
   ALWAYS verify the PR diff is non-empty + node --check the inline JS before merging.
3. check_digital_signature must be called with URLENCODED key - raw + and / in the query string
   get decoded as space/path separators -> registered:false (false alarm; the site encodes properly).
4. Offline queue corrupts Blobs (sunmint_beta #28): JSON.stringify(Blob) -> {} ; store base64 dataURLs.
   Symptom: POST never fires, pending record stuck forever.
5. DBH (cm) regex metacharacters (tokenomics #446): labels are interpolated into RegExp raw -
   ( and ) break the match. Escape with escapeRe(). Symptom: webhook "1 skipped", sheet empty.
6. Stale local checkout before clasp push - always git pull --ff-only origin main first, then
   confirm the change is present locally BEFORE pushing (pushed stale code twice in this E2E).
7. Stale CDN/browser cache on beta - Pages+Varnish serve variants; hard refresh (?cb=...) for truth.

---

## 6. §5g cleanup pattern (test writes)

- Identity/registration rows: delete via write-capable SA (edgar_dapp_listener_key.json) with
  spreadsheets().batchUpdate deleteRows - the Cypher Defense SA is blocked by sheet protection.
- Ledger rows from real signed test submissions (tree plant/monitor): these are legitimate records
  proving the pipeline - keep them (flag to governor; they carry no monetary value).
- **Ledger files in verify_public_signatures are immutable public attestations** - emit/cron writes
  are append-only; test artifacts (e.g. SMOKE-REPRO-*, LEDGER-SMOKE) are flagged to the governor,
  never auto-deleted.
- Emails sent are normal artifacts - no cleanup.
- Test photos uploaded to sunmint/images/: remove via GitHub API if the governor wants them gone.

---

## 7. Sender (email verification) - admin@truesight.me

- Verification emails are sent by GAS project 1m8IZ... (owner admin@truesight.me); the web app's
  "Execute as" account is the sender. Deploy with the ADMIN clasp credential
  (/home/ubuntu/.clasprc-admin.json swapped into ~/.clasprc.json - clasp 3.3.0 ignores CLASPRC env).
- Cutover 2026-08-29: webhook now points at the admin-executed deployment @32 -> From: admin@truesight.me.
- clasp always uses ~/.clasprc.json (default); to deploy as admin, BACK UP gary's file, copy admin's in,
  deploy, then restore.

---

## 8. Status (2026-08-29)

- Full chain green: email link, sentinel, plant, monitor, mark-invalid (share-only).
- Bugs fixed & merged: sunmint_beta #28, tokenomics #441/#442/#446/#447/#448, dao_protocol #149.
- Box env keys all set; service active; auto-dispatch working (verified with live plantings).
- Open: test photo keep/remove call (sunmint/images/20260829134704_MIIBIjANBgkqhkiG9w0B.jpg).
