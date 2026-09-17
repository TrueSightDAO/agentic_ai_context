# CRF Anapu × SunMint — tree-submission cohort proposal & execution roadmap

**Filed:** 2026-09-15, by Claude Anthropic (Envoy), at Gary's request, for review and rectification.
**Status: ✅ APPROVED 2026-09-15 · ARCHITECTURE DECIDED = OPTION B (vendored copy)** · **PR0 + PR0b + PR1 + PR2 + PR3 COMPLETE** — all §6 open decisions resolved; §7 pre-flight complete; §2.1 re-pointed to Option B per Gary (2026-09-15, thread 30026). PR1 (vendor-readiness) shipped `sunmint_beta` #84 (2026-09-16, sha 3732e2a4). PR2 (vendor into `cfr-anapu` `gh-pages`) shipped `cfr-anapu` #5 (2026-09-17, sha f0ffdbda) and is **live on `cfr.truesight.me`** (5-path smoke-check green). PR3 (the SunMint program-activity sync job) shipped `lineage-engine` #23 (2026-09-17, sha 81e61956). **RESUME HERE = PR4.**

> **PR0 result (Sophia, 2026-09-15):** two pre-flight items **rectified this document** — the plot
> flow *is* shipped but hardcodes its origin (§1.3b), and `program_assets/registry.json` does not
> exist (§1.4). Read §7 before starting PR1.

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

### 0.1 Gary's follow-up clarification (2026-09-15, same day) — resolves two of the rows above

*"So basically when a student registers a tree or monitors a tree or registers a plot it should be
the same as how it currently behaves on sunmint.truesight.me but the profile of the student should
show up here too [`programs/crf-anapu/members.html`] — and then clicking in should associate the
tree or the monitoring or the plot associated with the student who performed the effort."*

Two things this resolves:

1. **Confirms Open Decision #2 (§6) = YES.** Submission alone — no DAO credential required — is
   sufficient to earn a listing on `members.html`. Row 3 above was already read at High confidence;
   this removes any doubt.
2. **The submission UX itself is explicitly confirmed unchanged** — "the same as how it currently
   behaves on sunmint.truesight.me." This endorses **Option A** (§2.1, thin redirect into the
   canonical app) over Option B (vendored copy): a vendored copy risks behavioral drift from the
   canonical app over time, which is exactly what "the same as it currently behaves" rules out.
3. **New, more specific requirement than §2.2 point 3 originally captured:** clicking through from a
   member's card must show the **itemized** trees / monitoring events / plots that student
   specifically submitted — not merely an aggregate count badge. This maps directly onto a mechanism
   that already exists and didn't need inventing: `cv.programs[<program-slug>].recent_events[]` inside
   each member's CV JSON (§1.2 §5 of `CREDENTIALING_PROGRAM_PAGES.md` — already used to list a
   capoeira practitioner's practice sessions on their credential page). The click-through target is
   the **existing** `programs/crf-anapu/credentials/index.html` wrapper — extended to render SunMint
   event entries in `recent_events[]` alongside (or instead of) practice-session entries, using the
   same per-pk-hash `sunmint/*.json` files already proposed in §3.2. This does not require a new page
   type; it requires the existing CV renderer to know a second `recent_events` shape. See §2.2 and §4
   for the updated design and the privacy tension this introduces.

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

> **🔧 PR0 rectification (2026-09-15):** the "zero app-code change" headline holds for planting +
> monitoring but **NOT for the plot/boundary flow** (see §1.3b). And under **Option A** (the redirect),
> `Submission Source: window.location.href` records the **post-redirect** host
> (`sunmint.truesight.me`), *not* `cfr.truesight.me` — so origin attribution must ride on the explicit
> **`Program:` field** (§3.1), not on `href`. Treat `Program:` as **required in all options and all
> three flows**, not as an Option-A add-on.

### 1.3b The third event type — plot/boundary — IS shipped (✅ PR0-resolved; this section rectified)

