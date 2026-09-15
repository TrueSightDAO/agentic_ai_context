# CRF Anapu × SunMint — tree-submission cohort proposal & execution roadmap

**Filed:** 2026-09-15, by Claude Anthropic (Envoy), at Gary's request, for review and rectification —
not yet executed. **Status: proposal, awaiting governor correction.**

---

## 0. The misunderstanding, stated plainly

Gary (2026-09-15): *"There was a misunderstanding of the requirements for `https://cfr.truesight.me/`.
It is supposed to be a stand-alone somewhat mirror of `sunmint.truesight.me` — but all submissions
via that route can be traced back to `https://cfr.truesight.me/` — and that way when a visitor clicks
[View cohort] on the CRF Anapu program page and goes to `members.html`, we could view a list of all
the members who ever submitted a tree registration, a tree monitoring event, or a plot via
`https://cfr.truesight.me/`."*

**What was actually built (2026-09-11, this session's prior work on `CRF_ANAPU_MEDIA_TASK_PLAN.md`):**
`cfr.truesight.me` is a **static mirror of the DAO-credentialing program pages**
(`index.html` / `members.html` / `credentials/index.html`) — the same machinery that already serves
Butterfly Effect and Ivy Yoga. Its `members.html` lists **students who received a DAO credential**,
sourced from `lineage-credentials/_cache/index.json` filtered by `primary_program`. It has **no
connection whatsoever to SunMint tree submissions** — a farmer/student visiting `cfr.truesight.me`
today cannot plant a tree, log a monitoring visit, or register a plot there at all; those flows only
exist at `sunmint.truesight.me` / the `sunmint_beta` app, with no way to tag a submission as
CRF-Anapu-originated.

**My reading of what's actually wanted** (stated explicitly so it can be corrected, same convention as
the governor-decisions table in `handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md`):

| # | What I understand | Confidence |
|---|---|---|
| 1 | `cfr.truesight.me` should let a CRF Anapu student/farmer actually **submit** a tree planting, a tree growth monitoring event, and/or a plot boundary — the same three actions `sunmint.truesight.me` supports today — not just display static program copy. | High — directly stated |
| 2 | Every such submission must be **attributable back to `cfr.truesight.me`** as its origin, durably, so it can be counted later. | High — directly stated |
| 3 | `programs/crf-anapu/members.html` (**"View cohort"** from the program landing page) should list **everyone who has ever submitted via that route** — not (only) people who hold a DAO credential. | High — directly stated, this is the concrete deliverable |
| 4 | This is a **pattern**, not a one-off — CRF Anapu is the first case, but any future partner program that gets its own subdomain should get the same "submissions via our subdomain count toward our cohort" behavior. | Medium — inferred from "this way," treat as a design goal, confirm explicitly |
| 5 | The existing DAO-credential side of CRF Anapu (co_brand chrome, `manifest.json`, the "Credential + trees" hybrid described in its own `description_md` — see §1.3) is **not being thrown away** — it stays, and the tree-submission cohort is additive to it, not a replacement. | Medium — the manifest's own copy already describes a hybrid; treat as correct unless told otherwise |

> **If any row above is wrong, say so before PR1 starts** — this doc is written so the whole design
> can be corrected in one pass rather than discovered wrong mid-build (§5e of
> `OPERATING_INSTRUCTIONS.md`).

---

## 1. Current-state architecture audit (read directly from the live repos, 2026-09-15)

### 1.1 `cfr.truesight.me` today

Repo `TrueSightDAO/cfr-anapu` (GitHub Pages, `gh-pages` branch, Route53 CNAME). Contents:
`CNAME`, `index.html`, `members.html`, `credentials/index.html`, `manifest.json`, `media.json`,
vendored `styles/main.css` + `js/{nav,footer,program-shell,media-gallery}.js`. This is a **byte-level
vendored copy** of `truesight_me_beta/programs/crf-anapu/*`, with root-relative asset refs rewritten
to absolute `https://truesight.me/...` URLs (per `CRF_ANAPU_MEDIA_TASK_PLAN.md` §7). It is entirely
the **credentialing-program surface** (§1.2 below) — no tree-submission capability exists on this
domain today.

