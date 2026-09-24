# CFR Anapu (cfr.truesight.me) — açaí content update

**Filed:** 2026-09-24, by Claude Anthropic (Envoy/planner), at Gary's request.
**Status:** in progress — PR1 merged 2026-09-24 (sha `ec876b3`); PR2 (live publish) pending governor go.
**Trigger:** Gary: *"Some students are planting açaí. https://cfr.truesight.me/ Can we update this?"*

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**

---

## 0. My reading of the ask (state it so it can be corrected — §5e)

| # | What I understand | Confidence |
|---|---|---|
| 1 | Some CRF Anapu students are now planting açaí (a native Amazonian fruit palm) in addition to the cacao-based agroforestry the site currently describes, and the public program page should reflect that. | High — directly stated |
| 2 | This is a **content update**, not a new feature — nobody's asked for a new submission flow or schema change. | Medium — inferred; flagged in §4 below as a related-but-separate gap I found while investigating, not assumed in scope |
| 3 | No açaí-specific photos, student names, or planting details have been shared yet — I checked the Telegram monitor log (`claude_telegram_monitor/messages.jsonl`) for "açaí"/"acai" and found nothing. | High — directly checked, not assumed |

**If row 1 or 2 is wrong, say so before PR1 starts.**

---

## 1. Pre-flight — current-state architecture (read live, 2026-09-24, not assumed)

### 1.1 Two repos, one page — and they've already drifted

`cfr.truesight.me` (repo `TrueSightDAO/cfr-anapu`, `gh-pages` branch) is a **vendored, byte-level
copy** of `truesight_me_beta/programs/crf-anapu/*` (established in
`handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md` §7) — re-vendoring is a **manual** step, not an automated
sync. Confirmed live this session: they've already diverged — `truesight_me_beta`'s
`manifest.json` has `"program_modes": ["cohort_credentialing", "sunmint_cohort"]` (added by the
in-flight `plans/CRF_ANAPU_SUNMINT_COHORT_PROPOSAL.md` work) while `cfr-anapu`'s copy still has
the older singular `"program_mode": "cohort_credentialing"`. Both repos' `description_md` are
otherwise byte-identical today. **This plan edits `truesight_me_beta` first (source of truth),
then re-vendors into `cfr-anapu`** — same two-step pattern as the original CRF Anapu build — and
opportunistically catches up the `program_mode(s)` drift in the same re-vendor pass, since it's
the same mechanical step and already known-stale.

### 1.2 What the page currently says about species

`manifest.json`'s `description_md` (both repos, identical): *"Cacao-based agroforestry, with
native shade and timber trees, is expressly supported."* This doesn't name açaí, and açaí isn't a
shade/timber tree — it's a fruit palm — so the current copy doesn't clearly cover it. The
`tagline` ("native Amazonian trees") is generic enough to already technically include it, but
nothing on the page calls it out.

### 1.3 The submission form itself already half-supports açaí — worth knowing, not fixing here

