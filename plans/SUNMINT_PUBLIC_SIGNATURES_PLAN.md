# SunMint Public Signatures Cache — Public Audit Surface for All SunMint RSA Events

**Status:** new — awaiting kickoff
**Owner:** Gary Teh
**Requested by:** Gary Teh, 2026-09-01 (thread 17194)
**Goal:** Every SunMint-associated RSA-signed event gets a **publicly auditable GitHub JSON cache record** — `TrueSightDAO/sunmint/signatures.json` keyed by event/message ID — plus a **public link-share surface for the Tree Growth Measurements tab**.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. Update the resume tracker as units land; report the DAO
> contribution after each merge (§7). §5a: **one PR per execution turn, then stop.**

---

## 0. Decisions (Gary — confirm or override)

| # | Decision | Proposed choice |
|---|----------|-----------------|
| 0.1 | Cache location | `TrueSightDAO/sunmint` repo (public), file **`signatures.json`** at repo root — alongside `trees/index.geojson`, `plots/index.geojson`, `images/growth/`. |
| 0.2 | Event scope | **All SunMint-associated RSA-signed events**: `[EMAIL REGISTERED EVENT]`, `[TREE PLANTING EVENT]`, `[TREE GROWTH MONITORING EVENT]`, `[TREE PLANTING REJECT EVENT]`, `[TREE PLANTING LINK EVENT]`. |
| 0.3 | PII policy | **No PII.** Public key (already public via `check_digital_signature`), signature, full signed event text, contributor display name (already public on the impact map), tree/geo data already public in the geojson. **No emails, no phones, no private keys.** |
| 0.4 | Link-share form for Tree Growth Measurements | **Default: public JSON cache `tree_growth_measurements.json`** in the same repo + stable shareable per-measurement raw URL (matches the house pattern; sheet stays private). Fallback if Gary prefers: Google Sheets public link-share of the tab. |
| 0.5 | Writer | **Autopilot cron** `sync_sunmint_signatures.py` (verbatim mirror of `sync_pending_caches.py` — GITHUB_TOKEN + gspread creds already on the box, 30-min cadence). Alternative: GAS pushes from the webhook (`TGM_GITHUB_TOKEN` set 2026-08-31). Default keeps GitHub writes on the box where they are already proven. |

---

## 1. Why

- **Verifiable dMRV:** a VVB or any third party must be able to independently verify that every tree event was RSA-signed by the farmer's key. Today the signature lives only in a private sheet (Telegram Chat Logs col G / tab col F) — not publicly auditable.
- **Crediting-period evidence:** monitoring data accumulates as evidence over a crediting period (SunMint model, `plans/SUNMINT_TREE_GROWTH_MONITORING_PLAN.md` §3); the public signature ledger is the audit trail a future `[CARBON CREDIT ISSUANCE EVENT]` can cite.
- **Self-verifying by design:** `signed_text` + `signature` + `public_key` in one public record — anyone can re-verify offline (openssl). No trusted intermediary needed.
- **Cheap:** static JSON on GitHub raw — zero infra, immutable history, diffable per commit.

---

## 2. Pre-flight — captured facts (§5d: no PR below should need to re-discover any of this)

### 2.1 Signature flow (verified — `SUNMINT_E2E_RUNBOOK.md`)

```
Farmer site (sunmint_beta/prod: index.html + monitor-tree-growth/)
  RSA-2048 sign in-browser (keypair in localStorage)
        v  POST https://edgar.truesight.me/dao/submit_contribution
Edgar (dao_protocol) verifies signature
        v  appends FULL SIGNED SUBMISSION TEXT to Telegram Chat Logs (sheet 1qbZZhf-..._pyzASQ)
GAS webhooks parse into SunMint Tree Planting / Tree Growth Measurements / Tree Planting Link tabs
```

### 2.2 Sheets + schemas

