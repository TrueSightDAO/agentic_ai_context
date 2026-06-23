# Deploy Runbook: QR Self-Serve Currency Definition (PR3)

**Plan:** `QR_SELF_SERVE_CURRENCY_PLAN.md`
**PR1 (CLI + dispatch):** https://github.com/TrueSightDAO/dao_protocol/pull/131
**PR2 (GAS handler):** https://github.com/TrueSightDAO/tokenomics/pull/376
**Status:** PR1 + PR2 open, awaiting merge before deploy

---

## Prerequisites

- [ ] PR1 (#131) and PR2 (#376) are **merged** to `main`
- [ ] You have `clasp` logged in as `garyjob@agroverse.shop` (the script owner)
- [ ] You have SSH access to `dao_protocol_nelanco` (98.93.94.86)
- [ ] You have decided the UAT strategy (see §3 pre-flight below)

---

## Step 1: Sync local tokenomics checkout

```bash
cd ~/tokenomics
git checkout main
git pull origin main
```

Verify the new file is present:
```bash
ls google_app_scripts/agroverse_qr_codes/process_currency_definitions_telegram_logs.gs
```

---

## Step 2: Copy source files to clasp mirror

The clasp mirror at `clasp_mirrors/1N6o00…/` is the directory `clasp push` reads from.
Copy the relevant source files there:

```bash
MIRROR=clasp_mirrors/1N6o00N9VtRK_L3e0NQXEsmC6QME1KObZdmdbJgo0Tbgj_7P-ElNL5THn

# Copy all source files from agroverse_qr_codes to the mirror
cp google_app_scripts/agroverse_qr_codes/*.gs "$MIRROR/"
cp google_app_scripts/agroverse_qr_codes/*.js "$MIRROR/" 2>/dev/null
cp google_app_scripts/agroverse_qr_codes/manifest.json "$MIRROR/"
cp google_app_scripts/agroverse_qr_codes/appsscript.json "$MIRROR/" 2>/dev/null
cp google_app_scripts/agroverse_qr_codes/*.html "$MIRROR/" 2>/dev/null
cp google_app_scripts/agroverse_qr_codes/*.conf "$MIRROR/" 2>/dev/null
```

Verify the new handler file is in the mirror:
```bash
ls "$MIRROR/"
# Should include: process_currency_definitions_telegram_logs.gs
```

---

## Step 3: clasp push

```bash
cd "$MIRROR"
clasp push --force
```

Expected output: `└─ push: X files pushed` (no errors).

---

## Step 4: Update deployment version

List current deployments:
```bash
clasp deployments
```

You should see:
```
- AKfycbxtOS1OE3zd01IxfQ0Oo-Qurq0KSz15V9VFgVaZAWA @HEAD
- AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO @9
```

Create a new version and update the existing deployment:
```bash
# Create a new version
clasp version "Add processCurrencyDefinitionsFromTelegramChatLogs handler"
# Note the version number returned (e.g. @10)

# Update the existing deployment to the new version
clasp deploy --version-number 10 --description "Currency definition handler"
# OR if you want to update the existing deployment ID specifically:
# clasp undeploy AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO
# Then re-deploy with the same ID (not recommended — use version update)
```

**Important:** Do NOT create a new deployment ID — Edgar and 1MnAs reference the existing URL.

---

## Step 5: Configure Edgar webhook URL

SSH into the dao_protocol box:
```bash
ssh ubuntu@98.93.94.86
```

Back up the current `.env`:
```bash
cp /home/ubuntu/dao_protocol/.env /home/ubuntu/dao_protocol/.env.backup.$(date +%Y%m%d)
```

Add the webhook URL:
```bash
# Edit .env and add:
# DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION=https://script.google.com/macros/s/AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO/exec

# Using sed to append:
echo 'DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION=https://script.google.com/macros/s/AKfycbxn3siu2QrzCGdcsipt5FRxxMGY6gVPN1Z_tQdbfJY1GABsL1pZUlWpUbpdE_OymvIO/exec' >> /home/ubuntu/dao_protocol/.env
```

Restart the service:
```bash
sudo systemctl restart truesight-dao-protocol.service
sudo systemctl status truesight-dao-protocol.service
```

Verify the env var is loaded:
```bash
cat /proc/$(systemctl show -p MainPID truesight-dao-protocol.service | cut -d= -f2)/environ | tr '\0' '\n' | grep CURRENCY_DEFINITION
```

---

## Step 6: UAT

### Option A: UAT on prod with cleanup (recommended if sandbox lacks Currencies tab)

Run the CLI with `--dry-run` first to verify the payload:
```bash
truesight-dao-define-currency \
    --currency 'TEST Ceremonial Cacao (250g) — DELETE ME' \
    --price 25.00 \
    --serializable TRUE \
    --landing-page 'https://truesight.me/shop/ceremonial-cacao' \
    --ledger 'AGROVERSE' \
    --farm-name 'Fazenda Rendimento' \
    --state 'Bahia' \
    --country 'Brazil' \
    --year 2026 \
    --unit-weight-grams 250 \
    --dry-run
```

Then run without `--dry-run` to submit:
```bash
truesight-dao-define-currency \
    --currency 'TEST Ceremonial Cacao (250g) — DELETE ME' \
    --price 25.00 \
    --serializable TRUE \
    --landing-page 'https://truesight.me/shop/ceremonial-cacao' \
    --ledger 'AGROVERSE' \
    --farm-name 'Fazenda Rendimento' \
    --state 'Bahia' \
    --country 'Brazil' \
    --year 2026 \
    --unit-weight-grams 250
```

Check the Currencies tab in the Main Ledger for the new row. Verify:
- [ ] Row appears with all 12 columns populated
- [ ] Column C = TRUE
- [ ] Columns E–J are filled (QR-ready)
- [ ] Tab is sorted A→Z

**Clean up:** Delete the TEST row from the Currencies tab after verification.

### Option B: UAT on sandbox

If the sandbox sheet (`1qSi_-VSj7yiJl0Ak-Q3lch-l4mrH37cEw8EmQwS_6a4`) has a Currencies tab:
1. Temporarily switch `MAIN_LEDGER_URL` in the GAS handler to the sandbox URL
2. Deploy and test
3. Switch back to production URL and re-deploy

---

## Step 7: Update Version.js

After successful UAT, update `Version.js` in the tokenomics repo with the new deploy timestamp:

```javascript
var AGROVERSE_QR_GENERATION_LAST_CLASP_PUSH_UTC = '$(date -u +%Y-%m-%dT%H:%M:%SZ)';
```

And add a changelog line:
```
'2026-06-XX — Deployed processCurrencyDefinitionsFromTelegramChatLogs handler (PR3).\n' +
```

Commit and push this update.

---

## Rollback

If the deploy causes issues:

**GAS rollback:**
```bash
cd ~/tokenomics/clasp_mirrors/1N6o00…/
clasp deploy --version-number 9 --description "Rollback to pre-currency-definition"
```

**Edgar rollback:**
```bash
ssh ubuntu@98.93.94.86
# Remove the env var and restore backup:
cp /home/ubuntu/dao_protocol/.env.backup.$(date +%Y%m%d) /home/ubuntu/dao_protocol/.env
sudo systemctl restart truesight-dao-protocol.service
```

---

## Verification checklist

- [ ] `clasp push` succeeds (no syntax errors)
- [ ] Deployment version updated (not a new deployment ID)
- [ ] `DAO_PROTOCOL_WEBHOOK_CURRENCY_DEFINITION` set in `.env`
- [ ] `truesight-dao-protocol.service` restarted and healthy
- [ ] UAT: TEST currency row appears in Currencies tab with all 12 columns
- [ ] UAT: Tab is sorted A→Z
- [ ] UAT: TEST row deleted (if using prod)
- [ ] `Version.js` updated with deploy timestamp