`sunmint_beta/index.html`'s tree-planting species dropdown (lines 260-263) lists only `Cacao -
Criolla` / `Trinitario` / `Forestero` / `Other (specify)`. A student **can** already log an açaí
planting today via "Other (specify)" — nothing is broken or blocked — but açaí isn't a named
first-class option. This is a **shared SunMint-wide form**, not CRF-Anapu-specific, so adding a
dedicated option is out of scope for this plan; flagged in §4.

### 1.4 The credential-tree-link section has a real, separate hardcoded-species bug

While tracing how a planted tree's species would ever surface on a student's credential page, I
found `programs/*/credentials` pages (via the shared `js/program-shell.js:525-527`) hardcode:
`'<p>A cacao tree was issued in honour of this credential.</p>'` — unconditionally, regardless of
actual species, for **every** credentialing program using this shell (Butterfly Effect Club, Ivy
Yoga, CRF Anapu, any future partner). This was already slightly wrong before açaí ever entered
the picture; it becomes more visibly wrong the moment any açaí-tree credential renders. This is a
shared-code fix with a blast radius beyond CRF Anapu — flagged in §4, not in this plan's scope.

---

## 2. Authorization envelope (§5e)

| Surface | Envelope |
|---|---|
| `truesight_me_beta/programs/crf-anapu/manifest.json` copy edit | Pre-authorized by this request — beta repo, feature branch + PR, self-mergeable per standing `*_beta` authority. |
| Re-vendoring into `cfr-anapu` (`gh-pages`, live prod subdomain) | Pre-authorized — this domain has no separate prod/beta split (per §1.1, it *is* the live site); treat the re-vendor push itself as the deploy step and do a live URL check immediately after (§5). |
| §4's two flagged, out-of-scope items | **Not authorized here** — informational only, needs Gary's go before either gets its own plan. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Update `programs/crf-anapu/manifest.json`'s `description_md`: name açaí explicitly alongside cacao — e.g. *"Cacao-based agroforestry, with native shade and timber trees, is expressly supported — açaí, a native Amazonian fruit palm, is also being planted by students as of September 2026."* (exact wording open — see §5). Bump `last_reviewed`. **Shipped 2026-09-24, Option A:** appended only *"Students are also planting **açaí**, a native Amazonian fruit palm."* — no date, no intercropping claim. | `truesight_me_beta` |
| **PR2** | Re-vendor the updated `manifest.json` into `cfr-anapu` (`gh-pages`), same pass, also catch up `program_mode` → `program_modes: [cohort_credentialing, sunmint_cohort]` to close the drift found in §1.1. Live-check `https://cfr.truesight.me/` after push (§5c — this push *is* the prod deploy for this domain). | `cfr-anapu` |
| **PR3 (parked, not triggered)** | Once real açaí-planting photos/details exist: ingest via the established MAP pipeline (`farm_media_manifests`, `entity_type: program`, cross-indexed) → add to `programs/crf-anapu/media.json` gallery → re-vendor into `cfr-anapu`, same two-repo pattern as PR1/PR2 — see `handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md` §4/§5 for the exact precedent (that's how the original site-visit photos were added). **No photos exist yet** (checked, §0 row 3) — this unit stays parked until Gary or the CEPOTX contact supplies media. | `farm_media_manifests`, `truesight_me_beta`, `cfr-anapu` |

---

## 4. Flagged, out of scope for this plan

1. **SunMint species dropdown has no dedicated "Açaí" option** (§1.3) — students can already log it via "Other," so nothing is broken; a first-class option would just be cleaner. Cross-program (`sunmint_beta`) change, needs its own scoping if Gary wants it.
2. **Hardcoded "A cacao tree was issued…" credential text** (§1.4) — wrong for any non-cacao species, across every program using `js/program-shell.js`, not CRF-specific. Worth fixing (e.g. read species from the tree's own record and vary the sentence, or genericize the wording), but it's shared code with a wider blast radius than this plan's scope.

---

## 5. Resume tracker

> **RESUME HERE → PR2.** PR1 is complete (2026-09-24): Gary selected **Option A** in thread 35888 —
> açaí named additively, no unsourced date, and the "intercropped" phrasing deliberately withheld
> (still an open factual question). PR1 merged, sha `ec876b3`, contribution reported.
>
> PR2 is the **live publish** step: re-vendor the updated `manifest.json` into `cfr-anapu@gh-pages`
> and catch up the `program_mode` → `program_modes` drift (§1.1) in the same pass. For this domain
> the push *is* the prod deploy, so run the §6 UAT live check (`https://cfr.truesight.me/`, page 200
> + açaí sentence visible) immediately after.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☑ | ☐ |
| PR1 (beta copy edit) | ☑ | ☑ | ☑ |
| PR2 (re-vendor to cfr-anapu, live) | ☐ | — | ☐ |
| PR3 (photo ingestion) | parked | — | — |

---

## 6. UAT

| Step | What to expect | Acceptance criterion |
|---|---|---|
| 1 | `https://cfr.truesight.me/` after PR2 | Page loads 200, new açaí sentence visible in the description section |
| 2 | Cross-check `truesight_me_beta/programs/crf-anapu/` beta preview | Same copy, confirms source-of-truth and vendored copy match again (closes the §1.1 drift too) |

---

## 7. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first).