- **Telegram Chat Logs** (sheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`) — col G = Contribution Made = full signed submission text (the raw signature source).
- **SunMint Tree Planting** tab (gid `176124122`): A=Telegram Update ID, B=Chatroom ID, C=Chatroom Name, **D=Telegram Message ID (stable dedup key)**, E=Contributor Handle, **F=Contribution Made (full signed text)**, G=Status date, H=Telegram File IDs, I=Photo of Tree Planted, J=Submitted Name, K=Lat, L=Lng, M=Status, N=Specie, O=GitHub Commit URL, P=Cost, Q=Tree Planting Time.
- **Tree Growth Measurements** tab: A=Telegram Update ID, **B=Telegram Message ID (dedup key)**, C=Tree ID (QR Code), D=Species, E=DBH (cm), F=AGB (kg), G=CO2e (kg), H=Lat, I=Lng, J=Measured At, K=Close-up Photo URL, L=Context Photo URL, M=Analysis Commit URL, N=Analysis SHA-256, **O=Farmer Signature**, P=Contributor Name, Q=Status, R=Processed Timestamp.

### 2.3 The proven pattern to copy (key pre-flight fact)

`/home/ubuntu/scripts/sync_pending_caches.py` on the autopilot box, cron `*/30 * * * *` with `GOOGLE_APPLICATION_CREDENTIALS=/home/ubuntu/creds/google_credentials.json` + `GITHUB_TOKEN=<repo-scoped PAT>`: gspread reads the sheet → builds public JSON (`sunmint_pending.json`, `sold_pending_tree.json` in `TrueSightDAO/lineage-assets`) → sha-aware GitHub Contents-API PUT (skips on 422 unchanged) → prints commit sha. **NO PII in caches (owner emails intentionally omitted).** This exact script shape is the template for `sync_sunmint_signatures.py`.

### 2.4 Keys / credentials

- SunMint spreadsheet: `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` (Telegram Chat Logs / SunMint Tree Planting / Tree Growth Measurements / Tree Planting Link tabs)
- GAS webhooks: `1Jp8q…` (planting, @7), `1UrBgq…` (growth @36 + planting-link)
- GITHUB_TOKEN (repo-scoped PAT) in cron env on autopilot box — proven for Contents-API PUTs
- `TGM_GITHUB_TOKEN` Script Property set (2026-08-31) — GAS→GitHub viable if decision 0.5 flips
- Sophia identity: `admin+sophia@truesight.me` (sentinel) — signature events are farmer-keyed, not Sophia's

---

## 3. Target architecture

### 3.1 `signatures.json` (public, `TrueSightDAO/sunmint` repo root)

```json
{
  "status": "success",
  "generated_at": "2026-09-01T00:30:00Z",
  "schema_version": 1,
  "count": N,
  "events": {
    "<telegram_message_id>": {
      "event_type": "TREE GROWTH MONITORING EVENT",
      "telegram_message_id": "...",
      "telegram_update_id": "...",
      "submitted_at": "...",
      "contributor_name": "...",
      "public_key": "...",
      "signature": "...",
      "signed_text": "...",
      "source_tab": "SunMint Tree Planting | Tree Growth Measurements | ...",
      "linked_tree_id": "..."
    }
  }
}
```

- **Keyed by event/message ID** (Telegram Message ID — the stable dedup key in both tabs), per Gary's request.
- `signed_text` = the exact string that was signed (col F of the tabs) → anyone can re-verify `signature` over it with `public_key` via `openssl dgst -sha256 -verify`.
- `public_key` = base64 SPKI matching `Contributors Digital Signatures` / `check_digital_signature` format.

### 3.2 `tree_growth_measurements.json` (public link-share of Tree Growth Measurements)

One entry per measurement row (dedup by col B): Tree ID, Species, DBH, AGB, CO2e, Lat/Lng, Measured At, Close-up + Context photo URLs, Analysis Commit URL, Analysis SHA-256, **Farmer Signature (col O)**, Contributor Name (col P), Status, Processed Timestamp.

### 3.3 Public link-share

- Stable shareable URL per measurement: `https://raw.githubusercontent.com/TrueSightDAO/sunmint/main/tree_growth_measurements.json#<msg_id>` (optionally a future `truesight.me/sunmint` measurement page — P4+, out of scope).
- If Gary picks the sheet-link fallback (0.4): share the tab via Google Sheets public link instead — no JSON work for that leg.

---

## 4. Build sequencing (§5a: **ONE PR PER TURN, then stop**)

| Unit | Repo | What | Gate |
|------|------|------|------|
| **PR0** | agentic_ai_context | This roadmap + HANDOFF_MANIFEST row (thread 17194) | none — this PR |
| **PR1** | truesight_autopilot | `scripts/sync_sunmint_signatures.py` — reads Telegram Chat Logs + both SunMint tabs via gspread, builds `signatures.json` + `tree_growth_measurements.json`, sha-aware PUT to `TrueSightDAO/sunmint`. **No cron yet.** Local tests + `--dry-run` | `gate: dry-run diff review with Gary` (JSON shape + PII scan before anything goes public) |
| **PR2** | autopilot box (ops) | Add crontab `*/30 * * * *` mirroring sync_pending_caches; run once for real; confirm both JSONs live on raw.githubusercontent.com; **offline re-verify 3 sample signatures** (openssl over signed_text) | `gate: 3/3 signature re-verifications pass` |
| **PR3** | sunmint | Public link-share surface per decision 0.4 (README section + stable URL pattern, or Google-sheet public share if that's the pick) | — |
| **PR4** | agentic_ai_context | Docs: `SUNMINT_E2E_RUNBOOK.md` §2 pipeline map + §6 update; `GAS_SCRIPT_PROPERTIES.md` if GAS path used; UAT checklist §6 below | **`gate: UAT`** |

No prod, no money, no default-branch self-merge anywhere in scope. `sunmint` repo = API-only data repo → **single-file Contents-API writes from the script**, never branch-edit PRs.

---

## 5. Security / PII guardrails

- Public repo → **no emails, no phone numbers, no private-key material, no bearer tokens**. Only: public keys (already public), signatures, signed event text, display names (already public on the impact map), public tree/geo data (already public in geojson).
- **Never trust the sheet's verification column** — the `signed_text` + `signature` + `public_key` triple is self-verifying; Edgar's `check_digital_signature` is the authoritative re-check.
- Scripts must never log the GITHUB_TOKEN (sync_pending_caches precedent — env-var only, token from cron env).
- Script runs `--dry-run` by default; `--push` only with explicit env creds (same contract as the template).

---

## 6. UAT checklist

1. `signatures.json` fetchable via raw.githubusercontent.com (incognito), valid JSON, `count` > 0.
2. **3 sample events** (≥1 planting, ≥1 growth, plus reject/link if present): offline re-verify signature over `signed_text` with the farmer public key → 3/3 match.
3. Every event type present maps to exactly one entry keyed by message ID; zero duplicates.
4. `tree_growth_measurements.json` rows == Tree Growth Measurements tab rows (dedup by col B), incl. Farmer Signature + Analysis SHA-256.
5. New measurement submission appears in both the tab and the JSON within ≤35 min (cron cadence).
6. PII scan: grep both JSONs for `@` email pattern + phone patterns → zero hits.
7. Public URL shares without auth (incognito window).

---

## 7. Contribution reporting

After each merge, report the DAO contribution per `OPERATING_INSTRUCTIONS.md` §6 with the PR URL. Sophia reports time as `[CONTRIBUTION EVENT]` (`create_dao_submission`, Time (Minutes)); no TDG auto-issue.
