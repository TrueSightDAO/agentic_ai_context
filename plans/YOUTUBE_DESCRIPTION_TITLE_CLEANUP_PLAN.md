# YouTube Description & Title Cleanup — Execution Roadmap

**Status:** Complete — all 6 units landed 2026-09-01; live descriptions pushed + verified 73/73 (PRs #263/#266/#267/#881).
**Owner:** Gary Teh.
**Requested by:** Gary Teh, 2026-09-01.
**Repo:** `agroverse_shop` (scripts), `agentic_ai_context` (this plan + SOP update).
**Auto-start:** no — wait for governor's "go for it" in the handoff topic before touching live YouTube metadata.

**Goal:** Fix unhelpful YouTube video descriptions across the Agroverse channel (68 videos in
`youtube_videos.json`) by pushing the same **cleaned, Grok-polished transcript** already used for blog
posts — instead of the raw, error-ridden Whisper ASR text currently live — and clean up any titles that
are still placeholder-style (e.g. raw filename fragments like "Export: Full HD 1081 (newer").

> `OPERATING_INSTRUCTIONS.md` §5 tracked roadmap. §5a: **one PR per execution turn, then stop.**

---

## 0. Root cause (confirmed 2026-09-01, verified against live API + source)

- `agroverse_shop/scripts/youtube_batch_incoming.py`'s `description_for_video()` (line ~178) builds the
  YouTube description from the **raw manifest transcript** (`v.get("transcript")` — unpolished
  `faster-whisper` ASR output) **at upload time only**.
- Blog posts instead use `transcript_publish_helpers.clean_transcript()` + optional
  `grok_transcript_polish.py` polish (see `sops/DOWNLOADS_MEDIA_TO_AGROVERSE.md` §A.4) — so the blog reads
  well but the live YouTube description does not.
- There is a re-sync script for **titles** (`youtube_update_video_titles.py`, run per §A.7 of the SOP
  whenever `youtube_videos.json` changes) but **no equivalent re-sync for descriptions** — so raw-ASR
  descriptions from upload time are never revisited, even as the blog pipeline's transcript quality
  improved over time.
- Verified live via YouTube Data API (`videos.list`, part=snippet) on 4 sample videos — all 4 have raw
  ASR artifacts in their descriptions (e.g. "Fili Marsh" for a mis-heard name, "being the police, episode
  12" as a garbled intro line). This is not a one-off; it's systemic across the channel.
- `youtube_videos.json` currently has **no `description` field at all** per entry (only `video_id`, `url`,
  `embed_url`, `title`, `uploaded_via`) — descriptions live only on YouTube itself, invisible to the repo.
- Titles: `youtube_grok_project_titles.py` already exists to propose better titles via Grok (`--scope
  placeholder` targets exactly the ugly ones), but hasn't been re-run against the current channel state.

---

## 1. Sequenced plan — one PR per execution turn (§5a)

| Unit | Scope | Gate |
|------|-------|------|
| **PR1** | Add a `description` field to `youtube_videos.json` for all 68 entries, generated from the **cleaned + Grok-polished** transcript (same pipeline as blog posts, not raw ASR) + a link to the specific blog post URL for that episode (current descriptions only link to the generic agroverse.shop homepage) + the existing hashtag/CTA footer. **No live push yet** — this PR only updates the local JSON so it can be reviewed. | — |
| **PR2** | Write `agroverse_shop/scripts/youtube_update_video_descriptions.py` (sibling to `youtube_update_video_titles.py`, same `videos().update(part="snippet")` pattern) that pushes the new `description` field to YouTube. Run in `--dry-run` mode only this turn — print the before/after diff for all 68, do not push live. | — |
| **PR3** | Post a **sample of 5 before/after title+description pairs** (mix of the worst offenders, e.g. the "Fili Marsh" and "being the police" ones, plus 2–3 typical ones) to the handoff Telegram topic for governor review. | **Review gate — do not push live until governor approves the sample.** |
| **PR4** | After governor approval: run `youtube_update_video_descriptions.py` for real against all 68 videos. Verify via a fresh `videos.list` API call (not self-report) that descriptions actually changed live. | Requires PR3 approval first. |
| **PR5** | Run `youtube_grok_project_titles.py --scope placeholder --push-youtube` (or `--scope all` if governor wants a full pass, not just placeholder-style ones) to clean up titles that are still raw filename fragments. Dry-run first, then apply — same review pattern as PR3/PR4 if the diff looks non-trivial. | — |
| **PR6** | Update `agentic_ai_context/sops/DOWNLOADS_MEDIA_TO_AGROVERSE.md` §A.7 so **description push (using the polished transcript, not raw)** becomes a permanent step in the pipeline for all future uploads — either by fixing `description_for_video()` in `youtube_batch_incoming.py` to call the same clean/polish helpers before upload, or by adding "run `youtube_update_video_descriptions.py`" to the end-to-end checklist alongside the existing title-update step. Prevents this gap from recurring for new videos. | — |

---

## 2. Pre-flight facts (§5d)

- YouTube OAuth: `agroverse_shop/scripts/youtube_credentials.json` / `youtube_token.json`, scope
  `youtube.force-ssl` required for `videos.update` (same as title updates already use). If `invalid_scope`
  or `RefreshError`, delete `youtube_token.json` and run `youtube_oauth_reauthorize.py`, sign in as channel
  owner (e.g. `admin@truesight.me`).
- Description length limit: YouTube caps at 5000 chars — `description_for_video()` already handles
  truncation; reuse that logic.
- `youtube_videos.json` is the checked-in source of truth (per SOP §A.7) — changes there are what drive
  the push scripts, not manual YouTube Studio edits.
- Manifests with the original raw + source transcripts live under `agroverse_shop/docs/incoming_videos_*/manifest.json`.
- `transcript_publish_helpers.clean_transcript()` and `grok_transcript_polish.py` (needs `GROK_API_KEY`,
  env or `market_research/.env`) are the existing, proven polish steps — reuse them, don't write new
  cleanup logic.

---

## 3. Authorization envelope (§5e)

| Surface | Envelope |
|---------|----------|
| `youtube_videos.json` local edits (PR1), new script + dry-run (PR2) | Pre-authorized — no live YouTube changes yet. |
| Live YouTube description push (PR4), live title push (PR5) | **Review gate (PR3) required first** — this is public-facing content on a real channel; governor reviews a sample before any bulk push. |
| SOP doc update (PR6) | Pre-authorized — documentation only. |

---

## 4. Resume tracker

> **STATUS: COMPLETE** — all 6 units landed 2026-09-01. → PR1.**

| Unit | Built | Merged |
|------|:----:|:------:|
| PR1 (add description field, local only) | ✅ | ✅ |
| PR2 (description push script, dry-run only) | ✅ | ✅ |
| PR3 (sample for governor review) | ✅ | — |
| PR4 (live description push, post-approval) | ✅ | ✅ |
| PR5 (title cleanup pass) | ✅ | ✅ |
| PR6 (SOP update — prevent recurrence) | ✅ | ✅ |

---

## 5. Contribution reporting

Report DAO contribution after PR4 and PR5 land (the live-impact units), per `dao_client` CLI, signed as
whichever identity is executing (Sophia Truesight for this handoff).