### 1.2 The credentialing-program pattern (`CREDENTIALING_PROGRAM_PAGES.md`, `js/program-shell.js`)

- `truesight_me/programs/<slug>/{index.html, manifest.json, members.html, credentials/index.html}` —
  shared rendering shell (`js/program-shell.js`), driven entirely by `manifest.json` metadata.
- `members.html` fetches `lineage-credentials/_cache/index.json` and filters by
  `manifest.membership_filter.primary_program`. **Confirmed live**: `butterfly-effect` currently has
  **83 real members** in that index (checked 2026-09-15) — the pipeline genuinely works, it's just
  answering a different question ("who got a credential") than the one Gary is now asking ("who
  submitted a tree via our URL").
- `manifest.json` already has a `program_mode` field — currently only one value is in use anywhere
  (`"cohort_credentialing"`, on Butterfly Effect / Ivy Yoga / CRF Anapu; other programs leave it
  unset, defaulting to the same rendering). **No other `program_mode` exists yet** — introducing a
  SunMint-derived cohort is the first time this field's branching would actually matter.
- **CRF Anapu's own `manifest.json` already describes the target hybrid**, unprompted, from the
  original 2026-09-11 build: *"This is a 'Credential + trees' partner (route B of the DAO's Lineage
  credentialing platform): each attested student receives a verifiable credential, and a serialized
  tree-planting pledge is bound to that student — the tree's QR code and the student's credential
  page point at each other, and the public Impact Map carries passive proof of each planted tree."*
  The copy was written correctly; the plumbing behind it was never built. That's the actual gap.
- §16.10/§17.12 of the spec explicitly **defers** "cohort dashboards for partners" and "show me
  everyone we've certified" as a distinct `programs/<p>/cohort.html` surface — meaning a
  submission-derived cohort was a known, named, *un-scoped* gap in the original design, not an
  oversight this proposal is inventing.

### 1.3 SunMint's existing origin-tracking — the load-bearing fact for this whole proposal

`sunmint_beta/index.html` (tree planting registration) and
`sunmint_beta/monitor-tree-growth/index.html` (growth monitoring) **already embed the submitting
page's URL in every signed event body**:

```js
// sunmint_beta/index.html:889
const requestText = `[TREE PLANTING EVENT]\n${locationLine}- Species: ${species}\n- Planting Time: ${plantingTime}\n- Photo URL: ${photoDestinationURL}\n- Submission Source: ${window.location.href}\n--------`;

// sunmint_beta/monitor-tree-growth/index.html:1103
const requestText = `[TREE GROWTH MONITORING EVENT]\n- Tree ID: ${treeId}\n...\n- Submission Source: ${window.location.href}\n--------`;
```

`Submission Source` is a pre-existing, general convention across this workspace (also seen on
`[EMAIL VERIFICATION EVENT]` and a `[DAO Inventory Expense Event]` GAS regex parser at
`tokenomics/google_app_scripts/19Wag9x.../Code.js:539`) — **not something this proposal invents.**
This is the single most important finding: **if `cfr.truesight.me` serves the exact same tree-planting
and monitoring pages, every submission automatically self-tags with
`Submission Source: https://cfr.truesight.me/...` — zero app-code change required for those two event
types.** The origin tracking Gary asked for already exists; what's missing is (a) a way to actually
reach those forms from `cfr.truesight.me`, and (b) a pipeline that turns that field into a members.html
roster.

