# Blog post publishing workflow

This document describes the end-to-end process for publishing a blog post on truesight.me/blog, including the optional audio narration step.

## 1. Write the post

- Follow the editorial tone guide in `EDITORIAL_TONE.md`
- Posts live in `truesight_me_beta/blog/posts/` as static HTML files
- Byline format: `by Sophia Truesight (TrueSight DAO Autopilot)` or `by Gary Teh, long time contributor`
- Include OG meta tags for social sharing

## 2. Create a PR to beta

- Branch from `main` on `truesight_me_beta`
- Open a PR with the new HTML file
- Merge to beta for review

## 3. Generate audio narration (optional but recommended)

For posts authored by Sophia Truesight, generate an audio narration so readers can listen to the post.

### Prerequisites

- `edge-tts` Python package is installed on the `dao_protocol` host
- `ffmpeg` is installed for combining audio chunks
- The voice `en-US-AriaNeural` is available (this is the same voice used for Telegram responses)

### Steps

1. **Extract the text** from the blog post HTML (strip tags, decode entities)
2. **Write a plain-text version** of the post to a file on `dao_protocol` (e.g., `/tmp/post_my-post.html`)
3. **Generate the audio** using edge-tts:

```bash
# On dao_protocol:
python3 -m edge_tts --voice en-US-AriaNeural --text "$(cat /tmp/post_text.txt)" --write-media /tmp/tts_output.mp3
```

For long posts (over ~2500 chars), split into chunks on sentence boundaries, generate each chunk, then combine with ffmpeg:

```bash
ffmpeg -y -f concat -safe 0 -i /tmp/chunks.txt -c copy /tmp/tts_final.mp3
```

4. **Upload the MP3** to both beta and prod repos:
   - Path: `assets/blog/narration-<post-slug>.mp3`
   - Use the GitHub Contents API with `DAO_PROTOCOL_GITHUB_PAT`
   - Upload to both `truesight_me_beta` and `truesight_me_prod`

5. **Add the audio player** to the blog post HTML. Insert this block right after the opening `<div dir="ltr">` tag:

```html
<div style="background: var(--bg-secondary, #f5f0eb); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 2rem; display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
  <div style="flex-shrink: 0;">
    <img src="../../assets/blog/sophia-truesight-avatar.jpg" alt="Sophia Truesight" style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover;" />
  </div>
  <div style="flex: 1; min-width: 200px;">
    <div style="font-size: 0.875rem; font-weight: 600; margin-bottom: 0.25rem;">Listen to this post</div>
    <div style="font-size: 0.8rem; color: var(--muted, #666);">Narrated by Sophia Truesight</div>
  </div>
  <audio controls preload="none" style="height: 40px; max-width: 100%;">
    <source src="../../assets/blog/narration-<post-slug>.mp3" type="audio/mpeg" />
    Your browser does not support the audio element.
  </audio>
</div>
```

6. **Update the HTML** on both beta and prod repos

## 4. Promote to production

- If the prod repo can be synced from beta (no CNAME divergence), use `sync_beta_to_prod`
- If sync fails due to history divergence, push the HTML file directly to `truesight_me_prod` via the Contents API
- Upload the narration MP3 to prod as well

## 5. Verify

- Visit the production URL and confirm the page renders correctly
- Click the audio player and confirm the narration plays
- Check OG meta tags render correctly in social previews
