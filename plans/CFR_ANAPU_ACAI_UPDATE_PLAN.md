# CFR Anapu (cfr.truesight.me) — açaí content update

**Filed:** 2026-09-24, by Claude Anthropic (Envoy/planner), at Gary's request.
**Status:** ✅ **COMPLETE 2026-09-24.** PR1 (`ec876b3`), PR2 (`24ae6d6`), PR2-b (prod promotion, `5de3114`), and the follow-on **açaí dropdown option** (§4 item 1 — PRs `sunmint_beta#86` + `cfr-anapu#14`) all merged, UAT-passed. See §5.
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

> ⚠ **Correction (Sophia, live re-read 2026-09-24) — PR2 as written cannot achieve its own §6 UAT.**
> Re-verified against both live sites and both repos. Four premises in §1.1/§6 do not hold:
>
> 1. **The `program_mode`→`program_modes` drift is already closed.** `cfr-anapu@gh-pages`'s root
>    `manifest.json` *already* carries `program_modes: ["cohort_credentialing", "sunmint_cohort"]`
>    (commit `3bfe7af`, "CRF Anapu PR5 mirror (#6)", 2026-09-17). PR2's drift clause is a no-op.
> 2. **`cfr.truesight.me/` (root) is the SunMint farmer *app*** ("Sunmint - TrueSight DAO"; nav =
>    Registrar Plantio / Monitorar Árvore / …) — it has **no description section at all**. The plan's
>    §6 UAT ("açaí sentence visible at `cfr.truesight.me/`") targets a page that never renders
>    `description_md`.
> 3. **The cfr program landing page (`/program/`) cannot load any manifest.** `program/index.html`
>    calls `TrueSightProgramShell.init({ manifestPath: './manifest.json' })` → fetches
>    `/program/manifest.json`, which **404s** (that path has never existed in the repo; confirmed via
>    `git log --all -- program/manifest.json`). So re-vendoring the root `manifest.json` would **not**
>    surface the açaí copy at `cfr.truesight.me/program/` — the page needs its `manifestPath` changed
>    to `../manifest.json` (as `credentials/index.html` already does) *or* its own
>    `program/manifest.json`.
> 4. **The real, working CRF Anapu program page is `https://truesight.me/programs/crf-anapu/`**,
>    served by **`truesight_me_prod`** (CNAME `truesight.me`; live manifest sha `fb5972584742` ==
>    prod `main`). It renders `description_md` correctly. Prod is still **pre-PR1** (no açaí,
>    `last_reviewed` 2026-09-11); beta `main` has PR1 (`9bd6198`, `last_reviewed` 2026-09-24).
>    Publishing there is a **beta→prod promotion** — a production gate needing explicit governor
>    approval, not a `*_beta` self-merge.
>
> **Net:** no single "re-vendor the root `manifest.json` into `cfr-anapu`" step makes the açaí copy
> appear on any governor-facing page. PR2 must be re-scoped with Gary before execution — see the
> revised §2 envelope and §3 units.

