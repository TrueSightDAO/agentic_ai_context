# Public-Key Lookup Cache — Content-Addressed Per-Key Store — Execution Roadmap

**Status as of 2026-06-16:** design approved (Gary + Claude); **PR1 ✅ done** — see [tokenomics#359](https://github.com/TrueSightDAO/tokenomics/pull/359).
**Repos under change:** `tokenomics` (generator GAS), `treasury-cache` (data surface),
`truesight_autopilot` (reader), `dapp` (later consumer).
**Designed by:** Gary Teh + Claude · **Implemented by:** TBD (open PRs; `truesight_autopilot`
is own-repo / human-merge gated).

> **RESUME HERE:** PR2 — incremental write (diff-based) · `tokenomics` GAS
>
> **⚠️ ONE PR PER TURN (mandatory — `OPERATING_INSTRUCTIONS.md §5a`):** an execution turn does
> **exactly the single `RESUME HERE` PR, opens it, reports the contribution, ticks the tracker,
> and STOPS.** Do **not** chain PR1→PR2→PR3 in one turn — that is what choked Sophia on
> 2026-06-16 (whole-roadmap turn exhausted the 30-round cap → empty response). The next turn
> resumes the next PR.

---

## 1. Why

Today every "is this key a governor?" check fetches and parses the **entire**
`treasury-cache/dao_members.json` (≈129 KB today, one contributor alone has ~56 keys)
and filters it in memory. Three problems compound as the DAO grows:

1. **Read cost is O(n).** The vault has the *one* key it cares about (from the signed
   challenge) but must pull and walk the whole blob to answer a point question.
2. **Generation cost grows.** The GAS publisher
   (`tokenomics/.../dao_members_cache_publisher.gs`) rebuilds and commits the whole
   monolith on every `[EMAIL VERIFICATION EVENT]` and on a daily cron — the commit /
   payload grows with the entire contributor base.
3. **Staleness bug (observed 2026-06-16).** `governor_registry` caches the monolith for
   5 min (`GOVERNORS_CACHE_TTL=300`) with no manual refresh. A freshly-registered
   governor key (Gary's, created `10:21:48Z`) was denied at the vault until the cache
   aged out / the worker was restarted. Refreshing means re-pulling the whole blob, so
   the system biases toward *not* refreshing.

**Reframe:** the lookup is a point question on a value you already hold → make it a
**content-addressed fetch**. Hash the key, fetch one tiny file named by that hash.

## 2. Design

### 2.1 Storage shape

```
treasury-cache/
  dao_members.json            # KEPT — enumeration + back-compat fallback
  public_keys/
    _manifest.json            # { "<sha256>": "<git-blob-sha>", ... } for incremental writes
    <sha256(public_key)>.json # one file per key, point-lookup target
```

Per-key file (`schema_version: 1`):

```json
{
  "schema_version": 1,
  "sha256": "<hex>",
  "public_key": "MIIB...full base64...",
  "contributor": "Gary Teh",
  "roles": ["member", "governor"],
  "status": "ACTIVE",
  "created_at": "2026-06-16T10:21:48.000Z",
  "last_active_at": "...",
  "generated_at": "..."
}
```

### 2.2 Why hash the filename (not the raw key)

RSA public keys in base64 contain `/` and `+` (e.g. Gary's `…BC/wdPY6…`). `/` is a path
separator → it would create phantom subdirectories and break raw URLs. **Filename =
`sha256(public_key_b64)` hex** → path-safe, fixed 64-char length, and aligns with the
existing `pk_hash` pattern already used on credential/CV pages.

### 2.3 Reader (point lookup)

`governor_registry.resolve_key(public_key) -> identity | None`:
1. `h = sha256(public_key)`
2. short per-key in-memory cache (e.g. 60 s) keyed by `h`
3. fetch `public_keys/<h>.json`
4. validate `status == "ACTIVE"`; map `roles` → `is_governor = "governor" in roles`
5. miss/404 → `None`

`load_governors()` / the monolith is **retained** as (a) the enumeration source and
(b) a fallback if a per-key file is absent — so nothing breaks during migration.

### 2.4 Freshness — retires the 2026-06-16 bug

Because a per-key fetch is ~1 KB, the reader can afford to **force one fresh lookup on a
denied sign-in** before refusing. Use the GitHub **contents API** (not raw) for the
sign-in lookup: `raw.githubusercontent.com` has its own ~5-min CDN cache (and can cache
404s), whereas `api.github.com/repos/.../contents/...` is fresh. Authenticate the request
with the autopilot PAT to get the 5 000/hr limit instead of 60/hr unauth.

### 2.5 Revocation

A key going non-ACTIVE must stop granting access. The generator writes `status:"REVOKED"`
(preferred over deleting, so audit history survives) and the reader treats anything
`!= "ACTIVE"` as deny.

### 2.6 Incremental generation

The GAS publisher writes **all per-key files in ONE commit** via the Git Trees API
(create blobs → tree → commit → update ref) — never N commits. It diffs against
`_manifest.json` (hash → last blob sha) and only creates blobs for **changed/added/removed**
keys, so an unchanged key base produces a near-empty tree update. The sheet *read* stays
full (not the bottleneck); the *commit churn* — the part that grows — becomes diff-sized.

### 2.7 Caveats (eyes open)

- **GitHub is not a database.** Fine at login volume; if one day every API call validates a
  key, front it with a real edge cache / KV. Keep the reader interface narrow so the backend
  can be swapped.
- **Privacy.** `dao_members.json` already exposes `email` publicly. The vault's access
  decision needs only `contributor` + `roles` + `status` — **omit `email`** from per-key
  files unless a consumer needs it (see pre-flight decision). Cross-ref
  `feedback_no_email_on_public_cv`.
- **File count.** Thousands of files are fine for git/raw; tens of thousands slows tree ops —
  revisit sharding (`public_keys/<h[:2]>/<h>.json`) only if it gets there.

---

## 3. Pre-flight checklist (confirm BEFORE coding)

- [ ] **Consumer audit.** Classify every `load_governors` / `is_governor` caller in
      `truesight_autopilot` (`auth.py`, `vault_routes.py`, `policy.py`, `daily_briefing.py`,
      `main.py`, `telegram_adapter.py`) as **point-lookup** (migrate to `resolve_key`) vs
      **enumeration** (stays on the monolith). Record the matrix in this doc.
- [ ] **PAT scope.** Confirm `CONTRIBUTORS_CACHE_GITHUB_PAT` (GAS script property) has
      `contents:write` sufficient for the Git Trees API on `treasury-cache` (it already
      commits `dao_members.json`, so almost certainly yes).
- [ ] **Reader PAT.** Confirm the autopilot has a GitHub token available for authenticated
      contents-API reads (raise the rate limit); decide the env var.
- [ ] **Privacy decision.** Include `email` in per-key files? Default: **no**.
- [ ] **Freshness API decision.** Confirm contents-API for the sign-in lookup, raw for the
      warm-cache path. (Default in §2.4.)
- [ ] **Beta surface.** Confirm a beta autopilot exists to point at `treasury-cache`
      (or a test branch) for UAT — see `AUTOPILOT_TELEGRAM_BETA_DEPLOY_PLAN.md` /
      `BETA_SANDBOX_ENDPOINT_PLAN.md`. Never UAT key-grant logic on prod.

---

## 4. Sequenced plan (open PRs; human merges `truesight_autopilot`)

### PR1 — Generator emits per-key files (additive) · `tokenomics` GAS + `treasury-cache`
| Step | Description |
|------|-------------|
| 1 | In `dao_members_cache_publisher.gs`, after building the contributors array, compute `sha256` per ACTIVE key and assemble `public_keys/<sha256>.json` blobs. |
| 2 | Write them **in one commit** via the Git Trees API, alongside the existing `dao_members.json` write. Also write `public_keys/_manifest.json`. |
| 3 | No reader change. `dao_members.json` untouched in shape. Purely produce the new surface. |
| 4 | Smoke: run `publishDaoMembersCacheNow()`; confirm `public_keys/` populated + one commit. |

### PR2 — Incremental write (diff-based) · `tokenomics` GAS
| Step | Description |
|------|-------------|
| 1 | Diff current keys against `_manifest.json`; only create blobs for changed/added keys. |
| 2 | Keys no longer ACTIVE → write `status:"REVOKED"` (or tree-delete) and drop from manifest. |
| 3 | Confirm an unchanged run produces a no-op / near-empty tree update (eyeball exec time). |

### PR3 — Reader point-lookup · `truesight_autopilot/app/governor_registry.py`
| Step | Description |
|------|-------------|
| 1 | Add `resolve_key(public_key) -> identity | None`: hash → per-key cache → contents-API fetch (raw fallback) → validate ACTIVE + roles. |
| 2 | Authenticated GitHub reads (PAT) for the contents API. Short (≈60 s) per-key in-memory cache. |
| 3 | Keep `load_governors()` as enumeration + fallback (no behaviour change for existing callers). |
| 4 | Unit tests: hit/miss/revoked/404-then-found, cache hit, monolith fallback when per-key absent. |

### PR4 — Vault auth uses point-lookup + force-fresh-on-deny · `truesight_autopilot/app/vault_routes.py`
> ⚠️ **Collision hold:** `vault_routes.py` is under active edit by another session
> (`track_registry`). Land PR4 only when that work is merged. Until then, the **interim
> mitigation** is lowering `GOVERNORS_CACHE_TTL` on the box.

| Step | Description |
|------|-------------|
| 1 | `_resolve_identity_from_jwt` / `verify-signature` resolve via `resolve_key`. |
| 2 | On a governor miss **during sign-in**, do ONE fresh contents-API lookup before denying → retires the 5-min lag bug. |
| 3 | Tests: a key absent from the warm cache but present on GitHub is granted on first attempt. |

### PR5 — (Later) Other consumers + DApp · `truesight_autopilot`, `dapp`/`tokenomics permissions.js`
| Step | Description |
|------|-------------|
| 1 | Migrate point-lookup consumers from the audit (PR-pre-flight) to `resolve_key`. |
| 2 | DApp `permissions.js` resolves signed-in RSA via the per-key file instead of the monolith. |
| 3 | Keep a slim `governors_index.json` if any UI needs cheap enumeration; only then consider retiring monolith point-use. |

---

## 5. Resume tracker

> **RESUME HERE:** PR1 — generator emits `public_keys/<sha256>.json` (additive). Open PRs;
> human-merge `truesight_autopilot`. Report the DAO contribution after each unit before the next.
> **One PR per turn:** do PR1 and STOP; the next turn picks up PR2. Never run multiple PRs in a
> single turn (`OPERATING_INSTRUCTIONS.md §5a`).

| Unit | PR opened | Merged | Deployed | Contribution reported | UAT |
|------|-----------|--------|----------|-----------------------|-----|
| PR1 — generator emits per-key files | ☐ | ☐ | ☐ | ☐ | U1 |
| PR2 — incremental / revocation | ☐ | ☐ | ☐ | ☐ | U3, U5 |
| PR3 — reader `resolve_key` | ☐ | ☐ | ☐ | ☐ | (automated) |
| PR4 — vault auth + force-fresh-on-deny | ☐ | ☐ | ☐ | ☐ | U2 |
| PR5 — other consumers + DApp | ☐ | ☐ | ☐ | ☐ | U4 |

---

## 6. UAT (human-tested, on **beta** — never prod, never real money)

Run against a **beta autopilot** pointed at `treasury-cache` (or a test branch). The
`public_keys/` folder is additive, so producing it on prod `treasury-cache` is safe; the
grant-logic UAT (U2/U3) must use the **beta vault**, not prod.

- **U1 — per-key file exists & correct.**
  Surface: `https://raw.githubusercontent.com/TrueSightDAO/treasury-cache/main/public_keys/<sha256-of-a-known-governor-key>.json`.
  Expect: JSON with the right `contributor`, `roles` incl. `governor`, `status:"ACTIVE"`.
  Acceptance: fields match `dao_members.json` for that key. ✅/❌

- **U2 — new key recognised immediately (the bug).**
  Interaction: register a **new** device key on beta, then **immediately** sign in at the
  beta `/vault/login` with it.
  Expect: governor vault UI loads on the **first** attempt — no 5-min wait, no worker restart.
  Acceptance: access granted < ~10 s after registration. ✅/❌

- **U3 — revoked key denied.**
  Interaction: revoke a test key; re-run the publisher; attempt beta vault sign-in with it.
  Expect: per-key file shows `status:"REVOKED"` (or gone); vault denies with the
  contribution-nudge page. Acceptance: denied. ✅/❌

- **U4 — enumeration intact.**
  Surface: any "list governors" path (e.g. daily briefing, DApp governor gating).
  Expect: full governor set still resolves (monolith path unchanged).
  Acceptance: no regression vs pre-change. ✅/❌

- **U5 — generation no longer grows with unchanged keys.**
  Surface: Apps Script execution log for `publishDaoMembersCacheNow()` run twice with no
  key changes between runs.
  Expect: 2nd run is a near no-op (diff-empty tree); exec time flat, not scaling with total key count.
  Acceptance: 2nd-run commit touches only changed files. ✅/❌

**Completion gate:** PR1–PR4 merged + deployed; U1–U5 pass; contributions reported per unit.

---

## 7. Rollout

Additive-first: PR1/PR2 produce `public_keys/` with zero reader dependency, so they can ship
and bake before any reader flips. PR3 adds the reader behind `resolve_key` (unused in prod
until PR4). PR4 (held for the `vault_routes.py` collision) flips the vault to the fast path
and kills the cache-lag bug. Deploy `truesight_autopilot` via the targeted path
(`git reset --hard origin/main`, **no `git clean`**) + restart `truesight-vault`.

## 8. Dependency notes / open questions

- **Generator authority:** all key data originates from the `Contributors Digital
  Signatures` / `Governors` / `Contributors contact information` sheets via the GAS
  publisher — the per-key files are a *projection*, never a second source of truth.
- **Interim mitigation** for the live cache-lag (until PR4): lower `GOVERNORS_CACHE_TTL`
  on the box, or restart `truesight-vault` after a key registration.
- **Open:** authenticated-read PAT for the autopilot contents-API calls — reuse `GITHUB_PAT`
  or a read-scoped token? (pre-flight).
- **Cross-refs:** `reference_security_dashboard_pipeline` (treasury-cache compile),
  `DAPP_PERMISSION_CHANGE_FLOW.md` (permissions.json sibling surface),
  `EDGAR_DAO_EXTRACTION_PLAN.md` (roadmap reference example).
