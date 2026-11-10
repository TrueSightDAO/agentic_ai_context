# GENERATED_MEDIA_SOP.md — Generative models (Seedance / Seedream) inside the media workflow

**Status:** DRAFT — awaiting governor adoption (Gary Teh).
**Created:** 2026-11-10. **Owner:** Sophia Truesight (admin+sophia@truesight.me).
**Lives in `sops/`** (not `conventions/`) because this carries an operational workflow, a spend
approval, and a hard gate — same class as `PAYOUT_REPORT_SOP.md`. `conventions/` holds
format/style patterns (`PDF_STYLE_CONVENTION.md`, `EDITORIAL_TONE.md`).
**Parent runbook:** `MEDIA_ARCHIVE_PIPELINE.md` (MAP). This file extends it; where they
disagree, MAP wins on the archive and this file wins on generation.

**Contributors.** Gary Teh (the named scenarios: fillers, joiners, touch-ups,
product-to-video). Envoy (R5 fillers/joiners-prefer-Lane-A, R6 identifiable-people consent).
Sophia (Lane A/B architecture, R1–R4, economics, §7 scenario walkthroughs).

---

## 0. TL;DR

A generated asset is admissible **only** if it can answer one question: *what real thing is
this made of?*

- **Lane A — derivative.** Built from a real asset we already hold (a MAP preview frame, a
  gate-approved product photo). Records `derived_from: [sha256…]`. No disclosure needed —
  it is an edit of a real photograph, same class as a crop or a relight.
- **Lane B — synthetic.** Built from a text prompt. Records `derived_from: []` and
  `disclosure_required: true`. Needs a **visible AI label**.

Nothing generated ever enters the archive of record. Generation is a **distribution**
activity: MAP says *"Distribution ≠ archive — Instagram/TikTok/shop-page posting are
consumers of the archive, not the pipeline itself."* This SOP governs generating **for**
those consumers, and it never writes back into the archive.

**Recommended first pilot:** product-photo-to-video (§7.1) — zero consent questions, zero
location claims, lowest risk in the whole framework.

---

## 1. Why this exists (the one-paragraph version)

Gary asked how the new **ByteDance Seedance/Seedream** (Doubao, Volcano Ark) and **Meituan
LongCat** models could streamline social content marketing on top of MAP. The honest answer
is: barely, for generation — but substantially for **motion**, because MAP already
manufactures the perfect input for free. Every video in MAP has **one ffmpeg preview frame
in hot S3 Standard** (`previews/<farm-id>/<basename>.jpg`), GPS-stamped, sha256'd, manifest-
indexed. That is an image-to-video source that costs nothing and traces to a real original.
The framework below exists so we can use that, without ever shipping a picture of something
that did not happen.

**The forcing incident.** In the 2026-11-10 newsletter session, four images were rejected by
the image gate. `black-king-packing-header.jpg` was captioned as a packing room and the gate's
model independently read it as *"outdoor beach selfie of two smiling men."* That is the failure
mode this SOP is written against — not "AI images look bad," but **a caption claiming
provenance the pixels do not have.**

---

## 2. Where generation sits relative to MAP

```
real capture (HEIC/MOV, GPS, sha256)
   → MAP: manifest + S3 raw + YouTube yt_id + PREVIEW FRAME (hot S3)
        ↓                                              ↓
   archive of record                       ┌────────────────────────────┐
   (provenance chain,                     │ SEEDANCE I2V from that frame │
    never generated)                      │ → motion insert / b-roll     │
                                          │ → 9:16 + 1:1 social cuts     │
                                          └────────────────────────────┘
                                                        ↓
                                             social distribution only
                                             (derived_from_sha256 recorded)
```

The left column is append-only truth. The right column is a **consumer** and its outputs
are labelled as such.

---

## 3. The two lanes

| | **Lane A — derivative** | **Lane B — synthetic** |
|---|---|---|
| **Input** | A real asset we hold: MAP preview frame, `farm-media-raw` photo, gate-approved product shot | A text prompt, title card, texture |
| **`derived_from`** | `[sha256, …]` — mandatory, at least one | `[]` |
| **`disclosure_required`** | `false` | **`true` — visible AI label** |
| **Allowed destinations** | Farm page b-roll, product page motion, social/Reels/TikTok, blog | Social and blog **only**, with label |
| **Forbidden destinations** | Archive of record, public YouTube farm channel | Farm page gallery, newsletter body, QR/tree page, archive of record |
| **Example** | 81% bar photo → 6 s slow push-in | "abstract cacao pod texture" |