> **PR0 (Sophia, 2026-09-15):** this section originally claimed the boundary module was *not* shipped
> in the farmer-facing app and required a live pre-flight check. **That check is done and the claim
> was wrong** — the module ships, it was simply not in the two pages a static scan looked at.

The `[FARM BOUNDARY EVIDENCE EVENT]` lives at **`sunmint_beta/limites-da-fazenda/index.html`** —
reached only through the app's page-nav dropdown (`onNavChange` → `:884`), which is why scanning only
`index.html` + `monitor-tree-growth/` missed it. That page emits the full plot lifecycle:

- `[FARM BOUNDARY EVIDENCE EVENT]` (`:754`) — the plot submission,
- `[PLOT INVALIDATION EVENT]` (`:615`),
- `[MEDIA RETRACTION EVENT]` (`:682`).

**The relevant gotcha:** this page carries `Submission Source`, but as a **hardcoded slug**
(`'sunmint-limites-da-fazenda'`) — *not* `window.location.href` — and it has **no `Program` field** at
all. So the §1.3 headline ("zero app-code change required") is **true for planting + monitoring and
false for plots**: plot origin attribution needs an app-code change in *every* option. This is the
single reason the `Program:` field (§3.1) must be added to **all three flows** rather than only as an
Option-A affordance — see the rectification note in §1.3.

### 1.4 The `lineage-credentials` data model — the mechanism to reuse, not reinvent

`lineage-engine/scripts/build_cv_cache.py::collect_practitioners()` walks
`lineage-credentials/programs/<program-slug>/pk-<hash>/{identity.json, practice/*.json}` — one
directory per program, per contributor (identified by RSA-public-key hash, the same identity primitive
used everywhere else in this DAO). For each `pk-<hash>`, it aggregates the `practice/*.json` event
files into `practice_count` / `total_practice_minutes`, and `primary_program` is computed by
`_program_activity_score` — whichever program has the most practice activity for that pk-hash wins.
This is **entirely capoeira-shaped today**: the folder is literally named `practice`, and the
aggregation fields (`total_practice_minutes`) are capoeira-specific. > **🔧 PR0 rectification (2026-09-15):** the original text cited a `program_assets/registry.json` as an
existing data-slug ↔ URL-slug divergence mechanism. **That file does not exist** (`lineage-engine`
`scripts/program_assets/` is an empty directory) — the citation is withdrawn.

**This is the integration point.** Making SunMint submissions "count" toward `members.html` does not
require inventing a new membership system — it requires teaching this *existing* pipeline about a
second kind of activity (tree submissions) alongside practice sessions, and writing a small sync job
that turns `Submission Source`-tagged SunMint events into files this pipeline already knows how to
read (with a new, non-`practice`, appropriately-named subfolder — see §3).

---

## 2. Target architecture

### 2.1 `cfr.truesight.me`'s tree-submission surface — **DECIDED: Option B (vendored copy)**

> **✅ GOVERNOR DECISION (Gary, 2026-09-15, thread 30026): Option B — vendor a full copy of the SunMint app into the `cfr-anapu` repo.** Rationale: the parameterized-redirect (Option A) required persisting the slug across in-app navigation (the `?program=` param is silently dropped when the app moves from `/` to `/monitor-tree-growth/`), which Gary judged *"too complicated."* A vendored copy keeps the URL bar on `cfr.truesight.me` throughout and — because both live submission flows already stamp `Submission Source: ${window.location.href}` — needs **zero** app-code change for attribution. Option A is retained below for the record.

**Option A — thin branded redirect into the canonical app (REJECTED — retained for the record).**
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

**Decision: Option B (Gary, 2026-09-15).** Option A was rejected not on drift grounds but on **UX complexity** — the `?program=` param is dropped the moment the app navigates internally, so the redirect required stashing + re-applying the slug on every submit page.

