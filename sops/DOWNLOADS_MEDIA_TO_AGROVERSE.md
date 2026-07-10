# Downloads media → Agroverse blog (and YouTube)

Canonical heuristics when the user places **videos** or **images** in **`~/Downloads`** (or another local folder) for inclusion on **agroverse.shop**—especially the blog.

**Repo:** `agroverse_shop/`  
**Credentials:** YouTube + Google: see `agroverse_shop/docs/SECURITY.md` and **`agentic_ai_api_credentials`** (never commit tokens). **Grok (transcript polish):** `GROK_API_KEY` or sibling `market_research/.env` (see below).

---

## A. Videos (field clips, Bean to Bliss, projects)

### Goal

Turn local MP4s into: (1) optional **YouTube** uploads with sensible titles, (2) **blog posts** with embed + readable transcript, (3) **card/OG thumbnails** from the first video frame where applicable.

### Pipeline (order matters)

1. **Analyze + transcribe + dedupe metadata**  
   - Script: `agroverse_shop/scripts/analyze_incoming_videos.py`  
   - Example (incremental):  
     `python3 scripts/analyze_incoming_videos.py --input ~/Downloads --output docs/incoming_videos_2026-04 --glob '*.MP4' --reuse-from docs/incoming_videos_2026-04/manifest.json --model tiny`  
   - **Requires:** `ffmpeg`, `faster-whisper`, `Pillow`, `imagehash` (see script header).  
   - **Output:** `manifest.json` per file: duration, resolution, **anchor/timeline perceptual hashes** (frame sampling for dedupe—not semantic “what’s in the frame” ML captions), **Whisper transcript**, duplicate fields.

2. **Duplicate policy**  
   - `youtube_upload_recommended: false` = duplicate (exact byte match or strong visual near-duplicate). **Do not upload** duplicates to YouTube.  
   - Canonical file is chosen per duplicate group in the manifest README.

3. **YouTube upload**  
   - Script: `agroverse_shop/scripts/youtube_batch_incoming.py`  
   - Reads manifest + **`scripts/incoming_upload_skips.json`** (basenames to skip).  
   - Skips if basename already in **`scripts/youtube_videos.json`**.  
   - **Default:** only **story-grade** clips (≥ **45 s** and ≥ **80** transcript words). Use **`--include-non-story`** for shorter/music-forward clips.  
   - **Titles:** content-aware (transcript helpers + Bean/B2B labels), not raw filenames.  
   - Optional **`--captions`** (needs OAuth scope + may require deleting `youtube_token.json` once to re-consent—see script docstring).

4. **Blog posts + listing cards**  
   - Script: `agroverse_shop/scripts/generate_video_transcript_blog_posts.py`  
   - Needs: manifest path (default `docs/incoming_videos_2026-04/manifest.json`), **`scripts/youtube_videos.json`**.  
   - Regenerates Bean episode pages + **story** posts (duration/transcript thresholds per script).  
   - **No boilerplate** “Watch on YouTube below…” intro; body starts with embed then **Transcript**.  
   - **Transcript quality:** local `transcript_publish_helpers.clean_transcript` then optional **Grok** polish (`scripts/grok_transcript_polish.py`) for longer text; cache **`scripts/transcript_grok_polish_cache.json`**. Key: **`GROK_API_KEY`** env or **`../market_research/.env`** from `agroverse_shop/scripts/`.

5. **Thumbnails**  
   - **`scripts/video_poster_thumb.py`**: first-frame (or fall back to YouTube poster) → **`assets/images/blog/transcript-thumbs/{slug}.jpg`**.  
   - Used in post **og:image** / **twitter:image** and blog grid cards for those posts.

6. **Social preview (WhatsApp / Facebook)**  
   - After regenerating posts or editing **`blog/index.html`** card images, run **`python3 scripts/sync_post_open_graph_images.py`** so each post’s **`og:image`** and **`twitter:image`** match the same **relative** `src` as the listing card, and **`og:image:width` / `og:image:height`** are set from the local JPEG.  
   - Set **`AGROVERSE_PUBLIC_ORIGIN`** when building for a host where assets are available (e.g. **`https://beta.agroverse.shop`** if production **`www`** has not yet deployed new **`transcript-thumbs/`** files—crawlers require HTTP **200** on the image URL).  
   - **`generate_video_transcript_blog_posts.py`** also respects **`AGROVERSE_PUBLIC_ORIGIN`** for canonical / Open Graph URLs and always attaches image dimensions when the card path exists under **`assets/`**.