> **The lane is a field in the manifest, not a convention.** An asset without a resolvable
> lane is unmanifested, and an unmanifested asset is — per MAP's own invariant — invisible
> to every consumer and fails silently. Do not let one exist.

---

## 4. Rules

### R1 — Generated assets never enter the archive of record

Separate S3 prefix (`generated/`) or repo folder, **never** mixed into `raw/<farm>/` or
`farm-media-raw/<farm-id>/photos/`. Generated clips are **never** uploaded to the public
YouTube farm channel: `yt_id` is the manifest's binding to a real recorded event, and a
generated clip holding that field would corrupt the archive's meaning retroactively.

### R2 — Never a generated frame where a real one exists

If MAP already holds a São Jorge packing-room photo, the post uses **that** one. Lane B
exists to fill gaps the archive cannot cover — motion, abstracts, textures — not to replace
captures we were diligent enough to archive. Run the search before you run the prompt.

### R3 — No synthetic humans on farm content (Lane B)

Non-negotiable. No generated farmers, no avatars, no "for illustrative purposes" people in
any supply-chain context. This is the exact failure the gate caught on 2026-11-10. It is
also why **LongCat-Video-Avatar is rejected outright** (§5) despite being MIT-licensed and
free: it is purpose-built to synthesize people.

### R4 — The gate stays load-bearing

