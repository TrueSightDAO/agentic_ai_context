# Voice Response Implementation Plan

## Goal
Enable the TrueSight DAO Autopilot (Sentinel) to respond to voice messages with voice replies, using the designated voices per language.

## Designated Voices

| Language | Voice | Style |
|----------|-------|-------|
| English (default) | en-US-AriaNeural (Aria) | Positive, Confident |
| Mandarin (Chinese) | zh-CN-XiaoxiaoNeural (Xiaoxiao) | Warm, Natural |
| Portuguese (Brazilian) | pt-BR-FranciscaNeural (Francisca) | Friendly, Positive |

See `VOICE_DESIGNATION.md` for full details.

## Current State

The architecture already has most of the pieces:

1. **`telegram_adapter.py`** — handles Telegram messages, already transcribes voice notes via `voice.py` (faster-whisper), sends transcribed text to `/chat-blocking`, and replies with text
2. **`voice.py`** — has `transcribe_voice()` using faster-whisper (local, free, no API cost)
3. **`voice_samples/`** — we have designated voices already generated and stored
4. **`truesight_autopilot_transcript`** — already publishes text transcripts

## Requirements

### Voice Message → Voice Response
- When a governor sends a voice message, the autopilot should respond with a voice message
- The voice response should use the designated voice for the detected language

### URL Handling
- If the response contains URLs, the autopilot should send a follow-up text message listing the URLs
- The voice response should NOT recite URL values aloud

### Language Matching
- If the governor sends a voice message in a certain language, respond in the same language
- Supported languages: English (default), Mandarin Chinese, Portuguese
- Language detection via heuristic (CJK characters, Portuguese-specific patterns) or LLM

### Transcript Policy
- **Do NOT upload** the user's voice audio file to the GitHub transcript repo
- **Do NOT upload** the synthesized voice output to the repo
- Only upload the **text transcript** of both user message and assistant response

## Architecture

### New Module: `app/voice_output.py`

```python
# synthesize_voice(text, language) -> str (path to generated MP3)
# Uses edge-tts (Microsoft Edge TTS) — free, no API key, already installed on server
# Language -> voice mapping:
#   'en' -> en-US-AriaNeural
#   'zh' -> zh-CN-XiaoxiaoNeural
#   'pt' -> pt-BR-FranciscaNeural
# Output saved to /tmp/voice_responses/{uuid}.mp3
# Auto-cleanup via tempfile or background task
```

### Modified: `app/telegram_adapter.py`

**`handle_message()` changes:**
1. Voice note comes in → transcribe via `voice.py` (already works)
2. Detect language from transcription text
3. Send transcribed text to `/chat-blocking` (already works)
4. After getting text response:
   a. Call `synthesize_voice(response_text, detected_language)` → get MP3 path
   b. Send MP3 as voice reply via Telegram `sendVoice` API
   c. Parse response for URLs → if found, send separate text message listing them

### Modified: `app/main.py`

- Verify `_publish_transcript()` does not upload binary audio files (already the case — only text is published)

### Modified: `requirements.txt`

- Add `edge-tts` (already installed on server, but should be in requirements for reproducibility)

## Execution Roadmap

| Step | What | Files Changed | Effort |
|------|------|---------------|--------|
| 1 | Create `voice_output.py` with `synthesize_voice()` | New file | Small |
| 2 | Add `send_voice()` helper to `telegram_adapter.py` | `telegram_adapter.py` | Small |
| 3 | Add language detection helper | `telegram_adapter.py` | Tiny |
| 4 | Modify voice message handler to synthesize + send voice reply | `telegram_adapter.py` | Medium |
| 5 | Add URL extraction + follow-up text message | `telegram_adapter.py` | Small |
| 6 | Ensure transcript policy (no audio uploads) | `main.py` (_publish_transcript) | Tiny (verify) |
| 7 | Add `edge-tts` to `requirements.txt` | `requirements.txt` | Tiny |
| 8 | Deploy & test | — | Small |

## Checklist

### Phase 1: Voice Output Engine
- [ ] Create `app/voice_output.py`
- [ ] Implement `synthesize_voice(text, lang)` using `edge-tts`
- [ ] Language → voice mapping (en→Aria, zh→Xiaoxiao, pt→Francisca)
- [ ] Output to `/tmp/voice_responses/{uuid}.mp3`
- [ ] Auto-cleanup of old voice files

### Phase 2: Language Detection
- [ ] Implement `detect_language(text)` helper
- [ ] CJK character detection → Mandarin
- [ ] Portuguese-specific pattern detection → Portuguese
- [ ] Default → English

### Phase 3: Telegram Voice Reply
- [ ] Add `send_voice(chat_id, file_path, thread_id)` helper
- [ ] Modify voice message handler to call `synthesize_voice()` after getting response
- [ ] Send synthesized MP3 as voice reply via `sendVoice` API

### Phase 4: URL Follow-up
- [ ] Parse assistant response for `https?://` URLs
- [ ] If URLs found, send separate text message with URL list
- [ ] Do NOT recite URLs in voice response

### Phase 5: Transcript Policy
- [ ] Verify `_publish_transcript()` does not upload binary audio
- [ ] Confirm only text transcripts are published to `truesight_autopilot_transcript`

### Phase 6: Dependencies & Deploy
- [ ] Add `edge-tts` to `requirements.txt`
- [ ] Deploy to EC2
- [ ] Test: English voice → Aria voice reply
- [ ] Test: Mandarin voice → Xiaoxiao voice reply
- [ ] Test: Portuguese voice → Francisca voice reply
- [ ] Test: Response with URLs → voice reply + separate text with URLs
- [ ] Test: No audio files in transcript repo after conversation

### Future (DApp Chat)
- [ ] Add voice recording button to DApp chat UI (`chat.html`)
- [ ] Add `/chat/voice` endpoint accepting audio blob
- [ ] Same transcribe → LLM → synthesize → return audio URL flow