7. **Push title updates to YouTube** (mandatory whenever manifest titles drift)  
   - **`scripts/youtube_videos.json`** is the checked-in source of truth for each uploaded video’s **canonical title** (including ` | Agroverse`, max 100 chars). It is updated when you run **`generate_video_transcript_blog_posts.py`** (`sync_youtube_mapping_titles`) and when you edit titles manually.  
   - **YouTube Studio titles do not auto-sync.** After any change to that JSON—or after regenerating blog posts—run:  
     `python3 scripts/youtube_update_video_titles.py --dry-run` then `python3 scripts/youtube_update_video_titles.py`  
     so the **live YouTube title** matches the blog/H1 naming (iframe `title` in HTML is generated to match the post H1; the API updater pushes the snippet titles from the JSON).  
   - **OAuth scope:** title updates need **`https://www.googleapis.com/auth/youtube.force-ssl`**. Upload-only tokens will fail with **`invalid_scope`** or **`RefreshError`** on refresh. **Fix:** remove the stale token and re-authorize:  
     `rm scripts/youtube_token.json`  
     `python3 scripts/youtube_oauth_reauthorize.py`  
     Sign in as the channel owner (e.g. **`admin@truesight.me`**), then rerun **`youtube_update_video_titles.py`**.  
   - **`youtube_oauth_reauthorize.py`** lives next to the other YouTube helpers under **`agroverse_shop/scripts/`** (same Desktop client as **`youtube_credentials.json`**). See also **`agroverse_shop/docs/SECURITY.md`**.

8. **Legacy intro cleanup** (optional one-off)  
   - `scripts/strip_transcript_boilerplate_intros.py` removes old disclaimer `<p>` blocks from `post/*/index.html`.

### End-to-end checklist (do not skip)

Use this after **upload** and/or **blog regen** so you do not ship stale YouTube titles or broken OAuth:

1. `generate_video_transcript_blog_posts.py` (updates posts, **`youtube_videos.json`**, blog cards; runs **`sync_post_open_graph_images.py`** at the end).  
2. **`youtube_update_video_titles.py`** — dry-run, then apply — so **YouTube** matches the JSON.  
3. If step 2 errors on token/scope: **`youtube_oauth_reauthorize.py`**, then repeat step 2.

### What future agents should not do

- Do not commit **`youtube_credentials.json`**, **`youtube_token.json`**, or API keys.  
- Do not upload rows with **`youtube_upload_recommended: false`** unless the user explicitly overrides.  
- Do not assume **Grok** ran: without a key, posts still build using local cleanup only.  
- Raw video in **Downloads** is **not** git-tracked; manifests and small assets in-repo are.

---

## B. Images (Downloads → blog or pages)

### Existing heuristics in this context (in-repo, not Downloads-specific)

There is **no** dedicated automation that watches **`~/Downloads`** for images and wires them into the blog. What **is** documented elsewhere:

- **Blog listing cards (`blog/index.html`):** thumbnails MUST be **`assets/images/blog/listing-640w/{post-slug}.jpg`**, built by **`agroverse_shop/scripts/sync_blog_listing_thumbnails.py`** (640px max edge, ~q80). Source selection: prefer the post’s **first real in-body** `/assets/images/...` image; text-only posts use curated **`bahia-photo-library`** or other repo assets; avoid duplicate hashes/URLs. See **`PROJECT_INDEX.md`** (agroverse_shop row), **`WORKSPACE_CONTEXT.md`** §4, **`agroverse_shop/.cursor/rules/blog-listing-images.mdc`**.

### Recommended workflow when the user adds images to Downloads

1. **Ingest** — Copy (or export) into a sensible path under **`agroverse_shop/assets/images/`** (e.g. `blog/…`, `farms/…`, `shipments/…`). Use **web-facing paths** in HTML: `/assets/images/...`.  
2. **Size** — Prefer reasonable JPEG/WebP sizes for web; avoid committing enormous originals unless intentional.  
3. **Reference** — Add `<img>` (or hero) in the relevant **`post/<slug>/index.html`** (or other page) with correct relative or absolute paths.  
4. **Listing sync** — Run **`python3 scripts/sync_blog_listing_thumbnails.py`** so **`listing-640w/{slug}.jpg`** matches the new in-body image policy.  
5. **Uniqueness** — If two posts would share the same listing image file or perceptual duplicate, pick a distinct **`bahia-photo-library`** or other asset (same rules as blog-listing-images).

### Optional checks

- If the user says “use the photo I put in Downloads,” resolve the **actual filename** under `~/Downloads`, then **copy into `assets/`** as above—do not hotlink to `file://` or user-home paths in deployed HTML.

---

## C. Related docs

- `agroverse_shop/docs/incoming_videos_2026-04/README.md` (generated after analyze)  
- `agroverse_shop/docs/SHUAR_DESIGN_YOUTUBE_UPLOAD.md` (example manual upload from Downloads)  
- `agroverse_shop/docs/SECURITY.md` (credential files; YouTube OAuth reauthorize)  
- `video_editor/` — separate Flask/Grok tooling for Shorts; not the same as the manifest → blog pipeline above.

---

*When this workflow changes (new scripts or defaults), update this file and **`CONTEXT_UPDATES.md`**, and cross-link from **`PROJECT_INDEX.md`** / **`WORKSPACE_CONTEXT.md`** if needed.*