**The third event type — plot/boundary — is NOT confirmed shipped in the farmer-facing app.**
`SUNMINT_BOUNDARY_SUBMISSION_PLAN.md` records the event as **`FARM BOUNDARY EVIDENCE EVENT`** and its
own manifest row claims "complete — UAT passed 2026-09-01," but a direct grep of `sunmint_beta/`'s two
live pages for `FARM BOUNDARY` / `Limites da Fazenda` (the module's Portuguese name in that plan)
**turns up nothing** — it isn't in either shipped page. This needs a live pre-flight check (§6) before
PR1 — either the module shipped somewhere I haven't found (a `dapp` report page, most likely, given
that repo hosts most one-off signed-event forms), or the plan's "complete" status is itself stale in
the same way the merge-verification incident from earlier today showed self-reported completion can't
be trusted without a direct check.

### 1.4 The `lineage-credentials` data model — the mechanism to reuse, not reinvent

`lineage-engine/scripts/build_cv_cache.py::collect_practitioners()` walks
`lineage-credentials/programs/<program-slug>/pk-<hash>/{identity.json, practice/*.json}` — one
directory per program, per contributor (identified by RSA-public-key hash, the same identity primitive
used everywhere else in this DAO). For each `pk-<hash>`, it aggregates the `practice/*.json` event
files into `practice_count` / `total_practice_minutes`, and `primary_program` is computed by
`_program_activity_score` — whichever program has the most practice activity for that pk-hash wins.
This is **entirely capoeira-shaped today**: the folder is literally named `practice`, and the
aggregation fields (`total_practice_minutes`) are capoeira-specific. A `program_assets/registry.json`
already handles data-slug ↔ URL-slug divergence (e.g. data-side `capoeira-tribo-mirim` vs URL-side
`tribomirim`) — the exact mechanism a `crf-anapu` (URL) ↔ some SunMint-side identifier (data) mapping
would reuse if the two ever diverge.

**This is the integration point.** Making SunMint submissions "count" toward `members.html` does not
require inventing a new membership system — it requires teaching this *existing* pipeline about a
second kind of activity (tree submissions) alongside practice sessions, and writing a small sync job
that turns `Submission Source`-tagged SunMint events into files this pipeline already knows how to
read (with a new, non-`practice`, appropriately-named subfolder — see §3).

---

## 2. Target architecture

### 2.1 `cfr.truesight.me`'s tree-submission surface — two options

**Option A — thin branded redirect into the canonical app (recommended).**
`cfr.truesight.me`'s planting/monitoring pages are small static pages that immediately
`window.location.replace('https://sunmint.truesight.me/?program=crf-anapu')` (and the equivalent for
`monitor-tree-growth/`). The **one real app code change**: `sunmint_beta` reads an optional
`?program=<slug>` query param and (a) appends it into the signed event body as its own field (see §3.1)
and (b) — reusing the `cobrand-strip` component + `manifest.json::co_brand` fields already built for
the credentialing pages — renders a "CRF Anapu × CEPOTX" banner at the top of the canonical app when
the param is present, so the *visual* experience still reads as "this is CRF Anapu's tree-planting
tool" even though the URL bar shows `sunmint.truesight.me`.
- **Pro:** one canonical app, zero duplication, zero drift risk — a bug fix or new feature in
  `sunmint_beta` is instantly live for every partner subdomain.
- **Con:** the browser URL bar changes after the redirect; a user who bookmarks mid-flow bookmarks
  `sunmint.truesight.me`, not `cfr.truesight.me`.

**Option B — vendor a full copy into the `cfr-anapu` repo**, exactly like the credentialing pages
were vendored (§1.1), with `window.location.href` naturally differing per domain and needing zero app
change for `Submission Source` — but every future `sunmint_beta` change now needs a second, manual
sync into `cfr-anapu` (and any other future partner subdomain), or a sync script needs to be built and
maintained to do it automatically.
- **Pro:** URL bar stays `cfr.truesight.me` throughout; feels fully "their own app."
- **Con:** genuine, compounding maintenance burden — exactly the kind of duplication this workspace's
  conventions elsewhere (`AUTOPILOT_CHANNEL_INTEGRATIONS.md`'s adapter-pattern, the single-canonical-app
  principle behind `truesight_autopilot`) steer away from.

