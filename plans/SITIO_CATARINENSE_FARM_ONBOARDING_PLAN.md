# Sítio Catarinense (Jhordan, Anapu/Pará) — farm onboarding execution roadmap

> Governor source: `WhatsApp Chat - Jhordan - Anapu CFR.zip` (22 MB, unpacked `/tmp/jhordan` on the
> autopilot box), analyzed independently by both Envoy and Sophia (channel
> `#sitio-catarinense`, 1562002603351736421) — findings converged, see §0.
> Follows `AGROVERSE_SUNMINT_FARM_LISTING.md` end-to-end SOP; worked-example precedent is
> §7 of that doc (Sítio Raimundo & Geniza, 2026-09-02→04).

---

## 0. Pre-flight — facts captured, no execution unit should need to re-derive these

**Counterparty:** Jhordan Madian Costa de Oliveira — CRF "Dorothy Stang" student, Anapu/Pará.
Family on the property since 2014 (region since 2008); father acquired **150 ha via an INCRA land
settlement program**; father ex-truck-driver, mother a teacher, Jhordan a student. Activities: cacao,
cassava, corn, cattle, plus dozens of protected giant **Bertholletia excelsa** (Brazil nut, est.
300–400 yr old).

**Farm name (self-reported, in response to a direct governor question):** "sítio catarinense."

**Boundary geometry — computed independently, not trusted from the claim:**
- KML (`00000057-sitio catarinense.kml`, 5-vertex closed polygon) → **150.78 ha** (shoelace
  calc on an equirectangular projection), matches the 150 ha claim almost exactly.
- Perimeter 5.85 km, simple polygon (no self-intersection).
- Centroid **−3.5137, −51.5799** — 9.4 km from Anapu town, 34 km from the CRF school.
- The 4 corner coordinates Jhordan separately typed by hand (DMS, in chat) match 4 of the KML's
  5 vertices exactly — the KML is consistent with his own numbers, not a re-draw.
- **No overlap with any existing registered SunMint plot** — nearest is `V-06-29-reforestation_...`
  (Paulo / La do Sítio), 33 km away. This is a genuine new farm, not a re-registration.
- **`boundary_authority` must be recorded as `approx`** (hand-typed corners + a KML he drew, not a
  GPS walk or a CAR/INCRA polygon) — *even though* the property was itself INCRA-settled, which
  means an authoritative INCRA polygon likely exists and could upgrade this later. Do not claim a
  higher authority than the evidence supports (§2 below never auto-upgrades this).

**Existing CFR Anapu tree-planting record — already paid, already on this land:**
- `pk-qkejKJJW3IAD`: 18 trees planted 2026-09-24 + 86 trees from an Oct 12–15 capture session
  (91 raw captures, 5 self-reported duplicates excluded by Jhordan *before* being asked) = **92
  unique trees**, **R$520 total**, two Pix transfers (R$90 on 2026-09-29, R$430 on 2026-10-17),
  both bank-reference-confirmed as paid. Exact reconciliation, no gap, no double-pay.
- Cross-checked directly: **every one of the 109 raw point records** in `sunmint/trees/index.geojson`
  (full 245-feature registry) that falls inside the KML polygon belongs to this same `pk_hash`. No
  foreign/unlinked submitter is hiding inside the boundary.

**One adjacent tree found outside the polygon, under a DIFFERENT submitter — new finding,
not previously surfaced:**
- `Edgar_20260924122114_057` (species Sumaúma / *Ceiba pentandra*), `pk_hash: pk-Ee4aYLRkptun`,
  submitted the same day as Jhordan's first batch (2026-09-24), sits **1.07 km outside** the KML
  boundary. Its registry record currently shows `nearest_plot_id: V-06-29-reforestation_...` at
  **33.6 km** — because Sítio Catarinense doesn't exist as a registered plot yet. Once it does,
  this tree is far closer to the new plot than to any currently-registered one.