> ⚠️ **Correction 1.1-b (Sophia, live re-read 2026-09-24, during execution) — `cfr-anapu`'s Pages source is `main`, not `gh-pages`.**
> `gh api repos/TrueSightDAO/cfr-anapu/pages` → `source.branch = main`, `build_type = legacy`; the last
> Pages build before this fix was 2026-09-17T19:02Z — exactly the live `last-modified`. So `gh-pages`
> is **not served** at cfr.truesight.me: the first PR2 attempt (PR #12, merged into `gh-pages`) was a
> **silent no-op live**. The working fix landed on **`main`** (PR #13, sha `24ae6d6`), which triggered
> the real Pages rebuild. Correct §1.1's premise ("`cfr.truesight.me` … `gh-pages` branch") accordingly —
> the served branch is `main`. (The two branches had drifted in content; they now match on the açaí copy.)

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
| Re-vendoring into `cfr-anapu` (live `cfr.truesight.me`) | ~~GATE~~ **PASSED 2026-09-24 (Gary: "both").** Any push *is* a live publish. Applied to the served branch **`main`** (PR #13, sha `24ae6d6`) — see §1.1-b correction (`gh-pages` is not served). Includes the `manifestPath` `./`→`../` fix so the copy renders at `/program/`. |
| Promoting `truesight_me_beta` → `truesight_me_prod` (`truesight.me/programs/crf-anapu/`) | ~~GATE~~ **PASSED 2026-09-24 (Gary: "both").** `sync_beta_to_prod` merge `5de3114`, ledger `deploy_20260924T170044Z_truesight-me-prod`, no conflict, CNAME preserved. This is where `description_md` renders publicly. |
| §4's two flagged, out-of-scope items | **Not authorized here** — informational only, needs Gary's go before either gets its own plan. |

---

## 3. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Repo |
|---|---|---|
| **PR0** | This roadmap. | `agentic_ai_context` |
| **PR1** | Update `programs/crf-anapu/manifest.json`'s `description_md`: name açaí explicitly alongside cacao — e.g. *"Cacao-based agroforestry, with native shade and timber trees, is expressly supported — açaí, a native Amazonian fruit palm, is also being planted by students as of September 2026."* (exact wording open — see §5). Bump `last_reviewed`. **Shipped 2026-09-24, Option A:** appended only *"Students are also planting **açaí**, a native Amazonian fruit palm."* — no date, no intercropping claim. | `truesight_me_beta` |
| **PR2 — SHIPPED 2026-09-24** | Re-vendored root `manifest.json` into `cfr-anapu` **and** fixed `program/index.html`'s `manifestPath` (`./` → `../`) so the copy renders at `cfr.truesight.me/program/`. **Branch correction:** applied to **`main`** (Pages serves `main`, not `gh-pages` — §1.1-b); PR #13 sha `24ae6d6`, UAT ✅. (Prior PR #12 on `gh-pages` was a no-op.) | `cfr-anapu` |
| **PR2-b — SHIPPED 2026-09-24** | Promoted `truesight_me_beta` → `truesight_me_prod` so the açaí copy reaches `https://truesight.me/programs/crf-anapu/`. `sync_beta_to_prod` merge `5de3114`, ledger `deploy_20260924T170044Z_truesight-me-prod`, UAT ✅. | `truesight_me_prod` |
| **PR3 (parked, not triggered)** | Once real açaí-planting photos/details exist: ingest via the established MAP pipeline (`farm_media_manifests`, `entity_type: program`, cross-indexed) → add to `programs/crf-anapu/media.json` gallery → re-vendor into `cfr-anapu`, same two-repo pattern as PR1/PR2 — see `handoffs/CRF_ANAPU_MEDIA_TASK_PLAN.md` §4/§5 for the exact precedent (that's how the original site-visit photos were added). **No photos exist yet** (checked, §0 row 3) — this unit stays parked until Gary or the CEPOTX contact supplies media. | `farm_media_manifests`, `truesight_me_beta`, `cfr-anapu` |

---

## 4. Flagged, out of scope for this plan

1. **✅ SHIPPED 2026-09-24 — SunMint species dropdown now has a first-class "Açaí" option** (§1.3). Gary asked for it explicitly ("We need to have Acai as an option in the dropdown on this page https://cfr.truesight.me/"). Landed as a **3-line additive change** (new `<option value="Açaí" data-i18n="speciesAcai">` + `speciesAcai` in both `pt` and `en` i18n blocks) in **both** repos: source of truth `sunmint_beta` (#86, sha `1b1c10b` — also live on `beta.sunmint.truesight.me`) **and** the served vendor copy `cfr-anapu@main` (#14, sha `f68785e`) — kept in sync so the next `sync_sunmint_app.py` re-vendor is a no-op. Safe/additive: downstream species capture is free text (`process_tree_planting_telegram_logs.js` → `extractSpecies()` = `/- Species: (.+)$/m`, no allowlist). UAT ✅: `https://cfr.truesight.me/` serves 5 options with Açaí 4th + `speciesAcai` in both languages. **Note:** `cfr.truesight.me/` root is a vendored copy of `sunmint_beta/index.html` (only `og:url` differs) — and, like the manifest, `vendor.json` names the wrong target branch (`gh-pages`); the served branch is `main`.
2. **Hardcoded "A cacao tree was issued…" credential text** (§1.4) — wrong for any non-cacao species, across every program using `js/program-shell.js`, not CRF-specific. Worth fixing (e.g. read species from the tree's own record and vary the sentence, or genericize the wording), but it's shared code with a wider blast radius than this plan's scope.

---

## 5. Resume tracker

> **RESUME HERE → COMPLETE — both surfaces shipped & UAT-passed 2026-09-24 (Gary chose Option 3 "both").**
> PR1 complete (sha `ec876b3`).
>
> - **Option 1 — `cfr.truesight.me/program/` LIVE.** PR #13 on **`main`** (sha `24ae6d6`): re-vendored
>   root `manifest.json` (açaí + `last_reviewed` 2026-09-24) **and** fixed `program/index.html`'s
>   `manifestPath` `./`→`../` (was 404). UAT ✅: Pages rebuilt from `main` 16:59Z; `/manifest.json`
>   serves the açaí sentence; `/program/` references `../manifest.json`. (Prior PR #12 on `gh-pages` was
>   a silent no-op — see §1.1-b.)
> - **Option 2 — `truesight.me/programs/crf-anapu/` LIVE.** `sync_beta_to_prod(truesight_me_prod)` →
>   merge `5de3114`, ledger `deploy_20260924T170044Z_truesight-me-prod`, no conflict, CNAME `truesight.me`
>   preserved. UAT ✅: prod manifest serves the açaí sentence; page 200; apex 200.
>
> **No remaining units.** PR3 (photo ingestion) stays parked until real açaí media exists.

| Unit | Built | Merged | Contribution reported |
|---|:---:|:---:|:---:|
| PR0 (this roadmap) | ☑ | ☑ | ☐ |
| PR1 (beta copy edit) | ☑ | ☑ | ☑ |
| PR2 (re-vendor to cfr-anapu, live) | ☑ | ☑ | ☑ |
| PR2-b (beta→prod promotion) | ☑ | ☑ | ☑ |
| PR3 (photo ingestion) | parked | — | — |
| PR4 (§4 item 1 — açaí dropdown option) | ☑ | ☑ | ☐ |

---

## 6. UAT

| Step | What to expect | Acceptance criterion |
|---|---|---|
| 1 | `https://truesight.me/programs/crf-anapu/` after prod promotion | Page loads 200, açaí sentence visible in the description section — **this is the working public page** (Option 2) |
| 2 | `https://cfr.truesight.me/program/` after the cfr fix | Page loads 200, açaí sentence visible — **requires the `manifestPath` fix, not just a manifest re-vendor** (Option 1) |
| 3 | Cross-check `truesight_me_beta` (`main`) vs the published copy | Same copy, confirms source-of-truth and published copy match (`last_reviewed` 2026-09-24) |

**UAT results (2026-09-24) — all PASS:**
- **Step 1 ✅** `truesight.me/programs/crf-anapu/manifest.json` → `last_reviewed 2026-09-24`, açaí present; page 200; apex `truesight.me/` 200 (CNAME intact).
- **Step 2 ✅** `cfr.truesight.me/manifest.json` → `last_reviewed 2026-09-24`, açaí present; `/program/` references `../manifest.json` (Pages rebuilt from `main` 2026-09-24T16:59Z).
- **Step 3 ✅** `truesight_me_beta@main` and both published copies all show `last_reviewed 2026-09-24` with the açaí sentence.

---

## 7. Contribution reporting

Per `OPERATING_INSTRUCTIONS.md` §6, report each merged PR via `dao_client`
(`truesight-dao-report-ai-agent-contribution`, `--dry-run` first).
