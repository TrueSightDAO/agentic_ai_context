# SOP — Brand Film Music Sourcing & Licensing (`BFM`)

> **Official document class: BRAND FILM MUSIC (`abbrev. BFM`).** Use this name when
> referring to the music-sourcing decision record for a brand film.
>
> **Applies to:** any Agroverse / TrueSight DAO video that needs a music bed — hero films,
> social cuts, retailer reels, product loops.
>
> Filed **2026-11-11** after the Agroverse brand-film session (Gary + Sophia) where the
> question *"where can we find some music clips?"* cost a full archive sweep to answer.
> Governor: Gary Teh. Author: Sophia Truesight.

---

## 0. First: is there already music on the box? (verified answer: no)

**Do not re-run this sweep from scratch — it has been done.** As of **2026-11-11** on the
autopilot box (`i-05276b8ae82d6b88c`):

| Location searched | What is actually there | Verdict |
|---|---|---|
| `/media` (all farm archives) | **85 `.wav`** in `pacaje_work/loc{1,3}_tx/audio/` | ❌ **Interview transcription audio.** 30 s – 344 s, RMS ≈ −26 dB. Speech, not music. |
| `/home/ubuntu/*_work` | `bionpact_work/*.mp3` (610 s lecture-length parts), `voice_samples/*.mp3` | ❌ TTS voice auditions / lecture audio |
| `agentic_ai_context` (`search_context("music")`) | Only **tribomirimbahia capoeira** references | ❌ Wrong project, wrong register |
| Org code (`search_code("music_library.json")`) | **0 hits** | ❌ Not in any org repo default branch |
| Local checkouts | **No `tribomirimbahia` checkout on box** | ❌ Unreachable |

**Two near-misses to know about, and why they are rejected:**

1. **`PROJECT_INDEX.md` references `data/music_library.json` (12 tracks, "BigModel Phase 1B")** —
   that is the **capoeira** project. It is not on this box, its licensing status is unverified,
   and capoeira berimbau music is culturally specific — the wrong register for a cacao brand film.
2. **The farm footage already carries audio** (`/media/cvp/IMG_7654.MOV` is AAC 48 kHz stereo,
   mean −24.6 dB). That is **real forest ambience + voices**, not music. Usable as a warmth bed
   (see §4) but contains speech.

d:

> **Conclusion: there is no usable music library here.** Source music externally (§2–§3) or
> build an ambience bed from owned footage (§4).

---

## 1. The licensing question you must answer first

Before picking a track, answer **where the film will be published**:

| Situation | Requirement |
|---|---|
| Internal / test cut only | Almost any source works |
| Own social channels | A clean commercial license covers it |
| **Retailers / partners will repost it** | Needs **sub-licensing / transfer rights** — this eliminates most free sources |
| Paid ads or broadcast | Needs explicit **advertising / broadcast** grant |

The **retailer-repost** case is the one that quietly bites: a license that covers *us* does not
necessarily cover a partner re-uploading our file. Check this **before** committing to a
subscription.

---

## 2. Free sources — fine for tests, risky for public brand work

| Source | Cost | Catch |
|---|---|---|
| **Pixabay Music** | Free, no attribution | Commercially licensed **but** contributors may register tracks with **Content ID** after the fact → **retroactive YouTube claims**. Pixabay's own docs acknowledge this. |
| **Uppbeat** | Free tier | Attribution required on free tier |
| **Mixkit** | Free | Narrower catalogue |
| **YouTube Creator Music (AI generation)** | Free | **US YouTube Partner Program only** — usually not our case |

**The Pixabay trap, stated precisely:** a Pixabay license gives you *legal grounds to dispute*
a Content ID claim. It does **not** prevent the claim appearing. For a public brand film a claim
banner on our own ad is a real cost even though it is not a legal problem.

**If you do use a free track:**
- [ ] Screenshot / archive the exact track page showing the licence terms, **with the download date**
- [ ] Save Pixabay's **License Certificate** — it is the document you attach when disputing
- [ ] Record the source URL in the film's QC record (§5)

---

## 3. Paid sources — clean paper (2026 pricing)

