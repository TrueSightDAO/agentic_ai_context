# Credentialing — end-to-end validation runbook (cohort mode)

**Purpose:** prove that the full cohort-credentialing flow still works after any change to the credentialing stack (admin panel, GAS handler, lineage-engine renderer, build workflow, manifests, sheets). Written from the IVY E2E runs of 2026-08-20 (Tests 1–4, incl. v1.3 template + dual-signature render).

**Flow under test:**

```
Google Sheet roster row (pending)
  → admin panel sign-in (email verification, WebCrypto keypair)
  → Click Attest → signed [CREDENTIALING ATTESTATION EVENT] → Edgar
  → Process pending events (central GAS handler) → commit to lineage-credentials
  → build-cv-cache.yml auto-runs → _cache/ regenerated
  → credential profile + CV PDF + per-program certificate PDF (with signatures)
  → verify artifacts on GitHub main + jsDelivr + public profile page
```

---

## 0. When to run

- After ANY change to: `program_admin_endpoint.gs`, `build_cv_cache.py`, `cert_overlay.py`, program manifests, roster sheet schema, admin panel `index.html`/`config.json`, or the lineage-credentials workflow.
- After onboarding a NEW program (substitute the new slug/sheet/panel below).
- As a periodic smoke test (e.g. monthly).

## 1. Prerequisites

- **SSH access to `nelanco-claude`** (100.57.50.48) — has Playwright + Chromium, gspread, the IVY SA key at `/home/ubuntu/ivy_yoga_google_private_key.json`, and `gh` (garyjob PAT) for repo/run operations.
- **Admin mailbox access** (`admin@truesight.me`) — receives the verification email; the console's `admin@truesight.me` seat is a roster-sheet editor (= admin).
- **A fresh dummy row** inserted into the roster sheet (never attest a real learner in a smoke test).

## 2. Step-by-step

### 2.1 Insert a roster row (pending)

On nelanco-claude (`/tmp/ivy_e2e_insert.py` — adapt name/columns):

```python
import gspread
gc = gspread.service_account(filename="/home/ubuntu/ivy_yoga_google_private_key.json")
sh = gc.open_by_key("1IrzM8z9X0bt-1Zp21s6DNxlL_1XaT-8Fq6e3YaQRcnU")
ws = sh.worksheet("Cohort Roster")
ws.append_row(["Dummy E2E Test N (label)", "IVY Islamabad", "Yoga - Nov 2027",
               "14 November 2027", "", "", "Active", "dummy-e2e@example.com",
               "", "", "", "", "", "", "", "", "", "",
               "dummy E2E - inserted YYYY-MM-DD per Gary request", ""])
```

Verify: row appears in the panel's pending queue (see 2.3).

### 2.2 Sign in (admin, verified)

```bash
python3 /tmp/ivy_e2e_signin.py   # fills #emailInput=admin@truesight.me, clicks #signinBtn,
                                 # saves keypair to /tmp/ivy_e2e_pub.txt + _priv.txt
```

Then grab the fresh verification link from the admin mailbox (Gmail search `is:unread ivy` / `from:truesight`) — the URL contains `?em=...&vk=<token>`.

**Gotcha:** the verification email can lag indexing by a few seconds; re-query Gmail if the newest hit is an old run.

### 2.3 Verify sign-in + find the row

```bash
python3 /tmp/ivy_e2e_verify.py   # seed keypair, load the ?em&vk URL, wait ~10s
```

Expect: `ADMIN` mode, `STATUS VERIFIED`, `#identityCard` visible, pending queue shows your dummy row with an **Attest** button.

**Gotcha:** boot completes only when the page is loaded WITH the `?em&vk` params (the clean URL never fires the EMAIL VERIFICATION EVENT).

### 2.4 Attest

```bash
python3 /tmp/ivy_e2e_attest.py   # finds .attest-btn whose row contains "Dummy E2E", clicks it
```

Expect: queue shows the row leaving pending; eventually "Already attested N done".

### 2.5 Process pending events (MANDATORY)

**This is the step everyone misses.** The attest event lands in the Edgar intake and **waits** — it is NOT auto-committed. In the panel (admin mode) click the **"Process pending events"** button (fires `process_attestation_events` on the central GAS endpoint). Then expect: sheet row back-filled (`status=processed`, `pk_hash`, `github_commit_sha`), Audit Trail appended, and TWO commits in `lineage-credentials/programs/ivy-yoga/<pk-hash>/` (identity.json + attestations/<ts>.json).

Verify commits:
```bash
gh api "repos/TrueSightDAO/lineage-credentials/commits?per_page=5" --jq '.[] | .sha[0:8] + " " + (.commit.message | split("\n")[0])'
```

### 2.6 Wait for the build

```bash
# find the push-triggered run (event=push) and wait for completed/success
gh run list --repo TrueSightDAO/lineage-credentials -L 5 --json databaseId,status,event
gh run watch <RUN_ID> --repo TrueSightDAO/lineage-credentials
```