**Option B build spec (authoritative for PR1/PR2):**
- **Attribution needs no `Program:` field.** Both live flows already stamp `Submission Source: ${window.location.href}`; served from `cfr.truesight.me` that becomes `https://cfr.truesight.me/…` automatically. The **only** app fix is `limites-da-fazenda/`'s hardcoded `'sunmint-limites-da-fazenda'` literal (PR1).
- **Program mapping is by origin.** The derive/sync pipeline (PR3/PR4) maps a submission's `Submission Source` host → program slug via each program's `manifest.json`.
- **Layout on `cfr-anapu` `gh-pages`** (Pages serves *this* branch, not `main`): `/index.html` = vendored app (planting); `/monitor-tree-growth/`, `/limites-da-fazenda/`, `/instrucoes/` = vendored; the credentialing page moves to **`/program/`** (asset refs rewritten to `../`); **`members.html` stays at root** so existing links keep resolving. **Never vendor the app's `CNAME`.**
- **Sync is scripted, not manual** — `sync_sunmint_app.py` (dry-run default, opens a PR). A hand-copy of a repo with this many branches *will* drift.

**⚠️ No beta environment exists for `cfr-anapu`.** `cfr.truesight.me` is a live public Pages site, so merging to `gh-pages` deploys instantly. PR2 therefore ends with an immediate live smoke-check instead of a beta UAT.

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
6. **Itemized click-through (confirmed requirement, §0.1) — extend the CV renderer, don't build a new
   page.** `members.html` cards already link to `programs/crf-anapu/credentials/#<slug>`
   (§1.2/`CREDENTIALING_PROGRAM_PAGES.md` §3). That page already renders
   `cv.programs[<program-slug>].recent_events[]` for capoeira practitioners. Extend it so, when
   `cv.programs['crf-anapu'].sunmint_events[]` is present (populated from the same `sunmint/*.json`
   files as point 3, read alongside `practice_events`), the page lists each specific tree planting /
   monitoring visit / plot the student submitted — one row per event, not an aggregate. Each row: event
   type, species/date, and a link to that item's **already-public** record (the tree's entry on
   `truesight.me/sunmint.html`'s Impact Map, or its QR profile page) rather than re-rendering raw
   GPS/photo on the credential page itself — see §4 for why.

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
sensitive than a bare name-on-a-cohort-list. Gary's 2026-09-15 clarification (§0.1) confirms the
click-through **must** show itemized trees/monitoring/plots, not just a badge count — so the privacy
line has to be drawn at *what each item shows*, not *whether items show at all*:

- **`members.html` card (list view):** aggregate counts only (🌳 3 trees · 📍 1 plot · last active
  2026-09-10) — unchanged from the original recommendation, next to whatever name display the
  existing `public_listable` gate already allows.
- **`credentials/#<slug>` (click-through, per §2.2 point 6):** itemized rows — event type, species,
  planting/monitoring date — **linking out to that item's already-public record** (the tree's own
  entry on `truesight.me/sunmint.html`'s Impact Map or QR profile page, which is where raw GPS and
  the planting photo already legitimately live today, independent of this proposal) rather than
  re-rendering GPS/photo a second time on the credential page. This isn't a privacy compromise: the
  Impact Map is already public for every planted tree regardless of program, so linking to it exposes
  nothing that isn't already exposed; what stays off the credential page is the *aggregation* of "all
  of this specific minor's locations in one place," which is a materially different privacy surface
  than any single tree's already-public pin.
- **✅ RESOLVED (Gary, 2026-09-15): CEPOTX/Jedielcio already signed off** on this privacy posture —
  the link-out-rather-than-duplicate design is confirmed, not just recommended.

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

1. **✅ RESOLVED — Option B (vendored copy).** Gary, 2026-09-15 (thread 30026): *"instead of parameterized approach, a vendored approach is better"* — the param-drop-on-navigation problem made A "too complicated." Supersedes the earlier A-lean; see §2.1 for the build spec.
2. **✅ RESOLVED (§0.1, 2026-09-15):** a tree-submission-only contributor (no credential) IS allowed
   to appear on `members.html` — "the profile of the student should show up here too." No further
   confirmation needed on this point.