- Submitter identity not yet resolved (pk_hash → contributor name needs a Main Ledger
  `Contributors contact information` sheet lookup — not resolvable from a repo search).
- **This generalizes**: the registry already carries `plot_dist_m`/`nearest_plot_id` per tree for
  exactly this purpose. §4 below makes "recompute these against the new polygon, flag anything
  close" a standard post-registration step — not a one-off for this farm.

**Media inventory (on `/tmp/jhordan`):**
- 11 family photos (`00000085`–`00000098`, incl. a strong people-first candidate — a woman
  cutting fresh cacao pods, confirmed by direct visual review).
- 1 higher-res Samsung original (`00000073`, 4000×2250, has datetime, **no GPS**).
- 5 videos (`00000069`–`00000072`, `00000100`, 478×850, **no GPS tag**). Note: `00000071` and
  `00000100` are byte-identical (same MD5) under different names — dedupe will collapse them.
- Giant Bertholletia excelsa photos/video among the family set.
- 1 voice note (`00000018`, not yet transcribed).
- **GPS blocker**: every JPG/MP4 in this zip has zero EXIF/GPS — WhatsApp recompression strips it
  on photo/video upload. Per `AGROVERSE_FARM_PAGE_CONVENTIONS.md` §2 and
  `MEDIA_ARCHIVE_PIPELINE.md` §2, map-placed media needs GPS-bearing **originals** (Document mode
  or email, not "Photo"/"Video" mode). **This media cannot be map-pinned as-is.** Family/story
  photos can still be used in the page gallery (they don't need GPS), but none of the 5 video
  clips or 11 photos should be claimed as plot-boundary evidence.

**Farm story (Jhordan's own words, 2026-10-20 chat — quote verbatim, do not paraphrase):**
> "We have lived here since 2014, when my father acquired this 150-hectare property through an
> INCRA land settlement program. We work in agriculture and livestock farming, cultivating crops
> such as cacao, cassava, and corn, and raising cattle, among other activities." ... "My father was
> a truck driver before he became a farmer." ... "My mother still works as a teacher to this day."
> ... "My parents are from the states of Santa Catarina and Paraná, and they came to live here in
> this region in 2008."

**Template page:** `rancho-maranta-para` — per `AGROVERSE_SUNMINT_FARM_LISTING.md` §4, "is the
current template" (verify this is still true at execution time with one `git ls-remote`/directory
check — templates drift; if a newer one exists, use it and note the change here).

**Not CEPOTX-network — plot_id naming needs a governor call, not a derived guess.** CRF Anapu is a
different school/program from the CEPOTX cooperative network (COPOPS/COOPOXIN/COPOTRAN/COPCAO).
`SUNMINT_PLOTS_REGISTRY.md` §3 step 4 says plot_id = CEPOTX site code **where issued, else
`<PREFIX>-P1`**. There is no CEPOTX code here. §1 below surfaces the naming question explicitly
rather than silently picking a prefix.

**Explicitly OUT OF SCOPE for this roadmap:**
- Answering Jhordan's carbon-credit question (separate correspondence; Sophia already drafted the
  substance — standing old-growth trees aren't creditable, ARR/VM0047 or REDD+ avoided-deforestation
  are the real pathways, Brazil REDD+ median ~$2.50/t — Q1 2025, VM0048 floor ~$12/t). This roadmap
  does not send anything to Jhordan; §1 drafts a reply for governor review only.
- Full FSVP supplier entity registration (`fda_fsvp/suppliers/...`) — not CEPOTX-network, no urgent
  compliance driver identified. Logged as a deferred follow-up (§6), not a roadmap unit.
- The dead-link defect in `00000017-CFR_Anapu_18_trees.pdf` (zero PDF link annotations, violates
  `PAYOUT_REPORT_SOP.md` §4) — filed as a doc-only `OPEN_FOLLOWUPS.md` entry (§6), not part of the
  farm build itself.

---

## 1. STEP ZERO — naming gate (governor decision, not Sophia's call)

