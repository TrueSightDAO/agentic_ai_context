# Members page — reliability + single-source consolidation

**Goal.** `truesight.me/members.html` shows stale governor/member records because it
depends on two independently-built caches that drift:

- **`lineage-credentials/_cache/index.json`** (rich CV schema) — feeds **Governors + regular
  members**. Built by `lineage-engine/scripts/build_cv_cache.py` via `build-cv-cache.yml`
  (6h cron that GitHub **drops** + push + manual). This is the stale one.
- **`treasury-cache/dao_members.json`** (thin schema) — feeds **only the Sentinel section**.
  Built by GAS `dao_members_cache_publisher.gs`; refreshed reliably (every
  `[EMAIL VERIFICATION EVENT]` via Perch Sidekiq worker + daily safety-net trigger).

Two fixes:
1. **Reliability** — stop `index.json` going stale (cron drops).
2. **Consolidation** — make `index.json` the single source for all three sections
   (Governors, Members, Sentinels) so the page references one file and readers aren't confused.

---

## Pre-flight (captured — no execution unit needs a live cross-repo read)

**Repos / remotes (all TrueSightDAO, git pre-authorized under ~/Applications):**
- `lineage-credentials` → data repo (holds `_cache/index.json`); build workflow lives here.
- `lineage-engine` → code repo; `scripts/build_cv_cache.py` builds the index.
- `treasury-cache` → holds `dao_members.json`; has `.github/workflows/` already.
- `truesight_me` local clone = **`truesight_me_beta`** (beta). Prod = `truesight_me_prod`
  (human promotes via `gh repo sync`). members.html edit lands in beta.

**`index.json` build (build_cv_cache.py) — current member entry shape (~line 845):**
```py
members.append({
    'slug': slug, 'display_name': cv['display_name'], 'pk_hash': cv.get('pk_hash'),
    'is_governor': bool(gov.get('is_governor')),
    'voting_rights': _coerce_voting_pct(gov.get('total_voting_power_pct') or gov.get('voting_power_pct')),
    'primary_program': primary_program, 'programs': program_slugs,
    'has_dao_contributions': cv.get('has_dao_contributions', False),
    'has_elective_records': cv.get('has_elective_records', False),
    'total_tdg_controlled': dc_summary.get('total_tdg_issued') or 0,
    'total_contributions': dc_summary.get('total_contributions') or 0,
    'last_updated': cv['generated_at'],
})
# ... then: write_json(data_root/'_cache'/'index.json', {'generated_at': now_utc_iso(), 'count': len(members), 'members': members})
```
- Helpers available: `_coerce_voting_pct(raw)->float` (line 334), `now_utc_iso()` (line 237).
- Imports present: argparse, json, os, re, sys, unicodedata, datetime, pathlib, typing.
  **No HTTP lib** — PR3 adds `import urllib.request`.
- Governor/voting source: `fetch_contributions.py` reads Main Ledger `Governors` tab +
  `Contributors voting weight`. **No sentinel concept in lineage-engine today.**

**`dao_members.json` schema (public, no auth): `contributors[]` =**
`{ name, email, roles[], voting_rights (RAW TDG count, e.g. 1199.99), total_voting_power_pct (string %), public_keys[] }`
- Sentinel = `roles` contains `"sentinel"` (source: col W `Is Sentinel`=TRUE on
  `Contributors contact information`). The 6 sentinels (`Claude Anthropic`, `Deep Seek`,
  `Kimi Moon`, `Open Ai`, `Sophia Truesight`, `truesight-autopilot`) have **no CV** in
  lineage-credentials → they must be appended as synthetic index entries.
- **Semantic trap:** in `index.json`, `voting_rights` = **percentage**; in `dao_members.json`,
  `voting_rights` = **raw TDG count**, and the % lives in `total_voting_power_pct`. Map carefully.

**`members.html` (truesight_me_beta) — current wiring:**
- `DAO_MEMBERS_URL` const (line 255) — remove in PR4.
- `memberCardHtml(m)` (263) — clickable `<a href="credentials/#<slug>">`; reads display_name,
  primary_program, voting_rights (as %), total_tdg_controlled, total_contributions, is_governor,
  has_elective_records.
- `sortMembers(members)` (299) — splits governors vs regulars by `is_governor`.
- `sentinelCardHtml(m)` (315) — non-clickable div; reads `m.voting_rights` as raw TDG for "X TDG".
- `loadSentinels()` (330) — fetches `DAO_MEMBERS_URL`, filters `roles.includes('sentinel')`.
- `loadMembers()` (350) — fetches `INDEX_URL`, renders governors+regulars, calls loadSentinels.
- Both fetches already cache-busted (`?_=Date.now()`, `cache:'no-store'`).

