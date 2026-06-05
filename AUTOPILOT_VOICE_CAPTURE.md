# Autopilot (Sophia) — voice-note capture (speech → text, on-box, free)

**Status:** LIVE on the Sophia box (`/opt/truesight_autopilot`, `truesight-autopilot-telegram.service`) since 2026-06-05 (PR `TrueSightDAO/truesight_autopilot#100`).

## What it does
Send Sophia a **Telegram voice note** (or audio / video-note) in any topic and she transcribes it **on the box** and treats the transcript as your message — it flows through the normal command + chat path, and the per-topic session/role is preserved. She echoes `🎤 Heard: <transcript>` so you can see what was understood.

This is the low-friction **weak-signal capture front door**: speak a thought (or paste a DM) into a Sophia topic and it lands in a machine-readable place instead of dying in WhatsApp. Matches Gary's verbal working style.

## How it works (for LLMs editing this)
- **`app/voice.py` → `transcribe_voice(path)`** — lazy-loads **faster-whisper** (`base`, `device="cpu"`, `compute_type="int8"`), cached for the process. Returns `""` on failure/silence.
- **Silence-hallucination guard:** drops segments with `no_speech_prob > 0.8` (Whisper emits "Obrigado por assistir" / "Thanks for watching" on near-silent audio — see the whisper-silence reference).
- **`app/telegram_adapter.py`** — `extract_voice_file_id()` detects `voice`/`audio`/`video_note`; the handler downloads it (`download_telegram_file` → `/tmp/tg_attachments`), calls `transcribe_voice`, sets `text = transcript`, and dispatches.
- **Cost: $0.** Open-source model runs locally; audio never leaves the box. (The hosted OpenAI Whisper API is ~$0.006/min — not used.)

## Dependencies (turnkey on a fresh clone)
- `requirements.txt` includes **`faster-whisper`** (installed by `start_local.sh`).
- `scripts/user-data.sh` apt line includes **`ffmpeg`** (system codec for OGG/Opus).
- First transcription downloads the `base` model (~150 MB) to `~/.cache/huggingface`; the box has been pre-warmed.

## ⚠️ Privacy boundary
Sophia's **full session transcripts are published to a PUBLIC repo** (`TrueSightDAO/truesight_autopilot_transcript/sessions/`). So **don't speak/paste raw private PII (e.g. someone's verbatim DM + name) you don't want on the public internet.** For private-DM weak-signal capture, the intended pattern is a **private** signals buffer + redaction-at-ingest — NOT the public transcript repo.

## Not built yet (intended pipeline)
Capture (voice/paste → transcript) is the first stage. Still to build: a **private signals buffer** + a weekly **synthesis step** that turns accumulated weak signals into *open questions* posted to the Beer Hall (the "re-open the loop" facilitator move) — see the participation/weak-signal discussion. File follow-ups in `OPEN_FOLLOWUPS.md`.
