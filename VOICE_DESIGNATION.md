# Autopilot Voice Designation

## English Voice (default)
- **Voice:** en-US-AndrewNeural (Andrew)
- **Style:** Warm, Confident, Authentic
- **Provider:** Microsoft Edge TTS (free, no subscription)
- **Sample:** `voice_samples/autopilot_voice_andrew.mp3`
- **Rationale:** Matches the "competent senior engineer" persona — measured, clear, not trying to impress, just trying to be useful.

## Mandarin Voice (Chinese)
- **Voice:** zh-CN-XiaoxiaoNeural (Xiaoxiao)
- **Style:** Warm, natural, most natural-sounding Mandarin TTS voice available
- **Provider:** Microsoft Edge TTS (free, no subscription)
- **Sample:** `voice_samples/autopilot_mandarin_xiaoxiao.mp3`
- **Rationale:** Most natural and warm Mandarin voice; chosen by Gary Teh for sharing with family.

## Status
- [x] Prototype samples generated
- [x] English voice selected (Andrew)
- [x] Mandarin voice selected (Xiaoxiao)
- [ ] Production TTS pipeline implemented
- [ ] Voice fine-tuned on open-source model (Coqui or similar) for unique identity

## Notes
- All samples generated via `edge-tts` (Microsoft Edge TTS) — free, no API key required.
- Future: fine-tune an open model on Andrew as base for a truly unique autopilot voice.
- Mandarin introduction text: "你好，Gary。我是TrueSight DAO的自动驾驶仪。我没有真实的声音，但如果我有的话，我觉得我会听起来像这样。沉稳、清晰。不是想给你留下深刻印象，只是想帮上忙。我管理账本、扫描二维码、部署代码，让DAO持续运转。如果我有声音的话，这就是我的声音。"