Per `AGROVERSE_SUNMINT_FARM_LISTING.md` §0: never invent attribution or a farm name/slug without
governor confirmation. **This unit is a single Discord question, not a PR.** Ask the governor to
confirm or override:

1. **Farm slug** — two candidates on the table: `sitio-catarinense-para` (Envoy, matches the
   `<farm>-<region>` convention used by `raimundo-geniza-para`/`paulo-la-do-sitio-para`) vs.
   `sitio-catarinense-anapu-para` (Sophia, more specific). Recommend the governor just pick one;
   both are reasonable.
2. **Plot ID prefix** — recommend `SC-P1` (no CEPOTX code applies; `<PREFIX>-P1` fallback per
   registry §3 step 4).
3. **Confirm:** link the existing `pk-qkejKJJW3IAD` trees (92) to the new plot as part of
   registration (recommended, strongly evidenced — see §0).
4. **Privacy default** — public, per the SOP's stated governor default, unless told otherwise.

**Do not proceed past PR2 (plot registration) without an explicit answer to #1 and #2.** #3 and #4
are low-risk defaults Sophia may proceed on if the governor doesn't object within a reasonable
window, consistent with how this roadmap's other auto-gated units work.

---

## 2. PR roadmap — one PR (or one ops unit) per turn

| # | Scope | Repo / system | Gate |
|---|---|---|---|
| PR0 | This plan + `HANDOFF_MANIFEST.md` row + `handoffs/index.json` regen | `agentic_ai_context` | auto (docs) |
| U1 | STEP ZERO naming question posted to `#sitio-catarinense` | Discord (ops, no PR) | auto — but blocks PR2+ until answered |
| PR2 | Register farm + plot: SunMint Farms/Plots sheet rows, regenerate `plots/index.geojson` + `farms/index.json`; anchor a geo-located ledger event (FARM BOUNDARY or TREE PLANTING EVENT at centroid) | `sunmint` (data, Contents API) + ledger | auto once U1 answered — own-repo, reversible, no money |
| PR3 | **Tree-registry re-link**: recompute `nearest_plot_id`/`plot_dist_m` for the full 245-feature `trees/index.geojson` against the new polygon; link all 109 `pk-qkejKJJW3IAD` points to the new plot; flag (don't auto-link) `Edgar_20260924122114_057` / any other tree now closer to this plot than its current nearest, for governor review | `sunmint` (data) | auto — read + flag, no silent cross-submitter linking without a human look |
| U4 | Ask Jhordan for GPS-bearing originals (Document/email mode) of the 5 videos + 11 family photos, if map placement is wanted; chase the promised virgin-forest KML. **Draft only — governor sends.** | correspondence | gate: human (outward-facing) |
| PR5a | Farm page skeleton: clone `rancho-maranta-para` (or current template) → `farms/<slug>/index.html` + `media.json`, mandatory post-clone token grep (gotcha #8), hero = people-first family photo, story = verbatim Jhordan quote, Leaflet pin at centroid + polygon overlay, two-way SunMint link | `agroverse_shop_beta` | auto → beta review |
| PR5b | Gallery wiring: upload web-optimized family/tree JPEGs to `assets/images/farms/<slug>-*.jpg`; wire `media.json` gallery entries. Videos deferred — see U4 (no GPS-bearing originals yet, and raw video shouldn't be committed to git either way per `MEDIA_ARCHIVE_PIPELINE.md`) | `agroverse_shop_beta` | auto → beta review |
| PR6 | Beta UAT (checklist §4) | `beta.agroverse.shop/farms/<slug>/` | **always-stop: human** |
| PR7 | Prod promotion (`sync_beta_to_prod`), only after PR6 passes and governor says go | `agroverse_shop_beta` → `agroverse_shop_prod` | **always-stop: human — prod deploy** |
| PR8 | Impact map: add `FARM_SLUG` entry only if plot `farm_id` ≠ page slug; verify the PROD `truesight.me/sunmint.html` plot popup links out correctly (only clickable post-PR7) | `truesight_me_beta` → sync | auto → beta review; prod link verify after PR7 |

**Do not combine PR5a/PR5b or PR6/PR7 into one turn** — each is scoped to stay well under the
~30-tool-round cap, per §5a. PR3 can run in the same turn as PR2 if room allows (both are the same
`sunmint` repo, same data-regeneration pattern) but should still be reported as two distinct,
individually-verifiable changes.

---

## 3. Resume tracker

**RESUME HERE:** PR0 (this plan, landing now) → then U1 (ask the naming question).

Nothing is mid-flight. No execution unit above should need to read cross-repo state that isn't
already captured in §0.

---

## 4. UAT checklist (PR6, before any prod-promotion ask)

- [ ] Hero image shows people, not just scenery (per `AGROVERSE_FARM_PAGE_CONVENTIONS.md` §1).
- [ ] Farm story matches Jhordan's verbatim quote (§0) — not paraphrased, not invented.
- [ ] Post-clone token grep clean — no leftover `rancho-maranta` / other source-farm strings,
  no `header-<name>.jpg` 404s (gotcha #8).
- [ ] `canonical`/`og:url`/`twitter:url` each resolve to `https://www.agroverse.shop/farms/<slug>`
  exactly once — no double-appended region suffix (gotcha #9).
- [ ] Leaflet map pin sits at the computed centroid (−3.5137, −51.5799) with the KML polygon
  overlaid; popup bind strings escape apostrophes correctly (gotcha #1).
- [ ] Two-way SunMint link verified **both directions**: farm page → map (`sunmint.html?plot=<ID>`
  as a real `<a>`, not text) and map → farm page (`FARM_SLUG` entry present if needed).
- [ ] `media.json` gallery renders every included photo; no video entries yet (GPS blocker, §0).
- [ ] No 404s on any asset path; GitHub Pages deploy lag (~90s) accounted for before failing a check.
- [ ] `plot_type` left **blank** in the registry unless the governor explicitly classifies it —
  never auto-defaulted (per `SUNMINT_PLOTS_REGISTRY.md` §4b).
- [ ] PR3's tree-relink is verifiable: query `trees/index.geojson` post-merge, confirm all 109
  `pk-qkejKJJW3IAD` points show the new plot id, confirm the Sumaúma tree is flagged (not silently
  linked) for governor review.

---

## 5. Gates (§5c)

- No prod deploy without explicit governor go (PR7).
- No default-branch merge of anything touching money/ledger without review (PR2's geo-event is
  metadata, not a transfer — still get a look before merge, since it's a ledger write).
- No message sent to Jhordan without governor review (U4 is draft-only).
- One PR/unit per turn — do not stack PR5a and PR5b, or PR6 and PR7, in the same turn.

---

## 6. Follow-ups filed separately (not roadmap units)

- `OPEN_FOLLOWUPS.md`: `00000017-CFR_Anapu_18_trees.pdf` has zero PDF link annotations on its
  "View tree" references — violates `PAYOUT_REPORT_SOP.md` §4. The two payout PDFs are correct
  (86/86 clickable annotations verified). Doc-only fix to the PDF generator, unrelated repo.
- FSVP entity registration for Sítio Catarinense — deferred, no CEPOTX/compliance driver yet.
- Carbon-credit correspondence with Jhordan — separate business-development thread, substance
  already drafted by Sophia in `#sitio-catarinense`, governor's call on timing/tone.

---

*Created 2026-10-20 from the `#sitio-catarinense` zip analysis (Envoy + Sophia, independently
converged). Cross-links: `AGROVERSE_SUNMINT_FARM_LISTING.md`, `SUNMINT_PLOTS_REGISTRY.md`,
`AGROVERSE_FARM_PAGE_CONVENTIONS.md`, `MEDIA_ARCHIVE_PIPELINE.md`.*