**Cross-poke (PR2) requires an operator secret:** cross-repo `workflow_dispatch` needs a PAT
with `actions:write` on `lineage-credentials` (GITHUB_TOKEN is repo-scoped). Store as
`treasury-cache` secret `LINEAGE_DISPATCH_PAT`. This is the only operator step.

✅ **Pre-flight Completeness:** no execution unit requires reading a file/state not already
captured above.

---

## Sequenced plan (ONE PR per turn)

| Unit | Repo | Advance | PR opened | Merged | Deployed/Effective |
|------|------|---------|-----------|--------|--------------------|
| **PR1 — cron bump 6h→2h** | lineage-credentials | _(auto)_ | ☐ | ☐ | on merge |
| **PR2 — event-driven poke** | treasury-cache | `gate: needs LINEAGE_DISPATCH_PAT secret` | ☐ | ☐ | after secret added |
| **PR3 — emit sentinels + `is_sentinel` into index.json** | lineage-engine | _(auto)_ | ☐ | ☐ | after rebuild |
| **PR4 — members.html single-source + happy-dom test** | truesight_me_beta | `gate: beta→prod promotion (human)` | ☐ | ☐ | after human promote |

**Dependencies:** PR4 depends on PR3 merged **and** `index.json` rebuilt (so `is_sentinel` exists).
PR1/PR2 are reliability, independent of PR3/PR4.

### PR1 — lineage-credentials `.github/workflows/build-cv-cache.yml`
Change `- cron: '0 */6 * * *'` → `- cron: '0 */2 * * *'`. No-dependency staleness reduction
(6h → 2h window) that survives an occasional dropped scheduled run. Update the cron comment.

### PR2 — treasury-cache `.github/workflows/poke-lineage-cache.yml` (NEW)
`on: push: paths: ['dao_members.json']` → `gh workflow run build-cv-cache.yml --repo
TrueSightDAO/lineage-credentials` using `${{ secrets.LINEAGE_DISPATCH_PAT }}`. Ties the
index rebuild to the **reliable** dao_members heartbeat (push events aren't dropped like cron).
**Operator UAT:** add the `LINEAGE_DISPATCH_PAT` secret, then republish dao_members (verify a
build-cv-cache run fires within ~1 min).

### PR3 — lineage-engine `scripts/build_cv_cache.py`
- `import urllib.request`.
- After the `members[]` loop, fetch public `dao_members.json`; build `sentinel_names` set from
  `roles.includes('sentinel')`.
- Set `is_sentinel` on every existing member entry (`display_name in sentinel_names`).
- For sentinel names with no matching CV, append synthetic entries: `slug=None` (non-clickable),
  `display_name=name`, `is_governor=False`, `is_sentinel=True`, `roles=roles`,
  `voting_rights=_coerce_voting_pct(total_voting_power_pct)`,
  `total_tdg_controlled=<raw dao_members voting_rights>`, others null/0/[].
- Fetch failure = non-fatal warning (sentinels absent, same as pre-change).

### PR4 — truesight_me_beta `members.html` (+ test)
- Drop `DAO_MEMBERS_URL` + the `loadSentinels()` fetch.
- `loadMembers()` fetches `index.json` once, partitions into governors / sentinels
  (`is_sentinel`) / regulars.
- `sentinelCardHtml` reads `total_tdg_controlled` for "X TDG" (not raw `voting_rights`).
- `sortMembers` excludes sentinels from gov/regular grids.
- Add happy-dom test (§9 OPERATING_INSTRUCTIONS) covering the 3-way partition + non-clickable
  sentinel cards.
- Then **human promotes** beta→prod.

### UAT
Beta staging `members.html` (truesight_me_beta Pages / local `python3 -m http.server`):
open page → **expect** Governors, Members, and Sentinels all populated from a single
`index.json` fetch (Network tab shows no `dao_members.json` request); sentinel cards show
"Sentinel" badge + TDG and are non-clickable; governor/member cards still deep-link to CVs.
Acceptance: all three sections render, one JSON source, no console errors.

---

## RESUME HERE → **PR1** (lineage-credentials cron bump)

Contribution reporting: after each unit merges, file the DAO contribution before the next
(`DAO_CLIENT_AI_AGENT_CONTRIBUTIONS.md`), signed "Claude Anthropic".