`go_to_market/scripts/verify_newsletter_images.py` (PR #203) currently returns `FAIL` for
any `scene_type` in `{map, screenshot, graphic, render, illustration, chart}`. **That
behaviour is correct and is not to be loosened.** The permitted change is additive: an
`asset_class` field (`photo | ai_edit | illustration`) plus an `--allow-generated` switch,
so Lane A is auditable and Lane B must carry disclosure. An **unlabelled** generated photo
making a supply-chain claim stays a **hard FAIL**, unchanged.

### R5 — Fillers and joiners prefer Lane A (Envoy)

A "joiner" between real clip A and real clip B does **not** have to be synthesized from a
text prompt. It can be a Seedance I2V **motion-extension from clip A's own last real frame**
(or clip B's first real frame) — which is Lane A, because that frame has a real sha256.
That is a materially different claim from a generic prompted transition: *"a few extra
seconds of motion grown from a real moment"* vs *"an unrelated connective graphic."*

- **R5.1 —** When an adjacent real frame exists, fillers/joiners **MUST** be I2V-extended
  from it (Lane A, no disclosure).
- **R5.2 —** A prompted/generic filler with **no** real source frame is **Lane B** and needs
  the visible AI label from R4.
- **R5.3 — motion-extension is not event evidence.** The manifest records
  `motion: "extended"` with `motion_seconds`. An extended clip **may not** be cited as
  evidence that a recorded event occurred, may not carry a "recorded at" claim, and is
  capped at **≤ 4 s** of grown motion so it cannot drift into a fabricated scene. Grown
  motion is honest to the viewer only while it stays an embellishment of a real moment.

### R6 — Lane A I2V on an identifiable person needs that person's consent (Envoy)

Animating a real farmer's real photo — giving them motion they did not perform in that
moment — is a **narrower but different** question from animating a cacao pod, even though
both are "Lane A, `derived_from` a real sha256."

- **R6.1 —** Lane A I2V on any frame containing an **identifiable person** requires that
  person's **explicit consent before animation**, recorded in MAP's subject-release track.
- **R6.2 —** Consent is tracked **separately from the lane**. The lane answers
  *honesty to the viewer*; consent answers *the subject's own permission to be animated*.
  Both must pass; neither substitutes for the other.
- **R6.3 —** Default when unknown is **pending**, not granted. A frame whose people-status
  has not been resolved is treated as containing an identifiable person.
- **R6.3a — Recognizability threshold (added 2026-11-10, per Envoy/Gary review).** The
  conservative default is **kept**, but "identifiable" is now *defined* rather than assumed:
  it means **a face that is recognizably visible and in focus** — enough that a viewer could
  pick that person out again. A human-shaped presence that is distant, blurred, silhouetted,
  seen from behind, masked by helmet/gear, or under ~5% of frame area is **not** identifiable
  and does **not** trigger R6. Neither is a crowd so wide that no individual face resolves.
  The threshold narrows the *trigger*, not the obligation: once a face does meet it, consent
  is required exactly as R6.1 says.
- **R6.3b — The determination is a one-time human call, recorded on the frame — not a
  per-generation question.** Write it into the frame's own metadata (a sidecar keyed by the
  frame's `sha256`): `people_status: none | not_identifiable | identifiable | pending` plus
  `people_status_by` and `people_status_at`, so every future generation from that same frame
  **reuses** the ruling instead of re-asking. This is the difference between a policy that
  gets followed and one that gets routed around: an analyst generating 20 variants from one
  frame should answer the people-question **once**, and the answer should outlive the session.
- **R6.3c — Genuine ambiguity still defaults to `pending`, and `pending` still blocks
  generation.** The threshold exists to prevent paralysis on clearly-fine frames (a distant
  worker at the treeline), not to license a judgment call in favour of shipping. If two
  reasonable people would disagree about whether the face is recognizable, it is `pending` —
  pick another frame rather than spend the argument.
- **R6.3d — `people_status` is separate from `consent_ref`.** `not_identifiable` means no
  consent was triggered; `identifiable` means consent **is** sought and generation waits on
  `consent_ref`. Neither value may be inferred from the other.
- **R6.4 —** No people ⇒ no consent step (see §7.1: this is why product shots are the
  clean pilot).

---

## 5. Models, providers, licenses (facts as of 2026-11-10 — re-verify prices before integrating)

| Model | Role | Indicative price | Verdict |
|---|---|---|---|
| **Seedance 2.0** (ByteDance) | image-to-video / text-to-video | ~$0.030–0.060 **/sec** | **Adopt for Lane A I2V.** 15 s ≈ $0.45–0.90 |
| Seedance 2.0 Fast | low-latency | ~$0.048/s | fine for iteration |
| Seedance 2.0 Mini | lightweight 4–15 s clips | ~$0.030/s | cheapest pilot route |
| Seedance 2.5 | multimodal refs, ≤30 s, synced audio | ~$0.098/s | not needed yet |
| **Seedream 4.0** | text-to-image **and image editing** | ~$0.023–0.026 **/image** | **Adopt for photo touch-ups** (its strongest mode) |
| Seedream 4.5 / 5.0 Lite | 4K, precise text rendering | ~$0.029–0.034/image | later, if packaging text matters |
| **Meituan LongCat-Image** (6B) | text-to-image | MIT weights, free | **Do not self-host.** No GPU here |
| Meituan LongCat-Video-Avatar 1.5 | **audio-driven human** video | MIT weights | **Rejected on R3**, not on price |

Notes:

- **LongCat self-host math kills it at our scale:** ~**44 s of GPU compute per 1 s of
  finished video**, needing a **40 GB** card (A800-40GB) *after* INT8 quantisation + 8-step
  distill. An 82 s clip took just under an hour. A t3.medium autopilot box cannot touch
  this, and renting the card costs more than Seedance for any volume we will ever run.
- **Provider onboarding — use an aggregator, not Volcano direct.** Volcano Ark requires a
  Chinese mainland phone number + real-name verification; aggregators (fal / APIMart /
  LinkModel and similar) take a USD card. Credentials go in the **vault, never `.env`**.
- **Image/video models are per-generation priced, not per-token.** Do not reason about them
  with a token-cost model; pull current per-call rates before any batch. **Note:** Seedance's
  text rendering is not guaranteed — generated packaging text can mutate. See §7.1 QC.

---

## 6. Economics (why "generate 20, keep 2" is rational)

| Item | Cost |
|---|---|
| 15 s Seedance 2.0 clip (5 s grown motion + real footage) | **$0.45 – 0.90** |
| 2 Seedream 4.0 stills | $0.05 |
| **Per finished social post** | **< $1** |
| One-month cadence, 20 posts | **< $20** |

The economics only work *because* reject assets are cheap and never touch a provenance
field. Twenty generations produce two keeps; the eighteen rejects are deleted, unmanifested,
unmentioned.

---

## 7. Scenarios — worked examples ("what are we allowed to do")

This section is the operative one. The tables above tell you the vocabulary; this tells you
what to do on a Tuesday.

### 7.1 — Product-image-to-video  ⭐ RECOMMENDED FIRST PILOT

**The case:** the already-gate-approved `bar-81-dark-chocolate.jpg` (81% Brazil single
estate), animated via Seedance I2V into a 6 s slow push-in / subtle rotation.

- **Lane:** A. `derived_from: [sha256(bar-81-dark-chocolate.jpg)]`
- **People:** none. **Location claim:** none — "this is the physical product" is verifiably true.
- **Disclosure:** none required (it is the real bar, moved).
- **Why it's the cleanest case in the framework:** there is no *"did this really happen at
  this place, at this time"* question at all — only *"this is what the thing looks like, in
  motion."* That is strictly safer than farm b-roll, which carries both a location and a
  moment.
- **Extra QC (product only): label drift.** I2V can warp packaging text. Reuse the gate's
  proven label-reading ability — it independently read *"São Jorge, Bahia"* off a pin
  without being told what to look for — on the generated clip's frames and confirm the
  packaging text against the source still. If the label mutates, the asset is a **FAIL**
  even though it is Lane A. (The gate already `WARN`ed `bar-81` because its label says
  "81% Brazil Single Estate" and does not name the farm — that honesty is exactly how it
  will catch drift.)
- **Cost:** ~$0.30 for a 6 s clip.

### 7.2 — Farm b-roll from a MAP preview frame

**The case:** MAP holds `previews/fazenda-sao-jorge-bahia/IMG_1234.jpg`. Animate it 4 s.

- **Lane:** A. `derived_from: [sha256(original MOV)]` + the preview frame's own record.
- **People check first (R6).** If a person is identifiable → consent required, state
  `pending` until granted. If pending, **do not generate**; pick another frame.
- **Claim discipline:** the caption may say "on the farm in Bahia." It may **not** say
  "this is what happened" if the clip is `motion: extended` (R5.3).
- **Never** enter the farm gallery or the public YouTube channel (R1).

### 7.3 — Filler / joiner between two real clips (Envoy's R5 in practice)

**The case:** real clip A ends on a pan across drying racks; real clip B opens on a
fermentation box. You need ~3 s of connective tissue.

- **Correct (Lane A):** ffmpeg-extract clip A's **last real frame** → Seedance I2V, 3 s →
  `derived_from: [sha256(frame)]`, `motion: "extended"`, `motion_seconds: 3`. **No
  disclosure needed.** Caption stays silent or generic; it may not imply the extension is
  recorded footage.
- **Also correct (Lane A), but a *different operation* — read the caveat:** extend from
  clip B's **first real frame** instead, if that reads better.

  **Caveat — "generate forward" and "play reversed" are not the same thing.** Unless the
  provider genuinely supports **end-frame conditioning** (frame *N* as the terminal target,
  with the model solving for the frames that arrive there), the only way to get motion that
  *resolves into* clip B is: generate from B's first frame, then **play the result backward**
  in the edit. Seedance's documented conditioning is **first-frame (or first+last)** — so
  before relying on last-frame conditioning, verify it on the actual endpoint. Falling back
  silently to reverse-in-post changes what the clip *is*, not just how it is assembled.

  **Reverse-in-post only reads naturally for content without inherent directionality.**
  A pan, push-in, drift, or rise reverses fine — motion is roughly symmetric, and the eye
  reads it as a slow settle either way. **Do not reverse** anything with causal or physical
  directionality: pouring, falling, breaking, opening, unwrapping, steam rising, a knife
  cutting, liquid being absorbed. Reversed, these read as physically impossible and viewers
  catch it immediately — and it is a **silent** failure, because the manifest still says
  Lane A and the `derived_from` chain is still honest. The provenance is fine; the physics
  is wrong.

  **Practical rule:** if you cannot name the direction of the motion in the source frame in
  one word, do not reverse it — extend forward from clip A instead, and cut the seam.
- **Acceptable with label (Lane B):** no adjacent frame exists (clip A ends on a hard cut /
  black) → prompted transition. Now `derived_from: []`, `disclosure_required: true`, visible
  AI label.
- **Wrong:** prompting a "similar-looking" drying-rack clip and filing it as Lane A. The
  lane is determined by what the pixels were made from, not by how plausible they look.

### 7.4 — Touch-ups (stabilise / relight / colour / speed-ramp / trim)

**Always Lane A, no new rule needed.** Video touch-ups get exactly the treatment §7.1 gives
Seedream photo edits: a real sha256'd source, edited. Stabilisation, exposure correction,
white balance, speed ramps, trims, and noise reduction are *edits of a real capture* — the
same class as a crop. They do not need disclosure and they do not lose provenance.

Caveat: a speed-ramp that changes apparent pace is still an edit, not a fabrication — but it
may not be paired with a caption asserting a duration or a real-time rate ("in 40 seconds,
they broke 200 pods") unless that is literally true of the source.

### 7.5 — Lane B synthetics, done correctly

**The case:** an abstract cacao-pod texture for a blog header; a title card; a pattern
backdrop.

- `derived_from: []`, `disclosure_required: true`, visible AI label.
- Never farm gallery, never newsletter body (R4 gate), never QR/tree page.
- Fine on social and blog, labelled.

### 7.6 — Refused outright (do not build these)

| Attempt | Why it fails |
|---|---|
| Generated "farmer in Bahia" portrait or avatar | R3 + R6 + the 2026-11-10 incident |
| Generated packing room / fermentation facility presented as ours | R2 + R4: a fabricated provenance claim, the exact failure mode |
| Any generated asset uploaded to the YouTube farm channel | R1: poisons `yt_id` as a binding to a real event |
| Prompted filler filed as Lane A | §7.3 "wrong" — lane is determined by source, not plausibility |
| LongCat-Video-Avatar for "our farmer says hello" clips | R3; also 40 GB GPU / 44:1 compute |
| Generated photo in a newsletter body claiming supply chain | R4 hard FAIL, unchanged |

---

## 8. Manifest schema (`generated_media.json`)

One generated asset ⇒ one manifest row ⇒ one `index.json` entry with
`entity_type: "generated"`. Mirrors MAP's existing invariant.

```json
{
  "asset_id": "gen-2026-11-10-001",
  "lane": "A",
  "derived_from": ["<sha256 of source frame or photo>"],
  "source_type": "map_preview_frame | farm_media_photo | product_photo | prompt",
  "source_path": "previews/fazenda-sao-jorge-bahia/IMG_1234.jpg",
  "model": "seedance-2.0",
  "params": {"duration_s": 6, "aspect": "9:16", "resolution": "1080p"},
  "motion": "native | extended",
  "motion_seconds": 3,
  "people_present": false,
  "consent_ref": null,
  "disclosure_required": false,
  "destination": ["instagram", "tiktok"],
  "gate_result": "PASS",
  "cost_usd": 0.36,
  "created_at": "2026-11-10T00:00:00Z"
}
```

Invariants: `lane A ⇒ derived_from.length >= 1`; `lane B ⇒ derived_from == [] ∧
disclosure_required == true`; `motion == "extended" ⇒ motion_seconds <= 4 ∧ not citable as
recorded event`; `people_present == true ∧ lane == "A" ⇒ consent_ref is not null before
generation`.

---

## 9. Gate integration (the only code change this SOP requires)

Target: `go_to_market/scripts/verify_newsletter_images.py` (~40 lines, additive).

1. Read optional `asset_class` from the draft front-matter / sidecar: `photo | ai_edit |
   illustration`.
2. `ai_edit` of a real photo → still eligible for `PASS` (Lane A).
3. `illustration` → `PASS` only when a disclosure string is present in the caption/alt
   (Lane B, R4).
4. `--allow-generated` gates whether `ai_edit`/`illustration` are permitted at all for a
   given send; default **off**.
5. Unchanged: unlabelled generated-looking photo claiming supply chain → **hard FAIL**.

---

## 10. Pre-flight checklist (run before any inference call)

- [ ] **R2 search done** — MAP/manifest searched for an existing real asset that already
      does this job.
- [ ] **Lane determined** from the actual source, not from intent.
- [ ] **People check** — any identifiable person? If yes, `consent_ref` recorded, else stop (R6).
- [ ] **Data-residency / ToS reviewed** — real farm photos of real people go to a
      third-party inference API; that is a **consent** question, not a technical one, and
      MAP manifests carry GPS. Prefer crops/frames without people for third-party calls.
- [ ] **Credential in vault**, never `.env`.
- [ ] **Label-drift QC** for any product asset (§7.1).
- [ ] **Cost line** agreed (R: spend >$20 in a month needs a governor nod).

---

## 11. Pilot plan — $5, one product shot, no farm footage

| Step | Action | Gate |
|---|---|---|
| 1 | Provider credential (aggregator, USD card) → vault | governor approval |
| 2 | `bar-81-dark-chocolate.jpg` → Seedance I2V, 6 s, 9:16 | 1 asset, ~$0.30 |
| 3 | Gate the output + label-drift check vs source still | must PASS |
| 4 | Manifest row + `index.json` `entity_type: generated` | invariants §8 |
| 5 | One labelled social post; record actual cost | report back |

### ⛔ STEP 1 IS THE ONLY BLOCKING ITEM — and it is an account action, not engineering

**Status as of 2026-11-10: BLOCKED ON GOVERNOR.** Steps 2–5 are fully specified and every
prerequisite already exists (source photo sha256'd and gate-approved, manifest schema
defined, gate logic drafted). Step 1 cannot be performed by the autopilot under standing
policy:

- Opening a provider account is an **account/identity action with a payment instrument** —
  the same class as money movement. A governor must choose the route and put a card behind it.
- The credential then lands in the **vault**, never `.env`. Verified on 2026-11-10: the vault
  holds **zero** generation-related names — no Seedance, Seedream, fal, or Volcano entry.
  There is no route to execute against today.

**What a governor must supply to unblock** — pick one, then hand over the key:

| Route | What it needs | Note |
|---|---|---|
| **Aggregator** (fal / LinkModel / APIMart) | account + USD card | **Recommended** — no mainland-phone requirement |
| Volcano Ark direct | Chinese mainland phone + real-name verification | discouraged for this team |

**Do not work around this.** No scraping a free tier, no borrowing a key from another
project, no "just testing" call on someone else's account. The first inference call on a farm
or product asset is a data-residency decision as much as a billing one.

### Target placement — build the sample for a real slot

The pilot clip is **not** a generic test. It must be built against a specific upcoming
calendar row, so the output is usable and the cost line is attributable to a real post.
Upcoming Reels and their themes are enumerated in `tokenomics/SCHEMA.md` §5. Candidate slots
are raised with the governor rather than picked unilaterally, because the theme constrains
what the clip may claim — `Recipes & Rituals` and `Community Impact` want different assets
than a product hero shot does, and §7.1's product animation is only a natural fit for some
of them.

**Deliberately not in the pilot:** farm footage (consent + location questions), fillers/
joiners (needs two real clips sequenced first), any Lane B synthetic, reversal effects (§7.3
caveat).

---

## 12. Open questions

1. Where do generated blobs live — S3 `generated/` prefix (cheap, lifecycle-managed) or a
   GitHub repo like `farm-media-raw` (small files, but repo growth)? Leaning S3, since
   these are large and disposable.
2. Does disclosure live in the caption, the alt text, or a burnt-in corner watermark? Alt
   text is skippable by most viewers; a watermark is unambiguous but ugly. **Leaning: alt
   text + a platform-native AI label where the platform offers one.**
3. Retention: do Lane A derivatives expire with the post, or stay manifest-committed? MAP
   keeps everything; but derivatives are cheap to regenerate and their `derived_from` chain
   is what actually matters.
4. Cadence ownership — which loop owns the monthly generation quota, and is it capped in
   USD or in assets?

---

## 13. References

- `MEDIA_ARCHIVE_PIPELINE.md` — MAP parent runbook (archive of record, "Distribution ≠ archive", preview frames)
- `conventions/EDITORIAL_TONE.md` — voice for the captions this SOP governs
- `growth/CMO_SETH_GODIN.md` — smallest viable audience / stories over facts; the reason
  "real, specific, one farm" beats "generated, generic, plausible"
- `go_to_market/scripts/verify_newsletter_images.py` — the gate (PR #203)
- `sops/AGROVERSE_NEWSLETTER_WORKFLOW.md` — where the gate is invoked
- `sops/PAYOUT_REPORT_SOP.md` — path/format precedent for this file's home
