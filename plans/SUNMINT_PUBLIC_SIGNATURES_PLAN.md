# Public RSA Signature Ledger — Org-wide Auditable GitHub JSON Cache

**Status:** in execution — pivoted to org-wide ledger (2026-09-01, Gary) · legacy sunmint path (PR0–PR3) superseded
**Owner:** Gary Teh
**Requested by:** Gary Teh, 2026-09-01 (thread 17194)
**Goal:** Every RSA-signed DAO event — SunMint today; contribution reporting, sales, inventory movement and future event types tomorrow — gets a **publicly auditable GitHub JSON cache record** in `TrueSightDAO/verify_public_signatures`: **one immutable JSON file per event**, bucketed by event type, plus an org-wide `index.json`. Also: **public link-share surface for the Tree Growth Measurements tab**.

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. Update the resume tracker as units land; report the DAO
> contribution after each merge (§7). §5a: **one PR per execution turn, then stop.**

---

## 0. Decisions (Gary — confirmed or override)

| # | Decision | Chosen (final) | Rationale / history |
|---|----------|---------------|---------------------|
| 0.1 | Ledger location | **`TrueSightDAO/verify_public_signatures`** (public, currently empty — purpose-built name) | Pivoted 2026-09-01 from `sunmint/signatures.json`: an org-wide ledger needs an org-wide home; `sunmint` is tree-specific |
| 0.1b | File layout | **One immutable JSON per event**, per-event-type subfolders + `index.json` per folder + root `index.json` | Pivoted 2026-09-01 from single aggregate file: no size ceiling, real per-attestation URL (raw JSON fragments don't deep-link), append-only emission fits emit business logic, matches `lineage-assets` `qrs/<qr-id>.json` convention |
| 0.2 | Event scope | **All RSA-signed events**, bucketed by type: `tree_planting/`, `tree_growth_monitoring/`, `tree_planting_link/`, `tree_planting_reject/`, `email_registered/` (later: `contribution/`, `sales/`, `inventory_movement/`, …) | EMAIL REGISTERED contains a farmer email in signed_text — redaction breaks verification → excluded until a redaction-preserving design (§5) |
| 0.3 | PII policy | **No PII.** Public keys, signatures, signed text, display names (already public on the impact map), tree/geo data only. Fail-closed email scan on every build. No emails, phones, private keys. | — |
| 0.4 | Link-share form (Tree Growth Measurements) | **Public JSON cache** in the ledger: `tree_growth_monitoring/<msg_id>.json` + index; stable per-measurement raw URL. Sheet stays private. | — |
| 0.5 | Writer | **Primary: dao_protocol emit hook at verify time** (deploy-gated). **Reconciliation: autopilot cron** `sync_sunmint_signatures.py` (existing, retargeted to new repo/layout) | Pivoted 2026-09-01: emit-at-verify = only verified attestations published, instant freshness, single choke point sees every event type; cron heals any emit gap within 30 min |

---

## 1. Why

- **Verifiable dMRV:** a VVB or any third party must be able to independently verify that every tree event was RSA-signed by the farmer's key, without trusting us. Today the signature lives only in a private sheet.
- **Org-wide auditability:** contribution, sales and inventory events are also RSA-signed; one ledger gives every attestation a stable, citable public URL.
- **Crediting-period evidence:** monitoring data accumulates as evidence over a crediting period; the public signature ledger is the audit trail a future `[CARBON CREDIT ISSUANCE EVENT]` can cite.
- **Self-verifying by design:** `signed_payload` (exact bytes signed) + `signature` + `public_key` in one public record — anyone re-verifies offline (openssl). No trusted intermediary.
- **Cheap + scalable:** static per-event JSON on GitHub raw — zero infra, immutable history, per-file git audit trail, no size ceiling.

---

## 2. Pre-flight — captured facts

### 2.1 Signature flow (verified — `SUNMINT_E2E_RUNBOOK.md`)

```
Farmer site (sunmint_beta/prod)
  RSA-2048 sign in-browser (keypair in localStorage)
        v  POST https://edgar.truesight.me/dao/submit_contribution
Edgar (dao_protocol) verifies signature  ← EMIT HOOK HERE (0.5)
        v  appends FULL SIGNED SUBMISSION TEXT to Telegram Chat Logs (sheet 1qbZZhf-…_pyzASQ)
GAS webhooks parse into SunMint Tree Planting / Tree Growth Measurements / Tree Planting Link tabs
Cron sync_sunmint_signatures.py (reconciliation) reads sheets → per-event files
```

### 2.2 Sheets + schemas

- **Telegram Chat Logs** (sheet `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ`) — col G = Contribution Made = full signed submission text (raw signature source).
- **SunMint Tree Planting** tab (gid `176124122`): A=Telegram Update ID, B=Chatroom ID, C=Chatroom Name, **D=Telegram Message ID (stable dedup key)**, E=Contributor Handle, **F=Contribution Made (full signed text)**, G=Status date, H=Telegram File IDs, I=Photo of Tree Planted, J=Submitted Name, K=Lat, L=Lng, M=Status, N=Specie, O=GitHub Commit URL, P=Cost, Q=Tree Planting Time.
- **Tree Growth Measurements** tab: A=Telegram Update ID, **B=Telegram Message ID (dedup key)**, C=Tree ID (QR Code), D=Species, E=DBH (cm), F=AGB (kg), G=CO2e (kg), H=Lat, I=Lng, J=Measured At, K=Close-up Photo URL, L=Context Photo URL, M=Analysis Commit URL, N=Analysis SHA-256, **O=Farmer Signature**, P=Contributor Name, Q=Status, R=Processed Timestamp.

### 2.3 The proven pattern to copy

- `sync_pending_caches.py` on the autopilot box, cron `*/30 * * * *`: gspread → public JSON → sha-aware GitHub Contents-API PUT (skips 422 unchanged). **NO PII.** Template for the retargeted sync script.
- `lineage-assets` convention: **one JSON per entity** (`qrs/<qr-id>.json`) — "Why JSON-per-QR, not aggregated" (append-only diffs, independently fetchable, git history = audit trail, scales linearly). The per-event ledger mirrors this.
- **Verification algorithm** (`signature_verifier.rb`): signed payload = text **up to and including the `--------` separator**, joined `\n`, stripped. "My Digital Signature" field = **public key** (SPKI); "Request Transaction ID" field = **signature** (RSASSA-PKCS1-v1_5 + SHA256). Already proven: 73/73 live events re-verify offline.

### 2.4 Keys / credentials

- SunMint spreadsheet: `1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ` (Telegram Chat Logs / SunMint Tree Planting / Tree Growth Measurements / Tree Planting Link tabs)
- GAS webhooks: `1Jp8q…` (planting, @7), `1UrBgq…` (growth @36 + planting-link)
- GITHUB_TOKEN (repo-scoped PAT) in cron env on autopilot box — proven for Contents-API PUTs
- `TGM_GITHUB_TOKEN` Script Property set (2026-08-31) — GAS→GitHub viable if ever needed
- **`verify_public_signatures` repo exists (public, empty)** — no repo creation needed
- dao_protocol emit hook needs its own repo-scoped PAT (keep separate from autopilot's) — create at A4

---

## 3. Target architecture

### 3.1 Layout (`TrueSightDAO/verify_public_signatures`)

```
verify_public_signatures/
├── README.md                       # purpose, layout, schema, openssl verify how-to
├── index.json                      # org-wide: event_type → count, subfolder links, latest commit per type
├── tree_planting/
│   ├── index.json                  # message_id → url, submitted_at, commit_sha
│   └── 171.json                    # ONE immutable file per event (message ID = dedup key)
├── tree_growth_monitoring/
│   ├── index.json
│   └── <msg_id>.json
├── tree_planting_link/ …           # (existing 73 migrate into these folders by event type)
├── tree_planting_reject/ …
└── email_registered/ …             # empty until redaction design (0.2/§5)
```

### 3.2 Record schema (per-event file)

```json
{
  "schema_version": 1,
  "event_type": "TREE GROWTH MONITORING EVENT",
  "telegram_message_id": "…",
  "telegram_update_id": "…",
  "submitted_at": "…",
  "contributor_name": "…",
  "public_key": "…",                 // base64 SPKI
  "signature": "…",                 // RSASSA-PKCS1-v1_5 over SHA-256 (base64)
  "signed_payload": "…",            // EXACT bytes signed (text up to & incl. -------- separator) → openssl target
  "signed_text": "…",               // full signed submission text (context)
  "source_tab": "SunMint Tree Planting | Tree Growth Measurements | …",
  "linked_tree_id": "…"
}
```

- One immutable file per event; **message ID is the stable dedup key**; sha-aware PUT skips unchanged.
- Test/synthetic + malformed submissions → `test_events/` (or excluded) — public ledger carries only verifiable records.

### 3.3 `index.json` (per folder + root)

Registry for enumeration: `message_id → url, event_type, submitted_at, commit_sha`. Keeps aggregate reads cheap without a giant file; consumers fan out to per-event URLs.

### 3.4 Public link-share

- **Per-event URL:** `https://raw.githubusercontent.com/TrueSightDAO/verify_public_signatures/main/tree_planting/171.json`
- **Per-measurement share URL:** `…/tree_growth_monitoring/<msg_id>.json`
- (Optional future `truesight.me` measurement page — P4+, out of scope.)

---

## 4. Build sequencing (§5a: **ONE PR PER TURN, then stop**)

### Already done (legacy sunmint path — superseded by this pivot)

| Unit | Repo | What | Status |
|---|---|---|---|
| PR0 | agentic_ai_context | Original roadmap + manifest row | ✅ merged (`0629a6d`) |
| PR1 | truesight_autopilot | `sync_sunmint_signatures.py` (73 events, 100% verify) | ✅ merged (PR #354) |
| PR2 | autopilot box (ops) | cron `*/30` + first live publish + 3/3 re-verify | ✅ live |
| PR3 | sunmint | README documents `signatures.json` + measurements | ✅ live (`1c49a96`) |

Legacy `sunmint/signatures.json` + `tree_growth_measurements.json` remain live as a **deprecated mirror** through migration; A2 stops writing them after one transition sync.

### Post-pivot sequencing

| Unit | Repo | What | Gate |
|------|------|------|------|
| **A1** | agentic_ai_context | This plan amendment | none — this PR |
| **A2** | truesight_autopilot + verify_public_signatures | Retarget `sync_sunmint_signatures.py` → per-event files + indexes in `verify_public_signatures`; **migrate 73 live events** (one-time run); init repo (root `index.json`); local tests + `--dry-run` | `gate: dry-run diff review with Gary` (layout + PII scan before any push) |
| **A3** | verify_public_signatures | README: layout, schema, openssl verify how-to, per-event URL pattern | — |
| **A4** | dao_protocol | **Post-verify emit hook**: on verified submission, PUT `<type>/<msg_id>.json` at ingest (idempotent by message ID, PII fail-closed, PAT fallback to `github_pat`). Deploy-gated. | ✅ **complete** (merged #151, deployed, smoke-verified live 2026-08-31) |
| ~~A4.1~~ | dao_protocol | ~~Normalize emit `public_key` to PEM~~ — **dropped**: `verify.verify()` already returns PEM; emit-written files verified identical to cron format. | ✅ dropped (false alarm) |
| **A5** | agentic_ai_context | Docs: `SUNMINT_E2E_RUNBOOK.md` §2 pipeline map + §6 update; ledger README links; UAT checklist §6 below | **`gate: UAT`** |

No prod (dapp/shop/truesight_me/sunmint sites), no money, no default-branch self-merge anywhere in scope. `verify_public_signatures` = API-only data repo → **single-file Contents-API writes** from script + emit hook, never branch-edit PRs.

---

## 5. Security / PII guardrails

- Public repo → **no emails, no phone numbers, no private-key material, no bearer tokens**. Only public keys, signatures, signed event text, display names, public tree/geo data.
- **Never trust the sheet's verification column** — `signed_payload` + `signature` + `public_key` triple is self-verifying; Edgar's verifier is the authoritative re-check.
- **EMAIL REGISTERED** signed_text contains the farmer's email → redaction would break verification. **Excluded from the public ledger until a redaction-preserving scheme exists** (e.g. publish SHA-256 of signed_text + signature only). Tracked as an open item in OPEN_FOLLOWUPS.md.
- Scripts must never log GITHUB_TOKEN (sync_pending_caches precedent — env-var only).
- Script runs `--dry-run` by default; `--push` only with explicit env creds.

---

## 6. UAT checklist (A5)

1. `verify_public_signatures/index.json` + a per-event file fetchable via raw.githubusercontent.com (incognito), valid JSON, `count` > 0.
2. **3 sample events** (≥1 planting, ≥1 growth, plus reject/link if present): offline re-verify `signature` over `signed_payload` with the farmer public key → 3/3 match.
3. Every event type maps to exactly one entry keyed by message ID; zero duplicates; per-event file name == message ID.
4. `tree_growth_monitoring/index.json` rows == Tree Growth Measurements tab rows (dedup by col B), incl. Farmer Signature + Analysis SHA-256.
5. New measurement submission appears in tab + ledger within ≤35 min (cron cadence; immediate via emit hook once A4 ships).
6. PII scan: grep both JSONs for `@` email pattern + phone patterns → zero hits.
7. Public URL shares without auth (incognito window).
8. Post-migration: `sunmint/signatures.json` no longer updated (deprecated mirror), READMEs point to the ledger.

---

## 7. Contribution reporting

- DAO contribution via `create_dao_submission` after each merged PR (A1–A5), per OPERATING_INSTRUCTIONS §7.