**Recommendation: Option A.** It is less code, has no drift risk, and reuses the co-brand pattern that
already exists for exactly this purpose. This is one of the decisions batched in §6 for governor
confirmation before PR1 — pick one, once, rather than discover a preference mid-build.

### 2.2 Membership derivation — extend the existing pipeline, don't fork it

1. **A domain → program-slug registry.** A small addition (new file or a field on each program's
   `manifest.json`, e.g. `"sunmint_origin_program_slug": "crf-anapu"`) mapping the `?program=` value
   (or, for Option B, the submission's URL host) to the program directory. Mirrors the existing
   `program_assets/registry.json` divergence-handling pattern (§1.4).
2. **A sync job** (new script, `lineage-engine/scripts/sync_sunmint_program_activity.py` or similar)
   that:
   - Reads SunMint tree/monitoring/boundary events — **preferred source: `verify_public_signatures`**
     (the public, per-event-type immutable JSON attestation ledger — already structured, already
     public, no new credentials needed, no PII-exclusion risk since tree events aren't in that repo's
     `excluded_pii_events` bucket the way email-bearing events are). Needs a pre-flight read of that
     repo's actual `tree_*` bucket schema (§6) before this script can be written correctly.
   - Filters for events carrying the new `Program` field (Option A) or a `Submission Source` host
     matching a registered program domain (Option B).
   - Resolves the submitter's `pk-hash` (same public-key-hash primitive `lineage-credentials` already
     uses everywhere).
   - Writes one JSON file per event under `lineage-credentials/programs/<slug>/pk-<hash>/sunmint/*.json`
     — a **new, non-`practice`** subfolder name, so capoeira's `practice_count`/`total_practice_minutes`
     semantics are never accidentally polluted by tree data (see §1.4 — reusing the literal `practice/`
     folder for tree events would render nonsensical CV text like "Total practice time: 0 minutes" on
     a farmer's page).
   - Idempotent, content-addressed (same sha-aware skip pattern already used by
     `sync_sunmint_signatures.py` for `verify_public_signatures` itself).
3. **Extend `collect_practitioners()`** in `build_cv_cache.py` to also read the new `sunmint/` subfolder
   per pk-hash-per-program, aggregating into program-appropriate fields: `trees_planted_count`,
   `monitoring_events_count`, `plots_registered_count`, `last_sunmint_activity_at` — instead of (or
   alongside) `practice_count`/`total_practice_minutes`.
4. **Extend `_program_activity_score`** so a pk-hash with SunMint activity but zero practice/credential
   activity still resolves `primary_program` correctly and appears in `_cache/index.json` at all —
   today a pk-hash with no practice events for any program doesn't get a `primary_program`, which would
   silently exclude a tree-only contributor from ever showing up.
5. **`manifest.json` gains a second `program_mode` value** (e.g. `"sunmint_cohort"`, or a
   non-exclusive `program_modes: ["cohort_credentialing", "sunmint_cohort"]` array per Open Decision #4
   in §6) so `program-shell.js` knows to render SunMint activity badges (🌳 trees planted, 📍 plot
   registered, 🌱 last monitored) on `members.html` cards, alongside or instead of the existing
   governor/practitioner badges.

### 2.3 What does NOT change

- The credentialing side (DAO credentials, `credentials/index.html`, QR/PDF generation, the whole of
  `CREDENTIALING_PROGRAM_PAGES.md` §§1–17) is untouched — this proposal is additive.
- `sunmint.truesight.me` / `sunmint_beta`'s existing behavior for a visitor with **no** `?program=`
  param is byte-identical to today — the co-brand banner only renders when the param is present.
- The canonical `truesight.me/sunmint.html` public Impact Map is unaffected by this proposal (it
  already reads plots/trees from the existing public sources); a follow-on (not in this proposal's
  scope) could surface "planted via CRF Anapu" as a filter there, matching the manifest's own promise
  that "the public Impact Map carries passive proof of each planted tree."

---

## 3. Concrete schema additions

### 3.1 SunMint event body — new field (Option A only)

```
[TREE PLANTING EVENT]
- Location: ...
- Species: ...
- Planting Time: ...
- Photo URL: ...
- Program: crf-anapu          ← NEW, only present when ?program= was set
- Submission Source: https://sunmint.truesight.me/?program=crf-anapu   ← unchanged mechanism, now also carries the param
--------
```

Adding a dedicated `Program` field (rather than relying solely on parsing the query string back out of
`Submission Source`) keeps the sync job (§2.2.2) simple and matches this workspace's existing
convention of explicit named fields over positional parsing. `Submission Source` stays as-is for
audit/debugging; `Program` is the field the sync job actually filters on.

### 3.2 `lineage-credentials/programs/crf-anapu/pk-<hash>/sunmint/<event-id>.json`

```json
{
  "event_type": "TREE PLANTING EVENT",
  "message_id": "<dao ledger message id>",
  "captured_at": "2026-09-15T00:00:00Z",
  "payload": {
    "species": "...",
    "location": {"lat": -3.389, "lon": -51.300},
    "tree_id": "<if assigned>"
  },
  "_source": "verify_public_signatures/tree_planting_event/<sha>.json"
}
```

Mirrors the existing `practice/*.json` shape (`payload` sub-object, `_path`/`_source` provenance) so
`build_cv_cache.py`'s existing read/aggregate machinery needs the smallest possible extension.

---

## 4. Privacy — reuse the existing minors convention, don't invent a new one

`CREDENTIALING_PROGRAM_PAGES.md` §9 already establishes: certificate recipients are opt-in by the act
of being issued a cert; `public_listable` gates a minor's listing; `credential_visibility_default` on
the manifest is the programme-wide hint. CRF Anapu's manifest already sets
`"credential_visibility_default": "private"` for exactly this reason (CEPOTX students are minors).

**This proposal must inherit that posture for the SunMint side, not create a looser one.** A tree
submission is tied to GPS coordinates and (often) a planting photo with EXIF — arguably *more*
sensitive than a bare name-on-a-cohort-list. Recommendation: `members.html`'s SunMint activity badges
show **aggregate counts only** (🌳 3 trees · 📍 1 plot · last active 2026-09-10) next to whatever name
display the existing `public_listable` gate already allows — never expose raw GPS or the planting
photo on the public cohort page regardless of visibility setting. This needs explicit governor
confirmation (§6) since it's a genuine privacy-scope decision, not purely technical.

---

## 5. Comparison worked example — Butterfly Effect vs. the proposed CRF Anapu shape

| | Butterfly Effect (today, unchanged) | CRF Anapu (proposed) |
|---|---|---|
| `program_mode` | `cohort_credentialing` | `cohort_credentialing` **+** `sunmint_cohort` |
| Membership source | `lineage-credentials/_cache/index.json` filtered by `primary_program` | same index, **plus** pk-hashes that only have `sunmint/` activity and no credential |
| What earns a listing | ERA issues a certificate | Student/farmer submits ≥1 tree/monitoring/plot event via `cfr.truesight.me` (or gets a credential — either counts) |
| Card badges | governor / practitioner | 🌳 trees · 📍 plots · 🌱 last monitored (new), governor/practitioner badges unaffected if also credentialed |
| Live member count (checked 2026-09-15) | 83 | 0 (this proposal is what would start populating it) |

---

## 6. Open decisions — batch these once (§5e), don't re-ask per PR

1. **Option A (redirect + co-brand banner) vs. Option B (vendored copy)** for `cfr.truesight.me`'s
   planting/monitoring pages — §2.1. **Recommend A.**
2. **Is a tree-submission-only contributor (no credential) allowed to appear on `members.html` at
   all**, or does CRF Anapu want cohort membership to still require the credential, with SunMint
   activity shown only as an enrichment on top of an existing credentialed member's card? Re-read
   requirement #3 in §0 as "yes, submission alone is sufficient" — confirm.
2b. **If yes to #2** — should a tree/plot submitted through `sunmint.truesight.me` directly (no
   `?program=` param — the generic, unbranded surface) ever retroactively count toward a program's
   cohort if the submitter later turns out to be a CRF Anapu student? Recommend **no** — origin
   attribution should be at submission time only, exactly as literally requested ("submissions via
   that route"), not inferred after the fact from identity.
3. **Privacy scope** (§4) — aggregate counts only on the public cohort card, never raw GPS/photo.
   Confirm this matches CEPOTX's actual consent posture; may need CEPOTX/Jedielcio input, not just
   Gary's.
4. **`program_mode` as a single value vs. an array** (§2.2 point 5) — a single new value
   (`"sunmint_cohort"`, replacing `"cohort_credentialing"` for CRF Anapu) is simpler to ship first; an
   array (`program_modes: [...]`) is the more correct long-term shape if a program can be *both* at
   once (which CRF Anapu explicitly is, per its own `description_md`). Recommend building the array
   shape from the start since we already know we need it, rather than shipping the single-value
   version and having to migrate every consumer later.
5. **Which repo hosts the sync job** — `lineage-engine` (co-located with `build_cv_cache.py`, the
   natural home) vs. `truesight_autopilot` (Sophia already runs scheduled sync scripts like
   `sync_sunmint_signatures.py` there). Recommend `lineage-engine`, triggered the same way
   `capoeira.agroverse.shop/practice.html`'s existing sync already is (§1.4), for architectural
   consistency — but confirm since I haven't located that trigger's exact mechanism (cron vs. webhook)
   in this research pass; PR0 below resolves it.

---

## 7. Pre-flight — verify before PR1 (§5d completeness gate)

These are things this proposal **could not verify from static reading alone** and that PR1 must not
have to discover mid-turn:

1. **`FARM BOUNDARY EVIDENCE EVENT`'s actual shipped location** (§1.3) — confirmed as a catalog entry
   and claimed "UAT passed" in `SUNMINT_BOUNDARY_SUBMISSION_PLAN.md`, but not found in either live
   `sunmint_beta` page. Find it (likely a `dapp` report page) or confirm it was never actually shipped
   to a farmer-facing surface, and whether it already carries `Submission Source`.
2. **`verify_public_signatures`'s actual `tree_*` bucket schema** — this proposal assumes it's the
   right read source for the sync job (§2.2.2) based on `PROJECT_INDEX.md`'s description alone; the
   repo isn't cloned in this workspace and wasn't read directly this session. Confirm bucket names,
   per-file schema, and whether `Submission Source` / a future `Program` field survives into the
   attestation JSON (vs. being stripped during ingestion).
3. **The capoeira practice-event sync trigger mechanism** (§1.4, §6 open decision #5) — confirm
   whether it's a cron, a webhook, or a manual script, so the new SunMint sync job's trigger can follow
   the same operational pattern rather than inventing a third one.
4. **`sunmint_beta`'s exact query-param reading convention**, if any already exists for something else
   in that app (to match existing style rather than introduce a new one for `?program=`).
5. **CEPOTX/Jedielcio's actual consent posture** (§4, open decision #3) — not a code question, a
   partnership question; needs a real conversation, not an assumption.

✅ **Pre-flight Completeness (partial):** items 1–4 above are code/repo reads any executing agent can
resolve directly, at low cost, as **PR0** below — captured here so PR1 doesn't have to discover them
mid-turn. Item 5 is a human/partnership question outside any PR's scope and is called out explicitly
rather than silently assumed.

---

## 8. Sequenced execution roadmap (one PR per turn — §5a)

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | Pre-flight completion: resolve §7 items 1–4 (live repo reads only); update this doc's open decisions (§6) with governor + CEPOTX answers where received. No code. | auto |
| **PR1** | `sunmint_beta`: read `?program=` query param; append `Program: <slug>` field to `[TREE PLANTING EVENT]` and `[TREE GROWTH MONITORING EVENT]` bodies when present; render the `cobrand-strip` banner (reusing existing CSS/JS from the credentialing pages) when `?program=` resolves to a known program via a small fetched/vendored `manifest.json`-equivalent. Unit tests: param present/absent, unknown program slug (banner omitted, field still appended — never block a submission over an unrecognized tag), field ordering doesn't break existing event-catalog parsing (`canonical_labels` audit). | auto |
| **PR2** | `cfr-anapu` repo: add the two thin redirect pages (`plant-a-tree/index.html`, `monitor-tree-growth/index.html`) pointing at `sunmint.truesight.me/?program=crf-anapu` (Option A) — or the vendored-copy equivalent if Open Decision #1 lands on Option B. Wire a CTA from the existing `programs/crf-anapu/index.html` (both beta and the `cfr-anapu` mirror) to the new surface. | auto (beta); prod mirror gated same as any `truesight_me_*` prod touch |
| **PR3** | `lineage-engine`: new `sync_sunmint_program_activity.py` reading the confirmed source (§7 item 2), writing `programs/<slug>/pk-<hash>/sunmint/*.json` into `lineage-credentials`. Dry-run flag default, per this workspace's standing convention for any new write script. | auto |
| **PR4** | `lineage-engine`: extend `collect_practitioners()` + `_program_activity_score()` in `build_cv_cache.py` for the new `sunmint/` activity kind (§2.2 points 3–4); extend `manifest.json` schema for `program_modes` array (§6 decision #4). | auto |
| **PR5** | `truesight_me_beta` (+ `cfr-anapu` mirror): `program-shell.js` renders SunMint activity badges on `members.html` cards per §2.2 point 5 and §4's aggregate-only privacy rule; update `programs/crf-anapu/manifest.json` to the new `program_modes` shape. | auto (beta); prod gated on UAT |
| **PR6** | First real sync run (dry-run then live) against real CRF Anapu submissions (needs at least one real submission to exist first — may require a CEPOTX/Jedielcio coordination step outside any PR). Verify `members.html` populates. | **`gate: human`** — first live write into `lineage-credentials` from a new activity kind |
| **PR7** | Docs: update `CREDENTIALING_PROGRAM_PAGES.md` with the new `sunmint_cohort` mode (it's the canonical spec, editable per its own convention — this is documentation of a shipped feature, not a forecast); update `handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md`'s status; UAT. | auto |

**RESUME HERE → PR0** (once this proposal is confirmed/corrected by Gary — see Rollout below; do not
start PR0 before that confirmation per the governor-decisions convention this doc follows).

---

## 9. UAT

- **U1** — Submit a real (or clearly test-tagged, per §5g standing E2E authorization) tree planting via
  the new `cfr.truesight.me` surface. Confirm the ledger event carries `Program: crf-anapu`.
- **U2** — Confirm the sync job (PR3) picks up that event and writes the expected
  `lineage-credentials/programs/crf-anapu/pk-<hash>/sunmint/*.json` file.
- **U3** — Confirm `build_cv_cache.py` (PR4) correctly aggregates it and the pk-hash appears (or is
  updated) in `_cache/index.json` with `primary_program`/`programs[]` including `crf-anapu`.
- **U4** — Load `https://beta.truesight.me/programs/crf-anapu/members.html` (then, after prod
  promotion, `https://cfr.truesight.me/members.html` and `https://truesight.me/programs/crf-anapu/members.html`)
  and confirm the submitter's card shows the correct activity badge, with no raw GPS/photo exposed.
- **U5** — Confirm a submission with **no** `?program=` param (plain `sunmint.truesight.me`) is
  completely unaffected — no `Program` field, no banner, no change to existing behavior.
- **U6** — Confirm test data cleanup per §5g (test rows removed / clearly marked, no leftover value in
  a real ledger).

---

## 10. Rollout

**Not started.** Per Gary's instruction, this proposal is being sent to a new Telegram topic —
**"CFR partnership - figure out how to present"** — for review and correction before any PR begins.
RESUME HERE (§8) stays at PR0 until that review lands and this doc's §0/§6 open items are resolved.