2b. **If yes to #2** — should a tree/plot submitted through `sunmint.truesight.me` directly
   (i.e. `Submission Source` host `sunmint.truesight.me` — the generic, unbranded surface) ever retroactively count toward a program's
   cohort if the submitter later turns out to be a CRF Anapu student? Recommend **no** — origin
   attribution should be at submission time only, exactly as literally requested ("submissions via
   that route"), not inferred after the fact from identity.
3. **✅ RESOLVED (Gary, 2026-09-15).** Privacy scope (§4) — aggregate counts on the cohort card,
   itemized rows (type/species/date) on click-through, **linking to** each tree's already-public
   Impact Map/QR entry rather than duplicating GPS/photo on the credential page. **CEPOTX/Jedielcio
   have already signed off on this posture** — no further partner confirmation needed on this point.

   > **🔧 PR0 rectification (2026-09-15):** the sign-off is obtained, but name the *actual* new exposure
   > precisely when re-confirming: it is **not** "counts vs rows" (aggregation), it is the **linkage** —
   > a *named* (minor) student → a *public* GPS coordinate, where today the tree is public and the
   > profile is private but the two are **not joined**. The CRF Anapu plot centroid (−3.38925/−51.30040)
   > is a school. The sign-off should be recorded as covering that correlation, not merely itemization.
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

1. **`FARM BOUNDARY EVIDENCE EVENT`'s shipped location** — ✅ **RESOLVED (PR0, 2026-09-15).** It **is**
   shipped, at `sunmint_beta/limites-da-fazenda/index.html`, reached via the page-nav dropdown (not
   the two pages a static scan looked at). Emits `[FARM BOUNDARY EVIDENCE EVENT]` (`:754`) +
   `[PLOT INVALIDATION EVENT]` (`:615`) + `[MEDIA RETRACTION EVENT]` (`:682`). It **carries
   `Submission Source`, but hardcoded** as `'sunmint-limites-da-fazenda'` — **not**
   `window.location.href`, and **no `Program` field**. → see §1.3b; drives the §1.3/§3.1 correction.
2. **`verify_public_signatures`'s `tree_*` bucket schema** — ✅ **RESOLVED (PR0, 2026-09-15).**
   Confirmed a **valid** read source for the sync job. Buckets: `tree_planting` (167),
   `farm_boundary_evidence_event` (6), `tree_growth_monitoring` (2); root `index.json` carries
   `total_count` 4360 with per-type `index_url`. **`Submission Source` survives** into each attestation
   inside `signed_payload` (verified on the latest planting record) — it is **not** stripped during
   ingestion. A future `Program` field will survive the same way.
3. **The capoeira practice-event sync trigger mechanism** — ✅ **RESOLVED (PR0, 2026-09-15).** There is
   **no cron and no webhook** for practice events: `programs/<slug>/pk-<hash>/practice/*.json` are
   committed **by hand** (git author `Gary Teh`, message `practice event: capoeira-tribo-mirim pk-…`),
   and aggregation is the standalone `lineage-engine/scripts/build_cv_cache.py`. The **only** automated
   precedent on the autopilot box is the **every-30-min `sync_sunmint_signatures.py` cron** — PR3's new
   sync job should follow **that** pattern, not invent a third.
4. **`sunmint_beta`'s exact query-param reading convention** — ✅ **RESOLVED (PR0, 2026-09-15).** The
   planting page already reads query params via `URLSearchParams` (`searchParams.get('vk'/'em')`), so
   `?program=` matches the app's existing style — no new idiom introduced.
5. ~~**CEPOTX/Jedielcio's actual consent posture**~~ — **✅ RESOLVED (Gary, 2026-09-15): already
   signed off.** No longer a pre-flight blocker.

✅ **Pre-flight COMPLETE (PR0, 2026-09-15):** items 1–4 resolved by live repo reads — **no open
pre-flight items remain**. Two resolved items **rectified this document** (§1.3b boundary flow is
shipped-but-hardcoded; §1.4 `registry.json` citation withdrawn). Item 5 resolved earlier by Gary.
PR1 may start.

---

## 8. Sequenced execution roadmap (one PR per turn — §5a)

| Unit | Scope | Advance |
|---|---|---|
| **PR0** | ✅ **DONE 2026-09-15** — §7 items 1–4 resolved (live repo reads); §6 updated. Rectified §1.3/§1.3b/§1.4/§6 #3. No code. | auto |
| **PR0b** | ✅ **DONE 2026-09-15** — **architecture re-pointed to Option B (vendored copy)** per Gary (thread 30026); §2.1 rewritten with the Option B build spec; §6 #1 resolved; PR1/PR2 redefined; §8/§9 updated. No code. | auto |
| **PR1** | ✅ **DONE 2026-09-16** (`sunmint_beta` #84, sha 3732e2a4) — (a) un-hardcoded `limites-da-fazenda/index.html`'s `Submission Source` literal → `window.location.href` (the only flow that pinned an origin); (b) vendor-readiness audit landed as `VENDOR_READINESS.md` (PR2 rewrite list; canonical edgar/dapp endpoints; per-origin SW cache — no collision); (c) no `Program:` field — attribution is by origin. Tests: `tests/test_submission_source_origin.py` (4 cases); full suite 17 passed. | auto |
| **PR2** | ✅ **DONE 2026-09-17** (`cfr-anapu` #5, sha `f0ffdbda`, squash-merged to `gh-pages` = **deployed**) — vendored the SunMint app into `cfr-anapu` `gh-pages` (Option B): `index.html`, `monitor-tree-growth/`, `limites-da-fazenda/`, `instrucoes/` (+`instrucoes/send-as-file-tip.png`), `service-worker.js`; credentialing page relocated `index.html` → `program/index.html` (refs → `../styles/`, `../js/`; `View cohort` → `../members.html`); `members.html` + `CNAME` kept at root. Added `sync_sunmint_app.py` (dry-run default) + `vendor.json`. **Live smoke-check green** on `cfr.truesight.me` (`/`, `/monitor-tree-growth/`, `/limites-da-fazenda/`, `/instrucoes/`, `/program/` all 200; `/` = vendored app with `Submission Source` self-attribution; `/program/` = credentialing page). | auto (no beta env — see §2.1) |
| **PR3** | ✅ **DONE 2026-09-17** (`lineage-engine` #23, sha `81e61956`) — new `scripts/sync_sunmint_program_activity.py` reads `verify_public_signatures`' `tree_planting` / `tree_growth_monitoring` / `farm_boundary_evidence_event` buckets and writes one JSON per event into `lineage-credentials` at `programs/<slug>/pk-<hash>/sunmint/<msg_id>.json`. Option-B attribution (`Submission Source` host → slug) via new `scripts/sunmint_program_registry.json` (`cfr.truesight.me` → `crf-anapu`); new non-`practice` `sunmint/` folder so capoeira `practice_count`/`total_practice_minutes` stay clean; pk-hash = `pk-` + base64url(SHA-256(base64-decoded pubkey))[:12] (asserted byte-exact vs a live `identity.json`); idempotent content-addressed skip (git-blob sha); **dry-run default**, `--push` to write. Live dry-run reads 168/2/19 events → **0 attributable today** (no `cfr.truesight.me` source has landed yet — the app deployed in PR2). 19 unit tests; caught+fixed a markdown-bullet `Submission Source` parser bug during the live check. **Nothing written to `lineage-credentials` (dry-run).** | auto |
| **PR4** | `lineage-engine`: extend `collect_practitioners()` + `_program_activity_score()` in `build_cv_cache.py` for the new `sunmint/` activity kind (§2.2 points 3–4); extend `manifest.json` schema for `program_modes` array (§6 decision #4). | auto |
| **PR5** | `truesight_me_beta` (+ `cfr-anapu` mirror): `program-shell.js` renders SunMint activity badges on `members.html` cards (§2.2 point 5, aggregate-only per §4) **and** extends the `credentials/index.html` CV renderer to list itemized `sunmint_events[]` rows on click-through, each linking to the tree's public Impact Map/QR entry rather than duplicating GPS/photo (§2.2 point 6, §4). Update `programs/crf-anapu/manifest.json` to the new `program_modes` shape. | auto (beta); prod gated on UAT |
| **PR6** | First real sync run (dry-run then live) against real CRF Anapu submissions (needs at least one real submission to exist first — may require a CEPOTX/Jedielcio coordination step outside any PR). Verify `members.html` populates. | **`gate: human`** — first live write into `lineage-credentials` from a new activity kind |
| **PR7** | Docs: update `CREDENTIALING_PROGRAM_PAGES.md` with the new `sunmint_cohort` mode (it's the canonical spec, editable per its own convention — this is documentation of a shipped feature, not a forecast); update `handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md`'s status; UAT. | auto |

**RESUME HERE → PR4** (PR0 + PR0b + PR1 + PR2 + PR3 complete 2026-09-17 — §7 pre-flight resolved; architecture = **Option B**). PR1 = `sunmint_beta` vendor-readiness (`sunmint_beta` #84, sha 3732e2a4). PR2 = the vendor PR into `cfr-anapu` `gh-pages` (`cfr-anapu` #5, sha f0ffdbda; **live on `cfr.truesight.me`**, smoke-check green). PR3 = the `lineage-engine` sync job (`lineage-engine` #23, sha 81e61956; dry-run default — reads the confirmed source per §7 item 2, writes `programs/<slug>/pk-<hash>/sunmint/*.json` into `lineage-credentials`). **PR4 = extend `build_cv_cache.py` `collect_practitioners()` + `_program_activity_score()` for the new `sunmint/` kind** (§2.2 pts 3–4) + extend `manifest.json` for the `program_modes` array (§6 #4). **PR6 remains the only `gate: human`.**

---

## 9. UAT

- **U1** — Submit a real (or clearly test-tagged, per §5g standing E2E authorization) tree planting via
  the vendored `cfr.truesight.me` surface. Confirm the ledger event carries `Submission Source: https://cfr.truesight.me/…` and is attributed to `crf-anapu`.
- **U2** — Confirm the sync job (PR3) picks up that event and writes the expected
  `lineage-credentials/programs/crf-anapu/pk-<hash>/sunmint/*.json` file.
- **U3** — Confirm `build_cv_cache.py` (PR4) correctly aggregates it and the pk-hash appears (or is
  updated) in `_cache/index.json` with `primary_program`/`programs[]` including `crf-anapu`.
- **U4** — Load `https://beta.truesight.me/programs/crf-anapu/members.html` (then, after prod
  promotion, `https://cfr.truesight.me/members.html` and `https://truesight.me/programs/crf-anapu/members.html`)
  and confirm the submitter's card shows the correct activity badge, with no raw GPS/photo exposed.
- **U4b** — Click through from that card to `credentials/#<slug>` and confirm the specific tree
  planting appears as an itemized row (type, species, date) with a working link to its public Impact
  Map/QR entry — and confirm the credential page itself still shows no raw GPS/photo (§4).
- **U5** — Confirm a submission via plain `sunmint.truesight.me` is completely unaffected — it stamps `Submission Source: https://sunmint.truesight.me/…` and is **not** attributed to any partner program.
- **U6** — Confirm test data cleanup per §5g (test rows removed / clearly marked, no leftover value in
  a real ledger).

---

## 10. Rollout

**Approved; PR0 + PR0b + PR1 + PR2 + PR3 complete; PR4 is next.** Reviewed in the Telegram topic **"CFR partnership - figure
out how to present"**. All §6 open decisions are resolved (Gary confirmed Option A, submission-only
membership, and reported CEPOTX/Jedielcio's sign-off on the privacy posture). **PR0 completed
2026-09-15 (Sophia)** — all §7 pre-flight items resolved by live repo reads and folded back into this
doc (§1.3/§1.3b/§1.4/§6 #3). **RESUME HERE (§8) = PR4**, driven by a supervisor (Envoy or Sophia, per
`sophia/SUPERVISOR_LOOP.md`). **PR6 is the only `gate: human`** and no prod promotion happens before the
UAT gate (§9).