**Gotcha:** build takes ~2.5–4 min (fetch-depth:2 fix — was 20–60 min pre-2026-08-20). A build that checked out pre-commit and rebased can miss the new credential — if artifacts 404, dispatch a fresh run: `gh workflow run 277113125 --repo TrueSightDAO/lineage-credentials`.

### 2.7 Verify artifacts on GitHub main

Slug derives from `identity.names[0]` via slugify: `Dummy E2E Test 4 (v1.3)` → `dummy-e2e-test-4-v1-3`.

All should return 200 on raw.githubusercontent (and later jsDelivr):

```
_cache/cv/<slug>.json
_cache/cv/<slug>.md
_cache/cv/<slug>.pdf
_cache/cv/<slug>.qr.png
_cache/cv/<slug>__ivy-yoga.pdf
_cache/cv/<slug>__ivy-yoga.qr.png
_cache/cv/<slug>__ivy-yoga__cert.pdf
```

Also confirm aliases.json maps the pk-hash:
```bash
curl -sL https://raw.githubusercontent.com/TrueSightDAO/lineage-credentials/main/_cache/aliases.json | grep -c "<pk-hash>"
```

**Gotcha:** raw.githubusercontent and jsDelivr are CDN-cached; after a fresh commit, expect up to ~1–5 min staleness. If a lookup 404s, check the GitHub API (`gh api repos/.../contents/...`) which is authoritative.

### 2.8 Verify the certificate PDF content

```bash
curl -sL "https://raw.githubusercontent.com/TrueSightDAO/lineage-credentials/main/_cache/cv/<slug>__ivy-yoga__cert.pdf" -o /tmp/cert.pdf
python3 - <<'PY'
import pymupdf
doc = pymupdf.open("/tmp/cert.pdf")
txt = doc[0].get_text()
assert "200 hours" in txt          # v1.3 template wording
assert "Bilal Musharraf" in txt     # signature (script) + printed title
assert "Olivia Anselmo" in txt
assert "IVY-TT-0000" in txt         # cert ID placeholder (until PR3)
print("OK — certificate content valid, pages:", len(doc))
PY
```

Signatures land at: Bilal x≈111, Olivia x≈619 (Great Vibes over the signature lines). If both names are missing, the renderer's signature draw is broken (see lineage-engine PR #22).

### 2.9 Verify the live profile page

```
https://truesight.me/programs/ivy-yoga/credentials/#pk-<hash>
https://truesight.me/credentials/#<slug>          (QR target_url)
```

Playwright check: title should read "Credential — IVY" (NOT "Butterfly Effect" — the shell overrides from manifest), identity card shows name + lineage root "Indus Valley Yoga", both Download buttons resolve to 200s.

**Gotcha:** every credential page logs 2 benign console 404s — the tree-link probe (`lineage-assets/qrs/<pk>.json`). Expected feature check (only surfaces when a cacao tree is bound); do NOT treat as a failure.

## 3. Expected end-state summary

| Check | Pass when |
|---|---|
| Sheet row | status=processed, pk_hash, commit sha back-filled |
| Commits | identity.json + attestations/<ts>.json under programs/ivy-yoga/<pk-hash>/ |
| Build | push-triggered run completed/success (~2.5–4 min) |
| Artifacts | all 7 files 200 on main |
| aliases.json | contains pk-hash → slug |
| Cert PDF | 1 page, "200 hours", both signatures, VERIFY QR |
| Live page | "Credential — IVY" title, profile renders, downloads 200 |

## 4. Gotcha cheatsheet (all hit in real runs)

1. **Process pending events button is MANDATORY** — attest events sit in intake until clicked.
2. **Slug from names[0]** — parens/special chars become hyphens: `(v1.3)` → `-v1-3`.
3. **CDN staleness** — raw/jsDelivr lag commits; use GitHub API for truth.
4. **Boot needs the ?em&vk URL** — clean URL never verifies.
5. **Gmail indexing lag** — re-query for the fresh verification link.
6. **Benign tree-probe 404s** (2 console errors) — expected, not failures.
7. **Stale in-flight build can rebase over new commits** — re-dispatch if artifacts missing.
8. **compute-pressure / 403 throttle console noise** in Playwright — filter `Permissions policy violation: compute-pressure` and raw.githubusercontent 403s (agroverse_shop_beta #217 pattern).

## 5. Related docs

- `CREDENTIALING_COHORT_PROGRAM_ONBOARDING.md` — how to onboard a new program
- `plans/IVY_YOGA_COHORT_ONBOARDING_PLAN.md` — the IVY plan (PR3 = recertification + dual-signature)
- lineage-engine `scripts/build_cv_cache.py` + `scripts/cert_overlay.py`
- lineage-credentials `.github/workflows/build-cv-cache.yml` (fetch-depth:2, jsDelivr purge)