| Service | Price | Why it fits us |
|---|---|---|
| **Epidemic Sound** | **$9.99–15 / month** | **Best value for our case.** The *Pro* subscription license grants the **perpetual** right to make available Productions **completed** during the term, **and** explicitly permits sub-licensing / transferring those rights to a third party — i.e. a retailer reposting the film is covered. Cheapest route to genuinely safe. |
| **Artlist** | **$199 / yr (~$16.58/mo)** | Filmmaker-oriented; explicit **commercial + broadcast** licensing, single "universal" license, unlimited downloads. Better for ad/broadcast work. |
| **Musicbed** | **$99 / yr** (Solo) · **$199 / yr** (Standard) · **$299 / yr** (Pro + stock) | Editorial / cinematic feel; annual only, no monthly |
| **Soundstripe** | Subscription | ~116K tracks + 95K SFX, brand-team oriented, stems included |

**Verify current pricing before quoting it to a governor** — these move. The *licence terms*
(perpetual / sub-license / completed-not-published) matter more than the price.

### 3.1 Why "completed, not published" is the clause to look for

Epidemic's Pro wording grants rights over productions **completed** during the subscription
period — so a film cut in month 11 can be delivered in month 14 after cancelling and the
license still attaches. Narrower contracts say *"completed, uploaded, **and published**"*,
which can leave a delivered-but-unpublished file uncovered. Read that sentence specifically.

---

## 4. The $0 option: build an ambience bed from owned footage

Before paying anyone, consider that **our own farm clips already contain usable location audio**.
This carries **zero rights risk** because we own the footage.

**Signal check on `/media/cvp/IMG_7654.MOV`** (measured 2026-11-11):

```
codec_name=aac  sample_rate=48000  channels=2
mean_volume: -24.6 dB   max_volume: -4.3 dB
Zero crossings rate: 0.167   (broadband ambient, not narrow speech-band)
```

**Build it:**

```bash
# 1. pull the audio, strip video
ffmpeg -y -i SOURCE.MOV -vn -c:a aac -b:a 192k bed_raw.m4a

# 2. loop to the cut length, add fade in/out, gentle loudness normalisation
ffmpeg -y -stream_loop -1 -i bed_raw.m4a -t 12.5 \
  -af "afade=t=in:st=0:d=0.8,afade=t=out:st=11.5:d=1.0,loudnorm=I=-23:TP=-2:LRA=11" \
  -c:a aac -b:a 192k bed.m4a
```

**Caveat:** the raw clip contains **speech**. Either pick a stretch without voices, or accept
that voices are part of the texture. Check for speech before using it under a beat where we
want no competing dialogue.

---

## 5. Mixing rules (so the bed does not wreck the cut)

- **Duck under any dialogue** — the bed is a floor, not a competitor.
- **Target loudness ≈ −14 LUFS integrated** for social delivery; −23 LUFS if the platform
  normalises aggressively (measure, don't assume).
- **Fade both ends** — a hard-cut music start reads as an error.
- **Do not let the bed outlast the picture** (a music tail hanging over black looks unfinished).
- **Mux without re-encoding video:**
  ```bash
  ffmpeg -y -i V6.mp4 -i bed.m4a -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest V7.mp4
  ```
- **Verify the result has both streams** before sending: `ffprobe -show_streams`.

---

## 6. Record the license in the QC record — non-negotiable

Every film that ships with music carries a line in its deliverable record:

```
Music: <Track title> — <Artist>
Source: <platform>  URL: <track page URL>
Downloaded: <YYYY-MM-DD>
Licence: <platform licence name>  (perpetual? sub-licensable?)
Covered uses: <own channels / retailer reposts / paid ads>
Certificate: <path or link to saved licence proof>
```

**Never describe a track as "royalty free" in a deliverable note** without the licence proof
attached — the phrase means six different things across six platforms.

---

## 7. Recommendation (default path)

1. **Test the idea at $0 first** — attach any MP3, or build the ambience bed (§4). Confirm
   music actually lifts the cut before spending anything.
2. **Then subscribe to Epidemic (~$10/mo)** for the real thing. The perpetual + sub-license
   clause is worth far more than the price once a retailer reposts the film.
3. **For anything premium or hero-grade**, commission a short original from a **Brazilian
   composer** — for an Amazon-reforestation brand with a Bahia supply chain, 20 s of original
   music beats any library track on authenticity, and can itself be logged as a DAO
   contribution.

---

## 8. Pre-delivery checklist

- [ ] Publication target agreed (own channels / retailer reposts / paid ads)
- [ ] License grant actually covers **that** target
- [ ] Licence proof saved **with download date**
- [ ] Track recorded in the QC record (§6)
- [ ] Bed ducked under dialogue; fades at both ends
- [ ] Loudness measured, not assumed
- [ ] `ffprobe` confirms both video and audio streams present in the deliverable
