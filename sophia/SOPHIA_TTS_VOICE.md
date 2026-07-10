# Sophia TTS Voice Configuration

**Status:** Prototype — voice samples generated 2026-06-06.

## Selected voice

**Microsoft Edge TTS: `en-US-AriaNeural`** (Female, "Positive, Confident")

Sample: https://raw.githubusercontent.com/TrueSightDAO/agentic_ai_context/main/voice_samples/sophia_voice_aria.mp3

## Why Aria

- **Positive, Confident** — matches the "competent senior engineer who doesn't need to prove anything" personality
- Female voice (matches the name Sophia)
- Clear enunciation — important for reading QR codes, ledger entries, and runbooks
- Measured pace — not rushed, not slow

## Runner-up voices

| Voice | Personality | Sample |
|---|---|---|
| Jenny | Friendly, Considerate, Comfort | [Listen](https://raw.githubusercontent.com/TrueSightDAO/agentic_ai_context/main/voice_samples/sophia_voice_jenny.mp3) |
| Ava | Expressive, Caring, Pleasant | [Listen](https://raw.githubusercontent.com/TrueSightDAO/agentic_ai_context/main/voice_samples/sophia_voice_ava.mp3) |
| Emma | Cheerful, Clear, Conversational | [Listen](https://raw.githubusercontent.com/TrueSightDAO/agentic_ai_context/main/voice_samples/sophia_voice_emma.mp3) |

## Production plan (not yet built)

1. **Phase 1 — Web Speech API** (browser-native, $0): Add a read-aloud toggle to truesight.me / dapp that uses the browser's `speechSynthesis` API. Quality varies by OS — best on macOS.
2. **Phase 2 — Self-hosted Coqui TTS** (one-time training, $0 runtime): Fine-tune an open-source TTS model on Aria's voice profile so Sophia has a unique, consistent voice that runs on our own infra. No recurring subscription.
3. **Phase 3 — Real-time voice conversation**: Add STT (already have faster-whisper) + TTS pipeline for two-way voice dialogue.

## Technical notes

- Voice generated via `edge-tts` (Microsoft Edge TTS, free, no API key needed)
- All samples stored in `agentic_ai_context/voice_samples/`
- For production, the voice ID `en-US-AriaNeural` should be stored in an environment variable or config file on the autopilot box
